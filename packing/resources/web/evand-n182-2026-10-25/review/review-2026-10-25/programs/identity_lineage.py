"""Identity and L-cut lineage of the #806 packing, by optimal assignment.

Written for the stage 4 mathematical review of jlevy/squares issue 806. It decides
nothing about the bound: it measures how far the certificate's squares lie from
other packings' squares, in binary64 (every pose is read exactly and rounded once).

Two measurements:

* Identity: the certificate against each packing at the same count, under the eight
  symmetries of the box, by an optimal one-to-one assignment of squares (scipy's
  linear_sum_assignment) minimising the summed centre distance. Two frames are
  reported, since the boxes differ in side: corner-anchored (each packing in its own
  [0, S]^2) and box-centred (each centred on its own box). For each it counts the
  squares moved beyond 1e-1, 1e-2, 1e-3, 1e-6 and 1e-9, and reports the largest move,
  the largest tilt change (mod 90 degrees), and whether nearest centres pair the
  squares one to one.
* L-cut: the certificate against a packing of 211 squares with an L-shaped strip of
  29 cut away along two walls. For each symmetry g of the 211 box and each corner A
  of the 182 box, the image g(R) is placed with its corner A on the 182 box's corner
  A (the remaining squares stay put, and the strip along the two walls opposite A is
  what is cut), and the 182 squares are assigned optimally to 182 of the 211 (a
  rectangular assignment). The placement with the least summed distance, the
  assignment's own objective, is taken; a count of squares within 1e-3 would pick
  axis-aligned blocks at grid positions, which a unit grid matches under any whole
  shift, so it is reported but not used. For it the program reports the 29 squares left
  unassigned and whether they are the squares near the two cut walls, the moves of
  the 182 with tilted squares apart, and a coarse map of where the moves lie. It
  then compares the 211 packings of one design (T-175, T-181, T-182, T-188) on the
  squares that tell them apart.

Run with the project interpreter in isolated mode, from any directory:

    python3 -I identity_lineage.py --json OUT \
        --cert CERT806 --input INPUT806 --kkt EXACT806 --regularized REG806 \
        --t174 PINGYOU_FACTS_182 --house WITNESS_182 --t098 EVAND_182_CERT \
        --t056 COUZO_FACTS_182 --t188 COUZO_211_CERT --t175 OSTASHEV_211_SQCERT \
        --t182 COUZO_211_T182 --t181 COUZO_211_T181
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import re
import sys
from fractions import Fraction

import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment

TOKEN = re.compile(r"^-?[0-9]+(?:/[0-9]+)?$")
THRESHOLDS = (1e-1, 1e-2, 1e-3, 1e-6, 1e-9)
ANCHORS = ("lower-left", "lower-right", "upper-left", "upper-right")

Pose = tuple[float, float, float]  # x, y, tilt in degrees mod 90


def digest(path: str) -> str:
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def tilt(deg: float) -> float:
    return deg % 90.0


def dtilt(a: float, b: float) -> float:
    d = abs(a - b) % 90.0
    return min(d, 90.0 - d)


def is_tilted(pose: Pose) -> bool:
    return dtilt(pose[2], 0.0) > 1e-6


def read_xyt(path: str) -> tuple[Fraction, list[Pose]]:
    """`x y t` certificates (evand `.cert`, sqcert): exact tokens, t = tan(theta/2)."""
    rows = [ln.split() for ln in open(path, encoding="ascii") if ln.strip() and not ln.lstrip().startswith("#")]
    if rows[0][0] == "n":
        side, body = Fraction(rows[1][1]), rows[2:]
    else:
        side, body = Fraction(rows[0][1]), rows[1:]
    poses = []
    for x, y, t in body:
        for tok in (x, y, t):
            if not TOKEN.match(tok):
                raise ValueError(tok[:40])
        poses.append((float(Fraction(x)), float(Fraction(y)), tilt(math.degrees(2 * math.atan(float(Fraction(t)))))))
    return side, poses


def read_xydeg(path: str) -> tuple[Fraction, list[Pose]]:
    """`n S` then `x y degrees` lines (the binary64 input and the 80-digit KKT point)."""
    rows = [ln.split() for ln in open(path, encoding="ascii") if ln.strip()]
    return Fraction(rows[0][1]), [(float(x), float(y), tilt(float(d))) for x, y, d in rows[1:]]


def read_witness(path: str) -> tuple[Fraction, list[Pose]]:
    """Witness/v2 YAML (optionally gzipped): center-basis rational or center-angle radians."""
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as fh:
        w = yaml.safe_load(fh)["witness"]
    poses = []
    for sq in w["squares"]:
        x, y = (float(Fraction(str(v))) for v in sq["center"])
        if w["representation"] == "center-basis":
            c, s = (float(Fraction(str(v))) for v in sq["basis"])
            deg = math.degrees(math.atan2(s, c))
        elif w["representation"] == "center-angle" and w["coordinates"]["angle_unit"] == "radians":
            deg = math.degrees(float(sq["angle"]))
        else:
            raise ValueError(w["representation"])
        poses.append((x, y, tilt(deg)))
    return Fraction(str(w["side"])), poses


def symmetry(poses: list[Pose], side: float, g: int) -> list[Pose]:
    """The eight symmetries of [0, side]^2; reflections reverse the tilt."""
    out = []
    for x, y, a in poses:
        X, Y, A = {
            0: (x, y, a),
            1: (side - x, y, -a),
            2: (x, side - y, -a),
            3: (side - x, side - y, a),
            4: (y, x, -a),
            5: (side - y, x, a),
            6: (y, side - x, a),
            7: (side - y, side - x, -a),
        }[g]
        out.append((X, Y, tilt(A)))
    return out


def assign(p: list[Pose], r: list[Pose]) -> dict:
    """Optimal assignment of every square of p to a distinct square of r."""
    P = np.array([(x, y) for x, y, _ in p])
    R = np.array([(x, y) for x, y, _ in r])
    cost = np.sqrt(((P[:, None, :] - R[None, :, :]) ** 2).sum(axis=2))
    rows, cols = linear_sum_assignment(cost)
    moves = cost[rows, cols]
    tilts = np.array([dtilt(p[i][2], r[j][2]) for i, j in zip(rows, cols, strict=True)])
    nearest = cost.argmin(axis=1)
    worst = int(moves.argmax())
    return {
        "total": float(moves.sum()),
        "moved_beyond": {f"{t:g}": int((moves > t).sum()) for t in THRESHOLDS},
        "largest_move": float(moves.max()),
        "largest_move_square": int(rows[worst]),
        "largest_move_partner": int(cols[worst]),
        "largest_tilt_change_deg": float(tilts.max()),
        "tilt_changes_beyond_0.1_deg": int((tilts > 0.1).sum()),
        "nearest_centre_one_to_one": bool(len(set(nearest.tolist())) == len(p)),
        "removed": sorted(set(range(len(r))) - {int(j) for j in cols}),
        "map": [[int(i), int(j), float(m)] for i, j, m in zip(rows, cols, moves, strict=True)],
    }


def identity(p: list[Pose], sp: Fraction, r: list[Pose], sr: Fraction) -> dict:
    out: dict = {}
    for frame in ("corner", "centred"):
        best = None
        for g in range(8):
            q = symmetry(p, float(sp), g)
            if frame == "centred":
                hp, hr = float(sp) / 2, float(sr) / 2
                q = [(x - hp + hr, y - hp + hr, a) for x, y, a in q]
            res = assign(q, r)
            res["symmetry"] = g
            if best is None or res["total"] < best["total"]:
                best = res
        assert best is not None
        out[frame] = best
    return out


def placed(r: list[Pose], s211: float, s182: float, g: int, anchor: str) -> list[Pose]:
    """g(R) with its corner `anchor` on the 182 box's corner `anchor`."""
    d = s211 - s182
    dx = -d if anchor.endswith("right") else 0.0
    dy = -d if anchor.startswith("upper") else 0.0
    return [(x + dx, y + dy, a) for x, y, a in symmetry(r, s211, g)]


