---
uid: "blt1215a1f9bbcc9900"
seo_title: "Import Content Using the CLI | V2.x.x | Contentstack"
seo_description: "Import content efficiently with Contentstack’s latest Command-line Interface commands to streamline data onboarding and content setup."
---

# Import Content Using the CLI

## Overview

After [exporting content](/docs/headless-cms/export-content-using-the-cli) from a source stack, unzip the exported file and then use the Contentstack CLI to import it into the destination stack.

This guide covers how to use the `cm:stacks:import` command with:

- Authentication via CLI login or a management token
- Content import using a configuration file or CLI parameters

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli)
- CLI [authenticated](/docs/headless-cms/cli-authentication#login)
- [Configured management token](/docs/headless-cms/cli-authentication#add-management-token) *(optional)*
- [Exported](/docs/headless-cms/export-content-using-the-cli) content extracted (unzipped) in a local folder

## Supported Modules

- [Assets](/docs/headless-cms/about-assets/)
- [Locales](/docs/headless-cms/about-languages/)
- [Environments](/docs/headless-cms/about-environments/)
- [Stacks](/docs/headless-cms/about-stack) *(CLI supports Stacks from v1.43.0)*
- [Extensions](/docs/developer-hub/about-ui-locations)
- [Marketplace Apps](/docs/marketplace/about-marketplace/)
- [Webhooks](/docs/headless-cms/about-webhooks/)
- [Global Fields](/docs/headless-cms/about-global-field/) *(CLI supports* [*Nested Global Fields*](/docs/headless-cms/about-global-field#nested-global-fields) *from v1.42.0)*
- [Content Types](/docs/headless-cms/about-content-types/)
- [Entries](/docs/headless-cms/about-entries/)
- [Labels](/docs/headless-cms/about-labels/)
- [Workflows](/docs/headless-cms/about-workflows/)
- [Custom Roles](/docs/headless-cms/types-of-roles#custom-role)
- [Taxonomies](/docs/headless-cms/about-taxonomy)
- [Personalize](/docs/personalize/about-personalize)
- [Studio](/docs/studio/about-studio)

> **Note:** Imported content gets published to the same environment and locale as in the source stack. Unpublished content in the source stack remains unpublished after import.

## Commands

The `cm:stacks:import` command lets you import content into your destination stack.

> **Note:** By default, an [audit fix](/docs/headless-cms/cli-audit-plugin) is performed on the exported content before import. This helps identify and address potential issues in the exported data.

**Usage**

```
csdx cm:stacks:import -k <<stack_ApiKey>> --data-dir <<path_of_folder_where_content_is_stored>>
```

## Options

Use the following options with any applicable import command:

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--config` | `-c` | \[Optional\] Path to the configuration JSON file containing all options for a single run. |
| `--stack-api-key` | `-k` | API key of the target stack. |
| `--data-dir` | - | Path in your file system where the content to be imported is stored.<br>Example: `--data-dir "C:\Users\Name\Desktop\cli\content"`<br>Point this at the export folder itself. The export writes content flat, with no per-branch subfolder, so the same path works for both the export and the import. |
| `--alias` | `-a` | Management token alias of the destination stack. |
| `--module` | - | \[Optional\] Specify a module to import into the target stack.<br>If not specified, all modules are imported.<br>Supported values: `stack`, `assets`, `locales`, `environments`, `extensions`, `webhooks`, `global-fields`, `entries`, `content-types`, `custom-roles`, `workflows`, `publishing-rules`, `labels`, `marketplace-apps`, `taxonomies`, `personalize`, `variant-entries`, `composable-studio`<br>The CLI validates this value before the import starts and fails immediately if the module name is not in the list above. |
| `--backup-dir` | - | \[Optional\] Backup directory name when importing a specific module. |
| `--branch` | - | Name of the branch into which content is imported.<br>Default: `main` |
| `--branch-alias` | - | Alias of the branch into which content is imported. |
| `--import-webhook-status` | - | \[Optional\] Maintain webhook state configuration from the source stack.<br>Supported values: `disable`, `current`<br>Default: `disable` |
| `--yes` | `-y` | \[Optional\] Force override all Marketplace prompts. |
| `--replace-existing` | - | Replaces the existing module in the target stack. |
| `--skip-existing` | - | \[Optional\] Skips the module exists warning messages. |
| `--personalize-project-name` | - | \[Optional\] Provide a unique name for the Personalize project. |
| `--skip-audit` | - | Skips the audit fix that occurs during the import operation. |
| `--exclude-global-modules` | - | Excludes branch-independent modules from the import operation. |
| `--skip-assets-publish` | - | Skips asset publishing during the import process. |
| `--skip-entries-publish` | - | Skips entry publishing during the import process. |
| `--skip-taxonomy-publish` | - | Skips taxonomy publishing during the import process. |

> **Note:**
>
> - If you do not use the `--yes` flag during import:
>   - You’ll be prompted to enter an encryption key for Marketplace App configurations.
>   - You have three attempts to enter the correct key. After three failed attempts, the import process stops and must be restarted from the beginning.
>
> - If you don’t use the `--skip-audit` flag during import:
>   - The audit step removes all workflow branches except the one you're importing into.
>   - For example, if your source stack includes *main*, *development*, and *production*, and you import into *development*, the audit deletes the *main* and *production* branches from the workflow module.

## Module-wise Import

Use the `--module` flag in the `import` command to import individual modules into the target stack. If you do not use the flag, the `import` command includes all [available modules](/docs/headless-cms/import-content-using-the-cli#supported-modules) by default.

### Importing an Export Produced by an Older CLI Version

Two behaviours differ when the folder you pass to `--data-dir` was produced by CLI V1 rather than V2. Both fail quietly, so check for them before you rely on the result.

> **Warning:** Importing a V1 export skips every global field, with no error and no warning. The global fields step reports success having created zero items.

The cause is a change in file layout. The V2 importer reads one file per UID and ignores the aggregate files that V1 wrote:

| Module | A V1 export writes | The V2 importer reads | Result |
| --- | --- | --- | --- |
| Content types | Individual `<uid>.json` files and `schema.json` | Per-UID files only | Imports correctly, because the per-UID files exist |
| Global fields | `globalfields.json` only, with no individual files | Per-UID files only | Silently skipped, because no per-UID files exist |

To resolve it, re-export the source stack with the current CLI before importing.

The second difference affects multi-branch V1 exports. V1 wrote a `branches.json` file at the export root and the V1 importer used it to navigate into the correct branch subfolder automatically. The current importer does not do this. Point `--data-dir` at the branch subfolder yourself:

```
csdx cm:stacks:import --stack-api-key bltxxxxxx --data-dir ./my-v1-export/main
```

Pointing it at the export root instead finds no content files there, and the command completes and reports success having imported nothing.

### Dependency Order

Some modules depend on others. When importing modules individually, follow this sequence to avoid errors:

Locales → Environments → Assets → Taxonomies → Extensions → Marketplace Apps → Webhooks → Global Fields → Content Types → Workflows → Entries → Labels → Custom Roles → Publishing Rules → Personalize → Composable Studio.

> **Note:** Before importing a module, ensure all its dependencies have been imported.

**Example**:

- To import only `locales`:

  ```
  csdx cm:stacks:import --stack-api-key bltxxxxxx --data-dir "C:\Users\Name\Desktop\cli\content" --module locales
  ```

### Use of --backup-dir Flag

When importing modules individually with the `import` command, include the `--backup-dir` flag to prevent errors caused by inter-module dependencies. This flag stores mapping files that are required by dependent modules in future imports.

```
csdx cm:stacks:import --stack-api-key <<stack_ApiKey>> --data-dir <<path_of_folder_where_content_is_stored>> --module <<module>> --backup-dir <<backup_dir>>
```

During each module import, the system saves updated mapping files in the specified backup folder. These mappings are reused by dependent modules to ensure consistent and successful imports.

> **Note:** The parent backup folder created during the initial import can be reused for subsequent module imports. To avoid errors, always include the `--backup-dir` flag when importing modules one at a time.

**Examples**

- To import assets into a stack:
  `csdx cm:stacks:import --stack-api-key bltxxxxxx --data-dir "C:\Users\Name\Desktop\cli\content" --module assets`
- To import entries into a stack with backup mapping:
  `csdx cm:stacks:import --stack-api-key bltxxxxxx --data-dir "C:\Users\Name\Desktop\cli\content" --module entries --backup-dir <backup_dir>`

## Using Configuration File

You can also import content using a configuration file that stores all required parameters and values.

To get started, follow the steps below:

- Download the [configuration file](https://github.com/contentstack/cli-plugins/blob/main/packages/contentstack-export/example_config/auth_config.json).
- Add your values.
- Save the file and note its path.

**Usage**

```
csdx cm:stacks:import -c <<config_file_path>>
```

**Example**

- To import content using a configuration file:
  `csdx cm:stacks:import -c "C:\Users\Name\Desktop\cli\config.json"`

> **Note:**
>
> - Mac OS users must use `\` for paths in a JSON file.
> - Windows OS users must use `\\` for paths in a JSON file.

Using a configuration file simplifies the import process by storing all required parameters and values in one place. This removes the need to enter each option manually and is helpful for repeated or complex imports.

## Import Content Using Management Token

Use a [management token](/docs/headless-cms/cli-authentication#token-management) to import content into a stack when you prefer token-based authentication instead of CLI login. You can pass the token directly through the command line or reference it from a [configuration file](https://github.com/contentstack/cli-plugins/blob/main/packages/contentstack-import/example_config/management_config.json).

**Usage**

```
csdx cm:stacks:import -a <<alias>>
```

**Optional Parameters:**

- `--data-dir <path_of_folder_where_content_is_stored>`: Specify the folder where the content is located.
- `-c <config_file_path>`: Use a configuration file that contains all import parameters.

**Examples:**

- **To import content from a specific folder:**
  `csdx cm:stacks:import --alias mytoken --data-dir "C:\Users\Name\Desktop\cli\import-folder"`
- **To import content using a configuration file:**
  `csdx cm:stacks:import --alias mytoken -c "C:\Users\Name\Desktop\cli\config.json"`

## Import Overwrite Feature

Use the `--replace-existing` flag in the import command to **overwrite** the existing content in the target stack. This prevents import failures caused by module collisions and ensures that existing items are overwritten while new items are added.

When the import process detects a module that already exists in the target stack, the CLI replaces it instead of throwing an error. If the module does not exist, the CLI creates it as a new item.

**Example:**

```
csdx cm:stacks:import --replace-existing --backup-dir <backup-dir-path> --stack-api-key <value> --data-dir <content-dir-path>
```

For more details, refer [Overwrite Existing Content using CLI Import](/docs/headless-cms/overwrite-existing-content-using-cli-import) document.

## Toggle Between Console Logs and Progress Manager View (2.x.x-beta)

Contentstack CLI lets you toggle between the raw console logs and the visual Progress Manager UI during import or plugin workflows.

**Default Usage:**

```
csdx cm:stacks:import --data-dir "./export-data" --stack-api-key bltxxxxxx
```

> **Note:** By default, the Progress Manager UI displays when you run the `import` command and does not require any configuration.

**Example for Progress Manager View (Default Mode):**

```
LOCALES:
   ├─ Master Locale        |████████████████████████████████████████| 100% | 1/1 | ✓ Complete (1/1)
   ├─ Locales Create       |████████████████████████████████████████| 100% | 1/1 | ✓ Complete (0/1)
   ├─ Locales Update       |████████████████████████████████████████| 100% | 1/1 | ✓ Complete (1/1)

ENVIRONMENTS:
    └─ Environments        |████████████████████████████████████████| 100% | 2/2 | ✓ Complete (2/2)

STACK:
    └─ Stack               |██��█████████████████████████████████████| 100% | 1/1 | ✓ Complete (1/1)

ASSETS:
   ├─ Folders              |████████████████████████████████████████| 100% | 2/2 | ✓ Complete (2/2)
   ├─ Upload               |████████████████████████████████████████| 100% | 12/12 | ✓ Complete (12/12)
   ├─ Publish              |████████████████████████████████████████| 100% | 12/12 | ✓ Complete (12/12)

TAXONOMIES:
    └─ Taxonomies          |████████████████████████████████████████| 100% | 1/1 | ✓ Complete (1/1)

EXTENSIONS:
   ├─ Extensions Create    |████████████████████████████████████████| 100% | 1/1 | ✓ Complete (1/1)
```

**Steps to Switch to Console Logs (Optional):**

1. Run the following command to switch to console log mode:

   ```
   csdx config:set:log --show-console-logs
   ```

2. Run the import command:

   ```
   csdx cm:stacks:import --data-dir "./export-data" --stack-api-key bltxxxxxx
   ```

   The screen displays the console logs for the import operation.

   > **Tip:** Use `--show-console-logs` for detailed debugging when troubleshooting import issues.

3. Run the following command to switch back to default mode:

   ```
   csdx config:set:log --no-show-console-logs
   ```

**Options:**

**Options for `config:set:log`:**

| Option | Description |
| --- | --- |
| `--show-console-logs` | Displays the console logs for the operation. |
| `--no-show-console-logs` | Hides the console logs and displays the Progress Manager view for the operation. |

**Example for Console Log Mode:**

```
[2025-09-10 19:19:02] INFO: Audit process completed
[2025-09-10 19:19:03] INFO: Starting to import content version 2
[2025-09-10 19:19:03] INFO: Starting import of locales module
[2025-09-10 19:19:05] INFO: Created locale: 'fr-fr'
[2025-09-10 19:19:07] INFO: Updated locale: 'fr-fr'
[2025-09-10 19:19:07] SUCCESS: Languages have been imported successfully!
[2025-09-10 19:19:07] INFO: Starting import of environments module
```

## Limitations

- Only the **latest version** of published entries or assets is imported.

- Workflow imports do not include admins or workflow stage users.

- To resolve `maxContentLength` and `maxBodyLength` errors, include these parameters in the configuration JSON with values in bytes. The default limit is **100MB**. For implementation details, refer to the [example configuration file](https://github.com/contentstack/cli-plugins/blob/main/packages/contentstack-export/example_config/management_config.json).

- To manage API request timing and prevent concurrency issues, add the `delayMs` parameter to your configuration JSON.
  **Example:** `delayMs: 1000` (adds a 1-second delay between API requests).

- The following modules cannot be imported through CLI:
  - [Users](/docs/headless-cms/about-stack-users/)
  - [Releases](/docs/headless-cms/about-releases/)

> **Additional Resource:** Learn more about the CLI-supported import operations in the [Support for CLI-Based Stack Import Operations](/docs/headless-cms/cli-supported-features-for-export-import-and-clone-operations#importing) document.

## Next Steps

- [Export Content Using the CLI](/docs/headless-cms/export-content-using-the-cli): export stack content to disk before importing it elsewhere.
- [Audit Plugin](/docs/headless-cms/cli-audit-plugin): audit exported data for reference and field problems before importing it.
- [Overwrite Existing Content using CLI Import](/docs/headless-cms/overwrite-existing-content-using-cli-import): overwrite existing entries and assets during an import.
- [CLI-Supported Features for Export, Import, and Clone Operations](/docs/headless-cms/cli-supported-features-for-export-import-and-clone-operations): which modules export, import and clone cover, module by module.
