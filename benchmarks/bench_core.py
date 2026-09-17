"""asv performance regression benchmarks for `om4mtools.core`."""

from om4mtools.core import Demodulator


class DemodulatorConstruction:
    """Benchmark constructing a Demodulator."""

    def time_construct(self) -> None:
        Demodulator(carrier_frequency=(0.1, 0.0))
