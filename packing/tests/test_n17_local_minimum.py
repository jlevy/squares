"""Exact first-order parts of the n17 local-minimum checker (H-261, BC-407)."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import replace
from fractions import Fraction as Q
from functools import cache
from pathlib import Path

import pytest

from devtools import check_n17_local_minimum as local
from devtools.check_n17_contact_chart import CONTACTS


@cache
def _target() -> local.Model:
    midpoint, _ = local.read_point(local.ROOT_CERTIFICATE.read_bytes())
    return local.build_model(*midpoint)


@cache
def _space() -> local.Quotient:
    return local.quotient(_target())


@cache
def _solved(name: str, sign: int) -> local.DirectionSolution:
    return local.solve_direction(_target(), _space(), name, sign)


def test_six_prescribed_zero_weights_and_52_positive_rows() -> None:
    audit = local.weight_audit(_target())
    assert audit["passed"]
    assert audit["zero_weight_rows"] == sorted(map(local.row_label, local.ZERO_WEIGHT_KEYS))
    assert audit["positive_weight_rows"] == 52
    # The midpoint is not the root: only the two prescribed F2 columns are off zero.
    omega12, omega16 = local.column(12, "angle"), local.column(16, "angle")
    assert set(audit["stress_residual_columns_at_point"]) == {str(omega12), str(omega16)}


def test_coordinates_annihilate_the_sliders_and_number_ninety_directions() -> None:
    model = _target()
    covectors = local.coordinates(model)
    assert len(covectors) == 45
    assert len(local.directions(model)) == 90
    assert model.u[0] ** 2 + model.u[1] ** 2 == 1
    for vector in local.slider_generators(model).values():
        for covector in covectors.values():
            assert sum((covector.get(i, Q(0)) * v for i, v in vector.items()), Q(0)) == 0


def test_kernel_is_exactly_the_slider_span_with_two_lineality_directions() -> None:
    audit = local.kernel_audit(_target())
    assert audit["passed"]
    assert (audit["rank_positive"], audit["kernel_dimension"], audit["rank_all"]) == (46, 6, 50)
    assert (audit["rank_positive_mod_p"], audit["rank_all_mod_p"]) == (46, 50)
    assert audit["lineality_generators"] == ["v13", "xi6"]
    zero_rows = audit["generator_values_on_zero_weight_rows"]
    assert zero_rows["xi5"] == {"wall:5:right:0": "-1", "wall:5:right:1": "-1"}
    assert zero_rows["v11"] == {"pair:9:11:0": "-1", "pair:9:11:1": "-1"}
    assert zero_rows["omega6"] == {"wall:6:bottom:0": "-1/2", "wall:6:bottom:1": "1/2"}


def test_rank_helpers_on_a_known_deficient_matrix() -> None:
    rows = [[Q(1), Q(2), Q(3)], [Q(2), Q(4), Q(6)], [Q(0), Q(1), Q(1, 2)]]
    assert local.exact_rank(rows) == 2
    assert local.modular_rank(rows) == 2


@pytest.mark.parametrize(
    ("name", "sign", "prefix"),
    [
        ("omega11", -1, "175.848328842"),
        ("omega16", -1, "74.1727814434"),
        ("eta16", 1, "12.0116678565"),
        ("xi17", 1, "1"),
        ("xi1", -1, "0"),
    ],
)
def test_selected_coordinate_duals_are_exact_optima(name: str, sign: int, prefix: str) -> None:
    solution = _solved(name, sign)
    assert solution.status == "certified_optimal"
    assert solution.a is not None
    assert local.decimal(solution.a).startswith(prefix)
    assert all(value > 0 for value in solution.lam.values())
    assert set(solution.lam) <= set(_target().positive_keys)
    assert local.verify_solution(_target(), _space(), solution)


def test_tampered_certificates_are_rejected() -> None:
    solution = _solved("omega11", -1)
    assert solution.a is not None
    key = next(iter(solution.lam))
    bumped = {**solution.lam, key: solution.lam[key] + Q(1, 10**9)}
    negated = {**solution.lam, key: -solution.lam[key]}
    for tampered in (
        replace(solution, lam=bumped),
        replace(solution, lam=negated),
        replace(solution, a=solution.a - Q(1, 10**9)),
        replace(solution, sign=1),
        replace(solution, status="undecided"),
    ):
        assert not local.verify_solution(_target(), _space(), tampered)


def test_unavailable_owner_alternatives_are_strictly_negative() -> None:
    audit = local.owner_alternative_audit(_target())
    assert audit["passed"]
    assert audit["unavailable"] == audit["strictly_negative"] == 135
    assert audit["identity_options"] == 33
    assert audit["identity_exact_zero"] == 31
    leading = [row["margin_decimal"][:7] for row in audit["least_negative"][:4]]
    assert leading == ["-0.0557", "-0.0557", "-0.0707", "-0.1474"]
    assert {tuple(row["pair"]) for row in audit["least_negative"][:2]} == {(7, 14), (14, 17)}


def test_kernel_row_control_is_refused() -> None:
    result = local.run_control(_target(), "kernel-row")
    assert result["refused"]
    assert "kernel.kernel_equals_slider_span" in result["failed_checks"]


def test_infeasible_dual_control_keeps_the_kernel_and_loses_the_dual() -> None:
    result = local.run_control(_target(), "infeasible-dual")
    assert result["refused"]
    assert all(result["kernel_checks"].values())
    assert result["direction"]["status"] == "no_nonnegative_dual"
    assert result["failed_checks"] == ["duals.-omega11"]


@pytest.mark.parametrize(
    ("control", "failed"), [("kernel-row", "kernel"), ("infeasible-dual", "duals")]
)
def test_cli_refuses_each_control(
    control: str,
    failed: str,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    output = tmp_path / "receipt.json"
    assert local.main(["--control", control, "--output", str(output)]) == 1
    receipt = json.loads(output.read_text())
    raw = local.ROOT_CERTIFICATE.read_bytes()
    assert receipt["inputs"]["root_certificate_git_ref"] == local.FROZEN_ROOT_REF
    assert receipt["passed"] is False
    assert receipt["checks"][failed] is False
    assert receipt["inputs"]["root_certificate_sha256"] == hashlib.sha256(raw).hexdigest()
    assert json.loads(capsys.readouterr().out)["passed"] is False


def test_cli_rejects_unbound_or_malformed_input(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The root is named by revision and path; a copy elsewhere is not that root."""
    copy_elsewhere = tmp_path / "certificate.json"
    copy_elsewhere.write_bytes(local.ROOT_CERTIFICATE.read_bytes())
    assert local.main([str(copy_elsewhere)]) == 2
    assert "expected the retained" in json.loads(capsys.readouterr().out)["error"]
    malformed = tmp_path / "root.json"
    malformed.write_text("{}")
    monkeypatch.setattr(local, "require_retained_path", lambda _path, _reference: None)
    assert local.main([str(malformed)]) == 2
    assert json.loads(capsys.readouterr().out)["passed"] is False


