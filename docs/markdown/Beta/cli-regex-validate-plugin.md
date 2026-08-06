---
uid: "blt50c45d9983b508a7"
seo_title: "Regex Validate Plugin | V2.x.x | Contentstack"
seo_description: "Use the Contentstack CLI Regex Validate Plugin | V2 Beta to proactively audit a stack before deploying new content type schemas."
---

# Regex Validate Plugin | V2 Beta

## Overview

The `cm:stacks:validate-regex` command scans a Contentstack stack's content type and global field `format` properties (the regex pattern that validates a field's input) for regex patterns vulnerable to catastrophic backtracking, a condition where a regex engine's evaluation time grows exponentially for certain inputs and can bring a server to a halt. It checks each pattern using the `safe-regex` library and reports findings as a terminal table and a `results.csv` file. See [How Regex Validation Works](#how-regex-validation-works) for detail.

Run this command to:

- Proactively audit a stack before deploying new content type schemas.
- Investigate the source of a regex-related performance issue.
- Validate schemas before migrating a stack between environments.
- Confirm your stacks follow your organization's safe regex practices.

**This command only reads your stack's content types and global fields. It never modifies them.**

---

## Prerequisites

Before running the command, ensure:

1. **Contentstack CLI installed**: Install via npm:

   ```
   npm install -g @contentstack/cli
   ```

