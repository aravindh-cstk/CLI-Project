---
uid: "blt8e8d75af4f2678b0"
seo_title: "Migrate Content Between Stacks Using the CLI | V1.x.x | Contentstack"
seo_description: "Learn how to manually migrate content between Contentstack stacks with step-by-step instructions."
---

# Migrate Content Between Stacks Using the CLI

## Overview

This document guides you through the process of migrating content from one Contentstack stack to another manually.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli/v1) and [configured](/docs/headless-cms/configure-regions-in-the-cli/v1)
- CLI [authenticated](/docs/headless-cms/cli-authentication/v1#authentication)
- Access to both source and target stacks
- An empty target stack

## Steps for Execution

To migrate all content from one stack to another quickly, follow the steps below:

- [Export](/docs/headless-cms/export-content-using-the-cli/v1) from source stack:

  ```
  csdx cm:stacks:export -k <source_stack_api_key> -d ./export --branch main
  ```

- [Audit](/docs/headless-cms/cli-audit-plugin/v1) the exported content (recommended):

  ```
  csdx cm:stacks:audit -d ./export/main
  ```

  > **Note:** The [audit](/docs/headless-cms/cli-audit-plugin/v1) process runs automatically during [import](/docs/headless-cms/import-content-using-the-cli/v1) to validate and fix any issues.

- [Import](/docs/headless-cms/import-content-using-the-cli/v1) to target stack:

  ```
  csdx cm:stacks:import -k <target_stack_api_key> -d ./export/main
  ```

## Next Steps

- [Export Content Using the CLI](/docs/headless-cms/export-content-using-the-cli/v1): export stack content to disk before importing it elsewhere.
- [Audit Plugin](/docs/headless-cms/cli-audit-plugin/v1): audit exported data for reference and field problems before importing it.
- [Import Content Using the CLI](/docs/headless-cms/import-content-using-the-cli/v1): import exported content into a target stack.
- [Migrate from Contentstack CLI V1 to V2](/docs/headless-cms/cli-v1-to-v2-migration-guide): what changed at 2.0.0, flag by flag, and how to upgrade.
