# Claude Tools Architecture

## Overview

Claude Tools is a Python-based installer for Claude Code configurations (commands, skills, agents, and hooks).

## Module Structure

### Core Modules

```
src/claude_tools/
├── __init__.py              # Package entry point
├── __main__.py              # CLI entry point for `python -m claude_tools`
└── _internal/
    ├── cli.py               # Command-line interface
    ├── installer.py         # Core installation logic
    ├── ui.py                # Interactive terminal UI
    ├── debug.py             # Debug utilities
    └── __init__.py          # Internal package marker
```

## Module Descriptions

### cli.py

Handles command-line argument parsing and orchestrates the installation flow.

**Key Components:**
- `get_parser()` - Creates ArgumentParser for CLI arguments
- `run_interactive_installer()` - Manages the interactive UI loop
- `main()` - Entry point for the application

**Responsibilities:**
- Parse command-line arguments
- Validate user input
- Coordinate installer and UI modules
- Handle terminal setup/teardown

### installer.py

Core installation logic for copying configurations into projects.

**Key Classes:**
- `ConfigType` - Enum for configuration types (COMMANDS, SKILLS, AGENTS, HOOKS)
- `ConfigItem` - Data class representing a single configuration item
- `Installer` - Main installer class

**Installer Responsibilities:**
- Validate file paths
- Discover available configurations
- Copy configurations to target projects
- Merge hook settings into `.claude/settings.json`

**Key Methods:**
- `validate_paths()` - Check source and target paths
- `get_available_items(config_type)` - List available items by type
- `install_item(item)` - Install a single item
- `install_items(items)` - Install multiple items
- `merge_hook_settings(hook_items)` - Merge hook configurations

### ui.py

Interactive terminal user interface for selecting and installing configurations.

**Key Classes:**
- `Color` - ANSI color code constants
- `Focus` - Enum for UI focus states (LIST, CANCEL, OK)
- `UIState` - Data class tracking UI state
- `InstallUI` - Main UI class

**UI Features:**
- Tabbed interface for different configuration types
- Arrow key navigation
- Checkbox selection with space
- OK/Cancel buttons with keyboard navigation
- Live item filtering based on current tab

**Key Methods:**
- `draw()` - Render the complete UI
- `get_current_items()` - Get items for active tab
- `handle_up/down/left/right()` - Handle arrow keys
- `handle_space()` - Handle item selection
- `handle_tab()` - Handle tab switching
- `get_selected_items()` - Get all selected items

## Data Flow

```
User Input
    ↓
CLI Argument Parser
    ↓
Installer (validate paths)
    ↓
Get Available Items
    ↓
Interactive UI Loop
    ↓
User Selections
    ↓
Install Selected Items
    ↓
Merge Hook Settings
    ↓
Summary and Exit
```

## Configuration Item Discovery

### Commands
- **Location**: `commands/` directory
- **Format**: Markdown files (*.md)
- **Naming**: `command-name.md`
- **Installation**: Copy to `.claude/commands/`

### Skills
- **Location**: `skills/` directory
- **Format**: Directories with `SKILL.md`
- **Naming**: `skill-name/` directory
- **Installation**: Copy to `.claude/skills/`

### Agents
- **Location**: `agents/` directory
- **Format**: Directories with configuration
- **Naming**: `agent-name/` directory
- **Installation**: Copy to `.claude/agents/`

### Hooks
- **Location**: `hooks/` directory
- **Format**: Directories with `hook-name.sh` and `settings.json`
- **Naming**: `hook-name/` directory
- **Installation**: Copy to `.claude/hooks/` + merge settings

## Hook Settings Merge

When hooks are installed:

1. Copy hook directory to `.claude/hooks/hook-name/`
2. Read `hook-name/settings.json` if it exists
3. Load existing `.claude/settings.json` or create new
4. Merge hook configurations into the `hooks` section
5. Preserve existing hooks while adding new ones

