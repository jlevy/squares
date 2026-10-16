"""Independent re-evaluation of sq19's 2,304 endgame native facts `checkNat n = true`.

Each fact asserts, for one of the 4,096 sign/owner cases of the local endgame,
that on the whole angle box H of `Hull.prob`
  (geometry) the three Farkas multipliers lam1, lam2, lam3 are >= 0 and S1 > 0;
  (slope)    the directional derivative of the endpoint margin along each of the
             case's five direction prefixes is >= 0.
This program rebuilds the row expressions of `Case.P`, `Case.Q`, `Case.F`
(Endgame/RowsH.lean, RowsAH.lean, PhiExpr.lean, Combine.lean,
AngleReduction.lean, ReductionCases.lean, read and transcribed by hand) and
decides both inequalities with its own rigorous interval arithmetic: fixed-point
outward rounding at 2^-160, cos and sin of (M pi/4 + theta) from exact quarter-turn
values and the bounds |sin x - x| <= |x|^3/6, 1 - x^2/2 <= cos x <= 1, and
forward-mode differentiation for the slope. It does not use the source's Taylor
forms, trig table or derivative code. The box H is read from
Endgame/HullData.lean; the canonical case list from the shard modules.

    python -I check_endgame.py SQ19_DIR [--cases all|canonical|N,N,...] [--json OUT]

Standard library only.
"""

import argparse
import glob
import json
import math
import random
import re
import sys
from fractions import Fraction as F

K = 160
ONE = 1 << K
NUM = r"-?\d+(?:/\d+)?"


# ---------------------------------------------------------------- fixed-point intervals


def fdown(q):
    q = F(q)
    return (q.numerator << K) // q.denominator


def fup(q):
    q = F(q)
    return -((-q.numerator << K) // q.denominator)


class I:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi):
        assert lo <= hi
        self.lo, self.hi = lo, hi

    @staticmethod
    def of(q):
        return I(fdown(q), fup(q))

    def __add__(self, o):
        return I(self.lo + o.lo, self.hi + o.hi)

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, o):
        return self + (-o)

    def __mul__(self, o):
        ps = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return I(min(ps) >> K, -((-max(ps)) >> K))

    def abs(self):
        if self.lo >= 0:
            return self
        if self.hi <= 0:
            return -self
        return I(0, max(-self.lo, self.hi))

    def lo_f(self):
        return self.lo / ONE

    def hi_f(self):
        return self.hi / ONE


ZERO = I(0, 0)
# sqrt(2)/2 enclosed from an integer square root (independent of the source's s2 constant).
_r = math.isqrt(2 * 10**100)
R2 = I(fdown(F(_r, 2 * 10**50)), fup(F(_r + 1, 2 * 10**50)))
QUARTER = {0: (I.of(1), ZERO), 1: (R2, R2), 2: (ZERO, I.of(1)), 3: (-R2, R2),
           4: (I.of(-1), ZERO), 5: (-R2, -R2), 6: (ZERO, I.of(-1)), 7: (R2, -R2)}


# ---------------------------------------------------------------- expressions (Ex)


def c(q):
    return ("c", F(q))


def cs(s, M):
    return ("cs", s, M)


def sn(s, M):
    return ("sn", s, M)


def add(a, b):
    return ("add", a, b)


def mul(a, b):
    return ("mul", a, b)


def neg(a):
    return ("neg", a)


def ab(a):
    return ("abs", a)


def cosD(s, M, t, M2):
    return add(mul(cs(s, M), cs(t, M2)), mul(sn(s, M), sn(t, M2)))


def sinD(s, M, t, M2):
    return add(mul(sn(s, M), cs(t, M2)), neg(mul(cs(s, M), sn(t, M2))))


def suppE(sg2, s, M, t, M2):
    sc, ss = sg2
    return mul(c(F(1, 2)), add(mul(c(sc), cosD(s, M, t, M2)), mul(c(ss), sinD(s, M, t, M2))))


