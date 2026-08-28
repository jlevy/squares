#!/usr/bin/env python3
"""The soundness perimeter: every component that emits a packing, checked by the oracle.

Defect D-014 -- an LP that returned a configuration violating its own separation
constraint, and so a claimed side below the standing record -- was possible because of
a gap in coverage, not a gap in care. `sqsearch` was differential-tested against
`sqpack`; the quench was checked only against *its own* constraint rows, which is no
check at all when the constraint rows are what the solver got wrong.

The rule this file enforces:

    Every component that can emit a configuration is checked by sqpack, through code
    it does not share, before any number derived from it is recorded.

Tolerance is chosen, not inherited. HiGHS guarantees primal feasibility only to 1e-10,
so a valid solve may sit 1e-10 inside a constraint and the oracle must accept that. It
must reject anything worse -- D-014's violation was 9.9e-08, three orders above the
floor, and would have been caught here on its first appearance.

Usage: uv run --frozen python -m devtools.check_soundness_perimeter
"""

from __future__ import annotations

import json
import math
import random
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from sqpack.research.quench import quench, quench_bracket, solve_to_fixed_point
from sqpack.verify import corners_from_poses, float_sign, verify_packing
from sqpack.workers import worker_count

ROOT = Path(__file__).resolve().parent.parent
# The tightest bound the solver's own guarantee permits. Anything looser would let a
# D-014 through; anything tighter would reject solves that are correct by construction.
ORACLE_TOL = 1e-10
BIN = ROOT / "sqsearch/target/release/sqsearch"


def normalize(x, y, theta):
    """Translate a packing so its bounding box starts at the origin.

    The search minimises the ENCLOSING side and never fixes a container, so its output
    sits wherever the chains left it in the plane. Checking containment in [0, s]^2
    without this measures the drift, not the packing -- which is what the first version
    of this file did, and it reported the engine as breaching the perimeter when the
    fault was here.
    """
    half = [0.5 * (abs(math.cos(t)) + abs(math.sin(t))) for t in theta]
    lox = min(a - h for a, h in zip(x, half, strict=True))
    loy = min(b - h for b, h in zip(y, half, strict=True))
    return [a - lox for a in x], [b - loy for b in y]


def oracle(x, y, theta, side, label: str) -> list[str]:
    """Check one configuration against sqpack. Returns failure descriptions."""
    x, y = normalize(x, y, theta)
    report = verify_packing(corners_from_poses(x, y, theta), side, sign=float_sign(ORACLE_TOL))
    if report.valid:
        return []
    return [f"{label}: {kind} — {msg}" for kind, msg in report.failures[:4]]


def enclosing_side(x, y, theta) -> float:
    half = [0.5 * (abs(math.cos(t)) + abs(math.sin(t))) for t in theta]
    return max(
        max(a + h for a, h in zip(x, half, strict=True))
        - min(a - h for a, h in zip(x, half, strict=True)),
        max(b + h for b, h in zip(y, half, strict=True))
        - min(b - h for b, h in zip(y, half, strict=True)),
    )


