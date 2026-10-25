#!/usr/bin/env python3
"""Regenerate the exact certificates of the Karimi two-strip records from records.csv.

    python3 regenerate.py                 # writes certificates/n<N>.cert for every row
    python3 regenerate.py 2458 2459       # only these n

Construction (Mohsen Karimi). Box side S just below the integer K.
  H strip: mH rows of squares tilted by -a_H (tan(a_H/2) = tH) on the bottom wall,
           from the left wall to the V strip.
  V strip: mV columns of squares tilted by a_V (tan(a_V/2) = tV) on the right wall,
           full height (the H construction turned by 90 degrees).
  Grid:    (K-mV) x (K-mH) axis-parallel squares in the top-left corner.
Inside a strip consecutive rows touch: row j sits at height e + j cos a and is shifted
horizontally by sin a (mod 1/cos a); ph sets the shift of the first row.
If the construction holds more than n squares, surplus grid squares are removed.
All arithmetic is exact (fractions). Output format per line: x y t, t = tan(theta/2).

Check the files with the exact verifier of Mishapolk/square-packing-records:
    python3 check_packing.py certificates/n2458.cert
"""
import csv, os, sys
from fractions import Fraction as F


def trig(t):
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def strip(t, m, W, ph):
    ca, sa = trig(t)
    e = (ca + sa) / 2; p = 1 / ca
    out = []
    for j in range(m):
        x = e + (ph * p + j * sa) % p
        if x - p >= e:
            x -= p
        y = e + j * ca
        while x + e <= W:
            out.append((x, y)); x += p
    return out


def build(n, S, K, mH, tH, phH, mV, tV, phV):
    caH, saH = trig(tH); caV, saV = trig(tV)
    assert mH * caH + saH <= S - (K - mH), 'H strip does not fit'
    wV = mV * caV + saV
    assert wV <= S - (K - mV), 'V strip does not fit'
    sq = [(x, y, -tH) for x, y in strip(tH, mH, S - wV, phH)]
    sq += [(S - y, x, -tV) for x, y in strip(tV, mV, S, phV)]
    sq += [(F(1, 2) + i, S - F(1, 2) - j, F(0)) for i in range(K - mV) for j in range(K - mH)]
    while len(sq) > n:                       # drop surplus grid squares (last added first)
        for i in range(len(sq) - 1, -1, -1):
            if sq[i][2] == 0:
                sq.pop(i); break
    assert len(sq) == n, f'construction holds only {len(sq)} squares'
    return sq


def fr(q):
    return f'{q.numerator}/{q.denominator}'


def main(only):
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(here, 'certificates'), exist_ok=True)
    for r in csv.DictReader(open(os.path.join(here, 'records.csv'))):
        n = int(r['n'])
        if only and n not in only:
            continue
        S = F(r['new_side_exact']); K = int(r['K'])
        p = dict(mH=int(r['mH']), tH=F(r['tH']), phH=F(r['phH']),
                 mV=int(r['mV']), tV=F(r['tV']), phV=F(r['phV']))
        sq = build(n, S, K, **p)
        with open(os.path.join(here, 'certificates', f'n{n}.cert'), 'w') as f:
            f.write(f"# N={n}, Karimi two-strip construction (Mohsen Karimi), K={K}, "
                    f"mH={p['mH']} tH={fr(p['tH'])} phH={fr(p['phH'])} mV={p['mV']} tV={fr(p['tV'])} phV={fr(p['phV'])}\n")
            f.write(f'{n} {fr(S)}\n')
            for x, y, t in sq:
                f.write(f'{fr(x)} {fr(y)} {fr(t)}\n')
        print('wrote', n)


if __name__ == '__main__':
    main({int(a) for a in sys.argv[1:]})
