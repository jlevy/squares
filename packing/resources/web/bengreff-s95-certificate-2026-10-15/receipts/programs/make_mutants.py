"""Triage diagnostic for #610: write the drop-heaviest-point and drop-heaviest-segment
mutants of a cover with the repository's own devtools.replay_evand_zmx2.mutate, and print
where the dropped mass sits and the D4 root cells (pitch 1/10 over [0, s/2]^2) within one
unit of it, the ones a zmx2 control can be run on. The #594 triage's make_mutants.py with
the output prefix and the side read from the cover.

usage: python -I make_mutants.py PACKING_DIR COVER OUT_DIR PREFIX
"""

import hashlib
import re
import sys
from fractions import Fraction as F
from pathlib import Path

packing, cover, out, prefix = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
sys.path.insert(0, str(packing))
from devtools.replay_evand_zmx2 import mutate  # noqa: E402

text = cover.read_text()
toks = [ln.split("#", 1)[0].split() for ln in text.splitlines()]
toks = [t for t in toks if t]
side = F(int(toks[1][0]), int(toks[1][1]))
D = int(toks[2][0])
half = side / 2
for kind in ("drop-heaviest-point", "drop-heaviest-segment"):
    m = mutate(text, kind)
    path = out / f"{prefix}_{kind}.txt"
    path.write_text(m.text)
    print(kind, m.detail, "removed", m.removed, "rows", m.rows)
    print("  sha256", hashlib.sha256(m.text.encode()).hexdigest())
    nums = [int(v) for v in re.findall(r"\((\d+), (\d+)\)", m.detail)[0]]
    x, y = F(nums[0], D), F(nums[1], D)
    # the image of the dropped location in the fundamental region [0, s/2]^2, x <= y
    fx, fy = sorted((min(x, side - x), min(y, side - y)))
    print(f"  at ({x}, {y}); image in [0, {half}]^2 with x <= y: ({fx}, {fy})")
