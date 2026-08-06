#!/usr/bin/env python3
"""Flatten Version 0.x.x and Version 2.x.x to a direct docs_article dump.

Per the user's latest direction, abandon the per-category duplication/
substitution approach entirely for 0.x.x and 2.x.x:
  - Version 2.x.x (blt4ed3b6f5b3651053): nested_links = all Beta-tagged
    docs_article entries directly, no sub-sections.
  - Version 0.x.x (bltec579cd326694d5b): nested_links = all old-commands
    docs_article entries directly, no sub-sections.
  - Version 1.x.x (bltd7ee0a881bc07d3a): unchanged, keeps its existing 6
    category sections (already correct: exactly the docs with no beta/
    old-commands tag).

This fully overwrites nested_links on the two version entries, which
implicitly unlinks (but does not delete) every section entry they used to
reference: the 12 duplicate categories for 0.x.x, the 6 duplicate categories
for 2.x.x, and the 12 old-commands flat placeholder sections under 0.x.x.
Per the user's decision those are left alone in Contentstack, just no longer
referenced from the version entries.

Usage:
  python3 scripts/flatten_v0_v2_nav.py            # dry run
  python3 scripts/flatten_v0_v2_nav.py --confirm  # perform the update + publish
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

REGION_HOST = "https://api.contentstack.io"
LOCALE = "en-us"
PUBLISH_ENV_UIDS = ["blt4a008c3cde35b0c2", "blt92ab7d24e8c52483"]  # staging, development

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "docs/json/index.json")

VERSION_2X_UID = "blt4ed3b6f5b3651053"
VERSION_0X_UID = "bltec579cd326694d5b"

# Two doc families outside the tracked CLI breadcrumb (not in docs/json/index.json)
# confirmed live to have a Beta variant and no old-commands variant.
EXTRA_BETA_UIDS = [
    "blt8012fa025c919ece",  # Content Type Plugin | V2 Beta
    "blt50c45d9983b508a7",  # Regex Validate Plugin | V2 Beta
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


def load_index():
    with open(INDEX_PATH, encoding="utf-8") as fh:
        return json.load(fh)["entries"]


def get_entry(headers, content_type, uid):
    return request("GET", f"/v3/content_types/{content_type}/entries/{uid}", headers,
                    params={"locale": LOCALE})["entry"]


def publish(headers, content_type, uid, version):
    body = {
        "entry": {"environments": PUBLISH_ENV_UIDS, "locales": [LOCALE]},
        "locale": LOCALE,
        "version": version,
    }
    request("POST", f"/v3/content_types/{content_type}/entries/{uid}/publish", headers, body=body)


def put_entry(headers, content_type, uid, entry, confirm):
    if not confirm:
        return entry
    updated = request("PUT", f"/v3/content_types/{content_type}/entries/{uid}", headers,
                       body={"entry": entry}, params={"locale": LOCALE})["entry"]
    publish(headers, content_type, uid, updated["_version"])
    return updated


def ref(uid):
    return {"uid": uid, "_content_type_uid": "docs_article"}


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    index_entries = load_index()

    beta_uids = [e["uid"] for e in index_entries if e["bucket"] == "Beta"] + EXTRA_BETA_UIDS
    old_uids = [e["uid"] for e in index_entries if e["bucket"] == "old"]

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")
    print(f"Version 2.x.x will get {len(beta_uids)} direct Beta docs_article refs.")
    print(f"Version 0.x.x will get {len(old_uids)} direct old-commands docs_article refs.")
    print("Version 1.x.x is left unchanged.\n")

    for version_uid, label, target_uids in (
        (VERSION_2X_UID, "Version 2.x.x", beta_uids),
        (VERSION_0X_UID, "Version 0.x.x", old_uids),
    ):
        entry = get_entry(headers, "links_2026", version_uid)
        current = [n["uid"] for n in entry.get("nested_links", [])]
        target = list(target_uids)
        if current == target:
            print(f"{label}: nested_links already correct ({len(current)} refs), skipping")
            continue
        print(f"{label}: nested_links {len(current)} refs -> {len(target)} direct docs_article refs")
        entry["nested_links"] = [ref(u) for u in target]
        put_entry(headers, "links_2026", version_uid, entry, confirm)

    print("\nDone." if confirm else "\nDry run complete, no writes made. Re-run with --confirm to apply.")


if __name__ == "__main__":
    main()
