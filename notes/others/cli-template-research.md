# CLI Template Research (WI-1)

Research output for WI-1 of `~/.claude/plans/cli-structure-review-developer-harmonic-ripple.md`. No files outside `notes/` were changed.

---

## 1. The answer, up front

**Namespace grouping does not work for all CLI docs. It works for exactly one of the six archetypes in the corpus. The plan's preliminary evidence is confirmed, and your instinct is correct: multiple CLI doc templates, each with its own grouping rule.**

But the corpus does not need five new templates. It needs **three new types plus three existing types reused**, because three of the six archetypes are already served by files that exist in `doc-standards/`:

| Archetype | Files | Distinct docs | Template |
|---|---|---|---|
| CLI Command Reference | 43 | 42 | **NEW** `cli-command-reference` |
| CLI Task Runbook | 24 | 20 | **NEW** `cli-task-runbook` |
| CLI Module Reference | 6 | 5 | **NEW** `cli-module-reference` |
| Setup Guide | 2 | 2 | **REUSE** `setup-guide.md` as-is |
| Feature Doc | 2 | 2 | **REUSE** `feature-doc.md` plus a CLI addendum |
| Migration Guide | 1 | 1 | **REUSE** `migration-guide.md` plus a CLI addendum |
| Unassignable stubs | 4 | 2 | No template. Merge into other docs (see 4.7) |
| **Total** | **82** | **74** | **3 new types** |

The single testable grouping rule that is genuinely namespace-derived belongs to **CLI Command Reference** only, and only in its multi-command branch. Every other archetype orders its sections by something else: execution order, lifecycle phase, setup sequence, lexicographic command id, or V1-to-V2 change area.

Deviations from the plan's five candidate archetypes, and why, are in section 4.8.

---

## 2. Evidence base

Every number below was measured first-hand for this note, not carried over.

**Method.** A fence-aware extractor walked all 82 files under `docs/markdown/Version 1.x.x/` and `docs/markdown/Version 2.x.x/`, tracking ``` and ~~~ openers so that `# comment` lines inside code blocks were never counted as headings. This matters: `Bulk Operations in CLI | V2.x.x.md` has 54 code fences, and a naive `grep '^#'` inflates its heading count badly. Commands were matched with the pattern `csdx <topic>[:<sub>]*` and cross-checked against the 66 command source files.

**Corpus shape.**

- 82 files, 27,659 lines total, 41 files per version.
- H2 per doc: minimum 0, median 5, maximum 21. Four files have zero H2. Eighteen files have 10 or more.
- All 8 V1 and V2 pairs the plan named were re-verified as byte-identical (one distinct MD5 per pair), so 82 files represent 74 distinct docs.
- 179 H4 headings live in 16 files. See section 6.
- Prerequisites heading level: 66 at H2, 4 at H3, 2 at H4. Twelve files have no Prerequisites heading at any level.

**The namespace test.** Mapping every doc to the oclif topics its documented commands belong to:

| Result | Files |
|---|---|
| Docs spanning 0 topics | 2 |
| Docs spanning exactly 1 topic | 42 |
| Docs spanning 2 or more topics | 38 |
| Docs that touch the `cm` topic | 50 |

50 of 82 files touch `cm`. A one-namespace-per-doc rule would collapse 61 percent of the corpus into a single bucket. 38 files span two or more topics, so for those the rule has no single answer at all. Worst cases: `Migrate from Contentstack CLI V1 to V2 | V2.x.x.md` spans 8 topics and 54 distinct commands, and `CLI Limitations` spans 7 topics and 30 commands in both versions.

**Command coverage gaps, from source.** 23 core command files in `repo/cli-core/packages/*/src/commands/**/*.ts` plus 43 plugin command files in `repo/cli-plugins/packages/*/src/commands/**/*.ts`.

- `migrate:audit`, `migrate:create`, `migrate:import`, and `migrate:status` have **zero mentions anywhere in the 82 docs**.
- `migrate:convert` and `migrate:export` are mentioned in exactly one doc, the V1-to-V2 migration guide. So the whole `migrate:` topic has no owning doc, confirming the plan.
- `cm:stacks:import-setup` appears in 11 files but owns none. It is a step inside `Overwrite Existing Content using CLI Import` (8 mentions), `Migrate and Overwrite Content in the Same Stack`, and `Migrate Selected Content Using the Query Export Plugin`, plus the two Limitations and two Configuration Reference pages.

**Flag and option table shapes.** Fence-aware table-header extraction found **20 distinct column signatures** on tables whose header mentions Flag or Option. Top six by table count:

```
 58  Option | Type | Default | Description
 48  Option | Type | Default | Required | Description
 29  Flag | Short Flag | Description
 12  Flag | Short | Type | Required | Default | Description
  4  Option | Description | Required
  4  Flag | Description | Example
```

The shape `common-rules.md` C9 actually mandates, `Flag | Required | Description | Notes`, occurs on **one table in the entire corpus**. Confirmed.

**Bundled plugin list, V2.** `repo/cli-core/packages/contentstack/package.json` declares `oclif.plugins` with 3 `@oclif/*` entries and 13 `@contentstack/*` entries. Local snapshot still reads `version: 2.0.0-beta.30`, `engines.node: >=22.0.0`, so the plan's "run the pull before WI-5" note stands.

**Canonical module order exists in source.** `repo/cli-plugins/packages/contentstack-export/src/config/index.ts:26` declares `modules.types` with 17 entries, and `repo/cli-plugins/packages/contentstack-import/src/config/index.ts:30` declares 18 entries in a **different order**. Two different orders means a Module Reference template cannot simply cite "the module order" without saying which one. This is why the Module Reference grouping rule below is lexicographic rather than declaration-ordered (section 5.3).

---

## 3. Verdict on the 7 existing doc-standards types

Read in full: `common-rules.md` (B1, B2, C1 through C9, Section Definitions), `section-matrix.md`, and all 7 type files.

### 3.1 `getting-started.md` (Get Started Guide) - NOT APPLICABLE

Its required spine is Role-Based Routing Table, then Quick Start, then Documentation Map, and RS3 forbids both Troubleshooting and Theory sections outright. **Zero of the 82 docs has a Role-Based Routing Table or a Documentation Map.** The two docs whose folder says "Get Started" (`Install the CLI`, `CLI Authentication and Adding Tokens`) are a setup guide and a command reference respectively, not routers. Worse, `detectDocType()` at `lint-doc.js:82` fires `getting-started` on any title starting "get started with", which no CLI doc does, so this type is inert on the corpus rather than harmful. Do not extend it. The genuine gap it points at is the **missing CLI section hub page** already logged in WI-6, and if that page is ever created, `getting-started` is the correct type for it.

### 3.2 `setup-guide.md` (Setup Guide) - REUSABLE AS-IS

`Install the CLI` V1 and V2 have H2s `Prerequisites`, `Install CLI`, `Verify installation`, `Namespaces`, `Check CLI Version`, `Update CLI Version`, `Next Step`. That is install, verify, configure, upgrade, which is precisely what `setup-guide.md` encodes, and its governing rule ("every main-content section ends with a verification step or a clear observable outcome") is exactly the rule `Verify installation` embodies. Both docs currently fail the template on three points (no `Overview`, no `Troubleshooting`, `Next Step` singular against a required `Next Steps`), which is the right outcome: the template is correct and the docs are non-compliant. **No CLI addendum needed.** Assign these 2 files to `setup-guide` and let the existing linter fire.

### 3.3 `feature-doc.md` (Feature Doc) - REUSABLE WITH A CLI ADDENDUM

