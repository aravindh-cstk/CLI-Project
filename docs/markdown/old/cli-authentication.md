---
uid: "bltb29a84507c788306"
seo_title: "CLI Authentication | Old Commands | Contentstack"
seo_description: "Securely authenticate and access Contentstack's CLI with our comprehensive developer documentation."
---

# CLI Authentication and Adding Tokens | Old Commands

After installing the CLI in your system and before using the commands, you need to authenticate yourself either by using the [Login](/docs/headless-cms/cli-authentication) command or by adding the Management token within the CLI session.

> **Note**: Even though we support using delivery token for bulk publishing and unpublishing entries/assets, we recommend using management token in CLI session for efficient usability.

In the following table, we have listed the necessity of `auth:login` and `auth:tokens:add -m` commands:

| **Command** | **Mandatory for Import & Export commands?** | **Mandatory for Bulk Publish commands?** |
| --- | --- | --- |
| `auth:login` | Yes, if you want to use authtoken in `cm:import` or `cm:export` commands | No |
| `auth:tokens:add -m` | Yes, if you don’t want to use authtoken in `cm:import` or `cm:export` commands | Yes |

## Prerequisites

- [Contentstack account](https://app.contentstack.com/#!/login)
- CLI [installed](/docs/headless-cms/install-the-cli) on your machine

## Commands

### Login

The `auth:login` command lets you login to Contentstack and save the session.

Open the terminal and run the following command to login to your Contentstack account.

**Usage**

```
csdx auth:login
```

OR

```
csdx login
```

**Options**

- `-u`, `--username=username`: Email address of your Contentstack account

**Examples**

- Example 1:

  ```
  csdx auth:login -u youremail@domain.com
  ```

- Example 2:

  ```
  csdx login -u youremail@domain.com
  ```

After successful login, the authtoken will be generated automatically which you can use in import and export operations.

> **Note:**
>
> - Contentstack currently supports three regions: **North America**, **Europe** and **Azure North America**. If you want to use a specific endpoint, other than **NA**, refer to the [Set Region](/docs/headless-cms/configure-regions-in-the-cli#set-region) command.
> - Contentstack CLI now supports [Two-factor Authentication](/docs/administration/multi-factor-authentication), which ensures additional security to your Contentstack account.

### Logout

The `auth:logout` command lets you log out of Contentstack and clear the session.

**Usage**

```
csdx auth:logout
```

OR

```
csdx logout
```

**Options**

`-f`, `--force`: Exclude confirmation to logout

**Examples**

- Example 1:

  ```
  csdx auth:logout -f
  ```

- Example 2:

  ```
  csdx logout -f
  ```

### Add Management Token

To perform content management tasks, we recommend using the management token.

> **Note**: Before running this command, make sure you have [generated a management token](/docs/headless-cms/generate-a-management-token) in your stack.

The following command lets you add an existing management token from your Contentstack account and save it to the session for further use.

**Usage**

```
csdx auth:tokens:add -m
```

**Options**

- `-a`, `--alias=alias`: Alias (name) you want to assign to the token
- `-m`, `--management`: Flag to set management token
- `-e`, `--environment=environment`
- `-k`, `--api-key=api-key`: API key of the stack where the token exists
- `-t`, `--token=token`: Value of the token
- `-f`, `--force`: Force token replace

**Examples**

- To use options/ parameters in a single line:

  ```
  csdx auth:tokens:add -m -a tokenname -k blt******** --token cs*********
  ```

- To exclude confirmation when replacing the value of an existing management token:

  ```
  csdx auth:tokens:add -m -a tokenname -k blt******** --token cs********* -y
  ```

### Add Delivery Token

For Bulk Publish commands, if you don’t want to use the management token, you can use the delivery token instead. However, you will not be able to execute import and export content commands by using the delivery token.

> **Note**: Before running this command, make sure you have [generated a delivery token](/docs/headless-cms/create-a-delivery-token) in your stack.

**Usage**

```
csdx auth:tokens:add -d
```

**Options**

- `-a`, `--alias=alias` : Alias (name) of your delivery token
- `-d`, `--delivery` : Flag to set delivery token
- `-e`, `--environment=environment`: The delivery token's environment
- `-k`, `--api-key=api-key`: API key of the stack where the token exists
- `-t`, `--token=token`: Value of the token
- `-f`, `--force`: Force token replace

**Examples**

- To use options/ parameters in a single line:

  ```
  csdx auth:tokens:add -d -a tokenname -k blt******** -t cs*********
  ```

- To exclude confirmation when replacing the value of an existing delivery token:

  ```
  csdx auth:tokens:add -d -a tokenname -k blt******** -t cs********* -y
  ```

### Delete Token

The `auth:tokens:remove` command lets you delete a management/delivery token from the local CLI session.

> **Note**: This command will not delete the management/delivery token from the stack, it deletes the token from the local CLI session.

**Usage**

```
csdx auth:tokens:remove
```

**Options**

- `-a`,`--alias=alias`: Alias (name) of the token to delete
- `-i`,`--ignore`: Ignores if token not present

**Examples**

- Example 1:

  ```
  csdx auth:tokens:remove -a mytoken
  ```

- Example 2:

  ```
  csdx auth:tokens:remove --alias=mytoken
  ```

### List All Tokens

The `auth:tokens` command lists the existing tokens added to the session.

**Usage**

```
csdx auth:tokens
```

**Options**

- `--columns=columns`: To display specific columns, separated by comma
- `--filter=filter`: To filter the property by partial string matching
- `--no-header`: To hide table’s header in output
- `--no-truncate`: Not to truncate the output to fit the screen
- `--output=csv|json|yaml`: To display output in a particular format
- `--sort=sort`: To sort the list, prepend " **-** " to sort in a descending order

### Display Username of a Session

The `csdx auth:whoami` command returns the username (email address) of the user who is currently logged in the session.

**Usage**

```
csdx auth:whoami
```

> **Additional Resources**: Contentstack supports three regions: North America, Europe, and Azure North America. Refer to the [configuration](/docs/headless-cms/configure-regions-in-the-cli) guide if you want to use a particular region, other than North America (NA).

## Next Steps

- [Export](/docs/headless-cms/export-content-using-the-cli) and [import](/docs/headless-cms/import-content-using-the-cli) content
- [Publish entries/ assets in bulk](/docs/headless-cms/bulk-publish-and-unpublish-content)
