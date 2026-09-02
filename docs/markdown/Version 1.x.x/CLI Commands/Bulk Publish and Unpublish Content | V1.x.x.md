---
uid: "blt804647818d4181f9"
seo_title: "Bulk Publish and Unpublish Content | V1.x.x | Contentstack Documentation"
seo_description: "Use the CLI to bulk publish and unpublish entries and assets in Contentstack for efficient content management across environments."
---

# Bulk Publish and Unpublish Content

## Overview

The Bulk `publish` and `unpublish` commands allow you to publish entries and assets from multiple content types to one or more environments, and unpublish entries and assets.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- CLI [installed](/docs/headless-cms/install-the-cli/v1) and [configured](/docs/headless-cms/configure-regions-in-the-cli/v1) (version 1.7.0 and above)
- [Authentication](/docs/headless-cms/cli-authentication/v1) to use CLI
- A [configured management token](/docs/headless-cms/cli-authentication/v1#add-management-token)

## Commands

To perform bulk publish and unpublish operations on entries and assets, there are a series of commands that you need to run in the CLI.

Let's discuss them in detail.

> **Additional Resource:** Contentstack CLI lets you configure rate limits for various bulk publishing operations. Read more about [using rate limits for enhanced bulk publishing control](/docs/headless-cms/configure-rate-limits-in-the-cli/v1#using-rate-limits-for-enhanced-bulk-publishing-control).

### Bulk Publish All Entries

The `cm:entries:publish` command lets you publish multiple entries on multiple environments for specific locales.

**Usage:**

```
csdx cm:entries:publish --content-types <content_type_uid> --locales <locale_code> -e <environment_name> --stack-api-key <source_stack_api_key>
```

> **Note**: To avoid bulk publish failure, we recommend you to bulk publish content of one content type at a time.

**Options:**

- `--content-types=content-types`: The UID of the content type(s) whose entries you want to publish in bulk. In case of multiple content types, specify the IDs separated by spaces.
- `--locales=locales`: Locales in which entries will be published, e.g., *en-us*. In the case of multiple locales, specify the codes separated by spaces.
- `-e`, `--environments=environments`: The name of the environment on which entries will be published. In case of multiple environments, specify their names separated by spaces.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don't mention the branch name, then by default, the content from the **main** branch will be published.
- `--publish-all-content-types`: *(optional)* Set it to **true** to bulk publish entries from all content types. If the `--content-types` option is already used, then you cannot use this option.
- `--api-version=api-version`: API version to be used. Values \[Default: 3, Nested Reference Publishing: 3.2\].
- `--bulk-publish=bulk-publish`: Set this flag to use Contentstack's Bulk Publish APIs. It is **true,** by default.
- `--retry-failed=retry-failed`: *(optional)* Use this option to retry publishing the failed entries/ assets from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [configure](#build-the-configuration-file) command to create a configuration file.

### Bulk Publish Edited Entries

The `cm:entries:publish-modified` command lets you publish recently edited entries on a particular environment.

**Usage:**

```
csdx cm:entries:publish-modified --content-types <content_type_uid> --source-env <source_environment_name> -e <environment_name>  --locales <locale_code> --stack-api-key <stack_api_key>
```

**Options:**

- `--content-types=content-types`: The UID of the content type(s) whose edited entries you want to publish in bulk. In case of multiple content types, specify the IDs separated by spaces.
- `--source-env=source-env`: The name of the source environment where the entries were initially published.
- `-e`, `--environments=environments`: The name of the environment(s) on which the entries will be published. In case of multiple environments, specify their names separated by spaces.
- `--locales=locales`: Locales in which entries will be published, e.g., *en-us*. In the case of multiple locales, specify the codes separated by spaces.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don't mention the branch name, then by default the entries from the **main** branch will be published.
- `--api-version=api-version`: API version to be used. Values \[Default: 3, Nested Reference Publishing: 3.2\].
- `--bulk-publish=bulk-publish`: Set this flag to use Contentstack's Bulk Publish APIs. It is **true,** by default.
- `--retry-failed=retry-failed`: *(optional)* Use this option to retry publishing the failed entries/assets from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [configure](#build-the-configuration-file) command to create a configuration file.

### Bulk Publish Draft Entries

The `cm:entries:publish-only-unpublished` command lets you publish the unpublished or draft entries on any environment(s).

**Usage:**

```
csdx cm:entries:publish-only-unpublished  --content-types <content_type_uid> --source-env <source_environment_name> -e <environment_name>  --locales <locale_code> --stack-api-key <stack_api_key>
```

**Options:**

- `--content-types=content-types`: The UID of the content type(s) whose entries you want to publish in bulk. In case of multiple content types, specify their IDs separated by spaces.
- `--source-env=source-env`: The name of the source environment where the entries were initially published.
- `-e`, `--environments=environments`: The name of the environment on which entries will be published. In case of multiple environments, specify their names separated by spaces.
- `--locales=locales`: Locale in which entries will be published, e.g., *en-us*
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don't mention the branch name, then by default the entries from the **main** branch will be published.
- `--api-version=api-version`: API version to be used. Values \[Default: 3, Nested Reference Publishing: 3.2\].
- `--bulk-publish=bulk-publish`: Set this flag to use Contentstack's Bulk Publish APIs. It is **true,** by default.
- `--retry-failed=retry-failed`: *(optional)* Use this option to retry publishing the failed entries from the logfile. It is optional. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [configure](#build-the-configuration-file) command to create a configuration file.

### Bulk Publish All Assets

The `cm:assets:publish` command lets you publish all assets of a particular stack on any environment(s).

**Usage:**

```
csdx cm:assets:publish -e <environment_name> --locales <locale_code> --stack-api-key <stack_api_key>
```

**Options:**

- `-e`, `--environments=environments`: The name of the environment on which entries will be published. In case of multiple environments, specify their names separated by spaces.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don't mention the branch name, then by default the assets from the **main** branch will be published.
- `--api-version=api-version`: API version to be used. Values \[Default: 3, Nested Reference Publishing: 3.2\].
- `--bulk-publish=bulk-publish`: Set this flag to use Contentstack's Bulk Publish APIs. It is **true,** by default.
- `--retry-failed=retry-failed`: *(optional)* Use this option to retry publishing the failed assets from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `--folder-uid=folder-uid`: *(optional)* The UID of the Assets' folder from which the assets need to be published. The default value is **cs_root**.
- `--backup-dir=backup-dir`: *(optional)* Path to the import backup directory. When set, each imported asset is published only to the environments and locales it was published to in the source stack, read from the backup's publish details and asset UID mapping. Exclusive with `--source-env`, `--folder-uid`, `--environments`, and `--locales`. Use this option for the post-import publish flow described in [Import Content Using the CLI](/docs/headless-cms/import-content-using-the-cli/v1).
- `--locales=locales`: Locales in which assets will be published, e.g., *en-us*. In the case of multiple locales, specify the codes separated by spaces.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [configure](#build-the-configuration-file) command to create a configuration file.

**Asset Scan Skip Behavior:** If asset scanning is enabled for the stack, `cm:assets:publish` skips quarantined assets permanently and skips in-queue (pending) assets with no automatic retry. Wait for scanning to finish, then rerun the command to publish a skipped asset.

**Additional Resources:** For more information, refer to the [Asset Scanning in CLI](/docs/headless-cms/asset-scanning-in-cli/v1) documentation.

### Bulk Publish Entries/Assets from One Environment to Another

The `cm:entries:publish` and `cm:assets:publish` commands let you publish all the entries and assets respectively, from one environment to a newly created or some other environment.

**Usage:**

```
csdx cm:entries:publish --source-env <environment_name> --delivery-token <delivery_token> -e <destination_environment_name> --content-types <content_type_uid> --locales <locale_code> --stack-api-key <stack_api_key>
```

or

```
csdx cm:assets:publish --source-env <environment_name> --delivery-token <delivery_token> -e <destination_environment_name> --content-types <content_type_uid> --locales <locale_code> --stack-api-key <stack_api_key>
```

**Options:**

- `-e`, `--environments=environments`: Target environment.
- `--content-types=content-types`: The UID of the content type ID whose entries you want to publish in bulk. In case of multiple content types, specify their IDs separated by spaces.
- `--locales=locales`: Locale in which entries will be published, e.g., *en-us*
- `--api-version=api-version`: API version to be used. Values \[Default: 3, Nested Reference Publishing: 3.2\].
- `--bulk-publish=bulk-publish`: Set this flag to use Contentstack's Bulk Publish APIs. It is **true,** by default.
- `--delivery-token=delivery-token`: The delivery token of the source environment.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `--retry-failed=retry-failed` *(optional):* Use this option to retry publishing the failed entries from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don't mention the branch name, then by default the content from the **main** branch will be published.
- `--source-env=source-env`: Source environment.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config` *(optional):* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [configure](#build-the-configuration-file) command to create a configuration file.

### Bulk Publish All Entries after Adding a New Field in the Content Type

If you add a new field(s) to one or more content types, you have to update and publish the corresponding entries manually. To automate this process, the `cm:entries:update-and-publish` command lets you update and publish such entries in bulk.

**Usage:**

```
csdx cm:entries:update-and-publish --content-types <content_type_uid> --locales <locale_code> -e <environment_name> --stack-api-key <stack_api_key>
```

**Options:**

- `--content-types=content-types`: The UID of the content type ID whose entries you want to publish in bulk. In case of multiple content types, specify their IDs separated by spaces.
- `--locales=locales`: Locales in which entries will be published, e.g., *en-us*. In the case of multiple locales, specify the codes separated by spaces.
- `-e`, `--environments=environments`: The name of the environment on which entries will be published. In case of multiple environments, specify their names separated by spaces.
- `--api-version=api-version`: API version to be used. Values \[Default: 3, Nested Reference Publishing: 3.2\].
- `--bulk-publish=bulk-publish`: Set this flag to use Contentstack's Bulk Publish APIs. It is **true,** by default.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don't mention the branch name, then by default the content from the **main** branch will be published.
- `--retry-failed=retry-failed`: *(optional)* Use this option to retry publishing the failed entries from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [configure](#build-the-configuration-file) command to create a configuration file.

### Bulk Publish Entries after Non-localized Field is Updated

The `cm:entries:publish-non-localized-fields` command lets you publish the localized entries if the non-localized field of the master entry is updated.

**Usage:**

```
csdx cm:entries:publish-non-localized-fields --content-types <content_type_uid> --source-env <source_environment_name> -e <environment_name> --stack-api-key <stack-api-key>
```

**Options:**

- `--content-types=content-types`: The UID of the content type whose entries you want to publish in bulk. In case of multiple content types, specify their IDs separated by spaces.
- `--source-env=source-env`: The name of the source environment.
- `-e`, `--environments=environments`: The name of the environment on which entries will be published. In case of multiple environments, specify their names separated by spaces.
- `--api-version=api-version`: API version to be used. Values \[Default: 3, Nested Reference Publishing: 3.2\].
- `--bulk-publish=bulk-publish`: Set this flag to use Contentstack's Bulk Publish APIs. It is **true,** by default.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don't mention the branch name, then by default the content from the **main** branch will be published.
- `--retry-failed=retry-failed`: *(optional)* Use this option to retry publishing the failed entries from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [configure](#build-the-configuration-file) command to create a configuration file.

### Restore/Unpublish Entries Published

The `cm:stacks:publish-revert` command lets you unpublish the published entries and restore their version back to 1.

**Usage:**

```
csdx cm:stacks:publish-revert --log-file "<logfile_path>"
```

**Options:**

- `--log-file=log-file`: Path of the success logfile of a particular publish action.
- `--retry-failed=retry-failed`: *(optional)* Use this option to retry publishing the failed entries from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.

### Bulk Unpublish Entries/Assets

The `cm:entries:unpublish` and `cm:assets:unpublish` commands let you unpublish entries and assets respectively, of given content types from a given environment.

**Usage:**

```
csdx cm:entries:unpublish -e <environment_name> --locale <locale_code> --stack-api-key <stack_api_key>
```

or

```
csdx cm:assets:unpublish -e <environment_name> --locale <locale_code> --stack-api-key <stack_api_key>
```

**Options:**

- `-e`, `--environment=environment`: The name of the environment from where entries/assets need to be unpublished.
- `--locale=locale`: Locale from which entries/assets will be unpublished, e.g., *en-us*
- `--content-type=content-type`: The UID of the content type whose entries you want to unpublish in bulk.
- `--api-version=api-version`: API version to be used. Values \[Default: 3, Nested Reference Publishing: 3.2\].
- `--bulk-unpublish=bulk-unpublish`: Set this flag to use Contentstack's Bulk Publish APIs. It is **true,** by default.
- `--delivery-token=delivery-token`: The delivery token of the source environment.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `--branch=branch`: The name of the branch where you want to perform the bulk unpublish operation. If you don't mention the branch name, then by default the content from the **main** branch will be unpublished.
- `--retry-failed=retry-failed`: *(optional)* Use this option to retry unpublishing the failed entries from the logfile. Specify the name of the logfile that lists failed unpublish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* Path of an optional configuration JSON file containing all the options for a single run. Refer to the [configure](#build-the-configuration-file) command to create a configuration file.

### Bulk Publish All Entries Including Variants

The `cm:entries:publish` command allows you to publish multiple entries with associated [variant entries](/docs/headless-cms/about-entry-variants) on multiple environments for specific locales.

**Usage:**

```
csdx cm:entries:publish --content-types <content_type_uid> --locales <locale_code> -e <environment_name> --stack-api-key <source_stack_api_key> --include-variants
```

> **Note**: To avoid any failure during the bulk publish operation, it is recommended to bulk publish content of one content type at a time.

**Options:**

- `--content-types=content-types`: The UID of the content type(s) whose entries you want to publish in bulk. In case of multiple content types, specify the IDs separated by spaces.
- `--locales=locales`: Locales in which entries will be published, e.g., *en-us*. In the case of multiple locales, specify the codes separated by spaces.
- `-e`, `--environments=environments`: The name of the environment on which entries will be published. In case of multiple environments, specify their names separated by spaces.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don't mention the branch name, then by default the content from the **main** branch will be published.
- `--publish-all-content-types`: *(optional)* Set it to **true** to bulk publish entries from all content types. If the `--content-types` option is already used, then you cannot use this option.
- `--api-version=api-version`: API version to be used. Values \[Default: 3, Nested Reference Publishing: 3.2\].
- `--bulk-publish=bulk-publish`: Set this flag to use Contentstack's Bulk Publish APIs. It is **true,** by default.
- `--retry-failed=retry-failed`: *(optional)* Use this option to retry publishing the failed entries/ assets from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [configure](#build-the-configuration-file) command to create a configuration file.
- `--include-variants`: Set this flag to bulk publish variant entries.

### Bulk Publish Entry with Variants

The `cm:entries:publish` command allows you to publish a single base entry with their associated [variant entries](/docs/headless-cms/about-entry-variants) on multiple environments for specific locales.

**Usage:**

```
csdx cm:entries:publish --content-types <content_type_uid> --locales <locale_code> -e <environment_name> --stack-api-key <source_stack_api_key> --entry-uid <base_entry_uid> --include-variants
```

> **Note**: To avoid any failure during the bulk publish operation, it is recommended to bulk publish content of one content type at a time.

**Options:**

- `--content-types=content-types`: The UID of the content type(s) whose entries you want to publish in bulk. In case of multiple content types, specify the IDs separated by spaces.
- `--locales=locales`: Locales in which entries will be published, e.g., *en-us*. In the case of multiple locales, specify the codes separated by spaces.
- `-e`, `--environments=environments`: The name of the environment on which entries will be published. In case of multiple environments, specify their names separated by spaces.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don't mention the branch name, then by default the content from the **main** branch will be published.
- `--publish-all-content-types`: *(optional)* Set it to **true** to bulk publish entries from all content types. If the `--content-types` option is already used, then you cannot use this option.
- `--api-version=api-version`: API version to be used. Values \[Default: 3, Nested Reference Publishing: 3.2\].
- `--bulk-publish=bulk-publish`: Set this flag to use Contentstack's Bulk Publish APIs. It is **true,** by default.
- `--retry-failed=retry-failed`: *(optional)* Use this option to retry publishing the failed entries/ assets from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [configure](#build-the-configuration-file) command to create a configuration file.
- `--entry_uid`: The UID of the base entry whose variant entries you want to publish in bulk.
- `--include-variants`: Set this flag to bulk publish variant entries.

### Bulk Unpublish Entries with Variants

The `cm:entries:unpublish` command allows you to unpublish entries and their associated [variant entries](/docs/headless-cms/about-entry-variants) for specific content types from a given environment.

**Usage:**

```
csdx cm:entries:unpublish -e <environment_name> --locale <locale_code> --stack-api-key <stack_api_key> --include-variants
```

**Options:**

- `-e`, `--environment=environment`: The name of the environment from where entries/assets need to be unpublished.
- `--locale=locale`: Locale from which entries/assets will be unpublished, e.g., *en-us*
- `--content-type=content-type`: The UID of the content type whose entries you want to unpublish in bulk.
- `--api-version=api-version`: API version to be used. Values \[Default: 3, Nested Reference Publishing: 3.2\].
- `--bulk-unpublish=bulk-unpublish`: Set this flag to use Contentstack's Bulk Publish APIs. It is **true,** by default.
- `--delivery-token=delivery-token`: The delivery token of the source environment.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `--branch=branch`: The name of the branch where you want to perform the bulk unpublish operation. If you don't mention the branch name, then by default the content from the **main** branch will be unpublished.
- `--retry-failed=retry-failed`: *(optional)* Use this option to retry unpublishing the failed entries from the logfile. Specify the name of the logfile that lists failed unpublish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* Path of an optional configuration JSON file containing all the options for a single run. Refer to the [configure](#build-the-configuration-file) command to create a configuration file.
- `--include-variants`: Set this flag to bulk publish variant entries.

### Build the Configuration File

The `cm:stacks:publish-configure` command lets you generate a template for the configuration JSON file. It will set the variables for the Bulk Publish commands.

After you generate the configuration file, you can simply use its path in the `-c` , `--config=config` option of any Bulk Publish commands. You can view this [reference configuration file](https://github.com/contentstack/cli-plugins/blob/main/packages/contentstack-bulk-operations/src/config/index.ts) for Bulk Publish commands.

**Usage:**

```
csdx cm:stacks:publish-configure --stack-api-key <stack_api_key>
```

**Option:**

- `-a`, `--alias=alias`: Name (alias) of the management token you want to use. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.

## Troubleshooting

### Assets remain unpublished after `cm:assets:publish --backup-dir`

**Root Cause(s)**: Asset scanning found the asset still in the scan queue at the time the command ran. The retry mechanism for in-queue assets is disabled in this release, so the asset is skipped immediately instead of being retried.

**Resolution**: Wait for the asset's scan to complete, then run `cm:assets:publish --backup-dir <BACKUP_DIR>` again. Assets are not retried automatically within a single command run.

### `csdx cm:assets:publish --data-dir ...` reports an unrecognized flag

**Root Cause(s)**: A message printed at the end of asset import (from `cm:stacks:import`) tells you to run `csdx cm:assets:publish --data-dir <BACKUP_DIR> ...` to publish assets after scanning. `cm:assets:publish` does not have a `--data-dir` flag.

**Resolution**: Use `--backup-dir` instead: `csdx cm:assets:publish --backup-dir <BACKUP_DIR> --stack-api-key <STACK_API_KEY>`.

### Import prints an asset-scanning message but the org does not have asset scanning enabled

**Root Cause(s)**: The reminder to run `cm:assets:publish --backup-dir` after import is printed whenever assets were imported and `skipAssetsPublish` is set, including when `--skip-assets-publish` was passed manually and asset scanning played no part. The message text does not distinguish the two cases.

**Resolution**: Check whether `--skip-assets-publish` was passed explicitly. If it was, the message is unrelated to asset scanning and assets can be published normally with `csdx cm:assets:publish --backup-dir <BACKUP_DIR> --stack-api-key <STACK_API_KEY>` at any time.

## Limitations

- The [cm:bulk-publish:add-fields](#bulk-publish-all-entries-after-adding-a-new-field-in-the-content-type) command does not work for [custom](/docs/headless-cms/custom) and [mandatory](/docs/headless-cms/mandatory) fields.
- To manage API request timing and prevent concurrency issues, add the `delayMs` parameter to your configuration file to add controlled delays between requests. For example, use `delayMs: 1000` (for 1-second delays).
- On stacks with asset scanning enabled, `cm:assets:publish` does not retry assets that are still in the scan queue. See [Assets remain unpublished after cm:assets:publish --backup-dir](#assets-remain-unpublished-after) for the resolution.
