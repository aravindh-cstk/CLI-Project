#!/usr/bin/env python3
"""Wave C: convert flag tables to CLI-C2's six-column shape.

  | Flag | Type | Required | Default | Description | Notes |

Where a flag has a short form, both forms go in the Flag cell, long form first,
which is how the CLI's own --help presents them.

Values for columns a table does not already have come from
notes/reports/flag-inventory.json, which is generated from the oclif.manifest.json
inside each published npm tarball. That matters: the local repo sits on branch
v2-dev with no v2.0.0 tag, and its flag data disagrees with what GA actually
ships. Run scripts/gen_flag_inventory.py first.

A cell is left empty rather than guessed. An empty Notes cell says "no caveats".
A guessed one says something untrue.

Config-key tables are exempt. In Contentstack CLI Configuration Reference,
`Option` names a config-file key rather than a CLI flag, so renaming the column to
Flag would make the page wrong. Those tables keep their own shape.

Usage:
  python3 scripts/apply_wave_c.py                  # dry run
  python3 scripts/apply_wave_c.py --confirm        # write
  python3 scripts/apply_wave_c.py --only <substr>
  python3 scripts/apply_wave_c.py --report         # coverage, no edits
"""

import collections
import json
import os
import re
import sys

from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.docs_html import (Doc, body_rows, cli_json_paths, norm_text,
                           reshape_table, table_header)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY = os.path.join(ROOT, "notes", "reports", "flag-inventory.json")

TARGET = ["Flag", "Type", "Required", "Default", "Description", "Notes"]

# A table is a flag table when its first column names flags and another column
# describes them. Both spellings of the first column are in use.
FIRST_COL = {"flag", "flags", "option", "options"}

# Docs where `Option` means a config-file key, not a CLI flag. CLI-C2 does not
# apply, and forcing it would rename a correct column to a wrong one.
CONFIG_KEY_DOCS = ("Contentstack CLI Configuration Reference",)

# Existing column names that supply a target column under a different label.
RENAME = {
    "option": "Flag",
    "options": "Flag",
    "flags": "Flag",
    "flag": "Flag",
    "short": "_short",
    "short flag": "_short",
    "type": "Type",
    "required": "Required",
    "default": "Default",
    "description": "Description",
    "notes": "Notes",
    "note": "Notes",
    "example": "_example",
}


def load_inventory():
    if not os.path.exists(INVENTORY):
        sys.exit("notes/reports/flag-inventory.json missing. "
                 "Run: python3 scripts/gen_flag_inventory.py")
    data = json.load(open(INVENTORY, encoding="utf-8"))
    # Fallback lookup, by flag name across every command, for tables that cannot
    # be tied to one command. The key is only the three columns being filled.
    # Including the short form here would be wrong: --alias carries -a on some
    # commands and no short form on others, which is a real difference but not one
    # that changes its Type, Required or Default.
    by_name = collections.defaultdict(set)
    for cid, cmd in data["commands"].items():
        for name, flag in cmd["flags"].items():
            by_name[name].add((flag["type"], flag["required"], flag["default"]))
    return data, by_name


def flag_name(cell_text):
    """The long flag name from a Flag cell, without dashes or backticks."""
    text = norm_text(cell_text).replace("`", "")
    m = re.search(r"--([A-Za-z][\w-]*)", text)
    if m:
        return m.group(1)
    m = re.match(r"-([A-Za-z])\b", text)
    return None if m else (text.split()[0] if text else None)


def consistent(entries):
    """The single agreed value set for a flag name, or None if commands disagree."""
    if entries and len(entries) == 1:
        return next(iter(entries))
    return None


COMMAND_HEADING = re.compile(r"^`?(?:csdx\s+)?([a-z][a-z0-9-]*(?::[a-z][a-z0-9-]*)+)`?$")


def owning_command(_doc, table, inventory):
    """The command id from the nearest preceding heading, if it names a real one.

    Scoping a lookup to one command is strictly better than searching every
    command by flag name, because it resolves the cases where the same flag name
    genuinely differs. Returns None when no heading above the table names a
    command the inventory knows.
    """
    for node in table.find_all_previous(["h2", "h3"]):
        m = COMMAND_HEADING.match(norm_text(node.get_text()))
        if m and m.group(1) in inventory:
            return m.group(1)
    return None


