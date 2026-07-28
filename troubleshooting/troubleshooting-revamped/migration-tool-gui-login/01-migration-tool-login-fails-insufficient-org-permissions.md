# Migration Tool Login Fails Due to Insufficient Org-Level Permissions

The customer was unable to log in to the Contentstack migration tool and requested help understanding why access was failing.

**Root cause**

The migration tool requires Org-level Admin or Owner permissions. The user had Admin access only at the stack level, with a Member role at the org level, which blocked login. The user was also attempting to log in via the wrong region.

**Resolution**

1. Ask your Org Admin or Owner to update your role to Admin or Owner at the organization level.

2. Confirm you are logging in using the correct region for your organization (for example, AWS NA rather than Azure EU).

3. Retry logging in to the migration tool.

Login succeeds once org-level Admin/Owner permissions are granted and the correct region is used.

*Source ticket: Case 45213*
