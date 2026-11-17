#!/usr/bin/env python3
"""Exact front end of the rectangle-density checker.

  prep.py CAND.json[.gz] OUT.txt [--n N]      exact premises in Fractions, D4 expansion, outward-rounded instance
  (library) load_cert, premises, exact_F

Certificate format: {"n", "L", "B", "total_mass"?, "proof_net"?: {"step","last"}, "rectangles": [{"rectangle": [x1,y1,x2,y2], "mass"}]}
Each listed rectangle is an orbit representative: its 8 images under D4 of [0,L]^2 carry mass/8 each, uniformly.
"""
import json, gzip, sys
from fractions import Fraction as Fr

STD_NET = (Fr(83, 40000), 200)

def load_cert(path):
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rt') as f:
        d = json.load(f, parse_float=str, parse_int=str)
    return d

def fr(x):
    return Fr(str(x))

def premises(d, n=None):
    """Return (ok, info, parsed). All checks exact."""
    info = {}
    n = int(d['n']) if n is None else n
    L, B = fr(d['L']), fr(d['B'])
    if 'proof_net' in d:
        D, last = fr(d['proof_net']['step']), int(d['proof_net']['last'])
    else:
        D, last = STD_NET
    rects = []
    M = Fr(0)
    ok = True
    for r in d['rectangles']:
        x1, y1, x2, y2 = [fr(v) for v in r['rectangle']]
        w = fr(r['mass'])
        if w < 0 or not (0 <= x1 < x2 <= L and 0 <= y1 < y2 <= L):
            ok = False; info.setdefault('bad_rects', 0); info['bad_rects'] += 1
        M += w
        if w > 0:
            rects.append((x1, y1, x2, y2, w))
    if d.get('points'):
        ok = False; info['points_present'] = True
    tmax = last * D
    checks = {
        'mass_lt_n': M < n,
        'total_mass_matches': ('total_mass' not in d) or fr(d['total_mass']) == M,
        'B_in_0_1': 0 < B < 1,
        'shrink_B(1+D)<1': B * (1 + D) < 1,
        'endpoint_tmax_past_tan_pi8': tmax * tmax + 2 * tmax - 1 > 0,
        'tmax_le_half': tmax <= Fr(1, 2),
        'D_pos': D > 0 and last >= 1,
        'rects_ok': ok,
    }
    info.update({k: bool(v) for k, v in checks.items()})
    info.update({'n': n, 'L': str(L), 'B': str(B), 'D': str(D), 'last': last, 'M': str(M), 'n_minus_M': str(n - M),
                 'B(1+D)': str(B * (1 + D)), 'orbits': len(rects)})
    allok = all(checks.values())
    return allok, info, dict(n=n, L=L, B=B, D=D, last=last, M=M, rects=rects)

def d4_images(x1, y1, x2, y2, L):
    out = []
    for (a1, a2, b1, b2) in [(x1, x2, y1, y2), (y1, y2, x1, x2)]:  # identity, diagonal swap
        for fx in (0, 1):
            for fy in (0, 1):
                X = (a1, a2) if not fx else (L - a2, L - a1)
                Y = (b1, b2) if not fy else (L - b2, L - b1)
                out.append((X[0], Y[0], X[1], Y[1]))
    return out

def dec(q, mode, digits=28):
    """decimal string >= q (mode 'up') or <= q (mode 'dn'), `digits` significant digits"""
    q = Fr(q)
    if q == 0: return '0'
    neg = q < 0
    a = abs(q)
    e = 0
    while a >= 10: a /= 10; e += 1
    while a < 1: a *= 10; e -= 1
    scale = Fr(10) ** (digits - 1 - e)
    v = q * scale
    fl = v.numerator // v.denominator
    if mode == 'up':
        m = fl if fl == v else fl + 1
    else:
        m = fl
    s = f"{m}e{-(digits - 1 - e)}"
    assert (Fr(m) / scale >= q) if mode == 'up' else (Fr(m) / scale <= q)
    return s

