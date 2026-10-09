"""Band (wall-to-wall row) local-minimum certificates for the axis-parallel records (S = k an integer).

Lean side: lean/Sqpack/ChainLocalMin.lean, `isLocalMin_of_axisCert`.  The certificate is the record itself
(rational centres, all angles 0) and a band: k square indices whose centres lie within 1/2 - m of a line y = y0.
Notes: tasks/exact-minpoly/chain-lemma.md.

  python3 chain_lean.py --survey               # which integer-S records have a band (n <= 324)
  python3 chain_lean.py N [out.lean]           # write lean/Sqpack/Exact/N<N>Chain.lean (default path)
  python3 chain_lean.py --upto 82 [out.lean]   # all integer-side records n <= 82 in Exact/ChainUpTo82.lean

Input: batch/certs/n-N.cert (exact, scaled by S_cert / k) and batch/results.json (S_exact).  Stdlib only.
"""
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.join(HERE, '..', '..', 'lean', 'Sqpack', 'Exact')


def results():
    return {r['n']: r for r in json.load(open(os.path.join(HERE, 'batch', 'results.json')))}


def integer_side(r):
    """k if the record's exact side is an integer, else None."""
    try:
        S = F(r['S_exact'])
    except (KeyError, TypeError, ValueError):
        return None
    k = round(S)
    return k if abs(S - k) < F(1, 10 ** 30) else None


def load_cert(n):
    L = [l for l in open(os.path.join(HERE, 'batch', 'certs', f'n-{n}.cert')).read().split('\n')
         if l.strip() and not l.startswith('#')]
    nn, S = L[0].split()
    sq = [tuple(map(F, l.split())) for l in L[1:1 + int(nn)]]
    return F(S), sq


def axis_ok(S, P):
    """Python twin of `axisOK` (ChainLocalMin.lean)."""
    h = F(1, 2)
    if not all(h <= x <= S - h and h <= y <= S - h for x, y in P):
        return False
    return all(abs(P[i][0] - P[j][0]) >= 1 or abs(P[i][1] - P[j][1]) >= 1
               for i in range(len(P)) for j in range(i + 1, len(P)))


def simplify(P, S):
    """Small-denominator centres (within 1e-12) if they pass `axis_ok`; else P unchanged."""
    def nice(v):
        for D in (2, 4, 8, 16, 32, 64, 128, 256, 1024, 4096, 2 ** 16, 2 ** 20):
            q = F(round(v * D), D)
            if abs(q - v) < F(1, 10 ** 12):
                return q
        return v.limit_denominator(10 ** 6)
    Q = [(nice(x), nice(y)) for x, y in P]
    return Q if axis_ok(S, Q) else P


def record(n, r=None):
    """(k, P) with P the exact record at side k (axis-parallel), or None."""
    r = r or results()[n]
    k = integer_side(r)
    if k is None:
        return None
    Sc, sq = load_cert(n)
    if any(t != 0 for _, _, t in sq):
        return None
    sc = F(k) / Sc
    # the cert is the exact record scaled up by ~(1 + 1e-20) (plus slack): snap back to small denominators
    P = simplify([(x * sc, y * sc) for x, y, _ in sq], k)
    if not axis_ok(k, P):
        raise SystemExit(f'n={n}: the snapped record fails axis_ok')
    return k, P


def find_band(P, k, coord=1):
    """k indices whose coordinate `coord` spreads < 1 (largest margin first), with y0 and m; or None."""
    idx = sorted(range(len(P)), key=lambda i: P[i][coord])
    best = None
    for a in range(len(idx)):
        if a + k - 1 >= len(idx):
            break
        lo, hi = P[idx[a]][coord], P[idx[a + k - 1]][coord]
        if hi - lo < 1:
            m = F(1, 2) - (hi - lo) / 2
            if best is None or m > best[2]:
                best = (sorted(idx[a:a + k], key=lambda i: P[i][1 - coord]), (lo + hi) / 2, m)
    return best


