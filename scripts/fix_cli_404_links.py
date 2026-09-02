#!/usr/bin/env python3
"""Fix every broken link and dead in-page anchor found across the CLI docs.

Found by scripts/sweep_cli_links.py against what production serves. Three kinds:

  1. Wrong version suffix. Links to the Asset Scanning page use the bare URL, but
     the page lives at /asset-scanning-in-cli/v1, so the bare URL 404s.
  2. A stale legacy URL. /docs/developers/cli/configure-regions 404s. The
     redirect table only covers the longer configure-regions-in-the-cli form.
  3. Dead in-page anchors. Mostly apostrophe drift: the anchor was written as
     contentstack-s-... while the rendered id is contentstacks-... . One anchor
     points at app.contentstack.com instead of the page it meant.

Worth knowing about anchors: the docs renderer emits ids for h2 and h3 headings
only, never h4. Verified on the V1-to-V2 migration guide, where 13/13 h2 and
55/55 h3 ids resolve and 0/43 h4 ids do. Two anchors on that page target h4
headings and are therefore NOT fixable by rewriting the anchor. They need the
heading promoted to h3, which is a content-structure decision, so they are listed
in UNFIXABLE below rather than silently rewritten.

Replacements match on href="..." rather than on the bare URL, so a URL mentioned
in prose or in a code sample is never touched. Every replacement declares how
many times it must match, and a mismatch aborts the run.

Usage:
  python3 scripts/fix_cli_404_links.py            # dry run
  python3 scripts/fix_cli_404_links.py --confirm  # PUT + publish to staging and development
"""

import sys
import time

from cli_docs_common import (DOCS_ARTICLE, article_section, get_entry, load_env,
                             publish_entry, put_entry)

ASSET_SCANNING_OLD = "/docs/headless-cms/asset-scanning-in-cli"
ASSET_SCANNING_NEW = "/docs/headless-cms/asset-scanning-in-cli/v1"

# (uid, label, [(old href, new href, expected match count), ...])
TARGETS = [
    # 1. Asset Scanning page moved to /v1 during the URL restructure.
    ("blt1ee86e6419f390f8", "Import Content Using the CLI | V1.x.x",
     [(ASSET_SCANNING_OLD, ASSET_SCANNING_NEW, 1)]),
    ("blt74918691c8a465c1", "CLI Limitations | V1.x.x",
     [(ASSET_SCANNING_OLD, ASSET_SCANNING_NEW, 2)]),

    # 2. Legacy /developers/cli/ URL with no redirect covering it.
    ("blt64294e11f81fe300", "Create Custom CLI Plugins for Contentstack | V2.x.x",
     [("https://www.contentstack.com/docs/developers/cli/configure-regions",
       "/docs/headless-cms/configure-regions-in-the-cli", 2)]),

    # 3a. Anchor truncated at the inline code in the heading it points to. The
    #     heading is `### Assets remain unpublished after `cm:assets:publish
    #     --backup-dir``, and the rendered id stops at the backtick.
    ("blt804647818d4181f9", "Bulk Publish and Unpublish Content | V1.x.x",
     [("#assets-remain-unpublished-after-cmassetspublish---backup-dir",
       "#assets-remain-unpublished-after", 1)]),
    # Same truncation, on the Asset Scanning page's own Limitations bullet.
    ("blt6ee109a7b3725e1c", "Asset Scanning in CLI | V1.x.x",
     [("#assets-remain-unpublished-after-cmassetspublish---backup-dir",
       "#assets-remain-unpublished-after", 1)]),

    # 3b. Apostrophe drift, seed command (V2, V1, V0).
    ("blt9f703f1d6c0405d9", "Import Content Using the Seed Command | V2.x.x",
     [("#import-from-contentstack-s-github-organization",
       "#import-from-contentstacks-github-organization", 3),
      ("#upload-stack-s-content-on-github",
       "#upload-stacks-content-on-github", 2)]),
    ("bltd980d5d1a241b442", "Import Content Using the Seed Command | V1.x.x",
     [("#import-from-contentstack-s-github-organization",
       "#import-from-contentstacks-github-organization", 3),
      ("#upload-stack-s-content-on-github",
       "#upload-stacks-content-on-github", 2)]),
    ("blt78f6b7d84156806f", "Import Content using the Seed Command | V0.x.x",
     [# This one points at the Contentstack app instead of the page, so the whole
      # href is replaced rather than just the fragment.
      ("https://app.contentstack.com/#option-1-import-from-contentstack-s-github-organization",
       "#option-1-import-from-contentstacks-github-organization", 1),
      ("#option-1-import-from-contentstack-s-github-organization",
       "#option-1-import-from-contentstacks-github-organization", 1),
      ("#option-1-import-from-contentstacks-organization",
       "#option-1-import-from-contentstacks-github-organization", 1),
      ("#option-2-import-from-github-repository",
       "#option-2-import-from-non-contentstacks-github-repository", 1),
      ("#option-2-import-from-non-contentstack-s-github-repository",
       "#option-2-import-from-non-contentstacks-github-repository", 2),
      ("#upload-stack-s-content-on-github",
       "#upload-stacks-content-on-github", 2)]),

    # 3c. Heading is "Login to the Contentstack CLI session", anchor drops "the".
    ("blt992979390532a894", "Migrate your Content using the CLI Migration Command | V2.x.x",
     [("#login-to-contentstack-cli-session",
       "#login-to-the-contentstack-cli-session", 1)]),
    ("blt563cc44829432a89", "Migrate your Content using the CLI Migration Command | V1.x.x",
     [("#login-to-contentstack-cli-session",
       "#login-to-the-contentstack-cli-session", 1)]),
    ("bltce91c490961bf924", "Migrate your Content using the CLI Migration Command | V0.x.x",
     [("#login-to-contentstack-cli-session",
       "#login-to-the-contentstack-cli-session", 1)]),

    # 3d. Heading is "Use the 'cm:export-to-csv' command"; the id drops the colon.
    ("blt0a21fe8af5279f9d", "Export Content to .CSV File | V0.x.x",
     [("#use-the-cm-export-to-csv-command",
       "#use-the-cmexport-to-csv-command", 1)]),

    # 3e. Heading is "Using Flags to Migrate Content", anchor adds "the".
    ("bltcddcfb50d44a61db", "Migrate Content from HTML RTE to JSON RTE | V0.x.x",
     [("#using-flags-to-migrate-the-content",
       "#using-flags-to-migrate-content", 1)]),
]

