# Links Confirmation: CLI Docs V1 and V2

WI-4 of the CLI Structure Review. Generated 2026-08-31 against production.

**Scope.** All 82 markdown docs under `docs/markdown/Version 1.x.x/` and `Version 2.x.x/`. 1,230 links, 384 distinct targets, 404 anchor-bearing links.

**Method.** Anchor ids were read from the rendered production HTML, not computed. This matters, and the next section explains why.

---

## Read this before fixing anything: anchor ids cannot be computed offline

Verified from the live DOM. The docs renderer wraps **H2 and H3** in `<div id="<slug>" class="group heading-with-copy ...">` and gives them a copy-link button and a right-nav entry. **H4 renders as a bare `<h4>` with no id, no anchor, and no right-nav entry.**

So an anchor that targets an H4 heading is not a broken link that can be repaired by editing the href. There is no id to point at. The heading has to be promoted to H3.

The slug rule is also **not consistent across pages**, so it cannot be derived and applied in bulk. Two live examples, same construct, different results:

| Heading | Rendered id |
|---|---|
| `Bulk Publish/Unpublish Limitations` (on `cli-limitations`) | `bulk-publish-unpublish-limitations` |
| `Bulk Unpublish Entries/Assets` (on `cli-bulk-publish-and-unpublish-content/v1`) | `bulk-unpublish-entriesassets` |

The first turns `/` into a hyphen. The second drops it. Colons are dropped entirely (`cm:stacks:export` becomes `cmstacksexport`), dots become hyphens (`Node.js` becomes `node-js`), and repeated headings get numeric suffixes (`version-history`, `version-history-2`). Treat every anchor target as something to verify against the rendered page, never as something to compute.

**Every recommended URL in this report was fetched and confirmed to exist on the live page.** 17 distinct recommendations, 17 verified.

---

## Summary

| Finding | Count |
|---|---|
| Broken anchor links | 50 occurrences across 29 distinct hrefs |
| ... fixable by rewriting the href | 20 occurrences, 17 distinct |
| ... blocked: target heading is H4, needs promotion first | 30 occurrences, 12 distinct |
| Broken outbound links (non-anchor) | 1 |
| Links blocked by target host, not broken | 3 |
| CLI entries not published to production | 0 |
| Style normalizations | 3 groups |

---

## 1. Broken anchors fixable by rewriting the href

20 occurrences, 17 distinct hrefs. Each recommended URL is verified live.

