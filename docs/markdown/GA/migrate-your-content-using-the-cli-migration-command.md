---
uid: "blt563cc44829432a89"
seo_title: "Migrate your Content using the CLI Migration Command | Contentstack"
seo_description: "Migrate content effortlessly using Contentstack’s new Command-line Interface migration command to simplify and speed up content transfer."
---

# Migrate your Content using the CLI Migration Command

The `migration` command in Contentstack CLI allows developers to automate the content migration process using a custom migration script.

This guide explains how to migrate your content using the CLI migration plugin. We have provided sample migration scripts that developers can use to get started, or you can write your custom scripts.

Developers can validate the deployment before pushing it on production, using a test space to run the migration scripts.

> **Additional Resource**: For more information, refer to the [migration API documentation](https://github.com/contentstack/cli/blob/v2.0.0-beta/packages/contentstack-migration/docs/api-reference.md) and [advanced examples](https://github.com/contentstack/cli/tree/v2.0.0-beta/packages/contentstack-migration/examples).

## Process Overview

The first step is to write a migration script to perform content migration. We have provided sample migration scripts which you can refer [here](/docs/headless-cms/migrate-your-content-using-the-cli-migration-command#get-started-with-the-migration-script), or write custom scripts. Furthermore, you can use various methods and SDK instances to make your migration script easy to write and read.

After writing the migration script, use the CLI migration command to migrate your content to the destination stack.

Now let us understand how to migrate content from one stack to another using the CLI migration command.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login)
- CLI [installed](/docs/headless-cms/install-the-cli) on your machine

## Steps for Execution

1. [Login to Contentstack CLI session](#login-to-contentstack-cli-session)
2. [Use the “Migration” command](#use-the-migration-command)

## Login to the Contentstack CLI session

Firstly you should have the Contentstack CLI installed on your system. In case you haven't yet installed the Contentstack CLI, please follow the steps in the [CLI installation](/docs/headless-cms/install-the-cli) guide.

After installing the CLI on your machine, log in to the CLI session to run the `migration` command.

> **Note**: By default, the CLI session will work for the app hosted in the **AWS North America** region. If you want to switch to **AWS Europe**, **AWS Australia, Azure North America**, **Azure Europe**, **Google North America**, or **Google Europe** region, follow the steps mentioned in the [Set Region](/docs/headless-cms/configure-regions-in-the-cli#set-region) command section.

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
csdx cm:stacks:migration
```

Along with the migration command, users have to define various parameters to successfully migrate the content.

In order to add a number of options/parameters in a single line, use the following command:

**Usage:**

If management token is not specified, by default migration plugin uses Auth token:

```
csdx cm:stacks:migration --file-path <file_path> -k <api_key>
```

Migrate content using CLI Management token alias:

```
csdx cm:stacks:migration -a <alias> --file-path <file_path> -k <api_key>
```

**Options:**

- `-a`,`--alias=alias`: Use this flag to add the management token alias. You must use either the `--alias` flag or the `--stack-api-key` flag.
- `-k`, `--stack-api-key=stack-api-key`: Use this flag to add the API key of your stack. You must use either the `--stack-api-key` flag or the `--alias` flag.
- `--file-path=file-path`: Use this flag to provide the path of the file of the migration script.
- `--multiple=multiple`: This flag helps you to migrate multiple content files in a single instance. Mention the folder path where your migration script files are stored.
- `--branch=branch`: Use this flag to add the branch name where you want to perform the migration. (target branch name)
- `--config=config`: \[*optional*\] Inline configuration, \<key1\>:\<value1\>. Passing an external configuration makes the script re-usable.
- `--config-file=config-file`: \[*optional*\] Path of the JSON configuration file.

**Example**:

- ```
  csdx cm:stacks:migration -a my_token_alias --config contentTypeUID:author --file-path “path/to/migrate/single/contenttype/modification/script/file”
  ```
- ```
  csdx cm:stacks:migration -k bxxxxxxx --config  numberOfEntries:100 contentTypeUID:blog --file-path “path/to/update/first/100/entries/of/given/contenttype/script/file”
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

> **Note:** Developers can modify the code to meet their specific requirements.

Let's discuss the objects we used in the above example.

```
“migration”
```

This refers to your migration object. The migration object has some predefined methods to perform various tasks like create, edit, and so on.  
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

```
“stackSDKInstance”
```

This is an SDK instance initiated with an API key and the authentication method is chosen via the CLI.

This is an optional object users can add to customize tasks that are not supported by the migration script.

Currently, the migration script only supports **content type-related methods**. To extend your migration further, you can use this pre-initiated SDK instance to run the file via the CLI.

Consider this example where we are creating an **entry** for the **Blog** content type.

```
module.exports = async ({ migration, stackSDKInstance }) => {
  const createEntryTask = () => {
    return {
      title: "Create blog entries",
      successMessage: "Entry created successfully",
      failedMessage: "Failed to create entry",
      task: async () => {
        try {
          let entry = {
            title: `Awesome Blog`,

            url: `/awesome-blog`,
          };

          await stackSDKInstance
            .contentType("blog")
            .entry()
            .create({ entry });
        } catch (error) {
          throw error;
        }
      },
    };
  };

  migration.addTask(createEntryTask());
};
```

Carefully observe the SDK instance we have added to this example which extends our migration script and enables us to perform operations with entries in the content type.

Similar to the previous example, the last line of the code defines the migration task and adds this method to the existing migration tasks list for execution.

> **Additional Resource**: For more information, refer to the [migration API documentation](https://github.com/contentstack/cli/blob/v2.0.0-beta/packages/contentstack-migration/docs/api-reference.md) and [advanced examples](https://github.com/contentstack/cli/tree/v2.0.0-beta/packages/contentstack-migration/examples).

### Execute the Migration File

After configuring the migration script file, you can proceed to run the file via Contentstack CLI to complete the migration.

If management token is not specified, by default migration plugin uses Auth token:

```
csdx cm:stacks:migration --file-path <file_path> -k <api_key>
```

Migrate content using management token alias:

```
csdx cm:stacks:migration -a <alias> --file-path <file_path> -k <api_key>
```

> **Additional Resource**: Check out our GitHub repository for detailed information on the migration script and various [advanced options & examples](https://github.com/contentstack/cli/tree/v2.0.0-beta/packages/contentstack-migration/examples).

> **Warning:** CLI migration plugin is not ideal for branch merge.

## Points to Remember

1. Currently, you can pass a custom schema to the **createField** method to migrate group fields.
2. You can migrate global fields by creating an SDK instance and adding it to content types using the **createField** method.
3. Currently, you can migrate entries by creating an SDK instance to **create**/**update**/**delete** entries for your content type.
