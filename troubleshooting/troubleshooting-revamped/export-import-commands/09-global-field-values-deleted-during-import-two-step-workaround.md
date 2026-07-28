# Global Field Values Deleted During CLI Import: Two-Step Import Workaround

During a content migration using cm:stacks:import with a backup directory created by import-setup, a field inside a Global Field (implemented via a Marketplace App/Extension) was deleted from the content model in the destination stack. Because the Global Field was shared across multiple content types, this caused a temporary loss of that field stack-wide.

**Root cause**

Close, with one correction to where the "source of truth" actually lives. The global fields import step reads the global field schema it pushes to the destination stack from your `--data-dir` export folder, not from the backup folder. The backup folder created by `import-setup` (or passed via `--backup-dir`) only holds mapping metadata: UID mappings and success and failure logs. This is why editing the local schema files directly did not reliably prevent the issue: the edits most likely went into the backup/mapping folder rather than into the `--data-dir` export content. If a field is edited in the backup folder rather than in the export content, the import never sees that edit, since it reads schema content from your export data, not the backup folder. The backup folder itself is not reused or overwritten between runs in a way that would explain lost edits, since each `import-setup` run creates a new, separately named backup folder.

The actual deletion mechanism is the `--replace-existing` flag. When `cm:stacks:import` runs with `--replace-existing` and a global field with the same UID already exists in the destination stack, the CLI performs a full schema replace using the global field schema exactly as it appears in your export data, for that specific global field. Any field present in the destination's current schema but absent from that exported data is not preserved by this replace, so it disappears from the global field, and since the global field is shared across content types, every content type using it loses the field at once. This reproduces any time the exported global field data does not include a field that the destination stack's copy of that global field has, for example because the field was added directly in the destination after the export was taken, or the source stack never had the extension installed at export time.

**Resolution**

1. Run the import for assets first, so they exist in the destination stack and are available for referencing:

csdx cm:stacks:import ... --module=assets

2. Then run the import for entries only:

csdx cm:stacks:import ... --module=entries

Splitting the import into an assets-only pass followed by an entries-only pass works because `--module` restricts `cm:stacks:import` to that one module, so the global-fields import step never runs in either step. The existing global field schema in the destination stack, extension field included, is left completely untouched. This is a reliable way to avoid the schema replacement, not a side effect of import order.

3. If instead the global field schema needs to be edited directly, make the edit in your `--data-dir` export folder before running `cm:stacks:import --replace-existing`. Editing a copy in the backup folder has no effect on the imported schema.

A more direct fix, if a full combined import is still needed, is to either drop `--replace-existing` for the run (so the CLI only creates global fields that do not yet exist, and never replaces ones that do) or make sure the exported global field data actually contains the extension field before importing with `--replace-existing`, for example by re-exporting from a source stack where the Marketplace App or Extension is installed and the field is present.

*Source ticket: Case 56285*