def suppAbsE(s, M, t, M2):
    return mul(c(F(1, 2)), add(ab(cosD(s, M, t, M2)), ab(sinD(s, M, t, M2))))


def sg(b):
    return 1 if b else -1


# Rows: (ax, ay, b0, b1), the row ax x + ay y <= b0 + b1 L.


def ProwB(j, Y, sig):
    h1x_s, h2y_s, h2n_s, anc = sig
    cj, sj = cs(j, 0), sn(j, 0)
    h1x = suppE(h1x_s, 0, 0, 1, 0)
    h2y = suppE(h2y_s, 0, 2, 2, 0)
    h2n = suppE(h2n_s, 14, 3, 2, 0)
    h13n = suppAbsE(14, 3, 13, 1)
    anch = add(c(F(1, 2)), anc)
    return (mul(cj, cs(14, 3)), mul(cj, sn(14, 3)),
            add(mul(cs(14, 3), add(add(mul(cj, h1x), anch), neg(mul(sj, c(Y))))),
                mul(cj, add(add(add(neg(mul(sn(14, 3), h2y)), neg(h2n)), c(-1)), neg(h13n)))),
            mul(cj, sn(14, 3)))


def ProwA(j, Y, O, sig):
    h1x_s, h2y_s, h2n_s, anc = sig
    cj = cs(j, 0)
    cd, sd = cosD(14, 1, 13, 1), sinD(14, 1, 13, 1)
    h1x = suppE(h1x_s, 0, 0, 1, 0)
    h2y = suppE(h2y_s, 0, 2, 2, 0)
    h2n = suppE(h2n_s, 13, 3, 2, 0)
    h14n = suppAbsE(13, 3, 14, 1)
    xbound = add(add(mul(cj, h1x), add(c(F(1, 2)), anc)), neg(mul(sn(j, 0), c(Y))))
    base = add(mul(cs(13, 3), xbound),
               mul(cj, add(add(add(neg(mul(sn(13, 3), h2y)), neg(h2n)), c(F(-1, 2))), neg(h14n))))
    return (mul(mul(cj, cd), cs(13, 3)), mul(mul(cj, cd), sn(13, 3)),
            add(mul(cd, base), neg(mul(cj, add(c(F(1, 2)), mul(sd, c(O)))))),
            mul(mul(cj, cd), sn(13, 3)))


def QrowB(sig):
    h10x_s, h10y_s, h10n_s = sig
    h10x = suppE(h10x_s, 0, 0, 10, 0)
    h10y = suppE(h10y_s, 0, 2, 10, 0)
    h10n = suppE(h10n_s, 11, 1, 10, 0)
    h13n = suppAbsE(11, 1, 13, 1)
    return (cs(11, 1), sn(11, 1),
            add(add(add(neg(mul(cs(11, 1), h10x)), neg(mul(sn(11, 1), h10y))), neg(h10n)),
                add(c(-1), neg(h13n))),
            add(cs(11, 1), sn(11, 1)))


def QrowA(O, sig):
    h10x_s, h10y_s, h10n_s = sig
    cd, sd = cosD(11, 1, 13, 1), sinD(11, 1, 13, 1)
    h10x = suppE(h10x_s, 0, 0, 10, 0)
    h10y = suppE(h10y_s, 0, 2, 10, 0)
    h10n = suppE(h10n_s, 13, 1, 10, 0)
    h11n = suppAbsE(13, 1, 11, 1)
    base = add(add(add(neg(mul(cs(13, 1), h10x)), neg(mul(sn(13, 1), h10y))), neg(h10n)),
               add(c(F(-1, 2)), neg(h11n)))
    return (mul(cd, cs(13, 1)), mul(cd, sn(13, 1)),
            add(mul(cd, base), neg(add(c(F(1, 2)), mul(sd, c(O))))),
            mul(cd, add(cs(13, 1), sn(13, 1))))


