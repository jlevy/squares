"""Lean local-minimum certificate (lean/Sqpack/LocalMinCheck.lean) for a grade-A record:
  ∃ s, pS(s) = 0 ∧ Sa ≤ s ≤ Sb ∧ ∃ c θ, IsLocalMinPacking n s c θ
from minpoly.py's exact configuration and localmin.py's rows, exact multipliers and rational left inverse
(G as lists; the linear parts as sparse rational midpoints with one radius eps).
The exact-packing certificate is lean_cert.py's; the local-minimum checks are replayed here with the Lean checker's
arithmetic, and they take part in narrowing the t interval.

  python3 localmin_lean.py minpoly/solve/n-11 ../../lean/Sqpack/Exact/N11L.lean
"""
import sys
from fractions import Fraction as F
import mpmath
import localmin
import lean_cert as LC
from lean_cert import padd, psub, pmul, psmul, lean_q, lean_poly, pdivmod, qeval


def fr(p):
    """flint fmpq_poly -> list of Fractions."""
    return [F(int(c.p), int(c.q)) for c in p.coeffs()] if not p.is_zero() else []


def nrmN(c, s, k):
    m1 = lambda p: psmul(F(-1), p)
    return [(c, s), (m1(s), c), (m1(c), m1(s)), (s, m1(c))][k]


