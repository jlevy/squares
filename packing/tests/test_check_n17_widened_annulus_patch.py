"""Target-free exact controls for the one-patch all-owner interval certificate."""

from __future__ import annotations

import copy
import itertools
from decimal import Decimal
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_widened_annulus_patch as patch


def layout() -> exact.Layout:
    axes = {name: (exact.point(1), exact.point(0)) for name in ("ex", "u", "p")}
    axes.update({name: (exact.point(0), exact.point(1)) for name in ("ey", "v", "q")})
    return exact.Layout(
        {label: (exact.point(0), exact.point(0)) for label in range(1, 18)},
        axes,
        {},
        {},
        exact.point(5),
    )


@pytest.mark.parametrize(
    ("bound", "expected"), [(Q(1), True), (Q(1, 100), False), (Q(0), False)]
)
def test_one_dimensional_contradictory_borderline_and_feasible_systems(
    bound: Q,
    expected: bool,  # noqa: FBT001
) -> None:
    rows = (patch.row("one-dimensional", {0: patch.point(1)}, patch.point(bound)),)
    result = patch.evaluate(rows, (Q(1),), layout())
    assert result["passed"] is expected
    assert Q(result["eta"]) <= bound - patch.RHO
    assert bound - patch.RHO - Q(result["eta"]) < Q(1, 2**250)


def test_negative_multiplier_refused_and_rounding_ties_upward() -> None:
    with pytest.raises(exact.AuditError, match="multipliers"):
        patch.evaluate((patch.row("x", {}, patch.point(1)),), (Q(-1),), layout())
    for value, expected in [
        (Q(1, 2**45), Q(1, 2**44)),
        (Q(3, 2**45), Q(2, 2**44)),
        (Q(1, 2**46), Q(0)),
    ]:
        assert patch.round_weight(value) == expected
    with pytest.raises(exact.AuditError):
        patch.round_weight(Q(-1, 10))


def test_crossing_zero_square_absolute_and_owner_hull() -> None:
    value = patch.Dyadic.enclose(Q(-2), Q(1))
    assert patch.square(value) == patch.Dyadic.enclose(Q(0), Q(4))
    assert value.absolute() == patch.Dyadic.enclose(Q(0), Q(2))
    first = patch.row("owner1", {0: patch.point(1)}, patch.point(2))
    second = patch.row("owner2", {0: patch.point(-1)}, patch.point(3))
    merged = patch.hull_rows([first, second], "pair")
    assert merged.coefficients[0] == patch.Dyadic.enclose(Q(-1), Q(1))
    assert merged.rhs == patch.Dyadic.enclose(Q(2), Q(3))
    assert merged.options == ("owner1", "owner2")


def test_pair_reversal_and_zero_turn_owner_coincidence() -> None:
    basis = ((patch.point(1), patch.point(0)), (patch.point(0), patch.point(1)))
    bases = {1: basis, 2: basis}
    first = patch.pair_row(patch.probe.Feature(1, 2, 1, 0, 1), bases)
    reverse = patch.pair_row(patch.probe.Feature(2, 1, 1, 0, -1), bases)
    other_owner = patch.pair_row(patch.probe.Feature(1, 2, 2, 0, 1), bases)
    assert first.coefficients == reverse.coefficients == other_owner.coefficients
    assert first.rhs == reverse.rhs == other_owner.rhs
    assert patch.rotate(basis, patch.point(0)) == basis


def test_complete_row_option_roster_and_exact_clipped_boxes() -> None:
    rows = patch.build_rows(layout(), tuple(exact.point(0) for _ in patch.LABELS))
    assert len(rows) == 147
    assert [len(row.options) for row in rows[-19:]].count(2) == 8
    assert sum(len(row.options) for row in rows[-19:]) == 27
    seed = [Q(-patch.OUTER) if label == 16 else Q(0) for label in patch.LABELS]
    for bits in patch.LADDER:
        box = patch.patch_box(seed, bits)
        assert len(box) == 16
        assert all(-patch.OUTER <= lo < hi <= patch.OUTER for lo, hi in box)
        assert box[patch.LABELS.index(16)][0] == -patch.OUTER
    with pytest.raises(exact.AuditError):
        patch.patch_box(seed, 30)
    with pytest.raises(exact.AuditError):
        patch.build_rows(layout(), (exact.point(0),))


