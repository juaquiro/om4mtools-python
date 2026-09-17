"""Typer app for the fringeprocessor CLI. Parses argv, calls `runner.py`."""

from __future__ import annotations

import typer

from om4mtools.cli.fringeprocessor.runner import process_fringe_pattern

app = typer.Typer(help="Demodulate and unwrap fringe-pattern images from the command line.")


@app.command()
def process(image_path: str, fx: float, fy: float) -> None:
    """Process a fringe-pattern image and report the resulting phase shape."""
    phase = process_fringe_pattern(image_path, (fx, fy))
    typer.echo(f"unwrapped phase shape: {phase.shape}")


if __name__ == "__main__":
    app()
