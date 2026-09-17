"""om4mtools: fringe-pattern processing library (OM4M group).

The four core classes are the primary, intended way to use this library.
The CLI, GUI, and web layers under `om4mtools.cli`, `om4mtools.gui`, and
`om4mtools.web` are optional convenience wrappers around the same API.
"""

from om4mtools.core import Demodulator, DisplayProjector, PathFollower, Unwrapper

__all__ = ["Demodulator", "Unwrapper", "PathFollower", "DisplayProjector"]

__version__ = "0.1.0"
