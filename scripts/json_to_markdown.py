#!/usr/bin/env python3
"""Convert the JSON export in docs/json/ into Markdown in docs/markdown/.

Reads only from disk, no network. The body is always produced by converting the
article_section HTML. The md_content field is never read, even when populated.

Layout mirrors docs/json/index.json: each entry's "json" path maps to the same
relative path under docs/markdown/ with a .md extension.
"""

import html as html_mod
import json
import os
import re
import sys
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(ROOT, "docs", "json")
MD_DIR = os.path.join(ROOT, "docs", "markdown")
INDEX_PATH = os.path.join(JSON_DIR, "index.json")

CALLOUTS = {
    "note": "Note",
    "tip": "Tip",
    "warning": "Warning",
    "add-resource": "Additional Resource",
}
HEADINGS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}
BLOCK_TAGS = set(HEADINGS) | {"p", "div", "ul", "ol", "table", "pre", "hr", "blockquote"}

# Formatting tags that may legitimately appear inside <pre> and should be dropped,
# keeping their text. Anything else inside a <pre> is literal sample text.
PRE_INLINE = re.compile(r"</?\s*(strong|em|span|code|b|i|u)\b[^>]*>", re.I)
PRE_RE = re.compile(r"<pre\b[^>]*>(.*?)</pre>", re.S | re.I)


def indent_lines(text, prefix, first_prefix=None, blank=""):
    """Prefix every line, optionally using a different prefix for the first line.

    Blank lines inside a blockquote still need their marker, otherwise a multi-block
    callout is parsed as two separate blockquotes. Blank lines inside a list item must
    stay empty, so callers pass the marker they need via blank.
    """
    out = []
    for i, line in enumerate(text.split("\n")):
        pre = first_prefix if (i == 0 and first_prefix is not None) else prefix
        out.append((pre + line).rstrip() if line.strip() else blank)
    return "\n".join(out)


def code_span(text, keep_spacing=False):
    """Wrap text in the shortest backtick fence that survives its own backticks.

    Authors often put the word separator inside the code span as &nbsp;, so with
    keep_spacing the surrounding space is re-emitted outside the backticks instead
    of being stripped away and gluing the code to the next word.
    """
    text = text.replace("\xa0", " ")
    if not text.strip():
        return ""
    if keep_spacing:
        lead = " " if text[:1].isspace() else ""
        trail = " " if text[-1:].isspace() else ""
        return f"{lead}{code_span(text)}{trail}"
    text = text.strip()
    ticks = 1
    runs = re.findall(r"`+", text)
    if runs:
        ticks = max(len(run) for run in runs) + 1
    fence = "`" * ticks
    pad = " " if text.startswith("`") or text.endswith("`") else ""
    return f"{fence}{pad}{text}{pad}{fence}"


def emphasise(inner, marker):
    """Apply ** or * without swallowing the surrounding whitespace."""
    if not inner.strip():
        return inner
    lead = inner[: len(inner) - len(inner.lstrip())]
    trail = inner[len(inner.rstrip()):]
    return f"{lead}{marker}{inner.strip()}{marker}{trail}"


