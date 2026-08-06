#!/usr/bin/env python3
"""Take the V2 (Beta) asset-scanning documentation off production.

Asset scanning is live for CLI V1 (GA) but not for V2 (Beta), and the V2 content
reached production in the 2026-08-03 publish. This republishes the last scan-free
version of each Beta entry to production.

A version rollback rather than a scan-stripping PUT, deliberately:

  * The 2026-08-05 URL restructure sits un-deployed in each entry's draft and is
    published to staging and development only. A PUT would stack on top of that
    draft, and publishing the result to production would ship the restructure
    early, changing live URLs while the redirect release is still un-deployed.
  * Publishing an older version leaves the draft untouched, so the restructure
    stays queued exactly as it is.
  * The target versions carry the same URL production already serves, so nothing
    about the live URL changes.

Verified before writing this: the delta between each target version and the
version production serves is asset-scanning content only.

Staging and development keep the V2 content, so shipping it later is a publish
rather than a rewrite.

Usage:
  python3 scripts/rollback_beta_asset_scanning.py            # dry run
  python3 scripts/rollback_beta_asset_scanning.py --confirm  # publish to production
"""

import sys
import time

from cli_docs_common import (DOCS_ARTICLE, LOCALE, PROD_ENV_UID, article_section,
                             get_entry, load_env, publish_entry)

# (label, uid, target version) - the newest version with no asset-scanning content.
TARGETS = [
    ("Beta bulk-operations-in-cli", "blt85d9deae08de968d", 7),
    ("Beta import-content-using-the-cli", "blt1215a1f9bbcc9900", 14),
]

# Markers specific to the asset-scanning change. --backup-dir and
# --skip-assets-publish are deliberately absent: both predate asset scanning on the
# Beta import page, so they would flag a clean version.
MARKERS = ["scan status", "asset scanning", "still scanning", "quarantin",
           "asset-scanning-in-cli"]


def prod_record(entry):
    for record in entry.get("publish_details") or []:
        if record.get("environment") == PROD_ENV_UID and record.get("locale") == LOCALE:
            return record
    return None


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    print("LIVE RUN\n" if confirm else "DRY RUN (pass --confirm to publish)\n")

    planned = []
    for label, uid, target in TARGETS:
        draft = get_entry(headers, DOCS_ARTICLE, uid)
        record = prod_record(draft)
        if not record:
            sys.exit(f"{label}: not published to production, nothing to roll back")
        current = record["version"]

        want = get_entry(headers, DOCS_ARTICLE, uid, version=target)
        live = get_entry(headers, DOCS_ARTICLE, uid, version=current)

        want_html = (article_section(want).get("content") or "").lower()
        found = [m for m in MARKERS if m in want_html]
        if found:
            sys.exit(f"{label}: v{target} still contains {found}, refusing to publish it")

        if want.get("url") != live.get("url"):
            sys.exit(f"{label}: v{target} url {want.get('url')!r} differs from the live "
                     f"v{current} url {live.get('url')!r}, refusing to change a live URL")

        if current == target:
            print(f"{label}: production is already on v{target}, skipping")
            continue

        print(f"{label}  ({uid})")
        print(f"  production  v{current} -> v{target}")
        print(f"  url         {want.get('url')}  (unchanged)")
        print(f"  draft stays at v{draft['_version']}, restructure untouched")
        planned.append((label, uid, target))

    if not confirm:
        print(f"\nDry run complete, no writes made. {len(planned)} entry(s) would change.")
        return 0

    for label, uid, target in planned:
        publish_entry(headers, DOCS_ARTICLE, uid, target, env_uids=[PROD_ENV_UID])
        print(f"published {label} v{target} to production")
        time.sleep(0.3)

    print(f"\nDone. {len(planned)} entry(s) published.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
