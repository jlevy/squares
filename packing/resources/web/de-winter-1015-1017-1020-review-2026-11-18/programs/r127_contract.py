"""Uniform-contraction margins and the report-order steps, exactly.

Lane r127-1118.  Written for this review; imports only its own modules.  It implements
the measurement owner decision think-b0w5 (option D, 17 November 2026) names, from that
decision's words and from the module docstring of devtools.contraction_margin (read for
the definition only; none of its code is used here):

* Scale every centre by a factor lambda about the origin, every rotation fixed.  By
  r127_frame, a pair's margin becomes lambda M - T, so the pair stays interior-disjoint
  iff lambda >= T / M, and the least feasible factor is lambda* = max over pairs of T/M,
  an exact rational, at which the binding pair touches.
* The contracted packing is translated into the corner and boxed:
  L' = max(width, height), each extent read with every square's axis half-width
  (|a| + |b|)/2.  The margin is S - L'.
* A later certificate beats its predecessor shrunk to first contact iff its side is
  below the predecessor's L'; its gain over the predecessor, S_pred - S_succ, then
  exceeds the predecessor's margin.

    python -I -B r127_contract.py LABEL=FILE [LABEL=FILE ...] --out OUT.json

The labels are taken in the order given (the house first, then the reports in report
order) and every earlier-later step is measured.  Each input is first decided by both
methods and refused unless accepted at its own side; the contracted packing is then
written out as corners and decided by both methods in the box of side L', and must be
accepted with its binding pairs touching; the factor lambda* - 10^-30 must make every
binding pair overlap, by method A on that pair (margin exactly -10^-30 M) and by
method B.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script dir

import argparse
import hashlib
import json
import sys
import time
from fractions import Fraction

import r127_area as B
import r127_axes as A
import r127_decide as D
import r127_frame as F
import r127_read as R
from r127_read import Packing

DELTA = Fraction(1, 10**30)


def contraction(p: Packing) -> dict:
    cs, us = F.frames(p)
    for u in us:
        if u[0] * u[0] + u[1] * u[1] != 1:
            raise ValueError("a direction is not a unit vector")
    n = p.n
    best = None
    binding = []
    for i in range(n):
        for j in range(i + 1, n):
            d = (cs[j][0] - cs[i][0], cs[j][1] - cs[i][1])
            lam = F.T_of(us[i], us[j]) / F.M_of(us[i], us[j], d)
            if best is None or lam > best:
                best, binding = lam, [(i, j)]
            elif lam == best:
                binding.append((i, j))
    assert best is not None
    lam = best
    x0, x1, y0, y1 = F.extents(cs, us)
    ccs = [(lam * c[0], lam * c[1]) for c in cs]
    cx0, cx1, cy0, cy1 = F.extents(ccs, us)
    Lp = max(cx1 - cx0, cy1 - cy0)
    # contracted corners, translated into the corner of the box
    corners = []
    for pts, c in zip(p.corners, cs, strict=True):
        sx, sy = (lam - 1) * c[0] - cx0, (lam - 1) * c[1] - cy0
        corners.append([(x + sx, y + sy) for x, y in pts])
    q = Packing(n=n, side=Lp, corners=corners, form="contracted")
    dq = D.decide_full(q)
    sq = D.summarize(dq)
    touching = set(tuple(t) for t in sq["touching_pairs"])
    binding_touch = all((i + 1, j + 1) in touching for i, j in binding)
    # past: lambda* - DELTA
    past = []
    for i, j in binding:
        lam2 = lam - DELTA
        pi = [(x + (lam2 - 1) * cs[i][0], y + (lam2 - 1) * cs[i][1]) for x, y in p.corners[i]]
        pj = [(x + (lam2 - 1) * cs[j][0], y + (lam2 - 1) * cs[j][1]) for x, y in p.corners[j]]
        ma = A.margin(A.prepare(pi), A.prepare(pj))
        d = (cs[j][0] - cs[i][0], cs[j][1] - cs[i][1])
        expect = -DELTA * F.M_of(us[i], us[j], d)
        cb = B.pair_class(B.ccw(B.to_mpq(pi)), B.ccw(B.to_mpq(pj)))[0]
        past.append({"pair": [i + 1, j + 1], "margin_A": D.sci(ma),
                     "equals_minus_delta_M": ma == expect, "class_B": cb})
    past_ok = all(r["equals_minus_delta_M"] and r["class_B"] == "overlap" for r in past)
    return {
        "lambda_star": D.fs(lam),
        "one_less_lambda_star": D.sci(1 - lam),
        "binding_pairs": [[i + 1, j + 1] for i, j in binding],
        "extent_original": {"width": D.fs(x1 - x0), "height": D.fs(y1 - y0),
                            "side_less_larger_extent": D.sci(p.side - max(x1 - x0, y1 - y0))},
        "L_prime": D.fs(Lp),
        "L_prime_decimal": D.dec(Lp, 30),
        "contracted_width_height": [D.sci(cx1 - cx0), D.sci(cy1 - cy0)],
        "margin": D.fs(p.side - Lp),
        "margin_decimal": D.sci(p.side - Lp),
        "contracted_decision": {k: sq[k] for k in ("verdict", "pairs", "pair_classes_A",
                                                   "touching_pairs", "wall_contacts",
                                                   "least_margin", "problem_count")},
        "binding_pairs_touch_in_contracted": binding_touch,
        "past_lambda_star_less_1e-30": past,
        "past_refused_as_stated": past_ok,
        "_L": Lp,
        "_lam": lam,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.process_time()
    labels, packs, rec = [], [], {}
    for spec in a.inputs:
        label, path = spec.split("=", 1)
        p = R.read_path(path)
        s = D.summarize(D.decide_full(p))
        if s["verdict"] != "ACCEPT":
            print(f"{label}: refused at its own side; nothing measured")
            return 1
        c = contraction(p)
        if c["contracted_decision"]["verdict"] != "ACCEPT" or not c["binding_pairs_touch_in_contracted"]:
            print(f"{label}: the contracted packing was not accepted with its binding pair touching")
            return 1
        labels.append(label)
        packs.append((p, c))
        rec[label] = {"file": path, "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(),
                      "side": D.fs(p.side), "side_decimal": D.dec(p.side, 30),
                      **{k: v for k, v in c.items() if not k.startswith("_")}}
        print(f"{label}: S={D.dec(p.side, 18)} lambda*=1-{c['one_less_lambda_star']} "
              f"binding={c['binding_pairs']} L'={c['L_prime_decimal'][:22]} "
              f"margin={c['margin_decimal']} past_ok={c['past_refused_as_stated']}")
    steps = []
    for i in range(len(packs)):
        for j in range(i + 1, len(packs)):
            (pp, cp), (ps, _) = packs[i], packs[j]
            gain = pp.side - ps.side
            margin = pp.side - cp["_L"]
            step = {
                "predecessor": labels[i], "successor": labels[j],
                "gain": D.fs(gain), "gain_decimal": D.sci(gain),
                "predecessor_margin": D.fs(margin), "predecessor_margin_decimal": D.sci(margin),
                "gain_less_margin": D.fs(gain - margin),
                "gain_less_margin_decimal": D.sci(gain - margin),
                "gain_over_margin": D.sci(gain / margin) if margin > 0 else None,
                "successor_below_contracted_predecessor": ps.side < cp["_L"],
            }
            steps.append(step)
            print(f"{labels[i]} -> {labels[j]}: gain={step['gain_decimal']} "
                  f"margin={step['predecessor_margin_decimal']} "
                  f"gain-margin={step['gain_less_margin_decimal']} "
                  f"ratio={step['gain_over_margin']} beats={step['successor_below_contracted_predecessor']}")
    out = {"program": "r127_contract.py", "order": labels, "packings": rec, "steps": steps,
           "cpu_seconds": round(time.process_time() - t0, 2)}
    json.dump(out, open(a.out, "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
