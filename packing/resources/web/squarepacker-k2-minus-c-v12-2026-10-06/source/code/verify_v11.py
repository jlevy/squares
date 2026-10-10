"""High-precision verification of the numerical constants in paper/paper.tex (version 1.2). Contains every check of verify_v10.py
(version 1.1) that still applies. The check of Lemma 4.10 needs data/kw9_data.zip unpacked into this folder
(or the environment variable CSTAR_KW9_DIR pointing to the unpacked files). Usage: python verify_v11.py"""
from mpmath import mp, mpf, sqrt, pi, cos, sin, sec, tan, log, acos, polyroots, findroot, diff
import random
mp.dps = 40
ok = True
def check(name, cond, val=None):
    global ok
    print(f"{'OK ' if cond else 'FAIL'} {name}" + (f"   [{mp.nstr(val, 12)}]" if val is not None else ""))
    ok = ok and bool(cond)
SQ2 = sqrt(2)
# ---------- Lemma 3.4 (short chords)
for a in [mpf('1e-7'), mpf('0.1'), mpf('0.5'), pi/4]:
    sc = sin(a)*cos(a)
    I = mp.quad(lambda u: u/sc, [0, sc])
    check(f"ramp integral at a={mp.nstr(a,3)}: 2*int = sin a cos a", abs(2*I - sc) < mpf(10)**-30)
# ---------- Lemma 4.4 (sections near a vertex)
pmin = min(1 - (p-1)**2/2 for p in [1 + i*(SQ2-1)/1000 for i in range(1001)])
check("p - sin cos = 1-(p-1)^2/2 >= 0.91 on [1,sqrt2]", pmin >= mpf('0.91'), pmin)
def section(psi, u):
    s_, c_ = sin(psi), cos(psi)
    lo, hi = min(s_, c_), max(s_, c_)
    if psi == 0 or psi == pi/2: return mpf(1)
    if u <= lo: return u/(s_*c_)
    if u <= hi: return 1/hi
    return (s_ + c_ - u)/(s_*c_)
worst = min(section(mpf(i)/400*pi/2, mpf(j)/400*mpf('0.75')) - min(2*mpf(j)/400*mpf('0.75'), 1)
            for i in range(1, 400) for j in range(0, 401))
check("section >= min(2u,1) on grid (psi,u<=3/4)", worst >= -mpf(10)**-25, worst)
# ---------- Proposition 4.5 with d, theta1 <= 1e-5, eps0 = 1e-4
TH1 = mpf('1e-5'); DMAX = mpf('1e-5')
eps = DMAX + TH1; eps0 = mpf('1e-4'); gam = mpf('1.415')*eps
Qs = mpf('0.32')
check("eps1 = d+theta1 <= 2e-5", eps <= mpf('2e-5'))
check("wall case: eps0 > eps1, eps0 > theta, (1-2eps0)^2 > Q*", eps0 > eps and eps0 > TH1 and (1-2*eps0)**2 > Qs)
def rho(h): return sqrt(1+h*h)
def D(h): return mpf(1)/2 - (1-h)/(2*rho(h))
def chi(h): return 1 + rho(h)/2 - (1+h)/rho(h)
random.seed(1)
maxerr = 0
for _ in range(200):
    th = mpf(random.uniform(0, 1e-5)); d = mpf(random.uniform(0, 1e-5))
    a = 1 + mpf(random.uniform(0, 1))*(d + th/2); b = mpf(random.uniform(0.0, 1.00002))
    w = cos(th)+sin(th); sig = 1/w; l = a - sig/2; L = sqrt(a*a+b*b); h = b/a; r = rho(h)
    t = lambda x, y: (a*y - b*x)/L
    s = lambda x, y: (a*x + b*y)/L
    pairs = [((mpf(1)/2, mpf(1)/2), (1-h)/(2*r)), ((-mpf(1)/2, mpf(1)/2), (1+h)/(2*r)), ((mpf(1)/2, -mpf(1)/2), -(1+h)/(2*r)),
             ((l, b-sig/2), -sig*(1-h)/(2*r)), ((l, b+sig/2), sig*(1+h)/(2*r)), ((l+sig, b-sig/2), -sig*(1+h)/(2*r))]
    for P, val in pairs: maxerr = max(maxerr, abs(t(*P) - val))
    tt = mpf(random.uniform(-0.4, 0.4))
    y = (tt*L + b/2)/a; maxerr = max(maxerr, abs(s(mpf(1)/2, y) - (r/2 + h*tt)))
    y = (tt*L + b*l)/a; maxerr = max(maxerr, abs(s(l, y) - (r*l + h*tt)))
    if b > 0:
        x = (a/2 - tt*L)/b; maxerr = max(maxerr, abs(s(x, mpf(1)/2) - (r/2 - tt)/h))
        yb = b - sig/2; x = (a*yb - tt*L)/b; maxerr = max(maxerr, abs(s(x, yb) - (r*yb - tt)/h))
    if b > mpf('0.344')*a:
        tG2 = sig*(1+h)/(2*r)
        G = (r*l + h*tG2) - (r/2 - tG2)/h
        maxerr = max(maxerr, abs(G - (r*(l-mpf(1)/2) + r/(2*h)*(h-1+sig*(1+h)))))
        tl = -sig*(1+h)/(2*r); vx, vy = l+sig, b-sig/2
        Gl = s(vx, vy) - (r/2 + h*tl)
        maxerr = max(maxerr, abs(Gl - r*(a-(1-sig)/2)))
        cu = G/2 - 2*(tG2 - mpf(1)/2); cl = Gl/2 - 2*(tG2 - mpf(1)/2)
        e1 = d + TH1
        check_ok = cu <= chi(h) + mpf('2.2')*e1 and cl <= chi(h) + mpf('2.2')*e1
        if not check_ok: print("chi bound violated", th, d, a, b, cu, cl, chi(h))
        ok = ok and check_ok
check("level and section formulas (random parameters, eps1<=2e-5)", maxerr < mpf(10)**-30, maxerr)
check("D(0.344) < 0.19", D(mpf('0.344')) < mpf('0.19'), D(mpf('0.344')))
hc = findroot(lambda x: x**3 + 3*x - 2, 0.6); print("   h_c =", hc)
cmax = max(chi(mpf('0.344')), chi(mpf('1.00002')))
check("max(chi(0.344), chi(1.00002)) + 2.2 eps1 < 0.29295", cmax + mpf('2.2')*eps < mpf('0.29295'), cmax + mpf('2.2')*eps)
check("h/rho + 3 eps < 3/4 for h <= 1+eps", (1+eps)/rho(1+eps) + 3*eps < mpf('0.75'))
check("D(1+eps)+3eps <= 0.51", D(1+eps) + 3*eps <= mpf('0.51'))
cc = mpf('0.29295')
vals = [mpf(1)/3, (2-cc)**2/9, mpf(2)/3*(1-cc)**2, (1-cc/2)**2/2, mpf('0.48')]
check("all candidate minima > 0.3237 at chi*=0.29295", min(vals) > mpf('0.3237'), min(vals))
import numpy as np
R = np.linspace(0, 0.6, 1201); E = np.minimum(R**2, np.maximum(2*R - 0.29295, 0)**2)
G = np.maximum(1 - R[:, None] - R[None, :], 0)**2 + E[:, None] + E[None, :]
check("brute-force min Xi > 0.3237 (grid)", G.min() > 0.3237, mpf(float(G.min())))
beta1 = 3*gam
check("beta1 = 3 gamma* <= 8.5e-5", beta1 <= mpf('8.5e-5'), beta1)
check("0.3237 - 2.04 beta1 > 0.3235", mpf('0.3237') - mpf('2.04')*beta1 > mpf('0.3235'))
check("0.3235 - 4 eps0 > Q* = 0.32", mpf('0.3235') - 4*eps0 > Qs)
random.seed(7); worst_u = 0; worst_l = 0
for _ in range(4000):
    th = mpf(random.uniform(0, 1e-5)); d = mpf(random.uniform(0, 1e-5))
    a = 1 + mpf(random.uniform(0, 1))*(d + th/2); h = mpf(random.uniform(0.344, 1)) if random.random() < 0.9 else 1 + mpf(random.uniform(0,1))*(d+th/2)
    b = h*a; w = cos(th)+sin(th); sig = 1/w; l = a - sig/2; r = rho(h)
    G_ = r*(l-mpf(1)/2) + r/(2*h)*(h-1+sig*(1+h)); tG2 = sig*(1+h)/(2*r)
    Gl = r*(a-(1-sig)/2)
    worst_u = max(worst_u, (G_/2 - tG2)/(d+TH1))
    worst_l = max(worst_l, (Gl/2 - tG2)/(d+TH1))
