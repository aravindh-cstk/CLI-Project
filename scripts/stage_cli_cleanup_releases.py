#!/usr/bin/env python3
"""Bundle the 2026-08-26 CLI cleanup into releases for an approver to deploy.

Three releases, because they do not all deploy to the same environments and they
do not all carry the same content type.

  A  RELEASE_CLEANUP_LINKS    docs_article        deploy to all environments
  B  RELEASE_CLEANUP_V2_SCAN  docs_article        deploy to PRODUCTION ONLY
  C  RELEASE_CLEANUP_NAV      links_2026, server_redirects   all environments

Deploy order: A, then C, then B. A and C fix links, anchors and the nav. B then
removes the V2 asset-scanning content those links no longer point at.

Release B is the one to be careful with. Staging and development must keep serving
the versions that still contain the V2 asset-scanning content, so that shipping it
when V2 asset scanning launches is a publish rather than a rewrite. Deploying B to
staging or development destroys that copy. The release description says so, and
scripts/republish_v2_staging.py puts it back if it happens anyway.

Each item is pinned to the entry's current version, so run this after the fix
scripts, not before. Re-running is safe: add_item() skips an item already in the
release at the same version.

--archive-stale deals with a separate hazard. The 2026-08-06 release
"CLI asset scanning: GA page + V2 rollback" is unlocked, was never deployed, and
holds items pinned to versions that predate the URL restructure (v1, v7, v14).
Deploying it now would revert two pages to their old URLs. Archiving it takes it
out of reach.

Usage:
  python3 scripts/stage_cli_cleanup_releases.py --archive-stale
  python3 scripts/stage_cli_cleanup_releases.py --archive-stale --confirm
  python3 scripts/stage_cli_cleanup_releases.py --release A
  python3 scripts/stage_cli_cleanup_releases.py --release A --confirm
  python3 scripts/stage_cli_cleanup_releases.py --release all
"""

import sys

from cli_docs_common import (DOCS_ARTICLE, LOCALE, PROD_ENV_UID, SERVER_REDIRECTS,
                             get_entry, load_env, request)
from cli_release import (DESCRIPTIONS, RELEASE_ASSET_SCANNING, RELEASE_CLEANUP_LINKS,
                         RELEASE_CLEANUP_NAV, RELEASE_CLEANUP_V2_SCAN, add_item,
                         ensure_release, find_release, index_items, release_items)

NAV_TYPE = "links_2026"

# release key -> (release name, deploy note, [(content_type, uid, label), ...])
RELEASES = {
    "A": (RELEASE_CLEANUP_LINKS, "deploy to ALL environments", [
        (DOCS_ARTICLE, "blt1ee86e6419f390f8", "Import Content Using the CLI | V1.x.x"),
        (DOCS_ARTICLE, "blt74918691c8a465c1", "CLI Limitations | V1.x.x"),
        (DOCS_ARTICLE, "blt64294e11f81fe300", "Create Custom CLI Plugins | V2.x.x"),
        (DOCS_ARTICLE, "blt804647818d4181f9", "Bulk Publish and Unpublish Content | V1.x.x"),
        (DOCS_ARTICLE, "blt9f703f1d6c0405d9", "Import Content Using the Seed Command | V2.x.x"),
        (DOCS_ARTICLE, "bltd980d5d1a241b442", "Import Content Using the Seed Command | V1.x.x"),
        (DOCS_ARTICLE, "blt78f6b7d84156806f", "Import Content using the Seed Command | V0.x.x"),
        (DOCS_ARTICLE, "blt992979390532a894", "Migrate your Content using the CLI Migration Command | V2.x.x"),
        (DOCS_ARTICLE, "blt563cc44829432a89", "Migrate your Content using the CLI Migration Command | V1.x.x"),
        (DOCS_ARTICLE, "bltce91c490961bf924", "Migrate your Content using the CLI Migration Command | V0.x.x"),
        (DOCS_ARTICLE, "blt0a21fe8af5279f9d", "Export Content to .CSV File | V0.x.x"),
        (DOCS_ARTICLE, "bltcddcfb50d44a61db", "Migrate Content from HTML RTE to JSON RTE | V0.x.x"),
        (DOCS_ARTICLE, "blt6ee109a7b3725e1c", "Asset Scanning in CLI | V1.x.x (seo.title)"),
        (DOCS_ARTICLE, "blt18f5edee45f9d6c2", "Create Custom CLI Commands (url)"),
    ]),
    "B": (RELEASE_CLEANUP_V2_SCAN, "deploy to PRODUCTION ONLY", [
        (DOCS_ARTICLE, "blt85d9deae08de968d", "Bulk Operations in CLI | V2.x.x"),
        (DOCS_ARTICLE, "blt1215a1f9bbcc9900", "Import Content Using the CLI | V2.x.x"),
    ]),
    "C": (RELEASE_CLEANUP_NAV, "deploy to ALL environments, after release A", [
        (NAV_TYPE, "bltfc496d77b74a316b", "nav: Version 1.x.x > CLI Advanced Operations"),
        (SERVER_REDIRECTS, "blt0d2ab10c0fa412a8",
         "redirect: /docs/developers/cli/create-custom-cli-commands"),
    ]),
}

