---
uid: "blt66d5de60ef6a5cf1"
seo_title: "Apps CLI Plugin | V2.x.x | Contentstack"
seo_description: "The Contentstack Apps Command-line Interface plugin lets you perform CRUD operations on your Developer Hub apps for your stack."
---

# Apps CLI Plugin

## Overview

Contentstack lets you develop apps in your organization using the [Developer Hub](/docs/developer-hub/about-developer-hub/) portal. With the Apps CLI plugin, Contentstack CLI allows you to perform the CRUD operations on your app in Developer Hub and then use the app in your organization or stack by installing or uninstalling your app as required.

This step-by-step guide lets you install and use the Apps CLI plugin in CLI.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)
- [CLI installed](/docs/headless-cms/install-the-cli) and [configured](/docs/headless-cms/configure-regions-in-the-cli) (version 2.0.0 and above)
- [CLI authenticated](/docs/headless-cms/cli-authentication)

> **Note:** This plugin requires Node.js 22 or later, and it authenticates with your login session rather than a management token. Run `csdx auth:login` before using any `app:` command.

## Install the Apps CLI Plugin

Install the Apps CLI plugin using the following command:

```
csdx plugins:install @contentstack/apps-cli
```

## Commands

The Apps CLI Plugin lets you perform the following operations in Contentstack CLI:

