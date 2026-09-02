---
uid: "blt8cddf6452fd82024"
seo_title: "Migrate Content Between Stacks Using the CLI | V2.x.x | Contentstack"
seo_description: "Learn how to manually migrate content between Contentstack stacks with step-by-step instructions."
---

# Migrate Content Between Stacks Using the CLI

## Overview

This document guides you through the process of migrating content from one Contentstack stack to another manually.

> **Warning:** The export writes content flat into the folder you name. It does not create a `<branch-uid>/` subfolder, even when you pass `--branch`. Use the same path for the export and the import, and use a separate `--data-dir` per branch, because exporting a second branch into the same folder overwrites the first with no error.
>
> If you are importing an export produced by CLI V1, that layout did nest content under a branch subfolder. Point `--data-dir` at the subfolder itself, for example `./export/main`, because the automatic branch detection that V1 relied on has been removed.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli) and [configured](/docs/headless-cms/configure-regions-in-the-cli)
- CLI [authenticated](/docs/headless-cms/cli-authentication#authentication)
- Access to both source and target stacks
- An empty target stack

## Steps for Execution

To migrate all content from one stack to another quickly, follow the steps below:

- [Export](/docs/headless-cms/export-content-using-the-cli) from source stack:

  ```
  csdx cm:stacks:export -k <source_stack_api_key> --data-dir ./export --branch main
  ```

- [Audit](/docs/headless-cms/cli-audit-plugin) the exported content (recommended):

  ```
  csdx cm:stacks:audit --data-dir ./export
  ```

  > **Note:** The [audit](/docs/headless-cms/cli-audit-plugin) process runs automatically during [import](/docs/headless-cms/import-content-using-the-cli) to validate and fix any issues.

- [Import](/docs/headless-cms/import-content-using-the-cli) to target stack:

  ```
  csdx cm:stacks:import -k <target_stack_api_key> --data-dir ./export
  ```

## Behaviour to Check Before You Rely on the Result

- **Only the main branch is exported by default.** If you omit `--branch`, the export covers the branch named `main` and nothing else, and it fails when no such branch exists. Pass `--branch` once per branch to move a multi-branch stack.
- **Global fields from a V1 export are skipped silently.** If the folder you import came from CLI V1, every global field is skipped with no error and no warning, because V1 wrote them to a single aggregate file and the current importer reads one file per UID. The step reports success having created nothing. Re-export the source stack with the current CLI before importing.

## Next Steps

- [Export Content Using the CLI](/docs/headless-cms/export-content-using-the-cli): export stack content to disk before importing it elsewhere.
- [Audit Plugin](/docs/headless-cms/cli-audit-plugin): audit exported data for reference and field problems before importing it.
- [Import Content Using the CLI](/docs/headless-cms/import-content-using-the-cli): import exported content into a target stack.
- [CLI Limitations](/docs/headless-cms/cli-limitations): the coverage gaps and known constraints across CLI commands.
