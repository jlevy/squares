"""The same-side re-solve on fixtures whose exact answer is known before it runs.

An axis-aligned 2 x 2 block in side 2 with its centres perturbed below the tight
tolerance comes back exactly on the lattice. A square turned by the Pythagorean rotation
(4/5, 3/5) whose corner rests on an aligned square's side, and whose lowest corner rests
on the floor, comes back with that contact exactly closed; re-solved through
`resolve_view` at the witness's side it is `same`, at any other side `solved`. A row of
three in a box 5e-10 too short is an inconsistent tight set, refused with a Farkas
certificate; the same row in a box 5e-10 too long is refused by default and solved under
`relax`, the slack left at the far wall. A view rotation at 45 degrees is refused when
the source holds no rotation there, and snaps when it does; its mirror image is not the
source's rotation. A rattler whose free coordinates are rounded too coarsely overlaps,
and this module's own check refuses it; with that check disabled, the maintained routes
refuse it under their own kind. Two nearly parallel contacts on one square are not both
closed when that would move the view past the move limit. Two real witnesses, the
rational 5 x 5 grid and the decimal n = 26 with nine squares at 45 degrees, re-solve from
their own binary64 poses to packings at exactly their own sides, and the number-field
witness is refused as the axis tool refuses it. Malformed scalars, options and counts
are refused rather than raised, a side past binary64's range is reported exactly, and
`evand_view` undoes the vendored `reg.py` `d4` itself on a 50-digit record.
"""

from __future__ import annotations

import ast
import json
from collections.abc import Callable
from fractions import Fraction
from functools import cache
from typing import Any

import mpmath
import pytest

from devtools import regularize_same_side as same_side
from devtools.regularize_same_side import (
    ROOT,
    WITNESS_SCHEMA,
    Basis,
    Refusal,
    Resolved,
    Snapped,
    ViewResolution,
    basis_from_angle,
    basis_from_half_tangent,
    evand_view,
    main,
    pose_failures,
    pose_witness,
    quarter_turn,
    resolve_at_side,
    resolve_view,
    self_view,
    snap_rotations,
    source_frame,
    verify_pose,
)
from sqpack.witness import load_witness, validate_witness_document, witness_envelope

AXIS: Basis = (Fraction(1), Fraction(0))
TILT: Basis = (Fraction(4, 5), Fraction(3, 5))
HALF = Fraction(1, 2)
RATTLER: Basis = (Fraction(24, 25), Fraction(7, 25))
"""Half-width 31/50: at `RATTLER_VIEW` it is 1/100 clear of the floor and of square 0."""
RATTLER_VIEW = [(HALF, HALF), (Fraction("1.63"), Fraction("0.63"))]
REG = ROOT.parent / "vendor" / "evand-regularize" / "search" / "regularize" / "reg.py"


def resolved(outcome: Resolved | Refusal) -> Resolved:
    assert not isinstance(outcome, Refusal), f"refused: {outcome.kind}: {outcome.detail}"
    return outcome


def refusal(outcome: object) -> Refusal:
    assert isinstance(outcome, Refusal), f"expected a refusal, got {outcome!r}"
    return outcome


def rational_witness(
    side: Fraction, poses: list[tuple[Fraction, Fraction, Basis]], name: str = "fixture"
) -> dict[str, Any]:
    """A rational center-basis Witness/v2 record, the kind Ryan Xu's witnesses are."""
    return pose_witness(
        side,
        [basis for _, _, basis in poses],
        [(x, y) for x, y, _ in poses],
        witness_id=f"W-{name}",
    )


def test_axis_block_snaps_exactly_onto_the_lattice() -> None:
    approx = [
        ("0.5000000003", "0.4999999998"),
        ("1.5000000002", "0.5000000004"),
        ("0.4999999997", "1.5000000001"),
        ("1.5000000001", "1.4999999996"),
    ]
    result = resolved(resolve_at_side(Fraction(2), [AXIS] * 4, approx))
    assert result.side == 2
    assert list(result.centres) == [
        (HALF, HALF),
        (3 * HALF, HALF),
        (HALF, 3 * HALF),
        (3 * HALF, 3 * HALF),
    ]
    assert result.tight_walls == 8
    # Four pairs share a side; the two diagonal pairs meet at the block's centre point.
    assert result.tight_pairs == 6
    assert result.closed == 14
    assert result.relaxed == ()
    assert result.free_unknowns == 0
    assert result.max_move == Fraction(4, 10**10)
    assert result.verification["passed"]
    assert result.verification["exact_verify"]["minimum_best_pair_gap"] == "0"
    assert result.verification["independent"]["minimum_containment_clearance"] == "0"


