---
uid: "blt0756f65e7c6f9eed"
seo_title: "Install the CLI | V1.x.x | Contentstack"
seo_description: "Install and update the Contentstack CLI on macOS, Windows, and Linux with this step-by-step guide for cross-platform setup."
---

# Install the CLI

Contentstack CLI can be installed in macOS, Windows and Linux environments. In this guide, you will learn how to install and update command-line interface (CLI).

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- [Node.js version 22 or later](https://nodejs.org/en/download/)

## Install CLI

To install CLI as a global module in your machine, open your terminal (command prompt) and run this command:

```
npm install -g @contentstack/cli
```

Once the CLI is successfully installed, you can use the `csdx` command from your terminal.

The `csdx` is a top-level **namespace** in Contentstack that gives you access to Contentstack's extensive range of commands and functionalities.

> **Additional Resource**: Visit our CLI [GitHub](https://github.com/contentstack/cli) page for more information. You can also read about Contentstack CLI on the [npm](https://www.npmjs.com/package/@contentstack/cli) page.

Next, let us verify the CLI installation.

## Verify installation

Verify your installation by running the following command in your terminal to get a list of commands that will help you to interact with Contentstack.

```
csdx --help
```

```
C:\Users\vxxxh>csdx --help
   ____            _             _       _             _
  / ___|___  _ __ | |_ ___ _ __ | |_ ___| |_ __ _  ___| | __
 | |   / _ \| '_ \| __/ _ \ '_ \| __/ __| __/ _` |/ __| |/ /
 | |__| (_) | | | | ||  __/ | | | |_\__ \ || (_| | (__|   <
  \____\___/|_| |_|\__\___|_| |_|\__|___/\__\__,_|\___|_|\_\

Command-line tool (CLI) to interact with Contentstack

VERSION
  @contentstack/cli/<cli-version> win32-x64 node-v20.10.0

USAGE
  $ csdx [COMMAND]

TOPICS
  auth     Perform authentication-related activities
  cm       Perform content management activities
  config   Perform configuration related activities
  launch   Launch related operations
  plugins  List installed plugins

COMMANDS
  help     Display help for csdx.
  launch   Launch related operations
  plugins  List installed plugins.
```

As shown in the above code, the `help` namespace contains other namespaces within it.  
Let us understand these namespaces in detail.

## Namespaces

Namespace is used to categorize commands as per their functionality or purpose.

The following namespaces exist within the `csdx` command:

- `auth`: To perform [authentication-related](/docs/headless-cms/cli-authentication/v1) activities.
- `cm`: To perform content management activities such as [bulk publish, bulk unpublish](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1), [import](/docs/headless-cms/import-content-using-the-cli/v1), [export](/docs/headless-cms/export-content-using-the-cli/v1), [export-to-csv](/docs/headless-cms/cli-export-content-to-csv-file/v1), [branches](/docs/headless-cms/compare-and-merge-branches-using-the-cli/v1), and [migration](/docs/headless-cms/migrate-your-content-using-the-cli-migration-command/v1) content.
- `help`: To list useful commands in the CLI.
- `launch`: To perform [Launch](/docs/launch/about-launch/) related operations.
- `plugins`: To list the installed plugins.
- `config`: To perform configuration related activities in the CLI.

> **Note:** To build your own plugin for `csdx`, see [Create Custom CLI Plugins for Contentstack](/docs/headless-cms/create-custom-cli-plugins/v1). The CLI is built on oclif, so the [oclif plugin documentation](https://oclif.io/docs/plugins) applies as well.

Here are the commands within each namespace:

- **auth**
  - [csdx auth:login](/docs/headless-cms/cli-authentication/v1#login)
  - [csdx auth:logout](/docs/headless-cms/cli-authentication/v1#logout)
  - [csdx auth:tokens](/docs/headless-cms/cli-authentication/v1#list-all-tokens)
  - [csdx auth:whoami](/docs/headless-cms/cli-authentication/v1#display-username-of-a-session)

- **cm**
  - [cm:assets:publish](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-publish-all-assets)
  - [cm:assets:unpublish](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-unpublish-entries-assets)
  - [cm:branches:create](/docs/headless-cms/compare-and-merge-branches-using-the-cli/v1#create-a-branch)
  - [cm:branches:delete](/docs/headless-cms/compare-and-merge-branches-using-the-cli/v1#delete-a-branch)
  - [cm:branches:diff](/docs/headless-cms/compare-and-merge-branches-using-the-cli/v1#steps-to-compare-branches)
  - [cm:branches:merge](/docs/headless-cms/compare-and-merge-branches-using-the-cli/v1#steps-to-merge-branches)
  - [cm:bulk-publish](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1)
  - [cm:bulk-publish:cross-publish](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-publish-entries-assets-from-one-environment-to-another)
  - [cm:entries:migrate-html-rte](/docs/headless-cms/cli-migrate-content-from-html-rte-to-json-rte/v1)
  - [cm:entries:publish](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-publish-all-entries)
  - [cm:entries:publish-modified](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-publish-edited-entries)
  - [cm:entries:publish-non-localized-fields](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-publish-entries-after-non-localized-field-is-updated)
  - [cm:entries:publish-only-unpublished](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-publish-draft-entries)
  - [cm:entries:unpublish](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-unpublish-entries-assets)
  - [cm:entries:update-and-publish](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-publish-all-entries-after-adding-a-new-field-in-the-content-type)
  - [cm:stacks:export](/docs/headless-cms/export-content-using-the-cli/v1)
  - [cm:export-to-csv](/docs/headless-cms/cli-export-content-to-csv-file/v1)
  - [cm:stacks:import](/docs/headless-cms/import-content-using-the-cli/v1)
  - [cm:stacks:clone](/docs/headless-cms/cli-cloning-a-stack/v1#use-the-stacks-clone-command)
  - [cm:stacks:migration](/docs/headless-cms/migrate-your-content-using-the-cli-migration-command/v1)
  - [cm:stacks:seed](/docs/headless-cms/cli-import-content-using-the-seed-command/v1#run-the-seed-command-using-the-management-token)
  - [cm:stacks:publish-configure](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#build-the-configuration-file)
  - [cm:stacks:publish-revert](/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#restore-unpublish-entries-published)
  - [cm:stacks:audit](/docs/headless-cms/cli-audit-plugin/v1#issue-identification-in-references)
  - [cm:stacks:audit:fix](/docs/headless-cms/cli-audit-plugin/v1#issue-resolution-in-references)

- **launch**
  - [csdx launch](/docs/headless-cms/cli-for-launch/v1#steps-for-execution)
  - [csdx launch:logs](/docs/headless-cms/cli-for-launch/v1#logs)
  - [csdx launch:functions](/docs/headless-cms/cli-for-launch/v1#functions)
  - [csdx launch:deployments](/docs/headless-cms/cli-for-launch/v1#deployments)
  - [csdx launch:environments](/docs/headless-cms/cli-for-launch/v1#environments)
  - [csdx launch:open](/docs/headless-cms/cli-for-launch/v1#open)

- **config**
  - [config:get:region](/docs/headless-cms/configure-regions-in-the-cli/v1#get-region)
  - [config:get:base-branch](/docs/headless-cms/compare-and-merge-branches-using-the-cli/v1#get)
  - [config:get:early-access-header](/docs/headless-cms/configure-early-access-program-in-the-cli/v1#get-early-access-header)
  - [config:set:region](/docs/headless-cms/configure-regions-in-the-cli/v1#set-region)
  - [config:set:base-branch](/docs/headless-cms/compare-and-merge-branches-using-the-cli/v1#set)
  - [config:set:early-access-header](/docs/headless-cms/configure-early-access-program-in-the-cli/v1#set-early-access-header)
  - [config:remove:base-branch](/docs/headless-cms/compare-and-merge-branches-using-the-cli/v1#remove)
  - [config:remove:early-access-header](/docs/headless-cms/configure-early-access-program-in-the-cli/v1#remove-early-access-header)

Refer the section below to check the CLI version on your machine and update it to use the latest version.

## Check CLI Version

To check the current version of CLI installed on your machine, run this command in the terminal:

```
csdx --version
```

Running this command will display the current version, as shown below:

```
C:\Users\vxxxh>csdx --version
@contentstack/cli/<cli-version> win32-x64 node-v20.10.0
```

## Update CLI Version

As mentioned above, you can check the version of CLI installed on your machine.  
To get the latest version of CLI, run the following command in your terminal:

```
npm update -g @contentstack/cli
```

## Next Steps

- [CLI Authentication and Adding Tokens](/docs/headless-cms/cli-authentication/v1): log in and add a management token before running any command.
- [Create Custom CLI Plugins for Contentstack](/docs/headless-cms/create-custom-cli-plugins/v1): build and publish your own `csdx` commands.
