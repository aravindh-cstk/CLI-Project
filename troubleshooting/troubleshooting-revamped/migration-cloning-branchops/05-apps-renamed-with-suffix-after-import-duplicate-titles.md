# Applications Renamed with "?1" After Import (Duplicate Titles on Older CLI Versions)

After importing a stack, the customer found that all of their applications had been renamed with "?1" appended, and in many cases the names were truncated.

**Root cause**

When `cm:stacks:import` finds a Marketplace app name that already exists in the target stack, it generates a new name automatically. This name generation truncates the original name (18 characters for the app name itself, up to 50 characters for UI location names) and appends a lozenge character, `◈`, followed by a numeric suffix, for example `My App◈1`. This explains both symptoms reported in the ticket: the truncation, and a suffix that renders as "?1" instead of "◈1" when the customer's terminal or font cannot display the `◈` glyph and falls back to a replacement character.

The `-y` flag part of the original explanation still holds. Normally, a name conflict prompts you to confirm or edit the suggested name. Passing `-y`/`--yes` during import applies the suggested `◈`-suffixed name automatically, without prompting.

This suffix-and-truncate behavior is present in the current CLI version (`@contentstack/cli-import` 2.0.0-beta.24), not just in an old 1.12.0 release. There is no confirmation that upgrading the CLI resolves this specific behavior. Long app names can also get truncated even without a naming conflict, if the name is at or above the length threshold that triggers a suffix.

**Resolution**

1. Before importing, check the source stack for duplicate application titles and rename them to be unique. This avoids the conflict path entirely.

2. Avoid the `-y` flag when duplicate app titles may be present, so the suggested `◈`-suffixed name can be reviewed and edited via the interactive prompt before being applied.

3. If a rename already happened, look for the `◈` character (it may display as "?" depending on your terminal/font) followed by a number in the app name, and rename the app manually to the intended title.

4. Confirm the CLI version with `csdx --version` and update if you are on an old release, but treat this as a general hygiene step. This naming-conflict-resolution behavior is present in the current CLI version, so updating alone is not confirmed to change it.

Resolving duplicate titles before import, or reviewing renamed suggestions manually instead of using `-y`, prevents unwanted app renaming and truncation.

*Source ticket: Case 44445*
