---
uid: "blt4617ed0b5e1c23f4"
seo_title: "CLI Authentication | Contentstack"
seo_description: "Authenticate securely and access Contentstack Command-line Interface using our updated developer guide for streamlined setup and usage."
---

# CLI Authentication and Adding Tokens | Beta Commands

To start using CLI commands, you must first **authenticate** yourself after installing the CLI and configuring the region. The Contentstack CLI Authentication feature allows you to securely log in or use tokens—such as [Management](/docs/headless-cms/about-management-tokens) or [Delivery tokens](/docs/headless-cms/about-delivery-tokens)—to perform content management tasks via the terminal.

It supports login credentials, Two-Factor Authentication, and Single Sign-On (SSO). You can authenticate either by using the [login](/docs/headless-cms/cli-authentication#authentication) command or by adding a Management Token to the local config.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- CLI [installed](/docs/headless-cms/install-the-cli/)
- [Set Region](/docs/headless-cms/configure-regions-in-the-cli#set-region)

## Commands

### Authentication

#### Login

The `auth:login` command lets you log in to Contentstack and save the login information in your local storage.

> **Note:** The Contentstack CLI supports [Two-factor Authentication](/docs/administration/multi-factor-authentication) for enhanced security.

Open the terminal and run the following command to log in with your Contentstack account credentials. Once you log in, you can use the Contentstack CLI commands such as [export](/docs/headless-cms/export-content-using-the-cli/), [import](/docs/headless-cms/import-content-using-the-cli/), [clone](/docs/headless-cms/cloning-a-stack/), [bulk publish and unpublish](/docs/headless-cms/bulk-publish-and-unpublish-content/), [seed](/docs/headless-cms/import-content-using-the-seed-command/), [bootstrap](/docs/headless-cms/bootstrap-starter-apps/), [migration](/docs/headless-cms/migrate-your-content-using-the-cli-migration-command/), etc.

**Usage**

```
csdx auth:login
```

**OR**

```
csdx login
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--username=username` | `-u` | Email address of your Contentstack account. |
| `--password=password` | `-p` | Password of your Contentstack account. |
| `--oauth` | - | Enables Single Sign-On (SSO) for the Contentstack CLI. |

> **Note:** To enable automatic OTP generation for MFA-enabled Contentstack accounts, set the `CONTENTSTACK_MFA_SECRET` environment variable using the [MFA secret key](/docs/administration/multi-factor-authentication) provided by Contentstack. This allows the Contentstack CLI to generate one-time passwords (OTPs) automatically, eliminating the need to enter them manually from an authenticator app.

**Examples**

```
csdx auth:login -u youremail@contentstack.com
```

```
csdx auth:login -u youremail@contentstack.com -p *****
```

```
csdx auth:login --username youremail@contentstack.com --password *****
```

```
csdx login -u youremail@contentstack.com
```

```
csdx auth:login --oauth
```

#### Logout

The `auth:logout` command lets you log out and clear the authentication from the local storage.

**Usage**

```
csdx auth:logout
```

**OR**

```
csdx logout
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--yes` | `-y` | Skips the confirmation prompt and forces the logout process. |

**Examples**

```
csdx auth:logout -y
```

```
csdx logout -y
```

#### Display Username of the Logged in User

The `csdx auth:whoami` command returns the username (email address) of the user who is currently logged in.

**Usage**

```
csdx auth:whoami
```

**OR**

```
csdx whoami
```

### Token Management

#### Add Management Token

> **Note:** Ensure you have already [generated a Management Token](/docs/headless-cms/generate-a-management-token) in your stack before running this command.

The following command lets you add an existing Management Token from your Contentstack account to the local config for further use.

**Usage**

```
csdx auth:tokens:add --management
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--alias=alias` | `-a` | Alias (name) you want to assign to the token. |
| `--management` | - | Flag to save the Management Token. |
| `--stack-api-key=stack-api-key` | `-k` | API key of the stack where the token exists. |
| `--token=token` | - | Value of the token. |
| `--yes` | `-y` | Skips the confirmation and replaces any existing token with the same alias. |

**Examples**

```
csdx auth:tokens:add --management -a tokenname -k blt******** --token cs*********
```

```
csdx auth:tokens:add --management -a tokenname -k blt******** --token cs********* -y
```

> **Note:** This command does not generate a new token in your stack. It only allows you to use an existing Management Token with the CLI.

#### Add Delivery Token

> **Note:** Ensure you have already [generated a Delivery Token](/docs/headless-cms/create-a-delivery-token) in your stack before running this command.

For CLI commands, you may use a Delivery Token instead of a Management Token. However, Delivery Tokens cannot be used for importing or exporting content.

**Usage**

```
csdx auth:tokens:add --delivery
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--alias=alias` | `-a` | Alias (name) you want to assign to the token. |
| `--delivery` | - | Flag to save the Delivery Token. |
| `--environment=environment` | `-e` | Environment name for the Delivery Token. |
| `--stack-api-key=stack-api-key` | `-k` | API key of the stack where the token exists. |
| `--token=token` | - | Value of the token. |
| `--yes` | `-y` | Skips the confirmation and replaces any existing token with the same alias. |

**Examples**

```
csdx auth:tokens:add --delivery -a tokenname -k blt******** --token cs*********
```

```
csdx auth:tokens:add --delivery -a tokenname -k blt******** --token cs********* -y
```

#### Delete Token

> **Note:** This command will not delete the Management/Delivery token from the stack; it deletes the token from the local config.

**Usage**

```
csdx auth:tokens:remove
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--alias=alias` | `-a` | Alias (name) of the token to delete. |

**Examples**

```
csdx auth:tokens:remove -a mytoken
```

```
csdx auth:tokens:remove --alias=mytoken
```

#### List All Tokens

The `auth:tokens` command lists all tokens stored in the local config.

**Usage**

```
csdx auth:tokens
```

or

```
csdx tokens
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--columns` | - | Only show provided columns (comma-separated). |
| `--sort` | - | Property to sort by (prepend '-' for descending). |
| `--filter` | - | Filter property by partial string matching. |
| `--csv` | - | Output is csv format. |
| `--no-truncate` | - | Do not truncate output to fit screen. |
| `--no-header` | - | Hide table header from output. |
| `--output` | - | Output in a more machine friendly format.<br>Supported values: `csv`, `json`, `yaml` |

## Next Steps

- [Export](/docs/headless-cms/export-content-using-the-cli) and [import](/docs/headless-cms/import-content-using-the-cli) content
- [Publish entries/assets in bulk](/docs/headless-cms/bulk-publish-and-unpublish-content)
