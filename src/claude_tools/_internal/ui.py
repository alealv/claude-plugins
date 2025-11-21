"""Terminal UI for interactive installation."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum

from claude_tools._internal.installer import ConfigType, ConfigItem


class Color:
    """ANSI color codes."""

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"
    CLEAR_LINE = "\033[2K"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"


class Focus(Enum):
    """UI focus states."""

    LIST = "list"
    CANCEL = "cancel"
    OK = "ok"


@dataclass
class UIState:
    """Tracks the state of the UI."""

    current_tab: int = 0
    current_row: int = 0
    scroll_offset: int = 0
    focus: Focus = Focus.LIST
    selected_items: dict[str, bool] = None

    def __post_init__(self) -> None:
        """Initialize selected_items if None."""
        if self.selected_items is None:
            self.selected_items = {}


class InstallUI:
    """Interactive terminal UI for installing Claude configurations."""

    TABS = [ConfigType.COMMANDS.value, ConfigType.SKILLS.value, ConfigType.AGENTS.value, ConfigType.HOOKS.value]
    MAX_DISPLAY_ROWS = 15

    def __init__(self, items_by_type: dict[ConfigType, list[ConfigItem]], target_project: str) -> None:
        """Initialize the UI.

        Args:
            items_by_type: Dictionary mapping config types to available items
            target_project: Path to target project
        """
        self.items_by_type = items_by_type
        self.target_project = target_project
        self.state = UIState()

    def get_current_items(self) -> list[ConfigItem]:
        """Get items for the current tab.

        Returns:
            List of items for current tab
        """
        config_type = ConfigType(self.TABS[self.state.current_tab])
        return self.items_by_type.get(config_type, [])

    def draw(self) -> None:
        """Draw the UI."""
        print(f"{Color.HIDE_CURSOR}", end="", flush=True)

        # Clear screen
        print("\033[2J\033[H", end="", flush=True)

        # Header
        print(f"{Color.BOLD}{Color.CYAN}═══════════════════════════════════════════════════════════════{Color.RESET}")
        print(f"{Color.BOLD}{Color.CYAN}    Claude Config Installer{Color.RESET}")
        print(f"{Color.BOLD}{Color.CYAN}═══════════════════════════════════════════════════════════════{Color.RESET}")
        print()
        print(f"{Color.DIM}Target: {Color.RESET}{self.target_project}")
        print()

        # Draw tabs
        print("  ", end="")
        for i, tab in enumerate(self.TABS):
            if i == self.state.current_tab:
                print(f"{Color.BOLD}{Color.BLUE}[ {tab.upper()} ]{Color.RESET} ", end="")
            else:
                print(f"{Color.DIM}[ {tab} ]{Color.RESET} ", end="")
        print()
        print()

        # Get items for current tab
        items = self.get_current_items()

        # Display items
        if not items:
            print(f"{Color.DIM}  No items available in this category{Color.RESET}")
            print()
        else:
            display_end = min(self.state.scroll_offset + self.MAX_DISPLAY_ROWS, len(items))

            for i in range(self.state.scroll_offset, display_end):
                item = items[i]
                key = f"{item.type.value}:{item.name}"
                checkbox = "[ ]"
                if self.state.selected_items.get(key):
                    checkbox = "[✓]"

                if i == self.state.current_row and self.state.focus == Focus.LIST:
                    print(f"  {Color.BOLD}{Color.GREEN}→ {checkbox} {item.name}{Color.RESET}")
                else:
                    print(f"    {checkbox} {item.name}")

            print()

            # Scroll indicator
            if len(items) > self.MAX_DISPLAY_ROWS:
                print(f"{Color.DIM}  Showing {self.state.scroll_offset + 1}-{display_end} of {len(items)}{Color.RESET}")
                print()

        # Spacing
        for _ in range(3):
            print()

        # Draw buttons
        print("  ", end="")
        if self.state.focus == Focus.CANCEL:
            print(f"{Color.BOLD}{Color.RED}[ Cancel ]{Color.RESET}  ", end="")
        else:
            print(f"{Color.DIM}[ Cancel ]{Color.RESET}  ", end="")

        if self.state.focus == Focus.OK:
            print(f"{Color.BOLD}{Color.GREEN}[ OK ]{Color.RESET}")
        else:
            print(f"{Color.DIM}[ OK ]{Color.RESET}")
        print()
        print()

        # Help text
        print(f"{Color.DIM}  ↑/↓: Navigate  Space: Select  Tab: Switch tabs  Enter: Confirm  Esc: Cancel{Color.RESET}")

    def handle_up(self) -> None:
        """Handle up arrow key."""
        items = self.get_current_items()
        if self.state.focus == Focus.LIST and items:
            self.state.current_row = (self.state.current_row - 1) % len(items)
            if self.state.current_row < self.state.scroll_offset:
                self.state.scroll_offset = self.state.current_row
        else:
            self.state.focus = Focus.LIST
            if items:
                self.state.current_row = len(items) - 1
                self.state.scroll_offset = max(0, len(items) - self.MAX_DISPLAY_ROWS)
            else:
                self.state.current_row = 0

    def handle_down(self) -> None:
        """Handle down arrow key."""
        items = self.get_current_items()
        if self.state.focus == Focus.LIST:
            if items:
                self.state.current_row = (self.state.current_row + 1) % len(items)
                if self.state.current_row >= self.state.scroll_offset + self.MAX_DISPLAY_ROWS:
                    self.state.scroll_offset = self.state.current_row - self.MAX_DISPLAY_ROWS + 1
            else:
                self.state.focus = Focus.CANCEL
        elif self.state.focus == Focus.CANCEL:
            pass  # Can't go down from cancel
        elif self.state.focus == Focus.OK:
            pass  # Can't go down from ok

    def handle_left(self) -> None:
        """Handle left arrow key."""
        if self.state.focus == Focus.OK:
            self.state.focus = Focus.CANCEL

    def handle_right(self) -> None:
        """Handle right arrow key."""
        if self.state.focus == Focus.CANCEL:
            self.state.focus = Focus.OK

    def handle_space(self) -> None:
        """Handle space key for selection."""
        if self.state.focus == Focus.LIST:
            items = self.get_current_items()
            if items and self.state.current_row < len(items):
                item = items[self.state.current_row]
                key = f"{item.type.value}:{item.name}"
                self.state.selected_items[key] = not self.state.selected_items.get(key, False)

    def handle_tab(self) -> None:
        """Handle tab key for tab switching."""
        self.state.current_tab = (self.state.current_tab + 1) % len(self.TABS)
        self.state.current_row = 0
        self.state.scroll_offset = 0
        self.state.focus = Focus.LIST

    def get_selected_items(self) -> list[ConfigItem]:
        """Get all selected items.

        Returns:
            List of selected configuration items
        """
        selected = []
        for config_type in ConfigType:
            items = self.items_by_type.get(config_type, [])
            for item in items:
                key = f"{item.type.value}:{item.name}"
                if self.state.selected_items.get(key):
                    selected.append(item)
        return selected
