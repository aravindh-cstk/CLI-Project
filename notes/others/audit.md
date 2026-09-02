# Stage 3 Standards Audit

Scope: six docs updated in Stage 2 to document the new asset-scanning gating feature. Audit only, no edits applied.

Linter invocation used for all six files:
```
node "/Users/aravindh.s/CLI Project/doc-standards/scripts/lint-doc.js" "<file>" --type=<detected-type> --format=text
```
The script ran successfully for all six files (exit code 1 is the linter's normal "findings exist" exit, not a failure to run).

## Doc-type detection

Per the priority order in `/Users/aravindh.s/.claude/commands/revamp-doc.md` Step 1, applied to the first 60 lines of each file:

| File | doc_type front matter | Title/overview signal | Detected type |
|---|---|---|---|
| GA/bulk-publish-and-unpublish-content.md | none | Noun-phrase title, describes a capability (bulk publish/unpublish commands), not a single task walkthrough | Feature Doc (rule 7) |
| GA/import-content-using-the-cli.md | none | Title starts with imperative "Import", overview describes completing a specific task (import content into a destination stack) | How-To Guide (rule 4) |
| GA/cli-limitations.md | none | Not imperative, not migration, not a single feature, aggregates limitations across all modules | Conceptual Guide (default, rule 8) |
| GA/audit-plugin.md | none | Describes a specific product feature (the Audit plugin) | Feature Doc (rule 7) |
| Beta/bulk-operations-in-cli.md | none | Describes a specific feature (Bulk Operations plugin) | Feature Doc (rule 7) |
| Beta/import-content-using-the-cli.md | none | Title starts with imperative "Import", overview describes completing a specific task | How-To Guide (rule 4) |

Two of the six are **not** Feature Docs. `import-content-using-the-cli.md` (both versions) matches rule 4 (imperative title, task-completion overview) ahead of rule 7 in the priority order, so it is a How-To Guide. `cli-limitations.md` does not describe one specific feature, it aggregates limitations across every module, so no earlier rule matches and it falls to the default, Conceptual Guide. This changes which section-order table applies (`how-to-guide.md` / `conceptual-guide.md` instead of `feature-doc.md`) and explains some of the linter's own findings below (for example, "Quick Start" being forbidden for a How-To Guide/Feature Doc where the section-order table does not define it).

---

## File 1: GA/bulk-publish-and-unpublish-content.md (Feature Doc)

### Automated Findings (11, pre-confirmed)

1. L1: Missing front matter keys `title`, `description`, `url`. Rule [FM-01]: "SEO front matter must include a title, a description, and a url." Fix: add all three keys to the front matter block.
2. Required section "Overview" is missing. Rule [C1-01] (Do -> Understand -> Debug order requires the section set to be present). Fix: add an Overview section per common-rules.md's Overview definition, right after the title.
3. Required section "Next Steps" is missing. Rule [C1-01]. Fix: add a Next Steps section with described links.
4. L358, L364, L370: the three Troubleshooting entries are each flagged as missing a bolded `**Root Cause(s)**` label and a bolded `**Resolution**` label. Rule [C1-05]: "Troubleshooting entries require a root cause and a resolution, not just a symptom." Cause: all three entries write the label as `**Root Cause(s):**` and `**Resolution:**`, colon inside the bold markers, so the bold text is literally "Root Cause(s):" rather than "Root Cause(s)". common-rules.md's Section Definitions specify the label as `**Root Cause(s)**` (no colon inside the bold). Fix: move the colon outside the bold span, e.g. `**Root Cause(s)**:` in all three entries.

### Flagged for Review (2 heuristic detections)

1. L51 (and 10 more lines): `#build-the-configuration-file` anchor repeated 11 times. **Dismissed.** Each repeat is inside a different command's Options list pointing back to the one "Build the Configuration File" section, which is the intended cross-reference pattern for a doc with many sibling command subsections (C5-02 required inline reference), not accidental duplication.
2. L258/286/315: `/docs/headless-cms/about-entry-variants` repeated 3 times. **Dismissed.** Each occurrence is in a different, self-contained command subsection (Main Content subsections must be self-contained per common-rules.md), so repeating the same supporting link across independent subsections is expected, not redundant.

### Manual Review Queue

1. **Rule**: "When two sections are near-identical, the second section references the first and adds only what is genuinely different" (C7).
   **Location**: Troubleshooting entry "Assets remain unpublished after `cm:assets:publish --backup-dir`" (line 358-362) vs. Limitations bullet 3 (line 380).
   **Issue**: Both state the same fact, in-queue assets are skipped with no automatic retry and must be republished after scanning, in near-identical wording, with no cross-reference between them.
   **Required fix**: Keep the full explanation in Troubleshooting and shorten the Limitations bullet to a one-line pointer back to the Troubleshooting entry, or vice versa.
2. **Rule**: "State the consequence before the implementation rule" (C4-01).
   **Location**: New paragraph after the Bulk Publish All Assets Options list (line 128).
   **Issue check**: The paragraph already states consequence first (what gets skipped and why) before the remedy (wait, rerun). No violation found here.
3. All other B1 items (heading accuracy, cognitive grouping, scannability, terminology, code vs. prose, cross-reference classification, tone) and C1-C9 items not already listed as Automated Findings were checked against the new asset-scanning content specifically. No further violations found: the new Troubleshooting entries and Limitations bullet use correct terminology consistent with the rest of the doc, and the new content is grouped correctly (Troubleshooting facts in Troubleshooting, Limitations facts in Limitations).

---

## File 2: GA/import-content-using-the-cli.md (How-To Guide)

### Automated Findings (10, pre-confirmed)

1. L1: Missing front matter keys `title`, `description`, `url`. Rule [FM-01]. Fix: add all three keys.
2. Required section "Overview" is missing. Rule [C1-01]. Fix: add an Overview section.
3. L23: "Quick Start" is a forbidden/undefined section for a How-To Guide. Rule [C1-01], cross-checked against `how-to-guide.md`'s section-order table, which has no "Quick Start" entry (a How-To Guide's Main Content is the step-by-step procedure itself). Fix: fold the Quick Start examples into Main Content, or rename/restructure so the doc's second section is Overview followed directly by Prerequisites and Main Content.
4. L695: banned superlative "comprehensive" ("For comprehensive information about import limitations..."). Rule [C8-01]. Fix: state what is actually covered instead, e.g. "For the full list of import limitations, see...".
5. L709, L711, L712: bare links in Next Steps ("Export content", "Clone a stack", "Migrate content", "Overwrite existing content") lack trailing descriptions. Rule [C1-06]: "Each link in Next Steps must include a one-sentence description." Fix: add a one-sentence description to each Next Steps bullet.
6. L20: acronym "CI" used before its expansion. Rule [C8-07]. Fix: expand "CI/CD" on first use in Prerequisites.

