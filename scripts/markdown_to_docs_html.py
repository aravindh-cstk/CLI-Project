#!/usr/bin/env python3
"""Splice approved Markdown back into the article_section HTML in docs/json/.

The docs pipeline runs one way: docs/json (the CMS HTML, source of truth) becomes
docs/markdown via json_to_markdown.py. This is the return leg, and it exists
because the linter and the human reviewer both work in Markdown while the CMS only
takes HTML.

It does NOT regenerate a page. Only 10 of the 93 CLI docs contain nothing that
Markdown cannot express: the rest carry heading ids (18 of which deliberately no
longer match their own text, with 324 in-page links depending on them), link
targets, rel, image asset metadata and legacy RTE wrappers. So the unit of work is
a block whose Markdown actually changed. Every other block keeps its original
nodes byte for byte, which is what makes those attributes survive.

Two checks gate every write, and either one failing aborts the whole run:

  fixed point   converting the new HTML back with json_to_markdown must reproduce
                the approved Markdown exactly. Markdown is what the human signed
                off on, so Markdown is what gets verified.
  blast radius  every block the diff called unchanged must serialize identically
                before and after.

Usage:
  python3 scripts/markdown_to_docs_html.py --selftest
  python3 scripts/markdown_to_docs_html.py <md-path> [<md-path> ...]
  python3 scripts/markdown_to_docs_html.py <md-path> --write
  python3 scripts/markdown_to_docs_html.py --all-changed [--write]
  python3 scripts/markdown_to_docs_html.py --new <md-path> --url <url>
      --template <sibling json, relative to docs/json> [--title ...] [--seo-title ...]

--new writes a local draft entry only. Creating it in Contentstack is a separate,
confirmed step: scripts/create_cli_page.py.
"""

import argparse
import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

import md_blocks  # noqa: E402
import md_to_html  # noqa: E402
from json_to_markdown import Converter, article_section  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(ROOT, "docs", "json")
MD_DIR = os.path.join(ROOT, "docs", "markdown")
INDEX_PATH = os.path.join(JSON_DIR, "index.json")
REPORT_PATH = os.path.join(ROOT, "notes", "reports", "md-splice.json")

# Fields the CMA assigns, dropped when cloning a sibling into a new draft.
DROP = ("uid", "_version", "ACL", "created_at", "created_by", "updated_at",
        "updated_by", "publish_details", "_in_progress")


class SpliceError(Exception):
    pass


# ---------- index and markdown file handling ----------


