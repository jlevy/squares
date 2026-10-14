"""Own checker for the single-node wx-cert-3 certificate JQ (jQTw.n0.JQ.leaf), written from SPEC_v3.0.md alone.

It re-derives, with exact rationals and without using the author's checker:
  - the well-formedness items that matter for one node (numbers, unit rotations, node data, header ranges);
  - the ROOT CONDITIONS (parent, assumptions, side interval, ROOT CONTAINS WINDOW with centres, section 8);
  - the EMPTY test on the start store (section 2);
  - the preconditions of every `opt` declaration (4.5: the 7 other options excluded, 4.7) and of every `ind`
    declaration (4.10: every option not listed excluded), plus (R1)-(R3);
  - the term rules (T1)-(T4) for every term, the facts of 4.0-4.2, 4.5, 4.9, 4.10 as polynomials;
  - Rem := 0 - sum lambda_k prod(...) and L by the CENTRED RULE (section 5), the acceptance L >= value > 0;
  - the acceptance of the proposed store and the closure {"kind":"infeasible"};
  - L against the zero_step_L of the author's stored acceptance report (a cross-check, not a dependency).
Usage: python3 -I jq_leaf_check.py SRC_ROOT
"""
import gzip
import hashlib
import json
import os
import re
import sys
import time
from fractions import Fraction as Fr

SRC = sys.argv[1]
CERT = os.path.join(SRC, "local-research/claude-20261002/cloud/analysis/part3_exact/certs/JQ_v1/jQTw.n0.JQ.cert.jsonl.gz")
PACK = os.path.join(SRC, "upper-packing-certificate.json")
REPORT = os.path.join(SRC, "research/window-extension-20261008/acceptance/JQ_v1_jQTwn0_C1.json")
NUM = re.compile(r"^-?[0-9]+(/[0-9]+)?$")
fails = []
T0 = time.time()


def check(cond, text):
    print(("OK   " if cond else "FAIL ") + text, flush=True)
    if not cond:
        fails.append(text)


def num(s):
    assert isinstance(s, str) and NUM.match(s), "bad number string %r" % (s,)
    if "/" in s:
        assert int(s.split("/")[1]) != 0
    return Fr(s)


def rot(r):
    g, s = num(r[0]), num(r[1])
    assert g * g + s * s == 1, "non-unit rotation %r" % (r,)
    return (g, s)


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def conj(a):
    return (a[0], -a[1])


