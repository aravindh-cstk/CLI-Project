# Recommended Module Order for Bulk CLI Export and Import

The customer exported entries and assets from a stack using the CLI but was unable to successfully re-import the data, and requested a clear step-by-step guide.

**Root cause**

Modules do need to be imported in a specific order for dependencies to resolve correctly (for example, entries reference assets, so assets must exist in the destination stack before entries import). However, `csdx cm:stacks:import` enforces this order automatically when it runs a full import (no `--module` flag): the CLI loops through its built-in module list and imports each module in that fixed order. Manual ordering only matters when modules are imported one at a time with `--module`, for example when only entries and assets were exported and each is re-imported as a separate command. In that case, the CLI does not re-order anything, so the person running the commands must invoke them in the correct sequence. If the module order is correct and a bulk re-import still fails, check for missing or mismatched management token scopes on the destination stack, or for conflicting UIDs on locales or content types that already exist there, since these cause more re-import failures than module order alone.

**Resolution**

1. Install the CLI: npm install -g @contentstack/cli. The CLI requires Node.js 22 or later, so confirm the installed Node.js version meets that requirement before running exports or imports.

2. Generate the required management tokens and confirm access rights on both the source and destination stacks.

3. Run the export command using the source stack's API key.

4. Run the import command using the destination stack's token and API key, pointing to the same export directory.

5. If running a full import (no `--module` flag), the CLI already applies the correct module order internally, so no manual sequencing is needed. If importing modules individually with `--module`, run them in this order: locales, environments, assets, taxonomies, extensions, marketplace-apps, webhooks, global-fields, content-types, workflows, entries, labels, custom-roles.

Following the installation prerequisites and, for per-module imports, the module order above resolves failed re-imports and completes the bulk upload successfully. For a full-stack import, running `csdx cm:stacks:import` once without `--module` is sufficient since the tool sequences modules for you.

*Note: This exact question and resolution also appears in similar_qs_CLI.csv, indicating it's a recurring question. It was verified against CLI.md directly and does not duplicate any published article there.*

*Source ticket: Case 45968*
