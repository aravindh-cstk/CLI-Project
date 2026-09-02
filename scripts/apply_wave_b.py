#!/usr/bin/env python3
"""Wave B: section order. Six docs, eleven edits.

Wave B was planned as "263 section reorders" on the strength of C1-01 being the
largest rule count. That was wrong, and the correction matters more than the
wave. All 264 C1-01 findings read `Required section "X" is missing`. Not one
says a section is out of order, and `lib/section-index.compareOrder` was checked
against deliberately reversed input to prove it does detect ordering. So the CLI
docs are already in the mandated relative order, and the 264 belong to Wave D,
which writes the sections that do not exist.

What is genuinely wrong with section order:

  4 out-of-order pairs, reported as C1-02 rather than C1-01.
  7 forbidden `Quick Start` sections, across 6 distinct entries.

`quick start` is forbidden outside a Get Started Guide, per GET_STARTED_ONLY in
checks/section-structure.js, alongside role-based routing table, documentation
map and table of contents. `Examples` and `Common Commands` are both allowed.

Per-doc policy rather than a generic rule, because six docs do not justify
inferring intent and each one differs:

  Bulk Operations, both versions
      Installation sits before Prerequisites. Swap them.
      Quick Start holds runnable scenarios, which is what Examples is for.
      Rename it and move it to the Examples slot, before Troubleshooting.

  Export and Import Content, V1
      Limitations sits before Troubleshooting. Swap them.
      Same Quick Start to Examples rename, placed before Troubleshooting.

  Configure Regions, V1
      Quick Start duplicates the Get Region and Set Region H2s below it, so it
      is a condensed command preview rather than examples. It becomes Common
      Commands. The doc already ends with Developer Examples, which is its real
      examples section and is already in the right place, so that becomes
      Examples. Two renames, nothing moved, and the required Examples section is
      satisfied by content that was already there.

  Contentstack CLI Configuration Reference
      Its Quick Start is an empty heading with no content at all, sitting
      between Overview and Environment Variables. Deleted.
      Its trailing `Quick Reference Guide` is NOT renamed to `Quick Reference`.
      A module reference's Quick Reference is an index table mapping each module
      to its section, and that heading holds performance-tuning JSON snippets.
      Renaming it would satisfy the linter by mislabelling the content. Building
      the real index table is Wave E.

Nothing here writes new prose. Every edit is a rename, a move, or the deletion
of an empty heading, so the word multiset must come out identical except for the
heading words that were deliberately changed. The script asserts that.

Usage:
  python3 scripts/apply_wave_b.py            # dry run
  python3 scripts/apply_wave_b.py --confirm  # write
"""

import collections
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

from docs_html import Doc, JSON_DIR, norm_text  # noqa: E402


def sibling_paths(rel):
    """Every docs/json path holding the same entry as `rel`.

    7 CMS entries appear under two version folders because one entry is shown in
    two nav locations, so docs/json holds two files with the same uid. Editing
    one leaves the other stale, and the stale copy is what the linter reads for
    the other version tree. Contentstack CLI Configuration Reference is one of
    the 7, and the first run of this wave edited only its V1 path, which left
    the forbidden Quick Start heading reported against its V2 path.
    """
    index = json.load(open(os.path.join(JSON_DIR, "index.json"), encoding="utf-8"))
    uid = next((e["uid"] for e in index["entries"] if e["json"] == rel), None)
    if uid is None:
        return [rel]
    return [e["json"] for e in index["entries"] if e["uid"] == uid]

V1_BULK = "Version 1.x.x/CLI Advanced Operations/Bulk Operations in CLI | V1.x.x.json"
V2_BULK = "Version 2.x.x/CLI Commands V2/Bulk Operations in CLI | V2.x.x.json"
V1_EXPORT = "Version 1.x.x/CLI Commands/Export Content Using the CLI | V1.x.x.json"
V1_IMPORT = "Version 1.x.x/CLI Commands/Import Content Using the CLI | V1.x.x.json"
V1_REGIONS = "Version 1.x.x/Get Started with CLI/Configure Regions in the CLI | V1.x.x.json"
CONFIG_REF = "Version 1.x.x/Miscellaneous/Contentstack CLI Configuration Reference.json"

# (rel path, [(op, *args)]). Ops are applied in order.
#   swap   a, b        put a's block where b's is and vice versa
#   rename a, b        rename heading a to b
#   move   a, before   move a's block to immediately before `before`
#   drop   a           delete an empty heading, refusing if it has content
PLAN = [
    # swap reads "put the first before the second", matching the linter's own
    # wording: Section "Prerequisites" must come before "Installation".
    (V1_BULK, [("swap", "Prerequisites", "Installation"),
               ("rename", "Quick Start", "Examples"),
               ("move", "Examples", "Troubleshooting")]),
    (V2_BULK, [("swap", "Prerequisites", "Installation"),
               ("rename", "Quick Start", "Examples"),
               ("move", "Examples", "Troubleshooting")]),
    (V1_EXPORT, [("swap", "Troubleshooting", "Limitations"),
                 ("rename", "Quick Start", "Examples"),
                 ("move", "Examples", "Troubleshooting")]),
    (V1_IMPORT, [("swap", "Troubleshooting", "Limitations"),
                 ("rename", "Quick Start", "Examples"),
                 ("move", "Examples", "Troubleshooting")]),
    (V1_REGIONS, [("rename", "Quick Start", "Common Commands"),
                  ("rename", "Developer Examples", "Examples")]),
    (CONFIG_REF, [("drop", "Quick Start")]),
]

