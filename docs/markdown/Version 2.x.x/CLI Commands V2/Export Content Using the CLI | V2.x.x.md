---
uid: "blt2fe395869b399af0"
seo_title: "Export Content Using the CLI | V2.x.x | Contentstack"
seo_description: "Export content efficiently with Contentstack’s latest Command-line Interface commands to simplify data migration and content backup."
---

# Export Content Using the CLI

## Overview

To migrate content from one [stack](/docs/headless-cms/about-stack) to another, begin by exporting content from the source stack, then import it into the destination stack.

This guide explains how to use the `cm:stacks:export` command by logging in to the CLI (or using a management token), using configuration files, or using direct CLI parameters.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli)
- CLI [authenticated](/docs/headless-cms/cli-authentication#login)
- [Configured management token](/docs/headless-cms/cli-authentication#add-management-token) (alias) *(optional)*

## Supported Modules

- [Assets](/docs/headless-cms/about-assets/)
- [Locales](/docs/headless-cms/about-languages/)
- [Environments](/docs/headless-cms/about-environments/)
- [Stacks](/docs/headless-cms/about-stack) *(CLI supports Stacks from v1.42.0)*
- [Extensions](/docs/developer-hub/about-ui-locations)
- [Marketplace](/docs/marketplace/about-marketplace/) Apps
- [Webhooks](/docs/headless-cms/about-webhooks/)
- [Global Fields](/docs/headless-cms/about-global-field/) *(CLI supports* [*Nested Global Fields*](/docs/headless-cms/about-global-field#nested-global-fields) *from v1.42.0)*
- [Content Types](/docs/headless-cms/about-content-types/)
- [Entries](/docs/headless-cms/about-entries/)
- [Labels](/docs/headless-cms/about-labels/)
- [Workflow](/docs/headless-cms/about-workflows/)
- [Custom Role](/docs/headless-cms/types-of-roles#custom-role)
- [Taxonomy](/docs/headless-cms/about-taxonomy)
- [Personalize](/docs/personalize/about-personalize)
- [Studio](/docs/studio/about-studio)

## Commands

The `cm:stacks:export` command lets you export content from one stack to another.

**Usage**

```
csdx cm:stacks:export -k <<stack_ApiKey>> --data-dir <<file_path>>
```

**Options**

Use the following options with any applicable export command:

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--stack-api-key=stack-api-key` | `-k` | API key of the source stack. |
| `--alias=alias` | `-a` | Management token alias of the source stack. |
| `--data-dir=data-dir` | - | Absolute path to the folder where exported content is stored. |
| `--branch=branch` | - | Name of the branch from which content is exported.<br>Default: `main`<br>If not specified, content is exported from the `main` branch only. If the stack has no branch named `main`, the command fails. |
| `--branch-alias=branch-alias` |  | Alias of the branch from which content is exported. |
| `--module=module` | - | \[Optional\] Export a specific module from the source stack.<br>If not specified, all modules are exported.<br>Available modules: `stack`, `assets`, `locales`, `environments`, `extensions`, `webhooks`, `global-fields`, `entries`, `content-types`, `custom-roles`, `workflows`, `publishing-rules`, `labels`, `marketplace-apps`, `taxonomies`, `personalize`, `composable-studio`<br>The CLI validates this value before the export starts and fails immediately if the module name is not in the list above. |
| `--content-types=content-types` | - | \[Optional\] UID of the content type(s whose content should be exported.<br>For multiple content types, separate IDs using spaces. |
| `--secured-assets=secured-assets` | - | \[Optional\] Required if the secured assets feature is enabled for the stack.<br>Ensure this flag is included when exporting secured assets. |
| `--yes` | `-y` | Force override all Marketplace prompts.<br>If not provided, you are prompted to enter an encryption key while exporting Marketplace app configurations. |
| `--config=config` | `-c` | Path to the configuration JSON file containing all options for a single run. |

**Examples**

- To export all modules from a stack:

  ```
  csdx cm:stacks:export --data-dir "C:\Users\Name\Desktop\cli\content" -k bltxxxxxx
  ```

- To export all modules from a specific branch (e.g., develop):

  ```
  csdx cm:stacks:export --data-dir "C:\Users\Name\Desktop\cli\content" -k bltxxxxxx --branch develop
  ```

- To export all modules from a branch using an alias:

  ```
  csdx cm:stacks:export --data-dir "C:\Users\Name\Desktop\cli\content" -k bltxxxxxx --branch-alias developAlias
  ```

- To export only content types:

  ```
  csdx cm:stacks:export --data-dir "C:\Users\Name\Desktop\cli\content" --module content-types -k bltxxxxxx
  ```

> **Note:** When exporting modules individually, follow this module sequence:
>
> assets → environments → stack → locales → extensions → marketplace-apps → webhooks → taxonomies → global-fields → content-types → workflows → entries → labels → custom-roles → publishing-rules → personalize → composable-studio
>
> For example, before exporting entries, you must have already exported assets, environments, stacks, locales, extensions, marketplace-apps, webhooks, taxonomies, global-fields, content-types, and workflows.

### Export Output Structure

The export writes content directly into the folder you pass to `--data-dir`.

> **Warning:** The export never creates a per-branch subfolder. Exporting two branches into the same `--data-dir` overwrites the first export with the second, and no error is raised. Use a separate `--data-dir` for each branch.

```
csdx cm:stacks:export --branch main --data-dir ./export-main --stack-api-key bltxxxxxx
csdx cm:stacks:export --branch feature-x --data-dir ./export-feature --stack-api-key bltxxxxxx
```

Content types and global fields are each written as one file per UID:

```
export/content_types/blog.json
export/content_types/author.json
export/global_fields/my_header.json
export/global_fields/my_footer.json
```

Four files that earlier versions of the CLI wrote are no longer produced:

| File | Status |
| --- | --- |
| `content_types/schema.json` | Not written. Read the individual `content_types/<uid>.json` files instead. |
| `global_fields/globalfields.json` | Not written. Read the individual `global_fields/<uid>.json` files instead. |
| `branches.json` | Not written. The export no longer records the branch list at the export root. |
| `export-info.json` | Not written. Any pipeline step that reads `contentVersion` from this file needs to be removed. |

If a script or pipeline reads any of these files, it fails on an export produced by this version of the CLI, because the files do not exist.

### Using Configuration File

You can also export content using a configuration file.

To get started, follow the steps below:

- Download the [configuration file](https://github.com/contentstack/cli-plugins/blob/main/packages/contentstack-export/example_config/auth_config.json).
- Add your values.
- Note the path where the file is saved.

**Usage**

```
csdx cm:stacks:export -c <<config_file_path>>
```

**Example**

- To export content using a configuration file:

  ```
  csdx cm:stacks:export -c "C:\Users\Name\Desktop\cli\config.json"
  ```

> **Note:**
>
> - Mac OS users must use "/" for paths in a JSON file.
> - Windows OS users must use "\\\\" for paths in a JSON file.

**Configuration File Options**

The following are the possible file options in the [configuration file](https://github.com/contentstack/cli-plugins/blob/main/packages/contentstack-export/example_config/auth_config.json):

| Configuration File Option | Options | Description |
| --- | --- | --- |
| `versioning` | `true`, `false` | Exports versioned entries. |
| `host` | `Any valid CMA base URL` | Sets the host for the export operation. |
| `preserveStackVersion` | `true`, `false` | Preserves the stack version while exporting data. |
| `fetchConcurrency` | `Any natural number` | Specifies the number of files to fetch per request. |
| `writeConcurrency` | `Any natural number` | Specifies the number of files to write per request. |
| `source_stack` | `<stack_uid>` | UID of the stack from which data is exported. |
| `data` | `<path-where-data-is-stored>` | File path where the exported data is stored. |
| `branchName` | `<branch-name>` | Name of the branch to export data from. |
| `branchAlias` | - | Alias of the branch to export data from. |
| `moduleName` | `stack`, `assets`, `locales`, `environments`, `extensions`, `webhooks`, `global-fields`, `content-types`, `custom-roles`, `workflows`, `entries`, `labels`, `marketplace-apps` | Specifies the module to export. |
| `securedAssets` | `true`, `false` | Fetches only secured assets. |

## Export Content Using Management Token

You can also export content from your stack using a [management token](/docs/headless-cms/cli-authentication#token-management).

**Usage**

```
csdx cm:stacks:export -a <<alias>>
```

Alternatively, refer to the following command to add several parameters or options in a single line:

```
csdx cm:stacks:export -a <<alias>> --data-dir <<file_path>>
```

You can also **export content by using a management token and a** [**configuration file**](https://github.com/contentstack/cli-plugins/blob/main/packages/contentstack-export/example_config/management_config.json) that contains the parameters or options and the associated values.

By doing so, you don’t need to separately provide parameters or options in the command.

**Usage**

```
csdx cm:stacks:export -a <<alias>> -c <<config_file_path>>
```

**Example**

- To export content using a configuration file:

  ```
  csdx cm:stacks:export -a mytoken -c "C:\Users\Name\Desktop\cli\config.json"
  ```

## Toggle Between Console Logs and Progress Manager View (2.x.x-beta)

Contentstack CLI lets you toggle between the raw console logs and the visual Progress Manager UI during export or plugin workflows.

**Default Usage:**

```
csdx cm:stacks:export --data-dir "./export-data" -k bltxxxxxx
```

> **Note:** By default, the Progress Manager UI displays when you run the `export` command and does not require any configuration.

**Example for Progress Manager View (Default Mode):**

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

**Steps to Switch to Console Logs (Optional):**

1. Run the following command to switch to console log mode:

   ```
   csdx config:set:log --show-console-logs
   ```

2. Run the export command:

   ```
   csdx cm:stacks:export --data-dir "./export-data" -k bltxxxxxx
   ```

   The screen displays the console logs for the export operation.

   > **Tip:** Use `--show-console-logs` for detailed debugging when troubleshooting export issues.

3. Run the following command to switch back to default mode:

   ```
   csdx config:set:log --no-show-console-logs
   ```

**Options:**

- `--show-console-logs`: Displays the console logs for the operation.
- `--no-show-console-logs`: Hides the console logs and displays the Progress Manager view.

**Example for Console Log Mode:**

```
[2025-08-22 16:12:23] INFO: Exporting content from branch main
[2025-08-22 16:12:23] INFO: Started to export content, version is 2
[2025-08-22 16:12:23] INFO: Exporting module: stack
[2025-08-22 16:12:24] INFO: Exporting stack settings
[2025-08-22 16:12:25] SUCCESS: Exported stack settings successfully!
```

## Examples

Export an entire stack to a directory, authenticating with a management token alias.

```
csdx cm:stacks:export --alias <MANAGEMENT_TOKEN_ALIAS> --data-dir <EXPORT_PATH>
```

Export a single module rather than the whole stack.

```
csdx cm:stacks:export --stack-api-key <STACK_API_KEY> --data-dir <EXPORT_PATH> --module content-types
```

Export named content types from a specific branch, and skip the Marketplace prompts so the command can run unattended.

```
csdx cm:stacks:export --alias <MANAGEMENT_TOKEN_ALIAS> --data-dir <EXPORT_PATH> --branch <BRANCH_NAME> --content-types blog_post author --yes
```

## Limitations

- If multiple assets have the same UID and file name, only the first asset will be exported.

- To resolve the `maxContentLength` and `maxBodyLength` errors, include these parameters in the configuration JSON with values specified in bytes. The default limit is **100MB**. For implementation details, refer to the [example configuration file](https://github.com/contentstack/cli-plugins/blob/main/packages/contentstack-export/example_config/management_config.json).

- To manage API request timing and prevent concurrency issues, add the `delayMs` parameter to your configuration file.

  For example, use `delayMs: 1000` (for a 1-second delay).

- Currently, only the latest version of entries and assets is exported.

- Currently, the following modules cannot be exported:
  - [Users](/docs/headless-cms/about-stack-users/)
  - [Releases](/docs/headless-cms/about-releases/)

**Additional Resource:** Learn more about the CLI-supported export operations in the [CLI-Supported Features for Export, Import, and Clone Operations](/docs/headless-cms/cli-supported-features-for-export-import-and-clone-operations) document.