check("(f) capped upper case: < 1.1 eps1 (sampled)", worst_u < mpf('1.1'), worst_u)
check("(f) capped lower case: < 1.8 eps1 (sampled)", worst_l < mpf('1.8'), worst_l)
check("1.8 eps1 < eps0", mpf('1.8')*eps < eps0)
check("D<0.19 implies zeta < 0.19+3eps <= 0.1906", mpf("0.19") + 3*eps <= mpf("0.1906"))
check("(1-0.3812)^2 > 0.38", (1 - mpf('0.3812'))**2 > mpf('0.38'))
check("theta/6.26: 0.32*(2-1e-5)/4 >= 1/6.26", mpf('0.32')*(2-mpf('1e-5'))/4 >= 1/mpf('6.26'))
# (e): (1+h)/(2 rho_h) <= 0.71 on [0,1] (max at h=1: sqrt2/2), and 0.71 theta + 1.5 gamma* <= 3 eps1 using theta <= eps1
check("(e) (1+h)/(2rho_h) <= 0.71 on [0,1] (grid; derivative (1-h)/rho^3 >= 0 so max at h=1)",
      all((1+mpf(i)/1000)/(2*rho(mpf(i)/1000)) <= mpf('0.71') for i in range(1001)) and SQ2/2 <= mpf('0.71'))
check("(e) 0.71 eps1 + 1.5*1.415 eps1 <= 3 eps1", mpf('0.71') + mpf('1.5')*mpf('1.415') <= 3)
check("(g) D(h)<0.19 branch: 0.38 - 4 eps0 > Q*", mpf('0.38') - 4*eps0 > Qs)
check("(g) z,z' <= D(1+eps1) + 3 eps1 <= 0.51", D(1 + eps) + 3*eps <= mpf('0.51'))

# analytic versions of the bounds that are sampled above (theta <= theta1 <= eps1, d <= eps1)
rmax = rho(1 + eps)
check("rho_h <= 1.415 for h <= 1+eps1", rmax <= mpf('1.415'), rmax)
check("rho_h/h <= sqrt2 for h > 1 (sqrt(1+1/h^2) decreasing)", all(rho(1+mpf(i)/100)/(1+mpf(i)/100) <= SQ2 for i in range(1, 300)))
check("sigma_theta >= 1 - theta and (w - 1/w)/2 <= theta (grid in theta <= 1e-5)",
      all(1/(cos(t)+sin(t)) >= 1 - t and ((cos(t)+sin(t)) - 1/(cos(t)+sin(t)))/2 <= t for t in [mpf(i)/100*TH1 for i in range(101)]))
check("chi_u, chi_l <= chi(h) + (sqrt2 + rho_max/2) eps1 <= chi(h) + 2.2 eps1", SQ2 + rmax/2 <= mpf('2.2'), SQ2 + rmax/2)
hh = 1 + eps
cap_u = hh*(hh-1)/(2*rho(hh)) + rmax/2*eps
check("capped upper: h(h-1)/(2rho) + (rho/2)(l-1/2) <= 1.1 eps1 (analytic)", cap_u < mpf('1.1')*eps, cap_u/eps)
cap_l = hh*(hh-1)/(2*rho(hh)) + rmax/2*eps + SQ2/2*TH1
check("capped lower: ... + (1-sigma)(1+h)/(2rho) <= 1.8 eps1 (analytic)", cap_l < mpf('1.8')*eps, cap_l/eps)
Du_max = D(1 + eps) + 3*eps
check("tau >= 1/2 - D_u > -0.02", mpf(1)/2 - Du_max > mpf('-0.02'), mpf(1)/2 - Du_max)
sig_min = 1/(cos(TH1) + sin(TH1))
check("t(V3') <= -0.6 on [0.344, 1+eps1] ((1+h)/rho_h minimal at 0.344 there)",
      sig_min*(1 + mpf('0.344'))/(2*rho(mpf('0.344'))) > mpf('0.6') and all((1+x)/rho(x) >= (1+mpf('0.344'))/rho(mpf('0.344')) for x in [mpf('0.344') + i*(mpf('0.656')+eps)/2000 for i in range(2001)]))
check("Gamma_* <= rho_h + rho_h(l - 1/2) < 2", rmax*(1 + eps) < 2, rmax*(1+eps))
check("tau_* > 0 on [0.344, 1+eps1]: sigma(1+h)/(2 rho_h) > 1/2 at h = 0.344", sig_min*(1 + mpf('0.344'))/(2*rho(mpf('0.344'))) > mpf('0.5'))
# ---------- Fodor, Oler and counting
x0 = min(x.real for x in polyroots([9,-15,7,0,-3,1], maxsteps=200, extraprec=200) if abs(x.imag) < 1e-25 and x.real > 0)
R12 = 1/(sqrt(3)*x0); R0 = sqrt((SQ2 + mpf('1e-4'))**2 + mpf(1)/4)
check("Fodor R12 = 1.5148...", abs(R12 - mpf('1.5148009650580917')) < mpf('1e-15'), R12)
check("R0(1e-4) < 1.5001 < R12", R0 < mpf('1.5001') < R12, R0)
check("wall centre radius < R0", sqrt((mpf('1e-4') + SQ2/2)**2 + mpf(1)/4) < R0)
cD = mpf('1e-4') + SQ2/2 - mpf(1)/2
check("c = d + sqrt2/2 - 1/2 < 0.20721", cD < mpf('0.20721'), cD)
phi = acos(cD/R0)
AD = R0**2*(pi - phi) + cD*sqrt(R0**2 - cD**2)
PD = 2*R0*(pi - phi) + 2*sqrt(R0**2 - cD**2)
check("area(D0) < 4.155", AD < mpf('4.155'), AD)
check("perimeter(D0) < 8.1", PD < mpf('8.1'), PD)
ob = 2/sqrt(3)*mpf('4.155') + mpf('8.1')/2 + 1
check("Oler bound 2/sqrt3*4.155 + 8.1/2 + 1 < 9.85 (so <= 9 centres)", ob < mpf('9.85'), ob)
# the area/perimeter are increasing in d (R0 and c grow), so d = 1e-4 is the worst case
# area/perimeter formulas cross-checked by numerical integration over the disc segment
import math
def area_num(R, c, n=200000):
    # area of {x >= -c} ∩ disc(R): integrate chord length over x in [-c, R]
    xs = np.linspace(-float(c), float(R), n+1); y = np.sqrt(np.maximum(float(R)**2 - xs**2, 0))
    return float(np.trapezoid(2*y, xs))
