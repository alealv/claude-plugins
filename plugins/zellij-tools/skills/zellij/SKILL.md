---
name: zellij
description: Control Zellij terminal multiplexer sessions for interactive CLIs, long-running processes, and parallel workflows
---

# Zellij Tools

Remote control Zellij terminal sessions from Claude Code. Use this skill whenever
you need to interact with programs that require a terminal (REPLs, TUIs, long-running
servers, parallel tasks, debugging sessions).

## When to Use Zellij

- **Interactive REPLs** (python, node, psql, redis-cli) that need ongoing input
- **Long-running processes** (dev servers, build watchers) you want to monitor
- **Parallel workflows** where multiple commands run simultaneously
- **Debugging sessions** that require back-and-forth interaction
- **TUI applications** that need terminal control sequences

## Detecting Zellij

Check if already inside a Zellij session before creating one:

```bash
if [ -n "$ZELLIJ" ]; then
  echo "Already inside Zellij"
fi
```

## Quick Reference

| Action                        | Command                                                  |
|-------------------------------|----------------------------------------------------------|
| New named session             | `zellij -s <name>`                                       |
| New session (detached)        | `zellij -s <name> --new-session-with-layout <layout>`    |
| List sessions                 | `zellij list-sessions`                                   |
| Attach to session             | `zellij attach <name>`                                   |
| Kill session                  | `zellij kill-session <name>`                              |
| Kill all sessions             | `zellij kill-all-sessions`                                |
| New pane (tiled)              | `zellij action new-pane`                                  |
| New pane (floating)           | `zellij action new-pane --floating`                       |
| New pane (direction)          | `zellij action new-pane --direction <down\|right\|up\|left>` |
| Close focused pane            | `zellij action close-pane`                                |
| Focus direction               | `zellij action move-focus <left\|right\|up\|down>`        |
| New tab                       | `zellij action new-tab --name <name>`                     |
| Switch tab                    | `zellij action go-to-tab-name <name>`                     |
| Send text                     | `zellij action write-chars "text here"`                   |
| Send Enter                    | `zellij action write 13`                                  |
| Send Ctrl+C                   | `zellij action write 3`                                   |
| Send Ctrl+D                   | `zellij action write 4`                                   |
| Send Tab key                  | `zellij action write 9`                                   |
| Send Escape                   | `zellij action write 27`                                  |
| Dump screen to file           | `zellij action dump-screen <path>`                        |
| Dump full scrollback          | `zellij action dump-screen --full <path>`                 |
| Run command in new pane       | `zellij run -- <cmd> <args>`                              |
| Run floating command          | `zellij run -f -- <cmd> <args>`                           |
| Run and close on exit         | `zellij run -c -- <cmd> <args>`                           |

## Session Management

Always use named sessions for automation. Anonymous sessions are hard to target.

```bash
# Create a named session
zellij -s my-project

# List all sessions (shows name and status)
zellij list-sessions

# Attach to an existing session
zellij attach my-project

# Kill a specific session
zellij kill-session my-project

# Kill all sessions (use with caution)
zellij kill-all-sessions
```

## Pane Operations

Panes split the current tab into multiple terminal areas.

```bash
# Split a new pane (default: tiled layout)
zellij action new-pane

# Split in a specific direction
zellij action new-pane --direction down
zellij action new-pane --direction right

# Open a floating pane
zellij action new-pane --floating

# Close the currently focused pane
zellij action close-pane

# Navigate between panes
zellij action move-focus left
zellij action move-focus right
zellij action move-focus up
zellij action move-focus down

# Toggle floating panes visibility
zellij action toggle-floating-panes
```

### Important: Pane Targeting Limitation

Zellij CLI commands like `write`, `write-chars`, and `dump-screen` always operate
on the **currently focused pane**. There is no `--pane-id` flag to target a
specific pane directly. You must navigate to the desired pane first:

```bash
# Navigate to the pane, then send input
zellij action move-focus down
zellij action write-chars "my command"
zellij action write 13  # Enter
```

## Tab Management

Tabs organize panes into groups within a session.

```bash
# Create a new tab
zellij action new-tab
zellij action new-tab --name "servers"

# Switch to a tab by name
zellij action go-to-tab-name "servers"

# Switch to a tab by index (1-based)
zellij action go-to-tab 1

# Rename the current tab
zellij action rename-tab "new-name"

# Close the current tab
zellij action close-tab
```

## Sending Input

### Text Input

Use `write-chars` to send strings as if typed on a keyboard:

```bash
zellij action write-chars "echo hello world"
zellij action write 13  # press Enter to execute
```

### Control Bytes

Use `write` to send raw byte values for special keys:

