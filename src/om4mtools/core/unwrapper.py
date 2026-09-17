"""Phase unwrapping."""

from __future__ import annotations

import numpy as np


class Unwrapper:
    """Unwrap a wrapped phase map into a continuous phase map.

    Parameters
    ----------
    method : str, optional
        Unwrapping algorithm to use. Defaults to ``"quality_guided"``.
    """

    def __init__(self, method: str = "quality_guided") -> None:
        self.method = method

    def unwrap(self, wrapped_phase: np.ndarray) -> np.ndarray:
        """Unwrap a wrapped phase map.

        Parameters
        ----------
        wrapped_phase : numpy.ndarray
            2-D wrapped phase map with values in ``(-pi, pi]``.

        Returns
        -------
        numpy.ndarray
            Continuous (unwrapped) phase map, same shape as `wrapped_phase`.
        """
        raise NotImplementedError