def test_pythagorean_corner_rests_exactly_on_a_side() -> None:
    # The tilted square's half-width is (4/5 + 3/5)/2 = 7/10: its lowest corner is on the
    # floor at y = 7/10, and its leftmost corner, 1/10 above its centre, on the aligned
    # square's right side at x = 1 + 7/10.
    assert basis_from_half_tangent(Fraction(1, 3)) == TILT
    approx = [(0.5000000002, 0.4999999999), (1.7000000004, 0.6999999997)]
    result = resolved(resolve_at_side(Fraction(3), [AXIS, TILT], approx))
    assert list(result.centres) == [(HALF, HALF), (Fraction(17, 10), Fraction(7, 10))]
    assert result.tight_pairs == 1
    assert result.tight_walls == 3
    assert result.rank == 4
    assert result.verification["passed"]
    touching = result.verification["exact_verify"]["minimum_best_pair_gap"]
    assert touching == "0"


def test_resolve_view_keeps_the_witness_side_and_flags_the_register() -> None:
    side = Fraction(3)
    source = rational_witness(side, [(HALF, HALF, AXIS), (Fraction(17, 10), Fraction(1), TILT)])
    # The view turns the tilted square by a quarter turn plus 1e-12 and drops it onto the
    # floor against the aligned square: the snap restores the source's exact rotation.
    nearly = basis_from_half_tangent(Fraction(1, 3) + Fraction(1, 10**12))
    view = [
        (0.5, 0.5, AXIS),
        (1.7000000001, 0.7000000001, quarter_turn(nearly, 1)),
    ]
    outcome = resolve_view(source, view, verified_bound=Fraction(4))
    assert isinstance(outcome, ViewResolution)
    assert outcome.resolved.side == side
    assert outcome.resolved.rotations[1] == quarter_turn(TILT, 1)
    assert outcome.snapped.snaps[1].target == 1
    assert outcome.side_basis["side_minus_printed"] == "0"
    assert outcome.register["below_verified_bound"] is True
    document = witness_envelope(outcome.resolved.witness)
    validated = validate_witness_document(document, path=WITNESS_SCHEMA.parent / "view.yaml")
    assert validated["certificate"]["side_relation"] == "same"
    assert validated["certificate"]["derived_from"] == "W-fixture"


def test_a_side_other_than_the_frame_side_is_solved_not_same() -> None:
    source = rational_witness(
        Fraction(3), [(HALF, HALF, AXIS), (Fraction(17, 10), Fraction(1), TILT)]
    )
    view = [(0.5, 0.5, AXIS), (1.7000000001, 0.7000000001, TILT)]
    wider = resolve_view(source, view, side=Fraction(4))
    assert isinstance(wider, ViewResolution)
    assert wider.resolved.side == 4
    assert wider.resolved.centres[1] == (Fraction(17, 10), Fraction(7, 10))
    assert wider.side_relation == "solved"
    assert wider.resolved.witness["certificate"]["side_relation"] == "solved"
    assert wider.resolved.witness["id"] == "W-fixture-solved-side"
    assert wider.summary()["status"] == "solved-side"
    assert wider.side_basis["frame_side"] == "3"
    # The frame's own side, passed explicitly, is still `same`.
    again = resolve_view(source, view, side="3")
    assert isinstance(again, ViewResolution)
    assert again.side_relation == "same"
    assert again.summary()["status"] == "same-side"
    # With no source there is nothing to compare: no relation is written at all.
    bare = resolved(resolve_at_side(Fraction(3), [AXIS, TILT], [(x, y) for x, y, _ in view]))
    assert "side_relation" not in bare.witness["certificate"]
    assert bare.summary()["status"] == "resolved"


def row_of_three(side: Fraction) -> list[tuple[Fraction, Fraction]]:
    return [(HALF, HALF), (3 * HALF, HALF), (side - HALF, HALF)]


