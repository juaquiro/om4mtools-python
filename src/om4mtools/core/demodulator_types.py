from enum import Enum, auto

class DemodulatorTypes(Enum):
    """List of available demodulators

    References
    ----------
    .. [1] Servin, M., Quiroga, J. A., and Padilla, M., "Fringe Pattern
       Analysis for Optical Metrology: Theory, Algorithms, and
       Applications," Wiley-VCH (2014).
    """
    # A.4.1 4-step least-squares PSA of [1].
    PSA4 = auto() 

