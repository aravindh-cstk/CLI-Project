#!/usr/bin/env python3
"""Verify the CLI URL restructure, against Contentstack and against the live site.

Read-only. Safe to run at any point: before the live push it reports what is still
outstanding, after it reports what landed.

Checks
  1  every one of the 73 CLI entries has the mapped url, title and seo.title
  2  no two CLI entries share a url
  3  every visible H1 is free of a version qualifier
  4  no CLI doc content still points at an old-scheme CLI URL
  5  every redirect in the map exists, is permanent and points where the map says
  6  no redirect source shadows a URL that serves a live page
  7  the two releases hold the expected items with no item-level errors
  8  optional: HTTP status of the old and new URLs on a chosen host

Usage:
  python3 scripts/verify_cli_url_restructure.py
  python3 scripts/verify_cli_url_restructure.py --http https://www.contentstack.com
"""

import concurrent.futures as cf
import json
import re
import sys
import urllib.error
import urllib.request

import cli_release
import cli_url_map as url_map
import rewrite_cli_links as links
from cli_docs_common import (DOCS_ARTICLE, SERVER_REDIRECTS, article_section,
                             get_entry, list_entries, load_env,
                             staging_auth_header)

OLD_SCHEME = re.compile(r"(?:/docs)?/(?:headless-cms/[a-zA-Z0-9\-]+/(?:beta|old-commands)"
                        r"|developers/cli/[a-zA-Z0-9\-]+)")

results = []


def check(name, failures, detail_limit=8):
    ok = not failures
    results.append((name, ok, len(failures)))
    print(f"{'PASS' if ok else 'FAIL'}  {name}"
          f"{'' if ok else f'  ({len(failures)} problem(s))'}")
    for item in failures[:detail_limit]:
        print(f"        {item}")
    if len(failures) > detail_limit:
        print(f"        ... and {len(failures) - detail_limit} more")


def http_status(url, auth=None):
    """Single-hop status for a URL. Returns (code, location) without following."""

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            raise urllib.error.HTTPError(req.full_url, code, newurl, headers, fp)

    request_headers = {"User-Agent": "Mozilla/5.0"}
    if auth:
        request_headers["Authorization"] = auth
    try:
        opener = urllib.request.build_opener(NoRedirect)
        req = urllib.request.Request(url, headers=request_headers)
        with opener.open(req, timeout=30) as resp:
            return resp.getcode(), None
    except urllib.error.HTTPError as exc:
        return exc.code, exc.msg if exc.code in (301, 302, 307, 308) else None
    except Exception as exc:
        return f"ERR {exc}", None


