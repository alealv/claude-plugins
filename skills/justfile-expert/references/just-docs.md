# Just Comprehensive Reference

This file contains detailed reference information for advanced Just features. Load this when you need information beyond the common patterns in SKILL.md.

## Table of Contents

1. Complete Functions Reference
2. All Attributes Reference
3. Complete Settings Reference
4. String Syntax and Escape Sequences
5. Module System Deep Dive
6. Advanced Patterns
7. Error Handling
8. Command-Line Options

---

## 1. Complete Functions Reference

### System Information Functions

```just
os()          # "linux", "macos", "windows", "android", "freebsd", etc.
os_family()   # "unix" or "windows"
arch()        # "x86_64", "aarch64", "arm", "wasm32", etc.
num_cpus()    # Number of logical CPUs (v1.15.0)
```

### Path Functions

```just
# Current justfile location
justfile()                   # Full path to justfile
justfile_directory()         # Directory containing justfile

# For imports/modules (v1.27.0)
source_file()                # Path of current source file
source_directory()           # Directory of current source file

# User directories
home_directory()             # User's home directory
cache_directory()            # User cache dir (~/.cache on Linux)
config_directory()           # User config dir (~/.config on Linux)
config_local_directory()     # Local config directory
data_directory()             # User data dir
data_local_directory()       # Local data directory
executable_directory()       # User executable dir (~/.local/bin on Linux)

# Invocation
invocation_directory()       # Directory where just was invoked (cygpath on Windows)
invocation_directory_native() # Verbatim invocation directory

# Path manipulation
absolute_path(path)          # Convert relative to absolute
canonicalize(path)           # Resolve symlinks, normalize (v1.24.0)
clean(path)                  # Remove extra /, intermediate .., etc.
extension(path)              # File extension without dot
file_name(path)              # Filename without directory
file_stem(path)              # Filename without extension
parent_directory(path)       # Parent directory
without_extension(path)      # Path without extension
join(a, b, ...)              # Join path components (uses OS separator!)
```

**Note:** The `join()` function uses `\` on Windows. Prefer the `/` operator for consistent cross-platform behavior:
```just
# Prefer this (always uses /)
path := home_directory() / ".config" / "app"

# Instead of this (uses \ on Windows)
path := join(home_directory(), ".config", "app")
```

### Environment Functions

```just
env('KEY')                   # Get env var, error if not set (v1.15.0)
env('KEY', 'default')        # Get env var with default (v1.15.0)

# Deprecated aliases
env_var('KEY')               # Use env('KEY') instead
env_var_or_default('KEY', 'default')  # Use env('KEY', 'default') instead
```

### Executable Functions

```just
just_executable()            # Absolute path to just binary
just_pid()                   # Process ID of just
require('name')              # Find in PATH or error (v1.39.0)
which('name')                # Find in PATH or empty string (unstable)
```

**Example:**
```just
bash := require("bash")

test:
    @echo "Using bash at: {{bash}}"
```

### Filesystem Functions

```just
path_exists('path')          # Returns "true" or "false"
read('path')                 # Read file contents as string (v1.39.0)
```

### String Manipulation Functions

```just
# Whitespace
trim(s)                      # Remove leading/trailing whitespace
trim_start(s)                # Remove leading whitespace
trim_end(s)                  # Remove trailing whitespace
trim_start_match(s, prefix)  # Remove prefix once
trim_start_matches(s, prefix) # Remove prefix repeatedly
trim_end_match(s, suffix)    # Remove suffix once
trim_end_matches(s, suffix)  # Remove suffix repeatedly

# Transformation
replace(s, from, to)         # Replace all occurrences
replace_regex(s, regex, replacement)  # Regex replace with capture groups
quote(s)                     # Shell-safe quoting
encode_uri_component(s)      # URL encode (v1.27.0)

# Whitespace-separated string manipulation
append(suffix, s)            # Append to each word: append('/src', 'foo bar') -> 'foo/src bar/src'
prepend(prefix, s)           # Prepend to each word: prepend('src/', 'foo bar') -> 'src/foo src/bar'
```

### Case Conversion Functions

```just
lowercase(s)                 # all lowercase
uppercase(s)                 # ALL UPPERCASE
capitalize(s)                # First char upper, rest lower (v1.7.0)
kebabcase(s)                 # kebab-case (v1.7.0)
snakecase(s)                 # snake_case (v1.7.0)
shoutysnakecase(s)           # SHOUTY_SNAKE_CASE (v1.7.0)
shoutykebabcase(s)           # SHOUTY-KEBAB-CASE (v1.7.0)
titlecase(s)                 # Title Case (v1.7.0)
lowercamelcase(s)            # lowerCamelCase (v1.7.0)
uppercamelcase(s)            # UpperCamelCase (v1.7.0)
```

### External Command Functions

```just
shell('command', args...)    # Execute shell command, return stdout (v1.27.0)
```

**Usage:**
```just
# Basic usage
date := shell('date +%Y-%m-%d')

