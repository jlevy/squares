#!/usr/bin/env python3
"""job list for the tight-tile certification: one job = all charts of one line s_b, or of one strip between lines"""
from fractions import Fraction as F
RANGES = {  # d0: list of (s_lo, s_hi) in tenths, inclusive line indices
    '1.5': [(14, 17), (24, 27), (33, 55)],
    '2.5': [(14, 17), (23, 27), (33, 37), (38, 55)],
    '3.5': [(14, 17), (23, 27), (33, 37), (41, 45)],   # s >= 3.3 uses the Lebesgue area term (ttarea.py)
}
jobs = []
for d0, rs in RANGES.items():
    for sign in (1, -1):
        lines = sorted({j for a, b in rs for j in range(a, b+1)})
        for j in lines:
            jobs.append(f'{d0} {sign} line {j/10:.1f}')
            if j+1 in lines: jobs.append(f'{d0} {sign} strip {j/10:.1f}+ {(j+1)/10:.1f}-')
print('\n'.join(jobs))
