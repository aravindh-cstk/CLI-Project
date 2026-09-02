# CLI Version 2.0.0-beta.29

2026-07-20

**Enhancements:**

- `cli-bulk-operations`:
  - Merged the `cm:stacks:bulk-am-assets` command into `cm:stacks:bulk-assets`. All asset functionality is now supported directly by `cm:stacks:bulk-assets`, removing the need for a specific assets command.
  - Integrated the Progress Manager UI into all `cm:stacks:bulk-*` commands, ensuring bulk operations now display a clean header, a live summary, and per-command Module Details.

- Upgraded dependencies for the following plugins:
  - `cli-utilities (v2.0.0-beta.11)`
  - `cli-bulk-operations (v2.0.0-beta.4)`
  - `cli-auth (v2.0.0-beta.16)`
  - `cli-command (v2.0.0-beta.10)`
  - `cli-config (v2.0.0-beta.14)`
  - `apps-cli (v2.0.0-beta.4)`
  - `cli-asset-management (v1.0.0-beta.7)`
  - `cli-audit (v2.0.0-beta.15)`
  - `cli-cm-bootstrap (v2.0.0-beta.24)`
  - `cli-cm-branches (v2.0.0-beta.10)`
  - `cli-cm-regex-validate (v2.0.0-beta.3)`
  - `contentstack-cli-tsgen (v5.0.0-beta.3)`
  - `cli-cm-clone (v2.0.0-beta.25)`
  - `contentstack-cli-content-type (v2.0.0-beta.2)`
  - `cli-cm-export (v2.0.0-beta.24)`
  - `cli-cm-export-to-csv (v2.0.0-beta.11)`
  - `cli-external-migrate (v2.0.0-beta.3)`
  - `cli-cm-import (v2.0.0-beta.24)`
  - `cli-cm-import-setup (v2.0.0-beta.18)`
  - `cli-cm-migrate-rte (v2.0.0-beta.9)`
  - `cli-migration (v2.0.0-beta.16)`
  - `cli-cm-export-query (v2.0.0-beta.8)`
  - `cli-cm-seed (v2.0.0-beta.24)`
  - `cli-variants (v2.0.0-beta.19)`
