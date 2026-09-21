#!/usr/bin/env python3
"""Build article_section HTML from the Markdown that json_to_markdown.py emits.

This is the inverse of Converter, and only of Converter. It is not a general
Markdown engine and deliberately refuses anything outside the shapes that
Converter itself produces, because the correctness proof is a fixed point: take
the Markdown a human approved, build HTML from it, run Converter over that HTML,
and require the Markdown back exactly.

It is used on changed blocks only. Unchanged blocks keep their original nodes, so
heading ids, link targets, rel, image metadata and legacy RTE wrappers survive by
never being regenerated. Nothing here invents an id or a wrapper class.

CMS conventions this restores, none of which Markdown carries:
  inline code  -> <span class="code">, not <code>
  /docs/ link  -> target="_self"
  external     -> target="_blank" rel="noreferrer"
  callout      -> <p class="note"> for one block, <div class="note"> for several
"""

import re

from bs4 import BeautifulSoup, NavigableString, Tag

CALLOUT_CLASS = {
    "Note": "note",
    "Tip": "tip",
    "Warning": "warning",
    "Additional Resource": "add-resource",
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FENCE_RE = re.compile(r"^(`{3,})\s*$")
HR_RE = re.compile(r"^-{3,}$")
UL_RE = re.compile(r"^(\s*)-\s+(.*)$")
OL_RE = re.compile(r"^(\s*)(\d+)\.\s+(.*)$")
QUOTE_RE = re.compile(r"^>\s?(.*)$")
TABLE_DIVIDER_RE = re.compile(r"^\|(?:\s*:?-{3,}:?\s*\|)+$")
CELL_FENCE_RE = re.compile(r"^(`{3,}) (.*) \1$")
# Both label forms occur in the corpus, **Note:** and **Additional Resource**:, and
# the plural "Additional Resources" appears too. The class comes from the label's
# leading word, so an unknown label still fails loudly rather than guessing a class.
LABEL_RE = re.compile(r"^\*\*\s*([A-Za-z][A-Za-z ]*?)\s*:?\s*\*\*\s*:?")
LABEL_PREFIX = (
    ("additional resource", "add-resource"),
    ("note", "note"),
    ("tip", "tip"),
    ("warning", "warning"),
)

# Exactly the set Converter.escape_text escapes.
ESCAPED = set("\\`*[]<>")


class UnsupportedMarkdown(Exception):
    """Raised for a construct this builder will not guess at."""


# ---------- block splitting ----------


def split_blocks(md):
    """Split approved Markdown into the block strings Converter would have joined.

    Blank lines are the separator, except inside a fenced code block (samples may
    contain blank lines) and inside a loose list (items are separated by blank
    lines). Callouts never contain a bare blank line because indent_lines writes
    ">" on them.
    """
    lines = md.split("\n")
    blocks = []
    i = 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        fence = FENCE_RE.match(lines[i])
        if fence:
            start = i
            ticks = fence.group(1)
            i += 1
            while i < len(lines) and lines[i].strip() != ticks:
                i += 1
            if i >= len(lines):
                raise UnsupportedMarkdown(f"unterminated code fence at line {start + 1}")
            i += 1
            blocks.append("\n".join(lines[start:i]))
            continue
        if UL_RE.match(lines[i]) or OL_RE.match(lines[i]):
            start = i
            i = _consume_list(lines, i)
            blocks.append("\n".join(lines[start:i]).rstrip())
            continue
        if lines[i].startswith(">"):
            start = i
            while i < len(lines) and lines[i].startswith(">"):
                i += 1
            blocks.append("\n".join(lines[start:i]))
            continue
        start = i
        i += 1
        # A nested list hugs the text above it with no blank line between them
        # (render_list only inserts a separator for non-list blocks), so a list
        # marker ends the paragraph even though the line is not blank.
        while i < len(lines) and lines[i].strip():
            if UL_RE.match(lines[i]) or OL_RE.match(lines[i]):
                break
            i += 1
        blocks.append("\n".join(lines[start:i]))
    return _merge_trailing_breaks(blocks)


def _merge_trailing_breaks(blocks):
    """Rejoin paragraphs that a <br> before a newline split into two blocks.

    <p>a<br/>\\nb</p> converts to "a  \\n\\nb", which looks like two paragraphs. The
    trailing two spaces are the tell: Converter only emits them for a <br>, and a
    <br> at the very end of a paragraph is stripped, so a block ending in "  " was
    always mid-paragraph.
    """
    out = []
    for block in blocks:
        if (out and out[-1].endswith("  ") and block_kind(out[-1]) == "para"
                and block_kind(block) == "para"):
            out[-1] = out[-1] + "\n\n" + block
        else:
            out.append(block)
    return out


def _consume_list(lines, i):
    """Return the index just past a list starting at i, blank lines included."""
    while i < len(lines):
        if lines[i].strip():
            if (UL_RE.match(lines[i]) or OL_RE.match(lines[i])
                    or lines[i].startswith((" ", "\t"))):
                i += 1
                continue
            break
        # A blank line continues the list only if an item or continuation follows.
        j = i
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and (UL_RE.match(lines[j]) or OL_RE.match(lines[j])
                               or lines[j].startswith((" ", "\t"))):
            i = j
            continue
        break
    return i


def block_kind(md):
    first = md.split("\n", 1)[0]
    if FENCE_RE.match(first):
        return "code"
    if HEADING_RE.match(first):
        return "heading"
    if HR_RE.match(first.strip()):
        return "hr"
    if first.startswith(">"):
        return "quote"
    if UL_RE.match(first) or OL_RE.match(first):
        return "list"
    if first.startswith("|"):
        lines = md.split("\n")
        if len(lines) >= 2 and TABLE_DIVIDER_RE.match(lines[1].strip()):
            return "table"
    return "para"


SUPPORTED_KINDS = {"code", "heading", "hr", "quote", "list", "table", "para"}


# ---------- inline ----------


def link_attrs(href):
    """Link attributes by href shape, matching what the corpus uses for new links."""
    if href.startswith("#") or href.startswith("mailto:"):
        return {}
    if href.startswith("/"):
        return {"target": "_self"}
    if re.match(r"^https?://", href):
        return {"target": "_blank", "rel": "noreferrer"}
    return {}


def _unescape(text):
    out = []
    i = 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text) and text[i + 1] in ESCAPED:
            out.append(text[i + 1])
            i += 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def _find_unescaped(text, start, char):
    i = start
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == char:
            return i
        i += 1
    return -1