def cut_wall_distance(pose: Pose, s211: float, anchor: str) -> float:
    """Distance of a centre (in the g frame, before placing) from the two walls opposite the anchor."""
    x, y, _ = pose
    dx = x if anchor.endswith("right") else s211 - x
    dy = y if anchor.startswith("upper") else s211 - y
    return min(dx, dy)


def coincidences(p: list[Pose], res: dict) -> dict:
    moves = {i: m for i, _, m in res["map"]}
    tilted = [i for i in range(len(p)) if is_tilted(p[i])]
    return {
        "all": {f"within_{t:g}": sum(1 for m in moves.values() if m <= t) for t in (1e-9, 1e-6, 1e-4, 1e-3, 1e-2, 1e-1)},
        "tilted": {f"within_{t:g}": sum(1 for i in tilted if moves[i] <= t) for t in (1e-9, 1e-6, 1e-4, 1e-3, 1e-2, 1e-1)},
        "tilted_squares": len(tilted),
    }


def move_map(p: list[Pose], res: dict) -> list[str]:
    """One character per unit cell of the 182 box holding a centre, by its move.

    '.' below 1e-3, 'o' below 1e-1, 'X' beyond; ':', '%', '#' for two centres in a
    cell, by the larger move; rows from the top.
    """
    moves = {i: m for i, _, m in res["map"]}
    cells: dict[tuple[int, int], list[float]] = {}
    for i, (x, y, _) in enumerate(p):
        cells.setdefault((min(int(x), 13), min(int(y), 13)), []).append(moves[i])
    grid = []
    for row in range(13, -1, -1):
        line = ""
        for col in range(14):
            ms = cells.get((col, row))
            if not ms:
                line += " "
                continue
            m = max(ms)
            ch = "." if m < 1e-3 else ("o" if m < 1e-1 else "X")
            line += ch if len(ms) == 1 else {".": ":", "o": "%", "X": "#"}[ch]
        grid.append(line)
    return grid


