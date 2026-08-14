---
uid: "blt85d9deae08de968d"
seo_title: "Contentstack CLI Bulk | V2.x.x | Contentstack"
seo_description: "Run bulk publish and bulk unpublish operations with the Contentstack CLI for entries and assets across environments and locales at scale with built-in retries."
---

# Bulk Operations in CLI

## Overview

The CLI Bulk Operations plugin streamlines content management workflows by providing robust commands for bulk publishing and unpublishing operations. It intelligently handles API rate limits, retries failed operations, and processes large volumes of content efficiently.

### What Problem Does It Solve?

When managing content at scale in Contentstack, you often need to:

- Publish hundreds or thousands of entries to multiple environments
- Unpublish outdated content across multiple locales
- Handle API rate limits gracefully without manual intervention
- Retry failed operations automatically
- Track operation progress and results

This plugin handles all of these challenges automatically.

---

## Installation

### Prerequisites

- Node.js \>= 22
- Contentstack CLI installed
- Valid Contentstack account with Management Token or API Key

### Install Plugin

```
# Install Contentstack CLI
npm install -g @contentstack/cli

# Verify installation
csdx cm:stacks:bulk-entries --help
```

---

## Quick Start

### Basic Publish Operation

```
# Publish all entries of a content type
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types blog_post \
  --environments production \
  --locales en-us \
  --stack-api-key blt*******

# Publish assets
csdx cm:stacks:bulk-assets \
  --operation publish \
  --environments production \
  --locales en-us \
  --stack-api-key blt*******
```

### Basic Unpublish Operation

```
# Unpublish entries
csdx cm:stacks:bulk-entries \
  --operation unpublish \
  --content-types blog_post \
  --environments staging \
  --locales en-us \
  --stack-api-key blt*******
```

---

## Commands

### Bulk Entries

Perform bulk operations on entries with advanced filtering and publishing options.

#### Syntax

```
csdx cm:stacks:bulk-entries [OPTIONS]
```

#### Required Options

| Flag | Description | Example |
| --- | --- | --- |
| `--operation` | Operation type: `publish` or `unpublish` | `--operation publish` |
| `--environments` | The name of the environment(s) on which entries/assets will be published. In case of multiple environments, specify their names separated by spaces. | `--environments prod staging` |
| `--locales` | Locales in which entries/assets will be published. In case of multiple locales, specify the codes separated by spaces. | `--locales en-us fr-fr` |
| `-k, --stack-api-key` | API key of the source stack. You must use either the --stack-api-key flag or the --alias flag. | `-k blt*********` |
| `-a, --alias` | Alias (name) of the management token. You must use either the --alias flag or the --stack-api-key flag. | `-a my-token` |

#### Entry-Specific Options

| Flag | Description | Default |
| --- | --- | --- |
| `--content-types` | Content type UIDs to perform operation on. If not provided, operates on all content types. | - |
| `--filter` | Filter entries by status: `draft`, `modified`, `unpublished`, `non-localized` | - |
| `--include-variants` | Includes entry variants (alternate versions of a base entry) in the bulk operation. By default, only base entries are processed. | `false` |
| **Filter values:** |  |  |

- `draft` — Entries that have never been published
- `modified` — Entries updated since the last publish
- `unpublished` — Entries that were published earlier but are currently unpublished
- `non-localized` — Entries where non-localized fields have been updated in the master locale, requiring localized entries to be republished

#### General Options

| Flag | Description | Default |
| --- | --- | --- |
| `--publish-mode` | Publish mode: bulk (uses Bulk Publish API) or single (individual API calls) | `bulk` |
| `--branch` | The name of the branch where you want to perform the bulk publish operation. If you don't mention the branch name, then by default the content from main branch will be published. | `main` |
| `--source-env` | Source environment for cross-publish | - |
| `--source-alias` | Alias name for source environment delivery token (required for cross-publish). Add delivery token using: `csdx auth:tokens:add` | - |
| `-y, --yes` | Set it to true to process the command with the current configuration. | `false` |
| `-c, --config` | The path of the optional configuration JSON file containing all the options for a single run. | - |
| `--retry-failed` | Use this option to retry publishing the failed entries/assets from the logfile. | - |
| `--revert` | Revert publish operations from a log folder. | - |
| `--bulk-operation-file` | Folder path to store operation logs. | `bulk-operation` |

#### Examples

**1. Publish all content types to production**

