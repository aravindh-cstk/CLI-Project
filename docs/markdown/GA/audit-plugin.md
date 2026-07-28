---
uid: "blt5bf8ffa6d7788728"
seo_title: "Audit Plugin | Contentstack"
seo_description: "The Audit plugin in Contentstack CLI lets you perform audit operations to identify and fix various issues in the exported stack data."
---

# Audit Plugin

Contentstack CLI lets you use the Audit plugin to perform audit operations on the exported stack data, helping you identify and fix issues.

The Audit plugin provides users with detailed reports about any issues related to the following, in a given stack data:

- References in [Content Types](/docs/headless-cms/about-content-types), [Global Fields](/docs/headless-cms/global), and [Entries](/docs/headless-cms/about-entries).
- Content types used in [Workflows](/docs/headless-cms/about-workflows) and [Extensions](/docs/developer-hub/about-ui-locations).
- [Branches](/docs/headless-cms/about-branches/) used in custom roles and workflows.
- [Title field](/docs/headless-cms/title/), [select field](/docs/headless-cms/select/), publish details, and mandatory fields of entries.
- Multiple field type mismatches in entries where fields marked with `multiple: true` are not arrays.
- Publish details of [Assets](/docs/headless-cms/about-assets).
- Field rules in content types.

Additionally, it includes commands that validate and resolve these issues, including missing references, invalid field values, missing mandatory fields, incomplete publish details, field rule violations, and content type mismatches.

This step-by-step guide lets you install and use the Audit plugin in CLI.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- [CLI installed](/docs/headless-cms/install-the-cli/) and [configured](/docs/headless-cms/configure-regions-in-the-cli/) (version 1.9.1 or above)
- [Exported content](/docs/headless-cms/export-content-using-the-cli) generated using CLI (version 1.9.0 or above) available on local machine

## Supported Modules

