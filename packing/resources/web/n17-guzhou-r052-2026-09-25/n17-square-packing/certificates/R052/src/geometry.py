"""Unchanged extracted geometry functions / 原样提取的几何函数。"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import combinations
from math import comb, lcm
import numpy as np
from numba import njit

def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def trig(t: Q) -> tuple[Q, Q]:
    return (1-t*t)/(1+t*t), 2*t/(1+t*t)


@njit(cache=False)
def _add(mn, lazy, arg, node, left, right, qleft, qright, delta):
    if qright <= left or right <= qleft:
        return
    if qleft <= left and right <= qright:
        mn[node] += delta
        lazy[node] += delta
        return
    mid = (left+right)//2
    _add(mn, lazy, arg, 2*node, left, mid, qleft, qright, delta)
    _add(mn, lazy, arg, 2*node+1, mid, right, qleft, qright, delta)
    if mn[2*node] <= mn[2*node+1]:
        mn[node] = lazy[node]+mn[2*node]
        arg[node] = arg[2*node]
    else:
        mn[node] = lazy[node]+mn[2*node+1]
        arg[node] = arg[2*node+1]


@njit(cache=False)
def _query(mn, lazy, arg, node, left, right, qleft, qright):
    if qright <= left or right <= qleft:
        return np.int64(2**60), np.int64(-1)
    if qleft <= left and right <= qright:
        return mn[node], arg[node]
    mid = (left+right)//2
    a, ia = _query(mn, lazy, arg, 2*node, left, mid, qleft, qright)
    b, ib = _query(mn, lazy, arg, 2*node+1, mid, right, qleft, qright)
    if a <= b:
        return lazy[node]+a, ia
    return lazy[node]+b, ib


@njit(cache=False)
def sweep_argmin(ycells, event_x, event_atom, event_sign,
                 ylo, yhi, weights, feasible_first, feasible_last):
    n = 1
    while n < ycells:
        n *= 2
    mn = np.zeros(2*n, dtype=np.int64)
    lazy = np.zeros(2*n, dtype=np.int64)
    arg = np.zeros(2*n, dtype=np.int64)
    for i in range(n):
        arg[n+i] = i
    for k in range(n-1, 0, -1):
        arg[k] = arg[2*k]
    cursor = 0
    best = np.int64(2**60)
    best_x = -1
    best_y = -1
    cell_count = 0
    for k in range(len(feasible_first)):
        while cursor < len(event_x) and event_x[cursor] == k:
            j = event_atom[cursor]
            _add(mn, lazy, arg, 1, 0, n, ylo[j], yhi[j],
                 event_sign[cursor]*weights[j])
            cursor += 1
        if feasible_first[k] < feasible_last[k]:
            z, iy = _query(mn, lazy, arg, 1, 0, n,
                           feasible_first[k], feasible_last[k])
            if z < best:
                best, best_x, best_y = z, k, iy
            cell_count += feasible_last[k]-feasible_first[k]
    return best, best_x, best_y, cell_count


def physical_sites(cert: dict) -> tuple[list[tuple[int, int]], list[int]]:
    scale = cert['coordinate_denominator']
    require(type(scale) is int and scale > 0, 'invalid coordinate denominator')
    side = Q(cert['L'])*scale
    require(side.denominator == 1, 'outer side not integral on site grid')
    outer = int(side)
    sites: list[tuple[int, int]] = []
    owners: list[int] = []
    for j, (x, y, weight) in enumerate(cert['point_orbits']):
        require(all(type(z) is int for z in (x, y, weight)) and
                0 <= x <= outer and 0 <= y <= outer and weight >= 0,
                'invalid point orbit')
        image = sorted({(a, b) for u, v in ((x, y), (y, x))
                        for a in (u, outer-u) for b in (v, outer-v)})
        sites.extend(image)
        owners.extend([j]*len(image))
    require(len(sites) == len(set(sites)), 'duplicate physical site')
    return sites, owners


def weight_vectors(cert: dict, override: dict | None) -> tuple[list[int], list[int], list[int]]:
    vectors = ([item[2] for item in cert['point_orbits']],
               [item['weight'] for item in cert['threshold_orbits']],
               [item['weight'] for item in cert.get('generic_trigger_orbits', [])])
    if override is None:
        pass
    elif 'nonzero' in override:
        vectors = tuple([0]*len(part) for part in vectors)
        types = {'point': 0, 'threshold': 1, 'generic': 2}
        seen = set()
        for item in override['nonzero']:
            family, index = types[item['type']], item['index']
            require(type(index) is int and 0 <= index < len(vectors[family]),
                    'override weight index outside fixed support')
            require((family, index) not in seen, 'duplicate override weight')
            seen.add((family, index))
            vectors[family][index] = item['weight_units']
    else:
        require(len(override['point_orbits']) == len(vectors[0]) and
                len(override['threshold_orbits']) == len(vectors[1]) and
                len(override.get('generic_trigger_orbits', [])) == len(vectors[2]),
                'override support length mismatch')
        require([item[:2] for item in override['point_orbits']] ==
                [item[:2] for item in cert['point_orbits']],
                'override point support mismatch')
        require([item['triples'] for item in override['threshold_orbits']] ==
                [item['triples'] for item in cert['threshold_orbits']] and
                [(item['k'], item['groups'])
                 for item in override.get('generic_trigger_orbits', [])] ==
                [(item['k'], item['groups'])
                 for item in cert.get('generic_trigger_orbits', [])],
                'override trigger support mismatch')
        vectors = ([item[2] for item in override['point_orbits']],
                   [item['weight'] for item in override['threshold_orbits']],
                   [item['weight'] for item in override.get('generic_trigger_orbits', [])])
    require(all(type(w) is int and w >= 0 for part in vectors for w in part),
            'weights must be nonnegative integers')
    return vectors


def row_geometry(cert: dict, row: int):
    require(0 <= row < len(cert['entries']), 'row out of range')
    L, A = Q(cert['L']), Q(cert['A'])
    a, b, t, B = map(Q, cert['entries'][row])
    require(0 <= a < b < 1 and a <= t <= b and 0 < B < A < L,
            'invalid row geometry')
    c, s = trig(t)
    fa, fb = sum(trig(a)), sum(trig(b))
    parent_t = a if fa <= fb else b
    parent_c, parent_s = trig(parent_t)
    radius = A*min(fa, fb)/2
    low, high = radius, L-radius
    require(low < high, 'parent legal-center domain has no interior')
    # Strict containment of the selected probe in every parent orientation
    # of this interval, following the original package's rational criterion.
    for endpoint in (a, b):
        ce, se = trig(endpoint)
        dot, cross = c*ce+s*se, abs(c*se-s*ce)
        require(dot > 0 and dot >= cross,
                'row angle too far from probe orientation')
        require(A-B*(dot+cross) > 0, 'probe not strictly in parent interval')
    require(B*(c+s)/2 <= radius, 'probe not contained by source envelope')
    return L, A, a, b, t, B, c, s, low, high, parent_t, parent_c, parent_s


def build_event_grid(cert: dict, row: int, sites: list[tuple[int, int]],
                     owners: list[int], weights: tuple[list[int], list[int], list[int]]):
    """Build weighted rectangle atoms and the legal polygon exactly once."""
    L, A, a, b, t, B, c, s, low, high, parent_t, parent_c, parent_s = row_geometry(cert, row)
    D = cert['coordinate_denominator']
    LD = int(L*D)
    p, q = t.numerator, t.denominator
    C, S, R = q*q-p*p, 2*p*q, q*q+p*p
    H = L/2-low
    scale = lcm(2*D, (B/2).denominator, H.denominator)
    factor = scale//(2*D)
    half = int(B*scale/2)*R
    h = int(H*scale)
    uv = [(C*(2*x-LD)*factor+S*(2*y-LD)*factor,
           -S*(2*x-LD)*factor+C*(2*y-LD)*factor) for x, y in sites]
    rectangles: dict[tuple[int, int, int, int], int] = {}

    def insert(indices, weight):
        if weight == 0:
            return
        xs = [uv[i][0] for i in indices]
        ys = [uv[i][1] for i in indices]
        rect = max(xs)-half, min(xs)+half, max(ys)-half, min(ys)+half
        if rect[0] < rect[1] and rect[2] < rect[3]:
            rectangles[rect] = rectangles.get(rect, 0)+weight

    for i, owner in enumerate(owners):
        insert((i,), weights[0][owner])
    require(len(cert['threshold_orbits']) == len(weights[1]), 'threshold weight length')
    for orbit, item in enumerate(cert['threshold_orbits']):
        for group in item['triples']:
            require(len(group) == 3 and len(set(group)) == 3 and
                    all(type(i) is int and 0 <= i < len(sites) for i in group),
                    'bad threshold triple')
            for size in (2, 3):
                for subset in combinations(group, size):
                    insert(subset, weights[1][orbit]*(1 if size == 2 else -2))
    generic = cert.get('generic_trigger_orbits', [])
    require(len(generic) == len(weights[2]), 'generic weight length')
    for orbit, item in enumerate(generic):
        k = item['k']
        for group in item['groups']:
            require(1 <= k <= len(group) and len(set(group)) == len(group) and
                    all(type(i) is int and 0 <= i < len(sites) for i in group),
                    'bad generic group')
            for size in range(k, len(group)+1):
                coeff = (-1 if (size-k)%2 else 1)*comb(size-1, k-1)
                for subset in combinations(group, size):
                    insert(subset, weights[2][orbit]*coeff)
    rectangles = {r: w for r, w in rectangles.items() if w}
    require(sum(abs(w) for w in rectangles.values()) < 2**50,
            'signed rectangle mass too large for int64 sweep')
    # Coordinates are integer numerators with common denominator R*scale.
    polygon = [(C*x+S*y, -S*x+C*y)
               for x, y in ((-h, -h), (h, -h), (h, h), (-h, h))]
    xe = sorted({x for x, _ in polygon} | {v for r in rectangles for v in r[:2]})
    ye = sorted({y for _, y in polygon} | {v for r in rectangles for v in r[2:]})
    require(len(xe) >= 2 and len(ye) >= 2, 'empty event grid')
    xi = {x: i for i, x in enumerate(xe)}
    yi = {y: i for i, y in enumerate(ye)}
    atoms = list(rectangles.items())
    events = sorted([(xi[r[0]], i, 1) for i, (r, _) in enumerate(atoms)] +
                    [(xi[r[1]], i, -1) for i, (r, _) in enumerate(atoms)])
    return {
        'L': L, 'A': A, 't': t, 'B': B, 'c': c, 's': s,
        'low': low, 'high': high, 'parent_t': parent_t,
        'parent_c': parent_c, 'parent_s': parent_s,
        'scale_denominator': R*scale, 'polygon': polygon,
        'x_events': xe, 'y_events': ye, 'atoms': atoms, 'events': events,
        'ylo': [yi[r[2]] for r, _ in atoms],
        'yhi': [yi[r[3]] for r, _ in atoms],
    }

