#!/usr/bin/env python3
"""Take the V2 asset-scanning documentation off production.

Asset scanning is a released feature for CLI V1 only. The V2 version has not
shipped, but V2 asset-scanning content is live on production: the 2026-08-06
rollback republished scan-free versions (v7, v14), and then the 2026-08-13 URL
restructure release published the drafts, which still held the content.

Two things are deliberate here and differ from every other push script:

  * This does NOT publish. Staging and development must stay on the version that
    still carries the asset-scanning content, so shipping it when V2 asset
    scanning launches is a publish rather than a rewrite. Production gets the
    stripped version through a release deployed to production only.
  * Removal is by exact literal HTML fragment, not by regex over scan markers. A
    fragment that no longer matches aborts the run instead of silently removing
    the wrong thing or nothing at all.

A version rollback is no longer an option: the scan-free versions predate the URL
restructure, so publishing them would revert these two pages to their old URLs.

Usage:
  python3 scripts/strip_v2_asset_scanning.py            # dry run
  python3 scripts/strip_v2_asset_scanning.py --confirm  # PUT, no publish
"""

import json
import os
import re
import sys

from cli_docs_common import (DOCS_ARTICLE, ROOT, article_section, get_entry,
                             load_env, put_entry)

BULK = "blt85d9deae08de968d"
IMPORT = "blt1215a1f9bbcc9900"

PARKED = os.path.join(ROOT, "asset-scanning-v2-parked.md")

# Fragments to delete, in the order they appear. Each must match exactly once.
BULK_FRAGMENTS = [
    # Asset-Specific Options table: the --data-dir and --dry-run rows
    ('<tr><td><span class="code">--data-dir</span>, <span class="code">-d</span></td>'
     '<td>Path to exported content folder containing asset publish details. '
     'Publishes assets from that folder instead of scanning the live stack.</td>'
     '<td><span class="code">--data-dir ./content</span></td></tr>'),
    ('<tr><td><span class="code">--dry-run</span></td><td>Preview the publish plan '
     'without making any API calls. Default: <span class="code">false</span>. Only '
     'takes effect when combined with <span class="code">--data-dir</span>. It has no '
     'effect on the default live-folder-scan publish or unpublish flow.</td>'
     '<td><span class="code">--dry-run</span></td></tr>'),
    # The Asset Scan Status dashboard paragraph
    ('<p>On stacks where asset scanning applies, <span class="code">cm:stacks:bulk-assets'
     '</span> prints an "Asset Scan Status" dashboard before publishing. The dashboard '
     'reports the total assets found, how many are clean and will publish, how many are '
     'still scanning (skipped), and how many are quarantined (skipped). In the '
     '<span class="code">--data-dir</span> flow, it also reports assets skipped locally '
     'for missing publish details and assets skipped for having no mapped UID. If no '
     'assets are publishable after this filtering, the command prints a warning and '
     'exits without publishing anything.</p>'),
    # Example 7, its code block, and the --dry-run paragraph that follows it
    ('<p><strong>7. Publish assets from an exported content folder (data-dir flow)'
     '</strong></p><pre># Publish assets from a backup or export folder after asset '
     'scanning clears\ncsdx cm:stacks:bulk-assets \\\n  --data-dir ./content \\\n  '
     '--operation publish \\\n  -k blt*******\n</pre><p>Add '
     '<span class="code">--dry-run</span> to preview which assets would publish without '
     'making any API calls. <span class="code">--dry-run</span> only affects this '
     '<span class="code">--data-dir</span> flow. It has no effect on the default publish '
     'or unpublish flow shown in examples 1 through 4.</p>'),
    # Troubleshooting: still scanning, no automatic retry
    ('<h3 id="assets-stay-in-still-scanning-status-with-no-automatic-retry">Assets stay '
     'in "still scanning" status with no automatic retry</h3><p><strong>Root Cause(s)'
     '</strong>: <span class="code">cm:stacks:bulk-assets</span> checks each asset\'s '
     'scan status once at command run time. There is no polling loop that waits for a '
     'pending scan to finish before deciding whether to publish. An asset in the scan '
     'queue at the time the command runs is skipped for that run.</p><p><strong>'
     'Resolution</strong>: Wait for the asset\'s scan to complete, then run the same '
     '<span class="code">cm:stacks:bulk-assets</span> command again. The command '
     'rechecks scan status on every run.</p>'),
    # Troubleshooting: empty asset UID mapper
    ('<h3 id="asset-uid-mapper-is-empty-warning-during-a-data-dir-publish">"Asset UID '
     'mapper is empty" warning during a <span class="code">--data-dir</span> publish</h3>'
     '<p><strong>Root Cause(s)</strong>: The <span class="code">mapper/assets/'
     'uid-mapping.json</span> file in the data directory is missing or contains no '
     'entries. This file maps source asset UIDs to their UIDs on the destination stack. '
     'Unlike a missing <span class="code">assets.json</span>, a missing or empty UID '
     'mapping file does not stop the command. It logs this warning and continues, and '
     'every asset in the run is then skipped because none can be mapped to a destination '
     'UID.</p><p><strong>Resolution</strong>: Confirm the data directory points at a '
     'completed import backup and that <span class="code">mapper/assets/uid-mapping.json'
     '</span> exists and is populated. Re-run the import if the mapping file was not '
     'generated.</p>'),
    # Troubleshooting: environment names as raw UIDs
    ('<h3 id="environment-names-show-as-raw-uids-instead-of-names-in-a-data-dir-publish">'
     'Environment names show as raw UIDs instead of names in a '
     '<span class="code">--data-dir</span> publish</h3><p><strong>Root Cause(s)</strong>: '
     'The <span class="code">environments/environments.json</span> file in the data '
     'directory is missing. Asset scanning falls back to using raw environment UIDs in '
     'place of names for output, and continues processing. This is a warning, not a '
     'failure.</p><p><strong>Resolution</strong>: Confirm the data directory contains '
     '<span class="code">environments/environments.json</span> from the same import '
     'backup. If it is missing, re-export or re-import to regenerate it.</p>'),
    # The whole Limitations section: all three bullets are asset-scanning only, and
    # this file had no Limitations section before asset scanning was added.
    ('<h2 id="limitations">Limitations</h2><ul><li><span class="code">--retry-failed'
     '</span> on <span class="code">cm:stacks:bulk-assets</span> rebuilds its item list '
     'from the failed-operation log only. It does not recheck asset scan status before '
     'retrying, so an asset that entered quarantine after the original run can still be '
     'retried.</li><li>The retry mechanism for assets still in the scan queue only checks '
     'scan status once per command invocation. See <a href="#assets-stay-in-still-'
     'scanning-status-with-no-automatic-retry">Assets stay in "still scanning" status '
     'with no automatic retry</a> for details and the workaround.</li><li>In the '
     '<span class="code">--data-dir</span> publish flow, a missing '
     '<span class="code">assets.json</span> in the data directory stops the command with '
     'an error. A missing <span class="code">mapper/assets/uid-mapping.json</span> or '
     '<span class="code">environments/environments.json</span> only logs a warning and '
     'the command continues with degraded behavior (all assets skipped, or environment '
     'names shown as raw UIDs).</li></ul>'),
    # The whole Next Steps section: its only item is the asset-scanning page, and this
    # file had no Next Steps section before asset scanning was added.
    #
    # Two accepted forms. Production carries the de-linked one: a link-rewrite pass
    # dropped the <a> because the bare asset-scanning URL 404s. The local mirror still
    # has the link. Either matches, so this works before or after the mirror is synced.
    (('<h2 id="next-steps">Next Steps</h2><ul><li>Asset Scanning in CLI: full reference '
      'for asset-scan gating behavior, the scan status dashboard, and troubleshooting for '
      '<span class="code">cm:stacks:bulk-assets</span>.</li></ul>'),
     ('<h2 id="next-steps">Next Steps</h2><ul><li><a href="/docs/headless-cms/'
      'asset-scanning-in-cli">Asset Scanning in CLI</a>: full reference for asset-scan '
      'gating behavior, the scan status dashboard, and troubleshooting for '
      '<span class="code">cm:stacks:bulk-assets</span>.</li></ul>')),
]