def test_inconsistent_tight_set_is_refused_with_a_farkas_certificate() -> None:
    short = 3 - Fraction(5, 10**10)
    outcome = refusal(resolve_at_side(short, [AXIS] * 3, row_of_three(short)))
    assert outcome.kind == "inconsistent-tight-set"
    evidence = outcome.items[0]
    assert evidence["farkas"] is True
    assert evidence["forced_gap"] == "-1/2000000000"
    assert len(evidence["certificate"]) == 4
    relaxed = refusal(
        resolve_at_side(short, [AXIS] * 3, row_of_three(short), on_conflict="relax")
    )
    assert relaxed.kind == "tight-set-forces-overlap"


def test_slack_is_refused_by_default_and_left_at_the_far_wall_under_relax() -> None:
    long = 3 + Fraction(5, 10**10)
    outcome = refusal(resolve_at_side(long, [AXIS] * 3, row_of_three(long)))
    assert outcome.kind == "inconsistent-tight-set"
    assert outcome.items[0]["farkas"] is False
    result = resolved(
        resolve_at_side(long, [AXIS] * 3, row_of_three(long), on_conflict="relax")
    )
    assert [item["constraint"] for item in result.relaxed] == ["square 2 on the right wall"]
    assert result.relaxed[0]["gap_after"] == "1/2000000000"
    assert result.relaxed[0]["gap_after_decimal"] == "5.000e-10"
    assert result.centres[2] == (Fraction(5, 2), HALF)
    assert result.side == long


def test_forty_five_degrees_snaps_only_to_a_rotation_the_source_holds() -> None:
    forty_five = basis_from_angle("45")
    outcome = refusal(snap_rotations([AXIS, forty_five], [AXIS, TILT]))
    assert outcome.kind == "unmatched-rotation"
    assert outcome.items == ({"square": 1, "degrees": 45.0, "exactly_45": True},)
    # Evan Daniel writes 45 degrees as t = tan(22.5 degrees) to 35 digits; the source's
    # promotion holds it to 36. They differ by about 1e-36 and snap.
    upstream = basis_from_half_tangent(
        Fraction("2588834764831844055010554526310613/6250000000000000000000000000000000")
    )
    snapped = snap_rotations([upstream], [AXIS, basis_from_angle("45.0")])
    assert isinstance(snapped, Snapped)
    assert snapped.rotations[0] == basis_from_angle("45.0")
    assert 0 < snapped.snaps[0].deviation < Fraction(1, 10**35)


def test_a_reflected_rotation_is_not_the_source_rotation() -> None:
    # (4/5, -3/5) turns by -36.87 degrees, the mirror image of the source's +36.87; no
    # quarter turn of one is the other, so it is refused rather than snapped.
    mirrored: Basis = (Fraction(4, 5), Fraction(-3, 5))
    outcome = refusal(snap_rotations([mirrored], [AXIS, TILT]))
    assert outcome.kind == "unmatched-rotation"
    assert [(item["square"], item["exactly_45"]) for item in outcome.items] == [(0, False)]


def test_quarter_turns_are_one_rotation() -> None:
    snapped = snap_rotations([quarter_turn(TILT, k) for k in range(4)], [TILT])
    assert isinstance(snapped, Snapped)
    assert list(snapped.rotations) == [quarter_turn(TILT, k) for k in range(4)]
    assert all(snap.deviation == 0 and snap.target == 0 for snap in snapped.snaps)


def test_coarse_rounding_of_a_rattler_is_refused_by_the_module_check() -> None:
    # The rattler's coordinates are free; rounded to one decimal they drop it 2/100 into
    # the floor and the pinned aligned square, and `pose_failures` refuses every rung.
    coarse = refusal(
        resolve_at_side(Fraction(3), [AXIS, RATTLER], RATTLER_VIEW, free_digits=(1,))
    )
    assert coarse.kind == "verification-failed"
    failures = [item["failure"] for item in coarse.items if "failure" in item]
    assert any("overlap" in failure for failure in failures)
    assert any("wall" in failure for failure in failures)
    result = resolved(resolve_at_side(Fraction(3), [AXIS, RATTLER], RATTLER_VIEW))
    assert result.free_unknowns == 2
    assert result.centres[1] == (Fraction("1.63"), Fraction("0.63"))


