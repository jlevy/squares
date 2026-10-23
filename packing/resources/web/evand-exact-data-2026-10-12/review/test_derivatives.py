"""Self-test of check_theorem_c.py's row derivatives against finite differences.

For every row of the given counts, the gradient and Hessian that check_theorem_c.py
derives in closed form are compared with central differences of the row function
h(z) evaluated from scratch in floating point (corner of j from its perturbed angle,
side normal of i from its perturbed angle).  It decides nothing about any packing;
it tests the formulas the checker uses.

  python -I test_derivatives.py --minpoly-dir DIR --archive gradec-233.tar.zst N [N ...]
"""
import argparse
import gzip
import json
import math
import os
import sys
import tarfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_theorem_c as C  # noqa: E402


def h_float(r, xs, ys, th, S):
    if r[0] == 'W':
        _, j, a, w = r
        s1, s2 = C.CORNERS[a]
        c, s = math.cos(th[j]), math.sin(th[j])
        px = xs[j] + 0.5 * (c * s1 - s * s2)
        py = ys[j] + 0.5 * (s * s1 + c * s2)
        return {'L': px, 'R': S - px, 'B': py, 'T': S - py}[w]
    _, j, a, i, k = r
    s1, s2 = C.CORNERS[a]
    c, s = math.cos(th[j]), math.sin(th[j])
    px = xs[j] + 0.5 * (c * s1 - s * s2)
    py = ys[j] + 0.5 * (s * s1 + c * s2)
    ex, ey = C.SIDES[k]
    ci, si = math.cos(th[i]), math.sin(th[i])
    nx, ny = ci * ex - si * ey, si * ex + ci * ey
    return nx * (px - xs[i]) + ny * (py - ys[i]) - 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--minpoly-dir', required=True)
    ap.add_argument('--archive', required=True)
    ap.add_argument('counts', nargs='+', type=int)
    a = ap.parse_args()
    worst_g = worst_h = 0.0
    nrows = 0
    with tarfile.open(a.archive, 'r:zst') as tf:
        for n in a.counts:
            ct = json.loads(tf.extractfile(f'gradec-233/certs/n-{n}.contacts.json').read())
            D = json.load(gzip.open(os.path.join(a.minpoly_dir, f'n-{n}.minpoly.json.gz'), 'rt'))
            rec = C.Record(D)
            K = rec.K
            xs = [K.to_float(x) for x in rec.X]
            ys = [K.to_float(y) for y in rec.Y]
            th = [math.atan2(K.to_float(s), K.to_float(c)) for c, s in zip(rec.C, rec.Sn)]
            S = K.to_float(rec.S)
            rows = [tuple(r) for r in ct['load_bearing']]
            lb = sorted({r[1] for r in rows} | {r[3] for r in rows if r[0] == 'C'})
            var = {}
            for i in lb:
                for key in ('x', 'y', 't'):
                    var[(key, i)] = len(var)
            var['S'] = len(var)
            inv = {v: k for k, v in var.items()}

            def h_at(r, dz):
                X, Y, T = list(xs), list(ys), list(th)
                s = S
                for c, e in dz.items():
                    key = inv[c]
                    if key == 'S':
                        s += e
                    elif key[0] == 'x':
                        X[key[1]] += e
                    elif key[0] == 'y':
                        Y[key[1]] += e
                    else:
                        T[key[1]] += e
                return h_float(r, X, Y, T, s)

            e = 1e-5
            for r in rows:
                nrows += 1
                g = {c: K.to_float(v) for c, v in C.row_grad(rec, r, var).items()}
                hh = {cc: K.to_float(v) for cc, v in C.row_hess(rec, r, var).items()}
                cols = sorted({var[('x', r[1])], var[('y', r[1])], var[('t', r[1])], var['S']}
                              | ({var[('x', r[3])], var[('y', r[3])], var[('t', r[3])]} if r[0] == 'C' else set()))
                for c in cols:
                    num = (h_at(r, {c: e}) - h_at(r, {c: -e})) / (2 * e)
                    worst_g = max(worst_g, abs(num - g.get(c, 0.0)))
                for x in range(len(cols)):
                    for y in range(x, len(cols)):
                        c1, c2 = cols[x], cols[y]
                        if c1 == c2:
                            num = (h_at(r, {c1: e}) - 2 * h_at(r, {}) + h_at(r, {c1: -e})) / e ** 2
                        else:
                            num = (h_at(r, {c1: e, c2: e}) - h_at(r, {c1: e, c2: -e})
                                   - h_at(r, {c1: -e, c2: e}) + h_at(r, {c1: -e, c2: -e})) / (4 * e * e)
                        worst_h = max(worst_h, abs(num - hh.get((c1, c2), 0.0)))
    print(json.dumps({'rows_tested': nrows, 'max_gradient_error': worst_g, 'max_hessian_error': worst_h}))
    ok = worst_g < 1e-6 and worst_h < 1e-3
    print('PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
