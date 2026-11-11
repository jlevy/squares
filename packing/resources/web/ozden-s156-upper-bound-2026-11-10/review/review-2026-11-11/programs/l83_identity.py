"""Pose-by-pose lineage of a certificate against its house and its stated seed (review L83).

Usage: python -I -B l83_identity.py N CERT.yaml HOUSE.yaml SEED.yaml OUT.json

Binary64 throughout; it decides nothing. Angles are edge directions modulo 90 degrees in
(-45, 45]; a turn is the change of that direction, a tilt is its size.

Against the house (same n): all eight symmetries of the house's box, anchored at the
lower-left corner and, apart, at the box centres; nearest-centre pairing and SciPy's
optimal assignment of least summed squared move.

Against the seed (another n): the issues' construction cuts a horizontal and a vertical
unit strip out of the seed and closes it up (C+1, Cm), or adds an L of unit squares along
two walls (L-1). So under each symmetry and each cut position (a 0.05 grid), a square of
the new packing is compared with the seed shifted by 0 or 1 in x and y according to its
quadrant (for L-1, by 0 or -1, all squares alike). The score is the count of squares
within 0.05 of a seed square with a turn below 1 degree. The same cut model is run
against the house, as the baseline for what the model alone can match.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial import cKDTree

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l83_check as C  # noqa: E402
import l83_house as H  # noqa: E402
import l83_reader as R  # noqa: E402


def red(a):
    """Angle in degrees reduced to (-45, 45]."""
    r = math.fmod(a, 90.0)
    if r > 45:
        r -= 90
    elif r <= -45:
        r += 90
    return r


def turn(a, b):
    return abs(red(a - b))


def cert_pose(path):
    w = R.read_files(path).witness
    cs, angs = [], []
    for cr in w.corners:
        p = [(x[0] / x[1], y[0] / y[1]) for x, y in cr]
        cs.append(((p[0][0] + p[2][0]) / 2, (p[0][1] + p[2][1]) / 2))
        angs.append(red(math.degrees(math.atan2(p[1][1] - p[0][1], p[1][0] - p[0][0]))))
    return w.side[0] / w.side[1], np.array(cs), np.array(angs)


def ref_pose(path):
    n, side, cs, angs = H.read_float(path)
    return float(side), np.array([[float(x), float(y)] for x, y in cs]), np.array([red(float(a)) for a in angs])


SYMS = []
for swap in (False, True):
    for fx in (False, True):
        for fy in (False, True):
            SYMS.append((swap, fx, fy))


def apply(sym, S, cs, angs):
    swap, fx, fy = sym
    x, y = cs[:, 0].copy(), cs[:, 1].copy()
    a = angs.copy()
    if swap:
        x, y = y, x
        a = 90 - a
    if fx:
        x = S - x
        a = -a
    if fy:
        y = S - y
        a = -a
    return np.stack([x, y], 1), np.array([red(v) for v in a])


def name(sym):
    swap, fx, fy = sym
    if sym == (False, False, False):
        return "identity"
    return ("transpose " if swap else "") + ("flip-x " if fx else "") + ("flip-y" if fy else "")


def against_house(Sc, cc, ca, Sh, hc, ha):
    best = None
    for anchor in ("lower-left", "centre"):
        for sym in SYMS:
            rc, ra = apply(sym, Sh, hc, ha)
            if anchor == "centre":
                rc = rc + (Sc - Sh) / 2
            d2 = ((cc[:, None, :] - rc[None, :, :]) ** 2).sum(2)
            row, col = linear_sum_assignment(d2)
            cost = d2[row, col].sum()
            if best is None or cost < best[0]:
                best = (cost, anchor, sym, rc, ra, row, col, d2)
    cost, anchor, sym, rc, ra, row, col, d2 = best
    nearest = d2.argmin(1)
    moves = np.sqrt(d2[row, col])
    turns = np.array([turn(ca[i], ra[j]) for i, j in zip(row, col)])
    tilt_new = int((np.abs(ca) > 0.5).sum())
    tilt_ref = int((np.abs(ra) > 0.5).sum())
    moved = sorted(((int(i) + 1, int(j) + 1, round(float(m), 4), round(float(t), 3)) for i, j, m, t in zip(row, col, moves, turns) if m > 0.1 or t > 1), key=lambda x: -x[2])
    return {
        "best_symmetry": name(sym),
        "anchor": anchor,
        "nearest_one_to_one": len(set(nearest.tolist())) == len(cc),
        "nearest_distinct": len(set(nearest.tolist())),
        "assignment": {
            "moved_beyond": {t: int((moves > float(t)).sum()) for t in ("1e-9", "1e-6", "1e-3", "0.05", "0.1", "0.25", "0.5")},
            "within_0.05": int((moves <= 0.05).sum()),
            "largest_move": float(moves.max()),
            "turned_beyond_1deg": int((turns > 1).sum()),
            "turned_beyond_1e-6rad": int((turns > math.degrees(1e-6)).sum()),
            "largest_turn": float(turns.max()),
            "same_id": int((row == col).sum()),
        },
        "tilted_beyond_0.5deg": {"new": tilt_new, "house": tilt_ref},
        "tilted_beyond_1deg": {"new": int((np.abs(ca) > 1).sum()), "house": int((np.abs(ra) > 1).sum())},
        "moved_or_turned_beyond_0.1_or_1deg": moved[:80],
    }


def variants(Sc, cc, ca, Sh, hc, ha):
    """The issue's counts under each anchoring and each assignment cost, best symmetry per case."""
    out = {}
    for anchor in ("lower-left", "centre"):
        for costname in ("squared", "linear"):
            best = None
            for sym in SYMS:
                rc, ra = apply(sym, Sh, hc, ha)
                if anchor == "centre":
                    rc = rc + (Sc - Sh) / 2
                d = np.sqrt(((cc[:, None, :] - rc[None, :, :]) ** 2).sum(2))
                m = d**2 if costname == "squared" else d
                row, col = linear_sum_assignment(m)
                cost = m[row, col].sum()
                if best is None or cost < best[0]:
                    best = (cost, sym, row, col, d, ra)
            cost, sym, row, col, d, ra = best
            moves = d[row, col]
            turns = np.array([turn(ca[i], ra[j]) for i, j in zip(row, col)])
            out[f"{anchor}, {costname}"] = {
                "symmetry": name(sym),
                "moved_1e-3": int((moves > 1e-3).sum()),
                "moved_0.05": int((moves > 0.05).sum()),
                "largest_move": round(float(moves.max()), 4),
                "turned_1deg": int((turns > 1).sum()),
                "largest_turn": round(float(turns.max()), 3),
                "moves_within_1e-4_of_0.05": int((np.abs(moves - 0.05) < 1e-4).sum()),
            }
    return out


