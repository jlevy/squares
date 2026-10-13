#!/usr/bin/env python3
"""The two outputs (Evan 10-10): best-choice list and alternates list.  REGULARIZE.md.

  best      per n: the chosen regularized packing (variant, level, groups, proposed orientation vs the source drawing
            = jlevy's), from runs/regularize/poster/{conservative,fewest}/.  Rule: fewest rotation groups among the
            verified variants; ties -> conservative (same packing as the source).  --alternates-as-best no|yes: may a
            level-3 (alternate) variant be the best choice?
  alternates  packings at the record side that are truly distinct (not container symmetry, not rattlers only):
            ours (level-3 variants) and Ellsworth's catalogue (site/www/data), compared with the record.

Writes search/regularize/lists/{best,alternates}.{md,json,csv} and lists/certs/ (gzipped certificate + 50-digit JSON of
every chosen packing; certs/alt/ for our alternates).  Check a certificate: gunzip, then search/exact/verify_cert.py.
"""
import argparse, csv, glob, json, math, os, sys
import numpy as np
from scipy.optimize import linear_sum_assignment
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
POSTER = os.path.join(ROOT, 'runs', 'regularize', 'poster')
OUT = os.path.join(HERE, 'lists')
ORIENT = {0: 'as source', 1: 'rotated 90° anticlockwise', 2: 'rotated 180°', 3: 'rotated 90° clockwise',
          4: 'mirrored left-right', 5: 'reflected in the main diagonal', 6: 'mirrored top-bottom',
          7: 'reflected in the anti-diagonal'}
LEVEL = {0: 'identical', 1: 'rattlers only', 2: 'same packing (traversable without expansion)',
         3: 'alternate packing (not shown connected)'}


def load_variant(pol, n):
    f = os.path.join(POSTER, pol, f'n-{n:03d}.json')
    return json.load(open(f)) if os.path.exists(f) else None


def best(alt_as_best):
    import reg
    res = {r['n']: r for r in json.load(open(os.path.join(ROOT, 'search', 'exact', 'batch', 'results.json')))}
    rows = []
    for n in range(1, 325):
        cands = []
        for pol in ('conservative', 'fewest'):
            d = load_variant(pol, n)
            if d and d['cert_valid'] and d['verify_80']['ok'] and (alt_as_best or d['level'] < 3):
                cands.append((d['groups_after'], pol != 'conservative', pol, d))
        cands.sort(key=lambda z: (z[0], z[1]))
        g, _, pol, d = cands[0]
        inp = d['input']
        src = 'store best (refreshed)' if inp and 'runs/regularize' in str(inp) else 'exact batch (register witness)'
        rows.append(dict(n=n, side=d['S_exact'][:22], finder=', '.join(d['by'] or []) or '-', variant=pol,
                         level=d['level'], level_text=LEVEL[d['level']], groups=f"{d['groups_before']} -> {d['groups_after']}",
                         orientation_g=d['orientation_g'], orientation=ORIENT[d['orientation_g']], shape=d['shape'],
                         symmetry=d['symmetry'], input=src, cert=f'runs/regularize/poster/{pol}/n-{n:03d}.cert'))
    return rows


def catalogue_alternates():
    """Ellsworth's catalogue (site data): packings at the minimal catalogued side other than the main one, compared with
    our record input (8 symmetries x assignment on the record's force-carrying squares)."""
    import reg
    D = os.path.join(ROOT, 'site', 'www', 'data')
    F = json.load(open(os.path.join(D, 'index.json')))['files']
    byn = {}
    for k, v in F.items():
        if v.get('origin'):                # the site's own entries (our lists, history steps): not the catalogue
            continue
        try:
            s = float(v['s'])
        except Exception:
            continue
        if v.get('n') and v['n'] <= 324:
            byn.setdefault(v['n'], []).append((s, k))
    out = []
    for n, L in sorted(byn.items()):
        P = reg.load(n)
        S = float(P['S'])
        same = [k for s, k in L if abs(s - S) < 1e-7]
        if len(same) < 2 and not (len(same) == 1 and n in ()):
            continue
        rigid = [i for i in range(n) if i not in P['free']]
        PX = np.array([float(v) for v in P['X']]); PY = np.array([float(v) for v in P['Y']])
        PT = np.array([float(v) for v in P['T']])
        for k in same:
            pj = os.path.join(D, 'p', k.replace('.svg', '.json'))
            if not os.path.exists(pj):
                continue
            q = json.load(open(pj))
            sq = q['squares']
            Q = dict(n=n, S=P['S'], X=[x for x, y, t in sq], Y=[y for x, y, t in sq], T=[reg.fold(t) for x, y, t in sq], free=[])
            best_dev = None
            for g in range(8):
                Qg = reg.d4(Q, g)
                QX = np.array([float(v) for v in Qg['X']]); QY = np.array([float(v) for v in Qg['Y']])
                QT = np.array([float(v) for v in Qg['T']])
                C = np.hypot(PX[rigid][:, None] - QX[None, :], PY[rigid][:, None] - QY[None, :])
                dT = np.abs(((PT[rigid][:, None] - QT[None, :]) + 45) % 90 - 45)
                C = C + 10 * (dT > 1e-4)
                r, c = linear_sum_assignment(C)
                dev = float(C[r, c].max())
                if best_dev is None or dev < best_dev[0]:
                    best_dev = (dev, g)
            if best_dev[0] < 1e-4:
                rel = 'same as the record up to symmetry / rattlers'
            elif best_dev[0] < 10:
                rel = 'same tilts, squares placed differently (perhaps the same packing via flat motions; not tested)'
            else:
                rel = 'distinct: different tilt structure'
            out.append(dict(n=n, source=f'Ellsworth catalogue {k}', side=f'{S:.12f}', relation=rel,
                            max_dev=round(best_dev[0], 6), g=best_dev[1], attribution=(F[k].get('prose') or '').replace('\n', ' ')[:120]))
    return out


