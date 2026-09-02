# CLI Version 2.0.0-beta.16

2026-03-16

**Enhancements:**

- **contentstack-utilities (v2.0.0-beta.3):**
  - Updated the major version of inquirer for improved interactive CLI prompts.
  - Added NO_PROXY support in the environment file for better network configuration control.

- Updated the major version of inquirer in the following plugins:
  - **contentstack-bootstrap (v2.0.0-beta.12)**
  - **contentstack-clone (v2.0.0-beta.13)**
  - **contentstack-export-to-csv (v2.0.0-beta.3)**
  - **contentstack-seed (v2.0.0-beta.11)**

**Bug & Security Fixes:**

- **contentstack-audit (v2.0.0-beta.7):**
  - Fixed issues related to the progress manager and audit summary display in the audit command.

- Resolved security vulnerabilities by upgrading dependencies in the following:
  - **types-generator (v3.9.3)**
  - **contentstack-cli-tsgen (v4.8.2)**
  - **cli-bulk-operations (v1.0.1)**
  - **contentstack-cli-content-type (v1.4.2)**
