---
uid: "bltd980d5d1a241b442"
seo_title: "Import Content Using the Seed Command | V1.x.x | Contentstack"
seo_description: "Learn how to import content to your stack using the seed command in CLI from GitHub repositories or Contentstack’s organization."
---

# Import Content Using the Seed Command

The `seed` command in the Contentstack CLI allows you to import content into your stack from GitHub repositories. It helps you migrate content with minimal steps and setup.

You can import content into your stack from the following sources:

- **Contentstack’s GitHub Organization**: We provide sample content that you can import directly into your stack using the `seed` command. Learn how to [import from Contentstack’s GitHub organization](#import-from-contentstack-s-github-organization).
- **Non-Contentstack GitHub Repository**: You can also import stack content from any public GitHub repository owned by an individual or organization. Learn how to [import from a non-Contentstack GitHub repository](#import-from-a-non-contentstack-github-repository).

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli/v1) and [configured](/docs/headless-cms/configure-regions-in-the-cli/v1)
- CLI [authenticated](/docs/headless-cms/cli-authentication/v1)
- [GitHub](https://github.com/) access and working knowledge

## Commands

To use the `seed` command, choose one of the following options to import content into your stack.

- [Import from Contentstack’s GitHub Organization](#import-from-contentstack-s-github-organization)
- [Import from a Non-Contentstack GitHub Repository](#import-from-a-non-contentstack-github-repository)

> **Note**: To upload your stack’s content to a GitHub repository for others to import, refer to the steps in the [Upload Stack's Content on GitHub](#upload-stack-s-content-on-github) section.

### Import from Contentstack’s GitHub Organization

You can import content directly from Contentstack’s GitHub organization using the CLI. To begin, run the following command in your terminal:

```
csdx cm:stacks:seed
```

After running the command, you’ll be prompted to complete the following steps:

- **Stack to import**: Select a stack from the list of available source stacks.

- **Organization name**: From the list of organizations you have access to, select the one where your source stack is located or where you want to create a new stack.

  > **Note**: You must be an [owner](/docs/administration/about-administration-roles/#organization-owner) or [admin](/docs/administration/about-administration-roles/#organization-admin) of the selected organization.

- **Stack preference**: You’ll be prompted to choose one of the following options.
  - **Create a new stack**: Enter a name, and the CLI will begin the stack creation process.

  - **Use an existing stack**: Select a destination stack from the list of stacks you have access to within the selected organization. If the selected stack contains existing content, the CLI will prompt you to confirm before continuing.

    > **Additional resource**: Refer to the [Stack Roles](/docs/headless-cms/types-of-roles) documentation to learn more about permissions.

> **Tip:** To minimize errors, we recommend creating a new destination stack. If importing content into an existing stack, ensure that it is empty.

The content will be imported into the selected destination stack.

### Import from a Non-Contentstack GitHub Repository

You can import content from your GitHub repository into your stack using this option. Before doing so, ensure your GitHub repository contains the content. To upload content, follow the steps in the [Upload Stack’s Content on GitHub](#upload-stack-s-content-on-github) section.

> **Note**: The GitHub repository must be public.

To import content, run the following `seed` command:

```
csdx cm:stacks:seed --repo “<account/repository>”
```

After running this command, you’ll be prompted to select an organization and a stack, as described in the [Import from Contentstack’s GitHub Organization](#import-from-contentstack-s-github-organization) section.

Alternatively, you can run the command with all required parameters in a single line.

**Options:**

- `-r`, `--repo=repo`: GitHub organization name or GitHub user name/repository name.
- `-k`, `--stack-api-key=stack-api-key`: Provide the stack API key to seed content to.
- `-o`, `--org=org`: Provide the organization UID to create a new stack.
- `-n`, `--stack-name=stack-name`: Provide the name of the new stack that must be created.
- `-a`, `--alias=alias`: Alias of the management token.
- `-s`, `--stack=stack`: Provide the stack UID to seed content.
- `-y`, `--yes=yes`: \[Optional\] Skip the stack confirmation.

**Examples**:

- To import content from the "blog" repository in the "Stackcontent" organization, run:

  ```
  csdx cm:stacks:seed --repo "Stackcontent/blog"
  ```

- To import content from a personal GitHub repository, replace the organization name with your GitHub username:

  ```
  csdx cm:stacks:seed --repo "username/blog"
  ```

- To import content into a specific stack, run:

  ```
  csdx cm:stacks:seed --repo "<account/repository>" -k "<stack-api-key>"
  ```

- To create a new stack in your organization and import content, use:

  ```
  csdx cm:stacks:seed --repo "<account/repository>" --org "<org-uid>" -n "<stack-name>"
  ```

  This command creates a new stack in your organization and imports the content into it.

## Upload Stack’s Content on GitHub

Before uploading your stack’s content to GitHub, export it using the following steps.

1. Create a public repository in this format: `stack-<name>`. For example, `stack-exportdata`, `stack-gatsby-website`, etc.

2. On your local machine, create a folder named “stack”.

3. Open your terminal and log in to the CLI:

   ```
   csdx auth:login
   ```

   This command prompts you to provide your Contentstack account credentials.

4. After successful login, export your stack’s content to the `stack` folder:

   ```
   csdx cm:stacks:export -k <stack_ApiKey> -d “<path_to_store_content>”
   ```

   > **Note**: If the management token is not specified, the `export` command uses **Auth token** by default.

   This command exports your stack’s content and saves it to the `stack` folder.

5. Open Git Bash and follow [GitHub’s documentation](https://docs.github.com/en/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line) to upload the `stack` folder to your repository.

   > **Additional Resource:** Refer to this [sample repository](https://github.com/contentstack/stack-starter-app) in Contentstack's GitHub organization to learn the folder structure for uploading content.

   > **Note:** To avoid the following error, create a GitHub release before importing content.
   > `Error: Unable to find a release for '<account>/<repository>'`

Now any user can import your stack’s content to their stack by performing the steps mentioned in the [Import from a Non-Contentstack GitHub Repository](#import-from-a-non-contentstack-github-repository) section.

## Points to Remember

- To import content into an existing destination stack, ensure you have permission to create content in that stack.
- To create a new stack for storing content, you must have “[owner](/docs/administration/about-administration-roles#organization-owner)” or “[admin](/docs/administration/about-administration-roles#organization-admin)” rights in that organization.
