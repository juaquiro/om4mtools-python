"""Shared type aliases for om4mtools."""

from typing import Any

import numpy as np
import numpy.typing as npt

RealArray = npt.NDArray[np.integer[Any] | np.floating[Any]]  # uint8, uint16, float64, float32
ComplexArray = npt.NDArray[np.complex128]
BoolArray = npt.NDArray[np.bool]
