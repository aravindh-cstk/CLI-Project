#!/usr/bin/env python3
"""Generate notes/reports/links-confirmation.md from the audited data."""
import json
import os
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN = os.path.join(ROOT, "notes", "reports", "anchors.json")
OUT = os.path.join(ROOT, "notes", "reports", "links-confirmation.md")
rows = json.load(open(IN))

# Recommendations verified live against rendered pages on 2026-08-31. All 17 returned OK.
REC = {
    "/docs/headless-cms/cli-audit-plugin#issue-identification-in-references":
        "/docs/headless-cms/cli-audit-plugin#issue-identification",
    "/docs/headless-cms/cli-audit-plugin#issue-resolution-in-references":
        "/docs/headless-cms/cli-audit-plugin#issue-resolution",
    "/docs/headless-cms/cli-audit-plugin/v1#issue-identification-in-references":
        "/docs/headless-cms/cli-audit-plugin/v1#issue-identification",
    "/docs/headless-cms/cli-audit-plugin/v1#issue-resolution-in-references":
        "/docs/headless-cms/cli-audit-plugin/v1#issue-resolution",
    "/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-unpublish-entries-assets":
        "/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-unpublish-entriesassets",
    "/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-publish-entries-assets-from-one-environment-to-another":
        "/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#bulk-publish-entriesassets-from-one-environment-to-another",
    "/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#restore-unpublish-entries-published":
        "/docs/headless-cms/cli-bulk-publish-and-unpublish-content/v1#restoreunpublish-entries-published",
    "/docs/headless-cms/cli-limitations#bulk-publishunpublish-limitations":
        "/docs/headless-cms/cli-limitations#bulk-publish-unpublish-limitations",
    "/docs/headless-cms/import-content-using-the-cli#use-of---backup-dir-flag":
        "/docs/headless-cms/import-content-using-the-cli#use-of-backup-dir-flag",
    "/docs/headless-cms/migrate-content-between-stacks-using-the-cli#get-started-with-the-migration-script":
        "/docs/headless-cms/migrate-content-between-stacks-using-the-cli#steps-for-execution",
    "/docs/headless-cms/migrate-content-between-stacks-using-the-cli/v1#get-started-with-the-migration-script":
        "/docs/headless-cms/migrate-content-between-stacks-using-the-cli/v1#steps-for-execution",
    "/docs/headless-cms/cli-cloning-a-stack#use-the-stacks-clone-command":
        "/docs/headless-cms/cli-cloning-a-stack#steps-to-clone-a-stack",
    "/docs/headless-cms/cli-cloning-a-stack/v1#use-the-stacks-clone-command":
        "/docs/headless-cms/cli-cloning-a-stack/v1#steps-to-clone-a-stack",
    "/docs/headless-cms/cli-for-launch#steps-for-execution":
        "/docs/headless-cms/cli-for-launch#commands",
    "/docs/headless-cms/cli-for-launch/v1#steps-for-execution":
        "/docs/headless-cms/cli-for-launch/v1#commands",
    "/docs/headless-cms/cli-import-content-using-the-seed-command#run-the-seed-command-using-the-management-token":
        "/docs/headless-cms/cli-import-content-using-the-seed-command#commands",
    "/docs/headless-cms/cli-import-content-using-the-seed-command/v1#run-the-seed-command-using-the-management-token":
        "/docs/headless-cms/cli-import-content-using-the-seed-command/v1#commands",
}
# Notes for the rows where the recommendation is a redirect of intent, not a rename.
INTENT = {
    "/docs/headless-cms/cli-for-launch#commands":
        "no Steps for Execution section exists on this page, Commands is the nearest equivalent",
    "/docs/headless-cms/cli-for-launch/v1#commands":
        "no Steps for Execution section exists on this page, Commands is the nearest equivalent",
    "/docs/headless-cms/cli-import-content-using-the-seed-command#commands":
        "no management-token section exists on this page, Commands is the nearest equivalent",
    "/docs/headless-cms/cli-import-content-using-the-seed-command/v1#commands":
        "no management-token section exists on this page, Commands is the nearest equivalent",
    "/docs/headless-cms/cli-cloning-a-stack#steps-to-clone-a-stack":
        "section was renamed, Steps to Clone a Stack is the surviving section",
    "/docs/headless-cms/cli-cloning-a-stack/v1#steps-to-clone-a-stack":
        "section was renamed, Steps to Clone a Stack is the surviving section",
    "/docs/headless-cms/migrate-content-between-stacks-using-the-cli#steps-for-execution":
        "Get Started with the Migration Script no longer exists, Steps for Execution replaced it",
    "/docs/headless-cms/migrate-content-between-stacks-using-the-cli/v1#steps-for-execution":
        "Get Started with the Migration Script no longer exists, Steps for Execution replaced it",
}

