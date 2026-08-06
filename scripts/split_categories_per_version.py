#!/usr/bin/env python3
"""Split the shared 6 category sections into independent per-version copies.

The 6 common category sections (Get Started with CLI, CLI Commands, Content
Migration Commands, Advanced Operations, Migration Use Cases, Miscellaneous)
were shared links_2026 entries referenced by all three version entries. That
was fine while they only held common GA docs_article leaves, but it breaks
down once a version needs its own extra leaves merged into a category (e.g.
Beta docs for Version 2.x.x) because Contentstack references are shared, not
per-parent copies: any leaf added to a shared section becomes visible under
every version that references it.

Version 1.x.x needs nothing extra, so it keeps referencing the original
("master") 6 sections directly.

Version 0.x.x and Version 2.x.x each get their own independent copy of the 6
category sections (title suffixed with the version, e.g. "Get Started with
CLI (0.x.x)"), seeded with the same GA leaves as the master. Version 2.x.x's
copies additionally get the 16 Beta docs_article entries merged in, each
placed in the same category as its GA counterpart (matched by URL slug).
Version 0.x.x's copies are left as a plain duplicate of the GA leaves (its
old-commands entries stay in the existing separate flat placeholder
sections, unchanged).

Usage:
  python3 scripts/split_categories_per_version.py            # dry run
  python3 scripts/split_categories_per_version.py --confirm  # perform the split
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

VERSION_UIDS = {
    "0.x.x": "bltec579cd326694d5b",
    "1.x.x": "bltd7ee0a881bc07d3a",
    "2.x.x": "blt4ed3b6f5b3651053",
}

MASTER_CATEGORY_SECTIONS = [
    "blt2c12db20772ee18c",  # Get Started with CLI
    "blt2ad28d40a0ff8aa6",  # CLI Commands
    "blt2f95d98eb992b759",  # Content Migration Commands
    "bltfc496d77b74a316b",  # Advanced Operations
    "blt173073d4d91ff3dd",  # Migration Use Cases
    "blt1b8dec46b8af7fdb",  # Miscellaneous (has CLI FAQs nested inside)
]

OLD_PLACEHOLDER_SECTIONS = [
    "blt45854a5d73468a18", "blt958b427a4420c455", "blt358d8859bfc7c1d7",
    "blt47e1aee3f29c1645", "blt4b894a7acc6d256e", "blt4b57a07d3a71d71a",
    "blt3fbf41b5381dc57d", "bltb9a68f60b49ddf8e", "blt428ef74cfa6ebf17",
    "blt7db34983963e5e6d", "blt219fa41cd0eec69e", "blt001a7f708f23aa6c",
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


def find_by_title(headers, content_type, title):
    result = request("GET", f"/v3/content_types/{content_type}/entries", headers,
                      params={"locale": LOCALE, "query": json.dumps({"title": title})})
    entries = result.get("entries", [])
    return entries[0] if entries else None


def publish(headers, content_type, uid, version):
    body = {
        "entry": {"environments": PUBLISH_ENV_UIDS, "locales": [LOCALE]},
        "locale": LOCALE,
        "version": version,
    }
    request("POST", f"/v3/content_types/{content_type}/entries/{uid}/publish", headers, body=body)


def put_entry(headers, content_type, uid, entry, confirm):
    if not confirm:
        return entry
    updated = request("PUT", f"/v3/content_types/{content_type}/entries/{uid}", headers,
                       body={"entry": entry}, params={"locale": LOCALE})["entry"]
    publish(headers, content_type, uid, updated["_version"])
    return updated


def post_entry(headers, content_type, title, nested_links, confirm):
    if not confirm:
        return {"uid": f"<new:{title}>", "title": title, "nested_links": nested_links}
    existing = find_by_title(headers, content_type, title)
    if existing:
        return existing
    created = request("POST", f"/v3/content_types/{content_type}/entries", headers,
                       body={"entry": {"title": title, "nested_links": nested_links, "tags": []}},
                       params={"locale": LOCALE})["entry"]
    publish(headers, content_type, created["uid"], created["_version"])
    return created


def ref(uid, content_type):
    return {"uid": uid, "_content_type_uid": content_type}


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    index_entries = load_index()
    by_uid = {e["uid"]: e for e in index_entries}
    beta_entries = [e for e in index_entries if e["bucket"] == "Beta"]

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")

    masters = {uid: get_entry(headers, "links_2026", uid) for uid in MASTER_CATEGORY_SECTIONS}

    # slug -> master category uid, from the master categories' current (GA-only) leaves.
    slug_to_master_category = {}
    for uid, cat in masters.items():
        for n in cat.get("nested_links", []):
            if n["_content_type_uid"] != "docs_article":
                continue
            e = by_uid.get(n["uid"])
            if e:
                slug_to_master_category[url_slug(e["url"])] = uid

    # Build duplicate category sets for 0.x.x and 2.x.x.
    duplicate_category_uids = {"0.x.x": [], "2.x.x": []}
    duplicate_category_by_master_uid = {"0.x.x": {}, "2.x.x": {}}

    for version in ("0.x.x", "2.x.x"):
        for master_uid, master in masters.items():
            title = f"{master['title']} ({version})"
            base_leaves = list(master.get("nested_links", []))
            print(f"  [duplicate] creating/finding '{title}' with {len(base_leaves)} GA leaves")
            created = post_entry(headers, "links_2026", title, base_leaves, confirm)
            duplicate_category_uids[version].append(created["uid"])
            duplicate_category_by_master_uid[version][master_uid] = created

    # Merge the 16 Beta docs_article entries into Version 2.x.x's duplicate categories.
    for e in beta_entries:
        slug = url_slug(e["url"])
        master_uid = slug_to_master_category.get(slug)
        if not master_uid:
            sys.exit(f"No matching GA category for Beta slug '{slug}' ('{e['title']}'). Aborting.")
        dup = duplicate_category_by_master_uid["2.x.x"][master_uid]
        existing_uids = {n["uid"] for n in dup.get("nested_links", [])}
        if e["uid"] in existing_uids:
            print(f"  [2.x.x category] {dup['title']}: '{e['title']}' already present, skipping")
            continue
        print(f"  [2.x.x category] {dup['title']}: adding '{e['title']}'")
        dup["nested_links"] = dup.get("nested_links", []) + [ref(e["uid"], "docs_article")]

    # Write back the (possibly Beta-augmented) 2.x.x duplicate categories.
    if confirm:
        for dup in duplicate_category_by_master_uid["2.x.x"].values():
            if not dup["uid"].startswith("<new:"):
                put_entry(headers, "links_2026", dup["uid"], dup, confirm)

    # Point Version 0.x.x and Version 2.x.x at their own duplicate categories
    # (+ the existing old-commands placeholders for 0.x.x). Version 1.x.x keeps
    # referencing the master sections directly, unchanged.
    version_targets = {
        "0.x.x": duplicate_category_uids["0.x.x"] + OLD_PLACEHOLDER_SECTIONS,
        "2.x.x": duplicate_category_uids["2.x.x"],
    }
    for version, target_uids in version_targets.items():
        version_uid = VERSION_UIDS[version]
        entry = get_entry(headers, "links_2026", version_uid)
        current_uids = [n["uid"] for n in entry.get("nested_links", [])]
        if confirm and any(u.startswith("<new:") for u in target_uids):
            sys.exit("internal error: unresolved new-section placeholder uid")
        if current_uids == target_uids:
            print(f"  [version] {entry['title']}: nested_links already correct, skipping")
            continue
        print(f"  [version] {entry['title']}: nested_links {len(current_uids)} -> {len(target_uids)} entries")
        entry["nested_links"] = [ref(u, "links_2026") for u in target_uids]
        put_entry(headers, "links_2026", version_uid, entry, confirm)

    print("\nDone." if confirm else "\nDry run complete, no writes made. Re-run with --confirm to apply.")


if __name__ == "__main__":
    main()
