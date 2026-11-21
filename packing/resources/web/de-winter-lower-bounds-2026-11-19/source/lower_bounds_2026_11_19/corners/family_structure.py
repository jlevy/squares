#!/usr/bin/env python3
"""Validate a family using exact rational arithmetic (standard library only).

Check input format and nonnegativity (SPEC.md §3); the wall profile on the
1/5 grid, reflection/transposition, wall mass 9/5 per period, and corner separation.
Recompute the saving S at both endpoints, require equality with stored S_d0/S_d1,
and check the target lower bound. For δ = d0 and d1 and k = 7, 8, 9, check the
total-mass identity a² − 4S, support inside the container, C4 invariance, and
agreement with the local model in the window [0, 24/5]². Check the reduction of
k ≥ 10 by integer wall shifts and the terminal line, and the right-side family
derivation (--right). See SPEC.md §7.1 for the acceptance order.
Leaf checks are performed by replay4d, not this script.
Usage: python3 validate_family.py family.json --right family_right.json [--open-left]
"""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
import json
import re
import sys

# Disable the decimal integer conversion limit to preserve arbitrary-precision input.
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)

ALPHA = Q(9, 5)
WINDOW = Q(24, 5)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rational(value, where):
    require(isinstance(value, str) and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?', value),
            f'{where}: expected an integer or p/q string: {value!r}')
    return Q(value)


def load(path):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            require(key not in out, f'duplicate JSON key: {key}')
            out[key] = value
        return out
    with open(path, encoding='utf-8') as stream:
        data = json.load(stream, parse_float=str, object_pairs_hook=unique)
    require(isinstance(data, dict), 'expected a JSON object')
    result = {key: rational(data[key], key)
              for key in ('d0', 'd1', 'UA', 'S_d0', 'S_d1')}
    require(0 <= result['d0'] < result['d1'] <= 1, 'the δ interval must satisfy 0≤d0<d1≤1')
    if 'target' in data:             # Interval-specific target: S ≥ slope·δ + intercept at both endpoints.
        t = data['target']
        result['target'] = (rational(t['slope'], 'target.slope'), rational(t['intercept'], 'target.intercept'))
    require(result['UA'] == ALPHA, 'only standard UA=9/5 is supported')
    require('U' not in data and not data.get('edge_variant'), 'explicit U and edge variants are not supported')
    for key, size in (('F', 5), ('T', 5), ('V', 3)):
        require(isinstance(data[key], list), f'{key}: expected an array')
        result[key] = []
        for i, raw in enumerate(data[key]):
            label = f'{key}[{i}]'
            require(isinstance(raw, list) and len(raw) == size, f'{label}: expected {size} elements')
            row = tuple(rational(v, label) for v in raw)
            require(row[-1] >= 0, f'{label}: negative mass/density {row[-1]}')
            if key == 'V':
                require(0 <= row[0] <= 2 + result['d0'] and 0 <= row[1] <= 2,
                        f'{label}: V lies outside the corner or has negative length: {row}')
            else:
                ax, ay, bx, by, mass = row
                require((ax == bx) != (ay == by), f'{label}: expected an axis-aligned segment of positive length: {row}')
            result[key].append(row)
    return result


# Internal representation: (direction h/v, fixed coordinate, lower end, upper end, density). Negative densities are used only to compare differences.
def segments(rows):
    out = []
    for ax, ay, bx, by, mass in rows:
        kind, c, lo, hi = ('h', ay, min(ax, bx), max(ax, bx)) if ay == by else ('v', ax, min(ay, by), max(ay, by))
        out.append((kind, c, lo, hi, mass / (hi - lo)))
    return out


def canonical(segs):
    events = defaultdict(lambda: defaultdict(Q))
    for kind, c, lo, hi, density in segs:
        if hi > lo:
            events[kind, c][lo] += density
            events[kind, c][hi] -= density
    out = []
    for (kind, c), changes in sorted(events.items()):
        points = sorted(x for x, change in changes.items() if change)
        density = Q(0)
        for lo, hi in zip(points, points[1:]):
            density += changes[lo]
            if density:
                out.append((kind, c, lo, hi, density))
    return out


def difference(left, right):
    return canonical(list(left) + [(k, c, lo, hi, -r) for k, c, lo, hi, r in right])


def equal(left, right, label):
    diff = difference(left, right)
    require(not diff, f'{label}: difference segment (direction,coordinate,lower end,upper end,density)={diff[:1]}')


def nonnegative(segs, label):
    bad = next((s for s in canonical(segs) if s[-1] < 0), None)
    require(bad is None, f'{label}: negative density {bad}')