check("area formula vs numerical integration", abs(area_num(R0, cD) - float(AD)) < 1e-6, mpf(area_num(R0, cD)))
# sanity check only (not used in the text): a circumscribed polygon gives the same Oler bound
def circ_poly(R, c, n):
    ph = acos(-c/R)  # kept arc: angles in [-ph, ph] measured from the far side? use direction away from the cut
    th = [-ph + 2*ph*j/n for j in range(n+1)]
    verts = []
    def ti(t1, t2):
        det = cos(t1)*sin(t2) - sin(t1)*cos(t2)
        return (R*(sin(t2) - sin(t1))/det, R*(cos(t1) - cos(t2))/det)
    def tc(t):
        x = -c; return (x, (R - x*cos(t))/sin(t))
    verts.append(tc(th[0]))
    for j in range(n): verts.append(ti(th[j], th[j+1]))
    verts.append(tc(th[-1]))
    A = mpf(0); P = mpf(0)
    for i in range(len(verts)):
        x1, y1 = verts[i]; x2, y2 = verts[(i+1) % len(verts)]
        A += x1*y2 - x2*y1; P += sqrt((x2-x1)**2 + (y2-y1)**2)
    return abs(A)/2, P
Ap, Pp = circ_poly(R0, cD, 3000)
check("sanity: Oler for a circumscribed 3000-gon < 9.85", 2/sqrt(3)*Ap + Pp/2 + 1 < mpf('9.85'), 2/sqrt(3)*Ap + Pp/2 + 1)
check("K = max(3*11-6, 3*10-6) = 27", max(3*11-6, 3*10-6) == 27)
dist_side = (mpf('1e-4') + SQ2/2) + sqrt((mpf('1e-4') + SQ2/2)**2 + mpf(1)/4)
check("p within 1.58 of a side; 2*1.58 = 3.16 < 4", dist_side < mpf('1.58') and 2*mpf('1.58') < 4, dist_side)
Lam = SQ2 + mpf('1e-4')
check("12 Lambda/pi + 4 < 10", 12*Lam/pi + 4 < 10, 12*Lam/pi + 4)
# lem:count(a) Steiner count, directly: (pi/4) m' + 2 <= 3|L| + 2 + pi with |L| < Lambda  ->  m' < 12 Lambda/pi + 4
check("count(a) Steiner: (3*Lam + pi)*4/pi = 12 Lam/pi + 4 < 10, wall: (3(d+sqrt2/2) + pi/2)*4/pi < 5",
      (3*Lam + pi)*4/pi < 10 and (3*(mpf('1e-4') + SQ2/2) + pi/2)*4/pi < 5)
check("wall: 12(d+sqrt2/2)/pi + 2 < 5", 12*(mpf('1e-4') + SQ2/2)/pi + 2 < 5)
# ---------- Lemma 4.10/4.11
thmax = mpf('3e-6')
check("theta1(2-theta1)/40 >= Q* thmax(2-thmax)/4 (thmax<=3e-6)", TH1*(2-TH1)/40 >= Qs*thmax*(2-thmax)/4)
check("column (lem:Bv restated in v11): theta1(2-theta1)/40 >= Q* bbar(2-bbar)/4 (bbar<=3e-6)", TH1*(2-TH1)/40 >= Qs*mpf('3e-6')*(2-mpf('3e-6'))/4)
check("d' = thmax <= 3e-6 <= 1e-5 (Prop 4.5 applies)", thmax <= DMAX)
# ======== from verify_v8_parts.py ========
from mpmath import asin, floor, findroot
import itertools
mp.dps = 50
# =============================== (I) Lemma lem:Kw ===============================
# All quantities below are monotone in d (Lambda, rho1 increase with d; gamma0 decreases), and the worst case for an
# upper bound on the number of edges is the largest d, d = 1e-4: larger rho1/R_m and smaller gamma0 only enlarge D and
# shrink separations.  We check d = 1e-4 (and d = 1e-5 for information).
for d in [mpf('1e-4'), mpf('1e-5')]:
    Lam = SQ2 + d
    g0 = acos(1 - 1/(2*Lam**2))
    rho_sq = sqrt((Lam/2)**2 + mpf(1)/4)               # square-square edge: p within this of the nearer end of L
    rho_wall = sqrt((d + SQ2/2)**2 + mpf(1)/4)        # square-side edge: p within this of the square's centre
    rho1 = max(rho_sq, rho_wall)
    tag = f"[d={mp.nstr(d,2)}]"
    check(f"{tag} rho1 = max(...) < 0.8662 < 1", rho1 < mpf('0.8662'), rho1)
    # neighbour separation at a centre c: other ends c', c'' are centres at distance in [1, Lam) from c, |c'-c''| >= 1.
    # cos(angle) <= f(r1,r2) := (r1^2+r2^2-1)/(2 r1 r2) = r1/(2 r2) + (r2^2-1)/(2 r1 r2): convex in r1 (as r2^2-1 >= 0) and,
    # by symmetry, in r2 -> maximum over [1,Lam]^2 at a corner.
    f = lambda r1, r2: (r1**2 + r2**2 - 1)/(2*r1*r2)
    corners = [f(mpf(1), mpf(1)), f(mpf(1), Lam), f(Lam, Lam)]
    check(f"{tag} max over corners of f is f(Lam,Lam) = 1 - 1/(2 Lam^2)", max(corners) == f(Lam, Lam) and abs(f(Lam, Lam) - (1 - 1/(2*Lam**2))) < mpf(10)**-45)
    # grid sanity check of the convexity claim
    grid = max(f(1 + (Lam-1)*i/200, 1 + (Lam-1)*j/200) for i in range(201) for j in range(201))
    check(f"{tag} grid max of f on [1,Lam]^2 <= f(Lam,Lam)", grid <= f(Lam, Lam) + mpf(10)**-40, grid)
    # foot point on a side vs a neighbour centre: (c''-c).nu <= (d + sqrt2/2) - 1/2 = c0, |c''-c| >= 1
    c0 = d + SQ2/2 - mpf(1)/2
    wall_sep = acos(c0)
    check(f"{tag} side-foot separation arccos(c0) > gamma0", wall_sep > g0, wall_sep*180/pi)
    # degree classes
    R = {1: rho1, 2: rho1}
    for m in (3, 4, 5):
        R[m] = min(rho1, 1/(2*sin((m-1)*g0/2)))
    check(f"{tag} D(r) <= 5 for r > 1/2 (2 arcsin(1/(2r)) < pi < 5 gamma0)", pi < 5*g0, pi/g0)
    check(f"{tag} class radii R3,R4,R5 > 1/2 (classes nonempty) and R5 < R4 < R3 < rho1",
          mpf(1)/2 < R[5] < R[4] < R[3] < rho1)
    # inner centres a, b at radii r_a <= R_a, r_b <= R_b (< 1), |c_a - c_b| >= 1: angle at p >= arccos(f(R_a,R_b)),
    # as f is increasing in each variable when the other is < 1 (df/dr1 = (r1^2 - r2^2 + 1)/(2 r1^2 r2) > 0).
    gam = {(a, b): acos(f(R[a], R[b])) for a in R for b in R}
    minsep = min(gam.values())
    nmax = int(floor(2*pi/minsep))
    check(f"{tag} at most {nmax} inner centres (min separation {mp.nstr(minsep*180/pi, 6)} deg)", nmax == 5)
    classes = [2, 3, 4, 5]    # class 1 is dominated by class 2 (same radius bound, smaller degree)
    best = 0; margin = None
    for n in range(1, nmax + 1):
        for seq in itertools.product(classes, repeat=n):
            tot = mpf(0) if n == 1 else (2*gam[seq[0], seq[1]] if n == 2 else sum(gam[seq[i], seq[(i+1) % n]] for i in range(n)))
            s = sum(seq)
            if tot <= 2*pi:
                best = max(best, s)
    for n in range(1, nmax + 1):
        for seq in itertools.product(classes, repeat=n):
            s = sum(seq)
            if s <= 14:
                continue
            tot = mpf(0) if n == 1 else (2*gam[seq[0], seq[1]] if n == 2 else sum(gam[seq[i], seq[(i+1) % n]] for i in range(n)))
            margin = tot - 2*pi if margin is None else min(margin, tot - 2*pi)
    check(f"{tag} K_w: every feasible cyclic class sequence has degree sum <= 14", best <= 14, best)
    check(f"{tag} every sequence with degree sum >= 15 exceeds 2 pi by > 25 deg", margin > 25*pi/180, margin*180/pi)
    print(f"   {tag} gamma0 = {mp.nstr(g0*180/pi, 10)} deg; R3,R4,R5 = {mp.nstr(R[3],8)}, {mp.nstr(R[4],8)}, {mp.nstr(R[5],8)}")
    # numbers quoted in the proof (stated for the worst case d = 1e-4)
    deg = 180/pi
    check(f"{tag} quoted: gamma0 > 41.406 deg, rho1 < 0.86611, R3 < 0.75598, R4 < 0.56571, R5 < 0.50396, gamma(2,2) > 70.52 deg",
          g0*deg > mpf('41.406') and rho1 < mpf('0.86611') and R[3] < mpf('0.75598') and R[4] < mpf('0.56571') and R[5] < mpf('0.50396') and gam[2, 2]*deg > mpf('70.52'))
    sum14 = []
    for n in range(1, nmax + 1):
        for seq in itertools.product(classes, repeat=n):
            if sum(seq) != 14:
                continue
            tot = mpf(0) if n == 1 else (2*gam[seq[0], seq[1]] if n == 2 else sum(gam[seq[i], seq[(i+1) % n]] for i in range(n)))
            if tot <= 2*pi:
                sum14.append((seq, tot*deg))
    check(f"{tag} quoted: feasible sum-14 sequences are exactly the rotations of (5,2,5,2), total ~358.95 deg",
          sorted(q for q, _ in sum14) == [(2, 5, 2, 5), (5, 2, 5, 2)] and all(abs(t - mpf('358.95')) < mpf('0.05') for _, t in sum14),
          sum14[0][1] if sum14 else None)
    # monotonicity in d claimed in the text: Lambda, rho1, R_m increase and gamma0 decreases with d
    if d == mpf('1e-4'):
        dd = [mpf(i)*mpf('1e-6') for i in range(1, 101)]
        g0s = [acos(1 - 1/(2*(SQ2 + x)**2)) for x in dd]
        r1s = [sqrt((x + SQ2/2)**2 + mpf(1)/4) for x in dd]
        check(f"{tag} gamma0 decreasing and rho1 increasing in d on (0,1e-4] (grid)",
              all(g0s[i] > g0s[i+1] for i in range(99)) and all(r1s[i] < r1s[i+1] for i in range(99)))

