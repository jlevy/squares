"""Every planned benchmark attempt is counted: failures, refusals, budget stops and replays."""

from __future__ import annotations

import argparse
import io
import json
import math
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest

from devtools.known_structure import record
from workbench_tools import benchmark as bench
from workbench_tools.probes import probe
from workbench_tools.trial_records import (
    AttemptFailure,
    EffectiveConfiguration,
    PackingReference,
    RepairReceipt,
    SourceReceipt,
    Trial,
    admission_reason,
    attempt_from_json,
    attempt_to_json,
    canonical_reference,
    gap_closed,
)


def _source() -> SourceReceipt:
    return SourceReceipt(
        commit="0" * 40,
        dirty=False,
        page="packing/site/workbench/index.html",
        page_sha256="1" * 64,
        benchmark="packages/workbench/probes/bench-annealing.ts",
        browser="chromium",
        browser_version="test",
        browser_executable="/test/chromium",
        playwright_version="test",
        python_version="3.14.0",
        platform="test",
        viewport_width=1920,
        viewport_height=1080,
    )


def _probe_result(seed: int) -> dict[str, object]:
    """What the browser probe returns for the n = 5 record, as a seed's trial would."""
    matrix, side = record(5)
    poses = [[float(x), float(y), float(angle)] for x, y, angle in matrix]
    reference = canonical_reference(5)
    return {
        "configuration": {
            "style": "bodies",
            "mode": "blind",
            "seed": seed,
            "inflate": 1.12,
            "anneal": 3,
            "pairLaw": {"rigidity": 0.15, "repulsion": 2500, "attraction": 0, "range": 0},
            "wallLaw": {"rigidity": 0.25, "repulsion": 2500, "attraction": 0, "range": 0},
            "timing": {"dwell": 0.6, "move": 0.8, "correct": 0.25, "settle": 0.4},
            "annealSpan": 0.95,
        },
        "excess": (side / reference.side - 1) * 100,
        "side": side,
        "record": reference.side,
        "centre": 0.0,
        "angle": 0.0,
        "overlap": 0.0,
        "poses": poses,
        "resolvedPoses": poses,
        "resolvedSide": side,
        "resolvedOverlap": 0.0,
        "repairSweeps": 0,
        "repairSweepLimit": 400,
        "repairConverged": True,
        "steps": 20,
        "physicsMs": 0.4,
        "repairMs": 0.1,
        "ms": 1.0,
    }


def _run(sizes: list[int], seeds: list[int], budget: float = 60.0) -> bench.Run:
    return bench.Run(
        sizes=sizes,
        seeds=seeds,
        style="bodies",
        inflate=None,
        anneal=None,
        budget=budget,
        out=Path("unused.jsonl"),
    )


class _BrowserFault(bench.ProbeCallError):
    pass


def _attempts(
    evaluate: Callable[[dict[str, object]], object],
    run: bench.Run,
    *,
    clock: Callable[[], float] = lambda: 0.0,
) -> tuple[bench.RunResult, list[str]]:
    sink = io.StringIO()
    result = bench.run_attempts(evaluate, run, _source(), sink, clock=clock)
    return result, sink.getvalue().splitlines()


def test_each_malformed_probe_result_is_a_counted_failure_not_an_abort() -> None:
    broken: dict[int, Callable[[dict[str, object]], object]] = {
        1: lambda row: {**row, "excess": math.nan},
        2: lambda row: {**row, "overlap": math.inf},
        3: lambda row: {**row, "repairConverged": None},
        4: lambda row: {**row, "steps": 1.5},
        6: lambda row: {
            **row,
            "resolvedPoses": [
                [math.nan, 0.5, 0.0],
                *cast(list[object], row["resolvedPoses"])[1:],
            ],
        },
    }

    def evaluate(options: dict[str, object]) -> object:
        seed = cast(int, options["seed"])
        if seed == 5:
            raise _BrowserFault("Target page, context or browser has been closed")
        result = _probe_result(seed)
        return broken[seed](result) if seed in broken else result

    result, lines = _attempts(evaluate, _run([5], list(range(8))))
    assert [trial.seed for trial in result.trials] == [0, 7]
    assert [(failure.seed, failure.reason) for failure in result.failures] == [
        (1, "malformed-result"),
        (2, "malformed-result"),
        (3, "malformed-result"),
        (4, "malformed-result"),
        (5, "browser-error"),
        (6, "malformed-result"),
    ]
    assert "finite" in result.failures[-1].detail
    assert result.planned == [(5, seed) for seed in range(8)]
    assert result.attempted == len(result.planned)
    assert not result.stopped_early
    replayed = [attempt_from_json(line) for line in lines]
    assert [type(row).__name__ for row in replayed] == [
        "Trial",
        *["AttemptFailure"] * 6,
        "Trial",
    ]
    assert all(admission_reason(trial) is None for trial in result.trials)


