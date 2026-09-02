#!/usr/bin/env python3
"""Retire Create Custom CLI Commands, blt18f5edee45f9d6c2.

Why it is being retired rather than repaired. Its step one is:

    csdx plugins:create

That command has never existed. @oclif/plugin-plugins ships index, inspect,
install, link, reset, uninstall and update, and nothing else, checked against
the published tarballs at majors 1, 2, 3 and 5. CLI 1.68.0 and 2.0.0 both depend
on ^5.4.x, so no CLI release in either major has ever had it. It was most likely
the old oclif generator's command, never csdx's. Two more defects sit alongside
it: `Node.js version 16 or above`, on an entry that also serves the V2 tree
where 22 is required, and `csdx plugins: install` with a stray space.

Nothing is lost. The rest of the page is plugins:link, plugins:uninstall,
plugins and bin/run, all covered by Create Custom CLI Plugins for Contentstack
under `Plugin Registration and Linking` and `Managing Installed Plugins`. Its
single nav row sits directly below the V1 plugins guide in the same Miscellaneous
node, so the replacement is already in front of the reader. No CLI doc links to
it in prose, checked across all 82.

The page is invisible today only because a redirect hides it, so this is less of
a change than it looks. blt154a351243ad4eda sends
/headless-cms/create-custom-cli-commands to the plugins guide.

THIS SUPERSEDES scripts/fix_create_custom_cli_commands_url.py --redirects. That
step exists to unpublish the shadow redirect and reveal this page. Revealing it
would ship `plugins:create` to readers. Do not run it.

Environments. Staging and development are written directly, which is this
project's convention and what PUBLISH_ENV_UIDS encodes. Production goes into
RELEASE_RETIRE_COMMANDS for a human to deploy, so nothing on the live site
changes when this script runs.

One note on the redirect. RELEASE_CLEANUP_NAV already contained
blt0d2ab10c0fa412a8 at v3 and has deployed, yet the redirect still targets
/create-custom-cli-commands/v1 and still 404s. The release published v3
unchanged, because the content edit was never made. Write 3 below makes it.

Usage:
  python3 scripts/retire_create_custom_cli_commands.py            # dry run
  python3 scripts/retire_create_custom_cli_commands.py --confirm  # write
"""

import sys

from cli_docs_common import (DEVELOPMENT_ENV_UID, DOCS_ARTICLE, LOCALE, PROD_ENV_UID,
                             PUBLISH_ENV_UIDS, SERVER_REDIRECTS, STAGING_ENV_UID,
                             get_entry, load_env, publish_entry, put_entry, request,
                             unpublish_entry)
from cli_release import RELEASE_RETIRE_COMMANDS, ensure_release, index_items

NAV_TYPE = "links_2026"

ARTICLE = "blt18f5edee45f9d6c2"          # Create Custom CLI Commands
NAV_NODE = "blt1b8dec46b8af7fdb"         # CLI > Version 1.x.x > Miscellaneous
LEGACY_REDIRECT = "blt0d2ab10c0fa412a8"  # /docs/developers/cli/create-custom-cli-commands
SHADOW_REDIRECT = "blt154a351243ad4eda"  # keeps the retired URL resolving

PLUGINS_V1 = "blt4f27fd89adf6b6c1"       # must stay in the nav, it is the replacement

ARTICLE_URL = "/headless-cms/create-custom-cli-commands"
REDIRECT_BAD_TO = "/docs/headless-cms/create-custom-cli-commands/v1"
REDIRECT_NEW_TO = "/docs/headless-cms/create-custom-cli-plugins"

OLD_PROD_ENV_UID = "blt18d21c1c300e766f"

ENV_NAMES = {PROD_ENV_UID: "production", STAGING_ENV_UID: "staging",
             DEVELOPMENT_ENV_UID: "development", OLD_PROD_ENV_UID: "old-production"}


def nav_entry(headers, uid):
    return request("GET", f"/v3/content_types/{NAV_TYPE}/entries/{uid}", headers,
                   params={"locale": LOCALE, "include_publish_details": "true"})["entry"]


