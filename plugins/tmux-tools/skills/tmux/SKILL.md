---
name: tmux
description: "Remote control tmux sessions for interactive CLIs (python, gdb, etc.) by sending keystrokes and scraping pane output."
license: Vibecoded
---

# tmux Skill

Use tmux as a programmable terminal multiplexer for interactive work. Works on Linux and macOS with stock tmux; avoid custom config by using a private socket.

## When to Use

**Use tmux when:**
- Running vim, nano, or other text editors programmatically
- Controlling interactive REPLs (Python, Node, gdb, lldb, etc.)
- Handling interactive git commands (`git rebase -i`, `git add -p`)
- Working with full-screen terminal apps
- Commands that require terminal control codes or readline

**Don't use for:**
- Simple non-interactive commands (use regular Bash tool)
- Commands that accept input via stdin redirection
- One-shot commands that don't need interaction

## Quick Reference

| Task           | Command                                                  |
| -------------- | -------------------------------------------------------- |
| Start session  | `tmux -S "$SOCKET" new -d -s <name> <command>`           |
| Send input     | `tmux -S "$SOCKET" send-keys -t <name> 'text' Enter`     |
| Send literal   | `tmux -S "$SOCKET" send-keys -t <name> -l -- 'text'`     |
| Capture output | `tmux -S "$SOCKET" capture-pane -p -J -t <name> -S -200` |
| List sessions  | `tmux -S "$SOCKET" list-sessions`                        |
| Kill session   | `tmux -S "$SOCKET" kill-session -t <name>`               |
| Attach to view | `tmux -S "$SOCKET" attach -t <name>`                     |

## Quickstart (isolated socket)

```bash
SOCKET_DIR=${TMPDIR:-/tmp}/claude-tmux-sockets  # well-known dir for all agent sockets
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/claude.sock"                # keep agent sessions separate from your personal tmux
SESSION=claude-python                           # slug-like names; avoid spaces
tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- 'python3 -q' Enter
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200  # watch output
tmux -S "$SOCKET" kill-session -t "$SESSION"                   # clean up
```

After starting a session ALWAYS tell the user how to monitor the session by giving them a command to copy paste:

```
To monitor this session yourself:
  tmux -S "$SOCKET" attach -t claude-lldb

Or to capture the output once:
  tmux -S "$SOCKET" capture-pane -p -J -t claude-lldb:0.0 -S -200
```

This must ALWAYS be printed right after a session was started and once again at the end of the tool loop.  But the earlier you send it, the happier the user will be.

## Socket convention

- Agents MUST place tmux sockets under `CLAUDE_TMUX_SOCKET_DIR` (defaults to `${TMPDIR:-/tmp}/claude-tmux-sockets`) and use `tmux -S "$SOCKET"` so we can enumerate/clean them. Create the dir first: `mkdir -p "$CLAUDE_TMUX_SOCKET_DIR"`.
- Default socket path to use unless you must isolate further: `SOCKET="$CLAUDE_TMUX_SOCKET_DIR/claude.sock"`.

## Socket management

**Understanding socket flags:**
- `-L socket-name`: Creates/connects to named socket in default location (`/tmp/tmux-UID/socket-name`). Use for simple isolation.
- `-S /full/path`: Creates/connects to socket at exact path. Use for custom directories (required for `CLAUDE_TMUX_SOCKET_DIR`).

**Socket recovery:**
- If a socket is accidentally deleted, recover it by sending `USR1` signal: `pkill -USR1 tmux`
- Check socket path: `tmux -S "$SOCKET" display -p '#{socket_path}'`

**Maintenance scripts:**
- **Check socket health:** `./tools/socket-health.sh "$SOCKET"` - diagnose unresponsive sockets
- **Recover socket:** `./tools/socket-health.sh --recover "$SOCKET"` - attempt automatic recovery
- **Clean dead sockets:** `./tools/cleanup-sockets.sh` - remove orphaned socket files
- **Dry run cleanup:** `./tools/cleanup-sockets.sh --dry-run` - preview what would be removed

## Targeting panes and naming

- Target format: `{session}:{window}.{pane}`, defaults to `:0.0` if omitted. Keep names short (e.g., `claude-py`, `claude-gdb`).
- Use `-S "$SOCKET"` consistently to stay on the private socket path. If you need user config, drop `-f /dev/null`; otherwise `-f /dev/null` gives a clean config.
- Inspect: `tmux -S "$SOCKET" list-sessions`, `tmux -S "$SOCKET" list-panes -a`.

## Finding sessions

- List sessions on your active socket with metadata: `./tools/find-sessions.sh -S "$SOCKET"`; add `-q partial-name` to filter.
- Scan all sockets under the shared directory: `./tools/find-sessions.sh --all` (uses `CLAUDE_TMUX_SOCKET_DIR` or `${TMPDIR:-/tmp}/claude-tmux-sockets`).

## Sending input safely

