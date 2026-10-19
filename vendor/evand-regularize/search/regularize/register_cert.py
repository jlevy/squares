#!/usr/bin/env python3
"""Certificate from a jlevy/squares register witness, for records the lists could not certify themselves (REGULARIZE.md:
n = 261, where exactsolve's certificate at the exact optimum fails).

The register's known-best witnesses (Witness v2, center-basis, rational) carry exact unit rotations (c, s) with
c^2 + s^2 = 1, so t = s / (1 + c) is rational and the witness converts to our certificate format without rounding.
Writes lists/certs/raw/n-NNN.cert.gz (deterministic gzip) after both exact checkers accept it.

  register_cert.py N [N ...]      (witnesses from the store's register clone, search/packer/runs/jlevy)
"""
import gzip, os, subprocess, sys, tempfile
from fractions import Fraction as F
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
REG = os.path.join(ROOT, 'search', 'packer', 'runs', 'jlevy')
OUT = os.path.join(HERE, 'lists', 'certs', 'raw')


def convert(n):
    w = yaml.safe_load(open(os.path.join(REG, 'packing', 'witnesses', 'known-best', f'n-{n:03d}.yaml')))['witness']
    assert w['n'] == n and str(w.get('square_size', '1')) == '1' and w['representation'] == 'center-basis'
    sha = subprocess.run(['git', '-C', REG, 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()
    L = [f"# n = {n}: jlevy/squares register witness {w['id']} (@{sha}), converted exactly: t = s / (1 + c)",
         '# exact certificate: unit squares, centre (x, y), rotation (c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2)); check with verify_cert.py',
         f"{n} {w['side']}"]
    for q in w['squares']:
        c, s = map(F, q['basis'])
        x, y = map(F, q['center'])
        assert c * c + s * s == 1 and c != -1, f'square {q["id"]}: basis not an exact rational rotation'
        t = s / (1 + c)
        L.append(f'{x} {y} {t}')
    return '\n'.join(L) + '\n'


def main():
    os.makedirs(OUT, exist_ok=True)
    for n in map(int, sys.argv[1:]):
        text = convert(n)
        with tempfile.NamedTemporaryFile('w', suffix='.cert', delete=False) as fh:
            fh.write(text)
        for chk in ('verify_cert.py', 'verify_cert2.py'):
            r = subprocess.run([sys.executable, os.path.join(ROOT, 'search', 'exact', chk), fh.name],
                               capture_output=True, text=True)
            print(n, chk, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
            if r.returncode != 0:
                sys.exit(f'n={n}: {chk} rejected the certificate')
        os.unlink(fh.name)
        dst = os.path.join(OUT, f'n-{n:03d}.cert.gz')
        with open(dst, 'wb') as fo, gzip.GzipFile(filename='', mode='wb', compresslevel=9, fileobj=fo, mtime=0) as gz:
            gz.write(text.encode())
        print('wrote', os.path.relpath(dst, ROOT))


if __name__ == '__main__':
    main()
