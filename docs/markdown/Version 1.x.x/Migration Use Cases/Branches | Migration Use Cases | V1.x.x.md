---
uid: "bltd48fe0ffb5cf8b08"
seo_title: "Branches | Migration Use Cases | V1.x.x | Contentstack"
seo_description: "Branches | Migration Use Cases"
---

# Branches | Migration Use Cases

## Overview

The branches feature in Contentstack allows you to create multiple copies of your stack. You can add numerous branches of your stack and migrate your content to these branches.

[Branches](/docs/headless-cms/about-branches) primarily help you sync between your code and content model without making significant changes to the code.

Using the Contentstack CLI's Migration plugin, you can migrate your content from one branch to another using a **migration script**.

> **Note:** Branch merging is not currently automated as it can impact your production data and is a sensitive operation. You can use the existing scripts to perform the same function. Here are some [sample scripts](https://github.com/contentstack/cli/tree/v2.0.0-beta/packages/contentstack-migration/examples) to perform the branch merge action.

> **Additional Resource**: We recommend you to refer to our extensive guide on [migration plugin and how to write a migration script](/docs/headless-cms/migrate-content-between-stacks-using-the-cli/v1) for your content or refer our [GitHub](https://github.com/contentstack/cli/tree/v2.0.0-beta/packages/contentstack-migration/examples) page.

In this guide, let's look at different possible use case scenarios where you can use the CLI migration plugin to migrate your content from one branch to another by writing a migration script.

Here are a few possible scenarios where you can use the migration plugin to migrate your content.

1. [Rename or Remove a Field in your Content Type](#rename-or-remove-a-field-in-your-content-type)
2. [Update Content Models](#update-content-models)

Let's understand each use case in detail.

> **Note**: We assume you are well versed with the migration script and migration plugin. If not, read our detailed documentation on how to [get started with the migration script](/docs/headless-cms/migrate-content-between-stacks-using-the-cli/v1#get-started-with-the-migration-script) and [use the migration plugin](/docs/headless-cms/migrate-content-between-stacks-using-the-cli/v1) to migrate your content.

## Rename or Remove a Field in your Content Type

Consider a scenario where you want to apply a minor change to your content type. In this example, let's understand how to rename/remove a field in your content type using branches.

To do this, follow the steps given below:

1. Create a develop branch from your main (production) branch for your stack to store the updated content.

2. Now, add the following tasks in your migration script to perform the respective operations:
   1. Begin by adding a task to create a new field with the latest (updated) field name in your content type.

   2. Write tasks to add the data and update the entries with the newly created field.

      > **Warning**: We recommend you to keep the existing fields and optionally delete the old fields after your latest changes are published live. This will help you easily rollback, in case the new changes are not as expected.

      > **Additional Resource**: We recommend, you check some example scripts on our [GitHub page](https://github.com/contentstack/cli/tree/v2.0.0-beta/packages/contentstack-migration/examples). This will help you get started with the tasks mentioned above.

   3. Now, check your script, finalize the content and add a [task to publish](https://github.com/contentstack/cli/blob/v2.0.0-beta/packages/contentstack-migration/examples/02-publishing-entries.js) it.

3. You can move to your UI and make appropriate changes to the UI. Make other suitable changes at your end and start using the newly created field.

4. Content editors can verify the changes and content managers can confirm the changes on the develop (test) branch.

5. Use the migration plugin command given below to apply your changes to the main branch. If the management token is not specified, by default the migration plugin uses Auth token.

   ```
   csdx cm:stacks:migration --file-path <file_path> -k <api_key> --branch <branch_name>
   ```

> **Note**: Make sure, while running the script, it should point to the target branch.

While deploying, remember to deploy the migration script first and then deploy the UI.

![image.png](https://images.contentstack.io/v3/assets/blt23180bf2502c7444/bltb51352a6cc656abe/618a967cb23afd5860107a6a/image.png)

## Update Content Models

This is a complex use case where you want to make some significant changes to your stack. While revamping your website's content models or restructuring your application, you have to include some major updates to your stack.

Consider an example where you want to update the content models of your stack. Let's see the steps involved in executing this example using branches:

1. Begin by creating a branch from the main (production) branch of your stack, where the new models will be stored.

2. Then, update the migration script and write custom tasks to modify the existing content models according to the new changes.
   Add the following tasks to your migration script to perform the respective operations:
   1. Begin by creating tasks to update the content models.

   2. Add tasks to update the entries according to the new content models by adding your data to these entries.

   3. Once all the changes are done, add a [task to your migration script to publish](https://github.com/contentstack/cli/blob/v2.0.0-beta/packages/contentstack-migration/examples/02-publishing-entries.js) the changes.

      > **Additional Resource**: We recommend you check some [example scripts](https://github.com/contentstack/cli/tree/v2.0.0-beta/packages/contentstack-migration/examples) on our GitHub page. This will help you get started with the tasks mentioned above.

3. Now you can move to the UI and make appropriate changes. You can also make other suitable changes at your end.

4. After applying the changes, content editors can verify the changes and content managers can confirm the changes on the develop (test) branch.

5. Use the following migration plugin command to migrate your content to the newly created release branch.

   ```
   csdx cm:stacks:migration --file-path <file_path> -k <api_key> --branch <branch_name>
   ```

   > **Note**: Make sure, while running the script, it should point to the target branch.

6. Finally, you can deploy all the changes on your production branch. This can be done in the following two ways:
   - **Use an Alias for Release**:  This is an efficient way to apply new changes to your existing content. To use this method, create a production alias that points to the release branch.

     > **Additional Resource**: Read our detailed guide on [how to use aliases](/docs/headless-cms/about-branches#work-with-aliases) in content branching.

     > **Note**: By using an alias for release, you can eliminate the risk of data loss. In case of any errors, it will by default rollback to the old code/branch.

   - **Merge All your Changes with the Main Branch**: You can easily merge your content from the release branch to the main branch. This can help you merge data with the main branch and apply the changes.

   > **Note**: We recommend you to use this method only if your changes are minimal and can be easily merged with the main branch.

7. While deploying, remember to deploy the migration script first and then deploy the UI.

8. If your changes are working properly after deployment, you can merge them into your main branch. This will help you to keep a single original branch.
   ![image.png](https://images.contentstack.io/v3/assets/blt23180bf2502c7444/blt11e3ede5971ccc10/618a96bd953e1e65040092f6/image.png)

> **Additional Resource**: We highly recommend you to check our [GitHub](https://github.com/contentstack/cli/tree/v2.0.0-beta/packages/contentstack-migration/examples) page for more information on [migration script creation, use cases,](https://github.com/contentstack/cli/blob/v2.0.0-beta/packages/contentstack-migration/docs/api-reference.md) and [advanced examples](https://github.com/contentstack/cli/tree/v2.0.0-beta/packages/contentstack-migration/examples).
