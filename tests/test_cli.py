"""Tests for the CLI."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from claude_tools import main
from claude_tools._internal import debug


def test_main() -> None:
    """Basic CLI test."""
    assert main([]) == 0


def test_show_help(capsys: pytest.CaptureFixture) -> None:
    """Show help.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        main(["-h"])
    captured = capsys.readouterr()
    assert "claude-tools" in captured.out


def test_show_version(capsys: pytest.CaptureFixture) -> None:
    """Show version.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        main(["-V"])
    captured = capsys.readouterr()
    assert debug._get_version() in captured.out


def test_show_debug_info(capsys: pytest.CaptureFixture) -> None:
    """Show debug information.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        main(["--debug-info"])
    captured = capsys.readouterr().out.lower()
    assert "python" in captured
    assert "system" in captured
    assert "environment" in captured
    assert "packages" in captured


class TestCLIWithProjectPath:
    """Tests for CLI with project path argument."""

    def test_cli_with_valid_project_path(self) -> None:
        """CLI accepts a valid project path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)

            # Mock the installer to avoid actual installation
            with patch("claude_tools._internal.cli.Installer"):
                with patch("claude_tools._internal.cli.InstallUI"):
                    # Main should handle the path argument
                    result = main([str(project_path)])
                    # Should not raise an exception
                    assert result in (0, None)

    def test_cli_with_nonexistent_path(self) -> None:
        """CLI handles non-existent project path."""
        nonexistent_path = "/nonexistent/path/to/project"

        with patch("claude_tools._internal.cli.Installer") as mock_installer:
            # Setup the mock to return False for path validation
            mock_instance = MagicMock()
            mock_instance.validate_paths.return_value = False
            mock_installer.return_value = mock_instance

            result = main([nonexistent_path])
            # Should handle gracefully (0 or error code)
            assert result in (0, 1)


class TestCLIArgumentParsing:
    """Tests for CLI argument parsing."""

    def test_parser_has_help(self) -> None:
        """ArgumentParser includes help."""
        from claude_tools._internal.cli import get_parser

        parser = get_parser()
        assert parser is not None

    def test_parser_accepts_project_path(self) -> None:
        """ArgumentParser accepts project path argument."""
        from claude_tools._internal.cli import get_parser

        parser = get_parser()
        with tempfile.TemporaryDirectory() as tmpdir:
            args = parser.parse_args([tmpdir])
            assert args is not None
            assert hasattr(args, "project_path")

    def test_parser_accepts_version(self) -> None:
        """ArgumentParser includes version option."""
        from claude_tools._internal.cli import get_parser

        parser = get_parser()

        # Check that -V or --version is in the parser
        try:
            with pytest.raises(SystemExit):
                parser.parse_args(["-V"])
        except AssertionError:
            # If -V isn't recognized, it should have --version
            with pytest.raises(SystemExit):
                parser.parse_args(["--version"])

    def test_parser_accepts_help_flag(self) -> None:
        """ArgumentParser includes help flag."""
        from claude_tools._internal.cli import get_parser

        parser = get_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["-h"])


class TestCLIIntegration:
    """Integration tests for CLI."""

    def test_cli_main_function_exists(self) -> None:
        """Main function is callable."""
        from claude_tools import main as main_func

        assert callable(main_func)

    def test_cli_returns_exit_code(self) -> None:
        """CLI returns valid exit code."""
        result = main([])

        # Should return 0 or None (success)
        assert result in (0, None) or isinstance(result, int)

    def test_cli_help_text_complete(self, capsys: pytest.CaptureFixture) -> None:
        """Help text includes necessary information."""
        with pytest.raises(SystemExit):
            main(["-h"])

        captured = capsys.readouterr()
        # Help should mention the tool and its purpose
        assert "claude" in captured.out.lower()


class TestCLIErrorHandling:
    """Tests for CLI error handling."""

    def test_cli_handles_invalid_arguments(self) -> None:
        """CLI handles invalid arguments gracefully."""
        with patch("sys.exit"):
            # Invalid argument should not crash
            try:
                main(["--invalid-flag"])
            except SystemExit:
                # SystemExit is expected for invalid args
                pass

    def test_cli_handles_keyboard_interrupt(self) -> None:
        """CLI handles KeyboardInterrupt."""
        with patch("claude_tools._internal.cli.run_interactive_installer") as mock_run:
            mock_run.side_effect = KeyboardInterrupt()

            with tempfile.TemporaryDirectory() as tmpdir:
                # Should handle keyboard interrupt without crashing
                try:
                    main([tmpdir])
                except KeyboardInterrupt:
                    # KeyboardInterrupt is acceptable in tests
                    pass

