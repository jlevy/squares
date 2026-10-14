"""The same-side re-solve on fixtures small enough to be checked by hand, and on records.

Synthetic witnesses first, each built so the exact answer is known before the tool runs:
two axis squares that must land on exact halves, a square at the rational rotation
`(3/5, 4/5)` whose basis must come back exactly and in the quarter the view states, a
chain of three squares that cannot close at a side one part in `10^20` wider than it
needs (relaxed, the upper-right wall opens) or narrower (refused: no packing exists), a
rotation no witness square holds, and a witness over a number field. Then the record's
own witnesses with generator-like poses: n = 26 and 70 reach `same` at exactly `s_W` on
both exact routes, with a rattler moved well off its contacts; n = 5 and 10 refuse, and
the test says why they must.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_rational_witness_independent as independent
from devtools import regularize_same_side as same_side
from devtools.regularize_same_side import (
    AXIS,
    KNOWN_BEST,
    WITNESS_SCHEMA,
    GeneratorPose,
    Row,
    SameSideError,
    exact_frame,
    match_rotations,
    perturbed,
    resolve,
    settle,
    support,
    tight_rows,
    witness_poses,
)
from sqpack.witness import exact_verify, load_witness, validate_witness_document

HALF = Fraction(1, 2)
THREE_FIVE = (Fraction(3, 5), Fraction(4, 5))


def basis_witness(
    squares: list[tuple[str, str, tuple[str, str]]], side: str, *, name: str = "fixture"
) -> dict[str, Any]:
    """A rational centre-basis Witness/v2 record."""
    return {
        "id": f"W-{name}",
        "n": len(squares),
        "side": side,
        "square_size": "1",
        "representation": "center-basis",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {"id": index, "center": [x, y], "basis": list(basis)}
            for index, (x, y, basis) in enumerate(squares, start=1)
        ],
        "claim": {
            "coordinate_provenance": "reported",
            "method": "exact-algebraic",
            "limitations": "a test fixture",
        },
    }


def view(*poses: tuple[str, str, str]) -> list[GeneratorPose]:
    return [GeneratorPose(x, y, degrees) for x, y, degrees in poses]


def centers(outcome: same_side.SameSideOutcome) -> list[tuple[Fraction, Fraction]]:
    assert outcome.witness is not None
    return [
        (Fraction(square["center"][0]), Fraction(square["center"][1]))
        for square in outcome.witness["squares"]
    ]


def both_routes_accept(outcome: same_side.SameSideOutcome) -> bool:
    verdicts = outcome.report["verdicts"]
    return bool(verdicts["exact_verify"]["passed"] and verdicts["independent"]["passed"])


# --------------------------------------------------------------------------------------
# Synthetic fixtures
# --------------------------------------------------------------------------------------


def test_two_axis_squares_land_on_exact_halves() -> None:
    witness = basis_witness([("1/2", "1/2", ("1", "0")), ("3/2", "1/2", ("1", "0"))], "2")
    poses = view(("0.500000000001", "0.499999999999", "0"), ("1.499999999998", "0.5", "90"))
    outcome = resolve(witness, poses)
    assert outcome.status == "same"
    assert outcome.side == 2
    assert centers(outcome) == [(HALF, HALF), (Fraction(3, 2), HALF)]
    rows = outcome.report["rows"]
    assert rows["pairs"] == 1
    assert rows["walls"] == 4
    assert rows["used"] == 4
    assert rows["dependent"] == 1
    assert rows["relaxed"] == []
    assert rows["free_coordinates"] == 0
    assert outcome.report["displacement"]["max"] < 3e-12
    assert both_routes_accept(outcome)
    assert outcome.witness is not None
    assert outcome.witness["squares"][1]["basis"] == ["1", "0"]
    assert outcome.witness["claim"]["coordinate_provenance"] == "verified"


def test_the_witness_document_is_a_valid_witness(tmp_path: Path) -> None:
    witness = basis_witness([("1/2", "1/2", ("1", "0"))], "1")
    outcome = resolve(witness, view(("0.5", "0.5", "0")), view_id="W-fixture-view")
    assert outcome.witness is not None
    assert outcome.witness["id"] == "W-fixture-view"
    document = {
        "softschema": {
            "contract": "packing.squares:Witness/v2",
            "schema": str(WITNESS_SCHEMA),
            "envelope": "witness",
            "status": "enforced",
        },
        "witness": outcome.witness,
    }
    loaded = validate_witness_document(document, path=tmp_path / "view.yaml")
    assert loaded["side"] == "1"


def test_a_tilted_rational_rotation_comes_back_exactly_in_the_stated_quarter() -> None:
    # A square at (3/5, 4/5) has half-extent 7/10 along both axes: it fits exactly in a
    # box of side 7/5 with its centre at (7/10, 7/10).
    witness = basis_witness([("7/10", "7/10", ("3/5", "4/5"))], "7/5")
    degrees = math.degrees(math.atan2(0.8, 0.6))
    outcome = resolve(witness, view(("0.7000000000003", "0.69999999999", repr(degrees))))
    assert outcome.status == "same"
    assert centers(outcome) == [(Fraction(7, 10), Fraction(7, 10))]
    assert outcome.witness is not None
    assert outcome.witness["squares"][0]["basis"] == ["3/5", "4/5"]
    assert outcome.report["rotations"]["classes"] == [1]
    # The same rotation stated a quarter turn down takes the representative in that
    # quarter, (s, -c): the same square, the basis the view asked for.
    turned = resolve(witness, view(("0.7", "0.7", repr(degrees - 90))))
    assert turned.status == "same"
    assert turned.witness is not None
    assert turned.witness["squares"][0]["basis"] == ["4/5", "-3/5"]
    assert turned.report["rotations"]["quarter_turns"] == [3]


def test_a_corner_on_face_contact_closes_exactly() -> None:
    # The tilted square's rightmost corner is at x = 7/5, where the axis square's left
    # face must sit: an axis-normal pair row with a rational support on each side.
    witness = basis_witness(
        [("7/10", "7/10", ("3/5", "4/5")), ("19/10", "1/2", ("1", "0"))], "12/5"
    )
    degrees = math.degrees(math.atan2(0.8, 0.6))
    poses = view(("0.7", "0.7", repr(degrees)), ("1.9000000000004", "0.5", "0"))
    outcome = resolve(witness, poses)
    assert outcome.status == "same"
    assert centers(outcome) == [(Fraction(7, 10), Fraction(7, 10)), (Fraction(19, 10), HALF)]
    frame = exact_frame(witness)
    rows = tight_rows(frame, poses, match_rotations(frame, poses))
    pairs = [row for row in rows if row.kind == "pair"]
    assert len(pairs) == 1
    assert pairs[0].rhs == Fraction(7, 10) + HALF
    assert pairs[0].label["normal"] == {"of": 2, "face": 0, "sign": 1}
    assert pairs[0].coefficients == {0: Fraction(-1), 2: Fraction(1)}
    # Three low walls (both squares' floors and the tilted square's left) and the axis
    # square's right wall; the pair row leads them all.
    assert [row.kind for row in rows] == ["pair", "wall", "wall", "wall", "wall"]
    assert [row.label.get("wall") for row in rows[1:]] == ["low", "low", "low", "high"]


def test_a_relaxed_row_that_would_be_penetrated_is_promoted() -> None:
    # x2 - x1 = 1 and x1 = 1/2 close first; x2 = 3/2 + e is then inconsistent and its
    # slack negative, so it is promoted and x1's wall opens by +e instead.
    e = Fraction(1, 10**20)
    pair = Row(
        "pair",
        {0: Fraction(-1), 2: Fraction(1)},
        Fraction(1),
        1,
        {"squares": [1, 2]},
        (0, 0, 1),
    )
    first = Row("wall", {0: Fraction(1)}, HALF, 1, {"square": 1}, (1, 0, 0))
    second = Row("wall", {2: Fraction(1)}, Fraction(3, 2) + e, 1, {"square": 2}, (1, 1, 0))
    generator = [(HALF, HALF), (Fraction(3, 2), HALF)]
    solution, promoted, rounds = settle([pair, first, second], 2, generator, mode="relax")
    assert rounds == 2
    assert [row.priority for row in promoted] == [(1, 1, 0)]
    assert [row.priority for row in solution.relaxed] == [(1, 0, 0)]
    assert solution.relaxed[0].gap(solution.values) == e
    assert solution.values[0] == HALF + e
    assert solution.values[2] == Fraction(3, 2) + e
    with pytest.raises(SameSideError, match="cannot close exactly"):
        settle([pair, first, second], 2, generator, mode="refuse")


def test_a_chain_that_cannot_close_opens_at_the_upper_right_wall_or_refuses() -> None:
    wide = basis_witness(
        [("1/2", "1/2", ("1", "0")), ("3/2", "1/2", ("1", "0")), ("5/2", "1/2", ("1", "0"))],
        "300000000000000000001/100000000000000000000",
    )
    poses = view(("0.5", "0.5", "0"), ("1.5", "0.5", "0"), ("2.5", "0.5", "0"))
    relaxed = resolve(wide, poses, mode="relax")
    assert relaxed.status == "same"
    assert relaxed.side == Fraction("300000000000000000001/100000000000000000000")
    assert centers(relaxed) == [(HALF, HALF), (Fraction(3, 2), HALF), (Fraction(5, 2), HALF)]
    opened = relaxed.report["rows"]["relaxed"]
    assert [row["wall"] for row in opened] == ["high"]
    assert opened[0]["slack"] == "1/100000000000000000000"
    refused = resolve(wide, poses, mode="refuse")
    assert refused.status == "refused"
    assert refused.reason == "inconsistent-tight-set"
    assert refused.witness is None
    assert refused.report["refusal"]["row"] == {"square": 3, "axis": "x", "wall": "high"}


def test_a_side_too_small_for_its_chain_refuses_as_overlap() -> None:
    narrow = basis_witness(
        [("1/2", "1/2", ("1", "0")), ("3/2", "1/2", ("1", "0")), ("5/2", "1/2", ("1", "0"))],
        "299999999999999999999/100000000000000000000",
    )
    poses = view(("0.5", "0.5", "0"), ("1.5", "0.5", "0"), ("2.5", "0.5", "0"))
    outcome = resolve(narrow, poses, mode="relax")
    assert outcome.status == "refused"
    assert outcome.reason == "overlap"
    assert outcome.witness is None
    assert outcome.side is None
    assert not outcome.report["verdicts"]["exact_verify"]["passed"]
    assert not outcome.report["verdicts"]["independent"]["passed"]
    assert outcome.report["rows"]["relaxed"][0]["slack"] == "-1/100000000000000000000"


def test_supports_are_exact_and_the_axis_support_of_a_tilt_is_its_extent() -> None:
    assert support(THREE_FIVE, AXIS) == Fraction(7, 10)
    assert support(AXIS, AXIS) == HALF
    assert support(THREE_FIVE, THREE_FIVE) == HALF


def test_a_rotation_no_witness_square_holds_is_refused() -> None:
    witness = basis_witness(
        [("1/2", "1/2", ("1", "0")), ("7/10", "17/10", ("3/5", "4/5"))], "3"
    )
    poses = view(("0.5", "0.5", "0"), ("0.7", "1.7", "45"))
    outcome = resolve(witness, poses)
    assert outcome.status == "refused"
    assert outcome.reason == "unmatched-rotation"
    assert outcome.report["refusal"]["square"] == 2
    assert outcome.report["refusal"]["nearest_degrees"] == pytest.approx(8.13, abs=0.01)
    with pytest.raises(SameSideError, match="matches no rotation"):
        match_rotations(exact_frame(witness), poses)


TILT_DEGREES = math.degrees(math.atan2(0.8, 0.6))


def test_the_drift_the_exact_solve_leaves_on_a_rotation_still_matches_it() -> None:
    """The full run of 12 October 2026 refused 17 counts at a tolerance of 1e-12 degrees
    for drifts of 2e-11 to 7.5e-11 degrees (n = 146); a sine of 1e-9 takes them."""
    witness = basis_witness([("7/10", "7/10", ("3/5", "4/5"))], "7/5")
    drifted = resolve(witness, view(("0.7", "0.7", repr(TILT_DEGREES + 7.5e-11))))
    assert drifted.status == "same"
    assert drifted.witness is not None
    assert drifted.witness["squares"][0]["basis"] == ["3/5", "4/5"]
    assert math.isclose(same_side.ROTATION_TOLERANCE_DEGREES, 5.7296e-8, rel_tol=1e-4)
    # A turn of a millionth of a degree is a turn, not drift.
    turned = resolve(witness, view(("0.7", "0.7", repr(TILT_DEGREES + 1e-6))))
    assert (turned.status, turned.reason) == ("refused", "unmatched-rotation")


def test_a_reflected_rotation_is_not_the_witness_rotation() -> None:
    # (4/5, -3/5) at -36.87 degrees mirrors the witness's +36.87; no quarter turn of one
    # is the other, so it is refused rather than matched (after #515's test).
    witness = basis_witness([("7/10", "7/10", ("3/5", "4/5"))], "7/5")
    outcome = resolve(witness, view(("0.7", "0.7", repr(-TILT_DEGREES))))
    assert (outcome.status, outcome.reason) == ("refused", "unmatched-rotation")


def test_quarter_turns_of_a_rotation_are_one_class() -> None:
    frame = exact_frame(basis_witness([("7/10", "7/10", ("3/5", "4/5"))], "7/5"))
    matched = match_rotations(
        frame, [GeneratorPose("0.7", "0.7", repr(TILT_DEGREES + 90 * k)) for k in range(4)]
    )
    assert [(m.source, m.quarter_turns) for m in matched] == [(0, k) for k in range(4)]


def test_one_route_refusing_what_the_other_accepts_is_named(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def disagreeing(*_args: object) -> dict[str, Any]:
        return {
            "exact_verify": {"passed": True, "failures": []},
            "independent": {"passed": False, "failures": ["a test disagreement"]},
        }

    monkeypatch.setattr(same_side, "verify_both", disagreeing)
    witness = basis_witness([("1/2", "1/2", ("1", "0"))], "1")
    outcome = resolve(witness, view(("0.5", "0.5", "0")))
    assert (outcome.status, outcome.reason) == ("refused", "routes-disagree")


def test_a_pose_too_long_to_write_is_refused_by_name(monkeypatch: pytest.MonkeyPatch) -> None:
    def too_long(*_args: object, **_kwargs: object) -> same_side.SameSideOutcome:
        raise ValueError("Exceeds the limit (4300 digits) for integer string conversion")

    monkeypatch.setattr(same_side, "_resolve", too_long)
    witness = basis_witness([("1/2", "1/2", ("1", "0"))], "1")
    outcome = resolve(witness, view(("0.5", "0.5", "0")))
    assert (outcome.status, outcome.reason) == ("refused", "literal-too-large")


def test_a_witness_over_a_number_field_has_no_exact_frame() -> None:
    witness = load_witness(KNOWN_BEST / "n-051.yaml", fallback_schema=WITNESS_SCHEMA)
    outcome = resolve(witness, [GeneratorPose("0.5", "0.5", "0")] * 51)
    assert outcome.status == "refused"
    assert outcome.reason == "no-exact-frame"
    assert outcome.report["source"]["kind"] == "algebraic-number-field"
    with pytest.raises(SameSideError, match="no rational frame"):
        exact_frame(witness)


def test_a_view_with_the_wrong_count_is_an_error() -> None:
    witness = basis_witness([("1/2", "1/2", ("1", "0"))], "1")
    with pytest.raises(ValueError, match="the view has 2 squares"):
        resolve(witness, view(("0.5", "0.5", "0"), ("0.5", "0.5", "0")))


# --------------------------------------------------------------------------------------
# The record's witnesses
# --------------------------------------------------------------------------------------


def record(n: int) -> dict[str, Any]:
    return load_witness(KNOWN_BEST / f"n-{n:03d}.yaml", fallback_schema=WITNESS_SCHEMA)


def test_n26_reaches_the_printed_side_with_a_rattler_moved_off_its_contacts() -> None:
    witness = record(26)
    assert witness["scalar"]["kind"] == "decimal"
    # Square 9 is the rattler (one tight contact, the right wall); it keeps the wall and
    # loses nothing when moved 0.05 along it.
    poses = perturbed(witness_poses(witness), 1e-12, seed=26, squares={8: (0.0, 0.05)})
    outcome = resolve(witness, poses)
    assert outcome.status == "same", outcome.report.get("refusal")
    assert outcome.side == Fraction(witness["side"])
    assert both_routes_accept(outcome)
    assert outcome.report["side"]["side_minus_reported"] == "0"
    rows = outcome.report["rows"]
    assert rows["promoted"] != []
    assert all(not row["slack"].startswith("-") for row in rows["relaxed"])
    assert outcome.report["displacement"]["max"] < 1e-9
    moved = centers(outcome)[8]
    assert abs(float(moved[1]) - float(poses[8].y)) < 1e-29
    assert moved[0] == Fraction(witness["side"]) - HALF
    # Every 45-degree square took the promotion's rational rotation, the same class.
    classes = outcome.report["rotations"]["classes"]
    assert outcome.report["rotations"]["axis"] == 17
    assert len({c for c in classes if c is not None}) >= 1


def test_n70_reaches_its_rational_side_with_tilted_squares() -> None:
    witness = record(70)
    assert witness["scalar"]["kind"] == "rational"
    assert witness["representation"] == "center-basis"
    poses = perturbed(witness_poses(witness), 1e-12, seed=70)
    outcome = resolve(witness, poses)
    assert outcome.status == "same", outcome.report.get("refusal")
    assert outcome.side == Fraction(witness["side"])
    assert both_routes_accept(outcome)
    assert outcome.report["rotations"]["matched"] > 0
    assert outcome.report["displacement"]["max"] < 1e-9
    # The record's side is a rounding above the chain's exact length, so the chains
    # open at upper-right walls and nowhere else.
    assert {row.get("wall") for row in outcome.report["rows"]["relaxed"]} == {"high"}
    assert outcome.witness is not None
    bases = {tuple(square["basis"]) for square in outcome.witness["squares"]}
    source = {tuple(square["basis"]) for square in witness["squares"]}
    assert bases <= source


@pytest.mark.parametrize("n", [5, 10])
def test_the_truncated_goebel_sides_cannot_hold_a_rational_pose(n: int) -> None:
    # The printed side is 2 + sqrt(2)/2 (n = 5) or 3 + sqrt(2)/2 (n = 10) rounded down
    # at 28 places, and a rational rotation has c + s < sqrt(2), so the diagonal chain
    # through the 45-degree square needs a side above the printed one by about 1e-29.
    witness = record(n)
    poses = perturbed(witness_poses(witness), 1e-12, seed=n)
    relaxed = resolve(witness, poses, mode="relax")
    assert relaxed.status == "refused"
    assert relaxed.reason == "overlap"
    assert any(row["slack"].startswith("-") for row in relaxed.report["rows"]["relaxed"])
    assert relaxed.report["verdicts"]["exact_verify"]["failures"] != []
    assert relaxed.report["verdicts"]["independent"]["failures"] != []
    refused = resolve(witness, poses, mode="refuse")
    assert refused.status == "refused"
    assert refused.reason == "inconsistent-tight-set"
    assert refused.report["refusal"]["residual"].startswith("-9.698")


# --------------------------------------------------------------------------------------
# The command
# --------------------------------------------------------------------------------------


def test_the_command_writes_a_view_it_decided(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    witness = basis_witness([("1/2", "1/2", ("1", "0")), ("3/2", "1/2", ("1", "0"))], "2")
    witness_path = tmp_path / "fixture.yaml"
    witness_path.write_text(
        same_side.witness_document(witness, schema=str(WITNESS_SCHEMA)), encoding="utf-8"
    )
    view_path = tmp_path / "view.json"
    view_path.write_text(
        json.dumps({"packing": {"S": "2.0", "sq": [[0.5, 0.5, 0.0], ["1.5", "0.5", "0"]]}})
    )
    output = tmp_path / "run" / "view-same.yaml"
    code = same_side.main(
        [str(witness_path), str(view_path), "--output", str(output), "--json"]
    )
    assert code == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "same"
    assert report["output"] == str(output.resolve())
    loaded = load_witness(output)
    assert loaded["id"] == "W-fixture-regularized"
    assert loaded["side"] == "2"
    assert exact_verify(loaded)[1].valid
    squares = [
        same_side.corners_of(
            (Fraction(s["center"][0]), Fraction(s["center"][1])),
            (Fraction(s["basis"][0]), Fraction(s["basis"][1])),
        )
        for s in loaded["squares"]
    ]
    assert independent.check_squares(squares, Fraction(2))["verification_passed"]
    # Without --json the command prints the summary paragraph instead.
    assert same_side.main([str(witness_path), str(view_path)]) == 0
    text = capsys.readouterr().out
    assert text.startswith("same: n = 2, side 2")
    assert "rows: 4 used, 1 dependent, 0 relaxed, 0 promoted, 0 free coordinates" in text


def test_the_command_refuses_to_write_under_the_witnesses(tmp_path: Path) -> None:
    witness = basis_witness([("1/2", "1/2", ("1", "0"))], "1")
    witness_path = tmp_path / "fixture.yaml"
    witness_path.write_text(
        same_side.witness_document(witness, schema=str(WITNESS_SCHEMA)), encoding="utf-8"
    )
    view_path = tmp_path / "view.json"
    view_path.write_text(json.dumps({"packing": {"S": "1", "sq": [["0.5", "0.5", "0"]]}}))
    forbidden = KNOWN_BEST / "n-999-view.yaml"
    with pytest.raises(ValueError, match="may not be written"):
        same_side.main([str(witness_path), str(view_path), "--output", str(forbidden)])
    assert not forbidden.exists()


def test_the_survey_tallies_by_kind_and_reason(capsys: pytest.CaptureFixture[str]) -> None:
    code = same_side.main(["--survey", "1..2"])
    assert code == 0
    out = capsys.readouterr().out
    assert "rational-corners:" in out
    assert "same: 2" in out
