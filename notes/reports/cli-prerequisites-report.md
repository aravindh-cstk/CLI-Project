# CLI Prerequisites Accuracy Report

WI-5 of the CLI Structure Review. Checks each V2 doc's Prerequisites against what the code actually requires, rather than against what the prose already claims.

Reproduce with:

```bash
python3 scripts/gen_prerequisites_report.py
```

## Versions this was checked against

| Fact | Value | Source |
|---|---|---|
| V2 GA version | **2.0.0** | `v2.0.0` git tag, `packages/contentstack/package.json` |
| V2 GA release date | **2026-08-13** | `changelog/2.x/cli-2.0.0.md` |
| Node requirement | **>=22.0.0** | same `package.json`, `engines.node` |
| Latest V1 | **1.66.0**, released 2026-07-27 | `changelog/1.x/cli-1.66.0.md` |

**On the source used.** The working trees for `repo/cli-core` and `repo/cli-plugins` sit on branch `v2-dev` at 2026-08-05 and 2026-07-25, both behind the 2026-08-13 GA release. Rather than pull and hope, core facts here are read from the `v2.0.0` tag, which is exact. Nothing was checked out and no branch was changed. The plugins monorepo carries no `v2.0.0` tag, so its command inventory comes from the working tree, and every flag-level claim below is cross-checked against `changelog/2.x/cli-2.0.0.md` instead.

---

## The baseline every command doc needs

From `repo/cli-core/packages/contentstack-command/src/index.ts`, the base class every command extends:

- It throws `You are not logged in. Run the command: $ csdx auth:login` when no email is configured.
- It exits when no region is configured, printing `Error: Region not configured. Please set the region with command $ csdx config:set:region`.

So the minimum for **every** doc that runs a command is four items: a Contentstack account, the CLI installed, an authenticated session, and a configured region. A command taking `--alias` needs a fifth, a management token added with `csdx auth:tokens:add`.

Region is the one most often missing. It is not optional for non-North-America stacks, and `common-rules.md` is explicit that a conditional requirement like this is Mandatory stated conditionally, never Optional.

---

## Bundled versus external plugins at GA

This is the highest-value finding in the report, and it is mechanically decidable. A doc for a bundled plugin must not tell the reader to install anything. A doc for an external plugin must, or the command fails as `command not found`.

**Bundled at GA (13 Contentstack plugins),** from `oclif.plugins`:

- `@contentstack/cli-audit`
- `@contentstack/cli-auth`
- `@contentstack/cli-bulk-operations`
- `@contentstack/cli-cm-bootstrap`
- `@contentstack/cli-cm-branches`
- `@contentstack/cli-cm-clone`
- `@contentstack/cli-cm-export`
- `@contentstack/cli-cm-export-to-csv`
- `@contentstack/cli-cm-import`
- `@contentstack/cli-cm-import-setup`
- `@contentstack/cli-cm-seed`
- `@contentstack/cli-config`
- `@contentstack/cli-migration`

**External, requiring `csdx plugins:install`:**

- `@contentstack/apps-cli`
- `@contentstack/cli-cm-export-query`
- `@contentstack/cli-cm-regex-validate`
- `@contentstack/cli-external-migrate`
- `contentstack-cli-content-type`
- `contentstack-cli-tsgen`

The GA changelog confirms two of these moved out of the bundle at GA rather than having always been external: `@contentstack/cli-launch` ("Made the `launch` plugin opt-in, it is no longer bundled") and `@contentstack/cli-cm-migrate-rte` ("Made the RTE migration available as a separate, opt-in plugin"). GA also added a guided install prompt for both instead of a bare `command not found`, which is itself documentable behavior that no doc currently mentions.

---

## Findings

### No Prerequisites section at any level

| Doc | Commands it documents |
|---|---|
| `Version 2.x.x/CLI Commands V2/Overwrite Existing Content using CLI Import \| V2.x.x` | `cm:stacks:import-setup`, `cm:stacks:import` |
| `Version 2.x.x/CLI Migration Use Cases V2/Branches \| Migration Use Cases \| V2.x.x` | `cm:branches:merge-status`, `cm:stacks:bulk-entries`, `cm:stacks:bulk-assets`, `cm:stacks:migration` |
| `Version 2.x.x/Miscellaneous V2/CLI Limitations \| V2.x.x` | `cm:stacks:import-setup`, `cm:stacks:bulk-entries`, `config:set:rate-limit`, `cm:stacks:bulk-assets` |
| `Version 2.x.x/Miscellaneous V2/Contentstack CLI Configuration Reference` | `cm:stacks:import-setup`, `cm:stacks:export-query`, `cm:stacks:migration`, `cm:stacks:export` |
| `Version 2.x.x/Miscellaneous V2/Uninstall CLI Plugins` | none |
| `Version 2.x.x/Miscellaneous V2/Useful Plugins` | none |

