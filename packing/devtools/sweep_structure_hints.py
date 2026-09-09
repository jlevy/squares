#!/usr/bin/env python3
"""How much structure does a projection search need before it finds a known packing?

The ladder experiment. Handing a search the full contact structure of a record is copying
the answer -- realising it is then a linear program -- so the question worth asking is how
little suffices, and the amount given is the independent variable.

Two controls make the answer mean something.

- **Rewired graphs.** A search given the record's own graph is told the answer's shape; one
  given a graph of the same size with some edges replaced by pairs that do *not* touch at
  the record is told a lie of the same length. If both do equally well, the constraint
  count helped and the structure carried nothing.
- **Thinned graphs.** A random subset of the true edges says how much of the structure is
  load-bearing, rather than only whether all of it is.

Every hint is a constraint, never a force, and every one is a band rather than an equality.
That is not a detail. Declared as exact equalities the record becomes a *repelling* fixed
point of the iteration: started from Trump's exact `n = 11` packing with its own fourteen
contacts declared, the run drifts 0.0000 at 200 steps, 0.0012 at 1,000 and 0.2839 at 4,000,
with the violation growing from `1e-8` to `0.12`, deterministically and at every relaxation
above `0.1`. Exact tangency makes the constraint sets meet non-transversally, which is the
degenerate case the 2025 flow-limit paper excludes from its convergence results.

Usage, from `packing/`:
    uv run --frozen python -m devtools.sweep_structure_hints --n 11 --weights 1 2 4 8
    uv run --frozen python -m devtools.sweep_structure_hints --n 11 17 --seeds 12
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import time
from pathlib import Path
from typing import Any

import numpy as np

from devtools.divide_and_concur import corners_of, pair_separation, wall_clearance
from devtools.known_structure import (
    angle_classes,
    contact_edges,
    contact_kinds,
    record,
    rewired,
    thinned,
    wall_contacts,
)
from devtools.run_projection_ratchet import ratchet


def orientation_classes(edges: list[tuple[int, int]], kinds: dict, n: int) -> list[list[int]]:
    """Squares an edge-edge contact forces into a shared orientation.

    Derived from the contact *kinds*, not given. Saying "this contact is face to face"
    fixes the two squares' relative orientation to a multiple of a quarter turn without
    naming any angle, so the connected components of the edge-edge subgraph are orientation
    classes that fall out of the structure rather than being read off the answer. Corner
    contacts join nothing, which is what keeps the hint loose where the record is loose.
    """
    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i, j in edges:
        if kinds.get((i, j)) == "edge-edge":
            parent[find(i)] = find(j)
    groups: dict[int, list[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return [g for g in groups.values() if len(g) > 1]


LADDER = [
    (0, "nothing"),
    (1, "partition"),
    (2, "contact graph"),
    (3, "contact graph + types"),
    (4, "+ geometric constraints"),
    (5, "+ memory"),
]
"""The rungs, in order of how much they say about the configuration.

Each rung is strictly more informative than the one below, and the experiment is which is
the *lowest* one that suffices -- because the top of the ladder is the answer itself, and
realising a full contact structure is a linear program rather than a search.

- **0 nothing.** A cold random start, which is what the 2026-09-09 runs used.
- **1 partition.** Which squares share an orientation, as sizes only: for `n = 11` the two
  numbers "six and five", naming neither the angle nor which square.
- **2 contact graph.** Which pairs touch. Says nothing about how.
- **3 contact graph with types.** Which of those contacts are face to face. An edge-edge
  contact pins the pair's relative orientation to a quarter turn without naming an angle,
  so the orientation classes are *derived* from the structure rather than read off the
  record. A corner contact joins nothing, which keeps the hint loose where the record is.
- **4 additional geometric constraints.** Which squares lie against the container. At
  `n = 11` that is the other 20 of the record's 34 incidences, and their absence is the
  standing explanation for a realised graph that is still not a packing.
- **5 additional memory constraints.** Repulsion from local optima already visited, so a
  run is pushed out of basins it has explored. Not built; tracked as `think-dh4k`. This is
  metadynamics, and naming it that is what connects it to a literature the two surveys
  here did not cover.

