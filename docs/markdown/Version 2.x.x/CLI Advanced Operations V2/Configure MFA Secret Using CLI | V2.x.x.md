---
uid: "blt24a7546077dbb2e0"
seo_title: "Configure Multi-Factor Authentication (MFA) Secret Using CLI | V2.x.x | Contentstack"
seo_description: "Learn to set or remove your Multi-Factor Authentication (MFA) secret using Contentstack CLI for enhanced security and seamless MFA management."
---

# Configure MFA Secret Using CLI

## Overview

To use [Multi-Factor Authentication (MFA)](/docs/administration/multi-factor-authentication) with the Contentstack CLI, you must first set up or remove your MFA secret. This guide walks you through how to configure your MFA settings using CLI commands.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- [CLI installed](/docs/headless-cms/install-the-cli)
- [MFA enabled](/docs/administration/multi-factor-authentication#enable-mfa)
- A copy of MFA secret

## Commands

### Set the MFA Secret

The CLI reads the MFA secret from the `CONTENTSTACK_MFA_SECRET` environment variable. Set it in the shell session that runs the CLI, then log in as usual. The CLI generates the one-time password from it automatically.

**macOS and Linux**

```
export CONTENTSTACK_MFA_SECRET="<your-mfa-secret>"
csdx auth:login
```

**Windows PowerShell**

```
$env:CONTENTSTACK_MFA_SECRET = "<your-mfa-secret>"
csdx auth:login
```

> **Warning:** The `config:mfa:add` and `config:mfa:remove` commands no longer exist. Scripts that call either one fail with a command-not-found error. Replace them by setting or unsetting `CONTENTSTACK_MFA_SECRET`.

### Remove the MFA Secret

Unset the environment variable. There is no CLI command for this.

```
unset CONTENTSTACK_MFA_SECRET
```

> **Note:** Because the secret now lives in the environment rather than the CLI config file, treat it like any other credential. Avoid committing it to source control, and prefer your CI provider's secret store over a plain environment variable in a pipeline definition.
