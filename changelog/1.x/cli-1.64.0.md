# CLI Version 1.64.0

2026-06-29

**Enhancements**

- **Node.js 22 Runtime Migration:** Upgraded the Node.js runtime version to v22 across all CLI plugins and updated the corresponding documentation.

- **ESLint Infrastructure Upgrade:** Upgraded ESLint to v10.50.0 and migrated all plugin configurations to the new flat config format.

- **Dependency and Plugin Updates:** Rolled out the runtime and linting enhancements across the following plugin versions:
  - `cli-audit v1.19.5`
  - `cli-cm-export v1.25.2`
  - `cli-cm-import v1.33.4`
  - `cli-auth v1.8.4`
  - `cli-cm-bootstrap v1.19.7`
  - `cli-cm-branches v1.8.3`
  - `cli-cm-bulk-publish v1.12.1`
  - `cli-cm-clone v1.21.8`
  - `cli-cm-export-to-csv v1.12.5`
  - `cli-cm-import-setup v1.8.5`
  - `cli-cm-migrate-rte v1.7.1`
  - `cli-cm-seed v1.15.7`
  - `cli-command v1.8.4`
  - `cli-config v1.20.5`
  - `cli-migration v1.12.4`
  - `cli-utilities v1.18.5`
  - `apps-cli v1.7.1`
  - `cli-bulk-operations v1.2.1`
  - `cli-cm-regex-validate v1.0.1`
  - `contentstack-cli-tsgen v4.10.1`
  - `contentstack-cli-content-type v1.5.1`
  - `cli-external-migrate v1.0.0-alpha.4`
  - `cli-cm-export-query v1.0.4`

**Bug Fixe**

- **Organization User Pagination:** Resolved pagination bugs within the organization user fetch logic (`cli-cm-export-to-csv v1.12.4`).
