#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$ROOT_DIR/skills"
TARGET_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
FORCE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET_DIR="$2"
      shift 2
      ;;
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      cat <<'EOF'
Usage:
  ./install.sh [--target /path/to/skills] [--force]

Options:
  --target   Install into a custom skills directory
  --force    Overwrite existing skill folders with the same name
EOF
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

mkdir -p "$TARGET_DIR"

for skill_dir in "$SOURCE_DIR"/*; do
  [[ -d "$skill_dir" ]] || continue

  skill_name="$(basename "$skill_dir")"
  target_path="$TARGET_DIR/$skill_name"

  if [[ -e "$target_path" ]]; then
    if [[ "$FORCE" -eq 1 ]]; then
      rm -rf "$target_path"
    else
      echo "Target already exists: $target_path" >&2
      echo "Re-run with --force to overwrite." >&2
      exit 1
    fi
  fi

  cp -R "$skill_dir" "$target_path"
  echo "Installed: $skill_name -> $target_path"
done

echo "Done."
