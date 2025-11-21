# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m claude_tools` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `claude_tools.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `claude_tools.__main__` in `sys.modules`.

from __future__ import annotations

import argparse
import sys
import termios
import time
import tty
from pathlib import Path
from typing import Any

from claude_tools._internal import debug
from claude_tools._internal.installer import ConfigType, Installer
from claude_tools._internal.ui import Color, Focus, InstallUI


class _DebugInfo(argparse.Action):
    def __init__(self, nargs: int | str | None = 0, **kwargs: Any) -> None:
        super().__init__(nargs=nargs, **kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        debug._print_debug_info()
        sys.exit(0)


def get_parser() -> argparse.ArgumentParser:
    """Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(
        prog="claude-tools",
        description="Installer for Claude agents, skills, hooks, and commands",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {debug._get_version()}"
    )
    parser.add_argument(
        "--debug-info", action=_DebugInfo, help="Print debug information."
    )
    parser.add_argument(
        "project_path",
        nargs="?",
        default=None,
        help="Path to the target project (default: prompted if not provided)",
    )
    return parser


def read_key() -> str:
    """Read a single key from stdin.

    Returns:
        The key pressed
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def run_interactive_installer(installer: Installer, ui: InstallUI) -> bool:
    """Run the interactive installer UI.

    Args:
        installer: The installer instance
        ui: The UI instance

    Returns:
        True if installation should proceed, False if cancelled
    """
    try:
        # Setup terminal for raw input
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())

        while True:
            ui.draw()

            # Read input
            try:
                ch = sys.stdin.read(1)
                if ch == "\x1b":  # Escape sequence
                    ch2 = sys.stdin.read(1)
                    if ch2 == "[":
                        ch3 = sys.stdin.read(1)
                        if ch3 == "A":  # Up arrow
                            ui.handle_up()
                        elif ch3 == "B":  # Down arrow
                            ui.handle_down()
                        elif ch3 == "D":  # Left arrow
                            ui.handle_left()
                        elif ch3 == "C":  # Right arrow
                            ui.handle_right()
                elif ch == " ":  # Space
                    ui.handle_space()
                elif ch == "\t":  # Tab
                    ui.handle_tab()
                elif ch in ("\n", "\r"):  # Enter
                    if ui.state.focus == Focus.CANCEL:
                        return False
                    elif ui.state.focus == Focus.OK:
                        return True
                    elif ui.state.focus == Focus.LIST:
                        ui.state.focus = Focus.OK
                elif ch in ("q", "Q", "\x1b"):  # q or Escape
                    return False
            except KeyboardInterrupt:
                return False

    finally:
        # Restore terminal
        print(f"{Color.SHOW_CURSOR}", end="", flush=True)
        if sys.platform != "win32" and "old_settings" in locals():
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            except Exception:
                pass


def main(args: list[str] | None = None) -> int:
    """Run the main program.

    This function is executed when you type `claude-tools` or `python -m claude_tools`.

    Parameters:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    opts = parser.parse_args(args=args)

    # Get target project
    target_project = opts.project_path
    if not target_project:
        print("Enter target project path:")
        target_project = input().strip()

    if not target_project:
        print(f"{Color.YELLOW}No project path provided.{Color.RESET}")
        return 1

    # Get repository root (parent of src directory)
    repo_root = Path(__file__).parent.parent.parent.parent

    # Initialize installer
    installer = Installer(repo_root, target_project)

    # Validate paths
    if not installer.validate_paths():
        return 1

    # Ensure .claude directory exists
    if not installer.ensure_claude_directory():
        return 1

    # Get available items
    items_by_type = {}
    for config_type in ConfigType:
        items_by_type[config_type] = installer.get_available_items(config_type)

    # Run interactive UI
    ui = InstallUI(items_by_type, str(target_project))

    print(f"{Color.BOLD}Starting interactive installer...{Color.RESET}")
    time.sleep(1)  # Brief pause before UI starts

    if not run_interactive_installer(installer, ui):
        print(f"{Color.YELLOW}Installation cancelled.{Color.RESET}")
        return 0

    # Get selected items
    selected_items = ui.get_selected_items()

    if not selected_items:
        print(f"{Color.YELLOW}No items selected. Nothing to install.{Color.RESET}")
        return 0

    # Install selected items
    print(f"{Color.BOLD}Installing selected items...{Color.RESET}")
    print()

    # Separate items by type
    hook_items = [item for item in selected_items if item.type == ConfigType.HOOKS]
    other_items = [item for item in selected_items if item.type != ConfigType.HOOKS]

    # Install non-hook items
    successful, failed = installer.install_items(other_items)
    for item in other_items:
        print(f"{Color.GREEN}✓{Color.RESET} Installed {item.type.value}: {item.name}")

    # Install hook items and merge settings
    if hook_items:
        hook_successful, hook_failed = installer.install_items(hook_items)
        for item in hook_items:
            print(f"{Color.GREEN}✓{Color.RESET} Installed hook: {item.name}")

        # Merge hook settings
        if hook_successful > 0:
            if installer.merge_hook_settings(hook_items):
                print(
                    f"{Color.BLUE}✓{Color.RESET} Merged hook settings into .claude/settings.json"
                )
            else:
                print(
                    f"{Color.YELLOW}⚠{Color.RESET} Failed to merge some hook settings"
                )

        successful += hook_successful
        failed += hook_failed

    print()
    print(
        f"{Color.BOLD}{Color.GREEN}Installation complete!{Color.RESET} Installed {successful} item(s)."
    )
    if failed > 0:
        print(f"{Color.YELLOW}Failed to install {failed} item(s).{Color.RESET}")
        return 1

    return 0
