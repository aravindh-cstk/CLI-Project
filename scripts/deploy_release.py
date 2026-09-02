#!/usr/bin/env python3
"""Deploy a Contentstack release to named environments.

This is the one action in this repo that changes the live production site, so
it is deliberately its own script rather than a step inside a content script.

What it guards against, in order of how easily each one bites:

  * Deploying a release whose staged item versions no longer match the CMS. That
    is not hypothetical here: RELEASE_CLEANUP_NAV carried blt0d2ab10c0fa412a8 at
    v3 and deployed, but the content edit was never made, so it published v3
    unchanged and the legacy redirect kept 404ing for weeks. Every item version
    is re-read and compared before anything is sent.
  * Deploying an already locked release, which is a no-op that reads as success.
  * Deploying an empty release.

Mixed-action releases are supported. Each item carries its own publish or
unpublish action, which is how the retirement release removes a nav row and
unpublishes an article in one deploy.

Usage:
  python3 scripts/deploy_release.py <release_uid>                      # dry run
  python3 scripts/deploy_release.py <release_uid> --confirm            # deploy to production
  python3 scripts/deploy_release.py <release_uid> --env staging,development --confirm
"""

import sys

from cli_docs_common import (DEVELOPMENT_ENV_UID, LOCALE, PROD_ENV_UID,
                             STAGING_ENV_UID, load_env, request)
from cli_release import release_items

ENV_NAMES = {"production": PROD_ENV_UID, "staging": STAGING_ENV_UID,
             "development": DEVELOPMENT_ENV_UID}


def live_version(headers, content_type_uid, uid):
    """Current version of an entry, whatever its content type."""
    entry = request("GET", f"/v3/content_types/{content_type_uid}/entries/{uid}",
                    headers, params={"locale": LOCALE})["entry"]
    return entry["_version"]


def main():
    argv = sys.argv[1:]
    if not argv or argv[0].startswith("-"):
        sys.exit(__doc__)
    release_uid = argv[0]
    confirm = "--confirm" in argv
    envs = ["production"]
    if "--env" in argv:
        envs = [e.strip() for e in argv[argv.index("--env") + 1].split(",") if e.strip()]
    unknown = [e for e in envs if e not in ENV_NAMES]
    if unknown:
        sys.exit(f"Unknown environment(s) {unknown}. Choose from {list(ENV_NAMES)}.")

    headers = load_env()
    release = request("GET", f"/v3/releases/{release_uid}", headers)["release"]
    items = release_items(headers, release_uid)

    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to deploy\n")
    print(f"release  {release_uid}  {release.get('name')!r}")
    print(f"locked   {release.get('locked')}")
    print(f"deploy   -> {', '.join(envs)}   locale {LOCALE}\n")

    if release.get("locked"):
        sys.exit("This release is locked, which means it has already been deployed. "
                 "Deploying again would be a no-op that reads as success. Refusing.")
    if not items:
        sys.exit("This release has no items. Refusing to deploy nothing.")

    stale = []
    for item in items:
        ct, uid = item.get("content_type_uid"), item.get("uid")
        staged = item.get("version")
        try:
            current = live_version(headers, ct, uid)
        except Exception as exc:
            print(f"  {item.get('action'):9s} {ct:17s} {uid}  v{staged}  "
                  f"COULD NOT READ: {exc}")
            stale.append((uid, staged, "unreadable"))
            continue
        flag = "" if current == staged else f"  STALE, CMS is at v{current}"
        print(f"  {item.get('action'):9s} {ct:17s} {uid}  v{staged}{flag}")
        if current != staged:
            stale.append((uid, staged, current))

    if stale:
        print("\nStaged versions do not match the CMS:")
        for uid, staged, current in stale:
            print(f"  {uid}: release holds v{staged}, CMS has v{current}")
        print("\nDeploying would publish the staged version and silently discard the "
              "newer edit, which is exactly how the legacy redirect stayed broken. "
              "Re-stage the release against current versions first.")
        sys.exit(1)

    if not confirm:
        print("\nEvery staged version matches the CMS. Dry run complete, nothing deployed.")
        return 0

    body = {"release": {"environments": envs, "locales": [LOCALE]}}
    request("POST", f"/v3/releases/{release_uid}/deploy", headers, body=body)
    after = request("GET", f"/v3/releases/{release_uid}", headers)["release"]
    print(f"\nsubmitted. release locked: {after.get('locked')}")

    report_queue(headers, {i.get("uid") for i in items}, envs)
    return 0


def report_queue(headers, uids, envs):
    """Say what the deploy actually achieved, per item.

    A successful POST to /deploy does NOT mean the change is live. Production in
    this stack is approval gated, so items land as `pending_approval` and stay
    there until an approver acts. Saying "deployed" on the strength of the POST
    alone would be a false report, so the queue is read back and quoted.
    """
    queue = request("GET", "/v3/publish-queue", headers,
                    params={"limit": "30"}).get("queue", [])
    want = {ENV_NAMES[e] for e in envs}
    seen, pending = set(), []
    print("\nqueue status:")
    for job in queue:
        entry = job.get("entry") or {}
        uid = entry.get("uid")
        if uid not in uids or not want & set(job.get("environment") or []):
            continue
        key = (uid, job.get("action"))
        if key in seen:
            continue
        seen.add(key)
        details = job.get("publish_details") or {}
        status = details.get("status")
        print(f"  {job.get('action'):9s} {uid} v{entry.get('version')}  {status}")
        if status != "success":
            pending.append((uid, status, details.get("message") or ""))

    if pending:
        print("\nNOT LIVE YET. These items are queued but not applied:")
        for uid, status, message in pending:
            print(f"  {uid}  {status}  {message}")
        print("\nProduction in this stack requires publish approval, so a POST to "
              "/deploy only submits the request. An approver has to approve these "
              "in the Contentstack UI under Publish Queue before anything changes "
              "on the live site.")
    else:
        print("\nAll items applied.")


if __name__ == "__main__":
    sys.exit(main())
