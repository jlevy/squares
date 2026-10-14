"""Numerical sanity tests of the lemmas of SPEC_v3.0.md (sections 4.1-4.8, 5, 8), written from the text.

These are random tests with floats (not proofs): every lemma was also read and re-derived by hand; the tests
guard against a misread of a sign or a convention. Usage: python3 -I spec_lemmas_numeric.py
"""
import math
import random

random.seed(20261013)
fails = []


def check(cond, text):
    print(("OK   " if cond else "FAIL ") + text)
    if not cond:
        fails.append(text)


def rotv(a):
    return (math.cos(a), math.sin(a))


def Jv(v):
    return (-v[1], v[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def corners(q, a):
    b = Jv(a)
    return [(q[0] + (e1 * a[0] + e2 * b[0]) / 2, q[1] + (e1 * a[1] + e2 * b[1]) / 2) for e1 in (1, -1) for e2 in (1, -1)]


def support(a, n):
    b = Jv(a)
    return (abs(dot(n, a)) + abs(dot(n, b))) / 2


def disjoint_interiors(q1, a1, q2, a2):
    # separating axis test with the 4 axes (exact criterion for two squares)
    d = sub(q2, q1)
    for n in (a1, Jv(a1), a2, Jv(a2)):
        if abs(dot(n, d)) >= support(a1, n) + support(a2, n) - 1e-15:
            return True
    return False


def option_holds(qo, ao, qt, at, axis, eps):
    n = ao if axis == "a" else Jv(ao)
    n = (eps * n[0], eps * n[1])
    return all(dot(n, sub(c, qo)) >= 0.5 - 1e-12 for c in corners(qt, at))


# --- 4.5 SAT lemma: disjoint interiors => one of the 8 options holds
bad = 0
for _ in range(20000):
    q1 = (random.uniform(0, 3), random.uniform(0, 3)); q2 = (random.uniform(0, 3), random.uniform(0, 3))
    a1 = rotv(random.uniform(-math.pi, math.pi)); a2 = rotv(random.uniform(-math.pi, math.pi))
    if disjoint_interiors(q1, a1, q2, a2):
        ok = any(option_holds(q1, a1, q2, a2, ax, e) or option_holds(q2, a2, q1, a1, ax, e) for ax in "ab" for e in (1, -1))
        bad += not ok
check(bad == 0, "4.5 SAT lemma: every pair of disjoint squares satisfies one of its 8 options (%d failures)" % bad)

# --- 4.5 option polynomial identity: eps*(A or B) + (nbar.w) cos(psi_t-psi_o) + (nbar.Jw) sin(psi_t-psi_o) - 1/2 = n.(corner_t - q_o) - 1/2
bad = 0
for _ in range(5000):
    abar_o = rotv(random.uniform(-3, 3)); abar_t = rotv(random.uniform(-3, 3))
    po = random.uniform(-0.3, 0.3); pt = random.uniform(-0.3, 0.3)   # psi_o, psi_t
    Co, so, Ct, st = math.cos(po), math.sin(po), math.cos(pt), math.sin(pt)
    ao = (Co * abar_o[0] + so * Jv(abar_o)[0], Co * abar_o[1] + so * Jv(abar_o)[1])
    at = (Ct * abar_t[0] + st * Jv(abar_t)[0], Ct * abar_t[1] + st * Jv(abar_t)[1])
    qo = (random.uniform(0, 3), random.uniform(0, 3)); qt = (random.uniform(0, 3), random.uniform(0, 3))
    d = sub(qt, qo)
    Da, Db = dot(abar_o, d), dot(Jv(abar_o), d)
    A = Co * Da + so * Db; B = Co * Db - so * Da
    for axis in "ab":
        for eps in (1, -1):
            nbar = (eps * abar_o[0], eps * abar_o[1]) if axis == "a" else (eps * Jv(abar_o)[0], eps * Jv(abar_o)[1])
            n = ao if axis == "a" else Jv(ao); n = (eps * n[0], eps * n[1])
            for e1 in (1, -1):
                for e2 in (1, -1):
                    w = ((e1 * abar_t[0] + e2 * Jv(abar_t)[0]) / 2, (e1 * abar_t[1] + e2 * Jv(abar_t)[1]) / 2)
                    corner = (qt[0] + Ct * w[0] + st * Jv(w)[0], qt[1] + Ct * w[1] + st * Jv(w)[1])
                    lhs = eps * (A if axis == "a" else B) + dot(nbar, w) * math.cos(pt - po) + dot(nbar, Jv(w)) * math.sin(pt - po) - 0.5
                    rhs = dot(n, sub(corner, qo)) - 0.5
                    bad += abs(lhs - rhs) > 1e-9
check(bad == 0, "4.5 corner polynomial identity (%d failures)" % bad)

# --- 4.6 class dictionary and Lemma P
bad = 0; badP = 0; tested = 0
for _ in range(40000):
    ai = rotv(random.uniform(-3, 3)); aj = rotv(random.uniform(-3, 3))
    qi = (random.uniform(0, 3), random.uniform(0, 3)); qj = (random.uniform(0, 3), random.uniform(0, 3))
    d = sub(qj, qi)
    for axi, ei, axj, ej in [(x, s, y, t) for x in "ab" for s in (1, -1) for y in "ab" for t in (1, -1)]:
        ni = ai if axi == "a" else Jv(ai); ni = (ei * ni[0], ei * ni[1])
        nj = aj if axj == "a" else Jv(aj); nj = (ej * nj[0], ej * nj[1])
        al, be, co, si = dot(ni, d), dot(nj, d), dot(ni, nj), dot(Jv(ni), nj)
        Y = dot(Jv(ni), d) + dot(Jv(nj), d)
        if co > -0.999:
            bad += abs((be - al) - si * Y / (1 + co)) > 1e-9
        # options O_i = (i,j,axi,ei), O_j = (j,i,axj,-ej)
        Oi = option_holds(qi, ai, qj, aj, axi, ei); Oj = option_holds(qj, aj, qi, ai, axj, -ej)
        if (Oi or Oj) and co > -0.999:
            tested += 1
            m = (1 + co + abs(si)) / 2
            if Oi and al < m - 1e-9: badP += 1
            if Oj and be < m - 1e-9: badP += 1
            if 0 <= Y <= 1 + co:
                if be < (1 + co + si) / 2 - 1e-9 or al < (1 + co - si) / 2 - 1e-9: badP += 1
            if -(1 + co) <= Y <= 0:
                if al < (1 + co + si) / 2 - 1e-9 or be < (1 + co - si) / 2 - 1e-9: badP += 1
            # Pk with kappa = 1 - |Y|/(1+co) (the largest allowed), inside the lemma's precondition |Y| <= 1 + co
            if abs(Y) <= 1 + co:
                kap = 1 - abs(Y) / (1 + co)
                if al + be < 1 + co + kap * si - 1e-9 or al + be < 1 + co - kap * si - 1e-9: badP += 1
check(bad == 0, "4.6 identity be - al = si Y/(1+co) (%d failures)" % bad)
check(badP == 0, "4.6 Lemma P (P+, P-, Pk) on %d option-satisfying samples (%d failures)" % (tested, badP))

# --- 4.6 kind Ps: co + si - 1 >= kp si on 0 <= theta <= theta+ (concavity of g(s) = sqrt(1-s^2)+s-1)
bad = 0
for _ in range(2000):
    thp = random.uniform(0.001, 1.5)
    sp = math.sin(thp); kp = (math.cos(thp) + sp - 1) / sp
    for th in [random.uniform(0, thp) for _ in range(20)]:
        bad += math.cos(th) + math.sin(th) - 1 < kp * math.sin(th) - 1e-12
check(bad == 0, "4.6 Ps: cos t + sin t - 1 >= kp sin t on [0, t+] (%d failures)" % bad)

# --- 4.7 exclusion: h = (|cos th| + |sin th|)/2 >= h_lo when the arc from E- to E+ lies in one closed quadrant and is shorter than pi/2
bad = 0
for _ in range(20000):
    em = random.uniform(-math.pi, math.pi); length = random.uniform(0, math.pi / 2 - 1e-6)
    ep = em + length
    Em, Ep = rotv(em), rotv(ep)
    turn = rotv(ep - em)
    if Em[0] * Ep[0] >= 0 and Em[1] * Ep[1] >= 0 and turn[0] > 0 and turn[1] >= 0:
        h_lo = min(abs(Em[0]) + abs(Em[1]), abs(Ep[0]) + abs(Ep[1])) / 2
        for th in [em + random.uniform(0, length) for _ in range(10)]:
            bad += (abs(math.cos(th)) + abs(math.sin(th))) / 2 < h_lo - 1e-12
check(bad == 0, "4.7 h_lo is a lower bound of (|cos|+|sin|)/2 on an arc inside one quadrant (%d failures)" % bad)

# --- 4.2 arc facts: chord and tangent
bad = 0
for _ in range(20000):
    pm = random.uniform(-1.5, 1.5); pp = random.uniform(pm, 1.5)
    psi = random.uniform(pm, pp)
    C, s = math.cos(psi), math.sin(psi)
    gm, sm = math.cos(pm), math.sin(pm); gp, sp = math.cos(pp), math.sin(pp)
    chord = (C - gm) * (sp - sm) - (s - sm) * (gp - gm)
    bad += chord < -1e-12
    cmin = min(gm, gp); cmax = 1 if sm <= 0 <= sp else max(gm, gp)
    bad += (C < cmin - 1e-12) or (C > cmax + 1e-12) or (s < sm - 1e-12) or (s > sp + 1e-12)
    G = random.uniform(-1, 1); H = random.uniform(-1, 1)
    if G * G + H * H <= 1:
        bad += 1 - G * C - H * s < -1e-12
check(bad == 0, "4.2 arc facts slo/shi/clo/chi/chord/tan hold on the arc (%d failures)" % bad)

# --- 4.8 wall support facts
bad = 0
for _ in range(5000):
    tm = random.uniform(-1.4, 0); tp = random.uniform(0, 1.4)
    Vm, Vp = rotv(tm), rotv(tp)
    kp = (Vp[0] + Vp[1] - 1) / Vp[1] if Vp[1] > 0 else 0
    km = (Vm[0] - Vm[1] - 1) / (-Vm[1]) if Vm[1] < 0 else 0
    for t in [random.uniform(tm, tp) for _ in range(10)]:
        sigma = math.sin(t)
        D = (abs(math.cos(t)) + abs(math.sin(t))) / 2 + random.uniform(0, 0.5)   # a wall distance that satisfies (F1)
        bad += D - 0.5 - (kp / 2) * sigma < -1e-12
        bad += D - 0.5 + (km / 2) * sigma < -1e-12
check(bad == 0, "4.8 wsup facts hold when the arc contains the x-axis direction (%d failures)" % bad)

# --- section 8: root-contains-window and terminal test (asin x >= x; sin x >= x - x^3/6)
bad = 0
for _ in range(2000):
    al = random.uniform(0.001, 0.999)
    bad += math.asin(al) < al - 1e-12                   # a root end with sin >= alpha has angle >= alpha
    aT = random.uniform(0.001, 1)
    bad += math.sin(aT) < aT - aT ** 3 / 6 - 1e-12       # terminal test bound
check(bad == 0, "section 8: asin x >= x on [0,1) and sin x >= x - x^3/6 on [0,1] (%d failures)" % bad)

# --- section 5 raw rule: monomial interval bound (sanity) on random polynomials
bad = 0
for _ in range(2000):
    n = 4
    lo = [random.uniform(-1, 0) for _ in range(n)]; hi = [l + random.uniform(0, 1) for l in lo]
    terms = [(random.uniform(-2, 2), [random.randrange(n) for _ in range(random.randint(0, 3))]) for _ in range(6)]
    L = 0
    for c, m in terms:
        a, b = 1.0, 1.0
        for v in m:
            cands = [a * lo[v], a * hi[v], b * lo[v], b * hi[v]]
            a, b = min(cands), max(cands)
        L += min(c * a, c * b)
    for _ in range(20):
        x = [random.uniform(lo[i], hi[i]) for i in range(n)]
        val = sum(c * math.prod(x[v] for v in m) for c, m in terms)
        bad += val < L - 1e-9
check(bad == 0, "section 5 raw rule: L is a lower bound of Rem on the box (%d failures)" % bad)

# --- the chord inequality sin x + sin y - sin(x+y) >= 0 for x,y >= 0, x+y < pi
bad = 0
for _ in range(20000):
    x = random.uniform(0, math.pi); y = random.uniform(0, math.pi - x)
    bad += math.sin(x) + math.sin(y) - math.sin(x + y) < -1e-12
check(bad == 0, "4.2 chord: sin x + sin y - sin(x+y) >= 0 (%d failures)" % bad)

print()
print("FAILURES:", len(fails))
