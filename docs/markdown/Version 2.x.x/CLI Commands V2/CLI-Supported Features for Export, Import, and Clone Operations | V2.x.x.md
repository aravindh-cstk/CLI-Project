---
uid: "blt5ea38dadb4d99b6c"
seo_title: "CLI-Supported Features for Export, Import, and Clone Operations | V2.x.x | Contentstack"
seo_description: "Explore the CLI-supported features for export, import, and clone operations including Marketplace app handling, module imports, error management, and Personalize project support."
---

# CLI-Supported Features for Export, Import, and Clone Operations

---

## Overview

Contentstack CLI offers support for [export](/docs/headless-cms/export-content-using-the-cli), [import](/docs/headless-cms/import-content-using-the-cli), and clone operations, including Marketplace apps, module-wise imports, error handling, and Personalize project integration.

This guide outlines these features to help you manage content migration operations with flexibility and control.

---

## Supported Modules

The CLI supports the following modules for export, import, and clone operations:

| Module | Export | Import | Clone | Notes |
| --- | --- | --- | --- | --- |
| **Content Types** | ✅ | ✅ | ✅ | Schema definitions |
| **Entries** | ✅ | ✅ | ✅ | Content entries |
| **Assets** | ✅ | ✅ | ✅ | Media files |
| **Environments** | ✅ | ✅ | ✅ | Environment configurations |
| **Extensions** | ✅ | ✅ | ✅ | Experience extensions |
| **Global Fields** | ✅ | ✅ | ✅ | Global field definitions |
| **Labels** | ✅ | ✅ | ✅ | Content labels |
| **Locales** | ✅ | ✅ | ✅ | Locale configurations |
| **Webhooks** | ✅ | ✅ | ✅ | Webhook configurations |
| **Workflows** | ✅ | ✅ | ✅ | Workflow definitions |
| **Custom Roles** | ✅ | ✅ | ✅ | Custom role definitions |
| **Taxonomies** | ✅ | ✅ | ✅ | Taxonomy structures |
| **Marketplace Apps** | ✅ | ✅ | ✅ | Public and private apps |
| **Personalize** | ✅ | ✅ | ✅ | Personalize projects |
| **Entry Variants** | ✅ | ✅ | ✅ | Entry variant configurations |
| **CS Assets** | ✅ | ✅ | ❌ | Space-based assets (requires `cs-assets` region config) |
| **Publishing Rules** | ✅ | ✅ | ✅ | Workflow publishing rules |
| **Composable Studio** | ✅ | ✅ | ✅ | Requires Basic Auth. Skipped when you authenticate with a management token or with OAuth |

The names in the table above are display names. When you pass `--module` on the export or import command, use the identifier form instead: `stack`, `assets`, `locales`, `environments`, `extensions`, `webhooks`, `global-fields`, `entries`, `content-types`, `custom-roles`, `workflows`, `publishing-rules`, `labels`, `marketplace-apps`, `taxonomies`, `personalize`, `variant-entries`, `composable-studio`. The identifier `variant-entries` is valid on import only. The CLI validates the value before the operation starts and fails immediately on an unknown name.

---

## Marketplace Apps

You can export/import public and private Marketplace apps into a stack using CLI commands.

## Prerequisites

- **Logged In:** CLI authenticated (see [CLI Authentication and Adding Tokens](/docs/headless-cms/cli-authentication))
- **Permissions:** Owner or Admin rights to export Marketplace apps
- **Marketplace Apps Support:** Enabled in the destination organization

**Important Notes:**

- Only the latest version of a public or private Marketplace app can be installed via CLI
- If you're using a region other than AWS NA, AWS EU, AWS AU, Azure NA, Azure EU, GCP NA, or GCP EU, provide the Developer Hub URL when prompted
- To override the default Marketplace app encryption key, update the config.json file

### Public Apps

If a public Marketplace app with a specific configuration already exists in the destination organization, you will be prompted with the following options during import:

- **Update** - Update the app with the new configuration from the source organization

- **Skip updating** - Skip updating the app configuration

  > **Warning:** Skipping may result in issues with imported content.

- **Exit** - Cancel the entire stack import process

**Example:**

```
# Export with Marketplace apps
csdx cm:stacks:export -a source-alias --data-dir ./export

# Import with Marketplace apps (interactive prompts)
csdx cm:stacks:import -a target-alias --data-dir ./export
```

### Private Apps

If the imported app has the same name as an existing app in the destination stack:

- You will be prompted to **rename** the imported app

> **Note:** App names must be **3-20 characters** long.

**During Stack Import:**

- If acknowledged and confirmed, the listed private app(s) will be re-created and installed
- If you cancel the app recreation, it may disrupt the import process of entries, content types, or global fields
- To skip re-creation of private apps if they already exist, use the  flag

