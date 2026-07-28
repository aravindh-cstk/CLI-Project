# GUI Migration Tool Login Blocked by SSO Strict Mode

The customer could not log in to the GUI migration tool because it requires a standard Contentstack username and password, but their organization uses SSO without a Contentstack password.

**Root cause**

Organizations with SSO Strict Mode enabled prevent password-based logins entirely, which blocks access to the migration tool since it does not yet support SSO authentication.

**Resolution**

1. Preferred: create a separate non-SSO user account with a standard password dedicated to migration tasks. This option is preferred because it affects only the one account and does not change SSO enforcement for other users in your organization.

2. Alternative, only if a separate account is not workable: temporarily disable SSO Strict Mode so the user can set a standard Contentstack password, then log in to the migration tool. This removes password-login enforcement for the entire organization, not just the one user, so treat it as a temporary exception and re-enable Strict Mode as soon as the migration work is complete.

3. Re-enable Strict Mode immediately after the migration work is complete if you disabled it.

The user is able to log in to the migration tool using either workaround. Native SSO support for the migration tool is on the product roadmap but not yet available.

*Source ticket: Case 43946*
