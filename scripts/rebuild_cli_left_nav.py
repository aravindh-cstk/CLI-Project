#!/usr/bin/env python3
"""Rebuild the CLI left navigation (links_2026 content type) per version.

Version 0.x.x should show: the common (GA-bucket) category sections + the
old-commands (bucket "old") entries, nested under their existing placeholder
sections.
Version 1.x.x should show: only the common (GA-bucket) category sections.
Version 2.x.x should show: the common (GA-bucket) category sections + the
beta (bucket "Beta") entries, each in a new flat section mirroring the
old-commands pattern.

"Common" grouping is derived from docs/json/index.json's bucket field, which
in turn is derived from the docs_article URL suffix (/old-commands, /beta,
or neither). See scripts/fetch_cli_docs.py for that bucketing rule.

Usage:
  python3 scripts/rebuild_cli_left_nav.py            # dry run: show the plan, no writes
  python3 scripts/rebuild_cli_left_nav.py --confirm  # perform the updates + publish
  python3 scripts/rebuild_cli_left_nav.py --verify   # re-fetch live trees and print a report
"""

import json
import os
import re
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

# The 6 common category sections, already correctly attached to Version 2.x.x.
CATEGORY_SECTIONS = [
    "blt2c12db20772ee18c",  # Get Started with CLI
    "blt2ad28d40a0ff8aa6",  # CLI Commands
    "blt2f95d98eb992b759",  # Content Migration Commands
    "bltfc496d77b74a316b",  # Advanced Operations
    "blt173073d4d91ff3dd",  # Migration Use Cases
    "blt1b8dec46b8af7fdb",  # Miscellaneous (has CLI FAQs nested inside already)
]

# The 12 pre-created but empty old-commands placeholder sections under Version 0.x.x.
OLD_PLACEHOLDER_SECTIONS = [
    "blt45854a5d73468a18",
    "blt958b427a4420c455",
    "blt358d8859bfc7c1d7",
    "blt47e1aee3f29c1645",
    "blt4b894a7acc6d256e",
    "blt4b57a07d3a71d71a",
    "blt3fbf41b5381dc57d",
    "bltb9a68f60b49ddf8e",
    "blt428ef74cfa6ebf17",
    "blt7db34983963e5e6d",
    "blt219fa41cd0eec69e",
    "blt001a7f708f23aa6c",
]

# 8 GA-bucket docs_article entries not yet in any category section, and where
# they should go. Confirmed with the user.
#
# asset-scanning-in-cli was created after the production nav was last built, and
# its nav placement is deliberately left to this script rather than pushed to
# production on its own: the Advanced Operations draft already holds an
# un-deployed restructure change that removes a link, so publishing that entry
# now would drop Taxonomy Migration out of the live nav.
MISSING_GA_SLUG_TO_CATEGORY = {
    "asset-scanning-in-cli": "bltfc496d77b74a316b",          # Advanced Operations
    "branches-migration-use-cases": "blt173073d4d91ff3dd",   # Migration Use Cases
    "bulk-operations-in-cli": "bltfc496d77b74a316b",         # Advanced Operations
    "cli-for-cs-assets": "bltfc496d77b74a316b",              # Advanced Operations
    "configure-mfa-secret-using-cli": "bltfc496d77b74a316b", # Advanced Operations
    "create-custom-cli-commands": "blt1b8dec46b8af7fdb",     # Miscellaneous
    "uninstall-cli-plugins": "blt1b8dec46b8af7fdb",          # Miscellaneous
    "useful-plugins": "blt1b8dec46b8af7fdb",                 # Miscellaneous
}


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


def slugify(text):
    text = text.split("|")[0].strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


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


def find_by_title(headers, content_type, title):
    result = request("GET", f"/v3/content_types/{content_type}/entries", headers,
                      params={"locale": LOCALE, "query": json.dumps({"title": title})})
    entries = result.get("entries", [])
    return entries[0] if entries else None


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


def publish(headers, content_type, uid, version):
    body = {
        "entry": {"environments": PUBLISH_ENV_UIDS, "locales": [LOCALE]},
        "locale": LOCALE,
        "version": version,
    }
    request("POST", f"/v3/content_types/{content_type}/entries/{uid}/publish", headers, body=body)


def ref(uid, content_type):
    return {"uid": uid, "_content_type_uid": content_type}


def build_plan(index_entries):
    by_slug = {}
    for e in index_entries:
        slug = url_slug(e["url"])
        by_slug.setdefault(slug, {})[e["bucket"]] = e

    old_by_slug = {slug: b["old"] for slug, b in by_slug.items() if "old" in b}
    beta_by_slug = {slug: b["Beta"] for slug, b in by_slug.items() if "Beta" in b}
    ga_by_slug = {slug: b["GA"] for slug, b in by_slug.items() if "GA" in b}

    return old_by_slug, beta_by_slug, ga_by_slug


