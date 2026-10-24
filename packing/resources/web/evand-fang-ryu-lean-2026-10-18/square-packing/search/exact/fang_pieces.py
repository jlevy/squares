"""Lean certificates for the pieces of Fang's theorem (tasks/fang-gluing/): every rational certificate in
certificates/fang-gluing/inputs/ -> lean/Sqpack/Exact/Fang/<name>.lean (+ chunk dir), via lean_cert.py --cut.

Input: Evan Daniel's text format, line 1 `n S` (square) or `n W H` (rectangle), then `x y t` per square
(t = tan(theta/2)), exact rationals.  K = Q: f = T, t = 0.

  python3 search/exact/fang_pieces.py [NAME ...]        (default: all inputs)
then  lean/scripts/build_chunks.sh Sqpack.Exact.Fang.<NAME> 8
"""
import sys, os, json, glob, subprocess, tempfile
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INP = os.path.join(ROOT, 'certificates', 'fang-gluing', 'inputs')
OUT = os.path.join(ROOT, 'lean', 'Sqpack', 'Exact', 'Fang')


def read_cert(path):
    rows = [l.split() for l in open(path) if l.strip() and not l.lstrip().startswith('#')]
    n = int(rows[0][0])
    W = F(rows[0][1])
    H = F(rows[0][2]) if len(rows[0]) > 2 else None
    sq = [tuple(F(v) for v in r[:3]) for r in rows[1:n + 1]]
    assert len(sq) == n, path
    return n, W, H, sq


def to_json(n, W, sq):
    q = str
    return {'n': n, 'field': {'f': ['0', '1'], 't_interval': ['0', '0']},
            'squares': [{'x': [q(x)], 'y': [q(y)], 'u': [q(t)], 'm': 0} for x, y, t in sq],
            'S': {'in_K': [q(W)], 'poly': [q(-W), '1'], 'interval': [q(W), q(W)]}}


def main(names):
    os.makedirs(OUT, exist_ok=True)
    paths = sorted(glob.glob(os.path.join(INP, '*.cert')))
    if names:
        paths = [p for p in paths if os.path.basename(p)[:-5] in names]
    for p in paths:
        name = os.path.basename(p)[:-5]
        n, W, H, sq = read_cert(p)
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as fh:
            json.dump(to_json(n, W, sq), fh)
            js = fh.name
        cmd = [sys.executable, os.path.join(ROOT, 'search', 'exact', 'lean_cert.py'), js,
               os.path.join(OUT, name + '.lean'), '--split', '25', '--cut']
        if H is not None:
            cmd += ['--rect-h', str(H)]
        subprocess.run(cmd, check=True)
        os.unlink(js)


if __name__ == '__main__':
    main(sys.argv[1:])
