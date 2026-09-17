"""Integration tests for the imageviewer CLI entry point."""

from __future__ import annotations

import pytest

typer_testing = pytest.importorskip("typer.testing")

from om4mtools.cli.imageviewer.main import app  # noqa: E402


def test_describe_command_exists() -> None:
    """The `describe` command is registered on the Typer app."""
    runner = typer_testing.CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "describe" in result.stdout