Two docs describe a behavior that spans commands rather than a command surface: `Asset Scanning in CLI | V1.x.x.md` (H2s `Publishing With Scan-Gating`, `Import-Time Behavior`) and `CLI for CS Assets | V2.x.x.md` (H2s `Export CS Assets`, `Import CS Assets`, `Management Token Behavior`). Both already match the feature-doc spine of Overview, Prerequisites, main content, Troubleshooting, Next Steps, and `CLI for CS Assets` even carries a `Quick Decision Guide`. The addendum needed is small: feature-doc has **no Limitations row** in its Section Order table, while C9 mandates a Limitations section for CLI docs and `Asset Scanning` already has one. Add a CLI-scoped note to `feature-doc.md`'s Type-Specific Rules rather than a new type, because 2 docs cannot justify a fourth registration.

The real risk with feature-doc is the opposite one. `detectDocType()` at `lint-doc.js:98` returns `feature-doc` for anything with a `Commands` section or the word "plugin" or "command" in the title, which today swallows roughly half the corpus into the wrong type. The new `cli-command-reference` branch **must** be inserted above that line, as WI-2 step 6 already states.

### 3.4 `how-to-guide.md` (How-To Guide) - REUSABLE WITH A CLI ADDENDUM, but see 5.2

Its governing rule ("the developer must be able to complete the task by following the steps without leaving the page") is the right rule for the 24 runbook files, and its section list is nearly right. Two gaps make it insufficient on its own: it has **no Limitations row** (14 of the 24 runbook files already carry one, and C9 mandates it), and Troubleshooting is Optional where CLI runbooks that run destructive imports need it. Because Section Order tables are per-type and shared across all products, adding a Limitations row to `how-to-guide.md` would impose it on every non-CLI how-to guide too. That is why I recommend a new `cli-task-runbook` type instead, and why how-to-guide is the named fallback if you decide 3 new types is one too many.

### 3.5 `migration-guide.md` (Migration Guide) - REUSABLE WITH A CLI ADDENDUM

Exactly one doc matches: `Migrate from Contentstack CLI V1 to V2 | V2.x.x.md`. It already has `Overview`, `Quick Decision Guide`, `Prerequisites`, `Type Mapping Reference`, `Troubleshooting`, `Pre-Upgrade Checklist`, `Next Steps`, in that order. It is the single best-structured doc in the corpus against an existing standard. The addendum is two items. First, its `Command Reference` H2 with 55 H3s is a CLI-specific section the template does not name, so it currently lands in the pseudo-section `Main Content` bucket and gets no ordering check. Second, C8's Quick Decision Guide trigger reads "If multiple migration paths exist", which is the exact stale trigger the archived `doc-standards-amendment-proposals.md` flags: this doc is 1,509 lines covering one path across 27 commands, so the trigger never fires. Apply the proposed broadened trigger here.

### 3.6 `conceptual-guide.md` (Conceptual Guide) - NOT APPLICABLE

Its governing rule is "Do first, understand second, debug last", and its distinguishing feature is a `Theory Sections` slot placed after working setup. **No CLI doc in the corpus has a theory section.** The three docs that might look conceptual are all really lookup references (`CLI Limitations`, `Contentstack CLI Configuration Reference`, `CLI-Supported Features`) where a reader arrives with a specific module in mind and never reads top to bottom, so "do first" is the wrong governing rule. The one element worth borrowing is its `Quick Reference` row, which `Configure Proxy Settings` and `Content Type Plugin | V2.x.x` already use. Carry that row into the new types rather than assigning any doc here. Note that `conceptual-guide` is `detectDocType()`'s default fallthrough, so leaving it unmodified keeps the fallback harmless.

### 3.7 `kickstarter.md` (Kickstarter) - NOT APPLICABLE, but donate its Prerequisites rule

Its definition is "a starter app template that demonstrates a working integration", and its governing rule is that a developer with no prior context can clone, configure, and run using only this doc. The closest CLI doc is `Bootstrap Starter Apps` V1 and V2 (H2s `Using the Bootstrap Command`, `Run the Bootstrap Starter App`, `Run the Compass Starter`, `Deploy the Website`, `Supported Starter Apps`, `Limitations`). But that doc's subject is the `cm:bootstrap` command and the starters it scaffolds, not one starter repo, and it forbids Theory sections and Troubleshooting in ways that do not fit. It is assigned to CLI Task Runbook instead. What kickstarter contributes is its Prerequisites wording, "Blocking requirements with links: Node version, package manager, Contentstack stack setup", which is the closest existing text to the CLI baseline prerequisite chain and should be borrowed verbatim in the new types.

### 3.8 `section-matrix.md` - EXTEND, DO NOT REPLACE

One table, 15 section rows, 7 doc-type columns. `build-section-order.js:60-75` reads `doc.tables[0]` and slices `headerCells` after the first, so a new column is a header cell plus a value in all 15 rows. Three of its rows (`Role-Based Routing Table`, `Quick Start`, `Documentation Map`) are `Not used` for every CLI archetype, and three CLI-relevant sections are absent from the matrix entirely (`Commands`, `Installation`, `Quick Reference`). Add the three new columns and the three missing rows in WI-2. Note that the matrix is advisory: nothing in `lib/section-index.js` reads `section-matrix.json` for enforcement, only `section-order.json` drives `compareOrder()`.

---

## 4. Archetype clustering by observed structure

### 4.1 How the clusters were derived

Clustering was done on the **organizing axis** of the H2 sequence, not on folder, not on title. Five axes appear in the corpus:

| Axis | What orders the H2s | Archetype |
|---|---|---|
| A | Command identity, one section per sibling command | CLI Command Reference (multi branch) |
| B | Command facets: Syntax, Flags, Configuration File, Examples | CLI Command Reference (single branch) |
| C | Execution order: Step 1, Step 2, Step 3, or one Steps for Execution list | CLI Task Runbook |
| D | Module or command-config identity, lookup not narrative | CLI Module Reference |
| E | Setup sequence: install, verify, configure, upgrade | Setup Guide (existing) |
| F | V1-to-V2 change area | Migration Guide (existing) |

Axes A and B were **merged** into one archetype. Their section lists are identical (Overview, Prerequisites, Installation, Commands, Examples, Troubleshooting, Limitations, Next Steps). Only the content under the `Commands` H2 differs, and that difference is expressible as one conditional grouping rule (section 5.1) rather than two templates. Splitting them would double the registration cost for zero difference in required sections.

A sixth family, feature behavior across the export and import lifecycle, is 2 docs and maps onto the existing `feature-doc` rather than a new archetype.

### 4.2 CLI Command Reference (43 files, 42 distinct)

Proof docs, strongest first:

- `Content Type Plugin | V1.x.x.md` and `| V2.x.x.md`. The reference implementation. `Commands` H2, then 6 H3s that are **literal command ids** (`content-type:list`, `content-type:details`, `content-type:audit`, `content-type:compare`, `content-type:compare-remote`, `content-type:diagram`), each with the same 4 sub-blocks (`Syntax`, `Flags`, `Output`, `Examples`). Every command id maps to a file under `repo/cli-content-type/src/commands/`. This is axis A executed correctly, and it is the only doc pair that does so with literal ids.
- `Apps CLI Plugin | V1.x.x.md` and `| V2.x.x.md`. 8 H3s under `Commands` mapping one to one onto the 8 `app:*` command files (`app:create`, `app:get`, `app:install`, `app:update`, `app:deploy`, `app:reinstall`, `app:uninstall`, `app:delete`). Axis A with prose titles instead of ids.
- `CLI for Launch | V1.x.x.md` and `| V2.x.x.md`. 9 H3s covering the `launch` subcommands.
- The `config:` triad family, 9 files: `Configure CLI Logging Preferences` x2, `Configure Early Access in the CLI` x2, `Configure Proxy Settings in CLI` x2, `Configure Rate Limits in the CLI` x2, `Configure Regions in the CLI | V2.x.x.md`. Every one has a `Commands` H2 with exactly 3 H3s in Set, Get, Remove order, matching the `config:set:*`, `config:get:*`, `config:remove:*` triads in `repo/cli-core/packages/contentstack-config/src/commands/`. This is the cleanest axis-A evidence in the corpus and it is namespace-derived by construction.
- Axis B, single command with a large flag surface: `Export Content Using the CLI` x2 (`cm:stacks:export`), `Import Content Using the CLI` x2 (`cm:stacks:import`), `Export Content to CSV File Using the CLI` x2 (`cm:export-to-csv`), `Cloning a Stack` x2 (`cm:stacks:clone`), `Query-based Export` (`cm:stacks:export-query`), `Generate Typescript Typings with TSGen Plugin` x2 (`tsgen`), `Import Content Using the Seed Command` x2 (`cm:stacks:seed`).