H4 = [r for r in rows if r["action"].startswith("promote")]
FIX = [r for r in rows if not r["action"].startswith("promote")]


def short(src):
    """Filenames contain a literal pipe, which must be escaped inside a table cell."""
    return src.replace(".md", "").replace("|", "\\|")


def table(rs):
    out = ["| Doc | Anchor | Line | Current URL | Recommended URL |",
           "|---|---|---|---|---|"]
    for r in rs:
        rec = REC.get(r["href"], "")
        note = ""
        if rec and rec in INTENT:
            note = "<br>_" + INTENT[rec] + "_"
        rec = "`" + rec + "`" if rec else "_(promote the target heading to H3 first, see section 2)_"
        out.append("| `%s` | `#%s` | %d | `%s` | %s%s |" % (
            short(r["src"]), r["frag"], r["line"], r["href"], rec, note))
    return "\n".join(out)


L = []
L.append("# Links Confirmation: CLI Docs V1 and V2")
L.append("")
L.append("WI-4 of the CLI Structure Review. Generated 2026-08-31 against production.")
L.append("")
L.append("**Scope.** All 82 markdown docs under `docs/markdown/Version 1.x.x/` and `Version 2.x.x/`. "
         "1,230 links, 384 distinct targets, 404 anchor-bearing links.")
L.append("")
L.append("**Method.** Anchor ids were read from the rendered production HTML, not computed. "
         "This matters, and the next section explains why.")
L.append("")
L.append("---")
L.append("")
L.append("## Read this before fixing anything: anchor ids cannot be computed offline")
L.append("")
L.append("Verified from the live DOM. The docs renderer wraps **H2 and H3** in "
         "`<div id=\"<slug>\" class=\"group heading-with-copy ...\">` and gives them a copy-link button "
         "and a right-nav entry. **H4 renders as a bare `<h4>` with no id, no anchor, and no right-nav entry.**")
L.append("")
L.append("So an anchor that targets an H4 heading is not a broken link that can be repaired by editing the href. "
         "There is no id to point at. The heading has to be promoted to H3.")
L.append("")
L.append("The slug rule is also **not consistent across pages**, so it cannot be derived and applied in bulk. "
         "Two live examples, same construct, different results:")
L.append("")
L.append("| Heading | Rendered id |")
L.append("|---|---|")
L.append("| `Bulk Publish/Unpublish Limitations` (on `cli-limitations`) | `bulk-publish-unpublish-limitations` |")
L.append("| `Bulk Unpublish Entries/Assets` (on `cli-bulk-publish-and-unpublish-content/v1`) | `bulk-unpublish-entriesassets` |")
L.append("")
L.append("The first turns `/` into a hyphen. The second drops it. Colons are dropped entirely "
         "(`cm:stacks:export` becomes `cmstacksexport`), dots become hyphens (`Node.js` becomes `node-js`), "
         "and repeated headings get numeric suffixes (`version-history`, `version-history-2`). "
         "Treat every anchor target as something to verify against the rendered page, never as something to compute.")
L.append("")
L.append("**Every recommended URL in this report was fetched and confirmed to exist on the live page.** "
         "17 distinct recommendations, 17 verified.")
L.append("")
L.append("---")
L.append("")
L.append("## Summary")
L.append("")
L.append("| Finding | Count |")
L.append("|---|---|")
L.append("| Broken anchor links | %d occurrences across %d distinct hrefs |" % (
    len(rows), len(set(r["href"] for r in rows))))
L.append("| ... fixable by rewriting the href | %d occurrences, %d distinct |" % (
    len(FIX), len(set(r["href"] for r in FIX))))
L.append("| ... blocked: target heading is H4, needs promotion first | %d occurrences, %d distinct |" % (
    len(H4), len(set(r["href"] for r in H4))))
L.append("| Broken outbound links (non-anchor) | 1 |")
L.append("| Links blocked by target host, not broken | 3 |")
L.append("| CLI entries not published to production | 0 |")
L.append("| Style normalizations | 3 groups |")
L.append("")
L.append("---")
L.append("")
L.append("## 1. Broken anchors fixable by rewriting the href")
L.append("")
L.append("%d occurrences, %d distinct hrefs. Each recommended URL is verified live." % (
    len(FIX), len(set(r["href"] for r in FIX))))
