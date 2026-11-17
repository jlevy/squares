"""The packing against the registry's n = 70 and n = 207 packings: the s(70) + 5 question.

Lane L108, blind stage 4 review of jlevy/squares#959. Written after the findings were
frozen; decides nothing. Places the registry's 70 packing (and 207) under each of the
eight symmetries of its own box at each corner of the 179 box, counts the 179 squares a
placed square matches (centre and angle modulo 90 degrees both within a tolerance), and
classifies every square as matched by the 70 packing at the lower-left corner, by its
copy at the upper-right corner (offset S - s(70), which is 5 + 2.6e-12), or as an upright
square on a unit lattice anchored at two walls.

Usage: python -I -B l108_s70.py CERT.yaml REPO_ROOT OUT.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import mpmath

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l108_wit as wit  # noqa: E402

mpmath.mp.dps = 60
TOLS = ("1e-11", "1e-9", "1e-6", "1e-3")
CORNERS = ("lower-left", "lower-right", "upper-left", "upper-right")


def sym(k: int, x: Any, y: Any, deg: Any, side: Any) -> tuple[Any, Any, Any]:
    """The k-th symmetry of the box [0, side]^2; reflections negate the angle."""
    maps = [
        (x, y, deg),
        (side - y, x, deg),  # quarter turn
        (side - x, side - y, deg),  # half turn
        (y, side - x, deg),  # three quarters
        (side - x, y, -deg),  # mirror in the vertical centre line
        (x, side - y, -deg),  # mirror in the horizontal centre line
        (y, x, -deg),  # mirror in the main diagonal
        (side - y, side - x, -deg),  # mirror in the other diagonal
    ]
    return maps[k]


SYM_NAMES = ("identity", "quarter turn", "half turn", "three-quarter turn", "mirror x", "mirror y", "mirror main diagonal", "mirror other diagonal")


def norm_deg(d: Any) -> Any:
    while d > 45:
        d -= 90
    while d <= -45:
        d += 90
    return d


def place(ref: wit.Packing, k: int, corner: str, big: Any) -> list[tuple[Any, Any, Any]]:
    off = big - ref.side
    dx = off if corner in ("lower-right", "upper-right") else 0
    dy = off if corner in ("upper-left", "upper-right") else 0
    out = []
    for p in ref.poses:
        x, y, d = sym(k, p.cx, p.cy, p.deg, ref.side)
        out.append((x + dx, y + dy, norm_deg(d)))
    return out


def matches(cert: wit.Packing, placed: list[tuple[Any, Any, Any]], tol: Any) -> set[int]:
    hit: set[int] = set()
    fl = [(float(x), float(y)) for x, y, _d in placed]
    for i, p in enumerate(cert.poses):
        px, py = float(p.cx), float(p.cy)
        j = min(range(len(fl)), key=lambda t: (fl[t][0] - px) ** 2 + (fl[t][1] - py) ** 2)
        x, y, d = placed[j]
        dist = mpmath.sqrt((x - p.cx) ** 2 + (y - p.cy) ** 2)
        ang = abs(norm_deg(d - p.deg))
        if dist < tol and ang < tol * 57.29577951308232:
            hit.add(i + 1)
    return hit


def lattice(cert: wit.Packing, tol: Any) -> set[int]:
    """Upright squares whose centre is a half-integer from a wall in both x and y."""
    s = cert.side
    out: set[int] = set()
    for i, p in enumerate(cert.poses):
        if abs(mpmath.radians(p.deg)) >= tol:
            continue

        def anchored(c: Any) -> bool:
            for v in (c - mpmath.mpf(1) / 2, s - c - mpmath.mpf(1) / 2):
                if abs(v - mpmath.nint(v)) < tol:
                    return True
            return False

        if anchored(p.cx) and anchored(p.cy):
            out.add(i + 1)
    return out


def main(argv: list[str]) -> int:
    cert = wit.load(Path(argv[1]), "certificate")
    repo = Path(argv[2])
    p70 = wit.load(repo / "packing/witnesses/known-best/n-070.yaml", "n-070")
    p207 = wit.load(repo / "packing/witnesses/known-best/n-207.yaml", "n-207")
    s = cert.side
    out: dict[str, Any] = {"program": "l108_s70.py", "side_less_s70_plus_5": mpmath.nstr(s - p70.side - 5, 8)}
    band70 = sorted({mpmath.nstr(p.deg, 15) for p in p70.poses if abs(p.deg) > mpmath.mpf("0.5")})
    out["n70_tilted"] = {"count": sum(1 for p in p70.poses if abs(p.deg) > mpmath.mpf("0.5")), "angles": band70}
    out["n207_tilted"] = {
        "count": sum(1 for p in p207.poses if abs(p.deg) > mpmath.mpf("0.5")),
        "angles": sorted({mpmath.nstr(p.deg, 15) for p in p207.poses if abs(p.deg) > mpmath.mpf("0.5")}),
    }
    a70 = mpmath.mpf(band70[0]) if len(band70) == 1 else None
    tilted = [(i + 1, p) for i, p in enumerate(cert.poses) if abs(p.deg) > mpmath.mpf("0.5")]
    if a70 is not None:
        dev = sorted((abs(p.deg - a70), k) for k, p in tilted)
        out["certificate_tilted"] = {
            "count": len(tilted),
            "within_1e-9_deg_of_n70_band": sum(1 for d, _k in dev if d < mpmath.mpf("1e-9")),
            "within_1e-6_deg": sum(1 for d, _k in dev if d < mpmath.mpf("1e-6")),
            "within_0.01_deg": sum(1 for d, _k in dev if d < mpmath.mpf("0.01")),
            "largest_deviation_deg": [mpmath.nstr(dev[-1][0], 6), dev[-1][1]],
            "angles": sorted({mpmath.nstr(p.deg, 10) for _k, p in tilted}),
            "others": [[k, mpmath.nstr(p.deg, 10), mpmath.nstr(p.cx, 8), mpmath.nstr(p.cy, 8)] for k, p in tilted if abs(p.deg - a70) >= mpmath.mpf("1e-6")],
        }
    # Every placement of the 70 and 207 packings.
    for ref in (p70, p207):
        table = []
        for k in range(8):
            for corner in CORNERS:
                placed = place(ref, k, corner, s)
                counts = {t: len(matches(cert, placed, mpmath.mpf(t))) for t in TOLS}
                table.append({"symmetry": SYM_NAMES[k], "corner": corner, **counts})
        table.sort(key=lambda r: (-r["1e-11"], -r["1e-6"]))
        out[f"{ref.name}_placements_best"] = table[:6]
    # The decomposition: 70 at lower-left (identity), its copy at upper-right, lattice squares.
    tol = mpmath.mpf("1e-11")
    ll = matches(cert, place(p70, 0, "lower-left", s), tol)
    ur = matches(cert, place(p70, 0, "upper-right", s), tol)
    lat = lattice(cert, tol)
    union = ll | ur | lat
    rest = sorted(set(range(1, cert.n + 1)) - union)
    out["decomposition_tol_1e-11"] = {
        "n70_lower_left": len(ll),
        "n70_upper_right_copy": len(ur),
        "both": len(ll & ur),
        "lattice_upright_anchored": len(lat),
        "lattice_not_in_either_copy": len(lat - ll - ur),
        "union": len(union),
        "unexplained": [[k, mpmath.nstr(cert.poses[k - 1].cx, 8), mpmath.nstr(cert.poses[k - 1].cy, 8), mpmath.nstr(cert.poses[k - 1].deg, 8)] for k in rest],
        "tilted_in_lower_left_copy": sum(1 for k, _p in tilted if k in ll),
        "tilted_in_upper_right_copy": sum(1 for k, _p in tilted if k in ur),
        "tilted_in_neither": [k for k, _p in tilted if k not in ll and k not in ur],
    }
    # The seed the issue states: the 70 band where x + y <= 16, and its copy shifted by
    # (5, 5) where x + y > 16, under each symmetry of the 70 box.
    seed_rows = []
    for k in range(8):
        seed = []
        for p in p70.poses:
            if abs(p.deg) <= mpmath.mpf("0.5"):
                continue
            x, y, d = sym(k, p.cx, p.cy, p.deg, p70.side)
            if x + y <= 16:
                seed.append((x, y, norm_deg(d)))
            if x + y + 10 > 16:
                seed.append((x + 5, y + 5, norm_deg(d)))
        row: dict[str, Any] = {"symmetry": SYM_NAMES[k], "seed_squares": len(seed)}
        for tol in ("0.05", "0.1", "0.25"):
            hit = 0
            for _k, p in tilted:
                if any(mpmath.sqrt((x - p.cx) ** 2 + (y - p.cy) ** 2) < mpmath.mpf(tol) and abs(norm_deg(d - p.deg)) < 1 for x, y, d in seed):
                    hit += 1
            row[f"tilted_within_{tol}"] = hit
        seed_rows.append(row)
    out["stated_seed"] = seed_rows
    # 70 + an L-border: does any placement hold all 70 squares?
    full = []
    for k in range(8):
        for corner in CORNERS:
            placed = place(p70, k, corner, s)
            hit = matches(cert, placed, mpmath.mpf("1e-6"))
            full.append(len(hit))
    out["n70_whole_packing_present"] = {"best_placement_matches_at_1e-6": max(full), "of": p70.n}
    Path(argv[3]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
