# Bulk Re-Publishing Entries Is Not Supported via CLI

The customer asked whether it is possible to bulk re-publish already-published entries for a specific content type on the main branch using the CLI, or whether SDK usage is required.

**Root cause**

This is not correct for the current CLI. The `@contentstack/cli-bulk-operations` plugin provides `csdx cm:stacks:bulk-entries`, and it is an officially documented plugin that you install separately with `csdx plugins:install @contentstack/cli-bulk-operations` after installing the base CLI. It does not ship bundled with the main `@contentstack/cli` package. Once installed, the command's `--operation publish` path fetches entries for the given content types and locales and, when no `--filter` flag narrows the set to draft, modified, unpublished, or non-localized entries, publishes every matched entry to the target environments regardless of whether it was already published. That is exactly a bulk re-publish of already-published entries. The command also accepts a `--branch` flag (default `main`), so scoping the operation to the main branch is supported directly.

**Resolution**

1. Install the plugin if it isn't already installed:

csdx plugins:install @contentstack/cli-bulk-operations

2. Verify the installation:

csdx cm:stacks:bulk-entries --help

3. Run the bulk-entries command with the publish operation, content type, target environment(s), locale(s), and branch:

csdx cm:stacks:bulk-entries --operation publish --content-types <content_type_uid> --environments <environment_name> --locales <locale_code> --branch main -k <stack_api_key>

4. Confirm the operation when prompted. The command lists the matched entries and asks for confirmation before publishing.

5. Review the operation's summary output and log file (written under the `bulk-operation` directory by default, or the path passed via `--bulk-operation-file`) to confirm which entries were published and whether any failed.

6. If some entries fail, retry only those using the log file: csdx cm:stacks:bulk-entries --retry-failed ./bulk-operation

Installing the `@contentstack/cli-bulk-operations` plugin and running `csdx cm:stacks:bulk-entries --operation publish` against the target content type, environment, locale, and branch bulk re-publishes already-published entries directly through the CLI, without needing a separate Management SDK script. If custom logic beyond what the bulk-entries flags support is needed, using the Management SDK to query entries, fetch publish details, and re-publish each one remains a valid alternative.

*Source ticket: Case 44338*
