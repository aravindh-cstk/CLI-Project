#!/usr/bin/env python3
"""Make every internal docs link root-relative.

Nine links in the corpus are written as https://www.contentstack.com/docs/...
instead of /docs/... . An absolute link sends the reader to production whatever
environment they are on, so on staging it jumps them out of the environment they
are reviewing. That is why the link paths could not be reviewed on staging.

Not touched, on purpose: https://www.contentstack.com/login and /login/, which
appear 62 times in Prerequisites bullets. That is the application, not the docs
site, and it is not environment mirrored, so an absolute URL is correct there.

One of the nine is also pointing at the wrong version. Create Custom CLI Plugins
for Contentstack | V1.x.x opens with "how to develop an external plugin for
[Contentstack CLI]" linking the V2 install page. A V1 reader following it lands
on 2.0.0 instructions. Retargeted to /v1 in the same pass.

Two things checked and found NOT to be defects, recorded so nobody re-opens them:

  The V0 links to cli-authentication/v0 are inside V0 docs, so the version is
  right and only the form is wrong. An earlier reading of this called them a
  three-version regression, which was wrong.

  Configure Regions V0 links both content-delivery-api and
  content-management-api, and the link texts match their targets. A first pass
  read the wrong adjacent text and made it look like a mislabel.

Usage:
  python3 scripts/fix_absolute_internal_links.py            # dry run
  python3 scripts/fix_absolute_internal_links.py --confirm  # write
"""

import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.docs_html import JSON_DIR  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "https://www.contentstack.com"

# Absolute docs links become root-relative. The docs prefix is kept, because the
# stored href includes it, unlike the url field in index.json.
ABSOLUTE_DOCS = re.compile(r'https?://www\.contentstack\.com(/docs/)')

# The one version mismatch, fixed only in this doc.
VERSION_FIX = (
    "Version 1.x.x/Miscellaneous/Create Custom CLI Plugins for Contentstack | V1.x.x.json",
    '<a href="/docs/headless-cms/install-the-cli" target="_blank">Contentstack CLI</a>',
    '<a href="/docs/headless-cms/install-the-cli/v1" target="_blank">Contentstack CLI</a>',
)

# Left alone, reported instead. Change Master Locale is one entry shown in both
# the V1 and V2 trees, so a version-neutral install link is arguably right and
# picking a version would be wrong for one of the two readerships.
SHARED_ENTRY_NOTE = (
    "blt278785a9d6da5074 / blt3afca0a8bf912f83 (Change Master Locale, and Update "
    "Missing Reference UIDs) link /docs/headless-cms/install-the-cli with no version "
    "suffix. These are single entries shown in both version trees, so a suffix would "
    "be wrong for one of the two readerships. Left version-neutral."
)


def article_section(entry):
    for block in entry.get("article_content") or []:
        if "article_section" in block:
            return block["article_section"] or {}
    return {}


def main():
    confirm = "--confirm" in sys.argv
    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to write\n")

    index = json.load(open(os.path.join(JSON_DIR, "index.json"), encoding="utf-8"))
    paths = sorted({row["json"] for row in index["entries"]})

    total, touched, version_fixed = 0, 0, False
    for rel in paths:
        path = os.path.join(JSON_DIR, rel)
        entry = json.load(open(path, encoding="utf-8"))
        section = article_section(entry)
        html = section.get("content") or ""
        found = ABSOLUTE_DOCS.findall(html)
        new_html = ABSOLUTE_DOCS.sub(r"\1", html)

        extra = ""
        if rel == VERSION_FIX[0]:
            if VERSION_FIX[1] in new_html:
                new_html = new_html.replace(VERSION_FIX[1], VERSION_FIX[2], 1)
                extra = "  + retargeted the install link to /v1"
                version_fixed = True
            elif VERSION_FIX[2] in new_html:
                extra = "  (install link already at /v1)"

        if new_html == html:
            continue
        total += len(found)
        touched += 1
        print(f"  {len(found)} absolute -> relative{extra}")
        print(f"      {rel}")
        for url in sorted(set(re.findall(
                r'https?://www\.contentstack\.com(/docs/[^"\\ )<]+)', html))):
            print(f"        {HOST}{url}")
            print(f"          -> {url}")
        if confirm:
            section["content"] = new_html
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(entry, fh, indent=2, ensure_ascii=False)
                fh.write("\n")

    print(f"\n{total} absolute docs links across {touched} files")
    if rel and not version_fixed and confirm:
        print("NOTE: the version retarget did not match. Check it by hand.")
    print(f"\nnote: {SHARED_ENTRY_NOTE}")

    if not confirm:
        print("\nDry run complete. Nothing written.")
        return 0
    print("\nRegenerating docs/markdown ...")
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "json_to_markdown.py")],
                   check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
