#!/usr/bin/env python3
"""Create the "Asset Scanning in CLI" docs_article from the local GA draft.

Asset scanning is live for CLI V1 (GA). Four GA docs already link to
/docs/headless-cms/asset-scanning-in-cli, and every one of those links 404s
because the page was only ever drafted locally.

The draft was authored against the post-restructure world: /v1 URLs, cli- slug
prefixes, "| V1.x.x" titles. None of that is live yet, so creating the page that
way would trade five 404s for eight new ones. This script converts the draft back
to the conventions production actually uses today:

  * url        the bare /headless-cms/asset-scanning-in-cli, which is what the
               four GA docs already point at, so no existing entry needs a PUT
  * title      no version qualifier, matching every other live GA doc
  * links      rewritten from the new scheme to the old via cli_url_map

The pending URL restructure moves this page to /v1 along with everything else,
once its slug is registered in cli_url_map.

Creation only. The production publish goes through a Release, because a Publish
Rule requires approver sign-off for the production environment.

Usage:
  python3 scripts/create_asset_scanning_page.py            # dry run
  python3 scripts/create_asset_scanning_page.py --confirm  # create the entry
"""

import json
import os
import re
import sys

import cli_url_map as url_map
from cli_docs_common import DOCS_ARTICLE, LOCALE, ROOT, load_env, request

DRAFT = os.path.join(ROOT, "docs", "json", "GA", "asset-scanning-in-cli.json")

URL = "/headless-cms/asset-scanning-in-cli"
TITLE = "[Contentstack Command-line Interface (CLI)] - Asset Scanning in CLI"
SEO_TITLE = "Asset Scanning in CLI | Contentstack"

# Fields the CMA assigns. The draft carries "<TO BE ASSIGNED>" placeholders.
DROP = ("uid", "_version", "ACL", "created_at", "created_by", "updated_at",
        "updated_by", "publish_details", "_in_progress")

HREF = re.compile(r'href="([^"]+)"')


def new_to_old():
    """new_url -> old_url for every CLI doc, so draft links can be de-restructured."""
    table = {}
    for doc in url_map.load_map():
        table[doc["new_url"]] = doc["old_url"]
    return table


def rewrite_links(html, table):
    """Point the draft's links at the URLs production serves today."""
    changed, missing = [], []

    def swap(match):
        href = match.group(1)
        if not href.startswith("/docs/headless-cms/"):
            return match.group(0)
        path, _, anchor = href.partition("#")
        key = path[len("/docs"):]
        if key not in table:
            missing.append(href)
            return match.group(0)
        new = "/docs" + table[key] + (f"#{anchor}" if anchor else "")
        if new != href:
            changed.append((href, new))
        return f'href="{new}"'

    return HREF.sub(swap, html), changed, missing


def build_entry():
    with open(DRAFT, encoding="utf-8") as fh:
        draft = json.load(fh)

    entry = {k: v for k, v in draft.items() if k not in DROP}
    entry["url"] = URL
    entry["title"] = TITLE
    entry["seo"] = dict(entry.get("seo") or {})
    entry["seo"]["title"] = SEO_TITLE

    section = entry["article_content"][0]["article_section"]
    # Let Contentstack assign the modular block uid rather than reusing the
    # hand-written placeholder from the draft.
    section.pop("_metadata", None)
    section["content"], changed, missing = rewrite_links(section["content"], new_to_old())

    return entry, changed, missing


def find_existing(headers):
    data = request("GET", f"/v3/content_types/{DOCS_ARTICLE}/entries", headers,
                   params={"query": json.dumps({"url": URL}), "locale": LOCALE})
    return (data.get("entries") or [None])[0]


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    print("LIVE RUN\n" if confirm else "DRY RUN (pass --confirm to create)\n")

    entry, changed, missing = build_entry()

    print(f"url        {entry['url']}")
    print(f"title      {entry['title']}")
    print(f"seo.title  {entry['seo']['title']}")
    print(f"heading    {entry['article_content'][0]['article_section']['heading']}")
    print(f"content    {len(entry['article_content'][0]['article_section']['content'])} chars")

    print(f"\nlinks rewritten to the live URL scheme ({len(changed)}):")
    for old, new in changed:
        print(f"    {old}\n      -> {new}")
    if missing:
        print(f"\nUNMAPPED links, these would 404 ({len(missing)}):")
        for href in missing:
            print(f"    {href}")
        sys.exit("refusing to create the page with unmapped links")

    existing = find_existing(headers)
    if existing:
        print(f"\nEntry already exists at {URL}: {existing['uid']} v{existing['_version']}")
        print("Nothing to create.")
        return 0

    if not confirm:
        print("\nDry run complete, no writes made.")
        return 0

    created = request("POST", f"/v3/content_types/{DOCS_ARTICLE}/entries", headers,
                      body={"entry": entry}, params={"locale": LOCALE})["entry"]
    print(f"\ncreated {created['uid']} v{created['_version']} at {created.get('url')}")
    print("Not published. Add it to the release and deploy that to production.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
