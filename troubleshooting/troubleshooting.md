# Contentstack CLI — New Troubleshooting Articles

This batch covers gap-coverage articles generated from raw support ticket data, cross-checked against the existing CLI.md knowledge base to avoid duplication. Every article traces to a specific source case number.

# Migration, Cloning & Branch Operations (New Articles)

**Meta Title:** Contentstack CLI Migration, Cloning, and Branch Troubleshooting | Contentstack

**Meta Description:** Resolve CLI migration order issues, missing references after export/import, branch merge errors, and duplicate-title renaming problems.

**URL:** 

**Section:** 

**Subsection:** 

## 1\. Import Content from a GitHub Repository Using the CLI Seed Command

The customer wanted to import content directly from a GitHub repository into Contentstack and asked for the correct method.

**Root cause**

Content stored in an external GitHub repository cannot be imported directly; it must be hosted in a public repository and pulled in using the CLI's Seed command, which supports importing from non-Contentstack GitHub sources.

**Resolution**

1. Prepare and export the source stack content.

2. Upload the exported content to a public GitHub repository.

3. Run the CLI Seed command to import the content from the GitHub repository into the target stack.

Content from the GitHub repository imports successfully into the target stack using the Seed command.

*Source ticket: Case 40919*

## 2\. Recommended Order for Migrating Content Types Between Stacks

The customer asked for the correct order to follow when migrating content types and entries from one stack to another.

**Root cause**

Migrating modules out of order can cause dependency failures — content types may reference Marketplace App configurations or global fields that don't yet exist in the target stack.

**Resolution**

1. Import Marketplace Apps into the target stack first.

2. Update and configure those apps as needed.

3. Import content types and global fields.

4. Finally, migrate entries and any remaining modules.

Following this order avoids dependency errors, and all modules migrate into the target stack correctly.

*Source ticket: Case 43220*

## 3\. Migrating Entries Between Branches Using Migration Scripts

The customer asked how to migrate entries from one branch to another within the same stack.

**Root cause**

Branch-to-branch entry migration is not a single built-in CLI command; it is accomplished using Contentstack migration scripts, which give scripted, controlled movement of entries between branches.

**Resolution**

1. Use Contentstack migration scripts (run via csdx cm:stacks:migration) to move entries from the source branch to the destination branch rather than looking for a single built-in "move branch" command.

2. Refer to the Contentstack migration script documentation for the general script structure and execution steps.

3. Test the script against a non-production branch first, and confirm entries appear correctly in the destination branch before relying on it for production data.

Support confirmed migration scripts are the correct tool for branch-to-branch entry migration, and the customer acknowledged the guidance and confirmed they would proceed. This ticket's notes describe the recommended approach at a high level; they do not include a specific script example.

*Source ticket: Case 43819*

## 4\. Missing References After Export/Import or Clone: Resolving with Audit Fix

After performing export → import between stacks, and again after using the CLI clone command, the customer found that references were missing, with clone update failures showing no clear error messaging.

**Root cause**

Dependency inconsistencies within the exported content caused reference fields to fail to resolve correctly in the target stack, both during export/import and during cloning.

**Resolution**

1. Run the audit fix command against the target stack to repair structural inconsistencies in the imported content.

2. Re-import the entries after the audit fix completes.

3. Verify that previously broken references now resolve correctly.

Running audit fix followed by re-import resolved the majority of the reference errors, and the customer confirmed the improvement.

*Source ticket: Case not recorded in source data (row had a blank Case Number field)*

## 5\. Applications Renamed with "?1" After Import (Duplicate Titles on Older CLI Versions)

After importing a stack, the customer found that all of their applications had been renamed with "?1" appended, and in many cases the names were truncated.

**Root cause**

The customer was using an older CLI version (1.12.0). When importing a stack, that version suggests a modified name with a "?1" suffix for any duplicate application titles. Because the import command was run with the \-y flag, these suggested renamed values were auto-accepted without manual review.

**Resolution**

1. Confirm the CLI version in use with csdx \--version, and update to the latest version.

2. Before importing, check the source stack for duplicate application titles and rename them to be unique.