```
csdx cm:stacks:bulk-entries \
  --operation publish \
  --environments production \
  --locales en-us \
  -k blt*******
```

**2. Publish specific content types to multiple environments**

```
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types blog_post,article,page \
  --environments dev,staging,production \
  --locales en-us,es-es \
  -k blt*******
```

**3. Publish entries with non-localized field changes**

```
csdx cm:stacks:bulk-entries \
  --operation publish \
  --filter non-localized \
  --content-types blog_post \
  --environments production \
  -k blt*******
```

**3. Publish only draft entries**

```
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types blog_post \
  --filter draft \
  --environments production \
  --locales en-us \
  -k blt*******
```

**4. Cross-publish from production to staging**

First, add the delivery token for the source environment (one-time setup):

```
# Add delivery token for production environment
csdx auth:tokens:add \
  -a prod-delivery \
  --delivery-token prod-delivery-token \
  --stack-api-key blt******* \
  --environment production \
  --type delivery
```

Then use it for cross-publish:

```
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types blog_post \
  --source-env production \
  --source-alias prod-delivery \
  --environments staging \
  --locales en-us \
  -k blt*******
```

**5. Publish using single mode for fine control**

```
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types blog_post \
  --publish-mode single \
  --environments production \
  --locales en-us \
  -k blt*******
```

**6. Unpublish entries**

```
csdx cm:stacks:bulk-entries \
  --operation unpublish \
  --content-types blog_post \
  --environments staging \
  --locales en-us \
  -k blt*******
```

**7. Retry failed operations**

```
# Retry failed entries from a previous operation
csdx cm:stacks:bulk-entries \
  --retry-failed ./bulk-operation
```

**8. Revert a publish operation**

```
# Revert (unpublish) previously published entries
csdx cm:stacks:bulk-entries \
  --revert ./bulk-operation
```

**9. Publish with entry variants**

```
# Publish entries including their variants
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types blog_post \
  --include-variants \
  --environments production \
  --locales en-us \
  -k blt*******
```

---

### Bulk Assets

Perform bulk operations on assets with folder and file type filtering.

#### Syntax

```
csdx cm:stacks:bulk-assets [OPTIONS]
```

#### Required Options

Same as bulk entries (see above).

#### Asset-Specific Options

| Flag | Description | Example |
| --- | --- | --- |
| `--folder-uid` | The UID of the Assets' folder from which the assets need to be published. Default: cs_root | `--folder-uid cs_root` |
| `--data-dir`, `-d` | Path to exported content folder containing asset publish details. Publishes assets from that folder instead of scanning the live stack. | `--data-dir ./content` |
| `--dry-run` | Preview the publish plan without making any API calls. Default: `false`. Only takes effect when combined with `--data-dir`. It has no effect on the default live-folder-scan publish or unpublish flow. | `--dry-run` |

On stacks where asset scanning applies, `cm:stacks:bulk-assets` prints an "Asset Scan Status" dashboard before publishing. The dashboard reports the total assets found, how many are clean and will publish, how many are still scanning (skipped), and how many are quarantined (skipped). In the `--data-dir` flow, it also reports assets skipped locally for missing publish details and assets skipped for having no mapped UID. If no assets are publishable after this filtering, the command prints a warning and exits without publishing anything.

#### Examples

**1. Publish all assets**

```
csdx cm:stacks:bulk-assets \
  --operation publish \
  --environments production \
  --locales en-us \
  -k blt*******
```

**2. Publish assets from specific folder**

```
csdx cm:stacks:bulk-assets \
  --operation publish \
  --folder-uid cs_product_images \
  --environments production \
  --locales en-us \
  -k blt*******
```

**3. Cross-publish assets from production to staging**

```
csdx cm:stacks:bulk-assets \
  --operation publish \
  --source-env production \
  --source-alias prod-delivery \
  --environments staging \
  --locales en-us \
  -k blt*******
```

*Note: See Example 4 in Bulk Entries section for how to set up the delivery token alias.*

**4. Unpublish assets**

```
csdx cm:stacks:bulk-assets \
  --operation unpublish \
  --environments staging \
  --locales en-us \
  -k blt*******
```

**5. Retry failed asset operations**

```
# Retry failed assets from a previous operation
csdx cm:stacks:bulk-assets \
  --retry-failed ./bulk-operation
```

**6. Revert an asset publish operation**

