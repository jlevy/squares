"""A cross-check of [R] Lemma 4.9(b)'s least margin in mpmath at 60 digits; decides nothing."""

import itertools

import mpmath as mp

mp.mp.dps = 60
d = mp.mpf(1) / 10**4
Lam = d + mp.sqrt(2)
rho1 = mp.sqrt((d + mp.sqrt(2) / 2) ** 2 + mp.mpf(1) / 4)
g0 = mp.acos(1 - 1 / (2 * Lam**2))
R = {2: rho1}
for m in (3, 4, 5):
    R[m] = min(rho1, 1 / (2 * mp.sin((m - 1) * g0 / 2)))


def f(a, b):
    return (a * a + b * b - 1) / (2 * a * b)


gam = {(a, b): mp.acos(f(R[a], R[b])) for a in range(2, 6) for b in range(2, 6)}
deg = 180 / mp.pi
best = None
for n in (3, 4, 5):
    for seq in itertools.product((2, 3, 4, 5), repeat=n):
        if sum(seq) < 15:
            continue
        tot = sum(gam[(seq[i], seq[(i + 1) % n])] for i in range(n))
        mg = (tot - 2 * mp.pi) * deg
        if best is None or mg < best[0]:
            best = (mg, seq)
print("gamma0 deg", mp.nstr(g0 * deg, 12), "rho1", mp.nstr(rho1, 10))
print("R3,R4,R5", [mp.nstr(R[m], 10) for m in (3, 4, 5)])
print("gamma(2,2) deg", mp.nstr(gam[(2, 2)] * deg, 10), "gamma(5,5)", mp.nstr(gam[(5, 5)] * deg, 10))
print("worst margin deg", mp.nstr(best[0], 15), "at", best[1])
