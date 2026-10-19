"""Own check of the upper bound s(17) <= L: the seventeen squares of UPPER_FORMULAS.md at the algebraic root (t*, b*)
of F = G = 0 lie in [0, side]^2 with side = (6+4t)/(1+2t-t^2) and have pairwise disjoint interiors.
Strict inequalities are proved by interval arithmetic over the Krawczyk enclosure of root_box.py; equalities
(flush walls, tangencies) by ideal membership: the numerator of the exact expression reduces to 0 modulo a
Groebner basis of (F, G), and its denominator is bounded away from 0 on the enclosure.
Usage: python3 -I upper_at_L_check.py
"""
import sys
import os
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from root_box import enclosure, I, F as Fpoly, G as Gpoly  # noqa: E402
import sympy as sp  # noqa: E402

fails = []


def check(cond, text):
    print(("OK   " if cond else "FAIL ") + text)
    if not cond:
        fails.append(text)


def idiv(a, b):
    a = a if isinstance(a, I) else I(a)
    b = b if isinstance(b, I) else I(b)
    assert b.lo > 0 or b.hi < 0, "interval division by an interval containing 0"
    inv = I(1 / b.hi, 1 / b.lo)
    return a * inv


I.__truediv__ = idiv
I.__rtruediv__ = lambda s, o: idiv(I(o), s)


def layout(t, b, half):
    """UPPER_FORMULAS.md, transcribed; works over any field-like type (Fraction, interval, sympy)."""
    d_t, d_b = 1 + t * t, 1 + b * b
    c, s = (1 - t * t) / d_t, 2 * t / d_t
    d, e = (1 - b * b) / d_b, 2 * b / d_b
    k_denom = 1 + 2 * t - t * t
    side = (6 + 4 * t) / k_denom
    h = (c + s) / 2
    x = half + (2 + c * s + 3 * s - s * side) / c
    y = 3 * half + (2 + 3 * c - c * side) / s
    aa = d * (x + half) - e * (side - 1) + half
    bb = (d + e) * (side - 1) - half
    u10, v10 = 3 * half + c * s + 2 * s, c * (side - 1) - s - half
    u11, v11 = c + 2 * s + half, 2 * c + (c * c - s * s) / 2 - 1
    u12, v12 = u11 + 1, v10 - 1
    u13 = 2 * c + s + half
    u14, v14 = u13 + 1, v10 - 2
    r, hh = side - 3 * half, v11 - 1
    slack = c * (c + 4 - side)
    lambda6, lambda13 = r - slack / (3 * s), hh - slack / 3

    def rotate(uu, vv):
        return (c * uu - s * vv, s * uu + c * vv)

    ax = ((1, 0), (c, s), (d, -e))  # axis-parallel, theta, beta
    sq = [
        ((half, half), 0), ((3 * half, half), 0), ((half, 3 * half), 0), ((half, side - half), 0),
        ((side - half, half), 0), ((lambda6, half), 0), ((side - half, 3 * half), 0), ((side - half, side - half), 0),
        ((h, 2 + h), 1), (rotate(u10, v10), 1), (rotate(u11, v11), 1), (rotate(u12, v12), 1),
        (rotate(u13, lambda13), 1), (rotate(u14, v14), 1), ((x, side - half), 0),
        ((d * aa + e * bb, -e * aa + d * bb), 2), ((side - half, y), 0),
    ]
    out = []
    for (cx, cy), k in sq:
        a = ax[k]
        out.append(((cx, cy), (a[0], a[1]), (-a[1], a[0])))
    return side, out, {"c": c, "s": s, "slack": slack, "d_t": d_t, "d_b": d_b, "k_denom": k_denom}


def corners(sq, half):
    (cx, cy), a, bv = sq
    return [(cx + e1 * a[0] * half + e2 * bv[0] * half, cy + e1 * a[1] * half + e2 * bv[1] * half) for e1 in (1, -1) for e2 in (1, -1)]


