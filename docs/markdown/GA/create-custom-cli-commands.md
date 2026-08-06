---
uid: "blt18f5edee45f9d6c2"
seo_title: "Write a Custom CLI Command | V1.x.x | Contentstack Documentation"
seo_description: "Write a Custom CLI Command"
---

# Create Custom CLI Commands

Contentstack allows developers to write plugins and add custom commands to the CLI. You can then install and use these plugins as required. In this guide, we will learn how to write a custom CLI plugin.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- [Node.js version 16 or above](https://nodejs.org/en/download/)
- CLI installed on your machine: **npm** **install -g @contentstack/cli**

## Use the “plugins:create” command

To get started with the custom plugin creation process, open your terminal (command prompt), and run the command given below:

```
csdx plugins:create
```

This will prompt you to provide the following details:

- Name for your custom plugin, for example, “myplugin”.
- Few lines of *optional* description for this custom plugin.
- Version of this plugin, for example, “v1.” By default, the initial format will be “0.0.0”.
- Name of the license for this plugin. By default, it’s “MIT”.
- Owner’s name of GitHub repository.
- Name of the GitHub repository.
- Preference to use Typescript - Yes/ No.
- Preference to use ESLint - Yes/ No.
- Preference to use Mocha - Yes/ No.

After you provide these details, it will generate a plugin boilerplate (initial code of the plugin). You will find a **hello.ts** (if you choose “Yes” for Typescript) or **hello.js** (if you choose “No” for Typescript) file in your working directory. This file contains the basic code required for plugin development.

You can tailor this code as per your requirements.

## Run the Code

To run the code, open your terminal, point it to the “\<\<plugin_name\>\>” directory (path of your plugin) created above, and run the command given below:

```
node bin/run hello
```

Next, let’s set up this plugin within the **csdx** [namespace](/docs/headless-cms/install-the-cli/v1#namespaces), by using the **plugins:link** command so that you don’t have to use the above command for running the plugin’s code.

## Set up the Plugin

When you develop the plugin locally, you can use the **plugins:link** command for setting up the plugin. To do this, open your terminal, point it to the “\<\<plugin_name\>\>” directory, and run the command given below:

```
csdx plugins:link
```

You can validate this setup by running this command:

```
csdx hello
```

After running this command, you’ll see your plugin’s output in the terminal.

## Register and Install the Plugin

You can register a new plugin command and use it as per your requirements.

To register a new plugin command first publish your plugin package on npm.

Once your plugin is published, run the following command:

```
csdx plugins: install
```

This will successfully install the plugin and you can use this custom plugin to execute your tasks.

## Uninstall the Plugin

If you have created or installed a plugin using [Contentstack CLI](/docs/headless-cms/install-the-cli/v1), and want to uninstall/ remove that plugin, you can do it by using the **plugins:uninstall** command.

> **Note**: This command will not delete the plugin’s code folder.

To do this, run the following commands in your terminal:

1. Get a list of plugins you have installed:

   ```
   csdx plugins
   ```

2. From the available plugins listed in the terminal, uninstall it by passing its name in the command below:

   ```
   csdx plugins:uninstall <<plugin_name>>
   ```

This will uninstall/ remove the plugin.
