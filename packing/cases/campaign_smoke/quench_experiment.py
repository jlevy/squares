#!/usr/bin/env python3
"""H-002: does the LP-in-cell quench refine annealer output to the analytic optimum?

Two conditions per instance:
  annealer   the engine's own best, as exp-002..004 recorded it
  quenched   that configuration after the LP quench

and, at n = 11 only, a third that constrains the angles to CLASSES (all tilted squares
share one angle) and line-searches the shared tilt -- because the 11-dimensional angle
descent stalls, and the reason turns out to be geometric rather than numerical.

Emits JSONL; every number in the artifact is lifted from it.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import subprocess
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from sqpack.research.quench import (
    angle_classes,
    contacts,
    quench,
    quench_bracket,
    solve_to_fixed_point,
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENGINE = ROOT / "sqsearch/target/release/sqsearch"
ANALYTIC = {
    5: 2.0 + 1.0 / math.sqrt(2),
    10: 3.0 + 1.0 / math.sqrt(2),
    11: 3.877083590022814,
}


def anneal(engine: Path, n: int, seed: int, *, chains: int, budget: int) -> dict[str, Any]:
    """One engine run; returns the best chain's configuration."""
    out = subprocess.run(
        [
            str(engine),
            "--n",
            str(n),
            "--seed",
            str(seed),
            "--chains",
            str(chains),
            "--budget-moves",
            str(budget),
        ],
        cwd=ROOT,
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


def emit(rec: dict[str, Any]) -> None:
    print(json.dumps(rec), flush=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path, default=DEFAULT_ENGINE)
    parser.add_argument(
        "--instances", type=int, nargs="+", choices=sorted(ANALYTIC), default=[5, 10, 11]
    )
    parser.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    parser.add_argument("--chains", type=int, default=8)
    parser.add_argument("--budget-moves", type=int, default=20_000_000)
    parser.add_argument(
        "--skip-angle-class",
        action="store_true",
        help="omit the Trump-specific one-dimensional angle-class arm",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the H-002 arms and stream their JSONL records."""
    parser = _parser()
    options = parser.parse_args(argv)
    if not options.engine.is_file():
        parser.error(
            f"sqsearch executable not found at {options.engine}; "
            "run `cargo build --locked --release --manifest-path sqsearch/Cargo.toml`"
        )
    if options.chains <= 0 or options.budget_moves <= 0:
        parser.error("--chains and --budget-moves must be positive")
    if not options.seeds or any(seed < 0 for seed in options.seeds):
        parser.error("--seeds must contain non-negative integers")

    for n in options.instances:
        for seed in options.seeds:
            a = anneal(
                options.engine,
                n,
                seed,
                chains=options.chains,
                budget=options.budget_moves,
            )
            t0 = time.monotonic()
            b = quench_bracket(a["x"], a["y"], a["t"])
            emit(
                {
                    "kind": "quench",
                    "arm": "annealer->bracket",
                    "n": n,
                    "seed": seed,
                    "analytic": ANALYTIC[n],
                    "annealer_side": a["best_side"],
                    "annealer_gap": a["best_side"] - ANALYTIC[n],
                    "quenched_side": b.side,
                    "quenched_gap": b.side - ANALYTIC[n],
                    "lp_solves": b.lp_solves,
                    "angle_steps": b.angle_steps,
                    "cell_changes": b.cell_changes,
                    "converged": b.converged,
                    "reason": b.reason,
                    "contacts": len(contacts(b.x, b.y, b.theta)),
                    "classes": len(angle_classes(b.theta, 1e-2)),
                    "seconds": time.monotonic() - t0,
                }
            )
            t0 = time.monotonic()
            r = quench(a["x"], a["y"], a["t"], max_rounds=200)
            elapsed = time.monotonic() - t0
            emit(
                {
                    "kind": "quench",
                    "arm": "annealer->quench",
                    "n": n,
                    "seed": seed,
                    "analytic": ANALYTIC[n],
                    "annealer_side": a["best_side"],
                    "annealer_gap": a["best_side"] - ANALYTIC[n],
                    "quenched_side": r.side,
                    "quenched_gap": r.side - ANALYTIC[n],
                    "lp_solves": r.lp_solves,
                    "angle_steps": r.angle_steps,
                    "cell_changes": r.cell_changes,
                    "converged": r.converged,
                    "reason": r.reason,
                    "contacts": len(contacts(r.x, r.y, r.theta)),
                    "seconds": elapsed,
                }
            )

    # n = 11 only: the same quench with the angles constrained to two classes, and the
    # shared tilt found by golden section rather than by descent. Golden section needs a
    # deterministic objective, so every evaluation re-solves from the SAME centres.
    if options.skip_angle_class or 11 not in options.instances:
        return 0

    seed_cfg = json.loads(
        subprocess.run(
            [sys.executable, "-m", "cases.trump11.export_seed"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
    tilt = max(round(t, 9) for t in seed_cfg["t"])
    for eps in (1e-5, 1e-3, 1e-2, 1e-1):
        rnd = random.Random(2)
        ref_x = [v + eps * rnd.uniform(-1, 1) for v in seed_cfg["x"]]
        ref_y = [v + eps * rnd.uniform(-1, 1) for v in seed_cfg["y"]]
        start = tilt + eps * rnd.uniform(-1, 1)
        calls = 0

        def s_of(
            tt: float,
            ref_x: tuple[float, ...] = tuple(ref_x),
            ref_y: tuple[float, ...] = tuple(ref_y),
        ) -> float:
            nonlocal calls
            calls += 1
            got = solve_to_fixed_point([0.0] * 6 + [tt] * 5, list(ref_x), list(ref_y), 11)
            return got.side if got and got.settled else 1e3

        t0 = time.monotonic()
        gr = (math.sqrt(5) - 1) / 2
        lo, hi = start - 0.05, start + 0.05
        a, b = hi - gr * (hi - lo), lo + gr * (hi - lo)
        fa, fb = s_of(a), s_of(b)
        while hi - lo > 1e-15:
            if fa < fb:
                hi, b, fb = b, a, fa
                a = hi - gr * (hi - lo)
                fa = s_of(a)
            else:
                lo, a, fa = a, b, fb
                b = lo + gr * (hi - lo)
                fb = s_of(b)
        theta_hat = (lo + hi) / 2
        side = s_of(theta_hat)
        emit(
            {
                "kind": "quench",
                "arm": "angle-class-1d",
                "n": 11,
                "eps": eps,
                "analytic": ANALYTIC[11],
                "quenched_side": side,
                "quenched_gap": side - ANALYTIC[11],
                "theta": theta_hat,
                "theta_error": theta_hat - tilt,
                "lp_solves": calls,
                "seconds": time.monotonic() - t0,
            }
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
