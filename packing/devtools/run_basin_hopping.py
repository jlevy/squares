#!/usr/bin/env python3
"""Basin hopping over `quench_bracket`, budgeted in refined local optima.

    run_basin_hopping.py --cells 5,10,11 --seeds 1,2,3 --quenches 20 --out results/exp-133

This is Gensane and Ryckelynck's algorithm 4 with a stronger local solver substituted
for their layer 2: perturb every square at once, refine to a local optimum, accept only
on improvement, double the perturbation on success and halve it on failure, and restart
from a fresh scatter when it collapses. Their layer 2 is an adaptive-step greedy
billiard; the refiner here is the campaign's LP-in-cell quench, which is exact for fixed
angles and a fixed separating-axis assignment and brackets rather than descends over the
angle classes.

**The budget is refined local optima, not moves.** That is the unit Ellsworth's published
run statistics are denominated in -- 4 record basins in 3,004 classified refinements at
`n = 51` -- and a move budget is uninformative across proposers whose move costs differ
by orders of magnitude. Both conditions here get exactly the same number of quench calls.

Two conditions, so the arm has its own control:

* `multistart` -- every proposal is a fresh uniform scatter. Grosso and colleagues'
  measurement is that this is the wrong shape for packing: 50,000 local searches from
  random starts found roughly 16,000 *distinct* local minimisers by `n = 40`.
* `basin-hop` -- proposals perturb the incumbent refined optimum, with the adaptive
  step above. This is the condition the survey predicts should win.

**Nothing here reports a side it has not repaired and re-checked.** The quench solves an
LP, so its separations are non-negative only up to the solver's tolerance, and a pose
one part in `1e16` inside another is not a packing. Every refined pose is therefore
scaled apart about its own centre by the smallest factor that removes all penetration,
re-measured, and emitted only when `sqpack.verify` agrees it is valid. The reported side
is the side *after* that repair, so the repair can only ever cost the arm.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import random
import sys
import time
from pathlib import Path
from typing import Any

from sqpack.project import configured_project_root
from sqpack.research.quench import quench_bracket
from sqpack.verify import corners_from_poses, float_sign, verify_packing
from sqpack.yamlio import safe_load

ROOT = configured_project_root()
REPO = ROOT.parent


def shown(path: Path) -> str:
    """Repository-relative when it is inside the checkout, absolute otherwise."""
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


# The tolerance the campaign's independent pose oracle uses. Repairing to a margin
# above it is what makes the emitted packing survive that check rather than skirt it.
POSE_TOLERANCE = 1e-9
QUARTER = math.pi / 2


def _depth(pose_i: tuple[float, float, float], pose_j: tuple[float, float, float]) -> float:
    """Penetration depth of two unit squares: 0 when disjoint, positive when overlapping.

    The separating-axis test written in the same form the search engine uses, so the two
    agree about what a contact is. `sqpack.verify` is still what decides the emitted
    packing; this is the cheap inner predicate the repair loop bisects on.
    """
    xi, yi, ti = pose_i
    xj, yj, tj = pose_j
    ci, si, cj, sj = math.cos(ti), math.sin(ti), math.cos(tj), math.sin(tj)
    dx, dy = xi - xj, yi - yj
    half = 0.5 + 0.5 * (abs(ci * cj + si * sj) + abs(si * cj - ci * sj))
    gap = max(
        abs(dx * ci + dy * si) - half,
        abs(dy * ci - dx * si) - half,
        abs(dx * cj + dy * sj) - half,
        abs(dy * cj - dx * sj) - half,
    )
    return 0.0 if gap >= 0.0 else -gap


def total_depth(x: list[float], y: list[float], t: list[float]) -> float:
    """Total penetration over all pairs. Zero exactly when the configuration is valid."""
    n = len(x)
    return sum(
        _depth((x[i], y[i], t[i]), (x[j], y[j], t[j]))
        for i in range(n)
        for j in range(i + 1, n)
    )


def required_side(x: list[float], y: list[float], t: list[float]) -> float:
    """Side of the smallest axis-aligned square holding these poses."""
    squares = corners_from_poses(x, y, t)
    xs = [px for square in squares for px, _ in square]
    ys = [py for square in squares for _, py in square]
    return max(max(xs) - min(xs), max(ys) - min(ys))


def repair(x: list[float], y: list[float], t: list[float]) -> tuple[list[float], list[float]]:
    """Scale the centres apart about their own centroid until no pair penetrates.

    Scaling centres apart by a factor at least 1 strictly increases every centre
    distance and leaves every half-extent alone, so it increases every separating-axis
    gap. The smallest such factor is found by bisection. It can only enlarge the
    reported side, so a repaired candidate is never flattered by the repair.
    """
    if total_depth(x, y, t) == 0.0:
        return x, y
    cx, cy = sum(x) / len(x), sum(y) / len(y)

    def scaled(factor: float) -> tuple[list[float], list[float]]:
        return (
            [cx + factor * (v - cx) for v in x],
            [cy + factor * (v - cy) for v in y],
        )

    low, high = 1.0, 1.0 + 1e-6
    for _ in range(60):
        sx, sy = scaled(high)
        if total_depth(sx, sy, t) == 0.0:
            break
        high = 1.0 + (high - 1.0) * 4.0
        if high > 2.0:
            return scaled(high)
    for _ in range(80):
        mid = 0.5 * (low + high)
        sx, sy = scaled(mid)
        if total_depth(sx, sy, t) == 0.0:
            high = mid
        else:
            low = mid
    return scaled(high)


def scatter(n: int, rng: random.Random) -> tuple[list[float], list[float], list[float]]:
    """A fresh uniform proposal, in the box the trivial grid would need."""
    s0 = float(math.ceil(math.sqrt(n)))
    return (
        [rng.uniform(0.0, s0) for _ in range(n)],
        [rng.uniform(0.0, s0) for _ in range(n)],
        [rng.uniform(0.0, QUARTER) for _ in range(n)],
    )


def jolt(
    pose: tuple[list[float], list[float], list[float]], eps: float, rng: random.Random
) -> tuple[list[float], list[float], list[float]]:
    """Displace every square at once -- Gensane's layer 3, at magnitude `eps`."""
    x, y, t = pose
    return (
        [v + eps * rng.uniform(-1.0, 1.0) for v in x],
        [v + eps * rng.uniform(-1.0, 1.0) for v in y],
        [v + eps * rng.uniform(-1.0, 1.0) for v in t],
    )


