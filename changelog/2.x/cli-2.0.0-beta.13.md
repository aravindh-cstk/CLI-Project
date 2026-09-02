# CLI Version  2.0.0-beta.13

2026-03-03

**Enhancements:**

- **cli-audit (v2.0.0-beta.5):**
  - Added validation for referenced entry content types during entries audit.

**Bug & Security Fixes:**

- **cli-cm-export (v2.0.0-beta.10)** & **cli-cm-import (v2.0.0-beta.10):**
  - Updated schema JSON structure to utilize individual content type files instead of a single file.

- **cli-utilities (v2.0.0-beta.1):**
  - Added field rules files to the "read content type" ignore file set.

- **cli-variants (v2.0.0-beta.7):**
  - Resolved errors occurring during [Experience import](/docs/headless-cms/import-content-using-the-cli/) when variants reference Lytics audiences.

- **Dependency Updates:**
  - Upgraded dependency packages across the following plugins:
    - **cli-auth (v2.0.0-beta.6)**
    - **cli-cm-bootstrap (v2.0.0-beta.10)**
    - **cli-cm-branches (v2.0.0-beta.1)**
    - **cli-cm-clone (v2.0.0-beta.11)**
    - **cli-cm-export-to-csv (v2.0.0-beta.1)**
    - **cli-cm-import-setup (v2.0.0-beta.5)**
    - **cli-cm-seed (v2.0.0-beta.9)**
    - **cli-migration (v2.0.0-beta.6)**