# ---------------------------------------------------------------- interval evaluation over the enclosure
(tl, th), (bl, bh), (Llo, Lhi) = enclosure(steps=2)
T, B = I(tl, th), I(bl, bh)
HALF = I(Fr(1, 2))
side_i, sq_i, aux_i = layout(T, B, HALF)
check(side_i.lo <= Lhi and side_i.hi >= Llo and side_i.hi - side_i.lo < Fr(1, 10**50), "side = (6+4t)/(1+2t-t^2) agrees with the enclosure of L (overlapping enclosures of width < 1e-50)")


def dec(x, places=30):
    """decimal string of a Fraction, truncated"""
    neg = x < 0
    x = abs(x)
    ip = int(x)
    fp = int((x - ip) * 10**places)
    return ("-" if neg else "") + str(ip) + "." + str(fp).rjust(places, "0")

check(aux_i["s"].lo > 0 and aux_i["c"].lo > 0 and aux_i["slack"].lo > 0, "s > 0, c > 0, slack > 0 on the enclosure (the divisors of the formulas)")
print("   side in [%s, %s]" % (dec(side_i.lo), dec(side_i.hi)))
# unit directions
ok = True
for (cx, cy), a, bv in sq_i:
    n2 = a[0] * a[0] + a[1] * a[1]
    n2 = n2 if isinstance(n2, I) else I(n2)
    ok &= n2.lo <= 1 <= n2.hi
check(ok, "every direction has |a|^2 enclosing 1 (exactly 1 by the rational parametrization)")

# ---------------------------------------------------------------- exact algebra
t, b = sp.symbols("t b")

# F and G as sympy polynomials (same polynomials as root_box.py)
F_sym = t - 3*t**2 - t**3 - t**4 + (1 - t - t**4 + t**5)*b + (-3*t + t**2 - t**3 - t**4)*b**2
G_sym = (-2*t**3 - 2*t**4 + (-1 + 3*t - 4*t**2 + t**4 + t**5)*b + (4 - 2*t - 2*t**2 + 2*t**3 - 2*t**4)*b**2
         + (-1 - 5*t + 4*t**2 + t**4 + t**5)*b**3 + (2*t + 2*t**2)*b**4)
GB = sp.groebner([sp.expand(F_sym), sp.expand(G_sym)], t, b, order="lex")
print("   Groebner basis of (F, G) in lex(t > b): %d elements, degrees %s" % (len(GB.exprs), [sp.Poly(g, t, b).total_degree() for g in GB.exprs]))
side_s, sq_s, aux_s = layout(t, b, sp.Rational(1, 2))


def is_zero_at_root(expr):
    """expr (a rational function of t, b) vanishes at (t*, b*): numerator in (F, G), denominator nonzero on the enclosure."""
    num, den = sp.fraction(sp.together(sp.expand(expr)))
    rem = GB.reduce(sp.expand(num))[1]
    if rem != 0:
        return False
    den_i = eval_interval(den)
    return den_i.lo > 0 or den_i.hi < 0


def eval_interval(expr):
    """evaluate a polynomial in t, b over the enclosure by Horner-free interval arithmetic on its monomials"""
    P = sp.Poly(sp.expand(expr), t, b)
    acc = I(0)
    for (i, j), cf in P.terms():
        acc = acc + I(Fr(int(cf.p), int(cf.q))) * (T ** i) * (B ** j)
    return acc


# wall clearances: 17 squares x 4 walls, each the minimum over the 4 corners
flush, strict, bad = 0, 0, 0
for n, (sqi, sqs) in enumerate(zip(sq_i, sq_s), 1):
    ci_list, cs_list = corners(sqi, HALF), corners(sqs, sp.Rational(1, 2))
    for wall in range(4):
        vals_i = [(c[0], c[1], side_i - c[0], side_i - c[1])[wall] for c in ci_list]
        vals_s = [(c[0], c[1], side_s - c[0], side_s - c[1])[wall] for c in cs_list]
        if all(v.lo > 0 for v in vals_i):
            strict += 1
            continue
        if any(v.hi < 0 for v in vals_i):
            bad += 1
            print("   wall violation at square %d wall %d" % (n, wall))
            continue
        zeros = 0
        for v_i, v_s in zip(vals_i, vals_s):
            if v_i.lo > 0:
                continue
            if is_zero_at_root(v_s):
                zeros += 1
            else:
                bad += 1
                print("   undecided wall clearance at square %d wall %d: [%g, %g]" % (n, wall, float(v_i.lo), float(v_i.hi)))
        if zeros:
            flush += 1
