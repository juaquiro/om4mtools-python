from abc import ABC, abstractmethod
from typing import Any
from collections.abc import Sequence

import numpy as np
import numpy.typing as npt

from .demodulator_params import DemodParams

FloatArray   = npt.NDArray[np.floating[Any]]                    # float32, float64, …
RealArray    = npt.NDArray[np.integer[Any] | np.floating[Any]]  # uint8, uint16, float64, …
ComplexArray = npt.NDArray[np.complex128]


class Demodulator(ABC):

    def __init__(self) -> None:
        self.demod_params = DemodParams()
        self._setup()

    @abstractmethod
    def _setup(self) -> None:
        ...

    @abstractmethod
    def process(self, igram_list: Sequence[RealArray]) -> list[ComplexArray]:
        ...

    









        



