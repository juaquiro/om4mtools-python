from abc import ABC, abstractmethod
from collections.abc import Sequence

from .types import RealArray
from .demodulator_params import DemodParams


class Demodulator(ABC):
    """abstract class defining the interface of any Demodulator object"""

    def __init__(self) -> None:
        self.demod_params = DemodParams()
        self._setup()

    @abstractmethod
    def _setup(self) -> None:
        """All Demodulators must implement this function, where typically the
        demod_params are initialized"""
        ...

    @abstractmethod
    def process(self, igram_list: Sequence[RealArray]) -> None:
        """Demodulate interferograms.

        All demodulators must implement this function. The input is a
        sequence of RealArray. The method does not return a value; the
        resulting complex phasor(s) are stored in `self.demod_params.z_list`
        as a tuple of ComplexArray. Each demodulator has a different output
        signature (number and shape of phasors), but the result is always
        written to `demod_params.z_list`.
        Input is `Sequence` (covariant, read-only) so callers can pass
        a list, tuple, or any ordered collection without a forced copy.
        """
        ...