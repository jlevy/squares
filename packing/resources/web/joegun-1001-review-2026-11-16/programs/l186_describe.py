"""Lane L186: describe a certificate; it decides nothing.

Usage: python -I -B l186_describe.py CERT.yaml CHECK.json OUT.json

Reads the certificate through the reader and recomputes, with method A's
functions, the facts the review describes: each square's exact edge direction
reduced modulo a quarter turn, the tilts, the near pairs and their spread, how
each wall contact is made (one corner or an edge), the near clearances at each
wall, and the size of the rationals. It writes them; the verdict is the check's.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from collections import Counter
from fractions import Fraction
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l186_sat as ma  # noqa: E402
from l186_decide import WALLS, ftext, sci  # noqa: E402
from l186_reader import read_witness_file  # noqa: E402


def canonical_dir(c: Fraction, s: Fraction) -> tuple[Fraction, Fraction]:
    """The edge direction turned by quarter turns into c > 0, s >= 0."""
    for _ in range(4):
        if c > 0 and s >= 0:
            return c, s
        c, s = -s, c
    raise ValueError("zero direction")


def main() -> None:
    path, check_path, out_path = sys.argv[1:4]
    t0 = time.process_time()
    w = read_witness_file(path)
    with open(check_path) as fh:
        chk = json.load(fh)
    n, S = w.n, w.side
    pa = [ma.prepare(sq) for sq in w.squares]
    # ---- directions
    dirs: list[tuple[Fraction, Fraction]] = []
    for sq in w.squares:
        u = (sq[1][0] - sq[0][0], sq[1][1] - sq[0][1])
        dirs.append(canonical_dir(u[0], u[1]))
    groups = Counter(dirs)
    degs = {d: math.degrees(math.atan2(float(d[1]), float(d[0]))) for d in groups}

    def signed(d: tuple[Fraction, Fraction]) -> float:
        a = degs[d]
        return a - 90.0 if a > 45.0 else a

    upright = sum(1 for d in dirs if d[1] == 0)
    tilted = [signed(d) for d in dirs if d[1] != 0]
    orient = []
    for d, cnt in sorted(groups.items(), key=lambda kv: (-kv[1], signed(kv[0]))):
        c, s = d
        # tan of half the turn, for the signed angle in (-45, 45]
        if degs[d] > 45.0:
            c2, s2 = s, -c  # turned back a quarter
        else:
            c2, s2 = c, s
        t = s2 / (1 + c2)
        orient.append(
            {
                "count": cnt,
                "degrees": round(signed(d), 9),
                "tan_half": ftext(t) if len(ftext(t)) < 200 else f"{len(str(t.numerator))}-digit/{len(str(t.denominator))}-digit",
                "tan_half_den_digits": len(str(t.denominator)),
                "squares": [i + 1 for i in range(n) if dirs[i] == d][:12],
            }
        )
    # ---- near pairs
    near: list[tuple[Fraction, int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            m = ma.pair_margin(pa[i], pa[j])
            if m < Fraction(1, 10**3):
                near.append((m, i + 1, j + 1))
    near.sort()
    below9 = [x for x in near if x[0] < Fraction(1, 10**9)]
    above9 = [x for x in near if x[0] >= Fraction(1, 10**9)]
    vals9 = [x[0] for x in below9]
    near_desc: dict[str, Any] = {
        "pairs_below_1e-3": len(near),
        "pairs_below_1e-9": len(below9),
        "least": [sci(below9[0][0]), below9[0][1:]] if below9 else None,
        "greatest_below_1e-9": [sci(below9[-1][0]), below9[-1][1:]] if below9 else None,
        "median_below_1e-9": sci(vals9[len(vals9) // 2]) if vals9 else None,
        "distinct_values_below_1e-9": len(set(vals9)),
        "next_above_1e-9": [sci(above9[0][0]), above9[0][1:]] if above9 else None,
        "first_20": [[sci(m), i, j] for m, i, j in near[:20]],
        "decades": dict(
            Counter(
                (math.floor(math.log10(float(m))) if m > 0 else "nonpositive") for m, _, _ in near
            ).most_common()
        ),
    }
    # ---- wall contacts and near clearances
    contacts: list[dict[str, Any]] = []
    near_walls: dict[str, list[Any]] = {wl: [] for wl in WALLS}
    for i, sq in enumerate(w.squares):
        cl = ma.wall_clearances(pa[i], S)
        for k, wl in enumerate(WALLS):
            if cl[k] == 0:
                if wl == "left":
                    on = sum(1 for x, _ in sq if x == 0)
                elif wl == "bottom":
                    on = sum(1 for _, y in sq if y == 0)
                elif wl == "right":
                    on = sum(1 for x, _ in sq if x == S)
                else:
                    on = sum(1 for _, y in sq if y == S)
                contacts.append({"square": i + 1, "wall": wl, "corners_on_wall": on, "upright": dirs[i][1] == 0})
            elif cl[k] < Fraction(1, 10**9):
                near_walls[wl].append([i + 1, sci(cl[k])])
    # ---- size of the rationals
    den_digits = [len(str(v.denominator)) for sq in w.squares for p in sq for v in p]
    rec = {
        "file": os.path.basename(path),
        "n": n,
        "verdict_from_check": chk["verdict"],
        "side_digits": [len(str(S.numerator)), len(str(S.denominator))],
        "corner_denominator_digits": {"min": min(den_digits), "max": max(den_digits)},
        "exactly_upright": upright,
        "tilted": len(tilted),
        "tilted_beyond_1e-9_deg": sum(1 for a in tilted if abs(a) > 1e-9),
        "tilted_beyond_1_deg": sum(1 for a in tilted if abs(a) > 1.0),
        "tilt_range_deg": [min(tilted), max(tilted)] if tilted else None,
        "orientations_exact": len(groups),
        "orientations_six_places": len({round(signed(d), 6) for d in groups}),
        "orientations": orient[:40],
        "near_pairs": near_desc,
        "wall_contacts": contacts,
        "near_walls_below_1e-9": near_walls,
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    with open(out_path, "w") as fh:
        json.dump(rec, fh, indent=1)
        fh.write("\n")
    print(rec["file"], "upright", upright, "tilted", len(tilted), "orientations", len(groups), "near<1e-9", len(below9))


if __name__ == "__main__":
    main()