def test_the_module_check_and_both_routes_agree_on_an_overlap() -> None:
    overlapping = [(HALF, HALF), (Fraction("1.6"), Fraction("0.63"))]
    assert pose_failures(Fraction(3), [AXIS, RATTLER], overlapping) == [
        "squares 0 and 1 overlap by 2.000e-02"
    ]
    verdict = verify_pose(pose_witness(Fraction(3), [AXIS, RATTLER], overlapping))
    assert verdict["passed"] is False
    assert verdict["exact_verify"]["passed"] is False
    assert verdict["independent"]["passed"] is False


def test_the_routes_refuse_a_pose_the_module_check_was_made_to_pass(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # With the module's own check disabled, the coarse rounding reaches the maintained
    # routes, which refuse it under a kind of their own: in a real run that would mean
    # the checkers disagree, not that the view failed.
    monkeypatch.setattr(same_side, "pose_failures", lambda *_args, **_kwargs: [])
    outcome = refusal(
        resolve_at_side(Fraction(3), [AXIS, RATTLER], RATTLER_VIEW, free_digits=(1,))
    )
    assert outcome.kind == "routes-refused"
    verdict = outcome.items[0]
    assert verdict["exact_verify"]["passed"] is False
    assert verdict["independent"]["passed"] is False


def test_an_empty_rounding_ladder_is_refused_only_when_unknowns_are_free() -> None:
    empty = refusal(resolve_at_side(Fraction(3), [AXIS, RATTLER], RATTLER_VIEW, free_digits=()))
    assert empty.kind == "malformed-input"
    assert "2 unknown(s) are free" in empty.detail
    pinned = resolve_at_side(Fraction(2), [AXIS], [(HALF, HALF)], free_digits=())
    assert resolved(pinned).free_unknowns == 0


def test_a_view_that_is_not_approximately_a_packing_is_refused() -> None:
    outcome = refusal(
        resolve_at_side(Fraction(2), [AXIS] * 2, [(HALF, HALF), (Fraction(14, 10), HALF)])
    )
    assert outcome.kind == "approximate-overlap"
    assert outcome.items == (
        {
            "constraint": "squares 0 and 1 along square 0's edge normal 0",
            "approx_gap": "-1.000e-01",
        },
    )


def test_counts_must_agree() -> None:
    outcome = refusal(resolve_at_side(Fraction(2), [AXIS] * 2, [(HALF, HALF)]))
    assert (outcome.kind, outcome.detail) == ("count-mismatch", "2 rotations, 1 centres")
    ids = refusal(resolve_at_side(Fraction(2), [AXIS], [(HALF, HALF)], ids=["a", "b"]))
    assert ids.kind == "count-mismatch"
    source = rational_witness(
        Fraction(3), [(HALF, HALF, AXIS), (Fraction(17, 10), Fraction(1), TILT)]
    )
    view = refusal(resolve_view(source, [(0.5, 0.5, AXIS)]))
    assert (view.kind, view.detail) == (
        "count-mismatch",
        "the view has 1 squares, the witness 2",
    )


def test_a_coordinate_no_witness_file_could_carry_is_refused() -> None:
    # A free x with a 5001-digit numerator, kept exactly by the last rung alone: the pose
    # is a packing, but its literal is past CPython's 4300-digit text limit.
    x = 1 + Fraction(1, 10**5000)
    outcome = refusal(resolve_at_side(Fraction(3), [AXIS], [(x, HALF)], free_digits=(None,)))
    assert outcome.kind == "literal-too-large"
    rounded = resolved(resolve_at_side(Fraction(3), [AXIS], [(x, HALF)]))
    assert rounded.centres == ((Fraction(1), HALF),)


def _base_call() -> dict[str, Any]:
    return {"side": "2", "rotations": [AXIS], "approx_centres": [("0.5", "0.5")]}


@pytest.mark.parametrize(
    ("argument", "value"),
    [
        pytest.param("side", "nan", id="side-nan"),
        pytest.param("side", "abc", id="side-text"),
        pytest.param("side", "1/0", id="side-zero-denominator"),
        pytest.param("side", "-1", id="side-negative"),
        pytest.param("side", "1e999999999", id="side-exponent-past-limit"),
        pytest.param("side", float("inf"), id="side-infinite-float"),
        pytest.param("side", True, id="side-boolean"),
        pytest.param("side", None, id="side-none"),
        pytest.param("approx_centres", [(float("inf"), "0.5")], id="centre-infinite"),
        pytest.param("approx_centres", [(True, "0.5")], id="centre-boolean"),
        pytest.param("approx_centres", [(None, "0.5")], id="centre-none"),
        pytest.param("approx_centres", [("0.5", "abc")], id="centre-text"),
        pytest.param("approx_centres", [("0.5",)], id="centre-not-a-pair"),
        pytest.param("rotations", [(0.6, 0.8)], id="rotation-floats"),
        pytest.param("rotations", [("1", "0")], id="rotation-text"),
        pytest.param("tight_tol", "nan", id="tight-tol-nan"),
        pytest.param("tight_tol", 0, id="tight-tol-zero"),
        pytest.param("move_limit", "-1e-7", id="move-limit-negative"),
        pytest.param("free_digits", (-1,), id="free-digits-negative"),
        pytest.param("free_digits", (True,), id="free-digits-boolean"),
        pytest.param("free_digits", (1.5,), id="free-digits-float"),
        pytest.param("on_conflict", "maybe", id="on-conflict-unknown"),
    ],
)
def test_malformed_inputs_are_refused_not_raised(argument: str, value: object) -> None:
    outcome = refusal(resolve_at_side(**{**_base_call(), argument: value}))
    assert outcome.kind == "malformed-input"
    assert outcome.summary()["status"] == "refused"


@pytest.mark.parametrize(
    ("argument", "value"),
    [
        pytest.param("side", "nan", id="side-nan"),
        pytest.param("tol", "abc", id="snap-tol-text"),
        pytest.param("tol", "-1e-9", id="snap-tol-negative"),
        pytest.param("verified_bound", "inf", id="verified-bound-inf"),
        pytest.param("tight_tol", "1e400x", id="tight-tol-text"),
        pytest.param("view_squares", [(0.5, 0.5, (1.0, 0.0))], id="view-basis-floats"),
        pytest.param("view_squares", [(0.5, 0.5)], id="view-square-not-a-triple"),
    ],
)
def test_malformed_view_inputs_are_refused_not_raised(argument: str, value: object) -> None:
    source = rational_witness(Fraction(2), [(HALF, HALF, AXIS)])
    call: dict[str, Any] = {"view_squares": [(0.5, 0.5, AXIS)], argument: value}
    assert refusal(resolve_view(source, **call)).kind == "malformed-input"


def test_rational_witnesses_without_an_exact_frame_are_refused() -> None:
    angled = rational_witness(Fraction(2), [(HALF, HALF, AXIS)])
    angled["representation"] = "center-angle"
    angled["coordinates"]["angle_unit"] = "degrees"
    angled["squares"] = [{"id": 1, "center": ["1/2", "1/2"], "angle": "0"}]
    assert refusal(source_frame(angled)).kind == "promotion-unsupported"
    assert refusal(resolve_view(angled, [(0.5, 0.5, AXIS)])).kind == "promotion-unsupported"
    garbled = rational_witness(Fraction(2), [(HALF, HALF, AXIS)])
    garbled["side"] = "two"
    assert refusal(source_frame(garbled)).kind == "malformed-input"


@pytest.mark.parametrize("option", ["--tight-tol", "--snap-tol", "--verified-bound"])
def test_the_command_line_refuses_a_malformed_option(
    option: str, capsys: pytest.CaptureFixture[str]
) -> None:
    witness = WITNESS_SCHEMA.parent / "known-best" / "n-025.yaml"
    assert main([str(witness), option, "nan"]) == 1
    printed = json.loads(capsys.readouterr().out)
    assert (printed["status"], printed["kind"]) == ("refused", "malformed-input")


def test_a_side_past_binary64_resolves_and_is_reported_exactly() -> None:
    result = resolved(resolve_at_side("1e400", [AXIS], [("0.5", "0.5")]))
    assert result.side == 10**400
    summary = result.summary()
    assert summary["side_decimal"] == "1e+400"
    # With no pair, the minimum pair gap is reported as the side itself.
    assert summary["verification"]["exact_verify"]["minimum_best_pair_gap"] == "1.000e+400"


def known_best(n: int) -> dict[str, Any]:
    path = WITNESS_SCHEMA.parent / "known-best" / f"n-{n:03d}.yaml"
    return load_witness(path, fallback_schema=WITNESS_SCHEMA)


def test_real_witnesses_resolve_from_their_own_floats_at_exactly_their_side() -> None:
    # n = 25, rational corners: the 5 x 5 grid, every contact already exact.
    grid = known_best(25)
    frame = source_frame(grid)
    assert not isinstance(frame, Refusal)
    outcome = resolve_view(grid, self_view(frame))
    assert isinstance(outcome, ViewResolution)
    assert outcome.resolved.side == Fraction(grid["side"])
    assert outcome.resolved.max_move == 0
    assert outcome.resolved.verification["passed"]
    # n = 26, decimal: nine squares at 45 degrees, re-solved at its 36-digit promotion's
    # side. Closing every tight contact is refused, because the 36-digit rotation leaves
    # loops open by about 1e-36 and the far walls hold the slack; `relax` leaves those.
    tilted = known_best(26)
    frame = source_frame(tilted)
    assert not isinstance(frame, Refusal)
    view = self_view(frame)
    assert refusal(resolve_view(tilted, view)).kind == "inconsistent-tight-set"
    outcome = resolve_view(tilted, view, on_conflict="relax")
    assert isinstance(outcome, ViewResolution)
    assert outcome.resolved.side == frame.side == frame.printed_side
    assert outcome.side_basis["scalar_kind"] == "decimal"
    assert outcome.snapped.summary()["to_source_rotation"] == 9
    assert outcome.snapped.moved == 0
    assert outcome.resolved.relaxed
    assert all(Fraction(item["forced_gap"]) > 0 for item in outcome.resolved.relaxed)
    assert outcome.resolved.max_move < Fraction(1, 10**9)
    assert outcome.resolved.verification["passed"]


def test_number_field_and_decimal_frames() -> None:
    assert refusal(source_frame(known_best(51))).kind == "unsupported-scalar-kind"
    decimal = {
        "id": "W-decimal-fixture",
        "n": 4,
        "side": "2",
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "radians",
        },
        "squares": [
            {"id": index, "center": center, "angle": "0"}
            for index, center in enumerate(
                [["0.5", "0.5"], ["1.5", "0.5"], ["0.5", "1.5"], ["1.5", "1.5"]], start=1
            )
        ],
        "claim": {"coordinate_provenance": "numerically-checked", "method": "numerical-f64"},
    }
    frame = source_frame(decimal)
    assert not isinstance(frame, Refusal)
    assert frame.side == 2
    outcome = resolve_view(decimal, self_view(frame), verified_bound="3")
    assert isinstance(outcome, ViewResolution)
    assert outcome.register["below_verified_bound"] is True
    assert outcome.side_basis["fits_printed_side"] is True


