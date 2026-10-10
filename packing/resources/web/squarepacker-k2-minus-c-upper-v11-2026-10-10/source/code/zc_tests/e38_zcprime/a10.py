# a10.py -- E38 (z38.build, ZC walls) in the window [cy b^{4/5}, cy b^{4/5} + 2] with the wall parameters (cD, cR, aw)
# of a v3 tier, at a cy for which the main cut is aligned (tau > 0) at feasible b; exact certificate (cert.py).
# usage: python a10.py b cy_num cy_den cD_num cD_den aw offset_num offset_den
import sys, json, math
import run38
from z38 import F
b = int(sys.argv[1]); cy = F(int(sys.argv[2]), int(sys.argv[3])); cD = F(int(sys.argv[4]), int(sys.argv[5]))
aw = float(sys.argv[6]); off = F(int(sys.argv[7]), int(sys.argv[8]))
# y0 := ceil(4 cy b^{4/5})/4 (computed with a float b^{4/5}, then checked exactly against the window)
y0 = F(math.ceil(4 * float(cy) * b ** 0.8), 4)
y = y0 + off
lo = float(cy) * b ** 0.8
r = run38.run(b, y, cD, cD, aw, True, False)
r['cy'] = str(cy); r['offset'] = str(off); r['window_ok'] = bool(lo <= float(y) <= lo + 2)
r['tau_over_ta'] = r['tau'] / r['ta'] if r['ta'] else None
print(json.dumps(r), flush=True)