# The ratio test over the slider box (recipe C3, C4, C6, C7, C8, C9, C12).


@cache
def _family() -> local.Family:
    midpoint, _ = local.read_point(local.ROOT_CERTIFICATE.read_bytes())
    return local.build_family(*midpoint)


@cache
def _affine() -> tuple[local.AffineMatrix, dict[str, object]]:
    return local.affine_audit(_family(), local.DECLARED_BOX)


@cache
def _curvature() -> tuple[Q, ...]:
    radii = dict.fromkeys(_family().names, local.DECLARED_RADIUS)
    return local.curvature_audit(_family(), local.DECLARED_BOX, radii)[0]


@cache
def _outcome(name: str, sign: int) -> local.CoordinateOutcome:
    matrix, _ = _affine()
    family = _family()
    return local.certify_coordinate(
        matrix,
        local.float_system(matrix, 45),
        _curvature(),
        [local.DECLARED_RADIUS] * 45,
        names=family.names,
        name=name,
        sign=sign,
        box=local.DECLARED_BOX,
    )


# B_W' of H-268: the declared box with its b floor lowered to -2r, below b* = -1.685 r.
WIDENED_BOX_ARGUMENTS = ("0", "1/4", "-1/2500", "1/12", "-1/8", "1/16")
WIDENED_BOX = local.slider_box([Q(value) for value in WIDENED_BOX_ARGUMENTS])
EXP244_RUN = (
    local.REPO
    / "packing/campaign/series/series-000-smoke-and-calibration/results"
    / "exp-244-n17-local-minimum/run-001"
)


def _box_record(box: Sequence[tuple[Q, Q]]) -> dict[str, list[str]]:
    return {
        name: [str(lo), str(hi)]
        for name, (lo, hi) in zip(local.SLIDER_PARAMETERS, box, strict=True)
    }


def _family_offset(pair: tuple[int, int], w: local.Point) -> Q:
    axis = next(axis for left, right, axis, _ in CONTACTS if (left, right) == pair)
    return local.face_offset(pair, axis, _family().aux, local.moved_centres(_family(), w))