```
# Revert (unpublish) previously published assets
csdx cm:stacks:bulk-assets \
  --revert ./bulk-operation
```

**7. Publish assets from an exported content folder (data-dir flow)**

```
# Publish assets from a backup or export folder after asset scanning clears
csdx cm:stacks:bulk-assets \
  --data-dir ./content \
  --operation publish \
  -k blt*******
```

Add `--dry-run` to preview which assets would publish without making any API calls. `--dry-run` only affects this `--data-dir` flow. It has no effect on the default publish or unpublish flow shown in examples 1 through 4.

### Bulk CS Assets operations

Perform bulk **delete** or **move** operations on assets stored in cs-assets spaces. This command uses the cs-assets REST API and is separate from the CMA-based Bulk Publish API used by `bulk-entries` and `bulk-assets`.

**Prerequisite**: Your region must have CS Assets enabled. See [Configure Regions](/docs/headless-cms/configure-regions-in-the-cli).

> **Warning:** Do not combine CMS flags (`--stack-api-key`, `--alias`, `--environments`, `--locales`, `--branch`) with the CS Assets flags in the table below. The delete and move operations target the CS Assets API, not the CMS publish pipeline.

#### Syntax

```
csdx cm:stacks:bulk-assets [OPTIONS]
```

#### Options

| Flag | Description | Required |
| --- | --- | --- |
| `--operation` | Operation type: `delete` or `move` | Yes |
| `--space-uid` | UID of the CS Assets space | Yes |
| `--org-uid` | Organization UID | Yes |
| `--asset-uids-file` | Path to a JSON file listing the assets to act on, in the form `{ "uids": ["uid1", "uid2"] }` | Yes |
| `--workspace` | Workspace to operate in. Default: `main` | No |
| `--locale` | Locale to delete assets in. Required for `delete` and not accepted for `move` | For delete |
| `--target-folder-uid` | UID of the destination folder (`move` only) | For move |
| `--folder-uid` | UID of the source folder to filter assets | No |
| `-y, --yes` | Skip confirmation prompt | No |

#### Examples

**Bulk delete assets in a space:**

```
csdx cm:stacks:bulk-assets \
  --operation delete \
  --space-uid blt1234567890abcdef \
  --org-uid bltorg1234567890 \
  --locale en-us \
  --asset-uids-file ./assets.json
```

**Bulk move assets to a different folder:**

```
csdx cm:stacks:bulk-assets \
  --operation move \
  --space-uid blt1234567890abcdef \
  --org-uid bltorg1234567890 \
  --folder-uid cs_source_folder \
  --target-folder-uid cs_destination_folder \
  --asset-uids-file ./assets.json \
  --yes
```

---

### Bulk Taxonomies

Bulk publish or unpublish taxonomy terms. This command has no equivalent in CLI V1.

#### Syntax

```
csdx cm:stacks:bulk-taxonomies [OPTIONS]
```

#### Options

| Flag | Description | Required |
| --- | --- | --- |
| `--operation` | Operation type: `publish` or `unpublish` | Yes |
| `--taxonomies` | UIDs of the taxonomies to act on. Separate multiple UIDs with a space. | Yes |
| `--environments` | Environments to publish to or unpublish from | Yes |
| `--locales` | Locales to act on | Yes |
| `--stack-api-key` | API key of the target stack | Yes, unless `--alias` is used |
| `--alias` | Management token alias of the target stack | Yes, unless `--stack-api-key` is used |
| `-y, --yes` | Skip confirmation prompt | No |

#### Examples

**Publish taxonomy terms to an environment:**

```
csdx cm:stacks:bulk-taxonomies \
  --operation publish \
  --taxonomies product_category \
  --environments production \
  --locales en-us \
  --stack-api-key bltxxxxxx
```

**Unpublish taxonomy terms:**

```
csdx cm:stacks:bulk-taxonomies \
  --operation unpublish \
  --taxonomies product_category region \
  --environments production \
  --locales en-us \
  --alias myalias
```

---

## Operation Modes

### Bulk Mode (Default)

Uses Contentstack's native Bulk Publish APIs.

**Best For:**

- Publishing 100+ entries/assets
- Multi-environment deployments

**Example:**

```
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types blog_post \
  --environments production \
  --locales en-us \
  -k blt*******
```

### Single Mode

Makes individual API calls for each item with intelligent rate limiting.

**Best For:**

