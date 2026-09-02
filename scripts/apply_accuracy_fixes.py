#!/usr/bin/env python3
"""Fix the CLI doc accuracy findings: things the docs say that are not true.

Separate from apply_wave_a.py and apply_wave_c.py, which fix structure. A missing
Troubleshooting section is untidy. A flag that does not exist sends the reader to
a command that fails, so these are edits to what the docs assert.

Every edit is made to the HTML in docs/json/, never to docs/markdown/, which is
generated output. Run scripts/json_to_markdown.py afterwards.

Ground truth for flag facts is notes/reports/flag-inventory.json, generated from
the oclif.manifest.json inside each published npm tarball.

Usage:
  python3 scripts/apply_accuracy_fixes.py                # dry run
  python3 scripts/apply_accuracy_fixes.py --confirm      # write
  python3 scripts/apply_accuracy_fixes.py --only=wi1     # one work item
"""

import json
import os
import re
import sys

from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.docs_html import (JSON_DIR, Doc, body_rows, norm_text, table_header)


def code(soup, text):
    """The CMS inline-code element, which is <span class="code">, not <code>."""
    return BeautifulSoup(f'<span class="code">{text}</span>', "html.parser")


# --------------------------------------------------------------------------
# WI-1: cm:stacks:migration configuration flags
# --------------------------------------------------------------------------

MIGRATION_V2 = ("Version 2.x.x/Content Migration Commands V2/"
                "Migrate your Content using the CLI Migration Command | V2.x.x.json")

# What GA actually ships, from the 2.0.0 manifest:
#   --config        Path of the JSON configuration file
#   --inline-config Inline configuration, <key1>:<value1>
#   --config-file   does not exist
#
# V1 (1.12.7) had --config as the inline one and --config-file as the file path.
# The V2 doc inherited the V1 text, so its two rows carry the right descriptions
# under the wrong names. Renaming the rows fixes both in one move, and keeps the
# descriptions that were already correct.
MIGRATION_RENAMES = {"--config-file": "--config", "--config": "--inline-config"}


def wi1_migration_config(doc):
    edits = []
    flag_table = None
    for table in doc.tables():
        heads = table_header(table)
        if heads and heads[0] in ("flag", "flags"):
            flag_table = table
            break
    if flag_table is None:
        return ["WI-1: no flag table found, skipped"]

    # Rename in a single pass off a snapshot, so renaming --config-file to
    # --config cannot then be re-read as the --config row and renamed again.
    rows = []
    for tr in body_rows(flag_table):
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue
        rows.append((tr, cells, norm_text(cells[0].get_text())))

    for _tr, cells, name in rows:
        new = MIGRATION_RENAMES.get(name)
        if not new:
            continue
        cells[0].clear()
        cells[0].append(code(doc.soup, new))
        edits.append(f"WI-1: flag row {name} -> {new}")

    # The examples pass inline values to --config, which GA now reads as a file
    # path. That is the dangerous half: the command still parses.
    for pre in doc.soup.find_all("pre"):
        text = pre.get_text()
        if "--config " not in text or "cm:stacks:migration" not in text:
            continue
        pre.string = text.replace("--config ", "--inline-config ")
        edits.append("WI-1: example rewritten to --inline-config")

    # A reader upgrading from V1 has a working script that will now misbehave
    # rather than fail, so this is a Warning under C2's high-stakes bar.
    if not doc.soup.find("blockquote", string=re.compile("inline-config")):
        note = BeautifulSoup(
            '<blockquote><p><strong>Warning:</strong> The configuration flags '
            'changed in CLI 2.0.0. <span class="code">--config</span> now takes '
            'the path of a JSON configuration file, and inline configuration '
            'moved to the new <span class="code">--inline-config</span> flag. '
            'The <span class="code">--config-file</span> flag is removed. A '
            'script written for CLI 1.x that passes inline values to '
            '<span class="code">--config</span> will be read as a file path '
            'instead of failing, so update those calls to '
            '<span class="code">--inline-config</span>.</p></blockquote>',
            "html.parser")
        flag_table.insert_after(note)
        edits.append("WI-1: added a Warning callout about the breaking change")
    return edits


# --------------------------------------------------------------------------
# WI-2: GitHub links pinned to the v2.0.0-beta tag
# --------------------------------------------------------------------------

# The plugin packages moved out of contentstack/cli at GA. At the v2.0.0-beta tag
# that repo held all 19 packages, at v2.0.0 it holds five. So these paths 404 on
# both v2.0.0 and main in the old repo, and resolve only under the beta tag.
# Every rewritten URL below was confirmed 200 over HTTP before this ran.
BETA_LINK = re.compile(
    r"https://github\.com/contentstack/cli/(blob|tree)/v2\.0\.0-beta/")
