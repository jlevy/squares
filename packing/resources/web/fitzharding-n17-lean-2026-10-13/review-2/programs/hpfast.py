"""Checker functions lifted verbatim from fast_replay.py (no driver)."""
import re
from fractions import Fraction as F
from math import factorial

def rat(s):
    s = s.strip().strip("()")
    if "/" in s:
        a, b = s.split("/")
        return F(int(a.strip("( )")), int(b.strip("( )")))
    return F(int(s))

def parseInts(s):
    out = []
    for tkn in s.split(" "):
        try:
            out.append(int(tkn))
        except ValueError:
            pass  # String.toInt? fails on empty tokens etc.
    return out


# ---------- integer half-plane core (HalfPlaneInt) ----------
def pairUpper(u, v, ta, tb):
    d = u[0] * v[1] - v[0] * u[1]
    l = ta * v[1] - v[0] * tb
    m = u[0] * tb - ta * u[1]
    if d > 0 and l >= 0 and m >= 0:
        return (l * u[2] + m * v[2], d)
    return None


def better(p, q):
    if p is None:
        return q
    if q is None:
        return p
    N1, d1 = p
    N2, d2 = q
    return p if N1 * d2 <= N2 * d1 else q


def pairBoth(u, v, ta, tb):
    if u[0] * v[1] - v[0] * u[1] > 0:
        return pairUpper(u, v, ta, tb)
    return pairUpper(v, u, ta, tb)


def findUpper(hs, ta, tb):
    best = None
    n = len(hs)
    for a in range(n):
        u = hs[a]
        for b in range(a + 1, n):
            best = better(pairBoth(u, hs[b], ta, tb), best) if False else better(best, pairBoth(u, hs[b], ta, tb))
    return best


# NOTE: findUpper in Lean = better (scanPairs u vs) (findUpper vs); scanPairs folds
# better(pairBoth u v, rest) from the left. `better` picks p when N1*d2 <= N2*d1, i.e.
# ties go to the first argument; ordering can matter only for ties, which give equal
# bounds, so any order yields the same rational value. We keep the natural order.


def mkBox(hs):
    return (findUpper(hs, 1, 0), findUpper(hs, -1, 0), findUpper(hs, 0, 1), findUpper(hs, 0, -1))


def selX(bx, a):
    return bx[0] if a >= 0 else bx[1]


def selY(bx, b):
    return bx[2] if b >= 0 else bx[3]


def boxUpper(bx, a, b):
    x = selX(bx, a)
    y = selY(bx, b)
    if x is None or y is None:
        return None
    (N1, d1), (N2, d2) = x, y
    return (abs(a) * N1 * d2 + abs(b) * N2 * d1, d1 * d2)


def gapOK(hi, lo, L, T):
    if hi is None or lo is None:
        return False
    (N1, d1), (N2, d2) = hi, lo
    return (N1 * d2 + N2 * d1) * L < T * (d1 * d2)


def axisOK(S, P, bS, bP, a, b, L, T):
    return (gapOK(boxUpper(bP, a, b), boxUpper(bS, -a, -b), L, T) or gapOK(findUpper(P, a, b), findUpper(S, -a, -b), L, T)) and \
           (gapOK(boxUpper(bS, a, b), boxUpper(bP, -a, -b), L, T) or gapOK(findUpper(S, a, b), findUpper(P, -a, -b), L, T))


def crossNum(C, S, E, Fv):
    return abs(C * E + S * Fv) + abs(C * Fv - S * E)


def collide(S, P, bS, bP, C, Sn, cd, H, hd, E, Fv, ed, K, kd):
    if not (cd > 0 and hd > 0 and ed > 0 and kd > 0 and H > 0 and C * C + Sn * Sn > 0 and K > 0 and E * E + Fv * Fv > 0):
        return False
    L = 2 * hd * cd * kd * ed
    D = crossNum(C, Sn, E, Fv)
    TA = H * (C * C + Sn * Sn) * kd * ed + K * D * hd * cd
    TB = H * D * kd * ed + K * (E * E + Fv * Fv) * hd * cd
    return axisOK(S, P, bS, bP, C, Sn, L, TA) and axisOK(S, P, bS, bP, -Sn, C, L, TA) and \
        axisOK(S, P, bS, bP, E, Fv, L, TB) and axisOK(S, P, bS, bP, -Fv, E, L, TB)


# ---------- state (HalfPlaneState) ----------
def halfSpan(span):
    return (span if span >= 1 else F(1)) / 2


def collideRows(T, cons, bx, es, rows):
    for t in rows:
        if t[2] >= len(T):
            return False
        et = T[t[2]]
        if not collide(cons, t[0], bx, t[1], es["C"], es["S"], es["cd"], es["H"], es["hd"], et["C"], et["S"], et["cd"], et["H"], et["hd"]):
            return False
    return True


def wallOK(span, side, shift, c):
    a, b, q = c
    return (b == 0 and a < 0 and a * (halfSpan(span) - shift) <= q) or \
           (b == 0 and a > 0 and a * (side + shift - halfSpan(span)) <= q) or \
           (a == 0 and b < 0 and b * (halfSpan(span) - shift) <= q) or \
           (a == 0 and b > 0 and b * (side + shift - halfSpan(span)) <= q)


