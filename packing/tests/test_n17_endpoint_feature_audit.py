"""Independent, target-free controls for the H257 receipt auditor."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_n17_endpoint_features as audit
from devtools import audit_n17_endpoint_receipt as exact


def test_owner_roster_and_active_wall_corner_manifest() -> None:
    options = audit.expected_options()
    assert len(options) == 168
    zeros = [row for row in options if row["kind"] == "identity"]
    assert len(zeros) == 33
    assert len({(row["left"], row["right"], row["axis"], row["sign"]) for row in zeros}) == 22
    assert {
        (row["owner"], row["axis"], row["sign"])
        for row in zeros
        if (row["left"], row["right"]) == (2, 3)
    } == {(2, "ex", -1), (3, "ex", -1), (2, "ey", 1), (3, "ey", 1)}
    assert {
        (row["owner"], row["axis"], row["sign"])
        for row in zeros
        if (row["left"], row["right"]) == (8, 16)
    } == {(16, "q", -1)}
    corners = audit.expected_corners()
    assert len(corners) == 60
    assert sum(row["kind"] == "identity" for row in corners) == 29
    assert [(row["corner"], row["kind"]) for row in corners if row["label"] == 9] == [
        (0, "strict_positive"),
        (1, "strict_positive"),
        (2, "strict_positive"),
        (3, "identity"),
    ]
    assert (2, 3) not in audit.PARALLEL_PAIRS


def test_hand_computable_corner_and_tangent_arithmetic_outside_target_domain() -> None:
    layout = exact.reconstruct(exact.point(Fraction(1, 2)), exact.point(Fraction(1, 4)))
    assert [audit.corner_gap(layout, 1, "left", corner) for corner in range(4)] == [
        exact.point(0),
        exact.point(1),
        exact.point(1),
        exact.point(0),
    ]
    assert [audit.corner_gap(layout, 9, "left", corner) for corner in range(4)] == [
        exact.point(Fraction(4, 5)),
        exact.point(Fraction(7, 5)),
        exact.point(Fraction(3, 5)),
        exact.point(0),
    ]
    assert audit.tangent_offset(layout, 1, 2) == exact.point(0)
    assert audit.tangent_offset(layout, 2, 3) == exact.point(-1)
    assert audit.tangent_offset(layout, 9, 10) == exact.point(Fraction(-38, 175))
    assert audit.tangent_offset(layout, 9, 11) == exact.point(Fraction(3, 25))
    assert audit.tangent_offset(layout, 12, 14) == exact.point(Fraction(-1, 5))
    assert audit.tangent_offset(layout, 13, 14) == exact.point(Fraction(-37, 175))


class SyntheticLayout(exact.Layout):
    """A sign-control oracle, with no root or physical-packing assertion."""

    def pair_gap(self, left: int, right: int, axis: str, direction: str) -> exact.Interval:
        assert 1 <= left < right <= 17
        assert axis in ("ex", "ey", "u", "v", "p", "q")
        assert direction in ("forward", "reverse")
        return exact.point(-1)


def synthetic_inventory() -> dict[str, Any]:
    pairs = []
    for expected in audit.expected_options():
        row = expected.copy()
        identity = row["kind"] == "identity"
        row.update(
            bound=["0", "0"] if identity else ["-1", "-1"],
            bound_scope="certified_root" if identity else "whole_box",
            passed=True,
        )
        pairs.append(row)
    corners = []
    for expected in audit.expected_corners():
        row = expected.copy()
        identity = row["kind"] == "identity"
        row.update(
            bound=["0", "0"] if identity else ["1", "1"],
            bound_scope="certified_root" if identity else "whole_box",
            passed=True,
        )
        corners.append(row)
    offsets = [
        {
            "left": left,
            "right": right,
            "tau": ["0", "0"],
            "bound_scope": "whole_box",
            "passed": True,
        }
        for left, right in sorted(audit.PARALLEL_PAIRS)
    ]
    return {
        "schema": "n17-endpoint-features/v1",
        "feature_passed": True,
        "failures": [],
        "counts": dict(audit.COUNTS),
        "pair_options": pairs,
        "wall_corners": corners,
        "parallel_offsets": offsets,
    }


@pytest.fixture
def control(monkeypatch: pytest.MonkeyPatch) -> tuple[dict[str, Any], SyntheticLayout]:
    monkeypatch.setattr(audit, "corner_gap", lambda *_args: exact.point(1))
    monkeypatch.setattr(audit, "tangent_offset", lambda *_args: exact.point(0))
    return synthetic_inventory(), SyntheticLayout({}, {}, {}, {}, exact.point(1))


def test_full_synthetic_audit_and_coverage_mutations(
    control: tuple[dict[str, Any], SyntheticLayout],
) -> None:
    original, layout = control
    result = audit.audit_inventory(original, layout)
    assert result["strict_interval_comparisons"] == 175
    assert result["distinct_negative_intervals_computed"] == 106
    for mutation in (
        "missing_owner",
        "duplicate_owner",
        "bool_owner",
        "corner",
        "tau",
        "identity_reason",
        "scope",
        "negative_endpoint",
        "positive_endpoint",
    ):
        packet = copy.deepcopy(original)
        negative = next(
            row for row in packet["pair_options"] if row["kind"] == "strict_negative"
        )
        positive = next(
            row for row in packet["wall_corners"] if row["kind"] == "strict_positive"
        )
        if mutation == "missing_owner":
            packet["pair_options"].pop()
        elif mutation == "duplicate_owner":
            packet["pair_options"][-1] = packet["pair_options"][0]
        elif mutation == "bool_owner":
            packet["pair_options"][0]["owner"] = True
        elif mutation == "corner":
            packet["wall_corners"][-1] = packet["wall_corners"][0]
        elif mutation == "tau":
            packet["parallel_offsets"][-1] = packet["parallel_offsets"][0]
        elif mutation == "identity_reason":
            packet["pair_options"][0]["reason"] = "F3"
        elif mutation == "scope":
            negative["bound_scope"] = "certified_root"
        elif mutation == "negative_endpoint":
            negative["bound"] = ["-2", "-1"]
        else:
            positive["bound"] = ["1", "2"]
        with pytest.raises(exact.AuditError):
            audit.audit_inventory(packet, layout)


@pytest.mark.parametrize("upper", [0, 1])
def test_negative_alternative_requires_strict_upper(
    upper: int,
    control: tuple[dict[str, Any], SyntheticLayout],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet, layout = control
    monkeypatch.setattr(
        SyntheticLayout, "pair_gap", lambda *_args: (Fraction(-1), Fraction(upper))
    )
    for row in packet["pair_options"]:
        if row["kind"] == "strict_negative":
            row["bound"] = ["-1", str(upper)]
    with pytest.raises(exact.AuditError, match="strictly negative"):
        audit.audit_inventory(packet, layout)


def test_positive_corner_requires_strict_lower(
    control: tuple[dict[str, Any], SyntheticLayout],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet, layout = control
    monkeypatch.setattr(audit, "corner_gap", lambda *_args: (Fraction(0), Fraction(1)))
    for row in packet["wall_corners"]:
        if row["kind"] == "strict_positive":
            row["bound"] = ["0", "1"]
    with pytest.raises(exact.AuditError, match="nonpositive"):
        audit.audit_inventory(packet, layout)


@pytest.mark.parametrize("tau", [-1, 1])
def test_face_overlap_excludes_both_corner_limits(
    tau: int,
    control: tuple[dict[str, Any], SyntheticLayout],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet, layout = control
    monkeypatch.setattr(audit, "tangent_offset", lambda *_args: exact.point(tau))
    for row in packet["parallel_offsets"]:
        row["tau"] = [str(tau), str(tau)]
    with pytest.raises(exact.AuditError, match="overlap is not strict"):
        audit.audit_inventory(packet, layout)


def test_a_packet_naming_other_prerequisites_is_refused_without_target_reads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Prerequisites are named by revision and path; no bytes are compared with a blob."""
    packet = {
        "schema": "n17-endpoint-feature-certificate/v1",
        "criterion_passed": True,
        "root_git_ref": exact.ROOT_REF,
        "endpoint_git_ref": "elsewhere:certificate.json",
    }
    monkeypatch.setattr(exact, "read_bytes", lambda _path: json.dumps(packet).encode())
    with pytest.raises(exact.AuditError, match="wrong prerequisite references"):
        audit.audit(Path("synthetic-feature.json"), Path("synthetic-repository"))
