"""v11 constants (mpmath, 50 digits) for edition 11 (version 1.2) of the paper: improvement (d2), "use the lines near the walls".

Parameters: C = 2, C' = 2 sqrt2, delta = 1e-5, eps = 2e-3, omega0 = 2e-4, Q* = 0.32, K_w^* = 9 (13 for the hand-proof variant),
and the new constant smallest scale y_min = 236000 (replacing y0 = sqrt(k)/4 of v1.1).
Prints every number quoted in the edited text of Sections 5-6, the theorem and the remarks, checks each quoted rounding in the
safe direction, and reproduces the values of the two reviews R1/R2 (research/R1/consts_R1_out.txt, research/R2/d2_constants_output.txt).
Usage: python consts_v11.py            (K_w^* = 9)
"""
from mpmath import mp, mpf, sqrt, cos, sin, tan, sec, log, exp, findroot, floor, ceil, quad, inf
mp.dps = 50
ok = True


def check(name, cond, val=None):
    global ok
    print(f"{'OK ' if cond else 'FAIL'} {name}" + (f"   [{mp.nstr(val, 12)}]" if val is not None else ""))
    ok = ok and bool(cond)


SQ2 = sqrt(2); C = mpf(2); Cp = 2*SQ2; delta = mpf('1e-5'); Qs = mpf('0.32'); TH1 = mpf('1e-5')
eps = mpf('2e-3'); om0 = mpf('2e-4')
YMIN = mpf(236000)
K3 = mpf(10)**12            # below K3 the bound F(k) is < 1, so the theorem is Corollary cor:W1 there


def A_of(KW, Q=Qs):
    return 4*sqrt(mpf(KW)/Q)/(2 - mpf('3e-6'))


def quant(s):
    """Lemma lem:Q and lem:GZ quantities at scale s (alpha = alpha(s) = 1/(Cs))."""
    al = 1/(C*s)
    nq = mpf('0.50001')*(1 + al/s)/(C**2*s)                      # n (sec alpha - 1) bound
    w0_exact = max(delta + nq + al, al + al**2)                  # lower/upper ramp distance to an integer
    rho = cos(al) + sin(al)
    BZ = mpf('2.01')*al + (1 + (al + rho)/s)*(1 + mpf('3.04e-5'))/(C*(cos(al) - sin(al)))
    g0_exact = (cos(al) - sin(al)) - BZ
    return al, nq, w0_exact, BZ, g0_exact


def Gamma_of(A, ymin):
    """Gamma = int_H gamma(y) dy/d(y) <= 2 int_{ymin}^inf 0.50001 a'(y)(A + a'(y)/delta) dy/y, a'(y) = 1/(C'y)."""
    closed = 2*mpf('0.50001')*(A/(Cp*ymin) + 1/(2*Cp**2*delta*ymin**2))
    numer = 2*quad(lambda y: mpf('0.50001')/(Cp*y)*(A + 1/(Cp*y*delta))/y, [ymin, inf])
    return closed, numer


def exact_bracket(KW, ymin, Q=Qs, g0=None):
    """Bracket with exact (unrounded) constants; g0 exact unless given."""
    A = A_of(KW, Q)
    al, nq, w0e, BZ, g0e = quant(ymin)
    g = g0e if g0 is None else g0
    G, _ = Gamma_of(A, ymin)
    B = 1/(om0*ymin) + Cp/2*A + C*(1 + mpf('2.01')/(eps*ymin))/(Cp*g*(1 - eps))*(A + al/delta) + G
    return B, w0e


def report_exact(ymin, label, w0=None):
    """Reproduction of R1/R2: exact bracket, slope 2(1-om0)h0/B and the all-k constant 1/L*,
    with L0 = log(ceil(ymin)+1) - log((1-eps)/2) and log(1-6/k) included in the root."""
    B, w0e = exact_bracket(9, ymin)
    ww = w0e if w0 is None else w0
    h0 = 1 - 2*ww
    slope = 2*(1 - om0)*h0
    L0 = log(ceil(ymin) + 1) - log((1 - eps)/2)
    Ls = findroot(lambda L: slope*(L - L0 + log(1 - 6*exp(-L)))/B - 1, 28)
    print(f"  [{label}] y_min={mp.nstr(ymin, 12)}: exact bracket={mp.nstr(B, 10)}, w0_exact={mp.nstr(w0e, 10)}, "
          f"L0={mp.nstr(L0, 10)}, kappa_inf={mp.nstr(slope/B, 10)}, log k*={mp.nstr(Ls, 10)}, kappa_all={mp.nstr(1/Ls, 10)}")
    return B, slope/B, 1/Ls


