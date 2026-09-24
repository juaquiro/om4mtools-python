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
    """Rescale ``image`` to the [0, 1] range.
 
    Shared normalization step used across several demodulation and
    display-generation routines. Not part of the public API because
    its exact behavior (e.g. how it handles a constant image, or
    values outside the observed min/max) is an implementation detail
    other core/ code relies on, not a documented contract for users.
 
    Parameters
    ----------
    image : RealArray
        Input array.
 
    Returns
    -------
    RealArray
        Normalized array, same shape as ``image``.
    """
    # TODO: implement (e.g. (image - image.min()) / (image.max() -
    # image.min()), with a defined behavior for the constant-image
    # edge case).
    raise NotImplementedError



