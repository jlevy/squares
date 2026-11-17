#!/usr/bin/env python3
"""Figure: the measure mu_11 of the 11 x 11 board (left) and a zoom on one corner (right).
Segment colour = linear density (mass per unit length, log scale; segments below 1e-3 omitted);
grey = Lebesgue measure on U_11.
usage: make_board_figure.py ../../certificate/sol_exact_box11.txt board.pdf"""
import sys, math
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle
src, out = sys.argv[1], sys.argv[2]
L = open(src).read().split('\n'); i = 0
while not L[i].split() or L[i].startswith('#') or L[i].startswith('mixed'): i += 1
pitch = int(L[i+1]); wden = int(L[i+2]); n = int(L[i+4])
segs, dens = [], []
for j in range(n):
    x0, y0, x1, y1, w = map(int, L[i+5+j].split())
    length = math.hypot(x1 - x0, y1 - y0) / pitch
    segs.append([(x0/pitch, y0/pitch), (x1/pitch, y1/pitch)]); dens.append(w / wden / length)
keep = [k for k in range(n) if dens[k] >= 1e-3]                 # lighter segments omitted for clarity
order = sorted(keep, key=lambda k: dens[k])           # draw heavy segments on top
segs = [segs[k] for k in order]; dens = [dens[k] for k in order]
norm = LogNorm(vmin=1e-3, vmax=max(dens))
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.6), gridspec_kw=dict(width_ratios=[1, 1]))
for ax, lim, lw in ((axs[0], (0, 11), 0.6), (axs[1], (0, 5.5), 1.4)):
    ax.add_patch(Rectangle((3.8, 3.8), 3.4, 3.4, color='0.85', lw=0, zorder=0))
    lc = LineCollection(segs, array=[max(d, 1e-3) for d in dens], cmap='viridis_r', norm=norm, linewidths=lw)
    ax.add_collection(lc)
    ax.add_patch(Rectangle((0, 0), 11, 11, fill=False, lw=0.8, color='k'))
    ax.set_xlim(lim); ax.set_ylim(lim); ax.set_aspect('equal')
    ax.tick_params(labelsize=7)
axs[0].add_patch(Rectangle((0, 0), 5.5, 5.5, fill=False, lw=0.8, ls='--', color='tab:red'))
axs[0].set_title(r'$\mu_{11}$ on $[0,11]^2$', fontsize=9); axs[1].set_title(r'zoom on $[0,5.5]^2$', fontsize=9)
for v in (4,): axs[1].axvline(v, color='tab:red', lw=0.6, ls=':'); axs[1].axhline(v, color='tab:red', lw=0.6, ls=':')
cb = fig.colorbar(lc, ax=axs, shrink=0.8, pad=0.02); cb.set_label('mass per unit length', fontsize=8); cb.ax.tick_params(labelsize=7)
fig.savefig(out, bbox_inches='tight')
print('wrote', out, len(segs), 'of', n, 'segments drawn; max density', max(dens))
