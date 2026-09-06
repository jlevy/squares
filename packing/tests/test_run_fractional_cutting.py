"""Controls for the cutting-plane driver's launch-critical artifact paths.

A warm start only moves to a larger side, so a fresh side below every retained
state -- the scalar probe at ``61/16`` that agenda-025 pre-registers -- has to
start from the grid. ``--seed-certificate`` lets it start from the grid plus a
retained certificate's atom sites, carried by the same maps the column
generator uses; the driver records what it seeded, and refuses the flag beside
``--warm``, where the state already carries the sites it earned.

The covering-crossing control uses the same coarse fixture to exercise the
real loop, all four output artifacts, and the covering freeze bridge that must
consume the stopped state.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import run_fractional_cutting as cutting_driver
from devtools.freeze_cutting_primal import bridge
from devtools.run_fractional_colgen import seed_points_from
from devtools.run_fractional_cutting import main
from sqpack.fractional.cutting import CuttingLog
from sqpack.fractional.generate import net_half_tangents

LIMIT = "207107/500000"


def tiny_certificate(path: Path) -> None:
    """Four atoms at the quarter points of side 2, as a retained record carries them."""

    record = {
        "id": "C-n005-fractional-2-1",
        "n": 5,
        "claim": "s(5) >= 2",
        "outer_side": "2",
        "square_side": "9977/10000",
        "angle_limit": LIMIT,
        "direction_steps": 1,
        "total_mass": "4",
        "least_cell_mass": None,
        "symmetry": "D4",
        "atoms": [
            ["3/4", "3/4", "1"],
            ["5/4", "3/4", "1"],
            ["3/4", "5/4", "1"],
            ["5/4", "5/4", "1"],
        ],
    }
    path.write_text(json.dumps(record) + "\n")


def run(tmp_path: Path, *extra: str) -> tuple[int, dict[str, object]]:
    summary = tmp_path / "summary.json"
    code = main(
        [
            "--n", "5", "--side", "21/10", "--angle-limit", LIMIT, "--steps", "1",
            "--grids", "5", "--minutes", "1", "--iterations", "1", "--cap", "8",
            "--json", str(summary), *extra,
        ]
    )  # fmt: skip
    settings = json.loads(summary.read_text())["settings"]
    assert isinstance(settings, dict)
    return code, settings


def test_the_seed_joins_the_grid_and_is_recorded(tmp_path: Path) -> None:
    seed = tmp_path / "seed.json"
    tiny_certificate(seed)
    _, plain = run(tmp_path)
    code, seeded = run(tmp_path, "--seed-certificate", str(seed), "--seed-map", "centre")
    assert code == 0
    assert seeded["seed_certificate"] == str(seed)
    assert seeded["seed_map"] == "centre"
    assert seeded["seed_sites"] == len(seed_points_from(seed, Fraction(21, 10), "centre"))
    initial, plain_initial = seeded["initial_sites"], plain["initial_sites"]
    assert isinstance(initial, int)
    assert isinstance(plain_initial, int)
    assert initial > plain_initial
    assert "centre-mapped" in str(seeded["origin"])
    assert plain["seed_certificate"] is None
    assert plain["seed_sites"] == 0


def test_a_seed_beside_a_warm_start_is_refused(tmp_path: Path) -> None:
    seed = tmp_path / "seed.json"
    tiny_certificate(seed)
    state = tmp_path / "state.json"
    code, _ = run(tmp_path, "--state", str(state))
    assert code == 0
    with pytest.raises(SystemExit):
        run(tmp_path, "--warm", str(state), "--seed-certificate", str(seed))


def test_the_safe_stop_flag_and_scoped_timings_are_recorded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, object] = {}

    def fake_loop(*_args: object, **kwargs: object) -> CuttingLog:
        captured.update(kwargs)
        return CuttingLog(stopped="synthetic stop")

    wall = iter((10.0, 20.0, 32.0, 45.0))
    cpu = iter((5.0, 8.0, 11.0, 17.0))
    monkeypatch.setattr(cutting_driver, "cutting_plane_loop", fake_loop)
    monkeypatch.setattr(cutting_driver.time, "perf_counter", lambda: next(wall))
    monkeypatch.setattr(cutting_driver.time, "process_time", lambda: next(cpu))
    summary = tmp_path / "timing-summary.json"
    code = main(
        [
            "--n",
            "5",
            "--side",
            "21/10",
            "--angle-limit",
            LIMIT,
            "--steps",
            "1",
            "--grids",
            "5",
            "--minutes",
            "1",
            "--iterations",
            "1",
            "--stop-on-covering-below-n",
            "--json",
            str(summary),
        ]
    )
    record = json.loads(summary.read_text())
    assert code == 0
    assert record["settings"]["stop_on_covering_below_n"] is True
    assert captured["stop_on_covering_below_n"] is True
    assert captured["deadline"] == 80.0
    assert record["seconds"] == 12.0
    assert record["timing"] == {
        "scope": (
            "main entry through measurement immediately before summary serialization; "
            "excludes import/interpreter/uv startup, final summary write, and teardown"
        ),
        "loop_wall_seconds": 12.0,
        "loop_cpu_seconds": 3.0,
        "driver_wall_seconds_before_summary": 35.0,
        "driver_cpu_seconds_before_summary": 12.0,
    }


def test_crossing_stop_emits_every_artifact_and_its_state_feeds_the_freeze_bridge(
    tmp_path: Path,
) -> None:
    log_path = tmp_path / "crossing.log"
    state_path = tmp_path / "crossing-state.json"
    summary_path = tmp_path / "crossing-summary.json"
    family_path = tmp_path / "crossing-family.json"
    code = main(
        [
            "--n", "5", "--side", "21/10", "--angle-limit", LIMIT, "--steps", "1",
            "--grids", "5", "--minutes", "1", "--iterations", "1", "--cap", "8",
            "--stop-on-covering-below-n", "--log", str(log_path),
            "--state", str(state_path), "--json", str(summary_path),
            "--freeze", str(family_path),
        ]
    )  # fmt: skip
    summary = json.loads(summary_path.read_text())
    state = json.loads(state_path.read_text())
    family = json.loads(family_path.read_text())
    reason = "row-converged covering objective below n at iteration 0"
    assert code == 0
    assert summary["stopped"] == state["stopped"] == reason
    assert summary["iterations"][0]["rows_converged"] is True
    assert summary["iterations"][0]["rows_objective"] < 5
    assert summary["iterations"][0]["added"] == 0
    assert family["provenance"]["stopped"] == reason
    assert reason in log_path.read_text()

    certificate, receipt = bridge(
        state_path,
        n=5,
        half_tangents=net_half_tangents(Fraction(LIMIT), 1),
    )
    assert certificate.total_mass < 5
    assert str(receipt["rows_stopped"]).startswith("converged")
