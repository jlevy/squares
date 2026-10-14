#!/usr/bin/env python3
"""verify_sturm.py -- exact Sturm root-isolation checker (sturm-root-isolation-v1).

TCB-small: Python stdlib only (fractions, json, sys).  Every decision is exact
rational arithmetic; no floats anywhere.

What a PASS establishes, given the certificate's polynomial p and interval [a, b]:

  (1) p(a) and p(b) are exactly the recorded rationals, with the recorded signs
      (in particular p(a) != 0 and p(b) != 0);
  (2) p is squarefree (its Sturm chain ends in a nonzero constant), and by
      Sturm's theorem p has exactly `total_real_roots` real roots, of which
      exactly `real_roots_below_a` lie in (-inf, a] and exactly
      `real_roots_in_ab` lie in (a, b];
  (3) each interval in `all_real_root_isolating_intervals` contains exactly one
      real root, the intervals are disjoint and in increasing order, and they
      account for all real roots -- so the root in (a, b] is the
      `root_index_in_ab`-th real root of p in increasing order;
  (4) if `taylor_shift_at_a_positive_from_degree_1` is claimed: the recorded
      Taylor coefficients d_k of p(a + t) are exact and d_k > 0 for all
      k >= 1 (hence p is strictly increasing on [a, +inf): for 0 <= u < v,
      p(a+v) - p(a+u) = sum_{k>=1} d_k (v^k - u^k) > 0 -- the calculus-free
      uniqueness argument replayed by the Lean discharge of `shat_spec`).

Sturm's theorem (standard; e.g. Basu-Pollack-Roy, Algorithms in Real Algebraic
Geometry, Thm 2.50): for p squarefree with Sturm chain p_0 = p, p_1 = p',
p_{i+1} = -rem(p_{i-1}, p_i), and V(x) = number of sign variations (zeros
dropped) of (p_i(x))_i, the number of distinct real roots of p in (x1, x2] is
V(x1) - V(x2) for any x1 < x2 that are not roots of p.  Counting "roots of p"
vs "distinct roots" coincide for squarefree p.  V at -inf/+inf is computed from
leading coefficients and degrees.

Exit 0 = PASS, 1 = FAIL, 2 = malformed certificate.
"""
import json
import sys
from fractions import Fraction as F


def parse_q(s):
    return F(s)  # Fraction parses "n/d" and integer and decimal strings exactly


def polyval(c, x):
    r = F(0)
    for coef in reversed(c):
        r = r * x + coef
    return r


def polyderiv(c):
    return [F(k) * c[k] for k in range(1, len(c))]


def strip(c):
    c = list(c)
    while c and c[-1] == 0:
        c.pop()
    return c


def polyrem(a, b):
    """Remainder of a mod b over Q (b nonzero)."""
    r = [F(x) for x in a]
    db, lb = len(b) - 1, b[-1]
    while True:
        r = strip(r)
        if len(r) - 1 < db or not r:
            return r
        coef = r[-1] / lb
        deg = len(r) - 1 - db
        for i in range(len(b)):
            r[deg + i] -= coef * b[i]
        r.pop()


def sturm_chain(p):
    p0 = strip([F(x) for x in p])
    p1 = strip(polyderiv(p0))
    chain = [p0, p1]
    while True:
        r = polyrem(chain[-2], chain[-1])
        if not r:
            return chain
        chain.append([-x for x in r])


def sign(v):
    return (v > 0) - (v < 0)


def variations(signs):
    signs = [s for s in signs if s != 0]
    return sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])


def V_at(chain, x):
    return variations([sign(polyval(c, x)) for c in chain])


def V_inf(chain, direction):
    """direction = +1 for +inf, -1 for -inf."""
    signs = []
    for c in chain:
        s = sign(c[-1])
        if direction < 0 and (len(c) - 1) % 2 == 1:
            s = -s
        signs.append(s)
    return variations(signs)


def taylor_shift(c, a):
    """Coefficients of p(a + t) in t, by repeated synthetic division."""
    c = [F(x) for x in c]
    out = []
    for _ in range(len(c)):
        rem = F(0)
        horner = []
        for coef in reversed(c):
            rem = rem * a + coef
            horner.append(rem)
        out.append(horner[-1])
        c = list(reversed(horner[:-1]))
        if not c:
            break
    return out


