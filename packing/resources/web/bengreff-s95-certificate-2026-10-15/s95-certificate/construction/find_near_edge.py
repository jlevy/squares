"""Free point atoms lying (within EPS) on the edges of the unit square at the degenerate pose of each
uncertified box: angle snapped to the nearest arctan(p/q) (q <= 10) inside the box's angle range, centre at
the box centre. Covers rational-slope coincidences that are not Pythagorean (e.g. arctan(1/5)).
usage: python find_near_edge.py COVER EPS LOG [LOG ...]  -> "x y" lines"""
import sys, re, math
import numpy as np
cover, eps, logs = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
toks = [ln.split() for ln in open(cover) if ln.strip() and not ln.startswith("#")]
K = int(toks[1][0]); D = int(toks[2][0]); m = int(toks[4][0])
P = np.array(toks[5:5 + m], dtype=np.int64); xy = P[:, :2] / D
lo, hi = 2.5, K - 2.5
free = ((xy[:, 0] >= lo) & (xy[:, 0] <= hi)) | ((xy[:, 1] >= lo) & (xy[:, 1] <= hi))
slopes = sorted({math.degrees(math.atan2(p, q)) for q in range(1, 11) for p in range(0, q + 1)} |
                {90 - math.degrees(math.atan2(p, q)) for q in range(1, 11) for p in range(0, q + 1)})
out = set()
for lg in logs:
    for ln in open(lg):
        mm = re.match(r"\s*-\s+([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)\s*$", ln)
        if not mm: continue
        x0, x1, y0, y1, t0, t1 = map(float, mm.groups())
        inr = [s for s in slopes if t0 - 1e-6 <= s <= t1 + 1e-6]
        th = math.radians(inr[0] if inr else (t0 + t1) / 2)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = xy[:, 0] - cx, xy[:, 1] - cy
        u = math.cos(th) * dx + math.sin(th) * dy; v = -math.sin(th) * dx + math.cos(th) * dy
        near = free & (((np.abs(np.abs(u) - 0.5) <= eps) & (np.abs(v) <= 0.5 + eps)) |
                       ((np.abs(np.abs(v) - 0.5) <= eps) & (np.abs(u) <= 0.5 + eps)))
        print("%s: box (%.6f, %.6f) angle %.4f deg%s: %d free atoms within %.0e of an edge" %
              (lg, cx, cy, math.degrees(th), " (snapped)" if inr else "", near.sum(), eps), file=sys.stderr)
        for a, b in xy[near]:
            out.add("%.6f %.6f" % (a, b))
for s in sorted(out): print(s)