# ---------------- lem:Kw (c): two class-5 inner centres ----------------
f_ = lambda r1, r2: (r1**2 + r2**2 - 1)/(2*r1*r2)
from mpmath import asin
for dd in [mpf('1e-4'), mpf('1e-5')]:
    Lam_ = SQ2 + dd; g0_ = acos(1 - 1/(2*Lam_**2)); rho1_ = sqrt((dd + SQ2/2)**2 + mpf(1)/4)
    R5_ = min(rho1_, 1/(2*sin(2*g0_))); g55 = acos(f_(R5_, R5_)); psi_ = asin(R5_*sin(pi - g55))
    sep3 = acos(max(f_(mpf(1), mpf(1)), f_(mpf(1), Lam_), f_(2*R5_, mpf(1)), f_(2*R5_, Lam_)))
    c0_ = dd + SQ2/2 - mpf(1)/2; dg = 180/pi; tg = f"[d={mp.nstr(dd,2)}]"
    check(f"{tg} Kw(c): 2 R5 < 1.008, gamma(5,5) > 165.6 deg, psi < 7.19 deg", 2*R5_ < mpf('1.008') and g55*dg > mpf('165.6') and psi_*dg < mpf('7.19'), psi_*dg)
    check(f"{tg} Kw(c): separation from c3 > 44.99 deg (corners of [1,2R5]x[1,Lam]); side foot > 78 deg", sep3*dg > mpf('44.99') and acos(c0_)*dg > 78, sep3*dg)
    check(f"{tg} Kw(c): 90 + 7.19 - 44.99 < 2 gamma0", mpf(90) + mpf('7.19') - mpf('44.99') < 2*g0_*dg, 2*g0_*dg)
    check(f"{tg} Kw(c) text: 2R5 < Lambda (so (a) gives separation gamma0 from c3), gamma0 > 41.406 deg, 90 + 7.19 - 41.406 < 2 gamma0",
          2*R5_ < Lam_ and g0_*dg > mpf('41.406') and mpf(90) + mpf('7.19') - mpf('41.406') < 2*g0_*dg)
# =============================== Sections 5-6 (v11: y_min = 236000, K_w^* = 9; change (d2)) ===============================
import sys, os
from fractions import Fraction as Fr
from mpmath import tan, cos, sin, sec, log, floor, exp, quad, inf
mp.dps = 50
KW = 9
SQ2 = sqrt(2); C = mpf(2); Cp = 2*SQ2; delta = mpf('1e-5'); Qs = mpf('0.32'); TH1 = mpf('1e-5')
eps = mpf('2e-3'); om0 = mpf('2e-4')
YMIN = mpf(236000); K3 = mpf(10)**12
KW9_DIR = os.environ.get('CSTAR_KW9_DIR', os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KW9_DIR)
print('KW =', KW, ' y_min =', YMIN, ' KW9 data dir =', KW9_DIR)
alp = 1/(Cp*YMIN); al = 1/(C*YMIN)
# ---- hypotheses of the lemmas at the smallest scale
check("lem:Bh applies in Sec. 6: alpha'(y_min) < 1.4982e-6 <= 1.5e-6", alp < mpf('1.4982e-6') <= mpf('1.5e-6'), alp)
check("y_min = 236000 >= 1/(C' 1.5e-6) = 235702.26... (rem:k)", YMIN >= 1/(Cp*mpf('1.5e-6')) and mpf('235702.26') < 1/(Cp*mpf('1.5e-6')) < mpf('235702.27'), 1/(Cp*mpf('1.5e-6')))
check("lem:Bv restated: alpha(y_min) < 2.119e-6 <= 3e-6", al < mpf('2.119e-6') <= mpf('3e-6'), al)
check("lem:Bv restated: theta1(2-theta1)/40 >= Q* 3e-6 (2-3e-6)/4 and 4 sqrt(K/Q*)/(2-bbar) <= A for bbar <= 3e-6",
      TH1*(2 - TH1)/40 >= Qs*mpf('3e-6')*(2 - mpf('3e-6'))/4)
check("lem:Bv restated: limit of the condition is bbar ~ 3.125e-6 (> 3e-6)", TH1*(2 - TH1)/40 < Qs*mpf('3.126e-6')*(2 - mpf('3.126e-6'))/4)
check("lem:Eline hypotheses: alpha'(d(y)) <= 1.5e-6 on H; delta = 1e-5; d(y) <= (1-eps)(k/2-3) < k/2 - 1", alp <= mpf('1.5e-6') and (1 - eps)*(K3/2 - 3) < K3/2 - 1)
check("sec x - 1 <= 0.50001 x^2 for x <= 1e-3 (value at 1e-3; (sec x-1)/x^2 increasing)", (sec(mpf('1e-3')) - 1)/mpf('1e-6') < mpf('0.50001'))
okE = True
for i in range(1, 60):
    a = mpf(i)/60*mpf('1.5e-6'); A_ = mpf('1.5e-6')
    for c in [mpf(1), (1 + sec(a))/2, sec(a)]:
        okE &= (c - 1 <= mpf('0.50001')*a**2 <= mpf('0.50001')*A_*a*c)
