"""Terminal UI for interactive installation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from rich.console import Console, Group
from rich.text import Text
from rich.panel import Panel

from claude_tools._internal.installer import ConfigType, ConfigItem

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


@dataclass
class UIState:
    """Tracks the state of the UI."""

    current_tab: int = 0
    current_row: int = 0
    scroll_offset: int = 0
    focus: Focus = Focus.LIST
    selected_items: dict[str, bool] = field(default_factory=dict)


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
        header_text = Text("Claude Config Installer", justify="center", style="bold cyan")
        panel_kwargs = {"border_style": "cyan"}
        if console_width:
            panel_kwargs["width"] = console_width
        header = Panel(header_text, **panel_kwargs)
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
                tab_title += f"[bold cyan]\[{tab.upper()}][/bold cyan]"
            else:
                # Inactive tab - dim
                tab_title += f"[dim]\[{tab}][/dim]"

        # Items in a panel with tabs in title
        items = self.get_current_items()
        items_renderables = []

        if not items:
            items_renderables.append(Text("No items available in this category", style="dim", justify="center"))
        else:
            display_end = min(
                self.state.scroll_offset + self.MAX_DISPLAY_ROWS, len(items)
            )

            for i in range(self.state.scroll_offset, display_end):
                item = items[i]
                key = f"{item.type.value}:{item.name}"
                checkbox = "[ ]" if not self.state.selected_items.get(key) else "[X]"

                if i == self.state.current_row and self.state.focus == Focus.LIST:
                    items_renderables.append(Text(f"> {checkbox} {item.name}", style="bold green"))
                else:
                    items_renderables.append(Text(f"  {checkbox} {item.name}"))

            # Scroll indicator
            if len(items) > self.MAX_DISPLAY_ROWS:
                items_renderables.append(Text())
                items_renderables.append(
                    Text(
                        f"Showing {self.state.scroll_offset + 1}-{display_end} of {len(items)}",
                        style="dim",
                        justify="center"
                    )
                )

        items_panel_kwargs = {
            "border_style": "blue",
            "title": tab_title,
            "title_align": "left",
            "height": self.MAX_DISPLAY_ROWS + 4,
        }
        if console_width:
            items_panel_kwargs["width"] = console_width
        items_panel = Panel(
            Group(*items_renderables) if items_renderables else Text(""),
            **items_panel_kwargs,
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
        """Handle space key for selection."""
        if self.state.focus == Focus.LIST:
            items = self.get_current_items()
            if items and self.state.current_row < len(items):
                item = items[self.state.current_row]
                key = f"{item.type.value}:{item.name}"
                self.state.selected_items[key] = not self.state.selected_items.get(
                    key, False
                )

    def handle_tab(self) -> None:
        """Handle tab key for focus navigation."""
        if self.state.focus == Focus.LIST:
            self.state.focus = Focus.CANCEL
        elif self.state.focus == Focus.CANCEL:
            self.state.focus = Focus.OK
        elif self.state.focus == Focus.OK:
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