def nav_put(headers, uid, entry):
    return request("PUT", f"/v3/content_types/{NAV_TYPE}/entries/{uid}", headers,
                   body={"entry": entry}, params={"locale": LOCALE})["entry"]


def nav_publish(headers, uid, version):
    request("POST", f"/v3/content_types/{NAV_TYPE}/entries/{uid}/publish", headers,
            body={"entry": {"environments": PUBLISH_ENV_UIDS, "locales": [LOCALE]},
                  "locale": LOCALE, "version": version})


def add_release_item(headers, release_uid, content_type_uid, uid, version,
                     action="publish"):
    """One release item, with an explicit action.

    cli_release.add_item hardcodes action publish, which cannot express the
    unpublish this retirement needs, so that helper is left alone rather than
    widened for one caller.
    """
    request("POST", f"/v3/releases/{release_uid}/item", headers, body={"item": {
        "version": version, "uid": uid, "content_type_uid": content_type_uid,
        "locale": LOCALE, "action": action,
    }})


def envs_of(entry):
    return [r["environment"] for r in (entry.get("publish_details") or [])
            if r.get("locale") == LOCALE]


def check_state(headers):
    """Read every object first and refuse to run on anything unexpected.

    Each guard names a specific way this retirement could be the wrong action,
    rather than just asserting a version number.
    """
    article = get_entry(headers, DOCS_ARTICLE, ARTICLE)
    if article.get("url") != ARTICLE_URL:
        sys.exit(f"{ARTICLE}: url is {article.get('url')!r}, expected {ARTICLE_URL!r}. "
                 f"Something has moved this entry. Refusing to retire it.")

    nav = nav_entry(headers, NAV_NODE)
    links = nav.get("nested_links") or []
    rows = [l for l in links if l.get("uid") == ARTICLE]
    if len(rows) != 1:
        sys.exit(f"{NAV_NODE}: expected exactly 1 row for {ARTICLE}, found "
                 f"{len(rows)}. The nav has changed. Refusing to edit it.")
    if not any(l.get("uid") == PLUGINS_V1 for l in links):
        sys.exit(f"{NAV_NODE}: the V1 plugins guide {PLUGINS_V1} is not in this nav "
                 f"node. It is the replacement for the page being retired, so "
                 f"removing this row would leave no plugin guide in the sidebar. "
                 f"Refusing to edit it.")

    redirect = get_entry(headers, SERVER_REDIRECTS, LEGACY_REDIRECT)
    if redirect.get("to") != REDIRECT_BAD_TO:
        sys.exit(f"{LEGACY_REDIRECT}: to is {redirect.get('to')!r}, expected "
                 f"{REDIRECT_BAD_TO!r}. Someone has already changed this redirect. "
                 f"Refusing to overwrite it.")

    shadow = get_entry(headers, SERVER_REDIRECTS, SHADOW_REDIRECT)
    if PROD_ENV_UID not in envs_of(shadow):
        sys.exit(f"{SHADOW_REDIRECT} is not published to production. It is what "
                 f"keeps {ARTICLE_URL} resolving to the plugins guide, so without "
                 f"it that URL would 404 once the article is unpublished. Refusing "
                 f"to continue.")

    return article, nav, redirect, shadow


