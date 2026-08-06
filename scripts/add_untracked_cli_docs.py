#!/usr/bin/env python3
"""Pull the four CLI plugin docs that live outside the CLI breadcrumb into docs/json.

fetch_cli_docs.py scopes on the "Command-line Interface (CLI)" navigation node or
a "[Contentstack Command-line Interface (CLI)]" title prefix. The Content Type
Plugin and Regex Validate Plugin docs match neither (their titles use the older
"[Command Line Interface] - " prefix), so they were never tracked, even though
they are live CLI docs with a GA and a Beta variant each.

The URL restructure has to move them too, so this fetches them at their live
production version, writes them alongside the other docs, and appends them to
docs/json/index.json. Unlike a full fetch_cli_docs.py run this touches only the
four new files plus index.json, so local edits to the other 69 docs survive.

Usage:
  python3 scripts/add_untracked_cli_docs.py            # dry run
  python3 scripts/add_untracked_cli_docs.py --confirm  # write the files
"""

import json
import os
import sys

from cli_docs_common import (DOCS_ARTICLE, PROD_ENV_UID, ROOT, get_entry,
                             is_published_to, load_env, load_index, save_index)

# uid -> (bucket, slug). Confirmed live in production, GA plus Beta for each family.
UNTRACKED = {
    "bltb2268be653f55338": ("GA", "cli-content-type-plugin"),
    "blt8012fa025c919ece": ("Beta", "cli-content-type-plugin"),
    "blt33b42b2ce32f4cb4": ("GA", "cli-regex-validate-plugin"),
    "blt50c45d9983b508a7": ("Beta", "cli-regex-validate-plugin"),
}


def prod_record(entry):
    for record in entry.get("publish_details") or []:
        if record.get("environment") == PROD_ENV_UID and record.get("locale") == "en-us":
            return record
    return None


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    index = load_index()
    known = {e["uid"] for e in index["entries"]}

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")

    added = []
    for uid, (bucket, slug) in UNTRACKED.items():
        if uid in known:
            print(f"{bucket}/{slug} ({uid}): already in index.json, skipping")
            continue

        stub = get_entry(headers, DOCS_ARTICLE, uid)
        record = prod_record(stub)
        if not record:
            sys.exit(f"{uid} is not published to production, refusing to track it")

        entry = get_entry(headers, DOCS_ARTICLE, uid, version=record["version"])
        if entry.get("_version") != record["version"]:
            sys.exit(f"{uid}: asked for v{record['version']}, got v{entry.get('_version')}")

        rel = f"{bucket}/{slug}.json"
        print(f"{rel}  v{record['version']}  url={entry.get('url')}")
        print(f"   title: {entry.get('title')}")

        added.append({
            "url": entry.get("url"),
            "uid": uid,
            "title": entry.get("title"),
            "bucket": bucket,
            "slug": slug,
            "production_version": record["version"],
            "latest_version": stub.get("_version"),
            "published_at": record.get("time"),
            "json": rel,
            "markdown": f"{bucket}/{slug}.md",
            "entry": entry,
        })

    if not added:
        print("\nNothing to add.")
        return

    if not confirm:
        print(f"\nDry run complete. {len(added)} entry file(s) and "
              f"{len(added)} index row(s) would be written.")
        return

    for record in added:
        entry = record.pop("entry")
        path = os.path.join(ROOT, "docs", "json", record["json"])
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(entry, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print(f"wrote docs/json/{record['json']}")

    index["entries"] = sorted(index["entries"] + added, key=lambda e: e["url"])
    counts = {}
    for e in index["entries"]:
        counts[e["bucket"]] = counts.get(e["bucket"], 0) + 1
    index["total"] = len(index["entries"])
    index["counts"] = {b: counts.get(b, 0) for b in ("GA", "Beta", "old")}
    save_index(index)
    print(f"\nindex.json now tracks {index['total']} entries: {index['counts']}")


if __name__ == "__main__":
    main()
