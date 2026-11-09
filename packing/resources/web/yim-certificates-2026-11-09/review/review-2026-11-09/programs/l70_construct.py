"""How the certificates were made (L70 review): a measurement, which decides nothing.

Per certificate: the turns (exactly upright, below 1e-9 radian, to 0.5 degree,
beyond), the sizes of the rationals, and the distribution of the pair margins and
wall clearances below 1e-9 (from the check receipts, binary64 of exact values).

Usage: python -I l70_construct.py --src SRC --repo REPO --checks OUTDIR --out construct.json
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import l70_check as C  # noqa: E402
import l70_reader as R  # noqa: E402

WEB = "packing/resources/web"
BH = (553, 599, 600, 601, 602, 604, 645, 647, 648, 699, 700)
BINS = [0.0, 1e-30, 2e-30, 1e-20, 1e-15, 1e-14, 1e-13, 2e-13, 3e-13, 1e-12, 1e-10, 1e-9]


def hist(vals: list[float]) -> dict[str, int]:
    out = {}
    for lo, hi in zip(BINS[:-1], BINS[1:], strict=True):
        out[f"[{lo:g}, {hi:g})"] = sum(1 for v in vals if lo <= v < hi)
    return out


def turns(pk: R.Packing) -> dict[str, Any]:
    angles = []
    if pk.kind == "cert":
        for row in pk.squares:
            t = F(row[4], row[5])
            if t in (0, 1, -1):
                angles.append(0.0)
            else:
                a = 2 * math.atan(float(t))
                a = (a + math.pi / 4) % (math.pi / 2) - math.pi / 4
                angles.append(abs(a) if a != 0 else 1e-300)
        tdig = max(max(len(str(abs(r[4]))), len(str(r[5]))) for r in pk.squares)
        cdig = max(max(len(str(abs(r[k]))) for k in range(4)) for r in pk.squares)
    else:
        for row in pk.squares:
            ux = F(row[4], row[5]) - F(row[0], row[1])
            uy = F(row[6], row[7]) - F(row[2], row[3])
            if ux == 0 or uy == 0:
                angles.append(0.0)
            else:
                a = math.atan2(float(uy), float(ux))
                a = (a + math.pi / 4) % (math.pi / 2) - math.pi / 4
                angles.append(abs(a) if a != 0 else 1e-300)
        tdig = None
        cdig = max(max(len(str(abs(v))) for v in r) for r in pk.squares)
    deg = math.pi / 180
    tiny = [a for a in angles if 0 < a < 1e-9]
    return {
        "exactly_upright": sum(1 for a in angles if a == 0),
        "turned_below_1e-9_rad": len(tiny),
        "smallest_nonzero_turn_rad": min(tiny) if tiny else None,
        "largest_turn_below_1e-9_rad": max(tiny) if tiny else None,
        "turned_1e-9_rad_to_0.5_deg": sum(1 for a in angles if 1e-9 <= a <= 0.5 * deg),
        "turned_beyond_0.5_deg": sum(1 for a in angles if a > 0.5 * deg),
        "turned_beyond_1_deg": sum(1 for a in angles if a > deg),
        "tangent_digits_max": tdig,
        "coordinate_digits_max": cdig,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--checks", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()
    src = Path(ns.src)
    repo = Path(ns.repo)
    head = src / "ac14112"
    files = {
        "yim-n130": ("cert", head / "n130.cert"),
        "yim-n299": ("cert", head / "n299.cert"),
        "yim-n303": ("cert", head / "n303.cert"),
        "yim-n303-first": ("cert", src / "78eb9ea" / "n303.cert"),
        "house-t277-n299": ("corners", repo / WEB / "ozden-s299-upper-bound-2026-11-09/source/n-299-candidate.yaml"),
        "house-t278-n303": ("corners", repo / WEB / "ozden-s303-upper-bound-2026-11-09/source/n-303-candidate.yaml"),
        "house-t259-n130": ("cert", repo / WEB / "mishapolk-issue846-2026-10-30/source/certificates/0000-0999/n130.cert"),
    }
    for n in BH:
        files[f"yim-n{n}"] = ("cert", head / f"n{n}.cert")
        files[f"couzo-n{n}"] = ("cert", repo / WEB / ("couzo-43f666c-2026-10-24" if n == 604 else "couzo-issue763-2026-10-23") / f"source/certificates/best/n{n}.cert")
    out: dict[str, Any] = {"program": "l70_construct.py", "program_digests": C.file_digests(C.CHECKER_FILES + ("l70_construct.py",)), "certificates": {}}
    for label, (fmt, path) in files.items():
        pk = R.read_cert(path) if fmt == "cert" else R.read_corners_yaml(path)
        rec = json.loads((Path(ns.checks) / f"check-{label}.json").read_text())
        pm = [e[3] for e in rec["near_pairs_below_1e-9"]]
        wm = [e[3] for e in rec["near_walls_below_1e-9"]]
        entry = {
            "n": pk.n,
            "side_denominator_digits": len(str(pk.side[1])),
            "turns": turns(pk),
            "pair_margins_below_1e-9": hist(pm),
            "pairs_below_1e-9": len(pm),
            "largest_pair_margin_below_1e-9": max(pm) if pm else None,
            "wall_clearances_below_1e-9": hist(wm),
            "square_wall_pairs_below_1e-9": len(wm),
            "wall_contacts": {w: rec["A"]["walls"][w]["contacts"] for w in C.WALLS},
            "least_wall_clearance": {w: rec["A"]["walls"][w]["least_float"] for w in C.WALLS},
        }
        out["certificates"][label] = entry
        t = entry["turns"]
        print(label, "upright", t["exactly_upright"], "<1e-9", t["turned_below_1e-9_rad"], "to0.5", t["turned_1e-9_rad_to_0.5_deg"], ">0.5", t["turned_beyond_0.5_deg"], ">1", t["turned_beyond_1_deg"], "| pairs<1e-9", len(pm), {k: v for k, v in entry["pair_margins_below_1e-9"].items() if v}, "| walls<1e-9", len(wm), flush=True)
    Path(ns.out).write_text(json.dumps(out, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
