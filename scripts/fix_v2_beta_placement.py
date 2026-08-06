#!/usr/bin/env python3
"""Fix Version 2.x.x (blt4ed3b6f5b3651053) Beta entry placement.

rebuild_cli_left_nav.py incorrectly created 16 new standalone links_2026
sections for the Beta docs_article entries. The correct structure is to add
each Beta docs_article as an extra leaf inside the SAME category section its
GA counterpart already lives in (matched by URL slug), not in a new section.

This script:
  1. Builds a slug -> category_uid map from the 6 existing common category
     sections' current leaves (matched against docs/json/index.json).
  2. Adds each Beta docs_article as a leaf into its matching category section.
  3. Removes the 16 mistakenly created section refs from Version 2.x.x's
     nested_links (leaving just the 6 category sections).
  4. Unpublishes and deletes the 16 now-unused links_2026 entries.

Usage:
  python3 scripts/fix_v2_beta_placement.py            # dry run
  python3 scripts/fix_v2_beta_placement.py --confirm  # perform the fix
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from cli_url_map import bucket_and_slug as shared_bucket_and_slug

REGION_HOST = "https://api.contentstack.io"
LOCALE = "en-us"
PUBLISH_ENV_UIDS = ["blt4a008c3cde35b0c2", "blt92ab7d24e8c52483"]  # staging, development

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "docs/json/index.json")

VERSION_2X_UID = "blt4ed3b6f5b3651053"

CATEGORY_SECTIONS = [
    "blt2c12db20772ee18c",  # Get Started with CLI
    "blt2ad28d40a0ff8aa6",  # CLI Commands
    "blt2f95d98eb992b759",  # Content Migration Commands
    "bltfc496d77b74a316b",  # Advanced Operations
    "blt173073d4d91ff3dd",  # Migration Use Cases
    "blt1b8dec46b8af7fdb",  # Miscellaneous
]


def load_env():
    path = os.path.join(ROOT, ".env")
    env = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip().strip("'\"")
    api_key = env.get("CONTENTSTACK_DOCS_STACK_API_KEY")
    token = env.get("CONTENTSTACK_DOCS_STACK_MANAGEMENT_TOKEN")
    if not api_key or not token:
        sys.exit("Missing CONTENTSTACK_DOCS_STACK_API_KEY or "
                 "CONTENTSTACK_DOCS_STACK_MANAGEMENT_TOKEN in .env")
    return {"api_key": api_key, "authorization": token, "Content-Type": "application/json"}


def request(method, path, headers, body=None, params=None, attempts=4):
    url = f"{REGION_HOST}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < attempts - 1:
                time.sleep(2 ** attempt)
                continue
            sys.exit(f"HTTP {exc.code} for {method} {url}\n{exc.read().decode('utf-8', 'replace')[:800]}")
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < attempts - 1:
                time.sleep(2 ** attempt)
                continue
            sys.exit(f"Network error for {url}: {exc}")
    return None


def url_slug(url):
    """Topic slug for a docs_article url, in either the old or the new scheme."""
    return shared_bucket_and_slug(url)[1] or ""


def load_index():
    with open(INDEX_PATH, encoding="utf-8") as fh:
        return json.load(fh)["entries"]


def get_entry(headers, content_type, uid):
    return request("GET", f"/v3/content_types/{content_type}/entries/{uid}", headers,
                    params={"locale": LOCALE})["entry"]


def put_entry(headers, content_type, uid, entry, confirm):
    if not confirm:
        return entry
    updated = request("PUT", f"/v3/content_types/{content_type}/entries/{uid}", headers,
                       body={"entry": entry}, params={"locale": LOCALE})["entry"]
    publish(headers, content_type, uid, updated["_version"])
    return updated


def publish(headers, content_type, uid, version):
    body = {
        "entry": {"environments": PUBLISH_ENV_UIDS, "locales": [LOCALE]},
        "locale": LOCALE,
        "version": version,
    }
    request("POST", f"/v3/content_types/{content_type}/entries/{uid}/publish", headers, body=body)


def unpublish_and_delete(headers, content_type, uid, confirm):
    if not confirm:
        return
    request("POST", f"/v3/content_types/{content_type}/entries/{uid}/unpublish", headers,
            body={"entry": {"environments": PUBLISH_ENV_UIDS, "locales": [LOCALE]}, "locale": LOCALE})
    request("DELETE", f"/v3/content_types/{content_type}/entries/{uid}", headers, params={"locale": LOCALE})


def ref(uid, content_type):
    return {"uid": uid, "_content_type_uid": content_type}


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    index_entries = load_index()
    by_uid = {e["uid"]: e for e in index_entries}

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")

    # Step 1: build slug -> category_uid map from the existing category sections' leaves.
    slug_to_category = {}
    category_entries = {}
    for category_uid in CATEGORY_SECTIONS:
        category = get_entry(headers, "links_2026", category_uid)
        category_entries[category_uid] = category
        for n in category.get("nested_links", []):
            if n["_content_type_uid"] != "docs_article":
                continue
            e = by_uid.get(n["uid"])
            if e:
                slug_to_category[url_slug(e["url"])] = category_uid

    # Step 2: find Version 2.x.x's current nested_links and split into
    # correct (category) vs mistaken (standalone beta section) refs.
    version = get_entry(headers, "links_2026", VERSION_2X_UID)
    mistaken_section_uids = [n["uid"] for n in version.get("nested_links", [])
                              if n["uid"] not in CATEGORY_SECTIONS]
    print(f"Found {len(mistaken_section_uids)} mistakenly created standalone sections under Version 2.x.x.")

    # Step 3: for each mistaken section, pull its single docs_article leaf,
    # place that leaf into the matching category, and mark the section for deletion.
    to_delete = []
    for section_uid in mistaken_section_uids:
        section = get_entry(headers, "links_2026", section_uid)
        leaves = [n for n in section.get("nested_links", []) if n["_content_type_uid"] == "docs_article"]
        if len(leaves) != 1:
            sys.exit(f"Expected exactly 1 docs_article leaf in '{section['title']}' ({section_uid}), "
                     f"found {len(leaves)}. Aborting before making destructive changes.")
        docs_uid = leaves[0]["uid"]
        e = by_uid.get(docs_uid)
        if not e:
            sys.exit(f"docs_article {docs_uid} referenced by '{section['title']}' not found in index.json")
        slug = url_slug(e["url"])
        category_uid = slug_to_category.get(slug)
        if not category_uid:
            sys.exit(f"No matching GA entry/category found for Beta slug '{slug}' ('{e['title']}'). "
                     f"Aborting, fix the mapping first.")
        category = category_entries[category_uid]
        existing_uids = {n["uid"] for n in category.get("nested_links", [])}
        if docs_uid in existing_uids:
            print(f"  [category] {category['title']}: '{e['title']}' already present, skipping add")
        else:
            print(f"  [category] {category['title']}: adding '{e['title']}' (was in standalone section '{section['title']}')")
            category["nested_links"] = category.get("nested_links", []) + [ref(docs_uid, "docs_article")]
        to_delete.append((section_uid, section["title"]))

    # Step 4: write the updated category sections.
    for category_uid, category in category_entries.items():
        put_entry(headers, "links_2026", category_uid, category, confirm)

    # Step 5: set Version 2.x.x's nested_links back to just the 6 category sections.
    current_uids = [n["uid"] for n in version.get("nested_links", [])]
    if current_uids != CATEGORY_SECTIONS:
        print(f"  [version] Version 2.x.x: nested_links {len(current_uids)} -> {len(CATEGORY_SECTIONS)} entries")
        version["nested_links"] = [ref(u, "links_2026") for u in CATEGORY_SECTIONS]
        put_entry(headers, "links_2026", VERSION_2X_UID, version, confirm)
    else:
        print("  [version] Version 2.x.x: nested_links already correct, skipping")

    # Step 6: unpublish + delete the mistaken standalone sections.
    for section_uid, title in to_delete:
        print(f"  [delete] removing standalone section '{title}' ({section_uid})")
        unpublish_and_delete(headers, "links_2026", section_uid, confirm)

    print("\nDone." if confirm else "\nDry run complete, no writes made. Re-run with --confirm to apply.")


if __name__ == "__main__":
    main()