# Heading words this wave deliberately changes, so the word audit can subtract
# them instead of reporting them as loss.
RENAMED_WORDS = {"Quick", "Start", "Developer"}


def h2s(doc):
    return doc.soup.find_all("h2")


def find_h2(doc, text):
    want = norm_text(text)
    for h in h2s(doc):
        if norm_text(h.get_text()) == want:
            return h
    return None


def block(heading):
    """The heading plus every following sibling up to the next h1 or h2."""
    out = [heading]
    node = heading.next_sibling
    while node is not None:
        name = getattr(node, "name", None)
        if name in ("h1", "h2"):
            break
        out.append(node)
        node = node.next_sibling
    return out


def block_is_empty(heading):
    """True when the heading has no rendered content before the next heading."""
    for node in block(heading)[1:]:
        if getattr(node, "name", None) in ("h3", "h4", "h5", "h6"):
            return False
        if node.get_text(strip=True) if hasattr(node, "get_text") else str(node).strip():
            return False
    return True


def insert_block_before(nodes, target):
    for node in nodes:
        target.insert_before(node.extract())


def words(text):
    text = re.sub(r"<[^>]+>", " ", text)
    return collections.Counter(re.findall(r"[A-Za-z0-9_./:@-]{2,}", text))


def apply_ops(doc, ops):
    log = []
    for op in ops:
        kind = op[0]
        if kind == "swap":
            a_name, b_name = op[1], op[2]
            a, b = find_h2(doc, a_name), find_h2(doc, b_name)
            if a is None or b is None:
                return None, f"swap {a_name}/{b_name}: heading not found"
            order = [norm_text(h.get_text()) for h in h2s(doc)]
            if order.index(norm_text(a.get_text())) < order.index(norm_text(b.get_text())):
                return None, (f"swap {a_name}/{b_name}: already in order, "
                              f"refusing to reverse a correct document")
            insert_block_before(block(a), b)
            log.append(f"swap    {a_name} now before {b_name}")
        elif kind == "rename":
            old, new = op[1], op[2]
            h = find_h2(doc, old)
            if h is None:
                return None, f"rename {old}: heading not found"
            if find_h2(doc, new) is not None:
                return None, (f"rename {old} to {new}: a {new} heading already "
                              f"exists, which would create a duplicate")
            h.string = new
            log.append(f"rename  {old} -> {new}")
        elif kind == "move":
            name, before = op[1], op[2]
            h, target = find_h2(doc, name), find_h2(doc, before)
            if h is None or target is None:
                return None, f"move {name} before {before}: heading not found"
            insert_block_before(block(h), target)
            log.append(f"move    {name} to just before {before}")
        elif kind == "drop":
            name = op[1]
            h = find_h2(doc, name)
            if h is None:
                return None, f"drop {name}: heading not found"
            if not block_is_empty(h):
                return None, (f"drop {name}: this heading has content. Deleting it "
                              f"would lose text. Refusing.")
            for node in block(h):
                node.extract()
            log.append(f"drop    {name} (empty heading)")
        else:
            return None, f"unknown op {kind}"
    return log, None


def main():
    confirm = "--confirm" in sys.argv
    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to write\n")

    failures, written = [], 0
    expanded = []
    for rel, ops in PLAN:
        for sibling in sibling_paths(rel):
            expanded.append((sibling, ops))
    for rel, ops in expanded:
        path = os.path.join(JSON_DIR, rel)
        if not os.path.exists(path):
            failures.append(f"{rel}: file not found")
            continue
        doc = Doc.load(path)
        before_words = words(str(doc.soup))
        before_order = [h.get_text(strip=True) for h in h2s(doc)]

        log, error = apply_ops(doc, ops)
        name = rel.split("/")[-1][:58]
        if error:
            print(f"{name}\n    REFUSED  {error}")
            failures.append(f"{rel}: {error}")
            continue

        after_words = words(str(doc.soup))
        lost = {w: before_words[w] - after_words.get(w, 0)
                for w in before_words if before_words[w] > after_words.get(w, 0)}
        unexplained = {w: n for w, n in lost.items() if w not in RENAMED_WORDS}

        print(f"{name}  ({doc.entry['uid']})")
        for line in log:
            print(f"    {line}")
        if unexplained:
            print(f"    WORD LOSS  {unexplained}")
            failures.append(f"{rel}: unexplained word loss {unexplained}")
            continue
        after_order = [h.get_text(strip=True) for h in h2s(doc)]
        print(f"    h2 count {len(before_order)} -> {len(after_order)}, "
              f"words lost: none unexplained")
        if before_order != after_order:
            print(f"    order now: {' > '.join(after_order[:9])}"
                  f"{' > ...' if len(after_order) > 9 else ''}")
        if confirm and doc.save():
            written += 1

    print()
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  " + f)
    if not confirm:
        print("Dry run complete. Nothing written.")
        return 1 if failures else 0
    if failures:
        print("\nSome docs were refused. The rest were written.")
    print(f"wrote {written} files. Regenerating docs/markdown ...")
    subprocess.run([sys.executable,
                    os.path.join(os.path.dirname(JSON_DIR), "..", "scripts",
                                 "json_to_markdown.py")], check=False)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
