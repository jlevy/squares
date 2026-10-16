#!/usr/bin/env python3
"""Reviewer's programs for the stage 4 review of Benjamin Greff's mixed covers for s(76) = 9 and s(95) = 10.

Written for docs/project/reviews/review-2026-10-16-greff-k2m5-mixed-covers-76-95.md.  Standard library only.  Every
input is read as data; nothing is imported from the source, from Evan Daniel's checkers or from this repository.
Every verdict below is exact (integers and fractions.Fraction); floats only choose where to look.

  cover    COVER N --out JSON              data facts of a "mixed 1" cover: format, exact total, D4 invariance as a
                                           measure under all eight elements, segment and wall census, the bounds the
                                           two checkers' parsers impose, FNV-1a and SHA-256 of the bytes
  records  PACKET N --out JSON             the composite over the D4 region from the retained records: every zmx2
                                           root log (source, replay, wall control) and every zm_mixed.py record set
                                           (source, replay), checked cell by cell
  poses    COVER N PACKET --out JSON       exact mu(Q) at sampled poses: the D4 region, the zmx2-failing roots, the
                                           uncertified boxes zmx2 lists, random poses of the whole container folded
                                           into the region (mu compared at both), and the published control poses
  mutants  COVER N --out JSON              mutated covers (an orbit removed, every mass scaled): a pose where each
                                           captures less than one, exactly
  cellmin  COVER N --box B --out JSON      the lowest exact mu found in one pose box (where a scaled mutant's hole goes)
  localmut COVER N --pose P --write F      a mutant without the D4 orbit of the heaviest piece captured at one pose
  tiling   PACKET N CHECK_COVERAGE --out JSON
                                           mutated record sets run through the author's check_coverage.py and this
                                           program's own composite check, side by side

Run each from any directory with any CPython >= 3.10, e.g.  python3 -I k2m5_review.py cover s76_cover_v5.txt 76.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path

ZM_MIXED_SHA = 'ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac'
MIXED_COVER_SHA = 'bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5'
ZEROMARGIN_SHA = '640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab'
REACH = F(7072, 10000)   # > sqrt(2)/2: every point of a unit square is within this of its centre


# ============================================================================================ the cover
def read_bytes(path: str) -> bytes:
    with open(path, 'rb') as fh:
        data = fh.read()
    return gzip.decompress(data) if path.endswith('.gz') else data


def fnv1a64(data: bytes) -> int:
    h = 0xcbf29ce484222325
    for b in data:
        h ^= b
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h


class Cover:
    """A "mixed 1" cover read with this program's own tokenizer: '#' starts a comment to the end of the line, as in
    Daniel's FORMAT.md; header s_num s_den D W, then points (X Y w), segments (X0 Y0 X1 Y1 w), polygons (must be 0)."""

    def __init__(self, data: bytes):
        toks = []
        for line in data.decode('ascii').splitlines():
            toks.extend(line.split('#', 1)[0].split())
        pos = 0

        def nxt() -> str:
            nonlocal pos
            if pos >= len(toks):
                raise ValueError('unexpected end of file')
            v = toks[pos]
            pos += 1
            return v

        if nxt() != 'mixed' or nxt() != '1':
            raise ValueError('not a mixed-1 cover')
        self.s_num = int(nxt())
        self.s_den = int(nxt())
        self.D = int(nxt())
        self.W = int(nxt())
        n = int(nxt())
        self.points = [(int(nxt()), int(nxt()), int(nxt())) for _ in range(n)]
        n = int(nxt())
        self.segs = [(int(nxt()), int(nxt()), int(nxt()), int(nxt()), int(nxt())) for _ in range(n)]
        self.npg = int(nxt())
        if self.npg != 0:
            raise ValueError('polygons present')
        if pos != len(toks):
            raise ValueError('trailing tokens')
        if self.s_den <= 0 or (self.s_num * self.D) % self.s_den:
            raise ValueError('side is not a multiple of 1/D')
        self.S = self.s_num * self.D // self.s_den       # container side in units 1/D
        self.side = F(self.s_num, self.s_den)

    def total(self) -> F:
        return F(sum(p[2] for p in self.points) + sum(s[4] for s in self.segs), self.W)

    def replaced(self, points, segs) -> 'Cover':
        c = object.__new__(Cover)
        c.__dict__.update(self.__dict__)
        c.points, c.segs = list(points), list(segs)
        return c


def d4_maps(S: int):
    """The eight elements of D4 acting on integer coordinates of [0, S]^2."""
    return {
        'id': lambda X, Y: (X, Y), 'rot90': lambda X, Y: (S - Y, X), 'rot180': lambda X, Y: (S - X, S - Y),
        'rot270': lambda X, Y: (Y, S - X), 'x->s-x': lambda X, Y: (S - X, Y), 'y->s-y': lambda X, Y: (X, S - Y),
        'x<->y': lambda X, Y: (Y, X), 'antidiagonal': lambda X, Y: (S - Y, S - X)}


def canon_measure(points, segs):
    """The measure in a canonical form: atoms {(X, Y): weight} and, per axis line, the maximal intervals of constant
    non-zero density (weight per 1/D of length, a Fraction).  Two covers define the same measure iff these agree:
    atoms and length densities on lines are mutually singular, and a vertical and a horizontal line meet in a point."""
    atoms = Counter()
    for X, Y, w in points:
        if w:
            atoms[(X, Y)] += w
    atoms = {k: v for k, v in atoms.items() if v}
    lines = defaultdict(list)
    for X0, Y0, X1, Y1, w in segs:
        if not w:
            continue
        if X0 == X1:
            lines[('V', X0)].append((min(Y0, Y1), max(Y0, Y1), w))
        elif Y0 == Y1:
            lines[('H', Y0)].append((min(X0, X1), max(X0, X1), w))
        else:
            raise ValueError('segment not axis-parallel')
    dens = {}
    for key, ss in lines.items():
        bps = sorted({a for a, _, _ in ss} | {b for _, b, _ in ss})
        ix = {p: i for i, p in enumerate(bps)}
        d = [F(0)] * (len(bps) - 1)
        for a, b, w in ss:
            q = F(w, b - a)
            for i in range(ix[a], ix[b]):
                d[i] += q
        pieces = []
        for i, q in enumerate(d):
            if q == 0:
                continue
            lo, hi = bps[i], bps[i + 1]
            if pieces and pieces[-1][1] == lo and pieces[-1][2] == q:
                pieces[-1] = (pieces[-1][0], hi, q)
            else:
                pieces.append((lo, hi, q))
        if pieces:
            dens[key] = tuple(pieces)
    return atoms, dens


def image(cover: Cover, g):
    pts = [(*g(X, Y), w) for X, Y, w in cover.points]
    segs = [(*g(X0, Y0), *g(X1, Y1), w) for X0, Y0, X1, Y1, w in cover.segs]
    return pts, segs


