---
uid: "bltd28635508877b2ec"
seo_title: "Overwrite Existing Content using CLI Import | V2.x.x | Contentstack"
seo_description: "Learn how to overwrite existing content using the CLI Import Overwrite feature."
---

# Overwrite Existing Content using CLI Import

## Overview

The Import Overwrite feature in Contentstack CLI facilitates seamless stack-to-stack migration by enabling updates to existing content and adding new entries for unmatched content during imports. This ensures that the import process continues smoothly, even if an imported module already exists in the target stack, effectively preventing import failures.

By providing the ability to overwrite content, this feature streamlines content migration and eliminates the need for manual adjustments, saving time and effort during the import process.

**Supported Modules**

- [Extensions](/docs/developer-hub/about-ui-locations)
- [Global Fields](/docs/headless-cms/global)
- [Content Types](/docs/headless-cms/about-content-types)
- [Entries](/docs/headless-cms/about-entries)

**Usage**

```
csdx cm:stacks:import --replace-existing --backup-dir <backup-dir-path> -k <value> --data-dir <content-dir-path>
```

**Options**

- `-d, --data-dir=data-dir`: Path to the directory containing exported content.
- `-k, --stack-api-key=stack-api-key`: API key of the target stack where the content will be imported.
- `-b, branch=branch`: \[optional\] Branch name of the target stack.
- `-a, alias=alias`: \[optional\] Alias (name) for the management token.
- `--replace-existing`: Replaces the existing module in the target stack.
- `--skip-existing`: Skips the *module exists* warning messages.
- `--backup-dir=backup-dir`: Path to the backup directory.
- `--module=module`: \[optional\] Specify the module to import into the target stack. If not specified, the import command will import all the modules into the stack. The available modules are *content-types, entries, environments, extensions, marketplace-apps, global-fields, labels, locales, webhooks, workflows, custom-roles,* and *taxonomies*.

## Steps for Execution

Follow the steps below to perform the overwrite operation on your target stack:

1. Update the source stack modules that support the overwrite feature.

2. Export the content of your source stack using the CLI export command.

