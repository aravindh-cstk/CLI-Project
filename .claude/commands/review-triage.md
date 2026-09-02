# /review-triage

Triage review comments from gladys-cstk on a doc that has been pushed to origin. Classify each comment, decide whether it is valid, and either apply the fix, draft a reply explaining why it does not apply, or flag it for engineering. Also reconcile valid structural comments against `doc-standards/` so the same gap gets caught automatically next time.

**Usage:** `/review-triage <PR URL>`

The PR URL is where gladys-cstk left her review comments. If the doc's own path isn't obvious from the PR (for example the PR touches more than one doc), name the specific doc to triage, or Claude will ask.

If any comment references a feature that might live on a branch rather than `main`, name the branch if you know it. Otherwise Claude will ask before guessing.

---

## What this skill does

You work through gladys-cstk's comments on the PR at `$ARGUMENTS` in four steps. Do not skip steps, and do not silently apply a fix without stating its verdict first.

Two folders anchor every decision:
- `doc-standards/` holds the rules this org already enforces, and the scripts (`scripts/lint-doc.js`, `scripts/checks/*.js`, `scripts/data/rules-registry.json`) that check the mechanically checkable subset of them.
- `repo/` holds the actual product code. It contains `main`-branch folders (`cli-core`, `cli-plugins`, `cli-apps`, etc.) and numbered PR-branch folders (`cli-pr2646`, `cli-plugins-pr217`, `cli-plugins-pr294`). A feature a reviewer references may only exist in one of the PR folders, not on `main`.

---

## Step 1: Pull the review comments

`$ARGUMENTS` is a GitHub PR URL. Pull gladys-cstk's comments straight from GitHub with the `gh` CLI rather than asking the user to paste anything:

1. Parse the owner, repo, and PR number out of the URL.
2. Fetch both comment types, since GitHub splits them:
   - Inline (review) comments: `gh api repos/{owner}/{repo}/pulls/{number}/comments`
   - Top-level PR conversation comments: `gh api repos/{owner}/{repo}/issues/{number}/comments`
3. Filter to comments where the author is `gladys-cstk`. If none are found under that exact login, say so and ask the user for the correct login or to paste the comments directly, rather than silently triaging nothing.
4. For each inline comment, keep the file path, the line/diff hunk it's anchored to, and the comment body, that anchor tells you which doc and which passage the comment is actually about. Number the comments `1, 2, 3...` in the order returned.
5. If `gh` fails (not installed, not authenticated, PR not found), report the exact error to the user and fall back to asking them to paste the comments manually. Do not guess at comments you couldn't fetch.

Identify the target doc from the inline comments' file paths. If comments span more than one doc, either handle each doc as its own pass through Steps 2 to 4, or ask the user which doc to focus on first.

Read the target doc in full before proceeding.

---

## Step 2: Classify each comment

For every comment, decide:

- **Structural/cosmetic**: about wording, tone, formatting, section order, terminology, heading accuracy, or anything covered by `common-rules.md`'s B/C rules. Makes no claim about how the product actually behaves.
- **Technical**: makes or implies a claim about product behavior, such as a flag, command, API response, default value, or error condition, or anything a reader would rely on to be true.

If a comment mixes both (for example, "this section is out of order AND this flag doesn't exist"), split it into sub-comments and classify each half separately.

State the classification for every comment in one line before moving to Step 3. If a comment is genuinely ambiguous, ask the user rather than guessing which path to run it through.

---

## Step 3: Resolve each comment

### 3A: Structural/cosmetic path

For each comment on this path, work through in order:

**(a) Validity check.** A structural comment is valid only if both hold:
- *Reader benefit*: applying it measurably helps the reader (clearer, more scannable, more accurate), not just different.
- *Scope*: decide whether this is a rule that should apply to every doc of this type (or every doc, period), or whether it's specific to a quirk of this one doc. Both can still be valid, this distinction feeds Step 3A(d).

State the verdict (Valid or Not valid) and one sentence of reasoning.

**(b) If not valid:** do not edit the doc. Draft a reply for the user to paste back to gladys-cstk, in a plain, non-defensive, human tone. Explain the reasoning from (a), not "per company policy." One short paragraph, ready to paste as-is.

