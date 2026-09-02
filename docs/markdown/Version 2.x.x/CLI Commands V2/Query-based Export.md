---
uid: "blt7b3284729d3494f0"
seo_title: "Query-based Export | Contentstack"
seo_description: "Use the Contentstack CLI plugin to export content types using queries with automatic dependency and reference support."
---

# Query-based Export

## Overview

The Contentstack CLI Query Export Plugin gives you complete control over exporting specific content types and their dependencies using [queries](/docs/developers/apis/content-delivery-api/queries).

The Query-based Export plugin lets you perform the following operations in Contentstack CLI:

- Migrating specific content types.
- Backing up filtered content.
- Managing environments efficiently.

Key Features

- **Query-based Filtering:** Uses queries to select specific [content types](/docs/headless-cms/about-content-types).
- **Automatic Dependency Export:** Includes related [global fields](/docs/headless-cms/about-global-field), [extensions](/docs/developer-hub/about-ui-locations), [taxonomies](/docs/headless-cms/about-taxonomy), [Marketplace apps](/docs/marketplace/about-marketplace), and [personalize](/docs/personalize/about-personalize).
- **Reference Handling:** Automatically detects and exports referenced content types and their [entries](/docs/headless-cms/about-entries), [entry variants](/docs/headless-cms/about-entry-variants/), and referenced assets.
- **Reliable Exports:** Maintains content integrity by including all related parts.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- [CLI installed](/docs/headless-cms/install-the-cli) and [configured](/docs/headless-cms/configure-regions-in-the-cli) (version 1.44 or higher)
- CLI [authenticated](/docs/headless-cms/cli-authentication#authentication)

## Installation

Run the following command to install the plugin:

```
csdx plugins:install @contentstack/cli-cm-export-query
```

To verify the installation, run:

```
csdx plugins
```

**Usage**

```
csdx cm:stacks:export-query [OPTIONS]
```

Options

- `-k, --stack-api-key=stack-api-key`: API key of the source stack.

- `--query=query`: Query string or file path. Refer to the Query Format section.

- `-d, --data-dir=data-dir`: Absolute path to the folder to store the exported content.

- `-a, --alias=alias`: Management token alias of the source stack.

- `--branch=branch`: \[default: main\] Name of the branch where you want to export content.

- `--branch-alias=branch-alias`: Alias of the branch to export from. (Version: 1.0.0-beta.4 or above)

  > **Note:** If no branch or branch alias is provided, and the stack is branch-enabled, the default main branch will be exported.

- `-c, --config=config`: Path to the configuration JSON file containing all options for a single run.

- `--skip-references`: Skip referenced content types.

- `--skip-dependencies`: Skip global fields, extensions, and taxonomies.

- `--secured-assets=secured-assets`: \[optional\] Use this flag to export your content if the [secured assets](/docs/administration) feature is enabled.

- `--yes, -y`: \[optional\] Skip confirmation prompts.

- `--config, -c`: \[optional\] Path to the configuration file.

## Query Format

Use the following query structure to filter content types. Replace placeholders with appropriate field names and values.

```
{
  "modules": {
    "content-types": {
      "<field>": {
        "<operator>": "<value>"
      }
    }
  }
}
```

**Example Operators:** `$in`, `$regex`, `$gte`

> **Additional Resource:** Refer to the [Content Delivery API Queries](/docs/developers/apis/content-delivery-api/queries) for the full list of operators.

**Examples**

- To export content types by title:

  ```
  csdx cm:stacks:export-query -a prod-alias --query '{"modules":{"content-types":{"title":{"$in":["Blog","Author"]}}}}'
  ```

- To export using a query from a file:

  ```
  csdx cm:stacks:export-query -a prod-alias --query ./my-query.json

  my-query.json:
  {
    "modules": {
      "content-types": {
        "$and": [
          { "uid": { "$in": ["author","blog_post"] }}
        ]
      }
    }
  }
  ```

### Supported Modules

- **Query-supported Module:**
  - `content-types:` Schema and configuration of content types.

- **Automatically Exported Dependencies:**
  - `global-fields:` Linked global fields
  - `extensions:` Standard and marketplace custom field extensions
  - `marketplace-apps:` Marketplace integrations
  - `taxonomies:` Referenced taxonomy definitions

- **Always Exported Modules:**
  - `stack:` Stack metadata
  - `locales:` Language settings
  - `environments:` Deployment environments
  - `personalize:` Personalize the project

- **Content Data Modules:**
  - `entries:` Entries of all exported content types
  - `assets:` All assets linked in exported entries

## Limitations

- Only `content type` queries are supported.
- All **asset folders** are exported. Folder-level filtering is not supported.