def mass(segs):
    return sum(((hi-lo)*r for _, _, lo, hi, r in segs), Q(0))


def transform(segs, point):
    rows = []
    for kind, c, lo, hi, r in segs:
        a, b = ((lo, c), (hi, c)) if kind == 'h' else ((c, lo), (c, hi))
        a, b = point(*a), point(*b)
        rows.append((*a, *b, (hi-lo)*r))
    return segments(rows)


def shift(segs, dx=0, dy=0):
    return transform(segs, lambda x, y: (x+dx, y+dy))


def clip(segs, x0, x1, y0, y1, right_open=False):
    out = []
    for k, c, lo, hi, r in segs:
        lower, upper = (y0, y1) if k == 'h' else (x0, x1)
        if not lower <= c <= upper or (right_open and k == 'v' and c == x1):
            continue
        low, high = (x0, x1) if k == 'h' else (y0, y1)
        lo, hi = max(lo, low), min(hi, high)
        if hi > lo:
            out.append((k, c, lo, hi, r))
    return out


def period(segs, base):
    return shift(clip(segs, base, base+1, 0, ALPHA, True), -base)


def grid_profile(profile):
    """Reconstruct from cell integrals and verify constant density within each cell."""
    out = []
    for k in ('h', 'v'):
        for j in (range(1, 10) if k == 'h' else range(5)):
            c = Q(j, 5)
            for i in (range(5) if k == 'h' else range(9)):
                lo, hi = Q(i, 5), Q(i+1, 5)
                m = sum((max(Q(0), min(hi, b)-max(lo, a))*r
                         for kind, coord, a, b, r in profile if (kind, coord) == (k, c)), Q(0))
                out.append((k, c, lo, hi, 5*m))
    equal(profile, out, 'wall 1/5 grid and density within each cell')


def repeated(profile, count, left=False):
    out = [s for n in range(count) for s in shift(profile, 2+n)]
    return transform(out, lambda x, y: (y, x)) if left else out


