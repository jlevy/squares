"""Exact radical order and independent geometry boundaries for issue432."""

from __future__ import annotations

from fractions import Fraction

import pytest

from devtools import ryxu_radical_n51 as radical


@pytest.mark.parametrize(
    ("a", "b", "sign"),
    [
        (0, 0, 0),
        (0, 1, 1),
        (0, -1, -1),
        (3, -2, 1),
        (2, -2, -1),
        (-3, 2, -1),
        (-2, 2, 1),
        (1, 1, 1),
        (-1, -1, -1),
    ],
)
def test_exact_quadratic_order(a: int, b: int, sign: int) -> None:
    assert radical.Q2(Fraction(a), Fraction(b)).sign() == sign


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("7/2", (Fraction(7, 2), Fraction(0))),
        ("(10 \u2212 1√2)/4", (Fraction(5, 2), Fraction(-1, 4))),
        ("4 + 1√2", (Fraction(4), Fraction(1))),
        ("(16 + 5√2)/3", (Fraction(16, 3), Fraction(5, 3))),
    ],
)
def test_closed_source_expression_grammar(
    expression: str, expected: tuple[Fraction, Fraction]
) -> None:
    assert radical.parse(expression) == radical.Q2(*expected)


@pytest.mark.parametrize(
    "expression", ["sqrt(2)", "__import__('os')", "(1 + 1√2)/0", "1.5", "(1+1√2)/2"]
)
def test_no_expression_evaluation(expression: str) -> None:
    with pytest.raises(ValueError, match="unsupported"):
        radical.parse(expression)


def test_direct_axis_and_diamond_geometry_decides_both_failures() -> None:
    q = radical.Q2
    side = q(Fraction(10))
    poses = [(q(Fraction(2)), q(Fraction(2)), "0"), (q(Fraction(5)), q(Fraction(5)), "π/4")]
    result = radical.independent(side, poses)
    assert result["verification_passed"] is True
    assert result["pairs_tested"] == 1
    assert radical.independent(side, [poses[0], poses[0]])["verification_passed"] is False
    outside = [(q(Fraction(11)), q(Fraction(2)), "0"), poses[1]]
    assert radical.independent(side, outside)["verification_passed"] is False


def test_positive_source_side_polynomial_and_nonoptimal_scope() -> None:
    side = radical.parse("(16 + 5√2)/3")
    assert (
        radical.Q2(Fraction(9)) * side * side
        - radical.Q2(Fraction(96)) * side
        + radical.Q2(Fraction(206))
        == radical.Q2()
    )
    witness = radical.witness(side, [(radical.Q2(Fraction(1)), radical.Q2(Fraction(1)), "0")])
    assert "no global optimality" in witness["claim"]["limitations"]


@pytest.mark.parametrize(
    "mutation",
    [
        "drop-native-field",
        "forge-field",
        "change-diagnostic",
        "change-last-coordinate",
        "replace-control",
        "truncate-independent",
    ],
)
def test_complete_radical_outcome_custody(tmp_path, monkeypatch, mutation: str) -> None:
    root = radical.rational.PACKET
    relative_paths = ["facts/n051-undilated-record.json.xz"] + [
        f"receipts/n051-radical-{control}.json.xz" for control in radical.rational.JOBS
    ]
    retained = {path: (root / path).read_bytes() for path in relative_paths}
    monkeypatch.setattr(radical.rational, "REPO", tmp_path)
    monkeypatch.setattr(radical.rational, "PACKET", tmp_path / "packet")
    for relative, data in retained.items():
        path = radical.rational.PACKET / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    assert len(radical.check_certification()) == 3
    path = radical.rational.PACKET / "receipts/n051-radical-positive.json.xz"
    row = radical.rational.kernel.read_xz(path)
    if mutation == "drop-native-field":
        row["exact_verify"].pop("limitations")
    elif mutation == "forge-field":
        row["exact_verify"]["field_certificate"]["irreducible_over_q"] = False
    elif mutation == "change-diagnostic":
        row["exact_verify"]["minimum_containment_clearance"] = "1"
    elif mutation == "change-last-coordinate":
        row["native_input"]["squares"][-1]["center"][0] = ["0", "0"]
    elif mutation == "replace-control":
        row["control"] = "duplicate-square-overlap"
    else:
        row["independent"].pop("field")
    radical.rational.save(path, row)
    with pytest.raises(ValueError, match="complete frozen"):
        radical.check_certification()


def test_actual_negative_radical_replay_survives_json_failure_normalization(
    monkeypatch,
) -> None:
    """Native tuple failures and retained JSON lists must represent the same full outcome."""
    control = "duplicate-square-overlap"
    monkeypatch.setattr(radical.rational, "JOBS", (control,))
    admitted = radical.check_certification(replay=True)
    assert admitted[control]["exact_verify"]["verification_passed"] is False
    assert admitted[control]["independent"]["verification_passed"] is False
    assert admitted[control]["exact_verify"]["pairs_tested"] == 1275