def F1rowPos8(X5, s5y, s13w, s5w):
    h5y = suppE(s5y, 0, 2, 5, 0)
    h13w = suppE(s13w, 8, 2, 13, 1)
    return (neg(cs(8, 2)), neg(sn(8, 2)),
            neg(add(add(add(add(mul(cs(8, 2), c(X5)), mul(sn(8, 2), h5y)), c(F(1, 2))), s5w),
                    add(c(F(1, 2)), h13w))),
            c(0))


def F1rowNeg(j, X, Xh, s5y, s13w, sanc):
    h5y = suppE(s5y, 0, 2, 5, 0)
    h13w = suppE(s13w, 8, 2, 13, 1)
    anch = add(c(F(1, 2)), sanc)
    c8, cj = cs(8, 0), cs(j, 0)
    return (c(0), neg(mul(c8, cj)),
            neg(add(mul(c8, add(mul(cj, h5y), add(anch, mul(sn(j, 0), c(X))))),
                    mul(cj, add(add(c(F(1, 2)), h13w), mul(sn(8, 0), c(Xh)))))),
            c(0))


def F1rowPos5(X5, Cx, Cy, s5y, s13w, s8m):
    h5y = suppE(s5y, 0, 2, 5, 0)
    h13w = suppE(s13w, 8, 2, 13, 1)
    M0 = add(neg(mul(sn(5, 0), c(X5))), mul(cs(5, 0), h5y))
    W8 = add(mul(cosD(8, 0, 5, 0), add(add(M0, c(F(1, 2))), s8m)),
             neg(mul(sinD(8, 0, 5, 0), add(mul(cs(5, 0), c(Cx)), mul(sn(5, 0), c(Cy))))))
    return (neg(cs(8, 2)), neg(sn(8, 2)), neg(add(add(W8, c(F(1, 2))), h13w)), c(0))


def anchor58E(bd):
    return mul(c(F(1, 2)), add(cosD(8, 0, 5, 0), mul(c(sg(bd)), sinD(8, 0, 5, 0))))


def crossE(ax, ay, bx, by):
    return add(mul(ax, by), neg(mul(ay, bx)))


# ---------------------------------------------------------------- the case family


def parse_hull(text):
    body = text.split("def prob : Prob := ⟨[", 1)[1].split("]⟩", 1)[0]
    sqs = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("⟨"):
            continue
        s, m = (int(x) for x in re.match(r"⟨(\d+), (\d+),", line).groups())
        q = [F(x) for x in re.findall(rf"\(({NUM}) : ℚ\)", line)]
        sqs.append({"s": s, "m": m, "rx": q[0], "ry": q[1], "a": (q[2], q[3]), "x": (q[4], q[5]), "y": (q[6], q[7])})
    return sqs


def dIv(rA, rB, IA, IB):
    return (rB + IB[0] - rA - IA[1], rB + IB[1] - rA - IA[0])


