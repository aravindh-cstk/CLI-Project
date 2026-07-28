# Rate Limit Exceeded During Query-Based Migration Import: Reduce Import Concurrency

During a query-based content migration between stacks, the customer hit "Rate Limit Exceeded" errors while importing entries into the destination stack. This resulted in incomplete reference mapping. Only 3 of an expected 13 references were linked.

**Root cause**

The retry behavior here is not import-specific. Any command that talks to the Management API retries a request up to 3 times on HTTP 401, 429, 408, and 422 responses, with a randomized delay of 3 to 8 seconds between attempts. `cm:stacks:import` gets these retries automatically like every other command.

The default import concurrency is 5. This applies to `importConcurrency`, `fetchConcurrency`, and `writeConcurrency`, and it is what governs entry and reference-mapping writes during a query-based import. So 5 concurrent write operations is an accurate default for the step responsible for reference mapping.

Concurrency is only configurable through an external configuration file today. The import command has no `--concurrency` (or similarly named) flag, only `--config <path>` for a JSON file merged into the import configuration, so setting `importConcurrency` (and `fetchConcurrency`/`writeConcurrency` if other steps are also being throttled) requires that external file.

**Resolution**

1. Reduce the import concurrency below the default value of 5 using an external configuration file, for example a JSON file containing `{ "importConcurrency": 2 }` passed as `csdx cm:stacks:import --config <path/to/config.json> ...`. Lower `fetchConcurrency`/`writeConcurrency` as well if other modules (not just entries) are also hitting rate limits.

2. If rate-limit errors are affecting modules other than entries, lower `fetchConcurrency` or `writeConcurrency` specifically. These two keys govern most other modules' batching independently of the entries module.

3. If rate limits are still a constraint after reducing concurrency, request an increase to the organization's write limit.

Lowering import concurrency keeps requests within the organization's rate limit, allowing the built-in retry mechanism to succeed and references to map completely.

*Source ticket: Case 58171*