**(c) If valid:** apply the fix directly to the doc with the Edit tool. Note which lines changed.

**(d) Rule reconciliation.** Do this regardless of the (a) verdict. Even a rejected comment might point at a real gap, and an applied fix might reveal a rule that should exist.

Search `doc-standards/common-rules.md`, the matching doc-type file, and `doc-standards/scripts/data/rules-registry.json` for a rule that already covers this comment.

- **A matching rule already exists:**
  - If its `checkId` is non-null (tier 1 or 2, meant to be scriptable), this should have been caught by `lint-doc.js` before the doc was pushed. Open the check file named by that `checkId` in `doc-standards/scripts/checks/` and read its actual logic against this doc's text. Report the root cause in plain terms, for example: "the rule exists and is scripted, but the regex only matches a colon-terminated callout label, and this doc used a colon-less variant, so the check silently passed it." Propose the specific line to fix in the check file, but do not edit it without the user confirming. This script runs against every doc in the repo, not just this one.
  - If its `checkId` is null (tier 3, manual-only by design), say so and move on. This is expected: some rules require reading comprehension and were never meant to be scripted.
- **No matching rule exists:** draft a new rule row in the same shape as the existing entries in `rules-registry.json` (`id`, `source`, `docTypes`, `rule`, `why`, `exception`, `tier`, `checkId`), plus the matching plain-English line for `common-rules.md` or the doc-type file. Then judge whether it is *objectively, mechanically checkable* (a regex, a section-order check, a presence/absence check) versus something that needs judgment:
  - Mechanically checkable: tier 1 or 2, propose the actual check function (following the pattern in `doc-standards/scripts/checks/heuristic-flags.js`) and the one-line wiring into the `CHECKS` array in `lint-doc.js`.
  - Needs judgment: tier 3, `checkId: null`. No script to write.

Present every proposed rules-registry, script, or common-rules change as a **diff to review**, separate from the doc edits. Never write to any file under `doc-standards/scripts/` or edit `rules-registry.json` until the user explicitly says to. Those changes affect every doc that gets linted afterward, not just this one.

### 3B: Technical path

For each comment on this path:

**(a) Validity check against the repo.** Search `repo/` for the feature, flag, or behavior the comment references:
1. Check the relevant `main`-branch folder first (for example `repo/cli-core`, `repo/cli-plugins`, `repo/cli-apps`, whichever matches what the doc is documenting).
2. If not found on `main`, check the numbered PR-branch folders (`cli-pr2646`, `cli-plugins-pr217`, `cli-plugins-pr294`, and similar) for a branch that matches the doc's topic.
3. If you still can't find it, or the branch naming doesn't make the match obvious, stop and ask the user for the exact branch. Do not guess.

**(b) Outcomes:**
- **Not valid** (repo confirms the doc is already correct and the reviewer is mistaken): do not edit. Draft a reply citing the specific file and line in `repo/` as evidence, in the same plain human tone as 3A(b).
- **Valid, and confirmed in repo with high confidence:** apply the edit, and note which `repo/` file and line justified the change.
- **Valid, but not found in repo, or confidence is low:** do not edit and do not guess. Say explicitly that this needs engineering, and state the precise question to hand them (not just "is this true?" but the specific behavior that needs confirming).

---

## Step 4: Output

Report, in this order:

1. A table: comment # | classification | verdict | action (edited / replied / escalated).
2. All doc edits, already applied to the target doc by this point.
3. All drafted replies, grouped together, ready to post back on the PR at `$ARGUMENTS` (or paste manually if the user prefers to post them).
4. All escalation items, grouped together, each with the specific question for engineering.
5. Any proposed `doc-standards/` rule or script changes, shown as diffs, explicitly marked as **not yet applied**, waiting on user confirmation.

Do not post anything to the PR without the user's go-ahead. Fetching comments via `gh api` is read-only and safe to do automatically, but posting a reply is visible to gladys-cstk and the rest of the team, confirm with the user before running `gh api ... -X POST` (or `gh pr comment`) to actually post section 3's replies.
