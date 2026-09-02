---
uid: "blt78f6b7d84156806f"
seo_title: "Import Content using the Seed Command | V0.x.x | Contentstack"
seo_description: "The “seed” command in Contentstack CLI allows users to import content to your stack, from GitHub repositories."
---

# Import Content using the Seed Command

The “seed” command in Contentstack CLI allows users to import content to your stack, from GitHub repositories. It's an effective command that can help you to migrate content to your stack with minimal steps.

To import content to your stack, you can choose from the following two sources:

- **Contentstack’s GitHub organization**: In this organization, we have provided sample content, which you can import directly to your stack using the **seed** command. Learn more on how to [import from Contentstack’s GitHub organization](#option-1-import-from-contentstacks-github-organization).
- **Non-Contentstack's GitHub repository**: You can import stack content available on GitHub’s repository belonging to any organization or individual. Learn more on how to [import from Non-Contentstack's GitHub Repository](#option-2-import-from-non-contentstacks-github-repository).

Now let’s import content to your stack by performing the following steps:

1. [Log in to the CLI session](#log-in-to-the-cli-session)
2. [Use the “seed” command](#use-the-seed-command)

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- [Node.js version 16 or above](https://nodejs.org/en/download/)
- CLI installed on your machine: **npm install -g @contentstack/cli**

## Log in to the CLI Session

To use the "seed" command, you will first have to generate the [authtoken](/docs/headless-cms/types-of-tokens#authentication-tokens-authtokens-).

> **Note**: By default, this CLI session will work for the app hosted in the **North America** region. If you want to switch to **Europe** or **Azure North America** region, follow the steps mentioned in the [Set Region](/docs/headless-cms/configure-regions-in-the-cli/v0#set-region) command section.

To use the "seed" command, you will first have to generate the **authtoken**. To generate the authtoken, open your terminal, and run the following command to log in to your Contentstack account:

```
csdx auth:login
```

It will ask you to provide your email address and password of your Contentstack account. Once you log in successfully, an authtoken will be generated and saved to the CLI session until you [log out from this session](/docs/headless-cms/cli-authentication/v0#logout).

> **Additional Resource**: To learn more about the login command, refer to the [Login command section](/docs/headless-cms/cli-authentication/v0#login).

## Use the “seed” command

To use the "seed" command, you can choose from the following options to import the content to your stack, as mentioned above.

- [Import from Contentstack’s organization](#option-1-import-from-contentstacks-github-organization)
- [Import from a GitHub repository](#option-2-import-from-non-contentstacks-github-repository)

> **Note**: If you want to upload your stack’s content onto your GitHub repository for other users to import it, refer to the steps mentioned in the [Upload stack's content on the GitHub](#upload-stacks-content-on-github) section.

Let's discuss the above two options in detail.

### Option 1: Import from Contentstack’s GitHub Organization

In this option, you can import content that Contentstack provides from its GitHub organization. To use this option, run the following command in your terminal:

```
csdx cm:seed
```

After running the above command, it will ask you to provide the following inputs:

- **Organization name**: You’ll get a list of organizations to which you have access. Select the one from the list where your source stack is located. You can also create a new stack if required.

- **Stack preference**: Next, you need to select your choice to create a new stack:
  - If you select **Yes**, you’ll receive a list of all organizations you are a member of. You can choose an organization to which you either have the [owner](/docs/administration/about-administration-roles#organization-owner) or the [admin](/docs/administration/about-administration-roles#organization-admin) rights to create a new stack. Then, provide a name to the newly created stack.
  - If you select **No**, you need to choose the organization where your destination stack resides. You will then need to select that particular stack on which you have permission to import content. Refer to the [Stack Roles](/docs/headless-cms/types-of-roles) documentation to learn more about permissions.

> **Tip**: To ensure the above operations are error-free, we recommend that you select the option of creating a new destination stack. This is because the new stack will be empty and you can easily import content to it. If you choose to import content to an existing stack, you first need to ensure that the stack is empty and then proceed with the import operation.

Finally, you’ll get the content imported to the destination stack.

### Option 2: Import from Non-Contentstack's GitHub Repository

In this option, you can import content from your GitHub repository to your stack. However, first, ensure the content is available on your GitHub repository. To upload content on GitHub, perform the steps specified in the [upload stack’s content on GitHub](#upload-stacks-content-on-github) section.

> **Note**: The GitHub repository needs to be public.

To import content from the GitHub repository, run the “seed” command in the following format:

```
csdx cm:seed -r “<account/repository>”
```

After running this command, you'll be prompted to select an organization and a stack, as discussed in the [option 1](#option-1-import-from-contentstacks-github-organization) section.

The alternate way of using the plugin is by providing the required parameters after the command in a single line.

Options:

- `-r`, `--repo=repo`: GitHub organization name or GitHub user name/repository name.
- `-s`, `--stack=stack`: Provide the UID of the stack where you want to import the content.
- `-l`, `--fetch-limit=fetch-limit`: Limit for number of organizations or stacks to be fetched.
- `-o`, `--org=org`: Provide the organization UID to create a new stack.
- `-n`, `--stack-name=stack-name`: Provide the name of the new stack that needs to be created.

**Examples**:

- To import stack content from the “blog” repository belonging to the “Stackcontent” organization, the “seed” command should follow this format:

  `csdx cm:seed -r “Stackcontent/blog"`

  Likewise, you can use the above format if the stack content resides in an individual’s GitHub repository by replacing the organization’s name with the individual’s username.

- To import content to a specific stack use the following command:

  ```
  csdx cm:seed -r "<account/repository> -s "<stack-uid>"
  ```

- Use the following command to create a new stack in an organization and import your content:

  ```
  csdx cm:seed -r "<account/repository>" -o "<org-uid>" -n "<stack-name>"
  ```

  The above command creates a new stack in your organization and imports the content in that stack.

## Upload Stack’s Content on GitHub

To upload your stack’s content to your recently-created GitHub repository, first, you need to export the stack’s content. To do so, follow these steps:

> **Note**: We assume that you are familiar with GitHub and Git. If not, go through GitHub’s documentation to [create and upload files to a GitHub repository.](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)

Before uploading stack content on your GitHub repository, you need to create a public repository in this format: *stack-\<name\>*. For example, stack-exportdata, stack-gatsby-website, etc.

1. Create a folder named “stack” in your machine.

2. Then, open your terminal and run this command to log in to the CLI session:

   ```
   csdx auth:login
   ```

   This command will ask you to provide your Contentstack account credentials.

3. After successful login, run this command to export your stack’s content to the “stack” folder:

   ```
   csdx cm:export -A -s <stack_ApiKey> -d “<path_to_store_content>”
   ```

   For example:

   ```
   csdx cm:export -A -s blt********** -d “C:\Users\Name\Desktop\content\stack”
   ```

   This command will export your stack’s content and save it to the “stack” folder.

4. Open your Git Bash terminal and follow the steps specified in [GitHub’s documentation](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github) to upload the “stack” folder to your repository.
   Refer to this [sample repository](https://github.com/contentstack/stack-starter-app) present in Contentstack's GitHub organization to learn the folder structure while uploading content to your GitHub repository.

   > **Note:** To avoid the following error make sure to create a GitHub release and proceed to import content.
   > **Error:** `Unable to find a release for '<account>/<repository>'`

Now any user can import your stack’s content to their stack by performing the steps mentioned in the [option 2](#option-2-import-from-non-contentstacks-github-repository) section.

## Points to Remember

- To import content into an existing destination stack, make sure you have permissions to create content in the destination stack.
- If you want to create a new stack for storing content, make sure you have the “[owner](/docs/administration/about-administration-roles#organization-owner)” or “[admin](/docs/administration/about-administration-roles#organization-admin)” rights in that organization.
