#!/usr/bin/env python3
"""Side-by-side drawings: source packing vs regularized variants (prototype; REGULARIZE.md).

Usage:  gallery.py N [N ...] [--variants yx,xy,sum,nosym,nomerge,o1] [--out DIR]
Writes DIR/n-N.png (one row: source as given, then each variant) and DIR/n-N.json (reports).
Colours: axis-parallel squares grey-green; each tilted display group its own hue (theta and -theta share a hue,
the negative one darker); free (force-free) squares get a dot; a square that moved gets a thin red outline.
"""
import argparse, json, math, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import mpmath as mpm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reg

VARIANTS = {
    'yx': dict(gravity='yx'), 'xy': dict(gravity='xy'), 'sum': dict(gravity='sum'),
    'nosym': dict(gravity='yx', sym='off'), 'nomerge': dict(gravity='yx', merge='off'),
    'o1': dict(gravity='yx', orient='1st-runner-up'),
    'pretty': dict(style='pretty'), 'coincide': dict(style='coincide'),
    'as-strip': dict(style='coincide', orient_kind='strip'), 'as-arc': dict(style='coincide', orient_kind='arc'),
    'as-source': dict(style='coincide', orient_kind='source'),
    'keep': dict(gravity='yx', keep='on'), 'keepxy': dict(gravity='xy', keep='on'),
}


PALETTE = {}          # |tilt| rounded -> hue index, shared by all panels of a row (reset per n)


def hue_for(t, tilts=None):
    import colorsys
    a = round(abs(float(t)), 7)
    if a not in PALETTE:
        PALETTE[a] = len(PALETTE)
    h = (0.08 + 0.61803 * PALETTE[a]) % 1.0
    l = 0.62 if float(t) > 0 else 0.45
    return colorsys.hls_to_rgb(h, l, 0.6)


def draw(ax, P, title, moved=(), free=()):
    S = float(P['S'])
    ax.add_patch(Polygon([(0, 0), (S, 0), (S, S), (0, S)], closed=True, fill=False, lw=1.2, ec='k'))
    tilts = [t for t in P['T']]
    for i, (x, y, t) in enumerate(zip(P['X'], P['Y'], P['T'])):
        x, y = float(x), float(y)
        c, s = reg.frame(t)
        pts = [(x + 0.5 * (c * a - s * b), y + 0.5 * (s * a + c * b)) for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
        fc = (0.80, 0.86, 0.78) if abs(float(t)) < 1e-12 else hue_for(t, tilts)
        ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=(0.85, 0.1, 0.1) if i in moved else (0.25, 0.25, 0.25),
                             lw=1.0 if i in moved else 0.4))
        if i in free:
            ax.plot([x], [y], 'o', ms=2.2, color='k')
    ax.set_xlim(-0.05 * S, 1.05 * S); ax.set_ylim(-0.05 * S, 1.05 * S)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(title, fontsize=7)


def run(n, variants, out):
    P0 = reg.load(n)
    PALETTE.clear()
    for r, m in reg.angle_groups(P0['T']):        # big groups get the first (most distinct) hues
        if abs(r) > 1e-12 and len(m) > 1:
            hue_for(r)
    cols = 1 + len(variants)
    fig, axs = plt.subplots(1, cols, figsize=(3.2 * cols, 3.6))
    draw(axs[0], P0, f'n={n} source ({", ".join(P0["by"])})\nS={float(P0["S"]):.10f}  groups {len(reg.angle_groups(P0["T"]))}',
         free=P0['free'])
    reps = {}
    for ax, v in zip(axs[1:], variants):
        kw = dict(VARIANTS[v])
        if kw.get('orient') == '1st-runner-up':
            ors = reg.orientations(P0)
            kw['orient'] = str(ors[1][0]) if len(ors) > 1 else 'best'
        try:
            P, R, rep = reg.regularize(n, **kw)
        except Exception as e:                       # prototype: show the failure in the panel
            ax.axis('off'); ax.set_title(f'{v}: {type(e).__name__}: {e}'[:80], fontsize=6); continue
        reps[v] = rep
        ok = 'OK' if rep['verify']['ok'] else 'FAIL'
        fs = rep.get('face_spread') or 0
        t = (f"{v}: g={rep['g']}{' TIE' if rep['orient_tie'] else ''} sym={rep['sym_imposed']}{' FACE %.2g' % fs if fs > 1e-6 else ''}\n"
             f"groups {rep['groups_before']}->{rep['groups_after']} moved {len(rep['moved'])} "
             f"max {rep['max_move']:.3g} contacts {rep['contacts_before']}->{rep['verify']['contacts']} {ok}")
        draw(ax, R, t, moved=set(rep['moved']), free=[])
    fig.tight_layout()
    fig.savefig(os.path.join(out, f'n-{n}.png'), dpi=130)
    plt.close(fig)
    json.dump(reps, open(os.path.join(out, f'n-{n}.json'), 'w'), default=str, indent=1)
    return reps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int, nargs='+')
    ap.add_argument('--variants', default='yx,xy,sum,nosym')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'runs', 'regularize'))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for n in a.n:
        run(n, a.variants.split(','), a.out)
        print('wrote', os.path.join(a.out, f'n-{n}.png'))


if __name__ == '__main__':
    main()
