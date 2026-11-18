"""Price lane r1021-1118's jobs on a synthetic packing; reads no certificate.

Usage: python -I -B r1021_trial.py N DIGITS OUT.json

Builds N unit squares on a grid of pitch 21/20 with every centre a rational of
DIGITS-digit denominator and every direction a rational point of the unit circle
from a DIGITS-digit parameter (so its denominator has about 2*DIGITS digits), as the
certificates' are, then times method A, method B, the contraction and the identity
on it.  The receipt gives each job's CPU seconds and the pricing of the full run.
"""

from __future__ import annotations

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # this packet's programs/, run with -I

import json
import random
import sys
import time
from fractions import Fraction

import r1021_check as chk
import r1021_contract as con
import r1021_geom as geom
import r1021_identity as ident


def synthetic(n: int, digits: int, seed: int = 1118):
    rng = random.Random(seed)
    k = 1
    while k * k < n:
        k += 1
    q = 10**digits
    poses = []
    for idx in range(n):
        gx, gy = idx % k, idx // k
        x = Fraction(21 * gx, 20) + Fraction(rng.randrange(q // 40), q) + Fraction(3, 5)
        y = Fraction(21 * gy, 20) + Fraction(rng.randrange(q // 40), q) + Fraction(3, 5)
        if rng.random() < 0.5:
            c, s = Fraction(1), Fraction(0)
        else:
            t = Fraction(rng.randrange(q // 1000), q)  # a small angle: tan(theta/2) < 1e-3
            c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
        poses.append((x, y, c, s))
    side = Fraction(21 * k, 20) + Fraction(1, 5)
    return poses, side


def main(argv: list[str]) -> int:
    n, digits, out = int(argv[0]), int(argv[1]), argv[2]
    poses, side = synthetic(n, digits)
    rec: dict = {"n": n, "digits": digits}
    t0 = time.process_time()
    dec = chk.decide(poses, [geom.corners_of(p) for p in poses], side)
    rec["decide_accept"] = dec["accept"]
    rec["cpu_A"] = dec["cpu"]["A"]
    rec["cpu_B"] = dec["cpu"]["B"]
    t0 = time.process_time()
    c = con.contraction(poses, side)
    rec["cpu_contraction"] = round(time.process_time() - t0, 2)
    rec["lambda_less_1"] = float(1 - c["lambda"])
    t0 = time.process_time()
    ident.measure(poses, side, poses, side)
    rec["cpu_identity"] = round(time.process_time() - t0, 2)
    t0 = time.process_time()
    pairs = geom.pair_index(n)
    import r1021_clip as clipmod

    corners = [geom.corners_of(p) for p in poses]
    sample = pairs[:2000]
    for i, j in sample:
        clipmod.margin_from_corners(corners[i], corners[j])
    rec["cpu_C0_per_pair"] = (time.process_time() - t0) / len(sample)
    full = rec["cpu_A"] + rec["cpu_B"]
    rec["price"] = {
        "one_decision_both_methods_s": round(full, 1),
        "check_report_s": round(2 * full, 1),
        "C0_all_pairs_s": round(rec["cpu_C0_per_pair"] * len(pairs), 1),
    }
    with open(out, "w") as f:
        json.dump(rec, f, indent=1)
        f.write("\n")
    print(json.dumps(rec))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
