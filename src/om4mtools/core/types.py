"""Shared type aliases for fringe-pattern data."""

from typing import Any

import numpy.typing as npt
import numpy as np

RealArray    = npt.NDArray[np.integer[Any] | np.floating[Any]]  # uint8, uint16, float64, float32
ComplexArray = npt.NDArray[np.complex128]


