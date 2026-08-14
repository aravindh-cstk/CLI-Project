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

Display the full schema details of a specific content type.

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

A structured table of the content type schema with columns for field title, UID, data type, and path (dot-notation path through nested structures). Use `--no-path` to hide the path column for a more compact view.

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

Display recent [audit log](/docs/headless-cms/monitor-stack-activities-in-audit-log) changes to a specific content type.

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

Compare two versions of the same content type within a stack.

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
| `--left` | None | integer | No | Latest version | Base version to compare from |
| `--right` | None | integer | No | `latest - 1` | Version to compare against |

**Note**: Provide `--left` and `--right` together. If omitted, the latest two versions are compared automatically.

#### Output

A diff table showing fields that were added, removed, or changed between the two versions.

#### Examples

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

#### Syntax

```
csdx content-type:compare-remote --origin-stack <key> --remote-stack <key> --content-type <uid>
```

#### Flags

| Flag | Short | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `--origin-stack` | None | string | Yes | None | API Key of the origin stack (used for authentication) |
| `--remote-stack` | None | string | Yes | None | API Key of the remote stack |
| `--content-type` | None | string | Yes | None | content type UID to compare |

> **Note**: See the [Authentication Exception](#authentication-exception-content-typecompare-remote) for how this command authenticates.

#### Output

A diff table showing field-level differences between the same content type on two stacks.

#### Examples

```
csdx content-type:compare-remote \
  --origin-stack <origin-stack-api-key> \
  --remote-stack <remote-stack-api-key> \
  --content-type home_page
```

---

### content-type:diagram

Generate a visual diagram of all content types in a stack.

#### Syntax

```
csdx content-type:diagram --output <path> [FLAGS]
```

#### Flags

| Flag | Short | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `--stack-api-key` | `-k` | string | Yes (or `--alias`) | None | Stack API Key |
| `--alias` | `-a` | string | Yes (or `--stack-api-key`) | None | Alias of the management token |
| `--output` | None | string | Yes | None | Full path to the output file |
| `--direction` | None | string | No | `portrait` | Graph orientation: `portrait` or `landscape` |
| `--type` | None | string | No | `svg` | Output file type: `svg` or `dot` |

#### Output

Creates a file at the specified `--output` path. The file is either:

- **SVG** (default): a rendered visual graph, viewable in any browser or SVG viewer.
- **DOT**: a file in the DOT language, read by Graphviz, an open-source graph-visualization tool. Render it manually with `dot -Tpng content-model.dot -o content-model.png`.

The CLI always prints an absolute path here, regardless of whether you pass `--output` a relative or absolute path. On success, it prints something like:

```
Created Graph: /Users/you/project/content-model.svg
```

#### Examples

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

## Troubleshooting

### "You're not logged in. Run auth:login to sign in."

**Root Cause**: You have no active CLI login session. Every command authenticates using the [auth token](/docs/headless-cms/types-of-tokens#authentication-tokens-auth-tokens) that `auth:login` creates. This applies even when you pass `--stack-api-key` (`-k`). The stack API key sets the target stack. It does not replace the auth token.

**Resolution**:

1. Log in: `csdx auth:login`
2. Re-run your command.

For more detail, see [CLI Authentication](/docs/headless-cms/cli-authentication).

---

### "Connection failed. You might be using a delivery token."

**Root Cause**: The alias you passed with `-a` points to a [delivery token](/docs/headless-cms/about-delivery-tokens), a token scoped for reading published content only. These commands require a management token, which grants access to manage stack schema and data.

**Resolution**:

1. List your saved tokens and their type: `csdx auth:tokens`
2. If you do not have a management token, add one as shown in [Authentication](#authentication).
3. Pass the management token alias with `-a`.

See [Add a Management Token](/docs/headless-cms/cli-authentication#add-management-token).

---

### "You must provide either a token alias or a stack UID."

**Root Cause**: You ran a command without `--alias` (`-a`) and without `--stack-api-key` (`-k`). Every command except `content-type:compare-remote` needs one of them.

**Resolution**: Add either `-a <alias>` or `-k <stack-api-key>`. For `content-type:compare-remote`, pass `--origin-stack` and `--remote-stack` instead. See [Authentication](#authentication).

---

### "Error: ..." on a command that needs a stack API key or alias

This covers messages that start with `Error:` and name an authentication or permission problem. `An error occurred.` with no further text is the fallback the CLI shows when it cannot read a message off the failure, and the same root causes apply.

**Root Causes**:

- The stack API key or the management token behind the alias is wrong.
- The token lacks `Content Type: Read` permission.
- Your configured region does not match the stack's region, so the key is valid but the request reaches the wrong data center.

**Resolution**:

1. Verify the alias is saved and points to the right stack: `csdx auth:tokens`
2. Confirm the token has `Content Type: Read` permission in the Contentstack UI.
3. Check your region: `csdx config:get:region`. If it does not match the stack, reset it with `csdx config:set:region`.

See [Configure Regions in the CLI](/docs/headless-cms/configure-regions-in-the-cli#set-region).

---

### "Error: ..." naming a content type or version that was not found

Applies to `content-type:details`, `content-type:audit`, `content-type:compare`, and `content-type:compare-remote`.

**Root Causes**:

- The `--content-type` UID is misspelled or does not exist in the target stack.
- (`content-type:compare`) The version you passed to `--left` or `--right` does not exist for that content type.

**Resolution**:

1. List the valid UIDs in the stack: `csdx content-type:list -a my-token-alias`
2. Check the available versions of a content type: `csdx content-type:audit -a my-token-alias --content-type <uid>`
3. Re-run with a valid UID and, for `compare`, valid version numbers.

See [content-type:list](#content-typelist) and [content-type:audit](#content-typeaudit) for the commands used above.

---

### content-type:compare-remote: "You cannot compare the same stack"

**Root Cause**: `--origin-stack` and `--remote-stack` hold the same API key.

**Resolution**: Provide two different stack API keys. This message is a warning, so the command still runs and produces an empty diff. See [content-type:compare-remote](#content-typecompare-remote).

---

### content-type:compare: "You cannot compare the same version"

**Root Causes**:

- `--left` and `--right` are set to the same version number.
- You omitted both flags and the content type has only one version. The command defaults to comparing version 1 against itself and prints this warning.

**Resolution**:

- If two or more versions exist, pass different `--left` and `--right` values. Check the version history first with `csdx content-type:audit -a my-token-alias --content-type <uid>`.
- If only one version exists, there is nothing to compare yet. Save a change to the content type to create a second version first.

See [content-type:compare](#content-typecompare) and [content-type:audit](#content-typeaudit).

---

### content-type:diagram: output file not created

**Root Causes**:

- You lack write permission on the target directory.
- `--output` points at an existing directory instead of a file.
- A parent path segment is a file, not a folder.
- The disk is full.
- `--output` is blank or only whitespace. The command reports `Please provide an output path.`
- `--output` contains characters your filesystem does not allow.

**Resolution**:

1. Use an absolute path to a writable directory.
2. Name a file, not a directory, in `--output`.
3. Confirm the target has free disk space.
4. Remove any characters your operating system does not allow in file paths.

The CLI creates missing parent directories automatically. The `--type` value and the file extension are independent: `--type dot` with `--output content-model.svg` writes DOT content into a file named `.svg`. Match the extension to the type yourself. See [content-type:diagram](#content-typediagram) for the full flag reference.

---

### "Nonexistent flag" error after upgrading from v1

**Root Cause**: v2 removed a v1 short flag (for example `-s`, `-c`, `-l`, `-r`, `-o`, `-d`, `-t`, or `-p`) or a deprecated flag (`--stack`, `--token-alias`) that a script still passes.

**Resolution**: Replace the flag with its v2 long form. See [Upgrading from v1](#upgrading-from-v1) for the full mapping.

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
- [About Content Types](/docs/developers/create-content-types/about-content-types): conceptual background on how content types and their fields are structured.