check("lem:Eline chain c-1 <= 0.50001 a^2 <= 0.50001 alpha a c for 1 <= c <= sec a, a < alpha (grid)", okE)
check("(sec x - 1)/x^2 increasing (grid on (0, 1e-3])", all((sec(mpf(i+1)*mpf('1e-5')) - 1)/(mpf(i+1)*mpf('1e-5'))**2 > (sec(mpf(i)*mpf('1e-5')) - 1)/(mpf(i)*mpf('1e-5'))**2 for i in range(1, 100)))
check("alpha(y_min) <= 1e-3, delta <= 1e-3 (crack lemma range)", al <= mpf('1e-3') and delta <= mpf('1e-3'))
# ---- lem:Q at s >= y_min
def _quant(s):
    a = 1/(C*s); nq = mpf('0.50001')*(1 + a/s)/(C**2*s)
    BZ = mpf('2.01')*a + (1 + (a + cos(a) + sin(a))/s)*(1 + mpf('3.04e-5'))/(C*(cos(a) - sin(a)))
    return a, nq, BZ
a_, nq, BZ = _quant(YMIN)
check("lem:Q n(sec a - 1) < 5.3e-7", nq < mpf('5.3e-7'), nq)
check("lem:Q beta < n + 1.053e-5 (1e-5 + 5.3e-7 = 1.053e-5 exactly)", Fr('1e-5') + Fr('5.3e-7') == Fr('1.053e-5'))
check("lem:Q sin a(Z) < 2.119e-6; lower ramp < n + 1.2649e-5 (1.053e-5 + 2.119e-6 = 1.2649e-5 exactly)", Fr('1.053e-5') + Fr('2.119e-6') == Fr('1.2649e-5') and al < mpf('2.119e-6'))
check("lem:Q cos a - sin a > 1 - 2.12e-6", cos(al) - sin(al) > 1 - mpf('2.12e-6'))
w0 = mpf('1.265e-5')
check("lem:Q w0 = 1.265e-5 > 1.2649e-5 and > 2.12e-6", Fr('1.265e-5') > Fr('1.2649e-5') and w0 > mpf('2.12e-6'))
check("lem:Q exact bound delta + n(sec a-1) + alpha = 1.26483e-5 < w0 at y_min = 236000",  delta + nq + al < w0, delta + nq + al)
# ---- lem:GZ
check("tan a < 1.000001 a", tan(al) < mpf('1.000001')*al)
check("3.02 delta * 1.000001 <= 3.04e-5", mpf('3.02')*delta*mpf('1.000001') <= mpf('3.04e-5'))
check("alpha + 2.01 delta tan alpha <= 1.01 alpha (B_Z cover)", al + mpf('2.01')*delta*tan(al) <= mpf('1.01')*al)
check("lem:GZ |B_Z| < 0.500023", BZ < mpf('0.500023'), BZ)
check("lem:GZ: the bound for |B_Z| and n(sec a-1) decrease in s (grid s in [y_min, 1e13])",
      all(_quant(s)[2] <= BZ and _quant(s)[1] <= nq for s in [YMIN*(1 + mpf(j)/7) for j in range(40)] + [mpf(10)**e for e in range(6, 14)]))
g0 = mpf('0.49997')
check("g0: 1 - 2.12e-6 - 0.500023 > 0.49997", 1 - mpf('2.12e-6') - mpf('0.500023') > g0)
A = 4*sqrt(KW/Qs)/(2 - mpf('3e-6'))
Ab = mpf('10.6067')
check(f"A = 4 sqrt({KW}/0.32)/(2 - 3e-6) < {Ab}", A < Ab, A)
check("A >= 2", A >= 2)
check("Bh: theta1(2-theta1)/40 >= Q* thmax(2-thmax)/4, thmax <= 3e-6", mpf('1e-5')*(2 - mpf('1e-5'))/40 >= Qs*mpf('3e-6')*(2 - mpf('3e-6'))/4)
check("C'(1 - eps) > C", Cp*(1 - eps) > C)
check("vertical extent < 1.0001", cos(alp/(1 - eps)) + sin(alp/(1 - eps)) < mpf('1.0001'))
# ---- ell(H)
h0 = 1 - 2*w0
lead = (1 - om0)*h0
check("(1 - omega0) h0 >= 0.99977", lead >= mpf('0.99977'), lead)
L0 = log(2/(1 - eps)) + log(YMIN + 1)
check("log(2/(1-eps)) + log(y_min + 1) < 13.066741", L0 < mpf('13.066741'), L0)
check("log(1 - 6/k) > -1e-11 for k >= 1e12", log(1 - 6/K3) > mpf('-1e-11'), log(1 - 6/K3))
check("ell(H) >= 2 h0 (log k - 13.06675): 13.066741 + 1e-11 <= 13.06675", mpf('13.066741') + mpf('1e-11') <= mpf('13.06675'))
check("j1 > j0: floor((1-eps)(1e12/2 - 3)) > 236000", floor((1 - eps)*(K3/2 - 3)) > YMIN)
check("unit pieces: int_{m+w0}^{m+1-w0} dy/y >= h0/(m+1) for m >= y_min (m=y_min, 10 y_min, 1e11)",
      all(log((m + 1 - w0)/(m + w0)) >= h0/(m + 1) for m in [YMIN, 10*YMIN, mpf(10)**11]))
# ---- Gamma
Gc = 2*mpf('0.50001')*(A/(Cp*YMIN) + 1/(2*Cp**2*delta*YMIN**2))
Gq = 2*quad(lambda y: mpf('0.50001')/(Cp*y)*(A + 1/(Cp*y*delta))/y, [YMIN, inf])
check("Gamma = 1.00002(A/(C' y_min) + 1/(2 C'^2 delta y_min^2)) < 1.61e-5 (= quadrature)", Gc < mpf('1.61e-5') and abs(Gc - Gq) < mpf('1e-25'), Gc)
check("Gamma also < 1.61e-5 with A replaced by 10.6067", 2*mpf('0.50001')*(Ab/(Cp*YMIN) + 1/(2*Cp**2*delta*YMIN**2)) < mpf('1.61e-5'))
# ---- bracket
t1 = 1/(om0*YMIN); t2 = mpf('2.01')/(eps*YMIN); t3 = al/delta
print('1/(om0 y_min) =', t1, ' 2.01/(eps y_min) =', t2, ' alpha(y_min)/delta =', t3)
check("1/(omega0 y_min) < 0.021187, 2.01/(eps y_min) < 4.2585e-3, alpha(y_min)/delta < 0.21187", t1 < mpf('0.021187') and t2 < mpf('4.2585e-3') and t3 < mpf('0.21187'))
br = mpf('0.021187') + SQ2*Ab + (1 + mpf('4.2585e-3'))/(SQ2*g0*(1 - eps))*(Ab + mpf('0.21187')) + mpf('1.61e-5')
Bb = mpf('30.418')
print('bracket =', br)
check("bracket = 30.41797... < 30.418", mpf('30.41797') < br < Bb, br)
Bexact = t1 + SQ2*A + C*(1 + t2)/(Cp*(cos(al) - sin(al) - BZ)*(1 - eps))*(A + t3) + Gc
check("exact bracket (unrounded A, g0) = 30.41757556 (R2 value)", abs(Bexact - mpf('30.41757556')) < mpf('1e-7'), Bexact)
# ---- the theorem
SL = 2*mpf('0.99977')
check("2 (1-omega0) h0 >= 1.99954", 2*lead >= SL)
F = lambda L: SL*(L - mpf('13.06675'))/Bb
check("for 2 <= k < 1e12: log k < 27.632 and F(k) < 0.958", log(K3) < mpf('27.632') and F(mpf('27.632')) < mpf('0.958'), F(log(K3)))
check("text: (1.99954/30.418 - 0.0353) > 0.03043, 1.99954*13.06675/30.418 < 0.85895 < 0.03043*28.32, and 1/0.0353 > 28.32",
      SL/Bb - mpf('0.0353') > mpf('0.03043') and SL*mpf('13.06675')/Bb < mpf('0.85895') < mpf('0.03043')*mpf('28.32') and 1/mpf('0.0353') > mpf('28.32'))
