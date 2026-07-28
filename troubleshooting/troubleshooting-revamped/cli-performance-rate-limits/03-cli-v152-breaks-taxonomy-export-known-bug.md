# CLI v1.52 Breaks Taxonomy Export with Management Token Alias (Known Bug)

After upgrading to CLI v1.52, a taxonomy export command that previously worked in v1.51 with a management-token alias began failing with "Access denied. Please check your permissions."

**Root cause**

There is no confirmation that this is a version-specific defect introduced in CLI v1.52. The error message, "Access denied. Please check your permissions.", is a generic message the CLI shows whenever the Management API returns an HTTP 403 response. It is not specific to taxonomy export, to management-token authentication, or to any particular CLI version, so seeing it after an upgrade does not by itself point to a regression in that version.

Management-token aliases are a supported authentication method for taxonomy export, for example `csdx cm:export-to-csv --action taxonomies --alias <management-token-alias>`, so using an alias for this command is not itself invalid.

A 403 error on a taxonomy export using a management-token alias is more often caused by one of the following than by a CLI defect:
- The token lacks the required scope or taxonomy read access.
- The organization's plan does not include the taxonomies feature.
- The management token was created before taxonomy permissions existed on its role and needs to be regenerated.
- The alias points to a branch that does not have taxonomy access.

**Resolution**

1. Before downgrading, verify the management token alias still has the necessary permissions. Confirm the token is scoped to the stack in question and that its role includes taxonomy read access. A 403 error is the CLI's standard response to any permission-insufficient API call, not a taxonomy-specific error code.

2. Re-check the alias is correctly configured with `csdx auth:tokens` and that it points at the intended stack and token, in case the alias itself is stale or misconfigured.

3. If the token and permissions check out and the same command worked on a previous CLI version with no other change, downgrading to that previous version (for example `npm install -g @contentstack/cli@1.51.0`, adjusted to whatever version actually worked) remains a reasonable temporary workaround. Treat it as a workaround rather than a confirmed fix.

4. Escalate to Contentstack support with the exact CLI version (`csdx version`), the full error response body, and the management token's role and permissions if the permissions check does not explain the failure.

*Source ticket: Case 51155*
