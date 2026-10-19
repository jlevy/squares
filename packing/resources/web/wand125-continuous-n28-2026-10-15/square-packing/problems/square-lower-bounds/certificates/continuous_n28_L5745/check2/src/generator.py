"""Exact parsing and conservative kernel input generation (standard library only)."""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
G = 10**9
DEFAULT_ENDPOINTS = [1, 500] + list(range(10000, 410001, 10000)) + [415000]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def local(path):
    p = Path(path).resolve()
    require(p.is_relative_to(ROOT), 'Path must stay inside this folder')
    return p

def sha(path):
    return hashlib.sha256(local(path).read_bytes()).hexdigest()

def pairs(items):
    d = {}
    for k, v in items:
        require(k not in d, 'Duplicate JSON key: ' + k)
        d[k] = v
    return d

def load(path):
    def bad(v):
        raise ValueError('Nonfinite JSON: ' + v)
    return json.loads(local(path).read_text(), parse_float=Q,
                      parse_constant=bad, object_pairs_hook=pairs)

def save(path, obj):
    local(path).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')

def expand(coords, mass, L):
    a, b, c, e = map(Q, coords)
    require(0 <= a < c <= L and 0 <= b < e <= L, 'Rectangle outside support or degenerate')
    rho = mass / (8 * (c-a) * (e-b))
    rows, other = [], []
    for swap in (False, True):
        x0,y0,x1,y1 = (b,a,e,c) if swap else (a,b,c,e)
        for fx in (False, True):
            for fy in (False, True):
                xx0,xx1 = (L-x1,L-x0) if fx else (x0,x1)
                yy0,yy1 = (L-y1,L-y0) if fy else (y0,y1)
                rows.append((xx0,yy0,xx1,yy1,rho))
    for reflect in (False, True):
        x0,y0,x1,y1 = (L-c,b,L-a,e) if reflect else (a,b,c,e)
        for _ in range(4):
            other.append((x0,y0,x1,y1,rho))
            x0,y0,x1,y1 = L-y1,x0,L-y0,x1
    require(Counter(rows) == Counter(other), 'D4 reconciliation')
    return rows, other

def read_candidate(candidate, params=None):
    d = load(candidate)
    L = Q(d['L'])
    require(0 < L < 12, 'Side must be positive and less than 12')
    require(type(d['n']) is int and d['n'] > 0, 'Invalid n')
    require(not d.get('points', []), 'Nonempty points are unsupported')
    p = load(params) if params else {}
    if 'weights' in d:
        fmt = 'guzhou'
        require(len(d['weights']) == len(d['rectangles']), 'Rectangle/weight length mismatch')
        items = zip(d['rectangles'], d['weights'])
        mass = Q(d['mass'])
    else:
        fmt = 'mixed'
        items = ((r['rectangle'], r['mass']) for r in d['rectangles'])
        mass = Q(d['total_mass'])
    if p:
        require(Q(p['L']) == L and p['n'] == d['n'], 'Parameter L/n mismatch')
        require(Q(p['mass']) == mass, 'Parameter mass mismatch')
    rows, other, total = [], [], Q(0)
    for coords, wt in items:
        wt = Q(wt)
        require(wt >= 0, 'Negative mass')
        # Validate even zero-mass representatives.
        r, s = expand(coords, wt, L)
        if wt:
            rows.extend(r)
            other.extend(s)
        total += wt
    require(total == mass, 'Mass sum mismatch')
    require(0 < len(rows) <= 20000, 'Positive rectangle count outside kernel cap')
    require(sum((c-a)*(e-b)*w for a,b,c,e,w in rows) == mass, 'Expanded mass mismatch')
    return dict(format=fmt, L=L, mass=mass, n=d['n'], rows=rows, axis_rows=other)

def enclose(x, hexadecimal=False):
    x = Q(x)
    v = float(x)
    require(math.isfinite(v), 'Float overflow')
    lo = v if Q(v) <= x else math.nextafter(v, -math.inf)
    hi = v if Q(v) >= x else math.nextafter(v, math.inf)
    require(math.isfinite(lo) and math.isfinite(hi) and Q(lo) <= x <= Q(hi), 'Outward enclosure failed')
    return lo.hex() + ' ' + hi.hex() if hexadecimal else f'{lo:.17g} {hi:.17g}'

