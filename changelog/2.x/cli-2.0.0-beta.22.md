# CLI Version 2.0.0-beta.22

2026-05-18

**New Feature:**

- **cli-cm-export-query (v2.0.0-beta.1)**:
  - Added support for nested global fields, enabling more granular data extraction for complex content models.

**Enhancement:**

- Performed dependency upgrades across the following plugins to ensure compatibility and stability:
  - **cli-asset-management (v1.0.0-beta.1)**
  - **cli-audit (v2.0.0-beta.12)**
  - **cli-cm-bootstrap (v2.0.0-beta.17)**
  - **cli-cm-clone (v2.0.0-beta.18)**
  - **cli-cm-export (v2.0.0-beta.17)**
  - **cli-cm-import (v2.0.0-beta.17)**
  - **cli-cm-seed (v2.0.0-beta.17)**

**Bug fix:**

- **types-generator (v3.10.0)** and **contentstack-cli-tsgen (v4.9.0)**:
  - Fixed a bug that incorrectly handled or affected numeric IDs in generated types.

**Security fix:**

- Resolved security vulnerabilities by updating affected dependencies in:
  - **contentstack-cli-content-type (v1.4.5)**
  - **cli-cm-migrate-rte (v2.0.0-beta.6)**
