# Copying or Syncing Entries Between Branches (No Built-In Feature)

The customer asked how to copy or sync entries, including localized versions and references, from one branch to another, since no direct option was visible in the UI.

**Root cause**

Contentstack does not offer a single built-in feature to copy or sync entries between branches outside of manual UI actions. Bulk or reference-aware copying requires the Content Management API or the CLI, with custom scripting to handle localizations and references.

**Resolution**

1. For a single entry: copy manually via the UI, or use the Content Management API. Copying all localizations for one entry requires a custom script that fetches each locale and recreates it in the target branch.

2. For bulk copying: use the CLI to export content from the source branch and import it into the target branch, or use the Content Management API with a custom script that queries all entries from the source branch and creates them in the target.

3. For entries containing references: copy referenced entries first, then the entries that reference them. Maintain a UID-mapping table and use a two-pass approach: copy first, then resolve and update references using the mapped UIDs.

4. If your entries belong to content types involved in a branch merge, `csdx cm:branches:merge` can automatically generate ready-to-run entry migration scripts that create or update those entries in the base branch, and it prints the `csdx cm:stacks:migration --multiple` command to run them. This is the closest thing to a built-in entry-sync feature between branches, though it only covers entries of content types involved in a merge, not arbitrary entry copying.

Using CLI export/import or the Content Management API with a UID-mapping approach allows entries, localizations, and references to move between branches, even though no single one-click feature exists for this today. Both `cm:stacks:export` and `cm:stacks:import` accept a `--branch` flag, so exporting from the source branch and importing into the target branch is a genuinely supported flow, not an improvised workaround.

*Source ticket: Case 53260*
