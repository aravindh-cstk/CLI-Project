#!/usr/bin/env python3
"""Put the V2 asset-scanning content back on staging and development.

Recovery script for one specific mistake: release
"CLI V2 asset scanning removal 2026-08-26 [docs]" is meant to deploy to production
only. If it is deployed to all three environments, staging and development lose
the V2 asset-scanning content, and the point of keeping it there was that shipping
V2 asset scanning later would be a publish rather than a rewrite.

This republishes the last version that still carries the content to staging and
development, leaving production on the stripped version. Publishing an older
version does not touch the draft, so the stripped content stays queued as the
newest version.

Not needed if the release was deployed to production only. Run
scripts/verify_asset_scanning_live.py first to see which happened.

Usage:
  python3 scripts/republish_v2_staging.py            # dry run
  python3 scripts/republish_v2_staging.py --confirm  # publish to staging and development
"""

import sys
import time

from cli_docs_common import (DEVELOPMENT_ENV_UID, DOCS_ARTICLE, LOCALE, PROD_ENV_UID,
                             PUBLISH_ENV_UIDS, STAGING_ENV_UID, article_section,
                             get_entry, load_env, publish_entry)

# (label, uid, the version that still carries the asset-scanning content)
TARGETS = [
    ("Bulk Operations in CLI | V2.x.x", "blt85d9deae08de968d", 13),
    ("Import Content Using the CLI | V2.x.x", "blt1215a1f9bbcc9900", 19),
]

MARKERS = ["scan status", "asset scanning", "still scanning", "quarantin"]

ENV_NAMES = {PROD_ENV_UID: "production", STAGING_ENV_UID: "staging",
             DEVELOPMENT_ENV_UID: "development"}


def records(entry):
    return {r["environment"]: r["version"] for r in (entry.get("publish_details") or [])
            if r.get("locale") == LOCALE}


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    print("LIVE RUN\n" if confirm else "DRY RUN (pass --confirm to publish)\n")

    planned = []
    for label, uid, target in TARGETS:
        draft = get_entry(headers, DOCS_ARTICLE, uid)
        live = records(draft)

        want = get_entry(headers, DOCS_ARTICLE, uid, version=target)
        html = (article_section(want).get("content") or "").lower()
        present = [m for m in MARKERS if m in html]
        if not present:
            sys.exit(f"{label}: v{target} carries no asset-scanning content "
                     f"({MARKERS} all absent). It is not the version to restore.")

        if want.get("url") != draft.get("url"):
            sys.exit(f"{label}: v{target} url {want.get('url')!r} differs from the "
                     f"current url {draft.get('url')!r}. Publishing it would change a "
                     f"live URL. Refusing.")

        need = [e for e in PUBLISH_ENV_UIDS if live.get(e) != target]
        print(f"{label}  ({uid})")
        for env, version in sorted(live.items(), key=lambda kv: ENV_NAMES.get(kv[0], "")):
            print(f"  {ENV_NAMES.get(env, env):<12} v{version}")
        if not need:
            print(f"  staging and development are already on v{target}, nothing to do\n")
            continue
        print(f"  would publish v{target} to "
              f"{', '.join(ENV_NAMES.get(e, e) for e in need)}")
        print(f"  production stays on v{live.get(PROD_ENV_UID)}, draft untouched "
              f"at v{draft['_version']}\n")
        planned.append((label, uid, target, need))

    if not confirm:
        print(f"Dry run complete, no writes made. {len(planned)} entry(s) would change.")
        return 0

    for label, uid, target, need in planned:
        publish_entry(headers, DOCS_ARTICLE, uid, target, env_uids=need)
        print(f"published {label} v{target} to "
              f"{', '.join(ENV_NAMES.get(e, e) for e in need)}")
        time.sleep(0.3)

    print(f"\nDone. {len(planned)} entry(s) published.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
