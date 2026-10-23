"""Lean certificate from a minpoly.py output: writes a Lean file whose theorem
  ∃ s, pS(s) = 0 ∧ Sa ≤ s ≤ Sb ∧ Packs n s
is proved by `EC.packs_exact` and `decide +kernel` (lean/Sqpack/ExactCheck.lean).

The checks are replayed here in Python with exactly the Lean checker's arithmetic (same division, same positivity
bound), so the generated file is expected to compile; the t interval is narrowed by exact bisection until every
strict bound passes, and each pair gets a separating side line.

Rational shadows (lean/Sqpack/ShadowCheck.lean): each square gets rational enclosures of (x, y, c, s) at 20 digits,
proved once in the field; walls and pairs that pass the cheap interval / disc tests (replayed here with the same
arithmetic) need no field conditions.  Only contacts and near-contacts keep exact ones.

  python3 lean_cert.py minpoly/solve/n-11.minpoly.json ../../lean/Sqpack/Exact/N11.lean
"""
import sys, json, gzip
from fractions import Fraction as F


# ------------------------------------------------------------------ the Lean checker's polynomial arithmetic
def padd(p, q):
    if not p:
        return list(q)
    if not q:
        return list(p)
    return [p[0] + q[0]] + padd(p[1:], q[1:]) if len(p) < 400 and len(q) < 400 else _padd_it(p, q)


def _padd_it(p, q):
    r = []
    for i in range(max(len(p), len(q))):
        if i < len(p) and i < len(q):
            r.append(p[i] + q[i])
        elif i < len(p):
            r.append(p[i])
        else:
            r.append(q[i])
    return r


def psmul(c, p):
    return [c * x for x in p]


def psub(p, q):
    return padd(p, psmul(F(-1), q))


def pmul(p, q):
    if not p:
        return []
    r = [F(0)] * (len(p) + len(q) - 1) if q else []
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    # Lean's pmul keeps the length len(p) + len(q) - 1 (no trimming); the value is what matters
    return r


def pdivmod(p, f):
    fr = list(reversed(f))
    if not fr:
        return [], p
    lc, fd = fr[0], fr[1:]
    q, pr = [], list(reversed(p))
    for _ in range(len(p)):
        if len(pr) <= len(fd):
            break
        c = pr[0]
        k = c / lc
        rest = pr[1:]
        rest = [x - k * fd[i] if i < len(fd) else x for i, x in enumerate(rest)]
        q = [k] + q
        pr = rest
    return q, list(reversed(pr))


def qeval(p, t):
    v = F(0)
    for c in reversed(p):
        v = c + t * v
    return v


def bndA(R, p):
    v = F(0)
    for c in reversed(p):
        v = abs(c) + R * v
    return v


def bndB(R, p):
    # bndB (c :: p) = bndA p + R * bndB p
    A, B = F(0), F(0)
    for c in reversed(p):
        A, B = abs(c) + R * A, A + R * B
    return B


def all_zero(p):
    return all(x == 0 for x in p)


class Ctx:
    def __init__(self, f, a, b):
        self.f, self.a, self.b = f, a, b
        self.m, self.w, self.R = (a + b) / 2, (b - a) / 2, max(abs(a), abs(b))

    def nonneg(self, N):
        """None if fails, 'eq' or 'gt'; also the margin r(m) - w B for diagnostics."""
        q, r = pdivmod(N, self.f)
        assert all_zero(psub(N, padd(pmul(q, self.f), r))), 'division identity failed'
        if all_zero(r):
            return 'eq', None
        val, B = qeval(r, self.m), bndB(self.R, r)
        return ('gt' if self.w * B < val else None), (val, B)


# ------------------------------------------------------------------ geometry, as in ExactCheck.lean
def csN0(sq):
    u = sq['u']
    c, s = psub([F(1)], pmul(u, u)), psmul(F(2), u)
    for _ in range(sq['m']):
        c, s = psmul(F(-1), s), c
    return c, s


