"""Independent Python replay of the compiled half-plane trace checker on one node.

Re-implements, from the text of Sq17Lean/HalfPlaneFast.lean and CaptureTableFast.lean
(read by eye, not executed), the functions
  parseInts, decodeInit, decodeSteps, findUpper/pairUpper/better, mkBox, boxUpper,
  gapOK, axisOK, collide, collideRows, wallOK, emptyOK, Step.run, runAll, hasEmpty,
  excludes, and the degree-44 Taylor table check (trigCheck, endpointCheck, entryCheck)
with exact Python integers and Fractions, and runs them on a generated node file:
  python3 -I fast_replay.py NODE.lean COMMON.lean [TREE.lean]
where TREE.lean (optional) holds `NodeX.bounds` for the table check.
Prints whether `excludes table side shift 17 S0 steps` evaluates to true here, the
number of steps of each kind, and whether tableOK 44 holds.
"""
import re
import sys
from fractions import Fraction as F
from math import factorial
from pathlib import Path

node_path = Path(sys.argv[1])
common_path = Path(sys.argv[2])
tree_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None
text = node_path.read_text()
ns = re.search(r"^namespace (\S+)", text, re.M).group(1)
node_name = ns.split(".")[-1]


def rat(s):
    s = s.strip().strip("()")
    if "/" in s:
        a, b = s.split("/")
        return F(int(a.strip("( )")), int(b.strip("( )")))
    return F(int(s))


# ---------- table ----------
tbl = text[text.index("def table : Array Entry := #["):text.index("def initRaw")]
entries = []
for m in re.finditer(r"⟨\(?(-?\d+(?:/\d+)?)\)? : Rat\), \(?(-?\d+(?:/\d+)?)\)? : Rat\), (-?\d+), (-?\d+), (-?\d+), (-?\d+), (-?\d+), \(?(-?\d+(?:/\d+)?)\)? : Rat\)⟩", tbl):
    lo, hi, C, S, cd, H, hd, span = m.groups()
    entries.append(dict(lo=rat(lo), hi=rat(hi), C=int(C), S=int(S), cd=int(cd), H=int(H), hd=int(hd), span=rat(span)))
print(f"{node_name}: table entries parsed: {len(entries)}")

common = common_path.read_text()
side = rat(re.search(r"def side : Rat := \((-?\d+/\d+) : Rat\)", common).group(1))
shift = rat(re.search(r"def shift : Rat := \((-?\d+/\d+) : Rat\)", common).group(1))
initRaw = re.search(r'def initRaw : String := "([^"]*)"', text).group(1)
stepsRaw = re.search(r'def stepsRaw : String := "([^"]*)"', text).group(1)


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


S0 = decodeInit(parseInts(initRaw), [[] for _ in range(17)])
steps = decodeSteps(parseInts(stepsRaw))
kinds = {}
for st in steps:
    kinds[st[0]] = kinds.get(st[0], 0) + 1
print(f"{node_name}: owners {len(S0)}, initial rows per owner {[len(r) for r in S0]}, steps {len(steps)} {kinds}")

S = S0
ok = True
for n, st in enumerate(steps):
    S2 = run_step(entries, side, shift, S, st)
    if S2 is None:
        print(f"{node_name}: step {n} ({st[0]}) REJECTED by the replayed checker")
        ok = False
        break
    S = S2
if ok:
    empty = [i for i in range(17) if len(rowsOf(S, i)) == 0]
    print(f"{node_name}: all steps accepted; owners with no live row: {empty}; excludes = {len(empty) > 0}")
    print(f"{node_name}: final rows per owner {[len(r) for r in S]}")

