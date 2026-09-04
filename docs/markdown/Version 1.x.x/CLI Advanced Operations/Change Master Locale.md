---
uid: "blt278785a9d6da5074"
seo_title: "Change Master Locale | Contentstack"
seo_description: "Learn how to change the master locale of the data exported from the CLI"
---

# Change Master Locale

## Overview

While importing data using the Contentstack’s CLI, if the destination stack has a different master locale than the source stack, the API throws an error indicating that the master locale of the incoming data does not exist in the destination stack.

As a solution, you can change the master locale of the data exported from the CLI using the `change-master-locale` utility so that it matches the master locale of the destination stack.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- [CLI installed](/docs/headless-cms/install-the-cli) (version 1.1.0 and above)

## Steps for Execution

1. [Export the data](/docs/headless-cms/export-content-using-the-cli) from the source stack using the `cm:stacks:export` command.

2. Download the [examples](https://github.com/contentstack/cli-plugins/tree/main/packages/contentstack-migration/examples) folder and navigate to the folder using the `cd` command in the terminal.

   ```
   cd <path-to-examples>
   ```

3. Find the `change-master-locale` script in the `examples` folder. Execute the script using the migration command as follows:

   ```
   csdx cm:stacks:migration --file-path ./change-master-locale/02-change-master-locale-new-file-structure.js --config target_locale:<target-locale> data_dir:<path-to-the-exported-data>
   ```

   > **Note:** `path-to-the-exported-data` can either be the relative path or the absolute path.

   Alternatively, You can save the config parameters to a `config.json` file and use it as follows:

   ```
    csdx cm:stacks:migration --file-path ./change-master-locale/02-change-master-locale-new-file-structure.js --config-file <path-to-the-config-file>
   ```

   > **Note:** If you used the CLI version below `1.9.0` to [export the data](/docs/headless-cms/export-content-using-the-cli), use the `01-change-master-locale.js` script instead of `02-change-master-locale-new-file-structure.js` in the examples above.

4. [Import the data](/docs/headless-cms/import-content-using-the-cli) to the target stack using the `cm:stacks:import` command.

## Limitations

- This utility does not work for the clone command.
