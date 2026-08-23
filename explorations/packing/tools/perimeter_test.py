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

Usage:  python3 tools/perimeter_test.py
"""

from __future__ import annotations

import json
import math
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqpack.quench import quench, quench_bracket, solve_to_fixed_point  # noqa: E402
from sqpack.verify import corners_from_poses, float_sign, verify_packing  # noqa: E402

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
    lox = min(a - h for a, h in zip(x, half))
    loy = min(b - h for b, h in zip(y, half))
    return [a - lox for a in x], [b - loy for b in y]


def oracle(x, y, theta, side, label: str) -> list[str]:
    """Check one configuration against sqpack. Returns failure descriptions."""
    x, y = normalize(x, y, theta)
    report = verify_packing(
        corners_from_poses(x, y, theta), side, sign=float_sign(ORACLE_TOL)
    )
    if report.valid:
        return []
    return [f"{label}: {kind} — {msg}" for kind, msg in report.failures[:4]]


def enclosing_side(x, y, theta) -> float:
    half = [0.5 * (abs(math.cos(t)) + abs(math.sin(t))) for t in theta]
    return max(
        max(a + h for a, h in zip(x, half)) - min(a - h for a, h in zip(x, half)),
        max(b + h for b, h in zip(y, half)) - min(b - h for b, h in zip(y, half)),
    )


def anneal(n: int, seed: int) -> dict:
    out = subprocess.run(
        [str(BIN), "--n", str(n), "--seed", str(seed), "--chains", "4",
         "--budget-moves", "4000000"],
        capture_output=True, text=True, check=True,
    ).stdout
    best = None
    for line in out.splitlines():
        d = json.loads(line)
        if d.get("kind") == "chain" and (best is None or d["best_side"] < best["best_side"]):
            best = d
    return best


def main() -> int:
    failures: list[str] = []
    checked = 0
    seed_cfg = json.loads(
        subprocess.run([sys.executable, str(ROOT / "tools/export_trump11.py")],
                       capture_output=True, text=True, check=True).stdout
    )

    # 1. The reference packing itself. If the oracle rejects this, the oracle is wrong
    #    and nothing below it means anything.
    errs = oracle(seed_cfg["x"], seed_cfg["y"], seed_cfg["t"], seed_cfg["side"],
                  "reference trump11")
    failures += errs
    checked += 1

    # 2. sqsearch: the packing it reports, not merely its pair energy.
    if BIN.exists():
        for n in (5, 10, 11):
            best = anneal(n, 1)
            failures += oracle(best["x"], best["y"], best["t"],
                               best["best_side"] + ORACLE_TOL, f"sqsearch n={n}")
            checked += 1
    else:
        print("  sqsearch binary absent, skipping engine cells", file=sys.stderr)

    # 3. The quench, from perturbed starts -- the component that produced D-014, and
    #    the one that had no independent check at all.
    rnd = random.Random(11)
    for eps in (1e-5, 1e-3, 1e-2):
        for trial in range(2):
            x = [v + eps * rnd.uniform(-1, 1) for v in seed_cfg["x"]]
            y = [v + eps * rnd.uniform(-1, 1) for v in seed_cfg["y"]]
            t = [v + eps * rnd.uniform(-1, 1) for v in seed_cfg["t"]]
            got = solve_to_fixed_point(t, x, y, len(x))
            if got:
                failures += oracle(got[1], got[2], t, got[0] + ORACLE_TOL,
                                   f"solve_to_fixed_point eps={eps:g} #{trial}")
                checked += 1
            for name, fn in (("quench", quench), ("quench_bracket", quench_bracket)):
                r = fn(x, y, t)
                if math.isfinite(r.side):
                    failures += oracle(r.x, r.y, r.theta, r.side + ORACLE_TOL,
                                       f"{name} eps={eps:g} #{trial}")
                    # The side a component reports must also be a side the packing fits
                    # in: a claim about `s` is as much a claim as a claim about validity.
                    actual = enclosing_side(r.x, r.y, r.theta)
                    if actual > r.side + ORACLE_TOL:
                        failures.append(
                            f"{name} eps={eps:g} #{trial}: reports side {r.side:.15f} "
                            f"but its packing needs {actual:.15f}"
                        )
                    checked += 1

    if failures:
        print(f"PERIMETER BREACH: {len(failures)} of {checked} configurations rejected",
              file=sys.stderr)
        for f in failures[:10]:
            print(f"  {f}", file=sys.stderr)
        return 1
    print(f"  {checked} configurations from every emitting component pass sqpack "
          f"at tol {ORACLE_TOL:g}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