### 4.3 CLI Task Runbook (24 files, 20 distinct)

Proof docs:

- The `Steps for Execution` family, 8 files with near-identical shape: `Change Master Locale` x2, `Entry Migration` x2, `Update Missing Reference UIDs for Entries, Assets, and Extensions` x2, `Migrate Content Between Stacks Using the CLI` x2. H2 sequence is Prerequisites, Steps for Execution, Troubleshoot, and sometimes Limitations. Three of these four pairs are byte-identical across versions.
- The numbered-step family: `Migrate and Overwrite Content in the Same Stack` x2, whose H2s are literally `Step 1: Export Content (If Not Already Exported)`, `Step 2: Run Import Setup`, `Step 3: Import with Overwrite`.
- The authoring lifecycle family: `Create Custom CLI Commands` (H2s `Use the "plugins:create" command`, `Run the Code`, `Set up the Plugin`, `Register and Install the Plugin`, `Uninstall the Plugin`) and `Create Custom CLI Plugins for Contentstack` x2 (`Plugin Structure`, `Creating a Plugin`, `Plugin Registration and Linking`, `Commands and Flags`, `Testing`, `Publishing the Plugin`). Both are execution-ordered, so axis C.
- `Bootstrap Starter Apps` x2, whose H2s run scaffold, then run, then deploy.

### 4.4 CLI Module Reference (6 files, 5 distinct)

Small in file count but **5,736 lines, 20.7 percent of the entire corpus**, and it contains the three worst pages.

Proof docs:

- `CLI Limitations | V1.x.x.md` (1,386 lines, 20 H2, 57 H3, only 6 code fences) and `| V2.x.x.md` (1,349 lines, 21 H2, 55 H3). Every H2 is `<Module> Limitations`: Core, Authentication, Export, Import, Import Setup, Overwrite Operations, Bulk Publish/Unpublish, Clone, Branch, Launch, Migration Scripts, Bootstrap, Seed, RTE Migration, Entry Migration, Audit, Variants, Apps CLI, TSGen, Configuration. Pure axis D.
- `Contentstack CLI Configuration Reference.md` (1,145 lines, 10 H2, 49 H3, byte-identical across versions). Every body H2 is `<Command> Configuration`: Export, Import, Audit, Query-Export, Import-Setup, Migration. Each maps to a command that accepts `--config`. Pure axis D. Zero Commands section, zero Prerequisites.
- `CLI-Supported Features for Export, Import, and Clone Operations` x2. H2s `Supported Modules`, `Marketplace Apps`, `Personalize and Entry Variants`, `CS Assets`, `Module-Wise Operations`, `Error Handling`. A support matrix indexed by module.

### 4.5 Setup Guide, existing type (2 files, 2 distinct)

`Install the CLI | V1.x.x.md` and `| V2.x.x.md`. Justified in 3.2. Notable detail: their `Namespaces` H2 is the **only place in the corpus where the oclif topic tree appears as doc structure**, and it appears as a flat table, not as headings. That is a useful precedent: the namespace tree belongs in a table, not in a heading hierarchy.

### 4.6 Feature Doc and Migration Guide, existing types (3 files, 3 distinct)

`Asset Scanning in CLI | V1.x.x.md` and `CLI for CS Assets | V2.x.x.md` to `feature-doc`. `Migrate from Contentstack CLI V1 to V2 | V2.x.x.md` to `migration-guide`. Justified in 3.3 and 3.5.

### 4.7 Docs that fit no archetype, and what to do

Four files, 2 distinct docs. Both have **zero H2 headings**, so no Section Order table can ever apply to them.

**`Useful Plugins.md` (12 lines, 0 H2, 0 code fences, 0 commands, byte-identical across versions).** It is one paragraph and one bullet linking to `contentstack-cli-tsgen` on npm. That link duplicates the entire subject of `Generate Typescript Typings with TSGen Plugin`, which already exists as a full Command Reference doc in both versions.
**Recommendation: retire the page.** Move its one link into the `Next Steps` of `Create Custom CLI Plugins for Contentstack | V2.x.x.md`, which is the doc a reader looking for community plugins actually needs. Log it as a retire candidate for WI-6 rather than templating it.

**`Uninstall CLI Plugins.md` (26 lines, 0 H2, 2 code fences, byte-identical across versions).** It documents `plugins` and `plugins:uninstall` in a 2-step ordered list. `Create Custom CLI Plugins for Contentstack | V2.x.x.md` already has a `Managing Installed Plugins` H2 with H3s `Uninstalling a Plugin`, `Updating a Plugin`, `Resetting All Plugins`, `Inspecting a Plugin`, which is a strict superset of this page's content.
**Recommendation: retire the page and redirect to that section.** This is a content duplication finding (C7), not a template finding. If you would rather keep the URL, the correct fix is to grow it into a proper `cli-command-reference` doc for the whole `plugins` topic (`plugins`, `plugins:install`, `plugins:uninstall`, `plugins:update`, `plugins:link`, `plugins:inspect`), because the `plugins` topic is the one oclif topic with no owning reference doc. Do not leave it as a 26-line stub under any template.

Both recommendations are read-only findings for WI-6, not actions for this pass.

### 4.8 Deviations from the plan's five candidate archetypes

| Plan candidate | Disposition | Reason |
|---|---|---|
| CLI Command Reference | **Kept**, absorbed the single-command case | The plan's rule "one namespace or plugin per doc" fails on 38 of 82 files that span 2 or more topics. Kept the archetype, replaced the rule (5.1) |
| CLI Setup Guide | **Dropped as a new type, reused `setup-guide.md`** | Only 2 files, and `setup-guide.md` already encodes install, verify, configure with a verification governing rule. A new type here would be pure registration cost |
| CLI Use Case or Runbook | **Kept and renamed** to CLI Task Runbook | "Use Case" collides with the `## Use Cases` H2 that `Bulk Operations in CLI` and `Audit Plugin` use for something else entirely (11 numbered scenarios inside a command reference). A type name that collides with a real section name will confuse `detectDocType()` and reviewers alike |
| CLI Reference Table | **Kept and renamed** to CLI Module Reference | "Table" describes the format, not the grouping. The archetype's defining property is that its H2s are module or command identities, which is what the grouping rule has to test. Also, `CLI Limitations` is 57 H3s of prose with only 6 code fences, so "table" mis-describes it |
| CLI Migration Guide | **Dropped as a new type, reused `migration-guide.md` plus addendum** | One doc, already the corpus's best structural match to an existing standard |
| (added) Feature Doc reuse | **Added** | 2 docs (`Asset Scanning in CLI`, `CLI for CS Assets`) organize by lifecycle phase, not by command or by step. Without this they would be forced into Command Reference and would fail every command rule |

Net change: 5 candidates become 3 new types plus 3 reuses.

### 4.9 Full assignment table, all 82 files

Archetype codes: **CR** CLI Command Reference, **TR** CLI Task Runbook, **MR** CLI Module Reference, **SG** Setup Guide (existing), **FD** Feature Doc (existing), **MG** Migration Guide (existing), **NONE** no template, retire or merge.

