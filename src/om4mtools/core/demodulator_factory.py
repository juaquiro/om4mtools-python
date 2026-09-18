from .demodulator import Demodulator
from .demodulator_types import DemodulatorTypes
from .demodulator_PSA4 import DemodulatorPSA4


class DemodulatorFactory:
    def create(demodulator_type: DemodulatorTypes, **kwargs ) -> Demodulator
        if demodulator_type == DemodulatorTypes.PSA4:
            return(DemodulatorPSA4)

        else:
            raise ValueError(
                f"Unknown demodulator type: {demodulator_type}"
            )




