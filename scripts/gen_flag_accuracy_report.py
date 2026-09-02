#!/usr/bin/env python3
"""Check what the V2 docs say about flags against what CLI 2.0.0 actually ships.

The structural work asks whether a doc has the right sections. This asks a
different and sharper question: is what it says true. A missing Troubleshooting
section is untidy. A flag that does not exist sends the reader to a command that
fails.

Ground truth is notes/reports/flag-inventory.json, generated from the
oclif.manifest.json inside each published npm tarball. Run
scripts/gen_flag_inventory.py first.

Three findings are reported, and they are ordered by how much they cost a reader:

  GHOST    the doc documents a flag that exists on NO GA command at all. The
           reader copies it and the command fails.
  FOREIGN  the flag is real but belongs to a different command than the one the
           doc is about. Usually the doc is factually right and the table simply
           mixes two commands without saying so, which CMD1 asks it not to do.
  MISSING  the command has a flag the doc never mentions. The reader cannot
           discover it.
  SWAPPED  a documented flag exists, but its description matches a different
           flag on the same command. The reader uses the right name for the
           wrong purpose, which fails in a way that looks like their own error.

Scoping. A finding is only reported when the doc can be tied to exactly one
command, either by a heading naming a command id or by the doc mentioning exactly
one command in a `csdx` example. Comparing an unscoped table against every
command at once produces noise, not findings.

Read-only. Writes one report.

Usage:
  python3 scripts/gen_flag_accuracy_report.py
"""

import collections
import difflib
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY = os.path.join(ROOT, "notes", "reports", "flag-inventory.json")
MD = os.path.join(ROOT, "docs", "markdown", "Version 2.x.x")
OUT = os.path.join(ROOT, "notes", "reports", "cli-flag-accuracy-report.md")

# Plugins that publish no oclif.manifest.json, so GA flag data does not exist for
# their commands. Their docs cannot be checked and are listed as such rather than
# reported as full of ghosts.
UNCHECKABLE_PREFIXES = ("launch", "app:", "app ")

# oclif generates `--no-X` automatically for a boolean flag declared with allowNo.
# The docs are right to mention those even though the manifest lists only `X`.


def esc(text):
    return str(text).replace("|", "\\|")


def load_inventory():
    if not os.path.exists(INVENTORY):
        sys.exit("Run scripts/gen_flag_inventory.py first.")
    return json.load(open(INVENTORY, encoding="utf-8"))


def doc_commands(text):
    """Command ids the doc names, with how often, so a single subject can be found."""
    counts = collections.Counter()
    for m in re.finditer(r"`(?:csdx\s+)?([a-z][a-z0-9-]*(?::[a-z][a-z0-9-]*)+)`", text):
        counts[m.group(1)] += 1
    for m in re.finditer(r"csdx\s+([a-z][a-z0-9-]*(?::[a-z][a-z0-9-]*)+)", text):
        counts[m.group(1)] += 1
    return counts


def flag_rows(text, own_command=None):
    """{flag name: description} from every table row whose first cell is a flag.

    A table whose lead-in names a different command is skipped. Docs legitimately
    quote another command's flags, and `Import Content Using the CLI` does exactly
    that for `config:set:log`. Once the lead-in says so, the rows are not claims
    about the doc's own command and must not be read as such.
    """
    rows = {}
    lead_command = None
    for line in text.split("\n"):
        if not line.startswith("|"):
            # Two forms declare the command a following table belongs to. Inline
            # code, `csdx cm:stacks:export`, and the bare syntax line inside a
            # fence, `csdx cm:stacks:bulk-taxonomies [OPTIONS]`. The second form
            # has no backticks because the fence already supplies them, and
            # missing it produced three false positives on Bulk Operations in
            # CLI, where each command's section is introduced by exactly that
            # line. The doc was right and the checker was reading the wrong
            # lead-in.
            m = (re.search(r"`(?:csdx\s+)?([a-z][a-z0-9-]*(?::[a-z][a-z0-9-]*)+)`", line)
                 or re.search(r"csdx\s+([a-z][a-z0-9-]*(?::[a-z][a-z0-9-]*)+)", line))
            if m and line.strip():
                lead_command = m.group(1)
            continue
        if own_command and lead_command and lead_command != own_command:
            continue
        _consume(line, rows)
    return rows


