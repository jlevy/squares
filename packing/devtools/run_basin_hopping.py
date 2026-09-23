#!/usr/bin/env python3
"""Basin hopping over `quench_bracket`, budgeted in refined local optima.

    run_basin_hopping.py --cells 5,10,11 --seeds 1,2,3 --quenches 20 --out results/exp-204

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
import zlib
from pathlib import Path
from typing import Any

from sqpack.project import configured_project_root
from sqpack.research.descent_filter import (
    STROMQUIST_11_SIDE,
    DescentFilterConfig,
    DescentFilterResult,
    bounding_side,
    class_summary,
    descent_filter,
    exact_witness,
    min_pair_gap,
    rattling_squares,
    stromquist_11_pose,
)
from sqpack.research.quench import quench_bracket, solve_to_fixed_point
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


RNG_SEED_DERIVATION = "(seed << 20) ^ (n << 8) ^ (zlib.crc32(condition.encode()) % 251)"


def rng_seed(condition: str, n: int, seed: int) -> int:
    """The random stream's seed for one (condition, cell, seed), stable across processes.

    `hash(condition)` was used here once, and `str` hashing is salted per interpreter, so
    no recorded run could be re-seeded. CRC-32 is a fixed function of the bytes.
    """
    return (seed << 20) ^ (n << 8) ^ (zlib.crc32(condition.encode()) % 251)


def run_seed(
    condition: str, n: int, seed: int, *, quenches: int, budget: float, eps0: float
) -> dict[str, Any]:
    """One (condition, cell, seed): exactly `quenches` refined local optima."""
    rng = random.Random(rng_seed(condition, n, seed))
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
    # The census is a subcommand dispatched before the stock parser, so every existing
    # invocation parses exactly as it did.
    raw = sys.argv[1:] if argv is None else argv
    if raw and raw[0] == "census":
        return census_main(raw[1:])
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
        # A fixed seed fixes the proposals, not the refinements: a quench that reaches this
        # bound returns wherever it had got to, which depends on the host's load.
        "quench_bound": "wall clock, seconds per quench_bracket call",
        "eps0": options.eps0,
        "cells": cells,
        "seeds": seeds,
        "conditions": conditions,
        "rng_seed_derivation": RNG_SEED_DERIVATION,
        "rng_seeds": {
            condition: {
                str(n): {str(seed): rng_seed(condition, n, seed) for seed in seeds}
                for n in cells
            }
            for condition in conditions
        },
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


# --- Census mode (H-238) -------------------------------------------------------------
#
#   run_basin_hopping.py census --starts 1000 --out ../attic/census/run --stalls FILE
#
# Jolted starts about Trump's and Stromquist's n = 11 packings, each quenched by the stock
# `quench_bracket` and then passed through `sqpack.research.descent_filter`, which
# searches the full pose space for a verified side decrease. An endpoint the filter
# certifies a decrease from is rejected; the filter's terminal pose is recorded either
# way, and every descent-stable terminal carries an exact rational witness. The census
# refuses to run unless its controls pass first: Trump and Stromquist stable, two
# non-minimal Trump variants rejected, and every supplied stall rejected.

CENSUS_KILL_SIDE = 3.885618  # H-238's frozen threshold, just below 2 + 4 sqrt 2 / 3
CENSUS_CLASS_TOL = 1e-3  # orientation classes are counted at this angle tolerance
CENSUS_SIDE_TOL = 1e-9  # distinct minima are sides further apart than this


def trump_11_pose() -> tuple[list[float], list[float], list[float], float]:
    """Trump's packing rounded to floats: centres, angles, and its exact side as a float."""
    from cases.trump11.packing import build  # noqa: PLC0415 - case data, loaded on demand

    squares, side, field = build()
    field.refine_to(60)

    def value(element: Any) -> float:
        return float(field.decimal(element, 40))

    x = [sum(value(p[0]) for p in sq) / 4.0 for sq in squares]
    y = [sum(value(p[1]) for p in sq) / 4.0 for sq in squares]
    theta = [
        math.atan2(value(sq[1][1]) - value(sq[0][1]), value(sq[1][0]) - value(sq[0][0]))
        % QUARTER
        for sq in squares
    ]
    return x, y, theta, value(side)


