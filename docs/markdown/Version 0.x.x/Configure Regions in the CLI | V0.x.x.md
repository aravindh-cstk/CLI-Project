---
uid: "bltb2a9262996cb0033"
seo_title: "Configure Regions in the CLI | V0.x.x | Contentstack"
seo_description: "Optimize your Contentstack CLI setup with region configuration."
---

# Configure Regions in the CLI

The **config** namespace contains all the commands that you will need to configure the CLI as per your requirements.

Contentstack currently supports three regions: **North America**, **Europe**, and Azure North America.

By default, the CLI uses the North American region. Configuration changes are not required for North America region users.

Using the following set of commands, you can configure the CLI to use other [regions](/docs/administration).

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- CLI [installed](/docs/headless-cms/install-the-cli/v1)
- [Authentication](/docs/headless-cms/cli-authentication/v0) to use CLI

## Commands

### Get region

The `config:get:region` command will return the name of the region on which you are performing actions in Contentstack, via CLI.

**Usage**

```
csdx config:get:region
```

### Set region

The `config:set:region` command lets you select a region, from the available [Contentstack regions](/docs/administration), to perform actions using CLI.

**Usage**

```
csdx config:set:region <Region>
```

**Arguments**

- Region: Specifies the region that you want to use while executing the CLI commands. Possible values are as follows:
  - `EU` for Europe
  - `AZURE-NA` for Azure North America
  - `NA` for North America

**Example**

```
csdx config:set:region EU
```

```
csdx config:set:region AZURE-NA
```

### Set custom host and region

By using the `config:set:region` command, you can also set a custom host for [Content Delivery](/docs/developers/apis/content-delivery-api/) and [Content Management](/docs/developers/apis/content-management-api/) APIs, and set a custom region name for the hosts.

**Usage**

```
csdx config:set:region -d <custom_cda_host_url> -m <custom_cma_host_url> -n <custom_region_name>
```

**Options**

- `-d`, `--cda=cda`: Custom host to set for the Content Delivery API. If this option is used, then cma and name options are required.
- `-m`, `--cma=cma`: Custom host to set for the Content Management API. If this option is used, then cda and name options are required.
- `-n`, `--name=name`: The name for the region. If this option is used, then cda and cma options are required

**Example**

```
csdx config:set:region -d "https://in-cda.contentstack.com" -m "https://in-api.contentstack.com" -n "India"
```
