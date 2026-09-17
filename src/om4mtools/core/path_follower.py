"""Fringe path tracing."""

from __future__ import annotations

import numpy as np


class PathFollower:
    """Trace fringe skeleton paths through an unwrapped phase map.

    Parameters
    ----------
    step_size : float, optional
        Step size, in pixels, used while tracing a path. Defaults to ``1.0``.
    """

    def __init__(self, step_size: float = 1.0) -> None:
        self.step_size = step_size

    def follow(self, phase: np.ndarray, seed: tuple[int, int]) -> np.ndarray:
        """Trace a fringe path starting from a seed point.

        Parameters
        ----------
        phase : numpy.ndarray
            2-D unwrapped phase map.
        seed : tuple[int, int]
            ``(row, col)`` pixel coordinates to start tracing from.

        Returns
        -------
        numpy.ndarray
            Array of shape ``(n, 2)`` with the ``(row, col)`` coordinates of
            the traced path.
        """
        raise NotImplementedError
