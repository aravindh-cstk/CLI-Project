"""Edit helpers for the HTML stored in docs_article entries.

Why this exists. docs/markdown/ is generated output: json_to_markdown.py converts
docs/json/ to docs/markdown/ one way, and rebuild_cli_docs_tree.py deletes and
rewrites both trees from the live CMS. An edit made to a .md file is destroyed on
the next rebuild and never reaches Contentstack. So every content edit has to be
made to the HTML string at article_content[0].article_section.content inside the
docs/json/ file, which is what this module operates on.

The stored HTML is well behaved, which makes this tractable: headings are plain
h2/h3/h4 with no attributes, inline code is <span class="code">, and tables carry
a full thead and tbody. BeautifulSoup is already a dependency of
json_to_markdown.py, so nothing new is introduced here.

Nothing in this module touches the network. Writes go to local JSON only.
"""

import json
import os
import re

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_DIR = os.path.join(ROOT, "docs", "json")
MD_DIR = os.path.join(ROOT, "docs", "markdown")
INDEX_PATH = os.path.join(JSON_DIR, "index.json")

HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")


# --------------------------------------------------------------------------
# Load and save
# --------------------------------------------------------------------------

def article_section(entry):
    """The article_section dict inside an entry, or {} if absent.

    Mirrors cli_docs_common.article_section rather than importing it, so this
    module stays usable without the CMS client and its .env requirement.
    """
    for block in entry.get("article_content") or []:
        for key, value in block.items():
            if key == "article_section":
                return value or {}
    return {}