class Family:
    def __init__(self, hull, tightP, tightQ):
        self.hull = hull
        sq = hull
        self.dY12 = dIv(sq[0]["ry"], sq[1]["ry"], sq[0]["y"], sq[1]["y"])
        self.dX58 = dIv(sq[2]["rx"], sq[4]["rx"], sq[2]["x"], sq[4]["x"])
        self.dX813 = dIv(sq[4]["rx"], sq[7]["rx"], sq[4]["x"], sq[7]["x"])
        self.absX = lambda i: (sq[i]["rx"] + sq[i]["x"][0], sq[i]["rx"] + sq[i]["x"][1])
        self.absY = lambda i: (sq[i]["ry"] + sq[i]["y"][0], sq[i]["ry"] + sq[i]["y"][1])
        self.tightP, self.tightQ = tightP, tightQ

    @staticmethod
    def case(n):
        b = [(n >> k) & 1 == 1 for k in range(12)]
        keys = ["pa", "qa", "owner12", "owner58", "b1", "b2", "b5", "b8", "b10", "fiveLarger", "pd", "qd"]
        return dict(zip(keys, b))

    @staticmethod
    def bd58(cc):
        if cc["b5"] == cc["b8"]:
            return (not cc["b8"]) if cc["fiveLarger"] else cc["b8"]
        return cc["b8"]

    def rows(self, cc):
        j12 = 2 if cc["owner12"] else 1
        j58 = 8 if cc["owner58"] else 5
        Y = self.dY12[1] if (cc["b2"] if cc["owner12"] else cc["b1"]) else self.dY12[0]
        sigP = ((1, -sg(cc["b1"])), (sg(cc["b2"]), 1), (-1, 1), c(F(1, 2)))
        if cc["pa"]:
            P = ProwA(j12, Y, self.tightP[0] if cc["pd"] else self.tightP[1], sigP)
        else:
            P = ProwB(j12, Y, sigP)
        sigQ = ((1, -sg(cc["b10"])), (sg(cc["b10"]), 1), (1, 1))
        Q = QrowA(self.tightQ[0] if cc["qd"] else self.tightQ[1], sigQ) if cc["qa"] else QrowB(sigQ)
        bd = self.bd58(cc)
        if cc["b8"]:
            if cc["owner58"]:
                Fr = F1rowPos8(self.absX(2)[1], (sg(cc["b5"]), 1), (1, 1), anchor58E(bd))
            else:
                Fr = F1rowPos5(self.absX(2)[1] if cc["b5"] else self.absX(2)[0],
                               self.absX(4)[1] if bd else self.absX(4)[0],
                               self.absY(4)[1] if bd == cc["b5"] else self.absY(4)[0],
                               (sg(cc["b5"]), 1), (1, 1), anchor58E(bd))
        else:
            X = self.dX58[0] if (cc["b8"] if cc["owner58"] else cc["b5"]) else self.dX58[1]
            Fr = F1rowNeg(j58, X, self.dX813[1], (sg(cc["b5"]), 1), (1, 1), anchor58E(bd))
        return P, Q, Fr

    def exprs(self, cc):
        P, Q, Fr = self.rows(cc)
        lam1 = neg(crossE(Q[0], Q[1], Fr[0], Fr[1]))
        lam2 = neg(crossE(Fr[0], Fr[1], P[0], P[1]))
        lam3 = neg(crossE(P[0], P[1], Q[0], Q[1]))
        S0 = add(add(mul(lam1, P[2]), mul(lam2, Q[2])), mul(lam3, Fr[2]))
        S1 = add(add(mul(lam1, P[3]), mul(lam2, Q[3])), mul(lam3, Fr[3]))
        endpoint = add(c(3), mul(c(F(8, 3)), cs(0, 1)))
        margin = add(neg(S0), neg(mul(endpoint, S1)))
        return lam1, lam2, lam3, S1, margin

    @staticmethod
    def directions(cc):
        def coord(k, b):
            return {k: sg(b)}
        d4 = coord(5, cc["b5"]) if cc["fiveLarger"] else coord(8, cc["b8"])
        return [coord(1, cc["b1"]), coord(2, cc["b2"]), coord(10, cc["b10"]), d4,
                {5: sg(cc["b5"]), 8: sg(cc["b8"])}]


class TM:
    """First-order Taylor model c + sum_k a_k d_k + r, with d_k in the box D_k (theta_k itself)."""

    __slots__ = ("c", "lin", "rem")

    def __init__(self, c, lin, rem):
        self.c, self.lin, self.rem = c, lin, rem


