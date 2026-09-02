# CLI Version  1.59.0

2026-03-03

**Enhancements:**

- **cli-bulk-operations (v1.0.0):**
  - Implemented non-localized filter support in bulk-entries.
  - Added a method to fetch the master locale when using the non-localize filter.
  - Added pagination support for locales.

- **cli-audit (v1.18.0):**
  - Added validation for referenced entry content types during entries audit.

**Bug & Security Fixes:**

- **cli-variants (v1.3.8):**
  - Fixed an issue to filter Lytics audiences in experience variants during [import](/docs/headless-cms/import-content-using-the-cli/).
