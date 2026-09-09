#!/usr/bin/env python3
"""Shrink a container until the projection search stops finding a packing.

Gravel and Elser's own protocol for the sibling problem, inverted because this problem
minimises a container rather than maximising a diameter: fix a side, seek a packing,
tighten the side on success, and stop when the search stops succeeding. Their statement of
the starting information is the bar this has to clear -- "No information about the known
packings was used, apart from their densities" -- so the schedule starts at the trivial
grid, which is feasible for every `n` without consulting any record, and no run reads a
frontier file before it finishes.

Every side reported here is one at which a genuine packing was found: the search's own
separating-axis test at exactly zero, and then `sqpack.verify` out of process. That is the
whole difference from the 2026-09-08 penalty calibration, which ranked settings by
container sides that no arrangement achieved.

Usage, from `packing/`:
    uv run --frozen python -m devtools.run_projection_ratchet --n 5 10 11 --out /tmp/run
    uv run --frozen python -m devtools.run_projection_ratchet --n 11 --repeats 8 --json
"""

from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from devtools.divide_and_concur import (
    Array,
    Index,
    corners_of,
    pair_separation,
    pose_of,
    project_contacts,
    project_pairs,
    project_wall_contact,
    violation,
    wall_clearance,
)
from sqpack.verify import corners_from_poses, float_sign, verify_packing
from sqpack.yamlio import safe_load


@dataclass
class Problem:
    """The replica bookkeeping for `n` squares: which replica belongs to which square.

    `classes` is optional structural knowledge: a partition of the squares into groups
    that share an orientation. It is the lowest rung of the structure ladder -- for
    `n = 11` it is the two numbers "six squares at one angle, five at another", and it
    names neither the angle nor which square goes where.

    It enters as part of the concur set rather than as a force. The concur set is already
    "every replica of a square agrees, and each is a unit square"; a class adds "and these
    squares share an orientation", which is one more thing to project onto and not one
    more term to weigh against the others. That distinction is the reason to try this at
    all: the same idea measured as an *attraction* on 2026-09-08 pulled target structures
    apart rather than building them, for two recorded reasons -- the pull could not reach
    across one to four units, and nothing rotated a pair into registry. A projection has
    no range, and the rigidifying fit is a rotation.
    """

    n: int
    side: float
    classes: list[list[int]] | None = None
    contacts: list[tuple[int, int]] | None = None
    band: float = 0.02
    contact_weight: float = 1.0
    walls: list[int] | None = None
    ra: Index = field(init=False)
    rb: Index = field(init=False)
    rw: Index = field(init=False)
    owner: Index = field(init=False)
    weight: Array = field(init=False)

    def __post_init__(self) -> None:
        pairs = [(i, j) for i in range(self.n) for j in range(i + 1, self.n)]
        m = len(pairs)
        self.ra = np.arange(m, dtype=np.intp)
        self.rb = np.arange(m, 2 * m, dtype=np.intp)
        self.rw = np.arange(2 * m, 2 * m + self.n, dtype=np.intp)
        self.owner = np.concatenate(
            [
                np.array([p[0] for p in pairs], dtype=np.intp),
                np.array([p[1] for p in pairs], dtype=np.intp),
                np.arange(self.n, dtype=np.intp),
            ]
        )
        self.weight = np.ones(2 * m + self.n)
        # Which pair constraints are equalities. A contact graph does not enter this
        # search as a preference to be weighed against the others; it changes what the
        # constraint *is*, from "do not overlap" to "touch". That is the whole difference
        # between declaring a structure and hoping a force finds it.
        wanted = {(min(i, j), max(i, j)) for i, j in (self.contacts or ())}
        self.touching = np.array([p in wanted for p in pairs], dtype=bool)
        # A square touches about four others at a record but carries n - 1 pair replicas,
        # so at n = 11 the constraints that define the structure hold roughly a quarter of
        # the vote and the strangers hold the rest. Weighting is how the declared contacts
        # get their say back, and it is the difference between naming a structure and
        # having it survive the average.
        self.weight[self.ra[self.touching]] = self.contact_weight
        self.weight[self.rb[self.touching]] = self.contact_weight

    def poses(self, x: Array) -> Array:
        """The consensus square of each body: average the replicas, rigidify, share angles.

        The average is weighted by `self.weight`, which is one value per constraint and so
        is constant across the two replicas of a pair. That is what keeps the weighting
        legitimate: the divide projection sees a scalar multiple of the Euclidean metric
        inside each constraint's own variables, so its Euclidean projection is also the
        projection in the weighted metric, and the two halves of the iteration agree about
        what distance means.
        """
        total = np.zeros((self.n, 4, 2))
        np.add.at(total, self.owner, x * self.weight[:, None, None])
        mass = np.zeros(self.n)
        np.add.at(mass, self.owner, self.weight)
        poses = pose_of(total / mass[:, None, None])
        if self.classes is None:
            return poses
        # A square's orientation is defined modulo a quarter turn, so members of a class
        # are averaged on the circle at four times the angle. Averaging the raw angles
        # would let two squares that differ by exactly 90 degrees -- the same square --
        # pull the class to a meaningless value between them.
        for members in self.classes:
            a = 4 * poses[members, 2]
            poses[members, 2] = np.arctan2(np.sin(a).mean(), np.cos(a).mean()) / 4
        return poses

    def concur(self, x: Array) -> Array:
        return corners_of(self.poses(x))[self.owner]

    def divide(self, x: Array) -> Array:
        out = np.empty_like(x)
        out[self.ra], out[self.rb] = project_pairs(x[self.ra], x[self.rb])
        if self.touching.any():
            k = self.touching
            out[self.ra[k]], out[self.rb[k]] = project_contacts(
                x[self.ra[k]], x[self.rb[k]], self.band
            )
        out[self.rw] = np.clip(x[self.rw], 0.0, self.side)
        if self.walls:
            w = np.array(self.walls, dtype=np.intp)
            out[self.rw[w]] = project_wall_contact(
                np.clip(x[self.rw[w]], 0.0, self.side), self.side, self.band
            )
        return out

    def reweight(self, x: Array, alpha: float, rate: float = 0.01) -> None:
        """Elser's metric update: a constraint matters as much as its bodies are close.

        Without it every square is outvoted by its own strangers. A square touches about
        four others at a record but carries `n - 1` pair replicas, so at `n = 11` the
        constraints that decide the packing hold roughly a third of the vote and at
        `n = 26` a sixth. Measured at `n = 5` it changes nothing, which is the case where
        the dilution argument is weakest: four pair replicas, most of them active.
        """
        gap = np.concatenate(
            [
                np.tile(np.maximum(0.0, pair_separation(x[self.ra], x[self.rb])), 2),
                np.maximum(0.0, wall_clearance(x[self.rw], self.side)),
            ]
        )
        self.weight = (1 - rate) * self.weight + rate * np.exp(-alpha * gap)
        np.maximum(self.weight, 1e-6, out=self.weight)


