"""Measure a candidate packing pose by pose against the house packing it says it started from.

Usage: oz_identity.py CANDIDATE.yaml HOUSE.yaml HOUSE_SOURCE.cert OUT.json

A measurement in binary64 after exact reading; it decides nothing about the bound.

1. HOUSE.yaml (this repository's centre-basis witness of the house) is checked against the
   house's own source file, Evan Daniel's .cert (centre (x, y), half-angle t, basis
   ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))), exactly, square by square.
2. Under each of the box's eight symmetries the candidate is matched to the house by nearest
   centres (is that map one to one?) and by an optimal assignment (least total centre
   distance, scipy's linear_sum_assignment). Moves and turns are counted at fixed
   thresholds; a square's angle is read modulo 90 degrees and folded into (-45, 45].
3. Tilt counts at several thresholds, the sense of each tilt, and the squares that moved
   beyond a tenth, with where they are.
"""

from __future__ import annotations

import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial import cKDTree

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ozlib as oz  # noqa: E402


def fold(deg: float) -> float:
    """Angle of a square modulo 90 degrees, in (-45, 45]."""
    r = math.fmod(deg, 90.0)
    if r <= -45.0:
        r += 90.0
    elif r > 45.0:
        r -= 90.0
    return r


def poses(doc: dict):
    xs, ys, ang, ids, exact_tilt = [], [], [], [], []
    for sq in doc["squares"]:
        x = oz.to_F(sq["center"][0])
        y = oz.to_F(sq["center"][1])
        a = oz.to_F(sq["basis"][0])
        b = oz.to_F(sq["basis"][1])
        xs.append(float(x))
        ys.append(float(y))
        ang.append(fold(math.degrees(math.atan2(float(b), float(a)))))
        ids.append(sq["id"])
        exact_tilt.append(a * b != 0)
    return np.array(xs), np.array(ys), np.array(ang), ids, exact_tilt


# The eight symmetries of [0, S]^2: (swap, flip_x, flip_y) applied as x' = S - x etc.
SYMS = [(sw, fx, fy) for sw in (False, True) for fx in (False, True) for fy in (False, True)]


def apply(sym, S, xs, ys, ang):
    sw, fx, fy = sym
    x, y = (ys, xs) if sw else (xs, ys)
    a = -ang if sw else ang.copy()
    if fx:
        x = S - x
        a = -a
    if fy:
        y = S - y
        a = -a
    return x, y, np.array([fold(v) for v in a])


def sym_name(sym) -> str:
    sw, fx, fy = sym
    parts = []
    if sw:
        parts.append("x<->y")
    if fx:
        parts.append("x->S-x")
    if fy:
        parts.append("y->S-y")
    return " then ".join(parts) if parts else "identity"


def turn(a, b):
    return np.array([abs(fold(u - v)) for u, v in zip(a, b)])


MOVE_T = [1e-12, 1e-9, 1e-6, 1e-3, 1e-2, 0.05, 0.1, 0.25, 0.5]
TURN_T = [1e-12, 1e-9, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1.0, 5.0, 10.0]
TILT_T = [0.0, 1e-9, 1e-6, 1e-4, 1e-3, 1e-2, 0.05, 0.1, 0.5, 1.0]


def measure(cand, house, S_c):
    cx, cy, ca, cids, _ = cand
    hx, hy, ha, hids, _ = house
    tree = cKDTree(np.column_stack([hx, hy]))
    rows = []
    for sym in SYMS:
        x, y, a = apply(sym, S_c, cx, cy, ca)
        pts = np.column_stack([x, y])
        dist, idx = tree.query(pts)
        one_to_one = len(set(idx.tolist())) == len(idx)
        D = np.sqrt(((pts[:, None, :] - np.column_stack([hx, hy])[None, :, :]) ** 2).sum(-1))
        r, c = linear_sum_assignment(D)
        mv = D[r, c]
        tr = turn(a[r], ha[c])
        rows.append({
            "symmetry": sym_name(sym),
            "nearest_one_to_one": one_to_one,
            "nearest_max": float(dist.max()),
            "assignment_equals_nearest": bool(one_to_one and np.array_equal(idx[r], c)),
            "assignment_total": float(mv.sum()),
            "moved_beyond": {f"{t:g}": int((mv > t).sum()) for t in MOVE_T},
            "within_0.05": int((mv <= 0.05).sum()),
            "max_move": float(mv.max()),
            "turned_beyond_deg": {f"{t:g}": int((tr > t).sum()) for t in TURN_T},
            "turned_beyond_1e-6_rad": int((tr > math.degrees(1e-6)).sum()),
            "max_turn_deg": float(tr.max()),
            "_r": r, "_c": c, "_mv": mv, "_tr": tr, "_a": a,
        })
    return rows


