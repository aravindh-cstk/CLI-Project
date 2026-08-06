#!/usr/bin/env python3
"""Report what the asset-scanning documentation actually looks like in production.

Read-only. This is the gate for the asset-scanning cleanup: the V1 (GA) feature is
live so its content stays and only its broken links get fixed, while V2 (Beta) is
not live so its content has to come off production.

For each entry it compares the current draft against the exact version production
is serving (the version recorded in the publish_details record for the production
environment), reports whether the asset-scanning markers are present in each, and
status-checks every link that appears inside the asset-scanning passages.

Usage:
  python3 scripts/verify_asset_scanning_live.py
  python3 scripts/verify_asset_scanning_live.py --http https://www.contentstack.com
"""

import concurrent.futures as cf
import re
import sys

from cli_docs_common import (DOCS_ARTICLE, LOCALE, PROD_ENV_UID, article_section,
                             get_entry, list_entries, load_env, staging_auth_header)
from verify_cli_url_restructure import http_status

# The GA/V1 entries keep their asset-scanning content, the Beta/V2 entries lose it.
GA_TARGETS = [
    ("GA bulk-publish-and-unpublish-content", "blt804647818d4181f9"),
    ("GA import-content-using-the-cli", "blt1ee86e6419f390f8"),
    ("GA cli-limitations", "blt74918691c8a465c1"),
    ("GA audit-plugin", "blt5bf8ffa6d7788728"),
]
BETA_TARGETS = [
    ("Beta bulk-operations-in-cli", "blt85d9deae08de968d"),
    ("Beta import-content-using-the-cli", "blt1215a1f9bbcc9900"),
]

MARKERS = ["scan status", "asset scanning", "--backup-dir", "--skip-assets-publish",
           "still scanning", "quarantin", "--dry-run", "asset-scanning-in-cli"]

# Blocks whose text mentions scanning. Used to decide which links are ours to fix.
BLOCK = re.compile(r"<(p|li|tr|h2|h3|h4|pre)\b[^>]*>.*?</\1>", re.S | re.I)
HREF = re.compile(r'href="([^"]+)"', re.I)

NEW_PAGE_SLUG = "asset-scanning-in-cli"


def markers_in(html):
    lowered = (html or "").lower()
    return {m: lowered.count(m) for m in MARKERS if m in lowered}


def prod_version(entry):
    for record in entry.get("publish_details") or []:
        if record.get("environment") == PROD_ENV_UID and record.get("locale") == LOCALE:
            return record.get("version")
    return None


def scan_blocks(html):
    """Every top-level block in the body whose text mentions asset scanning."""
    out = []
    for match in BLOCK.finditer(html or ""):
        block = match.group(0)
        if any(m in block.lower() for m in MARKERS):
            out.append(block)
    return out


def scan_hrefs(html):
    """Distinct hrefs that appear inside asset-scanning blocks, in document order."""
    seen, out = set(), []
    for block in scan_blocks(html):
        for href in HREF.findall(block):
            if href not in seen:
                seen.add(href)
                out.append(href)
    return out


