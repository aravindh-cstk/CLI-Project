# CLI Orphan Page Report

WI-6 of the CLI Structure Review. Read-only audit against the live CMS and production, run 2026-08-31.

**Definition used.** An orphan is a `docs_article` in CLI scope that is published to production but is not a leaf anywhere under the CLI navigation root (`links_2026` entry `bltd697fa2bc1e38b53`). A reader can reach it by search, or by a cross-link from another page, but never by browsing the sidebar.

**How it was measured.** The live `links_2026` tree was walked recursively for every `docs_article` leaf. Separately, all 2,419 `docs_article` entries were listed and filtered to CLI scope using the existing `fetch_cli_docs.in_cli_scope` rule (breadcrumb contains the CLI nav node `bltef82f5fd1a4eab6e`, or the title carries a CLI prefix, or the uid is one of the known-untracked plugin docs). The two sets were compared by uid.

Reproduce with:

```bash
python3 scripts/cli_orphan_audit.py --out notes/reports/cli-orphan-report.md
```

---

## Counts

| Measure | Count |
|---|---|
| Total `docs_article` entries in the stack | 2,419 |
| In CLI scope | 96 |
| ... published to production | 89 |
| ... never published anywhere | 7 |
| Nav leaf rows under the CLI root | 93 |
| Distinct articles in the nav | 86 |
| Articles referenced from more than one nav location | 7 |
| **Orphans (live on production, absent from the nav)** | **3** |
| Nav leaves that are not live on production | **0** |

Two things worth reading off this table before the detail.

**The nav has no dead links.** All 86 articles the sidebar points at are live on production. Whatever else is wrong with the CLI docs, the sidebar does not send readers to missing pages.

**The 93 versus 86 gap is expected, not a defect.** Contentstack nav references are shared rather than copied, so a version-agnostic doc appears as a leaf under both the V1 and the V2 tree. Everything in this report is deduped by uid.

---

## 1. Orphans: live on production, missing from the sidebar

All three return HTTP 200 and are also on staging. None of them is broken. They are simply unreachable by browsing.

| UID | URL | Title | Inbound links from CLI docs | Verdict |
|---|---|---|---|---|
| `bltd423e81420316dfd` | `/headless-cms/cli-migrate-content-from-html-rte-to-json-rte/v1` | Migrate Content from HTML RTE to JSON RTE using CLI \| V1.x.x | 1 | **Keep, add to nav** |
| `blt2daebde64e3d2023` | `/headless-cms/cli-migrate-content-from-html-rte-to-json-rte` | Migrate Content from HTML RTE to JSON RTE using CLI \| V2.x.x | 3 | **Keep, add to nav** |
| `blt2a6acf45012c79f3` | `/headless-cms/cli-taxonomy-migration` | Taxonomy Migration | 0 | **Keep, add to nav** |

### 1a. RTE migration, V1 and V2

**Why these are live but unlisted is now explainable.** The GA changelog (`changelog/2.x/cli-2.0.0.md`) records that RTE migration became a separate opt-in plugin at V2: "Made the RTE migration available as a separate, opt-in plugin via `csdx plugins:install @contentstack/cli-cm-migrate-rte`." The V2 page reflects that correctly. Its five sections are Prerequisites, Install the Migrate RTE Plugin, Using a Config File to Pass the Commands, Using Flags to Migrate Content, and Points to Remember, and it documents `plugins:install`, `auth:tokens:add`, and `cm:entries:migrate-html-rte`. So the plugin moving out of the bundle appears to have taken its doc out of the sidebar along with it.

That is the wrong outcome. An opt-in plugin still needs a discoverable doc, and the CLI still ships a guided install prompt for exactly this command, so readers will hit it.

The content is not stale. Four CLI docs already link to these pages:

| Linking doc | Line |
|---|---|
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | 104 |
| `Version 2.x.x/Get Started with CLI V2/Install the CLI \| V2.x.x` | 105 |
| `Version 2.x.x/Get Started with CLI V2/Migrate from Contentstack CLI V1 to V2 \| V2.x.x` | 332 |
| `Version 2.x.x/Get Started with CLI V2/Migrate from Contentstack CLI V1 to V2 \| V2.x.x` | 1507 |

**Recommended nav placement:**

| Doc | Section | Section UID |
|---|---|---|
| V1 page `bltd423e81420316dfd` | Version 1.x.x > Content Migration Commands | `blt2f95d98eb992b759` |
| V2 page `blt2daebde64e3d2023` | Version 2.x.x > Content Migration Commands V2 | (V2 counterpart section) |