def is_flag_table(table):
    """A table this wave may reshape.

    The description column has to be named exactly `description`, not merely
    contain the word. The V1-to-V2 migration guide has a table headed
    `Flag | V1 description (incorrect) | V2 description (correct)` whose two
    columns are a before-and-after comparison rather than one description. A
    substring match claimed it as a flag table and the reshape dropped both
    columns, destroying the content. It is not a CLI-C2 table and is left alone.
    """
    heads = table_header(table)
    if len(heads) < 2:
        return False
    if heads[0] not in FIRST_COL:
        return False
    return any(h in ("description", "descriptions") for h in heads)


def resolvable(table, by_name, inventory):
    """(ok, unresolved_flag_names) without mutating the table.

    A table is only converted when every column it is missing can be sourced for
    every row. Converting a table half way would put empty Type and Required
    cells into a published page, and an empty Required cell reads as "not
    required" rather than as "nobody checked". 13 of the CLI's 159 flag names
    genuinely differ between commands, `--alias` and `--stack-api-key` among
    them, so a by-name lookup cannot answer for those and should not pretend to.
    """
    heads = table_header(table)
    canon = [RENAME.get(h, h) for h in heads]
    needed = [c for c in ("Type", "Required", "Default") if c not in canon]
    if not needed:
        return True, []

    cid = owning_command(None, table, inventory)
    scoped = inventory.get(cid, {}).get("flags", {}) if cid else {}
    fi = canon.index("Flag") if "Flag" in canon else 0

    unresolved = []
    for tr in body_rows(table):
        cells = tr.find_all(["td", "th"])
        if fi >= len(cells):
            continue
        name = flag_name(cells[fi].get_text())
        if not name:
            unresolved.append("(unreadable flag cell)")
            continue
        if name in scoped:
            continue
        if consistent(by_name.get(name)) is None:
            unresolved.append(name)
    return not unresolved, sorted(set(unresolved))


def convert(doc, table, by_name, stats, inventory=None):
    inventory = inventory or {}
    cid = owning_command(None, table, inventory)
    scoped = inventory.get(cid, {}).get("flags", {}) if cid else {}
    stats["table scoped to a command" if cid else "table not tied to a command"] += 1
    heads = table_header(table)
    canon = [RENAME.get(h, h) for h in heads]

    # Fold an existing Short column into the Flag cell before reshaping, so the
    # data is preserved rather than dropped with the column.
    if "_short" in canon:
        si, fi = canon.index("_short"), canon.index("Flag")
        for tr in body_rows(table):
            cells = tr.find_all(["td", "th"])
            if max(si, fi) >= len(cells):
                continue
            short = norm_text(cells[si].get_text()).replace("`", "")
            if short and short not in ("-", "None", "N/A", "NA"):
                if not short.startswith("-"):
                    short = f"-{short}"
                if norm_text(cells[fi].get_text()):
                    # Build a real inline-code element. Appending "`-k`" as text
                    # would put literal backticks into the HTML, which the
                    # markdown converter then escapes as \`-k\`.
                    soup = cells[fi].find_parent("table")
                    cells[fi].append(", ")
                    code = BeautifulSoup(
                        f'<span class="code">{short}</span>', "html.parser")
                    cells[fi].append(code)
        stats["short folded"] += 1

    # An Example column holds real content, unlike a Short column whose empty
    # rows say "None". Dropping it would lose usage examples such as
    # `--folder-uid cs_root`, so it is folded into Notes, which is where a
    # per-flag usage hint belongs under CLI-C2.
    if "_example" in canon and "Notes" not in canon:
        ei = canon.index("_example")
        for tr in body_rows(table):
            cells = tr.find_all(["td", "th"])
            if ei >= len(cells):
                continue
            example = norm_text(cells[ei].get_text())
            if example and example not in ("-", "None", "N/A", "NA"):
                cells[ei].insert(0, "Example: ")
        canon[ei] = "Notes"
        rename_local = dict(RENAME)
        rename_local[heads[ei]] = "Notes"
        stats["example folded into Notes"] += 1
    else:
        rename_local = RENAME

    filled = collections.Counter()

    def filler(column):
        def fn(row):
            # `row` is a text snapshot of the original row, keyed by column name.
            name = flag_name(row.get("Flag") or "")
            if not name:
                stats["row with no readable flag name"] += 1
                return None
            # Prefer the owning command's own flag, which is exact. Fall back to
            # the by-name lookup only when the table is not tied to a command.
            if name in scoped:
                flag = scoped[name]
                values = (flag["type"], flag["required"], flag["default"])
                filled[f"{column} (exact)"] += 1
            else:
                values = consistent(by_name.get(name))
                if values is None:
                    filled["left empty, no inventory match" if name not in by_name
                           else "left empty, commands disagree"] += 1
                    return None
                filled[f"{column} (by name)"] += 1
            vtype, required, default = values
            return {"Type": vtype, "Required": required, "Default": default}[column]
        return fn

    fill = {c: filler(c) for c in ("Type", "Required", "Default")}
    note = reshape_table(table, TARGET, rename=rename_local, fill=fill)
    for key, n in filled.items():
        stats[f"filled {key}"] += n
    return note


