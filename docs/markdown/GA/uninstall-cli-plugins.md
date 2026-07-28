---
uid: "blt553b89ec322a6199"
seo_title: "Uninstall CLI Plugins | Contentstack Documentation"
seo_description: "Steps to uninstall a CLI plugin"
---

# Uninstall CLI Plugins

If you have created or installed a plugin using [Contentstack CLI](/docs/headless-cms/install-the-cli), and want to uninstall/ remove that plugin, you can do it by using the **plugins:uninstall** command.

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