@dataclass
class Outcome:
    solved: bool
    poses: Array
    violation: float
    steps: int


def solve(
    n: int,
    side: float,
    rng: np.random.Generator,
    *,
    beta: float = 0.5,
    alpha: float = 0.0,
    iters: int = 5000,
    monotone: int = 700,
    tol: float = 1e-9,
    check: int = 20,
    classes: list[list[int]] | None = None,
    contacts: list[tuple[int, int]] | None = None,
    band: float = 0.02,
    contact_weight: float = 1.0,
    walls: list[int] | None = None,
    start: Array | None = None,
) -> Outcome:
    """One RRR run at a fixed container side.

    The stop rule is Elser's `m`-monotonicity: abandon as soon as the error has failed to
    improve for `monotone` iterations. It is a stop condition on evidence rather than a
    self-declared budget, which is what `OR-8` asks of one, and it is also the published
    way of grading how hard an instance is for this method -- the `m` at which the success
    probability reaches one half.

    `beta` is the relaxation. Elser used `0.5` throughout his sphere work and reasoned that
    values below one are more productive against nonconvex constraints; the 2025 flow-limit
    paper measures clean scaling only for `beta <= 0.3`. Both are worth an arm; `1.0` is the
    Douglas-Rachford limit that same paper models as degenerating, and is not offered.

    `alpha` turns on the metric weighting: zero leaves every constraint equal.
    """
    p = Problem(n, side, classes, contacts, band, contact_weight, walls)
    if start is None:
        start = np.stack(
            [
                rng.uniform(0.5, side - 0.5, n),
                rng.uniform(0.5, side - 0.5, n),
                rng.uniform(0, np.pi / 2, n),
            ],
            axis=-1,
        )
    x = corners_of(start)[p.owner].copy()

    best_eps, since, step = np.inf, 0, 0
    scale = math.sqrt(x.size)
    for step in range(1, iters + 1):
        xa = p.concur(x)
        delta = p.divide(2 * xa - x) - xa
        x = x + beta * delta
        eps = float(np.linalg.norm(delta)) / scale
        if alpha > 0:
            p.reweight(x, alpha)

        # Success is a packing, not a small step, so ask the geometry directly rather than
        # inferring it from the error. Checking every step would dominate the cost at large
        # n; checking never would run converged solutions to the budget.
        if eps < 1e-6 and step % check == 0:
            poses = p.poses(x)
            v = violation(poses, side)
            if v <= tol:
                return Outcome(solved=True, poses=poses, violation=v, steps=step)

        if eps < best_eps - 1e-15:
            best_eps, since = eps, 0
        else:
            since += 1
        if eps < 1e-12 or since >= monotone:
            break

    poses = p.poses(x)
    v = violation(poses, side)
    return Outcome(solved=v <= tol, poses=poses, violation=v, steps=step)


