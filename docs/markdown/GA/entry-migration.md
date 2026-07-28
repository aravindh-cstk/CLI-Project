---
uid: "blt844ebc9ef2c5bf61"
seo_title: "Entry Migration | Contentstack"
seo_description: "Entry Migration Contentstack CLI utility lets you merge the entries along with the content types."
---

# Entry Migration

In Branches, the [merge operation](/docs/headless-cms/compare-and-merge-branches-using-the-cli/) is performed on content types and not on the entries within the content types. With the Entry Migration utility, created as part of the Entry Migration flow, you can now merge the entries along with the content types.

This step-by-step guide lets you use the Entry Migration utility to perform the merge operation on entries.

> **Note**:
>
> - The generated entry migration scripts can handle only simple scenarios. For complicated entry migration scenarios, you can customize the migration scripts.
> - The entry migration scripts are available in the `merge_scripts` folder.
> - If you want to create a script from scratch, you can use the [Migration](/docs/headless-cms/migrate-your-content-using-the-cli-migration-command) command.
> - Entry migration generates migration scripts only for content types merged during the
>   `branches:merge` command.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- [CLI installed](/docs/headless-cms/install-the-cli/) and [configured](/docs/headless-cms/configure-regions-in-the-cli/) (version 1.7.0 and above)
- [CLI authenticated](/docs/headless-cms/cli-authentication/)
- [Branches](/docs/headless-cms/about-branches/) enabled for your organization
- [Merge operation](/docs/headless-cms/compare-and-merge-branches-using-the-cli/#steps-to-merge-branches) performed

**Usage**

```
csdx cm:stacks:migration --multiple --file-path <value> --config compare-branch:<value> --branch <value> --stack-api-key <value>
```

**Options**

- `-k`, `--stack-api-key=stack-api-key`: Stack API key.
- `--branch=branch`: Base branch.
- `--config=config`: Inline configuration, `compare-branch:<value>`. The key for receiving the compare branch name.
- `--file-path=filepath`: Path where the entry migration files are stored.
- `--multiple`: Migrate multiple content files in a single instance. You must mention the folder path where your migration script files are stored.

**Example**

```
csdx cm:stacks:migration --multiple --file-path ./merge_scripts/merge_scripts_bf7xxx-xxx-xxx-xxx-xxx_xxx044 --config compare-branch:develop --branch main --stack-api-key bltxxxxxxxxxxxe
```

## Steps for execution

After performing the merge operation, the merge command generates the merge scripts, and you will get the following message in your terminal:

![Entry-Migration.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/bltdd2197674fd384ab/6458c406ddeef24daa14be95/Entry-Migration.png)

Follow the steps below to run the migration command:

1. Copy the entry migration command from the message displayed in your terminal.

   ```
   csdx cm:stacks:migration --multiple --file-path <value> --config compare-branch:<value> --branch <value> --stack-api-key <value>
   ```

2. Run the command in your terminal.

This runs the merge scripts, which will be used to merge the entries.

> **Note**: You can find the error logs in the generated file path under `migration-logs > error.logs`. For example: `./Users/Documents/cli/packages/contentstack/migration-logs/error.logs`

You can also customize the generated merge script to suit your requirements.

For example, if you want to publish the entries using the merge scripts, you can add the publish entry task as follows:

```
const publishEntriesTask = contentTypeUID => {
  return {
    title: `Publish entries for Content type '${contentTypeUID}'`,
    successMessage: `Entries published successfully for '${contentTypeUID}'`,
    failedMessage: `Failed to publish entries for '${contentTypeUID}'`,
    task: async params => {
      try {

       // Add your custom logic here

      } catch (error) {
        console.log(error)
      }
    },
  }
}
```

## Troubleshoot

If you are facing a **Migration Unsuccessful** or **Module cannot be found** error, please try one of the following troubleshooting methods:

- **Troubleshoot in your current terminal session**:
  1. **Windows (CMD)**:

     ```
     FOR /F "usebackq tokens=*" %i IN (`npm root -g @contentstack/cli`) DO SET NODE_PATH=%i/@contentstack/cli/node_modules
     ```

  2. **Windows (PowerShell)**:

     ```
     foreach ($i in $(npm root -g @contentstack/cli)) { $env:NODE_PATH = "$i/@contentstack/cli/node_modules" }
     ```

  3. **Unix**:

     ```
     export NODE_PATH="$(npm root -g @contentstack/cli)/@contentstack/cli/node_modules"
     ```

- **Troubleshoot in the entire session**:

  ```
  npm link marked
  ```

  ```
  npm link lodash
  ```
