# No Support for Custom Filtered Exports via CLI

The customer asked whether Contentstack supports exporting a custom filtered view of entries directly, rather than exporting an entire content type.

**Root cause**

`cm:stacks:export` and `cm:export-to-csv` do not offer a way to filter entries within a content type during export. Their public flags (`--module`, `--content-types`) only select which content types to export, not which entries within a content type to include. For filtering which content types get exported, Contentstack provides an official, installable CLI plugin, the Query Export Plugin (`@contentstack/cli-cm-export-query`), which adds the `csdx cm:stacks:export-query` command. It exports the content types matched by a query and automatically includes their dependencies (global fields, extensions, taxonomies, marketplace apps) and references (referenced content types, entries, entry variants, and referenced assets), so the exported data stays consistent. The documented limitation is that only content-type-level queries are supported. There is no way to filter which entries within a content type get exported, and asset-folder-level filtering is not supported either, all asset folders are exported regardless of the query.

**Resolution**

1. Install the plugin:

csdx plugins:install @contentstack/cli-cm-export-query

2. Verify the installation:

csdx plugins

3. Run a query-based export, filtering by content type. For example, to export only the Blog and Author content types:

csdx cm:stacks:export-query -a <alias> --query '{"modules":{"content-types":{"title":{"$in":["Blog","Author"]}}}}'

A query can also be stored in a JSON file and passed with `--query ./my-query.json`. The query uses Content Delivery API-style operators, such as `$in`, `$regex`, and `$gte`.

4. Use `--skip-references` or `--skip-dependencies` if the automatic export of referenced content types or dependencies (global fields, extensions, taxonomies, marketplace apps) needs to be limited.

5. If the requirement is to filter which entries within a content type are exported (not just which content types), or to filter assets by folder, export the full content type or asset set and apply the filter to the exported data afterward, since neither of those is supported by the query.

The `cm:stacks:export-query` command from the Query Export Plugin is the supported way to export a filtered set of content types instead of the entire stack, with dependencies and references handled automatically. Its documented limitation is that only content-type-level queries are supported, so entry-level filtering within a content type and asset-folder-level filtering still require exporting fully and filtering the result afterward.

*Source ticket: Case 50983*