check(bad == 0, "all 68 square-wall clearances are >= 0: %d strict (interval), %d identity contacts (ideal membership)" % (strict, flush))


def option_holds(qi_i, qi_s, n_i, n_s, corners_i, corners_s):
    """n.(corner - q_i) - 1/2 >= 0 for every corner of j: each > 0 by interval or exactly 0."""
    tangent = 0
    for c_i, c_s in zip(corners_i, corners_s):
        val_i = n_i[0] * (c_i[0] - qi_i[0]) + n_i[1] * (c_i[1] - qi_i[1]) - HALF
        if val_i.lo > 0:
            continue
        if val_i.hi < 0:
            return None
        val_s = n_s[0] * (c_s[0] - qi_s[0]) + n_s[1] * (c_s[1] - qi_s[1]) - sp.Rational(1, 2)
        if is_zero_at_root(val_s):
            tangent += 1
        else:
            return None
    return tangent


sep_strict, sep_tangent, sep_bad = 0, 0, 0
tangent_pairs = []


def option_status(qi_i, qi_s, n_i, n_s, corners_i, corners_s):
    """'strict' if every corner value is > 0 by interval; 'tangent' if the option holds with some corner value
    exactly 0 (ideal membership); None if the option fails or is undecided."""
    status = "strict"
    for c_i, c_s in zip(corners_i, corners_s):
        val_i = n_i[0] * (c_i[0] - qi_i[0]) + n_i[1] * (c_i[1] - qi_i[1]) - HALF
        if val_i.lo > 0:
            continue
        if val_i.hi < 0:
            return None
        val_s = n_s[0] * (c_s[0] - qi_s[0]) + n_s[1] * (c_s[1] - qi_s[1]) - sp.Rational(1, 2)
        if is_zero_at_root(val_s):
            status = "tangent"
        else:
            return None
    return status


for i in range(17):
    for j in range(i + 1, 17):
        statuses = []
        for (o, tt) in ((i, j), (j, i)):
            qo_i, a_i, b_i = sq_i[o]
            qo_s, a_s, b_s = sq_s[o]
            co_i, co_s = corners(sq_i[tt], HALF), corners(sq_s[tt], sp.Rational(1, 2))
            for n_i, n_s in ((a_i, a_s), ((-a_i[0], -a_i[1]), (-a_s[0], -a_s[1])), (b_i, b_s), ((-b_i[0], -b_i[1]), (-b_s[0], -b_s[1]))):
                # interval test first; the exact test only when the option is not decided by intervals
                vals = [n_i[0] * (c[0] - qo_i[0]) + n_i[1] * (c[1] - qo_i[1]) - HALF for c in co_i]
                if all(v.lo > 0 for v in vals):
                    statuses.append("strict")
                elif any(v.hi < 0 for v in vals):
                    continue
                else:
                    r = option_status(qo_i, qo_s, n_i, n_s, co_i, co_s)
                    if r is not None:
                        statuses.append(r)
        if not statuses:
            sep_bad += 1
            print("   pair (%d, %d): no option established" % (i + 1, j + 1))
        elif "strict" in statuses:
            sep_strict += 1
        else:
            sep_tangent += 1
            tangent_pairs.append((i + 1, j + 1))
check(sep_bad == 0, "all 136 pairs satisfy some option (interiors disjoint): %d strictly separated by some axis, %d touching (every holding option has a zero corner)" % (sep_strict, sep_tangent))
print("   tangent pairs (construction labels):", tangent_pairs)
print()
print("FAILURES:", len(fails))
for f in fails:
    print("  -", f)
