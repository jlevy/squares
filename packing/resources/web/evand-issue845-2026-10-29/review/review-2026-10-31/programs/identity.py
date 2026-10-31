"""Identity and lineage measurement for review bold-ritchie-rv-daniel (binary64; decides nothing).

usage: identity.py A B [--subset]
  A, B: cert:PATH (evand certificate) or witness:PATH (known-best witness YAML)
  The second may have more squares (--subset): A's squares are then assigned to a subset of B's,
  with A's box anchored at each corner of B's box, under each of the eight symmetries of B's box.

Reports, for the best symmetry (least summed centre distance under the optimal assignment):
nearest-centre one-to-one or not, counts moved beyond 1e-1/1e-2/1e-3/1e-9, the largest move,
the largest turn (mod 90 degrees), and for --subset the unassigned squares of B and their
distances from B's walls.
"""

from __future__ import annotations

import json
import math
import sys

import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment
from scipy.spatial import cKDTree


def frac(s: str) -> float:
    s = str(s).strip()
    if "/" in s:
        a, b = s.split("/")
        return int(a) / int(b) if len(a) < 300 else float(_bigdiv(int(a), int(b)))
    return float(s)


def _bigdiv(a: int, b: int) -> float:
    from fractions import Fraction

    return float(Fraction(a, b))


def load(spec: str):
    kind, path = spec.split(":", 1)
    if kind == "cert":
        rows = []
        side = None
        for line in open(path):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p = line.split()
            if side is None:
                side = frac(p[1])
                continue
            x, y, t = (frac(v) for v in p)
            ang = math.degrees(2 * math.atan(t))
            rows.append((x, y, ang % 90.0))
        return side, np.array(rows)
    if kind == "witness":
        d = yaml.safe_load(open(path))["witness"]
        side = frac(d["side"])
        rows = []
        for sq in d["squares"]:
            x, y = (frac(v) for v in sq["center"])
            if "basis" in sq:
                u = sq["basis"]
                if isinstance(u[0], list):
                    u = u[0]
                ux, uy = frac(u[0]), frac(u[1])
                ang = math.degrees(math.atan2(uy, ux))
            else:
                ang = frac(sq.get("angle", "0"))
            rows.append((x, y, ang % 90.0))
        return side, np.array(rows)
    raise SystemExit(f"unknown spec {spec}")


def sym(P: np.ndarray, S: float, k: int) -> np.ndarray:
    x, y, a = P[:, 0], P[:, 1], P[:, 2]
    if k & 4:
        x, y, a = y, x, -a  # reflect in the diagonal
    if k & 1:
        x, a = S - x, -a
    if k & 2:
        y, a = S - y, -a
    return np.stack([x, y, a % 90.0], axis=1)


def turn(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    d = np.abs(a - b) % 90.0
    return np.minimum(d, 90.0 - d)


def measure(A, SA, B, SB, subset: bool):
    best = None
    anchors = [(0.0, 0.0)]
    if subset:
        dS = SB - SA
        anchors = [(0.0, 0.0), (dS, 0.0), (0.0, dS), (dS, dS)]
    for k in range(8):
        Bk = sym(B, SB, k)
        for ox, oy in anchors:
            Ak = A.copy()
            Ak[:, 0] += ox
            Ak[:, 1] += oy
            D = np.hypot(Ak[:, None, 0] - Bk[None, :, 0], Ak[:, None, 1] - Bk[None, :, 1])
            r, c = linear_sum_assignment(D)
            tot = D[r, c].sum()
            if best is None or tot < best[0]:
                best = (tot, k, (ox, oy), r, c, D, Ak, Bk)
    tot, k, off, r, c, D, Ak, Bk = best
    mv = D[r, c]
    tr = turn(Ak[r, 2], Bk[c, 2])
    # nearest centres one to one (only meaningful for equal n)
    tree = cKDTree(Bk[:, :2])
    _, nn = tree.query(Ak[:, :2])
    one_to_one = (not subset) and len(set(nn.tolist())) == len(nn)
    out = {
        "best_symmetry": k,
        "anchor_offset": off,
        "summed_distance": round(float(tot), 4),
        "nearest_one_to_one": one_to_one,
        "beyond_1e-1": int((mv > 1e-1).sum()),
        "beyond_1e-2": int((mv > 1e-2).sum()),
        "beyond_1e-3": int((mv > 1e-3).sum()),
        "beyond_1e-6": int((mv > 1e-6).sum()),
        "beyond_1e-9": int((mv > 1e-9).sum()),
        "largest_move": float(mv.max()),
        "turned_beyond_0.01deg": int((tr > 0.01).sum()),
        "largest_turn_deg": float(tr.max()),
    }
    if subset:
        left = sorted(set(range(len(Bk))) - set(c.tolist()))
        wall = []
        for j in left:
            x, y = Bk[j, 0], Bk[j, 1]
            wall.append(min(x, y, SB - x, SB - y))
        # which walls: distance to each
        L = Bk[left]
        out["unassigned"] = len(left)
        out["unassigned_max_wall_distance"] = float(max(wall)) if wall else None
        out["unassigned_near_left"] = int((L[:, 0] < 1.5).sum())
        out["unassigned_near_right"] = int((L[:, 0] > SB - 1.5).sum())
        out["unassigned_near_bottom"] = int((L[:, 1] < 1.5).sum())
        out["unassigned_near_top"] = int((L[:, 1] > SB - 1.5).sum())
        out["unassigned_tilted"] = int((np.minimum(L[:, 2], 90 - L[:, 2]) > 1e-6).sum())
    # all-symmetry summary
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    subset = "--subset" in sys.argv
    SA, A = load(args[0])
    SB, B = load(args[1])
    res = {"A": args[0].split("/")[-1], "nA": len(A), "SA": SA, "B": args[1].split("/")[-1], "nB": len(B), "SB": SB}
    res.update(measure(A, SA, B, SB, subset))
    print(json.dumps(res))
