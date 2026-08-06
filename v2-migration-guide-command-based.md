---

## sidebar: cliSidebar
title: Migrate from Contentstack CLI V1 to V2
description: Step-by-step guide to upgrading from Contentstack CLI V1 to V2, covering breaking changes, removed flags, command replacements, and a pre-upgrade checklist.
url: /developers/cli/v2-migration-guide
version: 2.0.0

---

# Migrate from Contentstack CLI V1 to V2

## Overview

This guide applies if you are upgrading Contentstack CLI from version 1.x.x to 2.x.x.

V2 requires Node.js 22+, routes all publish operations through the New Release Pipeline (NRP), removes several flags and command aliases with no runtime warning, and changes the on-disk format of exports (per-UID files replace aggregate JSON files like `schema.json` and `globalfields.json`).

You get a flag-by-flag mapping for every removed command, the export and import file-format changes to check in your tooling, a pre-upgrade checklist, and fixes for the failure modes in this upgrade that produce no error output (see [Troubleshooting](#troubleshooting)).

This guide covers CLI-only changes. It does not cover Contentstack platform or API changes.

## Prerequisites



### Node.js 22+

V2 requires Node.js `>=22.0.0`.

If you need to upgrade, run:

```bash
nvm install 22
nvm alias default 22   # makes 22 the permanent default, not just for this shell session
nvm use 22
```

**Note:** On Node 18 or 20, the `npm install -g @contentstack/cli` completes with `EBADENGINE` warnings and appears to succeed, but the CLI fails at runtime. Upgrade Node first, then install.

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
csdx --version
```

This should show `2.0.0`.

**Warning:** `npm install -g` replaces the `csdx` binary in place. A roughly **30-second** window exists during installation where `csdx` is unavailable. For continuous integration (CI) pipelines, run the install and the CLI commands in the same pipeline step. Do not rely on a pre-installed binary from a prior step.

On a 2.x beta, upgrade directly to 2.0.0 with `npm install -g @contentstack/cli@2.0.0`.

> **Note:** Verify Node 22 in Every Environment
>
> Run this check on every environment where the CLI runs, including CI and continuous delivery (CD) pipelines, not only your local machine:
>
> - Dev machines
> - CI/CD runners
> - Docker base images (pin to the Node 22 LTS tag)



## Type Mapping Reference

The table below lists every flag rename and removed short character across every command. Rows that repeat the same V1 and V2 flag name had only their short character removed. Rows marked "use OAuth" mean you authenticate with Open Authorization (OAuth) login (`csdx auth:login --oauth`) instead of the removed flag.


| Command                       | V1 Flag                    | V1 Short | V2 Flag                              | V2 Short |
| ----------------------------- | -------------------------- | -------- | ------------------------------------ | -------- |
| `cm:stacks:export`            | `--stack-uid`              | `-s`     | `--stack-api-key`                    | `-k`     |
|                               | `--data`                   | None     | `--data-dir`                         | None     |
|                               | `--management-token-alias` | None     | `--alias`                            | `-a`     |
|                               | `--auth-token`             | `-A`     | *(removed, use OAuth +* `--alias`*)* | None     |
|                               | `--module`                 | `-m`     | `--module`                           | None     |
|                               | `--content-types`          | `-t`     | `--content-types`                    | None     |
|                               | `--branch`                 | `-B`     | `--branch`                           | None     |
| `cm:stacks:import`            | `--stack-uid`              | `-s`     | `--stack-api-key`                    | `-k`     |
|                               | `--data`                   | None     | `--data-dir`                         | None     |
|                               | `--management-token-alias` | None     | `--alias`                            | `-a`     |
|                               | `--auth-token`             | `-A`     | *(removed, use OAuth +* `--alias`*)* | None     |
|                               | `--module`                 | `-m`     | `--module`                           | None     |
|                               | `--backup-dir`             | `-b`     | `--backup-dir`                       | None     |
|                               | `--branch`                 | `-B`     | `--branch`                           | None     |
|                               | `--skip-app-recreation`    | None     | *(removed, no replacement)*          | None     |
| `cm:stacks:import-setup`      | `--branch`                 | `-B`     | `--branch`                           | None     |
| `cm:stacks:seed`              | `--stack`                  | `-s`     | `--stack-api-key`                    | None     |
|                               | `--repo`                   | `-r`     | `--repo`                             | None     |
|                               | `--org`                    | `-o`     | `--org`                              | None     |
| `cm:stacks:migration`         | `--branch`                 | `-B`     | `--branch`                           | None     |
|                               | `--authtoken`              | `-A`     | `--authtoken`                        | None     |
|                               | `--filePath`               | `-n`     | `--file-path`                        | None     |
| `cm:stacks:validate-regex`    | `--contentType`            | `-c`     | `--contentType`                      | None     |
|                               | `--filePath`               | `-f`     | `--filePath`                         | None     |
|                               | `--globalField`            | `-g`     | `--globalField`                      | None     |
| `cm:bootstrap`                | `--appName`                | `-a`     | `--app-name`                         | None     |
|                               | `--directory`              | `-d`     | `--project-dir`                      | None     |
| `auth:tokens:add`             | `--delivery`               | `-d`     | `--delivery`                         | None     |
|                               | `--management`             | `-m`     | `--management`                       | None     |
|                               | `--token`                  | `-t`     | `--token`                            | None     |
|                               | `--api-key`                | None     | *(removed)*                          | None     |
|                               | `--force`                  | `-f`     | `--yes`                              | `-y`     |
| `auth:tokens:remove`          | `--ignore`                 | `-i`     | *(removed)*                          | None     |
| `auth:logout`                 | `--force`                  | `-f`     | `--yes`                              | `-y`     |
| `config:set:region`           | `--cda`                    | `-d`     | `--cda`                              | None     |
|                               | `--cma`                    | `-m`     | `--cma`                              | None     |
|                               | `--name`                   | `-n`     | `--name`                             | None     |
| `tsgen`                       | `--token-alias`            | None     | `--alias`                            | `-a`     |
|                               | `--output`                 | `-o`     | `--output`                           | None     |
|                               | `--prefix`                 | `-p`     | `--prefix`                           | None     |
|                               | `--doc`                    | `-d`     | `--doc`                              | None     |
| `app:create`                  | `--name`                   | `-n`     | `--name`                             | None     |
| `migrate:convert`             | `--output`                 | `-o`     | `--output`                           | None     |
|                               | `--master-locale`          | `-m`     | `--master-locale`                    | None     |
|                               | `--affix`                  | `-a`     | `--affix`                            | None     |
| `migrate:export`              | `--output`                 | `-o`     | `--output`                           | None     |
| `content-type:audit`          | `--stack`                  | `-s`     | `--stack-api-key`                    | `-k`     |
|                               | `--token-alias`            | `-a`     | `--alias`                            | `-a`     |
|                               | `--content-type`           | `-c`     | `--content-type`                     | None     |
| `content-type:compare`        | `--stack`                  | `-s`     | `--stack-api-key`                    | `-k`     |
|                               | `--token-alias`            | `-a`     | `--alias`                            | `-a`     |
|                               | `--content-type`           | `-c`     | `--content-type`                     | None     |
|                               | `--left`                   | `-l`     | `--left`                             | None     |
|                               | `--right`                  | `-r`     | `--right`                            | None     |
| `content-type:compare-remote` | `--origin-stack`           | `-o`     | `--origin-stack`                     | None     |
|                               | `--remote-stack`           | `-r`     | `--remote-stack`                     | None     |
|                               | `--content-type`           | `-c`     | `--content-type`                     | None     |
| `content-type:details`        | `--stack`                  | `-s`     | `--stack-api-key`                    | `-k`     |
|                               | `--token-alias`            | `-a`     | `--alias`                            | `-a`     |
|                               | `--content-type`           | `-c`     | `--content-type`                     | None     |
|                               | `--path`                   | `-p`     | `--path`                             | None     |
| `content-type:diagram`        | `--stack`                  | `-s`     | `--stack-api-key`                    | `-k`     |
|                               | `--token-alias`            | `-a`     | `--alias`                            | `-a`     |
|                               | `--output`                 | `-o`     | `--output`                           | None     |
|                               | `--direction`              | `-d`     | `--direction`                        | None     |
|                               | `--type`                   | `-t`     | `--type`                             | None     |
| `content-type:list`           | `--stack`                  | `-s`     | `--stack-api-key`                    | `-k`     |
|                               | `--token-alias`            | `-a`     | `--alias`                            | `-a`     |
|                               | `--order`                  | `-o`     | `--order`                            | None     |




## Global CLI Behavior Changes



### Default Output: Progress Bars Replace Console Logs


| Behavior           | V1                                                      | V2                                          |
| ------------------ | ------------------------------------------------------- | ------------------------------------------- |
| Output format      | Text printed line-by-line to `stdout` as operations run | Visual progress bars render in the terminal |
| Console log output | Printed live to `stdout`, parseable by scripts and CI   | Suppressed by default                       |
| End-of-run output  | Accumulated text output, no separate summary            | Shows only a summary and a log file path    |


**Effect:** Any script or CI pipeline that parses `stdout` for success or failure signals receives different output. V2 does not exit non-zero or throw because of this. Whether a log line still reaches the console depends on its level:

| Log level                  | Reaches the console when progress bars are active |
| --------------------------- | --------------------------------------------------- |
| `error`, `warn`             | Yes, always                                          |
| `info`, `success`, `debug`  | No, suppressed                                       |

A script that parses `stdout` for a suppressed line finds nothing, not an error.

**CI environments:** V2 does not auto-detect non-interactive (non-TTY) environments. Progress bars render regardless of whether `stdout` is a terminal, which produces escape code characters in CI logs. Restore plain text output with:

```
csdx config:set:log --show-console-logs
```

See [config:set:log](#configsetlog) for the full flag reference.

**Log file location:** V2 writes logs to a `logs/` directory in whichever folder you ran the CLI from (for example, `./logs/`). Set the `CS_CLI_LOG_PATH` environment variable or run `csdx config:set:log --path <dir>` to redirect logs.

### Deprecated Flags Removed

V2 raises no runtime warning when a deprecated flag stops working, unlike V1. Audit your scripts before upgrading.

**Before (V1):**

```bash
csdx cm:stacks:export --stack-uid blt123
```

This prints a deprecation warning, then runs.

**After (V2):**

```bash
csdx cm:stacks:export --stack-uid blt123
```

```
ERROR: Nonexistent flag: --stack-uid
```

The same applies to every other deprecated flag (`--data`, `-s`, `-B`, and similar).

### Short Flags Cleaned Up

V2 systematically removes single-character short flags that conflicted with global CLI flags or were ambiguous across commands. In every case the long form still works. See each command section for the specific characters removed.

### All Publish Operations Now Use NRP

In V2, all publish operations, including entry, asset, and taxonomy publishes triggered during import and all bulk publish and unpublish commands, go through the New Release Pipeline (NRP) API. V1 did not use NRP for import, and for bulk publish, V1 exposed an `--api-version` flag that let you control this.

**What changed:**


| Command                           | V1                                         | V2                                                    |
| --------------------------------- | ------------------------------------------ | ----------------------------------------------------- |
| `cm:stacks:import` (auto-publish) | Did not use NRP                            | Uses NRP for all entry, asset, and taxonomy publishes |
| `cm:stacks:bulk-entries`          | `--api-version` flag let you opt in or out | Always uses NRP, `--api-version` flag removed         |
| `cm:stacks:bulk-assets`           | `--api-version` flag let you opt in or out | Always uses NRP, `--api-version` flag removed         |


**Impact:** Your stack must have NRP enabled. V2 has no flag to run publish operations without NRP.

> **Note:** Passing `--api-version` to `cm:stacks:bulk-entries` or `cm:stacks:bulk-assets` in V2 causes an immediate error: `ERROR: Nonexistent flag: --api-version`.



### Command Aliases Removed

V2 removes several short-form aliases that V1 used:


| Removed Alias          | V2 Replacement                |
| ---------------------- | ----------------------------- |
| `csdx cm:export`       | `csdx cm:stacks:export`       |
| `csdx cm:import`       | `csdx cm:stacks:import`       |
| `csdx cm:import-setup` | `csdx cm:stacks:import-setup` |
| `csdx tokens`          | `csdx auth:tokens:list`       |
| `csdx cm:seed`         | `csdx cm:stacks:seed`         |
| `csdx audit`           | `csdx cm:stacks:audit`        |
| `csdx cm:migration`    | `csdx cm:stacks:migration`    |




## Plugin Changes



### launch Plugin: Now Opt-In

V2 no longer bundles `launch:*` commands in the CLI. When you run any `launch:*` command, V2 prints a guided error with the install instruction and exits with code 127.

**Affected commands:** `launch`, `launch:deployments`, `launch:environments`, `launch:functions`, `launch:logs`, `launch:open`, `launch:rollback`

**No prior equivalent required:** these commands existed bundled in V1. V2 keeps the same commands available as an installable plugin.

**Before:** the `launch` plugin ships bundled with the CLI in V1. You need no install step.

**After:**

```bash
csdx plugins:install @contentstack/cli-launch
```



### migrate-rte Plugin: Now Opt-In

V2 no longer bundles `cm:entries:migrate-html-rte` in the CLI. Unlike `launch`, V2 prints no guided error. The shell returns "command not found" with no install suggestion.

**Affected commands:** `cm:entries:migrate-html-rte`

**Before:** the `migrate-rte` plugin ships bundled with the CLI in V1. You need no install step.

**After:**

```bash
csdx plugins:install @contentstack/cli-cm-migrate-rte
```

Docs: [Migrate content from HTML RTE to JSON RTE](https://www.contentstack.com/docs/developers/cli/migrate-content-from-html-rte-to-json-rte)

## Post-Upgrade Behavior



### Tokens and Config Carry Over Automatically

V2 carries over your existing saved tokens (management tokens added with `csdx auth:tokens:add`) automatically. You do not need to re-authenticate after upgrading.

V2 also carries over other stored config (proxy settings, region config) unchanged. The console log setting is the one exception: if you ran `csdx config:set:log --show-console-logs` in V1, re-run it after upgrading. V2 uses a different internal key and silently ignores the V1 setting (see [V1 Console Log Config Silently Ignored After Upgrade](#v1-console-log-config-silently-ignored-after-upgrade)).

### Running V1 and V2 Side by Side

npm global install allows only one active version per Node environment. If you need V1 available during testing, install it under a different nvm Node version. For example:

```bash
nvm use 20 && npm install -g @contentstack/cli@1.x
nvm use 22 && npm install -g @contentstack/cli@2.0.0
```



## Command Reference



### cm:stacks:export



#### Removed Flags


| Removed                    | V2 Replacement                       |
| -------------------------- | ------------------------------------ |
| `--stack-uid` / `-s`       | `--stack-api-key`                    |
| `--data`                   | `--data-dir`                         |
| `--management-token-alias` | `--alias`                            |
| `--auth-token` / `-A`      | Use `csdx auth:login` then `--alias` |
| `-m`                       | `--module` (long form only)          |
| `-t`                       | `--content-types` (long form only)   |
| `-B`                       | `--branch` (long form only)          |


**Before:**

```bash
csdx cm:stacks:export -s blt123 --data ./export -m content_types -t blog article -B main
```

**After:**

```bash
csdx cm:stacks:export --stack-api-key blt123 --data-dir ./export --module content_types --content-types blog article --branch main
```



#### Branch Export Behavior Changed

**V1:** When you omit `--branch`, V1 exports all branches. V1 nests the output under `exportDir/<branch-uid>/...` for each branch.

**V2:** Two independent changes apply:

1. **Default branch:** When you omit `--branch`, V2 exports only the branch named `main`. If no `main` branch exists, the command errors.
2. **No branch subfolder, always:** Even when you specify `--branch`, V2 writes output flat to `exportDir/...` with no `<branch-uid>/` subfolder. This applies regardless of how you select the branch.

**Impact for multi-branch stacks:** You must export each branch to a separate `--data-dir`. If you export two branches to the same directory, the second export overwrites the first. V2 raises no error (see [Branch Export Silently Overwrites Another Branch's Data](#branch-export-silently-overwrites-another-branchs-data)).

1. `branches.json` **removed:** V1 wrote a `branches.json` file to the export root listing all branches at export time. V2 does not write this file, and raises no error. If your import pipeline or post-export tooling reads `branches.json`, remove that step.

Use a separate `--data-dir` per branch:

```bash
csdx cm:stacks:export --branch main       --data-dir ./export-main    --stack-api-key bltXXX
csdx cm:stacks:export --branch feature-x  --data-dir ./export-feature --stack-api-key bltXXX
csdx cm:stacks:export --branch-alias prod --data-dir ./export-prod     --stack-api-key bltXXX
```



#### `export-info.json` No Longer Written

V1 wrote `export-info.json` to the export directory containing `{ "contentVersion": 2, "logsPath": "..." }`. V2 does not write this file. If your pipeline checks for this file or reads `contentVersion` from it, remove that step.

#### `content_types/schema.json` Removed

> **Action required if your tooling reads this file.** A pipeline or script that reads `export/content_types/schema.json` fails on a V2 export with no error message, because the file does not exist in a V2 export.

V1 wrote a combined `content_types/schema.json` with all content type schemas in one array. V2 only writes individual `content_types/<uid>.json` files. V2 drops the aggregate file entirely.

**Before:**

```bash
cat export/content_types/schema.json
```

**After:**

```bash
ls export/content_types/*.json
```



#### Global Fields Format Changed (Per-File)

> **Action required if your tooling reads** `globalfields.json`**.** If any pipeline or script reads `export/global_fields/globalfields.json`, it fails on a V2 export. The file does not exist.

**Before:** V1 stores all global fields in one file.

```
export/global_fields/globalfields.json
```

**After:** V2 stores one file per global field UID.

```
export/global_fields/my_header.json
export/global_fields/my_footer.json
export/global_fields/shared_banner.json
```

Update any tooling that reads `globalfields.json` to iterate per-UID files instead.

#### Module Flag Now Validated, `studio` Renamed

In V2, the CLI validates `--module` against an explicit allowed-values list before any operation starts. Passing an invalid module name fails immediately with a clear error instead of failing mid-operation.

V2 renames V1's `--module studio` value to `--module composable-studio`. The old value fails:

```
Error: Expected --module=studio to be one of: stack, assets, locales, ...composable-studio
```

**Before:**

```bash
csdx cm:stacks:export --module studio
```

**After:**

```bash
csdx cm:stacks:export --module composable-studio
```

V2 also adds two export targets that V1 does not have: `publishing-rules`, `personalize`.

### cm:stacks:import



#### Removed Flags


| Removed                    | V2 Replacement                       |
| -------------------------- | ------------------------------------ |
| `--stack-uid` / `-s`       | `--stack-api-key`                    |
| `--data`                   | `--data-dir`                         |
| `--management-token-alias` | `--alias`                            |
| `--auth-token` / `-A`      | Use `csdx auth:login` then `--alias` |
| `-m`                       | `--module` (long form only)          |
| `-b`                       | `--backup-dir` (long form only)      |
| `-B`                       | `--branch` (long form only)          |
| `--skip-app-recreation`    | **Removed with no replacement**      |


**Before:**

```bash
csdx cm:stacks:import -s blt123 --data ./export -b ./backup -B main
```

**After:**

```bash
csdx cm:stacks:import --stack-api-key blt123 --data-dir ./export --backup-dir ./backup --branch main
```

> **Important:** V2 removes `--skip-app-recreation` completely, with no replacement. Remove it from all import scripts.
>
> `--skip-taxonomy-publish` is a **new, unrelated** flag (see [Taxonomy Publishing](#taxonomy-publishing)). It does not replace `--skip-app-recreation`.

The following flags exist in **both V1 and V2** and require no migration: `--branch-alias`, `--skip-audit`, `--exclude-global-modules`, `--replace-existing`, `--skip-existing`, `--import-webhook-status`, `--personalize-project-name`, `--skip-assets-publish`, `--skip-entries-publish`.

#### Module Flag Validates Against a Strict List

Same as export: V2 validates `--module` on import before any operation begins. `--module studio` fails. Use `--module composable-studio` instead. V2 adds `--module variant-entries` as a new valid value that V1 does not have.

#### Importing a V1 Export: Content Types and Global Fields Silently Skipped

V2's importers use per-UID file readers that explicitly ignore aggregate files. The impact differs between modules because V1 export behavior differs:


| Module        | V1 export writes                                    | V2 importer reads                                | Impact on V1 export                                                |
| ------------- | --------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------ |
| Content types | Individual `<uid>.json` files **and** `schema.json` | Per-UID files only (ignores `schema.json`)       | **No impact**, per-UID files exist, content types import correctly |
| Global fields | `globalfields.json` only (no individual files)      | Per-UID files only (ignores `globalfields.json`) | **Silently skipped**, no per-UID files exist in a V1 export        |


**Impact:** Running V2 import on a V1 export silently skips **all global fields**, with no error and no warning. Global fields complete "successfully" with zero items created. Content types are unaffected.

**Resolution:** Re-export your stack with V2 before importing. This is the correct fix. A separate migration conversion script covers cases where a V2 re-export is not possible.

See [Global Fields Silently Skipped on Import](#global-fields-silently-skipped-on-import) in Troubleshooting for the condensed symptom and resolution.

#### V1 Multi-Branch Export: Auto Branch Detection Removed

V1 import auto-detected the branch by reading `branches.json` at the export root and navigating to the correct `<branch-uid>/` subfolder. V2 removes this `selectBranchFromDirectory` logic.

**Before:**

```bash
csdx cm:stacks:import --data-dir ./my-export
```

V1 reads `branches.json` and auto-navigates to `./my-export/main/`.

**After:**

```bash
csdx cm:stacks:import --data-dir ./my-export/main
```

V2 requires you to specify the branch subfolder explicitly.

If you point V2 import at a V1 multi-branch export root, it attempts to read content files directly from the root (where only `branches.json` lives), finds nothing, and silently produces an empty import. See [V1 Multi-Branch Export Produces an Empty Import](#v1-multi-branch-export-produces-an-empty-import) in Troubleshooting.

#### `composable-studio` Module Requires Basic Auth

V2 skips the `composable-studio` module in two cases:

- **Management token** (`--alias` pointing to a management token):
  ```
  Skipping Studio project import when using management token
  ```
- **OAuth** (`csdx auth:login --oauth`):
  ```
  Skipping Studio project import when using OAuth authentication
  ```

To import `composable-studio`, authenticate with username and password (`csdx auth:login -u <email> -p <password>`). Basic Auth is the only supported path.

#### Removed Import Config Keys (Custom Plugins and Config Files)

If you maintain a custom plugin or tool that reads the import config object, V2 removes these keys:


| Removed Key                   | Was Set To                                                         |
| ----------------------------- | ------------------------------------------------------------------ |
| `importConfig.branchDir`      | a redundant alias for `contentDir`. V2 uses `contentDir` directly. |
| `importConfig.contentVersion` | a JS/TS module routing number used for internal module routing     |


Use `importConfig.contentDir` directly in V2.

If your external config JSON uses `modules["asset-management"]`, V2 renames it to `modules["cs-assets"]` internally and logs a deprecation warning. Update your config files to use `"cs-assets"` to suppress the warning.

### cm:stacks:import-setup



#### Alias Removed

V2 removes the short alias `cm:import-setup`. Only the full command name works in V2.

**Before:**

```bash
csdx cm:import-setup --stack-api-key blt123
```

**After:**

```bash
csdx cm:stacks:import-setup --stack-api-key blt123
```



#### `-B` Short Character Removed

**Before:**

```bash
csdx cm:stacks:import-setup -B main
```

**After:**

```bash
csdx cm:stacks:import-setup --branch main
```



### cm:stacks:bulk-entries

**Replaces (all removed in V2):** `cm:entries:publish`, `cm:entries:publish-modified`, `cm:entries:publish-only-unpublished`, `cm:entries:publish-non-localized-fields`, `cm:entries:unpublish`, `cm:entries:update-and-publish`, `cm:stacks:publish` (entries), `cm:stacks:unpublish` (entries), `cm:stacks:publish-revert`

> V2 replaces all 15 commands in the `@contentstack/cli-cm-bulk-publish` plugin (across `cm:entries:*`, `cm:stacks:*`, `cm:bulk-publish:*`, and `cm:assets:*`) with 3 commands in `@contentstack/cli-bulk-operations`, each driven by an `--operation` flag instead of a dedicated command per action. Rewrite every bulk publish script against the new flag-based interface.



#### V1 to V2 Command Mapping


| V1 Command (REMOVED)                                  | V2 Replacement                                                           |
| ----------------------------------------------------- | ------------------------------------------------------------------------ |
| `csdx cm:entries:publish`                             | `csdx cm:stacks:bulk-entries --operation publish`                        |
| `csdx cm:entries:publish-modified`                    | `csdx cm:stacks:bulk-entries --operation publish --filter modified`      |
| `csdx cm:entries:publish-only-unpublished`            | `csdx cm:stacks:bulk-entries --operation publish --filter unpublished`   |
| `csdx cm:entries:publish-non-localized-fields`        | `csdx cm:stacks:bulk-entries --operation publish --filter non-localized` |
| `csdx cm:entries:unpublish`                           | `csdx cm:stacks:bulk-entries --operation unpublish`                      |
| `csdx cm:entries:update-and-publish`                  | `csdx cm:stacks:bulk-entries --operation publish`                        |
| `csdx cm:stacks:publish` (for entries)                | `csdx cm:stacks:bulk-entries --operation publish`                        |
| `csdx cm:stacks:unpublish` (for entries)              | `csdx cm:stacks:bulk-entries --operation unpublish`                      |
| `csdx cm:bulk-publish:cross-publish`                  | `csdx cm:stacks:bulk-entries --operation publish --source-alias <alias>` |
| `csdx cm:stacks:publish-revert --log-file ./log.json` | `csdx cm:stacks:bulk-entries --revert ./log.json`                        |
| `csdx cm:stacks:publish-configure`                    | **NO EQUIVALENT, REMOVED**                                               |
| `csdx cm:stacks:publish-clear-logs`                   | **NO EQUIVALENT, REMOVED**                                               |


`--filter` **valid values:** `draft`, `modified`, `unpublished`, `non-localized`. Passing any other value causes an immediate error.

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



#### Cross-Publish Migration (`cm:bulk-publish:cross-publish` to `--source-alias`)

**Before:** V1 accepts an inline `--delivery-token` flag.

**After:** V2 requires a stored delivery token alias. Complete this one-time setup:

1. Store the delivery token as an alias.
2. Use the alias in `cm:stacks:bulk-entries`.

```bash
csdx auth:tokens:add \
  -a staging-delivery \
  --delivery \
  --token bltABC \
  --stack-api-key blt123 \
  --environment staging

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

V2 hardcodes `api_version: '3.2'` on every publish and unpublish call. V2 removes the `--api-version` flag. Passing it fails immediately:

```
ERROR: Nonexistent flag: --api-version
```

Remove `--api-version` from all bulk publish scripts. If you use the legacy rich text editor in your content types, test publish behavior in a staging stack before cutting over.

### cm:stacks:bulk-assets

**Replaces (all removed in V2):** `cm:assets:publish`, `cm:assets:unpublish`, `cm:stacks:publish` (assets), `cm:stacks:unpublish` (assets)

#### V1 to V2 Command Mapping


| V1 Command (REMOVED)       | V2 Replacement                                     |
| -------------------------- | -------------------------------------------------- |
| `csdx cm:assets:publish`   | `csdx cm:stacks:bulk-assets --operation publish`   |
| `csdx cm:assets:unpublish` | `csdx cm:stacks:bulk-assets --operation unpublish` |


```bash
csdx cm:stacks:bulk-assets --operation publish \
  --environments prod \
  --locales en-us \
  --stack-api-key bltXXX \
  --alias myalias
```



#### New: CS Assets Bulk Delete and Move

**No prior equivalent in V1.** V2 adds two new operation types to `cm:stacks:bulk-assets` that target the CS Assets API, separate from the CMS publish pipeline:


| Operation            | What it does                                             |
| -------------------- | -------------------------------------------------------- |
| `--operation delete` | Bulk delete assets from a CS Assets space (async job)    |
| `--operation move`   | Bulk move assets to a target folder in a CS Assets space |


**CS Assets bulk delete:**

```bash
csdx cm:stacks:bulk-assets \
  --operation delete \
  --space-uid am123 \
  --org-uid bltOrg \
  --locale en-us \
  --asset-uids-file ./assets.json
```

`assets.json` contains `{ "uids": ["uid1", "uid2"] }`.

**CS Assets bulk move:**

```bash
csdx cm:stacks:bulk-assets \
  --operation move \
  --space-uid am123 \
  --org-uid bltOrg \
  --target-folder-uid amFolder \
  --asset-uids-file ./assets.json
```

**Requirements:** you must configure `csAssetsUrl` in region settings (`csdx config:set:region --cs-assets <url>`). You cannot combine CMS flags (`--stack-api-key`, `--alias`, `--environments`, `--locales`, `--branch`) with CS Assets flags. `delete` requires `--locale`. `move` does not accept it.

> **Where to find** `--space-uid` **and** `--org-uid`**:** In the Contentstack UI, go to **Organization > Contentstack Assets > Settings**. The Space UID and Organization UID appear there. You can also retrieve them from the CS Assets API.

V2 removes the `--api-version` flag here too and hardcodes `api_version: '3.2'` on all calls (same as bulk-entries).

### cm:stacks:bulk-taxonomies

**No prior equivalent in V1.** New command for bulk publishing or unpublishing taxonomy terms. V2 hardcodes `api_version: '3.2'` on all calls.


| Flag              | Short | Description                                                   |
| ----------------- | ----- | ------------------------------------------------------------- |
| `--operation`     |       | `publish` or `unpublish`                                      |
| `--stack-api-key` | `-k`  | Stack API key                                                 |
| `--alias`         | `-a`  | Management token alias                                        |
| `--environments`  |       | Target environments (multiple allowed)                        |
| `--locales`       |       | Target locales (multiple allowed)                             |
| `--taxonomies`    |       | Comma-separated taxonomy UIDs. Omit to target all taxonomies. |
| `--branch`        |       | Branch (defaults to `main`)                                   |
| `--yes` / `--no`  | `-y`  | Skip confirmation prompt                                      |


**Publish specific taxonomies:**

```bash
csdx cm:stacks:bulk-taxonomies \
  --operation publish \
  --environments staging prod \
  --locales en-us fr-fr \
  --taxonomies products_tax,brands_tax \
  --stack-api-key bltXXX \
  --alias myalias
```

**Publish all taxonomies:**

```bash
csdx cm:stacks:bulk-taxonomies \
  --operation publish \
  --environments prod \
  --locales en-us \
  --stack-api-key bltXXX \
  --alias myalias
```



### cm:stacks:seed



#### Alias Removed

**Before:**

```bash
csdx cm:seed --repo contentstack/kickstart-stack-seed
```

**After:**

```bash
csdx cm:stacks:seed --repo contentstack/kickstart-stack-seed
```



#### Removed Flags


| Removed          | V2 Replacement                         |
| ---------------- | -------------------------------------- |
| `--stack` / `-s` | `--stack-api-key` (no short character) |
| `-r` (repo)      | `--repo` (long form only)              |
| `-o` (org)       | `--org` (long form only)               |


**Before:**

```bash
csdx cm:stacks:seed -s blt123 -r contentstack/kickstart-stack-seed -o orgUid
```

**After:**

```bash
csdx cm:stacks:seed --stack-api-key blt123 --repo contentstack/kickstart-stack-seed --org orgUid
```



#### Interactive Mode Changed: Curated List Replaces GitHub API

**Before:** running `csdx cm:stacks:seed` without `--repo` in V1 queries the GitHub API for all Contentstack repos.

**After:** V2 shows a fixed curated list of 3 repos:

1. Kickstart stack seed (`contentstack/kickstart-stack-seed`)
2. Kickstart Veda (`contentstack/kickstart-veda-seed`)
3. Compass starter stack (`contentstack/compass-starter-stack`)

> **Note:** V2 removes `contentstack/stack-starter-app` from the curated list. If you need it, pass it directly with `--repo contentstack/stack-starter-app`.

If you need a repo that is not on this list, use `--repo owner/repo` directly.

### cm:bootstrap



#### Removed Flags


| Removed              | V2 Replacement                                                       |
| -------------------- | -------------------------------------------------------------------- |
| `--appName` / `-a`   | `--app-name`                                                         |
| `--directory` / `-d` | `--project-dir`                                                      |
| `--appType` / `-s`   | *(removed, no replacement needed, V2 hardcodes app type internally)* |


> **Note:** V1 has a short flag collision, both `--appName` and `--alias` claim `-a`. V2 resolves this: `--app-name` has no short character, and `-a` exclusively means `--alias`. Any script that used `-a` for app name must switch to `--app-name` (long form only).

**Before:**

```bash
csdx cm:bootstrap --appName reactjs --directory ./myapp --appType sampleapp
```

**After:**

```bash
csdx cm:bootstrap --app-name compass-app --project-dir ./myapp
```



#### 13 App Configs Removed

V2 no longer accepts the following `--app-name` values. Passing any of them throws `CLI_BOOTSTRAP_INVALID_APP_NAME`.

**Removed sample apps (4), were in the** `sampleApps` **interactive list:**


| `--app-name` | GitHub Source                                            | Stack Seed                                                     |
| ------------ | -------------------------------------------------------- | -------------------------------------------------------------- |
| `reactjs`    | `contentstack/contentstack-reactjs-universal-sample-app` | `contentstack/stack-contentstack-reactjs-universal-sample-app` |
| `nextjs`     | `contentstack/contentstack-nextjs-react-universal-demo`  | `contentstack/stack-contentstack-nextjs-react-universal-demo`  |
| `gatsby`     | `contentstack/gatsby-starter-contentstack`               | `contentstack/stack-gatsby-starter-contentstack`               |
| `angular`    | `contentstack/contentstack-angular-modularblock-example` | `contentstack/stack-contentstack-angular-modularblock-example` |


**Removed starter apps (8), were in the** `starterApps` **interactive list:**


| `--app-name`      | GitHub Source                                   | Stack Seed                       |
| ----------------- | ----------------------------------------------- | -------------------------------- |
| `reactjs-starter` | `contentstack/contentstack-react-starter-app`   | `contentstack/stack-starter-app` |
| `nextjs-starter`  | `contentstack/contentstack-nextjs-starter-app`  | `contentstack/stack-starter-app` |
| `gatsby-starter`  | `contentstack/contentstack-gatsby-starter-app`  | `contentstack/stack-starter-app` |
| `angular-starter` | `contentstack/contentstack-angular-starter`     | `contentstack/stack-starter-app` |
| `nuxt-starter`    | `contentstack/contentstack-nuxtjs-starter-app`  | `contentstack/stack-starter-app` |
| `vue-starter`     | `contentstack/contentstack-vuejs-starter-app`   | `contentstack/stack-starter-app` |
| `stencil-starter` | `contentstack/contentstack-stencil-starter-app` | `contentstack/stack-starter-app` |
| `nuxt3-starter`   | `contentstack/contentstack-nuxt3-starter-app`   | `contentstack/stack-starter-app` |


**Removed hidden config entry (1), never shown interactively, passable through** `--app-name`**:**


| `--app-name`      | GitHub Source                                         |
| ----------------- | ----------------------------------------------------- |
| `nuxtjs-disabled` | `contentstack/contentstack-nuxtjs-vue-universal-demo` |




#### Valid App Names in V2 (8)

These apps existed in V1's `starterApps` list and carry over to V2 unchanged. Display names ending in SSR or SSG name the app's rendering strategy, server-side rendering (SSR) or static site generation (SSG):


| `--app-name`                | Display Name                 | GitHub Source                            | Stack Seed                           |
| --------------------------- | ---------------------------- | ---------------------------------------- | ------------------------------------ |
| `compass-app`               | Compass App                  | `contentstack/compass-starter-app`       | `contentstack/compass-starter-stack` |
| `kickstart-next`            | Kickstart Next.js            | `contentstack/kickstart-next`            | `contentstack/kickstart-stack-seed`  |
| `kickstart-next-ssr`        | Kickstart Next.js SSR        | `contentstack/kickstart-next-ssr`        | `contentstack/kickstart-stack-seed`  |
| `kickstart-next-ssg`        | Kickstart Next.js SSG        | `contentstack/kickstart-next-ssg`        | `contentstack/kickstart-stack-seed`  |
| `kickstart-next-graphql`    | Kickstart Next.js GraphQL    | `contentstack/kickstart-next-graphql`    | `contentstack/kickstart-stack-seed`  |
| `kickstart-next-middleware` | Kickstart Next.js Middleware | `contentstack/kickstart-next-middleware` | `contentstack/kickstart-stack-seed`  |
| `kickstart-nuxt`            | Kickstart NuxtJS             | `contentstack/kickstart-nuxt`            | `contentstack/kickstart-stack-seed`  |
| `kickstart-nuxt-ssr`        | Kickstart NuxtJS SSR         | `contentstack/kickstart-nuxt-ssr`        | `contentstack/kickstart-stack-seed`  |




### cm:stacks:audit



#### Short Aliases Removed

V2 strips the short aliases from both commands:


| Removed Alias | Canonical V2 Command  |
| ------------- | --------------------- |
| `audit`       | `cm:stacks:audit`     |
| `audit:fix`   | `cm:stacks:audit:fix` |


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



#### Audit Reads Per-UID Files: V1 Exports Produce Silent Empty Results

`cm:stacks:audit` now uses `readContentTypeSchemas` and `readGlobalFieldSchemas` (the same utilities V2 import uses) to load content type and global field schemas from the `--report-path` directory. These utilities read individual `<uid>.json` files and explicitly ignore `schema.json` and `globalfields.json`.

If you run audit against a V1 export directory, content types load correctly (V1 export writes per-UID files). **Global fields return zero results,** a false clean, because V1 export writes only `globalfields.json` with no per-UID files.

**Migration:** Re-export global fields with V2 before auditing. A separate conversion script covers cases where re-export is not possible.

See [cm:stacks:audit Reports Zero Global-Field Issues on a V1 Export (False Clean)](#cmstacksaudit-reports-zero-global-field-issues-on-a-v1-export-false-clean) in Troubleshooting for the condensed symptom and resolution.

### cm:stacks:migration



#### Removed Flags


| Removed                    | V2 Replacement                                        |
| -------------------------- | ----------------------------------------------------- |
| `-B`                       | `--branch`                                            |
| `-A`                       | `--alias`                                             |
| `-n`                       | `--file-path`                                         |
| `--api-key`                | `--stack-api-key`                                     |
| `--authtoken`              | *(removed, use* `csdx auth:login` *then* `--alias`*)* |
| `--management-token-alias` | `--alias`                                             |
| `--filePath`               | `--file-path`                                         |
| `--multi`                  | `--multiple`                                          |


**Before:**

```bash
csdx cm:migration -B feature-branch -n ./migrate.js
```

**After:**

```bash
csdx cm:stacks:migration --branch feature-branch --file-path ./migrate.js
```



### cm:stacks:validate-regex



#### Removed Flags


| Removed | V2 Replacement  |
| ------- | --------------- |
| `-c`    | `--contentType` |
| `-f`    | `--filePath`    |
| `-g`    | `--globalField` |


**Before:**

```bash
csdx cm:stacks:validate-regex -c blog -f ./regex.json -g header
```

**After:**

```bash
csdx cm:stacks:validate-regex --contentType blog --filePath ./regex.json --globalField header
```



#### Output Format

The results table and `results.csv` file use the same column order in both V1 and V2: `Module`, `Title`, `UID`, `Invalid Regex Count`. If you parse CSV output by header name, you need no changes.

### auth:tokens



#### Behavior Changed: Now a Help Dispatcher

**Before:** `csdx auth:tokens` lists your tokens in V1.

```bash
csdx auth:tokens
```

**After:** V2 displays sub-command help instead. Use `csdx auth:tokens:list` to list tokens.

```bash
csdx auth:tokens:list
```

**Silent failure risk:** if your script runs `csdx auth:tokens` to get a token table and parses `stdout`, it silently receives help text instead of a table. V2 raises no error code.

V2 also removes the `tokens` short alias. `csdx tokens` fails with "command not found".

### auth:tokens:add



#### Removed Flags


| Removed                   | V2 Replacement                  |
| ------------------------- | ------------------------------- |
| `-d`                      | `--delivery` (long form only)   |
| `-m`                      | `--management` (long form only) |
| `-t`                      | `--token` (long form only)      |
| `--api-key` (hidden)      | Removed entirely                |
| `-f` / `--force` (hidden) | Use `-y` / `--yes`              |


**Before:**

```bash
csdx auth:tokens:add -a myalias -d -t bltABC -k blt123
```

**After:**

```bash
csdx auth:tokens:add -a myalias --delivery --token bltABC --stack-api-key blt123
```



### auth:tokens:remove



#### `-i` / `--ignore` Flag Removed

**Before:** in V1, `-i` / `--ignore` makes the command succeed silently even if the alias does not exist.

```bash
csdx auth:tokens:remove -a myalias -i
```

**After:** V2 removes the flag. If the alias does not exist, V2 prints a yellow warning and exits 0 (raises no error). Scripts that relied on a non-zero exit when you omitted `--ignore` should account for this change.

```bash
csdx auth:tokens:remove -a myalias
```

V2 prints `No token found with alias 'myalias'.` (yellow) and exits 0.

### auth:logout



#### `-f` / `--force` Hidden Flag Removed

**Before:**

```bash
csdx auth:logout -f
csdx auth:logout --force
```

**After:** V2 returns an "Unexpected argument" error for both forms above. Use:

```bash
csdx auth:logout -y
csdx auth:logout --yes
```



### config:set:region



#### Removed Flags


| Removed | V2 Replacement |
| ------- | -------------- |
| `-d`    | `--cda`        |
| `-m`    | `--cma`        |
| `-n`    | `--name`       |


**Before:**

```bash
csdx config:set:region -d https://cdn.example.com -m https://api.example.com -n MyRegion
```

**After:**

```bash
csdx config:set:region --cda https://cdn.example.com --cma https://api.example.com --name MyRegion
```



#### New: `--cs-assets` Flag

**No prior equivalent in V1.** V2 adds a `--cs-assets` flag for specifying the Contentstack Assets API URL when you configure a custom region:

```bash
csdx config:set:region \
  --cma https://custom.cma.example.com \
  --cda https://custom.cda.example.com \
  --ui-host https://custom.ui.example.com \
  --name MyRegion \
  --cs-assets https://custom.am-api.example.com
```

When you omit `--cs-assets`, V2 derives the CS Assets URL from the Content Management API (CMA) URL automatically.

`config:get:region` now also shows `Contentstack Assets URL` in its output.

### config:set:log



#### Config Key Changed: V1 Settings Lost on Upgrade

V1 stores the console log preference as `log["show-console-logs"]` (hyphenated). V2 stores it as `log["showConsoleLogs"]` (camelCase). The two formats are not compatible.

**After you upgrade, V2 silently ignores your V1 console log configuration.** Progress bars are the default. If your CI needs console log output, re-run:

```bash
csdx config:set:log --show-console-logs
```

To explicitly switch back to progress bars (the V2 default):

```bash
csdx config:set:log --no-show-console-logs
```

See [V1 Console Log Config Silently Ignored After Upgrade](#v1-console-log-config-silently-ignored-after-upgrade) in Troubleshooting for the condensed symptom and resolution.

### config:set:early-access-header

**Documentation fix, no behavioral change.**

V1 has the `--header` and `--header-alias` descriptions swapped:


| Flag             | V1 description (incorrect)                   | V2 description (correct)                              |
| ---------------- | -------------------------------------------- | ----------------------------------------------------- |
| `--header-alias` | "Provide the Early Access header value"      | "Provide a name (alias) for this Early Access header" |
| `--header`       | "Provide the Early Access header alias name" | "Provide the Early Access header value"               |


The actual behavior was always: `--header-alias` sets the alias name, `--header` sets the header value. If you followed V1's incorrect help text and passed values in the wrong order, correct your scripts:

```bash
csdx config:set:early-access-header --header-alias myheader --header x-header-value
```



### tsgen

`tsgen` generates TypeScript interfaces from your stack's content type schemas, authenticated with a delivery token alias. Use the generated types to annotate content model access in a TypeScript client, whether that client uses the Contentstack Delivery SDK or a plain HTTP request. See the [tsgen plugin docs](https://www.contentstack.com/docs/headless-cms/tsgen-plugin) for full usage.

#### `--token-alias` Renamed to `--alias`, Short Characters Removed


| Change                               | Details                                                                      |
| ------------------------------------ | ---------------------------------------------------------------------------- |
| `--token-alias` renamed to `--alias` | The full flag name changed. `--token-alias` now produces "Nonexistent flag:" |
| `-o` removed                         | Was short for `--output`                                                     |
| `-p` removed                         | Was short for `--prefix`                                                     |
| `-d` removed                         | Was short for `--doc`                                                        |
| `-a` (short for alias)               | **Kept** on the renamed `--alias` flag                                       |


**Before:**

```bash
csdx tsgen --token-alias myalias -o ./types -p CS_ -d
```

**After:**

```bash
csdx tsgen --alias myalias --output ./types --prefix CS_ --doc
```

Or use `-a` for alias:

```bash
csdx tsgen -a myalias --output ./types --prefix CS_ --doc
```



### app:create



#### `-n` Short Character Removed

**Before:**

```bash
csdx app:create -n my-app
```

**After:**

```bash
csdx app:create --name my-app
```



### migrate:convert



#### Removed Flags


| Removed | V2 Replacement    |
| ------- | ----------------- |
| `-o`    | `--output`        |
| `-m`    | `--master-locale` |
| `-a`    | `--affix`         |


**Before:**

```bash
csdx migrate:convert -o ./output -m en-us -a v2_
```

**After:**

```bash
csdx migrate:convert --output ./output --master-locale en-us --affix v2_
```



### migrate:export



#### `-o` Short Character Removed

**Before:**

```bash
csdx migrate:export -o ./output
```

**After:**

```bash
csdx migrate:export --output ./output
```



### content-type:audit

> **Note on the** `content-type:`* **namespace:** these commands belong to a separate plugin (`@contentstack/contentstack-content-type`) that inspects and compares content type schemas. They differ from `cm:stacks:`* commands: they do not export or import content, they analyze schema structure. The flag changes below apply to every command in this namespace.



#### Removed Flags


| Removed                | V2 Replacement           |
| ---------------------- | ------------------------ |
| `--stack` / `-s`       | `--stack-api-key` / `-k` |
| `--token-alias` / `-a` | `--alias` / `-a`         |
| `-c` (content-type)    | `--content-type`         |


**Before:**

```bash
csdx content-type:audit --stack blt123 --token-alias myalias -c blog
```

**After:**

```bash
csdx content-type:audit --stack-api-key blt123 --alias myalias --content-type blog
```



### content-type:compare



#### Removed Flags


| Removed                | V2 Replacement           |
| ---------------------- | ------------------------ |
| `--stack` / `-s`       | `--stack-api-key` / `-k` |
| `--token-alias` / `-a` | `--alias` / `-a`         |
| `-c` (content-type)    | `--content-type`         |
| `-l` (left)            | `--left`                 |
| `-r` (right)           | `--right`                |


**Before:**

```bash
csdx content-type:compare --stack blt123 --token-alias myalias -c blog -l v1 -r v2
```

**After:**

```bash
csdx content-type:compare --stack-api-key blt123 --alias myalias --content-type blog --left v1 --right v2
```



### content-type:compare-remote



#### Removed Flags


| Removed | V2 Replacement   |
| ------- | ---------------- |
| `-o`    | `--origin-stack` |
| `-r`    | `--remote-stack` |
| `-c`    | `--content-type` |


Note: `content-type:compare-remote` never has `--stack` / `--token-alias` flags in V1.

**Before:**

```bash
csdx content-type:compare-remote -o bltOrigin -r bltRemote -c blog
```

**After:**

```bash
csdx content-type:compare-remote --origin-stack bltOrigin --remote-stack bltRemote --content-type blog
```



### content-type:details



#### Removed Flags


| Removed                | V2 Replacement           |
| ---------------------- | ------------------------ |
| `--stack` / `-s`       | `--stack-api-key` / `-k` |
| `--token-alias` / `-a` | `--alias` / `-a`         |
| `-c` (content-type)    | `--content-type`         |
| `-p` (path)            | `--path`                 |


**Before:**

```bash
csdx content-type:details --stack blt123 --token-alias myalias -c blog -p fields.title
```

**After:**

```bash
csdx content-type:details --stack-api-key blt123 --alias myalias --content-type blog --path fields.title
```



### content-type:diagram



#### Removed Flags


| Removed                | V2 Replacement           |
| ---------------------- | ------------------------ |
| `--stack` / `-s`       | `--stack-api-key` / `-k` |
| `--token-alias` / `-a` | `--alias` / `-a`         |
| `-o` (output)          | `--output`               |
| `-d` (direction)       | `--direction`            |
| `-t` (type)            | `--type`                 |


**Before:**

```bash
csdx content-type:diagram --stack blt123 --token-alias myalias -o ./diagram.svg -d LR -t svg
```

**After:**

```bash
csdx content-type:diagram --stack-api-key blt123 --alias myalias --output ./diagram.svg --direction LR --type svg
```



### content-type:list



#### Removed Flags


| Removed                | V2 Replacement           |
| ---------------------- | ------------------------ |
| `--stack` / `-s`       | `--stack-api-key` / `-k` |
| `--token-alias` / `-a` | `--alias` / `-a`         |
| `-o` (order)           | `--order`                |


**Before:**

```bash
csdx content-type:list --stack blt123 --token-alias myalias -o asc
```

**After:**

```bash
csdx content-type:list --stack-api-key blt123 --alias myalias --order asc
```



## CS Assets (Asset Management 2.0)

**No prior equivalent in V1.** V2 adds support for Contentstack's CS Assets system (Asset Management 2.0, or AM 2.0) in export, import, and import-setup, each of which detects and handles CS Assets automatically if your stack has linked workspaces. Bulk operations supports CS Assets **delete** and **move** only. CS Assets has no bulk publish or unpublish support.

**Export:** if your stack has linked workspaces configured in Contentstack Assets settings, export writes CS Assets data to a `spaces/` directory alongside the standard `assets/` directory. If your stack has no linked workspaces, export falls back to standard asset export automatically:

```
export/
  assets/         (CMS assets, unchanged)
  spaces/         (new: CS Assets)
    <space-id>/workspaces/
    <space-id>/asset_types/
    <space-id>/assets/
    <space-id>/folders/
```

**Import:** V2 detects the `spaces/` directory and imports CS Assets automatically.

**Import-setup:** V2 detects CS Assets exports and generates identity UID and URL mapper files.

**New bulk operations:** `cm:stacks:bulk-assets --operation delete` and `--operation move` handle CS Assets (see the new flags `--space-uid`, `--org-uid`, `--workspace`, `--asset-uids-file`, `--target-folder-uid` in [cm:stacks:bulk-assets](#cmstacksbulk-assets)).

## Taxonomy Publishing

V2 adds taxonomy publishing support across export, import, and bulk operations.

**Before:** V1 export does not capture taxonomy publish details. V1 import does not re-publish taxonomies.

**After:**

- **Export** captures `publish_details` per locale for each taxonomy.
- **Import** re-publishes taxonomies after import by default. To skip publishing (for example, if you want to review entries before publishing):
  ```bash
  csdx cm:stacks:import --skip-taxonomy-publish -d ./export -k bltXXX
  ```
- `cm:stacks:bulk-taxonomies` handles bulk taxonomy publish operations (see [cm:stacks:bulk-taxonomies](#cmstacksbulk-taxonomies)).



## Global Fields Per-File Export

**Before:** V1 exports all global fields into a single `globalfields.json` file.

**After:** V2 exports each global field as its own `<uid>.json` file (same format as content types). See [cm:stacks:export](#cmstacksexport) for the full file structure change.

## Visual Progress System

**Before:** V1 prints text line-by-line to `stdout` for all major operations.

**After:** V2 shows visual progress bars and a summary table at the end of the run for all major operations. See [config:set:log](#configsetlog) to restore console log output for CI environments.

## Troubleshooting



### Global Fields Silently Skipped on Import

**Symptom:** you run `cm:stacks:import` against a V1 export. The command reports success. Zero global fields exist in the target stack afterward, with no error or warning.

**Root Cause:** V2's per-UID file readers ignore the aggregate `globalfields.json` file that V1 export writes. V1 export never writes individual global-field files, so V2 import finds nothing to read.

**Resolution:** Re-export your stack with V2 before importing. A separate migration conversion script covers cases where a V2 re-export is not possible.

**See also:** [cm:stacks:import](#cmstacksimport)

### Branch Export Silently Overwrites Another Branch's Data

**Symptom:** you export two branches to the same `--data-dir`. The second export command completes successfully. The first branch's data is gone, with no error or warning.

**Root Cause:** V2 writes flat output to `exportDir/...` with no `<branch-uid>/` subfolder, regardless of how you select the branch. The second export overwrites the first at the file level.

**Resolution:** Use a separate `--data-dir` per branch:

```bash
csdx cm:stacks:export --branch main       --data-dir ./export-main    --stack-api-key bltXXX
csdx cm:stacks:export --branch feature-x  --data-dir ./export-feature --stack-api-key bltXXX
```

**See also:** [cm:stacks:export](#cmstacksexport)

### V1 Console Log Config Silently Ignored After Upgrade

**Symptom:** after you upgrade to V2, CI pipelines that parse console output for success or failure signals start receiving progress-bar escape codes instead of plain text, even though you configured `csdx config:set:log --show-console-logs` under V1.

**Root Cause:** V1 stores the console log preference under the key `log["show-console-logs"]` (hyphenated). V2 reads a different key, `log["showConsoleLogs"]` (camelCase). The two formats are not compatible, so V2 treats the setting as unset and defaults to progress bars.

**Resolution:** Re-run the config command after upgrading:

```bash
csdx config:set:log --show-console-logs
```

**See also:** [config:set:log](#configsetlog), [Default Output: Progress Bars Replace Console Logs](#default-output-progress-bars-replace-console-logs)

### V1 Multi-Branch Export Produces an Empty Import

**Symptom:** you run V2 `cm:stacks:import` with `--data-dir` pointing at the root of a V1 multi-branch export. The command completes. No content imports, with no error or warning.

**Root Cause:** V1 import auto-detects the branch by reading `branches.json` at the export root and navigating into the matching `<branch-uid>/` subfolder (the `selectBranchFromDirectory` logic). V2 removes this logic. When you point V2 at the export root, it looks for content files directly in that folder, where only `branches.json` lives, and finds nothing.

**Resolution:** Point `--data-dir` directly at the branch subfolder:

```bash
csdx cm:stacks:import --data-dir ./my-export/main
```

**See also:** [cm:stacks:import](#cmstacksimport)

### cm:stacks:audit Reports Zero Global-Field Issues on a V1 Export (False Clean)

**Symptom:** you run `cm:stacks:audit` against a V1 export directory. The audit reports zero global-field issues, even when the export contains actual issues.

**Root Cause:** audit uses the same per-UID-only file readers as V2 import (`readContentTypeSchemas` and `readGlobalFieldSchemas`). These readers ignore `globalfields.json`, the only global-field file a V1 export writes. With no per-UID files to read, audit reports zero results instead of an accurate count.

**Resolution:** Re-export global fields with V2 before auditing. A separate conversion script covers cases where re-export is not possible.

**See also:** [cm:stacks:audit](#cmstacksaudit)

### Rolling Back After a Broken Upgrade

**Symptom:** the V2 upgrade breaks a workflow and you need to return to V1 while you investigate.

**Root Cause:** Not applicable. This entry is a recovery procedure rather than a failure diagnosis. It is grouped with the other Troubleshooting entries because it applies after any upgrade-related failure, regardless of cause.

**Resolution:** follow these steps:

1. Restore from your pre-upgrade stack export (the one you made in [Prerequisites](#prerequisites) before upgrading).
2. Downgrade the CLI: `npm install -g @contentstack/cli@1.x`.
3. Your tokens remain available. Both V1 and V2 read from the same token store.



## Pre-Upgrade Checklist

This checklist orders items by risk. Complete top sections before lower ones.

### Critical: Do These First

1. Test the entire upgrade in a non-production environment before touching production.
2. **Your saved tokens carry over automatically.** Management tokens stored with `csdx auth:tokens:add` are available immediately after upgrading. You need no re-authentication. ([Tokens and Config Carry Over Automatically](#tokens-and-config-carry-over-automatically))



### High-Risk Script Changes

1. Add an explicit `--branch` flag to **all** `cm:stacks:export` calls for non-main branches. V2 only exports `main` when you omit `--branch`. ([cm:stacks:export](#cmstacksexport), [Branch Export Silently Overwrites Another Branch's Data](#branch-export-silently-overwrites-another-branchs-data))
2. Use a **separate** `--data-dir` **per branch.** V2 output is always flat (no `<branch-uid>/` subfolder), so exporting two branches to the same directory silently overwrites the first. ([Branch Export Silently Overwrites Another Branch's Data](#branch-export-silently-overwrites-another-branchs-data))
3. Rewrite all `cm:entries:publish*`, `cm:assets:publish*`, `cm:bulk-publish:*`, `cm:stacks:publish`, `cm:stacks:unpublish` calls to `cm:stacks:bulk-entries` / `cm:stacks:bulk-assets` commands. ([cm:stacks:bulk-entries](#cmstacksbulk-entries), [cm:stacks:bulk-assets](#cmstacksbulk-assets))
4. Verify publish behavior in a staging stack. All bulk publish and unpublish calls now use `api_version: '3.2'`, and V2 removes the `--api-version` flag. ([All Publish Operations Now Use NRP](#all-publish-operations-now-use-nrp))
5. Remove checks for `export-info.json` or `content_types/schema.json` in post-export tooling. V2 does not write these files. ([cm:stacks:export](#cmstacksexport))
6. Update tooling that reads `global_fields/globalfields.json` to iterate per-UID JSON files instead. ([cm:stacks:export](#cmstacksexport), [Global Fields Per-File Export](#global-fields-per-file-export))



### CI and Pipeline Audit

1. Verify your CI does not parse `stdout` for success signals. The output format changed to progress bars by default. ([Default Output: Progress Bars Replace Console Logs](#default-output-progress-bars-replace-console-logs))
2. Run `csdx config:set:log --show-console-logs` after upgrading if your CI parses console output. V2 silently drops the V1 log setting. ([V1 Console Log Config Silently Ignored After Upgrade](#v1-console-log-config-silently-ignored-after-upgrade))



### Script Audit: Command Renames

1. Replace `csdx cm:export` with `csdx cm:stacks:export`. ([Command Aliases Removed](#command-aliases-removed))
2. Replace `csdx cm:import` with `csdx cm:stacks:import`. ([Command Aliases Removed](#command-aliases-removed))
3. Replace `csdx cm:import-setup` with `csdx cm:stacks:import-setup`. ([Command Aliases Removed](#command-aliases-removed))
4. Replace `csdx cm:seed` with `csdx cm:stacks:seed`. ([Command Aliases Removed](#command-aliases-removed))
5. Replace `csdx tokens` with `csdx auth:tokens:list`. ([Command Aliases Removed](#command-aliases-removed))
6. Replace `csdx auth:tokens` (when used to list tokens) with `csdx auth:tokens:list`. ([auth:tokens](#authtokens))
7. Replace `csdx audit` with `csdx cm:stacks:audit`. ([Command Aliases Removed](#command-aliases-removed))



### Script Audit: Flag Changes

1. Remove `--stack-uid` / `-s` everywhere and use `--stack-api-key` instead. ([Type Mapping Reference](#type-mapping-reference))
2. Remove `--data` and use `--data-dir` instead. ([Type Mapping Reference](#type-mapping-reference))
3. Remove `--management-token-alias` and use `--alias` instead. ([Type Mapping Reference](#type-mapping-reference))
4. Remove `--auth-token` / `-A` and use `csdx auth:login` then `--alias` instead. ([Type Mapping Reference](#type-mapping-reference))
5. Remove `--skip-app-recreation` from all import scripts. V2 has no replacement. ([cm:stacks:import](#cmstacksimport))
6. Remove `--token-alias` on `tsgen` and use `--alias` instead. ([tsgen](#tsgen))
7. Audit scripts for removed short flags on export and import commands: `-m` / `-t` / `-B` / `-b` / `-A` (switch to long form only). ([cm:stacks:export](#cmstacksexport), [cm:stacks:import](#cmstacksimport))
8. Update `cm:bootstrap` flags: `--appName` to `--app-name`, `--directory` to `--project-dir`. ([cm:bootstrap](#cmbootstrap))
9. Remove bootstrap app names that no longer exist: `reactjs`, `nextjs`, `gatsby`, `angular`, and the `*-starter` variants. ([cm:bootstrap](#cmbootstrap))
10. Update `content-type:*` commands: remove `--stack` / `-s`, `--token-alias` / `-a`, and every listed short character. ([content-type:audit](#content-typeaudit))
11. Replace `csdx auth:logout -f` / `--force` with `csdx auth:logout -y` / `--yes`. ([auth:logout](#authlogout))



### Plugin Management

1. Install the `launch` plugin separately if you use `launch:*` commands: `csdx plugins:install @contentstack/cli-launch`. ([launch Plugin: Now Opt-In](#launch-plugin-now-opt-in))
2. Install the `migrate-rte` plugin separately if you use `cm:entries:migrate-html-rte`: `csdx plugins:install @contentstack/cli-cm-migrate-rte`. ([migrate-rte Plugin: Now Opt-In](#migrate-rte-plugin-now-opt-in))
3. If you use CS Assets, verify your stack has linked workspaces configured in Contentstack Assets settings. Otherwise export falls back to standard asset export. ([CS Assets (Asset Management 2.0)](#cs-assets-asset-management-20))



### Custom Plugins (Plugin Authors Only)

1. Update `engines.node` to `>=22.0.0` in your plugin's `package.json`. ([Node.js 22+](#nodejs-22))



### Test Run

1. Run a full export and import cycle on a non-production stack before cutting over.
2. Verify branch exports capture the correct branches explicitly.
3. If you use CS Assets, verify your stack has linked workspaces configured. Otherwise export falls back to standard asset export automatically, with no error.
4. If you use bulk publish or unpublish, run a test publish in staging. All calls now use `api_version: '3.2'`.



## Next Steps

- [Contentstack CLI documentation](https://www.contentstack.com/docs/headless-cms/install-the-cli): reference documentation for the V1 CLI.
- [Migrate content from HTML RTE to JSON RTE](https://www.contentstack.com/docs/developers/cli/migrate-content-from-html-rte-to-json-rte): docs for the `migrate-rte` plugin you now install separately (see [migrate-rte Plugin: Now Opt-In](#migrate-rte-plugin-now-opt-in)).
- [tsgen plugin docs](https://www.contentstack.com/docs/headless-cms/tsgen-plugin): full usage reference for the `tsgen` command (see [tsgen](#tsgen)).
- CLI changelog: TODO, add a link to the Contentstack CLI changelog once a public URL exists. No changelog URL exists in the source material for this guide.