BETA_LINK_NEW = r"https://github.com/contentstack/cli-plugins/\1/main/"


def wi2_beta_links(doc):
    edits = []
    for a in doc.soup.find_all("a", href=True):
        if not BETA_LINK.search(a["href"]):
            continue
        old = a["href"]
        a["href"] = BETA_LINK.sub(BETA_LINK_NEW, old)
        edits.append("WI-2: " + old.split("/v2.0.0-beta/")[-1])
    # The same URLs also appear as plain text in some code blocks and prose.
    for node in doc.soup.find_all(string=BETA_LINK):
        node.replace_with(BETA_LINK.sub(BETA_LINK_NEW, str(node)))
        edits.append("WI-2: rewrote a plain-text occurrence")
    return edits


# --------------------------------------------------------------------------
# WI-3: links into TypeScript source, pinned to a raw commit SHA
# --------------------------------------------------------------------------

CONFIG_REF = "Miscellaneous V2/Contentstack CLI Configuration Reference.json"
CONFIG_REF_V1 = "Miscellaneous/Contentstack CLI Configuration Reference.json"

SHA_LINK = re.compile(r"https://github\.com/contentstack/cli/blob/[0-9a-f]{40}/")


def wi3_source_links(doc):
    """Delete the five paragraphs whose only content is a link into source.

    C6: "Do not cite internal implementation details as justification for a
    claim: internal function or variable names, internal PR numbers or repo
    paths." A link to `entries.ts#L95` is exactly that, and pinning it to a
    commit SHA freezes it at one revision forever.

    Nothing is lost by deleting them, which was checked rather than assumed:

    - The two "Code Reference" paragraphs each follow a "Result:" line that
      already states the behaviour in full. The link only said which line of
      TypeScript implements it, which is not a fact a reader can act on.
    - The three "Default Configuration" paragraphs each sit directly above the
      section's own option tables, and those tables already carry a populated
      Default column with real values. The link pointed at a source file to
      supply defaults the page documents better a few lines further down.
    """
    edits = []
    for a in list(doc.soup.find_all("a", href=True)):
        if not SHA_LINK.search(a["href"]):
            continue
        holder = a.find_parent("p") or a.find_parent("li")
        label = norm_text(holder.get_text())[:58] if holder else norm_text(a.get_text())
        # Only remove the whole paragraph when the link is all it carries.
        if holder is not None and holder.find_all("a") == [a] and \
                norm_text(holder.get_text()).startswith(("Code Reference",
                                                         "Default Configuration")):
            holder.decompose()
            edits.append(f"WI-3: removed source-internal paragraph: {label}")
        else:
            a.unwrap()
            edits.append(f"WI-3: unwrapped source-internal link: {label}")
    return edits


# --------------------------------------------------------------------------
# WI-4: the Launch doc
# --------------------------------------------------------------------------

LAUNCH_V2 = "Version 2.x.x/CLI Commands V2/CLI for Launch | V2.x.x.json"


def wi4_launch(doc):
    edits = []
    # GA is 2.0.0. A beta version number is not a boundary a reader can act on.
    for node in doc.soup.find_all(string=re.compile(r"2\.0\.0-beta\.30")):
        node.replace_with(str(node).replace("2.0.0-beta.30", "2.0.0"))
        edits.append("WI-4: 2.0.0-beta.30 -> 2.0.0")
    # A V2 page should not send readers to the V1 install guide.
    for a in doc.soup.find_all("a", href=True):
        if a["href"].rstrip("/").endswith("/install-the-cli/v1"):
            a["href"] = a["href"].replace("/install-the-cli/v1", "/install-the-cli")
            edits.append("WI-4: install-the-cli/v1 -> install-the-cli")
    return edits


# --------------------------------------------------------------------------
# WI-5: label the console-log table with the command it belongs to
# --------------------------------------------------------------------------

IMPORT_V2 = "Version 2.x.x/CLI Commands V2/Import Content Using the CLI | V2.x.x.json"