def cut_model(Sc, cc, ca, Sr, rc0, ra0, kind):
    """Best count of new squares within 0.05 (turn < 1 deg) of a reference square under the cut model."""
    grid = np.arange(0.0, Sc + 0.05, 0.05)
    shifts = [(0, 0), (1, 0), (0, 1), (1, 1)] if kind != "L" else [(0, 0), (-1, 0), (0, -1), (-1, -1)]
    best = None
    for sym in SYMS:
        rc, ra = apply(sym, Sr, rc0, ra0)
        tree = cKDTree(rc)
        ok = []
        for sx, sy in shifts:
            q = cc + np.array([sx, sy], float)
            hits = tree.query_ball_point(q, 0.05)
            ok.append(np.array([any(turn(ca[i], ra[j]) < 1 for j in h) for i, h in enumerate(hits)]))
        ok = np.array(ok)  # 4 x n
        tilted = np.abs(ca) > 0.5
        if kind == "L":
            for k in range(4):
                c = int(ok[k].sum())
                if best is None or c > best[0]:
                    best = (c, int((ok[k] & tilted).sum()), name(sym), shifts[k], None)
            continue
        qx = (cc[:, 0][None, :] >= grid[:, None]).astype(int)  # cuts x n
        qy = (cc[:, 1][None, :] >= grid[:, None]).astype(int)
        for ix in range(len(grid)):
            idx = qx[ix][None, :] + 2 * qy  # cuts_y x n
            sel = ok[idx, np.arange(len(cc))[None, :]]
            counts = sel.sum(1)
            iy = int(counts.argmax())
            c = int(counts[iy])
            if best is None or c > best[0]:
                best = (c, int((sel[iy] & tilted).sum()), name(sym), None, (round(float(grid[ix]), 2), round(float(grid[iy]), 2)))
    c, ct, sym, shift, cut = best
    return {"matched_within_0.05_turn_below_1deg": c, "of_which_tilted": ct, "of_tilted_total": int((np.abs(ca) > 0.5).sum()), "symmetry": sym, "global_shift": shift, "cut_at": cut}


def main(argv):
    n = int(argv[1])
    Sc, cc, ca = cert_pose(Path(argv[2]))
    Sh, hc, ha = ref_pose(Path(argv[3]))
    Ss, sc, sa = ref_pose(Path(argv[4]))
    kind = "L" if n == 180 else "C"
    doc = {
        "n": n,
        "side": Sc,
        "house_side": Sh,
        "seed_n": len(sc),
        "seed_side": Ss,
        "against_house": against_house(Sc, cc, ca, Sh, hc, ha),
        "issue_count_variants": variants(Sc, cc, ca, Sh, hc, ha),
        "cut_model_against_seed": cut_model(Sc, cc, ca, Ss, sc, sa, kind),
        "cut_model_against_house": cut_model(Sc, cc, ca, Sh, hc, ha, kind),
        "tilted_beyond_0.5deg_seed": int((np.abs(sa) > 0.5).sum()),
        "programs": C.program_digests(),
    }
    Path(argv[5]).write_text(json.dumps(doc, indent=1) + "\n")
    h = doc["against_house"]
    print(n, h["best_symmetry"], h["anchor"], "1to1", h["nearest_one_to_one"], h["assignment"]["moved_beyond"], "largest", round(h["assignment"]["largest_move"], 3), "turn>1", h["assignment"]["turned_beyond_1deg"], round(h["assignment"]["largest_turn"], 2), "tilted", h["tilted_beyond_0.5deg"], "sameid", h["assignment"]["same_id"])
    print("   seed", doc["cut_model_against_seed"], "\n   house-cut", doc["cut_model_against_house"])
    for k, v in doc["issue_count_variants"].items():
        print("   ", k, v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