L.append("")
L.append(table(FIX))
L.append("")
L.append("---")
L.append("")
L.append("## 2. Broken anchors that a href fix cannot repair")
L.append("")
L.append("%d occurrences, %d distinct hrefs. Every one targets an **H4** heading, which the renderer "
         "gives no id. Editing the href cannot help. The fix is a structural change to the target doc." % (
             len(H4), len(set(r["href"] for r in H4))))
L.append("")
L.append("### The systemic cause: CLI Authentication puts its procedures at H4")
L.append("")
L.append("`CLI Authentication and Adding Tokens` (both V1 and V2) nests its five procedures under two H3 "
         "section headings, leaving the procedures themselves at H4:")
L.append("")
L.append("```")
L.append("## Prerequisites                                  <- H2, has id")
L.append("## Commands                                       <- H2, has id")
L.append("### Authentication                                <- H3, has id")
L.append("#### Login                                        <- H4, NO id")
L.append("#### Logout                                       <- H4, NO id")
L.append("#### Display Username of the Logged in User       <- H4, NO id")
L.append("### Token Management                              <- H3, has id")
L.append("#### Add Management Token                         <- H4, NO id")
L.append("#### Add Delivery Token                           <- H4, NO id")
L.append("#### Delete Token                                 <- H4, NO id")
L.append("#### List All Tokens                              <- H4, NO id")
L.append("## Next Steps                                     <- H2, has id")
L.append("```")
L.append("")
L.append("The whole rendered page exposes only five anchor targets: `#prerequisites`, `#commands`, "
         "`#authentication`, `#token-management`, `#next-steps`.")
L.append("")
L.append("This matters more than the raw count suggests, because **`#login` and `#add-management-token` "
         "are part of the standard Prerequisites boilerplate** that most command docs copy:")
L.append("")
L.append("```markdown")
L.append("- CLI [authenticated](/docs/headless-cms/cli-authentication#login)")
L.append("- [Configured management token](/docs/headless-cms/cli-authentication#add-management-token) (alias)")
L.append("```")
L.append("")
L.append("So the single highest-leverage fix in this whole report is: **promote `Login`, `Logout`, "
         "`Add Management Token`, and `List All Tokens` from H4 to H3 in "
         "`CLI Authentication and Adding Tokens`, in both V1 and V2.** That repairs **26 of the %d** blocked "
         "occurrences at once, and it also makes those procedures appear in the page's right-hand navigation, "
         "which today they do not." % len(H4))
L.append("")
L.append("The remaining 4 break down as 2 for `Display Username of the Logged in User` (see the note below) "
         "and 2 in the V1 to V2 migration guide (next subsection).")
L.append("")
L.append("One extra step for `Display Username of the Logged in User`: the incoming anchor is "
         "`#display-username-of-a-session`, which does not match the heading text either. After promoting the "
         "heading, update the two inbound links to the id the renderer then produces.")
L.append("")
L.append("### The same problem in the V1 to V2 migration guide")
L.append("")
L.append("Two same-page anchors in `Migrate from Contentstack CLI V1 to V2 | V2.x.x` point at H4 headings, "
         "so its own internal navigation is broken:")
L.append("")
L.append("- `#global-fields-format-changed-per-file` targets H4 `Global Fields Format Changed (Per-File)`")
L.append("- `#removed-import-config-keys-custom-plugins-and-config-files` targets H4 "
         "`Removed Import Config Keys (Custom Plugins and Config Files)`")
L.append("")
L.append("These are the only two findings the existing `scripts/sweep_cli_links.py` also reported, which is "
         "worth noting: that script checks the links present in the live page, so it found the same-page pair "
         "and missed the cross-doc H4 cases. Both passes are needed.")
L.append("")
L.append("### Full list")
L.append("")
L.append(table(H4))
L.append("")
L.append("---")
L.append("")
L.append("## 3. Broken outbound link")
L.append("")
L.append("| Doc | Line | Current URL | Status | Recommended URL |")
L.append("|---|---|---|---|---|")
L.append("| `Query-based Export` (one shared entry, under both V1 and V2) | see entry | "
         "`/docs/developers/apis/content-delivery-api/queries` | **502**, confirmed on 3 consecutive requests | "
         "_(blank: needs owner confirmation)_ |")
L.append("")
L.append("A 502 is a server error rather than a 404, so the page may exist but be failing to render. "
         "This one is left blank deliberately: the correct action is to ask the Content Delivery API doc owner "
         "whether the page is being retired or is simply broken. Do not repoint it on a guess.")