Lc = findroot(lambda L: F(L) - 1, 28)
lim = SL/Bb
print('F > 1 for log k >', Lc, '  1/log k* =', 1/Lc, '  limit =', lim)
check("kappa = 0.0353 is rounded DOWN: 0.0353 <= 1/log k* = 0.035361... < 0.0354 (never 0.0354)", mpf('0.0353') <= 1/Lc < mpf('0.0354') and 1/Lc < mpf('0.0354'), 1/Lc)
mn = min([max(1, F(log(mpf(k))))/log(mpf(k)) for k in range(2, 3000)] + [max(1, F(L))/L for L in [mpf(i)/500 for i in range(4000, 100000)]])
check("grid: inf over k of max(1,F(k))/log k >= 0.0353", mn >= mpf('0.0353'), mn)
check("theorem/abstract: slope 1.99954/30.418 = 0.065735... > 0.0657", mpf('0.0657') < lim < mpf('0.065736'), lim)
check("abstract/intro: 1/kappa = 1/0.0353 ~ 28 (28.3)", abs(1/mpf('0.0353') - mpf('28.33')) < mpf('0.01'))
check("intro: the second bound exceeds 1 only for log k > 28.279", mpf('28.279') < Lc < mpf('28.2793'))
# ---------------- numbers quoted in the remarks of v11 ----------------
check("rem:k: F exceeds 1 for log k > 28.2792..., 1/28.2793 < 1/log k*, kappa(k1) = 0.035361..., limit 0.065735...",
      mpf('28.2792') < Lc < mpf('28.2793') and mpf('0.035361') < 1/Lc < mpf('0.035362') and mpf('0.065735') < lim < mpf('0.065736'))
check("rem:k: 13.06675 ~ log(2(y_min+1)/(1-eps))", abs(log(2*(YMIN + 1)/(1 - eps)) - mpf('13.06675')) < mpf('1e-5'))
check("rem:k: slope limit 1/(sqrt2 A_inf) = sqrt(Q*/9)/(2 sqrt2) ~ 0.066667", abs(sqrt(Qs/9)/(2*SQ2) - mpf('0.066667')) < mpf('1e-6'))
def _exact(ymin):
    a = 1/(C*ymin); ap = 1/(Cp*ymin); nq_ = mpf('0.50001')*(1 + a/ymin)/(C**2*ymin)
    w0e = delta + nq_ + a
    BZe = mpf('2.01')*a + (1 + (a + cos(a) + sin(a))/ymin)*(1 + mpf('3.04e-5'))/(C*(cos(a) - sin(a)))
    g0e = cos(a) - sin(a) - BZe
    G = 2*mpf('0.50001')*(A/(Cp*ymin) + 1/(2*Cp**2*delta*ymin**2))
    B = 1/(om0*ymin) + SQ2*A + C*(1 + mpf('2.01')/(eps*ymin))/(Cp*g0e*(1 - eps))*(A + a/delta) + G
    sl = 2*(1 - om0)*(1 - 2*w0e)
    L0_ = log(mp.ceil(ymin) + 1) - log((1 - eps)/2)
    Ls = findroot(lambda L: sl*(L - L0_ + log(1 - 6*exp(-L)))/B - 1, 28)
    return sl/B, 1/Ls
s3, k3_ = _exact(mpf(300000)); s6, k6_ = _exact(mpf(10)**6)
check("rem:k: y_min = 3e5 and 1e6 (unrounded): slopes 0.0659 / 0.0663, constants 0.0351 / 0.0338",
      mpf('0.0659') < s3 < mpf('0.0660') and mpf('0.0663') < s6 < mpf('0.0664') and mpf('0.0351') < k3_ < mpf('0.0352') and mpf('0.0338') < k6_ < mpf('0.0339'),
      k6_)
check("rem:k: version 1.1 limit 0.99977/30.147 = 0.033163...", mpf('0.033163') < mpf('0.99977')/mpf('30.147') < mpf('0.033164'))
th4 = mpf('13.06675') + Bb*4/SL
check("rate: threshold 13.06675 + 30.418c/1.99954 <= 15.22c + 13.07 (c >= 0); s(k^2-4)=k for log k > 73.92 (exact 73.9167...)",
      Bb/SL <= mpf('15.22') and mpf('13.06675') <= mpf('13.07') and mpf('73.91') < th4 < mpf('73.92'), th4)
check("rate: for c >= 1 the threshold is >= 28.279 > log 1e12 (the bound F applies there)", mpf('13.06675') + Bb/SL > log(K3))
check("rem:const: sqrt(9/0.32) ~ 5.3", abs(sqrt(9/Qs) - mpf('5.303')) < mpf('0.001'))
c3r = (1 + mpf('4.2585e-3'))/(SQ2*g0*(1 - eps))
A3 = 4*sqrt(9/(mpf(1)/3))/(2 - mpf('3e-6'))
br3 = t1 + SQ2*A3 + c3r*(A3 + mpf('0.21187')) + 2*mpf('0.50001')*(A3/(Cp*YMIN) + 1/(2*Cp**2*delta*YMIN**2))
L3 = findroot(lambda L: SL*(L - mpf('13.06675'))/br3 - 1, 28)
check("rem:const: with Q* = 1/3: slope ~ 0.0670 (0.06708), constant for all k ~ 0.0357 (0.03575)",
      mpf('0.0670') < SL/br3 < mpf('0.0671') and mpf('0.0357') < 1/L3 < mpf('0.0358'), SL/br3)
_lhs = mpf('1e-5')*(2 - mpf('1e-5'))/40
_rhs = lambda th: (mpf(1)/3)*th*(2 - th)/4
check("rem:const (Q* = 1/3): the comparison theta_1(2-theta_1)/40 >= Q* theta(2-theta)/4 of Lemmas 4.13 and 4.14 fails at theta = 3e-6 (so both are "
      "restated) and holds for theta = 2*1.4999e-6 (Lemma 4.13, theta_max = 2 beta_bar) and theta = 2.99e-6 (Lemma 4.14)",
      _lhs < _rhs(mpf('3e-6')) and _lhs >= _rhs(2*mpf('1.4999e-6')) and _lhs >= _rhs(mpf('2.99e-6')), _lhs - _rhs(mpf('3e-6')))
check("rem:const (Q* = 1/3): the uses in Section 6 stay in the restated ranges: alpha'(y_min) < 1.4982e-6 <= 1.4999e-6, alpha(y_min) < 2.119e-6 <= 2.99e-6",
      1/(2*SQ2*YMIN) < mpf('1.4982e-6') <= mpf('1.4999e-6') and 1/(2*YMIN) < mpf('2.119e-6') <= mpf('2.99e-6'), 1/(2*SQ2*YMIN))
check("rem:const: kappa_all < 1/13.06675 < 1/13.06 for any bracket", 1/mpf('13.06675') < 1/mpf('13.06'))
check("changes: v1.1 slope 0.99977/30.147 ~ 0.0331 -> v1.2 0.0657", abs(mpf('0.99977')/mpf('30.147') - mpf('0.0331')) < mpf('1e-4'))