| # | Ver | Folder | Doc | Lines | H2 | Type | Structural evidence |
|---|---|---|---|---|---|---|---|
| 1 | V1 | CLI Advanced Operations | Apps CLI Plugin | 480 | 4 | CR | 8 H3 under Commands map 1:1 to the 8 `app:*` command files |
| 2 | V1 | CLI Advanced Operations | Asset Scanning in CLI | 75 | 6 | FD | H2s are lifecycle phases (Publishing With Scan-Gating, Import-Time Behavior), no Commands section |
| 3 | V1 | CLI Advanced Operations | Bulk Operations in CLI | 994 | 11 | CR | Commands H2 with 2 command H3s, flag tables at H4. See section 6 |
| 4 | V1 | CLI Advanced Operations | Change Master Locale | 72 | 4 | TR | Prerequisites, Steps for Execution, Troubleshoot, Limitations |
| 5 | V1 | CLI Advanced Operations | Configure MFA Secret Using CLI | 49 | 3 | CR | Set and Remove command pair promoted to H2 instead of H3 |
| 6 | V1 | CLI Advanced Operations | Entry Migration | 124 | 3 | TR | Prerequisites, Steps for execution, Troubleshoot |
| 7 | V1 | CLI Advanced Operations | Generate Typescript Typings with TSGen Plugin | 140 | 7 | CR | Single command `tsgen`, facet H2s Usage, Options, Examples |
| 8 | V1 | CLI Advanced Operations | Update Missing Reference UIDs for Entries, Assets, and Extensions | 81 | 3 | TR | Prerequisites, Steps for Execution, Troubleshoot |
| 9 | V1 | CLI Commands | Audit Plugin | 700 | 9 | CR | Commands H2 covering `cm:stacks:audit` and `audit:fix`, plus Use Cases and Best Practices |
| 10 | V1 | CLI Commands | Bulk Publish and Unpublish Content | 383 | 4 | CR | Commands H2 with 12 H3s, but H3s are task names not command names. Non-compliant grouping |
| 11 | V1 | CLI Commands | CLI for Launch | 645 | 4 | CR | 9 H3s covering `launch` subcommands. `Prerequisites` sits at H4 |
| 12 | V1 | CLI Commands | CLI-Supported Features for Export, Import, and Clone Operations | 354 | 10 | MR | Support matrix indexed by module. `Prerequisites` at H3 |
| 13 | V1 | CLI Commands | Cloning a Stack | 143 | 5 | CR | Single command `cm:stacks:clone`, facet H2s Commands, Options, Steps |
| 14 | V1 | CLI Commands | Compare and Merge Branches Using the CLI | 559 | 5 | CR | 6 `cm:branches:*` plus 3 `config:*:base-branch` commands grouped under 4 "Steps to" H2s. Non-compliant grouping |
| 15 | V1 | CLI Commands | Configure CLI Logging Preferences | 59 | 2 | CR | Commands H2, Set and Get H3s, `config:*:log` triad |
| 16 | V1 | CLI Commands | Configure Early Access in the CLI | 154 | 2 | CR | Commands H2, Set, Get, Remove H3s |
| 17 | V1 | CLI Commands | Configure Proxy Settings in CLI | 208 | 5 | CR | Commands H2, Set, Get, Remove H3s, plus a Quick Reference |
| 18 | V1 | CLI Commands | Configure Rate Limits in the CLI | 145 | 3 | CR | Commands H2, Set, Get, Remove H3s |
| 19 | V1 | CLI Commands | Content Type Plugin | 501 | 10 | CR | 6 H3s are literal command ids, 24 H4s are Syntax, Flags, Output, Examples |
| 20 | V1 | CLI Commands | Export Content Using the CLI | 607 | 13 | CR | Single command `cm:stacks:export`, facets split across 13 H2s, 6 H4 examples |
| 21 | V1 | CLI Commands | Import Content Using the CLI | 714 | 14 | CR | Single command `cm:stacks:import`, 14 H2s, 10 H4 examples |
| 22 | V1 | CLI Commands | Overwrite Existing Content using CLI Import | 156 | 3 | TR | Steps for Execution, Migration Scenarios, Limitations. No Prerequisites |
| 23 | V1 | CLI Commands | Query-based Export | 148 | 4 | CR | Single command `cm:stacks:export-query`. No Commands H2 at all |
| 24 | V1 | CLI Commands | Regex Validate Plugin | 363 | 11 | CR | Command Reference H2 with Command Syntax, Flags, Flag Details H3s |
| 25 | V1 | Content Migration Commands | Export Content to CSV File Using the CLI | 214 | 2 | CR | Single command `cm:export-to-csv`. Only 2 H2s for 214 lines |
| 26 | V1 | Content Migration Commands | Import Content Using the Seed Command | 152 | 4 | CR | Single command `cm:stacks:seed`, 2 source-variant H3s |
| 27 | V1 | Content Migration Commands | Migrate your Content using the CLI Migration Command | 248 | 7 | TR | Process Overview, Prerequisites, Steps for Execution, then 3 step H2s |
| 28 | V1 | Get Started with CLI | CLI Authentication and Adding Tokens | 233 | 3 | CR | 7 `auth:*` commands live at H4. See section 6 |
| 29 | V1 | Get Started with CLI | Configure Regions in the CLI | 260 | 8 | CR | `config:*:region` triad as H2s, plus Developer Examples. Intro sections out of order |
| 30 | V1 | Get Started with CLI | Install the CLI | 169 | 7 | SG | Install, Verify installation, Namespaces, Check Version, Update Version |
| 31 | V1 | Migration Use Cases | Branches \| Migration Use Cases | 112 | 2 | TR | Two scenario H2s, 246-word intro, no Prerequisites |
| 32 | V1 | Migration Use Cases | Migrate Content Between Stacks Using the CLI | 42 | 2 | TR | Prerequisites, Steps for Execution. Crosses export, audit, import |
| 33 | V1 | Migration Use Cases | Migrate Selected Content Using the Query Export Plugin | 131 | 5 | TR | Export, Query Format, Output Structure, Import. Execution ordered |
| 34 | V1 | Migration Use Cases | Migrate and Overwrite Content in the Same Stack | 97 | 6 | TR | H2s are literally Step 1, Step 2, Step 3 |
| 35 | V1 | Miscellaneous | Bootstrap Starter Apps | 388 | 7 | TR | Scaffold, run, deploy ordering. `kickstarter.md` is the nearest existing type |
| 36 | V1 | Miscellaneous | CLI Limitations | 1386 | 20 | MR | 20 H2s all named `<Module> Limitations`. No Prerequisites |
| 37 | V1 | Miscellaneous | Contentstack CLI Configuration Reference | 1145 | 10 | MR | 6 body H2s named `<Command> Configuration`. No Prerequisites, no Commands |
| 38 | V1 | Miscellaneous | Create Custom CLI Commands | 102 | 6 | TR | Scaffold, run, set up, register, uninstall ordering |
| 39 | V1 | Miscellaneous | Create Custom CLI Plugins for Contentstack | 771 | 16 | TR | Build lifecycle ordering. `Introduction` used as the intro heading |
| 40 | V1 | Miscellaneous | Uninstall CLI Plugins | 26 | 0 | NONE | Zero H2. Fully duplicated by Create Custom CLI Plugins V2 Managing Installed Plugins. See 4.7 |
| 41 | V1 | Miscellaneous | Useful Plugins | 12 | 0 | NONE | Zero H2, zero fences, zero commands. One npm link. See 4.7 |
| 42 | V2 | CLI Advanced Operations V2 | Apps CLI Plugin | 482 | 4 | CR | Same as row 1 |
| 43 | V2 | CLI Advanced Operations V2 | CLI for CS Assets | 264 | 9 | FD | H2s are lifecycle phases (Export CS Assets, Import CS Assets, Management Token Behavior). Already has a Quick Decision Guide |
| 44 | V2 | CLI Advanced Operations V2 | Change Master Locale | 72 | 4 | TR | Byte-identical to row 4 |
| 45 | V2 | CLI Advanced Operations V2 | Configure MFA Secret Using CLI | 47 | 3 | CR | Same as row 5 |
| 46 | V2 | CLI Advanced Operations V2 | Entry Migration | 124 | 3 | TR | Same as row 6 |
| 47 | V2 | CLI Advanced Operations V2 | Generate Typescript Typings with TSGen Plugin | 140 | 7 | CR | Same as row 7 |
| 48 | V2 | CLI Advanced Operations V2 | Update Missing Reference UIDs for Entries, Assets, and Extensions | 81 | 3 | TR | Byte-identical to row 8 |
| 49 | V2 | CLI Commands V2 | Audit Plugin | 696 | 9 | CR | Same as row 9 |
| 50 | V2 | CLI Commands V2 | Bulk Operations in CLI | 1093 | 11 | CR | 4 command H3s (entries, assets, cs-assets, taxonomies), 15 H4s carry the flag tables |
| 51 | V2 | CLI Commands V2 | CLI for Launch | 646 | 4 | CR | Same as row 11. Adds Install the Launch Plugin H2 |
| 52 | V2 | CLI Commands V2 | CLI-Supported Features for Export, Import, and Clone Operations | 357 | 10 | MR | Same as row 12 |
| 53 | V2 | CLI Commands V2 | Cloning a Stack | 131 | 5 | CR | Same as row 13 |
| 54 | V2 | CLI Commands V2 | Compare and Merge Branches Using the CLI | 602 | 6 | CR | Same as row 14, adds Steps to Check a Merge Status for `cm:branches:merge-status` |
| 55 | V2 | CLI Commands V2 | Configure CLI Logging Preferences | 64 | 2 | CR | Same as row 15 |
| 56 | V2 | CLI Commands V2 | Configure Early Access in the CLI | 158 | 2 | CR | Same as row 16 |
| 57 | V2 | CLI Commands V2 | Configure Proxy Settings in CLI | 208 | 5 | CR | Same as row 17 |
| 58 | V2 | CLI Commands V2 | Content Type Plugin | 587 | 11 | CR | Same as row 19, plus Quick Reference and Upgrading from v1 H2s |
| 59 | V2 | CLI Commands V2 | Export Content Using the CLI | 295 | 6 | CR | Single command, 6 H2s, only 2 H3s. Half the V1 doc's length |
| 60 | V2 | CLI Commands V2 | Import Content Using the CLI | 315 | 10 | CR | Single command, 10 H2s, 3 H3s |
| 61 | V2 | CLI Commands V2 | Overwrite Existing Content using CLI Import | 170 | 3 | TR | Same as row 22. No Prerequisites |
| 62 | V2 | CLI Commands V2 | Query-based Export | 148 | 4 | CR | Byte-identical to row 23 |
| 63 | V2 | CLI Commands V2 | Regex Validate Plugin | 359 | 11 | CR | Same as row 24 |
| 64 | V2 | CLI Migration Use Cases V2 | Branches \| Migration Use Cases | 124 | 3 | TR | Same as row 31, adds Check the Status of a Merge |
| 65 | V2 | CLI Migration Use Cases V2 | Migrate Content Between Stacks Using the CLI | 51 | 3 | TR | Same as row 32, adds a behavior-check H2 |
| 66 | V2 | CLI Migration Use Cases V2 | Migrate Selected Content Using the Query Export Plugin | 131 | 5 | TR | Byte-identical to row 33 |
| 67 | V2 | CLI Migration Use Cases V2 | Migrate and Overwrite Content in the Same Stack | 101 | 6 | TR | Same as row 34 |
| 68 | V2 | Content Migration Commands V2 | Export Content to CSV File Using the CLI | 216 | 2 | CR | Same as row 25 |
| 69 | V2 | Content Migration Commands V2 | Import Content Using the Seed Command | 153 | 4 | CR | Same as row 26 |
| 70 | V2 | Content Migration Commands V2 | Migrate your Content using the CLI Migration Command | 250 | 7 | TR | Same as row 27 |
| 71 | V2 | Get Started with CLI V2 | CLI Authentication and Adding Tokens | 248 | 3 | CR | Same as row 28. 7 `auth:*` commands at H4 |
| 72 | V2 | Get Started with CLI V2 | Configure Regions in the CLI | 126 | 2 | CR | Commands H2 with Get, Set, Set custom host H3s. Cleaner than V1 |
| 73 | V2 | Get Started with CLI V2 | Install the CLI | 162 | 7 | SG | Same as row 30 |
| 74 | V2 | Get Started with CLI V2 | Migrate from Contentstack CLI V1 to V2 | 1509 | 13 | MG | Overview, Quick Decision Guide, Prerequisites, Type Mapping Reference, Command Reference, Troubleshooting, Pre-Upgrade Checklist, Next Steps |
| 75 | V2 | Miscellaneous V2 | Bootstrap Starter Apps | 391 | 7 | TR | Same as row 35 |
| 76 | V2 | Miscellaneous V2 | CLI Limitations | 1349 | 21 | MR | Same as row 36, adds Version Requirements and Removed Flags |
| 77 | V2 | Miscellaneous V2 | Configure Rate Limits in the CLI | 149 | 3 | CR | Same as row 18. Folder placement contradicts its `config:` siblings, per the plan |
| 78 | V2 | Miscellaneous V2 | Contentstack CLI Configuration Reference | 1145 | 10 | MR | Byte-identical to row 37 |
| 79 | V2 | Miscellaneous V2 | Create Custom CLI Commands | 102 | 6 | TR | Byte-identical to row 38 |
| 80 | V2 | Miscellaneous V2 | Create Custom CLI Plugins for Contentstack | 1033 | 14 | TR | Same as row 39 plus 18 H4s of utility API reference. Hybrid, see section 6 |
| 81 | V2 | Miscellaneous V2 | Uninstall CLI Plugins | 26 | 0 | NONE | Byte-identical to row 40 |
| 82 | V2 | Miscellaneous V2 | Useful Plugins | 12 | 0 | NONE | Byte-identical to row 41 |

