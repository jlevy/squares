#!/usr/bin/env python3
"""Read jlevy register data (local clone; data only, CC BY 4.0, Joshua Levy, the squares project) into our formats.

  register.py table                 -> candidates: Ellsworth "not yet analytically optimized" + register newer than mirror
  register.py witness N out.txt     -> known-best witness for n = N in our text format (n s / x y deg)
"""
import json, math, os, re, sys
import yaml

CLONE = os.path.expanduser('~/math/_untrusted-third-party/jlevy-squares/packing')
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '../../../site/data')


def frontier(n):
    p = _path('frontier', n, 'md')
    if p is None:
        return None
    txt = open(p).read()
    fm = yaml.safe_load(txt.split('---')[1])['packing']
    rep = (fm.get('reported_upper_bound') or {})
    ver = (fm.get('verified_upper_bound') or {})
    return dict(reported=rep.get('value'), verified=ver.get('value'), by=rep.get('found_by'),
                analytic=rep.get('analytically_optimized'), witnesses=rep.get('witnesses') or [], status=fm.get('status'))


FRESH = os.path.join(HERE, 'regnow')   # files fetched from GitHub after the clone (gh api; data only); checked first


def _path(sub, n, ext):
    for name in (f'n-{n:03d}.{ext}', f'n-{n}.{ext}'):
        for p in (f'{FRESH}/{sub}/{name}',
                  f'{CLONE}/{sub}/{name}' if sub == 'frontier' else f'{CLONE}/witnesses/known-best/{name}'):
            if os.path.exists(p):
                return p
    return None


def witness(n):
    p = _path('known-best', n, 'yaml')
    w = yaml.safe_load(open(p))['witness']
    if w['representation'] == 'corners':
        from fractions import Fraction as F
        sq = []
        for q in w['squares']:
            P = [(F(str(a)), F(str(b))) for a, b in q['corners']]
            cx, cy = sum(p[0] for p in P) / 4, sum(p[1] for p in P) / 4
            (x0, y0), (x1, y1) = P[0], P[1]
            assert abs(float((x1 - x0) ** 2 + (y1 - y0) ** 2) - 1) < 1e-9, 'not a unit edge'
            sq.append((float(cx), float(cy), math.atan2(float(y1 - y0), float(x1 - x0)) % (math.pi / 2)))
        assert len(sq) == n
        return float(F(str(w['side']))), sq, str(w['side'])
    unit = w['coordinates']['angle_unit']
    assert w['representation'] == 'center-angle' and unit in ('radians', 'degrees'), (w['representation'], unit)
    assert w['coordinates']['origin'] == 'lower-left'
    f = 1.0 if unit == 'radians' else math.pi / 180
    sq = [(float(q['center'][0]), float(q['center'][1]), f * float(q['angle'])) for q in w['squares']]
    assert len(sq) == n
    return float(w['side']), sq, w['side']


def mirror():
    """Ellsworth page (our 09-30 mirror): {n: (s, unoptimized flag)}"""
    import html
    s = open(f'{SITE}/ellsworth/squares_in_squares.html', encoding='utf-8').read()
    t = html.unescape(re.sub('<[^>]+>', ' ', s))
    ents = list(re.finditer(r'\s(\d{1,3})\s+\$s = \\Nn\{([\d.]+)\}', t))
    out = {}
    for k, m in enumerate(ents):
        end = ents[k + 1].start() if k + 1 < len(ents) else len(t)
        out[int(m.group(1))] = (float(m.group(2)), bool(re.search('(?i)not yet analytically', t[m.start():end])))
    # side values for every n from the mirror's SVGs (the regex above only parses part of the page)
    P = json.load(open(f'{SITE}/packings.json'))
    for v in P.values():
        n = v['n']
        if n not in out or float(v['s']) < out[n][0]:
            out[n] = (float(v['s']), out.get(n, (0, False))[1])
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'table':
        M = mirror()
        rows = []
        for n in range(1, 400):
            f = frontier(n)
            if f is None or f['reported'] is None:
                continue
            r = float(f['reported'])
            ms, unopt = M.get(n, (None, False))
            newer = ms is not None and r < ms - 1e-12
            if unopt or newer:
                has_w = _path('known-best', n, 'yaml') is not None
                rows.append(dict(n=n, register=f['reported'], verified=f['verified'], mirror=ms, unopt=unopt, newer=newer,
                                 by=f['by'], analytic=f['analytic'], witness=has_w))
        for r in rows:
            print(f"{r['n']:4d} reg {r['register']:<20} mirror {r['mirror']!s:<18} {'UNOPT' if r['unopt'] else '     '} "
                  f"{'NEWER' if r['newer'] else '     '} w={int(r['witness'])} analytic={r['analytic']} by={r['by']}")
        json.dump(rows, open(os.path.join(HERE, 'candidates.json'), 'w'), indent=1)
    elif sys.argv[1] == 'all':
        rows = []
        for n in range(1, 400):
            f = frontier(n)
            if f is None or f['reported'] is None or _path('known-best', n, 'yaml') is None:
                continue
            rows.append(dict(n=n, register=f['reported'], verified=f['verified'], by=f['by'], analytic=f['analytic'],
                             status=f['status']))
        json.dump(rows, open(os.path.join(HERE, 'candidates_all.json'), 'w'), indent=1)
        print(len(rows), 'records with witnesses; n range', rows[0]['n'], '-', rows[-1]['n'],
              '; missing n <= 324:', [n for n in range(1, 325) if n not in {r['n'] for r in rows}])
    elif sys.argv[1] == 'witness':
        n = int(sys.argv[2])
        s, sq, sstr = witness(n)
        with open(sys.argv[3], 'w') as f:
            f.write(f'{n} {sstr}\n')
            for x, y, t in sq:
                f.write(f'{x!r} {y!r} {math.degrees(t) % 90!r}\n')
