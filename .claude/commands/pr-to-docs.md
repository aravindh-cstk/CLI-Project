# /pr-to-docs

Turn a Contentstack CLI pull request into staged documentation. This command reads the PR, agrees the scope with the user, drafts and lints the Markdown, converts the approved Markdown into the CMS's HTML, and publishes to **staging and development only**. It never touches production, and it never writes anything the user has not seen first.

**Usage:** `/pr-to-docs <PR URL or number>`

If `$ARGUMENTS` does not identify a PR, ask for the URL. If the PR spans more than one repository, ask which one. Otherwise Claude will ask before guessing.

---

## What this command does

You work through the PR at `$ARGUMENTS` in eight steps. Do not skip steps. There are three points where you stop and wait for the user: the scope document (Step 2), the drafted Markdown (Step 4), and the push itself (Step 6). Never run `--write`, `--confirm` or any publish without an explicit go-ahead at that step.

Reference material:

- `scripts/markdown_to_docs_html.py` converts approved Markdown back into `article_section` HTML. It rebuilds only the blocks whose Markdown changed and keeps every other block byte-identical. Run its `--selftest` if you have any reason to doubt it.
- `scripts/push_all_wave_changes.py` diffs local `docs/json` against the CMS and publishes to staging and development. Its word-loss guard is the corpus-level safety net.
- `scripts/create_cli_page.py` creates a new page in Contentstack from a local draft.
- `scripts/add_page_to_nav.py` appends a new page to a left-nav section.
- `scripts/cli_release.py` holds `ensure_release()` and `add_item()` for bundling entries into a release.
- `scripts/lib/docs_html.py` edits existing HTML in place, for the blocks the converter refuses.
- `doc-standards/cli-templates/` holds the four CLI doc templates and `cli-common-rules.md`.
- `docs/json/index.json` is the authoritative map of uid, title, folder, url, json path and markdown path. `cli-url-map.csv` is stale against the current folder layout, so prefer the index.

---

## Step 1: Confirm prerequisites

Check `.env` at the repo root for `CONTENTSTACK_DOCS_STACK_API_KEY` and `CONTENTSTACK_DOCS_STACK_MANAGEMENT_TOKEN`. If you will verify staging URLs later, also check `STAG_USERNAME` and `STAG_PASSWORD`, since staging is password-protected.

Check `gh auth status`.

If anything is missing, stop and report the exact error. Do not run the scripts, since they hard-exit anyway, and do not guess a value.

---

## Step 2: Read the PR

```
gh pr view <n> --json title,body,files,commits,url,state
gh pr diff <n>
```

Do not clone. If `gh` fails, report the exact error, then fall back to an existing clone under `repo/` and say in your output that you did so.

Extract only what a reader of the docs can see:

- commands and aliases that were added, renamed or removed
- flags that were added, renamed, given a new default, or deprecated
- changed prompts, console output and error messages
- changed prerequisites: auth, region, tokens, minimum versions
- behavior changes with no flag attached, such as a limit moving from 100 to 500

Drop refactors, tests, CI and dependency bumps.

Cross-check every flag claim against `notes/reports/flag-inventory.json`, which is built from the published npm manifests rather than the repo. If it looks stale, regenerate it with `python3 scripts/gen_flag_inventory.py --refetch`.

Note whether the PR is merged and released. If the code is merged but unreleased, say so, because the docs should then be staged and not published.

---

## Step 3: Write the scope document

Write `notes/reports/pr-<n>-scope.md` and show it to the user. It contains:

1. **Change table.** One row per change: what changed, is it user-visible, and why.
2. **Pages to update.** Resolve each through `docs/json/index.json`. Give the uid, the version folder, the local `.md` path and which template in `doc-standards/cli-templates/` the page follows.
3. **Pages to create.** Give a proposed URL, title, SEO title, template, and the nav section uid it belongs under. Find the section uid with `python3 scripts/add_page_to_nav.py --section <uid> --list` against a sibling's section, or by walking the tree from `CLI_ROOT`.
4. **Version pairing.** A change to a V2 page is checked against its V1 twin and the reverse. List the twin explicitly as in scope or out of scope, with a reason. Never silently update one side.
5. **Open questions.**

**Stop here.** The user confirms or corrects the list. Write no doc files until they do.

---

## Step 4: Draft and lint

For each approved page, edit the Markdown at `docs/markdown/<folder>/<file>.md`.

Follow the page's template in `doc-standards/cli-templates/`: `cli-command-reference.md`, `cli-task-runbook.md`, `cli-module-reference.md` or `cli-plugin-guide.md`, each layered on `cli-common-rules.md`. Two rules catch people out: CLI-C1 forbids H4 and deeper, because the renderer only emits anchor ids for H2 and H3, and CLI-C14 says to link the troubleshooting hub rather than documenting failure modes on the page.

Then lint each file until it is clean:

```
node doc-standards/scripts/lint-doc.js "docs/markdown/<path>.md" --type=<template-type>
```

Exit code 1 means error-severity findings. **Do not show the user a draft that has not passed the linter.** Flagged-for-review items are non-blocking, but mention them.

Two constraints the converter imposes on your writing, both of which the linter will not catch:

