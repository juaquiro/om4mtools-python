"""Tests for `om4mtools.core.demodulator_PSA4`."""

from __future__ import annotations

import numpy as np
import pytest

from om4mtools.core.demodulator_PSA4 import DemodulatorPSA4

@pytest.fixture
def synthetic_igrams_8x9() -> tuple[list[np.ndarray], float, np.ndarray]:
    """Generate 4 synthetic 8x9 PSA4 interferograms with a known phase.

    Builds interferograms of the form ``I_n = a + b * cos(phi + delta_n)``
    over an 8x9 grid, for the PSA4 phase steps
    ``delta_n in {0, pi/2, pi, 3*pi/2}``. `phi` and `b` are chosen so the
    phasor `DemodulatorPSA4.process` should recover is known exactly:
    ``z = i0 - i2 + j*(i3 - i1) = 2*b*exp(j*phi)``.

    Returns
    -------
    igrams : list of 4 (8, 9) float64 arrays, in i0..i3 order.
    b : float
        Modulation amplitude used to build the interferograms.
    phi : (8, 9) array
        The known phase used to build the interferograms.

    Run:
        pytest tests/unit/test_demodulator_psa4.py::test_process_recovers_known_phasor -v
    """
    rows = np.arange(8).reshape(-1, 1)
    cols = np.arange(9).reshape(1, -1)

    a = 1.0
    b = 0.5
    phi = 2.0 * np.pi * (rows / 8 + cols / 9) - np.pi  # in [-pi, pi)

    delta_list = (0.0, np.pi / 2, np.pi, 3 * np.pi / 2)
    igrams = [a + b * np.cos(phi + delta) for delta in delta_list]

    return igrams, b, phi


@pytest.mark.smoke
def test_process_recovers_known_phasor(
    synthetic_igrams_8x9: tuple[list[np.ndarray], float, np.ndarray], ) -> None:
    """DemodulatorPSA4.process() recovers the expected 2*b*exp(j*phi) phasor.

    Run:
        pytest tests/unit/test_demodulator_psa4.py::test_process_recovers_known_phasor -v
    """
    igrams, b, phi = synthetic_igrams_8x9
    demod = DemodulatorPSA4()

    demod.process(igrams)

    assert demod.demod_params.z_list is not None
    (z,) = demod.demod_params.z_list
    assert z.shape == (8, 9)

    z_expected = 2.0 * b * np.exp(1j * phi)
    np.testing.assert_allclose(z, z_expected, rtol=1e-10, atol=1e-12)