That section already holds the sibling migration-command docs (Seed, Export to CSV, Migration Command), so the grouping is consistent with what is there.

**One tracking gap to fix at the same time.** The V2 entry `blt2daebde64e3d2023` is **absent from `cli-url-map.csv`**. Only the V1 entry (`bltd423e81420316dfd`, bucket GA) and a V0 entry (`bltcddcfb50d44a61db`) are tracked. This is an instance of the known drift where 14 index uids are missing from the CSV, and it means any tooling driven off the CSV silently skips the V2 page.

### 1b. Taxonomy Migration

This one is different, and worth a closer look before acting: it has **zero inbound links from any CLI doc**. It is reachable only by search.

Despite that, the evidence says keep it:

- It is actively maintained. Entry version **27**, last updated **2026-08-06**, three weeks before this audit.
- It documents a real, current command, `cm:stacks:migration`.
- Its structure is already a clean three-section runbook: Prerequisites, Steps for Execution, Troubleshoot.
- That shape is **identical** to `Entry Migration` and `Change Master Locale`, both of which sit in the nav under CLI Advanced Operations. There is no structural reason for this page to be treated differently from its two siblings.

**Recommended nav placement:** Version 1.x.x > CLI Advanced Operations (`bltfc496d77b74a316b`) and the V2 counterpart section. Its URL is version-agnostic (no `/v1` suffix), so like the other 7 shared docs it belongs as a leaf under both version trees.

**Also worth doing:** give it at least one inbound link. The natural place is the `Namespaces` section of `Install the CLI`, which already links to the RTE migration page and to most other command docs.

---

## 2. The missing CLI landing page is a draft, not a gap

This resolves an open question from WI-4. Three source repos (`repo/cli-core/README.md:65`, `repo/cli-plugins/README.md:66`, `repo/cli-plugins-pr294/README.md:66`) send readers to `https://www.contentstack.com/docs/headless-cms/cli`, which returns **404**.

The reason: the entry exists but was never published and has no content.

| Field | Value |
|---|---|
| UID | `blt28d887c3a468d6fe` |
| URL | `/headless-cms/cli` |
| Title | `[Second level navigation] - Command-line Interface (CLI)` |
| Entry version | 71 |
| Last updated | 2026-07-22 |
| Article content | **0 characters** |
| Published to | nothing (production, staging, and development all false) |

So the URL the READMEs point at is reserved by an empty navigation shell. Version 71 says it has been edited many times, which fits a structural entry rather than an abandoned draft.

**Recommendation.** Decide between two options, and either closes the 404:

1. **Publish a real hub page at `/headless-cms/cli`.** Fills the entry with a landing page that routes readers to Install, Authentication, Commands, and Migration. This is the better answer, because the URL is already the one the tooling advertises and it is what a reader typing the obvious URL expects.
2. **Create a `server_redirects` entry** from `/docs/headless-cms/cli` to `/docs/headless-cms/install-the-cli`. Cheaper, and reasonable as an interim step.

**Do not do both without checking order.** On this site a redirect overrides a live page, so a redirect created first would shadow the hub page if it is published later. If you take option 2 now and option 1 later, the redirect has to be unpublished as part of publishing the page. Run the shadow guard from `scripts/create_cli_redirects.py` either way.

---

## 3. Never-published entries in CLI scope

Seven entries. None has ever been published to any environment. They fall into three groups.

### 3a. Correctly retired: 1 entry

| UID | URL | Content | Note |
|---|---|---|---|
| `bltfbc10d646f00f90e` | `/headless-cms/cli-for-cs-assets/beta` | 16,692 chars | Pre-restructure Beta URL. The V2 page now owns the bare `/headless-cms/cli-for-cs-assets`. |

No action. This is the URL restructure working as designed.

### 3b. Navigation shell: 1 entry

`blt28d887c3a468d6fe`, covered in section 2 above.

### 3c. Unpublished drafts: 5 entries

These look like an in-progress troubleshooting or FAQ reorganization. Four are substantial (6 to 10 KB of content), one is a 724-character stub. All predate this audit by one to four months.

