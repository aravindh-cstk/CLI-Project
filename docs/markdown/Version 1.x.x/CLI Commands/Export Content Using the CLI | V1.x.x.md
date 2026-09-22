---
uid: "blt878916ff618af5c2"
seo_title: "Export Content Using the CLI | V1.x.x | Contentstack"
seo_description: "Export content efficiently with Contentstack’s latest Command-line Interface commands to simplify data migration and content backup."
---

# Export Content Using the CLI

## Overview

To migrate content from one [stack](/docs/headless-cms/about-stack) to another, begin by exporting content from the source stack, then import it into the destination stack.

This guide explains how to use the `cm:stacks:export` command by logging in to CLI (or with a **management token**), using configuration files or direct CLI parameters.

## Prerequisites

Before exporting content, ensure you have:

- [Contentstack account](https://www.contentstack.com/login/)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli/v1)
- CLI [authenticated](/docs/headless-cms/cli-authentication/v1)
- [Configured management token](/docs/headless-cms/cli-authentication/v1#add-management-token) *(optional, but recommended for CI/CD)*

## Supported Modules

The export command supports the following modules:

- **Assets** - All assets in the stack
- **Locales** - Language configurations
- **Environments** - Environment settings
- **Stacks** - Stack settings (supported from CLI v1.42.0)
- **Extensions** - UI Extensions
- **Marketplace Apps** - Installed marketplace applications
- **Webhooks** - Webhook configurations
- **Global Fields** - Global field definitions (including Nested Global Fields from v1.42.0)
- **Content Types** - Content type schemas
- **Entries** - Content entries
- **Labels** - Content labels
- **Workflow** - Workflow configurations
- **Custom Role** - Custom role definitions
- **Taxonomy** - Taxonomy structures
- **Personalize** - Personalize project configurations
- **CS Assets** - Space-based asset export when cs-assets is enabled for the region

**Not Supported:**

- ❌ Users
- ❌ Releases

## Commands

The `cm:stacks:export` command lets you export content from one stack to your local file system.

### Usage

```
csdx cm:stacks:export [OPTIONS]
```

**OR**

```
csdx cm:export [OPTIONS]
```

### Options

| Option | Description | Required |
| --- | --- | --- |
| `-k, --stack-api-key=<stack-api-key>` | API key of the source stack. | No\* |
| `-a, --alias=<alias>` | Management token alias of the source stack. | No\* |
| `-d, --data-dir=<data-dir>` | Absolute path to the folder to store the exported content. Example: `-d "/Users/Name/Desktop/cli/content"` or `-d "C:\\Users\\Name\\Desktop\\cli\\content"`. If using branches, include the branch folder in the path: `-d "/path/to/export/branch_name"`. | No |
| `--branch=<branch>` | Name of the branch where you want to export content. Default: `main`. If not specified, exports from all branches. | No |
| `--branch-alias=<branch-alias>` | Alias of the branch where you want to export content. Cannot be used with `--branch`. | No |
| `--module=<module>` | Export a specific module from the source stack. If not specified, all modules are exported. Available modules: `assets`, `content-types`, `entries`, `environments`, `stacks`, `extensions`, `marketplace-apps`, `global-fields`, `labels`, `locales`, `webhooks`, `workflows`, `custom-roles`, `taxonomies`, `personalize`. | No |
| `--content-types=<content-types>` | The UID of the content type(s) whose content you want to export. For multiple content types, specify the IDs separated by spaces. Example: `--content-types blog_post article`. | No |
| `--secured-assets` | Use this flag to export content if the [secured assets](/docs/administration#manage-asset-security) feature is enabled for your stack. | No |
| `-y, --yes` | Force override all Marketplace prompts. | No |
| `-c, --config=<config>` | Path to the configuration JSON file containing all the options for a single run. | No |

> **Note:** Either `-k` (stack-api-key) or `-a` (alias) is required. If using `-k`, you must be logged in or have a management token configured.

### Examples

**Export All Modules**

**Using Stack API Key:**

```
csdx cm:stacks:export -k blt1234567890abcdef --data-dir ./export
```

**Using Management Token Alias (Recommended):**

```
csdx cm:stacks:export -a production --data-dir ./export
```

**Using Relative Path:**

```
csdx cm:stacks:export -a production --data-dir ./export-data
```

**Using Absolute Path (macOS/Linux):**

```
csdx cm:stacks:export -a production --data-dir /Users/username/Desktop/export
```

**Using Absolute Path (Windows):**

```
csdx cm:stacks:export -a production --data-dir "C:\Users\Username\Desktop\export"
```

**Export from Specific Branch**

**Using Branch Name:**

```
csdx cm:stacks:export -a production --data-dir ./export --branch develop
```

**Using Branch Alias:**

```
csdx cm:stacks:export -a production --data-dir ./export --branch-alias developAlias
```

**Export Structure with Branch:**

```
./export/
  └── develop/
      ├── assets/
      ├── content-types/
      ├── entries/
      └── ...
```

**Export Specific Module**

**Export Only Content Types:**

```
csdx cm:stacks:export -a production --data-dir ./export --module content-types
```

**Export Only Assets:**

```
csdx cm:stacks:export -a production --data-dir ./export --module assets
```

**Export Only Entries:**

```
csdx cm:stacks:export -a production --data-dir ./export --module entries
```

**Export Multiple Modules (Sequential):**

```
# Export assets first
csdx cm:stacks:export -a production --data-dir ./export --module assets

# Then export content types
csdx cm:stacks:export -a production --data-dir ./export --module content-types

# Finally export entries
csdx cm:stacks:export -a production --data-dir ./export --module entries
```

When exporting modules individually, follow this module sequence for best results:

1. `assets`
2. `environments`
3. `stacks`
4. `locales`
5. `extensions`
6. `marketplace-apps`
7. `webhooks`
8. `taxonomies`
9. `global-fields`
10. `content-types`
11. `workflows`
12. `entries`
13. `labels`
14. `custom-roles`

**Export Specific Content Types**

**Export Entries from Specific Content Types:**

```
csdx cm:stacks:export -a production --data-dir ./export --content-types blog_post article
```

**Export Multiple Content Types:**

```
csdx cm:stacks:export -a production --data-dir ./export --content-types blog_post article product_page
```

> **Note:** This exports only entries from the specified content types. Content types themselves are still exported if using `--module content-types`.

**Export Secured Assets**

**Export with Secured Assets Flag:**

```
csdx cm:stacks:export -a production --data-dir ./export --secured-assets
```

> **Note:** Ensure to add the `--secured-assets` flag to avoid errors while exporting content for stacks where the [secured assets](/docs/administration#manage-asset-security) feature is enabled.

**Export Marketplace Apps**

**Export Marketplace Apps (Interactive):**

```
csdx cm:stacks:export -a production --data-dir ./export --module marketplace-apps
```

**Export Marketplace Apps (Skip Prompts):**

```
csdx cm:stacks:export -a production --data-dir ./export --module marketplace-apps -y
```

> **Note:** If the `--yes` flag is not passed, you are prompted to enter an encryption key while exporting Marketplace apps for app configurations.

## Using Configuration File

You can also export content using a configuration file. This is useful for:

- Reproducible exports
- CI/CD automation
- Complex export configurations
- Performance tuning

### Step 1: Download Configuration File

Download the example configuration file:

- [Authentication-based config](https://github.com/contentstack/cli/blob/db01c8a991988e6546e4188ffe3f6693048c7a89/packages/contentstack-export/example_config/auth_config.json)
- [Management token-based config](https://github.com/contentstack/cli/blob/db01c8a991988e6546e4188ffe3f6693048c7a89/packages/contentstack-export/example_config/management_config.json)

### Step 2: Configure Your Values

Edit the configuration file with your values:

**Example Configuration (auth_config.json):**

```
{
  "contentVersion": 2,
  "master_locale": {
    "name": "English - United States",
    "code": "en-us"
  },
  "source_stack": "blt1234567890abcdef",
  "data": "/path/to/export/directory",
  "branchName": "develop",
  "moduleName": "content-types",
  "fetchConcurrency": 5,
  "writeConcurrency": 5,
  "securedAssets": false,
  "maxContentLength": 100000000,
  "maxBodyLength": 100000000,
  "delayMs": 1000
}
```

**Example Configuration (management_config.json):**

```
{
  "contentVersion": 2,
  "master_locale": {
    "name": "English - United States",
    "code": "en-us"
  },
  "data": "/path/to/export/directory",
  "branchName": "develop",
  "moduleName": "content-types",
  "fetchConcurrency": 5,
  "writeConcurrency": 5,
  "securedAssets": false,
  "createBackupDir": "./temp",
  "maxContentLength": 100000000,
  "maxBodyLength": 100000000,
  "delayMs": 1000
}
```

### Step 3: Run Export with Config File

**Using Authentication:**

```
csdx cm:stacks:export -c /path/to/auth_config.json
```

**Using Management Token Alias:**

```
csdx cm:stacks:export -a production -c /path/to/management_config.json
```

**Example (macOS/Linux):**

```
csdx cm:stacks:export -a production -c "/Users/username/Desktop/config.json"
```

**Example (Windows):**

```
csdx cm:stacks:export -a production -c "C:\Users\Username\Desktop\config.json"
```

> **Note:**
>
> - macOS/Linux users must use `/` for paths in a JSON file.
> - Windows users must use `\\` (double backslashes) for paths in a JSON file.

### Configuration File Options

| Option | Description | Type | Default |
| --- | --- | --- | --- |
| `contentVersion` | Content version format. | number | `2` |
| `master_locale` | Master locale configuration. | object | - |
| `source_stack` | UID of the stack from which data must be exported. Required for auth-based config. | string | - |
| `data` | File path where the data must be stored. | string | - |
| `branchName` | Name of the branch from which data must be exported. | string | `main` |
| `branchAlias` | Alias of the branch from which data must be exported. | string | - |
| `moduleName` | Module name to be exported. Options: `stack`, `assets`, `locales`, `environments`, `extensions`, `webhooks`, `global-fields`, `content-types`, `custom-roles`, `workflows`, `entries`, `labels`, `marketplace-apps`, `taxonomies`, `personalize`. | string | - |
| `fetchConcurrency` | Number of files that must be fetched in one request. | number | `5` |
| `writeConcurrency` | Number of files that must be written in one request. | number | `5` |
| `securedAssets` | Fetch only secured assets. | boolean | `false` |
| `maxContentLength` | Maximum content length in bytes. Default: 100 MB (100000000). | number | `100000000` |
| `maxBodyLength` | Maximum body length in bytes. Default: 100 MB (100000000). | number | `100000000` |
| `delayMs` | Delay in milliseconds between API requests to prevent concurrency issues. | number | `1000` |
| `createBackupDir` | Path for backup directory (management token config only). | string | - |
| `versioning` | Export versioned entries. | boolean | `false` |
| `preserveStackVersion` | Preserve stack version while exporting the data. | boolean | `false` |
| `host` | Set the host for export operation. Any valid base URL from [Content Management API](/docs/developers/apis/content-management-api). | string | - |

## Export Content Using Management Token

You can export content from your stack using a [management token](/docs/headless-cms/cli-authentication/v1#add-management-token). This is the recommended approach for CI/CD environments.

### Basic Usage

**Export with Alias Only:**

```
csdx cm:stacks:export -a production
```

**Export with Alias and Data Directory:**

```
csdx cm:stacks:export -a production --data-dir ./export
```

**Export with Alias and Configuration File:**

```
csdx cm:stacks:export -a production -c /path/to/config.json
```

### Developer Example - CI/CD Integration

**GitHub Actions:**

```
- name: Export Contentstack Stack
  run: |
    csdx cm:stacks:export \
      -a ${{ secrets.MANAGEMENT_TOKEN_ALIAS }} \
      --data-dir ./export \
      --module entries \
      -y
```

**GitLab CI:**

```
export_stack:
  script:
    - csdx cm:stacks:export -a $MANAGEMENT_TOKEN_ALIAS --data-dir ./export -y
  artifacts:
    paths:
      - export/
```

## Toggle Between Console Logs and Progress Manager View

Contentstack CLI lets you toggle between the raw console logs and the visual Progress Manager UI during export workflows.

### Default Mode (Progress Manager UI)

By default, the Progress Manager UI displays when you run the export command:

```
csdx cm:stacks:export -a production --data-dir ./export
```

**Example Output:**

```
STACK:
   ├─ Settings             |████████████████████████████████████████| 100% | 1/1 | ✓ Complete (1/1)
   ├─ Locale               |████████████████████████████████████████| 100% | 1/1 | ✓ Complete (1/1)

LOCALES:
    └─ Locales             |████████████████████████████████████████| 100% | 2/2 | ✓ Complete (2/2)

CONTENT TYPES:
    └─ Content types       |████████████████████████████████████████| 100% | 6/6 | ✓ Complete (6/6)

ENTRIES:
   ├─ Entries              |████████████████████████████████████████| 100% | 12/12 | ✓ Complete (12/12)
```

### Console Log Mode

**Step 1: Enable Console Logs**

```
csdx config:set:log --show-console-logs
```

**Step 2: Run Export Command**

```
csdx cm:stacks:export -a production --data-dir ./export
```

**Example Output:**

```
[2025-08-22 16:12:23] INFO: Exporting content from branch main
[2025-08-22 16:12:23] INFO: Started to export content, version is 2
[2025-08-22 16:12:23] INFO: Exporting module: stack
[2025-08-22 16:12:24] INFO: Exporting stack settings
[2025-08-22 16:12:25] SUCCESS: Exported stack settings successfully!
```

**Step 3: Switch Back to Default Mode**

```
csdx config:set:log --no-show-console-logs
```

> **Tip:** Use `--show-console-logs` for detailed debugging when troubleshooting export issues.

## Common Export Scenarios

### Scenario 1: Full Stack Export

Export all modules from a stack for backup or migration:

```
csdx cm:stacks:export -a production --data-dir ./full-export
```

### Scenario 2: Selective Content Export

Export only specific content types:

```
csdx cm:stacks:export -a production --data-dir ./export --content-types blog_post article
```

### Scenario 3: Branch-Specific Export

Export content from a development branch:

```
csdx cm:stacks:export -a production --data-dir ./export --branch develop
```

### Scenario 4: High-Performance Export

Use configuration file with optimized concurrency settings:

```
{
  "fetchConcurrency": 10,
  "writeConcurrency": 10,
  "delayMs": 500,
  "data": "/path/to/export"
}
```

```
csdx cm:stacks:export -a production -c ./high-performance-config.json
```

### Scenario 5: Large Stack Export

For large stacks, use configuration file with increased limits:

```
{
  "maxContentLength": 200000000,
  "maxBodyLength": 200000000,
  "fetchConcurrency": 3,
  "writeConcurrency": 3,
  "delayMs": 2000,
  "data": "/path/to/export"
}
```

```
csdx cm:stacks:export -a production -c ./large-stack-config.json
```

## Export Directory Structure

After export, your directory structure will look like this:

```
./export/
├── assets/
│   ├── assets.json
│   └── files/
│       └── [asset files]
├── content-types/
│   └── content_types.json
├── entries/
│   └── [content-type-uid]/
│       └── [locale]/
│           └── entries.json
├── environments/
│   └── environments.json
├── locales/
│   └── locales.json
├── global-fields/
│   └── global_fields.json
├── webhooks/
│   └── webhooks.json
├── extensions/
│   └── extensions.json
├── workflows/
│   └── workflows.json
├── labels/
│   └── labels.json
├── custom-roles/
│   └── custom_roles.json
├── taxonomies/
│   └── taxonomies.json
└── stack.json
```

**With Branch:**

```
./export/
└── develop/
    ├── assets/
    ├── entries/
    └── ...
```

## Examples

**Export all modules from a stack:**

```
csdx cm:stacks:export -a <alias> --data-dir ./export
```

**Export specific module:**

```
csdx cm:stacks:export -a <alias> --data-dir ./export --module content-types
```

**Export from specific branch:**

```
csdx cm:stacks:export -a <alias> --data-dir ./export --branch develop
```

## Limitations

For comprehensive information about export limitations, see the [CLI Limitations Guide](/docs/headless-cms/cli-limitations/v1#export-module-limitations).

## Best Practices

For best practices on export workflows, see the CLI Best Practices Guide.

## Next Steps

After successful export:

- [Import content](/docs/headless-cms/import-content-using-the-cli/v1)
- Clone a stack
- [Migrate content](/docs/headless-cms/migrate-content-between-stacks-using-the-cli/v1)
