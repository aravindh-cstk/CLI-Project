---
uid: "blt25e29bfc7ef93e50"
seo_title: "Export Content to CSV File Using the CLI | V2.x.x | Contentstack"
seo_description: "Export entries, users, teams, and taxonomies to CSV files using Contentstack CLI with detailed commands and flexible options."
---

# Export Content to CSV File Using the CLI | V2.x.x Beta

The `cm:export-to-csv` command lets you export the following data into a CSV file using Contentstack CLI:

- [Stack Entries](/docs/headless-cms/about-entries)
- [Organization users’ details](/docs/administration/organization-users)
- [Organization teams' details](/docs/administration/about-teams)
- [Taxonomy details](/docs/headless-cms/about-taxonomy)

You can use this to perform tasks such as creating content backups, analyzing data, and more.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli/v1) and [configured](/docs/headless-cms/configure-regions-in-the-cli)
- CLI [authenticated](/docs/headless-cms/cli-authentication)

> **Note:** Only the Organization [Owner](/docs/administration/about-administration-roles#organization-owner)/[Admin](/docs/administration/about-administration-roles#organization-admin) has the permissions to export an organization’s user or teams’ data.

## Commands

Contentstack CLI lets you export content from the source stack to a CSV file by running the following command in your terminal:

```
csdx cm:export-to-csv
```

This command prompts the following options:

- **Export entries of a stack to a CSV file**: To export entries, you must have access to the stack.
  You’ll be prompted to select the following:
  1. **Organization** where your stack resides.
  2. **Stack** where the content type resides.
  3. **Branch** of the stack, if the organization is branch-enabled.
  4. **Content type(s)** to which the entries belong.
  5. **Language** of the entries to be exported.

  The CSV file gets generated in the following format:

  `<stack_name>_<content_type>_<language>_entries_exports.csv`

  You can also export entries to CSV using the [Management Token](/docs/headless-cms/about-management-tokens) alias.

- **Export organization users' data to a CSV file**: To use this option, you must be an [Organization Owner](/docs/administration/about-administration-roles#organization-owner) or [Organization Admin](/docs/administration/about-administration-roles#organization-admin). The command lists only the organization(s) for which you have either role.

  > **Note:** You must be logged in to the Contentstack app to export organization users.

  When prompted, select the organization containing the user data you want to export. The CSV file is generated in the following format:

  `<orgName>_users_exports.csv`

- **Export organization teams’ data to a CSV file**: Exports a selected organization’s teams data and generates **three CSV files** with the following details:
  - **File 1:** Contains a list of **all teams** in the selected organization.

    The CSV file is generated in the following format:

    `<org-name>_teams_export.csv`

  - **File 2:**
    - Contains a list of **all the users in a particular team** if the `team-uid` flag is passed.

      The CSV file is generated in the following format:

      `<org-name>_team_<team-uid>_User_Details_export.csv`

    - Contains a list of **all the users in all the teams** if the `team-uid` flag is not passed.

      The CSV file is generated in the following format:

      `<org-name>_team_User_Details_export.csv`

  - **File 3:**
    - Contains a list of **all the stack role details of a particular team** if the `team-uid` flag is passed.

      The CSV file is generated in the following format:

      `stack_role_mapping_<team-uid>.csv`

    - Contains a list of **all the stack role details of all the teams** if the `team-uid` flag is not passed.

      The CSV file is generated in the following format:

      `stack_role_mapping.csv`

- **Export taxonomies to a CSV file**: Export taxonomies and related terms to CSV files.
  When you choose this option, you are prompted to select the following:
  1. The organization where your stack resides.
  2. The stack that contains the taxonomy you want to export.

  The CSV files are generated in the following formats:

  `<stack-name>_taxonomies.csv`

  `<stack-name>_<taxonomy-name>_<taxonomy-uid>_terms.csv`

- **Exit**: Stops the command from executing further.

Once you select any of the above options, a “data” folder is automatically created in your current working directory. The corresponding CSV files are stored within this folder.

Alternatively, you can provide the required parameters after the command in a single line as shown below:

```
csdx cm:export-to-csv -a <alias_of_management_token> -n <name_of_the_stack> --action <<entries_or_users_or_taxonomies>>  --org <organization_UID> --org-name <name_of_the_organization> --locale <name_of_the_locale> --content-type <content_type_name> --delimiter <value>
```

**Options**:

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--action` | - | Option to export data.<br>Supported values: `entries`, `users`, `teams`, `taxonomies` |
| `--alias` | `-a` | Alias of the management token. |
| `--org` | - | Provide the organization UID to clone organization-level users. |
| `--stack-name` | `-n` | Name of the stack to be used in the CSV file name. |
| `--stack-api-key` | `-k` | API key of the source stack. |
| `--org-name` | - | Name of the organization to be used in the CSV file name. |
| `--locale` | - | Locale of the entries to be exported. |
| `--content-type` | - | Content type of the entries to be exported. |
| `--branch` | - | Name of the branch from which entries will be exported. |
| `--team-uid` | - | Provide the UID of a specific team in an organization. |
| `--taxonomy-uid` | - | Provide the taxonomy UID of the related terms you want to export. |
| `--include-fallback` | - | \[Optional\] Includes fallback locale data when exporting taxonomies.<br>When enabled, if a taxonomy term does not exist in the specified locale, it falls back to the hierarchy defined in the branch settings. |
| `--fallback-locale` | - | \[Optional\] Specify a fallback locale for taxonomy export.<br>This locale is used when a taxonomy term does not exist in the primary locale.<br>Takes priority over branch fallback hierarchy when both are specified. |
| `--delimiter` | - | \[Optional\] Provide a delimiter to separate individual data fields within the CSV file.<br>Default: `,`<br>Example: `cm:export-to-csv --delimiter ','` |

**Examples**:

- Export entries to a CSV file:

  ```
  csdx cm:export-to-csv --action <entries> --locale <locale> --alias <management-token-alias> --content-type <content-type>
  ```

- Export entries to a CSV file with a custom stack name:

  ```
  csdx cm:export-to-csv --action <entries> --locale <locale> --alias <management-token-alias> --content-type <content-type> --stack-name <stack-name>
  ```

- Export organization users to a CSV file:

  ```
  csdx cm:export-to-csv --action <users> --org <org-uid>
  ```

- Export organization users to a CSV file with a custom organization name:

  ```
  csdx cm:export-to-csv --action <users> --org <org-uid> --org-name <org-name>
  ```

- Export all teams in an organization:

  ```
  csdx cm:export-to-csv --action <teams> --org <org-uid>
  ```

- Export all the data for a specific team:

  ```
  csdx cm:export-to-csv --action <teams> --team-uid <team-uid>
  ```

- Export all the data for a specific team of a given organization by providing the organization UID and name:

  ```
  csdx cm:export-to-csv --action <teams> --org <org-uid> --org-name <org-name> --team-uid <team-uid>
  ```

- Export taxonomies and related terms to a CSV file by providing the taxonomy UID:

  ```
  csdx cm:export-to-csv --action <taxonomies> --alias <management-token-alias> --taxonomy-uid <taxonomy-uid>
  ```

- Export taxonomies and respective terms to a CSV file:

  ```
  csdx cm:export-to-csv --action <taxonomies> --alias <management-token-alias>
  ```

- Export taxonomies and respective terms to a CSV file with a delimiter:

  ```
  csdx cm:export-to-csv --action <taxonomies> --alias <management-token-alias> --delimiter <delimiter>
  ```

- Export entries to a CSV file with branch name provided:

  ```
  csdx cm:export-to-csv --action <entries> --locale <locale> --alias <management-token-alias> --content-type <content-type> --stack-name <stack-name> --branch <branch-name>
  ```

- Export taxonomies with a specific locale:

  ```
  csdx cm:export-to-csv --action <taxonomies> --alias <management-token-alias> --locale <locale>
  ```

- Export taxonomies with a fallback locale support:

  ```
  csdx cm:export-to-csv --action <taxonomies> --alias <management-token-alias> --locale <locale> --include-fallback
  ```

- Export taxonomies with a custom fallback locale:

  ```
  csdx cm:export-to-csv --action <taxonomies> --alias <management-token-alias> --locale <locale> --include-fallback --fallback-locale <fallback-locale>
  ```
