"""Summarise rational certificates: header, denominators, squeeze against n - 1/10000."""
import sys
from fractions import Fraction as F
from math import lcm

def read_cert(path):
    rows = []
    hdr = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if hdr is None:
                hdr = [F(p) for p in parts]
                continue
            rows.append(tuple(F(p) for p in parts))
    return hdr, rows

if __name__ == '__main__':
    for p in sys.argv[1:]:
        hdr, rows = read_cert(p)
        n = int(hdr[0])
        assert n == len(rows), (p, n, len(rows))
        dxy = 1
        dt = 1
        for x, y, t in rows:
            dxy = lcm(dxy, x.denominator, y.denominator)
            dt = lcm(dt, t.denominator)
        print(p.split('/')[-1], 'n', n, 'hdr', [float(h) for h in hdr[1:]], 'Dxy bits', dxy.bit_length(), 'Dt bits', dt.bit_length(),
              'pow2xy', dxy & (dxy - 1) == 0, 'pow2t', dt & (dt - 1) == 0)