L.append("")
L.append("---")
L.append("")
L.append("## 4. Not broken, no action needed")
L.append("")
L.append("Three links return 403 because npmjs.com rejects non-browser clients. They work for real readers.")
L.append("")
L.append("- `https://www.npmjs.com/package/@contentstack/cli`")
L.append("- `https://www.npmjs.com/package/@contentstack/apps-cli`")
L.append("- `https://www.npmjs.com/package/contentstack-cli-tsgen`")
L.append("")
L.append("---")
L.append("")
L.append("## 5. Style normalizations")
L.append("")
L.append("Not broken links, but inconsistencies worth settling once so the linter can hold the line afterwards.")
L.append("")
L.append("### 5a. Absolute URLs where the corpus convention is root-relative")
L.append("")
L.append("The corpus uses root-relative `/docs/...` for internal links, with zero file-relative links. "
         "Three links break that convention, all pointing at the same page:")
L.append("")
L.append("| Doc | Line | Current URL | Recommended URL |")
L.append("|---|---|---|---|")
L.append("| `Version 1.x.x/Miscellaneous/Create Custom CLI Plugins for Contentstack \\| V1.x.x` | 9 | "
         "`https://www.contentstack.com/docs/headless-cms/install-the-cli` | `/docs/headless-cms/install-the-cli` |")
L.append("| `Version 1.x.x/CLI Advanced Operations/Change Master Locale` | 16 | "
         "`https://www.contentstack.com/docs/headless-cms/install-the-cli` | `/docs/headless-cms/install-the-cli` |")
L.append("| `Version 2.x.x/CLI Advanced Operations V2/Change Master Locale` | 16 | "
         "`https://www.contentstack.com/docs/headless-cms/install-the-cli` | `/docs/headless-cms/install-the-cli` |")
L.append("")
L.append("The two `Change Master Locale` rows are one CMS entry shown in two nav locations, so fixing it once "
         "resolves both.")
L.append("")
L.append("### 5b. Login URL trailing slash")
L.append("")
L.append("`https://www.contentstack.com/login/` appears 33 times and `https://www.contentstack.com/login` "
         "20 times, inside the same Prerequisites boilerplate. Both resolve. Pick one and enforce it. "
         "Recommended: **without** the trailing slash, matching the rest of the corpus.")
L.append("")
L.append("### 5c. A V2 doc linking into V1")
L.append("")
L.append("| Doc | Line | Current URL | Recommended URL |")
L.append("|---|---|---|---|")
L.append("| `Version 2.x.x/CLI Commands V2/CLI for Launch \\| V2.x.x` | 19 | "
         "`/docs/headless-cms/install-the-cli/v1` | `/docs/headless-cms/install-the-cli` |")
L.append("")
L.append("This is in the Prerequisites list, so a reader following the V2 doc is sent to the V1 install page. "
         "It is the only `/v1` leak left in V2. Note the same line also cites version gates "
         "(\"version 1.6.0 and above\" for AWS and similar) that predate V2, so the sentence needs a content "
         "check alongside the link fix.")
L.append("")
L.append("---")
L.append("")
L.append("## 6. What this means for the doc standard")
L.append("")
L.append("Three rules worth adding to the CLI templates in WI-2, each earned by a finding above:")
L.append("")
L.append("1. **Any heading that is a link target must be H2 or H3.** H4 gets no id and no right-nav entry, so a "
         "procedure documented at H4 cannot be linked to or navigated to. This is mechanically checkable: "
         "flag every same-page anchor whose target heading is H4 or deeper.")
L.append("2. **Do not nest command procedures below H3.** The `CLI Authentication` pattern of "
         "`## Commands` then `### Authentication` then `#### Login` buries every actual procedure past the "
         "navigable depth. Command procedures belong at H3 directly under an H2.")
L.append("3. **Cross-doc deep links must be verified against the rendered page, not computed.** Given the "
         "inconsistent slug behavior shown above, a linter can flag a suspicious anchor but cannot confirm one. "
         "The live check in `scripts/sweep_cli_links.py` stays part of the release routine.")
L.append("")
L.append("---")
L.append("")
L.append("## Reproducing this report")
L.append("")
L.append("```bash")
L.append("# live pass: outbound link status plus the anchors present in the served pages")
L.append("python3 scripts/sweep_cli_links.py --env prod")
L.append("```")
L.append("")
L.append("The cross-doc anchor pass in sections 1 and 2 is not yet a committed script. It reads links from the "
         "local `docs/markdown/` mirror and resolves each one against ids fetched from the rendered production "
         "page. Folding it into `sweep_cli_links.py` as a second mode would make it repeatable, and is "
         "recommended, since the two passes catch different defects.")
L.append("")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write("\n".join(L) + "\n")
print("wrote", OUT)
print("rows:", len(rows), "fix:", len(FIX), "h4:", len(H4))