print("=================== reproduction of the reviews (exact constants) ===================")
B1, ki1, ka1 = report_exact(1/(Cp*mpf('1.5e-6')), "R2 minimal y_min = 235702.26 (w0 exact)")
B2, ki2, ka2 = report_exact(mpf(235703), "R1 y_min = 235703 (w0 exact)")
B3, ki3, ka3 = report_exact(YMIN, "this paper, y_min = 236000 (w0 exact)")
check("R2 reproduced at y_min=235702.26: bracket 30.418066, kappa_inf 0.0657356, kappa_all 0.0353633",
      abs(B1 - mpf('30.41806606')) < mpf('1e-7') and abs(ki1 - mpf('0.06573558619')) < mpf('1e-10') and abs(ka1 - mpf('0.03536325287')) < mpf('1e-10'))
check("R1 reproduced at y_min=235703: bracket 30.418065 (R1 used a cruder Gamma, 1.614e-5), kappa_inf 0.0657356, kappa_all 0.0353632",
      abs(B2 - mpf('30.418065')) < mpf('2e-6') and abs(ki2 - mpf('0.0657356')) < mpf('1e-7') and abs(ka2 - mpf('0.0353632')) < mpf('1e-7'))
check("R2 reproduced at y_min=236000: bracket 30.41757556, kappa_inf 0.06573664666, kappa_all 0.03536198503",
      abs(B3 - mpf('30.41757556')) < mpf('1e-7') and abs(ki3 - mpf('0.06573664666')) < mpf('1e-10') and abs(ka3 - mpf('0.03536198503')) < mpf('1e-10'))
for ym in (mpf(300000), mpf(10)**6):
    report_exact(ym, "larger y_min (for Remark rem:k)")

print("=================== constants of the text (y_min = 236000) ===================")
alp = 1/(Cp*YMIN); al = 1/(C*YMIN)
print("alpha'(y_min) =", mp.nstr(alp, 12), "  alpha(y_min) =", mp.nstr(al, 12))
check("lem:Bh applies: alpha'(y_min) <= 1.4982e-6 <= 1.5e-6", alp <= mpf('1.4982e-6') <= mpf('1.5e-6'), alp)
check("y_min = 236000 >= 1/(C' 1.5e-6) = 235702.26 (smallest y_min allowed by lem:Bh)", YMIN >= 1/(Cp*mpf('1.5e-6')), 1/(Cp*mpf('1.5e-6')))
check("lem:Bv (restated, bbar <= 3e-6) applies: alpha(y_min) <= 2.119e-6 <= 3e-6", al <= mpf('2.119e-6') <= mpf('3e-6'), al)
check("lem:Bv restated: theta1(2-theta1)/40 >= Q* bbar(2-bbar)/4 for bbar = 3e-6", TH1*(2 - TH1)/40 >= Qs*mpf('3e-6')*(2 - mpf('3e-6'))/4,
      TH1*(2 - TH1)/40 - Qs*mpf('3e-6')*(2 - mpf('3e-6'))/4)
check("lem:Bv restated: 4 sqrt(K/Q*)/(2 - bbar) <= A for bbar <= 3e-6 (A unchanged)", 4*sqrt(9/Qs)/(2 - mpf('3e-6')) <= A_of(9))
check("sec x - 1 <= 0.50001 x^2 for x <= 1e-3 (value at 1e-3, the ratio is increasing)", (sec(mpf('1e-3')) - 1)/mpf('1e-6') < mpf('0.50001'),
      (sec(mpf('1e-3')) - 1)/mpf('1e-6'))