def drawn(
    x: Fraction, y: Fraction, angle: str, g: int, side: Fraction
) -> tuple[Fraction, Fraction, str]:
    """`reg.py` `d4`: `g & 3` quarter turns `(x, y) -> (S - y, x)`, then the mirror."""
    for _ in range(g & 3):
        x, y = side - y, x
    if g & 4:
        return side - x, y, f"-{angle}"
    return x, y, angle


def test_evand_view_undoes_the_drawing_orientation() -> None:
    side = Fraction(3)
    source = [(Fraction(1, 2), Fraction(5, 4), "10"), (Fraction(2), Fraction(7, 3), "0")]
    for g in (0, 3, 5, 6):
        rows = [[str(v) for v in drawn(x, y, angle, g, side)] for x, y, angle in source]
        view = evand_view({"orientation_g": g, "packing": {"S": "3", "sq": rows}})
        assert [(x, y) for x, y, _ in view] == [(x, y) for x, y, _ in source]
        for (_, _, basis), (_, _, angle) in zip(view, source, strict=True):
            target = basis_from_angle(angle)
            assert any(quarter_turn(basis, k) == target for k in range(4))


@cache
def vendored_d4() -> Callable[[dict[str, Any], int], dict[str, Any]]:
    """`reg.py`'s own `d4` and the `fold` it calls, compiled alone from the vendored file.

    Importing `reg` would pull in scipy and set mpmath's global precision to 80 digits;
    `d4` needs neither, only `mpm.floor` inside `fold`.
    """
    tree = ast.parse(REG.read_text(encoding="utf-8"), filename=str(REG))
    wanted: list[ast.stmt] = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in {"d4", "fold"}
    ]
    assert sorted(node.name for node in wanted if isinstance(node, ast.FunctionDef)) == [
        "d4",
        "fold",
    ]
    namespace: dict[str, Any] = {"mpm": mpmath}
    exec(compile(ast.Module(wanted, type_ignores=[]), str(REG), "exec"), namespace)
    return namespace["d4"]


