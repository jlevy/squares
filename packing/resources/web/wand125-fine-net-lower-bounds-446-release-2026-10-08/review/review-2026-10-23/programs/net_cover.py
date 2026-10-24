"""Exact check of what the declared net covers, by direct geometry at sampled orientations.

The algebraic premises (premises.py) prove the net lemma. This program checks its
conclusion again without the closed form: for every node r of the net (step 1/5002,
indices 0..2072) and five rational half-angle tangents u in its bin (both ends, both
quarter points and the node), it builds, in exact rationals,

- the closed unit square at half-angle tangent u and the core of side B = 4999/5000 at
  the node's angle, both centred at the origin, and checks every core vertex strictly
  inside the open unit square (N3, the strict containment the counting lemma needs);
- |tan(delta/2)| <= step/2 for the relative turn (N2);
- for u in [0, tan(pi/8)], that the unit square's half-width rho(u) is at least the
  per-bin domain's rho(a_r) (lemma D: every centre the node stands for is checked).

It also checks that the bins cover [0, tan(pi/8)] with no gap. The net and the core are
the same for all four certificates, so one run covers them all.

    python3 -I net_cover.py --out outputs/net-cover.json
"""

from __future__ import annotations

import argparse
import json
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from t233lib import bin_floor, half_width  # noqa: E402

STEP = Fraction(1, 5002)
LAST = 2072
B = Fraction(4999, 5000)


def trig(t: Fraction) -> tuple[Fraction, Fraction]:
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def below_tan_pi_8(u: Fraction) -> bool:
    return u * u + 2 * u - 1 <= 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    t0 = time.perf_counter()
    half = B / 2
    checked = 0
    worst_clearance = None
    worst_at = None
    worst_z = Fraction(0)
    domain_checks = 0
    failures: list[dict[str, object]] = []
    for r in range(LAST + 1):
        tr = r * STEP
        cr, sr = trig(tr)
        # core vertices at the node angle (centre 0)
        core = [
            (half * (cr * a - sr * b), half * (sr * a + cr * b))
            for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))
        ]
        samples = {tr - STEP / 2, tr - STEP / 4, tr, tr + STEP / 4, tr + STEP / 2}
        samples = {u for u in samples if u >= 0}
        a_r = bin_floor(STEP, r)
        for u in sorted(samples):
            cu, su = trig(u)
            # the unit square at half-angle u: axes (cu, su) and (-su, cu), half-side 1/2
            clearance = None
            for px, py in core:
                p1 = abs(cu * px + su * py)
                p2 = abs(-su * px + cu * py)
                gap = Fraction(1, 2) - max(p1, p2)
                clearance = gap if clearance is None else min(clearance, gap)
            z = abs(u - tr) / (1 + u * tr)
            worst_z = max(worst_z, z)
            checked += 1
            if clearance is None or clearance <= 0 or z > STEP / 2:
                failures.append({"r": r, "u": str(u), "clearance": str(clearance)})
            if worst_clearance is None or clearance < worst_clearance:
                worst_clearance = clearance
                worst_at = (r, str(u))
            if below_tan_pi_8(u) and u >= a_r:
                domain_checks += 1
                if half_width(u) < half_width(a_r):
                    failures.append({"r": r, "u": str(u), "domain": "rho(u) < rho(a_r)"})
    # bins [t_r - D/2, t_r + D/2] are contiguous and start below 0; the last reaches past
    top = LAST * STEP + STEP / 2
    coverage = {
        "first_bin_starts_at_or_below_0": 0 * STEP - STEP / 2 <= 0,
        "consecutive_bins_share_endpoints": all(
            (r * STEP + STEP / 2) == ((r + 1) * STEP - STEP / 2) for r in range(LAST)
        ),
        "last_bin_reaches_past_tan_pi_8": not below_tan_pi_8(top),
    }
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out = {
        "kind": "t233-review-net-cover/v1",
        "net": {"step": "1/5002", "last": LAST, "B": "4999/5000"},
        "orientations_checked": checked,
        "domain_monotonicity_checks": domain_checks,
        "least_clearance_of_core_inside_unit_square": str(worst_clearance),
        "least_clearance_decimal": float(worst_clearance),
        "least_clearance_at": worst_at,
        "largest_half_turn_tangent": str(worst_z),
        "half_step": str(STEP / 2),
        "coverage": coverage,
        "failures": failures,
        "verdict": "NET_COVERS" if not failures and all(coverage.values()) else "NET_FAILS",
        "cpu_seconds": round(usage.ru_utime + usage.ru_stime, 3),
        "wall_seconds": round(time.perf_counter() - t0, 3),
    }
    args.out.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(out["verdict"], checked, "orientations; least clearance", float(worst_clearance),
          "at", worst_at, "cpu", out["cpu_seconds"])
    return 0 if out["verdict"] == "NET_COVERS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