def census_bases() -> dict[str, tuple[list[float], list[float], list[float]]]:
    """The two packings the census jolts about."""
    tx, ty, tt, _ = trump_11_pose()
    return {"trump": (tx, ty, tt), "stromquist": stromquist_11_pose()}


def _filter_config(seconds: float, seed: int) -> DescentFilterConfig:
    return DescentFilterConfig(time_budget=seconds, seed=seed)


def _control(
    name: str,
    pose: tuple[list[float], list[float], list[float]],
    reference: float | None,
    expect: str,
    seconds: float,
) -> dict[str, Any]:
    x, y, t = pose
    result = descent_filter(
        x, y, t, reference_side=reference, config=_filter_config(seconds, 0)
    )
    if expect == "stable":
        passed = result.status == "stable" and not result.rejected
    else:
        passed = result.rejected
    record = result.as_dict(with_pose=False)
    record.update(
        {
            "control": name,
            "expect": expect,
            "passed": passed,
            "terminal_classes": class_summary(result.theta, CENSUS_CLASS_TOL),
        }
    )
    print(
        f"control {name:24s} expect={expect:8s} passed={passed} status={result.status} "
        f"rejected={result.rejected} ref={result.reference_side:.12f} "
        f"terminal={result.terminal_side:.12f} {result.seconds:.1f}s",
        file=sys.stderr,
        flush=True,
    )
    return record


def census_controls(stalls: Path | None, seconds: float) -> list[dict[str, Any]]:
    """Run every control the frozen criterion names; the census needs all to pass."""
    tx, ty, tt, u_side = trump_11_pose()
    records = [
        _control("trump", (tx, ty, tt), u_side, "stable", seconds),
        _control("stromquist", stromquist_11_pose(), STROMQUIST_11_SIDE, "stable", seconds),
    ]
    # Trivially non-minimal: centres scaled apart, one square turned, side enlarged.
    cx, cy = sum(tx) / len(tx), sum(ty) / len(ty)
    nx = [cx + 1.002 * (v - cx) for v in tx]
    ny = [cy + 1.002 * (v - cy) for v in ty]
    nt = list(tt)
    nt[10] += 0.003
    if min_pair_gap(nx, ny, nt) <= 0.0:
        raise RuntimeError("nudged Trump control overlaps; the control is mis-built")
    records.append(
        _control("trump-nudged", (nx, ny, nt), bounding_side(nx, ny, nt), "reject", seconds)
    )
    # Non-minimal in the angles only: square 10 released by 0.02 rad, centres optimal.
    rt = list(tt)
    rt[10] += 0.02
    released = solve_to_fixed_point(rt, tx, ty, len(tx))
    records.append(
        _control(
            "trump-released-sq10",
            (list(released.x), list(released.y), rt),
            released.side,
            "reject",
            seconds,
        )
    )
    if stalls is not None:
        rows = [json.loads(line) for line in stalls.read_text().splitlines() if line.strip()]
        targets = [r for r in rows if 1e-9 < r["side"] - u_side < 0.006]
        records.extend(
            _control(
                f"stall {row['kind']} {row['detail']}",
                (row["x"], row["y"], row["theta"]),
                row["side"],
                "reject",
                seconds,
            )
            for row in targets
        )
    return records


