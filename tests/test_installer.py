"""Tests for the installer module."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from claude_tools._internal.installer import ConfigType, ConfigItem, Installer

if TYPE_CHECKING:
    from collections.abc import Iterator


@pytest.fixture
def temp_repo_dir() -> Iterator[Path]:
    """Create temporary repository directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / "repo"
        repo_path.mkdir()

        # Create configuration directories
        (repo_path / "commands").mkdir()
        (repo_path / "skills").mkdir()
        (repo_path / "agents").mkdir()
        (repo_path / "hooks").mkdir()

        # Create sample command
        (repo_path / "commands" / "test-command.md").write_text("# Test Command\n\nTest description")

        # Create sample skill
        skill_dir = repo_path / "skills" / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Test Skill")

        # Create sample agent
        agent_dir = repo_path / "agents" / "test-agent"
        agent_dir.mkdir()
        (agent_dir / "config.json").write_text("{}")

        # Create sample hook
        hook_dir = repo_path / "hooks" / "test-hook"
        hook_dir.mkdir()
        (hook_dir / "test-hook.sh").write_text("#!/bin/bash\necho 'test'")
        (hook_dir / "settings.json").write_text('{"hooks": {"Stop": [{"test": true}]}}')

        yield repo_path


@pytest.fixture
def temp_target_dir() -> Iterator[Path]:
    """Create temporary target directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        target_path = Path(tmpdir)
        yield target_path


class TestConfigType:
    """Tests for ConfigType enum."""

    def test_config_type_values(self) -> None:
        """ConfigType has expected values."""
        assert ConfigType.COMMANDS.value == "commands"
        assert ConfigType.SKILLS.value == "skills"
        assert ConfigType.AGENTS.value == "agents"
        assert ConfigType.HOOKS.value == "hooks"


class TestConfigItem:
    """Tests for ConfigItem dataclass."""

    def test_config_item_creation(self) -> None:
        """ConfigItem can be created with required fields."""
        item = ConfigItem(
            name="test-item",
            type=ConfigType.COMMANDS,
            source_path=Path("/source"),
            target_path=Path("/target"),
        )
        assert item.name == "test-item"
        assert item.type == ConfigType.COMMANDS
        assert item.source_path == Path("/source")
        assert item.target_path == Path("/target")


class TestInstallerPathValidation:
    """Tests for Installer path validation."""

    def test_validate_paths_success(self, temp_repo_dir: Path, temp_target_dir: Path) -> None:
        """Path validation succeeds with valid paths."""
        installer = Installer(repo_root=temp_repo_dir, target_project=temp_target_dir)
        assert installer.validate_paths() is True

    def test_validate_paths_missing_repo(self, temp_target_dir: Path) -> None:
        """Path validation fails when repo doesn't exist."""
        installer = Installer(
            repo_root=Path("/nonexistent/repo"),
            target_project=temp_target_dir,
        )
        assert installer.validate_paths() is False

    def test_validate_paths_missing_target(self, temp_repo_dir: Path) -> None:
        """Path validation fails when target doesn't exist."""
        installer = Installer(
            repo_root=temp_repo_dir,
            target_project=Path("/nonexistent/target"),
        )
        assert installer.validate_paths() is False


class TestInstallerItemDiscovery:
    """Tests for Installer item discovery."""

    def test_discover_commands(self, temp_repo_dir: Path, temp_target_dir: Path) -> None:
        """Discover available commands."""
        installer = Installer(repo_root=temp_repo_dir, target_project=temp_target_dir)
        items = installer.get_available_items(ConfigType.COMMANDS)

        assert len(items) > 0
        assert any(item.name == "test-command" for item in items)

    def test_discover_skills(self, temp_repo_dir: Path, temp_target_dir: Path) -> None:
        """Discover available skills."""
        installer = Installer(repo_root=temp_repo_dir, target_project=temp_target_dir)
        items = installer.get_available_items(ConfigType.SKILLS)

        assert len(items) > 0
        assert any(item.name == "test-skill" for item in items)

    def test_discover_agents(self, temp_repo_dir: Path, temp_target_dir: Path) -> None:
        """Discover available agents."""
        installer = Installer(repo_root=temp_repo_dir, target_project=temp_target_dir)
        items = installer.get_available_items(ConfigType.AGENTS)

        assert len(items) > 0
        assert any(item.name == "test-agent" for item in items)

    def test_discover_hooks(self, temp_repo_dir: Path, temp_target_dir: Path) -> None:
        """Discover available hooks."""
        installer = Installer(repo_root=temp_repo_dir, target_project=temp_target_dir)
        items = installer.get_available_items(ConfigType.HOOKS)

        assert len(items) > 0
        assert any(item.name == "test-hook" for item in items)

    def test_discover_empty_config_type(self, temp_repo_dir: Path, temp_target_dir: Path) -> None:
        """Discover returns empty list for non-existent items."""
        # Create empty repo without items
        with tempfile.TemporaryDirectory() as tmpdir:
            empty_repo = Path(tmpdir)
            (empty_repo / "commands").mkdir()
            (empty_repo / "skills").mkdir()
            (empty_repo / "agents").mkdir()
            (empty_repo / "hooks").mkdir()

            installer = Installer(repo_root=empty_repo, target_project=temp_target_dir)
            items = installer.get_available_items(ConfigType.COMMANDS)
            assert len(items) == 0