class Converter:
    def __init__(self):
        self.pres = []

    # ---------- entry point ----------

    def convert(self, raw_html):
        self.pres = []
        stashed = PRE_RE.sub(self._stash_pre, raw_html or "")
        soup = BeautifulSoup(stashed, "html.parser")
        blocks = self.render_blocks(soup)
        body = "\n\n".join(text for _, text in blocks if text.strip())
        return re.sub(r"\n{3,}", "\n\n", body).strip()

    def _stash_pre(self, match):
        """Pull code blocks out before parsing so no parser can eat their contents."""
        self.pres.append(match.group(1))
        return f'<pre data-cs-pre="{len(self.pres) - 1}"></pre>'

    def pre_text(self, index):
        raw = self.pres[index]
        raw = re.sub(r"<br\s*/?>", "\n", raw, flags=re.I)
        raw = re.sub(r"</?\s*wbr\s*/?>", "", raw, flags=re.I)
        raw = PRE_INLINE.sub("", raw)
        # Drop closing tags of anything else. The RTE auto-closes literal placeholders
        # such as <field>/<operator>/<value>, and those closers are not real content.
        raw = re.sub(r"</\s*[a-zA-Z][a-zA-Z0-9_:-]*\s*>", "", raw)
        text = html_mod.unescape(raw).replace("\xa0", " ")
        return text.strip("\n").rstrip()

    # ---------- block level ----------

    def render_blocks(self, node):
        """Return a list of (kind, text) blocks for a container's children."""
        blocks, buffer = [], []

        def flush():
            text = "".join(buffer).strip()
            buffer.clear()
            if text:
                blocks.append(("para", text))

        for child in node.children:
            if isinstance(child, NavigableString):
                buffer.append(self.escape_text(str(child)))
            elif isinstance(child, Tag) and child.name in BLOCK_TAGS:
                flush()
                blocks.extend(self.block(child))
            elif isinstance(child, Tag):
                buffer.append(self.inline(child))
        flush()
        return blocks

    def block(self, tag):
        name = tag.name
        classes = tag.get("class") or []

        if name == "pre":
            return [("code", self.fence(self.pre_text(int(tag["data-cs-pre"]))))]

        if name == "hr":
            return [("hr", "---")]

        if name in HEADINGS:
            text = self.inline(tag).strip()
            match = re.fullmatch(r"\*\*(.+)\*\*", text, re.S)
            if match:  # <h3><strong>Title</strong></h3> should not double up
                text = match.group(1).strip()
            return [("heading", f"{'#' * HEADINGS[name]} {text}")] if text else []

        if name in ("ul", "ol"):
            # ol.step-sec is a numbered step wrapper whose items hold real headings.
            # Unwrap it so those stay Markdown headings and keep their anchor slugs.
            if "step-sec" in classes:
                out = []
                for item in tag.find_all("li", recursive=False):
                    out.extend(self.render_blocks(item))
                return out
            return [self.render_list(tag)]

        if name == "table":
            return [("table", self.render_table(tag))]

        callout = next((CALLOUTS[c] for c in classes if c in CALLOUTS), None)
        if callout:
            return [("quote", self.render_callout(tag, callout))]

        if name == "div":  # cs-table-wrapper, cs-table and bare wrappers are transparent
            return self.render_blocks(tag)

        if name == "blockquote":
            inner = "\n\n".join(t for _, t in self.render_blocks(tag) if t.strip())
            return [("quote", indent_lines(inner, "> ", blank=">"))]

        text = self.inline(tag).strip()
        return [("para", text)] if text else []

    def fence(self, code):
        ticks = "```"
        while re.search(rf"^\s*{re.escape(ticks)}", code, re.M):
            ticks += "`"
        return f"{ticks}\n{code}\n{ticks}"

    def render_callout(self, tag, label):
        inner = [t for _, t in self.render_blocks(tag) if t.strip()]
        body = "\n\n".join(inner)
        # The source already carries its own bold label, so only add one when absent.
        if not body.lstrip().startswith("**"):
            body = f"**{label}:** {body}"
        return indent_lines(body, "> ", blank=">")

    def render_list(self, tag):
        ordered = tag.name == "ol"
        counter = int(tag.get("start") or 1)
        items, loose = [], False

        for item in tag.find_all("li", recursive=False):
            marker = f"{counter}. " if ordered else "- "
            counter += 1
            pad = " " * len(marker)
            blocks = [(k, t) for k, t in self.render_blocks(item) if t.strip()]
            if not blocks:
                continue
            if len(blocks) > 1:
                loose = True
            parts = []
            for i, (kind, text) in enumerate(blocks):
                if i == 0:
                    parts.append(indent_lines(text, pad, marker))
                else:
                    if kind != "list":  # nested lists hug the parent item
                        parts.append("")
                    parts.append(indent_lines(text, pad))
            items.append("\n".join(parts))

        return ("list", ("\n\n" if loose else "\n").join(items))

    def render_table(self, tag):
        rows = []
        for tr in tag.find_all("tr"):
            cells = tr.find_all(["th", "td"], recursive=False)
            if cells:
                rows.append([self.cell(c) for c in cells])
        if not rows:
            return ""
        header, body = rows[0], rows[1:]
        width = max(len(r) for r in rows)
        header += [""] * (width - len(header))

        lines = ["| " + " | ".join(header) + " |",
                 "| " + " | ".join(["---"] * width) + " |"]
        for row in body:
            row = row + [""] * (width - len(row))
            lines.append("| " + " | ".join(row) + " |")
        return "\n".join(lines)

    def cell(self, td):
        """Flatten a cell to one line. Block children are joined with <br>."""
        parts = []
        blocks = [t for _, t in self.render_blocks(td) if t.strip()]
        if blocks:
            parts = blocks
        else:
            inline = self.inline(td).strip()
            if inline:
                parts = [inline]
        text = "<br>".join(p.strip() for p in parts)
        text = re.sub(r"\s*\n+\s*", " ", text)
        return text.replace("|", "\\|").strip()

    # ---------- inline level ----------

    def escape_text(self, text):
        text = text.replace("\xa0", " ")
        return re.sub(r"([\\`*\[\]<>])", r"\\\1", text)

    def inline(self, node):
        if isinstance(node, NavigableString):
            return self.escape_text(str(node))
        if not isinstance(node, Tag):
            return ""

        name = node.name
        classes = node.get("class") or []

        if name == "pre":  # a stashed code block used inline, e.g. inside a table cell
            return code_span(re.sub(r"\s*\n\s*", " ", self.pre_text(int(node["data-cs-pre"]))))
        if name == "span" and "code" in classes:
            return code_span(node.get_text(), keep_spacing=True)
        if name in ("code", "kbd", "samp"):
            return code_span(node.get_text(), keep_spacing=True)
        if name == "br":
            return "  \n"
        if name == "wbr":
            return ""
        if name == "hr":
            return ""
        if name == "img":
            src = node.get("src") or ""
            alt = (node.get("alt") or "").replace("]", "\\]")
            return f"![{alt}]({src})" if src else ""
        if name == "a":
            return self.link(node)

        inner = "".join(self.inline(child) for child in node.children)
        if name in ("strong", "b"):
            return emphasise(inner, "**")
        if name in ("em", "i"):
            return emphasise(inner, "*")
        return inner

    def link(self, node):
        href = (node.get("href") or "").strip()
        raw = "".join(self.inline(child) for child in node.children)
        text = raw.strip()
        if not text:
            text = href
            if not text:
                return ""
        # Authors often leave the word separator inside the anchor text. Keep it, but
        # outside the brackets, so the link does not glue itself to the next word.
        lead = " " if raw[:1].isspace() else ""
        trail = " " if raw[-1:].isspace() and raw.strip() else ""
        if not href:
            return f"{lead}{text}{trail}"
        if re.search(r"[\s()]", href):
            href = f"<{href}>"
        return f"{lead}[{text}]({href}){trail}"


