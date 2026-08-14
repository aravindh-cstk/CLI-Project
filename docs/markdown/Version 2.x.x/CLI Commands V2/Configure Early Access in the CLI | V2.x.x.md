---
uid: "blt275d7d8eb02308f3"
seo_title: "Configure Early Access in the CLI | V2.x.x | Contentstack"
seo_description: "Learn how to configure and use the Early Access header in Contentstack Command-line Interface with this clear, step-by-step setup guide."
---

# Configure Early Access in the CLI

Contentstack’s **Early Access** program provides customers with the opportunity to explore Contentstack's products and features before they are generally available. Through this program, users can engage in collaborative communication with the product teams, enabling them to test and influence the development of products tailored to their organization's unique requirements.

The configuration of headers in a Command Line Interface (CLI) involves the setting of HTTP headers when interacting with web services or APIs through the command line. The Early Access header support in CLI includes commands to set, get and remove headers for requests made to web servers or APIs for Contentstack products and features before they are generally available.

This step-by-step guide lets you configure and use the Early Access header in the CLI.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- [CLI installed](/docs/headless-cms/install-the-cli) and [configured](/docs/headless-cms/configure-regions-in-the-cli) (version 1.12.1 and above)
- [CLI authenticated](/docs/headless-cms/cli-authentication)

## Commands

### Set Early Access Header

The `config:set:early-access-header` command lets you set an Early Access header with an alias name and value in the CLI.

1. Open the terminal.

2. Fire the following command:

   ```
   csdx config:set:early-access-header
   ```

3. Enter an **alias** name for the Early Access header.

4. Enter a **value** for the Early Access header.

You have successfully set an Early Access header in the CLI.

Alternatively, you can pass the **alias** and **value** in the command as given below:

```
csdx config:set:early-access-header  --header-alias <alias_name> --header <value>
```

**Usage**

```
csdx config:set:early-access-header
```

or

```
csdx config:set:ea-header
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--header-alias` | - | (Optional) Provide the Early Access header value. |
| `--header` | - | (Optional) Provide the Early Access header alias name. |

**Examples**

- To set an Early Access header by providing the header value:

  ```
  csdx config:set:early-access-header  --header 3.2
  ```

- To set an Early Access header by providing the header value and alias name:

  ```
  csdx config:set:early-access-header  --header-alias ta****my --header tx
  ```

### Get Early Access Header

The `config:get:early-access-header` command fetches a list of the Early Access headers that you have set in the CLI.

1. Open the terminal.

2. Fire the following command:

   ```
   csdx config:get:early-access-header
   ```

You have successfully retrieved a list of Early Access headers you have set in the CLI.

**Usage**

```
csdx config:get:early-access-header
```

or

```
csdx config:get:ea-header
```

### Remove Early Access Header

The `config:remove:early-access-header` command lets you remove an existing Early Access header configuration from the CLI.

1. Open the terminal.

2. Fire the following command:

   ```
   csdx config:remove:early-access-header
   ```

3. Enter the **alias** name of the Early Access header for which you want to remove the configuration.

4. In the prompt that appears, enter the following:
   - **Yes**, to remove the configuration of the provided Early Access header.
   - **No**, to skip removing the Early Access header configuration.

You have successfully removed the configuration of the provided Early Access header from the CLI.

**Usage**

```
csdx config:remove:early-access-header
```

or

```
csdx config:remove:ea-header
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--header-alias` | - | (Optional) Provide the Early Access header alias name. |
| `--yes` | `-y` | (Optional) Force the removal of Early Access header configuration by skipping the confirmation. |

**Examples**

- To remove the configuration of an Early Access header by skipping the confirmation:

  ```
  csdx config:remove:early-access-header  --yes
  ```

- To remove the configuration of an Early Access header by providing the header alias name:

  ```
  csdx config:remove:early-access-header  --header-alias ta****my
  ```