| Doc | Anchor | Line | Current URL | Recommended URL |
|---|---|---|---|---|
| `Version 1.x.x/CLI Advanced Operations/Asset Scanning in CLI \| V1.x.x` | `#use-of---backup-dir-flag` | 72 | `/docs/headless-cms/import-content-using-the-cli#use-of---backup-dir-flag` | `/docs/headless-cms/import-content-using-the-cli#use-of-backup-dir-flag` |
| `Version 1.x.x/CLI Advanced Operations/Asset Scanning in CLI \| V1.x.x` | `#bulk-publishunpublish-limitations` | 73 | `/docs/headless-cms/cli-limitations#bulk-publishunpublish-limitations` | `/docs/headless-cms/cli-limitations#bulk-publish-unpublish-limitations` |
| `Version 1.x.x/CLI Commands/Cloning a Stack \| V1.x.x` | `#issue-resolution-in-references` | 23 | `/docs/headless-cms/cli-audit-plugin/v1#issue-resolution-in-references` | `/docs/headless-cms/cli-audit-plugin/v1#issue-resolution` |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#bulk-unpublish-entries-assets` | 97 | `/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-unpublish-entries-assets` | `/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-unpublish-entriesassets` |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#bulk-publish-entries-assets-from-one-environment-to-another` | 103 | `/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-publish-entries-assets-from-one-environment-to-another` | `/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-publish-entriesassets-from-one-environment-to-another` |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#bulk-unpublish-entries-assets` | 109 | `/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-unpublish-entries-assets` | `/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-unpublish-entriesassets` |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#use-the-stacks-clone-command` | 114 | `/docs/headless-cms/cli-cloning-a-stack/v1#use-the-stacks-clone-command` | `/docs/headless-cms/cli-cloning-a-stack/v1#steps-to-clone-a-stack`<br>_section was renamed, Steps to Clone a Stack is the surviving section_ |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#run-the-seed-command-using-the-management-token` | 116 | `/docs/headless-cms/cli-import-content-using-the-seed-command/v1#run-the-seed-command-using-the-management-token` | `/docs/headless-cms/cli-import-content-using-the-seed-command/v1#commands`<br>_no management-token section exists on this page, Commands is the nearest equivalent_ |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#restore-unpublish-entries-published` | 118 | `/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#restore-unpublish-entries-published` | `/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#restoreunpublish-entries-published` |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#issue-identification-in-references` | 119 | `/docs/headless-cms/cli-audit-plugin/v1#issue-identification-in-references` | `/docs/headless-cms/cli-audit-plugin/v1#issue-identification` |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#issue-resolution-in-references` | 120 | `/docs/headless-cms/cli-audit-plugin/v1#issue-resolution-in-references` | `/docs/headless-cms/cli-audit-plugin/v1#issue-resolution` |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#steps-for-execution` | 123 | `/docs/headless-cms/cli-for-launch/v1#steps-for-execution` | `/docs/headless-cms/cli-for-launch/v1#commands`<br>_no Steps for Execution section exists on this page, Commands is the nearest equivalent_ |
| `Version 1.x.x/Migration Use Cases/Branches \| Migration Use Cases \| V1.x.x` | `#get-started-with-the-migration-script` | 28 | `/docs/headless-cms/migrate-content-between-stacks-using-the-cli/v1#get-started-with-the-migration-script` | `/docs/headless-cms/migrate-content-between-stacks-using-the-cli/v1#steps-for-execution`<br>_Get Started with the Migration Script no longer exists, Steps for Execution replaced it_ |
| `Version 2.x.x/CLI Commands V2/Cloning a Stack \| V2.x.x` | `#issue-resolution-in-references` | 23 | `/docs/headless-cms/cli-audit-plugin#issue-resolution-in-references` | `/docs/headless-cms/cli-audit-plugin#issue-resolution` |
| `Version 2.x.x/CLI Migration Use Cases V2/Branches \| Migration Use Cases \| V2.x.x` | `#get-started-with-the-migration-script` | 28 | `/docs/headless-cms/migrate-content-between-stacks-using-the-cli#get-started-with-the-migration-script` | `/docs/headless-cms/migrate-content-between-stacks-using-the-cli#steps-for-execution`<br>_Get Started with the Migration Script no longer exists, Steps for Execution replaced it_ |
| `Version 2.x.x/Get Started with CLI V2/Install the CLI \| V2.x.x` | `#use-the-stacks-clone-command` | 109 | `/docs/headless-cms/cli-cloning-a-stack#use-the-stacks-clone-command` | `/docs/headless-cms/cli-cloning-a-stack#steps-to-clone-a-stack`<br>_section was renamed, Steps to Clone a Stack is the surviving section_ |
| `Version 2.x.x/Get Started with CLI V2/Install the CLI \| V2.x.x` | `#run-the-seed-command-using-the-management-token` | 111 | `/docs/headless-cms/cli-import-content-using-the-seed-command#run-the-seed-command-using-the-management-token` | `/docs/headless-cms/cli-import-content-using-the-seed-command#commands`<br>_no management-token section exists on this page, Commands is the nearest equivalent_ |
| `Version 2.x.x/Get Started with CLI V2/Install the CLI \| V2.x.x` | `#issue-identification-in-references` | 112 | `/docs/headless-cms/cli-audit-plugin#issue-identification-in-references` | `/docs/headless-cms/cli-audit-plugin#issue-identification` |
| `Version 2.x.x/Get Started with CLI V2/Install the CLI \| V2.x.x` | `#issue-resolution-in-references` | 113 | `/docs/headless-cms/cli-audit-plugin#issue-resolution-in-references` | `/docs/headless-cms/cli-audit-plugin#issue-resolution` |
| `Version 2.x.x/Get Started with CLI V2/Install the CLI \| V2.x.x` | `#steps-for-execution` | 116 | `/docs/headless-cms/cli-for-launch#steps-for-execution` | `/docs/headless-cms/cli-for-launch#commands`<br>_no Steps for Execution section exists on this page, Commands is the nearest equivalent_ |

