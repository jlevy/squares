"""Control 'same G, smaller rise': cover ctl_rise.txt = k05-5 with one segment (x = 1.9, y in [5.0, 5.1], weight
0.0284007811) moved up by 1/10 to y in [5.1, 5.2].  At the tight tile (d0, s) = (3/2, 9/2) the face values (h -> 0
limits) are unchanged, but the first-order gain of that segment at the top edge is gone: the exact mass at the pose
(3/2 + h, 9/2 + h, u = h) is 1 - 1.3e-7 at h = 1e-6 (original: 1 + 1.2e-7).  The checker must refuse the C_u chart
around the face point (1, 1); the original cover must certify the same region."""
import sys
from fractions import Fraction as F
import ttbox as T
cov = sys.argv[1]
segs = T.load(cov)
name, ch, poly, h0 = [c for c in T.charts_line(F(3, 2), F(9, 2), 1, F(4), F(1, 4000)) if c[0] == 'C_u'][0]
Q = [(F(3, 4), F(3, 4)), (F(5, 4), F(3, 4)), (F(5, 4), F(5, 4)), (F(3, 4), F(5, 4))]
st, fails = T.run(segs, ch, [Q], h0, maxcells=int(sys.argv[2]) if len(sys.argv) > 2 else 20000, minarea=F(1, 2**60), progress=200)
print(cov, {k: v for k, v in st.items() if k != 'worst'})
inside = [f for f in fails if min(v[0] for v in f[0]) <= 1 <= max(v[0] for v in f[0]) and min(v[1] for v in f[0]) <= 1 <= max(v[1] for v in f[0])]
print('refused cells', len(fails), '; of which containing the face point (1, 1):', len(inside))
for f in fails[:4]: print('  FAIL', [(float(a), float(b)) for a, b in f[0]], f[1])
