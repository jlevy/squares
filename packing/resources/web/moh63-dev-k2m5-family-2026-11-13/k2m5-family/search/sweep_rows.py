#!/usr/bin/env python3
"""Summarize a zmx2 oracle sweep and write its uncertified poses as LP rows.
usage: sweep_rows.py LOGDIR OUT.npz
Reads LOGDIR/col*.out; keeps tilts in [0.05, 89.95] deg and admissible poses (the quadrant model's domain), as in
Daniel's qx2_xloop.sh."""
import glob, math, re, sys
import numpy as np

logdir, out = sys.argv[1], sys.argv[2]
tot = cpu = 0; fm = []; P = []
for f in sorted(glob.glob(f'{logdir}/col*.out')):
    t = open(f).read()
    m = re.search(r'uncertified (\d+), max depth (\d+), cpu (\S+)s', t)
    tot += int(m.group(1)); cpu += float(m.group(3))
    for l in t.splitlines():
        if not l.startswith('UNCERT'): continue
        mm = re.search(r'th ([\d.]+)-[\d.]+ deg\) \| float-min ([\d.]+) at \(([\d.]+),([\d.]+),u ([\d.]+)', l)
        if not mm: continue
        th0, v, x, y, u = map(float, mm.groups()); fm.append((v, th0, x, y))
        th = 2 * math.atan(u)
        if math.radians(0.05) <= th <= math.radians(89.95) and min(x, y) >= (math.cos(th) + math.sin(th)) / 2:
            P.append((x, y, th))
g = [a for a in fm if a[1] >= 0.05]
print(f'uncertified {tot} (listed {len(fm)}), cpu {cpu / 3600:.2f} h')
print(f'tilt >= 0.05 deg: {len(g)} listed, {sum(a[0] < 1 for a in g)} with float-min < 1'
      + (f', worst {min(g)[0]} at {min(g)[1:]}' if g else ''))
print(f'tilt < 0.05 deg: {len(fm) - len(g)} listed, {sum(a[0] < 1 for a in fm if a[1] < 0.05)} below 1')
P = np.unique(np.round(np.array(P), 12), axis=0) if P else np.zeros((0, 3))
np.savez(out, rows=P); print(f'{len(P)} rows -> {out}')
