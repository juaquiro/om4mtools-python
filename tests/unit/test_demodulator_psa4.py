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
    synthetic_igrams_8x9: tuple[list[np.ndarray], float, np.ndarray],
) -> None:
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


@pytest.mark.smoke
def test_process_default_roi_is_whole_image(
    synthetic_igrams_8x9: tuple[list[np.ndarray], float, np.ndarray],
) -> None:
    """With no `inp_roi_mask`, `out_roi_mask` is all-True and the input stays None.

    Run:
        pytest tests/unit/test_demodulator_psa4.py::test_process_default_roi_is_whole_image -v
    """
    igrams, _, _ = synthetic_igrams_8x9
    demod = DemodulatorPSA4()

    demod.process(igrams)

    assert demod.demod_params.inp_roi_mask is None
    out_roi_mask = demod.demod_params.out_roi_mask
    assert out_roi_mask is not None
    assert out_roi_mask.shape == (8, 9)
    assert out_roi_mask.all()
    (z,) = demod.demod_params.z_list
    assert np.isfinite(z).all()


@pytest.mark.smoke
def test_process_nan_outside_roi(
    synthetic_igrams_8x9: tuple[list[np.ndarray], float, np.ndarray],
) -> None:
    """`z` is NaN outside `inp_roi_mask`, which `process()` does not modify.

    Run:
        pytest tests/unit/test_demodulator_psa4.py::test_process_nan_outside_roi -v
    """
    igrams, b, phi = synthetic_igrams_8x9
    mask = np.zeros((8, 9), dtype=bool)
    mask[2:6, 3:7] = True
    demod = DemodulatorPSA4()
    demod.demod_params.inp_roi_mask = mask

    demod.process(igrams)

    np.testing.assert_array_equal(demod.demod_params.inp_roi_mask, mask)
    np.testing.assert_array_equal(demod.demod_params.out_roi_mask, mask)
    (z,) = demod.demod_params.z_list
    assert np.isnan(z[~mask]).all()
    np.testing.assert_allclose(z[mask], (2.0 * b * np.exp(1j * phi))[mask], rtol=1e-10)


@pytest.mark.smoke
def test_process_twice_with_different_shapes(
    synthetic_igrams_8x9: tuple[list[np.ndarray], float, np.ndarray],
) -> None:
    """A second `process()` call with a new igram shape builds a new default mask.

    Run:
        pytest tests/unit/test_demodulator_psa4.py::test_process_twice_with_different_shapes -v
    """
    igrams, _, _ = synthetic_igrams_8x9
    demod = DemodulatorPSA4()

    demod.process(igrams)
    demod.process([ig[:5, :6] for ig in igrams])

    assert demod.demod_params.inp_roi_mask is None
    assert demod.demod_params.out_roi_mask.shape == (5, 6)
    (z,) = demod.demod_params.z_list
    assert z.shape == (5, 6)
