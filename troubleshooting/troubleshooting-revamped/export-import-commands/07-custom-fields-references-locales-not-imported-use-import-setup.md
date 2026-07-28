# Custom Fields, References, or Locales Not Imported Correctly: Use import-setup First

After a CLI import, several problems appeared together: a custom field (implemented via a Developer Hub app) wasn't populated even though it existed in the export JSON, reference fields for one content type weren't linked in the parent entries, and localized content was created as separate full entries instead of localized versions of the original entry. Running the stack import without specifying a backup directory also caused certain fields to be dropped from the content model entirely.

**Root cause**

Running import-setup first does help, but not for the reason originally stated. `cm:stacks:import` reads two different things from two different places:

1. The actual content payload for each module (content types, global fields, entries) comes from your `--data-dir` export folder.
2. Cross-module reference data, such as the mapping between old and new UIDs for extensions, marketplace apps, global fields, and entries, is read from and written to your `--backup-dir` folder.

When you run `cm:stacks:import` without `--backup-dir`, the CLI creates a fresh, empty backup folder each time, so none of those UID mappings exist yet. That's why a custom field's extension reference or a cross-content-type reference can fail to resolve on that run. Running `cm:stacks:import-setup` first does help, and it does more than just create an empty folder: for the module(s) you specify (content types, entries, or global fields), it generates the mapper files that record how source items correspond to what's already in the destination stack, and it creates the backup folder and branch configuration that the main import reads from and writes to. That gives the subsequent `cm:stacks:import --backup-dir <path>` run a real, populated folder to resolve UID mappings against, and to keep reusing across repeated runs, instead of starting from a throwaway empty one each time.

**Resolution**

1. Run the setup command first to create the backup directory that the main import will read and write UID mappings into:

csdx cm:stacks:import-setup -k <stack_api_key> -d ./export/main --module entries

2. Then run the import using that backup directory and the replace option, so the mappings persist across runs instead of resetting:

csdx cm:stacks:import -k <stack_api_key> -d ./export/main --backup-dir ./_backup_123 --replace-existing --module entries

3. Import any Marketplace Apps used by custom fields, and do this before importing the content types or entries that depend on them, so their UID mapping already exists in the backup folder when those content types and entries are imported:

csdx cm:stacks:import -k <stack_api_key> -d ./export/main --backup-dir ./_backup_123 --module marketplace-apps

Running `cm:stacks:import-setup` before the main import, and always pointing `cm:stacks:import` at the same `--backup-dir`, gives every module a persistent place to read and write its UID mappings, which is what actually resolves custom field population and cross-module references. It does not, by itself, change how localized entries are created. If localized entries still appear as separate full entries instead of localized versions of the original, confirm that the master-locale entry for each source entry finished importing and was mapped before the CLI processed other locales, since import order between locales affects this. If the custom field itself is missing from the exported content type or global field data (for example, because the field was added directly in the destination stack after the export was taken), no combination of `import-setup` or `--backup-dir` resolves that. Confirm the field exists in the export data before troubleshooting the import step further. (Reference-linking issues specific to one content type in this case required additional investigation. See the following article on reference UID mismatches.)

*Source ticket: Case 53894*
