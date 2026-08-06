#!/usr/bin/env python3
"""Phase 5: retarget the 86 legacy /docs/developers/cli/* redirects.

Measured against production before writing this, rather than assumed:

  51 of the 86 work today. Their `to` omits the /docs prefix, which turned out to
     be harmless because the platform prepends it. Every one of them still points
     at a bare /headless-cms/{slug} URL though, so the restructure breaks them:
     that URL either moves to /v1 or changes slug.
  35 are already broken. 21 have a `to` of /headless-cms/beta or
     /headless-cms/old-commands, the residue of a script that kept only the last
     path segment. 14 name a slug that never existed.

So all 86 get retargeted, not just the broken ones, and every new `to` carries the
/docs prefix so the table stops relying on that fallback.

The target is derived from the `from` path, never from the existing broken `to`:

  /docs/developers/cli/{name}                -> the current GA doc for that topic
  /docs/developers/cli/{name}/beta           -> the V2 doc's new URL
  /docs/developers/cli/{name}/old-commands   -> the V0 doc's new URL

18 legacy names do not match any current slug and are resolved through
LEGACY_NAME_TO_SLUG. The dry run prints those separately for sign-off.

Usage:
  python3 scripts/retarget_legacy_cli_redirects.py            # dry run
  python3 scripts/retarget_legacy_cli_redirects.py --confirm  # update, publish, release
"""

import re
import sys
import time

import cli_release
import cli_url_map as url_map
from cli_docs_common import (LOCALE, SERVER_REDIRECTS, list_entries, load_env,
                             publish_entry, put_entry)

LEGACY_PREFIX = "/docs/developers/cli/"
LEGACY_PATH = re.compile(r"^/docs/developers/cli/([a-zA-Z0-9\-]+)"
                         r"(/beta|/old-commands)?/?$")

# Legacy page names with no matching current slug. Every one of these is a 404
# today, so there is no working target to preserve and the mapping is by intent.
LEGACY_NAME_TO_SLUG = {
    "authenticate-with-the-cli": "cli-authentication",
    "authentication": "cli-authentication",
    "bootstrap-starter-apps-using-the-cli": "bootstrap-starter-apps",
    "bulk-publish-and-unpublish": "bulk-publish-and-unpublish-content",
    "bulk-publish-and-unpublish-using-cli": "bulk-publish-and-unpublish-content",
    "clone-a-stack-using-the-cli": "cloning-a-stack",
    "configuration": "contentstack-cli-configuration-reference",
    "configure-the-cli": "contentstack-cli-configuration-reference",
    "create-custom-plugins-using-the-cli": "create-custom-cli-plugins",
    "export-content": "export-content-using-the-cli",
    "export-content-using-cli": "export-content-using-the-cli",
    "import-content": "import-content-using-the-cli",
    "import-content-using-cli": "import-content-using-the-cli",
    "installation": "install-the-cli",
    "migrate-content-from-html-rte-to-json-rte-using-the-cli":
        "migrate-content-from-html-rte-to-json-rte",
    "migrate-content-using-cli": "migrate-your-content-using-the-cli-migration-command",
    "migrate-your-content-using-the-cli-migration-plugin":
        "migrate-your-content-using-the-cli-migration-command",
    "migration": "migrate-your-content-using-the-cli-migration-command",
}

# Names whose mapping is a judgement call rather than an obvious rename. Surfaced
# in the dry run so a human signs them off before the live run.
NEEDS_SIGNOFF = {"configuration", "configure-the-cli", "migration",
                 "migrate-content-using-cli"}


