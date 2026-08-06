# References Not Populated in Parent Entries After Import: Reference UID Mismatch

After a CLI export/import, reference fields inside a specific content type's entries (product carousel references) were not linked in the parent entries, even though the carousel entries themselves imported successfully. Reinstalling the CLI and retrying with a previous version did not resolve it.

**Root cause**

A reference UID mismatch is the correct diagnosis here.

Here's how `cm:stacks:import` works in terms of resolving references:

- **Two-pass process:** The CLI imports entries in two passes. In the first pass, it creates each entry and records the mapping from the old (source) UID to the new (destination) UID in your `--backup-dir` folder.
- **Updating references:** In the second pass, it tries to rewrite all reference fields in every entry, looking up each referenced UID in that same mapping file.
- **Missing mappings:** If a referenced entry's old UID is *not* present in the mapping when the second pass runs, the CLI cannot resolve it. The result: the reference field is left pointing at a UID that doesn't exist in the destination stack. This causes the exact symptom where carousel entries appear to be successfully imported, but the reference field in the parent entries is not linked.

**Common causes of a missing mapping for one content type:**
- The referenced content type’s entries were imported during a separate `cm:stacks:import` run, but with a different (or no) `--backup-dir`, so their UID mapping didn’t make it into the mapping file the parent entries' update pass reads.
- Some referenced entries failed to import and were logged as failures, so they never got added to the mapping.

**Other cases that can cause symptoms:**
- Parent and carousel content types were imported into different branches.
- Carousel entries were later deleted and recreated in the destination stack (outside of the CLI).
- In these cases, even if the mapping file exists, it may point to destination UIDs that no longer exist, so the references still fail, even without a true mapping mismatch.

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
