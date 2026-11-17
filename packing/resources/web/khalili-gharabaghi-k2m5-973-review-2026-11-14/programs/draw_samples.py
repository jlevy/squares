"""Draw every pre-stated sample of PLAN.md from one random.Random(973) stream, in the plan's order.

usage: python -I draw_samples.py LOGDIR COVDIR TTOUTDIR OUT_JSON
  LOGDIR    the source's verification/logs/zmx2_box11 (column logs: which roots are uncertified, column CPU)
  COVDIR    the extracted cov/ dumps (leftover boxes; per-root CPU)
  TTOUTDIR  the source's tight_tile/out (per-job seconds)
Order: S1, S2, S3, S4 (exact poses for the evaluator), Z-B, Z-C, Z-E, T-A.
Every pose is (cx, cy, u) as exact fractions, u = tan(theta/2).
"""
import glob
import json
import math
import os
import re
import sys
from fractions import Fraction as F
import random

logd, covd, ttd, out = sys.argv[1:5]
rng = random.Random(973)
Q = 10 ** 6


def rat(lo, hi):
    return lo + (hi - lo) * F(rng.randrange(Q + 1), Q)


def width(u):
    return (1 + 2 * u - u * u) / (1 + u * u)


samples = {}
# S1: uniform admissible poses, theta uniform in [0, 90 deg)
s1 = []
for _ in range(20000):
    th = rng.random() * math.pi / 2
    u = F(math.tan(th / 2)).limit_denominator(Q)
    if u >= 1:
        u = F(Q - 1, Q)
    w = width(u)
    s1.append((rat(w / 2, 11 - w / 2), rat(w / 2, 11 - w / 2), u))
samples["S1"] = s1
# S2: base lines of the Tight-Tile Lemma's ranges, both signs, 10 face points at h = 1e-5 and 10 at h = 1e-7
RANGES = {F(3, 2): [(14, 17), (24, 27), (33, 55)], F(5, 2): [(14, 17), (23, 27), (33, 37), (38, 55)],
          F(7, 2): [(14, 17), (23, 27), (33, 37), (41, 45)]}
s2 = []
for d0, rs in RANGES.items():
    lines = sorted({j for a, b in rs for j in range(a, b + 1)})
    for sg in (1, -1):
        for j in lines:
            yb = F(j, 10)
            for h in (F(1, 10 ** 5), F(1, 10 ** 7)):
                for _ in range(10):
                    p, q = rat(-4, 4), rat(-4, 4)
                    s2.append((d0 + h * p, yb + h * q, sg * h, str(d0), sg, str(yb), str(p), str(q), str(h)))
samples["S2"] = s2
# S3: the root-9632 window
W = (F("4.3224"), F("4.3264"), F("4.3199"), F("4.3239"), F("0.0229"), F("0.0272"))
samples["S3"] = [(rat(W[0], W[1]), rat(W[2], W[3]), rat(W[4], W[5])) for _ in range(2000)]
# S4: 2,000 leftover boxes of the coverage dumps: centre and u > 0 corners
pat = re.compile(r"^UNCERT (\d+) pass \d+ box (\S+) ")
boxes = []
for f in sorted(glob.glob(os.path.join(covd, "r*.out"))):
    for line in open(f):
        m = pat.match(line)
        if m:
            boxes.append((int(m.group(1)), m.group(2)))
pick = rng.sample(range(len(boxes)), 2000)
s4 = []
for i in pick:
    rid, b = boxes[i]
    x0, x1, y0, y1, u0, u1 = (F(t) for t in b.split(","))
    pts = [((x0 + x1) / 2, (y0 + y1) / 2, (u0 + u1) / 2)]
    for x in (x0, x1):
        for y in (y0, y1):
            for u in (u0, u1):
                if u > 0:
                    pts.append((x, y, u))
    s4.append((rid, b, pts))
samples["S4"] = s4
samples["S4_population"] = len(boxes)
# Z-B: 3 whole columns among those with recorded CPU in [1, 300] s
col_cpu = {}
unc_roots = set()
for f in sorted(glob.glob(os.path.join(logd, "col*.out"))):
    c = int(re.search(r"col(\d+)\.out", f).group(1))
    t = open(f).read()
    col_cpu[c] = int(re.findall(r"cpu (\d+)s", t)[-1])
    unc_roots |= {int(r) for r in re.findall(r"^UNCERT (\d+) ", t, re.M)}
elig = sorted(c for c, s in col_cpu.items() if 1 <= s <= 300)
samples["ZB_eligible"] = elig
samples["ZB"] = sorted(rng.sample(elig, 3))
# Z-C: 40 roots among the certified ones (D4 ids: (i*55 + j)*4 + bin)
cert_roots = sorted(set(range(12100)) - unc_roots)
samples["ZC_population"] = len(cert_roots)
samples["ZC"] = sorted(rng.sample(cert_roots, 40))
# Z-E: 3 tight-tile roots whose dump records at most 120 CPU-s
cov_cpu = {}
for f in sorted(glob.glob(os.path.join(covd, "r*.out"))):
    rid = int(re.search(r"r(\d+)\.out", f).group(1))
    m = re.findall(r"cpu (\d+)s", open(f).read())
    cov_cpu[rid] = int(m[-1])
elig = sorted(r for r, s in cov_cpu.items() if s <= 120)
samples["ZE_eligible"] = elig
samples["ZE"] = sorted(rng.sample(elig, 3))
# T-A: 8 main tight-tile jobs whose outputs record at most 120 s
jobs = {}
for f in sorted(glob.glob(os.path.join(ttd, "*.out"))):
    secs = 0
    for line in open(f):
        if line.startswith("{"):
            secs += json.loads(line).get("secs", 0)
    jobs[os.path.basename(f)] = secs
elig = sorted(n for n, s in jobs.items() if s <= 120)
samples["TA_eligible_count"] = len(elig)
samples["TA"] = sorted(rng.sample(elig, 8))
json.dump(samples, open(out, "w"), default=str)
print({k: (v if not isinstance(v, list) or len(v) < 50 else len(v)) for k, v in samples.items()})
