# CLI Version 1.55.0

2026-01-19

**Enhancements**

- Added OAuth support in the **cli-content-type (v1.4.0)** plugin.

- Introduced a new logger configuration in the **cli-config (v1.17.0)** plugin.

- Upgraded dependencies to improve stability and compatibility in the following plugins:
  - **cli-cm-seed (v1.14.0)**
  - **cli-cm-bulk-publish (v1.10.5)**
  - **cli-cm-clone (v1.19.0)**
  - **cli-cm-bootstrap (v1.18.0)**
  - **cli-cm-export (v1.23.0)**

**Bugs & Security Fixes**

- Added Studio validation in the **cli-audit (v1.17.0)** plugin.
- Updated the import workflow to skip composition types and compositions when a Studio project fails to import in the **cli-cm-import (v1.31.0)** plugin.