- [Create an App](#create-an-app)
- [Get App Details](#get-app-details)
- [Install an App](#install-an-app)
- [Update an App](#update-an-app)
- [Deploy an App](#deploy-an-app)
- [Reinstall an App](#reinstall-an-app)
- [Uninstall an App](#uninstall-an-app)
- [Delete an App](#delete-an-app)

### Create an App

The `app:create` command allows you to create or register an app in Developer Hub, and optionally, clone a boilerplate locally. Let's perform the following steps to create an app:

1. Open a terminal.

2. Fire the following command:

   ```
   csdx app:create
   ```

3. In the prompt that appears, select a **boilerplate template**.

4. Enter a **name** for your app.

5. Select an **organization**.

6. In the prompt that appears, select **Y** if you want to fetch the app template from GitHub. Else select **n**.
   ![Apps-CLI_Create_Prompt](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/bltf4c1c2f360fb711f/64c27dd1ec43995f77ea04a4/Apps-CLI_Create_Prompt.png)
   With these steps, you have successfully created an app in Developer Hub.
   Alternatively, you can pass the name and organization UID in the command as given below:

   ```
   csdx app:create --name <app_name> --org <organization uid>
   ```

**Usage**

```
csdx app:create
```

**Options**

- `-c`, `--config=config`: \[optional\] Path of the external config.
- `-d`, `--data-dir=data-dir`: \[optional\] Current working directory.
- `--name=name`: \[default: app-boilerplate\] Name of the app to be created.
- `--app-type`: \[default: stack\] Type of app \<options: stack|organization\>.
- `--org`: Provide the organization UID to fetch the app details for the operation.
- `--boilerplate`: Provide a boilerplate \<options: App Boilerplate|DAM App Boilerplate|Ecommerce App Boilerplate\>.

**Examples**

- To create a stack app named App-1:

  ```
  csdx app:create --name App-1 --app-type stack
  ```

- To create an organization app named App-3 by providing the current working directory and the path of the external config:

  ```
  csdx app:create --name App-3 --app-type organization --org <UID> -d ./boilerplate -c ./external-config.json
  ```

### Get App Details

The `app:get` command allows you to get the details of an app in Developer Hub. Let's discuss how to use this command:

1. Open a terminal.

2. Fire the following command:

   ```
   csdx app:get
   ```

3. Select the **organization** in which the app has been created and whose details you want to fetch.

4. Select the required **app** from the displayed list.
   You receive the fetched app data in the `manifest.json` file in your folder.

**Usage**

```
csdx app:get
```

**Options**

- `-d`, `--data-dir=data-dir`: \[optional\] Current working directory.
- `--app-type`: \[default: stack\] Type of app \<options: stack|organization\>.
- `--app-uid`: Provide the app UID of an existing app.
- `--org`: Provide the organization UID to fetch the app details for the operation.

**Examples**

- To fetch the details of a stack app:

  ```
  csdx app:get --org <value> --app-uid <value> --app-type stack
  ```

- To fetch the details of an organization app:

  ```
  csdx app:get --org <value> --app-uid <value> --app-type organization
  ```

### Install an App

The `app:install` command allows you to install an app from Developer Hub to an organization or a stack as shown below:

1. Open a terminal.

2. Fire the following command to install an app:

   ```
   csdx app:install
   ```

3. Select an **organization** from the displayed list.

4. Select the **app** you want to install.

5. If you select a Stack App, then select a **stack** where you want to install the app and the app gets installed successfully.
   Alternatively, you can pass the app UID and the organization UID in the command as given below:

   ```
   csdx app:install --app-uid <app_uid> --org <org_uid>
   ```

**Usage**

```
csdx app:install
```

**Options**

- `--org`: Provide the organization UID to fetch the app details for the operation.
- `--app-uid`: Provide the app UID of an existing app.
- `--stack-api-key`: API Key of the stack where the app operation is to be performed.

**Examples**

- To install an app:

  ```
  csdx app:install
  ```

- To install an app by providing the stack where the app is to be installed:

  ```
  csdx app:install --stack-api-key
  ```

### Update an App

The `app:update` command allows you to update an existing app in Developer Hub.

1. Make the required app updates in the app `manifest.json` file.

2. Open a terminal.

3. Fire the following command to update the app in the UI with respect to the app `manifest.json` file:

   ```
   csdx app:update
   ```

4. Select an **organization** from the displayed list.

5. Enter the **path** to the app `manifest.json` file.

6. Select the **app** you want to update.
   You have successfully updated the app.
   Alternatively, you can pass the app `manifest.json` file path in the command as given below:

   ```
   csdx app:update --app-manifest <file_path>
   ```

**Usage**

```
csdx app:update
```

**Options**

- `--app-manifest`: Path to the app `manifest.json` file.
- `--org`: Provide the organization UID to fetch the app details for the operation.

**Examples**

- To update an app for a provided app manifest file:

  ```
  csdx app:update --app-manifest <value>
  ```

### Deploy an App

The `app:deploy` command in CLI allows you to deploy an app on the [Contentstack Launch](/docs/launch/about-launch/) platform, or on an external platform using [custom hosting](/docs/developer-hub/app-hosting#custom-hosting).

1. Open a terminal.

2. Fire the following command to deploy an app:

   ```
   csdx app:deploy
   ```

3. Select an **organization** from the displayed list.

4. Select the **app** you want to deploy.

5. Select a **Hosting Type**.
   1. If you select **Hosting with Launch**, then select from the following:
      1. **Existing**: Allows you to select an existing Launch project to host your app.

      2. **New**: Creates a new Launch project to host your app.

         > **Note:** When you create a new Launch project (using [GitHub](/docs/launch/import-project-using-github) or [File upload](/docs/launch/import-project-using-file-upload/)) to host your app, you can pass the project parameters in a [config](https://github.com/contentstack/contentstack-apps-cli/blob/main/examples/create-launch-project.json) file.

   2. If you select **Custom Hosting**, enter any custom URL to host your app.

You have successfully deployed an app.  
Alternatively, you can pass the app UID and the organization UID in the command as given below:

```
csdx app:deploy --app-uid <app_uid> --org <org_uid>
```

**Usage**

```
csdx app:deploy
```

**Options**

- `--org`: Provide the organization UID to fetch the app details for the operation.
- `--app-uid`: Provide the app UID of an existing app.
- `--yes`: Use this flag to skip the confirmation.
- `--hosting-type`: Provide a valid Hosting Type. \<options: hosting-with-launch|custom-hosting\>
- `--app-url`: Enter the URL of the app you want to deploy.
- `--launch-project`: Choose a new or an existing Launch project. \<options: existing|new\>
- `--config`: Enter the path of the config file.

**Examples**

- To deploy an app:

  ```
  csdx app:deploy
  ```

- To deploy an app by providing the organization UID and the app UID:

  ```
  csdx app:deploy --org <UID> --app-uid <APP-UID-1>
  ```

- To deploy an app using custom hosting by providing the organization UID and the app UID:

  ```
  csdx app:deploy --org <UID> --app-uid <APP-UID-1> --hosting-type <custom-hosting> --app-url <https://localhost:3000>
  ```

- To deploy an app using an existing Launch project, by providing the organization UID and the app UID:

  ```
  csdx app:deploy --org <UID> --app-uid <APP-UID-1> --hosting-type <hosting-with-launch> --launch-project <existing>
  ```

- To deploy an app using a new Launch project, by providing the organization UID and the app UID:

  ```
  csdx app:deploy --org <UID> --app-uid <APP-UID-1> --hosting-type <hosting-with-launch> --launch-project <new>
  ```

- To deploy an app using a new Launch project, by providing a config file path, the organization UID, and the app UID:

  ```
  csdx app:deploy --org <UID> --app-uid <APP-UID-1> --hosting-type <hosting-with-launch> --launch-project <new> --config <config-path>
  ```

### Reinstall an App

The `app:reinstall` command allows you to reinstall an app from Developer Hub to an organization or a stack.

1. Open a terminal.

2. Fire the following command to reinstall an app:

   ```
   csdx app:reinstall
   ```

3. Select an **organization** from the displayed list.

4. Select the **app** you want to reinstall.

5. If you select a Stack App, select a **stack** where you want to reinstall the app.
   You have successfully reinstalled the app.
   Alternatively, you can pass the app UID and the organization UID in the command as given below:

   ```
   csdx app:reinstall --app-uid <app_uid> --org <org_uid>
   ```

**Usage**

```
csdx app:reinstall
```

**Options**

- `--org`: Provide the organization UID to fetch the app details for the operation.
- `--app-uid`: Provide the app UID of an existing app.
- `--stack-api-key`: API Key of the stack where the app operation is to be performed.

**Examples**

- To reinstall an app:

  ```
  csdx app:reinstall
  ```

- To reinstall an app by providing the stack where the app is to be reinstalled:

  ```
  csdx app:reinstall --stack-api-key
  ```

### Uninstall an App

The `app:uninstall` command allows you to uninstall an app from the organization or stack as shown below:

1. Open a terminal.

2. Fire the following command to uninstall an app:

   ```
   csdx app:uninstall
   ```

3. Select the **organization** which has the app you want to uninstall.

4. Select the **app** you want to uninstall.

5. If you select a Stack App, select the **stack(s)** from where you want to uninstall the app.
   You have successfully uninstalled the app.
   Alternatively, you can pass the app UID and the organization UID in the command as given below:

   ```
   csdx app:uninstall --app-uid <app_uid> --org <org_uid>
   ```

**Usage**

```
csdx app:uninstall
```

**Options**

- `--org`: Provide the organization UID to fetch the app details for the operation.
- `--app-uid`: Provide the app UID of an existing app.
- `--installation-uid`: Provide the installation ID of the app that needs to be uninstalled.
- `--uninstall-all`: Uninstalls the app from all the stacks where it is installed.

**Examples**

- To uninstall an organization app:

  ```
  csdx app:uninstall --org <UID> --app-uid <APP-UID-1>
  ```

- To uninstall an organization app from all the stacks where it is installed:

  ```
  csdx app:uninstall --org <UID> --app-uid <APP-UID-1> --uninstall-all
  ```

- To uninstall an organization app for a given installation ID:

  ```
  csdx app:uninstall --org <UID> --app-uid <APP-UID-1> --installation-uid <INSTALLATION-UID-1>
  ```

### Delete an App

The `app:delete` command allows you to delete an app from Developer Hub as follows:

> **Note**: If you want to delete an installed app, [uninstall the app](#uninstall-an-app) first and then perform the delete operation.

1. Open a terminal.

2. Fire the following command to delete an app:

   ```
   csdx app:delete
   ```

3. Select an **organization** from the displayed list.

4. Select the **app** you want to delete.
   You have successfully deleted the app.
   Alternatively, you can pass the app UID and the organization UID in the command as given below:

   ```
   csdx app:delete --app-uid <app_uid> --org <org_uid>
   ```

**Usage**

```
csdx app:delete
```

**Options**

- `--org`: Provide the organization UID to fetch the app details for the operation.
- `--app-uid`: Provide the app UID of an existing app.

**Examples**

- To delete an app for a given app UID:

  ```
  csdx app:delete --app-uid <value>
  ```

- To delete an organization app for a given app UID:

  ```
  csdx app:delete --app-uid <value> --org <value>
  ```

## Limitations

- If a stack (where the app is installed) gets deleted, you cannot uninstall or delete the app from the organization. Please contact the [support team](mailto:support@contentstack.com) for the next steps.