def floor(x):
    return x.numerator // x.denominator

def ceil(x):
    return -floor(-x)

def generate(candidate, out, B, tau, epsilon, params=None):
    out = local(out)
    out.mkdir(parents=True, exist_ok=True)
    cert = read_candidate(candidate, params)
    L = cert['L']
    require(0 < B < L and tau > 0, 'Invalid core or threshold')
    require(0 < epsilon <= Q(1, 1000), 'Near-axis epsilon outside supported band')
    # Choose the largest even grid side strictly below B/W(epsilon).
    width = (1+2*epsilon-epsilon**2)/(1+epsilon**2)
    A = Q(2*(ceil(B/width*G/2)-1), G)
    # Reproduce the frozen regression patch exactly when applicable.
    if B == Q(199529,200000) and epsilon == Q(1,10**6):
        A = Q(997643,10**6)
    margin = B-A*width
    require(0 < A < B and margin > 0, 'Near-axis containment failed')
    ll, ab = int(L*G), int(A*G)
    require(Q(ll,G) == L and ll % 2 == 0 and ab % 2 == 0, 'L and A require even integer grid units')
    pose = enclose(L,True)+'\n'+enclose(B)+'\n'+str(len(cert['rows']))+'\n'
    pose += ''.join(' '.join(enclose(x,True) for x in row)+'\n' for row in cert['rows'])
    # Coordinates use the fixed 10^9 grid. The kernel independently accepts
    # a density denominator P; lower it only when needed to retain all guards.
    P = G
    while True:
        rr = []
        for a,b,c,e,w in cert['axis_rows']:
            aa,bb,cc,ee,ww = ceil(a*G),ceil(b*G),floor(c*G),floor(e*G),floor(w*P)
            if aa < cc and bb < ee and ww > 0:
                require(Q(aa,G)>=a and Q(bb,G)>=b and Q(cc,G)<=c and Q(ee,G)<=e and Q(ww,P)<=w, 'Integer domination failed')
                rr.append((aa,bb,cc,ee,ww))
        weights = sum(r[4] for r in rr)
        bound = 16*weights*(2*ll+ab//2)**2
        if weights < 10**15 and bound < 2**125:
            break
        require(P > 1, 'Axis overflow bound exceeded')
        P //= 10
    require(Counter(rr) == Counter((ll-e,a,ll-b,c,w) for a,b,c,e,w in rr), 'Axis quarter-turn symmetry failed')
    require(tau.numerator <= 10**6 and tau.denominator <= 10**6, 'Axis threshold limits exceeded')
    axis = f'{ll} {ab} {G} {P} {tau.numerator} {tau.denominator} {len(rr)}\n'
    axis += ''.join(' '.join(map(str,r))+'\n' for r in rr)
    (out/'certificate_input.txt').write_text(pose)
    (out/'axis_input.txt').write_text(axis)
    manifest = {'candidate_sha256':sha(candidate), 'params_sha256':sha(params) if params else None,
                'files':{name:sha(out/name) for name in ('certificate_input.txt','axis_input.txt')},
                'format':cert['format'], 'terms':len(cert['rows']), 'axis_terms':len(rr),
                'L':str(L), 'B':str(B), 'mass':str(cert['mass']), 'tau':str(tau),
                'epsilon':str(epsilon), 'axis_side':str(A), 'axis_containment_margin':str(margin),
                'axis_evaluation_bound':str(bound), 'axis_coordinate_denominator':G,
                'axis_density_denominator':P, 'axis_scale':str(P*G*G)}
    save(out/'manifest.json',manifest)
    return cert, manifest

if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate',required=True);p.add_argument('--params')
    p.add_argument('--out',required=True);p.add_argument('--core',type=Q,required=True)
    p.add_argument('--tau',type=Q,required=True);p.add_argument('--epsilon',type=Q,default=Q(1,10**6))
    a=p.parse_args()
    _,m=generate(a.candidate,a.out,a.core,a.tau,a.epsilon,a.params)
    print(json.dumps(m,sort_keys=True))