### Flagged for Review (3 heuristic detections)

1. L20/464: `cli-authentication#add-management-token` repeated. **Dismissed.** One occurrence is in Prerequisites (blocking requirement), the other is in "Import Content Using Management Token", a later section developers may arrive at directly. C5-04's exception explicitly allows a Prerequisites link to be repeated as a reminder in a long doc.
2. L21/709: `export-content-using-the-cli` repeated. **Dismissed.** One is a Prerequisites link (what you need before importing), the other is a Next Steps link (what to do after importing) pointing to the same doc for a different purpose. Not redundant.
3. L561/712: `overwrite-existing-content-using-cli-import` repeated. **Dismissed.** Same pattern, one inline in the Import Overwrite Feature section, one in Next Steps. Acceptable per C5-04's exception for long docs.

### Manual Review Queue

1. **Rule**: "When two sections are near-identical, the second section references the first and adds only what is genuinely different" (C7).
   **Location**: "Using Backup Directory" section (paragraph at line 250) and "Import with Publishing Options" section (paragraph at line 286).
   **Issue**: Both paragraphs give a full, independent explanation of the same fact (asset scanning rolling out as an org-plan feature auto-sets `--skip-assets-publish`, and the post-scan publish command to run). Each links to the other, but neither is reduced to a pointer, so the mechanism is explained twice in full.
   **Required fix**: Pick one location as the source of truth (recommend "Using Backup Directory", since that's where `--backup-dir` and the resulting publish command are introduced) and shorten the other to a one-sentence pointer.
2. **Rule**: "Remove cross-references that duplicate links already present in Prerequisites or Next Steps" / bare cross-reference callouts must be classified (C5, B1-8).
   **Location**: "Troubleshooting" section (line 697-699) and "Best Practices" section (line 701-703).
   **Issue**: Both sections consist of a single sentence ("For troubleshooting import issues, see the CLI Troubleshooting Guide." / "For best practices on import workflows, see the CLI Best Practices Guide.") with no actual hyperlink, just a bare name. These callouts cannot be classified as required/optional/redundant because there is nothing to follow.
   **Required fix**: Either link "CLI Troubleshooting Guide" and "CLI Best Practices Guide" to their actual doc paths, or remove the sections if no such docs exist yet.
3. **Rule**: heading accuracy (B1-2, C6-01).
   **Location**: "Using Backup Directory" heading (line 230).
   **Issue**: The section now also documents asset-scanning's automatic `--skip-assets-publish` behavior during import, which is not about the backup directory itself, it is about publish-skip behavior that happens to be explained alongside the backup-dir flow.
   **Required fix**: Add a one-clause lead-in sentence orienting the reader ("...and, on stacks with asset scanning enabled, the same import also skips asset publishing automatically") so the heading's scope is not silently exceeded, or split the asset-scanning note into its own short subsection.

---

## File 3: GA/cli-limitations.md (Conceptual Guide)

### Automated Findings (7, pre-confirmed)

1. L1: Missing front matter keys `title`, `description`, `url`. Rule [FM-01]. Fix: add all three keys.
2. Required section "Overview" is missing. Rule [C1-01]. Fix: add an Overview per the Conceptual Guide definition, since this is a reference/conceptual doc, a short paragraph on what the page catalogs and how to use it satisfies this.
3. Required section "Next Steps" is missing. Rule [C1-01]. Fix: add a Next Steps section.
4. L93: acronym "OAuth" used before expansion. Rule [C8-07]. Fix: expand on first use (MFA Support Limitations section).
5. L99: acronym "SSO" used before expansion. Rule [C8-07]. Fix: expand on first use (Organization Switching section).

### Flagged for Review

None. The linter reported 0 flagged items for this file.

### Manual Review Queue

1. **Rule**: formatting correctness (B1 scannability / general markdown hygiene, not a single numbered C-rule but implicit in document structure).
   **Location**: lines 729-730, between "Asset Scan In-Queue Assets Are Not Retried" and "## Clone Operations Limitations".
   **Issue**: Two consecutive `---` horizontal-rule separators appear back to back with a blank line between them, an artifact of the Stage 2 edit that inserted the new "Asset Scan In-Queue Assets Are Not Retried" entry.
   **Required fix**: Remove the duplicate `---`.
2. **Rule**: "When two sections are near-identical, the second section references the first and adds only what is genuinely different" (C7).
   **Location**: "Asset Publishing Is Skipped When Asset Scanning Is Active" (Import Setup Limitations / Import Module Limitations area, lines 454-472) vs. "Asset Scan In-Queue Assets Are Not Retried" (Bulk Publish/Unpublish Limitations, lines 709-727).
   **Issue**: Both entries describe the same underlying asset-scanning gating mechanism (skip-assets-publish during import, retry-once-scan-completes workaround), from the import side and the publish side respectively. Some of this is legitimately different (one is about import auto-setting the flag, the other is about publish skipping in-queue assets), but the "wait for scan, then run `cm:assets:publish --backup-dir`" resolution text is repeated near-verbatim in both.
   **Required fix**: Keep the import-side entry focused only on why publishing is skipped during import, and have it point to the publish-side entry for the actual retry/wait mechanic, rather than restating the wait-and-rerun instruction in both places.
3. **Rule**: Cognitive grouping (B1-3, C6-02), this file being an aggregator across modules.
   **Location**: whole file.
   **Issue check**: Verified that the two new asset-scanning entries are placed under the correct module headings (Import Module Limitations and Bulk Publish/Unpublish Limitations respectively) consistent with the rest of the file's per-module grouping. No violation found.

---

## File 4: GA/audit-plugin.md (Feature Doc)

### Automated Findings (9, pre-confirmed)

1. L1: Missing front matter keys `title`, `description`, `url`. Rule [FM-01]. Fix: add all three keys.
2. Required section "Overview" is missing. Rule [C1-01]. Fix: add an Overview section (the current intro paragraphs under the title should be consolidated into one).
3. Required section "Next Steps" is missing. Rule [C1-01]. Fix: add a Next Steps section.
4. L667: "Common Issues" Troubleshooting entry (bullet-list Error/Solution format) is missing bolded `**Root Cause(s)**` and `**Resolution**` labels. Rule [C1-05]. This is a pre-existing formatting pattern (bullet list of `**Error:** ... **Solution:**`), not part of the Stage 2 asset-scanning edit. Fix: convert to the standard heading + `**Root Cause(s)**` / `**Resolution**` format.
5. L552: acronyms "CI" and "CD" used before expansion. Rule [C8-07]. Fix: expand on first use in the CI/CD Pipeline Integration section.

### Flagged for Review (10 heuristic detections)

All 10 are repeated links between the module-overview bullet list (lines 13-21) and the corresponding Module-Specific Audit Checks / Limitation sections (lines 33-40, 689-697). **Dismissed, all 10.** The overview list is a scannable summary of what the plugin covers. The later sections are the detailed reference for each of those same items, and the Limitation section at the end is an intentional recap. This is the expected "summary up top, detail below, recap at the end" structure for a reference-heavy Feature Doc, not redundant cross-referencing per C5-04's exception for long docs with per-module subsections developers may jump to directly.

### Manual Review Queue

1. **Rule**: "Required cross-references include a brief inline summary of the critical fact" (C5-02).
   **Location**: Assets Module section, line 319 (new Stage 2 addition): "This check validates the structural completeness of `publish_details` only. It does not check an asset's scan or quarantine status. For asset-scan gating during publish, see [Bulk Publish and Unpublish Content](/docs/headless-cms/bulk-publish-and-unpublish-content#bulk-publish-all-assets)."
   **Issue check**: This is a correctly-formed required cross-reference, it states the critical fact inline (audit does not check scan/quarantine status) before pointing to the doc that covers scan gating. No violation, cited as confirmation the pattern was followed correctly here.
2. All other B1/C1-C9 items were checked against the one new line added for asset scanning (line 319) and no additional findings were found. The new content is a single well-scoped sentence and does not introduce grouping, duplication, or tone issues.

---

## File 5: Beta/bulk-operations-in-cli.md (Feature Doc)

### Automated Findings (33, pre-confirmed)

1. L1: Missing front matter keys `title`, `description`, `url`. Rule [FM-01]. Fix: add all three keys.
2. Required section "Next Steps" is missing. Rule [C1-01]. Fix: add a Next Steps section.
3. L47: "Quick Start" is a forbidden/undefined section for a Feature Doc (per `feature-doc.md`'s section-order table, which has no Quick Start entry). Fix: fold Quick Start examples into Main Content (the "Commands" section), or restructure.
4. L11: banned superlative "robust" ("providing robust commands for bulk publishing"). Rule [C8-01]. Fix: state the concrete behavior (retries, adaptive rate limiting) instead.
5. L13, L473: Q&A-style headers "What Problem Does It Solve?" and "Why Delivery Tokens?" outside a dedicated FAQ section. Rule [C3-02]. Fix: rename to declarative headings ("Problem This Plugin Solves" / "Delivery Tokens for Cross-Publish").
6. L936-1029 (11 entries x 2 = 22 findings): every Troubleshooting entry in the section, both the pre-existing `### Problem: ...` entries and the three new asset-scanning entries added in Stage 2, is flagged as missing bolded `**Root Cause(s)**` and `**Resolution**` labels. Rule [C1-05]. Two distinct causes are collapsed into this one finding count, see Manual Review Queue item 1 below for the required fix, since a mechanical relabel is not sufficient for the pre-existing entries.
7. L374: acronym "CMA" used before expansion. Rule [C8-07]. Fix: expand on first use (Bulk CS Assets operations section).
8. L793: acronyms "CI" and "CD" used before expansion. Rule [C8-07]. Fix: expand on first use (Use Case 10).

### Flagged for Review (3 heuristic detections)

1. L31: "Node.js >= 22" has no link. **Dismissed.** This is an environment fact (a runtime version requirement), which C1-04's exception explicitly exempts from needing a link.
2. L32: "Contentstack CLI installed" has no link. **Confirmed as a minor gap**, not the environment-fact exception since an install doc exists and is linked from the equivalent GA docs (e.g. `/docs/headless-cms/install-the-cli`). **Required fix**: link "Contentstack CLI installed" to the install doc, consistent with how the GA docs in this set link their Prerequisites.
3. L33: "Valid Contentstack account with Management Token or API Key" has no link. **Confirmed as a minor gap** for the same reason as item 2. **Required fix**: link to the account/management-token setup docs, consistent with the GA docs' Prerequisites pattern.

### Manual Review Queue

1. **Rule** (this is the specific issue flagged for review by the prior stage): "Format each [Troubleshooting] entry as the symptom stated as the heading, followed by a bolded `**Root Cause(s)**` label and a bolded `**Resolution**` label, in that order." (Section Definitions, Troubleshooting, common-rules.md)
   **Location**: Troubleshooting section, lines 936-1033. Pre-existing entries ("### Problem: 429 Rate Limit Errors" through "### Problem: Source Alias Invalid Type", lines 936-1016) use `### Problem: <symptom>` headings followed by a `**Solution**:` label only, no `**Root Cause(s)**` at all. The three new Stage 2 entries ("Assets stay in 'still scanning' status...", "'Asset UID mapper is empty' warning...", "Environment names show as raw UIDs...", lines 1017-1033) use the symptom directly as the heading (no "Problem:" prefix) followed by `**Root Cause(s):**` and `**Resolution:**` labels.
   **Issue**: This is a **confirmed, real inconsistency**. The same Troubleshooting section now contains two different entry conventions: the older `### Problem:` / `**Solution**` style (11 entries) and the common-rules-compliant symptom-heading / `**Root Cause(s)**` / `**Resolution**` style (3 entries, newly added). A developer scanning this one section sees two different structures for equivalent information, and the older entries are missing a root cause element entirely (Solution alone does not substitute for Root Cause, per C1-05's "requires a root cause and a resolution, not just a symptom").
   **Required fix**: Rewrite all 11 pre-existing entries to match the common-rules format used by the 3 new entries: drop the "Problem: " prefix so the heading is the symptom itself, split each existing "Solution" content into an explicit `**Root Cause(s)**` sentence/list and a `**Resolution**` sentence/numbered-list. Do not go the other direction (converting the new entries to the old style), since the old style is not compliant with common-rules.md's Troubleshooting definition regardless of which convention the majority of the file currently uses.
2. **Rule**: same Section Definition as above, colon placement.
   **Location**: The three new Stage 2 entries (lines 1017-1033) write the labels as `**Root Cause(s):**` and `**Resolution:**` (colon inside the bold span), which is why the linter's Automated Findings above flag them as "missing" the label even though the content is present.
   **Issue**: Minor deviation from the literal `**Root Cause(s)**` / `**Resolution**` format (colon, if used, should sit outside the bold span).
   **Required fix**: Change `**Root Cause(s):**` to `**Root Cause(s)**:` and `**Resolution:**` to `**Resolution**:` in all three new entries (and, per item 1's fix, in the 11 rewritten entries too).
3. **Rule**: "When two sections are near-identical, the second section references the first and adds only what is genuinely different" (C7).
   **Location**: Troubleshooting entry "Assets stay in 'still scanning' status with no automatic retry" (line 1017-1021) vs. Limitations bullet 2 (line 1040).
   **Issue**: Both state that the scan-status check happens once per invocation with no polling/retry loop, in near-identical terms, with no cross-reference between the two sections.
   **Required fix**: Keep the full explanation in Troubleshooting and shorten the Limitations bullet to a pointer, or vice versa.
4. **Rule**: cognitive grouping / self-contained subsections (B1-3, Main Content definition).
   **Location**: "Asset Scan Status" dashboard description and example (lines 281-295), inside "Asset-Specific Options" under "Bulk Assets".
   **Issue check**: This content is directly tied to the `--data-dir` option documented immediately above it in the same table, and is explanatory rather than a second, unrelated topic. No grouping violation found.

---

## File 6: Beta/import-content-using-the-cli.md (How-To Guide)

### Automated Findings (5, pre-confirmed)

1. L1: Missing front matter keys `title`, `description`, `url`. Rule [FM-01]. Fix: add all three keys.
2. Required section "Overview" is missing. Rule [C1-01]. Fix: add an Overview section (currently the doc opens directly with a prose paragraph under the title, no dedicated Overview heading).
3. Required section "Next Steps" is missing. Rule [C1-01]. Fix: add a Next Steps section (this doc has no Next Steps at all, unlike its GA counterpart).

### Flagged for Review

None. The linter reported 0 flagged items for this file.

### Manual Review Queue

1. **Rule**: heading accuracy / section scope (B1-2, C6-03).
   **Location**: "Use of --backup-dir Flag" heading (line 112), paragraph at line 124.
   **Issue**: The section now also explains that asset scanning auto-sets `--skip-assets-publish` during import and prints a reminder pointing to the post-scan publish command, content about publish-skip behavior rather than about the backup-dir flag itself.
   **Required fix**: Add a one-clause lead-in orienting the reader that this also covers the asset-scan-triggered publish skip, or split it into its own short subsection.
2. **Rule**: "A fact stated in Prerequisites must not be restated mid-doc as a general reminder. One canonical location per fact" / C7 duplication.
   **Location**: paragraph at line 124 ("Asset scanning is rolling out...") vs. Limitations bullet (line 297, "On stacks where asset scanning is active for the org plan, `cm:stacks:import` skips asset publishing automatically...").
   **Issue**: The same fact (org-plan asset scanning auto-sets skip-assets-publish, then run `cm:stacks:bulk-assets --data-dir ... --operation publish` once scanning completes) is stated in full twice in this doc, once inline under "Use of --backup-dir Flag" and again in Limitations, with no cross-reference linking the two.
   **Required fix**: Keep the full explanation at line 124 (where the exact publish command is first introduced) and shorten the Limitations bullet to a one-line pointer back to it.
3. **Rule**: Consequence before implementation (C4-01).
   **Location**: line 124 paragraph.
   **Issue check**: The paragraph states the mechanism and its effect (assets not published) before pointing to the remedy command. No violation found, ordering is consequence-first.
4. **Rule**: Cross-doc consistency, not a single numbered rule but relevant to accuracy across the doc set.
   **Location**: line 124 says the reminder points to `csdx cm:stacks:bulk-assets --data-dir <BACKUP_DIR> --stack-api-key <STACK_API_KEY> --operation publish`. The equivalent GA doc (File 2, line 250) points to `csdx cm:assets:publish --backup-dir <BACKUP_DIR> --stack-api-key <STACK_API_KEY>`.
   **Issue check**: These are different commands (`cm:stacks:bulk-assets` with `--data-dir`, the Beta v2.x.x plugin command, vs. `cm:assets:publish` with `--backup-dir`, the GA command), which is expected since this file documents the Beta plugin and File 2 documents GA. Verified the command name and flags used here match the ones documented elsewhere in this same Beta doc set (File 5's `cm:stacks:bulk-assets --data-dir` usage). No inconsistency found.

---

## Summary of the flagged Troubleshooting-format issue

Confirmed as a real finding, scoped to **File 5 (Beta/bulk-operations-in-cli.md)** only. The other five files either have no Troubleshooting section with a mixed convention (Files 1, 2, 6 use only the common-rules format or none at all) or have a single, internally consistent legacy convention that predates Stage 2 and is unrelated to the new entries (File 4's bullet-list `**Error:**/**Solution:**` style, which has no new entries mixed into it). File 5 is the only file where old-style and new-style Troubleshooting entries coexist side by side in the same section. Required fix: rewrite the 11 pre-existing `### Problem:` entries to the common-rules symptom-heading / `**Root Cause(s)**` / `**Resolution**` format (not the reverse), and fix the colon-inside-bold formatting on all entries in that section, old and new alike.
