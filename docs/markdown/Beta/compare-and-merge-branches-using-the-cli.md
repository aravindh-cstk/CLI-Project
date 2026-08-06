---
uid: "blt1f5e428e3a8d3734"
seo_title: "Compare and Merge Branches Using the CLI | V2.x.x | Contentstack"
seo_description: "Learn to create, update, delete, compare, and merge branches using the Contentstack Command-line Interface with this step-by-step guide."
---

# Compare and Merge Branches Using the CLI | V2.x.x Beta

Contentstack provides [Branches](/docs/headless-cms/about-branches/) to create multiple copies of your [stack](/docs/headless-cms/about-stack/) content. By default, stacks have a **main** branch. You can fork a branch from the main branch (parent branch) to create a new branch (child branch).

Contentstack lets you list, create, delete, compare, and merge Branches using the CLI. You can compare two branches and merge the two with the desired changes into a single branch.

This step-by-step guides you on how to create, update, delete, compare, and merge Branches using the CLI. In the CLI, the **base branch** refers to the ***target*** branch, while the **compare branch** is the ***source*** branch.

## Prerequisites

- [Contentstack account](https://www.contentstack.com/login/)

- [CLI installed](/docs/headless-cms/install-the-cli/v1) and configured (version 1.7.0 and above)

- [CLI authenticated](/docs/headless-cms/cli-authentication)

- [Branches](/docs/headless-cms/about-branches/) enabled for your organization.

  > **Note:** Contact your organization administrator for more details.

## Steps to List, Create, and Delete Branches

You can list the branches in a stack, create a new branch in a stack from a base branch, and delete an existing branch from a stack.

### List Branches

1. Open a terminal.

2. Run the following command to list the available branches:

   ```
   csdx cm:branches
   ```

3. The CLI prompts you to enter a Stack API key. To list the branches of a specific stack, enter its **Stack API key**.

   You can see the branches for the specific stack displayed.

   Alternatively, you can pass the **Stack API key** in the command as given below:

   ```
   csdx cm:branches --stack-api-key <value>
   ```

   You can also view the list in a detailed view using the `verbose` flag:

   ```
   csdx cm:branches --verbose
   ```

**Usage**

```
csdx cm:branches
```

or

```
csdx cm:branches -k <value>
```

or

```
csdx cm:branches --stack-api-key <value>
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--stack-api-key` | `-k` | Stack API key. |
| `--verbose` | - | Verbose display information in detailed format. |

### Create a Branch

1. Open a terminal.

2. Run the following command to create a new branch:

   ```
   csdx cm:branches:create
   ```

3. Enter the **Stack API key** of the stack for which you want to create a branch.

4. Enter a **source branch** for the branch you want to create.

5. Enter a **unique ID** (name) for branch UID.

You have successfully created a new branch.

Alternatively, you can pass the **Stack API key**, **source**, and **UID** in the command as given below:

```
csdx cm:branches:create --stack-api-key <value> --source <value> --uid <value>
```

**Limitations**

- The branch UID must be in lowercase. Only ‘_’ can be used to separate two words.
- The UID must not exceed **15 characters**.
- The maximum number of branches allowed per stack depends on the product tier.
- Once you create a branch, you cannot edit its name or the source branch.

**Usage**

```
csdx cm:branches:create
```

or

```
csdx cm:branches:create --stack-api-key <value> --source <value> --uid <value>
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--uid` | - | Branch UID (unique name) to be created. |
| `--source` | - | Source branch from which a new branch is to be created. |
| `--stack-api-key` | `-k` | Stack API key. |

### Delete a Branch

1. Open a terminal.

2. Run the following command to delete a branch:

   ```
   csdx cm:branches:delete
   ```

3. Enter the **Stack API key** of the stack from which you want to delete a branch.

4. Enter the **UID** of the branch you want to delete.

5. To confirm the deletion, you are prompted to type the **name** of the branch you want to delete.

You have successfully deleted a branch.

Alternatively, you can pass the **Stack API key** and **UID** in the command as given below, and then in the following step, when prompted, enter the **name** of the branch to confirm the deletion.

```
csdx cm:branches:delete --stack-api-key <value> --uid <value>
```

To skip confirmation and delete the branch forcefully:

```
csdx cm:branches:delete --stack-api-key <value> --uid <value> --yes
```

**Usage**

```
csdx cm:branches:delete
```

or

```
csdx cm:branches:delete --stack-api-key <value> --uid <value>
```

or

```
csdx cm:branches:delete --stack-api-key <value> --uid <value> --yes
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--uid` | - | Branch UID to be deleted. |
| `--stack-api-key` | `-k` | Stack API key. |
| `--yes` | `-y` | Force the deletion of the branch by skipping the confirmation. |

**Examples**

- To list out the branches in a stack:

  ```
  csdx cm:branches --stack-api-key bltxxxxxxxx7
  ```

- To create a new branch in a stack:

  ```
  csdx cm:branches:create --stack-api-key bltxxxxxxxx7 --source test1 --uid test2
  ```

- To delete a branch from a stack:

  ```
  csdx cm:branches:delete --stack-api-key bltxxxxxxxx7 --uid test2
  ```

## Steps to Configure Base Branches

You can set, get, or remove the default base branch for a stack. This will be used as the default base branch when performing a compare or merge command and will act as the target branch where the final changes will be merged during the merge operation.

### Set

1. Run the following command to set a base branch:

   ```
   csdx config:set:base-branch
   ```

2. Enter the **Stack API key** of the stack where you want to set the base branch.

3. Enter the **name** of the branch you want to set as the base branch.

   Alternatively, you can pass the **Stack API key** and base branch **name** in the command as given below:

   ```
   csdx config:set:base-branch --stack-api-key <value> --base-branch <value>
   ```

**Usage**

```
csdx config:set:base-branch
```

or

```
csdx config:set:base-branch --stack-api-key <value> --base-branch <value>
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--stack-api-key` | `-k` | Stack API key. |
| `--base-branch` | - | Base branch (Target branch). |

### Get

1. Run the following command to get the base branch:

   ```
   csdx config:get:base-branch
   ```

   The base branch will be displayed along with the Stack API key.

**Usage**

```
csdx config:get:base-branch
```

### Remove

1. Run the following command to remove a base branch:

   ```
   csdx config:remove:base-branch
   ```

2. Enter the **Stack API key** of the stack for which you want to remove the base branch.

3. When prompted, enter **Y** to remove the base branch.

   Alternatively, you can pass the **Stack API key** in the command as given below, and then when prompted, enter **Y** to remove the base branch.

   ```
   csdx config:remove:base-branch --stack-api-key <value>
   ```

   To forcefully remove the base branch by bypassing the confirmation step, pass the command as given below:

   ```
   csdx config:remove:base-branch --stack-api-key <value> --yes
   ```

**Usage**

```
csdx config:remove:base-branch
```

or

```
csdx config:remove:base-branch --stack-api-key <value>
```

or

```
csdx config:remove:base-branch --stack-api-key <value> --yes
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--stack-api-key` | `-k` | Stack API key. |
| `--yes` | `-y` | Force remove. |

**Examples**

- To set a base branch in a stack:

  ```
  csdx config:set:base-branch --stack-api-key bltxxxxxxxx7 --base-branch test2
  ```

- To remove the base branch from a stack:

  ```
  csdx config:remove:base-branch --stack-api-key bltxxxxxxxx7 --yes
  ```

## Steps to Compare Branches

Follow the steps below to compare two branches:

1. Run the following command to compare two branches:

   ```
   csdx cm:branches:diff
   ```

2. Enter the **Stack API key** of the stack where you want to compare branches.

3. Enter the **name** of the base branch.

4. Enter the **name** of the compare branch.

5. When prompted, select a specific **module** or all modules of the branch to compare.

   Alternatively, you can pass the **Stack API key**, **base branch** (target branch), and **compare branch** (source branch) in the command as given below:

   ```
   csdx cm:branches:diff --stack-api-key <value> --base-branch <value> --compare-branch <value> --module <value>
   ```

   > **Note**: To choose a base branch other than the default, specify the `--base-branch` flag as given in the command above.

   You get the comparison results as displayed below:

   ![Branches_CM_CompareRegular.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt35efc4b1c5fbd0ff/644a3f77de40d20defb3d5af/Branches_CM_CompareRegular.png)

   The CLI displays the branch comparison summary along with the modules affected.

6. Pass the `format` flag as given below to get detailed branch comparison results.

   ```
   csdx cm:branches:diff --stack-api-key <value> --base-branch <value> --compare-branch <value> --format detailed-text
   ```

   You get the detailed comparison results as displayed below:

   ![Branches_CM_CompareFormatNew.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt6b002bfb288ed5b9/64510c3b1276ca183e1c23d0/Branches_CM_CompareFormatNew.png)

   This displays the branch comparison summary, showing modules and the affected sub-modules. In our example, the content types are displayed along with their fields.

   The comparison results are distinguished based on the following:
   - A “+” symbol with green highlighted text: Indicates that this is present only in the compare branch.
   - A “±” symbol with blue highlighted text: Indicates that this is present in both branches, but has different values between them.
   - A “-” symbol with red highlighted text: Indicates that this is not present in the compare branch.

**Usage**

```
csdx cm:branches:diff
```

or

```
csdx cm:branches:diff --stack-api-key <value> --base-branch <value> --compare-branch <value> --module <value>
```

or

```
csdx cm:branches:diff --stack-api-key <value> --base-branch <value> --compare-branch <value> --module <value> --format <value>
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--base-branch` | - | \[Optional\] Base branch (Target branch). |
| `--compare-branch` | - | \[Optional\] Compare branch (Source branch). |
| `--module` | - | \[Optional\] Module.<br>Supported values: `content-types`, `global-fields`, `all` |
| `--stack-api-key` | `-k` | \[Optional\] Provide the stack API key to show the difference between branches. |
| `--format` | - | Type of flags to show the difference.<br>Supported values: `compact-text`, `detailed-text`<br>Default: `compact-text` |
| `--csv-path` | - | \[Optional\] Custom path for the CSV output file.<br>If not provided, the system uses the current working directory. |

**Examples**

- To compare the content types between two branches:

  ```
  csdx cm:branches:diff --stack-api-key bltxxxxxxxx --base-branch main --compare-branch develop --module content-types
  ```

- To compare the global fields between two branches with format:

  ```
  csdx cm:branches:diff --stack-api-key bltxxxxxxxx --base-branch main --compare-branch develop --module global-fields --format detailed-text
  ```

- To compare the global fields between two branches with format, providing a custom path for CSV file:

  ```
  csdx cm:branches:diff --stack-api-key bltxxxxxxxx --base-branch main --compare-branch develop --module global-fields --format detailed-text --csv-path "/path/to/folder"
  ```

  > **Note**: When you use `--format "detailed-text"`, the command also generates a CSV file for easier analysis and reporting of branch differences. You can use the `--csv-path` flag to choose where the file is saved. If you select `--format "compact-text"`, the `--csv-path` flag is ignored.

## Steps to Merge Branches

Follow the steps below to merge two branches:

1. Run the following command to merge two branches:

   ```
   csdx cm:branches:merge
   ```

2. Enter the **Stack API key** of the stack where you want to merge the branches.

3. Enter the **name** of the base branch.

4. Enter the **name** of the compare branch. By default, the current base branch is used.

   Alternatively, you can pass the **Stack API key**, **base branch** (target branch), and **compare branch** (source branch) in the command as given below:

   ```
   csdx cm:branches:merge --stack-api-key <value> --base-branch <value> --compare-branch <value>
   ```

   > **Note**: To choose a base branch other than the default, specify the `--base-branch` flag as given in the command above.

   The branches' compare results will be displayed for individual modules as `Content Types Summary` and `Global Fields Summary`.

5. Choose a merge strategy from the displayed list.
   - **Merge, Prefer Base**: Adds all changes from the compare branch to the base branch. In case of any conflicts, the preference goes to the base branch.
   - **Merge, Prefer Compare**: Adds all changes from the compare branch to the base branch. In case of any conflicts, the preference goes to the compare branch.
   - **Merge, Ask for Preference**: Asks you to choose how you want to merge every difference individually at the content type or global field level.
   - **Overwrite with Compare**: Replaces the base branch with the compare branch. Anything in the base branch that is not in the compare branch is removed.

   The following table contains an example of field changes to a content type between the base branch and compare branch, and explains how the changes are merged based on the merge strategy you choose:

   | **Base Branch** | **Compare Branch** | **Merge, Prefer Base** | **Merge, Prefer Compare** | **Overwrite with Compare** | **Is conflict?** |
   | --- | --- | --- | --- | --- | --- |
   | Title (unchanged) | Title (unchanged) | Title (unchanged) | Title (unchanged) | Title (unchanged) | No |
   | Categories (present) | (not present) | Categories (from Base) | Categories (from Base) |  | No |
   | Feature B (renamed/reconfigured) | Feature C (renamed/reconfigured) | Feature B (from Base) | Feature C (from Compare) | Feature C (from Compare) | Yes |
   | (not present) | SEO Description (present) | SEO Description (from Compare) | SEO Description (from Compare) | SEO Description (from Compare) | No |
   | Topics |  | Topics (from Base) | Topics (from Base) | (removed from Base) | No |

6. If you choose **Merge, Prefer Base** or **Merge, Prefer Compare** from step 4, choose what you want to merge from the following list:
   - **New in Compare Only**: Adds only new items from the compare branch to the base branch. All the items that are modified are ignored.
   - **Modified Only**: Adds only modified items from the compare branch to the base branch. All the items that are new are ignored.
   - **Both**: Adds both new and modified items from the compare branch to the base branch.
   - **Go Back**: Takes you back to the previous step.
   - **Start Over**: Takes you back to step 4.

   The following table contains the content types in the base branch and compare branch, explaining how data is merged based on the merge strategy preference you choose:

   | **Base Branch** | **Compare Branch** | **Merge New in Compare Only** | **Merge Modified Only, Prefer Base** | **Merge, Modified Only, Prefer Compare** |
   | --- | --- | --- | --- | --- |
   | Title | Title | Title | Title | Title |
   | Categories |  | Categories | Categories | Categories |
   | Feature B | Feature C | Feature B | Feature B | Feature C |
   |  | SEO Description |  | SEO Description | SEO Description |
   | Topics |  | Topics | Topics |  |

7. If you choose **Overwrite with Compare** from step 4, or **New in Compare Only**, **Modified Only**, or **Both** from step 5, choose what you want to do next from the following list:
   - **Execute Merge**: Executes the merge action and exports the merge result summary to the specified location.
   - **Export Merge Summary**: Exports the merge result summary to the specified location but does not execute the merge action. This can be used to apply the merge later.
   - **Execute Merge and Generate Content Migration Scripts**: Executes merge action, exports merge result summary to the specified location, and generates the entries migration script.
   - **Export Summary and Generate Content Migration Scripts**: Exports merge result summary to the specified location and generates the entries migration script.
   - **Go Back**: Takes you back to the previous step.
   - **Start Over**: Takes you back to step 4.

8. If you choose **Execute Merge and Generate Content Migration Scripts** or **Export Summary and Generate Content Migration Scripts** from step 6, choose what you want to do next from the following list:
   - **Both existing and new**: Generates script for both new and modified entries.

   - **New only**: Generates script for the new entries.

   - **Existing only**: Generates script for the updated entries.

   - **Ask for preference**: If you choose this option, the following table displays:

     ![CLI_Merge_Migrate_Content_Entries_Ask_for_Preference.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blt7a73723b1253889f/6527a16d87b4db5c967590ee/CLI_Merge_Migrate_Content_Entries_Ask_for_Preference.png)

     Choose what you want to do next from the following list:
     - **Merge New Only**: Generates script for the new entries.
     - **Merge Modified Only**: Generates script for the updated entries.
     - **Merge Both**: Generates script for both new and modified entries.
     - **Ignore**: Ignores entries from a particular content-type.

9. If you choose **Merge, Ask for Preference** from step 4, follow the steps below:
   1. Select the **content type changes** for merge from the provided tabular column. With this, you can choose to modify/add/remove only those content types from a selected branch during the merge operation. ![Branches_CM_Merge_Ask_For_Preference_CT.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/blted2babceee226a5b/644a3f781338252c6f8711e8/Branches_CM_Merge_Ask_For_Preference_CT.png)

      > **Note:** To ignore the changes in the compare branch for a specific content type, select the **Ignore(Use Base)** option for that content type.

      > **Tip**: Use the **arrow keys** to move along the table cells and then hit the **spacebar** to make the selection.

   2. Select the **global field changes** for merge from the provided tabular column. With this, you can choose to modify/add/remove only those global fields from a selected branch during the merge operation. ![Branches_CM_Merge_Ask_For_Preference_GF.png](https://images.contentstack.io/v3/assets/blt2d43f51baca745a8/bltd02e46508c2f7d1d/644a3f77398bc14b3cfff63a/Branches_CM_Merge_Ask_For_Preference_GF.png)

      > **Note:** To ignore the changes in the compare branch for a specific global field, select the **Ignore(Use Base)** option for that global field.

   3. In the next step, choose what you want to merge from the following list:
      - **Execute Merge**: Executes the merge action and exports the merge result summary to the specified location.
      - **Export Merge Summary**: Exports the merge result summary to the specified location but does not execute the merge action.
      - **Execute Merge and Generate Content Migration Scripts**: Executes merge action, exports merge result summary to the specified location, and generates the entries migration script.
      - **Export Summary and Generate Content Migration Scripts**: Exports merge result summary to the specified location and generates the entries migration script.
      - **Go Back**: Takes you back to the previous step.
      - **Start Over**: Takes you back to step 4.

   4. If you choose **Execute Merge and Generate Content Migration Scripts** or **Export Summary and Generate Content Migration Scripts** from the above step, follow the steps in step 7.

With this, the merge operation is completed, and the [Entry Migration](/docs/headless-cms/cli-entry-migration/v1) files generated are placed in the “YYYYMMDDHHMMSS_bltxxx” folder under `merge_scripts` folder in the current working directory.

**Usage**

```
csdx cm:branches:merge
```

or

```
csdx cm:branches:merge --stack-api-key <value> --base-branch <value> --compare-branch <value>
```

**Options**

| Flag | Short Flag | Description |
| --- | --- | --- |
| `--compare-branch` | - | \[Optional\] Compare branch (Source branch). |
| `--base-branch` | - | \[Optional\] Base branch (Target branch). |
| `--comment` | - | \[Optional\] Pass a comment. |
| `--stack-api-key` | `-k` | \[Optional\] Provide stack API key to show the difference between the branches. |
| `--export-summary-path` | - | \[Optional\] Export summary file path. |
| `--use-merge-summary` | - | \[Optional\] Path of merge summary file. |
| `--no-revert` | - | \[Optional\] If passed, will not create the new revert branch. |

**Examples**

- To merge feature-branch with the base branch for a stack:

  ```
  csdx cm:branches:merge --stack-api-key bltxxxxxxxx --compare-branch feature-branch
  ```

- To merge branches and export the results summary to a file path:

  ```
  csdx cm:branches:merge --export-summary-path "/file/path"
  ```
