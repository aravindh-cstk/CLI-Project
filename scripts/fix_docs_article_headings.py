#!/usr/bin/env python3
"""Strip the version-qualifier suffix from docs_article Heading fields.

The Beta and old-commands docs_article entries carry a trailing version
qualifier in article_content[0].article_section.heading, e.g.
"Configure Regions in the CLI | V2.x.x Beta" or
"Bootstrap Starter Apps | Old Commands". Only the clean document name should
be visible in that heading, so this strips one known trailing suffix (never
a blind split on the first pipe, since some real doc names contain a pipe
themselves, e.g. "Branches | Migration Use Cases | Old Commands").

Usage:
  python3 scripts/fix_docs_article_headings.py            # dry run
  python3 scripts/fix_docs_article_headings.py --confirm  # perform the update + publish
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from heading_cleanup import strip_heading_suffix

REGION_HOST = "https://api.contentstack.io"
CONTENT_TYPE = "docs_article"
LOCALE = "en-us"
PUBLISH_ENV_UIDS = ["blt4a008c3cde35b0c2", "blt92ab7d24e8c52483"]  # staging, development

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "docs/json/index.json")


def load_env():
    path = os.path.join(ROOT, ".env")
    env = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip().strip("'\"")
    api_key = env.get("CONTENTSTACK_DOCS_STACK_API_KEY")
    token = env.get("CONTENTSTACK_DOCS_STACK_MANAGEMENT_TOKEN")
    if not api_key or not token:
        sys.exit("Missing CONTENTSTACK_DOCS_STACK_API_KEY or "
                 "CONTENTSTACK_DOCS_STACK_MANAGEMENT_TOKEN in .env")
    return {"api_key": api_key, "authorization": token, "Content-Type": "application/json"}


def request(method, path, headers, body=None, params=None, attempts=4):
    url = f"{REGION_HOST}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < attempts - 1:
                time.sleep(2 ** attempt)
                continue
            sys.exit(f"HTTP {exc.code} for {method} {url}\n{exc.read().decode('utf-8', 'replace')[:800]}")
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < attempts - 1:
                time.sleep(2 ** attempt)
                continue
            sys.exit(f"Network error for {url}: {exc}")
    return None


def article_content_block(entry):
    for block in entry.get("article_content") or []:
        if "article_section" in block:
            return block
    sys.exit(f"entry {entry.get('uid')} has no article_section block")


def load_targets():
    with open(INDEX_PATH, encoding="utf-8") as fh:
        entries = json.load(fh)["entries"]
    targets = []
    for e in entries:
        if e["bucket"] not in ("Beta", "old"):
            continue
        uid = e["uid"]
        if not uid or uid == "<TO BE ASSIGNED>":
            print(f"Skipping '{e['title']}': no live uid yet")
            continue
        targets.append(e)
    return targets


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    targets = load_targets()

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")

    unmatched = []
    changed = 0
    for e in targets:
        uid = e["uid"]
        fresh = request("GET", f"/v3/content_types/{CONTENT_TYPE}/entries/{uid}", headers,
                         params={"locale": LOCALE})["entry"]
        block = article_content_block(fresh)
        heading = block["article_section"]["heading"]
        cleaned = strip_heading_suffix(heading)
        if cleaned is None:
            unmatched.append((uid, heading))
            continue
        if cleaned == heading:
            print(f"{e['title']}: heading already clean ('{heading}'), skipping")
            continue

        print(f"{e['title']} ({uid}): '{heading}' -> '{cleaned}'")
        changed += 1
        if not confirm:
            continue

        block["article_section"]["heading"] = cleaned
        updated = request("PUT", f"/v3/content_types/{CONTENT_TYPE}/entries/{uid}", headers,
                           body={"entry": fresh}, params={"locale": LOCALE})["entry"]
        new_version = updated["_version"]
        publish_body = {
            "entry": {"environments": PUBLISH_ENV_UIDS, "locales": [LOCALE]},
            "locale": LOCALE,
            "version": new_version,
        }
        request("POST", f"/v3/content_types/{CONTENT_TYPE}/entries/{uid}/publish", headers,
                body=publish_body)
        print(f"  updated -> v{new_version}, published to staging + development")
        time.sleep(0.3)

    if unmatched:
        sys.exit(f"\nThese headings don't end with a known suffix, fix the mapping before proceeding: {unmatched}")

    print(f"\n{changed} heading(s) {'updated' if confirm else 'would be updated'}.")
    print("\nDone." if confirm else "\nDry run complete, no writes made. Re-run with --confirm to apply.")


if __name__ == "__main__":
    main()
