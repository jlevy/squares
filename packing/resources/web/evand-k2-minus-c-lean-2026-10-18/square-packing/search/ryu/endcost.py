"""End cost E(y) of a band end (Ryu §6-7 accounting): E(y) = A0(y) - |packing of Reg(y)|, A0(y) = y w + gam sig (1+b^2)/2,
Reg(y) = {0 <= X <= w, 0 <= Y <= y + (X - sig) mu}, mu = tan(theta).  Compares
  axis:  y = 0, one axis layer [x, x+1] x [0, 1] where the ceiling allows (what lean/Sqpack/RyuFill.lean uses), and
         general y with axis layers only;
  stair: Ryu's staircase end lemma (S1)-(S6) (columns of m squares at one tilt alpha + layers + wedge rows), best y.
Floats, exploration only.  python3 search/ryu/endcost.py B [B ...]
"""
import sys, math


def band(b):
    t = 1 / b                       # theta0 = 2 arctan(1/b): w = b exactly (the perturbation is negligible here)
    gam, sig = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    return b * gam + sig, sig / gam, sig, gam


def A0(b, y):
    w, mu, sig, gam = band(b)
    return y * w + gam * sig * (1 + b * b) / 2


def axis_count(b, y):
    """axis layers [x0, x0+L] x [j, j+1], x0 = first X with ceiling >= j+1, packed to the right wall."""
    w, mu, sig, gam = band(b)
    g = lambda X: y + (X - sig) * mu
    n = 0
    j = 0
    while True:
        x0 = max(0.0, sig + (j + 1 - y) / mu)        # g(x0) = j + 1
        if x0 >= w:
            break
        n += math.floor(w - x0 + 1e-12)
        j += 1
    return n


def stair_count(b, y, Q=10 ** 6):
    w, mu, sig0, gam = band(b)
    g = lambda X: y + (X - sig0) * mu
    g0, gbar = g(0), g(w)
    if g0 <= 1:
        return None
    m = math.floor(gbar) + 1
    Dm, delta = m + g0, m - g0
    tstar = (1 + math.sqrt(1 + Dm * delta)) / Dm
    t = math.ceil(tstar * Q) / Q
    if t >= 1:
        return None
    ca, sa = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    ta, se = 2 * t / (1 - t * t), (1 + t * t) / (1 - t * t)
    xi = lambda i: m * ta + i * se
    I = 0
    while xi(I) + se <= w:
        I += 1
    if I < 1:
        return None
    H = lambda J: J + (m - J) * ca + sa
    Js = [math.floor((g(xi(i) - m * ta) - m * ca - sa) / (1 - ca)) for i in range(I)]
    ns = [m - J for J in Js]
    count = sum(ns)
    import bisect
    def p(j): return bisect.bisect_right(Js, j)       # Js is nondecreasing
    a = lambda j: xi(p(j)) - j * ta
    j1 = -1
    for j in range(0, math.floor(gbar) + 1):           # largest j with g(a(j')) >= j' + 1 for all j' <= j
        if g(a(j)) >= j + 1:
            j1 = j
        else:
            break
    for j in range(0, j1 + 1):
        L = math.floor(w - a(j))
        if L >= 1:
            count += L
    for r in range(0, math.floor(g0)):
        l = math.floor((m - r - 1) * ta)
        if l >= 1:
            count += l
    return count


if __name__ == '__main__':
    for b in map(int, sys.argv[1:]):
        e_axis0 = A0(b, 0) - axis_count(b, 0)
        e_axis = min((A0(b, y) - axis_count(b, y), y) for y in [i / 20 for i in range(0, 200)])
        best = None
        for yi in range(1, 4000):
            y = yi / 20
            c = stair_count(b, y)
            if c is None:
                continue
            e = A0(b, y) - c
            if best is None or e < best[0]:
                best = (e, y)
        st = f'E={best[0]:8.2f} ({best[0]/b:.3f} b) at y={best[1]}' if best else 'infeasible'
        print(f'b={b:5d}  axis y=0: E={e_axis0:7.2f} ({e_axis0/b:.3f} b)   axis best y: E={e_axis[0]:7.2f} at y={e_axis[1]}'
              f'   staircase best: {st}')
