#!/usr/bin/env python3
"""Bundle every entry that staging is ahead on into one release for production.

Targets are computed by comparing each entry's staging version against its
production version, not read from a file. The first version of this script read
notes/reports/pushed-entries.json, which push_all_wave_changes.py overwrites on
every run, so a second push left the script able to see only the last 7 entries
of 74. It happened to work because add_item is idempotent and the earlier items
were already in the release, but rebuilding the release from scratch would have
produced a silently incomplete one. That is the same class of bug as
RELEASE_CLEANUP_NAV, and it is the bug this file most needs to avoid.

"staging is ahead of production" is the definition that matters, because that is
exactly the set of changes a production deploy has to carry.

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

from cli_docs_common import (DOCS_ARTICLE, LOCALE, PROD_ENV_UID, ROOT,
                             STAGING_ENV_UID, get_entry, load_env, request)
from cli_release import RELEASE_FULL_RESTRUCTURE, add_item, ensure_release, index_items

CHANGELOG_TYPE = "changelog_details"
CHANGELOG_UID = "blt48436d263389bb65"
RETIRED = {"blt18f5edee45f9d6c2"}   # Create Custom CLI Commands, unpublished separately


def live_version(headers, content_type, uid):
    return request("GET", f"/v3/content_types/{content_type}/entries/{uid}",
                   headers, params={"locale": LOCALE})["entry"]["_version"]


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to write\n")

    index = json.load(open(os.path.join(ROOT, "docs", "json", "index.json"),
                          encoding="utf-8"))
    seen, items, drift = set(), [], []
    for row in index["entries"]:
        uid = row["uid"]
        if uid in seen or uid in RETIRED:
            continue
        seen.add(uid)
        entry = get_entry(headers, DOCS_ARTICLE, uid)
        published = {r["environment"]: r["version"]
                     for r in (entry.get("publish_details") or [])
                     if r.get("locale") == LOCALE}
        staging = published.get(STAGING_ENV_UID)
        production = published.get(PROD_ENV_UID)
        if staging is None or staging == production:
            continue
        if staging != entry["_version"]:
            drift.append((uid, staging, entry["_version"], row["json"]))
        items.append((DOCS_ARTICLE, uid, staging, row["json"]))
    cl_version = live_version(headers, CHANGELOG_TYPE, CHANGELOG_UID)
    items.append((CHANGELOG_TYPE, CHANGELOG_UID, cl_version, "changelog 2.0.0"))
    print(f"{len(items) - 1} entries where staging is ahead of production, "
          f"plus the changelog\n")

    if drift:
        print("staging is behind the latest saved version on these, so the release "
              "carries what staging serves rather than an unpublished draft:")
        for uid, staged, latest, path in drift:
            print(f"  {uid}  staging v{staged}, latest v{latest}  "
                  f"{path.split('/')[-1][:40]}")
        print()

    print(f"release: {RELEASE_FULL_RESTRUCTURE!r}")
    print(f"items:   {len(items)}  ({len(items) - 1} docs + 1 changelog "
          f"at v{cl_version})")

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