def lq(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else f'{q.numerator}/{q.denominator}'


def block(n, space='Chain'):
    """The Lean namespace certifying record n; returns (text, summary)."""
    rec = record(n)
    if rec is None:
        raise SystemExit(f'n={n}: not an axis-parallel integer-side record')
    k, P = rec
    band = find_band(P, k)
    if band is None:
        raise SystemExit(f'n={n}: no horizontal band of {k} squares')
    B, y0, m = band
    pts = ',\n    '.join(f'(({lq(x)} : ℚ), ({lq(y)} : ℚ))' for x, y in P)
    cast = 'Nat.cast_one' if k == 1 else 'Nat.cast_ofNat'
    text = f'''namespace UnitSquarePacking.{space}.N{n}

set_option maxRecDepth 100000

/-! Register record n = {n}, side {k}, all squares axis-parallel (`batch/certs/n-{n}.cert`, unscaled to side {k}).
Band: squares {B} (0-based), centres within `1/2 - m` of `y = {lq(y0)}`, `m = {lq(m)}`. -/

/-- The record's centres (angles all `0`). -/
def P : List (ℚ × ℚ) := [
    {pts}]

/-- The band: `{k}` squares spanning the container from wall to wall. -/
def band : List ℕ := {list(B)}

theorem axis_ok : axisOK ({k} : ℕ) P = true := by decide +kernel

theorem band_ok : bandOK P {n} {k} band ({lq(y0)} : ℚ) ({lq(m)} : ℚ) = true := by decide +kernel

/-- **The n = {n} record (side {k}) is a local minimum of the side.** -/
theorem localMin : IsLocalMinPacking {n} {k} (fun i => cenOf P i) (fun _ => 0) := by
  have h := isLocalMin_of_axisCert (n := {n}) (k := {k}) P band _ _ rfl axis_ok band_ok
  rwa [{cast}] at h

end UnitSquarePacking.{space}.N{n}
'''
    return text, f'n={n}: k={k}, band {B}, y0={y0}, m={m}'


HEAD = '''import Sqpack.ChainLocalMin

/-! Generated by `search/exact/chain_lean.py` ({what}).  Each record is axis-parallel with integer side `k` and
has `k` squares in a row from wall to wall; `isLocalMin_of_axisCert` (`ChainLocalMin.lean`) turns the record and
that row into `IsLocalMinPacking` (ball radius `m / 2` in pose space).  No multipliers, no field arithmetic. -/

'''


def emit(n, out=None):
    out = out or os.path.join(LEAN, f'N{n}Chain.lean')
    text, summ = block(n)
    open(out, 'w').write(HEAD.format(what=f'`python3 chain_lean.py {n}`') + text)
    print(summ, '->', out)


def emit_upto(lim, out=None):
    out = out or os.path.join(LEAN, f'ChainUpTo{lim}.lean')
    R = results()
    ns = [n for n in sorted(R) if n <= lim and record(n, R[n]) is not None]
    parts = [block(n, f'ChainUpTo{lim}')[0] for n in ns]
    open(out, 'w').write(HEAD.format(what=f'`python3 chain_lean.py --upto {lim}`: {len(ns)} records, n = '
                                     + ', '.join(map(str, ns))) + '\n'.join(parts))
    print(f'{len(ns)} records -> {out}')


def survey():
    R = results()
    rows = []
    for n in sorted(R):
        rec = record(n, R[n])
        if rec is None:
            continue
        k, P = rec
        bh, bv = find_band(P, k, 1), find_band(P, k, 0)
        rows.append((n, k, bh, bv))
    for lim in (82, 324):
        sel = [r for r in rows if r[0] <= lim]
        h = [r[0] for r in sel if r[2]]
        v = [r[0] for r in sel if r[3]]
        none = [r[0] for r in sel if not r[2] and not r[3]]
        stag = [r[0] for r in sel if r[2] and r[2][2] < F(1, 2)]
        print(f'n <= {lim}: {len(sel)} integer-side records; horizontal band {len(h)}, vertical band {len(v)}, '
              f'none {len(none)} {none}; staggered (m < 1/2) bands {stag}')
        print('  n:', ' '.join(map(str, [r[0] for r in sel])))


if __name__ == '__main__':
    if sys.argv[1:] == ['--survey']:
        survey()
    elif sys.argv[1] == '--upto':
        emit_upto(int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        emit(int(sys.argv[1]), sys.argv[2] if len(sys.argv) > 2 else None)