| Key       | Byte | Command                     |
|-----------|------|-----------------------------|
| Enter     | 13   | `zellij action write 13`    |
| Ctrl+C    | 3    | `zellij action write 3`     |
| Ctrl+D    | 4    | `zellij action write 4`     |
| Ctrl+L    | 12   | `zellij action write 12`    |
| Ctrl+Z    | 26   | `zellij action write 26`    |
| Tab       | 9    | `zellij action write 9`     |
| Escape    | 27   | `zellij action write 27`    |
| Backspace | 127  | `zellij action write 127`   |

### Sending a Command to the Focused Pane

```bash
zellij action write-chars "npm run dev"
zellij action write 13
```

## Capturing Output

Zellij dumps screen content to a **file** (not stdout). You must always read the
file back after dumping.

```bash
# Capture visible screen of focused pane
zellij action dump-screen /tmp/zellij-capture.txt
cat /tmp/zellij-capture.txt

# Capture full scrollback history
zellij action dump-screen --full /tmp/zellij-scrollback.txt
cat /tmp/zellij-scrollback.txt
```

### Capture-and-Read Pattern

```bash
CAPTURE_FILE="/tmp/zellij-capture-$$.txt"
zellij action dump-screen "$CAPTURE_FILE"
output=$(cat "$CAPTURE_FILE")
rm -f "$CAPTURE_FILE"
echo "$output"
```

## Running Commands

`zellij run` opens a new pane and executes a command in it.

```bash
# Run a command in a new tiled pane
zellij run -- ls -la

# Run in a floating pane
zellij run -f -- htop

# Run and close the pane when the command exits
zellij run -c -- make build

# Run with a custom pane name
zellij run -n "build" -- cargo build

# Run in a specific working directory
zellij run --cwd /path/to/project -- npm test

# Combine options
zellij run -f -c -n "tests" --cwd ./backend -- pytest -v
```

## Layouts (KDL Format)

Define workspace layouts in KDL format for reproducible setups:

```kdl
// my-layout.kdl
layout {
    tab name="code" focus=true {
        pane split_direction="vertical" {
            pane command="nvim" size="60%"
            pane split_direction="horizontal" {
                pane command="bash"
                pane command="bash" {
                    args "run" "dev"
                    cwd "/path/to/project"
                }
            }
        }
    }
    tab name="logs" {
        pane command="tail" {
            args "-f" "/var/log/app.log"
        }
    }
}
```

Start a session with a layout:

```bash
zellij --layout my-layout.kdl -s my-project
```

## Common Patterns

### Start a Server and Wait for Ready

```bash
# Create session and start server
zellij -s dev
zellij action write-chars "npm run dev"
zellij action write 13

# Wait for server to be ready (uses helper script)
./tools/wait-for-text.sh -s dev -p "ready on port" -t 60
```

### Multi-Pane Orchestration

```bash
# Create session with named tabs
zellij -s workspace

# Tab 1: backend server
zellij action rename-tab "backend"
zellij action write-chars "cd backend && cargo run"
zellij action write 13

# Tab 2: frontend server
zellij action new-tab --name "frontend"
zellij action write-chars "cd frontend && npm run dev"
zellij action write 13

# Tab 3: test runner in split panes
zellij action new-tab --name "tests"
zellij action write-chars "cd backend && cargo watch -x test"
zellij action write 13
zellij action new-pane --direction right
zellij action write-chars "cd frontend && npm run test:watch"
zellij action write 13

# Go back to backend tab
zellij action go-to-tab-name "backend"
```

### Run Command and Capture Output

```bash
CAPTURE="/tmp/zellij-cmd-$$.txt"

# Send command to focused pane
zellij action write-chars "echo 'DONE_MARKER'"
zellij action write 13
sleep 1

# Capture and parse
zellij action dump-screen "$CAPTURE"
cat "$CAPTURE"
rm -f "$CAPTURE"
```

### Interactive REPL Session

```bash
# Start Python REPL in a session
zellij -s python-repl
zellij action write-chars "python3"
zellij action write 13
sleep 1

# Send commands to the REPL
zellij action write-chars "import json"
zellij action write 13
zellij action write-chars "data = json.loads('{\"key\": \"value\"}')"
zellij action write 13
zellij action write-chars "print(data)"
zellij action write 13
```

## Helper Scripts

This plugin includes helper scripts in the `tools/` directory:

- **`tools/wait-for-text.sh`** -- Poll a session's screen output until a text
  pattern appears or a timeout is reached. Useful for waiting on server startup
  messages, prompts, or command completion markers.
- **`tools/find-sessions.sh`** -- List and filter Zellij sessions by name
  substring. Wraps `zellij list-sessions` with optional filtering.

## Cleanup

Always clean up sessions when done to avoid resource leaks:

```bash
# Kill a specific session
zellij kill-session my-project

# Kill all sessions (nuclear option)
zellij kill-all-sessions

# Verify cleanup
zellij list-sessions
```

Leaving sessions running consumes system resources (memory, file descriptors, PTYs).
Always kill sessions you no longer need, especially in automated workflows.