def match_old_placeholder(headers, old_by_slug):
    """Match each of the 12 empty placeholder sections to its old-commands docs_article uid."""
    matches = {}
    unmatched_placeholders = []
    for section_uid in OLD_PLACEHOLDER_SECTIONS:
        section = get_entry(headers, "links_2026", section_uid)
        key = slugify(section["title"])
        docs_entry = old_by_slug.get(key)
        if not docs_entry:
            unmatched_placeholders.append((section_uid, section["title"]))
            continue
        matches[section_uid] = (section, docs_entry)
    if unmatched_placeholders:
        sys.exit(f"Could not match these old-commands placeholder sections to a docs_article "
                 f"entry by slug, fix the mapping before proceeding: {unmatched_placeholders}")
    matched_slugs = {slugify(s["title"]) for s, _ in matches.values()}
    unclaimed = set(old_by_slug) - matched_slugs
    if unclaimed:
        sys.exit(f"These old-commands docs_article entries have no matching placeholder "
                 f"section: {[old_by_slug[s]['title'] for s in unclaimed]}")
    return matches


def main():
    confirm = "--confirm" in sys.argv
    verify_only = "--verify" in sys.argv
    headers = load_env()
    index_entries = load_index()
    old_by_slug, beta_by_slug, ga_by_slug = build_plan(index_entries)

    if verify_only:
        verify(headers)
        return

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")

    # Step 1: match the 12 old-commands placeholders to their docs_article uid.
    old_matches = match_old_placeholder(headers, old_by_slug)
    print(f"Matched {len(old_matches)}/12 old-commands placeholder sections to their docs_article entry.")

    # Step 2: fill each old-commands placeholder's nested_links.
    for section_uid, (section, docs_entry) in old_matches.items():
        current = [n["uid"] for n in section.get("nested_links", [])]
        target = [docs_entry["uid"]]
        if current == target:
            print(f"  [old] {section['title']}: already correct, skipping")
            continue
        print(f"  [old] {section['title']}: nested_links {current} -> {target}")
        section["nested_links"] = [ref(docs_entry["uid"], "docs_article")]
        put_entry(headers, "links_2026", section_uid, section, confirm)

    # Step 3: add the 7 missing GA docs_article entries into their category section.
    for slug, category_uid in MISSING_GA_SLUG_TO_CATEGORY.items():
        docs_entry = ga_by_slug.get(slug)
        if not docs_entry:
            sys.exit(f"Expected a GA docs_article for slug '{slug}' but found none in index.json")
        category = get_entry(headers, "links_2026", category_uid)
        existing_uids = {n["uid"] for n in category.get("nested_links", [])}
        if docs_entry["uid"] in existing_uids:
            print(f"  [category] {category['title']}: '{docs_entry['title']}' already present, skipping")
            continue
        print(f"  [category] {category['title']}: adding '{docs_entry['title']}'")
        category["nested_links"] = category.get("nested_links", []) + [ref(docs_entry["uid"], "docs_article")]
        put_entry(headers, "links_2026", category_uid, category, confirm)

    # Step 4: create 16 new flat Beta sections, mirroring the old-commands pattern.
    new_beta_section_uids = []
    for slug, docs_entry in beta_by_slug.items():
        title = docs_entry["title"].split("|")[0].strip()
        title = re.sub(r"^\[.*?\]\s*-\s*", "", title).strip() + " | Beta"
        print(f"  [beta] creating new section '{title}' -> '{docs_entry['title']}'")
        created = post_entry(headers, "links_2026", title, [ref(docs_entry["uid"], "docs_article")], confirm)
        new_beta_section_uids.append(created["uid"])

    # Step 5: set each version's top-level nested_links.
    version_targets = {
        "0.x.x": CATEGORY_SECTIONS + OLD_PLACEHOLDER_SECTIONS,
        "1.x.x": CATEGORY_SECTIONS,
        "2.x.x": CATEGORY_SECTIONS + new_beta_section_uids,
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
        entry["nested_links"] = [
            ref(u, "links_2026") for u in target_uids
        ]
        put_entry(headers, "links_2026", version_uid, entry, confirm)

    print("\nDone." if confirm else "\nDry run complete, no writes made. Re-run with --confirm to apply.")


def walk(headers, uid, depth=0, path=""):
    e = get_entry(headers, "links_2026", uid)
    title = e["title"]
    leaves = []
    print("  " * depth + f"[SECTION] {title} ({uid})")
    for n in e.get("nested_links", []):
        if n["_content_type_uid"] == "links_2026":
            leaves.extend(walk(headers, n["uid"], depth + 1, path + "/" + title))
        else:
            leaves.append(n["uid"])
    return leaves


def verify(headers):
    index_entries = load_index()
    by_uid = {e["uid"]: e for e in index_entries}
    for version, version_uid in VERSION_UIDS.items():
        print(f"\n=== Version {version} ===")
        leaves = walk(headers, version_uid)
        buckets = {}
        for uid in leaves:
            e = by_uid.get(uid)
            bucket = e["bucket"] if e else "unknown"
            buckets[bucket] = buckets.get(bucket, 0) + 1
        print(f"  Leaf docs_article count: {len(leaves)}, by bucket: {buckets}")


if __name__ == "__main__":
    main()
