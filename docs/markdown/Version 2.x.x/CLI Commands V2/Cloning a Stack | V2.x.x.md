---
uid: "bltb61fca77fed848a6"
seo_title: "Cloning a Stack | V2.x.x | Contentstack"
seo_description: "Clone a stack easily with Contentstack Command-line Interface commands using our step-by-step guide to streamline stack duplication."
---

# Cloning a Stack

## Overview

Contentstack enables you to **clone a stack** and its associated **structure and content** using the `cm:stacks:clone` CLI command. This process lets you [export](/docs/headless-cms/export-content-using-the-cli) data from a source stack and [import](/docs/headless-cms/import-content-using-the-cli) it into a new or existing stack, facilitating rapid setup, testing, or migration. This guide uses the latest **Contentstack CLI** commands to ensure a seamless cloning experience.

> **Note:** Before executing this command, ensure you have the required permissions for creating or accessing the destination stack. To know more about user roles and their permissions, refer to [this](/docs/headless-cms/types-of-roles#stack-roles-and-permissions-overview) documentation.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli) and [configured](/docs/headless-cms/configure-regions-in-the-cli)
- [Configured authtoken](/docs/headless-cms/cli-authentication#authentication)

## Commands

The `cm:stacks:clone` command lets you export content from the source stack and import it into the destination stack instantly.

> **Note:** By default, an [audit fix](/docs/headless-cms/cli-audit-plugin#issue-resolution-in-references) is performed on the exported content before import. This helps identify and address potential issues in the exported data.

## Options

Use the following options while performing the clone operation:

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--source-branch` | - | Branch of the source stack. |
| `--source-branch-alias` | - | Alias of the branch of the source stack. |
| `--target-branch` | - | Branch of the target stack. |
| `--target-branch-alias` | - | Alias of the branch of the target stack. |
| `--source-management-token-alias` | - | Source management token alias. |
| `--destination-management-token-alias` | - | Destination management token alias. |
| `--stack-name` | `-n` | Provide a name for the new stack to store the cloned content. |
| `--type` | - | Type of data to clone.<br>Supported values: `a`, `b`<br>`a`: Structure (all modules except entries and assets).<br>`b`: Structure with content (all modules including entries and assets). |
| `--source-stack-api-key` | - | Source stack API key. |
| `--destination-stack-api-key` | - | Destination stack API key. |
| `--import-webhook-status` | - | \[Optional\] The status of the import webhook.<br>Supported values: `disable`, `current`<br>Default: `disable` |
| `--yes` | `-y` | Force override all Marketplace prompts. |
| `--skip-audit` | - | \[Optional\] Skips the audit fix that occurs during an import operation. |
| `--config` | `-c` | Path for the external configuration. |

Below is an example of a config file

```
{
    "master_locale": {
        "name": "English - United States",
        "code": "en-us"
      },
    "export": { 
              // export specific configs
             "fetchConcurrency": 1
      } ,
    "import": { 
              // import specific configs
             "entriesPublish": false
      }
}
```

On passing the `--config` flag, the config will be passed to export and import in the `--clone` command. You can pass separate or common config for export and import as given in the above sample config file.

> **Note:** If the `--yes` flag is not passed, you’ll be prompted to enter an encryption key when cloning a Marketplace app with its configuration. You have **three attempts** to provide the correct key. After three failed attempts, the cloning process must be restarted from the beginning.

## Steps to Clone a Stack

Follow the steps below to clone a stack using the `cm:stacks:clone` command:

1. Run the following command in your terminal:

   ```
   csdx cm:stacks:clone
   ```

2. Choose the **organization** from the displayed list.

3. Select the **stack** you want to clone.

4. Choose the **branch** of the stack.

5. Choose whether to clone content to a **new stack** or use an existing one:
   - **Y:** Create a new stack.
     - Select the destination organization.
     - The default name format: `Copy of {source_stack_name}`.
     - You can provide a custom name for the new stack.

   - **n:** Use an existing stack.
     - Select the destination organization and stack (must have permissions).

   > **Tip:** To minimize errors, we recommend creating **a new destination stack**. If importing content into an existing stack, ensure that it is empty.

6. Select one of the following types of content to clone:
   - **Structure:** Imports only the schema (no entries/assets).
   - **Structure with content:** Imports schema, entries, and assets.

After you complete these prompts, the source stack’s content will be cloned to the destination stack.

Alternatively, you can also run the entire operation using a single command with parameters as given below:

```
csdx cm:stacks:clone -n "<>" --source-management-token-alias "<>" --destination-management-token-alias "<>" --target-branch "<>" --source-branch "<>" --type a|b {choose either a or b} -y
```

**Examples:**

- To clone content using management token aliases:

  ```
  csdx cm:stacks:clone --source-management-token-alias <<management token alias for source>> --destination-management-token-alias <<management token alias for destination>>
  ```

- To clone content and force override all Marketplace prompts:

  ```
  csdx cm:stacks:clone --source-management-token-alias <<management token alias for source>> --destination-management-token-alias <<management token alias for destination>> --yes
  ```

## Points to Remember

- To import content into an **existing stack**, ensure you have permissions to create or update content in that stack.
- Currently, we migrate only the latest version of entries and assets.
- To **create a new stack**, you must have the [owner](/docs/administration/about-administration-roles/#organization-owner) or [admin](/docs/administration/about-administration-roles/#organization-admin) rights in the destination organization.
- During **workflow migration**, admins and workflow stage users are not included. These must be manually reconfigured after cloning.
- The clone function supports the **same modules** as the CLI [export](/docs/headless-cms/export-content-using-the-cli) and [import](/docs/headless-cms/import-content-using-the-cli) commands.

> **Additional Resources**: Learn more about the CLI-supported clone operations in the [CLI-Supported Features for Export, Import, and Clone Operations](/docs/headless-cms/cli-supported-features-for-export-import-and-clone-operations) document.
