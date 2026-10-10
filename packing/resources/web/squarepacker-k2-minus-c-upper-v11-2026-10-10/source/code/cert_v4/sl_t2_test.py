# sl_t2_test.py -- exact random tests (not proofs) of Lemma SL and Lemma T2 of the paper.
#  SL: random rational beta in (0,1), c, n, eps, d_j in [0, eps], sgn; check sum frac(x_j) <= n(1+beta)/2 + n eps + 1/(8 beta)
#      exactly (Fractions); also an adversarial family (one run of length ~1/(2 beta), top value just below 1) to see the
#      bound is nearly attained (ratio of excess to 1/(8 beta)).
#  T2: random integer b >= 10^4, band length Lb (integer k minus b, or k - b + W), alpha = cy b^{4/5} (rational
#      approximation); construct y0 by the algorithm of the proof (R* = max{R >= 1: Y_R >= alpha}), and check exactly:
#      alpha <= y0 < alpha + (d+1)/2, R = floor((Lb - h - 2 y0)/d) + 1 >= 1, y1 - y0 in {0, 1},
#      frac(G(y0)) = frac(G(y1)) >= 1/2, y0, y1 <= alpha + 2.0001.
import random, json, math, sys
from fractions import Fraction as F

def fl(x):
    return x.numerator // x.denominator

def fr(x):
    return x - fl(x)

def sl_tests(N, rng):
    worst = 0.0; fails = 0
    for _ in range(N):
        q = rng.randint(2, 4000)
        beta = F(rng.randint(1, q - 1), q)
        n = rng.randint(0, 400)
        c = F(rng.randint(-10 ** 6, 10 ** 6), rng.randint(1, 10 ** 4))
        eps = F(rng.randint(0, 50), 1000) if rng.random() < 0.7 else F(0)
        sgn = rng.choice((1, -1))
        s = F(0)
        for j in range(n):
            d = eps * F(rng.randint(0, 1000), 1000)
            s += fr(c + sgn * j * beta + d)
        bound = F(n) * (1 + beta) / 2 + n * eps + 1 / (8 * beta)
        if s > bound:
            fails += 1
        ex = (s - F(n) * (1 + beta) / 2 - n * eps) / (1 / (8 * beta))
        worst = max(worst, float(ex))
    # adversarial: one run of r ~ 1/(2 beta) values ending just below 1
    adv = []
    for qb in (10, 37, 100, 1000):
        beta = F(1, qb)
        r = max(1, round(1 / (2 * float(beta))))
        top = 1 - F(1, 10 ** 9)
        c = top - (r - 1) * beta
        s = sum(fr(c + j * beta) for j in range(r))
        adv.append(dict(beta=str(beta), r=r, excess_over_1_8beta=float((s - F(r) * (1 + beta) / 2) * 8 * beta),
                        within=bool(s <= F(r) * (1 + beta) / 2 + 1 / (8 * beta))))
    return dict(sl_random=N, sl_fails=fails, sl_worst_excess_ratio=worst, sl_adversarial=adv)

def tilt_band(b):
    tt = F(b, b * b - 1)                  # tan(theta/2)
    c = (1 - tt * tt) / (1 + tt * tt); s = 2 * tt / (1 + tt * tt); T = s / c
    W = b * c + s; d = 1 / c; h = b * s + c
    return c, s, T, W, d, h

def t2_one(b, Lb, alpha, W, s, T, d, h):
    c0 = (W - s) * T
    def Y(R):
        S = Lb - h - (R - 1) * d
        K = S + 2 * c0
        e = 0 if fl(K) % 2 == 1 else 1
        return (S - e) / 2, e
    # R* = max{R >= 1 : Y_R >= alpha}: Y decreasing; estimate then adjust
    R = max(1, int((Lb - h - 2 * alpha) / d))
    while R > 1 and Y(R)[0] < alpha:
        R -= 1
    while Y(R + 1)[0] >= alpha:
        R += 1
    y0, e = Y(R)
    Rc = fl((Lb - h - 2 * y0) / d) + 1
    y1 = Lb - h - (Rc - 1) * d - y0
    G0, G1 = y0 + c0, y1 + c0
    ok = (alpha <= y0 < alpha + (d + 1) / 2 and Rc == R and R >= 1 and (y1 - y0) in (0, 1)
          and fr(G0) == fr(G1) and fr(G0) >= F(1, 2) and y1 <= alpha + F(20001, 10000) and y0 >= 0)
    return ok, float(y0 - alpha), int(y1 - y0), float(fr(G0))

def t2_tests(N, rng):
    fails = 0; maxoff = 0.0; mins = 1.0; n1 = 0
    for _ in range(N):
        b = rng.randint(10 ** 4, 3 * 10 ** 5)
        c, s, T, W, d, h = tilt_band(b)
        k = rng.randint(b * b // 50 + 10 ** 5, b * b // 5 + 10 ** 6)
        cy = F(rng.randint(5, 200), 1000)
        alpha = cy * F(round(b ** 0.8 * 10 ** 6), 10 ** 6)
        # the two real band lengths, plus two with a random fractional offset (Lemma T2 holds for any real Lb; the
        # offsets make frac(K_R) and the parity of floor(K_R) vary over the whole range)
        for Lb in (F(k - b), k - b + W, F(k - b) + F(rng.randint(0, 9999), 10000), F(rng.randint(10 ** 5, 10 ** 9), 7)):
            if Lb - h - 1 < 2 * alpha:
                continue
            ok, off, gap, fg = t2_one(b, Lb, alpha, W, s, T, d, h)
            if not ok:
                fails += 1
            maxoff = max(maxoff, off); mins = min(mins, fg); n1 += gap
    return dict(t2_random=N, t2_fails=fails, t2_max_y0_minus_alpha=maxoff, t2_min_fracG=mins, t2_count_y1_eq_y0_plus_1=n1)

if __name__ == '__main__':
    rng = random.Random(20261010)
    out = sl_tests(int(sys.argv[1]) if len(sys.argv) > 1 else 3000, rng)
    out.update(t2_tests(int(sys.argv[2]) if len(sys.argv) > 2 else 300, rng))
    print(json.dumps(out))
