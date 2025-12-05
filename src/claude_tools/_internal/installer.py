"""Claude configuration installer module.

Handles installation of commands, skills, agents, and hooks into projects.
"""

from __future__ import annotations

import json
import shutil
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ConfigType(Enum):
    """Types of Claude configurations."""

    COMMANDS = "commands"
    SKILLS = "skills"
    AGENTS = "agents"
    HOOKS = "hooks"


class InstallStatus(Enum):
    """Installation status of a configuration item."""

    NOT_INSTALLED = "not_installed"
    INSTALLED_CURRENT = "installed_current"
    INSTALLED_OUTDATED = "installed_outdated"


@dataclass
class ConfigItem:
    """Represents a configuration item."""

    name: str
    type: ConfigType
    source_path: Path
    target_path: Path | None = None
    install_status: InstallStatus = InstallStatus.NOT_INSTALLED


class Installer:
    """Handles installation of Claude configurations into projects."""

    def __init__(self, repo_root: Path | str, target_project: Path | str) -> None:
        """Initialize the installer.

        Args:
            repo_root: Path to the claude-tools repository
            target_project: Path to the target project
        """
        self.repo_root = Path(repo_root)
        self.target_project = Path(target_project)
        self.claude_dir = self.target_project / ".claude"

    def validate_paths(self) -> bool:
        """Validate that paths exist and are valid.

        Returns:
            True if paths are valid, False otherwise
        """
        if not self.repo_root.exists():
            print(
                f"Error: Repository root does not exist: {self.repo_root}",
                file=sys.stderr,
            )
            return False

        if not self.target_project.exists():
            print(
                f"Error: Target project does not exist: {self.target_project}",
                file=sys.stderr,
            )
            return False

        if not self.target_project.is_dir():
            print(
                f"Error: Target project is not a directory: {self.target_project}",
                file=sys.stderr,
            )
            return False

        return True

    def get_available_items(self, config_type: ConfigType) -> list[ConfigItem]:
        """Get available items for a configuration type.

        Args:
            config_type: The type of configuration to list

        Returns:
            List of available configuration items
        """
        repo_dir = self.repo_root / config_type.value
        items = []

        if not repo_dir.exists():
            return items

        if config_type in (ConfigType.COMMANDS, ConfigType.AGENTS):
            # Commands and agents are .md files
            for file in sorted(repo_dir.glob("*.md")):
                name = file.stem
                item = ConfigItem(
                    name=name,
                    type=config_type,
                    source_path=file,
                    target_path=self.claude_dir / config_type.value / f"{name}.md",
                )
                item.install_status = self.get_install_status(item)
                items.append(item)
        elif config_type == ConfigType.SKILLS:
            # Skills are directories
            for dir_path in sorted(repo_dir.iterdir()):
                if dir_path.is_dir() and not dir_path.name.startswith("."):
                    item = ConfigItem(
                        name=dir_path.name,
                        type=config_type,
                        source_path=dir_path,
                        target_path=self.claude_dir / config_type.value / dir_path.name,
                    )
                    item.install_status = self.get_install_status(item)
                    items.append(item)
        elif config_type == ConfigType.HOOKS:
            # Hooks are directories
            for dir_path in sorted(repo_dir.iterdir()):
                if dir_path.is_dir() and not dir_path.name.startswith("."):
                    item = ConfigItem(
                        name=dir_path.name,
                        type=config_type,
                        source_path=dir_path,
                        target_path=self.claude_dir / "hooks" / dir_path.name,
                    )
                    item.install_status = self.get_install_status(item)
                    items.append(item)

        return items

    def install_item(self, item: ConfigItem) -> bool:
        """Install a single configuration item.

        Args:
            item: The configuration item to install

        Returns:
            True if installation succeeded, False otherwise
        """
        if not item.target_path:
            print(f"Error: No target path for {item.name}", file=sys.stderr)
            return False

        # Create parent directories
        item.target_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if item.source_path.is_dir():
                # Copy directory
                if item.target_path.exists():
                    shutil.rmtree(item.target_path)
                shutil.copytree(item.source_path, item.target_path)
            else:
                # Copy file
                shutil.copy2(item.source_path, item.target_path)

            return True
        except Exception as e:
            print(f"Error installing {item.name}: {e}", file=sys.stderr)
            return False

    def install_items(self, items: list[ConfigItem]) -> tuple[int, int]:
        """Install multiple configuration items.

        Args:
            items: List of configuration items to install

        Returns:
            Tuple of (successful, failed) counts
        """
        successful = 0
        failed = 0

        for item in items:
            if self.install_item(item):
                successful += 1
            else:
                failed += 1

        return successful, failed

    def merge_hook_settings(self, hook_items: list[ConfigItem]) -> bool:
        """Merge hook settings into .claude/settings.json.

        Args:
            hook_items: List of hook items to merge

        Returns:
            True if merge succeeded, False otherwise
        """
        settings_file = self.claude_dir / "settings.json"

        # Load existing settings or create new
        if settings_file.exists():
            try:
                with open(settings_file) as f:
                    settings = json.load(f)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in {settings_file}", file=sys.stderr)
                return False
        else:
            settings = {"hooks": {}}

        # Ensure hooks section exists
        if "hooks" not in settings:
            settings["hooks"] = {}

        # Merge hook settings from each hook
        for item in hook_items:
            if item.target_path is None:
                continue
            hook_settings_file = item.target_path / "settings.json"
            if hook_settings_file.exists():
                try:
                    with open(hook_settings_file) as f:
                        hook_config = json.load(f)

                    # Merge hooks from the config
                    if "hooks" in hook_config:
                        for event, handlers in hook_config["hooks"].items():
                            if event not in settings["hooks"]:
                                settings["hooks"][event] = []
                            # Append handlers if not already present
                            for handler in handlers:
                                if handler not in settings["hooks"][event]:
                                    settings["hooks"][event].append(handler)
                except json.JSONDecodeError:
                    print(
                        f"Error: Invalid JSON in {hook_settings_file}", file=sys.stderr
                    )
                    return False

        # Write merged settings
        try:
            settings_file.write_text(json.dumps(settings, indent=2))
            return True
        except Exception as e:
            print(f"Error writing settings: {e}", file=sys.stderr)
            return False

    def ensure_claude_directory(self) -> bool:
        """Ensure .claude directory exists.

        Returns:
            True if successful, False otherwise
        """
        try:
            self.claude_dir.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating .claude directory: {e}", file=sys.stderr)
            return False

    def _compare_files(self, source: Path, target: Path) -> bool:
        """Compare two files for equality.

        Args:
            source: Source file path
            target: Target file path

        Returns:
            True if files are identical, False otherwise
        """
        try:
            return source.read_bytes() == target.read_bytes()
        except Exception:
            return False

    def _compare_directories(self, source: Path, target: Path) -> bool:
        """Compare two directories recursively.

        Args:
            source: Source directory path
            target: Target directory path

        Returns:
            True if directories are identical, False otherwise
        """
        try:
            # Get all files in both directories
            source_files = {
                f.relative_to(source): f for f in source.rglob("*") if f.is_file()
            }
            target_files = {
                f.relative_to(target): f for f in target.rglob("*") if f.is_file()
            }

            # Check same files exist
            if source_files.keys() != target_files.keys():
                return False

            # Compare each file
            for rel_path in source_files:
                if not self._compare_files(
                    source_files[rel_path], target_files[rel_path]
                ):
                    return False

            return True
        except Exception:
            return False

    def get_install_status(self, item: ConfigItem) -> InstallStatus:
        """Check if item is installed and if it matches source.

        Args:
            item: The configuration item to check

        Returns:
            Installation status of the item
        """
        if not item.target_path or not item.target_path.exists():
            return InstallStatus.NOT_INSTALLED

        # Compare based on file or directory
        if item.source_path.is_dir():
            is_current = self._compare_directories(item.source_path, item.target_path)
        else:
            is_current = self._compare_files(item.source_path, item.target_path)

        return (
            InstallStatus.INSTALLED_CURRENT
            if is_current
            else InstallStatus.INSTALLED_OUTDATED
        )

    def uninstall_item(self, item: ConfigItem) -> bool:
        """Remove an installed configuration item.

        Args:
            item: The configuration item to uninstall

        Returns:
            True if uninstallation succeeded, False otherwise
        """
        if not item.target_path or not item.target_path.exists():
            return True  # Already not installed

        try:
            if item.target_path.is_dir():
                shutil.rmtree(item.target_path)
            else:
                item.target_path.unlink()
            return True
        except Exception as e:
            print(f"Error uninstalling {item.name}: {e}", file=sys.stderr)
            return False

    def unmerge_hook_settings(self, hook_item: ConfigItem) -> bool:
        """Remove hook handlers from .claude/settings.json.

        Args:
            hook_item: The hook item whose handlers should be removed

        Returns:
            True if unmerge succeeded, False otherwise
        """
        settings_file = self.claude_dir / "settings.json"

        if not settings_file.exists():
            return True  # Nothing to unmerge

        # Read the hook's settings to know what to remove
        if hook_item.target_path is None:
            # Try to find handlers from source
            hook_settings_file = hook_item.source_path / "settings.json"
        else:
            hook_settings_file = hook_item.target_path / "settings.json"
            if not hook_settings_file.exists():
                hook_settings_file = hook_item.source_path / "settings.json"

        if not hook_settings_file.exists():
            return True  # No handlers to remove

        try:
            # Load current settings
            with open(settings_file) as f:
                settings = json.load(f)

            # Load hook handlers to remove
            with open(hook_settings_file) as f:
                hook_config = json.load(f)

            if "hooks" not in settings or "hooks" not in hook_config:
                return True

            # Remove handlers for each event
            for event, handlers_to_remove in hook_config["hooks"].items():
                if event in settings["hooks"]:
                    settings["hooks"][event] = [
                        h
                        for h in settings["hooks"][event]
                        if h not in handlers_to_remove
                    ]
                    # Clean up empty event lists
                    if not settings["hooks"][event]:
                        del settings["hooks"][event]

            # Clean up empty hooks section
            if not settings["hooks"]:
                del settings["hooks"]

            # Write updated settings
            settings_file.write_text(json.dumps(settings, indent=2))
            return True

        except Exception as e:
            print(f"Error unmerging hook settings: {e}", file=sys.stderr)
            return False
