"""claude-tools package.

Installer for common Claude agents, skills, hooks and commands
"""

from __future__ import annotations

from claude_tools._internal.cli import get_parser, main

__all__: list[str] = ["get_parser", "main"]
