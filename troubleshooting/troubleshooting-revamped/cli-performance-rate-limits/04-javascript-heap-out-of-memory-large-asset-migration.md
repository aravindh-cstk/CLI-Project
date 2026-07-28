# JavaScript Heap Out of Memory During Large Asset Migration

Migrating a large batch of assets (roughly 5,354 assets across 554 folders, totaling 5.53GB) from one stack to another consistently crashed at around 80% completion with a "JavaScript heap out of memory" error, even after significantly raising the Node.js memory limit with NODE_OPTIONS=--max-old-space-size=30720.

**Root cause**

Raising the Node.js heap limit to 30 GB and still crashing at around 80% completion points to a memory-handling issue in the CLI's asset import process, not an under-provisioned heap. The CLI's default asset upload settings are already conservative (`assetBatchLimit: 1`, `uploadAssetsConcurrency: 2`, `importFoldersConcurrency: 1`), so the failure is unlikely to be caused by too many simultaneous uploads competing for memory.

Instead, the import process loads the full list of assets and folder mappings for a module into memory before processing it in batches, and keeps mapping data such as the asset-to-UID map in memory for the life of that module's run. For a batch this size (roughly 5,354 assets across 554 folders, 5.53 GB of files), the per-asset metadata, folder mappings, and UID mappings accumulate in memory for the full run, even though the asset file bytes themselves are referenced by file path rather than loaded into memory as a whole.

This explains the general memory-growth pattern for large asset batches. The exact point at which memory use becomes unbounded has not been pinned down and would need further investigation from Contentstack engineering using a real large-batch run.

**Resolution**

1. As a workaround, build a custom upload script against the already-exported asset files instead of relying on the CLI's built-in asset import for this batch size.

2. Deliberately limit request concurrency in the custom script to avoid overwhelming the API and to keep memory usage bounded.

3. Alternatively, before writing a fully custom script, try lowering the CLI's own asset concurrency settings further through an external configuration file (`assetBatchLimit`, `uploadAssetsConcurrency`, `importFoldersConcurrency` passed via `csdx cm:stacks:import --config <file>`) and splitting the import into smaller runs by moving a subset of the exported `assets` folder's contents at a time. This has not been verified against this specific failure, but may avoid a full custom-script rewrite.

A concurrency-limited custom upload script completed the asset migration successfully where the CLI's built-in import could not. This case was shared with Contentstack engineering to investigate the underlying memory behavior for large asset batches, and that investigation remains the authoritative source for a confirmed root cause.

*Source ticket: Case 53631*
