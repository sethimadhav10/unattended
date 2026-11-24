#!/usr/bin/env bash
# Manual install (no plugin system): copies the five skills into ~/.claude/skills.
# Never overwrites a skill of the same name that isn't ours. Undo with ./uninstall.sh.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
C="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
mkdir -p "$C/skills"
for s in autonomous ship-safe deploy-audit dreamer summary; do
  if [ -e "$C/skills/$s" ] && [ ! -f "$C/skills/$s/.unattended" ]; then
    echo "skip $s: $C/skills/$s already exists and isn't ours"; continue
  fi
  mkdir -p "$C/skills/$s"; cp -R "$SRC/skills/$s/." "$C/skills/$s/"; touch "$C/skills/$s/.unattended"
  echo "✔ $s"
done
echo "Installed. Open a new Claude Code session and type /autonomous, /ship-safe, /deploy-audit, /dreamer or /summary."
