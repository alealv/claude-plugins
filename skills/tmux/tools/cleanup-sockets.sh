#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: cleanup-sockets.sh [options]

Scan for and clean up dead tmux socket files.

Options:
  -d, --dir       Socket directory (default: CLAUDE_TMUX_SOCKET_DIR or ${TMPDIR:-/tmp}/claude-tmux-sockets)
  -f, --force     Auto-remove dead sockets without prompting
  -n, --dry-run   Show what would be removed without deleting
  -h, --help      Show this help
USAGE
}

socket_dir="${CLAUDE_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/claude-tmux-sockets}"
force=false
dry_run=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -d|--dir)       socket_dir="${2-}"; shift 2 ;;
    -f|--force)     force=true; shift ;;
    -n|--dry-run)   dry_run=true; shift ;;
    -h|--help)      usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux not found in PATH" >&2
  exit 1
fi

if [[ ! -d "$socket_dir" ]]; then
  echo "Socket directory does not exist: $socket_dir"
  exit 0
fi

# Find all socket files
shopt -s nullglob
sockets=("$socket_dir"/*)
shopt -u nullglob

if [[ "${#sockets[@]}" -eq 0 ]]; then
  echo "No sockets found in $socket_dir"
  exit 0
fi

dead_sockets=()
live_sockets=()

echo "Scanning sockets in $socket_dir..."
echo

for sock in "${sockets[@]}"; do
  if [[ ! -S "$sock" ]]; then
    continue
  fi

  # Try to list sessions on this socket
  if tmux -S "$sock" list-sessions >/dev/null 2>&1; then
    session_count=$(tmux -S "$sock" list-sessions 2>/dev/null | wc -l)
    live_sockets+=("$sock")
    echo "✓ $sock (${session_count} session(s))"
  else
    dead_sockets+=("$sock")
    echo "✗ $sock (no server responding)"
  fi
done

echo
echo "Summary:"
echo "  Live sockets: ${#live_sockets[@]}"
echo "  Dead sockets: ${#dead_sockets[@]}"

if [[ "${#dead_sockets[@]}" -eq 0 ]]; then
  echo
  echo "No dead sockets to clean up."
  exit 0
fi

echo
echo "Dead sockets to remove:"
for sock in "${dead_sockets[@]}"; do
  echo "  - $sock"
done

if [[ "$dry_run" == true ]]; then
  echo
  echo "[DRY RUN] Would remove ${#dead_sockets[@]} dead socket(s)"
  exit 0
fi

if [[ "$force" == false ]]; then
  echo
  read -r -p "Remove ${#dead_sockets[@]} dead socket(s)? [y/N] " response
  if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
  fi
fi

echo
echo "Removing dead sockets..."
for sock in "${dead_sockets[@]}"; do
  if rm -f "$sock"; then
    echo "  ✓ Removed: $sock"
  else
    echo "  ✗ Failed to remove: $sock" >&2
  fi
done

echo
echo "Cleanup complete. Removed ${#dead_sockets[@]} dead socket(s)."
