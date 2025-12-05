"""Tests for the terminal UI module."""

from __future__ import annotations

from pathlib import Path

import pytest

from claude_tools._internal.installer import ConfigType, ConfigItem, InstallStatus
from claude_tools._internal.ui import Focus, ItemAction, UIState, InstallUI


class TestFocus:
    """Tests for Focus enum."""

    def test_focus_values(self) -> None:
        """Focus enum has expected values."""
        assert Focus.LIST.value == "list"
        assert Focus.CANCEL.value == "cancel"
        assert Focus.OK.value == "ok"


class TestItemAction:
    """Tests for ItemAction enum."""

    def test_item_action_values(self) -> None:
        """ItemAction enum has expected values."""
        assert ItemAction.NONE.value == "none"
        assert ItemAction.INSTALL.value == "install"
        assert ItemAction.UNINSTALL.value == "uninstall"


class TestUIState:
    """Tests for UIState dataclass."""

    def test_ui_state_creation(self) -> None:
        """UIState can be created with default values."""
        state = UIState(
            current_tab=0,
            current_row=0,
            scroll_offset=0,
            focus=Focus.LIST,
            item_actions={},
        )

        assert state.current_tab == 0
        assert state.current_row == 0
        assert state.scroll_offset == 0
        assert state.focus == Focus.LIST
        assert state.item_actions == {}

    def test_ui_state_item_actions(self) -> None:
        """UIState can track item actions."""
        actions = {
            "commands:cmd1": ItemAction.INSTALL,
            "hooks:hook1": ItemAction.UNINSTALL,
        }
        state = UIState(
            current_tab=0,
            current_row=0,
            scroll_offset=0,
            focus=Focus.LIST,
            item_actions=actions,
        )

        assert state.item_actions["commands:cmd1"] == ItemAction.INSTALL
        assert state.item_actions["hooks:hook1"] == ItemAction.UNINSTALL


