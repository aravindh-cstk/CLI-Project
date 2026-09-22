---
uid: "blt8012fa025c919ece"
seo_title: "Content Type Plugin | V2.x.x | Contentstack"
seo_description: "Use the Contentstack CLI Content Type Plugin | V2 Beta to audit schema changes before deploying to production and compare content models across versions or stacks."
---

# Content Type Plugin

## Overview

The content type plugin includes commands to inspect, compare, and visualize content types in a Contentstack [stack](/docs/headless-cms/about-stack) directly from the CLI. Use it to:

- Audit schema changes before deploying to production.
- Compare [content models](/docs/headless-cms/about-content-modeling) across versions or stacks.
- Generate visual documentation of your content architecture.

If you are upgrading from v1, see [Upgrading from v1](#upgrading-from-v1) for the flags that changed.

These commands only read your stack's content types. They don't write, update, or delete any content in your stack.

### Commands at a Glance

| Command | Description |
| --- | --- |
| `content-type:list` | List all content types in a stack |
| `content-type:details` | Display full schema details for a content type |
| `content-type:audit` | View recent audit log changes to a content type |
| `content-type:compare` | Diff two versions of the same content type |
| `content-type:compare-remote` | Diff the same content type across two stacks |
| `content-type:diagram` | Generate a Scalable Vector Graphics (SVG) or DOT (Graphviz DOT graph description language) diagram of your content model |

---

## Quick Reference

Find your starting point based on what you are doing.

| Use Case | Section | Key Call |
| --- | --- | --- |
| First time using the plugin | [Prerequisites](#prerequisites), then [Installation](#installation) | `csdx plugins:install contentstack-cli-content-type` |
| Your v1 scripts fail after upgrading to v2 | [Upgrading from v1](#upgrading-from-v1) | `--stack-api-key` / `--alias` (long-form flags) |
| List or inspect content types | [content-type:list](#content-typelist), [content-type:details](#content-typedetails) | `content-type:list` |
| Review or diff a schema change | [content-type:audit](#content-typeaudit), [content-type:compare](#content-typecompare) | `content-type:compare` |
| Compare a content type across two stacks | [content-type:compare-remote](#content-typecompare-remote) | `content-type:compare-remote` |
| A command returns an error | [Troubleshooting](#troubleshooting) | N/A |

---

## Prerequisites

- **Contentstack CLI v2 installed**: See [Install the Contentstack CLI](/docs/headless-cms/install-the-cli). This provides the `csdx` command used throughout this doc.

- **Plugin installed**: See [Installation](#installation). This adds the `content-type:*` commands to your CLI.

- **Authentication**: A saved management token alias or a stack API key. See [Authentication](#authentication). If using a management token, its [role](/docs/headless-cms/about-stack-roles) must grant `Content Type: Read` permission.

- **Region configured, if your stack is not in North America**: [Set your region](/docs/headless-cms/configure-regions-in-the-cli#set-region) before running any stack commands.

  ```
   csdx config:set:region
  ```

  This routes requests to the correct data center for your stack.

---

## Installation

1. Install the plugin:

   ```
   csdx plugins:install contentstack-cli-content-type
   ```

2. Verify:

   ```
   csdx plugins
   ```

---

## Commands

### content-type:list

List all content types in a stack.

**Syntax**

```
csdx content-type:list [FLAGS]
```

**Flags**

| Flag | Type | Required | Default | Description | Notes |
| --- | --- | --- | --- | --- | --- |
| `--stack-api-key`, `-k` | string | Yes (or `--alias`) | None | Stack API Key |  |
| `--alias`, `-a` | string | Yes (or `--stack-api-key`) | None | Alias of the management token |  |
| `--order` | string | No | `title` | Sort order: `title` or `modified` |  |

**Note**: Pass either `--stack-api-key` or `--alias`, not both. See [Authentication](#authentication) for the full enforcement table.

**Output**

Displays a table of all content types with their title, UID, and last modified date.

**Examples**

List all content types, sorted by title:

```
csdx content-type:list -a my-token-alias
```

List sorted by last modified:

```
csdx content-type:list -a my-token-alias --order modified
```

Using stack API key directly:

```
csdx content-type:list -k <stack-api-key>
```

---

### content-type:details

Display the full schema details of a specific content type.

**Syntax**

```
csdx content-type:details --content-type <uid> [FLAGS]
```

**Flags**

| Flag | Type | Required | Default | Description | Notes |
| --- | --- | --- | --- | --- | --- |
| `--stack-api-key`, `-k` | string | Yes (or `--alias`) | None | Stack API Key |  |
| `--alias`, `-a` | string | Yes (or `--stack-api-key`) | None | Alias of the management token |  |
| `--content-type` | string | Yes | None | content type UID |  |
| `--path` / `--no-path` | boolean | No | `true` | Show or hide the field path column |  |

**Output**

A structured table of the content type schema with columns for field title, UID, data type, and path (dot-notation path through nested structures). Use `--no-path` to hide the path column for a more compact view.

**Examples**

View full details for a content type:

```
csdx content-type:details -a my-token-alias --content-type home_page
```

Hide the path column:

```
csdx content-type:details -a my-token-alias --content-type home_page --no-path
```

Using stack API key:

```
csdx content-type:details -k <stack-api-key> --content-type blog_post
```

---

### content-type:audit

Display recent [audit log](/docs/headless-cms/monitor-stack-activities-in-audit-log) changes to a specific content type.

**Syntax**

```
csdx content-type:audit --content-type <uid> [FLAGS]
```

**Flags**

| Flag | Type | Required | Default | Description | Notes |
| --- | --- | --- | --- | --- | --- |
| `--stack-api-key`, `-k` | string | Yes (or `--alias`) | None | Stack API Key |  |
| `--alias`, `-a` | string | Yes (or `--stack-api-key`) | None | Alias of the management token |  |
| `--content-type` | string | Yes | None | content type UID |  |

**Output**

A table of audit log entries showing the action, the user who made the change, and the timestamp.

**Examples**

View audit log for a content type:

```
csdx content-type:audit -a my-token-alias --content-type home_page
```

Using stack API key:

```
csdx content-type:audit -k <stack-api-key> --content-type blog_post
```

---

### content-type:compare

Compare two versions of the same content type within a stack.

**Syntax**

```
csdx content-type:compare --content-type <uid> [FLAGS]
```

**Flags**

| Flag | Type | Required | Default | Description | Notes |
| --- | --- | --- | --- | --- | --- |
| `--stack-api-key`, `-k` | string | Yes (or `--alias`) | None | Stack API Key |  |
| `--alias`, `-a` | string | Yes (or `--stack-api-key`) | None | Alias of the management token |  |
| `--content-type` | string | Yes | None | content type UID |  |
| `--left` | integer | No | Latest version | Base version to compare from |  |
| `--right` | integer | No | `latest - 1` | Version to compare against |  |

**Note**: Provide `--left` and `--right` together. If omitted, the latest two versions are compared automatically.

**Output**

A diff table showing fields that were added, removed, or changed between the two versions.

**Examples**

Auto-compare latest two versions:

```
csdx content-type:compare -a my-token-alias --content-type home_page
```

Compare specific versions:

```
csdx content-type:compare -a my-token-alias --content-type home_page --left 5 --right 4
```

---

### content-type:compare-remote

Compare the same content type across two different stacks.

**Syntax**

```
csdx content-type:compare-remote --origin-stack <key> --remote-stack <key> --content-type <uid>
```

**Flags**

| Flag | Type | Required | Default | Description | Notes |
| --- | --- | --- | --- | --- | --- |
| `--origin-stack` | string | Yes | None | API Key of the origin stack (used for authentication) |  |
| `--remote-stack` | string | Yes | None | API Key of the remote stack |  |
| `--content-type` | string | Yes | None | content type UID to compare |  |

> **Note**: See the [Authentication Exception](#authentication-exception-content-typecompare-remote) for how this command authenticates.

**Output**

A diff table showing field-level differences between the same content type on two stacks.

**Examples**

```
csdx content-type:compare-remote \
  --origin-stack <origin-stack-api-key> \
  --remote-stack <remote-stack-api-key> \
  --content-type home_page
```

---

### content-type:diagram

Generate a visual diagram of all content types in a stack.

**Syntax**

```
csdx content-type:diagram --output <path> [FLAGS]
```

**Flags**

| Flag | Type | Required | Default | Description | Notes |
| --- | --- | --- | --- | --- | --- |
| `--stack-api-key`, `-k` | string | Yes (or `--alias`) | None | Stack API Key |  |
| `--alias`, `-a` | string | Yes (or `--stack-api-key`) | None | Alias of the management token |  |
| `--output` | string | Yes | None | Full path to the output file |  |
| `--direction` | string | No | `portrait` | Graph orientation: `portrait` or `landscape` |  |
| `--type` | string | No | `svg` | Output file type: `svg` or `dot` |  |

**Output**

Creates a file at the specified `--output` path. The file is either:

- **SVG** (default): a rendered visual graph, viewable in any browser or SVG viewer.
- **DOT**: a file in the DOT language, read by Graphviz, an open-source graph-visualization tool. Render it manually with `dot -Tpng content-model.dot -o content-model.png`.

The CLI always prints an absolute path here, regardless of whether you pass `--output` a relative or absolute path. On success, it prints something like:

```
Created Graph: /Users/you/project/content-model.svg
```

**Examples**

Generate SVG diagram:

```
csdx content-type:diagram -a my-token-alias --output ./content-model.svg
```

Landscape orientation:

```
csdx content-type:diagram -a my-token-alias --output ./content-model.svg --direction landscape
```

DOT file for further processing:

```
csdx content-type:diagram -a my-token-alias --output ./content-model.dot --type dot
```

---

## Authentication

Most commands support a management token alias or a stack API key. Whether `--stack-api-key` and `--alias` are mutually exclusive depends on the command. Pass only one flag regardless.

| Command | Enforces `--stack-api-key` / `--alias` as mutually exclusive | Result of passing both |
| --- | --- | --- |
| `content-type:list` | Yes | Command exits with an error |
| `content-type:audit` | Yes | Command exits with an error |
| `content-type:diagram` | Yes | Command exits with an error |
| `content-type:details` | No | Command runs, using one of the two values (unspecified which) |
| `content-type:compare` | No | Command runs, using one of the two values (unspecified which) |

**Option 1: Management Token Alias (Recommended)**

```
csdx auth:tokens:add -a my-token-alias -k <stack-api-key> --management --token <management-token>
```

Then use `-a my-token-alias` in any command that accepts `--alias`.

**Option 2: Stack API Key**

```
csdx content-type:list -k <stack-api-key>
```

### Authentication Exception: content-type:compare-remote

`content-type:compare-remote` does not accept `--alias` or `--stack-api-key`. It authenticates by taking both stack API keys directly, via `--origin-stack` (the origin/authenticating stack) and `--remote-stack` (the stack to compare against). Every other command in this doc that mentions this exception links back to this section rather than restating it.

---

## Examples

### Review a schema change

Who changed `blog_post` and when:

```
csdx content-type:audit -a my-token-alias --content-type blog_post
```

What exactly changed in the last update:

```
csdx content-type:compare -a my-token-alias --content-type blog_post
```

### Validate staging matches production

```
csdx content-type:compare-remote \
  --origin-stack <staging-key> \
  --remote-stack <production-key> \
  --content-type home_page
```

### Automate schema documentation

```
#!/bin/bash
set -euo pipefail

# Generate a landscape diagram and open it
csdx content-type:diagram \
  -a production-token \
  --output ./docs/content-model.svg \
  --direction landscape

open ./docs/content-model.svg
```

`set -euo pipefail` stops the script if `content-type:diagram` fails, so `open` never runs against a diagram that was not created.

---

## Upgrading from v1

v2 removes the deprecated flags and all command-specific short flags from v1. Only `-k` (`--stack-api-key`) and `-a` (`--alias`) remain as short flags. Replace each removed flag with its long form.

| v1 flag (removed) | Short in v1 | Use in v2 | Commands affected |
| --- | --- | --- | --- |
| `--stack` | `-s` | `--stack-api-key` (`-k`) | list, details, audit, compare, diagram |
| `--token-alias` | `-a` | `--alias` (`-a`) | list, details, audit, compare, diagram |
| `--content-type` short | `-c` | `--content-type` (long form) | details, audit, compare, compare-remote |
| `--left` / `--right` short | `-l` / `-r` | `--left` / `--right` (long form) | compare |
| `--origin-stack` / `--remote-stack` short | `-o` / `-r` | `--origin-stack` / `--remote-stack` (long form) | compare-remote |
| `--path` short | `-p` | `--path` / `--no-path` (long form) | details |
| `--output` / `--direction` / `--type` short | `-o` / `-d` / `-t` | `--output` / `--direction` / `--type` (long form) | diagram |
| `--order` short | `-o` | `--order` (long form) | list |

**Note**: `content-type:compare-remote` is the one exception to the retained short flags above. See [Authentication Exception](#authentication-exception-content-typecompare-remote).

---

## Limitations

- These commands compare and diagram schema only. They do not diff [entry](/docs/headless-cms/about-entries)-level content or data records.
- `content-type:diagram` writes a local SVG or DOT file. It is never uploaded or synced back to the stack.
- `content-type:compare` needs at least two saved versions of a content type. With only one version, it compares the version against itself and returns an empty diff. See [content-type:compare](#content-typecompare) for the single-version case.

---

## Next Steps

- [Content Type Plugin (v1)](/docs/headless-cms/cli-content-type-plugin): the v1 command reference, useful if you still run v1 or need the old flag names while upgrading.
- [Regex Validate Plugin (v2)](/docs/headless-cms/cli-regex-validate-plugin): scan your content types and [global fields](/docs/headless-cms/about-global-field) for regex patterns vulnerable to catastrophic backtracking.
- [Audit Plugin](/docs/headless-cms/cli-audit-plugin): a related Contentstack plugin for reviewing audit log activity across your stack.
- [CLI Authentication: Add Management Token](/docs/headless-cms/cli-authentication#add-management-token): create and save the management token alias these commands use.
- [Configure Regions in the CLI](/docs/headless-cms/configure-regions-in-the-cli#set-region): set your region if your stack is not in North America.
- [About Content Types](/docs/headless-cms/about-content-types): conceptual background on how content types and their fields are structured.