**Reconciliation.** CR 43, TR 24, MR 6, SG 2, FD 2, MG 1, NONE 4. Total 82, no doc unassigned. Subtracting the 8 byte-identical pairs (rows 44, 48, 62, 66, 78, 79, 81, 82 duplicate rows 4, 8, 23, 33, 37, 38, 40, 41) gives 74 distinct docs: CR 42, TR 20, MR 5, SG 2, FD 2, MG 1, NONE 2.

---

## 5. Grouping rule per archetype

Each rule is one sentence, checkable by a script with no judgment call, and labelled for whether it derives from the CLI's own namespace tree.

### 5.1 CLI Command Reference

> **Grouping rule:** Under the `Commands` H2, when the doc documents two or more commands each H3 must name a command that resolves to a file under that plugin's `src/commands/` tree and the H3s must appear in that tree's sorted order, and when the doc documents exactly one command each H3 must be a member of the closed list Syntax, Flags, Configuration File, Output, Examples in that order.

**Namespace-derived: yes for the multi-command branch, no for the single-command branch.** This is the one archetype where the oclif tree genuinely supplies the order, and it covers 43 files. The single-command branch cannot be namespace-derived because a single namespace node supplies exactly one item and therefore no ordering.

How a script checks it: parse `Commands` H3s, resolve each against a generated command inventory built from `repo/cli-core/packages/*/src/commands/**/*.ts` and `repo/cli-plugins/packages/*/src/commands/**/*.ts`, then compare index order. Both halves are exact string work.

