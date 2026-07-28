# Branch Merge Fails with Error Code 116 (Global Fields: Failed to Fetch Global Fields)

While attempting to merge branches, the customer received Error Code 116, "Global Fields: Failed to fetch global fields," and the merge process failed.

**Root cause**

`csdx cm:branches:merge` does not implement the merge logic itself. It builds a merge request and sends it through a single API call. Any error, including "Error Code 116, Global Fields: Failed to fetch global fields," comes back from that API call, and the CLI prints it as-is before exiting. The only client-side handling for merge errors is a retry when the API responds with HTTP 429 (rate limiting). The CLI does not inspect error code 116 specifically, and it does not evaluate field visibility rules on its own.

This means the specific mechanism described (an outdated field visibility rule that migrated inconsistently from staging to main) is a stack or backend condition, not CLI behavior. The resolution steps below are a reasonable workaround, confirmed by the customer, though the CLI itself doesn't reveal why they work. Any transient failure in fetching global fields during a merge can surface through this same error code, so error 116 isn't necessarily specific to field visibility rules. Other global field inconsistencies between branches can produce the same message.

**Resolution**

1. Review field visibility rules for global fields across the branches involved in the merge (this is a stack/content-type configuration step done in the UI or via the Content Management API, not a CLI operation).

2. Identify and manually remove the outdated field visibility rule in the main branch.

3. Re-run `csdx cm:branches:merge`, which resends the merge request. The CLI does not retry or fix this error automatically.

After removing the outdated field visibility rule, the branch merge completed successfully.

*Source ticket: Case 47200*
