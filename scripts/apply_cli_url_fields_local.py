#!/usr/bin/env python3
"""Phase 1: apply the new url, title and seo.title to the local docs/json snapshot.

Reads the frozen mapping in cli-url-map.csv and, for each of the 73 tracked CLI
docs, rewrites those three fields, renames the JSON and markdown files onto the
new slug, and updates docs/json/index.json to match. Stale markdown from a renamed
slug is removed so json_to_markdown.py does not leave an orphan behind.

The two asset-scanning-in-cli drafts are not in index.json (no uid assigned yet),
so they are handled from UNTRACKED_DRAFTS using the same rules. Creating them in
Contentstack stays outside this task.

In-content cross-links are a separate pass, see rewrite_cli_links.py.

Usage:
  python3 scripts/apply_cli_url_fields_local.py            # dry run
  python3 scripts/apply_cli_url_fields_local.py --confirm  # write the files
"""

import json
import os
import sys

import cli_url_map as url_map
from cli_docs_common import ROOT, load_index, save_index

JSON_DIR = os.path.join(ROOT, "docs", "json")
MD_DIR = os.path.join(ROOT, "docs", "markdown")

# Local drafts with no uid yet, keyed by the docs/json path they live at.
UNTRACKED_DRAFTS = [
    ("GA", "asset-scanning-in-cli"),
    ("Beta", "asset-scanning-in-cli"),
]


def read_json(rel_path):
    with open(os.path.join(JSON_DIR, rel_path), encoding="utf-8") as fh:
        return json.load(fh)


def write_json(rel_path, entry):
    with open(os.path.join(JSON_DIR, rel_path), "w", encoding="utf-8") as fh:
        json.dump(entry, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def plan_doc(doc):
    """Return (entry, changes) for a tracked doc, or (None, []) if already applied."""
    source = doc["old_json"] if os.path.exists(os.path.join(JSON_DIR, doc["old_json"])) \
        else doc["new_json"]
    if not os.path.exists(os.path.join(JSON_DIR, source)):
        sys.exit(f"{doc['bucket']}/{doc['slug']}: neither {doc['old_json']} nor "
                 f"{doc['new_json']} exists on disk")
    entry = read_json(source)
    seo = entry.setdefault("seo", {})
    changes = []
    if entry.get("url") != doc["new_url"]:
        changes.append(("url", entry.get("url"), doc["new_url"]))
    if entry.get("title") != doc["new_title"]:
        changes.append(("title", entry.get("title"), doc["new_title"]))
    if (seo.get("title") or "") != doc["new_seo_title"]:
        changes.append(("seo.title", seo.get("title"), doc["new_seo_title"]))
    entry["url"] = doc["new_url"]
    entry["title"] = doc["new_title"]
    seo["title"] = doc["new_seo_title"]
    return entry, changes, source


def plan_draft(bucket, slug):
    rel = f"{bucket}/{slug}.json"
    path = os.path.join(JSON_DIR, rel)
    if not os.path.exists(path):
        return None
    entry = read_json(rel)
    new_url = url_map.new_url(slug, bucket)
    new_title = url_map.new_title(entry.get("title") or "", bucket)
    new_seo = url_map.new_seo_title((entry.get("seo") or {}).get("title") or "",
                                    bucket, slug)
    if new_title is None:
        sys.exit(f"{rel}: title {entry.get('title')!r} ends in an unrecognized "
                 f"version segment, add it to VERSION_QUALIFIERS")
    return {"rel": rel, "entry": entry, "bucket": bucket, "slug": slug,
            "new_url": new_url, "new_title": new_title, "new_seo_title": new_seo}


def main():
    confirm = "--confirm" in sys.argv
    docs = url_map.load_map()

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")

    renames, edits, writes = [], 0, []
    for doc in sorted(docs, key=lambda d: (d["slug"], d["bucket"])):
        entry, changes, source = plan_doc(doc)
        if changes:
            edits += 1
            print(f"{doc['bucket']}/{doc['slug']}")
            for field, before, after in changes:
                print(f"   {field:9} {before!r}")
                print(f"   {' ' * 9} -> {after!r}")
        if source != doc["new_json"]:
            renames.append((source, doc["new_json"], doc["old_markdown"],
                            doc["new_markdown"]))
        writes.append((doc["new_json"], entry, source))

    drafts = [d for d in (plan_draft(b, s) for b, s in UNTRACKED_DRAFTS) if d]
    if drafts:
        print("\nUntracked local drafts (no uid, not pushed by this task):")
        for draft in drafts:
            print(f"  {draft['rel']}")
            print(f"     url       {draft['entry'].get('url')!r} -> {draft['new_url']!r}")
            print(f"     title     {draft['entry'].get('title')!r} -> {draft['new_title']!r}")
            print(f"     seo.title {(draft['entry'].get('seo') or {}).get('title')!r} "
                  f"-> {draft['new_seo_title']!r}")

    print(f"\n{edits} tracked doc(s) with field changes, {len(renames)} file rename(s).")

    if not confirm:
        print("\nDry run complete, no writes made.")
        return

    for rel, entry, source in writes:
        write_json(rel, entry)
        if source != rel:
            os.remove(os.path.join(JSON_DIR, source))

    for _, _, old_md, new_md in renames:
        stale = os.path.join(MD_DIR, old_md)
        if old_md != new_md and os.path.exists(stale):
            os.remove(stale)

    for draft in drafts:
        entry = draft["entry"]
        entry["url"] = draft["new_url"]
        entry["title"] = draft["new_title"]
        if draft["new_seo_title"] is not None:
            entry.setdefault("seo", {})["title"] = draft["new_seo_title"]
        write_json(draft["rel"], entry)

    index = load_index()
    by_uid = {d["uid"]: d for d in docs}
    for record in index["entries"]:
        doc = by_uid.get(record["uid"])
        if not doc:
            sys.exit(f"index.json has uid {record['uid']} with no row in cli-url-map.csv")
        record["url"] = doc["new_url"]
        record["title"] = doc["new_title"]
        record["slug"] = doc["new_slug"]
        record["json"] = doc["new_json"]
        record["markdown"] = doc["new_markdown"]
    index["entries"].sort(key=lambda e: e["url"])
    save_index(index)

    print(f"\nRewrote {len(writes)} JSON file(s), renamed {len(renames)}, "
          f"updated {len(drafts)} draft(s), refreshed index.json.")
    print("Next: python3 scripts/rewrite_cli_links.py")


if __name__ == "__main__":
    main()