def refine(
    proposal: tuple[list[float], list[float], list[float]], budget: float
) -> dict[str, Any] | None:
    """One refined local optimum: quench, repair, re-check. `None` if it is not valid."""
    x0, y0, t0 = proposal
    started = time.time()
    result = quench_bracket(list(x0), list(y0), list(t0), time_budget=budget)
    x, y, t = list(result.x), list(result.y), list(result.theta)
    x, y = repair(x, y, t)
    depth = total_depth(x, y, t)
    side = required_side(x, y, t)
    squares = corners_from_poses(x, y, t)
    xs = [px for square in squares for px, _ in square]
    ys = [py for square in squares for _, py in square]
    shifted = [[(px - min(xs), py - min(ys)) for px, py in square] for square in squares]
    report = verify_packing(shifted, side, sign=float_sign(POSE_TOLERANCE))
    if depth != 0.0 or not report.valid:
        return None
    return {
        "side": side,
        "x": x,
        "y": y,
        "t": t,
        "lp_solves": result.lp_solves,
        "converged": result.converged,
        "reason": result.reason,
        "quench_seconds": round(time.time() - started, 3),
    }


def run_seed(
    condition: str, n: int, seed: int, *, quenches: int, budget: float, eps0: float
) -> dict[str, Any]:
    """One (condition, cell, seed): exactly `quenches` refined local optima."""
    rng = random.Random((seed << 20) ^ (n << 8) ^ hash(condition) % 251)
    incumbent: dict[str, Any] | None = None
    eps = eps0
    accepted = invalid = restarts = 0
    trace: list[dict[str, Any]] = []
    started = time.time()

    for step in range(quenches):
        if condition == "multistart" or incumbent is None:
            proposal = scatter(n, rng)
        else:
            proposal = jolt((incumbent["x"], incumbent["y"], incumbent["t"]), eps, rng)
        refined = refine(proposal, budget)
        if refined is None:
            invalid += 1
            trace.append({"step": step, "eps": eps, "side": None})
            continue
        trace.append(
            {
                "step": step,
                "eps": eps,
                "side": refined["side"],
                "lp_solves": refined["lp_solves"],
                "seconds": refined["quench_seconds"],
            }
        )
        if incumbent is None or refined["side"] < incumbent["side"]:
            incumbent = refined
            accepted += 1
            eps = min(eps * 2.0, 1.0)
        elif condition == "basin-hop":
            eps *= 0.5
            if eps < 1e-6:
                # The step has collapsed: this funnel is exhausted, so start another.
                eps = eps0
                restarts += 1
        # `multistart` keeps the best it has seen and proposes independently of it.

    return {
        "condition": condition,
        "n": n,
        "seed": seed,
        "quenches": quenches,
        "refined_valid": quenches - invalid,
        "refined_invalid": invalid,
        "accepted": accepted,
        "restarts": restarts,
        "seconds": round(time.time() - started, 3),
        "incumbent": incumbent,
        "trace": trace,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", required=True, help="comma-separated n")
    parser.add_argument("--seeds", required=True, help="comma-separated seeds")
    parser.add_argument("--quenches", type=int, required=True, help="refined optima per seed")
    parser.add_argument(
        "--quench-seconds", type=float, default=5.0, help="per-quench wall bound"
    )
    parser.add_argument(
        "--eps0", type=float, default=0.1, help="initial perturbation magnitude"
    )
    parser.add_argument(
        "--conditions", default="multistart,basin-hop", help="comma-separated conditions"
    )
    parser.add_argument("--out", type=Path, required=True)
    options = parser.parse_args(argv)

    cells = [int(v) for v in options.cells.split(",")]
    seeds = [int(v) for v in options.seeds.split(",")]
    conditions = options.conditions.split(",")
    out = options.out if options.out.is_absolute() else ROOT / options.out
    out.mkdir(parents=True, exist_ok=True)

    meta = {
        "quenches_per_seed": options.quenches,
        "quench_seconds": options.quench_seconds,
        "eps0": options.eps0,
        "cells": cells,
        "seeds": seeds,
        "conditions": conditions,
        "host": {
            "platform": platform.platform(),
            "cpu_count": os.cpu_count(),
            "loadavg_before": os.getloadavg(),
        },
        "records": {},
    }
    for n in cells:
        path = ROOT / "frontier" / f"n-{n:03d}.md"
        case = safe_load(path.read_text().split("---\n")[1])["packing"]
        bound = case.get("reported_upper_bound") or case["upper_bound"]
        meta["records"][str(n)] = float(bound["value"])

    for condition in conditions:
        archive = out / f"D-{condition}.jsonl"
        detail = out / f"D-{condition}.trace.jsonl"
        with archive.open("w", encoding="utf-8") as handle, detail.open("w") as tracefile:
            for n in cells:
                for seed in seeds:
                    result = run_seed(
                        condition,
                        n,
                        seed,
                        quenches=options.quenches,
                        budget=options.quench_seconds,
                        eps0=options.eps0,
                    )
                    tracefile.write(json.dumps(result, sort_keys=True) + "\n")
                    best = result["incumbent"]
                    if best is None:
                        print(
                            f"{condition} n={n} seed={seed} NO VALID REFINEMENT",
                            file=sys.stderr,
                        )
                        continue
                    # The harness result-line contract: cell, seed, side, a zero overlap
                    # and the full pose, so an oracle that never saw this process can
                    # re-decide the geometry for itself.
                    handle.write(
                        json.dumps(
                            {
                                "kind": "basin-hop",
                                "condition": condition,
                                "n": n,
                                "seed": seed,
                                "best_side": best["side"],
                                "overlap": 0.0,
                                "quenches": result["quenches"],
                                "refined_valid": result["refined_valid"],
                                "accepted": result["accepted"],
                                "restarts": result["restarts"],
                                "seconds": result["seconds"],
                                "x": best["x"],
                                "y": best["y"],
                                "t": best["t"],
                            },
                            sort_keys=True,
                        )
                        + "\n"
                    )
                    # Flushed per (cell, seed): the archive is the only copy of the pose,
                    # and a run that dies with its poses in a buffer leaves numbers no
                    # oracle can re-check.
                    handle.flush()
                    tracefile.flush()
                    gap = best["side"] - meta["records"][str(n)]
                    print(
                        f"{condition} n={n} seed={seed} best={best['side']:.12f} "
                        f"gap={gap:+.3e} valid={result['refined_valid']}/{result['quenches']} "
                        f"{result['seconds']:.0f}s",
                        file=sys.stderr,
                    )
    meta["host"]["loadavg_after"] = os.getloadavg()
    (out / "meta.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"wrote": shown(out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
