"""Compare a report's two files as packings: square by square in file order, each
square's four corners as a set, in exact fractions.

Lane r127-1118.  Written for this review; imports only its own modules.

    python -I -B r127_twin.py FIRST SECOND --out OUT.json

SAME_PACKING when n and the side are equal and, for every k, square k of one file has
the same four corners as square k of the other.  It also reports, for each square, the
corner of the first file's listing at which the second file's listing starts and its
sense, which decides nothing.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script dir

import argparse
import hashlib
import json
import sys

import r127_read as R


def compare(p, q) -> dict:
    out: dict = {"n": [p.n, q.n], "side_equal": p.side == q.side}
    unequal = []
    starts: dict[str, int] = {}
    if p.n == q.n:
        for k in range(p.n):
            a, b = p.corners[k], q.corners[k]
            if set(a) != set(b):
                unequal.append(k + 1)
                continue
            start = a.index(b[0])
            sense = "same" if b[1] == a[(start + 1) % 4] else "reversed"
            key = f"from {start} {sense}"
            starts[key] = starts.get(key, 0) + 1
    out["unequal_squares"] = unequal[:50]
    out["unequal_count"] = len(unequal)
    out["listing"] = starts
    same = p.n == q.n and p.side == q.side and not unequal
    out["verdict"] = "SAME_PACKING" if same else "DIFFERENT"
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("first")
    ap.add_argument("second")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    p, q = R.read_path(a.first), R.read_path(a.second)
    res = compare(p, q)
    res["files"] = {f: hashlib.sha256(R.read_bytes(f)).hexdigest() for f in (a.first, a.second)}
    json.dump(res, open(a.out, "w"), indent=1)
    print(f"{a.first} vs {a.second}: {res['verdict']} unequal={res['unequal_count']} "
          f"listing={res['listing']}")
    return 0 if res["verdict"] == "SAME_PACKING" else 1


if __name__ == "__main__":
    sys.exit(main())