- A blockquote must start with `**Note:**`, `**Tip:**`, `**Warning:**` or `**Additional Resource:**`. Any other label is refused, because the CSS class cannot be guessed from it.
- Do not edit inside an `ol.step-sec` or a wrapper `div`. The converter refuses those, since rebuilding them would drop the wrapper and its class. If the change has to land there, edit the HTML directly with `scripts/lib/docs_html.py` and regenerate the Markdown with `python3 scripts/json_to_markdown.py`.

---

## Step 5: User review

Hand back:

- the local `.md` path for each page, as a clickable link
- one line per page on what changed
- the clean lint output, and any non-blocking flags

The user reads the files themselves.

Apply their feedback, re-lint, and present again. When a piece of feedback is a general rule rather than a one-off ("we never phrase it that way"), ask explicitly whether to change `doc-standards/cli-templates/` or add a lint check. If they say yes, hand off to `/doc-gap` rather than editing the standards inline. Never change a shared standard without being asked.

**Stop here** until the user approves the drafts.

---

## Step 6: Convert and dry-run the push

### 6A. Convert the Markdown into the CMS HTML

```
python3 scripts/markdown_to_docs_html.py "docs/markdown/<path>.md" [...]
```

This is a dry run. Show the user the per-page line: blocks touched out of blocks total, the byte delta, and any warning. Pay attention to two warnings:

- **heading text changed but its id was kept.** The anchor is now stale. Note it, and plan to run `scripts/cli_anchor_audit.py` in Step 8.
- **adjacent elements rebuilt as one.** Two neighbouring lists are being merged, because the approved Markdown describes them as one.

If it aborts, it writes nothing at all and prints a unified diff of the offending block. Fix the Markdown, or hand-edit that one block's HTML, and re-run.

On the user's go-ahead, re-run with `--write`.

### 6B. Dry-run the push

```
python3 scripts/push_all_wave_changes.py
```

Show the output verbatim. **Unexplained word loss stops the run.** Never add to `ALLOWED_REMOVALS` to get past it. Investigate instead: it usually means a section was dropped that the user did not intend to drop.

---

## Step 7: Push, create, nav, release

Each of the four needs its own explicit go-ahead. Do them in this order.

1. **Updated pages.**
   ```
   python3 scripts/push_all_wave_changes.py --confirm
   ```
   This PUTs each entry and publishes to staging and development. Production is never touched.

2. **New pages.** Two steps. First build the local draft, cloning the skeleton from a sibling in the same version folder so `breadcrumb`, `related_articles`, `next_and_prev_links`, `seo` and the display flags match its neighbours:
   ```
   python3 scripts/markdown_to_docs_html.py --new "docs/markdown/<path>.md" \
       --url /headless-cms/<slug> --template "<sibling json under docs/json>"
   ```
   Then create it, dry run first:
   ```
   python3 scripts/create_cli_page.py docs/json/drafts/<name>.json
   python3 scripts/create_cli_page.py docs/json/drafts/<name>.json --confirm
   ```
   This refuses to create a page whose internal links point at no known CLI doc, and publishes to staging and development only.

3. **Left nav, new pages only.**
   ```
   python3 scripts/add_page_to_nav.py --page <uid> --section <uid> --url <url> --env staging
   ```
   Dry run first. Show the user the section title and the position the leaf will take, then re-run with `--confirm`. The script refuses if the page is not published to the named environment, so run this after step 2, not before.

4. **Release.** Always bundle, even for a single entry, so the user has one ID to track.
   ```python
   from cli_release import ensure_release, add_item, index_items
   release = ensure_release(headers, "CLI docs for PR #<n>, <slug> <date> [docs]")
   ```
   Re-read each entry's version from the CMS rather than from `notes/reports/pushed-entries.json`. `scripts/stage_wave_release.py` records why: reading that file produced a silently incomplete release. Put the updated pages, any new pages and the nav entry into the same release.

---

## Step 8: Verify and report

Confirm each entry is actually being served on staging. `env_version(entry, STAGING_ENV_UID)` in `scripts/sweep_cli_links.py` reads this from `publish_details`.

If any heading was renamed or inserted, run `python3 scripts/cli_anchor_audit.py` against staging. Anchor ids are assigned at render time, and `docs_html.predict_anchor_id` documents why they cannot be computed offline.

Report:

1. Every affected entry: title, uid, new version, and whether it was updated or created.
2. The staging URL for each, as `https://stag-www.contentstack.com/docs<url>`. Mention that staging needs the Basic auth from `STAG_USERNAME` and `STAG_PASSWORD`.
3. The release name and release ID.
4. Any nav change made, naming the section.
5. Anything you left out of scope, and why.
6. That the user-facing release note is a separate step, `/publish-release-note`. This command does not write one.

Append a short record of the run to `notes/reports/`, in the style of the existing reports.

---

Reading the PR, resolving pages, drafting Markdown and every dry run are read-only and happen without asking. Creating an entry, updating an entry, publishing, changing the nav and creating a release are all visible outside this machine, so each one waits for the user to say go. If a step fails, report the exact error rather than working around it, and never disable a guard to make a script proceed.