3. Avoid the \-y flag when duplicate titles may be present, so renamed suggestions can be reviewed before being accepted.

Once duplicate titles are resolved and renamed suggestions are reviewed manually (or the CLI is updated), imported applications retain their intended names.

*Source ticket: Case 44445*

## 6\. Branch Merge Fails with Error Code 116 (Global Fields: Failed to Fetch Global Fields)

While attempting to merge branches, the customer received Error Code 116 — "Global Fields: Failed to fetch global fields" — and the merge process failed.

**Root cause**

An outdated field visibility rule had been removed in one branch but did not migrate correctly from staging to main, even though it had migrated correctly from develop to staging. This inconsistency in field visibility rules across environments blocked the merge.

**Resolution**

1. Review field visibility rules for global fields across the branches involved in the merge.

2. Identify and manually remove the outdated field visibility rule in the main branch.

3. Re-run the branch merge.

After removing the outdated field visibility rule, the branch merge completed successfully.

*Source ticket: Case 47200*

# Migration Tool (GUI) Login & Access

**Meta Title:** Troubleshoot Contentstack Migration Tool Login Issues | Contentstack

**Meta Description:** Resolve login failures in the Contentstack GUI migration tool caused by insufficient permissions, region mismatches, or SSO Strict Mode.

**URL:** 

**Section:** 

**Subsection:** 

## 1\. Migration Tool Login Fails Due to Insufficient Org-Level Permissions

The customer was unable to log in to the Contentstack migration tool and requested help understanding why access was failing.

**Root cause**

The migration tool requires Org-level Admin or Owner permissions. The user had Admin access only at the stack level, with a Member role at the org level, which blocked login. The user was also attempting to log in via the wrong region.

**Resolution**

1. Ask your Org Admin or Owner to update your role to Admin or Owner at the organization level.

2. Confirm you are logging in using the correct region for your organization (for example, AWS NA rather than Azure EU).

3. Retry logging in to the migration tool.

Login succeeds once org-level Admin/Owner permissions are granted and the correct region is used.

*Source ticket: Case 45213*

## 2\. GUI Migration Tool Login Blocked by SSO Strict Mode

The customer could not log in to the GUI migration tool because it requires a standard Contentstack username and password, but their organization uses SSO without a Contentstack password.

**Root cause**

Organizations with SSO Strict Mode enabled prevent password-based logins entirely, which blocks access to the migration tool since it does not yet support SSO authentication.

**Resolution**

1. Option A: Temporarily disable SSO Strict Mode so the user can set a standard Contentstack password, then log in to the migration tool.

2. Option B: Create a separate non-SSO user account with a standard password dedicated to migration tasks.

3. Re-enable Strict Mode (if disabled) once the migration work is complete.

The user is able to log in to the migration tool using either workaround. Native SSO support for the migration tool is on the product roadmap but not yet available.

*Source ticket: Case 43946*

# Export/Import Commands & Data Handling (New Articles)

**Meta Title:** Fix Additional Contentstack CLI Export and Import Issues | Contentstack

**Meta Description:** Resolve management token export failures, unsupported bulk republishing, custom export filtering limitations, and data constraint questions.

**URL:** 

**Section:** 

**Subsection:** 

## 1\. CLI Stack Export Fails with "No Management Token Found on Given Alias"

CLI stack export failed with the error "No management token found on given alias \<alias\>" even though the customer confirmed the management token existed on the stack.

**Root cause**

The management token existed on the stack but was not registered in the CLI's local token store under that alias, so the CLI could not resolve it during export.

**Resolution**

1. Register the management token in the CLI with the correct alias:

csdx auth:tokens:add \--management \--alias \<alias\> \--stack-api-key \<stack\_api\_key\> \--token \<management\_token\> \--branch \<branch\_name\>

2. Confirm the alias was registered correctly:

csdx auth:tokens:list

3. Re-run the export command:

csdx cm:stacks:export \--stack-api-key \<stack-api-key\> \--data-dir "\<path\>" \--alias \<alias\>

After registering the management token under the correct alias, csdx cm:stacks:export runs successfully.

