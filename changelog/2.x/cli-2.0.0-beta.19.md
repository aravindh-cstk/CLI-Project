# CLI Version 2.0.0-beta.19

2026-03-30

**New Features:**

- **cli-cm-export (v2.0.0-beta.14):** Added support for management tokens, allowing for authentication during export processes.

**Enhancements:**

- Dependency upgrades for the following plugins:
  - **cli-import (v2.0.0-beta.14)**
  - **cli-auth (v2.0.0-beta.10)**
  - **cli-cm-bootstrap (v2.0.0-beta.14)**
  - **cli-cm-branches (v2.0.0-beta.5)**
  - **cli-cm-clone (v2.0.0-beta.15)**
  - **cli-cm-export-to-csv (v2.0.0-beta.5)**
  - **cli-cm-import-setup (v2.0.0-beta.9)**
  - **cli-command (v2.0.0-beta.5)**
  - **cli-config (v2.0.0-beta.6)**
  - **cli-migration (v2.0.0-beta.10)**
  - **cli-variants (v2.0.0-beta.11)**

**Bug & Security Fixes:**

- **cli-utilities (v2.0.0-beta.5):**
  - Refactored the OAuth token refresh logic in `AuthHandler` to prevent concurrent refresh operations.
  - Introduced the `oauthRefreshInFlight` promise to manage refresh state and updated tests to validate new behavior.

- **cli-audit (v2.0.0-beta.9):**
  - Fixed the Audit fix progress bar and the overwrite confirmation UX.

- **cli-cm-seed (v2.0.0-beta.13):**
  - Fixed an issue that stops `chdir` before nested import.

- Security updates to resolve vulnerabilities in:
  - **cli-tsgen (v4.8.3)**
  - **cli-cm-migrate-rte (v2.0.0-beta.4)**
