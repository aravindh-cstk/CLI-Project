#!/usr/bin/env python3
"""Give the Create Custom CLI Commands page its own URL again.

    --urls       DONE. Ran and deployed. The entry sits at
                 /headless-cms/create-custom-cli-commands.

    --redirects  SUPERSEDED, DO NOT RUN. See below.

Superseded on 2026-09-02 by scripts/retire_create_custom_cli_commands.py.

--redirects exists to unpublish the shadow redirect and make this page reachable.
It must not run, because the page should not be reachable: its step one is
`csdx plugins:create`, a command that has never existed. @oclif/plugin-plugins
ships index, inspect, install, link, reset, uninstall and update and nothing
else, verified against the published tarballs at majors 1, 2, 3 and 5, and both
CLI 1.68.0 and 2.0.0 depend on ^5.4.x. Revealing the page would ship a
non-existent command as the first instruction a plugin author reads. It also
states Node 16 while serving the V2 tree, which requires 22.

The page is being retired instead. Everything it covers beyond `plugins:create`
is already in Create Custom CLI Plugins for Contentstack. The shadow redirect
blt154a351243ad4eda stays published, which is what keeps the URL resolving to
that guide rather than 404ing.

The code below is left intact rather than deleted, so the original reasoning and
the ordering constraints stay readable.

Two docs_article entries currently claim the same URL, and both are published to
production:

  blt18f5edee45f9d6c2  Create Custom CLI Commands            /headless-cms/create-custom-cli-plugins
  blt64294e11f81fe300  Create Custom CLI Plugins | V2.x.x    /headless-cms/create-custom-cli-plugins

Only one can be served, so one page is unreachable. The Commands entry is the one
in the wrong place: cli-url-map.csv and docs/json/index.json both say it belongs
at /headless-cms/create-custom-cli-commands. It has no working URL of its own
today, because a redirect sends that URL to the plugins page and
/create-custom-cli-commands/v1 404s.

Ordering matters, so the work is split into two steps run at different times:

  --urls        Move the Commands entry to /headless-cms/create-custom-cli-commands.
                Goes into release A. On its own this already fixes the collision:
                /create-custom-cli-plugins starts unambiguously serving the V2
                Plugins page. /create-custom-cli-commands keeps redirecting for
                now, so nothing 404s in the meantime.

  --redirects   Run only AFTER release A has deployed. Stops the redirect that
                shadows /create-custom-cli-commands, and repoints the legacy
                /docs/developers/cli/create-custom-cli-commands redirect, whose
                current target 404s.

Running it the other way round would leave /create-custom-cli-commands with no
redirect and no page for as long as release A sits undeployed.

The shadowing redirect is unpublished, not deleted, so it can be put back by
publishing it again.

Usage:
  python3 scripts/fix_create_custom_cli_commands_url.py --urls
  python3 scripts/fix_create_custom_cli_commands_url.py --urls --confirm
  python3 scripts/fix_create_custom_cli_commands_url.py --redirects
  python3 scripts/fix_create_custom_cli_commands_url.py --redirects --confirm
"""

import sys

from cli_docs_common import (DEVELOPMENT_ENV_UID, DOCS_ARTICLE, LOCALE, PROD_ENV_UID,
                             PUBLISH_ENV_UIDS, SERVER_REDIRECTS, STAGING_ENV_UID,
                             get_entry, list_entries, load_env, publish_entry,
                             put_entry, request, unpublish_entry)

COMMANDS_UID = "blt18f5edee45f9d6c2"
COMMANDS_WRONG_URL = "/headless-cms/create-custom-cli-plugins"
COMMANDS_RIGHT_URL = "/headless-cms/create-custom-cli-commands"

PLUGINS_V2_UID = "blt64294e11f81fe300"

# The redirect that shadows COMMANDS_RIGHT_URL. Unpublished, not deleted.
SHADOW_REDIRECT = "blt154a351243ad4eda"

