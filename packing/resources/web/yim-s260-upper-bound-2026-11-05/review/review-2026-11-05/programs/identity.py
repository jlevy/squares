#!/usr/bin/env python3
"""Pose-by-pose identity of #895's packing against T-257's at 260, with the house witness.

A measurement for the review; it decides nothing about the bound.

- Confirms the n-260 house witness is T-257's certificate (same side, same centres, and
  basis vectors equal to (c, s) of the certificate's tangents under the counterclockwise
  sense), which fixes the rotation sense the record reads the format with.
- Under each of the box's eight symmetries (box-centred coordinates), pairs every square
  of the certificate with the nearest centre of T-257's packing and says whether that is
  one to one; takes the optimal assignment (sum of distances, and sum of squared
  distances) for the symmetry that is.
- Measures moves (box-centred and from the lower-left corner), turns (orientation mod 90
  degrees, wrapped to (-45, 45]), tilts beyond 1 degree, exactly upright squares, and the
  near-upright squares' tiny turns.
- Compares the contact graphs of the two packings (separating-axis gaps, every pair and
  wall, by certcheck.py's method A) at several tolerances, under the pairing.
- Lists every square moved beyond 0.01 with its displacement and its contacts in both.

Usage: python -I identity.py --yim CERT --t257 CERT --house WITNESS.yaml --out RECEIPT.json
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import platform
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import mpmath
import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, str(Path(__file__).resolve().parent))
import certcheck as cc  # noqa: E402

mpmath.mp.dps = 60
QUARTER = mpmath.pi / 2
DEG = 180 / mpmath.pi

SYMMETRIES = {
    "identity": ((1, 0), (0, 1)),
    "rot90": ((0, -1), (1, 0)),
    "rot180": ((-1, 0), (0, -1)),
    "rot270": ((0, 1), (-1, 0)),
    "flip_x": ((-1, 0), (0, 1)),
    "flip_y": ((1, 0), (0, -1)),
    "diag": ((0, 1), (1, 0)),
    "antidiag": ((0, -1), (-1, 0)),
}


def phi(t: F):
    """Orientation mod 90 degrees, in (-pi/4, pi/4], radians, high precision."""
    theta = 2 * mpmath.atan(mpmath.mpf(t.numerator) / t.denominator)
    r = mpmath.fmod(theta, QUARTER)
    if r > QUARTER / 2:
        r -= QUARTER
    if r <= -QUARTER / 2:
        r += QUARTER
    return r


def wrap(a):
    while a > QUARTER / 2:
        a -= QUARTER
    while a <= -QUARTER / 2:
        a += QUARTER
    return a


def exactly_upright(t: F) -> bool:
    den = 1 + t * t
    c = (1 - t * t) / den
    s = 2 * t / den
    return c == 0 or s == 0


def load_house(path):
    doc = yaml.safe_load(Path(path).read_text())
    w = doc["witness"]
    out = []
    for sq in w["squares"]:
        cx, cy = (F(str(v)) for v in sq["center"])
        bx, by = (F(str(v)) for v in sq["basis"])
        out.append((cx, cy, bx, by))
    return F(str(w["side"])), out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yim", required=True)
    ap.add_argument("--t257", required=True)
    ap.add_argument("--house", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    t0 = time.time()
    Y = cc.parse_cert(args.yim)
    T = cc.parse_cert(args.t257)
    n = Y["n"]
    out: dict = {"program": "identity.py", "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 "certcheck_sha256": cc.program_digest(), "python": platform.python_version(),
                 "inputs": {"yim": {"path": args.yim, "sha256": Y["sha256"]},
                            "t257": {"path": args.t257, "sha256": T["sha256"]},
                            "house": {"path": args.house,
                                      "sha256": hashlib.sha256(Path(args.house).read_bytes()).hexdigest()}}}

    # ---- the house witness is T-257's certificate, read counterclockwise
    hs, house = load_house(args.house)
    same_side = hs == T["side"]
    same_centres = all(h[0] == s["x"] and h[1] == s["y"] for h, s in zip(house, T["squares"]))
    basis_ccw = basis_cw = basis_same_square = 0
    for h, s in zip(house, T["squares"]):
        u_ccw, _ = cc.frame(s["t"], "ccw")
        u_cw, _ = cc.frame(s["t"], "cw")
        basis_ccw += (h[2], h[3]) == u_ccw
        basis_cw += (h[2], h[3]) == u_cw
        # the same square: basis equal to one of the four edge directions of the ccw square
        v = (-u_ccw[1], u_ccw[0])
        dirs = {u_ccw, v, (-u_ccw[0], -u_ccw[1]), (-v[0], -v[1])}
        basis_same_square += (h[2], h[3]) in dirs
    out["house_witness"] = {"squares": len(house), "same_side": same_side, "same_centres_in_order": same_centres,
                            "basis_equals_ccw_u": basis_ccw, "basis_equals_cw_u": basis_cw,
                            "basis_is_an_edge_direction_of_the_ccw_square": basis_same_square}

    # ---- orientations
    py = [phi(s["t"]) for s in Y["squares"]]
    pt = [phi(s["t"]) for s in T["squares"]]
    one_deg = mpmath.pi / 180
    tilt_y = [i for i in range(n) if abs(py[i]) > one_deg]
    tilt_t = [i for i in range(n) if abs(pt[i]) > one_deg]
    near_y = [i for i in range(n) if abs(py[i]) <= one_deg]
    near_t = [i for i in range(n) if abs(pt[i]) <= one_deg]
    up_y = [i for i in range(n) if exactly_upright(Y["squares"][i]["t"])]
    up_t = [i for i in range(n) if exactly_upright(T["squares"][i]["t"])]
    tiny = [i for i in near_y if -1.40e-10 <= float(py[i] * DEG) <= -1.34e-10]
    tiny_tangents = collections.Counter(Y["squares"][i]["t"] for i in tiny)
    near_y_other = sorted(((float(py[i] * DEG), i + 1, str(Y["squares"][i]["t"])) for i in near_y if i not in tiny))
    near_t_other = sorted(((float(pt[i] * DEG), i + 1, str(T["squares"][i]["t"])) for i in near_t if i not in up_t))
    t_counts = collections.Counter(str(s["t"]) for s in T["squares"])
    tilt_sign_y = collections.Counter("positive" if py[i] > 0 else "negative" for i in tilt_y)
    tilt_sign_t = collections.Counter("positive" if pt[i] > 0 else "negative" for i in tilt_t)
    out["orientations"] = {
        "yim_tilted_beyond_1_degree": len(tilt_y), "t257_tilted_beyond_1_degree": len(tilt_t),
        "yim_tilt_signs": dict(tilt_sign_y), "t257_tilt_signs": dict(tilt_sign_t),
        "yim_within_1_degree": len(near_y), "t257_within_1_degree": len(near_t),
        "yim_exactly_upright": len(up_y), "t257_exactly_upright": len(up_t),
        "t257_exactly_upright_t0": t_counts.get("0", 0), "t257_exactly_upright_t1": t_counts.get("1", 0),
        "t257_exactly_upright_tminus1": t_counts.get("-1", 0),
        "yim_near_upright_turned_-1.40e-10_to_-1.34e-10_degrees": len(tiny),
        "their_distinct_tangents": len(tiny_tangents),
        "their_commonest_tangent": [str(tiny_tangents.most_common(1)[0][0]), tiny_tangents.most_common(1)[0][1]],
        "their_turn_degrees_range": [min(float(py[i] * DEG) for i in tiny), max(float(py[i] * DEG) for i in tiny)],
        "their_turn_radians_range": [min(float(py[i]) for i in tiny), max(float(py[i]) for i in tiny)],
        "yim_other_near_upright": near_y_other,
        "t257_other_near_upright_not_exact": near_t_other,
        "yim_distinct_tangents": len({str(s["t"]) for s in Y["squares"]}),
        "t257_distinct_tangents": len(t_counts),
    }

    # ---- symmetries and nearest centres, box-centred
    hy, ht = Y["side"] / 2, T["side"] / 2
    cy = np.array([[float(s["x"] - hy), float(s["y"] - hy)] for s in Y["squares"]])
    ct = np.array([[float(s["x"] - ht), float(s["y"] - ht)] for s in T["squares"]])
    sym_report = {}
    for name, M in SYMMETRIES.items():
        m = np.array(M, dtype=float)
        mapped = cy @ m.T
        d = np.linalg.norm(mapped[:, None, :] - ct[None, :, :], axis=2)
        nearest = d.argmin(axis=1)
        one_to_one = len(set(nearest.tolist())) == n
        r, c = linear_sum_assignment(d)
        moves = d[r, c]
        sym_report[name] = {"nearest_one_to_one": one_to_one, "nearest_distinct": len(set(nearest.tolist())),
                            "assignment_sum": float(moves.sum()), "assignment_max": float(moves.max()),
                            "assignment_beyond_0.1": int((moves > 0.1).sum())}
    out["symmetries"] = sym_report

    # ---- the identity pairing, exact displacements
    d = np.linalg.norm(cy[:, None, :] - ct[None, :, :], axis=2)
    nearest = d.argmin(axis=1)
    r1, c1 = linear_sum_assignment(d)
    r2, c2 = linear_sum_assignment(d**2)
    pairing = {int(i): int(j) for i, j in zip(r1, c1)}
    out["pairing"] = {
        "nearest_equals_assignment_sum": all(pairing[i] == int(nearest[i]) for i in range(n)),
        "assignment_sum_equals_assignment_squares": all(pairing[int(i)] == int(j) for i, j in zip(r2, c2)),
        "pairing_is_row_order": all(pairing[i] == i for i in range(n)),
        "rows_paired_off_order": sum(1 for i in range(n) if pairing[i] != i),
    }
    moves_c, moves_raw, turns = [], [], []
    for i in range(n):
        j = pairing[i]
        a, b = Y["squares"][i], T["squares"][j]
        dxc = (a["x"] - hy) - (b["x"] - ht)
        dyc = (a["y"] - hy) - (b["y"] - ht)
        dxr = a["x"] - b["x"]
        dyr = a["y"] - b["y"]
        moves_c.append((mpmath.sqrt(mpmath.mpf(dxc.numerator) / dxc.denominator * mpmath.mpf(dxc.numerator) / dxc.denominator
                                    + mpmath.mpf(dyc.numerator) / dyc.denominator * mpmath.mpf(dyc.numerator) / dyc.denominator),
                        float(dxc), float(dyc)))
        moves_raw.append(mpmath.sqrt((mpmath.mpf(dxr.numerator) / dxr.denominator) ** 2
                                     + (mpmath.mpf(dyr.numerator) / dyr.denominator) ** 2))
        turns.append(wrap(py[i] - pt[j]))
    thresholds = [1e-1, 1e-2, 1e-3, 1e-4, 1e-6, 1e-8, 1e-9, 1e-10]
    out["moves"] = {
        "box_centred": {f"beyond_{t:g}": sum(1 for m in moves_c if m[0] > t) for t in thresholds},
        "from_lower_left": {f"beyond_{t:g}": sum(1 for m in moves_raw if m > t) for t in thresholds},
        "largest_box_centred": float(max(m[0] for m in moves_c)),
        "largest_at_row": 1 + max(range(n), key=lambda i: moves_c[i][0]),
        "least_box_centred": float(min(m[0] for m in moves_c)),
        "least_from_lower_left": float(min(moves_raw)),
    }
    out["turns"] = {
        "beyond_1e-6_rad": sum(1 for x in turns if abs(x) > 1e-6),
        "beyond_1e-9_rad": sum(1 for x in turns if abs(x) > 1e-9),
        "beyond_1e-11_rad": sum(1 for x in turns if abs(x) > 1e-11),
        "largest_degrees": float(max(abs(x) for x in turns) * DEG),
        "beyond_1e-6": sorted(((float(turns[i] * DEG), i + 1, pairing[i] + 1) for i in range(n) if abs(turns[i]) > 1e-6),
                              key=lambda z: -abs(z[0])),
        "tilt_class_changes": [(i + 1, pairing[i] + 1, float(py[i] * DEG), float(pt[pairing[i]] * DEG))
                               for i in range(n) if (abs(py[i]) > one_deg) != (abs(pt[pairing[i]]) > one_deg)],
    }
    # the near-upright squares' tiny turn against T-257's poses
    tiny_vs_t = collections.Counter(
        "t257 exactly upright" if exactly_upright(T["squares"][pairing[i]]["t"]) else "t257 not exactly upright"
        for i in tiny)
    out["orientations"]["tiny_turn_squares_against_t257"] = dict(tiny_vs_t)

    # ---- contact graphs
    gy = cc.decide(Y, "ccw", "A")
    gt = cc.decide(T, "ccw", "A")
    gapy, gapt = gy["_gaps"], gt["_gaps"]
    wally, wallt = gy["_walls"], gt["_walls"]
    inverse = {j: i for i, j in pairing.items()}
    contacts = {}
    for tol in ("1e-14", "1e-12", "1e-11", "1e-10", "1e-9", "1e-8", "1e-7", "1e-6", "1e-4"):
        tau = F(tol)
        cy_set = {tuple(sorted((pairing[i], pairing[j]))) for (i, j), g in gapy.items() if g <= tau}
        ct_set = {(i, j) for (i, j), g in gapt.items() if g <= tau}
        wy = {(pairing[i], w) for i in range(n) for w in range(4) if wally[i][w] <= tau}
        wt = {(i, w) for i in range(n) for w in range(4) if wallt[i][w] <= tau}
        contacts[tol] = {"yim_pair_contacts": len(cy_set), "t257_pair_contacts": len(ct_set),
                         "pair_contacts_in_both": len(cy_set & ct_set),
                         "only_yim": len(cy_set - ct_set), "only_t257": len(ct_set - cy_set),
                         "yim_wall_contacts": len(wy), "t257_wall_contacts": len(wt),
                         "wall_contacts_in_both": len(wy & wt)}
    out["contacts"] = contacts

    def decades(gaps):
        hist = collections.Counter()
        for g in gaps:
            if g < 0:
                hist["negative"] += 1
            elif g == 0:
                hist["zero"] += 1
            else:
                e = int(mpmath.floor(mpmath.log10(mpmath.mpf(g.numerator) / g.denominator)))
                if e < -1:
                    hist[f"[1e{e},1e{e + 1})"] += 1
                else:
                    hist[">=0.1"] += 1
        return dict(hist)

    out["gap_decades"] = {"yim_pairs": decades(gapy.values()), "t257_pairs": decades(gapt.values()),
                          "yim_walls": decades([w for ws in wally for w in ws]),
                          "t257_walls": decades([w for ws in wallt for w in ws])}

    # ---- the movers beyond 0.01
    def nbrs(gaps, walls, k, tau):
        out_n = []
        for (i, j), g in gaps.items():
            if g <= tau and k in (i, j):
                out_n.append(j if i == k else i)
        out_w = [w for w in range(4) if walls[k][w] <= tau]
        return sorted(out_n), out_w

    tau = F(1, 10**8)
    movers = []
    for i in sorted(range(n), key=lambda i: -moves_c[i][0]):
        if moves_c[i][0] <= 0.01:
            break
        j = pairing[i]
        ny_, wy_ = nbrs(gapy, wally, i, tau)
        nt_, wt_ = nbrs(gapt, wallt, j, tau)
        movers.append({
            "yim_row": i + 1, "t257_row": j + 1,
            "move": float(moves_c[i][0]), "dx": moves_c[i][1], "dy": moves_c[i][2],
            "yim_centre": [float(Y["squares"][i]["x"]), float(Y["squares"][i]["y"])],
            "t257_centre": [float(T["squares"][j]["x"]), float(T["squares"][j]["y"])],
            "yim_tilt_deg": float(py[i] * DEG), "t257_tilt_deg": float(pt[j] * DEG),
            "turn_deg": float(turns[i] * DEG),
            "yim_contacts_1e-8": [pairing[k] + 1 for k in ny_], "yim_walls_1e-8": wy_,
            "t257_contacts_1e-8": [k + 1 for k in nt_], "t257_walls_1e-8": wt_,
        })
    out["movers_beyond_0.01"] = movers
    out["note_rows"] = "rows are 1-based row numbers in each file (row k is on line k + 2); contacts are T-257 rows"
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out["cpu_seconds_total"] = round(usage.ru_utime + usage.ru_stime, 3)
    out["wall_seconds"] = round(time.time() - t0, 3)
    Path(args.out).write_text(json.dumps(out, indent=1, default=str) + "\n")
    brief = {k: out[k] for k in ("house_witness", "symmetries", "pairing", "moves", "contacts")}
    print(json.dumps(brief, indent=1, default=str))
    o = dict(out["orientations"])
    o.pop("yim_other_near_upright")
    o.pop("t257_other_near_upright_not_exact")
    print(json.dumps(o, indent=1, default=str))
    print(json.dumps({k: v for k, v in out["turns"].items()}, default=str))
    print("cpu", out["cpu_seconds_total"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
