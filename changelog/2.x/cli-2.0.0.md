# CLI Version 2.0.0

2026-08-13

**Breaking Changes:**

- **`cm:stacks:migration` configuration flags changed.** `--config` now takes the path of a JSON configuration file, inline configuration moved to the new `--inline-config` flag, and `--config-file` is removed. `--config` kept its name and changed its meaning, so a script written for CLI 1.x that passes inline values to `--config` is read as a file path rather than failing outright. Update those calls to `--inline-config`.
- Removed `--reference-only` from `cm:stacks:audit` and `cm:stacks:audit:fix`.
- Removed `--app-type` from `cm:bootstrap`.
- Removed `--fetch-limit` from `cm:stacks:seed`.

**New Features:**

- **`@contentstack/cli (2.0.0)`**:
  - Introduced a guided warning and install prompt for missing `launch:*` or `cm:entries:migrate-html-rte` commands instead of a bare "command not found" error, making plugins opt-in at GA.

- **`@contentstack/cli-asset-management (1.0.0)`**:
  - Introduced a new plugin providing full Asset Management 2.0 (AM 2.0) API support, covering spaces, workspaces, fields, and asset types.
  - Added OAuth authentication support for AM.

- **`@contentstack/cli-bulk-operations (2.0.0)`**:
  - Consolidated 14 separate bulk-publish commands into unified commands (`cm:stacks:bulk-entries`, `cm:stacks:bulk-assets`).
  - Added the new `cm:stacks:bulk-taxonomies` command for bulk publishing or unpublishing taxonomy terms.
  - Integrated the Progress Manager UI.
  - Configured NRP to be used on all publish/unpublish calls.

- **`@contentstack/cli-cm-migrate-rte (2.0.0)`**:
  - Made the RTE migration available as a separate, opt-in plugin via `csdx plugins:install @contentstack/cli-cm-migrate-rte`.

- **`@contentstack/cli-auth (2.0.0)`**:
  - Added the new `auth:tokens:list` command for listing saved tokens and introduced the `auth:tokens` namespace as help.

- **`@contentstack/cli-utilities (2.0.0)`**:
  - Added a new `readGlobalFieldSchemas` utility function.
  - Introduced a retry mechanism with backoff for transient HTTP errors (network / 429 / 5xx), used across AM and export/import.
  - Implemented a strategy pattern to support Progress Manager and Summary Manager rollout across plugins.
  - Registered bulk-operations as a Progress-Manager-supported module.

**Enhancements:**

- **`@contentstack/cli-cm-export (2.0.0)`**:
  - Added AM 2.0 export support, featuring automatic detection via org plan-check to correctly skip assets under a management token.
  - Updated the export structure to output a flat directory.
  - Main branch is exported by default for branch enabled stack when branch flag is empty.
  - Changed Global fields to export as individual files (one per item) rather than a single combined file.
  - Removed the content type schema JSON export.
  - Added concurrency support for faster AM exports and improved logging.
  - Integrated Progress Manager and Summary Manager across stack, assets, environments, taxonomies, extensions, global fields, locales, personalize, and variant-entries export.
  - Removed the short flags `-A`, `-B`, `-m`, `-s`, `-t` from `cm:stacks:export`. The short forms `-a`, `-c`, `-d`, `-k`, `-y` are unchanged, so `--data-dir`, `--stack-api-key` and `--alias` keep `-d`, `-k` and `-a`.

- **`@contentstack/cli-cm-import (2.0.0)`**:
  - Added AM 2.0 import and asset publishing support.
  - Updated taxonomies to re-publish automatically after import, and added a new `--skip-taxonomy-publish` flag to allow review before publishing.
  - Integrated Progress Manager and Summary Manager.
  - Removed the short flags `-A`, `-B`, `-b`, `-m`, `-s` from `cm:stacks:import`. The short forms `-a`, `-c`, `-d`, `-k`, `-y` are unchanged.

- **`@contentstack/cli-cm-import-setup (2.0.0)`**:
  - Added AM 2.0 support and Progress Manager integration.

- **`@contentstack/cli-cm-seed (2.0.0)`**:
  - Refined the interactive stack-seed picker to display a curated list of 3 official starter repos instead of searching GitHub live for a faster, more reliable experience.