class Evaluator:
    """Rigorous enclosures of an Ex and of its derivative along v, on a box of angles."""

    def __init__(self, box):
        self.D = {s: I(fdown(lo), fup(hi)) for s, (lo, hi) in box.items()}
        self.rc, self.rs = {}, {}
        self.moving_abs = 0
        for s, (lo, hi) in box.items():
            m = max(abs(lo), abs(hi))
            self.rc[s] = I(fdown(-m * m / 2), 0)  # cos d - 1
            self.rs[s] = I(fdown(-m**3 / 6), fup(m**3 / 6))  # sin d - d

    def bound(self, t):
        r = t.c + t.rem
        for k, a in t.lin.items():
            r = r + a * self.D[k]
        return r

    def lbound(self, lin):
        r = ZERO
        for k, a in lin.items():
            r = r + a * self.D[k]
        return r

    def const(self, iv):
        return TM(iv, {}, ZERO)

    def trig(self, s, M, want_cos):
        C, S = QUARTER[M % 8]
        if s not in self.D:  # angle fixed at 0
            return self.const(C if want_cos else S)
        if want_cos:  # cos(a + d) = C - S d + C (cos d - 1) - S (sin d - d)
            return TM(C, {s: -S}, C * self.rc[s] - S * self.rs[s])
        return TM(S, {s: C}, S * self.rc[s] + C * self.rs[s])  # sin(a + d)

    def tadd(self, x, y):
        lin = dict(x.lin)
        for k, a in y.lin.items():
            lin[k] = lin[k] + a if k in lin else a
        return TM(x.c + y.c, lin, x.rem + y.rem)

    def tneg(self, x):
        return TM(-x.c, {k: -a for k, a in x.lin.items()}, -x.rem)

    def tmul(self, x, y):
        lin = {k: a * y.c for k, a in x.lin.items()}
        for k, a in y.lin.items():
            t = a * x.c
            lin[k] = lin[k] + t if k in lin else t
        bx, by = self.lbound(x.lin), self.lbound(y.lin)
        rem = bx * by + x.c * y.rem + y.c * x.rem + bx * y.rem + x.rem * by + x.rem * y.rem
        return TM(x.c * y.c, lin, rem)

    def tabs(self, x):
        b = self.bound(x)
        if b.lo >= 0:
            return x
        if b.hi <= 0:
            return self.tneg(x)
        return self.const(b.abs())

    @staticmethod
    def mentions(e, out):
        if e[0] in ("cs", "sn"):
            out.add(e[1])
        elif e[0] != "c":
            for sub in e[1:]:
                Evaluator.mentions(sub, out)
        return out

    def val(self, e, memo):
        k = id(e)
        if k in memo:
            return memo[k]
        t = e[0]
        if t == "c":
            r = self.const(I.of(e[1]))
        elif t in ("cs", "sn"):
            r = self.trig(e[1], e[2], t == "cs")
        elif t == "add":
            r = self.tadd(self.val(e[1], memo), self.val(e[2], memo))
        elif t == "mul":
            r = self.tmul(self.val(e[1], memo), self.val(e[2], memo))
        elif t == "neg":
            r = self.tneg(self.val(e[1], memo))
        else:
            r = self.tabs(self.val(e[1], memo))
        memo[k] = r
        return r

    def jet(self, e, v, memo):
        """(value, derivative along v) as Taylor models; |a| needs a v-constant or sign-definite a."""
        k = id(e)
        if k in memo:
            return memo[k]
        t = e[0]
        zero = self.const(ZERO)
        if t == "c":
            r = (self.const(I.of(e[1])), zero)
        elif t in ("cs", "sn"):
            w = v.get(e[1], 0)
            cv, sv = self.trig(e[1], e[2], True), self.trig(e[1], e[2], False)
            wc = self.const(I.of(w))
            r = (cv, self.tmul(wc, self.tneg(sv))) if t == "cs" else (sv, self.tmul(wc, cv))
        elif t == "add":
            a, b = self.jet(e[1], v, memo), self.jet(e[2], v, memo)
            r = (self.tadd(a[0], b[0]), self.tadd(a[1], b[1]))
        elif t == "mul":
            a, b = self.jet(e[1], v, memo), self.jet(e[2], v, memo)
            r = (self.tmul(a[0], b[0]), self.tadd(self.tmul(a[1], b[0]), self.tmul(a[0], b[1])))
        elif t == "neg":
            a = self.jet(e[1], v, memo)
            r = (self.tneg(a[0]), self.tneg(a[1]))
        else:
            if not any(v.get(s, 0) for s in self.mentions(e[1], set())):
                r = (self.tabs(self.val(e[1], {})), zero)
            else:
                self.moving_abs += 1
                a = self.jet(e[1], v, memo)
                b = self.bound(a[0])
                if b.lo > 0:
                    r = a
                elif b.hi < 0:
                    r = (self.tneg(a[0]), self.tneg(a[1]))
                else:
                    raise ValueError("abs of a sign-changing operand that moves along v")
        memo[k] = r
        return r

    def lo(self, tm):
        return self.bound(tm).lo_f()