def test_default_box_replays_the_committed_exp244_receipt() -> None:
    """The default run at B_W is exp-244's: same box, constants, residuals and verdicts.

    The certificates are the committed run's, bound to its receipt by digest, and replay
    through the current code at `DECLARED_BOX` to the receipt's C8/C9 result exactly.
    """
    receipt = json.loads((EXP244_RUN / "receipt.json").read_text())
    raw = (EXP244_RUN / "certificates.json").read_bytes()
    assert (
        hashlib.sha256(raw.rstrip(b"\n")).hexdigest()
        == (receipt["inputs"]["certificates_sha256"])
    )
    assert receipt["slider_box"] == _box_record(local.DECLARED_BOX)
    assert receipt["radius"]["uniform"] == str(local.DECLARED_RADIUS)
    documents = json.loads(raw)
    records = {record["direction"]: record for record in receipt["c8_c9"]["results"]}
    for document in documents:
        digest = hashlib.sha256(json.dumps(document["cells"], sort_keys=True).encode())
        assert digest.hexdigest() == records[document["direction"]]["duals_sha256"]
    family = _family()
    matrix, _ = _affine()
    _, radii = local.read_point(local.ROOT_CERTIFICATE.read_bytes())
    enclosure = local.root_enclosure(family, radii)
    deviation, root = local.root_box_audit(family, enclosure, local.DECLARED_BOX, matrix)
    assert root["row_deviation_sha256"] == receipt["c8i_root_box"]["row_deviation_sha256"]
    uniform = dict.fromkeys(family.names, local.DECLARED_RADIUS)
    curvature, detail = local.curvature_audit(family, local.DECLARED_BOX, uniform, enclosure)
    assert detail["sha256"] == receipt["c7_curvature"]["sha256"]
    replay = local.replay_certificates(
        matrix,
        curvature,
        [local.DECLARED_RADIUS] * 45,
        names=family.names,
        documents=documents,
        box=local.DECLARED_BOX,
        deviation=deviation,
    )
    assert replay == receipt["c8_c9_replay"]
    assert replay["worst_ratio"] == receipt["c8_c9"]["worst"]["worst_ratio"]
    assert replay["cells"] == receipt["c8_c9"]["total_cells"] == 93


