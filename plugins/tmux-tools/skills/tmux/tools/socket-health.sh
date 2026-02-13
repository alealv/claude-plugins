#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: socket-health.sh [options] <socket-path>

Check health and status of a tmux socket, with optional recovery.

Arguments:
  socket-path     Path to tmux socket file (required)

Options:
  -r, --recover   Attempt recovery if socket is unresponsive (sends USR1 to tmux)
  -v, --verbose   Show detailed information
  -h, --help      Show this help

Examples:
  socket-health.sh /tmp/claude-tmux-sockets/claude.sock
  socket-health.sh -r -v /tmp/claude-tmux-sockets/claude.sock
USAGE
}

socket_path=""
recover=false
verbose=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -r|--recover)   recover=true; shift ;;
    -v|--verbose)   verbose=true; shift ;;
    -h|--help)      usage; exit 0 ;;
    -*)             echo "Unknown option: $1" >&2; usage; exit 1 ;;
    *)              socket_path="$1"; shift ;;
  esac
done

if [[ -z "$socket_path" ]]; then
  echo "Error: socket-path is required" >&2
  usage
  exit 1
fi

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux not found in PATH" >&2
  exit 1
fi

# Check if socket file exists
if [[ ! -e "$socket_path" ]]; then
  echo "Status: MISSING"
  echo "Socket file does not exist: $socket_path"
  exit 1
fi

# Check if it's actually a socket
if [[ ! -S "$socket_path" ]]; then
  echo "Status: INVALID"
  echo "File exists but is not a socket: $socket_path"
  exit 1
fi

# Get socket file info
if [[ "$verbose" == true ]]; then
  echo "Socket path: $socket_path"
  ls -lh "$socket_path"
  echo
fi

# Try to connect and get sessions
if sessions=$(tmux -S "$socket_path" list-sessions 2>/dev/null); then
  session_count=$(echo "$sessions" | wc -l)
  echo "Status: HEALTHY"
  echo "Sessions: $session_count"

  if [[ "$verbose" == true ]]; then
    echo
    echo "Session details:"
    echo "$sessions" | while IFS= read -r line; do
      echo "  $line"
    done

    echo
    echo "Socket path from tmux:"
    tmux -S "$socket_path" display -p '#{socket_path}'
  fi

  exit 0
fi

# Socket exists but server isn't responding
echo "Status: UNRESPONSIVE"
echo "Socket file exists but tmux server is not responding"

if [[ "$recover" == false ]]; then
  echo
  echo "To attempt recovery, run with --recover flag"
  echo "Or manually: pkill -USR1 tmux"
  exit 1
fi

# Attempt recovery
echo
echo "Attempting recovery..."

# Find tmux processes
if ! pgrep tmux >/dev/null 2>&1; then
  echo "  No tmux processes found running"
  echo "  Socket is orphaned - remove it with: rm '$socket_path'"
  exit 1
fi

# Send USR1 signal to recreate sockets
echo "  Sending USR1 signal to tmux processes..."
if pkill -USR1 tmux; then
  echo "  Signal sent successfully"

  # Wait a moment for socket to be recreated
  sleep 0.5

  # Check again
  if tmux -S "$socket_path" list-sessions >/dev/null 2>&1; then
    echo
    echo "Status: RECOVERED"
    session_count=$(tmux -S "$socket_path" list-sessions 2>/dev/null | wc -l)
    echo "Socket is now responsive (${session_count} session(s))"
    exit 0
  else
    echo
    echo "Status: RECOVERY FAILED"
    echo "Socket is still unresponsive after recovery attempt"
    echo "Consider removing the socket: rm '$socket_path'"
    exit 1
  fi
else
  echo "  Failed to send signal"
  exit 1
fi
