#!/usr/bin/env python3
"""WI-6: find CLI docs that are live on production but absent from the left nav.

Read-only. Makes only GET calls. Writes one report file and nothing else.

Definition used here:
    orphan = a docs_article in CLI scope, published to production,
             that is not a leaf anywhere under the CLI nav root.

CLI scope reuses fetch_cli_docs.in_cli_scope: breadcrumb contains the CLI
navigation node, or the title carries the CLI prefix, or the uid is one of the
known-untracked plugin docs that sit outside the CLI breadcrumb.

Two traps this handles deliberately:
  * The nav shares references rather than copying them, so one article can be a
    leaf under more than one section. Dedupe by uid, never by nav row.
  * docs/json/index.json has 93 rows for 86 distinct uids for that same reason.
    This script does not read the index at all, it reads the live tree.

Usage:
  python3 scripts/cli_orphan_audit.py
  python3 scripts/cli_orphan_audit.py --out notes/reports/cli-orphan-report.md
"""

import os
import re
import sys
import urllib.request

from cli_docs_common import (DOCS_ARTICLE, PROD_ENV_UID, STAGING_ENV_UID,
                             is_published_to, list_entries, load_env)
from add_asset_scanning_to_nav import CLI_ROOT, leaves
from fetch_cli_docs import in_cli_scope

HOST = "https://www.contentstack.com"
UA = {"User-Agent": "Mozilla/5.0"}
ONLY = ("uid", "title", "url", "breadcrumb", "tags", "_version")


def http_code(url):
    try:
        req = urllib.request.Request(HOST + url, headers=UA, method="GET")
        return urllib.request.urlopen(req, timeout=120).getcode()
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception:
        return None


def main():
    out_path = None
    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]

    headers = load_env()

    print("walking the live CLI nav tree ...")
    nav = leaves(headers, CLI_ROOT)
    nav_uids = {uid for _path, uid in nav}
    paths_by_uid = {}
    for path, uid in nav:
        paths_by_uid.setdefault(uid, []).append(path)
    print(f"  {len(nav)} nav leaf rows, {len(nav_uids)} distinct articles")
    multi = {u: p for u, p in paths_by_uid.items() if len(p) > 1}
    print(f"  {len(multi)} articles referenced from more than one nav location")

    print("listing every docs_article and filtering to CLI scope ...")
    every = list_entries(headers, DOCS_ARTICLE, only=ONLY, progress=True)
    cli = [e for e in every if in_cli_scope(e)]
    print(f"  {len(every)} total articles, {len(cli)} in CLI scope")

    live = [e for e in cli if is_published_to(e, PROD_ENV_UID)]
    print(f"  {len(live)} of those are published to production")

    orphans = [e for e in live if e["uid"] not in nav_uids]
    in_nav_not_live = [uid for uid in nav_uids
                       if uid not in {e["uid"] for e in live}]
    unpublished_in_scope = [e for e in cli if not is_published_to(e, PROD_ENV_UID)]

    print(f"\n=== ORPHANS: {len(orphans)} ===")
    for e in sorted(orphans, key=lambda x: x.get("url") or ""):
        code = http_code("/docs" + (e.get("url") or ""))
        staging = is_published_to(e, STAGING_ENV_UID)
        print(f"  {e['uid']}  HTTP {code}  staging={staging}")
        print(f"      url   : {e.get('url')}")
        print(f"      title : {e.get('title')}")

    print(f"\n=== nav leaves NOT live on production: {len(in_nav_not_live)} ===")
    for uid in in_nav_not_live:
        print(f"  {uid}   nav path(s): {paths_by_uid.get(uid)}")

    print(f"\n=== in CLI scope but not published to production: {len(unpublished_in_scope)} ===")
    for e in unpublished_in_scope:
        print(f"  {e['uid']}  {e.get('url')}  {e.get('title')}")

    if out_path:
        write_report(out_path, orphans, nav, nav_uids, cli, live, multi,
                     paths_by_uid, in_nav_not_live, unpublished_in_scope)
        print(f"\nwrote {out_path}")


