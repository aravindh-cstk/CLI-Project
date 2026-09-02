# Proposed Amendments to `doc-standards/migration-guide.md`

Status: **proposal only.** Nothing in `doc-standards/` has been edited. These four gaps surfaced while
triaging an external review of `v2-migration-guide-command-based.md`. Each one is a case where the guide
had a real weakness that the current standard did not require anyone to fix.

---

## 1. Broaden the Quick Decision Guide trigger

**Current rule.** Section 4 of the section-order table marks Quick Decision Guide as required only
"If multiple migration paths exist".

**Problem.** A single-path migration can still be large. The CLI V1 to V2 guide runs past 1,700 lines and
covers more than 25 commands on one path, so the current trigger did not fire. A reader had no way to
tell whether the migration affected them until they had read most of the document.

**Proposed rule.** Require the Quick Decision Guide when any of these is true:

- More than one migration path exists (current trigger, unchanged).
- The guide exceeds roughly 500 lines.
- The guide covers more than roughly 5 commands, endpoints, or public types.

**Why:** at that size the reader's first question stops being "which path?" and becomes "does this affect
me at all?". Both questions are answered by the same table.

---

## 2. Require the checklist to state its ordering principle

**Current rule.** The Pre-Upgrade Checklist must be an ordered list of discrete, anchor-linked actions.

**Problem.** The rule governs the items but not the sequence. A reader cannot tell whether item 1 comes
first because it is most urgent, because it is chronologically first, or for no reason at all. The CLI
guide happens to say "This checklist orders items by risk", which is exactly the missing information, but
nothing in the standard required that sentence.

**Proposed rule.** The Pre-Upgrade Checklist opens with one sentence naming its ordering principle (risk,
execution order, or dependency order).

---

## 3. Separate behavioral changes from syntactic ones

**Current rule.** None. The standard requires a Before block and an After block per subsection, which
treats a flag rename and a silent data-loss change identically.

**Problem.** These are not equivalent. "`--data` is now `--data-dir`" fails loudly and is fixed in
seconds. "Export no longer creates branch subfolders" silently destroys the previous branch's data.
In the CLI guide both rendered as sibling H4 headings under the same command.

**Proposed rule.** Within a command or API subsection:

- Behavioral changes are labeled as such in the heading (for example, `Behavior Change: ...`).
- Behavioral changes are ordered before purely syntactic ones.

**Note on rendering.** On the Contentstack docs platform the right navigation lists H2 and H3 only, so an
H4 heading carries no navigational weight. The label is what makes the distinction survive. This is the
reason the rule targets heading text rather than heading level.

---

## 4. Do not add a Breaking Changes Summary section

**Recorded as a decision, not a change.** The external review asked for a top-of-document "Top Breaking
Changes" list. Recommend rejecting it as a standing section.

**Why:** the facts would then appear in three places: the summary, the Quick Decision Guide, and the
command section that owns them. C7 requires one canonical location per fact. The Quick Decision Guide
already delivers the same benefit, because it routes by reader situation rather than restating content.

Suggested addition to the migration-guide rules, so this does not get re-litigated:

> **Rule:** Do not add a standalone breaking-changes summary in addition to the Quick Decision Guide.
> **Why:** it restates facts that the Quick Decision Guide and the owning sections already carry, which
> violates C7 and doubles the maintenance surface.
> **Exception:** None.

---

## Open item, unrelated to the standard

`cm:stacks:migration` documents `--authtoken` two different ways inside the same guide. The Type Mapping
Reference says the flag survives into V2 unchanged. The command section says it is removed in favor of
`csdx auth:login` plus `--alias`. Three further renames on that command (`--api-key`,
`--management-token-alias`, `--multi`) appear only in the command section and are missing from Type
Mapping. This needs a source-of-truth check against the CLI implementation before the Type Mapping table
can be completed. The command section's table was left in place rather than collapsed for this reason.
