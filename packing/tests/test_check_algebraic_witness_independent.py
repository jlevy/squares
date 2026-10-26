"""The second exact route over a number field, on fixtures decided by hand and on records.

The fixture is two unit squares in `Q(sqrt 2)`: an axis square in the lower-left corner
and a square turned 45 degrees whose left vertex touches the first square's right side
and whose lower vertex touches the floor, in a box of side `1 + sqrt 2`, which its right
vertex touches. Every contact is exact, so the route must decide each zero separation
as zero; pushing the turned square `10^-30` to the left, shrinking the box by
`10^-40` or lengthening a basis vector by `10^-50` makes a packing that is not one, and
both exact routes must refuse each. The record's algebraic houses must pass, and a field
whose stated polynomial factors over `Q` still decides signs, through the gcd.
"""

from __future__ import annotations

import copy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_algebraic_witness_independent as algebraic
from sqpack.witness import exact_verify
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
KNOWN_BEST = ROOT / "witnesses/known-best"
ROOT_TWO = ["0", "1"]
HALF_ROOT_TWO = ["0", "1/2"]


def fixture() -> dict[str, Any]:
    """Two touching squares in a box of side `1 + sqrt 2`, over `Q(sqrt 2)`."""
    return {
        "id": "W-fixture-sqrt2",
        "n": 2,
        "side": ["1", "1"],
        "square_size": "1",
        "representation": "center-basis",
        "scalar": {
            "kind": "algebraic-number-field",
            "minimal_polynomial": ["1", "0", "-2"],
            "isolating_interval": ["1", "2"],
        },
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {"id": 1, "center": ["1/2", "1/2"], "basis": ["1", "0"]},
            {
                "id": 2,
                "center": [["1", "1/2"], HALF_ROOT_TWO],
                "basis": [HALF_ROOT_TWO, HALF_ROOT_TWO],
            },
        ],
        "claim": {
            "coordinate_provenance": "reported",
            "method": "exact-algebraic",
            "limitations": "a test fixture",
        },
    }


def both(witness: dict[str, Any]) -> tuple[bool, bool]:
    first, _report = exact_verify(witness)
    second = algebraic.check_witness(witness)
    return bool(first["verification_passed"]), bool(second["verification_passed"])


def test_two_squares_touching_exactly_pass_on_both_routes() -> None:
    result = algebraic.check_witness(fixture())
    assert result["verification_passed"], result["failures"]
    assert result["pairs_tested"] == 1
    assert result["touching_pairs"] == 1
    assert result["minimum_best_pair_gap"] == "0.000000e+00"
    assert result["minimum_containment_clearance"] == "0.000000e+00"
    assert both(fixture()) == (True, True)


def _shift(value: Any, delta: Fraction) -> Any:
    if isinstance(value, str):
        return str(Fraction(value) + delta)
    return [str(Fraction(value[0]) + delta), *value[1:]]


def test_a_square_pushed_into_its_neighbour_is_refused_by_both_routes() -> None:
    witness = fixture()
    second = witness["squares"][1]
    second["center"][0] = _shift(second["center"][0], Fraction(-1, 10**30))
    result = algebraic.check_witness(witness)
    assert not result["verification_passed"]
    assert any("overlap" in failure for failure in result["failures"])
    assert both(witness) == (False, False)


def test_a_box_too_small_and_a_basis_too_long_are_refused() -> None:
    small = fixture()
    small["side"] = _shift(small["side"], Fraction(-1, 10**40))
    assert any("leave the container" in f for f in algebraic.check_witness(small)["failures"])
    assert both(small) == (False, False)
    long = fixture()
    long["squares"][1]["basis"][0] = _shift(long["squares"][1]["basis"][0], Fraction(1, 10**50))
    failures = algebraic.check_witness(long)["failures"]
    assert any("not a unit vector" in failure for failure in failures)
    assert both(long) == (False, False)


def test_corners_are_read_and_held_to_a_square() -> None:
    witness = fixture()
    half = Fraction(1, 2)
    witness["representation"] = "corners"
    witness["squares"] = [
        {"id": 1, "corners": [["0", "0"], ["1", "0"], ["1", "1"], ["0", "1"]]},
        {
            "id": 2,
            "corners": [
                [["1", "1/2"], ["0", "0"]],
                [["1", "1"], HALF_ROOT_TWO],
                [["1", "1/2"], ROOT_TWO],
                ["1", HALF_ROOT_TWO],
            ],
        },
    ]
    assert algebraic.check_witness(witness)["verification_passed"]
    witness["squares"][1]["corners"][3] = [str(1 + half), HALF_ROOT_TWO]
    failures = algebraic.check_witness(witness)["failures"]
    assert any("do not close a square" in failure for failure in failures)


def test_a_reducible_polynomial_still_decides_a_zero_through_the_gcd() -> None:
    # (x^2 - 2)(x - 3), whose one root in (1, 2) is sqrt 2: x^2 - 2 reduces to itself
    # modulo the cubic, is no zero polynomial there, and vanishes at the root.
    field = algebraic.Field([Fraction(v) for v in (1, -3, -2, 6)], [Fraction(1), Fraction(2)])
    vanishing = field.reduce([Fraction(-2), Fraction(0), Fraction(1)])
    assert any(vanishing)
    assert field.sign(vanishing) == 0
    assert field.gcd_decisions == 1
    assert field.sign(field.reduce([Fraction(-1), Fraction(1)])) == 1
    with pytest.raises(algebraic.WitnessFormatError, match="no single root"):
        algebraic.Field([Fraction(v) for v in (1, 0, -2)], [Fraction(-2), Fraction(2)])


def test_a_rational_witness_is_not_read() -> None:
    witness = copy.deepcopy(fixture())
    witness["scalar"] = {"kind": "rational"}
    with pytest.raises(algebraic.WitnessFormatError, match="algebraic-number-field"):
        algebraic.check_witness(witness)


@pytest.mark.parametrize("n", [51, 102])
def test_the_record_s_algebraic_houses_pass(n: int) -> None:
    document = load_yaml((KNOWN_BEST / f"n-{n:03d}.yaml").read_text(encoding="utf-8"))
    result = algebraic.check_document(document)
    assert result["verification_passed"], result["failures"]
    assert result["pairs_tested"] + result["pairs_separated_by_sweep"] == n * (n - 1) // 2
