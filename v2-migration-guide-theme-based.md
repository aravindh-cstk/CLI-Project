---
sidebar: cliSidebar
title: Migrate from Contentstack CLI V1 to V2
description: Step-by-step guide to upgrading from Contentstack CLI V1 to V2, covering breaking changes, removed flags, command replacements, and a pre-upgrade checklist.
url: /developers/cli/v2-migration-guide
version: 2.0.0
---

# Migrate from Contentstack CLI V1 to V2

## Overview

This guide applies if you are upgrading Contentstack CLI from version 1.x to 2.0.0.

V2 requires Node.js 22+, routes all publish operations through the NRP API, removes several flags and command aliases with no runtime warning, and changes the on-disk format of exports (per-UID files replace aggregate JSON files like `schema.json` and `globalfields.json`).

This guide walks through every removed flag and command, the file-format changes that affect export and import tooling, a pre-upgrade checklist, and troubleshooting steps for failure modes that produce no error output. See [Troubleshooting](#troubleshooting) for the specifics.

This guide covers CLI-only changes. It does not cover Contentstack platform or API changes.

## Prerequisites

### Node.js 22+ Required

V2 requires Node.js >=22.0.0.

```bash
node --version   # must be v22.0.0 or higher
```

> **On Node 18 or 20:** `npm install -g @contentstack/cli` completes with `EBADENGINE` warnings and appears to succeed, but the CLI fails at runtime. Upgrade Node first, then install.

If you need to upgrade Node:
```bash
nvm install 22
nvm alias default 22   # makes 22 the permanent default, not just for this shell session
nvm use 22
```

Before installing, confirm Node 22 is in place everywhere the CLI runs:

- [ ] Dev machines: `node --version` shows v22+
- [ ] All CI/CD runners upgraded to Node 22
- [ ] Docker base images updated to Node 22 LTS

### Install V2

```bash
npm install -g @contentstack/cli@2.0.0
```

Using **yarn** or **pnpm**:
```bash
yarn global add @contentstack/cli@2.0.0
pnpm add -g @contentstack/cli@2.0.0
```

Verify the upgrade succeeded:
```bash
csdx --version   # should show 2.0.0
```

> **Upgrade note:** `npm install -g` replaces the `csdx` binary in place. The install has an approximately 30-second window during which `csdx` is unavailable. For CI pipelines, run the install and the CLI commands in the same pipeline step. Do not rely on a pre-installed binary from a prior step.
>
> **Running V1 and V2 side by side:** npm global install allows only one active version per Node environment. If you need V1 available during testing, install it under a different nvm Node version:
> ```bash
> nvm use 20
> npm install -g @contentstack/cli@1.x
>
> nvm use 22
> npm install -g @contentstack/cli@2.0.0
> ```
>
> **On a 2.x beta:** Upgrade directly to 2.0.0: `npm install -g @contentstack/cli@2.0.0`. Your tokens and stored config carry over automatically.

> **Note:** Your existing saved tokens (management tokens added with `csdx auth:tokens:add`) carry over automatically. You do not need to re-authenticate after upgrading.
>
> Other stored config (proxy settings, region config) also carries over unchanged. The console log setting is the only exception: if you ran `csdx config:set:log --show-console-logs` in V1, re-run it after upgrading. V2 uses a different internal key, so it silently ignores the V1 setting. See [config:set:log](#configsetlog) for the resolution.

## Type Mapping Reference

All flag renames and removed short characters across every command. Rows with the same V1 and V2 flag name had only their short character removed.

| Command | V1 Flag | V1 Short | V2 Flag | V2 Short |
|---|---|---|---|---|
| `cm:stacks:export` | `--stack-uid` | `-s` | `--stack-api-key` | `-k` |
| | `--data` | N/A | `--data-dir` | N/A |
| | `--management-token-alias` | N/A | `--alias` | `-a` |
| | `--auth-token` | `-A` | *(removed, use OAuth + `--alias`)* | N/A |
| | `--module` | `-m` | `--module` | N/A |
| | `--content-types` | `-t` | `--content-types` | N/A |
| | `--branch` | `-B` | `--branch` | N/A |
| `cm:stacks:import` | `--stack-uid` | `-s` | `--stack-api-key` | `-k` |
| | `--data` | N/A | `--data-dir` | N/A |
| | `--management-token-alias` | N/A | `--alias` | `-a` |
| | `--auth-token` | `-A` | *(removed, use OAuth + `--alias`)* | N/A |
| | `--module` | `-m` | `--module` | N/A |
| | `--backup-dir` | `-b` | `--backup-dir` | N/A |
| | `--branch` | `-B` | `--branch` | N/A |
| | `--skip-app-recreation` | N/A | *(removed, no replacement)* | N/A |
| `cm:stacks:import-setup` | `--branch` | `-B` | `--branch` | N/A |
| `cm:stacks:seed` | `--stack` | `-s` | `--stack-api-key` | N/A |
| | `--repo` | `-r` | `--repo` | N/A |
| | `--org` | `-o` | `--org` | N/A |
| `cm:stacks:migration` | `--branch` | `-B` | `--branch` | N/A |
| | `--authtoken` | `-A` | `--authtoken` | N/A |
| | `--filePath` | `-n` | `--file-path` | N/A |
| `cm:stacks:validate-regex` | `--contentType` | `-c` | `--contentType` | N/A |
| | `--filePath` | `-f` | `--filePath` | N/A |
| | `--globalField` | `-g` | `--globalField` | N/A |
| `cm:bootstrap` | `--appName` | `-a` | `--app-name` | N/A |
| | `--directory` | `-d` | `--project-dir` | N/A |
| `auth:tokens:add` | `--delivery` | `-d` | `--delivery` | N/A |
| | `--management` | `-m` | `--management` | N/A |
| | `--token` | `-t` | `--token` | N/A |
| | `--api-key` | N/A | *(removed)* | N/A |
| | `--force` | `-f` | `--yes` | `-y` |
| `auth:tokens:remove` | `--ignore` | `-i` | *(removed)* | N/A |
| `auth:logout` | `--force` | `-f` | `--yes` | `-y` |
| `config:set:region` | `--cda` | `-d` | `--cda` | N/A |
| | `--cma` | `-m` | `--cma` | N/A |
| | `--name` | `-n` | `--name` | N/A |
| `tsgen` | `--token-alias` | N/A | `--alias` | `-a` |
| | `--output` | `-o` | `--output` | N/A |
| | `--prefix` | `-p` | `--prefix` | N/A |
| | `--doc` | `-d` | `--doc` | N/A |
| `app:create` | `--name` | `-n` | `--name` | N/A |
| `migrate:convert` | `--output` | `-o` | `--output` | N/A |
| | `--master-locale` | `-m` | `--master-locale` | N/A |
| | `--affix` | `-a` | `--affix` | N/A |
| `migrate:export` | `--output` | `-o` | `--output` | N/A |
| `content-type:audit` | `--stack` | `-s` | `--stack-api-key` | `-k` |
| | `--token-alias` | `-a` | `--alias` | `-a` |
| | `--content-type` | `-c` | `--content-type` | N/A |
| `content-type:compare` | `--stack` | `-s` | `--stack-api-key` | `-k` |
| | `--token-alias` | `-a` | `--alias` | `-a` |
| | `--content-type` | `-c` | `--content-type` | N/A |
| | `--left` | `-l` | `--left` | N/A |
| | `--right` | `-r` | `--right` | N/A |
| `content-type:compare-remote` | `--origin-stack` | `-o` | `--origin-stack` | N/A |
| | `--remote-stack` | `-r` | `--remote-stack` | N/A |
| | `--content-type` | `-c` | `--content-type` | N/A |
| `content-type:details` | `--stack` | `-s` | `--stack-api-key` | `-k` |
| | `--token-alias` | `-a` | `--alias` | `-a` |
| | `--content-type` | `-c` | `--content-type` | N/A |
| | `--path` | `-p` | `--path` | N/A |
| `content-type:diagram` | `--stack` | `-s` | `--stack-api-key` | `-k` |
| | `--token-alias` | `-a` | `--alias` | `-a` |
| | `--output` | `-o` | `--output` | N/A |
| | `--direction` | `-d` | `--direction` | N/A |
| | `--type` | `-t` | `--type` | N/A |
| `content-type:list` | `--stack` | `-s` | `--stack-api-key` | `-k` |
| | `--token-alias` | `-a` | `--alias` | `-a` |
| | `--order` | `-o` | `--order` | N/A |

## Main Content

### 1. Runtime and Install Changes

#### Node.js 22 Requirement

**V1:** Runs on Node.js 18 or 20.

**V2:** Requires Node.js >=22.0.0. Installing under Node 18 or 20 completes with `EBADENGINE` warnings, and the CLI then fails at runtime instead of failing at install time. See [Prerequisites](#prerequisites) for the full upgrade checklist.

**Before (V1):**
```bash
node --version   # v18 or v20 supported
```

**After (V2):**
```bash
node --version   # must show v22.0.0 or higher
```

#### Progress Bars Replace Console Logs

**V1:** All operations print text line by line to stdout as they run. Scripts and CI parse this output.

**V2:** Visual progress bars render in the terminal. V2 suppresses console log output by default. The end of the run shows only a summary and a log file path.

**Effect:** Any script or CI pipeline that parses stdout for success or failure signals receives different output. V2 raises no error. The output is simply different.

> **CI environments:** V2 does not auto-detect non-interactive (non-TTY) environments. Progress bars render regardless of whether stdout is a terminal. If you see escape code characters in your CI logs, enable console log mode to get plain text output instead.

To restore console log output for CI, run `csdx config:set:log --show-console-logs`. See [config:set:log](#configsetlog) for the full flag reference.

Logs write to a `logs/` directory in whichever folder you ran the CLI from (for example, `./logs/`). Set the `CS_CLI_LOG_PATH` environment variable, or run `csdx config:set:log --path <dir>`, to redirect logs.

#### Deprecated Flags Removed With No Warning

**V1:** Deprecated flags (`--stack-uid`, `--data`, `-s`, `-B`, and others) print a deprecation warning but still work.

**V2:** V2 completely removes these flags. Passing one now causes an immediate error, with no runtime warning to catch it first.

**Before (V1):**
```bash
csdx cm:stacks:export --stack-uid blt123   # prints a deprecation warning, still runs
```

**After (V2):**
```bash
csdx cm:stacks:export --stack-uid blt123
# ERROR: Nonexistent flag: --stack-uid
```

Audit your scripts for deprecated flags before upgrading. See the [Type Mapping Reference](#type-mapping-reference) for every renamed or removed flag.

#### Short Flag Cleanup Across Commands

V2 systematically removes single-character short flags that conflicted with global CLI flags or were ambiguous across commands. In every case the long form still works. For example:

**Before:**
```bash
csdx migrate:export -o ./output
csdx app:create -n my-app
```

**After:**
```bash
csdx migrate:export --output ./output
csdx app:create --name my-app
```

See the [Type Mapping Reference](#type-mapping-reference) for the complete list of removed short characters across every command.

### 2. Publishing Changes

#### All Publish Operations Now Use NRP

In V2, all publish operations (including entry, asset, and taxonomy publishes triggered during import, and all bulk publish and unpublish commands) go through the NRP API. V1 did not do this for import. For bulk publish, V1 exposed an `--api-version` flag that let you control this.

**What changed:**

| Command | V1 | V2 |
|---|---|---|
| `cm:stacks:import` (auto-publish) | Did not use NRP | Uses NRP for all entry, asset, and taxonomy publishes |
| `cm:stacks:bulk-entries` | `--api-version` flag let you opt in or out | Always uses NRP, `--api-version` flag removed |
| `cm:stacks:bulk-assets` | `--api-version` flag let you opt in or out | Always uses NRP, `--api-version` flag removed |

**Impact:** Your stack must have NRP enabled. V2 has no flag to run publish operations without NRP.

> **Note:** Passing `--api-version` to `cm:stacks:bulk-entries` or `cm:stacks:bulk-assets` in V2 causes an immediate error: `ERROR: Nonexistent flag: --api-version`.

#### cm:stacks:bulk-entries Replaces the Bulk Publish Plugin

**Replaces (all removed in V2):** `cm:entries:publish`, `cm:entries:publish-modified`, `cm:entries:publish-only-unpublished`, `cm:entries:publish-non-localized-fields`, `cm:entries:unpublish`, `cm:entries:update-and-publish`, `cm:stacks:publish` (entries), `cm:stacks:unpublish` (entries), `cm:stacks:publish-revert`.

> **This is the highest-effort migration in V2.** V2 replaces the entire `@contentstack/cli-cm-bulk-publish` plugin (14 commands) with `@contentstack/cli-bulk-operations`. Rewrite every bulk publish script.

**V1 to V2 command mapping:**

| V1 Command (REMOVED) | V2 Replacement |
|---|---|
| `csdx cm:entries:publish` | `csdx cm:stacks:bulk-entries --operation publish` |
| `csdx cm:entries:publish-modified` | `csdx cm:stacks:bulk-entries --operation publish --filter modified` |
| `csdx cm:entries:publish-only-unpublished` | `csdx cm:stacks:bulk-entries --operation publish --filter unpublished` |
| `csdx cm:entries:publish-non-localized-fields` | `csdx cm:stacks:bulk-entries --operation publish --filter non-localized` |
| `csdx cm:entries:unpublish` | `csdx cm:stacks:bulk-entries --operation unpublish` |
| `csdx cm:entries:update-and-publish` | `csdx cm:stacks:bulk-entries --operation publish` |
| `csdx cm:stacks:publish` (for entries) | `csdx cm:stacks:bulk-entries --operation publish` |
| `csdx cm:stacks:unpublish` (for entries) | `csdx cm:stacks:bulk-entries --operation unpublish` |
| `csdx cm:bulk-publish:cross-publish` | `csdx cm:stacks:bulk-entries --operation publish --source-alias <alias>` |
| `csdx cm:stacks:publish-revert --log-file ./log.json` | `csdx cm:stacks:bulk-entries --revert ./log.json` |
| `csdx cm:stacks:publish-configure` | **NO EQUIVALENT, REMOVED** |
| `csdx cm:stacks:publish-clear-logs` | **NO EQUIVALENT, REMOVED** |

**`--filter` valid values:** `draft`, `modified`, `unpublished`, `non-localized`. Passing any other value causes an immediate error.

**Before:**
```bash
csdx cm:entries:publish --content-types blog article --environments prod --locales en-us
```

**After:**
```bash
csdx cm:stacks:bulk-entries --operation publish \
  --content-types blog article \
  --environments prod \
  --locales en-us \
  --stack-api-key bltXXX \
  --alias myalias

csdx cm:stacks:bulk-entries --operation unpublish \
  --content-types blog \
  --environments prod \
  --locales en-us \
  --stack-api-key bltXXX \
  --alias myalias

csdx cm:stacks:bulk-entries --revert ./log.json \
  --stack-api-key bltXXX \
  --alias myalias
```

**Cross-publish migration:** V1 accepted an inline `--delivery-token` flag on `cm:bulk-publish:cross-publish`. V2 requires a stored delivery token alias instead. Set it up once:

```bash
# Step 1: store delivery token as an alias (one-time)
csdx auth:tokens:add \
  -a staging-delivery \
  --delivery \
  --token bltABC \
  --stack-api-key blt123 \
  --environment staging

# Step 2: use the alias in bulk-entries
csdx cm:stacks:bulk-entries \
  --operation publish \
  --source-env staging \
  --source-alias staging-delivery \
  --content-types blog article \
  --environments prod \
  --locales en-us \
  -k blt123
```

See [auth:tokens:add](#authtokensadd) for the full flag reference on that command.

#### cm:stacks:bulk-assets Replaces Asset Publish Commands

**Replaces (all removed in V2):** `cm:assets:publish`, `cm:assets:unpublish`, `cm:stacks:publish` (assets), `cm:stacks:unpublish` (assets).

**V1 to V2 command mapping:**

| V1 Command (REMOVED) | V2 Replacement |
|---|---|
| `csdx cm:assets:publish` | `csdx cm:stacks:bulk-assets --operation publish` |
| `csdx cm:assets:unpublish` | `csdx cm:stacks:bulk-assets --operation unpublish` |

**Before:**
```bash
csdx cm:assets:publish --environments prod --locales en-us
```

**After:**
```bash
csdx cm:stacks:bulk-assets --operation publish \
  --environments prod \
  --locales en-us \
  --stack-api-key bltXXX \
  --alias myalias
```

**No prior equivalent in V1: CS Assets bulk delete and move.** V2 adds two new operation types to `cm:stacks:bulk-assets` that target the CS Assets API (Asset Management 2.0), separate from the CMS publish pipeline:

| Operation | What it does |
|---|---|
| `--operation delete` | Bulk delete assets from a CS Assets space (async job) |
| `--operation move` | Bulk move assets to a target folder in a CS Assets space |

```bash
# CS Assets bulk delete
csdx cm:stacks:bulk-assets \
  --operation delete \
  --space-uid am123 \
  --org-uid bltOrg \
  --locale en-us \
  --asset-uids-file ./assets.json   # JSON: { "uids": ["uid1", "uid2"] }

# CS Assets bulk move
csdx cm:stacks:bulk-assets \
  --operation move \
  --space-uid am123 \
  --org-uid bltOrg \
  --target-folder-uid amFolder \
  --asset-uids-file ./assets.json
```

**Requirements:** You must configure `csAssetsUrl` in region settings (`csdx config:set:region --cs-assets <url>`). CMS flags (`--stack-api-key`, `--alias`, `--environments`, `--locales`, `--branch`) cannot combine with CS Assets flags. The `delete` operation requires `--locale`, the `move` operation does not allow it.

> **Where to find `--space-uid` and `--org-uid`:** In the Contentstack UI, go to **Organization > Contentstack Assets > Settings**. The page shows the Space UID and Organization UID. You can also retrieve them from the CS Assets API.

V2 removes the `--api-version` flag here too and hardcodes `api_version: '3.2'` on all calls, the same as `cm:stacks:bulk-entries`.

#### cm:stacks:bulk-taxonomies (New)

**No prior equivalent in V1.** V2 adds `cm:stacks:bulk-taxonomies` for bulk publishing or unpublishing taxonomy terms. It hardcodes `api_version: '3.2'` on all calls.

| Flag | Short | Description |
|---|---|---|
| `--operation` | | `publish` or `unpublish` |
| `--stack-api-key` | `-k` | Stack API key |
| `--alias` | `-a` | Management token alias |
| `--environments` | | Target environments (multiple allowed) |
| `--locales` | | Target locales (multiple allowed) |
| `--taxonomies` | | Comma-separated taxonomy UIDs. Omit to target all taxonomies. |
| `--branch` | | Branch (defaults to `main`) |
| `--yes` / `--no` | `-y` | Skip confirmation prompt |

```bash
# Publish specific taxonomies
csdx cm:stacks:bulk-taxonomies \
  --operation publish \
  --environments staging prod \
  --locales en-us fr-fr \
  --taxonomies products_tax,brands_tax \
  --stack-api-key bltXXX \
  --alias myalias

# Publish all taxonomies
csdx cm:stacks:bulk-taxonomies \
  --operation publish \
  --environments prod \
  --locales en-us \
  --stack-api-key bltXXX \
  --alias myalias
```

#### --api-version Flag Removed Everywhere

**V1:** `cm:stacks:bulk-entries` and `cm:stacks:bulk-assets` accept an `--api-version` flag that lets you opt in or out of the newer publish API.

**V2:** V2 hardcodes `api_version: '3.2'` on every publish and unpublish call and removes the `--api-version` flag. Passing it fails immediately:

```
ERROR: Nonexistent flag: --api-version
```

Remove `--api-version` from all bulk publish scripts. If your content types use the legacy rich text editor, test publish behavior in a staging stack before cutting over.

### 3. Export and Import Format Changes

#### Per-UID Files Replace Aggregate JSON Files

**V1:** `cm:stacks:export` writes a combined `content_types/schema.json` with all content type schemas in one array, and a combined `global_fields/globalfields.json` with all global fields in one file.

**V2:** V2 writes only individual per-UID files. The aggregate files are gone.

```bash
# V1 export: aggregate files
cat export/content_types/schema.json
cat export/global_fields/globalfields.json

# V2 export: per-UID files instead
ls export/content_types/*.json
```

```
# V2 global fields, one file per UID
export/global_fields/my_header.json
export/global_fields/my_footer.json
export/global_fields/shared_banner.json
```

> **Action required if your tooling reads either aggregate file.** If any pipeline or script reads `export/content_types/schema.json` or `export/global_fields/globalfields.json`, it fails on a V2 export with no error message. The files do not exist. Update tooling to iterate per-UID files instead.

This same per-UID reading behavior affects `cm:stacks:import` and `cm:stacks:audit`. See the next two subsections and [Troubleshooting](#troubleshooting).

#### Branch Export Behavior Changed

**V1:** When you omit `--branch`, export writes ALL branches, nested under `exportDir/<branch-uid>/...` for each branch. Export also writes a `branches.json` file to the export root listing all branches at export time.

**V2:** Two independent changes:
1. **Default branch:** When you omit `--branch`, V2 exports only the branch named `main`. If no `main` branch exists, the command errors.
2. **No branch subfolder, always:** Even when you specify `--branch`, V2 writes output flat to `exportDir/...` with no `<branch-uid>/` subfolder. This applies regardless of how you select the branch. V2 also does not write `branches.json`, and raises no error for its absence.

**Impact for multi-branch stacks:** You must export each branch to a separate `--data-dir`. If you export two branches to the same directory, the second export silently overwrites the first.

**Before:**
```bash
csdx cm:stacks:export --branch main --data-dir ./export --stack-api-key bltXXX
csdx cm:stacks:export --branch feature-x --data-dir ./export --stack-api-key bltXXX
```

**After:**
```bash
# One --data-dir per branch
csdx cm:stacks:export --branch main       --data-dir ./export-main    --stack-api-key bltXXX
csdx cm:stacks:export --branch feature-x  --data-dir ./export-feature --stack-api-key bltXXX
csdx cm:stacks:export --branch-alias prod --data-dir ./export-prod     --stack-api-key bltXXX
```

If your import pipeline or post-export tooling reads `branches.json`, remove that step.

This same flat-output change removes the branch auto-detection that `cm:stacks:import` relied on. See the next subsection.

#### export-info.json No Longer Written

**V1:** `cm:stacks:export` writes `export-info.json` to the export directory, containing `{ "contentVersion": 2, "logsPath": "..." }`.

**V2:** V2 does not write this file.

If your pipeline checks for this file or reads `contentVersion` from it, remove that step.

#### Content Types and Global Fields Silently Skipped on Import

V2's importers use per-UID file readers that explicitly ignore aggregate files. The impact differs by module because V1 export behavior differs between them:

| Module | V1 export writes | V2 importer reads | Impact on a V1 export |
|---|---|---|---|
| Content types | Individual `<uid>.json` files, plus `schema.json` | Per-UID files only (ignores `schema.json`) | **No impact.** Per-UID files exist, content types import correctly |
| Global fields | `globalfields.json` only (no individual files) | Per-UID files only (ignores `globalfields.json`) | **Silently skipped.** No per-UID files exist in a V1 export |

**Impact:** Running V2 import on a V1 export silently skips all global fields. V2 raises no error and no warning. Global fields complete "successfully" with zero items created. Content types are unaffected.

**Resolution:** Re-export your stack with V2 before importing. This is the correct fix. See [Troubleshooting](#troubleshooting) for the full write-up.

**No prior equivalent in V1: multi-branch import auto-detection removal.** V1 import auto-detects the branch by reading `branches.json` at the export root and navigating to the correct `<branch-uid>/` subfolder (the `selectBranchFromDirectory` logic). V2 removes this logic entirely.

**Before:**
```bash
csdx cm:stacks:import --data-dir ./my-export    # V1 read branches.json, then auto-navigated to ./my-export/main/
```

**After:**
```bash
csdx cm:stacks:import --data-dir ./my-export/main    # V2: specify the branch subfolder explicitly
```

If you point V2 import at a V1 multi-branch export root, it attempts to read content files directly from the root, where only `branches.json` lives, finds nothing, and silently produces an empty import. See [Troubleshooting](#troubleshooting).

Additional import changes:
- **Module flag validation:** Same as export, V2 validates `--module` on import before any operation begins. `--module studio` fails, use `--module composable-studio` instead. `--module variant-entries` is a new valid value in V2 that V1 did not have.
- **composable-studio requires Basic Auth:** V2 skips the composable-studio module when you authenticate with a management token (`Skipping Studio project import when using management token`) or OAuth (`Skipping Studio project import when using OAuth authentication`). To import composable-studio, authenticate with `csdx auth:login -u <email> -p <password>`. Basic Auth is the only supported path.
- **Removed import config keys:** If you maintain a custom plugin or tool that reads the import config object, V2 removes `importConfig.branchDir` (was a redundant alias for `contentDir`, use `contentDir` directly) and `importConfig.contentVersion` (a JS/TS module routing number used internally). If your external config JSON uses `modules["asset-management"]`, V2 renames it to `modules["cs-assets"]` internally and logs a deprecation warning. Update your config files to use `"cs-assets"` to suppress it.

#### cm:stacks:audit Reads Per-UID Files

`cm:stacks:audit` uses `readContentTypeSchemas` and `readGlobalFieldSchemas`, the same utilities as V2 import, to load content type and global field schemas from the `--report-path` directory. These utilities read individual `<uid>.json` files and explicitly ignore `schema.json` and `globalfields.json`.

**V1:** Auditing a V1 export directory loads content types correctly, since V1 export writes per-UID content type files.

**V2:** Global fields return zero results, a false clean, because V1 export writes only `globalfields.json` with no per-UID files.

**Before (V1 export as input):**
```bash
csdx cm:stacks:audit --report-path ./v1-export
# global field issues: 0 (false clean, no per-UID files to read)
```

**After (V2 export as input):**
```bash
csdx cm:stacks:audit --report-path ./v2-export
# global field issues: detected correctly
```

**Resolution:** Re-export global fields with V2 before auditing. See [Troubleshooting](#troubleshooting).

#### CS Assets (Asset Management 2.0) Support

**No prior equivalent in V1.** V2 adds full support for Contentstack's CS Assets system (Asset Management 2.0, or AM 2.0). Export, import, and import-setup automatically detect and handle CS Assets when your stack has linked workspaces.

**Export:** If your stack has linked workspaces configured in Contentstack Assets settings, export writes CS Assets data to a `spaces/` directory alongside the standard `assets/` directory. If your stack does not have linked workspaces configured, export automatically falls back to standard asset export:

```
export/
  assets/         # CMS assets, unchanged
  spaces/         # NEW: CS Assets
    <space-id>/workspaces/
    <space-id>/asset_types/
    <space-id>/assets/
    <space-id>/folders/
```

**Import:** V2 detects the `spaces/` directory and imports CS Assets automatically.

**Import-setup:** V2 detects CS Assets exports and generates identity UID and URL mapper files.

For the CS Assets bulk delete and move operations added to `cm:stacks:bulk-assets`, see [cm:stacks:bulk-assets Replaces Asset Publish Commands](#cmstacksbulk-assets-replaces-asset-publish-commands).

### 4. Removed Plugins

#### launch Plugin Now Opt-In

**V1:** `launch:*` commands come bundled in the CLI.

**V2:** `launch:*` commands are no longer bundled. V2 no longer bundles them. Running any `launch:*` command prints a guided error with the install instruction and exits with code 127.

**Affected commands:** `launch`, `launch:deployments`, `launch:environments`, `launch:functions`, `launch:logs`, `launch:open`, `launch:rollback`.

**After:**
```bash
csdx plugins:install @contentstack/cli-launch
```

#### migrate-rte Plugin Now Opt-In

**V1:** `cm:entries:migrate-html-rte` comes bundled in the CLI.

**V2:** V2 no longer bundles `cm:entries:migrate-html-rte`. Unlike `launch`, V2 does not print a guided error. The shell returns "command not found" with no install suggestion.

**Affected commands:** `cm:entries:migrate-html-rte`.

**After:**
```bash
csdx plugins:install @contentstack/cli-cm-migrate-rte
```

Docs: [Migrate content from HTML RTE to JSON RTE](https://www.contentstack.com/docs/developers/cli/migrate-content-from-html-rte-to-json-rte)

### 5. Command and Flag Renames

#### Command Aliases Removed

V2 removes several short-form aliases used in V1:

| Removed Alias | V2 Replacement |
|---|---|
| `csdx cm:export` | `csdx cm:stacks:export` |
| `csdx cm:import` | `csdx cm:stacks:import` |
| `csdx cm:import-setup` | `csdx cm:stacks:import-setup` |
| `csdx tokens` | `csdx auth:tokens:list` |
| `csdx cm:seed` | `csdx cm:stacks:seed` |
| `csdx audit` | `csdx cm:stacks:audit` |
| `csdx cm:migration` | `csdx cm:stacks:migration` |

#### cm:stacks:import-setup

**Alias removed.** Only the full command name works in V2.

**Before:**
```bash
csdx cm:import-setup --stack-api-key blt123
csdx cm:stacks:import-setup -B main
```

**After:**
```bash
csdx cm:stacks:import-setup --stack-api-key blt123
csdx cm:stacks:import-setup --branch main
```

#### cm:stacks:seed

**Alias removed**, and V2 removes the `-s` (stack), `-r` (repo), and `-o` (org) short characters:

**Before:**
```bash
csdx cm:seed -s blt123 -r contentstack/kickstart-stack-seed -o orgUid
```

**After:**
```bash
csdx cm:stacks:seed --stack-api-key blt123 --repo contentstack/kickstart-stack-seed --org orgUid
```

**Interactive mode changed:** Running `csdx cm:stacks:seed` without `--repo` queried the GitHub API for all Contentstack repos in V1. V2 shows a fixed curated list of 3 repos instead: Kickstart stack seed (`contentstack/kickstart-stack-seed`), Kickstart Veda (`contentstack/kickstart-veda-seed`), and Compass starter stack (`contentstack/compass-starter-stack`).

> **Note:** V2 removes `contentstack/stack-starter-app` from the curated list. If you need it, pass it directly with `--repo contentstack/stack-starter-app`.

For any repo not on the curated list, use `--repo owner/repo` directly.

#### cm:bootstrap

V2 removes the `--appName` / `-a`, `--directory` / `-d`, and `--appType` / `-s` flags:

| Removed | V2 Replacement |
|---|---|
| `--appName` / `-a` | `--app-name` |
| `--directory` / `-d` | `--project-dir` |
| `--appType` / `-s` | *(removed, no replacement needed, V2 hardcodes the app type internally)* |

> **Note:** V1 had a short flag collision: both `--appName` and `--alias` claimed `-a`. V2 resolves this. `--app-name` has no short character, and `-a` exclusively means `--alias`. Any script that used `-a` for app name must switch to `--app-name` (long form only).

**Before:**
```bash
csdx cm:bootstrap --appName reactjs --directory ./myapp --appType sampleapp
```

**After:**
```bash
csdx cm:bootstrap --app-name compass-app --project-dir ./myapp
```

**13 app configs removed.** V2 no longer accepts these `--app-name` values. Passing any of them throws `CLI_BOOTSTRAP_INVALID_APP_NAME`.

Removed sample apps (4, were in the `sampleApps` interactive list): `reactjs`, `nextjs`, `gatsby`, `angular`.

Removed starter apps (8, were in the `starterApps` interactive list): `reactjs-starter`, `nextjs-starter`, `gatsby-starter`, `angular-starter`, `nuxt-starter`, `vue-starter`, `stencil-starter`, `nuxt3-starter`.

Removed hidden config entry (1, never shown interactively, but passable through `--app-name`): `nuxtjs-disabled`.

**Valid app names in V2 (8), unchanged from V1's `starterApps` list:** `compass-app`, `kickstart-next`, `kickstart-next-ssr`, `kickstart-next-ssg`, `kickstart-next-graphql`, `kickstart-next-middleware`, `kickstart-nuxt`, `kickstart-nuxt-ssr`.

#### cm:stacks:audit Short Aliases Removed

**Before:**
```bash
csdx audit
csdx audit:fix
```

**After:**
```bash
csdx cm:stacks:audit
csdx cm:stacks:audit:fix
```

For the per-UID file reading change that affects audit results on a V1 export, see [cm:stacks:audit Reads Per-UID Files](#cmstacksaudit-reads-per-uid-files).

#### cm:stacks:migration

V2 removes these flags:

| Removed | V2 Replacement |
|---|---|
| `-B` | `--branch` |
| `-A` | `--alias` |
| `-n` | `--file-path` |
| `--api-key` | `--stack-api-key` |
| `--authtoken` | *(removed, use `csdx auth:login` then `--alias`)* |
| `--management-token-alias` | `--alias` |
| `--filePath` | `--file-path` |
| `--multi` | `--multiple` |

**Before:**
```bash
csdx cm:migration -B feature-branch -n ./migrate.js
```

**After:**
```bash
csdx cm:stacks:migration --branch feature-branch --file-path ./migrate.js
```

#### cm:stacks:validate-regex

V2 removes the `-c`, `-f`, and `-g` short characters:

**Before:**
```bash
csdx cm:stacks:validate-regex -c blog -f ./regex.json -g header
```

**After:**
```bash
csdx cm:stacks:validate-regex --contentType blog --filePath ./regex.json --globalField header
```

The results table and `results.csv` file use the same column order in both V1 and V2: `Module`, `Title`, `UID`, `Invalid Regex Count`. If you parse CSV output by header name, you need no changes.

#### auth:tokens

**Behavior changed.** `csdx auth:tokens` no longer lists your tokens. In V2 it displays sub-command help instead.

**Silent failure risk:** If your script runs `csdx auth:tokens` to get a token table and parses stdout, it silently receives help text instead of a table. V2 raises no error code.

**Before:**
```bash
csdx auth:tokens          # listed tokens in V1
```

**After:**
```bash
csdx auth:tokens:list     # lists tokens in V2
```

V2 also removes the `tokens` short alias. `csdx tokens` fails with "command not found".

#### auth:tokens:add

V2 removes the `-d`, `-m`, and `-t` short characters, removes the hidden `--api-key` flag entirely, and replaces the hidden `-f` / `--force` flag with `-y` / `--yes`:

| Removed | V2 Replacement |
|---|---|
| `-d` | `--delivery` (long form only) |
| `-m` | `--management` (long form only) |
| `-t` | `--token` (long form only) |
| `--api-key` (hidden) | Removed entirely |
| `-f` / `--force` (hidden) | Use `-y` / `--yes` |

**Before:**
```bash
csdx auth:tokens:add -a myalias -d -t bltABC -k blt123
```

**After:**
```bash
csdx auth:tokens:add -a myalias --delivery --token bltABC --stack-api-key blt123
```

#### auth:tokens:remove

**V1:** `-i` / `--ignore` makes the command succeed silently even if the alias does not exist.

**V2:** V2 removes the flag. If the alias does not exist, V2 prints a yellow warning and exits 0 (it raises no error). Scripts that relied on a non-zero exit when you omitted `--ignore` should account for this change.

**Before:**
```bash
csdx auth:tokens:remove -a myalias -i    # silently succeeded even if not found
```

**After:**
```bash
csdx auth:tokens:remove -a myalias       # prints "No token found with alias 'myalias'." (yellow) and exits 0
```

#### auth:logout

V2 removes the hidden `-f` / `--force` flag:

**Before:**
```bash
csdx auth:logout -f
csdx auth:logout --force
```

**After:**
```bash
csdx auth:logout -y
csdx auth:logout --yes
```
Passing `-f` or `--force` in V2 raises an "Unexpected argument" error.

#### config:set:region

V2 removes the `-d`, `-m`, and `-n` short characters:

| Removed | V2 Replacement |
|---|---|
| `-d` | `--cda` |
| `-m` | `--cma` |
| `-n` | `--name` |

**Before:**
```bash
csdx config:set:region -d https://cdn.example.com -m https://api.example.com -n MyRegion
```

**After:**
```bash
csdx config:set:region --cda https://cdn.example.com --cma https://api.example.com --name MyRegion
```

**No prior equivalent in V1: `--cs-assets` flag.** V2 adds a `--cs-assets` flag for specifying the Contentstack Assets API URL when configuring a custom region:

```bash
csdx config:set:region \
  --cma https://custom.cma.example.com \
  --cda https://custom.cda.example.com \
  --ui-host https://custom.ui.example.com \
  --name MyRegion \
  --cs-assets https://custom.am-api.example.com
```

When you omit `--cs-assets`, V2 derives the CS Assets URL from the CMA URL automatically. `config:get:region` also now shows `Contentstack Assets URL` in its output.

#### config:set:log

**V1:** Stores the console log preference as `log["show-console-logs"]` (hyphenated).

**V2:** Stores it as `log["showConsoleLogs"]` (camelCase). The two formats are not compatible. After upgrading, V2 silently ignores your V1 console log configuration, and progress bars become the default.

If your CI needs console log output, re-run:
```bash
csdx config:set:log --show-console-logs
```

To explicitly switch back to progress bars (the V2 default):
```bash
csdx config:set:log --no-show-console-logs
```

See [Troubleshooting](#troubleshooting) for the full failure write-up.

#### config:set:early-access-header

**Documentation fix only, no behavioral change.** V1 had the `--header` and `--header-alias` descriptions swapped:

| Flag | V1 Description (WRONG) | V2 Description (CORRECT) |
|---|---|---|
| `--header-alias` | "Provide the Early Access header value" | "Provide a name (alias) for this Early Access header" |
| `--header` | "Provide the Early Access header alias name" | "Provide the Early Access header value" |

The actual behavior was always: `--header-alias` sets the alias name, and `--header` sets the header value. If you followed V1's incorrect help text and passed values in the wrong order, correct your scripts:

```bash
csdx config:set:early-access-header --header-alias myheader --header x-header-value
```

#### tsgen

`tsgen` generates TypeScript type definitions from your stack's content types. If you use the Contentstack TypeScript SDK and want type-safe content model access in your codebase, use this command. See the [tsgen plugin docs](https://www.contentstack.com/docs/headless-cms/tsgen-plugin) for full usage.

V2 renames `--token-alias` to `--alias`, and removes the `-o`, `-p`, and `-d` short characters. The `-a` short character stays on the renamed `--alias` flag:

| Change | Details |
|---|---|
| `--token-alias` renamed to `--alias` | The full flag name changed, `--token-alias` now produces "Nonexistent flag:" |
| `-o` removed | Was short for `--output` |
| `-p` removed | Was short for `--prefix` |
| `-d` removed | Was short for `--doc` |
| `-a` (short for alias) | **KEPT** on the renamed `--alias` flag |

**Before:**
```bash
csdx tsgen --token-alias myalias -o ./types -p CS_ -d
```

**After:**
```bash
csdx tsgen --alias myalias --output ./types --prefix CS_ --doc
# or use -a for alias:
csdx tsgen -a myalias --output ./types --prefix CS_ --doc
```

#### app:create

V2 removes the `-n` short character:

**Before:**
```bash
csdx app:create -n my-app
```

**After:**
```bash
csdx app:create --name my-app
```

#### migrate:convert

V2 removes the `-o`, `-m`, and `-a` short characters:

| Removed | V2 Replacement |
|---|---|
| `-o` | `--output` |
| `-m` | `--master-locale` |
| `-a` | `--affix` |

**Before:**
```bash
csdx migrate:convert -o ./output -m en-us -a v2_
```

**After:**
```bash
csdx migrate:convert --output ./output --master-locale en-us --affix v2_
```

#### migrate:export

V2 removes the `-o` short character:

**Before:**
```bash
csdx migrate:export -o ./output
```

**After:**
```bash
csdx migrate:export --output ./output
```

#### content-type:* Commands

> **Note on the `content-type:*` namespace:** These commands belong to a separate plugin (`@contentstack/contentstack-content-type`) that inspects and compares content type schemas. They are distinct from `cm:stacks:*` commands: they do not export or import content, they analyze schema structure. If you use any `content-type:*` commands, the flag changes below apply.

**content-type:audit.** V2 removes `--stack` / `-s` (use `--stack-api-key` / `-k`), renames `--token-alias` / `-a` to `--alias` / `-a`, and removes `-c` (use `--content-type`):

```bash
# V1
csdx content-type:audit --stack blt123 --token-alias myalias -c blog

# V2
csdx content-type:audit --stack-api-key blt123 --alias myalias --content-type blog
```

**content-type:compare.** Same `--stack`, `--token-alias`, and `-c` changes as `content-type:audit`, plus V2 removes `-l` (use `--left`) and `-r` (use `--right`):

```bash
# V1
csdx content-type:compare --stack blt123 --token-alias myalias -c blog -l v1 -r v2

# V2
csdx content-type:compare --stack-api-key blt123 --alias myalias --content-type blog --left v1 --right v2
```

**content-type:compare-remote.** V2 removes `-o` (use `--origin-stack`), `-r` (use `--remote-stack`), and `-c` (use `--content-type`). Note that `content-type:compare-remote` never had `--stack` / `--token-alias` flags in V1:

```bash
# V1
csdx content-type:compare-remote -o bltOrigin -r bltRemote -c blog

# V2
csdx content-type:compare-remote --origin-stack bltOrigin --remote-stack bltRemote --content-type blog
```

**content-type:details.** Same `--stack`, `--token-alias`, and `-c` changes as `content-type:audit`, plus V2 removes `-p` (use `--path`):

```bash
# V1
csdx content-type:details --stack blt123 --token-alias myalias -c blog -p fields.title

# V2
csdx content-type:details --stack-api-key blt123 --alias myalias --content-type blog --path fields.title
```

**content-type:diagram.** Same `--stack` and `--token-alias` changes as `content-type:audit`, plus V2 removes `-o` (use `--output`), `-d` (use `--direction`), and `-t` (use `--type`):

```bash
# V1
csdx content-type:diagram --stack blt123 --token-alias myalias -o ./diagram.svg -d LR -t svg

# V2
csdx content-type:diagram --stack-api-key blt123 --alias myalias --output ./diagram.svg --direction LR --type svg
```

**content-type:list.** Same `--stack` and `--token-alias` changes as `content-type:audit`, plus V2 removes `-o` (use `--order`):

```bash
# V1
csdx content-type:list --stack blt123 --token-alias myalias -o asc

# V2
csdx content-type:list --stack-api-key blt123 --alias myalias --order asc
```

### 6. New Features

#### CS Assets (Asset Management 2.0)

**No prior equivalent in V1.** V2 adds full support for Contentstack's CS Assets system (AM 2.0). See [CS Assets (Asset Management 2.0) Support](#cs-assets-asset-management-20-support) for the export directory structure and detection behavior.

**New bulk operations:** `cm:stacks:bulk-assets --operation delete` and `--operation move` for CS Assets, using the new `--space-uid`, `--org-uid`, `--workspace`, `--asset-uids-file`, and `--target-folder-uid` flags. See [cm:stacks:bulk-assets Replaces Asset Publish Commands](#cmstacksbulk-assets-replaces-asset-publish-commands).

#### Taxonomy Publishing

New in V2 across export, import, and bulk operations:

- **Export** captures `publish_details` per locale for each taxonomy. V1 did not capture this.
- **Import** re-publishes taxonomies after import by default. To skip publishing (for example, if you want to review entries before publishing):
  ```bash
  csdx cm:stacks:import --skip-taxonomy-publish -d ./export -k bltXXX
  ```
- **`cm:stacks:bulk-taxonomies`** provides bulk taxonomy publish operations with no prior equivalent in V1. See [cm:stacks:bulk-taxonomies (New)](#cmstacksbulk-taxonomies-new).

#### Global Fields Per-File Export

Each global field now exports as its own `<uid>.json` file, the same format as content types. See [Per-UID Files Replace Aggregate JSON Files](#per-uid-files-replace-aggregate-json-files) for the full file structure change.

#### Visual Progress System

All major operations now show visual progress bars and a summary table at the end of the run. See [config:set:log](#configsetlog) to restore console log output for CI environments.

## Troubleshooting

### Global fields silently skipped on import

**Symptom:** Running V2 import against a V1 export completes with no error, but the stack ends up with zero global fields.

**Root cause:** V2's per-UID file readers explicitly ignore `globalfields.json`. V1 export writes global fields only to that single aggregate file, with no per-UID files.

**Resolution:** Re-export your stack with V2 before importing. See [Content Types and Global Fields Silently Skipped on Import](#content-types-and-global-fields-silently-skipped-on-import).

### Branch export silently overwrites another branch's data

**Symptom:** You export two branches to the same `--data-dir`, and the second export contains only the second branch's content, with no warning that the first branch's export was lost.

**Root cause:** V2 always writes flat output with no `<branch-uid>/` subfolder, regardless of how you select the branch.

**Resolution:** Use a separate `--data-dir` per branch. See [Branch Export Behavior Changed](#branch-export-behavior-changed).

### V1 console log config silently ignored after upgrade

**Symptom:** After upgrading, a CI pipeline that previously received plain console log output now receives progress bar escape codes instead, with no error raised.

**Root cause:** V2 renamed the internal config key from `log["show-console-logs"]` to `log["showConsoleLogs"]`. The two formats are not compatible, so V2 silently ignores the V1 setting.

**Resolution:** Re-run `csdx config:set:log --show-console-logs` after upgrading. See [config:set:log](#configsetlog).

### V1 multi-branch export produces an empty import

**Symptom:** Pointing V2 import at the root of a V1 multi-branch export directory completes with no error, but imports zero content.

**Root cause:** V2 removes the `selectBranchFromDirectory` auto-detection logic that V1 import used to read `branches.json` and navigate to the correct `<branch-uid>/` subfolder. V2 import reads directly from whatever path you give `--data-dir`, finds only `branches.json` at the export root, and finds no content files.

**Resolution:** Point `--data-dir` directly at the branch subfolder, for example `--data-dir ./my-export/main`. See [Content Types and Global Fields Silently Skipped on Import](#content-types-and-global-fields-silently-skipped-on-import).

### cm:stacks:audit reports zero global-field issues on a V1 export (false clean)

**Symptom:** Running `cm:stacks:audit` against a V1 export directory reports zero global field issues, even on a stack known to have global field problems.

**Root cause:** `cm:stacks:audit` uses the same per-UID-only schema readers as V2 import, and a V1 export writes global fields only to `globalfields.json`, with no per-UID files for the reader to find.

**Resolution:** Re-export global fields with V2 before auditing. See [cm:stacks:audit Reads Per-UID Files](#cmstacksaudit-reads-per-uid-files).

### Rolling back after a broken upgrade

**Symptom:** The V2 upgrade breaks a workflow badly enough that you need to return to V1 while you investigate.

**Root cause:** Not applicable. This is a recovery procedure, not a failure diagnosis, but it belongs here since it is the section a developer reaches for when something has gone wrong.

**Resolution:**
1. Restore from your pre-upgrade stack export (see [Install V2](#install-v2) for the note on keeping a pre-upgrade export).
2. Downgrade the CLI: `npm install -g @contentstack/cli@1.x`.
3. Your tokens remain available. Both V1 and V2 read from the same token store.

## Pre-Upgrade Checklist

This checklist orders items by risk. Complete top sections before lower ones.

### Critical: Do These First

- [ ] Test the entire upgrade in a non-production environment before touching production.
- [ ] **Your saved tokens carry over automatically.** Management tokens stored with `csdx auth:tokens:add` are available immediately after upgrading. You need no re-authentication. ([Install V2](#install-v2))

### High-Risk Script Changes

- [ ] Add an explicit `--branch` flag to all `cm:stacks:export` calls for non-main branches. V2 only exports `main` when you omit `--branch`. ([Branch Export Behavior Changed](#branch-export-behavior-changed))
- [ ] Use a separate `--data-dir` per branch. V2 output is always flat (no `<branch-uid>/` subfolder), and exporting two branches to the same directory silently overwrites the first. ([Branch export silently overwrites another branch's data](#branch-export-silently-overwrites-another-branchs-data))
- [ ] Rewrite all `cm:entries:publish*`, `cm:assets:publish*`, `cm:bulk-publish:*`, `cm:stacks:publish`, and `cm:stacks:unpublish` calls to `cm:stacks:bulk-entries` / `cm:stacks:bulk-assets`. ([cm:stacks:bulk-entries Replaces the Bulk Publish Plugin](#cmstacksbulk-entries-replaces-the-bulk-publish-plugin))
- [ ] Verify publish behavior in a staging stack. All bulk publish and unpublish calls now use `api_version: '3.2'`, and V2 removes the `--api-version` flag. ([--api-version Flag Removed Everywhere](#--api-version-flag-removed-everywhere))
- [ ] Remove checks for `export-info.json` or `content_types/schema.json` in post-export tooling. V2 does not write these files. ([export-info.json No Longer Written](#export-infojson-no-longer-written))
- [ ] Update tooling that reads `global_fields/globalfields.json` to iterate per-UID JSON files instead. ([Per-UID Files Replace Aggregate JSON Files](#per-uid-files-replace-aggregate-json-files))

### CI / Pipeline Audit

- [ ] Verify your CI does not parse stdout for success signals. Output format changed, since progress bars are now the default. ([Progress Bars Replace Console Logs](#progress-bars-replace-console-logs))
- [ ] Run `csdx config:set:log --show-console-logs` after upgrading if your CI parses console output. V2 silently drops the V1 log setting. ([V1 console log config silently ignored after upgrade](#v1-console-log-config-silently-ignored-after-upgrade))

### Script Audit: Command Renames

- [ ] Replace `csdx cm:export` with `csdx cm:stacks:export`. ([Command Aliases Removed](#command-aliases-removed))
- [ ] Replace `csdx cm:import` with `csdx cm:stacks:import`. ([Command Aliases Removed](#command-aliases-removed))
- [ ] Replace `csdx cm:import-setup` with `csdx cm:stacks:import-setup`. ([cm:stacks:import-setup](#cmstacksimport-setup))
- [ ] Replace `csdx cm:seed` with `csdx cm:stacks:seed`. ([cm:stacks:seed](#cmstacksseed))
- [ ] Replace `csdx tokens` with `csdx auth:tokens:list`. ([auth:tokens](#authtokens))
- [ ] Replace `csdx auth:tokens` (when used as the list command) with `csdx auth:tokens:list`. ([auth:tokens](#authtokens))
- [ ] Replace `csdx audit` with `csdx cm:stacks:audit`. ([cm:stacks:audit Short Aliases Removed](#cmstacksaudit-short-aliases-removed))

### Script Audit: Flag Changes

- [ ] Remove `--stack-uid` / `-s` everywhere and use `--stack-api-key` instead. ([Type Mapping Reference](#type-mapping-reference))
- [ ] Remove `--data` and use `--data-dir` instead. ([Type Mapping Reference](#type-mapping-reference))
- [ ] Remove `--management-token-alias` and use `--alias` instead. ([Type Mapping Reference](#type-mapping-reference))
- [ ] Remove `--auth-token` / `-A` and use `csdx auth:login` then `--alias` instead. ([Type Mapping Reference](#type-mapping-reference))
- [ ] Remove `--skip-app-recreation` from all import scripts. V2 has no replacement. ([Content Types and Global Fields Silently Skipped on Import](#content-types-and-global-fields-silently-skipped-on-import))
- [ ] Remove `--token-alias` on `tsgen` and use `--alias` instead. ([tsgen](#tsgen))
- [ ] Audit scripts for removed short flags on export and import commands: `-m` / `-t` / `-B` / `-b` / `-A` (use the long form only). See [Type Mapping Reference](#type-mapping-reference) for the full list.
- [ ] Update `cm:bootstrap` flags: `--appName` to `--app-name`, `--directory` to `--project-dir`. ([cm:bootstrap](#cmbootstrap))
- [ ] Remove bootstrap app names that no longer exist: `reactjs`, `nextjs`, `gatsby`, `angular`, and the `*-starter` variants. ([cm:bootstrap](#cmbootstrap))
- [ ] Update `content-type:*` commands: remove `--stack` / `-s`, `--token-alias` / `-a`, and all listed short characters. ([content-type:* Commands](#content-type-commands))
- [ ] Replace `csdx auth:logout -f` / `--force` with `csdx auth:logout -y` / `--yes`. ([auth:logout](#authlogout))

### Plugin Management

- [ ] Install the `launch` plugin separately if you use `launch:*` commands: `csdx plugins:install @contentstack/cli-launch`. ([launch Plugin Now Opt-In](#launch-plugin-now-opt-in))
- [ ] Install the `migrate-rte` plugin separately if you use `cm:entries:migrate-html-rte`: `csdx plugins:install @contentstack/cli-cm-migrate-rte`. ([migrate-rte Plugin Now Opt-In](#migrate-rte-plugin-now-opt-in))
- [ ] If you use CS Assets, verify your stack has linked workspaces configured in Contentstack Assets settings. Otherwise export falls back to standard asset export. ([CS Assets (Asset Management 2.0) Support](#cs-assets-asset-management-20-support))

### Custom Plugins (Plugin Authors Only)

- [ ] Update `engines.node` to `>=22.0.0` in your plugin's `package.json`. ([Node.js 22 Requirement](#nodejs-22-requirement))

### Test Run

- [ ] Run a full export and import cycle on a non-production stack before cutting over.
- [ ] Verify branch exports capture the correct branches explicitly.
- [ ] If you use CS Assets, verify your stack has linked workspaces configured. Otherwise export falls back to standard asset export automatically, with no error.
- [ ] If you use bulk publish or unpublish, run a test publish in staging. All calls now use `api_version: '3.2'`.

## Next Steps

- [Contentstack CLI documentation](https://www.contentstack.com/docs/headless-cms/install-the-cli) for the full V1 CLI reference.
- [Migrate content from HTML RTE to JSON RTE](https://www.contentstack.com/docs/developers/cli/migrate-content-from-html-rte-to-json-rte) for the `migrate-rte` plugin, now opt-in in V2.
- [tsgen plugin docs](https://www.contentstack.com/docs/headless-cms/tsgen-plugin) for full `tsgen` usage.
- CLI changelog: TODO, add a link once a public CLI V2 changelog URL exists. The source content for this guide has no changelog URL to carry over.
