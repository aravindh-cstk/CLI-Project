#!/usr/bin/env python3
"""Status-check every link in every CLI doc, against what an environment serves.

Read-only. This generalises verify_asset_scanning_live.py's check_links(), which
only looks at links inside asset-scanning passages, to every href in all 92 CLI
entries.

Two things worth knowing about how it checks:

  * Content comes from the exact version the chosen environment serves, taken
    from the entry's publish_details record, not from the draft and not from the
    local docs/json mirror. A draft ahead of the environment would otherwise
    report links that nobody can click yet.
  * Same-page anchors are resolved against the RENDERED page, not against
    article_section.content. Heading ids are generated at render time and do not
    appear in the stored HTML, so matching anchors against the stored content
    reports almost every anchor as broken.

npm returns 403 to anything that does not look like a browser. Those are
reported separately rather than as breakage.

Usage:
  python3 scripts/sweep_cli_links.py
  python3 scripts/sweep_cli_links.py --env staging
  python3 scripts/sweep_cli_links.py --skip-anchors
"""

import concurrent.futures as cf
import json
import re
import sys
import urllib.error
import urllib.request

from cli_docs_common import (DEVELOPMENT_ENV_UID, DOCS_ARTICLE, INDEX_PATH, LOCALE,
                             PROD_ENV_UID, STAGING_ENV_UID, article_section,
                             get_entry, load_env, staging_auth_header)
from verify_cli_url_restructure import http_status

ENVIRONMENTS = {
    "prod": (PROD_ENV_UID, "https://www.contentstack.com"),
    "staging": (STAGING_ENV_UID, "https://stag-www.contentstack.com"),
    "development": (DEVELOPMENT_ENV_UID, "https://dev-www.contentstack.com"),
}

HREF = re.compile(r'href="([^"]+)"', re.I)
ID = re.compile(r'\bid="([^"]+)"', re.I)

# Hosts that reject non-browser requests. Reported, not counted as broken.
BOT_BLOCKED = ("npmjs.com", "www.npmjs.com")


def env_version(entry, env_uid):
    for record in entry.get("publish_details") or []:
        if record.get("environment") == env_uid and record.get("locale") == LOCALE:
            return record.get("version")
    return None


def fetch(headers, meta, env_uid):
    """Return (meta, served entry, version) for one index entry, or a None entry."""
    draft = get_entry(headers, DOCS_ARTICLE, meta["uid"])
    version = env_version(draft, env_uid)
    if version is None:
        return meta, None, None
    served = draft if version == draft.get("_version") else get_entry(
        headers, DOCS_ARTICLE, meta["uid"], version=version)
    return meta, served, version


def get_html(url, auth=None):
    """Rendered page HTML, or None if it could not be fetched."""
    request_headers = {"User-Agent": "Mozilla/5.0"}
    if auth:
        request_headers["Authorization"] = auth
    try:
        req = urllib.request.Request(url, headers=request_headers)
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read().decode("utf-8", "replace")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return None


def main():
    argv = sys.argv[1:]
    env = "prod"
    if "--env" in argv:
        env = argv[argv.index("--env") + 1]
    if env not in ENVIRONMENTS:
        sys.exit(f"--env must be one of {', '.join(ENVIRONMENTS)}")
    env_uid, host = ENVIRONMENTS[env]
    auth = staging_auth_header() if env != "prod" else None
    check_anchors = "--skip-anchors" not in argv

    headers = load_env()
    with open(INDEX_PATH, encoding="utf-8") as fh:
        index = json.load(fh)["entries"]

    print(f"Sweeping {len(index)} CLI entries as served by {env} ({host})\n")

    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(lambda m: fetch(headers, m, env_uid), index))

    unpublished = [meta for meta, served, _ in rows if served is None]
    for meta in unpublished:
        print(f"  NOT PUBLISHED TO {env.upper()}  {meta['uid']}  {meta['title']}")
    if unpublished:
        print()

    # url -> [(folder, title)], and (page url, anchor) -> [titles]
    outbound, anchors, page_of = {}, {}, {}
    for meta, served, _ in rows:
        if served is None:
            continue
        html = article_section(served).get("content") or ""
        page = (served.get("url") or "").rstrip("/")
        page_of[meta["uid"]] = page
        where = ("/".join(meta.get("folder") or []), meta["title"])
        for href in set(HREF.findall(html)):
            if href.startswith("#"):
                anchors.setdefault((page, href), []).append(where)
            elif href.startswith("/") or href.startswith("http"):
                outbound.setdefault(href, []).append(where)

    print(f"{len(outbound)} distinct outbound links, "
          f"{len(anchors)} distinct same-page anchors\n")

    def probe(href):
        return href, http_status(href if href.startswith("http") else host + href, auth)

    with cf.ThreadPoolExecutor(max_workers=12) as pool:
        statuses = dict(pool.map(probe, outbound))

    broken, blocked = [], []
    for href, (code, location) in statuses.items():
        if code is None or code < 400:
            continue
        (blocked if any(h in href for h in BOT_BLOCKED) else broken).append(
            (code, href, location))

    print(f"=== BROKEN LINKS: {len(broken)} ===")
    for code, href, location in sorted(broken, key=lambda r: (-r[0], r[1])):
        print(f"{code}  {href}" + (f"  -> {location}" if location else ""))
        for folder, title in sorted(set(outbound[href])):
            print(f"        in {folder}  ::  {title}")
    if not broken:
        print("  none")

    if blocked:
        print(f"\n=== BLOCKED BY THE TARGET HOST, NOT BROKEN: {len(blocked)} ===")
        for code, href, _ in sorted(blocked):
            print(f"{code}  {href}")

    missing_anchors = []
    if check_anchors and anchors:
        pages = sorted({page for page, _ in anchors})
        print(f"\nFetching {len(pages)} rendered page(s) to resolve anchors")
        with cf.ThreadPoolExecutor(max_workers=8) as pool:
            rendered = dict(zip(pages, pool.map(
                lambda p: get_html(f"{host}/docs{p}", auth), pages)))
        for (page, anchor), wheres in anchors.items():
            html = rendered.get(page)
            if html is None:
                missing_anchors.append((page, anchor, "page could not be fetched"))
            elif anchor.lstrip("#") not in set(ID.findall(html)):
                missing_anchors.append((page, anchor, "no matching id on the page"))
        print(f"\n=== ANCHORS THAT DO NOT RESOLVE: {len(missing_anchors)} "
              f"of {len(anchors)} ===")
        for page, anchor, why in sorted(missing_anchors):
            print(f"  {page}{anchor}   ({why})")
        if not missing_anchors:
            print("  none")

    print(f"\n=== Summary ({env}) ===")
    print(f"  entries swept          {len(rows) - len(unpublished)}")
    print(f"  not published          {len(unpublished)}")
    print(f"  outbound links checked {len(outbound)}")
    print(f"  broken                 {len(broken)}")
    print(f"  blocked by host        {len(blocked)}")
    if check_anchors:
        print(f"  anchors unresolved     {len(missing_anchors)}")
    return 1 if broken or unpublished else 0


if __name__ == "__main__":
    sys.exit(main())
