"""Measure a candidate pose by pose against its count's house (binary64; decides nothing).

Usage: python3.14 identity.py INPUTS_DIR OUT_DIR

For each of the box's eight symmetries applied to the candidate, pair every candidate
square with its nearest house centre and report whether the pairing is one to one, the
largest centre move, the largest turn (angles mod 90 degrees, signed for reflections),
and how many squares move beyond 1e-12 ... 1e-1. The best symmetry is the one-to-one
pairing with the least largest move.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import qio

THRESHOLDS = (1e-12, 1e-11, 1e-10, 1e-9, 1e-6, 1e-3, 1e-1)


def floats(squares: list[qio.Square]) -> list[tuple[float, float, float]]:
    out = []
    for cx, cy, a, b in squares:
        ang = math.degrees(math.atan2(float(b), float(a))) % 90.0
        out.append((float(cx), float(cy), ang))
    return out


def sym(k: int, side: float, x: float, y: float, ang: float) -> tuple[float, float, float]:
    swap, fx, fy = k & 4, k & 1, k & 2
    if swap:
        x, y = y, x
    if fx:
        x = side - x
    if fy:
        y = side - y
    reflections = (1 if swap else 0) + (1 if fx else 0) + (1 if fy else 0)
    if reflections % 2:
        ang = (-ang) % 90.0
    return x, y, ang


def turn(a: float, b: float) -> float:
    return ((a - b + 45.0) % 90.0) - 45.0


def measure(cand: list[qio.Square], cside: Fraction, house: list[qio.Square]) -> dict[str, object]:
    c = floats(cand)
    h = floats(house)
    side = float(cside)
    best: dict[str, object] | None = None
    per_sym = []
    for k in range(8):
        moved = [sym(k, side, *p) for p in c]
        match = []
        for x, y, ang in moved:
            j = min(range(len(h)), key=lambda m: (h[m][0] - x) ** 2 + (h[m][1] - y) ** 2)
            match.append((j, math.hypot(h[j][0] - x, h[j][1] - y), turn(ang, h[j][2])))
        one_to_one = len({m[0] for m in match}) == len(h) == len(c)
        dmax = max(m[1] for m in match)
        tmax = max(abs(m[2]) for m in match)
        counts = {f"{t:.0e}": sum(1 for m in match if m[1] > t) for t in THRESHOLDS}
        rec = {
            "symmetry": k,
            "one_to_one": one_to_one,
            "largest_move": dmax,
            "largest_turn_degrees": tmax,
            "moved_beyond": counts,
            "moved_squares_beyond_1e-9": sorted(
                ((i + 1, match[i][0] + 1, match[i][1], match[i][2]) for i in range(len(c)) if match[i][1] > 1e-9),
                key=lambda r: -r[2],
            ),
        }
        per_sym.append({kk: rec[kk] for kk in ("symmetry", "one_to_one", "largest_move")})
        if one_to_one and (best is None or dmax < best["largest_move"]):  # type: ignore[operator]
            best = rec
    return {"best": best, "per_symmetry": per_sym}


def main() -> None:
    inp, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    _, s260, sq260, _ = qio.read_tcert(inp / "s260_1028.cert")
    cands = {
        130: qio.read_view(inp / "n130-view-solved.yaml")[1:3],
        307: qio.read_view(inp / "n307-view-solved.yaml")[1:3],
    }
    cands["130-solve"] = qio.read_tcert(inp / "n130-solve-witness.cert")[1:3]
    cands["307-solve"] = qio.read_tcert(inp / "n307-solve-witness.cert")[1:3]
    result = {}
    for key, (cside, csq) in cands.items():
        n = int(str(key).split("-")[0])
        _, hside, hsq, _ = qio.read_view(inp / f"house-n{n}.yaml")
        m = measure(csq, cside, hsq)
        result[str(key)] = m
        b = m["best"]
        assert isinstance(b, dict)
        print(
            f"n={key}: best symmetry {b['symmetry']} one_to_one={b['one_to_one']} largest move {b['largest_move']:.3e}"
            f" largest turn {b['largest_turn_degrees']:.3e} deg; moved beyond {b['moved_beyond']}"
        )
        for row in b["moved_squares_beyond_1e-9"][:12]:
            print(f"   cand {row[0]:3d} -> house {row[1]:3d}: move {row[2]:.3e}, turn {row[3]:+.3e} deg")
    # 293: the house's strip and its 260 block apart. A strip square is axis-aligned
    # with its centre within 1e-9 of x = U - 1/2 or y = U - 1/2, U the house's side.
    _, h293side, h293, _ = qio.read_view(inp / "house-n293.yaml")
    edge = float(h293side - Fraction(1, 2))
    is_l = [q[2] == 1 and q[3] == 0 and min(abs(float(q[0]) - edge), abs(float(q[1]) - edge)) < 1e-9 for q in h293]
    block = [q for q, f in zip(h293, is_l) if not f]
    strip = [q for q, f in zip(h293, is_l) if f]
    print(f"n=293 house: {len(block)} block squares, {len(strip)} strip squares (ids {[i + 1 for i, f in enumerate(is_l) if f]})")
    m_block = measure(sq260, s260, block)
    b = m_block["best"]
    assert isinstance(b, dict)
    print(
        f"n=293: s260_1028.cert against the house's block: best symmetry {b['symmetry']} one_to_one={b['one_to_one']}"
        f" largest move {b['largest_move']:.3e} largest turn {b['largest_turn_degrees']:.3e} deg; moved beyond {b['moved_beyond']}"
    )
    for variant in ("17top+16", "16+16+1", "17+16"):
        m_strip = measure(qio.l_strip(s260, variant), s260 + 1, strip)
        bs = m_strip["best"]
        if bs is None:
            print(f"n=293: strip {variant} against the house's strip: no one-to-one pairing under any symmetry")
            continue
        print(
            f"n=293: strip {variant} against the house's strip: best symmetry {bs['symmetry']}"
            f" largest move {bs['largest_move']:.3e}; moved beyond {bs['moved_beyond']}"
        )
        result[f"293-strip-{variant}"] = m_strip
    result["293-block"] = m_block
    (outdir / "identity.json").write_text(json.dumps(result, indent=1, default=str) + "\n")


if __name__ == "__main__":
    main()
