#!/usr/bin/env python3
"""Export every changelog_details entry tagged "CLI" into docs/json/changelog/.

CLI changelog titles carry no language and no api_type (unlike the SDK changelog),
only a version, so the release line is derived from the major version alone:

    docs/json/changelog/<line>/cli-<version>.json
    e.g. docs/json/changelog/1.x/cli-1.55.0.json
         docs/json/changelog/2.x/cli-2.0.0-beta.4.json

A title naming a different product ("CLI Apps-CLI Version 1.0.4") is filed under
its own folder so it can never be mistaken for a core CLI release of the same
version number. A title with no parseable version is reported, never guessed at.

Run scripts/changelog_json_to_markdown.py afterwards to refresh changelog/.

Usage: python3 scripts/export_changelog_cli.py [--since=YYYY-MM-DD|--since=all]
  --since=YYYY-MM-DD  only export entries dated on or after this date
  --since=all         drop the date filter and export the full CLI history
Default: 2026-01-01.

Read-only against the stack: GET requests only.
"""

import json
import os
import re
import sys

from cli_docs_common import LOCALE, ROOT, load_env, request

CHANGELOG_CT = "changelog_details"
CLI_TAG_UID = "blta9b77391ce974879"     # changelog_tags entry: CLI
OUT_DIR = os.path.join(ROOT, "docs", "json", "changelog")
DEFAULT_MIN_DATE = "2026-01-01"
PAGE_SIZE = 100

# Known core-CLI release lines. A major outside this set is reported rather than
# silently creating a new top-level folder.
RELEASE_LINES = {"1", "2"}

# Titles append the release date in a few casings ("- Release date:", "- Release
# Date:"). Stripped before parsing so it can never be read as a version.
RELEASE_DATE_SUFFIX_RE = re.compile(r"\s*-\s*Release\s+[Dd]ate:.*$")

# "Apps-CLI" and friends are separate products that happen to carry the CLI tag.
PRODUCT_RE = re.compile(r"\b([A-Za-z0-9]+)-CLI\b", re.IGNORECASE)

# Bounded charset (not \S*) so the prerelease tail is captured without swallowing
# trailing prose: 1.55.0, 2.0.0-beta, 2.0.0-beta.4, 1.60.0-beta.6.
VERSION_RE = re.compile(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z][0-9A-Za-z.]*)?)")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

USAGE = ("Usage: python3 scripts/export_changelog_cli.py "
         "[--since=YYYY-MM-DD|--since=all]")


def parse_args(argv):
    """Return the date floor, or None for the full history."""
    since = DEFAULT_MIN_DATE
    for arg in argv:
        if not arg.startswith("--since="):
            sys.exit(f'Unknown argument "{arg}".\n{USAGE}')
        value = arg[len("--since="):].strip()
        if value == "all":
            since = None
            continue
        # Reject a typo'd date rather than falling back to a wider window.
        if not DATE_RE.match(value):
            sys.exit(f'--since expects YYYY-MM-DD or "all", got "{value}".')
        since = value
    return since


def normalize_title(raw_title):
    """Collapse whitespace runs and drop the release-date suffix.

    Reduces every real title shape to "[<prefix>] Version <version>", including
    "CLI Version  2.0.0-beta.5" (double space) and the 2022 entries that have no
    "CLI" prefix at all.
    """
    title = re.sub(r"\s+", " ", str(raw_title or "")).strip()
    return RELEASE_DATE_SUFFIX_RE.sub("", title).strip()


def classify(raw_title):
    """Return (directory, filename stem) for a title, or (None, reason)."""
    title = normalize_title(raw_title)
    if not title:
        return None, "empty title"

    product_match = PRODUCT_RE.search(title)
    product = None
    if product_match and product_match.group(1).lower() != "cli":
        product = f"{product_match.group(1).lower()}-cli"

    version_match = VERSION_RE.search(title)
    if not version_match:
        return None, "no parseable version"
    version = version_match.group(1).rstrip(".-")
    if not version:
        return None, "no parseable version"

    # A non-core product gets its own folder so it can never be mistaken for a
    # core CLI release carrying the same version number.
    if product:
        return (product, f"{product}-{version}"), None

    major = version.split(".")[0]
    if major not in RELEASE_LINES:
        return None, f"unexpected major version {major}"
    return (f"{major}.x", f"cli-{version}"), None


def fetch_entries(headers, since):
    """Page through every CLI-tagged changelog entry."""
    query = {"filters.uid": CLI_TAG_UID}
    if since:
        query["date"] = {"$gte": since}

    entries = []
    skip = 0
    while True:
        page = request("GET", f"/v3/content_types/{CHANGELOG_CT}/entries", headers,
                       params={"locale": LOCALE, "query": json.dumps(query),
                               "limit": PAGE_SIZE, "skip": skip})
        batch = page.get("entries") or []
        entries.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
        skip += PAGE_SIZE
    return entries


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main():
    since = parse_args(sys.argv[1:])
    headers = load_env()

    entries = fetch_entries(headers, since)
    print(f'Fetched {len(entries)} {CHANGELOG_CT} entries tagged "CLI" '
          f'(since={since or "all"}).')

    written_paths = set()
    per_dir = {}
    unmapped = []
    written = 0

    for entry in entries:
        placement, reason = classify(entry.get("title"))
        if placement is None:
            unmapped.append((entry, reason))
            continue
        directory, stem = placement
        rel_path = os.path.join(directory, f"{stem}.json")
        if rel_path in written_paths:
            print(f"WARNING: duplicate filename {rel_path} for uid {entry.get('uid')} "
                  f"(\"{entry.get('title')}\"), appending uid to disambiguate",
                  file=sys.stderr)
            rel_path = os.path.join(directory, f"{stem}-{entry.get('uid')}.json")
        written_paths.add(rel_path)
        write_json(os.path.join(OUT_DIR, rel_path), entry)
        per_dir[directory] = per_dir.get(directory, 0) + 1
        written += 1

    print(f"Classified and wrote {written} entries to docs/json/changelog/.")
    if per_dir:
        breakdown = ", ".join(f"{d}: {n}" for d, n in sorted(per_dir.items()))
        print(f"Per release line: {breakdown}")
    print(f"Unmapped (skipped): {len(unmapped)}")
    if unmapped:
        print("\nUnmapped entries (title | date | uid):")
        for entry, reason in unmapped:
            print(f"  {entry.get('title')} | {entry.get('date')} | "
                  f"{entry.get('uid')}  [{reason}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