---

## 2. Broken anchors that a href fix cannot repair

30 occurrences, 12 distinct hrefs. Every one targets an **H4** heading, which the renderer gives no id. Editing the href cannot help. The fix is a structural change to the target doc.

### The systemic cause: CLI Authentication puts its procedures at H4

`CLI Authentication and Adding Tokens` (both V1 and V2) nests its five procedures under two H3 section headings, leaving the procedures themselves at H4:

```
## Prerequisites                                  <- H2, has id
## Commands                                       <- H2, has id
### Authentication                                <- H3, has id
#### Login                                        <- H4, NO id
#### Logout                                       <- H4, NO id
#### Display Username of the Logged in User       <- H4, NO id
### Token Management                              <- H3, has id
#### Add Management Token                         <- H4, NO id
#### Add Delivery Token                           <- H4, NO id
#### Delete Token                                 <- H4, NO id
#### List All Tokens                              <- H4, NO id
## Next Steps                                     <- H2, has id
```

The whole rendered page exposes only five anchor targets: `#prerequisites`, `#commands`, `#authentication`, `#token-management`, `#next-steps`.

This matters more than the raw count suggests, because **`#login` and `#add-management-token` are part of the standard Prerequisites boilerplate** that most command docs copy:

```markdown
- CLI [authenticated](/docs/headless-cms/cli-authentication#login)
- [Configured management token](/docs/headless-cms/cli-authentication#add-management-token) (alias)
```

So the single highest-leverage fix in this whole report is: **promote `Login`, `Logout`, `Add Management Token`, and `List All Tokens` from H4 to H3 in `CLI Authentication and Adding Tokens`, in both V1 and V2.** That repairs **26 of the 30** blocked occurrences at once, and it also makes those procedures appear in the page's right-hand navigation, which today they do not.

The remaining 4 break down as 2 for `Display Username of the Logged in User` (see the note below) and 2 in the V1 to V2 migration guide (next subsection).

One extra step for `Display Username of the Logged in User`: the incoming anchor is `#display-username-of-a-session`, which does not match the heading text either. After promoting the heading, update the two inbound links to the id the renderer then produces.

### The same problem in the V1 to V2 migration guide

Two same-page anchors in `Migrate from Contentstack CLI V1 to V2 | V2.x.x` point at H4 headings, so its own internal navigation is broken:

- `#global-fields-format-changed-per-file` targets H4 `Global Fields Format Changed (Per-File)`
- `#removed-import-config-keys-custom-plugins-and-config-files` targets H4 `Removed Import Config Keys (Custom Plugins and Config Files)`

These are the only two findings the existing `scripts/sweep_cli_links.py` also reported, which is worth noting: that script checks the links present in the live page, so it found the same-page pair and missed the cross-doc H4 cases. Both passes are needed.

### Full list

