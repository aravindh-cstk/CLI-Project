#!/usr/bin/env python3
"""Phase 2: repoint in-content CLI cross-links at the new versioned URLs.

Two rules, depending on whether the link names a version:

  Explicit version segment (/beta, /old-commands, /v0, /v1)
      The link already names one specific doc, so it maps to that doc's new URL.
      A GA doc linking to ".../cli-content-type-plugin/beta" wants the V2 doc and
      keeps wanting it, so it becomes ".../cli-content-type-plugin".

  No version segment
      In-version linking: a V1 doc links to the target's /v1, a V0 doc to /v0, a
      V2 doc to the bare URL, falling back to the nearest version that exists.

Only slugs in cli-url-map.csv are touched, so links to non-CLI docs such as
/docs/headless-cms/about-entries are left exactly as they are. The host and the
/docs prefix are preserved as found. A trailing slash is dropped, so every
rewritten link matches the one form used by the url field and the redirect table.

After writing, regenerate the markdown mirror:
  python3 scripts/json_to_markdown.py

Usage:
  python3 scripts/rewrite_cli_links.py            # dry run
  python3 scripts/rewrite_cli_links.py --confirm  # write the files
"""

import collections
import json
import os
import re
import sys

import cli_url_map as url_map
from apply_cli_url_fields_local import UNTRACKED_DRAFTS
from cli_docs_common import ROOT, load_index

JSON_DIR = os.path.join(ROOT, "docs", "json")

VERSION_SEGMENTS = {
    "/beta": "Beta",
    "/old-commands": "old",
    "/v0": "old",
    "/v1": "GA",
}

LINK = re.compile(
    r"(?P<host>https?://[^\"'\s<>\\]*?)?"
    r"(?P<prefix>/docs)?"
    r"/headless-cms/(?P<slug>[a-zA-Z0-9\-]+)"
    r"(?P<version>/beta|/old-commands|/v0|/v1)?"
    r"(?P<slash>/)?"
    r"(?P<anchor>\#[A-Za-z0-9\-_]*)?"
)

# Links still on the pre-2024 information architecture. These resolve today only
# because the legacy redirect table forwards them, and after the restructure some
# of those forwards would land on a URL that no longer exists. Repointing them at
# the real target removes the hop as well as the risk.
LEGACY_LINK = re.compile(
    r"(?P<host>https?://[^\"'\s<>\\]*?)?"
    r"(?P<prefix>/docs)?"
    r"/developers/cli/(?P<slug>[a-zA-Z0-9\-]+)"
    r"(?P<version>/beta|/old-commands)?"
    r"(?P<slash>/)?"
    r"(?P<anchor>\#[A-Za-z0-9\-_]*)?"
)


def build_lookup(docs):
    """slug -> {bucket: new_url}, keyed by both the old and the new slug.

    Content in an already-migrated file may reference either spelling, so both
    resolve and the script stays safe to re-run.
    """
    lookup = collections.defaultdict(dict)
    for doc in docs:
        lookup[doc["slug"]][doc["bucket"]] = doc["new_url"]
        lookup[doc["new_slug"]][doc["bucket"]] = doc["new_url"]
    return lookup


def make_rewriter(docs, lookup, from_bucket, report, migrated=False, legacy=False):
    """Return a re.sub callback that rewrites one CLI link, or leaves it alone.

    migrated says the source document has already been through this rewrite. It
    matters because a bare current-IA link is ambiguous afterwards: before the
    migration a bare link from a V1 doc meant the V1 doc, and after it means the
    V2 doc that now owns the bare URL. Rewriting one a second time would drag a
    deliberate V2 link back to /v1, so bare links in a migrated document are left
    exactly as they are. Legacy-IA links are never correct, migrated or not.
    """

    def rewrite(match):
        whole = match.group(0)
        slug = match.group("slug")
        if slug not in lookup:
            return whole

        version = match.group("version")
        if migrated and not legacy and not version:
            return whole

        if version:
            bucket = VERSION_SEGMENTS[version]
            target = lookup[slug].get(bucket)
            if target is None:
                # The named version has no doc. Fall back to in-version resolution
                # rather than emitting a URL that will not resolve.
                target = url_map.link_target(docs, slug, from_bucket)
                report.append(("no-such-version", whole, target))
        else:
            target = url_map.link_target(docs, slug, from_bucket)

        if target is None:
            report.append(("unresolved", whole, None))
            return whole

        new = f"{match.group('host') or ''}{match.group('prefix') or ''}{target}"
        new += match.group("anchor") or ""
        return new

    return rewrite