def net_cs(r, D):
    p, q = D.numerator, D.denominator
    den = q * q + r * r * p * p
    return (q * q - r * r * p * p, 2 * r * p * q, den)

def domain_margin(r, D, B):
    t = r * D
    a = max(Fr(0), t - D / 2)
    rho = (1 + 2 * a - a * a) / (2 * (1 + a * a))
    cn, sn, den = net_cs(r, D)
    core = B * Fr(cn + sn, den) / 2
    return max(rho, core)

def write_instance(P, out, dirs=None):
    L, B, D, last = P['L'], P['B'], P['D'], P['last']
    lines = [f"{dec(L/2,'dn')} {dec(B/2,'dn')}"]
    ex = []
    for (x1, y1, x2, y2, w) in P['rects']:
        rho = w / 8 / ((x2 - x1) * (y2 - y1))
        for (a1, b1, a2, b2) in d4_images(x1, y1, x2, y2, L):
            ex.append(f"{dec(a1,'up')} {dec(b1,'up')} {dec(a2,'dn')} {dec(b2,'dn')} {dec(rho,'dn')}")
    lines.append(str(len(ex))); lines += ex
    rs = list(range(last + 1)) if dirs is None else dirs
    lines.append(str(len(rs)))
    for r in rs:
        cn, sn, den = net_cs(r, D)
        assert den < 2 ** 53
        U = L - domain_margin(r, D, B)
        lines.append(f"{r} {cn} {sn} {den} {dec(U,'up')}")
    with open(out, 'w') as f:
        f.write("\n".join(lines) + "\n")
    return len(ex)

# ---------- exact evaluation (for confirming counterexamples) ----------
def _clip(poly, f):
    out = []
    n = len(poly)
    for i in range(n):
        P, Q = poly[i], poly[(i + 1) % n]
        fp, fq = f(P), f(Q)
        if fp <= 0: out.append(P)
        if (fp <= 0) != (fq <= 0):
            t = fp / (fp - fq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return out

def exact_F(P, r, cx, cy):
    """exact measure of the closed core at net index r centred at (cx,cy) (Fractions)"""
    L, B, D = P['L'], P['B'], P['D']
    cn, sn, den = net_cs(r, D)
    c, s = Fr(cn, den), Fr(sn, den)
    h = B / 2
    tot = Fr(0)
    ext = h * (c + s)
    for (x1, y1, x2, y2, w) in P['rects']:
        rho = w / 8 / ((x2 - x1) * (y2 - y1))
        for (a1, b1, a2, b2) in d4_images(x1, y1, x2, y2, L):
            if a2 <= cx - ext or a1 >= cx + ext or b2 <= cy - ext or b1 >= cy + ext: continue
            poly = [(a1 - cx, b1 - cy), (a2 - cx, b1 - cy), (a2 - cx, b2 - cy), (a1 - cx, b2 - cy)]
            for f in (lambda p: c * p[0] + s * p[1] - h, lambda p: -(c * p[0] + s * p[1]) - h,
                      lambda p: -s * p[0] + c * p[1] - h, lambda p: s * p[0] - c * p[1] - h):
                poly = _clip(poly, f)
                if len(poly) < 3: break
            if len(poly) < 3: continue
            A = Fr(0)
            for i in range(len(poly)):
                (xa, ya), (xb, yb) = poly[i], poly[(i + 1) % len(poly)]
                A += xa * yb - xb * ya
            tot += rho * abs(A) / 2
    return tot

if __name__ == '__main__':
    d = load_cert(sys.argv[1])
    ok, info, P = premises(d)
    print(json.dumps(info))
    if not ok:
        print("PREMISES_FAIL"); sys.exit(1)
    nex = write_instance(P, sys.argv[2])
    print("PREMISES_HOLD", "expanded_rects", nex)
