---
name: justfile-expert
description: Expert guidance for Just task runner and justfiles. Use when working with justfiles, creating build automation, defining task recipes, organizing project commands, or troubleshooting Just syntax errors. Covers modern Just features including recipe groups, attributes, settings, and best practices for cross-platform task automation.
---

# Justfile Expert

## Overview

Just is a modern command runner for defining and executing project tasks. This skill provides expertise in creating, organizing, and troubleshooting justfiles with modern syntax and patterns.

## Quick Start

Basic justfile structure:

```just
# Settings at top
set shell := ["bash", "-uc"]
set dotenv-load

# Default recipe (first one runs when no recipe specified, or use [default] attribute)
default:
    @just --list

# Grouped recipes - use [group('name')] for organization
# Build the project
[group('build')]
build:
    cargo build --release

# Run tests
[group('test')]
test:
    cargo test
```

**Key syntax rules:**
1. Recipe body lines MUST be indented with spaces or tabs (not mixed)
2. Comments describing recipes go BEFORE any attributes
3. Use `@` prefix to suppress command echoing
4. Use `-` prefix to ignore command errors

## Recipe Attributes

### Available Attributes (with version introduced)

| Attribute | Purpose |
|-----------|---------|
| `[group('name')]` | Organize recipe into a named group |
| `[private]` | Hide from `--list` output |
| `[confirm]` | Require y/n confirmation before running |
| `[confirm('prompt')]` | Custom confirmation prompt |
| `[doc('text')]` | Set/override documentation comment |
| `[default]` | Mark as the default recipe (v1.43.0) |
| `[no-cd]` | Don't change to justfile directory |
| `[no-exit-message]` | Suppress error message on failure |
| `[no-quiet]` | Override `set quiet` for this recipe |
| `[linux]` | Only run on Linux |
| `[macos]` | Only run on macOS |
| `[windows]` | Only run on Windows |
| `[unix]` | Only run on Unix-like systems |
| `[parallel]` | Run dependencies in parallel (v1.42.0) |
| `[positional-arguments]` | Enable positional args for this recipe |
| `[script]` | Execute as script (v1.33.0) |
| `[script('interpreter')]` | Execute with specific interpreter |
| `[extension('.ext')]` | Set shebang script file extension |
| `[working-directory('path')]` | Override working directory |

### Attribute Syntax

Both forms are valid for single-argument attributes:
```just
[group('build')]    # Parentheses form
[group: 'build']    # Colon shorthand form
```

Multiple attributes can be combined:
```just
# On separate lines
[group('build')]
[private]
[linux]
helper:
    echo "hidden linux helper"

# Or comma-separated on one line
[group('deploy'), confirm, private]
deploy-prod:
    kubectl apply -f production/
```

## Recipe Groups

Organize recipes into logical groups for discoverability:

```just
# Install dependencies
[group('setup')]
install:
    npm install

# Format code
[group('quality')]
fmt:
    prettier --write .

# Run all tests
[group('test')]
test:
    npm test
```

**Recommended group names:** `setup`, `build`, `test`, `quality`, `docs`, `release`, `dev`, `clean`, `info`, `deploy`

List groups with `just --groups`. Recipes appear under their groups in `just --list`.

## Recipe Parameters

```just
# Required parameter
build target:
    cargo build --target {{target}}

# Default value
test filter="":
    pytest {{ if filter != "" { "-k " + filter } else { "" } }}

# Variadic (one or more)
backup +files:
    tar -czf backup.tar.gz {{files}}

# Variadic (zero or more)
commit message *flags:
    git commit {{flags}} -m "{{message}}"

# Export as environment variable
serve $PORT="8080":
    ./server --port $PORT
```

## Dependencies

```just
# Prior dependencies (run before)
build: install
    cargo build

# Subsequent dependencies (run after) with &&
deploy: build && notify cleanup
    ./deploy.sh

# Dependencies with arguments
release: (build "release") (test "integration")
    ./release.sh

# Parallel dependencies
[parallel]
all: lint test build
```

## Variables and Expressions

### Variable Assignment

```just
version := "1.0.0"
target := "x86_64-unknown-linux-gnu"
build_dir := justfile_directory() / "build"
```

### Operators