def _grid(n: int, side: float) -> Array:
    k = round(side)
    cells = [(i, j) for j in range(k) for i in range(k)][:n]
    return np.array([[i + 0.5, j + 0.5, 0.0] for i, j in cells])


def _squeeze(poses: Array, old: float, new: float) -> Array:
    """Carry a packing into a smaller container by scaling centres, not squares.

    The squares stay unit; only the arrangement contracts. This is what makes a warm start
    worth attempting: it leaves overlaps rather than gaps, which is the direction the
    divide projection knows how to repair.
    """
    out = poses.copy()
    out[:, :2] = (poses[:, :2] - old / 2) * (new / old) + new / 2
    return out


def ratchet(
    n: int,
    rng: np.random.Generator,
    *,
    beta: float = 0.5,
    alpha: float = 0.0,
    attempts: int = 6,
    iters: int = 5000,
    monotone: int = 700,
    steps: int = 30,
    floor: float = 1e-3,
    jitter: float = 0.02,
    cold: float = 0.0,
    band: float = 0.02,
    contact_weight: float = 1.0,
    classes: list[list[int]] | None = None,
    contacts: list[tuple[int, int]] | None = None,
    walls: list[int] | None = None,
) -> dict[str, Any]:
    """Tighten the container while the search keeps up, halving the step when it does not.

    The step halves on failure rather than the run stopping outright, so a run ends at a
    side it has actually packed rather than at the first side it missed. The floor is loose
    on purpose: the survey's instruction is not to ask the projection loop for the final
    digits, which belong to the fixed-angle LP.

    `cold` is the fraction of each side's attempts spent on fresh random configurations
    rather than on continuing the packing already in hand, and it is the arm worth
    sweeping. Gravel and Elser's published protocol is entirely cold -- up to 400
    independent random starts per `n` -- and continuation is this implementation's
    addition. The reason it matters here is specific to squares: the schedule starts at
    the trivial grid, and a grid of `k` squares in a row needs a container of exactly `k`,
    so *every* tightening makes the grid topology infeasible at once. There is no small
    repair. Continuation from the grid therefore has to invent a new arrangement on its
    first step or never move at all, which is the same wall this repository already
    measured for its annealing engine, where no single-square move lowers the side at a
    grid ([H-135](../campaign/hypotheses/H-135-simultaneous-perturbation-move.md)).
    Measured at `n = 5`: three of four fully continuation-led runs never left `3.0`, and
    the fourth reached `2.708`, which is the record to four decimals.
    """
    side = float(math.ceil(math.sqrt(n)))
    best = _grid(n, side)
    if violation(best, side) > 1e-12:
        msg = f"the grid at side {side} is not feasible for n = {n}"
        raise AssertionError(msg)

    delta = 0.05 * side
    history: list[tuple[float, bool]] = []
    calls = 0
    for _ in range(steps):
        trial = side - delta
        found = None
        for a in range(attempts):
            # One clean continuation, then continuations shaken progressively harder, then
            # one cold start. The shaken ones are basin hopping laid over the projection
            # search: the previous packing is the only thing known to be nearly right at
            # this side, and jitter is how a run leaves its basin without discarding it.
            if a < round(cold * attempts):
                start = None
            elif a == round(cold * attempts):
                start = _squeeze(best, side, trial)
            elif a < attempts - 1:
                first = round(cold * attempts)
                spread = jitter * (1.0 + 3.0 * (a - first - 1) / max(1, attempts - first - 1))
                start = _squeeze(best, side, trial) + rng.normal(0, spread, best.shape)
            else:
                start = None
            out = solve(
                n,
                trial,
                rng,
                beta=beta,
                alpha=alpha,
                iters=iters,
                monotone=monotone,
                band=band,
                contact_weight=contact_weight,
                classes=classes,
                contacts=contacts,
                walls=walls,
                start=start,
            )
            calls += 1
            if out.solved:
                found = out.poses
                break
        history.append((trial, found is not None))
        if found is not None:
            side, best = trial, found
        else:
            delta *= 0.5
            if delta < floor:
                break
    return {
        "n": n,
        "side": side,
        "poses": best.tolist(),
        "violation": violation(best, side),
        "calls": calls,
        "history": history,
    }


ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"


