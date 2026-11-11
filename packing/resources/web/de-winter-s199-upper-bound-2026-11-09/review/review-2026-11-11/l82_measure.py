"""Measurements (no verdicts): uniform-contraction margins (K1, K2), gains, padding shares,
12-place prints, the #939 construction, the cores against T-282 and each other, and
Daniel's held KKT solve. Decides contracted packings with the frozen checker.

Usage: python -I l82_measure.py T282_YAML T284_YAML N172_JSON N199_JSON DANIEL_REPORT_GZ ALGEBRA_JSON OUT.json
"""

from __future__ import annotations

import gzip
import json
import os
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l82_check as C  # noqa: E402

t0 = time.time()
a = sys.argv[1:]
t282 = C.read_witness_yaml(a[0])
t284 = C.read_witness_yaml(a[1])
c946 = C.read_author_json(a[2])
c939 = C.read_author_json(a[3])
daniel = json.load(gzip.open(a[4]))
alg = json.load(open(a[5]))
OUT: dict = {}


def fs(pk):
    return [[F(*v) for v in q] for q in pk["squares"]]


def sq_of(*vals):
    return tuple((F(v).numerator, F(v).denominator) for v in vals)


def frac(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


def pair_T_mm(qi, qj):
    xi, yi, ci, si = qi
    xj, yj, cj, sj = qj
    d = (xj - xi, yj - yi)
    T = (1 + abs(ci * cj + si * sj) + abs(-ci * sj + si * cj)) / 2
    ws = ((ci, si), (-si, ci), (cj, sj), (-sj, cj))
    return T, max(abs(w[0] * d[0] + w[1] * d[1]) for w in ws)


def extents(q, lam):
    hs = [(abs(c) + abs(s)) / 2 for _, _, c, s in q]
    xs = [lam * x for x, _, _, _ in q]
    ys = [lam * y for _, y, _, _ in q]
    x0 = min(x - h for x, h in zip(xs, hs))
    y0 = min(y - h for y, h in zip(ys, hs))
    ex = max(x + h for x, h in zip(xs, hs)) - x0
    ey = max(y + h for y, h in zip(ys, hs)) - y0
    return ex, ey, x0, y0


def contraction(pk):
    q = fs(pk)
    S = F(*pk["side"])
    best = None
    for i in range(len(q)):
        for j in range(i + 1, len(q)):
            T, mm = pair_T_mm(q[i], q[j])
            r = T / mm
            if best is None or r > best[0]:
                best = (r, i + 1, j + 1)
    lam = best[0]
    ex1, ey1, _, _ = extents(q, F(1))
    ex, ey, x0, y0 = extents(q, lam)
    sc = max(ex, ey)
    env = S - max(ex1, ey1)
    return {
        "lam": lam, "binding": [best[1], best[2]], "contracted_side": sc, "margin": S - sc,
        "envelope": env, "scaling": S - sc - env, "x0": x0, "y0": y0, "q": q,
    }


def contracted_pk(k, lam=None):
    q = k["q"]
    lam = k["lam"] if lam is None else lam
    ex, ey, x0, y0 = extents(q, lam)
    side = max(ex, ey)
    sqs = [sq_of(lam * x - x0, lam * y - y0, c, s) for x, y, c, s in q]
    return {"n": len(sqs), "side": (side.numerator, side.denominator), "squares": sqs}, side


def summ(k):
    return {
        "one_minus_lambda": C.sci(1 - k["lam"], 6), "binding_pair": k["binding"],
        "envelope": C.sci(k["envelope"], 6), "scaling": C.sci(k["scaling"], 6),
        "margin": C.sci(k["margin"], 10), "margin_exact": frac(k["margin"]),
        "contracted_side_floor_30": C.decimal_floor(k["contracted_side"], 30),
        "contracted_side_ceil_12": C.decimal_ceil(k["contracted_side"], 12),
    }


S282, S284 = F(*t282["side"]), F(*t284["side"])
S946, S939 = F(*c946["side"]), F(*c939["side"])
OUT["sides"] = {k: {"floor_40": C.decimal_floor(v, 40), "ceil_12": C.decimal_ceil(v, 12), "exact": frac(v)}
                for k, v in (("T-282", S282), ("T-284", S284), ("946", S946), ("939", S939))}
OUT["T284_side_is_T282_plus_1"] = S284 == S282 + 1

# ---- K1: T-282 contracted, decided
k282 = contraction(t282)
OUT["K_T282"] = summ(k282)
cpk, cside = contracted_pk(k282)
r = C.decide(cpk)
r_lo = C.decide(cpk, side=cside - F(1, 10**30))
pk_in, side_in = contracted_pk(k282, k282["lam"] * (1 - F(1, 10**30)))
r_in = C.decide(pk_in)
OUT["K1"] = {
    "at_contracted_side": r["verdict"], "binding_touching": k282["binding"] in r["touching_pairs"],
    "touching": r["touching_pairs"], "below_by_1e-30": r_lo["verdict"],
    "factor_less_1e-30": r_in["verdict"], "overlapping_there": [x[:2] for x in r_in["overlapping_pairs"]],
}
OUT["K1"]["as_stated"] = (r["verdict"] == "ACCEPT" and OUT["K1"]["binding_touching"] and r_lo["verdict"] == "REFUSE"
                          and r_in["verdict"] == "REFUSE" and k282["binding"] in OUT["K1"]["overlapping_there"])
print("K1", OUT["K1"]["as_stated"], f"{time.time() - t0:.0f}s", flush=True)

# ---- K2: contracted T-282 plus the L of the lemma at side + 1
L = [sq_of(F(2 * a_ + 1, 2), cside + F(1, 2), 1, 0) for a_ in range(14)]
L += [sq_of(cside + F(1, 2), F(2 * b + 1, 2), 1, 0) for b in range(13)]
k2 = {"n": 199, "side": ((cside + 1).numerator, (cside + 1).denominator), "squares": list(cpk["squares"]) + L}
r2 = C.decide(k2)
OUT["K2"] = {"verdict": r2["verdict"], "side_floor_30": C.decimal_floor(cside + 1, 30),
             "side_ceil_12": C.decimal_ceil(cside + 1, 12), "touching": len(r2["touching_pairs"]),
             "as_stated": r2["verdict"] == "ACCEPT"}
print("K2", r2["verdict"], f"{time.time() - t0:.0f}s", flush=True)

# ---- whole-certificate contraction of T-284 and of the two new certificates
k284 = contraction(t284)
OUT["K_T284_whole"] = summ(k284)
k946 = contraction(c946)
OUT["K_946_own"] = summ(k946)
k939 = contraction(c939)
OUT["K_939_own"] = summ(k939)
print("own contractions", f"{time.time() - t0:.0f}s", flush=True)

# ---- gains and shares
m282 = k282["margin"]
inherited = S284 - (cside + 1)
g946 = S282 - S946
g939 = S284 - S939
root_lo = F(alg["946_root_bracket"][0])
OUT["gains"] = {
    "gain_946_vs_T282": C.sci(g946, 12), "gain_946_exact": frac(g946),
    "gain_939_vs_T284": C.sci(g939, 12), "gain_939_exact": frac(g939),
    "gain_939_minus_gain_946": C.sci(g939 - g946, 6),
    "T282_margin": C.sci(m282, 12),
    "T284_inherited_margin": C.sci(inherited, 12), "inherited_equals_T282_margin": inherited == m282,
    "T284_whole_margin": C.sci(k284["margin"], 6),
    "share_946": C.sci(g946 / m282, 8), "share_939_inherited": C.sci(g939 / inherited, 8),
    "946_less_contracted_T282": C.sci(S946 - cside, 10),
    "939_less_contracted_T282_plus_L": C.sci(S939 - (cside + 1), 10),
    "root_less_contracted_T282": C.sci(root_lo - cside, 10),
    "T282_less_root": C.sci(S282 - root_lo, 12),
    "T282_margin_share_of_T282_less_root": C.sci(m282 / (S282 - root_lo), 8),
}
P = {
    "T-282": C.decimal_ceil(S282, 12), "contracted T-282": C.decimal_ceil(cside, 12),
    "946": C.decimal_ceil(S946, 12), "root 172": alg["946"]["root_ceil_12"],
    "T-284": C.decimal_ceil(S284, 12), "contracted T-282 + 1": C.decimal_ceil(cside + 1, 12),
    "939": C.decimal_ceil(S939, 12), "root 199": alg["939"]["root_ceil_12"],
}
OUT["prints_ceil_12"] = P
OUT["option_D_print_below"] = {
    "946": F(P["946"]) < F(P["contracted T-282"]), "939": F(P["939"]) < F(P["contracted T-282 + 1"]),
    "root_172_could_ever": F(P["root 172"]) < F(P["contracted T-282"]),
}
OUT["prints_floor_14"] = {
    "contracted T-282": C.decimal_floor(cside, 14), "946": C.decimal_floor(S946, 14),
    "T-282": C.decimal_floor(S282, 14),
}

# ---- construction of #939
q939 = fs(c939)
Sc = S939 - 1
grid_row = {(F(2 * a_ + 1, 2), Sc + F(1, 2)) for a_ in range(14)}
grid_col = {(Sc + F(1, 2), F(2 * b + 1, 2)) for b in range(13)}
upright = [i for i, (x, y, c, s) in enumerate(q939, 1) if {abs(c), abs(s)} == {F(0), F(1)}]
row_ids = [i for i, (x, y, c, s) in enumerate(q939, 1) if (x, y) in grid_row and i in upright]
col_ids = [i for i, (x, y, c, s) in enumerate(q939, 1) if (x, y) in grid_col and i in upright]
core_ids = [i for i in range(1, 200) if i not in row_ids and i not in col_ids]
hmax_core = max(max(x + (abs(c) + abs(s)) / 2, y + (abs(c) + abs(s)) / 2) for i, (x, y, c, s) in enumerate(q939, 1)
                if i in core_ids)
q284 = fs(t284)
row284 = [i for i, (x, y, c, s) in enumerate(q284, 1) if (x, y) in {(F(2 * a_ + 1, 2), S282 + F(1, 2)) for a_ in range(14)}]
col284 = [i for i, (x, y, c, s) in enumerate(q284, 1) if (x, y) in {(S282 + F(1, 2), F(2 * b + 1, 2)) for b in range(13)}]
OUT["construction_939"] = {
    "row_ids": [min(row_ids), max(row_ids), len(row_ids)] if row_ids else [],
    "col_ids": [min(col_ids), max(col_ids), len(col_ids)] if col_ids else [],
    "core_ids": [min(core_ids), max(core_ids), len(core_ids)],
    "core_inside_side_minus_1": hmax_core <= Sc, "core_top_clearance": C.sci(Sc - hmax_core, 6),
    "core_side_minus_946_side": C.sci(Sc - S946, 6),
    "T284_row_ids": [min(row284), max(row284), len(row284)] if row284 else [],
    "T284_col_ids": [min(col284), max(col284), len(col284)] if col284 else [],
    "same_L_ids_as_T284": row_ids == row284 and col_ids == col284,
}


# ---- cores against T-282 and each other
def z4(c, s):
    re, im = c, s
    r2, i2 = re * re - im * im, 2 * re * im
    return (r2 * r2 - i2 * i2, 2 * r2 * i2)


def compare(qa, qb, ids_a, ids_b):
    best = []
    for ia, ib in zip(ids_a, ids_b):
        xa, ya, ca, sa = qa[ia - 1]
        xb, yb, cb, sb = qb[ib - 1]
        dc = float((xa - xb) ** 2 + (ya - yb) ** 2) ** 0.5
        za, zb = z4(ca, sa), z4(cb, sb)
        dz = float((za[0] - zb[0]) ** 2 + (za[1] - zb[1]) ** 2) ** 0.5 / 4
        best.append((dc, dz, ia))
    return {"max_centre_move": f"{max(b[0] for b in best):.6e}", "at": max(best)[2],
            "max_turn_rad": f"{max(b[1] for b in best):.6e}",
            "moved_beyond_1e-9": sum(1 for b in best if b[0] > 1e-9),
            "exactly_equal": sum(1 for b in best if b[0] == 0 and b[1] == 0)}


q282, q946 = fs(t282), fs(c946)
ids = list(range(1, 173))
OUT["cores"] = {
    "946_vs_T282": compare(q946, q282, ids, ids),
    "939core_vs_T282": compare(q939, q282, core_ids, ids),
    "939core_vs_946": compare(q939, q946, core_ids, ids),
    "939core_exactly_946": [q939[i - 1] for i in core_ids] == q946,
}


# ---- contact structure: T-282 pairs below 1e-12 against #946 pairs below 1e-300
def near(pk, th):
    q = pk["squares"]
    ca = [C._corners_a(s) for s in q]
    out = set()
    for i in range(len(q)):
        for j in range(i + 1, len(q)):
            if C.pair_margin_a(q[i], q[j], ca[i], ca[j]) < th:
                out.add((i + 1, j + 1))
    return out


n282 = near(t282, F(1, 10**12))
n946 = near(c946, F(1, 10**300))
n946b = near(c946, F(1, 10**12))
OUT["contact_structure"] = {
    "T282_pairs_below_1e-12": len(n282), "946_pairs_below_1e-300": len(n946), "946_pairs_below_1e-12": len(n946b),
    "946_tight_subset_of_T282_near": n946 <= n282,
    "T282_near_not_tight_in_946": sorted(n282 - n946)[:40], "count_T282_near_not_tight_in_946": len(n282 - n946),
    "946_tight_not_T282_near": sorted(n946 - n282),
}
print("contacts", f"{time.time() - t0:.0f}s", flush=True)

# ---- Daniel's held KKT solve (think-wju3)
sv = daniel["solve"]
Sx = F(sv["S_exact"])
Sc_d = F(sv["S_cert"])
root_hi = F(alg["946_root_bracket"][1])
places = len(sv["S_exact"].split(".")[1])
OUT["daniel"] = {
    "status": sv["status"], "second_order": sv["second_order"],
    "S_exact": sv["S_exact"], "S_exact_places": places,
    "S_exact_within_one_unit_of_root": abs(Sx - root_lo) < F(1, 10**places),
    "S_exact_minus_root": C.sci(Sx - root_lo, 6),
    "S_cert": sv["S_cert"], "S_cert_minus_root": C.sci(Sc_d - root_hi, 6),
    "S_cert_minus_946": C.sci(Sc_d - S946, 6), "S_cert_ceil_12": C.decimal_ceil(Sc_d, 12),
    "T282_minus_S_cert": C.sci(S282 - Sc_d, 10), "share_S_cert": C.sci((S282 - Sc_d) / m282, 8),
    "witness_sha256_in_report": daniel["source"]["sha256"],
}
OUT["seconds"] = round(time.time() - t0)
with open(a[6], "w") as fh:
    json.dump(OUT, fh, indent=1)
    fh.write("\n")
print(json.dumps({k: v for k, v in OUT.items() if k not in ("K1",)}, indent=1))
