---
uid: "blt91a20a3ff7b6e05d"
seo_title: "Install the CLI | V2.x.x | Contentstack"
seo_description: "Install and update the Contentstack CLI on macOS, Windows, and Linux with this step-by-step guide for cross-platform setup."
---

# Install the CLI

Contentstack CLI can be installed in macOS, Windows and Linux environments. In this guide, you will learn how to install and update command-line interface (CLI).

> **Warning:** During an npm install or update the `csdx` binary is briefly unavailable, for roughly 30 seconds on a typical machine. A CI pipeline that installs the CLI and invokes it in the very next step can fail with a command-not-found error. Add a readiness check such as `csdx --version` with a short retry loop rather than assuming the binary is ready the moment the install command exits.

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
  @contentstack/cli/<cli-version> win32-x64 node-v22.11.0

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

- `auth`: To perform [authentication-related](/docs/headless-cms/cli-authentication) activities.
- `cm`: To perform content management activities such as [bulk publish, bulk unpublish](/docs/headless-cms/bulk-operations-in-cli), [import](/docs/headless-cms/import-content-using-the-cli), [export](/docs/headless-cms/export-content-using-the-cli), [export-to-csv](/docs/headless-cms/cli-export-content-to-csv-file), [branches](/docs/headless-cms/compare-and-merge-branches-using-the-cli), and [migration](/docs/headless-cms/migrate-your-content-using-the-cli-migration-command) content.
- `help`: To list useful commands in the CLI.
- `launch`: To perform [Launch](/docs/launch/about-launch/) related operations.
- `plugins`: To list the installed plugins.
- `config`: To perform configuration related activities in the CLI.

> **Note**: The guide to create your own plugin within `csdx` is yet to come. But, as our CLI is built using the oclif package, you can create your custom plugin by referring to [oclif plugin documentation](https://oclif.io/docs/plugins).

Here are the commands within each namespace:

- **auth**
  - [csdx auth:login](/docs/headless-cms/cli-authentication#login)
  - [csdx auth:logout](/docs/headless-cms/cli-authentication#logout)
  - [csdx auth:tokens:list](/docs/headless-cms/cli-authentication#list-all-tokens)
  - [csdx auth:whoami](/docs/headless-cms/cli-authentication#display-username-of-a-session)

- **cm**
  - [cm:branches:create](/docs/headless-cms/compare-and-merge-branches-using-the-cli#create-a-branch)
  - [cm:branches:delete](/docs/headless-cms/compare-and-merge-branches-using-the-cli#delete-a-branch)
  - [cm:branches:diff](/docs/headless-cms/compare-and-merge-branches-using-the-cli#steps-to-compare-branches)
  - [cm:branches:merge](/docs/headless-cms/compare-and-merge-branches-using-the-cli#steps-to-merge-branches)
  - [cm:stacks:bulk-assets](/docs/headless-cms/bulk-operations-in-cli)
  - [cm:stacks:bulk-entries](/docs/headless-cms/bulk-operations-in-cli)
  - [cm:stacks:bulk-taxonomies](/docs/headless-cms/bulk-operations-in-cli)
  - [cm:entries:migrate-html-rte](/docs/headless-cms/cli-migrate-content-from-html-rte-to-json-rte)
  - [cm:stacks:export](/docs/headless-cms/export-content-using-the-cli)
  - [cm:export-to-csv](/docs/headless-cms/cli-export-content-to-csv-file)
  - [cm:stacks:import](/docs/headless-cms/import-content-using-the-cli)
  - [cm:stacks:clone](/docs/headless-cms/cli-cloning-a-stack#use-the-stacks-clone-command)
  - [cm:stacks:migration](/docs/headless-cms/migrate-your-content-using-the-cli-migration-command)
  - [cm:stacks:seed](/docs/headless-cms/cli-import-content-using-the-seed-command#run-the-seed-command-using-the-management-token)
  - [cm:stacks:audit](/docs/headless-cms/cli-audit-plugin#issue-identification-in-references)
  - [cm:stacks:audit:fix](/docs/headless-cms/cli-audit-plugin#issue-resolution-in-references)

- **launch**
  - [csdx launch](/docs/headless-cms/cli-for-launch#steps-for-execution)
  - [csdx launch:logs](/docs/headless-cms/cli-for-launch#logs)
  - [csdx launch:functions](/docs/headless-cms/cli-for-launch#functions)
  - [csdx launch:deployments](/docs/headless-cms/cli-for-launch#deployments)
  - [csdx launch:environments](/docs/headless-cms/cli-for-launch#environments)
  - [csdx launch:open](/docs/headless-cms/cli-for-launch#open)

- **config**
  - [config:get:region](/docs/headless-cms/configure-regions-in-the-cli#get-region)
  - [config:get:base-branch](/docs/headless-cms/compare-and-merge-branches-using-the-cli#get)
  - [config:get:early-access-header](/docs/headless-cms/configure-early-access-program-in-the-cli#get-early-access-header)
  - [config:set:region](/docs/headless-cms/configure-regions-in-the-cli#set-region)
  - [config:set:base-branch](/docs/headless-cms/compare-and-merge-branches-using-the-cli#set)
  - [config:set:early-access-header](/docs/headless-cms/configure-early-access-program-in-the-cli#set-early-access-header)
  - [config:remove:base-branch](/docs/headless-cms/compare-and-merge-branches-using-the-cli#remove)
  - [config:remove:early-access-header](/docs/headless-cms/configure-early-access-program-in-the-cli#remove-early-access-header)

Refer the section below to check the CLI version on your machine and update it to use the latest version.

## Check CLI Version

To check the current version of CLI installed on your machine, run this command in the terminal:

```
csdx --version
```

Running this command will display the current version, as shown below:

```
C:\Users\vxxxh>csdx --version
@contentstack/cli/<cli-version> win32-x64 node-v22.11.0
```

## Update CLI Version

As mentioned above, you can check the version of CLI installed on your machine.  
To get the latest version of CLI, run the following command in your terminal:

```
npm update -g @contentstack/cli
```

## Next Step

- [CLI Authentication and Adding Tokens](/docs/headless-cms/cli-authentication)
