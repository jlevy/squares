"""Lane L163 plan facts: the exact facts the controls plan states its outcomes from.

Usage: l163_plan_facts.py LABEL MAIN.json CHECK.json OUT.json

Decides no modified file. Everything is computed by the closed form of `l163_geom`
(corner projections and corner extents in fractions), apart from both methods; the
check receipt is read only for the verdict and the least margin, which are compared.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction as F  # noqa: E402

import l163_geom as geom  # noqa: E402
from l163_reader import read_json  # noqa: E402

WALLS = ("left", "bottom", "right", "top")
DELTA = F(1, 10**30)
NEAR = F(1, 10**6)


def fr(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


class Pre:
    """Corners and unit normals of each square, from the closed form."""

    def __init__(self, rows: list[geom.Row]) -> None:
        self.rows = rows
        self.corners = [geom.corners(r) for r in rows]
        self.normals = [geom.normals(r) for r in rows]

    def gaps(self, i: int, j: int) -> list[F]:
        pi, pj = self.corners[i], self.corners[j]
        out: list[F] = []
        for w in self.normals[i] + self.normals[j]:
            a = [p[0] * w[0] + p[1] * w[1] for p in pi]
            b = [p[0] * w[0] + p[1] * w[1] for p in pj]
            out.append(max(min(b) - max(a), min(a) - max(b)))
        return out

    def margin(self, i: int, j: int) -> F:
        return max(self.gaps(i, j))


def margins_all(pre: Pre) -> dict[tuple[int, int], F]:
    n = len(pre.rows)
    return {(i, j): pre.margin(i, j) for i in range(n) for j in range(i + 1, n)}


def digest(lines: list[str]) -> str:
    h = hashlib.sha256()
    for s in lines:
        h.update((s + "\n").encode())
    return h.hexdigest()


def main() -> None:
    label, main_json, check_json, out = sys.argv[1:5]
    t0 = time.process_time()
    cert = read_json(main_json)
    with open(check_json, encoding="utf-8") as fh:
        check = json.load(fh)
    rows = list(cert.squares)
    n = cert.n
    side = F(*cert.side)
    rec: dict[str, object] = {"label": label, "lane": "L163", "program": "l163_plan_facts.py", "n": n}
    pre = Pre(rows)
    m = margins_all(pre)
    least = min(m.values())
    rec["least_margin_closed_form"] = fr(least)
    rec["least_margin_equals_check"] = fr(least) == check["main"]["least_margin"]
    rec["pairs_overlapping_or_touching_closed_form"] = sum(1 for v in m.values() if v <= 0)
    clear = [geom.clearances(r, side) for r in rows]
    contacts = [[i + 1, WALLS[w]] for i, cl in enumerate(clear) for w in range(4) if cl[w] == 0]
    rec["contacts_closed_form"] = contacts
    rec["contacts_equal_check"] = contacts == check["main"]["wall_contacts"]
    # side controls
    floor12, ceil12 = geom.floor_value(side, 12), geom.ceil_value(side, 12)
    rec["side"] = {
        "exact": fr(side),
        "floor12": geom.floor_places(side, 12),
        "ceil12": geom.ceil_places(side, 12),
        "S_less_floor12_sci": geom.sci(side - floor12),
        "ceil12_less_S_sci": geom.sci(ceil12 - side),
        "unit_of_last_place": f"1/{side.denominator}",
    }
    rt = [(cl[2], i + 1, "right") for i, cl in enumerate(clear)] + [(cl[3], i + 1, "top") for i, cl in enumerate(clear)]
    pos_rt = sorted(x for x in rt if x[0] > 0)
    rec["least_positive_right_or_top"] = [pos_rt[0][1], pos_rt[0][2], geom.sci(pos_rt[0][0])]
    drops = {
        "S1a": F(1, side.denominator),
        "S1b": DELTA,
        "S1c": side - floor12,
    }
    s1: dict[str, object] = {}
    for name, drop in drops.items():
        crossing = sorted([i, w] for c, i, w in rt if c < drop)
        touching = sorted([i, w] for c, i, w in rt if c == drop)
        s1[name] = {"drop_sci": geom.sci(drop), "crossing": crossing, "touching_after": touching}
    up = ceil12 - side
    s1["S1d"] = {
        "rise_sci": geom.sci(up),
        "crossing": [],
        "contacts_after": [x for x in contacts if x[1] in ("left", "bottom")],
    }
    rec["S1"] = s1
    # S4: the tightest pair, closed along its centre line, with a move shorter than
    # every other margin and every clearance of the moved square
    order = sorted((v, k) for k, v in m.items() if v > 0)
    chosen = None
    tried = 0
    for v, (i, j) in order:
        for mover, other in ((j, i), (i, j)):
            tried += 1
            moved, l2 = geom.close_pair(rows[other], rows[mover], DELTA)
            others = [m[tuple(sorted((mover, k)))] for k in range(n) if k not in (mover, other)]  # pyright: ignore[reportArgumentType]
            nxt = min(others)
            cl = clear[mover]
            ok = all(x > 0 and x * x > l2 for x in others) and all(c > 0 and c * c > l2 for c in cl)
            if ok:
                tau0, g, rates = geom.closing(rows[other], rows[mover], F(0))
                chosen = {
                    "pair": sorted([i + 1, j + 1]),
                    "moving": mover + 1,
                    "toward": other + 1,
                    "margin_sci": geom.sci(v),
                    "move_past_squared_sci": geom.sci(l2),
                    "next_margin_of_mover_sci": geom.sci(nxt),
                    "least_clearance_of_mover_sci": geom.sci(min(cl)),
                    "binding_normals_at_contact": sum(1 for gk, rk in zip(g, rates, strict=True) if rk > 0 and gk / rk == tau0),
                    "tau_contact": fr(tau0),
                    "tau_past": fr(geom.closing(rows[other], rows[mover], DELTA)[0]),
                    "candidates_tried": tried,
                }
                break
        if chosen is not None:
            break
    rec["S4"] = chosen
    # S5: every positive pair below NEAR, closed along its centre line (j toward i)
    near = sorted(k for k, v in m.items() if 0 < v < NEAR)
    lines: list[str] = []
    bind_hist: dict[int, int] = {}
    for i, j in near:
        tc, g, rates = geom.closing(rows[i], rows[j], F(0))
        tp = geom.closing(rows[i], rows[j], DELTA)[0]
        b = sum(1 for gk, rk in zip(g, rates, strict=True) if rk > 0 and gk / rk == tc)
        bind_hist[b] = bind_hist.get(b, 0) + 1
        lines.append(f"{i + 1} {j + 1} {fr(tc)} {fr(tp)}")
    rec["S5"] = {"threshold": "1e-6", "pairs": len(near), "binding_normals_histogram": bind_hist, "closing_times_sha256": digest(lines)}
    # S6: every square to its nearest wall
    s6 = []
    for i, cl in enumerate(clear):
        w = min(range(4), key=lambda k: (cl[k], k))
        s6.append([i + 1, WALLS[w], fr(cl[w])])
    rec["S6"] = {"nearest_wall_counts": {w: sum(1 for x in s6 if x[1] == w) for w in WALLS}, "list_sha256": digest([" ".join(map(str, x)) for x in s6])}
    # G1: square n given square 1's pose
    rec["G1"] = {
        "contacts_square_1": [x[1] for x in contacts if x[0] == 1],
        "contacts_square_n": [x[1] for x in contacts if x[0] == n],
    }
    # G2: square 1 translated by (S, 0)
    moved = geom.translate(rows[0], side, F(0))
    pm = Pre([moved] + rows[1:])
    g2m = [pm.margin(0, k) for k in range(1, n)]
    rec["G2"] = {
        "clearances_moved_sci": [geom.sci(c) for c in geom.clearances(moved, side)],
        "pairs_overlapping": [k + 2 for k, v in enumerate(g2m) if v < 0],
        "pairs_touching": [k + 2 for k, v in enumerate(g2m) if v == 0],
        "least_margin_sci": geom.sci(min(g2m)),
        "contacts_square_1": [x[1] for x in contacts if x[0] == 1],
    }
    # G5: the first left-contact square, t moved by +1e-30 and by -1e-30
    k5 = next(x[0] for x in contacts if x[1] == "left") - 1
    cx, cy, t = geom.parts(rows[k5])
    g5: dict[str, object] = {"square": k5 + 1, "t": fr(t), "contacts_before": [x[1] for x in contacts if x[0] == k5 + 1]}
    for sign, name in ((1, "plus"), (-1, "minus")):
        r5 = geom.row(cx, cy, t + sign * DELTA)
        c5 = geom.clearances(r5, side)
        p5 = Pre([r5] + [rows[k] for k in range(n) if k != k5])
        g5[name] = {
            "clearances": [fr(c) for c in c5],
            "clearances_sci": [geom.sci(c) for c in c5],
            "crossing_walls": [WALLS[w] for w in range(4) if c5[w] < 0],
            "contact_walls": [WALLS[w] for w in range(4) if c5[w] == 0],
            "least_pair_margin_sci": geom.sci(min(p5.margin(0, k) for k in range(1, n))),
        }
    rec["G5"] = g5
    # G6: every t negated
    neg = [geom.row(*geom.parts(r)[:2], -geom.parts(r)[2]) for r in rows]
    pn = Pre(neg)
    mn = margins_all(pn)
    over = sorted(k for k, v in mn.items() if v < 0)
    rec["G6"] = {
        "overlapping_pairs": len(over),
        "touching_pairs": sum(1 for v in mn.values() if v == 0),
        "least_margin_sci": geom.sci(min(mn.values())),
        "least_margin_pair": [x + 1 for x in min(mn, key=lambda k: mn[k])],
        "overlapping_list_sha256": digest([f"{i + 1} {j + 1}" for i, j in over]),
        "clearances_unchanged": [geom.clearances(r, side) for r in neg] == clear,
    }
    # G9, G10: the re-based angles are defined
    ts = [geom.parts(r)[2] for r in rows]
    rec["G9_G10"] = {"t_equal_1": sum(1 for x in ts if x == 1), "t_equal_minus_1": sum(1 for x in ts if x == -1)}
    rec["cpu_seconds"] = round(time.process_time() - t0, 1)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1)
    print(label, "least", geom.sci(least), "S4", chosen and chosen["pair"], "S5", len(near), "G6", len(over), "cpu", rec["cpu_seconds"])


if __name__ == "__main__":
    main()
