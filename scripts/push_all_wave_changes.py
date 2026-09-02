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
}


def words(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return collections.Counter(re.findall(r"[A-Za-z0-9_./:@-]{2,}", text))


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
        unexplained = {t: n for t, n in gone.items() if t not in ALLOWED_REMOVALS}
        targets.append({"uid": uid, "path": row["json"], "live": live,
                        "content": local_html, "delta": len(local_html) - len(live_html),
                        "lost": sum(gone.values()), "unexplained": unexplained})

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