| Doc | Anchor | Line | Current URL | Recommended URL |
|---|---|---|---|---|
| `Version 1.x.x/CLI Advanced Operations/Asset Scanning in CLI \| V1.x.x` | `#add-management-token` | 14 | `/docs/headless-cms/cli-authentication#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/CLI Commands/Bulk Publish and Unpublish Content \| V1.x.x` | `#add-management-token` | 16 | `/docs/headless-cms/cli-authentication/v1#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/CLI Commands/CLI for Launch \| V1.x.x` | `#login` | 342 | `/docs/headless-cms/cli-authentication/v1#login` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/CLI Commands/Content Type Plugin \| V1.x.x` | `#add-management-token` | 498 | `/docs/headless-cms/cli-authentication/v1#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/CLI Commands/Export Content Using the CLI \| V1.x.x` | `#add-management-token` | 20 | `/docs/headless-cms/cli-authentication/v1#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/CLI Commands/Export Content Using the CLI \| V1.x.x` | `#add-management-token` | 371 | `/docs/headless-cms/cli-authentication/v1#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/CLI Commands/Import Content Using the CLI \| V1.x.x` | `#add-management-token` | 20 | `/docs/headless-cms/cli-authentication/v1#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/CLI Commands/Import Content Using the CLI \| V1.x.x` | `#add-management-token` | 464 | `/docs/headless-cms/cli-authentication/v1#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/CLI Commands/Regex Validate Plugin \| V1.x.x` | `#add-management-token` | 44 | `/docs/headless-cms/cli-authentication/v1#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/Content Migration Commands/Migrate your Content using the CLI Migration Command \| V1.x.x` | `#login` | 51 | `/docs/headless-cms/cli-authentication/v1#login` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#login` | 90 | `/docs/headless-cms/cli-authentication/v1#login` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#logout` | 91 | `/docs/headless-cms/cli-authentication/v1#logout` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#list-all-tokens` | 92 | `/docs/headless-cms/cli-authentication/v1#list-all-tokens` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 1.x.x/Get Started with CLI/Install the CLI \| V1.x.x` | `#display-username-of-a-session` | 93 | `/docs/headless-cms/cli-authentication/v1#display-username-of-a-session` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/CLI Commands V2/CLI for Launch \| V2.x.x` | `#login` | 343 | `/docs/headless-cms/cli-authentication#login` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/CLI Commands V2/Content Type Plugin \| V2.x.x` | `#add-management-token` | 466 | `/docs/headless-cms/cli-authentication#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/CLI Commands V2/Content Type Plugin \| V2.x.x` | `#add-management-token` | 584 | `/docs/headless-cms/cli-authentication#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/CLI Commands V2/Export Content Using the CLI \| V2.x.x` | `#login` | 17 | `/docs/headless-cms/cli-authentication#login` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/CLI Commands V2/Export Content Using the CLI \| V2.x.x` | `#add-management-token` | 18 | `/docs/headless-cms/cli-authentication#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/CLI Commands V2/Import Content Using the CLI \| V2.x.x` | `#login` | 20 | `/docs/headless-cms/cli-authentication#login` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/CLI Commands V2/Import Content Using the CLI \| V2.x.x` | `#add-management-token` | 21 | `/docs/headless-cms/cli-authentication#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/CLI Commands V2/Regex Validate Plugin \| V2.x.x` | `#add-management-token` | 44 | `/docs/headless-cms/cli-authentication#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/CLI Commands V2/Regex Validate Plugin \| V2.x.x` | `#add-management-token` | 357 | `/docs/headless-cms/cli-authentication#add-management-token` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/Content Migration Commands V2/Migrate your Content using the CLI Migration Command \| V2.x.x` | `#login` | 51 | `/docs/headless-cms/cli-authentication#login` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/Get Started with CLI V2/Install the CLI \| V2.x.x` | `#login` | 92 | `/docs/headless-cms/cli-authentication#login` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/Get Started with CLI V2/Install the CLI \| V2.x.x` | `#logout` | 93 | `/docs/headless-cms/cli-authentication#logout` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/Get Started with CLI V2/Install the CLI \| V2.x.x` | `#list-all-tokens` | 94 | `/docs/headless-cms/cli-authentication#list-all-tokens` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/Get Started with CLI V2/Install the CLI \| V2.x.x` | `#display-username-of-a-session` | 95 | `/docs/headless-cms/cli-authentication#display-username-of-a-session` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/Get Started with CLI V2/Migrate from Contentstack CLI V1 to V2 \| V2.x.x` | `#removed-import-config-keys-custom-plugins-and-config-files` | 34 | `#removed-import-config-keys-custom-plugins-and-config-files` | _(promote the target heading to H3 first, see section 2)_ |
| `Version 2.x.x/Get Started with CLI V2/Migrate from Contentstack CLI V1 to V2 \| V2.x.x` | `#global-fields-format-changed-per-file` | 1456 | `#global-fields-format-changed-per-file` | _(promote the target heading to H3 first, see section 2)_ |

---

## 3. Broken outbound link

| Doc | Line | Current URL | Status | Recommended URL |
|---|---|---|---|---|
| `Query-based Export` (one shared entry, under both V1 and V2) | see entry | `/docs/developers/apis/content-delivery-api/queries` | **502**, confirmed on 3 consecutive requests | _(blank: needs owner confirmation)_ |