def fail(msg):
    print("FAIL:", msg)
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("usage: verify_sturm.py <certificate.json>")
        sys.exit(2)
    try:
        cert = json.load(open(sys.argv[1]))
        p = [parse_q(s) for s in cert["polynomial"]["coefficients_low_to_high"]]
        a = parse_q(cert["interval"]["a"])
        b = parse_q(cert["interval"]["b"])
        cl = cert["claims"]
    except Exception as e:  # malformed
        print("MALFORMED:", e)
        sys.exit(2)

    if strip(p) != p or len(p) < 2:
        fail("polynomial not normalised or constant")
    if not (a < b):
        fail("interval endpoints not ordered")

    # (1) endpoint values and signs
    pa, pb = polyval(p, a), polyval(p, b)
    if pa != parse_q(cl["p_at_a"]):
        fail("p(a) mismatch: computed %s" % pa)
    if pb != parse_q(cl["p_at_b"]):
        fail("p(b) mismatch: computed %s" % pb)
    if sign(pa) != cl["sign_p_at_a"] or sign(pa) == 0:
        fail("sign of p(a) wrong or zero")
    if sign(pb) != cl["sign_p_at_b"] or sign(pb) == 0:
        fail("sign of p(b) wrong or zero")

    # (2) Sturm counts
    chain = sturm_chain(p)
    if len(chain[-1]) != 1 or chain[-1][0] == 0:
        fail("p is not squarefree (Sturm chain does not end in a nonzero constant)")
    vm, vp = V_inf(chain, -1), V_inf(chain, +1)
    va, vb = V_at(chain, a), V_at(chain, b)
    total = vm - vp
    below_a = vm - va
    in_ab = va - vb
    if total != cl["total_real_roots"]:
        fail("total real roots: computed %d, claimed %d" % (total, cl["total_real_roots"]))
    if below_a != cl["real_roots_below_a"]:
        fail("roots below a: computed %d, claimed %d" % (below_a, cl["real_roots_below_a"]))
    if in_ab != cl["real_roots_in_ab"]:
        fail("roots in (a,b]: computed %d, claimed %d" % (in_ab, cl["real_roots_in_ab"]))
    if cl["root_index_in_ab"] != below_a + in_ab or in_ab != 1:
        fail("root index in (a,b] inconsistent (need exactly one root there)")

    # (3) isolating intervals: disjoint, increasing, one root each, exhaustive
    ivs = [(parse_q(lo), parse_q(hi)) for lo, hi in cl["all_real_root_isolating_intervals"]]
    prev_hi = None
    for lo, hi in ivs:
        if not (lo < hi):
            fail("isolating interval not ordered")
        if prev_hi is not None and not (prev_hi <= lo):
            fail("isolating intervals overlap or out of order")
        if polyval(p, lo) == 0 or polyval(p, hi) == 0:
            fail("isolating interval endpoint is a root (open/half-open counting broken)")
        n = V_at(chain, lo) - V_at(chain, hi)
        if n != 1:
            fail("isolating interval (%s, %s] holds %d roots, want 1" % (lo, hi, n))
        prev_hi = hi
    if len(ivs) != total:
        fail("isolating intervals do not account for all %d real roots" % total)

    # (4) Taylor shift positivity
    if cl.get("taylor_shift_at_a_positive_from_degree_1"):
        ds = taylor_shift(p, a)
        rec = [parse_q(s) for s in cert["taylor_shift_at_a"]["coefficients_low_to_high"]]
        if ds != rec:
            fail("Taylor-shift coefficients mismatch")
        if any(d <= 0 for d in ds[1:]):
            fail("some Taylor coefficient d_k, k>=1, is not positive")
        if ds[0] >= 0:
            fail("d_0 = p(a) is not negative (expected by the shift claim)")

    print("PASS: p has exactly %d real roots; exactly one lies in (%s, %s] "
          "(the number %d in increasing order); p(a) %s 0 < p(b); "
          "Taylor shift at a all-positive from degree 1: %s"
          % (total, a, b, cl["root_index_in_ab"],
             "<" if pa < 0 else ">", bool(cl.get("taylor_shift_at_a_positive_from_degree_1"))))
    sys.exit(0)


if __name__ == "__main__":
    main()
