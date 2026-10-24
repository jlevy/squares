"""Evidence prose uses retained platform, timing and producer relationships."""

from __future__ import annotations

import gzip
import json
from pathlib import Path
from typing import Any

import pytest

from devtools import sqverify_fast_census as census
from sqpack.yamlio import safe_load

FINE_NET = "wand125-fine-net-lower-bounds-2026-10-16"
SOURCE = "d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88"


def retained_case(
    root: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    rectangle: bool = False,
    packet: str = FINE_NET,
) -> tuple[census.Case, dict[str, Any], Path]:
    """Small stand-ins for reporting only; no native coverage decision is run."""
    project = root / "packing"
    name = "rect_n68_L853" if rectangle else "mixed_n68_L853"
    candidate = (
        project
        / "resources/web"
        / packet
        / "certificates"
        / name
        / ("certified_candidate.json.gz" if rectangle else "candidate.json.gz")
    )
    candidate.parent.mkdir(parents=True)
    candidate.write_bytes(gzip.compress(b"{}"))
    monkeypatch.setattr(census, "PROJECT", project)
    monkeypatch.setattr(census, "EVIDENCE", project / "evidence.yaml")
    case = census.Case(packet, name, 68, "853/100", candidate, "1")
    census.EVIDENCE.write_text(
        json.dumps(
            {
                "evidence": [
                    {
                        "id": "E-example-report",
                        "assurance": "reported",
                        "source_key": "[example]",
                        "scope": {"n_values": [68]},
                        "certificate": str(
                            (candidate.parent.parent if rectangle else candidate).relative_to(
                                project
                            )
                        ),
                    }
                ]
            }
        )
    )
    build = {
        "source_sha256": SOURCE,
        "target": "aarch64-apple-darwin",
        "rustc": "rustc 1.98.0 (88d9e12ae 2026-08-18)",
        "profile": "release",
    }
    entry = {
        "status": "VERIFIED",
        "returncode": 0,
        "n": 68,
        "L": "853/100",
        "packet": packet,
        "build": build,
        "threshold": "1",
        "threads": 2,
        "candidate_sha256": "candidate",
        "binary_sha256": "binary",
        "nodes": 104,
        "directions_verified": 201,
        "cpu_seconds": 855.891151,
        "wall_seconds": 437.339,
        "direction_cpu_seconds": {},
        "least_certified_bound": 1.00001,
        "least_bound_leaf_exact": {"r": 1, "exact_coverage": "11/10", "clears_threshold": True},
        "premises": {
            "format": "T" if rectangle else "M",
            "angle_count": 201,
            "net_origin": "standard" if rectangle else "proof_net",
            "D": "83/40000",
            "B": "9977/10000",
            "mass_exact": "6799999/100000",
            "source_rectangles": 726,
            "expanded_rectangles": 5796,
            "shrink_bound": "399908091/400000000",
            "net_last_tangent": "83/200",
        },
    }
    out = root / "receipts"
    folder = out / packet
    folder.mkdir(parents=True)
    rows = [
        {"r": 0, "vertices": 10, "min_certified_lower_bound": 1.1},
        {"r": 1, "min_certified_lower_bound": 1.00001},
        {"kind": "sqverify-fast-summary/v1", "direction_cpu_seconds": -0.0},
    ]
    (folder / f"{name}.jsonl.gz").write_bytes(
        gzip.compress("\n".join(map(json.dumps, rows)).encode())
    )
    refused = {
        "verdict": "counterexample-candidate",
        "mutation": {"capture_at_centre": "99/100", "factor": "999/1000"},
    }
    control = {
        "status": "CONTROLS_REFUSED",
        "build": build,
        "index": 1,
        "centres_weighed": 200,
        "exact_capture_independent": "11/10",
        "runs": [
            {"name": "original", "verdict": "verified"},
            {
                "name": "scaled-99-100",
                **refused,
                **(
                    {}
                    if rectangle
                    else {
                        "sweep": {
                            "directions": 201,
                            "refused": [r for r in range(201) if r not in {46, 47, 48, 49}],
                            "verified_directions": [46, 47, 48, 49],
                        }
                    }
                ),
            },
            {"name": "near-threshold", **refused},
        ],
    }
    (folder / f"{name}.control.json").write_text(json.dumps(control))
    monkeypatch.setattr(census, "source_replayed", lambda _: False)
    return case, entry, out