def _match_bracket(text, start):
    """Index of the ] closing the [ at start, honouring nesting and escapes."""
    depth = 0
    i = start
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _match_paren(text, start):
    depth = 0
    i = start
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def inline_to_nodes(md, soup):
    """Parse one block's inline Markdown into a list of nodes."""
    nodes = []
    buf = []

    def flush():
        if buf:
            nodes.append(NavigableString("".join(buf)))
            buf.clear()

    i = 0
    n = len(md)
    while i < n:
        ch = md[i]

        if ch == "\\" and i + 1 < n and md[i + 1] in ESCAPED:
            buf.append(md[i + 1])
            i += 2
            continue

        if ch == "`":
            run = len(md) - i - len(md[i:].lstrip("`"))
            close = md.find("`" * run, i + run)
            while close != -1 and close + run < n and md[close + run] == "`":
                close = md.find("`" * run, close + 1)
            if close != -1:
                raw = md[i + run:close]
                # code_span pads with one space when the text touches a backtick.
                if len(raw) >= 2 and raw.startswith(" ") and raw.endswith(" ") \
                        and (raw[1:-1].startswith("`") or raw[1:-1].endswith("`")):
                    raw = raw[1:-1]
                flush()
                span = soup.new_tag("span")
                span["class"] = ["code"]
                span.string = raw
                nodes.append(span)
                i = close + run
                continue

        if ch == "!" and i + 1 < n and md[i + 1] == "[":
            close = _match_bracket(md, i + 1)
            if close != -1 and close + 1 < n and md[close + 1] == "(":
                end = _match_paren(md, close + 1)
                if end != -1:
                    alt = _unescape(md[i + 2:close].replace("\\]", "]"))
                    src = md[close + 2:end].strip()
                    flush()
                    img = soup.new_tag("img")
                    img["src"] = src
                    img["alt"] = alt
                    nodes.append(img)
                    i = end + 1
                    continue

        if ch == "[":
            close = _match_bracket(md, i)
            if close != -1 and close + 1 < n and md[close + 1] == "(":
                end = _match_paren(md, close + 1)
                if end != -1:
                    href = md[close + 2:end].strip()
                    if href.startswith("<") and href.endswith(">"):
                        href = href[1:-1]
                    flush()
                    anchor = soup.new_tag("a")
                    anchor["href"] = href
                    for key, value in link_attrs(href).items():
                        anchor[key] = value
                    for child in inline_to_nodes(md[i + 1:close], soup):
                        anchor.append(child)
                    nodes.append(anchor)
                    i = end + 1
                    continue

        if md.startswith("***", i):
            close = md.find("***", i + 3)
            if close != -1:
                flush()
                strong = soup.new_tag("strong")
                em = soup.new_tag("em")
                for child in inline_to_nodes(md[i + 3:close], soup):
                    em.append(child)
                strong.append(em)
                nodes.append(strong)
                i = close + 3
                continue

        if md.startswith("**", i):
            close = md.find("**", i + 2)
            if close != -1:
                flush()
                strong = soup.new_tag("strong")
                for child in inline_to_nodes(md[i + 2:close], soup):
                    strong.append(child)
                nodes.append(strong)
                i = close + 2
                continue

        if ch == "*":
            close = _find_unescaped(md, i + 1, "*")
            if close != -1:
                flush()
                em = soup.new_tag("em")
                for child in inline_to_nodes(md[i + 1:close], soup):
                    em.append(child)
                nodes.append(em)
                i = close + 1
                continue

        if md.startswith("  \n", i):
            flush()
            nodes.append(soup.new_tag("br"))
            i += 3
            continue

        buf.append(ch)
        i += 1

    flush()
    return nodes


