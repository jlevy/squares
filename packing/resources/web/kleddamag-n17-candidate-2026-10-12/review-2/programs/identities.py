"""Symbolic check of the 52 base-gap identities and the slider invariance, from my own layout transcription.

usage: identities.py GATE_RECEIPT AUDIT_JSON

For every one of the 52 labels: the base gap (wall: sign*(p_k+v_k) [+S for sign -1]; pair: n.d - 1/2 - n.v;
parallel: n.d - 1) is formed as a rational function of (t, b) with geom.layout over SymPy symbols; its numerator
must lie in the ideal <F, G> (reduction by a lex Groebner basis to zero), and its denominator must not vanish at
the Krawczyk-verified root (interval evaluation). The slider coefficients n.(dc/dw) must be identically zero as
rational functions. Also checks the three parallel offsets tau = Jn.d that are zero identically.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import itertools
import sympy as sp
from mpmath import iv, mp
import geom

t, b = sp.symbols('t b')
Fp = sp.expand(geom.F(t, b))
Gp = sp.expand(geom.G(t, b))


def main():
    labels = json.load(open(sys.argv[1]))['new_labels']
    audit = json.load(open(sys.argv[2]))['retained']
    normals = {}
    for key, opts in audit.items():
        l, r = map(int, key.split('-'))
        normals[(l, r)] = (opts[0][1], opts[0][2])
    side, pts, axes, aux = geom.layout(t, b, sp.Integer(1))
    GB = sp.groebner([Fp, Gp], t, b, order='lex')
    print('Groebner basis of <F,G>:', len(GB.exprs), 'elements; degrees',
          [sp.Poly(g, t, b).total_degree() for g in GB.exprs])
    T, B = geom.newton_root()
    rad = mp.mpf(10)**-100
    Ti, Bi = iv.mpf([T - rad, T + rad]), iv.mpf([B - rad, B + rad])

    def axis(lab, which):
        u = axes[lab - 1]
        return u if which == 0 else (-u[1], u[0])

    def corner(lab, c):
        ea, eb = list(itertools.product((-1, 1), repeat=2))[c]
        u = axis(lab, 0); v = axis(lab, 1)
        return (sp.Rational(ea, 2)*u[0] + sp.Rational(eb, 2)*v[0], sp.Rational(ea, 2)*u[1] + sp.Rational(eb, 2)*v[1])

    def slide(lab):
        u = axis(lab, 0); v = axis(lab, 1)
        if lab == 2:
            return [(-1, 0)]
        if lab == 11:
            return [(-v[0], -v[1])]
        if lab == 13:
            return [v]
        return []

    dot = lambda a, c: a[0]*c[0] + a[1]*c[1]
    ok = 0
    for label in labels:
        f = label.split(':')
        sliders = []
        if f[0] == 'wall':
            lab, c, k, sign = map(int, f[1:5])
            v = corner(lab, c)
            gap = sign*(pts[lab-1][k] + v[k]) + (side if sign == -1 else 0)
            sliders = [sign*w[k] for w in slide(lab)]
        else:
            l, r = int(f[1]), int(f[2])
            ax, sg = normals[(l, r)]
            if f[0] == 'pair':
                o, c = int(f[3]), int(f[4])
                tt = l if o == r else r
                n = tuple(sg*x for x in axis(o, ax))
                d = (pts[r-1][0] - pts[l-1][0], pts[r-1][1] - pts[l-1][1])
                gap = dot(n, d) - sp.Rational(1, 2) - dot(n, corner(tt, c))
            else:
                n = tuple(sg*x for x in axis(l, ax))
                d = (pts[r-1][0] - pts[l-1][0], pts[r-1][1] - pts[l-1][1])
                gap = dot(n, d) - 1
            sliders = [dot(n, w) for w in slide(r)] + [-dot(n, w) for w in slide(l)]
        num, den = sp.fraction(sp.together(sp.cancel(gap)))
        num = sp.expand(num)
        red = GB.reduce(num)[1] if num != 0 else 0
        assert red == 0, ('identity fails', label)
        dval = sp.lambdify((t, b), den, modules=[{'sqrt': iv.sqrt}])(Ti, Bi) if den.free_symbols else den
        if hasattr(dval, 'a'):
            assert not (dval.a <= 0 <= dval.b), ('denominator may vanish', label)
        else:
            assert dval != 0
        for sv in sliders:
            assert sp.simplify(sp.cancel(sv)) == 0, ('slider coefficient not identically zero', label)
        ok += 1
    # three axis-parallel tangential offsets used as exact zero
    for (l, r) in ((1, 3), (1, 5), (2, 6)):
        ax, sg = normals[(l, r)]
        n = tuple(sg*x for x in axis(l, ax))
        Jn = (-n[1], n[0])
        d = (pts[r-1][0] - pts[l-1][0], pts[r-1][1] - pts[l-1][1])
        assert sp.simplify(dot(Jn, d)) == 0, ('tau not zero', l, r)
    print('52 base-gap identities in <F,G>, denominators nonzero at the root, slider coefficients identically 0:', ok)
    print('tau = 0 identically for (1,3), (1,5), (2,6)')


if __name__ == '__main__':
    main()