def _census_task(task: dict[str, Any]) -> dict[str, Any]:
    """One start: jolt, quench, filter. Runs in a worker process."""
    started = time.time()
    rng = random.Random(task["rng_seed"])
    x0, y0, t0 = task["pose"]
    proposal = jolt((list(x0), list(y0), list(t0)), task["scale"], rng)
    quenched = quench_bracket(*proposal, time_budget=task["quench_seconds"])
    quench_seconds = time.time() - started
    record: dict[str, Any] = {
        "base": task["base"],
        "index": task["index"],
        "scale": task["scale"],
        "rng_seed": task["rng_seed"],
        "quench": {
            "side": quenched.side,
            "converged": quenched.converged,
            "reason": quenched.reason,
            "lp_solves": quenched.lp_solves,
            "seconds": round(quench_seconds, 3),
            "classes": class_summary(quenched.theta, CENSUS_CLASS_TOL),
            "x": list(quenched.x),
            "y": list(quenched.y),
            "theta": list(quenched.theta),
        },
    }
    if not math.isfinite(quenched.side):
        record["filter"] = None
        return record
    result: DescentFilterResult = descent_filter(
        quenched.x,
        quenched.y,
        quenched.theta,
        reference_side=quenched.side,
        config=_filter_config(task["filter_seconds"], task["rng_seed"]),
    )
    record["filter"] = result.as_dict(with_pose=True)
    record["filter"]["terminal_classes"] = class_summary(result.theta, CENSUS_CLASS_TOL)
    record["seconds"] = round(time.time() - started, 3)
    return record


def census_tasks(options: argparse.Namespace) -> list[dict[str, Any]]:
    """Interleaved over bases and cycling over scales, so any prefix is balanced."""
    bases = census_bases()
    names = options.bases.split(",")
    scales = [float(v) for v in options.scales.split(",")]
    per_base = options.starts // len(names)
    return [
        {
            "base": name,
            "index": index,
            "scale": scales[index % len(scales)],
            "rng_seed": zlib.crc32(f"{options.seed}:{name}:{index}".encode()),
            "pose": bases[name],
            "quench_seconds": options.quench_seconds,
            "filter_seconds": options.filter_seconds,
        }
        for index in range(per_base)
        for name in names
    ]


