"""Triage diagnostic for #594: bind the Lean data of S76T/Pts.lean to the cover file.

Extracts every (X, Y, w) of the `pts` tree and every (X0, Y0, X1, Y1, w) of the `segs` tree
from the generated Lean source, and compares them as multisets with the cover's points
(aggregated by location, positive weights) and segments (endpoints in canonical order,
aggregated, positive weights), which is what mk_s76_lean.py says it emits. Also prints the
total and checks the region constants of S76Cover in S76Lower.lean.

usage: python -I lean_data_binding.py PTS_LEAN[.gz] COVER S76LOWER_LEAN
"""
import gzip
import re
import sys
from collections import Counter
from fractions import Fraction as F

pts_path, cover_path, lower_path = sys.argv[1:4]
op = gzip.open if pts_path.endswith(".gz") else open
lines = op(pts_path, "rt").read().splitlines()
pts_line = next(i for i, ln in enumerate(lines) if ln.startswith("noncomputable def pts")) + 1
segs_line = next(i for i, ln in enumerate(lines) if ln.startswith("noncomputable def segs")) + 1
pts_text, segs_text = lines[pts_line], lines[segs_line]
lean_pts = Counter(tuple(map(int, m)) for m in re.findall(r"(?<=\s)(\d+) (\d+) (\d+)(?=\s)", pts_text))
lean_segs = Counter(tuple(map(int, m)) for m in re.findall(r"\((\d+), (\d+), (\d+), (\d+), (\d+)\)", segs_text))
# every numeral in the trees is accounted for by the extracted tuples
assert len(re.findall(r"\d+", pts_text)) == 3 * sum(lean_pts.values()), "unparsed numerals in pts"
assert len(re.findall(r"\d+", segs_text)) == 5 * sum(lean_segs.values()), "unparsed numerals in segs"

toks = [ln.split() for ln in open(cover_path) if ln.strip() and not ln.startswith("#")]
D, W, m = int(toks[2][0]), int(toks[3][0]), int(toks[4][0])
agg = Counter()
for t in toks[5:5 + m]:
    x, y, w = map(int, t)
    if w > 0:
        agg[(x, y)] += w
k = int(toks[5 + m][0])
sagg = Counter()
for t in toks[6 + m:6 + m + k]:
    a, b, c, d, w = map(int, t)
    if w > 0:
        p, q = sorted([(a, b), (c, d)])
        sagg[(p, q)] += w
cover_pts = Counter((x, y, w) for (x, y), w in agg.items())
cover_segs = Counter((p[0], p[1], q[0], q[1], w) for (p, q), w in sagg.items())
print(f"lean pts {sum(lean_pts.values())} (distinct {len(lean_pts)}), cover locations {len(agg)}; equal: {lean_pts == cover_pts}")
print(f"lean segs {sum(lean_segs.values())} (distinct {len(lean_segs)}), cover segments {len(sagg)}; equal: {lean_segs == cover_segs}")
tot = sum(w * c for (_, _, w), c in lean_pts.items()) + sum(t[4] * c for t, c in lean_segs.items())
print(f"lean total {F(tot, W)} = {tot / W:.9f}; below 76: {tot < 76 * W}")
lower = open(lower_path).read()
m2 = re.search(r"CovM (\d+) (\d+) (\d+) (\d+) (\d+) pts\.toList segs\.toList 0 \((\d+) \* (\d+) - (\d+) \* (\d+) / 2\) 0 \((\d+) \* (\d+) - (\d+) \* (\d+) / 2\) 0 (\d+)", lower)
Dl, S, Mq, R, Wl = (int(m2.group(i)) for i in range(1, 6))
half = int(m2.group(6)) * int(m2.group(7)) - int(m2.group(8)) * int(m2.group(9)) // 2
umax = int(m2.group(14))
print(f"S76Cover: D={Dl} S={S} Mq={Mq} R={R} W={Wl}; centre upper limit {F(half, Dl * S)}; u upper limit {F(umax, R)}")
print(f"consistent with cover: D {Dl == D}, W {Wl == W}, Mq = 9D {Mq == 9 * D}")
