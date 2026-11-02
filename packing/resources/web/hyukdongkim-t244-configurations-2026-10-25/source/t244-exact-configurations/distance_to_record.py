"""Distance between an exact configuration and the record's binary64 packing (centres and angles)."""
import json, math, sys
from fractions import Fraction as Fr
cert, rec = sys.argv[1], sys.argv[2]
C = json.load(open(cert)); A = json.load(open(rec))
ta, tb = (Fr(x) for x in C["field"]["t_interval"]); t = float((ta + tb) / 2)
ev = lambda cs: sum(float(Fr(c)) * t ** i for i, c in enumerate(cs)) if cs else 0.0
dmax = amax = 0.0
for q, a in zip(C["squares"], A["squares"]):
    x, y = ev(q["x"]), ev(q["y"]); th = 2 * math.atan(ev(q["u"])) + q["m"] * math.pi / 2
    dmax = max(dmax, math.hypot(x - a[0], y - a[1]))
    amax = max(amax, abs(((math.degrees(th) - a[2] + 45) % 90) - 45))
print(f"{cert}: max centre distance to the record {dmax:.2e}, max angle difference {amax:.2e} degrees "
      f"(binary64 evaluation)")