# With arguments (note: $1 refers to first arg, not $0)
contents := shell('cat $1', 'file.txt')

# More complex
version := shell('grep "^version" $1 | cut -d= -f2', 'Cargo.toml')
```

### Hash and UUID Functions

```just
uuid()                       # Random v4 UUID
sha256('string')             # SHA-256 hash of string
sha256_file('path')          # SHA-256 hash of file
blake3('string')             # BLAKE3 hash (v1.25.0)
blake3_file('path')          # BLAKE3 hash of file (v1.25.0)
```

### Random Functions

```just
choose(n, alphabet)          # Generate n random chars from alphabet (v1.27.0)
```

**Example:**
```just
# Generate 32-char hex string
token := choose('32', HEX)

# Generate 16-char alphanumeric
id := choose('16', 'abcdefghijklmnopqrstuvwxyz0123456789')
```

### DateTime Functions (v1.30.0)

```just
datetime(format)             # Local time with strftime format
datetime_utc(format)         # UTC time with strftime format
```

**Common format specifiers:**
- `%Y-%m-%d` - 2024-01-15
- `%H:%M:%S` - 14:30:45
- `%Y%m%d%H%M%S` - 20240115143045
- `%A, %B %d, %Y` - Monday, January 15, 2024

### Semantic Version Functions

```just
semver_matches(version, requirement)  # Check version against requirement (v1.16.0)
```

**Example:**
```just
is_compatible := semver_matches('1.2.3', '>=1.0.0')
```

### Terminal Style Functions (v1.37.0)

```just
style('name')                # Get just's internal style escape sequence
```

Available names: `'command'`, `'error'`, `'warning'`

```just
@error:
    echo '{{style("error")}}Something went wrong{{NORMAL}}'
```

### Utility Functions

```just
error('message')             # Halt execution with error
is_dependency()              # Returns "true" if recipe called as dependency
```

---

## 2. All Attributes Reference

### Recipe Attributes

| Attribute | Since | Description |
|-----------|-------|-------------|
| `[confirm]` | 1.17.0 | Require y/n confirmation |
| `[confirm('prompt')]` | 1.23.0 | Custom confirmation prompt |
| `[default]` | 1.43.0 | Mark as default recipe |
| `[doc('text')]` | 1.27.0 | Set documentation comment |
| `[doc]` | 1.27.0 | Suppress documentation comment |
| `[extension('.ext')]` | 1.32.0 | Shebang script file extension |
| `[group('name')]` | 1.27.0 | Assign to recipe group |
| `[linux]` | 1.8.0 | Enable only on Linux |
| `[macos]` | 1.8.0 | Enable only on macOS |
| `[metadata(...)]` | 1.42.0 | Attach metadata (unused by just) |
| `[no-cd]` | 1.9.0 | Don't change directory |
| `[no-exit-message]` | 1.7.0 | Suppress error message |
| `[no-quiet]` | 1.23.0 | Override `set quiet` |
| `[openbsd]` | 1.38.0 | Enable only on OpenBSD |
| `[parallel]` | 1.42.0 | Run dependencies in parallel |
| `[positional-arguments]` | 1.29.0 | Enable positional arguments |
| `[private]` | 1.10.0 | Hide from `--list` |
| `[script]` | 1.33.0 | Execute as script |
| `[script('interpreter')]` | 1.32.0 | Execute with specific interpreter |
| `[unix]` | 1.8.0 | Enable on Unix-like systems |
| `[windows]` | 1.8.0 | Enable only on Windows |
| `[working-directory('path')]` | 1.38.0 | Override working directory |

### Module Attributes

| Attribute | Description |
|-----------|-------------|
| `[group('name')]` | Assign module to group |
| `[private]` | Hide module from `--list` |
| `[doc('text')]` | Module documentation |

### Alias Attributes

| Attribute | Description |
|-----------|-------------|
| `[private]` | Hide alias from `--list` |

### Attribute Syntax Forms

Single-argument attributes support both forms:
```just
[group('build')]    # Parentheses form
[group: 'build']    # Colon shorthand

[doc('Build the project')]
[doc: 'Build the project']
```

Multiple attributes:
```just
# Separate lines
[group('build')]
[private]
[linux]
recipe:

