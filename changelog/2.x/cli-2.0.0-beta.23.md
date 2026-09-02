# CLI Version 2.0.0-beta.23

2026-05-25

**New Feature:**

- **Asset Management 2.0 (AM2.0) Support**: Added AM2.0 support to the import setup flow across the following plugins:
  - **cli-cm-import-setup (v2.0.0-beta.12)**
  - **cli-asset-management (v1.0.0-beta.2)**
  - **cli-cm-import (v2.0.0-beta.18)**

**Enhancement:**

- Performed dependency upgrades to improve stability and performance for:
  - **cli-cm-export (v2.0.0-beta.18)**
  - **cli-cm-export-query (v2.0.0-beta.2)**
  - **cli-cm-seed (v2.0.0-beta.18)**

**Bug fixes:**

- **cli-cm-bootstrap (v2.0.0-beta.18)**:
  - Cleaned up the plugin by removing deprecated sample and starter apps.

- **cli-cm-clone (v2.0.0-beta.19)**:
  - Fixed an issue to ensure the correct path is resolved in the clone plugin while running imports.

- **cli-config (v2.0.0-beta.10)**:
  - Fixed a bug where the `get region` command failed to display the AM endpoint for custom regions.