- Small batches (less than 50 items)
- Operations requiring detailed error tracking
- Testing and debugging

**Example:**

```
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types blog_post \
  --environments production \
  --locales en-us \
  --publish-mode single \
  -k blt*******
```

---

## Cross-Publish Setup

Cross-publish allows you to promote content from one environment to another (e.g., staging → production). To use cross-publish, you need to set up a delivery token for the source environment.

### Why Delivery Tokens?

Cross-publish uses the **Delivery API** to fetch only published content from the source environment. This ensures you're promoting exactly what's live, not draft content.

### Setting Up Delivery Tokens

**Step 1: Create a Delivery Token in Contentstack**

1. Navigate to **Settings → Tokens → Delivery Tokens** in your Contentstack stack
2. Click **+ Add Delivery Token**
3. Name your token (e.g., "Production Delivery Token")
4. Select the source environment (e.g., "production")
5. Copy the generated delivery token

**Step 2: Add Token to CLI**

```
csdx auth:tokens:add \
  -a <alias-name> \
  --delivery-token <your-delivery-token> \
  --stack-api-key <your-stack-api-key> \
  --environment <source-environment> \
  --type delivery
```

**Example:**

```
# Add production delivery token
csdx auth:tokens:add \
  -a prod-delivery \
  --delivery-token prod-delivery-token \
  --stack-api-key blt******** \
  --environment production \
  --type delivery

# Add staging delivery token  
csdx auth:tokens:add \
  -a staging-delivery \
  --delivery-token stag-delivery-token \
  --stack-api-key blt******** \
  --environment staging \
  --type delivery
```

**Step 3: Use in Cross-Publish Operations**

```
# Promote from staging to production
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types blog_post \
  --source-env staging \
  --source-alias staging-delivery \
  --environments production \
  --locales en-us \
  -k blt********
```

### Managing Delivery Tokens

```
# List all stored tokens (including delivery tokens)
csdx auth:tokens

# Remove a delivery token
csdx auth:tokens:remove -a staging-delivery
```

---

## Use Cases

### Use Case 1: Content Unpublish

**Scenario**: A critical bug is discovered in 500 blog posts that need immediate unpublishing from production.

**Solution**:

```
csdx cm:stacks:bulk-entries \
  --operation unpublish \
  --content-types blog_post \
  --environments production \
  --locales en-us,es-es,fr-fr \
  --yes \
  -k blt********
```

**Result**: All 500 blog posts unpublished across 3 locales in ~2 minutes (bulk mode).

---

### Use Case 2: Scheduled Content Release

**Scenario**: Publish 200 product entries to production every Monday at 9 AM.

**Solution**: Create a cron job with a config file

```
# config.json
{
  "operation": "publish",
  "contentTypes": ["product"],
  "environments": ["production"],
  "locales": ["en-us"],
  "filter": "modified",
  "publishMode": "bulk"
}

# Cron command
0 9 * * 1 csdx cm:stacks:bulk-entries -c /path/to/config.json -k $STACK_API_KEY --yes
```

---

### Use Case 3: Cross-Environment Promotion

**Scenario**: Promote all content published in staging to production.

**Setup** (one-time):

```
# Add delivery token for staging environment
csdx auth:tokens:add \
  -a staging-delivery \
  --delivery-token blt_staging_token \
  --stack-api-key blt******** \
  --environment staging \
  --type delivery
```

**Solution**:

```
# Promote entries
csdx cm:stacks:bulk-entries \
  --operation publish \
  --source-env staging \
  --source-alias staging-delivery \
  --environments production \
  --locales en-us \
  -k blt********

# Promote assets
csdx cm:stacks:bulk-assets \
  --operation publish \
  --source-env staging \
  --source-alias staging-delivery \
  --environments production \
  --locales en-us \
  -k blt********
```

**Result**: All staging content promoted to production with verification.

**How it works**: The `--source-alias` uses a stored delivery token to fetch only published content from the source environment. This ensures you're promoting exactly what's live in staging.

---

### Use Case 4: Selective Publishing with Filters

**Scenario**: Publish only draft entries that have never been published.

**Solution**:

```
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types article,blog_post \
  --filter draft \
  --environments production \
  --locales en-us \
  -k blt********
```

**Result**: Only unpublished entries are sent to production, saving API calls.

---

### Use Case 5: Multi-Locale Product Launch

**Scenario**: Launch 50 new product entries across 10 locales and 3 environments simultaneously.