2. **Plugin installed**: The regex validation command is a separate plugin. See [Installation](#installation).

3. **Region configured** *(if not North America)*: [Set your region](/docs/headless-cms/configure-regions-in-the-cli#set-region) before running any stack commands.

4. **Management token added**: A management token scoped to the stack you want to scan must be saved with an alias:

   ```
   csdx auth:tokens:add -a <alias> -k <stack-api-key> --management --token <management-token>
   ```

   Reference: [Add a management token](/docs/headless-cms/cli-authentication#add-management-token)

---

## Installation

This command is not bundled with the core CLI and must be installed as a plugin:

```
csdx plugins:install @contentstack/cli-cm-regex-validate
```

Verify the plugin is installed:

```
csdx plugins
```

You should see `@contentstack/cli-cm-regex-validate` in the list.

---

## Command Reference

### Command Syntax

```
csdx cm:stacks:validate-regex [FLAGS]
```

### Flags

| Flag | Short | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `--alias` | `-a` | string | Yes (or prompted) | Alias of the management token for the target stack |
| `--contentType` | None | boolean | No | Scan content types for invalid regexes |
| `--globalField` | None | boolean | No | Scan global fields for invalid regexes |
| `--filePath` | None | string | No | Directory path where the output CSV should be saved |

> **v2 change**: `-c`, `-g`, and `-f` short flags have been removed. Use the long-form flags `--contentType`, `--globalField`, and `--filePath`. Only `-a` (`--alias`) is retained as a short flag.

### Flag Details

**`--alias` / `-a`**  

Added via `csdx auth:tokens:add`. If omitted, the CLI will prompt you to enter it interactively.

**`--contentType`**  

Scans all field levels including nested groups, global field references, and modular blocks.

**`--globalField`**  

Traversal logic is identical to content type scanning.

**`--filePath`**  

If the directory does not exist, it is created automatically. Defaults to a `results/` folder relative to the plugin's install location.

**Note**: At least one of `--contentType` or `--globalField` must be selected. If neither is provided, the CLI enters interactive mode and prompts you to choose.

---

## Interactive Mode

If flags are not fully provided, the CLI fills in the gaps via prompts:

**Missing `--alias`**: The CLI displays:

```
? Enter management token alias:
```

The alias is required and cannot be left blank.

**Neither `--contentType` nor `--globalField` provided**: The CLI displays a checkbox prompt:

```
? Select the module you need to check.
 ◉ Content Type
 ◯ Global Field
```

Content Type is selected by default. You must select at least one option.

You can skip all prompts by providing all required flags upfront.

---

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

A `results.csv` file is generated only when invalid regexes are found. It is saved to the `--filePath` directory (or the default `results/` folder relative to the plugin's install location) and contains one row per invalid regex with the following columns (in this order):

| Column | Description |
| --- | --- |
| `Field Path` | Dot-separated path to the field (e.g., `author.email` for a nested field) |
| `Field Title` | Display name of the field |
| `Field UID` | Unique identifier of the field |
| `Invalid Regex` | The regex pattern that failed the safe-regex check |
| `Module` | Either `Content Type` or `Global Field` |
| `Title` | Display name of the content type or global field |
| `UID` | Unique identifier of the content type or global field |

**Example CSV content**:

```
Field Path,Field Title,Field UID,Invalid Regex,Module,Title,UID
author.email,Email,email,(a+)+@domain\.com,Content Type,Blog Post,blog_post
phone,Phone Number,phone,(\d+)*,Global Field,Author Info,author_info
```

After the table, the CLI also prints:

```
CSV output stored successfully at: /path/to/results/results.csv
To know more, visit our documentation site on catastrophic-backtracking:
https://www.contentstack.com/docs/developers/create-content-types/validation-regex/#prevent-catastrophic-backtracking
```

---

## Examples

### Example 1: Interactive Mode (No Flags)

Run without flags and answer all prompts:

```
csdx cm:stacks:validate-regex
```

The CLI will prompt for:

1. Management token alias
2. Module(s) to scan

---

### Example 2: Scan Content Types Only

```
csdx cm:stacks:validate-regex -a my-stack-token --contentType
```

Scans all content types in the stack associated with the `my-stack-token` alias.

---

### Example 3: Scan Global Fields Only

```
csdx cm:stacks:validate-regex -a my-stack-token --globalField
```

Scans all global fields in the stack.

---

### Example 4: Scan Both Content Types and Global Fields

```
csdx cm:stacks:validate-regex -a my-stack-token --contentType --globalField
```

Scans both modules in a single run.

---

### Example 5: Save CSV to a Custom Directory

```
csdx cm:stacks:validate-regex -a my-stack-token --contentType --globalField --filePath /Users/name/Desktop/regex-audit
```

Saves `results.csv` to `/Users/name/Desktop/regex-audit/results.csv`. The directory is created if it does not already exist.

---

### Example 6: Automation Script

Use in a CI/CD or audit script with all flags provided to skip interactive prompts. Check the exit code before checking for `results.csv`, since a command failure and a clean scan both leave no CSV file behind:

```
#!/bin/bash
ALIAS="ci-management-token"
OUTPUT_DIR="./regex-audit-$(date +%Y%m%d)"

csdx cm:stacks:validate-regex -a "$ALIAS" --contentType --globalField --filePath "$OUTPUT_DIR"
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

---

## How Regex Validation Works

### Catastrophic Backtracking

The `cm:stacks:validate-regex` command scans a Contentstack stack and identifies regex patterns in content type and global field `format` properties that are vulnerable to catastrophic backtracking: a condition where a regex engine enters exponential retry loops when evaluating certain inputs, which can bring a server to a halt. Common causes include nested quantifiers like `(a+)+` or `(.*)*`.

**Regex Format Property**: In Contentstack, certain field types (for example Single-line Text, Multi-line Text) allow you to configure a `format` property (a regex pattern that validates field input). If this regex is poorly written, it can cause catastrophic backtracking, as defined above.

### The safe-regex Library

The command uses the [`safe-regex`](https://github.com/davisjam/safe-regex) library to test each regex pattern:

- It evaluates the pattern's abstract syntax tree.
- It flags patterns that are provably vulnerable to super-linear backtracking, either polynomial or exponential.

Results are displayed as a terminal table and saved to a CSV file for further review.

---

## Troubleshooting

### "Token not found. Add a token using csdx auth:tokens:add"

**Root Cause**: The alias provided with `-a` does not match any stored management token.

**Resolution**:

1. List your saved tokens: `csdx auth:tokens`

2. If the alias is missing, add the token:

   ```
   csdx auth:tokens:add -a <alias> -k <stack-api-key> --management --token <token>
   ```

3. Re-run the command with the correct alias.

---

### "Error in connecting to the stack. Please try again."

**Root Causes**: This message covers a range of underlying issues, including:

- Incorrect API key associated with the management token
- Management token lacks read permissions for content types or global fields
- Network connectivity issue
- Wrong region configured
- The output directory (`--filePath`) could not be written to, or an error occurred generating the CSV

**Resolution**:

1. Verify the management token is valid and has `Content Type: Read` and `Global Field: Read` permissions on the stack.

2. Confirm your region: `csdx config:get:region`. If on a non-North America region, set it: `csdx config:set:region`.

3. Test connectivity by running another CMA command against the same stack.

4. If saving to a custom path, verify the directory is writable and avoid special characters (`*`, `&`, `{`, `}`, `[`, `]`, `$`, `%`, `<`, `>`, `?`, `!`). Try an absolute path if unsure:

   ```
   csdx cm:stacks:validate-regex -a my-token --contentType --filePath /tmp/regex-output
   ```

5. Retry (this may be a transient API error).

---

### No results printed (no table, no CSV)

**Root Cause**: No invalid regexes were found in the scanned modules.

**Resolution**: No action required. This is the expected outcome when all `format` fields in your stack contain safe regex patterns.

---

## Limitations

- The command only flags patterns the `safe-regex` library's AST-based check identifies as provably vulnerable. It does not test regexes against runtime input, and it does not guarantee that every catastrophic-backtracking pattern is caught.
- The command only inspects the `format` property on content type and global field schema fields. It does not scan regex used in Custom Extensions, Apps, or client-side validation.

---

## Next Steps

- [Regex Validation in Content Type Fields (v2)](/docs/headless-cms/cli-content-type-plugin): how the `format` regex is configured on a field in the Contentstack UI.
- [Regex Validate Plugin (v1)](/docs/headless-cms/cli-regex-validate-plugin): the v1 command reference, useful if you still run v1 or need the old flag names while upgrading.
- [Prevent Catastrophic Backtracking (Contentstack Docs)](/docs/developers/create-content-types/validation-regex/#prevent-catastrophic-backtracking): background on why certain regex patterns are unsafe and how to rewrite them.
- [CLI Authentication: Add Management Token](/docs/headless-cms/cli-authentication#add-management-token): create and save the management token alias these commands use.
- [Configure Regions in the CLI](/docs/headless-cms/configure-regions-in-the-cli#set-region): set your region if your stack is not in North America.
