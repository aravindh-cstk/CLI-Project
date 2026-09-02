# CLI Version 2.0.0-beta.27

2026-07-06

**Enhancements:**

- Upgraded dependencies for the following plugins:
  - `cli-cm-clone (v2.0.0-beta.23)`
  - `cli-cm-seed (v2.0.0-beta.22)`
  - `cli-cm-export-query (v2.0.0-beta.6)`
  - `cli-cm-bootstrap (v2.0.0-beta.22)`
  - `cli-cm-import-setup (v2.0.0-beta.16)`

- Improved API key validation in `cli-cm-export (v2.0.0-beta.22)`.

- Updated and removed short flags across the following plugins:
  - `apps-cli (v2.0.0-beta.2)`
  - `contentstack-cli-tsgen (v5.0.0-beta.2)`
  - `cli-external-migrate (v2.0.0-beta.1)`
  - `cli-migration (v2.0.0-beta.15)`
  - `cli-cm-regex-validate (v2.0.0-beta.2)`
  - `cli-auth (v2.0.0-beta.15)`
  - `cli-config (v2.0.0-beta.13)`

**Bug & Security Fixes:**

- Fixed an issue to ensure login errors are displayed on the console and improved core API key validation.
- Fixed an issue to successfully display the backup folder path upon command completion.
- Fixed and improved API key validation specifically in `cli-cm-import (v2.0.0-beta.22)`.
