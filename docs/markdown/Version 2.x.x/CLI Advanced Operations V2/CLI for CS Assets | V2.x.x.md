---
uid: "blt642ce07c5edd5f56"
seo_title: "CLI for CS Assets | V2.x.x | Contentstack"
seo_description: ""
---

# CLI for CS Assets

## Overview

CS Assets extends standard Contentstack CLI export and import operations to support space-based asset management.

During export, CS Assets mode activates when

- Your region is configured with a CS Assets URL and
- The branch has linked workspaces.

During import, the CLI detects CS Assets mode from the export directory.

When CS Assets mode is not active, the CLI falls back to legacy asset export, the standard flow that writes an `assets/` folder at the branch root.

## What You'll Learn

- Configure prerequisites for CS Assets export and import
- Export assets using the standard CLI workflow
- Understand the CS Assets directory structure
- Import CS Assets exports safely into a target stack
- Understand how the CLI detects CS Assets import mode automatically
- Prevent workspace linking errors by understanding how stack settings are handled during import
- Understand the dependency order for import operations
- Understand management token limitations that affect CS Assets export

## Quick Decision Guide

Select an authentication method based on your operation:

| Operation | Auth method | CS Assets mode | Go to |
| --- | --- | --- | --- |
| Export | Session (`csdx auth:login`) | Activates when prerequisites are met | [Export CS Assets](#export-cs-assets) |
| Export | Management token | Never activates. Falls back to legacy asset export | [Management Token Behavior](#management-token-behavior) |
| Import | Session (`csdx auth:login`) | Activates from the export directory | [Import CS Assets](#import-cs-assets) |
| Import | Management token | Activates from the export directory | [Import CS Assets](#import-cs-assets) |

## Prerequisites

### Mandatory

- **CS Assets URL configured for your region:** Your Contentstack administrator must add a CS Assets URL to the region configuration. See [Configure Regions in the CLI](/docs/headless-cms/configure-regions-in-the-cli):

  ```
  csdx config:set:region \
    --cda <cda_url> \
    --cma <cma_url> \
    --ui-host <ui_url> \
    --cs-assets <cs_assets_url> \
    -n <region_name>
  ```

  Without this URL, the CLI has no CS Assets endpoint even if workspaces are linked.

- **Linked workspaces on the stack branch:** The stack branch must have linked workspaces configured in your Contentstack organization.

  > **Note:** Linked workspaces are CS Assets spaces in your Contentstack organization that are associated with a stack branch. The CLI reads linked workspace assignments automatically from branch settings during export. Without linked workspaces, the CLI has no spaces to export, even if the URL is configured.

### Optional

- Management token for import

## Export CS Assets

When both prerequisites are met, the CLI activates CS Assets mode automatically and exports assets under a `spaces/` directory instead of `assets/`.

```
csdx cm:stacks:export -k <stack-api-key> --data-dir ./export --branch <branch-name>
```

> **Note:** CS Assets mode does not activate when using a management token. See [Management Token Behavior](#management-token-behavior) for details.

### What gets exported

| Path | Contents |
| --- | --- |
| `spaces/export-metadata.json` | Stack API key used to map source assets to the target stack during import |
| `spaces/fields/fields.json` | Organization-level field definitions (shared across all spaces) |
| `spaces/asset_types/asset-types.json` | Organization-level asset type definitions (shared across all spaces) |
| `spaces/{space_uid}/space.json` | Space details, workspace UID, and branch information |
| `spaces/{space_uid}/folders.json` | Asset folder structure for the space |
| `spaces/{space_uid}/assets.json` | Asset metadata for the space |
| `spaces/{space_uid}/assets/files/{asset_uid}/{filename}` | Downloaded asset files |

> **Note:** In CS Assets mode, the `assets/` folder at the branch root is replaced with the `spaces/` directory.

### Export directory structure

The command creates the following structure under `--data-dir`, with `--branch` as the top-level subdirectory:

```
./export/
└── {branch}/
    ├── spaces/
    │   ├── export-metadata.json
    │   ├── fields/
    │   │   └── fields.json
    │   ├── asset_types/
    │   │   └── asset-types.json
    │   ├── {space_uid}/
    │   │   ├── space.json
    │   │   ├── folders.json
    │   │   ├── assets.json
    │   │   └── assets/
    │   │       └── files/
    │   │           └── {asset_uid}/
    │   │               └── {filename}
    │   └── {space_uid}/
    │       ├── space.json
    │       ├── folders.json
    │       ├── assets.json
    │       └── assets/
    │           └── ...
    ├── content-types/
    ├── entries/
    └── locales/
```

**Key points:**

- Space directories use the space UID rather than human-readable space names. For example, `blt1234567890abcdef/`.
- `fields/` and `asset_types/` are organization-level and exported once, shared across all linked spaces.
- All spaces linked to a stack are exported.

## Import CS Assets

The CLI detects CS Assets exports automatically from the directory you specify with `--data-dir`.

```
csdx cm:stacks:import -k <stack-api-key> --data-dir ./export
```

### How CS Assets import is detected

CS Assets import mode activates when **both** of the following are present in `--data-dir`:

1. A `spaces/` directory at the branch root.
2. `stack/settings.json` contains an `am_v2` key. The source stack writes this key automatically during export.

When neither condition is present, the CLI runs legacy asset export instead. All other modules (content types, entries, and locales) import normally in both cases.

### How the stack settings are handled

The `stack/settings.json` file in `--data-dir` contains linked workspaces from the source stack. The CLI strips these entries before writing the file to the target stack, then creates the correct links for the target branch in the [How the target branch is linked](#how-the-target-branch-is-linked) step. This ensures the target branch connects to the newly imported workspaces.

### What gets imported

Imports run in the following dependency order:

| Step | What gets imported | Source | Why |
| --- | --- | --- | --- |
| 1 | Organization-level fields | `spaces/fields/fields.json` | Asset types reference these definitions |
| 2 | Organization-level asset types | `spaces/asset_types/asset-types.json` | Asset types depend on field definitions |
| 3 | Per-space data | `spaces/{space_uid}/` | Runs after asset types are in place: space metadata, asset folders, asset metadata, and asset files |

### What mapper files are created

Each asset imported into the target stack receives a new UID and URL. The CLI writes mapper files that record the source-to-target mapping for asset UIDs, asset URLs, and space UIDs. During the entries import step, these files are used to update asset references across all entry fields.

The mapper files are written to the `mapper/assets/` folder inside your backup directory (the path set by `--backup-dir`):

| File | Contents |
| --- | --- |
| `uid-mapping.json` | Source asset UID → target asset UID |
| `url-mapping.json` | Source asset URL → target asset URL |
| `space-uid-mapping.json` | Source space UID → target space UID |
| `duplicate-assets.json` | Empty (reserved for duplicate tracking) |

### How the target branch is linked

After spaces are created in the target organization, the CLI links each new space to the target branch. This ensures subsequent exports from the target stack detect linked workspaces correctly.

If you use management tokens in automated pipelines, read [Management Token Behavior](#management-token-behavior) before running import commands.

## Management Token Behavior

Management tokens affect export and import differently in CS Assets.

### How management tokens affect export

CS Assets export requires linked workspaces, which the CLI reads from branch settings. Reading branch settings is not supported when using a management token, so the CLI skips this step. Without that information, CS Assets **never activates for export**. The export always falls back to legacy asset export.

**Workaround:** Use session-based authentication for export:

```
csdx auth:login
csdx cm:stacks:export -k <stack-api-key> --data-dir ./export
```

### How management tokens affect import

Management tokens do not block CS Assets import. Import detects CS Assets from `--data-dir` (the `spaces/` folder), not from branch settings. The CS Assets URL is read from the configured region. When the organization UID is needed, the CLI fetches it from the stack automatically.

```
# CS Assets import works with management token
csdx cm:stacks:import -a <alias> --data-dir ./export
```

## Next Steps

- [Export Content Using the CLI](/docs/headless-cms/export-content-using-the-cli): Full reference for all flags and options available with `csdx cm:stacks:export`, including module filtering and branch targeting.
- [Import Content Using the CLI](/docs/headless-cms/import-content-using-the-cli): Full reference for all flags and options available with `csdx cm:stacks:import`, including `--backup-dir` and module-level controls.
- [Configure Regions in the CLI](/docs/headless-cms/configure-regions-in-the-cli): Reference for all `csdx config:set:region` flags, including `--cs-assets` for enabling CS Assets mode in a region.
- [CLI-Supported Features for Export, Import, and Clone Operations](/docs/headless-cms/cli-supported-features-for-export-import-and-clone-operations): Matrix of which content types and asset features are supported across CLI versions.