def main():
    confirm = "--confirm" in sys.argv
    headers = load_env()
    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to write\n")

    article, nav, redirect, shadow = check_state(headers)

    print(f"article   {ARTICLE}  v{article['_version']}  {article.get('url')}")
    print(f"          published: "
          f"{', '.join(ENV_NAMES.get(e, e) for e in envs_of(article))}")
    print(f"nav       {NAV_NODE}  v{nav['_version']}  {nav.get('title')!r}  "
          f"{len(nav.get('nested_links') or [])} rows")
    print(f"redirect  {LEGACY_REDIRECT}  v{redirect['_version']}  "
          f"{redirect.get('from')}")
    print(f"          to  {redirect.get('to')}  (404 today)")
    print(f"shadow    {SHADOW_REDIRECT}  v{shadow['_version']}  left published, "
          f"deliberately not in the release")

    # old-production is a legacy environment carrying a much older version of this
    # entry. Nothing else in scripts/ writes to it, PUBLISH_ENV_UIDS excludes it,
    # and it is not the live site. Reported rather than touched, so the leftover is
    # a known one instead of a surprise.
    if OLD_PROD_ENV_UID in envs_of(article):
        stale = next(r["version"] for r in article["publish_details"]
                     if r["environment"] == OLD_PROD_ENV_UID
                     and r.get("locale") == LOCALE)
        print(f"\nnote      {ARTICLE} is also published to old-production at v{stale}. "
              f"Left alone,\n          as every other script here does. Retire it "
              f"there separately if that\n          environment still serves "
              f"anything.")
    print()

    if not confirm:
        print("Would do, in this order:")
        print(f"  1  remove the {ARTICLE} row from nav {NAV_NODE}, publish to "
              f"staging and development")
        print(f"  2  retarget {LEGACY_REDIRECT} to {REDIRECT_NEW_TO}, publish to "
              f"staging and development")
        print(f"  3  unpublish {ARTICLE} from staging and development")
        print(f"  4  stage all three for production in release "
              f"{RELEASE_RETIRE_COMMANDS!r}, the article as an unpublish item")
        print("\nNothing on production changes until that release is deployed.")
        print("Dry run complete. Nothing written.")
        return 0

    # 1. Nav first, so the sidebar never points at an unpublished page.
    nav["nested_links"] = [l for l in (nav.get("nested_links") or [])
                           if l.get("uid") != ARTICLE]
    nav_updated = nav_put(headers, NAV_NODE, nav)
    nav_publish(headers, NAV_NODE, nav_updated["_version"])
    print(f"1  nav {NAV_NODE} -> v{nav_updated['_version']}, "
          f"{len(nav_updated.get('nested_links') or [])} rows, published to "
          f"staging and development")

    # 2. Fix the redirect before the page goes, so the legacy URL is never worse
    #    off than it is now.
    redirect["to"] = REDIRECT_NEW_TO
    red_updated = put_entry(headers, SERVER_REDIRECTS, LEGACY_REDIRECT, redirect)
    publish_entry(headers, SERVER_REDIRECTS, LEGACY_REDIRECT,
                  red_updated["_version"])
    print(f"2  redirect {LEGACY_REDIRECT} -> v{red_updated['_version']}, now "
          f"{REDIRECT_NEW_TO}, published to staging and development")

    # 3. Unpublish, not delete. Reversible by publishing the same version again.
    unpublish_entry(headers, DOCS_ARTICLE, ARTICLE, article["_version"])
    print(f"3  article {ARTICLE} v{article['_version']} unpublished from staging "
          f"and development")

    # 4. Production, queued for a human to deploy.
    release = ensure_release(headers, RELEASE_RETIRE_COMMANDS)
    existing = index_items(headers, release)
    print(f"4  release {release}  ({len(existing)} items already present)")
    for ct, uid, version, action in [
        (NAV_TYPE, NAV_NODE, nav_updated["_version"], "publish"),
        (SERVER_REDIRECTS, LEGACY_REDIRECT, red_updated["_version"], "publish"),
        (DOCS_ARTICLE, ARTICLE, article["_version"], "unpublish"),
    ]:
        try:
            add_release_item(headers, release, ct, uid, version, action)
            print(f"     {action:9s} {ct:17s} {uid} v{version}")
        except Exception as exc:
            print(f"     FAILED {action} {ct} {uid} v{version}: {exc}")
            print(f"     Add this item by hand in the release UI. Staging and "
                  f"development are already correct, so only the production "
                  f"staging of this one item is missing.")

    print(f"\nProduction is unchanged. Deploy {RELEASE_RETIRE_COMMANDS!r} to apply it.")
    print("Then refresh the local mirror: python3 scripts/fetch_cli_docs.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
