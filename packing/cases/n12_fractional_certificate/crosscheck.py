# ruff: noqa
# Provenance: independent reviewer's break test, 2026-09-04; see independent_verify.py.
"""Slow, deliberately naive cross-check of the C4 minimum, done the way the task
describes: full grid of edge coordinates AND midpoints, feasibility by testing the
four corners of the rotated B-square against [0,L]^2 exactly, mass summed atom by
atom with Fractions.  Compares against verify.py's fast exact answer."""
from fractions import Fraction as Fr
import sys, time
sys.path.insert(0, "/tmp/claude-0/-home-user-squares/21ae3bfc-58a6-55fc-90e3-6e29d229a7f1/scratchpad/indep")
from verify import load, net, direction_min
import numpy as np

def naive(cert, t):
    L, B, atoms = cert["L"], cert["B"], cert["atoms"]
    p, q = t.numerator, t.denominator
    A, Bb, m = q*q - p*p, 2*p*q, q*q + p*p
    c, s = Fr(A, m), Fr(Bb, m)              # cos theta, sin theta
    H = B / 2
    # rotated-frame atom coords (unscaled)
    R = [(x*c + y*s, -x*s + y*c) for x, y, _ in atoms]
    ub = sorted({a + d for a, _ in R for d in (-H, H)})
    vb = sorted({b + d for _, b in R for d in (-H, H)})
    def grid(bs):
        g = []
        for i, z in enumerate(bs):
            if i: g.append((bs[i-1] + z) / 2)
            g.append(z)
        return [bs[0] - 1] + g + [bs[-1] + 1]
    U, V = grid(ub), grid(vb)
    best, arg = None, None
    for u in U:
        for v in V:
            ok = True
            for du in (-H, H):
                for dv in (-H, H):
                    uu, vv = u + du, v + dv
                    x = uu*c - vv*s; y = uu*s + vv*c        # back to xy
                    if not (0 <= x <= L and 0 <= y <= L):
                        ok = False; break
                if not ok: break
            if not ok:
                continue
            tot = Fr(0)
            for i, (a, b) in enumerate(R):
                if abs(a - u) <= H and abs(b - v) <= H:
                    tot += atoms[i][2]
            if best is None or tot < best:
                best, arg = tot, (u, v)
    return best, arg

if __name__ == "__main__":
    base = "/home/user/squares/packing/cases/n12_fractional_certificate/"
    for name in ("certificate-19-5.json", "certificate.json"):
        cert = load(base + name)
        ts = net(cert)
        atoms = cert["atoms"]
        def _g(a,b):
            while b: a,b=b,a%b
            return a
        den = 1
        for _,_,w in atoms: den = den*w.denominator//_g(den, w.denominator)
        wint = np.array([int(w*den) for _,_,w in atoms], dtype=np.int64)
        for k in (0, 1, 57, 180):
            t0 = time.time(); nb, narg = naive(cert, ts[k]); dtn = time.time()-t0
            t1 = time.time(); lo, rp, arg = direction_min(cert, ts[k], wint, den); dtf = time.time()-t1
            print("%-24s k=%-4d naive=%-8s fast_lower=%-8s fast_rep=%-8s  agree=%s  (%.1fs vs %.2fs)"
                  % (name, k, nb, Fr(lo, den), Fr(rp, den),
                     nb == Fr(lo, den) == Fr(rp, den), dtn, dtf))
