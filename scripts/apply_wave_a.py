#!/usr/bin/env python3
"""Wave A: structural edits to the CLI docs that invent no prose.

Four steps, applied to the HTML in docs/json/ (never to docs/markdown/, which is
generated output and is rebuilt from the JSON):

  A1  Heading depth. CLI-C1 stops CLI headings at H3, because the renderer emits
      an anchor id and a right-hand nav entry for h2 and h3 only. Every h4 is
      either promoted to h3 or converted to a bold lead-in.
  A2  Intro section. Insert or rename so the intro prose sits under an
      "Overview" h2. No text is written.
  A3  Plural section names, per CLI-C9. Limitation -> Limitations, and so on.
  A4  Prerequisites to h2 where it sits deeper.

Usage:
  python3 scripts/apply_wave_a.py                 # dry run, prints every edit
  python3 scripts/apply_wave_a.py --confirm       # write
  python3 scripts/apply_wave_a.py --only <substr> # one doc
  python3 scripts/apply_wave_a.py --steps a1,a3   # subset of steps
  python3 scripts/apply_wave_a.py --all-versions  # lift the V1 subset gate
"""

import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.docs_html import (Doc, cli_json_paths, insert_heading_before, norm_text,
                           promote_heading, rename_heading, to_bold_lead_in)

# --------------------------------------------------------------------------
# A1: heading depth
# --------------------------------------------------------------------------

# Two docs need a policy rather than a per-heading rule, because in both cases a
# per-heading rule produces a structure that C6 forbids: sibling headings of the
# same kind ending up at different levels purely because of which ones happen to
# have an inbound link today.
#
# The rest of the corpus is uniform: every remaining h4 is a facet of the command
# above it (Syntax, Flags, Output, Examples) or a per-item change note, and none
# is a navigation target. Those all become bold lead-ins.

AUTH_DOCS = "CLI Authentication and Adding Tokens"
MIGRATION_GUIDE = "Migrate from Contentstack CLI V1 to V2"
LAUNCH_DOCS = "CLI for Launch"

# A1 policy for the auth docs. Current shape:
#   h2 Commands / h3 Authentication / h4 Login, Logout, Display Username
#              \ h3 Token Management / h4 Add Management Token, ...
# The seven h4s are the auth:* commands, so CMD1 puts them at h3. The two h3
# groupings are labels rather than commands, so they become bold lead-ins. The
# Commands h2 stays, because the template requires it. This is the edit that
# repairs 26 inbound deep links, without touching a single href.
AUTH_GROUP_LABELS = {"authentication", "token management"}

# A1 policy for the migration guide. Its h3s are command ids and are the real
# navigation targets. Its 43 h4s are per-command change notes, with "Removed
# Flags" recurring 22 times, so none of them is a heading a reader navigates to.
# All become bold lead-ins. Two same-page links point into two of them and are
# retargeted to the owning command's anchor instead. Those two anchor ids were
# read off the rendered page, not predicted: the renderer drops the colons
# entirely, so cm:stacks:export becomes #cmstacksexport rather than
# #cm-stacks-export.
MIGRATION_LINK_RETARGET = {
    "#removed-import-config-keys-custom-plugins-and-config-files": "#cmstacksimport",
    "#global-fields-format-changed-per-file": "#cmstacksexport",
}

# A1 policy for CLI for Launch. A Prerequisites heading and its one sibling sit at
# h4 under an h3. Prerequisites is a structural section the template names, so it
# has to be reachable. Both members of the group go to h3 together.
LAUNCH_PROMOTE = {"prerequisites", "triggering redeployments in ci"}


def step_a1(doc):
    edits = []
    name = doc.rel

    if AUTH_DOCS in name:
        for h in doc.headings(level=3):
            if norm_text(h.get_text()).lower() in AUTH_GROUP_LABELS:
                edits.append(to_bold_lead_in(h))
        for h in doc.headings(level=4):
            edits.append(promote_heading(h, 3))
        return edits

    if MIGRATION_GUIDE in name:
        for h in doc.headings(min_level=4):
            edits.append(to_bold_lead_in(h))
        for a in doc.soup.find_all("a", href=True):
            new = MIGRATION_LINK_RETARGET.get(a["href"])
            if new:
                edits.append(f"retargeted same-page link {a['href']} -> {new}")
                a["href"] = new
        return edits

    if LAUNCH_DOCS in name:
        for h in doc.headings(level=4):
            if norm_text(h.get_text()).lower() in LAUNCH_PROMOTE:
                edits.append(promote_heading(h, 3))
            else:
                edits.append(to_bold_lead_in(h))
        return edits

    for h in doc.headings(min_level=4):
        edits.append(to_bold_lead_in(h))
    return edits


# --------------------------------------------------------------------------
# A2: the intro section
# --------------------------------------------------------------------------

# Intro headings the corpus uses instead of Overview. Renaming is preferred over
# inserting, because the prose is already introduced, just under the wrong name.
INTRO_ALIASES = {
    "introduction", "what you will learn", "what you'll learn",
    "process overview", "about", "summary",
}

# A first h2 that is emphatically not an intro. If the doc opens with one of
# these, the intro prose above it is untitled and needs an inserted Overview.
NON_INTRO_FIRST = {"prerequisites", "commands", "command reference", "quick start",
                   "steps for execution", "installation", "overview"}


