---
uid: "bltc7c58ab7c7d76974"
seo_title: "Contentstack CLI Configuration Reference | Contentstack"
seo_description: "Configure Contentstack CLI export, import, audit, and migration with clear precedence rules, env vars, and module overrides for automation in CI/CD pipelines."
---

# Contentstack CLI Configuration Reference

This document provides a comprehensive reference for all configuration options available across Contentstack CLI plugins.

---

## Quick Start

## Environment Variables

The CLI supports several environment variables that can be used to configure behavior without modifying configuration files.

### CLI Configuration Environment Variables

| Variable | Type | Default | Description |
| --- | --- | --- | --- |
| `CS_CLI_CONFIG_PATH` | `string` | - | Custom path for CLI configuration directory |
| `CS_CLI_LOG_PATH` | `string` | `process.cwd()` | Custom path for CLI log files |
| `CONFIG_NAME` | `string` | `contentstack_cli` | Name of the configuration file |
| `ENC_CONFIG_NAME` | `string` | `contentstack_cli_obfuscate` | Name of the encrypted configuration file |
| `ENC_KEY` | `string` | `encryptionKey` | Encryption key for configuration files |
| `ENCRYPT_CONF` | `boolean` | `true` | Enable/disable configuration encryption |

### Usage Examples

**Set custom log path:**

```
export CS_CLI_LOG_PATH="/path/to/logs"
csdx cm:stacks:export
```

**Disable configuration encryption:**

```
export ENCRYPT_CONF=false
csdx cm:stacks:import
```

**Use custom config directory:**

```
export CS_CLI_CONFIG_PATH="/path/to/config"
csdx cm:stacks:export
```

> **Note:** Environment variables take precedence over configuration file settings and defaults.

---

## Configuration Precedence

When the same configuration key exists at both the root level and module level, the CLI follows a specific precedence order.

### Precedence Order

1. **Module-specific configuration** (highest priority)
2. **Root-level configuration**
3. **Default values** (lowest priority)

### How It Works

The CLI uses a recursive merge strategy (`merge.recursive()`) when loading configuration files. This means:

- **Module config overrides root config**: If a key exists in both `modules.<module-name>.<key>` and root-level `<key>`, the module-specific value is used.
- **Root config is fallback**: If a key doesn't exist in module config, the root-level value is used.
- **Defaults are last resort**: If neither module nor root config has the key, default values are used.

### Examples

#### Import Configuration Precedence

**Example 1:** `importConcurrency` **for Entries Module**

```
{
  "importConcurrency": 5,
  "modules": {
    "entries": {
      "importConcurrency": 10
    }
  }
}
```

**Result:** Entries module uses `importConcurrency: 10` (module config), while other modules use `importConcurrency: 5` (root config).