# Comma-separated (v1.14.0)
[group('build'), private, linux]
recipe:
```

---

## 3. Complete Settings Reference

### Shell Settings

```just
set shell := ["bash", "-uc"]              # Default shell
set windows-shell := ["pwsh", "-Command"] # Windows-only shell
set windows-powershell                    # Deprecated: use windows-shell
set script-interpreter := ['sh', '-eu']   # For [script] recipes (v1.33.0)
```

### Environment Settings

```just
set dotenv-load                    # Load .env file if present
set dotenv-filename := '.env.local' # Custom .env filename
set dotenv-path := '/path/.env'    # Specific path (error if missing)
set dotenv-required                # Error if .env not found
set dotenv-override                # Override existing env vars with .env values
set export                         # Export all just variables as env vars
```

### Execution Settings

```just
set positional-arguments           # Pass args as $1, $2, etc.
set quiet                          # Don't echo commands
set ignore-comments                # Ignore # in recipe lines
set fallback                       # Search parent directories for justfile
set tempdir := '/tmp/just'         # Custom temp directory
set working-directory := 'subdir'  # Change working directory (v1.33.0)
set unstable                       # Enable unstable features (v1.31.0)
```

### Override Settings

```just
set allow-duplicate-recipes        # Allow later recipes to override earlier
set allow-duplicate-variables      # Allow later variables to override earlier
```

### Boolean Setting Syntax

Boolean settings can be written two ways:
```just
set dotenv-load          # Equivalent to:
set dotenv-load := true
```

---

## 4. String Syntax and Escape Sequences

### String Types

```just
# Single-quoted (no escape processing)
raw := 'Tab: \t Newline: \n'    # Literal \t and \n

# Double-quoted (escape sequences processed)
escaped := "Tab:\tNewline:\n"   # Actual tab and newline

# Indented triple-quoted (common indentation stripped)
multi := '''
  Line 1
  Line 2
'''
# Result: "Line 1\nLine 2\n"

# Shell-expanded (v1.27.0)
path := x'~/$USER/config'       # Expands ~ and $USER at compile time
```

### Escape Sequences (Double-Quoted Only)

| Sequence | Result |
|----------|--------|
| `\\` | Backslash |
| `\"` | Double quote |
| `\n` | Newline |
| `\r` | Carriage return |
| `\t` | Tab |
| `\u{XXXX}` | Unicode codepoint (v1.36.0, up to 6 hex digits) |
| `\` + newline | Line continuation (empty string) |

### Shell Expansion (x-prefix)

```just
# Compile-time expansion only (not runtime!)
home := x'~'                     # User's home directory
var := x'$HOME'                  # Value of HOME env var
var := x'${HOME}'                # Same thing
default := x'${VAR:-default}'    # With default value
```

---

## 5. Module System Deep Dive

### Module File Resolution

For `mod foo`, just searches (in order):
1. `foo.just`
2. `foo/mod.just`
3. `foo/justfile` (case-insensitive)
4. `foo/.justfile` (case-insensitive)

### Module Declaration Forms

```just
# Standard module
mod foo

# Optional module (no error if missing)
mod? foo

# Custom path
mod foo 'path/to/foo.just'
mod foo '~/global/foo.just'

# Optional with custom path
mod? foo 'path/to/optional.just'

# Documented module
# Database operations
[group('db')]
mod database
```

### Module Invocation

```just
# Space-separated
just foo bar          # Run bar in foo module

# Path syntax
just foo::bar         # Same thing

# From within justfile
main: foo::build
    just foo::deploy
```

### Module Behavior

- Recipes in different modules cannot share variables
- Each module uses its own settings
- `[no-cd]` recipes use invocation directory
- Other recipes use module's source directory
- `justfile()` and `justfile_directory()` return root justfile info
- `source_file()` and `source_directory()` return current module info

### Import vs Module

**Imports** merge recipes into current namespace:
```just
import 'shared.just'   # Recipes available directly
import? 'optional.just' # Optional import

# Recipe `build` from shared.just is called as:
default: build
```

**Modules** create namespaced subcommands:
```just
mod shared   # Creates namespace

# Recipe `build` in shared module is called as:
default: shared::build
```

---

## 6. Advanced Patterns

### Parallel Dependencies

```just
[parallel]
all: lint test build
    @echo "All tasks completed"

# Dependencies run concurrently
# Each still runs in its own process
```

### Subsequent Dependencies

```just
# a runs first, then b, then c and d in parallel after b
[parallel]
pipeline: a && b && c d
    @echo "Pipeline complete"
```

### Conditional Recipe Selection

```just
[linux]
install:
    apt install -y {{packages}}

[macos]
install:
    brew install {{packages}}

[windows]
install:
    choco install {{packages}}