# Release B must not carry a version that staging or development is also on, or
# deploying it would take the content off those environments too.
PRODUCTION_ONLY = {"B"}


def entry_version(headers, content_type, uid):
    if content_type == NAV_TYPE:
        entry = request("GET", f"/v3/content_types/{NAV_TYPE}/entries/{uid}",
                        headers, params={"locale": LOCALE,
                                         "include_publish_details": "true"})["entry"]
    else:
        entry = get_entry(headers, content_type, uid)
    return entry


def stage(headers, key, confirm):
    name, note, items = RELEASES[key]
    print(f"=== Release {key}: {name}")
    print(f"    {note}\n")

    release_uid = ensure_release(headers, name, confirm=confirm)
    if not release_uid:
        print(f"    Release does not exist yet. Rerun with --confirm to create it.\n")
        existing = {}
    else:
        existing = index_items(headers, release_uid)

    for content_type, uid, label in items:
        entry = entry_version(headers, content_type, uid)
        version = entry["_version"]

        if key in PRODUCTION_ONLY:
            prod = next((r["version"] for r in (entry.get("publish_details") or [])
                         if r.get("environment") == PROD_ENV_UID
                         and r.get("locale") == LOCALE), None)
            if prod == version:
                print(f"    [already live] {uid}  v{version}  {label}")
                continue

        if not release_uid:
            print(f"    [DRY-RUN] {content_type}  {uid}  v{version}  {label}")
            continue

        if not confirm:
            state = ("present" if existing.get((content_type, uid, LOCALE)) == version
                     else "would add/update")
            print(f"    [DRY-RUN] {content_type}  {uid}  v{version}  {label}  ({state})")
            continue

        outcome = add_item(headers, release_uid, content_type, uid, version,
                           existing=existing)
        print(f"    [{outcome}] {content_type}  {uid}  v{version}  {label}")
    print()


def archive_stale(headers, confirm):
    """Archive the superseded 2026-08-06 asset-scanning release."""
    release = find_release(headers, RELEASE_ASSET_SCANNING)
    if not release:
        print(f"[unchanged] {RELEASE_ASSET_SCANNING!r} does not exist, nothing to do")
        return 0
    if release.get("archived"):
        print(f"[unchanged] already archived: {release['uid']}")
        return 0

    items = release_items(headers, release["uid"])
    deploys = release.get("status") or []
    print(f"[{'ARCHIVE' if confirm else 'DRY-RUN'}] {release['uid']}  "
          f"{RELEASE_ASSET_SCANNING}")
    print(f"      locked={release.get('locked')}  items={len(items)}  "
          f"deploys={len(deploys)}")
    for item in items:
        print(f"      pinned: {item.get('content_type_uid')} {item.get('uid')} "
              f"v{item.get('version')}")
    if deploys:
        print("      WARNING: this release has been deployed before. Check what it did "
              "before archiving.")
    print("      These versions predate the URL restructure. Deploying this release "
          "would revert two pages to their old URLs.")

    if not confirm:
        print("\nDry run complete, no writes made.")
        return 0

    try:
        request("PUT", f"/v3/releases/{release['uid']}", headers, body={"release": {
            "name": RELEASE_ASSET_SCANNING,
            "description": ("SUPERSEDED, DO NOT DEPLOY. Items are pinned to versions "
                            "that predate the 2026-08-13 URL restructure, so deploying "
                            "this would revert two pages to their old URLs. The work is "
                            "redone by the three 2026-08-26 cleanup releases. "
                            + DESCRIPTIONS.get(RELEASE_ASSET_SCANNING, "")),
            "archived": True,
            "locked": True,
        }})
        print(f"      archived and locked {release['uid']}")
    except SystemExit as exc:
        print(f"      COULD NOT archive: {exc}")
        print(f"      Archive it from the Contentstack UI instead. Until then, do not "
              f"deploy {RELEASE_ASSET_SCANNING!r}.")
        return 1
    return 0


def main():
    argv = sys.argv[1:]
    confirm = "--confirm" in argv

    if "--archive-stale" in argv:
        headers = load_env()
        print("LIVE RUN\n" if confirm else "DRY RUN (pass --confirm to write)\n")
        return archive_stale(headers, confirm)

    if "--release" not in argv:
        sys.exit("Pass --release A, B, C or all, or --archive-stale")
    which = argv[argv.index("--release") + 1].upper()
    keys = ["A", "C", "B"] if which == "ALL" else [which]
    for key in keys:
        if key not in RELEASES:
            sys.exit(f"Unknown release {key!r}. Use A, B, C or all.")

    headers = load_env()
    print("LIVE RUN\n" if confirm else "DRY RUN (pass --confirm to write)\n")
    for key in keys:
        stage(headers, key, confirm)

    print("An approver deploys these from the Contentstack UI. Publish rule "
          "blte4575c7c38862a50 requires sign-off for production, so a management "
          "token cannot publish there directly.")
    print("\nDeploy order: A, then C, then B.")
    print("Release B goes to PRODUCTION ONLY. Read its description first.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
