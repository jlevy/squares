"""Triage diagnostic for #610: segment mass on the container walls of a mixed-1 cover, its
census by weight and length, and a copy of the cover with every wall segment removed
(still D4-invariant, lower total). The #594 triage's wall_mass.py with the census added.

No closed unit square inside [0,s]^2 that is not flush with a wall meets a wall in more than
a point, and the mass a flush square captures off the wall is the limit of what squares
moved inward by epsilon capture, so wall segment mass is never needed by the covering
property: a sound checker should certify the stripped cover wherever it certifies the
original.

usage: python -I wall_mass.py COVER STRIPPED_OUT
"""

import sys
from collections import Counter
from fractions import Fraction as F

src, out = sys.argv[1], sys.argv[2]
lines = open(src).read().splitlines()
body = [(i, ln) for i, ln in enumerate(lines) if ln.strip() and not ln.startswith("#")]
assert body[0][1].split() == ["mixed", "1"]
s_num, s_den = map(int, body[1][1].split())
D = int(body[2][1])
W = int(body[3][1])
m = int(body[4][1])
edge = s_num * D // s_den
k_idx = 5 + m
k = int(body[k_idx][1])
segs = body[k_idx + 1 : k_idx + 1 + k]
keep, wall_mass, wall_count, by_wall = [], 0, 0, {}
weights, lengths, places = Counter(), Counter(), Counter()
for _, ln in segs:
    x0, y0, x1, y1, w = map(int, ln.split())
    vertical = x0 == x1
    pos = x0 if vertical else y0
    if pos in (0, edge):
        wall_mass += w
        wall_count += 1
        key = ("x" if vertical else "y") + ("0" if pos == 0 else "s")
        by_wall[key] = by_wall.get(key, 0) + w
        weights[w] += 1
        lengths[F(abs(x1 - x0) + abs(y1 - y0), D)] += 1
        if key == "x0":
            places[F(y0 + y1, 2 * D)] += 1
    else:
        keep.append(ln)
total = sum(int(ln.split()[2]) for _, ln in body[5 : 5 + m]) + sum(
    int(ln.split()[4]) for _, ln in segs
)
print(f"segments {k}, on walls {wall_count}, wall mass {F(wall_mass, W)} = {wall_mass / W:.9f}")
print("by wall:", {key: f"{v / W:.9f}" for key, v in sorted(by_wall.items())})
print("wall segment weights (units of 1/W):", dict(sorted(weights.items())))
print("wall segment lengths:", {str(a): b for a, b in sorted(lengths.items())})
mids = sorted(places)
print(
    f"wall x = 0: {len(mids)} distinct midpoints, from {mids[0] if mids else None} "
    f"to {mids[-1] if mids else None}"
)
print(
    f"total {F(total, W)} = {total / W:.9f}; stripped total {F(total - wall_mass, W)} = "
    f"{(total - wall_mass) / W:.9f}"
)
head = lines[: body[k_idx][0]]
tail = lines[body[k_idx + k][0] + 1 :]
with open(out, "w") as fh:
    fh.write("\n".join(head + [str(len(keep))] + keep + tail) + "\n")
