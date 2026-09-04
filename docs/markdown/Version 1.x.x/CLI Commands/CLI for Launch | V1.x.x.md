---
uid: "bltff3041eae16be17d"
seo_title: "CLI for Launch | V1.x.x | Contentstack"
seo_description: "Use Contentstack CLI for Launch: Step-by-step guide to deploy & manage your JAMstack sites. Learn to create projects, view logs & more!"
---

# CLI for Launch

[Launch](/docs/launch/about-launch/) is a deployment platform that enables you to host your Contentstack-powered JAM stack website instantly. Launch hosts websites managed by any CMS (headless or traditional).

You can create a project in Launch by [connecting your GitHub repository](/docs/launch/import-project-using-github/)—Launch deploys your site instantly. Alternatively, you can [upload a folder or .zip file](/docs/launch/import-project-using-file-upload/) to create a project.

This step-by-step guide discusses how you can perform different operations in Launch using the CLI.

## Overview

- How to create a Launch project from GitHub or a file upload using the CLI.
- How to redeploy an existing Launch project, including from a CI environment.
- How to fetch logs, list deployments and environments, test cloud functions, and open the live site.
- How to roll back to a previous deployment.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)

- [CLI installed](/docs/headless-cms/install-the-cli/v1) and [configured](/docs/headless-cms/configure-regions-in-the-cli/v1) for AWS (version 1.6.0 and above), Azure (version 1.23.0 and above), or GCP (version 1.31.0 and above)

- [CLI authenticated](/docs/headless-cms/cli-authentication/v1) (the cli-launch plugin supports only login-based authentication)

- Launch-enabled Organization with [permissions](/docs/administration/about-administration-roles)

