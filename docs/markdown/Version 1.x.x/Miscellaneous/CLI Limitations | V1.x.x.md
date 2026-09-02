---
uid: "blt74918691c8a465c1"
seo_title: "CLI Limitations | V1.x.x | Contentstack"
seo_description: "Understand Contentstack CLI limitations, supported environments, and workarounds for import/export, authentication, OS support, and more."
---

# CLI Limitations

---

## Core CLI Limitations

### Node.js Version Requirements

**Limitation:** CLI requires Node.js version 18.0.0 or above (recommended: 20.x or 22.x)

**Impact:** CLI won't work with Node.js versions below 18.0.0

**Workaround:**

- Install supported Node.js version (18.0.0+, recommended: 20.x or 22.x)

- Use nvm for version management:

  ```
  nvm install 20
  nvm use 20
  ```

**Related Commands:**

- `node --version`
- `npm install -g @contentstack/cli@latest`

**Version Information:** All CLI versions

**Tags:** nodejs, version, compatibility, prerequisites

---

### Operating System Support

**Limitation:** CLI is tested and supported on:

- macOS (latest versions)
- Linux (Ubuntu, Debian, CentOS)
- Windows (10, 11)

**Impact:** Other operating systems may work but are not officially supported

**Workaround:**

- Use Docker for unsupported OS
- Use supported OS for production operations

**Related Commands:**

- `csdx --version`

**Version Information:** All CLI versions

**Tags:** operating system, platform, compatibility

---

## Authentication Module Limitations

### Management Token Expiration

**Limitation:** Management tokens don't expire automatically but can be revoked

**Impact:** Tokens remain valid until manually revoked, which can be a security risk

**Workaround:**

- Rotate tokens regularly (every 90 days recommended)
- Monitor token usage
- Revoke unused tokens

**Related Commands:**

- `csdx auth:tokens`
- `csdx auth:tokens:remove`

**Version Information:** All CLI versions

**Tags:** authentication, management token, security, expiration

---

### MFA Support Limitations

**Limitation:** MFA requires manual code entry or OAuth flow

**Impact:** Cannot fully automate MFA-enabled accounts without MFA secret

**Workaround:**

- Use OAuth for SSO accounts: `csdx auth:login --oauth`
- Set `CONTENTSTACK_MFA_SECRET` environment variable for automatic OTP generation
- Use management tokens (bypass MFA once added)

**Related Commands:**

- `csdx auth:login`
- `csdx auth:login --oauth`

**Version Information:** All CLI versions

**Tags:** authentication, MFA, 2FA, OAuth

---

### Organization Switching

**Limitation:** CLI doesn't have built-in organization switcher

**Impact:** Must logout/login or use different token aliases to switch organizations

**Workaround:**

- Use different management token aliases for different orgs
- Logout and re-login for different organization

**Related Commands:**

- `csdx auth:logout`
- `csdx auth:login`
- `csdx auth:tokens:add --management`

**Version Information:** All CLI versions

**Tags:** authentication, organizations, switching

---

## Export Module Limitations

### Unsupported Modules

**Limitation:** The following modules cannot be exported:

- Users
- Releases

**Impact:** User data and release information cannot be migrated via CLI

**Workaround:**

- Users must be manually added to destination stack
- Releases must be recreated manually

**Related Commands:**

- `csdx cm:stacks:export`

**Version Information:** All versions

**Tags:** export, unsupported, users, releases

---

### Duplicate Assets

**Limitation:** If multiple assets have the same UID and file name, only the first asset will be exported

**Impact:** Duplicate assets may not all be exported

**Workaround:**

- Ensure unique UIDs for all assets
- Check for duplicate assets before export
- Re-export assets module if needed

**Related Commands:**

- `csdx cm:stacks:export --module assets`

**Version Information:** All versions

**Tags:** export, assets, duplicates, UID

---

### Payload Size Limits

**Limitation:** Default maxContentLength and maxBodyLength is 100 MB

**Impact:** Large exports may fail with payload size errors

**Workaround:**

- Add to configuration file:

  ```
  {
    "maxContentLength": 200000000,
    "maxBodyLength": 200000000
  }
  ```

- Process exports in smaller batches

- Export specific modules

**Related Commands:**

- `csdx cm:stacks:export --config`

**Tags:** export, payload size, maxContentLength, maxBodyLength

---

### API Request Timing

**Limitation:** Export operations may encounter concurrency issues

