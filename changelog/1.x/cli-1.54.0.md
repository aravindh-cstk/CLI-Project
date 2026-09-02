# CLI Version 1.54.0

2026-01-12

**Enhancements**

- Added session file support in the session-based logger in the following plugins:
  - **cli-cm-export (v1.22.2)**
  - **cli-cm-import (v1.30.2)**
  - **cli-utilities (v1.16.0)**

- Introduced Progress Manager support in:
  - **cli-audit (v2.0.0-beta)**
  - **cli-cm-import-setup (v2.0.0-beta.1)**

- Upgraded dependencies to ensure stability and compatibility across the following plugins::
  - **cli-audit (v1.16.2)**
  - **cli-auth (v1.6.3)**
  - **cli-cm-bootstrap (v1.17.2)**
  - **cli-cm-branches (v1.6.2)**
  - **cli-cm-bulk-publish (v1.10.4)**
  - **cli-cm-export-to-csv (v1.10.2)**
  - **cli-cm-import-setup (v1.7.2)**
  - **cli-cm-migrate-rte (v1.6.3)**
  - **cli-cm-seed (v1.13.2)**
  - **cli-command (v1.7.1)**
  - **cli-config (v1.16.2)**
  - **cli-migration (v1.10.2)**
  - **cli-variants (v1.3.6)**

**Bugs & Security Fixes**

- Fixed an authentication failure during stack cloning for non-NA regions in **cli-cm-clone (v1.18.1)**.

- Resolved security issues in the following plugins:
  - **contentstack-cli-content-type (v1.3.2)**
  - **cli-cm-migrate-rte (v2.0.0-beta.1)**
  - **contentstack-apps-cli (v1.6.3)**

- Fixed additional security issues and upgraded Jest to v30 in **cli-cm-regex-validate (v1.2.5).**
