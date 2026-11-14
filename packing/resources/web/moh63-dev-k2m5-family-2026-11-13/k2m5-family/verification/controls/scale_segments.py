#!/usr/bin/env python3
"""Control cover: every segment mass of a mixed cover multiplied by p/q and rounded down (exact integers);
the Lebesgue square is left unchanged.  usage: scale_segments.py IN P Q OUT"""
import sys
src, p, q, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
L = open(src).read().split('\n'); i = 0
while not L[i].split() or L[i].startswith('#') or L[i].startswith('mixed'): i += 1
n = int(L[i+4]); o = L[:i] + [f'# CONTROL: every segment mass scaled by {p}/{q} (floor); Lebesgue square unchanged'] + L[i:i+5]
for j in range(n):
    t = L[i+5+j].split(); t[4] = str(int(t[4]) * p // q); o.append(' '.join(t))
o += L[i+5+n:]
open(out, 'w').write('\n'.join(o))
