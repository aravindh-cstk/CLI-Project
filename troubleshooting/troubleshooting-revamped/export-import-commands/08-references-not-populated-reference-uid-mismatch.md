# References Not Populated in Parent Entries After Import: Reference UID Mismatch

After a CLI export/import, reference fields inside a specific content type's entries (product carousel references) were not linked in the parent entries, even though the carousel entries themselves imported successfully. Reinstalling the CLI and retrying with a previous version did not resolve it.

**Root cause**

A reference UID mismatch is the right general diagnosis. `cm:stacks:import` resolves entry references in two passes. It first creates each entry and records the mapping from the old (source) UID to the new (destination) UID in your `--backup-dir` folder. In a second pass, the CLI rewrites every entry's reference fields by looking up each referenced UID in that same mapping. If a referenced entry's old UID is not present in the mapping at the time this second pass runs, the CLI cannot resolve it, and the reference field is left pointing at a UID that does not exist in the destination stack, which is exactly the "carousel entries imported, but the reference did not link" symptom. The most common reason the mapping is missing for one content type specifically: the referenced content type's entries were imported in a separate `cm:stacks:import` run that used a different (or no) `--backup-dir`, so its UID mapping never landed in the same mapping file the parent entries' update pass reads, or some of the referenced entries failed to import and were logged as failures instead of being added to the mapping. If the parent and carousel content types were imported into different branches, or the carousel entries were later deleted and recreated in the destination stack outside the CLI, the mapping file will point to destination UIDs that no longer exist, producing the same symptom even though the mapping itself was never actually mismatched.

For this exact situation, once the referenced entries, assets, or extensions already exist in the destination stack but their UIDs were not updated in the referring entries, Contentstack provides a documented migration script that updates those missing reference UIDs without requiring a full re-import.

**Resolution**

1. Confirm the export/import logs show the referenced (carousel) entries were created successfully in the destination stack, and check the failed-entries log in your `--backup-dir` folder for that content type to rule out import failures.

2. Open the entries UID mapping file under your `--backup-dir` folder and confirm it contains an entry for each old carousel-entry UID referenced by the parent entries. If entries were imported in a separate run with a different backup folder, re-import using the same `--backup-dir` for both content types so both sets of UID mappings live in the same mapping file.

3. Download the `examples` folder from the CLI's migration package on GitHub (in the `contentstack/cli` repository, under `packages/contentstack-migration/examples`), and navigate to it in your terminal.

4. Create a `config.json` file in that folder with two keys:
   - `mapper-path`: the path to the backup directory where the import logs are stored, for example `<path>/_backup_<number>/`.
   - `contentTypes`: an array of the content type UIDs whose references need to be updated, for example the parent content type that contains the carousel reference field.

5. Run the `05-Update-reference-entry-from-mapper` script from the examples folder using the migration command:

csdx cm:stacks:migration --file-path ./05-Update-reference-entry-from-mapper.js --config-file ./config.json -k <stack_ApiKey>

6. Validate that the previously unlinked reference fields now populate correctly in the parent entries. If they still don't, check whether the referenced entries still exist in the destination stack under the same UIDs recorded in the mapping, since entries deleted and recreated outside the CLI will not match, and confirm the `contentTypes` array in `config.json` includes the correct parent content type.

Making sure both the parent content type and the referenced (carousel) content type were imported against the same `--backup-dir`, so their UID mappings live in one mapping file, is the first thing to check. Running the `05-Update-reference-entry-from-mapper` script against that backup directory's mapper path is the documented way to update the missing reference UIDs afterward, without repeating the full import.

*Source ticket: Case 54012*
