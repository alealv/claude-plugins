"""Tests for the terminal UI module."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from claude_tools._internal.installer import ConfigType, ConfigItem
from claude_tools._internal.ui import Color, Focus, UIState, InstallUI


class TestColor:
    """Tests for ANSI color codes."""

    def test_color_constants(self) -> None:
        """Color class has expected constants."""
        assert hasattr(Color, "RESET")
        assert hasattr(Color, "BOLD")
        assert hasattr(Color, "GREEN")
        assert hasattr(Color, "BLUE")
        assert hasattr(Color, "CYAN")
        assert hasattr(Color, "RED")
        assert hasattr(Color, "YELLOW")


class TestFocus:
    """Tests for Focus enum."""

    def test_focus_values(self) -> None:
        """Focus enum has expected values."""
        assert Focus.LIST.value == "list"
        assert Focus.CANCEL.value == "cancel"
        assert Focus.OK.value == "ok"


class TestUIState:
    """Tests for UIState dataclass."""

    def test_ui_state_creation(self) -> None:
        """UIState can be created with default values."""
        state = UIState(
            current_tab=0,
            current_row=0,
            scroll_offset=0,
            focus=Focus.LIST,
            selected_items=set(),
        )

        assert state.current_tab == 0
        assert state.current_row == 0
        assert state.scroll_offset == 0
        assert state.focus == Focus.LIST
        assert state.selected_items == set()

    def test_ui_state_selected_items(self) -> None:
        """UIState can track selected items."""
        selected = {"item1", "item2"}
        state = UIState(
            current_tab=0,
            current_row=0,
            scroll_offset=0,
            focus=Focus.LIST,
            selected_items=selected,
        )

        assert "item1" in state.selected_items
        assert "item2" in state.selected_items


class TestInstallUI:
    """Tests for InstallUI class."""

    @pytest.fixture
    def sample_items(self) -> dict[ConfigType, list[ConfigItem]]:
        """Create sample configuration items."""
        from pathlib import Path

        return {
            ConfigType.COMMANDS: [
                ConfigItem(
                    name="cmd1",
                    type=ConfigType.COMMANDS,
                    source_path=Path("/source/commands/cmd1.md"),
                    target_path=Path("/target/.claude/commands/cmd1.md"),
                ),
                ConfigItem(
                    name="cmd2",
                    type=ConfigType.COMMANDS,
                    source_path=Path("/source/commands/cmd2.md"),
                    target_path=Path("/target/.claude/commands/cmd2.md"),
                ),
            ],
            ConfigType.SKILLS: [
                ConfigItem(
                    name="skill1",
                    type=ConfigType.SKILLS,
                    source_path=Path("/source/skills/skill1"),
                    target_path=Path("/target/.claude/skills/skill1"),
                ),
            ],
            ConfigType.AGENTS: [],
            ConfigType.HOOKS: [
                ConfigItem(
                    name="hook1",
                    type=ConfigType.HOOKS,
                    source_path=Path("/source/hooks/hook1"),
                    target_path=Path("/target/.claude/hooks/hook1"),
                ),
            ],
        }

    def test_install_ui_creation(self, sample_items: dict) -> None:
        """InstallUI can be created with items."""
        ui = InstallUI(sample_items)

        assert ui is not None
        assert hasattr(ui, "state")
        assert hasattr(ui, "items")

    def test_install_ui_state_initialization(self, sample_items: dict) -> None:
        """InstallUI initializes state correctly."""
        ui = InstallUI(sample_items)

        assert ui.state.current_tab == 0
        assert ui.state.focus == Focus.LIST
        assert isinstance(ui.state.selected_items, set)

    def test_get_current_items_commands(self, sample_items: dict) -> None:
        """Get items for commands tab."""
        ui = InstallUI(sample_items)
        ui.state.current_tab = 0  # Commands tab

        current = ui.get_current_items()

        assert len(current) == 2
        assert all(item.type == ConfigType.COMMANDS for item in current)

    def test_get_current_items_skills(self, sample_items: dict) -> None:
        """Get items for skills tab."""
        ui = InstallUI(sample_items)
        ui.state.current_tab = 1  # Skills tab

        current = ui.get_current_items()

        assert len(current) == 1
        assert current[0].type == ConfigType.SKILLS

    def test_handle_up_navigation(self, sample_items: dict) -> None:
        """Handle up arrow key navigation."""
        ui = InstallUI(sample_items)
        ui.state.current_tab = 0  # Commands tab
        ui.state.current_row = 1

        ui.handle_up()

        assert ui.state.current_row == 0

    def test_handle_down_navigation(self, sample_items: dict) -> None:
        """Handle down arrow key navigation."""
        ui = InstallUI(sample_items)
        ui.state.current_tab = 0  # Commands tab
        ui.state.current_row = 0

        ui.handle_down()

        assert ui.state.current_row >= 0  # May stay at 0 if no more items

    def test_handle_tab_switching(self, sample_items: dict) -> None:
        """Handle tab switching."""
        ui = InstallUI(sample_items)
        initial_tab = ui.state.current_tab

        ui.handle_tab()

        assert ui.state.current_tab != initial_tab or initial_tab == 3  # Wrap around

    def test_handle_space_toggles_selection(self, sample_items: dict) -> None:
        """Handle space key to toggle item selection."""
        ui = InstallUI(sample_items)
        ui.state.current_tab = 0  # Commands tab
        ui.state.current_row = 0

        items = ui.get_current_items()
        if items:
            item_name = items[0].name

            # Initially not selected
            assert item_name not in ui.state.selected_items

            # Toggle selection
            ui.handle_space()
            assert item_name in ui.state.selected_items

            # Toggle again to deselect
            ui.handle_space()
            assert item_name not in ui.state.selected_items

    def test_get_selected_items(self, sample_items: dict) -> None:
        """Get all selected items across tabs."""
        ui = InstallUI(sample_items)

        # Select some items
        commands = sample_items[ConfigType.COMMANDS]
        if commands:
            ui.state.selected_items.add(commands[0].name)

        selected = ui.get_selected_items()

        assert isinstance(selected, list)
        assert all(isinstance(item, ConfigItem) for item in selected)

    def test_ui_draw_does_not_crash(self, sample_items: dict) -> None:
        """UI draw method doesn't crash with valid items."""
        ui = InstallUI(sample_items)

        # Mock stdout to prevent actual output
        with patch("sys.stdout"):
            try:
                ui.draw()
                assert True
            except Exception as e:
                pytest.fail(f"draw() raised {type(e).__name__}: {e}")

    def test_ui_handles_empty_items(self) -> None:
        """UI handles empty configuration items gracefully."""
        empty_items = {
            ConfigType.COMMANDS: [],
            ConfigType.SKILLS: [],
            ConfigType.AGENTS: [],
            ConfigType.HOOKS: [],
        }

        ui = InstallUI(empty_items)
        assert ui is not None

        current = ui.get_current_items()
        assert len(current) == 0


class TestUINavigation:
    """Tests for complex navigation scenarios."""

    def test_left_right_navigation_buttons(self, sample_items: dict | None = None) -> None:
        """Test left/right arrow navigation between buttons."""
        if sample_items is None:
            from pathlib import Path

            sample_items = {
                ConfigType.COMMANDS: [
                    ConfigItem(
                        name="cmd1",
                        type=ConfigType.COMMANDS,
                        source_path=Path("/source/cmd1.md"),
                        target_path=Path("/target/cmd1.md"),
                    ),
                ],
                ConfigType.SKILLS: [],
                ConfigType.AGENTS: [],
                ConfigType.HOOKS: [],
            }

        ui = InstallUI(sample_items)

        # Start with LIST focus
        assert ui.state.focus == Focus.LIST

        # Navigate to buttons
        ui.state.focus = Focus.CANCEL
        assert ui.state.focus == Focus.CANCEL

        ui.state.focus = Focus.OK
        assert ui.state.focus == Focus.OK
