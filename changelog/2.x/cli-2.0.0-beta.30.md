# CLI Version 2.0.0-beta.30

2026-07-27

**Enhancements:**

- Made the `launch` plugin opt-in, it is no longer bundled with the CLI. Install it using `csdx plugins:install @contentstack/cli-launch` to use launch commands in **CLI (v2.0.0-beta.30)**.

- Added the `readGlobalFieldSchemas` utility function in **cli-utilities (v2.0.0-beta.12)**.

- Automatically refreshed region configurations set on older CLI versions with the latest endpoint data upon the next command execution, eliminating the need to manually run `config:set:region` in **cli-utilities (v2.0.0-beta.12)**.

- Updated the `config:set:region` command to store the full endpoint set for the selected region, making any future Contentstack endpoints available without requiring a command re-run in **cli-config (v2.0.0-beta.15)**.

- Switched global fields to a per-file export/import format in the following CLI plugins:
  - **cli-export (v2.0.0-beta.25)**
  - **cli-import (v2.0.0-beta.25)**
  - **cli-audit (v2.0.0-beta.16)**
  - **cli-import-setup (v2.0.0-beta.19)**

- Added global field rule handling to content types in **cli-import (v2.0.0-beta.25)**.

- Added `addHeader` to the publish-entries chain in **cli-import (v2.0.0-beta.25)**.

- Enhanced the field rules audit to include global fields in **cli-audit (v2.0.0-beta.16)**.

- Enhanced Asset Management (AM) with asset publishing support in **cli-asset-management (v1.0.0-beta.8)**.

- Forced `api_version=3.2` on all entry and asset publish/unpublish call sites in the following CLI plugins:
  - **contentstack-external-migrate (v2.0.0-beta.4)**
  - **cli-bulk-operations (v2.0.0-beta.5)**

- Hardened the NRP header on taxonomy publish and fixed `include-variants` validation in **cli-bulk-operations (v2.0.0-beta.5)**.

**Bug & Security Fixes:**

- Reconciled completed progress bar counts with processed items in **cli-utilities (v2.0.0-beta.12)**.

- Resolved an issue where resolving the org plan or auth host would fail hard when not explicitly configured, and successfully derived it from the existing region host as a fallback in **cli-utilities (v2.0.0-beta.12)**.

- Fixed context setting issues in **cli-command (v2.0.0-beta.11)**.

- Fixed an issue to add global fields Field Validation Rules (FVRs) in exports in **cli-export (v2.0.0-beta.25)**.

- Fixed an issue by collecting all locales and deduplicating asset UIDs in the bulk payload in **cli-bulk-operations (v2.0.0-beta.5)**.

- Updated dependency versions in the following CLI plugins:
  - **cli-auth (v2.0.0-beta.17)**
  - **cli-command (v2.0.0-beta.11)**
  - **cli-config (v2.0.0-beta.15)**
  - **apps-cli (v2.0.0-beta.5)**
  - **cli-cm-bootstrap (v2.0.0-beta.25)**
  - **cli-cm-branches (v2.0.0-beta.11)**
  - **cli-cm-regex-validate (v2.0.0-beta.4)**
  - **contentstack-cli-tsgen (v5.0.0-beta.4)**
  - **cli-cm-clone (v2.0.0-beta.26)**
  - **contentstack-cli-content-type (v2.0.0-beta.3)**
  - **cli-cm-export-to-csv (v2.0.0-beta.12)**
  - **cli-cm-migrate-rte (v2.0.0-beta.10)**
  - **cli-migration (v2.0.0-beta.17)**
  - **cli-cm-export-query (v2.0.0-beta.9)**
  - **cli-cm-seed (v2.0.0-beta.25)**
  - **cli-variants (v2.0.0-beta.20)**