def _stable_terminals(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for record in records:
        result = record.get("filter")
        if not result or result["status"] != "stable":
            continue
        witness = result["terminal_witness"]
        if not witness or not witness["valid"]:
            continue
        out.append(record)
    return out


def census_minima(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Distinct descent-stable terminals: side within 1e-9, class count, multiplicities."""
    stable = sorted(_stable_terminals(records), key=lambda r: r["filter"]["terminal_side"])
    clusters: list[dict[str, Any]] = []
    for record in stable:
        result = record["filter"]
        classes = result["terminal_classes"]
        key = (classes["classes"], tuple(classes["multiplicities"]))
        for cluster in clusters:
            if (
                cluster["key"] == key
                and abs(result["terminal_side"] - cluster["side_max"]) <= CENSUS_SIDE_TOL
            ):
                cluster["members"].append(record)
                cluster["side_max"] = result["terminal_side"]
                break
        else:
            clusters.append(
                {"key": key, "side_max": result["terminal_side"], "members": [record]}
            )
    table = []
    for cluster in clusters:
        members = cluster["members"]
        rep = members[0]["filter"]
        free = rattling_squares(rep["x"], rep["y"], rep["theta"], rep["terminal_side"])
        fixed_theta = [t for k, t in enumerate(rep["theta"]) if k not in free]
        essential = class_summary(fixed_theta, CENSUS_CLASS_TOL) if fixed_theta else None
        table.append(
            {
                "side": rep["terminal_side"],
                "side_spread": cluster["side_max"] - rep["terminal_side"],
                "witness_side_min": min(
                    m["filter"]["terminal_witness"]["side"] for m in members
                ),
                "classes": cluster["key"][0],
                "multiplicities": list(cluster["key"][1]),
                "class_degrees": rep["terminal_classes"]["class_degrees"],
                "rattling_squares": free,
                "classes_without_rattlers": essential["classes"] if essential else 0,
                "count": len(members),
                "immediate_survivors": sum(1 for m in members if not m["filter"]["rejected"]),
                "after_certified_descent": sum(1 for m in members if m["filter"]["rejected"]),
                "bases": sorted({m["base"] for m in members}),
                "example": {"base": members[0]["base"], "index": members[0]["index"]},
            }
        )
    return table


def census_summary(
    records: list[dict[str, Any]], minima: list[dict[str, Any]]
) -> dict[str, Any]:
    """Counts, the minima table, and the frozen H-238 verdict."""
    filtered = [r for r in records if r.get("filter")]
    rejected = [r for r in filtered if r["filter"]["rejected"]]
    survivors = [
        r for r in filtered if not r["filter"]["rejected"] and r["filter"]["status"] == "stable"
    ]
    kills = [
        m for m in minima if m["classes"] >= 3 and m["witness_side_min"] < CENSUS_KILL_SIDE
    ]
    return {
        "starts": len(records),
        "by_base": {
            name: sum(1 for r in records if r["base"] == name)
            for name in sorted({r["base"] for r in records})
        },
        "quench_converged": sum(1 for r in records if r["quench"]["converged"]),
        "quench_endpoint_three_plus_classes_below_kill_side": sum(
            1
            for r in records
            if r["quench"]["classes"]["classes"] >= 3 and r["quench"]["side"] < CENSUS_KILL_SIDE
        ),
        "filtered": len(filtered),
        "descent_rejected": len(rejected),
        "survivors": len(survivors),
        "filter_budget_exhausted": sum(
            1 for r in filtered if r["filter"]["status"] == "budget"
        ),
        "stable_terminals": len(_stable_terminals(records)),
        "distinct_minima": len(minima),
        "kill_candidates": kills,
        "verdict": (
            "KILL: a descent-stable minimum with at least three classes below 3.885618"
            if kills
            else "SUPPORT ONLY: no descent-stable minimum with at least three classes "
            "below 3.885618 among the census terminals"
        ),
    }


def census_carried(path: Path | None, tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Records of an interrupted run, refused unless each matches one of these tasks.

    A record is matched on its base, index and random seed, so a file from a census with
    different arguments cannot be carried into this one. Records are carried unchanged;
    only the starts they do not cover are run again.
    """
    if path is None:
        return []
    planned = {(t["base"], t["index"]): t["rng_seed"] for t in tasks}
    carried = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        key = (record["base"], record["index"])
        if planned.get(key) != record["rng_seed"]:
            raise SystemExit(f"resume record {key} is not a task of this census")
        carried.append(record)
    if len({(r["base"], r["index"]) for r in carried}) != len(carried):
        raise SystemExit("resume file repeats a start")
    return carried


def census_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="run_basin_hopping.py census",
        description="H-238 census: jolted starts, stock quench, full-pose descent filter.",
    )
    parser.add_argument("--bases", default="trump,stromquist")
    parser.add_argument("--starts", type=int, default=1000, help="total starts over bases")
    parser.add_argument("--scales", default="0.02,0.05,0.1,0.2,0.3")
    parser.add_argument("--seed", type=int, default=238)
    parser.add_argument("--quench-seconds", type=float, default=8.0)
    parser.add_argument("--filter-seconds", type=float, default=60.0)
    parser.add_argument("--control-seconds", type=float, default=120.0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--wall-seconds", type=float, default=None, help="stop the census after this wall"
    )
    parser.add_argument("--stalls", type=Path, default=None, help="probe-C JSONL of stalls")
    parser.add_argument("--controls-only", action="store_true")
    parser.add_argument(
        "--resume-from",
        type=Path,
        default=None,
        help="census.jsonl of an interrupted run with these same arguments; its starts are "
        "carried into this run and skipped",
    )
    parser.add_argument("--out", type=Path, required=True)
    options = parser.parse_args(argv)
    out = options.out if options.out.is_absolute() else Path.cwd() / options.out
    out.mkdir(parents=True, exist_ok=True)
    started = time.time()
    meta: dict[str, Any] = {
        "argv": argv,
        "filter_config": _filter_config(options.filter_seconds, 0).as_dict(),
        "kill_side": CENSUS_KILL_SIDE,
        "class_tol": CENSUS_CLASS_TOL,
        "side_tol": CENSUS_SIDE_TOL,
        "host": {"platform": platform.platform(), "cpu_count": os.cpu_count()},
        "loadavg_before": os.getloadavg(),
    }
    controls = census_controls(options.stalls, options.control_seconds)
    (out / "controls.json").write_text(json.dumps(controls, indent=1) + "\n")
    failed = [c["control"] for c in controls if not c["passed"]]
    meta["controls_passed"] = not failed
    meta["controls_seconds"] = round(time.time() - started, 1)
    if failed or options.controls_only:
        (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
        print(json.dumps({"controls_failed": failed, "wrote": shown(out)}))
        return 1 if failed else 0

    import multiprocessing  # noqa: PLC0415 - only the census needs worker processes

    tasks = census_tasks(options)
    carried = census_carried(options.resume_from, tasks)
    done = {(r["base"], r["index"]) for r in carried}
    tasks = [t for t in tasks if (t["base"], t["index"]) not in done]
    meta["resumed_from"] = str(options.resume_from) if options.resume_from else None
    meta["carried_records"] = len(carried)
    records: list[dict[str, Any]] = list(carried)
    census_started = time.time()
    wall_stop = False
    with (out / "census.jsonl").open("w", encoding="utf-8") as handle:
        handle.writelines(json.dumps(r, sort_keys=True) + "\n" for r in carried)
        handle.flush()
        pool = multiprocessing.get_context("spawn").Pool(options.workers)
        try:
            for record in pool.imap_unordered(_census_task, tasks, chunksize=1):
                records.append(record)
                handle.write(json.dumps(record, sort_keys=True) + "\n")
                handle.flush()
                result = record.get("filter") or {}
                print(
                    f"[{len(records)}/{len(tasks)}] {record['base']:10s} "
                    f"scale={record['scale']:.2f} quench={record['quench']['side']:.9f} "
                    f"conv={record['quench']['converged']} "
                    f"rejected={result.get('rejected')} status={result.get('status')} "
                    f"terminal={result.get('terminal_side', float('nan')):.9f} "
                    f"classes={(result.get('terminal_classes') or {}).get('multiplicities')}",
                    file=sys.stderr,
                    flush=True,
                )
                if (
                    options.wall_seconds is not None
                    and time.time() - census_started > options.wall_seconds
                ):
                    wall_stop = True
                    break
        finally:
            pool.terminate()
            pool.join()
    minima = census_minima(records)
    summary = census_summary(records, minima)
    summary["wall_stop"] = wall_stop
    summary["tasks_planned"] = len(tasks)
    summary["census_seconds"] = round(time.time() - census_started, 1)
    meta["loadavg_after"] = os.getloadavg()
    meta["seconds"] = round(time.time() - started, 1)
    (out / "minima.json").write_text(json.dumps(minima, indent=1) + "\n")
    (out / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    kill_poses = []
    for record in _stable_terminals(records):
        result = record["filter"]
        classes = result["terminal_classes"]["classes"]
        if classes >= 3 and result["terminal_witness"]["side"] < CENSUS_KILL_SIDE:
            witness = exact_witness(result["x"], result["y"], result["theta"])
            kill_poses.append({**record, "exact_witness": witness.as_dict(with_pose=True)})
    if kill_poses:
        (out / "kill-candidates.jsonl").write_text(
            "".join(json.dumps(r, sort_keys=True) + "\n" for r in kill_poses)
        )
    print(json.dumps({"verdict": summary["verdict"], "wrote": shown(out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
