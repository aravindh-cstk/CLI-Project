#!/usr/bin/env python3
"""Phase 4: create the server_redirects that cover every CLI URL that stops resolving.

60 entries, derived from cli-url-map.csv:

  /docs/headless-cms/{slug}                 -> new /v1, or the new bare URL when
                                               the slug changed and a V2 doc exists
  /docs/headless-cms/{slug}/beta            -> new bare URL
  /docs/headless-cms/{slug}/old-commands    -> new /v0

Deliberately absent: the 13 topics whose V1 URL is byte-identical to their new V2
URL. server_redirects override published pages on this site, verified with curl, so
a redirect there would make the new GA doc unreachable. The guard below refuses to
write any redirect whose source is a URL that will serve a live page.

Run after push_cli_url_changes.py. Redirect targets have to exist first.

Usage:
  python3 scripts/create_cli_redirects.py            # dry run
  python3 scripts/create_cli_redirects.py --confirm  # create/update, publish, release
"""

import sys
import time

import cli_release
import cli_url_map as url_map
from cli_docs_common import (LOCALE, SERVER_REDIRECTS, list_entries, load_env,
                             publish_entry, put_entry, request)


def normalise(path):
    return (path or "").split("#")[0].split("?")[0].rstrip("/")


def existing_by_from(headers):
    """normalised from -> [entry], across the whole redirect table."""
    table = {}
    # _version is needed by the already-correct branch, which adds the live version
    # to the release without going through a PUT first.
    entries = list_entries(headers, SERVER_REDIRECTS,
                           only=("uid", "title", "from", "to", "is_permanent",
                                 "_version"))
    for entry in entries:
        table.setdefault(normalise(entry.get("from")), []).append(entry)
    return table, len(entries)


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    docs = url_map.load_map()
    pairs = url_map.redirects(docs)

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")

    # Guard: a redirect source must never be a URL that will serve a live page.
    live_pages = {f"/docs{doc['new_url']}" for doc in docs}
    shadowing = sorted({src for src, _ in pairs if normalise(src) in
                        {normalise(p) for p in live_pages}})
    if shadowing:
        sys.exit("FATAL: these redirect sources would shadow a live page, which on "
                 f"this site wins over the page itself: {shadowing}")

    targets = {normalise(dst) for _, dst in pairs}
    missing = sorted(targets - {normalise(p) for p in live_pages})
    if missing:
        sys.exit(f"FATAL: redirect target(s) match no CLI doc URL: {missing}")

    print(f"{len(pairs)} redirect(s) to ensure, "
          f"{len(docs) - len(pairs)} CLI doc(s) deliberately without one.\n")

    table, total = existing_by_from(headers)
    print(f"redirect table currently holds {total} entries\n")

    release_uid, release_items = None, None
    if confirm:
        release_uid = cli_release.ensure_release(headers, cli_release.RELEASE_REDIRECTS)
        release_items = cli_release.index_items(headers, release_uid)

    created, updated, unchanged = 0, 0, 0
    for source, target in pairs:
        matches = table.get(normalise(source), [])
        if len(matches) > 1:
            print(f"  NOTE {source}: {len(matches)} existing entries share this from, "
                  f"updating all of them")

        if not matches:
            created += 1
            print(f"CREATE {source}\n    -> {target}")
            if confirm:
                body = {"entry": {"title": source, "from": source, "to": target,
                                  "is_permanent": True, "taxonomies": []}}
                entry = request("POST", f"/v3/content_types/{SERVER_REDIRECTS}/entries",
                                headers, body=body, params={"locale": LOCALE})["entry"]
                publish_entry(headers, SERVER_REDIRECTS, entry["uid"], entry["_version"])
                cli_release.add_item(headers, release_uid, SERVER_REDIRECTS,
                                     entry["uid"], entry["_version"], LOCALE,
                                     release_items)
                print(f"    created {entry['uid']} v{entry['_version']}, published, "
                      f"added to release")
                time.sleep(0.2)
            continue

        for entry in matches:
            needs = (entry.get("to") != target or entry.get("is_permanent") is not True)
            if not needs:
                unchanged += 1
                print(f"OK     {source} already points at {target}")
                if confirm:
                    cli_release.add_item(headers, release_uid, SERVER_REDIRECTS,
                                         entry["uid"], entry["_version"], LOCALE,
                                         release_items)
                continue
            updated += 1
            print(f"UPDATE {source}\n    {entry.get('to')!r} -> {target!r}"
                  f"  (is_permanent {entry.get('is_permanent')} -> True)")
            if confirm:
                entry["to"] = target
                entry["is_permanent"] = True
                fresh = put_entry(headers, SERVER_REDIRECTS, entry["uid"], entry)
                publish_entry(headers, SERVER_REDIRECTS, entry["uid"], fresh["_version"])
                cli_release.add_item(headers, release_uid, SERVER_REDIRECTS,
                                     entry["uid"], fresh["_version"], LOCALE,
                                     release_items)
                print(f"    updated {entry['uid']} -> v{fresh['_version']}, published, "
                      f"added to release")
                time.sleep(0.2)

    print(f"\n{created} to create, {updated} to update, {unchanged} already correct.")
    if confirm:
        print(f"\nRelease {release_uid}. Next: python3 scripts/"
              f"retarget_legacy_cli_redirects.py")
    else:
        print("\nDry run complete, no writes made.")


if __name__ == "__main__":
    main()
