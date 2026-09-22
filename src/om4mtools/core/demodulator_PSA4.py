import math
from collections.abc import Sequence

import numpy as np

from .demodulator import ComplexArray, Demodulator, RealArray


class DemodulatorPSA4(Demodulator):

    def _setup(self) -> None:
        self.n_igrams = 4
        self.delta_list = [0.0, math.pi / 2, math.pi, 3 * math.pi / 2]

    def process(self, igram_list: Sequence[RealArray]) -> list[ComplexArray]:
        if len(igram_list) != self.n_igrams:
            raise ValueError(
                f"DemodulatorPSA4.process expects {self.n_igrams} "
                f"fringe patterns, got {len(igram_list)}"
            )
        igrams = [np.asarray(ig, dtype=np.float64) for ig in igram_list]
        raise NotImplementedError

    