"""Checks for Lemma 4.9 (K_w <= 13), part (c), and for the constants of the variant of the proof that uses Lemma 4.9 in place
of the computer-assisted Lemma 4.10 (version 1.2 of the paper: Remark 7.5 and the remark after Corollary 1.3); mpmath, 50 digits.
Version 1.2: the second half now checks the constants of version 1.2 (version 1.1 checked those of an earlier draft).
Refinement (part (c) of lem:Kw): if two inner centres c1, c3 both have class 5 (radius <= R5), then the number of relevant
edges is at most sum_i m_i - 1.  Proof ingredients checked here:
 (i)   |c1 - c3| in [1, 2 R5];
 (ii)  the angle at c1 between p - c1 and c3 - c1 is at most psi_max = arcsin(R5 sin(pi - gamma(5,5)))  (law of sines);
 (iii) a neighbour centre c' of c1 (|c' - c1| in [1, Lambda), |c' - c3| >= 1) is seen from c1 at angle >= sep3 from c3, where
       cos(sep3) = max of f over [1, 2R5] x [1, Lambda] (convex in each variable -> corners);
       a side foot is >= arccos(c0) > sep3 from c3;
 (iv)  if c3 is not an other end of a relevant edge at c1, the other ends lie in [-beta, beta] minus (psi - sep3, psi + sep3),
       beta < 90 deg, so in two arcs of length < 90 + psi_max - sep3 < 2 gamma0  ->  at most 2 + 2 = 4 of them: deg(c1) <= 4;
 (v)   if c3 is such an other end, the edge {c1, c3} is counted in deg(c1) and in deg(c3).
Either way the count is <= sum m_i - 1, and (5,2,5,2) is the only class sequence with sum 14, so K_w <= 13.
Usage: python kw13_check.py"""
from mpmath import mp, mpf, sqrt, acos, asin, sin, pi, log, findroot
mp.dps = 50
ok = True


def check(name, cond, val=None):
    global ok
    print(f"{'OK ' if cond else 'FAIL'} {name}" + (f"   [{mp.nstr(val, 12)}]" if val is not None else ""))
    ok = ok and bool(cond)


SQ2 = sqrt(2); deg = 180/pi
f = lambda r1, r2: (r1**2 + r2**2 - 1)/(2*r1*r2)
for d in [mpf('1e-4'), mpf('1e-5')]:
    Lam = SQ2 + d; g0 = acos(1 - 1/(2*Lam**2))
    rho1 = sqrt((d + SQ2/2)**2 + mpf(1)/4)
    R5 = min(rho1, 1/(2*sin(2*g0)))
    g55 = acos(f(R5, R5))
    psi = asin(R5*sin(pi - g55))
    cand = [f(mpf(1), mpf(1)), f(mpf(1), Lam), f(2*R5, mpf(1)), f(2*R5, Lam)]
    sep3 = acos(max(cand))
    c0 = d + SQ2/2 - mpf(1)/2
    tag = f"[d={mp.nstr(d,2)}]"
    check(f"{tag} 2 R5 < 1.008 (|c1-c3| in [1, 2R5])", 2*R5 < mpf('1.008'), 2*R5)
    check(f"{tag} psi_max = arcsin(R5 sin(pi - gamma(5,5))) < 7.19 deg (the value used in the text)", psi*deg < mpf('7.19'), psi*deg)
    check(f"{tag} f convex in r1 for r2 >= 1 (coefficient (r2^2-1)/(2 r2) >= 0) -> corners; sep3 > 44.99 deg", sep3*deg > mpf('44.99'), sep3*deg)
    check(f"{tag} side-foot separation arccos(c0) > sep3", acos(c0) > sep3)
    # two remaining arcs, each of length < 90 + psi_max - sep3, must each hold < 3 points (needs < 2 gamma0)
    Lmax = pi/2 + psi - sep3
    check(f"{tag} each remaining arc has length < 90 + psi - sep3 < 2 gamma0 (so <= 2 points per arc)", Lmax < 2*g0, Lmax*deg)
    # the inner centres c1, c3 subtend at p an angle >= gamma(5,5) > 165 deg
    check(f"{tag} gamma(5,5) > 165 deg", g55*deg > 165, g55*deg)