@pytest.mark.parametrize("g", [1, 2, 3, 4, 5, 6, 7])
def test_evand_view_inverts_the_vendored_d4_on_a_fifty_digit_record(g: int) -> None:
    # A source drawn by the generator's own `d4` in orientation `g`, written at 50
    # digits as the shim writes `packing`, comes back to the source frame within the
    # printing, and each rotation to the source's exactly up to a quarter turn.
    xs, ys = [Fraction(1, 3), Fraction(2)], [Fraction(5, 4), Fraction(7, 3)]
    with mpmath.workdps(60):
        source = {
            "S": mpmath.mpf(3),
            "X": [mpmath.mpf(x.numerator) / x.denominator for x in xs],
            "Y": [mpmath.mpf(y.numerator) / y.denominator for y in ys],
            "T": [mpmath.mpf(10) / 3, mpmath.mpf(-20)],
        }
        drawn = vendored_d4()(source, g)
        rows = zip(drawn["X"], drawn["Y"], drawn["T"], strict=True)
        record = {
            "orientation_g": g,
            "packing": {
                "S": mpmath.nstr(drawn["S"], 50),
                "sq": [[mpmath.nstr(value, 50) for value in row] for row in rows],
            },
        }
        angles = [str(mpmath.nstr(angle, 50)) for angle in source["T"]]
    view = evand_view(record)
    for (x, y, _), x_source, y_source in zip(view, xs, ys, strict=True):
        assert max(abs(Fraction(x) - x_source), abs(Fraction(y) - y_source)) < Fraction(
            1, 10**48
        )
    snapped = snap_rotations(
        [basis for _, _, basis in view], [basis_from_angle(angle) for angle in angles]
    )
    assert isinstance(snapped, Snapped)
    assert [(snap.target, snap.deviation) for snap in snapped.snaps] == [(0, 0), (1, 0)]


