#!/usr/bin/env python3
"""Create (or update) a single changelog_details entry in the Contentstack
Docs stack from a local draft JSON file, then optionally publish it.

This is the CLI-docs counterpart to SDK Project/scripts/push-changelog-entry.js,
tagged with the "CLI" changelog_tags entry instead of "SDKs" so it lands where
scripts/export_changelog_cli.py expects to find it.

Usage:
  python3 scripts/push_changelog_entry.py <draft.json> [--publish=staging,development] [--write]

  <draft.json>   a file shaped like the exported changelog entries:
                 { title, date, filters, description }. A "uid" key, if
                 present and not a "PENDING:" placeholder, switches this to an
                 update of that existing entry instead of a create.
  --publish=...  comma-separated environment names to publish to after the
                 create/update. Omit to create the entry as an unpublished
                 draft (some existing changelog entries live that way).
  --write        actually perform HTTP requests / file writes. Without this
                 flag the script only prints what it WOULD do (dry-run).

Safety: dry-run by default. Publishing to "production" puts the note on the
live docs site, so it is never implied -- it only happens if you name it.
"""

import json
import os
import re
import sys

from cli_docs_common import (
    LOCALE,
    ROOT,
    STAGING_ENV_UID,
    DEVELOPMENT_ENV_UID,
    PROD_ENV_UID,
    load_env,
    request,
)

CONTENT_TYPE = "changelog_details"
CLI_TAG_UID = "blta9b77391ce974879"  # changelog_tags entry: CLI

ENV_UIDS = {
    "staging": STAGING_ENV_UID,
    "development": DEVELOPMENT_ENV_UID,
    "production": PROD_ENV_UID,
}

# Read-only fields the CMA rejects (or ignores) on write.
SYSTEM_FIELDS = [
    "_version",
    "_content_type_uid",
    "ACL",
    "_in_progress",
    "created_at",
    "created_by",
    "updated_at",
    "updated_by",
    "publish_details",
]

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")

USAGE = ("Usage: python3 scripts/push_changelog_entry.py <draft.json> "
         "[--publish=staging,development] [--write]")


def parse_args(argv):
    draft_path = None
    write = False
    environments = []
    for arg in argv:
        if arg == "--write":
            write = True
        elif arg.startswith("--publish="):
            environments = [e.strip() for e in arg[len("--publish="):].split(",") if e.strip()]
        elif not arg.startswith("--"):
            draft_path = arg
        else:
            sys.exit(f'Unknown argument "{arg}".\n{USAGE}')
    if not draft_path:
        sys.exit(USAGE)
    return draft_path, write, environments


def is_real_uid(uid):
    return isinstance(uid, str) and len(uid) > 0 and not uid.startswith("PENDING:")


def validate(draft, draft_path):
    errors = []
    if not draft.get("title") or not isinstance(draft["title"], str):
        errors.append("title is required")
    if not DATE_RE.match(draft.get("date") or ""):
        errors.append("date must be YYYY-MM-DD")
    if not draft.get("description"):
        errors.append("description is required")
    filters = draft.get("filters") or []
    if not any(isinstance(f, dict) and f.get("uid") == CLI_TAG_UID for f in filters):
        errors.append(f'filters must include the "CLI" changelog tag ({CLI_TAG_UID})')
    if errors:
        print(f"Invalid draft {draft_path}:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)


def find_existing_by_title(headers, title):
    params = {"locale": LOCALE, "query": json.dumps({"title": title}), "only[BASE][]": "title"}
    body = request("GET", f"/v3/content_types/{CONTENT_TYPE}/entries", headers, params=params)
    return body.get("entries") or []


def resolve_env_uids(names):
    uids = []
    for name in names:
        uid = ENV_UIDS.get(name.lower())
        if not uid:
            sys.exit(f'Unknown environment "{name}". Known: {", ".join(ENV_UIDS)}')
        uids.append(uid)
    return uids


def main():
    draft_path, write, environments = parse_args(sys.argv[1:])

    with open(draft_path, encoding="utf-8") as fh:
        draft = json.load(fh)
    validate(draft, draft_path)

    headers = load_env()

    body = {k: v for k, v in draft.items() if k not in SYSTEM_FIELDS and k != "tags"}
    prefix = "" if write else "[dry-run] "
    uid = draft.get("uid")

    if is_real_uid(uid):
        body.pop("uid", None)
        print(f'{prefix}UPDATE {CONTENT_TYPE} {uid} "{draft["title"]}"')
        if write:
            request("PUT", f"/v3/content_types/{CONTENT_TYPE}/entries/{uid}",
                     headers, body={"entry": body}, params={"locale": LOCALE})
    else:
        duplicates = find_existing_by_title(headers, draft["title"])
        if duplicates:
            uids = ", ".join(e.get("uid") for e in duplicates)
            print(f'WARNING: {len(duplicates)} existing entry/entries already titled '
                  f'"{draft["title"]}" ({uids}). Add that uid to the draft to update '
                  f'instead of duplicating.', file=sys.stderr)
        body.pop("uid", None)
        print(f'{prefix}CREATE {CONTENT_TYPE} "{draft["title"]}" ({draft["date"]})')
        if write:
            created = request("POST", f"/v3/content_types/{CONTENT_TYPE}/entries",
                               headers, body={"entry": body}, params={"locale": LOCALE})
            uid = created["entry"]["uid"]
            with open(draft_path, "w", encoding="utf-8") as fh:
                json.dump({**draft, "uid": uid}, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
            print(f"  -> created {uid} (written back to {os.path.basename(draft_path)})")

    if environments:
        env_uids = resolve_env_uids(environments)
        print(f'{prefix}PUBLISH {CONTENT_TYPE} {uid or "<new uid>"} -> {", ".join(environments)}')
        if write:
            request("POST", f"/v3/content_types/{CONTENT_TYPE}/entries/{uid}/publish",
                     headers, body={"entry": {"environments": env_uids, "locales": [LOCALE]},
                                    "locale": LOCALE})
    else:
        print(f"{prefix}(no --publish given: entry stays an unpublished draft)")

    if not write:
        print("\nDry-run complete. No network requests or file writes were made. "
              "Re-run with --write to apply.")


if __name__ == "__main__":
    main()