def main():
    confirm = "--confirm" in sys.argv
    report_only = "--report" in sys.argv
    only = None
    for arg in sys.argv[1:]:
        if arg.startswith("--only="):
            only = arg.split("=", 1)[1]

    data, by_name = load_inventory()
    print(f"inventory: {len(data['commands'])} commands, "
          f"{sum(len(c['flags']) for c in data['commands'].values())} flags "
          f"from published GA manifests\n")

    paths = cli_json_paths()
    if only:
        paths = [p for p in paths if only.lower() in p.lower()]

    stats = collections.Counter()
    converted = exempt = already = deferred = 0
    deferred_rows = []
    touched_docs = 0

    for path in paths:
        doc = Doc.load(path)
        is_config_doc = any(d in doc.rel for d in CONFIG_KEY_DOCS)
        notes = []
        for table in doc.tables():
            if not is_flag_table(table):
                continue
            heads = table_header(table)
            if len(heads) == 2:
                already += 1  # C9's two-column exception
                continue
            if is_config_doc:
                exempt += 1
                continue
            if [h.lower() for h in heads] == [t.lower() for t in TARGET]:
                already += 1
                continue
            ok, unresolved = resolvable(table, by_name, data["commands"])
            if not ok:
                deferred += 1
                deferred_rows.append((doc.rel, " | ".join(heads), unresolved))
                continue
            notes.append(convert(doc, table, by_name, stats, data["commands"]))
            converted += 1

        if not notes:
            continue
        touched_docs += 1
        if not report_only:
            print(f"{'PUSH' if confirm else 'DRY-RUN'}  {doc.rel}")
            for n in notes:
                print(f"    {n}")
            doc.save(dry_run=not confirm)

    print("\n" + "=" * 68)
    print(f"tables converted        {converted}   across {touched_docs} docs")
    print(f"tables already correct  {already}")
    print(f"tables exempt           {exempt}   (config-key tables)")
    print(f"tables deferred         {deferred}   (cannot be fully sourced)")
    if deferred_rows:
        print("\ndeferred tables, with the flags no source can settle:")
        for rel, heads, un in deferred_rows:
            print(f"  {rel}")
            print(f"      [{heads}]  ->  {', '.join('--' + u if not u.startswith('(') else u for u in un)}")
    print("\ncell fills from the GA inventory:")
    for key, n in sorted(stats.items()):
        print(f"  {key:28s} {n}")
    if report_only:
        print("\nReport only. Nothing written.")
    elif not confirm:
        print("\nDry run. Nothing written. Re-run with --confirm to apply.")
    else:
        print("\nWritten to docs/json. Next: python3 scripts/json_to_markdown.py")


if __name__ == "__main__":
    main()