def lcut(p: list[Pose], sp: Fraction, r: list[Pose], sr: Fraction) -> dict:
    s211, s182 = float(sr), float(sp)
    trials = []
    for g in range(8):
        for anchor in ANCHORS:
            res = assign(p, placed(r, s211, s182, g, anchor))
            within = sum(1 for _, _, m in res["map"] if m <= 1e-3)
            near = sum(1 for _, _, m in res["map"] if m <= 1e-1)
            trials.append((res["total"], g, anchor, within, near, res))
    trials.sort(key=lambda t: t[0])
    _, g, anchor, _, _, best = trials[0]
    img = symmetry(r, s211, g)
    removed = [
        {
            "square_211": j,
            "x": round(img[j][0], 6),
            "y": round(img[j][1], 6),
            "tilt_deg": round(img[j][2], 6),
            "distance_from_cut_walls": round(cut_wall_distance(img[j], s211, anchor), 6),
        }
        for j in best["removed"]
    ]
    strip = {
        f"w={w}": {
            "near_cut_walls": sum(1 for q in img if cut_wall_distance(q, s211, anchor) < w),
            "of_which_removed": sum(1 for s in removed if s["distance_from_cut_walls"] < w),
        }
        for w in (1.0, 1.5, 2.0)
    }
    return {
        "symmetry": g,
        "anchor": anchor,
        "placements": [{"symmetry": t[1], "anchor": t[2], "total": round(t[0], 4), "within_1e-3": t[3], "within_0.1": t[4]} for t in trials],
        "runners_up": [{"symmetry": t[1], "anchor": t[2], "total": round(t[0], 4), "within_1e-3": t[3], "within_0.1": t[4]} for t in trials[1:4]],
        "assignment": best,
        "coincidences": coincidences(p, best),
        "removed_29": removed,
        "strip_at_cut_corner": strip,
        "move_map_rows_top_down": move_map(p, best),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    names = ("cert", "input", "kkt", "regularized", "t174", "house", "t098", "t056", "t188", "t175", "t182", "t181")
    for name in names:
        ap.add_argument(f"--{name}", required=True)
    ap.add_argument("--json", required=True)
    a = ap.parse_args()

    readers = {
        "cert": read_xyt, "regularized": read_xyt, "t098": read_xyt, "t188": read_xyt, "t175": read_xyt, "t182": read_xyt, "t181": read_xyt,
        "input": read_xydeg, "kkt": read_xydeg, "t174": read_witness, "house": read_witness, "t056": read_witness,
    }
    data = {k: readers[k](getattr(a, k)) for k in names}
    sp, p = data["cert"]
    out: dict = {
        "program": "identity_lineage.py",
        "program_sha256": digest(__file__),
        "python": sys.version.split()[0],
        "inputs": {k: {"path": getattr(a, k), "sha256": digest(getattr(a, k)), "n": len(v[1]), "side": str(v[0])} for k, v in data.items()},
    }

    print("Identity: the certificate against packings at 182 (optimal assignment over the 8 symmetries)")
    out["identity"] = {}
    for k in ("input", "kkt", "regularized", "t174", "house", "t098", "t056"):
        sr, r = data[k]
        res = identity(p, sp, r, sr)
        out["identity"][k] = res
        c, m = res["corner"], res["centred"]
        print(f"  {k:<12} side={float(sr):.15f} corner g={c['symmetry']} >0.1:{c['moved_beyond']['0.1']:>3} >1e-3:{c['moved_beyond']['0.001']:>3} >1e-9:{c['moved_beyond']['1e-09']:>3}"
              f" max={c['largest_move']:.4e} tilt-max={c['largest_tilt_change_deg']:.3e} deg nearest-1:1={c['nearest_centre_one_to_one']}"
              f" | centred g={m['symmetry']} >0.1:{m['moved_beyond']['0.1']:>3} >1e-3:{m['moved_beyond']['0.001']:>3} max={m['largest_move']:.4e}")

    print("L-cut: the certificate inside 211 packings with an L of 29 cut away")
    out["lcut"] = {}
    for k in ("t188", "t175", "t182", "t181"):
        sr, r = data[k]
        res = lcut(p, sp, r, sr)
        out["lcut"][k] = res
        b, co = res["assignment"], res["coincidences"]
        print(f"  {k} side={float(sr):.12f}: symmetry {res['symmetry']}, anchored {res['anchor']} (cut at the opposite corner); runners-up {res['runners_up']}")
        print(f"    moved >0.1: {b['moved_beyond']['0.1']}, >1e-2: {b['moved_beyond']['0.01']}, >1e-3: {b['moved_beyond']['0.001']}, >1e-9: {b['moved_beyond']['1e-09']}; largest {b['largest_move']:.4f} (182 square {b['largest_move_square']} to 211 square {b['largest_move_partner']})")
        print(f"    coincidences, all squares: {co['all']}")
        print(f"    coincidences, the {co['tilted_squares']} tilted squares: {co['tilted']}")
        print(f"    211 squares near the two cut walls, and how many the assignment leaves out: {res['strip_at_cut_corner']}")
        far = [s for s in res["removed_29"] if s["distance_from_cut_walls"] >= 1.5]
        print(f"    left out, centre 1.5 or more from the cut walls: {far}")
        if k == "t188":
            print("    move map of the 182 packing (top row first; '.' < 1e-3, 'o' < 0.1, 'X' beyond; ':', '%', '#' two centres):")
            for line in res["move_map_rows_top_down"]:
                print(f"      |{line}|")

    print("The 211 packings of one design against T-188, and what the 182 follows where they differ")
    out["among_211"] = {}
    s188, r188 = data["t188"]
    l188 = out["lcut"]["t188"]
    f188 = placed(r188, float(s188), float(sp), l188["symmetry"], l188["anchor"])
    partner_182 = {j: i for i, j, _ in l188["assignment"]["map"]}
    for k in ("t175", "t182", "t181"):
        sr, r = data[k]
        res = identity(r188, s188, r, sr)
        c = res["corner"]
        moved = sorted(i for i, _, m in c["map"] if m > 0.1)
        moved_3 = sorted(i for i, _, m in c["map"] if m > 1e-3)
        lk = out["lcut"][k]
        fk = placed(r, float(sr), float(sp), lk["symmetry"], lk["anchor"])
        pair = {i: j for i, j, _ in c["map"]}
        rows = []
        for k188 in moved:
            j = pair[k188]
            i182 = partner_182.get(k188)
            row: dict = {"t188_square": k188, f"{k}_square": j, "t188_pose": [round(v, 6) for v in f188[k188]], f"{k}_pose": [round(v, 6) for v in fk[j]]}
            if i182 is None:
                row["182_square"] = None
            else:
                q = p[i182]
                row["182_square"] = i182
                row["182_pose"] = [round(v, 6) for v in q]
                row["distance_to_t188"] = round(math.dist(q[:2], f188[k188][:2]), 6)
                row[f"distance_to_{k}"] = round(math.dist(q[:2], fk[j][:2]), 6)
                row["tilt_change_to_t188_deg"] = round(dtilt(q[2], f188[k188][2]), 4)
                row[f"tilt_change_to_{k}_deg"] = round(dtilt(q[2], fk[j][2]), 4)
            rows.append(row)
        # Squares of the 182 within 1e-9 of one 211 and not of the other, in each one's own best placement.
        mk = {i: m for i, _, m in lk["assignment"]["map"]}
        m188 = {i: m for i, _, m in l188["assignment"]["map"]}
        only_k = sorted(i for i in mk if mk[i] <= 1e-9 < m188[i])
        only_188 = sorted(i for i in m188 if m188[i] <= 1e-9 < mk[i])
        out["among_211"][k] = {
            "t188_vs": {key: c[key] for key in ("symmetry", "moved_beyond", "largest_move")},
            "t188_squares_moved_beyond_0.1": moved,
            "t188_squares_moved_beyond_1e-3": len(moved_3),
            "differing_squares": rows,
            f"182_within_1e-9_of_{k}_not_t188": [[i, [round(v, 4) for v in p[i]], m188[i]] for i in only_k],
            f"182_within_1e-9_of_t188_not_{k}": [[i, [round(v, 4) for v in p[i]], mk[i]] for i in only_188],
        }
        print(f"  T-188 against {k}: symmetry {c['symmetry']}, moved >0.1: {c['moved_beyond']['0.1']}, >1e-3: {c['moved_beyond']['0.001']}, largest {c['largest_move']:.4f}; T-188 squares beyond 0.1: {moved}")
        for row in rows:
            print(f"    {row}")
        print(f"    182 squares within 1e-9 of {k} and not of T-188: {len(only_k)} " + ", ".join(f"{i}@({p[i][0]:.3f},{p[i][1]:.3f},{p[i][2]:.2f}deg; T-188 {m188[i]:.1e})" for i in only_k))
        print(f"    182 squares within 1e-9 of T-188 and not of {k}: {len(only_188)} " + ", ".join(f"{i}@({p[i][0]:.3f},{p[i][1]:.3f},{p[i][2]:.2f}deg; {k} {mk[i]:.1e})" for i in only_188))

    # Compact: the receipt keeps every square-for-square map, which indentation would triple.
    with open(a.json, "w", encoding="utf-8") as fh:
        json.dump(out, fh, separators=(",", ":"))
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
