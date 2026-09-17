"""Typer app for the imageviewer CLI. Parses argv, calls `runner.py`."""

from __future__ import annotations

import typer

from om4mtools.cli.imageviewer.runner import load_and_describe

app = typer.Typer(help="Inspect fringe-pattern images from the command line.")


@app.command()
def describe(image_path: str) -> None:
    """Print basic properties of an image file."""
    info = load_and_describe(image_path)
    for key, value in info.items():
        typer.echo(f"{key}: {value}")


if __name__ == "__main__":
    app()