def main() -> int:
    cand_p, house_p, cert_p, out_p = sys.argv[1:5]
    t0 = time.process_time()
    cdoc = oz.read_witness_yaml(cand_p)
    hdoc = oz.read_witness_yaml(house_p)
    cert = oz.read_daniel_cert(cert_p)

    # 1. The house witness against its source certificate, exactly.
    mism = []
    if cert["n"] != len(hdoc["squares"]):
        mism.append("count")
    if oz.to_F(cert["side"]) != oz.to_F(hdoc["header"]["side"]):
        mism.append("side")
    for sq, cs in zip(hdoc["squares"], cert["squares"]):
        if (oz.to_F(sq["center"][0]), oz.to_F(sq["center"][1])) != (cs["x"], cs["y"]):
            mism.append(f"centre {sq['id']}")
        if (oz.to_F(sq["basis"][0]), oz.to_F(sq["basis"][1])) != (cs["a"], cs["b"]):
            mism.append(f"basis {sq['id']}")
    reversed_sense = sum(
        1 for sq, cs in zip(hdoc["squares"], cert["squares"])
        if (oz.to_F(sq["basis"][0]), oz.to_F(sq["basis"][1])) == (cs["a"], -cs["b"]) and cs["b"] != 0)
    house_vs_cert = {
        "cert_sha256": cert["sha256"],
        "cert_header": cert["comments"][:2],
        "house_witness_sha256": hdoc["sha256"],
        "squares_compared": len(cert["squares"]),
        "mismatches": mism[:20],
        "mismatch_count": len(mism),
        "house_equals_cert": not mism,
        "tilted_squares_matching_reversed_sense": reversed_sense,
    }

    S_c = float(oz.to_F(cdoc["header"]["side"]))
    S_h = float(oz.to_F(hdoc["header"]["side"]))
    cand = poses(cdoc)
    house = poses(hdoc)
    rows = measure(cand, house, S_c)
    best = min(rows, key=lambda r: r["assignment_total"])

    # Tilt counts and senses.
    def tilts(p):
        _, _, ang, _, exact = p
        out = {f">{t:g}deg": int((np.abs(ang) > t).sum()) for t in TILT_T}
        out["exact_nonaxis"] = int(sum(exact))
        nz = ang[np.abs(ang) > 1e-9]
        out["positive"] = int((nz > 0).sum())
        out["negative"] = int((nz < 0).sum())
        big = ang[np.abs(ang) > 1.0]
        out["beyond_1deg_positive"] = int((big > 0).sum())
        out["beyond_1deg_negative"] = int((big < 0).sum())
        out["beyond_1deg_range_deg"] = [round(float(big.min()), 4), round(float(big.max()), 4)] if len(big) else None
        out["abs_angle_histogram_deg"] = {
            "(0,1e-6]": int(((np.abs(ang) > 0) & (np.abs(ang) <= 1e-6)).sum()),
            "(1e-6,0.01]": int(((np.abs(ang) > 1e-6) & (np.abs(ang) <= 0.01)).sum()),
            "(0.01,0.1]": int(((np.abs(ang) > 0.01) & (np.abs(ang) <= 0.1)).sum()),
            "(0.1,1]": int(((np.abs(ang) > 0.1) & (np.abs(ang) <= 1)).sum()),
            "(1,10]": int(((np.abs(ang) > 1) & (np.abs(ang) <= 10)).sum()),
            "(10,45]": int((np.abs(ang) > 10).sum()),
        }
        return out

    # Squares that moved or turned most under the best symmetry.
    cx, cy, ca, cids, cex = cand
    hx, hy, ha, hids, hex_ = house
    r, c, mv, tr, a_sym = best["_r"], best["_c"], best["_mv"], best["_tr"], best["_a"]
    movers = []
    for k in np.argsort(-mv):
        if mv[k] <= 0.05:
            break
        i, j = int(r[k]), int(c[k])
        movers.append({
            "candidate": cids[i], "house": hids[j], "move": round(float(mv[k]), 6),
            "candidate_xy": [round(float(cx[i]), 4), round(float(cy[i]), 4)],
            "house_xy": [round(float(hx[j]), 4), round(float(hy[j]), 4)],
            "candidate_deg": round(float(a_sym[i]), 4), "house_deg": round(float(ha[j]), 4),
            "turn_deg": round(float(tr[k]), 4),
        })
    turners = []
    for k in np.argsort(-tr):
        if tr[k] <= 1.0:
            break
        i, j = int(r[k]), int(c[k])
        turners.append({
            "candidate": cids[i], "house": hids[j], "turn_deg": round(float(tr[k]), 4),
            "candidate_deg": round(float(a_sym[i]), 4), "house_deg": round(float(ha[j]), 4),
            "move": round(float(mv[k]), 6), "candidate_xy": [round(float(cx[i]), 4), round(float(cy[i]), 4)],
        })
    # Tilt status changes between paired squares (at the 1e-6 degree threshold).
    newly_axis = [cids[int(r[k])] for k in range(len(r))
                  if abs(a_sym[int(r[k])]) <= 1e-6 < abs(ha[int(c[k])])]
    newly_tilted = [cids[int(r[k])] for k in range(len(r))
                    if abs(ha[int(c[k])]) <= 1e-6 < abs(a_sym[int(r[k])])]
    reversed_tilt = [cids[int(r[k])] for k in range(len(r))
                     if abs(a_sym[int(r[k])]) > 1e-6 and abs(ha[int(c[k])]) > 1e-6
                     and (a_sym[int(r[k])] > 0) != (ha[int(c[k])] > 0)]

    def strip(row):
        return {k: v for k, v in row.items() if not k.startswith("_")}

    order = {
        "assignment_is_same_id": all(cids[int(i)] == hids[int(j)] for i, j in zip(r, c)),
        "same_id_pairs": int(sum(1 for i, j in zip(r, c) if cids[int(i)] == hids[int(j)])),
        "exactly_unchanged_squares": int(sum(
            1 for i, j in zip(r, c)
            if cdoc["squares"][int(i)]["center"] == hdoc["squares"][int(j)]["center"]
            and cdoc["squares"][int(i)]["basis"] == hdoc["squares"][int(j)]["basis"])),
    }
    # Moves by direction for the squares beyond 0.1, to read the source's account of them.
    receipt = {
        "program": "oz_identity.py",
        "program_sha256": oz.sha256_file(__file__),
        "ozlib_sha256": oz.sha256_file(HERE / "ozlib.py"),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "argv": sys.argv[1:],
        "candidate_sha256": cdoc["sha256"],
        "candidate_side": S_c,
        "house_side": S_h,
        "house_vs_source_cert": house_vs_cert,
        "by_symmetry": [strip(rw) for rw in rows],
        "best_symmetry": best["symmetry"],
        "best_order": order,
        "tilts_candidate": tilts(cand),
        "tilts_house": tilts(house),
        "best_moved_beyond_0.05": movers,
        "best_turned_beyond_1deg": turners,
        "tilt_changes_at_1e-6_deg": {
            "tilted_in_house_axis_parallel_here": newly_axis,
            "axis_parallel_in_house_tilted_here": newly_tilted,
            "tilt_sense_reversed": reversed_tilt,
        },
        "decides": "nothing about the bound; a measurement",
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    Path(out_p).write_text(json.dumps(receipt, indent=1) + "\n")
    b = strip(best)
    print(f"{Path(cand_p).name} vs {Path(house_p).name}: house==cert {house_vs_cert['house_equals_cert']}; "
          f"best {b['symmetry']}, one-to-one {b['nearest_one_to_one']}, beyond 0.1: {b['moved_beyond']['0.1']}, "
          f"max move {b['max_move']:.6f}, max turn {b['max_turn_deg']:.3f} deg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
