"""The exact L-shaped packings behind Ryu's c*(k) <= 8 ceil(sqrt(k-4)) - 1, and refusals."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction

from cases.asymptotic.ryu_upper_l_packing import (
    build,
    ceil_sqrt,
    check_formulas,
    check_packings,
    count,
    defects,
    theorem_14_table,
)


def test_every_small_packing_is_valid_with_n_k_b_squares() -> None:
    (check,) = check_packings(10)
    assert check.holds, check.value
    assert check.value.startswith("44 packings")


def test_the_counting_statements_hold_on_a_short_range() -> None:
    checks = check_formulas(300)
    assert all(check.holds for check in checks), [c for c in checks if not c.holds]
    assert len(checks) == 7


def test_theorem_14_is_tight_for_the_construction_where_the_review_says() -> None:
    tight = [row["k"] for row in theorem_14_table() if row["construction"] == row["bound"]]
    assert tight == [13, 18, 19, 20, *range(23, 31)]
    assert all(row["construction"] <= row["bound"] for row in theorem_14_table())


def test_a_square_moved_into_its_neighbour_is_refused() -> None:
    packing = build(9, 3)
    (a, b, c, d), *rest = packing.squares
    shift = Fraction(1, 10**6)
    moved = (
        (a[0] + shift, a[1]),
        (b[0] + shift, b[1]),
        (c[0] + shift, c[1]),
        (d[0] + shift, d[1]),
    )
    found = defects(replace(packing, squares=(moved, *rest)))
    assert any("overlap" in item for item in found)


def test_one_square_too_many_is_refused() -> None:
    packing = build(9, 3)
    found = defects(replace(packing, squares=(*packing.squares, packing.squares[-1])))
    assert any("squares, N(k,b)" in item for item in found)


def test_a_side_of_k_is_refused() -> None:
    packing = build(9, 3)
    assert "S >= k" in defects(replace(packing, side=Fraction(9)))


def test_exact_ceilings_and_counts() -> None:
    assert [ceil_sqrt(n) for n in (0, 1, 2, 4, 5, 9, 10)] == [0, 1, 2, 2, 3, 3, 4]
    assert count(2, 2) == 0
    assert count(13, 3) == 13 * 13 - 24
