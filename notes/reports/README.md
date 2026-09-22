# CLI Structure Review: Deliverables Index

Everything produced by the audit pass, mapped to the six items on the developer ticket.

The audit itself made only GET calls. Content changes were applied later, to `docs/json` and then to the CMS **staging and development** environments only. Production is approval gated and is the docs owner's call, so nothing here reaches the live site. See [Production is approval gated](#production-is-approval-gated-which-changes-what-deploy-means).

---

## The ticket, item by item

| # | Ticket item | Status | Where |
|---|---|---|---|
| 1 | Ensure each doc follows a consistent template | **Answered and enforceable** | [Templates](#1-templates), [section-order report](cli-section-order-report.md) |
| 2 | Check logical grouping and hierarchy of commands | **Answered** | [Template research](../others/cli-template-research.md), sections 4 and 5 |
| 3 | Identify and fix broken internal cross-links | **Identified, with verified fixes. Not applied** | [links-confirmation.md](links-confirmation.md) |
| 4 | Find and address orphaned pages | **Found. Not addressed, all fixes are CMS writes** | [cli-orphan-report.md](cli-orphan-report.md) |
| 5 | Ensure all docs have a Prerequisites section | **Answered, and checked against source rather than prose** | [cli-prerequisites-report.md](cli-prerequisites-report.md) |
| 6 | Flag inconsistent section ordering | **Answered, and now machine-checked** | [cli-section-order-report.md](cli-section-order-report.md) |
| + | Not on the ticket: is what the docs say **true** | **Checked and fixed** | [cli-flag-accuracy-report.md](cli-flag-accuracy-report.md) |
| + | Not on the ticket: does a doc deny its own documentation exists | **Found and fixed, rule added** | [Absence claims](#absence-claims-the-cheapest-defect-with-the-highest-cost) |

---

## What was built

### 1. Templates

Three new doc types under `doc-standards/cli-templates/`, plus `cli-common-rules.md` holding the twelve rules that apply across all three, wired into the existing linter:

| Type | Docs | Grouping rule |
|---|---|---|
| `cli-command-reference` | 43 | Commands appear as H3 in the order the plugin's `src/commands/` tree declares them. Single-command docs use the fixed facet order Syntax, Flags, Configuration File, Output, Examples, as bold lead-ins |
| `cli-task-runbook` | 24 | Exactly one procedure spine, ordered by execution rather than by namespace |
| `cli-module-reference` | 6 | Command and module H2s use the real identifier verbatim, in one contiguous lexicographic run, with structural and cross-cutting sections exempt |

`cli-common-rules.md` is a delta on `sdk-templates/common-rules.md`, not a replacement. It carries the rules that are true of the CLI regardless of which template a doc follows: headings stop at H3, flag tables use `Flag | Type | Required | Default | Description | Notes`, the baseline prerequisite order, six settled style conventions each recorded with the corpus split that motivated it, and two rules against stale claims.

Three archetypes reuse product-wide types instead of getting their own: `setup-guide` (2 docs), `feature-doc` (2), `migration-guide` (1). Two stubs get no type and are retire candidates.

**The grouping question the ticket left open is settled.** Namespace grouping is not universal. It works for exactly one archetype and for the V1-to-V2 migration guide, whose subject is the entire command surface. For any narrower subject the oclif tree is either too coarse (50 files sit under `cm`) or too fine (one node supplies no ordering). The reasoning and the per-archetype rules are in [cli-template-research.md](../others/cli-template-research.md).

### 2. Linter support

- `doc-standards/scripts/checks/cli-specific.js`, plus 16 registered rules `CLI-01` through `CLI-16`. 8 are machine-checked and 8 sit in the manual review queue. The registry holds 109 rules in total.
- Doc-type detection extended, keyed off each doc's **subject** rather than its current structure, so a doc missing its `Commands` section is still linted as a command reference and the omission is reported.
- Heading depth is gated on subject rather than on type, so a CLI doc typed `migration-guide` or `feature-doc` is still checked. That one change is what surfaces the 43 unlinkable headings in the V1-to-V2 migration guide.
- 21 tests pass, 12 of them new. Two feed the linter the exact sentence that shipped on the Install pages and assert `CLI-16` fires, so the rule is known to have teeth rather than merely to pass.

**Three pre-existing bugs fixed along the way:**

- `build/build-section-order.js` still resolved the seven product-wide types and `section-matrix.md` against `doc-standards/` after they moved into `sdk-templates/`. The build failed outright on the first file, so no template change could take effect.
- `checks/troubleshooting-format.js` required the literal `**Root Cause(s)**` while `common-rules.md` mandates `**Root Cause**` or `**Root Causes**`. Every doc following the written standard was failing a tier-1 check.
- `checks/front-matter.js` demanded `title`, `description`, `url`. Docs mirrored from the CMS carry `uid`, `seo_title`, `seo_description`, so all 82 CLI docs were reporting three spurious errors each.

---

## Headline findings

**One page breaks 26 links across the corpus.** `CLI Authentication and Adding Tokens`, in both versions, documents all seven `auth:*` procedures at H4. The docs renderer emits anchor ids for H2 and H3 only, so none of them can be linked to and none appears in the page's own navigation. `#login` and `#add-management-token` are part of the Prerequisites boilerplate most command docs copy, which is how one page's heading levels break links everywhere else. Promoting four headings to H3, in both versions, fixes 26 of the 30 blocked links.

**179 headings in total sit below the linkable depth.** The 18 in `CLI Authentication and Adding Tokens` and `CLI for Launch` are the ones that already break a link. The rest break nothing today only because nothing links to them yet, which is itself the problem: they are absent from their own page's navigation. Headings now stop at H3 across every CLI doc, with a bold lead-in where a fourth level is genuinely needed. The largest concentrations are the V1-to-V2 migration guide at 43, `Content Type Plugin` at 24 per version, and `Create Custom CLI Plugins` at 18.

**Anchor ids cannot be computed offline.** Verified on live pages: the same construct produces different ids on different pages (`Bulk Publish/Unpublish Limitations` becomes `bulk-publish-unpublish-limitations`, but `Bulk Unpublish Entries/Assets` becomes `bulk-unpublish-entriesassets`). Every recommended URL in the links report was fetched and confirmed against the live page rather than derived.

**The flag table has no agreed shape.** 16 distinct column signatures across 82 docs, and none matches the mandated shape. That shape is now `Flag | Type | Required | Default | Description | Notes`, which extends C9's four columns with the two the CLI actually needs: the CLI declares 62 explicit flag defaults across its V2 plugins, and 106 of the 167 existing tables already document Type and Default. The six-column shape is therefore both stricter and cheaper to reach than the four-column one it replaces.

**Three live pages are missing from the sidebar**, and the CLI docs have no landing page: `/docs/headless-cms/cli` returns 404 because the entry exists but was never published and holds no content, while three source repo READMEs send readers there.

**GA changes to check against the docs.** CLI 2.0.0 shipped 2026-08-13. All 13 machine-checkable changelog claims were verified against the `oclif.manifest.json` inside each published npm package, and **none is contradicted**: `--api-version` is gone from the two bulk commands, tsgen's `--token-alias` is now `--alias`, `auth:tokens:list` and `cm:stacks:bulk-taxonomies` exist, and `--skip-taxonomy-publish`, `--cs-assets` and `--auth-api` are all present.

**Four claims are true but partial, and the changelog wording overstates them.** The short-flag removals are real but selective: `cm:stacks:export` dropped `-A -B -m -s -t` and kept `-a -c -d -k -y`. So "in favor of long-form only" is misleading, and the three flags the changelog cites as examples are three that kept their short forms. `Migrate from Contentstack CLI V1 to V2` already records the exact per-command removals correctly, and its Type Mapping Reference matches the published packages flag for flag. The correction belongs in the changelog, not the docs.

---

## Accuracy, which the ticket did not ask for

The six ticket items are all about structure. Partway through, the flag inventory made a different question answerable: **is what the docs say true.** It is a sharper question, because a missing Troubleshooting section is untidy while a flag that does not exist sends the reader to a command that fails.

**Ground truth is the `oclif.manifest.json` inside each published npm tarball**, which is what the released binary exposes. Not the local repo: `repo/cli-plugins` sits on `v2-dev` with no `v2.0.0` tag, and its export plugin is at `2.0.0-beta.24`.

**One doc would have broken a reader's command.** `Migrate your Content using the CLI Migration Command | V2.x.x` documented `--config-file`, which GA removed, and described `--config` as taking inline configuration, which is now `--inline-config`. Both worked examples were wrong. The root cause is that the page was created from its V1 page, and the V1 page is correct: `cm:stacks:migration` moved its configuration interface underneath the text.

**`--config` kept its name and changed its meaning**, which is the one defect class no name diff catches and no reader can detect, since a V1 script still parses and GA reads the string as a file path. It is the only flag in the CLI surface that did this, and it had slipped through the changelog and the migration guide as well as the doc. `CLI-C11` now states the rule that catches it.

Fixed in the same pass: 22 GitHub links pinned to the `v2.0.0-beta` tag of a repo that no longer holds that code, 5 links into TypeScript source pinned to a raw commit SHA (a C6 violation), a beta version number given as a release boundary, and a V1 link inside a V2 page. All verified over HTTP after rewriting.

**The changelog was corrected too**, drafted locally in `docs/json/changelog/`. Four short-flag claims were true but partial, with the three flags they cited as examples being three that kept their short forms, and four changes were missing entirely including the migration breaking change.

---

## Absence claims: the cheapest defect with the highest cost

Found from a Slack thread rather than from any check, which is the point.

**Both `Install the CLI` pages told readers the plugin guide did not exist.** The note sat in their `Namespaces` section:

> **Note**: The guide to create your own plugin within `csdx` is yet to come. But, as our CLI is built using the oclif package, you can create your custom plugin by referring to [oclif plugin documentation](https://oclif.io/docs/plugins).

`Create Custom CLI Plugins for Contentstack` had shipped in both versions by then, roughly 1,030 lines for V2 and 770 for V1, both live on production and both in the sidebar. A developer looking for CLI 2.0.0 plugin information read the note, concluded Contentstack had no plugin documentation, and built their plugin from the source repo and oclif's own docs. They told us. Nobody found it from our side.

**A sentence describing a gap outlives the gap.** Nothing in the authoring workflow points back at a page that merely mentions the absence of a guide, so the note survived both guides being written. `CLI-C12` and registry rule `CLI-16` now ban the pattern, enforced through `banned-phrases` so it applies to every doc type rather than only the three CLI types. The Install pages are typed `setup-guide`, so a CLI-scoped rule would have missed the two docs that motivated it.

**Zero docs linked to either guide.** Discovery depended entirely on the sidebar and site search. Three docs now link it in prose, and each Next Steps entry carries a description, which took two tier-1 `C1-06` findings off the board at the same time.

**The migration guide's plugin-author checklist had one item.** Bump Node to 22. Four more author-facing breaking changes were sitting documented in the V2 authoring guide and absent from the checklist: `@oclif/core` v3 to v4, the new `~2.0.0` Contentstack dependencies, `oclif.commands` moving to the compiled `./lib/commands`, and `@oclif/test` v4 deleting the chained test API.

**`Create Custom CLI Commands` documents a command that has never existed.** Its step one is `csdx plugins:create`. `@oclif/plugin-plugins` ships `index`, `inspect`, `install`, `link`, `reset`, `uninstall` and `update` and nothing else, verified against the published tarballs at majors 1, 2, 3 and 5, and both CLI 1.68.0 and 2.0.0 depend on `^5.4.x`. The page is retired rather than repaired, because everything else it covers is already in the plugins guide.

**The local mirror carried it twice.** `docs/json` and `docs/markdown` held byte-identical copies under both `Version 1.x.x/Miscellaneous` and `Version 2.x.x/Miscellaneous V2`, while the live sidebar only ever had it under V1. The V2 copy and its `index.json` row are removed, taking the mirror from 94 entries to 93. The V1 copy stays until the release deploys, because production still serves the page until then. `rebuild_cli_docs_tree.py` builds folders from the live nav's `nested_links`, so once deployed a rebuild produces no row for it in either tree.

**Two things that retirement uncovered.** `scripts/fix_create_custom_cli_commands_url.py --redirects` was pending and would have made that page reachable, so it is now guarded and refuses to run. And `RELEASE_CLEANUP_NAV` already carried the legacy redirect at v3 and deployed, yet `/docs/developers/cli/create-custom-cli-commands` still 404s: the release published v3 unchanged, because the content edit had never been made. It is made now, staged at v4.

---

## Production is approval gated, which changes what "deploy" means

Found while deploying the retirement release, and it applies to every production change in this stack.

**A successful `POST /v3/releases/{uid}/deploy` does not mean anything is live.** The release locks, the API returns success, and the items land in the publish queue as:

```
"publish_details": {
  "status": "pending_approval",
  "message": "Entry has not received the required approval(s).",
  "error": "The request cannot be processed as approval is pending."
}
```

**Staging and development are not gated.** Publishes there return `status: success` immediately, which is why every write script in `scripts/` can target them directly. Only production (`bltfe8376c13fe85b9c`) holds items for approval.

**So an approver has to act in the Contentstack UI, under Publish Queue, before the live site changes.** `scripts/deploy_release.py` reads the queue back after submitting and quotes the real per-item status, because reporting "deployed" on the strength of the POST alone is a false report. Its first version did exactly that and was corrected.

**This tooling now refuses production outright.** That is the docs owner's standing instruction, and it matches what the server does anyway. `deploy_release.py` defaults to staging and development and rejects `--env production` even with `--confirm`. The handover to production is a release uid, not a deploy: the docs owner approves it in the UI.

This also explains a long-standing puzzle. `RELEASE_CLEANUP_NAV` is locked, so it looked deployed, yet `/docs/developers/cli/create-custom-cli-commands` kept returning 404. Two separate causes: the release carried `blt0d2ab10c0fa412a8` at v3 with the content edit never made, and a locked release is not proof its items were approved.

---

## The restructure, wave by wave

Errors fell from **831 to 499** across the six waves. The count is a rough guide, not the point: during Wave C two table columns were destroyed and the count went **down**, because deleting content deletes the problems in it. Every wave is verified by a word-level audit instead.

| Wave | What it did | Result |
|---|---|---|
| A | Heading depth. 179 unlinkable H4s became H3s or bold lead-ins, 32 docs gained an `Overview` over prose that already existed, plurals normalised | 50 docs |
| B | Section order. 4 out-of-order pairs and 7 forbidden `Quick Start` headings | both now zero |
| C | Flag tables reshaped to `Flag \| Type \| Required \| Default \| Description \| Notes` | 26 converted, 35 deferred, 106 config tables exempt |
| D | The missing sections. `Commands` and `Steps for Execution` where the content existed, 25 `Next Steps`, 8 `Examples` | 42 and 24 deferred with reasons |
| E | Module references. 4 `Quick Reference` index tables, plus a wrong Node.js requirement | `C2-04` reaches zero |
| F | Links and anchors | **not started**, and it cannot be until this ships |

**Wave B was planned wrong, and the correction is worth more than the wave.** It was scoped as 263 reorders because `C1-01` was the largest rule count and its rule text is about ordering. Every one of those 264 findings actually reads `Required section "X" is missing`. `compareOrder` was tested against deliberately reversed input to prove the zero was real: the CLI docs were already in the mandated order. Those findings belonged to Wave D.

**Why Wave F has to be last, and why it is blocked.** Anchor ids are generated at render time, so every fix has to be confirmed against a rendered page. `dev-www` runs an older build that emits no heading anchors at all, and `stag-www` returns 401. So Wave F can only be verified once the restructure is live on production, which needs an approval this tooling cannot grant.

## Where the quality bar was held rather than the count

Three places where moving the number down was the wrong answer.

**42 of the 67 `Next Steps` sections were not written.** A doc gets one only when at least 2 sourced links survive **and** at least one is specific to that doc. "How to upgrade" plus "coverage gaps" is true and relevant, but it is the same pair on every page, so on its own it is padding dressed as a section.

**24 of the 32 `Examples` sections were not written.** V1 docs get none at all, because the only verified flag data is from the published **2.0.0** manifests and putting a 2.0.0 example on a V1 page is the `CLI-C11` defect exactly.

**53 `Troubleshooting` and 43 `Limitations` sections are still absent.** The plugin sources yield 18 thrown error messages and around 120 error call sites across 47 docs that need one. Some docs have none. A fabricated root cause reads exactly as authoritative as a real one and the reader cannot tell, so the section is omitted and the linter keeps reporting it.

## 2026-09-02 update: Troubleshooting and Next Steps are no longer required on CLI docs

The docs owner corrected the plan above. `Troubleshooting` was never meant to be a per-page CLI section: the corpus already has a dedicated troubleshooting hub (`troubleshooting/`, 30 ticket-sourced articles). `cli-templates/cli-common-rules.md` CLI-C14 now routes new failure modes there, and `Troubleshooting` is `Recommended` rather than `Required` in `cli-command-reference.md` and `cli-task-runbook.md`. The 25 `Next Steps` sections this project had written were reverted (`scripts/revert_wave_d2_next_steps.py`) after the bar that produced them turned out to leave 42 of 67 candidate docs with only a generic, non-doc-specific pair of links. `Next Steps` is `Recommended` across all three CLI types now. **The 22 pre-existing Troubleshooting sections and 16 pre-existing Next Steps sections, written before this project touched anything, are unaffected.**

`Limitations` stayed `Required`, and got a first real pass: 18 docs (9 command/runbook pairs) gained a sourced `Limitations` section, drawn from the plugin and CLI-core source rather than from the doc's own prose. See `notes/reports/limitations-pass.md` for the sources, what was ruled out on closer reading, and what is still deferred (25 docs beyond the V0 legacy tree).

`Compare and Merge Branches Using the CLI` (V1, V2) was retyped from `cli-command-reference` to `cli-task-runbook`: it has five `Steps to <X>` H2s and no `Commands` or `Options` section, which is a runbook shape the type detector didn't recognize. `lint-doc.js`'s `detectCliDocType` now checks for two or more `Steps to` headings with no `Commands`/`Options` section alongside it. The migration guide's existing "Running V1 and V2 Side by Side" content was promoted to a `## Gradual Migration` H2, the one `migration-guide` section that was missing.

## 2026-09-03 update: Troubleshooting removed outright, and a limitation-versus-vulnerability rule

The `Recommended` middle ground above did not hold. The docs owner corrected it again: `Troubleshooting` is not carried on any CLI doc at all, not Required, not Recommended. The 22 pre-existing sections that the update above left untouched were removed. `cli-command-reference.md` and `cli-task-runbook.md` no longer list `Troubleshooting` in their Section Order tables, CLI-C14 in `cli-common-rules.md` was rewritten to state the rule plainly, and a new machine check, `CLI-19` in `checks/section-structure.js`, reports a `Troubleshooting` H2 added back to any CLI doc.

That check turned up an edge case worth recording: three real CLI docs are typed under a product-wide template that still requires Troubleshooting for the non-CLI docs that share it (`Install the CLI` as `setup-guide`, `CLI for CS Assets` and `Asset Scanning in CLI` as `feature-doc`, the V1-to-V2 migration guide as `migration-guide`). Removing their Troubleshooting content made all three newly fail `C1-01`. Fixed by keying the exemption off `isCli`, the same content-based signal `checkCliSpecific` already uses for H4 depth, rather than off `docType`, so the skip applies to any CLI doc regardless of which template it is checked against.

The other half of this update is a new rule rather than a content change. Before this session wrote 18 `Limitations` bullets sourced from the plugin and CLI-core code, it was asked to check whether any of them were actually describing a code vulnerability rather than a product limitation, since the two read as the same sentence shape from outside the code ("the CLI cannot do X"). Re-reading each finding's surrounding code rather than just the matched line: the MFA secret's base32 format check is a limitation, and it is only safe to call one because the secret is read solely from `CONTENTSTACK_MFA_SECRET`, never a bare flag, never written to disk. The proxy protocol restriction is a limitation, and the stored proxy password was checked too, the underlying config store encrypts its file by default. Neither turned out to be a vulnerability, so nothing was corrected, but the check itself is now a standing rule: `CLI-C15`, with a matching registry entry `CLI-20`, states the difference and requires it be checked before a code-sourced Limitations bullet is published, holding it back and routing it to the docs owner instead if a finding is a vulnerability or the source is unclear.

## Accuracy defects found during the restructure

Two that a reader would have hit, neither of them on the ticket.

**The Node.js requirement was wrong in both `CLI Limitations` pages**, in three places each. They said `18.0.0 or above (recommended: 20.x or 22.x)`. Checked against each published package's own `engines` field, 18 was never the floor: 1.40.0 to 1.60.0 declared `>=14.0.0`, and 1.65.0 onward declares `>=22.0.0`. A reader on Node 18 or 20 installs, and the CLI fails at runtime.

**`csdx plugins:create` has never existed.** It is step one of `Create Custom CLI Commands`. `@oclif/plugin-plugins` ships `index`, `inspect`, `install`, `link`, `reset`, `uninstall` and `update` and nothing else, at majors 1, 2, 3 and 5. That page is retired rather than repaired.

---

## Reproducing everything

```bash
# Links: live pass against production, then the cross-doc anchor pass
python3 scripts/sweep_cli_links.py --env prod
python3 scripts/cli_anchor_audit.py      # writes notes/reports/anchors.json
python3 scripts/gen_links_report.py      # writes links-confirmation.md

# Orphans, read-only CMS audit
python3 scripts/cli_orphan_audit.py --out notes/reports/cli-orphan-report.md

# Section order and consistency, all 82 docs
python3 scripts/gen_section_order_report.py

# Flag ground truth, then the accuracy check
python3 scripts/gen_flag_inventory.py --refetch
python3 scripts/gen_flag_accuracy_report.py

# Prerequisites, checked against the v2.0.0 git tag
python3 scripts/gen_prerequisites_report.py

# Linter self-test
cd doc-standards/scripts && npm run build:section-order && node --test

# Plugin guide discovery: the false note, the inbound links, the author checklist
python3 scripts/fix_plugin_guide_discovery.py            # dry run
python3 scripts/fix_plugin_guide_discovery.py --confirm

# Retire Create Custom CLI Commands. Staging and development directly,
# production staged in a release for a human to deploy.
python3 scripts/retire_create_custom_cli_commands.py            # dry run
python3 scripts/retire_create_custom_cli_commands.py --confirm
```

---

## What still needs a decision

Ordered by value. Every item is a write, so all of them need approval.

| # | Action | Type |
|---|---|---|
| 1 | Promote 4 headings to H3 in `CLI Authentication and Adding Tokens`, both versions | Content |
| 2 | Apply the 20 verified anchor fixes from the links report | Content |
| 3 | Add the RTE migration pages and Taxonomy Migration to the sidebar | Nav |
| 4 | Resolve `/docs/headless-cms/cli`, publish a hub page or add a redirect | Content or redirect |
| 5 | Work the nine GA changes the docs have not caught up with | Content |
| 6 | Add `Overview` headings above existing intro prose in 36 command references | Content |
| 7 | Convert the remaining 165 H4s to H3s or bold lead-ins | Content |
| 8 | Convert 167 flag tables to the six-column shape | Content |
| 9 | Write `Examples` sections for the 32 command references that have none | Content |
| 10 | Decide whether to retire `Useful Plugins` and `Uninstall CLI Plugins` | Content |
| 11 | Rename the `Content Migration Commands` folder, which holds command docs rather than version migration guides | Nav |
| 12 | **Deploy release `CLI retire create-custom-cli-commands 2026-09-02 [docs]`** (`blt709e2fb5f57c8659`). Already applied to staging and development. Three items: the nav node minus one row, an unpublish of `blt18f5edee45f9d6c2`, and the legacy redirect fixed. | Deploy |

Items 1 through 4 are small, high-value, and independently shippable. Item 5 is the one with a correctness deadline, since those docs currently describe flags that GA removed. Items 7 and 8 are the largest mechanical jobs. **Item 9 is the only one that needs new writing rather than restructuring**, which is why `Examples` was made Required rather than Recommended: a Recommended section is advisory and would have been skipped.