def dd0(sq):
    return padd([F(1)], pmul(sq['u'], sq['u']))


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def add_reduced(sq, f):
    """The stored c, s, d (reduced mod f), as the Lean SqD fields."""
    c0, s0 = csN0(sq)
    sq['c'] = trim(pdivmod(c0, f)[1]) or [F(0)]
    sq['s'] = trim(pdivmod(s0, f)[1]) or [F(0)]
    sq['d'] = trim(pdivmod(dd0(sq), f)[1]) or [F(0)]


def csN(sq):
    return sq['c'], sq['s']


def dd(sq):
    return sq['d']


def lin2(c, d, a, b):
    return psub(psmul(a, c), psmul(b, d))


def lin2p(c, d, a, b):
    return padd(psmul(a, c), psmul(b, d))


def boxN(S, sq, a, b):
    c, s = csN(sq)
    d = dd(sq)
    return [padd(pmul(d, sq['x']), lin2(c, s, a, b)),
            psub(pmul(d, psub(S, sq['x'])), lin2(c, s, a, b)),
            padd(pmul(d, sq['y']), lin2p(s, c, a, b)),
            psub(pmul(d, psub(S, sq['y'])), lin2p(s, c, a, b))]


def nrmN(c, s, k):
    return [(c, s), (psmul(F(-1), s), c), (psmul(F(-1), c), psmul(F(-1), s)), (s, psmul(F(-1), c))][k]


def sepN(qi, qj, k, a, b):
    ci, si = csN(qi)
    cj, sj = csN(qj)
    nx, ny = nrmN(ci, si, k)
    return psub(psmul(F(2), padd(pmul(nx, padd(pmul(dd(qj), psub(qj['x'], qi['x'])), lin2(cj, sj, a, b))),
                                 pmul(ny, padd(pmul(dd(qj), psub(qj['y'], qi['y'])), lin2p(sj, cj, a, b))))),
                pmul(dd(qi), dd(qj)))


HALVES = [F(1, 2), F(-1, 2)]


def lean_q(x):
    x = F(x)
    if x.denominator == 1:
        return f'({x.numerator} : ℚ)' if x.numerator < 0 else str(x.numerator)
    return f'({x.numerator}/{x.denominator} : ℚ)'


def lean_poly(p):
    return '[' + ', '.join(lean_q(x) for x in p) + ']'


def quad_closed(pS, Sa, Sb):
    """For a quadratic pS: (P, Q, D, lo, hi, expr) with the root in [Sa, Sb] equal to P + Q sqrt(D) (D squarefree),
    lo <= sqrt(D) <= hi, and expr a Lean real expression for it; mirrors ExactQuad.quadOK.  None if pS is not quadratic."""
    import math
    if len(pS) != 3:
        return None
    c0, c1, c2 = pS
    disc = c1 * c1 - 4 * c2 * c0
    assert disc > 0 and disc.denominator == 1
    disc = disc.numerator
    k, D = 1, disc
    for m in range(2, math.isqrt(disc) + 1):
        while D % (m * m) == 0:
            D //= m * m
            k *= m
    assert D > 1, 'rational root: pS is not irreducible'
    sc = 10 ** 30
    lo = F(math.isqrt(D * sc * sc), sc)
    hi = lo + F(1, sc)
    assert lo * lo <= D <= hi * hi
    P0 = -c1 / (2 * c2)
    for Q in (F(k) / (2 * c2), -F(k) / (2 * c2)):
        rlo, rhi = sorted([P0 + Q * lo, P0 + Q * hi])
        if Sa <= rhi and rlo <= Sb:
            break
    else:
        raise RuntimeError('no root P + Q sqrt(D) in [Sa, Sb]')
    P = P0
    # the mirror of quadOK
    assert c2 != 0 and c2 * (P * P + Q * Q * D) + c1 * P + c0 == 0 and Q * (2 * c2 * P + c1) == 0
    Pp = -c1 / c2 - P
    assert (Pp - Q * lo < Sa and Pp - Q * hi < Sa) or (Sb < Pp - Q * lo and Sb < Pp - Q * hi), 'other root not excluded'

    def num(x):
        return str(x.numerator) if x.denominator == 1 else f'{x.numerator} / {x.denominator}'
    a = abs(Q)
    t = f'√{D}'
    if a.numerator != 1:
        t = f'{a.numerator} * {t}'
    if a.denominator != 1:
        t = f'{t} / {a.denominator}'
    expr = (num(P) + (' + ' if Q > 0 else ' - ') + t) if P != 0 else (t if Q > 0 else f'-({t})')
    return P, Q, D, lo, hi, expr


