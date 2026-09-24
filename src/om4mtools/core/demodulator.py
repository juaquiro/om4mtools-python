from abc import ABC, abstractmethod
from typing import Any
from collections.abc import Sequence

from .types import RealArray, ComplexArray

from .demodulator_params import DemodParams




class Demodulator(ABC):

    def __init__(self) -> None:
        self.demod_params = DemodParams()
        self._setup()

    @abstractmethod
    def _setup(self) -> None:
        ...

    @abstractmethod
    def process(self, igram_list: Sequence[RealArray]) -> tuple[ComplexArray, ...]:
        """Demodulate interferograms.

        All demodulators must implement this function. 
        The input is a sequence of RealArray and the output is a tuple of CppmpexArray
        Each demodulator has a differnet output signature, but always returns a tuple
        Input is `Sequence` (covariant, read-only) so callers can pass
        a list, tuple, or any ordered collection without a forced copy.
        Output is `tuple` (immutable) so the result cannot be mutated
        by the caller after construction; subclasses returning exactly
        one array may narrow the return type to `tuple[ComplexArray]`.
        """
        ...

    









        



