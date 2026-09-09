#!/usr/bin/env python3
"""Measure how often a proposal moves the objective at all.

    measure_objective_sparsity.py --cells 5,11,17,27,52 --scale 0.05 --samples 20000
    measure_objective_sparsity.py --archive results/exp-131/A-control.jsonl --scale 0.05

The 2026-09-08 annealing survey argues from the shape of the objective that a plain
annealer must stall: `required_side` is a max over the two to four squares attaining the
binding span, so most single-square translations leave it *exactly* unchanged and the
search walks a plateau bounded only by the overlap rejection. The survey lists this among
the things it could not establish -- "it predicts a specific plateau statistic that no
experiment here has yet measured".

This measures it. For a configuration, it draws proposals from the same two distributions
the engine draws from -- a single square translated or rotated, and every square displaced
at once -- and reports, for each:

* `changed`   -- the fraction that move `required_side` by more than 0 at all;
* `lowered`   -- the fraction that lower it, ignoring overlap;
* `admissible`-- the fraction that lower it *and* leave the packing overlap-free, which
  is the only kind of proposal the cold end of the anneal can accept.

Run it on the trivial grid (`--cells`) to see what the search is up against at its own
starting point, and on an archive of emitted poses (`--archive`) to see what it is up
against where the search actually stops. The two are different questions and the tool
answers both the same way.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path
from typing import Any

# Matches sqsearch's Params::default: a rotation step is this multiple of the
# translation step, so the two proposal kinds are drawn as the engine draws them.
MOVE_ROTATE = 2.0
P_ROTATE = 0.35


def half_extent(theta: float) -> float:
    """Half-width of a unit square's axis-aligned bounding box along either axis."""
    return 0.5 * (abs(math.cos(theta)) + abs(math.sin(theta)))


def required_side(x: list[float], y: list[float], t: list[float]) -> float:
    """The engine's objective, written the same way `geom::required_side` writes it."""
    ex = [half_extent(v) for v in t]
    lox = min(x[k] - ex[k] for k in range(len(x)))
    hix = max(x[k] + ex[k] for k in range(len(x)))
    loy = min(y[k] - ex[k] for k in range(len(y)))
    hiy = max(y[k] + ex[k] for k in range(len(y)))
    return max(hix - lox, hiy - loy)


def depth(pose_i: tuple[float, float, float], pose_j: tuple[float, float, float]) -> float:
    """Penetration depth of two unit squares by the separating-axis test."""
    xi, yi, ti = pose_i
    xj, yj, tj = pose_j
    ci, si, cj, sj = math.cos(ti), math.sin(ti), math.cos(tj), math.sin(tj)
    dx, dy = xi - xj, yi - yj
    h = 0.5 + 0.5 * (abs(ci * cj + si * sj) + abs(si * cj - ci * sj))
    gap = max(
        abs(dx * ci + dy * si) - h,
        abs(dy * ci - dx * si) - h,
        abs(dx * cj + dy * sj) - h,
        abs(dy * cj - dx * sj) - h,
    )
    return 0.0 if gap >= 0.0 else -gap


def local_overlap(
    x: list[float], y: list[float], t: list[float], k: int, pose: tuple[float, float, float]
) -> float:
    """Overlap of one square at a proposed pose against every other square."""
    px, py, pt = pose
    return sum(depth((px, py, pt), (x[j], y[j], t[j])) for j in range(len(x)) if j != k)


def total_overlap(x: list[float], y: list[float], t: list[float]) -> float:
    """Overlap over every unordered pair."""
    n = len(x)
    return sum(
        depth((x[i], y[i], t[i]), (x[j], y[j], t[j])) for i in range(n) for j in range(i + 1, n)
    )