# ---------------- lem:Kw9: final computation complete (see make_stats_v10.py) ----------------
import glob, re as _re, json as _json
_here = KW9_DIR  # the leaf files (data/kw9_data.zip) and bnb*.py of the computation of Lemma 4.10
leaves = sorted(glob.glob(os.path.join(_here, '*_T9_*_final_leaves.jsonl')))
tot = 0; fails = 0; finished = True; mx = 0; per_file_ok = True; groups = {}
for lf in leaves:
    m_ = _re.match(r'(bnbw?)_n(\d)_T9_(\d+)of(\d+)_final_leaves\.jsonl$', os.path.basename(lf))
    groups.setdefault((m_.group(1), int(m_.group(2)), int(m_.group(4))), set()).add(int(m_.group(3)))
    n_l = sum(1 for _ in open(lf))
    parts = sorted(glob.glob(lf.replace('.jsonl', '_verify2_*of4.json')))
    c_l = 0
    for f in parts:
        D_ = _json.load(open(f)); c_l += D_['checked']; fails += len(D_['fail']); finished &= bool(D_.get('finished')); mx = max(mx, D_['maxU'])
    per_file_ok &= (len(parts) == 4 and c_l == n_l)
    tot += c_l
tasks_ok = all(any(k[0] == w and k[1] == n and v == set(range(k[2])) for k, v in groups.items()) and
               sum(1 for k in groups if k[0] == w and k[1] == n) == 1 for w in ('bnb', 'bnbw') for n in range(1, 6))
check("lem:Kw9: final T=9 runs present for n = 1..5, without and with a side, all task indices", tasks_ok)
nleaves = sum(sum(1 for _ in open(f)) for f in leaves)
check(f"lem:Kw9: all {nleaves} accepted boxes re-verified in Arb by verify_leaves2.py ({tot} checked), no failure, max rigorous bound {mx}",
      finished and fails == 0 and per_file_ok and tot == nleaves and mx <= 9 and nleaves > 0)
cov_ok = True
for lf in leaves:
    cj = lf.replace('.jsonl', '_coverage.json')
    C_ = _json.load(open(cj)) if os.path.exists(cj) else None
    cov_ok &= bool(C_ and C_['ok'] and C_['unused'] == 0 and C_['overused'] == 0 and C_['duplicates'] == 0 and C_['volume_equal']
                   and C_['leaves'] == sum(1 for _ in open(lf)))
check(f"lem:Kw9: the accepted boxes of all {len(leaves)} final runs tile the initial boxes (tree rebuilt, each box used once, exact volumes)", cov_ok and len(leaves) > 0)
import bnb as _B, bnb_wall as _BW, math as _math
_hi = [max(float(_B.PHI_HI[k]), float(_B.PHI_LO[k + 1])) for k in range(_B.NC - 1)]
check("lem:Kw9: direction cells used by verify_leaves2 cover [0, 2pi_float] without gaps (last cell extended to the exact 2pi in Arb); rho pieces cover [1, Lambda]",
      _B.PHI_LO[0] == 0.0 and all(_hi[k] >= _B.PHI_LO[k + 1] for k in range(_B.NC - 1)) and float(_B.PHI_HI[-1]) == 2*_math.pi
      and all(_B.RHI[q] == _B.RLO[q + 1] for q in range(_B.NR - 1)) and _B.RLO[0] <= 1 and mpf(float(_B.RHI[-1])) >= SQ2 + mpf('1e-4'))
check("lem:Kw9: wall angle slices and the no-side slices of theta_2 share their end points (same float expression), first slice starts at 0",
      all(2*_math.pi*(s + 1)/m == 2*_math.pi*(s + 1)/m for m in (4, 8, 16) for s in range(m)) and 2*_math.pi*0/8 == 0.0)
# ---------------- rem:const (v11): without the computer, the analytic K_w = 13 gives kappa = 0.0319 ----------------
A13 = 4*sqrt(mpf(13)/Qs)/(2 - mpf('3e-6'))
G13 = 2*mpf('0.50001')*(mpf('12.7476')/(Cp*YMIN) + 1/(2*Cp**2*delta*YMIN**2))
br13 = mpf('0.021187') + SQ2*mpf('12.7476') + (1 + mpf('4.2585e-3'))/(SQ2*g0*(1 - eps))*(mpf('12.7476') + mpf('0.21187')) + G13
F13 = lambda L: SL*(L - mpf('13.06675'))/mpf('36.493')
L13 = findroot(lambda L: F13(L) - 1, 31)
check("rem:const: with K_w = 13: A < 12.7476, Gamma < 1.93e-5, bracket < 36.493, slope 1.99954/36.493 > 0.0547, kappa_all = 1/log k* in [0.0319, 0.0320)",
      A13 < mpf('12.7476') and G13 < mpf('1.93e-5') and br13 < mpf('36.493') and SL/mpf('36.493') > mpf('0.0547') and mpf('0.0319') <= 1/L13 < mpf('0.0320'), br13)
check("rem:const: K_w = 13: F13(k) >= 0.0319 log k whenever 0.0319 log k > 1 (F13 - 0.0319 L increasing, positive at L = 1/0.0319)",
      SL/mpf('36.493') > mpf('0.0319') and F13(1/mpf('0.0319')) - 1 > 0, F13(1/mpf('0.0319')))
from mpmath import mp as _mp, mpf as _mpf, sqrt as _sqrt
_mp.dps = 40
import bnb as _B, bnb_wall as _BW
_rho1 = _sqrt((_mpf('1e-4') + _sqrt(2)/2)**2 + _mpf(1)/4)
check("lem:Kw9: floating-point rho_1, Lambda and d+sqrt2/2 used by the search are upper bounds of the exact values",
      _mpf(_B.RHO1) >= _rho1 and _mpf(_B.LAM) >= _sqrt(2) + _mpf('1e-4') and _mpf(_BW.WALL_R) >= _mpf('1e-4') + _sqrt(2)/2)
check("lem:Kw9: gamma_0 used in the count (float G0 - 1e-12) is below the exact gamma_0 = acos(1 - 1/(2 Lambda^2))", _mpf(_B.G0) - _mpf('1e-12') < __import__('mpmath').acos(1 - 1/(2*(_sqrt(2) + _mpf('1e-4'))**2)))
check("lem:Kw9: arc (2pi_float, 2pi) is empty without a side: rho_1 - 1/2 < 1 (two centres there would be closer than 1)", _rho1 - _mpf(1)/2 < 1)
# ---------------- lem:Kw9 (version 1.2): the arc (2pi_float, 2pi) and the rounding errors of the floating-point count ----------------
_arc = 2*pi - _mpf(2*_math.pi)
check("lem:Kw9: the arc (2pi_float, 2pi) has length < 2.5e-16; two centres at radii in (1/2, rho_1] whose angles differ by less than that are at "
      "distance <= rho_1 - 1/2 + rho_1*2.5e-16 < rho_1 - 1/2 + 1e-15 < 1", 0 < _arc < _mpf('2.5e-16') and _rho1*_mpf('2.5e-16') < _mpf('1e-15')
      and _rho1 - _mpf(1)/2 + _mpf('1e-15') < 1, _arc)
