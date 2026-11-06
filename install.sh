#!/usr/bin/env bash
# Install the Claude Code status line into ~/.claude (Linux / macOS).
# On Windows use install.ps1 instead.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
dest="$HOME/.claude"

py=""
for cand in python3 python; do
  if p="$(command -v "$cand")" && "$p" -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>/dev/null; then
    py="$p"
    break
  fi
done
if [ -z "$py" ]; then
  echo "Python 3.8+ not found (Arch: sudo pacman -S python)" >&2
  exit 1
fi

mkdir -p "$dest"
cp "$here/statusline.py" "$dest/statusline.py"

cmd="$py $dest/statusline.py"
case "$cmd" in *" "*" "*) echo "warning: path contains spaces, check the command in $dest/settings.json" >&2 ;; esac

"$py" "$here/merge_settings.py" "$dest/settings.json" "$cmd"
echo "done — the status line appears on the next Claude Code refresh"
