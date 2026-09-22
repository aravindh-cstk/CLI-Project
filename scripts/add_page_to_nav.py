#!/usr/bin/env python3
"""Append a docs_article to a left-navigation section.

Generalizes add_asset_scanning_to_nav.py, which hardcoded one page, one section
and a production-published guard. A staging-first flow never satisfies that guard,
because the page is on staging and development and deliberately not yet on
production, so the environment the guard checks is a parameter here.

Every other guard is kept:
  * the page must exist and, when --url is given, serve the URL you expect
  * the page must be published to the environment you name, so the sidebar never
    gets a dead link
  * the whole CLI nav tree is walked first, so a page already in the nav is a
    no-op rather than a duplicate leaf
  * the leaf is appended, not inserted alphabetically, because the existing order
    is not alphabetical and reordering the nav is not this script's job

This deliberately does not use rebuild_cli_left_nav.py, which reads e["bucket"]
from docs/json/index.json. The rebuilt index has no bucket key, so that script
raises KeyError today. A targeted append also avoids rewriting the whole tree to
add one leaf.

Usage:
  python3 scripts/add_page_to_nav.py --page <uid> --section <uid> [--env staging]
  python3 scripts/add_page_to_nav.py --page <uid> --section <uid> --confirm
  python3 scripts/add_page_to_nav.py --section <uid> --list
"""

import argparse
import sys

from cli_docs_common import (DEVELOPMENT_ENV_UID, DOCS_ARTICLE, LOCALE, PROD_ENV_UID,
                             STAGING_ENV_UID, get_entry, load_env, publish_entry,
                             put_entry, request)

NAV_TYPE = "links_2026"
CLI_ROOT = "bltd697fa2bc1e38b53"

ENVIRONMENTS = {
    "staging": STAGING_ENV_UID,
    "development": DEVELOPMENT_ENV_UID,
    "production": PROD_ENV_UID,
}


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


def published_to(entry, env_uid):
    return [r for r in (entry.get("publish_details") or [])
            if r.get("environment") == env_uid and r.get("locale") == LOCALE]


def parse_args(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--page", help="docs_article uid of the page to add")
    parser.add_argument("--section", required=True,
                        help=f"{NAV_TYPE} uid of the section to append to")
    parser.add_argument("--url", help="expected page url, checked before writing")
    parser.add_argument("--env", default="staging", choices=sorted(ENVIRONMENTS),
                        help="environment the page must already be published to")
    parser.add_argument("--list", action="store_true",
                        help="print the section's current leaves and exit")
    parser.add_argument("--confirm", action="store_true",
                        help="write and publish, instead of a dry run")
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    headers = load_env()

    if args.list:
        section = nav_entry(headers, args.section)
        print(f"section {args.section}  {section.get('title')}")
        for index, link in enumerate(section.get("nested_links") or [], 1):
            child = link["uid"]
            title = link.get("_content_type_uid")
            print(f"  {index:3}. {child}  ({title})")
        return 0

    if not args.page:
        sys.exit("--page is required unless --list is given")

    print("LIVE RUN\n" if args.confirm else "DRY RUN (pass --confirm to write)\n")
    env_uid = ENVIRONMENTS[args.env]

    page = get_entry(headers, DOCS_ARTICLE, args.page)
    if args.url and page.get("url") != args.url:
        sys.exit(f"{args.page}: url is {page.get('url')!r}, expected {args.url!r}. "
                 f"Refusing to add an unexpected page to the nav.")

    published = published_to(page, env_uid)
    if not published:
        sys.exit(f"{args.page} is not published to {args.env}. Adding it to the nav "
                 f"would put a dead link in the sidebar. Publish it first.")

    print(f"page    {args.page}  {page.get('title')}")
    print(f"        {page.get('url')}  ({args.env} v{published[0]['version']})")

    existing = leaves(headers, CLI_ROOT)
    already = [path for path, uid in existing if uid == args.page]
    if already:
        print(f"\n[unchanged] already in the nav under {already[0]}")
        return 0
    print(f"        not in the nav today ({len(existing)} leaves scanned)")

    section = nav_entry(headers, args.section)
    links = list(section.get("nested_links") or [])
    print(f"\nsection {args.section}  {section.get('title')}  v{section['_version']}  "
          f"({len(links)} leaves)")
    print(f"        appending as leaf {len(links) + 1}")

    if not args.confirm:
        print("\nDry run complete, no writes made.")
        return 0

    links.append({"uid": args.page, "_content_type_uid": DOCS_ARTICLE})
    section["nested_links"] = links
    updated = put_entry(headers, NAV_TYPE, args.section, section)
    publish_entry(headers, NAV_TYPE, args.section, updated["_version"])
    print(f"        wrote v{updated['_version']}, published to staging and development")
    print("\nNext: add this nav entry to the release alongside the page.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