check("alpha(y_min), alpha'(y_min) <= 1e-3 (crack lemma, sec bound)", al <= mpf('1e-3') and alp <= mpf('1e-3'))
# Lemma lem:Q at s >= y_min (every bound below is decreasing in s, checked on a grid too)
al_, nq, w0e, BZ, g0e = quant(YMIN)
print("lem:Q: n(sec a-1) <", mp.nstr(nq, 10), " exact w0 bound", mp.nstr(w0e, 12), "  lem:GZ: |B_Z| <", mp.nstr(BZ, 12), " g0 exact", mp.nstr(g0e, 12))
check("lem:Q: n(sec alpha - 1) < 5.3e-7", nq < mpf('5.3e-7'), nq)
check("lem:Q: beta < n + delta + 5.3e-7 = n + 1.053e-5", delta + mpf('5.3e-7') <= mpf('1.053e-5'))
from fractions import Fraction as Fr
check("lem:Q: sin a(Z) < alpha <= 2.119e-6; lower ramp < n + 1.053e-5 + 2.119e-6 = n + 1.2649e-5 (exact rationals)",
      Fr('1.053e-5') + Fr('2.119e-6') == Fr('1.2649e-5') and Fr('1e-5') + Fr('5.3e-7') == Fr('1.053e-5') and Fr('1.2649e-5') < Fr('1.265e-5'))
check("lem:Q: cos alpha - sin alpha > 1 - 2.12e-6", cos(al) - sin(al) > 1 - mpf('2.12e-6'), 1 - (cos(al) - sin(al)))
W0 = mpf('1.265e-5')
check("lem:Q: w0 = 1.265e-5 > 1.2649e-5 > 2.12e-6 (and > exact bound 1.264832e-5)", W0 > mpf('1.2649e-5') > mpf('2.12e-6') and W0 > w0e, w0e)
check("lem:Q: w0 = 1.265e-5 would FAIL at y_min = 235702.26 (as R2 found): exact bound there > 1.265e-5",
      quant(1/(Cp*mpf('1.5e-6')))[2] > W0, quant(1/(Cp*mpf('1.5e-6')))[2])
check("lem:GZ: tan alpha < 1.000001 alpha; 3.02 delta 1.000001 <= 3.04e-5; alpha + 2.01 delta tan alpha <= 1.01 alpha",
      tan(al) < mpf('1.000001')*al and mpf('3.02')*delta*mpf('1.000001') <= mpf('3.04e-5') and al + mpf('2.01')*delta*tan(al) <= mpf('1.01')*al)
check("lem:GZ: |B_Z| < 0.500023", BZ < mpf('0.500023'), BZ)
G0 = mpf('0.49997')
check("lem:GZ: g0: 1 - 2.12e-6 - 0.500023 > 0.49997", 1 - mpf('2.12e-6') - mpf('0.500023') > G0, 1 - mpf('2.12e-6') - mpf('0.500023'))
grid_ok = True
for s in [YMIN*(1 + mpf(j)/10) for j in range(0, 50)] + [mpf(10)**e for e in range(6, 14)]:
    a_, n_, w_, b_, g_ = quant(s)
    grid_ok &= (n_ <= nq and w_ <= w0e and b_ <= BZ and a_ <= al)
check("lem:Q/GZ bounds are largest at s = y_min (grid s in [y_min, 5.9 y_min] and 1e6..1e13)", grid_ok)
A = A_of(9)
Ab = mpf('10.6067')
check("A = 4 sqrt(9/0.32)/(2 - 3e-6) < 10.6067, A >= 2", A < Ab and A >= 2, A)
check("C'(1 - eps) > C", Cp*(1 - eps) > C)
check("vertical extent < 1.0001 for a < alpha'((1-eps) y_min)", cos(alp/(1 - eps)) + sin(alp/(1 - eps)) < mpf('1.0001'))
# Gamma
Gc, Gn = Gamma_of(A, YMIN)
print("Gamma =", mp.nstr(Gc, 12), " (quad", mp.nstr(Gn, 12), ")")
check("Gamma = 1.00002(A/(C' y_min) + 1/(2 C'^2 delta y_min^2)) < 1.61e-5 (closed form = quadrature)", Gc < mpf('1.61e-5') and abs(Gc - Gn) < mpf('1e-25'), Gc)
Gb = 2*mpf('0.50001')*(Ab/(Cp*YMIN) + 1/(2*Cp**2*delta*YMIN**2))
check("Gamma with A < 10.6067 also < 1.61e-5", Gb < mpf('1.61e-5'), Gb)
# bracket
t1 = 1/(om0*YMIN); t2 = mpf('2.01')/(eps*YMIN); t3 = al/delta
print("1/(om0 y_min) =", mp.nstr(t1, 12), " 2.01/(eps y_min) =", mp.nstr(t2, 12), " alpha(y_min)/delta =", mp.nstr(t3, 12))
check("1/(omega0 y_min) < 0.021187, 2.01/(eps y_min) < 4.2585e-3, alpha(y_min)/delta < 0.21187",
      t1 < mpf('0.021187') and t2 < mpf('4.2585e-3') and t3 < mpf('0.21187'))
