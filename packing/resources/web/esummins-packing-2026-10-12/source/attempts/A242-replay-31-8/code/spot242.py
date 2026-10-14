"""A242 -- INDEPENDENT spot-check of Kleddamag's global certificate (T-037), lab code only (Fraction / int), no import
from the external repository.  Reads ext/repo/global-certificate.json as DATA (and, for the row minima it compares
against, evidence/portable/python.json as DATA).

  (a) Scaling:  (191/50) / (764/775) = 31/8.
  (b) Budget:   M = sum of point-site weights over the D4-expanded sites + sum over charge sets of floor(m/k) w,
                per family, = budget_units; D4 invariance of sites, weights and charge sets checked independently.
  (c) Charges:  >= 200 random (row, parent angle u in [a,b], legal centre) poses + the four corners of the first
                sampled legal domains: the row's core (side B, half-angle t) is strictly inside the parent (exact)
                and its CLOSED capture charge (point weights + k-of-m indicators, evaluated logically) is >= Gamma
                and >= the release's recorded minimum for that row.
  (d) 11 Gamma > M.
    python code/spot242.py [N_random=600] [N_critical=400] [seed=242]
"""
import json, math, os, random, sys, time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ATT = os.path.abspath(os.path.join(HERE, '..'))
REPO = os.path.join(ATT, 'ext', 'repo')
RES = os.path.join(ATT, 'results')


def lower_priority():
    try:
        import ctypes
        k32 = ctypes.windll.kernel32
        h = k32.GetCurrentProcess()
        k32.SetPriorityClass(h, 0x00004000)
        k32.SetProcessAffinityMask(h, 0xFFFF)
    except Exception:
        pass


def d4(Z):
    """The eight symmetries of [0, Z]^2 as functions on integer points."""
    gs = []
    for sw in (0, 1):
        for fx in (0, 1):
            for fy in (0, 1):
                def g(p, sw=sw, fx=fx, fy=fy):
                    x, y = (p[1], p[0]) if sw else p
                    return (Z - x if fx else x, Z - y if fy else y)
                gs.append(g)
    return gs


def expand(c):
    D = c['coordinate_denominator']
    Z = F(c['L']) * D
    assert Z.denominator == 1
    Z = int(Z)
    G = d4(Z)
    sites, w = [], []
    for x, y, wt in c['point_orbits']:
        orb = sorted({g((x, y)) for g in G})          # index convention of the format: orbit order, sorted within
        sites += orb
        w += [wt] * len(orb)
    assert len(set(sites)) == len(sites)
    idx = {p: i for i, p in enumerate(sites)}
    charges = []
    for orb in c['charge_orbits']:
        k, wt = orb['threshold'], orb['weight']
        for S in orb['sets']:
            assert len(S) == len(set(S)) and len(S) in (3, 5) and 1 <= k <= len(S) and wt >= 0
            charges.append((tuple(sorted(S)), k, wt))
    key = sorted(charges)                              # D4 invariance of weights and of the charge multiset
    for g in G:
        perm = [idx[g(p)] for p in sites]
        assert all(w[perm[i]] == w[i] for i in range(len(sites)))
        assert sorted((tuple(sorted(perm[i] for i in S)), k, wt) for S, k, wt in charges) == key
    return D, Z, sites, w, charges


