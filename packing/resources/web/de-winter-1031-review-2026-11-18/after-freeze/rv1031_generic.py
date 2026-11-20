"""Is #1031's coincidence with T-325 under one rigid motion generic? (decides nothing)

Written after the findings' freeze for the review of jlevy/squares#1031, in answer to
review A's A2 on #1036; imports nothing from this repository. It reads each file exactly
with the frozen ``rv1031_reader`` and measures in binary64.

    python -I -B rv1031_generic.py --subject json:n299_exact.json \
        --ref "T-325=witness:..." --ref "T-101=cert:..." --self --out generic.json

For the subject against each reference, under each of the eight symmetries of the
reference's box, every translation that carries a square of the reference onto a square
of the subject of the same kind (a turned square onto a turned square whose tilt agrees
within 2 degrees, or an upright square onto an upright one) is a candidate. Candidates
are binned at 0.1; the 40 strongest bins of each kind, and the 5 x 5 unit shifts of the
strongest turned motion, are each refined to their bin's mean and scored: the subject's
squares with a reference square within 0.1 whose tilt agrees within 2 degrees, turned and
upright counted apart. Unit squares with disjoint interiors have centres at least 1 apart,
so a match within 0.1 is one to one. ``--self`` scores the subject against itself with
the identity motion left out, which measures how many squares any lattice shift lines up.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "programs"))

import numpy as np

import rv1031_identity as I

TOL = 0.1
TILT_TOL = 2.0


def score(sub: dict, pr: np.ndarray, tr: np.ndarray, t: np.ndarray) -> dict:
    moved = pr + t
    d = np.sqrt(((sub["xy"][:, None, :] - moved[None, :, :]) ** 2).sum(axis=2))
    k = d.argmin(axis=1)
    dist = d[np.arange(sub["n"]), k]
    good = (dist <= TOL) & (I.tilt_diff(sub["tilt"], tr[k]) <= TILT_TOL)
    st = np.abs(sub["tilt"]) > 1e-9
    return {
        "translation": [round(float(t[0]), 4), round(float(t[1]), 4)],
        "matched": int(good.sum()),
        "matched_tilted": int((good & st).sum()),
        "matched_upright": int((good & ~st).sum()),
        "subject_matched": [int(i) + 1 for i in np.where(good)[0]],
        "reference_matched": sorted(int(k[i]) + 1 for i in np.where(good)[0]),
    }


def scan(sub: dict, ref: dict, exclude_identity: bool) -> dict:
    st = np.abs(sub["tilt"]) > 1e-9
    rows = []
    for sym in I.SYMS:
        pr, tr = I.apply_sym(ref["xy"], ref["tilt"], ref["side"], sym)
        rt = np.abs(tr) > 1e-9
        cands: list[np.ndarray] = []
        best_tilted = None
        for kind in ("tilted", "upright"):
            a = np.where(st if kind == "tilted" else ~st)[0]
            b = np.where(rt if kind == "tilted" else ~rt)[0]
            if not len(a) or not len(b):
                continue
            if kind == "tilted":
                ok = I.tilt_diff(sub["tilt"][a][:, None], tr[b][None, :]) <= TILT_TOL
                ia, ib = np.nonzero(ok)
            else:
                ia, ib = np.meshgrid(np.arange(len(a)), np.arange(len(b)), indexing="ij")
                ia, ib = ia.ravel(), ib.ravel()
            t = sub["xy"][a[ia]] - pr[b[ib]]
            keys = np.round(t / TOL).astype(int)
            top = Counter(map(tuple, keys.tolist())).most_common(40)
            for j, ((bx, by), _) in enumerate(top):
                sel = (keys == np.array([bx, by])).all(axis=1)
                tt = t[sel].mean(axis=0)
                cands.append(tt)
                if kind == "tilted" and j == 0:
                    best_tilted = tt
        if best_tilted is not None:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    cands.append(best_tilted + np.array([dx, dy], dtype=float))
        seen = set()
        for tt in cands:
            key = (int(round(tt[0] / 0.05)), int(round(tt[1] / 0.05)))
            if key in seen:
                continue
            seen.add(key)
            if exclude_identity and sym == "identity" and abs(tt[0]) < 0.5 and abs(tt[1]) < 0.5:
                continue
            r = score(sub, pr, tr, tt)
            r["symmetry"] = sym
            rows.append(r)
    rows.sort(key=lambda r: -r["matched"])
    totals = [r["matched"] for r in rows]
    uprights = [r["matched_upright"] for r in rows]
    best = rows[0]
    unmatched = [i for i in range(1, sub["n"] + 1) if i not in set(best["subject_matched"])]
    um_t = [i for i in unmatched if abs(sub["tilt"][i - 1]) > 1e-9]
    return {
        "reference": {k: ref[k] for k in ("n", "side", "path", "sha256")} | {"tilted": int((np.abs(ref["tilt"]) > 1e-9).sum())},
        "motions_scored": len(rows),
        "best_total": {k: best[k] for k in ("symmetry", "translation", "matched", "matched_tilted", "matched_upright")},
        "best_upright": {k: max(rows, key=lambda r: r["matched_upright"])[k] for k in ("symmetry", "translation", "matched", "matched_tilted", "matched_upright")},
        "best_tilted": {k: max(rows, key=lambda r: (r["matched_tilted"], r["matched"]))[k] for k in ("symmetry", "translation", "matched", "matched_tilted", "matched_upright")},
        "motions_matching_at_least": {str(m): sum(1 for x in totals if x >= m) for m in (100, 150, 180, 200)},
        "motions_with_upright_at_least": {str(m): sum(1 for x in uprights if x >= m) for m in (100, 130, 150)},
        "top10": [{k: r[k] for k in ("symmetry", "translation", "matched", "matched_tilted", "matched_upright")} for r in rows[:10]],
        "best_motion_unmatched": {
            "count": len(unmatched), "tilted": len(um_t),
            "tilted_negative": sum(1 for i in um_t if sub["tilt"][i - 1] < 0),
            "tilted_positive": sum(1 for i in um_t if sub["tilt"][i - 1] > 0),
            "upright": len(unmatched) - len(um_t),
            "x_range": [round(float(sub["xy"][i - 1, 0]), 2) for i in (min(unmatched, key=lambda i: sub["xy"][i - 1, 0]), max(unmatched, key=lambda i: sub["xy"][i - 1, 0]))] if unmatched else [],
            "y_range": [round(float(sub["xy"][i - 1, 1]), 2) for i in (min(unmatched, key=lambda i: sub["xy"][i - 1, 1]), max(unmatched, key=lambda i: sub["xy"][i - 1, 1]))] if unmatched else [],
            "squares": unmatched,
        },
        "best_motion_reference_matched": best["reference_matched"],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--ref", action="append", default=[])
    ap.add_argument("--self", dest="self_", action="store_true")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    sub = I.load(args.subject)
    rec: dict = {"program": "rv1031_generic.py", "tolerance": TOL, "tilt_tolerance_deg": TILT_TOL, "subject": {k: sub[k] for k in ("n", "side", "path", "sha256")}, "references": {}}
    specs = [s.split("=", 1) for s in args.ref]
    for label, spec in specs:
        ref = I.load(spec)
        r = scan(sub, ref, exclude_identity=False)
        rec["references"][label] = r
        print(label, json.dumps({k: r[k] for k in ("best_total", "best_upright", "motions_matching_at_least", "motions_with_upright_at_least")}), flush=True)
    if args.self_:
        r = scan(sub, sub, exclude_identity=True)
        rec["references"]["self (identity left out)"] = r
        print("self", json.dumps({k: r[k] for k in ("best_total", "best_upright", "motions_matching_at_least", "motions_with_upright_at_least")}), flush=True)
    with open(args.out, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
