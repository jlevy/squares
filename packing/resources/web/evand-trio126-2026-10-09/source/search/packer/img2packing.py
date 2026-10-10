"""Recover a unit-square packing from a picture (black squares on white, thin light separators, square frame).

    python3 img2packing.py IMAGE X0 X1 Y0 Y1 SIDE OUT

Crops IMAGE to pixel box [Y0:Y1, X0:X1] (one panel, frame included), finds the frame (rows/columns > 30 % dark),
labels the black blobs (threshold 110, one erosion to cut separator lines), and for each blob of plausible size writes
its centre and the angle in [0, 90) that minimises its bounding-box area, in container units (frame -> [0, SIDE]²,
y up).  Output: the usual packer text format (n S, then x y angle_deg per square).  The result is only a start
(~0.02 error): finish with `fq quench` (loosen 1.0 / 1.02) and `exact/exactsolve.py`.

Used 10-08 for the 126 trio (`../trio126/README.md`).
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as nd


def extract(path, x0c, x1c, y0c, y1c, side, min_frac=0.45):
    im = np.asarray(Image.open(path).convert('L')).astype(float)
    sub = im[y0c:y1c, x0c:x1c]
    dark = sub < 200
    cols = np.where(dark.mean(0) > 0.3)[0]
    rows = np.where(dark.mean(1) > 0.3)[0]
    x0, x1, y0, y1 = cols[0], cols[-1], rows[0], rows[-1]
    sc = side / (((x1 - x0) + (y1 - y0)) / 2)          # container units per pixel
    lab, n = nd.label(nd.binary_erosion(sub < 110, iterations=1))
    out = []
    for k in range(1, n + 1):
        ys, xs = np.nonzero(lab == k)
        if len(xs) * sc * sc < min_frac:                # specks and separator fragments
            continue
        px, py = (xs - x0) * sc, (y1 - ys) * sc
        cx, cy = px.mean(), py.mean()
        best = None
        for t in np.arange(0, 90, 0.25):
            r = np.radians(t)
            u = (px - cx) * np.cos(r) + (py - cy) * np.sin(r)
            v = -(px - cx) * np.sin(r) + (py - cy) * np.cos(r)
            a = np.ptp(u) * np.ptp(v)
            if best is None or a < best[0]:
                best = (a, t)
        out.append((cx, cy, best[1], len(xs) * sc * sc))
    return out, (x1 - x0, y1 - y0)


def main():
    path, x0, x1, y0, y1, side, dst = sys.argv[1], *map(int, sys.argv[2:6]), float(sys.argv[6]), sys.argv[7]
    sq, frame = extract(path, x0, x1, y0, y1, side)
    big = max(a for *_, a in sq)
    tilted = sorted(round(t) for _, _, t, _ in sq if 2 < t < 88)
    print(f'{dst}: frame {frame[0]}x{frame[1]} px, {len(sq)} squares, largest blob {big:.2f} (merged blobs show '
          f'as > 1), tilted angles {tilted}')
    with open(dst, 'w') as f:
        print(len(sq), side, file=f)
        for cx, cy, t, _ in sq:
            print(f'{cx:.4f} {cy:.4f} {t:.2f}', file=f)


if __name__ == '__main__':
    main()
