# Branch Merge Consumes Excessive Memory and Time: Use the --no-revert Flag

Merging branches on a large stack with significant data differences consumed roughly 12GB of memory and took a long time to complete.

**Root cause**

The --no-revert flag is real. It controls whether a revert (backup) branch is created as part of the merge.

Two parts of the original explanation for why this drives up memory do not hold up, though:

- Backup-branch creation itself is not something the CLI does locally. The CLI only signals whether a revert branch should be created, and the work of creating that branch happens on the Contentstack server, not inside the CLI process. So it is unlikely to be the direct cause of high memory usage measured on the machine running the CLI.
- The CLI's status polling after a merge starts is not "every 5 seconds" and does not accumulate data. It starts with a 5-second delay and increases by 1 second per attempt up to a 60-second cap, making a lightweight status-check request each time. This is very unlikely to be a meaningful contributor to memory usage.

The more plausible client-side memory driver is this: before a merge executes, the CLI computes and holds the full difference between the base and compare branches in memory, and this happens regardless of whether --no-revert is passed. For a large stack with substantial differences, this diff computation, not the backup-branch behavior, is the step most directly tied to memory scaling with the size of the difference between branches.

**Resolution**

1. Add the --no-revert flag to the merge command to skip automatic backup-branch creation on the server:

csdx cm:branches:merge ... --no-revert

This remains a valid flag and skipping backup-branch creation can reduce overall merge time (and server-side load), but it does not reduce how much branch-diff data the CLI itself loads into memory before the merge runs, since that step happens either way.

2. If memory usage is the primary concern rather than time, be aware there is currently no flag to limit or paginate the branch-diff computation. Reducing the size of a single merge (merging more frequently, in smaller increments, so each diff is smaller) is the more directly-supported way to lower memory usage for this specific step.

Using --no-revert skips server-side backup-branch creation and can reduce overall merge time. Skipping the revert branch also means there is no automatic backup to roll back to, so consider your own backup strategy before merging without it.

*Source ticket: Case 56439*