def _consume(line, rows):
    for line in (line,):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        # Four shapes appear in the corpus: `--flag`, `--flag=<value>`,
        # `--flag`, `-f` (the CLI-C2 order), and `-f, --flag` (the older order
        # that Wave C has not reached yet). Anchoring on a leading `-- missed
        # the last of those and produced four false MISSING findings on Bulk
        # Operations in CLI, where every flag is written short form first. So
        # the test is "this cell starts with a flag" and then the long name is
        # taken from wherever in the cell it appears.
        if not re.match(r"^`\s*-", cells[0]):
            continue
        m = re.search(r"--([A-Za-z][\w-]*)", cells[0])
        if not m:
            continue
        # The description is the longest remaining cell, which survives the
        # column-order differences still present across the corpus.
        body = max(cells[1:], key=len) if len(cells) > 1 else ""
        rows[m.group(1)] = re.sub(r"<br\s*/?>", " ", body)


def normalise(text):
    text = re.sub(r"\[?optional\]?", " ", text, flags=re.I)
    text = re.sub(r"[`*\\<>\[\]]", " ", text)
    text = re.sub(r"[^a-z0-9 ]", " ", text.lower())
    return " ".join(text.split())


def best_match(description, ga_flags):
    """The GA flag whose description most resembles this one, and the score."""
    target = normalise(description)
    if len(target) < 25:
        return None, 0.0
    best, score = None, 0.0
    for name, flag in ga_flags.items():
        s = difflib.SequenceMatcher(None, target, normalise(flag["description"])).ratio()
        if s > score:
            best, score = name, s
    return best, score


