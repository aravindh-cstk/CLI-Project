---
uid: "blt7cd9c7438ee7322e"
seo_title: "Bulk Publish and Unpublish Content | V0.x.x | Contentstack"
seo_description: "Use the CLI to bulk publish and unpublish entries and assets in Contentstack, streamlining content deployment across environments."
---

# Bulk Publish and Unpublish Content | Old Commands

The Bulk Publish and Unpublish commands allow you to publish entries and assets from multiple content types to one or more environments.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- CLI [installed](/docs/headless-cms/install-the-cli/v1) on your machine
- [Authentication](https://www.contentstack.com/docs/headless-cms/cli-authentication/v0) to use CLI
- A [configured management token](/docs/headless-cms/cli-authentication/v0#add-token)

## Commands

To perform bulk publish and unpublish operations on entries and assets, there are a series of commands that you need to run in the CLI.

Let's discuss them in detail.

### Bulk Publish All Entries

The `cm:bulk-publish:entries` command lets you publish multiple entries on multiple environments for specific locales.

**Usage**

```
csdx cm:bulk-publish:entries -t <content_type_uid> -l <locale_code> -e <environment_name>
```

> **Note**: To avoid bulk publish failure, we recommend you to bulk publish content of one content type at a time.

**Options**

- `-t`, `--contentTypes=contentTypes`: The UID of the content type(s) whose entries you want to publish in bulk. In case of multiple content types, specify the IDs separated by spaces.
- `-l`, `--locales=locales`: Locales in which entries will be published, e.g., *en-us*. In the case of multiple locales, specify the codes separated by spaces.
- `-e`, `--environments=environments`: The name of the environment on which entries will be published. In case of multiple environments, specify their names separated by spaces.
- `-a`, `--alias=alias`: Alias (name) of the management token.
- `-B`, `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don’t mention the branch name, then by default the content from the **main** branch will be published.
- `-o`, `--publishAllContentTypes`: *(optional)* Set it to **true** to bulk publish entries from all content types. If the **contentTypes** option is already used, then you cannot use this option.
- `-b`, `--[no-]bulkPublish=bulkPublish`: Set this flag to use Contentstack’s Bulk Publish APIs. It is **true,** by default.
- `-r`, `--retryFailed=retryFailed`: *(optional)* Use this option to retry publishing the failed entries/assets from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [**configure**](#build-the-configuration-file) command to create a configuration file.

### Bulk Publish Edited Entries

The `cm:bulk-publish:entry-edits` command lets you publish recently edited entries on a particular environment.

**Usage**

```
csdx cm:bulk-publish:entry-edits -t <content_type_uid> -s <source_environment_name> -e <environment_name>  -l <locale_code>
```

**Options**

- `-t`, `--contentTypes=contentTypes`: The UID of the content type(s) whose edited entries you want to publish in bulk. In case of multiple content types, specify the IDs separated by spaces.
- `-s`, `--sourceEnv=sourceEnv`: The name of the source environment where the entries were initially published.
- `-e`, `--environments=environments`: The name of the environment(s) on which the entries will be published. In case of multiple environments, specify their names separated by spaces.
- `-l`, `--locales=locales`: Locales in which entries will be published, e.g., *en-us*. In the case of multiple locales, specify the codes separated by spaces.
- `-a`, `--alias=alias`: Alias (name) of the management token.
- `-B`, `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don’t mention the branch name, then by default the entries from the **main** branch will be published.
- `-b`, `--[no-]bulkPublish=bulkPublish`: Set this flag to use Contentstack’s Bulk Publish APIs. It is **true,** by default.
- `-r`, `--retryFailed=retryFailed`: *(optional)* Use this option to retry publishing the failed entries/assets from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [**configure**](#build-the-configuration-file) command to create a configuration file.

### Bulk Publish Draft Entries

The `cm:bulk-publish:unpublished-entries` command lets you publish the unpublished or draft entries on any environment(s).

**Usage**

```
csdx cm:bulk-publish:unpublished-entries  -t <content_type_uid> -s <source_environment_name> -e <environment_name>  -l <locale_code>
```

**Options**

- `-t`, `--contentTypes=contentTypes`: The UID of the content type(s) whose entries you want to publish in bulk. In case of multiple content types, specify their IDs separated by spaces.
- `-s`, `--sourceEnv=sourceEnv`: The name of the source environment where the entries were initially published.
- `-e`, `--environments=environments`: The name of the environment on which entries will be published. In case of multiple environments, specify their names separated by spaces.
- `-l`, `--locale=locale`: Locale in which entries will be published, e.g., *en-us.*
- `-a`, `--alias=alias`: Alias (name) of the management token.
- `-B`, `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don’t mention the branch name, then by default the entries from **main** branch will be published.
- `-b`, `--[no-]bulkPublish=bulkPublish`: Set this flag to use Contentstack’s Bulk Publish APIs. It is **true,** by default.
- `-r`, `--retryFailed=retryFailed`: *(optional)* Use this option to retry publishing the failed entries from the logfile. It is optional. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)*  The path of the optional configuration JSON file containing all the options for a single run. Refer to the [**configure**](#build-the-configuration-file) command to create a configuration file.

### Bulk Publish All Assets

The `cm:bulk-publish:assets` command lets you publish all assets of a particular stack on any environment(s).

**Usage**

```
csdx cm:bulk-publish:assets -e <environment_name> --stack-api-key <stack_api_key>
```

**Options**

- `-e`, `--environments=environments`: The name of the environment on which entries will be published. In case of multiple environments, specify their names separated by spaces.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `-B`, `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don’t mention the branch name, then by default the assets from **main** branch will be published.
- `-b`, `--[no-]bulkPublish=bulkPublish`: Set this flag to use Contentstack’s Bulk Publish APIs. It is **true,** by default.
- `-r`, `--retryFailed=retryFailed`: *(optional)*  Use this option to retry publishing the failed assets from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-u`, `--folderUid=folderUid`: *(optional)*  The UID of the Assets’ folder from which the assets need to be published. The default value is **cs_root**.
- `-l`, `--locales=locales`: Locales in which assets will be published, e.g., *en-us*. In the case of multiple locales, specify the codes separated by spaces.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [**configure**](#build-the-configuration-file) command to create a configuration file.

### Bulk Publish Entries/Assets from One Environment to Another

The `cm:bulk-publish:cross-publish` command lets you publish all the entries and assets from one environment to a newly created or some other environment.

**Usage**

```
csdx cm:bulk-publish:cross-publish -e <environment_name> -d <destination_environment_name> -t <content_type_uid> -l <locale_code> --stack-api-key <stack_api_key> --onlyAssets
```

**Options**

- `-e`, `--environment=environment`: The name of the source Environment.
- `-d`, `--destEnv=destEnv`: The name of destination Environment.
- `-t`, `--content-type=content-type`: The UID of the Content Type ID whose entries you want to publish in bulk. In case of multiple Content Types, specify their IDs separated by spaces.
- `-l`, `--locale=locale`: Locale in which entries will be published, e.g., *en-us.*
- `-b`, `--[no-]bulkPublish=bulkPublish`: Set this flag to use Contentstack’s Bulk Publish APIs. It is **true,** by default.
- `-x`, `--deliveryToken=deliveryToken`: The delivery token of the source Environment.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag to publish assets. Use the `--alias` flag to publish entries.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag to publish assets.
- `-B`, `--branch=branch`: Branch to fetch the content from (default = main).
- `-r`, `--retryFailed=retryFailed` *(optional):*  Use this option to retry publishing the failed entries from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config` *(optional):* The path of the optional configuration JSON file containing all the options for a single run. Refer to the [**configure**](#build-the-configuration-file) command to create a configuration file.
- `--onlyAssets` *(optional)*: Use this flag to cross-publish only assets from the source environment.
- `--onlyEntries` *(optional)*: Use this flag to cross-publish only entries (all the entries) from the source environment.

### Bulk Publish All Entries After Adding a New Field in the Content Type

If you add a new field(s) to one or more content types, you have to update and publish the corresponding entries manually. To automate this process, the `cm:bulk-publish:add-fields` command lets you update and publish such entries in bulk.

**Usage**

```
csdx cm:bulk-publish:add-fields -t <content_type_uid> -l <locale_code> -e <environment_name>
```

**Options**

- `-t`, `--contentTypes=contentTypes`: The UID of the Content Type ID whose entries you want to publish in bulk. In case of multiple Content Types, specify their IDs separated by spaces.
- `-l`, `--locales=locales`: Locales in which entries will be published, e.g., *en-us*. In the case of multiple locales, specify the codes separated by spaces.
- `-e`, `--environments=environments`: The name of the environment on which entries will be published. In case of multiple environments, specify their names separated by spaces.
- `-b`, `--[no-]bulkPublish=bulkPublish`: Set this flag to use Contentstack’s Bulk Publish APIs. It is **true,** by default.
- `-a`, `--alias=alias`: Alias (name) of the management token.
- `-B`, `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don’t mention the branch name, then by default the content from **main** branch will be published.
- `-r`, `--retryFailed=retryFailed`: *(optional)*  Use this option to retry publishing the failed entries from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)*  The path of the optional configuration JSON file containing all the options for a single run. Refer to the [**configure**](#build-the-configuration-file) command to create a configuration file.

### Bulk Publish Entries After Non-localized field is Updated

The `cm:bulk-publish:nonlocalized-field-changes` command lets you publish the localized entries if the non-localized field of the master entry is updated.

**Usage**

```
csdx cm:bulk-publish:nonlocalized-field-changes -t <content_type_uid> -s <source_environment_name> -e <environment_name> -a <management_token_alias>
```

**Options**

- `-t`, `--contentTypes=contentTypes`: The UID of the Content Type whose entries you want to publish in bulk. In case of multiple Content Types, specify their IDs separated by spaces.
- `-s`, `--sourceEnv=sourceEnv`: The name of the source environment.
- `-e`, `--environments=environments`: The name of the environment on which entries will be published. In case of multiple environments, specify their names separated by spaces.
- `-b`, `--[no-]bulkPublish=bulkPublish`: Set this flag to use Contentstack’s Bulk Publish APIs. It is **true,** by default.
- `-a`, `--alias=alias`: Alias (name) of the management token.
- `-B`, `--branch=branch`: The name of the branch where you want to perform the bulk publish operation. If you don’t mention the branch name, then by default the content from **main** branch will be published.
- `-r`, `--retryFailed=retryFailed`: *(optional)*  Use this option to retry publishing the failed entries from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)*  The path of the optional configuration JSON file containing all the options for a single run. Refer to the [**configure**](#build-the-configuration-file) command to create a configuration file.

### Restore/Unpublish Entries Published

The `cm:bulk-publish:revert` command lets you unpublish the published entries and restore their version back to 1.

**Usage**

```
csdx cm:bulk-publish:revert -l <logfile_path>
```

**Options**

- `-l`, `--logFile=logFile`: Path of the success logfile of a particular publish action.
- `-r`, `--retryFailed=retryFailed`: *(optional)*  Use this option to retry publishing the failed entries from the logfile. Specify the name of the logfile that lists failed publish calls. If this option is used, it will override all other flags.

### Bulk Unpublish Entries/Assets

Unpublishing multiple entries/assets from several content types manually can be a time-consuming task. To ease this process, the `cm:bulk-publish:unpublish` command lets you unpublish all the entries/assets at once.

> **Note**: Use `--onlyAssets` option for unpublishing only assets and `--onlyEntries` for unpublishing only entries. If you do not specify either of these options, all the assets and entries will get unpublished at a time.

**Usage**

```
csdx cm:bulk-publish:unpublish -e <environment_name> -l <locale_code> --stack-api-key <stack_api_key> --onlyAssets
```

**Options**

- `-e`, `--environment=environment`: The name of the environment from where entries/assets need to be unpublished.
- `-l`, `--locale=locale`: Locale from which entries/assets will be unpublished, e.g., *en-us.*
- `-t`, `--contentType=contentType`: The UID of the content type whose entries you want to unpublish in bulk.
- `--onlyAssets`: *(optional)* Use this option to unpublish only assets.
- `--onlyEntries`: *(optional)* Use this option to unpublish only entries.
- `-b`, `--[no-]bulkUnpublish=bulkUnpublish`: Set this flag to use Contentstack’s Bulk Publish APIs. It is **true,** by default.
- `-x`, `--deliveryToken=deliveryToken`: The delivery token of the source environment.
- `-a`, `--alias=alias`: Alias (name) of the management token. You must use either the `--alias` flag or the `--stack-api-key` flag to unpublish assets. Use the `--alias` flag to unpublish entries.
- `--stack-api-key=stack-api-key`: API key of the source stack. You must use either the `--stack-api-key` flag or the `--alias` flag to unpublish assets.
- `-B`, `--branch=branch`: The name of the branch where you want to perform the bulk unpublish operation. If you don’t mention the branch name, then by default the content from **main** branch will be unpublished.
- `-r`, `--retryFailed=retryFailed`: *(optional)*  Use this option to retry unpublishing the failed entries from the logfile. Specify the name of the logfile that lists failed unpublish calls. If this option is used, it will override all other flags.
- `-y`, `--yes`: Set it to **true** to process the command with the current configuration.
- `-c`, `--config=config`: *(optional)*  Path of an optional configuration JSON file containing all the options for a single run. Refer to the [**configure**](#build-the-configuration-file) command to create a configuration file.

### Build the Configuration File

The `cm:bulk-publish:configure` command lets you generate a template for the configuration JSON file. It will set the variables for the Bulk Publish commands.

After you generate the configuration file, you can simply use its path in the `-c`, `--config=config` option of any Bulk Publish commands. You can view this [reference configuration file](https://github.com/contentstack/cli/blob/main/packages/contentstack-bulk-publish/src/config/index.js) for Bulk Publish commands.

**Usage**

```
csdx cm:bulk-publish:configure
```

**Options**

- `-a`, `--alias=alias`: Name (alias) of the management token you want to use

> **Additional Resources**: If you want to migrate your content from one stack to another, refer to the [Migration](/docs/headless-cms/migrate-your-content-using-the-cli-migration-command/v0) guide.

## Limitations

- The [cm:bulk-publish:add-fields](#bulk-publish-all-entries-after-adding-a-new-field-in-the-content-type) command does not work for [custom](/docs/headless-cms/custom) and [mandatory](/docs/headless-cms/mandatory) fields.
