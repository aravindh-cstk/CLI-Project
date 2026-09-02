---
uid: "blt0a21fe8af5279f9d"
seo_title: "Export Content to .CSV File | V0.x.x | Contentstack"
seo_description: "Export Content to .CSV File using CLI"
---

# Export Content to .CSV File

The `cm:export-to-csv` command allows users to export the following data into a CSV file:

- Stack Entries
- [Organization users’ details](/docs/administration/organization-users)

This makes it easy for users to perform other operations such as create content backups, perform data analysis, and so on.

To export the content of a stack, you need to have access to it. Likewise, to export an organization’s user data, you need to be the “[owner](/docs/administration/about-administration-roles#organization-owner)” or an “[admin](/docs/administration/about-administration-roles#organization-admin)” user of that organization.

You can export content into a .csv file by performing the following two steps:

1. [Log in to the CLI session](#log-in-to-the-cli-session)
2. [Use the “cm:export-to-csv” command](#use-the-cmexport-to-csv-command)

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- [Node.js version 16 or above](https://nodejs.org/en/download/)
- CLI installed on your machine: `npm install -g @contentstack/cli`

## Log in to the CLI Session

> **Note:** By default, the CLI session uses the **North American** region. To set the **European** or **Azure North Amercian** region, refer to the [Set Region](/docs/headless-cms/configure-regions-in-the-cli/v0#set-region) command for more details.

You will need an **authtoken** to use the **export-to-csv** command. To generate the authtoken, open your terminal, and run the following command to log in to your Contentstack account:

```
csdx auth:login
```

It will ask you to provide your email address and password of your Contentstack account. Once you log in successfully, an authtoken will be generated and saved to the CLI session until you [log out from this session](/docs/headless-cms/cli-authentication/v0#logout).

> **Additional Resource**: To learn more about the login command, refer to the [Login command section](/docs/headless-cms/cli-authentication/v0#login).

![login.png](https://images.contentstack.io/v3/assets/blt23180bf2502c7444/blt73f5044ed2d4b1ff/6047bb9608636f3d7749c6a6/login.png)

## Use the ‘cm:export-to-csv’ command

Now that you are logged in to Contentstack, let’s export content from the source stack in a CSV file by running the following command in your terminal:

```
csdx cm:export-to-csv
```

This command will prompt the following options as follows:

- **Export entries to CSV**: Export all entries of a stack to a CSV file. You should have access to the stack.
  This option will ask you to select the following:
  - Organization where your stack resides
  - Stack where the content type resides
  - Content type(s) to which the entries belong
  - Language of which you want to export the entries

- **Export organization users to CSV**: Export the organization users’ details to a CSV file. To use this option, you should either be an [Organization Owner](/docs/administration/about-administration-roles#organization-owner) or the [Organization Admin](/docs/administration/about-administration-roles#organization-admin). This option lists the organization(s) of which you are either an owner or admin.

- **Exit**: Stop this command from further execution.

Once you select any one of the above-mentioned options, the “data” folder is auto-generated in the current working directory (folder), and the corresponding CSV files are stored within this “data” folder.