# Legacy redirect whose target 404s: Commands is version agnostic, so there is no
# /v1 form of its URL.
RETARGET = [("blt0d2ab10c0fa412a8",
             "/docs/headless-cms/create-custom-cli-commands/v1",
             "/docs/headless-cms/create-custom-cli-commands")]

ENV_NAMES = {PROD_ENV_UID: "production", STAGING_ENV_UID: "staging",
             DEVELOPMENT_ENV_UID: "development"}


def published_envs(entry):
    return [r["environment"] for r in (entry.get("publish_details") or [])
            if r.get("locale") == LOCALE]


def do_urls(headers, confirm):
    entry = get_entry(headers, DOCS_ARTICLE, COMMANDS_UID)
    current = entry.get("url")

    if current == COMMANDS_RIGHT_URL:
        print(f"[unchanged] {COMMANDS_UID} is already at {COMMANDS_RIGHT_URL}")
        return 0
    if current != COMMANDS_WRONG_URL:
        sys.exit(f"{COMMANDS_UID}: url is {current!r}, expected {COMMANDS_WRONG_URL!r}. "
                 f"Something else has moved this entry. Refusing to write.")

    # Confirm the collision is real before moving anything.
    plugins = get_entry(headers, DOCS_ARTICLE, PLUGINS_V2_UID)
    if plugins.get("url") != COMMANDS_WRONG_URL:
        sys.exit(f"{PLUGINS_V2_UID}: url is {plugins.get('url')!r}, not "
                 f"{COMMANDS_WRONG_URL!r}. There is no collision to resolve, so moving "
                 f"the Commands entry may not be the right fix. Refusing to write.")

    # Nothing else may already sit on the destination URL.
    clash = [e for e in list_entries(headers, DOCS_ARTICLE, only=("uid", "url", "title"))
             if (e.get("url") or "").rstrip("/") == COMMANDS_RIGHT_URL.rstrip("/")
             and e.get("uid") != COMMANDS_UID]
    if clash:
        sys.exit(f"{COMMANDS_RIGHT_URL} is already taken by "
                 f"{clash[0]['uid']} ({clash[0].get('title')}). Refusing to write.")

    print(f"[{'FIX' if confirm else 'DRY-RUN'}] {COMMANDS_UID}  v{entry['_version']}  "
          f"{entry.get('title')}")
    print(f"      url  {current}\n        ->  {COMMANDS_RIGHT_URL}")
    print(f"      frees {COMMANDS_WRONG_URL} for {PLUGINS_V2_UID} "
          f"(Create Custom CLI Plugins | V2.x.x), which is unreachable today")

    if not confirm:
        print("\nDry run complete, no writes made.")
        return 0

    entry["url"] = COMMANDS_RIGHT_URL
    updated = put_entry(headers, DOCS_ARTICLE, COMMANDS_UID, entry)
    publish_entry(headers, DOCS_ARTICLE, COMMANDS_UID, updated["_version"])
    print(f"      wrote v{updated['_version']}, published to staging and development")
    print("\nNext: python3 scripts/stage_cli_cleanup_releases.py --release A")
    print("Then, once release A has deployed: "
          "python3 scripts/fix_create_custom_cli_commands_url.py --redirects --confirm")
    return 0


