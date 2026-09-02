---
uid: "blt33b42b2ce32f4cb4"
seo_title: "Regex Validate Plugin | V1.x.x | Contentstack"
seo_description: "Use the Contentstack CLI Regex Validate Plugin to scan content types and global fields for regex patterns vulnerable to catastrophic backtracking."
---

# Regex Validate Plugin

A newer version of this command is available. See [Regex Validate Plugin (v2)](/docs/headless-cms/cli-regex-validate-plugin) for the current flag syntax before installing v1.

## Overview

The `cm:stacks:validate-regex` command scans a Contentstack stack's content type and global field `format` properties (the regex pattern that validates a field's input) for regex patterns vulnerable to catastrophic backtracking, a condition where a regex engine's evaluation time grows exponentially for certain inputs and can bring a server to a halt. It checks each pattern using the `safe-regex` library and reports findings as a terminal table and a `results.csv` file. See [How Regex Validation Works](#how-regex-validation-works) for detail.

Run this command to:

- Proactively audit a stack before deploying new content type schemas.
- Investigate the source of a regex-related performance issue.
- Validate schemas before migrating a stack between environments.
- Confirm your stacks follow your organization's safe regex practices.

**This command only reads your stack's content types and global fields. It never modifies them.**

## Prerequisites

Before running the command, ensure the following.

### Mandatory

- **Contentstack CLI v1 installed**: See the [Contentstack CLI installation guide](/docs/headless-cms/install-the-cli/v1).

  ```
   npm install -g @contentstack/cli
  ```