# ---------- blocks ----------


def _fill(tag, md, soup):
    for node in inline_to_nodes(md, soup):
        tag.append(node)
    return tag


def block_to_nodes(md, soup):
    """Build the nodes for one Markdown block."""
    kind = block_kind(md)
    if kind not in SUPPORTED_KINDS:
        raise UnsupportedMarkdown(f"unsupported block kind {kind!r}")

    if kind == "hr":
        return [soup.new_tag("hr")]

    if kind == "heading":
        match = HEADING_RE.match(md.split("\n", 1)[0])
        level = len(match.group(1))
        if level > 3:
            raise UnsupportedMarkdown(
                f"H{level} is not allowed in CLI docs (rule CLI-C1, no H4 or deeper)")
        return [_fill(soup.new_tag(f"h{level}"), match.group(2).strip(), soup)]

    if kind == "code":
        lines = md.split("\n")
        pre = soup.new_tag("pre")
        pre.string = "\n".join(lines[1:-1])
        return [pre]

    if kind == "table":
        return [_table_to_nodes(md, soup)]

    if kind == "list":
        return [_list_to_nodes(md, soup)]

    if kind == "quote":
        return [_callout_to_nodes(md, soup)]

    para = soup.new_tag("p")
    return [_fill(para, md, soup)]


