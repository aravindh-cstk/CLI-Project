# Rate Limit Errors During cm:stacks:clone

The customer encountered rate limit exceeded errors while running cm:stacks:clone, resulting in incomplete clones. They also asked whether the CLI supports cloning only a subset of languages/locales.

**Root cause**

cm:stacks:clone runs an export step against the source stack followed by an import step into the destination stack. Both steps share the same automatic retry behavior for API requests: a rate-limited (429) request is retried up to 3 times, with a randomized delay of 3 to 8 seconds between attempts, and the same retry behavior also covers HTTP 401, 408, and 422 responses.

A single rate-limited request does not fail the clone right away. The "process stops on a rate limit error" symptom happens when the rate limiting is sustained enough that all 3 retries are also rejected. At that point the error propagates up through the export or import step, and the clone has no checkpoint or resume mechanism for the module it was processing, so the whole clone stops. This is different from having no retry behavior at all, since the retries exist but get exhausted under sustained throttling.

Selective cloning of a subset of locales is not supported. The clone command's type flag only chooses between structure-only and structure-with-content, not a subset of locales. The underlying export step's locales module always exports the entire locales module, not specific locale codes.

If retries seem to fail immediately rather than being exhausted gradually over several seconds, check your proxy configuration. Connection errors such as ECONNREFUSED or ETIMEDOUT are not retried when a proxy is in use, so a proxy issue can produce a failure that looks like a rate-limit error with no retry attempted.

**Resolution**

1. A rate limit error during clone means the automatic retries (up to 3 attempts per request, with a 3-8 second delay) were already exhausted, not that the CLI gave up on the first 429. Review the output for the specific module where the export or import step failed.

2. If fewer locales are needed, clone all locales as usual, then manually remove the unwanted locales afterward. The CLI does not support cloning a subset of locales directly.

3. If clones are frequently interrupted by rate limits, space out large clone operations or run them during lower API-traffic periods so the built-in retries have a better chance of succeeding.

4. If retries appear to fail immediately instead of being exhausted gradually, check whether a proxy is configured. Proxy-related connection errors are not retried and can produce a failure that looks identical to an exhausted rate limit.

Manual post-clone cleanup for locales and spacing out large clone operations are the practical workarounds. There is no CLI flag to resume a clone from the point of failure.

*Source ticket: Case 45226*
