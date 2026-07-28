---
uid: "bltce91c490961bf924"
seo_title: "Migrate your Content using the CLI Migration Command | Old Commands | Contentstack"
seo_description: "Effortlessly migrate your content with Contentstack's CLI Migration Command."
---

# Migrate your Content using the CLI Migration Command | Old Commands

The “Migration” plugin in Contentstack CLI allows developers to automate the content migration process using a custom migration script.

This guide explains how to migrate your content using the CLI migration plugin. We have provided sample migration scripts that developers can use to get started, or you can write your custom scripts.

Developers can validate the deployment before pushing it on production, using a test space to run the migration scripts.

> **Additional Resource**: For more information, refer the [migration API documentation](https://github.com/contentstack/cli-plugins/blob/main/packages/contentstack-migration/docs/api-reference.md) and [advanced examples](https://github.com/contentstack/cli-plugins/tree/main/packages/contentstack-migration/examples).

## Process Overview

The first step is to write a migration script to perform content migration. We have provided sample migration scripts which you can refer [here](/docs/headless-cms/migrate-your-content-using-the-cli-migration-command#get-started-with-the-migration-script), or write custom scripts. Furthermore, you can use various methods and SDK instances to make your migration script easy to write and read.

After writing the migration script, use the CLI migration command to migrate your content to the destination stack.

Now let us understand how to migrate content from one stack to another using the CLI migration command.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- [Node.js version 16 or above](https://nodejs.org/en/download/)
- CLI installed on your machine: `npm install -g @contentstack/cli`

## Steps for Execution

1. [Login to Contentstack CLI session](#login-to-contentstack-cli-session)
2. [Use the “Migration” command](#use-the-migration-command)

## Login to the Contentstack CLI session

Firstly you should have the Contentstack CLI installed on your system. In case you haven't yet installed the Contentstack CLI, please follow the steps in the [CLI installation](/docs/headless-cms/install-the-cli) guide.

After installing the CLI on your machine, log in to the CLI session to run the ‘Migration’ command.

> **Note**: By default, the CLI session will work for the app hosted in the **North America** region. If you want to switch to **Europe** or **Azure North America** region, follow the steps mentioned in the [Set Region](/docs/headless-cms/configure-regions-in-the-cli#set-region) command section.

Now log in to your Contentstack account, by running the following command in your terminal:

```
csdx auth:login
```

Provide your Contentstack account’s email and password to successfully login to the CLI session.

> **Additional Resources**: To learn more about the CLI login command, refer to the [Login command](/docs/headless-cms/cli-authentication#login) section.

## Use the “Migration” Command

Once you log in to Contentstack, run the migration command to initiate the procedure.

To perform the operation you have to write a migration script in your code editor, and mention its file path while using the migration command.

> **Tip:** We have created a sample migration script for you to get started, which we have discussed further in this guide. Refer [this](/docs/headless-cms/migrate-your-content-using-the-cli-migration-command#get-started-with-the-migration-script) section, to understand migration scripts and various methods you can use to execute your tasks.

We assume that you have a migration script ready with you, to migrate the content.

Now, run the following command to start migrating your content.

**Usage:**

```
csdx cm:migration
```

Along with the migration command, users have to define various parameters to successfully migrate the content.

In order to add a number of options/parameters in a single line, use the following command:

**Usage:**

Migrate content using Auth token:

```
csdx cm:migration -A -n <filepath> -k <api_key>
```

Migrate content using CLI Management token alias:

```
csdx cm:migration -a <management_token_alias> -n <file_path> -k <api_key>
```

**Options:**

- `-A`, `--auth-token`: Add this flag to use the auth token of the current session. After logging in to CLI, an auth token is generated for each new session.
- `-a`, `--management-token-alias=management-token-alias`: Use this flag to add the management token alias.
- `-k`, `--api-key=api-key`: Use this flag to add the API key of your stack.
- `-n`, `--file-path=filepath`: Use this flag to provide the path of the file of the migration script.
- `--multi`: This flag helps you to migrate multiple content files in a single instance. Mention the folder path where your migration script files are stored.
- `-B`, `--branch=branch`: Use this flag to add the branch name where you want to perform the migration. (target branch name)
- `--config=config`: \[*optional*\] Inline configuration, \<key1\>:\<value1\>. Passing an external configuration makes the script re-usable.
- `--config-file=config-file`: \[*optional*\] Path of the JSON configuration file.

**Example**:

- Example 1:

  ```
  csdx cm:migration -A -n "path/to/transform-contenttype/script/file" -k bxxxxxxx
  ```

- Example 2:

  ```
  csdx cm:migration -a my_token_alias  -k bxxxxxxx --config contentTypeUID:author -n “path/to/migrate/single/contenttype/modification/script/file”
  ```

- Example 3:

  ```
  csdx cm:migration -a my_token_alias -k bxxxxxxx --config  numberOfEntries:100 contentTypeUID:blog -n “path/to/update/first/100/entries/of/given/contenttype/script/file”
  ```

In the next section, let’s understand how to create the migration files and use various methods to perform operations in your stack.

## Get Started with the Migration Script

Now let’s understand how to create and execute migration scripts using Contentstack CLI. Furthermore, we will discuss various methods for making migration scripts easier to write and more readable.

### Create Migration File

First, determine the location where the migration script will be written. The migration script file will be exported when the migration command is run, accordingly, you can decide the location.

Now, you must specify the file path of the migration script to run the migration process, as mentioned in the migration command.

Developers can use JavaScript to create migration scripts that specify changes to a content model.

Here’s a sample code snippet for you to get started. Copy the sample code and initiate with your migration script.

```
'use strict';

module.exports = async ({migration, stackSDKInstance}) => {

     // write your scripts here

})
```

The script file of the code should have a function exported as default, that's the method where the scripts reside.

> **Note:** Developers can alter the code and make changes according to their own requirements.

Let's discuss the objects we used in the above example.

`“migration”` : This refers to your migration object. The migration object has some predefined methods to perform various tasks like create, edit, and so on.  
Using these methods you can define the tasks and write other tasks to execute them.

Consider this example, where we have defined a method for creating the **Blog** content type.

```
module.exports = async ({ migration, stackSDKInstance }) => {
  const blog = migration
    .createContentType("blog")
    .title("Blog")
    .description('The is Blog content type')
    .isPage(true)
    .singleton(false);  
blog
    .createField("title")
    .display_name("Title")
    .data_type("text")
   .mandatory(true); 
blog
       .createField("url")
       .display_name("URL")
      .data_type("text")
      .mandatory(true); 

 migration.addTask(blog.getTaskDefinition());
};
```

The last line of the code defines the migration task to execute the method.  
Below we have mentioned various methods you can use to easily perform migration.

`“stackSDKInstance”` : This is an SDK instance initiated with API key and the authentication method is chosen via the CLI.

This is an optional object users can add to customize tasks that are not supported by the migration script.

Currently, the migration script only supports **content type-related methods**. To extend your migration further, you can use this pre-initiated SDK instance to run the file via the CLI.

Consider this example where we are creating an entry for the **Blog** content type.

```
module.exports = async ({migration, stackSDKInstance}) => {

    let createEntryTask = {

    title: 'Create blog entries',

    task: [async (params) => {

      try {

        let entry = {

          title: `Awesome Blog`,

          url: `/awesome-blog`

        }

        await stackSDKInstance.contentType('blog').entry().create({ entry })

      } catch (error) {

        throw error

      }

    }]

  }

  migration.addTask(createEntryTask);

}
```

Carefully observe the SDK instance we have added to this example which extends our migration script and enables us to perform operations with entries in the content type.

Similar to the previous example, the last line of the code defines the migration task and adds this method to the existing migration tasks list for execution.

> **Additional Resource**: For more information, refer to the [migration API documentation](https://github.com/contentstack/cli-plugins/blob/main/packages/contentstack-migration/docs/api-reference.md) and [advanced examples](https://github.com/contentstack/cli-plugins/tree/main/packages/contentstack-migration/examples).

### Execute the Migration File

After configuring the migration script file, you can proceed to run the file via Contentstack CLI to complete the migration.

Migrate content using Auth token:

```
csdx cm:migration -A -n <file_path> -k <api_key>
```

OR

Migrate content using management token alias:

```
csdx cm:migration -a <management_token_alias> -n <file_path> -k <api_key>
```

> **Additional Resource**: Check out our GitHub repository for detailed information on the migration script and various [advanced options & examples](https://github.com/contentstack/cli-plugins/tree/main/packages/contentstack-migration/examples).

## Points to Remember

1. Currently, you can pass a custom schema to the **createField** method to migrate group fields.
2. You can migrate global fields by creating an SDK instance and adding it to content types using the **createField** method.
3. Currently, you can migrate entries by creating an SDK instance to **create**/**update**/**delete** entries for your content type.