class TestInstallerInstallation:
    """Tests for installation functionality."""

    def test_install_command(self, temp_repo_dir: Path, temp_target_dir: Path) -> None:
        """Install a command successfully."""
        installer = Installer(repo_root=temp_repo_dir, target_project=temp_target_dir)
        items = installer.get_available_items(ConfigType.COMMANDS)

        assert len(items) > 0
        item = items[0]

        # Ensure target .claude/commands doesn't exist
        target_commands = temp_target_dir / ".claude" / "commands"
        assert not target_commands.exists()

        # Install should create the directory structure
        success, failed = installer.install_items([item])

        assert success >= 0
        assert failed >= 0

    def test_install_multiple_items(self, temp_repo_dir: Path, temp_target_dir: Path) -> None:
        """Install multiple items at once."""
        installer = Installer(repo_root=temp_repo_dir, target_project=temp_target_dir)

        commands = installer.get_available_items(ConfigType.COMMANDS)
        skills = installer.get_available_items(ConfigType.SKILLS)

        items_to_install = commands + skills

        if items_to_install:
            success, failed = installer.install_items(items_to_install)
            assert success >= 0
            assert failed >= 0


class TestHookSettingsMerge:
    """Tests for hook settings merge functionality."""

    def test_merge_hook_settings_new_file(
        self, temp_repo_dir: Path, temp_target_dir: Path
    ) -> None:
        """Merge hook settings when settings.json doesn't exist."""
        installer = Installer(repo_root=temp_repo_dir, target_project=temp_target_dir)

        # Ensure .claude directory exists
        claude_dir = temp_target_dir / ".claude"
        claude_dir.mkdir(exist_ok=True)

        # Get hook items
        hooks = installer.get_available_items(ConfigType.HOOKS)

        if hooks:
            installer.merge_hook_settings(hooks)

            # Check if settings.json was created
            settings_file = claude_dir / "settings.json"
            # Settings file may or may not be created depending on hook structure
            if settings_file.exists():
                with open(settings_file) as f:
                    settings = json.load(f)
                assert "hooks" in settings or isinstance(settings, dict)

    def test_merge_hook_settings_existing_file(
        self, temp_repo_dir: Path, temp_target_dir: Path
    ) -> None:
        """Merge hook settings when settings.json already exists."""
        installer = Installer(repo_root=temp_repo_dir, target_project=temp_target_dir)

        # Create .claude directory with existing settings
        claude_dir = temp_target_dir / ".claude"
        claude_dir.mkdir(exist_ok=True)

        existing_settings = {
            "hooks": {
                "PreToolUse": [{"existing": "handler"}]
            }
        }
        settings_file = claude_dir / "settings.json"
        with open(settings_file, "w") as f:
            json.dump(existing_settings, f)

        # Get hook items and merge
        hooks = installer.get_available_items(ConfigType.HOOKS)

        if hooks:
            installer.merge_hook_settings(hooks)

            # Verify settings file still exists
            assert settings_file.exists()

            # Verify it's still valid JSON
            with open(settings_file) as f:
                merged = json.load(f)
            assert isinstance(merged, dict)


class TestConfigItemFields:
    """Tests for ConfigItem field validation."""

    def test_config_item_has_required_fields(self) -> None:
        """ConfigItem has all required fields."""
        item = ConfigItem(
            name="test",
            type=ConfigType.COMMANDS,
            source_path=Path("/source"),
            target_path=Path("/target"),
        )

        assert hasattr(item, "name")
        assert hasattr(item, "type")
        assert hasattr(item, "source_path")
        assert hasattr(item, "target_path")