def test_oblique_position_lift_and_slider_family_recovery() -> None:
    scene = layout()
    scene.axes["u"] = exact.point(Q(3, 5)), exact.point(Q(4, 5))
    scene.axes["v"] = exact.point(Q(-4, 5)), exact.point(Q(3, 5))
    vertex = Q(1, 4), Q(1, 12), Q(1, 16)
    moved = patch.forcing.shifted(scene, vertex)
    u, v = scene.axes["u"], scene.axes["v"]
    assert exact.dot(u, moved[11]) == exact.point(0)
    assert exact.dot(v, moved[11]) == exact.point(-vertex[1])
    assert exact.dot(v, moved[13]) == exact.point(vertex[2])
    assert moved[5][0] == exact.point(-vertex[0])
    indices = patch.column(11, 0), patch.column(11, 1)
    item = patch.row(
        "u11",
        {indices[0]: patch.point(Q(3, 5)), indices[1]: patch.point(Q(4, 5))},
        patch.point(1),
    )
    result = patch.evaluate((item,), (Q(1),), scene)
    lo, hi = (
        Q(value)
        for value in result["position_residual_intervals"][
            patch.apex.position_names().index("u11")
        ]
    )
    assert lo <= 1 <= hi
    assert hi - lo < Q(1, 2**240)