# seo.title corrections, applied to the same entries or standalone.
SEO_TITLES = [
    ("blt6ee109a7b3725e1c", "Asset Scanning in CLI | V1.x.x",
     "Asset Scanning in CLI | Contentstack",
     "Asset Scanning in CLI | V1.x.x | Contentstack"),
]

# Reported, not rewritten. Both target h4 headings, which never get an id.
UNFIXABLE = [
    ("blt05c442f72f396864", "Migrate from Contentstack CLI V1 to V2 | V2.x.x",
     "#global-fields-format-changed-per-file",
     'targets the h4 "Global Fields Format Changed (Per-File)"'),
    ("blt05c442f72f396864", "Migrate from Contentstack CLI V1 to V2 | V2.x.x",
     "#removed-import-config-keys-custom-plugins-and-config-files",
     'targets the h4 "Removed Import Config Keys (Custom Plugins and Config Files)"'),
]


def apply_replacements(html, replacements, label):
    """Rewrite href values.

    Idempotent: a replacement whose old href is already gone is treated as done, so
    the script can be re-run after a partial pass. Any other count mismatch means
    the content drifted for some other reason, and that aborts the run.
    """
    changes = []
    for old, new, expected in replacements:
        needle, target = f'href="{old}"', f'href="{new}"'
        found = html.count(needle)
        if found == 0:
            continue
        if found != expected:
            sys.exit(f"{label}: expected {expected} occurrence(s) of href=\"{old}\", "
                     f"found {found}. Content has drifted, refusing to write.")
        html = html.replace(needle, target)
        changes.append((old, new, found))
    return html, changes


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    print("LIVE RUN\n" if confirm else "DRY RUN (pass --confirm to write)\n")

    touched = 0
    for uid, label, replacements in TARGETS:
        entry = get_entry(headers, DOCS_ARTICLE, uid)
        section = article_section(entry)
        before = section["content"]
        after, changes = apply_replacements(before, replacements, label)

        if after == before:
            print(f"[unchanged] {uid}  {label}")
            continue

        print(f"[{'FIX' if confirm else 'DRY-RUN'}] {uid}  v{entry['_version']}  {label}")
        for old, new, count in changes:
            print(f"      {count}x  {old}\n           ->  {new}")
        touched += 1

        if not confirm:
            continue

        section["content"] = after
        updated = put_entry(headers, DOCS_ARTICLE, uid, entry)
        publish_entry(headers, DOCS_ARTICLE, uid, updated["_version"])
        print(f"      wrote v{updated['_version']}, published to staging and development")
        time.sleep(0.3)

    for uid, label, old, new in SEO_TITLES:
        entry = get_entry(headers, DOCS_ARTICLE, uid)
        seo = entry.get("seo") or {}
        current = seo.get("title")
        if current == new:
            print(f"[unchanged] {uid}  {label}  seo.title already correct")
            continue
        if current != old:
            print(f"[SKIP] {uid}  {label}  seo.title is {current!r}, "
                  f"expected {old!r}. Leaving it alone.")
            continue
        print(f"[{'FIX' if confirm else 'DRY-RUN'}] {uid}  v{entry['_version']}  {label}")
        print(f"      seo.title  {current!r}\n           ->  {new!r}")
        touched += 1
        if not confirm:
            continue
        seo["title"] = new
        entry["seo"] = seo
        updated = put_entry(headers, DOCS_ARTICLE, uid, entry)
        publish_entry(headers, DOCS_ARTICLE, uid, updated["_version"])
        print(f"      wrote v{updated['_version']}, published to staging and development")
        time.sleep(0.3)

    print(f"\n{touched} entry(s) {'updated' if confirm else 'would change'}.")

    print("\n=== Broken anchors this script deliberately does NOT rewrite ===")
    print("The docs renderer emits anchor ids for h2 and h3 headings only, never h4.")
    print("These anchors point at h4 headings, so no anchor text can make them work.")
    print("Fixing them means promoting the target heading to h3, which is a content")
    print("structure change, not a link fix.\n")
    for uid, label, anchor, why in UNFIXABLE:
        print(f"  {uid}  {label}\n      {anchor}\n      {why}")

    if confirm:
        print("\nNext: python3 scripts/stage_cli_cleanup_releases.py --release A")
    return 0


if __name__ == "__main__":
    sys.exit(main())
