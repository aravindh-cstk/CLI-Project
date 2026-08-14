#!/usr/bin/env python3
"""Add the four 404-link-fix docs_article entries to a release.

Usage:
  python3 scripts/add_link_fixes_to_release.py            # dry run
  python3 scripts/add_link_fixes_to_release.py --confirm  # create release + add items
"""

import sys

from cli_docs_common import DOCS_ARTICLE, LOCALE, get_entry, load_env
from cli_release import add_item, ensure_release, index_items

RELEASE_NAME = "CLI 404 fixes Aug 14"

TARGETS = [
    ("blt7cd9c7438ee7322e", "Bulk Publish and Unpublish Content | V0.x.x"),
    ("blt804647818d4181f9", "Bulk Publish and Unpublish Content | V1.x.x"),
    ("blte46be17c7b0eacde", "CLI-Supported Features for Export, Import, and Clone Operations | V1.x.x"),
    ("blt74918691c8a465c1", "CLI Limitations | V1.x.x"),
]


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()

    release_uid = ensure_release(headers, RELEASE_NAME, confirm=confirm)
    if not release_uid:
        print(f"Release {RELEASE_NAME!r} does not exist yet. Rerun with --confirm to create it.")
        return

    existing = index_items(headers, release_uid)

    for uid, label in TARGETS:
        entry = get_entry(headers, DOCS_ARTICLE, uid)
        version = entry["_version"]
        if not confirm:
            key = (DOCS_ARTICLE, uid, LOCALE)
            state = "present" if existing.get(key) == version else "would add/update"
            print(f"[DRY-RUN] {uid}  v{version}  {label}  ({state})")
            continue
        outcome = add_item(headers, release_uid, DOCS_ARTICLE, uid, version, existing=existing)
        print(f"[{outcome}] {uid}  v{version}  {label}")


if __name__ == "__main__":
    main()
