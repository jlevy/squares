"""Write the L70 controls addendum: S4 and S7 restated, before any of it runs.

The frozen plan's S4c/S4p said exactly the least pair touches (overlaps); where the
moved square has another neighbour at the same gap along the same axis, more pairs
close with it (the n130 trial). Its S7 expected the methods to agree on containment;
method B's containment criterion (clipped area exactly 1) presumes the unit-square
test it runs first, so it calls a refused enlarged square outside as well.

S4' states the touching and overlapping sets exactly, from the centre half-width
formula (margin = max_w |w.d| - T over the pair's four edge normals), computed here
for every pair of the moved square. S7' states method A's and method B's containment
separately.

Usage: python -I l70_plan_addendum.py --src SRC --plan controls-plan.json --out controls-plan-addendum.json
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from typing import Any

EPS = F(1, 10**30)
TOKENS = ("left", "bottom", "right", "top")


def parse_rows(path: Path) -> tuple[F, list[tuple[F, F, F]]]:
    lines = path.read_text(encoding="utf-8").split("\n")[:-1]
    body = [ln for ln in lines if not ln.startswith("#")]
    side = F(body[0].split(" ")[1])
    rows = [tuple(F(t) for t in ln.split(" ")) for ln in body[1:]]
    return side, rows  # type: ignore[return-value]


def basis(t: F) -> tuple[F, F]:
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def margin(ri: tuple[F, F, F], rj: tuple[F, F, F]) -> F:
    c1, s1 = basis(ri[2])
    c2, s2 = basis(rj[2])
    dx, dy = rj[0] - ri[0], rj[1] - ri[1]
    t_half = (1 + abs(c1 * c2 + s1 * s2) + abs(c1 * s2 - s1 * c2)) / 2
    m = max(abs(c1 * dx + s1 * dy), abs(-s1 * dx + c1 * dy), abs(c2 * dx + s2 * dy), abs(-s2 * dx + c2 * dy))
    return m - t_half


def _factor(ri: tuple[F, F, F], rj: tuple[F, F, F]) -> F:
    c1, s1 = basis(ri[2])
    c2, s2 = basis(rj[2])
    dx, dy = rj[0] - ri[0], rj[1] - ri[1]
    t_half = (1 + abs(c1 * c2 + s1 * s2) + abs(c1 * s2 - s1 * c2)) / 2
    m = max(abs(c1 * dx + s1 * dy), abs(-s1 * dx + c1 * dy), abs(c2 * dx + s2 * dy), abs(-s2 * dx + c2 * dy))
    return t_half / m


def clearances(r: tuple[F, F, F], side: F) -> list[F]:
    c, s = basis(r[2])
    h = (abs(c) + abs(s)) / 2
    return [r[0] - h, r[1] - h, side - r[0] - h, side - r[1] - h]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()
    src = Path(ns.src)
    plan = json.loads(Path(ns.plan).read_text())
    out: dict[str, Any] = {
        "addendum": "S4' and S7', stated before any of them runs, after the frozen plan's S4c/S4p and S7 missed on the n130 trial",
        "definitions": {
            "touching and overlapping sets": "every pair (j, k) of the moved square j whose margin max_w |w.d| - T is 0 (touching) or negative (overlapping) after the move, exact; no other pair changes",
            "S7' containment": "method A: the enlarged square's corners against the walls (outside only if a clearance is below 1e-30 h); method B: clipped area exactly 1, which a square of area (1 + 1e-30)^2 cannot keep, so B reports it outside",
        },
        "files": {},
    }
    for label, entry in plan["files"].items():
        path = src / entry["input"]
        side, rows = parse_rows(path)
        ids = [str(k + 1) for k in range(len(rows))]
        s4 = next(c for c in entry["controls"] if c["id"] == "S4c")
        i, j = s4["what"].split("(")[1].split(")")[0].split(", ")
        ki, kj = ids.index(i), ids.index(j)
        lam = _factor(rows[ki], rows[kj])
        expect: dict[str, Any] = {}
        for tag, f in (("contact", lam), ("past", lam * (1 - EPS))):
            ri, rj = rows[ki], rows[kj]
            moved = (ri[0] + f * (rj[0] - ri[0]), ri[1] + f * (rj[1] - ri[1]), rj[2])
            touch, over = [], []
            for k, rk in enumerate(rows):
                if k == kj:
                    continue
                m = margin(rk, moved)
                pair = sorted([ids[k], j], key=int)
                if m == 0:
                    touch.append(pair)
                elif m < 0:
                    over.append(pair)
            outside = [j] if min(clearances(moved, side)) < 0 else []
            expect[tag] = {"touching_pairs": sorted(touch, key=lambda p: (int(p[0]), int(p[1]))), "overlapping_pairs": sorted(over, key=lambda p: (int(p[0]), int(p[1]))), "outside": outside}
        s7 = next(c for c in entry["controls"] if c["id"] == "S7")
        si = s7["what"].split("square ")[1].split(" ")[0]
        r = rows[ids.index(si)]
        c, s = basis(r[2])
        h = (abs(c) + abs(s)) / 2
        a_out = [si] if min(clearances(r, side)) < EPS * h else []
        out["files"][label] = {
            "input": entry["input"],
            "input_sha256": entry["input_sha256"],
            "controls": [
                {"id": "S4'c", "level": "whole-file", "what": f"the least-margin pair ({i}, {j}) closed along its centre line to contact (square {j} moved), as S4c",
                 "expect": {"verdict": "ACCEPT" if not expect["contact"]["overlapping_pairs"] and not expect["contact"]["outside"] else "REFUSE", **expect["contact"]}},
                {"id": "S4'p", "level": "whole-file", "what": f"the same, 1e-30 past, as S4p",
                 "expect": {"verdict": "REFUSE", **expect["past"]}},
                {"id": "S7'", "level": "whole-file", "what": f"square {si} (as four corners) enlarged by 1 + 1e-30 about its centre, as S7",
                 "expect": {"verdict": "REFUSE", "not_unit": [si], "outside_A": a_out, "outside_B": [si], "overlapping_pairs": []}},
            ],
        }
        print(label, "S4'c touch", expect["contact"]["touching_pairs"], "| S4'p overlap", expect["past"]["overlapping_pairs"], "| S7' A out", a_out)
    Path(ns.out).write_text(json.dumps(out, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
