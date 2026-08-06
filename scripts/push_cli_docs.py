#!/usr/bin/env python3
"""Push the article_section.content of specific docs/json entries back to Contentstack.

Scope is deliberately explicit (TARGETS below), not "every changed file in docs/json" -
this pushes the asset-scanning documentation fixes to five existing entries only.

For each target: fetch the entry fresh (so any field we do not know about is preserved),
splice in the content HTML from the local docs/json file, PUT the update, then publish
the resulting version to the given environments.

Also strips any known version-qualifier suffix (see heading_cleanup.py) from the live
heading on every push, so a Beta/old-commands heading never regresses back to something
like "... | V2.x.x Beta" even if the local docs/json file still has the old heading.

Usage:
  python3 scripts/push_cli_docs.py            # dry run: show what would change, no writes
  python3 scripts/push_cli_docs.py --confirm  # perform the update + publish
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

TARGETS = [
    ("docs/json/GA/bulk-publish-and-unpublish-content.json", "blt804647818d4181f9"),
    ("docs/json/GA/import-content-using-the-cli.json", "blt1ee86e6419f390f8"),
    ("docs/json/GA/cli-limitations.json", "blt74918691c8a465c1"),
    ("docs/json/Beta/bulk-operations-in-cli.json", "blt85d9deae08de968d"),
    ("docs/json/Beta/import-content-using-the-cli.json", "blt1215a1f9bbcc9900"),
]


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
    sys.exit("entry has no article_section block")


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")

    for rel_path, uid in TARGETS:
        local_path = os.path.join(ROOT, rel_path)
        with open(local_path, encoding="utf-8") as fh:
            local_entry = json.load(fh)
        new_content = article_content_block(local_entry)["article_section"]["content"]

        fresh = request("GET", f"/v3/content_types/{CONTENT_TYPE}/entries/{uid}", headers,
                         params={"include_publish_details": "true"})["entry"]
        live_block = article_content_block(fresh)
        live_content = live_block["article_section"]["content"]
        live_heading = live_block["article_section"]["heading"]
        new_heading = strip_heading_suffix(live_heading)
        if new_heading is None:
            sys.exit(f"{rel_path}: heading '{live_heading}' ends with an unrecognized "
                     f"' | ...' suffix, fix heading_cleanup.py before proceeding")

        if live_content == new_content and live_heading == new_heading:
            print(f"{rel_path}: no change from current live v{fresh['_version']}, skipping")
            continue

        print(f"{rel_path}: live v{fresh['_version']} -> will update"
              f"{' and publish to staging+development' if confirm else ''}")
        if live_heading != new_heading:
            print(f"  heading '{live_heading}' -> '{new_heading}'")

        if not confirm:
            continue

        live_block["article_section"]["content"] = new_content
        live_block["article_section"]["heading"] = new_heading
        update_body = {"entry": fresh}
        updated = request(
            "PUT", f"/v3/content_types/{CONTENT_TYPE}/entries/{uid}", headers,
            body=update_body, params={"locale": LOCALE},
        )["entry"]
        new_version = updated["_version"]
        print(f"  updated -> v{new_version}")

        publish_body = {
            "entry": {"environments": PUBLISH_ENV_UIDS, "locales": [LOCALE]},
            "locale": LOCALE,
            "version": new_version,
        }
        request("POST", f"/v3/content_types/{CONTENT_TYPE}/entries/{uid}/publish", headers,
                body=publish_body)
        print(f"  published v{new_version} to staging + development")
        time.sleep(0.3)

    print("\nDone." if confirm else "\nDry run complete, no writes made.")


if __name__ == "__main__":
    main()