def test_box_option_defaults_to_the_declared_box(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    seen: list[object] = []

    def stub(*_point: Q, box: object, **_options: object) -> None:
        seen.append(box)
        raise ValueError("stopped after the box was read")

    monkeypatch.setattr(local, "ratio_certify", stub)
    assert local.main(["--ratio"]) == 2
    assert local.main(["--ratio", "--box", *WIDENED_BOX_ARGUMENTS]) == 2
    assert seen[0] is local.DECLARED_BOX
    assert (
        seen[1]
        == WIDENED_BOX
        == ((Q(0), Q(1, 4)), (Q(-1, 2500), Q(1, 12)), (Q(-1, 8), Q(1, 16)))
    )
    capsys.readouterr()
    for empty in (("0", "1/4", "1/12", "0", "-1/8", "1/16"), ("0", "0", "0", "1", "0", "1")):
        assert local.main(["--ratio", "--box", *empty]) == 2
        assert "LO < HI" in json.loads(capsys.readouterr().out)["error"]
    assert len(seen) == 2
    with pytest.raises(ValueError, match="six exact rationals"):
        local.slider_box([Q(0), Q(1)])


@pytest.mark.parametrize(
    ("bounds", "face"),
    [
        (("0", "1/4", "-1/16", "1/12", "-1/8", "1/16"), "11/12"),
        (("-1/1000", "1/4", "0", "1/12", "-1/8", "1/16"), "5/7"),
        (("0", "1/4", "0", "1/12", "-1/8", "1/10"), "13/14"),
    ],
)
def test_a_box_leaving_a_tau_branch_is_refused_before_any_dual(
    bounds: tuple[str, ...],
    face: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    box = local.slider_box([Q(value) for value in bounds])
    assert local.sign_branch_audit(_family(), box)["failures"] == [face]

    def unreachable(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("the C4 audit ran on a box outside the tau branches")

    monkeypatch.setattr(local, "affine_audit", unreachable)
    assert local.main(["--ratio", "--box", *bounds]) == 2
    assert json.loads(capsys.readouterr().out)["error"].endswith(f"face {face}")


def test_the_b_floor_may_approach_the_11_12_branch_but_not_reach_it() -> None:
    delta = _family_offset((11, 12), (Q(0), Q(0), Q(0)))
    assert Q(56, 1000) < delta < Q(57, 1000)
    for b in (Q(-1, 2500), Q(1, 12), -delta):
        assert _family_offset((11, 12), (Q(0), b, Q(0))) == delta + b
    for floor, failures in ((-delta + Q(1, 10**9), []), (-delta, ["11/12"])):
        box = ((Q(0), Q(1, 4)), (floor, Q(1, 12)), (Q(-1, 8), Q(1, 16)))
        assert local.sign_branch_audit(_family(), box)["failures"] == failures
    widened = local.sign_branch_audit(_family(), WIDENED_BOX)
    assert widened["passed"]
    assert widened["faces"]["11/12"]["min_decimal"] == local.decimal(delta - Q(1, 2500), 12)


def test_a_negative_b_floor_keeps_the_affine_map_and_the_stress() -> None:
    family = _family()
    matrix, audit = local.affine_audit(family, WIDENED_BOX)
    assert audit["passed"]
    # Pinned at the widened box's own corner, the affine map is the B_W one exactly.
    assert matrix == _affine()[0]
    stress = local.stress_audit(family, WIDENED_BOX)
    assert stress["passed"]
    assert stress["vertex_ranks_mod_p"] == [46] * 8
    assert stress["rows_reaching_zero"] == []
    assert stress["least_weight"]["vertex"] == ["0", "1/12", "-1/8"]
    # At b < 0 the family overlaps 9 and 11 by |b| across the dropped 9/11 face: its
    # offset does not move, and its weights stay exactly zero at the b-floor vertices.
    vx, vy = family.aux["v"]
    for b in (Q(-1, 2500), Q(1, 12)):
        moved = local.moved_centres(family, (Q(0), b, Q(0)))
        base = family.centres
        gap = -(vx * (moved[10][0] - moved[8][0]) + vy * (moved[10][1] - moved[8][1]))
        assert gap - -(vx * (base[10][0] - base[8][0]) + vy * (base[10][1] - base[8][1])) == b
        offset = _family_offset((9, 11), (Q(0), b, Q(0)))
        assert offset == _family_offset((9, 11), (Q(0), Q(0), Q(0)))
    weights, _ = local.family_stress(family, (Q(0), Q(-1, 2500), Q(-1, 8)))
    assert all(weights[key] == 0 for key in local.ZERO_WEIGHT_KEYS)


def test_a_negative_b_floor_keeps_curvature_options_and_the_minus_omega11_ratio() -> None:
    family = _family()
    radii = dict.fromkeys(family.names, local.DECLARED_RADIUS)
    # Every centre separation is largest at b = 1/12, so C7 does not move.
    assert local.curvature_audit(family, WIDENED_BOX, radii)[0] == _curvature()
    options = local.unavailable_option_audit(family, WIDENED_BOX, radii)
    assert options["passed"]
    assert options["least_negative"][0]["worst_margin_decimal"].startswith("-0.05527")
    matrix, _ = _affine()
    outcome = local.certify_coordinate(
        matrix,
        local.float_system(matrix, 45),
        _curvature(),
        [local.DECLARED_RADIUS] * 45,
        names=family.names,
        name="omega11",
        sign=-1,
        box=WIDENED_BOX,
    )
    assert outcome.passed
    assert local.tiling_audit([dual.cell for dual, _ in outcome.certificates], WIDENED_BOX)
    assert Q(9, 10) < Q(local.outcome_record(outcome)["worst_ratio"]) < 1


def test_family_rows_at_the_origin_are_the_frozen_h258_rows_and_affine_in_the_sliders() -> None:
    matrix, audit = _affine()
    assert audit["passed"]
    assert audit["checks"] == {
        "identity_at_eleven_points": True,
        "support_as_stated": True,
        "rows_at_origin_equal_frozen_h258_rows": True,
        "rank_at_origin_45": True,
    }
    family = _family()
    omega5, omega7 = family.names.index("omega5"), family.names.index("omega7")
    rows = {key: index for index, key in enumerate(family.keys)}
    # Only the (5,7) moment arm k = (1 - a)/2 moves with a: d/da of tau/2 + k is -1.
    assert matrix.slopes[0][rows["pair", 5, 7, 0]] == {omega5: Q(-1)}
    assert matrix.slopes[0][rows["pair", 5, 7, 1]] == {omega7: Q(-1)}
    assert len(family.keys) == 52
    assert not set(family.keys) & local.ZERO_WEIGHT_KEYS


def test_perturbed_slope_control_is_refused() -> None:
    _, audit = local.affine_audit(_family(), local.DECLARED_BOX, perturb=True)
    assert not audit["passed"]
    assert not audit["checks"]["identity_at_eleven_points"]
    assert not audit["checks"]["support_as_stated"]


def test_sign_branches_hold_on_the_declared_box_and_a_flipped_branch_is_refused() -> None:
    audit = local.sign_branch_audit(_family(), local.DECLARED_BOX)
    assert audit["passed"]
    assert audit["faces"]["5/7"]["min_decimal"] == "-0.25"
    crossing = Q(audit["tau_13_14_zero_at_z"])
    assert Q(1, 16) < crossing < Q(81, 1000)
    assert audit["tau_13_14_slope_in_z"] == "-1"
    flipped = local.build_family(
        _family().t, _family().beta, branches={**local.FACE_BRANCHES, (5, 7): 1}
    )
    refused = local.sign_branch_audit(flipped, local.DECLARED_BOX)
    assert refused["failures"] == ["5/7"]
    wide = ((Q(0), Q(1, 4)), (Q(0), Q(1, 12)), (Q(-1, 8), Q(1, 10)))
    assert local.sign_branch_audit(_family(), wide)["failures"] == ["13/14"]


def test_curvature_constants_follow_the_n11_formula() -> None:
    radius = local.DECLARED_RADIUS
    curvature = _curvature()
    family = _family()
    walls = {curvature[i] for i, key in enumerate(family.keys) if key[0] == "wall"}
    assert walls == {local.INVERSE_ROOT2_UPPER * radius * radius}
    assert 2 * local.INVERSE_ROOT2_UPPER**2 > 1
    assert all(
        8 * radius**2 < value < 10 * radius**2 for value in curvature if value not in walls
    )
    assert local.pair_curvature(Q(2), Q(3), Q(5), Q(7), Q(1, 2)) == 50 + 30 + 72
    for value in (Q(0), Q(2), Q(1, 3), Q(10**6 + 1, 7)):
        upper = local.sqrt_upper(value)
        assert upper**2 >= value
        assert (
            upper - Q(1, local.SQRT_SCALE) < 0 or (upper - Q(1, local.SQRT_SCALE)) ** 2 < value
        )
    with pytest.raises(ValueError, match="nonnegative"):
        local.sqrt_upper(Q(-1))


def test_ratio_test_is_strict_and_agrees_with_the_n11_consumer() -> None:
    from devtools import check_n11_optimality_local_isolation as n11  # noqa: PLC0415

    assert local.ratio_test(Q(2), Q(1, 4), Q(2), Q(1)) == (True, Q(1, 3))
    assert local.ratio_test(Q(2), Q(1, 4), Q(2), Q(3)) == (False, Q(1))
    assert local.ratio_test(Q(1), Q(1), Q(1), Q(1)) == (False, None)
    for case in ((Q(2), Q(1, 4), Q(2), Q(1)), (Q(3, 7), Q(1, 9), Q(1, 2), Q(1, 5))):
        assert local.ratio_test(*case)[1] == n11.strict_dual_margin(*case)


def test_minus_omega11_passes_on_tiling_cells_with_its_worst_ratio_below_one() -> None:
    outcome = _outcome("omega11", -1)
    assert outcome.passed
    cells = [dual.cell for dual, _ in outcome.certificates]
    assert local.tiling_audit(cells, local.DECLARED_BOX)
    record = local.outcome_record(outcome)
    assert record["cells"] == len(cells) <= 16
    assert Q(9, 10) < Q(record["worst_ratio"]) < 1
    assert all(
        verdict["nonnegative"] and verdict["epsilon"] < Q(1, 10)
        for _, verdict in outcome.certificates
    )


def test_single_cell_directions_pass_with_small_ratios() -> None:
    for name, sign in (("u11", -1), ("xi1", 1), ("omega16", -1)):
        record = local.outcome_record(_outcome(name, sign))
        assert record["passed"]
        assert record["cells"] == 1
        assert Q(record["worst_ratio"]) < Q(1, 2)


def test_negative_vertex_dual_and_wider_radius_are_refused() -> None:
    outcome = _outcome("omega11", -1)
    matrix, _ = _affine()
    coordinate = _family().names.index("omega11")
    dual = outcome.certificates[0][0]
    negative = local.evaluate_dual(
        matrix,
        _curvature(),
        [local.DECLARED_RADIUS] * 45,
        coordinate=coordinate,
        sign=-1,
        dual=local.negative_vertex_control(dual),
    )
    assert negative["vertex_min"] == Q(-1, 10**6)
    assert not negative["nonnegative"]
    assert not negative["passed"]
    radii = dict.fromkeys(_family().names, 2 * local.DECLARED_RADIUS)
    wide, _ = local.curvature_audit(_family(), local.DECLARED_BOX, radii)
    verdicts = [
        local.evaluate_dual(
            matrix,
            wide,
            [2 * local.DECLARED_RADIUS] * 45,
            coordinate=coordinate,
            sign=-1,
            dual=item,
        )
        for item, _ in outcome.certificates
    ]
    assert not any(verdict["passed"] for verdict in verdicts)


def test_certificates_replay_from_json_and_tampering_is_refused() -> None:
    outcome = _outcome("omega11", -1)
    matrix, _ = _affine()
    documents = [
        {
            "direction": "-omega11",
            "cells": [local.dual_document(dual) for dual, _ in outcome.certificates],
        }
    ]
    stored = json.loads(json.dumps(documents))
    replay = local.replay_certificates(
        matrix,
        _curvature(),
        [local.DECLARED_RADIUS] * 45,
        names=_family().names,
        documents=stored,
        box=local.DECLARED_BOX,
    )
    assert replay["failures"] == []
    assert not replay["complete"]
    assert replay["worst_ratio"] == local.outcome_record(outcome)["worst_ratio"]
    scaled = json.loads(json.dumps(stored))
    scaled[0]["cells"][0]["lambda"] = [2 * value for value in scaled[0]["cells"][0]["lambda"]]
    missing = json.loads(json.dumps(stored))
    missing[0]["cells"].pop()
    for tampered in (scaled, missing):
        result = local.replay_certificates(
            matrix,
            _curvature(),
            [local.DECLARED_RADIUS] * 45,
            names=_family().names,
            documents=tampered,
            box=local.DECLARED_BOX,
        )
        assert result["failures"] == ["-omega11"]


def test_tiling_audit_rejects_gaps_and_overlaps() -> None:
    whole = local.Cell((Q(0), Q(0), Q(-1, 8)), (Q(1, 4), Q(1, 12), Q(1, 16)))
    left, right = whole.split(1)
    assert local.tiling_audit([left, right], local.DECLARED_BOX)
    assert not local.tiling_audit([left], local.DECLARED_BOX)
    assert not local.tiling_audit([whole, left], local.DECLARED_BOX)


def test_unavailable_options_stay_negative_and_the_largest_corner_is_refused() -> None:
    family = _family()
    radii = dict.fromkeys(family.names, local.DECLARED_RADIUS)
    audit = local.unavailable_option_audit(family, local.DECLARED_BOX, radii)
    assert audit["passed"]
    assert audit["options"] == audit["strictly_negative"] == 125
    leading = audit["least_negative"][0]
    assert leading["base_gap_decimal"].startswith("-0.0557998")
    assert leading["worst_margin_decimal"].startswith("-0.05527")
    # The chosen corner gap at the origin is the point checker's support margin.
    point = {
        (tuple(row["pair"]), row["owner"], row["axis"], row["sign"]): row["margin_decimal"]
        for row in local.owner_alternative_audit(_target())["margins"]
    }
    for row in audit["least_negative"]:
        key = (tuple(row["pair"]), row["owner"], row["axis"], row["sign"])
        assert point[key] == row["base_gap_decimal"]
    control = local.unavailable_option_audit(
        family, local.DECLARED_BOX, radii, largest_corner=True
    )
    assert not control["passed"]


@pytest.mark.parametrize("box", [(), WIDENED_BOX_ARGUMENTS], ids=["default", "widened"])
def test_cli_ratio_mode_without_the_n11_replay(
    box: tuple[str, ...],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # C11 has its own test; a stub keeps this wiring test fast and shows it is load-bearing.
    monkeypatch.setattr(local, "stress_audit", lambda _family, _box: {"passed": False})
    output = tmp_path / "ratio.json"
    partial = ["--direction", "omega11:-1", "--direction", "u11:1"]
    command = [
        "--ratio",
        "--no-n11",
        "--midpoint-only",
        *(("--box", *box) if box else ()),
        *partial,
        "--output",
        str(output),
    ]
    assert local.main(command) == 1
    receipt = json.loads(output.read_text())
    assert receipt["schema"] == local.RATIO_SCHEMA
    declared = local.slider_box([Q(value) for value in box]) if box else local.DECLARED_BOX
    assert receipt["slider_box"] == _box_record(declared)
    # The items read the declared box's own vertices: the 11/12 offset at its b floor.
    floor = _family_offset((11, 12), (Q(0), declared[1][0], Q(0)))
    assert receipt["c3_sign_branches"]["faces"]["11/12"]["min_decimal"] == local.decimal(
        floor, 12
    )
    assert receipt["inputs"]["core_stress_commit"] == "2fbf8d29"
    assert receipt["checks"]["c8_c9_every_direction"]
    assert receipt["checks"]["c12_controls"]
    # A partial run cannot pass: two of 90 directions, and no root-box items.
    assert not receipt["checks"]["c8_c9_replayed_from_certificates"]
    assert not receipt["checks"]["c8i_root_box"]
    assert not receipt["checks"]["c11_stress_on_the_box"]
    assert receipt["checks"]["c1_roster_binding"]
    assert json.loads(capsys.readouterr().out)["passed"] is False
    assert local.main(["--ratio", "--radius", "1/10"]) == 2
    assert "radius" in json.loads(capsys.readouterr().out)["error"]


EXP248_RUN = (
    local.REPO
    / "packing/campaign/series/series-000-smoke-and-calibration/results"
    / "exp-248-n17-local-half-composition/run-002"
)


@pytest.mark.slow
def test_cli_ratio_on_the_widened_box_passes_end_to_end_as_exp248_run_002(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """exp-248 run-002's recipe exactly replays newly searched duals at least as strong as
    the retained bound.

    The receipt records the core-stress blob that ran and gates on nothing about it
    (OR-16), so an edit to `check_n17_core_stress.py` that leaves every mathematical
    check true cannot turn the run red, as the pinned blob once did.
    """
    output, certificates = tmp_path / "receipt.json", tmp_path / "certificates.json"
    command = ["--ratio", "--box", *WIDENED_BOX_ARGUMENTS, "--output", str(output)]
    assert local.main([*command, "--certificates", str(certificates)]) == 0
    summary = json.loads(capsys.readouterr().out.splitlines()[-1])
    receipt = json.loads(output.read_text())
    retained = json.loads((EXP248_RUN / "receipt.json").read_text())
    assert summary["passed"] is True
    assert receipt["passed"]
    assert all(receipt["checks"].values())
    assert set(receipt["checks"]) == set(retained["checks"]) - {"core_stress_matches_commit"}
    assert receipt["inputs"]["core_stress_commit"] == local.CORE_STRESS_COMMIT
    assert receipt["inputs"]["core_stress_blob"] == local.core_stress_blob()
    assert "core_stress_matches_commit" not in receipt["inputs"]
    assert receipt["slider_box"] == retained["slider_box"] == _box_record(WIDENED_BOX)
    worst, kept = receipt["c8_c9"]["worst"], retained["c8_c9"]["worst"]
    assert worst["direction"] == kept["direction"]
    # HiGHS proposes floating multipliers; their 44-bit rationalization can differ
    # across builds. All exact certificate replays above must pass, and the fresh
    # certified bound must be at least as strong as the retained one, without slack.
    assert 0 < Q(worst["worst_ratio"]) <= Q(kept["worst_ratio"]) < 1
    assert receipt["c8_c9"]["total_cells"] == retained["c8_c9"]["total_cells"] == 93
    assert receipt["radius"]["uniform"] == str(local.DECLARED_RADIUS)
    family = _family()
    matrix, _ = local.affine_audit(family, WIDENED_BOX)
    _, root_radii = local.read_point(local.ROOT_CERTIFICATE.read_bytes())
    enclosure = local.root_enclosure(family, root_radii)
    deviation, _ = local.root_box_audit(family, enclosure, WIDENED_BOX, matrix)
    curvature, _ = local.curvature_audit(
        family, WIDENED_BOX, dict.fromkeys(family.names, local.DECLARED_RADIUS), enclosure
    )
    replay = local.replay_certificates(
        matrix,
        curvature,
        [local.DECLARED_RADIUS] * 45,
        names=family.names,
        documents=json.loads(certificates.read_text()),
        box=WIDENED_BOX,
        deviation=deviation,
    )
    assert replay == receipt["c8_c9_replay"]
    assert replay["passed"]
    assert replay["complete"]
    assert replay["directions"] == 90
    assert replay["worst_ratio"] == worst["worst_ratio"]
    assert 0 <= Q(replay["worst_ratio"]) < 1


def test_affine_structure_holds_at_symbolic_root_parameters() -> None:
    matrix, _ = _affine()
    audit = local.symbolic_affine_audit(_family(), matrix)
    assert audit["passed"]
    assert audit["entries"] == 52 * 45
    assert audit["offsets"] == {"1/2": True, "1/3": True, "5/7": True}


def test_root_box_deviation_is_tiny_and_folds_into_the_residual() -> None:
    matrix, _ = _affine()
    family = _family()
    _, radii = local.read_point(local.ROOT_CERTIFICATE.read_bytes())
    enclosure = local.root_enclosure(family, radii)
    deviation, audit = local.root_box_audit(family, enclosure, local.DECLARED_BOX, matrix)
    assert audit["passed"]
    assert audit["midpoint_entries_contained"]
    assert 0 < max(deviation) < Q(1, 10**18)
    outcome = _outcome("omega11", -1)
    coordinate = family.names.index("omega11")
    dual, plain = outcome.certificates[0]
    folded = local.evaluate_dual(
        matrix,
        _curvature(),
        [local.DECLARED_RADIUS] * 45,
        coordinate=coordinate,
        sign=-1,
        dual=dual,
        deviation=deviation,
    )
    assert folded["root_box_residual"] > 0
    assert folded["epsilon"] == plain["epsilon"] + folded["root_box_residual"]
    assert folded["passed"]
    widened = [value * 10**19 for value in deviation]
    refused = local.evaluate_dual(
        matrix,
        _curvature(),
        [local.DECLARED_RADIUS] * 45,
        coordinate=coordinate,
        sign=-1,
        dual=dual,
        deviation=widened,
    )
    assert not refused["passed"]


def test_slides_leave_every_retained_contact_and_anchor_unchanged() -> None:
    slides = local.slide_invariance_audit(_family())
    assert slides["passed"]
    assert slides["identity_options"] == slides["slide_invariant"] == 27
    # Only the two closing contacts carry the midpoint's residual, far below any margin.
    assert set(slides["nonzero_at_midpoint"]) == {"12/16:12:u:1", "16/17:16:p:1"}
    spanning = local.spanning_audit()
    assert spanning["passed"]
    assert spanning["walls"] == {
        "left": [1, 3, 4, 9],
        "right": [7, 8, 17],
        "bottom": [1, 2, 5],
        "top": [4, 8, 15],
    }


def test_recomputed_stress_is_a_nonnegative_stress_on_the_whole_box() -> None:
    audit = local.stress_audit(_family(), local.DECLARED_BOX)
    assert audit["passed"]
    assert all(audit["checks"].values())
    assert audit["rows_reaching_zero"] == []
    assert audit["vertex_ranks_mod_p"] == [46] * 8
    assert audit["least_weight"]["row"] == "pair:11:12:1"
    assert audit["least_weight"]["vertex"] == ["0", "1/12", "-1/8"]
    assert Q(1, 250) < Q(audit["least_weight"]["value_decimal"]) < Q(1, 200)
    # Only the midpoint's two F2 columns (omega12, omega16) are off zero, as in H-258.
    assert set(audit["origin_residual_columns"]) == {
        str(local.column(12, "angle")),
        str(local.column(16, "angle")),
    }


def test_family_stress_needs_the_wall_rebalancing_when_square_5_slides() -> None:
    family = _family()
    origin = (Q(0), Q(0), Q(0))
    _, reference = local.family_stress(family, origin)
    corner = (Q(1, 4), Q(0), Q(0))
    _, unbalanced = local.family_stress(family, corner)
    moved = {c for c, (x, y) in enumerate(zip(unbalanced, reference, strict=True)) if x != y}
    assert moved == {local.column(5, "angle"), local.column(7, "angle")}
    stress, balanced = local.family_stress(family, corner, reference)
    assert balanced == reference
    assert all(stress[key] == 0 for key in local.ZERO_WEIGHT_KEYS)


def test_roster_is_bound_to_the_accepted_h257_inventory() -> None:
    audit = local.roster_binding_audit(_family())
    assert audit["passed"]
    assert (audit["retained_pairs"], audit["retained_walls"]) == (19, 13)
    assert audit["retained_identity_options"] == 27
    raw = local.FEATURE_CERTIFICATE.read_bytes()
    tampered = local.roster_binding_audit(
        _family(), raw.replace(b'"pairs": 21', b'"pairs": 22')
    )
    assert not tampered["checks"]["manifest_reproduces_counts"]
    assert not tampered["passed"]
    # Re-laying the certificate's bytes is not a change to it (OR-18): the blob moves,
    # is recorded, and nothing refuses it.
    relaid = json.dumps(json.loads(raw), indent=2, sort_keys=True).encode()
    moved = local.roster_binding_audit(_family(), relaid)
    assert moved["passed"]
    assert moved["certificate_blob"] != audit["certificate_blob"]


def test_restoring_the_non_tight_9_11_row_fails_slide_invariance() -> None:
    audit = local.slide_invariance_audit(_family(), restore=frozenset({(9, 11)}))
    assert not audit["passed"]
    assert audit["identity_options"] == 29
    assert audit["not_invariant"] == ["9/11:11:v:-1", "9/11:9:v:-1"]
