---
uid: "blt1ee86e6419f390f8"
seo_title: "Import Content Using the CLI | V1.x.x | Contentstack"
seo_description: "Import content efficiently with Contentstack’s latest Command-line Interface commands to streamline data onboarding and content setup."
---

# Import Content Using the CLI

## Overview

After exporting content from a source stack, use the Contentstack CLI to import it into a destination stack.

This guide explains how to use the `cm:stacks:import` command by logging in to CLI (or with a **management token**), using configuration files or direct CLI parameters.

## Prerequisites

Before importing content, ensure you have:

- [Contentstack account](https://www.contentstack.com/login)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli/v1)
- CLI [authenticated](/docs/headless-cms/cli-authentication/v1)
- [Configured management token](/docs/headless-cms/cli-authentication/v1#add-management-token) *(optional, but recommended for CI/CD)*
- [Exported content](/docs/headless-cms/export-content-using-the-cli/v1) extracted (unzipped) in a local folder

## Supported Modules

The import command supports the following modules:

- **Assets** - All assets in the stack
- **Locales** - Language configurations
- **Environments** - Environment settings
- **Stacks** - Stack settings (supported from CLI v1.43.0)
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
- **CS Assets** - Space-based assets

**Not Supported:**

- ❌ Users
- ❌ Releases

> **Note:** Imported content will be published to the same environment and locale as in the source stack. Unpublished content in the source stack will remain unpublished after import.

## Commands

The `cm:stacks:import` command lets you import content into your destination stack.

> **Note:** By default, an audit fix is performed on the exported content before import. This helps identify and address potential issues in the exported data.

### Usage

```
csdx cm:stacks:import [OPTIONS]
```

**OR**

```
csdx cm:import [OPTIONS]
```

### Options

| Option | Description | Required |
| --- | --- | --- |
| `-k, --stack-api-key=<stack-api-key>` | API key of the target stack. | No\* |
| `-a, --alias=<alias>` | Management token alias of the destination stack. | No\* |
| `-d, --data-dir=<data-dir>` | Absolute path to the folder with your exported content. Example: `-d "/Users/Name/Desktop/cli/content"` or `-d "C:\\Users\\Name\\Desktop\\cli\\content"`. If using branches, include the branch folder in the path: `-d "/path/to/export/branch_name"`. | No |
| `--branch=<branch>` | Name of the branch to import content into. Default: `main`. | No |
| `--branch-alias=<branch-alias>` | Alias of the branch to import content into. Cannot be used with `--branch`. | No |
| `--exclude-global-modules` | Exclude [branch-independent modules](/docs/headless-cms/global-modules) from the import operation. | No |
| `--module=<module>` | Import a specific module from the source stack. If not specified, all modules are imported. Available modules: `assets`, `content-types`, `entries`, `environments`, `stacks`, `extensions`, `marketplace-apps`, `global-fields`, `labels`, `locales`, `webhooks`, `workflows`, `custom-roles`, `taxonomies`, `personalize`. | No |
| `--backup-dir=<backup-dir>` | Backup directory name for a specific module. Essential when repeatedly using single module import. | No |
| `--import-webhook-status=<disable\|current>` | Maintain webhook state configuration from the source stack. Default: `disable`. Options: `disable`, `current`. | No |
| `--skip-audit` | Skip the audit fix that occurs during import. | No |
| `--skip-app-recreation` | Skip the recreation of private apps if they already exist. | No |
| `--skip-assets-publish` | Skip asset publishing during import. | No |
| `--skip-entries-publish` | Skip entry publishing during import. | No |
| `--replace-existing` | Replace the existing module in the target stack. | No |
| `--skip-existing` | Skip the module exists warning messages. | No |
| `--personalize-project-name=<name>` | Provide a unique name for the Personalize project. | No |
| `-y, --yes` | Force override all Marketplace prompts. | No |
| `-c, --config=<config>` | Path to the configuration JSON file containing all the options for a single run. | No |

> **Note:** Either `-k` (stack-api-key) or `-a` (alias) is required. If using `-k`, you must be logged in or have a management token configured.

**Important Notes:**

- If you don't use the `--yes` flag during import, you'll be prompted to enter an encryption key for Marketplace App configurations. You can attempt up to three times to enter the correct key. After **three failed attempts**, the import process will stop and must be restarted from the beginning.
- If you don't use the `--skip-audit` flag, the audit step will remove all workflow branches except the one you're importing into. For example, if your source stack has main, development, and production branches, and you import into the development branch, the audit will remove the main and production branches from the workflow module to ensure a clean import.

### Examples

**Import All Modules**

**Using Stack API Key:**

```
csdx cm:stacks:import -k blt1234567890abcdef --data-dir ./export
```

**Using Management Token Alias (Recommended):**

```
csdx cm:stacks:import -a production --data-dir ./export
```

**Using Relative Path:**

```
csdx cm:stacks:import -a production --data-dir ./export-data
```

**Using Absolute Path (macOS/Linux):**

```
csdx cm:stacks:import -a production --data-dir /Users/username/Desktop/export
```

**Using Absolute Path (Windows):**

```
csdx cm:stacks:import -a production --data-dir "C:\Users\Username\Desktop\export"
```

**Import to Specific Branch**

**Using Branch Name:**

```
csdx cm:stacks:import -a production --data-dir ./export --branch develop
```

**Using Branch Alias:**

```
csdx cm:stacks:import -a production --data-dir ./export --branch-alias developAlias
```

**Import Structure with Branch:**

```
./export/
  └── develop/
      ├── assets/
      ├── content-types/
      ├── entries/
      └── ...
```

**Import Specific Module**

**Import Only Content Types:**

```
csdx cm:stacks:import -a production --data-dir ./export --module content-types
```

**Import Only Assets:**

```
csdx cm:stacks:import -a production --data-dir ./export --module assets
```

**Import Only Entries:**

```
csdx cm:stacks:import -a production --data-dir ./export --module entries
```

**Import Multiple Modules (Sequential):**

```
# Import locales first
csdx cm:stacks:import -a production --data-dir ./export --module locales

# Then import environments
csdx cm:stacks:import -a production --data-dir ./export --module environments

# Then import assets
csdx cm:stacks:import -a production --data-dir ./export --module assets

# Finally import entries
csdx cm:stacks:import -a production --data-dir ./export --module entries
```

> **Note:** When importing modules individually, follow this module sequence for best results:

1. `locales`
2. `environments`
3. `assets`
4. `taxonomies`
5. `extensions`
6. `marketplace-apps`
7. `webhooks`
8. `global-fields`
9. `content-types`
10. `workflows`
11. `entries`
12. `labels`
13. `custom-roles`

**Using Backup Directory**

The `--backup-dir` flag is essential when repeatedly using the single module import command. Due to module inter-dependencies, the backup flag helps avoid import errors.

> **Note:** Asset scanning is rolling out as an org-plan feature. Once it is active for a stack's org plan, `--skip-assets-publish` is set automatically during import, in addition to being settable explicitly with the flag itself. When this happens, imported assets are not published, and a reminder is printed at the end of the import pointing to `csdx cm:assets:publish --backup-dir <BACKUP_DIR> --stack-api-key <STACK_API_KEY>` to publish them once scanning completes.

**First Import (Creates Backup):**

```
csdx cm:stacks:import -a production --data-dir ./export --module locales
# Backup directory is created automatically
```

**Subsequent Imports (Use Backup):**

```
# Import content types using backup directory
csdx cm:stacks:import -a production --data-dir ./export --module content-types --backup-dir ./export/_backup_1234567890
```

> **Note:** The parent backup folder created during the initial import can be reused for subsequent module imports. To ensure a smooth import process, always provide this backup folder when importing modules individually.

**Import with Overwrite**

**Replace Existing Module:**

```
csdx cm:stacks:import -a production --data-dir ./export --module content-types --replace-existing
```

**Skip Existing Module Warnings:**

```
csdx cm:stacks:import -a production --data-dir ./export --module content-types --skip-existing
```

**Import with Publishing Options**

**Skip Asset Publishing:**

```
csdx cm:stacks:import -a production --data-dir ./export --skip-assets-publish
```

**Skip Entry Publishing:**

```
csdx cm:stacks:import -a production --data-dir ./export --skip-entries-publish
```

**Skip Both:**

```
csdx cm:stacks:import -a production --data-dir ./export --skip-assets-publish --skip-entries-publish
```

> **Note:** `--skip-assets-publish` can also be set automatically rather than passed explicitly when asset scanning is active for a stack's org plan. See Using Backup Directory above for details and the post-scan publish command.

**Import Marketplace Apps**

**Import Marketplace Apps (Interactive):**

```
csdx cm:stacks:import -a production --data-dir ./export --module marketplace-apps
```

**Import Marketplace Apps (Skip Prompts):**

```
csdx cm:stacks:import -a production --data-dir ./export --module marketplace-apps -y
```

**Import with Webhook Status**

**Disable Webhooks (Default):**

```
csdx cm:stacks:import -a production --data-dir ./export --import-webhook-status disable
```

**Maintain Current Webhook State:**

```
csdx cm:stacks:import -a production --data-dir ./export --import-webhook-status current
```

**Import with Audit Options**

**Skip Audit Fix:**

```
csdx cm:stacks:import -a production --data-dir ./export --skip-audit
```

**Import with Audit (Default):**

```
csdx cm:stacks:import -a production --data-dir ./export
# Audit fix runs automatically
```

**Import Personalize Projects**

**Import with Custom Project Name:**

```
csdx cm:stacks:import -a production --data-dir ./export --module personalize --personalize-project-name my-project
```

## Using Configuration File

You can also import content using a configuration file. This is useful for:

- Reproducible imports
- CI/CD automation
- Complex import configurations
- Performance tuning

### Step 1: Download Configuration File

Download the example configuration file:

- [Authentication-based config](https://github.com/contentstack/cli/blob/db01c8a991988e6546e4188ffe3f6693048c7a89/packages/contentstack-import/example_config/auth_config.json)
- [Management token-based config](https://github.com/contentstack/cli/blob/db01c8a991988e6546e4188ffe3f6693048c7a89/packages/contentstack-import/example_config/management_config.json)

### Step 2: Configure Your Values

Edit the configuration file with your values:

**Example Configuration (auth_config.json):**

```
{
  "master_locale": {
    "name": "English - United States",
    "code": "en-us"
  },
  "data": "/path/to/export/directory",
  "target_stack": "blt1234567890abcdef",
  "branchName": "develop",
  "moduleName": "content-types",
  "concurrency": 1,
  "importConcurrency": 5,
  "fetchConcurrency": 5,
  "writeConcurrency": 5,
  "securedAssets": false,
  "developerHubBaseUrl": "",
  "createBackupDir": "./temp",
  "cliLogsPath": "./tmp",
  "maxContentLength": 100000000,
  "maxBodyLength": 100000000,
  "delayMs": 1000
}
```

**Example Configuration (management_config.json):**

```
{
  "master_locale": {
    "name": "English - United States",
    "code": "en-us"
  },
  "data": "/path/to/export/directory",
  "branchName": "develop",
  "moduleName": "content-types",
  "concurrency": 1,
  "importConcurrency": 5,
  "fetchConcurrency": 5,
  "writeConcurrency": 5,
  "securedAssets": false,
  "developerHubBaseUrl": "",
  "cliLogsPath": "./tmp",
  "maxContentLength": 100000000,
  "maxBodyLength": 100000000,
  "delayMs": 1000
}
```

### Step 3: Run Import with Config File

**Using Authentication:**

```
csdx cm:stacks:import -c /path/to/auth_config.json
```

**Using Management Token Alias:**

```
csdx cm:stacks:import -a production -c /path/to/management_config.json
```

**Example (macOS/Linux):**

```
csdx cm:stacks:import -a production -c "/Users/username/Desktop/config.json"
```

**Example (Windows):**

```
csdx cm:stacks:import -a production -c "C:\Users\Username\Desktop\config.json"
```

> **Note:**
>
> - macOS/Linux users must use `/` for paths in a JSON file.
> - Windows users must use `\\` (double backslashes) for paths in a JSON file.

### Configuration File Options

| Option | Description | Type | Default |
| --- | --- | --- | --- |
| `master_locale` | Master locale configuration. | object | - |
| `target_stack` | UID of the stack to which data must be imported. Required for auth-based config. | string | - |
| `data` | File path where the exported data is stored. | string | - |
| `branchName` | Name of the branch to import content into. | string | `main` |
| `branchAlias` | Alias of the branch to import content into. | string | - |
| `moduleName` | Module name to be imported. Options: `stack`, `assets`, `locales`, `environments`, `extensions`, `webhooks`, `global-fields`, `content-types`, `custom-roles`, `workflows`, `entries`, `labels`, `marketplace-apps`, `taxonomies`, `personalize`. | string | - |
| `concurrency` | General concurrency setting. | number | `1` |
| `importConcurrency` | Number of concurrent import operations. | number | `5` |
| `fetchConcurrency` | Number of files that must be fetched in one request. | number | `5` |
| `writeConcurrency` | Number of files that must be written in one request. | number | `5` |
| `securedAssets` | Import secured assets. | boolean | `false` |
| `developerHubBaseUrl` | Base URL for Developer Hub operations. | string | - |
| `createBackupDir` | Path for backup directory. | string | - |
| `cliLogsPath` | Path for CLI logs. | string | - |
| `maxContentLength` | Maximum content length in bytes. Default: 100 MB (100000000). | number | `100000000` |
| `maxBodyLength` | Maximum body length in bytes. Default: 100 MB (100000000). | number | `100000000` |
| `delayMs` | Delay in milliseconds between API requests to prevent concurrency issues. | number | `1000` |

## Import Content Using Management Token

You can import content to your stack using a [management token](/docs/headless-cms/cli-authentication/v1#add-management-token). This is the recommended approach for CI/CD environments.

### Basic Usage

**Import with Alias Only:**

```
csdx cm:stacks:import -a production
```

**Import with Alias and Data Directory:**

```
csdx cm:stacks:import -a production --data-dir ./export
```

**Import with Alias and Configuration File:**

```
csdx cm:stacks:import -a production -c /path/to/config.json
```

### Developer Example - CI/CD Integration

**GitHub Actions:**

```
- name: Import Contentstack Stack
  run: |
    csdx cm:stacks:import \
      -a ${{ secrets.MANAGEMENT_TOKEN_ALIAS }} \
      --data-dir ./export \
      --module entries \
      -y
```

**GitLab CI:**

```
import_stack:
  script:
    - csdx cm:stacks:import -a $MANAGEMENT_TOKEN_ALIAS --data-dir ./export -y
  artifacts:
    paths:
      - export/
```

## Module-wise Import

The `--module` flag in the import command allows module-specific imports into the target stack. Specify a module to import only that module. To import all modules, avoid using the flag.

**Available modules:**

- `assets`
- `content-types`
- `entries`
- `environments`
- `stacks`
- `extensions`
- `marketplace-apps`
- `global-fields`
- `labels`
- `locales`
- `webhooks`
- `workflows`
- `custom-roles`
- `taxonomies`
- `personalize`

> **Note:** Before importing a module, ensure its dependent modules are imported first. When importing individually, follow this sequence:

1. `locales`
2. `environments`
3. `assets`
4. `taxonomies`
5. `extensions`
6. `marketplace-apps`
7. `webhooks`
8. `global-fields`
9. `content-types`
10. `workflows`
11. `entries`
12. `labels`
13. `custom-roles`

For example, before importing entries, you must first import locales, environments, assets, taxonomies, extensions, marketplace-apps, webhooks, global-fields, content-types, and workflows.

## Import Overwrite Feature

The Overwrite feature in the import command enhances the import process by allowing you to seamlessly update the existing content within a stack. By using this feature, you can prevent an import failure if an imported module already exists in the target stack.

**Use** `--replace-existing` **flag:**

```
csdx cm:stacks:import -a production --data-dir ./export --module content-types --replace-existing
```

Learn more in the [Overwrite Existing Content using CLI Import](/docs/headless-cms/overwrite-existing-content-using-cli-import/v1) guide.

## Toggle Between Console Logs and Progress Manager View

Contentstack CLI lets you toggle between the raw console logs and the visual Progress Manager UI during import workflows.

### Default Mode (Progress Manager UI)

By default, the Progress Manager UI displays when you run the import command:

```
csdx cm:stacks:import -a production --data-dir ./export
```

**Example Output:**

```
LOCALES:
   ├─ Master Locale        |████████████████████████████████████████| 100% | 1/1 | ✓ Complete (1/1)
   ├─ Locales Create       |████████████████████████████████████████| 100% | 1/1 | ✓ Complete (0/1)
   ├─ Locales Update       |████████████████████████████████████████| 100% | 1/1 | ✓ Complete (1/1)

ENVIRONMENTS:
    └─ Environments        |████████████████████████████████████████| 100% | 2/2 | ✓ Complete (2/2)

STACK:
    └─ Stack               |████████████████████████████████████████| 100% | 1/1 | ✓ Complete (1/1)

ASSETS:
   ├─ Folders              |████████████████████████████████████████| 100% | 2/2 | ✓ Complete (2/2)
   ├─ Upload               |████████████████████████████████████████| 100% | 12/12 | ✓ Complete (12/12)
   ├─ Publish              |████████████████████████████████████████| 100% | 12/12 | ✓ Complete (12/12)
```

### Console Log Mode

**Step 1: Enable Console Logs**

```
csdx config:set:log --show-console-logs
```

**Step 2: Run Import Command**

```
csdx cm:stacks:import -a production --data-dir ./export
```

**Example Output:**

```
[2025-09-10 19:19:02] INFO: Audit process completed
[2025-09-10 19:19:03] INFO: Starting to import content version 2
[2025-09-10 19:19:03] INFO: Starting import of locales module
[2025-09-10 19:19:05] INFO: Created locale: 'fr-fr'
[2025-09-10 19:19:07] INFO: Updated locale: 'fr-fr'
[2025-09-10 19:19:07] SUCCESS: Languages have been imported successfully!
[2025-09-10 19:19:07] INFO: Starting import of environments module
```

**Step 3: Switch Back to Default Mode**

```
csdx config:set:log --no-show-console-logs
```

> **Tip:** Use `--show-console-logs` for detailed debugging when troubleshooting import issues.

## Common Import Scenarios

### Scenario 1: Full Stack Import

Import all modules from an export for migration or backup restoration:

```
csdx cm:stacks:import -a production --data-dir ./full-export
```

### Scenario 2: Selective Module Import

Import only specific modules:

```
# Import content types first
csdx cm:stacks:import -a production --data-dir ./export --module content-types

# Then import entries
csdx cm:stacks:import -a production --data-dir ./export --module entries --backup-dir ./export/_backup_1234567890
```

### Scenario 3: Branch-Specific Import

Import content to a development branch:

```
csdx cm:stacks:import -a production --data-dir ./export --branch develop
```

### Scenario 4: Import with Overwrite

Replace existing content in target stack:

```
csdx cm:stacks:import -a production --data-dir ./export --module content-types --replace-existing
```

### Scenario 5: Import Without Publishing

Import content without automatically publishing:

```
csdx cm:stacks:import -a production --data-dir ./export --skip-assets-publish --skip-entries-publish
```

### Scenario 6: High-Performance Import

Use configuration file with optimized concurrency settings:

```
{
  "importConcurrency": 10,
  "fetchConcurrency": 10,
  "writeConcurrency": 10,
  "delayMs": 500,
  "data": "/path/to/export"
}
```

```
csdx cm:stacks:import -a production -c ./high-performance-config.json
```

## Examples

**Import all modules to a stack:**

```
csdx cm:stacks:import -a <alias> --data-dir ./export
```

**Import specific module:**

```
csdx cm:stacks:import -a <alias> --data-dir ./export --module content-types
```

**Import to specific branch:**

```
csdx cm:stacks:import -a <alias> --data-dir ./export --branch develop
```

## Troubleshooting

For troubleshooting import issues, see the CLI Troubleshooting Guide.

## Limitations

For comprehensive information about import limitations, see the [CLI Limitations Guide](/docs/headless-cms/cli-limitations/v1#import-module-limitations).

## Best Practices

For best practices on import workflows, see the CLI Best Practices Guide.

## Next Steps

After successful import:

- [Export content](/docs/headless-cms/export-content-using-the-cli/v1)
- Clone a stack
- [Migrate content](/docs/headless-cms/migrate-content-between-stacks-using-the-cli/v1)
- [Overwrite existing content](/docs/headless-cms/overwrite-existing-content-using-cli-import/v1)
- [Asset Scanning in CLI](/docs/headless-cms/asset-scanning-in-cli/v1): asset-scan gating behavior during import, including the automatic `--skip-assets-publish` trigger and the post-scan publish command.
