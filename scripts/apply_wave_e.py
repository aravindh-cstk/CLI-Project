#!/usr/bin/env python3
"""Wave E: the module references.

Three jobs, one of which turned out to be an accuracy bug rather than structure.

1. The Node.js requirement is wrong in both CLI Limitations pages.

   Both say "CLI requires Node.js version 18.0.0 or above (recommended: 20.x or
   22.x)". Checked against the published packages' own engines field, 18 was
   never the requirement for any release:

       1.40.0 to 1.60.0   >=14.0.0
       1.65.0 and 1.68.0  >=22.0.0
       2.0.0              >=22.0.0

   This is user breaking, not untidy. A reader on Node 18 or 20 follows the
   page, installs, and the CLI fails at runtime, which is exactly the
   EBADENGINE failure the V1-to-V2 migration guide warns about.

2. Quick Reference index tables for the four docs that lack one.

   A module reference's Quick Reference exists so nobody scrolls a 1,000 line
   page. CLI Limitations is 20 module sections long and has no index at all.

   Every in-page link in these tables was taken from the live rendered page,
   not derived. Anchor ids are generated at render time and cannot be computed
   offline: the same page proves it, where `Bulk Publish/Unpublish Limitations`
   renders as `bulk-publish-unpublish-limitations` while an existing inbound
   link points at `bulk-publishunpublish-limitations` and resolves to nothing.

3. An Overview for both CLI Limitations pages, which open on `Core CLI
   Limitations` with no intro at all. These are three sentences describing what
   the page indexes and what it does not cover, which is a statement about the
   page's own contents rather than a claim about the product.

Deliberately NOT done: the MOD1 heading renames. MOD1a asks for the real
identifier verbatim, so `Export Module Limitations` would become
`cm:stacks:export`. That would rewrite 20 headings and therefore 20 anchor ids,
and three inbound links already point into these sections. Renaming them before
Wave F has re-baselined the anchors would break working links to fix a naming
rule. Recorded in notes/reports/wave-e-deferred.md instead.

Usage:
  python3 scripts/apply_wave_e.py            # dry run
  python3 scripts/apply_wave_e.py --confirm  # write
"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.docs_html import Doc, JSON_DIR, insert_heading_before  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(ROOT, "notes", "reports", "wave-e-deferred.md")

LIM_V1 = "Version 1.x.x/Miscellaneous/CLI Limitations | V1.x.x.json"
LIM_V2 = "Version 2.x.x/Miscellaneous V2/CLI Limitations | V2.x.x.json"
FEAT_V1 = ("Version 1.x.x/CLI Commands/CLI-Supported Features for Export, Import, "
           "and Clone Operations | V1.x.x.json")
FEAT_V2 = ("Version 2.x.x/CLI Commands V2/CLI-Supported Features for Export, Import, "
           "and Clone Operations | V2.x.x.json")

# The old sentence, matched literally in both pages.
NODE_OLD = ("CLI requires Node.js version 18.0.0 or above (recommended: 20.x or 22.x)")
NODE_NEW_V2 = ("CLI 2.0.0 requires Node.js version 22.0.0 or above, which is what the "
               "package's own engines field declares")
NODE_NEW_V1 = ("CLI 1.65.0 and later require Node.js version 22.0.0 or above. Releases "
               "from 1.40.0 to 1.60.0 declared 14.0.0")
NODE_IMPACT_OLD = "CLI won't work with Node.js versions below 18.0.0"
# The workaround bullet repeated the wrong floor, so fixing only the Limitation
# and Impact lines left "18.0.0+" standing three lines below the correction.
NODE_WORKAROUND_OLD = ("Install supported Node.js version (18.0.0+, recommended: "
                       "20.x or 22.x)")
NODE_WORKAROUND_NEW = {
    "V2": "Install Node.js 22.0.0 or above, then install the CLI",
    "V1": ("Install Node.js 22.0.0 or above for CLI 1.65.0 and later, then install "
           "the CLI"),
}
NODE_IMPACT_NEW = ("On an unsupported Node version the install completes with "
                   "EBADENGINE warnings and appears to succeed, then the CLI fails at "
                   "runtime. Upgrade Node first, then install")

# (Use Case, heading text, verified live anchor id, Key Call).
#
# The linter mandates the columns Use Case, Section and Key Call for a Quick
# Reference table (QUICK_REFERENCE_COLUMNS in checks/quick-reference-table.js).
# The first attempt used Module and Jump to, which read fine and failed the
# check, so these were rebuilt. The mandated shape is the more useful one: a
# reader scanning for "I am exporting a stack" finds it faster than one scanning
# module names.
#
# Every Key Call is a command that exists in the published 2.0.0 manifests, all
# 58 of which are listed in notes/reports/flag-inventory.json. A dash means no
# single command owns that section, which is true of Core CLI, the Variants
# plugin and Configuration. Guessing a plausible command there would be exactly
# the ghost-flag defect one level up.
LIM_INDEX = [
    ("Installing or upgrading the CLI", "Core CLI Limitations",
     "core-cli-limitations", "-"),
    ("Logging in or managing tokens", "Authentication Module Limitations",
     "authentication-module-limitations", "auth:login"),
    ("Exporting a stack", "Export Module Limitations",
     "export-module-limitations", "cm:stacks:export"),
    ("Importing into a stack", "Import Module Limitations",
     "import-module-limitations", "cm:stacks:import"),
    ("Preparing an import", "Import Setup Limitations",
     "import-setup-limitations", "cm:stacks:import-setup"),
    ("Overwriting existing content", "Overwrite Operations Limitations",
     "overwrite-operations-limitations", "cm:stacks:import"),
    ("Publishing or unpublishing in bulk", "Bulk Publish/Unpublish Limitations",
     "bulk-publish-unpublish-limitations", "cm:stacks:bulk-entries"),
    ("Cloning a stack", "Clone Operations Limitations",
     "clone-operations-limitations", "cm:stacks:clone"),
    ("Comparing or merging branches", "Branch Operations Limitations",
     "branch-operations-limitations", "cm:branches:merge"),
    ("Deploying with Launch", "Launch Operations Limitations",
     "launch-operations-limitations", "-"),
    ("Running a migration script", "Migration Scripts Limitations",
     "migration-scripts-limitations", "cm:stacks:migration"),
    ("Bootstrapping a starter app", "Bootstrap Plugin Limitations",
     "bootstrap-plugin-limitations", "cm:bootstrap"),
    ("Seeding a stack", "Seed Command Limitations",
     "seed-command-limitations", "cm:stacks:seed"),
    ("Converting HTML RTE to JSON RTE", "RTE Migration Limitations",
     "rte-migration-limitations", "cm:entries:migrate-html-rte"),
    ("Migrating entries between stacks", "Entry Migration Limitations",
     "entry-migration-limitations", "migrate:import"),
    ("Auditing exported data", "Audit Plugin Limitations",
     "audit-plugin-limitations", "cm:stacks:audit"),
    ("Working with entry variants", "Variants Plugin Limitations",
     "variants-plugin-limitations", "-"),
    ("Managing Marketplace apps", "Apps CLI Limitations",
     "apps-cli-limitations", "-"),
    ("Generating TypeScript typings", "TSGen Plugin Limitations",
     "tsgen-plugin-limitations", "tsgen"),
    ("Setting CLI configuration", "Configuration Limitations",
     "configuration-limitations", "config:set:region"),
]

FEAT_INDEX = [
    ("Checking module coverage", "Supported Modules", "supported-modules", "-"),
    ("Moving Marketplace apps", "Marketplace Apps", "marketplace-apps", "-"),
    ("Meeting the requirements first", "Prerequisites", "prerequisites", "-"),
    ("Moving Personalize data and entry variants", "Personalize and Entry Variants",
     "personalize-and-entry-variants", "-"),
    ("Moving CS Assets", "CS Assets", "cs-assets", "-"),
    ("Running one module at a time", "Module-Wise Operations",
     "module-wise-operations", "cm:stacks:export"),
    ("Reading an error", "Error Handling", "error-handling", "-"),
    ("Following the recommended order", "Best Practices", "best-practices", "-"),
    ("Checking what is not covered", "Limitations", "limitations", "-"),
]

LIM_OVERVIEW = (
    "This page indexes the known limitations of the Contentstack CLI, one section "
    "per module or plugin. Use the Quick Reference below to jump to the module you "
    "are working with rather than reading the page end to end."
)
LIM_OVERVIEW_2 = (
    "Each entry states the limitation, its impact, and a workaround where one "
    "exists. This page does not document command syntax or flags. Those live in "
    "each command's own reference page."
)


def build_table(soup, rows):
    """A Quick Reference table in the mandated Use Case, Section, Key Call shape."""
    table = soup.new_tag("table")
    thead = soup.new_tag("thead")
    tr = soup.new_tag("tr")
    for label in ("Use Case", "Section", "Key Call"):
        th = soup.new_tag("th")
        th.string = label
        tr.append(th)
    thead.append(tr)
    table.append(thead)
    tbody = soup.new_tag("tbody")
    for use_case, text, anchor, call in rows:
        tr = soup.new_tag("tr")
        td = soup.new_tag("td")
        td.string = use_case
        tr.append(td)
        td = soup.new_tag("td")
        # A bare fragment, not a full doc path. C2-04's own test is
        # /\]\(#[^)]+\)/, and it is the right form anyway: the same table is
        # written into both the V1 and V2 copies, so a hardcoded path would send
        # a V1 reader to the V2 page. 289 bare fragment links are already in use
        # across the corpus.
        a = soup.new_tag("a", href=f"#{anchor}")
        a.string = text
        td.append(a)
        tr.append(td)
        td = soup.new_tag("td")
        if call == "-":
            td.string = "-"
        else:
            code = soup.new_tag("span", attrs={"class": "code"})
            code.string = f"csdx {call}"
            td.append(code)
        tr.append(td)
        tbody.append(tr)
    table.append(tbody)
    return table


PLAN = [
    (LIM_V2, "V2", "/docs/headless-cms/cli-limitations", LIM_INDEX),
    (LIM_V1, "V1", "/docs/headless-cms/cli-limitations/v1", LIM_INDEX),
    (FEAT_V2, None,
     "/docs/headless-cms/cli-supported-features-for-export-import-and-clone-operations",
     FEAT_INDEX),
    (FEAT_V1, None,
     "/docs/headless-cms/cli-supported-features-for-export-import-and-clone-operations/v1",
     FEAT_INDEX),
]


def main():
    confirm = "--confirm" in sys.argv
    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to write\n")

    written, notes = 0, []
    for rel, version, _base_url, rows in PLAN:
        path = os.path.join(JSON_DIR, rel)
        if not os.path.exists(path):
            print(f"MISSING {rel}")
            continue
        doc = Doc.load(path)
        html = str(doc.soup)
        log = []

        # 1. the Node.js accuracy fix, CLI Limitations only
        if version:
            new_sentence = NODE_NEW_V2 if version == "V2" else NODE_NEW_V1
            if NODE_OLD in html:
                html = html.replace(NODE_OLD, new_sentence)
                log.append("fix     Node.js requirement, 18.0.0 -> verified value")
            if NODE_IMPACT_OLD in html:
                html = html.replace(NODE_IMPACT_OLD, NODE_IMPACT_NEW)
                log.append("fix     Node.js impact statement")
            if NODE_WORKAROUND_OLD in html:
                html = html.replace(NODE_WORKAROUND_OLD, NODE_WORKAROUND_NEW[version])
                log.append("fix     Node.js workaround bullet")
            if log:
                doc.soup = __import__("bs4").BeautifulSoup(html, "html.parser")

        # 2. Overview, CLI Limitations only
        if version and not doc.find_heading("Overview", level=2):
            first = doc.soup.find("h2")
            if first is not None:
                p1 = doc.soup.new_tag("p")
                p1.string = LIM_OVERVIEW
                p2 = doc.soup.new_tag("p")
                p2.string = LIM_OVERVIEW_2
                first.insert_before(p1)
                first.insert_before(p2)
                insert_heading_before(p1, "Overview", level=2)
                log.append("insert  h2 'Overview' with a 2-paragraph intro")

        # 3. Quick Reference, all four
        if not doc.find_heading("Quick Reference", level=2):
            missing_rows = [t for _u, t, _a, _c in rows
                            if doc.find_heading(t, level=2) is None]
            if missing_rows:
                print(f"{rel.split('/')[-1][:54]}\n    SKIP  index rows with no "
                      f"matching h2: {missing_rows[:3]}")
                notes.append(f"{rel}: index rows had no matching heading")
                continue
            anchor = doc.find_heading("Next Steps", level=2)
            heading = doc.soup.new_tag("h2")
            heading.string = "Quick Reference"
            table = build_table(doc.soup, rows)
            target = anchor
            if target is None:
                # Place it after the Overview block, before the first content h2.
                h2s = doc.soup.find_all("h2")
                after_overview = [h for h in h2s
                                  if h.get_text(strip=True).lower() != "overview"]
                target = after_overview[0] if after_overview else None
            if target is None:
                notes.append(f"{rel}: nowhere safe to place Quick Reference")
                continue
            target.insert_before(heading)
            target.insert_before(table)
            log.append(f"insert  h2 'Quick Reference' with {len(rows)} verified links")

        print(f"{rel.split('/')[-1][:54]}  ({doc.entry['uid']})")
        for line in log:
            print(f"    {line}")
        if not log:
            print("    nothing to do")
        if confirm and doc.save():
            written += 1

    lines = ["# Wave E: what was deferred, and why", "",
             "## The MOD1 heading renames", "",
             "`MOD1a` asks a module reference to name each command or module with its "
             "real identifier verbatim, so `Export Module Limitations` would become "
             "`cm:stacks:export`. Not done, on purpose.", "",
             "Renaming those headings rewrites 20 anchor ids on each CLI Limitations "
             "page, and three inbound links already point into those sections:", "",
             "```", "cli-limitations/v1#import-module-limitations",
             "cli-limitations/v1#export-module-limitations",
             "cli-limitations#bulk-publishunpublish-limitations", "```", "",
             "The third of those is already broken. The live page renders "
             "`bulk-publish-unpublish-limitations`, with a hyphen where the link has "
             "none, which is the clearest available proof that anchor ids are "
             "generated at render time and cannot be derived. Renaming headings before "
             "Wave F has re-baselined the anchors would break two working links in "
             "order to satisfy a naming rule.", "",
             "The right order is Wave F first, then MOD1, with every rename verified "
             "against the re-rendered page.", "",
             "## Splitting the cli-utilities API surface", "",
             "`notes/others/cli-template-research.md` recommends lifting the "
             "`@contentstack/cli-utilities` API reference out of `Create Custom CLI "
             "Plugins for Contentstack | V2.x.x` into its own module reference. That "
             "creates a new page and therefore a new URL, so it needs a slug and a nav "
             "placement decision before it can be written.", "",
             "## The Configuration Reference", "",
             "It carries a trailing `Quick Reference Guide` holding "
             "performance-tuning JSON, which is not the index table `Quick Reference` "
             "means. Renaming it would satisfy the linter by mislabelling the content. "
             "Its remaining errors are almost entirely `CLI-01`: it is over 1,100 lines "
             "of option tables in a shape the standard does not recognise, and "
             "converting those tables is a job of its own.", ""]
    if confirm:
        open(REPORT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print(f"\nwrote {os.path.relpath(REPORT, ROOT)}")
    print()
    for n in notes:
        print("  note: " + n)
    if not confirm:
        print("Dry run complete. Nothing written.")
        return 0
    print(f"wrote {written} json files. Regenerating docs/markdown ...")
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "json_to_markdown.py")],
                   check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
