"""C1: exact check of the construction for s(18) <= (7+sqrt7)/2, with controls.

Usage: python -I r1050_construction.py --construction six-tilt18.json --out out.json

Reads the coordinate table only. Every wall inequality and every pair is decided in
Q(sqrt 7) with no tolerance (r1050_q7). Then four kinds of mutation, each of which must
be refused: the side lowered by 10^-30; each touching pair closed by 10^-30 of its
centre difference; each tilted tile's orientation bit flipped; a tile duplicated.
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from r1050_q7 import (  # noqa: E402
    U_AXIS,
    U_TILT,
    V_AXIS,
    V_TILT,
    Q7,
    Tile,
    check_packing,
    frame_ok,
    load_construction,
)

TINY = Fraction(1, 10**30)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--construction", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    side, tiles = load_construction(args.construction)
    h_exact = Q7(Fraction(7, 2), Fraction(1, 2))
    report: dict[str, object] = {
        "program": "r1050_construction.py",
        "tiles": len(tiles),
        "tilted": sum(1 for t in tiles if t.u is U_TILT),
        "side_is_H": side == h_exact,
        "frames_orthonormal": frame_ok(U_TILT, V_TILT) and frame_ok(U_AXIS, V_AXIS),
        "side_float": float(side),
    }
    base = check_packing(side, tiles)
    report["check"] = base

    controls: list[dict[str, object]] = []
    # Side lowered by 10^-30.
    r = check_packing(side - TINY, tiles)
    controls.append({"control": "side H - 1e-30", "refused": not r["valid"],
                     "wall_failures": len(r["wall_failures"])})  # type: ignore[arg-type]
    # Each touching pair closed by 10^-30 of its centre difference.
    by_id = {t.tid: t for t in tiles}
    for a_id, b_id in base["pair_contacts"]:  # type: ignore[union-attr]
        a, b = by_id[a_id], by_id[b_id]
        dx = (a.c[0] - b.c[0]).scale(TINY)
        dy = (a.c[1] - b.c[1]).scale(TINY)
        moved = [b.moved(dx, dy) if t.tid == b_id else t for t in tiles]
        r = check_packing(side, moved)
        refused_pair = [a_id, b_id] in r["pair_failures"]  # type: ignore[operator]
        controls.append({"control": f"pair {a_id}-{b_id} closed by 1e-30",
                         "refused": refused_pair})
    # Each tilted tile flipped to the axis frame.
    for t in tiles:
        if t.u is not U_TILT:
            continue
        flipped = [Tile(s.tid, s.c, U_AXIS, V_AXIS) if s.tid == t.tid else s for s in tiles]
        r = check_packing(side, flipped)
        controls.append({"control": f"tile {t.tid} orientation flipped", "refused": not r["valid"]})
    # A tile duplicated.
    dup = [*tiles, Tile(999, tiles[0].c, tiles[0].u, tiles[0].v)]
    r = check_packing(side, dup)
    controls.append({"control": f"tile {tiles[0].tid} duplicated", "refused": not r["valid"]})

    report["controls"] = controls
    all_refused = all(c["refused"] for c in controls)
    ok = bool(base["valid"]) and bool(report["side_is_H"]) and bool(report["frames_orthonormal"])
    report["verdict"] = "CONSTRUCTION_VALID" if ok else "CONSTRUCTION_REFUSED"
    report["controls_verdict"] = "ALL_CONTROLS_REFUSED" if all_refused else "SOME_CONTROL_PASSED"
    args.out.write_text(json.dumps(report, indent=1) + "\n")
    print(report["verdict"], report["controls_verdict"], f"valid {base['valid']}",
          f"side_is_H {report['side_is_H']}", f"walls {base['walls_checked']}",
          f"pairs {base['pairs_checked']}", f"contacts {len(base['pair_contacts'])}",  # type: ignore[arg-type]
          f"wall contacts {len(base['wall_contacts'])}")  # type: ignore[arg-type]
    return 0 if ok and all_refused else 1


if __name__ == "__main__":
    raise SystemExit(main())
