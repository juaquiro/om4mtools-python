"""Fringe-pattern demodulation."""

from __future__ import annotations

import numpy as np


class Demodulator:
    """Extract phase and amplitude from a fringe pattern.

    Parameters
    ----------
    carrier_frequency : tuple[float, float]
        Spatial carrier frequency ``(fx, fy)`` of the fringe pattern, in
        cycles per pixel.
    """

    def __init__(self, carrier_frequency: tuple[float, float]) -> None:
        self.carrier_frequency = carrier_frequency

    def demodulate(self, image: np.ndarray) -> np.ndarray:
        """Compute the wrapped phase map of a fringe pattern.

        Parameters
        ----------
        image : numpy.ndarray
            2-D grayscale fringe-pattern image.

        Returns
        -------
        numpy.ndarray
            Wrapped phase map, same shape as `image`, with values in
            ``(-pi, pi]``.
        """
        raise NotImplementedError
