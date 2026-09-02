#!/usr/bin/env python3
"""Wave D, tier 1: the Commands and Steps for Execution headings.

Wave D has 259 missing-section findings. They are not one job. Sorting them by
what can honestly be sourced:

  tier 1   59  Overview, Commands, Steps for Execution, Quick Reference.
                Structural. The content is already on the page, it just has no
                heading over it, or has one under another name.
  tier 2   99  Next Steps and Examples. Derivable from verified data:
                cli-url-map.csv for link targets, flag-inventory.json for real
                flags. Every link has to return 200 before it ships.
  tier 3   97  Troubleshooting and Limitations. NOT derivable. The plugin
                sources yield 18 thrown error messages and about 120 error call
                sites across 47 docs that need a Troubleshooting section. Where
                no failure mode can be sourced, the section is omitted, because
                a fabricated root cause reads exactly as authoritative as a real
                one and the reader cannot tell. That is the failure mode CLI-C11
                and CLI-C12 exist to prevent.

This script does the tier-1 Commands and Steps for Execution work only. The
tier-1 Overview work was done by re-running apply_wave_a.py with
--all-versions, which lifted the V1 subset gate that had kept a2 and a3 off the
V1 tree.

Demotion is anchor safe, which is what makes this mechanical rather than risky.
The renderer emits an anchor id for h2 and h3 alike, and the id derives from the
heading text, so moving a heading from h2 to h3 keeps its id. Verified on the
live Compare and Merge Branches page, which carries ids for both its h2
sections (steps-to-compare-branches) and its h3 subsections (create-a-branch,
delete-a-branch, list-branches). Six inbound anchor links point into these
docs and all six survive.

Two patterns, and only where the answer is not a judgment call:

  rename    The section exists under an alias. `Command Reference`,
            `Export Command` and `Import Command` are all the Commands section
            named differently. A rename changes one heading and no content.

  wrap      The band between Prerequisites and the tail is entirely per-command
            procedures or a numbered spine. Insert the required h2 and demote
            those headings to h3 beneath it.

Everything else is deferred to notes/reports/wave-d-deferred.md with a reason,
because guessing which of five task-shaped h2 sections belong under a Commands
heading is an editorial decision, not a mechanical one.

Usage:
  python3 scripts/apply_wave_d1.py            # dry run
  python3 scripts/apply_wave_d1.py --confirm  # write
"""

import collections
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.docs_html import Doc, JSON_DIR, norm_text  # noqa: E402

V1 = "Version 1.x.x"
V2 = "Version 2.x.x"

# (rel path, op, *args)
#   rename <old> <new>
#   wrap   <new h2> [<h2 to demote>, ...]
PLAN = [
    (f"{V1}/CLI Commands/Regex Validate Plugin | V1.x.x.json",
     "rename", "Command Reference", "Commands"),
    (f"{V2}/CLI Commands V2/Regex Validate Plugin | V2.x.x.json",
     "rename", "Command Reference", "Commands"),
    (f"{V1}/CLI Commands/Export Content Using the CLI | V1.x.x.json",
     "rename", "Export Command", "Commands"),
    (f"{V1}/CLI Commands/Import Content Using the CLI | V1.x.x.json",
     "rename", "Import Command", "Commands"),

    (f"{V1}/CLI Advanced Operations/Configure MFA Secret Using CLI | V1.x.x.json",
     "wrap", "Commands", ["Set MFA Secret", "Remove MFA Secret"]),
    (f"{V2}/CLI Advanced Operations V2/Configure MFA Secret Using CLI | V2.x.x.json",
     "wrap", "Commands", ["Set the MFA Secret", "Remove the MFA Secret"]),

    (f"{V1}/Migration Use Cases/Migrate and Overwrite Content in the Same Stack | V1.x.x.json",
     "wrap", "Steps for Execution",
     ["Step 1: Export Content (If Not Already Exported)", "Step 2: Run Import Setup",
      "Step 3: Import with Overwrite"]),
    (f"{V2}/CLI Migration Use Cases V2/Migrate and Overwrite Content in the Same Stack | V2.x.x.json",
     "wrap", "Steps for Execution",
     ["Step 1: Export Content (If Not Already Exported)", "Step 2: Run Import Setup",
      "Step 3: Import with Overwrite"]),
]

