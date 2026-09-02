#!/usr/bin/env python3
"""Release bookkeeping for the CLI docs.

The URL restructure, deployed 2026-08-13. Order mattered: the docs release had to
land first, otherwise every redirect in the second release pointed at a URL that
did not exist yet.

  RELEASE_DOCS      the 73 CLI docs plus the non-CLI docs whose inbound links moved
  RELEASE_REDIRECTS the new and repaired server_redirects entries

The 2026-08-26 cleanup. Three releases, because they differ in where they deploy
and in what content type they carry. Deploy links first, then nav, then the V2
removal.

  RELEASE_CLEANUP_LINKS    broken links and anchors, plus the URL collision fix
  RELEASE_CLEANUP_NAV      nav placement and one legacy redirect
  RELEASE_CLEANUP_V2_SCAN  PRODUCTION ONLY, see its description

Read each release's description before deploying it. RELEASE_CLEANUP_V2_SCAN in
particular must not go to staging or development.

The write scripts import ensure_release() and add_item() rather than running this
file. Run it directly to print the current contents of every release.

Usage:
  python3 scripts/cli_release.py            # show every release and its items
  python3 scripts/cli_release.py --create   # create whichever release is missing
"""

import sys

from cli_docs_common import load_env, request

RELEASE_DOCS = "CLI docs URL restructure (V0/V1/V2) 2026-08-05 [docs]"
RELEASE_REDIRECTS = "Redirect cleanup - CLI URL restructure 2026-08-05 [docs]"

# Independent of the two restructure releases above and safe to deploy before them.
# Every item in it carries the URL scheme production serves today.
#
# SUPERSEDED, DO NOT DEPLOY. Its three items are pinned to versions that predate
# the URL restructure (v1, v7, v14), so deploying it now would revert two pages to
# their old URLs. Archive it. The work it was for is redone by the three releases
# below, against post-restructure versions.
RELEASE_ASSET_SCANNING = "CLI asset scanning: GA page + V2 rollback 2026-08-06 [docs]"

# The 2026-08-26 cleanup. Three releases rather than one, because they do not all
# deploy to the same environments and they do not all carry the same content type.
RELEASE_CLEANUP_LINKS = "CLI 404 fixes + custom-commands URL 2026-08-26 [docs]"
RELEASE_CLEANUP_V2_SCAN = "CLI V2 asset scanning removal 2026-08-26 [docs]"
RELEASE_CLEANUP_NAV = "CLI nav + redirect cleanup 2026-08-26 [docs]"

# 2026-09-02. Retires Create Custom CLI Commands. Carries an unpublish item, which
# add_item cannot express, so retire_create_custom_cli_commands.py uses its own
# add_release_item helper that takes an action.
RELEASE_RETIRE_COMMANDS = "CLI retire create-custom-cli-commands 2026-09-02 [docs]"

# The full restructure, Waves A to E, staged by stage_wave_release.py.
RELEASE_FULL_RESTRUCTURE = "CLI docs full restructure (Waves A-E) 2026-09-02 [docs]"

