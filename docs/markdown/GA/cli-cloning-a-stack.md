---
uid: "bltf1f565bcdf7e63cd"
seo_title: "Cloning a Stack | V1.x.x | Contentstack"
seo_description: "Clone a stack easily with Contentstack Command-line Interface commands using our step-by-step guide to streamline stack duplication."
---

# Cloning a Stack

Contentstack enables you to **clone a stack** and its associated **structure and content** using the `cm:stacks:clone` CLI command. This process lets you [export](/docs/headless-cms/export-content-using-the-cli/v1) data from a source stack and [import](/docs/headless-cms/import-content-using-the-cli/v1) it into a new or existing stack, facilitating rapid setup, testing, or migration. This guide uses the latest **Contentstack CLI** commands to ensure a seamless cloning experience.

> **Note:** Before executing this command, ensure you have the required permissions for creating or accessing the destination stack. To know more about user roles and their permissions, refer to [this](/docs/headless-cms/types-of-roles#stack-roles-and-permissions-overview) documentation.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli/v1) and [configured](/docs/headless-cms/configure-regions-in-the-cli/v1)
- [Configured authtoken](/docs/headless-cms/cli-authentication/v1#authentication)

## Commands

The `cm:stacks:clone` command lets you export content from the source stack and import it into the destination stack instantly.

> **Note:** By default, an [audit fix](/docs/headless-cms/cli-audit-plugin/v1#issue-resolution-in-references) is performed on the exported content before import. This helps identify and address potential issues in the exported data.

## Options

Use the following options while performing the clone operation:

- `-n, --stack-name=stack-name`: Name for the new stack where cloned content will be stored.

- `--destination-management-token-alias=destination-management-token-alias`: Alias for the destination stack's management token.

- `--destination-stack-api-key=destination-stack-api-key`: API key of the destination stack.

- `--source-stack-api-key=source-stack-api-key`: API key of the source stack.

- `--source-branch=source-branch`: Name of the branch in the source stack.

- `--source-branch-alias=source-branch-alias`: Alias of the branch in the source stack.

- `--source-management-token-alias=source-management-token-alias`: Alias for the source stack's management token.

- `--target-branch=target-branch`: Name of the branch in the target stack.

- `--target-branch-alias=target-branch-alias`: Alias of the branch in the target stack.

- `--import-webhook-status=<option>`: \[default: disable\] (optional) The status of the import webhook. \<options: disable|current\>

- `--type=type`: Type of data to clone. You can select option a or b.
  a) Structure (all modules except entries & assets).
  b) Structure with content (all modules including entries & assets).

- `--skip-audit`: (optional) Skips the audit fix that occurs during an import operation.

- `–y, --yes`: Force override all Marketplace prompts.

- `-c, --config`: Path for the external configuration (an example of a config file is given below).
  **Sample config file:**

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
- The clone function supports the **same modules** as the CLI [export](/docs/headless-cms/export-content-using-the-cli/v1) and [import](/docs/headless-cms/import-content-using-the-cli/v1) commands.

> **Additional Resources**: Learn more about the CLI-supported clone operations in the [CLI-Supported Features for Export, Import, and Clone Operations](/docs/headless-cms/cli-supported-features-for-export-import-and-clone-operations/v1) document.
