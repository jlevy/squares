#!/usr/bin/env python3
"""How near can a generic strategy get to each best-known packing below n = 100?

The whole-benchmark question. Every strategy here is a *family* -- the same phases and the
same settings for every `n` -- so a good column is evidence about the family rather than
about a value someone tuned. Where a strategy reads structure off a record, the rung it
used is reported beside its result, because a run told the answer's shape has to say so.

The targets are the 36 non-grid cases at `n <= 100`: the ones whose best known packing
beats the trivial `ceil(sqrt(n))` grid. The other 64 are already solved by the grid and
would flatter any column they appeared in.

Usage, from `packing/`:
    uv run --frozen python -m devtools.recover_records --max-n 30
    uv run --frozen python -m devtools.recover_records --max-n 100 --workers 8 --out runs.json
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import time
from pathlib import Path
from typing import Any

import numpy as np

from devtools.known_structure import record
from devtools.packing_strategy import run
from devtools.screen_jamming_targets import non_grid_cases


def families(budget: int) -> dict[str, list[dict[str, Any]]]:
    """The strategy families under test, each identical across every `n`.

    `bare` and `mixed` know nothing. `built` uses the record's face contacts to construct a
    start and then RELEASES them before tightening -- the squeeze measurement is why: holding
    the faces through the ratchet reached 4.0014 at `n = 11` against 3.9484 for the plain
    grid, because six of that record's fourteen contacts are corner-on-edge between squares
    40.2 degrees apart and no face structure can produce them.
    """
    return {
        "bare": [
            {"mechanism": "grid"},
            {
                "mechanism": "ratchet",
                "relaxation": 0.1,
                "until": {"steps": budget},
                "schedule": {"attempts": 5, "floor": 1e-3},
            },
        ],
        "mixed": [
            {"mechanism": "grid"},
            {
                "mechanism": "ratchet",
                "relaxation": 0.1,
                "until": {"steps": budget},
                "schedule": {"attempts": 6, "floor": 1e-3, "cold": 0.5},
            },
        ],
        "built": [
            {
                "mechanism": "assemble",
                "structure": {"rung": "contact-graph-with-types"},
                "side": {"relative_to": "record", "factor": 1.12},
            },
            {
                "mechanism": "project",
                "relaxation": 0.1,
                "constraints": {"band": 0.02, "weight": 2.0},
                "until": {"steps": budget},
            },
            {"mechanism": "relax", "relaxation": 0.1, "until": {"steps": budget // 2}},
            {
                "mechanism": "ratchet",
                "relaxation": 0.1,
                "until": {"steps": budget},
                "schedule": {"attempts": 5, "floor": 1e-3},
            },
        ],
    }


def _one(job: tuple[int, str, int, int]) -> dict[str, Any]:
    n, family, seed, budget = job
    phases = families(budget)[family]
    began = time.time()
    try:
        state = run({"name": family, "n": n, "seed": seed, "phases": phases})
        side = state.side
        rung = state.log[-1]["rung"]
        viol = float(state.log[-1]["violation"])
    except (ValueError, KeyError, AssertionError) as exc:
        return {"n": n, "family": family, "seed": seed, "error": str(exc)[:120]}
    known = record(n)[1]
    return {
        "n": n,
        "family": family,
        "seed": seed,
        "side": side,
        "excess_pct": 100.0 * (side - known) / known,
        "violation": viol,
        "rung": rung,
        "seconds": time.time() - began,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-n", type=int, default=30)
    ap.add_argument("--min-n", type=int, default=2)
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--budget", type=int, default=4000)
    ap.add_argument("--families", nargs="+", default=["bare", "mixed", "built"])
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--out", type=Path, default=None)
    o = ap.parse_args()

    targets = [n for n, *_ in non_grid_cases(o.max_n) if n >= o.min_n]
    jobs = [
        (n, family, 900 + 31 * k, o.budget)
        for n in targets
        for family in o.families
        for k in range(o.seeds)
    ]
    print(f"{len(targets)} non-grid cases, {len(jobs)} runs on {o.workers} workers", flush=True)
    began = time.time()
    with mp.Pool(o.workers) as pool:
        rows = list(pool.imap_unordered(_one, jobs))
    if o.out:
        o.out.write_text(json.dumps(rows, default=str), encoding="utf-8")

    good = [r for r in rows if "error" not in r and r["violation"] <= 1e-9]
    print(
        f"\n{len(good)} of {len(rows)} runs ended on a verified packing, "
        f"{time.time() - began:.0f}s"
    )
    header = f"{'n':>4} {'grid':>5} {'record':>11}"
    for family in o.families:
        header += f" {family:>16}"
    print(header)
    for n in targets:
        line = f"{n:>4} {int(np.ceil(np.sqrt(n))):>5} {record(n)[1]:>11.6f}"
        for family in o.families:
            sel = [r for r in good if r["n"] == n and r["family"] == family]
            line += f" {min(r['excess_pct'] for r in sel):>+15.3f}%" if sel else f" {'-':>16}"
        print(line)
    for family in o.families:
        sel = [r for r in good if r["family"] == family]
        if sel:
            best = {
                n: min(r["excess_pct"] for r in sel if r["n"] == n)
                for n in {r["n"] for r in sel}
            }
            print(
                f"{family}: median excess {np.median(list(best.values())):+.3f}%, "
                f"reached {len(best)} of {len(targets)} cases, "
                f"within 1% on {sum(1 for v in best.values() if v < 1.0)}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