**Code Reference:** See [entries.ts](https://github.com/contentstack/cli/blob/db01c8a991988e6546e4188ffe3f6693048c7a89/packages/contentstack-import/src/import/modules/entries.ts#L95) in the CLI repository.

**Example 2:** `writeConcurrency` **for Content Types Module**

```
{
  "writeConcurrency": 5,
  "modules": {
    "content-types": {
      "writeConcurrency": 8
    }
  }
}
```

**Result:** Content Types module uses `writeConcurrency: 8` (module config), while other modules use `writeConcurrency: 5` (root config).

**Code Reference:** See [content-types.ts](https://github.com/contentstack/cli/blob/db01c8a991988e6546e4188ffe3f6693048c7a89/packages/contentstack-import/src/import/modules/content-types.ts#L63) in the CLI repository.

#### Export Configuration Precedence

**Example 3:** `chunkFileSize` **for Entries Module**

```
{
  "modules": {
    "entries": {
      "chunkFileSize": 20
    }
  }
}
```

**Result:** Entries module uses `chunkFileSize: 20` (module config). If not specified, it defaults to `10` (FsUtility default).

**Example 4:** `fetchConcurrency` **for Assets Module**

```
{
  "fetchConcurrency": 5,
  "modules": {
    "assets": {
      "fetchConcurrency": 10
    }
  }
}
```

**Result:** Assets module uses `fetchConcurrency: 10` (module config), while other modules use `fetchConcurrency: 5` (root config).

### Common Keys with Precedence

The following keys can be set at both root and module levels:

**Import:**

- `importConcurrency` → `modules.entries.importConcurrency`
- `fetchConcurrency` → `modules.<module>.fetchConcurrency`
- `writeConcurrency` → `modules.<module>.writeConcurrency`
- `chunkFileSize` → `modules.entries.chunkFileSize`

**Export:**

- `fetchConcurrency` → `modules.<module>.fetchConcurrency`
- `writeConcurrency` → `modules.<module>.writeConcurrency`
- `chunkFileSize` → `modules.entries.chunkFileSize`
- `limit` → `modules.<module>.limit`
- `batchLimit` → `modules.<module>.batchLimit`

### Best Practices

1. **Use root-level config for global settings**: Set common values at the root level to apply across all modules.
2. **Override per module when needed**: Use module-specific config to customize behavior for specific modules.
3. **Avoid duplication**: Don't repeat root-level values in module config unless you need different values.

**Example - Recommended Pattern:**

```
{
  "fetchConcurrency": 5,
  "writeConcurrency": 5,
  "modules": {
    "entries": {
      "importConcurrency": 10,
      "chunkFileSize": 20
    },
    "assets": {
      "fetchConcurrency": 10
    }
  }
}
```

In this example:

- Most modules use `fetchConcurrency: 5` and `writeConcurrency: 5` from root
- Entries module uses `importConcurrency: 10` and `chunkFileSize: 20` (module-specific)
- Assets module uses `fetchConcurrency: 10` (overrides root)

---

## Export Configuration

**Command:** `csdx cm:stacks:export`

**Default Configuration:** See the [default export configuration file](https://github.com/contentstack/cli/blob/db01c8a991988e6546e4188ffe3f6693048c7a89/packages/contentstack-export/src/config/index.ts) in the CLI repository.

### Basic Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `host` | `string` | `"https://api.contentstack.io/v3"` | No | Base URL for Content Management API |
| `preserveStackVersion` | `boolean` | `false` | No | Preserve stack version information |
| `source_stack` | `string` | - | Yes\* | API key of source stack |
| `data` | `string` | - | Yes\* | Path to export directory |
| `exportDir` | `string` | - | No | Alias for `data` |

\*Required unless using CLI flags or management token alias

### Path & Directory Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `cliLogsPath` | `string` | - | No | Custom path for CLI logs |
| `branchName` | `string` | - | No | Branch name to export from |
| `branchAlias` | `string` | - | No | Branch alias to export from |

### Content Filtering

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `moduleName` | `string` | - | No | Specific module to export |
| `contentTypes` | `string[]` | - | No | Array of content type UIDs |
| `filteredModules` | `string[]` | - | No | Array of module names to filter |
| `query` | `object\|string` | - | No | Query object or file path for filtering |

### Performance Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `fetchConcurrency` | `number` | `5` | No | Number of parallel fetch operations |
| `writeConcurrency` | `number` | `5` | No | Number of parallel write operations |
| `delayMs` | `number` | - | No | Delay in milliseconds between requests |
| `maxContentLength` | `number` | `100000000` | No | Max content length in bytes (100 MB) |
| `maxBodyLength` | `number` | `100000000` | No | Max body length in bytes (100 MB) |

### Feature Flags

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `securedAssets` | `boolean` | `false` | No | Export secured assets |
| `personalizationEnabled` | `boolean` | `false` | No | Enable personalization features |
| `skipStackSettings` | `boolean` | `false` | No | Skip exporting stack settings (not in default config, but supported) |
| `skipDependencies` | `boolean` | `false` | No | Skip dependency resolution (not in default config, but supported) |

### Authentication

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `email` | `string` | - | No | Email for basic authentication |
| `password` | `string` | - | No | Password for basic authentication |

> **Note:** Use the `--alias` flag to specify a management token alias instead of providing credentials directly in the configuration file.

### Advanced Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `master_locale` | `object` | - | No | Master locale configuration |
| `developerHubBaseUrl` | `string` | - | No | Base URL for Developer Hub API |
| `marketplaceAppEncryptionKey` | `string` | `"nF2ejRQcTv"` | No | Encryption key for Marketplace apps |

### Configuration Precedence Note

**Important:** When the same configuration key exists at both root level and module level, **module-specific configuration takes precedence**. For example, if you set `fetchConcurrency: 5` at root and `modules.assets.fetchConcurrency: 10`, the assets module will use `10`. See [Configuration Precedence](#configuration-precedence) section for detailed explanation and examples.

### Module-Specific Configuration

**Assets Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.assets.batchLimit` | `number` | `20` | Asset objects fetched per API call |
| `modules.assets.chunkFileSize` | `number` | `1` | Size in MB for chunking large metadata JSON files (assets.json) |
| `modules.assets.downloadLimit` | `number` | `5` | Parallel asset file downloads |
| `modules.assets.fetchConcurrency` | `number` | `5` | Parallel fetch operations for asset metadata |
| `modules.assets.includeVersionedAssets` | `boolean` | `false` | Include versioned assets |
| `modules.assets.securedAssets` | `boolean` | `false` | Export secured assets (adds auth token to asset URLs) |
| `modules.assets.displayExecutionTime` | `boolean` | `false` | Display execution time for batch operations |
| `modules.assets.enableDownloadStatus` | `boolean` | `false` | Enable download progress display for asset files |
| `modules.assets.assetsMetaKeys` | `string[]` | `[]` | Additional metadata keys to include (default includes: `['uid', 'url', 'filename', 'parent_uid']`) |
| `modules.assets.host` | `string` | `"https://images.contentstack.io"` | CDN host for asset URLs |

**CS Assets (cs-assets)**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.cs-assets.chunkFileSizeMb` | `number` | `1` | Maximum size (in MB) of each chunk when the CLI splits large assets.json metadata files during export. |
| `modules.cs-assets.apiConcurrency` | `number` | `5` | Parallel Asset Management (AM) API calls during export. |
| `modules.cs-assets.downloadAssetsConcurrency` | `number` | `5` | Number of asset files downloaded in parallel during export. |
| `modules.cs-assets.securedAssets` | `boolean` | `false` | Add auth token to asset download URLs. Required when [secured assets](/docs/administration) are enabled. |

> **Note:** If CS Assets is not active, the CLI ignores these options. They apply only when your region has CS Assets enabled and the branch has linked workspaces. See [CLI for CS Assets](/docs/developers/cli/cli-for-cs-assets).

**Entries Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.entries.limit` | `number` | `100` | Entries fetched per API call per content type/locale |
| `modules.entries.batchLimit` | `number` | `20` | Parallel entry version fetches when `exportVersions: true` (only used for version export) |
| `modules.entries.exportVersions` | `boolean` | `false` | Export all versions of each entry |
| `modules.entries.chunkFileSize` | `number` | `10` | Size in MB for chunking large entry JSON files (defaults to FsUtility default of 10 if not specified) |
| `modules.entries.invalidKeys` | `string[]` | See default | Keys to exclude from exported entries |
| `modules.entries.dependencies` | `string[]` | `['locales', 'content-types']` | Required modules that must be exported first |

**Default invalidKeys:** `['stackHeaders', 'content_type_uid', 'urlPath', 'created_at', 'updated_at', 'created_by', 'updated_by', '_metadata', 'published']`

> **Note:** `downloadLimit` is not used for entries export (only applies to assets module).

**Precedence:** Module-specific `chunkFileSize`, `limit`, and `batchLimit` are module-specific only and don't have root-level equivalents.

**Content Types Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.content-types.limit` | `number` | `100` | Content types fetched per API call |
| `modules.content-types.validKeys` | `string[]` | See default | Valid keys to export |

**Default validKeys:** `["title", "uid", "field_rules", "schema", "options", "singleton", "description"]`

> **Note:** Content Types module uses the root-level `writeConcurrency` setting. Module-specific `writeConcurrency` is not supported for this module.

**Global Fields Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.global-fields.limit` | `number` | `100` | Global fields fetched per API call |
| `modules.global-fields.validKeys` | `string[]` | See default | Valid keys to export |

**Default validKeys:** `["title", "uid", "schema", "options", "singleton", "description"]`

**Taxonomies Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.taxonomies.limit` | `number` | `100` | Taxonomies fetched per API call |
| `modules.taxonomies.invalidKeys` | `string[]` | See default | Keys to exclude from exported taxonomies |

**Default invalidKeys:** `['updated_at', 'created_by', 'updated_by', 'stackHeaders', 'urlPath', 'created_at']`

**Personalize Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.personalize.baseURL` | `object` | Region-specific | Base URLs for Personalize API by region |
| `modules.personalize.exportOrder` | `string[]` | `['attributes', 'audiences', 'events', 'experiences']` | Export order |

**Base URLs by Region:**

- `AWS-NA`: `https://personalize-api.contentstack.com`
- `AWS-EU`: `https://eu-personalize-api.contentstack.com`
- `AWS-AU`: `https://au-personalize-api.contentstack.com`
- `AZURE-NA`: `https://azure-na-personalize-api.contentstack.com`
- `AZURE-EU`: `https://azure-eu-personalize-api.contentstack.com`
- `GCP-NA`: `https://gcp-na-personalize-api.contentstack.com`
- `GCP-EU`: `https://gcp-eu-personalize-api.contentstack.com`

**Locales Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.locales.limit` | `number` | `100` | Locales fetched per API call |
| `modules.locales.requiredKeys` | `string[]` | See default | Required keys to export for locales |

**Default requiredKeys:** `['code', 'uid', 'name', 'fallback_locale']`

**Environments Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.environments.limit` | `number` | `100` | Environments fetched per API call |

**Extensions Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.extensions.limit` | `number` | `100` | Extensions fetched per API call |

**Stack Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.stack.limit` | `number` | `100` | Stack data fetched per API call |

**Webhooks Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.webhooks.limit` | `number` | `100` | Webhooks fetched per API call |

**Workflows Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.workflows.limit` | `number` | `100` | Workflows fetched per API call |
| `modules.workflows.invalidKeys` | `string[]` | See default | Keys to exclude from exported workflows |

**Default invalidKeys:** `['stackHeaders', 'urlPath', 'created_at', 'updated_at', 'created_by', 'updated_by']`

**Labels Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.labels.limit` | `number` | `100` | Labels fetched per API call |
| `modules.labels.invalidKeys` | `string[]` | See default | Keys to exclude from exported labels |

**Default invalidKeys:** `['stackHeaders', 'urlPath', 'created_at', 'updated_at', 'created_by', 'updated_by']`

### Complete Export Configuration Example

```
{
  "versioning": false,
  "host": "https://api.contentstack.io/v3",
  "preserveStackVersion": false,
  "master_locale": {
    "name": "English - United States",
    "code": "en-us"
  },
  "source_stack": "bltXXXXXXXXXX",
  "data": "./export-data",
  "branchName": "main",
  "moduleName": null,
  "contentTypes": [],
  "securedAssets": false,
  "fetchConcurrency": 5,
  "writeConcurrency": 5,
  "delayMs": 1000,
  "maxContentLength": 100000000,
  "maxBodyLength": 100000000,
  "personalizationEnabled": false,
  "skipStackSettings": false,
  "skipDependencies": false,
  "developerHubBaseUrl": "",
  "marketplaceAppEncryptionKey": "nF2ejRQcTv",
  "modules": {
    "assets": {
      "batchLimit": 20,
      "chunkFileSize": 1,
      "downloadLimit": 5,
      "fetchConcurrency": 5,
      "includeVersionedAssets": false,
      "securedAssets": false,
      "displayExecutionTime": false,
      "enableDownloadStatus": false,
      "assetsMetaKeys": [],
      "host": "https://images.contentstack.io"
    },
    "entries": {
      "limit": 100,
      "batchLimit": 20,
      "exportVersions": false,
      "chunkFileSize": 10
    },
    "content-types": {
      "limit": 100,
      "validKeys": ["title", "uid", "field_rules", "schema", "options", "singleton", "description"]
    },
    "global-fields": {
      "validKeys": ["title", "uid", "schema", "options", "singleton", "description"]
    },
    "taxonomies": {
      "limit": 100
    },
    "personalize": {
      "baseURL": {
        "AWS-NA": "https://personalize-api.contentstack.com",
        "AWS-EU": "https://eu-personalize-api.contentstack.com",
        "AWS-AU": "https://au-personalize-api.contentstack.com",
        "AZURE-NA": "https://azure-na-personalize-api.contentstack.com",
        "AZURE-EU": "https://azure-eu-personalize-api.contentstack.com",
        "GCP-NA": "https://gcp-na-personalize-api.contentstack.com",
        "GCP-EU": "https://gcp-eu-personalize-api.contentstack.com"
      },
      "exportOrder": ["attributes", "audiences", "events", "experiences"]
    }
  }
}
```

---

## Import Configuration

**Command:** `csdx cm:stacks:import`

**Default Configuration:** See the [default import configuration file](https://github.com/contentstack/cli/blob/db01c8a991988e6546e4188ffe3f6693048c7a89/packages/contentstack-import/src/config/index.ts) in the CLI repository.

### Basic Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `versioning` | `boolean` | `false` | No | Import versioned entries |
| `host` | `string` | `"https://api.contentstack.io/v3"` | No | Base URL for Content Management API |
| `extensionHost` | `string` | `"https://app.contentstack.com"` | No | Base URL for Contentstack application |
| `contentVersion` | `number` | - | No | Version of the import format |
| `preserveStackVersion` | `boolean` | `false` | No | Preserve stack version information |
| `target_stack` | `string` | - | Yes\* | API key of target stack |
| `data` | `string` | - | Yes\* | Path to import directory |
| `contentDir` | `string` | - | No | Alias for `data` |

\*Required unless using CLI flags or management token alias

### Path & Directory Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `cliLogsPath` | `string` | - | No | Custom path for CLI logs |
| `backupDir` | `string` | - | No | Path to backup directory |
| `createBackupDir` | `string` | - | No | Path where backup directory should be created |
| `branchName` | `string` | `"main"` | No | Branch name to import into |
| `branchAlias` | `string` | - | No | Branch alias to import into |

### Content Filtering

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `moduleName` | `string` | - | No | Specific module to import |
| `contentTypes` | `string[]` | - | No | Array of content type UIDs |
| `modules` | `string[]` | - | No | Array of module names to import |

### Performance Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `concurrency` | `number` | `1` | No | General concurrency level (used as fallback in some modules) |
| `importConcurrency` | `number` | `5` | No | Number of parallel import operations |
| `fetchConcurrency` | `number` | `5` | No | Number of parallel fetch operations |
| `writeConcurrency` | `number` | `5` | No | Number of parallel write operations |
| `delayMs` | `number` | - | No | Delay in milliseconds between requests |
| `maxContentLength` | `number` | `100000000` | No | Max content length in bytes (100 MB) |
| `maxBodyLength` | `number` | `100000000` | No | Max body length in bytes (100 MB) |

### Publish Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `skipAssetsPublish` | `boolean` | - | No | Skip asset publishing |
| `skipEntriesPublish` | `boolean` | - | No | Skip entry publishing |
| `entriesPublish` | `boolean` | `true` | No | Publish entries after import |

### Feature Flags

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `skipAudit` | `boolean` | - | No | Skip audit fix during import |
| `skipExisting` | `boolean` | - | No | Skip "module exists" warnings |
| `replaceExisting` | `boolean` | - | No | Replace existing modules |
| `exclude-global-modules` | `boolean` | `false` | No | Exclude branch-independent modules (global modules are shared across all branches in a stack; see [Contentstack documentation](/docs/headless-cms/global-modules)) |

### Advanced Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `importWebhookStatus` | `string` | `"disable"` | No | Webhook state: `"disable"` or `"current"` |
| `personalizeProjectName` | `string` | - | No | Unique name for Personalize project |
| `developerHubBaseUrl` | `string` | - | No | Base URL for Developer Hub API |
| `marketplaceAppEncryptionKey` | `string` | `"nF2ejRQcTv"` | No | Encryption key for Marketplace apps |
| `getEncryptionKeyMaxRetry` | `number` | `3` | No | Max retry attempts for encryption key |
| `auditConfig` | `object` | - | No | Configuration for audit process |
| `master_locale` | `object` | - | No | Master locale configuration |

### Authentication

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `email` | `string` | - | No | Email for basic authentication |
| `password` | `string` | - | No | Password for basic authentication |

> **Note:** Use the `--alias` flag to specify a management token alias instead of providing credentials directly in the configuration file.

### Configuration Precedence Note

**Important:** When the same configuration key exists at both root level and module level, **module-specific configuration takes precedence**. For example, if you set `importConcurrency: 5` at root and `modules.entries.importConcurrency: 10`, the entries module will use `10`. See [Configuration Precedence](#configuration-precedence) section for detailed explanation and examples.

### Module-Specific Configuration

**Assets Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.assets.assetBatchLimit` | `number` | `1` | Assets processed per batch |
| `modules.assets.uploadAssetsConcurrency` | `number` | `2` | Assets uploaded in parallel |
| `modules.assets.importFoldersConcurrency` | `number` | `1` | Folders processed in parallel |
| `modules.assets.importSameStructure` | `boolean` | `true` | Maintain folder structure |
| `modules.assets.includeVersionedAssets` | `boolean` | `false` | Include versioned assets |
| `modules.assets.displayExecutionTime` | `boolean` | `false` | Display execution time |
| `modules.assets.host` | `string` | `"https://api.contentstack.io"` | API host for asset operations |
| `modules.assets.validKeys` | `string[]` | See default | Valid keys to import for assets |
| `modules.assets.folderValidKeys` | `string[]` | See default | Valid keys to import for folders |

**Default validKeys:** `["title", "parent_uid", "description", "tags"]`  
**Default folderValidKeys:** `["name", "parent_uid"]`

> **Note:** `modules.assets.fetchConcurrency` can override root-level `fetchConcurrency` if specified.

**Entries Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.entries.importConcurrency` | `number` | `5` | Parallel entry import operations (overrides root `importConcurrency` if set) |
| `modules.entries.chunkFileSize` | `number` | `10` | Size in MB for chunking large entry mapper JSON files (defaults to FsUtility default of 10 if not specified) |
| `modules.entries.invalidKeys` | `string[]` | See default | Keys to exclude from entry mapper files |

**Default invalidKeys:** `['created_at', 'updated_at', 'created_by', 'updated_by', '_metadata', 'published']`

**Precedence:** `modules.entries.importConcurrency` takes precedence over root-level `importConcurrency`. If not set, falls back to root `importConcurrency` (default: 5).

**CS Assets (cs-assets)**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.cs-assets.apiConcurrency` | `number` | `5` | Parallel Asset Management (AM) API calls during import. |
| `modules.cs-assets.uploadAssetsConcurrency` | `number` | `2` | Number of asset files uploaded in parallel during import. |
| `modules.cs-assets.importFoldersConcurrency` | `number` | `1` | Number of folder creation operations run in parallel during import. |

> **Note:** If CS Assets is not active, the CLI ignores these options. They apply only when the content directory contains a `spaces/` directory exported using CS Assets mode. See [CLI for CS Assets](/docs/developers/cli/cli-for-cs-assets).

**Content Types Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.content-types.limit` | `number` | `100` | Content types processed per batch |
| `modules.content-types.validKeys` | `string[]` | See default | Valid keys to import |
| `modules.content-types.writeConcurrency` | `number` | `5` | Parallel content type operations (overrides root `writeConcurrency` if set) |

**Default validKeys:** `["title", "uid", "schema", "options", "singleton", "description"]`

**Precedence:** `modules.content-types.writeConcurrency` takes precedence over root-level `writeConcurrency`. If not set, falls back to root `writeConcurrency` (default: 5).

**Global Fields Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.global-fields.limit` | `number` | `100` | Global fields processed per batch |
| `modules.global-fields.validKeys` | `string[]` | See default | Valid keys to import |
| `modules.global-fields.writeConcurrency` | `number` | `5` | Parallel global field operations (overrides root `writeConcurrency` if set) |

**Default validKeys:** `["title", "uid", "schema", "options", "singleton", "description"]`

**Precedence:** `modules.global-fields.writeConcurrency` takes precedence over root-level `writeConcurrency`. If not set, falls back to root `writeConcurrency` (default: 5).

**Locales Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.locales.writeConcurrency` | `number` | `5` | Parallel locale operations (overrides root `writeConcurrency` if set) |
| `modules.locales.requiredKeys` | `string[]` | See default | Required keys to import for locales |

**Default requiredKeys:** `['code', 'uid', 'name', 'fallback_locale']`

**Precedence:** `modules.locales.writeConcurrency` takes precedence over root-level `writeConcurrency`. If not set, falls back to root `writeConcurrency` (default: 5).

**Environments Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.environments.fetchConcurrency` | `number` | `2` | Parallel environment operations (overrides root `fetchConcurrency` if set) |

**Precedence:** `modules.environments.fetchConcurrency` takes precedence over root-level `fetchConcurrency`. If not set, falls back to root `fetchConcurrency` (default: 5), but the module default is 2.

**Extensions Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.extensions.concurrency` | `number` | `1` | Parallel extension operations (falls back to `fetchConcurrency` if not set) |
| `modules.extensions.validKeys` | `string[]` | See default | Valid keys to import for extensions |

**Default validKeys:** `['data_type', 'srcdoc', 'title', 'type', 'mutiple', 'config']`

**Taxonomies Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.taxonomies.dirName` | `string` | `"taxonomies"` | Directory name for taxonomies |
| `modules.taxonomies.fileName` | `string` | `"taxonomies.json"` | File name for taxonomies data |

**Personalize Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.personalize.baseURL` | `object` | Region-specific | Base URLs for Personalize API by region |
| `modules.personalize.importData` | `boolean` | `true` | Enable/disable Personalize data import |
| `modules.personalize.importOrder` | `string[]` | `['attributes', 'audiences', 'events', 'experiences']` | Import order |
| `modules.personalize.project_id` | `string` | `""` | Personalize project ID (auto-populated) |
| `modules.personalize.experiences.thresholdTimer` | `number` | `60000` | Timer threshold in milliseconds |
| `modules.personalize.experiences.checkIntervalDuration` | `number` | `10000` | Check interval duration in milliseconds |

**Base URLs:** Same as Export configuration (see Export section above).

**Variant Entry Module**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.variantEntry.apiConcurrency` | `number` | `5` | Parallel API calls |
| `modules.variantEntry.query.locale` | `string` | `"en-us"` | Locale for variant entry queries |

**General Module Settings**

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.apiConcurrency` | `number` | `5` | General API concurrency for modules |

### Complete Import Configuration Example

```
{
  "versioning": false,
  "host": "https://api.contentstack.io/v3",
  "extensionHost": "https://app.contentstack.com",
  "contentVersion": 2,
  "preserveStackVersion": false,
  "master_locale": {
    "name": "English - United States",
    "code": "en-us"
  },
  "target_stack": "bltXXXXXXXXXX",
  "data": "./import-data",
  "branchName": "main",
  "moduleName": null,
  "contentTypes": [],
  "skipAssetsPublish": false,
  "skipEntriesPublish": false,
  "entriesPublish": true,
  "concurrency": 1,
  "importConcurrency": 5,
  "fetchConcurrency": 5,
  "writeConcurrency": 5,
  "delayMs": 1000,
  "maxContentLength": 100000000,
  "maxBodyLength": 100000000,
  "skipAudit": false,
  "skipExisting": false,
  "replaceExisting": false,
  "importWebhookStatus": "disable",
  "personalizeProjectName": null,
  "exclude-global-modules": false,
  "backupDir": "./backup",
  "createBackupDir": "./temp",
  "cliLogsPath": "./logs",
  "developerHubBaseUrl": "",
  "marketplaceAppEncryptionKey": "nF2ejRQcTv",
  "getEncryptionKeyMaxRetry": 3,
  "auditConfig": {
    "noLog": false,
    "skipConfirm": true,
    "returnResponse": true,
    "noTerminalOutput": false,
    "config": {
      "basePath": ""
    }
  },
  "modules": {
    "apiConcurrency": 5,
    "assets": {
      "assetBatchLimit": 1,
      "uploadAssetsConcurrency": 2,
      "importFoldersConcurrency": 1,
      "importSameStructure": true,
      "includeVersionedAssets": false,
      "displayExecutionTime": false,
      "host": "https://api.contentstack.io",
      "validKeys": ["title", "parent_uid", "description", "tags"],
      "folderValidKeys": ["name", "parent_uid"]
    },
    "entries": {
      "importConcurrency": 5,
      "chunkFileSize": 10
    },
    "content-types": {
      "limit": 100,
      "validKeys": ["title", "uid", "schema", "options", "singleton", "description"]
    },
    "global-fields": {
      "limit": 100,
      "validKeys": ["title", "uid", "schema", "options", "singleton", "description"]
    },
    "taxonomies": {
      "dirName": "taxonomies",
      "fileName": "taxonomies.json"
    },
    "personalize": {
      "baseURL": {
        "AWS-NA": "https://personalize-api.contentstack.com",
        "AWS-EU": "https://eu-personalize-api.contentstack.com",
        "AWS-AU": "https://au-personalize-api.contentstack.com",
        "AZURE-NA": "https://azure-na-personalize-api.contentstack.com",
        "AZURE-EU": "https://azure-eu-personalize-api.contentstack.com",
        "GCP-NA": "https://gcp-na-personalize-api.contentstack.com",
        "GCP-EU": "https://gcp-eu-personalize-api.contentstack.com"
      },
      "importData": true,
      "importOrder": ["attributes", "audiences", "events", "experiences"],
      "project_id": "",
      "experiences": {
        "thresholdTimer": 60000,
        "checkIntervalDuration": 10000
      }
    },
    "variantEntry": {
      "apiConcurrency": 5,
      "query": {
        "locale": "en-us"
      }
    }
  },
}
```

---

## Audit Configuration

**Command:** `csdx cm:stacks:audit`

**Default Configuration:** See the [default audit configuration file](https://github.com/contentstack/cli/blob/db01c8a991988e6546e4188ffe3f6693048c7a89/packages/contentstack-audit/src/config/index.ts) in the CLI repository.

### Basic Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `showTerminalOutput` | `boolean` | `true` | No | Display output on terminal |
| `skipRefs` | `string[]` | `['sys_assets']` | No | References to skip during audit |
| `skipFieldTypes` | `string[]` | `['taxonomy', 'group']` | No | Field types to skip |
| `fixSelectField` | `boolean` | `false` | No | Fix select field issues |

### Module Configuration

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `modules` | `string[]` | See default | No | Modules to audit |

**Default modules:** `['content-types', 'global-fields', 'entries', 'extensions', 'workflows', 'custom-roles', 'assets', 'field-rules']`

### Field Configuration

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `fix-fields` | `string[]` | See default | No | Field types that can be fixed |
| `schema-fields-data-type` | `string[]` | See default | No | Schema field data types to check |

**Default fix-fields:** `['reference', 'global_field', 'json:rte', 'json:extension', 'blocks', 'group', 'content_types']`  
**Default schema-fields-data-type:** `['blocks', 'group', 'global_field']`

### Entry System Keys

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `entries.systemKeys` | `string[]` | See default | No | System keys in entries |

**Default systemKeys:** `['uid', 'ACL', 'tags', 'locale', '_version', '_metadata', 'published', 'created_at', 'updated_at', 'created_by', 'updated_by', '_in_progress', '_restore_status', 'publish_details']`

### External Configuration (via --config flag)

When using the `--config` flag with audit commands, you can pass external configuration options:

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `noLog` | `boolean` | `false` | Skip logs printing on terminal |
| `skipConfirm` | `boolean` | `true` | Skip confirmation prompts |
| `returnResponse` | `boolean` | `true` | Return config used in command on completion |
| `noTerminalOutput` | `boolean` | `false` | Skip final audit table output on terminal |
| `basePath` | `string` | `""` | Overwrite built-in config base path (equivalent to --data-dir flag) |

**Example external config file:**

```
{
  "noLog": false,
  "skipConfirm": true,
  "returnResponse": true,
  "noTerminalOutput": false,
  "basePath": "./export-data"
}
```

---

## Query-Export Configuration

**Command:** `csdx cm:stacks:export-query`

### Basic Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `host` | `string` | `"https://api.contentstack.io/v3"` | No | Base URL for Content Management API |
| `exportDir` | `string` | - | Yes\* | Path to export directory |
| `stackApiKey` | `string` | - | Yes\* | API key of source stack |
| `branchName` | `string` | - | No | Branch name to export from |
| `branchAlias` | `string` | - | No | Branch alias to export from |

\*Required unless using CLI flags or management token alias

### Query Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `query` | `object\|string` | - | Yes\* | Query object or file path for filtering |
| `skipReferences` | `boolean` | `false` | No | Skip referenced content types |
| `skipDependencies` | `boolean` | `false` | No | Skip dependent modules |
| `skipStackSettings` | `boolean` | `false` | No | Skip exporting stack settings |
| `maxCTReferenceDepth` | `number` | `20` | No | Max depth for content type references |

### Performance Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `fetchConcurrency` | `number` | `5` | No | Number of parallel fetch operations |
| `writeConcurrency` | `number` | `5` | No | Number of parallel write operations |
| `batchSize` | `number` | `100` | No | Number of items per batch |

### Feature Flags

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `securedAssets` | `boolean` | `false` | No | Export secured assets |
| `personalizationEnabled` | `boolean` | `false` | No | Enable personalization features |

### Query Configuration

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `queryConfig.maxRecursionDepth` | `number` | `10` | Maximum depth for recursive query processing |
| `queryConfig.batchSize` | `number` | `100` | Number of items per batch |
| `queryConfig.metadataFileName` | `string` | `"_query-meta.json"` | Name of the metadata file |
| `queryConfig.validation.maxQueryDepth` | `number` | `5` | Maximum depth of nested queries |
| `queryConfig.validation.maxArraySize` | `number` | `1000` | Maximum size of arrays in queries |
| `queryConfig.validation.allowedDateFormats` | `string[]` | `['ISO8601', 'YYYY-MM-DD', 'MM/DD/YYYY']` | Allowed date formats |

### Module Configuration

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `modules.general` | `string[]` | `['stack', 'locales', 'environments']` | Always exported modules |
| `modules.queryable` | `string[]` | `['content-types']` | Modules that can be queried |
| `modules.dependent` | `string[]` | `['global-fields', 'extensions', 'marketplace-apps', 'taxonomies', 'personalize']` | Dependent modules |
| `modules.content` | `string[]` | `['entries', 'assets']` | Content modules |
| `modules.exportOrder` | `string[]` | See default | Export order based on dependencies |

**Default exportOrder:** `['stack', 'locales', 'environments', 'content-types', 'global-fields', 'extensions', 'taxonomies', 'entries', 'assets']`

> **Note:** The `modules.dependent` array includes `marketplace-apps` and `personalize` in addition to the listed modules.

### Authentication

> **Note:** Use the `--alias` flag to specify a management token alias instead of providing credentials directly in the configuration file.

### Complete Query-Export Configuration Example

```
{
  "host": "https://api.contentstack.io/v3",
  "exportDir": "./query-export-data",
  "stackApiKey": "bltXXXXXXXXXX",
  "branchName": "main",
  "query": {
    "title": {
      "$regex": "blog"
    }
  },
  "skipReferences": false,
  "skipDependencies": false,
  "skipStackSettings": false,
  "securedAssets": false,
  "fetchConcurrency": 5,
  "writeConcurrency": 5,
  "batchSize": 100,
  "personalizationEnabled": false,
  "maxCTReferenceDepth": 20,
  "queryConfig": {
    "maxRecursionDepth": 10,
    "batchSize": 100,
    "metadataFileName": "_query-meta.json",
    "validation": {
      "maxQueryDepth": 5,
      "maxArraySize": 1000,
      "allowedDateFormats": ["ISO8601", "YYYY-MM-DD", "MM/DD/YYYY"]
    }
  },
  "modules": {
    "general": ["stack", "locales", "environments"],
    "queryable": ["content-types"],
    "dependent": ["global-fields", "extensions", "marketplace-apps", "taxonomies", "personalize"],
    "content": ["entries", "assets"],
    "exportOrder": [
      "stack",
      "locales",
      "environments",
      "content-types",
      "global-fields",
      "extensions",
      "taxonomies",
      "entries",
      "assets"
    ]
  }
}
```

---

## Import-Setup Configuration

**Command:** `csdx cm:stacks:import-setup`

### Basic Settings

| Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `host` | `string` | `"https://api.contentstack.io/v3"` | No | Base URL for Content Management API |
| `developerHubBaseUrl` | `string` | `""` | No | Base URL for Developer Hub API |
| `fetchConcurrency` | `number` | `5` | No | Number of parallel fetch operations |

### Module Configuration

Each module can specify dependencies that must be imported first:

| Module | Option | Type | Default | Required | Description |
| --- | --- | --- | --- | --- | --- |
| `custom-roles` | `modules.custom-roles.dependencies` | `string[]` | `['environments', 'entries']` | No | Required dependencies |
| `locales` | `modules.locales.dependencies` | `string[]` | `[]` | No | Required dependencies |
| `environments` | `modules.environments.dependencies` | `string[]` | - | No | Required dependencies |
| `extensions` | `modules.extensions.dependencies` | `string[]` | - | No | Required dependencies |
| `assets` | `modules.assets.fetchConcurrency` | `number` | `5` | No | Fetch concurrency for assets |
| `content-types` | `modules.content-types.dependencies` | `string[]` | `['extensions', 'marketplace-apps', 'taxonomies']` | No | Required dependencies |
| `entries` | `modules.entries.dependencies` | `string[]` | `['assets', 'extensions', 'marketplace-apps', 'taxonomies']` | No | Required dependencies |
| `global-fields` | `modules.global-fields.dependencies` | `string[]` | `['extensions', 'marketplace-apps']` | No | Required dependencies |
| `marketplace-apps` | `modules.marketplace-apps.dependencies` | `string[]` | - | No | Required dependencies |
| `taxonomies` | `modules.taxonomies.invalidKeys` | `string[]` | See default | No | Keys to exclude during import |

**Default taxonomies invalidKeys:** `['updated_at', 'created_by', 'updated_by', 'stackHeaders', 'urlPath', 'created_at', 'ancestors', 'update', 'delete', 'fetch', 'descendants', 'move', 'search']`

---

## Migration Configuration

**Command:** `csdx cm:stacks:migration`

### Configuration Options

Migration uses either inline configuration or external JSON files.

### Inline Configuration

Use `--config` flag with key-value pairs:

```
csdx cm:migration --config key1:value1 key2:value2 --file-path <migration/script/file/path>
```

### External Configuration File

Use `--config-file` flag with JSON file:

```
{
  "apiKey": "your-api-key",
  "branch": "main",
  "customKey": "customValue"
}
```

> **Note:** Use the `--alias` flag to specify a management token alias instead of providing `managementToken` in the configuration file.

> **Note:** Migration configuration is script-specific and varies based on your migration requirements.

---

## Quick Reference Guide

### Common Configuration Patterns

#### Performance Tuning

```
{
  "fetchConcurrency": 10,
  "writeConcurrency": 10,
  "delayMs": 500
}
```

#### Export Specific Content Types

```
{
  "contentTypes": ["blog_post", "author"],
  "moduleName": "entries"
}
```

#### Import with Backup

```
{
  "backupDir": "./backup",
  "createBackupDir": "./temp-backup"
}
```

### Best Practices

1. **Path Formatting**:
   - Mac/Linux: Use forward slashes `/`
   - Windows: Use double backslashes `\\\\` or forward slashes `/`

2. **Authentication**:
   - Always use `--alias` flag instead of hardcoding tokens
   - Never commit configuration files with credentials

3. **Module Dependencies**:
   - Import/export modules in correct order
   - CLI handles dependencies automatically for full imports/exports

4. **Performance**:
   - Adjust concurrency based on API rate limits
   - Use `delayMs` to avoid rate limiting
   - Monitor `maxContentLength` and `maxBodyLength` for large operations

5. **Backup**:
   - Always provide `backupDir` when importing modules individually
   - Maintain mapping files across multiple imports

### Troubleshooting

**Issue:** Horizontal scrolling on tables  
**Solution:** Use collapsible sections (details/summary tags) for module-specific configs

**Issue:** Configuration not being read  
**Solution:**

- Verify JSON syntax is valid
- Check file path is correct
- Ensure required fields are present

**Issue:** Rate limiting errors  
**Solution:**

- Reduce `fetchConcurrency` and `writeConcurrency`
- Increase `delayMs` between requests
