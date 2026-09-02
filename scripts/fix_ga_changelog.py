#!/usr/bin/env python3
"""Correct the CLI 2.0.0 GA changelog entry, drafted locally.

The changelog is generated from the CMS the same way the docs are, which is easy
to miss:

    CMS changelog_details blt48436d263389bb65
      -> scripts/export_changelog_cli.py       -> docs/json/changelog/2.x/cli-2.0.0.json
      -> scripts/changelog_json_to_markdown.py -> changelog/2.x/cli-2.0.0.md

So changelog/2.x/cli-2.0.0.md is rendered output and editing it achieves nothing.
This edits the `description` HTML in the docs/json copy. No CMS write.

Two classes of correction, both established by diffing the last 1.x release of
each plugin against 2.0.0, using the oclif.manifest.json inside each published
npm tarball:

  A. Four short-flag claims are true but partial. The current wording says "in
     favor of long-form only", which reads as total removal, and the three flags
     it offers as examples are three that KEPT their short forms. Replaced with
     the characters actually removed and the ones that remain.

  B. Four changes are missing entirely. The most serious is the
     cm:stacks:migration configuration interface, where --config kept its name
     and changed its meaning. That is the only flag in the CLI that did so, and a
     V1 script passing inline values to --config is now read as a file path
     rather than failing, so it is a silent breaking change.

Usage:
  python3 scripts/fix_ga_changelog.py            # dry run, shows the diff
  python3 scripts/fix_ga_changelog.py --confirm  # write
"""

import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "docs", "json", "changelog", "2.x", "cli-2.0.0.json")


def c(text):
    return f'<span class="code">{text}</span>'


def flags(*chars):
    return ", ".join(c("-" + x) for x in chars)


# --- A. Reword the four partial claims -------------------------------------
# Each key is the exact <li> currently in the entry. Matched literally, so a
# silent no-op is impossible: a miss is reported rather than skipped.
REWORDS = {
    # cli-cm-export
    (f'<li>Removed deprecated short flags in favor of long-form only '
     f'({c("--data-dir")}, {c("--stack-api-key")}, {c("--alias")}, etc.).</li>'):
        (f'<li>Removed the short flags {flags("A", "B", "m", "s", "t")} from '
         f'{c("cm:stacks:export")}. The short forms {flags("a", "c", "d", "k", "y")} '
         f'are unchanged, so {c("--data-dir")}, {c("--stack-api-key")} and '
         f'{c("--alias")} keep {c("-d")}, {c("-k")} and {c("-a")}.</li>'),

    # cli-cm-import
    '<li>Removed deprecated short flags in favor of long-form only.</li>':
        (f'<li>Removed the short flags {flags("A", "B", "b", "m", "s")} from '
         f'{c("cm:stacks:import")}. The short forms {flags("a", "c", "d", "k", "y")} '
         f'are unchanged.</li>'),

    # cli-migration and cli-external-migrate
    ('<li>Cleaned up additional short-character flags in favor of long-form '
     'flags only.</li>'):
        (f'<li>Removed the short flags {flags("A", "B", "n")} from '
         f'{c("cm:stacks:migration")}. The short forms {flags("a", "k")} are '
         f'unchanged.</li>'),
}

# The content-type claim spans a longer <li>, so it is matched on its distinctive
# opening rather than in full.
CONTENT_TYPE_OLD = ("Removed deprecated flags and ambiguous short characters "
                    "across all six")
CONTENT_TYPE_NEW = (
    f'Removed the short flags {flags("c", "d", "l", "o", "p", "r", "s", "t")} '
    f'across the six {c("content-type:*")} commands (audit, compare, '
    f'compare-remote, details, diagram, list). {flags("a", "k")} are unchanged, '
    f'except on {c("content-type:compare-remote")}, which now has no short flags')


# --- B. The four missing entries -------------------------------------------
# Inserted as a Breaking Changes block, because the migration one is a breaking
# change and the current entry has nowhere that says so.
MISSING_BLOCK = (
    '<p><strong>Breaking Changes:</strong></p>'
    '<ul>'
    f'<li><strong>{c("cm:stacks:migration")} configuration flags changed.</strong> '
    f'{c("--config")} now takes the path of a JSON configuration file, inline '
    f'configuration moved to the new {c("--inline-config")} flag, and '
    f'{c("--config-file")} is removed. {c("--config")} kept its name and changed '
    'its meaning, so a script written for CLI 1.x that passes inline values to '
    f'{c("--config")} is read as a file path rather than failing outright. Update '
    f'those calls to {c("--inline-config")}.</li>'
    f'<li>Removed {c("--reference-only")} from {c("cm:stacks:audit")} and '
    f'{c("cm:stacks:audit:fix")}.</li>'
    f'<li>Removed {c("--app-type")} from {c("cm:bootstrap")}.</li>'
    f'<li>Removed {c("--fetch-limit")} from {c("cm:stacks:seed")}.</li>'
    '</ul>'
)


def main():
    confirm = "--confirm" in sys.argv
    entry = json.load(open(TARGET, encoding="utf-8"))
    html = entry["description"]
    original = html
    applied, missed = [], []

    for old, new in REWORDS.items():
        if old in html:
            html = html.replace(old, new, 1)
            applied.append("reworded: " + re.sub(r"<[^>]+>", "", old)[:64])
        else:
            missed.append(re.sub(r"<[^>]+>", "", old)[:74])

    m = re.search(r"<li>" + re.escape(CONTENT_TYPE_OLD) + r"(?:(?!</li>).)*</li>",
                  html, re.S)
    if m:
        html = html.replace(m.group(0), f"<li>{CONTENT_TYPE_NEW}.</li>", 1)
        applied.append("reworded: content-type short characters")
    else:
        missed.append(CONTENT_TYPE_OLD)

    if "Breaking Changes" not in html:
        html = MISSING_BLOCK + html
        applied.append("added a Breaking Changes block with 4 missing entries")

    print(f"target: {os.path.relpath(TARGET, ROOT)}")
    print(f"entry:  {entry['uid']}  version {entry['_version']}\n")
    for a in applied:
        print("  applied  " + a)
    for x in missed:
        print("  MISSED   " + x)
    if missed:
        print("\nA missed pattern means the entry text has changed since this was "
              "written. Re-read it rather than forcing the edit.")
    print(f"\ndescription: {len(original)} -> {len(html)} chars")

    if not confirm:
        print("\nDry run. Nothing written. Re-run with --confirm.")
        return
    if missed:
        sys.exit("\nRefusing to write with unmatched patterns.")

    entry["description"] = html
    with open(TARGET, "w", encoding="utf-8") as fh:
        json.dump(entry, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("\nwritten. Regenerating changelog/ ...")
    subprocess.run([sys.executable,
                    os.path.join(ROOT, "scripts", "changelog_json_to_markdown.py")],
                   check=False)


if __name__ == "__main__":
    main()