DESCRIPTIONS = {
    RELEASE_DOCS: ("CLI docs moved to /v0, /v1 and unsuffixed-for-GA URLs, slugs "
                   "prefixed with cli- where missing, titles and SEO titles "
                   "relabelled V0.x.x / V1.x.x / V2.x.x, and CLI cross-links "
                   "repointed. Deploy this release BEFORE the redirect release."),
    RELEASE_REDIRECTS: ("Server redirects for the CLI URL restructure: 60 new "
                        "entries for the old URLs, plus repair of the legacy "
                        "/docs/developers/cli/* table. Deploy AFTER the CLI docs "
                        "URL restructure release."),
    RELEASE_ASSET_SCANNING: (
        "Asset scanning is GA for CLI V1 and not live for V2. Adds the new "
        "Asset Scanning in CLI page, which four live GA docs already link to, "
        "and rolls the two V2 Beta docs back to their last scan-free version. "
        "Independent of the URL restructure releases, deploy in any order."),
    RELEASE_CLEANUP_LINKS: (
        "DEPLOY TO ALL ENVIRONMENTS. Fixes every broken link and dead in-page "
        "anchor found across the CLI docs: Asset Scanning links repointed to /v1, "
        "a stale /docs/developers/cli/configure-regions link, and 13 dead anchors. "
        "Also moves the Create Custom CLI Commands page off the URL it shares with "
        "Create Custom CLI Plugins | V2.x.x, which makes the V2 Plugins page "
        "reachable again. Deploy this BEFORE the nav and redirect release."),
    RELEASE_CLEANUP_V2_SCAN: (
        "DEPLOY TO PRODUCTION ONLY. Do not deploy to staging or development.\n\n"
        "Asset scanning shipped for CLI V1 and has not shipped for V2, but V2 "
        "asset-scanning content is live on production. This removes it from the two "
        "V2 pages that carry it.\n\n"
        "Staging and development must keep serving the older versions that still "
        "contain the content (blt85d9deae08de968d v13, blt1215a1f9bbcc9900 v19), so "
        "that shipping V2 asset scanning later is a publish rather than a rewrite. "
        "Deploying this release to staging or development would destroy that copy.\n\n"
        "If it is deployed everywhere by mistake, recover with "
        "scripts/republish_v2_staging.py."),
    RELEASE_CLEANUP_NAV: (
        "DEPLOY TO ALL ENVIRONMENTS, and only after the 404 fixes release. Adds the "
        "Asset Scanning in CLI page to the Version 1.x.x > CLI Advanced Operations "
        "nav, which it was missing, and repoints the legacy create-custom-cli-commands "
        "redirect whose target 404s."),
    RELEASE_RETIRE_COMMANDS: (
        "DEPLOY TO ALL ENVIRONMENTS. Retires Create Custom CLI Commands "
        "(blt18f5edee45f9d6c2). Its step one is csdx plugins:create, a command that "
        "has never existed: @oclif/plugin-plugins ships only index, inspect, "
        "install, link, reset, uninstall and update, checked at majors 1, 2, 3 and "
        "5, and both CLI 1.68.0 and 2.0.0 depend on ^5.4.x. It also states Node 16 "
        "while serving the V2 tree, which needs 22, and shows csdx plugins: install "
        "with a stray space. Everything else it covers is in Create Custom CLI "
        "Plugins for Contentstack, whose V1 page sits directly above it in the same "
        "nav node. Three items: the Version 1.x.x > Miscellaneous nav node with the "
        "row removed, an UNPUBLISH of the article, and the legacy "
        "/docs/developers/cli/create-custom-cli-commands redirect retargeted from "
        "/create-custom-cli-commands/v1, which 404s today, to "
        "/create-custom-cli-plugins. The nav item must deploy at or before the "
        "unpublish, or the sidebar briefly points at an unpublished page. The "
        "shadow redirect blt154a351243ad4eda stays published and is deliberately "
        "not in this release: it is what keeps /create-custom-cli-commands "
        "resolving to the plugins guide instead of 404ing."),
    RELEASE_FULL_RESTRUCTURE: (
        "DEPLOY TO ALL ENVIRONMENTS, AS A UNIT. Carries the CLI docs restructure, "
        "Waves A to E, plus the corrected 2.0.0 changelog entry. Do not deploy a "
        "subset: these waves edit the same pages repeatedly, so a partial deploy "
        "leaves pages in a state no wave intended. Contents: 179 unlinkable H4 "
        "headings resolved, 32 Overview headings added over prose that already "
        "existed, 26 flag tables reshaped, section order and forbidden headings "
        "fixed, 25 Next Steps and 8 Examples sections added with every link "
        "verified over HTTP and every flag verified against the published 2.0.0 "
        "manifests, 4 Quick Reference index tables built from live anchor ids, and "
        "three accuracy fixes that matter to a reader: cm:stacks:migration's "
        "renamed config flags, 22 GitHub links pinned to a tag whose repo no "
        "longer holds that code, and a Node.js floor of 18.0.0 that was never the "
        "requirement for any release. Wave F, links and anchors, is deliberately "
        "NOT here: anchor ids are generated at render time, so it can only be "
        "verified after this release is live."),
}


