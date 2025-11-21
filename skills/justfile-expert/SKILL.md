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
set shell := ["bash", "-c"]
set dotenv-load := true

# Default recipe (first one runs when no recipe specified)
default:
    @just --list

# Grouped recipes (modern approach - always use groups)
# Build the project
[group: 'build']
build:
    cargo build --release

# Run tests
[group: 'test']
test:
    cargo test
```

**Critical syntax rules:**
1. Comments describing recipes go BEFORE `[group: ]` attributes
2. Recipe name must immediately follow the group attribute
3. Use `[group: 'name']` syntax (colon, not parentheses)

## Recipe Groups

Always organize recipes into groups for discoverability:

```just
# Install dependencies
[group: 'setup']
install:
    npm install

# Format code
[group: 'quality']
fmt:
    prettier --write .

# Run all tests
[group: 'test']
test:
    npm test
```

Common group names: `setup`, `build`, `test`, `quality`, `docs`, `release`, `dev`, `clean`, `info`

### Multi-Group Recipes

Recipes can belong to multiple groups:

```just
# Run quality checks and tests
[group: 'quality']
[group: 'ci']
check: lint test types
```

## Common Patterns

### Subcommand Pattern

For recipes with multiple operations:

```just
# Build operations (default: all, options: wheel, sdist)
[group: 'build']
build OPERATION="":
    bash -c 'case "{{ OPERATION }}" in \
      "") python -m build; ;; \
      wheel) python -m build --wheel; ;; \
      sdist) python -m build --sdist; ;; \
      *) echo "Unknown: {{ OPERATION }}"; exit 1; ;; \
    esac'
```

Usage: `just build`, `just build wheel`, `just build sdist`

### Parameters with Defaults

```just
# Run tests with optional filter
[group: 'test']
test FILTER="":
    pytest {{ if FILTER != "" { "-k " + FILTER } else { "" } }}

# Run specific test file
[group: 'test']
test-file FILE:
    pytest {{ FILE }}
```

### Recipe Dependencies

```just
[group: 'build']
build: install
    cargo build

[group: 'setup']
install:
    cargo fetch
```

Dependencies run first automatically.

## Attributes

### Private Recipes

Hide helper recipes from `--list`:

```just
[private]
internal-helper:
    echo "hidden from users"
```

### Confirmation

Require confirmation before running:

```just
[confirm]
[group: 'deploy']
deploy-prod:
    kubectl apply -f production/
```

### Documentation

Add doc strings (alternative to comments):

```just
[doc('Run all quality checks')]
[group: 'quality']
quality: lint test types
```

### Platform-Specific

```just
[linux]
[group: 'build']
build-linux:
    cargo build --target x86_64-unknown-linux-gnu

[macos]
[group: 'build']
build-mac:
    cargo build --target aarch64-apple-darwin
```

## Settings

Configure justfile behavior at the top:

```just
# Use bash for all commands
set shell := ["bash", "-c"]

# Load .env file
set dotenv-load := true

# Allow duplicate recipe names (avoid if possible)
set allow-duplicate-recipes := false

# Set working directory
set working-directory := "subdir"
```

## Common Mistakes

### MISTAKE 1: Comment After Group Attribute

**WRONG - Causes "Extraneous attribute" error:**
```just
[group: 'setup']
# Install dependencies
install:
    npm install
```

**CORRECT:**
```just
# Install dependencies
[group: 'setup']
install:
    npm install
```

### MISTAKE 2: Old Attribute Syntax

**WRONG:**
```just
[group('setup')]  # Parentheses don't work
```

**CORRECT:**
```just
[group: 'setup']  # Use colon
```

### MISTAKE 3: Separator Comments

**WRONG - Breaks group parsing:**
```just
default:
    @just --list

# ================================
# SETUP SECTION
# ================================

[group: 'setup']  # Error!
install:
    npm install
```

**CORRECT:**
```just
default:
    @just --list

# Install dependencies
[group: 'setup']
install:
    npm install
```

### MISTAKE 4: Not Using @ for Quiet Output

Commands echo by default. Use `@` to suppress:

```just
# Show version
[group: 'info']
version:
    @echo "v1.0.0"  # Only prints version, not command
```

### MISTAKE 5: Shell Variables vs Just Variables

```just
# Just variable (use {{ }})
version := "1.0.0"

[group: 'info']
show-version:
    @echo {{ version }}  # CORRECT

# Shell variable (use $)
[group: 'info']
show-home:
    @echo $HOME  # CORRECT for shell vars
```

## Cross-Platform Patterns

Use Just functions for portability:

```just
# Cross-platform home directory
[group: 'info']
show-home:
    @echo {{ home_directory() }}

# Cross-platform path joining
[group: 'build']
build:
    @echo {{ join(justfile_directory(), "dist") }}
```

Common functions: `home_directory()`, `justfile_directory()`, `env_var("VAR")`, `os()`, `arch()`

## Troubleshooting

### "Extraneous attribute" Error

**Cause:** Comment between `[group: ]` and recipe name

**Fix:** Move comment before the group attribute:
```just
# Comment here
[group: 'name']
recipe:
    command
```

### Recipe Not in --list

**Causes:**
- Marked `[private]`
- Syntax error preventing parsing
- File not saved

**Check:** Run `just --dump` to see parsed justfile

### Variable Not Expanding

**Wrong:** `$variable` (shell syntax)
**Right:** `{{ variable }}` (Just syntax)

Just variables use `{{ }}`, shell variables use `$`

## Resources

### references/

See **references/just-docs.md** for comprehensive Just documentation including:
- Complete function reference
- All available attributes
- Advanced patterns (conditionals, loops, error handling)
- Module system
- Remote justfiles

Load when you need detailed reference information beyond quick patterns.

### Documentation Links

- Official manual: https://just.systems/man/en/
- GitHub: https://github.com/casey/just
- Local docs: /tmp/just-systems/just.systems/man/en/

Key pages:
- Groups: https://just.systems/man/en/groups.html
- Attributes: https://just.systems/man/en/attributes.html
- Functions: https://just.systems/man/en/functions.html
- Settings: https://just.systems/man/en/settings.html
