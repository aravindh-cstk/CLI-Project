#!/bin/bash
# Hourly sync of contentstack/product-wiki's developer-experience/cli into repo/wikis/cli.
set -u
SRC="/Users/aravindh.s/CLI Project/repo/wikis/.source/product-wiki"
DEST="/Users/aravindh.s/CLI Project/repo/wikis/cli"
LOG="/Users/aravindh.s/CLI Project/repo/wikis/.sync.log"
WATCH_PATH="developer-experience/cli"

log() { echo "[$(date -Iseconds)] $*" >> "$LOG"; }

log "sync start"
cd "$SRC" || { log "FAILED: clone missing at $SRC"; exit 1; }

OLD_SHA=$(git rev-parse HEAD)
if ! git pull --ff-only origin main >> "$LOG" 2>&1; then
  log "FAILED: git pull"
  exit 1
fi
NEW_SHA=$(git rev-parse HEAD)

if [ "$OLD_SHA" = "$NEW_SHA" ]; then
  log "no new commits"
  exit 0
fi

CHANGED=$(git diff --name-only "$OLD_SHA" "$NEW_SHA" -- "$WATCH_PATH")
if [ -z "$CHANGED" ]; then
  log "new commits ($OLD_SHA -> $NEW_SHA) but none touched $WATCH_PATH"
  exit 0
fi

log "changes detected under $WATCH_PATH:"
echo "$CHANGED" | sed 's/^/  /' >> "$LOG"

rsync -a --delete "$SRC/$WATCH_PATH/" "$DEST/"
log "synced to $DEST"
