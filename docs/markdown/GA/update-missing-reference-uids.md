---
uid: "blt3afca0a8bf912f83"
seo_title: "Update Missing Reference UIDs for Entries, Assets, and Extensions | Contentstack"
seo_description: "Update the missing reference UIDs of entries, assets, and extensions in your destination stack after the Import operation."
---

# Update Missing Reference UIDs for Entries, Assets, and Extensions

When importing data via Contentstack's CLI, if some of the reference UIDs of [assets](/docs/headless-cms/about-assets), [entries](/docs/headless-cms/about-entries), or [extensions](/docs/developer-hub/about-ui-locations) in the destination stack are not updated within the entries. This can result in those entries not displaying correctly, potentially affecting functionalities that depend on them.

To resolve this, you can use the script `05-Update-reference-entry-from-mapper` to update the references. This script can be used under the following conditions:

1. The referenced entries, assets, and extensions have already been created in the stack.
2. The unique identifiers (UIDs) of the referenced items have not been updated in the referring entries.

This step-by-step guide lets you update the missing reference UIDs of entries, assets, and extensions in CLI.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- [CLI installed](/docs/headless-cms/install-the-cli/) and [configured](/docs/headless-cms/configure-regions-in-the-cli/) (version 1.17.4 and above)
- [CLI authenticated](/docs/headless-cms/cli-authentication/)

## Steps for Execution

Follow the steps below to update the missing reference UIDs:

1. [Import the data](/docs/headless-cms/import-content-using-the-cli) from the source stack using the `cm:stacks:import` command.

2. Download the [examples](https://github.com/contentstack/cli/tree/v2.0.0-beta/packages/contentstack-migration/examples) folder and navigate to the folder using the `cd` command in the terminal.

   ```
   cd <path-to-examples>
   ```

3. Create a `config.json` file containing the following key-value pairs:
   - **mapper-path**: The path to the backup directory where the logs are stored.
     You can find the following path after a successful import operation in your CLI:
     `<path>/_backup_<number>/logs/import`
     Copy and use `<path>/_backup_<number>` in the config file.
   - **contentTypes**: An array of content type UIDs whose references need to be updated.

   ```
   {
     "mapper-path": "<path>/_backup_<number>/",
     "contentTypes": [
       "ct1",
       "ct2", ....
     ]
   }
   ```

4. Find the `05-Update-reference-entry-from-mapper` script in the `examples` folder. Execute the script using the [Migration](/docs/headless-cms/migrate-your-content-using-the-cli-migration-command/) command as follows:

   ```
   csdx cm:stacks:migration --file-path ./05-Update-reference-entry-from-mapper.js --config-file ./config.json -k <stack_ApiKey>
   ```

## Troubleshoot

If you are facing a **Migration Unsuccessful** or **Module cannot be found** error, please try one of the following troubleshooting methods:

- **Troubleshoot in your current terminal session**:
  1. **Windows (CMD)**:

     ```
     FOR /F "usebackq tokens=*" %i IN (`npm root -g @contentstack/cli`) DO SET NODE_PATH=%i/@contentstack/cli/node_modules
     ```

  2. **Windows (PowerShell)**:

     ```
     foreach ($i in $(npm root -g @contentstack/cli)) { $env:NODE_PATH = "$i/@contentstack/cli/node_modules" }
     ```

  3. **Mac/Unix**:

     ```
     export NODE_PATH="$(npm root -g @contentstack/cli)/@contentstack/cli/node_modules"
     ```
