#!/usr/bin/env python3
"""Push the article_section.content of docs/json/GA/create-custom-cli-plugins.json
to the live Contentstack entry blt64294e11f81fe300.

That UID is not the one tracked locally for this doc (the local JSON's own "uid"
field is blt4f27fd89adf6b6c1, and cli-url-map.csv / docs/json/index.json don't
list blt64294e11f81fe300 at all). It was confirmed directly by the requester as
the correct live entry to update, so this script fetches it fresh, prints its
current heading/title/url for a manual sanity check, and refuses to proceed
past that point without --confirm.

Usage:
  python3 scripts/push_creating-custom-plugins.py            # dry run, no writes
  python3 scripts/push_creating-custom-plugins.py --confirm   # write + publish
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli_docs_common import load_env, get_entry, put_entry, publish_entry, article_section
from heading_cleanup import strip_heading_suffix

CONTENT_TYPE = "docs_article"
UID = "blt64294e11f81fe300"
LOCAL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docs", "json", "GA", "create-custom-cli-plugins.json",
)


def main():
    import json

    confirm = "--confirm" in sys.argv
    headers = load_env()

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")

    fresh = get_entry(headers, CONTENT_TYPE, UID)
    live_section = article_section(fresh)
    print("Live entry before any change:")
    print(f"  uid:     {fresh.get('uid')}")
    print(f"  title:   {fresh.get('title')}")
    print(f"  url:     {fresh.get('url')}")
    print(f"  heading: {live_section.get('heading')}")
    print(f"  version: {fresh.get('_version')}")
    print()
    print("Confirm this is really the 'Creating Custom CLI Plugins' article before "
          "proceeding. This UID is not tracked in cli-url-map.csv or docs/json/index.json, "
          "so nothing here has been cross-checked automatically.\n")

    with open(LOCAL_PATH, encoding="utf-8") as fh:
        local_entry = json.load(fh)
    local_section = article_section(local_entry)
    new_content = local_section["content"]

    live_heading = live_section["heading"]
    new_heading = strip_heading_suffix(local_section["heading"]) or local_section["heading"]

    if live_section["content"] == new_content and live_heading == new_heading:
        print("No change from current live content/heading, nothing to do.")
        return

    print(f"Will update live v{fresh['_version']}"
          f"{' and publish to staging+development' if confirm else ''}")
    if live_heading != new_heading:
        print(f"  heading '{live_heading}' -> '{new_heading}'")
    print(f"  content: {len(live_section['content'])} chars -> {len(new_content)} chars")

    if not confirm:
        print("\nDry run complete, no writes made.")
        return

    live_section["content"] = new_content
    live_section["heading"] = new_heading
    updated = put_entry(headers, CONTENT_TYPE, UID, fresh)
    new_version = updated["_version"]
    print(f"  updated -> v{new_version}")

    publish_entry(headers, CONTENT_TYPE, UID, new_version)
    print(f"  published v{new_version} to staging + development")
    print("\nDone.")


if __name__ == "__main__":
    main()
