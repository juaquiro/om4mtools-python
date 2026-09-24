import math
from collections.abc import Sequence

import numpy as np

from .demodulator import ComplexArray, Demodulator, RealArray


class DemodulatorPSA4(Demodulator):

    def _setup(self) -> None:
        self.n_igrams = 4
        self.delta_list = [0.0, math.pi / 2, math.pi, 3 * math.pi / 2]

    def process(self, igram_list: Sequence[RealArray]) -> list[ComplexArray]:
        """
        4 step method as descrived in A.4.1 4-step least-squares PSA of [1]
        PSA4 is a special case of a 4 step equispaced PSA with 
        :math:`\delta_n = \omega_0 n` for :math:`n = 0, 1, 2, 3`, 
        with :math:`\omega_0 = \pi/2`
        
        References
        ----------
        .. [1] Servin, M., Quiroga, J. A., and Padilla, M., "Fringe Pattern
        Analysis for Optical Metrology: Theory, Algorithms, and
        Applications," Wiley-VCH (2014).
        """
        if len(igram_list) != self.n_igrams:
            raise ValueError(
                f"DemodulatorPSA4.process expects {self.n_igrams} "
                f"fringe patterns, got {len(igram_list)}"
            )
        igrams = [np.asarray(ig, dtype=np.float64) for ig in igram_list]

        i0, i1, i2, i3 = igrams

        z= i0 - i2 + 1j*(i3 - i1)

        return (z,)  # comlex phasor tuple, trailing comma matters — this is a 1-tuple
        
    