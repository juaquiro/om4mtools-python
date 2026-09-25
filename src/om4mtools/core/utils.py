"""Public utility functions for fringe-pattern generation and analysis."""

from .types import RealArray
import numpy as np

def peaks(n_rows: int, n_cols:int) -> RealArray:
    r"""Compute MATLAB's ``peaks`` test function on an n_rows x n_cols grid.

        Notes
        -----
        Samples

        .. math::
            z = 3(1-x)^2 e^{-x^2 - (y+1)^2}
                - 10\left(\frac{x}{5} - x^3 - y^5\right) e^{-x^2 - y^2}
                - \frac{1}{3} e^{-(x+1)^2 - y^2}

        over :math:`x, y \in [-3, 3]`.

        Parameters
        ----------
        n_rows : int
            Number of samples along y (rows of the output matrices).
        n_cols : int
            Number of samples along x (columns of the output matrices).

        Returns
        -------
        z : RealArray, shape (n_rows, n_cols)
            The peaks surface evaluated at (x, y).
        """

    x_vec = np.linspace(-3.0, 3.0, n_cols) # n_cols values -> varies along columns
    y_vec = np.linspace(-3.0, 3.0, n_rows) # n_rows values -> varies along rows
    x, y = np.meshgrid(x_vec, y_vec) 

    z = (
        3.0 * (1.0 - x) ** 2 * np.exp(-(x**2) - (y + 1.0) ** 2)
        - 10.0 * (x / 5.0 - x**3 - y**5) * np.exp(-(x**2) - y**2)
        - (1.0 / 3.0) * np.exp(-((x + 1.0) ** 2) - y**2)
    )

    return z


def generate_peaks_igram() -> RealArray:
    raise NotImplementedError