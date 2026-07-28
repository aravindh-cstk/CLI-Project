---
uid: "blta33efb37c73c3bdf"
seo_title: "Configure CLI Logging Preferences | Contentstack"
seo_description: "Set and retrieve logging preferences in Contentstack CLI, including log level and file path configuration."
---

# Configure CLI Logging Preferences

The `config` namespace in the Contentstack CLI provides commands to configure various settings, including logging preferences.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli/)

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

- `--level=level`: Set the log level for the CLI. \<options: debug|info|warn|error\>
- `--path=path`: Specify the file path where logs should be saved.

**Examples**

- Set log level to `debug`

  ```
  csdx config:set:log --level debug
  ```

- Set log level to `info` and specify a log file path:

  ```
  csdx config:set:log --level info --path ./logs/app.log
  ```

### Get the Current Logging Configuration for the CLI

The `config:get:log` command retrieves the current logging settings, including the log level and the file path where logs are stored. If no configuration is set, the CLI will indicate that no logging configuration is available.

**Usage**

```
csdx config:get:log
```
