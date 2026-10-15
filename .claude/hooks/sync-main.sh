#!/usr/bin/env bash
# Keeps the working copy in step with origin/main, so both officers always start from the
# latest shared version. Runs on every session start ("session"), and on a prompt ("prompt")
# when the previous prompt was more than SYNC_AFTER_HOURS ago. Never blocks: always exits 0.
# Whatever it prints is added to Claude's context.

mode="${1:-session}"
SYNC_AFTER_HOURS="${SYNC_AFTER_HOURS:-3}"

cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0
stamp="$(git rev-parse --git-dir)/claude-last-prompt"

now=$(date +%s)
if [ "$mode" = "prompt" ]; then
  last=$(cat "$stamp" 2>/dev/null || echo 0)
  echo "$now" > "$stamp"
  [ $((now - last)) -lt $((SYNC_AFTER_HOURS * 3600)) ] && exit 0
  why="first message in over ${SYNC_AFTER_HOURS}h"
else
  echo "$now" > "$stamp"
  why="session start"
fi

if ! git fetch -q origin main 2>/dev/null; then
  echo "[sync-main] ($why) Could not fetch origin/main. Working from the local copy; tell the user it may be out of date."
  exit 0
fi

branch=$(git rev-parse --abbrev-ref HEAD)
behind=$(git rev-list --count HEAD..origin/main)
if [ "$behind" = "0" ]; then
  echo "[sync-main] ($why) Up to date with origin/main."
  exit 0
fi

if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  echo "[sync-main] ($why) origin/main has $behind new commit(s), NOT merged: there are uncommitted changes on '$branch'. Tell the user before working, and offer to commit or stash and then merge origin/main."
  exit 0
fi

if [ "$branch" = "main" ]; then
  if git merge -q --ff-only origin/main >/dev/null 2>&1; then
    echo "[sync-main] ($why) Pulled $behind new commit(s) from origin/main."
  else
    echo "[sync-main] ($why) Local main has diverged from origin/main, NOT merged. Tell the user before working."
  fi
elif git merge -q --no-edit origin/main >/dev/null 2>&1; then
  echo "[sync-main] ($why) Merged $behind new commit(s) from origin/main into '$branch'."
else
  git merge --abort >/dev/null 2>&1
  echo "[sync-main] ($why) Merging origin/main into '$branch' conflicts, NOT merged. Tell the user and resolve it before other work."
fi
exit 0