What it flags today: `Bulk Publish and Unpublish Content | V1.x.x.md` (12 H3s that are task names, not commands), `Compare and Merge Branches Using the CLI` x2 (commands grouped under 4 "Steps to" H2s with no `Commands` H2 at all), `Query-based Export` (no `Commands` H2), `CLI Authentication and Adding Tokens` x2 (commands at H4, so invisible to an H3 check and to the right-nav). It passes `Content Type Plugin` x2, `Apps CLI Plugin` x2, and the 9 `config:` triad docs.

### 5.2 CLI Task Runbook

> **Grouping rule:** The doc must contain exactly one procedure spine, either a single `Steps for Execution` H2 whose body holds one ordered list, or a consecutive run of H2s each matching `^Step \d+:` with strictly ascending numbers, and no `csdx` command may appear in a code fence before the step that introduces it.

**Namespace-derived: no.** These docs cross namespaces by design. `Migrate Content Between Stacks Using the CLI` runs `cm:stacks:export`, then `cm:stacks:audit`, then `cm:stacks:import`, three different plugins in one required order, and reordering them by namespace would make the doc wrong. Execution order is the only correct axis, and it is a property of the operation, not of the CLI's topic tree.

How a script checks it: regex on H2 text for the two allowed forms, reject docs matching both or neither, then a first-occurrence scan of `csdx <cmd>` tokens against step boundaries.

What it flags today: `Migrate your Content using the CLI Migration Command` x2 (has both a `Steps for Execution` H2 **and** three sibling step H2s, so two competing spines), `Branches | Migration Use Cases` x2 (no spine at all, just two scenario H2s), `Bootstrap Starter Apps` x2 (prose H2s with no step numbering). It passes the 8-file `Steps for Execution` family and `Migrate and Overwrite Content in the Same Stack` x2.

### 5.3 CLI Module Reference

> **Grouping rule:** Every H2 in the reference body must be titled `<id> <noun>` where `<id>` is a real command id or a module name drawn from `modules.types` in the export or import config, and those H2s must appear in ascending lexicographic order of `<id>`.

**Namespace-derived only in its vocabulary, not in its order.** The section titles must be real ids, which is namespace-derived. The order is deliberately lexicographic rather than declaration order, for a hard reason: `repo/cli-plugins/packages/contentstack-export/src/config/index.ts:26` and `repo/cli-plugins/packages/contentstack-import/src/config/index.ts:30` declare the same modules in **two different orders**, and `oclif.plugins` in `repo/cli-core/packages/contentstack/package.json` declares a third order that reflects load sequence, not reader need. There is no single declared order to cite, so citing one would be arbitrary. Lexicographic order is unambiguous, script-checkable, stable across releases, and correct for a lookup doc a reader scans rather than reads.

What it flags today: all 6 files. `Contentstack CLI Configuration Reference` runs Export, Import, Audit, Query-Export, Import-Setup, Migration where lexicographic order is Audit, Export, Export-Query, Import, Import-Setup, Migration. `CLI Limitations` x2 runs Core, Authentication, Export, Import, Import Setup, Overwrite, Bulk, Clone, Branch, Launch and so on, which is neither lexicographic nor any declared order.

### 5.4 Setup Guide, existing type

> **Grouping rule:** H2s must appear in the order install, verify, configure, upgrade, with the verify H2 immediately following the install H2.

**Namespace-derived: no.** This is the setup sequence, which is a property of the install path. Already the governing rule of `setup-guide.md` ("every main-content section ends with a verification step or a clear observable outcome") so no new rule text is needed.

### 5.5 Feature Doc, existing type

> **Grouping rule:** Each body H2 must name exactly one lifecycle phase from the closed list Export, Import, Publish, Unpublish, Clone, and no body H2 may contain a `csdx` command id.

**Namespace-derived: no.** These docs describe one behavior seen at several points in the pipeline, so the axis is the pipeline phase. The second clause is what keeps them out of Command Reference: the moment a heading names a command, the doc is a command reference and should be retyped.

### 5.6 Migration Guide, existing type

> **Grouping rule:** Under the `Command Reference` H2, every H3 must be a literal command id, the H3s must be grouped so that all ids sharing a topic prefix are contiguous, and each H3 must contain both a V1-labelled and a V2-labelled statement.

**Namespace-derived: yes, and this is the corpus's only working proof of it.** `Migrate from Contentstack CLI V1 to V2 | V2.x.x.md` already does this. Its 27 command H3s run `cm:*` (11), then `auth:*` (4), then `config:*` (3), then `tsgen`, then `app:create`, then `migrate:*` (2), then `content-type:*` (5). Contiguous by topic prefix, exactly as the rule requires. The third clause is C8's existing labelled-statement rule, restated so a script can test it per H3.

The reason namespace grouping works here and nowhere else is worth stating plainly: **this doc's subject is the entire command surface.** When the subject is the whole tree, the tree is the right index. Every other CLI doc has a narrower subject (one plugin, one operation, one module, one behavior), and for a narrower subject the tree is either too coarse (50 files under `cm`) or too fine (one node, no order).

---

## 6. The H2 and H3 constraint

The Contentstack docs platform right-nav renders H2 and H3 only. An H4 gets no anchor id and no nav entry, which is the same fact behind the unfixable H4-targeted anchors in WI-4.

**Measured: 179 H4 headings across 16 of the 82 files.** Every Section Order proposed in section 7 works entirely within H2 and H3. The archetypes that currently rely on H4 for structure, worst first:

| Doc | H4 count | What is stranded at H4 | Archetype | Fix |
|---|---|---|---|---|
| `Migrate from Contentstack CLI V1 to V2 \| V2.x.x` | 43 | Per-command change blocks (Removed Flags, Behavior Change, V1 to V2 Command Mapping), repeated under each of 27 command H3s | MG | Keep the 27 command H3s. Convert the repeated H4 blocks into a fixed 3-column table inside each H3 so nothing needs a nav stop |
| `Content Type Plugin` V1 and V2 | 24 each | `Syntax`, `Flags`, `Output`, `Examples` repeated under all 6 command H3s | CR | Same pattern. Collapse the 4 H4s per command into one flag table plus one fenced example block, both unheaded |
| `Create Custom CLI Plugins for Contentstack \| V2.x.x` | 18 | The entire `@contentstack/cli-utilities` API surface (cliux, CLIError, Args, configHandler, HttpClient, FsUtility and 12 more) | TR | This is a genuine hybrid. Split the utilities API out into its own MR doc, which restores its 18 entries to H2 or H3 |
| `Bulk Operations in CLI \| V2.x.x` | 15 | `Syntax`, `Required Options`, `Entry-Specific Options`, `General Options`, `Examples` under each of 4 command H3s | CR | Same collapse as Content Type Plugin. This is the plan's named known-bad acceptance doc |
| `Import Content Using the CLI \| V1.x.x` | 10 | 10 named import examples | CR | Move into one `Examples` H3 as a labelled list |
| `Bulk Operations in CLI \| V1.x.x` | 9 | Same as V2, 2 commands | CR | Same |
| `CLI Authentication and Adding Tokens` V1 and V2 | 7 each | **All 7 `auth:*` commands themselves** | CR | Most damaging case in the corpus. Promote the 7 commands from H4 to H3 and drop the two grouping H3s (`Authentication`, `Token Management`) to lead-in sentences |
| `Export Content Using the CLI \| V1.x.x` | 6 | 6 named export examples | CR | Same as Import |
| `Contentstack CLI Configuration Reference` (both) | 5 | Precedence and tuning examples | MR | Convert to unheaded labelled blocks |
| `CLI for Launch` V1 and V2 | 2 each | A second `Prerequisites` at H4, plus CI redeployment guidance | CR | The H4 `Prerequisites` is the plan's "2 at H4" count. Merge into the doc's H2 Prerequisites |
| `Audit Plugin` V1 and V2 | 1 each | `Shell Script Example:` | CR | Drop the heading, keep the fence |

