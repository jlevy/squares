"""A226 pages (docs/residue_map/campaigns/A226-one-flush/), every panel geometry-checked from the results files:
  survey_small.svg / survey_mid.svg / survey_large.svg -- the record packings below ceil(sqrt n) with their corner
      status (F = flush, k = number of meeters of the open unit corner box; flush corner squares green, meeters of a
      doubly-met corner red, other tilted squares blue, flat grey);
  crowd_above.svg  -- Proposition CROWD-ABOVE: four-crowds at side S = s + (ceil - s)/2 built from the corner dominoes
      of the n = 29 and n = 55 records, with a zoom of one crowded corner;
  ring11.svg       -- n = 11: the eight-square crowd ring at S = 3.95 and the free region's capacity (one square).
    python pages226.py
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from svg226 import square_corners, verify_packing  # noqa: E402
from survey226 import corner_status, CORNERS  # noqa: E402

ATT = os.path.abspath(os.path.join(HERE, '..'))
PAGES = os.path.join(ATT, '..', '..', 'docs', 'residue_map', 'campaigns', 'A226-one-flush')
os.makedirs(PAGES, exist_ok=True)
GREEN = ('#d9f2d9', '#2e7d32')
RED = ('#f8d0d0', '#c62828')
BLUE = ('#dbe9f6', '#1f4e79')
GREY = ('#eeeeee', '#888888')


def load(path):
    return [json.loads(l) for l in open(path, encoding='utf-8')]


def panel(sq, s, x0, y0, size, title, note, zoom=None, labels=False):
    """one packing at scale size/s (or a zoomed window zoom = (u0, v0, w) in container coords)."""
    cs = corner_status(sq, s)
    meet_red = set()
    for c in CORNERS:
        if cs[c]['n_meet'] >= 2:
            meet_red |= {m['i'] for m in cs[c]['meeters']}
    flush = {m['i'] for c in CORNERS for m in cs[c]['meeters'] if m['flush']}
    if zoom is None:
        u0, v0, w = 0.0, 0.0, s
    else:
        u0, v0, w = zoom
    k = size / w

    def P(x, y):
        return (x0 + (x - u0) * k, y0 + size - (y - v0) * k)
    out = ['<clipPath id="clip%d_%d"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath>' % (
        int(x0), int(y0), x0, y0, size, size)]
    out.append('<g clip-path="url(#clip%d_%d)">' % (int(x0), int(y0)))
    for i, (x, y, th) in enumerate(sq):
        tilt = min(th % (math.pi / 2), math.pi / 2 - th % (math.pi / 2))
        col = RED if i in meet_red else GREEN if i in flush else BLUE if tilt > 1e-7 else GREY
        pts = ' '.join('%.2f,%.2f' % P(*q) for q in square_corners(x, y, th))
        out.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="1"/>' % (pts, col[0], col[1]))
        if labels:
            cx, cy = P(x, y)
            out.append('<text x="%.1f" y="%.1f" font-size="10" text-anchor="middle" fill="#222">%d</text>' % (cx, cy + 3, i))
    out.append('</g>')
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="#333" stroke-width="1.4"/>' % (
        x0, y0, size, size))
    if zoom is None:
        for c, (ax, ay, dx, dy) in zip(CORNERS, ((0, 0, 14, -6), (1, 0, -14, -6), (1, 1, -14, 14), (0, 1, 14, 14))):
            px, py = x0 + ax * size + dx, y0 + (1 - ay) * size + dy
            lab = 'F' if cs[c]['flush'] else str(cs[c]['n_meet'])
            colr = GREEN[1] if cs[c]['flush'] else RED[1] if cs[c]['n_meet'] >= 2 else '#555'
            out.append('<text x="%.1f" y="%.1f" font-size="13" font-weight="bold" text-anchor="middle" fill="%s">%s</text>' % (
                px, py, colr, lab))
    out.append('<text x="%.1f" y="%.1f" font-size="12" font-weight="bold" fill="#222">%s</text>' % (x0, y0 - 18, title))
    out.append('<text x="%.1f" y="%.1f" font-size="9.5" fill="#444">%s</text>' % (x0, y0 - 6, note))
    return '\n'.join(out), cs


def page(name, width, height, header, body):
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Helvetica,Arial,sans-serif">' % (
        width, height), '<rect width="%d" height="%d" fill="white"/>' % (width, height),
        '<text x="12" y="22" font-size="14" font-weight="bold" fill="#222">%s</text>' % header] + body + ['</svg>']
    with open(os.path.join(PAGES, name), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(svg))
    print('wrote', name)


def survey_pages():
    rows = [r for r in load(os.path.join(ATT, 'results', 'survey226.jsonl')) if r['label'] != 'trump_cert']
    groups = [('survey_small.svg', [r for r in rows if r['n'] <= 19], 3),
              ('survey_mid.svg', [r for r in rows if 26 <= r['n'] <= 41], 3),
              ('survey_large.svg', [r for r in rows if r['n'] >= 50], 3)]
    for name, grp, cols in groups:
        size, gx, gy = 250, 300, 310
        nrow = (len(grp) + cols - 1) // cols
        body = []
        for j, r in enumerate(grp):
            sq = [tuple(q) for q in r['squares']]
            gap = verify_packing(sq, r['side'])
            x0, y0 = 30 + (j % cols) * gx, 70 + (j // cols) * gy
            title = 'n = %d, s = %.6f < %d = ceil(sqrt n)  [%s]' % (r['n'], r['side'], r['ceil_sqrt'], r['source'])
            note = 'check: %d squares in [0,s]^2, min SAT gap %.1e (>= -1e-9), corners BL BR TR TL = %s, %d flush, %d tilted' % (
                r['n'], gap, r['pattern'], r['flush_corners'], r['n_tilted'])
            p, _ = panel(sq, r['side'], x0, y0, size, title, note)
            body.append(p)
        header = ('A226 -- the record packings below ceil(sqrt n) and their corners: F = flush (green slot square), '
                  'k = meeters of the open unit corner box (red when >= 2); blue = tilted, grey = flat.  '
                  'Source: Ellsworth, Squares in Squares (2026-09-14).')
        page(name, 30 + cols * gx, 70 + nrow * gy, header, body)


def crowd_page():
    rows = {r['n']: r for r in load(os.path.join(ATT, 'results', 'crowd226.jsonl')) if 'S' in r}
    body = []
    for j, n in enumerate((29, 55)):
        r = rows[n]
        sq, S = [tuple(q) for q in r['squares']], r['S']
        gap = verify_packing(sq, S)
        cs = corner_status(sq, S)
        x0, y0 = 30 + j * 620, 70
        title = 'n = %d four-crowd at S = %.6f < %d (record %.6f + w = %.4f, eps = %.4f)' % (
            n, S, r['ceil_sqrt'], r['side'], r['w'], r['eps'])
        note = 'check: %d squares in [0,S]^2, min SAT gap %.1e; meeters per corner BL BR TR TL = %s' % (
            n, gap, ' '.join(str(cs[c]['n_meet']) for c in CORNERS))
        p, _ = panel(sq, S, x0, y0, 360, title, note)
        body.append(p)
        d = cs['BL']['meeters']
        zt = 'BL corner zoomed (window [0, 2.4]^2): meeters #%d depth %.4f, #%d depth %.4f' % (
            d[0]['i'], d[0]['depth'], d[1]['i'], d[1]['depth'])
        zn = 'A slid up by eps = %.4f; B tilted by eps/2 = %.3f deg, its vertex pokes into the strip under A; the corner point is bare' % (
            r['eps'], math.degrees(r['eps'] / 2))
        p, _ = panel(sq, S, x0 + 390, y0, 200, zt, zn, zoom=(0.0, 0.0, 2.4))
        body.append(p)
        # the open corner box in the zoom
        k = 200 / 2.4
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="#c62828" stroke-dasharray="4,3" stroke-width="1.2"/>' % (
            x0 + 390, y0 + 200 - k, k, k))
    header = ('A226 -- Proposition CROWD-ABOVE: from a record with a corner DOMINO at every corner, a packing at every larger side '
              'with all four corner boxes doubly met (red = the eight meeters); STUCK(n) for ALL packings below ceil(sqrt n) is false.')
    page('crowd_above.svg', 1270, 470, header, body)


def ring_page():
    rows = load(os.path.join(ATT, 'results', 'ring11_226.jsonl'))
    r = next(x for x in rows if abs(x['S'] - 3.95) < 1e-9 and abs(x['eps'] - 0.05) < 1e-9)
    ring = [tuple(q) for q in r['ring']]
    S = r['S']
    gap = verify_packing(ring, S)
    title = 'n = 11: the eight-square crowd ring at S = %.2f, eps = %.2f (floor / wall variants alternating)' % (S, r['eps'])
    note = 'check: 8 squares in [0,S]^2, min SAT gap %.1e, meeters BL BR TR TL = %s; region search for 3 more: %s (greedy fits %d)' % (
        gap, r['ring_pattern'], 'FOUND' if r['found3'] else 'not found', r['k_max_greedy'])
    p, _ = panel(ring, S, 30, 70, 400, title, note, labels=True)
    body = [p]
    y = 70
    for x in rows:
        body.append('<text x="470" y="%d" font-size="11" fill="#222">S = %.2f, eps = %.2f: ring ok (gap %.0e), 3 interior squares %s; greedy max %d; best penalty %.1e</text>' % (
            y, x['S'], x['eps'], x['ring_gap'], 'found' if x['found3'] else 'NOT found', x['k_max_greedy'], x['best_penalty']))
        y += 18
    body.append('<text x="470" y="%d" font-size="11" fill="#444">The pinwheel left by the ring (a 1.9-box with four 0.9-wide stubs) holds one square: the construction that</text>' % (y + 10))
    body.append('<text x="470" y="%d" font-size="11" fill="#444">gives four-crowds below ceil(sqrt n) for n = 26 .. 55 gives NONE below 4 at n = 11 (A217: none below 4.0014).</text>' % (y + 26))
    header = 'A226 -- n = 11: the crowd ring below side 4 leaves no room for the three remaining squares (A222 region search, 40 restarts each).'
    page('ring11.svg', 1000, 500, header, body)


if __name__ == '__main__':
    survey_pages()
    crowd_page()
    ring_page()
