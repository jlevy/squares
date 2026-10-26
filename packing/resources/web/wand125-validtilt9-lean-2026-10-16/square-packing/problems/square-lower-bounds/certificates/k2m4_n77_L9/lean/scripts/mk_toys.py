#!/usr/bin/env python3
"""Write the toy mixed covers used to validate the mixed Lean verifier (lean/toys/), from
search/zm_mixed_test.py's grid_cover (ZM_MIXED.md §4.3): grid lines at uniform density.

  M2        m = 2: the lines x = 1, y = 1 at density 5/8 (total 2.5 < 3: s(3) >= 2)
  M2bad     M2 x 0.95 (minimum 0.984 < 1: must be rejected)
  T1        m = 4: the six interior grid lines at 5/8 (total 15 < 16)
  R_lighten T1 x 0.95 (must be rejected)
  T1p       T1 with a point of mass 0.02 at every tile centre (points + segments)
  M2p       M2 at density 1/2 plus points 0.2 at the four tile centres and 0.05 on the lines' crossing
Usage: python3 lean/scripts/mk_toys.py lean/toys
"""
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'search'))
import zm_mixed_test as ZT  # noqa: E402
import mixed_cover as MC  # noqa: E402

out = sys.argv[1] if len(sys.argv) > 1 else 'lean/toys'
os.makedirs(out, exist_ok=True)
D = 1000
T1p = [(D // 2 + i * D, D // 2 + j * D, 20000) for i in range(4) for j in range(4)]
M2p = [(D // 2 + i * D, D // 2 + j * D, 200000) for i in range(2) for j in range(2)] + [(D, D, 50000)]
for name, cv in [('M2', ZT.grid_cover(m=2, rho=F(5, 8))), ('T1', ZT.grid_cover(rho=F(5, 8))),
                 ('M2bad', ZT.grid_cover(m=2, rho=F(5, 8) * F(95, 100))),
                 ('R_lighten', ZT.grid_cover(rho=F(5, 8) * F(95, 100))),
                 ('T1p', ZT.grid_cover(rho=F(5, 8), pts=T1p)),
                 ('M2p', ZT.grid_cover(m=2, rho=F(1, 2), pts=M2p))]:
    MC.validate(cv)
    MC.write(os.path.join(out, name + '.txt'), cv, comment='toy ' + name + ' (lean/scripts/mk_toys.py)')
    print(name, float(MC.total(cv)))