**Archetype-level verdict.** CLI Command Reference is the archetype that structurally depends on H4 today, in 8 of its 43 files, and the dependency is always the same pattern: a repeated 4-part facet block under each command. Fixing it is mechanical and does not lose information, because a flag table plus a fenced example block carries the same content with no heading. CLI Task Runbook depends on H4 in exactly one file (`Create Custom CLI Plugins V2`), and there the right fix is a doc split, not a heading demotion. CLI Module Reference and Migration Guide use H4 for examples only.

---

## 7. Draft Section Order tables

Format verified against `doc-standards/scripts/build/build-section-order.js:29-59`. The `## Section Order` heading text and the four header cells `#`, `Section`, `Required`, `Purpose` are matched literally. Only a `Required` cell whose text starts with "Required" is machine-enforced, per the `/^required\b/i` test at `doc-standards/scripts/lib/section-index.js:44`. The three pseudo-sections `SEO front matter`, `Page title`, and `Main Content` are never matched against real headings (`section-index.js:18`), so their `Required` value has no enforcement effect and is set to `Required` only for consistency with the existing 7 files.

Cell wording was chosen deliberately in every row. Advisory choices are justified in the note under each table.

### 7.1 `cli-command-reference`

A CLI command reference documents the command surface of one plugin or one namespace: what each command does, its flags, and its output.

| # | Section | Required | Purpose |
|---|---|---|---|
| 1 | SEO front matter (title, description, URL) | Required | Machine-readable metadata for search and indexing |
| 2 | Page title | Required | Human-readable entry point, names the plugin or namespace |
| 3 | Overview | Required | 1-3 sentences: what this command surface does, and whether any command mutates stack data |
| 4 | Quick Reference | If the doc covers 3 or more commands | Command-to-purpose table so a reader can jump to the one command they need |
| 5 | Prerequisites | Required | CLI installed, authenticated, region configured, plus token scope and plugin install where they apply |
| 6 | Installation | Required if the plugin is not bundled | The `csdx plugins:install` line, present if and only if the plugin is absent from `oclif.plugins` |
| 7 | Commands | Required | One H3 per command, or the fixed facet order for a single-command doc |
| 8 | Examples | Recommended | Runnable scenarios that combine flags, kept out of the per-command H3s |
| 9 | Troubleshooting | Required | Root cause and resolution for each known failure |
| 10 | Limitations | Required | Known coverage gaps, per C9 |
| 11 | Next Steps | Required | Links to what comes after, each with a description |

**Governing rule:** A reader arrives knowing a command name and must find it as an H3 in the right-nav without reading prose. The grouping rule in section 5.1 decides what those H3s are.

Deliberately advisory: **Quick Reference** (row 4) and **Examples** (row 8). Quick Reference is left advisory because only 2 of 43 files have one today (`Configure Proxy Settings` and `Content Type Plugin | V2.x.x`), so making it Required would raise 41 tier-1 errors that are all really one backlog item, and the "3 or more commands" condition needs a command count the linter does not yet compute. Examples is advisory because a 2-H2 doc like `Export Content to CSV File Using the CLI` legitimately folds its examples into the `Commands` section. Deliberately enforced: **Installation** starts with "Required" so `/^required\b/i` matches and the bundled-versus-external finding, the plan's highest-value prerequisites item, becomes a hard error rather than a suggestion. Its condition is checked by `cli-prerequisites.js`, not by the section-order comparison.

### 7.2 `cli-task-runbook`

A CLI task runbook walks a developer through one operation end to end, usually across more than one command and more than one plugin.

| # | Section | Required | Purpose |
|---|---|---|---|
| 1 | SEO front matter (title, description, URL) | Required | Machine-readable metadata for search and indexing |
| 2 | Page title | Required | Human-readable entry point, states the operation as an outcome |
| 3 | Overview | Required | 1-3 sentences: what the developer will have done, and what it changes in the stack |
| 4 | Quick Decision Guide | If the operation has more than one path | Orients the reader before they read requirements, for example overwrite versus fresh import |
| 5 | Prerequisites | Required | CLI installed, authenticated, region configured, plus the token scope each step needs |
| 6 | Steps for Execution | Required | The one procedure spine, per the grouping rule. Every step ends with an observable outcome |
| 7 | Verification | Recommended | How the developer confirms the operation succeeded before moving on |
| 8 | Troubleshooting | Required | Root cause and resolution for each failure this operation can produce |
| 9 | Limitations | Required | What this path does not cover, per C9 |
| 10 | Next Steps | Required | Links to what comes after, each with a description |

**Governing rule:** The developer completes the whole operation from this page alone, in the order the page presents it, and can tell at each step whether it worked.

Deliberately advisory: **Verification** (row 7). It appears as a distinct section in zero of the 24 files today, so requiring it would produce 24 identical tier-1 errors on a section nobody has written yet. The verification requirement is instead carried by row 6's purpose text ("every step ends with an observable outcome") and belongs in the Manual Review Queue until the docs catch up. Deliberately enforced: **Steps for Execution** and **Limitations**. Steps for Execution is the archetype's whole identity, and its exact heading text is already the corpus convention in 8 files. Limitations is enforced because C9 mandates it and because these are the docs that overwrite and delete stack content, where an unstated gap is a production incident. Note that requiring the literal label `Steps for Execution` is what makes the two-spine defect in `Migrate your Content using the CLI Migration Command` visible: the doc has the heading and three competing step H2s, so it passes the presence check and fails the grouping check, which is the correct split of a hard error from an advisory one.

### 7.3 `cli-module-reference`

A CLI module reference is a lookup page: it lists what the CLI supports, or what it does not, or what it accepts, one section per module or per command, with no procedure.

| # | Section | Required | Purpose |
|---|---|---|---|
| 1 | SEO front matter (title, description, URL) | Required | Machine-readable metadata for search and indexing |
| 2 | Page title | Required | Human-readable entry point, names the scope of the lookup |
| 3 | Overview | Required | 1-3 sentences: what this page indexes, and what it deliberately does not cover |
| 4 | Quick Reference | Required | Index table mapping each module or command to its section, so no reader scrolls a 1,000-line page |
| 5 | Precedence and Scope | Recommended | How overlapping sources resolve, where the page documents configuration |
| 6 | Main Content | Required | One H2 per module or command, in the order the grouping rule sets |
| 7 | Next Steps | Required | Links to the command docs the entries here refer to |

**Governing rule:** A reader arrives with one module or one command in mind and reaches its section in one jump. No section assumes the reader read the section before it.

Deliberately advisory: **Precedence and Scope** (row 5). Only `Contentstack CLI Configuration Reference` needs it, where it already exists as `Configuration Precedence`, so requiring it would fail all 4 `CLI Limitations` and `CLI-Supported Features` files for a section that is meaningless to them. Deliberately enforced: **Quick Reference** (row 4). This is the one place I make a currently-absent section a hard error on purpose. None of the 6 files has one, so this will raise 6 tier-1 errors, and that is the intent: these are 5,736 lines, 20.7 percent of the corpus, on pages with 10 to 21 H2s and up to 57 H3s, and the absence of an index is their single largest usability defect. Six deliberate errors on five distinct docs is a tractable backlog item, unlike the 41 that Quick Reference would raise in 7.1. Note there is no Prerequisites row at all: none of these docs runs a command, all 6 lack Prerequisites today, and the plan already lists them among the "defensibly exempt" set for WI-5. Note also there is no Troubleshooting and no Limitations row, because `CLI Limitations` is itself the corpus's limitations page and nesting a Limitations section inside it is incoherent.

