"""Smoke tests for the public core API."""

from __future__ import annotations

import pytest

from om4mtools import Demodulator, DisplayProjector, PathFollower, Unwrapper
from om4mtools.core import Demodulator as CoreDemodulator


@pytest.mark.smoke
def test_core_classes_are_reexported_at_top_level() -> None:
    """The four core classes are importable from both `om4mtools` and `om4mtools.core`."""
    assert Demodulator is CoreDemodulator
    assert all(cls is not None for cls in (Demodulator, Unwrapper, PathFollower, DisplayProjector))


@pytest.mark.smoke
def test_demodulator_is_constructible() -> None:
    """Demodulator can be constructed with a carrier frequency."""
    demod = Demodulator(carrier_frequency=(0.1, 0.0))
    assert demod.carrier_frequency == (0.1, 0.0)
