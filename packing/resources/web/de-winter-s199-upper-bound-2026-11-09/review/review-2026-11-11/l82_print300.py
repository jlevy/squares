"""Compare the author's 300-place print of the optimum with the root isolated here.

Usage: python -I l82_print300.py ALGEBRA_JSON OPTIMUM_300_TXT OUT.json
"""

import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l82_check as C  # noqa: E402

alg = json.load(open(sys.argv[1]))
lo, hi = (F(x) for x in alg["946_root_bracket"])
line = next(ln for ln in open(sys.argv[2], encoding="utf-8") if not ln.startswith("#"))
n, side = line.split()[:2]
places = len(side.split(".")[1])
out = {
    "n": n, "places": places,
    "equals_root_floor": side == C.decimal_floor(lo, places) == C.decimal_floor(hi, places),
}
with open(sys.argv[3], "w") as fh:
    json.dump(out, fh, indent=1)
print(out)
