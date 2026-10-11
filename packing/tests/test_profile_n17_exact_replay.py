"""Target-free profiling custody and exact-check preservation controls."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest
from test_verify_n17_centered_cap import fixture

from devtools import profile_n17_exact_replay as profile
from devtools import verify_n17_kernel_certificate as standing

SQUARE = [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1))]


def test_callgraph_counts_actual_cache_hits_and_misses() -> None:
    state = standing.State([SQUARE], Q(4), 1, [0])
    core = tuple(standing.homogeneous(p) for p in SQUARE)
    cover = standing.CoverRow(None, None, core, core)

    def run() -> dict[str, Any]:
        assert state.difference(core, core) == state.difference(core, core)
        assert state.forbidden_region(SQUARE, SQUARE) == state.forbidden_region(SQUARE, SQUARE)
        assert cover.minimum(1, 0) == cover.minimum(1, 0)
        _ = cover.minimum(0, 1)
        return {"status": "PASS_STALL", "mode": "full"}

    report = profile.profile_call(
        run, instrumentation="callgraph", deadline=time.monotonic() + 30
    )
    counters = report["callgraph"]["cache_counts"]
    assert counters["facets"] == {"lookups": 2, "misses": 1, "hits": 1}
    assert counters["forbidden_regions"] == {"lookups": 2, "misses": 1, "hits": 1}
    assert counters["support_minima"] == {"lookups": 3, "misses": 2, "hits": 1}
    assert report["profile_overhead_is_not_gain"]
    assert not report["scientific_admission_proved"]


def test_callgraph_counts_admitted_partner_cover_reuse() -> None:
    state = standing.State([SQUARE, SQUARE], Q(4), 1, [0, 1])
    reference = {"kind": "wall_seed", "owner": 1, "row": 0}
    state.rows[1] = [standing.Row((Q(0), Q(1)), reference, SQUARE, [SQUARE])]
    item = {
        "reference": reference,
        "interval": ["0", "1"],
        "domain": [[str(x), str(y)] for x, y in SQUARE],
        "core": [[str(x / 10), str(y / 10)] for x, y in SQUARE],
    }
    step = {"owner": 0, "prior_partner_pose_covers": {"1": [item]}}

    def run() -> dict[str, Any]:
        standing.check_partners(state, step, 0)
        standing.check_partners(state, step, 0)
        return {"status": "PASS_STALL", "mode": "full", "counts": state.stats}

    report = profile.profile_call(
        run, instrumentation="callgraph", deadline=time.monotonic() + 30
    )
    assert report["callgraph"]["cache_counts"]["partner_row_covers"] == {
        "lookups": 2,
        "misses": 1,
        "hits": 1,
    }


@pytest.mark.parametrize("instrumentation", ["none", "phases", "stages", "callgraph"])
def test_complete_standing_replay_retains_exact_receipt(
    tmp_path: Path, instrumentation: str
) -> None:
    cells, container, _, _ = fixture(tmp_path / "objects", closed=True)
    original = standing.verify(tmp_path / "objects", cells, container=container)
    check, bound = standing.check_step, standing.bound_memos
    report = profile.profile_call(
        lambda: standing.verify(tmp_path / "objects", cells, container=container),
        instrumentation=instrumentation,
        deadline=time.monotonic() + 30,
    )
    assert report["status"] == "COMPLETE"
    assert report["verification_result"]["status"] == "PASS_CLOSED"
    assert profile.result_payload(report["verification_result"]) == profile.result_payload(
        original
    )
    assert report["mathematical_result_sha256"] == profile.result_identity(original)
    assert (standing.check_step, standing.bound_memos) == (check, bound)
    if instrumentation != "none":
        assert report["steps"][0]["rows_requested_in_full"] == 1
        assert len(report["memo_evictions"]) == 1


def test_memo_evictions_are_observed_without_changing_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state = standing.State([SQUARE], Q(4), 1, [0])
    state.groups[0] = [(Q(2), Q(2))]
    core = tuple(standing.homogeneous(p) for p in SQUARE)
    _ = state.difference(core, core)
    _ = state.forbidden_region(SQUARE, SQUARE)
    monkeypatch.setattr(standing, "MEMO_PAIRS", 0)
    recorder = profile.Recorder(time.monotonic() + 30)
    with recorder.installed():
        standing.bound_memos(state, 0, SQUARE)
    assert state.facets == state.forbidden == {}
    assert recorder.evictions[0]["facet_pairs_evicted"] == 1
    assert recorder.evictions[0]["forbidden_pairs_evicted"] == 1


def test_observers_restore_after_failure() -> None:
    check, bound = standing.check_step, standing.bound_memos

    def broken() -> dict[str, Any]:
        raise RuntimeError("injected failure")

    with pytest.raises(RuntimeError, match="injected"):
        profile.profile_call(
            broken, instrumentation="callgraph", deadline=time.monotonic() + 30
        )
    assert (standing.check_step, standing.bound_memos) == (check, bound)
    assert sys.getprofile() is None


def test_expired_profile_keeps_partial_diagnostics_without_verdict() -> None:
    def expired() -> dict[str, Any]:
        raise profile.IncompleteError("synthetic ceiling")

    report = profile.profile_call(
        expired, instrumentation="callgraph", deadline=time.monotonic() + 30
    )
    assert report["status"] == "INCOMPLETE"
    assert report["verification_result"] is None
    assert report["mathematical_result_sha256"] is None
    assert report["callgraph"]["functions"]


def test_current_rss_failure_is_explicit_and_never_a_peak_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unavailable() -> int:
        raise OSError("no RSS")

    monkeypatch.setattr(profile, "current_memory_bytes", unavailable)
    sample = profile.memory_sample()
    assert sample["current_rss_bytes"] is None
    assert "no RSS" in sample["current_rss_error"]


@pytest.mark.parametrize("token", ["1e999999999", "1/0", "2/4", "-0", "1" * 2501])
def test_cap_parser_refuses_before_unbounded_fraction_allocation(token: str) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        profile.cap_rational(token)
    assert profile.cap_rational("935106018721/200000000000") == Q(935106018721, 200000000000)


def test_digest_enforces_streamed_bytes_after_initial_stat(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "growing"
    path.write_bytes(b"0123456789")
    original = Path.stat

    def stale_stat(self: Path, *args: Any, **kwargs: Any) -> Any:
        return (
            type("Stat", (), {"st_size": 1})()
            if self == path
            else original(self, *args, **kwargs)
        )

    monkeypatch.setattr(Path, "stat", stale_stat)
    with pytest.raises(profile.IncompleteError, match="streamed"):
        profile.digest(path, time.monotonic() + 30, ceiling=5)


def test_serialization_expiry_cannot_publish_complete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = profile.retained_json.dumps
    now = [100.0]
    monkeypatch.setattr(profile.time, "monotonic", lambda: now[0])

    def slow_serialization(value: Any, *args: Any, **kwargs: Any) -> str:
        encoded = original(value, *args, **kwargs)
        now[0] = 200.0
        return encoded

    monkeypatch.setattr(profile.retained_json, "dumps", slow_serialization)
    output = tmp_path / "expired.json"
    assert profile.main([*cli_inputs(tmp_path), "--output", str(output)]) == 1
    result = json.loads(output.read_bytes())
    assert result["status"] == "INCOMPLETE"
    assert "final wall" in result["error"]


@pytest.mark.parametrize("changed", ["mode", "status", "container", "counts", "certificate"])
def test_result_identity_preserves_all_mathematical_boundaries(changed: str) -> None:
    result = {
        "mode": "full",
        "status": "PASS_STALL",
        "container": {"inner": "3"},
        "counts": {"rows_full": 1},
        "certificate": {"node_sha256": "a"},
    }
    tampered = copy.deepcopy(result)
    tampered[changed] = "changed"
    assert profile.result_identity(result) != profile.result_identity(tampered)
    timed = result | {"seconds": 5, "provenance": {"revision": "presentation"}}
    assert profile.result_identity(result) == profile.result_identity(timed)


def cli_inputs(tmp_path: Path) -> list[str]:
    cells, _, _, _ = fixture(tmp_path / "objects", closed=True)
    document = {
        "U": str(cells.cap),
        "order": list(cells.names),
        "cells": {
            name: [[str(x), str(y)] for x, y in polygon]
            for name, polygon in zip(cells.names, cells.polygons, strict=True)
        },
    }
    path = tmp_path / "cells.json"
    path.write_text(json.dumps(document))
    return [
        "--directory",
        str(tmp_path / "objects"),
        "--cells",
        str(path),
        "--cells-sha256",
        hashlib.sha256(path.read_bytes()).hexdigest(),
        "--centered-inner-cap",
        "3",
        "--max-seconds",
        "30",
    ]


@pytest.mark.parametrize("diagnostic", ["callgraph", "stages"])
def test_two_fresh_cli_processes_match_full_replay(tmp_path: Path, diagnostic: str) -> None:
    args = cli_inputs(tmp_path)
    baseline, candidate = tmp_path / "baseline.json", tmp_path / "candidate.json"
    for mode, path, extra in (
        ("none", baseline, []),
        (diagnostic, candidate, ["--compare", str(baseline)]),
    ):
        done = subprocess.run(
            [
                sys.executable,
                "-m",
                "devtools.profile_n17_exact_replay",
                *args,
                "--instrumentation",
                mode,
                "--output",
                str(path),
                *extra,
            ],
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        assert done.returncode == 0, done.stdout + done.stderr
    report = json.loads(candidate.read_text())
    assert report["matched_uninstrumented_baseline"]
    assert report["verification_result"]["mode"] == "full"
    assert report["verification_result"]["counts"]["steps"] == 1
    assert report["post_replay_input_recheck_complete"]
    if diagnostic == "stages":
        records = report["stage_attribution"]["records"]
        assert any(r["stage"] == "node_step_decode_or_eof" for r in records)
        assert any(r["stage"] == "compress" and r["step"] == 0 for r in records)


def test_stage_nested_wall_and_cpu_partition_does_not_double_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = [0.0]
    monkeypatch.setattr(profile.time, "perf_counter", lambda: now[0])
    monkeypatch.setattr(profile.time, "process_time", lambda: now[0] / 2)
    recorder = profile.StageRecorder(time.monotonic() + 30)

    def inner() -> int:
        now[0] += 2
        return 7

    def outer() -> int:
        now[0] += 1
        result = recorder.measure("inner", inner)
        now[0] += 3
        return result

    assert recorder.measure("outer", outer) == 7
    records = {r["stage"]: r for r in recorder.report(8, 4)["records"]}
    assert records["outer"]["inclusive_wall_seconds"] == 6
    assert records["outer"]["exclusive_wall_seconds"] == 4
    assert records["inner"]["exclusive_wall_seconds"] == 2
    assert records["outer"]["exclusive_cpu_seconds"] == 2
    report = recorder.report(8, 4)
    assert report["unattributed_replay_wall_seconds"] == 2
    assert report["unattributed_replay_cpu_seconds"] == 1


@pytest.mark.parametrize("failure", ["runtime", "deadline"])
def test_stage_hooks_restore_all_functions_after_failed_work(failure: str) -> None:
    names = (
        "check_seed",
        "check_final",
        "check_centered_final",
        "load_object",
        "check_step",
        "check_partners",
        "compress",
        "derive_closure",
        "check_collisions",
        "check_cover",
    )
    originals = {name: getattr(standing, name) for name in names}
    stream_originals = standing.NodeStream.__init__, standing.NodeStream.steps
    recorder = profile.StageRecorder(time.monotonic() + 30)
    expected = RuntimeError if failure == "runtime" else profile.IncompleteError

    def broken() -> None:
        if failure == "deadline":
            recorder.deadline = time.monotonic() - 1
            raise profile.IncompleteError("injected deadline")
        raise RuntimeError("injected failure")

    with pytest.raises(expected, match="injected"), recorder.installed():
        recorder.measure("failing_work", broken)
    assert {name: getattr(standing, name) for name in names} == originals
    assert (standing.NodeStream.__init__, standing.NodeStream.steps) == stream_originals
    assert recorder.stack == []
    assert recorder.records[(None, "failing_work")]["failed_calls"] == 1


def test_stage_expiry_retains_partial_attribution_without_acceptance() -> None:
    def expired() -> dict[str, Any]:
        raise profile.IncompleteError("synthetic incomplete")

    report = profile.profile_call(
        expired, instrumentation="stages", deadline=time.monotonic() + 30
    )
    assert report["status"] == "INCOMPLETE"
    assert report["verification_result"] is None
    assert report["stage_attribution"] is not None
    assert report["mathematical_result_sha256"] is None


def test_tampered_baseline_is_not_matched(tmp_path: Path) -> None:
    args = cli_inputs(tmp_path)
    baseline = tmp_path / "baseline.json"
    assert profile.main([*args, "--instrumentation", "none", "--output", str(baseline)]) == 0
    data = json.loads(baseline.read_text())
    data["verification_result"]["closed"] = False
    baseline.write_text(json.dumps(data))
    output = tmp_path / "candidate.json"
    assert profile.main([*args, "--compare", str(baseline), "--output", str(output)]) == 1
    assert json.loads(output.read_text())["status"] == "REFUSED"


@pytest.mark.parametrize("limit", ["0", "-1", "nan", "inf"])
def test_invalid_profile_wall_limit_refused(tmp_path: Path, limit: str) -> None:
    with pytest.raises(SystemExit):
        profile.main(
            [
                "--directory",
                str(tmp_path),
                "--max-seconds",
                limit,
                "--output",
                str(tmp_path / "out.json"),
            ]
        )