def test_a_probe_error_counts_every_remaining_seed_of_that_n() -> None:
    calls: list[int] = []

    def evaluate(options: dict[str, object]) -> object:
        n = cast(int, options["n"])
        calls.append(n)
        if n == 9:
            return {"error": "the page carries no pair into n = 9"}
        return _probe_result(cast(int, options["seed"]))

    result, _lines = _attempts(evaluate, _run([9, 5], [0, 1, 2]))
    assert calls == [9, 5, 5, 5]
    assert [(failure.n, failure.seed, failure.reason) for failure in result.failures] == [
        (9, 0, "probe-error"),
        (9, 1, "probe-error"),
        (9, 2, "probe-error"),
    ]
    assert [trial.seed for trial in result.trials] == [0, 1, 2]


def test_a_missing_witness_is_a_reference_failure() -> None:
    def missing(_n: int) -> PackingReference:
        raise FileNotFoundError("witnesses/known-best/n-005.yaml")

    sink = io.StringIO()
    result = bench.run_attempts(
        lambda options: _probe_result(cast(int, options["seed"])),
        _run([5], [0]),
        _source(),
        sink,
        clock=lambda: 0.0,
        reference_for=missing,
    )
    assert [(failure.reason, failure.detail) for failure in result.failures] == [
        ("reference-unavailable", "witnesses/known-best/n-005.yaml")
    ]


def test_a_nonfinite_pose_in_a_stored_trial_is_named_nonfinite_geometry() -> None:
    trial = bench.run_attempts(
        lambda options: _probe_result(cast(int, options["seed"])),
        _run([5], [0]),
        _source(),
        io.StringIO(),
        clock=lambda: 0.0,
    ).trials[0]
    assert trial.resolved_poses is not None
    forged = replace(trial, resolved_poses=((math.nan, 0.5, 0.0), *trial.resolved_poses[1:]))
    assert admission_reason(forged) == "nonfinite-geometry"


def test_a_budget_stop_is_partial_names_its_counts_and_fails(
    capsys: pytest.CaptureFixture[str],
) -> None:
    ticks = iter([0.0, 0.0, 1.0, 5.0, 5.0, 5.0, 5.0])
    result, _lines = _attempts(
        lambda options: _probe_result(cast(int, options["seed"])),
        _run([5], list(range(6)), budget=2.0),
        clock=lambda: next(ticks),
    )
    assert result.stopped_early
    assert result.attempted == 2
    assert (
        bench.report(result.trials, result.failures, planned=result.planned, stopped_early=True)
        == 1
    )
    output = capsys.readouterr().out
    assert "PARTIAL" in output
    assert "planned 6, attempted 2, admitted 2" in output
    best_line = output.split("best-of-10", 1)[1].splitlines()[1].split()
    assert best_line == ["5", "1.000", "-", "-", "-", "-"]


def _admitted_scores(
    monkeypatch: pytest.MonkeyPatch, closed: dict[int, float], refused: set[int]
) -> list[Trial]:
    """Trials whose score is set directly, with admission reduced to a seed list."""
    base = bench.run_attempts(
        lambda options: _probe_result(cast(int, options["seed"])),
        _run([5], [0]),
        _source(),
        io.StringIO(),
        clock=lambda: 0.0,
    ).trials[0]
    assert base.configuration is not None
    trials = [
        replace(
            base,
            seed=seed,
            configuration=replace(base.configuration, seed=seed),
            resolved_closed=score,
        )
        for seed, score in sorted(closed.items())
    ]

    def partition(rows: list[Trial]) -> tuple[list[Trial], dict[str, int]]:
        kept = [trial for trial in rows if trial.seed not in refused]
        return kept, (
            {"invalid-packing": len(rows) - len(kept)} if len(kept) < len(rows) else {}
        )

    monkeypatch.setattr(bench, "partition_trials", partition)
    return trials


