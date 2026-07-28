# Migrating Entries Between Branches Using Migration Scripts

The customer asked how to migrate entries from one branch to another within the same stack.

**Root cause**

Branch-to-branch entry migration is not a single built-in CLI command. The migration script feature's built-in operations (such as creating or editing a content type or field) only cover content type and global field schema changes, not entries. Moving entries between branches requires a migration script that calls the entry-level management operations directly, giving you scripted, controlled movement of entries between branches.

**Resolution**

1. Use Contentstack migration scripts (run via `csdx cm:stacks:migration`) to move entries from the source branch to the destination branch rather than looking for a single built-in "move branch" command. Keep in mind that the `--branch` flag scopes the script to one branch, so a script that copies entries between branches needs to open a second connection to the source branch within the script itself.

2. Refer to the Contentstack migration script documentation for the general script structure and execution steps.

3. Test the script against a non-production branch first, and confirm entries appear correctly in the destination branch before relying on it for production data.

4. If your branch merge involves added or modified content types, consider `csdx cm:branches:merge` first. It can automatically generate ready-to-run entry migration scripts for the affected content types and prints the `csdx cm:stacks:migration --multiple --file-path ...` command to run them. This can be a faster path than writing a migration script from scratch when the entry sync is tied to a content-type merge.

Support confirmed migration scripts are the correct tool for branch-to-branch entry migration, and the customer acknowledged the guidance and confirmed they would proceed. This ticket's notes describe the recommended approach at a high level. They do not include a specific script example.

*Source ticket: Case 43819*