print("ALL OK (lem:Kw refinement)" if ok else "SOME CHECK FAILED")

# ---------------- constants of version 1.2 with K_w = 13 in place of K_w^* = 9 (Remark 7.5) ----------------
# Parameters of Section 6: C = 2, C' = 2 sqrt2, delta = 1e-5, eps = 2e-3, omega0 = 2e-4, y_min = 236000, w0 = 1.265e-5,
# g0 = 0.49997, Q* = 0.32; the bracket is evaluated with the rounded values stated in Section 6.
Kw = 13; Qs = mpf('0.32'); C = 2; Cp = 2*SQ2; delta = mpf('1e-5'); eps = mpf('2e-3'); om0 = mpf('2e-4'); YMIN = mpf(236000)
W0 = mpf('1.265e-5'); G0 = mpf('0.49997')
A = 4*sqrt(Kw/Qs)/(2 - mpf('3e-6'))
Ab = mpf('12.7476')
check("K_w = 13: A = 4 sqrt(13/0.32)/(2 - 3e-6) < 12.7476", A < Ab, A)
al = 1/(C*YMIN)
check("1/(omega0 y_min) < 0.021187, 2.01/(eps y_min) < 4.2585e-3, alpha(y_min)/delta < 0.21187",
      1/(om0*YMIN) < mpf('0.021187') and mpf('2.01')/(eps*YMIN) < mpf('4.2585e-3') and al/delta < mpf('0.21187'))
G13 = 2*mpf('0.50001')*(Ab/(Cp*YMIN) + 1/(2*Cp**2*delta*YMIN**2))
check("K_w = 13: Gamma = 1.00002 (A/(C' y_min) + 1/(2 C'^2 delta y_min^2)) < 1.93e-5 (with A < 12.7476)", G13 < mpf('1.93e-5'), G13)
br = mpf('0.021187') + SQ2*Ab + (1 + mpf('4.2585e-3'))/(SQ2*G0*(1 - eps))*(Ab + mpf('0.21187')) + G13
print("bracket (K_w = 13) =", mp.nstr(br, 12))
check("K_w = 13: bracket < 36.493", br < mpf('36.493'), br)
SL = mpf('1.99954'); Bb = mpf('36.493')
check("2 (1 - omega0)(1 - 2 w0) >= 1.99954 (the numerator of the slope)", 2*(1 - om0)*(1 - 2*W0) >= SL, 2*(1 - om0)*(1 - 2*W0))
check("K_w = 13: slope 1.99954/36.493 > 0.0547", SL/Bb > mpf('0.0547'), SL/Bb)
F13 = lambda L: SL*(L - mpf('13.06675'))/Bb
L13 = findroot(lambda L: F13(L) - 1, 31)
check("K_w = 13: F13(k) = 1.99954 (log k - 13.06675)/36.493 exceeds 1 for log k > log k*, and 1/log k* lies in [0.0319, 0.0320)",
      mpf('0.0319') <= 1/L13 < mpf('0.0320'), 1/L13)
check("K_w = 13: kappa = 0.0319 for every k >= 2 (W >= 1 if 0.0319 log k <= 1; otherwise F13 - 0.0319 log k is increasing and positive at log k = 1/0.0319)",
      SL/Bb > mpf('0.0319') and F13(1/mpf('0.0319')) > 1, F13(1/mpf('0.0319')))
L4h = mpf('13.06675') + 4*Bb/SL
check("remark after Corollary 1.3: with K_w = 13, 4/(13.06675 + 4*36.493/1.99954) = 4/86.0695... > 0.0464",
      mpf('86.0695') < L4h < mpf('86.0696') and 4/L4h > mpf('0.0464'), 4/L4h)
print("s(k^2-c) = k with K_w = 13 for log k > 13.06675 + 36.493 c/1.99954; c = 4:", mp.nstr(mpf('13.06675') + 4*Bb/SL, 10))
print("ALL OK" if ok else "SOME CHECK FAILED")
