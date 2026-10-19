#!/usr/bin/env python3
"""Compute the certified lower bound a(N) of README.md / SPEC.md §1.1.

Usage (from problems/closed-form):

    python3 a_of_n.py 50                 # one N
    python3 a_of_n.py 49-200             # a range
    python3 a_of_n.py 10000 --digits 15  # more digits
    python3 a_of_n.py 49-60 --json
    python3 a_of_n.py 52 --exact          # also print the exact form

For a non-square N ≥ 49 with k = ⌊√N⌋ and the intervals I_i = [d0_i, d1_i] of intervals.json,

    a(N) = max { min(a_i(N), k + d1_i) : a_i(N) > k + d0_i },   a_i(N) = 2α_i + √(4α_i² + N + 4β_i − 4α_i k).

The script prints the interval i that attains the maximum, the exact form of a(N) (either
2α_i + √R_i with exact rationals, or the rational k + d1_i), and a decimal value rounded DOWN, so the
printed decimal is itself a valid lower bound for s(N). All decisions (which intervals count, the cap at
k + d1_i, the maximum) are made in exact rational arithmetic; square roots are bounded from below and
above with integer square roots. Python 3 standard library only.
"""
import argparse, json, os, sys
from fractions import Fraction as Q
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    rows = json.load(open(os.path.join(HERE, 'intervals.json')))['intervals']
    return [(r['index'], Q(r['d0']), Q(r['d1']), r['open_left'], Q(r['certified_line']['alpha']), Q(r['certified_line']['beta']))
            for r in rows]


def root_gt(al, R, c):
    """2α + √R > c, exactly."""
    t = c - 2 * al
    return t < 0 or R > t * t


def sqrt_bounds(R, scale):
    """Integers lo, hi with lo/scale ≤ √R ≤ hi/scale."""
    lo = isqrt(R.numerator * scale * scale // R.denominator)
    return lo, lo + 1


def value_bounds(v, scale):
    """Rational bounds (lo, hi) for a candidate value v = ('q', q) or ('r', α, R)."""
    if v[0] == 'q': return v[1], v[1]
    lo, hi = sqrt_bounds(v[2], scale)
    return 2 * v[1] + Q(lo, scale), 2 * v[1] + Q(hi, scale)


def greater(u, v):
    """u > v exactly for candidate values (rational, or 2α + √R)."""
    if u[0] == 'q' and v[0] == 'q': return u[1] > v[1]
    if u[0] == 'q': return not root_gt(v[1], v[2], u[1]) and not _eq_qr(u[1], v)
    if v[0] == 'q': return root_gt(u[1], u[2], v[1])
    scale = 10 ** 40
    while scale < 10 ** 4000:                      # refine until the intervals separate (equal values never occur here)
        a, b = value_bounds(u, scale), value_bounds(v, scale)
        if a[0] > b[1]: return True
        if a[1] < b[0]: return False
        if u[1:] == v[1:]: return False
        scale *= 10 ** 40
    raise ArithmeticError('could not separate two candidate values')


def _eq_qr(q, v):
    t = q - 2 * v[1]
    return t >= 0 and t * t == v[2]


def a_of_n(N, ivs):
    k = isqrt(N)
    if N < 49: return dict(N=N, k=k, claim=False, note='no claim for N < 49')
    if k * k == N: return dict(N=N, k=k, claim=True, interval=None, exact=f'{k}', value=Q(k), note='square: area bound')
    best = None
    for i, d0, d1, ol, al, be in ivs:
        R = 4 * al * al + N + 4 * be - 4 * al * k
        if R < 0 or not root_gt(al, R, k + d0): continue
        cand = ('q', k + d1) if root_gt(al, R, k + d1) else ('r', al, R)     # cap at the interval's right end
        if best is None or greater(cand, best[1]): best = (i, cand)
    i, v = best
    exact = f'{v[1]} (= k + d1_{i})' if v[0] == 'q' else f'2*({v[1]}) + sqrt({v[2]})'
    return dict(N=N, k=k, claim=True, interval=i, exact=exact, value=v)


def floor_decimal(v, digits):
    scale = 10 ** digits
    if isinstance(v, Q): lo = v
    elif v[0] == 'q': lo = v[1]
    else: lo = value_bounds(v, 10 ** (digits + 20))[0]
    n = (lo * scale).numerator // (lo * scale).denominator
    s = str(n).rjust(digits + 1, '0')
    return f'{s[:-digits]}.{s[-digits:]}' if digits else s


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('n', help='N or a range N1-N2'); ap.add_argument('--digits', type=int, default=9); ap.add_argument('--json', action='store_true')
    ap.add_argument('--exact', action='store_true', help='also print the exact form (2α + √R with exact rationals, or k + d1)')
    a = ap.parse_args()
    lo, _, hi = a.n.partition('-'); lo = int(lo); hi = int(hi) if hi else lo
    ivs = load(); out = []
    for N in range(lo, hi + 1):
        r = a_of_n(N, ivs)
        if r.get('claim'): r['a_N_rounded_down'] = floor_decimal(r['value'], a.digits)
        r.pop('value', None)
        if a.json and not a.exact: r.pop('exact', None)
        out.append(r)
        if not a.json:
            if not r['claim']: print(f'{N}: {r["note"]}')
            else:
                print(f'{N}: a(N) = {r["a_N_rounded_down"]} (k = {r["k"]}, interval {r["interval"] or "-"})')
                if a.exact: print(f'    exact: {r["exact"]}')
    if a.json: json.dump(out, sys.stdout, indent=1); print()


if __name__ == '__main__':
    main()