def fval(e, th, memo):
    """Floating-point value of an Ex at angles th (a plausibility sampler, not a proof)."""
    k = id(e)
    if k in memo:
        return memo[k]
    t = e[0]
    if t == "c":
        r = float(e[1])
    elif t == "cs":
        r = math.cos(e[2] * math.pi / 4 + th.get(e[1], 0.0))
    elif t == "sn":
        r = math.sin(e[2] * math.pi / 4 + th.get(e[1], 0.0))
    elif t == "add":
        r = fval(e[1], th, memo) + fval(e[2], th, memo)
    elif t == "mul":
        r = fval(e[1], th, memo) * fval(e[2], th, memo)
    elif t == "neg":
        r = -fval(e[1], th, memo)
    else:
        r = abs(fval(e[1], th, memo))
    memo[k] = r
    return r


def cone_sample(cc, box, rng):
    """A random angle vector of H in the case's signed cone (signs of 1, 2, 5, 8, 10; order of |5|, |8|)."""
    th = {}
    for s, (lo, hi) in box.items():
        lo, hi = float(lo), float(hi)
        bit = {1: "b1", 2: "b2", 5: "b5", 8: "b8", 10: "b10"}.get(s)
        if bit is None:
            th[s] = rng.uniform(lo, hi)
        elif cc[bit]:
            th[s] = rng.uniform(0.0, hi)
        else:
            th[s] = rng.uniform(lo, 0.0)
    a5, a8 = abs(th[5]), abs(th[8])
    if (cc["fiveLarger"] and a5 < a8) or (not cc["fiveLarger"] and a8 < a5):
        # swap magnitudes when the box allows it, else drop the sample
        t5, t8 = math.copysign(a8, th[5] or (1 if cc["b5"] else -1)), math.copysign(a5, th[8] or (1 if cc["b8"] else -1))
        if not (float(box[5][0]) <= t5 <= float(box[5][1]) and float(box[8][0]) <= t8 <= float(box[8][1])):
            return None
        th[5], th[8] = t5, t8
    return th


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("sq19")
    ap.add_argument("--cases", default="canonical")
    ap.add_argument("--samples", type=int, default=8, help="random cone points per case (plausibility)")
    ap.add_argument("--json")
    a = ap.parse_args()
    S = a.sq19 + "/Sq19Lean/"
    hull = parse_hull(open(S + "Endgame/HullData.lean", encoding="utf-8").read())
    ob = open(S + "Endgame/OffsetBounds.lean", encoding="utf-8").read()
    tp = re.search(rf"def tightOffPIv : Iv := ⟨({NUM}), ({NUM})⟩", ob).groups()
    tq = re.search(rf"def tightOffQIv : Iv := ⟨({NUM}), ({NUM})⟩", ob).groups()
    fam = Family(hull, (F(tp[0]), F(tp[1])), (F(tq[0]), F(tq[1])))
    box = {q["s"]: q["a"] for q in hull}
    ev = Evaluator(box)
    ev0 = Evaluator({q["s"]: (F(0), F(0)) for q in hull})
    evaz = Evaluator({q["s"]: (q["a"] if q["s"] in (7, 11, 13, 14) else (F(0), F(0))) for q in hull})
    m0 = [float("inf"), float("-inf")]
    maz = float("inf")
    rng = random.Random(640)
    sampled, sample_bad, sample_min = 0, 0, float("inf")
    shard_dir = a.sq19 + "/s19/certificates/endgame_reduction/canonical"
    canon = sorted(int(m) for p in glob.glob(shard_dir + "/Shard*.lean")
                   for m in re.findall(r"theorem case\d+ : checkNat (\d+) = true := by native_decide",
                                       open(p, encoding="utf-8").read()))
    if a.cases == "canonical":
        cases = canon
    elif a.cases == "all":
        cases = list(range(4096))
    else:
        cases = [int(x) for x in a.cases.split(",")]
    worst = {"lam1": None, "lam2": None, "lam3": None, "S1": None, "slope": None}
    fails, worst_case = [], {}
    for n in cases:
        cc = fam.case(n)
        lam1, lam2, lam3, S1, margin = fam.exprs(cc)
        memo = {}
        vals = {"lam1": ev.lo(ev.val(lam1, memo)), "lam2": ev.lo(ev.val(lam2, memo)),
                "lam3": ev.lo(ev.val(lam3, memo)), "S1": ev.lo(ev.val(S1, memo))}
        good = vals["lam1"] >= 0 and vals["lam2"] >= 0 and vals["lam3"] >= 0 and vals["S1"] > 0
        b0 = ev0.bound(ev0.val(margin, {}))
        m0 = [min(m0[0], b0.lo_f()), max(m0[1], b0.hi_f())]
        maz = min(maz, evaz.lo(evaz.val(margin, {})))
        for _ in range(a.samples):
            th = cone_sample(cc, box, rng)
            if th is None:
                continue
            fm = {}
            sampled += 1
            mval = fval(margin, th, fm)
            sample_min = min(sample_min, mval)
            if mval < -1e-12 or min(fval(x, th, fm) for x in (lam1, lam2, lam3)) < 0 or fval(S1, th, fm) <= 0:
                sample_bad += 1
        slope_lo = None
        for v in fam.directions(cc):
            try:
                d = ev.lo(ev.jet(margin, v, {})[1])
            except ValueError:
                d = float("-inf")
            slope_lo = d if slope_lo is None else min(slope_lo, d)
        vals["slope"] = slope_lo
        good &= slope_lo >= 0
        for key, x in vals.items():
            if worst[key] is None or x < worst[key]:
                worst[key], worst_case[key] = x, n
        if not good:
            fails.append({"n": n, **vals})
    print(f"cases evaluated: {len(cases)} ({a.cases}; the shards hold {len(canon)} native cases)")
    for key in worst:
        print(f"  min lower bound of {key:5s} over H: {worst[key]:.6g} (case {worst_case[key]})")
    print(f"cases failing either inequality: {len(fails)}")
    print(f"note  abs operands moving along a direction: {ev.moving_abs} (0: the source's smoothAlong holds)")
    print(f"note  margin at theta = 0: [{m0[0]:.3g}, {m0[1]:.3g}] over the cases; lower bound on the axis-zero "
          f"face (theta 7, 11, 13, 14 free): {maz:.3g} (the source proves this face exactly, not by intervals)")
    ok = not fails
    print(f"note  {sampled} random points of the cases' cones (floating point): margin min {sample_min:.3g}, "
          f"{sample_bad} with a negative margin or multiplier")
    print("PASS" if ok else "FAIL")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"cone_samples": sampled, "cone_samples_bad": sample_bad, "cone_sample_margin_min": sample_min,
                       "cases": len(cases), "selection": a.cases, "canonical_in_shards": len(canon),
                       "min_lower_bounds": worst, "argmin_case": worst_case, "failures": fails[:50],
                       "failure_count": len(fails), "moving_abs_operands": ev.moving_abs,
                       "margin_at_zero_range": m0, "margin_axis_zero_face_lower": maz,
                       "all_checks_pass": ok}, f, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