| UID | URL | Content | Last updated |
|---|---|---|---|
| `blt3f56ba22fea3dacd` | `/headless-cms/migration-cloning-architecture` | 10,171 chars | 2026-07-22 |
| `bltfe625afc6c950c19` | `/headless-cms/export-import-commands-data-formats` | 6,218 chars | 2026-05-12 |
| `blt56e99ee120e64ec5` | `/headless-cms/typescript-generation(tsgen)-plugins` | 6,972 chars | 2026-05-12 |
| `blt70a6780bd872a5ac` | `/headless-cms/authentication-network-node.j-environments` | 6,269 chars | 2026-05-13 |
| `blt357e28079a7f1b20` | `/headless-cms/migrate-content-using-cli` | 724 chars | 2026-07-22 |

Their titles and groupings match the folder structure under `troubleshooting/troubleshooting-revamped/` in this repo, so they are most likely the CMS side of that revamp.

**Two of these URLs are malformed and must be fixed before publishing, not after.** Changing a URL after publishing means creating a redirect, so it is much cheaper to correct now:

- `/headless-cms/typescript-generation(tsgen)-plugins` contains literal parentheses. Suggested: `/headless-cms/cli-tsgen-and-plugins-troubleshooting`.
- `/headless-cms/authentication-network-node.j-environments` reads `node.j`, which is a typo for `node.js`, and also carries a dot in the slug. Suggested: `/headless-cms/cli-authentication-and-network-troubleshooting`.

None of the five carries the `cli-` URL prefix that the rest of the CLI corpus adopted in the restructure. If they are published as-is they will be the only CLI pages outside that convention.

**Recommendation.** These are out of scope for a structure review, since publishing decisions belong to whoever owns the troubleshooting revamp. Flagging them so the URL and prefix problems get caught before publication rather than after.

---

## 4. Nav placement question carried over from WI-7

`Migrate from Contentstack CLI V1 to V2` (`blt05c442f72f396864`, `/headless-cms/cli-v1-to-v2-migration-guide`) is live on production and **is** in the nav, under `Get Started with CLI V2`. It is not an orphan.

It is listed here only because the working draft of the same content was filed under `CLI Commands V2`, which suggests the intended home may be different from the published one. If it should move, that is a nav edit on the two section entries, not a change to the article.

Both placements are defensible. `Get Started with CLI V2` suits a reader arriving to upgrade. `CLI Commands V2` suits its actual bulk, which is a 27-command reference. Worth one decision rather than leaving the draft and the published page disagreeing.

---

## 5. Articles shared across both version trees

Not defects, but they constrain any per-version edit. Each of these is a single CMS entry rendered in two sidebar locations, so it cannot be versioned independently and an edit for V2 is simultaneously an edit for V1.

| UID | Doc |
|---|---|
| `blt278785a9d6da5074` | Change Master Locale |
| `blt3afca0a8bf912f83` | Update Missing Reference UIDs for Entries, Assets, and Extensions |
| `blt7b3284729d3494f0` | Query-based Export |
| `blt3168251b46327602` | Migrate Selected Content Using the Query Export Plugin |
| `bltc7c58ab7c7d76974` | Contentstack CLI Configuration Reference |
| `blt553b89ec322a6199` | Uninstall CLI Plugins |
| `bltb4d51965b514f7c6` | Useful Plugins |

If any of these needs to say something different for V2 than for V1, it has to be forked into two entries first. That is a content decision, and it is the single biggest constraint on treating V1 and V2 as independently maintainable doc sets.

---

## Summary of recommended actions

Ordered by value, with the write operations marked. Nothing in this list has been executed. All of it needs your approval, and all of it is a CMS write.

| # | Action | Type | Value |
|---|---|---|---|
| 1 | Add the two RTE migration pages to Content Migration Commands, V1 and V2 | Nav write | Restores browse access to a doc 4 other docs already link to |
| 2 | Add Taxonomy Migration to CLI Advanced Operations, both trees | Nav write | Makes an actively maintained page discoverable for the first time |
| 3 | Resolve `/headless-cms/cli`, publish a hub page or add a redirect | Content or redirect write | Fixes the 404 that 3 source repos point readers at |
| 4 | Add `blt2daebde64e3d2023` to `cli-url-map.csv` | Local file | Stops CSV-driven tooling silently skipping the V2 RTE page |
| 5 | Give Taxonomy Migration at least one inbound link | Content write | It currently has zero |
| 6 | Fix the two malformed draft URLs before anyone publishes them | Local decision | Avoids needing redirects later |
| 7 | Settle the migration guide's nav home | Nav write | Removes the draft versus published disagreement |
