"""Internal shared plumbing for core/.
 
Holds math helpers and algorithm-level building blocks used by other
core/ modules (Demodulator subclasses, Unwrapper, utils.py's public
functions, ...). Nothing here is part of the public API: signatures
can change without notice, and nothing in this file is re-exported
from core/__init__.py. If a function here needs to become directly
callable by users, move it to utils.py instead.
"""

from .types import ComplexArray, RealArray

 
def vortex_transform(igram: RealArray) -> ComplexArray:
    """Compute the vortex transform of a fringe pattern.
 
    Used internally as a building block by spatial-carrier
    demodulation methods (e.g. single-pattern demodulators that
    estimate the local phase via an isotropic quadrature operator).
 
    Parameters
    ----------
    image : RealArray
        Input fringe pattern.
 
    Returns
    -------
    ComplexArray
        Complex-valued transform, same shape as ``image``.
    """
    # TODO: implement the vortex transform. Placeholder keeps the
    # public/private module boundary in place before the algorithm
    # itself is written.
    raise NotImplementedError
 
 
def normalize(igram: RealArray) -> RealArray:
    r"""Normalize an interferogram to unit background and modulation.

    Notes
    -----
    Given an interferogram

    .. math::
        g = b + m \cos(\phi)

    with :math:`b` the background and :math:`m` the modulation, the
    normalization computes

    .. math::
        g_n = \cos(\phi) 

    i.e. the interferogram with :math:`b = 0` and :math:`m = 1`.

    Parameters
    ----------
    igram : RealArray
        The interferogram :math:`g`.

    Returns
    -------
    RealArray
        The normalized interferogram :math:`g_n = \cos(\phi)`.
    """
    
    raise NotImplementedError



