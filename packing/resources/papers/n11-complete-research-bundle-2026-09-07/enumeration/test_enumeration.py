#!/usr/bin/env python3
"""Known-answer and negative controls, not an n=11 solver validation."""
from fractions import Fraction as F
from math import comb
import json
import enumeration_checks as c


def refused(fn):
    try:
        fn()
    except ValueError:
        return
    raise RuntimeError("invalid input was not refused")


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    tests = []
    for n in range(1, 12):
        p = [x for k in range(1, n+1) for x in c.positive_compositions(n, k)]
        c.validate_profiles(p, n)
        check(len(p) == 2**(n-1), "profile count")
        for k in range(1, 6):
            check(len(list(c.weak_compositions(n, k))) == comb(n+k-1, k-1), "bin count")
    tests.append("recursive profiles agree with independent cut-mask enumeration for n=1..11")
    p = [x for k in range(1, 12) for x in c.positive_compositions(11, k)]
    refused(lambda: c.validate_profiles(p[:-1]))
    refused(lambda: c.validate_profiles(p+[p[0]]))
    refused(lambda: c.positive_compositions(0, 1).__next__())
    tests.append("omitted, duplicate, and invalid descriptor inputs rejected")
    c.check_disks(c.disk_centers())
    bad = c.disk_centers(); bad[0] = bad[1]
    refused(lambda: c.check_disks(bad))
    refused(lambda: c.check_disks(c.disk_centers(), F(7, 2)))
    tests.append("twelve-disk construction passes; overlap and wall-crossing mutations rejected")
    c.angular_arithmetic(); c.angle_controls()
    tests.append("angular transfer arithmetic and independent-reflection counterexample pass")
    exact = lambda x: (F(x), F(x))
    # x<=0, -x<=-1 is infeasible; no cancellation error at all.
    A = [[exact(1)], [exact(-1)]]; b = [exact(0), exact(-1)]; box = [(-F(2), F(2))]
    check(c.robust_farkas_gap(A, b, [F(1), F(1)], box) == 1, "Farkas fixture")
    check(c.robust_farkas_gap(A[:1], b[:1], [F(1)], box) <= 0, "missing row")
    refused(lambda: c.robust_farkas_gap(A, b, [F(-1), F(1)], box))
    refused(lambda: c.robust_farkas_gap(A, b, [F(1)], box))
    refused(lambda: c.robust_farkas_gap(A, b, [1.0, F(1)], box))
    # p*x<=-1, p in [1,2], x in [0,1] is impossible.
    check(c.robust_farkas_gap([[(F(1), F(2))]], [exact(-1)], [F(1)], [(F(0), F(1))]) > 0,
          "robust coefficient fixture")
    # Widening p to [-2,2] admits p=-1,x=1, so a midpoint-based rejection would be unsound.
    check(c.robust_farkas_gap([[(-F(2), F(2))]], [exact(-1)], [F(1)], [(F(0), F(1))]) <= 0,
          "widened feasible coefficient box")
    tests.append("robust-Farkas positive controls pass; missing-row, negative-multiplier and widening traps do not certify")
    print(json.dumps({"status": "PASS", "checks": tests,
        "scope": "Elementary exact controls and descriptor enumeration; no full packing branch closed",
        "independence": "Same-author controls, not an external mathematical review"}, indent=2))


if __name__ == '__main__':
    main()