def resolve(from_path, docs):
    """Return (target, slug, note) for one legacy path, or (None, None, reason)."""
    match = LEGACY_PATH.match(from_path)
    if not match:
        return None, None, "path does not match the legacy pattern"

    name, version = match.group(1), match.group(2) or ""
    slug = name if name in {d["slug"] for d in docs} else LEGACY_NAME_TO_SLUG.get(name)
    if not slug:
        return None, None, f"no slug mapping for {name!r}"

    available = url_map.by_slug(docs).get(slug) or {}
    note = ""
    if version == "/beta":
        doc = available.get("Beta")
        if not doc:
            note = "no V2 doc for this topic, sent to current GA instead"
    elif version == "/old-commands":
        doc = available.get("old")
        if not doc:
            note = "no V0 doc for this topic, sent to current GA instead"
    else:
        doc = None

    if doc:
        return f"/docs{doc['new_url']}", slug, note

    target = url_map.current_ga_url(docs, slug)
    if not target:
        return None, None, f"no doc found for slug {slug!r}"
    return f"/docs{target}", slug, note


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    docs = url_map.load_map()

    print(f"{'LIVE RUN' if confirm else 'DRY RUN (pass --confirm to write)'}\n")

    # _version is needed by the already-correct branch, which adds the live version
    # to the release without going through a PUT first.
    entries = [e for e in list_entries(headers, SERVER_REDIRECTS,
                                      only=("uid", "title", "from", "to",
                                            "is_permanent", "_version"))
               if (e.get("from") or "").startswith(LEGACY_PREFIX)]
    print(f"{len(entries)} legacy /docs/developers/cli/* redirect(s) found\n")

    live_pages = {f"/docs{d['new_url']}" for d in docs}

    plan, failures, signoff = [], [], []
    for entry in sorted(entries, key=lambda e: e["from"]):
        target, slug, note = resolve(entry["from"], docs)
        if target is None:
            failures.append((entry["from"], note))
            continue
        if target not in live_pages:
            failures.append((entry["from"], f"target {target} is not a CLI doc URL"))
            continue
        name = LEGACY_PATH.match(entry["from"]).group(1)
        if name in NEEDS_SIGNOFF:
            signoff.append((entry["from"], entry.get("to"), target))
        plan.append((entry, target, note))

    if failures:
        print("Unresolvable, fix LEGACY_NAME_TO_SLUG before the live run:")
        for from_path, why in failures:
            print(f"  {from_path}\n      {why}")
        sys.exit(f"\nFATAL: {len(failures)} legacy redirect(s) could not be resolved.")

    if signoff:
        print("Judgement-call mappings, please confirm these before the live run:")
        for from_path, old_to, target in signoff:
            print(f"  {from_path}")
            print(f"      current to={old_to}  (404 today)")
            print(f"      new     to={target}")
        print()

    changed, same = 0, 0
    release_uid, release_items = None, None
    if confirm:
        release_uid = cli_release.ensure_release(headers, cli_release.RELEASE_REDIRECTS)
        release_items = cli_release.index_items(headers, release_uid)

    for entry, target, note in plan:
        needs = entry.get("to") != target or entry.get("is_permanent") is not True
        suffix = f"   [{note}]" if note else ""
        if not needs:
            same += 1
            print(f"OK     {entry['from']} -> {target}{suffix}")
            if confirm:
                cli_release.add_item(headers, release_uid, SERVER_REDIRECTS,
                                     entry["uid"], entry["_version"], LOCALE,
                                     release_items)
            continue
        changed += 1
        print(f"UPDATE {entry['from']}{suffix}")
        print(f"    {entry.get('to')!r} -> {target!r}")
        if confirm:
            entry["to"] = target
            entry["is_permanent"] = True
            fresh = put_entry(headers, SERVER_REDIRECTS, entry["uid"], entry)
            publish_entry(headers, SERVER_REDIRECTS, entry["uid"], fresh["_version"])
            cli_release.add_item(headers, release_uid, SERVER_REDIRECTS,
                                 entry["uid"], fresh["_version"], LOCALE, release_items)
            print(f"    updated -> v{fresh['_version']}, published, added to release")
            time.sleep(0.2)

    print(f"\n{changed} to retarget, {same} already correct.")
    if confirm:
        print(f"\nRelease {release_uid}. Next: python3 scripts/fix_inbound_cli_links.py")
    else:
        print("\nDry run complete, no writes made.")


if __name__ == "__main__":
    main()