**Impact:** Large exports may fail or be throttled

**Workaround:**

- Add `delayMs` parameter to configuration file (e.g., `delayMs: 1000` for 1-second delays)
- Export in smaller batches using `--module` flag
- Configure rate limits: `csdx config:set:rate-limit`

**Related Commands:**

- `csdx cm:stacks:export --config`
- `csdx config:set:rate-limit`

**Tags:** export, delayMs, concurrency, rate limits

---

### Version History

**Limitation:** Only the latest version of published entries and assets is exported

**Impact:** Historical versions are not preserved during export

**Workaround:**

- Export creates new versions in destination stack
- Historical versions cannot be restored

**Related Commands:**

- `csdx cm:stacks:export`

**Version Information:** All versions

**Tags:** export, version history, entries, assets

---

## Import Module Limitations

### Version History

**Limitation:** Only the latest version of published entries and assets is imported

**Impact:** Historical versions are not restored during import

**Workaround:**

- Import creates new versions in destination stack
- Historical versions cannot be restored

**Related Commands:**

- `csdx cm:stacks:import`

**Version Information:** All versions

**Tags:** import, version history, entries, assets

---

### cs-assets export requires login-based authentication

**Limitation:** CS Assets mode does not activate when using a management token (`-a <alias>`). The CLI reads linked workspaces from branch settings, which is not supported with management tokens. The export falls back to legacy asset mode.

**Impact:** Stacks with cs-assets enabled export using the legacy `assets/` directory instead of the CS Assets `spaces/` directory.

**Workaround:** Use session-based authentication for cs-assets stacks:

```
csdx auth:login
csdx cm:stacks:export -k <stack-api-key> --data-dir ./export
```

