"""Synthetic exact event parity, full replay and fixed ABBA acceptance controls."""

from __future__ import annotations

import copy
import hashlib
import json
import random
import subprocess
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest
from test_verify_n17_centered_cap import fixture, save

from devtools import profile_n17_coverage_candidate as candidate
from devtools import profile_n17_exact_replay as profile
from devtools import verify_n17_kernel_certificate as standing


def rectangle(x: Q, y: Q, w: Q = Q(1), h: Q = Q(1)) -> list[standing.Point]:
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


@pytest.mark.parametrize("offset", [Q(0), Q(1), Q(2), Q(1, 3), Q(1, 2**400)])
def test_exact_events_retain_closed_touch_and_narrow_gaps(offset: Q) -> None:
    polygons = [rectangle(Q(0), Q(0)), rectangle(Q(0), offset), rectangle(Q(0), Q(3))]
    homogeneous = [tuple(standing.homogeneous(v) for v in p) for p in polygons]
    edges, _ = standing.compile_edges(homogeneous)
    counts: dict[str, int] = {}
    expected = standing.sweep_events_reference(homogeneous, edges, (0, 1), (1, 1))
    observed = standing.sweep_events_y_filtered(
        homogeneous, edges, (0, 1), (1, 1), counts=counts
    )
    assert expected == observed
    assert counts["strict_y_rejections"] > 0
    assert (
        counts["pair_candidates"]
        == counts["strict_y_rejections"] + counts["executed_determinants"]
    )
    assert counts["probes"] == 2 * len(expected) - 1


def test_seeded_convex_and_collinear_event_rosters_are_identical() -> None:
    generator = random.Random(714)
    for _ in range(40):
        polygons = [
            standing.hull(
                [
                    (Q(generator.randrange(-4, 5), 3), Q(generator.randrange(-4, 5), 5))
                    for _ in range(10)
                ]
            )
            for _ in range(4)
        ]
        homogeneous = [tuple(standing.homogeneous(v) for v in p) for p in polygons]
        edges, _ = standing.compile_edges(homogeneous)
        assert standing.sweep_events_reference(
            homogeneous, edges, (-2, 1), (2, 1)
        ) == standing.sweep_events_y_filtered(homogeneous, edges, (-2, 1), (2, 1))


@pytest.mark.parametrize("gap", [Q(0), Q(1, 2**100)])
def test_full_sweep_decisions_and_first_probe_match(gap: Q) -> None:
    domain = rectangle(Q(0), Q(0))
    regions = [rectangle(Q(0), Q(0), Q(1, 2) - gap), rectangle(Q(1, 2), Q(0), Q(1, 2))]
    results = []
    for arm in ("baseline", "candidate"):
        with candidate.CoverageObserver(arm, time.monotonic() + 10, observe=True).installed():
            results.append(standing.covered_by_sweep(domain, regions))
    assert results[0] == results[1]
    assert results[0][0] is (gap == 0)


@pytest.mark.parametrize("domain", [[(Q(0), Q(0))], [(Q(0), Q(0)), (Q(1), Q(0))]])
def test_degenerate_coverage_is_unchanged(domain: list[standing.Point]) -> None:
    results = []
    for arm in ("baseline", "candidate"):
        with candidate.CoverageObserver(arm, time.monotonic() + 10).installed():
            results.append(standing.degenerate_covered(domain, [rectangle(Q(0), Q(0))]))
    assert results == [True, True]


@pytest.mark.parametrize("arm", ["baseline", "candidate"])
@pytest.mark.parametrize("observe", [False, True])
def test_full_synthetic_saved_replay_preserves_receipt_and_restores(
    tmp_path: Path,
    arm: str,
    observe: bool,  # noqa: FBT001 - pytest parameter
) -> None:
    cells, container, _, _ = fixture(tmp_path / "objects", closed=True)
    expected = standing.verify(tmp_path / "objects", cells, container=container)
    originals = standing.sweep_events, standing.compile_edges, standing.check_step
    observer = candidate.CoverageObserver(arm, time.monotonic() + 30, observe=observe)
    with observer.installed():
        report = profile.profile_call(
            lambda: standing.verify(tmp_path / "objects", cells, container=container),
            instrumentation="phases",
            deadline=time.monotonic() + 30,
        )
    assert report["status"] == "COMPLETE"
    assert report["mathematical_result_sha256"] == profile.result_identity(expected)
    assert (standing.sweep_events, standing.compile_edges, standing.check_step) == originals


def test_observer_restores_every_hook_after_expired_boundary() -> None:
    names = (
        "sweep_events",
        "compile_edges",
        "covered_by_sweep",
        "section_covered",
        "check_step",
    )
    originals = [getattr(standing, n) for n in names]
    with (
        pytest.raises(profile.IncompleteError),
        candidate.CoverageObserver("candidate", 0, observe=True).installed(),
    ):
        standing.compile_edges([])
    assert [getattr(standing, n) for n in names] == originals


