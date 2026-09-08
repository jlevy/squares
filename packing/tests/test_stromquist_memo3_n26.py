"""Independent rational-polynomial and oriented-half-plane checks of Memo III n=26."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from cases.stromquist.memo3_n26 import build, comparisons, parameters

type Polynomial = tuple[Fraction, Fraction, Fraction]
type ExactPoint = tuple[Polynomial, Polynomial]
type ExactSquare = tuple[ExactPoint, ...]

ZERO: Polynomial = (Fraction(0), Fraction(0), Fraction(0))
ONE: Polynomial = (Fraction(1), Fraction(0), Fraction(0))
ROOT: Polynomial = (Fraction(0), Fraction(1), Fraction(0))
ROOT_LO = Fraction("5.6506291914393882188808009674")
ROOT_HI = Fraction("5.6506291914393882188808009675")


def _plus(a: Polynomial, b: Polynomial) -> Polynomial:
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def _minus(a: Polynomial, b: Polynomial) -> Polynomial:
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


def _times(a: Polynomial, b: Polynomial) -> Polynomial:
    """Direct cubic reduction, without importing the production field arithmetic."""
    degree3 = a[1] * b[2] + a[2] * b[1]
    degree4 = a[2] * b[2]
    return (
        a[0] * b[0] + 112 * degree3 + 1568 * degree4,
        a[0] * b[1] + a[1] * b[0] - 67 * degree3 - 826 * degree4,
        a[0] * b[2] + a[1] * b[1] + a[2] * b[0] + 14 * degree3 + 129 * degree4,
    )


def _sign(value: Polynomial) -> int:
    """Exact zero or interval exclusion using a fixed independently checked bracket."""
    if value == ZERO:
        return 0
    low = high = Fraction(0)
    for coefficient in reversed(value):
        products = low * ROOT_LO, low * ROOT_HI, high * ROOT_LO, high * ROOT_HI
        low, high = min(products) + coefficient, max(products) + coefficient
    assert low > 0 or high < 0, "independent rational bracket did not decide this sign"
    return 1 if low > 0 else -1


def _orientation(a: ExactPoint, b: ExactPoint, point: ExactPoint) -> Polynomial:
    return _minus(
        _times(_minus(b[0], a[0]), _minus(point[1], a[1])),
        _times(_minus(b[1], a[1]), _minus(point[0], a[0])),
    )


def _distance2(a: ExactPoint, b: ExactPoint) -> Polynomial:
    dx, dy = _minus(b[0], a[0]), _minus(b[1], a[1])
    return _plus(_times(dx, dx), _times(dy, dy))


def _separation(a: ExactSquare, b: ExactSquare) -> int | None:
    """Seek a polygon edge with the other polygon in its exterior half-plane."""
    contact = False
    for piece, other in ((a, b), (b, a)):
        for index in range(4):
            left, right = piece[index], piece[(index + 1) % 4]
            orientations = tuple(_sign(_orientation(left, right, point)) for point in other)
            if max(orientations) < 0:
                return 1
            if max(orientations) == 0:
                contact = True
    return 0 if contact else None


def _coordinates() -> tuple[ExactSquare, ...]:
    pieces, _, _ = build()
    return tuple(
        tuple(
            ((x.coeffs[0], x.coeffs[1], x.coeffs[2]), (y.coeffs[0], y.coeffs[1], y.coeffs[2]))
            for x, y in piece
        )
        for piece in pieces
    )


def test_independent_field_preconditions_and_reduction() -> None:
    def cubic(value: Fraction) -> Fraction:
        return value**3 - 14 * value**2 + 67 * value - 112

    assert cubic(ROOT_LO) < 0 < cubic(ROOT_HI)
    # This cubic has no root over F_3, hence is irreducible over Q.
    assert all((value**3 - 14 * value**2 + 67 * value - 112) % 3 for value in range(3))
    # 3*p'(x) = (3*x - 14)^2 + 5 > 0: there is only one real root.
    assert 28**2 - 4 * 3 * 67 == -20
    assert _times(_times(ROOT, ROOT), ROOT) == (Fraction(112), Fraction(-67), Fraction(14))
    assert _times(_times(ROOT, ROOT), _times(ROOT, ROOT)) == (
        Fraction(1568),
        Fraction(-826),
        Fraction(129),
    )


def test_source_domino_parameters_reduce_to_exact_cubic_coordinates() -> None:
    _, _, field = build()
    values = parameters(field)
    expected = {
        "sin_theta": (-9, Fraction(9, 2), Fraction(-1, 2)),
        "cos_theta": (16, Fraction(-11, 2), Fraction(1, 2)),
        "tan_theta": (Fraction(-43, 8), Fraction(7, 4), Fraction(-1, 8)),
        "x1": (-3, 1, 0),
        "x2": (47, Fraction(-33, 2), Fraction(3, 2)),
        "y2": (-21, Fraction(25, 2), Fraction(-3, 2)),
        "dx": (-39, Fraction(31, 2), Fraction(-3, 2)),
        "dy": (-1, Fraction(-5, 2), Fraction(1, 2)),
    }
    assert {name: tuple(values[name].coeffs) for name in expected} == expected
    assert field.decimal(values["side"], 20).startswith("5.65062919143938821888")
    assert field.decimal(values["tan_theta"], 15).startswith("0.522399802625560")


def test_all_shapes_walls_and_325_pairs_pass_the_independent_oracle() -> None:
    pieces = _coordinates()
    assert len(pieces) == 26
    wall_contacts = 0
    for piece in pieces:
        for index in range(4):
            assert _distance2(piece[index], piece[(index + 1) % 4]) == ONE
            assert (
                _sign(
                    _orientation(piece[index], piece[(index + 1) % 4], piece[(index + 2) % 4])
                )
                > 0
            )
        assert _distance2(piece[0], piece[2]) == _plus(ONE, ONE)
        assert _distance2(piece[1], piece[3]) == _plus(ONE, ONE)
        for point in piece:
            for value in point:
                for gap in (value, _minus(ROOT, value)):
                    assert _sign(gap) >= 0
                    wall_contacts += _sign(gap) == 0
    separations = [_separation(a, b) for a, b in combinations(pieces, 2)]
    assert len(separations) == 325
    assert None not in separations
    assert separations.count(0) == 41
    assert separations.count(1) == 284
    assert wall_contacts == 38


def test_independent_oracle_rejects_overlap_and_a_smaller_container() -> None:
    pieces = _coordinates()
    assert _separation(pieces[14], pieces[14]) is None
    # A small motion of one domino square into its neighbour preserves its shape.
    dx = tuple(value / 1_000_000 for value in _minus(pieces[15][0][0], pieces[14][0][0]))
    dy = tuple(value / 1_000_000 for value in _minus(pieces[15][0][1], pieces[14][0][1]))
    moved = tuple(
        (_plus(x, (dx[0], dx[1], dx[2])), _plus(y, (dy[0], dy[1], dy[2])))
        for x, y in pieces[14]
    )
    assert _separation(moved, pieces[15]) is None
    smaller = _minus(ROOT, (Fraction(1, 1_000_000), Fraction(0), Fraction(0)))
    assert any(
        _sign(_minus(smaller, value)) < 0
        for piece in pieces
        for point in piece
        for value in point
    )


def test_current_bound_is_strictly_smaller_and_the_historical_comparisons_are_exact() -> None:
    _, _, field = build()
    compared = comparisons(field)
    assert compared["friedman"]["p_at_comparator_in_q_sqrt2"] == ["-175/8", "123/8"]
    # p((7+3sqrt(2))/2) = (-175+123sqrt(2))/8 < 0, using integer arithmetic.
    assert 2 * 123**2 < 175**2
    assert compared["friedman"]["p_at_comparator_sign"] == -1
    assert compared["gobel"]["p_at_comparator_sign"] == 1
    assert compared["stenlund"]["p_at_comparator_sign"] == 1
    gap = compared["friedman"]["memo_minus_comparator_approx"]
    assert isinstance(gap, float)
    assert gap > 0.0293
    assert gap < 0.0294


def test_cli_emits_and_retains_verified_evidence(tmp_path: Path) -> None:
    output = tmp_path / "memo3-n26.json"
    completed = subprocess.run(
        [sys.executable, "-m", "cases.stromquist.memo3_n26", "--output", str(output)],
        cwd=Path(__file__).resolve().parents[1],
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.stdout == output.read_text()
    retained = Path(__file__).resolve().parents[1] / "cases/stromquist/memo3-n26.json"
    assert completed.stdout == retained.read_text()
    record = json.loads(completed.stdout)
    assert record["construction_verified"] is True
    assert record["optimality_proved"] is False
    assert record["improves_current_best_known"] is False
    assert record["checks"]["all_pairs"] == 325
    assert record["checks"]["duplicate_rejected"] is True
    assert record["checks"]["container_shrunk_by_1e_minus_6_rejected"] is True