**Related Documentation:** [CLI for CS Assets](/docs/headless-cms/cli-for-cs-assets#how-management-tokens-affect-export)

**Version Information:** All versions

**Tags:** export, cs-assets, management token, authentication

---

### Workflow Users

**Limitation:** When importing workflows, admins and workflow stage users are not included in the migration

**Impact:** Workflow configurations are imported but user assignments are lost

**Workaround:**

- Manually reassign workflow users after import
- Update workflow stages with correct users

**Related Commands:**

- `csdx cm:stacks:import --module workflows`

**Tags:** import, workflows, users, migration

---

### Payload Size Limits

**Limitation:** Default maxContentLength and maxBodyLength is 100 MB

**Impact:** Large imports may fail with payload size errors

**Workaround:**

- Add to configuration file:

  ```
  {
    "maxContentLength": 200000000,
    "maxBodyLength": 200000000
  }
  ```

- Process imports in smaller batches

- Export/import specific modules

**Related Commands:**

- `csdx cm:stacks:import --config`

**Tags:** import, payload size, maxContentLength, maxBodyLength

---

### API Request Timing

**Limitation:** Import operations may encounter concurrency issues

**Impact:** Large imports may fail or be throttled

**Workaround:**

- Add `delayMs` parameter to configuration file (e.g., `delayMs: 1000` for 1-second delays)
- Import in smaller batches using `--module` flag
- Configure rate limits: `csdx config:set:rate-limit`

**Related Commands:**

- `csdx cm:stacks:import --config`
- `csdx config:set:rate-limit`

**Tags:** import, delayMs, concurrency, rate limits

---

### Unsupported Modules

**Limitation:** The following modules cannot be imported:

- Users
- Releases

**Impact:** User data and release information cannot be migrated via CLI

**Workaround:**

- Users must be manually added to destination stack
- Releases must be recreated manually

**Related Commands:**

- `csdx cm:stacks:import`

**Version Information:** All versions

**Tags:** import, unsupported, users, releases

---

## Import Setup Limitations

### Supported Modules Limitation

**Limitation:** Only three modules can be directly selected for import-setup:

- `global-fields`
- `content-types`
- `entries`

**Impact:** Other modules cannot be directly selected for import-setup

**Workaround:**

- Other modules (extensions, assets, etc.) are automatically handled as dependencies
- If you need to import other modules, use the full import command without import-setup

**Code Evidence:**

- `cli/packages/contentstack-import-setup/src/commands/cm/stacks/import-setup.ts` lines 42-47: Module options restricted to only three

**Related Commands:**

- `csdx cm:stacks:import-setup --module`

**Version Information:** All versions

**Tags:** import-setup, modules, selective import

---

### Asset Duplication Limitation

**Limitation:** When multiple assets in the target stack match a source asset (same title, filename, file_size), `import-setup` cannot automatically determine which one to use. These duplicates are recorded in `duplicate-assets.json` but are NOT added to `uid-mapping.json`.

**Impact:**

- Duplicate assets may be uploaded as new assets during import
- Manual resolution required for duplicates

**Workaround:**

1. Review `duplicate-assets.json` before import
2. Manually resolve duplicates in target stack (delete or merge duplicates)
3. Re-run import-setup to regenerate mappers with resolved duplicates

**Code Evidence:**

- `../advanced-features/import-setup.md` lines 1260-1274: Confirms this limitation with detailed explanation

**Related Commands:**

- `csdx cm:stacks:import-setup --module assets`
- `csdx cm:stacks:import --backup-dir`

**Version Information:** All versions

**Tags:** import-setup, assets, duplicates, uid-mapping

---

### Complex Dependencies Not Fully Automated

**Limitation:** Some modules with complex dependencies may require manual intervention

**Impact:** Import-setup may not handle all dependency scenarios automatically

**Workaround:**

1. Import dependencies manually first
2. Then use import-setup for dependent modules
3. Or use full import with `--replace-existing` for all modules

**Related Commands:**

- `csdx cm:stacks:import-setup`
- `csdx cm:stacks:import --replace-existing`

**Version Information:** All versions

**Tags:** import-setup, dependencies, automation

---

### Large Exports Take Time

**Limitation:** Processing thousands of items can take 10+ minutes

**Impact:** Import-setup operations may be slow for large stacks

**Workaround:**

1. Be patient, process is working correctly
2. Monitor progress through log messages
3. Consider exporting/importing in smaller batches

**Related Commands:**

- `csdx cm:stacks:import-setup`

**Version Information:** All versions

**Tags:** import-setup, performance, large exports

---

### Branch Structure Must Match

**Limitation:** Export directory structure must match branch structure for branch imports

**Impact:** Branch imports may fail if directory structure doesn't match

**Workaround:**

1. Export specific branch: `csdx cm:stacks:export -k <key> -d ./export --branch <branch>`
2. Point import-setup to branch directory: `-d ./export/<branch-name>`

**Related Commands:**

- `csdx cm:stacks:export --branch`
- `csdx cm:stacks:import-setup --branch`

**Version Information:** All versions

**Tags:** import-setup, branch, directory structure

---

### Asset Publishing Is Skipped When Asset Scanning Is Active

**Limitation:** During `cm:stacks:import`, assets are not published in the same run when asset scanning applies. This happens either because `--skip-assets-publish` was passed explicitly, or because the org plan has asset scanning enabled, which sets the same flag automatically. Org-plan auto-detection of asset scanning is rolling out and is not yet active for every org plan.

**Impact:** Assets are imported but remain unpublished until a separate publish step runs after scanning completes.

**Workaround:** See [Asset Scan In-Queue Assets Are Not Retried](#asset-scan-in-queue-assets-are-not-retried) for the wait-and-republish steps, since the same retry behavior applies here.

**Related Commands:**

- `csdx cm:stacks:import --skip-assets-publish`
- `csdx cm:assets:publish --backup-dir`

**Related Documentation:** [Asset Scanning in CLI](/docs/headless-cms/asset-scanning-in-cli/v1)

**Version Information:** All versions with asset scanning enabled

**Tags:** asset scanning, import, skip-assets-publish, backup-dir

---

## Overwrite Operations Limitations

### Dependency on Properly Structured Exported Content

**Limitation:** The process requires access to properly formatted exported content before running the command

**Impact:** Overwrite operations may fail if export structure is incorrect

**Workaround:**

- Ensure export was completed successfully
- Verify export directory structure
- Re-export if structure is invalid

**Related Commands:**

- `csdx cm:stacks:export`
- `csdx cm:stacks:import --replace-existing`

**Version Information:** All versions

**Tags:** overwrite, export structure, migration

---

### Asset Duplication

**Limitation:** Duplicate assets in the target stack are uploaded to a new folder, which can lead to redundancy. A resolution is under development.

**Impact:** Duplicate assets may be created during overwrite operations

**Workaround:**

- Review duplicate assets before overwrite
- Manually remove duplicates after import
- Use import-setup to identify duplicates first

**Related Commands:**

- `csdx cm:stacks:import-setup`
- `csdx cm:stacks:import --replace-existing`

**Version Information:** All versions

**Tags:** overwrite, assets, duplicates

---

### Limited Module Support

**Limitation:** Currently, the import-setup command supports only content types, entries, global fields, and extensions. Modules with complex dependencies are not yet included.

**Impact:** Some modules cannot be overwritten automatically

**Workaround:**

- Use full import with `--replace-existing` for all modules
- Import dependencies manually first
- Use standard import for unsupported modules

**Related Commands:**

- `csdx cm:stacks:import-setup`
- `csdx cm:stacks:import --replace-existing`

**Version Information:** All versions

**Tags:** overwrite, modules, import-setup

---

### Manual Overwrite Steps

**Limitation:** Overwriting certain modules requires manual intervention due to the absence of an automated overwrite command

**Impact:** Some overwrite operations cannot be fully automated

**Workaround:**

- Use Contentstack UI for manual overwrites
- Combine CLI and UI operations
- Script manual steps where possible

**Related Commands:**

- `csdx cm:stacks:import --replace-existing`

**Version Information:** All versions

**Tags:** overwrite, manual intervention, automation

---

### Processing Large Data Sets

**Limitation:** Migration of extensive content or assets may be time-consuming and requires accuracy verification

**Impact:** Large overwrite operations may take significant time

**Workaround:**

- Process in smaller batches
- Verify accuracy after each batch
- Use import-setup to preview changes
- Monitor progress through logs

**Related Commands:**

- `csdx cm:stacks:import-setup`
- `csdx cm:stacks:import --replace-existing`

**Version Information:** All versions

**Tags:** overwrite, large datasets, performance

---

### Handling Complex Relationships

**Limitation:** Additional manual effort may be necessary to map deeply nested or interdependent modules correctly

**Impact:** Complex relationships may not be overwritten correctly

**Workaround:**

- Review relationships before overwrite
- Import dependencies in correct order
- Manually verify relationships after import
- Use import-setup to identify dependencies

**Related Commands:**

- `csdx cm:stacks:import-setup`
- `csdx cm:stacks:import --replace-existing`

**Version Information:** All versions

**Tags:** overwrite, relationships, dependencies

---

## Bulk Publish/Unpublish Limitations

### Batch Size Limitations

**Limitation:** Bulk publish operations process entries/assets in batches

**Impact:** Very large operations may take time

**Workaround:**

- Process in smaller batches
- Use configuration files for better control
- Monitor progress

**Related Commands:**

- `csdx cm:entries:publish`
- `csdx cm:assets:publish`

**Version Information:** All versions

**Tags:** bulk publish, batch size, performance

---

### Asset Scan In-Queue Assets Are Not Retried

**Limitation:** When a stack has asset scanning enabled, `cm:assets:publish` skips any asset that is still in the scan queue (pending) at the time the command runs. The retry loop that would otherwise wait and recheck pending assets is present in the code but configured with zero retries in this release, so it never executes.

**Impact:** In-queue assets are skipped and logged as "Skipped (max retries exceeded)" on the same run, even though the underlying scan may finish moments later.

**Workaround:**

- Wait for the asset's scan to complete, then run `csdx cm:assets:publish --backup-dir <BACKUP_DIR>` again to publish it.
- Quarantined assets are skipped permanently and are not resolved by retrying.

**Related Commands:**

- `csdx cm:assets:publish --backup-dir`

**Related Documentation:** [Asset Scanning in CLI](/docs/headless-cms/asset-scanning-in-cli/v1)

**Version Information:** All versions with asset scanning enabled

**Tags:** asset scanning, bulk publish, quarantine, in-queue

---

---

## Clone Operations Limitations

### cs-assets space-based assets are not cloned

**Limitation:** The `csdx cm:stacks:clone` command does not export or import cs-assets space-based assets. Clone internally runs export then import, but neither step activates cs-assets mode — the `spaces/` directory is never written, and any existing cs-assets spaces on the source branch are silently skipped.

**Impact:** If the source stack uses cs-assets, the cloned stack will not contain the `spaces/` directory or any cs-assets data. Only the legacy `assets/` structure is cloned.

**Workaround:** Run export and import as separate commands to migrate cs-assets:

```
csdx auth:login
csdx cm:stacks:export -k <source-api-key> --data-dir ./export
csdx cm:stacks:import -k <target-api-key> --data-dir ./export
```

**Related Commands:**

- `csdx cm:stacks:export`
- `csdx cm:stacks:import`

**Related Documentation:** [CLI for CS Assets](/docs/headless-cms/cli-for-cs-assets)

**Version Information:** All versions

**Tags:** clone, cs-assets, space-based assets

---

### Environment Limitations

**Limitation:** Bulk publish operations are environment-specific

**Impact:** Must specify environment for each operation

**Workaround:**

- Use configuration files to manage multiple environments
- Script multiple operations for different environments

**Related Commands:**

- `csdx cm:entries:publish -e <environment>`
- `csdx cm:assets:publish -e <environment>`

**Version Information:** All versions

**Tags:** bulk publish, environments

---

## Branch Operations Limitations

### Branch UID Format

**Limitation:** The branch UID must be in lower case, and only '_' can be used to separate two words

**Impact:** Invalid UID formats will cause branch creation to fail

**Workaround:**

- Use lowercase letters only
- Use underscore (_) as word separator
- Avoid special characters and spaces

**Related Commands:**

- `csdx cm:branches:create --uid`

**Version Information:** All versions

**Tags:** branch, UID, format, naming

---

### Branch UID Length

**Limitation:** The maximum character length for a branch UID is 15

**Impact:** Branch UIDs longer than 15 characters will be rejected

**Workaround:**

- Keep branch UIDs to 15 characters or less
- Use abbreviations if needed
- Plan branch naming convention

**Related Commands:**

- `csdx cm:branches:create --uid`

**Version Information:** All versions

**Tags:** branch, UID, length, limits

---

### Maximum Branches Per Stack

**Limitation:** The maximum number of branches allowed per stack depends on the product tier

**Impact:** Stack may reach branch limit based on subscription tier

**Workaround:**

- Check product tier limits
- Delete unused branches
- Upgrade tier if more branches needed

**Related Commands:**

- `csdx cm:branches:list`

**Version Information:** All versions

**Tags:** branch, limits, product tier, subscription

---

### Branch Name and Source Cannot Be Edited

**Limitation:** Once you create a branch, you cannot edit its name or the source branch

**Impact:** Branch configuration cannot be changed after creation

**Workaround:**

- Delete and recreate branch with correct name/source
- Plan branch structure before creation
- Use Contentstack UI if available

**Related Commands:**

- `csdx cm:branches:create`
- `csdx cm:branches:delete`

**Version Information:** All versions

**Tags:** branch, edit, name, source branch

---

## Launch Operations Limitations

### Environment Creation Not Supported

**Limitation:** Creating a new Launch environment via the CLI is currently not supported. At this time, environment creation is a one-time setup that must be done through the Launch UI. Once the environment is created, the Launch CLI can be used to trigger redeployments on existing environments.

**Impact:** Cannot create new environments via CLI

**Workaround:**

- Create environments through Launch UI first
- Use CLI for redeployments on existing environments
- Use `csdx launch:redeploy` for existing environments

**Related Commands:**

- `csdx launch:redeploy`

**Version Information:** All versions

**Tags:** launch, environment, creation, UI

---

### Bitbucket Cloud Not Supported

**Limitation:** Currently, the Launch CLI does not support Bitbucket Cloud as a source provider

**Impact:** Cannot use Bitbucket Cloud repositories with Launch CLI

**Workaround:**

- Use GitHub or GitLab as source provider
- Use Launch UI for Bitbucket Cloud projects
- Migrate repository to supported provider

**Related Commands:**

- `csdx launch`

**Version Information:** All versions

**Tags:** launch, Bitbucket, source provider

---

### Settings Modification Not Supported

**Limitation:** Currently, the Launch CLI does not support modifying settings for existing projects or environments. To make these changes, please use the Launch UI.

**Impact:** Cannot modify project or environment settings via CLI

**Workaround:**

- Use Launch UI to modify settings
- Use CLI only for deployment operations
- Configure settings before using CLI

**Related Commands:**

- `csdx launch`

**Version Information:** All versions

**Tags:** launch, settings, configuration, UI

---

## Migration Scripts Limitations

### NODE_PATH Requirement

**Limitation:** Custom migration scripts require NODE_PATH environment variable to be set

**Impact:** Migration scripts may fail with "module not found" errors

**Workaround:**

- Set NODE_PATH before running migrations:

  ```
  export NODE_PATH="$(npm root -g @contentstack/cli)/@contentstack/cli/node_modules"
  ```

- Add to shell profile for permanent fix

**Related Commands:**

- `csdx cm:stacks:migration`

**Version Information:** All versions

**Tags:** migration, NODE_PATH, module not found

---

### Migration Script Complexity

**Limitation:** Complex migration scripts may have performance issues

**Impact:** Large migrations may be slow or fail

**Workaround:**

- Break migrations into smaller scripts
- Test migrations on small datasets first
- Use dry-run mode to preview changes

**Related Commands:**

- `csdx cm:stacks:migration --dry-run`

**Version Information:** All versions

**Tags:** migration, performance, complexity

---

## Bootstrap Plugin Limitations

### Duplicate Content Types

**Limitation:** Avoid importing duplicate content types into existing stacks

**Impact:** Duplicate content types may cause conflicts or errors

**Workaround:**

- Check existing content types before bootstrap
- Use different stack for bootstrap
- Remove duplicate content types if needed

**Related Commands:**

- `csdx cm:bootstrap`

**Version Information:** All versions

**Tags:** bootstrap, content types, duplicates

---

### Role Requirements

**Limitation:** To create new stacks, ensure your role is set to Owner or Admin in the organization

**Impact:** Users without Owner/Admin role cannot create stacks via bootstrap

**Workaround:**

- Request Owner or Admin role from organization admin
- Use existing stack with appropriate permissions
- Have Owner/Admin run bootstrap command

**Related Commands:**

- `csdx cm:bootstrap`

**Version Information:** All versions

**Tags:** bootstrap, roles, permissions, owner, admin

---

### Deprecated Apps

**Limitation:** Deprecated starter apps (reactjs-starter, nextjs-starter, gatsby-starter, angular-starter, nuxt-starter, vue-starter, stencil-starter, nuxt3-starter) are still available but not recommended for new projects

**Impact:** Deprecated apps may not receive updates or support

**Workaround:**

- Use active "Kickstart" apps instead (kickstart-next, kickstart-nuxt, etc.)
- Migrate from deprecated apps to active apps if needed

**Related Commands:**

- `csdx cm:bootstrap --app-name`

**Version Information:** All versions

**Tags:** bootstrap, deprecated, starter apps, migration

---

## Seed Command Limitations

### GitHub Repository Requirements

**Limitation:** Seed command requires GitHub repository with specific structure

**Impact:** Repositories not following structure may fail

**Workaround:**

- Follow Contentstack seed repository structure
- Use Contentstack's sample repositories
- Structure custom repositories correctly

**Related Commands:**

- `csdx cm:stacks:seed`

**Version Information:** All versions

**Tags:** seed, GitHub, repository structure

---

## RTE Migration Limitations

### Content Type Requirements

**Limitation:** RTE migration requires content types with HTML RTE fields

**Impact:** Content types without HTML RTE fields cannot be migrated

**Workaround:**

- Verify content types have HTML RTE fields
- Migrate only applicable content types

**Related Commands:**

- `csdx cm:entries:migrate-html-rte`

**Version Information:** All versions

**Tags:** RTE migration, HTML RTE, content types

---

### Migration Scope

**Limitation:** RTE migration processes all entries in content type

**Impact:** Cannot selectively migrate specific entries

**Workaround:**

- Export entries first
- Filter entries manually
- Import filtered entries

**Related Commands:**

- `csdx cm:entries:migrate-html-rte`

**Version Information:** All versions

**Tags:** RTE migration, selective migration

---

## Entry Migration Limitations

**Limitation:** Entry migration has limitations similar to general import limitations

**Impact:** Same limitations as import module apply

**Workaround:**

- Follow import best practices
- Use import-setup for UID preservation
- Handle dependencies correctly

**Related Commands:**

- `csdx cm:stacks:import --module entries`

**Version Information:** All versions

**Tags:** entry migration, import limitations

---

## Audit Plugin Limitations

### Audit Scope

**Limitation:** Audit may not detect all issues

**Impact:** Some issues may require manual review

**Workaround:**

- Review audit reports carefully
- Manually verify critical content
- Run audit multiple times if needed

**Related Commands:**

- `csdx cm:stacks:audit`
- `csdx audit:fix`

**Version Information:** All versions

**Tags:** audit, scope, detection

---

### Fix Limitations

**Limitation:** Audit fix may not resolve all issues automatically

**Impact:** Some issues require manual intervention

**Workaround:**

- Review fix reports
- Manually fix issues that audit cannot resolve
- Use `--fix-only` to fix specific issue types

**Related Commands:**

- `csdx audit:fix --fix-only <type>`

**Version Information:** All versions

**Tags:** audit, fix, automation

---

## Variants Plugin Limitations

### Personalize Authentication

**Limitation:** Variants and Personalize currently support only basic authentication (login)

**Impact:** Cannot use management tokens for variants operations

**Workaround:**

- Use `csdx auth:login` before variants operations
- Use OAuth for SSO accounts

**Code Evidence:**

- `backup/../advanced-features/supported-features.md` line 99: Confirms Personalize and Entry Variants limitation with authentication

**Related Commands:**

- `csdx cm:variants:export`
- `csdx cm:variants:import`
- `csdx auth:login`

**Version Information:** All versions

**Tags:** variants, Personalize, authentication, login

---

### Variant Export/Import Scope

**Limitation:** Variants are exported/imported as part of entries

**Impact:** Cannot export/import variants independently

**Workaround:**

- Export/import entries to include variants
- Variants are automatically included

**Related Commands:**

- `csdx cm:stacks:export --module entries`
- `csdx cm:stacks:import --module entries`

**Version Information:** All versions

**Tags:** variants, entries, export, import

---

## Apps CLI Limitations

### Login Requirement

**Limitation:** Apps CLI requires login (management tokens not supported)

**Impact:** Cannot fully automate Apps CLI operations with management tokens

**Workaround:**

- Use `csdx auth:login` before Apps CLI operations
- Use OAuth for SSO accounts

**Related Commands:**

- `csdx app:create`
- `csdx app:deploy`
- `csdx auth:login`

**Version Information:** All versions

**Tags:** apps cli, authentication, login, developer hub

---

### App Name Constraints

**Limitation:** App names must be 3-20 characters long

**Impact:** App names outside this range will fail

**Workaround:**

- Ensure app names meet length requirements
- Use valid characters only

**Related Commands:**

- `csdx app:create -n <app_name>`

**Version Information:** All versions

**Tags:** apps cli, app name, constraints

---

## TSGen Plugin Limitations

### Plugin Installation Required

**Limitation:** TSGen plugin must be installed separately

**Impact:** TSGen commands won't work without plugin installation

**Workaround:**

- Install plugin: `csdx plugins:install @contentstack/cli-tsgen`
- Verify installation: `csdx plugins`

**Related Commands:**

- `csdx plugins:install @contentstack/cli-tsgen`
- `csdx tsgen`

**Version Information:** All versions

**Tags:** tsgen, plugin, installation

---

### Type Generation Scope

**Limitation:** Type generation is based on current stack structure

**Impact:** Types may not reflect all possible content structures

**Workaround:**

- Regenerate types after stack changes
- Manually update types if needed

**Related Commands:**

- `csdx tsgen`

**Version Information:** All versions

**Tags:** tsgen, type generation, scope

---

## Configuration Limitations

### Configuration File Size

**Limitation:** Very large configuration files may cause issues

**Impact:** Large configs may slow down operations

**Workaround:**

- Keep configuration files focused
- Use multiple config files for different scenarios
- Optimize configuration structure

**Related Commands:**

- `csdx cm:stacks:export --config`
- `csdx cm:stacks:import --config`

**Version Information:** All versions

**Tags:** configuration, file size, performance

---

### Rate Limit Configuration Scope

**Limitation:** Rate limit configuration applies globally

**Impact:** Cannot set different rate limits for different operations

**Workaround:**

- Use configuration files for operation-specific settings
- Adjust rate limits before different operations

**Related Commands:**

- `csdx config:set:rate-limit`
- Use `--config` flag for operation-specific settings

**Version Information:** All versions

**Tags:** configuration, rate limit, global settings

---

## Next Steps

- [CLI for CS Assets](/docs/headless-cms/cli-for-cs-assets): the CS Assets commands, which use the cs-assets REST API rather than the Content Management API.
- [Asset Scanning in CLI](/docs/headless-cms/asset-scanning-in-cli/v1): scan assets for malware as part of an import or export.
- [Migrate from Contentstack CLI V1 to V2](/docs/headless-cms/cli-v1-to-v2-migration-guide): what changed at 2.0.0, flag by flag, and how to upgrade.