def list_releases(headers):
    releases, skip = [], 0
    while True:
        data = request("GET", "/v3/releases", headers,
                       params={"limit": "100", "skip": str(skip),
                               "include_count": "true"})
        page = data.get("releases", [])
        releases.extend(page)
        if not page or len(releases) >= data.get("count", 0):
            return releases
        skip += 100


def find_release(headers, name):
    for release in list_releases(headers):
        if release.get("name") == name:
            return release
    return None


def ensure_release(headers, name, confirm=True):
    """Return the release uid for name, creating the release if it is missing.

    Refuses to reuse a locked release, since a locked release cannot take new
    items and silently skipping them would leave the production deploy incomplete.
    """
    existing = find_release(headers, name)
    if existing:
        if existing.get("locked"):
            sys.exit(f"Release {name!r} ({existing['uid']}) is locked. Unlock it or "
                     f"rename the constant in cli_release.py before continuing.")
        return existing["uid"]
    if not confirm:
        return None
    created = request("POST", "/v3/releases", headers, body={"release": {
        "name": name,
        "description": DESCRIPTIONS.get(name, ""),
        "locked": False,
        "archived": False,
    }})["release"]
    print(f"created release {name!r} -> {created['uid']}")
    return created["uid"]


def release_items(headers, release_uid, page_size=100):
    """Every item in a release.

    The endpoint returns at most 100 items per call and reports the real total in
    `count`, so this has to page. Reading only the first page silently under-counts
    a release once it passes 100 items, which makes both the idempotency check and
    the reconciliation report wrong.
    """
    items, skip = [], 0
    while True:
        data = request("GET", f"/v3/releases/{release_uid}/items", headers,
                       params={"include_count": "true", "limit": str(page_size),
                               "skip": str(skip)})
        page = data.get("items", [])
        items.extend(page)
        if not page or len(items) >= data.get("count", 0):
            return items
        skip += page_size


def item_key(item):
    return (item.get("content_type_uid"), item.get("uid"), item.get("locale"))


def add_item(headers, release_uid, content_type_uid, uid, version, locale="en-us",
             existing=None):
    """Add one entry version to a release. Returns "added", "updated" or "present".

    Pass existing (the dict returned by index_items) to skip a redundant POST when
    the same uid is already in the release at the same version, so a partial run
    can be resumed without duplicating work.
    """
    key = (content_type_uid, uid, locale)
    if existing is not None and key in existing:
        if existing[key] == version:
            return "present"
        outcome = "updated"
    else:
        outcome = "added"

    request("POST", f"/v3/releases/{release_uid}/item", headers, body={"item": {
        "version": version,
        "uid": uid,
        "content_type_uid": content_type_uid,
        "locale": locale,
        "action": "publish",
    }})
    if existing is not None:
        existing[key] = version
    return outcome


def index_items(headers, release_uid):
    """content_type/uid/locale -> version, for the items already in the release."""
    return {item_key(item): item.get("version")
            for item in release_items(headers, release_uid)}


def main():
    headers = load_env()
    create = "--create" in sys.argv

    for name in (RELEASE_DOCS, RELEASE_REDIRECTS, RELEASE_ASSET_SCANNING,
                 RELEASE_CLEANUP_LINKS, RELEASE_CLEANUP_V2_SCAN, RELEASE_CLEANUP_NAV):
        release = find_release(headers, name)
        if not release:
            if create:
                ensure_release(headers, name)
                continue
            print(f"{name!r}\n   MISSING (pass --create to create it)\n")
            continue

        items = release_items(headers, release["uid"])
        errored = [i for i in items if i.get("errors")]
        by_type = {}
        for item in items:
            by_type[item["content_type_uid"]] = by_type.get(item["content_type_uid"], 0) + 1
        deployed = [s for s in release.get("status") or []]
        print(f"{name!r}\n   uid      {release['uid']}"
              f"\n   locked   {release.get('locked')}"
              f"\n   items    {len(items)}  {by_type}"
              f"\n   errors   {len(errored)}"
              f"\n   deploys  {[(s.get('environment'), s.get('status')) for s in deployed]}\n")


if __name__ == "__main__":
    main()