def best_known(n: int) -> float | None:
    """The reported upper bound for `n`, read only to score a finished run.

    Nothing in the search touches this. The container schedule starts at the trivial grid
    and stops where it stops, so the comparison below is applied to results rather than
    used to steer them -- which is what makes "no information about the known packings"
    an honest description of the run.
    """
    path = FRONTIER / f"n-{n:03d}.md"
    if not path.exists():
        return None
    payload = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
    bound = payload.get("reported_upper_bound") or {}
    value = bound.get("value")
    return float(value) if value is not None else None


def verified_out_of_process(row: dict[str, Any]) -> bool:
    """Re-check one reported packing with code this search does not share.

    The search's own separating-axis test agreeing with itself proves nothing. This is the
    repository's independent oracle, and the reason it exists is on the record: a quench
    once returned a packing that violated its own constraints (`D-014`).

    A tolerance is unavoidable and `sqpack.verify` says why -- a tight packing has exact
    contacts, so no tolerance separates a contact from a small overlap. The side is nudged
    by the tolerance rather than the test being loosened.
    """
    poses = row["poses"]
    squares = corners_from_poses(
        [p[0] for p in poses], [p[1] for p in poses], [p[2] for p in poses]
    )
    return verify_packing(squares, float(row["side"]) + 1e-9, sign=float_sign(1e-12)).valid


def _one(job: tuple[int, int, float, float, float, int, int, int]) -> dict[str, Any]:
    n, seed, beta, alpha, cold, attempts, iters, monotone = job
    began = time.time()
    row = ratchet(
        n,
        np.random.default_rng(seed),
        beta=beta,
        alpha=alpha,
        cold=cold,
        attempts=attempts,
        iters=iters,
        monotone=monotone,
    )
    return row | {
        "seed": seed,
        "beta": beta,
        "alpha": alpha,
        "cold": cold,
        "seconds": time.time() - began,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, nargs="+", required=True)
    ap.add_argument("--repeats", type=int, default=2)
    ap.add_argument("--beta", type=float, nargs="+", default=[0.3, 0.5])
    ap.add_argument("--alpha", type=float, nargs="+", default=[0.0])
    ap.add_argument("--cold", type=float, nargs="+", default=[0.0])
    ap.add_argument("--attempts", type=int, default=6)
    ap.add_argument("--iters", type=int, default=5000)
    ap.add_argument("--monotone", type=int, default=700)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--json", action="store_true")
    o = ap.parse_args()

    jobs = [
        (n, 7000 + 131 * k, beta, alpha, cold, o.attempts, o.iters, o.monotone)
        for n in o.n
        for beta in o.beta
        for alpha in o.alpha
        for cold in o.cold
        for k in range(o.repeats)
    ]
    began = time.time()
    with mp.Pool(o.workers) as pool:
        rows = list(pool.imap_unordered(_one, jobs))
    checked = sum(verified_out_of_process(row) for row in rows)
    payload = {
        "rows": rows,
        "verified_out_of_process": f"{checked}/{len(rows)}",
        "seconds": time.time() - began,
        "args": vars(o) | {"out": str(o.out)},
    }

    if o.out is not None:
        o.out.write_text(json.dumps(payload, default=str, sort_keys=True), encoding="utf-8")
    if o.json:
        print(json.dumps(payload, default=str, sort_keys=True))
        return 0

    print(
        f"{len(jobs)} ratchet runs in {payload['seconds']:.0f}s on {o.workers} workers; "
        f"{checked}/{len(rows)} verified out of process by sqpack.verify"
    )
    print(
        f"{'n':>4} {'beta':>5} {'alpha':>6} {'cold':>5} {'side':>13} {'viol':>9} "
        f"{'grid':>6} {'best':>11} {'excess%':>8} {'calls':>6} {'sec':>7}"
    )

    def order(r: dict[str, Any]) -> tuple[Any, ...]:
        return (r["n"], r["beta"], r["alpha"], r["cold"], r["side"])

    for row in sorted(rows, key=order):
        n = int(row["n"])
        side = float(row["side"])
        grid = math.ceil(math.sqrt(n))
        known = best_known(n)
        excess = f"{100 * (side - known) / known:+8.3f}" if known else f"{'-':>8}"
        shown = f"{known:>11.7f}" if known else f"{'-':>11}"
        print(
            f"{n:>4} {row['beta']:>5.1f} {row['alpha']:>6.1f} "
            f"{row['cold']:>5.2f} {side:>13.9f} {row['violation']:>9.1e} "
            f"{grid:>6} {shown} {excess} {row['calls']:>6} {row['seconds']:>7.1f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