A doc with no commands and no Prerequisites is defensible: it runs nothing. A doc that documents a command and has no Prerequisites is not, because the base class will reject the reader before the command starts.

### Prerequisites present but not at H2

None.

### External plugin documented with no install instruction

| Doc | External package | Needs |
|---|---|---|
| `Version 2.x.x/Miscellaneous V2/Contentstack CLI Configuration Reference` | `@contentstack/cli-cm-export-query` | `csdx plugins:install @contentstack/cli-cm-export-query` |

Each of these documents a command that is not in the GA bundle, without telling the reader to install it. A reader following the doc gets `command not found`.

The `Contentstack CLI Configuration Reference` case is the softest of these. It is a module reference, and MOD3 deliberately gives that type no Prerequisites or Installation section. The right fix is not to add an install step to the reference, it is to make the `cm:stacks:export-query` entry link to `Query-based Export`, which carries the install step.

### Verified non-findings

Recorded so they are not re-raised. Each looks like a defect and is not.

- **`CLI for CS Assets | V2.x.x` needs no `plugins:install`.** `@contentstack/cli-asset-management` is absent from the GA bundle and is an oclif package, so it looks external. It ships no commands of its own: its `src/` holds `export`, `import`, `import-setup`, and `query-export` library code that the bundled export and import plugins consume. The GA changelog matches, recording "Added AM 2.0 export support" under `cli-cm-export` rather than a new command namespace. The doc correctly drives AM 2.0 through `cm:stacks:export` and `cm:stacks:import`, both bundled. This doc is also the strongest Prerequisites section in the corpus, with Mandatory and Optional subsections and a specific, verifiable list.
- **The five external plugin docs already carry their install step.** `Apps CLI Plugin`, `Content Type Plugin`, `Regex Validate Plugin`, `Generate Typescript Typings with TSGen Plugin`, and `CLI for Launch` each reference `csdx plugins:install`. `CLI for Launch` matters most, because the changelog shows `launch` only left the bundle at GA, so that doc has kept pace.

### Bundled plugin with a spurious install instruction

| Doc | Bundled packages |
|---|---|
| `Version 2.x.x/CLI Commands V2/CLI for Launch \| V2.x.x` | `@contentstack/cli-auth`, `@contentstack/cli-config` |
| `Version 2.x.x/Miscellaneous V2/Create Custom CLI Plugins for Contentstack \| V2.x.x` | `@contentstack/cli-auth`, `@contentstack/cli-config` |

These mention `plugins:install` while documenting only bundled commands. Verify each one: some legitimately reference installing a different plugin, which is fine, and the rest are telling readers to install something they already have.

### Prerequisites that omit region configuration

15 docs have a Prerequisites list that never mentions region.

| Doc | Items | Has account | Has install | Has auth |
|---|---|---|---|---|
| `Version 2.x.x/CLI Advanced Operations V2/Change Master Locale` | 2 | yes | yes | no |
| `Version 2.x.x/CLI Advanced Operations V2/Configure MFA Secret Using CLI \| V2.x.x` | 4 | yes | yes | no |
| `Version 2.x.x/CLI Advanced Operations V2/Generate Typescript Typings with TSGen Plugin \| V2.x.x` | 3 | yes | yes | no |
| `Version 2.x.x/CLI Commands V2/Bulk Operations in CLI \| V2.x.x` | 3 | no | yes | no |
| `Version 2.x.x/CLI Commands V2/Compare and Merge Branches Using the CLI \| V2.x.x` | 4 | yes | yes | yes |
| `Version 2.x.x/CLI Commands V2/Configure CLI Logging Preferences \| V2.x.x` | 2 | yes | yes | no |
| `Version 2.x.x/CLI Commands V2/Configure Proxy Settings in CLI \| V2.x.x` | 7 | no | yes | no |
| `Version 2.x.x/CLI Commands V2/Export Content Using the CLI \| V2.x.x` | 4 | yes | yes | yes |
| `Version 2.x.x/CLI Commands V2/Import Content Using the CLI \| V2.x.x` | 5 | yes | yes | yes |
| `Version 2.x.x/CLI Migration Use Cases V2/Migrate Selected Content Using the Query Export Plugin` | 4 | no | yes | yes |
| `Version 2.x.x/CLI Migration Use Cases V2/Migrate and Overwrite Content in the Same Stack \| V2.x.x` | 4 | no | no | yes |
| `Version 2.x.x/Content Migration Commands V2/Migrate your Content using the CLI Migration Command \| V2.x.x` | 2 | yes | yes | no |
| `Version 2.x.x/Get Started with CLI V2/Configure Regions in the CLI \| V2.x.x` | 2 | yes | yes | no |
| `Version 2.x.x/Get Started with CLI V2/Install the CLI \| V2.x.x` | 2 | yes | no | no |
| `Version 2.x.x/Miscellaneous V2/Create Custom CLI Plugins for Contentstack \| V2.x.x` | 4 | yes | yes | no |