def wi5_console_log_label(doc):
    """The table is correct. It just never says which command owns it.

    `--show-console-logs` belongs to `config:set:log`, not to `cm:stacks:import`.
    A reader scanning the import doc's tables reads it as an import flag, and so
    did the accuracy checker. Naming the command in the lead-in fixes both.
    """
    for table in doc.tables():
        heads = table_header(table)
        if heads[:2] != ["option", "description"]:
            continue
        names = {norm_text(c[0].get_text()) for c in
                 (tr.find_all(["td", "th"]) for tr in body_rows(table)) if c}
        if not any("show-console-logs" in n for n in names):
            continue
        lead = table.find_previous(["p", "strong"])
        if lead is not None and "config:set:log" in lead.get_text():
            return []
        label = BeautifulSoup(
            '<p><strong>Options for '
            '<span class="code">config:set:log</span>:</strong></p>',
            "html.parser")
        table.insert_before(label)
        return ["WI-5: labelled the console-log table as config:set:log options"]
    return []


# --------------------------------------------------------------------------
# WI-7: close the migration guide's Type Mapping Reference gaps
# --------------------------------------------------------------------------

MIGRATION_GUIDE = ("Version 2.x.x/Get Started with CLI V2/"
                   "Migrate from Contentstack CLI V1 to V2 | V2.x.x.json")

# Every long flag removed between the last 1.x and 2.0.0 that the guide does not
# already record, verified by diffing the published manifests of both versions.
# The guide already covers the other 16 removals correctly, so this closes the
# gap rather than rewriting the table.
#
# Format is (command, v1 flag, v1 short, v2 replacement note).
MISSING_ROWS = [
    ("cm:stacks:migration", "--config-file", None, "removed, use --config"),
    ("cm:stacks:audit", "--reference-only", None, "removed"),
    ("cm:stacks:audit:fix", "--reference-only", None, "removed"),
    ("cm:bootstrap", "--app-type", None, "removed"),
    ("cm:stacks:seed", "--fetch-limit", None, "removed"),
]


def _cell(soup, content):
    td = soup.new_tag("td")
    if content is None:
        td.append("None")
    elif content.startswith("--"):
        td.append(code(soup, content))
    else:
        td.append(content)
    return td


def _removed_cell(soup, note):
    """Matches the table's existing convention: italic parenthetical, code flag."""
    td = soup.new_tag("td")
    if "use --" in note:
        head, flag = note.split("use ", 1)
        em = soup.new_tag("em")
        em.append(f"({head}use ")
        td.append(em)
        td.append(code(soup, flag))
        em2 = soup.new_tag("em")
        em2.append(")")
        td.append(em2)
    else:
        em = soup.new_tag("em")
        em.append(f"({note})")
        td.append(em)
    return td


def wi7_migration_guide_rows(doc):
    heading = doc.find_heading("Type Mapping Reference", level=2)
    if heading is None:
        return ["WI-7: no Type Mapping Reference heading, skipped"]
    table = heading.find_next("table")
    if table is None:
        return ["WI-7: no table under Type Mapping Reference, skipped"]

    body = table.find("tbody") or table
    present = {norm_text(tr.get_text()) for tr in body_rows(table)}
    # Which command each row belongs to, since the command cell is filled only on
    # the first row of a group.
    last_command = {}
    current = None
    for tr in body_rows(table):
        cells = tr.find_all(["td", "th"])
        if cells and norm_text(cells[0].get_text()):
            current = norm_text(cells[0].get_text())
        if current:
            last_command[current] = tr

    edits = []
    for command, v1flag, v1short, note in MISSING_ROWS:
        if any(v1flag in row for row in present):
            continue
        tr = doc.soup.new_tag("tr")
        anchor = last_command.get(command)
        # A row joining an existing group leaves the command cell empty, which is
        # this table's convention for "same command as above".
        tr.append(_cell(doc.soup, "" if anchor is not None else command))
        tr.append(_cell(doc.soup, v1flag))
        tr.append(_cell(doc.soup, v1short))
        tr.append(_removed_cell(doc.soup, note))
        tr.append(_cell(doc.soup, None))
        if anchor is not None:
            anchor.insert_after(tr)
        else:
            body.append(tr)
        edits.append(f"WI-7: added {command} {v1flag} ({note})")

    # --config kept its name and changed its meaning, so a mapping row would read
    # as "no change". It belongs in prose, and it is the most dangerous item here
    # because a V1 script still parses.
    if "--inline-config" not in doc.soup.get_text():
        para = BeautifulSoup(
            '<p><strong>Behavior Change: '
            '<span class="code">cm:stacks:migration</span> configuration flags'
            '</strong> In V1, <span class="code">--config</span> took inline '
            'configuration and <span class="code">--config-file</span> took a '
            'file path. In V2, <span class="code">--config</span> takes the file '
            'path, inline configuration moved to the new '
            '<span class="code">--inline-config</span> flag, and '
            '<span class="code">--config-file</span> is removed. This is the one '
            'flag in the CLI that kept its name and changed its meaning, so a V1 '
            'script passing inline values to <span class="code">--config</span> '
            'is read as a file path rather than failing outright.</p>',
            "html.parser")
        table.insert_after(para)
        edits.append("WI-7: documented the --config meaning change in prose")
    return edits


