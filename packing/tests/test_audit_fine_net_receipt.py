"""Analytic oracles and refusal controls for the independent point-audit instrument."""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_fine_net_receipt as audit


def uniform_measure(density: Fraction, *, core: Fraction = Fraction(1)) -> audit.Measure:
    return audit.Measure(
        32,
        Fraction(4),
        core,
        Fraction(83, 40000),
        201,
        16 * density,
        1,
        {(Fraction(0), Fraction(4), Fraction(0), Fraction(4)): density},
    )


def candidate() -> dict[str, Any]:
    return {
        "n": 4,
        "L": "2",
        "B": "4/5",
        "proof_net": {"step": "21/100", "last": 2},
        "total_mass": "3",
        "points": [],
        "rectangles": [{"rectangle": ["0", "0", "2", "2"], "mass": "3"}],
    }


@pytest.mark.parametrize("index", [0, 1, 2, 157, 200])
def test_uniform_capture_is_density_times_core_area(index: int) -> None:
    measure = uniform_measure(Fraction(3, 2), core=Fraction(4, 5))
    assert audit.capture_at(measure, [2, 2], index) == Fraction(24, 25)


@pytest.mark.parametrize("index", [0, 157, 200])
def test_central_half_plane_has_half_the_rotated_core_area(index: int) -> None:
    measure = uniform_measure(Fraction(1))
    measure.rectangles.clear()
    measure.rectangles[(Fraction(0), Fraction(2), Fraction(0), Fraction(4))] = Fraction(1)
    assert audit.capture_at(measure, [2, 2], index) == Fraction(1, 2)


def test_triangle_clip_and_tangent_contact() -> None:
    unit = [
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(1)),
    ]
    assert audit.polygon_area(
        audit.clip_polygon(unit, Fraction(1), Fraction(1), Fraction(1))
    ) == Fraction(1, 2)
    assert (
        audit.polygon_area(audit.clip_polygon(unit, Fraction(-1), Fraction(0), Fraction(-1)))
        == 0
    )
    assert audit.clip_polygon(unit, Fraction(1), Fraction(0), Fraction(-1)) == []


def test_coincident_d4_images_add_density_and_preserve_mass() -> None:
    measure = audit.candidate_measure(candidate(), 4, Fraction(2))
    assert measure.rectangles == {
        (Fraction(0), Fraction(2), Fraction(0), Fraction(2)): Fraction(3, 4)
    }
    assert measure.mass == 3


def test_eight_distinct_d4_images() -> None:
    data = candidate()
    data["rectangles"][0]["rectangle"] = ["0", "0", "1/2", "1"]
    measure = audit.candidate_measure(data, 4, Fraction(2))
    assert len(measure.rectangles) == 8
    assert set(measure.rectangles.values()) == {Fraction(3, 4)}
    assert all((b - a) * (d - c) == Fraction(1, 2) for a, b, c, d in measure.rectangles)


@pytest.mark.parametrize(
    "defect", ["negative", "outside", "mass", "shrink", "endpoint", "points", "boolean_count"]
)
def test_candidate_rejects_broken_mathematical_premises(defect: str) -> None:
    data = candidate()
    if defect == "negative":
        data["rectangles"][0]["mass"] = "-3"
    elif defect == "outside":
        data["rectangles"][0]["rectangle"][0] = "-1"
    elif defect == "mass":
        data["total_mass"] = "2"
    elif defect == "shrink":
        data["B"] = "99/100"
    elif defect == "endpoint":
        data["proof_net"]["step"] = "1/10"
    elif defect == "points":
        data["points"] = [{}]
    else:
        data["n"] = True
    with pytest.raises(audit.AuditError):
        audit.candidate_measure(data, 4, Fraction(2))


def direction_log() -> list[dict[str, Any]]:
    return [
        *[
            {"r": index, "verdict": "verified", "threshold": 1, "min_certified_lower_bound": 1}
            for index in range(3)
        ],
        {
            "status": "VERIFIED",
            "directions": 3,
            "refused_directions": [],
            "fault_injected_at_box": None,
        },
    ]


def test_complete_receipt_is_accepted() -> None:
    assert audit.check_direction_log(direction_log(), 3)["status"] == "VERIFIED"


@pytest.mark.parametrize("indices", [[0, 1], [0, 1, 1], [0, 1, 3], [False, 1, 2], [0.0, 1, 2]])
def test_missing_duplicate_or_noninteger_directions_fail(indices: list[Any]) -> None:
    rows = direction_log()
    altered = [{**rows[0], "r": index} for index in indices] + [rows[-1]]
    with pytest.raises(audit.AuditError, match="direction"):
        audit.check_direction_log(altered, 3)


