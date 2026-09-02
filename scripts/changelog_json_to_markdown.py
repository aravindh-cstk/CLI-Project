#!/usr/bin/env python3
"""Convert the CLI changelog JSON under docs/json/changelog/ into Markdown
under changelog/.

Layout mirrors the export: docs/json/changelog/<line>/<slug>.json becomes
changelog/<line>/<slug>.md. Each document is the entry title as an H1, the
release date, then the converted description HTML.

Run scripts/export_changelog_cli.py first to refresh the JSON.

Usage: python3 scripts/changelog_json_to_markdown.py
"""

import json
import os
import re
import sys

from json_to_markdown import Converter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(ROOT, "docs", "json", "changelog")
MD_DIR = os.path.join(ROOT, "changelog")

HEADING_RE = re.compile(r"<(h[1-6])\b[^>]*>(.*?)</\1>", re.IGNORECASE | re.DOTALL)


def demote_headings(html):
    """Render heading tags as bold paragraphs instead of '#' markers.

    Changelog RTE authors mix real <h2>/<h3> tags with <p><strong> for the same
    visual bold-label intent. Left as headings they would compete with the "# title"
    H1 emitted below. The shared Converter in json_to_markdown.py has no
    demote_headings flag and is used by the other docs scripts, so the rewrite
    happens here rather than in shared code.
    """
    return HEADING_RE.sub(lambda m: f"<p><strong>{m.group(2)}</strong></p>", html)


def main():
    if not os.path.isdir(JSON_DIR):
        print(f"WARNING: missing {JSON_DIR}", file=sys.stderr)
        return 1

    converter = Converter()
    written = 0
    problems = []

    for dirpath, _dirnames, filenames in os.walk(JSON_DIR):
        rel_dir = os.path.relpath(dirpath, JSON_DIR)
        for filename in sorted(filenames):
            if not filename.endswith(".json"):
                continue
            rel_path = os.path.join(rel_dir, filename) if rel_dir != "." else filename
            with open(os.path.join(dirpath, filename), encoding="utf-8") as fh:
                entry = json.load(fh)

            title = (entry.get("title") or "").strip()
            if not title:
                problems.append(f"{rel_path}: no title")

            date = (entry.get("date") or "").strip()

            body = converter.convert(demote_headings(entry.get("description") or ""))
            if not body:
                problems.append(f"{rel_path}: empty body")

            slug = filename[: -len(".json")]
            document = f"# {title}\n\n{date}\n\n{body}\n"
            out_dir = os.path.join(MD_DIR, rel_dir) if rel_dir != "." else MD_DIR
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, f"{slug}.md"), "w", encoding="utf-8") as fh:
                fh.write(document)
            written += 1

    print(f"total {written}")
    for problem in problems:
        print(f"WARNING: {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
