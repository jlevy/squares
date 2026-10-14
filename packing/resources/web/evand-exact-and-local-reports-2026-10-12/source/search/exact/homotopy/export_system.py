"""Export minpoly.py's angle-class system for a record to a Julia file (for homotopy continuation).

    ./env.sh python3 homotopy/export_system.py minpoly/solve/n-29 homotopy/work/n29_system.jl

Writes: variables t1..tk; the k consistency polynomials msolve would get (F); t* (70 digits); S = Sn/Sd as a function
of t; the full contact system as affine forms in the centres and S with coefficients in Q(t) (rows: list of
(Dict(var => (num, den)), (knum, kden))), for filtering solutions where elimination's pivots degenerate.
"""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__file__) + '/..')
import minpoly as M
from mpmath import mp

base, out = sys.argv[1], sys.argv[2]
last_rows = []
orig_elim = M.eliminate


def elim(rows, tv):
    last_rows[:] = [rows]
    return orig_elim(rows, tv)


M.eliminate = elim


def jl(p):                       # flint fmpq_mpoly string -> Julia expression with exact rationals
    s = str(p)
    return re.sub(r'(\d+)/(\d+)', r'(big(\1)//\2)', s)


state = {}
orig_mf = M.multi_field


def mf(leftover, tv, base_, log, piv_rows, frozen=()):
    state['S'] = M.back_rf(piv_rows)['S']
    state['tv'] = tv
    return orig_mf(leftover, tv, base_, log, piv_rows, frozen)


def fake(polys, k, tag):
    rows = last_rows[0]
    S = state['S']
    with open(out, 'w') as f:
        f.write(f'# exported from {base} by export_system.py\n')
        f.write(f'@var ' + ' '.join(f't{i+1}' for i in range(k)) + '\n')
        f.write(f'tvars = [' + ', '.join(f't{i+1}' for i in range(k)) + ']\n')
        f.write('F = [\n' + ',\n'.join(jl(p) for p in polys) + '\n]\n')
        f.write('tstar = [' + ', '.join(f'big"{mp.nstr(x, 70)}"' for x in state['tv']) + ']\n')
        f.write(f'Sn = {jl(S.n)}\nSd = {jl(S.d)}\n')
        vs = sorted({v for r in rows for v in r.c})
        f.write('zvars = [' + ', '.join(f'"{v}"' for v in vs) + ']\n')
        f.write('rows = [\n')
        for r in rows:
            ent = ', '.join(f'"{v}" => ({jl(a.n)}, {jl(a.d)})' for v, a in r.c.items())
            f.write(f'  (Dict{{String,Any}}({ent}), ({jl(r.k.n)}, {jl(r.k.d)})),\n')
        f.write(']\n')
    print(f'wrote {out}: {len(polys)} polys, {len(rows)} rows, {len(vs)} unknowns', file=sys.stderr)
    raise SystemExit(0)


M.multi_field = mf
M.msolve_param = fake
M.run(base)
