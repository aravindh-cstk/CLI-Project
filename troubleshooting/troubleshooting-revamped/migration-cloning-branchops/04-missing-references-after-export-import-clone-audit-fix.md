# Missing References After Export/Import or Clone: Resolving with Audit Fix

After performing export to import between stacks, and again after using the CLI clone command, the customer found that references were missing, with clone update failures showing no clear error messaging.

**Root cause**

Entries in the exported content reference other entries (or content types) by UID, and those referenced targets did not exist in the target stack, for example because the referenced entry was deleted, not part of the exported module set, or referenced a content type not allowed by the field's `reference_to` list. `cm:stacks:audit` and `cm:stacks:audit:fix` (from `@contentstack/cli-audit`) check the reference fields in your exported data (the `--data-dir` folder), not the live target stack, so they catch references pointing at UIDs that don't exist in the exported content. `cm:stacks:clone` runs this same audit internally as part of the import step it performs after exporting, which is why the same class of error shows up for both plain export/import and clone.

A reference can also be flagged as broken even when the referenced entry exists, if that entry's content type isn't in the field's `reference_to` list. Contentstack treats this the same way as a fully missing reference. Similarly, if a referenced module (for example assets, or a specific content type) was excluded from the export using `--module` or `--content-types` filters, the reference breaks purely because of the export scope, not because of data corruption.

**Resolution**

1. Run `csdx cm:stacks:audit:fix` (or let `cm:stacks:import`/`cm:stacks:clone` run it automatically, since both invoke audit fix on the exported data before importing) against the exported content directory, not the target stack.

2. Import the corrected content into the target stack.

3. Review the audit report at the path the command prints. Audit fix does not restore or recreate the missing referenced entries. It removes the invalid UID from the reference field so the entry can be created or updated without the import failing. This removes the broken reference rather than making it resolve to real content. If the referenced content is supposed to exist, verify the missing entries in the exported data or the source stack, and re-export or manually recreate them, then re-run the audit and import.

Running audit fix before import prevents the import failures caused by broken references, and the customer confirmed the improvement. It does not, on its own, restore the missing referenced content, if the target entries genuinely do not exist, they need to be located or recreated separately.

*Source ticket: Case not recorded in source data (row had a blank Case Number field)*
