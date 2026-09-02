# CLI Structure Review: Deliverables Index

Everything produced by the audit pass, mapped to the six items on the developer ticket.

Nothing in this pass changed a published doc or wrote to the CMS. Every CMS call was a GET. The reports say what should change and, where the answer is verified, exactly what to change it to.

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

Three new doc types under `doc-standards/cli-templates/`, plus `cli-common-rules.md` holding the ten rules that apply across all three, wired into the existing linter:

| Type | Docs | Grouping rule |
|---|---|---|
| `cli-command-reference` | 43 | Commands appear as H3 in the order the plugin's `src/commands/` tree declares them. Single-command docs use the fixed facet order Syntax, Flags, Configuration File, Output, Examples, as bold lead-ins |
| `cli-task-runbook` | 24 | Exactly one procedure spine, ordered by execution rather than by namespace |
| `cli-module-reference` | 6 | Command and module H2s use the real identifier verbatim, in one contiguous lexicographic run, with structural and cross-cutting sections exempt |

`cli-common-rules.md` is a delta on `sdk-templates/common-rules.md`, not a replacement. It carries the rules that are true of the CLI regardless of which template a doc follows: headings stop at H3, flag tables use `Flag | Type | Required | Default | Description | Notes`, the baseline prerequisite order, and six settled style conventions each recorded with the corpus split that motivated it.

Three archetypes reuse product-wide types instead of getting their own: `setup-guide` (2 docs), `feature-doc` (2), `migration-guide` (1). Two stubs get no type and are retire candidates.

**The grouping question the ticket left open is settled.** Namespace grouping is not universal. It works for exactly one archetype and for the V1-to-V2 migration guide, whose subject is the entire command surface. For any narrower subject the oclif tree is either too coarse (50 files sit under `cm`) or too fine (one node supplies no ordering). The reasoning and the per-archetype rules are in [cli-template-research.md](../others/cli-template-research.md).

### 2. Linter support

- `doc-standards/scripts/checks/cli-specific.js`, 14 registered rules `CLI-01` through `CLI-14`, 7 of them machine-checked and 7 in the manual review queue.
- Doc-type detection extended, keyed off each doc's **subject** rather than its current structure, so a doc missing its `Commands` section is still linted as a command reference and the omission is reported.
- Heading depth is gated on subject rather than on type, so a CLI doc typed `migration-guide` or `feature-doc` is still checked. That one change is what surfaces the 43 unlinkable headings in the V1-to-V2 migration guide.
- 19 tests pass, 10 of them new.

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
