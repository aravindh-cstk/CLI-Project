---
sidebar: cliSidebar
---

# Contentstack CLI V2 Migration Guide

> **CLI Version:** 2.0.0
> **Node.js requirement:** `>=22.0.0`
> **V1 Reference Docs:** [Contentstack CLI documentation](https://www.contentstack.com/docs/headless-cms/install-the-cli)

---

## Table of Contents

1. [Before You Upgrade](#1-before-you-upgrade)
2. [CLI-Wide Changes](#2-cli-wide-changes)
   - [2.4 All Publish Operations Now Use NRP](#24-all-publish-operations-now-use-nrp)
3. [Removed Plugins — Install Separately](#3-removed-plugins)
4. [Command Migration Reference](#4-command-migration-reference)
   - [Flag Changes — All Commands Quick Reference](#flag-changes--all-commands-quick-reference)
   - [cm:stacks:export](#cmstacksexport)
   - [cm:stacks:import](#cmstacksimport)
   - [cm:stacks:import-setup](#cmstacksimport-setup)
   - [cm:stacks:bulk-entries](#cmstacksbulk-entries) ← replaces 7 V1 commands
   - [cm:stacks:bulk-assets](#cmstacksbulk-assets) ← replaces 2 V1 commands
   - [cm:stacks:bulk-taxonomies](#cmstacksbulk-taxonomies)
   - [cm:stacks:seed](#cmstacksseed)
   - [cm:bootstrap](#cmbootstrap)
   - [cm:stacks:audit](#cmstacksaudit)
   - [cm:stacks:migration](#cmstacksmigration)
   - [cm:stacks:validate-regex](#cmstacksvalidate-regex)
   - [auth:tokens](#authtokens)
   - [auth:tokens:add](#authtokensadd)
   - [auth:tokens:remove](#authtokensremove)
   - [auth:logout](#authlogout)
   - [config:set:region](#configsetregion)
   - [config:set:log](#configsetlog)
   - [tsgen](#tsgen)
   - [app:create](#appcreate)
   - [migrate:convert](#migrateconvert)
   - [migrate:export](#migrateexport)
   - [content-type:audit](#content-typeaudit)
   - [content-type:compare](#content-typecompare)
   - [content-type:compare-remote](#content-typecompare-remote)
   - [content-type:details](#content-typedetails)
   - [content-type:diagram](#content-typediagram)
   - [content-type:list](#content-typelist)
5. [New Features](#5-new-features)
6. [Pre-Upgrade Checklist](#6-pre-upgrade-checklist)
7. [Rollback Plan](#7-rollback-plan)

---

## 1. Before You Upgrade

> **⚠️ Silent Failures — Read These First**
>
> These three behaviors produce **no error, no warning, and no non-zero exit code.** Your script or pipeline will appear to succeed while data is missing or wrong.
>
> 1. **Global fields silently skipped on import** — Running V2 import on a V1 export silently imports zero global fields. All global fields "complete successfully" with nothing created. → [Details](#critical-importing-a-v1-export--content-types-and-global-fields-silently-skipped)
> 2. **Branch export silently overwrites** — Exporting two branches to the same `--data-dir` silently overwrites the first with no error. → [Details](#branch-export-behavior-changed--critical)
> 3. **V1 console log config silently dropped** — After upgrading, your V1 `show-console-logs` setting is ignored. Output switches to progress bars. CI that parses stdout will silently receive different output. → [Details](#config-key-changed--v1-settings-lost-on-upgrade)

### Critical: Node.js 22+

**V2 requires Node.js >=22.0.0.**

```bash
node --version   # must be v22.0.0 or higher
```

> **On Node 18 or 20:** `npm install -g @contentstack/cli` will complete with `EBADENGINE` warnings and appear to succeed — but the CLI will fail at runtime. Upgrade Node first, then install.

If you need to upgrade Node:
```bash
nvm install 22
nvm alias default 22   # makes 22 the permanent default, not just for this shell session
nvm use 22
```

Before installing, confirm Node 22 is in place everywhere the CLI runs:

- [ ] Dev machines — `node --version` shows v22+
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

> **Upgrade note:** `npm install -g` replaces the `csdx` binary in place. There is a ~30-second window during installation where `csdx` is unavailable. For CI pipelines, run the install and the CLI commands in the same pipeline step — do not rely on a pre-installed binary from a prior step.
>
> **Running V1 and V2 side by side:** npm global install can only have one version active per Node environment. If you need V1 available during testing, install it under a different nvm Node version (e.g. `nvm use 20 → npm install -g @contentstack/cli@1.x`; `nvm use 22 → npm install -g @contentstack/cli@2.0.0`).
>
> **On a 2.x beta:** Upgrade directly to 2.0.0: `npm install -g @contentstack/cli@2.0.0`. Your tokens and stored config carry over automatically.

> **Note:** Your existing saved tokens (management tokens added with `csdx auth:tokens:add`) carry over automatically — you do not need to re-authenticate after upgrading.
>
> **Other stored config (proxy settings, region config) also carries over unchanged.** The only exception is the console log setting — if you ran `csdx config:set:log --show-console-logs` in V1, re-run it after upgrading (V2 uses a different internal key and the V1 setting is silently ignored).

### Re-run your log config (CI and pipelines only)

V2 changes its internal config key for console log mode. If you ran `csdx config:set:log --show-console-logs` in V1, that setting is silently lost after upgrading — V2 will not pick it up.

If your CI environment parses console output from the CLI, re-run this after upgrading:

```bash
csdx config:set:log --show-console-logs
```

If you use the default terminal (not CI), you do not need to do anything — progress bars are the default.

---

## 2. CLI-Wide Changes

These changes affect every user regardless of which commands you run.

### 2.1 Default Output — Progress Bars Replace Console Logs

**V1:** All operations print text line-by-line to stdout as they run. Scripts and CI can parse this output.

**V2:** Visual progress bars render in the terminal. Console log output is suppressed by default. End of run shows only a summary and log file path.

**Effect:** Any script or CI pipeline parsing stdout for success/failure signals will receive different output. No error is raised — output is simply different.

> **CI environments:** V2 does not auto-detect non-interactive (non-TTY) environments. Progress bars render regardless of whether stdout is a terminal. If you see escape code characters in your CI logs, enable console log mode to get plain text output instead.

To restore console log output for CI, use `csdx config:set:log --show-console-logs` (see [config:set:log](#configsetlog) for full flag reference).

Logs are written to a `logs/` directory in whichever folder you ran the CLI from (e.g. `./logs/`). Set `CS_CLI_LOG_PATH` env var or `csdx config:set:log --path <dir>` to redirect logs.

### 2.2 Deprecated Flags Are Gone — No More Warnings

In V1, deprecated flags (like `--stack-uid`, `--data`, `-s`, `-B`) printed a deprecation warning but still worked. In V2 they are **completely removed**. Passing them now causes an immediate error:

```
ERROR: Nonexistent flag: --stack-uid
```

There are no runtime warnings to catch this. You must audit your scripts before upgrading.

### 2.3 All Single-Character Short Flags Cleaned Up

V2 systematically removed single-character short flags that conflicted with global CLI flags or were ambiguous across commands. In every case the long form still works. See each command section for the specific chars removed.


### 2.4 All Publish Operations Now Use NRP

In V2, all publish operations — including entry/asset/taxonomy publishes triggered during import and all bulk publish/unpublish commands — go through the NRP API. This was not the case in V1 for import; and for bulk publish, V1 exposed an `--api-version` flag that let you control this.

**What changed:**

| Command | V1 | V2 |
|---|---|---|
| `cm:stacks:import` (auto-publish) | Did not use NRP | Uses NRP for all entry, asset, and taxonomy publishes |
| `cm:stacks:bulk-entries` | `--api-version` flag let you opt in or out | Always uses NRP; `--api-version` flag removed |
| `cm:stacks:bulk-assets` | `--api-version` flag let you opt in or out | Always uses NRP; `--api-version` flag removed |

**Impact:** Your stack must have NRP enabled. There is no flag in V2 to run publish operations without NRP.

> **Note:** Passing `--api-version` to `cm:stacks:bulk-entries` or `cm:stacks:bulk-assets` in V2 causes an immediate error: `ERROR: Nonexistent flag: --api-version`.

### 2.6 Command Aliases Removed

Several short-form aliases used in V1 are gone:

| Removed Alias | V2 Replacement |
|---|---|
| `csdx cm:export` | `csdx cm:stacks:export` |
| `csdx cm:import` | `csdx cm:stacks:import` |
| `csdx cm:import-setup` | `csdx cm:stacks:import-setup` |
| `csdx tokens` | `csdx auth:tokens:list` |
| `csdx cm:seed` | `csdx cm:stacks:seed` |
| `csdx audit` | `csdx cm:stacks:audit` |
| `csdx cm:migration` | `csdx cm:stacks:migration` |

---

## 3. Removed Plugins

### 3.1 `launch` Plugin — Now Opt-In

`launch:*` commands are no longer bundled in the V2 CLI. When you run any `launch:*` command, V2 prints a guided error with the install instruction and exits with code 127.

**Affected commands:** `launch`, `launch:deployments`, `launch:environments`, `launch:functions`, `launch:logs`, `launch:open`, `launch:rollback`

**Migration:**
```bash
csdx plugins:install @contentstack/cli-launch
```

### 3.2 `migrate-rte` Plugin — Now Opt-In

`cm:entries:migrate-html-rte` is no longer bundled in the V2 CLI. Unlike `launch`, V2 does **not** print a guided error — the shell returns "command not found" with no install suggestion.

**Affected commands:** `cm:entries:migrate-html-rte`

**Migration:**
```bash
csdx plugins:install @contentstack/cli-cm-migrate-rte
```

Docs: [Migrate content from HTML RTE to JSON RTE](https://www.contentstack.com/docs/developers/cli/migrate-content-from-html-rte-to-json-rte)

---

## 4. Command Migration Reference

### Flag Changes — All Commands Quick Reference

All flag renames and removed short chars across every command. Rows with the same V1 and V2 flag name had only their short char removed.

| Command | V1 Flag | V1 Short | V2 Flag | V2 Short |
|---|---|---|---|---|
| `cm:stacks:export` | `--stack-uid` | `-s` | `--stack-api-key` | `-k` |
| | `--data` | — | `--data-dir` | — |
| | `--management-token-alias` | — | `--alias` | `-a` |
| | `--auth-token` | `-A` | *(removed — use OAuth + `--alias`)* | — |
| | `--module` | `-m` | `--module` | — |
| | `--content-types` | `-t` | `--content-types` | — |
| | `--branch` | `-B` | `--branch` | — |
| `cm:stacks:import` | `--stack-uid` | `-s` | `--stack-api-key` | `-k` |
| | `--data` | — | `--data-dir` | — |
| | `--management-token-alias` | — | `--alias` | `-a` |
| | `--auth-token` | `-A` | *(removed — use OAuth + `--alias`)* | — |
| | `--module` | `-m` | `--module` | — |
| | `--backup-dir` | `-b` | `--backup-dir` | — |
| | `--branch` | `-B` | `--branch` | — |
| | `--skip-app-recreation` | — | *(removed — no replacement)* | — |
| `cm:stacks:import-setup` | `--branch` | `-B` | `--branch` | — |
| `cm:stacks:seed` | `--stack` | `-s` | `--stack-api-key` | — |
| | `--repo` | `-r` | `--repo` | — |
| | `--org` | `-o` | `--org` | — |
| `cm:stacks:migration` | `--branch` | `-B` | `--branch` | — |
| | `--authtoken` | `-A` | `--authtoken` | — |
| | `--filePath` | `-n` | `--file-path` | — |
| `cm:stacks:validate-regex` | `--contentType` | `-c` | `--contentType` | — |
| | `--filePath` | `-f` | `--filePath` | — |
| | `--globalField` | `-g` | `--globalField` | — |
| `cm:bootstrap` | `--appName` | `-a` | `--app-name` | — |
| | `--directory` | `-d` | `--project-dir` | — |
| `auth:tokens:add` | `--delivery` | `-d` | `--delivery` | — |
| | `--management` | `-m` | `--management` | — |
| | `--token` | `-t` | `--token` | — |
| | `--api-key` | — | *(removed)* | — |
| | `--force` | `-f` | `--yes` | `-y` |
| `auth:tokens:remove` | `--ignore` | `-i` | *(removed)* | — |
| `auth:logout` | `--force` | `-f` | `--yes` | `-y` |
| `config:set:region` | `--cda` | `-d` | `--cda` | — |
| | `--cma` | `-m` | `--cma` | — |
| | `--name` | `-n` | `--name` | — |
| `tsgen` | `--token-alias` | — | `--alias` | `-a` |
| | `--output` | `-o` | `--output` | — |
| | `--prefix` | `-p` | `--prefix` | — |
| | `--doc` | `-d` | `--doc` | — |
| `app:create` | `--name` | `-n` | `--name` | — |
| `migrate:convert` | `--output` | `-o` | `--output` | — |
| | `--master-locale` | `-m` | `--master-locale` | — |
| | `--affix` | `-a` | `--affix` | — |
| `migrate:export` | `--output` | `-o` | `--output` | — |
| `content-type:audit` | `--stack` | `-s` | `--stack-api-key` | `-k` |
| | `--token-alias` | `-a` | `--alias` | `-a` |
| | `--content-type` | `-c` | `--content-type` | — |
| `content-type:compare` | `--stack` | `-s` | `--stack-api-key` | `-k` |
| | `--token-alias` | `-a` | `--alias` | `-a` |
| | `--content-type` | `-c` | `--content-type` | — |
| | `--left` | `-l` | `--left` | — |
| | `--right` | `-r` | `--right` | — |
| `content-type:compare-remote` | `--origin-stack` | `-o` | `--origin-stack` | — |
| | `--remote-stack` | `-r` | `--remote-stack` | — |
| | `--content-type` | `-c` | `--content-type` | — |
| `content-type:details` | `--stack` | `-s` | `--stack-api-key` | `-k` |
| | `--token-alias` | `-a` | `--alias` | `-a` |
| | `--content-type` | `-c` | `--content-type` | — |
| | `--path` | `-p` | `--path` | — |
| `content-type:diagram` | `--stack` | `-s` | `--stack-api-key` | `-k` |
| | `--token-alias` | `-a` | `--alias` | `-a` |
| | `--output` | `-o` | `--output` | — |
| | `--direction` | `-d` | `--direction` | — |
| | `--type` | `-t` | `--type` | — |
| `content-type:list` | `--stack` | `-s` | `--stack-api-key` | `-k` |
| | `--token-alias` | `-a` | `--alias` | `-a` |
| | `--order` | `-o` | `--order` | — |

---

### cm:stacks:export


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `--stack-uid` / `-s` | `--stack-api-key` |
| `--data` | `--data-dir` |
| `--management-token-alias` | `--alias` |
| `--auth-token` / `-A` | Use `csdx auth:login` then `--alias` |
| `-m` | `--module` (long form only) |
| `-t` | `--content-types` (long form only) |
| `-B` | `--branch` (long form only) |

**Before:**
```bash
csdx cm:stacks:export -s blt123 --data ./export -m content_types -t blog article -B main
```

**After:**
```bash
csdx cm:stacks:export --stack-api-key blt123 --data-dir ./export --module content_types --content-types blog article --branch main
```

#### Branch Export Behavior Changed — CRITICAL

**V1:** When `--branch` is not specified, exports ALL branches. Output is nested under `exportDir/<branch-uid>/...` for each branch.

**V2:** Two independent changes:
1. **Default branch:** When `--branch` is not specified, only the branch named `main` is exported. If no `main` branch exists, the command errors.
2. **No branch subfolder — always:** Even when `--branch` IS specified, V2 writes output flat to `exportDir/...` with no `<branch-uid>/` subfolder. This applies regardless of how the branch is selected.

**Impact for multi-branch stacks:** You must export each branch to a separate `--data-dir`. If you export two branches to the same directory, the second export overwrites the first — no error is raised.

3. **`branches.json` removed:** V1 wrote a `branches.json` file to the export root listing all branches at export time. V2 does not write this file — no error is raised. If your import pipeline or post-export tooling reads `branches.json`, remove that step.

```bash
# V2: one --data-dir per branch
csdx cm:stacks:export --branch main       --data-dir ./export-main    --stack-api-key bltXXX
csdx cm:stacks:export --branch feature-x  --data-dir ./export-feature --stack-api-key bltXXX
csdx cm:stacks:export --branch-alias prod --data-dir ./export-prod     --stack-api-key bltXXX
```

#### `export-info.json` No Longer Written

V1 wrote `export-info.json` to the export directory containing `{ "contentVersion": 2, "logsPath": "..." }`. V2 does not write this file. If your pipeline checks for this file or reads `contentVersion` from it, remove that step.

#### `content_types/schema.json` Removed

> **Action required if your tooling reads this file.** If any pipeline or script reads `export/content_types/schema.json`, it will fail on a V2 export with no error message — the file simply does not exist.

V1 wrote a combined `content_types/schema.json` with all content type schemas in one array. V2 only writes individual `content_types/<uid>.json` files. The aggregate file is gone.

```bash
# V1 export — aggregate file
cat export/content_types/schema.json

# V2 export — iterate per-UID files instead
ls export/content_types/*.json
```

#### Global Fields Format Changed (per-file)

> **Action required if your tooling reads `globalfields.json`.** If any pipeline or script reads `export/global_fields/globalfields.json`, it will fail on a V2 export — the file does not exist.

V1 wrote all global fields to `global_fields/globalfields.json` (one file). V2 writes one file per global field UID:

```
# V1
export/global_fields/globalfields.json

# V2
export/global_fields/my_header.json
export/global_fields/my_footer.json
export/global_fields/shared_banner.json
```

Update any tooling that reads `globalfields.json` to iterate per-UID files instead.

#### Module Flag Now Validated + `studio` Renamed

In V2, `--module` is validated against an explicit allowed-values list before any operation starts. Passing an invalid module name fails immediately with a clear error instead of failing mid-operation.

V1's `--module studio` value is renamed to `--module composable-studio` in V2. Using the old value fails:

```
Error: Expected --module=studio to be one of: stack, assets, locales, ...composable-studio
```

```bash
# V1
csdx cm:stacks:export --module studio

# V2
csdx cm:stacks:export --module composable-studio
```

Two additional modules are now valid export targets (not present in V1): `publishing-rules`, `personalize`.

---

### cm:stacks:import


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `--stack-uid` / `-s` | `--stack-api-key` |
| `--data` | `--data-dir` |
| `--management-token-alias` | `--alias` |
| `--auth-token` / `-A` | Use `csdx auth:login` then `--alias` |
| `-m` | `--module` (long form only) |
| `-b` | `--backup-dir` (long form only) |
| `-B` | `--branch` (long form only) |
| `--skip-app-recreation` | **Removed with no replacement** |

**Before:**
```bash
csdx cm:stacks:import -s blt123 --data ./export -b ./backup -B main
```

**After:**
```bash
csdx cm:stacks:import --stack-api-key blt123 --data-dir ./export --backup-dir ./backup --branch main
```

> **Important:** `--skip-app-recreation` is completely removed. There is no replacement. Remove it from all import scripts.
>
> `--skip-taxonomy-publish` is a **new, unrelated** flag (see [New Features](#5-new-features)). It does not replace `--skip-app-recreation`.

The following flags exist in **both V1 and V2** and require no migration: `--branch-alias`, `--skip-audit`, `--exclude-global-modules`, `--replace-existing`, `--skip-existing`, `--import-webhook-status`, `--personalize-project-name`, `--skip-assets-publish`, `--skip-entries-publish`.

#### Module Flag Validates Against a Strict List

Same as export: V2 validates `--module` on import before any operation begins. `--module studio` fails — use `--module composable-studio`. `--module variant-entries` is a new valid value in V2 (not available in V1).

#### CRITICAL: Importing a V1 Export — Content Types and Global Fields Silently Skipped

V2's importers use per-UID file readers that **explicitly ignore aggregate files**. The impact differs between modules because V1 export behavior differs:

| Module | V1 export writes | V2 importer reads | Impact on V1 export |
|---|---|---|---|
| Content types | Individual `<uid>.json` files **+ `schema.json`** | Per-UID files only (ignores `schema.json`) | **No impact** — per-UID files exist, content types import correctly |
| Global fields | `globalfields.json` only (no individual files) | Per-UID files only (ignores `globalfields.json`) | **Silently skipped** — no per-UID files exist in a V1 export |

**Impact:** Running V2 import on a V1 export silently skips **all global fields** — no error, no warning. Global fields complete "successfully" with zero items created. Content types are unaffected.

**Resolution:** Re-export your stack with V2 before importing — this is the correct fix. A migration conversion script will be provided separately for cases where a V2 re-export is not possible.

#### CRITICAL: V1 Multi-Branch Export — Auto Branch Detection Removed

V1 import auto-detected the branch by reading `branches.json` at the export root and navigating to the correct `<branch-uid>/` subfolder. This `selectBranchFromDirectory` logic is removed in V2.

**V1 behavior:**
```bash
csdx cm:stacks:import --data-dir ./my-export    # V1 read branches.json → auto-navigated to ./my-export/main/
```

**V2 behavior:** `--data-dir` must point directly to the content, not the root.
```bash
csdx cm:stacks:import --data-dir ./my-export/main    # V2: specify the branch subfolder explicitly
```

If you point V2 import at a V1 multi-branch export root, it will attempt to read content files directly from the root (where only `branches.json` lives), find nothing, and silently produce an empty import.

#### `composable-studio` Module Requires Basic Auth

The composable-studio module is skipped in two cases:

- **Management token** (`--alias` pointing to a management token):
  ```
  Skipping Studio project import when using management token
  ```
- **OAuth** (`csdx auth:login --oauth`):
  ```
  Skipping Studio project import when using OAuth authentication
  ```

To import composable-studio, authenticate with username and password (`csdx auth:login -u <email> -p <password>`) — Basic Auth is the only supported path.


#### Removed Import Config Keys (Custom Plugins / Config Files)

If you maintain a custom plugin or tool that reads the import config object, these keys are gone in V2:

| Removed Key | Was Set To |
|---|---|
| `importConfig.branchDir` | was a redundant alias for `contentDir` — V2 uses `contentDir` directly |
| `importConfig.contentVersion` | JS/TS module routing number used for internal module routing |

Use `importConfig.contentDir` directly in V2.

If your external config JSON uses `modules["asset-management"]`, V2 renames it to `modules["cs-assets"]` internally and logs a deprecation warning. Update your config files to use `"cs-assets"` to suppress the warning.

---

### cm:stacks:import-setup


#### Alias Removed

The short alias `cm:import-setup` is gone. Only the full command name works in V2.

```bash
# V1 (fails in V2)
csdx cm:import-setup --stack-api-key blt123

# V2
csdx cm:stacks:import-setup --stack-api-key blt123
```

#### `-B` Short Char Removed

```bash
# V1
csdx cm:stacks:import-setup -B main

# V2
csdx cm:stacks:import-setup --branch main
```

---

### cm:stacks:bulk-entries

**Replaces (all removed in V2):** `cm:entries:publish`, `cm:entries:publish-modified`, `cm:entries:publish-only-unpublished`, `cm:entries:publish-non-localized-fields`, `cm:entries:unpublish`, `cm:entries:update-and-publish`, `cm:stacks:publish` (entries), `cm:stacks:unpublish` (entries), `cm:stacks:publish-revert`

> **This is the highest-effort migration in V2.** The entire `@contentstack/cli-cm-bulk-publish` plugin (14 commands) is replaced by `@contentstack/cli-bulk-operations`. Every bulk publish script must be rewritten.

#### V1 → V2 Command Mapping

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
| `csdx cm:stacks:publish-configure` | **NO EQUIVALENT — REMOVED** |
| `csdx cm:stacks:publish-clear-logs` | **NO EQUIVALENT — REMOVED** |

**`--filter` valid values:** `draft`, `modified`, `unpublished`, `non-localized` (passing any other value causes an immediate error).

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

#### Cross-Publish Migration (`cm:bulk-publish:cross-publish` → `--source-alias`)

V1 accepted an inline `--delivery-token` flag. V2 requires a stored delivery token alias. One-time setup:

```bash
# Step 1 — store delivery token as an alias (one-time)
csdx auth:tokens:add \
  -a staging-delivery \
  --delivery \
  --token bltABC \
  --stack-api-key blt123 \
  --environment staging

# Step 2 — use alias in bulk-entries
csdx cm:stacks:bulk-entries \
  --operation publish \
  --source-env staging \
  --source-alias staging-delivery \
  --content-types blog article \
  --environments prod \
  --locales en-us \
  -k blt123
```

#### `--api-version` Flag Removed

`api_version: '3.2'` is now hardcoded on every publish/unpublish call. The `--api-version` flag is removed. Passing it fails immediately:

```
ERROR: Nonexistent flag: --api-version
```

Remove `--api-version` from all bulk publish scripts. If you use the legacy rich text editor in your content types, test publish behavior in a staging stack before cutting over.

---

### cm:stacks:bulk-assets

**Replaces (all removed in V2):** `cm:assets:publish`, `cm:assets:unpublish`, `cm:stacks:publish` (assets), `cm:stacks:unpublish` (assets)

#### V1 → V2 Command Mapping

| V1 Command (REMOVED) | V2 Replacement |
|---|---|
| `csdx cm:assets:publish` | `csdx cm:stacks:bulk-assets --operation publish` |
| `csdx cm:assets:unpublish` | `csdx cm:stacks:bulk-assets --operation unpublish` |

```bash
csdx cm:stacks:bulk-assets --operation publish \
  --environments prod \
  --locales en-us \
  --stack-api-key bltXXX \
  --alias myalias
```

#### New: CS Assets Bulk Delete and Move

V2 adds two new operation types to `cm:stacks:bulk-assets` targeting the CS Assets API — separate from the CMS publish pipeline:

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

**Requirements:** `csAssetsUrl` must be configured in region settings (`csdx config:set:region --cs-assets <url>`). CMS flags (`--stack-api-key`, `--alias`, `--environments`, `--locales`, `--branch`) cannot be combined with CS Assets flags. `--locale` required for `delete`, not allowed for `move`.

> **Where to find `--space-uid` and `--org-uid`:** In the Contentstack UI, go to **Organization > Contentstack Assets > Settings**. The Space UID and Organization UID are shown there. You can also retrieve them from the CS Assets API.

`--api-version` flag removed; `api_version: '3.2'` is hardcoded on all calls (same as bulk-entries).

---

### cm:stacks:bulk-taxonomies

New command for bulk publishing or unpublishing taxonomy terms. `api_version: '3.2'` is hardcoded on all calls.

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

---

### cm:stacks:seed


#### Alias Removed

```bash
# V1 (fails in V2)
csdx cm:seed --repo contentstack/kickstart-stack-seed

# V2
csdx cm:stacks:seed --repo contentstack/kickstart-stack-seed
```

#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `--stack` / `-s` | `--stack-api-key` (no short char) |
| `-r` (repo) | `--repo` (long form only) |
| `-o` (org) | `--org` (long form only) |

```bash
# V1
csdx cm:stacks:seed -s blt123 -r contentstack/kickstart-stack-seed -o orgUid

# V2
csdx cm:stacks:seed --stack-api-key blt123 --repo contentstack/kickstart-stack-seed --org orgUid
```

#### Interactive Mode Changed — GitHub API Replaced by Curated List

When running `csdx cm:stacks:seed` without `--repo`, V1 queried the GitHub API for all Contentstack repos. V2 shows a fixed curated list of 3 repos:

1. Kickstart stack seed (`contentstack/kickstart-stack-seed`)
2. Kickstart Veda (`contentstack/kickstart-veda-seed`)
3. Compass starter stack (`contentstack/compass-starter-stack`)

> **Note:** `contentstack/stack-starter-app` was removed from the curated list. If you need it, pass it directly via `--repo contentstack/stack-starter-app`.

If you need a repo not on this list, use `--repo owner/repo` directly.

---

### cm:bootstrap


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `--appName` / `-a` | `--app-name` |
| `--directory` / `-d` | `--project-dir` |
| `--appType` / `-s` | *(removed — no replacement needed; app type is hardcoded internally)* |

> **Note:** V1 had a short flag collision — both `--appName` and `--alias` claimed `-a`. V2 resolves this: `--app-name` has no short char, and `-a` exclusively means `--alias`. Any script that used `-a` for app name must switch to `--app-name` (long form only).

```bash
# V1
csdx cm:bootstrap --appName reactjs --directory ./myapp --appType sampleapp

# V2
csdx cm:bootstrap --app-name compass-app --project-dir ./myapp
```

#### 13 App Configs Removed

The following `--app-name` values are no longer valid in V2. Passing any of them throws `CLI_BOOTSTRAP_INVALID_APP_NAME`.

**Removed sample apps (4) — were in `sampleApps` interactive list:**

| `--app-name` | GitHub Source | Stack Seed |
|---|---|---|
| `reactjs` | `contentstack/contentstack-reactjs-universal-sample-app` | `contentstack/stack-contentstack-reactjs-universal-sample-app` |
| `nextjs` | `contentstack/contentstack-nextjs-react-universal-demo` | `contentstack/stack-contentstack-nextjs-react-universal-demo` |
| `gatsby` | `contentstack/gatsby-starter-contentstack` | `contentstack/stack-gatsby-starter-contentstack` |
| `angular` | `contentstack/contentstack-angular-modularblock-example` | `contentstack/stack-contentstack-angular-modularblock-example` |

**Removed starter apps (8) — were in `starterApps` interactive list:**

| `--app-name` | GitHub Source | Stack Seed |
|---|---|---|
| `reactjs-starter` | `contentstack/contentstack-react-starter-app` | `contentstack/stack-starter-app` |
| `nextjs-starter` | `contentstack/contentstack-nextjs-starter-app` | `contentstack/stack-starter-app` |
| `gatsby-starter` | `contentstack/contentstack-gatsby-starter-app` | `contentstack/stack-starter-app` |
| `angular-starter` | `contentstack/contentstack-angular-starter` | `contentstack/stack-starter-app` |
| `nuxt-starter` | `contentstack/contentstack-nuxtjs-starter-app` | `contentstack/stack-starter-app` |
| `vue-starter` | `contentstack/contentstack-vuejs-starter-app` | `contentstack/stack-starter-app` |
| `stencil-starter` | `contentstack/contentstack-stencil-starter-app` | `contentstack/stack-starter-app` |
| `nuxt3-starter` | `contentstack/contentstack-nuxt3-starter-app` | `contentstack/stack-starter-app` |

**Removed hidden config entry (1) — never shown interactively, passable via `--app-name`:**

| `--app-name` | GitHub Source |
|---|---|
| `nuxtjs-disabled` | `contentstack/contentstack-nuxtjs-vue-universal-demo` |

#### Valid App Names in V2 (8)

These apps existed in V1 `starterApps` and carry over to V2 unchanged:

| `--app-name` | Display Name | GitHub Source | Stack Seed |
|---|---|---|---|
| `compass-app` | Compass App | `contentstack/compass-starter-app` | `contentstack/compass-starter-stack` |
| `kickstart-next` | Kickstart Next.js | `contentstack/kickstart-next` | `contentstack/kickstart-stack-seed` |
| `kickstart-next-ssr` | Kickstart Next.js SSR | `contentstack/kickstart-next-ssr` | `contentstack/kickstart-stack-seed` |
| `kickstart-next-ssg` | Kickstart Next.js SSG | `contentstack/kickstart-next-ssg` | `contentstack/kickstart-stack-seed` |
| `kickstart-next-graphql` | Kickstart Next.js GraphQL | `contentstack/kickstart-next-graphql` | `contentstack/kickstart-stack-seed` |
| `kickstart-next-middleware` | Kickstart Next.js Middleware | `contentstack/kickstart-next-middleware` | `contentstack/kickstart-stack-seed` |
| `kickstart-nuxt` | Kickstart NuxtJS | `contentstack/kickstart-nuxt` | `contentstack/kickstart-stack-seed` |
| `kickstart-nuxt-ssr` | Kickstart NuxtJS SSR | `contentstack/kickstart-nuxt-ssr` | `contentstack/kickstart-stack-seed` |

---

### cm:stacks:audit


#### Short Aliases Removed

Both commands had short aliases stripped:

| Removed Alias | Canonical V2 Command |
|---|---|
| `audit` | `cm:stacks:audit` |
| `audit:fix` | `cm:stacks:audit:fix` |

```bash
# V1 (fails in V2)
csdx audit
csdx audit:fix

# V2
csdx cm:stacks:audit
csdx cm:stacks:audit:fix
```

#### Audit Reads Per-UID Files — V1 Exports Produce Silent Empty Results

`cm:stacks:audit` now uses `readContentTypeSchemas` and `readGlobalFieldSchemas` (the same utilities as V2 import) to load content type and global field schemas from the `--report-path` directory. These utilities read individual `<uid>.json` files and **explicitly ignore `schema.json` and `globalfields.json`**.

If you run audit against a V1 export directory, content types will load correctly (V1 export writes per-UID files). **Global fields will return zero results** — a false clean — because V1 export writes only `globalfields.json` with no per-UID files.

**Migration:** Re-export global fields with V2 before auditing. A conversion script will be provided for cases where re-export is not possible.

---

### cm:stacks:migration


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `-B` | `--branch` |
| `-A` | `--alias` |
| `-n` | `--file-path` |
| `--api-key` | `--stack-api-key` |
| `--authtoken` | *(removed — use `csdx auth:login` then `--alias`)* |
| `--management-token-alias` | `--alias` |
| `--filePath` | `--file-path` |
| `--multi` | `--multiple` |

```bash
# V1
csdx cm:migration -B feature-branch -n ./migrate.js

# V2
csdx cm:stacks:migration --branch feature-branch --file-path ./migrate.js
```

---

### cm:stacks:validate-regex


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `-c` | `--contentType` |
| `-f` | `--filePath` |
| `-g` | `--globalField` |

```bash
# V1
csdx cm:stacks:validate-regex -c blog -f ./regex.json -g header

# V2
csdx cm:stacks:validate-regex --contentType blog --filePath ./regex.json --globalField header
```

#### Output Format

The results table and `results.csv` file use the same column order in both V1 and V2: `Module`, `Title`, `UID`, `Invalid Regex Count`. If you parse CSV output by header name, no changes are needed.

---

### auth:tokens


#### Behavior Changed — Now a Help Dispatcher

`csdx auth:tokens` no longer lists your tokens. In V2 it displays sub-command help.

**Silent failure risk:** If your script runs `csdx auth:tokens` to get a token table and parses stdout, it will silently receive help text instead of a table. No error code is raised.

```bash
# V1
csdx auth:tokens          # listed tokens

# V2
csdx auth:tokens:list     # lists tokens
```

The `tokens` short alias is also removed. `csdx tokens` fails with "command not found".

---

### auth:tokens:add


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `-d` | `--delivery` (long form only) |
| `-m` | `--management` (long form only) |
| `-t` | `--token` (long form only) |
| `--api-key` (hidden) | Removed entirely |
| `-f / --force` (hidden) | Use `-y / --yes` |

```bash
# V1
csdx auth:tokens:add -a myalias -d -t bltABC -k blt123

# V2
csdx auth:tokens:add -a myalias --delivery --token bltABC --stack-api-key blt123
```

---

### auth:tokens:remove


#### `-i / --ignore` Flag Removed

V1: `-i / --ignore` caused the command to succeed silently even if the alias did not exist.

V2: Flag removed. If the alias does not exist, V2 prints a yellow warning and exits 0 (no error thrown). Scripts that relied on a non-zero exit when `--ignore` was not passed should note this change.

```bash
# V1
csdx auth:tokens:remove -a myalias -i    # silently succeeded even if not found

# V2
csdx auth:tokens:remove -a myalias       # prints "No token found with alias 'myalias'." (yellow) and exits 0
```

---

### auth:logout


#### `-f / --force` Hidden Flag Removed

```bash
# V1 (hidden but functional)
csdx auth:logout -f
csdx auth:logout --force

# V2 — passes "Unexpected argument" error
# Use:
csdx auth:logout -y
csdx auth:logout --yes
```

---

### config:set:region


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `-d` | `--cda` |
| `-m` | `--cma` |
| `-n` | `--name` |

```bash
# V1
csdx config:set:region -d https://cdn.example.com -m https://api.example.com -n MyRegion

# V2
csdx config:set:region --cda https://cdn.example.com --cma https://api.example.com --name MyRegion
```

#### New: `--cs-assets` Flag

V2 adds a `--cs-assets` flag for specifying the Contentstack Assets API URL when configuring a custom region:

```bash
csdx config:set:region \
  --cma https://custom.cma.example.com \
  --cda https://custom.cda.example.com \
  --ui-host https://custom.ui.example.com \
  --name MyRegion \
  --cs-assets https://custom.am-api.example.com
```

When `--cs-assets` is omitted, V2 derives the CS Assets URL from the CMA URL automatically.

`config:get:region` now also shows `Contentstack Assets URL` in its output.

---

### config:set:log


#### Config Key Changed — V1 Settings Lost on Upgrade

V1 stored the console log preference as `log["show-console-logs"]` (hyphenated). V2 stores it as `log["showConsoleLogs"]` (camelCase). The two formats are not compatible.

**After upgrading, your V1 console log configuration is silently ignored.** Progress bars are the default. If your CI needs console log output, re-run:

```bash
csdx config:set:log --show-console-logs
```

To explicitly switch back to progress bars (V2 default):
```bash
csdx config:set:log --no-show-console-logs
```

---


### config:set:early-access-header

**Documentation fix — no behavioral change.**

V1 had `--header` and `--header-alias` descriptions swapped:

| Flag | V1 description (WRONG) | V2 description (CORRECT) |
|---|---|---|
| `--header-alias` | "Provide the Early Access header value" | "Provide a name (alias) for this Early Access header" |
| `--header` | "Provide the Early Access header alias name" | "Provide the Early Access header value" |

The actual behavior was always: `--header-alias` = the alias name, `--header` = the header value. If you were following V1's incorrect help text and passing values in the wrong order, correct your scripts:

```bash
# Correct usage (was correct in V1 behavior, now also correct in V1 documentation)
csdx config:set:early-access-header --header-alias myheader --header x-header-value
```

---

### tsgen

`tsgen` generates TypeScript type definitions from your stack's content types. If you use the Contentstack TypeScript SDK and want type-safe content model access in your codebase, you use this command. See the [tsgen plugin docs](https://www.contentstack.com/docs/headless-cms/tsgen-plugin) for full usage.

#### `--token-alias` Renamed to `--alias` + Short Chars Removed

| Change | Details |
|---|---|
| `--token-alias` → `--alias` | Full flag name changed — `--token-alias` now produces "Nonexistent flag:" |
| `-o` removed | Was short for `--output` |
| `-p` removed | Was short for `--prefix` |
| `-d` removed | Was short for `--doc` |
| `-a` (short for alias) | **KEPT** on the renamed `--alias` flag |

```bash
# V1
csdx tsgen --token-alias myalias -o ./types -p CS_ -d

# V2
csdx tsgen --alias myalias --output ./types --prefix CS_ --doc
# or use -a for alias:
csdx tsgen -a myalias --output ./types --prefix CS_ --doc
```

---

### app:create


#### `-n` Short Char Removed

```bash
# V1
csdx app:create -n my-app

# V2
csdx app:create --name my-app
```

---

### migrate:convert


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `-o` | `--output` |
| `-m` | `--master-locale` |
| `-a` | `--affix` |

```bash
# V1
csdx migrate:convert -o ./output -m en-us -a v2_

# V2
csdx migrate:convert --output ./output --master-locale en-us --affix v2_
```

---

### migrate:export


#### `-o` Short Char Removed

```bash
# V1
csdx migrate:export -o ./output

# V2
csdx migrate:export --output ./output
```


---

> **Note on the `content-type:*` namespace:** These commands are a separate plugin (`@contentstack/contentstack-content-type`) that inspects and compares content type schemas. They are distinct from `cm:stacks:*` commands — they do not export or import content; they analyze schema structure. If you use any `content-type:*` commands, the flag changes below apply.

### content-type:audit


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `--stack` / `-s` | `--stack-api-key` / `-k` |
| `--token-alias` / `-a` | `--alias` / `-a` |
| `-c` (content-type) | `--content-type` |

```bash
# V1
csdx content-type:audit --stack blt123 --token-alias myalias -c blog

# V2
csdx content-type:audit --stack-api-key blt123 --alias myalias --content-type blog
```

---

### content-type:compare


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `--stack` / `-s` | `--stack-api-key` / `-k` |
| `--token-alias` / `-a` | `--alias` / `-a` |
| `-c` (content-type) | `--content-type` |
| `-l` (left) | `--left` |
| `-r` (right) | `--right` |

```bash
# V1
csdx content-type:compare --stack blt123 --token-alias myalias -c blog -l v1 -r v2

# V2
csdx content-type:compare --stack-api-key blt123 --alias myalias --content-type blog --left v1 --right v2
```

---

### content-type:compare-remote


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `-o` | `--origin-stack` |
| `-r` | `--remote-stack` |
| `-c` | `--content-type` |

Note: `content-type:compare-remote` did NOT have `--stack` / `--token-alias` flags in V1.

```bash
# V1
csdx content-type:compare-remote -o bltOrigin -r bltRemote -c blog

# V2
csdx content-type:compare-remote --origin-stack bltOrigin --remote-stack bltRemote --content-type blog
```

---

### content-type:details


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `--stack` / `-s` | `--stack-api-key` / `-k` |
| `--token-alias` / `-a` | `--alias` / `-a` |
| `-c` (content-type) | `--content-type` |
| `-p` (path) | `--path` |

```bash
# V1
csdx content-type:details --stack blt123 --token-alias myalias -c blog -p fields.title

# V2
csdx content-type:details --stack-api-key blt123 --alias myalias --content-type blog --path fields.title
```

---

### content-type:diagram


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `--stack` / `-s` | `--stack-api-key` / `-k` |
| `--token-alias` / `-a` | `--alias` / `-a` |
| `-o` (output) | `--output` |
| `-d` (direction) | `--direction` |
| `-t` (type) | `--type` |

```bash
# V1
csdx content-type:diagram --stack blt123 --token-alias myalias -o ./diagram.svg -d LR -t svg

# V2
csdx content-type:diagram --stack-api-key blt123 --alias myalias --output ./diagram.svg --direction LR --type svg
```

---

### content-type:list


#### Removed Flags

| Removed | V2 Replacement |
|---|---|
| `--stack` / `-s` | `--stack-api-key` / `-k` |
| `--token-alias` / `-a` | `--alias` / `-a` |
| `-o` (order) | `--order` |

```bash
# V1
csdx content-type:list --stack blt123 --token-alias myalias -o asc

# V2
csdx content-type:list --stack-api-key blt123 --alias myalias --order asc
```


## 5. New Features

### CS Assets (Asset Management 2.0)

V2 adds full support for Contentstack's new CS Assets system (AM 2.0). Export, import, and import-setup automatically detect and handle CS Assets if your stack has linked workspaces.

**Export:** If your stack has linked workspaces configured in Contentstack Assets settings, export writes CS Assets data to a `spaces/` directory alongside the standard `assets/` directory. If not configured, export falls back to standard asset export automatically:
```
export/
  assets/         ← CMS assets (unchanged)
  spaces/         ← NEW: CS Assets
    <space-id>/workspaces/
    <space-id>/asset_types/
    <space-id>/assets/
    <space-id>/folders/
```

**Import:** Detects `spaces/` directory and imports CS Assets automatically.

**Import-setup:** Detects CS Assets exports and generates identity UID/URL mapper files.

**New bulk operations:** `cm:stacks:bulk-assets --operation delete` and `--operation move` for CS Assets (see new flags `--space-uid`, `--org-uid`, `--workspace`, `--asset-uids-file`, `--target-folder-uid`).

### Taxonomy Publishing

New in V2 across export, import, and bulk operations:

- **Export** captures `publish_details` per locale for each taxonomy
- **Import** re-publishes taxonomies after import by default. To skip publishing (for example, if you want to review entries before publishing):
  ```bash
  csdx cm:stacks:import --skip-taxonomy-publish -d ./export -k bltXXX
  ```
- **`cm:stacks:bulk-taxonomies`** for bulk taxonomy publish operations

### Global Fields Per-File Export

Each global field now exports as its own `<uid>.json` file (same format as content types). See [cm:stacks:export section](#cmstacksexport) for the full file structure change.

### Visual Progress System

All major operations now show visual progress bars and a summary table at end of run. See [config:set:log](#configsetlog) to restore console log output for CI environments.


## 6. Pre-Upgrade Checklist

Items are ordered by risk. Complete top sections before lower ones.

### 🔴 Critical — Do These First

- [ ] Test the entire upgrade in a non-production environment before touching production.
- [ ] **Your saved tokens carry over automatically** — management tokens stored with `csdx auth:tokens:add` are available immediately after upgrading. No re-authentication required.

### 🔴 High-Risk Script Changes

- [ ] Add explicit `--branch` flag to **all** `cm:stacks:export` calls for non-main branches — V2 only exports `main` when `--branch` is omitted
- [ ] Use a **separate `--data-dir` per branch** — V2 output is always flat (no `<branch-uid>/` subfolder); exporting two branches to the same directory silently overwrites the first
- [ ] Rewrite all `cm:entries:publish*`, `cm:assets:publish*`, `cm:bulk-publish:*`, `cm:stacks:publish`, `cm:stacks:unpublish` → `cm:stacks:bulk-entries` / `cm:stacks:bulk-assets` commands
- [ ] Verify publish behavior in a staging stack — all bulk publish/unpublish calls now use `api_version: '3.2'` and `--api-version` flag is removed
- [ ] Remove checks for `export-info.json` or `content_types/schema.json` in post-export tooling — these files are not written by V2
- [ ] Update tooling that reads `global_fields/globalfields.json` → iterate per-UID JSON files instead

### 🟡 CI / Pipeline Audit

- [ ] Verify your CI does not parse stdout for success signals — output format changed (progress bars by default)
- [ ] Run `csdx config:set:log --show-console-logs` after upgrading if your CI parses console output (V1 log setting is silently dropped)

### 🟡 Script Audit — Command Renames

- [ ] Replace `csdx cm:export` → `csdx cm:stacks:export`
- [ ] Replace `csdx cm:import` → `csdx cm:stacks:import`
- [ ] Replace `csdx cm:import-setup` → `csdx cm:stacks:import-setup`
- [ ] Replace `csdx cm:seed` → `csdx cm:stacks:seed`
- [ ] Replace `csdx tokens` → `csdx auth:tokens:list`
- [ ] Replace `csdx auth:tokens` (when used as list command) → `csdx auth:tokens:list`
- [ ] Replace `csdx audit` → `csdx cm:stacks:audit`

### 🟡 Script Audit — Flag Changes

- [ ] Remove `--stack-uid` / `-s` everywhere → `--stack-api-key`
- [ ] Remove `--data` → `--data-dir`
- [ ] Remove `--management-token-alias` → `--alias`
- [ ] Remove `--auth-token` / `-A` → use `csdx auth:login` then `--alias`
- [ ] Remove `--skip-app-recreation` from all import scripts (no replacement)
- [ ] Remove `--token-alias` on `tsgen` → `--alias`
- [ ] Audit scripts using removed short flags on export/import commands: `-m`/`-t`/`-B`/`-b`/`-A` (→ long form only). See each command section for the full list.
- [ ] Update `cm:bootstrap` flags: `--appName` → `--app-name`, `--directory` → `--project-dir`
- [ ] Remove bootstrap app names that no longer exist: `reactjs`, `nextjs`, `gatsby`, `angular`, `*-starter` variants
- [ ] Update `content-type:*` commands: remove `--stack`/`-s`, `--token-alias`/`-a`, and all listed short chars
- [ ] Replace `csdx auth:logout -f`/`--force` → `csdx auth:logout -y`/`--yes`

### 🟢 Plugin Management

- [ ] Install `launch` plugin separately if you use `launch:*` commands: `csdx plugins:install @contentstack/cli-launch`
- [ ] Install `migrate-rte` plugin separately if you use `cm:entries:migrate-html-rte`: `csdx plugins:install @contentstack/cli-cm-migrate-rte`
- [ ] If you use CS Assets, verify your stack has linked workspaces configured in Contentstack Assets settings — otherwise export falls back to standard asset export

### 🟢 Custom Plugins (Plugin Authors Only)

- [ ] Update `engines.node` to `>=22.0.0` in your plugin's `package.json`

### Test Run

- [ ] Run a full export + import cycle on a non-production stack before cutting over
- [ ] Verify branch exports are capturing the correct branches explicitly
- [ ] If you use CS Assets, verify your stack has linked workspaces configured — otherwise export falls back to standard asset export automatically (no error)
- [ ] If you use bulk publish/unpublish, run a test publish in staging — all calls now use `api_version: '3.2'`

---

## 7. Rollback Plan

If something breaks after upgrading:

1. Restore from your pre-upgrade stack export (you made one in "Before You Start" above)
2. Downgrade the CLI: `npm install -g @contentstack/cli@1.x`
3. Your tokens are still available — both V1 and V2 read from the same token store