**Solution**:

```
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types product \
  --environments dev,staging,production \
  --locales en-us,es-es,fr-fr,de-de,it-it,pt-br,ja-jp,zh-cn,ko-kr,ar-ae \
  --publish-mode bulk \
  -k blt********
```

**Result**: 50 products × 10 locales × 3 envs = 1,500 publish operations completed in ~5 minutes via batching.

---

### Use Case 6: Retry Failed Operations

**Scenario**: A network issue caused 20 out of 200 entries to fail publishing.

**Solution**:

```
# Retry only failed entries
csdx cm:stacks:bulk-entries \
  --retry-failed bulk-operation/failed-20250112-143022.json \
  -k blt********
```

**Result**: Only the 20 failed entries are retried, successful ones are skipped.

---

### Use Case 7: Asset Organization by Folder

**Scenario**: Publish only marketing assets in a specific folder.

**Solution**:

```
csdx cm:stacks:bulk-assets \
  --operation publish \
  --folder-uid cs_marketing_2026 \
  --environments production \
  --locales en-us \
  -k blt********
```

**Result**: Only assets in the `cs_marketing_2026` folder are published.

---

### Use Case 8: Rollback Published Content

**Scenario**: After publishing 300 blog entries to production, you discover that some entries contain incorrect information and need to be unpublished immediately.

**Solution**:

```
# Step 1: Revert the publish operation using the operation log
csdx cm:stacks:bulk-entries \
  --revert ./bulk-operation
```

**How it works**:

- The `--revert` flag reads the operation log from the `bulk-operation` folder
- It automatically unpublishes all entries that were published in the last operation
- Restores entries to their previous version before publishing
- Only works with publish operations (cannot revert unpublish operations)

**Result**: All 300 blog entries are unpublished and reverted to their previous version, effectively rolling back the entire operation.

**Important Notes**:

- The `bulk-operation` folder stores detailed logs of the last operation only

- Each new operation overwrites the previous logs

- To preserve logs for audit purposes, copy the folder before running a new operation:

  ```
  cp -r bulk-operation bulk-operation-backup-$(date +%Y%m%d-%H%M%S)
  ```

---

### Use Case 9: Retry Failed Operations After Network Issues

**Scenario**: While publishing 500 product entries to production, a temporary network issue caused 75 entries to fail. You want to retry only the failed entries without re-processing the successful ones.

**Solution**:

```
# Step 1: Check the operation summary to identify failures
# The CLI automatically logs failed operations

# Step 2: Retry only the failed entries
csdx cm:stacks:bulk-entries \
  --retry-failed ./bulk-operation
```

**How it works**:

- The `--retry-failed` flag reads the failed operation logs from the `bulk-operation` folder
- It identifies all entries/assets that failed in the last operation
- Re-attempts the operation only for failed items
- Successful entries are skipped automatically

**Result**: The 75 failed entries are retried and successfully published, while the 425 successful entries are untouched.

**Best Practices**:

1. **Wait before retrying**: If the failure was due to rate limiting or network issues, wait a few minutes before retrying
2. **Check error logs**: Review the error messages in the operation logs to understand the root cause
3. **Fix underlying issues**: If failures are due to invalid data, fix the content before retrying
4. **Monitor retry attempts**: The CLI tracks retry counts and will stop after max retries (default: 5)

**Common Retry Scenarios**:

- Network timeouts or connection issues
- Temporary API rate limit errors (429)
- Server errors (5xx responses)
- Transient infrastructure issues

**Non-retryable Scenarios** (require manual intervention):

- Invalid content type UIDs (404)
- Missing required fields in entries
- Permission errors (403)
- Invalid API credentials (401)

---

### Use Case 10: Automated Retry with Custom Configuration

**Scenario**: You have a CI/CD pipeline that publishes content, and you want to automatically retry failures with custom retry logic.

**Solution**:

```
# config.json
{
  "operation": "publish",
  "contentTypes": ["product", "article"],
  "environments": ["production"],
  "locales": ["en-us", "es-es"],
  "publishMode": "bulk",
  "maxRetries": 3,
  "retryDelay": 5000,
  "rateLimit": {
    "requestsPerSecond": 10,
    "maxConcurrent": 3
  }
}

# Initial publish attempt
csdx cm:stacks:bulk-entries -c config.json -k blt******** --yes

# If failures occur, automatically retry after 30 seconds
sleep 30
csdx cm:stacks:bulk-entries --retry-failed ./bulk-operation  --yes
```