Controls sit beside the rungs rather than under them: a *rewired* graph is the same size as
the true one with edges moved to pairs that do not touch, and a *thinned* one is a random
subset. Without them a result says only that constraints help, not that the structure did.
"""


def hints(n: int, seed: int) -> list[tuple[str, dict[str, Any]]]:
    """One entry per rung, plus the controls that make the rungs mean something."""
    poses, side = record(n)
    edges = contact_edges(poses)
    kinds = contact_kinds(poses)
    rng = np.random.default_rng(seed)
    m = len(edges)
    faces = sum(1 for e in edges if kinds.get(e) == "edge-edge")
    classes = orientation_classes(edges, kinds, n)
    return [
        ("0 nothing", {}),
        ("1 partition (angle classes)", {"classes": angle_classes(poses)}),
        (f"2 graph: {m // 4} of {m}", {"contacts": thinned(edges, m // 4, rng)}),
        (f"2 graph: {m // 2} of {m}", {"contacts": thinned(edges, m // 2, rng)}),
        (f"2 graph: all {m}", {"contacts": edges}),
        (f"2 control: rewired {m // 4}", {"contacts": rewired(edges, n, m // 4, rng)}),
        (f"2 control: rewired all {m}", {"contacts": rewired(edges, n, m, rng)}),
        (f"3 graph + types ({faces} face)", {"contacts": edges, "classes": classes}),
        (f"3 types only ({faces} face)", {"classes": classes}),
        (
            f"4 + walls ({len(wall_contacts(poses, side))} on wall)",
            {"contacts": edges, "classes": classes, "walls": wall_contacts(poses, side)},
        ),
    ]


def _one(job: tuple[int, str, dict[str, Any], float, int, float, float, int]) -> dict[str, Any]:
    n, name, hint, weight, seed, side, band, iters = job
    poses, _ = record(n)
    truth = contact_edges(poses)
    ia = np.array([e[0] for e in truth])
    ib = np.array([e[1] for e in truth])
    # The ratchet rather than a single side, because the question is how CLOSE a rung
    # gets, not whether it happens to hit one number. A rung that cannot reach the record
    # but reliably beats the grid is saying something, and a binary test would discard it.
    row = ratchet(
        n,
        np.random.default_rng(seed),
        beta=0.1,
        iters=iters,
        monotone=iters // 4,
        attempts=4,
        band=band,
        contact_weight=weight,
        **hint,
    )
    poses_out = np.array(row["poses"])
    v = corners_of(poses_out)
    ja, jb = np.triu_indices(n, 1)
    return {
        "n": n,
        "hint": name,
        "weight": weight,
        "seed": seed,
        "side": float(row["side"]),
        "excess_pct": 100.0 * (float(row["side"]) - side) / side,
        "violation": float(row["violation"]),
        "worst_pair": float(-pair_separation(v[ja], v[jb]).min()),
        "worst_wall": float(-wall_clearance(v, side).min()),
        "true_edges_realised": int((np.abs(pair_separation(v[ia], v[ib])) < 0.03).sum()),
        "true_edges": len(truth),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, nargs="+", required=True)
    ap.add_argument("--weights", type=float, nargs="+", default=[1.0, 2.0, 4.0, 8.0])
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--band", type=float, default=0.02)
    ap.add_argument("--iters", type=int, default=20000)
    ap.add_argument("--slack", type=float, default=1.000000001)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", type=Path, default=None)
    o = ap.parse_args()

    jobs = [
        (n, name, hint, weight, 4000 + 97 * k, record(n)[1], o.band, o.iters)
        for n in o.n
        for name, hint in hints(n, 17)
        for weight in o.weights
        for k in range(o.seeds)
    ]
    began = time.time()
    with mp.Pool(o.workers) as pool:
        rows = list(pool.imap_unordered(_one, jobs))
    if o.out:
        o.out.write_text(json.dumps(rows, default=str), encoding="utf-8")

    print(f"{len(jobs)} ratchet runs in {time.time() - began:.0f}s, beta 0.1, band {o.band}")
    print(
        f"{'n':>3} {'rung':>30} {'w':>3} {'best side':>12} {'excess%':>9} "
        f"{'median%':>9} {'true edges':>11}"
    )
    for n in o.n:
        for name, _ in hints(n, 17):
            for weight in o.weights:
                sel = [
                    r
                    for r in rows
                    if r["n"] == n and r["hint"] == name and r["weight"] == weight
                ]
                if not sel:
                    continue
                ed = int(np.median([r["true_edges_realised"] for r in sel]))
                best = min(r["side"] for r in sel)
                bx = min(r["excess_pct"] for r in sel)
                mx = float(np.median([r["excess_pct"] for r in sel]))
                print(
                    f"{n:>3} {name:>30} {weight:>3.0f} {best:>12.7f} {bx:>+9.3f} "
                    f"{mx:>+9.3f} {ed:>5} of {sel[0]['true_edges']:<3}"
                )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
