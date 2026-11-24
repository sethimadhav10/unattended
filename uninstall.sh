#!/usr/bin/env bash
# Removes only the skills that install.sh put there (marked with .unattended).
set -euo pipefail
C="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
for s in autonomous ship-safe deploy-audit dreamer summary; do
  if [ -f "$C/skills/$s/.unattended" ]; then rm -rf "$C/skills/$s"; echo "removed $s"; fi
done
