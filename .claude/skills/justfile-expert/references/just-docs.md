# Just Comprehensive Reference

This file contains detailed reference information for advanced Just features. Load this when you need information beyond the common patterns in SKILL.md.

## Table of Contents

1. Functions Reference
2. All Attributes
3. Advanced Patterns
4. Module System
5. Remote Justfiles
6. Error Handling

## 1. Functions Reference

### String Functions
- `lowercase(s)` - Convert to lowercase
- `uppercase(s)` - Convert to uppercase
- `trim(s)` - Remove whitespace
- `trim_start(s)` - Remove leading whitespace
- `trim_end(s)` - Remove trailing whitespace
- `replace(s, from, to)` - Replace all occurrences

### Path Functions
- `justfile_directory()` - Directory containing justfile
- `justfile()` - Path to justfile
- `home_directory()` - User home directory
- `join(a, b, ...)` - Join path components
- `absolute_path(path)` - Convert to absolute path
- `parent_directory(path)` - Parent directory
- `file_name(path)` - File name without directory
- `extension(path)` - File extension
- `without_extension(path)` - Path without extension

### Environment Functions
- `env_var(key)` - Get environment variable (fails if not set)
- `env_var_or_default(key, default)` - Get env var with default
- `env(key, default)` - Deprecated, use env_var_or_default

### System Functions
- `os()` - Operating system name
- `os_family()` - OS family (unix, windows)
- `arch()` - Architecture (x86_64, aarch64, etc.)
- `num_cpus()` - Number of CPU cores

### Execution Functions
- `shell(command, args...)` - Execute command, return output
- `just_executable()` - Path to just binary
- `just_pid()` - Process ID of just

### Utility Functions
- `uuid()` - Generate UUID
- `datetime()` - Current datetime
- `datetime_utc()` - Current UTC datetime
- `sha256(string)` - SHA-256 hash
- `sha256_file(path)` - SHA-256 hash of file

## 2. All Attributes

### Recipe Attributes

`[group: 'name']` - Organize into group
`[private]` - Hide from --list
`[confirm]` - Require confirmation
`[confirm(prompt)]` - Custom confirmation prompt
`[doc(text)]` - Documentation string
`[linux]` - Run only on Linux
`[macos]` - Run only on macOS
`[windows]` - Run only on Windows
`[unix]` - Run only on Unix-like systems
`[no-cd]` - Don't change to recipe directory
`[no-exit-message]` - Suppress error messages
`[extension(ext)]` - Shebang recipe file extension
`[macos]`, `[linux]`, `[unix]`, `[windows]` - Platform-specific

### Module Attributes

`[private]` - Make module private
`[group: 'name']` - Assign module to group

## 3. Advanced Patterns

### Conditionals

```just
# Conditional execution
test:
    {{ if os() == "linux" { "echo Linux" } else { "echo Other" } }}

# Multiple conditions
build:
    {{ if os() == "macos" && arch() == "aarch64" { \
        "cargo build --target aarch64-apple-darwin" \
    } else { \
        "cargo build" \
    } }}
```

### Loops (using shell)

```just
# Process multiple files
process-all:
    #!/usr/bin/env bash
    for file in src/*.rs; do
        echo "Processing $file"
        rustfmt "$file"
    done
```

### Error Handling

```just
# Continue on error
build:
    -cargo build  # - prefix ignores errors

# Custom error handling
deploy:
    #!/usr/bin/env bash
    set -euo pipefail  # Exit on error
    echo "Deploying..."
    kubectl apply -f config.yaml || {
        echo "Deployment failed!"
        exit 1
    }
```

### String Interpolation

```just
version := "1.0.0"
target := "x86_64-unknown-linux-gnu"

# Variable interpolation
build:
    cargo build --release --target {{ target }}
    echo "Built version {{ version }}"

# Expression interpolation
info:
    @echo "Running on {{ os() }} {{ arch() }}"
    @echo "Home: {{ home_directory() }}"
```

### Shebang Recipes

```just
# Python recipe
[private]
py-script:
    #!/usr/bin/env python3
    import sys
    print(f"Python {sys.version}")

# Bash script
[private]
bash-script:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Complex bash script here"
```

## 4. Module System

### Creating Modules

```just
# main justfile
mod utils
mod build

default:
    @just utils::hello
```

```just
# utils/mod.just
hello:
    @echo "Hello from utils module"

[private]
internal:
    @echo "Private to module"
```

### Module Imports

```just
# Import specific recipe
import 'utils/mod.just' as utils

default:
    @just utils::hello
```

### Module Groups

```just
# Assign module to group
[group: 'dev']
mod tools
```

## 5. Remote Justfiles

### Running Remote Recipes

```just
# Execute from URL
default:
    just --justfile https://example.com/justfile recipe-name

# Execute from GitHub
ci:
    just --justfile https://raw.githubusercontent.com/user/repo/main/justfile test
```

### Including Remote Content

Not directly supported - download first:

```just
fetch-remote:
    curl -o remote.just https://example.com/justfile

run-remote: fetch-remote
    just --justfile remote.just task
```

## 6. Error Handling Patterns

### Graceful Degradation

```just
# Optional tool usage
format:
    @{{ if `which prettier` =~ ".+" { \
        "prettier --write ." \
    } else { \
        "echo 'prettier not found, skipping format'" \
    } }}
```

### Validation

```just
# Validate before running
deploy target:
    @[ "{{ target }}" = "staging" ] || [ "{{ target }}" = "production" ] || \
        (echo "Invalid target: {{ target }}"; exit 1)
    kubectl apply -f {{ target }}/

# File existence check
process file:
    @test -f "{{ file }}" || (echo "File not found: {{ file }}"; exit 1)
    ./process.sh "{{ file }}"
```

### Cleanup on Failure

```just
# Always cleanup
deploy:
    #!/usr/bin/env bash
    set -euo pipefail
    trap 'rm -f /tmp/deploy.lock' EXIT

    touch /tmp/deploy.lock
    kubectl apply -f deployment.yaml
```

## Advanced Settings

```just
# Export all variables as environment variables
set export

# Positional arguments
set positional-arguments

# Fallback recipe (runs if recipe not found)
set fallback

# Shell with custom environment
set shell := ["bash", "-cu"]

# Allow .env override
set dotenv-load := true
set dotenv-filename := ".env.local"

# Windows-specific settings
set windows-powershell
set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]
```

## Documentation Sources

All information derived from:
- https://just.systems/man/en/
- https://github.com/casey/just
- /tmp/just-systems/just.systems/man/en/

For the most current information, always check the official documentation.
