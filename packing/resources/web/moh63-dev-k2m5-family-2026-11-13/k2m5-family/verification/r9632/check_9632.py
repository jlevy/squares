#!/usr/bin/env python3
"""Root 9632 closure check (exact).  zmx2 (dump.out, ZMX2_PRINT_ALL) leaves 6,850 uncertified sub-boxes in root 9632.
qx2_zm.py was run (zm.out) on the cropped cover c9632.txt over every qx2 root box meeting the window
W = [4.3224,4.3264] x [4.3199,4.3239] x u[0.0229,0.0272]; it certified all of it except 83 boxes (zm_unc.txt).
The root is closed if (1) every zmx2 uncertified box lies in W, (2) exactly one qx2 root meets W, so W lies in it, and
(3) no qx2-uncertified box meets any zmx2-uncertified box (closed boxes).  Then every pose of root 9632 is certified by
zmx2 or by qx2_zm.  (Cropping only drops segments, which can only lower masses, so a certificate for the cropped cover
is one for the full cover.)
usage: check_9632.py dump.out zm.out zm_unc.txt"""
import sys, re
from fractions import Fraction as F
dump, zmout, unc = sys.argv[1:4]
W = (F('4.3224'), F('4.3264'), F('4.3199'), F('4.3239'), F('0.0229'), F('0.0272'))
Z = [[F(t) for t in re.search(r'box (\S+) ', l).group(1).split(',')] for l in open(dump) if l.startswith('UNCERT')]
Q = [[F(x) for x in l.split()[:6]] for l in open(unc) if len(l.split()) >= 6]
txt = open(zmout).read()
argv_ok = all(s in txt for s in ('--cx-lo 4.3224', '--cx-hi 4.3264', '--cy-lo 4.3199', '--cy-hi 4.3239', '--u-lo 0.0229', '--u-hi 0.0272'))
one_root = ': 1 roots (PARTIAL)' in txt
n_unc = re.search(r'UNCERT (\d+)', txt.split('leaves:')[1]).group(1)
inW = all(W[0] <= z[0] and z[1] <= W[1] and W[2] <= z[2] and z[3] <= W[3] and W[4] <= z[4] and z[5] <= W[5] for z in Z)
meet = lambda a, b: all(max(a[2*i], b[2*i]) <= min(a[2*i+1], b[2*i+1]) for i in range(3))
hits = sum(1 for z in Z for q in Q if meet(z, q))
print(f'zmx2 uncertified boxes: {len(Z)}; all inside W: {inW}')
print(f'qx2_zm run on W: {argv_ok}; one qx2 root meets W: {one_root}; qx2 uncertified boxes: {len(Q)} (log says {n_unc})')
print(f'qx2-uncertified boxes meeting a zmx2-uncertified box: {hits}')
ok = inW and argv_ok and one_root and str(len(Q)) == n_unc and hits == 0 and len(Z) > 0
print('ROOT-9632-CLOSED' if ok else 'ROOT-9632-NOT-CLOSED')