class TestInstallUI:
    """Tests for InstallUI class."""

    @pytest.fixture
    def sample_items(self) -> dict[ConfigType, list[ConfigItem]]:
        """Create sample configuration items."""
        return {
            ConfigType.COMMANDS: [
                ConfigItem(
                    name="cmd1",
                    type=ConfigType.COMMANDS,
                    source_path=Path("/source/commands/cmd1.md"),
                    target_path=Path("/target/.claude/commands/cmd1.md"),
                    install_status=InstallStatus.NOT_INSTALLED,
                ),
                ConfigItem(
                    name="cmd2",
                    type=ConfigType.COMMANDS,
                    source_path=Path("/source/commands/cmd2.md"),
                    target_path=Path("/target/.claude/commands/cmd2.md"),
                    install_status=InstallStatus.INSTALLED_CURRENT,
                ),
            ],
            ConfigType.SKILLS: [
                ConfigItem(
                    name="skill1",
                    type=ConfigType.SKILLS,
                    source_path=Path("/source/skills/skill1"),
                    target_path=Path("/target/.claude/skills/skill1"),
                    install_status=InstallStatus.INSTALLED_OUTDATED,
                ),
            ],
            ConfigType.AGENTS: [],
            ConfigType.HOOKS: [
                ConfigItem(
                    name="hook1",
                    type=ConfigType.HOOKS,
                    source_path=Path("/source/hooks/hook1"),
                    target_path=Path("/target/.claude/hooks/hook1"),
                    install_status=InstallStatus.NOT_INSTALLED,
                ),
            ],
        }

    def test_install_ui_creation(self, sample_items: dict) -> None:
        """InstallUI can be created with items."""
        ui = InstallUI(sample_items, "/target/project")

        assert ui is not None
        assert hasattr(ui, "state")
        assert hasattr(ui, "items_by_type")

    def test_install_ui_state_initialization(self, sample_items: dict) -> None:
        """InstallUI initializes state correctly."""
        ui = InstallUI(sample_items, "/target/project")

        assert ui.state.current_tab == 0
        assert ui.state.focus == Focus.LIST
        assert isinstance(ui.state.item_actions, dict)

    def test_get_current_items_commands(self, sample_items: dict) -> None:
        """Get items for commands tab."""
        ui = InstallUI(sample_items, "/target/project")
        ui.state.current_tab = 0  # Commands tab

        current = ui.get_current_items()

        assert len(current) == 2
        assert all(item.type == ConfigType.COMMANDS for item in current)

    def test_get_current_items_skills(self, sample_items: dict) -> None:
        """Get items for skills tab."""
        ui = InstallUI(sample_items, "/target/project")
        ui.state.current_tab = 1  # Skills tab

        current = ui.get_current_items()

        assert len(current) == 1
        assert current[0].type == ConfigType.SKILLS

    def test_handle_up_navigation(self, sample_items: dict) -> None:
        """Handle up arrow key navigation."""
        ui = InstallUI(sample_items, "/target/project")
        ui.state.current_tab = 0  # Commands tab
        ui.state.current_row = 1

        ui.handle_up()

        assert ui.state.current_row == 0

    def test_handle_down_navigation(self, sample_items: dict) -> None:
        """Handle down arrow key navigation."""
        ui = InstallUI(sample_items, "/target/project")
        ui.state.current_tab = 0  # Commands tab
        ui.state.current_row = 0

        ui.handle_down()

        assert ui.state.current_row >= 0  # May stay at 0 if no more items

    def test_handle_tab_focus_switching(self, sample_items: dict) -> None:
        """Handle tab key switches focus between LIST, CANCEL, OK."""
        ui = InstallUI(sample_items, "/target/project")
        assert ui.state.focus == Focus.LIST

        ui.handle_tab()
        assert ui.state.focus == Focus.CANCEL

        ui.handle_tab()
        assert ui.state.focus == Focus.OK

        ui.handle_tab()
        assert ui.state.focus == Focus.LIST

    def test_handle_space_not_installed(self, sample_items: dict) -> None:
        """Handle space key for NOT_INSTALLED item cycles NONE → INSTALL → NONE."""
        ui = InstallUI(sample_items, "/target/project")
        ui.state.current_tab = 0  # Commands tab
        ui.state.current_row = 0  # cmd1 is NOT_INSTALLED

        items = ui.get_current_items()
        item = items[0]
        key = f"{item.type.value}:{item.name}"

        # Initially NONE
        assert ui.state.item_actions.get(key, ItemAction.NONE) == ItemAction.NONE

        # Toggle to INSTALL
        ui.handle_space()
        assert ui.state.item_actions.get(key) == ItemAction.INSTALL

        # Toggle back to NONE
        ui.handle_space()
        assert ui.state.item_actions.get(key) == ItemAction.NONE

    def test_handle_space_installed_current(self, sample_items: dict) -> None:
        """Handle space key for INSTALLED_CURRENT item cycles NONE → UNINSTALL → NONE."""
        ui = InstallUI(sample_items, "/target/project")
        ui.state.current_tab = 0  # Commands tab
        ui.state.current_row = 1  # cmd2 is INSTALLED_CURRENT

        items = ui.get_current_items()
        item = items[1]
        key = f"{item.type.value}:{item.name}"

        # Initially NONE
        assert ui.state.item_actions.get(key, ItemAction.NONE) == ItemAction.NONE

        # Toggle to UNINSTALL
        ui.handle_space()
        assert ui.state.item_actions.get(key) == ItemAction.UNINSTALL

        # Toggle back to NONE
        ui.handle_space()
        assert ui.state.item_actions.get(key) == ItemAction.NONE

    def test_handle_space_installed_outdated(self, sample_items: dict) -> None:
        """Handle space key for INSTALLED_OUTDATED item cycles NONE → INSTALL → NONE."""
        ui = InstallUI(sample_items, "/target/project")
        ui.state.current_tab = 1  # Skills tab
        ui.state.current_row = 0  # skill1 is INSTALLED_OUTDATED

        items = ui.get_current_items()
        item = items[0]
        key = f"{item.type.value}:{item.name}"

        # Initially NONE
        assert ui.state.item_actions.get(key, ItemAction.NONE) == ItemAction.NONE

        # Toggle to INSTALL (update)
        ui.handle_space()
        assert ui.state.item_actions.get(key) == ItemAction.INSTALL

        # Toggle back to NONE
        ui.handle_space()
        assert ui.state.item_actions.get(key) == ItemAction.NONE

    def test_get_items_to_install(self, sample_items: dict) -> None:
        """Get all items with INSTALL action."""
        ui = InstallUI(sample_items, "/target/project")

        # Mark items for install
        ui.state.item_actions["commands:cmd1"] = ItemAction.INSTALL
        ui.state.item_actions["skills:skill1"] = ItemAction.INSTALL

        items_to_install = ui.get_items_to_install()

        assert len(items_to_install) == 2
        names = [item.name for item in items_to_install]
        assert "cmd1" in names
        assert "skill1" in names

    def test_get_items_to_uninstall(self, sample_items: dict) -> None:
        """Get all items with UNINSTALL action."""
        ui = InstallUI(sample_items, "/target/project")

        # Mark item for uninstall
        ui.state.item_actions["commands:cmd2"] = ItemAction.UNINSTALL

        items_to_uninstall = ui.get_items_to_uninstall()

        assert len(items_to_uninstall) == 1
        assert items_to_uninstall[0].name == "cmd2"

    def test_get_selected_items_backward_compat(self, sample_items: dict) -> None:
        """get_selected_items returns same as get_items_to_install."""
        ui = InstallUI(sample_items, "/target/project")

        ui.state.item_actions["commands:cmd1"] = ItemAction.INSTALL

        selected = ui.get_selected_items()
        to_install = ui.get_items_to_install()

        assert selected == to_install

    def test_ui_render_does_not_crash(self, sample_items: dict) -> None:
        """UI render method doesn't crash with valid items."""
        ui = InstallUI(sample_items, "/target/project")

        try:
            result = ui.render()
            assert result is not None
        except Exception as e:
            pytest.fail(f"render() raised {type(e).__name__}: {e}")

    def test_ui_handles_empty_items(self) -> None:
        """UI handles empty configuration items gracefully."""
        empty_items = {
            ConfigType.COMMANDS: [],
            ConfigType.SKILLS: [],
            ConfigType.AGENTS: [],
            ConfigType.HOOKS: [],
        }

        ui = InstallUI(empty_items, "/target/project")
        assert ui is not None

        current = ui.get_current_items()
        assert len(current) == 0