def do_redirects(headers, confirm):
    # Superseded. This would reveal a page whose first instruction is
    # `csdx plugins:create`, a command that has never shipped in any CLI major.
    # See the module docstring. A docstring alone is not a guard, so this refuses
    # outright rather than relying on someone having read it.
    if "--i-know-this-is-superseded" not in sys.argv:
        sys.exit(
            "--redirects is SUPERSEDED and must not run.\n\n"
            "It unpublishes the shadow redirect to make Create Custom CLI Commands "
            "reachable. That page documents `csdx plugins:create`, which does not "
            "exist and never has. It is being retired instead, by\n"
            "  scripts/retire_create_custom_cli_commands.py\n\n"
            "If you genuinely need the old behaviour, re-read the module docstring "
            "first, then pass --i-know-this-is-superseded.")

    # Guard the ordering: the page must already be at its new URL on production.
    entry = get_entry(headers, DOCS_ARTICLE, COMMANDS_UID)
    prod = next((r for r in (entry.get("publish_details") or [])
                 if r.get("environment") == PROD_ENV_UID and r.get("locale") == LOCALE),
                None)
    if entry.get("url") != COMMANDS_RIGHT_URL:
        sys.exit(f"{COMMANDS_UID} is still at {entry.get('url')!r}. Run --urls first.")
    if prod is None or prod["version"] != entry["_version"]:
        served = "nothing" if prod is None else f"v{prod['version']}"
        sys.exit(f"Production serves {served} of {COMMANDS_UID} but the URL change is "
                 f"v{entry['_version']}. Deploy release A before removing the redirect, "
                 f"or {COMMANDS_RIGHT_URL} will 404.")

    shadow = get_entry(headers, SERVER_REDIRECTS, SHADOW_REDIRECT)
    envs = published_envs(shadow)
    print(f"[{'FIX' if confirm else 'DRY-RUN'}] {SHADOW_REDIRECT}  "
          f"v{shadow['_version']}  shadowing redirect")
    print(f"      {shadow.get('from')}  ->  {shadow.get('to')}")
    print(f"      unpublish from: "
          f"{', '.join(ENV_NAMES.get(e, e) for e in envs) or 'nowhere'}")

    for uid, want_from, want_to in RETARGET:
        red = get_entry(headers, SERVER_REDIRECTS, uid)
        if red.get("to") == want_to:
            print(f"[unchanged] {uid}  already points at {want_to}")
            continue
        if red.get("to") != want_from:
            print(f"[SKIP] {uid}  points at {red.get('to')!r}, expected {want_from!r}")
            continue
        print(f"[{'FIX' if confirm else 'DRY-RUN'}] {uid}  v{red['_version']}")
        print(f"      {red.get('from')}\n      to  {red.get('to')}  ->  {want_to}")

    if not confirm:
        print("\nDry run complete, no writes made.")
        return 0

    for env in envs:
        try:
            unpublish_entry(headers, SERVER_REDIRECTS, SHADOW_REDIRECT,
                            shadow["_version"], env_uids=[env])
            print(f"      unpublished {SHADOW_REDIRECT} from {ENV_NAMES.get(env, env)}")
        except SystemExit as exc:
            print(f"      COULD NOT unpublish from {ENV_NAMES.get(env, env)}: {exc}")
            print(f"      Do it from the Contentstack UI, or add an unpublish item for "
                  f"{SHADOW_REDIRECT} to release C.")

    for uid, want_from, want_to in RETARGET:
        red = get_entry(headers, SERVER_REDIRECTS, uid)
        if red.get("to") != want_from:
            continue
        red["to"] = want_to
        updated = put_entry(headers, SERVER_REDIRECTS, uid, red)
        publish_entry(headers, SERVER_REDIRECTS, uid, updated["_version"],
                      env_uids=PUBLISH_ENV_UIDS)
        print(f"      {uid} now points at {want_to}, "
              f"published v{updated['_version']} to staging and development")

    print("\nNext: python3 scripts/stage_cli_cleanup_releases.py --release C")
    return 0


def main():
    argv = sys.argv[1:]
    confirm = "--confirm" in argv
    headers = load_env()
    print("LIVE RUN\n" if confirm else "DRY RUN (pass --confirm to write)\n")

    if "--urls" in argv:
        return do_urls(headers, confirm)
    if "--redirects" in argv:
        return do_redirects(headers, confirm)
    sys.exit("Pass --urls or --redirects. See the module docstring for the ordering.")


if __name__ == "__main__":
    sys.exit(main())
