# Limitations: sourced from the codebase, first pass

18 docs (9 command/runbook pairs, V1 and V2) gained a `Limitations` section, each sourced from
the plugin or CLI-core code that implements the command, not written from the doc's own prose.
34 docs still lack one. 9 of those are the V0 legacy tree, out of scope for this project. The
remaining 25 were checked and no reviewed package yielded a claim solid enough to write down.

**The bar, same as Wave D's Troubleshooting and Examples passes:** a bullet needs a file and line
in the CLI source that states the constraint directly, either a closed `options` list on a flag,
an explicit "not supported" branch, or a validation rule that rejects otherwise-plausible input.
No bullet here is inferred from behavior the code doesn't state outright.

## Vetted against CLI-C15: none of the 18 turned out to be a vulnerability

Asked directly whether any of these 18 were a code vulnerability mislabeled as a limitation, not
a product limitation, each was re-checked past the matched line into the surrounding function.
Two needed a second check because the underlying feature handles a credential:

- **Configure MFA Secret.** The base32 format requirement is a limitation. Checked separately: the
  secret is read only from `process.env.CONTENTSTACK_MFA_SECRET` in `mfa-handler.ts`. No `--secret`
  flag exists, and nothing is written to disk. Nothing to correct.
- **Configure Proxy Settings.** The `http`/`https`-only restriction is a limitation. Checked
  separately: the proxy password goes through `configHandler.set`, backed by `cli-core`'s
  `contentstack-utilities/src/config-handler.ts`, which encrypts its config file by default
  (`ENCRYPT_CONF` defaults to `true`). Nothing to correct.

The other 16 are closed lists or unsupported-operation statements with no credential-handling
angle at all (rate-limit names, region values, GitHub repo visibility, CSV export scope, audit
fix-only field types, taxonomy publish modes). This check, and the rule that now requires it going
forward, is `CLI-C15` in `cli-common-rules.md` (registry `CLI-20`).

## What shipped, with sources

| Doc | Finding | Source |
|---|---|---|
| Bulk Operations in CLI | `--retry-failed`/`--revert` and cross-publish are not supported for `cm:stacks:bulk-taxonomies`. Term-level publish is not supported by the API. | `contentstack-bulk-operations/src/commands/cm/stacks/bulk-taxonomies.ts:48`, `src/messages/index.ts:365-366`, `src/utils/taxonomy-publish-parse.ts:4` |
| Configure Proxy Settings in CLI | `--protocol` accepts only `http` or `https`. No SOCKS support. | `cli-core/packages/contentstack-config/src/commands/config/set/proxy.ts` |
| Configure Rate Limits in the CLI | `--limit-name` accepts only `getLimit`, `limit`, `bulkLimit`. `--utilize` must be 0-100. | `cli-core/packages/contentstack-config/src/commands/config/set/rate-limit.ts`, `src/utils/common-utilities.ts:1` |
| Configure Regions in the CLI | The region argument is a closed 10-value list. A custom region requires `--cda`, `--cma`, `--ui-host`, `--name` together, no partial override. | `cli-core/packages/contentstack-config/src/commands/config/set/region.ts` |
| Configure MFA Secret Using CLI | The secret must be base32 (A-Z, 2-7), 16+ characters before padding, or it is rejected before a code is generated. | `cli-core/packages/contentstack-auth/src/utils/mfa-handler.ts` |
| Migrate Selected Content Using the Query Export Plugin | `--query` filters content types only, not entries within a content type. Asset-folder filtering is not supported. | `troubleshooting/troubleshooting-revamped/export-import-commands/04-no-support-custom-filtered-exports.md` (Case 50983), cross-checked against the same limitation already live on `Query-based Export.md` |
| Import Content Using the Seed Command | The source must be a public GitHub repository. Seed authenticates to Contentstack, not GitHub. | `contentstack-seed/src/seed/github/client.ts` (unauthenticated GitHub API calls throughout) |
| Export Content to CSV File Using the CLI | `--action` accepts only `entries`, `users`, `teams`, `taxonomies`. No CSV export for assets, content type schemas, or global fields. | `contentstack-export-to-csv/src/commands/cm/export-to-csv.ts:104` |
| Update Missing Reference UIDs for Entries, Assets, and Extensions | `--fix-only` repairs `reference`, `global_field`, `json:rte`, `json:extension`, `blocks`, `group`, `content_types` only. | `contentstack-audit/src/config/index.ts:17` (`fix-fields`) |

