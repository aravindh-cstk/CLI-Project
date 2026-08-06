#!/usr/bin/env python3
"""Phase 6: repoint CLI links that live in non-CLI docs.

A non-CLI doc has no version context of its own, so every CLI link in one goes to
the current GA doc: the bare URL where the topic has a V2 doc, otherwise /v1. This
differs from the in-version rule used inside the CLI docs themselves.

Scope is discovered live rather than from a saved list, so a doc that gained a CLI
link since the last scan is still caught. The 73 CLI docs are excluded here, since
push_cli_url_changes.py owns those.

Anchors are preserved. Legacy /docs/developers/cli/* links are repointed too.

Usage:
  python3 scripts/fix_inbound_cli_links.py            # dry run
  python3 scripts/fix_inbound_cli_links.py --confirm  # update, publish, add to release
"""

import collections
import json
import sys
import time

import cli_release
import cli_url_map as url_map
import rewrite_cli_links as links
from cli_docs_common import (DOCS_ARTICLE, LOCALE, PROD_ENV_UID, is_published_to,
                             list_entries, load_env, publish_entry, put_entry,
                             request)


def make_ga_rewriter(docs, lookup, report):
    """re.sub callback sending every CLI link to the current GA doc for its topic."""

    def rewrite(match):
        whole = match.group(0)
        slug = match.group("slug")
        if slug not in lookup:
            return whole
        target = url_map.current_ga_url(docs, slug)
        if target is None:
            report.append((whole, None))
            return whole
        new = f"{match.group('host') or ''}{match.group('prefix') or ''}{target}"
        new += match.group("anchor") or ""
        if new != whole:
            report.append((whole, new))
        return new

    return rewrite


def rewrite_strings(value, rewriter):
    """Walk a nested entry value, rewriting CLI links in every string it contains."""
    if isinstance(value, str):
        return links.rewrite_all(value, rewriter, rewriter)
    if isinstance(value, list):
        return [rewrite_strings(item, rewriter) for item in value]
    if isinstance(value, dict):
        return {key: rewrite_strings(item, rewriter) for key, item in value.items()}
    return value


def rewrite_entry_links(entry, rewriter):
    """Rewrite links throughout an entry, leaving its own url field alone.

    Nested url fields are rewritten, since a CTA or card link to a CLI doc needs
    moving like any other. Only the entry's own top-level url identifies the page
    and must survive untouched.
    """
    own_url = entry.get("url")
    updated = rewrite_strings(entry, rewriter)
    if "url" in entry:
        updated["url"] = own_url
    return updated


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    docs = url_map.load_map()
    lookup = links.build_lookup(docs)
    cli_uids = {d["uid"] for d in docs}

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n", flush=True)
    print("Listing docs_article entries...", file=sys.stderr)

    # Page through with the link-bearing fields included so the whole corpus is
    # scanned in ~45 requests. Only the entries that actually contain a CLI link
    # are then fetched in full, because a PUT has to send every field back.
    stubs = list_entries(headers, DOCS_ARTICLE, progress=True,
                         only=("uid", "url", "title", "article_content",
                               "related_articles", "next_and_prev_links",
                               "md_content", "seo"))
    live = [s for s in stubs if is_published_to(s, PROD_ENV_UID)]
    candidates = [s for s in live
                  if s["uid"] not in cli_uids
                  and any(slug in json.dumps(s, ensure_ascii=False) for slug in lookup)]
    print(f"{len(stubs)} entries, {len(live)} published to production, "
          f"{len(cli_uids)} of them CLI docs.\n"
          f"{len(candidates)} non-CLI doc(s) mention a CLI slug, fetching those "
          f"in full.\n", flush=True)

    release_uid, release_items = None, None
    if confirm:
        release_uid = cli_release.ensure_release(headers, cli_release.RELEASE_DOCS)
        release_items = cli_release.index_items(headers, release_uid)

    touched, unresolved = [], []
    samples = collections.Counter()
    for stub in sorted(candidates, key=lambda s: s.get("url") or ""):
        entry = request("GET", f"/v3/content_types/{DOCS_ARTICLE}/entries/{stub['uid']}",
                        headers, params={"locale": LOCALE})["entry"]
        before = json.dumps(entry, ensure_ascii=False)

        report = []
        rewriter = make_ga_rewriter(docs, lookup, report)
        updated = rewrite_entry_links(entry, rewriter)
        after = json.dumps(updated, ensure_ascii=False)
        if after == before:
            continue

        moved = [(a, b) for a, b in report if b]
        for pair in moved:
            samples[pair] += 1
        unresolved += [(stub.get("url"), a) for a, b in report if not b]

        print(f"{stub.get('url')}  ({stub['uid']}, v{entry['_version']})")
        for old, new in moved:
            print(f"   {old}\n      -> {new}")
        touched.append((stub, updated, len(moved)))

        if confirm:
            fresh = put_entry(headers, DOCS_ARTICLE, stub["uid"], updated)
            publish_entry(headers, DOCS_ARTICLE, stub["uid"], fresh["_version"])
            cli_release.add_item(headers, release_uid, DOCS_ARTICLE, stub["uid"],
                                 fresh["_version"], LOCALE, release_items)
            print(f"   updated -> v{fresh['_version']}, published, added to release")
            time.sleep(0.25)

    total = sum(count for _, _, count in touched)
    print(f"\n{len(touched)} non-CLI doc(s) to update, {total} link occurrence(s).")
    print(f"{len(samples)} distinct rewrite(s).")
    if unresolved:
        print("\nLinks that could not be resolved:")
        for url, link in unresolved:
            print(f"  {url}: {link}")

    if confirm:
        print(f"\nRelease {release_uid}.")
    else:
        print("\nDry run complete, no writes made.")


if __name__ == "__main__":
    main()