def step_a2(doc):
    edits = []
    if doc.find_heading("Overview", level=2):
        return edits

    # Case 1: the intro exists under another name. Rename it.
    for h in doc.headings(level=2):
        if norm_text(h.get_text()).lower() in INTRO_ALIASES:
            edits.append(rename_heading(h, "Overview"))
            return edits

    # Case 2: prose sits above the first h2 with no heading. Title it.
    first_h2 = doc.soup.find("h2")
    if first_h2 is None:
        return edits
    lead = [n for n in first_h2.find_all_previous(["p", "ul", "ol", "table", "pre"])]
    if not lead:
        return edits
    # find_all_previous walks backwards, so the earliest node is last.
    top = lead[-1]
    edits.append(insert_heading_before(top, "Overview", level=2))
    return edits


# --------------------------------------------------------------------------
# A3: plural section names
# --------------------------------------------------------------------------

PLURALS = {"limitation": "Limitations", "troubleshoot": "Troubleshooting",
           "next step": "Next Steps"}


def step_a3(doc):
    edits = []
    for h in doc.headings(level=2):
        target = PLURALS.get(norm_text(h.get_text()).lower())
        if target:
            edits.append(rename_heading(h, target))
    return edits


# --------------------------------------------------------------------------
# A4: Prerequisites to h2
# --------------------------------------------------------------------------

def step_a4(doc):
    edits = []
    if doc.find_heading("Prerequisites", level=2):
        return edits
    for level in (3, 4, 5):
        for h in doc.headings(level=level):
            if norm_text(h.get_text()).lower() in ("prerequisites", "prerequisite"):
                edits.append(promote_heading(h, 2))
                if norm_text(h.get_text()).lower() == "prerequisite":
                    edits.append(rename_heading(h, "Prerequisites"))
                return edits
    return edits


STEPS = [("a1", "heading depth", step_a1),
         ("a2", "intro section", step_a2),
         ("a3", "plural section names", step_a3),
         ("a4", "Prerequisites level", step_a4)]

# --------------------------------------------------------------------------
# Scope
# --------------------------------------------------------------------------

# V2 is GA and gets the full restructure. V1 is superseded and gets only the two
# steps that fix something broken rather than reshaping the page:
#   a1, because an h4 is unlinkable on V1 exactly as it is on V2
#   a4, because a Prerequisites heading below h2 is invisible to the page nav
# a2 and a3 change the section shape, so they stay off V1.
#
# The exception is the 7 docs that are one CMS entry shown in two nav locations.
# Editing the V2 file edits that entry, so the V1 file has to receive the same
# edit or the two local mirrors of one entry drift apart. Those get all 4 steps.
V1_STEPS = {"a1", "a4"}


def shared_uids(paths):
    """UIDs that appear under more than one version folder."""
    import json
    seen = {}
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            uid = json.load(fh).get("uid")
        seen.setdefault(uid, set()).add(
            "V1" if os.sep + "Version 1" in path or "/Version 1" in path else "V2")
    return {uid for uid, versions in seen.items() if len(versions) > 1}


def steps_for(path, uid, shared, requested, all_versions=False):
    """Which step keys apply to this doc, intersected with what was requested.

    `all_versions` lifts the V1 restriction. It exists because the scope
    decision changed: the first pass was "V2 full restructure, V1 safe subset
    only", so a2 and a3 never ran on V1 and 32 V1 docs still have untitled
    intro prose. The full restructure was approved later, and lifting the gate
    is the honest way to record that rather than editing V1_STEPS and losing
    why it was ever narrow.
    """
    is_v1 = "Version 1" in path
    if all_versions or not is_v1 or uid in shared:
        allowed = {k for k, _, _ in STEPS}
    else:
        allowed = V1_STEPS
    return [k for k, _, _ in STEPS if k in allowed and k in requested]


def main():
    confirm = "--confirm" in sys.argv
    all_versions = "--all-versions" in sys.argv
    only = None
    steps = [s[0] for s in STEPS]
    for arg in sys.argv[1:]:
        if arg.startswith("--only="):
            only = arg.split("=", 1)[1]
        elif arg.startswith("--steps="):
            steps = [s.strip().lower() for s in arg.split("=", 1)[1].split(",")]

    paths = cli_json_paths()
    if only:
        paths = [p for p in paths if only.lower() in p.lower()]
        if not paths:
            sys.exit(f"no doc matched --only={only}")

    shared = shared_uids(cli_json_paths())
    tally = collections.Counter()
    touched = 0
    by_version = collections.Counter()
    for path in paths:
        doc = Doc.load(path)
        uid = doc.entry.get("uid")
        applicable = steps_for(path, uid, shared, steps, all_versions)
        edits = []
        for key, _label, fn in STEPS:
            if key not in applicable:
                continue
            produced = fn(doc)
            edits.extend(f"[{key}] {e}" for e in produced)
            tally[key] += len(produced)

        if not edits:
            continue
        touched += 1
        by_version["V1" if "Version 1" in path else "V2"] += 1
        scope = "full" if len(applicable) == len([k for k, _, _ in STEPS if k in steps]) \
            else "V1 safe subset"
        shared_note = "  [shared entry with V2]" if uid in shared else ""
        print(f"\n{'PUSH' if confirm else 'DRY-RUN'}  {doc.rel}")
        print(f"    scope: {scope}{shared_note}")
        for e in edits:
            print(f"    {e}")
        doc.save(dry_run=not confirm)

    print("\n" + "=" * 68)
    print(f"docs touched: {touched} of {len(paths)}   "
          f"(V2 {by_version['V2']}, V1 {by_version['V1']})")
    for key, label, _ in STEPS:
        if key in steps:
            print(f"  {key}  {label:24s} {tally[key]} edit(s)")
    if not confirm:
        print("\nDry run. Nothing written. Re-run with --confirm to apply.")
    else:
        print("\nWritten to docs/json. Next: python3 scripts/json_to_markdown.py")


if __name__ == "__main__":
    main()
