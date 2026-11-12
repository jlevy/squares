"""Growth step: insert one row and one column into a packing of unit squares, then re-optimize.

Usage:
  python grow.py SEED X_CUT Y_CUT OUT.npz [N]

SEED is either an .npz file written by this script (arrays S and P) or a CSV file with the columns
id,n,i,x,y,theta (the layout of best_fit_101_500.csv in Samanyu-dev/squares_in_squares). For a CSV, N selects the
packing. OUT.npz holds the side S and the array P with one row (x, y, theta) per square.

The packing is cut along the lines x = X_CUT and y = Y_CUT. The parts are moved apart, the squares in the layer next
to each cut are copied once across it, and all squares are then optimized together (see surgery.py and nlp.py).
"""
import sys, csv
import numpy as np
import slp, surgery, nlp

def load(path, n=None):
    if path.endswith('.npz'):
        d = np.load(path); S, P = float(d['S']), d['P'].copy()
        P[:, 2] = surgery.nrm(P[:, 2]); return S, P
    rows = []
    with open(path) as f:
        r = csv.reader(f); next(r)
        for row in r:
            if int(row[1]) == n: rows.append((float(row[3]), float(row[4]), float(row[5])))
    P = np.array(rows)
    assert len(P) == n, 'packing with n = %s not found' % n
    if np.abs(P[:, 2]).max() > 3.2: P[:, 2] = np.radians(P[:, 2])       # angles given in degrees
    P[:, 2] = surgery.nrm(P[:, 2])
    X, Y, _, _ = slp.verts(P); x0, y0 = X.min(), Y.min()
    P[:, 0] -= x0; P[:, 1] -= y0
    return max(X.max() - x0, Y.max() - y0), P

if __name__ == '__main__':
    seed, xc, yc, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    n = int(sys.argv[5]) if len(sys.argv) > 5 else None
    S, P = load(seed, n)
    print('seed: %d squares, side %.12f' % (len(P), S))
    S2, P2, ny, nx = surgery.up_step(S, P, xc, yc)
    print('after the cut at x = %.2f, y = %.2f: %d squares (%d + %d added), box %.4f' % (xc, yc, len(P2), ny, nx, S2))
    v = slp.violation(S2, P2)
    if v > 2e-10:
        P2, v = slp.repair(S2, P2, tmax=20)
        assert v <= 2e-10, 'overlaps could not be removed (%.2e)' % v
    S3, P3, v3 = nlp.compact(S2, P2, tmax=120)
    assert v3 <= 0
    print('re-optimized: %d squares, side %.12f' % (len(P3), S3))
    np.savez(out, S=S3, P=P3)