def test_nearly_parallel_contacts_are_not_closed_beyond_the_move_limit() -> None:
    # An aligned square on the floor against the left wall, and a square turned by
    # t = 1e-7, whose edge normal is 2e-7 from the x axis, touching it and the right
    # wall. With both walls closed, the pair's row pins only `y` of the turned square,
    # through a 2e-7 coefficient; the view has it 1e-6 high, so closing everything
    # would move it 1e-6, ten times the move limit.
    tilt = basis_from_half_tangent(Fraction(1, 10**7))
    c, s = tilt
    extent = (c + s) / 2
    x_turned = HALF + (extent + HALF - s * Fraction(1, 10)) / c
    side = x_turned + extent
    rotations = [AXIS, tilt]
    view = [(HALF, HALF), (x_turned, Fraction(6, 10) + Fraction(1, 10**6))]
    outcome = refusal(resolve_at_side(side, rotations, view))
    assert outcome.kind == "ill-conditioned-tight-set"
    assert outcome.items[0]["constraint"] == "square 1 on the right wall"
    assert outcome.items[0]["predicted_shift"] == "1.000e-06"
    relaxed = resolved(resolve_at_side(side, rotations, view, on_conflict="relax"))
    assert [item["relaxed"] for item in relaxed.relaxed] == ["ill-conditioned"]
    assert 0 < Fraction(relaxed.relaxed[0]["gap_after"]) < Fraction(1, 10**12)
    assert relaxed.max_move < Fraction(1, 10**12)
    closed = resolved(resolve_at_side(side, rotations, view, move_limit=Fraction(1, 10**5)))
    assert closed.relaxed == ()
    assert closed.centres[1] == (x_turned, Fraction(6, 10))
    assert closed.max_move == Fraction(1, 10**6)