# Why each remaining doc is not in PLAN. Written to the deferred report so the
# gap is a known quantity rather than an oversight.
DEFERRED = [
    ("Compare and Merge Branches Using the CLI, both versions", "Commands",
     "Five h2 sections named `Steps to ...` cover ten commands between them. "
     "Mapping each command to its own h3 is the restructure CMD1 asks for, and "
     "it needs someone who knows which command belongs to which step."),
    ("Generate Typescript Typings with TSGen Plugin, both versions", "Commands",
     "Carries `Usage` and `Options` rather than a command section. Whether "
     "Commands should absorb both, or `Usage` alone becomes Commands with "
     "`Options` as its flag table, is an editorial call."),
    ("Query-based Export, both versions", "Commands",
     "Has Overview, Prerequisites, Installation, Query Format and Limitations "
     "and documents no command section at all. This is missing content, not a "
     "missing heading."),
    ("Bootstrap Starter Apps, both versions", "Steps for Execution",
     "The band holds four procedure sections plus `Supported Starter Apps`, "
     "which is reference material. Wrapping all five under Steps for Execution "
     "would file reference content as a step."),
    ("Create Custom CLI Plugins for Contentstack, both versions", "Steps for Execution",
     "Twelve h2 sections spanning build, test, publish and plugin management. "
     "cli-template-research.md already recommends splitting the cli-utilities "
     "API surface out of this doc, so its structure is a Wave E decision."),
    ("Branches, Migration Use Cases, both versions", "Steps for Execution",
     "Two h2 sections, each a separate use case with its own procedure. One "
     "Steps for Execution spine would have to merge two independent walkthroughs."),
    ("Migrate Selected Content Using the Query Export Plugin", "Steps for Execution",
     "Interleaves procedure sections with `Query Format` and `Export Output "
     "Structure` reference sections, so the spine is not contiguous."),
    ("Create Custom CLI Commands", "Steps for Execution",
     "Being retired. Its step one is `csdx plugins:create`, which has never "
     "shipped. Release blt709e2fb5f57c8659 unpublishes it, pending approval."),
]


def sibling_paths(rel):
    """Every docs/json path holding the same entry, so shared entries stay in sync."""
    index = json.load(open(os.path.join(JSON_DIR, "index.json"), encoding="utf-8"))
    uid = next((e["uid"] for e in index["entries"] if e["json"] == rel), None)
    if uid is None:
        return [rel]
    return [e["json"] for e in index["entries"] if e["uid"] == uid]


def find_h2(doc, text):
    want = norm_text(text)
    for h in doc.soup.find_all("h2"):
        if norm_text(h.get_text()) == want:
            return h
    return None


def words(text):
    text = re.sub(r"<[^>]+>", " ", text)
    return collections.Counter(re.findall(r"[A-Za-z0-9_./:@-]{2,}", text))


def do_rename(doc, old, new):
    if find_h2(doc, new):
        return None, f"a {new} h2 already exists"
    h = find_h2(doc, old)
    if h is None:
        return None, f"{old} not found"
    h.string = new
    return [f"rename  {old} -> {new}"], None


def do_wrap(doc, new_h2, demote):
    if find_h2(doc, new_h2):
        return None, f"a {new_h2} h2 already exists"
    tags = []
    for text in demote:
        h = find_h2(doc, text)
        if h is None:
            return None, f"{text} not found, refusing to wrap a partial set"
        tags.append(h)
    # The wrapper goes immediately before the first heading it will own.
    wrapper = doc.soup.new_tag("h2")
    wrapper.string = new_h2
    tags[0].insert_before(wrapper)
    for h in tags:
        h.name = "h3"
    return ([f"insert  h2 '{new_h2}'"] +
            [f"demote  '{t}' h2 -> h3" for t in demote]), None