def front_matter(entry):
    seo = entry.get("seo") or {}
    fields = {
        "uid": entry.get("uid") or "",
        "seo_title": seo.get("title") or "",
        "seo_description": seo.get("description") or "",
    }
    lines = ["---"]
    for key, value in fields.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines)


def article_section(entry):
    for block in entry.get("article_content") or []:
        for key, value in block.items():
            if key == "article_section":
                return value or {}
    return {}


def main():
    converter = Converter()
    written = 0
    problems = []

    with open(INDEX_PATH, encoding="utf-8") as fh:
        index = json.load(fh)

    for record in index.get("entries", []):
        json_rel = record["json"]
        md_rel = record["markdown"]
        json_path = os.path.join(JSON_DIR, json_rel)
        md_path = os.path.join(MD_DIR, md_rel)

        with open(json_path, encoding="utf-8") as fh:
            entry = json.load(fh)

        section = article_section(entry)
        heading = (section.get("heading") or "").strip()
        if not heading:
            problems.append(f"{json_rel}: no article_section heading")

        body = converter.convert(section.get("content") or "")
        if not body:
            problems.append(f"{json_rel}: empty body")

        os.makedirs(os.path.dirname(md_path), exist_ok=True)
        document = f"{front_matter(entry)}\n\n# {heading}\n\n{body}\n"
        with open(md_path, "w", encoding="utf-8") as fh:
            fh.write(document)
        written += 1

    print(f"wrote {written} markdown files")
    for problem in problems:
        print(f"WARNING: {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