### 7.4 Existing types, changes needed

`setup-guide.md`: **no change.** Assign rows 30 and 73 to it as-is.

`feature-doc.md`: add one row and one Type-Specific Rule. The row is `| 8a | Limitations | Required | Known coverage gaps, per C9 |` placed between Troubleshooting and Next Steps, renumbered. This does affect non-CLI feature docs, so if that is unacceptable the fallback is to add the lifecycle-phase grouping rule to Type-Specific Rules only and leave Limitations advisory. The Type-Specific Rule to add is section 5.5's grouping rule.

`migration-guide.md`: add one row and one Type-Specific Rule. The row is `| 7a | Command Reference | Required if the guide covers a command-line tool | One H3 per command, grouped by topic prefix |` placed after Main Content. Because the cell starts with "Required", it is machine-enforced, and because the only migration guide in the corpus already has the section, it costs zero new errors. The Type-Specific Rule to add is section 5.6's grouping rule, plus the broadened Quick Decision Guide trigger from the archived amendment proposals (more than one path, or more than about 500 lines, or more than about 5 commands), which is what makes the trigger fire on this 1,509-line, 27-command doc.

### 7.5 New `section-matrix.md` columns

Add three columns (`CLI Command Reference`, `CLI Task Runbook`, `CLI Module Reference`) and three rows (`Commands`, `Installation`, `Quick Reference`), giving an 18-row by 10-column table. Values follow the tables above, with `Not used` for `Role-Based Routing Table`, `Quick Start`, `Documentation Map`, `Type Mapping Reference`, `Gradual Migration`, `Pre-Upgrade Checklist`, and `Theory Sections` across all three new columns.

---

## 8. Placement recommendation

**Create `doc-standards/cli-templates/` as a separate folder holding the three new type files. Do not extend the 7 existing type files, and do not flatten the CLI types into the root `doc-standards/` directory.**

One recommendation, and here is the cost accounting behind it.

**The registration cost is per type, not per folder.** The doc-type taxonomy is hardcoded in four places:

1. `doc-standards/scripts/lint-doc.js:25-33`, `VALID_TYPES`
2. `doc-standards/scripts/lint-doc.js:98`, the `detectDocType()` `feature-doc` branch that the CLI branch must precede
3. `doc-standards/scripts/build/build-section-order.js:19-27`, `TYPE_FILES`
4. `~/.claude/commands/revamp-doc.md`, its Step 1 detection list at lines 18 to 25 and its 8-branch priority list at lines 33 to 43

Every one of those four lists grows by three entries whichever folder the files sit in. `TYPE_FILES` maps a kebab key to a filename and `build-section-order.js:38` joins it against `STANDARDS_DIR`, so a subfolder costs exactly three characters per entry (`'cli-command-reference': 'cli-templates/cli-command-reference.md'`) and no code change. **The folder decision is therefore nearly free, and the type-count decision is where all the cost is.** That reframes the question: the right thing to minimize is the number of new types, which is why section 1 lands on 3 rather than the plan's 5.

**Why a subfolder rather than the root.** Three concrete reasons.

- **It keeps the reusability answer legible.** The recommendation is that 3 of the 6 CLI archetypes reuse product-wide types. If `cli-command-reference.md` sits beside `feature-doc.md` in the root, the next reader sees 10 peer types and has no way to tell that `setup-guide.md` is deliberately shared with the CLI while `getting-started.md` is deliberately not. A folder boundary encodes that.
- **It scopes the C9 rule block correctly.** C9 already exists in `common-rules.md` as CLI-specific rules applied to all types, which is why the mandated `Flag | Required | Description | Notes` shape has been silently ignored 19 times out of 20. The new `CMD-` or `CLI-` registry entries from WI-2 set `docTypes` to the three new keys, and a folder makes the correspondence between the folder and that `docTypes` list obvious.
- **It leaves room for the second and third CLI docs the corpus already needs.** Section 4.7 recommends a `plugins` topic reference, and section 6 recommends splitting the `cli-utilities` API surface out of `Create Custom CLI Plugins V2`. Both would be new CLI docs assigned to existing CLI types, and both are easier to reason about with a folder that says where CLI standards live.

**What I am explicitly rejecting.** Extending the existing 7 by editing their Section Order tables in place. `feature-doc.md` and `how-to-guide.md` are the two files that would have to absorb the CLI requirements, and both are used by non-CLI docs across the product. Adding a Required `Limitations` row to `how-to-guide.md` to serve 24 CLI runbooks would silently impose it on every SDK and CMS how-to guide, and there is no per-type mechanism to scope a Section Order row by product. That is a worse outcome than a fourth copy of a three-item list.

**Do all four edits in the same commit.** The four hardcoded lists are the failure mode here, and item 4 is already broken independently: `~/.claude/commands/revamp-doc.md` points at `/Users/aravindh.s/New Plugins for CLI/doc-standards/` at lines 14, 15, and 26, a directory that no longer exists, so the skill cannot load any standard today. Fixing those paths is a prerequisite for the new types being reachable from the skill at all, not a follow-up.

---

## 9. Items for WI-2 and WI-3 that fell out of this research

Recorded so they are not rediscovered.

1. **`detectDocType()` ordering is load-bearing.** `lint-doc.js:98` returns `feature-doc` for any doc with a `Commands` or `Command Reference` section or the word "plugin" or "command" in its title. That matches 43 of the 82 files. The three CLI branches must precede it. Also note `lint-doc.js:86` returns `migration-guide` on any title matching `/\bmigrat|upgrad/`, which today captures 9 runbook files whose titles start with "Migrate" (`Migrate Content Between Stacks`, `Migrate and Overwrite Content in the Same Stack`, `Migrate Selected Content Using the Query Export Plugin`, `Migrate your Content using the CLI Migration Command`, and their V1 or V2 twins). The `cli-task-runbook` branch must precede the migration branch, or those 9 files get linted against `Type Mapping Reference` and `Pre-Upgrade Checklist` requirements that make no sense for them.
2. **`checkHeadingUniformity` will need a CLI vocabulary.** The singular-plural splits the plan measured (`Limitations` 22 against `Limitation` 4, `Troubleshooting` 16 against `Troubleshoot` 6, `Next Steps` 12 against `Next Step` 2) are exactly what the Section Order label match at `section-index.js` loose-matches away. `Limitation` singular appears in `Apps CLI Plugin` x2 and `Audit Plugin` x2, and `Troubleshoot` singular in the entire 6-file `Steps for Execution` family. Pin the plural forms in the Section Order tables, which sections 7.1 to 7.3 do, and let the uniformity check flag the singulars.
3. **`Prerequisites` at H3 and H4 is invisible to `compareOrder()`.** `section-index.js` compares H2 text only, so the 4 H3 and 2 H4 Prerequisites headings register as missing rather than as misleveled. The 6 affected files are `CLI-Supported Features` x2 and `Bulk Operations in CLI` x2 (H3), and `CLI for Launch` x2 (H4). `cli-prerequisites.js` should report level, not just presence, so WI-3 can distinguish "absent" from "wrong level".
4. **The two docs with no archetype are content findings, not template findings.** `Useful Plugins` and `Uninstall CLI Plugins` should be reported in WI-6 as retire-or-merge candidates with the duplication evidence in section 4.7, and excluded from the WI-3 linter run rather than assigned a type they cannot satisfy.
5. **`migrate:` has no owning doc, and 4 of its 6 commands are undocumented.** `migrate:audit`, `migrate:create`, `migrate:import`, and `migrate:status` have zero mentions in all 82 files. `cm:stacks:import-setup` likewise owns no page. Both are `cli-command-reference` gaps for the second pass, and both are coverage findings rather than structure findings, so they belong in WI-6 alongside the missing changelog and hub pages.