## Ruled out, not just unchecked

Two candidates looked like real limitations and turned out not to be, once read past the title:

- **"Bulk Re-Publishing Entries Is Not Supported via CLI"** (`troubleshooting-revamped/export-import-commands/05-...`). The article's own root cause says the opposite: `cm:stacks:bulk-entries --operation publish` does this today. Not used.
- **"CLI 2.x Asset Management Beta Features Are Not Yet GA"** (`troubleshooting-revamped/cli-feature-availability/01-...`). The root cause again says the opposite: both the standard asset export and CS Assets are GA in the current CLI. Not used.

An earlier read of these two, before opening them, assumed the titles matched real gaps. They didn't. Read the root cause before citing an article as a source, not the title.

**"Title Field Cannot Be Made Non-Unique"** is real (server-side, not CLI-side) but has no clean target doc: it isn't specific to any of the 25 remaining CLI-doc gaps, and forcing it into one would misattribute a platform constraint to a CLI flag. Left out.

## Deferred, 25 docs (V0's 9 excluded)

Checked and found nothing solid enough to write:

- **Cloning a Stack** (V1, V2), **Generate Typescript Typings with TSGen Plugin** (V1, V2), **Configure CLI Logging Preferences** (V1, V2), **Configure Early Access in the CLI** (V1, V2), **CLI Authentication and Adding Tokens** (V1, V2): `contentstack-clone`, `contentstack-cli-tsgen`, and the `config:set:log` / `config:set:early-access-header` / `auth` commands in `cli-core` were searched with the same patterns as the docs above. No closed list, no explicit "not supported" branch, no rejected-input rule. `config:set:log`'s `level` flag is a plain enum (`debug`/`info`/`warn`/`error`), which is normal command surface, not a coverage gap.
- **Compare and Merge Branches Using the CLI** (V1, V2), **Branches | Migration Use Cases** (V1, V2): `contentstack-branches` was searched the same way. Nothing beyond internal pagination (`skip`/`limit`) and generic "no merge job found" errors, neither of which is a documented constraint a reader needs to plan around.
- **Entry Migration** (V1, V2), **Migrate your Content using the CLI Migration Command** (V1, V2): `contentstack-migration` yields only input-validation throws (missing config, missing file), not a coverage gap.
- **Migrate Content Between Stacks Using the CLI** (V1, V2), **Migrate and Overwrite Content in the Same Stack** (V1, V2): both compose export and import. The management-token stack-settings gap found in `contentstack-export`/`contentstack-import` (see below) was considered for these, but neither doc's Prerequisites states which auth method the reader uses, so applying a management-token-specific caveat here would be a guess about the reader's setup, not a documented fact about the doc.
- **Create Custom CLI Commands**, **Create Custom CLI Plugins for Contentstack** (V1, V2): plugin-authoring guides, not command surface. Out of scope for this pass. `Create Custom CLI Commands` is a separate retire candidate already tracked (Slack thread, 2026-09-02).

## Found, but with no gap doc to carry it

Real, sourced, and left unused only because the target already has a `Limitations` section (so this pass didn't touch it) or the finding fits an existing section better as an addition than a new one:

- **Export/Import stack settings require a logged-in session.** Both `contentstack-export/src/export/modules/stack.ts:83-86` and `contentstack-import/src/import/modules/stack.ts:43` skip exporting or importing stack settings when authenticated with a management token, falling back to a stack.json built from the API key alone. `Export Content Using the CLI` and `Import Content Using the CLI` already carry `Limitations` sections and weren't in this pass's scope, but this is a real, undocumented gap in both. Worth a follow-up addition, not a new section.
- **Import skips private marketplace apps it cannot access** (`contentstack-import/src/import/modules/marketplace-apps.ts:602`, `skipped - private app not allowed`). Same situation: `Import Content Using the CLI` already has a `Limitations` section this could extend.
- **Taxonomy localization depends on the org's plan** (`contentstack-export/src/export/modules/taxonomies.ts:296-313`): if the plan doesn't include it, export falls back to non-localized taxonomies silently. Relevant to `Bulk Operations in CLI`'s taxonomy coverage and to the Export/Import docs, not written in anywhere yet.