def evidence(case: census.Case, entry: dict[str, Any], out: Path) -> dict[str, Any]:
    return safe_load(
        census.evidence_entry(case, out, entry, audit_record="review", date="2026-10-19")
    )[0]


@pytest.mark.parametrize("rectangle", [False, True])
def test_mac_evidence_uses_retained_build_and_distinguishes_cpu_sources(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    rectangle: bool,
) -> None:
    case, entry, out = retained_case(tmp_path, monkeypatch, rectangle=rectangle)
    record = evidence(case, entry, out)
    text = " ".join(record["limitations"].split())
    assert entry["build"]["rustc"] in text
    assert "release, aarch64-apple-darwin" in text
    assert "856 aggregate process CPU seconds (wait4)" in text
    assert "Per-direction CPU is unavailable" in text
    assert "Linux" not in text
    assert "4-core" not in text
    assert "container" not in text
    assert "load average" not in text
    assert "native exit 0" in text
    if not rectangle:
        assert "refused at 197 of the 201 net directions" in text
        assert "the mutant verified at the other 4" in text


def test_current_packet_keeps_shared_crate_provenance_and_unknown_packets_make_no_claim(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for packet, relation in [
        (FINE_NET, "shared-components"),
        ("wand125-mixed-bounds-check2-2026-10-06", "shared-components"),
        ("wand125-point-and-mixed-2026-10-01", "independent-implementation"),
        ("unreviewed-new-packet", "unknown-historical"),
    ]:
        case, entry, out = retained_case(tmp_path / packet, monkeypatch, packet=packet)
        record = evidence(case, entry, out)
        assert record["relationship_to_generator"] == relation
        text = " ".join(record["limitations"].split())
        if relation == "shared-components":
            assert "declared-net reader" in " ".join(record["shared_components"])
            assert "producer adapted this repository's crate" in text
            assert "not an independent full implementation or a second method" in text
            assert "shares no code with it" not in text
        elif relation == "independent-implementation":
            assert "shares no code with it" in text
            assert "shared_components" not in record
        else:
            assert "relationship to the producer's checker is not recorded" in text
            assert "shares no code" not in text
            assert "second implementation" not in text


def test_missing_build_facts_are_not_invented_and_linux_timings_remain_available(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case, entry, out = retained_case(tmp_path, monkeypatch)
    entry["build"] = {"source_sha256": SOURCE}
    text = " ".join(evidence(case, entry, out)["limitations"].split())
    assert "compiler, profile and target not recorded" in text
    assert "rustc 1.98.0" not in text
    assert "Linux" not in text
    entry["build"].update(
        target="x86_64-unknown-linux-gnu", profile="release", rustc="rustc 1.98.0"
    )
    entry["direction_cpu_seconds"] = {str(r): 1.25 for r in range(201)}
    entry["load_before"] = 3.5
    text = " ".join(evidence(case, entry, out)["limitations"].split())
    assert "rustc 1.98.0, release, x86_64-unknown-linux-gnu" in text
    assert "251.2 summed per-direction CPU seconds" in text
    assert "load average 3.5" in text
    assert "4-core" not in text
    assert "container" not in text


def test_check2_n29_relationship_follows_its_published_cpp_records_only() -> None:
    check2 = "wand125-mixed-bounds-check2-2026-10-06"
    cases = [
        (census.Case(check2, "mixed_n29_L581", 29, "581/100"), "independent-implementation"),
        (census.Case(check2, "mixed_n28_L5735", 28, "1147/200"), "shared-components"),
        (census.Case(FINE_NET, "mixed_n68_L853", 68, "853/100"), "shared-components"),
        (census.Case(check2, "mixed_n29_L582", 29, "291/50"), "shared-components"),
        (
            census.Case("unreviewed-new-packet", "mixed_n29_L581", 29, "581/100"),
            "unknown-historical",
        ),
    ]
    for case, expected in cases:
        fields, text = census.mixed_relationship(case)
        record = safe_load("\n".join(fields))
        assert record["relationship_to_generator"] == expected
        if expected == "independent-implementation":
            assert "mixed_rotated_verify.cpp" in text
            assert "published claim rests on the shipped C++ records" in text
            assert "pre-publication run" in text
            assert "no retained receipt" in text
            assert "shared_components" not in record
        elif expected == "shared-components":
            assert "declared-net reader" in " ".join(record["shared_components"])
            assert "not an independent full implementation or a second method" in text
        else:
            assert "relationship to the producer's checker is not recorded" in text


def test_companion_preserves_recovery_and_control_aggregate_timing_only_when_bound(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case, entry, out = retained_case(tmp_path, monkeypatch)
    companion = out / case.packet / f"{case.certificate}.execution.json"
    execution = {
        "aggregate_timing": "/usr/bin/time -lp includes complete driver and children",
        "certificate": case.certificate,
        "candidate_sha256": entry["candidate_sha256"],
        "binary_sha256": entry["binary_sha256"],
        "build": entry["build"],
        "commands": [
            {
                "mode": "capture",
                "returncode": None,
                "native_returncode": 0,
                "recovered_complete_capture": True,
                "timing": {"cpu_seconds": 856.53, "real": 438.0},
            },
            {
                "mode": "control",
                "returncode": 0,
                "timing": {"cpu_seconds": 346.81, "real": 186.31},
            },
        ],
    }
    companion.write_text(json.dumps(execution))
    text = " ".join(evidence(case, entry, out)["limitations"].split())
    assert "outer capture exit was unobserved" in text
    assert "recovered complete native capture" in text
    assert "346.81 aggregate control CPU seconds" in text
    assert "186.31 seconds of wall time" in text
    assert "/usr/bin/time" in text
    assert f"{case.certificate}.execution.json" in text
    for invalid_cpu in (None, True, -1, float("nan"), float("inf"), "346.81", 10**400):
        execution["commands"][1]["timing"]["cpu_seconds"] = invalid_cpu
        companion.write_text(json.dumps(execution))
        text = " ".join(evidence(case, entry, out)["limitations"].split())
        assert "aggregate control CPU seconds" not in text
    execution["commands"][1]["timing"]["cpu_seconds"] = 346.81
    execution["candidate_sha256"] = "different"
    companion.write_text(json.dumps(execution))
    text = " ".join(evidence(case, entry, out)["limitations"].split())
    assert "outer capture exit" not in text


def test_reports_and_summary_do_not_convert_missing_direction_cpu_to_zero(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case, entry, out = retained_case(tmp_path, monkeypatch)
    monkeypatch.setattr(census, "mixed_cases", lambda: [case])
    monkeypatch.setattr(census, "rectangle_cases", list)
    monkeypatch.setattr(census, "replay_reference", dict)
    monkeypatch.setattr(
        census,
        "mixed_reference",
        lambda _: {
            "directions": [1, 2],
            "cpu_seconds": 100,
            "per_direction_cpu": True,
        },
    )
    mixed = {"cases": {case.certificate: entry}}
    text = census.render_mixed_report(mixed, out)
    assert "| 855.9 |" in text
    assert "| unavailable | - |" in text
    assert "wait4" in text
    assert "Per-direction CPU" in text
    monkeypatch.setattr(census, "CENSUS_ROOT", tmp_path / "summary")
    for family, data in [("census", {"cases": {}}), ("census-mixed", mixed)]:
        folder = census.CENSUS_ROOT / family
        folder.mkdir(parents=True)
        (folder / "census.json").write_text(json.dumps(data))
    (row,) = census.summary_rows()
    assert row["cpu_seconds"] == 855.9
    assert row["direction_cpu_seconds"] is None
    assert "unavailable" in census.render_summary([row])
    entry["direction_cpu_seconds"] = {str(r): 1.25 for r in range(201)}
    text = census.render_mixed_report(mixed, out)
    assert "| 100 | 2.5 | 40x |" in text
    entry["direction_cpu_seconds"].pop("2")
    assert "| unavailable | - |" in census.render_mixed_report(mixed, out)


@pytest.mark.parametrize(
    "reference",
    [
        {"directions": [], "cpu_seconds": 0, "per_direction_cpu": True},
        {"directions": [1, 2], "cpu_seconds": 0, "per_direction_cpu": False},
    ],
    ids=["none-replayed", "no-author-direction-cpu"],
)
def test_the_mixed_report_marks_an_uncompared_cell_not_applicable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    reference: dict[str, Any],
) -> None:
    """Where no direction was compared there is nothing unavailable: the cell is "-"."""
    case, entry, out = retained_case(tmp_path, monkeypatch)
    monkeypatch.setattr(census, "mixed_cases", lambda: [case])
    monkeypatch.setattr(census, "mixed_reference", lambda _: reference)
    entry["direction_cpu_seconds"] = {str(r): 1.25 for r in range(201)}
    text = census.render_mixed_report({"cases": {case.certificate: entry}}, out)
    (row,) = [line for line in text.splitlines() if line.startswith(f"| `{case.certificate}`")]
    cells = [cell.strip() for cell in row.strip("|").split("|")]
    assert cells[11:14] == ["-", "-", "-"]


def _view_rows(view: str) -> set[str]:
    return {
        line.split("|")[1].strip().strip("`")
        for line in view.splitlines()
        if line.startswith("| `")
    }


def test_the_committed_census_views_carry_every_census_row() -> None:
    """The generated views carry every `census.json` row and its verified count.

    #671 and #688 added census rows without regenerating the views (Review A of #688,
    A1). The views are formatted after rendering, so this compares their rows and
    their verified counts with the registers rather than their bytes; a stale row's
    contents still pass (Review C of #688, C3).
    """
    root = census.CENSUS_ROOT
    names: set[str] = set()
    for family in ("census", "census-mixed"):
        register = json.loads((root / family / "census.json").read_text(encoding="utf-8"))
        cases = register["cases"]
        view = (root / family / "README.md").read_text(encoding="utf-8")
        assert _view_rows(view) == set(cases), family
        verified = sum(entry.get("status") == "VERIFIED" for entry in cases.values())
        assert f"\n{verified} of {len(cases)} certificates verified;" in view, family
        names |= set(cases)
    summary = json.loads((root / "census-summary.json").read_text(encoding="utf-8"))
    assert {row["certificate"] for row in summary["certificates"]} == names
    view = (root / "census-summary.md").read_text(encoding="utf-8")
    assert _view_rows(view) == names


@pytest.mark.parametrize(
    ("receipts", "mark"),
    [
        ({}, "-"),
        ({"control-failed-v2": "CONTROL_FAILED"}, "CONTROL_FAILED (kept)"),
        (
            {"control-failed-v1": "CONTROL_FAILED", "control": "CONTROLS_REFUSED"},
            "CONTROLS_REFUSED",
        ),
    ],
    ids=["no-control", "failed-only", "failed-then-refused"],
)
def test_the_mixed_report_tells_a_failed_control_from_none(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    receipts: dict[str, str],
    mark: str,
) -> None:
    """A certificate whose only control receipt failed closed reads `CONTROL_FAILED
    (kept)`, not the `-` of a certificate with no control, and a passing receipt kept
    beside a failed one is the one read (A6 of PR #745's review A)."""
    case, entry, out = retained_case(tmp_path, monkeypatch)
    monkeypatch.setattr(census, "mixed_cases", lambda: [case])
    monkeypatch.setattr(
        census,
        "mixed_reference",
        lambda _: {"directions": [], "cpu_seconds": 0, "per_direction_cpu": True},
    )
    folder = out / case.packet
    (folder / f"{case.certificate}.control.json").unlink()
    for suffix, status in receipts.items():
        (folder / f"{case.certificate}.{suffix}.json").write_text(
            json.dumps({"status": status})
        )
    text = census.render_mixed_report({"cases": {case.certificate: entry}}, out)
    (row,) = [line for line in text.splitlines() if line.startswith(f"| `{case.certificate}`")]
    cells = [cell.strip() for cell in row.strip("|").split("|")]
    assert cells[-1] == mark
