"""A JSON file {"n": N, "rows": [[centre x, centre y, turn in radians], ...]} -> a Witness/v2 decimal pose.

python3 make-pose.py rows.json n-NNN-decimal-pose.yaml
"""
import json, math, sys
from decimal import Decimal, ROUND_CEILING

p = json.load(open(sys.argv[1]))
n, rows = p["n"], p["rows"]
assert len(rows) == n
h = lambda a: (abs(math.cos(a)) + abs(math.sin(a))) / 2
x0 = min(x - h(a) for x, y, a in rows); y0 = min(y - h(a) for x, y, a in rows)
side = max(max(x + h(a) for x, y, a in rows) - x0, max(y + h(a) for x, y, a in rows) - y0)
# the declared side: the f64 bounding side, rounded up at 14 places (the promotion recomputes the exact one)
dside = Decimal(repr(side)).quantize(Decimal("1e-14"), rounding=ROUND_CEILING)
out = ["softschema:", "  contract: packing.squares:Witness/v2", "  schema: witness.schema.yaml", "  envelope: witness", "  status: enforced",
       "witness:", f"  id: W-pose-n{n}", f"  n: {n}", f"  side: '{dside}'", "  square_size: '1'", "  representation: center-angle",
       "  scalar:", "    kind: decimal", "  coordinates:", "    origin: lower-left", "    axes: x-right-y-up", "    angle_unit: radians", "  squares:"]
for i, (x, y, a) in enumerate(rows, 1):
    out += [f"  - id: {i}", "    center:", f"    - '{Decimal(repr(x - x0))}'", f"    - '{Decimal(repr(y - y0))}'", f"    angle: '{Decimal(repr(a))}'"]
out += ["  claim:", "    coordinate_provenance: reported", "    method: numerical-f64", "    precision:", "      binary_bits: 53", "      rounding: round-to-nearest",
        "    tolerance: '1e-12'", "    limitations: search output as f64 centres and turns, not verified in this file."]
open(sys.argv[2], "w").write("\n".join(out) + "\n")
print(n, dside)
