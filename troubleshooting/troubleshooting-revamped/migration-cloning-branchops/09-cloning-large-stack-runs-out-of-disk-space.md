# Cloning a Large Stack Runs Out of Disk Space

The customer needed to clone a large stack (entries and assets), but the CLI cloning process consumed all available disk space and could not complete.

**Root cause**

`csdx cm:stacks:clone` runs as an export followed by an import, both executing locally using the same process that powers `cm:stacks:export` and `cm:stacks:import`. The export step writes the source stack's content types, entries, and assets to a local directory, and only after that completes does the import step read that same directory and upload the content to the target stack. The directory is deleted automatically once the import finishes. For a large stack, this means the full set of entries and asset files must exist on local disk at once, which is what exhausts available disk space on large clones.

The claim that cloning through the Content Delivery API or Content Management API directly is unsupported is imprecise. Clone already uses the Content Management API under the hood for both its export and import steps. What is actually missing is a streaming or in-memory clone path that avoids writing the exported content to local disk before importing it.

**Resolution**

1. Confirm available local disk space before starting a large clone, and free up space or run the clone from a machine/volume with sufficient headroom for the full exported content (entries and assets), since that is what gets written to disk during the export step.

2. If entries and assets are not needed, run `csdx cm:stacks:clone --type a` to clone structure only (all modules except entries and assets). This avoids downloading the large asset files entirely and is a supported flag, not a manual workaround.

3. If both structure and content are needed but disk space is limited, clone content types and global fields with `--type a` first, then use `cm:stacks:export`/`cm:stacks:import` with `--content-types` or `--branch` filters to move entries and assets in smaller batches instead of all at once.

4. If none of the above is workable, replicate stack components manually as a last resort.

`cm:stacks:clone --type a` (structure only) is the most direct way to avoid the disk space ceiling. Filtering entries/assets through export/import in smaller batches is the fallback for a full content clone. Manual replication remains the last resort.

*Source ticket: Case 54041*