*Source ticket: Case 45251*

## 2\. Recommended Module Order for Bulk CLI Export and Import

The customer exported entries and assets from a stack using the CLI but was unable to successfully re-import the data, and requested a clear step-by-step guide.

**Root cause**

Bulk export/import requires the CLI to be installed with the correct prerequisites, and modules must be imported in a specific order for dependencies to resolve correctly.

**Resolution**

1. Install the CLI: npm install \-g @contentstack/cli (requires Node.js v16 or later).

2. Generate the required management tokens and confirm access rights on both the source and destination stacks.

3. Run the export command using the source stack's API key.

4. Run the import command using the destination stack's token and API key, pointing to the same export directory.

5. Import modules in this order: locales, environments, assets, extensions, global fields, content types, and finally entries.

Following the installation prerequisites and the recommended import order resolves failed re-imports and completes the bulk upload successfully.

*Note: This exact question and resolution also appears in similar\_qs\_CLI.csv, indicating it's a recurring question. It was verified against CLI.md directly and does not duplicate any published article there.*

*Source ticket: Case 45968*

## 3\. CLI Export Hangs for Large Content Types with Nested References

Exporting a large content type (\~85,000 records with multiple references and arrays) using csdx cm:export-to-csv hung indefinitely, while smaller content types exported successfully.

**Root cause**

export-to-csv is not optimal for very large, reference-heavy datasets; nested references and high record counts cause the command to hang rather than complete.

**Resolution**

1. Use csdx cm:stacks:export to export the content in JSON format instead, which handles large datasets more reliably.

2. Explicitly include all referenced content types using the \--content-types flag to ensure completeness.

3. Convert the exported JSON to CSV afterward with a script, if a CSV file is still required.

Exporting large, reference-heavy content types as JSON via cm:stacks:export completes reliably where export-to-csv previously hung. This case was also escalated to CLI engineering to evaluate improvements for large dataset exports.

*Source ticket: Case 46907*

## 4\. No Support for Custom Filtered Exports via CLI

The customer asked whether Contentstack supports exporting a custom filtered view of entries directly, rather than exporting an entire content type.

**Root cause**

The CLI does not offer a custom filtered export option; export operations work at the content-type level.

**Resolution**

1. Export all entries of the relevant content type to CSV using the CLI.

2. Apply the required filters or formulas to the exported CSV file after the export completes.

The customer is able to get the filtered dataset they need by applying filters to the exported CSV, since Contentstack does not currently support exporting a pre-filtered view.

*Source ticket: Case 50983*

## 5\. Bulk Re-Publishing Entries Is Not Supported via CLI

The customer asked whether it is possible to bulk re-publish already-published entries for a specific content type on the main branch using the CLI, or whether SDK usage is required.

**Root cause**

The Contentstack CLI does not support this specific bulk re-publishing scenario.

**Resolution**

1. Use the Contentstack Management SDK instead of the CLI for this use case.

2. Query all entries of the target content type.

3. Fetch each entry along with its publish details.

4. Re-publish each entry to the required environment(s) and locale(s) using its latest version.

A Management SDK script covering these steps successfully bulk re-publishes previously published entries for the target content type.

*Source ticket: Case 44338*

## 6\. Title Field Cannot Be Made Non-Unique

The customer asked whether the title field on entries can be configured as non-unique.

**Root cause**

The title field is unique by default in Contentstack and is not configurable to allow non-unique values.

**Resolution**

No configuration change is available for this. If entries need a non-unique display label alongside a unique title, add a separate custom field for that purpose rather than trying to make the title field non-unique.

*Note: This exact question and answer also appears in similar\_qs\_CLI.csv, indicating it's a recurring question. It was verified against CLI.md directly and does not duplicate any published article there.*

*Source ticket: Case 43563*

# CLI Performance, Rate Limits & Known Version Issues

**Meta Title:** Troubleshoot Contentstack CLI Performance and Version Issues | Contentstack

**Meta Description:** Resolve CLI rate limit errors during cloning, hidden log output during migrations, and known version-specific bugs.

**URL:** 

**Section:** 

**Subsection:** 

