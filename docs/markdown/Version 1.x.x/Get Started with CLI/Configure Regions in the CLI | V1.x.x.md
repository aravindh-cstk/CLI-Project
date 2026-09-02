---
uid: "bltbc6ad24437532c4f"
seo_title: "Configure Regions in the CLI | V1.x.x | Contentstack"
seo_description: "Configure regions in Contentstack Command-line Interface to optimize your setup and streamline workflows across multiple data centers."
---

# Configure Regions in the CLI

---

## Overview

The **config** namespace contains commands to configure the CLI. Contentstack supports multiple regions across different cloud providers. You can configure the CLI to use a specific region for all operations.

**Supported Regions:**

| Cloud Provider | Region | Argument |
| --- | --- | --- |
| AWS | North America | `AWS-NA` |
| AWS | Europe | `AWS-EU` |
| AWS | Australia | `AWS-AU` |
| Azure | North America | `AZURE-NA` |
| Azure | Europe | `AZURE-EU` |
| Google Cloud Platform | North America | `GCP-NA` |
| Google Cloud Platform | Europe | `GCP-EU` |

You can also configure custom hosts for different APIs and set a custom region name.

---

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- **CLI Installed:** Version 1.7.0 or above (see [Install the CLI](/docs/headless-cms/install-the-cli/v1))

## What You Will Learn

- How to view the region the CLI is currently using.
- How to set a predefined region for CLI operations.
- How to select a region interactively.
- How to configure a custom region with custom API hosts.

---

## Common Commands

### Get Current Region

```
csdx config:get:region
```

### Set Region

```
# Interactive selection
csdx config:set:region

# Or specify region directly
csdx config:set:region AWS-NA
```

---

## Get Region

Get the currently configured region.

**Command:** `csdx config:get:region`

**Usage:**

```
csdx config:get:region
```

**Example:**

```
csdx config:get:region
# Output: AWS-NA
```

---

## Set Region

Set the region for CLI operations. You can choose from predefined regions or configure custom hosts.

**Command:** `csdx config:set:region`

### Set Predefined Region

**Usage:**

```
csdx config:set:region <region>
```

**Available Regions:**

- `AWS-NA` - AWS North America
- `AWS-EU` - AWS Europe
- `AWS-AU` - AWS Australia
- `AZURE-NA` - Azure North America
- `AZURE-EU` - Azure Europe
- `GCP-NA` - Google Cloud Platform North America
- `GCP-EU` - Google Cloud Platform Europe

**Examples:**

```
# Set AWS North America
csdx config:set:region AWS-NA

# Set AWS Europe
csdx config:set:region AWS-EU

# Set AWS Australia
csdx config:set:region AWS-AU

# Set Azure North America
csdx config:set:region AZURE-NA

# Set Azure Europe
csdx config:set:region AZURE-EU

# Set GCP North America
csdx config:set:region GCP-NA

# Set GCP Europe
csdx config:set:region GCP-EU
```

### Interactive Region Selection

Run the command without arguments to interactively select a region:

```
csdx config:set:region
```

You'll be prompted to choose from available regions.

---

## Set Custom Host and Region

Configure custom hosts for Content Delivery API (CDA), Content Management API (CMA), UI Host, Developer Hub, Launch, and Personalize APIs, and set a custom region name.

**Command:** `csdx config:set:region`

**Usage:**

```
csdx config:set:region \
  --cda <custom_cda_host_url> \
  --cma <custom_cma_host_url> \
  --ui-host <custom_ui_host_url> \
  -n <custom_region_name> \
  [--developer-hub <custom_developer_hub_url>] \
  [--launch <custom_launch_url>] \
  [--personalize <custom_personalize_url>]
```

**Options:**

| Flag | Type | Required | Default | Description | Notes |
| --- | --- | --- | --- | --- | --- |
| `--cda`, `-d` | string | Conditional\* | - | Custom host for Content Delivery API. If used, `--cma`, `--ui-host`, and `-n` are required |  |
| `--cma`, `-m` | string | Conditional\* | - | Custom host for Content Management API. If used, `--cda`, `--ui-host`, and `-n` are required |  |
| `--ui-host` | string | Conditional\* | - | Custom UI host for CLI. If used, `--cda`, `--cma`, and `-n` are required |  |
| `--name`, `-n` | string | Conditional\* | - | Name for the custom region. If used, `--cda`, `--cma`, and `--ui-host` are required |  |
| `--developer-hub` | string | No | - | Custom host for Developer Hub API |  |
| `--launch` | string | No | - | Custom host for Launch API |  |
| `--personalize` | string | No | - | Custom host for Personalize Management API |  |

\* If any of `--cda`, `--cma`, `--ui-host`, or `-n` is used, all four are required.

> **Note:** When configuring a custom region, the CLI automatically generates Developer Hub, Launch, Personalize, and Asset Management API hosts from the CMA URL.

**Example:**

```
csdx config:set:region \
  --cda "https://in-cdn.contentstack.com" \
  --cma "https://in-api.contentstack.com" \
  --ui-host "https://in-app.contentstack.com" \
  --developer-hub "https://in-developerhub-api.contentstack.com" \
  --launch "https://in-launch-api.contentstack.com" \
  --personalize "https://in-personalize-api.contentstack.com" \
  -n "India"
```

---

## Examples

### Example 1: Configure Region for Different Environments

```
# Development - AWS North America
csdx config:set:region AWS-NA

# Staging - AWS Europe
csdx config:set:region AWS-EU

# Production - Azure North America
csdx config:set:region AZURE-NA
```

### Example 2: Configure Custom Region

```
# Set custom region with all required hosts
csdx config:set:region \
  --cda "https://custom-cdn.example.com" \
  --cma "https://custom-api.example.com" \
  --ui-host "https://custom-ui.example.com" \
  -n "Custom Region"
```

### Example 3: Configure Custom Region with Optional APIs

```
# Set custom region with Developer Hub, Launch, and Personalize
csdx config:set:region \
  --cda "https://custom-cdn.example.com" \
  --cma "https://custom-api.example.com" \
  --ui-host "https://custom-ui.example.com" \
  --developer-hub "https://custom-developerhub.example.com" \
  --launch "https://custom-launch.example.com" \
  --personalize "https://custom-personalize.example.com" \
  -n "Custom Region"
```

### Example 4: Check Current Region

```
# Get current region
csdx config:get:region

# Change region
csdx config:set:region AWS-EU

# Verify change
csdx config:get:region
```

---

> **Additional Resource**
>
> For more information, refer to the following documents:
>
> - [Install the CLI](/docs/headless-cms/install-the-cli/v1)
> - [CLI Authentication and Adding Tokens](/docs/headless-cms/cli-authentication/v1)
> - [Configure Rate Limits in the CLI](/docs/headless-cms/configure-rate-limits-in-the-cli/v1)
> - [Contentstack Regions](/docs/administration/about-regions)