- **`@contentstack/cli-bulk-operations (2.0.0)`**:
  - Removed the `--api-version` flag from `cm:stacks:bulk-entries` and `cm:stacks:bulk-taxonomies` as the NRP header is used by default.

- **`@contentstack/cli-config (2.0.0)`**:
  - Added optional `--cs-assets` and `--auth-api` flags to `config:set:region` for setting custom Contentstack Assets and Auth API endpoints.
  - Improved error handling for rate-limit failures and region-endpoint resolution.

- **`@contentstack/cli-utilities (2.0.0)`**:
  - Consolidated session log files into a single folder per run.
  - Renamed the console log config key internally to `showConsoleLogs`.

- **`@contentstack/cli-variants (2.0.0)`**:
  - Ensured entry variants and variant groups correctly respect the `--branch` flag on export and import instead of always operating against the default branch.

- **`@contentstack/apps-cli (2.0.0)`**:
  - Added support for `-k` as a shorthand for `--stack-api-key`.

- **`contentstack-cli-tsgen (5.0.0)`**:
  - Renamed the `--token-alias` flag to `--alias`.
  - Removed `-o`, `-p`, and `-d` short flags in favor of long-form flags only.

- **`contentstack-cli-content-type (2.0.0)`**:
  - Removed the short flags `-c`, `-d`, `-l`, `-o`, `-p`, `-r`, `-s`, `-t` across the six `content-type:*` commands (audit, compare, compare-remote, details, diagram, list). `-a`, `-k` are unchanged, except on `content-type:compare-remote`, which now has no short flags.

- **`@contentstack/cli-migration (2.0.0)`** & **`@contentstack/cli-external-migrate (2.0.0)`**:
  - Removed the short flags `-A`, `-B`, `-n` from `cm:stacks:migration`. The short forms `-a`, `-k` are unchanged.

- **`@contentstack/cli-cm-regex-validate (2.0.0)`**:
  - Added new message strings to the plugin.

- **Cross-Plugin Enhancements**:
  - Implemented clearer, conditional success/warning messaging and consolidated end-of-run failure summaries across export, import, and bulk operations.

**Bug & Security Fixes:**

- **`@contentstack/cli (2.0.0)`**:
  - Fixed an issue where `Ctrl+C` during an interactive prompt threw an uncaught error; it now exits cleanly with code 130.
  - Resolved several false-positive hardcoded-secret findings flagged during a routine security scan.

- **`@contentstack/cli-auth (2.0.0)`**:
  - Fixed a two-factor authentication (2FA) login issue.

- **`@contentstack/cli-utilities (2.0.0)`**:
  - Fixed a race condition in OAuth token refresh where concurrent refresh attempts could conflict.

- **`@contentstack/cli-cm-clone (2.0.0)`**:
  - Resolved a prompt issue during clone import.
  - Fixed a path-resolution bug that broke when the CLI was installed under a directory path containing `/lib/` (e.g., Node's own `lib/node_modules`).

- **`@contentstack/cli-cm-export (2.0.0)`** & **`@contentstack/cli-cm-import (2.0.0)`**:
  - Fixed a null/undefined crash affecting multiple export/import modules (custom roles, environments, extensions, labels, locales, taxonomies, webhooks, and workflows).
  - Resolved a duplicate prompt for the marketplace app encryption key during export.
  - Corrected the taxonomy and extension mapper path used during import, which previously pointed to the wrong directory.

- **`@contentstack/cli-cm-export-to-csv (2.0.0)`**:
  - Fixed pagination when fetching organization users for organization owners with a large number of users.

- **`@contentstack/cli-cm-seed (2.0.0)`**:
  - Fixed a directory-change ordering bug that could break a nested import during seeding.

- **`@contentstack/cli-audit (2.0.0)`**:
  - Fixed the prompt shown when auditing a stack with no global fields.

- **`@contentstack/cli-variants (2.0.0)`**:
  - Fixed a content-type linking failure when a personalize experience had no audience.

- **`@contentstack/cli-external-migrate (2.0.0)`**:
  - Resolved a path traversal vulnerability in the Contentful migration adapter.