def main():
    inv = load_inventory()
    ga = inv["commands"]

    findings = []
    scoped = unscoped = unchecked = 0
    checked_docs = []

    for path in sorted(glob.glob(MD + "/**/*.md", recursive=True)):
        text = open(path, encoding="utf-8").read()
        text = re.sub(r"^---.*?^---", "", text, flags=re.S | re.M)
        rel = os.path.relpath(path, os.path.dirname(MD))
        rows = flag_rows(text)
        if not rows:
            continue

        counts = doc_commands(text)
        known = {c: n for c, n in counts.items() if c in ga}
        if any(c.startswith(UNCHECKABLE_PREFIXES) for c in counts) and not known:
            unchecked += 1
            checked_docs.append((rel, "no GA manifest for this plugin", 0, 0))
            continue
        if not known:
            unscoped += 1
            checked_docs.append((rel, "no command this inventory knows", 0, 0))
            continue
        # One clear subject: the most-mentioned command, when it dominates.
        top, top_n = max(known.items(), key=lambda kv: kv[1])
        if len(known) > 1 and top_n < 2 * max(n for c, n in known.items() if c != top):
            unscoped += 1
            checked_docs.append((rel, f"documents {len(known)} commands, not scoped", 0, 0))
            continue

        scoped += 1
        rows = flag_rows(text, own_command=top)
        ga_flags = ga[top]["flags"]
        ga_names = set(ga_flags)
        allow_no = {"no-" + n for n, f in ga_flags.items() if f["type"] == "boolean"}

        elsewhere = {n: sorted(c for c, cc in ga.items() if n in cc["flags"])
                     for n in rows if n not in ga_names}
        ghosts, foreign = [], []
        for n in sorted(rows):
            if n in ga_names or n in allow_no or n.startswith(("help", "version")):
                continue
            base = n[3:] if n.startswith("no-") else n
            owners = elsewhere.get(n) or [c for c, cc in ga.items() if base in cc["flags"]]
            (foreign if owners else ghosts).append((n, owners))
        missing = sorted(n for n in ga_names
                         if n not in rows and not ga_flags[n]["hidden"])
        swapped = []
        for name, desc in sorted(rows.items()):
            if name not in ga_names:
                continue
            match, score = best_match(desc, ga_flags)
            if match and match != name and score > 0.72:
                own = difflib.SequenceMatcher(
                    None, normalise(desc), normalise(ga_flags[name]["description"])).ratio()
                if score - own > 0.2:
                    swapped.append((name, match, round(score, 2), round(own, 2)))

        checked_docs.append((rel, top, len(rows), len(ga_names)))
        for n, _ in ghosts:
            findings.append(("GHOST", rel, top, n, "exists on no GA command"))
        for n, owners in foreign:
            findings.append(("FOREIGN", rel, top, n,
                             "belongs to " + ", ".join(f"`{o}`" for o in owners[:3])))
        for n in missing:
            findings.append(("MISSING", rel, top, n,
                             ga_flags[n]["description"][:90] or "no description"))
        for name, match, score, own in swapped:
            findings.append(("SWAPPED", rel, top, name,
                             f"description matches `--{match}` (similarity {score} "
                             f"against {own} for its own)"))

    by_kind = collections.Counter(f[0] for f in findings)
    L = []
    A = L.append
    A("# CLI Flag Accuracy Report")
    A("")
    A("What the V2 docs say about flags, checked against what CLI 2.0.0 ships.")
    A("")
    A("Ground truth is the `oclif.manifest.json` inside each published npm tarball, "
      "collected by `scripts/gen_flag_inventory.py`. The local repo is not used: "
      "`repo/cli-plugins` sits on `v2-dev` with no `v2.0.0` tag, and its export "
      "plugin is still at `2.0.0-beta.24`.")
    A("")
    A("Reproduce with:")
    A("")
    A("```bash")
    A("python3 scripts/gen_flag_inventory.py")
    A("python3 scripts/gen_flag_accuracy_report.py")
    A("```")
    A("")
    A("## Summary")
    A("")
    A("| Finding | Count | What it costs a reader |")
    A("|---|---|---|")
    A(f"| `GHOST` | {by_kind['GHOST']} | Copies a flag that does not exist. The command fails. |")
    A(f"| `FOREIGN` | {by_kind['FOREIGN']} | Table mixes another command's flags in without saying so. |")
    A(f"| `SWAPPED` | {by_kind['SWAPPED']} | Uses a real flag for the wrong purpose. Fails in a way that looks like their mistake. |")
    A(f"| `MISSING` | {by_kind['MISSING']} | Cannot discover a flag the command supports. |")
    A("")
    A(f"{scoped} docs were tied to a single command and checked. {unscoped} could not "
      f"be scoped to one command. {unchecked} document a plugin that publishes no "
      "manifest, so no GA flag data exists for them.")
    A("")
    A("---")
    A("")
    A("## The defect class this report cannot catch")
    A("")
    A("Every check here compares flag **names**. One defect class escapes that "
      "entirely: a flag that keeps its name and changes its meaning.")
    A("")
    A("`cm:stacks:migration --config` is the only instance in the CLI surface. "
      "In V1 it took inline configuration. In 2.0.0 it takes the path of a JSON "
      "configuration file, and inline configuration moved to the new "
      "`--inline-config` flag. A name diff sees no change, and neither does a "
      "reader: a V1 script passing inline values still parses, and GA reads the "
      "string as a file path rather than failing.")
    A("")
    A("It was found by diffing flag **descriptions** between the last 1.x "
      "manifest and 2.0.0, not by diffing names. Re-run that comparison after "
      "any major version, because it is the only thing that surfaces this class. "
      "CLI-C11 states the rule.")
    A("")
    A("---")
    A("")
    A("## Findings")
    A("")
    for kind in ("GHOST", "SWAPPED", "FOREIGN", "MISSING"):
        rows = [f for f in findings if f[0] == kind]
        if not rows:
            continue
        A(f"### {kind} ({len(rows)})")
        A("")
        A("| Doc | Command | Flag | Detail |")
        A("|---|---|---|---|")
        for _k, rel, cid, flag, detail in rows:
            A(f"| `{esc(rel)}` | `{cid}` | `--{flag}` | {esc(detail)} |")
        A("")
    A("---")
    A("")
    A("## Coverage")
    A("")
    A("| Doc | Scoped to | Flags documented | Flags at GA |")
    A("|---|---|---|---|")
    for rel, cid, n_doc, n_ga in checked_docs:
        A(f"| `{esc(rel)}` | `{cid}` | {n_doc or '-'} | {n_ga or '-'} |")
    A("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    print(f"scoped {scoped} docs, {unscoped} unscoped, {unchecked} uncheckable")
    print("findings:", dict(by_kind))
    for kind in ("GHOST", "SWAPPED"):
        for f in findings:
            if f[0] == kind:
                print(f"  {kind:8s} {f[2]:26s} --{f[3]:22s} {f[1].split('/')[-1][:44]}")


if __name__ == "__main__":
    main()
