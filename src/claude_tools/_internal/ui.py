"""Terminal UI for interactive installation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from rich.console import Console, Group
from rich.text import Text
from rich.panel import Panel

from claude_tools._internal.installer import ConfigType, ConfigItem, InstallStatus

# Create console with proper terminal detection
console = Console(
    color_system="truecolor",
    legacy_windows=False,
)


class Focus(Enum):
    """UI focus states."""

    LIST = "list"
    CANCEL = "cancel"
    OK = "ok"


class ItemAction(Enum):
    """User action for an item."""

    NONE = "none"  # No action (keep as-is or skip)
    INSTALL = "install"  # Install or update
    UNINSTALL = "uninstall"  # Remove


@dataclass
class UIState:
    """Tracks the state of the UI."""

    current_tab: int = 0
    current_row: int = 0
    scroll_offset: int = 0
    focus: Focus = Focus.LIST
    item_actions: dict[str, ItemAction] = field(default_factory=dict)


class InstallUI:
    """Interactive terminal UI for installing Claude configurations."""

    TABS = [
        ConfigType.COMMANDS.value,
        ConfigType.SKILLS.value,
        ConfigType.AGENTS.value,
        ConfigType.HOOKS.value,
    ]
    MAX_DISPLAY_ROWS = 15

    def __init__(
        self, items_by_type: dict[ConfigType, list[ConfigItem]], target_project: str
    ) -> None:
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

    def render(self, console_width: int | None = None) -> Group:
        """Render the UI as a Group.

        Args:
            console_width: Optional console width for constraining panels

        Returns:
            A Rich Group containing all UI elements
        """
        renderables = []

        # Header
        header_text = Text(
            "Claude Config Installer", justify="center", style="bold cyan"
        )
        header = Panel(
            header_text,
            border_style="cyan",
            width=console_width,
        )
        renderables.append(header)
        renderables.append(Text())

        # Target path
        target_text = Text()
        target_text.append("  Target: ", style="dim")
        target_text.append(self.target_project)
        renderables.append(target_text)
        renderables.append(Text())

        # Build tab title for panel - rectangles around each tab
        tab_title = ""
        for i, tab in enumerate(self.TABS):
            if i > 0:
                tab_title += "[dim] ─── [/dim]"
            if i == self.state.current_tab:
                # Active tab - cyan and bold
                tab_title += f"[bold cyan]\\[{tab.upper()}][/bold cyan]"
            else:
                # Inactive tab - dim
                tab_title += f"[dim]\\[{tab}][/dim]"

        # Items in a panel with tabs in title
        items = self.get_current_items()
        items_renderables = []

        if not items:
            items_renderables.append(
                Text(
                    "No items available in this category", style="dim", justify="center"
                )
            )
        else:
            display_end = min(
                self.state.scroll_offset + self.MAX_DISPLAY_ROWS, len(items)
            )

            for i in range(self.state.scroll_offset, display_end):
                item = items[i]
                key = f"{item.type.value}:{item.name}"
                action = self.state.item_actions.get(key, ItemAction.NONE)

                # Determine checkbox symbol and suffix based on install status and action
                if item.install_status == InstallStatus.NOT_INSTALLED:
                    checkbox = "[✓]" if action == ItemAction.INSTALL else "[ ]"
                    suffix = ""
                elif item.install_status == InstallStatus.INSTALLED_CURRENT:
                    checkbox = "[ ]" if action == ItemAction.UNINSTALL else "[✓]"
                    suffix = " (installed)"
                else:  # INSTALLED_OUTDATED
                    checkbox = "[✓]" if action == ItemAction.INSTALL else "[✗]"
                    suffix = " (outdated)"

                display_text = f"{checkbox} {item.name}{suffix}"

                if i == self.state.current_row and self.state.focus == Focus.LIST:
                    items_renderables.append(
                        Text(f"> {display_text}", style="bold green")
                    )
                else:
                    items_renderables.append(Text(f"  {display_text}"))

            # Scroll indicator
            if len(items) > self.MAX_DISPLAY_ROWS:
                items_renderables.append(Text())
                items_renderables.append(
                    Text(
                        f"Showing {self.state.scroll_offset + 1}-{display_end} of {len(items)}",
                        style="dim",
                        justify="center",
                    )
                )

        items_panel = Panel(
            Group(*items_renderables) if items_renderables else Text(""),
            border_style="blue",
            title=tab_title,
            title_align="left",
            height=self.MAX_DISPLAY_ROWS + 4,
            width=console_width,
        )
        renderables.append(items_panel)
        renderables.append(Text())

        # Buttons
        buttons = Text(justify="center")
        if self.state.focus == Focus.CANCEL:
            buttons.append("[ Cancel ]", style="bold red")
        else:
            buttons.append("[ Cancel ]", style="dim")
        buttons.append("  ")
        if self.state.focus == Focus.OK:
            buttons.append("[ OK ]", style="bold green")
        else:
            buttons.append("[ OK ]", style="dim")
        renderables.append(buttons)
        renderables.append(Text())

        # Help text
        help_text = Text(style="dim", justify="center")
        help_text.append("↑↓/jk: Navigate  ")
        help_text.append("←→/hl: Switch tabs  ")
        help_text.append("Space/x: Select  ")
        help_text.append("Tab: Change focus  ")
        help_text.append("Enter: Confirm  ")
        help_text.append("Esc/q: Cancel")
        renderables.append(help_text)

        return Group(*renderables)

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
                if (
                    self.state.current_row
                    >= self.state.scroll_offset + self.MAX_DISPLAY_ROWS
                ):
                    self.state.scroll_offset = (
                        self.state.current_row - self.MAX_DISPLAY_ROWS + 1
                    )
            else:
                self.state.focus = Focus.CANCEL
        elif self.state.focus == Focus.CANCEL:
            pass  # Can't go down from cancel
        elif self.state.focus == Focus.OK:
            pass  # Can't go down from ok

    def handle_left(self) -> None:
        """Handle left arrow key."""
        if self.state.focus == Focus.LIST:
            # Switch to previous tab
            self.state.current_tab = (self.state.current_tab - 1) % len(self.TABS)
            self.state.current_row = 0
            self.state.scroll_offset = 0
        elif self.state.focus == Focus.OK:
            self.state.focus = Focus.CANCEL

    def handle_right(self) -> None:
        """Handle right arrow key."""
        if self.state.focus == Focus.LIST:
            # Switch to next tab
            self.state.current_tab = (self.state.current_tab + 1) % len(self.TABS)
            self.state.current_row = 0
            self.state.scroll_offset = 0
        elif self.state.focus == Focus.CANCEL:
            self.state.focus = Focus.OK

    def handle_space(self) -> None:
        """Handle space key for selection.

        Cycles through actions based on install status:
        - NOT_INSTALLED: NONE → INSTALL → NONE
        - INSTALLED_CURRENT: NONE → UNINSTALL → NONE
        - INSTALLED_OUTDATED: NONE → INSTALL → NONE
        """
        if self.state.focus == Focus.LIST:
            items = self.get_current_items()
            if items and self.state.current_row < len(items):
                item = items[self.state.current_row]
                key = f"{item.type.value}:{item.name}"
                current_action = self.state.item_actions.get(key, ItemAction.NONE)

                if item.install_status == InstallStatus.NOT_INSTALLED:
                    # Cycle: NONE → INSTALL → NONE
                    new_action = (
                        ItemAction.INSTALL
                        if current_action == ItemAction.NONE
                        else ItemAction.NONE
                    )
                elif item.install_status == InstallStatus.INSTALLED_CURRENT:
                    # Cycle: NONE → UNINSTALL → NONE (default is NONE = keep)
                    new_action = (
                        ItemAction.UNINSTALL
                        if current_action == ItemAction.NONE
                        else ItemAction.NONE
                    )
                else:  # INSTALLED_OUTDATED
                    # Cycle: NONE → INSTALL → NONE (NONE = keep outdated)
                    new_action = (
                        ItemAction.INSTALL
                        if current_action == ItemAction.NONE
                        else ItemAction.NONE
                    )

                self.state.item_actions[key] = new_action

    def handle_tab(self) -> None:
        """Handle tab key for focus navigation."""
        if self.state.focus == Focus.LIST:
            self.state.focus = Focus.CANCEL
        elif self.state.focus == Focus.CANCEL:
            self.state.focus = Focus.OK
        elif self.state.focus == Focus.OK:
            self.state.focus = Focus.LIST

    def get_items_to_install(self) -> list[ConfigItem]:
        """Get items that should be installed or updated.

        Returns:
            List of items with INSTALL action
        """
        items_to_install = []
        for config_type in ConfigType:
            items = self.items_by_type.get(config_type, [])
            for item in items:
                key = f"{item.type.value}:{item.name}"
                if self.state.item_actions.get(key) == ItemAction.INSTALL:
                    items_to_install.append(item)
        return items_to_install

    def get_items_to_uninstall(self) -> list[ConfigItem]:
        """Get items that should be uninstalled.

        Returns:
            List of items with UNINSTALL action
        """
        items_to_uninstall = []
        for config_type in ConfigType:
            items = self.items_by_type.get(config_type, [])
            for item in items:
                key = f"{item.type.value}:{item.name}"
                if self.state.item_actions.get(key) == ItemAction.UNINSTALL:
                    items_to_uninstall.append(item)
        return items_to_uninstall

    def get_selected_items(self) -> list[ConfigItem]:
        """Get all selected items (for backward compatibility).

        Returns:
            List of items to install (same as get_items_to_install)
        """
        return self.get_items_to_install()
