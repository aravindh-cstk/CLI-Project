# CLI 2.x Asset Management Beta Features Are Not Yet Generally Available

The customer asked about exporting asset metadata for a specific folder, referencing an enhanced CLI version with asset management capabilities they had heard about.

**Root cause**

Folder-aware asset export already works in the current, generally available CLI. Running a standard asset export writes out the folder structure for the stack and includes each asset's folder association as part of the exported asset data. This works today and does not require a newer or beta CLI version.

The customer likely heard about Contentstack Assets (CS Assets), a separate, space-based asset management system. CS Assets is also generally available in the current CLI, not a beta or a newer version. It exports assets from workspaces linked to a stack branch into a dedicated directory instead of the standard assets folder, along with organization-level field and asset type definitions. This mode only activates when two conditions are both met: an administrator has configured a CS Assets URL for the region, and the stack branch has workspaces linked to it in the organization. Both are configuration steps, not a CLI version requirement. If either condition is missing, or if the export uses a management token instead of a logged-in session, the CLI falls back to the standard asset export automatically, without an error. This combination of conditional, silent fallback and an unfamiliar export layout is the most likely source of the "enhanced CLI version with asset management" impression.

Folder scoping works the same way in both systems. Neither the standard export nor CS Assets exports a single folder on its own. The standard export fetches all folders and all assets for the stack, and CS Assets fetches all folders across every linked space. Getting results for just one folder requires filtering the exported data (or a Management API response) by folder after export.

**Resolution**

1. Run the standard export: `csdx cm:stacks:export --module assets` (or a full export, which includes the assets module by default). The exported data includes the folder structure and each asset's folder association. No beta CLI or newer version is required.

2. If the organization has CS Assets configured (a CS Assets URL set for the region and workspaces linked to the branch) and the export runs under a logged-in session rather than a management token, the CLI exports in CS Assets format instead. The folder structure and asset data are still included, just organized by workspace rather than in a single assets folder.

3. To scope the result to one folder, filter the exported asset data locally by matching each asset's folder association against the folder you want. The export already contains full folder and association data, so no extra export step is needed.

4. If a full local export isn't an option, fetch assets directly from the Management API and filter the response by folder, since the CLI has no flag that scopes export to a single folder, in either export format.

*Source ticket: Case 57886*
