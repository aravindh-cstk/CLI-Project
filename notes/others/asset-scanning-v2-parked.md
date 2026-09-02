# V2 asset-scanning passages, parked

Asset scanning shipped for CLI V1 only. These passages were removed from the two V2 pages on production so the docs do not describe an unreleased feature.

Staging and development still serve the versions that contain them (`blt85d9deae08de968d` v13, `blt1215a1f9bbcc9900` v19), so the live copy is one publish away. This file exists so restoring them does not depend on reading an entry version.

Removed by `scripts/strip_v2_asset_scanning.py`. The fragments below are the exact HTML that came out, in document order.

## Bulk Operations in CLI | V2.x.x

Entry `blt85d9deae08de968d`.

### Fragment 1

```html
<tr><td><span class="code">--data-dir</span>, <span class="code">-d</span></td><td>Path to exported content folder containing asset publish details. Publishes assets from that folder instead of scanning the live stack.</td><td><span class="code">--data-dir ./content</span></td></tr>
```

### Fragment 2

```html
<tr><td><span class="code">--dry-run</span></td><td>Preview the publish plan without making any API calls. Default: <span class="code">false</span>. Only takes effect when combined with <span class="code">--data-dir</span>. It has no effect on the default live-folder-scan publish or unpublish flow.</td><td><span class="code">--dry-run</span></td></tr>
```

### Fragment 3

```html
<p>On stacks where asset scanning applies, <span class="code">cm:stacks:bulk-assets</span> prints an "Asset Scan Status" dashboard before publishing. The dashboard reports the total assets found, how many are clean and will publish, how many are still scanning (skipped), and how many are quarantined (skipped). In the <span class="code">--data-dir</span> flow, it also reports assets skipped locally for missing publish details and assets skipped for having no mapped UID. If no assets are publishable after this filtering, the command prints a warning and exits without publishing anything.</p>
```

### Fragment 4

```html
<p><strong>7. Publish assets from an exported content folder (data-dir flow)</strong></p><pre># Publish assets from a backup or export folder after asset scanning clears
csdx cm:stacks:bulk-assets \
  --data-dir ./content \
  --operation publish \
  -k blt*******
</pre><p>Add <span class="code">--dry-run</span> to preview which assets would publish without making any API calls. <span class="code">--dry-run</span> only affects this <span class="code">--data-dir</span> flow. It has no effect on the default publish or unpublish flow shown in examples 1 through 4.</p>
```

### Fragment 5

```html
<h3 id="assets-stay-in-still-scanning-status-with-no-automatic-retry">Assets stay in "still scanning" status with no automatic retry</h3><p><strong>Root Cause(s)</strong>: <span class="code">cm:stacks:bulk-assets</span> checks each asset's scan status once at command run time. There is no polling loop that waits for a pending scan to finish before deciding whether to publish. An asset in the scan queue at the time the command runs is skipped for that run.</p><p><strong>Resolution</strong>: Wait for the asset's scan to complete, then run the same <span class="code">cm:stacks:bulk-assets</span> command again. The command rechecks scan status on every run.</p>
```

### Fragment 6

```html
<h3 id="asset-uid-mapper-is-empty-warning-during-a-data-dir-publish">"Asset UID mapper is empty" warning during a <span class="code">--data-dir</span> publish</h3><p><strong>Root Cause(s)</strong>: The <span class="code">mapper/assets/uid-mapping.json</span> file in the data directory is missing or contains no entries. This file maps source asset UIDs to their UIDs on the destination stack. Unlike a missing <span class="code">assets.json</span>, a missing or empty UID mapping file does not stop the command. It logs this warning and continues, and every asset in the run is then skipped because none can be mapped to a destination UID.</p><p><strong>Resolution</strong>: Confirm the data directory points at a completed import backup and that <span class="code">mapper/assets/uid-mapping.json</span> exists and is populated. Re-run the import if the mapping file was not generated.</p>
```

### Fragment 7

```html
<h3 id="environment-names-show-as-raw-uids-instead-of-names-in-a-data-dir-publish">Environment names show as raw UIDs instead of names in a <span class="code">--data-dir</span> publish</h3><p><strong>Root Cause(s)</strong>: The <span class="code">environments/environments.json</span> file in the data directory is missing. Asset scanning falls back to using raw environment UIDs in place of names for output, and continues processing. This is a warning, not a failure.</p><p><strong>Resolution</strong>: Confirm the data directory contains <span class="code">environments/environments.json</span> from the same import backup. If it is missing, re-export or re-import to regenerate it.</p>
```

### Fragment 8

```html
<h2 id="limitations">Limitations</h2><ul><li><span class="code">--retry-failed</span> on <span class="code">cm:stacks:bulk-assets</span> rebuilds its item list from the failed-operation log only. It does not recheck asset scan status before retrying, so an asset that entered quarantine after the original run can still be retried.</li><li>The retry mechanism for assets still in the scan queue only checks scan status once per command invocation. See <a href="#assets-stay-in-still-scanning-status-with-no-automatic-retry">Assets stay in "still scanning" status with no automatic retry</a> for details and the workaround.</li><li>In the <span class="code">--data-dir</span> publish flow, a missing <span class="code">assets.json</span> in the data directory stops the command with an error. A missing <span class="code">mapper/assets/uid-mapping.json</span> or <span class="code">environments/environments.json</span> only logs a warning and the command continues with degraded behavior (all assets skipped, or environment names shown as raw UIDs).</li></ul>
```

### Fragment 9

```html
<h2 id="next-steps">Next Steps</h2><ul><li>Asset Scanning in CLI: full reference for asset-scan gating behavior, the scan status dashboard, and troubleshooting for <span class="code">cm:stacks:bulk-assets</span>.</li></ul>
```

## Import Content Using the CLI | V2.x.x

Entry `blt1215a1f9bbcc9900`.

### Fragment 1

```html
<p>Asset scanning is rolling out as an org-plan feature. Once it is active for a stack's org plan, <span class="code">cm:stacks:import</span> sets <span class="code">--skip-assets-publish</span> automatically, and imported assets are not published in the same run. When this happens, the command prints a reminder pointing to the publish command to run once scanning completes:</p><pre>csdx cm:stacks:bulk-assets --data-dir &lt;BACKUP_DIR&gt; --stack-api-key &lt;STACK_API_KEY&gt; --operation publish</pre>
```

### Fragment 2

```html
<li>On stacks where asset scanning is active for the org plan, <span class="code">cm:stacks:import</span> skips asset publishing automatically. See <a href="/docs/headless-cms/import-content-using-the-cli#use-of---backup-dir-flag">Use of --backup-dir Flag</a> for the post-scan publish command.</li>
```

### Fragment 3

```html
<h2>Next Steps</h2><ul><li><a href="/docs/headless-cms/asset-scanning-in-cli">Asset Scanning in CLI</a>: asset-scan gating behavior during import, including the automatic <span class="code">--skip-assets-publish</span> trigger and the post-scan publish command.</li></ul>
```