3. Import the content to your target stack using the CLI import command with the `--replace-existing` flag.
   1. Import all modules (It will replace modules which are supported by the Overwrite feature).

      ```
      csdx cm:stacks:import --replace-existing --backup-dir <backup-dir-path> -k <value> --data-dir <content-dir-path>
      ```

   2. [Overwrite specific modules](#overwrite-specific-modules) using the `import-setup` command.

### Overwrite Specific Modules

The Import Setup command is an enhancement to the Import Overwrite feature, designed to address the challenges of dependency handling during imports. Updating specific modules—such as entries—often requires importing all dependent modules (e.g., extensions, assets) first, making the process more complex and time-consuming.

To resolve this, Contentstack CLI introduces the `cm:stacks:import-setup` pre-command, which:

- Generates essential mappers to streamline the import process.
- Creates a backup folder tailored to user-defined requirements.

By using these mappers with the import command, users can perform targeted imports without importing all dependencies. This enhancement simplifies dependency handling, providing greater flexibility and efficiency when using the Import Overwrite feature.

The `cm:stacks:import-setup` command is designed to simplify the import process by creating necessary mappers and backups for selected modules.

> **Note:**
>
> - Before using the `import-setup` command, make sure you have successfully [exported](/docs/headless-cms/export-content-using-the-cli) and unzipped the exported content located within the corresponding folder.
> - After using the `import-setup` command, a **backup directory will be generated** with the required mapper files. This **directory’s path** will be provided in the import command’s `--backup-dir` flag during the overwrite operation.

**Usage**

```
cm:stacks:import-setup --module module-name1 module-name2 --data-dir <exported-content-dir> -k <target-stack-api-key> --branch <branch>
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--stack-api-key` | `-k` | API key of the target stack where the content will be imported. |
| `--data-dir` | - | The path or location in your file system where the content to be imported is stored. |
| `--alias` | `-a` | \[Optional\] Alias (name) of the management token for the destination stack. |
| `--module` | - | \[Optional\] Specify the module(s) to import into the target stack.<br>Supported values: `global-fields`, `content-types`, `entries` |
| `--branch` |  | \[Optional\] Name of the branch where you want to import your content. |
| `--branch-alias` | - | \[Optional\] Alias of the target stack branch where you want to import your content. |
| `--config` | `-c` | \[optional\] Path of the configuration JSON file. |
| `--backup-dir` | - | \[optional\] Backup directory name when using a specific module. |
| `--import-webhook-status` | - | (optional) Status of the import webhook (disable / current). |
| `--yes` | `-y` | \[optional\] Force override all Marketplace prompts. |
| `--replace-existing` | - | Replaces the existing module in the target stack. |
| `--skip-existing` | - | Skips the module exists warning messages. |
| `--personalize-project-name` | - | (optional) Unique name for the Personalize project. |
| `--skip-audit` | - | Skips the audit fix during an import operation. |
| `--exclude-global-modules` | - | Excludes branch-independent modules from the import operation. |
| `--skip-assets-publish` | - | Skips asset publishing during the import process. |
| `--skip-entries-publish` | - | Skips entry publishing during the import process. |
| `--skip-taxonomy-publish` | - | Skips taxonomy publishing during the import process. |

**Examples**

1. Import to update only the global fields in the target stack:
   1. ```
      csdx cm:stacks:import-setup --module global-fields --data-dir <exported-content-dir> -k <target-stack-api-key>
      ```
   2. ```
      csdx cm:stacks:import --replace-existing --backup-dir <backup-dir-path-generated-by-import-setup> -k <value> --data-dir <content-dir-path> --module global-fields
      ```

2. Import to update only the content types in the target stack:
   1. ```
      csdx cm:stacks:import-setup --module content-types --data-dir <exported-content-dir> -k <target-stack-api-key>
      ```
   2. ```
      csdx cm:stacks:import --replace-existing --backup-dir <backup-dir-path-generated-by-import-setup> -k <value> --data-dir <content-dir-path> --module content-types
      ```

3. Import to update both global fields and content types in the target stack:
   1. ```
      csdx cm:stacks:import-setup --module global-fields content-types --data-dir <exported-content-dir> -k <target-stack-api-key>
      ```
   2. ```
      csdx cm:stacks:import --replace-existing --backup-dir <backup-dir-path-generated-by-import-setup> -k <value> --data-dir <content-dir-path> --module global-fields
      ```
   3. ```
      csdx cm:stacks:import --replace-existing --backup-dir <backup-dir-path-generated-by-import-setup> -k <value> --data-dir <content-dir-path> --module content-types
      ```

4. Import to update only the entries in the target stack:
   1. ```
      csdx cm:stacks:import-setup --module entries --data-dir <exported-content-dir> -k <target-stack-api-key>
      ```
   2. ```
      csdx cm:stacks:import --replace-existing --backup-dir <backup-dir-path-generated-by-import-setup> -k <value> --data-dir <content-dir-path> --module entries
      ```

5. Import to update both content types and entries in the target stack:
   1. ```
      csdx cm:stacks:import-setup --module content-types entries content-types --data-dir <exported-content-dir> -k <target-stack-api-key>
      ```
   2. ```
      csdx cm:stacks:import --replace-existing --backup-dir <backup-dir-path-generated-by-import-setup> -k <value> --data-dir <content-dir-path> --module content-types
      ```
   3. ```
      csdx cm:stacks:import --replace-existing --backup-dir <backup-dir-path-generated-by-import-setup> -k <value> --data-dir <content-dir-path> --module entries
      ```

## Migration Scenarios

The overwrite feature is a highly versatile tool designed to support various migration scenarios. It simplifies content management and updates while minimizing dependency issues. Here are the key migration use cases:

- **From One Stack to Another:** Seamlessly migrate content from one stack to another while ensuring proper mapping and updates.
- **Import into the Same Stack:** Update or overwrite existing content within the same stack to streamline workflows and eliminate redundancies.
- **From One Branch to Another:** Transfer content between branches of the same stack, enabling smooth collaboration and environment-specific changes.
- **Import into the Same Branch:** Refine or overwrite content within a single branch to efficiently implement updates or roll out changes.

This flexibility enables users to adapt the CLI to specific migration requirements, improving efficiency and reducing manual effort.

## Limitations

Here are the primary limitations to consider when leveraging the overwrite feature, despite its significant simplification of the migration process:

- **Dependency on Properly Structured Exported Content**: The process requires access to properly formatted exported content before running the command.
- **Asset Duplication**: Duplicate assets in the target stack are uploaded to a new folder, which can lead to redundancy. A resolution is under development.
- **Limited Module Support**: Currently, the `import-setup` command supports only content types, entries, global fields, and extensions. Modules with complex dependencies are not yet included.
- **Manual Overwrite Steps**: Overwriting certain modules requires manual intervention due to the absence of an automated overwrite command.
- **Processing Large Data Sets**: Migration of extensive content or assets may be time-consuming and requires accuracy verification.
- **Handling Complex Relationships**: Additional manual effort may be necessary to map deeply nested or interdependent modules correctly.
