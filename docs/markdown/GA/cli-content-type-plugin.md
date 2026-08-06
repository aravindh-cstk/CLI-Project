---
uid: "bltb2268be653f55338"
seo_title: "Content Type Plugin | V1.x.x | Contentstack"
seo_description: "Use the Contentstack CLI Content Type Plugin to audit logs, compare schema diffs across stacks, and visualize your content model with SVG/DOT diagrams."
---

# Content Type Plugin

A newer version of this plugin is available. See [Content Type Plugin (v2)](/docs/headless-cms/cli-content-type-plugin) for the current flag syntax before installing v1.

## Overview

The content type plugin provides commands to inspect, compare, and visualize content types in a [stack](/docs/headless-cms/about-stack) directly from the CLI. Use it to:

- Audit schema changes before deploying to production.
- Compare [content models](/docs/headless-cms/about-content-modeling) across versions or stacks.
- Generate visual documentation of your content architecture as a Scalable Vector Graphics (SVG) or DOT (Graphviz DOT graph description language) diagram.

### Commands at a Glance

These commands only read your stack's content types. They don't write, update, or delete any content in your stack.

| Command | Description |
| --- | --- |
| `content-type:list` | List all content types in a stack |
| `content-type:details` | Display full schema details for a content type |
| `content-type:audit` | View recent audit log changes to a content type |
| `content-type:compare` | Diff two versions of the same content type |
| `content-type:compare-remote` | Diff the same content type across two stacks |
| `content-type:diagram` | Generate an SVG or DOT diagram of your content model |

## Prerequisites

