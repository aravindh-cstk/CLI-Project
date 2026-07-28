# CLI Hides Log Output During Migration Runs

The customer reported that CLI log messages disappear while a migration is running.

**Root cause**

The migration command uses an interactive task-list display that redraws its progress lines in place while running. Any console.log output your migration script writes during that time lands in the same region of the terminal and gets overwritten on the next redraw.

This only happens in an interactive terminal session. If the command's output is piped or redirected to a file, the CLI automatically switches to a plain, non-redrawing output mode instead, where every line prints once with no risk of being overwritten.

**Resolution**

1. Add a newline character (\n) at the beginning of console.log statements in the migration script, for example: console.log('\nMigration started...'). This can reduce how often a log line lands on the exact spot the display is about to redraw, but it does not stop the redraw, so it is not a guaranteed fix.

2. Redirect the command's output to a file or run it in a non-interactive context, for example `csdx cm:stacks:migration --file-path <path> -k <api-key> > migration.log`. Because the CLI detects the non-interactive output stream and switches to plain output automatically, every console.log line prints in order without being overwritten.

3. For persistent, guaranteed output regardless of terminal state, note that migration errors are also written to `migration-logs/error.logs` in the current working directory. This only captures error-level entries logged by the migration tool itself, not arbitrary console.log calls from your migration script, so it is a partial substitute at best.

Redirecting output to a non-interactive stream is the more reliable fix because it changes which output mode runs, instead of trying to race the display with an extra newline.

*Source ticket: Case 46978*
