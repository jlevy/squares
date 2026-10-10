"""精确密度、有限上界及角网转移。
Exact density, finite upper bounds and angular-net transfer.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

PIN = '71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0'
PARAMS = {'n': 40, 'L': '67/10', 'B': '9977/10000', 'D': '83/80000',
          'last': 400, 'X': '335427/50000', 'h': '514946944479/1000000000000000',
          'tau': '10001/10000', 'mass': '3999/100',
          'H': '2818711359413/1000000000', 'charge': '99979/100000'}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def unique(items):
    result = {}
    for key, value in items:
        require(key not in result, 'DUPLICATE_JSON_KEY')
        result[key] = value
    return result

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      parse_float=Q, object_pairs_hook=unique)

def read_source(path):
    require(sha(path) == PIN, 'SOURCE_IDENTITY')
    data = read_json(path)
    require(data['n'] == 40 and Q(data['L']) == Q(67, 10)
            and Q(data['B']) == Q(9977, 10000), 'SOURCE_PARAMETERS')
    require(len(data['rectangles']) == len(data['weights']), 'SOURCE_LENGTHS')
    positive = []
    for coords, value in zip(data['rectangles'], data['weights']):
        weight = Q(value)
        require(weight >= 0 and len(coords) == 4, 'SOURCE_ROW')
        if not weight:
            continue
        a, b, c, d = map(Q, coords)
        require(0 <= a < c <= Q(67, 10) and 0 <= b < d <= Q(67, 10), 'SOURCE_SUPPORT')
        positive.append(((a, b, c, d), weight))
    require(len(positive) == 480 and sum(w for _, w in positive) == Q(3999, 100), 'SOURCE_MASS')
    return positive

def expand_rotations(positive):
    L = Q(67, 10)
    result = []
    for (a, b, c, d), w in positive:
        rho = w / (8 * (c-a) * (d-b))
        for reflected in (False, True):
            x1, y1, x2, y2 = (L-c, b, L-a, d) if reflected else (a, b, c, d)
            for _ in range(4):
                result.append((x1, y1, x2, y2, rho))
                x1, y1, x2, y2 = L-y2, x1, L-y1, x2
    return result

def expand_vertices(positive):
    origin = Q(67, 20)
    result = []
    for (a, b, c, d), w in positive:
        corners = [(x-origin, y-origin) for x in (a, c) for y in (b, d)]
        rho = w / (8 * (c-a) * (d-b))
        for swap in (False, True):
            for sx in (-1, 1):
                for sy in (-1, 1):
                    points = [(origin+sx*(y if swap else x), origin+sy*(x if swap else y))
                              for x, y in corners]
                    result.append((min(p[0] for p in points), min(p[1] for p in points),
                                   max(p[0] for p in points), max(p[1] for p in points), rho))
    return result

def derived_candidate(positive):
    return {'n': 40, 'L': PARAMS['L'], 'B': PARAMS['B'],
            'rectangles': [[str(v) for v in box] for box, _ in positive],
            'weights': [str(w) for _, w in positive],
            'coverage_lower_bound_exact': PARAMS['tau'],
            'certificate': {'L': PARAMS['L'], 'B': PARAMS['B'],
                            'D': PARAMS['D'], 'angle_count': 401}}

def candidate_bytes(positive):
    return (json.dumps(derived_candidate(positive), sort_keys=True, separators=(',', ':'))+'\n').encode()

def rounded_events(rows):
    ys = sorted({v for r in rows for v in (r[1], r[3])})
    yi = {y: i for i, y in enumerate(ys)}
    events = defaultdict(list)
    for a, b, c, d, rho in rows:
        require(a < c and b < d and rho >= 0, 'ENVELOPE_ROW')
        w = -(-(rho.numerator * 10**9) // rho.denominator)
        require(Q(w, 10**9) >= rho, 'ROUNDING_DIRECTION')
        events[a].append((yi[b], yi[d], w))
        events[c].append((yi[b], yi[d], -w))
    return ys, events

def peak_tree(rows):
    ys, events = rounded_events(rows)
    n = len(ys)-1
    require(n > 0, 'EMPTY_ENVELOPE')
    maximum, lazy = [0]*(4*n+8), [0]*(4*n+8)
    def update(left, right, value, node=1, lo=0, hi=n):
        if right <= lo or hi <= left:
            return
        if left <= lo and hi <= right:
            maximum[node] += value
            lazy[node] += value
            return
        mid = (lo+hi)//2
        update(left, right, value, 2*node, lo, mid)
        update(left, right, value, 2*node+1, mid, hi)
        maximum[node] = lazy[node]+max(maximum[2*node], maximum[2*node+1])
    peak = 0
    xs = sorted(events)
    for index, x in enumerate(xs):
        for left, right, value in events[x]:
            update(left, right, value)
        if index+1 < len(xs):
            peak = max(peak, maximum[1])
    require(maximum[1] == 0, 'TREE_BALANCE')
    return Q(peak, 10**9)

def peak_scan(rows):
    # 独立事件构造；Python 整数无固定宽度溢出。
    # Independently constructed events; Python integers have no fixed-width overflow.
    y = sorted(set([r[1] for r in rows]+[r[3] for r in rows]))
    indices = dict(zip(y, range(len(y))))
    events = defaultdict(Counter)
    for left, bottom, right, top, density in rows:
        scaled = density * 10**9
        height = scaled.numerator // scaled.denominator
        if scaled.denominator != 1:
            height += 1
        lower, upper = indices[bottom], indices[top]
        events[left][lower] += height
        events[left][upper] -= height
        events[right][lower] -= height
        events[right][upper] += height
    differences = [0]*len(y)
    largest = 0
    xs = sorted(events)
    for i, x in enumerate(xs):
        for j, change in events[x].items():
            differences[j] += change
        height = 0
        for change in differences:
            height += change
            require(height >= 0, 'SCAN_NEGATIVE_HEIGHT')
            if i+1 < len(xs):
                largest = max(largest, height)
        require(height == 0, 'SCAN_PREFIX_BALANCE')
    require(not any(differences), 'SCAN_EVENT_BALANCE')
    return Q(largest, 10**9)

def cs(t):
    return (1-t*t)/(1+t*t), 2*t/(1+t*t)

def transfer(parameters, peak):
    require(parameters == PARAMS, 'FIXED_PARAMETERS')
    L, B, D, X, h, tau, M, simple = [Q(parameters[k]) for k in ('L','B','D','X','h','tau','mass','charge')]
    require(peak == Q(parameters['H']), 'DENSITY_PEAK')
    q = L/X
    require(0 < h < D and 2*h <= 1-h*h and q >= B, 'TRANSFER_DOMAIN')
    c0, s0 = cs(h)
    require(B*(c0+s0) <= q, 'UPPER_NODE_CONTAINMENT')
    require((1+400*D)**2 > 2 and 400*D <= Q(1, 2), 'NET_REACH')
    require(all(0 < D/(1+j*(j+1)*D*D) <= D for j in range(400)), 'NET_GAPS')
    b = (D-h)/(1+D*h)
    require(0 < b and 2*b <= 1-b*b, 'CAP_ANGLE')
    c, s = cs(b)
    excess = max(Q(0), B*(c+s)-q)
    area = excess*excess/(2*c*s)
    charge = tau-peak*area
    require(charge >= simple and 40*simple > M, 'COUNTING_CONTRADICTION')
    uncut_squared = L*L*(1+D*D)/(B*B*(1+D)**2)
    require(Q('6.70848908')**2 < uncut_squared and 40*tau > M, 'UNCUT_BOUND')
    return {'X': str(X), 'parent_side': str(q), 'h': str(h), 'b': str(b),
            'density_upper': str(peak), 'cap_area_upper': str(area), 'charge_lower': str(charge),
            'simple_charge': str(simple), 'counting_margin': str(40*charge-M),
            'simple_counting_margin': str(40*simple-M), 'uncut_side_squared': str(uncut_squared)}

def finite_check(candidate, parameters):
    positive = read_source(candidate)
    first, second = expand_rotations(positive), expand_vertices(positive)
    require(Counter(first) == Counter(second) and len(first) == 3840, 'D4_EXPANSION')
    mass = sum((c-a)*(d-b)*rho for a,b,c,d,rho in first)
    require(mass == Q(3999,100), 'EXPANDED_MASS')
    a, b = peak_tree(first), peak_scan(second)
    require(a == b, 'INDEPENDENT_ENVELOPES')
    return positive, transfer(parameters, a)

def validate_nodes(summary, rows, candidate_digest):
    require(summary['kind'] == 'sqverify-fast-summary/v1' and summary['status'] == 'VERIFIED', 'NODE_SUMMARY')
    require(summary['refused_directions'] == [] and summary['fault_injected_at_box'] is None, 'NODE_REFUSAL')
    require(Q(summary['threshold']) == Q(PARAMS['tau']), 'NODE_THRESHOLD')
    p = summary['premises']
    require(p['n'] == 40 and p['angle_count'] == 401 and p['centre_domain'] == 'tokoharu'
            and p['input_sha256'] == candidate_digest and p['net_origin'] == 'metadata', 'NODE_PREMISES')
    for key, expected in [('L','67/10'),('B','9977/10000'),('D','83/80000'),('mass_exact','3999/100')]:
        require(Q(p[key]) == Q(expected), 'NODE_PARAMETER:'+key)
    require(len(rows) == 401 and sorted(r['r'] for r in rows) == list(range(401)), 'NODE_COMPLETENESS')
    for row in rows:
        require(row['verdict'] == 'verified' and Q(row['threshold']) == Q(PARAMS['tau']), 'NODE_VERDICT')
        require(row.get('fault_injected_at_box') is None, 'NODE_FAULT')
        value = row['min_certified_lower_bound']
        require(isinstance(value, (float,int)) and Q.from_float(float(value)) >= Q(PARAMS['tau']), 'NODE_LOWER_BOUND')
        if row['r'] == 0:
            require(row['method'] == 'axis-vertex-sweep' and row['vertices'] > 0, 'AXIS_SCOPE')
        else:
            require(row['method'] == 'interval-branch-and-bound' and row['nodes'] > 0
                    and row['leaves'] > 0, 'NONAXIS_SCOPE')
    return True
