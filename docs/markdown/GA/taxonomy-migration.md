---
uid: "blt2a6acf45012c79f3"
seo_title: "Taxonomy Migration | Contentstack"
seo_description: "Taxonomy Migration Contentstack CLI utility lets you perform the taxonomy migration operation on a stack."
---

# Taxonomy Migration

With the Taxonomy Migration utility, you can **import the taxonomies** and respective terms using a CSV file created using one of the following methods:

- [export-to-csv](/docs/headless-cms/export-content-to-csv-file) plugin
- [CSV template](https://github.com/contentstack/cli/blob/v2.0.0-beta/packages/contentstack-migration/examples/taxonomies/test_taxonomies.csv)

This step-by-step guide lets you use the Taxonomy Migration utility to perform the taxonomy migration operation on a stack.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- [CLI installed](/docs/headless-cms/install-the-cli/) and [configured](/docs/headless-cms/configure-regions-in-the-cli/) (version 1.11.0 and above)
- [CLI authenticated](/docs/headless-cms/cli-authentication/)
- CSV file (generated using the [export-to-csv](/docs/headless-cms/export-content-to-csv-file) plugin or a [CSV template](https://github.com/contentstack/cli/blob/v2.0.0-beta/packages/contentstack-migration/examples/taxonomies/test_taxonomies.csv))

> **Note:** If you are using a CSV template to generate the CSV file, the `Taxonomy Name` and `Term Level* Name` fields are mandatory.

> **Additional Resource:** Here is a [sample script](https://github.com/contentstack/cli/blob/v2.0.0-beta/packages/contentstack-migration/examples/taxonomies/import-taxonomies.js) to import taxonomies into your stack. Preferably, use this sample script to try out the commands in this guide.

**Usage**

```
csdx cm:stacks:migration --file-path <value> --config data-dir:<value> --stack-api-key <value>
```

**Options**

- `-k`, `--stack-api-key=stack-api-key`: Stack API key.

- `--config=config`: \[Inline configuration\] The key for receiving data-dir and delimiter. To provide the path of the CSV file in the data-dir, use `data-dir:<value>`. If you used a delimiter while exporting or manually creating taxonomies to CSV, use `{data-dir:<value>,delimiter:<value>}`.

- `--file-path=filepath`: Path where the taxonomy migration files are stored.

  > **Tip:** Preferably, use the sample [taxonomy migration script](https://github.com/contentstack/cli/blob/v2.0.0-beta/packages/contentstack-migration/examples/taxonomies/import-taxonomies.js) to import taxonomies.

**Example**

Without delimiter:

```
csdx cm:stacks:migration -k b*******9ca0 --file-path "../contentstack-migration/examples/taxonomies/import-taxonomies.js" --config data-dir:'./data/Taxonomy Stack_taxonomies.csv'
```

> **Note:** For Windows OS, use "`\`" instead of "`/`" for paths.

With delimiter (Mac OS):

```
csdx cm:stacks:migration -k b*******9ca0 --file-path "../contentstack-migration/examples/taxonomies/import-taxonomies.js" --config {data-dir:'./data/Taxonomy Stack_taxonomies.csv',delimiter:'|'}
```

With delimiter (Windows OS):

```
csdx cm:stacks:migration -k b*********d4 --file-path "C:\Users\v***h\Desktop\Contentstack\CLI\Taxonomy\import-taxonomies.js" --config data-dir:'C:\Users\v***h\Desktop\Contentstack\CLI\Taxonomy\test_taxonomies.csv' delimiter:','
```

## Steps for Execution

Follow the steps below to run the taxonomy migration command:

1. Provide the following flags in the `cm:stacks:migration` command to import taxonomy:
   - File path that contains the taxonomy migration files.

     > **Note:** Provide the file path of the downloaded [sample script](https://github.com/contentstack/cli/blob/v2.0.0-beta/packages/contentstack-migration/examples/taxonomies/import-taxonomies.js).

   - Stack API key

   - Config that contains the CSV file path and the delimiter

     > **Note:** You must provide a delimiter in config only if you used a delimiter while exporting taxonomies to CSV or generating CSV file manually.

   ```
   csdx cm:stacks:migration --stack-api-key <value> --file-path <value> --config {data-dir:<value>,delimiter:<value>}
   ```

   > **Note:** For Windows OS, use '`,`' as the delimiter.

2. Run the command in your terminal.

You have successfully migrated taxonomies from your CSV file to the provided stack.

Without delimiter:

![CLI_Taxonomy_Migration_WithoutDelimiter_Stage.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/bltb0af67f7320aac70/65dd996a6c65d74fd187b2cc/CLI_Taxonomy_Migration_WithoutDelimiter_Stage.png)

With delimiter (Windows OS):

![CLI_New_Taxonomy_Delimiter_WindowsOS.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blte03fb309fa5a7c0c/65dc0ac4fcf7fe17b53c400c/CLI_New_Taxonomy_Delimiter_WindowsOS.png)

With delimiter (Mac OS):

![CLI_Taxonomy_Migration_WithDelimiter_Stage_MacOS.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/bltb090938e22ebe1f8/65dd996a31aca131f07ee6b4/CLI_Taxonomy_Migration_WithDelimiter_Stage_MacOS.png)

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

- **Troubleshoot in the entire session**:

  ```
  npm link fast-csv
  ```
