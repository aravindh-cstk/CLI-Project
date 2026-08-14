---
uid: "bltc0036c8ffee6ddd5"
seo_title: "Bootstrap Starter Apps | V2.x.x | Contentstack"
seo_description: "Set up Starter apps quickly with Contentstack's Bootstrap CLI plugin—automate stack creation, content import, and Live Preview setup."
---

# Bootstrap Starter Apps

The Bootstrap plugin in the Contentstack CLI simplifies the process of setting up [Starter apps](/docs/headless-cms/nuxt) by automating stack creation and content import. With a single command, developers can quickly clone a Starter app and configure it with all the required assets and content.

Using this plugin, all necessary content—such as [content types](/docs/headless-cms/about-content-types), [environments](/docs/headless-cms/about-environments), [entries](/docs/headless-cms/about-entries), and [assets](/docs/headless-cms/about-assets)—is automatically created in the stack you choose or create.

This guide explains how to use the Bootstrap plugin to automate the setup process for your Starter app projects.

> **Note:** This Starter app uses [Live Preview](/docs/headless-cms/about-live-preview) version 2.0.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)

- CLI [installed](/docs/headless-cms/install-the-cli)

- [Set region](/docs/headless-cms/configure-regions-in-the-cli#set-region)

- Authenticate CLI using one of the following:
  - [Login](/docs/headless-cms/cli-authentication#authentication)
  - [Management Token](/docs/headless-cms/cli-authentication#token-management)

## Using the Bootstrap Command

Use the `cm:bootstrap` command to automate Starter app setup. This command performs the following:

- Clones the selected app from GitHub
- Creates or uses an existing stack
- Imports content types, entries, assets, and environments

**Command:**

```
csdx cm:bootstrap
```

When executed, the command prompts you to provide the following details:

1. **Technology**

   Select the Starter app you want to use (e.g., React, Next.js, Gatsby, Angular).

   In this example, let's select **React JS** as the Starter app.

   ![CLI-Bootstrap-SelectReact.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt9a23df561b2365af/680f5f298638c9da83ff1694/CLI-Bootstrap-SelectReact.png)

2. **Path**

   Choose the folder path to clone the app’s source code.
   Use one of the following:
   - **Current Folder**
   - **Other** (to provide a custom path)

3. **Live Preview**

   Choose whether to enable Live Preview (Y/n).

   Press **Y** to enable or **n** to skip.

   ![CLI-Bootstrap-LivePreview.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt280f893d236fdab7/680f5f29779714670265ced7/CLI-Bootstrap-LivePreview.png)

   This will start cloning the selected app to the folder you provide.

4. **Organization Name**

   Select the organization under which the stack should be created.

   ![CLI-Bootstrap-SelectOrg.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt86501569f082aa47/680f5f29d6b2551be2ebb4c1/CLI-Bootstrap-SelectOrg.png)

5. **Stack Preference**

   Choose to create a **New** stack or use an **Existing** stack to import the app content.

   In this example, let's create a new stack in the organization we selected.

   ![CLI-Bootstrap-NewStack.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/bltc19d800dad7fc5e7/680f5f29a61e01023bda74a4/CLI-Bootstrap-NewStack.png)

6. **Stack Name**

   Enter a **name** for the new stack and click **Enter**.

   ![CLI-Bootstrap-StackCreation.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/bltf3fa0cd2d05e0823/680f5f29ee7e7328f3c6143e/CLI-Bootstrap-StackCreation.png)

   With this process, the content—including fields, assets, environments, languages, and other settings—will be imported into the selected stack.

> **Note:** Imported content will be automatically published in the target stack.

This is how you can automate project setup in Contentstack by using the Bootstrap command.

You can also run the bootstrap command with all required parameters in a single line:

```
csdx cm:bootstrap --app-name "<starter_app_name>" --project-dir "<path_or_the_location_of_the_folder_to_clone_the_app>" -k "<stack_api_key>"
```

or

```
csdx cm:bootstrap --app-name "<starter_app_name>" --project-dir "<path_or_the_location_of_the_folder_to_clone_the_app>" --org "<organization_uid>" -n "<stack_name>"
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--app-name` | - | App name.<br>Supported values: `compass-app`, `kickstart-next`, `kickstart-next-ssr`, `kickstart-next-ssg`, `kickstart-next-graphql`, `kickstart-next-middleware`, `kickstart-nuxt`, `kickstart-nuxt-ssr` |
| `--project-dir` | - | Directory to set up the project. |
| `--stack-api-key` | `-k` | Provide the stack API key to seed content. |
| `--org` | - | Provide the organization UID to create a new stack. |
| `--stack-name` | `-n` | Name of the new stack that will be created. |
| `--yes` | `-y` | \[Optional\] Skip stack confirmation. |
| `--run-dev-server` | - | Automatically start the development server after setup. |
| `--alias` | `-a` | Alias of the management token. |

**Examples**

- To select the app you want to clone:

  ```
  csdx cm:bootstrap --app-name "<starter_app_name>"
  ```

  Example: React JS

  ```
  csdx cm:bootstrap --app-name kickstart-next
  ```

- Use this command to provide the path to the location of the folder to clone the app:

  ```
  csdx cm:bootstrap --project-dir "<The path or the location to clone the app>"
  ```

  Example:

  ```
  csdx cm:bootstrap --project-dir "C:\Users\Name\Desktop\cli\content"
  ```

- Use this command to add all the flags in a single command:

  ```
  csdx cm:bootstrap --app-name <<starter-app-name>> --project-dir "<The path or the location to clone the app>" --org "your-org-uid" --stack-name "stack-name"
  ```

  Example

  ```
  csdx cm:bootstrap --app-name kickstart-next --project-dir "C:\Users\Name\Desktop\cli\content" --org "your-org-uid" --stack-name "sample-stack"
  ```

The above command will add the Starter app’s (React JS) content to your stack as shown below:

![CLI-Bootstrap-Bootstrap-Stack.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt094971ffb299f4ce/680f5f29858ac99fb022b33b/CLI-Bootstrap-Bootstrap-Stack.png)

## Run the Bootstrap Starter App

You can easily run this Starter app on your local machine by following the steps below:

1. Build, Configure, and Run the Website (Manual Process)
   1. [Download](https://codeload.github.com/contentstack/contentstack-react-starter-app/zip/refs/heads/master) the website code.

   2. Open your terminal.

   3. Navigate to your project folder.

   4. Run the following command to create a configuration file named `.env.development`.

      ```
      cp .env.example .env.development
      ```

      > **Note:** If you are a Windows user, replace `cp` with `copy` in the command above.

      The `.env.development` file contains all the necessary configuration parameters.
      1. Open it in any code editor or IDE of your choice.
      2. Provide your stack credentials (such as [API key](/docs/headless-cms/view-stack-details/), [Delivery token](/docs/headless-cms/about-delivery-tokens/), and [environment](/docs/headless-cms/about-environments/)), and save the file.

      ```
      # Contentstack is the tool we use to manage our website's content.
      # You need to replace 'your_stack_api_key', 'your_delivery_token', and 'your_environment_name' with the actual information.
      REACT_APP_CONTENTSTACK_API_KEY=<your_stack_api_key>
      REACT_APP_CONTENTSTACK_DELIVERY_TOKEN=<your_delivery_token>
      REACT_APP_CONTENTSTACK_ENVIRONMENT=<your_environment_name>

      # Below config options are for enabling live preview/live edit tags for the starter app
      REACT_APP_CONTENTSTACK_API_HOST=api.contentstack.io
      REACT_APP_CONTENTSTACK_MANAGEMENT_TOKEN=<your_management_token>
      REACT_APP_CONTENTSTACK_APP_HOST=app.contentstack.com
      REACT_APP_CONTENTSTACK_LIVE_PREVIEW=true
      REACT_APP_CONTENTSTACK_LIVE_EDIT_TAGS=false

      # API Host, APP Host and Region Environment Variables for AWS North America region users
      # REACT_APP_CONTENTSTACK_API_HOST=api.contentstack.io
      # REACT_APP_CONTENTSTACK_REGION=NA
      # REACT_APP_CONTENTSTACK_APP_HOST=app.contentstack.io

      # API Host, APP Host and Region Environment Variables for AWS Europe region users
      # REACT_APP_CONTENTSTACK_API_HOST=eu-api.contentstack.com
      # REACT_APP_CONTENTSTACK_REGION=EU
      # REACT_APP_CONTENTSTACK_APP_HOST=eu-app.contentstack.io

      # API Host, APP Host and Region Environment Variables for AWS Australia region users
      # REACT_APP_CONTENTSTACK_API_HOST=au-api.contentstack.com
      # REACT_APP_CONTENTSTACK_REGION=AU
      # REACT_APP_CONTENTSTACK_APP_HOST=au-app.contentstack.io

      # API Host, APP Host and Region Environment Variables for Azure North America region users
      # REACT_APP_CONTENTSTACK_API_HOST=azure-na-api.contentstack.com
      # REACT_APP_CONTENTSTACK_REGION=AZURE-NA
      # REACT_APP_CONTENTSTACK_APP_HOST=azure-na-app.contentstack.io

      # API Host, APP Host and Region Environment Variables for Azure Europe region users
      # REACT_APP_CONTENTSTACK_API_HOST=azure-eu-api.contentstack.com
      # REACT_APP_CONTENTSTACK_REGION=AZURE-EU
      # REACT_APP_CONTENTSTACK_APP_HOST=azure-eu-app.contentstack.io

      # API Host, APP Host and Region Environment Variables for Google North America region users
      # REACT_APP_CONTENTSTACK_API_HOST=gcp-na-api.contentstack.com
      # REACT_APP_CONTENTSTACK_REGION=GCP-NA
      # REACT_APP_CONTENTSTACK_APP_HOST=gcp-na-app.contentstack.io

      # API Host, APP Host and Region Environment Variables for Google Europe region users
      # REACT_APP_CONTENTSTACK_API_HOST=gcp-eu-api.contentstack.com
      # REACT_APP_CONTENTSTACK_REGION=GCP-EU
      # REACT_APP_CONTENTSTACK_APP_HOST=gcp-eu-app.contentstack.io

      # By default branch=main, if a branch is not provided
      # REACT_APP_CONTENTSTACK_BRANCH=<your_branch_name>

      SKIP_PREFLIGHT_CHECK=true
      ```

      > **Note:** Live Preview that uses the `REACT_APP_CONTENTSTACK_MANAGEMENT_TOKEN` will soon be deprecated. Instead, we recommend using the Live Preview that relies on the `REACT_APP_CONTENTSTACK_PREVIEW_TOKEN`, `REACT_APP_CONTENTSTACK_PREVIEW_HOST`, `REACT_APP_CONTENTSTACK_APP_HOST`, and `REACT_APP_CONTENTSTACK_API_HOST` as given below.

      ```
      REACT_APP_CONTENTSTACK_PREVIEW_HOST=rest-preview.contentstack.io
      REACT_APP_CONTENTSTACK_PREVIEW_TOKEN=<preview_token_linked_to_delivery_token>
      REACT_APP_CONTENTSTACK_APP_HOST=app.contentstack.com
      REACT_APP_CONTENTSTACK_LIVE_PREVIEW=true
      REACT_APP_CONTENTSTACK_LIVE_EDIT_TAGS=false

      # API Host, APP Host, Preview Host and Region Environment Variables for AWS North America region users
      # REACT_APP_CONTENTSTACK_PREVIEW_HOST=rest-preview.contentstack.io
      # REACT_APP_CONTENTSTACK_REGION=NA
      # REACT_APP_CONTENTSTACK_API_HOST=api.contentstack.io

      # API Host, APP Host, Preview Host and Region Environment Variables for AWS Europe region users
      # REACT_APP_CONTENTSTACK_PREVIEW_HOST=eu-rest-preview.contentstack.com
      # REACT_APP_CONTENTSTACK_REGION=EU
      # REACT_APP_CONTENTSTACK_API_HOST=eu-api.contentstack.com

      # API Host, APP Host, Preview Host and Region Environment Variables for AWS Australia region users
      # REACT_APP_CONTENTSTACK_PREVIEW_HOST=au-rest-preview.contentstack.com
      # REACT_APP_CONTENTSTACK_REGION=AU
      # REACT_APP_CONTENTSTACK_API_HOST=au-api.contentstack.com

      # API Host, APP Host, Preview Host and Region Environment Variables for Azure North America region users
      # REACT_APP_CONTENTSTACK_PREVIEW_HOST=azure-na-rest-preview.contentstack.com
      # REACT_APP_CONTENTSTACK_REGION=AZURE-NA
      # REACT_APP_CONTENTSTACK_API_HOST=azure-na-api.contentstack.com

      # API Host, APP Host, Preview Host and Region Environment Variables for Azure Europe region users
      # REACT_APP_CONTENTSTACK_PREVIEW_HOST=azure-eu-rest-preview.contentstack.com
      # REACT_APP_CONTENTSTACK_REGION=AZURE-EU
      # REACT_APP_CONTENTSTACK_API_HOST=azure-eu-api.contentstack.com

      # API Host, APP Host, Preview Host and Region Environment Variables for Google North America region users
      # REACT_APP_CONTENTSTACK_PREVIEW_HOST=gcp-na-rest-preview.contentstack.com
      # REACT_APP_CONTENTSTACK_REGION=GCP-NA
      # REACT_APP_CONTENTSTACK_API_HOST=gcp-na-api.contentstack.com

      # API Host, APP Host, Preview Host and Region Environment Variables for Google Europe region users
      # REACT_APP_CONTENTSTACK_PREVIEW_HOST=gcp-eu-rest-preview.contentstack.com
      # REACT_APP_CONTENTSTACK_REGION=GCP-EU
      # REACT_APP_CONTENTSTACK_API_HOST=gcp-eu-api.contentstack.com

      # By default, branch=main if a branch is not provided
      # REACT_APP_CONTENTSTACK_BRANCH=<your_branch_name>

      SKIP_PREFLIGHT_CHECK=true
      ```

      > **Note:** By default, the Live Preview feature is disabled for this project. To enable it, set `REACT_APP_CONTENTSTACK_LIVE_PREVIEW=true`.

   5. Now, open your terminal, point it to your project location, and run the following commands:

      ```
      npm install
      ```

      ```
      npm start
      ```

   That’s it, you have successfully completed the setup!

   You can now view the website by navigating to `http://localhost:3000`.

   Here's how your website's Home page will look after running on your localhost.

   ![CLI-Bootstrap-LivePage.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt0a8d0af1a144f91c/680f5f2969863dfae9732007/CLI-Bootstrap-LivePage.png)

## Run the Compass Starter

You can easily run the Compass Starter on your local machine by following the steps below:

1. Using Bootstrap Command
   1. Open your terminal.

   2. Navigate to your project folder.

   3. Run the following commands:

      ```
      npm install
      npm start
      ```

2. Build, Configure, and Run the Website (Manual Process)
   1. [Download](https://github.com/contentstack/compass-starter-app/archive/refs/tags/3.2.0.zip) the website code.

   2. Open your terminal.

   3. Navigate to your project folder.

   4. Run the following command to create a configuration file named `.env`:

      ```
      cp .env.sample .env
      ```

      > **Note:** If you are a Windows user, replace `cp` with `copy` in the command above.

      The `.env` file contains all the necessary configuration parameters.

   5. Open it in any code editor or IDE of your choice.

   6. Provide your stack credentials (such as [API key](/docs/headless-cms/view-stack-details/), [Delivery token](/docs/headless-cms/about-delivery-tokens/), and [environment](/docs/headless-cms/about-environments/)), and save the file.

   7. Now, open your terminal, point it to your project location, and run the following commands:

      ```
      npm install
      npm start
      ```

      > **Note:** While running the Compass Starter app on your local machine in development mode, use the command `npm run dev` instead of `npm start`.

That’s it!

You can now view the website by navigating to `http://localhost:3000`.

Here's how your website's Home page will look after running on your localhost.

![CLI-Bootstrap-Compass-Final.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/bltc5de3b5da75780f0/680f5f293b56c245671740c6/CLI-Bootstrap-Compass-Final.png)

## Deploy the Website

You can deploy your Starter app using:

- [Contentstack Launch](https://app.contentstack.com/#!/launch)

  > **Additional Resource:** For more details, visit the [Contentstack Launch documentation](/docs/launch).

- [Vercel](https://vercel.com/)

## Supported Starter Apps

- React JS
- Next JS
- Gatsby
- Angular
- Nuxt JS
- Vue JS
- Stencil

> **Additional Resource:** To create and run a demo website, use the sample code and guide provided in the [Contentstack Starter apps documentation](/docs/headless-cms/nuxt).

## Limitations

- Avoid importing duplicate content types into existing stacks.
- To create new stacks, ensure your role is set to [**Owner**](/docs/administration/about-administration-roles/#organization-owner) or [**Admin**](/docs/administration/about-administration-roles/#organization-admin) in the organization.
