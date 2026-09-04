---
uid: "bltdb5ced1cd5ecc104"
seo_title: "Configure Rate Limits in the CLI | V1.x.x | Contentstack"
seo_description: "Configure Contentstack CLI rate limits with csdx config:set:rate-limit. Manage bulkLimit, set utilization, and get or remove settings for bulk publishing control."
---

# Configure Rate Limits in the CLI

## Overview

[Rate Limit](/docs/developers/apis/content-management-api#rate-limiting) defines the maximum number of requests you can make using Contentstack's API within a specific time frame.

This guide provides step-by-step instructions on how to configure and manage rate limits in the Contentstack Command Line Interface (CLI).

By following these instructions, you can effectively control the number of requests made to the Contentstack API within a specified timeframe, ensuring optimal performance and preventing any disruptions due to exceeding rate limits.

> **Warning:** The CLI supports rate limit configuration only for the `bulkLimit` parameter, which is [used in bulk publish commands](/docs/headless-cms/configure-rate-limits-in-the-cli/v1#using-rate-limits-for-enhanced-bulk-publishing-control) to control requests.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- [CLI installed](/docs/headless-cms/install-the-cli/v1) and [configured](/docs/headless-cms/configure-regions-in-the-cli/v1) (version 1.25.0 and above)
- [CLI authenticated](/docs/headless-cms/cli-authentication/v1)

## Commands

### Set Custom Rate Limit

The `config:set:rate-limit` command lets you set a Custom rate limit for your organization in the CLI.

1. Open the terminal.

2. Enter the following command:

   ```
   csdx config:set:rate-limit
   ```

3. Then, enter the **organization UID**.

With these steps, you have successfully set a rate limit in the CLI.

To set a **Custom** rate limit, you can pass the **--limit-name** and **--utilize** flags along with the **--org** flag in the command as given below:

```
csdx config:set:rate-limit --org blt***********1b --utilize 60,80 --limit-name bulkLimit
```

**Usage**

```
csdx config:set:rate-limit
```

**Options**

- `--default`: (optional) Reset to default rate limit.
- `--limit-name`: (optional) Enter the limit names separated by commas \<options: limit|getLimit|bulkLimit\>.
- `--org`: Enter the organization UID.
- `--utilize=utilize`: \[default: 50\] Enter the utilization percentages for rate limit, separated by commas.

### Get the Rate Limit of an Organization

The `config:get:rate-limit` command fetches the rate limit that you have set in an organization in the CLI.

1. Open the terminal.

2. Enter the following command:

   ```
   csdx config:get:rate-limit
   ```

With these steps, you have successfully retrieved the rate limit you have set in the CLI.

**Usage**

```
csdx config:get:rate-limit
```

### Remove the Rate Limit of an Organization

The `config:remove:rate-limit` command lets you remove an existing rate limit configuration from the CLI.

1. Open the terminal.

2. Enter the following command:

   ```
   csdx config:remove:rate-limit
   ```

3. Then, enter the **organization UID**.

With these steps, you have successfully removed the rate limit configuration of an organization.

**Usage**

```
csdx config:remove:rate-limit
```

**Options**

- `--org`: Enter the organization UID.

## Using Rate Limits for Enhanced Bulk Publishing Control

By default, the rate limit is set to 1, letting you publish one asset or entry per second. To enable the bulk publish feature, you must configure the rate limit for your specific organization.

The `config:set:rate-limit` command lets you [set the rate limit](#set-custom-rate-limit) to utilize the bulk publish feature according to your plan.

**Usage**

```
csdx config:set:rate-limit  --org blt***********1b  --utilize 10 --limit-name bulkLimit
```

## Examples

**Set Custom Rate Limit**

- To set a default rate limit for your organization:

  ```
  csdx config:set:rate-limit  --org blt***********1b  --default
  ```

- To set a Custom rate limit for your organization:

  ```
  csdx config:set:rate-limit  --org blt***********1b  --utilize 60 --limit-name bulkLimit
  ```

> **Note:**
>
> - CLI applies a utilization percentage of your organization’s actual rate limit, based on your subscription plan.
> - By default, this is set to **50%**, which means the CLI internally enforces a limit at half of the available rate. For example, if your **getLimit** is **10**, the CLI will apply a **limit of 5** at **50% utilization**, or **6** at **60% utilization**.
> - This utilization is managed internally and is not shown in the CLI output.

**Remove the Rate Limit of an Organization**

- To remove the configuration of the rate limit from the CLI by providing the organization UID:

  ```
  csdx config:remove:rate-limit --org
  ```

## Limitations

- `--limit-name` accepts only `getLimit`, `limit`, and `bulkLimit`. No other API operation can be rate-limited individually through this command.
- `--utilize` must be a number between 0 and 100.