def probe(
    x: list[float],
    y: list[float],
    t: list[float],
    *,
    scale: float,
    samples: int,
    rng: random.Random,
) -> dict[str, Any]:
    """Draw both proposal kinds and count what each does to the objective."""
    base_side = required_side(x, y, t)
    base_overlap = total_overlap(x, y, t)
    counts = {
        kind: {"changed": 0, "lowered": 0, "admissible": 0} for kind in ("single", "collective")
    }

    for _ in range(samples):
        k = rng.randrange(len(x))
        if rng.random() < P_ROTATE:
            pose = (x[k], y[k], t[k] + MOVE_ROTATE * scale * rng.uniform(-1.0, 1.0))
        else:
            pose = (
                x[k] + scale * rng.uniform(-1.0, 1.0),
                y[k] + scale * rng.uniform(-1.0, 1.0),
                t[k],
            )
        nx, ny, nt = list(x), list(y), list(t)
        nx[k], ny[k], nt[k] = pose
        side = required_side(nx, ny, nt)
        moved = base_overlap - local_overlap(x, y, t, k, (x[k], y[k], t[k]))
        overlap = moved + local_overlap(x, y, t, k, pose)
        row = counts["single"]
        if side != base_side:
            row["changed"] += 1
        if side < base_side:
            row["lowered"] += 1
            if overlap <= 1e-12:
                row["admissible"] += 1

    for _ in range(samples):
        nx = [v + scale * rng.uniform(-1.0, 1.0) for v in x]
        ny = [v + scale * rng.uniform(-1.0, 1.0) for v in y]
        nt = [v + MOVE_ROTATE * scale * rng.uniform(-1.0, 1.0) for v in t]
        side = required_side(nx, ny, nt)
        row = counts["collective"]
        if side != base_side:
            row["changed"] += 1
        if side < base_side:
            row["lowered"] += 1
            if total_overlap(nx, ny, nt) <= 1e-12:
                row["admissible"] += 1

    return {
        "n": len(x),
        "base_side": base_side,
        "base_overlap": base_overlap,
        "samples": samples,
        "scale": scale,
        "single": {k: v / samples for k, v in counts["single"].items()},
        "collective": {k: v / samples for k, v in counts["collective"].items()},
    }


def grid(n: int) -> tuple[list[float], list[float], list[float]]:
    """The trivial `ceil(sqrt(n))` grid, which every chain starts from."""
    m = math.ceil(math.sqrt(n))
    return (
        [(k % m) + 0.5 for k in range(n)],
        [(k // m) + 0.5 for k in range(n)],
        [0.0] * n,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", help="comma-separated n, probed at the trivial grid")
    parser.add_argument("--archive", type=Path, help="JSONL of emitted poses to probe")
    parser.add_argument("--scale", type=float, default=0.05, help="proposal magnitude")
    parser.add_argument("--samples", type=int, default=20000, help="proposals per kind")
    parser.add_argument("--seed", type=int, default=1)
    options = parser.parse_args(argv)
    if not options.cells and not options.archive:
        parser.error("give --cells, --archive, or both")

    rng = random.Random(options.seed)
    out: list[dict[str, Any]] = []
    if options.cells:
        for n in (int(v) for v in options.cells.split(",")):
            x, y, t = grid(n)
            row = probe(x, y, t, scale=options.scale, samples=options.samples, rng=rng)
            row["source"] = "trivial-grid"
            out.append(row)
    if options.archive:
        # One probe per (cell, seed), on that seed's BEST line. An archive carries one
        # line per chain, and probing whichever came first would measure a chain that
        # lost rather than the configuration the round scores.
        best: dict[tuple[int, int], dict[str, Any]] = {}
        for line in options.archive.read_text().splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            if "best_side" not in rec or rec.get("kind") == "summary":
                continue
            key = (int(rec["n"]), int(rec["seed"]))
            if key not in best or float(rec["best_side"]) < float(best[key]["best_side"]):
                best[key] = rec
        for rec in best.values():
            row = probe(
                rec["x"], rec["y"], rec["t"],
                scale=options.scale, samples=options.samples, rng=rng,
            )  # fmt: skip
            row["source"] = f"{options.archive.name} seed {rec['seed']}"
            out.append(row)

    print(
        f"{'source':<28} {'n':>4} {'side':>12} | "
        f"{'single chg':>10} {'lower':>8} {'admiss':>8} | "
        f"{'coll chg':>9} {'lower':>8} {'admiss':>8}",
        file=sys.stderr,
    )
    for row in out:
        print(
            f"{row['source'][:28]:<28} {row['n']:>4} {row['base_side']:>12.6f} | "
            f"{row['single']['changed']:>10.4f} {row['single']['lowered']:>8.4f} "
            f"{row['single']['admissible']:>8.4f} | "
            f"{row['collective']['changed']:>9.4f} {row['collective']['lowered']:>8.4f} "
            f"{row['collective']['admissible']:>8.4f}",
            file=sys.stderr,
        )
    print(json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