The base class exits without a configured region, so for any reader on a non-North-America stack this is a blocking requirement that the doc does not state. State it conditionally rather than marking it Optional.

---

## GA changes the docs have not caught up with

From `changelog/2.x/cli-2.0.0.md`. These are content-accuracy findings rather than prerequisites, and each names the doc to check.

| GA change | Doc to check |
|---|---|
| Short flags removed in favour of long-form only, across export, import, tsgen (`-o`, `-p`, `-d`), content-type, migration, external-migrate | `Export Content Using the CLI` still documents a `Short Flag` column with `-k` and `-a`. Check each of the six. Note `apps-cli` went the other way and **added** `-k` |
| `--api-version` removed from `cm:stacks:bulk-entries` and `cm:stacks:bulk-taxonomies` | `Bulk Operations in CLI` |
| tsgen `--token-alias` renamed to `--alias` | `Generate Typescript Typings with TSGen Plugin` |
| New `auth:tokens:list` command and `auth:tokens` namespace | `CLI Authentication and Adding Tokens` |
| New `--cs-assets` and `--auth-api` flags on `config:set:region` | `Configure Regions in the CLI` |
| New `--skip-taxonomy-publish` on import, and taxonomies now auto-republish after import | `Import Content Using the CLI` |
| Export output is now a flat directory, global fields export one file per item, content type schema JSON export removed, main branch exported by default when `--branch` is empty | `Export Content Using the CLI` |
| New command `cm:stacks:bulk-taxonomies` | No doc owns it. Check `Bulk Operations in CLI` |
| `@contentstack/cli-asset-management` reached 1.0.0 at GA (AM 2.0: spaces, workspaces, fields, asset types, OAuth) | `CLI for CS Assets` |

---

## Commands with no owning doc

7 of 66 known commands are not mentioned in any V2 doc.

| Command | Package |
|---|---|
| `app` | `@contentstack/apps-cli` |
| `auth:tokens` | `@contentstack/cli-auth` |
| `cm:branches` | `@contentstack/cli-cm-branches` |
| `migrate:audit` | `@contentstack/cli-external-migrate` |
| `migrate:create` | `@contentstack/cli-external-migrate` |
| `migrate:import` | `@contentstack/cli-external-migrate` |
| `migrate:status` | `@contentstack/cli-external-migrate` |

---

## Per-doc detail

