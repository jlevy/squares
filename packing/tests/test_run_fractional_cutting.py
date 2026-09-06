"""Controls for the cutting-plane driver's seed flag.

A warm start only moves to a larger side, so a fresh side below every retained
state -- the scalar probe at ``61/16`` that agenda-025 pre-registers -- has to
start from the grid. ``--seed-certificate`` lets it start from the grid plus a
retained certificate's atom sites, carried by the same maps the column
generator uses; the driver records what it seeded, and refuses the flag beside
``--warm``, where the state already carries the sites it earned.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools.run_fractional_colgen import seed_points_from
from devtools.run_fractional_cutting import main

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