# ---------- table check (degree 44) ----------
if tree_path is not None:
    tt = tree_path.read_text()
    m = re.search(rf"def {node_name}\.bounds : Array \(TrigBounds × TrigBounds\) := #\[(.*?)\n\]", tt, re.S)
    if m is None:
        print("no bounds found in tree file for", node_name)
    else:
        pairs = re.findall(r"\(⟨([^⟩]*)⟩, ⟨([^⟩]*)⟩\)", m.group(1))
        def tb(s):
            v = [rat(x) for x in re.findall(r"\(?-?\d+(?:/\d+)?\)?(?= : ℚ\))", s)]
            if len(v) != 4:
                v = [rat(x) for x in re.findall(r"\(?-?\d+(?:/\d+)?\)?", s)][:4]
            return dict(cosLo=v[0], cosHi=v[1], sinLo=v[2], sinHi=v[3])
        bounds = [(tb(a), tb(b)) for a, b in pairs]
        print(f"{node_name}: bounds parsed: {len(bounds)} (table size {len(entries)})")
        N = 44

        def taylor(x):
            c = s = F(0)
            sign = [1, 0, -1, 0]
            for k in range(N + 1):
                term = x ** k / factorial(k)
                if k % 4 == 0:
                    c += term
                elif k % 4 == 1:
                    s += term
                elif k % 4 == 2:
                    c -= term
                else:
                    s -= term
            return c, s

        def remainder(x):
            return abs(x) ** (N + 1) / factorial(N + 1)

        def trigCheck(x, b):
            c, s = taylor(x)
            r = remainder(x)
            return b["cosLo"] <= c - r and c + r <= b["cosHi"] and b["sinLo"] <= s - r and s + r <= b["sinHi"]

        def endpoint(c, s, b):
            dLo = min(c * b["cosLo"], c * b["cosHi"]) + min(s * b["sinLo"], s * b["sinHi"])
            dHi = max(c * b["cosLo"], c * b["cosHi"]) + max(s * b["sinLo"], s * b["sinHi"])
            xLo = min(c * b["sinLo"], c * b["sinHi"]) + min(-s * b["cosLo"], -s * b["cosHi"])
            xHi = max(c * b["sinLo"], c * b["sinHi"]) + max(-s * b["cosLo"], -s * b["cosHi"])
            return dLo, dHi, xLo, xHi

        def endpointCheck(h, ep):
            dLo, dHi, xLo, xHi = ep
            mx = max(abs(xLo), abs(xHi))
            return h >= 0 and dLo > 0 and dLo <= dHi and xLo <= xHi and mx <= dLo and h * (dHi + mx) <= 1

        def entryCheck(e, b1, b2):
            c = F(e["C"], e["cd"]); s = F(e["S"], e["cd"]); h = F(e["H"], e["hd"])
            if e["lo"] >= 0:
                d = (F(1), F(1))
            elif e["hi"] <= 0:
                d = (F(1), F(-1))
            else:
                d = (F(0), F(0))
            ok = trigCheck(e["lo"], b1) and trigCheck(e["hi"], b2)
            ok &= 0 <= e["hi"] - e["lo"] <= 1
            ok &= endpointCheck(h, endpoint(c, s, b1)) and endpointCheck(h, endpoint(c, s, b2))
            ok &= abs(d[0]) <= 1 and abs(d[1]) <= 1 and e["span"] >= 0 and e["lo"] <= e["hi"] and e["hi"] - e["lo"] <= 1
            ok &= e["span"] <= endpoint(d[0], d[1], b1)[0] and e["span"] <= endpoint(d[0], d[1], b2)[0]
            return ok

        bad = [k for k, (e, (b1, b2)) in enumerate(zip(entries, bounds)) if not entryCheck(e, b1, b2)]
        print(f"{node_name}: tableOK 44 replayed: {len(bad) == 0 and len(bounds) == len(entries)}  (failing entries: {bad[:5]})")
        spans = [float(e["span"]) for e in entries]
        print(f"{node_name}: angle range [{float(min(e['lo'] for e in entries)):.6f}, {float(max(e['hi'] for e in entries)):.6f}], span range [{min(spans):.4f}, {max(spans):.4f}], min core H/hd {float(min(F(e['H'], e['hd']) for e in entries)):.6f}")
