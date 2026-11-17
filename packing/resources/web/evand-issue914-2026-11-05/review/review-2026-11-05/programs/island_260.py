"""The tilted island of the new 260 against T-257's 260 and T-265's, measured in binary64.

Usage (from packing/, Python 3.14):
  python -I island_260.py NEW_260_CERT T257_260_CERT HOUSE_260_WITNESS OUT.json

A measurement; it decides nothing. The island of a packing is its squares turned by
more than 10 degrees (angles modulo 90 in (-45, 45]). For each pair of packings it
reports the island sizes and angles, then matches the two islands under each of the
box's eight symmetries combined with the translation that best aligns them
(centroid-to-centroid after the optimal assignment, iterated), and reports the moves of
the island squares after that rigid alignment, and of the remaining (frame) squares
under the same symmetry without the translation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from identity import SYMS, apply, from_cert, from_witness, hungarian, mod90  # noqa: E402


def island(p: dict, thr: float = 10.0) -> np.ndarray:
    return np.nonzero(np.abs(p["a"]) > thr)[0]


def describe(p: dict, idx: np.ndarray) -> dict:
    a = p["a"][idx]
    vals, counts = np.unique(np.round(a, 1), return_counts=True)
    top = sorted(zip(counts.tolist(), vals.tolist()), reverse=True)[:4]
    return {"size": int(len(idx)), "angle_min": float(a.min()), "angle_max": float(a.max()),
            "most_common_angles_0.1deg": [[v, c] for c, v in top],
            "bbox": [float(p["x"][idx].min()), float(p["x"][idx].max()), float(p["y"][idx].min()), float(p["y"][idx].max())]}


def match(new: dict, ref: dict) -> dict:
    ni, ri = island(new), island(ref)
    out = {"new_island": describe(new, ni), "ref_island": describe(ref, ri), "per_symmetry": {}}
    best = None
    for k in range(8):
        rx, ry, ra = apply(k, ref)
        ax_, ay_ = new["x"][ni], new["y"][ni]
        bx_, by_ = rx[ri], ry[ri]
        m = min(len(ni), len(ri))
        # translation-aligned matching of the islands (iterate assignment and centroid shift)
        tx, ty = float(ax_.mean() - bx_.mean()), float(ay_.mean() - by_.mean())
        for _ in range(5):
            d2 = (ax_[:, None] - (bx_[None, :] + tx)) ** 2 + (ay_[:, None] - (by_[None, :] + ty)) ** 2
            if d2.shape[0] != d2.shape[1]:
                # pad to square with large cost
                n = max(d2.shape)
                pad = np.full((n, n), 1e6)
                pad[: d2.shape[0], : d2.shape[1]] = d2
                d2 = pad
            asg = hungarian(d2)
            pairs = [(i, j) for i, j in enumerate(asg) if i < len(ni) and j < len(ri)]
            ii = np.array([i for i, _ in pairs])
            jj = np.array([j for _, j in pairs])
            tx = float((ax_[ii] - bx_[jj]).mean())
            ty = float((ay_[ii] - by_[jj]).mean())
        mv = np.hypot(ax_[ii] - (bx_[jj] + tx), ay_[ii] - (by_[jj] + ty))
        turn = np.abs(mod90(new["a"][ni][ii] - ra[ri][jj]))
        ent = {"translation": [tx, ty], "matched": int(len(ii)), "island_beyond_1e-2": int((mv > 1e-2).sum()),
               "island_beyond_0.1": int((mv > 0.1).sum()), "island_largest_move": float(mv.max()),
               "island_rms": float(np.sqrt((mv ** 2).mean())), "island_turned_beyond_0.5deg": int((turn > 0.5).sum()),
               "island_angle_shift_median": float(np.median(mod90(new["a"][ni][ii] - ra[ri][jj])))}
        out["per_symmetry"][SYMS[k]] = ent
        if best is None or ent["island_rms"] < best[1]["island_rms"]:
            best = (k, ent)
    out["best_symmetry_for_island"] = SYMS[best[0]]
    out["best"] = best[1]
    # frame squares under that symmetry, no translation
    k = best[0]
    rx, ry, ra = apply(k, ref)
    nf = np.setdiff1d(np.arange(new["n"]), ni)
    rf = np.setdiff1d(np.arange(ref["n"]), ri)
    d2 = (new["x"][nf][:, None] - rx[rf][None, :]) ** 2 + (new["y"][nf][:, None] - ry[rf][None, :]) ** 2
    n = max(d2.shape)
    pad = np.full((n, n), 1e6)
    pad[: d2.shape[0], : d2.shape[1]] = d2
    asg = hungarian(pad)
    pairs = [(i, j) for i, j in enumerate(asg) if i < len(nf) and j < len(rf)]
    mv = np.array([np.hypot(new["x"][nf][i] - rx[rf][j], new["y"][nf][i] - ry[rf][j]) for i, j in pairs])
    out["frame_under_island_symmetry"] = {"new_frame": int(len(nf)), "ref_frame": int(len(rf)), "matched": len(pairs),
                                          "beyond_1e-2": int((mv > 1e-2).sum()), "beyond_0.1": int((mv > 0.1).sum()),
                                          "beyond_0.5": int((mv > 0.5).sum()), "largest": float(mv.max())}
    return out


def main() -> None:
    new = from_cert(Path(sys.argv[1]))
    t257 = from_cert(Path(sys.argv[2]))
    house = from_witness(Path(sys.argv[3]))
    res = {"new 260 vs T-257's 260": match(new, t257), "new 260 vs T-265 (house)": match(new, house),
           "calibration: T-265 vs T-257's 260": match(house, t257)}
    Path(sys.argv[4]).write_text(json.dumps(res, indent=1) + "\n")
    for k, r in res.items():
        print(k)
        print("   islands", r["new_island"]["size"], r["new_island"]["most_common_angles_0.1deg"], "|", r["ref_island"]["size"], r["ref_island"]["most_common_angles_0.1deg"])
        print("   island bbox new", [round(v, 3) for v in r["new_island"]["bbox"]], "ref", [round(v, 3) for v in r["ref_island"]["bbox"]])
        print("   best island symmetry", r["best_symmetry_for_island"], {kk: (round(v, 5) if isinstance(v, float) else v) for kk, v in r["best"].items()})
        print("   frame", r["frame_under_island_symmetry"])


if __name__ == "__main__":
    main()
