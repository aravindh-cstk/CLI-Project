---
uid: "blt1637a00d696b0fe4"
seo_title: "Configure Multi-Factor Authentication (MFA) Secret Using CLI | V1.x.x | Contentstack"
seo_description: "Learn to set or remove your Multi-Factor Authentication (MFA) secret using Contentstack CLI for enhanced security and seamless MFA management."
---

# Configure MFA Secret Using CLI

## Overview

To use [Multi-Factor Authentication (MFA)](/docs/administration/multi-factor-authentication) with the Contentstack CLI, you must first set up or remove your MFA secret. This guide walks you through how to configure your MFA settings using CLI commands.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- [CLI installed](/docs/headless-cms/install-the-cli/v1)
- [MFA enabled](/docs/administration/multi-factor-authentication#enable-mfa)
- A copy of MFA secret

## Commands

### Set MFA Secret

Use the `config:mfa:add` command to set the MFA secret used to generate one-time passwords (OTP).

**Usage**

```
csdx config:mfa:add
```

### Remove MFA Secret

Use the `config:mfa:remove` command to remove the MFA secret.

**Usage**

```
csdx config:mfa:remove
```

**Options**

- `-y, --yes`: Skips the confirmation prompt and proceeds with the logout process.

**Example**

- To remove the MFA secret by skipping the confirmation prompt:

  ```
  csdx config:mfa:remove -y
  ```

## Limitations

- The MFA secret must be a valid base32 string using only uppercase letters A-Z and digits 2-7, at least 16 characters before padding. A secret in any other format is rejected before a code is generated.
