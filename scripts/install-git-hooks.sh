#!/usr/bin/env bash
# Install repo git hooks (pre-commit validation).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"

if [ ! -d "$HOOKS_DIR" ]; then
  echo "Error: $HOOKS_DIR not found. Run from a git clone." >&2
  exit 1
fi

cp "$REPO_ROOT/scripts/pre-commit" "$HOOKS_DIR/pre-commit"
chmod +x "$HOOKS_DIR/pre-commit"
echo "Installed pre-commit hook → .git/hooks/pre-commit"
echo "Runs: skillctl validate --all, backlog validate, dist/ staging reminder"
