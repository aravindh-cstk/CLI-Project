# CLI Export Hangs for Large Content Types with Nested References

Exporting a large content type (approximately 85,000 records with multiple references and arrays) using csdx cm:export-to-csv hung indefinitely, while smaller content types exported successfully.

**Root cause**

export-to-csv does not hang in the sense of an infinite loop or deadlock. The command fetches entries for a content type one page at a time (100 entries per request, one request after another, with no concurrency), and it expands each entry's nested objects, references, and arrays into individual flattened columns (for example `field[0].uid`). All flattened rows for the entire content type accumulate in memory, and the CSV file is written only once, after every page has been fetched. For a content type with around 85,000 records and multiple reference and array fields, this means roughly 850 sequential API calls, memory usage that keeps growing until the very end, and no per-page progress output beyond a single static "Fetching entries for `<content type>`..." loader message. That combination makes a long-running but still-progressing export look identical to a hang from the outside. If the stack's API rate limits are being hit during those hundreds of sequential requests, retries or backoff at the network layer can add further delay on top of the sequential design, compounding the perceived hang.

**Resolution**

1. Use csdx cm:stacks:export to export the content in JSON format instead. It also paginates in batches of 100, but it writes each page to disk as soon as it is fetched and reports progress per entry, so large content types export without holding the full dataset in memory and without long silent gaps.

2. Explicitly include all referenced content types using the --content-types flag to ensure completeness.

3. Convert the exported JSON to CSV afterward with a script, if a CSV file is still required.

Exporting large, reference-heavy content types as JSON via cm:stacks:export completes reliably where export-to-csv previously appeared to hang, because it writes data incrementally instead of buffering an entire content type's flattened rows in memory. This case was also escalated to CLI engineering to evaluate improvements for large dataset exports.

*Source ticket: Case 46907*
