#!/usr/bin/env python3
"""Phase 3: push the new url, title, seo.title and cross-links to Contentstack.

Transforms are applied to the entry fetched live, not to the local docs/json
snapshot, so a doc edited in the CMS since the last fetch keeps those edits and
only the fields this restructure owns change. Where the live content differs from
the local snapshot the run says so, since that means docs/json is behind.

Per entry: GET fresh, set url from the frozen map, relabel title and seo.title,
strip any version qualifier from the visible heading, repoint CLI cross-links,
PUT, publish to staging plus development, then add the new version to the docs
release.

Ordering: this must run before create_cli_redirects.py, otherwise every redirect
target 404s.

Usage:
  python3 scripts/push_cli_url_changes.py            # dry run
  python3 scripts/push_cli_url_changes.py --confirm  # update, publish, add to release
"""

import json
import os
import sys
import time

import cli_release
import cli_url_map as url_map
import rewrite_cli_links
from cli_docs_common import (DOCS_ARTICLE, LOCALE, ROOT, article_section,
                             get_entry, load_env, publish_entry, put_entry)


JSON_DIR = os.path.join(ROOT, "docs", "json")


def local_content(doc):
    """article_section.content from the local snapshot, for drift comparison."""
    path = os.path.join(JSON_DIR, f"{doc['bucket']}/{doc['new_slug']}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return article_section(json.load(fh)).get("content")


def plan_entry(entry, doc, docs, lookup):
    """Mutate entry in place. Returns the list of (field, before, after) changes."""
    changes = []

    # Read before the url is overwritten below. A doc whose url is already the new
    # one has been pushed before, so its bare CLI links are final.
    migrated = entry.get("url") == doc["new_url"]

    if entry.get("url") != doc["new_url"]:
        changes.append(("url", entry.get("url"), doc["new_url"]))
        entry["url"] = doc["new_url"]

    live_title = entry.get("title") or ""
    new_title = url_map.new_title(live_title, doc["bucket"])
    if new_title is None:
        sys.exit(f"{doc['uid']}: live title {live_title!r} ends in an unrecognized "
                 f"version segment. Add it to VERSION_QUALIFIERS in cli_url_map.py.")
    if new_title != live_title:
        changes.append(("title", live_title, new_title))
        entry["title"] = new_title

    seo = entry.setdefault("seo", {})
    live_seo = seo.get("title") or ""
    new_seo = url_map.new_seo_title(live_seo, doc["bucket"], doc["slug"])
    if new_seo is None:
        sys.exit(f"{doc['uid']}: live seo.title {live_seo!r} has no brand segment "
                 f"and no SEO_TITLE_OVERRIDES value.")
    if new_seo != live_seo:
        changes.append(("seo.title", live_seo, new_seo))
        seo["title"] = new_seo

    section = article_section(entry)
    live_heading = section.get("heading") or ""
    cleaned = url_map.clean_heading(live_heading)
    if cleaned is None:
        sys.exit(f"{doc['uid']}: heading {live_heading!r} ends with an unrecognized "
                 f"version segment. Add it to VERSION_QUALIFIERS in cli_url_map.py.")
    if cleaned != live_heading:
        changes.append(("heading", live_heading, cleaned))
        section["heading"] = cleaned

    before = section.get("content") or ""
    rewrite_cli_links.rewrite_entry(entry, docs, lookup, doc["bucket"], migrated)
    after = section.get("content") or ""
    if after != before:
        moved = rewrite_cli_links.diff_links(before, after, lookup)
        changes.append(("links", f"{len(moved)} CLI link(s)", moved[:3]))

    return changes


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    docs = url_map.load_map()
    lookup = rewrite_cli_links.build_lookup(docs)

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")

    release_uid, existing_items = None, None
    if confirm:
        release_uid = cli_release.ensure_release(headers, cli_release.RELEASE_DOCS)
        existing_items = cli_release.index_items(headers, release_uid)
        print(f"docs release {release_uid} currently holds "
              f"{len(existing_items)} item(s)\n")

    changed, unchanged, drift, added = 0, 0, [], 0
    for doc in sorted(docs, key=lambda d: (d["slug"], d["bucket"])):
        entry = get_entry(headers, DOCS_ARTICLE, doc["uid"])
        live_version = entry["_version"]
        snapshot = local_content(doc)
        live_before = article_section(entry).get("content") or ""

        changes = plan_entry(entry, doc, docs, lookup)
        after = article_section(entry).get("content") or ""
        if snapshot is not None and snapshot != after:
            drift.append(f"{doc['bucket']}/{doc['new_slug']}")

        if not changes:
            unchanged += 1
            print(f"{doc['bucket']:5} {doc['new_slug']}: already current at "
                  f"v{live_version}, nothing to push")
        else:
            changed += 1
            print(f"{doc['bucket']:5} {doc['new_slug']}  (live v{live_version})")
            for field, before, value in changes:
                if field == "links":
                    print(f"   links     {before}")
                    for old, new in value:
                        print(f"             {old} -> {new}")
                else:
                    print(f"   {field:9} {before!r}")
                    print(f"   {' ' * 9} -> {value!r}")

        if not confirm:
            continue

        version = live_version
        if changes:
            updated = put_entry(headers, DOCS_ARTICLE, doc["uid"], entry)
            version = updated["_version"]
            publish_entry(headers, DOCS_ARTICLE, doc["uid"], version)
            print(f"   updated -> v{version}, published to staging + development")

        outcome = cli_release.add_item(headers, release_uid, DOCS_ARTICLE,
                                       doc["uid"], version, LOCALE, existing_items)
        if outcome != "present":
            added += 1
        print(f"   release item {outcome} (v{version})")
        time.sleep(0.25)

    print(f"\n{changed} entry(ies) to update, {unchanged} already current.")
    if drift:
        print(f"\nLive content differs from the local docs/json snapshot for "
              f"{len(drift)} doc(s). The live value was pushed, so nothing is lost, "
              f"but docs/json is behind. Re-run fetch_cli_docs.py to resync:")
        for name in drift:
            print(f"  {name}")

    if confirm:
        print(f"\n{added} item(s) added to release {release_uid}. "
              f"Next: python3 scripts/create_cli_redirects.py")
    else:
        print("\nDry run complete, no writes made.")


if __name__ == "__main__":
    main()
