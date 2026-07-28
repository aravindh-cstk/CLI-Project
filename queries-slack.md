Hey team, I have couple of question while I'm documenting the new asset scanning gating for CLI import (both `cli-plugins-pr217` / V1 GA and `cli-plugins-pr294` / V2 beta).  
  
**Question 1:**

I'm looking at the "auto-detect `assetsScan` from the org plan and auto-set `skipAssetsPublish` during import" logic in `import-config-handler.ts` (and the matching `export-config-handler.ts`), and it looks like the plan-check block never actually runs in either branch as currently checked out:

- It only executes if `context.planCheckRequired` is a non-empty array, but I can't find anywhere in either repo that ever sets `context.planCheckRequired`. It always looks empty, so the block is skipped.
- Separately, it calls `isFeatureEnabled` / `FeatureCtx` from `@contentstack/cli-utilities`, but neither of those exist in the installed `@contentstack/cli-utilities@1.18.5` in either worktree's `node_modules`.

So as far as I can tell, the "automatically skip publishing assets on import when the org plan has asset scanning" behavior isn't wired up yet.

Before I write this up as working behavior in the docs, I want to confirm which of these is true:

1. This is genuinely still in progress (waiting on a `cli-utilities` update that hasn't shipped), and the docs should hold off on describing auto-detection until it lands.
2. `context` gets populated somewhere I'm not seeing (a hook, a different package, a build step not in these worktrees), and it does work end to end.
3. There's a different code path that actually does this job, and this block is dead/leftover code.

---

**Question 2:**

Does asset scanning apply to CS Assets (space-based) stacks at all? The scan-status check (`include_asset_scan_status` / `_asset_scan_status`) is only called against the standard `stack.asset()` API in both branches, I don't see an equivalent check anywhere in the CS Assets export/import flow. So for orgs that have CS Assets enabled, does scanning cover their assets too, or does it currently only apply to stacks on standard assets? Trying to figure out if `cli-for-cs-assets.md` needs a callout about this either way.