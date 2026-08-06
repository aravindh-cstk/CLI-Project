#!/usr/bin/env python3
"""Release bookkeeping for the CLI URL restructure.

Two releases carry this change to production, and the deploy order matters. The
docs release has to land first, otherwise every redirect in the second release
points at a URL that does not exist yet.

  RELEASE_DOCS      the 73 CLI docs plus the non-CLI docs whose inbound links move
  RELEASE_REDIRECTS the new and repaired server_redirects entries

The write scripts import ensure_release() and add_item() rather than running this
file. Run it directly to print the current contents of both releases.

Usage:
  python3 scripts/cli_release.py            # show both releases and their items
  python3 scripts/cli_release.py --create   # create whichever release is missing
"""

import sys

from cli_docs_common import load_env, request

RELEASE_DOCS = "CLI docs URL restructure (V0/V1/V2) 2026-08-05 [docs]"
RELEASE_REDIRECTS = "Redirect cleanup - CLI URL restructure 2026-08-05 [docs]"

DESCRIPTIONS = {
    RELEASE_DOCS: ("CLI docs moved to /v0, /v1 and unsuffixed-for-GA URLs, slugs "
                   "prefixed with cli- where missing, titles and SEO titles "
                   "relabelled V0.x.x / V1.x.x / V2.x.x, and CLI cross-links "
                   "repointed. Deploy this release BEFORE the redirect release."),
    RELEASE_REDIRECTS: ("Server redirects for the CLI URL restructure: 60 new "
                        "entries for the old URLs, plus repair of the legacy "
                        "/docs/developers/cli/* table. Deploy AFTER the CLI docs "
                        "URL restructure release."),
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

    for name in (RELEASE_DOCS, RELEASE_REDIRECTS):
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