```just
# Concatenation
full_name := first + " " + last

# Path joining (always uses /)
config := home_directory() / ".config" / "myapp"

# Logical operators (unstable, use `set unstable`)
value := env('VAR') || 'default'    # Fallback if empty
```

### Backtick Command Evaluation

```just
# Single line
git_hash := `git rev-parse --short HEAD`

# Multi-line (indented backticks)
build_info := ```
    echo "Version: $(cat VERSION)"
    echo "Date: $(date)"
  ```
```

### Shell-Expanded Strings (v1.27.0)

```just
# x-prefix enables shell expansion at compile time
config_path := x'~/.config/$APP_NAME'
```

## Conditional Expressions

```just
foo := if os() == "linux" { "penguin" } else { "other" }

# Regex matching
bar := if version =~ '[0-9]+\.[0-9]+' { "valid" } else { "invalid" }

# Chained conditionals
target := if os() == "macos" {
  if arch() == "aarch64" { "aarch64-apple-darwin" } else { "x86_64-apple-darwin" }
} else if os() == "linux" {
  "x86_64-unknown-linux-gnu"
} else {
  error("Unsupported OS")
}
```

## Shebang and Script Recipes

### Shebang Recipes

```just
# Python
analyze:
    #!/usr/bin/env python3
    import json
    print(json.dumps({"status": "ok"}))

# Bash with safety options
deploy:
    #!/usr/bin/env bash
    set -euxo pipefail
    echo "Deploying..."
```

### Script Recipes (v1.33.0)

```just
set script-interpreter := ['uv', 'run', '--script']

[script]
hello:
    print("Hello from Python!")
```

## Settings Reference

```just
set shell := ["bash", "-uc"]              # Shell for recipes
set windows-shell := ["pwsh", "-Command"] # Windows-specific shell
set dotenv-load                           # Load .env file
set dotenv-filename := ".env.local"       # Custom .env filename
set dotenv-path := "/path/to/.env"        # Specific .env path
set dotenv-required                       # Error if .env missing
set export                                # Export all vars as env vars
set positional-arguments                  # Enable positional args globally
set quiet                                 # Suppress command echoing
set fallback                              # Search parent dirs for justfile
set ignore-comments                       # Ignore # in recipe lines
set unstable                              # Enable unstable features
set working-directory := "subdir"         # Change working directory
set script-interpreter := ['sh', '-eu']   # Interpreter for [script] recipes
```

## Constants (v1.37.0+)

Built-in constants for terminal styling and utilities:

```just
# Path separators
PATH_SEP       # "/" on Unix, "\" on Windows
PATH_VAR_SEP   # ":" on Unix, ";" on Windows

# Hex character sets
HEX, HEXLOWER  # "0123456789abcdef"
HEXUPPER       # "0123456789ABCDEF"

# Terminal colors
RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE, BLACK
BG_RED, BG_GREEN, BG_BLUE, BG_YELLOW, BG_CYAN, BG_MAGENTA, BG_WHITE, BG_BLACK

# Terminal styles
BOLD, ITALIC, UNDERLINE, INVERT, HIDE, STRIKETHROUGH
NORMAL         # Reset styling
CLEAR          # Clear screen
```

Usage:
```just
@status:
    echo '{{GREEN}}Success!{{NORMAL}}'
    echo '{{BOLD}}{{RED}}Error{{NORMAL}}'
```

## Common Patterns

### Default Recipe with List

```just
default:
    @just --list

# Or use [default] attribute on any recipe
[default]
help:
    @just --list --list-heading $'Commands:\n'
```

### Subcommand Pattern

```just
# Usage: just db migrate, just db seed, just db reset
[group('database')]
db command="":
    #!/usr/bin/env bash
    case "{{command}}" in
        migrate) ./db migrate ;;
        seed) ./db seed ;;
        reset) ./db reset ;;
        "") just --list | grep -A100 '\[database\]' ;;
        *) echo "Unknown: {{command}}" && exit 1 ;;
    esac
```

### Cross-Platform Recipes

```just
[linux]
open path:
    xdg-open {{path}}

[macos]
open path:
    open {{path}}

[windows]
open path:
    start {{path}}
```

### Confirmation for Destructive Actions

```just
[confirm("This will delete all data. Continue?")]
[group('dangerous')]
reset-db:
    dropdb myapp && createdb myapp
```

