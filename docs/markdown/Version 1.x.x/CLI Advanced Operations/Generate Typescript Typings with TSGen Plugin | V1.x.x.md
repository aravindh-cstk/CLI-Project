---
uid: "bltcc14ad6c062c9a82"
seo_title: "Generate Typescript Typings with TSGen Plugin | V1.x.x | Contentstack"
seo_description: "The tsgen plugin is a Contentstack CLI plugin that generates TypeScript typings from content types. This step-by-step guide lets you install and use the tsgen plugin in CLI."
---

# Generate Typescript Typings with TSGen Plugin

## Overview

The Contentstack CLI TSGen plugin generates TypeScript typings from REST API and GraphQL queries. The type file containing the TypeScript typings assists developers in working with content types, global fields, and GraphQL queries in TypeScript.

With the TSGen plugin, you can annotate interfaces and fields with comments from the JSDoc library. Additionally, the TSGen plugin allows you to add prefixes to interfaces.

> **Note:** The Contentstack CLI uses the [introspection query](/docs/developers/apis/graphql-content-delivery-api/#introspection) to generate a GraphQL schema.

This step-by-step guide lets you install and use the tsgen plugin in the CLI.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- [CLI installed](/docs/headless-cms/install-the-cli/v1) (version 1.1.0 and above)
- [Delivery token](/docs/headless-cms/create-a-delivery-token/)

## Steps for execution

1. Install the TSGen plugin using the following command:

   ```
   csdx plugins:install contentstack-cli-tsgen
   ```

2. Add the delivery token as an alias to the CLI using the following command:

   ```
   csdx auth:tokens:add --delivery
   ```

   > **Note:** Skip this step if you already have a delivery token as an alias.

## Usage

```
csdx tsgen
```

## Options

- `-a`, `--token-alias=token-alias`: (mandatory) Delivery token alias.
- `-d`, `--[no-]doc`: (optional) Includes documentation comments. By default, this flag is enabled.
- `-o`, `--output=output`: (mandatory) The full output path.
- `-p`, `--prefix=prefix`: (optional) Interface prefix, e.g., "I".
- `--api-type=api-type`: \[default: rest\] (optional) The API type to generate type definitions. \<options: rest|graphql\>
- `--branch=branch`: (optional) The name of the branch to be used.
- `--include-system-fields`: Includes system fields in generated types.
- `--namespace=namespace`: (optional) The namespace for the GraphQL API type to organize the generated types.
- `--include-editable-tags`: (optional) Includes editable tags in typings.
- `--include-referenced-entry`: (optional) Includes the `ReferencedEntry` interface in generated types. Use this option to add a generic interface for handling referenced entries when the exact content type is unknown or when a flexible reference type is needed.

## Examples

1. To generate a type file with a delivery token alias and output file path:

   ```
   csdx tsgen -a "delivery token alias" -o "contentstack/generated.d.ts"
   ```

2. To generate a type file with a delivery token alias and output file path for a branch named `develop`:

   ```
   csdx tsgen -a "delivery token alias" -o "contentstack/generated.d.ts" --branch "develop"
   ```

3. To generate a type file with a prefix:

   ```
   csdx tsgen -a "delivery token alias" -o "contentstack/generated.d.ts" -p "I"
   ```

4. To generate a type file excluding documentation comments:

   ```
   csdx tsgen -a "delivery token alias" -o "contentstack/generated.d.ts" --no-doc
   ```

5. To generate a type file with the `graphql` API type:

   ```
   csdx tsgen -a "delivery token alias" -o "contentstack/generated.d.ts" --api-type graphql
   ```

6. To generate a type file with the `graphql` API type and GraphQL as the namespace:

   ```
   csdx tsgen -a "delivery token alias" -o "contentstack/generated.d.ts" --api-type graphql --namespace "GraphQL"
   ```

7. To generate a type file with editable tags:

   ```
   csdx tsgen -a "delivery token alias" -o "contentstack/generated.d.ts" --include-editable-tags
   ```

8. To generate a type file with `ReferencedEntry` interface:

   ```
   csdx tsgen -a "delivery token alias" -o "contentstack/generated.d.ts" --include-referenced-entry
   ```

9. To generate typings with full Entry support:

   ```
   csdx tsgen -a "delivery token alias" -o "contentstack/generated.d.ts" --include-system-fields --include-referenced-entry
   ```

> **Note:** Together, these two flags enable **full, accurate Entry typings**, ensuring that relationships, system metadata, and dynamic references are all represented correctly in the generated TypeScript definitions.

## Supported Contentstack Fields

- [Number](/docs/headless-cms/number)
- [Title](/docs/headless-cms/title/)
- [Date](/docs/headless-cms/date/)
- [Boolean](/docs/headless-cms/boolean/)
- [Single Select w/ String and Number Types](/docs/headless-cms/single-line-textbox/)
- [Multiple Select w/ String and Number Types](/docs/headless-cms/multi-line-textbox/)
- [Modular Block](/docs/headless-cms/modular-blocks/)
- [Global Field](/docs/headless-cms/about-global-field/) (CLI supports [Nested Global Fields](/docs/headless-cms/about-global-field#nested-global-fields) from v1.42.0)
- [Group](/docs/headless-cms/group/)
- [Link](/docs/headless-cms/link/)
- [File](/docs/headless-cms/file/)
- [Reference](/docs/headless-cms/reference/)
- [Taxonomy](/docs/headless-cms/about-taxonomy)

## Supported Field Options

- [Mandatory](/docs/headless-cms/mandatory)
- [Multiple](/docs/headless-cms/multiple)
- [Multiple Max Limit](/docs/headless-cms/minimum-and-maximum-limit)
- Description (used in JSDoc comment)

> **Additional Resource:** For a major TSGen version upgrade, refer to the [Migration.md](https://github.com/contentstack/contentstack-cli-tsgen/blob/master/MIGRATION.md) file in the GitHub repository.
