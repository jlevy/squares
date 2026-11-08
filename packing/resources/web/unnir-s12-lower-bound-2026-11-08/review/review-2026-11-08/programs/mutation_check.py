"""Mutation check for test_decider: the brute force must catch small sweep defects.

Each mutant feeds min_capture a box half-side or a domain that is off by one
scaled unit 1/(Q D) and counts the random instances where the brute force
disagrees.  A test with no mismatches against every mutant would have no teeth.

Usage: python -I mutation_check.py
"""

import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decide_bins as db  # noqa: E402
import test_decider as td  # noqa: E402


def run(label, mutate_half, mutate_lo, n=600, seed=11):
    rng = random.Random(seed)
    d = 40
    caught = tried = 0
    for _ in range(n):
        side = Fraction(rng.randint(60, 140), d)
        m = rng.randint(1, 18)
        grid = rng.choice([4, 8, 40])
        pts = []
        for _ in range(m):
            x = rng.randint(0, int(side * d) // (d // grid)) * (d // grid)
            y = rng.randint(0, int(side * d) // (d // grid)) * (d // grid)
            pts.append((min(x, int(side * d)), min(y, int(side * d)), rng.randint(1, 5)))
        t_r = Fraction(rng.choice([0, 1, 1, 2, 3, 5]), rng.choice([7, 9, 12, 40]))
        half = rng.choice([Fraction(1, 2), Fraction(2, 5), Fraction(49, 100), Fraction(1, 4)])
        lo = rng.choice([db.half_extent(t_r), Fraction(1, 2), Fraction(3, 5)])
        if 2 * lo >= side:
            continue
        cn, sn, Q = db.rotation_of_t(t_r)
        tried += 1
        got, _ = db.min_capture(pts, side, d, t_r, mutate_half(half, Q, d), mutate_lo(lo, Q, d))
        ref = td.brute_min(pts, side, d, t_r, half, lo)
        caught += got != ref
    print(f"{label}: tried={tried} mismatches={caught}")


def main():
    run("half-side +1 scaled unit", lambda h, Q, d: h + Fraction(1, Q * d), lambda lo, Q, d: lo)
    run("half-side -1 scaled unit", lambda h, Q, d: h - Fraction(1, Q * d), lambda lo, Q, d: lo)
    run("domain shrunk 1/(QD) a side", lambda h, Q, d: h, lambda lo, Q, d: lo + Fraction(1, Q * d))
    run("domain grown 1/(QD) a side", lambda h, Q, d: h, lambda lo, Q, d: lo - Fraction(1, Q * d))


if __name__ == "__main__":
    main()