br = mpf('0.021187') + SQ2*Ab + (1 + mpf('4.2585e-3'))/(SQ2*G0*(1 - eps))*(Ab + mpf('0.21187')) + mpf('1.61e-5')
Bb = (floor(br*1000) + 1)/1000
print("bracket (rounded constants) =", mp.nstr(br, 12), " -> bound", Bb)
check("bracket < 30.418", br < mpf('30.418') and Bb == mpf('30.418'), br)
c3r = (1 + mpf('4.2585e-3'))/(SQ2*G0*(1 - eps))
print("c3 = (1+2.01/(eps y_min))/(sqrt2 g0 (1-eps)) <", mp.nstr(c3r, 10))
# ell(H)
h0 = 1 - 2*W0
lead = (1 - om0)*h0
check("(1 - omega0) h0 >= 0.99977 (h0 = 1 - 2 w0)", lead >= mpf('0.99977'), lead)
L0 = log(2/(1 - eps)) + log(YMIN + 1)
print("L0 = log(2/(1-eps)) + log(y_min+1) =", mp.nstr(L0, 15))
check("log(2/(1-eps)) + log(y_min+1) < 13.066741", L0 < mpf('13.066741'), L0)
check("log(1 - 6/k) > -1e-11 for k >= 1e12", log(1 - 6/K3) > mpf('-1e-11'), log(1 - 6/K3))
check("hence ell(H) >= 2 h0 (log k - 13.06675) for k >= 1e12", L0 + mpf('1e-11') < mpf('13.06675'))
check("j1 = floor((1-eps)(k/2-3)) > j0 = y_min for k >= 1e12 (H_b contains the unit intervals)", floor((1 - eps)*(K3/2 - 3)) > YMIN)
check("(1-eps)(k/2-3) = (1-eps)(k/2)(1-6/k) identity at k = 1e12", (1 - eps)*(K3/2 - 3) == (1 - eps)*(K3/2)*(1 - 6/K3))
# F(k) and kappa
SL = 2*mpf('0.99977')
check("2(1-omega0)h0 >= 1.99954", 2*lead >= SL, 2*lead)
F = lambda L: SL*(L - mpf('13.06675'))/Bb
check("for 2 <= k < 1e12: log k < 27.632 and F(k) < 0.958 < 1", log(K3) < mpf('27.632') and F(mpf('27.632')) < mpf('0.958'), F(log(K3)))
Lstar = findroot(lambda L: F(L) - 1, 28)
print("F(k) = 1 at log k* =", mp.nstr(Lstar, 15), "  1/log k* =", mp.nstr(1/Lstar, 15), "  limit 1.99954/30.418 =", mp.nstr(SL/Bb, 15))
check("F exceeds 1 exactly for log k > 28.2792... (28.2792 < log k* < 28.2793)", mpf('28.2792') < Lstar < mpf('28.2793'), Lstar)
check("kappa_all = 1/log k* = 0.035361... in [0.0353, 0.0354): stated value 0.0353 is rounded DOWN", mpf('0.0353') <= 1/Lstar < mpf('0.0354')
      and mpf('0.035361') < 1/Lstar < mpf('0.035362'), 1/Lstar)
check("limit 1.99954/30.418 = 0.065735... (stated 0.0657)", mpf('0.065735') < SL/Bb < mpf('0.065736'), SL/Bb)
check("F(k)/log k increasing in k (offset negative): derivative of (L-13.06675)/L > 0", mpf('13.06675') > 0)
# proof of kappa = 0.0353 in the text
check("text: if 0.0353 log k > 1 then log k > 28.32 (1/0.0353 = 28.328...)", 1/mpf('0.0353') > mpf('28.32'), 1/mpf('0.0353'))
lhs = (SL/Bb - mpf('0.0353'))*mpf('28.32') - SL*mpf('13.06675')/Bb
check("text: (1.99954/30.418 - 0.0353) 28.32 - 1.99954*13.06675/30.418 > 0, so F(k) > 0.0353 log k for log k > 28.32", lhs > 0, lhs)
check("text: (1.99954/30.418 - 0.0353) > 0.03043 and 1.99954*13.06675/30.418 < 0.85895 and 0.03043*28.32 > 0.85895",
      SL/Bb - mpf('0.0353') > mpf('0.03043') and SL*mpf('13.06675')/Bb < mpf('0.85895') and mpf('0.03043')*mpf('28.32') > mpf('0.85895'))
