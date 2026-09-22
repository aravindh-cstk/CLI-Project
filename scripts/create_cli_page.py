#!/usr/bin/env python3
"""Create a new CLI docs_article from a local draft, and publish it to staging.

Generalizes create_asset_scanning_page.py, which hardcoded one page, one draft
path and one URL. The parts worth keeping are kept verbatim:

  * the CMA-assigned fields are stripped, so the POST carries no stale uid or
    version
  * article_section._metadata is popped, so Contentstack assigns the modular
    block uid rather than reusing a hand-written one
  * every /docs/headless-cms/ link is checked against cli_url_map, and an
    unmapped link aborts the run. Creating a page whose links 404 just trades one
    broken link for several
  * an entry already at that URL is reported rather than duplicated

Publishing goes to staging and development only. Production needs a Release and
approver sign-off, so it is never done here.

Usage:
  python3 scripts/create_cli_page.py <draft.json>
  python3 scripts/create_cli_page.py <draft.json> --confirm
  python3 scripts/create_cli_page.py <draft.json> --confirm --no-publish
"""

import argparse
import json
import os
import re
import sys

import cli_url_map as url_map
from cli_docs_common import (DOCS_ARTICLE, LOCALE, PUBLISH_ENV_UIDS, ROOT, load_env,
                             publish_entry, request)

HREF = re.compile(r'href="([^"]+)"')


def known_urls():
    """Every CLI doc URL the map knows, in both the old and new schemes."""
    known = set()
    for doc in url_map.load_map():
        known.add(doc["new_url"])
        known.add(doc["old_url"])
    return known


def check_links(html, known, own_url):
    """Return the internal links that point at no known CLI doc."""
    missing = []
    for href in HREF.findall(html):
        if not href.startswith("/docs/headless-cms/"):
            continue
        path = href.partition("#")[0][len("/docs"):]
        if path in known or path == own_url:
            continue
        missing.append(href)
    return missing


def article_section(entry):
    for block in entry.get("article_content") or []:
        if "article_section" in block:
            return block["article_section"] or {}
    return {}


def find_existing(headers, url):
    data = request("GET", f"/v3/content_types/{DOCS_ARTICLE}/entries", headers,
                   params={"query": json.dumps({"url": url}), "locale": LOCALE})
    return (data.get("entries") or [None])[0]


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("draft", help="the draft entry JSON to create")
    parser.add_argument("--confirm", action="store_true", help="perform the create")
    parser.add_argument("--no-publish", action="store_true",
                        help="create the entry but leave it unpublished")
    args = parser.parse_args(argv)

    path = args.draft if os.path.isabs(args.draft) else os.path.join(ROOT, args.draft)
    if not os.path.exists(path):
        sys.exit(f"{args.draft} not found")
    with open(path, encoding="utf-8") as fh:
        entry = json.load(fh)

    url = entry.get("url")
    section = article_section(entry)
    if not url or not section.get("content"):
        sys.exit(f"{args.draft} has no url or no article_section content. "
                 f"Build it with markdown_to_docs_html.py --new.")

    headers = load_env()
    print("LIVE RUN\n" if args.confirm else "DRY RUN (pass --confirm to create)\n")

    print(f"url        {url}")
    print(f"title      {entry.get('title')}")
    print(f"seo.title  {(entry.get('seo') or {}).get('title')}")
    print(f"heading    {section.get('heading')}")
    print(f"content    {len(section['content'])} chars")
    print(f"breadcrumb {[b.get('uid') for b in entry.get('breadcrumb') or []]}")

    if "uid" in entry or "_version" in entry:
        sys.exit("the draft still carries uid or _version. "
                 "Rebuild it with markdown_to_docs_html.py --new.")
    if "_metadata" in section:
        sys.exit("article_section still carries _metadata. Contentstack must assign "
                 "the modular block uid. Rebuild the draft.")

    missing = check_links(section["content"], known_urls(), url)
    if missing:
        print(f"\nUNMAPPED links, these would 404 ({len(missing)}):")
        for href in missing:
            print(f"    {href}")
        sys.exit("refusing to create the page with unmapped links")
    print("\nall internal links resolve to known CLI docs")

    existing = find_existing(headers, url)
    if existing:
        print(f"\nAn entry already serves {url}: {existing['uid']} "
              f"v{existing['_version']}. Nothing to create.")
        return 0

    if not args.confirm:
        print("\nDry run complete, no writes made.")
        return 0

    created = request("POST", f"/v3/content_types/{DOCS_ARTICLE}/entries", headers,
                      body={"entry": entry}, params={"locale": LOCALE})["entry"]
    print(f"\ncreated {created['uid']} v{created['_version']} at {created.get('url')}")

    if args.no_publish:
        print("Left unpublished, as asked.")
    else:
        publish_entry(headers, DOCS_ARTICLE, created["uid"], created["_version"],
                      PUBLISH_ENV_UIDS)
        print("published to staging and development")

    print(f"\nNext:\n"
          f"  add {created['uid']} to the left nav:\n"
          f"    python3 scripts/add_page_to_nav.py --page {created['uid']} "
          f"--section <section uid> --url {url} --env staging\n"
          f"  then add the page and the nav entry to the release.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
