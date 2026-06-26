#!/usr/bin/env bash
# Install generated skills from a local agent-skills clone into a project or user Cursor config.
#
# Usage:
#   ./scripts/install-from-clone.sh --dest /path/to/project --pack java-backend-pack
#   ./scripts/install-from-clone.sh --dest /path/to/project --target codex
#   ./scripts/install-from-clone.sh --dest /path/to/project --target claude
#   ./scripts/install-from-clone.sh --dest /path/to/project --target opencode
#   ./scripts/install-from-clone.sh --user --pack frontend-react-pack
#   AGENT_SKILLS_ROOT=/other/clone ./scripts/install-from-clone.sh --dest . --pack java-backend-pack
#
# Requires: Python 3.11+, dist/ present (or pass --build)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="${AGENT_SKILLS_ROOT:-$REPO_ROOT}"

DEST=""
PACK=""
TARGET="cursor"
MODES=()
USER_WIDE=false
RUN_BUILD=false

usage() {
  cat <<'EOF'
Install skills from a local agent-skills clone.

Required (one of):
  --dest PATH       Target project root
  --user            Install Cursor skills to ~/.cursor (same as --dest $HOME)

Options:
  --pack ID         Pack to install (omit to install all active skills)
  --target TARGET   cursor (default), copilot, codex, claude, or opencode
  --modes MODE ...  Filter by modes: planning, coding (pack install only)
  --build           Run make build if dist/ is missing
  -h, --help        Show this help

Examples:
  git clone git@github.com:josalero/agent-skills.git && cd agent-skills
  ./scripts/install-from-clone.sh --dest ../my-app --pack java-backend-pack
  ./scripts/install-from-clone.sh --dest ../my-app --target codex
  ./scripts/install-from-clone.sh --dest ../my-app --target claude
  ./scripts/install-from-clone.sh --dest ../my-app --target opencode
  ./scripts/install-from-clone.sh --user

List packs: ./tools/skillctl list --packs
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dest)
      DEST="$2"
      shift 2
      ;;
    --pack)
      PACK="$2"
      shift 2
      ;;
    --target)
      TARGET="$2"
      shift 2
      ;;
    --modes)
      shift
      while [[ $# -gt 0 && "$1" != --* ]]; do
        MODES+=("$1")
        shift
      done
      ;;
    --user)
      USER_WIDE=true
      shift
      ;;
    --build)
      RUN_BUILD=true
      shift
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ "$USER_WIDE" == true ]]; then
  DEST="${HOME}"
fi

if [[ -z "$DEST" ]]; then
  echo "Error: pass --dest PATH or --user" >&2
  usage >&2
  exit 1
fi

if [[ "$TARGET" != "cursor" && "$TARGET" != "copilot" && "$TARGET" != "codex" && "$TARGET" != "claude" && "$TARGET" != "opencode" ]]; then
  echo "Error: --target must be cursor, copilot, codex, claude, or opencode" >&2
  exit 1
fi

DEST="$(cd "$DEST" && pwd)"

ensure_dist() {
  local marker=""
  case "$TARGET" in
    cursor) marker="$REPO_ROOT/dist/cursor/.cursor/skills" ;;
    copilot) marker="$REPO_ROOT/dist/copilot/.github/skills" ;;
    codex) marker="$REPO_ROOT/dist/codex/skills" ;;
    claude) marker="$REPO_ROOT/dist/claude/.claude/skills" ;;
    opencode) marker="$REPO_ROOT/dist/opencode/.opencode/skills" ;;
  esac

  if [[ ! -d "$marker" ]]; then
    if [[ "$RUN_BUILD" == true ]]; then
      echo "Building dist/ in $REPO_ROOT ..."
      (cd "$REPO_ROOT" && make build)
    else
      echo "Error: generated output not found under $REPO_ROOT/dist/." >&2
      echo "Run 'make build' in the clone or pass --build." >&2
      exit 1
    fi
  fi
}

SKILLCTL="$REPO_ROOT/tools/skillctl"
export PYTHONPATH="$REPO_ROOT/tools${PYTHONPATH:+:$PYTHONPATH}"

ensure_dist

if [[ -n "$PACK" ]]; then
  args=(--root "$REPO_ROOT" install --pack "$PACK" --target "$TARGET" --dest "$DEST")
  if [[ ${#MODES[@]} -gt 0 ]]; then
    args+=(--modes "${MODES[@]}")
  fi
  "$SKILLCTL" "${args[@]}"
else
  case "$TARGET" in
    cursor)
      mkdir -p "$DEST/.cursor"
      cp -R "$REPO_ROOT/dist/cursor/.cursor/." "$DEST/.cursor/"
      ;;
    copilot)
      mkdir -p "$DEST/.github"
      cp -R "$REPO_ROOT/dist/copilot/.github/." "$DEST/.github/"
      ;;
    codex)
      cp -R "$REPO_ROOT/dist/codex/skills" "$DEST/skills"
      cp "$REPO_ROOT/dist/codex/AGENTS.md" "$DEST/AGENTS.md"
      ;;
    claude)
      mkdir -p "$DEST/.claude"
      cp -R "$REPO_ROOT/dist/claude/.claude/." "$DEST/.claude/"
      if [[ -f "$REPO_ROOT/dist/claude/CLAUDE.md" ]]; then
        cp "$REPO_ROOT/dist/claude/CLAUDE.md" "$DEST/CLAUDE.md"
      fi
      ;;
    opencode)
      mkdir -p "$DEST/.opencode"
      cp -R "$REPO_ROOT/dist/opencode/.opencode/." "$DEST/.opencode/"
      ;;
  esac
  echo "Installed all active skills ($TARGET) to $DEST"
fi
