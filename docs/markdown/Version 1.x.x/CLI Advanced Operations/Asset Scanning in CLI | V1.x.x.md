---
uid: "blt6ee109a7b3725e1c"
seo_title: "Asset Scanning in CLI | V1.x.x | Contentstack"
seo_description: "Learn how asset scanning gates publishing in the Contentstack CLI for cm:assets:publish and cm:stacks:import, including prerequisites, troubleshooting, and known limitations."
---

# Asset Scanning in CLI

## Overview

Asset scanning checks each asset for a scan status before it is published, and holds back assets that are still being scanned or that fail the scan. It affects the `cm:assets:publish` and `cm:stacks:import` commands.

## Prerequisites

- The `assetsScan` org-plan feature enabled for the stack’s organization.
- [Authenticated](/docs/headless-cms/cli-authentication) in the CLI, with a [configured management token](/docs/headless-cms/cli-authentication#add-management-token) (`--alias`) or a stack API key (`--stack-api-key`). If you haven’t set this up, refer to the [CLI Authentication](/docs/headless-cms/cli-authentication) document.

## Publishing With Scan-Gating

The `cm:assets:publish` command checks each asset’s scan status before publishing it when the stack has asset scanning enabled.

```
csdx cm:assets:publish --backup-dir <BACKUP_DIR> --stack-api-key <STACK_API_KEY>
```

| Flag | Type | Required | Default | Description | Notes |
| --- | --- | --- | --- | --- | --- |
| `--backup-dir=<BACKUP_DIR>` | string | Optional | - | Path to the import backup directory. When set, each imported asset is published only to the environments and locales it was published to in the source stack, read from the backup’s publish details and asset UID mapping. | Exclusive with `--source-env`, `--folder-uid`, `--environments`, and `--locales`. Use this option for the post-import publish flow described in [Import Content Using the CLI](/docs/headless-cms/import-content-using-the-cli). |
| `--retry-failed=<LOGFILE>` | string | Optional | - | Replays failed publish calls from a logfile. | Bypasses asset-scan status checks entirely. |

**Asset Scan Skip Behavior:** Quarantined assets are skipped permanently. Assets still in the scan queue (pending) are skipped until scanning completes and the command runs again. `--retry-failed` bypasses the scan-status check, so it can retry either one immediately.

## Import-Time Behavior

During `cm:stacks:import`, asset publishing is skipped in the same run when `--skip-assets-publish` is passed explicitly, or automatically when the org plan has asset scanning enabled (see [Limitations](#limitations) for rollout status).

When this happens, assets are imported but remain unpublished, and a reminder is printed at the end of the import pointing to the command above:

```
csdx cm:assets:publish --backup-dir <BACKUP_DIR> --stack-api-key <STACK_API_KEY>
```

## Troubleshooting

### Assets remain unpublished after `cm:assets:publish --backup-dir`

**Root Cause**: Asset scanning found the asset still in the scan queue at the time the command ran. The retry mechanism for in-queue assets is disabled in this release, so the asset is skipped immediately instead of being retried.

**Resolution**: Wait for the asset’s scan to complete, then run `cm:assets:publish --backup-dir <BACKUP_DIR>` again.

### `csdx cm:assets:publish --data-dir ...` reports an unrecognized flag

**Root Cause**: A message printed at the end of asset import (from `cm:stacks:import`) tells you to run `csdx cm:assets:publish --data-dir <BACKUP_DIR> ...` to publish assets after scanning. `cm:assets:publish` does not have a `--data-dir` flag.

**Resolution**: Use `--backup-dir` instead: `csdx cm:assets:publish --backup-dir <BACKUP_DIR> --stack-api-key <STACK_API_KEY>`.

### Import prints an asset-scanning message but the org does not have asset scanning enabled

**Root Causes**:

- The reminder is printed whenever assets were imported and `skipAssetsPublish` is set, whether it was set automatically by asset scanning or manually via `--skip-assets-publish`.
- The message text does not distinguish between the two triggers.

**Resolution**: Check whether `--skip-assets-publish` was passed explicitly. If it was, the message is unrelated to asset scanning and assets can be published normally with `csdx cm:assets:publish --backup-dir <BACKUP_DIR> --stack-api-key <STACK_API_KEY>` at any time.

## Limitations

- `cm:assets:publish` does not retry assets that are still in the scan queue within a single run. See [Assets remain unpublished after cm:assets:publish --backup-dir](#assets-remain-unpublished-after) for the resolution.
- Asset scanning does not apply to CS Assets (space-based) stacks. See [CLI for CS Assets](/docs/headless-cms/cli-for-cs-assets) for the separate space-based asset flow.

## Next Steps

- [Bulk Publish and Unpublish Content](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1): full reference for `cm:assets:publish`, including flags not specific to asset scanning.
- [Import Content Using the CLI](/docs/headless-cms/import-content-using-the-cli#use-of---backup-dir-flag): full reference for `cm:stacks:import`, including the `--backup-dir` flag used in the post-scan publish flow.
- [CLI Limitations](/docs/headless-cms/cli-limitations#bulk-publishunpublish-limitations): the broader limitations catalog this content is also mirrored into.
- [Audit Plugin](/docs/headless-cms/cli-audit-plugin): a related but distinct check. `cm:stacks:audit` validates the structural completeness of publish details, it does not check scan or quarantine status.