- **Contentstack CLI v1 installed**. See [Contentstack CLI installation](/docs/headless-cms/install-the-cli/v1):
- **Plugin installed**: See [Installation](#installation).
- **Authentication**: Either a saved management token alias or a stack API key. See [Authentication](#authentication). If using a management token, its [role](/docs/headless-cms/about-stack-roles) must grant `Content Type: Read` permission.
- **Region configured, if your stack is not in North America**. Requests default to the North America endpoint, so set your region if your stack is hosted elsewhere. See [Configure Regions in the CLI](/docs/headless-cms/configure-regions-in-the-cli/v1#set-region):

---

## Installation

1. Install the plugin:

   ```
    csdx plugins:install contentstack-cli-content-type
   ```

2. Verify the plugin is installed:

   ```
    csdx plugins
   ```

   You should see `contentstack-cli-content-type` in the list.

## Commands

### content-type:list

List all content types in a stack, ordered by title or last modified date.

#### Syntax

```
csdx content-type:list [FLAGS]
```

#### Flags

| Flag | Short | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `--stack-api-key` | `-k` | string | Yes (or `--alias`) | None | Stack API Key |
| `--alias` | `-a` | string | Yes (or `--stack-api-key`) | None | Alias of the management token |
| `--order` | None | string | No | `title` | Sort order: `title` or `modified` |

**Note**: Pass either `--stack-api-key` or `--alias`, not both. See [Authentication](#authentication) for the full enforcement table.

#### Output

Displays a table of all content types with their title, UID, and last modified date.

#### Examples

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

Display the full schema details of a specific content type, including all fields, their types, and reference paths.

#### Syntax

```
csdx content-type:details --content-type <uid> [FLAGS]
```

#### Flags

| Flag | Short | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `--stack-api-key` | `-k` | string | Yes (or `--alias`) | None | Stack API Key |
| `--alias` | `-a` | string | Yes (or `--stack-api-key`) | None | Alias of the management token |
| `--content-type` | None | string | Yes | None | content type UID |
| `--path` / `--no-path` | None | boolean | No | `true` | Show or hide the field path column |

#### Output

A structured table of the content type schema with columns for field title, UID, data type, and path (dot-notation path through nested structures).

Use `--no-path` to hide the path column for a more compact view.

#### Examples

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

Display the recent [audit log](/docs/headless-cms/monitor-stack-activities-in-audit-log) of changes made to a specific content type: who changed it, when, and what changed.

#### Syntax

```
csdx content-type:audit --content-type <uid> [FLAGS]
```

#### Flags

| Flag | Short | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `--stack-api-key` | `-k` | string | Yes (or `--alias`) | None | Stack API Key |
| `--alias` | `-a` | string | Yes (or `--stack-api-key`) | None | Alias of the management token |
| `--content-type` | None | string | Yes | None | content type UID |

#### Output

A table of audit log entries showing the action, the user who made the change, and the timestamp.

#### Examples

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

Compare two versions of the same content type within a stack. Shows fields added, removed, or modified between versions.

#### Syntax

```
csdx content-type:compare --content-type <uid> [FLAGS]
```

#### Flags

| Flag | Short | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `--stack-api-key` | `-k` | string | Yes (or `--alias`) | None | Stack API Key |
| `--alias` | `-a` | string | Yes (or `--stack-api-key`) | None | Alias of the management token |
| `--content-type` | None | string | Yes | None | content type UID |
| `--left` | None | integer | No | Latest version | Version number to use as the "left" (base) side of the diff |
| `--right` | None | integer | No | `latest - 1` | Version number to use as the "right" (compare) side of the diff |

**Note**: Provide `--left` and `--right` together, or omit both and let the command automatically compare the latest version against the previous version.

#### Output

A diff table showing fields that were added, removed, or changed between the two versions.

#### Examples

Compare the two most recent versions (automatic):

```
csdx content-type:compare -a my-token-alias --content-type home_page
```

Compare specific versions:

```
csdx content-type:compare -a my-token-alias --content-type home_page --left 5 --right 4
```

Using stack API key:

```
csdx content-type:compare -k <stack-api-key> --content-type blog_post --left 3 --right 2
```

---

### content-type:compare-remote

Compare the same content type across two different stacks, for example to validate that a staging schema matches production.

#### Syntax

```
csdx content-type:compare-remote --origin-stack <key> --remote-stack <key> --content-type <uid>
```

#### Flags

| Flag | Short | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `--origin-stack` | None | string | Yes | None | API Key of the origin (source) stack |
| `--remote-stack` | None | string | Yes | None | API Key of the remote (target) stack |
| `--content-type` | None | string | Yes | None | content type UID to compare |

**Note**: Pass two different stack API keys for `--origin-stack` and `--remote-stack`. Passing the same key for both produces an empty diff.

#### Output

A diff table showing field-level differences between the same content type on two stacks.

#### Examples

```
# Compare home_page across staging and production stacks
csdx content-type:compare-remote \
  --origin-stack <origin-stack-api-key> \
  --remote-stack <remote-stack-api-key> \
  --content-type home_page
```

---

### content-type:diagram

Generate a visual diagram of all content types in a stack, including references and relationships between them. Outputs an SVG or Graphviz DOT file.

#### Syntax

```
csdx content-type:diagram --output <path> [FLAGS]
```

#### Flags

| Flag | Short | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `--stack-api-key` | `-k` | string | Yes (or `--alias`) | None | Stack API Key |
| `--alias` | `-a` | string | Yes (or `--stack-api-key`) | None | Alias of the management token |
| `--output` | None | string | Yes | None | Full path to the output file (e.g. `./content-model.svg`) |
| `--direction` | None | string | No | `portrait` | Graph orientation: `portrait` or `landscape` |
| `--type` | None | string | No | `svg` | Output file type: `svg` or `dot` |

#### Output

Creates a file at the specified `--output` path. The file is either:

- **SVG** (default): A rendered visual graph, viewable in any browser or SVG viewer.
- **DOT**: A file in the DOT language, read by Graphviz, an open-source graph-visualization tool. Render it manually with `dot -Tpng content-model.dot -o content-model.png`.

The CLI always prints an absolute path here, regardless of whether you pass `--output` a relative or absolute path. On success, it prints something like:

```
Created Graph: /Users/you/project/content-model.svg
```

#### Examples

Generate an SVG diagram (portrait, default):

```
csdx content-type:diagram -a my-token-alias --output ./content-model.svg
```

Generate in landscape orientation:

```
csdx content-type:diagram -a my-token-alias --output ./content-model.svg --direction landscape
```

Generate a DOT file for further processing:

```
csdx content-type:diagram -a my-token-alias --output ./content-model.dot --type dot
```

Using stack API key:

```
csdx content-type:diagram -k <stack-api-key> --output ./diagram.svg
```

---

## Deprecated Flags (v1)

v1's short flags and the `--stack` / `--token-alias` long flags are deprecated in favor of the long-form flags used in v2. See [Upgrading from v1](/docs/headless-cms/cli-content-type-plugin#upgrading-from-v1) for the full old-to-new flag mapping.

When you use a deprecated flag, the CLI prints a deprecation warning pointing to the replacement.

---

## Authentication

Most commands accept a management token alias or a stack API key. Whether `--stack-api-key` and `--alias` are mutually exclusive depends on the command. Pass only one flag regardless.

| Command | Enforces `--stack-api-key` / `--alias` as mutually exclusive | Result of passing both |
| --- | --- | --- |
| `content-type:list` | Yes | Command exits with an error |
| `content-type:audit` | Yes | Command exits with an error |
| `content-type:diagram` | Yes | Command exits with an error |
| `content-type:details` | No | Command runs, using one of the two values (unspecified which) |
| `content-type:compare` | No | Command runs, using one of the two values (unspecified which) |

### Option 1: Management Token Alias (Recommended)

Save a management token once and reference it by alias:

```
csdx auth:tokens:add -a my-token-alias -k <stack-api-key> --management --token <management-token>
```

Then use `-a my-token-alias` in commands that accept `--alias`: `list`, `details`, `audit`, `compare`, `diagram`.

### Option 2: Stack API Key

Pass the stack API key directly:

```
csdx content-type:list -k <stack-api-key>
```

> **Exception (**`content-type:compare-remote`**)**: This command authenticates differently. Pass both stack API keys directly via `--origin-stack` and `--remote-stack` instead of `--alias` or `--stack-api-key`.

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
  --origin-stack <staging-api-key> \
  --remote-stack <production-api-key> \
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

## Troubleshooting

### "An error occurred." with no further detail

**Root Causes**: The stack API key or management token alias is incorrect, or the token lacks read permissions.

**Resolution**:

1. Verify the alias is saved: `csdx auth:tokens`
2. Confirm the token has `Content Type: Read` permission in the Contentstack UI.
3. Check your region is correctly configured: `csdx config:get:region`

See [Authentication](#authentication) for how the two credential methods work and which commands enforce them.

---

### `content-type:compare-remote`: "You cannot compare the same stack"

**Root Cause**: `--origin-stack` and `--remote-stack` are identical.

**Resolution**: Provide two different stack API keys. See [content-type:compare-remote](#content-typecompare-remote) for the full flag reference.

---

### `content-type:compare`: "You cannot compare the same version"

**Root Causes**:

- `--left` and `--right` are set to the same version number.
- You omitted both flags and the content type has only one version. The command defaults to comparing version 1 against itself and prints this warning.

**Resolution**:

- If two or more versions exist, use different `--left` and `--right` values. Check the version history via `content-type:audit` first.
- If only one version exists, there is nothing to compare yet. Save a change to the content type to create a second version first.

See [content-type:compare](#content-typecompare) and [content-type:audit](#content-typeaudit).

---

### `content-type:diagram`: output file not created

**Root Causes**:

- You lack write permission on the resolved output path
- The `--output` contains characters your OS's filesystem doesn't allow.

**Resolution**:

1. Check write permissions on the target directory. The CLI creates missing parent directories automatically.
2. Use an absolute path if you want full control over where the file lands.
3. Remove any characters your OS doesn't allow in file paths.

See [content-type:diagram](#content-typediagram) for the full flag and output reference.

---

### Plugin not found after install

**Root Cause**: The install did not complete, or the CLI is not listing the installed plugin.

**Resolution**: Reinstall following [Installation](#installation). If `contentstack-cli-content-type` still does not appear in `csdx plugins` after a clean reinstall, the issue is in your local npm/CLI environment rather than the plugin itself.

---

## Limitations

- These commands compare and diagram schema only. They do not diff [entry](/docs/headless-cms/about-entries)-level content or data records.
- `content-type:diagram` writes a local SVG or DOT file. It is never uploaded or synced back to the stack.
- `content-type:compare` needs at least two saved versions of a content type. With only one version, it compares the version against itself and returns an empty diff. See [content-type:compare](#content-typecompare) for the single-version case.

---

## Next Steps

- [Regex Validate Plugin (v1)](/docs/headless-cms/cli-regex-validate-plugin/v1): scan your content types and [global fields](/docs/headless-cms/about-global-field) for regex patterns vulnerable to catastrophic backtracking (a regex performance bug that can make matching hang).
- [Audit Plugin](/docs/headless-cms/cli-audit-plugin/v1): a related Contentstack plugin for reviewing audit log activity across your stack.
- [CLI Authentication: Add Management Token](/docs/headless-cms/cli-authentication/v1#add-management-token): create and save the management token alias these commands use.
- [Configure Regions in the CLI](/docs/headless-cms/configure-regions-in-the-cli/v1#set-region): set your region if your stack is not in North America.
- [About Content Types](/docs/developers/create-content-types/about-content-types): conceptual background on how content types and their fields are structured.