def lean_r(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


# ------------------------------------------------------------------ the shadow checks, as in ShadowCheck.lean
def iadd(a, b): return (a[0] + b[0], a[1] + b[1])
def ineg(a): return (-a[1], -a[0])
def isub(a, b): return iadd(a, ineg(b))
def imul(a, b):
    p = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return (min(p), max(p))
def gap(a, b): return max(F(0), max(b[0] - a[1], a[0] - b[1]))
def far_ok(Ei, Ej): return 2 <= gap(Ei['x'], Ej['x']) ** 2 + gap(Ei['y'], Ej['y']) ** 2
def nrm_i(c, s, k): return [(c, s), (ineg(s), c), (ineg(c), ineg(s)), (s, ineg(c))][k]
def corner_x(E, a, b): return iadd(iadd(E['x'], imul(E['c'], (a, a))), ineg(imul(E['s'], (b, b))))
def corner_y(E, a, b): return iadd(iadd(E['y'], imul(E['s'], (a, a))), imul(E['c'], (b, b)))
def sep_ok(Ei, Ej, k):
    N = nrm_i(Ei['c'], Ei['s'], k)
    return all(F(1, 2) <= iadd(imul(N[0], isub(corner_x(Ej, a, b), Ei['x'])),
                               imul(N[1], isub(corner_y(Ej, a, b), Ei['y'])))[0] for a in HALVES for b in HALVES)
def pair_ok(Ei, Ej):
    return far_ok(Ei, Ej) or any(sep_ok(Ei, Ej, k) for k in range(4)) or any(sep_ok(Ej, Ei, k) for k in range(4))
def inbox_ok(E, Sl):
    return all(0 <= corner_x(E, a, b)[0] and corner_x(E, a, b)[1] <= Sl and
               0 <= corner_y(E, a, b)[0] and corner_y(E, a, b)[1] <= Sl for a in HALVES for b in HALVES)

ENCL_DIGITS = 20


def enclose(v, digits=ENCL_DIGITS):
    """A rational interval around the mpmath value v, on a 10^-digits grid, one grid step of slack each side."""
    import mpmath
    sc = 10 ** digits
    return (F(int(mpmath.floor(v * sc)) - 1, sc), F(int(mpmath.ceil(v * sc)) + 1, sc))


def build(path, out, mod, extra=None, split=None, cut=False, rect_h=None):
    """extra(sqs, f, S) -> (polys that must be >= 0 on the t interval, emit(ta, tb) -> Lean lines)."""
    D = json.load(gzip.open(path, 'rt') if path.endswith('.gz') else open(path))
    n = D['n']
    f = [F(x) for x in D['field']['f']]
    ta, tb = (F(x) for x in D['field']['t_interval'])
    sqs = [{'x': [F(v) for v in q['x']], 'y': [F(v) for v in q['y']], 'u': [F(v) for v in q['u']], 'm': q['m']}
           for q in D['squares']]
    for q in sqs:
        add_reduced(q, f)
    S = [F(v) for v in D['S']['in_K']]
    pS = [F(v) for v in D['S']['poly']]
    Sa, Sb = (F(x) for x in D['S']['interval'])
    fv = lambda x: qeval(f, x)
    if ta == tb:                                  # K = Q: f = T, t = 0
        assert fv(ta) == 0
    import mpmath
    mpmath.mp.dps = 60
    ctx = Ctx(f, ta, tb)
    tm = ctx.m
    tmp = mpmath.mpf(tm.numerator) / tm.denominator
    def mval(p):
        return sum(mpmath.mpf(c.numerator) / c.denominator * tmp ** e for e, c in enumerate(p))
    def numval(N):
        return float(qeval(pdivmod(N, f)[1], tm))
    # enclosures (proved once per square in the field) and S >= Sl
    encl = []
    encl_polys = []
    for q in sqs:
        d = mval(dd(q))
        E = {'x': enclose(mval(q['x'])), 'y': enclose(mval(q['y'])),
             'c': enclose(mval(csN(q)[0]) / d), 's': enclose(mval(csN(q)[1]) / d)}
        encl.append(E)
        encl_polys += [psub(q['x'], [E['x'][0]]), psub([E['x'][1]], q['x']),
                       psub(q['y'], [E['y'][0]]), psub([E['y'][1]], q['y']),
                       psub(csN(q)[0], psmul(E['c'][0], dd(q))), psub(psmul(E['c'][1], dd(q)), csN(q)[0]),
                       psub(csN(q)[1], psmul(E['s'][0], dd(q))), psub(psmul(E['s'][1], dd(q)), csN(q)[1])]
    Sl = enclose(mval(S))[0]
    # sweep-line pruning (lean/Sqpack/ExactCheckCut.lean): squares sorted by the x lower bound of their enclosure;
    # row i only visits j < cut[i], the first j > i with x_lo(j) >= x_hi(i) + 3/2 (every later j is far: farOK)
    cutv = None
    if cut:
        order = sorted(range(n), key=lambda i: encl[i]['x'][0])
        sqs = [sqs[i] for i in order]
        encl = [encl[i] for i in order]
        cutv = []
        for i in range(n):
            j = i + 1
            while j < n and encl[j]['x'][0] < encl[i]['x'][1] + F(3, 2):
                j += 1
            cutv.append(j)
    # exact conditions only where the shadow tests fail
    box_exact = [i for i in range(n) if not inbox_ok(encl[i], Sl)]
    if rect_h is not None:          # rectangle W x H (lean/Sqpack/ExactRect.lean): top wall on the shadows only
        bad = [i for i in range(n) if any(corner_y(encl[i], a, b)[1] > rect_h for a in HALVES for b in HALVES)]
        if bad:
            raise RuntimeError(f'top wall y <= {rect_h} fails on the enclosures of squares {bad[:10]}')
    choice = {}
    for i in range(n):
        for j in range(i + 1, cutv[i] if cutv else n):
            if pair_ok(encl[i], encl[j]):
                continue
            best = None
            for own in (True, False):
                for k in range(4):
                    qi, qj = (sqs[i], sqs[j]) if own else (sqs[j], sqs[i])
                    worst = min(numval(sepN(qi, qj, k, a, b)) for a in HALVES for b in HALVES)
                    if best is None or worst > best[0]:
                        best = (worst, own, k)
            choice[(i, j)] = (best[1], best[2])
    Ns = []
    for i in box_exact:
        for a in HALVES:
            for b in HALVES:
                Ns += boxN(S, sqs[i], a, b)
    for (i, j), (own, k) in choice.items():
        qi, qj = (sqs[i], sqs[j]) if own else (sqs[j], sqs[i])
        Ns += [sepN(qi, qj, k, a, b) for a in HALVES for b in HALVES]
    n_exact = len(Ns)
    Ns = Ns + encl_polys + [psub(S, [Sl]), psub(S, [Sa]), psub([Sb], S)]
    if extra:
        ex_polys, ex_emit = extra(sqs, f, S)
        Ns = Ns + ex_polys
    for it in range(400):
        ctx = Ctx(f, ta, tb)
        bad = 0
        for N in Ns:
            r, _ = ctx.nonneg(N)
            if r is None:
                bad += 1
        if not bad:
            break
        if ta == tb:
            raise RuntimeError(f'{bad} conditions fail at the exact rational point')
        # halve the interval (exact bisection keeps a root), round outward to dyadics
        for _ in range(8):
            mid = (ta + tb) / 2
            if fv(mid) == 0:
                ta = tb = mid
                break
            if fv(ta) * fv(mid) < 0:
                tb = mid
            else:
                ta = mid
    else:
        raise RuntimeError('could not narrow the t interval enough')
    assert ta == tb or fv(ta) * fv(tb) < 0
    # p_S(S(t)) = 0 mod f
    comp = []
    for c in reversed(pS):
        comp = padd([c], pmul(S, comp))
    qq, rr = pdivmod(comp, f)
    assert all_zero(psub(comp, padd(pmul(qq, f), rr))) and all_zero(rr), 'pS(S) != 0 mod f'
    eqs = sum(1 for N in Ns if ctx.nonneg(N)[0] == 'eq')
    # Lean file
    L = []
    L.append('import Sqpack.ExactQuad\n' + ('import Sqpack.ExactCheckCut\n' if cut else '') +
             ('import Sqpack.ExactRect\n' if rect_h is not None else ''))
    L.append(f'/-! Generated by `search/exact/lean_cert.py` from `{path.split("/")[-1]}`: register record n = {n}, '
             f'field degree {len(f) - 1}, `S` of degree {len(pS) - 1}.\n'
             f'{eqs} touching conditions are identities mod `f`, {len(Ns) - eqs} are strict; walls and pairs: '
             f'{n - len(box_exact)}/{n} squares and {n * (n - 1) // 2 - len(choice)}/{n * (n - 1) // 2} pairs by '
             f'rational shadows. -/\n')
    L.append(f'namespace UnitSquarePacking.EC.{mod}\n')
    L.append('set_option maxHeartbeats 0\nset_option maxRecDepth 100000\n')
    L.append(f'noncomputable def cert : Cert {n} where')
    L.append(f'  f := {lean_poly(f)}')
    L.append(f'  a := {lean_q(ta)}')
    L.append(f'  b := {lean_q(tb)}')
    L.append(f'  S := {lean_poly(S)}')
    L.append('  sq := ![' + ',\n    '.join(f'⟨{lean_poly(q["x"])}, {lean_poly(q["y"])}, {lean_poly(q["u"])}, {q["m"]}, '
                                          f'{lean_poly(q["c"])}, {lean_poly(q["s"])}, {lean_poly(q["d"])}⟩'
                                          for q in sqs) + ']')
    sepR = []
    for i in range(n):
        ent = [f'({j}, {"true" if own else "false"}, {k})' for (ii, j), (own, k) in sorted(choice.items()) if ii == i]
        sepR.append('[' + ', '.join(ent) + ']')
    # sparse: only the pairs that need the exact test; the default is never used (shadow tests pass there)
    L.append('  sep := fun i j => (((![' + ',\n    '.join(sepR) + '] : Fin ' + str(n) +
             ' → List (ℕ × Bool × Fin 4)) i).find? (·.1 == j.val)).elim (true, 0) (·.2)')
    L.append('  encl := ![' + ',\n    '.join('⟨' + ', '.join(f'({lean_q(E[v][0])}, {lean_q(E[v][1])})' for v in 'xycs') + '⟩'
                                             for E in encl) + ']')
    L.append(f'  Sl := {lean_q(Sl)}\n')
    if cut:
        L.append(f'/-- Sweep-line cuts (`ExactCheckCut`). -/\ndef cut : Fin {n} → ℕ := fun i => (![' +
                 ', '.join(map(str, cutv)) + f'] : Fin {n} → ℕ) i\n')
    L.append(f'/-- The polynomial of `S` (ascending coefficients). -/\ndef pS : Poly := {lean_poly(pS)}\n')
    if rect_h is not None:
        L.append(f'/-- The rectangle height. -/\ndef H : ℚ := {lean_q(rect_h)}\n')
    packs_thm = [f'/-- `s({n}) ≤ S*`, `S*` the root of `pS` in `[{float(Sa):.12g}, {float(Sb):.12g}]`. -/',
                 f'theorem packs : ∃ s : ℝ, peval pS s = 0 ∧ (({lean_q(Sa)} : ℚ) : ℝ) ≤ s ∧ s ≤ (({lean_q(Sb)} : ℚ) : ℝ) ∧ '
                 f'Packs {n} s :=',
                 (f'  packs_exact_cut cert pS _ _ cut (by decide +kernel) (by decide +kernel) (by decide +kernel) boxes\n'
                  f'    sorted cuts rows\n' if cut else
                  f'  packs_exact cert pS _ _ (by decide +kernel) (by decide +kernel) (by decide +kernel) boxes rows\n') +
                 f'    (by decide +kernel)\n'
                 f'    (by decide +kernel) (by decide +kernel)\n']
    if rect_h is not None:
        packs_thm = [f'/-- {n} unit squares in `[0, W] × [0, H]`, `W` the root of `pS` in `[{float(Sa):.12g}, {float(Sb):.12g}]`. -/',
                     f'theorem packs : ∃ s : ℝ, peval pS s = 0 ∧ (({lean_q(Sa)} : ℚ) : ℝ) ≤ s ∧ s ≤ (({lean_q(Sb)} : ℚ) : ℝ) ∧ '
                     f'UnitSquarePacking.Conjectures.PacksIn {n} (UnitSquarePacking.Conjectures.rect s (H : ℝ)) :=',
                     f'  packsIn_rect_cut cert pS _ _ H cut (by decide +kernel) (by decide +kernel) (by decide +kernel) boxes\n'
                     f'    tops sorted cuts rows (by decide +kernel) (by decide +kernel) (by decide +kernel)\n']
    qc = quad_closed(pS, Sa, Sb) if rect_h is None else None
    if qc is not None:
        P, Q, Dq, lo, hi, expr = qc
        packs_thm += [f'/-- `s({n}) ≤ {expr}`: the side in closed form (`ExactQuad.packs_quad`). -/',
                      f'theorem packs_closed : Packs {n} ({expr}) := by',
                      f'  have h := packs_quad (P := {lean_q(P)}) (Q := {lean_q(Q)}) (D := {Dq}) (lo := {lean_q(lo)})'
                      f' (hi := {lean_q(hi)}) packs (by decide +kernel)',
                      '  convert h using 1; push_cast; ring\n',
                      f'theorem minSide_le_closed : minSide {n} ≤ {expr} :=',
                      '  csInf_le ⟨0, fun _ hs => nonneg_of_packs_q (by norm_num) hs⟩ packs_closed\n']
    if split:
        # modules: <out>/Data.lean (the certificate), <out>/C<k>.lean (chunks of squares, checked in parallel by lake),
        # <out>.lean (glue: no fin_cases, ranges by omega)
        import os
        base = out[:-len('.lean')]
        modname = base.split('lean/')[-1].replace('/', '.')
        os.makedirs(base, exist_ok=True)
        L.append(f'end UnitSquarePacking.EC.{mod}\n')
        open(f'{base}/Data.lean', 'w').write('\n'.join(L))
        cuts = list(range(0, n, split)) + [n]
        ROW = ('boxOK cert i = true ∧ cutOK cert cut i = true ∧ rowOKc cert cut i = true' if cut else
               'boxOK cert i = true ∧ rowOK cert i = true')
        if rect_h is not None:
            ROW = 'topOK cert H i = true ∧ ' + ROW
        if cut:
            open(f'{base}/Sorted.lean', 'w').write('\n'.join([
                f'import {modname}.Data\n', f'namespace UnitSquarePacking.EC.{mod}\n', 'set_option maxHeartbeats 0\n',
                'theorem sorted : sortedOK cert = true := by decide +kernel\n', f'end UnitSquarePacking.EC.{mod}\n']))
        for c in range(len(cuts) - 1):
            lo, hi = cuts[c], cuts[c + 1]
            open(f'{base}/C{c}.lean', 'w').write('\n'.join([
                f'import {modname}.Data\n',
                f'namespace UnitSquarePacking.EC.{mod}\n',
                'set_option maxHeartbeats 0\n',
                f'theorem chunk_{c} : ∀ i : Fin {n}, {lo} ≤ i.val → i.val < {hi} → {ROW} := by',
                '  decide +kernel\n',
                f'end UnitSquarePacking.EC.{mod}\n']))
        M = [''.join(f'import {modname}.C{c}\n' for c in range(len(cuts) - 1)) + (f'import {modname}.Sorted\n' if cut else ''),
             f'/-! Generated by `search/exact/lean_cert.py --split {split}`: n = {n}, the certificate in `Data`, '
             f'squares checked in {len(cuts) - 1} chunks. -/\n',
             f'namespace UnitSquarePacking.EC.{mod}\n',
             'set_option maxHeartbeats 0\n',
             f'theorem ok (i : Fin {n}) : {ROW} := by']
        for c in range(len(cuts) - 2):
            M.append(f'  by_cases h{c} : i.val < {cuts[c + 1]}\n  · exact chunk_{c} i (by omega) h{c}')
        M.append(f'  exact chunk_{len(cuts) - 2} i (by omega) i.isLt\n')
        if rect_h is None:
            M.append('theorem boxes : ∀ i, boxOK cert i = true := fun i => (ok i).1\n')
        if rect_h is not None:
            M.append('theorem tops : ∀ i, topOK cert H i = true := fun i => (ok i).1\n')
            M.append('theorem boxes : ∀ i, boxOK cert i = true := fun i => (ok i).2.1\n')
            M.append('theorem cuts : ∀ i, cutOK cert cut i = true := fun i => (ok i).2.2.1\n')
            M.append('theorem rows : ∀ i, rowOKc cert cut i = true := fun i => (ok i).2.2.2\n')
        elif cut:
            M.append('theorem cuts : ∀ i, cutOK cert cut i = true := fun i => (ok i).2.1\n')
            M.append('theorem rows : ∀ i, rowOKc cert cut i = true := fun i => (ok i).2.2\n')
        else:
            M.append('theorem rows : ∀ i, rowOK cert i = true := fun i => (ok i).2\n')
        M += packs_thm
        M.append(f'end UnitSquarePacking.EC.{mod}\n')
        open(out, 'w').write('\n'.join(M))
        print(f'{out}: split into Data + {len(cuts) - 1} chunks; n = {n}, {len(Ns)} field conditions ({eqs} identities; '
              f'{n_exact} for walls/pairs, {len(choice)} exact pairs, {len(box_exact)} exact boxes)')
        return
    for i in range(n):
        L.append(f'theorem box_{i} : boxOK cert {i} = true := by decide +kernel')
    L.append('')
    for i in range(n):
        L.append(f'theorem row_{i} : rowOK cert {i} = true := by decide +kernel')
    L.append('')
    L.append('theorem boxes : ∀ i, boxOK cert i = true := by\n  intro i; fin_cases i\n  exacts [' +
             ', '.join(f'box_{i}' for i in range(n)) + ']\n')
    L.append('theorem rows : ∀ i, rowOK cert i = true := by\n  intro i; fin_cases i\n  exacts [' +
             ', '.join(f'row_{i}' for i in range(n)) + ']\n')
    L += packs_thm
    if extra:
        L += ex_emit(ta, tb, Sa, Sb)
    L.append(f'end UnitSquarePacking.EC.{mod}\n')
    open(out, 'w').write('\n'.join(L))
    print(f'{out}: n = {n}, {len(Ns)} field conditions ({eqs} identities; {n_exact} for walls/pairs, '
          f'{len(choice)} exact pairs, {len(box_exact)} exact boxes), t interval width {float(tb - ta):.3g}')


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('out')
    ap.add_argument('--split', type=int, default=None, help='squares per chunk module (large n)')
    ap.add_argument('--cut', action='store_true', help='sweep-line pair pruning (ExactCheckCut); needs --split')
    ap.add_argument('--rect-h', default=None, help='rectangle W x H certificate (ExactRect): the height H, a rational; '
                    'the JSON side S is W; needs --cut')
    A = ap.parse_args()
    mod = A.out.split('/')[-1].replace('.lean', '')
    if A.cut and not A.split:
        ap.error('--cut needs --split')
    if A.rect_h is not None and not A.cut:
        ap.error('--rect-h needs --cut')
    build(A.path, A.out, mod, split=A.split, cut=A.cut, rect_h=F(A.rect_h) if A.rect_h is not None else None)
