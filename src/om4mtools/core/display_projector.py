"""Projection of phase/displacement fields for display."""

from __future__ import annotations

import numpy as np


class DisplayProjector:
    """Project a phase or displacement field into a displayable image.

    Parameters
    ----------
    colormap : str, optional
        Name of the colormap to use when rendering the field. Defaults to
        ``"viridis"``.
    """

    def __init__(self, colormap: str = "viridis") -> None:
        self.colormap = colormap

    def project(self, field: np.ndarray) -> np.ndarray:
        """Render a scalar field as an RGB image.

        Parameters
        ----------
        field : numpy.ndarray
            2-D scalar field (e.g. an unwrapped phase or displacement map).

        Returns
        -------
        numpy.ndarray
            RGB image of shape ``(*field.shape, 3)`` with values in
            ``[0, 255]``.
        """
        raise NotImplementedError
