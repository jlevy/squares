"""Basin hopping's random streams are a function of the run's declared inputs alone.

A seed derived from `hash(str)` changes with every interpreter, because string hashing is
salted per process, so a recorded per-seed range could never be re-run. These tests pin the
derivation to its inputs and the record to the derivation.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import zlib
from pathlib import Path
from typing import Any

import pytest

from devtools import run_basin_hopping

CONDITIONS = ("multistart", "basin-hop")
PROBE = """\
import json
from devtools.run_basin_hopping import rng_seed
conditions = ("multistart", "basin-hop")
print(json.dumps({
    "old": [(1 << 20) ^ (5 << 8) ^ hash(c) % 251 for c in conditions],
    "new": [rng_seed(c, 5, 1) for c in conditions],
}))
"""


def _under_hash_seed(value: str) -> dict[str, list[int]]:
    """Both derivations, computed in a fresh interpreter under one `PYTHONHASHSEED`."""
    done = subprocess.run(
        [sys.executable, "-c", PROBE],
        cwd=run_basin_hopping.ROOT,
        env=os.environ | {"PYTHONHASHSEED": value},
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(done.stdout)


def test_the_rng_seed_does_not_depend_on_the_interpreter_hash_seed() -> None:
    """The old derivation moves between interpreters; the recorded one does not."""
    zero, one = _under_hash_seed("0"), _under_hash_seed("1")
    assert zero["old"] != one["old"], "the control: hash() really is salted per process"
    assert zero["new"] == one["new"]
    assert zero["new"] == [
        (1 << 20) ^ (5 << 8) ^ (zlib.crc32(c.encode()) % 251) for c in CONDITIONS
    ]


def test_meta_records_every_derived_seed_and_the_wall_clock_bound(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`meta.json` carries what a replay needs: each stream's seed and the quench bound."""
    used: list[tuple[str, int, int, int]] = []

    def fake_run_seed(condition: str, n: int, seed: int, **_: Any) -> dict[str, Any]:
        used.append((condition, n, seed, run_basin_hopping.rng_seed(condition, n, seed)))
        return {"incumbent": None}

    monkeypatch.setattr(run_basin_hopping, "run_seed", fake_run_seed)
    status = run_basin_hopping.main(
        ["--cells", "4,5", "--seeds", "1,2", "--quenches", "1", "--quench-seconds", "2.5",
         "--out", str(tmp_path)]
    )  # fmt: skip
    meta = json.loads((tmp_path / "meta.json").read_text())

    assert status == 0
    assert meta["quench_seconds"] == 2.5
    assert "wall" in meta["quench_bound"]
    assert "zlib.crc32" in meta["rng_seed_derivation"]
    assert len(used) == 8
    for condition, n, seed, value in used:
        assert meta["rng_seeds"][condition][str(n)][str(seed)] == value
