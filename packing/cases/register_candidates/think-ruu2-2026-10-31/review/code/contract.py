"""Contract a certificate uniformly to first contact, exactly, and decide the result.

Usage: python3.14 contract.py INPUTS_DIR OUT_DIR

A certificate padded by a dilation keeps every pair apart by about the padding. Scaling
every centre by lambda about the origin (rotations fixed) scales each pair's
projections on its four fixed edge normals by lambda and leaves its threshold T alone,
so the pair stays interior-disjoint iff lambda >= T / M, M = max_u |u . d|. The least
feasible lambda is therefore lambda* = max over pairs of T / M, an exact rational, at
which the binding pair touches. The contracted packing is then translated into the
corner and boxed: Lx = max(lambda* cx + h) - min(lambda* cx - h), likewise Ly, and the
box side is L' = max(Lx, Ly).

The contracted packing is decided again on both routes, so L' is a proved bound on its
own, and is compared with the house's side and the candidate's: house - L' is padding
that uniform contraction alone removes from the house's own coordinates.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import qio
import route_area
import route_sat


def lambda_star(squares: list[qio.Square]) -> tuple[Fraction, int, int]:
    best = Fraction(0)
    where = (-1, -1)
    n = len(squares)
    for i in range(n):
        cxi, cyi, ai, bi = squares[i]
        for j in range(i + 1, n):
            cxj, cyj, aj, bj = squares[j]
            dx, dy = cxj - cxi, cyj - cyi
            t = (1 + abs(ai * aj + bi * bj) + abs(ai * bj - bi * aj)) / 2
            m = max(abs(ai * dx + bi * dy), abs(-bi * dx + ai * dy), abs(aj * dx + bj * dy), abs(-bj * dx + aj * dy))
            r = t / m
            if r > best:
                best, where = r, (i, j)
    return best, where[0], where[1]


def contract(squares: list[qio.Square], lam: Fraction) -> tuple[Fraction, list[qio.Square]]:
    h = [(abs(a) + abs(b)) / 2 for _, _, a, b in squares]
    xs = [lam * s[0] for s in squares]
    ys = [lam * s[1] for s in squares]
    x0 = min(x - hh for x, hh in zip(xs, h))
    y0 = min(y - hh for y, hh in zip(ys, h))
    lx = max(x + hh for x, hh in zip(xs, h)) - x0
    ly = max(y + hh for y, hh in zip(ys, h)) - y0
    out = [(x - x0, y - y0, s[2], s[3]) for x, y, s in zip(xs, ys, squares)]
    return max(lx, ly), out


def main() -> None:
    inp, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    _, s260, sq260, _ = qio.read_tcert(inp / "s260_1028.cert")
    cand_side = {
        130: qio.read_view(inp / "n130-view-solved.yaml")[1],
        307: qio.read_view(inp / "n307-view-solved.yaml")[1],
        293: s260 + 1,
        260: s260,
    }
    subjects: dict[str, tuple[int, Fraction, list[qio.Square]]] = {}
    for n in (130, 293, 307):
        _, side, sq, _ = qio.read_view(inp / f"house-n{n}.yaml")
        subjects[f"house{n}"] = (n, side, sq)
    subjects["s260"] = (260, s260, sq260)
    report: dict[str, object] = {}
    for label, (n, side, sq) in subjects.items():
        t0 = time.process_time()
        lam, i, j = lambda_star(sq)
        lp, packed = contract(sq, lam)
        ra = route_sat.check(lp, packed)
        rb = route_area.check(lp, packed)
        cpu = round(time.process_time() - t0, 2)
        line = (
            f"{label}: lambda* = 1 - {float(1 - lam):.6e} (pair {i + 1},{j + 1}); contracted side {float(lp):.18f};"
            f" house - contracted {float(side - lp):.6e}; contracted - candidate {float(lp - cand_side[n]):+.6e};"
            f" route A {ra['accepted']} route B {rb['accepted']}; cpu {cpu}s"
        )
        print(line, flush=True)
        report[label] = {
            "n": n,
            "house_or_certificate_side": str(side),
            "lambda_star": str(lam),
            "binding_pair": [i + 1, j + 1],
            "contracted_side": str(lp),
            "side_minus_contracted": f"{float(side - lp):.6e}",
            "contracted_minus_candidate": f"{float(lp - cand_side[n]):+.6e}",
            "route_A_accepted": ra["accepted"],
            "route_B_accepted": rb["accepted"],
            "route_A_least_pair_slack": str(ra["least_pair_slack"][0]),
            "cpu_seconds": cpu,
        }
    (outdir / "contract.json").write_text(json.dumps(report, indent=1) + "\n")


if __name__ == "__main__":
    main()