def reports() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    result = {
        "status": "PASS_STALL",
        "mode": "full",
        "counts": {"steps": 16, "rows_full": 1024},
    }
    values = []
    rss = {}
    for i, arm in enumerate(candidate.ORDER):
        values.append(
            {
                "schema": candidate.SCHEMA,
                "matched_uninstrumented_baseline": True,
                "accepted_control_receipt_sha256": "a" * 64,
                "status": "COMPLETE",
                "arm": arm,
                "instrumentation": "phases",
                "coverage_observation": False,
                "verification_result": result,
                "mathematical_result_sha256": profile.result_identity(result),
                "input_compressed_or_file_sha256": {"seed": "a", "node": "b", "cells": "c"},
                "post_replay_input_recheck_complete": True,
                "steps": [
                    {
                        "step": k,
                        "owner": k,
                        "rows_requested_in_full": 64,
                        "counter_delta": {"rows_full": 64},
                        "memo_sizes_after_row_checks": {},
                    }
                    for k in range(16)
                ],
                "memo_evictions": [],
                "replay_wall_seconds": 100 if arm == "baseline" else 85,
                "replay_cpu_seconds": 90 if arm == "baseline" else 75,
                "runtime": {
                    "pid": i,
                    "python": "synthetic3.14",
                    "platform": "fixture",
                    "logical_cpus": 4,
                    "single_worker": True,
                },
            }
        )
        rss[str(i)] = 100000
    return values, {
        "schema": "posix-bounded-command-supervision/v1",
        "max_memory_mib_per_process": 4096,
        "max_seconds": 1440,
        "cleanup_seconds": 10,
        "status": "COMPLETED",
        "returncode": 0,
        "cleanup_complete": True,
        "maximum_sampled_current_rss_bytes_by_pid": rss,
    }


def test_fixed_two_block_gain_requires_both_wall_cpu_and_sampled_memory() -> None:
    values, guard = reports()
    assert candidate.compare(values, guard)["gain_accepted"]
    values[1]["replay_cpu_seconds"] = 90
    values[2]["replay_cpu_seconds"] = 90
    assert not candidate.compare(values, guard)["gain_accepted"]
    values, guard = reports()
    guard["maximum_sampled_current_rss_bytes_by_pid"]["1"] = 110001
    assert not candidate.compare(values, guard)["gain_accepted"]


@pytest.mark.parametrize(
    "mutation", ["order", "input", "payload", "boundary", "observer", "rss"]
)
def test_malformed_or_changed_comparison_refuses(mutation: str) -> None:
    values, guard = reports()
    values = copy.deepcopy(values)
    if mutation == "order":
        values[0]["arm"] = "candidate"
    elif mutation == "input":
        values[1]["input_compressed_or_file_sha256"]["node"] = "changed"
    elif mutation == "payload":
        values[1]["verification_result"]["counts"]["steps"] = 15
    elif mutation == "boundary":
        values[1]["memo_evictions"] = [{"owner": 1}]
    elif mutation == "observer":
        values[1]["coverage_observation"] = True
    else:
        guard["maximum_sampled_current_rss_bytes_by_pid"]["1"] = True
    with pytest.raises(ValueError, match=r"differ|invalid"):
        candidate.compare(values, guard)


def test_partial_campaign_never_claims_gain() -> None:
    values, guard = reports()
    values[7]["status"] = "INCOMPLETE"
    assert candidate.compare(values, guard) == {
        "schema": candidate.SCHEMA,
        "status": "INCOMPLETE",
        "gain_accepted": False,
    }


def test_plan_emits_eight_distinct_fresh_processes_without_launch(tmp_path: Path) -> None:
    value = candidate.plan(["--directory", "objects", "--max-seconds", "180"], tmp_path)
    assert (
        tuple(p["argv"][p["argv"].index("--arm") + 1] for p in value["phases"])
        == candidate.ORDER
    )
    assert len({p["argv"][-1] for p in value["phases"]}) == 8
    assert not value["benchmarks_launched"]


def test_observed_diagnostic_cannot_accept_speed_gain() -> None:
    values, guard = reports()
    for value in values:
        value["coverage_observation"] = True
    assert not candidate.compare(values, guard)["gain_accepted"]


@pytest.mark.parametrize("mutation", ["runtime", "pid", "step", "guard"])
def test_measurement_regime_and_complete_boundary_refusal(mutation: str) -> None:
    values, guard = reports()
    if mutation == "runtime":
        values[1]["runtime"]["python"] = "different"
    elif mutation == "pid":
        values[1]["runtime"]["pid"] = 0
    elif mutation == "step":
        values[1]["steps"].pop()
    else:
        guard["max_memory_mib_per_process"] = 8192
    with pytest.raises(ValueError, match="differ"):
        candidate.compare(values, guard)


def test_empty_event_diagnostics_do_not_claim_negative_probes() -> None:
    counts: dict[str, int] = {}
    assert standing.sweep_events_y_filtered([], [], (0, 1), (0, 1), counts=counts) == []
    assert counts["probes"] == 0