def write_report(path, orphans, nav, nav_uids, cli, live, multi, paths_by_uid,
                 in_nav_not_live, unpublished_in_scope):
    L = []
    A = L.append
    A("# CLI Orphan Page Report")
    A("")
    A("WI-6 of the CLI Structure Review. Read-only audit against the live CMS and production.")
    A("")
    A("**Definition used.** An orphan is a `docs_article` in CLI scope that is published to "
      "production but is not a leaf anywhere under the CLI navigation root "
      "(`links_2026` entry `bltd697fa2bc1e38b53`). A reader can reach it by search or by a "
      "cross-link from another page, but never by browsing the sidebar.")
    A("")
    A("## Counts")
    A("")
    A("| Measure | Count |")
    A("|---|---|")
    A(f"| Nav leaf rows under the CLI root | {len(nav)} |")
    A(f"| Distinct articles in the nav | {len(nav_uids)} |")
    A(f"| Articles referenced from more than one nav location | {len(multi)} |")
    A(f"| Articles in CLI scope | {len(cli)} |")
    A(f"| ... published to production | {len(live)} |")
    A(f"| ... in CLI scope but NOT on production | {len(unpublished_in_scope)} |")
    A(f"| **Orphans (live on production, absent from nav)** | **{len(orphans)}** |")
    A(f"| Nav leaves that are not live on production | {len(in_nav_not_live)} |")
    A("")
    A("The gap between nav leaf rows and distinct articles is expected. Contentstack nav "
      "references are shared rather than copied, so a version-agnostic doc appears as a leaf "
      "under both the V1 and the V2 tree. Everything below is deduped by uid.")
    A("")
    A("---")
    A("")
    A("## Orphans")
    A("")
    if not orphans:
        A("None. Every CLI doc that is live on production is reachable from the sidebar.")
    else:
        A("| UID | URL | Title | HTTP | On staging |")
        A("|---|---|---|---|---|")
        for e in sorted(orphans, key=lambda x: x.get("url") or ""):
            code = http_code("/docs" + (e.get("url") or ""))
            A("| `%s` | `%s` | %s | %s | %s |" % (
                e["uid"], e.get("url"),
                (e.get("title") or "").replace("|", "\\|"),
                code, is_published_to(e, STAGING_ENV_UID)))
    A("")
    A("---")
    A("")
    A("## Articles in the nav that are not live on production")
    A("")
    if not in_nav_not_live:
        A("None. Every sidebar link points at a page that production serves.")
    else:
        A("These are the inverse of an orphan: a sidebar entry whose target is not published, "
          "so the link is dead for a reader.")
        A("")
        A("| UID | Nav path |")
        A("|---|---|")
        for uid in in_nav_not_live:
            A("| `%s` | %s |" % (uid, "; ".join(
                p.replace("|", "\\|") for p in paths_by_uid.get(uid, []))))
    A("")
    A("---")
    A("")
    A("## In CLI scope but not published to production")
    A("")
    if not unpublished_in_scope:
        A("None.")
    else:
        A("| UID | URL | Title |")
        A("|---|---|---|")
        for e in unpublished_in_scope:
            A("| `%s` | `%s` | %s |" % (e["uid"], e.get("url"),
                                        (e.get("title") or "").replace("|", "\\|")))
    A("")
    A("---")
    A("")
    A("## Articles shared across both version trees")
    A("")
    A("Not defects, but they constrain any per-version edit: these are single CMS entries shown "
      "in two places, so they cannot be versioned independently and an edit to one is an edit to both.")
    A("")
    A("| UID | Nav paths |")
    A("|---|---|")
    for uid, ps in sorted(multi.items(), key=lambda kv: kv[1][0]):
        A("| `%s` | %s |" % (uid, "; ".join(p.replace("|", "\\|") for p in ps)))
    A("")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