| Doc | Prereq level | Items | Commands | External packages |
|---|---|---|---|---|
| `Version 2.x.x/CLI Advanced Operations V2/Apps CLI Plugin \| V2.x.x` | H2 | 3 | 9 | `@contentstack/apps-cli` |
| `Version 2.x.x/CLI Advanced Operations V2/CLI for CS Assets \| V2.x.x` | H2 | 0 | 5 | none |
| `Version 2.x.x/CLI Advanced Operations V2/Change Master Locale` | H2 | 2 | 3 | none |
| `Version 2.x.x/CLI Advanced Operations V2/Configure MFA Secret Using CLI \| V2.x.x` | H2 | 4 | 1 | none |
| `Version 2.x.x/CLI Advanced Operations V2/Entry Migration \| V2.x.x` | H2 | 10 | 1 | none |
| `Version 2.x.x/CLI Advanced Operations V2/Generate Typescript Typings with TSGen Plugin \| V2.x.x` | H2 | 3 | 2 | `contentstack-cli-tsgen` |
| `Version 2.x.x/CLI Advanced Operations V2/Update Missing Reference UIDs for Entries, Assets, and Extensions` | H2 | 3 | 2 | none |
| `Version 2.x.x/CLI Commands V2/Audit Plugin \| V2.x.x` | H2 | 3 | 3 | none |
| `Version 2.x.x/CLI Commands V2/Bulk Operations in CLI \| V2.x.x` | H2 | 3 | 5 | none |
| `Version 2.x.x/CLI Commands V2/CLI for Launch \| V2.x.x` | H2 | 5 | 2 | none |
| `Version 2.x.x/CLI Commands V2/CLI-Supported Features for Export, Import, and Clone Operations \| V2.x.x` | H2 | 6 | 5 | none |
| `Version 2.x.x/CLI Commands V2/Cloning a Stack \| V2.x.x` | H2 | 3 | 1 | none |
| `Version 2.x.x/CLI Commands V2/Compare and Merge Branches Using the CLI \| V2.x.x` | H2 | 4 | 9 | none |
| `Version 2.x.x/CLI Commands V2/Configure CLI Logging Preferences \| V2.x.x` | H2 | 2 | 2 | none |
| `Version 2.x.x/CLI Commands V2/Configure Early Access in the CLI \| V2.x.x` | H2 | 3 | 3 | none |
| `Version 2.x.x/CLI Commands V2/Configure Proxy Settings in CLI \| V2.x.x` | H2 | 7 | 3 | none |
| `Version 2.x.x/CLI Commands V2/Content Type Plugin \| V2.x.x` | H2 | 4 | 10 | `contentstack-cli-content-type` |
| `Version 2.x.x/CLI Commands V2/Export Content Using the CLI \| V2.x.x` | H2 | 4 | 2 | none |
| `Version 2.x.x/CLI Commands V2/Import Content Using the CLI \| V2.x.x` | H2 | 5 | 2 | none |
| `Version 2.x.x/CLI Commands V2/Overwrite Existing Content using CLI Import \| V2.x.x` | **none** | 0 | 2 | none |
| `Version 2.x.x/CLI Commands V2/Query-based Export` | H2 | 3 | 2 | `@contentstack/cli-cm-export-query` |
| `Version 2.x.x/CLI Commands V2/Regex Validate Plugin \| V2.x.x` | H2 | 0 | 4 | `@contentstack/cli-cm-regex-validate` |
| `Version 2.x.x/CLI Migration Use Cases V2/Branches \| Migration Use Cases \| V2.x.x` | **none** | 0 | 5 | none |
| `Version 2.x.x/CLI Migration Use Cases V2/Migrate Content Between Stacks Using the CLI \| V2.x.x` | H2 | 5 | 3 | none |
| `Version 2.x.x/CLI Migration Use Cases V2/Migrate Selected Content Using the Query Export Plugin` | H2 | 4 | 5 | `@contentstack/cli-cm-export-query` |
| `Version 2.x.x/CLI Migration Use Cases V2/Migrate and Overwrite Content in the Same Stack \| V2.x.x` | H2 | 4 | 4 | none |
| `Version 2.x.x/Content Migration Commands V2/Export Content to CSV File Using the CLI \| V2.x.x` | H2 | 3 | 1 | none |
| `Version 2.x.x/Content Migration Commands V2/Import Content Using the Seed Command \| V2.x.x` | H2 | 4 | 3 | none |
| `Version 2.x.x/Content Migration Commands V2/Migrate your Content using the CLI Migration Command \| V2.x.x` | H2 | 2 | 2 | none |
| `Version 2.x.x/Get Started with CLI V2/CLI Authentication and Adding Tokens \| V2.x.x` | H2 | 3 | 6 | none |
| `Version 2.x.x/Get Started with CLI V2/Configure Regions in the CLI \| V2.x.x` | H2 | 2 | 2 | none |
| `Version 2.x.x/Get Started with CLI V2/Install the CLI \| V2.x.x` | H2 | 2 | 26 | none |
| `Version 2.x.x/Get Started with CLI V2/Migrate from Contentstack CLI V1 to V2 \| V2.x.x` | H2 | 0 | 30 | `@contentstack/apps-cli`, `@contentstack/cli-cm-regex-validate`, `@contentstack/cli-external-migrate`, `contentstack-cli-content-type`, `contentstack-cli-tsgen` |
| `Version 2.x.x/Miscellaneous V2/Bootstrap Starter Apps \| V2.x.x` | H2 | 6 | 1 | none |
| `Version 2.x.x/Miscellaneous V2/CLI Limitations \| V2.x.x` | **none** | 0 | 20 | `@contentstack/apps-cli`, `contentstack-cli-tsgen` |
| `Version 2.x.x/Miscellaneous V2/Configure Rate Limits in the CLI \| V2.x.x` | H2 | 3 | 3 | none |
| `Version 2.x.x/Miscellaneous V2/Contentstack CLI Configuration Reference` | **none** | 0 | 6 | `@contentstack/cli-cm-export-query` |
| `Version 2.x.x/Miscellaneous V2/Create Custom CLI Plugins for Contentstack \| V2.x.x` | H2 | 4 | 4 | none |
| `Version 2.x.x/Miscellaneous V2/Uninstall CLI Plugins` | **none** | 0 | 0 | none |
| `Version 2.x.x/Miscellaneous V2/Useful Plugins` | **none** | 0 | 0 | none |

