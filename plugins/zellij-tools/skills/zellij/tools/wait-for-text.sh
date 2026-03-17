#!/usr/bin/env bash
# wait-for-text.sh - Poll a Zellij session's screen until a text pattern appears.
#
# Usage:
#   wait-for-text.sh -s <session> -p <pattern> [-t <timeout>] [-i <interval>] [-r]
#
# Options:
#   -s  Session name (required)
#   -p  Text pattern to search for (required)
#   -t  Timeout in seconds (default: 30)
#   -i  Poll interval in seconds (default: 0.5)
#   -r  Treat pattern as extended regex (default: fixed string)
#
# Exit codes:
#   0   Pattern found
#   1   Timeout reached (last captured screen printed to stderr)

set -euo pipefail

# Defaults
SESSION=""
PATTERN=""
TIMEOUT=30
INTERVAL=0.5
USE_REGEX=false

usage() {
  echo "Usage: $0 -s <session> -p <pattern> [-t <timeout>] [-i <interval>] [-r]" >&2
  exit 1
}

while getopts "s:p:t:i:r" opt; do
  case "$opt" in
    s) SESSION="$OPTARG" ;;
    p) PATTERN="$OPTARG" ;;
    t) TIMEOUT="$OPTARG" ;;
    i) INTERVAL="$OPTARG" ;;
    r) USE_REGEX=true ;;
    *) usage ;;
  esac
done

if [ -z "$SESSION" ] || [ -z "$PATTERN" ]; then
  echo "Error: -s (session) and -p (pattern) are required." >&2
  usage
fi

# Temp file for screen capture
CAPTURE_FILE="/tmp/zellij-wait-$$-output.txt"

# Clean up temp file on exit
cleanup() {
  rm -f "$CAPTURE_FILE"
}
trap cleanup EXIT

# Build grep flags
if [ "$USE_REGEX" = true ]; then
  GREP_FLAGS="-qE"
else
  GREP_FLAGS="-qF"
fi

# Poll loop
elapsed=0
while true; do
  # Capture the focused pane's screen content
  if zellij -s "$SESSION" action dump-screen "$CAPTURE_FILE" 2>/dev/null; then
    if [ -f "$CAPTURE_FILE" ] && grep $GREP_FLAGS "$PATTERN" "$CAPTURE_FILE"; then
      echo "Pattern found after ${elapsed}s"
      exit 0
    fi
  fi

  # Check timeout
  if awk "BEGIN { exit ($elapsed >= $TIMEOUT) ? 0 : 1 }"; then
    echo "Timeout after ${TIMEOUT}s waiting for pattern: $PATTERN" >&2
    if [ -f "$CAPTURE_FILE" ]; then
      echo "--- Last captured screen ---" >&2
      cat "$CAPTURE_FILE" >&2
    fi
    exit 1
  fi

  sleep "$INTERVAL"
  elapsed=$(awk "BEGIN { print $elapsed + $INTERVAL }")
done
