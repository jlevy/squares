#!/usr/bin/env python3
"""Cost of checking a packing: exact versus approximate, and how it scales.

Three measurements:

1. exact verification of Trump's 11-square packing;
2. the approximate float64 check on grid packings, with and without spatial
   bucketing -- the point being that bucketing makes it linear in n, since
   unit squares in a container of side O(sqrt(n)) have O(1) neighbours each;
3. the cost of one multiplication in Q(alpha) as the algebraic degree grows,
   for the degrees that actually occur in the record table:
   deg 8 at s(11), 18 at s(17), 40 at s(300), 62 at s(1453).
"""

import math
import random
import time
from fractions import Fraction

from sqpack.field import NumberField, _poly_mul  # pyright: ignore[reportPrivateUsage]
from sqpack.packings import trump11
from sqpack.verify import exact_sign, float_sign, verify_packing


def grid_packing(n: int):
    """k x k grid of unit squares: same corner and axis count as a real packing."""
    k = math.ceil(math.sqrt(n))
    squares = []
    for i in range(n):
        x, y = float(i % k), float(i // k)
        squares.append([(x, y), (x + 1.0, y), (x + 1.0, y + 1.0), (x, y + 1.0)])
    return squares, float(k)


def bench_exact() -> None:
    squares, side, field = trump11.build()
    start = time.time()
    report = verify_packing(squares, side, sign=exact_sign)
    elapsed = time.time() - start
    print("1. exact verification, Trump's n=11 packing")
    print(
        f"   valid={report.valid}  degree={field.degree}  "
        f"pairs={report.pairs_tested}  zero-gap pairs={report.touching_pairs}"
    )
    print(
        f"   {elapsed * 1e3:.0f} ms  "
        f"({elapsed * 1e6 / max(1, report.pairs_tested):.0f} us/pair)"
    )


def bench_float() -> None:
    print("\n2. approximate float64 check on grid packings (this package, pure Python)")
    print("      n   pairs (all)  quadratic      pairs (bucketed)  bucketed")
    sign = float_sign(1e-9)
    for n in (11, 100, 324, 1000):
        squares, side = grid_packing(n)
        t0 = time.time()
        r_all = verify_packing(squares, side, sign=sign, check_shapes=False)
        t_all = time.time() - t0
        t0 = time.time()
        r_bkt = verify_packing(squares, side, sign=sign, check_shapes=False, bucket=True)
        t_bkt = time.time() - t0
        assert r_all.valid and r_bkt.valid
        print(
            f"   {n:>5}   {r_all.pairs_tested:>10}  {t_all * 1e3:>8.1f} ms"
            f"      {r_bkt.pairs_tested:>10}  {t_bkt * 1e3:>8.1f} ms"
        )


def bench_degrees() -> None:
    print("\n3. one multiplication in Q(alpha), by algebraic degree")
    print("      deg   ms/multiply   relative")
    baseline = None
    for degree in (8, 18, 40, 62):
        rnd = random.Random(degree)
        # a random monic modulus; only its size matters for this measurement
        min_poly = [1] + [rnd.randint(-9, 9) for _ in range(degree)]
        field = NumberField.__new__(NumberField)
        field.degree = degree
        field._high_to_low = [Fraction(c) for c in min_poly]  # pyright: ignore[reportPrivateUsage]
        field._low_to_high = field._high_to_low[::-1]  # pyright: ignore[reportPrivateUsage]
        a = [Fraction(rnd.randint(-9999, 9999), rnd.randint(1, 9999)) for _ in range(degree)]
        b = [Fraction(rnd.randint(-9999, 9999), rnd.randint(1, 9999)) for _ in range(degree)]
        trials = 200 if degree <= 18 else 40
        t0 = time.time()
        for _ in range(trials):  # fixed operands: no coefficient blow-up
            field._reduce(_poly_mul(a, b))  # pyright: ignore[reportPrivateUsage]
        dt = (time.time() - t0) / trials
        baseline = baseline or dt
        print(f"      {degree:>3}   {dt * 1e3:>10.2f}   {dt / baseline:>6.1f}x")


if __name__ == "__main__":
    bench_exact()
    bench_float()
    bench_degrees()