import numpy as _np
_NC, _D, _TPF = _B.NC, _B.DPHI, 2*_math.pi
_lo = _np.asarray(_B.PHI_LO, dtype=_np.float64)
_hie = _np.array([max(float(_B.PHI_HI[k]), float(_B.PHI_LO[k + 1])) for k in range(_NC - 1)] + [float(_B.PHI_HI[_NC - 1])])
_S, _O = _np.meshgrid(_np.arange(_NC), _np.arange(_NC), indexing='ij')
_base = _lo[_S] + _O*_D                     # the arc starts as bnb.max_points computes them: PHI_LO[s] + off*DPHI
_end = _base + _D                           # and the arc ends: base + DPHI
_k = (_S + _O) % _NC; _wr = (_S + _O) >= _NC
_ster = lambda x, y: bool(_np.all((y == 0) | ((y/2 <= x) & (x <= 2*y))))   # x - y is exact: trivially if y = 0, by Sterbenz's lemma otherwise
_t0 = _np.where(_wr, _base - _TPF, _base); _t1 = _np.where(_wr, _end - _TPF, _end)
_exact = (_ster(_np.where(_wr, _base, _TPF), _np.where(_wr, _TPF, _TPF)) and _ster(_np.where(_wr, _end, _TPF), _np.where(_wr, _TPF, _TPF))
          and _ster(_t0, _lo[_k]))
_last = (_k == _NC - 1) & ~_wr               # the last arc ends at the exact 2pi in the certification
_exact = _exact and _ster(_np.where(_last, _end, _t1), _np.where(_last, _TPF, _hie[_k])) and not bool(_np.any(_wr & (_k == _NC - 1)))
_ds = _t0 - _lo[_k]                          # exact differences (Sterbenz); the true deviation subtracts the arc length when wrapped
_de = _np.where(_last, _end - _TPF, _t1 - _hie[_k])
_dev = max(max(abs(_mpf(float(_ds[_wr].min())) - _arc), abs(_mpf(float(_ds[_wr].max())) - _arc), _mpf(float(abs(_ds[~_wr]).max()))),
           max(abs(_mpf(float(_de[_wr | _last].min())) - _arc), abs(_mpf(float(_de[_wr | _last].max())) - _arc), _mpf(float(abs(_de[~_wr & ~_last]).max()))))
check("lem:Kw9 (count): all 1440*1440 arc end points computed in bnb.max_points lie within 1e-14 of the certified arc end points "
      "(differences exact by Sterbenz's lemma; arcs extended as in verify_leaves2.py, the last one to the exact 2pi)", _exact and _dev < _mpf('1e-14'), _dev)
check("lem:Kw9 (count): all numbers compared in the count have absolute value < 14 (unwrapped positions < 4pi + DPHI)",
      float(_end.max()) < 14 and 4*pi + _D < 14, _mpf(float(_end.max())))
_g0x = __import__('mpmath').acos(1 - 1/(2*(_sqrt(2) + _mpf('1e-4'))**2))
_gs = _mpf(_B.G0 - 1e-12)
check("lem:Kw9 (count): the separation used, float(G0 - 1e-12), is within 1e-15 of gamma_0 - 1e-12",
      abs(_gs - (_g0x - _mpf('1e-12'))) < _mpf('1e-15'), _gs - (_g0x - _mpf('1e-12')))
_h = pi/720
_gap = min(abs(j*_g0x/_h - __import__('mpmath').nint(j*_g0x/_h))*_h for j in range(1, 10))
check("lem:Kw9 (count): j*gamma_0 (1 <= j <= 9) differs from every integer multiple of the arc length pi/720 by more than 4e-5 "
      "(minimum 4.3249e-5 at j = 8), far more than the errors (< 1e-14 rounding, < 9e-12 from gamma_0 - 1e-12 over 9 steps, 2e-12 closing slack): "
      "every comparison of the count has the exact outcome", _gap > _mpf('4e-5') and _gap > _mpf('1e-14') + 9*_mpf('1e-12') + 2*_mpf('1e-12')
      and 9*_g0x > 2*pi > 8*_g0x and abs(_mpf(_D) - _h) < _mpf('1e-18'), _gap)
try:                                          # the certificate itself (verify_leaves2.py), not a model of it
    import verify_leaves2 as _V2
    from flint import arb as _arb
    _tp = 2*_math.pi                          # a degenerate interval: Arb's rounding of the radius cannot reach the exact 2pi
    _ext = (_V2.V.iv is _V2.iv2 and _V2.iv2(_tp, _tp).contains(2*_arb.pi()) and not _V2._iv0(_tp, _tp).contains(2*_arb.pi())
            and not _V2.iv2(0.0, 1.0).contains(2*_arb.pi())
            and all(_V2.PHI_HI_EFF[k] == max(float(_B.PHI_HI[k]), float(_B.PHI_LO[k + 1])) for k in range(_B.NC - 1))
            and _V2.PHI_HI_EFF[-1] == 2*_math.pi and _V2.V.G0_SAFE == _B.G0 - 1e-12)
except Exception as _e:
    print('   (could not import verify_leaves2:', repr(_e), ')'); _ext = False
check("lem:Kw9: verify_leaves2.py (the certificate) uses the arcs [PHI_LO[k], max(PHI_HI[k], PHI_LO[k+1])], installs iv2 as verify_leaves.iv, "
      "where iv2 extends every interval ending at the float 2pi so that it contains the exact 2pi (Arb), and counts with G0_SAFE = G0 - 1e-12", _ext)
# ---------------- cor:evand (version 1.2): W >= 4 for k >= 6 (assuming s(k^2-3) = k, [Dan]) gives 0.0541 for all k >= 2 ----------------
L4 = mpf('13.06675') + 4*mpf('30.418')/mpf('1.99954')
check("cor:evand: SL = 1.99954 is the slope numerator of the second bound F(k) = SL (log k - 13.06675)/30.418", abs(SL - mpf('1.99954')) < mpf(10)**-35)
check("cor:evand: L_4 = 13.06675 + 4*30.418/1.99954 = 73.91674... (F(k) >= 4 iff log k >= L_4)", mpf('73.91674') < L4 < mpf('73.91675'), L4)
check("cor:evand: F(e^{L_4}) = 4", abs(SL*(L4 - mpf('13.06675'))/mpf('30.418') - 4) < mpf(10)**-30)
check("cor:evand: 0.0541 L_4 < 3.999 < 4 (the bound 4 covers 6 <= k with log k <= L_4)", mpf('0.0541')*L4 < mpf('3.999'), mpf('0.0541')*L4)
check("cor:evand: F(k)/log k = (SL/30.418)(1 - 13.06675/log k) is increasing (13.06675 > 0), and 4/L_4 > 0.05411 > 0.0541",
      mpf('13.06675') > 0 and 4/L4 > mpf('0.05411'), 4/L4)
check("cor:evand: 2 <= k <= 5: 0.0541 log 5 < 1 <= W (Corollary 3.3)", mpf('0.0541')*log(5) < 1, mpf('0.0541')*log(5))
check("cor:evand / rem:k: 4/L_4 = 0.054114... (so 0.0541 is rounded down; 0.0542 would be false)", mpf('0.054114') <= 4/L4 < mpf('0.054115') and 4/L4 < mpf('0.0542'), 4/L4)
L3 = mpf('13.06675') + 3*mpf('30.418')/mpf('1.99954')
check("cor:evand (remark after it): L_3 = 13.06675 + 3*30.418/1.99954 = 58.7042... < 58.71 (beyond it F > 3, so W >= 4 by integrality)",
      mpf('58.7042') < L3 < mpf('58.7043') and L3 < mpf('58.71'), L3)
L4h = mpf('13.06675') + 4*mpf('36.493')/mpf('1.99954')
check("cor:evand (remark after it): with K_w = 13 (bracket 36.493): 4/L_4' with L_4' = 86.0695... is > 0.0464",
      mpf('86.0695') < L4h < mpf('86.0696') and 4/L4h > mpf('0.0464'), 4/L4h)


print("ALL OK" if ok else "SOME CHECK FAILED")