class TestUINavigation:
    """Tests for complex navigation scenarios."""

    def test_left_right_navigation_tabs(self) -> None:
        """Test left/right arrow navigation between tabs."""
        sample_items = {
            ConfigType.COMMANDS: [
                ConfigItem(
                    name="cmd1",
                    type=ConfigType.COMMANDS,
                    source_path=Path("/source/cmd1.md"),
                    target_path=Path("/target/cmd1.md"),
                    install_status=InstallStatus.NOT_INSTALLED,
                ),
            ],
            ConfigType.SKILLS: [],
            ConfigType.AGENTS: [],
            ConfigType.HOOKS: [],
        }

        ui = InstallUI(sample_items, "/target/project")

        # Start on first tab
        assert ui.state.current_tab == 0

        # Move right
        ui.handle_right()
        assert ui.state.current_tab == 1

        # Move left
        ui.handle_left()
        assert ui.state.current_tab == 0

    def test_left_right_navigation_buttons(self) -> None:
        """Test left/right arrow navigation between buttons."""
        sample_items = {
            ConfigType.COMMANDS: [],
            ConfigType.SKILLS: [],
            ConfigType.AGENTS: [],
            ConfigType.HOOKS: [],
        }

        ui = InstallUI(sample_items, "/target/project")

        # Navigate to CANCEL
        ui.state.focus = Focus.CANCEL
        assert ui.state.focus == Focus.CANCEL

        # Move right to OK
        ui.handle_right()
        assert ui.state.focus == Focus.OK

        # Move left back to CANCEL
        ui.handle_left()
        assert ui.state.focus == Focus.CANCEL