def ours_alternates():
    out = []
    for f in sorted(glob.glob(os.path.join(POSTER, 'fewest', 'n-*.json'))):
        d = json.load(open(f))
        if d['level'] == 3:
            out.append(dict(n=d['n'], source='ours (fewest rotation groups variant)', side=d['S_exact'][:22],
                            relation=d['level_text'], groups=f"{d['groups_before']} -> {d['groups_after']}",
                            parent=', '.join(d['by'] or []), cert=os.path.relpath(f.replace('.json', '.cert'), ROOT)))
    return out


def write(rows, stem, cols, title, intro):
    os.makedirs(OUT, exist_ok=True)
    json.dump(rows, open(os.path.join(OUT, stem + '.json'), 'w'), indent=1, ensure_ascii=False)
    with open(os.path.join(OUT, stem + '.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(rows)
    with open(os.path.join(OUT, stem + '.md'), 'w') as fh:
        fh.write(f'# {title}\n\n{intro}\n\n| ' + ' | '.join(cols) + ' |\n|' + '---|' * len(cols) + '\n')
        for r in rows:
            fh.write('| ' + ' | '.join(str(r.get(c, '')) for c in cols) + ' |\n')


def _gz(src, dst):
    """gzip src to dst, deterministically (mtime 0), and only if the content changed: rewriting identical certificates
    would change every .gz in git through the timestamp gzip embeds."""
    import gzip
    data = open(src, 'rb').read()
    if os.path.exists(dst):
        try:
            if gzip.decompress(open(dst, 'rb').read()) == data:
                return
        except OSError:
            pass
    with open(dst, 'wb') as fo, gzip.GzipFile(filename='', mode='wb', compresslevel=9, fileobj=fo, mtime=0) as gz:
        gz.write(data)


def package(B, A):
    """Copy the chosen packings (certificate + 50-digit JSON, gzipped) into lists/certs/ and point the lists there."""
    cdir = os.path.join(OUT, 'certs'); adir = os.path.join(cdir, 'alt')
    os.makedirs(adir, exist_ok=True)
    for r in B:
        src = os.path.join(ROOT, r['cert'])
        for ext in ('.cert', '.json'):
            _gz(src.replace('.cert', ext), os.path.join(cdir, f"n-{r['n']:03d}{ext}.gz"))
        r['cert'] = os.path.relpath(os.path.join(cdir, f"n-{r['n']:03d}.cert.gz"), ROOT)
    for r in A:
        if r.get('cert') and r['source'].startswith('ours'):
            src = os.path.join(ROOT, r['cert'])
            for ext in ('.cert', '.json'):
                _gz(src.replace('.cert', ext), os.path.join(adir, f"n-{r['n']:03d}{ext}.gz"))
            r['cert'] = os.path.relpath(os.path.join(adir, f"n-{r['n']:03d}.cert.gz"), ROOT)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--alternates-as-best', default='no', choices=['no', 'yes'])
    a = ap.parse_args()
    B = best(a.alternates_as_best == 'yes')
    A = ours_alternates() + catalogue_alternates()
    A.sort(key=lambda r: (r['n'], r['source']))
    package(B, A)
    write(B, 'best', ['n', 'side', 'finder', 'variant', 'level', 'level_text', 'groups', 'orientation', 'shape',
                      'symmetry', 'input', 'cert'],
          'Best-choice packings (display), n = 1..324',
          'Generated by `search/regularize/lists.py` (REGULARIZE.md).  Every packing is certified at the record side '
          '(rational certificate, two independent checkers).  Orientation is relative to the source drawing (= jlevy\'s '
          'atlas).  Rule: fewest rotation groups; ties -> the conservative variant (same packing as the source); '
          f"alternates as best choice: {a.alternates_as_best}.")
    write(A, 'alternates', ['n', 'source', 'side', 'relation', 'groups', 'parent', 'max_dev', 'attribution', 'cert'],
          'Alternate packings at the record side',
          'Ours: level-3 variants (merging determined angles gives a packing at the record side not shown connected to '
          'the source).  Catalogue: Ellsworth\'s drawings at the same side, compared with the record (8 symmetries, '
          'force-carrying squares matched; max_dev = worst centre mismatch).')
    import collections
    print('best:', collections.Counter(r['variant'] for r in B), collections.Counter(r['level'] for r in B))
    print('alternates:', collections.Counter((r['source'].split()[0], r['relation']) for r in A))


if __name__ == '__main__':
    main()
