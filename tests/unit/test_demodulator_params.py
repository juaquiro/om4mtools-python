"""Tests for `om4mtools.core.demodulator_params.DemodParams`."""

from __future__ import annotations

import math

import numpy as np
import pytest

from om4mtools.core.demodulator_params import DemodParams

# ---------------------------------------------------------------------------
# 1) Default values
# ---------------------------------------------------------------------------


@pytest.mark.smoke
def test_default_values() -> None:
    """A fresh `DemodParams()` has the documented defaults."""
    p = DemodParams()

    assert p.roi_mask is None
    assert p.z_list is None
    assert p.n_igrams is None
    assert p.roi_norm_th == 0.15
    assert p.delta_list is None


@pytest.mark.smoke
def test_slots_reject_unknown_attribute() -> None:
    """`slots=True`: a typo'd field name raises instead of being created."""
    p = DemodParams()

    with pytest.raises(AttributeError):
        p.n_intgrams = 4  # typo of n_igrams


# ---------------------------------------------------------------------------
# 2) _validate(): per-field checks, on assignment and on construction
# ---------------------------------------------------------------------------


@pytest.mark.smoke
@pytest.mark.parametrize("value", [-0.1, 1.1])
def test_roi_norm_th_out_of_range_raises(value: float) -> None:
    p = DemodParams()

    with pytest.raises(ValueError, match=r"roi_norm_th must be in \[0, 1\]"):
        p.roi_norm_th = value


@pytest.mark.smoke
@pytest.mark.parametrize("value", [0.0, 0.5, 1.0])
def test_roi_norm_th_in_range_accepted(value: float) -> None:
    p = DemodParams()
    p.roi_norm_th = value

    assert p.roi_norm_th == value


@pytest.mark.smoke
@pytest.mark.parametrize("value", [0, -3])
def test_n_igrams_below_one_raises(value: int) -> None:
    p = DemodParams()

    with pytest.raises(ValueError, match="n_igrams must be at least 1"):
        p.n_igrams = value


@pytest.mark.smoke
@pytest.mark.parametrize("value", [2.5, 4.0, "3", True, [4]])
def test_n_igrams_not_integer_raises(value: object) -> None:
    """Floats (even integral ones), strings, bools and sequences are rejected."""
    p = DemodParams()

    with pytest.raises(TypeError, match="n_igrams must be an int"):
        p.n_igrams = value


@pytest.mark.smoke
@pytest.mark.parametrize("value", [4, np.int64(4), np.uint8(4)])
def test_n_igrams_integer_normalized_to_int(value: object) -> None:
    """Python and NumPy integers are accepted and stored as a plain `int`."""
    p = DemodParams()
    p.n_igrams = value

    assert p.n_igrams == 4
    assert type(p.n_igrams) is int


@pytest.mark.smoke
@pytest.mark.parametrize("value", [5, ["a", "b"], [0.0, None]])
def test_delta_list_not_numeric_sequence_raises(value: object) -> None:
    """Non-iterables and sequences with non-numeric items are rejected."""
    p = DemodParams()

    with pytest.raises(TypeError, match="delta_list must be a sequence of numbers"):
        p.delta_list = value


@pytest.mark.smoke
def test_delta_list_normalized_to_tuple_of_floats() -> None:
    p = DemodParams()
    p.delta_list = [0, 1, 2]

    assert p.delta_list == (0.0, 1.0, 2.0)
    assert isinstance(p.delta_list, tuple)
    assert all(isinstance(d, float) for d in p.delta_list)


@pytest.mark.smoke
@pytest.mark.parametrize("value", [[[True, False]], "mask", 1])
def test_roi_mask_not_ndarray_raises(value: object) -> None:
    p = DemodParams()

    with pytest.raises(TypeError, match="roi_mask must be a numpy array"):
        p.roi_mask = value


@pytest.mark.smoke
@pytest.mark.parametrize("dtype", [np.uint8, np.int64, np.float64])
def test_roi_mask_not_boolean_raises(dtype: type) -> None:
    p = DemodParams()

    with pytest.raises(TypeError, match="roi_mask must be a boolean array"):
        p.roi_mask = np.ones((4, 4), dtype=dtype)


@pytest.mark.smoke
@pytest.mark.parametrize("shape", [(), (4,), (2, 3, 4, 5)])
def test_roi_mask_wrong_ndim_raises(shape: tuple[int, ...]) -> None:
    p = DemodParams()

    with pytest.raises(ValueError, match="roi_mask must be 2D or 3D"):
        p.roi_mask = np.ones(shape, dtype=bool)


@pytest.mark.smoke
@pytest.mark.parametrize("shape", [(4, 5), (4, 5, 3)])
def test_roi_mask_2d_3d_accepted(shape: tuple[int, ...]) -> None:
    p = DemodParams()
    mask = np.ones(shape, dtype=bool)
    p.roi_mask = mask

    np.testing.assert_array_equal(p.roi_mask, mask)


@pytest.mark.smoke
def test_roi_mask_stored_as_copy() -> None:
    """Modifying the caller's array afterwards does not affect the params."""
    p = DemodParams()
    mask = np.zeros((4, 4), dtype=bool)
    p.roi_mask = mask

    mask[0, 0] = True

    assert p.roi_mask is not mask
    assert not p.roi_mask[0, 0]


@pytest.mark.smoke
@pytest.mark.parametrize(
    ("field", "value", "exc"),
    [
        ("roi_norm_th", 2.0, ValueError),
        ("n_igrams", 0, ValueError),
        ("delta_list", 5, TypeError),
        ("roi_mask", np.ones(4, dtype=bool), ValueError),
    ],
)
def test_validation_runs_on_construction(field: str, value: object, exc: type) -> None:
    """`_validate` also runs for constructor arguments, not only assignment."""
    with pytest.raises(exc):
        DemodParams(**{field: value})


# ---------------------------------------------------------------------------
# 3) verify_params(): cross-field consistency
# ---------------------------------------------------------------------------


@pytest.mark.smoke
def test_verify_params_n_igrams_not_set_raises() -> None:
    p = DemodParams(delta_list=[0.0, math.pi])

    with pytest.raises(ValueError, match="n_igrams must be set"):
        p.verify_params()


@pytest.mark.smoke
def test_verify_params_delta_list_not_set_raises() -> None:
    p = DemodParams(n_igrams=2)

    with pytest.raises(ValueError, match="delta_list must be set"):
        p.verify_params()


@pytest.mark.smoke
def test_verify_params_length_mismatch_raises() -> None:
    p = DemodParams(n_igrams=6, delta_list=[0.0, 1.0, 2.0, 3.0, 4.0])

    with pytest.raises(ValueError, match="delta_list has 5 entries, but n_igrams is 6"):
        p.verify_params()


@pytest.mark.smoke
def test_verify_params_consistent_passes() -> None:
    p = DemodParams(n_igrams=4, delta_list=[0.0, math.pi / 2, math.pi, 3 * math.pi / 2])

    p.verify_params()  # must not raise
