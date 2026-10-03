"""The kernel memory profiler marks every step and reports the checkers' own verdicts."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from benchmarks import profile_n17_kernel_memory as profiler
from devtools import check_n17_subpattern as tool
from devtools import verify_n17_kernel_certificate as kernel_verifier
from sqpack.hull_kernel import Budget, producer, sequential
from sqpack.hull_kernel.frame import make_frame
from sqpack.hull_kernel.rational import Q

TRIANGLE = [(Q(1), Q(1)), (Q(19, 10), Q(1)), (Q(29, 20), Q(89, 50))]
SHIFTED = [(x + Q(1, 100), y) for x, y in TRIANGLE]


def test_the_profiler_marks_each_step_of_either_checker(tmp_path: Path) -> None:
    frame = make_frame(
        name="blind-pair",
        cap=Q(3),
        length=Q(3),
        cells=[TRIANGLE, SHIFTED],
        cell_names=["left", "right"],
        occupancy=2,
        action_names=("r0",),
    )
    budget = Budget(time.monotonic() + 60, 200_000)
    production = producer.produce(frame, [0, 1], bins=16, max_rounds=2, budget=budget)
    tool.save_certificate(tmp_path / "cert", production.seed, production.node)
    count = len(production.node["steps"])
    admit = sequential.admit_partner_covers
    recorder = profiler.Recorder(None)
    saved = profiler.profile_saved(
        tmp_path / "cert", recorder, 60, frame, require_no_producer=False
    )
    assert sequential.admit_partner_covers is admit
    assert saved["status"] == "PASS_SAVED_CLOSED"
    assert saved["node_sha256"] == tool.content_sha256(production.node)
    assert [step["step"] for step in recorder.steps] == list(range(count))
    assert all(step["rss_mb"] > 0 for step in recorder.steps)
    cells = tmp_path / "cells.json"
    document = {
        "U": "3",
        "order": ["left", "right"],
        "cells": {
            name: [[str(x), str(y)] for x, y in polygon]
            for name, polygon in (("left", TRIANGLE), ("right", SHIFTED))
        },
    }
    _ = cells.write_text(json.dumps(document), encoding="utf-8")
    digest = hashlib.sha256(cells.read_bytes()).hexdigest()
    check = kernel_verifier.check_partners
    recorder = profiler.Recorder(None)
    verified = profiler.profile_verifier(
        tmp_path / "cert", recorder, kernel_verifier.file_cells(cells, digest)
    )
    assert kernel_verifier.check_partners is check
    assert verified["status"] == "PASS", verified["failure"]
    assert verified["counts"]["steps"] == count
    assert [step["step"] for step in recorder.steps] == list(range(count))


def test_the_profiler_marks_production_the_save_and_the_check(tmp_path: Path) -> None:
    arguments = ["--pattern", "A", "--bins", "4", "--max-rounds", "2", "--no-collision"]
    arguments += ["--max-seconds", "60", "--save-objects", str(tmp_path)]
    produce, save = producer.produce, tool.save_certificate
    recorder = profiler.Recorder(None)
    verdict = profiler.profile_produce(arguments, recorder)
    assert (producer.produce, tool.save_certificate) == (produce, save)
    assert verdict["status"] == "PASS_CERTIFIED_STALL"
    assert set(recorder.phases) == {"produced", "saved"}
    phases = [step["phase"] for step in recorder.steps]
    count = verdict["steps_checked"]
    assert phases == ["produce"] * count + ["check"] * count
    report = recorder.report()
    assert report["peak_rss_mb"] >= report["peak_in_check_mb"] > 0
