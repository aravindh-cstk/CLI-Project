#!/usr/bin/env python3
"""Export every production CLI doc from the Contentstack docs stack into docs/json/.

Scope is the union of two signals, then filtered to the production environment:
  * breadcrumb contains the "Command-line Interface (CLI)" navigation node
  * title starts with "[Contentstack Command-line Interface (CLI)]"

Each entry is written at the exact version that is live in production, read from
publish_details, so drafts ahead of production are ignored.
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter

REGION_HOST = "https://api.contentstack.io"
CONTENT_TYPE = "docs_article"
CLI_NAV_UID = "bltef82f5fd1a4eab6e"          # navigation entry: Command-line Interface (CLI)
PROD_ENV_UID = "bltfe8376c13fe85b9c"         # environment: production
LOCALE = "en-us"
TITLE_PREFIX = "[Contentstack Command-line Interface (CLI)]"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "docs", "json")
BUCKETS = ("GA", "Beta", "old")
EXPECTED = {"GA": 41, "Beta": 16, "old": 12}


def load_env():
    """Read the stack credentials out of .env without pulling in a dependency."""
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
    return {"api_key": api_key, "authorization": token}


def get(path, params, headers, attempts=4):
    """GET a CMA endpoint, retrying on rate limits and transient network errors."""
    url = f"{REGION_HOST}{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < attempts - 1:
                time.sleep(2 ** attempt)
                continue
            sys.exit(f"HTTP {exc.code} for {url}\n{exc.read().decode('utf-8', 'replace')[:500]}")
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < attempts - 1:
                time.sleep(2 ** attempt)
                continue
            sys.exit(f"Network error for {url}: {exc}")
    return None


def list_all_entries(headers):
    """Page through every docs_article entry, keeping only the fields needed to scope."""
    entries, skip = [], 0
    while True:
        params = [
            ("limit", "100"),
            ("skip", str(skip)),
            ("include_count", "true"),
            ("include_publish_details", "true"),
        ]
        for field in ("url", "title", "uid", "breadcrumb", "_version"):
            params.append(("only[BASE][]", field))
        data = get(f"/v3/content_types/{CONTENT_TYPE}/entries", params, headers)
        page = data.get("entries", [])
        entries.extend(page)
        total = data.get("count", 0)
        print(f"  listed {len(entries)}/{total}", file=sys.stderr)
        if not page or len(entries) >= total:
            return entries
        skip += 100


def prod_record(entry):
    """Return the production publish record for the master locale, if any."""
    for record in entry.get("publish_details") or []:
        if record.get("environment") == PROD_ENV_UID and record.get("locale") == LOCALE:
            return record
    return None


def in_cli_scope(entry):
    breadcrumb = entry.get("breadcrumb") or []
    if any(ref.get("uid") == CLI_NAV_UID for ref in breadcrumb):
        return True
    return (entry.get("title") or "").startswith(TITLE_PREFIX)


def bucket_and_slug(url):
    """GA keeps its own slug. Beta and old are named after the parent topic slug."""
    segments = [seg for seg in (url or "").strip("/").split("/") if seg]
    if not segments:
        return None, None
    last = segments[-1]
    if last == "old-commands":
        return "old", segments[-2]
    if last == "beta":
        return "Beta", segments[-2]
    return "GA", last


def main():
    headers = load_env()

    print("Listing docs_article entries...", file=sys.stderr)
    everything = list_all_entries(headers)

    selected = []
    for entry in everything:
        record = prod_record(entry)
        if record and in_cli_scope(entry):
            selected.append((entry, record))
    print(f"\n{len(everything)} entries total, {len(selected)} CLI entries live in production",
          file=sys.stderr)

    for bucket in BUCKETS:
        os.makedirs(os.path.join(OUT_DIR, bucket), exist_ok=True)

    manifest, counts, seen = [], Counter(), {}
    for index, (stub, record) in enumerate(sorted(selected, key=lambda x: x[0].get("url") or ""), 1):
        url = stub.get("url")
        bucket, slug = bucket_and_slug(url)
        if not slug:
            sys.exit(f"Could not derive a slug for {url}")
        key = (bucket, slug)
        if key in seen:
            sys.exit(f"Filename collision: {bucket}/{slug}.json wanted by {seen[key]} and {url}")
        seen[key] = url

        version = record["version"]
        data = get(
            f"/v3/content_types/{CONTENT_TYPE}/entries/{stub['uid']}",
            [("version", str(version)), ("include_publish_details", "true")],
            headers,
        )
        entry = data["entry"]
        if entry.get("_version") != version:
            sys.exit(f"{url}: asked for v{version}, got v{entry.get('_version')}")

        rel = os.path.join(bucket, f"{slug}.json")
        with open(os.path.join(OUT_DIR, rel), "w", encoding="utf-8") as fh:
            json.dump(entry, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

        counts[bucket] += 1
        manifest.append({
            "url": url,
            "uid": stub["uid"],
            "title": stub.get("title"),
            "bucket": bucket,
            "slug": slug,
            "production_version": version,
            "latest_version": stub.get("_version"),
            "published_at": record.get("time"),
            "json": rel.replace(os.sep, "/"),
            "markdown": f"{bucket}/{slug}.md",
        })
        print(f"  [{index}/{len(selected)}] {bucket}/{slug}.json  v{version}", file=sys.stderr)
        time.sleep(0.12)  # stay well under the CMA rate limit

    with open(os.path.join(OUT_DIR, "index.json"), "w", encoding="utf-8") as fh:
        json.dump({
            "stack_api_key": headers["api_key"],
            "content_type": CONTENT_TYPE,
            "environment": "production",
            "environment_uid": PROD_ENV_UID,
            "locale": LOCALE,
            "cli_navigation_uid": CLI_NAV_UID,
            "total": len(manifest),
            "counts": {bucket: counts[bucket] for bucket in BUCKETS},
            "entries": manifest,
        }, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    summary = " ".join(f"{bucket}={counts[bucket]}" for bucket in BUCKETS)
    print(f"\n{summary}, total {len(manifest)}")
    actual = {bucket: counts[bucket] for bucket in BUCKETS}
    if actual != EXPECTED:
        print(f"WARNING: expected {EXPECTED}, got {actual}", file=sys.stderr)
        return 1
    print(f"Wrote {len(manifest)} JSON files plus index.json to docs/json/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
