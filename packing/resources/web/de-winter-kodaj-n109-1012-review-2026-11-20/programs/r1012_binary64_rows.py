"""Lane r1012: read binary64 Kaggle rows of one count exactly, as a Witness/v2 corners file.

Usage: r1012_binary64_rows.py CSV EXPECTED_SHA256 N OUT.yaml OUT.json

Written after the findings' freeze, to measure Samanyu-dev's 109 (best_fit_101_500.csv
at Samanyu-dev/squares_in_squares 53551d7) with this repository's tools, which read a
corners witness. It decides nothing. Each row id,n,square_id,x,y,angle (angle in
radians) is read exactly as the binary64 values its decimals name; each square's turn
is the exact rotation whose half-angle tangent is the binary64 value of tan(angle / 2),
so that its edges are exactly unit; the packing is translated, exactly, so that its
least corner coordinates are 0, and the side is its exact extent, the larger of width
and height. The rows' order is kept, and the ids are 1 to n, as this repository's witness-corners
adapter reads them.
"""

import csv
import hashlib
import io
import json
import math
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)

import r1012_writer  # noqa: E402


def main(argv):
    path, expected, n, out_yaml, out_json = argv[1], argv[2], int(argv[3]), argv[4], argv[5]
    with open(path, "rb") as handle:
        data = handle.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected:
        print(f"digest {digest} != {expected}")
        return 2
    rows = [r for r in csv.DictReader(io.StringIO(data.decode("utf-8"))) if int(r["n"]) == n]
    rows.sort(key=lambda r: int(r["square_id"]))
    if [int(r["square_id"]) for r in rows] != list(range(n)):
        print("square ids are not 0 .. n-1")
        return 2
    quads = []
    for r in rows:
        x, y, a = F(float(r["x"])), F(float(r["y"])), float(r["angle"])
        t = F(math.tan(a / 2))
        e = ((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t))
        f = (-e[1], e[0])
        h = F(1, 2)
        quads.append([
            (x - h * e[0] - h * f[0], y - h * e[1] - h * f[1]),
            (x + h * e[0] - h * f[0], y + h * e[1] - h * f[1]),
            (x + h * e[0] + h * f[0], y + h * e[1] + h * f[1]),
            (x - h * e[0] + h * f[0], y - h * e[1] + h * f[1]),
        ])
    min_x = min(p[0] for q in quads for p in q)
    min_y = min(p[1] for q in quads for p in q)
    quads = [[(p[0] - min_x, p[1] - min_y) for p in q] for q in quads]
    width = max(p[0] for q in quads for p in q)
    height = max(p[1] for q in quads for p in q)
    side = max(width, height)
    ids = list(range(1, n + 1))
    text = r1012_writer.write(n, side, ids, quads)
    with open(out_yaml, "wb") as handle:
        handle.write(text)
    receipt = {
        "program": "r1012_binary64_rows.py",
        "csv": os.path.basename(path),
        "csv_sha256": digest,
        "n": n,
        "translation": [f"{float(-min_x):.6e}", f"{float(-min_y):.6e}"],
        "width": f"{width.numerator}/{width.denominator}",
        "height": f"{height.numerator}/{height.denominator}",
        "side_exact": f"{side.numerator}/{side.denominator}",
        "side_float": repr(float(side)),
        "witness_sha256": hashlib.sha256(text).hexdigest(),
    }
    with open(out_json, "w", encoding="utf-8") as handle:
        json.dump(receipt, handle, indent=1)
        handle.write("\n")
    print(f"wrote {n} squares, side {float(side)!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