**Configuration Options**:

- `maxRetries`: Maximum retry attempts per item (default: 5)
- `retryDelay`: Delay in milliseconds between retries (default: 1000)
- `rateLimit.requestsPerSecond`: API request rate limit (default: 15)
- `rateLimit.maxConcurrent`: Maximum concurrent operations (default: 5)

**Result**: Failed operations are automatically retried with controlled rate limiting, making the process resilient to transient failures.

---

### Use Case 11: Safe Multi-Stage Deployment with Rollback

**Scenario**: Deploy content to staging for testing, and if approved, promote to production. If issues are found in production, quickly rollback.

**Solution**:

```
# Step 1: Publish to staging
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types blog_post,article \
  --environments staging \
  --locales en-us \
  -k blt********

# Backup the operation logs
cp -r bulk-operation bulk-operation-staging-$(date +%Y%m%d-%H%M%S)

# Step 2: After testing, promote to production
csdx cm:stacks:bulk-entries \
  --operation publish \
  --content-types blog_post,article \
  --environments production \
  --locales en-us \
  -k blt********

# Backup production operation logs
cp -r bulk-operation bulk-operation-production-$(date +%Y%m%d-%H%M%S)

# Step 3: If issues found, rollback production
csdx cm:stacks:bulk-entries \
  --revert ./bulk-operation-production-YYYYMMDD-HHMMSS
```

**Result**: Content is safely deployed with the ability to quickly rollback production while preserving staging state.

---

## Content Filters

The CLI supports various filters to target specific entries based on their status and content state:

### Non-Localized Filter

The `non-localized` filter identifies entries where non-localized fields have been updated in the master locale, requiring localized entries to be republished to maintain consistency.

**How it works:**

1. Fetches all available locales from your stack
2. Determines the master locale (first locale in the stack)
3. For each entry, compares non-localized field values between the master locale and all other locales
4. Returns entries where non-localized fields differ between locales

**Use Case:** When you update a non-localized field (like a status, category, or global setting) in the master locale, all localized versions of that entry should be republished to reflect the change.

**Example:**

```
# Publish entries where non-localized fields have been updated
csdx cm:stacks:bulk-entries \
  --operation publish \
  --filter non-localized \
  --content-types product \
  --environments production \
  -k blt*******
```

> **Note:** This filter automatically discovers all locales in your stack and doesn't require specifying the `--locales` flag.

---

## Configuration

### Using Config Files

Instead of passing flags, use a JSON configuration file:

```
csdx cm:stacks:bulk-entries -c my-config.json -k blt********
```

**Example Config File:**

```
{
  "operation": "publish",
  "contentTypes": ["blog_post", "article"],
  "environments": ["production", "staging"],
  "locales": ["en-us", "es-es"],
  "filter": "draft",
  "publishMode": "bulk",
  "branch": "main",
  "rateLimit": {
    "requestsPerSecond": 15,
    "maxConcurrent": 5
  },
  "maxRetries": 3
}
```

---

## Troubleshooting

### Problem: 429 Rate Limit Errors

**Solution**: The adaptive rate limiter should prevent this, but if it occurs:

1. Reduce `requestsPerSecond` in config
2. Reduce `maxConcurrent` in config
3. Use `--publish-mode single` for better control

### Problem: Operations Timing Out

**Solution**:

1. Check batch sizes - reduce if too large
2. Increase `maxPolls` in config (default: 300)
3. Check network connectivity

### Problem: Failed Items Not Retrying

**Solution**:

1. Check `maxRetries` config (default: 5)
2. Review error logs for non-retryable errors
3. Manually retry using `--retry-failed`

### Problem: Memory Issues with Large Operations

**Solution**:

1. Process content types separately
2. Use filtering to reduce item count
3. Increase Node.js heap size: `NODE_OPTIONS=--max-old-space-size=4096`

### Problem: Invalid Configuration

**Error**: `Invalid configuration: errors`

**Solution**: Validate your config file or flags:

- Ensure required flags are present
- Check locale/environment codes are valid
- Verify content type UIDs exist

### Problem: Cross-Publish Requires --source-alias

**Error**: `Cross-publish requires --source-alias flag with a delivery token`

**Solution**:

