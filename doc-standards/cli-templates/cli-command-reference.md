# CLI Command Reference: Section Order

A CLI command reference documents the command surface of one plugin or one namespace: what each command does, its flags, and its output. The reader arrives knowing a command name and needs to find it without reading prose.

Apply `sdk-templates/common-rules.md` (B1, B2, C1-C9) and `cli-common-rules.md` (CLI-C1 to CLI-C10) alongside this file.

---

## Section Order

| # | Section | Required | Purpose |
|---|---|---|---|
| 1 | SEO front matter (title, description, URL) | Required | Machine-readable metadata for search and indexing |
| 2 | Page title | Required | Human-readable entry point, names the plugin or namespace |
| 3 | Overview | Required | 1-3 sentences: what this command surface does, and whether any command mutates stack data |
| 4 | Quick Reference | If the doc covers 3 or more commands | Command-to-purpose table so a reader can jump to the one command they need |
| 5 | Prerequisites | Required | CLI installed, authenticated, region configured, plus token scope and plugin install where they apply |
| 6 | Installation | If the plugin is not bundled | The `csdx plugins:install` line, present if and only if the plugin is absent from `oclif.plugins` |
| 7 | Commands | Required | One H3 per command, or the fixed facet order in bold lead-ins for a single-command doc |
| 8 | Examples | Required | Runnable scenarios that combine flags, kept out of the per-command H3s |
| 9 | Troubleshooting | Required | Root cause and resolution for each known failure |
| 10 | Limitations | Required | Known coverage gaps, per C9 |
| 11 | Next Steps | Required | Links to what comes after, each with a description |

**Governing rule:** A reader arrives knowing a command name and must find it as an H3 in the right-hand navigation without reading prose.

Two rows are deliberately conditional rather than hard-required, because a Section Order cell is checked unconditionally and neither condition can be evaluated from the doc alone. **Quick Reference** stays conditional because the linter does not count commands. **Installation** stays conditional because whether a plugin is bundled is a fact about `oclif.plugins`, not about the page. CMD2 carries the real bidirectional rule, and `checks/cli-specific.js` enforces the half of it that a script can see.

**Examples is Required rather than Recommended, deliberately.** Only a cell beginning with the word "Required" is machine-enforced, so a Recommended section is advisory and gets dropped under time pressure. 37 of the 43 existing command references have no `Examples` H2, which is the omission this change is meant to close.

---

## Type-Specific Rules

Three rules that used to live here now sit in `cli-common-rules.md`, because they apply to all three CLI types rather than to this one:

- **Command headings stop at H3.** See CLI-C1.
- **Flag tables use the six-column shape.** See CLI-C2.
- **State whether the commands mutate stack data.** See CLI-C3.

---

### CMD1: Command grouping

**Rule:** Under the `Commands` H2, when the doc documents two or more commands, each H3 must name a command that resolves to a file under that plugin's `src/commands/` tree, and the H3s must appear in that tree's sorted order.

When the doc documents exactly one command, that command is the H3 and its facets are bold lead-ins inside it, drawn from the closed list Syntax, Flags, Configuration File, Output, Examples, in that order. Omit a facet that does not apply rather than reordering the rest.

**Why:** The reader's entry point is a command name they already know. Ordering the page by the CLI's own command tree means the page's structure matches the structure the reader learned from `--help`, so a name they hold in mind maps to a heading they can find. The single-command branch needs a different rule because one namespace node supplies no ordering at all.

The facets are bold lead-ins rather than headings because CLI-C1 stops headings at H3, and the command itself already occupies that level. A reader never navigates to `Syntax` in isolation, they navigate to a command and read its facets in order, so the facets lose nothing by carrying no anchor.

**Exception:** None. A doc whose `Commands` H3s are task names rather than command ids is a task runbook, not a command reference, and should be retyped.

---

### CMD2: Installation is present if and only if the plugin is external

**Rule:** Include an `Installation` section with the `csdx plugins:install` command if and only if the plugin is absent from `oclif.plugins` in the CLI's `package.json` for the documented version.
**Why:** A bundled plugin needs no install step, and telling a reader to install one wastes their time and implies the CLI is incomplete. An external plugin without the step produces a "command not found" error the reader cannot diagnose. The two lists differ by version: V2 dropped `cli-cm-migrate-rte` and `cli-launch` from the bundle and replaced `cli-cm-bulk-publish` with `cli-bulk-operations`, so a V1 doc and its V2 twin can legitimately disagree here.
**Exception:** None. The bundled list is machine-readable, so this is always decidable.
