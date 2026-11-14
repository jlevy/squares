#!/usr/bin/env python3
"""Audit of the recorded zmx2 sweep of the 11 x 11 board (logs in verification/logs/zmx2_box11).
Checks: theta = 0 sweep (cert0) VERIFIED on all 2,500 roots; all 55 columns of the first-order D4 sweep finished
(12,100 roots, none missing) with one settings hash, depth 40, on the cover with total 121 - 4D; and the roots left
with uncertified boxes are exactly the 75 tight-tile roots dumped in cov/ plus root 9632.
usage: audit_zmx2.py LOGDIR COVDIR"""
import sys, os, re, glob
logd, covd = sys.argv[1:3]
c0 = open(os.path.join(logd, 'cert0.txt')).read()
assert 'roots 2500, boxes 2500, certified 2500, uncertified 0' in c0 and 'VERIFIED-D4 (theta = 0)' in c0, 'cert0'
cols = sorted(glob.glob(os.path.join(logd, 'col*.out')))
assert len(cols) == 55, f'{len(cols)} columns'
roots = 0; hashes = set(); unc_roots = set(); totals = set()
for f in cols:
    t = open(f).read()
    h = re.findall(r'# zmx2 cert hash=(\S+) mode=d4 atoms=grid\+fo depth=40 ', t); assert h, f'settings {f}'
    hashes |= set(h)
    m = re.search(r'done in \S+ wall: roots (\d+) \(missing 0\)', t); assert m, f'unfinished {f}'
    roots += int(m.group(1))
    totals |= set(re.findall(r'total (\d+/\d+)', t))
    unc_roots |= {int(r) for r in re.findall(r'^UNCERT (\d+) ', t, re.M)}
cov = {int(re.search(r'r(\d+)\.out', os.path.basename(f)).group(1)) for f in glob.glob(os.path.join(covd, 'r*.out'))}
covh = set()
for f in glob.glob(os.path.join(covd, 'r*.out')):
    with open(f) as fh:
        for line in fh:
            m = re.match(r'# zmx2 cert hash=(\S+) (mode=d4 atoms=grid\+fo depth=40 node_cap=20000000) ', line)
            if line.startswith('# zmx2 cert'): covh.add(m.group(1) if m else 'WRONG-SETTINGS:' + line.strip()); break
print(f'cover hashes of the cov/ dumps (same settings: d4, first-order, depth 40, node cap 2e7): {sorted(covh)}')
print(f'cert0: 2,500 roots VERIFIED; columns 55, roots {roots}, cover hash {sorted(hashes)}, totals {sorted(totals)}')
print(f'roots with uncertified boxes: {len(unc_roots)}; tight-tile roots dumped: {len(cov)}; other: {sorted(unc_roots - cov)}')
ok = roots == 12100 and len(hashes) == 1 and totals == {'28909433072241/250000000000'} and unc_roots == cov | {9632} and len(cov) == 75 and covh == hashes
print('ZMX2-AUDIT-OK' if ok else 'ZMX2-AUDIT-NOT-OK')