**Skip App Recreation:**

```
csdx cm:stacks:import \
  -a target-alias \
  --data-dir ./export \
  -y
```

**Important:** You cannot reuse any existing private apps during the import process.

### Error Handling

If an error occurs while importing a public or private app:

- You will be prompted to confirm whether to proceed
  - If you choose **not to proceed**, the import stops
  - If you choose **to proceed**, the import may still succeed but could affect entries, content types, or global fields

---

## Personalize and Entry Variants

When working with stacks that are synced with a [Personalize](/docs/personalize/about-personalize) project, certain modules and configurations are automatically handled during export and import operations.

### Exporting

If the stack you're exporting is linked to a Personalize project, the following items will be exported:

- **Personalize Project** - The associated Personalize project

- **Personalize Modules:**
  - [Experiences](/docs/personalize/about-experiences/)
  - [Audience](/docs/personalize/about-audiences/)
  - [Attributes](/docs/personalize/about-attributes/)
  - [Events](/docs/personalize/about-events/)

- **Entry Variants** - Exported from the stack as part of entries

**Example:**

```
# Export stack with Personalize project
csdx cm:stacks:export -a source-alias --data-dir ./export
```

### Importing

If the content you're importing is associated or synced with a Personalize project, a new Personalize project will be created and linked to the new stack. Additionally, the following items will be imported:

- **Personalize Modules:**
  - Experiences
  - Audience
  - Attributes
  - Events

- **Entry Variants** - Imported into the stack as part of entries

**Options:**

| Flag | Type | Required | Default | Description | Notes |
| --- | --- | --- | --- | --- | --- |
| `--personalize-project-name` | string | No | - | Provide a unique name for the Personalize project |  |

**Example:**

```
# Import with Personalize project
csdx cm:stacks:import \
  -a target-alias \
  --data-dir ./export \
  --personalize-project-name "My Personalize Project"
```

> **Note:** Variants and Personalize currently support only basic authentication.

### Personalize and Entry Variants Limitation