def live_fixture(directory: Path) -> tuple[standing.Cells, standing.CenteredContainer]:
    cells, container, seed, node = fixture(directory)
    row = copy.deepcopy(seed["cells"]["0"][0])
    core = rectangle(Q(-1, 8), Q(-1, 8), Q(1, 4), Q(1, 4))
    vertices = standing.poly(row["outer_domain"])
    planes = []
    for i, p in enumerate(core):
        q = core[(i + 1) % len(core)]
        a, b = q[1] - p[1], p[0] - q[0]
        planes.append(
            {
                "normal": [str(a), str(b)],
                "upper": str(a * p[0] + b * p[1] + min(a * x + b * y for x, y in vertices)),
            }
        )
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    row.update(
        reference={"kind": "phase3", "node": "synthetic", "step": 0, "row": 0},
        prior_reference=copy.deepcopy(row["reference"]),
        core_vertices=[[str(x), str(y)] for x, y in core],
        common_core_halfplanes=planes,
        collision_regions=[],
        self_hull_cuts=[],
        outer_bounds=[
            {"normal": [str(a), str(b)], "upper": str(max(a * x + b * y for x, y in vertices))}
            for a, b in directions
        ],
    )
    node["steps"] = [
        {
            "index": 0,
            "owner": 0,
            "complete": True,
            "allowed_half_angle": ["0", "1"],
            "prior_owned_hulls": copy.deepcopy(seed["groups"]),
            "prior_partner_pose_covers": {},
            "rows": [row],
            "common_owned_kernel": [],
        }
    ]
    node["final_state"]["cells"]["0"][0]["reference"] = row["reference"]
    save(directory, seed, node)
    return cells, container


def test_full_live_row_replay_executes_exact_sweep_in_both_arms(tmp_path: Path) -> None:
    cells, container = live_fixture(tmp_path / "objects")
    results = []
    for arm in ("baseline", "candidate"):
        observer = candidate.CoverageObserver(arm, time.monotonic() + 30, observe=True)
        with observer.installed():
            result = standing.verify(tmp_path / "objects", cells, container=container)
        assert observer.counts["event_calls"] > 0
        results.append(result)
    assert profile.result_identity(results[0]) == profile.result_identity(results[1])
    assert results[0]["counts"]["steps"] == 1


def test_two_clean_processes_keep_full_live_math_and_input_identity(tmp_path: Path) -> None:
    cells, _ = live_fixture(tmp_path / "objects")
    cellpath = tmp_path / "cells.json"
    cellpath.write_text(
        json.dumps(
            {
                "U": "4",
                "order": list(cells.names),
                "cells": {
                    name: [[str(x), str(y)] for x, y in p]
                    for name, p in zip(cells.names, cells.polygons, strict=True)
                },
            }
        )
    )
    digest = hashlib.sha256(cellpath.read_bytes()).hexdigest()
    accepted = tmp_path / "accepted-none.json"
    assert (
        profile.main(
            [
                "--directory",
                str(tmp_path / "objects"),
                "--cells",
                str(cellpath),
                "--cells-sha256",
                digest,
                "--centered-inner-cap",
                "3",
                "--max-seconds",
                "30",
                "--instrumentation",
                "none",
                "--output",
                str(accepted),
            ]
        )
        == 0
    )
    accepted_sha = hashlib.sha256(accepted.read_bytes()).hexdigest()
    results = []
    for arm in ("baseline", "candidate"):
        output = tmp_path / f"{arm}.json"
        run = subprocess.run(
            [
                sys.executable,
                "-m",
                "devtools.profile_n17_coverage_candidate",
                "replay",
                "--arm",
                arm,
                "--directory",
                str(tmp_path / "objects"),
                "--cells",
                str(cellpath),
                "--cells-sha256",
                digest,
                "--centered-inner-cap",
                "3",
                "--max-seconds",
                "30",
                "--compare",
                str(accepted),
                "--output",
                str(output),
            ],
            capture_output=True,
            text=True,
            timeout=40,
            check=False,
        )
        assert run.returncode == 0, run.stderr + run.stdout
        result = json.loads(output.read_text())
        assert result["status"] == "COMPLETE"
        assert result["matched_uninstrumented_baseline"] is True
        assert result["accepted_control_receipt_sha256"] == accepted_sha
        results.append(result)
    assert results[0]["runtime"]["pid"] != results[1]["runtime"]["pid"]
    assert results[0]["mathematical_result_sha256"] == results[1]["mathematical_result_sha256"]
    assert candidate.boundary_payload(results[0]) == candidate.boundary_payload(results[1])
    assert (
        results[0]["input_compressed_or_file_sha256"]
        == results[1]["input_compressed_or_file_sha256"]
    )


@pytest.mark.parametrize("mutation", ["accepted_sha", "accepted_match"])
def test_accepted_control_receipt_must_join_every_arm(mutation: str) -> None:
    values, guard = reports()
    if mutation == "accepted_sha":
        values[1]["accepted_control_receipt_sha256"] = "b" * 64
    else:
        values[1]["matched_uninstrumented_baseline"] = False
    with pytest.raises(ValueError, match="accepted control"):
        candidate.compare(values, guard)