- [Extensions](/docs/developer-hub/about-ui-locations)
- [Global Fields](/docs/headless-cms/global)
- [Content Types](/docs/headless-cms/about-content-types)
- [Field Rules](/docs/headless-cms/about-field-visibility-rules)
- [Entries](/docs/headless-cms/about-entries)
- [Workflow](/docs/headless-cms/about-workflows)
- [Custom Roles](/docs/headless-cms/types-of-roles#custom-role)
- [Assets](/docs/headless-cms/about-assets)

## Commands

The Audit plugin lets you perform the following operation in Contentstack CLI:

- [Issue Identification](#issue-identification)
- [Issue Resolution](#issue-resolution)

### Issue Identification

The `cm:stacks:audit` command allows you to validate exported stack data and identify various issues across all supported modules.

1. Open the terminal.

2. Run the following command:

   ```
   csdx cm:stacks:audit
   ```

3. Enter the **local path** where the data is stored.

   ![CLI_Audit_Plugin_Path.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt7d2bee5298009286/652d0fcff620d479b3438bf6/CLI_Audit_Plugin_Path.png)

   > **Note:** If you exported data from a branch-enabled stack, make sure to provide the complete local path up to the branch. For example, `C:\Users\...\CLI\Content\branch_folder`.

You successfully ran an audit operation to find data issues in your stack.

Alternatively, you can pass the path in the command as given below:

```
csdx cm:stacks:audit --data-dir <path>
```

**Usage**

```
csdx cm:stacks:audit
```

**Options**

- `-c`, `--config=config`: \[optional\] Path of the external config.
- `-d`, `--data-dir=data-dir`: \[optional\] Path where the data is stored.
- `--columns=columns`: Show only the specified columns (comma-separated).
- `--csv`: The output is in the CSV format \[alias: `--output=csv`\].
- `--filter=filter`: Filter property by partial string matching. For example: name=foo.
- `--modules=modules`: Provide the list of modules to be audited. \[options: content-types|global-fields|entries|extensions|workflows|custom-roles|assets|field-rules\]
- `--no-header`: Hide table headers in output.
- `--no-truncate`: The output is not truncated to fit the screen.
- `--output=output`: Specify the output format. \[options: csv|json\]
- `--report-path=report-path`: Path to store the audit reports.
- `--sort=sort`: Sort the table by a column. Use "-" for descending.
- `--show-console-output`: Displays the audit and audit fix results for individual modules.

> **Note:** If the custom role or the workflow module has branches **enabled** and you want audit to operate on all the branches except a particular branch, then you can provide that specific branch name using the `--config` flag as given below:

```
{
"branch": "<branch-name>"
}
```

Passing this flag makes the auditing process check and report on all branches except the one specified in the config file.

**Examples**

- To perform the audit operation by providing the path to store the audit reports:

  ```
  csdx cm:stacks:audit --report-path <path>
  ```

- To perform the audit operation by fetching the results in CSV format and providing the path to store the audit reports:

  ```
  csdx cm:stacks:audit --report-path <path> --csv
  ```

- To perform the audit operation with a name filter and by providing the path to store the audit reports:

  ```
  csdx cm:stacks:audit --report-path <path> --filter="name=<filter-value>"
  ```

- To perform the audit operation by providing the module for which the audit must be performed, along with the path to store the audit reports:

  ```
  csdx cm:stacks:audit --report-path <path> --modules=content-types
  ```

### Issue Resolution

The `cm:stacks:audit:fix` command allows you to validate exported stack data and actively resolve the identified issues.

1. Open the terminal.

2. Run the following command:

   ```
   csdx cm:stacks:audit:fix
   ```

3. Enter the **local path** where the data is stored.

   ![CLI_Audit_Plugin_Path.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt7d2bee5298009286/652d0fcff620d479b3438bf6/CLI_Audit_Plugin_Path.png)

4. In the prompt that appears, enter the following:
   - **Yes**, to overwrite the existing file.
   - **No**, to skip overwriting the existing file.

   > **Note:** The prompt appears only if you have not passed the `--copy-dir` flag.

You successfully ran an audit operation to fix data issues in your stack.

Alternatively, you can pass the path in the command as given below:

```
csdx cm:stacks:audit:fix --data-dir <path>
```

**Usage**

```
csdx cm:stacks:audit:fix
```

or

```
csdx audit:fix
```

**Options**

- `-c`, `--config=config`: \[optional\] Path of the external config.
- `-d`, `--data-dir=data-dir`: \[optional\] Path where the data is stored.
- `--copy-path=copy-path`: Provide the path to backup the copied data.
- `--columns=columns`: Show only the specified columns (comma-separated).
- `--copy-dir`: \[recommended\] Create backup from the original data.
- `--csv`: The output is in the CSV format \[alias: `--output=csv`\].
- `--filter=filter`: Filter property by partial string matching. For example: name=foo.
- `--modules=modules`: Provide the list of modules to be audited. \[options: content-types|global-fields|entries|extensions|workflows|custom-roles|assets|field-rules\]
- `--no-header`: Hide table headers in output.
- `--no-truncate`: The output is not truncated to fit the screen.
- `--output=output`: Specify the output format. \[options: csv|json\]
- `--report-path=report-path`: Path to store the audit reports.
- `--sort=sort`: Property to sort by (prepend '-' for descending).
- `--fix-only=fix-only`: Provide the list of fix options. \[options: reference|global_field|json:rte|json:extension|blocks|group|content_types\]
- `--show-console-output`: Displays the audit and audit fix results for individual modules.

> **Note:**
>
> - If the custom role or the workflow module has branches **enabled** and you want audit to operate on all the branches except a particular branch, then you can provide that specific branch name using the `--config` flag as given below:
>
>   ```
>   {
>   "branch": "<branch-name>"
>   }
>   ```
>
>   Passing this flag makes the auditing process check and remove all branches except the one specified in the config file.
>
> - When you use the `--copy-dir` flag, a copy of the original data gets created and the audit fix operation occurs on the copied data.
>
> - By default, `audit:fix` does not populate values in the select fields. To enable this behavior, use the `–-config` flag and provide a configuration file containing the following keys:
>
>   ```
>   {
>   "fixSelectField": true
>   }
>   ```

**Examples**

- To perform the audit fix operation on a copied version of the original data:

  ```
  csdx cm:stacks:audit:fix --copy-dir
  ```

- To perform the audit operation on a copied version of the original data by providing the path to store the audit reports:

  ```
  csdx cm:stacks:audit:fix --report-path <path> --copy-dir
  ```

- To perform the audit fix operation with a name filter and by providing the path to store the audit reports:

  ```
  csdx cm:stacks:audit:fix --report-path <path> --filter="name=<filter-value>"
  ```

- To perform the audit operation on a copied version of the original data by providing the backup directory path to store the copied data, along with the path to store the audit reports:

  ```
  csdx cm:stacks:audit:fix --report-path <path> --copy-dir --copy-path <path>
  ```

## Module-Specific Audit Checks

### Content Types Module

The Content Types module audits the following:

- **Missing references in reference fields**: Detects referenced entries that are missing from the exported data.
- **Missing global field references**: Identifies global fields referenced in content types that are missing.
- **Missing references in JSON RTE fields**: Finds missing entry/asset references within JSON Rich Text Editor fields.
- **Missing extension/app references**: Detects missing references to extensions or marketplace apps in JSON fields.
- **Missing references in modular blocks**: Identifies missing references within modular block fields.
- **Missing references in group fields**: Finds missing references within group field structures.

**Report files generated:**  
`content-types.json`/`content-types.csv`

### Global Fields Module

The Global Fields module audits the same issues as the Content Types module, using the same audit logic.

- All reference-related issues listed under Content Types.

**Report files generated:**  
`global-fields.json`/`global-fields.csv`

### Entries Module

The Entries module audits the following:

- **Missing references**: Detects all reference types supported by the Content Types module, including reference fields, global fields, JSON RTE, extensions, modular blocks, and groups.
- **Invalid select field values**: Detects when entry data contains select field values that do not match the content type's defined options.
- **Missing mandatory fields**: Identifies entries with missing required fields.
- **Missing title fields**: Finds entries without the title field values.
- **Missing locale/environment in publish details**: Detects entries with incomplete publish details (missing locale or environment information).
- **Multiple field type mismatches**: Identifies fields marked as `multiple: true` in the content type that are not arrays in the entry data.

**Report files generated:**

- `entries.json`/`entries.csv` (missing references)
- `Entries_Select_field.json`/`Entries_Select_field.csv` (invalid select field values)
- `Entries_Mandatory_field.json`/`Entries_Mandatory_field.csv` (missing mandatory fields)
- `Entries_Title_field.json`/`Entries_Title_field.csv` (missing title fields)
- `Entry_Missing_Locale_and_Env_in_Publish_Details.json`/`Entry_Missing_Locale_and_Env_in_Publish_Details.csv` (publish details issues)
- `Entry_Multiple_Fields.json`/`Entry_Multiple_Fields.csv` (multiple field type mismatches)

### Extensions Module

The Extensions module audits the following:

- **Missing content types**: Detects content types referenced in extensions that are missing in the exported data.

**Report files generated:**  
`extensions.json`/`extensions.csv`

### Workflows Module

The Workflows module audits the following:

- **Missing content types**: Identifies missing content types referenced in workflows.
- **Missing branches**: Detects branches referenced in workflows that are missing from the exported data.

**Report files generated:**  
`workflows.json`/`workflows.csv`

### Custom Roles Module

The Custom Roles module audits the following:

- **Missing branches**: Identifies branches referenced in custom role rules that are missing from the exported data.

**Report files generated:**  
`custom-roles.json`/`custom-roles.csv`

### Assets Module

The Assets module audits the following:

- **Missing locale/environment in publish details**: Detects assets with incomplete publish details (missing locale or environment information).

This check validates the structural completeness of `publish_details` only. It does not check an asset's scan or quarantine status. For asset-scan gating during publish, see [Bulk Publish and Unpublish Content](/docs/headless-cms/bulk-publish-and-unpublish-content#bulk-publish-all-assets).

**Report files generated:**  
`assets.json`/`assets.csv`

### Field Rules Module

The Field Rules module audits the following:

- **Invalid field references**: Detects field UIDs referenced in field rules that are missing from the content type schema.
- **Missing content types**: Identifies content types referenced in field rule conditions that are missing from the exported data.

**Report files generated:**  
`field-rules.json` / `field-rules.csv`

### Summary Report

A summary report provides an overview of all audited modules.

**Report file:**  
`Summary.json`/`Summary.csv`

**Summary report structure:**

- **Module**: Name of the module audited.
- **Total**: Total number of items audited in the module.
- **Passed**: Number of items with no issues found.
- **Fixable**: Number of issues that can be automatically fixed (audit command only).
- **Non-Fixable**: Number of issues that cannot be automatically fixed (audit command only).
- **Fixed**: Number of issues that were successfully fixed (audit:fix command only).
- **Not-Fixed**: Number of issues that could not be fixed (audit:fix command only).

## Module Dependencies

Some modules require other modules to be present in the exported data for proper auditing. Understanding these dependencies helps ensure accurate audit results.

### Entries Module Dependencies

The Entries module requires the following modules to be present in the exported data to perform a complete audit:

- **Content Types** (`content_types`/`schema.json`): (Required) Validates entry structure, field types, and references.
- **Global Fields** (`global_fields`/`globalfields.json`): (Required) Validates global field references in entries.
- **Locales** (`locales`/`locales.json` and `locales`/`master-locale.json`): (Required) Validates locale references in entries and the publish details.
- **Environments** (`environments`/`environments.json`): (Required) Validates environment references in the publish details.
- **Extensions** (`extensions`/`extensions.json`): (Optional) Validates extension/app references in JSON fields (loaded if exists).
- **Marketplace Apps** (`marketplace_apps`/`marketplace_apps.json`): (Optional) Validates Marketplace app extension references (loaded if exists).

> **Note:** If required dependencies are missing, the Entries audit may return incomplete or inaccurate results.

### Assets Module Dependencies

The Assets module requires the following modules to be present in the exported data to perform a complete audit:

- **Locales** (`locales`/`locales.json` and `locales`/`master-locale.json`): (Required) Validates locale references in asset publish details.
- **Environments** (`environments`/`environments.json`): (Required) Validates environment references in asset publish details.

### Field Rules Module Dependencies

The Field Rules module requires the following modules to be present in the exported data to perform a complete audit:

- **Content Types** (`content_types`/`schema.json`): (Required) Validates field UIDs referenced in field rules.
- **Extensions** (`extensions`/`extensions.json`): (Optional) Validates extension references in field rules (loaded if exists).
- **Entries**: (Required) Entry metadata is needed for field rule validation.

### Other Modules

The following modules have no dependencies and can be audited independently:

- Content Types
- Global Fields
- Extensions
- Workflows
- Custom Roles

## Common Use Cases

This section outlines complete workflows for common developer use cases with the Audit plugin.

### Pre-Import Validation

Validate exported data before importing it into another stack to identify and fix issues early.

**Complete Workflow:**

```
# Step 1: Export data from the source stack
csdx cm:stacks:export --data-dir ./exported-data

# Step 2: Audit the exported data
csdx cm:stacks:audit --data-dir ./exported-data --report-path ./audit-reports

# Step 3: Review the Summary report
cat ./audit-reports/Summary.json

# Step 4: If issues are found, fix them
csdx cm:stacks:audit:fix --data-dir ./exported-data --copy-dir --report-path ./audit-reports

# Step 5: Verify fixes by auditing again
csdx cm:stacks:audit --data-dir ./exported-data --report-path ./audit-reports-verify

# Step 6: Import the fixed data
csdx cm:stacks:import --data-dir ./exported-data
```

### Post-Export Quality Check

After exporting, run a quality check on critical modules to ensure data integrity and structural completeness.

**Complete Workflow:**

```
# Step 1: Export data
csdx cm:stacks:export --data-dir ./my-export

# Step 2: Run a quick audit (focus on critical modules)
csdx cm:stacks:audit \
  --data-dir ./my-export \
  --modules=content-types \
  --modules=entries \
  --modules=assets \
  --report-path ./quick-audit

# Step 3: Check for any critical issues in the export
if [ -s ./quick-audit/Summary.json ]; then
  echo "Issues found. Review the reports in ./quick-audit"
  # Review specific reports
  cat ./quick-audit/entries.json
else
  echo "Export completed. No issues detected."
fi
```

### Fixing Before Migration

Automatically fix all audit-detected issues to prepare your data for a clean migration.

**Complete Workflow:**

```
# Step 1: Export data from the source stack
csdx cm:stacks:export --data-dir ./migration-data

# Step 2: Perform a full audit to identify all issues
csdx cm:stacks:audit \
  --data-dir ./migration-data \
  --report-path ./migration-audit \
  --show-console-output

# Step 3: Review which issues can be fixed automatically
cat ./migration-audit/Summary.json | grep -A 5 "Fixable"

# Step 4: Fix all fixable issues with backup
csdx cm:stacks:audit:fix \
  --data-dir ./migration-data \
  --copy-dir \
  --copy-path ./migration-data-backup \
  --report-path ./migration-fix-reports

# Step 5: Verify the fixes
csdx cm:stacks:audit \
  --data-dir ./migration-data \
  --report-path ./migration-verify

# Step 6: Compare results before and after
echo "Before fix:"
cat ./migration-audit/Summary.json
echo "After fix:"
cat ./migration-verify/Summary.json
```

### Selective Module Auditing

Run audits only on specific modules when you want to target known problem areas or speed up the process for large stacks.

**Complete Workflow:**

```
# Step 1: Audit only the entries module (recommended for large stacks)
csdx cm:stacks:audit \
  --data-dir ./exported-data \
  --modules=entries \
  --report-path ./entries-audit

# Step 2: If entry issues are found, audit dependent modules
csdx cm:stacks:audit \
  --data-dir ./exported-data \
  --modules=content-types \
  --modules=global-fields \
  --report-path ./dependencies-audit

# Step 3: Fix entry-specific issues
csdx cm:stacks:audit:fix \
  --data-dir ./exported-data \
  --modules=entries \
  --copy-dir
```

### Branch Migration Preparation

Audit branch-specific issues before merging or migrating to the main branch.

**Complete Workflow:**

```
# Step 1: Export branch data
csdx cm:stacks:export \
  --data-dir ./branch-data \
  --branch my-feature-branch

# Step 2: Audit branch data (excluding main branch from workflows/roles)
csdx cm:stacks:audit \
  --data-dir ./branch-data \
  --config branch-config.json \
  --report-path ./branch-audit

# Where branch-config.json contains:
# {
#   "branch": "main"
# }

# Step 3: Fix issues in the branch data
csdx cm:stacks:audit:fix \
  --data-dir ./branch-data \
  --config branch-config.json \
  --copy-dir

# Step 4: Verify the branch data is clean
csdx cm:stacks:audit \
  --data-dir ./branch-data \
  --config branch-config.json \
  --report-path ./branch-verify
```

### CI/CD Pipeline Integration

Automate auditing in your deployment pipeline.

**Complete Workflow (GitHub Actions example):**

```
# .github/workflows/audit.yml
name: Audit Exported Data

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Export stack data
        run: |
          csdx cm:stacks:export --data-dir ./exported-data

      - name: Run audit
        run: |
          csdx cm:stacks:audit \
            --data-dir ./exported-data \
            --report-path ./audit-reports \
            --output json

      - name: Check for issues
        run: |
          if [ -s ./audit-reports/Summary.json ]; then
            echo "Issues found in exported data!"
            cat ./audit-reports/Summary.json
            exit 1
          else
            echo "No issues found. Data is clean!"
          fi

      - name: Upload audit reports
        uses: actions/upload-artifact@v2
        if: failure()
        with:
          name: audit-reports
          path: ./audit-reports
```

#### Shell Script Example:

```
#!/bin/bash
# audit-check.sh

EXPORT_DIR="./exported-data"
AUDIT_DIR="./audit-reports"

# Export data
csdx cm:stacks:export --data-dir "$EXPORT_DIR"

# Run audit
csdx cm:stacks:audit \
  --data-dir "$EXPORT_DIR" \
  --report-path "$AUDIT_DIR" \
  --output json

# Check if issues were found
if [ -s "$AUDIT_DIR/Summary.json" ]; then
  echo "Audit failed: Issues found"
  cat "$AUDIT_DIR/Summary.json"
  exit 1
else
  echo "Audit passed: No issues found"
  exit 0
fi
```

### Fixing Select Field Issues

Automatically fix invalid select field values in the entries.

**Complete Workflow:**

```
# Step 1: Audit entries to find select field issues
csdx cm:stacks:audit \
  --data-dir ./exported-data \
  --modules=entries \
  --report-path ./audit-reports

# Step 2: Review the select field issues report
cat ./audit-reports/Entries_Select_field.json

# Step 3: Create a configuration file to enable select field fixing
cat > select-fix-config.json << EOF
{
  "fixSelectField": true
}
EOF

# Step 4: Fix select field issues using the configuration
csdx cm:stacks:audit:fix \
  --data-dir ./exported-data \
  --config select-fix-config.json \
  --copy-dir \
  --report-path ./fix-reports

# Step 5: Verify that select field issues were resolved
csdx cm:stacks:audit \
  --data-dir ./exported-data \
  --modules=entries \
  --report-path ./verify-reports
```

## Troubleshooting

### Common Issues

- **Error:** `Path does not exist`
  **Solution:** Ensure the `--data-dir` path points to the correct exported data directory. For branch-enabled stacks, include the full path to the branch folder.
- **Error:** `No reports generated`
  **Solution:** Verify that the `--report-path` directory is writable. Reports are only generated if issues are found.
- **Error:** `Fix operation not working`
  **Solution:** Ensure you are using the `--copy-dir` flag. The fix operation modifies files, and without a backup, you may lose the original data.
- **Error:** `Select field values not being fixed`
  **Solution:** Enable select field fixing by adding `{ "fixSelectField": true }` to your config file and passing it using the `--config` flag.

## Best Practices

- Always use the `--copy-dir` flag when running `audit:fix` to preserve your original data.
- Review **audit reports** before running `audit:fix` to understand what will be changed.
- Use **configuration files** for repeated operations with the same settings.
- Check the **Summary report** to get an overview before diving into specific module reports.

## Limitation

- The Audit plugin currently supports audit operations for identifying and fixing issues in the following areas:
  - To find and fix missing reference issues in:
    - [Content Types](/docs/headless-cms/about-content-types)
    - [Global Fields](/docs/headless-cms/global)
    - [Entries](/docs/headless-cms/about-entries)

  - To find and fix the following in a given exported stack data:
    - Missing content types in [Workflows](/docs/headless-cms/about-workflows) and [Extensions](/docs/developer-hub/about-ui-locations).
    - Missing branches in workflows and [custom roles](/docs/headless-cms/types-of-roles#custom-role).
    - Publish details of entries and [assets](/docs/headless-cms/about-assets).
    - [Select](/docs/headless-cms/select/), [title](/docs/headless-cms/title/), and mandatory fields of entries.
    - Multiple field type mismatches in entries.
    - Field rules of content types.