def emptyOK(cons):
    for c in cons:
        r = findUpper(cons, -c[0], -c[1])
        if r is not None and r[0] < -c[2] * r[1]:
            return True
    return False


def dropBits(l, m):
    out = []
    for c in l:
        if m % 2 == 1:
            pass
        else:
            out.append(c)
        m //= 2
    return out


def mkRow(cons, e):
    return (cons, mkBox(cons), e)


def splice(S, i, k, new):
    S = list(S)
    if i < len(S):
        rows = S[i]
        S[i] = rows[:k] + new + rows[k + 1:]
    return S


def rowsOf(S, i):
    return S[i] if i < len(S) else []


def run_step(T, side, shift, S, st):
    tag = st[0]
    if tag == "cut":
        _, i, k, j, keep, m = st
        rows = rowsOf(S, i)
        if k >= len(rows):
            return None
        r = rows[k]
        if r[2] >= len(T):
            return None
        es = T[r[2]]
        opp = (-keep[0], -keep[1], -keep[2])
        cons2 = [opp] + r[0]
        if i != j and j < len(S) and collideRows(T, cons2, mkBox(cons2), es, rowsOf(S, j)):
            return splice(S, i, k, [mkRow(dropBits([keep] + r[0], m), r[2])])
        return None
    if tag == "kill":
        _, i, k, j = st
        rows = rowsOf(S, i)
        if k >= len(rows):
            return None
        r = rows[k]
        if r[2] >= len(T):
            return None
        es = T[r[2]]
        if i != j and j < len(S) and collideRows(T, r[0], r[1], es, rowsOf(S, j)):
            return splice(S, i, k, [])
        return None
    if tag == "wall":
        _, i, k, w, m = st
        rows = rowsOf(S, i)
        if k >= len(rows):
            return None
        r = rows[k]
        if r[2] >= len(T):
            return None
        es = T[r[2]]
        if all(wallOK(es["span"], side, shift, c) for c in w):
            return splice(S, i, k, [mkRow(dropBits(w + r[0], m), r[2])])
        return None
    if tag == "split":
        _, i, k, e1, e2 = st
        rows = rowsOf(S, i)
        if k >= len(rows):
            return None
        r = rows[k]
        if r[2] >= len(T) or e1 >= len(T) or e2 >= len(T):
            return None
        a, a1, a2 = T[r[2]], T[e1], T[e2]
        if a1["lo"] <= a["lo"] and a2["lo"] <= a1["hi"] and a["hi"] <= a2["hi"]:
            return splice(S, i, k, [(r[0], r[1], e1), (r[0], r[1], e2)])
        return None
    if tag == "dead":
        _, i, k = st
        rows = rowsOf(S, i)
        if k >= len(rows):
            return None
        r = rows[k]
        if emptyOK(r[0]):
            return splice(S, i, k, [])
        return None
    raise ValueError(tag)


def toNat(x):
    return x if x >= 0 else 0


def at(a, i):
    return a[i] if 0 <= i < len(a) else 0  # a[i]! on Int defaults to 0 out of range


def getICs(a, pos, n):
    return [(at(a, pos + 3 * t), at(a, pos + 3 * t + 1), at(a, pos + 3 * t + 2)) for t in range(n)]


def decodeSteps(a):
    pos = 0
    acc = []
    while pos < len(a):
        tag = a[pos]
        if tag == 1:
            acc.append(("cut", toNat(at(a, pos + 1)), toNat(at(a, pos + 2)), toNat(at(a, pos + 3)), (at(a, pos + 4), at(a, pos + 5), at(a, pos + 6)), toNat(at(a, pos + 7))))
            pos += 8
        elif tag == 2:
            acc.append(("kill", toNat(at(a, pos + 1)), toNat(at(a, pos + 2)), toNat(at(a, pos + 3))))
            pos += 4
        elif tag == 3:
            n = toNat(at(a, pos + 4))
            acc.append(("wall", toNat(at(a, pos + 1)), toNat(at(a, pos + 2)), getICs(a, pos + 5, n), toNat(at(a, pos + 3))))
            pos += 5 + 3 * n
        elif tag == 4:
            acc.append(("split", toNat(at(a, pos + 1)), toNat(at(a, pos + 2)), toNat(at(a, pos + 3)), toNat(at(a, pos + 4))))
            pos += 5
        elif tag == 5:
            acc.append(("dead", toNat(at(a, pos + 1)), toNat(at(a, pos + 2))))
            pos += 3
        else:
            break
    return acc


def decodeInit(a, S):
    pos = 0
    while pos < len(a):
        i = toNat(at(a, pos))
        n = toNat(at(a, pos + 2))
        row = mkRow(getICs(a, pos + 3, n), toNat(at(a, pos + 1)))
        if i < len(S):
            S[i] = S[i] + [row]
        pos += 3 + 3 * n
    return S