def _split_row(line):
    """Split a table row on unescaped pipes, dropping the leading and trailing one."""
    cells = []
    cur = []
    i = 0
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|") and not inner.endswith("\\|"):
        inner = inner[:-1]
    while i < len(inner):
        if inner[i] == "\\" and i + 1 < len(inner) and inner[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if inner[i] == "|":
            cells.append("".join(cur).strip())
            cur = []
            i += 1
            continue
        cur.append(inner[i])
        i += 1
    cells.append("".join(cur).strip())
    return cells


def _table_to_nodes(md, soup):
    lines = [line for line in md.split("\n") if line.strip()]
    header = _split_row(lines[0])
    body = [_split_row(line) for line in lines[2:]]

    table = soup.new_tag("table")
    thead = soup.new_tag("thead")
    tr = soup.new_tag("tr")
    for cell in header:
        tr.append(_cell_to_node(cell, "th", soup))
    thead.append(tr)
    table.append(thead)

    tbody = soup.new_tag("tbody")
    for row in body:
        tr = soup.new_tag("tr")
        for cell in row:
            tr.append(_cell_to_node(cell, "td", soup))
        tbody.append(tr)
    table.append(tbody)
    return table


def _cell_to_node(text, name, soup):
    """A cell whose parts were joined with <br> becomes one paragraph per part.

    Converter.cell() joins the cell's *block* children with a literal <br>, and
    separately collapses any real <br> to a space. So a multi-part cell has to come
    back as several <p>, never as one paragraph with <br> in it.
    """
    cell = soup.new_tag(name)
    parts = re.split(r"<br\s*/?>", text)
    if len(parts) == 1 and not CELL_FENCE_RE.match(parts[0].strip()):
        for node in inline_to_nodes(parts[0], soup):
            cell.append(node)
        return cell
    for part in parts:
        part = part.strip()
        # cell() flattens a fenced code block's newlines to spaces, so a part that
        # still looks fenced was a <pre>, not an inline code span.
        fence = CELL_FENCE_RE.match(part)
        if fence:
            pre = soup.new_tag("pre")
            pre.string = fence.group(2)
            cell.append(pre)
            continue
        para = soup.new_tag("p")
        for node in inline_to_nodes(part, soup):
            para.append(node)
        cell.append(para)
    return cell


def _item_lines(lines):
    """Group raw list lines into (marker, [content lines]) per top-level item."""
    items = []
    current = None
    for line in lines:
        ul = UL_RE.match(line)
        ol = OL_RE.match(line)
        top = (ul and not ul.group(1)) or (ol and not ol.group(1))
        if top:
            if current is not None:
                items.append(current)
            marker = ul.group(2) if ul else ol.group(3)
            width = len(line) - len(line.lstrip()) + (2 if ul else len(ol.group(2)) + 2)
            current = {"first": marker, "rest": [], "pad": width}
        elif current is not None:
            current["rest"].append(line)
    if current is not None:
        items.append(current)
    return items


def _list_to_nodes(md, soup):
    lines = md.split("\n")
    first = lines[0]
    ordered = bool(OL_RE.match(first))
    tag = soup.new_tag("ol" if ordered else "ul")
    if ordered:
        start = int(OL_RE.match(first).group(2))
        if start != 1:
            tag["start"] = str(start)

    for item in _item_lines(lines):
        li = soup.new_tag("li")
        pad = item["pad"]
        dedented = [line[pad:] if len(line) > pad else line.strip()
                    for line in item["rest"]]
        body = "\n".join([item["first"]] + dedented).rstrip()
        sub_blocks = split_blocks(body)
        if len(sub_blocks) == 1 and block_kind(sub_blocks[0]) == "para":
            _fill(li, sub_blocks[0], soup)
        else:
            for sub in sub_blocks:
                for node in block_to_nodes(sub, soup):
                    li.append(node)
        tag.append(li)
    return tag


def _callout_to_nodes(md, soup):
    stripped = []
    for line in md.split("\n"):
        match = QUOTE_RE.match(line)
        stripped.append(match.group(1) if match else line)
    body = "\n".join(stripped).strip("\n")

    match = LABEL_RE.match(body)
    label = match.group(1).strip().lower() if match else ""
    css = next((c for prefix, c in LABEL_PREFIX if label.startswith(prefix)), None)
    if not css:
        found = f"**{match.group(1).strip()}**" if match else body.split("\n", 1)[0][:40]
        raise UnsupportedMarkdown(
            f"callout label {found} is not in the taxonomy. A blockquote must start "
            f"with **Note:**, **Tip:**, **Warning:** or **Additional Resource:** "
            f"(doc-standards callout-taxonomy). Fix the label in the Markdown rather "
            f"than guessing a CSS class here.")

    # The label stays in the body rather than being re-synthesized. 360 of the 371
    # callouts in the corpus carry the literal bold label, and Converter only adds
    # one when the body does not already start with bold, so keeping it verbatim is
    # both the majority shape and the one that round trips.
    sub_blocks = split_blocks(body)
    if len(sub_blocks) == 1 and block_kind(sub_blocks[0]) == "para":
        para = soup.new_tag("p")
        para["class"] = [css]
        return _fill(para, sub_blocks[0], soup)

    div = soup.new_tag("div")
    div["class"] = [css]
    for sub in sub_blocks:
        for node in block_to_nodes(sub, soup):
            div.append(node)
    return div


def build_fragment(md):
    """Build the HTML for a whole Markdown body. Used for new pages."""
    soup = BeautifulSoup("", "html.parser")
    out = []
    for block in split_blocks(md):
        out.extend(block_to_nodes(block, soup))
    return "".join(str(node) for node in out)
