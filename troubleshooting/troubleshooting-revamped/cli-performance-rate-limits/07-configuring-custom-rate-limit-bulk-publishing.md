# Configuring a Custom Rate Limit for Bulk Publishing via CLI

The customer hit CLI publishing limits during large-scale bulk publish operations.

**Root cause**

`csdx config:set:rate-limit` is the documented, correct way to raise bulk publish throughput for the CLI's core bulk publish and unpublish commands (`cm:entries:publish`, `cm:assets:publish`, and related commands). By default the CLI limits these commands to 1 request per second. That default is deliberately conservative, and you must configure a higher rate limit for your organization before bulk publishing runs at anything faster.

The command accepts `--org`, `--utilize` (a percentage of your organization's actual plan limit), and `--limit-name` (`getLimit`, `limit`, or `bulkLimit`). Setting `--limit-name bulkLimit` with a higher `--utilize` percentage raises the throughput these bulk publish commands use, since they read this stored value on each run.

If bulk publishing is slow, the more likely explanation is that the rate limit was never configured for the organization, or was configured with a low utilization percentage, not that the command has no effect.

Note that this configuration applies to the CLI's core bulk publish commands listed above. If you bulk publish using the separate CLI Bulk Operations plugin (`cm:stacks:bulk-entries` / `cm:stacks:bulk-assets`), that plugin controls its own throughput independently through `rateLimit.requestsPerSecond` and `rateLimit.maxConcurrent` in its `--config` file, and it does not read the value set by `config:set:rate-limit`.

**Resolution**

1. Set a custom bulk publish rate limit for your organization: `csdx config:set:rate-limit --org <your_org_uid> --utilize <percentage> --limit-name bulkLimit`. Start with a moderate percentage and raise it gradually, watching for rate-limit errors, since the utilization is applied against your organization's actual plan limit.

2. Confirm the change with `csdx config:get:rate-limit`. Reset to the default rate limit with `--default`, or remove the custom configuration entirely with `csdx config:remove:rate-limit --org <your_org_uid>`.

3. If you bulk publish through the CLI Bulk Operations plugin (`cm:stacks:bulk-entries` / `cm:stacks:bulk-assets`) instead, configure throughput through that command's own `--config` file using `rateLimit.requestsPerSecond` and `rateLimit.maxConcurrent`, since `config:set:rate-limit` does not apply to that plugin.

4. If publishing is still rate-limited after raising the configured limit, the constraint is likely your organization's actual API plan. Request a plan-level rate limit increase from Contentstack, since no local CLI configuration can exceed your organization's real backend limit.

*Source ticket: Case 57566*
