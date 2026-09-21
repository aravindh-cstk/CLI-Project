#!/usr/bin/env python3
"""Split an article_section HTML string into provenance-mapped blocks.

Each block records both the Markdown that json_to_markdown.py produces for it and
the original top-level HTML nodes that produced it. That mapping is what lets the
markdown -> HTML direction rebuild only the blocks whose Markdown actually changed
and leave every other block's HTML byte-identical, which is the only way heading
ids, link targets and image metadata survive a round trip.

The grouping mirrors Converter.render_blocks exactly: a child in BLOCK_TAGS is its
own block, and a run of consecutive inline children (text nodes, <strong>, <br>,
bare <a> and so on) is buffered and flushed as a single paragraph. Getting that
buffer rule wrong is the difference between 91 and 93 of the 93 CLI docs
reassembling, so assert_reassembles() is the gate every caller should run.

Markdown for a block is produced by running the real Converter over that block's
serialized nodes rather than by reimplementing any of it. The Converter is the
ground truth and must never be forked.
"""

import os
import re
import sys
from html.parser import HTMLParser

from bs4 import BeautifulSoup, NavigableString, Tag

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from json_to_markdown import BLOCK_TAGS, Converter  # noqa: E402


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}


class _TopLevelSpans(HTMLParser):
    """Character spans of the top-level elements, taken from the source text.

    Re-serializing a bs4 node is not byte-safe: it rewrites <br /> to <br/>, turns
    &nbsp; into a literal character and reorders attributes, which showed up in 22
    of the 93 CLI docs. Unchanged blocks therefore have to be sliced out of the
    original string, so their exact bytes survive.
    """

    def __init__(self, html):
        super().__init__(convert_charrefs=False)
        self.html = html
        self.spans = []
        self.depth = 0
        self.start = None
        self._line_offsets = [0]
        for line in html.split("\n")[:-1]:
            self._line_offsets.append(self._line_offsets[-1] + len(line) + 1)

    def _offset(self):
        line, column = self.getpos()
        return self._line_offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            if self.depth == 0:
                start = self._offset()
                self.spans.append((start, start + len(self.get_starttag_text() or "")))
            return
        if self.depth == 0:
            self.start = self._offset()
        self.depth += 1

    def handle_startendtag(self, tag, attrs):
        if self.depth == 0:
            start = self._offset()
            self.spans.append((start, start + len(self.get_starttag_text() or "")))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.depth == 0:
            return
        self.depth -= 1
        if self.depth == 0 and self.start is not None:
            close = self.html.find(">", self._offset())
            end = close + 1 if close != -1 else len(self.html)
            self.spans.append((self.start, end))
            self.start = None


def _tag_spans(html):
    parser = _TopLevelSpans(html)
    parser.feed(html)
    parser.close()
    return parser.spans


def _slice_children(soup, html):
    """Map each top-level child to its exact slice of the original HTML."""
    spans = _tag_spans(html)
    children = list(soup.children)
    slices = []
    cursor = 0
    index = 0
    for child in children:
        if isinstance(child, Tag):
            if index >= len(spans):
                return None
            start, end = spans[index]
            index += 1
            if start < cursor:
                return None
            slices.append(html[cursor:end])
            cursor = end
        else:
            nxt = spans[index][0] if index < len(spans) else len(html)
            if nxt < cursor:
                return None
            slices.append(html[cursor:nxt])
            cursor = nxt
    if cursor != len(html) and slices:
        slices[-1] += html[cursor:]
    if "".join(slices) != html:
        return None
    return dict(zip((id(c) for c in children), slices))


class Block:
    """One top-level unit of an article_section, in both representations.

    md may be empty: a whitespace-only text node between two block tags produces no
    Markdown but still has to be carried so the HTML can be reassembled unchanged.
    """

    __slots__ = ("kind", "md", "nodes", "index", "_html")

    def __init__(self, kind, md, nodes, index, html=None):
        self.kind = kind
        self.md = md
        self.nodes = nodes
        self.index = index
        self._html = html

    @property
    def html(self):
        if self._html is not None:
            return self._html
        return "".join(str(node) for node in self.nodes)

    @property
    def emits(self):
        return bool(self.md.strip())

    def __repr__(self):
        head = self.md.split("\n", 1)[0][:60]
        return f"<Block {self.index} {self.kind} {head!r}>"


def _kind_of(nodes):
    """Label a block for reporting. The splice does not branch on this."""
    if len(nodes) == 1 and isinstance(nodes[0], Tag):
        name = nodes[0].name
        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            return "heading"
        if name in ("ul", "ol"):
            return "list"
        if name in ("table", "pre", "hr", "blockquote", "div", "p"):
            return name
    return "inline-run"


def _to_markdown(html):
    return Converter().convert(html)


def split(html):
    """Return the Block list for an article_section content string.

    Nodes are taken from a soup parsed from the original HTML, not from the
    pre-stashed soup Converter.convert builds internally, so block.html gives back
    the real <pre> contents rather than a placeholder.
    """
    html = html or ""
    soup = BeautifulSoup(html, "html.parser")
    source = _slice_children(soup, html)
    blocks = []
    buffer = []

    def raw(nodes):
        if source is None:
            return None
        return "".join(source[id(n)] for n in nodes)

    def flush():
        if not buffer:
            return
        nodes = list(buffer)
        buffer.clear()
        blocks.append(Block(_kind_of(nodes), _to_markdown("".join(str(n) for n in nodes)),
                            nodes, len(blocks), raw(nodes)))

    for child in soup.children:
        if isinstance(child, Tag) and child.name in BLOCK_TAGS:
            flush()
            blocks.append(Block(_kind_of([child]), _to_markdown(str(child)), [child],
                                len(blocks), raw([child])))
        else:
            buffer.append(child)
    flush()
    return blocks


def join(blocks):
    """Reassemble the Markdown body the way Converter.convert joins its blocks."""
    body = "\n\n".join(b.md for b in blocks if b.emits)
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def assert_reassembles(html):
    """Raise unless the split reproduces Converter().convert(html) exactly."""
    blocks = split(html)
    got = join(blocks)
    want = Converter().convert(html or "")
    if got != want:
        raise AssertionError(_first_difference(got, want))
    return blocks


def _first_difference(got, want):
    got_lines = got.split("\n")
    want_lines = want.split("\n")
    for i in range(max(len(got_lines), len(want_lines))):
        a = got_lines[i] if i < len(got_lines) else "<missing>"
        b = want_lines[i] if i < len(want_lines) else "<missing>"
        if a != b:
            return (f"reassembly differs at line {i + 1}\n"
                    f"  split:     {a!r}\n"
                    f"  converter: {b!r}")
    return "reassembly differs (no line-level difference found)"
