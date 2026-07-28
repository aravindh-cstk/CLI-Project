---
uid: "blt88f14f6af9eca1d9"
seo_title: "Export Content using the CLI | Old Commands | Contentstack"
seo_description: "Efficiently export content using Contentstack's CLI commands."
---

# Export Content using the CLI | Old Commands

If you want to migrate your content from one [stack](/docs/headless-cms/about-stack) to another, you need to export the content from the source stack and then import it into the destination stack.

You can export the following modules from a stack:

- [Assets](/docs/headless-cms/about-assets/)
- [Locales](/docs/headless-cms/about-languages)
- [Environments](/docs/headless-cms/about-environments)
- [Extensions](/docs/developers/experience-extensions-overview)
- [Webhooks](/docs/headless-cms/about-webhooks)
- [Global Fields](/docs/headless-cms/about-global-field)
- [Content Types](/docs/headless-cms/about-content-types)
- [Entries](/docs/headless-cms/about-entries/)
- [Labels](/docs/headless-cms/about-labels)
- [Workflow](/docs/headless-cms/about-workflows)

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- CLI [installed](/docs/headless-cms/install-the-cli)
- A [configured management token](/docs/headless-cms/cli-authentication#add-token) (alias) or [authtoken](/docs/headless-cms/cli-authentication#login)

## Commands

The `cm:export` command lets you export content from one stack to another.

Below we have listed down how you can use the `cm:export` command:

- [Export Content Using Management Token and Parameters](#export-content-using-management-token-and-parameters)
- [Export Content Using Management Token and Config file](#export-content-using-management-token-and-config-file)
- [Export Content Using Auth Token and Parameters](#export-content-using-auth-token-and-parameters)
- [Export Content Using Auth Token and Config file](#export-content-using-auth-token-and-config-file)

Let us understand in detail how you can export content from your stack.

### Export Content Using Management Token and Parameters

This command lets you export content using a management token. For ease, you can pass several parameters/options to this command at once.

> **Tip**: To store the exported content efficiently, create a folder named “content” in your system and make a note of its path

**Usage**

```
csdx cm:export -a <management_token_alias>
```

Alternatively, refer to the following command to add several parameters/options in a single line:

```
csdx cm:export -a <management_token_alias> -d <file_path>
```

**Options**

- `-a`, `--management-token-alias=management-token-alias`: The management token of the source stack from which you will export content
- `-d`, `--data=data`: The path or the location in your file system to store the exported content. For e.g., *./content*
- `-B`, `--branch=branch`: The name of the branch where you want to export your content. If you don’t mention the branch name, then by default the content will be exported from **all** the branches of your stack.
- `-m`, `--module=module`: (optional) Specify a module to export to the source stack. If not specified, the export command will export all the modules to the stack. The available modules are *assets, content-types, entries, environments, extensions, global-fields, labels, locales*, *webhooks,* and *workflows.*

**Examples**:

- To export all modules from a stack:

  ```
  csdx cm:export -a mytoken  -d "C:\Users\Name\Desktop\cli\content"
  ```

- To export all modules from a particular branch of your stack(For example: **develop**).

  ```
  csdx cm:export -a mytoken -d "C:\Users\Name\Desktop\cli\content" -B develop
  ```

- To export only content types from a stack:

  ```
  csdx cm:export -a mytoken  -d "C:\Users\Name\Desktop\cli\content" -m content-types
  ```

  OR

  ```
  csdx cm:export -a mytoken  -d "C:\Users\Name\Desktop\cli\content" --module content-types
  ```

- To export only environments from a stack:

  ```
  csdx cm:export -a mytoken  -d "C:\Users\Name\Desktop\cli\content" -m environments
  ```

  OR

  ```
  csdx cm:export -a mytoken  -d "C:\Users\Name\Desktop\cli\content" --module environments
  ```

> **Note**: When exporting modules individually, make sure you follow this module sequence: **assets \> environments \> locales \> extensions \> webhooks \> global-fields \> content-types \> workflows \> entries \> labels.** For example, before exporting entries, you must have had exported assets, environments, locales, extensions, webhooks, global-fields, content-types, and workflows.

### Export Content Using Management Token and Config file

This command lets you export content to your stack using a management token and a configuration file containing the parameters/options and their associated value.

To get started with this command, download this [config file](https://github.com/contentstack/cli-plugins/tree/main/packages/contentstack-import/example_config), add values to this file, and note down the path where you have saved this file. By doing so, you don’t need to provide parameters/options in the command separately.

> **Tip**: To store the exported content efficiently, create a folder named “content” in your system and make a note of its path.

**Usage**

```
csdx cm:export -a <management_token_alias> -c <config_file_path>
```

**Options**

- `-a`, `--management-token-alias=management-token-alias`: The management token of the source stack from which you will export content
- `-c`, `--config=config`: The path of the configuration JSON file containing all the options for a single run. You can refer to an [example config file here](https://github.com/contentstack/cli-plugins/tree/main/packages/contentstack-export/example_config).

**Example**

- To export content using a config file:

  ```
  csdx cm:export -a mytoken -c “C:/Users/Name/Desktop/cli/config.json”
  ```

### Export Content Using Auth Token and Parameters

You can use this method to export content to your stack if you have logged in to the session using the [Login](https://www.contentstack.com/docs/headless-cms/cli-authentication/#login) command. Running the Login command generates an auth token, which is used in the command below.

> **Tip**: To store the exported content efficiently, create a folder named “content” in your system and note its path.

**Usage**

```
csdx cm:export -A
```

Alternatively, refer to the below command for adding several parameters/options in a single line:

```
csdx cm:export -A -s <stack_ApiKey> -d <file_path>
```

**Options**

- `-A`, `--auth-token`: To use the auth token of the current session. It is automatically generated and stored in the session after running the login command.

- `-d`, `--data=data`: The path or the location in your file system to store the exported content. For e.g., *./content*

- `-s`, `--stack-uid=stack-uid`: The API key of the source stack.

- `-t`, `--content-type=contentType`: (optional) Content type.

- `-B`, `--branch=branch`: The name of the branch where you want to export your content. If you don’t mention the branch name, then by default the content will be exported from **all** the branches of your stack.

- `-m`, `--module=module` (*optional*): Specify the module to export to the source stack. If not specified, the export command will export all the modules to the stack. The available modules are *assets, content-types, entries, environments, extensions, global-fields, labels, locales*, *workflows, releases,* *webhooks,* and *workflows.*

- `--secured-assets`: Use this flag to export your content, if the [secured assets](/docs/administration#manage-asset-security) feature is enabled for your stack.

  > **Note**: Make sure to add the `--secured-assets` flag to avoid errors while exporting content for the stack where the [secured assets](/docs/administration#manage-asset-security) feature is enabled.

**Examples**

- To export all modules from a stack:

  ```
  csdx cm:export -A  -d "C:\Users\Name\Desktop\cli\content" -s bltxxxxxx
  ```

- To export all modules from a particular branch of your stack(For example: **develop**).

  ```
  csdx cm:export -A -d "C:\Users\Name\Desktop\cli\content" -s bltxxxxxx  -B develop
  ```

- To export only content types from a stack:

  ```
  csdx cm:export -A -d "C:\Users\Name\Desktop\cli\content" -m content-types -s bltxxxxxx
  ```

  OR

  ```
  csdx cm:export -A -d "C:\Users\Name\Desktop\cli\content" --module content-types -s bltxxxxxxxx
  ```

- To export only environments from a stack:

  ```
  csdx cm:export -A  -d "C:\Users\Name\Desktop\cli\content" -m environments -s bltxxxxxx
  ```

  OR

  ```
  csdx cm:export -A -d "C:\Users\Name\Desktop\cli\content" --module environments -s bltxxxxxxxx
  ```

- To export content from your stack where secured assets feature is enabled:

  ```
  csdx cm:export -A -d "C:\Users\Name\Desktop\cli\content" -s bltxxxxxx --secured-assets
  ```

> **Note**: When exporting  modules individually, make sure you follow this module sequence: **assets \> locales \> environments \> extensions \> webhooks \> global-fields \> content-types \> workflows \> entries \> labels**.  For example, before exporting entries, you must have had exported assets, environments, locales, extensions, webhooks, global-fields, content-types, and workflows.

### Export Content Using Auth Token and Config file

This command lets you export content to your stack using an auth token and a configuration file containing the parameters/options and their associated value.

To get started with this command, download this [config file](https://github.com/contentstack/cli-plugins/tree/main/packages/contentstack-import/example_config), add values to this file, and note down the path where you have saved this file.

By doing so, you don’t need to provide parameters/options in the command separately.

> **Tip**: To store the exported content efficiently, create a folder named “content” in your system and make a note of its path.

**Usage**

```
csdx cm:export -A -c <config_file_path>
```

**Options**

- `-A`, `--auth-token`: To use the auth token of the current session. It is automatically generated and stored in the session after running the login command.
- `-c`, `--config=config`: The path of the configuration JSON file containing all the options for a single run. You can refer to an [example config file](https://github.com/contentstack/cli-plugins/tree/main/packages/contentstack-export/example_config).

**Example**

- To export content using a config file:

  ```
  csdx cm:export -A -c “C:/Users/Name/Desktop/cli/config.json”
  ```

## Limitations

- For assets, if you are exporting two or more assets having the same UID and file name, then only the first asset in the queue will get exported.

- Currently, you cannot export content from the following modules:
  - [Roles](/docs/headless-cms/about-stack-roles)
  - [Users](/docs/headless-cms/about-stack-users)
  - [Releases](/docs/headless-cms/about-releases)

## Next Steps

- [Import the content in the stack](/docs/developers/cli/import-content-using-the-cli)
- [Audit Plugin](/docs/headless-cms/audit-plugin/)
