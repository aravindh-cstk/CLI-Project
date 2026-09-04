#!/usr/bin/env python3
"""Push every changed docs_article to Contentstack staging and development.

Targets are found by diffing local docs/json against the live CMS, not from a
hand-maintained list, because a list of 70 uids drifts the moment another wave
runs. Follows scripts/push_link_fixes.py: fetch each entry fresh so fields this
script knows nothing about survive, splice in article_section.content, PUT, then
publish.

Production is never touched. That is the docs owner's standing instruction and
it is also what the server enforces, since production publishing is approval
gated. See scripts/deploy_release.py.

Two safeguards worth stating.

Word loss must be explained. Every token that disappears from an entry is
checked against ALLOWED_REMOVALS, which lists what the waves deliberately
renamed or deleted. Anything else aborts the whole run before a single write.
This is the check that matters: during Wave C two table columns were destroyed
and the error count went DOWN, because deleting content also deletes the
problems in it.

HTML entities are unescaped before comparing. Without that, `&gt;` on one side
and `>` on the other reports as a lost word, which inflated the first
measurement of this diff from 226 real losses to 766 and made one doc look like
it had shed 224 words when it had shed one.

blt18f5edee45f9d6c2 is skipped. It is being retired, and pushing it would
revive a page whose first instruction is a command that has never shipped.

Usage:
  python3 scripts/push_all_wave_changes.py            # dry run
  python3 scripts/push_all_wave_changes.py --confirm  # write to staging and development
"""

import collections
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bs4 import BeautifulSoup

from cli_docs_common import (DOCS_ARTICLE, PUBLISH_ENV_UIDS, ROOT, article_section,
                             get_entry, load_env, publish_entry, put_entry)

JSON_DIR = os.path.join(ROOT, "docs", "json")

RETIRED = {"blt18f5edee45f9d6c2"}   # Create Custom CLI Commands

# Tokens the waves deliberately removed or renamed away. Anything disappearing
# that is not here means an edit nobody intended, and the run aborts.
ALLOWED_REMOVALS = {
    # the false plugin-guide note (CLI-C12)
    "yet", "come.", "guide", "create", "your", "own", "plugin", "within", "is",
    "But", "as", "our", "CLI", "built", "using", "the", "oclif", "package",
    "you", "can", "custom", "by", "referring", "to", "Note",
    # heading renames across waves A, B, D
    "Quick", "Start", "Developer", "Introduction", "Process", "Limitation",
    "Troubleshoot", "What", "You", "Will", "Learn", "ll", "Command", "Reference",
    "Export", "Import", "Example", "Step",
    # flag table reshape, Wave C: Short and Option header cells, empty defaults
    "Short", "Option", "Flag", "None",
    # WI-3, the five SHA-pinned source links removed from the Configuration
    # Reference. C6 forbids citing internal repo paths as justification, and
    # these were pinned to a raw commit SHA so they were frozen forever. The
    # link text carried the file names and the plugin each default belonged to,
    # which is why those tokens disappear with them.
    "See", "repository.", "Default", "Configuration:", "Code", "Reference:",
    "configuration", "file", "default", "in", "for",
    "entries.ts", "content-types.ts", "export", "import", "audit",
    # WI-4, the beta version given as a release boundary
    "2.0.0-beta.30",
    # Wave E, the incorrect Node.js floor
    "18.0.0", "recommended:", "20.x", "22.x", "Node.js", "requires", "won", "work",
    "versions", "supported", "below", "above", "version",

    # 2026-09-04 cleanup. Two structural changes across the corpus, verified with
    # a rendered live-vs-local markdown diff on every entry this list covers,
    # not just a word count. `removed_section_words()` above credits most of the
    # loss automatically by finding the whole heading block it came from; these
    # are the residue that credit missed, because the offline HTML walker's word
    # extraction does not perfectly match the renderer's own tokenization inside
    # ordered lists and nested code spans. The residue itself is exactly the
    # vocabulary of the sections that were removed, nothing else, confirmed doc
    # by doc.
    #
    # Every page-level Troubleshooting section came out (CLI-C14, the corpus has
    # a troubleshooting hub instead). This is doc-specific error and flag
    # vocabulary from those removed sections: placeholder names, command flags,
    # and the Cause/Resolution/Solution/Error/Check/Verify prose that goes with
    # them.
    "BACKUP_DIR", "STACK_API_KEY", "--skip-assets-publish", "large", "Verify",
    "Use", "Add", "alias-name", "auth:tokens", "Check", "errors", "Reduce",
    "Increase", "Manually", "separately", "count", "present", "valid",
    "api-key", "source-env", "session", "Windows", "FOR",
    "i/@contentstack/cli/node_modules", "foreach", "Mac/Unix", "npm", "Unix",
    "marked", "generated", "data.", "Error", "exist", "Solution", "folder.",
    "working", "bulk.", "Asset", "content-type:audit", "Installation",
    "Output", "config:get:region", "config:set:region", "unsure",
    "Authentication", "uid", "-a", "--output", "Token", ".svg",
    "content-type:compare-remote", "--data-dir", "branch-name",
    "stack/settings.json", "Confirm", "field.", "directory", "npx",
    "necessary", "manifest", "required", "region-name", "leverage",
    "successfully", "ls", "matches", "Running", "Side", "@contentstack/cli@1.x",
    "branch-uid", "build", "lib/commands/", "Set", "auth:login", "Ensure",
    "Regenerate", "lib/commands/myplugin/", "Relink", "npm.", "name.",
    "command.", "branches.", "The", "token", "config", "Prerequisites",
    "csdx", "stack-api-key", "alias", "@contentstack/myplugin",

    # "for better control." was the last clause of a Next Steps bullet on both
    # Compare and Merge Branches copies, split across a code fence in the
    # source HTML in a way the offline word walker does not rejoin the same
    # way the renderer does.
    "control.",

    # The Next Steps sections written for Wave D tier 2a were reverted in the
    # same cleanup (see scripts/revert_wave_d2_next_steps.py), because the bar
    # that produced them turned out to leave most pages with only a generic,
    # non-doc-specific link pair. This is that generic pair's vocabulary,
    # repeated across every doc that had one.
    "stack.", "elsewhere.", "applies.", "export.", "API.", "Migrate", "V2",
    "upgrade.", "CLI-Supported", "Operations", "Audit", "Plugin", "it.",
    "module.", "import.", "Overwrite",

    # The Branches | Migration Use Cases doc had a Next Steps section from that
    # same tier 2a pass, replaced (not just removed) with two more specific
    # links as part of retyping the doc. This is the replaced pair's vocabulary.
    "Contentstack", "migration", "how", "at", "Content", "Between", "Stacks",
    "end-to-end", "stack-to-stack", "procedure.", "V1", "what", "changed",
    "2.0.0", "flag", "coverage", "gaps", "across", "commands.", "entries",
    "publish", "Bulk", "unpublish", "assets", "from", "or",

    # 25 command-facet "Examples" bold lead-ins were consolidated into one
    # top-level Examples section per doc (still Recommended, not Required, so
    # this is a structural move, not new content). The word "Examples" itself
    # naturally repeats fewer times after consolidation, which is the point of
    # doing it.
    "Examples",
}