A 502 is a server error rather than a 404, so the page may exist but be failing to render. This one is left blank deliberately: the correct action is to ask the Content Delivery API doc owner whether the page is being retired or is simply broken. Do not repoint it on a guess.

---

## 4. Not broken, no action needed

Three links return 403 because npmjs.com rejects non-browser clients. They work for real readers.

- `https://www.npmjs.com/package/@contentstack/cli`
- `https://www.npmjs.com/package/@contentstack/apps-cli`
- `https://www.npmjs.com/package/contentstack-cli-tsgen`

---

## 5. Style normalizations

Not broken links, but inconsistencies worth settling once so the linter can hold the line afterwards.

### 5a. Absolute URLs where the corpus convention is root-relative

The corpus uses root-relative `/docs/...` for internal links, with zero file-relative links. Three links break that convention, all pointing at the same page:

| Doc | Line | Current URL | Recommended URL |
|---|---|---|---|
| `Version 1.x.x/Miscellaneous/Create Custom CLI Plugins for Contentstack \| V1.x.x` | 9 | `https://www.contentstack.com/docs/headless-cms/install-the-cli` | `/docs/headless-cms/install-the-cli` |
| `Version 1.x.x/CLI Advanced Operations/Change Master Locale` | 16 | `https://www.contentstack.com/docs/headless-cms/install-the-cli` | `/docs/headless-cms/install-the-cli` |
| `Version 2.x.x/CLI Advanced Operations V2/Change Master Locale` | 16 | `https://www.contentstack.com/docs/headless-cms/install-the-cli` | `/docs/headless-cms/install-the-cli` |

The two `Change Master Locale` rows are one CMS entry shown in two nav locations, so fixing it once resolves both.

### 5b. Login URL trailing slash

`https://www.contentstack.com/login/` appears 33 times and `https://www.contentstack.com/login` 20 times, inside the same Prerequisites boilerplate. Both resolve. Pick one and enforce it. Recommended: **without** the trailing slash, matching the rest of the corpus.

### 5c. A V2 doc linking into V1

| Doc | Line | Current URL | Recommended URL |
|---|---|---|---|
| `Version 2.x.x/CLI Commands V2/CLI for Launch \| V2.x.x` | 19 | `/docs/headless-cms/install-the-cli/v1` | `/docs/headless-cms/install-the-cli` |

This is in the Prerequisites list, so a reader following the V2 doc is sent to the V1 install page. It is the only `/v1` leak left in V2. Note the same line also cites version gates ("version 1.6.0 and above" for AWS and similar) that predate V2, so the sentence needs a content check alongside the link fix.

---

## 6. What this means for the doc standard

Three rules worth adding to the CLI templates in WI-2, each earned by a finding above:

1. **Any heading that is a link target must be H2 or H3.** H4 gets no id and no right-nav entry, so a procedure documented at H4 cannot be linked to or navigated to. This is mechanically checkable: flag every same-page anchor whose target heading is H4 or deeper.
2. **Do not nest command procedures below H3.** The `CLI Authentication` pattern of `## Commands` then `### Authentication` then `#### Login` buries every actual procedure past the navigable depth. Command procedures belong at H3 directly under an H2.
3. **Cross-doc deep links must be verified against the rendered page, not computed.** Given the inconsistent slug behavior shown above, a linter can flag a suspicious anchor but cannot confirm one. The live check in `scripts/sweep_cli_links.py` stays part of the release routine.

---

## Reproducing this report

```bash
# live pass: outbound link status plus the anchors present in the served pages
python3 scripts/sweep_cli_links.py --env prod
```

The cross-doc anchor pass in sections 1 and 2 is a second script, because the two passes catch different defects. `sweep_cli_links.py` checks the links present in the served pages, so it finds same-page problems and outbound status codes. The anchor audit reads links from the local `docs/markdown/` mirror and resolves each one against ids fetched from the rendered production page, which is what catches the cross-doc H4 cases:

```bash
python3 scripts/cli_anchor_audit.py      # writes notes/reports/anchors.json
python3 scripts/gen_links_report.py      # rebuilds this file from it
```

Run both. On this corpus the live sweep found 2 of the 50 broken anchors and the anchor audit found all 50.