**Important:** The `-a <alias>` flag (management token) skips Personalize modules as they require an [auth token for import](/docs/headless-cms/import-content-using-the-cli#import-content-using-management-token) and cannot be imported using a management token.

**Workaround:**

- Use `csdx auth:login` for authentication instead of management tokens when importing Personalize projects
- Or use `--stack-api-key` with login-based authentication

---

## CS Assets

The CLI uses CS Assets for asset export and import only when **both** of the following conditions are met:

- A CS Assets URL is configured for your region using `csdx config:set:region`.
- The stack branch has linked workspaces in your Contentstack organization.

> **Note:** Linked workspaces are CS Assets spaces in your Contentstack organization that are associated with a branch. The CLI reads them automatically from branch settings.

### Partial activation behavior

When only one condition is met, the CLI behaves as follows:

| Condition | Export behavior | Import behavior |
| --- | --- | --- |
| CS Assets URL configured, no linked workspaces | Falls back to legacy asset export silently | Falls back to legacy asset export silently |
| Linked workspaces found, no CS Assets URL | Falls back to legacy asset export silently | Logs a message and skips the CS Assets step. Import continues for all other modules (content types, entries, locales). |

### Exporting

When both conditions are met, the CLI activates CS Assets mode automatically and writes assets under a `spaces/` directory instead of `assets/`.

```
csdx cm:stacks:export -k <stack-api-key> --data-dir ./export
```

> **Note:** Use `csdx auth:login` for CS Assets export. When using a management token, the CLI cannot read branch settings, so linked workspaces are never populated and CS Assets mode never activates. The export falls back to legacy asset export. See [Management Token Behavior](/docs/headless-cms/cli-for-cs-assets#management-token-behavior).

### How CS Assets differs from legacy asset export

| Aspect | Legacy Asset Export | CS Assets |
| --- | --- | --- |
| **Export directory** | `assets/` at branch root | `spaces/` at branch root |
| **Asset organization** | Single flat structure | Per-space directories (`spaces/{space_uid}/`) |
| **Fields & asset types** | Not exported | Exported once per run; org-level definitions shared across all spaces (`spaces/fields/`, `spaces/asset_types/`) |
| **Space metadata** | N/A | Exported to `spaces/{space_uid}/space.json` |
| **Activation** | Always on | Automatic when CS Assets URL is configured and linked workspaces exist |
| **Management token** | Supported | Falls back to legacy asset export. The CLI skips the stack-settings step and logs a debug message. |

### Importing

CS Assets import works with all authentication methods, including management tokens.

```
csdx cm:stacks:import -k <stack-api-key> --data-dir ./export
```

The import command detects CS Assets mode when **both** the `spaces/` directory and the `am_v2` key in `stack/settings.json` are present in the export directory. No additional flags are required. See [How CS Assets import is detected](/docs/headless-cms/cli-for-cs-assets#how-cs-assets-import-is-detected).

For full details on CS Assets export and import behavior, see [CLI for CS Assets](/docs/headless-cms/cli-for-cs-assets).

---

## Module-Wise Operations

You can export, import, or clone specific modules instead of all modules.

### Export Specific Modules

```
# Export only entries
csdx cm:stacks:export -a <alias> --data-dir ./export --module entries

# Export multiple modules
csdx cm:stacks:export -a <alias> --data-dir ./export --module entries assets content-types
```

### Import Specific Modules

```
# Import only entries
csdx cm:stacks:import -a <alias> --data-dir ./export --module entries

# Import multiple modules
csdx cm:stacks:import -a <alias> --data-dir ./export --module entries assets content-types
```

### Clone Specific Modules

```
# Clone structure only (no entries/assets)
csdx cm:stacks:clone \
  --source-management-token-alias source-alias \
  --destination-management-token-alias destination-alias \
  --type a

# Clone structure with content (all modules)
csdx cm:stacks:clone \
  --source-management-token-alias source-alias \
  --destination-management-token-alias destination-alias \
  --type b
```

---

## Error Handling

The CLI provides comprehensive error handling for export, import, and clone operations:

### Export Errors

- **Authentication Errors:** Verify management token or login credentials
- **Permission Errors:** Ensure you have appropriate permissions
- **Network Errors:** Check network connectivity and region configuration
- **Module Errors:** Verify module names are correct

### Import Errors

- **Module Already Exists:** Use `--replace-existing` flag or `import-setup` command
- **Dependency Errors:** Import dependencies before dependent modules
- **Reference Errors:** Run audit fix before import
- **Marketplace App Errors:** Handle app recreation prompts or use

### Clone Errors

- **Permission Errors:** Ensure owner/admin rights for creating stacks
- **Authentication Errors:** Verify management token aliases
- **Marketplace App Errors:** Provide encryption key (3 attempts allowed)

For detailed troubleshooting, see the CLI Troubleshooting Guide.

---

## Best Practices

### Marketplace Apps

- **Test First:** Test Marketplace app import on staging before production
- **Backup:** Always backup before importing Marketplace apps
- **Review Configuration:** Review app configurations before updating
- **Skip Recreation:** Use  if apps already exist and are configured correctly

### Personalize Projects

- **Use Login Authentication:** Use `csdx auth:login` instead of management tokens for Personalize imports
- **Unique Project Names:** Provide unique names for Personalize projects
- **Verify Sync:** Verify Personalize project sync after import

### Module-Wise Operations

- **Import Dependencies First:** Import dependencies before dependent modules
- **Use Import-Setup:** Use `import-setup` for selective module updates
- **Test Incrementally:** Test module imports incrementally

For more best practices, see the CLI Best Practices Guide.

---

## Limitations

For detailed limitations, see the [CLI Limitations Guide](/docs/headless-cms/cli-limitations).

**Key Limitations:**

- Only latest version of Marketplace apps can be installed
- Personalize modules require login authentication (not management tokens)
- Entry variants are exported/imported as part of entries
- Some modules may have dependencies that must be imported first

---

## Related Documentation

- [Export Content Using the CLI](/docs/headless-cms/export-content-using-the-cli)
- [Import Content Using the CLI](/docs/headless-cms/import-content-using-the-cli#import-content-using-management-token)
- Cloning a Stack
- [Overwrite Existing Content Using CLI Import](/docs/headless-cms/overwrite-existing-content-using-cli-import)
- CLI Troubleshooting Guide
- [CLI Limitations Guide](/docs/headless-cms/cli-limitations)
- CLI Best Practices Guide

## Quick Reference

| Use Case | Section | Key Call |
| --- | --- | --- |
| Checking module coverage | [Supported Modules](#supported-modules) | - |
| Moving Marketplace apps | [Marketplace Apps](#marketplace-apps) | - |
| Meeting the requirements first | [Prerequisites](#prerequisites) | - |
| Moving Personalize data and entry variants | [Personalize and Entry Variants](#personalize-and-entry-variants) | - |
| Moving CS Assets | [CS Assets](#cs-assets) | - |
| Running one module at a time | [Module-Wise Operations](#module-wise-operations) | `csdx cm:stacks:export` |
| Reading an error | [Error Handling](#error-handling) | - |
| Following the recommended order | [Best Practices](#best-practices) | - |
| Checking what is not covered | [Limitations](#limitations) | - |
