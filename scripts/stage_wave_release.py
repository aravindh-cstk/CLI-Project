#!/usr/bin/env python3
"""Bundle every pushed entry into one release for production.

Reads notes/reports/pushed-entries.json, written by
scripts/push_all_wave_changes.py, and adds each entry to a single release
together with the corrected 2.0.0 changelog entry.

One release, deployed as a unit. Waves A to E touch the same pages repeatedly,
so deploying a subset would put pages live in a state no wave intended.

Item versions are re-read from the CMS rather than taken from the file. That is
not defensive padding: RELEASE_CLEANUP_NAV carried blt0d2ab10c0fa412a8 at v3 and
deployed, but the content edit had never been made, so it published v3 unchanged
and the legacy redirect kept 404ing. A release is only as good as the versions
in it.

This script does not deploy. Production is approval gated and is the docs
owner's call, made in the Contentstack UI. The handover is a release uid.

Usage:
  python3 scripts/stage_wave_release.py            # dry run
  python3 scripts/stage_wave_release.py --confirm  # create the release and add items
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli_docs_common import DOCS_ARTICLE, LOCALE, ROOT, get_entry, load_env, request
from cli_release import RELEASE_FULL_RESTRUCTURE, add_item, ensure_release, index_items

PUSHED = os.path.join(ROOT, "notes", "reports", "pushed-entries.json")
CHANGELOG_TYPE = "changelog_details"
CHANGELOG_UID = "blt48436d263389bb65"


def live_version(headers, content_type, uid):
    return request("GET", f"/v3/content_types/{content_type}/entries/{uid}",
                   headers, params={"locale": LOCALE})["entry"]["_version"]


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to write\n")

    if not os.path.exists(PUSHED):
        sys.exit(f"{os.path.relpath(PUSHED, ROOT)} not found. Run "
                 f"scripts/push_all_wave_changes.py --confirm first.")
    pushed = json.load(open(PUSHED, encoding="utf-8"))
    print(f"{len(pushed)} docs_article entries from the push, plus the changelog\n")

    items, drift = [], []
    for row in pushed:
        current = live_version(headers, DOCS_ARTICLE, row["uid"])
        if current != row["version"]:
            drift.append((row["uid"], row["version"], current, row["path"]))
        items.append((DOCS_ARTICLE, row["uid"], current, row["path"]))
    cl_version = live_version(headers, CHANGELOG_TYPE, CHANGELOG_UID)
    items.append((CHANGELOG_TYPE, CHANGELOG_UID, cl_version, "changelog 2.0.0"))

    if drift:
        print("versions moved since the push, using the current one:")
        for uid, was, now, path in drift:
            print(f"  {uid}  pushed v{was}, CMS now v{now}  {path.split('/')[-1][:40]}")
        print()

    print(f"release: {RELEASE_FULL_RESTRUCTURE!r}")
    print(f"items:   {len(items)}  ({len(pushed)} docs + 1 changelog at v{cl_version})")

    if not confirm:
        print("\nDry run complete. Nothing written.")
        return 0

    release_uid = ensure_release(headers, RELEASE_FULL_RESTRUCTURE)
    existing = index_items(headers, release_uid)
    counts = {"added": 0, "updated": 0, "present": 0}
    for content_type, uid, version, _path in items:
        outcome = add_item(headers, release_uid, content_type, uid, version,
                           existing=existing)
        counts[outcome] += 1

    print(f"\nrelease {release_uid}")
    print(f"  added {counts['added']}, updated {counts['updated']}, "
          f"already present {counts['present']}")
    print(f"  total items now {len(index_items(headers, release_uid))}")
    print("\nProduction is unchanged. Deploying this release is the docs owner's "
          "call, in the Contentstack UI, because production publishing is approval "
          "gated. Nothing here can or does deploy it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