def horizon(segs, left=False):
    # Walls consist of an integer number of complete periods; check through the last period with positive-mass support.
    longitudinal = [hi if (k == 'v') == left else c for k, c, lo, hi, r in segs if r]
    require(bool(longitudinal), 'wall support is empty')
    end = max(longitudinal)
    count = -((-end.numerator)//end.denominator) - 2
    require(count >= 3, f'at least 3 periods are required to cover the local window: {count}')
    return count


def wrap_shift(segs, dx):
    """Shift one period [0, 1) cyclically by dx in x (h segments) or phase (v lines), splitting h segments that cross the period boundary."""
    out = []
    for k, c, lo, hi, r in segs:
        if k == 'v': out.append((k, (c + dx) % 1, lo, hi, r)); continue
        a, b = lo + dx, hi + dx
        n = -((-a.numerator) // a.denominator) - 1 if a < 0 else (a.numerator // a.denominator)
        a, b = a - n, b - n
        if b <= 1: out.append((k, c, a, b, r))
        else: out.append((k, c, a, Q(1), r)); out.append((k, c, Q(0), b - 1, r))
    return canonical(out)


def reflect_profile(profile):
    """Reflect the period x ↔ 1 − x (vertical phase c ↔ −c mod 1), rotating the far-end wall into the left wall of the adjacent corner."""
    return canonical([(k, c, 1-hi, 1-lo, r) if k == 'h' else (k, (-c) % 1, lo, hi, r) for k, c, lo, hi, r in profile])


def profile_phase(profile):
    """Return the common phase φ of vertical wall lines (positions mod 1/5), or 0 for phase zero."""
    ph = {(c % Q(1, 5)) for k, c, lo, hi, r in profile if k == 'v'}
    require(len(ph) <= 1, f'vertical wall lines have inconsistent phases: {sorted(ph)[:3]}')
    return ph.pop() if ph else Q(0)


def decompose(f):
    fixed, moving = segments(f['F']), segments(f['T'])
    profile = canonical(period(moving, 3))
    phi = profile_phase(profile)
    grid_profile(wrap_shift(profile, -phi) if phi else profile)     # Shift back by φ to check the 1/5 grid for a nonzero phase.
    reflected = reflect_profile(profile)
    if phi == 0 or phi == Q(1, 10):
        # At phases 0 and 1/10, reflection preserves the grid and the LP shares variables symmetrically.
        equal(profile, reflected, 'hvar/vvar reflection symmetry')
    left_profile = period(transform(fixed, lambda x, y: (y, x)), 3)
    # The local left wall is the rotated far-end wall of the adjacent corner: the reflected bottom wall (identical at phases 0 and 1/10).
    equal(reflected, left_profile, 'left wall equals reflected bottom wall (transposed)')
    require(mass(profile) == ALPHA, f'bottom wall mass per period={mass(profile)} ≠ 9/5')
    require(mass(left_profile) == ALPHA, f'left wall mass per period={mass(left_profile)} ≠ 9/5')
    cf = difference(fixed, repeated(reflected, horizon(fixed, True), True))
    ct = difference(moving, repeated(profile, horizon(moving)))
    nonnegative(cf, 'corner after removing the left wall from F')
    nonnegative(ct, 'corner after removing the bottom wall from T')
    equal(cf, clip(cf, 0, 2+f['d0'], 0, 2), 'F corner support / complete left-wall periods')
    require(all(k == 'v' and c == 2 and 0 <= lo < hi <= 2 for k, c, lo, hi, r in ct),
            f'the T corner must contain only vertical lines at x=2: {ct[:1]}')
    return profile, cf, ct


def corner(f, cf, ct, d):
    return cf + shift(ct, d) + [('h', y, xl, 2+d, r) for xl, y, r in f['V'] if xl < 2+d]


def saving(f, cf, ct, profile, d):
    area = 2*(2+d) - (2+d-ALPHA)*(2-ALPHA)
    mv = mass([s for s in profile if s[0] == 'v' and s[1] == 0])
    return area - mass(corner(f, cf, ct, d)) - mv


LINE = None         # --line-alpha/--line-beta: check S ≥ ALPHA·δ + BETA (and S > δ/2) at both ends instead of the default targets
OPEN_LEFT = False   # --open-left: treat the interval as (d0, d1]; the adjacent interval handles d0, so omit the lower branch when d0 = 2/5.


def target_checks(f, value):
    if LINE is not None or 'target' in f:
        slope, intercept = LINE if LINE is not None else f['target']   # --line (the certified line) takes precedence
        for d in sorted({f['d0'], f['d1']}):
            actual = value(d)
            require(actual >= slope*d+intercept, f'δ={d}: S={actual} < certified line / interval target {slope*d+intercept}')
            require(actual >= 0 if d == 0 else actual > d / 2, f'δ={d}: S={actual} fails the δ/2 lower bound')
        return
    cut = Q(2, 5)
    branches = []
    if f['d0'] < cut or (f['d0'] == cut and not OPEN_LEFT):
        branches.append((f['d0'], min(f['d1'], cut), Q(3, 2), Q(0)))
    if f['d1'] > cut:
        branches.append((max(f['d0'], cut), f['d1'], Q(2, 5), Q(31, 100)))
    for low, high, slope, intercept in branches:
        for d in sorted({low, high}):
            actual = value(d)
            require(actual >= slope*d+intercept,
                    f'δ={d}: S={actual} < target/right-hand limit {slope*d+intercept}')


def build(f, profile, cf, ct, d, k):
    a = k+d
    base = corner(f, cf, ct, d)
    base += [s for n in range(k-4) for s in shift(profile, 2+d+n)]
    base += shift([s for s in profile if s[0] == 'v' and s[1] == 0], 2+d+k-4)
    out = []
    for _ in range(4):
        out.extend(base)
        base = transform(base, lambda x, y: (a-y, x))
    return out


class Report:
    def __init__(self):
        self.ok = True

    def check(self, label, action):
        try:
            detail = action()
            print(f'OK {label}' + (f': {detail}' if detail else ''))
            return True
        except (ValueError, KeyError, TypeError, ZeroDivisionError, OSError) as exc:
            self.ok = False
            print(f'NG {label}: {exc}')
            return False


def validate(path, right=None, monotone_over=None):
    report = Report()
    box = {}
    if not report.check('1 format, nonnegativity, standard U', lambda: box.update(f=load(path))):
        print('NG 2–4: cannot check because input is invalid')
        return False
    f = box['f']
    if right:
        def check_right():
            other = load(right)
            for key in ('d0', 'd1', 'UA'):
                require(other[key] == f[key], f'right-side {key} mismatch')
            require(other['F'] == f['T'] and not other['T'] and not other['V'],
                    'right-side row-by-row derivation F=T_original, T=V=[] mismatch')
        report.check('right-side derivation', check_right)
    if monotone_over:
        def monotone():
            old = load(monotone_over)
            for key in ('d0', 'd1', 'UA'):
                require(old[key] == f[key], f'reference {key} mismatch')
            equal(segments(f['F']), segments(old['F']), 'F preservation under monotone modification')
            require(sorted(f['V']) == sorted(old['V']), 'V preservation under monotone modification mismatch')
            delta = difference(segments(f['T']), segments(old['T']))
            nonnegative(delta, 'T_new − T_old')
            require(all(k == 'v' and c == 2 and 0 <= lo < hi <= 2 for k, c, lo, hi, r in delta),
                    f'changes extend beyond the T corner: {delta[:1]}')
            return f'T corner mass increase={mass(delta)} (monotone for all δ)'
        report.check('monotone modification', monotone)
    if not report.check('2 grid, reflection, transposition, both wall masses 9/5, complete periods, corner separation',
                        lambda: box.update(parts=decompose(f))):
        print('NG 3–4: cannot check because the structure does not match')
        return False
    profile, cf, ct = box['parts']
    value = lambda d: saving(f, cf, ct, profile, d)
    for key in ('d0', 'd1'):
        def saved(key=key):
            actual = value(f[key])
            require(actual == f['S_'+key], f'δ={f[key]}: recomputed={actual}, stored={f["S_"+key]}')
            return f'S({f[key]})={actual}'
        report.check(f'3 saving {key} equals stored value', saved)
    report.check('3 certified line or target lower bound at both ends', lambda: target_checks(f, value))
    for d in (f['d0'], f['d1']):
        covers = {}
        local = segments(f['F']) + shift(segments(f['T']), d)
        local += [('h', y, xl, 2+d, r) for xl, y, r in f['V'] if xl < 2+d]
        window = lambda ss: clip(ss, 0, WINDOW, 0, WINDOW)
        for k in (7, 8, 9):
            covers[k] = build(f, profile, cf, ct, d, k)
            a, ss = k+d, covers[k]
            def total(a=a, ss=ss):
                require(mass(ss)+(a-2*ALPHA)**2 == a*a-4*value(d), 'total-mass identity mismatch')
                equal(ss, clip(ss, 0, a, 0, a), 'support inside the container')
                equal(ss, transform(ss, lambda x, y: (a-y, x)), 'C4 invariance')
            report.check(f'4a δ={d}, k={k} total mass, support, C4', total)
            def local_match(a=a, ss=ss):
                require(a-ALPHA >= WINDOW, 'the upper boundary of U_global lies inside the local window')
                equal(window(ss), window(local), 'local/global segment measures within the window')
            report.check(f'4b δ={d}, k={k} agreement in [0,24/5]² (including U)', local_match)
        def reduction():
            equal(window(covers[7]), window(covers[9]), 'k=7/9 corner windows')
            for k in (7, 9):
                for n in range(1, k-4):
                    equal(period(covers[k], 2+d+n), profile, f'k={k} wall period n={n}')
                # The adjacent corner boundary also overlaps the terminal line; subtract all 4 corner contributions to compare only walls.
                corners, part = [], corner(f, cf, ct, d)
                for _ in range(4):
                    corners.extend(part)
                    part = transform(part, lambda x, y: (k+d-y, x))
                walls = difference(covers[k], corners)
                terminal = [s for s in clip(walls, 2+d+k-4, 2+d+k-4, 0, ALPHA)
                            if s[0] == 'v']
                equal(shift(terminal, -(2+d+k-4)),
                      [s for s in profile if s[0] == 'v' and s[1] == 0], 'terminal phase 0')
        report.check(f'4c δ={d} k=7/9 corner windows, integer wall shifts, terminal line', reduction)
    print('Note: the leaf checks are done by replay4d; the localization inequalities are in SPEC.md §2.3.')
    return report.ok


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('family')
    parser.add_argument('--right')
    parser.add_argument('--monotone-over')
    parser.add_argument('--line-alpha', metavar='ALPHA', help='certified line slope α (rational string; pass as --line-alpha=ALPHA)')
    parser.add_argument('--line-beta', metavar='BETA', help='certified line intercept β (rational string; pass as --line-beta=BETA): with --line-alpha, check S ≥ αδ + β and S > δ/2 at both ends')
    parser.add_argument('--open-left', action='store_true', help='check the target on (d0, d1] (the adjacent interval handles d0)')
    args = parser.parse_args(argv)
    global OPEN_LEFT, LINE
    OPEN_LEFT = args.open_left
    require((args.line_alpha is None) == (args.line_beta is None), '--line-alpha and --line-beta must be given together')
    if args.line_alpha is not None: LINE = (rational(args.line_alpha, '--line-alpha'), rational(args.line_beta, '--line-beta'))
    ok = validate(args.family, args.right, args.monotone_over)
    print('VALIDATE OK' if ok else 'VALIDATE NG')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