def report_entry(headers, label, uid):
    draft = get_entry(headers, DOCS_ARTICLE, uid)
    version = prod_version(draft)
    if version is None:
        print(f"\n{label}  ({uid})")
        print("  NOT PUBLISHED TO PRODUCTION")
        return {"label": label, "uid": uid, "prod_version": None,
                "draft_version": draft.get("_version"), "prod_markers": {},
                "draft_markers": markers_in(article_section(draft).get("content")),
                "hrefs": [], "url": draft.get("url")}

    live = draft if version == draft.get("_version") else get_entry(
        headers, DOCS_ARTICLE, uid, version=version)

    prod_html = article_section(live).get("content") or ""
    draft_html = article_section(draft).get("content") or ""
    prod_markers = markers_in(prod_html)
    hrefs = scan_hrefs(prod_html)

    draft_version = draft.get("_version")
    drift = "" if version == draft_version else f"   (draft is v{draft_version})"

    print(f"\n{label}  ({uid})")
    print(f"  url             {live.get('url')}")
    print(f"  prod version    {version}{drift}")
    print(f"  scan content in production: "
          f"{'YES' if prod_markers else 'no'}"
          f"{'  ' + ', '.join(f'{k} x{v}' for k, v in prod_markers.items()) if prod_markers else ''}")
    if markers_in(draft_html) != prod_markers:
        print("  NOTE: the draft differs from production on these markers")
    if hrefs:
        print(f"  links inside the scan content ({len(hrefs)}):")
        for href in hrefs:
            print(f"      {href}")

    return {"label": label, "uid": uid, "prod_version": version,
            "draft_version": draft_version, "prod_markers": prod_markers,
            "draft_markers": markers_in(draft_html), "hrefs": hrefs,
            "url": live.get("url")}


def check_links(rows, host):
    """Status-check every scan-content link, resolving same-page anchors in place."""
    auth = staging_auth_header() if "stag" in host else None
    print(f"\nHTTP checks against {host}{' (with staging basic auth)' if auth else ''}")

    jobs = []
    for row in rows:
        for href in row["hrefs"]:
            if href.startswith("#"):
                jobs.append((row, href, None))          # resolved below, not fetched
            elif href.startswith("http"):
                jobs.append((row, href, href))
            elif href.startswith("/"):
                jobs.append((row, href, host + href))
            else:
                jobs.append((row, href, None))

    fetchable = [(row, href, url) for row, href, url in jobs if url]
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        statuses = list(pool.map(lambda job: http_status(job[2], auth), fetchable))

    problems = []
    for (row, href, _), (code, location) in zip(fetchable, statuses):
        if code != 200:
            problems.append(f"{row['label']}: {href} -> {code}"
                            + (f" ({location})" if location else ""))

    for row, href, url in jobs:
        if url is None and href.startswith("#"):
            problems.append(f"{row['label']}: same-page anchor {href}, "
                            f"verify the id exists on {row['url']}")

    if problems:
        print(f"  {len(problems)} link problem(s):")
        for item in problems:
            print(f"      {item}")
    else:
        print("  all scan-content links return 200")
    return problems


def main():
    headers = load_env()
    host = None
    if "--http" in sys.argv:
        host = sys.argv[sys.argv.index("--http") + 1].rstrip("/")

    print("=== Track A: GA / V1 entries (content stays, links get fixed) ===")
    ga_rows = [report_entry(headers, label, uid) for label, uid in GA_TARGETS]

    print("\n\n=== Track B: Beta / V2 entries (content comes off production) ===")
    beta_rows = [report_entry(headers, label, uid) for label, uid in BETA_TARGETS]

    print("\n\n=== Does the dedicated asset-scanning page exist yet? ===")
    existing = [e for e in list_entries(headers, DOCS_ARTICLE,
                                        only=("uid", "url", "title"))
                if NEW_PAGE_SLUG in (e.get("url") or "")]
    if existing:
        for entry in existing:
            print(f"  EXISTS  {entry.get('uid')}  {entry.get('url')}  {entry.get('title')}")
    else:
        print(f"  no docs_article has a url containing {NEW_PAGE_SLUG!r}, "
              f"so every link to it currently 404s")

    if host:
        check_links(ga_rows + beta_rows, host)

    print("\n\n=== Summary ===")
    for row in ga_rows + beta_rows:
        print(f"  {row['label']:<44} prod v{row['prod_version']}  "
              f"scan content: {'YES' if row['prod_markers'] else 'no'}")

    beta_dirty = [r for r in beta_rows if r["prod_markers"]]
    if beta_dirty:
        print(f"\n  Track B has work: {len(beta_dirty)} Beta entry(s) serve scan "
              f"content in production.")
    else:
        print("\n  Track B is a no-op: production carries no Beta scan content.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