def load_index():
    with open(INDEX_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def records_by_md(index):
    out = {}
    for record in index.get("entries", []):
        out[os.path.normpath(record["markdown"])] = record
    return out


def split_front_matter(text):
    """Return (front matter dict, heading, body) for a generated markdown file."""
    lines = text.split("\n")
    meta = {}
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            key, _, value = lines[i].partition(":")
            try:
                meta[key.strip()] = json.loads(value.strip())
            except json.JSONDecodeError:
                meta[key.strip()] = value.strip()
            i += 1
        i += 1

    heading = None
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        match = re.match(r"^#\s+(.*)$", lines[i])
        if match:
            heading = match.group(1).strip()
            i += 1
        break

    body = "\n".join(lines[i:]).strip("\n")
    return meta, heading, body


def normalise_body(body):
    """The comparison form: Converter's own join and collapse rules."""
    return re.sub(r"\n{3,}", "\n\n", body).strip()


# ---------- the splice ----------


class Unit:
    """An emitting block plus the non-emitting blocks that precede it."""

    __slots__ = ("prefix", "block")

    def __init__(self, prefix, block):
        self.prefix = prefix
        self.block = block

    @property
    def prefix_html(self):
        return "".join(b.html for b in self.prefix)

    @property
    def html(self):
        return self.prefix_html + self.block.html


def to_units(blocks):
    """Split a block list into emitting units plus any trailing filler."""
    units = []
    prefix = []
    for block in blocks:
        if block.emits:
            units.append(Unit(prefix, block))
            prefix = []
        else:
            prefix.append(block)
    return units, prefix


class Group:
    """Units and Markdown blocks whose boundaries line up.

    The two sides do not always agree on where a block ends. One unit can produce
    several Markdown blocks (an ol.step-sec wrapper, a transparent div), and two
    units can produce one (two adjacent <ul> elements read back as a single list,
    since Markdown has no way to say "these are two lists"). Grouping up to the
    nearest shared boundary keeps the diff honest in both directions.
    """

    __slots__ = ("units", "blocks")

    def __init__(self, units, blocks):
        self.units = units
        self.blocks = blocks

    @property
    def html(self):
        return "".join(u.html for u in self.units)

    @property
    def prefix_html(self):
        return self.units[0].prefix_html if self.units else ""

    @property
    def simple(self):
        """One unit, one block: safe to rebuild from Markdown alone."""
        return len(self.units) == 1 and len(self.blocks) == 1


def to_groups(units):
    """Align unit boundaries with Markdown block boundaries."""
    body = md_blocks.join([u.block for u in units])
    blocks = md_to_html.split_blocks(body)

    unit_ends = []
    total = 0
    for index, unit in enumerate(units):
        total += len(unit.block.md)
        unit_ends.append(total)
        if index < len(units) - 1:
            total += 2  # the "\n\n" Converter joins blocks with

    block_ends = []
    cursor = 0
    for block in blocks:
        start = body.find(block, cursor)
        if start == -1:
            return [Group(units, blocks)]
        cursor = start + len(block)
        block_ends.append(cursor)

    groups = []
    i = j = 0
    while i < len(units) and j < len(blocks):
        start_i, start_j = i, j
        while True:
            if unit_ends[i] < block_ends[j]:
                i += 1
            elif unit_ends[i] > block_ends[j]:
                j += 1
            else:
                break
        groups.append(Group(units[start_i:i + 1], blocks[start_j:j + 1]))
        i += 1
        j += 1
    return groups


def _key(md):
    return re.sub(r"\s+", " ", md).strip()


def _build(md):
    try:
        return md_to_html.build_fragment(md)
    except md_to_html.UnsupportedMarkdown as exc:
        raise SpliceError(f"{exc}\n\nblock:\n{md[:400]}") from exc


def splice(html, approved_body):
    """Return (new_html, stats). Only changed blocks are rebuilt.

    The diff runs at Markdown-block granularity on both sides, because one HTML
    unit can expand to several Markdown blocks: an ol.step-sec wrapper turns its
    items into headings, and a wrapper div is transparent. Those units are atomic
    here. Their wrapper and its class cannot be recovered from Markdown, so an
    edit inside one is refused rather than silently flattened.
    """
    units, tail = to_units(md_blocks.split(html))
    groups = to_groups(units)

    owner = []
    old_md = []
    for index, group in enumerate(groups):
        for part in group.blocks:
            owner.append(index)
            old_md.append(part)

    new_md = md_to_html.split_blocks(approved_body)
    matcher = difflib.SequenceMatcher(
        None, [_key(m) for m in old_md], [_key(m) for m in new_md], autojunk=False)

    plan = [[] for _ in groups]
    insert_before = [[] for _ in range(len(groups) + 1)]
    dirty = set()

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for offset in range(i2 - i1):
                plan[owner[i1 + offset]].append(new_md[j1 + offset])
        elif tag == "insert":
            target = owner[i1] if i1 < len(owner) else len(groups)
            insert_before[target].extend(new_md[j1:j2])
        else:  # replace or delete
            for index in range(i1, i2):
                dirty.add(owner[index])
            if tag == "replace":
                plan[owner[i1]].extend(new_md[j1:j2])

    pieces = []
    touched = 0
    notes = []
    for index, group in enumerate(groups):
        for md in insert_before[index]:
            pieces.append(_build(md))
            touched += 1
        if index not in dirty:
            pieces.append(group.html)
            continue
        if len(group.blocks) > 1:
            raise SpliceError(
                f"this edit falls inside a <{group.units[0].block.kind}> wrapper that "
                f"Markdown cannot describe (an ol.step-sec or a wrapper div). "
                f"Rebuilding it would drop the wrapper and its class.\n\nEdit this "
                f"block's HTML directly in docs/json with scripts/lib/docs_html.py, "
                f"then regenerate the Markdown.\n\nblock starts:\n"
                f"{group.blocks[0][:300]}")
        if len(group.units) > 1:
            notes.append(f"{len(group.units)} adjacent elements were rebuilt as one, "
                         f"because the approved Markdown describes them as one block")
        if not plan[index]:
            continue
        pieces.append(group.prefix_html + "".join(_build(md) for md in plan[index]))
        touched += len(plan[index])

    for md in insert_before[len(groups)]:
        pieces.append(_build(md))
        touched += 1

    pieces.append("".join(b.html for b in tail))
    return "".join(pieces), {"blocks_total": len(groups), "blocks_touched": touched,
                             "notes": notes, "dirty": sorted(dirty),
                             "groups": groups}


def verify_fixed_point(new_html, approved_body):
    got = Converter().convert(new_html)
    want = normalise_body(approved_body)
    if got == want:
        return
    diff = "\n".join(difflib.unified_diff(
        want.split("\n"), got.split("\n"),
        fromfile="approved markdown", tofile="markdown regenerated from new HTML",
        lineterm="", n=2))
    raise SpliceError("fixed-point check failed, the HTML does not reproduce the "
                      "approved Markdown:\n" + diff)


def heading_warnings(old_html, new_html):
    """Report headings whose text changed, because their anchor id is now stale."""
    old = re.findall(r'<(h[123])([^>]*)>(.*?)</\1>', old_html, re.S)
    new = re.findall(r'<(h[123])([^>]*)>(.*?)</\1>', new_html, re.S)
    out = []
    for (tag_a, attrs_a, text_a), (tag_b, _, text_b) in zip(old, new):
        if text_a != text_b and 'id=' in attrs_a:
            out.append(f"heading text changed but its id was kept: "
                       f"{re.sub('<[^>]+>', '', text_a)!r} -> "
                       f"{re.sub('<[^>]+>', '', text_b)!r}")
    return out


# ---------- per-file driver ----------


def process(md_rel, record, write):
    json_path = os.path.join(JSON_DIR, record["json"])
    md_path = os.path.join(MD_DIR, md_rel)

    with open(json_path, encoding="utf-8") as fh:
        entry = json.load(fh)
    with open(md_path, encoding="utf-8") as fh:
        _, heading, body = split_front_matter(fh.read())

    section = article_section(entry)
    old_html = section.get("content") or ""

    new_html, stats = splice(old_html, body)
    verify_fixed_point(new_html, body)

    changed_html = new_html != old_html
    changed_heading = heading is not None and heading != (section.get("heading") or "")

    result = {
        "path": record["json"],
        "uid": record.get("uid"),
        "blocks_total": stats["blocks_total"],
        "blocks_touched": stats["blocks_touched"],
        "bytes_delta": len(new_html) - len(old_html),
        "heading_changed": changed_heading,
        "warnings": heading_warnings(old_html, new_html),
        "roundtrip": "pass",
        "written": False,
    }

    if write and (changed_html or changed_heading):
        section["content"] = new_html
        if changed_heading:
            section["heading"] = heading
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(entry, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        result["written"] = True

    return result


def report(results, write):
    print("LIVE RUN\n" if write else "DRY RUN, pass --write to update docs/json\n")
    for item in results:
        flag = "wrote " if item["written"] else "     "
        print(f"{flag} {item['blocks_touched']:3}/{item['blocks_total']:<3} blocks  "
              f"{item['bytes_delta']:+6} bytes  {item['path']}")
        if item["heading_changed"]:
            print("        heading changed")
        for warning in item["warnings"]:
            print(f"        WARNING: {warning}")
    touched = sum(i["blocks_touched"] for i in results)
    print(f"\n{len(results)} file(s), {touched} block(s) rebuilt, "
          f"every other block byte-identical")
    if touched and not write:
        print("Dry run complete. Nothing written.")


def write_report(results):
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# ---------- selftest ----------


def selftest():
    index = load_index()
    entries = index.get("entries", [])

    print("gate 0: every doc splits into blocks that reassemble to its Markdown")
    failures = []
    total_blocks = 0
    for record in entries:
        with open(os.path.join(JSON_DIR, record["json"]), encoding="utf-8") as fh:
            entry = json.load(fh)
        html = article_section(entry).get("content") or ""
        try:
            total_blocks += len(md_blocks.assert_reassembles(html))
        except AssertionError as exc:
            failures.append((record["json"], str(exc)))
    print(f"        {len(entries) - len(failures)}/{len(entries)} docs, "
          f"{total_blocks} blocks")
    for path, message in failures[:5]:
        print(f"        FAIL {path}: {message}")
    if failures:
        return 1

    print("\ngate 1: identity splice, generated Markdown must rebuild the same HTML")
    mismatches = []
    for record in entries:
        with open(os.path.join(JSON_DIR, record["json"]), encoding="utf-8") as fh:
            entry = json.load(fh)
        html = article_section(entry).get("content") or ""
        body = Converter().convert(html)
        try:
            new_html, _ = splice(html, body)
        except SpliceError as exc:
            mismatches.append((record["json"], str(exc).split("\n")[0]))
            continue
        if new_html != html:
            mismatches.append((record["json"], "HTML differs after an identity splice"))
    print(f"        {len(entries) - len(mismatches)}/{len(entries)} docs byte-identical")
    for path, message in mismatches[:5]:
        print(f"        FAIL {path}: {message}")
    if mismatches:
        return 1

    print("\ngate 2: block mutation matrix, every block must survive md -> HTML -> md")
    stats = {}
    refused = []
    for record in entries:
        with open(os.path.join(JSON_DIR, record["json"]), encoding="utf-8") as fh:
            entry = json.load(fh)
        html = article_section(entry).get("content") or ""
        for block in md_blocks.split(html):
            if not block.emits:
                continue
            kind = md_to_html.block_kind(block.md)
            bucket = stats.setdefault(kind, [0, 0])
            try:
                back = Converter().convert(md_to_html.build_fragment(block.md))
            except md_to_html.UnsupportedMarkdown as exc:
                bucket[1] += 1
                refused.append((record["json"], str(exc).split(".")[0]))
                continue
            if back == block.md:
                bucket[0] += 1
            else:
                bucket[1] += 1
                refused.append((record["json"], f"{kind} block does not round trip"))
    ok = sum(v[0] for v in stats.values())
    bad = sum(v[1] for v in stats.values())
    for kind in sorted(stats):
        good, fail = stats[kind]
        print(f"        {kind:8} {good:5} ok  {fail:3} refused")
    print(f"        {ok}/{ok + bad} blocks round trip")
    for path, message in refused[:5]:
        print(f"        refused in {path}: {message}")
    if refused:
        print("\n        Refused blocks keep their original HTML and are only a problem "
              "if someone edits them.")

    print("\ngate 3: word-edit fuzz, one edited block must touch only that block")
    return fuzz(entries)


def fuzz(entries, per_doc=6):
    """Edit one word in one block at a time and check the blast radius.

    The property under test is the one the whole design rests on: an edit to one
    block must rebuild that block and leave every other byte alone.
    """
    checked = failures = skipped = 0
    messages = []

    for record in entries:
        with open(os.path.join(JSON_DIR, record["json"]), encoding="utf-8") as fh:
            entry = json.load(fh)
        html = article_section(entry).get("content") or ""
        body = Converter().convert(html)
        blocks = md_to_html.split_blocks(body)

        seen_kinds = set()
        for index, block in enumerate(blocks):
            kind = md_to_html.block_kind(block)
            if kind in seen_kinds or kind == "hr":
                continue
            edited = _edit_one_word(block)
            if edited is None:
                continue
            seen_kinds.add(kind)
            if len(seen_kinds) > per_doc:
                break

            candidate = list(blocks)
            candidate[index] = edited
            try:
                new_html, stats = splice(html, "\n\n".join(candidate))
                verify_fixed_point(new_html, "\n\n".join(candidate))
            except SpliceError:
                skipped += 1  # a refused wrapper or callout, reported by gate 2
                continue

            checked += 1
            if stats["blocks_touched"] != 1:
                failures += 1
                messages.append(f"{record['json']}: a {kind} edit rebuilt "
                                f"{stats['blocks_touched']} blocks, expected 1")
                continue
            outside = _outside_unchanged(html, new_html, stats)
            if outside:
                failures += 1
                messages.append(f"{record['json']}: a {kind} edit changed the HTML "
                                f"{outside} the block it edited")

    print(f"        {checked - failures}/{checked} edits touched exactly one block "
          f"({skipped} skipped as already refused)")
    for message in messages[:5]:
        print(f"        FAIL {message}")
    return 1 if failures else 0


def _edit_one_word(block):
    """Rename the last plain word in a block, or None if it has none to rename."""
    for match in reversed(list(re.finditer(r"\b[a-z]{5,}\b", block))):
        start, end = match.span()
        line_start = block.rfind("\n", 0, start) + 1
        if block[line_start:start].count("`") % 2:
            continue  # inside a code span
        if block[line_start:line_start + 3] in ("```", "   "):
            continue  # inside a fenced block
        return block[:start] + match.group(0) + "ish" + block[end:]
    return None


def _outside_unchanged(old, new, stats):
    """Return "" when every byte outside the rebuilt block is identical.

    Rebuilding one block legitimately changes several byte ranges inside it, since
    the builder re-emits that block's HTML from scratch. What must never change is
    anything around it, which is the property that keeps heading ids and link
    targets safe on the rest of the page.
    """
    groups = stats["groups"]
    dirty = stats["dirty"]
    if len(dirty) != 1:
        return "in more than one block"
    index = dirty[0]
    start = sum(len(g.html) for g in groups[:index])
    end = start + len(groups[index].html)
    if old[:start] != new[:start]:
        return "before"
    if old[end:] != new[len(new) - (len(old) - end):]:
        return "after"
    return ""


# ---------- main ----------


def new_page(argv):
    """Write a local draft entry for a page that does not exist in the CMS yet.

    There is no prior HTML to protect, so the whole body is built at once. The
    skeleton is cloned from a sibling in the same version folder, which is how the
    breadcrumb, related_articles, next_and_prev_links and display flags end up
    matching the page's neighbours instead of being invented here.
    """
    parser = argparse.ArgumentParser(prog="markdown_to_docs_html.py --new")
    parser.add_argument("--new", required=True, help="the markdown file to build from")
    parser.add_argument("--url", required=True, help="e.g. /headless-cms/cli-foo")
    parser.add_argument("--template", required=True,
                        help="a sibling entry, relative to docs/json")
    parser.add_argument("--title", help="defaults to the CLI title convention")
    parser.add_argument("--seo-title", help="defaults to '<heading> | Contentstack'")
    parser.add_argument("--out", help="where to write the draft, default docs/json/drafts")
    args, _ = parser.parse_known_args(argv)

    with open(args.new, encoding="utf-8") as fh:
        _, heading, body = split_front_matter(fh.read())
    if not heading:
        sys.exit(f"{args.new} has no '# Heading' line. "
                 f"It becomes article_section.heading and cannot be guessed.")

    content = _build_whole(body)
    verify_fixed_point(content, body)

    template_path = os.path.join(JSON_DIR, args.template)
    if not os.path.exists(template_path):
        sys.exit(f"template {args.template} not found under docs/json")
    with open(template_path, encoding="utf-8") as fh:
        entry = json.load(fh)

    for field in DROP:
        entry.pop(field, None)
    entry["url"] = args.url
    entry["title"] = args.title or (
        f"[Contentstack Command-line Interface (CLI)] - {heading}")
    entry["seo"] = dict(entry.get("seo") or {})
    entry["seo"]["title"] = args.seo_title or f"{heading} | Contentstack"
    entry["md_content"] = ""

    section = article_section(entry)
    section.pop("_metadata", None)  # Contentstack assigns the modular block uid
    section["heading"] = heading
    section["content"] = content

    out = args.out or os.path.join(JSON_DIR, "drafts",
                                   os.path.basename(args.new).replace(".md", ".json"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(entry, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"draft      {os.path.relpath(out, ROOT)}")
    print(f"url        {entry['url']}")
    print(f"title      {entry['title']}")
    print(f"seo.title  {entry['seo']['title']}")
    print(f"heading    {heading}")
    print(f"content    {len(content)} chars, "
          f"{len(md_to_html.split_blocks(body))} blocks, fixed point verified")
    print(f"skeleton   cloned from {args.template}")
    print("\nNothing was created in Contentstack. Next, after review:")
    print(f"  python3 scripts/create_cli_page.py {os.path.relpath(out, ROOT)!r}")
    return 0


def _build_whole(body):
    try:
        return md_to_html.build_fragment(body)
    except md_to_html.UnsupportedMarkdown as exc:
        sys.exit(f"cannot build this page: {exc}")


def main(argv):
    write = "--write" in argv
    args = [a for a in argv if not a.startswith("--")]

    if "--selftest" in argv:
        return selftest()

    if "--new" in argv:
        return new_page(argv)

    index = load_index()
    by_md = records_by_md(index)

    if "--all-changed" in argv:
        targets = []
        for md_rel, record in by_md.items():
            md_path = os.path.join(MD_DIR, md_rel)
            json_path = os.path.join(JSON_DIR, record["json"])
            if os.path.exists(md_path) and os.path.getmtime(md_path) > \
                    os.path.getmtime(json_path):
                targets.append(md_rel)
    else:
        targets = []
        for arg in args:
            path = os.path.abspath(arg)
            rel = os.path.normpath(os.path.relpath(path, MD_DIR))
            if rel not in by_md:
                sys.exit(f"{arg} is not a tracked CLI doc. "
                         f"docs/json/index.json has no entry whose markdown is {rel!r}.")
            targets.append(rel)

    if not targets:
        print("Nothing to do.")
        return 0

    # A uid living under two version folders would silently lose one copy's edits.
    seen = {}
    for rel in targets:
        uid = by_md[rel].get("uid")
        if uid in seen:
            sys.exit(f"{rel} and {seen[uid]} are the same CMS entry ({uid}). "
                     f"Edit one and let the other be regenerated.")
        seen[uid] = rel

    results = []
    for rel in targets:
        try:
            results.append(process(rel, by_md[rel], write))
        except SpliceError as exc:
            print(f"ABORT {rel}\n\n{exc}\n", file=sys.stderr)
            print("Nothing was written. Fix the block by hand in docs/json with "
                  "scripts/lib/docs_html.py, regenerate the Markdown, and re-run.",
                  file=sys.stderr)
            return 1

    report(results, write)
    if write:
        write_report(results)
        print(f"\nwrote {os.path.relpath(REPORT_PATH, ROOT)}")
        print("Next: python3 scripts/push_all_wave_changes.py")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
