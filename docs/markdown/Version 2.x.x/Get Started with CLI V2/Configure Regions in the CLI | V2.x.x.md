---
uid: "blt267c4988aa1389a5"
seo_title: "Configure Regions in the CLI | V2.x.x | Contentstack"
seo_description: "Configure regions in Contentstack Command-line Interface to optimize your setup and streamline workflows across multiple data centers."
---

# Configure Regions in the CLI

The **config** namespace contains all the commands that you will need to configure the CLI as per your requirements.

Contentstack currently supports the following regions:

| **Cloud Provider** | **Region** | **Arguments** |
| --- | --- | --- |
| AWS | North America | AWS-NA |
| AWS | Europe | AWS-EU |
| AWS | Australia | AWS-AU |
| Azure | North America | Azure-NA |
| Azure | Europe | Azure-EU |
| Google Cloud Platform | North America | GCP-NA |
| Google Cloud Platform | Europe | GCP-EU |

Using the following set of commands you can configure the [regions](/docs/administration) in the CLI.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- CLI [installed](/docs/headless-cms/install-the-cli)

## Commands

### Get region

The `config:get:region`command will return the name of the region on which you are performing actions in Contentstack, via the CLI.

**Usage**

```
csdx config:get:region
```

### Set region

The `config:set:region` command lets you select a region, from the available [Contentstack regions](/docs/administration), to perform actions using the CLI.

**Usage**

```
csdx config:set:region <<region>>
```

**Arguments**

- Region: Specifies the region that you want to use while executing the CLI commands. Possible values are as follows:
  - `AWS-NA` for AWS North America
  - `AWS-EU` for AWS Europe
  - `AWS-AU` for AWS Australia
  - `AZURE-NA` for Azure North America
  - `AZURE-EU` for Azure Europe
  - `GCP-NA` for Google North America
  - `GCP-EU` for Google Europe

**Example**

```
csdx config:set:region AWS-NA
```

```
csdx config:set:region AWS-EU
```

```
csdx config:set:region AWS-AU
```

```
csdx config:set:region AZURE-NA
```

```
csdx config:set:region AZURE-EU
```

```
csdx config:set:region GCP-NA
```

```
csdx config:set:region GCP-EU
```

### Set custom host and region

By using the `config:set:region` command, you can also set a custom host for [Content Delivery](/docs/developers/apis/content-delivery-api), [Content Management](/docs/developers/apis/content-management-api), UI Host, [Developer Hub](/docs/developer-hub/about-developer-hub/), [Launch](/docs/launch/about-launch/), [Personalize,](/docs/personalize/about-personalize) and [Studio](/docs/studio/about-studio) APIs, and set a custom region name for the hosts.

**Usage**

```
csdx config:set:region --cda <<custom_cda_host_url>> --cma <<custom_cma_host_url>> --ui-host <<custom_ui_host_url>> --name <<custom_region_name>>
--developer-hub <<custom_developer_hub_url>> --launch <<custom_launch_url>> --personalize <<custom_personalize_url>>
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--cda` | - | Custom host to set for the Content Delivery API.<br>If this flag is used, the following flags are required: `--cma`, `--ui-host`, `--name` |
| `--cma` | - | Custom host to set for the Content Management API.<br>If this flag is used, the following flags are required: `--cda`, `--ui-host`, `--name` |
| `--ui-host` | - | Custom UI host to set for the CLI.<br>If this flag is used, the following flags are required: `--cda`, `--cma`, `--name` |
| `--name` | - | Name for the region.<br>If this flag is used, the following flags are required: `--cda`, `--cma`, `--ui-host` |
| `--developer-hub` | - | Custom host to set for the Developer Hub API. |
| `--personalize` | - | Custom host to set for the Personalize API. |
| `--launch` | - | Custom host to set for the Launch API. |
| `--studio` | - | Custom host to set for the Studio API. |
| `--cs-assets` | - | Custom host for Contentstack Assets API. |
| `--auth-api` | - | Custom host for the Auth API. |

> **Note**: The CLI generates the Developer Hub, Launch, Studio and Personalize APIs by default unless their corresponding flags are passed.

**Example**

```
csdx config:set:region --cda "https://in-cdn.contentstack.com" --cma "https://in-api.contentstack.com" --ui-host "https://in-app.contentstack.com" --developer-hub "https://in-developerhub-api.contentstack.com" --launch "https://in-launch-api.contentstack.com" --personalize "https://in-personalize-api.contentstack.com" --name "India"
```
