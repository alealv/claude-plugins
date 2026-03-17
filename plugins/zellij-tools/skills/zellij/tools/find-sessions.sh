#!/usr/bin/env bash
# find-sessions.sh - List and filter Zellij sessions.
#
# Usage:
#   find-sessions.sh [-q <query>]
#
# Options:
#   -q  Filter sessions by name substring (case-insensitive)
#
# Displays session name and status from `zellij list-sessions`.
# Exit codes:
#   0   Sessions found (or no filter specified)
#   1   No matching sessions found

set -euo pipefail

QUERY=""

while getopts "q:" opt; do
  case "$opt" in
    q) QUERY="$OPTARG" ;;
    *) echo "Usage: $0 [-q <query>]" >&2; exit 1 ;;
  esac
done

# Get session list from zellij
SESSION_OUTPUT=$(zellij list-sessions 2>/dev/null) || {
  echo "No Zellij sessions found or zellij is not available." >&2
  exit 1
}

if [ -z "$SESSION_OUTPUT" ]; then
  echo "No Zellij sessions found." >&2
  exit 1
fi

# Filter by query if provided
if [ -n "$QUERY" ]; then
  FILTERED=$(echo "$SESSION_OUTPUT" | grep -i "$QUERY" || true)
  if [ -z "$FILTERED" ]; then
    echo "No sessions matching '$QUERY'." >&2
    exit 1
  fi
  echo "$FILTERED"
else
  echo "$SESSION_OUTPUT"
fi
