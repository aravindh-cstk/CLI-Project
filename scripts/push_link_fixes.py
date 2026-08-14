#!/usr/bin/env python3
"""Push the 404 link fixes (CS Assets URL, bulk-publish config reference) to Contentstack.

Scope is deliberately explicit (TARGETS below): four existing docs_article
entries whose article_section.content had broken links fixed locally.

For each target: fetch the entry fresh (so any field we do not know about is
preserved), splice in the content HTML from the local docs/json file, PUT the
update, then publish the resulting version to staging + development.

Usage:
  python3 scripts/push_link_fixes.py            # dry run: show what would change, no writes
  python3 scripts/push_link_fixes.py --confirm  # perform the update + publish
"""

import json
import os
import sys

from cli_docs_common import (DOCS_ARTICLE, ROOT, article_section, get_entry,
                             load_env, publish_entry, put_entry)

TARGETS = [
    ("docs/json/Version 0.x.x/Bulk Publish and Unpublish Content | V0.x.x.json", "blt7cd9c7438ee7322e"),
    ("docs/json/Version 1.x.x/CLI Commands/Bulk Publish and Unpublish Content | V1.x.x.json", "blt804647818d4181f9"),
    ("docs/json/Version 1.x.x/CLI Commands/CLI-Supported Features for Export, Import, and Clone Operations | V1.x.x.json", "blte46be17c7b0eacde"),
    ("docs/json/Version 1.x.x/Miscellaneous/CLI Limitations | V1.x.x.json", "blt74918691c8a465c1"),
]


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()

    for rel_path, uid in TARGETS:
        local_path = os.path.join(ROOT, rel_path)
        with open(local_path, encoding="utf-8") as fh:
            local = json.load(fh)
        local_content = article_section(local)["content"]

        entry = get_entry(headers, DOCS_ARTICLE, uid)
        live_section = article_section(entry)
        live_content = live_section["content"]

        if live_content == local_content:
            print(f"[unchanged] {uid}  {rel_path}")
            continue

        print(f"[{'PUSH' if confirm else 'DRY-RUN'}] {uid}  {rel_path}")

        if not confirm:
            continue

        live_section["content"] = local_content
        updated = put_entry(headers, DOCS_ARTICLE, uid, entry)
        publish_entry(headers, DOCS_ARTICLE, uid, updated["_version"])
        print(f"  updated to version {updated['_version']} and published")


if __name__ == "__main__":
    main()
