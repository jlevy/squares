"""Tilt census of a certificate (review bold-ritchie-rv-daniel; binary64, decides nothing)."""
import sys, math
from collections import Counter
from fractions import Fraction as F
for path in sys.argv[1:]:
    rows = [l.split() for l in open(path) if l.strip() and not l.startswith('#')][1:]
    angs = []
    for x, y, t in rows:
        a = math.degrees(2 * math.atan(float(F(t)))) % 90
        angs.append(min(a, 90 - a) * (1 if a <= 45 else -1))
    c = Counter(round(a, 2) for a in angs if abs(a) > 1e-6)
    upright = sum(1 for a in angs if abs(a) <= 1e-6)
    print(path.split('/')[-1], 'upright', upright, 'tilted', len(angs) - upright, 'top tilts (deg, count):', c.most_common(4))