## 1\. Rate Limit Errors During cm:stacks:clone

The customer encountered rate limit exceeded errors while running cm:stacks:clone, resulting in incomplete clones. They also asked whether the CLI supports cloning only a subset of languages/locales.

**Root cause**

The CLI does not include built-in throttling or automatic retries for cloning, export, or import operations. When a rate limit error occurs, the process stops, which can result in missing entries, assets, or configurations. Selective cloning of a subset of locales is also not supported — cm:stacks:clone always clones all locales and content.

**Resolution**

1. Expect that a rate limit error will stop the clone process rather than retry automatically; review the output carefully for any incomplete sections.

2. If fewer locales are needed, clone all locales as usual, then manually remove the unwanted locales afterward — the CLI does not support cloning a subset directly.

3. If clones are frequently interrupted by rate limits, space out large clone operations or run them during lower API-traffic periods.

This is expected CLI behavior rather than a bug. Manual post-clone cleanup and awareness of the lack of retries lets the customer work around the current limitations.

*Source ticket: Case 45226*

## 2\. CLI Hides Log Output During Migration Runs

The customer reported that CLI log messages disappear while a migration is running.

**Root cause**

The CLI uses a progress spinner to indicate an ongoing migration, and the spinner updates the same terminal line using a carriage return. When console.log statements execute immediately before or during a spinner update, the spinner overwrites the log output before it can fully render.

**Resolution**

1. Add a newline character (\\n) at the beginning of each console.log statement in the migration script to force output onto a new line, for example: console.log('\\nMigration started...').

2. Be aware this introduces extra blank lines and may not be 100% reliable in all terminal environments or under heavy load.

Adding the leading newline prevents most log output from being overwritten by the spinner, making migration progress visible again.

*Source ticket: Case 46978*

## 3\. CLI v1.52 Breaks Taxonomy Export with Management Token Alias (Known Bug)

After upgrading to CLI v1.52, a taxonomy export command that previously worked in v1.51 with a management-token alias began failing with "Access denied. Please check your permissions."

**Root cause**

Engineering confirmed this is a known bug specific to CLI v1.52 affecting the taxonomy export command; it is not a permissions issue on the customer's stack.

**Resolution**

1. As an immediate workaround, downgrade the CLI to the previous stable version:

npm install \-g @contentstack/cli@1.51.0

2. Continue using the management-token alias as before; the same command works correctly on v1.51.

3. Watch for the patch release once it ships, then upgrade back to a fixed version.

Downgrading to CLI v1.51 immediately restores taxonomy export functionality. A permanent fix is planned in a future patch release.

*Source ticket: Case 51155*

# Migration, Cloning & Branch Operations (Additional Articles)

**Meta Title:** Troubleshoot Contentstack CLI Branch and Cloning Issues | Contentstack

**Meta Description:** Resolve branch-to-branch entry copying questions, false-positive branch diff results, and disk space limits when cloning large stacks.

**URL:** 

**Section:** 

**Subsection:** 

## 1\. Copying or Syncing Entries Between Branches (No Built-In Feature)

The customer asked how to copy or sync entries — including localized versions and references — from one branch to another, since no direct option was visible in the UI.

**Root cause**

Contentstack does not offer a single built-in feature to copy or sync entries between branches outside of manual UI actions. Bulk or reference-aware copying requires the Content Management API or the CLI, with custom scripting to handle localizations and references.

**Resolution**

1. For a single entry: copy manually via the UI, or use the Content Management API — copying all localizations for one entry requires a custom script that fetches each locale and recreates it in the target branch.

2. For bulk copying: use the CLI to export content from the source branch and import it into the target branch, or use the Content Management API with a custom script that queries all entries from the source branch and creates them in the target.

3. For entries containing references: copy referenced entries first, then the entries that reference them. Maintain a UID-mapping table and use a two-pass approach — copy first, then resolve and update references using the mapped UIDs.

Using CLI export/import or the Content Management API with a UID-mapping approach allows entries, localizations, and references to move between branches, even though no single one-click feature exists for this today.

*Source ticket: Case 53260*

