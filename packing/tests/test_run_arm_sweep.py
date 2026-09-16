"""The arm sweep enforces what it reports: oracle-refused sides never reach a statistic.

Each test drives `run_arm_sweep` against a fake engine whose claims are chosen per seed,
so the independent pose oracle (`packing-campaign verify-archive`, in its own process) is
the real one and only the thing under test is faked. The fake emits the trivial grid pose
at whatever side it is told to claim: at `n = 4` that pose needs side 2, so a claim of 2 or
more is a packing and a claim of 1.9 is a number with no packing behind it.
"""

from __future__ import annotations

import json
import stat
import sys
from pathlib import Path
from typing import Any

import pytest

from devtools import run_arm_sweep

FAKE_ENGINE = """\
import json, math, sys

args = sys.argv[1:]
if args == ["--selftest"]:
    print("SELFTEST PASSED")
    raise SystemExit(0)
options = dict(zip(args[::2], args[1::2], strict=False))
n, seed = int(options["--n"]), int(options["--seed"])
claims = json.loads(options["--claims"])[str(seed)]
columns = math.ceil(math.sqrt(n))
x = [0.5 + i % columns for i in range(n)]
y = [0.5 + i // columns for i in range(n)]
for chain, side in enumerate(claims):
    line = {"kind": "chain", "n": n, "seed": seed, "chain": chain, "best_side": side,
            "overlap": 0.0, "x": x, "y": y, "t": [0.0] * n}
    print(json.dumps(line))
print(json.dumps({"kind": "summary", "n": n, "seed": seed, "pair_tests": 10, "moves": 5}))
"""


def _sweep(tmp_path: Path, claims: dict[int, list[float]]) -> tuple[Path, Path]:
    """A one-arm, one-cell plan over the fake engine, and the directory it writes to."""
    engine = tmp_path / "fake-engine"
    engine.write_text(f"#!{sys.executable}\n{FAKE_ENGINE}")
    engine.chmod(engine.stat().st_mode | stat.S_IXUSR)
    plan = tmp_path / "plan.yaml"
    body: dict[str, Any] = {
        "label": "fake sweep",
        "engine": str(engine),
        "chains": 1,
        "threads": 1,
        "budget_pair_tests": 10,
        "cells": [4],
        "seeds": sorted(claims),
        "arms": {"A-fake": ["--claims", json.dumps({str(k): v for k, v in claims.items()})]},
    }
    plan.write_text(json.dumps(body))
    return plan, tmp_path / "out"


def test_an_impossible_side_fails_the_sweep_and_stays_out_of_the_median(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The review's reproduction: side 1.9 at n = 4 was the median and the exit was 0."""
    plan, out = _sweep(tmp_path, {1: [2.0, 1.9], 2: [2.5], 3: [1.9]})
    status = run_arm_sweep.main([str(plan), "--out", str(out)])
    err = capsys.readouterr().err

    assert status != 0, "an arm the oracle refused must fail the sweep"
    assert "A-fake" in err
    assert "n=4" in err
    summary = json.loads((out / "summary.json").read_text())
    arm = summary["arms"]["A-fake"]
    cell = arm["cells"]["4"]
    assert arm["verification"]["verified"] is False
    # Seed 1 is admitted at its packing (2.0), seed 2 at 2.5, and seed 3 has no packing.
    assert cell["median_side"] == 2.25
    assert cell["best_side"] == 2.0
    assert cell["seeds"] == 2
    assert cell["rejected_poses"] == 2
    assert cell["unadmitted_seeds"] == 1
    assert cell["below_record_runs"] == 0


def test_an_admitted_side_below_the_record_fails_the_sweep(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Below the standing best is flagged by the exit status, not only by a counter.

    No packing of four unit squares beats side 2, so the record is raised instead: the pose
    is genuine, the oracle admits it, and it sits below the (moved) standing best.
    """
    monkeypatch.setattr(run_arm_sweep, "frontier_best", lambda n: (2.2, f"test n={n}"))
    plan, out = _sweep(tmp_path, {1: [2.0], 2: [2.5]})
    status = run_arm_sweep.main([str(plan), "--out", str(out)])
    err = capsys.readouterr().err

    assert status != 0
    assert "A-fake" in err
    assert "n=4" in err
    cell = json.loads((out / "summary.json").read_text())["arms"]["A-fake"]["cells"]["4"]
    assert cell["below_record_runs"] == 1


def test_a_clean_sweep_outside_the_checkout_exits_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`--out` outside the repository is legal; reporting where it wrote must not raise."""
    plan, out = _sweep(tmp_path, {1: [2.0], 2: [2.5]})
    assert run_arm_sweep.REPO not in out.resolve().parents, "the fixture must be outside"
    status = run_arm_sweep.main([str(plan), "--out", str(out)])
    stdout = capsys.readouterr().out

    assert status == 0
    wrote = json.loads(stdout.strip().splitlines()[-1])["wrote"]
    assert Path(wrote) == out / "summary.json"
    cell = json.loads((out / "summary.json").read_text())["arms"]["A-fake"]["cells"]["4"]
    assert cell["median_side"] == 2.25
    assert cell["rejected_poses"] == 0


def test_a_rebuilt_summary_does_not_claim_a_gate_it_never_saw(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The archive carries no gate result, so a rebuild records it as unknown."""
    plan, out = _sweep(tmp_path, {1: [2.0], 2: [2.5]})
    assert run_arm_sweep.main([str(plan), "--out", str(out)]) == 0
    capsys.readouterr()

    status = run_arm_sweep.main([str(plan), "--out", str(out), "--rebuild"])
    rendered = capsys.readouterr().out

    assert status == 0
    rebuilt = json.loads((out / "summary-rebuilt.json").read_text())
    assert rebuilt["gate"]["passed"] is None
    assert "Engine gate: passed" not in rendered
    assert "Engine gate: not recorded" in rendered
