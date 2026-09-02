# CLI Version 2.0.0-beta.20

2026-04-20

**Enhancements:**

- **cli-cm-export (v2.0.0-beta.15):**
  - Introduced Single-branch layout support: Content is now written directly under the export directory. The `branchDir` is set to `exportDir`, eliminating per-branch subfolders for a flatter structure.

- **cli-variants (v2.0.0-beta.12):**
  - Standardized all variant export modules (attributes, audiences, events, experiences, projects, and variant-entries) to use the `exportDir`.

- Updated the following plugins to ensure compatibility and stability:
  - **cli-auth (v2.0.0-beta.11)**
  - **cli-cm-bootstrap (v2.0.0-beta.15)**
  - **cli-cm-branches (v2.0.0-beta.6)**
  - **cli-cm-export-to-csv (v2.0.0-beta.6)**
  - **cli-cm-import-setup (v2.0.0-beta.10)**
  - **cli-command (v2.0.0-beta.6)**
  - **cli-config (v2.0.0-beta.8)**
  - **cli-migration (v2.0.0-beta.11)**
  - **cli-audit (v2.0.0-beta.10)**
  - **cli-cm-seed (v2.0.0-beta.14)**

**Bug & Security Fixes:**

- **cli-cm-import (v2.0.0-beta.15):**
  - Fixed taxonomy mapping during import by correctly utilizing the backup directory.
  - Simplified path resolution: The plugin no longer reads `branches.json` or triggers branch selection. It now defaults to the user-provided content directory (export root).

- **cli-cm-clone (v2.0.0-beta.16):**
  - Fixed issues with test report generation.

- Resolved security vulnerabilities by updating dependencies in the following plugins:
  - **cli-utilities (v2.0.0-beta.6)**
  - **cli-cm-export-query (v1.0.0-beta.11)**