def main(base, out):
    lm = localmin.build(base, quiet=True)['_internal']
    rows, lam, G, Ls, n3, m = lm['rows'], lm['lam'], lm['G'], lm['Ls'], lm['N'], lm['m']
    C = [fr(p) for p in lm['C']]
    S_ = [fr(p) for p in lm['S']]
    n = (n3 - 1) // 3
    lamP = [fr(lam[r]) for r in range(m)]
    # rational parameters (with slack)
    lmin = F(int(float(lm['lam_min']) * 0.99 * 10 ** 8), 10 ** 8)
    Lam = F(int(float(lm['Lam']) * 1.01 * 10 ** 6) + 1, 10 ** 6)
    mu = F(int(float(lm['mu']) * 0.99 * 10 ** 8), 10 ** 8)
    Gn = F(int(float(lm['Gnorm']) * 1.0001 * 10 ** 6) + 1, 10 ** 6)
    GL = [[G[v][r] for r in range(m)] for v in range(n3)]                # v: 3i + c, S = 3n

    def extra(sqs, f, S):
        X = [q['x'] for q in sqs]
        Y = [q['y'] for q in sqs]
        qx = lambda j, a, b: psub(psmul(a, C[j]), psmul(b, S_[j]))
        qy = lambda j, a, b: padd(psmul(a, S_[j]), psmul(b, C[j]))

        def sv(j, a, b, i, k):
            nx, ny = nrmN(C[i], S_[i], k)
            return padd(pmul(nx, psub(padd(X[j], qx(j, a, b)), X[i])), pmul(ny, psub(padd(Y[j], qy(j, a, b)), Y[i])))
        polys = []
        for r in rows:
            if r[0] == 'P':
                _, j, (a, b), i, k = r
                Ax = psub(padd(X[j], qx(j, a, b)), X[i])
                Ay = psub(padd(Y[j], qy(j, a, b)), Y[i])
                polys += [psub([F(2)], Ax), padd([F(2)], Ax), psub([F(2)], Ay), padd([F(2)], Ay)]
                polys += [psub([F(1, 2) - mu], sv(j, a, b, i, kk)) for kk in range(4) if kk != k]
        polys += [psub(lamP[r], [lmin]) for r in range(m)]
        tot = []
        for r in range(m):
            tot = padd(tot, lamP[r])
        polys.append(psub([Lam], tot))
        # bounds lo <= L_rv <= hi: exact constants where L is constant, else a slightly widened numerical interval
        mpmath.mp.dps = 80
        lo, hi = {}, {}
        tm = None
        for r in range(m):
            for v, c in Ls[r].items():
                cp = fr(c)
                rem = pdivmod(cp, f)[1]
                while rem and rem[-1] == 0:
                    rem.pop()
                if len(rem) <= 1:
                    val = rem[0] if rem else F(0)
                    lo[(r, v)] = hi[(r, v)] = val
                else:
                    lo[(r, v)] = rem                                   # filled in emit once t is known
        return polys, lambda ta, tb, Sa, Sb: emit(ta, tb, f, lo, hi, Sa, Sb)

    def emit(ta, tb, f, lo, hi, Sa, Sb):
        # sparse midpoints of the linear parts: exact where constant, else rounded at 1e-15 (radius eps covers both)
        mpmath.mp.dps = 80
        tm = mpmath.mpf(ta.numerator) / ta.denominator
        eps = F(2, 10 ** 15)
        mid = {}
        for key, val in lo.items():
            if isinstance(val, list):
                x = sum(mpmath.mpf(c.numerator) / c.denominator * tm ** e for e, c in enumerate(val))
                mid[key] = F(int(mpmath.nint(x * 10 ** 15)), 10 ** 15)
            else:
                mid[key] = val
        cols = {w: sorted((r, d) for (r, v), d in mid.items() if v == w and d != 0) for w in range(n3)}
        # the G condition as the Lean checker computes it
        worst = F(0)
        for v in range(n3):
            tot = F(0)
            for w in range(n3):
                d = F(1) if v == w else F(0)
                tot += abs(sum(GL[v][r] * x for r, x in cols[w]) - d)
            worst = max(worst, tot + n3 * Gn * eps)
            assert sum(abs(x) for x in GL[v]) <= Gn
        assert worst <= F(1, 2), f'G check fails: {float(worst)}'

        def row_lean(r):
            if r[0] == 'P':
                _, j, (a, b), i, k = r
                return f'LM.Row.pt {j} {lean_q(a)} {lean_q(b)} {i} {k}'
            _, j, (a, b), w = r
            return f'LM.Row.wall {j} {lean_q(a)} {lean_q(b)} {"LRBT".index(w)}'

        def qlist(xs):
            return '[' + ', '.join(lean_q(x) for x in xs) + ']'

        def clist(w):
            return '[' + ', '.join(f'(({r} : Fin {m}), {lean_q(x)})' for r, x in cols[w]) + ']'
        Lt = []
        Lt.append('\n/-! ## The local-minimum certificate -/\n')
        Lt.append(f'noncomputable def GS : List ℚ := {qlist(GL[3 * n])}')
        Lt.append(f'noncomputable def GT : Fin {n} → Fin 3 → List ℚ := ![' + ',\n  '.join(
            '![' + ', '.join(qlist(GL[3 * i + c]) for c in range(3)) + ']' for i in range(n)) + ']')
        Lt.append(f'noncomputable def LcS : List (Fin {m} × ℚ) := {clist(3 * n)}')
        Lt.append(f'noncomputable def LcT : Fin {n} → Fin 3 → List (Fin {m} × ℚ) := ![' + ',\n  '.join(
            '![' + ', '.join(clist(3 * i + c) for c in range(3)) + ']' for i in range(n)) + ']')
        Lt.append(f'''
noncomputable def lcert : UnitSquarePacking.LMC.LCert {n} {m} where
  P := cert
  C := ![{', '.join(lean_poly(c) for c in C)}]
  S := ![{', '.join(lean_poly(c) for c in S_)}]
  rows := ![{', '.join(row_lean(r) for r in rows)}]
  mu := {lean_q(mu)}
  lam := ![{', '.join(lean_poly(p) for p in lamP)}]
  lmin := {lean_q(lmin)}
  Lam := {lean_q(Lam)}
  Gr := fun v => match v with | none => GS | some (i, c) => GT i c
  Gn := {lean_q(Gn)}
  Lc := fun w => match w with | none => LcS | some (i, c) => LcT i c
  eps := {lean_q(eps)}

open UnitSquarePacking.LMC in
theorem unit_ok : ∀ i, unitOK lcert i = true := by decide +kernel
open UnitSquarePacking.LMC in
theorem rowsL_ok : ∀ r, rowOKb lcert (lcert.rows r) = true := by decide +kernel
open UnitSquarePacking.LMC in
theorem lam_ok : ∀ r, lamOK lcert r = true := by decide +kernel
open UnitSquarePacking.LMC in
theorem lamS_ok : lamSumOK lcert = true := by decide +kernel
open UnitSquarePacking.LMC in
theorem kkt_ok : ∀ v, kktOK lcert v = true := by decide +kernel
open UnitSquarePacking.LMC in
theorem bnd_ok : ∀ r v, boundOK lcert r v = true := by decide +kernel
open UnitSquarePacking.LMC in
theorem col_ok : ∀ w, colOK lcert w = true := by decide +kernel
open UnitSquarePacking.LMC in
theorem Gn_ok : ∀ v, GnOK lcert v = true := by decide +kernel
open UnitSquarePacking.LMC in
theorem G_ok : ∀ v, GOK lcert v = true := by decide +kernel

/-- **The record is a local minimum** (first-order rigid, all contact forces positive): there is a pose-space ball
around it containing no packing of {n} unit squares in a smaller square. -/
theorem localmin : ∃ s : ℝ, peval pS s = 0 ∧ (({lean_q(Sa)} : ℚ) : ℝ) ≤ s ∧ s ≤ (({lean_q(Sb)} : ℚ) : ℝ) ∧
    ∃ c θ, IsLocalMinPacking {n} s c θ := by
  obtain ⟨t, ha, hb, hf⟩ := exists_root (f := cert.f) (a := cert.a) (b := cert.b) (by decide +kernel)
    (by decide +kernel)
  obtain ⟨θ, hθ⟩ := UnitSquarePacking.LMC.isLocalMin_of_lcert (L := lcert) (by decide +kernel) boxes rows unit_ok rowsL_ok lam_ok
    lamS_ok kkt_ok bnd_ok col_ok Gn_ok G_ok hf ha hb
  refine ⟨peval cert.S t, ?_, ?_, ?_, _, θ, hθ⟩
  · have := zero_of_zeroOK (f := cert.f) (N := pcomp pS cert.S) (by decide +kernel) hf
    rwa [peval_pcomp] at this
  · have := nonneg_of_nonnegOK (f := cert.f) (a := cert.a) (b := cert.b) (N := psub cert.S [{lean_q(Sa)}])
      (by decide +kernel) hf ha hb
    simp at this; linarith
  · have := nonneg_of_nonnegOK (f := cert.f) (a := cert.a) (b := cert.b) (N := psub [{lean_q(Sb)}] cert.S)
      (by decide +kernel) hf ha hb
    simp at this; linarith
''')
        return Lt

    LC.build(base + '.minpoly.json', out, out.split('/')[-1].replace('.lean', ''), extra=extra)
    # import the local-minimum checker too
    txt = open(out).read().replace('import Sqpack.ExactCheck\n', 'import Sqpack.ExactCheck\nimport Sqpack.LocalMinCheck\n', 1)
    # the G and column tables are large literals (noncomputable: only the kernel evaluates them)
    # (maxRecDepth for the large literals is in lean_cert.py's header)
    open(out, 'w').write(txt)
    print(f'{out}: local-minimum certificate, {m} rows, lmin {float(lmin):.4g}, mu {float(mu):.4g}, Gn {float(Gn):.4g}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
