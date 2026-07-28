# CLI Stack Export Fails with "No Management Token Found on Given Alias"

CLI stack export failed with the error "No management token found on given alias <alias>" even though the customer confirmed the management token existed on the stack.

**Root cause**

The management token existed on the stack but was not registered in the CLI's local token store under that alias, so the CLI could not resolve it during export. This also happens if the alias was registered once and later overwritten by a second `auth:tokens:add` call using the same alias with a different token, or if the alias was registered under a different CLI profile or user account than the one running the export. The token store is local to the machine and user profile, not shared across machines and not read from the stack itself.

**Resolution**

1. Register the management token in the CLI with the correct alias:

csdx auth:tokens:add --management --alias <alias> --stack-api-key <stack_api_key> --token <management_token>

2. Confirm the alias was registered correctly:

csdx auth:tokens

3. Re-run the export command:

csdx cm:stacks:export --stack-api-key <stack-api-key> --data-dir "<path>" --alias <alias>

After registering the management token under the correct alias, csdx cm:stacks:export runs successfully.

*Source ticket: Case 45251*