def J(v):
    return (-v[1], v[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


# ---------------------------------------------------------------- reference data (section 1)
pack_bytes = open(PACK, "rb").read()
pack = json.loads(pack_bytes)
Sref = num(pack["side"])
LABELS = list(range(1, 18))
u, v, pfile = {}, {}, {}
for i in LABELS:
    sq = pack["squares"][i - 1]
    t = num(sq["t"])
    u[i] = (Fr(1 - t * t, 1 + t * t), Fr(2 * t, 1 + t * t))
    v[i] = J(u[i])
    pfile[i] = (num(sq["x"]), num(sq["y"]))
p = dict(pfile)
T0ref = u[9][0] * (u[9][0] + 4 - Sref)
p[13] = (pfile[13][0] - (T0ref / 3) * v[13][0], pfile[13][1] - (T0ref / 3) * v[13][1])
frame = {i: ((u[i], v[i]) if i in (11, 13) else ((Fr(1), Fr(0)), (Fr(0), Fr(1)))) for i in LABELS}

# ---------------------------------------------------------------- the certificate file
raw = gzip.open(CERT, "rb").read()
text = raw.decode("utf-8")
assert not text.startswith("﻿")
lines = text.split("\n")
if lines[-1] == "":
    lines.pop()
check(len(lines) == 2 and all(l.strip() for l in lines), "file: a header line and one node line, no empty line")
hdr = json.loads(lines[0])
node = json.loads(lines[1])
check(hdr["schema"] == "wx-cert-3", "schema wx-cert-3")
check(hdr["packing_sha256"] == hashlib.sha256(pack_bytes).hexdigest(), "packing_sha256 is the SHA-256 of upper-packing-certificate.json")
check(num(hdr["Sref"]) == Sref, "header Sref equals the file's side")
check(hdr["labels"] == 17 and isinstance(hdr["labels"], int), "labels = 17 (JSON integer)")
S_floor = num(hdr["S_floor"])
check(4 <= S_floor <= Sref, "4 <= S_floor <= Sref")
check(set(hdr.keys()) == {"schema", "packing_sha256", "Sref", "root", "labels", "S_floor", "window", "terminal"}, "header keys")
check(hdr["root"] == node["id"] and isinstance(node["id"], str) and node["id"] != "", "root is the one node; id a non-empty string")
check(set(node.keys()) == {"id", "parent", "S", "box", "arc", "assume", "forms", "rounds", "close"}, "node keys")


def read_region(obj, with_centre):
    keys = {"box", "alpha"} | ({"centre"} if with_centre and "centre" in obj else set())
    assert set(obj.keys()) == keys, "region keys %s" % sorted(obj.keys())
    assert set(obj["box"].keys()) == {str(i) for i in LABELS}
    assert set(obj["alpha"].keys()) == {str(i) for i in LABELS}
    box = {i: [(num(obj["box"][str(i)][k][0]), num(obj["box"][str(i)][k][1])) for k in (0, 1)] for i in LABELS}
    for i in LABELS:
        assert box[i][0][0] <= box[i][0][1] and box[i][1][0] <= box[i][1][1]
    alpha = {i: num(obj["alpha"][str(i)]) for i in LABELS}
    centre = {i: (Fr(1), Fr(0)) for i in LABELS}
    if "centre" in obj:
        assert set(obj["centre"].keys()) == {str(i) for i in LABELS}
        centre = {i: rot(obj["centre"][str(i)]) for i in LABELS}
    return box, alpha, centre


Wbox, Walpha, Wcentre = read_region(hdr["window"], True)
Tbox, Talpha, Tcentre = read_region(hdr["terminal"], True)
check(all(0 < Walpha[i] < 1 for i in LABELS) and all(0 < Talpha[i] <= 1 for i in LABELS), "header alpha ranges")

# node data
S_lo, S_hi = num(node["S"][0]), num(node["S"][1])
assert set(node["box"].keys()) == {str(i) for i in LABELS} and set(node["arc"].keys()) == {str(i) for i in LABELS}
box = {i: [(num(node["box"][str(i)][k][0]), num(node["box"][str(i)][k][1])) for k in (0, 1)] for i in LABELS}
rho, Pm, Pp = {}, {}, {}
for i in LABELS:
    a = node["arc"][str(i)]
    assert set(a.keys()) == {"c", "lo", "hi"}
    rho[i], Pm[i], Pp[i] = rot(a["c"]), rot(a["lo"]), rot(a["hi"])
check(S_lo <= S_hi and all(box[i][k][0] <= box[i][k][1] for i in LABELS for k in (0, 1)), "node data: lo <= hi, S_lo <= S_hi")
check(all(Pm[i][0] > 0 and Pp[i][0] > 0 and Pm[i][1] <= Pp[i][1] for i in LABELS), "node data: cos P^- > 0, cos P^+ > 0, sin P^- <= sin P^+")
check(node["parent"] is None and node["assume"] == [], "root: parent null, empty assumption list")
check(S_lo <= S_floor and S_hi >= Sref, "root: S_lo <= S_floor and S_hi >= Sref")
check(all(box[i][k][0] <= Wbox[i][k][0] and Wbox[i][k][1] <= box[i][k][1] for i in LABELS for k in (0, 1)), "root box contains the window box")
ok = True
for i in LABELS:
    Abm = cmul(cmul(conj(Wcentre[i]), rho[i]), Pm[i])
    Abp = cmul(cmul(conj(Wcentre[i]), rho[i]), Pp[i])
    ok &= Abm[0] > 0 and Abp[0] > 0 and Abp[1] >= Walpha[i] and Abm[1] <= -Walpha[i]
check(ok, "ROOT CONTAINS WINDOW (section 8, with the window's centres): cos Ab^+- > 0, sin Ab^+ >= alpha, sin Ab^- <= -alpha")
check(all(rho[i] == Wcentre[i] for i in LABELS), "(info) the root centres equal the window centres")

# node-centre directions
abar = {i: cmul(rho[i], u[i]) for i in LABELS}
bbar = {i: J(abar[i]) for i in LABELS}

# ---------------------------------------------------------------- the round and its start store (= node data)
check(len(node["rounds"]) == 1, "one round")
rnd = node["rounds"][0]
check(set(rnd.keys()) == {"pairs", "steps", "store"}, "round keys")
# store bounds (section 3) on the start store: no rarc, no cuts
cmax = {i: (Fr(1) if Pm[i][1] <= 0 <= Pp[i][1] else max(Pm[i][0], Pp[i][0])) for i in LABELS}
SB = {}
for i in LABELS:
    SB["xi:%d:1" % i] = box[i][0]
    SB["xi:%d:2" % i] = box[i][1]
    SB["s:%d" % i] = (Pm[i][1], Pp[i][1])
    SB["C:%d" % i] = (min(Pm[i][0], Pp[i][0]), cmax[i])
SB["S"] = (S_lo, S_hi)
# EMPTY test on the start store
check(all(SB[k][0] <= SB[k][1] for k in SB), "start store not EMPTY (box, side, arcs; no rarc, no cuts)")


def imul(a, b):
    c = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return (min(c), max(c))


def iadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def iscale(c, a):
    return (c * a[0], c * a[1]) if c >= 0 else (c * a[1], c * a[0])


def lin_D(o, t, which):
    """Da:o:t (which='a') or Db:o:t (which='b') as (constant, {xi name: coef})."""
    n = abar[o] if which == "a" else bbar[o]
    const = dot(n, (p[t][0] - p[o][0], p[t][1] - p[o][1]))
    coefs = {}
    for lab, sgn in ((t, 1), (o, -1)):
        for k in (1, 2):
            coefs["xi:%d:%d" % (lab, k)] = coefs.get("xi:%d:%d" % (lab, k), Fr(0)) + sgn * dot(n, frame[lab][k - 1])
    return const, coefs


def SB_D(o, t, which):
    const, coefs = lin_D(o, t, which)
    iv = (const, const)
    for name, c in coefs.items():
        iv = iadd(iv, iscale(c, SB[name]))
    return iv


def SB_AB(o, t, which):
    """SB(A:o:t) = SB(C:o) SB(Da) + SB(s:o) SB(Db); SB(B:o:t) = SB(C:o) SB(Db) - SB(s:o) SB(Da)."""
    Da, Db = SB_D(o, t, "a"), SB_D(o, t, "b")
    C, s = SB["C:%d" % o], SB["s:%d" % o]
    if which == "a":
        return iadd(imul(C, Da), imul(s, Db))
    return iadd(imul(C, Db), iscale(Fr(-1), imul(s, Da)))


def effective_rarc(i, j):
    """default endpoints D^- = P_j^- conj(P_i^+), D^+ = P_j^+ conj(P_i^-) (no stored endpoints in this store)."""
    Dm, Dp = cmul(Pm[j], conj(Pp[i])), cmul(Pp[j], conj(Pm[i]))
    Rm = Dm if Dm[0] > 0 else None
    Rp = Dp if Dp[0] > 0 else None
    return Rm, Rp


def excluded(o, t, axis, eps):
    """4.7: option (o, t, axis, eps) is EXCLUDED on the start store iff U < 1/2 + h_lo."""
    A = SB_AB(o, t, axis)
    U = A[1] if eps == 1 else -A[0]
    i, j = min(o, t), max(o, t)
    Rm, Rp = effective_rarc(i, j)
    h_lo = Fr(1, 2)
    if Rm is not None and Rp is not None:
        if (o, t) == (i, j):
            Qm, Qp = Rm, Rp
        else:
            Qm, Qp = conj(Rp), conj(Rm)
        nbar = abar[o] if axis == "a" else bbar[o]
        nbar = (eps * nbar[0], eps * nbar[1])
        Ebar = cmul(abar[t], conj(nbar))
        Em, Ep = cmul(Ebar, Qm), cmul(Ebar, Qp)
        D = cmul(Ep, conj(Em))
        if Em[0] * Ep[0] >= 0 and Em[1] * Ep[1] >= 0 and D[0] > 0 and D[1] >= 0:
            h_lo = min(abs(Em[0]) + abs(Em[1]), abs(Ep[0]) + abs(Ep[1])) / 2
    return U < Fr(1, 2) + h_lo


def all_options(i, j):
    return [(o, t, ax, e) for (o, t) in ((i, j), (j, i)) for ax in "ab" for e in (1, -1)]


# declarations
opt_avail = set()          # options with an accepted `opt` declaration
ind_lists = {}             # (i,j) -> list of options
ind_pairs_declared = []
bad_decl = 0
for d in rnd["pairs"]:
    i, j = d["i"], d["j"]
    assert i < j and i in LABELS and j in LABELS
    if d["mode"] == "opt":
        assert set(d.keys()) == {"i", "j", "mode", "o", "t", "axis", "eps"}
        opt = (d["o"], d["t"], d["axis"], d["eps"])
        assert {opt[0], opt[1]} == {i, j} and opt[2] in ("a", "b") and opt[3] in (1, -1)
        others = [x for x in all_options(i, j) if x != opt]
        if all(excluded(*x) for x in others):
            opt_avail.add(opt)
        else:
            bad_decl += 1
            print("   opt declaration precondition FAILS for", opt)
    elif d["mode"] == "ind":
        assert set(d.keys()) == {"i", "j", "mode", "options"}
        lst = [(x["o"], x["t"], x["axis"], x["eps"]) for x in d["options"]]
        assert 1 <= len(lst) <= 8 and len(set(lst)) == len(lst)
        assert all({x[0], x[1]} == {i, j} and x[2] in ("a", "b") and x[3] in (1, -1) for x in lst)
        assert (i, j) not in ind_lists, "(R1) two ind declarations of one pair"
        ind_lists[(i, j)] = lst
        unlisted = [x for x in all_options(i, j) if x not in lst]
        if not all(excluded(*x) for x in unlisted):
            bad_decl += 1
            print("   ind declaration precondition FAILS for pair", (i, j))
    else:
        raise AssertionError("unknown mode %r" % d["mode"])
opt_pairs = {(min(o, t), max(o, t)) for (o, t, ax, e) in opt_avail}
check(bad_decl == 0, "every declaration's precondition holds on the start store (opt: 7 others excluded; ind: unlisted options excluded)")
check(not (opt_pairs & set(ind_lists)), "(R2) no pair has both an opt and an ind declaration")
print("   opt-available options:", sorted(opt_avail))
print("   ind declarations: %d pairs, %d indicator variables" % (len(ind_lists), sum(len(l) - 1 for l in ind_lists.values())))
n_listed_excluded = sum(1 for (i, j), lst in ind_lists.items() for x in lst if excluded(*x))
print("   (info) listed options that are themselves excluded on the store: %d" % n_listed_excluded)

# ---------------------------------------------------------------- polynomials in the shifted variables
VAR = {}
for i in LABELS:
    for nm in ("xi:%d:1" % i, "xi:%d:2" % i, "C:%d" % i, "s:%d" % i):
        VAR[nm] = len(VAR)
VAR["S"] = len(VAR)
NBASE = len(VAR)
for (i, j), lst in sorted(ind_lists.items()):
    for k in range(1, len(lst)):
        VAR["z:%d:%d:%d" % (i, j, k)] = len(VAR)
step = rnd["steps"][0]
check(len(rnd["steps"]) == 1 and set(step.keys()) == {"form", "sense", "value", "centre", "terms"}, "one step with keys form/sense/value/centre/terms")
check(step["form"] == "0" and step["sense"] == "lo", "the step is on the form 0 with sense lo")
value = num(step["value"])
centre = {nm: Fr(0) for nm in VAR}
for k, val in step["centre"].items():
    assert k in VAR and VAR[k] < NBASE, "centre key %r is not a base variable" % k
    centre[k] = num(val)
# y-interval of every variable
YIV = {}
for nm, idx in VAR.items():
    if idx < NBASE:
        YIV[idx] = (SB[nm][0] - centre[nm], SB[nm][1] - centre[nm])
    else:
        YIV[idx] = (Fr(0), Fr(1))


def P_const(c):
    return {(): Fr(c)} if c != 0 else {}


def P_var(nm):
    """the base variable v = c_v + y_v (or an indicator variable z = y_z)."""
    out = {(VAR[nm],): Fr(1)}
    if centre[nm] != 0:
        out[()] = centre[nm]
    return out


def padd(a, b, cb=Fr(1)):
    out = dict(a)
    for m, c in b.items():
        x = out.get(m, Fr(0)) + cb * c
        if x == 0:
            out.pop(m, None)
        else:
            out[m] = x
    return out


def pscale(c, a):
    return {m: c * x for m, x in a.items()} if c != 0 else {}


def pmul(a, b):
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(sorted(ma + mb))
            x = out.get(m, Fr(0)) + ca * cb
            if x == 0:
                out.pop(m, None)
            else:
                out[m] = x
    return out


def P_lin(const, coefs):
    out = P_const(const)
    for nm, c in coefs.items():
        out = padd(out, P_var(nm), c)
    return out


def P_Da(o, t):
    return P_lin(*lin_D(o, t, "a"))


def P_Db(o, t):
    return P_lin(*lin_D(o, t, "b"))


def P_A(o, t):
    return padd(pmul(P_var("C:%d" % o), P_Da(o, t)), pmul(P_var("s:%d" % o), P_Db(o, t)))


def P_B(o, t):
    return padd(pmul(P_var("C:%d" % o), P_Db(o, t)), pmul(P_var("s:%d" % o), P_Da(o, t)), Fr(-1))


def P_Cr(i, j):
    return padd(pmul(P_var("C:%d" % i), P_var("C:%d" % j)), pmul(P_var("s:%d" % i), P_var("s:%d" % j)))


def P_Sr(i, j):
    return padd(pmul(P_var("C:%d" % i), P_var("s:%d" % j)), pmul(P_var("s:%d" % i), P_var("C:%d" % j)), Fr(-1))


def P_q(name):
    ent = node["forms"]["q:" + name]
    out = {}
    for coef, mon in ent:
        c = num(coef)
        assert len(mon) <= 2 and all(m in VAR and VAR[m] < NBASE for m in mon)
        term = P_const(c)
        for m in mon:
            term = pmul(term, P_var(m))
        out = padd(out, term)
    return out


sgn = {"p": 1, "m": -1}
fact_cache = {}


def fact_poly(name):
    if name in fact_cache:
        return fact_cache[name]
    parts = name.split(":")
    kind = parts[0]
    if kind == "box":
        i, k, end = int(parts[1]), int(parts[2]), parts[3]
        assert i in LABELS and k in (1, 2) and end in ("lo", "hi") and len(parts) == 4
        lo, hi = box[i][k - 1]
        P = padd(P_var("xi:%d:%d" % (i, k)), P_const(lo), Fr(-1)) if end == "lo" else padd(P_const(hi), P_var("xi:%d:%d" % (i, k)), Fr(-1))
    elif kind == "arc":
        i, what = int(parts[1]), parts[2]
        assert i in LABELS and len(parts) == 3 and what in ("slo", "shi", "clo", "chi", "chord")
        gm, sm = Pm[i]
        gp, sp = Pp[i]
        if what == "slo":
            P = padd(P_var("s:%d" % i), P_const(sm), Fr(-1))
        elif what == "shi":
            P = padd(P_const(sp), P_var("s:%d" % i), Fr(-1))
        elif what == "clo":
            P = padd(P_var("C:%d" % i), P_const(min(gm, gp)), Fr(-1))
        elif what == "chi":
            P = padd(P_const(cmax[i]), P_var("C:%d" % i), Fr(-1))
        else:
            P = padd(pscale(sp - sm, padd(P_var("C:%d" % i), P_const(gm), Fr(-1))),
                     pscale(gp - gm, padd(P_var("s:%d" % i), P_const(sm), Fr(-1))), Fr(-1))
    elif kind == "wall":
        i, e1, e2, kk, end = int(parts[1]), sgn[parts[2]], sgn[parts[3]], parts[4], parts[5]
        assert i in LABELS and kk in ("x", "y") and end in ("lo", "hi") and len(parts) == 6
        w = ((e1 * abar[i][0] + e2 * bbar[i][0]) / 2, (e1 * abar[i][1] + e2 * bbar[i][1]) / 2)
        Jw = J(w)
        c = 0 if kk == "x" else 1
        X = P_const(p[i][c])
        X = padd(X, P_var("xi:%d:1" % i), frame[i][0][c])
        X = padd(X, P_var("xi:%d:2" % i), frame[i][1][c])
        X = padd(X, P_var("C:%d" % i), w[c])
        X = padd(X, P_var("s:%d" % i), Jw[c])
        P = X if end == "lo" else padd(P_var("S"), X, Fr(-1))
    elif kind == "opt":
        o, t, axis, eps, e1, e2 = int(parts[1]), int(parts[2]), parts[3], sgn[parts[4]], sgn[parts[5]], sgn[parts[6]]
        assert o != t and o in LABELS and t in LABELS and axis in ("a", "b") and len(parts) == 7
        w = ((e1 * abar[t][0] + e2 * bbar[t][0]) / 2, (e1 * abar[t][1] + e2 * bbar[t][1]) / 2)
        nbar = abar[o] if axis == "a" else bbar[o]
        nbar = (eps * nbar[0], eps * nbar[1])
        i, j = min(o, t), max(o, t)
        P = pscale(Fr(eps), P_A(o, t) if axis == "a" else P_B(o, t))
        P = padd(P, P_Cr(i, j), dot(nbar, w))
        P = padd(P, P_Sr(i, j), dot(nbar, J(w)) * (1 if (o, t) == (i, j) else -1))
        P = padd(P, P_const(Fr(1, 2)), Fr(-1))
    elif kind == "circ":
        i = int(parts[1])
        assert i in LABELS and len(parts) == 2
        P = padd(padd(pmul(P_var("C:%d" % i), P_var("C:%d" % i)), pmul(P_var("s:%d" % i), P_var("s:%d" % i))), P_const(1), Fr(-1))
    elif kind == "sq":
        q = P_q(parts[1])
        P = pmul(q, q)
    elif kind == "pol":
        P = P_q(parts[1])
    elif kind == "ind":
        i, j, k = int(parts[1]), int(parts[2]), int(parts[3])
        assert i < j and (i, j) in ind_lists and 1 <= k <= len(ind_lists[(i, j)]) and len(parts) == 4 and len(parts[3]) == 1
        m = len(ind_lists[(i, j)])
        if k < m:
            P = P_var("z:%d:%d:%d" % (i, j, k))
        else:
            P = P_const(1)
            for kk in range(1, m):
                P = padd(P, P_var("z:%d:%d:%d" % (i, j, kk)), Fr(-1))
    else:
        raise AssertionError("fact kind %r not handled by this checker" % kind)
    if kind not in ("sq", "pol"):
        fact_cache[name] = P
    return P


def option_of_name(name):
    parts = name.split(":")
    return (int(parts[1]), int(parts[2]), parts[3], sgn[parts[4]])


# ---------------------------------------------------------------- the terms: rules (T1)-(T4), Rem
Rem = {}
nterm = 0
bad_T = {"T1": 0, "T2": 0, "T3": 0, "T4": 0}
pattern_counts = {}
for lam_s, names in step["terms"]:
    lam = num(lam_s)
    assert 1 <= len(names) <= 3
    kinds = [n.split(":")[0] for n in names]
    has_circ = "circ" in kinds
    if lam < 0 and not has_circ:
        bad_T["T1"] += 1
    if "pol" in kinds and not has_circ:
        bad_T["T2"] += 1
    # (T3) guard rule and (T4) availability of opt names
    for n in names:
        k0 = n.split(":")[0]
        if k0 == "opt":
            opt = option_of_name(n)
            i, j = min(opt[0], opt[1]), max(opt[0], opt[1])
            if opt in opt_avail:
                pass
            elif (i, j) in ind_lists and opt in ind_lists[(i, j)]:
                kk = ind_lists[(i, j)].index(opt) + 1
                if ("ind:%d:%d:%d" % (i, j, kk)) not in names:
                    bad_T["T3"] += 1
            else:
                bad_T["T4"] += 1
        elif k0 in ("sq", "pol"):
            if ("q:" + n.split(":", 1)[1]) not in node["forms"]:
                bad_T["T4"] += 1
        elif k0 == "ind":
            i, j, kk = int(n.split(":")[1]), int(n.split(":")[2]), int(n.split(":")[3])
            if (i, j) not in ind_lists or not (1 <= kk <= len(ind_lists[(i, j)])):
                bad_T["T4"] += 1
        elif k0 in ("box", "arc", "wall", "circ"):
            pass
        else:
            bad_T["T4"] += 1
    P = {(): Fr(1)}
    for n in names:
        P = pmul(P, fact_poly(n))
    Rem = padd(Rem, P, -lam)
    nterm += 1
    if nterm % 5000 == 0:
        print("   ... %d terms, Rem has %d monomials, %.0f s" % (nterm, len(Rem), time.time() - T0), flush=True)
check(nterm == 48209, "48209 terms read")
check(all(x == 0 for x in bad_T.values()), "term rules (T1) lambda >= 0 unless circ, (T2) pol only with circ, (T3) guard rule, (T4) availability: violations %s" % bad_T)
print("   Rem: %d monomials; max degree %d" % (len(Rem), max((len(m) for m in Rem), default=0)))

# ---------------------------------------------------------------- the CENTRED RULE
L = Fr(0)
for m, r in Rem.items():
    iv = (Fr(1), Fr(1))
    for idx in m:
        iv = imul(iv, YIV[idx])
    L += min(r * iv[0], r * iv[1])
print("   L = %s (~ %.9g), value = %s (~ %.9g)" % (str(L)[:60] + "...", float(L), value, float(value)))
check(L >= value > 0, "the 0 step is ACCEPTED: L >= value > 0")
rep = json.load(open(REPORT))
repL = Fr(rep["nodes"][0]["zero_step_L"])
check(repL == L, "L equals the zero_step_L of the author's stored acceptance report exactly (cross-check)")

# ---------------------------------------------------------------- the proposed store and the closure
st = rnd["store"]
check(set(st.keys()) == {"S", "box", "arc", "rarc", "cuts"} and st["rarc"] == {} and st["cuts"] == {}, "store keys; no rarc, no cuts")
ok = num(st["S"][0]) <= S_lo and num(st["S"][1]) >= S_hi
for i in LABELS:
    ok &= num(st["box"][str(i)][0][0]) <= box[i][0][0] and num(st["box"][str(i)][0][1]) >= box[i][0][1]
    ok &= num(st["box"][str(i)][1][0]) <= box[i][1][0] and num(st["box"][str(i)][1][1]) >= box[i][1][1]
    lo, hi = rot(st["arc"][str(i)]["lo"]), rot(st["arc"][str(i)]["hi"])
    ok &= lo[0] > 0 and hi[0] > 0 and lo[1] <= Pm[i][1] and hi[1] >= Pp[i][1]
check(ok, "every entry of the proposed store is accepted (each is the old entry or looser)")
check(node["close"] == {"kind": "infeasible"}, "closure infeasible, evidenced by the accepted 0 step of the evaluated round")
print()
print("CONCLUSION: F(root) is empty: no feasible configuration (17 labels, S = Sref) has every xi in the root box and every a_i in the root arc.")
print("time %.0f s" % (time.time() - T0))
print("FAILURES:", len(fails))
for f in fails:
    print("  -", f)