## 2\. cm:branches:diff Shows a Field as Modified with No Visible UI Difference

Running cm:branches:diff to compare the prod and main branches showed a modification in a content type's URL field, but manually reviewing both branches in the UI showed no visible difference.

**Root cause**

The command was run with the \--format detailed-text option, which compares the complete field configuration, including metadata-level properties. Minor differences in metadata — internal configuration attributes, field settings, or other system-level properties not visible in the standard UI schema view — are still reflected in this detailed diff output.

**Resolution**

1. When cm:branches:diff \--format detailed-text reports a change with no visible UI difference, treat it as a metadata-level difference rather than a schema defect.

2. If only structural/visible schema differences matter for your review, compare using the default or summary diff format instead of detailed-text.

Understanding that detailed-text includes metadata-level comparison explains the discrepancy between the CLI diff output and the UI's schema view.

*Source ticket: Case 53530*

## 3\. Cloning a Large Stack Runs Out of Disk Space

The customer needed to clone a large stack (entries and assets), but the CLI cloning process consumed all available disk space and could not complete.

**Root cause**

cm:stacks:clone is the most reliable method currently available for cloning a stack, but for very large stacks its local storage requirements during the clone process can exceed available disk space. Cloning via the CDA or CMA APIs directly is not supported.

**Resolution**

1. Confirm available local disk space before starting a large clone, and free up space or run the clone from a machine/volume with sufficient headroom.

2. If disk space cannot be increased, replicate stack components (content types, entries, assets) manually as an alternative to a full clone — this requires more manual effort but avoids the disk space ceiling.

cm:stacks:clone remains the recommended approach when sufficient disk space is available; manual replication is the fallback when it is not.

*Source ticket: Case 54041*

# Export/Import Commands & Data Handling (Additional Articles)

**Meta Title:** Fix Contentstack CLI Import Field and Reference Issues | Contentstack

**Meta Description:** Resolve custom field import failures, missing carousel references, deleted Global Field values, and UI JSON import limits.

**URL:** 

**Section:** 

**Subsection:** 

## 1\. Custom Fields, References, or Locales Not Imported Correctly — Use import-setup First

After a CLI import, several problems appeared together: a custom field (implemented via a Developer Hub app) wasn't populated even though it existed in the export JSON; reference fields for one content type weren't linked in the parent entries; and localized content was created as separate full entries instead of localized versions of the original entry. Running the stack import without specifying a backup directory also caused certain fields to be dropped from the content model entirely.

**Root cause**

The import was run directly with cm:stacks:import without first generating mapper files via the import-setup command. Without that mapping step, the CLI cannot reliably track references and can mishandle custom fields and locale relationships during import.

**Resolution**

1. Run the setup command first to generate backup and mapping directories:

csdx cm:stacks:import-setup \-k \<stack\_api\_key\> \-d ./export/main \--module entries

2. Then run the import using the generated backup directory and the replace option:

csdx cm:stacks:import \-k \<stack\_api\_key\> \-d ./export/main \--backup-dir ./\_backup\_123 \--replace-existing \--module entries

3. If any Marketplace Apps used by custom fields are private, import them explicitly as well:

csdx cm:stacks:import \--module marketplace-apps

Running import-setup before the main import resolves custom field population, locale handling, and content-model field retention. (Reference-linking issues specific to one content type in this case required additional investigation — see the following article on reference UID mismatches.)

*Source ticket: Case 53894*

## 2\. References Not Populated in Parent Entries After Import — Reference UID Mismatch

After a CLI export/import, reference fields inside a specific content type's entries (product carousel references) were not linked in the parent entries, even though the carousel entries themselves imported successfully. Reinstalling the CLI and retrying with a previous version did not resolve it.

**Root cause**

The root cause was a reference UID mismatch introduced during migration — the UIDs recorded for the referenced entries did not line up with the UIDs actually created in the destination stack, so the reference fields could not resolve.

**Resolution**

1. Confirm the export/import logs show the referenced entries were created successfully in the destination stack.

2. Run the Update Missing Reference UIDs utility to reconcile reference relationships between the mapper output and the actual destination UIDs.

