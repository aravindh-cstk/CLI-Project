"""Shared rule for stripping version-qualifier suffixes from docs_article headings.

Some CLI docs_article entries carry a trailing version qualifier in their
article_section heading, e.g. "Configure Regions in the CLI | V2.x.x Beta" or
"Bootstrap Starter Apps | Old Commands". Only the clean document name should
ever be visible in that heading. Used by both fix_docs_article_headings.py
(one-off live cleanup) and push_cli_docs.py (so future pushes never
reintroduce the suffix).
"""

KNOWN_HEADING_SUFFIXES = [
    " | V2.x.x Beta",
    " | Beta Commands",
    " | V2 Beta",
    " | Beta",
    " | Old Commands",
    # Applied to title and seo.title by the URL restructure. Listed here so the
    # heading cleanup keeps stripping them from the visible H1, which stays
    # version-free, and so a later push never leaves a doubled label behind.
    " | V0.x.x",
    " | V1.x.x",
    " | V2.x.x",
]


def strip_heading_suffix(heading):
    """Return heading with a known trailing suffix removed, unchanged if none
    match, or None if the heading is non-empty and ends with a pipe segment
    that isn't a recognized suffix (caller should treat that as needing review
    rather than silently leaving it or guessing at a split point)."""
    for suffix in KNOWN_HEADING_SUFFIXES:
        if heading.endswith(suffix):
            return heading[: -len(suffix)].rstrip()
    if " | " in heading:
        return None
    return heading
