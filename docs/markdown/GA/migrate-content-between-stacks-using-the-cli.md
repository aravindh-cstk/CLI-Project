---
uid: "blt8e8d75af4f2678b0"
seo_title: "Migrate Content Between Stacks Using the CLI | Contentstack"
seo_description: "Learn how to manually migrate content between Contentstack stacks with step-by-step instructions."
---

# Migrate Content Between Stacks Using the CLI

This document guides you through the process of migrating content from one Contentstack stack to another manually.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli) and [configured](/docs/headless-cms/configure-regions-in-the-cli/)
- CLI [authenticated](/docs/headless-cms/cli-authentication#authentication)
- Access to both source and target stacks
- An empty target stack

## Steps for Execution

To migrate all content from one stack to another quickly, follow the steps below:

- [Export](/docs/headless-cms/export-content-using-the-cli) from source stack:

  ```
  csdx cm:stacks:export -k <source_stack_api_key> -d ./export --branch main
  ```

- [Audit](/docs/headless-cms/audit-plugin) the exported content (recommended):

  ```
  csdx cm:stacks:audit -d ./export/main
  ```

  > **Note:** The [audit](/docs/headless-cms/audit-plugin) process runs automatically during [import](/docs/headless-cms/import-content-using-the-cli) to validate and fix any issues.

- [Import](/docs/headless-cms/import-content-using-the-cli) to target stack:

  ```
  csdx cm:stacks:import -k <target_stack_api_key> -d ./export/main
  ```
