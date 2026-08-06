---
uid: "bltc569502a4237c38f"
seo_title: "Bootstrap Starter Apps using the CLI | V0.x.x | Contentstack Documentation"
seo_description: "Learn how to Bootstrap Starter Apps using the CLI"
---

# Bootstrap Starter Apps | Old Commands

The “Bootstrap” plugin in Contentstack CLI allows users to automate the process of project setup for [starter apps](/docs/headless-cms/nuxt).

Using the CLI “Bootstrap” plugin developers can set up projects quickly and effectively. The plugin automates the whole procedure of stack creation and setting up the project.  
Using this plugin, the content types, environments, entries, and assets required to run the starter apps get created in the stack you select or create.

In this guide, we will discuss how to use this plugin and automate the process.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- [Node.js version 16 or above](https://nodejs.org/en/download/)
- CLI installed on your machine: `npm install -g @contentstack/cli`

## Steps for Execution

1. [Log in to Contentstack CLI session](#log-in-to-contentstack-cli-session)
2. [Use the Bootstrap command](#use-the-bootstrap-command)

## Log in to Contentstack CLI session

If you haven't installed the Contentstack CLI yet, follow the steps mentioned in the [CLI installation](/docs/headless-cms/install-the-cli/v1) guide and get it installed.

After you have successfully installed the CLI on your machine, you have to log in to the CLI session to run the ‘Bootstrap’ command.

> **Note**: By default, this CLI session will work for the app hosted in the **North America** region. If you want to switch to **Europe** or **Azure North America** region, follow the steps mentioned in the [**Set Region**](/docs/headless-cms/configure-regions-in-the-cli/v0#set-region) command section.

Now, open your terminal (command prompt) and run the following command to log in to your Contentstack account:

```
csdx auth:login
```

Provide your Contentstack account’s email and password to successfully log in to the CLI session.

> **Additional Resources**: To learn more about the CLI login command, refer to the [**Login command**](/docs/headless-cms/cli-authentication/v0#login) section.

## Use the Bootstrap command

After successfully logging in to Contentstack CLI, run the following command to initiate the procedure:

```
csdx cm:bootstrap
```

This command will prompt you to enter the following details:

1. Technology
2. Path
3. Organization name
4. Stack preference

Let's discuss these options in detail.

1. **Technology**: Select the starter app (the technology type, such as React, Next, and so on) that you want to clone from the GitHub repository, from the available options.
   For our example let's select **React JS** app.![Select the starter app technology](https://images.contentstack.io/v3/assets/blt23180bf2502c7444/blt1f7b8e4c628aa6cb/62b58c0e64a9600f86bb77c0/Select_the_starter_app_technology.png)
2. **Path**: Once you have selected the app, provide the folder path to copy the app's source code.
   According to your preference, provide the folder path by selecting the **Other** option or you can use the **Current** directory as a default option.
   This will start cloning the selected app to the folder you provide.![Folder path to copy the source code](https://images.contentstack.io/v3/assets/blt23180bf2502c7444/bltd2925f19f328565a/62b58c0d64a9600f86bb77bc/Folder_path_to_copy_the_source_code.png)
3. **Organization name**: Now, **Select an Organization** from the list of your organizations.
   The cloned app content will be added to a stack in the organization you select.![Select an organization](https://images.contentstack.io/v3/assets/blt23180bf2502c7444/bltd384cc10c107e997/62b58c0e919dfb0f9bf008c2/Select_an_organization.png)
4. **Stack preference**: In the organization you picked above, select if you want to create a **new stack** or use an **existing stack** to import the content of the app.
   For this example let's create a **new stack** in the organization we selected.![Stack preference for the starter app](https://images.contentstack.io/v3/assets/blt23180bf2502c7444/bltb3d45ffff40185cd/62b58c0e4d83761026d9c2c6/Stack_preference_for_the_starter_app.png)
5. Accordingly, add the **Name of the Stack** where you want to import the project content and click the **Enter** button to start importing the project to the stack.![Importing the project to a stack](https://images.contentstack.io/v3/assets/blt23180bf2502c7444/blt165ada16fbd07ef0/62b58c0ef8ac3b0f97e1162b/Importing_the_project_to_a_stack.png)
6. On providing the above details, the plugin will add the project content including fields, and assets. It will also set up the environments, languages, and other settings for the selected app.

> **Note**: Imported content will be automatically published in the target stack.

This is how you can automate the process of project creation in Contentstack by using the Bootstrap command.

The alternate way of using the plugin is by providing the required parameters after the command in a single line as shown below:

```
csdx cm:bootstrap -s <starterapp> -t <optional github private repo token> -a <app name> -d "<path or the location of the folder to clone the app>"
```

**Options**:

- `-t`, `--accessToken=accessToken`: (optional) The token of your private repo to access the project.
- `-s`, `--appType=appType`: Sample or Starter app
- `-a`, `--appName=appName`: The app name of the starter app.
  For eg. **reactjs-starter**, **nextjs-starter**, **gatsby-starter**, **angular-starter**, **nuxt-starter**.
- `-d`, `--directory=directory`: Specify the path or the location of the folder to clone the app.

**Examples:**

- To select the app you want to clone, use this command:

  ```
  csdx cm:bootstrap -a <app name>
  ```

  For Eg. To clone content of a **React JS** app:

  ```
  csdx cm:bootstrap -a reactjs-starter
  ```

- This is an optional command to be used if you want to clone a project from a private GitHub repository.

  Provide the token of the private repository.

  ```
  csdx cm:bootstrap -t <github private repo token>
  ```

- Use this command to provide the path to the location of the folder to clone the app:

  ```
  csdx cm:bootstrap -d "<The path or the location to clone the app>"
  ```

  For Eg.

  ```
  csdx cm:bootstrap -d "C:\Users\Name\Desktop\cli\content"
  ```

The above command will add the starter app’s (**React JS**) content to your stack as shown below:

![image.png](https://images.contentstack.io/v3/assets/blt23180bf2502c7444/blt80928c2db849ad9e/6151c5ff64c8007a9bdecb26/image.png)

## Run the Starter Apps

You can easily run this starter app on your local machine by following the steps below:

### Build, Configure and Run the Website (Manual Process)

Download the website code from our [GitHub repository](https://codeload.github.com/contentstack/contentstack-react-starter-app/zip/refs/heads/master).

After downloading the website code, navigate to the root folder and **create** a configuration file named **.env.development.**,

Provide your stack credentials like [API key](/docs/headless-cms/view-stack-details), [Delivery token](/docs/headless-cms/about-delivery-tokens), and [environment](/docs/headless-cms/about-environments):

```
REACT_APP_CONTENTSTACK_API_KEY = <api_key_of_your_stack>
REACT_APP_CONTENTSTACK_DELIVERY_TOKEN = <delivery_token_of_the_environment>
REACT_APP_CONTENTSTACK_ENVIRONMENT = <environment_name>
REACT_APP_CONTENTSTACK_LIVE_PREVIEW= true
```

> **Note:** By default, the Live Preview feature is disabled for this project. To enable it, set `REACT_APP_CONTENTSTACK_LIVE_PREVIEW= true`.

Now, fire up your terminal, point it to your project location, and run the following commands:

```
npm install
npm start
```

That’s it!  
You can now view the website at **http://localhost:3000**.  
Here's how your website's **Home** page will look after running on your localhost. ![Dashboard.jpg](https://images.contentstack.io/v3/assets/blt23180bf2502c7444/blt09f74db8c2a8c8dc/638712a175befa109d301774/Dashboard.jpg)

### Deploy the Website

The easiest and the quickest way to deploy the React JS starter website on production is to use Vercel.  
You need a [Vercel account](https://vercel.com/signup) before you start deploying.

> **Note**: During deployment, to use the European or Azure North American region, add an environment variable **REACT_APP_CONTENTSTACK_REGION** and set its value to **eu** or **azure-na** respectively**.**

The Bootstrap plugin supports the following starter apps.

Starter Apps

- React JS
- Next JS
- Gatsby
- Angular
- Nuxt JS

> **Additional Resource**: To create and run a demo website, use the sample code and guide provided in the Contentstack starter apps [documentation](/docs/headless-cms/nuxt).

**Limitations:**

1. When importing content to an existing stack, make sure you don't add duplicate content types. If you try to add similar content types, you'll get an error.
2. If you want to create a new stack for storing content, make sure you have the “[owner](/docs/administration/about-administration-roles#organization-owner)” or “[admin](/docs/administration/about-administration-roles#organization-admin)” rights in that organization.