def budget(w, charges):
    fam = {'point': sum(w)}
    for S, k, wt in charges:
        name = '%d-of-%d' % (k, len(S))
        fam[name] = fam.get(name, 0) + (len(S) // k) * wt
    return fam


def trig(u):
    return (1 - u * u) / (1 + u * u), 2 * u / (1 + u * u)


def charge(D, sites, w, charges, cx, cy, t, B):
    """Closed capture: site (X/D, Y/D) in the core iff |R(-phi)(x - c)|_inf <= B/2 -- an all-integer test."""
    p, q = t.numerator, t.denominator
    C, S, R = q * q - p * p, 2 * p * q, q * q + p * p
    dc = cx.denominator * cy.denominator // math.gcd(cx.denominator, cy.denominator)
    nx, ny = int(cx * dc), int(cy * dc)
    rhs = B.numerator * R * D * dc                     # 2 bd |rot| <= bn R D dc  <=>  |rot / (R D dc)| <= B/2
    two_bd = 2 * B.denominator
    cap = set()
    for i, (X, Y) in enumerate(sites):
        dx, dy = X * dc - nx * D, Y * dc - ny * D
        if two_bd * abs(C * dx + S * dy) <= rhs and two_bd * abs(-S * dx + C * dy) <= rhs:
            cap.add(i)
    tot = sum(w[i] for i in cap)
    for St, k, wt in charges:
        if wt and sum(1 for i in St if i in cap) >= k:
            tot += wt
    return tot, len(cap)


def main():
    lower_priority()
    nr = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    nc = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 242
    t0 = time.monotonic()
    c = json.load(open(os.path.join(REPO, 'global-certificate.json')))
    ev = json.load(open(os.path.join(REPO, 'evidence', 'portable', 'python.json')))
    rowmin = {r['row']: r['minimum_units'] for r in ev['rows']}
    L, A = F(c['L']), F(c['A'])
    out = {'a_scaling': {'L': str(L), 'A': str(A), 'L_over_A': str(L / A), 'pass': L / A == F(31, 8)}}
    D, Z, sites, w, charges = expand(c)
    fam = budget(w, charges)
    M = sum(fam.values())
    Gam = c['minimum_units']
    out['b_budget'] = {'sites': len(sites), 'positive_point_sites': sum(1 for x in w if x),
                       'charge_sets': len(charges), 'positive_charge_sets': sum(1 for x in charges if x[2]),
                       'families_units': fam, 'M_units': M, 'budget_units_in_cert': c['budget_units'],
                       'd4_invariant': True, 'pass': M == c['budget_units'] == 10999479944}
    out['d_counting'] = {'Gamma_units': Gam, 'M_units': M, '11Gamma_minus_M': 11 * Gam - M,
                         'pass': 11 * Gam > M and 11 * Gam - M == 107864}
    rng = random.Random(seed)
    E = [tuple(map(F, e)) for e in c['entries']]
    crit = sorted(k for k, z in rowmin.items() if z < max(rowmin.values()))
    picks = [('random', rng.randrange(len(E))) for _ in range(nr)] + [('critical', rng.choice(crit)) for _ in range(nc)]
    worst, fails, n, ncorner = None, 0, 0, 0
    with open(os.path.join(RES, 'spot242.jsonl'), 'w') as f:
        for kind, k in picks:
            a, b, t, B = E[k]
            u = a + (b - a) * F(rng.randrange(0, 10 ** 6 + 1), 10 ** 6)
            cu, su = trig(u)
            ct, st = trig(t)
            cd, sd = ct * cu + st * su, ct * su - st * cu          # cos, sin of (phi_core - theta_parent)
            inside = B * (abs(cd) + abs(sd)) < A                   # concentric core strictly inside the parent
            r = A * (cu + su) / 2                                  # legal centres [r, L - r]^2 at this u
            poses = [(r + (L - 2 * r) * F(rng.randrange(10 ** 6 + 1), 10 ** 6),
                      r + (L - 2 * r) * F(rng.randrange(10 ** 6 + 1), 10 ** 6), 'interior')]
            if ncorner < 60:
                ncorner += 1
                poses += [(x, y, 'corner') for x in (r, L - r) for y in (r, L - r)]
            for cx, cy, where in poses:
                z, ncap = charge(D, sites, w, charges, cx, cy, t, B)
                ok = inside and z >= Gam and z >= rowmin[k] and r <= L - r
                fails += not ok
                n += 1
                worst = z if worst is None else min(worst, z)
                f.write(json.dumps({'kind': kind, 'pose': where, 'row': k, 'u': str(u), 'cx': str(cx), 'cy': str(cy),
                                    'core_inside_parent': inside, 'captured_sites': ncap, 'charge_units': z,
                                    'row_min_recorded': rowmin[k], 'slack_vs_gamma': z - Gam, 'pass': ok}) + '\n')
    out['c_charges'] = {'poses': n, 'random_rows': nr, 'critical_rows_drawn': nc, 'critical_rows': len(crit),
                        'corner_domains': ncorner, 'failures': fails, 'min_charge_units': worst, 'seed': seed,
                        'pass': fails == 0 and n >= 200}
    out['all_pass'] = all(out[x]['pass'] for x in ('a_scaling', 'b_budget', 'c_charges', 'd_counting'))
    out['seconds'] = round(time.monotonic() - t0, 1)
    json.dump(out, open(os.path.join(RES, 'spot242.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