# --------------------------------------------------------------------------
# Registry
# --------------------------------------------------------------------------

# (work item, path or None for every CLI doc, function)
ITEMS = [
    ("wi1", MIGRATION_V2, wi1_migration_config),
    ("wi2", None, wi2_beta_links),
    # Configuration Reference is one CMS entry shown in both version trees, so
    # both local files carry the same content and both need the same edit.
    ("wi3", "Version 2.x.x/" + CONFIG_REF, wi3_source_links),
    ("wi3", "Version 1.x.x/" + CONFIG_REF_V1, wi3_source_links),
    ("wi4", LAUNCH_V2, wi4_launch),
    ("wi5", IMPORT_V2, wi5_console_log_label),
    ("wi7", MIGRATION_GUIDE, wi7_migration_guide_rows),
]


def cli_paths():
    out = []
    for dirpath, _d, files in os.walk(JSON_DIR):
        for name in sorted(files):
            if not name.endswith(".json") or name == "index.json":
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, JSON_DIR)
            if rel.startswith(("Version 1", "Version 2")):
                out.append(path)
    return sorted(out)


def in_scope(path, shared):
    """V2 docs, plus V1 files that mirror a shared entry.

    A shared entry is one CMS entry shown in both version trees, so editing the
    V2 file edits the V1 view whether intended or not. Its V1 file has to receive
    the same edit or the two local mirrors of one entry drift apart.

    V1-only docs are out of scope. Two of them carry v2.0.0-beta GitHub links,
    which is a real defect, but retargeting a V1 page at V2 plugin code would
    make it worse rather than better. They need a 1.x target, which is a separate
    decision, and they are reported rather than edited.
    """
    rel = os.path.relpath(path, JSON_DIR)
    if not rel.startswith("Version 1"):
        return True
    with open(path, encoding="utf-8") as fh:
        return json.load(fh).get("uid") in shared


def shared_uids(paths):
    seen = {}
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            uid = json.load(fh).get("uid")
        rel = os.path.relpath(path, JSON_DIR)
        seen.setdefault(uid, set()).add(rel.split(os.sep)[0])
    return {uid for uid, trees in seen.items() if len(trees) > 1}


def main():
    confirm = "--confirm" in sys.argv
    only = None
    for arg in sys.argv[1:]:
        if arg.startswith("--only="):
            only = arg.split("=", 1)[1].lower()

    every = cli_paths()
    shared = shared_uids(every)
    skipped = []

    plan = {}
    for key, target, fn in ITEMS:
        if only and key != only:
            continue
        if target:
            plan.setdefault(os.path.join(JSON_DIR, target), []).append((key, fn))
            continue
        for path in every:
            if in_scope(path, shared):
                plan.setdefault(path, []).append((key, fn))
            else:
                skipped.append((key, os.path.relpath(path, JSON_DIR)))

    total = 0
    touched = 0
    for path in sorted(plan):
        if not os.path.exists(path):
            print(f"  MISSING {os.path.relpath(path, JSON_DIR)}")
            continue
        doc = Doc.load(path)
        edits = []
        for _key, fn in plan[path]:
            edits.extend(fn(doc))
        if not edits:
            continue
        touched += 1
        total += len(edits)
        print(f"\n{'PUSH' if confirm else 'DRY-RUN'}  {doc.rel}")
        for e in edits:
            print(f"    {e}")
        doc.save(dry_run=not confirm)

    # A V1-only doc that would have matched, reported so the defect is not lost.
    would_match = []
    for _key, rel in dict.fromkeys(skipped):
        path = os.path.join(JSON_DIR, rel)
        if BETA_LINK.search(json.dumps(Doc.load(path).entry)):
            would_match.append(rel)
    if would_match:
        print("\n" + "-" * 70)
        print("V1-only docs carrying v2.0.0-beta GitHub links, left unedited "
              "because a V1 page needs a 1.x target rather than the V2 one:")
        for rel in sorted(set(would_match)):
            print(f"    {rel}")

    print("\n" + "=" * 70)
    print(f"{total} edit(s) across {touched} doc(s)")
    if not confirm:
        print("Dry run. Nothing written. Re-run with --confirm.")
    else:
        print("Written to docs/json. Next: python3 scripts/json_to_markdown.py")


if __name__ == "__main__":
    main()