3. Validate that the previously unlinked reference fields now populate correctly in the parent entries.

Running the Update Missing Reference UIDs utility resolved the mismatch, and the product carousel references populated correctly in the parent entries after validation.

*Source ticket: Case 54012*

## 3\. Global Field Values Deleted During CLI Import — Two-Step Import Workaround

During a content migration using cm:stacks:import with a backup directory created by import-setup, a field inside a Global Field (implemented via a Marketplace App/Extension) was deleted from the content model in the destination stack. Because the Global Field was shared across multiple content types, this caused a temporary loss of that field stack-wide.

**Root cause**

The CLI's import synchronization treats the local schema files in the backup/modified folder as the source of truth for the destination stack. Because the affected field was missing or mismatched in the local globalfields.json file, the CLI removed it from the destination stack to match. The import-setup phase itself sometimes overwrote manual edits to these local schema files, so editing them directly did not reliably prevent the issue.

**Resolution**

1. Run the import for assets first, so they exist in the destination stack and are available for referencing:

csdx cm:stacks:import ... \--module=assets

2. Then run the import for entries only. Since the content model is already established in the destination stack and the assets already exist, this step populates data without re-syncing (and potentially stripping) the content model:

csdx cm:stacks:import ... \--module=entries

Splitting the import into an assets-only pass followed by an entries-only pass preserves the Global Field and its extension field, avoiding the schema deletion seen when running a full combined import. The precise reason the setup phase strips the extension field from the schema JSON was not fully root-caused, but this two-step workaround is confirmed stable.

*Source ticket: Case 56285*

## 4\. UI JSON Import Creates Only One Entry Even with Multiple Records in the File

The customer tried to import 500+ entries of the same content type using a single JSON file through the Contentstack UI's entry import option, but only one empty entry was created.

**Root cause**

This is expected behavior, not a bug: the Contentstack UI entry importer supports only a single entry per JSON file. It is not designed for bulk multi-record import.

**Resolution**

1. For bulk entry creation, use the Content Management API to programmatically create entries — this is the preferred approach for scalability.

2. Alternatively, use the Contentstack CLI, which supports bulk import through a structured export/import format.

Bulk entry creation succeeds using either the Content Management API or the CLI; the UI's JSON importer remains limited to one entry per file by design.

*Source ticket: Case 56501*

# CLI Performance, Rate Limits & Known Version Issues (Additional Articles)

**Meta Title:** Troubleshoot Contentstack CLI Memory and Rate Limit Errors | Contentstack

**Meta Description:** Resolve JavaScript heap out-of-memory errors, high-memory branch merges, and rate limit errors during CLI publishing and imports.

**URL:** 

**Section:** 

**Subsection:** 

## 1\. JavaScript Heap Out of Memory During Large Asset Migration

Migrating a large batch of assets (roughly 5,354 assets across 554 folders, totaling 5.53GB) from one stack to another consistently crashed at around 80% completion with a "JavaScript heap out of memory" error — even after significantly raising the Node.js memory limit with NODE\_OPTIONS=--max-old-space-size=30720.

**Root cause**

The failure persisted well below the allocated heap ceiling, which points to inefficient memory handling in the CLI's asset-processing logic for very large batches rather than a configuration problem on the customer's side.

**Resolution**

1. As a workaround, build a custom upload script against the already-exported asset files instead of relying on the CLI's built-in asset import for this batch size.

2. Deliberately limit request concurrency in the custom script to avoid overwhelming the API and to keep memory usage bounded.

A concurrency-limited custom upload script completed the asset migration successfully where the CLI's built-in import could not. This case was shared with Contentstack engineering to investigate the underlying memory behavior for large asset batches.

*Source ticket: Case 53631*

## 2\. CLI Command Fails with Heap Memory Error — Increase the Node.js Memory Limit

A CLI operation failed with a heap memory error during execution.

**Root cause**

The CLI runs on Node.js and inherits standard Node.js memory behavior, including the default \~4GB V8 heap limit on 64-bit systems. Operations on large datasets can exceed this default limit.

**Resolution**

1. Increase the heap limit using the standard Node.js memory flag, either by invoking the CLI directly:

