#!/bin/bash
# Daily git pull for every clone under repos/cli.
set -u
ROOT="/Users/aravindh.s/Desktop/cursor/repos/cli"
echo "[$(date -Iseconds)] git-pull-all-cli start"
failures=0
while IFS= read -r gitdir; do
  repo="$(dirname "$gitdir")"
  branch="$(cd "$repo" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "?")"
  echo "=== $repo (branch: $branch) ==="
  if ! (cd "$repo" && git pull --ff-only); then
    echo "FAILED: $repo" >&2
    failures=$((failures + 1))
  fi
done < <(find "$ROOT" -type d -name .git | sort)

echo "[$(date -Iseconds)] git-pull-all-cli done (failures: $failures)"
exit $(( failures == 0 ? 0 : 1 ))