# brute-force: inf over integers k >= 2 of max(1,F(k))/log k, using the bound W >= max(1, F)
mn = min([max(1, F(log(mpf(k))))/log(mpf(k)) for k in range(2, 2000)] +
         [max(1, F(L))/L for L in [mpf(i)/1000 for i in range(int(log(2000)*1000), 200000)]])
check("grid inf_k max(1,F(k))/log k >= 0.0353 (log k up to 200)", mn >= mpf('0.0353'), mn)
# s(k^2 - c) = k thresholds
th = lambda c: mpf('13.06675') + Bb*c/SL
print("s(k^2-c)=k thresholds: c=1..5:", [mp.nstr(th(c), 8) for c in range(1, 6)])
check("rate: exact threshold 13.06675 + 30.418c/1.99954 <= 15.22c + 13.07 for all c >= 0; s(k^2-4)=k for log k > 73.92",
      Bb/SL <= mpf('15.22') and mpf('13.06675') <= mpf('13.07') and th(4) < mpf('73.92') and th(4) > mpf('73.91'), th(4))
check("intro: 1/0.0353 ~ 28.3", abs(1/mpf('0.0353') - mpf('28.3')) < mpf('0.05'))
check("rem:k: architecture limit for the slope 1/(sqrt2 A_inf) = sqrt(Q*/K)/(2 sqrt2) ~ 0.066667", abs(sqrt(Qs/9)/(2*SQ2) - mpf('0.066667')) < mpf('1e-6'),
      sqrt(Qs/9)/(2*SQ2))
check("rem:k: kappa_all < 1/13.06 for any bracket (L* > 13.06675)", 1/mpf('13.06675') < 1/mpf('13.06'))
# K_w = 13 variant (hand proof only)
A13 = A_of(13)
check("K_w = 13: A < 12.7476", A13 < mpf('12.7476'), A13)
G13 = 2*mpf('0.50001')*(mpf('12.7476')/(Cp*YMIN) + 1/(2*Cp**2*delta*YMIN**2))
br13 = mpf('0.021187') + SQ2*mpf('12.7476') + c3r*(mpf('12.7476') + mpf('0.21187')) + G13
B13 = (floor(br13*1000) + 1)/1000
L13 = findroot(lambda L: SL*(L - mpf('13.06675'))/B13 - 1, 31)
print("K_w = 13: Gamma13 =", mp.nstr(G13, 8), " bracket", mp.nstr(br13, 12), "->", B13, " log k* =", mp.nstr(L13, 12),
      " kappa_all =", mp.nstr(1/L13, 12), " slope =", mp.nstr(SL/B13, 12))
check("K_w = 13: Gamma13 < 1.93e-5 and bracket < 36.493", G13 < mpf('1.93e-5') and br13 < mpf('36.493') and B13 == mpf('36.493'), br13)
check("K_w = 13: kappa_all = 1/log k* in [0.0319, 0.0320) (stated 0.0319), slope 1.99954/36.493 = 0.05479...",
      mpf('0.0319') <= 1/L13 < mpf('0.0320') and mpf('0.0547') < SL/B13 < mpf('0.0548'), 1/L13)
lhs13 = (SL/B13 - mpf('0.0319'))/1*(1/mpf('0.0319')) - SL*mpf('13.06675')/B13
check("K_w = 13: F13(k) > 0.0319 log k whenever 0.0319 log k > 1", lhs13 > 0, lhs13)
# Q* = 1/3 variant (asymptotic slope)
A3 = A_of(9, mpf(1)/3)
G3 = 2*mpf('0.50001')*(A3/(Cp*YMIN) + 1/(2*Cp**2*delta*YMIN**2))
br3 = t1 + SQ2*A3 + c3r*(A3 + mpf('0.21187')) + G3
print("Q* = 1/3: A =", mp.nstr(A3, 10), " bracket", mp.nstr(br3, 10), " slope", mp.nstr(SL/br3, 10),
      " kappa_all", mp.nstr(1/findroot(lambda L: SL*(L - mpf('13.06675'))/br3 - 1, 28), 10))
check("rem:const: with Q* = 1/3, asymptotically about 0.0670", abs(SL/br3 - mpf('0.0670')) < mpf('2e-4'), SL/br3)
print("ALL OK" if ok else "SOME CHECK FAILED")
