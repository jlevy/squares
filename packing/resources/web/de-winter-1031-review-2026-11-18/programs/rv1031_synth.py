"""Write a synthetic certificate in the two byte layouts of jlevy/squares#1031's source.

Written for this review; decides nothing.  It writes ``OUT.json`` (form J) and
``OUT.yaml`` (form C) for 13 squares in a box of side 8: a 3 x 3 grid of upright squares
in contact at the lower-left corner, two tilted squares apart, and two upright squares at
the right wall, one of them in the top-right corner.  ``dilated`` opens every gap by a
dilation of 1 + 2e-28 and sets the squares 1e-28 from the left and bottom walls.

    python -I -B rv1031_synth.py OUT contact|dilated
"""
import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # this packet's own modules, under python -I
import rv1031_reader as R

out = sys.argv[1]
kind = sys.argv[2] if len(sys.argv) > 2 else "contact"
def fs(v):
    return f"{v.numerator}/{v.denominator}" if v.denominator != 1 else str(v.numerator)
S = F(8)
poses = []
for i in range(3):
    for j in range(3):
        poses.append((F(2*i+1, 2), F(2*j+1, 2), F(1), F(0)))
t = R.tangent_direction(F(1, 2))  # (3/5, 4/5)
t2 = R.tangent_direction(F(-123456789, 10**12))
poses.append((F(5) + F(1, 10**50), F(5), *t))
poses.append((F(13, 2) + F(3, 10**45), F(5) + F(7, 10**47), *t2))
poses.append((S - F(1, 2), S - F(1, 2), F(1), F(0)))
poses.append((S - F(1, 2), F(1, 2) + F(1, 3), F(0), F(1)))
if kind == "dilated":
    g = 1 + F(2, 10**28)
    poses = [(g*x + F(1, 10**28), g*y + F(1, 10**28), ux, uy) for x, y, ux, uy in poses]
    S = g*S + F(3, 10**28)
n = len(poses)
doc = {"n": n, "side": fs(S), "square_size": "1", "format": "synthetic", "squares": [[fs(x), fs(y), fs(ux), fs(uy)] for x, y, ux, uy in poses]}
open(out + ".json", "w").write(json.dumps(doc, indent=1))
lines = ["softschema:", "  contract: packing.squares:Witness/v2", "  schema: x", "  envelope: witness", "  status: enforced",
 "witness:", "  id: W-n013-synthetic", f"  n: {n}", f"  side: {fs(S) if "/" in fs(S) else chr(39)+fs(S)+chr(39)}", "  square_size: '1'", "  representation: corners",
 "  scalar:", "    kind: rational", "  coordinates:", "    origin: lower-left", "    axes: x-right-y-up", "    angle_unit: not-applicable",
 "  claim:", "    coordinate_provenance: reported", "    method: exact-algebraic", "    limitations: synthetic", "  squares:"]
for k, p in enumerate(poses, start=1):
    lines += [f"  - id: square-{k}", "    corners:"]
    for x, y in R.pose_corners(p):
        q = lambda v: fs(v) if "/" in fs(v) else f"'{fs(v)}'"
        lines += [f"    - - {q(x)}", f"      - {q(y)}"]
open(out + ".yaml", "w").write("\n".join(lines) + "\n")
print(n, float(S))