- Prefer literal sends to avoid shell splitting: `tmux -S "$SOCKET" send-keys -t target -l -- "$cmd"`
- When composing inline commands, use single quotes or ANSI C quoting to avoid expansion: `tmux ... send-keys -t target -- $'python3 -m http.server 8000'`.
- To send control keys: `tmux ... send-keys -t target C-c`, `C-d`, `C-z`, `Escape`, etc.

## Watching output

- Capture recent history (joined lines to avoid wrapping artifacts): `tmux -S "$SOCKET" capture-pane -p -J -t target -S -200`.
- For continuous monitoring, poll with the helper script (below) instead of `tmux wait-for` (which does not watch pane output).
- You can also temporarily attach to observe: `tmux -S "$SOCKET" attach -t "$SESSION"`; detach with `Ctrl+b d`.
- When giving instructions to a user, **explicitly print a copy/paste monitor command** alongside the action don't assume they remembered the command.

## Spawning Processes

Some special rules for processes:

- When asked to debug, use lldb by default
- **Python REPL:** ALWAYS set `PYTHON_BASIC_REPL=1` environment variable before starting Python. This is critical—the fancy console interferes with send-keys. Example:
  ```bash
  tmux -S "$SOCKET" send-keys -t "$SESSION" 'PYTHON_BASIC_REPL=1 python3 -q' Enter
  ```

## Synchronizing / waiting for prompts

- Use timed polling to avoid races with interactive tools. Example: wait for a Python prompt before sending code:
  ```bash
  ./tools/wait-for-text.sh -t "$SESSION":0.0 -p '^>>>' -T 15 -l 4000
  ```
- For long-running commands, poll for completion text (`"Type quit to exit"`, `"Program exited"`, etc.) before proceeding.

## Interactive tool recipes

- **Python REPL**: `tmux ... send-keys -- 'PYTHON_BASIC_REPL=1 python3 -q' Enter`; wait for `^>>>`; send code with `-l`; interrupt with `C-c`. ALWAYS set `PYTHON_BASIC_REPL=1`.
- **gdb**: `tmux ... send-keys -- 'gdb --quiet ./a.out' Enter`; disable paging `tmux ... send-keys -- 'set pagination off' Enter`; break with `C-c`; issue `bt`, `info locals`, etc.; exit via `quit` then confirm `y`.
- **Other TTY apps** (ipdb, psql, mysql, node, bash): same pattern—start the program, poll for its prompt, then send literal text and Enter.

## Cleanup

- Kill a session when done: `tmux -S "$SOCKET" kill-session -t "$SESSION"`.
- Kill all sessions on a socket: `tmux -S "$SOCKET" list-sessions -F '#{session_name}' | xargs -r -n1 tmux -S "$SOCKET" kill-session -t`.
- Remove everything on the private socket: `tmux -S "$SOCKET" kill-server`.

## Helper: wait-for-text.sh

`./tools/wait-for-text.sh` polls a pane for a regex (or fixed string) with a timeout. Works on Linux/macOS with bash + tmux + grep.

```bash
./tools/wait-for-text.sh -t session:0.0 -p 'pattern' [-F] [-T 20] [-i 0.5] [-l 2000]
```

- `-t`/`--target` pane target (required)
- `-p`/`--pattern` regex to match (required); add `-F` for fixed string
- `-T` timeout seconds (integer, default 15)
- `-i` poll interval seconds (default 0.5)
- `-l` history lines to search from the pane (integer, default 1000)
- Exits 0 on first match, 1 on timeout. On failure prints the last captured text to stderr to aid debugging.

## Helper: socket-health.sh

`./tools/socket-health.sh` checks socket health and attempts recovery if needed.

```bash
./tools/socket-health.sh [--recover] [--verbose] <socket-path>
```

- `socket-path` - Path to tmux socket file (required)
- `-r`/`--recover` - Attempt recovery if unresponsive (sends `USR1` to tmux)
- `-v`/`--verbose` - Show detailed information
- Exits 0 if healthy or recovered, 1 if unresponsive or failed

**Status codes:**
- `HEALTHY` - Socket is responsive
- `MISSING` - Socket file doesn't exist
- `INVALID` - File exists but isn't a socket
- `UNRESPONSIVE` - Socket exists but tmux server not responding
- `RECOVERED` - Socket recovered after `USR1` signal
- `RECOVERY FAILED` - Recovery attempt unsuccessful

## Helper: cleanup-sockets.sh

`./tools/cleanup-sockets.sh` scans for and removes dead socket files.

```bash
./tools/cleanup-sockets.sh [--dir <path>] [--force] [--dry-run]
```

- `-d`/`--dir` - Socket directory (default: `CLAUDE_TMUX_SOCKET_DIR`)
- `-f`/`--force` - Auto-remove without prompting
- `-n`/`--dry-run` - Show what would be removed without deleting
- Scans socket directory, tests each socket, and removes unresponsive ones
