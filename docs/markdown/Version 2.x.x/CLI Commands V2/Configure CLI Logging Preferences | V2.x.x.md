---
uid: "blt66365ee2f36e0315"
seo_title: "Configure CLI Logging Preferences | V2.x.x | Contentstack"
seo_description: "Set and retrieve logging preferences in Contentstack CLI, including log level and file path configuration."
---

# Configure CLI Logging Preferences

## Overview

The `config` namespace in the Contentstack CLI provides commands to configure various settings, including logging preferences.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli)

## Commands

### Set a Logging Configuration for the CLI

The `config:set:log` command lets you configure the logging behavior of the Contentstack CLI. You can set the preferred log level and specify a file path for storing log outputs.

- If the `--level` flag is not provided, the CLI will prompt you to select a log level interactively.
- If the `--path` flag is not specified, the CLI will prompt you to enter a file path for log storage.

**Usage**

```
csdx config:set:log [--level <level>] [--path <path>]
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--level` | - | Set the log level for the CLI.<br>Supported values: `debug`, `info`, `warn`, `error` |
| `--path` | - | Specify the directory path where logs should be saved. |
| `--show-console-logs` | - | Enable console logging.<br>Use `--no-show-console-logs` to disable it. |

**Examples**

- Set log level to `debug`

  ```
  csdx config:set:log --level debug
  ```

- Set log level to `info` and specify a log file path:

  ```
  csdx config:set:log --level info --path ./logs/app.log
  ```

> **Warning:** The configuration key for this setting changed between major versions. V1 stored it as `log["show-console-logs"]` and the current CLI reads `log["showConsoleLogs"]`. After you upgrade, the older key is ignored with no warning and console logging falls back to its default. Run `csdx config:set:log --show-console-logs` once after upgrading to write the key in the form the current CLI reads.

### Get the Current Logging Configuration for the CLI

The `config:get:log` command retrieves the current logging settings, including the log level and the file path where logs are stored. If no configuration is set, the CLI will indicate that no logging configuration is available.

**Usage**

```
csdx config:get:log
```
