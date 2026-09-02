#!/usr/bin/env python3
"""Stage the asset-scanning production changes into a Contentstack Release.

A Publish Rule (blte4575c7c38862a50) requires approver sign-off for the
production environment, so a management token cannot publish there directly. The
CMA returns 422. Releases are the sanctioned path: stage the exact versions here,
then an approver deploys the release to production from the Contentstack UI.

Items, all pinned to an explicit version:

  blt6ee109a7b3725e1c  v1   Asset Scanning in CLI, the new GA page
  blt85d9deae08de968d  v7   Beta bulk-operations-in-cli, last scan-free version
  blt1215a1f9bbcc9900  v14  Beta import-content-using-the-cli, last scan-free version

Every one of these carries the URL scheme production serves today, so deploying
this release does not disturb the un-deployed URL restructure sitting in the
drafts.

Usage:
  python3 scripts/stage_asset_scanning_release.py            # dry run
  python3 scripts/stage_asset_scanning_release.py --confirm  # create and fill
"""

import sys

import cli_release
from cli_docs_common import DOCS_ARTICLE, LOCALE, PROD_ENV_UID, get_entry, load_env

ITEMS = [
    ("Asset Scanning in CLI (new GA page)", "blt6ee109a7b3725e1c", 1),
    ("Beta bulk-operations-in-cli (scan-free)", "blt85d9deae08de968d", 7),
    ("Beta import-content-using-the-cli (scan-free)", "blt1215a1f9bbcc9900", 14),
]


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    print("LIVE RUN\n" if confirm else "DRY RUN (pass --confirm to write)\n")

    print(f"Release: {cli_release.RELEASE_ASSET_SCANNING}\n")
    for label, uid, version in ITEMS:
        entry = get_entry(headers, DOCS_ARTICLE, uid, version=version)
        current = next((r["version"] for r in entry.get("publish_details") or []
                        if r.get("environment") == PROD_ENV_UID
                        and r.get("locale") == LOCALE), None)
        print(f"  {label}")
        print(f"    {uid}  v{version}  ->  {entry.get('url')}")
        print(f"    production today: "
              f"{'not published' if current is None else 'v' + str(current)}")

    if not confirm:
        print("\nDry run complete, no writes made.")
        return 0

    release_uid = cli_release.ensure_release(headers,
                                             cli_release.RELEASE_ASSET_SCANNING)
    existing = cli_release.index_items(headers, release_uid)
    for label, uid, version in ITEMS:
        outcome = cli_release.add_item(headers, release_uid, DOCS_ARTICLE, uid,
                                       version, LOCALE, existing)
        print(f"  {outcome:<8} {uid} v{version}  {label}")

    print(f"\nRelease {release_uid} is ready. "
          f"An approver deploys it to production from the Contentstack UI.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
