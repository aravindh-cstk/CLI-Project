# /publish-release-note

Publish a CLI release note (a `changelog_details` entry) to the Contentstack docs site from a rough draft, using `scripts/push_changelog_entry.py`. This command turns a plain-text or markdown draft into the CMS's HTML shape, previews it with a dry run, and only writes or publishes after the user confirms.

**Usage:** `/publish-release-note <rough draft text>`

If the draft doesn't clearly state a version number and a date, ask the user rather than guessing. Never assume "today" for the date.

---

## What this command does

You work through the draft at `$ARGUMENTS` in five steps. Do not skip steps, and never run `--write` or `--publish=` without the user's explicit go-ahead in Step 4.

Reference material:
- `scripts/push_changelog_entry.py` is the script that actually creates/updates and publishes the entry. Read it if you need to double check its flags or validation rules.
- `docs/json/changelog/2.x/` holds real, already-published entries. Use the most recent one as your formatting template for the `description` HTML (heading structure like `<p><strong>Enhancements:</strong></p><ul><li>...</li></ul>`, `<span class="code">...</span>` around flag/command names, package names bolded per bullet group).

---

## Step 1: Confirm prerequisites

Check that `.env` at the repo root contains `CONTENTSTACK_DOCS_STACK_API_KEY` and `CONTENTSTACK_DOCS_STACK_MANAGEMENT_TOKEN` (the two keys `scripts/cli_docs_common.py`'s `load_env()` requires). If either is missing, stop and tell the user. Don't run the script, since it will hard-exit anyway.

If `$ARGUMENTS` is empty, ask the user to paste the rough draft.

---

## Step 2: Draft the entry

Extract from the draft, or ask the user for, whatever is missing:
- **Title**: convention is `"CLI Version X.Y.Z"`.
- **Date**: `YYYY-MM-DD`.

Convert the rough draft body into RTE-style HTML for the `description` field. Sample the most recent file in `docs/json/changelog/2.x/` first and match its structure and tone exactly (section headers such as Breaking Changes / New Features / Enhancements / Bug & Security Fixes, per-package bullet groups, `<span class="code">` around command and flag names).

Build the full draft JSON:
```json
{
  "title": "CLI Version X.Y.Z",
  "date": "YYYY-MM-DD",
  "filters": [{ "uid": "blta9b77391ce974879", "_content_type_uid": "changelog_tags" }],
  "description": "<converted HTML>"
}
```

Ask the user whether this is a **new entry** or an **update to an existing one**. For an update, get the existing entry's `uid` (ask the user, or search `docs/json/changelog/` for a matching title) and add it to the JSON as `"uid"`.

Write the draft to a file in the session scratchpad directory (for example `release-note-draft.json`), not into the project. Show the user the title, date, and rendered description before moving on.

---

## Step 3: Dry run

Run the script with no `--write` and no `--publish=`:
```
python3 scripts/push_changelog_entry.py <scratchpad>/release-note-draft.json
```

Show the user the dry-run output verbatim. If validation fails (bad date format, missing description, wrong `filters` tag), fix the draft and dry-run again. Never move to Step 4 on a failing dry run.

---

## Step 4: Confirm and publish

Ask the user explicitly:
1. Create/update as an unpublished draft, or publish now?
2. If publishing, which environment(s): `staging`, `development`, `production`? Never assume `production`, it must be named by the user.

Only after they answer, re-run with `--write` and, if requested, `--publish=<envs>`.

---

## Step 5: Report

Report to the user:
1. Whether this was a create or update, and the resulting `uid`.
2. Which environment(s) it was published to, or "left as unpublished draft" if none.
3. That a full site refresh (`scripts/export_changelog_cli.py` then `scripts/changelog_json_to_markdown.py`) is a separate step if they also want the rendered Markdown changelog updated. This command does not run that automatically.
