#!/usr/bin/env python3
"""Fresh-import CLI docs from the links_2026 nav tree into docs/json/ and docs/markdown/.

Walks the links_2026 tree starting at the "CLI" root entry, recursing into
nested_links. Each links_2026 child becomes a folder (named by its title,
verbatim). Each docs_article leaf becomes a JSON file (the raw entry) and a
Markdown file (converted via json_to_markdown.Converter), written to the same
relative path under docs/json/ and docs/markdown/.

This replaces the old GA/Beta/old bucket layout entirely: those folders are
deleted first, since the nav tree no longer has any notion of those buckets.
"""

import json
import os
import re
import shutil
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cli_docs_common import get_entry, load_env
from json_to_markdown import Converter, article_section, front_matter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(ROOT, "docs", "json")
MD_DIR = os.path.join(ROOT, "docs", "markdown")
INDEX_PATH = os.path.join(JSON_DIR, "index.json")

CLI_ROOT_UID = "bltd697fa2bc1e38b53"
OLD_BUCKETS = ("GA", "Beta", "old")
TITLE_PREFIX_RE = re.compile(r"^\[.*?\]\s*-\s*")


def clean_name(title):
    """Strip a leading bracketed prefix from a docs_article title, e.g.
    '[Contentstack Command-line Interface (CLI)] - Install the CLI | V2.x.x'
    becomes 'Install the CLI | V2.x.x'.
    """
    name = TITLE_PREFIX_RE.sub("", title or "").strip()
    return name or title


def walk(headers, uid, ancestors, leaves, empty_folders):
    """Recurse into a links_2026 entry, collecting (folder_path, docs_article entry)
    tuples in leaves and logging folders with no nested_links in empty_folders."""
    entry = get_entry(headers, "links_2026", uid)
    title = entry.get("title") or uid
    here = ancestors + [title]
    nested = entry.get("nested_links") or []
    if not nested:
        empty_folders.append("/".join(here))
        return
    for link in nested:
        time.sleep(0.05)
        if link.get("_content_type_uid") == "links_2026":
            walk(headers, link["uid"], here, leaves, empty_folders)
        else:
            article = get_entry(headers, "docs_article", link["uid"])
            leaves.append((tuple(here), article))


def main():
    headers = load_env()

    print("Walking links_2026 nav tree...", file=sys.stderr)
    root = get_entry(headers, "links_2026", CLI_ROOT_UID)
    leaves, empty_folders = [], []
    for link in root.get("nested_links") or []:
        if link.get("_content_type_uid") != "links_2026":
            sys.exit(f"root {CLI_ROOT_UID} has an unexpected docs_article leaf: {link}")
        walk(headers, link["uid"], [], leaves, empty_folders)

    print(f"{len(leaves)} leaf references, "
          f"{len({a['uid'] for _, a in leaves})} distinct articles", file=sys.stderr)
    for folder in empty_folders:
        print(f"WARNING: empty folder, nothing written: {folder}", file=sys.stderr)

    for bucket in OLD_BUCKETS:
        for base in (JSON_DIR, MD_DIR):
            old_dir = os.path.join(base, bucket)
            if os.path.isdir(old_dir):
                shutil.rmtree(old_dir)

    converter = Converter()
    manifest, seen_names, shared = [], {}, Counter()

    for folder_path, article in leaves:
        name = clean_name(article.get("title"))
        key = folder_path + (name,)
        if key in seen_names and seen_names[key] != article["uid"]:
            sys.exit(f"filename collision in {'/'.join(folder_path)}: "
                      f"'{name}' wanted by both {seen_names[key]} and {article['uid']}")
        seen_names[key] = article["uid"]
        shared[article["uid"]] += 1

        json_rel = os.path.join(*folder_path, f"{name}.json") if folder_path else f"{name}.json"
        md_rel = os.path.join(*folder_path, f"{name}.md") if folder_path else f"{name}.md"

        json_path = os.path.join(JSON_DIR, json_rel)
        md_path = os.path.join(MD_DIR, md_rel)
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        os.makedirs(os.path.dirname(md_path), exist_ok=True)

        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(article, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

        section = article_section(article)
        heading = (section.get("heading") or "").strip()
        body = converter.convert(section.get("content") or "")
        document = f"{front_matter(article)}\n\n# {heading}\n\n{body}\n"
        with open(md_path, "w", encoding="utf-8") as fh:
            fh.write(document)

        manifest.append({
            "uid": article["uid"],
            "title": article.get("title"),
            "folder": list(folder_path),
            "url": article.get("url"),
            "json": json_rel.replace(os.sep, "/"),
            "markdown": md_rel.replace(os.sep, "/"),
        })

    dupes = {uid: count for uid, count in shared.items() if count > 1}
    if dupes:
        print(f"NOTE: {len(dupes)} articles written to multiple nav locations: "
              f"{sorted(dupes)}", file=sys.stderr)

    with open(INDEX_PATH, "w", encoding="utf-8") as fh:
        json.dump({
            "stack_api_key": headers["api_key"],
            "content_type": "docs_article",
            "locale": "en-us",
            "cli_root_uid": CLI_ROOT_UID,
            "total": len(manifest),
            "entries": manifest,
        }, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"Wrote {len(manifest)} JSON + Markdown files, plus index.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
