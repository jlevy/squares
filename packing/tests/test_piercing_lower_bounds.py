"""Bašić and Slivková's piercing bound, replayed against the paper's own numbers."""

from __future__ import annotations

import itertools
import json
from decimal import Decimal
from pathlib import Path

import pytest
import sympy

from devtools import check_piercing_lower_bounds as piercing

#: Table 1 of the paper: Theorem 3's bound on the piercing number at integer sides 1..20.
#: Theorem 7 agrees with it at every integer side, where its floor plus two is Theorem 3's
#: ceiling plus one because the lattice's row count is never an integer there.
TABLE_1 = (
    1,
    4,
    9,
    16,
    25,
    36,
    49,
    72,
    90,
    110,
    132,
    156,
    182,
    224,
    255,
    288,
    323,
    360,
    399,
    440,
)


def test_the_bound_reproduces_the_papers_table_at_integer_sides() -> None:
    assert tuple(piercing.pierce_bound(sympy.Integer(n)) for n in range(1, 21)) == TABLE_1


def test_theorem_10_and_the_case_it_did_not_state() -> None:
    sqrt2, sqrt3 = sympy.sqrt(2), sympy.sqrt(3)
    assert sympy.simplify(piercing.piercing_bound(61) - (7 * sqrt3 / 2 + 2 * sqrt2 - 1)) == 0
    assert sympy.simplify(piercing.piercing_bound(37) - (5 * sqrt3 / 2 + 2 * sqrt2 - 1)) == 0
    assert piercing.floor_decimal(piercing.piercing_bound(61)) == "7.89060495123"
    assert piercing.floor_decimal(piercing.piercing_bound(37)) == "6.15855414366"


def test_just_below_the_bound_too_few_points_pierce_and_at_it_enough_do() -> None:
    for n in (37, 61):
        bound = piercing.piercing_bound(n)
        assert piercing.pierce_bound(bound - sympy.Rational(1, 10**9)) <= n - 1
        assert piercing.pierce_bound(bound) >= n


def test_a_printed_bound_is_rounded_down() -> None:
    assert piercing.floor_decimal(sympy.Rational(2, 3), 4) == "0.6666"
    assert piercing.floor_decimal(sympy.Integer(6)) == "6"


def test_a_floor_within_a_tiny_distance_of_an_integer_is_decided_exactly() -> None:
    # Review A2 on jlevy/squares#305: `5 - (√2 - 1)^170` is within 10^-64 of 5, and
    # `nsimplify` at 30 digits used to floor it to 5.
    near = 5 - sympy.expand((sympy.sqrt(2) - 1) ** 170)
    assert piercing.exact_floor(near) == 4
    assert piercing.exact_sign(near - 5) == -1
    assert piercing.exact_floor(10 - near) == 5
    assert piercing.exact_floor(sympy.Integer(5)) == 5
    assert piercing.exact_sign(sympy.sqrt(8) - 2 * sympy.sqrt(2)) == 0


def test_a_value_outside_exact_surds_is_refused() -> None:
    with pytest.raises(ArithmeticError, match="not an exact surd"):
        piercing.exact_floor(sympy.Float("2.5"))
    with pytest.raises(ArithmeticError, match="not an exact surd"):
        piercing.exact_floor(sympy.pi)


def test_the_steps_are_exact_and_strictly_increasing() -> None:
    points = piercing.steps(12)
    assert all(not point.atoms(sympy.Float) for point in points)
    assert all(
        piercing.exact_sign(right - left) > 0 for left, right in itertools.pairwise(points)
    )


def test_the_retained_survey_is_current() -> None:
    retained = json.loads(piercing.RESULT.read_text(encoding="utf-8"))
    # Registered as T-087 on 2026-10-03: the bound holds the verified floor at the two
    # cases where it beat the floor held before, and beats it nowhere. It also reaches the
    # integer floor at the cases its Theorem 9 reproduces (s(8) = 3 up to s(48) = 7) and
    # at the perfect squares, which other results already hold. Since the merge of the
    # same day it holds neither n = 37 nor n = 61: replayed bounds recorded in parallel
    # stand above it there, 161/25 (T-069; 2599/400, T-178, since 2026-11-02) and
    # s(61) = 8 (T-063).
    assert retained["holds"] == [
        4,
        8,
        9,
        15,
        16,
        23,
        24,
        25,
        34,
        35,
        36,
        46,
        47,
        48,
        49,
    ]
    assert retained["improves"] == []
    assert retained == piercing.survey(range(2, len(retained["cases"]) + 2))


def test_holds_and_improves_are_exact_not_float(monkeypatch: pytest.MonkeyPatch) -> None:
    """Floors a float cannot tell from the bound's decimal are told apart exactly.

    `7.89060495123` is the bound at `n = 61` rounded down; a record 1e-21 either side of
    it is the same float, and until 2026-10-04 the survey compared floats.
    """
    printed = piercing.floor_decimal(piercing.piercing_bound(61))
    assert printed == "7.89060495123"
    for record, holds, improves in (
        (printed, True, False),
        ("7.890604951230000000001", False, False),
        ("7.890604951229999999999", False, True),
    ):
        assert float(record) == float(printed)
        monkeypatch.setattr(piercing, "verified_floor", lambda _n, value=record: Decimal(value))
        (row,) = piercing.survey([61])["cases"]
        assert (row["holds"], row["improves"]) == (holds, improves), record
        assert row["verified_lower"] == record


def test_a_verified_floor_that_is_not_a_decimal_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "n-007.md").write_text(
        "---\npacking:\n  verified_lower_bound:\n    value: '2 + sqrt(2)'\n---\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(piercing, "FRONTIER", tmp_path)
    with pytest.raises(ValueError, match="not a decimal"):
        piercing.verified_floor(7)
