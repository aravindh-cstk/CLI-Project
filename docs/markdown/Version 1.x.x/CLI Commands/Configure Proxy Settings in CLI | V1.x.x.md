---
uid: "bltd66941065e0c9244"
seo_title: "Configure Proxy Settings in CLI | V1.x.x | Contentstack"
seo_description: "Configure HTTP or HTTPS proxy settings in the Contentstack CLI using global config or environment variables to ensure reliable API access behind firewalls."
---

# Configure Proxy Settings in CLI

Configure a proxy to control how the Contentstack CLI routes network requests. Use this setup when working behind corporate firewalls or restricted networks.

This guide provides step-by-step instructions on how to configure and manage proxy settings in the Contentstack Command Line Interface (CLI).

## Overview

- How to configure and manage proxy settings for the Contentstack CLI using global configuration and environment variables
- How proxy configuration precedence works between environment variables and CLI global config when connecting to Contentstack APIs

> **Note:** The CLI supports proxy configuration through both global config and environment variables. Environment variables (`HTTPS_PROXY` or `HTTP_PROXY`) take priority over global config settings.

## Quick Reference

| Task | Command |
| --- | --- |
| Set proxy | ``` csdx config:set:proxy --host <host> --port <port> ``` |
| Get proxy | ``` csdx config:get:proxy ``` |
| Remove proxy | ``` csdx config:remove:proxy ``` |

## Prerequisites

- **Contentstack CLI installed and configured**
  - CLI version **1.55.0** or above (see [Install the CLI](/docs/headless-cms/install-the-cli/v1))

- **Proxy server details**
  - Proxy host
  - Proxy port
  - Proxy protocol (http or https)
  - Proxy authentication details (username and password), if required

Having these details upfront helps you choose the correct configuration method and avoid connectivity issues later.

## Commands

### Set Proxy Configuration

The `config:set:proxy` command lets you set proxy configuration for the CLI in the global config.

1. Enter the following command with required flags:

```
csdx config:set:proxy --host <host> --port <port> --protocol <protocol>
```

2. If your proxy requires authentication, include the `--username` flag. The CLI prompts you to enter the password securely.

With these steps, you have successfully set proxy configuration in the CLI. After you set the proxy, the CLI routes requests through the proxy stored in global configuration.

**Usage**

```
csdx config:set:proxy
```

**Options**

- `--host`: (required) Proxy host address
- `--port`: (required) Proxy port number (must be between 1 and 65535)
- `--protocol`: (required) Proxy protocol - either `http` or `https`
- `--username`: (optional) Proxy username for authentication

**Examples**

- To set a basic proxy configuration:

  ```
  csdx config:set:proxy --host 127.0.0.1 --port 3128
  ```

  When you omit the `--username` flag, the proxy is configured without authentication.

- To set a proxy with HTTPS protocol:

  ```
  csdx config:set:proxy --host proxy.example.com --port 8080 --protocol https
  ```

- To set a proxy with authentication:

  ```
  csdx config:set:proxy --host proxy.example.com --port 8080 --username user
  ```

  When you include the `--username` flag, the CLI prompts you to enter the password securely.

### Get Proxy Configuration

The `config:get:proxy` command fetches the proxy configuration that you have set in the global config.

1. Open the terminal.
2. Enter the following command:

```
csdx config:get:proxy
```

You can now view the proxy configuration currently stored in the CLI global config.

**Usage**

```
csdx config:get:proxy
```

**Output**

- Host
- Port
- Protocol
- Username (if configured)
- Password (displayed as `***` if configured)

> **Note:**
>
> - This command only displays proxy configuration stored in the global config.
> - If no proxy configuration is found in the global config, the command does not display any output.
> - Proxy settings from environment variables (`HTTPS_PROXY`, `HTTP_PROXY`) are not displayed by this command but are used if present.

### Remove Proxy Configuration

The `config:remove:proxy` command lets you remove an existing proxy configuration from the global config.

1. Open the terminal.
2. Enter the following command:

```
csdx config:remove:proxy
```

The proxy configuration has been removed from the CLI global config, and the CLI no longer uses it unless a proxy is set via environment variables.

**Usage**

```
csdx config:remove:proxy
```

**Examples**

```
csdx config:remove:proxy
```

> **Note:**
>
> - This command only removes the proxy configuration from the global config.
> - Proxy settings from environment variables (`HTTPS_PROXY`, `HTTP_PROXY`) are used if present.
> - If no proxy configuration exists in the global config, the command completes without error.

## Using Environment Variables for Proxy Configuration

In addition to the global config, you can also configure proxy settings using environment variables. Environment variables take priority over global config settings.

### Setting Environment Variables

**macOS/Linux:** Add the following to your `~/.zshrc`, `~/.bashrc` or `~/.profile` file:

```
export HTTPS_PROXY=http://proxy.example.com:8080
```

or

```
export HTTP_PROXY=http://proxy.example.com:8080
```

For authenticated proxies:

```
export HTTPS_PROXY=http://<username>:<password>@proxy.example.com:<port>
```

**Windows:** Set via System Properties or PowerShell:

```
$env:HTTPS_PROXY="http://proxy.example.com:8080"
```

or

```
$env:HTTP_PROXY="http://proxy.example.com:8080"
```

For authenticated proxies:

```
$env:HTTPS_PROXY="http://<username>:<password>@proxy.example.com:<port>"
```

### Priority Order

The CLI determines which proxy configuration to use in the following order:

1. Environment variables (`HTTPS_PROXY` or `HTTP_PROXY`) — highest priority
2. Global configuration (set via `config:set:proxy`) - lower priority

If both are configured, the CLI uses the proxy settings defined in the environment variables.