- **Plugin installed**: The regex validation command is distributed as a separate plugin. See [Installation](#installation).

- **Management token added**: The scan authenticates against your stack using a saved management token alias. Add one scoped to the stack you want to scan:

  ```
   csdx auth:tokens:add -a <alias> -k <stack-api-key> --management --token <management-token>
  ```

  Reference: [Add a management token](/docs/headless-cms/cli-authentication/v1#add-management-token). The token's role must grant read access to the modules you scan: `Content Type: Read` for `--contentType`, `Global Field: Read` for `--globalField`.

- **Region configured, if your stack is not in North America**: [Set your region](/docs/headless-cms/configure-regions-in-the-cli/v1#set-region) before running any stack commands. Skipping this on a non-North America stack causes the connection error described in [Troubleshooting](#error-in-connecting-to-the-stack-please-try-again).

### Optional

None.

## Installation

This command is distributed as a separate plugin:

1. Install the plugin:

   ```
   csdx plugins:install @contentstack/cli-cm-regex-validate
   ```

2. Verify the plugin is installed:

   ```
   csdx plugins
   ```

   You should see `@contentstack/cli-cm-regex-validate` in the list with version `1.x`.

## Command Reference

### Command Syntax

```
csdx cm:stacks:validate-regex [FLAGS]
```

### Flags

| Flag | Short | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `--alias` | `-a` | string | Yes (or prompted) | Alias of the management token for the target stack |
| `--contentType` | `-c` | boolean | No | Toggle to scan content types for invalid regexes |
| `--globalField` | `-g` | boolean | No | Toggle to scan global fields for invalid regexes |
| `--filePath` | `-f` | string | No | Directory path where the output CSV should be saved |
| `--help` | `-h` | boolean | No | Toggle to display command help and available flags |

### Flag Details

- `--alias` **/** `-a`:
  - Added via `csdx auth:tokens:add`.
  - If omitted, the CLI prompts you to enter it interactively.

- `--contentType` **/** `-c`:
  - Scans all field levels, including nested groups, global field references, and modular blocks.

- `--globalField` **/** `-g`:
  - Walks each field, including nested groups and modular blocks, the same way `--contentType` does for content types.

- `--filePath` **/** `-f`:
  - If the directory does not exist, it is created automatically.
  - Defaults to a `results/` folder relative to the plugin's install location.
  - See [CSV Output](#csv-output) for the full save-location behavior.

At least one of `--contentType` or `--globalField` must be provided to specify the scan target. If neither flag is passed, the CLI defaults to interactive mode and prompts for a selection. To bypass the prompt, pass at least one flag explicitly:

```
csdx cm:stacks:validate-regex -a my-token-alias -c
```

## Interactive Mode

If flags are not fully provided, the CLI fills in the gaps via prompts:

**Missing** `--alias`: The CLI displays:

```
? Enter management token alias:
```

Enter the alias to identify which stack to connect to.

**Neither** `--contentType` **nor** `--globalField` **provided**: The CLI displays a checkbox prompt (both options can be selected):

```
? Select the module you need to check.
 ◉ Content Type
 ◯ Global Field
```

Content Type is selected by default. At least one option must be selected to specify the scan target.

You can skip all prompts by providing all required flags upfront.

## Output

### Terminal Table

After scanning, the CLI prints a summary table to the terminal:

```
The following table shows the invalid regexes present in your stack.

┌───────────────┬────────────────────┬─────────────────────┬──────────────────────┐
│ Module        │ Title              │ UID                 │ Invalid Regex Count  │
├───────────────┼────────────────────┼─────────────────────┼──────────────────────┤
│ Content Type  │ Blog Post          │ blog_post           │ 2                    │
│ Global Field  │ Author Info        │ author_info         │ 1                    │
└───────────────┴────────────────────┴─────────────────────┴──────────────────────┘
```

If no invalid regexes are found:

```
There are no invalid regexes in your stack.
```

### CSV Output

If no invalid regexes are found, no `results.csv` file or output directory is created. The rest of this section describes the file the command produces when invalid regexes are found.

The CSV (comma-separated values) file (`results.csv`) is saved to one of two locations:

- If `--filePath` is set, to that directory.
- If `--filePath` is not set, to a `results` folder inside the plugin's package root, the same directory that contains the plugin's `lib` folder and `package.json`.

If the target directory does not exist, it is created automatically.

The file contains one row per invalid regex. Each row includes the field's full path, supporting nested groups and modular blocks, so you can locate and fix it precisely.

The file has the following columns, in this order:

| Column | Description |
| --- | --- |
| `Module` | Either `Content Type` or `Global Field` |
| `Title` | Display name of the content type or global field |
| `UID` | Unique identifier of the content type or global field |
| `Field Title` | Display name of the field |
| `Field UID` | Unique identifier of the field |
| `Field Path` | Dot-separated path to the field (for example `author.email` for a nested field) |
| `Invalid Regex` | The regex pattern that failed the safe-regex check |

**Example CSV content**:

```
Module,Title,UID,Field Title,Field UID,Field Path,Invalid Regex
Content Type,Blog Post,blog_post,Email,email,author.email,(a+)+@domain\.com
Global Field,Author Info,author_info,Phone Number,phone,phone,(\d+)*
```

After the table, the CLI also prints:

```
CSV output stored successfully at: <plugin-install-directory>/results/results.csv
```

To fix a flagged regex:

1. Update the field's `format` value in the Content Type Builder (or Global Field builder) to a pattern that does not nest repeated groups.
2. Re-run the scan to confirm the field no longer appears in the results.

For guidance on rewriting a specific vulnerable pattern, see the [Prevent Catastrophic Backtracking documentation](/docs/headless-cms/validation-regex).

## Examples

### Example 1: Interactive Mode (No Flags)

Run without flags and answer all prompts:

```
csdx cm:stacks:validate-regex
```

The CLI prompts for:

1. Management token alias
2. Module(s) to scan

### Example 2: View Help

```
csdx cm:stacks:validate-regex -h
```

### Example 3: Scan Content Types Only

```
csdx cm:stacks:validate-regex -a my-token-alias -c
```

Scans all content types in the stack associated with the `my-token-alias` alias.

### Example 4: Scan Global Fields Only

```
csdx cm:stacks:validate-regex -a my-token-alias -g
```

Scans all global fields in the stack associated with the `my-token-alias` alias.

### Example 5: Scan Both Content Types and Global Fields

```
csdx cm:stacks:validate-regex -a my-token-alias -c -g
```

Scans both content types and global fields in the stack associated with the `my-token-alias` alias, in a single run.

### Example 6: Save CSV to a Custom Directory

```
csdx cm:stacks:validate-regex -a my-token-alias -c -g -f /Users/name/Desktop/regex-audit
```

Scans both content types and global fields in the stack associated with the `my-token-alias` alias and saves `results.csv` to `/Users/name/Desktop/regex-audit/results.csv`, creating the directory if it does not already exist (see [--filePath](#flag-details) for this behavior).

### Example 7: Automation Script

Use this script in a CI/CD pipeline or audit script, with all flags provided to skip interactive prompts. It checks the command's exit code to decide what to report:

- The command exits `0` both for a clean scan and for a scan that finds invalid regexes.
- It returns a non-zero exit code only when the command itself fails, for example an invalid token or a connection error.
- In bash, `$?` holds the exit code of the last command that ran.

```
#!/bin/bash
ALIAS="my-token-alias"
OUTPUT_DIR="./regex-audit-$(date +%Y%m%d)"

csdx cm:stacks:validate-regex -a "$ALIAS" -c -g -f "$OUTPUT_DIR"
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "Command failed with exit code $EXIT_CODE."
  exit $EXIT_CODE
elif [ -f "$OUTPUT_DIR/results.csv" ]; then
  echo "Invalid regexes found. Review: $OUTPUT_DIR/results.csv"
  exit 1
else
  echo "No invalid regexes found."
fi
```

The script checks `$?` first because two different outcomes both leave no CSV file behind:

- **Command failure** (for example, an invalid token): the scan never ran.
- **Clean scan**: the scan ran fine and found no invalid regexes.

Checking the exit code first tells these apart, so a real failure is reported as a failure, not a false "no invalid regexes found."

## How Regex Validation Works

### Catastrophic Backtracking

The `cm:stacks:validate-regex` command scans a Contentstack stack and identifies regex patterns in content type and global field `format` properties that are vulnerable to catastrophic backtracking: a condition where a regex engine enters exponential retry loops when evaluating certain inputs, which can bring a server to a halt. Common causes include nested quantifiers like `(a+)+` or `(.*)*`.

**Regex Format Property**: In Contentstack, certain field types (for example Single-line Text, Multi-line Text) allow you to configure a `format` property (a regex pattern that validates field input). If this regex is poorly written, it can cause catastrophic backtracking, as defined above.

### The safe-regex Library

The command uses the [`safe-regex`](https://github.com/davisjam/safe-regex) library to test each regex pattern:

- It evaluates the pattern's abstract syntax tree.
- It flags patterns that are provably vulnerable to super-linear backtracking, either polynomial or exponential.

Results are displayed as a terminal table and saved to a CSV file for further review.

## Troubleshooting

### "Token not found. Add a token using csdx auth:tokens:add"

**Root Cause**: The alias provided with `-a` does not match any stored management token.

**Resolution**:

1. List your saved tokens: `csdx auth:tokens`
2. If the alias is missing, add the token as described in [Prerequisites](#prerequisites).
3. Re-run the command with the correct alias. See [--alias / -a](#flag-details) for how the flag is used.

### "Error in connecting to the stack. Please try again."

**Root Cause(s)**: This message covers a range of underlying issues, including:

- **A special character in `--filePath` prevented the CSV from being written.** This cause is easy to mistake for a network issue, since the message is the same either way.
- Incorrect API key associated with the management token
- Management token lacks read permissions for content types or global fields
- Network connectivity issue
- Wrong region configured

**Resolution**:

1. If saving to a custom path, verify the directory is writable and avoid special characters (`*`, `&`, `{`, `}`, `[`, `]`, `$`, `%`, `<`, `>`, `?`, `!`). Try an absolute path if unsure:

   ```
    csdx cm:stacks:validate-regex -a my-token-alias -c -f /tmp/regex-output
   ```

2. Verify the management token is valid and has `Content Type: Read` and `Global Field: Read` permissions on the stack.

3. Confirm your region: `csdx config:get:region`. If on a non-North America region, set it: `csdx config:set:region`. See [Region configured](#mandatory) in Prerequisites.

4. Test connectivity by running another CMA (Content Management API) command against the same stack.

5. Retry. The connection error may be transient, a temporary condition such as a brief network interruption that clears up without further action, so retrying can succeed even without changing anything else.

### No results printed (no table, no CSV)

**Root Cause**: No invalid regexes were found in the scanned modules.

**Resolution**: No action required. This is the expected outcome when all `format` fields in your stack contain safe regex patterns, matching the `There are no invalid regexes in your stack.` message described in [Output](#output).

## Limitations

- The command only flags patterns the `safe-regex` library's AST-based check identifies as provably vulnerable. It does not test regexes against runtime input, and it does not guarantee that every catastrophic-backtracking pattern is caught.
- The command only inspects the `format` property on content type and global field schema fields. It does not scan regex used in Custom Extensions, Apps, or client-side validation.
- Coverage on stacks with a very large number of content types or global fields has not been verified against the underlying Management SDK's pagination behavior. Treat results on such stacks as unconfirmed until this is verified.

## Next Steps

- [Regex Validate Plugin (v2)](/docs/headless-cms/cli-regex-validate-plugin): the v2 command reference. Flag names and the `results.csv` column order changed in v2, read this before upgrading.
- [Regex Validation in Content Type Fields (v1)](/docs/headless-cms/cli-content-type-plugin/v1): how the `format` regex is configured on a field in the Contentstack UI.
- [Prevent Catastrophic Backtracking (Contentstack Docs)](/docs/headless-cms/validation-regex): background on why certain regex patterns are unsafe and how to rewrite them.