@pytest.mark.parametrize("defect", ["threshold", "bound", "fault"])
def test_verified_label_cannot_mask_invalid_receipt(defect: str) -> None:
    rows = direction_log()
    if defect == "threshold":
        rows[0]["threshold"] = "99/100"
    elif defect == "bound":
        rows[0]["min_certified_lower_bound"] = "99/100"
    else:
        rows[-1]["fault_injected_at_box"] = 1
    with pytest.raises(audit.AuditError):
        audit.check_direction_log(rows, 3)


def refusal() -> dict[str, Any]:
    return {
        "r": 0,
        "pose": [2, 2],
        "capture": "19899/20000",
        "verdict": "refused",
        "method": "axis-vertex-sweep",
        "crate_lower_bound": "19899/20000",
        "coverage_refusal": True,
        "in_domain": True,
        "capture_below_1": True,
        "captures_agree": True,
        "original_at_least_1": True,
    }


def test_control_capture_matches_an_analytic_integral() -> None:
    assert audit.check_refusal(
        uniform_measure(Fraction(201, 200)), refusal(), Fraction(99, 100), float("inf")
    ) == Fraction(201, 200)


@pytest.mark.parametrize("defect", ["capture", "domain", "flag"])
def test_refusal_flags_do_not_replace_mathematical_checks(defect: str) -> None:
    row = refusal()
    if defect == "capture":
        row["capture"] = "99/100"
    elif defect == "domain":
        row["pose"] = [0, 0]
    else:
        row["coverage_refusal"] = False
    with pytest.raises(audit.AuditError):
        audit.check_refusal(
            uniform_measure(Fraction(201, 200)), row, Fraction(99, 100), float("inf")
        )


def test_numeric_pose_preserves_binary64_not_decimal_semantics() -> None:
    data = audit.read_json('{"numeric":0.1,"rational":"0.1"}')
    assert audit.rational(data["numeric"]) == Fraction(3602879701896397, 36028797018963968)
    assert audit.rational(data["rational"]) == Fraction(1, 10)


@pytest.mark.parametrize("data", ['{"n":1,"n":2}', '{"n":NaN}', '{"n":Infinity}'])
def test_ambiguous_json_is_rejected(data: str) -> None:
    with pytest.raises(audit.AuditError):
        audit.read_json(data)


def test_expired_budget_refuses_work() -> None:
    with pytest.raises(audit.AuditError, match="time budget"):
        audit.capture_at(uniform_measure(Fraction(1)), [2, 2], 0, deadline=0)


