#!/usr/bin/env python3
"""Rational certificate for any feasible f64 packing (no jamming / local-minimality needed), by dilation (10-10).

Centres and box are scaled by (1 + delta) about the origin, squares keep unit size: every pair gap and wall gap grows by
about delta * (centre distance) >= delta / 2, which absorbs f64 overlaps up to ~delta / 4.  Coordinates are then rounded to
rationals with denominator 10^digits and each angle to a rational half-angle tangent t (so cos, sin are exact rationals
and the square is exactly unit).  The result is a certificate in verify_cert.py's format: check it with verify_cert.py and
verify_cert2.py.  The side bound is S (1 + delta) rounded up.

  dilate_cert.py in.txt out.cert [--delta 1e-12] [--digits 30]
"""
import argparse, math, sys
from fractions import Fraction as Fr

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('inp'); ap.add_argument('out')
ap.add_argument('--delta', type=float, default=1e-12); ap.add_argument('--digits', type=int, default=30)
a = ap.parse_args()

rows = [l.split() for l in open(a.inp) if l.strip() and not l.startswith('#')]
n, S = int(rows[0][0]), Fr(rows[0][1])
D = 10 ** a.digits
f = 1 + Fr(a.delta)


def rnd(v):
    return Fr(round(v * D), D)


lines = []
for r in rows[1:n + 1]:
    x, y, deg = Fr(r[0]), Fr(r[1]), float(r[2])
    th = math.radians(deg % 90.0)
    t = Fr(math.tan(th / 2)).limit_denominator(10 ** 15)   # exact rational tangent; angle error ~1e-16 rad
    lines.append(f'{rnd(x * f)} {rnd(y * f)} {t}')
S2 = Fr(math.ceil(S * f * D), D)
with open(a.out, 'w') as fo:
    fo.write(f'# dilation certificate (dilate_cert.py, delta {a.delta:g}) of {a.inp}; check with verify_cert.py\n')
    fo.write(f'{n} {S2}\n' + '\n'.join(lines) + '\n')
print(f'{a.out}: n = {n}, S = {float(S):.15f} -> S\' = {float(S2):.15f} (+{float(S2 - S):.2e})')