class Doc:
    """One docs_article JSON file, with its content parsed as HTML.

    Usage:
        doc = Doc.load(path)
        for h in doc.headings(4):
            doc.to_bold_lead_in(h)
        doc.save()
    """

    def __init__(self, path, entry, soup):
        self.path = path
        self.entry = entry
        self.soup = soup
        self._original = str(soup)
        self.log = []

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as fh:
            entry = json.load(fh)
        html = article_section(entry).get("content") or ""
        # html.parser keeps the markup as-is. lxml and html5lib both inject
        # <html>/<body> wrappers, which would end up serialised into the field.
        return cls(path, entry, BeautifulSoup(html, "html.parser"))

    @property
    def rel(self):
        return os.path.relpath(self.path, JSON_DIR)

    @property
    def heading_field(self):
        """The visible H1, which lives in its own field, not in the content."""
        return (article_section(self.entry).get("heading") or "").strip()

    @property
    def changed(self):
        return str(self.soup) != self._original

    def save(self, dry_run=False):
        """Write the serialised HTML back into the entry. Returns True if written."""
        if not self.changed:
            return False
        if dry_run:
            return True
        article_section(self.entry)["content"] = str(self.soup)
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(self.entry, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        self._original = str(self.soup)
        return True

    def note(self, message):
        self.log.append(message)

    # ----------------------------------------------------------------------
    # Reading structure
    # ----------------------------------------------------------------------

    def headings(self, level=None, min_level=None):
        """Headings in document order. `level` for one level, `min_level` for
        that level and deeper."""
        if level is not None:
            names = [f"h{level}"]
        elif min_level is not None:
            names = [f"h{n}" for n in range(min_level, 7)]
        else:
            names = list(HEADING_TAGS)
        return self.soup.find_all(names)

    def find_heading(self, text, level=2):
        """First heading at `level` whose text matches `text`, case-insensitively."""
        want = norm_text(text)
        for h in self.headings(level=level):
            if norm_text(h.get_text()) == want:
                return h
        return None

    def tables(self):
        return self.soup.find_all("table")


# --------------------------------------------------------------------------
# Heading edits
# --------------------------------------------------------------------------

def promote_heading(tag, level):
    """Change a heading's level in place, keeping its children."""
    old = tag.name
    tag.name = f"h{level}"
    return f"{old} -> h{level}: {norm_text(tag.get_text())!r}"


def to_bold_lead_in(tag):
    """Replace a heading with <p><strong>text</strong></p>.

    CLI-C1 stops CLI headings at H3, because the renderer emits an anchor id and
    a right-hand navigation entry for h2 and h3 only. A bold lead-in is the
    replacement for a fourth level that does not need to be linked to. Inline
    markup inside the heading is preserved rather than flattened to text, so a
    heading containing <span class="code">Syntax</span> keeps its code styling.
    """
    text = norm_text(tag.get_text())
    soup = _owning_soup(tag)
    p = soup.new_tag("p")
    strong = soup.new_tag("strong")
    for child in list(tag.contents):
        strong.append(child.extract())
    p.append(strong)
    tag.replace_with(p)
    return f"{tag.name} -> bold lead-in: {text!r}"


def rename_heading(tag, new_text):
    """Replace a heading's text, dropping any inline markup it carried."""
    old = norm_text(tag.get_text())
    tag.clear()
    tag.append(new_text)
    return f"renamed {tag.name}: {old!r} -> {new_text!r}"


def insert_heading_before(tag, text, level=2):
    """Insert a new heading immediately before `tag`.

    Used to put an <h2>Overview</h2> above intro prose that is already there but
    untitled. Writes no prose of its own.
    """
    soup = _owning_soup(tag)
    h = soup.new_tag(f"h{level}")
    h.append(text)
    tag.insert_before(h)
    return f"inserted h{level} {text!r} before <{tag.name}>"


def _owning_soup(tag):
    """The BeautifulSoup object a tag belongs to, needed for new_tag."""
    node = tag
    while node.parent is not None:
        node = node.parent
    return node


# --------------------------------------------------------------------------
# Table edits
# --------------------------------------------------------------------------

def table_header(table):
    """Header cell texts, lowercased and stripped. [] if the table has no thead."""
    thead = table.find("thead")
    if not thead:
        return []
    row = thead.find("tr")
    if not row:
        return []
    return [norm_text(c.get_text()).lower() for c in row.find_all(["th", "td"])]


def body_rows(table):
    """The <tr> elements of the table body, excluding the header row."""
    tbody = table.find("tbody")
    rows = (tbody or table).find_all("tr")
    if not tbody:
        # No tbody: drop any row that lives inside a thead.
        rows = [r for r in rows if not r.find_parent("thead")]
    return rows


def reshape_table(table, target, rename=None, fill=None):
    """Reshape a table to exactly `target` columns.

    target : list of column names, in order, in the case they should be written.
    rename : {existing lowercased header -> target column name}. Lets an
             `Option` column become `Flag` without touching its cells.
    fill   : {target column name -> callable(row_text_by_column) -> str or Tag}
             supplying a value for a column that has to be created. The callable
             receives a dict of the row's ORIGINAL cell text keyed by column name,
             snapshotted before any cell is touched. That snapshot matters: cells
             are moved into the new row by extracting their children, so a filler
             handed live tags would see whichever cells had already been emptied.
             A column with no filler gets an empty cell, which is the honest
             default: an empty Notes cell says "no caveats", whereas a guessed one
             says something untrue.

    Header and body are rewritten together from one column plan, so a cell can
    never end up under the wrong heading. Returns a one-line description.
    """
    rename = rename or {}
    fill = fill or {}
    current = table_header(table)
    if not current:
        raise ValueError("cannot reshape a table with no thead")

    # Map each target column to the index of the existing column that supplies it.
    canon = [rename.get(h, h) for h in current]
    canon_lower = [c.lower() for c in canon]
    source_index = {}
    for col in target:
        key = col.lower()
        source_index[col] = canon_lower.index(key) if key in canon_lower else None

    dropped = [current[i] for i, c in enumerate(canon_lower) if c not in
               {t.lower() for t in target}]

    soup = _owning_soup(table)
    rows_out = []
    for tr in body_rows(table):
        cells = tr.find_all(["td", "th"])
        # Snapshot the row's text before anything is extracted, so a filler sees
        # the row as it was rather than as it is part way through the rewrite.
        snapshot = {canon[i]: norm_text(cells[i].get_text())
                    for i in range(min(len(canon), len(cells)))}
        new_tr = soup.new_tag("tr")
        for col in target:
            td = soup.new_tag("td")
            idx = source_index[col]
            if idx is not None and idx < len(cells):
                for child in list(cells[idx].contents):
                    td.append(child.extract())
            elif col in fill:
                value = fill[col](snapshot)
                if value is not None:
                    td.append(value)
            new_tr.append(td)
        rows_out.append(new_tr)

    table.clear()
    thead = soup.new_tag("thead")
    hrow = soup.new_tag("tr")
    for col in target:
        th = soup.new_tag("th")
        th.append(col)
        hrow.append(th)
    thead.append(hrow)
    table.append(thead)
    tbody = soup.new_tag("tbody")
    for tr in rows_out:
        tbody.append(tr)
    table.append(tbody)

    return ("reshaped table [%s] -> [%s]%s"
            % (" | ".join(current), " | ".join(c.lower() for c in target),
               f", dropped {dropped}" if dropped else ""))


# --------------------------------------------------------------------------
# Text helpers
# --------------------------------------------------------------------------

def norm_text(text):
    """Collapse whitespace, including the non-breaking spaces the CMS emits."""
    return re.sub(r"\s+", " ", (text or "").replace("\xa0", " ")).strip()


def predict_anchor_id(text):
    """A guess at the anchor id the renderer will emit. NOT authoritative.

    Anchor ids are generated at render time and are not consistently derived:
    `Bulk Publish/Unpublish Limitations` renders as
    `bulk-publish-unpublish-limitations`, while `Bulk Unpublish Entries/Assets`
    renders as `bulk-unpublish-entriesassets`. The same construct produces
    different ids on different pages, so this cannot be computed offline.

    Use this only to shortlist candidates. scripts/cli_anchor_audit.py fetches
    the rendered page and is the only authority on what an anchor actually is.
    """
    slug = norm_text(text).lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    return re.sub(r"[\s_]+", "-", slug).strip("-")


# --------------------------------------------------------------------------
# Corpus iteration
# --------------------------------------------------------------------------

def cli_json_paths(versions=("Version 1", "Version 2")):
    """Every docs/json path in scope, deduplicated and sorted.

    Note that 7 entries appear under two version folders because one CMS entry is
    shown in two nav locations. Both file paths are returned, and both hold the
    same uid, so a caller editing both writes the same entry twice. Use
    `by_uid` when an edit must happen once per entry.
    """
    out = []
    for dirpath, _dirnames, filenames in os.walk(JSON_DIR):
        for name in sorted(filenames):
            if not name.endswith(".json") or name == "index.json":
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, JSON_DIR)
            if any(rel.startswith(v) for v in versions):
                out.append(path)
    return sorted(out)


def by_uid(paths):
    """{uid: [paths]}, so a shared entry is edited once rather than twice."""
    groups = {}
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            entry = json.load(fh)
        groups.setdefault(entry.get("uid"), []).append(path)
    return groups
