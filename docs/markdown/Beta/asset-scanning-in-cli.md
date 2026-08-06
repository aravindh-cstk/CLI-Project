---
uid: "<TO BE ASSIGNED>"
seo_title: "Asset Scanning in CLI | V2.x.x | Contentstack"
seo_description: "Learn how asset scanning gates publishing in the Contentstack CLI V2.x.x Beta for cm:stacks:bulk-assets and cm:stacks:import, including prerequisites, troubleshooting, and known limitations."
---

# Asset Scanning in CLI | V2.x.x Beta

Asset scanning checks each asset for a scan status before it is published, and holds back assets that are still being scanned or that are quarantined. It affects the `cm:stacks:bulk-assets` and `cm:stacks:import` commands.

## Prerequisites

- The `assetsScan` org-plan feature enabled for the stack’s organization.
- [Authenticated](/docs/headless-cms/cli-authentication) in the CLI, with a [configured management token](/docs/headless-cms/cli-authentication#add-management-token) (`--alias`) or a stack API key (`--stack-api-key`). If you haven’t set this up, refer to the [CLI Authentication](/docs/headless-cms/cli-authentication) document.

## Bulk Publish With Scan-Gating

On stacks where asset scanning applies, `cm:stacks:bulk-assets` checks each asset’s scan status before publishing it.

```
csdx cm:stacks:bulk-assets --data-dir <BACKUP_DIR> --operation publish --stack-api-key <STACK_API_KEY>
```

| Flag | Required | Description | Notes |
| --- | --- | --- | --- |
| `--data-dir`, `-d` | Optional | Path to exported content folder containing asset publish details. Publishes assets from that folder instead of scanning the live stack. | - |
| `--dry-run` | Optional | Preview the publish plan without making any API calls. Default: `false`. | Only takes effect when combined with `--data-dir`. Has no effect on the default live-folder-scan publish or unpublish flow. |
| `--retry-failed` | Optional | Rebuilds its item list from the failed-operation log only. | Does not recheck asset scan status before retrying, so an asset that entered quarantine after the original run can still be retried. |

`cm:stacks:bulk-assets` prints an "Asset Scan Status" dashboard before publishing. In the `--data-dir` flow, it also reports assets skipped for missing publish details or an unmapped UID. If no assets are publishable after this filtering, the command prints a warning and exits without publishing anything.

The following is an illustrative example of the dashboard output, not a captured terminal session:

```
Asset Scan Status
──────────────────────────────────────────
Total assets found                    120
──────────────────────────────────────────
Clean (will publish)                  100
Still scanning (skipped)               15
Quarantined (skipped)                   5
──────────────────────────────────────────
Will publish                          100
```

**Scan Queue Retry Behavior:** An asset in the scan queue at run time is skipped for that run, and can be retried by running the command again once scanning completes.

## Import-Time Behavior

During `cm:stacks:import`, asset publishing is skipped in the same run when `--skip-assets-publish` is passed explicitly, or automatically when the org plan has asset scanning enabled (see [Limitations](#limitations) for rollout status).

When this happens, the command prints a reminder pointing to the publish command to run once scanning completes:

```
csdx cm:stacks:bulk-assets --data-dir <BACKUP_DIR> --stack-api-key <STACK_API_KEY> --operation publish
```

## Troubleshooting

### Assets stay in "still scanning" status with no automatic retry

**Root Cause**: `cm:stacks:bulk-assets` checks each asset’s scan status once at command run time. An asset in the scan queue at that time is skipped for that run.

**Resolution**: Wait for the asset’s scan to complete, then run the same `cm:stacks:bulk-assets` command again.

### "Asset UID mapper is empty" warning during a `--data-dir` publish

**Root Cause**: The `mapper/assets/uid-mapping.json` file in the data directory is missing or contains no entries. This file maps source asset UIDs to their UIDs on the destination stack. Unlike a missing `assets.json`, a missing or empty UID mapping file does not stop the command. It logs this warning and continues, and every asset in the run is then skipped because none can be mapped to a destination UID.

**Resolution**: Confirm the data directory points at a completed import backup and that `mapper/assets/uid-mapping.json` exists and is populated. Re-run the import if the mapping file was not generated.

### Environment names show as raw UIDs instead of names in a `--data-dir` publish

**Root Cause**: The `environments/environments.json` file in the data directory is missing. Asset scanning falls back to using raw environment UIDs in place of names for output, and continues processing. This is a warning, not a failure.

**Resolution**: Confirm the data directory contains `environments/environments.json` from the same import backup. If it is missing, re-export or re-import to regenerate it.

## Limitations

- `--retry-failed` does not recheck asset scan status before retrying. See the flag table above for details.
- The retry mechanism for assets still in the scan queue only checks scan status once per command invocation. See [Assets stay in "still scanning" status with no automatic retry](#assets-stay-in-still-scanning-status-with-no-automatic-retry) for details and the workaround.
- In the `--data-dir` publish flow, a missing `assets.json` in the data directory stops the command with an error. A missing `mapper/assets/uid-mapping.json` or `environments/environments.json` only logs a warning and the command continues with degraded behavior (all assets skipped, or environment names shown as raw UIDs).
- Org-plan auto-detection of asset scanning is rolling out and had not yet shipped to every account at the time of writing.
- Asset scanning does not apply to CS Assets (space-based) stacks. See [CLI for CS Assets](/docs/headless-cms/cli-for-cs-assets/v1) for the separate space-based asset flow.

## Next Steps

- [Bulk Operations in CLI](/docs/headless-cms/bulk-operations-in-cli#bulk-assets): full reference for `cm:stacks:bulk-assets`, including flags not specific to asset scanning.
- [Import Content Using the CLI](/docs/headless-cms/import-content-using-the-cli#use-of---backup-dir-flag): full reference for `cm:stacks:import`, including the `--backup-dir`/`--data-dir` flags used in the post-scan publish flow.
