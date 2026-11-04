"""Analytic oracles and refusal controls for the independent point-audit instrument."""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_fine_net_receipt as audit
from devtools import sqverify_fast_census as census
from devtools.check_sqverify_fast import COINCIDENT_AXIS
from devtools.sqverify_fast_axis import column_enclosure, images

#: The axis sweep's enclosure at (2, 2) of `uniform_measure(201/200)` scaled by 99/100,
#: by this instrument's walk and by the census's (`devtools.sqverify_fast_axis`) alike.
UNIFORM_AXIS = (0.994949999999997, 0.9949500000000029)


def uniform_measure(density: Fraction, *, core: Fraction = Fraction(1)) -> audit.Measure:
    whole = (Fraction(0), Fraction(4), Fraction(0), Fraction(4))
    return audit.Measure(
        32,
        Fraction(4),
        core,
        Fraction(83, 40000),
        201,
        16 * density,
        1,
        {whole: density},
        (whole,),
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


def test_a_provenance_note_is_admitted_and_not_read() -> None:
    """A regenerated certificate may say where it came from in `derived_from` (#890's
    dilation does), which the crate's admission ignores: the measure is the same with it
    or without it. Only a string is admitted, and no other extra field."""
    plain = audit.candidate_measure(candidate(), 4, Fraction(2))
    noted = {**candidate(), "derived_from": "published certificate at L=2 scaled by 1"}
    assert audit.candidate_measure(noted, 4, Fraction(2)) == plain
    for extra in ({"derived_from": 1}, {"derived_from": None}, {"scaling_factor": "1"}):
        with pytest.raises(audit.AuditError):
            audit.candidate_measure({**candidate(), **extra}, 4, Fraction(2))


@pytest.mark.parametrize("field", sorted(audit.CANDIDATE_FIELDS))
def test_a_candidate_missing_a_format_field_is_refused_on_admission(field: str) -> None:
    """Admission names the format's fields as a lower bound as well as an upper one, so a
    candidate without one is refused there with the format's reason, with or without a
    provenance note, and never reaches a later read of the missing key."""
    for base in (candidate(), {**candidate(), "derived_from": "a note"}):
        data = {key: value for key, value in base.items() if key != field}
        with pytest.raises(audit.AuditError, match="format-M audit fields"):
            audit.candidate_measure(data, 4, Fraction(2))


@pytest.mark.parametrize(
    ("flags", "expected"),
    [
        ([], None),
        (
            ["--candidate", "source/certificate/n94_L9965.json.gz"],
            "source/certificate/n94_L9965.json.gz",
        ),
    ],
)
def test_the_cli_hands_its_candidate_path_to_the_audit(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    flags: list[str],
    expected: str | None,
) -> None:
    """`--candidate` reaches `audit` as `candidate_path`, and without it the default
    release layout is asked for (None)."""
    seen: dict[str, Any] = {}

    def recorded(*args: Any, **kwargs: Any) -> dict[str, Any]:
        seen.update(args=args, **kwargs)
        return {"status": "PASS"}

    monkeypatch.setattr(audit, "audit", recorded)
    argv = ["--root", ".", "--packet", "p", "--certificate", "c", "--n", "94"]
    assert audit.main([*argv, "--side", "1993/200", *flags]) == 0
    assert seen["candidate_path"] == expected
    assert seen["args"][1:4] == ("p", "c", 94)
    assert json.loads(capsys.readouterr().out)["status"] == "PASS"


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
        "crate_lower_bound": UNIFORM_AXIS[0],
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


def test_an_axis_refusal_is_judged_by_the_sweeps_enclosure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """F-1 of the 14 October review, as the census control judges it since #892: the
    bound must be the lower end of the enclosure recomputed at the vertex, to the bit, and
    the exact capture must lie in it, with no constant allowance. A bound one ulp off, a
    capture outside an enclosure, a stored enclosure that differs, a vertex off the event
    grid, and a measure without the crate's order are refused."""
    measure, factor = uniform_measure(Fraction(201, 200)), Fraction(99, 100)
    assert audit.axis_enclosure(measure, factor, [2, 2]) == UNIFORM_AXIS
    row = refusal()
    assert audit.check_refusal(measure, row, factor, math.inf) == Fraction(201, 200)
    stored = {**row, "sweep_enclosure": list(UNIFORM_AXIS)}
    assert audit.check_refusal(measure, stored, factor, math.inf) == Fraction(201, 200)
    low = UNIFORM_AXIS[0]
    off_grid = "200000000000000000000000000001/100000000000000000000000000000"
    refused = [
        ({**row, "crate_lower_bound": math.nextafter(low, math.inf)}, "lower end"),
        ({**row, "crate_lower_bound": math.nextafter(low, -math.inf)}, "lower end"),
        (
            {**row, "sweep_enclosure": [low, math.nextafter(UNIFORM_AXIS[1], math.inf)]},
            "differs from the recomputed",
        ),
        ({**row, "pose": [2, off_grid]}, "no sweep enclosure"),
        ({**row, "pose": [off_grid, 2]}, "no sweep enclosure"),
    ]
    for defect, reason in refused:
        with pytest.raises(audit.AuditError, match=reason):
            audit.check_refusal(measure, defect, factor, math.inf)
    unordered = audit.Measure(
        *(getattr(measure, f) for f in audit.Measure.__dataclass_fields__ if f != "axis_order")
    )
    with pytest.raises(audit.AuditError, match="no sweep enclosure"):
        audit.check_refusal(unordered, row, factor, math.inf)
    monkeypatch.setattr(
        audit, "axis_enclosure", lambda *_: (low, math.nextafter(low, math.inf))
    )
    with pytest.raises(audit.AuditError, match="outside the sweep's enclosure"):
        audit.check_refusal(measure, row, factor, math.inf)


def crate_key(rectangle: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    """This instrument's `(x0, x1, y0, y1)` written as the crate's `(x1, y1, x2, y2)`."""
    x0, x1, y0, y1 = rectangle
    return x0, y0, x1, y1


def test_the_axis_walk_is_the_census_walk() -> None:
    """This instrument's walk, written apart from `devtools.sqverify_fast_axis` but from
    the same Rust, sums in the crate's order and gives the same enclosure, on a uniform
    measure, on `COINCIDENT_AXIS` (whose images coincide) and at the 99/100 mutant's axis
    refusal of mixed_n37_L64975, where the census's walk is the crate's to the bit."""
    uniform = {
        "L": "4",
        "B": "1",
        "rectangles": [{"rectangle": ["0", "0", "4", "4"], "mass": "402/25"}],
    }
    factor = Fraction(99, 100)
    assert column_enclosure(uniform, factor, Fraction(2), Fraction(2), Fraction(7, 2)) == (
        UNIFORM_AXIS
    )
    coincident = {**COINCIDENT_AXIS, "proof_net": {"step": "83/40000", "last": 200}}
    name = "mixed_n37_L64975"
    case = {c.certificate: c for c in census.mixed_cases()}[name]
    control = json.loads(
        (census.CENSUS_ROOT / "census-mixed" / case.packet / f"{name}.control.json").read_text(
            encoding="utf-8"
        )
    )
    sweep = next(run["sweep"] for run in control["runs"] if "sweep" in run)
    item = next(row for row in sweep["refused"] if row["r"] == 0)
    real = audit.read_json(gzip.decompress(case.candidate.read_bytes()))
    for raw, pose in ((coincident, ["27/20", "2"]), (real, item["pose"])):
        measure = audit.candidate_measure(raw, int(raw["n"]), Fraction(raw["L"]))
        order = [(crate_key(key), measure.rectangles[key]) for key in measure.axis_order]
        assert order == images(raw, Fraction(1))
        x, y = (Fraction(value) for value in pose)
        upper = Fraction(raw["L"]) - Fraction(1, 2)
        assert audit.axis_enclosure(measure, factor, pose) == column_enclosure(
            raw, factor, x, y, upper
        )
    measure = audit.candidate_measure(real, case.n, Fraction(case.side))
    assert audit.check_refusal(measure, item, factor, math.inf) >= 1


def test_the_kept_n94_axis_refusal_holds_under_the_enclosure_rule() -> None:
    """mixed_n94_L9965's control failed closed on the constant allowance alone (#890). Its
    axis refusal, with `captures_agree` as the enclosure rule judges it, passes here: the
    bound is the recomputed lower end, and the exact capture, 1.12e-9 above it, lies in
    the enclosure. Its candidate's `derived_from` note is admitted and not read."""
    name = "mixed_n94_L9965"
    case = {c.certificate: c for c in census.mixed_cases()}[name]
    folder = census.CENSUS_ROOT / "census-mixed" / case.packet
    control = json.loads((folder / f"{name}.control-failed-v2.json").read_text("utf-8"))
    sweep = next(run["sweep"] for run in control["runs"] if "sweep" in run)
    item = {**next(row for row in sweep["refused"] if row["r"] == 0), "captures_agree": True}
    raw = audit.read_json(gzip.decompress(case.candidate.read_bytes()))
    assert "derived_from" in raw
    measure = audit.candidate_measure(raw, case.n, Fraction(case.side))
    factor = Fraction(99, 100)
    assert factor * audit.check_refusal(measure, item, factor, math.inf) == Fraction(
        item["capture"]
    )
    low, high = audit.axis_enclosure(measure, factor, item["pose"]) or (0.0, 0.0)
    assert low == item["crate_lower_bound"]
    assert Fraction(item["capture"]) - Fraction(low) > Fraction(1, 10**9)
    assert (low, high) == (0.9930860126842824, 0.9930860149308234)


def test_the_whole_audit_reads_n94_from_its_source_packet(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The auditor reads mixed_n94_L9965 where #890's packet keeps it, as its source
    published it (`--candidate source/certificate/n94_L9965.json.gz`), with its
    `derived_from` note, and binds it to the census row, the 600-direction capture and the
    control receipt the enclosure rule passed. The axis refusal and the least-bound
    direction's are recomputed exactly here, with the selected centre and the
    near-threshold witness; the other 598 refusals take their receipt's captures, to keep
    the test fast. The full run, every refusal recomputed, passed on 4 November 2026 in
    37.5 s (`independent_refusal_points` 600)."""
    real = audit.check_refusal

    def sampled(
        measure: audit.Measure, row: dict[str, Any], factor: Fraction, deadline: float
    ) -> Fraction:
        if row["r"] in (0, 277):
            return real(measure, row, factor, deadline)
        return Fraction(row["capture"]) / factor

    monkeypatch.setattr(audit, "check_refusal", sampled)
    root = census.PROJECT.parent
    packet = "ozden-s94-lower-bound-2026-11-03"
    with pytest.raises(FileNotFoundError):
        audit.audit(root, packet, "mixed_n94_L9965", 94, Fraction(1993, 200), seconds=60)
    result = audit.audit(
        root,
        packet,
        "mixed_n94_L9965",
        94,
        Fraction(1993, 200),
        seconds=120,
        candidate_path="source/certificate/n94_L9965.json.gz",
    )
    assert result["status"] == "PASS"
    assert result["candidate_gzip_sha256"].startswith("116c8342")
    assert (result["rectangles"], result["expanded_rectangles"]) == (853, 6720)
    assert result["independent_refusal_points"] == 600
    assert result["least_leaf_index"] == 277
    for outside in ("../ozden-s94-lower-bound-2026-11-03/README.md", "/etc/hostname", "."):
        with pytest.raises(audit.AuditError, match="inside the packet"):
            audit.audit(
                root,
                packet,
                "mixed_n94_L9965",
                94,
                Fraction(1993, 200),
                seconds=10,
                candidate_path=outside,
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