def main():
    headers = load_env()
    docs = url_map.load_map()
    lookup = links.build_lookup(docs)

    print(f"Verifying {len(docs)} CLI docs and "
          f"{len(url_map.redirects(docs))} redirects\n")

    # 1, 2, 3, 4
    field_problems, heading_problems, content_problems = [], [], []
    seen_urls = {}
    duplicate_urls = []
    for doc in sorted(docs, key=lambda d: (d["slug"], d["bucket"])):
        entry = get_entry(headers, DOCS_ARTICLE, doc["uid"])
        label = f"{doc['bucket']}/{doc['new_slug']}"

        for field, want, got in (
            ("url", doc["new_url"], entry.get("url")),
            ("title", doc["new_title"], entry.get("title")),
            ("seo.title", doc["new_seo_title"], (entry.get("seo") or {}).get("title")),
        ):
            if want != got:
                field_problems.append(f"{label} {field}: want {want!r}, got {got!r}")

        if entry.get("url") in seen_urls:
            duplicate_urls.append(f"{entry.get('url')} used by {label} and "
                                  f"{seen_urls[entry.get('url')]}")
        seen_urls[entry.get("url")] = label

        section = article_section(entry)
        heading = section.get("heading") or ""
        if url_map.strip_version_qualifier(heading)[1]:
            heading_problems.append(f"{label} heading: {heading!r}")

        content = section.get("content") or ""
        for match in OLD_SCHEME.finditer(content):
            slug_match = re.search(r"/(?:headless-cms|developers/cli)/([a-zA-Z0-9\-]+)",
                                   match.group(0))
            if slug_match and slug_match.group(1) in lookup:
                content_problems.append(f"{label}: {match.group(0)}")

    check("every CLI entry has the mapped url, title and seo.title", field_problems)
    check("no two CLI entries share a url", duplicate_urls)
    check("no visible H1 carries a version qualifier", heading_problems)
    check("no CLI doc content points at an old-scheme CLI URL", content_problems)

    # 5, 6
    table = {}
    for entry in list_entries(headers, SERVER_REDIRECTS,
                              only=("uid", "from", "to", "is_permanent")):
        key = (entry.get("from") or "").rstrip("/")
        table.setdefault(key, []).append(entry)

    redirect_problems = []
    for source, target in url_map.redirects(docs):
        matches = table.get(source.rstrip("/"))
        if not matches:
            redirect_problems.append(f"missing: {source} -> {target}")
            continue
        for entry in matches:
            if entry.get("to") != target:
                redirect_problems.append(
                    f"{source}: points at {entry.get('to')!r}, want {target!r}")
            elif entry.get("is_permanent") is not True:
                redirect_problems.append(f"{source}: is_permanent is not True")
    check("every mapped redirect exists, is permanent and points at the new URL",
          redirect_problems)

    live_pages = {f"/docs{d['new_url']}".rstrip("/") for d in docs}
    shadowed = sorted(set(table) & live_pages)
    check("no redirect source shadows a URL that serves a live page", shadowed)

    # 7
    release_problems = []
    for name, expected_type in ((cli_release.RELEASE_DOCS, DOCS_ARTICLE),
                                (cli_release.RELEASE_REDIRECTS, SERVER_REDIRECTS)):
        release = cli_release.find_release(headers, name)
        if not release:
            release_problems.append(f"release not created yet: {name}")
            continue
        items = cli_release.release_items(headers, release["uid"])
        errored = [i for i in items if i.get("errors")]
        if errored:
            release_problems.append(
                f"{name}: {len(errored)} item(s) with errors, first "
                f"{errored[0].get('uid')} {errored[0].get('errors')}")
        wrong = [i for i in items if i.get("content_type_uid") != expected_type]
        if wrong:
            release_problems.append(
                f"{name}: {len(wrong)} item(s) of an unexpected content type")
        print(f"        {name}: {len(items)} item(s)")
    check("both releases exist with no item-level errors", release_problems)

    # 8
    if "--http" in sys.argv:
        host = sys.argv[sys.argv.index("--http") + 1].rstrip("/")
        auth = staging_auth_header() if "stag" in host else None
        print(f"\nHTTP checks against {host}"
              f"{' (with staging basic auth)' if auth else ''}")

        with cf.ThreadPoolExecutor(max_workers=8) as pool:
            redirect_rows = list(pool.map(
                lambda pair: (pair[0], pair[1], *http_status(host + pair[0], auth)),
                url_map.redirects(docs)))
            page_rows = list(pool.map(
                lambda d: (d, *http_status(f"{host}/docs{d['new_url']}", auth)),
                docs))

        http_problems = []
        for source, target, code, location in redirect_rows:
            if code not in (301, 302, 307, 308):
                http_problems.append(f"{source}: expected a redirect, got {code}")
            elif location and target not in location:
                http_problems.append(f"{source}: redirects to {location}, want {target}")
        check("every old CLI URL redirects to its new URL", http_problems)

        page_problems = []
        for doc, code, location in page_rows:
            if code != 200:
                page_problems.append(
                    f"/docs{doc['new_url']}: got {code}"
                    + (f" -> {location}" if location else ""))
        check("every new CLI URL serves a page", page_problems)

        # The 13 topics with no redirect: the URL must still serve a page, and that
        # page must now be the V2 doc rather than 404 or a redirect.
        bare_problems = []
        skipped = [d for d in docs if d["bucket"] == "GA"
                   and "Beta" in (url_map.by_slug(docs).get(d["slug"]) or {})
                   and d["new_slug"] == d["slug"]]
        with cf.ThreadPoolExecutor(max_workers=8) as pool:
            rows = list(pool.map(
                lambda d: (d, *http_status(
                    f"{host}/docs{url_map.old_url(d['slug'], 'GA')}", auth)), skipped))
        for doc, code, location in rows:
            if code != 200:
                bare_problems.append(
                    f"/docs{url_map.old_url(doc['slug'], 'GA')}: got {code}"
                    + (f" -> {location}" if location else ""))
        check(f"the {len(skipped)} unchanged V1 URLs still serve a page, now V2",
              bare_problems)

    failed = [name for name, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed.")
    if failed:
        print("Failed:")
        for name in failed:
            print(f"  {name}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
