#!/usr/bin/env python3
"""Reset docs/json to what the CMS currently holds, then regenerate the markdown.

This is the reliable way to undo a wave and start again. `git checkout -- docs/json`
is not: some docs/json files are untracked, so git leaves them edited, and
index.json is tracked with fewer entries than the working tree carries, so a
checkout silently drops rows for the untracked docs.

Read-only against the CMS. Every call is a GET. Writes only local files.

Usage:
  python3 scripts/reset_docs_json.py            # dry run, reports what differs
  python3 scripts/reset_docs_json.py --confirm   # overwrite local JSON from the CMS
"""

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli_docs_common import DOCS_ARTICLE, ROOT, get_entry, load_env

JSON_DIR = os.path.join(ROOT, "docs", "json")
INDEX_PATH = os.path.join(JSON_DIR, "index.json")


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    index = json.load(open(INDEX_PATH, encoding="utf-8"))

    changed = same = missing = 0
    for record in index["entries"]:
        path = os.path.join(JSON_DIR, record["json"])
        if not os.path.exists(path):
            missing += 1
            print(f"  [missing locally] {record['json']}")
            continue
        local = json.load(open(path, encoding="utf-8"))
        live = get_entry(headers, DOCS_ARTICLE, local["uid"])
        if json.dumps(live, sort_keys=True) == json.dumps(local, sort_keys=True):
            same += 1
            continue
        changed += 1
        print(f"  [{'reset' if confirm else 'would reset'}] {record['json']}")
        if confirm:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(live, fh, indent=2, ensure_ascii=False)
                fh.write("\n")

    print(f"\n{changed} differ from the CMS, {same} identical, {missing} missing locally")
    if not confirm:
        print("Dry run. Nothing written. Re-run with --confirm.")
        return

    print("\nregenerating docs/markdown from docs/json")
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "json_to_markdown.py")],
                   check=True)


if __name__ == "__main__":
    main()
