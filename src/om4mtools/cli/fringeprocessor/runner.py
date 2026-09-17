"""Notebook-callable logic for the fringeprocessor tool.

No argv parsing or Typer here — see `main.py` for the CLI entry point.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from om4mtools.core import Demodulator, Unwrapper


def process_fringe_pattern(
    image_path: str | Path, carrier_frequency: tuple[float, float]
) -> np.ndarray:
    """Demodulate and unwrap a fringe-pattern image.

    Parameters
    ----------
    image_path : str or pathlib.Path
        Path to the fringe-pattern image.
    carrier_frequency : tuple[float, float]
        Spatial carrier frequency ``(fx, fy)``, in cycles per pixel.

    Returns
    -------
    numpy.ndarray
        Unwrapped phase map.
    """
    from om4mtools.io.images import load_image

    image = load_image(image_path)
    wrapped = Demodulator(carrier_frequency).demodulate(image)
    return Unwrapper().unwrap(wrapped)