node \--max-old-space-size=8192 \<csdx-bin\> ...

2. or by setting it as an environment variable before running the command:

NODE\_OPTIONS=--max-old-space-size=8192

The CLI supports standard Node.js memory flags, and raising the heap limit resolves memory-related command failures for larger operations.

*Source ticket: Case 53727*

## 3\. Branch Merge Consumes Excessive Memory and Time — Use the \--no-revert Flag

Merging branches on a large stack with significant data differences consumed roughly 12GB of memory and took a long time to complete.

**Root cause**

By default, the CLI's merge behavior creates a revert (backup) branch unless the \--no-revert flag is used. For large stacks with substantial differences, this backup-branch creation duplicates data, driving up memory usage and execution time. Frequent recursive status polling during the merge (every 5 seconds) may also add to heap memory usage.

**Resolution**

1. Add the \--no-revert flag to the merge command to skip automatic backup-branch creation:

csdx cm:branches:merge ... \--no-revert

Using \--no-revert produces a noticeably faster merge with significantly lower memory consumption for large stacks. Note that skipping the revert branch also means there is no automatic backup to roll back to, so consider your own backup strategy before merging without it.

*Source ticket: Case 56439*

## 4\. Configuring a Custom Rate Limit for Bulk Publishing via CLI

The customer hit CLI publishing limits during large-scale bulk publish operations.

**Root cause**

By default, bulk publish operations run at approximately 1 request per second, which can be a bottleneck for large-scale publishing and increases the chance of hitting rate limits inefficiently.

**Resolution**

1. Configure a custom rate limit for bulk operations based on your organization's plan limits:

csdx config:set:rate-limit \--org \<your\_org\_uid\> \--utilize 10 \--limit-name bulkLimit

The \--utilize flag sets the percentage of your organization's total available rate limit capacity to use (10 in this example allows use of around 10% of total capacity). Adjusting this improves throughput and reduces interruptions during bulk publish operations.

*Source ticket: Case 57566*

## 5\. Rate Limit Exceeded During Query-Based Migration Import — Reduce Import Concurrency

During a query-based content migration between stacks, the customer hit "Rate Limit Exceeded" errors while importing entries into the destination stack. This resulted in incomplete reference mapping — only 3 of an expected 13 references were linked.

**Root cause**

The CLI's import already includes a built-in retry mechanism (up to 3 retries on failed operations), but at the default import concurrency of 5 parallel operations, rate limits were still being exceeded on this organization's plan, causing some operations to fail even after retries.

**Resolution**

1. Reduce the import concurrency below the default value of 5, using an external configuration file with the import command.

2. If rate limits are still a constraint after reducing concurrency, request an increase to the organization's write limit.

Lowering import concurrency keeps requests within the organization's rate limit, allowing the built-in retry mechanism to succeed and references to map completely.

*Source ticket: Case 58171*

# CLI Feature Availability & Beta Limitations

**Meta Title:** Contentstack CLI Version and Beta Feature Availability | Contentstack

**Meta Description:** Understand current limitations around CLI 2.x asset management beta features and workarounds available in CLI 1.x.

**URL:** 

**Section:** 

**Subsection:** 

## 1\. CLI 2.x Asset Management Beta Features Are Not Yet Generally Available

The customer asked about exporting asset metadata for a specific folder, referencing an enhanced CLI version with asset management capabilities they had heard about.

**Root cause**

Folder-aware asset management, including folder-specific metadata export, is part of a newer asset management integration available in CLI 2.x, which is currently in beta verification and not yet generally available. The currently available CLI 1.x does not support this asset management system.

**Resolution**

1. Confirm you are on CLI 1.x if you do not have beta access — folder-specific asset metadata export is not available in this version.

2. As a workaround, use the Content Management API to fetch assets and filter by folder-related metadata where available, or write a custom script against the Management API to iterate through assets and extract metadata such as name, URL, size, and folder association.

The Management API workaround provides folder-level asset metadata today; native folder-aware asset management in the CLI will be available once the CLI 2.x beta reaches general availability.

*Source ticket: Case 57886*

