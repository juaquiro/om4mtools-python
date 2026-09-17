"""Image loading helpers."""

from __future__ import annotations

from pathlib import Path

import numpy as np


def load_image(path: str | Path) -> np.ndarray:
    """Load an image file into a numpy array.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the image file.

    Returns
    -------
    numpy.ndarray
        Loaded image array.
    """
    raise NotImplementedError