## Modules and Imports

### Modules (v1.31.0)

```just
# Load foo.just or foo/mod.just as submodule
mod foo

# Optional module (no error if missing)
mod? optional_module

# Custom path
mod utils 'scripts/utils.just'

# Module with docs and group
# Utility commands
[group('tools')]
mod tools

# Call module recipes
main: foo::build
    @just foo::test
```

### Imports

```just
# Include another justfile's recipes directly
import 'common.just'

# Optional import
import? 'local-overrides.just'
```

## Useful Functions

### System Info
- `os()` - Operating system (linux, macos, windows)
- `os_family()` - OS family (unix, windows)
- `arch()` - Architecture (x86_64, aarch64, etc.)
- `num_cpus()` - Number of logical CPUs

### Paths
- `justfile()` - Path to current justfile
- `justfile_directory()` - Directory containing justfile
- `source_file()` - Current source file (for imports/modules)
- `source_directory()` - Directory of current source file
- `home_directory()` - User's home directory
- `invocation_directory()` - Directory where just was invoked

### Environment
- `env('KEY')` - Get env var (error if not set)
- `env('KEY', 'default')` - Get env var with default

### Executables
- `require('name')` - Find executable or error (v1.39.0)
- `which('name')` - Find executable or empty string (unstable)

### Filesystem
- `path_exists('path')` - Check if path exists
- `read('path')` - Read file contents (v1.39.0)

### Strings
- `replace(s, from, to)` - Replace all occurrences
- `replace_regex(s, regex, replacement)` - Regex replace
- `trim(s)`, `trim_start(s)`, `trim_end(s)` - Whitespace trimming
- `quote(s)` - Shell-safe quoting
- `uppercase(s)`, `lowercase(s)` - Case conversion
- `kebabcase(s)`, `snakecase(s)`, `uppercamelcase(s)` - Case styles

### External Commands
- `shell('command', args...)` - Execute shell command and return output

### Utilities
- `uuid()` - Generate random UUID
- `sha256(s)`, `sha256_file(path)` - SHA-256 hash
- `datetime(format)`, `datetime_utc(format)` - Current time
- `error('message')` - Halt with error message

## Troubleshooting

### "Extraneous attribute" Error

**Cause:** Something between attribute and recipe name

**Wrong:**
```just
[group('setup')]
# This comment causes the error
install:
    npm install
```

**Correct:**
```just
# Comment goes before attributes
[group('setup')]
install:
    npm install
```

### Recipe Not Appearing in `--list`

**Check:**
1. Not marked `[private]` or name starts with `_`
2. No syntax errors (`just --dump` to verify)
3. File saved

### Variable Not Expanding

- Just variables: `{{variable}}`
- Shell variables: `$VARIABLE`

### Each Line Runs in New Shell

This means `cd` doesn't persist:

```just
# Wrong - cd has no effect on pwd
wrong:
    cd subdir
    pwd

# Correct - use && or shebang
correct:
    cd subdir && pwd

also-correct:
    #!/usr/bin/env bash
    cd subdir
    pwd
```

### Command Output Not Captured

Use backticks for command substitution, not `$(...)`:

```just
# Wrong in assignments
version := $(cat VERSION)

# Correct
version := `cat VERSION`
```

## Command-Line Reference

```bash
just                    # Run default recipe
just recipe             # Run specific recipe
just recipe arg1 arg2   # Pass arguments
just var=value recipe   # Override variable
just --list             # List recipes
just --list --unsorted  # List in file order
just --groups           # List groups
just --show recipe      # Show recipe source
just --summary          # Compact recipe list
just --dump             # Dump parsed justfile
just --evaluate         # Evaluate and print variables
just --fmt              # Format justfile
just --check            # Check for errors without running
just -f path/justfile   # Use specific justfile
just -d directory       # Set working directory
```

## Resources

See **references/just-docs.md** for:
- Complete function reference with examples
- All settings with detailed explanations
- Advanced module patterns
- String escape sequences
- Grammar specification

### Documentation Links

- Official manual: https://just.systems/man/en/
- GitHub: https://github.com/casey/just
- Cheatsheet: https://cheatography.com/linux-china/cheat-sheets/justfile/