def cmd_cover(a) -> dict:
    data = read_bytes(a.cover)
    cv = Cover(data)
    n = a.n
    D, W, S = cv.D, cv.W, cv.S
    out = dict(file=os.path.basename(a.cover), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
               fnv1a64='%016x' % fnv1a64(data), side=str(cv.side), D=D, W=W, S_units=S,
               points=len(cv.points), segments=len(cv.segs), polygons=cv.npg)
    problems = []
    # well-formedness
    for X, Y, w in cv.points:
        if not (0 <= X <= S and 0 <= Y <= S):
            problems.append('point outside: %r' % ((X, Y, w),))
        if w < 0:
            problems.append('negative point weight: %r' % ((X, Y, w),))
    for X0, Y0, X1, Y1, w in cv.segs:
        if not all(0 <= v <= S for v in (X0, Y0, X1, Y1)):
            problems.append('segment outside: %r' % ((X0, Y0, X1, Y1, w),))
        if w < 0:
            problems.append('negative segment weight')
        if (X0 == X1) == (Y0 == Y1):
            problems.append('segment degenerate or not axis-parallel: %r' % ((X0, Y0, X1, Y1, w),))
    out['zero_weight_points'] = sum(1 for p in cv.points if p[2] == 0)
    out['zero_weight_segments'] = sum(1 for s in cv.segs if s[4] == 0)
    tot = cv.total()
    out['total'] = str(tot)
    out['total_decimal'] = '%.12f' % float(tot)
    out['total_below_n'] = tot < n
    out['slack_n_minus_total'] = str(n - tot)
    out['slack_decimal'] = '%.9f' % float(n - tot)
    out['grid_count_k2'] = int(cv.side) ** 2 if cv.side.denominator == 1 else None
    out['k2_minus_n'] = (int(cv.side) ** 2 - n) if cv.side.denominator == 1 else None
    out['ceil_sqrt_n'] = math.isqrt(n - 1) + 1
    # points
    pos = Counter((X, Y) for X, Y, w in cv.points if w)
    out['distinct_point_positions'] = len(pos)
    out['repeated_point_positions'] = sum(1 for v in pos.values() if v > 1)
    out['max_point_weight'] = max(p[2] for p in cv.points)
    on_int_line = sum(1 for X, Y, w in cv.points if w and (X % D == 0 or Y % D == 0))
    vlines = {X0 for X0, Y0, X1, Y1, w in cv.segs if w and X0 == X1}
    hlines = {Y0 for X0, Y0, X1, Y1, w in cv.segs if w and Y0 == Y1}
    on_seg_line = sum(1 for X, Y, w in cv.points if w and (X in vlines or Y in hlines))
    on_wall = sum(1 for X, Y, w in cv.points if w and (X in (0, S) or Y in (0, S)))
    out['points_on_integer_lines'] = on_int_line
    out['points_on_segment_lines'] = on_seg_line
    out['points_on_container_boundary'] = on_wall
    # segments
    lens = Counter()
    for X0, Y0, X1, Y1, w in cv.segs:
        if w:
            lens[str(F(abs(X1 - X0) + abs(Y1 - Y0), D))] += 1
    out['segment_lengths'] = dict(sorted(lens.items(), key=lambda kv: F(kv[0])))
    lc = 1
    for X0, Y0, X1, Y1, w in cv.segs:
        if w:
            lc = math.lcm(lc, abs(X1 - X0) + abs(Y1 - Y0))
    out['lcm_segment_lengths_units'] = lc
    out['segment_lines_vertical'] = sorted(str(F(x, D)) for x in vlines)
    out['segment_lines_horizontal'] = sorted(str(F(y, D)) for y in hlines)
    out['all_segment_lines_integer'] = all(x % D == 0 for x in vlines | hlines)
    walls = [s for s in cv.segs if s[4] and ((s[0] == s[2] and s[0] in (0, S)) or (s[1] == s[3] and s[1] in (0, S)))]
    out['wall_segments'] = len(walls)
    out['wall_segment_mass'] = str(F(sum(s[4] for s in walls), W))
    out['wall_segment_weights'] = sorted(Counter(s[4] for s in walls).items())
    out['wall_segment_lengths'] = sorted(Counter(str(F(abs(s[2] - s[0]) + abs(s[3] - s[1]), D)) for s in walls).items())
    per_wall = Counter()
    for X0, Y0, X1, Y1, w in walls:
        per_wall['x=0' if X0 == X1 == 0 else 'x=s' if X0 == X1 == S else 'y=0' if Y0 == Y1 == 0 else 'y=s'] += 1
    out['wall_segments_per_wall'] = dict(per_wall)
    mids = sorted({F(Y0 + Y1, 2 * D) for X0, Y0, X1, Y1, w in walls if X0 == X1 == 0})
    steps = {b - a for a, b in zip(mids, mids[1:])}
    out['wall_segments_x0_midpoints'] = dict(count=len(mids), first=str(mids[0]), last=str(mids[-1]),
                                             steps=sorted(str(v) for v in steps)) if mids else None
    tot_nowall = tot - F(sum(s[4] for s in walls), W)
    out['total_without_wall_segments'] = str(tot_nowall)
    out['total_without_wall_segments_below_n'] = tot_nowall < n
    # overlapping segments on one line
    byline = defaultdict(list)
    for X0, Y0, X1, Y1, w in cv.segs:
        if w:
            byline[('V', X0) if X0 == X1 else ('H', Y0)].append(
                (min(Y0, Y1), max(Y0, Y1)) if X0 == X1 else (min(X0, X1), max(X0, X1)))
    ov = 0
    for ivs in byline.values():
        ivs.sort()
        for i in range(1, len(ivs)):
            for j in range(i - 1, -1, -1):
                if ivs[j][1] > ivs[i][0]:
                    ov += 1
                else:
                    break
    out['overlapping_segment_pairs_same_line'] = ov
    # D4 invariance of the measure, all eight elements
    base = canon_measure(cv.points, cv.segs)
    d4 = {}
    for name, g in d4_maps(S).items():
        d4[name] = canon_measure(*image(cv, g)) == base
    out['d4_invariant_as_measure'] = d4
    out['d4_all'] = all(d4.values())
    # raw multiset invariance (the stricter criterion zm_mixed.py uses)
    def raw(g):
        P = Counter()
        for X, Y, w in cv.points:
            if w:
                P[g(X, Y)] += w
        Sg = Counter()
        for X0, Y0, X1, Y1, w in cv.segs:
            if w:
                Sg[(frozenset((g(X0, Y0), g(X1, Y1))), w)] += 1
        return P, Sg
    raw0 = raw(lambda X, Y: (X, Y))
    out['d4_raw_multiset_generators'] = {nm: raw(d4_maps(S)[nm]) == raw0 for nm in ('x->s-x', 'x<->y')}
    # what the checkers' parsers require
    tw = sum(p[2] for p in cv.points) + sum(s[4] for s in cv.segs)
    out['zmx2_input_bounds'] = dict(
        D_lt_2p20=D < 2 ** 20, S_lt_2p27=S < 2 ** 27, W_lt_2p50=W < 2 ** 50,
        weights_lt_2p50=max([p[2] for p in cv.points] + [s[4] for s in cv.segs]) < 2 ** 50,
        total_weight_lt_2p56=tw < 2 ** 56, lcm_lengths_le_2p24=lc <= 2 ** 24,
        d4_side_multiple_of_1_5=(S * 10) % D == 0 and ((S * 10) // D) % 2 == 0)
    out['zm_mixed_d4_half_side_multiple_of_pitch_1_20'] = ((cv.side / 2) / F(1, 20)).denominator == 1
    # heaviest pieces (for the mutation controls)
    hp = max(cv.points, key=lambda p: p[2])
    hs = max(cv.segs, key=lambda s: s[4])
    out['heaviest_point'] = dict(X=str(F(hp[0], D)), Y=str(F(hp[1], D)), w=str(F(hp[2], W)))
    out['heaviest_segment'] = dict(ends=[str(F(v, D)) for v in hs[:4]], w=str(F(hs[4], W)))
    # mass by region (corner block [0, 5/2)^2 and its images, the rest the cross)
    def in_corner(X, Y):
        lo, hi = F(5, 2) * D, S - F(5, 2) * D
        return (X < lo or X > hi) and (Y < lo or Y > hi)
    cm = sum(w for X, Y, w in cv.points if in_corner(X, Y)) + sum(
        s[4] for s in cv.segs if in_corner(s[0], s[1]) and in_corner(s[2], s[3]))
    out['mass_in_four_corner_blocks'] = str(F(cm, W))
    out['problems'] = problems
    out['ok'] = not problems and out['total_below_n'] and out['d4_all']
    return out


# ============================================================================================ exact mu(Q)
class Evaluator:
    """Exact mu(Q) for the closed unit square Q(c, theta), theta = 2 atan u, u in [0, 1]: atoms by an exact integer
    containment test, each segment by exact clipping of its parameter interval by the four half-planes |X|, |Y| <= 1/2
    of the square's frame.  Pose: c = (cxn/cd, cyn/cd), u = un/ud, all integers."""

    def __init__(self, cv: Cover):
        self.cv = cv
        D = cv.D
        agg = Counter()
        for X, Y, w in cv.points:
            if w:
                agg[(X, Y)] += w
        self.pb = defaultdict(list)
        for (X, Y), w in agg.items():
            if w:
                self.pb[(X // D, Y // D)].append((X, Y, w))
        self.segs = [s for s in cv.segs if s[4]]
        self.sb = defaultdict(list)
        for k, (X0, Y0, X1, Y1, w) in enumerate(self.segs):
            xs = sorted({X0 // D, (X0 - 1) // D} if X0 % D == 0 and X0 == X1 else
                        set(range(min(X0, X1) // D, max(X0, X1) // D + 1)))
            ys = sorted({Y0 // D, (Y0 - 1) // D} if Y0 % D == 0 and Y0 == Y1 else
                        set(range(min(Y0, Y1) // D, max(Y0, Y1) // D + 1)))
            # every cell the closed segment touches (a segment on a cell boundary belongs to both sides)
            if X0 == X1 and X0 % D != 0:
                xs = [X0 // D]
            if Y0 == Y1 and Y0 % D != 0:
                ys = [Y0 // D]
            for i in xs:
                for j in ys:
                    self.sb[(i, j)].append(k)

    def mass(self, cxn: int, cyn: int, cd: int, un: int, ud: int, without=None) -> F:
        D, W = self.cv.D, self.cv.W
        N = ud * ud + un * un
        Cn = ud * ud - un * un
        Sn = 2 * un * ud
        HH = N * D * cd                      # |X| <= 1/2  <=>  2 |X N D cd| <= N D cd
        cx, cy = cxn / cd, cyn / cd
        i0, i1 = math.floor(cx - 0.7072), math.floor(cx + 0.7072)
        j0, j1 = math.floor(cy - 0.7072), math.floor(cy + 0.7072)
        wsum = 0
        segk = set()
        for i in range(i0, i1 + 1):
            for j in range(j0, j1 + 1):
                for X, Y, w in self.pb.get((i, j), ()):
                    a = X * cd - cxn * D
                    b = Y * cd - cyn * D
                    xl = a * Cn + b * Sn
                    yl = b * Cn - a * Sn
                    if 2 * abs(xl) <= HH and 2 * abs(yl) <= HH:
                        wsum += w
                segk.update(self.sb.get((i, j), ()))
        smass = F(0)
        for k in segk:
            X0, Y0, X1, Y1, w = self.segs[k]
            if X0 == X1:                      # vertical, parameter t = y
                T0, T1 = min(Y0, Y1), max(Y0, Y1)
                aa = X0 * cd - cxn * D
                p0, p1 = 2 * (aa * Cn - cyn * D * Sn), 2 * cd * Sn
                q0, q1 = 2 * (-aa * Sn - cyn * D * Cn), 2 * cd * Cn
            else:                             # horizontal, parameter t = x
                T0, T1 = min(X0, X1), max(X0, X1)
                bb = Y0 * cd - cyn * D
                p0, p1 = 2 * (bb * Sn - cxn * D * Cn), 2 * cd * Cn
                q0, q1 = 2 * (cxn * D * Sn + bb * Cn), -2 * cd * Sn
            lo, hi = F(T0), F(T1)
            empty = False
            for c0, c1 in ((p0, p1), (q0, q1)):
                if c1 == 0:
                    if abs(c0) > HH:
                        empty = True
                        break
                    continue
                if c1 > 0:
                    lo2, hi2 = F(-HH - c0, c1), F(HH - c0, c1)
                else:
                    lo2, hi2 = F(HH - c0, c1), F(-HH - c0, c1)
                if lo2 > lo:
                    lo = lo2
                if hi2 < hi:
                    hi = hi2
                if lo >= hi:
                    empty = True
                    break
            if not empty:
                smass += w * (hi - lo) / (T1 - T0)
        return (wsum + smass) / W

    def admissible(self, cxn, cyn, cd, un, ud) -> bool:
        """Q(c, theta) inside [0, s]^2, theta in [0, 90deg]: w/2 <= c <= s - w/2 with w = cos + sin."""
        N = ud * ud + un * un
        wn = (ud * ud - un * un) + 2 * un * ud        # w = wn / N
        sc = self.cv.side * cd
        lo = F(wn * cd, 2 * N)
        return lo <= cxn <= sc - lo and lo <= cyn <= sc - lo


def frac_parts(x: F, den: int) -> tuple[int, int]:
    """x as num/den with the given denominator (den must clear x's denominator)."""
    assert (x * den).denominator == 1
    return int(x * den), den


def fold(cx: F, cy: F, u: F, s: F):
    """The D4 image of the pose in the fundamental region [0, s/2]^2 x u in [0, sqrt2 - 1].  A reflection of the
    container maps Q(c, theta) to Q(g c, -theta) = Q(g c, 90deg - theta), i.e. u -> (1 - u)/(1 + u)."""
    refl = lambda v: (1 - v) / (1 + v)    # noqa: E731
    steps = []
    if cx > s / 2:
        cx, u = s - cx, refl(u)
        steps.append('x->s-x')
    if cy > s / 2:
        cy, u = s - cy, refl(u)
        steps.append('y->s-y')
    if u * u + 2 * u - 1 > 0:            # theta > 45deg
        cx, cy, u = cy, cx, refl(u)
        steps.append('x<->y')
    return cx, cy, u, steps


def mass_f(ev: Evaluator, cx: F, cy: F, u: F) -> F:
    cd = math.lcm(cx.denominator, cy.denominator)
    return ev.mass(int(cx * cd), int(cy * cd), cd, u.numerator, u.denominator)


def adm_f(ev: Evaluator, cx: F, cy: F, u: F) -> bool:
    cd = math.lcm(cx.denominator, cy.denominator)
    return ev.admissible(int(cx * cd), int(cy * cd), cd, u.numerator, u.denominator)


# ============================================================================================ the records
ROOT_RE = re.compile(r'^ROOT (\d+) pass (\d+) root (\S+) boxes (\d+) cert (\d+) empty (\d+) uncert (\d+) '
                     r'maxdepth (\d+) capped (\d+) ms (\d+)$')
UNC_RE = re.compile(r'^UNCERT (\d+) pass (\d+) box (\S+) \| .* \| float-min (\S+) at')
HDR_RE = re.compile(r'^# zmx2 cert hash=([0-9a-f]{16}) mode=(\S+) atoms=(\S+) depth=(\d+) node_cap=(\d+) '
                    r'kappa=(\S+) K=(\d+) region=x(\d+)-(\d+),y(\d+)-(\d+),bins(\d+)-(\d+)$')


def fbox(text: str):
    return tuple(F(v) for v in text.split(','))


def read_zmx2_log(path: str, k: int, fnv: str) -> dict:
    """One zmx2 root log: header, every ROOT line, every UNCERT line, checked against the D4 grid of side k."""
    text = read_bytes(path).decode('ascii')
    lines = text.splitlines()
    cmax = 5 * k                                   # root columns of 1/10 across [0, k/2]
    res = dict(path=path, problems=[])
    m = HDR_RE.match(lines[0])
    if not m:
        res['problems'].append('no header')
        return res
    hsh, mode, atoms, depth, node_cap, kappa, K, x0, x1, y0, y1, b0, b1 = m.groups()
    res['header'] = lines[0]
    res['header_hash_matches_cover'] = hsh == fnv
    res['header_ok'] = (hsh == fnv and mode == 'd4' and atoms == 'grid' and depth == '40' and node_cap == '20000000'
                        and kappa == '1.5' and K == '30' and (x0, x1, y0, y1, b0, b1) ==
                        ('0', str(cmax - 1), '0', str(cmax - 1), '0', '3'))
    roots = {}
    unc = defaultdict(list)
    other = 0
    for ln in lines[1:]:
        r = ROOT_RE.match(ln)
        if r:
            rid, pas, box, boxes, cert, empty, unc_n, maxd, capped, _ms = r.groups()
            b = fbox(box)
            i, j, kk = b[0] * 10, b[2] * 10, b[4] * 8
            ok = (all(v.denominator == 1 for v in (i, j, kk)) and b[1] - b[0] == F(1, 10) and b[3] - b[2] == F(1, 10)
                  and b[5] - b[4] == F(1, 8) and 0 <= i < cmax and 0 <= j < cmax and 0 <= kk < 4)
            if not ok:
                res['problems'].append('root not a grid cell: %s' % box)
                continue
            i, j, kk = int(i), int(j), int(kk)
            if int(rid) != (i * cmax + j) * 4 + kk or pas != '0':
                res['problems'].append('root id/pass mismatch: %s' % ln[:60])
            key = (i, j, kk)
            if key in roots:
                res['problems'].append('duplicate root %s' % (key,))
            c = dict(boxes=int(boxes), cert=int(cert), empty=int(empty), uncert=int(unc_n), maxdepth=int(maxd),
                     capped=int(capped))
            if c['capped'] == 0 and c['boxes'] != 2 * (c['cert'] + c['empty'] + c['uncert']) - 1:
                res['problems'].append('census is not a full binary tree at %s' % (key,))
            roots[key] = c
            continue
        u = UNC_RE.match(ln)
        if u:
            unc[int(u.group(1))].append((fbox(u.group(3)), u.group(4)))
            continue
        other += 1
    res['other_lines'] = other
    res['roots'] = len(roots)
    expect = {(i, j, kk) for i in range(cmax) for j in range(cmax) for kk in range(4)}
    res['roots_are_exactly_the_grid'] = set(roots) == expect
    fail = sorted(key for key, c in roots.items() if c['uncert'] > 0 or c['capped'] > 0)
    res['failing'] = fail
    res['census'] = dict(boxes=sum(c['boxes'] for c in roots.values()), cert=sum(c['cert'] for c in roots.values()),
                         empty=sum(c['empty'] for c in roots.values()),
                         uncert=sum(c['uncert'] for c in roots.values()),
                         maxdepth=max(c['maxdepth'] for c in roots.values()),
                         capped=sum(c['capped'] for c in roots.values()))
    res['certified_roots'] = sum(1 for c in roots.values() if c['uncert'] == 0 and c['capped'] == 0)
    res['maxdepth_certified_roots'] = max(c['maxdepth'] for c in roots.values() if c['uncert'] == 0)
    # listed UNCERT boxes inside their roots
    listed = 0
    inside = True
    mins = []
    for rid, bl in unc.items():
        kk = rid % 4
        j = (rid // 4) % cmax
        i = rid // (4 * cmax)
        R = (F(i, 10), F(i + 1, 10), F(j, 10), F(j + 1, 10), F(kk, 8), F(kk + 1, 8))
        for b, fm in bl:
            listed += 1
            mins.append(float(fm))
            inside &= R[0] <= b[0] < b[1] <= R[1] and R[2] <= b[2] < b[3] <= R[3] and R[4] <= b[4] < b[5] <= R[5]
            if (i, j, kk) not in fail:
                res['problems'].append('UNCERT box listed for a root without uncertified boxes')
    res['uncert_boxes_listed'] = listed
    res['uncert_boxes_inside_their_roots'] = inside
    res['uncert_listed_float_min_range'] = [min(mins), max(mins)] if mins else None
    res['_roots'] = roots
    res['_unc'] = {rid: [b for b, _ in bl] for rid, bl in unc.items()}
    return res


EXPECTED_SETTINGS = dict(mode='D4', depth=24, pitch='1/20', ubins=16, chain=True, chain_from=0, theta_bias=4,
                         clip=True, lemma_T=True, lemma_L=True, split=True, cert_mode=True, tprime=False,
                         split_maxchain=400, reach='442/625')
KINDS = ('ADM', 'CORE', 'P1', 'MIX', 'CHAIN', 'TRI', 'PIECE', 'EMPTY', 'UNCERT', 'SPLIT')


def read_zm_dir(d: str, cover_sha: str, total: str) -> dict:
    """Every j*.jsonl record of one zm_mixed.py record set: header, settings, region, one record, census."""
    res = dict(dir=d, problems=[], files=0)
    cells = {}
    heads = {}
    recs = {}
    maxd = 0
    boxes = 0
    cpu = 0.0
    for fn in sorted(os.listdir(d)):
        if not re.fullmatch(r'j\d+\.jsonl', fn):
            continue
        res['files'] += 1
        rows = [json.loads(ln) for ln in open(os.path.join(d, fn)) if ln.strip()]
        if not rows or rows[0].get('kind') != 'zm_mixed cert header':
            res['problems'].append('%s: no header' % fn)
            continue
        h = rows[0]
        sh = h['sha256']
        if (sh.get('zm_mixed.py'), sh.get('mixed_cover.py'), sh.get('zeromargin.py'), sh.get('input')) != \
                (ZM_MIXED_SHA, MIXED_COVER_SHA, ZEROMARGIN_SHA, cover_sha):
            res['problems'].append('%s: digests differ' % fn)
        if h.get('version') != 2 or h.get('total') != total:
            res['problems'].append('%s: version or total differ' % fn)
        st = dict(h['settings'])
        region = st.pop('region')
        if st != EXPECTED_SETTINGS:
            res['problems'].append('%s: settings differ: %s' % (fn, st))
        reg = tuple(F(region[k]) for k in ('cx_lo', 'cx_hi', 'cy_lo', 'cy_hi', 'u_lo', 'u_hi'))
        body = rows[1:]
        if len(body) != 1:
            res['problems'].append('%s: %d records, expected 1' % (fn, len(body)))
            continue
        r = body[0]
        root = tuple(F(v) for v in r['root'])
        if root != reg:
            res['problems'].append('%s: record root differs from the region it was run on' % fn)
        if r.get('label') != '' or r['st']['UNCERT'] != 0 or r['unc']:
            res['problems'].append('%s: not certified' % fn)
        leaves = sum(r['st'][k] for k in KINDS)
        if r['st']['boxes'] != 2 * leaves - 1:
            res['problems'].append('%s: census is not a full binary tree' % fn)
        i, j, kk = root[0] * 20, root[2] * 20, root[4] * 32
        aligned = (all(v.denominator == 1 for v in (i, j, kk)) and root[1] - root[0] == F(1, 20) and
                   root[3] - root[2] == F(1, 20) and root[5] - root[4] == F(1, 32))
        if not aligned:
            res['problems'].append('%s: not an aligned 1/20 x 1/20 x 1/32 cell' % fn)
            continue
        key = (int(i), int(j), int(kk))
        if key in cells:
            res['problems'].append('%s: duplicate cell' % fn)
        cells[key] = fn
        heads[fn] = h
        recs[fn] = r
        maxd = max(maxd, r['st']['maxdepth'])
        boxes += r['st']['boxes']
        cpu += r['st']['cpu']
    res['cells'] = len(cells)
    res['boxes'] = boxes
    res['maxdepth'] = maxd
    res['cpu_s_by_records'] = round(cpu, 1)
    res['_cells'] = cells
    res['_heads'] = heads
    res['_recs'] = recs
    return res


def subcells(key):
    i, j, kk = key
    return {(2 * i + a, 2 * j + b, 4 * kk + c) for a in (0, 1) for b in (0, 1) for c in range(4)}


PACKETS = {
    76: dict(src='s76-certificate', cover='cover/s76_cover_v5.txt.gz', zlog='records/zmx2/zmx2_v5.log.gz',
             zout='records/zmx2/zmx2_v5.out', rlog='receipts/n76_zmx2_d4_roots.log.gz',
             wlog='receipts/controls/n76_control_nowall_zmx2_d4_roots.log.gz', rzm='receipts/n76_zm_mixed'),
    95: dict(src='s95-certificate', cover='cover/s95_cover_v2.txt.gz', zlog='records/zmx2/zmx2_s95_v2.log.gz',
             zout='records/zmx2/zmx2_s95_v2.out', rlog='receipts/n95_zmx2_d4_roots.log.gz',
             wlog='receipts/controls/n95_control_nowall_zmx2_d4_roots.log.gz', rzm='receipts/n95_zm_mixed'),
}


def composite(zl: dict, zm: dict, k: int) -> dict:
    """Does every cell of [0, k/2]^2 x [0, 1/2] carry a certified decision of exactly one checker?"""
    fail = set(zl['failing'])
    need = set()
    for key in fail:
        need |= subcells(key)
    have = set(zm['_cells'])
    cmax = 5 * k
    return dict(zmx2_roots_complete=zl['roots_are_exactly_the_grid'], zmx2_certified=zl['certified_roots'],
                zmx2_failing=len(fail), zm_cells=len(have), zm_cells_needed=len(need),
                zm_cells_equal_subcells_of_failing=have == need,
                zm_cells_missing=sorted(need - have)[:5], zm_cells_extra=sorted(have - need)[:5],
                every_cell_decided=(bool(zl.get('header_ok')) and zl['roots_are_exactly_the_grid'] and have == need
                                    and not zl['problems'] and not zm['problems']),
                region='[0,%d/2]^2 x [0,1/2], %d x %d x 4 roots' % (k, cmax, cmax))


def cmd_records(a) -> dict:
    n = a.n
    k = math.isqrt(n - 1) + 1
    P = PACKETS[n]
    pk = a.packet
    src = os.path.join(pk, P['src'])
    data = read_bytes(os.path.join(src, P['cover']))
    cv = Cover(data)
    sha = hashlib.sha256(data).hexdigest()
    fnv = '%016x' % fnv1a64(data)
    total = str(cv.total())
    out = dict(n=n, k=k, cover_sha256=sha, cover_fnv1a64=fnv)
    logs = {}
    for name, rel in (('source', os.path.join(P['src'], P['zlog'])), ('replay', P['rlog']), ('nowall', P['wlog'])):
        logs[name] = read_zmx2_log(os.path.join(pk, rel), k, fnv)
    # the wall control ran on a different cover (the published one without its wall segments): its hash differs
    for name, zl in logs.items():
        out['zmx2_' + name] = {key: v for key, v in zl.items() if not key.startswith('_')}
        out['zmx2_' + name]['failing'] = [list(f) for f in zl['failing']]
    listed = sorted(tuple(fbox(ln.strip())) for ln in open(os.path.join(src, 'records/zmx2/failing_roots.txt'))
                    if ln.strip())
    fail_boxes = sorted((F(i, 10), F(i + 1, 10), F(j, 10), F(j + 1, 10), F(kk, 8), F(kk + 1, 8))
                        for i, j, kk in logs['source']['failing'])
    out['failing_roots_txt_equals_source_log'] = listed == fail_boxes
    # .out summary line
    m = re.search(r'^done in \S+ wall: roots (\d+) \(missing (\d+)\), boxes (\d+), certified (\d+), empty (\d+), '
                  r'uncertified (\d+), max depth (\d+)', open(os.path.join(src, P['zout'])).read(), re.M)
    if m:
        c = logs['source']['census']
        out['source_out_summary_matches_log'] = tuple(int(v) for v in m.groups()) == (
            logs['source']['roots'], 0, c['boxes'], c['cert'], c['empty'], c['uncert'], c['maxdepth'])
    # source vs replay vs wall control: per-root census and listed boxes
    for other in ('replay', 'nowall'):
        same = logs['source']['_roots'] == logs[other]['_roots']
        out['zmx2_%s_census_equals_source_root_by_root' % other] = same
        out['zmx2_%s_listed_uncert_boxes_equal_source' % other] = logs['source']['_unc'] == logs[other]['_unc']
    # zm_mixed record sets
    zms = {'source': read_zm_dir(os.path.join(src, 'records/zm_mixed'), sha, total),
           'replay': read_zm_dir(os.path.join(pk, P['rzm']), sha, total)}
    for name, zm in zms.items():
        out['zm_' + name] = {key: v for key, v in zm.items() if not key.startswith('_')}
    # jobs.txt <-> records
    jobs = {}
    for ln in open(os.path.join(src, 'records/zm_mixed/jobs.txt')):
        t = ln.split()
        if t:
            jobs['j%s.jsonl' % t[0]] = tuple(F(v) for v in t[1:7])
    jm = all(tuple(F(v) for v in zms['source']['_recs'][fn]['root']) == box for fn, box in jobs.items()
             if fn in zms['source']['_recs'])
    out['jobs_txt'] = dict(jobs=len(jobs), all_have_a_record=set(jobs) == set(zms['source']['_recs']),
                           regions_match_records=jm)
    # source vs replay records: equal apart from the input path and the CPU time
    eq = True
    for fn, h in zms['source']['_heads'].items():
        h2 = zms['replay']['_heads'].get(fn)
        r1 = dict(zms['source']['_recs'][fn])
        r2 = dict(zms['replay']['_recs'].get(fn, {}))
        if h2 is None:
            eq = False
            continue
        hh1 = {kk: v for kk, v in h.items() if kk != 'input'}
        hh2 = {kk: v for kk, v in h2.items() if kk != 'input'}
        s1 = {kk: v for kk, v in r1['st'].items() if kk != 'cpu'}
        s2 = {kk: v for kk, v in r2['st'].items() if kk != 'cpu'}
        r1.pop('st')
        r2.pop('st')
        eq &= hh1 == hh2 and s1 == s2 and r1 == r2
    out['zm_replay_equals_source_apart_from_path_and_cpu'] = eq and set(zms['source']['_heads']) == set(
        zms['replay']['_heads'])
    # the composite, from the source's records and from the replay's own
    out['composite_source'] = composite(logs['source'], zms['source'], k)
    out['composite_replay'] = composite(logs['replay'], zms['replay'], k)
    # where the failing roots are, and whether any wall line is within reach of a zm_mixed cell
    fr = []
    for i, j, kk in logs['source']['failing']:
        x0, y0 = F(i, 10), F(j, 10)
        dist = min(x0, y0)                           # distance of the centre cell from the walls x = 0, y = 0
        reg = 'corner [0,5/2)^2' if (x0 + F(1, 10) <= F(5, 2) and y0 + F(1, 10) <= F(5, 2)) else 'cross'
        seam = any(abs(v - F(5, 2)) <= REACH for v in (x0, x0 + F(1, 10), y0, y0 + F(1, 10)))
        fr.append(dict(root='[%s,%s]x[%s,%s]x u[%s,%s]' % (x0, x0 + F(1, 10), y0, y0 + F(1, 10), F(kk, 8),
                                                           F(kk + 1, 8)),
                       theta_deg='%.2f-%.2f' % (2 * math.degrees(math.atan(kk / 8)),
                                                2 * math.degrees(math.atan((kk + 1) / 8))),
                       uncert=logs['source']['_roots'][(i, j, kk)]['uncert'],
                       min_centre_distance_to_wall=str(dist), wall_lines_within_reach=dist <= REACH,
                       region=reg, near_seam_x_or_y_5_2=seam,
                       contains_u_1_3=F(kk, 8) <= F(1, 3) <= F(kk + 1, 8)))
    out['failing_roots'] = fr
    out['zm_cells_with_a_wall_line_within_reach'] = sum(1 for (i, j, kk) in zms['source']['_cells']
                                                        if min(F(i, 20), F(j, 20)) <= REACH)
    # the root of the source's second route (06993982, not retained): which zmx2 root holds it, and its census
    if n == 76:
        R = (F(27, 20), F(7, 5), F(13, 10), F(27, 20), F(1, 4), F(9, 32))
        key = (int(R[0] * 10), int(R[2] * 10), int(R[4] * 8))
        Rz = (F(key[0], 10), F(key[0] + 1, 10), F(key[1], 10), F(key[1] + 1, 10), F(key[2], 8), F(key[2] + 1, 8))
        inside = Rz[0] <= R[0] and R[1] <= Rz[1] and Rz[2] <= R[2] and R[3] <= Rz[3] and Rz[4] <= R[4] and R[5] <= Rz[5]
        out['second_route_root_R'] = dict(R='[27/20,7/5]x[13/10,27/20]x u[1/4,9/32]', zmx2_root=[str(v) for v in Rz],
                                          R_inside_that_root=inside,
                                          zmx2_census=logs['source']['_roots'][key],
                                          zmx2_certified=key not in set(logs['source']['failing']))
    out['ok'] = (out['composite_source']['every_cell_decided'] and out['composite_replay']['every_cell_decided']
                 and out['failing_roots_txt_equals_source_log'] and logs['source']['header_ok']
                 and logs['replay']['header_ok'])
    return out


# ============================================================================================ poses
def rand_frac(rng: random.Random, lo: F, hi: F, den: int) -> F:
    """A random rational in [lo, hi] with denominator den, refined until the interval holds one."""
    if lo == hi:
        return lo
    while True:
        a, b = math.ceil(lo * den), math.floor(hi * den)
        if a <= b:
            return F(rng.randint(a, b), den)
        den *= 2


# The triage's control poses (receipts/controls/*pose*.log): the pose, and zm_mixed.py pose's exact mu there for the
# published cover and for the mutated cover (drop-heaviest-point, drop-heaviest-segment).
CONTROL_POSES = {
    76: [((F(1500011, 1000000), F(1500002, 1000000), F(1, 250000)),
          '7890087444062733817589347613/7812499999875000000000000000',
          '7791864319064305387589347613/7812499999875000000000000000'),
         ((F(500006, 1000000), F(7, 2), F(19, 5000000)),
          '8393827087780112907255184733/8333333333213000000000000000',
          '7473478837793402735985184733/8333333333213000000000000000')],
    95: [((F(1500011, 1000000), F(750001, 500000), F(1, 250000)),
          '7890087444062733817589347613/7812499999875000000000000000',
          '7791864319064305387589347613/7812499999875000000000000000'),
         ((F(500001, 1000000), F(4500001, 1000000), F(1, 5000000)),
          '843334565845979785768980657/833333333333300000000000000',
          '705154582512651979634980657/833333333333300000000000000')],
}


def cmd_poses(a) -> dict:
    n = a.n
    k = math.isqrt(n - 1) + 1
    P = PACKETS[n]
    cv = Cover(read_bytes(a.cover))
    s = cv.side
    ev = Evaluator(cv)
    rng = random.Random(a.seed)
    den = 2 ** 20
    out = dict(n=n, seed=a.seed, denominator=den)
    t0 = time.process_time()
    # 0. the published control poses of the triage (exact values printed by zm_mixed.py pose)
    ctl = [(p, z) for p, z, _ in CONTROL_POSES[n]]
    out['published_control_poses'] = [dict(pose=[str(v) for v in p], mu=str(mass_f(ev, *p)), zm_mixed_pose=z,
                                           agrees=str(mass_f(ev, *p)) == z) for p, z in ctl]

    def sample_box(box, count, label):
        lo = None
        worst = None
        nadm = 0
        below = 0
        for _ in range(count):
            for _try in range(50):
                cx = rand_frac(rng, box[0], box[1], den)
                cy = rand_frac(rng, box[2], box[3], den)
                u = rand_frac(rng, box[4], box[5], den)
                if adm_f(ev, cx, cy, u):
                    break
            else:
                continue
            nadm += 1
            m = mass_f(ev, cx, cy, u)
            if m < 1:
                below += 1
            if lo is None or m < lo:
                lo, worst = m, (cx, cy, u)
        return dict(label=label, poses=nadm, below_one=below, min_mu=None if lo is None else '%.9f' % float(lo),
                    argmin=None if worst is None else [str(v) for v in worst])

    # 1. the D4 region, uniformly
    region = (F(0), s / 2, F(0), s / 2, F(0), F(1, 2))
    out['d4_region_uniform'] = sample_box(region, a.count, 'D4 region')
    # 2. the zmx2-failing roots and 3. the uncertified boxes zmx2 lists
    zl = read_zmx2_log(os.path.join(a.packet, P['src'], P['zlog']), k, '%016x' % fnv1a64(read_bytes(a.cover)))
    fr = []
    for i, j, kk in zl['failing']:
        box = (F(i, 10), F(i + 1, 10), F(j, 10), F(j + 1, 10), F(kk, 8), F(kk + 1, 8))
        fr.append(sample_box(box, a.per_root, 'root %d,%d,%d' % (i, j, kk)))
    out['failing_roots'] = fr
    ub = []
    ncorner = 0
    cmax = 5 * k
    for rid, boxes in sorted(zl['_unc'].items()):
        for b in boxes:
            pts = []
            for cx in (b[0], b[1]):
                for cy in (b[2], b[3]):
                    for u in (b[4], b[5]):
                        if adm_f(ev, cx, cy, u):
                            pts.append(mass_f(ev, cx, cy, u))
            r = sample_box(b, a.per_box, 'uncert box of root %d' % rid)
            ncorner += len(pts)
            r['corner_min_mu'] = '%.9f' % float(min(pts)) if pts else None
            r['corners_below_one'] = sum(1 for m in pts if m < 1)
            ub.append(r)
    out['uncert_boxes'] = dict(boxes=len(ub), poses=sum(r['poses'] for r in ub), corner_poses=ncorner,
                               below_one=sum(r['below_one'] + r['corners_below_one'] for r in ub),
                               min_mu='%.9f' % min(float(r['min_mu']) for r in ub if r['min_mu']),
                               per_box=ub if len(ub) <= 20 else ub[:20])
    # 4. random poses of the whole container, folded into the region: mu equal at both, image in the region
    fold_res = dict(poses=0, mu_equal=0, image_in_region=0, below_one=0, steps=Counter(), landing=Counter())
    failset = set(zl['failing'])
    lo = None
    while fold_res['poses'] < a.fold_count:
        cx = rand_frac(rng, F(0), s, den)
        cy = rand_frac(rng, F(0), s, den)
        u = rand_frac(rng, F(0), F(1), den)          # theta in [0, 90deg]
        if not adm_f(ev, cx, cy, u):
            continue
        fold_res['poses'] += 1
        m0 = mass_f(ev, cx, cy, u)
        gx, gy, gu, steps = fold(cx, cy, u, s)
        m1 = mass_f(ev, gx, gy, gu)
        fold_res['mu_equal'] += m0 == m1
        inreg = 0 <= gx <= s / 2 and 0 <= gy <= s / 2 and 0 <= gu and gu * gu + 2 * gu - 1 <= 0 and gu <= F(1, 2)
        fold_res['image_in_region'] += inreg and adm_f(ev, gx, gy, gu)
        fold_res['below_one'] += m0 < 1
        fold_res['steps'][' '.join(steps) or 'none'] += 1
        key = (min(int(gx * 10), cmax - 1), min(int(gy * 10), cmax - 1), min(int(gu * 8), 3))
        fold_res['landing']['zm_mixed cell' if key in failset else 'zmx2 root'] += 1
        if lo is None or m0 < lo:
            lo = m0
    fold_res['min_mu'] = '%.9f' % float(lo)
    fold_res['steps'] = dict(fold_res['steps'])
    fold_res['landing'] = dict(fold_res['landing'])
    out['folded_whole_container'] = fold_res
    # 5. the coincidence angles: u = 1/3 (theta = 2 atan(1/3), tan theta = 3/4) in the failing roots that contain it
    #    and near u = sqrt(26) - 5 (theta = atan(1/5)) in the failing roots of the first u-bin
    co = []
    for i, j, kk in zl['failing']:
        box = (F(i, 10), F(i + 1, 10), F(j, 10), F(j + 1, 10), F(kk, 8), F(kk + 1, 8))
        if box[4] <= F(1, 3) <= box[5]:
            co.append(sample_box(box[:4] + (F(1, 3), F(1, 3)), a.per_root, 'u = 1/3 in root %d,%d,%d' % (i, j, kk)))
        u5 = F(math.sqrt(26) - 5).limit_denominator(10 ** 9)
        if box[4] <= u5 <= box[5]:
            co.append(sample_box(box[:4] + (u5 - F(1, 10 ** 6), u5 + F(1, 10 ** 6)), a.per_root,
                                 'u near sqrt26-5 in root %d,%d,%d' % (i, j, kk)))
    out['coincidence_angles'] = co
    # 6. tile germs: theta -> 0+ with the edges on (or next to) the unit grid lines, where the mass is
    #    discontinuous and a closed square counts a segment on its edge in full; and one-cut germs, one edge pair
    #    on a grid line, the other coordinate anywhere
    gm = []
    half = int(s) // 2 if s.denominator == 1 else 0
    eps = F(1, 10 ** 4)
    for i in range(half + 1):
        for j in range(half + 1):
            cx0, cy0 = F(2 * i + 1, 2), F(2 * j + 1, 2)
            if cx0 > s / 2 + F(1, 2) or cy0 > s / 2 + F(1, 2):
                continue
            gm.append(sample_box((cx0 - eps, cx0 + eps, cy0 - eps, cy0 + eps, F(0), eps), a.per_germ,
                                 'tile germ at (%s, %s)' % (cx0, cy0)))
    for i in range(half + 1):
        cx0 = F(2 * i + 1, 2)
        gm.append(sample_box((cx0 - eps, cx0 + eps, F(1, 2), s / 2, F(0), eps), a.per_germ,
                             'one-cut germ at x = %s' % cx0))
    gm.sort(key=lambda r: float(r['min_mu']) if r['min_mu'] else 9)
    out['germs'] = dict(boxes=len(gm), poses=sum(r['poses'] for r in gm), below_one=sum(r['below_one'] for r in gm),
                        lowest=gm[:6])
    # 7. local descent from the lowest poses found (exact mu at every step)
    starts = []
    for r in [out['d4_region_uniform']] + fr + co + gm:
        if r['argmin']:
            starts.append((F(r['min_mu']), tuple(F(v) for v in r['argmin'])))
    starts.sort()
    best = None
    for _m, (cx, cy, u) in starts[:a.descents]:
        cur = mass_f(ev, cx, cy, u)
        for step in (F(1, 10 ** 3), F(1, 10 ** 4), F(1, 10 ** 5), F(1, 10 ** 6)):
            for _ in range(a.descent_steps):
                d = [F(rng.randint(-1000, 1000), 1000) * step for _ in range(3)]
                cand = (cx + d[0], cy + d[1], min(max(u + d[2], F(0)), F(1, 2)))
                if not adm_f(ev, *cand):
                    continue
                m = mass_f(ev, *cand)
                if m < cur:
                    cur, (cx, cy, u) = m, cand
        if best is None or cur < best[0]:
            best = (cur, (cx, cy, u))
    if best:
        out['descent_min'] = dict(mu='%.12f' % float(best[0]), mu_exact_below_one=best[0] < 1,
                                  pose=[str(v) for v in best[1]],
                                  theta_deg='%.6f' % (2 * math.degrees(math.atan(float(best[1][2])))))
    out['cpu_s'] = round(time.process_time() - t0, 1)
    allb = out['d4_region_uniform']['below_one'] + sum(r['below_one'] for r in fr) + out['uncert_boxes'][
        'below_one'] + fold_res['below_one'] + sum(r['below_one'] for r in co) + out['germs']['below_one']
    out['poses_below_one'] = allb
    out['ok'] = (allb == 0 and fold_res['mu_equal'] == fold_res['poses'] and fold_res['image_in_region'] ==
                 fold_res['poses'] and all(c['agrees'] for c in out['published_control_poses'])
                 and not (best and best[0] < 1))
    return out


# ============================================================================================ mutants
def orbit_of(cv: Cover, piece, is_point: bool):
    S = cv.S
    gs = d4_maps(S).values()
    if is_point:
        X, Y, w = piece
        return {g(X, Y) for g in gs}
    X0, Y0, X1, Y1, w = piece
    return {frozenset((g(X0, Y0), g(X1, Y1))) for g in gs}


def cmd_mutants(a) -> dict:
    cv = Cover(read_bytes(a.cover))
    ev0 = Evaluator(cv)
    rng = random.Random(a.seed)
    out = dict(n=a.n, mutants=[])
    D, W = cv.D, cv.W
    hp = max(cv.points, key=lambda p: p[2])
    hs = max(cv.segs, key=lambda q: q[4])
    po = orbit_of(cv, hp, True)
    so = orbit_of(cv, hs, False)
    m_pt = cv.replaced([p for p in cv.points if (p[0], p[1]) not in po or p[2] != hp[2]], cv.segs)
    m_sg = cv.replaced(cv.points, [q for q in cv.segs if frozenset(((q[0], q[1]), (q[2], q[3]))) not in so
                                   or q[4] != hs[4]])

    def search_near(evm, X, Y, tries):
        """poses whose square holds (X/D, Y/D) near an edge; the lowest exact mu of the mutant."""
        best = None
        for _ in range(tries):
            u = F(rng.randint(0, 2 ** 16), 2 ** 20)            # theta near 0, where germs are tight
            cx = F(X, D) + F(rng.randint(-2 ** 19, 2 ** 19), 2 ** 20)
            cy = F(Y, D) + F(rng.randint(-2 ** 19, 2 ** 19), 2 ** 20)
            if not adm_f(evm, cx, cy, u):
                continue
            m = mass_f(evm, cx, cy, u)
            if best is None or m < best[0]:
                best = (m, (cx, cy, u))
        return best

    for name, mut, anchor in (('drop the heaviest point orbit', m_pt, (hp[0], hp[1])),
                              ('drop the heaviest segment orbit', m_sg, ((hs[0] + hs[2]) // 2, (hs[1] + hs[3]) // 2))):
        evm = Evaluator(mut)
        best = search_near(evm, *anchor, a.tries)
        rec = dict(mutation=name, removed_mass=str(cv.total() - mut.total()), total=str(mut.total()))
        if best:
            m0 = mass_f(ev0, *best[1])
            rec.update(pose=[str(v) for v in best[1]], mu_mutant='%.12f' % float(best[0]),
                       mu_published='%.12f' % float(m0), refused_at_pose=best[0] < 1, published_ok_there=m0 >= 1)
        out['mutants'].append(rec)
    # the triage's own control poses: the mutants there, against zm_mixed.py pose's exact values
    for name, mut, (pose, zpub, zmut) in zip(('drop the heaviest point orbit', 'drop the heaviest segment orbit'),
                                             (m_pt, m_sg), CONTROL_POSES[a.n]):
        evm = Evaluator(mut)
        mm, mp = mass_f(evm, *pose), mass_f(ev0, *pose)
        out['mutants'].append(dict(mutation=name + ', at the triage control pose', pose=[str(v) for v in pose],
                                   mu_mutant=str(mm), mu_mutant_decimal='%.12f' % float(mm),
                                   mu_mutant_agrees_with_zm_mixed_pose=str(mm) == zmut,
                                   mu_published='%.12f' % float(mp), mu_published_agrees_with_zm_mixed_pose=str(mp) == zpub,
                                   refused_at_pose=mm < 1))
    # every mass scaled by (1 - eps), at the lowest pose the descent found (given on the command line)
    if a.low_pose:
        pose = tuple(F(v) for v in a.low_pose.split(','))
        m0 = mass_f(ev0, *pose)
        lam = F(a.scale)
        out['mutants'].append(dict(mutation='every mass scaled by %s' % lam, pose=[str(v) for v in pose],
                                   mu_published='%.12f' % float(m0), mu_mutant='%.12f' % float(m0 * lam),
                                   refused_at_pose=m0 * lam < 1, total=str(cv.total() * lam)))
    # the zmx2 D4 root that holds each pose (a pose on a root boundary lies in both; the lower is named)
    cmax = int(5 * cv.side)
    for rec in out['mutants']:
        if 'pose' in rec:
            cx, cy, u = (F(v) for v in rec['pose'])
            if cx <= cv.side / 2 and cy <= cv.side / 2 and u <= F(1, 2):
                rec['zmx2_root'] = [min(math.floor(cx * 10), cmax - 1), min(math.floor(cy * 10), cmax - 1),
                                    min(math.floor(u * 8), 3)]
    # the cover without its wall segments: still a cover?  sampled flush axis-parallel squares on the walls
    nw = cv.replaced(cv.points, [q for q in cv.segs if not ((q[0] == q[2] and q[0] in (0, cv.S)) or
                                                            (q[1] == q[3] and q[1] in (0, cv.S)))])
    evn = Evaluator(nw)
    lo = None
    lo0 = None
    cnt = 0
    for _ in range(a.tries):
        t = rand_frac(rng, F(1, 2), cv.side - F(1, 2), 2 ** 20)
        for cx, cy in ((F(1, 2), t), (cv.side - F(1, 2), t), (t, F(1, 2)), (t, cv.side - F(1, 2))):
            cnt += 1
            m = mass_f(evn, cx, cy, F(0))
            m0 = mass_f(ev0, cx, cy, F(0))
            lo = m if lo is None or m < lo else lo
            lo0 = m0 if lo0 is None or m0 < lo0 else lo0
    out['without_wall_segments'] = dict(total=str(nw.total()), flush_axis_parallel_squares=cnt,
                                        min_mu_without='%.12f' % float(lo), min_mu_published='%.12f' % float(lo0))
    if a.write_mutants:
        os.makedirs(a.write_mutants, exist_ok=True)
        lam = F(a.scale)
        scaled = cv.replaced([(X, Y, lam.numerator * w) for X, Y, w in cv.points],
                             [(*q[:4], lam.numerator * q[4]) for q in cv.segs])
        scaled.W = lam.denominator * W
        for tag, mut in (('drop-heaviest-point', m_pt), ('drop-heaviest-segment', m_sg), ('nowall', nw),
                         ('scaled-%d-%d' % (lam.numerator, lam.denominator), scaled)):
            p = os.path.join(a.write_mutants, 'n%d_%s.txt' % (a.n, tag))
            with open(p, 'w') as fh:
                fh.write('mixed 1\n%d %d\n%d\n%d\n%d\n' % (cv.s_num, cv.s_den, D, mut.W, len(mut.points)))
                fh.writelines('%d %d %d\n' % q for q in mut.points)
                fh.write('%d\n' % len(mut.segs))
                fh.writelines('%d %d %d %d %d\n' % q for q in mut.segs)
                fh.write('0\n')
            out.setdefault('written', []).append(dict(path=os.path.basename(p), total=str(mut.total()),
                                                      sha256=hashlib.sha256(open(p, 'rb').read()).hexdigest(),
                                                      fnv1a64='%016x' % fnv1a64(open(p, 'rb').read())))
    return out


# ============================================================================================ a local mutant
def captured_pieces(ev: Evaluator, cx: F, cy: F, u: F):
    """Every piece with positive mass inside Q at one pose: ('pt', index) or ('seg', index), with its mass."""
    cv = ev.cv
    out = []
    for i, (X, Y, w) in enumerate(cv.points):
        if w and mass_f(Evaluator(cv.replaced([(X, Y, w)], [])), cx, cy, u) > 0:
            out.append((F(w, cv.W), 'pt', i))
    for i, q in enumerate(cv.segs):
        if q[4]:
            m = mass_f(Evaluator(cv.replaced([], [q])), cx, cy, u)
            if m > 0:
                out.append((m, 'seg', i))
    out.sort(reverse=True)
    return out


def cmd_localmut(a) -> dict:
    """A mutant that removes the D4 orbit of the heaviest piece captured at one pose, so that the hole stays near
    that pose's orbit and the rest of the cover keeps its margin."""
    cv = Cover(read_bytes(a.cover))
    ev = Evaluator(cv)
    pose = tuple(F(v) for v in a.pose.split(','))
    near = [p for p in cv.points if abs(F(p[0], cv.D) - pose[0]) <= 1 and abs(F(p[1], cv.D) - pose[1]) <= 1]
    nsegs = [q for q in cv.segs if min(abs(F(q[0], cv.D) - pose[0]), abs(F(q[2], cv.D) - pose[0])) <= 1 and
             min(abs(F(q[1], cv.D) - pose[1]), abs(F(q[3], cv.D) - pose[1])) <= 1]
    sub = Evaluator(cv.replaced(near, nsegs))
    caps = captured_pieces(sub, *pose)
    m0 = mass_f(ev, *pose)
    out = dict(pose=a.pose, mu_published=str(m0), mu_published_decimal='%.12f' % float(m0),
               heaviest_captured=[dict(kind=k, mass='%.9f' % float(m), piece=(near if k == 'pt' else nsegs)[i])
                                  for m, k, i in caps[:8]])
    for m, kind, i in caps:
        piece = (near if kind == 'pt' else nsegs)[i]
        if m0 - m >= 1:
            continue
        orb = orbit_of(cv, piece, kind == 'pt')
        if kind == 'pt':
            mut = cv.replaced([p for p in cv.points if not ((p[0], p[1]) in orb and p[2] == piece[2])], cv.segs)
        else:
            mut = cv.replaced(cv.points, [q for q in cv.segs if not (frozenset(((q[0], q[1]), (q[2], q[3]))) in orb
                                                                     and q[4] == piece[4])])
        mm = mass_f(Evaluator(mut), *pose)
        out['removed'] = dict(kind=kind, piece=piece, orbit_size=len(orb), mass_removed=str(cv.total() - mut.total()))
        out['mu_mutant'] = str(mm)
        out['mu_mutant_decimal'] = '%.12f' % float(mm)
        out['refused_at_pose'] = mm < 1
        if a.write:
            with open(a.write, 'w') as fh:
                fh.write('mixed 1\n%d %d\n%d\n%d\n%d\n' % (cv.s_num, cv.s_den, cv.D, cv.W, len(mut.points)))
                fh.writelines('%d %d %d\n' % q for q in mut.points)
                fh.write('%d\n' % len(mut.segs))
                fh.writelines('%d %d %d %d %d\n' % q for q in mut.segs)
                fh.write('0\n')
            data = open(a.write, 'rb').read()
            out['written'] = dict(path=os.path.basename(a.write), sha256=hashlib.sha256(data).hexdigest(),
                                  total=str(mut.total()))
        break
    return out


# ============================================================================================ one cell's minimum
def cmd_cellmin(a) -> dict:
    """The lowest exact mu found in one pose box: random admissible poses, the box's corners, then a local descent
    from the lowest few; used to place a scaled mutant's hole inside one zm_mixed.py cell."""
    cv = Cover(read_bytes(a.cover))
    ev = Evaluator(cv)
    rng = random.Random(a.seed)
    box = tuple(F(v) for v in a.box.split(','))
    cand = []
    for cx in (box[0], box[1]):
        for cy in (box[2], box[3]):
            for u in (box[4], box[5]):
                if adm_f(ev, cx, cy, u):
                    cand.append((mass_f(ev, cx, cy, u), (cx, cy, u)))
    for _ in range(a.count):
        p = (rand_frac(rng, box[0], box[1], 2 ** 24), rand_frac(rng, box[2], box[3], 2 ** 24),
             rand_frac(rng, box[4], box[5], 2 ** 24))
        if adm_f(ev, *p):
            cand.append((mass_f(ev, *p), p))
    cand.sort()
    best = cand[0]
    inside = lambda p: box[0] <= p[0] <= box[1] and box[2] <= p[1] <= box[3] and box[4] <= p[2] <= box[5]  # noqa
    for m0, p in cand[:a.descents]:
        cur, q = m0, p
        for step in (F(1, 10 ** 3), F(1, 10 ** 4), F(1, 10 ** 5), F(1, 10 ** 6), F(1, 10 ** 7)):
            for _ in range(a.descent_steps):
                d = [F(rng.randint(-1000, 1000), 1000) * step for _ in range(3)]
                c2 = (q[0] + d[0], q[1] + d[1], q[2] + d[2])
                if not inside(c2) or not adm_f(ev, *c2):
                    continue
                m = mass_f(ev, *c2)
                if m < cur:
                    cur, q = m, c2
        if cur < best[0]:
            best = (cur, q)
    thr = F(a.threshold) if a.threshold else None
    frac = None
    if thr is not None:
        below = sum(1 for m, _ in cand if m < thr)
        frac = '%d of %d sampled poses' % (below, len(cand))
    return dict(box=a.box, poses=len(cand), min_mu=str(best[0]), min_mu_decimal='%.12f' % float(best[0]),
                argmin=[str(v) for v in best[1]], threshold=a.threshold, below_threshold=frac,
                lowest_sampled=['%.9f' % float(m) for m, _ in cand[:5]])


# ============================================================================================ tiling controls
def cmd_tiling(a) -> dict:
    """Mutated record sets, each run through the author's check_coverage.py (python3 -I, from a scratch copy) and
    through composite() above."""
    n = a.n
    k = math.isqrt(n - 1) + 1
    P = PACKETS[n]
    src = os.path.join(a.packet, P['src'])
    data = read_bytes(os.path.join(src, P['cover']))
    sha = hashlib.sha256(data).hexdigest()
    fnv = '%016x' % fnv1a64(data)
    total = str(Cover(data).total())
    zlog = os.path.join(src, P['zlog'])
    zdir = os.path.join(src, 'records/zm_mixed')
    os.makedirs(a.work, exist_ok=True)
    work = tempfile.mkdtemp(prefix='k2m5-tiling-', dir=a.work)
    out = dict(n=n, checker=a.check_coverage, checker_sha256=hashlib.sha256(open(a.check_coverage, 'rb').read())
               .hexdigest(), controls=[])
    zl = read_zmx2_log(zlog, k, fnv)

    def run(tag, mutate):
        d = os.path.join(work, tag)
        shutil.copytree(zdir, d)
        note = mutate(d)
        r = subprocess.run([a.python, '-I', a.check_coverage, zlog, d, sha] + ([str(k)] if n != 76 else []),
                           capture_output=True, text=True)
        zm = read_zm_dir(d, sha, total)
        mine = composite(zl, zm, k)
        out['controls'].append(dict(control=tag, what=note, check_coverage_exit=r.returncode,
                                    check_coverage_last_line=(r.stdout.strip().splitlines() or [''])[-1] if
                                    r.returncode == 0 else (r.stderr.strip().splitlines() or [''])[-1][:160],
                                    this_program_every_cell_decided=mine['every_cell_decided'],
                                    this_program_problems=zm['problems'][:3]))

    def first_file(d):
        return sorted(f for f in os.listdir(d) if f.endswith('.jsonl'))[0]

    def edit(d, fn, fun):
        p = os.path.join(d, fn)
        rows = [json.loads(ln) for ln in open(p) if ln.strip()]
        fun(rows)
        with open(p, 'w') as fh:
            fh.writelines(json.dumps(r) + '\n' for r in rows)

    run('published', lambda d: 'the source records unchanged')

    def drop(d):
        fn = first_file(d)
        os.remove(os.path.join(d, fn))
        return 'record %s removed' % fn
    run('one-record-removed', drop)

    def shift(d):
        # a cell at the low-x edge of its failing root, moved by 1/40 in x: same size, inside the root, distinct,
        # total volume unchanged; it overlaps its neighbour and leaves a slab of width 1/40 undecided
        for fn in sorted(f for f in os.listdir(d) if f.endswith('.jsonl')):
            rows = [json.loads(ln) for ln in open(os.path.join(d, fn)) if ln.strip()]
            root = [F(v) for v in rows[1]['root']]
            if (root[0] * 10).denominator == 1:
                def f(rows, root=root):
                    nr = [root[0] + F(1, 40), root[1] + F(1, 40)] + root[2:]
                    rows[1]['root'] = [str(v) for v in nr]
                    rows[0]['settings']['region'].update(cx_lo=str(nr[0]), cx_hi=str(nr[1]))
                edit(d, fn, f)
                return '%s: root shifted by +1/40 in x (header region with it)' % fn
        return 'no candidate'
    run('cell-shifted-1/40', shift)

    def settings(d):
        fn = first_file(d)
        def f(rows):
            rows[0]['settings']['cert_mode'] = False
            rows[0]['settings']['depth'] = 6
        edit(d, fn, f)
        return '%s: header says cert_mode false, depth 6' % fn
    run('other-settings', settings)

    def checker(d):
        fn = first_file(d)
        def f(rows):
            rows[0]['sha256']['zm_mixed.py'] = '0' * 64
        edit(d, fn, f)
        return '%s: header names another zm_mixed.py' % fn
    run('other-checker-digest', checker)

    def noheader(d):
        fn = first_file(d)
        def f(rows):
            del rows[0]
        edit(d, fn, f)
        return '%s: header line removed' % fn
    run('header-removed', noheader)

    def other_cover(d):
        fn = first_file(d)
        def f(rows):
            rows[0]['sha256']['input'] = '0' * 64
        edit(d, fn, f)
        return '%s: header names another cover' % fn
    run('other-cover-digest', other_cover)

    # the zmx2 root log: a log of another cover, and a log with one certified root missing
    def run_log(tag, note, transform):
        p = os.path.join(work, tag + '.log')
        lines = transform(read_bytes(zlog).decode('ascii').splitlines(keepends=True))
        with open(p, 'w') as fh:
            fh.writelines(lines)
        r = subprocess.run([a.python, '-I', a.check_coverage, p, zdir, sha] + ([str(k)] if n != 76 else []),
                           capture_output=True, text=True)
        zl2 = read_zmx2_log(p, k, fnv)
        mine = composite(zl2, read_zm_dir(zdir, sha, total), k)
        out['controls'].append(dict(control=tag, what=note, check_coverage_exit=r.returncode,
                                    check_coverage_last_line=(r.stdout.strip().splitlines() or [''])[-1] if
                                    r.returncode == 0 else (r.stderr.strip().splitlines() or [''])[-1][:160],
                                    this_program_every_cell_decided=mine['every_cell_decided'],
                                    this_program_problems=(zl2['problems'] + ([] if zl2.get('header_ok') else
                                                                              ['zmx2 log header: not this cover '
                                                                               'or not the D4 settings']))[:3]))

    def other_hash(lines):
        lines[0] = re.sub(r'hash=[0-9a-f]{16}', 'hash=' + '0' * 16, lines[0])
        return lines
    run_log('zmx2-log-of-another-cover', 'zmx2 log header names another cover (FNV-1a hash)', other_hash)

    def drop_root(lines):
        for i, ln in enumerate(lines):
            if ln.startswith('ROOT ') and ' uncert 0 ' in ln and ' empty 0 ' in ln:
                return lines[:i] + lines[i + 1:]
        return lines
    run_log('zmx2-root-missing', 'one certified ROOT line removed from the zmx2 log', drop_root)
    shutil.rmtree(work)
    out['ok'] = all((c['control'] == 'published') == c['this_program_every_cell_decided'] for c in out['controls'])
    return out


# ============================================================================================ main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('cover')
    p.add_argument('cover')
    p.add_argument('n', type=int)
    p.add_argument('--out')
    p = sub.add_parser('records')
    p.add_argument('packet')
    p.add_argument('n', type=int)
    p.add_argument('--out')
    p = sub.add_parser('poses')
    p.add_argument('cover')
    p.add_argument('n', type=int)
    p.add_argument('packet')
    p.add_argument('--seed', type=int, default=20261016)
    p.add_argument('--count', type=int, default=2000)
    p.add_argument('--per-root', type=int, default=150)
    p.add_argument('--per-box', type=int, default=8)
    p.add_argument('--fold-count', type=int, default=1000)
    p.add_argument('--per-germ', type=int, default=40)
    p.add_argument('--descents', type=int, default=8)
    p.add_argument('--descent-steps', type=int, default=60)
    p.add_argument('--out')
    p = sub.add_parser('mutants')
    p.add_argument('cover')
    p.add_argument('n', type=int)
    p.add_argument('--seed', type=int, default=20261016)
    p.add_argument('--tries', type=int, default=400)
    p.add_argument('--low-pose', help='cx,cy,u of a low pose of the published cover (for the scaled mutant)')
    p.add_argument('--scale', default='999/1000', help='the factor of the scaled mutant')
    p.add_argument('--write-mutants', help='directory to write the mutated covers into')
    p.add_argument('--out')
    p = sub.add_parser('localmut')
    p.add_argument('cover')
    p.add_argument('n', type=int)
    p.add_argument('--pose', required=True, help='cx,cy,u (rationals) where the hole should be')
    p.add_argument('--write', help='file to write the mutated cover to')
    p.add_argument('--out')
    p = sub.add_parser('cellmin')
    p.add_argument('cover')
    p.add_argument('n', type=int)
    p.add_argument('--box', required=True, help='x0,x1,y0,y1,u0,u1 (rationals)')
    p.add_argument('--seed', type=int, default=20261016)
    p.add_argument('--count', type=int, default=1500)
    p.add_argument('--descents', type=int, default=6)
    p.add_argument('--descent-steps', type=int, default=60)
    p.add_argument('--threshold', help='count the sampled poses with mu below this')
    p.add_argument('--out')
    p = sub.add_parser('tiling')
    p.add_argument('packet')
    p.add_argument('n', type=int)
    p.add_argument('check_coverage')
    p.add_argument('--python', default=sys.executable)
    p.add_argument('--work', default='tiling-work', help='scratch directory for the mutated record sets')
    p.add_argument('--out')
    a = ap.parse_args()
    t0 = time.time()
    res = dict(cover=cmd_cover, records=cmd_records, poses=cmd_poses, mutants=cmd_mutants, cellmin=cmd_cellmin,
               localmut=cmd_localmut,
               tiling=cmd_tiling)[a.cmd](a)
    res['wall_s'] = round(time.time() - t0, 1)
    res['program'] = dict(name=os.path.basename(__file__),
                          sha256=hashlib.sha256(open(__file__, 'rb').read()).hexdigest(), python=sys.version.split()[0])
    text = json.dumps(res, indent=1, default=str)
    if a.out:
        with open(a.out, 'w') as fh:
            fh.write(text + '\n')
    print(text if len(text) < 6000 else text[:6000] + '\n... (%d characters; see --out)' % len(text))
    return 0 if res.get('ok', True) else 1


if __name__ == '__main__':
    sys.exit(main())
