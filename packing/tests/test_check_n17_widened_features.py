"""Synthetic exact controls for conditional widened feature forcing; no target reads."""

from __future__ import annotations

import copy
import json
from fractions import Fraction as Q
from typing import Any

import pytest

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_widened_features as check


def synthetic_layout() -> exact.Layout:
    axes = {name: (exact.point(1), exact.point(0)) for name in ("ex", "u", "p")}
    axes.update({name: (exact.point(0), exact.point(1)) for name in ("ey", "v", "q")})
    return exact.Layout(
        {label: (exact.point(0), exact.point(0)) for label in range(1, 18)},
        axes,
        {},
        {},
        exact.point(5),
    )


@pytest.fixture
def packet(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    layout = synthetic_layout()
    monkeypatch.setattr(check, "load_root", lambda _path: ({"synthetic": True}, layout, layout))
    return check.generate()


def test_complete_synthetic_certificate_and_exact_margin(packet: dict[str, Any]) -> None:
    result = check.check(packet)
    assert result["verification_passed"]
    assert result["final_margin"] == "-71/21000"
    assert len(packet["distances"]) == 19
    assert len(packet["features"]) == 125
    assert all(len(row["vertices"]) == 8 for row in packet["features"])


@pytest.mark.parametrize(
    "mutation", ["feature", "vertex", "duplicate", "root", "domain", "bound", "corner"]
)
def test_missing_tampered_and_duplicate_evidence_refused(
    packet: dict[str, Any],
    mutation: str,
) -> None:
    damaged = copy.deepcopy(packet)
    if mutation == "feature":
        damaged["features"].pop()
    elif mutation == "vertex":
        damaged["features"][0]["vertices"].pop()
    elif mutation == "duplicate":
        damaged["features"][0] = damaged["features"][1]
    elif mutation == "root":
        damaged["inputs"] = {"synthetic": False}
    elif mutation == "domain":
        damaged["slider_box"][1][0] = "0"
    elif mutation == "bound":
        damaged["features"][0]["vertices"][0]["gap_interval"] = ["-2", "-2"]
    else:
        damaged["features"][0]["corner"] = [True, -1]
    with pytest.raises(exact.AuditError):
        check.check(damaged)


def test_owner_sign_convention_matches_ordered_pair_support_for_both_owners() -> None:
    layout = synthetic_layout()
    layout.centres[1] = (exact.point(Q(1, 5)), exact.point(Q(2, 5)))
    layout.centres[2] = (exact.point(Q(7, 5)), exact.point(Q(4, 5)))
    for owner in (1, 2):
        for sign in (-1, 1):
            option = {"left": 1, "right": 2, "owner": owner, "axis": "ex", "sign": sign}
            minimum = min(
                check.corner_gap(layout, layout.centres, option, corner)[1]
                for corner in check.CORNERS
            )
            full = layout.pair_gap(1, 2, "ex", "forward" if sign == 1 else "reverse")
            assert full[0] == full[1] == minimum


def test_invalid_sqrt_bound_and_wider_region_fail(packet: dict[str, Any]) -> None:
    damaged = copy.deepcopy(packet)
    damaged["constants"]["sqrt2_upper"] = "7/5"
    with pytest.raises(exact.AuditError, match="square-root"):
        check.check(damaged)
    damaged = copy.deepcopy(packet)
    damaged["constants"]["position_radius"] = "1/50"
    damaged["final_margin"] = str(check.analytic_margin(damaged["constants"]))
    with pytest.raises(exact.AuditError, match="forcing margin"):
        check.check(damaged)


@pytest.mark.parametrize(
    ("name", "value"), [("position_radius", "1/200"), ("half_angle_radius", "1/400")]
)
def test_smaller_region_cannot_pass_as_the_frozen_certificate(
    packet: dict[str, Any], name: str, value: str
) -> None:
    damaged = copy.deepcopy(packet)
    damaged["constants"][name] = value
    damaged["final_margin"] = str(check.analytic_margin(damaged["constants"]))
    with pytest.raises(exact.AuditError, match="frozen analytic region"):
        check.check(damaged)


def test_distance_control_exceeds_one_and_nominal_margin_control() -> None:
    layout = synthetic_layout()
    layout.centres[2] = (exact.point(Q(11, 10)), exact.point(0))
    assert check.distance_squared(layout.centres, (1, 2))[1] > 1
    option = {"left": 1, "right": 2, "owner": 1, "axis": "ex", "sign": 1}
    layout.centres[2] = (exact.point(Q(23, 25)), exact.point(0))
    gap = check.corner_gap(layout, layout.centres, option, (-1, 1))[1]
    assert Q(-1, 10) < gap <= Q(-11, 200)


def test_full_interval_not_just_parameter_corners() -> None:
    centres = synthetic_layout().centres
    centres[2] = ((Q(-2), Q(1)), exact.point(0))
    assert check.distance_squared(centres, (1, 2)) == (Q(0), Q(4))


def test_non_target_parameter_interval_rounds_outward_and_serializes() -> None:
    radius = Q(1, 2**256)
    layout = exact.reconstruct(
        (Q(1, 2) - radius, Q(1, 2) + radius),
        (Q(1, 4) - radius, Q(1, 4) + radius),
    )
    rounded = check.rounded_layout(layout)
    for label in layout.centres:
        for original, enclosed in zip(
            layout.centres[label], rounded.centres[label], strict=True
        ):
            assert enclosed[0] <= original[0] <= original[1] <= enclosed[1]
    encoded = check.encode(check.distance_squared(rounded.centres, (16, 17)))
    assert exact.read_interval(json.loads(json.dumps(encoded))) == check.distance_squared(
        rounded.centres, (16, 17)
    )
    assert max(len(value) for value in encoded) < 1000


def test_loader_uses_checked_inclusion_box_and_retains_search_box(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document = {
        "box": {"midpoint": ["1/2", "1/4"], "radius": "1/10"},
        "inclusion_bounds": ["1/3", "1/3"],
    }
    monkeypatch.setattr(exact, "read_bytes", lambda _path: b"synthetic")
    monkeypatch.setattr(exact, "decode", lambda _raw: document)
    monkeypatch.setattr(
        check.root,
        "check",
        lambda _document, _source: {
            "verification_passed": True,
            "inclusion_bounds": ["1/100", "1/200"],
        },
    )
    inputs, layout, _ = check.load_root()
    used = inputs["root_inclusion_box_used"]
    assert used == [
        check.encode((value.lo, value.hi))
        for value in (
            check.Dyadic.enclose(Q(49, 100), Q(51, 100)),
            check.Dyadic.enclose(Q(49, 200), Q(51, 200)),
        )
    ]
    assert inputs["root_search_box"] == document["box"]
    assert layout.centres


def test_loader_refuses_failed_root_before_geometry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(exact, "read_bytes", lambda _path: b"synthetic")
    monkeypatch.setattr(exact, "decode", lambda _raw: {})

    def rejected(_document: Any, _source: bytes) -> dict[str, Any]:
        raise check.root.CertificateError("synthetic root refusal")

    monkeypatch.setattr(check.root, "check", rejected)
    with pytest.raises(check.root.CertificateError, match="root refusal"):
        check.load_root()
