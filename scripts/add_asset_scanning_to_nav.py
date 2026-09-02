#!/usr/bin/env python3
"""Put the Asset Scanning page into the left navigation.

The page is live on production (/headless-cms/asset-scanning-in-cli/v1 returns
200) but it is not in the nav. Walking the live links_2026 tree from the CLI root
returns 92 leaves and this page is not one of them, so today it is reachable only
from cross-links inside other pages.

It goes under Version 1.x.x > CLI Advanced Operations. V1 and V2 have separate
category trees now, so this appears under Version 1.x.x only. That is what we
want: asset scanning shipped for V1 and not for V2.

Appended to the end of the section rather than inserted alphabetically, because
the existing order is not alphabetical and reordering the nav is not the job.

This deliberately does not use rebuild_cli_left_nav.py, which reads e["bucket"]
from docs/json/index.json. The rebuilt index has no bucket key, so that script
raises KeyError today. A targeted append also avoids rewriting the whole tree to
add one leaf.

Usage:
  python3 scripts/add_asset_scanning_to_nav.py            # dry run
  python3 scripts/add_asset_scanning_to_nav.py --confirm  # write + publish to staging and development
"""

import sys

from cli_docs_common import (DOCS_ARTICLE, LOCALE, PROD_ENV_UID, get_entry, load_env,
                             publish_entry, put_entry, request)

NAV_TYPE = "links_2026"
CLI_ROOT = "bltd697fa2bc1e38b53"
SECTION = "bltfc496d77b74a316b"          # Version 1.x.x > CLI Advanced Operations
PAGE = "blt6ee109a7b3725e1c"             # Asset Scanning in CLI | V1.x.x
EXPECTED_URL = "/headless-cms/asset-scanning-in-cli/v1"


def nav_entry(headers, uid):
    return request("GET", f"/v3/content_types/{NAV_TYPE}/entries/{uid}",
                   headers, params={"locale": LOCALE,
                                    "include_publish_details": "true"})["entry"]


def leaves(headers, uid, path="", seen=None):
    """Every docs_article leaf under a nav node, as (path, uid)."""
    seen = seen if seen is not None else set()
    if uid in seen:
        return []
    seen.add(uid)
    entry = nav_entry(headers, uid)
    here = f"{path}/{entry.get('title')}"
    out = []
    for link in entry.get("nested_links") or []:
        if link.get("_content_type_uid") == NAV_TYPE:
            out += leaves(headers, link["uid"], here, seen)
        else:
            out.append((here, link["uid"]))
    return out


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    print("LIVE RUN\n" if confirm else "DRY RUN (pass --confirm to write)\n")

    page = get_entry(headers, DOCS_ARTICLE, PAGE)
    if page.get("url") != EXPECTED_URL:
        sys.exit(f"{PAGE}: url is {page.get('url')!r}, expected {EXPECTED_URL!r}. "
                 f"Refusing to add an unexpected page to the nav.")
    prod = [r for r in (page.get("publish_details") or [])
            if r.get("environment") == PROD_ENV_UID and r.get("locale") == LOCALE]
    if not prod:
        sys.exit(f"{PAGE} is not published to production. Adding it to the nav would "
                 f"put a dead link in the sidebar.")
    print(f"page   {PAGE}  {page.get('title')}")
    print(f"       {page.get('url')}  (production v{prod[0]['version']})")

    existing = leaves(headers, CLI_ROOT)
    already = [path for path, uid in existing if uid == PAGE]
    if already:
        print(f"\n[unchanged] already in the nav under {already[0]}")
        return 0
    print(f"       not in the nav today ({len(existing)} leaves scanned)")

    section = nav_entry(headers, SECTION)
    links = list(section.get("nested_links") or [])
    print(f"\nsection {SECTION}  {section.get('title')}  v{section['_version']}  "
          f"({len(links)} leaves)")
    print(f"       appending as leaf {len(links) + 1}")

    if not confirm:
        print("\nDry run complete, no writes made.")
        return 0

    links.append({"uid": PAGE, "_content_type_uid": DOCS_ARTICLE})
    section["nested_links"] = links
    updated = put_entry(headers, NAV_TYPE, SECTION, section)
    publish_entry(headers, NAV_TYPE, SECTION, updated["_version"])
    print(f"       wrote v{updated['_version']}, published to staging and development")
    print("\nNext: python3 scripts/stage_cli_cleanup_releases.py --release C")
    return 0


if __name__ == "__main__":
    sys.exit(main())
