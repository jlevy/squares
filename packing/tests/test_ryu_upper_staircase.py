"""The staircase end packing of Ryu's Lemma 7.3, built and decided exactly, and refusals."""

from __future__ import annotations

import pytest
from gmpy2 import mpq

from cases.asymptotic.ryu_upper_staircase import in_window, run


@pytest.mark.parametrize(("b", "y", "pairs"), [(400, "41", 3279), (1600, "103", 19784)])
def test_small_end_packings_are_valid_and_within_both_bounds(
    b: int, y: str, pairs: int
) -> None:
    result = run(b, y)
    assert result.passed
    assert result.in_window
    assert result.box_pairs == pairs
    assert result.uncovered <= result.b_star <= result.phi_bound


def test_a_tilt_one_grid_step_below_t_star_is_refused() -> None:
    result = run(400, "41", tilt_offset=-1)
    assert result.bad_containment > 0
    assert not result.passed


def test_the_window_is_decided_exactly() -> None:
    # kappa b^{2/3} = 3/4 * 1000^{2/3} = 75 exactly, so the window is [75, 77].
    assert in_window(1000, mpq(75))
    assert in_window(1000, mpq(77))
    assert not in_window(1000, mpq(75) - mpq(1, 10**30))
    assert not in_window(1000, mpq(77) + mpq(1, 10**30))
