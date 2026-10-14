"""Random spot-test of the parallel-pair row derivation of PROOF.md P098-P107 (FINITE_PARALLEL_DERIVATION).
Two unit squares with a common reference side direction n, rotated by omega_i and omega_j, centre difference
Delta = d_w + delta_h; one of the two retained separating alternatives holds (owner i with normal R(omega_i) n,
or owner j with normal R(omega_j) n). The chain P100 -> P102 -> P105 -> P106 is tested on random instances.
Usage: python3 -I parallel_row_check.py
"""
import math
import random

random.seed(7)
fails = {"P100": 0, "P102": 0, "P104": 0, "P105": 0, "P106": 0}
tested = 0


def rot(a, v):
    return (math.cos(a) * v[0] - math.sin(a) * v[1], math.sin(a) * v[0] + math.cos(a) * v[1])


def Jv(v):
    return (-v[1], v[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def support(n, a):
    """support of a unit square with side direction a in the unit direction n"""
    return (abs(dot(n, a)) + abs(dot(n, Jv(a)))) / 2


for _ in range(200000):
    th = random.uniform(0, 2 * math.pi)
    n = (math.cos(th), math.sin(th))
    m, q = random.uniform(0.001, 0.1), random.uniform(0.001, 0.1)
    D, dr = random.uniform(0.5, 1.5), random.uniform(0.0001, 0.05)
    mu, eps = random.uniform(-m, m), random.uniform(-q, q)
    wi, wj = mu - eps, mu + eps
    ai, aj = rot(wi, n), rot(wj, n)
    # a centre difference with one of the two alternatives holding
    owner_i = random.random() < 0.5
    tau_p = random.uniform(-0.95, 0.95)
    # d_w along n and Jn, |d_w| <= D; delta_h small
    xw = random.uniform(0.9, 1.4)
    d_w = (xw * n[0] + tau_p * Jv(n)[0], xw * n[1] + tau_p * Jv(n)[1])
    if math.hypot(*d_w) > D:
        continue
    ang = random.uniform(0, 2 * math.pi)
    rr = random.uniform(0, dr)
    delta_h = (rr * math.cos(ang), rr * math.sin(ang))
    Delta = (d_w[0] + delta_h[0], d_w[1] + delta_h[1])
    ni, nj = ai, aj
    hold_i = dot(ni, Delta) >= 1 / 2 + support(ni, aj)
    hold_j = dot(nj, Delta) >= 1 / 2 + support(nj, ai)
    if not (hold_i or hold_j):
        continue
    tested += 1
    tau_p = dot(Jv(n), d_w)
    tmax = abs(tau_p) + 1e-12
    if tmax >= 1:
        continue
    nm = rot(mu, n)
    Xm, taum = dot(nm, Delta), dot(Jv(nm), Delta)
    X = dot(n, Delta)
    e = abs(eps)
    # P100
    if math.cos(e) * Xm + math.sin(e) * abs(taum) < math.cos(e) ** 2 + math.sin(e) * math.cos(e) - 1e-12:
        fails["P100"] += 1
    # P102
    if Xm - 1 < e * (1 - abs(taum)) - e * e / 2 - e ** 3 / 6 - e ** 3 * abs(taum) - 1e-12:
        fails["P102"] += 1
    # P104
    if abs(Xm - X - mu * tau_p) > D * m * m / 2 + m * dr + 1e-12 or abs(taum - tau_p) > D * m + dr + 1e-12:
        fails["P104"] += 1
    # P105 / P106
    E = D * m * m / 2 + m * dr + q * q / 2 + q ** 3 / 6 + tmax * q ** 3 + (D * m + dr) * (q + q ** 3)
    if X - 1 + mu * tau_p + E < e * (1 - abs(tau_p)) - 1e-12:
        fails["P105"] += 1
    for s in (-1, 1):
        if X - 1 + mu * tau_p + s * eps * (1 - abs(tau_p)) + E < -1e-12:
            fails["P106"] += 1
print("tested instances:", tested)
print("failures:", fails)
print("FAILURES:", sum(fails.values()))
