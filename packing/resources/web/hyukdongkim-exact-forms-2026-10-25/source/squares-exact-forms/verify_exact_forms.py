"""Re-derive and check the exact side lengths of the record packings for n = 88, 126, 172, 199, 263.

Usage:
    python verify_exact_forms.py ATLAS_DATA_DIR [DIGITS]

ATLAS_DATA_DIR is site/www/data/p of evand/square-packing (pinned revision in README.md);
the record coordinates are read from best-<n>.json there.

For each n:
  1. load the record packing (x, y, angle in degrees) and polish it to a local optimum with an
     exact-for-fixed-angles LP plus trust-region SLP (the side does not change beyond 1e-14);
  2. collect every active contact (SAT contact between squares, square-wall contact), with the
     |cos|, |sin| kinks resolved into sign branches;
  3. solve the KKT system   g(z) = 0,  e_s = sum_k lam_k grad g_k(z)   to DIGITS digits
     (mixed precision: frozen double pseudo-inverse, residuals in arb);
  4. check that the claimed polynomial P vanishes at the solved side to about DIGITS digits,
     that P is irreducible over Q, and which real root of P the side is.
Requires: numpy, scipy, python-flint, sympy.
"""
import json, math, os, sys, time
import numpy as np
import sympy as sp
from flint import arb, ctx

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lppolish as L
import exactform as E
import kkt_fast as KF


def main():
    data_dir = sys.argv[1]
    digits = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    claims = json.load(open(os.path.join(HERE, "exact_forms.json")))
    x = sp.symbols("x")
    ok_all = True
    for cl in claims:
        n = cl["n"]
        P_desc = [int(c) for c in cl["minimal_polynomial_descending"]]
        rec = json.load(open(os.path.join(data_dir, f"best-{n}.json")))
        a = np.array(rec["squares"], float)
        c, th, s = a[:, :2].copy(), np.radians(a[:, 2]), float(rec["s"])
        t0 = time.time()
        c2, th2, s2, _ = L.polish(c, th, s, iters=150)
        assert L.max_violation(c2, th2, s2) < 1e-9, "polished packing infeasible"
        z, lam, hist, info = KF.solve(n, c2, th2, s2, digits=digits)
        S = z[3 * n]
        val = sum(arb(cf) * S ** i for i, cf in enumerate(reversed(P_desc)))
        P = sp.Poly(P_desc, x)
        roots = P.real_roots()
        vals = [float(r.evalf(30)) for r in roots]
        k = min(range(len(vals)), key=lambda i: abs(vals[i] - s))
        exact_root = str(sp.N(roots[k], 40))
        lg_val = E.lg(val)
        ok = hist[-1] < -0.9 * digits and lg_val < -0.9 * digits + len(str(max(map(abs, P_desc)))) \
            and P.is_irreducible and exact_root[:35] == str(S.mid()).lstrip("[")[:35]
        ok_all &= ok
        print(f"n={n}: record s={s:.15f} polished s={s2:.15f}; {info['m']} active equations; "
              f"KKT residual 1e{hist[-1]:.0f}; |P(s)| = 1e{lg_val:.0f}; degree {P.degree()}, "
              f"irreducible={P.is_irreducible}; real root #{k + 1} of {len(vals)} = {exact_root[:32]}...  "
              f"{'OK' if ok else 'FAIL'} ({time.time() - t0:.0f}s)", flush=True)
    print("ALL OK" if ok_all else "SOME CHECK FAILED")


if __name__ == "__main__":
    main()
