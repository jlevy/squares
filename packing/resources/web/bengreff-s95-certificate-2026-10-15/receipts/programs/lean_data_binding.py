"""Triage diagnostic for #610: bind the Lean data of S<N>T/Pts.lean to the cover file. The
#594 triage's lean_data_binding.py with the count and side as arguments.

Extracts every (X, Y, w) of the `pts` tree and every (X0, Y0, X1, Y1, w) of the `segs` tree
from the generated Lean source, and compares them as multisets with the cover's points
(aggregated by location, positive weights) and segments (endpoints in canonical order,
aggregated, positive weights), which is what mk_lean.py says it emits. Also prints the
total, checks the constants of the data facts (`d4Check`, `segD4Check`, `wsum_lt`) and the
region constants of S<N>Cover in S<N>Lower.lean, and lists the theorem statements there.

usage: python -I lean_data_binding.py PTS_LEAN[.gz] COVER LOWER_LEAN N K
"""

import gzip
import re
import sys
from collections import Counter
from fractions import Fraction as F

pts_path, cover_path, lower_path = sys.argv[1:4]
n, side = int(sys.argv[4]), int(sys.argv[5])
op = gzip.open if pts_path.endswith(".gz") else open
text = op(pts_path, "rt").read()
lines = text.splitlines()
pts_line = next(i for i, ln in enumerate(lines) if ln.startswith("noncomputable def pts")) + 1
segs_line = next(i for i, ln in enumerate(lines) if ln.startswith("noncomputable def segs")) + 1
pts_text, segs_text = lines[pts_line], lines[segs_line]
lean_pts = Counter(
    tuple(map(int, m)) for m in re.findall(r"(?<=\s)(\d+) (\d+) (\d+)(?=\s)", pts_text)
)
lean_segs = Counter(
    tuple(map(int, m)) for m in re.findall(r"\((\d+), (\d+), (\d+), (\d+), (\d+)\)", segs_text)
)
# every numeral in the trees is accounted for by the extracted tuples
assert len(re.findall(r"\d+", pts_text)) == 3 * sum(lean_pts.values()), "unparsed numerals in pts"
assert len(re.findall(r"\d+", segs_text)) == 5 * sum(lean_segs.values()), "unparsed numerals in segs"

toks = [ln.split() for ln in open(cover_path) if ln.strip() and not ln.startswith("#")]
D, W, m = int(toks[2][0]), int(toks[3][0]), int(toks[4][0])
agg = Counter()
for t in toks[5 : 5 + m]:
    x, y, w = map(int, t)
    if w > 0:
        agg[(x, y)] += w
k = int(toks[5 + m][0])
sagg = Counter()
for t in toks[6 + m : 6 + m + k]:
    a, b, c, d, w = map(int, t)
    if w > 0:
        p, q = sorted([(a, b), (c, d)])
        sagg[(p, q)] += w
cover_pts = Counter((x, y, w) for (x, y), w in agg.items())
cover_segs = Counter((p[0], p[1], q[0], q[1], w) for (p, q), w in sagg.items())
print(
    f"lean pts {sum(lean_pts.values())} (distinct {len(lean_pts)}), cover locations {len(agg)}; "
    f"equal: {lean_pts == cover_pts}"
)
print(
    f"lean segs {sum(lean_segs.values())} (distinct {len(lean_segs)}), cover segments {len(sagg)}; "
    f"equal: {lean_segs == cover_segs}"
)
tot = sum(w * c for (_, _, w), c in lean_pts.items()) + sum(t[4] * c for t, c in lean_segs.items())
print(f"lean total {F(tot, W)} = {tot / W:.9f}; below {n}: {tot < n * W}")
Mq = side * D
facts = {
    "d4Check": f"theorem pts_d4 : d4Check {Mq} pts = true := by decide +kernel" in text,
    "segD4Check": f"theorem segs_d4 : segD4Check {Mq} segs = true := by decide +kernel" in text,
    "wsum_lt": f"theorem wsum_lt : pts.wsum + segs.wsum < {n} * {W} := by decide +kernel" in text,
    "pts_nodup": "theorem pts_nodup : pts.toList.Nodup :=" in text,
}
print("data-fact statements with this cover's constants:", facts)
lower = open(lower_path).read()
m2 = re.search(
    r"CovM (\d+) (\d+) (\d+) (\d+) (\d+) pts\.toList segs\.toList 0 \((\d+) \* (\d+) - (\d+) \* (\d+) / 2\) "
    r"0 \((\d+) \* (\d+) - (\d+) \* (\d+) / 2\) 0 (\d+)",
    lower,
)
assert m2, "no CovM statement"
Dl, S, Mql, R, Wl = (int(m2.group(i)) for i in range(1, 6))
half = int(m2.group(6)) * int(m2.group(7)) - int(m2.group(8)) * int(m2.group(9)) // 2
half_y = int(m2.group(10)) * int(m2.group(11)) - int(m2.group(12)) * int(m2.group(13)) // 2
umax = int(m2.group(14))
print(
    f"S{n}Cover: D={Dl} S={S} Mq={Mql} R={R} W={Wl}; centre upper limits {F(half, Dl * S)}, "
    f"{F(half_y, Dl * S)}; u upper limit {F(umax, R)}"
)
print(f"consistent with cover: D {Dl == D}, W {Wl == W}, Mq = {side}D {Mql == Mq}")
for stmt in re.findall(r"^theorem .*$", lower, flags=re.M):
    print("statement:", stmt)
print("namespace refers to S%dT:" % n, f"open BoxTree ZMTreeM S{n}T" in lower)
