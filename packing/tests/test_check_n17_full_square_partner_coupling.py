"""Target-free full-square SAT signs, complete quantifiers and fresh custody."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest
from test_check_n17_partner_pose_coupling import synthetic_state, write_fixture

from devtools import check_n17_full_square_partner_coupling as tool

Q = tool.Q
ZERO, ONE = Q(0), Q(1)


def deadline() -> float:
    return time.monotonic() + 30


@pytest.mark.parametrize(
    ("polynomial", "expected"),
    [
        ((Q(2), Q(0), Q(0)), (Q(2), Q(0))),
        ((Q(2), Q(-1), Q(0)), (Q(1), Q(1))),
        ((Q(0), Q(1), Q(0)), (Q(0), Q(0))),
        ((Q(1, 4), Q(-1), Q(1)), (Q(0), Q(1, 2))),
        ((Q(0), Q(-1), Q(1)), (Q(-1, 4), Q(1, 2))),
        ((Q(0), Q(1), Q(-1)), (Q(0), Q(0))),
    ],
)
def test_exact_quadratic_minimum_least_tie_and_stationary(
    polynomial: tool.Polynomial, expected: tuple[Q, Q]
) -> None:
    assert tool.minimum(polynomial, Q(0), Q(1)) == expected


def test_stationary_violation_missed_by_endpoint_sampling() -> None:
    polynomial = (Q(1, 8), Q(-1), Q(1))
    assert tool.value_at(polynomial, Q(0)) > 0
    assert tool.value_at(polynomial, Q(1)) > 0
    assert tool.minimum(polynomial, Q(0), Q(1)) == (Q(-1, 8), Q(1, 2))


def test_closed_split_seams_both_formulas_agree() -> None:
    assert tool.split(Q(0), Q(1)) == [(Q(0), tool.TAU, -1), (tool.TAU, Q(1), 1)]
    assert tool.split(tool.TAU, tool.TAU) == [(tool.TAU, tool.TAU, -1)]
    for axis in tool.AXES:
        for eta in (-1, 1):
            below = tool.coefficients((Q(1, 3), Q(-2, 5)), -1, axis, eta)
            above = tool.coefficients((Q(1, 3), Q(-2, 5)), 1, axis, eta)
            assert tool.value_at(below, tool.TAU) == tool.value_at(above, tool.TAU)


@pytest.mark.parametrize("t", [Q(0), Q(1, 3), tool.TAU, Q(3, 4), Q(1)])
def test_all_signed_polynomials_equal_independent_square_support(t: Q) -> None:
    c, s = tool.finite.trig(t)
    own_u, own_v = (tool.C0, tool.S0), (-tool.S0, tool.C0)
    partner_u, partner_v = (c, s), (-s, c)
    displacement = (Q(7, 13), Q(-11, 17))
    sigma = -1 if t <= tool.TAU else 1
    for axis, normal in zip(tool.AXES, (own_u, own_v, partner_u, partner_v), strict=True):
        support = sum(
            abs(tool.finite.dot(normal, direction)) / 2
            for direction in (own_u, own_v, partner_u, partner_v)
        )
        for eta in (-1, 1):
            actual = tool.value_at(tool.coefficients(displacement, sigma, axis, eta), t)
            assert actual == 2 * (1 + t * t) * (
                support - eta * tool.finite.dot(normal, displacement)
            )


def record(domain: list[tool.Point], lo: Q = ZERO, hi: Q = ONE) -> dict[str, Any]:
    return {
        "domain": domain,
        "interval": [str(lo), str(hi)],
        "reference": {"kind": "wall_seed", "owner": 1, "row": 0},
    }


def test_zero_projection_margin_never_certifies_interior_touch() -> None:
    threshold = (1 + tool.C0 + tool.S0) / 2
    d = (threshold * tool.C0, threshold * tool.S0)
    polynomial = tool.coefficients(d, -1, "owner_u", 1)
    assert tool.minimum(polynomial, Q(0), Q(0))[0] == 0
    outcome = tool.partner_minimum([record([d], Q(0), Q(0))], (Q(0), Q(0)), [0], deadline())
    assert not outcome["strict_collision"]


@pytest.mark.parametrize("vertex", [["1", "1"], ["0", "0"]])
def test_negative_minimizer_exact_wall_secondary_only(vertex: list[str]) -> None:
    diagnostic = tool.exact_wall_at_minimizer({"minimizer": "0", "vertex": vertex})
    assert diagnostic["exact_numeric_wall_contained"] is (vertex[0] == "1")
    assert len(diagnostic["wall_margins"]) == 4
    assert diagnostic["secondary_only"]
    assert not diagnostic["seventeen_square_packing_proved"]


def test_each_partner_requires_all_rows_not_different_row_choices() -> None:
    first = record([(Q(1), Q(1))], Q(0), Q(1, 64))
    second = record([(Q(3), Q(3))], Q(1, 64), Q(1, 32))
    individual = tool.partner_minimum([first], (Q(1), Q(1)), [0], deadline())
    assert individual["strict_collision"]
    combined = tool.partner_minimum([first, second], (Q(1), Q(1)), [0], deadline())
    assert not combined["strict_collision"]
    assert combined["minimum_witness"]["row_index"] == 1


def test_disconnected_and_degenerate_centre_domains_affine_minimum() -> None:
    vertices = [(Q(1), Q(1)), (Q(3), Q(1))]
    outcome = tool.partner_minimum([record(vertices)], (Q(1), Q(1)), [0], deadline())
    assert not outcome["strict_collision"]
    assert outcome["minimum_witness"]["vertex"] == ["3", "1"]
    assert outcome["quadratic_minimizations"] == 32
    # Midpoint membership in a convex relaxation cannot remove its escape vertex.
    assert tool.partner_minimum([record([(Q(1), Q(1))])], (Q(1), Q(1)), [0], deadline())[
        "strict_collision"
    ]


def test_domains_clip_each_disjunct_without_unused_core(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("full-square method must not require a common core")

    monkeypatch.setattr(tool.parent, "core", forbidden)
    raw = {
        "interval": ["0", "1/64"],
        "reference": {},
        "residual_polygons": [[["0", "1"]], [["5", "1"]]],
    }
    outcome = tool.row_domain(raw, [0], deadline())
    assert outcome["domain"] == []
    assert len(outcome["pieces"]) == 2


@pytest.mark.parametrize("margin", [Q(1, 100000), Q(1), Q(100)])
def test_exact_positive_margin_lift_width_and_guard(margin: Q) -> None:
    outcome = tool.lift(margin, (Q(1), Q(1)))
    h = Q(outcome["half_width"])
    assert h == min(Q(1, 128), margin / (8 * tool.L))
    assert Q(outcome["gap_lower_bound"]) >= margin / 8 > 0
    assert Q(13, 32) <= tool.TAU - h < tool.TAU + h <= Q(27, 64)
    assert outcome["positive_coordinate_widths"]
    with pytest.raises(ValueError, match="positive"):
        tool.lift(Q(0), (Q(1), Q(1)))


@pytest.mark.parametrize("positive", [False, True])
def test_complete992_and1056_calibration_and_least_partner(positive: bool) -> None:  # noqa: FBT001
    cells, roles, roster, centre = synthetic_state(positive=positive)
    outcome = tool.construct(cells, roles, roster, centre, deadline=deadline())
    assert outcome["all_rows_checked"] == 1056
    assert outcome["foreign_rows_checked"] == 992
    assert len(outcome["partners"]) == 16
    assert outcome["endpoint_control"]["all17_retained"]
    assert outcome["criterion_met"] is positive
    if positive:
        assert outcome["selected_partner"] == min(map(int, outcome["partners"]))
        assert Q(outcome["region"]["half_width"]) > 0
    else:
        assert outcome["status"] == "criterion_missed"
        assert all(Q(p["minimum"]) <= 0 for p in outcome["partners"].values())


@pytest.mark.parametrize("mutation", ["missing_row", "seam", "typed_ref", "empty", "piece"])
def test_complete_domain_and_endpoint_controls_refuse(mutation: str) -> None:
    cells, roles, roster, centre = synthetic_state()
    if mutation == "missing_row":
        cells["1"].pop()
    elif mutation == "seam":
        cells["1"][1]["interval"][0] = "0"
    elif mutation == "typed_ref":
        cells["1"][0]["reference"]["owner"] = 2
    elif mutation == "empty":
        cells["1"][0]["residual_polygons"] = []
    else:
        cells["0"][26]["residual_polygons"] = []
    with pytest.raises(ValueError, match=r"roster|partition|reference|empty|witness"):
        tool.construct(cells, roles, roster, centre, deadline=deadline())


def test_quadratic_limit_and_deadline_preserve_incomplete(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tool, "QUADRATIC_LIMIT", 1)
    with pytest.raises(tool.IncompleteError, match="quadratic"):
        tool.partner_minimum([record([(Q(1), Q(1))])], (Q(1), Q(1)), [0], deadline())
    with pytest.raises(tool.IncompleteError, match="wall"):
        tool.partner_minimum([record([(Q(1), Q(1))])], (Q(1), Q(1)), [0], time.monotonic() - 1)


def adapted_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    return write_fixture(tmp_path, monkeypatch) | {"schema": tool.DESCRIPTOR_SCHEMA}


def test_fresh_complete_roundtrip_and_changed_margin_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = adapted_fixture(tmp_path, monkeypatch)
    certificate = tool.generate(document, deadline=deadline())
    decoded = tool.finite.decode(tool.retained_json.dumps(certificate).encode())
    assert tool.check(document, decoded, deadline=deadline())["verification_passed"]
    decoded["partners"]["1"]["minimum"] = "1"
    with pytest.raises(ValueError, match="reconstruction differs"):
        tool.check(document, decoded, deadline=deadline())


def test_context_byte_and_during_construction_custody(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = adapted_fixture(tmp_path, monkeypatch)
    wrong = copy.deepcopy(document) | {"centered_receipt_sha256": "f" * 64}
    with pytest.raises(ValueError, match="identity"):
        tool.generate(wrong, deadline=deadline())
    original = tool.construct

    def changed(*args: Any, **kwargs: Any) -> Any:
        result = original(*args, **kwargs)
        path = tmp_path / document["parent_descriptor"]
        path.write_bytes(path.read_bytes() + b" ")
        return result

    monkeypatch.setattr(tool, "construct", changed)
    with pytest.raises(ValueError, match="inputs changed"):
        tool.generate(document, deadline=deadline())


def test_two_fresh_clean_cli_complete_reconstruction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = adapted_fixture(tmp_path, monkeypatch)
    descriptor = tmp_path / "full-square.json"
    descriptor.write_text(json.dumps(document))
    outputs = [tmp_path / "generated.json", tmp_path / "checked.json"]
    code = (
        "from pathlib import Path; import sys; "
        "from devtools import check_n17_full_square_partner_coupling as t; "
        "t.finite.REPO=Path(sys.argv[1]); raise SystemExit(t.main(sys.argv[2:]))"
    )
    for index, output in enumerate(outputs):
        argv = [
            sys.executable,
            "-c",
            code,
            str(tmp_path),
            "--descriptor",
            str(descriptor),
            "--max-seconds",
            "30",
            "--output",
            str(output),
        ]
        if index:
            argv.extend(["--certificate", str(outputs[0])])
        process = subprocess.run(argv, capture_output=True, text=True, timeout=40, check=False)
        assert process.returncode == 0, process.stderr
    first, second = (json.loads(path.read_bytes()) for path in outputs)
    assert tool.parent.feasible.witness.payload(first) == tool.parent.feasible.witness.payload(
        second
    )
    assert second["verification_passed"]
    assert first["invocation"] != second["invocation"]
    assert all(first[k] is False for k in tool.parent.scope())


@pytest.mark.parametrize("kind", ["expired", "output_cap", "wrong_schema"])
def test_cli_scoped_incomplete_or_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, kind: str
) -> None:
    document = adapted_fixture(tmp_path, monkeypatch)
    if kind == "wrong_schema":
        document["schema"] = "wrong"
    if kind == "output_cap":
        monkeypatch.setattr(tool, "OUTPUT_LIMIT", 1)
    descriptor = tmp_path / "input.json"
    descriptor.write_text(json.dumps(document))
    output = tmp_path / "output.json"
    assert (
        tool.main(
            [
                "--descriptor",
                str(descriptor),
                "--max-seconds",
                "0.000001" if kind == "expired" else "30",
                "--output",
                str(output),
            ]
        )
        == 1
    )
    result = json.loads(output.read_bytes())
    assert result["status"] == ("refused" if kind == "wrong_schema" else "incomplete")
    assert not result["criterion_met"]
    assert all(result[k] is False for k in tool.parent.scope())