- [GitHub account](https://github.com/login) where your website code is hosted

  > **Note**: This prerequisite is applicable only if you are importing a project via GitHub.

## Commands

Contentstack Launch lets you perform the following operations in Contentstack CLI:

- [Launch (Create a Project)](#launch-create-a-project)
- [Logs](#logs)
- [Functions](#functions)
- [Deployments](#deployments)
- [Environments](#environments)
- [Open](#open)

### Launch (Create a Project)

To begin with, create a project in Launch using the CLI by importing a project from [GitHub](/docs/launch/import-project-using-github) or [uploading a file](/docs/launch/import-project-using-file-upload/). To do this, follow the steps given below:

1. Open the terminal and fire the `launch` command:
   - Run the below command if you are in the current working directory.

     ```
     csdx launch
     ```

   - If you are in a different directory, provide the path of the current working directory.

     ```
     csdx launch --data-dir <path>
     ```

     > **Note**: If you choose GitHub to create your project, provide the directory path in the Git repository as the current working directory path.

   > **Note**: Launch automatically identifies Git projects.

2. If your current working directory is not a Git repository, you will be prompted to choose a project type to proceed. Select **Continue with GitHub** or **Continue with FileUpload** to proceed.
   ![Launch_Plugin-Project_Type.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt0e0d2bc64da6923d/6437b49d1c46cc118806d761/Launch_Plugin-Project_Type.png)

3. If you select **Continue with GitHub** and have more than one GitHub namespace connected, you are prompted to **Choose a GitHub Namespace**. If only one GitHub account is connected, this is selected by default, and the prompt is skipped.

4. Select the **organization** where you want to create your project.

5. In this step, select a **branch** if you decided to create your project using GitHub.

6. Enter a **name** for your project.

7. Enter a **name** for your Environment or press **Enter** to proceed with the Default environment.

8. By default, Launch identifies the framework. Select a **Framework Preset** if you want to change the default framework, and then press **Enter**.

9. In the Build Command section, perform one of the following:
   - Press **Enter** if you want to proceed with the default Build command `npm run build`.
   - Or, enter a new build command or update the existing command if you want to customize the command.

10. Enter the output path in the **Output Directory** section or press **Enter** to proceed with the default output path.

11. Enter the server command in the **Server Command** section or press **Enter** to proceed.

12. Select a response mode:
    - **Streaming**: Delivers response chunks in real time as they are generated.
    - **Buffered**: Displays output only after the entire response has been generated.

    > **Note:** Buffered is selected by default.

13. **Enable Contentstack Authentication**: Restricts access to this environment to members of your Contentstack organization. Enter **Y** to enable it or **n** to disable it. If you press **Enter** without entering a value, it is enabled by default.

14. In the next step, follow the instructions provided on screen to choose one or more of the following options to import or add the variables:
    - **Import variables from a stack**

      Use this option to import environment variables directly from an existing stack in your organization.
      If selected, you’ll be prompted to choose a specific **Stack** and provide a valid **Delivery Token**.

    - **Manually add custom variables to the list**

      You can manually add variables as key-value pairs.
      If selected, after adding key-value pairs, a prompt, `Would you like to add more variables.?` appears.
      - Enter **Y** to add another custom variable.
      - Enter **n** to proceed with the project deployment.

    - **Import variables from the** `.env.local` **file**

      You can import variables from a `.env.local` file.

      > **Note**: Create a `.env.local` file in the repo to import variables from your `.env.local` file. In this file, each key-value pair must be on a separate line using the format `KEY=VALUE`.

    - **Skip adding environment variables**

      Allows you to skip these options and create a project without any environment variables.

      > **Note**: The 'Skip adding environment variables' option cannot be combined with other environment variable options. You can either choose 'Skip adding environment variables' or one or more of the other available options.

You have successfully deployed a Launch project using the CLI.

**Usage**

```
csdx launch
```

**Options**

- `-a, --alias=alias_token`: \[optional\] Alias (name) for the [delivery token](/docs/headless-cms/cli-authentication/v1#token-management).
- `-d, --data-dir=data-dir`: \[optional\] Current working directory.
- `-c, --config=config`: \[optional\] Path to the local '.cs-launch.json' file.
- `--type=type`: \[optional\] Type of adapters. \<options: GitHub|FileUpload\>
- `-e, --environment=environment`: \[optional\] Environment name for the Launch project.
- `-n, --name=name`: \[optional\] Name of the project.
- `--namespace=namespace`: \[optional\] GitHub account or organization namespace to use for this deployment.
- `--branch=branch`: \[optional\] GitHub branch name.
- `--build-command=build-command`: \[optional\] Build Command.
- `--env-variables=env-variables`: \[optional\] Provide the environment variables in the key:value format, separated by comma. For example: APP_ENV:prod, TEST_ENV:testVal
- `--framework=<option>`: \[optional\] Type of framework. \<options: Gatsby|NextJs|CRA (Create React App)|CSR (Client-Side Rendered)|Angular|VueJs|Other\>
- `--org=org`: \[optional\] Provide the organization UID to create a new project or deployment.
- `--out-dir=outdir`: \[optional\] Output Directory.
- `--variable-type=variable-type`: \[optional\] Provide a variable type. \<options: Import variables from a stack|Manually add custom variables to the list|Import variables from the .env.local file|Skip adding environment variables\>
- `--server-command=serverCommand`: \[optional\] Server Command.
- `--response-mode=response-mode`: \[optional\] Provide response mode. \<options: streaming|buffered\>.
- `--enable-cs-auth`: \[optional\] Enables Contentstack Authentication, restricting access to this environment to members of your Contentstack organization.
- `--disable-cs-auth`: \[optional\] Disable Contentstack Authentication, making this environment publicly accessible to anyone with its URL.

> **Note**: The `--enable-cs-auth` and `--disable-cs-auth` flags are mutually exclusive.

### Launch (Redeploy an Existing Project)

To redeploy or re-initialize an existing project, run the `launch` command using the project’s directory path or execute it from the current working directory.

- If the `cs-launch.json` file is present in the project directory, the existing project will be redeployed.
- If the `cs-launch.json` file is absent, you will be prompted to [create a new project](#launch-create-a-project).

**Usage**

If the `cs-launch.json` file is present, then run the following command to redeploy from the current working directory:

```
csdx launch
```

If you are using [GitHub](/docs/launch/import-project-using-github/) projects, after running the command, you will see a prompt as shown in the screenshot below:

![CLI-for-Launch-Redeploy-LatestCommit.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt56787498fec00135/67c6d7c1af5e642428cd1073/CLI-for-Launch-Redeploy-LatestCommit.png)

- Press **Y** to redeploy using the latest commit on GitHub.
- Press **n** to cancel the process.

If you are using the [File Upload](/docs/launch/import-project-using-file-upload/) projects, after running the command, you will see a prompt as shown in the screenshot below:

![CLI-for-Launch-Redeploy.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/bltbc292c79b70134e6/67c6d7c14f9066d2d58f9768/CLI-for-Launch-Redeploy.png)

- Press **Y** to redeploy the existing launch project.

  You will be prompted to select a redeployment method, as shown in the screenshot below:

  ![CLI-for-Launch-Redeploy-Method.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt35ab4553b49cc69b/67c6d7c1d1b1de8210ca84ea/CLI-for-Launch-Redeploy-Method.png)
  - Select the preferred redeployment method and press **Enter**.
    - **Redeploy with last file upload**: Redeploys the last uploaded file.
    - **Redeploy with new file**: Uploads a new file containing the latest changes to the project.

    Your project will be redeployed.

- Press **n** to cancel the process.

**Options**

- `-d, --data-dir=data-dir`: \[optional\] Current working directory.

- `-e, --environment=environment`: \[optional\] Environment name or UID.

- `-c, --config=config`: \[optional\] Path to the local '.cs-launch.json' file.

- `--redeploy-latest`: \[optional\] Redeploy the latest commit/code.
  - For 'File Upload' projects, redeploy by uploading the updated files.
  - For 'GitHub' projects, redeploy using the latest commit.

- `--redeploy-last-upload`: \[optional\] Redeploy using the last uploaded file (applicable only for the 'File Upload' projects).

### Using Launch CLI in a CI Environment

The Launch CLI can be utilized within CI environments to trigger redeployments for Launch projects. Follow the steps below to configure and use Launch CLI in your CI pipeline.

### Prerequisites

- **Environment Setup**
  - Use the Launch UI to create the necessary environments for your Launch project. This is a one-time setup process.
  - For detailed steps, refer to the [Creating a New Environment](/docs/launch/environments#create-an-environment) guide.

- **Configuration in Codebase**
  - In the root directory of your project, create a configuration file named `cs-launch.json`.
  - Use the following structure as a template:

  ```
  {
    "project": {
      "uid": "<projectUid>",
      "name": "<projectName>",
      "projectType": "GITHUB", // (Or FILEUPLOAD if it's a FILEUPLOAD-based project)
      "organizationUid": "<organizationUid>",
      "environments": [
        {
          "uid": "<environmentUid>",
          "name": "<environmentName>",
          "frameworkPreset": "OTHER" // Possible values: GATSBY, NEXTJS, CRA, CSR, ANGULAR, VUEJS, OTHER
        }
      ],
      "deployments": [
        {
          "uid": "<deploymentUid of latest or any previous deployment belonging to the particular environment>"
        }
      ]
    }
  }
  ```

  You can find the values for `projectUid`, `environmentUid`, `organizationUid`, and `deploymentUid` by inspecting the network requests made to your deployed site. These values are available in the response headers:
  - `x-project-uid`
  - `x-environment-uid`
  - `x-org-uid`
  - `x-deployment-uid`

  **Commit** the `cs-launch.json` file to your repository.

### Triggering Redeployments in CI

Use the following steps to trigger a redeployment using the Launch CLI within your CI environment:

- [**Set Region**](/docs/headless-cms/configure-regions-in-the-cli/v1#set-region)

  Configure the CLI to use the appropriate region.

  **Example:** `csdx config:set:region NA`

- [**Authenticate**](/docs/headless-cms/cli-authentication/v1#login) **with Launch CLI**

  Use the `csdx auth:login` command to log in.

  **Example:** `csdx auth:login --username youremail@contentstack.com --password *****`

- **Trigger Redeployment**

  Use the following command to redeploy a specific environment:

  **Example:** `csdx launch -c /path/to/project/launch-cli-config/cs-launch.json -e development --redeploy-latest`

> **Note:** The Launch CLI exits with a **non-zero status code** if the deployment fails. Ensure your CI pipeline is configured to handle this appropriately.

By following these steps, you can seamlessly integrate Launch redeployments into your CI/CD pipeline, enhancing automation and deployment efficiency.

### Logs

You can fetch the previous [deployment logs](/docs/launch/deployments#deployment-logs) and the latest server logs for Launch projects in CLI using the `launch:logs` command.

1. Open a terminal and fire the `launch:logs` command:

   ```
   csdx launch:logs
   ```

2. Select the **organization** where you created the project.

3. Then, select your **project** for which you want to fetch the logs.

4. Select the required **environment**.

**Usage**

```
csdx launch:logs
```

**Options**

- `-d, --data-dir=data-dir`: Current working directory.
- `-c, --config=config`: Path to the local '.cs-launch.json' file.
- `-e, --environment=environment`: Environment name or UID.
- `--deployment=deployment`: Deployment number or UID.
- `--type=type`: Type of flags to show logs. By default, these are server logs. Options \[`d` - deployment logs, `s` - server logs\]

> **Note**: If you do not pass a deployment ID, by default Launch fetches the latest deployment logs.

### Functions

You can test your Launch project [Cloud Functions](/docs/launch/cloud-functions/) locally using the `launch:functions` command in CLI.

**Usage**

```
csdx launch:functions
```

**Options**

- `-d, --data-dir=data-dir`: Current working directory.
- `-c, --config=config`: Path to the local '.cs-launch.json' file.
- `-p, --port=port`: \[default: 3000\] Port number.

### Deployments

You can display the list of [deployments](/docs/launch/deployments/) for an environment for Launch projects using the `launch:deployments` command in CLI.

1. Open a terminal and fire the `launch:deployments` command:

   ```
   csdx launch:deployments
   ```

2. Select the **organization** where you created the project.

3. Select your **project**.

4. Select the **environment** for which you want to list the deployments.

You have successfully listed the deployments for the selected environment.

**Usage**

```
csdx launch:deployments
```

**Options**

- `-d`, `--data-dir=data-dir`: Current working directory.
- `-c`, `--config=config`: Path to the local '.cs-launch.json' file.
- `-e`, `--environment=environment`: Environment name or UID.
- `-–org=org`: \[Optional\] Provide the organization UID.
- `-–project=project`: \[Optional\] Provide the project UID.

### Environments

You can display the list of [environments](/docs/launch/environments/) that are available for a particular project using the `launch:environments` command in CLI.

1. Open a terminal and fire the `launch:environments` command:

   ```
   csdx launch:environments
   ```

2. Select the **organization** where you created the project.

3. Select your **project**.

You have successfully listed the environments for the selected project.

**Usage**

```
csdx launch:environments
```

**Options**

- `-d`, `--data-dir=data-dir`: Current working directory.
- `-c`, `--config=config`: Path to the local '.cs-launch.json' file.
- `-–org=org`: \[Optional\] Provide the organization UID.
- `-–project=project`: \[Optional\] Provide the project UID.

### Open

You can open the live site for an environment of your Launch projects using the `launch:open` command in CLI.

1. Open the terminal and fire the `launch:open` command:

   ```
   csdx launch:open
   ```

2. Select the **organization** where you created the project.

3. Select your **project**.

4. Select the **environment** for which you want to view the live site.

You have successfully opened the live site for the selected environment.

**Usage**

```
csdx launch:open
```

**Options**

- `-d`, `--data-dir=data-dir`: Current working directory.
- `-c`, `--config=config`: Path to the local '.cs-launch.json' file.
- `-e`, `--environment=environment`: Environment name or UID.
- `-–org=org`: \[Optional\] Provide the organization UID.
- `-–project=project`: \[Optional\] Provide the project UID.

### Rollback

You can roll back to a previous successful deployment for a Launch project using the `launch:rollback` command in the CLI. This performs an [instant rollback](/docs/launch/instant-rollbacks), restoring your application to a previously archived deployment without triggering a rebuild.

1. Open a terminal and run the `launch:rollback` command:

   ```
   csdx launch:rollback
   ```

2. Select the **organization** where you created the project.

3. Select your **project**.

4. Select the **environment** you want to roll back.

5. Select an eligible **deployment** to restore from the list of previously successful deployments. The CLI displays the eligible archived deployments with their deployment number, branch, commit hash, commit message, and timestamp.

6. Review the rollback summary. The CLI displays:
   - **Current Live** deployment number
   - **Roll back to** deployment number, branch, commit hash, and timestamp

7. Enter a **Reason** for the rollback (saved to the audit log), or press **Enter** to skip.

8. When prompted with **Confirm & Rollback?**, enter **Y** to proceed or **n** to cancel.

You have successfully rolled back to a previous deployment. The CLI confirms the rollback with the new deployment ID and status.

> **Note:**
>
> - The rolled back instance uses the environment variables associated with the selected deployment.
> - Auto-deployments triggered by commits, webhooks, or automations may continue to run during a rollback. Disable them before you begin to avoid unintended deployments.

**Usage**

```
csdx launch:rollback
```

**Options**

- `-e, --environment=environment`: \[optional\] Environment number or UID.
- `--deployment=deployment`: \[optional\] Deployment UID to roll back to.
- `--org=org`: \[optional\] Provide the organization UID.
- `--project=project`: \[optional\] Provide the project UID.
- `--reason=reason`: \[optional\] Reason for the rollback (saved to audit log).

## Examples

**Launch (Create a Project)**

- To create a Launch project by providing the config file path and file type:

  ```
  csdx launch --config <path to launch config file> --type <options: GitHub|FileUpload>
  ```

- To create a Launch project by providing the directory path and file type:

  ```
  csdx launch --data-dir <path of current working dir> --type <options: GitHub|FileUpload>
  ```

- To create a Launch project from a specific connected GitHub namespace:

  ```
  csdx launch --type=GitHub --namespace=<name> --org=<org_uid> --name=<value>
  ```

- To create a Launch project by passing the server command:

  ```
  csdx launch --config <path to launch config file> --type <options: GitHub|FileUpload> --name=<value> --environment=<value> --branch=<value> --build-command=<value> --framework=<option> --org=<value> --out-dir=<value> --server-command=<value>
  ```

- To create a Launch project by providing a variable type:

  ```
  csdx launch --config <path to launch config file> --type <options: GitHub|FileUpload> --name=<value> --environment=<value> --branch=<value> --build-command=<value> --framework=<option> --org=<value> --out-dir=<value> --variable-type="Import variables from a stack" --alias=<value>
  ```

- To create a Launch project by providing a variable type and environment variables:

  ```
  csdx launch --config <path to launch config file> --type <options: GitHub|FileUpload> --name=<value> --environment=<value> --branch=<value> --build-command=<value> --framework=<option> --org=<value> --out-dir=<value> --variable-type="Manually add custom variables to the list" --env-variables="APP_ENV:prod, TEST_ENV:testVal"
  ```

> **Note**: If multiple branches are identified in the configuration, you will be prompted to **Choose a branch** to proceed with the Launch operations. A single config file can have multiple configurations based on the branch.

**Launch (Redeploy an Existing Project)**

- To redeploy using the project’s directory path, use `--data-dir`:

  ```
  csdx launch --data-dir <project-directory-path>
  ```

- To specify either the name or the UID of the environment to be redeployed, use `--environment`:

  ```
  csdx launch --environment <environment name or UID>
  ```

- To redeploy an existing GitHub project with the latest commit, use `--redeploy-latest`:

  ```
  csdx launch --redeploy-latest
  ```

- To redeploy an existing File Upload project with a new zip file, use `--redeploy-latest`:

  ```
  csdx launch --redeploy-latest
  ```

- To redeploy an existing File Upload project with the last uploaded file, use `--redeploy-last-upload`:

  ```
  csdx launch --redeploy-last-upload
  ```

- To redeploy an existing File Upload project with the new zip file from a specific path, using a specific config file, use `--redeploy-latest`, `--data-dir` and `--config`:

  ```
  csdx launch --data-dir=/root/src/project1  --redeploy-latest
   --config=/root/configs/project1/dev.json
  ```

**Logs**

- To fetch Launch project logs based on the environment number and type of flags:

  ```
  csdx launch:logs -e "environment number or uid" --type "types of flags"
  ```

- To fetch Launch project logs based on the environment number and deployment number:

  ```
  csdx launch:logs -e "environment number or uid" --deployment "deployment number or uid"
  ```

**Functions**

- To test your Launch project Cloud Function locally:

  ```
  csdx launch:functions
  ```

- To test your Launch project Cloud Function locally in a specific port:

  ```
  csdx launch:functions -p "port number"
  ```

**Deployments**

- To list the deployments in your current working directory

  ```
  csdx launch:deployments -d "current working directory"
  ```

- To list the deployments for a given environment

  ```
  csdx launch:deployments -e "environment number or uid"
  ```

**Environments**

- To list the environments in your current working directory

  ```
  csdx launch:environments -d "current working directory"
  ```

- To list the environments for a specific project under a given organization

  ```
  csdx launch:environments --org=<org UID> --project=<Project UID>
  ```

**Open**

- To open the website for an environment by passing your current working directory

  ```
  csdx launch:open --environment=environment --data-dir <path/of/current/working/dir>
  ```

- To open the website for an environment for a given configuration

  ```
  csdx launch:open --environment=environment --config <path/to/launch/config/file>
  ```

**Rollback**

To perform an interactive rollback by selecting options from prompts:

```
csdx launch:rollback
```

To roll back a specific environment to a specific deployment:

```
csdx launch:rollback -e "environment number or UID" --deployment=<deployment UID>
```

To roll back by providing the organization, project, and reason:

```
csdx launch:rollback -e "environment number or UID" \
  --deployment=<deployment UID> \
  --org=<org UID> \
  --project=<Project UID> \
  --reason="restoring previous build"
```

## Limitations

- Creating a new Launch environment via the CLI is currently not supported. At this time, environment creation is a one-time setup that must be done through the Launch UI. Once the environment is created, the Launch CLI can be used to trigger [redeployments on existing environments](#launch-redeploy-an-existing-project).
- Currently, the Launch CLI does not support Bitbucket Cloud as a source provider.
- Currently, the Launch CLI does not support modifying settings for existing projects or environments. To make these changes, please use the Launch UI.
