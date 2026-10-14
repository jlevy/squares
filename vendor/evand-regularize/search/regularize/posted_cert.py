#!/usr/bin/env python3
"""Certificate for a record drawn as posted (provenance 'raw': posted after the lists, or not certifiable by them), from
the poster's own exact certificate, converted without rounding.  Companion of register_cert.py (register witnesses).

Reads: our format (`n S` then rational `x y t`), `cert.json` (SQUISH, PingYou: `s_exact`, squares [x, y, t]) and
`.sqcert` (dostashev: `n N` / `s S` lines).  t = tan(theta/2) throughout.  --dilate multiplies centres and side by
1 + 1e-30: SQUISH certificates put the box at the exact extent (closed box, wall contacts exact), while our checkers
decide the open box; s(n) <= S(1 + d) for every d > 0 gives s(n) <= S.
Writes lists/certs/raw/n-NNN.cert.gz (deterministic gzip) after both exact checkers accept it.

  posted_cert.py FILE --label TEXT [--dilate]
"""
import argparse, gzip, json, os, subprocess, sys, tempfile
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(HERE, 'lists', 'certs', 'raw')
DILATE = 1 + F(1, 10 ** 30)


def load(path):
    txt = open(path).read()
    if txt.lstrip().startswith('{'):
        d = json.loads(txt)
        rows = [q[:3] if isinstance(q, list) else (q['x'], q['y'], q['t']) for q in d['squares']]
        return d['n'], F(str(d['s_exact'])), [tuple(F(str(v)) for v in r) for r in rows]
    L = [l.split() for l in txt.splitlines() if l.strip() and not l.startswith('#')]
    if L[0][0] == 'n':                                              # .sqcert
        assert L[1][0] == 's'
        n, S, rows = int(L[0][1]), F(L[1][1]), L[2:]
    else:
        n, S, rows = int(L[0][0]), F(L[0][1]), L[1:]
    return n, S, [tuple(F(v) for v in r[:3]) for r in rows[:n]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--label', required=True, help='where it was posted, e.g. "jlevy/squares#500, itsnaka/squish-certs@aeacc6c"')
    ap.add_argument('--dilate', action='store_true')
    a = ap.parse_args()
    n, S, sq = load(a.file)
    assert len(sq) == n, f'{len(sq)} squares, n = {n}'
    k = DILATE if a.dilate else 1
    head = [f'# n = {n}: posted certificate ({a.label}), {os.path.basename(a.file)}, converted exactly'
            + (f'; centres and side multiplied by 1 + 1e-30 (posted side {float(S):.15f}, closed box)' if a.dilate else ''),
            '# exact certificate: unit squares, centre (x, y), rotation (c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2)); check with verify_cert.py']
    text = '\n'.join(head) + f'\n{n} {S * k}\n' + ''.join(f'{x * k} {y * k} {t}\n' for x, y, t in sq)
    with tempfile.NamedTemporaryFile('w', suffix='.cert', delete=False) as fh:
        fh.write(text)
    for chk in ('verify_cert.py', 'verify_cert2.py'):
        r = subprocess.run([sys.executable, os.path.join(ROOT, 'search', 'exact', chk), fh.name], capture_output=True, text=True)
        print(n, chk, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
        if r.returncode != 0:
            sys.exit(f'n={n}: {chk} rejected the certificate')
    os.unlink(fh.name)
    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, f'n-{n:03d}.cert.gz')
    with open(dst, 'wb') as fo, gzip.GzipFile(filename='', mode='wb', compresslevel=9, fileobj=fo, mtime=0) as gz:
        gz.write(text.encode())
    print('wrote', os.path.relpath(dst, ROOT))


if __name__ == '__main__':
    main()
