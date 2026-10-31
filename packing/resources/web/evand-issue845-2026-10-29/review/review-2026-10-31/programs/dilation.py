"""Dilation check (review bold-ritchie-rv-daniel): certificate side and centres against the
source's binary64 input (header 'n S', rows 'x y degrees'); decides nothing."""
import sys, math
from fractions import Fraction as F
def rd(path, cert):
    rows, side = [], None
    for l in open(path):
        l = l.strip()
        if not l or l.startswith('#'): continue
        p = l.split()
        if side is None: side = F(p[1]) if cert else F(float(p[1])); continue
        rows.append([F(v) for v in p] if cert else [F(float(v)) for v in p])
    return side, rows
for n in sys.argv[2:]:
    Sc, C = rd(f'{sys.argv[1]}/s{n}_1028.cert', True)
    Si, I = rd(f'{sys.argv[1]}/s{n}_1028.input.txt', False)
    fac = Sc / Si
    dc = max(max(abs(float(c[0] - fac * i[0])), abs(float(c[1] - fac * i[1]))) for c, i in zip(C, I))
    da = 0.0
    for c, i in zip(C, I):
        a = math.degrees(2 * math.atan(float(c[2])))
        d = (a - float(i[2])) % 90; da = max(da, min(d, 90 - d))
    print(f'n={n} S_cert - S_input = {float(Sc - Si):.4e}; factor - 1 = {float(fac - 1):.4e}; '
          f'max |centre - factor*input| = {dc:.3e}; max turn vs input = {da:.3e} deg')
