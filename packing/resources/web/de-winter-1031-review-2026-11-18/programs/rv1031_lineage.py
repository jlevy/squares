"""What of #1031's stated lineage can be measured here (decides nothing).

Written for the review of jlevy/squares#1031 after the checker's freeze; imports nothing
from this repository or the source.  Reads exactly with ``rv1031_reader``, measures in
binary64.

    python -I -B rv1031_lineage.py --subject json:n299_exact.json \
        --donor "LABEL=cert:n372.cert" ... --out lineage.json

1. **The reflection across x + y = S.**  Each tilted square ``(x, y, theta)`` is mapped
   to ``(S - y, S - x, -theta)`` and paired with the nearest tilted square of the other
   tilt sign; the counts within 0.05, 0.1 and 0.25 whose tilts agree within 1 and 3
   degrees say how far one tilted group is the mirror image of the other.  The same is
   done for every square of the packing.
2. **Copies of a donor.**  For each donor packing and each of the eight symmetries of
   its box, every pair of a tilted subject square and a tilted donor square whose tilts
   (mod 90 degrees) agree within 2 degrees votes for the translation that carries the
   one centre onto the other.  The five strongest votes (bins of 0.1) are refined and
   each is scored by the subject squares, tilted and upright counted apart, that have a
   donor square within 0.1 with a tilt within 2 degrees.  A slice copied and then
   optimized shows as many tilted squares matched under one motion; an upright lattice
   matches at many offsets, so upright matches alone say nothing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # this packet's own modules, under python -I

import numpy as np

import rv1031_identity as I


def tilt_ok(a: np.ndarray, b: np.ndarray, tol: float) -> np.ndarray:
    return I.tilt_diff(a, b) <= tol


def reflection(sub: dict) -> dict:
    s = sub["side"]
    xy, th = sub["xy"], sub["tilt"]
    tilted = np.abs(th) > 1e-9
    out: dict = {}
    for name, sel_from, sel_to in (("negative_to_positive", (th < -1e-9), (th > 1e-9)), ("positive_to_negative", (th > 1e-9), (th < -1e-9))):
        src = np.where(sel_from)[0]
        dst = np.where(sel_to)[0]
        mx = np.c_[s - xy[src, 1], s - xy[src, 0]]
        mt = -th[src]
        d = np.sqrt(((mx[:, None, :] - xy[dst][None, :, :]) ** 2).sum(axis=2))
        k = d.argmin(axis=1)
        dist = d[np.arange(len(src)), k]
        td = I.tilt_diff(mt, th[dst][k])
        out[name] = {
            "squares": int(len(src)),
            "within": {f"{r} and {t} deg": int(((dist <= r) & (td <= t)).sum()) for r in (0.05, 0.1, 0.25) for t in (1.0, 3.0)},
            "median_distance": float(np.median(dist)),
            "distinct_partners": int(len(set(k.tolist()))),
        }
    mx = np.c_[s - xy[:, 1], s - xy[:, 0]]
    mt = -th
    d = np.sqrt(((mx[:, None, :] - xy[None, :, :]) ** 2).sum(axis=2))
    k = d.argmin(axis=1)
    dist = d[np.arange(len(xy)), k]
    td = I.tilt_diff(mt, th[k])
    out["every_square"] = {
        "squares": int(len(xy)),
        "within": {f"{r} and {t} deg": int(((dist <= r) & (td <= t)).sum()) for r in (0.01, 0.05, 0.1, 0.25) for t in (1.0, 3.0)},
        "tilted_within_0.1_and_3_deg": int(((dist <= 0.1) & (td <= 3.0) & tilted).sum()),
    }
    return out


def donor_scan(sub: dict, don: dict) -> dict:
    res = []
    st = np.abs(sub["tilt"]) > 1e-9
    for sym in I.SYMS:
        pd, td = I.apply_sym(don["xy"], don["tilt"], don["side"], sym)
        dt = np.abs(td) > 1e-9
        a = np.where(st)[0]
        b = np.where(dt)[0]
        if len(a) == 0 or len(b) == 0:
            continue
        ok = tilt_ok(sub["tilt"][a][:, None], td[b][None, :], 2.0)
        ia, ib = np.nonzero(ok)
        t = sub["xy"][a[ia]] - pd[b[ib]]
        bins = Counter(map(tuple, np.round(t / 0.1).astype(int).tolist()))
        for (bx, by), votes in bins.most_common(5):
            sel = (np.round(t / 0.1).astype(int) == np.array([bx, by])).all(axis=1)
            tt = t[sel].mean(axis=0)
            moved = pd + tt
            d = np.sqrt(((sub["xy"][:, None, :] - moved[None, :, :]) ** 2).sum(axis=2))
            k = d.argmin(axis=1)
            dist = d[np.arange(sub["n"]), k]
            good = (dist <= 0.1) & tilt_ok(sub["tilt"], td[k], 2.0)
            res.append({
                "symmetry": sym,
                "translation": [float(tt[0]), float(tt[1])],
                "votes": int(votes),
                "matched_tilted": int((good & st).sum()),
                "matched_upright": int((good & ~st).sum()),
                "matched_tilted_squares": [int(x) + 1 for x in np.where(good & st)[0]],
            })
    res.sort(key=lambda r: (-r["matched_tilted"], -r["votes"]))
    return {"donor": {k: don[k] for k in ("n", "side", "path", "sha256")} | {"tilted": int((np.abs(don["tilt"]) > 1e-9).sum())}, "best": res[:5]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--donor", action="append", default=[])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    sub = I.load(args.subject)
    rec: dict = {"program": "rv1031_lineage.py", "subject": {k: sub[k] for k in ("n", "side", "path", "sha256")}, "reflection_across_x_plus_y_equals_S": reflection(sub), "donors": {}}
    print(json.dumps(rec["reflection_across_x_plus_y_equals_S"]), flush=True)
    for spec in args.donor:
        label, s = spec.split("=", 1)
        don = I.load(s)
        r = donor_scan(sub, don)
        rec["donors"][label] = r
        b = r["best"][0] if r["best"] else {}
        print(label, don["n"], f"{don['side']:.9f}", "tilted", r["donor"]["tilted"], "| best", b.get("symmetry"), b.get("matched_tilted"), b.get("matched_upright"), b.get("votes"), flush=True)
    with open(args.out, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(args.out, "rb") as fh:
        print("wrote", args.out, hashlib.sha256(fh.read()).hexdigest()[:16])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