**Merge Strategy:**
- Per-event merging (PreToolUse, PostToolUse, etc.)
- Append new handlers if not already present
- Preserve existing event handlers

Example merge result:
```json
{
  "hooks": {
    "Stop": [
      { "auto-commit hook handler" },
      { "your existing handler" }
    ]
  }
}
```

## Terminal UI Interaction

### Key Bindings

| Key | Action |
|-----|--------|
| `↑`/`↓` | Navigate items in list |
| `←`/`→` | Navigate between buttons |
| `Tab` | Switch to next tab |
| `Space` | Toggle item selection |
| `Enter` | Confirm if on OK button |
| `Esc`/`q` | Cancel |

### UI States

```
┌─────────────────────────────┐
│    Tab Selection (Focus)    │
├─────────────────────────────┤
│ [COMMANDS] [skills] [agents]│  ← Current tab highlighted
└─────────────────────────────┘
         ↓
┌─────────────────────────────┐
│  Item Selection (Focus)     │
├─────────────────────────────┤
│ → [✓] selected-item         │  ← Can navigate and select
│   [ ] unselected-item       │
└─────────────────────────────┘
         ↓
┌─────────────────────────────┐
│  Button Selection (Focus)   │
├─────────────────────────────┤
│ [ Cancel ]  [ OK ]          │  ← Navigate with arrows
└─────────────────────────────┘
```

## Error Handling

### Path Validation
- Checks if repo root exists
- Checks if target project exists
- Validates that target is a directory

### Installation Errors
- Returns (successful, failed) count
- Prints error messages to stderr
- Continues with other items on failure

### Settings Merge Errors
- Validates JSON syntax before merge
- Reports parsing errors
- Preserves existing settings on error

## Extension Points

### Adding New Configuration Types

1. Add type to `ConfigType` enum in `installer.py`
2. Implement discovery in `Installer.get_available_items()`
3. Add tab in `InstallUI.TABS`
4. Handle installation in `main()` if special logic needed

### Customizing Installation

Subclass `Installer` and override:
- `get_available_items()` - Custom discovery logic
- `install_item()` - Custom installation logic
- `merge_hook_settings()` - Custom settings merge

### Customizing UI

Subclass `InstallUI` and override:
- `draw()` - Custom rendering
- `handle_*()` - Custom keyboard handling
- `get_selected_items()` - Custom filtering

## Performance Considerations

- **Path validation** - O(1) filesystem checks
- **Item discovery** - O(n) directory listing
- **Installation** - O(n*m) where n=items, m=avg item size
- **UI rendering** - O(k) where k=visible items (constant)

For large numbers of items:
- Discovery is still fast (< 1s typical)
- Installation is I/O bound (depends on item sizes)
- UI remains responsive (only displays ~15 items)

## Testing Strategy

### Unit Tests (Planned)
- Installer path validation
- Configuration item discovery
- Hook settings merge logic
- UI state transitions

### Integration Tests (Planned)
- Full installation workflow
- Terminal interaction
- File copying
- Settings merge

### Manual Testing Checklist
- [ ] Run with valid project path
- [ ] Run without path (prompt)
- [ ] Navigate all tabs
- [ ] Select/deselect items
- [ ] Cancel installation
- [ ] Complete installation
- [ ] Verify files copied correctly
- [ ] Verify hook settings merged

## Security Considerations

1. **Path Traversal** - Use `Path` class which normalizes paths
2. **File Permissions** - Preserves source file permissions
3. **JSON Injection** - Validates JSON before merging
4. **Command Injection** - No shell commands executed

## Future Enhancements

- [ ] Non-interactive mode for CI/CD
- [ ] Config file support for default selections
- [ ] Uninstall functionality
- [ ] Update existing installations
- [ ] Dry-run mode
- [ ] Parallel installation
- [ ] Custom repository support
- [ ] Plugin system for custom installers