def anneal(n: int, seed: int) -> dict:
    out = subprocess.run(
        [
            str(BIN),
            "--n",
            str(n),
            "--seed",
            str(seed),
            "--chains",
            "4",
            "--budget-moves",
            "4000000",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    best = None
    for line in out.splitlines():
        d = json.loads(line)
        if d.get("kind") == "chain" and (best is None or d["best_side"] < best["best_side"]):
            best = d
    if best is None:
        msg = f"sqsearch produced no chain records for n={n}, seed={seed}"
        raise RuntimeError(msg)
    return best


def _quench_unit(
    unit: tuple[str, float, int, list[float], list[float], list[float]],
) -> tuple[list[str], int]:
    """Run one quench variant on one perturbed configuration and check it with sqpack.

    A module-level function taking a plain tuple, because that is what a process pool
    can pickle. Returns (failures, checked) so the parent does the accounting.
    """
    kind, eps, trial, x, y, t = unit
    label = f"{kind} eps={eps:g} #{trial}"

    if kind == "solve_to_fixed_point":
        got = solve_to_fixed_point(t, x, y, len(x))
        if not got:
            return [], 0
        return oracle(got.x, got.y, t, got.side + ORACLE_TOL, label), 1

    fn = quench if kind == "quench" else quench_bracket
    r = fn(x, y, t)
    if not math.isfinite(r.side):
        return [], 0
    failures = oracle(r.x, r.y, r.theta, r.side + ORACLE_TOL, label)
    # The side a component reports must also be a side the packing fits in: a claim
    # about `s` is as much a claim as a claim about validity.
    actual = enclosing_side(r.x, r.y, r.theta)
    if actual > r.side + ORACLE_TOL:
        failures.append(
            f"{label}: reports side {r.side:.15f} but its packing needs {actual:.15f}"
        )
    return failures, 1


def main() -> int:
    failures: list[str] = []
    checked = 0
    seed_cfg = json.loads(
        subprocess.run(
            [sys.executable, "-m", "cases.trump11.export_seed"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )

    # 1. The reference packing itself. If the oracle rejects this, the oracle is wrong
    #    and nothing below it means anything.
    errs = oracle(
        seed_cfg["x"], seed_cfg["y"], seed_cfg["t"], seed_cfg["side"], "reference trump11"
    )
    failures += errs
    checked += 1

    # 2. sqsearch: the packing it reports, not merely its pair energy.
    if BIN.exists():
        for n in (5, 10, 11):
            best = anneal(n, 1)
            failures += oracle(
                best["x"],
                best["y"],
                best["t"],
                best["best_side"] + ORACLE_TOL,
                f"sqsearch n={n}",
            )
            checked += 1
    else:
        print("  sqsearch binary absent, skipping engine cells", file=sys.stderr)

    # 3. The quench, from perturbed starts -- the component that produced D-014, and
    #    the one that had no independent check at all.
    #
    # The eighteen units below are independent by construction, and each is ~1.5s of
    # LP solving, which made this file the gate's critical path at ~35s. They now run
    # in a process pool.
    #
    # The perturbations are drawn HERE, serially, in the original order, and only the
    # finished configurations are handed to the workers. Drawing them inside the
    # workers would make the inputs depend on scheduling, which is the one thing a
    # soundness check must never do -- the whole point of `random.Random(11)` is that
    # this file checks the same eighteen configurations on every run, so a breach is
    # reproducible from the seed alone. Verified: the unit labels and the `checked`
    # count are identical to the serial version.
    rnd = random.Random(11)
    units: list[tuple[str, float, int, list[float], list[float], list[float]]] = []
    for eps in (1e-5, 1e-3, 1e-2):
        for trial in range(2):
            x = [v + eps * rnd.uniform(-1, 1) for v in seed_cfg["x"]]
            y = [v + eps * rnd.uniform(-1, 1) for v in seed_cfg["y"]]
            t = [v + eps * rnd.uniform(-1, 1) for v in seed_cfg["t"]]
            units.extend(
                (kind, eps, trial, x, y, t)
                for kind in ("solve_to_fixed_point", "quench", "quench_bracket")
            )

    # Results are collected by submission index, so the order of `failures` does not
    # depend on which worker finished first.
    with ProcessPoolExecutor(max_workers=worker_count(len(units))) as pool:
        for got_failures, got_checked in pool.map(_quench_unit, units):
            failures += got_failures
            checked += got_checked

    if failures:
        print(
            f"PERIMETER BREACH: {len(failures)} of {checked} configurations rejected",
            file=sys.stderr,
        )
        for f in failures[:10]:
            print(f"  {f}", file=sys.stderr)
        return 1
    print(
        f"  {checked} configurations from every emitting component pass sqpack "
        f"at tol {ORACLE_TOL:g}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