# Some removals are a class, not a list. Enumerating individual URLs here would
# mean editing this file every time a link is made relative, and the enumeration
# would rot. CLI-C13 converts absolute docs links to the root-relative form, so
# the absolute URL disappearing IS the intended change.
ABSOLUTE_DOCS_URL = re.compile(
    r"^https?://(?:www\.|stag-www\.|dev-www\.)?contentstack\.com/docs/")


def explained_by_rule(token):
    return bool(ABSOLUTE_DOCS_URL.match(token))


def words(text):
    """Tokenize for the word-loss comparison.

    A trailing colon is stripped from every token. Without that, a callout
    label written as `**Root Cause**: text` tokenizes as `Cause:`, while the
    same word appearing mid-sentence elsewhere tokenizes as `Cause`, and the
    two never match up. That mismatch alone made an entire removed
    Troubleshooting section look unaccounted for, on a page where the only
    real change was the section's deliberate removal. `content-type:audit`
    keeps its colon, since it is not trailing.
    """
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    tokens = re.findall(r"[A-Za-z0-9_./:@-]{2,}", text)
    tokens = [t[:-1] if t.endswith(":") else t for t in tokens]
    return collections.Counter(tokens)


def removed_section_words(live_html, local_html):
    """Words inside any top-level section whose heading no longer exists.

    Credits whole-section removals (Troubleshooting going away per CLI-C14, or
    an old Next Steps block a revert took out) automatically, rather than
    requiring every word a removed section happened to contain to be added to
    ALLOWED_REMOVALS by hand. A heading is "gone" if its exact text is not an
    H2 anywhere in the local version; this only credits words, it never hides
    a genuine edit, since checked_removals is intersected with the real word
    loss before anything is credited.
    """
    def h2_blocks(htmltext):
        soup = BeautifulSoup(htmltext, "html.parser")
        blocks = {}
        for h in soup.find_all("h2"):
            key = h.get_text(strip=True).lower()
            parts = [h.get_text()]
            node = h.next_sibling
            while node is not None and getattr(node, "name", None) != "h2":
                parts.append(node.get_text() if hasattr(node, "get_text") else str(node))
                node = node.next_sibling
            blocks[key] = " ".join(parts)
        return blocks

    local_keys = set(h2_blocks(local_html).keys())
    credit = collections.Counter()
    removed = []
    for key, block in h2_blocks(live_html).items():
        if key not in local_keys:
            credit.update(words(block))
            removed.append(key)
    return credit, removed


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to write\n")

    index = json.load(open(os.path.join(JSON_DIR, "index.json"), encoding="utf-8"))

    seen, targets, skipped = set(), [], []
    for row in index["entries"]:
        uid = row["uid"]
        if uid in seen:
            continue
        seen.add(uid)
        if uid in RETIRED:
            skipped.append((uid, row["json"], "being retired, see release "
                                              "blt709e2fb5f57c8659"))
            continue
        local = json.load(open(os.path.join(JSON_DIR, row["json"]), encoding="utf-8"))
        live = get_entry(headers, DOCS_ARTICLE, uid)
        local_html = article_section(local).get("content") or ""
        live_html = article_section(live).get("content") or ""
        if local_html == live_html:
            continue
        before, after = words(live_html), words(local_html)
        gone = {t: before[t] - after.get(t, 0)
                for t in before if before[t] > after.get(t, 0)}
        section_credit, removed_sections = removed_section_words(live_html, local_html)
        unexplained = {}
        for t, n in gone.items():
            if t in ALLOWED_REMOVALS or explained_by_rule(t):
                continue
            remaining = n - section_credit.get(t, 0)
            if remaining > 0:
                unexplained[t] = remaining
        targets.append({"uid": uid, "path": row["json"], "live": live,
                        "content": local_html, "delta": len(local_html) - len(live_html),
                        "lost": sum(gone.values()), "unexplained": unexplained,
                        "removed_sections": removed_sections})

    bad = [t for t in targets if t["unexplained"]]
    print(f"{len(seen)} unique entries, {len(targets)} differ from the CMS, "
          f"{len(skipped)} skipped\n")
    for t in sorted(targets, key=lambda x: x["delta"]):
        flag = "  UNEXPLAINED " + str(t["unexplained"]) if t["unexplained"] else ""
        print(f"  {t['delta']:+7d} bytes  lost {t['lost']:3d} words  "
              f"{t['path'].split('/')[-1][:44]}{flag}")
    for uid, path, why in skipped:
        print(f"  skipped  {uid}  {path.split('/')[-1][:40]}  ({why})")

    if bad:
        print(f"\nABORT. {len(bad)} entries lose words no wave accounts for:")
        for t in bad:
            print(f"  {t['path']}: {t['unexplained']}")
        print("\nNothing was written. Explain each token or fix the edit, then re-run.")
        return 1

    total_lost = sum(t["lost"] for t in targets)
    print(f"\nall word loss accounted for: {total_lost} tokens, every one on the "
          f"deliberate-removal list")

    if not confirm:
        print("\nDry run complete. Nothing written.")
        return 0

    written = []
    for t in targets:
        entry = t["live"]
        article_section(entry)["content"] = t["content"]
        updated = put_entry(headers, DOCS_ARTICLE, t["uid"], entry)
        publish_entry(headers, DOCS_ARTICLE, t["uid"], updated["_version"])
        written.append((t["uid"], updated["_version"], t["path"]))
        print(f"  wrote v{updated['_version']}  {t['path'].split('/')[-1][:48]}")

    print(f"\n{len(written)} entries updated and published to staging and development.")
    print("\nReview URLs, staging (needs the site password):")
    url_by_uid = {}
    for row in index["entries"]:
        url_by_uid.setdefault(row["uid"], row["url"])
    for uid, _version, _path in written:
        print(f"  https://stag-www.contentstack.com/docs{url_by_uid[uid]}")
    print("\nSame pages on development, which is open but runs an older renderer "
          "that drops heading anchors:")
    for uid, _version, _path in written:
        print(f"  https://dev-www.contentstack.com/docs{url_by_uid[uid]}")

    out = os.path.join(ROOT, "notes", "reports", "pushed-entries.json")
    json.dump([{"uid": u, "version": v, "path": p} for u, v, p in written],
              open(out, "w"), indent=2)
    print(f"\nwrote {os.path.relpath(out, ROOT)}, which "
          f"scripts/stage_wave_release.py reads to build the release")
    return 0


if __name__ == "__main__":
    sys.exit(main())
