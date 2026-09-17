"""Notebook-callable logic for the imageviewer tool.

No argv parsing or Typer here — see `main.py` for the CLI entry point.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


def load_and_describe(image_path: str | Path) -> dict[str, object]:
    """Load an image and report its basic properties.

    Parameters
    ----------
    image_path : str or pathlib.Path
        Path to the image file to inspect.

    Returns
    -------
    dict[str, object]
        Summary with keys ``"path"``, ``"shape"``, and ``"dtype"``.
    """
    from om4mtools.io.images import load_image

    image: np.ndarray = load_image(image_path)
    return {"path": str(image_path), "shape": image.shape, "dtype": str(image.dtype)}