# Just automatically picks the right one
```

### Dynamic Defaults

```just
target := env('TARGET', arch() + '-unknown-' + os())

build:
    cargo build --target {{target}}
```

### Required Tool Checking

```just
python := require('python3')
cargo := require('cargo')

setup:
    @echo "Python: {{python}}"
    @echo "Cargo: {{cargo}}"
```

### Graceful Degradation

```just
set unstable

prettier := which('prettier')

format:
    {{ if prettier != '' { 'prettier --write .' } else { 'echo "prettier not found"' } }}
```

### Validation Pattern

```just
deploy target:
    #!/usr/bin/env bash
    set -euo pipefail

    case "{{target}}" in
        staging|production) ;;
        *) echo "Invalid target: {{target}}"; exit 1 ;;
    esac

    kubectl config use-context {{target}}
    kubectl apply -f k8s/
```

### Using GNU Parallel

```just
[private]
parallel-tasks:
    #!/usr/bin/env -S parallel --shebang --ungroup --jobs {{ num_cpus() }}
    task1.sh
    task2.sh
    task3.sh
```

### Colored Output

```just
@success message:
    echo '{{GREEN}}{{BOLD}}SUCCESS:{{NORMAL}} {{message}}'

@warn message:
    echo '{{YELLOW}}{{BOLD}}WARNING:{{NORMAL}} {{message}}'

@error message:
    echo '{{RED}}{{BOLD}}ERROR:{{NORMAL}} {{message}}'
```

### Python with uv

```just
set unstable
set script-interpreter := ['uv', 'run', '--script']

[script]
analyze:
    # /// script
    # requires-python = ">=3.11"
    # dependencies = ["pandas", "matplotlib"]
    # ///
    import pandas as pd
    print("Analysis complete")
```

### Self-Documenting Justfile

```just
[default]
help:
    @just --list --list-heading $'Available commands:\n' --list-prefix '  '
```

---

## 7. Error Handling

### Ignore Errors

```just
clean:
    -rm -rf build/      # Continues even if fails
    -rm -rf dist/
    @echo "Cleanup attempted"
```

### Halt with Error

```just
target := if os() == "linux" {
    "x86_64-unknown-linux-gnu"
} else if os() == "macos" {
    "x86_64-apple-darwin"
} else {
    error("Unsupported OS: " + os())
}
```

### Suppress Exit Messages

```just
[no-exit-message]
git *args:
    @git {{args}}
```

### Bash Safety

```just
deploy:
    #!/usr/bin/env bash
    set -euo pipefail
    trap 'echo "Deployment failed"; cleanup' ERR

    # Your deployment logic
```

---

## 8. Command-Line Options

### Running Recipes

```bash
just                      # Run default recipe
just recipe               # Run named recipe
just recipe arg1 arg2     # With arguments
just var=value recipe     # Override variable
just --set var value recipe  # Alternative override
just mod::recipe          # Run module recipe
just mod recipe           # Same thing (space form)
```

### Listing and Inspection

```bash
just --list               # List available recipes
just --list --unsorted    # List in file order
just --list mod           # List recipes in module
just --list-heading ''    # Remove heading
just --list-prefix '- '   # Custom prefix

just --groups             # List recipe groups
just --summary            # Compact one-line list
just --show recipe        # Show recipe source
just --dump               # Dump parsed justfile
just --dump --format json # Dump as JSON (unstable)
just --evaluate           # Show variable values
just --variables          # List variable names
```

### File Selection

```bash
just -f path/justfile     # Use specific justfile
just --justfile path      # Same thing
just -d directory         # Set working directory
just --working-directory dir  # Same thing
```

### Execution Options

```bash
just -n, --dry-run        # Print commands without running
just -q, --quiet          # Suppress output
just -v, --verbose        # Extra output
just --yes                # Auto-confirm [confirm] recipes
just --highlight          # Syntax highlight output
just --no-highlight       # Disable highlighting
```

### Shell Configuration

```bash
just --shell bash         # Override shell
just --shell-arg '-c'     # Override shell argument
just --shell-command bash # Combined shell setting
```

### Formatting

```bash
just --fmt                # Format justfile
just --fmt --check        # Check formatting without changing
just --fmt --diff         # Show formatting diff
```

### Checking

```bash
just --check              # Verify syntax without running
just --unstable           # Enable unstable features
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `JUST_UNSTABLE` | Enable unstable features |
| `JUST_CHOOSER` | Interactive chooser command |

---

## Documentation Sources

All information from:
- https://just.systems/man/en/
- https://github.com/casey/just
- Just version: Latest as of documentation scrape

For the most current information, always check the official documentation.
