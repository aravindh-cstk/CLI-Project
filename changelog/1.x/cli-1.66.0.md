# CLI Version 1.66.0

2026-07-27

**Enhancements:**

- `CLI (v1.66.0)`:
  - Added groundwork for organization plan-based feature gating for CLI commands (currently inactive until individual commands opt in).
  - Introduced an auto-refresh for endpoints on command pre-run.

- Added support for global field validation rule for the following plugins:
  - `cli-audit (v1.20.0)`
  - `cli-export (v1.26.0)`
  - `cli-import (v1.34.0)`

`cli-config (v1.22.0)`:

`cli-utilities (v1.20.0)`:

Updated dependency versions for the following plugins:

**Bug & Security Fixes:**

- `cli-utilities (v1.20.0)`:
  - Resolved an issue where resolving the org plan or auth host would fail hard when not explicitly configured. It now successfully falls back to deriving from the existing region host.

- `cli-command (v1.8.6)`:
  - Fixed issues related to context setting.

- **Security Fixes**: Resolved security vulnerabilities in the following plugins:
  - `cli-bulk-operations (v1.2.3)`
  - `cli-cm-regex-validate (v1.0.2)`
  - `contentstack-cli-content-type (v1.5.3)`
  - `cli-cm-migrate-rte (v1.7.3)`
