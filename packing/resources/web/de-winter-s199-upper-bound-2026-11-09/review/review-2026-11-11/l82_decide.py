"""Decide one certificate with the frozen checker, then run the stated controls on it.

Usage: python -I l82_decide.py LABEL JSON YAML OUT.json [--controls]
       python -I l82_decide.py LABEL - YAML OUT.json        (house witness, no twin)
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l82_check as C  # noqa: E402

label, jpath, ypath, out = sys.argv[1:5]
run_controls = "--controls" in sys.argv
t0 = time.time()
rec: dict = {"label": label}

pk = C.read_witness_yaml(ypath)
if jpath != "-":
    pj = C.read_author_json(jpath)
    rec["R0_twin_equal"] = pj["side"] == pk["side"] and pj["squares"] == pk["squares"]
S = F(*pk["side"])
n = pk["n"]
rec["side_exact"] = f"{S.numerator}/{S.denominator}"
rec["side_floor_40"] = C.decimal_floor(S, 40)
rec["side_ceil_12"] = C.decimal_ceil(S, 12)
rec["side_den_digits"] = len(str(S.denominator))
rec["max_scalar_den_digits"] = max(len(str(v[1])) for sq in pk["squares"] for v in sq)
base = C.decide(pk)
rec["base"] = base
print(label, "base", base["verdict"], f"{time.time() - t0:.0f}s", flush=True)


def sq_of(cx, cy, c, s):
    return tuple((F(v).numerator, F(v).denominator) for v in (cx, cy, c, s))


def fr(sq):
    return [F(*v) for v in sq]


def with_squares(new):
    return {"n": len(new), "side": pk["side"], "squares": new}


def summary(r):
    return {
        "verdict": r["verdict"],
        "not_unit": [r["not_unit_a"], r["not_unit_b"]],
        "outside": [r["outside_a"], r["outside_b"]],
        "overlapping": r["overlapping_pairs"],
        "touching": len(r["touching_pairs"]),
        "least": r["least_positive_margin"],
        "disagree": r["method_disagreements"],
    }


if run_controls:
    sqs = list(pk["squares"])
    ctl: dict = {}
    # G1
    g = sqs[:-1] + [sqs[0]]
    r = C.decide(with_squares(g))
    ctl["G1"] = summary(r)
    ctl["G1"]["as_stated"] = r["verdict"] == "REFUSE" and [x[:2] for x in r["overlapping_pairs"]] == [[1, n]] and \
        r["overlapping_pairs"][0][2:] == ["-1.000000e+00", "1.000000e+00"]
    # G2
    cx, cy, c, s = fr(sqs[0])
    g = [sq_of(cx + S, cy, c, s)] + sqs[1:]
    r = C.decide(with_squares(g))
    ctl["G2"] = summary(r)
    ctl["G2"]["as_stated"] = r["verdict"] == "REFUSE" and r["outside_a"] == r["outside_b"] == [1] and not r["overlapping_pairs"]
    # G5
    g = [sq_of(cx, cy, c + F(1, 10**330), s)] + sqs[1:]
    r = C.decide(with_squares(g))
    ctl["G5"] = summary(r)
    ctl["G5"]["as_stated"] = r["verdict"] == "REFUSE" and r["not_unit_a"] == r["not_unit_b"] == [1]
    # G8, G9
    for name, f in (("G8", lambda x, y, c, s: (y, x, s, c)), ("G9", lambda x, y, c, s: (S - y, x, -s, c))):
        g = [sq_of(*f(*fr(q))) for q in sqs]
        r = C.decide(with_squares(g))
        ctl[name] = summary(r)
        ctl[name]["as_stated"] = r["verdict"] == "ACCEPT" and len(r["touching_pairs"]) == len(base["touching_pairs"]) \
            and r["least_positive_margin_exact"] == base["least_positive_margin_exact"]
    # S1
    wall_rt = sorted({k for k, w in base["wall_contacts"] if w in ("right", "top")})
    r = C.decide(pk, side=S - F(1, 10**400))
    ctl["S1"] = summary(r)
    ctl["S1"]["right_top_contact_squares"] = wall_rt
    ctl["S1"]["as_stated"] = r["verdict"] == "REFUSE" and r["outside_a"] == r["outside_b"] == wall_rt and bool(wall_rt)
    # S2, S3
    if label.startswith("939"):
        s2 = F("14.61468985328358057514628890087947061619")
        s3 = S - F(1, 10**98)
    else:
        s2 = F(C.decimal_ceil(S, 12))
        s3 = F("13.61468985328358057514628890087947061618972730200175769881")
    r = C.decide(pk, side=s2)
    ctl["S2"] = summary(r)
    ctl["S2"]["side"] = str(s2)
    ctl["S2"]["as_stated"] = r["verdict"] == "ACCEPT"
    r = C.decide(pk, side=s3)
    ctl["S3"] = summary(r)
    ctl["S3"]["as_stated"] = r["verdict"] == "REFUSE"
    # R1
    r = C.decide({"n": n - 1, "side": pk["side"], "squares": sqs[:-1]})
    ctl["R1"] = summary(r)
    ctl["R1"]["as_stated"] = r["verdict"] == "ACCEPT"
    # C1: the 12 closest positive-margin pairs, pair-level by both methods
    ca = [C._corners_a(q) for q in sqs]
    ms = []
    for i in range(n):
        for j in range(i + 1, n):
            m = C.pair_margin_a(sqs[i], sqs[j], ca[i], ca[j])
            if m > 0:
                ms.append((m, i, j))
    ms.sort()
    eps = F(1, 10**320)
    c1 = []
    for m, i, j in ms[:12]:
        xi, yi, ci_, si_ = fr(sqs[i])
        xj, yj, cj_, sj_ = fr(sqs[j])
        d = (xj - xi, yj - yi)
        ws = [(ci_, si_), (-si_, ci_), (cj_, sj_), (-sj_, cj_)]
        T = (1 + abs(ci_ * cj_ + si_ * sj_) + abs(-ci_ * sj_ + si_ * cj_)) / 2
        mm = max(abs(w[0] * d[0] + w[1] * d[1]) for w in ws)
        tstar = T / mm
        res = []
        for de, want in ((F(0), "contact"), (-eps, "overlap"), (eps, "clear")):
            t = tstar + de / mm
            qj = sq_of(xi + t * d[0], yi + t * d[1], cj_, sj_)
            ma = C.pair_margin_a(sqs[i], qj)
            kb, _ = C.pair_class_b(C._corners_b(sqs[i]), C._corners_b(qj))
            res.append(C.classify_margin(ma) == kb == want and ma == de)
        c1.append({"pair": [i + 1, j + 1], "margin": C.sci(m), "ok": all(res)})
    ctl["C1"] = {"pairs": c1, "as_stated": all(x["ok"] for x in c1)}
    rec["controls"] = ctl
    rec["every_control_as_stated"] = all(v["as_stated"] for v in ctl.values())
    print(label, "controls", rec["every_control_as_stated"], f"{time.time() - t0:.0f}s", flush=True)

rec["seconds"] = round(time.time() - t0)
with open(out, "w") as fh:
    json.dump(rec, fh, indent=1)
    fh.write("\n")
