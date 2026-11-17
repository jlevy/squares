"""Pose-by-pose identity of the new packings against the houses, T-257, their inputs and views.

Usage (from packing/, Python 3.14):
  python -I identity.py CANDIDATES_DIR HOUSES_DIR SLACK.json OUT.json

A measurement in binary64 of exactly read poses; it decides nothing about any bound.
Each reference packing is mapped by each of the box's eight symmetries in its own box
(side S_ref), and for each symmetry this program measures:
  * whether nearest centres pair the squares one to one;
  * the assignment minimizing the total squared centre displacement, by this program's
    own Hungarian algorithm (shortest augmenting paths), cross-checked against
    scipy.optimize.linear_sum_assignment's optimal cost;
  * under the symmetry with the least total, the squares moved beyond 1e-9, 1e-3, 1e-2,
    0.1 and 0.5, the largest move and the RMS move, the squares turned beyond 1 degree
    (angles compared modulo 90 degrees), the squares tilted beyond 1 degree in each
    packing, the tilts reversed, and, with SLACK.json, the contact pairs (exact gap
    below 1e-9) shared, only in the new packing and only in the reference;
  * the same counts with centres measured from each box's centre (box-centred), which
    discounts the difference of the two sides.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cert_reader import read_cert  # noqa: E402

NAMES = {175: "s175_1105", 204: "s204_trig1", 260: "s260_ks_1105", 268: "s268_1105", 293: "s293_1105", 303: "s303_1105", 304: "s304_1105"}
HOUSE_T = {175: "T-186", 204: "T-264", 260: "T-265", 268: "T-242", 293: "T-257", 303: "T-240", 304: "T-242"}
SYMS = ["identity", "mirror x", "mirror y", "rotation 180", "transpose", "anti-transpose", "rotation 90", "rotation 270"]


def frac(s) -> F:
    s = str(s)
    p, _, q = s.partition("/")
    return F(int(p), int(q or 1))


def mod90(a: np.ndarray) -> np.ndarray:
    """Reduce degrees into (-45, 45]."""
    r = np.mod(a + 45.0, 90.0) - 45.0
    r[r == -45.0] = 45.0
    return r


def from_cert(path: Path) -> dict:
    c = read_cert(path)
    xs = np.array([float(q[0]) for q in c["squares"]])
    ys = np.array([float(q[1]) for q in c["squares"]])
    th = np.array([math.degrees(2 * math.atan(float(q[2]))) for q in c["squares"]])
    return {"S": float(c["S"]), "x": xs, "y": ys, "a": mod90(th), "n": c["n"]}


def from_witness(path: Path) -> dict:
    doc = yaml.load(path.read_text(), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    w = doc["witness"]
    xs, ys, th = [], [], []
    for item in w["squares"]:
        x, y = (frac(v) for v in item["center"])
        c, s = (frac(v) for v in item["basis"])
        xs.append(float(x))
        ys.append(float(y))
        th.append(math.degrees(math.atan2(float(s), float(c))))
    return {"S": float(frac(w["side"])), "x": np.array(xs), "y": np.array(ys), "a": mod90(np.array(th)), "n": w["n"]}


def from_points(path: Path) -> dict:
    rows = [r for r in path.read_text().split("\n") if r.strip()]
    n, s = rows[0].split()
    xs, ys, th = [], [], []
    for r in rows[1:]:
        a, b, c = r.split()
        xs.append(float(a))
        ys.append(float(b))
        th.append(float(c))
    return {"S": float(s), "x": np.array(xs), "y": np.array(ys), "a": mod90(np.array(th)), "n": int(n)}


def apply(sym: int, p: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    S, x, y, a = p["S"], p["x"], p["y"], p["a"]
    if sym == 0:
        return x, y, a
    if sym == 1:
        return S - x, y, mod90(-a)
    if sym == 2:
        return x, S - y, mod90(-a)
    if sym == 3:
        return S - x, S - y, a
    if sym == 4:
        return y, x, mod90(-a)
    if sym == 5:
        return S - y, S - x, mod90(-a)
    if sym == 6:
        return S - y, x, a
    if sym == 7:
        return y, S - x, a
    raise ValueError(sym)


def hungarian(cost: np.ndarray) -> np.ndarray:
    """Minimum-cost perfect assignment, rows to columns (shortest augmenting paths)."""
    n = cost.shape[0]
    inf = float("inf")
    u = np.zeros(n + 1)
    v = np.zeros(n + 1)
    p = np.zeros(n + 1, dtype=np.int64)
    way = np.zeros(n + 1, dtype=np.int64)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = np.full(n + 1, inf)
        used = np.zeros(n + 1, dtype=bool)
        while True:
            used[j0] = True
            i0 = p[j0]
            cur = cost[i0 - 1, :] - u[i0] - v[1:]
            free = ~used[1:]
            upd = free & (cur < minv[1:])
            mv1 = minv[1:]
            mv1[upd] = cur[upd]
            w1 = way[1:]
            w1[upd] = j0
            masked = np.where(free, mv1, inf)
            j1 = int(np.argmin(masked)) + 1
            delta = masked[j1 - 1]
            used_idx = np.nonzero(used)[0]
            u[p[used_idx]] += delta
            v[used_idx] -= delta
            mv1[free] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    ans = np.zeros(n, dtype=np.int64)
    for j in range(1, n + 1):
        ans[p[j] - 1] = j - 1
    return ans


def compare(new: dict, ref: dict, new_contacts=None, ref_contacts=None, syms=range(8)) -> dict:
    n = new["n"]
    assert ref["n"] == n
    out: dict = {"per_symmetry": {}}
    best = None
    for k in syms:
        rx, ry, ra = apply(k, ref)
        dx = new["x"][:, None] - rx[None, :]
        dy = new["y"][:, None] - ry[None, :]
        d2 = dx * dx + dy * dy
        nearest = np.argmin(d2, axis=1)
        one_to_one = len(set(nearest.tolist())) == n
        assign = hungarian(d2)
        r_, c_ = linear_sum_assignment(d2)
        own = float(d2[np.arange(n), assign].sum())
        sci = float(d2[r_, c_].sum())
        if abs(own - sci) > 1e-9 * max(1.0, sci):
            raise AssertionError(f"Hungarian disagrees with scipy: {own} vs {sci}")
        ent = {"nearest_one_to_one": one_to_one, "nearest_distinct_targets": len(set(nearest.tolist())), "total_squared": own}
        out["per_symmetry"][SYMS[k]] = ent
        if best is None or own < best[1]:
            best = (k, own, assign, rx, ry, ra)
    k, own, assign, rx, ry, ra = best
    moves = np.hypot(new["x"] - rx[assign], new["y"] - ry[assign])
    turn = np.abs(mod90(new["a"] - ra[assign]))
    tilted_new = np.abs(new["a"]) > 1.0
    tilted_ref = np.abs(ra[assign]) > 1.0
    reversed_ = int(np.sum(tilted_new & tilted_ref & (np.sign(new["a"]) != np.sign(ra[assign]))))
    res = {
        "best_symmetry": SYMS[k],
        "best_total_squared": own,
        "best_nearest_one_to_one": out["per_symmetry"][SYMS[k]]["nearest_one_to_one"],
        "any_symmetry_one_to_one": [s for s, e in out["per_symmetry"].items() if e["nearest_one_to_one"]],
        "assignment_is_row_identity": bool(np.all(assign == np.arange(n))),
        "within_1e-9": int(np.sum(moves <= 1e-9)),
        "within_1e-3": int(np.sum(moves <= 1e-3)),
        "beyond_1e-2": int(np.sum(moves > 1e-2)),
        "beyond_0.1": int(np.sum(moves > 0.1)),
        "beyond_0.5": int(np.sum(moves > 0.5)),
        "largest_move": float(moves.max()),
        "largest_move_square": int(np.argmax(moves)) + 1,
        "rms_move": float(np.sqrt(np.mean(moves**2))),
        "turned_beyond_1_degree": int(np.sum(turn > 1.0)),
        "largest_turn_degrees": float(turn.max()),
        "tilted_beyond_1_degree_new": int(np.sum(np.abs(new["a"]) > 1.0)),
        "tilted_beyond_1_degree_ref": int(np.sum(np.abs(ref["a"]) > 1.0)),
        "tilts_reversed": reversed_,
    }
    # box-centred
    ox, oy = new["x"] - new["S"] / 2, new["y"] - new["S"] / 2
    bx, by = rx - ref["S"] / 2, ry - ref["S"] / 2
    d2c = (ox[:, None] - bx[None, :]) ** 2 + (oy[:, None] - by[None, :]) ** 2
    ac = hungarian(d2c)
    mc = np.hypot(ox - bx[ac], oy - by[ac])
    res["box_centred"] = {
        "nearest_one_to_one": len(set(np.argmin(d2c, axis=1).tolist())) == n,
        "beyond_1e-2": int(np.sum(mc > 1e-2)),
        "beyond_0.1": int(np.sum(mc > 0.1)),
        "largest_move": float(mc.max()),
    }
    if new_contacts is not None and ref_contacts is not None:
        ref_set = {tuple(sorted(c)) for c in ref_contacts}
        mapped = {tuple(sorted((int(assign[i - 1]) + 1, int(assign[j - 1]) + 1))) for i, j in new_contacts}
        res["contacts"] = {
            "new": len(new_contacts),
            "ref": len(ref_set),
            "shared": len(mapped & ref_set),
            "only_new": len(mapped - ref_set),
            "only_ref": len(ref_set - mapped),
        }
    out["best"] = res
    return out


def main() -> None:
    cand, houses, slack_path, out_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    slack = json.loads(slack_path.read_text())
    result: dict = {}
    for n, name in NAMES.items():
        new = from_cert(cand / f"{name}.cert")
        house = from_witness(houses / f"W-known-best-n{n}.yaml")
        r = {}
        r[f"certificate vs house {HOUSE_T[n]} (main's W-known-best-n{n})"] = compare(
            new, house, slack[f"new {n}"]["contacts"], slack[f"house {n}"]["contacts"])
        inp = from_points(cand / f"{name}.input.txt")
        r["certificate vs its binary64 input"] = compare(new, inp, syms=[0])
        view = cand / f"{name}_regularized.cert"
        if view.exists():
            v = from_cert(view)
            r["view vs certificate"] = compare(v, new)
            r["view vs house"] = compare(v, house)
        if n == 260:
            t257 = from_cert(houses / "T-257-s260_1028.cert")
            r["certificate vs T-257's 260 (s260_1028.cert)"] = compare(new, t257, slack["new 260"]["contacts"], slack["T-257 260"]["contacts"])
            r["calibration: house T-265 vs T-257's 260"] = compare(house, t257)
        if n == 204:
            t257 = from_cert(houses / "T-257-s204_1028.cert")
            r["calibration: house T-264 vs T-257's 204"] = compare(house, t257)
        if n == 293:
            t257 = from_cert(houses / "T-257-s293_1028.cert")
            r["calibration: house witness vs T-257's s293_1028.cert"] = compare(house, t257, syms=[0])
        result[str(n)] = r
        for k, e in r.items():
            b = e["best"]
            print(n, "|", k, "|", b["best_symmetry"], "one-to-one(best)", b["best_nearest_one_to_one"], "any", b["any_symmetry_one_to_one"],
                  "rows", b["assignment_is_row_identity"], ">0.1", b["beyond_0.1"], ">1e-2", b["beyond_1e-2"], "<=1e-3", b["within_1e-3"],
                  "max", round(b["largest_move"], 6), "turned>1", b["turned_beyond_1_degree"], "tilted", b["tilted_beyond_1_degree_new"], "/", b["tilted_beyond_1_degree_ref"],
                  "rev", b["tilts_reversed"], "boxc>0.1", b["box_centred"]["beyond_0.1"], b.get("contacts", ""))
    out_path.write_text(json.dumps(result, indent=1) + "\n")


if __name__ == "__main__":
    main()
