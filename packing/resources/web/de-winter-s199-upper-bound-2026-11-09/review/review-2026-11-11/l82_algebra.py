"""Exact checks of the two quintics (A1-A4) by a Sturm sequence of my own, cross-checked
with sympy's exact root counting and factorisation.

Usage: python -I l82_algebra.py N199_JSON N172_JSON OUT.json
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F

import sympy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l82_check as C  # noqa: E402

P946 = [62, -4116, 107933, -1397031, 8918035, -22427977]
P939 = [62, -4426, 125017, -1746146, 12052670, -32855154]


def ev(p, x):
    acc = F(0)
    for c in p:
        acc = acc * x + c
    return acc


def pdiv_rem(a, b):
    a = [F(c) for c in a]
    while len(a) >= len(b) and a:
        f = a[0] / b[0]
        for k in range(len(b)):
            a[k] -= f * b[k]
        a.pop(0)
    while a and a[0] == 0:
        a.pop(0)
    return a


def deriv(p):
    d = len(p) - 1
    return [c * (d - k) for k, c in enumerate(p[:-1])]


def sturm(p):
    seq = [[F(c) for c in p], [F(c) for c in deriv(p)]]
    while True:
        r = pdiv_rem(seq[-2], seq[-1])
        if not r:
            break
        seq.append([-c for c in r])
    return seq


def var(seq, x):
    signs = [ev(q, x) for q in seq]
    signs = [v for v in signs if v != 0]
    return sum(1 for a, b in zip(signs, signs[1:]) if (a > 0) != (b > 0))


def var_inf(seq, sgn):
    signs = []
    for q in seq:
        d = len(q) - 1
        s = q[0] if sgn > 0 or d % 2 == 0 else -q[0]
        signs.append(s)
    return sum(1 for a, b in zip(signs, signs[1:]) if (a > 0) != (b > 0))


def count(seq, a, b):
    return var(seq, a) - var(seq, b)


def taylor_shift(p, h):
    x = sympy.Symbol("x")
    poly = sum(c * x ** (len(p) - 1 - k) for k, c in enumerate(p))
    return [int(c) for c in sympy.Poly(sympy.expand(poly.subs(x, x + h)), x).all_coeffs()]


def bisect_root(p, lo, hi, width):
    flo = ev(p, lo)
    while hi - lo > width:
        mid = (lo + hi) / 2
        fm = ev(p, mid)
        if fm == 0:
            return mid, mid
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return lo, hi


x = sympy.Symbol("x")
n199 = C.read_author_json(sys.argv[1])
n172 = C.read_author_json(sys.argv[2])
cases = {
    "939": (P939, F(*n199["side"]), F(1, 10**98), F(1, 10**125)),
    "946": (P946, F(*n172["side"]), F(1, 10**318), F(1, 10**345)),
}
out: dict = {}
out["A4_p939_is_p946_shifted"] = taylor_shift(P946, -1) == P939
for key, (p, S, tol, width) in cases.items():
    r: dict = {}
    sq = sturm(p)
    r["sturm_length"] = len(sq)
    r["real_roots_total"] = var_inf(sq, -1) - var_inf(sq, 1)
    sp = sympy.Poly(p, x)
    r["sympy_real_roots_total"] = int(sp.count_roots())
    r["content"] = int(sympy.gcd_list(p))
    fl = sympy.factor_list(sp)
    r["sympy_factor_list"] = str(fl)
    r["irreducible_over_Q_sympy"] = len(fl[1]) == 1 and fl[1][0][1] == 1 and sympy.Poly(fl[1][0][0], x).degree() == 5
    mod_cert = None
    for prime in sympy.primerange(3, 200):
        if 62 % prime == 0:
            continue
        if sympy.Poly(p, x, modulus=prime).is_irreducible:
            mod_cert = prime
            break
    r["irreducible_mod_prime"] = mod_cert
    r["discriminant_nonzero"] = sympy.discriminant(sp) != 0
    r["A_in_stated_interval"] = count(sq, S - tol, S)
    r["A_above_side_same_width"] = count(sq, S, S + tol)
    r["sympy_count_in_interval"] = int(sp.count_roots(S - tol, S))
    r["sign_at_side"] = 1 if ev(p, S) > 0 else -1
    r["sign_at_side_minus_tol"] = 1 if ev(p, S - tol) > 0 else -1
    lo, hi = bisect_root(p, S - tol, S, width)
    r["side_minus_root_between"] = [C.sci(S - hi, 6), C.sci(S - lo, 6)]
    r["root_floor_60"] = C.decimal_floor(lo, 60)
    r["root_ceil_12"] = C.decimal_ceil(hi, 12)
    r["side_ceil_12"] = C.decimal_ceil(S, 12)
    pm = list(p)
    pm[-1] -= 1
    r["A3_perturbed_in_interval"] = count(sturm(pm), S - tol, S)
    # the root near 13.6/14.6 isolated on a unit interval too
    r["roots_in_unit_window"] = count(sq, S - F(1, 2), S + F(1, 2))
    out[key] = r
    out[key + "_root_bracket"] = [f"{lo.numerator}/{lo.denominator}", f"{hi.numerator}/{hi.denominator}"]
ok = out["A4_p939_is_p946_shifted"]
for key in cases:
    r = out[key]
    ok = ok and r["A_in_stated_interval"] == 1 == r["sympy_count_in_interval"] and r["A_above_side_same_width"] == 0
    ok = ok and r["A3_perturbed_in_interval"] == 0 and r["irreducible_over_Q_sympy"] and r["irreducible_mod_prime"]
out["A_controls_as_stated"] = bool(ok)
with open(sys.argv[3], "w") as fh:
    json.dump(out, fh, indent=1)
    fh.write("\n")
print(json.dumps({k: v for k, v in out.items() if not k.endswith("bracket")}, indent=1))