IMPORT_FRAGMENTS = [
    # The asset-scanning note after "Use of --backup-dir Flag", plus its code block
    ('<p>Asset scanning is rolling out as an org-plan feature. Once it is active for a '
     "stack's org plan, <span class=\"code\">cm:stacks:import</span> sets "
     '<span class="code">--skip-assets-publish</span> automatically, and imported assets '
     'are not published in the same run. When this happens, the command prints a reminder '
     'pointing to the publish command to run once scanning completes:</p><pre>csdx '
     'cm:stacks:bulk-assets --data-dir &lt;BACKUP_DIR&gt; --stack-api-key '
     '&lt;STACK_API_KEY&gt; --operation publish</pre>'),
    # One Limitations bullet. The rest of that list is unrelated and stays.
    ('<li>On stacks where asset scanning is active for the org plan, '
     '<span class="code">cm:stacks:import</span> skips asset publishing automatically. '
     'See <a href="/docs/headless-cms/import-content-using-the-cli#use-of---backup-dir-'
     'flag">Use of --backup-dir Flag</a> for the post-scan publish command.</li>'),
    # The whole Next Steps section: its only item is the asset-scanning page.
    ('<h2>Next Steps</h2><ul><li><a href="/docs/headless-cms/asset-scanning-in-cli">'
     'Asset Scanning in CLI</a>: asset-scan gating behavior during import, including the '
     'automatic <span class="code">--skip-assets-publish</span> trigger and the post-scan '
     'publish command.</li></ul>'),
]