def test_nonpositive_patch_attempts_keep_only_frozen_five_levels(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seed = {
        "half_angle_turns": [
            str(-patch.OUTER) if label == 16 else "0" for label in patch.LABELS
        ],
        "weights": ["0"] * 147,
    }
    monkeypatch.setattr(
        patch,
        "load_inputs",
        lambda _feature, _apex: ({"synthetic": True}, layout(), seed, Q(1, 10000)),
    )
    packet = patch.generate(Path("features"), Path("apex"))
    assert packet["status"] == "inconclusive"
    assert [attempt["h_bits"] for attempt in packet["attempts"]] == list(patch.LADDER)
    assert all(attempt["passed"] is False for attempt in packet["attempts"])


@pytest.fixture
def packet(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    seed = {
        "half_angle_turns": [
            str(-patch.OUTER) if label == 16 else "0" for label in patch.LABELS
        ],
        "weights": ["1"] + ["0"] * 146,
    }
    monkeypatch.setattr(
        patch,
        "load_inputs",
        lambda _feature, _apex: ({"synthetic": True}, layout(), seed, Q(1, 10000)),
    )
    return patch.generate(Path("features"), Path("apex"))


def test_synthetic_patch_and_fresh_replay(packet: dict[str, Any]) -> None:
    result = patch.check(packet, Path("features"), Path("apex"))
    assert result["verification_passed"]
    assert result["positive_patch_certified"]
    assert len(packet["attempts"]) == 1
    assert packet["attempts"][0]["h_bits"] == 20


@pytest.mark.parametrize(
    "mutation", ["row", "option", "label", "root", "domain", "box", "margin"]
)
def test_tampered_patch_refused(packet: dict[str, Any], mutation: str) -> None:
    damaged = copy.deepcopy(packet)
    if mutation == "row":
        damaged["attempts"][0]["row_ids"].pop()
    elif mutation == "option":
        damaged["attempts"][0]["pair_options"][0].pop()
    elif mutation == "label":
        damaged["seed"]["half_angle_turns"].pop()
    elif mutation == "root":
        damaged["inputs"]["synthetic"] = False
    elif mutation == "domain":
        damaged["apex_q0"] = "1/200"
    elif mutation == "box":
        damaged["attempts"][0]["angle_box"][0] = ["-1", "1"]
    else:
        damaged["attempts"][0]["eta"] = "999"
    with pytest.raises(exact.AuditError):
        patch.check(damaged, Path("features"), Path("apex"))


def seed_receipt() -> dict[str, Any]:
    rows = patch.build_rows(layout(), tuple(exact.point(0) for _ in patch.LABELS))
    choices = next(itertools.product(*patch.probe.feature_groups()))
    ids = [item.name for item in rows[:128]] + [feature.name for feature in choices]
    outcome = {
        "status": "numerically_optimal",
        "representative_branch": 0,
        "diagnostics": {"primal_value": Decimal("4.5")},
        "row_ids": ids,
        "multipliers": [Decimal(0)] * 147,
    }
    outcome["multipliers"][0] = Decimal(1) / Decimal(2**45)
    return {
        "point_aliases": [{"id": patch.SEED_ID, "outcome_index": 0}],
        "points": [
            {
                "profile": "bounded_tube",
                "execution_complete": True,
                "status": "complete_numerical",
                "half_angle_turns": [
                    str(-patch.OUTER) if label == 16 else "0" for label in patch.LABELS
                ],
                "branches": [
                    {"branch_id": i, "outcome_index": 0, "status": "numerically_optimal"}
                    for i in range(256)
                ],
                "outcomes": [outcome],
            }
        ],
    }


def test_decimal_seed_tie_selects_lowest_raw_branch_and_rounds_exactly() -> None:
    receipt = seed_receipt()
    result = patch.seed_from_receipt(receipt)
    assert result["selected_raw_branch"] == 0
    assert result["representative_branch"] == 0
    assert Q(result["weights"][0]) == patch.round_weight(
        Q(receipt["points"][0]["outcomes"][0]["multipliers"][0])
    )


def test_seed_objective_order_retains_below_float_precision_difference() -> None:
    receipt = seed_receipt()
    result = receipt["points"][0]
    first = result["outcomes"][0]
    first["diagnostics"]["primal_value"] = Decimal("4.50000000000000000000000001")
    second = copy.deepcopy(first)
    second["diagnostics"]["primal_value"] = Decimal("4.5")
    second["representative_branch"] = 1
    choices = tuple(itertools.product(*patch.probe.feature_groups()))[1]
    second["row_ids"] = first["row_ids"][:128] + [feature.name for feature in choices]
    result["outcomes"].append(second)
    result["branches"][1]["outcome_index"] = 1
    assert float(first["diagnostics"]["primal_value"]) == float(
        second["diagnostics"]["primal_value"]
    )
    assert patch.seed_from_receipt(receipt)["selected_raw_branch"] == 1


@pytest.mark.parametrize(
    "value",
    [Decimal("1e999999999"), Decimal("1e-999999999"), Decimal("NaN"), Decimal("Infinity")],
)
def test_oversized_or_nonfinite_decimal_refused_before_fraction_expansion(
    value: Decimal,
) -> None:
    with pytest.raises(exact.AuditError):
        patch.decimal_rational(value)


def test_cli_generation_and_independent_json_replay(
    packet: dict[str, Any], tmp_path: Path
) -> None:
    original, replay = tmp_path / "original.json", tmp_path / "replay.json"
    arguments = ["--features", "features", "--apex", "apex"]
    assert patch.main([*arguments, "--output", str(original)]) == 0
    decoded = exact.decode(original.read_bytes())
    assert decoded["attempts"] == packet["attempts"]
    assert decoded["checker"]["positive_patch_certified"] is True
    assert (
        patch.main([*arguments, "--certificate", str(original), "--output", str(replay)]) == 0
    )
    assert exact.decode(replay.read_bytes())["checker"]["positive_patch_certified"] is True


@pytest.mark.parametrize("bad_input", ["oversized", "nonfinite"])
def test_seed_loader_refuses_size_and_nonfinite_json_before_seed_evaluation(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, bad_input: str
) -> None:
    source = tmp_path / "seed.json"
    source.write_bytes(b"x" * 65 if bad_input == "oversized" else b'{"x":NaN}')
    monkeypatch.setattr(patch, "SEED_RUN", source)
    monkeypatch.setattr(patch, "MAX_SEED_BYTES", 64)
    monkeypatch.setattr(patch.exact, "read_bytes", lambda _path: b"{}")
    monkeypatch.setattr(patch.forcing, "check", lambda _packet: {})
    monkeypatch.setattr(patch.apex, "check", lambda _packet, _path: {})
    monkeypatch.setattr(patch.forcing, "load_root", lambda: ({}, layout(), {}))
    with pytest.raises(exact.AuditError, match=r"32 MiB|nonfinite"):
        patch.load_inputs(Path("features"), Path("apex"))


@pytest.mark.parametrize("refused", ["features", "apex"])
def test_prerequisite_refusal_precedes_root_or_seed_evaluation(
    monkeypatch: pytest.MonkeyPatch, refused: str
) -> None:
    calls: list[str] = []
    monkeypatch.setattr(patch.exact, "read_bytes", lambda _path: b"{}")

    def feature_check(_packet: dict[str, Any]) -> dict[str, Any]:
        calls.append("features")
        if refused == "features":
            raise exact.AuditError("synthetic prerequisite refused")
        return {}

    def apex_check(_packet: dict[str, Any], _path: Path) -> dict[str, Any]:
        calls.append("apex")
        raise exact.AuditError("synthetic prerequisite refused")

    def forbidden() -> Any:
        pytest.fail("root or seed evaluation preceded accepted prerequisites")

    monkeypatch.setattr(patch.forcing, "check", feature_check)
    monkeypatch.setattr(patch.apex, "check", apex_check)
    monkeypatch.setattr(patch.forcing, "load_root", forbidden)
    with pytest.raises(exact.AuditError, match="prerequisite refused"):
        patch.load_inputs(Path("features"), Path("apex"))
    assert calls == (["features"] if refused == "features" else ["features", "apex"])


@pytest.mark.parametrize("mutation", ["negative", "rows", "branch", "alias", "profile"])
def test_invalid_seed_witness_refused(mutation: str) -> None:
    receipt = seed_receipt()
    result = receipt["points"][0]
    if mutation == "negative":
        result["outcomes"][0]["multipliers"][0] = Decimal("-0.00001")
    elif mutation == "rows":
        result["outcomes"][0]["row_ids"].reverse()
    elif mutation == "branch":
        result["branches"].pop()
    elif mutation == "alias":
        receipt["point_aliases"].append(receipt["point_aliases"][0])
    else:
        result["profile"] = "drop_sliders"
    with pytest.raises(exact.AuditError):
        patch.seed_from_receipt(receipt)
