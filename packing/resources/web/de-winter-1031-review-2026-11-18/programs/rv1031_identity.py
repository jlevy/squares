"""Measure a packing's identity against other packings at its count (decides nothing).

Written for this review of jlevy/squares#1031 after the checker's freeze; imports nothing
from this repository or the source.  It reads each file exactly with ``rv1031_reader``
and measures in binary64, which is ample for distances of 1e-9 and up.

    python -I -B rv1031_identity.py --subject json:n299_exact.json \
        --ref "T-325=witness:n-299.yaml" --ref "T-277=witness:..." --out identity.json

For each reference and each of the box's eight symmetries (applied to the reference in
its own box) and two frames (lower-left: the centres as given; box-centred: each box's
centre at the origin), it gives:

* the nearest-centre map from the subject's squares to the reference's, and whether it
  pairs them one to one;
* the optimal assignment (least total squared distance, ``scipy.optimize``), the squares
  it moves beyond 1e-9, 1e-6, 1e-3, 1e-2 and 1e-1, the largest move, and the squares
  whose tilt (mod 90 degrees, a reflection negating it) differs by more than 1e-6 and
  1 degree;
* the best symmetry by the assignment's total.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # this packet's own modules, under python -I

import numpy as np
from scipy.optimize import linear_sum_assignment

import rv1031_reader as R

SYMS = ["identity", "rot90", "rot180", "rot270", "mirror-x", "mirror-y", "transpose", "anti-transpose"]


def tilt_deg(ux: float, uy: float) -> float:
    """The edge direction's angle mod 90 degrees, in (-45, 45]."""
    a = math.degrees(math.atan2(uy, ux)) % 90.0
    return a - 90.0 if a > 45.0 else a


def load(spec: str) -> dict:
    kind, path = spec.split(":", 1)
    doc = R.read_any(path, kind, require_claim=False)
    s = float(doc["side"])
    xy = np.array([[float(p[0]), float(p[1])] for p in doc["poses"]])
    th = np.array([tilt_deg(float(p[2]), float(p[3])) for p in doc["poses"]])
    with open(path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    return {"n": doc["n"], "side": s, "side_exact": f"{doc['side'].numerator}/{doc['side'].denominator}", "xy": xy, "tilt": th, "path": path, "kind": kind, "sha256": digest}


def apply_sym(xy: np.ndarray, th: np.ndarray, s: float, sym: str) -> tuple[np.ndarray, np.ndarray]:
    x, y = xy[:, 0], xy[:, 1]
    if sym == "identity":
        p, t = np.c_[x, y], th
    elif sym == "rot90":
        p, t = np.c_[s - y, x], th
    elif sym == "rot180":
        p, t = np.c_[s - x, s - y], th
    elif sym == "rot270":
        p, t = np.c_[y, s - x], th
    elif sym == "mirror-x":
        p, t = np.c_[s - x, y], -th
    elif sym == "mirror-y":
        p, t = np.c_[x, s - y], -th
    elif sym == "transpose":
        p, t = np.c_[y, x], -th
    else:
        p, t = np.c_[s - y, s - x], -th
    t = (t + 45.0) % 90.0 - 45.0
    t[t == -45.0] = 45.0
    return p, t


def tilt_diff(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    d = np.abs(a - b) % 90.0
    return np.minimum(d, 90.0 - d)


def measure(sub: dict, ref: dict) -> dict:
    out: dict = {"reference_side": ref["side"], "reference_n": ref["n"], "gain_vs_reference": ref["side"] - sub["side"], "frames": {}}
    for frame in ("lower-left", "box-centred"):
        rows = []
        for sym in SYMS:
            pr, tr = apply_sym(ref["xy"], ref["tilt"], ref["side"], sym)
            ps = sub["xy"].copy()
            if frame == "box-centred":
                pr = pr - ref["side"] / 2
                ps = ps - sub["side"] / 2
            d2 = ((ps[:, None, :] - pr[None, :, :]) ** 2).sum(axis=2)
            nearest = d2.argmin(axis=1)
            one_to_one = len(set(nearest.tolist())) == sub["n"] == ref["n"]
            r_idx, c_idx = linear_sum_assignment(d2)
            moves = np.sqrt(d2[r_idx, c_idx])
            turns = tilt_diff(sub["tilt"][r_idx], tr[c_idx])
            rows.append({
                "symmetry": sym,
                "nearest_one_to_one": bool(one_to_one),
                "nearest_distinct": len(set(nearest.tolist())),
                "assignment_total_sq": float((moves**2).sum()),
                "moved_beyond": {f"1e-{e}": int((moves > 10.0**-e).sum()) for e in (9, 6, 3, 2, 1)},
                "largest_move": float(moves.max()),
                "largest_move_square": int(r_idx[moves.argmax()]) + 1,
                "turned_beyond": {"1e-6 deg": int((turns > 1e-6).sum()), "1 deg": int((turns > 1.0).sum()), "5 deg": int((turns > 5.0).sum())},
                "largest_turn_deg": float(turns.max()),
                "same_index_assignment": bool((c_idx[np.argsort(r_idx)] == np.arange(sub["n"])).all()) if sub["n"] == ref["n"] else False,
            })
        best = min(rows, key=lambda r: r["assignment_total_sq"])
        out["frames"][frame] = {"best": best, "all": rows}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--ref", action="append", default=[])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    sub = load(args.subject)
    rec: dict = {"program": "rv1031_identity.py", "python": sys.version.split()[0], "subject": {k: sub[k] for k in ("n", "side", "side_exact", "path", "kind", "sha256")}, "references": {}}
    sub_tilts = sub["tilt"]
    rec["subject"]["tilted"] = int((np.abs(sub_tilts) > 1e-12).sum())
    for spec in args.ref:
        label, s = spec.split("=", 1)
        ref = load(s)
        m = measure(sub, ref)
        m["reference"] = {k: ref[k] for k in ("n", "side", "side_exact", "path", "kind", "sha256")}
        m["reference"]["tilted"] = int((np.abs(ref["tilt"]) > 1e-12).sum())
        rec["references"][label] = m
        b = m["frames"]["lower-left"]["best"]
        c = m["frames"]["box-centred"]["best"]
        print(label, f"gain {m['gain_vs_reference']:.6e}", "LL", b["symmetry"], b["nearest_one_to_one"], b["moved_beyond"], f"{b['largest_move']:.3f}", "| BC", c["symmetry"], c["nearest_one_to_one"], c["moved_beyond"], f"{c['largest_move']:.3f}", flush=True)
    with open(args.out, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