TARGETS = [
    ("Bulk Operations in CLI | V2.x.x", BULK, BULK_FRAGMENTS,
     "docs/json/Version 2.x.x/CLI Commands V2/Bulk Operations in CLI | V2.x.x.json"),
    ("Import Content Using the CLI | V2.x.x", IMPORT, IMPORT_FRAGMENTS,
     "docs/json/Version 2.x.x/CLI Commands V2/Import Content Using the CLI | V2.x.x.json"),
]

# From rollback_beta_asset_scanning.py. --backup-dir and --skip-assets-publish are
# deliberately absent: both predate asset scanning on these pages and would flag
# content that is meant to stay.
MARKERS = ["scan status", "asset scanning", "still scanning", "quarantin",
           "asset-scanning-in-cli", "asset scan"]


def strip(html, fragments, label):
    """Remove every fragment, exactly once each. Exits on any mismatch.

    A fragment given as a tuple is a set of accepted variants: exactly one of them
    must match exactly once.
    """
    removed = []
    for i, fragment in enumerate(fragments, 1):
        variants = fragment if isinstance(fragment, tuple) else (fragment,)
        hits = [v for v in variants if html.count(v) == 1]
        if len(hits) != 1:
            counts = ", ".join(str(html.count(v)) for v in variants)
            sys.exit(f"{label}: fragment {i} matched [{counts}] time(s) across "
                     f"{len(variants)} variant(s), expected exactly one variant to match "
                     f"once.\n  Production content has drifted. First 200 chars of the "
                     f"first variant:\n  {variants[0][:200]}")
        html = html.replace(hits[0], "", 1)
        removed.append(hits[0])
    # Removing a whole section between two rules leaves the rules adjacent, which
    # renders as a double separator. Collapse any run back to one.
    html = re.sub(r"(?:<hr\s*/?>\s*){2,}", "<hr/>", html)
    return html, removed


def write_parked(sections):
    lines = [
        "# V2 asset-scanning passages, parked",
        "",
        "Asset scanning shipped for CLI V1 only. These passages were removed from the "
        "two V2 pages on production so the docs do not describe an unreleased feature.",
        "",
        "Staging and development still serve the versions that contain them "
        "(`blt85d9deae08de968d` v13, `blt1215a1f9bbcc9900` v19), so the live copy is "
        "one publish away. This file exists so restoring them does not depend on "
        "reading an entry version.",
        "",
        "Removed by `scripts/strip_v2_asset_scanning.py`. The fragments below are the "
        "exact HTML that came out, in document order.",
        "",
    ]
    for label, uid, fragments in sections:
        lines += [f"## {label}", "", f"Entry `{uid}`.", ""]
        for i, fragment in enumerate(fragments, 1):
            lines += [f"### Fragment {i}", "", "```html", fragment, "```", ""]
    with open(PARKED, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"\nparked the removed passages in {os.path.relpath(PARKED, ROOT)}")


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    print("LIVE RUN (PUT only, no publish)\n" if confirm
          else "DRY RUN (pass --confirm to write)\n")

    sections = []
    for label, uid, fragments, rel_path in TARGETS:
        entry = get_entry(headers, DOCS_ARTICLE, uid)
        section = article_section(entry)
        before = section["content"]
        url_before = entry.get("url")

        after, removed = strip(before, fragments, label)

        leftover = [m for m in MARKERS if m in after.lower()]
        if leftover:
            sys.exit(f"{label}: asset-scanning markers survive the strip: {leftover}. "
                     f"Refusing to write a partial removal.")

        print(f"{label}  ({uid})  draft v{entry['_version']}")
        print(f"  url        {url_before}  (unchanged)")
        print(f"  content    {len(before)} -> {len(after)} chars "
              f"({len(before) - len(after)} removed across {len(removed)} fragments)")
        sections.append((label, uid, removed))

        if not confirm:
            continue

        section["content"] = after
        updated = put_entry(headers, DOCS_ARTICLE, uid, entry)
        if updated.get("url") != url_before:
            sys.exit(f"{label}: url changed on write, from {url_before!r} to "
                     f"{updated.get('url')!r}. Investigate before continuing.")
        print(f"  wrote v{updated['_version']}, NOT published "
              f"(staging and development stay on v{entry['_version']})")

        # Keep the local mirror in step with what production will serve.
        local_path = os.path.join(ROOT, rel_path)
        with open(local_path, encoding="utf-8") as fh:
            local = json.load(fh)
        article_section(local)["content"] = after
        with open(local_path, "w", encoding="utf-8") as fh:
            json.dump(local, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print(f"  updated {rel_path}")

    if confirm:
        write_parked(sections)
        print("\nNext: python3 scripts/stage_cli_cleanup_releases.py --release B")
    else:
        print("\nDry run complete, no writes made.")
        for label, uid, removed in sections:
            print(f"\n{label}: {len(removed)} fragment(s) would be removed")
            for i, fragment in enumerate(removed, 1):
                preview = fragment[:160].replace("\n", " ")
                print(f"  {i}. {preview}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