def main():
    confirm = "--confirm" in sys.argv
    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to write\n")

    expanded = []
    for rel, op, *args in PLAN:
        for sibling in sibling_paths(rel):
            expanded.append((sibling, op, args))

    written, failures = 0, []
    for rel, op, args in expanded:
        path = os.path.join(JSON_DIR, rel)
        if not os.path.exists(path):
            failures.append(f"{rel}: not found")
            continue
        doc = Doc.load(path)
        before = words(str(doc.soup))
        log, error = (do_rename(doc, *args) if op == "rename"
                      else do_wrap(doc, args[0], args[1]))
        name = rel.split("/")[-1][:58]
        if error:
            print(f"{name}\n    SKIP  {error}")
            failures.append(f"{rel}: {error}")
            continue
        after = words(str(doc.soup))
        allowed = set()
        for a in args:
            for token in (a if isinstance(a, list) else [a]):
                allowed |= set(re.findall(r"[A-Za-z0-9_./:@-]{2,}", token))
        lost = {w: before[w] - after.get(w, 0)
                for w in before if before[w] > after.get(w, 0) and w not in allowed}
        print(f"{name}  ({doc.entry['uid']})")
        for line in log:
            print(f"    {line}")
        if lost:
            print(f"    WORD LOSS  {lost}")
            failures.append(f"{rel}: word loss {lost}")
            continue
        if confirm and doc.save():
            written += 1

    report = os.path.join(os.path.dirname(JSON_DIR), "..", "notes", "reports",
                          "wave-d-deferred.md")
    report = os.path.normpath(report)
    lines = ["# Wave D: what was deferred, and why", "",
             "Wave D had 259 missing-section findings. This records the ones that "
             "are not mechanical, so the gap stays a known quantity.", "",
             "The rule throughout: **omit rather than invent.** A fabricated root "
             "cause or a guessed section boundary reads exactly as authoritative "
             "as a real one, and the reader cannot tell the difference. A visible "
             "hole that the linter keeps reporting is the better outcome.", "",
             "## Commands and Steps for Execution", "",
             "| Doc | Section | Why it needs a person |", "|---|---|---|"]
    for doc_name, section, why in DEFERRED:
        lines.append(f"| {doc_name} | `{section}` | {why} |")
    lines += ["", "## Troubleshooting and Limitations", "",
              "97 findings, and the least sourceable work in the wave. The cloned "
              "plugin sources yield 18 thrown error messages and roughly 120 error "
              "call sites in total, spread across 47 docs that need a "
              "Troubleshooting section. Some docs have two or three sourceable "
              "failures. Some have none.", "",
              "Each section must use `**Root Cause**` or `**Root Causes**` per "
              "`sdk-templates/common-rules.md`, which `checks/troubleshooting-"
              "format.js` enforces correctly now that its literal "
              "`**Root Cause(s)**` requirement is fixed.", "",
              "## Next Steps and Examples", "",
              "99 findings, and the most sourceable. `Next Steps` needs a link plus "
              "a one-sentence description per entry, which `C1-06` requires and "
              "which the plugin-guide pass showed is worth doing properly: adding "
              "bare links there raised the error count until the descriptions went "
              "in. Targets come from `cli-url-map.csv` and every one must return "
              "200 before it ships. `Examples` draws on the 58 commands and 360 "
              "flags in `notes/reports/flag-inventory.json`.", ""]
    if confirm:
        os.makedirs(os.path.dirname(report), exist_ok=True)
        open(report, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print(f"\nwrote {os.path.relpath(report, os.getcwd())}")

    print()
    if failures:
        print("SKIPPED:")
        for f in failures:
            print("  " + f)
    if not confirm:
        print("Dry run complete. Nothing written.")
        return 0
    print(f"wrote {written} json files. Regenerating docs/markdown ...")
    subprocess.run([sys.executable, os.path.join(os.getcwd(), "scripts",
                                                 "json_to_markdown.py")], check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