1. Create a delivery token in Contentstack (Settings → Tokens → Delivery Tokens)
2. Add it to CLI using:

```
csdx auth:tokens:add \
  -a <alias-name> \
  --delivery-token <token> \
  --stack-api-key <api-key> \
  --environment <source-env> \
  --type delivery
```

1. Use the alias in your command with `--source-alias <alias-name>`

### Problem: Source Alias Not Found

**Error**: `No token found for alias 'staging-delivery'`

**Solution**:

1. List your stored tokens: `csdx auth:tokens`
2. Add the missing delivery token (see above)
3. Verify the alias name matches exactly

### Problem: Source Alias Invalid Type

**Error**: `Alias 'my-token' is not a delivery token (type: management)`

**Solution**: You're using a management token alias instead of a delivery token. Cross-publish requires a delivery token:

1. Add a delivery token with `--type delivery` flag
2. Use the delivery token alias with `--source-alias`

### Assets stay in "still scanning" status with no automatic retry

**Root Cause(s)**: `cm:stacks:bulk-assets` checks each asset's scan status once at command run time. There is no polling loop that waits for a pending scan to finish before deciding whether to publish. An asset in the scan queue at the time the command runs is skipped for that run.

**Resolution**: Wait for the asset's scan to complete, then run the same `cm:stacks:bulk-assets` command again. The command rechecks scan status on every run.

### "Asset UID mapper is empty" warning during a `--data-dir` publish

**Root Cause(s)**: The `mapper/assets/uid-mapping.json` file in the data directory is missing or contains no entries. This file maps source asset UIDs to their UIDs on the destination stack. Unlike a missing `assets.json`, a missing or empty UID mapping file does not stop the command. It logs this warning and continues, and every asset in the run is then skipped because none can be mapped to a destination UID.

**Resolution**: Confirm the data directory points at a completed import backup and that `mapper/assets/uid-mapping.json` exists and is populated. Re-run the import if the mapping file was not generated.

### Environment names show as raw UIDs instead of names in a `--data-dir` publish

**Root Cause(s)**: The `environments/environments.json` file in the data directory is missing. Asset scanning falls back to using raw environment UIDs in place of names for output, and continues processing. This is a warning, not a failure.

**Resolution**: Confirm the data directory contains `environments/environments.json` from the same import backup. If it is missing, re-export or re-import to regenerate it.

---

## Limitations

- `--retry-failed` on `cm:stacks:bulk-assets` rebuilds its item list from the failed-operation log only. It does not recheck asset scan status before retrying, so an asset that entered quarantine after the original run can still be retried.
- The retry mechanism for assets still in the scan queue only checks scan status once per command invocation. See [Assets stay in "still scanning" status with no automatic retry](#assets-stay-in-still-scanning-status-with-no-automatic-retry) for details and the workaround.
- In the `--data-dir` publish flow, a missing `assets.json` in the data directory stops the command with an error. A missing `mapper/assets/uid-mapping.json` or `environments/environments.json` only logs a warning and the command continues with degraded behavior (all assets skipped, or environment names shown as raw UIDs).

## Next Steps

- [Asset Scanning in CLI](/docs/headless-cms/asset-scanning-in-cli): full reference for asset-scan gating behavior, the scan status dashboard, and troubleshooting for `cm:stacks:bulk-assets`.

---

## Best Practices

### 1. Test in Lower Environments First

Always test bulk operations in dev/staging before production:

```
# Test in dev first
csdx cm:stacks:bulk-entries --operation publish --environments dev ...

# Then staging
csdx cm:stacks:bulk-entries --operation publish --environments staging ...

# Finally production
csdx cm:stacks:bulk-entries --operation publish --environments production ...
```

### 2. Use Config Files for Complex Operations

For operations with many flags, use config files for repeatability and version control.

### 3. Monitor Rate Limiter Logs

Pay attention to rate limiter messages to understand system behavior.

### 4. Start with Bulk Mode

Use bulk mode by default for efficiency, switch to single mode only when needed.

### 5. Keep Log Files

Save log files for auditing and potential rollback:

```
cp -r bulk-operation bulk-operation-backup-$(date +%Y%m%d)
```

### 6. Use Filters to Reduce Load

Apply filters to publish only necessary content:

```
--filter draft  # Only unpublished entries
--filter modified  # Only entries modified since last publish
```

### 7. Batch Similar Operations

Group operations by content type, environment, or locale for better performance.

---
