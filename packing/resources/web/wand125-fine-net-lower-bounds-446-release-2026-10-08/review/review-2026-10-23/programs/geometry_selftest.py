"""Analytic fixtures for this review's own capture geometry (t233lib), and agreement of
its float search capture with its exact capture on the real certificates.

Fixtures, each at three rational half-angle tangents (0, 1/5002 * 977, 2/5) and the
exact clipping routine:

- a rectangle containing the core: area B^2;
- the half-plane x >= cx (a long rectangle): half the core, B^2/2 (central symmetry);
- the quadrant x >= cx, y >= cy: a quarter, B^2/4 (quarter-turn symmetry);
- a rectangle strictly inside the core: its own area;
- a rectangle far away: zero;
- a rectangle touching the core at one edge only: zero.

Then, for each certificate, the float capture used by the search is compared with the
exact capture at 40 seeded random centres and directions (agreement to 1e-9).

    python3 -I geometry_selftest.py --packet PACKET --out outputs/geometry-selftest.json
"""

from __future__ import annotations

import argparse
import json
import random
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from t233lib import (  # noqa: E402
    CERTS,
    clipped_area,
    cos_sin,
    domain_upper,
    exact_capture,
    expand,
    float_capture,
    read_candidate,
    square_vertices,
)

B = Fraction(4999, 5000)


def fixtures() -> list[dict[str, object]]:
    rows = []
    h = B / 2
    cx, cy = Fraction(3, 1), Fraction(5, 2)
    big = Fraction(10)
    for t in (Fraction(0), Fraction(977, 5002), Fraction(2, 5)):
        c, s = cos_sin(Fraction(1), 0) if t == 0 else ((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t))
        poly = square_vertices(cx, cy, c, s, h)
        reach = h * (c + s)
        cases = {
            "contains_core": ((cx - 2, cy - 2, cx + 2, cy + 2), B * B),
            "half_plane_x_ge_cx": ((cx, cy - big, cx + big, cy + big), B * B / 2),
            "quadrant": ((cx, cy, cx + big, cy + big), B * B / 4),
            "inside_core": ((cx - h / 4, cy - h / 4, cx + h / 4, cy + h / 4), (h / 2) ** 2),
            "far_away": ((cx + 3, cy + 3, cx + 4, cy + 4), Fraction(0)),
            "touches_edge_only": ((cx + reach, cy - 1, cx + reach + 1, cy + 1), Fraction(0)),
        }
        for name, (rect, want) in cases.items():
            got = clipped_area(poly, *rect)
            rows.append({"t": str(t), "case": name, "ok": got == want, "got": str(got)})
    return rows


def agreement(packet: Path, seed: int = 20261023) -> dict[str, object]:
    rng = random.Random(seed)
    out = {}
    for n in CERTS:
        cand = read_candidate(packet, n)
        meas = expand(cand)
        worst = 0.0
        for _ in range(10):
            r = rng.randrange(0, cand.last + 1)
            c, s = cos_sin(cand.step, r)
            upper = domain_upper(cand.L, cand.step, r)
            lo = cand.L / 2
            x = float(lo + (upper - lo) * Fraction(rng.random()))
            y = float(lo + (upper - lo) * Fraction(rng.random()))
            ex, _ins, _bnd = exact_capture(meas, Fraction(x), Fraction(y), c, s, cand.B / 2)
            fl = float_capture(meas, x, y, float(c), float(s), float(cand.B / 2))
            worst = max(worst, abs(float(ex) - fl))
        out[str(n)] = {"samples": 10, "max_abs_difference": float(worst), "ok": bool(worst < 1e-9)}
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--packet", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    t0 = time.perf_counter()
    fx = fixtures()
    ag = agreement(args.packet)
    ok = all(r["ok"] for r in fx) and all(v["ok"] for v in ag.values())
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out = {
        "kind": "t233-review-geometry-selftest/v1",
        "fixtures": fx,
        "float_exact_agreement": ag,
        "verdict": "PASS" if ok else "FAIL",
        "cpu_seconds": round(usage.ru_utime + usage.ru_stime, 3),
        "wall_seconds": round(time.perf_counter() - t0, 3),
    }
    args.out.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(out["verdict"], sum(r["ok"] for r in fx), "of", len(fx), "fixtures;", ag,
          "cpu", out["cpu_seconds"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
