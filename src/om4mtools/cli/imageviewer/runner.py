"""Notebook-callable logic for the imageviewer tool.

No argv parsing or Typer here — see `main.py` for the CLI entry point.
"""

from __future__ import annotations

from pathlib import Path

import cv2
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

    Raises
    ------
    FileNotFoundError
        If `image_path` does not exist.
    OSError
        If OpenCV could not decode the file at `image_path`.
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(path)

    image: np.ndarray = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise OSError(f"could not decode image: {path}")

    return {"path": str(path), "shape": image.shape, "dtype": str(image.dtype)}