def rewrite_all(text, current, legacy):
    """Apply the current-IA pattern then the legacy-IA pattern to one string."""
    return LEGACY_LINK.sub(legacy, LINK.sub(current, text))


def rewrite_entry(entry, docs, lookup, from_bucket, migrated=False):
    """Rewrite CLI links in the content fields. Returns (changed_count, report)."""
    report = []
    current = make_rewriter(docs, lookup, from_bucket, report, migrated, legacy=False)
    legacy = make_rewriter(docs, lookup, from_bucket, report, migrated, legacy=True)
    changed = 0

    for block in entry.get("article_content") or []:
        section = block.get("article_section")
        if not section:
            continue
        for field in ("content", "heading"):
            before = section.get(field)
            if not isinstance(before, str) or not before:
                continue
            after = rewrite_all(before, current, legacy)
            if after != before:
                section[field] = after
                changed += 1

    before = entry.get("md_content")
    if isinstance(before, str) and before:
        after = rewrite_all(before, current, legacy)
        if after != before:
            entry["md_content"] = after
            changed += 1

    return changed, report


def count_links(text, lookup):
    return sum(1 for m in LINK.finditer(text) if m.group("slug") in lookup)


def main():
    confirm = "--confirm" in sys.argv
    docs = url_map.load_map()
    lookup = build_lookup(docs)
    index = load_index()
    by_uid = {d["uid"]: d for d in docs}

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")

    total_links = 0
    touched = []
    problems = []
    samples = collections.Counter()

    # Tracked docs plus the local drafts, which carry CLI links of their own and
    # would otherwise keep pointing at pre-restructure URLs.
    work = [(r["json"], by_uid[r["uid"]]["bucket"], by_uid[r["uid"]]["new_url"])
            for r in index["entries"]]
    work += [(f"{bucket}/{slug}.json", bucket, url_map.new_url(slug, bucket))
             for bucket, slug in UNTRACKED_DRAFTS
             if os.path.exists(os.path.join(JSON_DIR, f"{bucket}/{slug}.json"))]

    for rel_path, from_bucket, new_url in sorted(work):
        path = os.path.join(JSON_DIR, rel_path)
        with open(path, encoding="utf-8") as fh:
            entry = json.load(fh)
        # Phase 1 already set url on every local file, so bare links here are
        # final and must not be re-resolved. See make_rewriter's migrated flag.
        migrated = entry.get("url") == new_url

        original = json.dumps(entry, ensure_ascii=False)
        links_here = sum(
            count_links(block["article_section"].get("content") or "", lookup)
            for block in entry.get("article_content") or []
            if block.get("article_section")
        )
        changed, report = rewrite_entry(entry, docs, lookup, from_bucket, migrated)
        updated = json.dumps(entry, ensure_ascii=False)
        total_links += links_here

        for kind, whole, target in report:
            problems.append((rel_path, kind, whole, target))

        if updated != original:
            touched.append((rel_path, entry, links_here))
            for before, after in diff_links(original, updated, lookup):
                samples[(before, after)] += 1

    print(f"{len(touched)} of {len(index['entries'])} docs have CLI links to repoint, "
          f"{total_links} CLI link occurrences scanned.\n")

    print("Rewrites, most frequent first:")
    for (before, after), count in samples.most_common(40):
        print(f"  {count:4}  {before}")
        print(f"        -> {after}")
    if len(samples) > 40:
        print(f"  ... and {len(samples) - 40} more distinct rewrites")

    if problems:
        print("\nLinks that could not be resolved cleanly:")
        for rel, kind, whole, target in problems:
            print(f"  [{kind}] {rel}: {whole} -> {target}")

    if not confirm:
        print("\nDry run complete, no writes made.")
        return

    for rel, entry, _ in touched:
        with open(os.path.join(JSON_DIR, rel), "w", encoding="utf-8") as fh:
            json.dump(entry, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

    print(f"\nRewrote {len(touched)} JSON file(s).")
    print("Next: python3 scripts/json_to_markdown.py")


def all_cli_links(blob, lookup):
    """Every CLI link in a blob, current IA and legacy IA, in document order."""
    found = []
    for pattern in (LINK, LEGACY_LINK):
        for match in pattern.finditer(blob):
            if match.group("slug") in lookup:
                found.append((match.start(), match.group(0)))
    return [text for _, text in sorted(found)]


def diff_links(before_blob, after_blob, lookup):
    """Pair up the CLI links that changed between two serialized entries."""
    old = all_cli_links(before_blob, lookup)
    new = all_cli_links(after_blob, lookup)
    return [(o, n) for o, n in zip(old, new) if o != n]


if __name__ == "__main__":
    main()
