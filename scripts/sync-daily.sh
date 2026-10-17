#!/bin/sh
# Summary: Daily espanso config sync — regenerate skills mirror, commit local changes, pull origin/master, push to origin.
# ~~~
# - Regenerates match/skills.yml from ~/.config/opencode/skills (md -> yml mirror)
# - Commits any local changes on the current branch (dev) with a dated auto-sync message
# - Fetches and merges origin/master (the remote default branch)
# - On merge conflict: aborts the merge, logs the conflict, and skips the push
# - Pushes the result to origin master
# - Appends a timestamped line to .sync.log for every run
# ~~~
# returns: exit 0 on success or nothing-to-do; exit 1 on conflict or push failure
set -u

REPO="$HOME/Library/Application Support/espanso"
LOG="$REPO/.sync.log"

log() {
  printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" >>"$LOG"
}

cd "$REPO" || { log "ERROR: repo not found at $REPO"; exit 1; }

# Regenerate the skills mirror so :<skill-name> triggers stay current
if python3 "$REPO/match/packages/skills/skills_lib.py" sync >/dev/null 2>&1; then
  log "Regenerated match/skills.yml"
else
  log "WARN: skills regen failed"
fi

git add -A
if ! git diff --cached --quiet; then
  git commit -m "Auto-sync: local config changes ($(date +%F))" >/dev/null 2>&1 \
    && log "Committed local changes" \
    || log "ERROR: commit failed"
fi

git fetch origin >/dev/null 2>&1 || { log "ERROR: fetch failed"; exit 1; }

if ! git merge origin/master -m "Auto-sync: merge origin/master ($(date +%F))" >/dev/null 2>&1; then
  git merge --abort >/dev/null 2>&1
  log "WARN: merge conflict with origin/master — merge aborted, push skipped"
  exit 1
fi

if git push origin HEAD:master >/dev/null 2>&1; then
  log "OK: pushed to origin/master ($(git rev-parse --short HEAD))"
else
  log "ERROR: push failed"
  exit 1
fi
