import math
from collections.abc import Sequence

import numpy as np

from .demodulator import Demodulator
from .types import RealArray

class DemodulatorPSA4(Demodulator):
    r"""4-step least-squares phase-shifting algorithm (A.4.1 of [1]).

    Demodulates 4 equispaced phase-shifted interferograms with
    :math:`\delta_n = \omega_0 n` for :math:`n = 0, 1, 2, 3` and
    :math:`\omega_0 = \pi/2`, i.e. :math:`\delta_n \in \{0, \pi/2, \pi,
    3\pi/2\}`.

    References
    ----------
    .. [1] Servin, M., Quiroga, J. A., and Padilla, M., "Fringe Pattern
       Analysis for Optical Metrology: Theory, Algorithms, and
       Applications," Wiley-VCH (2014).
    """

    def _setup(self) -> None:
        r"""Configure the A.4.1 4-step least-squares PSA of [1].

        Notes
        -----
        The four phase steps are set as

        .. math::
            \delta_n = \omega_0 n, \quad n = 0, 1, 2, 3

        with :math:`\omega_0 = \pi/2`, giving
        :math:`\delta_n \in \{0, \pi/2, \pi, 3\pi/2\}`.

        References
                ----------
                .. [1] Servin, M., Quiroga, J. A., and Padilla, M., "Fringe Pattern
                Analysis for Optical Metrology: Theory, Algorithms, and
                Applications," Wiley-VCH (2014).
        """
        self.demod_params.n_igrams = 4
        self.demod_params.delta_list = [0.0, math.pi / 2, math.pi, 3 * math.pi / 2]

    def process(self, igram_list: Sequence[RealArray]) -> None:
        r"""
        4 step method as described in A.4.1 4-step least-squares PSA of [1]
        PSA4 is a special case of a 4 step equispaced PSA with 
        :math:`\delta_n = \omega_0 n` for :math:`n = 0, 1, 2, 3`, 
        with :math:`\omega_0 = \pi/2`
        
        References
        ----------
        .. [1] Servin, M., Quiroga, J. A., and Padilla, M., "Fringe Pattern
        Analysis for Optical Metrology: Theory, Algorithms, and
        Applications," Wiley-VCH (2014).
        """

        self.demod_params.verify_params()

        if len(igram_list) != self.demod_params.n_igrams:
            raise ValueError(
                f"DemodulatorPSA4.process expects {self.demod_params.n_igrams} "
                f"fringe patterns, got {len(igram_list)}"
            )

        
        igrams = [np.asarray(ig, dtype=np.float64) for ig in igram_list]

        i0, i1, i2, i3 = igrams

        z= i0 - i2 + 1j*(i3 - i1)

        self.demod_params.z_list = (z,)  # complex phasor tuple, trailing comma matters — this is a 1-tuple
        
    