def test_best_of_k_is_over_the_first_k_planned_seeds_with_refusals_as_misses(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    scores = {seed: 0.1 + seed / 100 for seed in range(11)}
    scores[10] = 0.9
    trials = _admitted_scores(monkeypatch, scores, refused={3})
    planned = [(5, seed) for seed in range(11)]
    assert bench.report(trials, planned=planned) == 0
    output = capsys.readouterr().out
    assert "planned 11, attempted 11, admitted 10" in output
    best_line = output.split("best-of-10", 1)[1].splitlines()[1]
    assert "0.190" in best_line
    assert "0.900" not in best_line
    assert "rates per attempted seed" in output


def test_sweep_keeps_every_planned_cell_and_gates_best_of_k_on_attempted_seeds(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    one = _probe_result(0)
    source = _source()

    def run_trials(run: bench.Run) -> bench.RunResult:
        trial = bench.run_attempts(
            lambda _options: one, replace(run, sizes=[5], seeds=[0]), source, io.StringIO()
        ).trials
        return bench.RunResult(
            planned=[(n, seed) for n in run.sizes for seed in run.seeds],
            trials=trial,
            failures=[],
            stopped_early=True,
        )

    monkeypatch.setattr(bench, "RESULTS", tmp_path)
    monkeypatch.setattr(bench, "run_trials", run_trials)
    args = argparse.Namespace(
        sweep=["anneal=3"], n=[5, 11], style="bodies", inflate=None, anneal=None, budget=1.0
    )
    assert bench.sweep(args, list(range(10)), "fixture") == 1
    output = capsys.readouterr().out
    rows = [line for line in output.splitlines() if line.strip().startswith("3 ")]
    assert len(rows) == 2, output
    assert "PARTIAL" in output
    assert all("1.000" not in row.split()[-1] for row in rows), rows


def test_replay_reports_unlike_rows_separately_and_refuses_duplicate_seeds(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = _source()
    trial = bench.run_attempts(
        lambda options: _probe_result(cast(int, options["seed"])),
        _run([5], [0, 1]),
        source,
        io.StringIO(),
        clock=lambda: 0.0,
    ).trials
    assert trial[1].configuration is not None
    other_level = replace(
        trial[1],
        params={"anneal": 6},
        configuration=replace(cast(EffectiveConfiguration, trial[1].configuration), anneal=6),
    )
    failure = AttemptFailure(
        n=5,
        seed=2,
        style="bodies",
        params={},
        reason="browser-error",
        detail="closed",
        source=source,
    )
    path = tmp_path / "rows.jsonl"
    path.write_text(
        "\n".join(attempt_to_json(row) for row in (trial[0], other_level, failure)) + "\n",
        encoding="utf-8",
    )
    assert bench.main(["--replay", str(path)]) == 0
    output = capsys.readouterr().out
    assert output.count("== group") == 2
    assert "failed 1 (browser-error=1)" in output

    duplicate = tmp_path / "duplicate.jsonl"
    duplicate.write_text(
        "\n".join(attempt_to_json(row) for row in (trial[0], trial[0])) + "\n", encoding="utf-8"
    )
    assert bench.main(["--replay", str(duplicate)]) == 2
    assert "duplicate" in capsys.readouterr().out


def test_failure_rows_round_trip_strictly() -> None:
    failure = AttemptFailure(
        n=5,
        seed=3,
        style="bodies",
        params={"anneal": 3},
        reason="malformed-result",
        detail="excess must be a finite number",
        source=_source(),
    )
    assert attempt_from_json(attempt_to_json(failure)) == failure
    row = json.loads(attempt_to_json(failure))
    row["reason"] = "made-up"
    with pytest.raises(ValueError, match="failure reason"):
        attempt_from_json(json.dumps(row))
    assert isinstance(attempt_from_json(attempt_to_json(_trial_from_probe())), Trial)


def _trial_from_probe() -> Trial:
    return bench.run_attempts(
        lambda options: _probe_result(cast(int, options["seed"])),
        _run([5], [0]),
        _source(),
        io.StringIO(),
        clock=lambda: 0.0,
    ).trials[0]


def test_repair_receipt_and_gap_score_helpers_still_agree() -> None:
    trial = _trial_from_probe()
    assert isinstance(trial.repair, RepairReceipt)
    assert trial.resolved_closed == gap_closed(5, trial.record, trial.excess)


def test_a_missing_page_names_the_build_command_that_exists(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    monkeypatch.setattr(bench, "PAGE", tmp_path / "missing.html")
    assert bench.main(["--n", "5", "--seeds", "1"]) == 1
    output = capsys.readouterr().out
    assert "squares-workbench-build" in output
    assert "devtools" not in output


def test_the_harness_drives_the_page_only_through_probe_files() -> None:
    source = Path(bench.__file__).read_text(encoding="utf-8")
    for call in ("page.wait_for_function(", "page.evaluate(", ".add_init_script("):
        for line in source.splitlines():
            if call in line:
                assert "probe(" in line, line
    for name in bench.BENCHMARK_PROBES.values():
        assert probe(name).strip()
