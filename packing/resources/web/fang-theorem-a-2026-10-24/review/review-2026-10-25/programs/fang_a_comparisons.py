#!/usr/bin/env python3
"""The comparisons of Fang's Theorem A note (v0.2, Section 7 and the abstract), in integers.

Stage 4 mathematical review of issue #797, lane c-review-797-math, 25 October 2026.
Written from the note and from the statements of the asymptotic register's
deficiency_upper_bounds rows (frontier/asymptotic-waste-bounds.yaml at PR #801's head
a3e826606), before its author read cases/asymptotic/fang_theorem_a.py or
deficiency_family.py's comparison code (deficiency_family.py was read only for its
definition of c*(k) and its statement texts). Every finite comparison is decided one k
at a time in integers; each "for every k" claim is closed by the tail lemma printed in
the receipt. Only Daniel's k^{2/5} bound and Ryu's Theorem 1.2, which have real
constants, are evaluated in mpmath at 50 digits, with a guard on nearness to integers.

    python3 -I fang_a_comparisons.py --out comparisons.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path

import mpmath as mp

mp.mp.dps = 50


def ceil_sqrt(n: int) -> int:
    r = math.isqrt(n)
    return r if r * r == n else r + 1


def theorem_a(k: int) -> int:
    """c*(k) <= ceil(sqrt(32k)), k >= 6."""
    return ceil_sqrt(32 * k)


def daniel(k: int) -> int:
    """c*(k) <= 4 ceil(sqrt(2k - 7)) - 1, k >= 7."""
    return 4 * ceil_sqrt(2 * k - 7) - 1


def ryu_1_4(k: int) -> int:
    """c*(k) <= 8 ceil(sqrt(k - 4)) - 1, k >= 6."""
    return 8 * ceil_sqrt(k - 4) - 1


def ryu_R(L: int, b: int) -> int:
    """Ryu's R(L) = max(0, ceil((L - h0) gamma0)), h0 = (3b^2-1)/D, gamma0 = (b^2-1)/D."""
    D = b * b + 1
    num = (L * D - (3 * b * b - 1)) * (b * b - 1)
    den = D * D
    return max(0, -((-num) // den))


def ryu_1_3_best(k: int) -> int:
    """Ryu's Theorem 1.3 at its best b: min over 2 <= b <= k of k^2 - N(k,b) - 1."""
    best = None
    for b in range(2, k + 1):
        if (k, b) == (2, 2):
            continue
        N = (k - b) ** 2 + b * (ryu_R(k, b) + ryu_R(k - b, b))
        val = k * k - N - 1
        best = val if best is None or val < best else best
    assert best is not None
    return best


def fang_t163(k: int) -> int:
    """c*(k) <= k - 1 - F(k), F(k) = 1 + max{p + 2q : 16p + 21q <= k - 15}, k >= 15.

    An optimum has q >= m // 21 - 15 (m = k - 15): if q <= m // 21 - 16, then either
    p >= 21 and (p - 21, q + 16) costs the same and gains 11, or p <= 20 and
    16p + 21q <= m - 16 leaves room for one more p. So only that window is searched;
    `fang_t163_brute` checks it against every q for k <= 3000."""
    m = k - 15
    qmax = m // 21
    best = max(((m - 21 * q) // 16) + 2 * q for q in range(max(0, qmax - 15), qmax + 1))
    return k - 1 - (1 + best)


def fang_t163_brute(k: int) -> int:
    m = k - 15
    best = max(((m - 21 * q) // 16) + 2 * q for q in range(0, m // 21 + 1))
    return k - 1 - (1 + best)


def int_bound_from_real(x: mp.mpf) -> int:
    """c* < x for an integer c* means c* <= ceil(x) - 1; refuse when x is within 1e-30 of an integer."""
    n = int(mp.ceil(x))
    if abs(x - mp.nint(x)) < mp.mpf("1e-30"):
        raise ValueError(f"too near an integer: {x}")
    return n - 1


def fifth_root(k: int) -> int | None:
    """The integer m with m^5 = k, or None. Otherwise k^(1/5) has degree 5 over Q
    (x^5 - k is irreducible), so no expression a k^(2/5) + b k^(1/5) + c with rational
    a, b, c and (a, b) != (0, 0) is rational, and the 1e-30 guard is only a numerical one."""
    m = round(k ** 0.2)
    for cand in (m - 1, m, m + 1):
        if cand >= 0 and cand**5 == k:
            return cand
    return None


def ceil_minus_one(x: Q) -> int:
    return -((-x.numerator) // x.denominator) - 1


def daniel_2_5(k: int) -> int:
    m = fifth_root(k)
    if m is not None:
        return ceil_minus_one(Q(189, 10) * m * m + Q(357, 10) * m + 122)
    k_ = mp.mpf(k)
    return int_bound_from_real(mp.mpf("18.9") * k_ ** mp.mpf("0.4") + mp.mpf("35.7") * k_ ** mp.mpf("0.2") + 122)


def ryu_1_2(k: int) -> int:
    m = fifth_root(k)
    if m is not None:
        return ceil_minus_one(Q(20668, 1000) * m * m + Q(623, 1000))
    k_ = mp.mpf(k)
    return int_bound_from_real(mp.mpf("20.668") * k_ ** mp.mpf("0.4") + mp.mpf("0.623"))


def runs(values: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    for v in values:
        if out and out[-1][1] == v - 1:
            out[-1][1] = v
        else:
            out.append([v, v])
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    t0 = time.process_time()
    res: dict[str, object] = {}
    checks: dict[str, bool] = {}

    # --- Daniel, 7 <= k < 10^6
    ours_smaller = his_smaller = tie = 0
    big_gap_below_89 = []
    over2_from_89 = []
    longest_run = (0, 0, 0)  # (length, start, end) of consecutive k with A < D
    cur_start = None
    for k in range(7, 10**6):
        a, d = theorem_a(k), daniel(k)
        if a < d:
            ours_smaller += 1
            if cur_start is None:
                cur_start = k
        else:
            if cur_start is not None:
                length = k - cur_start
                if length > longest_run[0]:
                    longest_run = (length, cur_start, k - 1)
                cur_start = None
            if a > d:
                his_smaller += 1
            else:
                tie += 1
        if k >= 89 and abs(a - d) > 2:
            over2_from_89.append(k)
        if k < 89 and a - d >= 3:
            big_gap_below_89.append((k, a - d))
    res["daniel"] = {
        "ours_smaller": ours_smaller, "his_smaller": his_smaller, "tie": tie,
        "k_at_least_89_with_difference_above_2": over2_from_89[:20],
        "below_89_his_smaller_by_3_or_more": big_gap_below_89,
        "longest_run_of_consecutive_k_with_ours_strictly_smaller": list(longest_run),
        "tail_lemma": "for k >= 102: A < 4 sqrt(2k) + 1 and D >= 4 sqrt(2k-7) - 1 give A - D < 2 + "
                      "28/(sqrt(2k) + sqrt(2k-7)) < 3, and D < 4 sqrt(2k-7) + 3 gives A - D > -3; "
                      "so |A - D| <= 2 for every k >= 102, and k = 89..101 are decided above",
    }
    checks["daniel counts 495210 / 255215 / 249568"] = (ours_smaller, his_smaller, tie) == (495210, 255215, 249568)
    checks["daniel: |A - D| <= 2 for 89 <= k < 10^6"] = not over2_from_89
    checks["daniel: 17 values below 89 with D smaller by 3 to 5"] = (
        len(big_gap_below_89) == 17 and all(3 <= g <= 5 for _, g in big_gap_below_89))
    # the tail lemma's numeric premise at k = 102: sqrt(204) + sqrt(197) > 28
    checks["tail premise: sqrt(2k) + sqrt(2k-7) > 28 at k = 102"] = (
        mp.sqrt(204) + mp.sqrt(197) > 28)
    # 88 is the last k with |A - D| > 2
    last_over2 = max(k for k in range(7, 200) if abs(theorem_a(k) - daniel(k)) > 2)
    res["daniel"]["last_k_with_difference_above_2"] = last_over2  # type: ignore[index]
    checks["daniel: the last k with |A - D| > 2 is 88"] = last_over2 == 88

    # --- Daniel's k^{2/5} bound against Theorem A, 3*10^5 <= k < 10^6
    his25_not_smaller = []
    first_smaller = None
    for k in range(3 * 10**5, 10**6):
        if not daniel_2_5(k) < theorem_a(k):
            his25_not_smaller.append(k)
        elif first_smaller is None:
            first_smaller = k
    last_not = max(his25_not_smaller) if his25_not_smaller else None
    res["daniel_k25"] = {
        "k_range": [3 * 10**5, 10**6 - 1],
        "count_where_not_smaller": len(his25_not_smaller),
        "first_k_where_smaller": first_smaller,
        "last_k_where_not_smaller": last_not,
        "first_k_from_which_always_smaller_to_10^6": None if last_not is None else last_not + 1,
        "at_10^6": {"sqrt_32k_minus_bound": float(mp.sqrt(32 * 10**6) - (
            mp.mpf("18.9") * mp.mpf(10**6) ** mp.mpf("0.4") + mp.mpf("35.7") * mp.mpf(10**6) ** mp.mpf("0.2") + 122))},
        "tail_lemma": "sqrt(32k) - 18.9 k^0.4 - 35.7 k^0.2 is increasing for k >= 3*10^5 "
                      "(derivative 2 sqrt 2 k^-1/2 - 7.56 k^-0.6 - 7.14 k^-0.8 > 0 there), so the "
                      "k^{2/5} bound stays smaller once sqrt(32k) exceeds it",
    }
    # derivative premise at 3e5, and growth of k^0.1 makes it hold beyond
    kk = mp.mpf(3 * 10**5)
    checks["daniel k25 tail derivative positive at 3e5"] = (
        2 * mp.sqrt(2) * kk ** mp.mpf(-0.5) - mp.mpf("7.56") * kk ** mp.mpf(-0.6)
        - mp.mpf("7.14") * kk ** mp.mpf(-0.8) > 0)
    first_always = None if last_not is None else last_not + 1
    checks["daniel k25: always smaller from about 7.4e5"] = (
        first_always is not None and 7.35 * 10**5 <= first_always <= 7.45 * 10**5)

    # --- Ryu Theorem 1.4
    r14 = {k: (theorem_a(k), ryu_1_4(k)) for k in range(6, 10**6)}
    res["ryu_1_4"] = {
        "k6": r14[6], "k7": r14[7], "k8": r14[8], "k9": r14[9],
        "first_10": {k: r14[k] for k in range(6, 16)},
        "tail_lemma": "for k >= 12: 8 sqrt(k-4) - sqrt(32k) >= 2 (increasing, 3.03 at k = 12), so "
                      "A < sqrt(32k) + 1 <= 8 sqrt(k-4) - 1 <= Ryu 1.4",
    }
    checks["ryu 1.4: ours smaller at 6 and every 9 <= k < 10^6"] = (
        r14[6][0] < r14[6][1] and all(a < r for k, (a, r) in r14.items() if k >= 9))
    checks["ryu 1.4: tie at 7, Ryu smaller at 8"] = r14[7][0] == r14[7][1] and r14[8][0] > r14[8][1]
    checks["ryu 1.4 tail premise at k = 12"] = 8 * mp.sqrt(8) - mp.sqrt(384) >= 2

    # --- Ryu Theorem 1.3 at its best b
    r13 = {k: (theorem_a(k), ryu_1_3_best(k)) for k in range(6, 401)}
    smaller = [k for k, (a, r) in r13.items() if a < r]
    ties = [k for k, (a, r) in r13.items() if a == r]
    larger = [k for k, (a, r) in r13.items() if a > r]
    res["ryu_1_3"] = {
        "ours_smaller_runs": runs(smaller), "tie": ties, "ours_larger": larger,
        "values_6_to_20": {k: r13[k] for k in range(6, 21)},
        "tail_lemma": "Ryu's Proposition 1.5: k^2 - N(k,b) > 8 sqrt(k) - 14 for all b, so Theorem "
                      "1.3 gives no less than 8 sqrt(k) - 15 + something; A < sqrt(32k) + 1 <= "
                      "8 sqrt(k) - 15 once (8 - 4 sqrt 2) sqrt(k) >= 16, i.e. k >= 47",
    }
    checks["ryu 1.3: ours smaller for every 14 <= k <= 400"] = all(r13[k][0] < r13[k][1] for k in range(14, 401))
    checks["ryu 1.3: ours not smaller at 13"] = not r13[13][0] < r13[13][1]
    checks["ryu 1.3 tail premise: (8 - 4 sqrt 2) sqrt 47 >= 16"] = (8 - 4 * mp.sqrt(2)) * mp.sqrt(47) >= 16

    # --- T-163 (Fang's Theorem 2, [Fan26a] in the note)
    checks["t163 window search equals brute force for 15 <= k <= 3000"] = all(
        fang_t163(k) == fang_t163_brute(k) for k in range(15, 3001))
    t163 = {k: (theorem_a(k), fang_t163(k)) for k in range(15, 10**6)}
    res["t163"] = {
        "larger_runs": runs([k for k, (a, f) in t163.items() if a > f]),
        "tie": [k for k, (a, f) in t163.items() if a == f],
        "smaller_from": min(k for k, (a, f) in t163.items() if a < f and all(
            t163[j][0] < t163[j][1] for j in range(k, min(k + 1000, 10**6)))),
        "tail_lemma": "F(k) <= 1 + 2(k-15)/21 since p + 2q <= (2/21)(16p + 21q), so the bound is "
                      ">= (19k - 12)/21 > sqrt(32k) + 1 > A once 19k - 33 > 21 sqrt(32k), i.e. k >= 45",
    }
    checks["t163: ours larger for 15 <= k <= 39"] = all(t163[k][0] > t163[k][1] for k in range(15, 40))
    checks["t163: tie at 40 and 41"] = t163[40][0] == t163[40][1] and t163[41][0] == t163[41][1]
    checks["t163: ours smaller for every 42 <= k < 10^6"] = all(t163[k][0] < t163[k][1] for k in range(42, 10**6))
    checks["t163 tail premise at k = 45: 19k - 33 > 21 sqrt(32k)"] = 19 * 45 - 33 > 21 * mp.sqrt(32 * 45)

    # --- Ryu Theorem 1.2 from 1.6*10^7, and Theorem 1.6's values
    k0 = 16 * 10**6
    g0 = mp.mpf("20.668") * mp.mpf(k0) ** mp.mpf("0.4") + mp.mpf("0.623")
    res["ryu_1_2"] = {
        "at_1.6e7": {"ryu_real": float(g0), "ryu_int": ryu_1_2(k0), "ours": theorem_a(k0)},
        "tail_lemma": "sqrt(32k) - 20.668 k^0.4 is increasing for k > 2.93^10 ~ 4.6*10^4 and positive "
                      "at 1.6*10^7, so Theorem 1.2's integer bound is below ours at every k >= 1.6*10^7",
    }
    checks["ryu 1.2 smaller at 1.6e7"] = ryu_1_2(k0) < theorem_a(k0)
    checks["ryu 1.2 derivative premise"] = (mp.sqrt(32) / 2 * mp.mpf(k0) ** mp.mpf(-0.5)
                                          - mp.mpf("0.4") * mp.mpf("20.668") * mp.mpf(k0) ** mp.mpf(-0.6) > 0)
    r16 = {10**5: 1583, 10**6: 3972, 10**7: 10039}
    res["ryu_1_6"] = {str(k): {"ryu": v, "ours": theorem_a(k)} for k, v in r16.items()}
    checks["ours at 1e5, 1e6, 1e7 = 1789, 5657, 17889"] = [theorem_a(k) for k in r16] == [1789, 5657, 17889]

    # --- the register's "strictly the least statement of the family at 346,919 of 42 <= k <= 702,000"
    least = 0
    below_daniel = 0
    run_best = (0, 0, 0)
    run_start: int | None = None
    for k in range(42, 702001):
        a = theorem_a(k)
        d = daniel(k)
        if a < d:
            below_daniel += 1
        others = [d, k - 1, ryu_1_4(k), fang_t163(k)]
        if k <= 46:
            others.append(ryu_1_3_best(k))
        if k == 10**5:
            others.append(1583)
        if all(a < o for o in others):
            least += 1
            run_start = k if run_start is None else run_start
        else:
            if run_start is not None and k - run_start > run_best[0]:
                run_best = (k - run_start, run_start, k - 1)
            run_start = None
    if run_start is not None and 702001 - run_start > run_best[0]:
        run_best = (702001 - run_start, run_start, 702000)
    res["family_least_42_to_702000"] = {
        "strictly_least": least, "below_daniel": below_daniel,
        "longest_run_of_consecutive_k_strictly_least": list(run_best),
        "note": "Ryu 1.3 needs no check from 47 (tail above); 10^5 has Ryu's 1583"}
    checks["register: strictly least at 346,919 of 42..702,000, below Daniel at 346,920"] = (
        least == 346919 and below_daniel == 346920)

    res["checks"] = checks
    res["all_hold"] = all(checks.values())
    res["cpu_seconds"] = round(time.process_time() - t0, 1)
    receipt = {"program": Path(__file__).name,
               "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "python": sys.version.split()[0], "mpmath": mp.__version__, **res}
    args.out.write_text(json.dumps(receipt, indent=1, default=str) + "\n")
    for name, ok in checks.items():
        print(("ok  " if ok else "FAIL") + "  " + name)
    print(json.dumps({k: v for k, v in res.items() if k not in ("checks",)}, indent=1, default=str)[:4000])
    return 0 if res["all_hold"] else 1


if __name__ == "__main__":
    sys.exit(main())