def test_optimized_cli_still_rejects_invalid_case_name(tmp_path: Path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-O",
            str(Path(audit.__file__)),
            "--root",
            str(tmp_path),
            "--packet",
            "..",
            "--certificate",
            "case",
            "--n",
            "4",
            "--side",
            "2",
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    assert completed.returncode == 1
    assert json.loads(completed.stderr)["status"] == "FAIL"
    assert "single path components" in completed.stderr


def binding_receipts() -> tuple[audit.Measure, dict[str, Any], dict[str, Any], dict[str, Any]]:
    measure = audit.candidate_measure(candidate(), 4, Fraction(2))
    premises: dict[str, Any] = {
        "input_sha256": "candidate",
        "B": "4/5",
        "D": "21/100",
        "L": "2",
        "mass_exact": "3",
        "mass_below_n": "1",
        "net_last_tangent": "21/50",
        "shrink_bound": "121/125",
        "format": "M",
        "centre_domain": "per-bin",
        "net_origin": "proof_net",
        "expanded_points": 0,
        "expanded_segments": 0,
        "expanded_rectangles": 1,
        "n": 4,
        "angle_count": 3,
        "source_rectangles": 1,
    }
    build = {"source_sha256": "source", "profile": "release"}
    entry: dict[str, Any] = {
        "candidate_sha256": "candidate",
        "status": "VERIFIED",
        "returncode": 0,
        "directions_verified": 3,
        "refused_directions": [],
        "premises": premises,
        "build": build,
        "threshold": 1,
        "binary_sha256": "binary",
    }
    summary: dict[str, Any] = {"premises": premises, "build": build, "threshold": 1}
    control: dict[str, Any] = {
        "candidate_sha256": "candidate",
        "build": build,
        "n": 4,
        "L": "2",
        "binary_sha256": "binary",
    }
    return measure, summary, entry, control


@pytest.mark.parametrize("defect", ["candidate", "build", "binary", "threshold", "mass"])
def test_receipt_bindings_reject_forged_identity_or_premises(defect: str) -> None:
    measure, summary, entry, control = binding_receipts()
    audit.check_bindings(measure, summary, entry, control, candidate_sha="candidate")
    if defect == "candidate":
        control["candidate_sha256"] = "other"
    elif defect == "build":
        control["build"] = {**control["build"], "source_sha256": "other"}
    elif defect == "binary":
        control["binary_sha256"] = "other"
    elif defect == "threshold":
        summary["threshold"] = "99/100"
    else:
        summary["premises"]["mass_exact"] = "2"
    with pytest.raises(audit.AuditError):
        audit.check_bindings(measure, summary, entry, control, candidate_sha="candidate")


@pytest.mark.parametrize("crate_present", [False, True])
def test_point_audit_reads_historical_receipts_without_gating_current_crate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, crate_present: bool
) -> None:
    """Current source is neither needed nor admitted by the saved-point audit."""
    _, summary, entry, control = binding_receipts()
    packet, certificate = "packet", "certificate"
    raw = gzip.compress(json.dumps(candidate()).encode(), mtime=0)
    candidate_path = (
        tmp_path
        / "packing/resources/web"
        / packet
        / "release/certificates"
        / certificate
        / "candidate.json.gz"
    )
    candidate_path.parent.mkdir(parents=True)
    candidate_path.write_bytes(raw)
    candidate_identity = hashlib.sha256(raw).hexdigest()
    entry.update(packet=packet, certificate=certificate, candidate_sha256=candidate_identity)
    control.update(packet=packet, certificate=certificate, candidate_sha256=candidate_identity)
    summary["premises"]["input_sha256"] = candidate_identity
    base = tmp_path / "packing/benchmarks/measure-verifier/census-mixed"
    (base / packet).mkdir(parents=True)
    (base / "census.json").write_text(json.dumps({"cases": {certificate: entry}}))
    rows = direction_log()
    rows[-1].update(summary)
    (base / packet / f"{certificate}.jsonl.gz").write_bytes(
        gzip.compress(b"\n".join(json.dumps(row).encode() for row in rows), mtime=0)
    )
    (base / packet / f"{certificate}.control.json").write_text(json.dumps(control))
    if crate_present:
        current_source = tmp_path / "packing/sqverify_fast/src/certificate.rs"
        current_source.parent.mkdir(parents=True)
        current_source.write_text("current unreviewed checkout edits are not audit inputs")

    # Geometry and refusal arithmetic have analytic tests above; isolate source custody.
    def skip_point_evaluation(
        _measure: audit.Measure,
        _entry: dict[str, Any],
        _control: dict[str, Any],
        _deadline: float,
    ) -> dict[str, Any]:
        return {}

    monkeypatch.setattr(audit, "check_controls", skip_point_evaluation)
    result = audit.audit(tmp_path, packet, certificate, 4, Fraction(2), seconds=10)
    assert result["status"] == "PASS"
    assert result["recorded_native_source_sha256"] == "source"
    assert (
        result["source_identity_scope"]
        == "historical receipt metadata; current crate source not read"
    )


@pytest.mark.parametrize("index", [0, 157])
def test_exact_refusal_route_is_selected_by_evidence_not_direction(index: int) -> None:
    row = refusal()
    row.update(
        r=index,
        verdict="counterexample-candidate",
        method="interval-branch-and-bound",
        crate_exact_below_threshold=True,
    )
    assert audit.check_refusal(
        uniform_measure(Fraction(201, 200)), row, Fraction(99, 100), float("inf")
    ) == Fraction(201, 200)


@pytest.mark.parametrize(
    "defect", ["axis_index", "axis_bound", "exact_flag", "unknown_verdict"]
)
def test_refusal_route_requires_its_corresponding_evidence(defect: str) -> None:
    row = refusal()
    if defect == "axis_index":
        row["r"] = 157
    elif defect == "axis_bound":
        row["crate_lower_bound"] = "99/100"
    elif defect == "exact_flag":
        row.update(verdict="counterexample-candidate", crate_exact_below_threshold=False)
    else:
        row["verdict"] = "resource-exhausted"
    with pytest.raises(audit.AuditError):
        audit.check_refusal(
            uniform_measure(Fraction(201, 200)), row, Fraction(99, 100), float("inf")
        )
