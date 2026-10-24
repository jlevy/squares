"""Decide the capture condition of mixed_n31_L59775 at chosen net directions, exactly.

Usage:
  python3 -I capture.py CANDIDATE OUTDIR J [J ...] [--mass-scale P/Q] [--tag NAME]
                        [--drop-row K] [--max-nodes N] [--cpu-limit SECONDS]

--mass-scale and --drop-row make the mutants of the controls: every density scaled, or
one listed row (0-based) removed before the expansion.

Written for review-2026-10-23 from the mathematics and SPEC.md's statement of the
condition alone. It imports nothing of the source, of sqverify_fast or of devtools.

The condition at direction j: for every centre c in [r(a_j), L - r(a_j)]^2 the closed
core of side B, centre c and angle theta_j has mu(core) >= 1. The rotation by a quarter
turn about the container's centre maps the core at angle theta_j to the core at the
same angle, and mu is D4-invariant (premises.py decides that), so it is enough to cover
the quadrant [L/2, L - r(a_j)]^2; the upper end is rounded up onto a grid of step
1/(10^17 2^20), which only enlarges the set decided.

Method. A branch and bound over axis-parallel cells of centres. For a cell P with centre
p0 and half-widths hx, hy, and every centre p in it:

  mu(Q(p)) >= mu(K) + 2 eta_u min(Lambda_+u, Lambda_-u) + 2 eta_v min(Lambda_+v, Lambda_-v)

where K is the kernel, the intersection of all cores over the cell (a rotated rectangle
of half-sides B/2 - eta_u and B/2 - eta_v with eta_u = hx cos + hy sin and
eta_v = hx sin + hy cos), and the other terms bound the four slabs of Q(p) outside K
along each edge: the +u and -u slabs have widths eta_u + u.(p - p0) and
eta_u - u.(p - p0), summing to 2 eta_u, so their measure is at least 2 eta_u times the
smaller of their least line densities. Lambda_+u is the sum over rectangles of density
times the smaller of the rectangle's chords on the slab's two extreme lines, which bounds
the least line density from below because a section of a convex set is concave in its
offset (Brunn-Minkowski in one dimension). The bound is exact to first order.

A float64 pass (numpy, vectorised over cells) chooses the cells; each leaf it accepts
is then decided again in exact integer arithmetic (n31_geometry), every rectangle being
gathered from an exact bucket index and classified exactly. The densities are rounded
down onto the grid 2^-64, which only lowers mu. A leaf that fails exactly is split and
decided exactly again. The leaves are checked to be exactly the leaves of one bisection
tree of the quadrant (a walk from the root reaches each once and every branch ends at
one), so they partition it. The decision is the exact pass alone: VERIFIED.

The float pass also evaluates the float capture at the centre of every refused cell past
depth 8; one below 1 - 1e-9 ends the direction, and the exact capture there, by the
second method (n31_brute) with the unrounded densities, decides REFUTED when it is below
one at a centre of the exact domain. Anything else that stops the pass (a node or CPU
budget, a cell at the depth limit) is UNDECIDED, never VERIFIED. At every accepted leaf
it evaluates the float capture at the centre too; the least of these is evaluated
exactly and reported as the least capture found, an upper bound on the true minimum.

Output: OUTDIR/capture-<tag>-<j>.json for each direction, and a line on stdout.
"""

from __future__ import annotations

import argparse
import json
import math
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import n31_brute as nb  # noqa: E402
import n31_exact as nx  # noqa: E402
import n31_geometry as ng  # noqa: E402

P_BITS = 64  # densities are rounded down to multiples of 2^-64
DMAX = 40  # most bisections per axis
GRID0 = 10**17 * 2**20  # the domain's upper end is rounded up onto this grid
FLOAT_MARGIN = 1e-10  # the float pass accepts a cell at 1 + this
EXACT_RETRY_DEPTH = 8  # extra exact bisections of a leaf the exact pass refuses
BUCKET = Fraction(1, 4)  # bucket side of the exact index, in units


def cpu() -> float:
    return time.process_time()


class Direction:
    """Exact and float data of one direction of the net."""

    def __init__(self, cand: dict, merged: dict, j: int, mass_scale: Fraction):
        self.j = j
        side, core, step = cand["L"], cand["B"], cand["step"]
        self.side, self.core, self.step = side, core, step
        if j == 0:
            self.C, self.S, self.E = 1, 0, 1
        else:
            self.C, self.S, self.E = nx.direction(j, step)
        assert self.C * self.C + self.S * self.S == self.E * self.E
        self.cos = Fraction(self.C, self.E)
        self.sin = Fraction(self.S, self.E)
        self.E2 = self.E * self.E
        a_j = max(Fraction(0), j * step - step / 2)
        self.a_j = a_j
        self.r_j = nx.r_of(a_j)
        lo = side / 2
        hi_exact = side - self.r_j
        hi = Fraction(math.ceil(hi_exact * GRID0), GRID0)
        assert (lo * GRID0).denominator == 1
        self.dom_lo, self.dom_hi, self.dom_hi_exact = lo, hi, hi_exact
        self.G = GRID0 * 2 ** (DMAX + 1)
        g = self.G
        self.XL = int(lo * g)
        self.XU = int(hi * g)
        self.W = self.XU - self.XL
        assert self.W % 2 ** (DMAX + 1) == 0
        b_half = core / 2
        assert (b_half * g).denominator == 1
        self.b = int(b_half * g)
        self.Eb = self.E * self.b
        self.zarea = 2 * self.C * self.S * self.E2 if self.S else 1
        self.threshold = (1 << P_BITS) * self.zarea * g * g
        # Core half-extent along the axes, B/2 (cos + sin), rounded up, grid units.
        self.rx = -((-self.b * (self.C + self.S)) // self.E)
        # Rectangles.
        self.rects = []
        dens_exact = []
        for (x0, y0, x1, y1), d in merged.items():
            scaled = (x0 * g, y0 * g, x1 * g, y1 * g)
            if any(v.denominator != 1 for v in scaled):
                msg = "a rectangle coordinate is off the grid"
                raise ValueError(msg)
            self.rects.append(tuple(int(v) for v in scaled))
            dens_exact.append(d * mass_scale)
        self.dens_exact = dens_exact
        self.r = [math.floor(d * (1 << P_BITS)) for d in dens_exact]
        c_i, s_i = self.C, self.S
        self.corners = []
        self.rbox = []
        self.full = []
        for (x0, y0, x1, y1), ri in zip(self.rects, self.r, strict=True):
            cs = tuple((c_i * xx + s_i * yy, -s_i * xx + c_i * yy)
                       for xx, yy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)))
            self.corners.append(cs)
            ss = [p[0] for p in cs]
            ws = [p[1] for p in cs]
            self.rbox.append((min(ss), max(ss), min(ws), max(ws)))
            self.full.append(ri * self.zarea * (x1 - x0) * (y1 - y0))
        # Exact bucket index over the original frame.
        self.bucket = int(BUCKET * g)
        index: dict[tuple[int, int], list[int]] = {}
        for i, (x0, y0, x1, y1) in enumerate(self.rects):
            for bx in range(x0 // self.bucket, x1 // self.bucket + 1):
                for by in range(y0 // self.bucket, y1 // self.bucket + 1):
                    index.setdefault((bx, by), []).append(i)
        self.index = index
        self._cache: dict[tuple[int, int, int, int], list[int]] = {}
        self.least_point: tuple[float, tuple[int, int, int, int] | None] = (math.inf, None)
        # Float arrays (units).
        self.c = float(self.cos)
        self.s = float(self.sin)
        arr = np.array([[x0 / g, y0 / g, x1 / g, y1 / g] for x0, y0, x1, y1 in self.rects])
        self.fx0, self.fy0, self.fx1, self.fy1 = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]
        self.frho = np.array([float(d) for d in dens_exact])
        self.fmass = self.frho * (self.fx1 - self.fx0) * (self.fy1 - self.fy0)
        c, s = self.c, self.s
        self.fsig = np.stack([c * self.fx0 + s * self.fy0, c * self.fx1 + s * self.fy0,
                              c * self.fx0 + s * self.fy1, c * self.fx1 + s * self.fy1])
        self.fome = np.stack([-s * self.fx0 + c * self.fy0, -s * self.fx1 + c * self.fy0,
                              -s * self.fx0 + c * self.fy1, -s * self.fx1 + c * self.fy1])
        self.fsmin, self.fsmax = self.fsig.min(axis=0), self.fsig.max(axis=0)
        self.fwmin, self.fwmax = self.fome.min(axis=0), self.fome.max(axis=0)
        self.fb = float(b_half)
        self.fxl = float(lo)
        self.fw = self.W / g

    # ----------------------------------------------------------------- float pass

    def _h(self, a, b):
        c, s = self.c, self.s
        if self.S == 0:
            return np.where((a > 0) & (b > 0), a * b, 0.0)
        t1 = s * a + c * b
        t2 = c * a - s * b
        two_cs = 2.0 * c * s
        val_neg = t1 * t1 / two_cs
        val_full = a * a / two_cs
        val_mid = (s * a * a + 2.0 * c * a * b - s * b * b) / (2.0 * c)
        out = np.where(b <= 0, val_neg, np.where(t2 <= 0, val_full, val_mid))
        return np.where((a > 0) & (t1 > 0), out, 0.0)

    def _chord_sigma(self, t, wlo, whi, i):
        x0, x1, y0, y1 = self.fx0[i], self.fx1[i], self.fy0[i], self.fy1[i]
        c, s = self.c, self.s
        if self.S == 0:
            ok = (x0 <= t) & (t <= x1)
            return np.where(ok, np.maximum(0.0, np.minimum(y1, whi) - np.maximum(y0, wlo)),
                            0.0)
        lo = np.maximum(np.maximum((t * c - x1) / s, (y0 - t * s) / c), wlo)
        hi = np.minimum(np.minimum((t * c - x0) / s, (y1 - t * s) / c), whi)
        return np.maximum(0.0, hi - lo)

    def _chord_omega(self, t, slo, shi, i):
        x0, x1, y0, y1 = self.fx0[i], self.fx1[i], self.fy0[i], self.fy1[i]
        c, s = self.c, self.s
        if self.S == 0:
            ok = (y0 <= t) & (t <= y1)
            return np.where(ok, np.maximum(0.0, np.minimum(x1, shi) - np.maximum(x0, slo)),
                            0.0)
        lo = np.maximum(np.maximum((x0 + t * s) / c, (y0 - t * c) / s), slo)
        hi = np.minimum(np.minimum((x1 + t * s) / c, (y1 - t * c) / s), shi)
        return np.maximum(0.0, hi - lo)

    def float_batch(self, ax, dx, ay, dy, base, cand_ids, cand_off, *, point=False):
        """Float lower bounds for a batch of cells; returns (lb, inside_mass, keep_mask).

        With point=True the half-widths are zero: the value is then the float capture of
        the core at each cell's centre (base must then be the cell's inherited mass).
        """
        ncell = len(ax)
        wx = self.fw / np.exp2(dx)
        wy = self.fw / np.exp2(dy)
        px = self.fxl + (ax + 0.5) * wx
        py = self.fxl + (ay + 0.5) * wy
        hx, hy = 0.5 * wx, 0.5 * wy
        if point:
            hx, hy = 0.0 * hx, 0.0 * hy
        c, s, b = self.c, self.s, self.fb
        sig0 = c * px + s * py
        om0 = -s * px + c * py
        eu = hx * c + hy * s
        ev = hx * s + hy * c
        au = b - eu
        av = b - ev
        counts = np.diff(cand_off)
        k = np.repeat(np.arange(ncell), counts)
        i = cand_ids
        ksig, kom, keu, kev, kau, kav = sig0[k], om0[k], eu[k], ev[k], au[k], av[k]
        smin, smax, wmin, wmax = self.fsmin[i], self.fsmax[i], self.fwmin[i], self.fwmax[i]
        out = ((smax <= ksig - b - keu) | (smin >= ksig + b + keu)
               | (wmax <= kom - b - kev) | (wmin >= kom + b + kev))
        inside = ((smin >= ksig - kau) & (smax <= ksig + kau)
                  & (wmin >= kom - kav) & (wmax <= kom + kav))
        bnd = ~out & ~inside
        inside_mass = np.bincount(k[inside], weights=self.fmass[i[inside]],
                                  minlength=ncell)
        kb, ib = k[bnd], i[bnd]
        rho = self.frho[ib]
        slo, shi = sig0[kb] - au[kb], sig0[kb] + au[kb]
        wlo, whi = om0[kb] - av[kb], om0[kb] + av[kb]
        area = np.zeros(len(kb))
        signs = (1.0, -1.0, -1.0, 1.0)
        for q in range(4):
            sq, wq = self.fsig[q][ib], self.fome[q][ib]
            part = (self._h(shi - sq, whi - wq) - self._h(slo - sq, whi - wq)
                    - self._h(shi - sq, wlo - wq) + self._h(slo - sq, wlo - wq))
            area += signs[q] * part
        area_sum = np.bincount(kb, weights=rho * area, minlength=ncell)
        bb, beu, bev = self.fb, eu[kb], ev[kb]
        lpu = np.minimum(self._chord_sigma(shi, wlo, whi, ib),
                         self._chord_sigma(sig0[kb] + bb + beu, wlo, whi, ib))
        lmu = np.minimum(self._chord_sigma(slo, wlo, whi, ib),
                         self._chord_sigma(sig0[kb] - bb - beu, wlo, whi, ib))
        lpv = np.minimum(self._chord_omega(whi, slo, shi, ib),
                         self._chord_omega(om0[kb] + bb + bev, slo, shi, ib))
        lmv = np.minimum(self._chord_omega(wlo, slo, shi, ib),
                         self._chord_omega(om0[kb] - bb - bev, slo, shi, ib))
        spu = np.bincount(kb, weights=rho * lpu, minlength=ncell)
        smu = np.bincount(kb, weights=rho * lmu, minlength=ncell)
        spv = np.bincount(kb, weights=rho * lpv, minlength=ncell)
        smv = np.bincount(kb, weights=rho * lmv, minlength=ncell)
        lb = (base + inside_mass + area_sum + 2 * eu * np.minimum(spu, smu)
              + 2 * ev * np.minimum(spv, smv))
        lb = np.where((au > 0) & (av > 0), lb, -1.0)
        return lb, inside_mass, bnd

    def point_values(self, ax, dx, ay, dy, base, ids, off, sel):
        """Float captures at the centres of the cells sel of a batch."""
        seg_ids = [ids[off[t]:off[t + 1]] for t in sel]
        p_off = np.concatenate([[0], np.cumsum([len(sg) for sg in seg_ids])])
        cat = np.concatenate(seg_ids) if seg_ids else np.zeros(0, np.int64)
        pv, _, _ = self.float_batch(ax[sel], dx[sel], ay[sel], dy[sel], base[sel], cat,
                                    p_off.astype(np.int64), point=True)
        return pv

    def float_bnb(self, max_nodes: int, cpu_limit: float, start: float):
        """The float pass: returns (leaves, nodes, status, least float bound)."""
        leaves = []
        nodes = 0
        root = (np.zeros(1, np.int64), np.zeros(1, np.int64), np.zeros(1, np.int64),
                np.zeros(1, np.int64), np.zeros(1), np.arange(len(self.rects)),
                np.array([0, len(self.rects)]))
        stack = [root]
        max_pairs = 1_500_000
        status = "complete"
        least = math.inf
        failures = []
        while stack:
            if cpu() - start > cpu_limit or nodes > max_nodes:
                status = "budget"
                break
            ax, dx, ay, dy, base, ids, off = stack.pop()
            nodes += len(ax)
            lb, inside_mass, bnd = self.float_batch(ax, dx, ay, dy, base, ids, off)
            acc = lb >= 1.0 + FLOAT_MARGIN
            acc_idx = np.nonzero(acc)[0]
            for t in acc_idx:
                leaves.append((int(ax[t]), int(dx[t]), int(ay[t]), int(dy[t]), float(lb[t])))
                least = min(least, float(lb[t]))
            if len(acc_idx):
                # The float capture at each accepted leaf's centre: the least of these
                # names a pose whose exact capture bounds the true minimum from above.
                pv = self.point_values(ax, dx, ay, dy, base, ids, off, acc_idx)
                t = acc_idx[np.argmin(pv)]
                if pv.min() < self.least_point[0]:
                    self.least_point = (float(pv.min()),
                                        (int(ax[t]), int(dx[t]), int(ay[t]), int(dy[t])))
            split = np.nonzero(~acc)[0]
            if len(split) == 0:
                continue
            # The float capture at the centre of each refused cell past depth 8: a value
            # below one is a candidate counterexample, which ends the pass (the exact
            # pass then evaluates it).
            probe = split[(dx[split] + dy[split]) >= 8]
            if len(probe):
                pv = self.point_values(ax, dx, ay, dy, base, ids, off, probe)
                low = np.nonzero(pv < 1.0 - 1e-9)[0]
                if len(low):
                    t = probe[low[np.argmin(pv[low])]]
                    failures.append((int(ax[t]), int(dx[t]), int(ay[t]), int(dy[t]),
                                     float(pv.min())))
                    status = "counterexample"
                    break
            deep = (dx[split] >= DMAX) | (dy[split] >= DMAX)
            if deep.any():
                for t in split[deep]:
                    failures.append((int(ax[t]), int(dx[t]), int(ay[t]), int(dy[t]),
                                     float(lb[t])))
                split = split[~deep]
                if len(split) == 0:
                    continue
            # Children inherit the boundary candidates.
            counts = np.diff(off)
            k = np.repeat(np.arange(len(ax)), counts)
            kb, ib = k[bnd], ids[bnd]
            bcount = np.bincount(kb, minlength=len(ax))
            boff = np.concatenate([[0], np.cumsum(bcount)])
            along_x = dx[split] <= dy[split]
            cax, cdx, cay, cdy, cbase, cids, coff = [], [], [], [], [], [], [0]
            for t, ax_split in zip(split, along_x, strict=True):
                seg = ib[boff[t]:boff[t + 1]]
                nb_ = base[t] + inside_mass[t]
                if ax_split:
                    kids = ((2 * ax[t], dx[t] + 1, ay[t], dy[t]),
                            (2 * ax[t] + 1, dx[t] + 1, ay[t], dy[t]))
                else:
                    kids = ((ax[t], dx[t], 2 * ay[t], dy[t] + 1),
                            (ax[t], dx[t], 2 * ay[t] + 1, dy[t] + 1))
                for kid in kids:
                    cax.append(kid[0])
                    cdx.append(kid[1])
                    cay.append(kid[2])
                    cdy.append(kid[3])
                    cbase.append(nb_)
                    cids.append(seg)
                    coff.append(coff[-1] + len(seg))
            # Push in chunks bounded by pairs.
            start_k = 0
            nkid = len(cax)
            while start_k < nkid:
                end_k = start_k
                while end_k < nkid and (coff[end_k + 1] - coff[start_k] <= max_pairs
                                        or end_k == start_k):
                    end_k += 1
                sl = slice(start_k, end_k)
                ids_cat = (np.concatenate(cids[sl]) if end_k > start_k
                           else np.zeros(0, np.int64))
                off_cat = np.array(coff[start_k:end_k + 1]) - coff[start_k]
                stack.append((np.array(cax[sl], np.int64), np.array(cdx[sl], np.int64),
                              np.array(cay[sl], np.int64), np.array(cdy[sl], np.int64),
                              np.array(cbase[sl]), ids_cat, off_cat))
                start_k = end_k
        return leaves, nodes, status, least, failures

    # ----------------------------------------------------------------- exact pass

    def cell_int(self, ax, dx, ay, dy):
        wx = self.W >> dx
        wy = self.W >> dy
        x_lo = self.XL + ax * wx
        y_lo = self.XL + ay * wy
        return x_lo + wx // 2, y_lo + wy // 2, wx // 2, wy // 2

    def candidates(self, px, py, hx, hy):
        """Every rectangle whose box meets the box of all cores over the cell (a superset
        of those that meet any core): the buckets the query box touches, in a cache keyed
        by that bucket range, since consecutive leaves lie close together."""
        bk = self.bucket
        x_lo, x_hi = px - hx - self.rx, px + hx + self.rx
        y_lo, y_hi = py - hy - self.rx, py + hy + self.rx
        key = (x_lo // bk, x_hi // bk, y_lo // bk, y_hi // bk)
        hit = self._cache.get(key)
        if hit is not None:
            return hit
        seen = set()
        for bx in range(key[0], key[1] + 1):
            for by in range(key[2], key[3] + 1):
                seen.update(self.index.get((bx, by), ()))
        hit = sorted(seen)
        if len(self._cache) > 4096:
            self._cache.clear()
        self._cache[key] = hit
        return hit

    def exact_lb(self, px, py, hx, hy):
        """Exact scaled lower bound for every centre of the cell; None if no kernel."""
        c, s, e2 = self.C, self.S, self.E2
        sig0 = c * px + s * py
        om0 = -s * px + c * py
        eu = hx * c + hy * s
        ev = hx * s + hy * c
        eb = self.Eb
        au, av = eb - eu, eb - ev
        if au <= 0 or av <= 0:
            return None
        slo, shi, wlo, whi = sig0 - au, sig0 + au, om0 - av, om0 + av
        hslo, hshi, hwlo, hwhi = sig0 - eb - eu, sig0 + eb + eu, om0 - eb - ev, om0 + eb + ev
        t_pu, t_pu2 = shi, sig0 + eb + eu
        t_mu, t_mu2 = slo, sig0 - eb - eu
        t_pv, t_pv2 = whi, om0 + eb + ev
        t_mv, t_mv2 = wlo, om0 - eb - ev
        total = 0
        lpu = lmu = lpv = lmv = 0
        rbox, rects, rr, full, corners = self.rbox, self.rects, self.r, self.full, self.corners
        chs, cho = ng.chord_sigma, ng.chord_omega
        for i in self.candidates(px, py, hx, hy):
            smin, smax, wmin, wmax = rbox[i]
            if smax <= hslo or smin >= hshi or wmax <= hwlo or wmin >= hwhi:
                continue
            if smin >= slo and smax <= shi and wmin >= wlo and wmax <= whi:
                total += full[i]
                continue
            ri = rr[i]
            total += ri * ng.area16(corners[i], slo, shi, wlo, whi, c, s, e2)
            x0, y0, x1, y1 = rects[i]
            # A rectangle adds to a slab's least line density only if it meets both of
            # the slab's extreme lines; otherwise its smaller chord is zero, exactly.
            if wmax > wlo and wmin < whi:
                if smin <= t_pu and smax >= t_pu2:
                    lpu += ri * min(chs(t_pu, wlo, whi, x0, x1, y0, y1, c, s, e2),
                                    chs(t_pu2, wlo, whi, x0, x1, y0, y1, c, s, e2))
                if smin <= t_mu2 and smax >= t_mu:
                    lmu += ri * min(chs(t_mu, wlo, whi, x0, x1, y0, y1, c, s, e2),
                                    chs(t_mu2, wlo, whi, x0, x1, y0, y1, c, s, e2))
            if smax > slo and smin < shi:
                if wmin <= t_pv and wmax >= t_pv2:
                    lpv += ri * min(cho(t_pv, slo, shi, x0, x1, y0, y1, c, s, e2),
                                    cho(t_pv2, slo, shi, x0, x1, y0, y1, c, s, e2))
                if wmin <= t_mv2 and wmax >= t_mv:
                    lmv += ri * min(cho(t_mv, slo, shi, x0, x1, y0, y1, c, s, e2),
                                    cho(t_mv2, slo, shi, x0, x1, y0, y1, c, s, e2))
        if s:
            total += 4 * eu * min(lpu, lmu) + 4 * ev * min(lpv, lmv)
        else:
            total += 2 * hx * min(lpu, lmu) + 2 * hy * min(lpv, lmv)
        return total

    def exact_leaf(self, leaf, depth=0):
        """Decide one leaf exactly; split on failure. Returns (ok, paths, least)."""
        ax, dx, ay, dy = leaf
        px, py, hx, hy = self.cell_int(ax, dx, ay, dy)
        val = self.exact_lb(px, py, hx, hy)
        if val is not None and val >= self.threshold:
            return True, [leaf], Fraction(val, self.threshold)
        if depth >= EXACT_RETRY_DEPTH or dx >= DMAX or dy >= DMAX:
            return False, [leaf], (Fraction(val, self.threshold) if val is not None else None)
        paths, least, ok = [], None, True
        for kid in children(leaf):
            k_ok, k_paths, k_least = self.exact_leaf(kid, depth + 1)
            ok = ok and k_ok
            paths += k_paths
            if k_least is not None and (least is None or k_least < least):
                least = k_least
        return ok, paths, least

    def point_capture(self, px_units: Fraction, py_units: Fraction) -> Fraction:
        """Exact mu(Q(p)) with the unrounded densities, by the second method."""
        merged = {}
        g = self.G
        for (x0, y0, x1, y1), d in zip(self.rects, self.dens_exact, strict=True):
            merged[(Fraction(x0, g), Fraction(y0, g), Fraction(x1, g), Fraction(y1, g))] = d
        return nb.capture(merged, px_units, py_units, self.core, self.cos, self.sin)


def children(node):
    """The two halves of a cell under the one splitting rule both passes use."""
    ax, dx, ay, dy = node
    if dx <= dy:
        return (2 * ax, dx + 1, ay, dy), (2 * ax + 1, dx + 1, ay, dy)
    return (ax, dx, 2 * ay, dy + 1), (ax, dx, 2 * ay + 1, dy + 1)


def partition_holds(paths) -> bool:
    """The leaves are exactly the leaves of one bisection tree of the root.

    Walk the tree from the root under the splitting rule, stopping at a leaf. Every
    branch must end at a leaf (so the leaves cover the root), and every leaf must be
    reached exactly once (so none lies inside another, and none is repeated). The leaves
    then partition the quadrant, up to shared boundaries.
    """
    leafset = set(paths)
    if len(leafset) != len(paths):
        return False
    deepest = max(dx + dy for _, dx, _, dy in paths)
    reached = 0
    stack = [(0, 0, 0, 0)]
    while stack:
        node = stack.pop()
        if node in leafset:
            reached += 1
            continue
        if node[1] + node[3] >= deepest:
            return False
        stack.extend(children(node))
    return reached == len(leafset)


def run_direction(cand, merged, j, mass_scale, max_nodes, cpu_limit):
    start = cpu()
    d = Direction(cand, merged, j, mass_scale)
    setup = cpu() - start
    t0 = cpu()
    leaves, nodes, status, least_float, failures = d.float_bnb(max_nodes, cpu_limit, start)
    t_float = cpu() - t0
    rec = {
        "j": j, "C": d.C, "S": d.S, "E": d.E,
        "t_j": str(j * d.step), "a_j": str(d.a_j), "r_a_j": str(d.r_j),
        "domain_quadrant_exact": [str(d.dom_lo), str(d.dom_hi_exact)],
        "domain_quadrant_decided": [str(d.dom_lo), str(d.dom_hi)],
        "mass_scale": str(mass_scale),
        "float_nodes": nodes, "float_leaves": len(leaves), "float_status": status,
        "float_least_accepted_bound": least_float if leaves else None,
        "float_failures": len(failures),
        "cpu_setup": round(setup, 3), "cpu_float": round(t_float, 3),
    }
    if status != "complete" or failures:
        # Locate the worst cell and evaluate the exact capture at its centre.
        worst = None
        if failures:
            worst = min(failures, key=lambda f: f[4])
        rec["verdict"] = "UNDECIDED"
        if worst is not None:
            px, py, _hx, _hy = d.cell_int(*worst[:4])
            fx, fy = Fraction(px, d.G), Fraction(py, d.G)
            cap = d.point_capture(fx, fy)
            rec["worst_cell"] = list(worst[:4])
            rec["worst_cell_float_bound"] = worst[4]
            rec["worst_centre"] = [str(fx), str(fy)]
            rec["worst_centre_capture_exact"] = str(cap)
            rec["worst_centre_capture_float"] = float(cap)
            rec["worst_centre_in_exact_domain"] = bool(
                d.dom_lo <= fx <= d.dom_hi_exact and d.dom_lo <= fy <= d.dom_hi_exact)
            if cap < 1 and rec["worst_centre_in_exact_domain"]:
                rec["verdict"] = "REFUTED"
        rec["cpu_total"] = round(cpu() - start, 3)
        return rec
    t1 = cpu()
    all_paths = []
    exact_ok = True
    least_exact = None
    least_leaf = None
    retried = 0
    for leaf in leaves:
        ok, paths, least = d.exact_leaf(leaf[:4])
        if len(paths) > 1:
            retried += 1
        exact_ok = exact_ok and ok
        all_paths += paths
        if least is not None and (least_exact is None or least < least_exact):
            least_exact, least_leaf = least, leaf[:4]
        if cpu() - start > cpu_limit:
            exact_ok = False
            rec["exact_status"] = "budget"
            break
    t_exact = cpu() - t1
    rec["exact_leaves"] = len(all_paths)
    rec["exact_retried_leaves"] = retried
    rec["exact_least_bound"] = (f"{least_exact.numerator}/{least_exact.denominator}"
                                if least_exact is not None else None)
    rec["exact_least_bound_float"] = float(least_exact) if least_exact is not None else None
    rec["exact_least_leaf"] = list(least_leaf) if least_leaf else None
    t2 = cpu()
    part = partition_holds(all_paths) if exact_ok else False
    rec["partition_holds"] = part
    rec["cpu_partition"] = round(cpu() - t2, 3)
    rec["cpu_exact"] = round(t_exact, 3)
    rec["verdict"] = "VERIFIED" if exact_ok and part else "UNDECIDED"
    # The exact capture at the least certified leaf's centre, which must be at least the
    # leaf's bound, and at the leaf centre of least float capture: an upper bound on the
    # least capture over the domain, by the second method (n31_brute).
    if least_leaf is not None:
        px, py, _hx, _hy = d.cell_int(*least_leaf)
        fx, fy = Fraction(px, d.G), Fraction(py, d.G)
        cap = d.point_capture(fx, fy)
        rec["least_leaf_centre"] = [str(fx), str(fy)]
        rec["least_leaf_centre_capture_float"] = float(cap)
        rec["least_leaf_centre_capture_at_least_bound"] = bool(cap >= least_exact)
    if d.least_point[1] is not None:
        px, py, _hx, _hy = d.cell_int(*d.least_point[1])
        fx, fy = Fraction(px, d.G), Fraction(py, d.G)
        cap = d.point_capture(fx, fy)
        rec["least_capture_found_centre"] = [str(fx), str(fy)]
        rec["least_capture_found_float"] = float(cap)
        rec["least_capture_found_float_pass"] = d.least_point[0]
        rec["least_capture_found_at_least_one"] = bool(cap >= 1)
    rec["cpu_total"] = round(cpu() - start, 3)
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("outdir")
    ap.add_argument("j", type=int, nargs="+")
    ap.add_argument("--mass-scale", default="1")
    ap.add_argument("--tag", default="original")
    ap.add_argument("--max-nodes", type=int, default=3_000_000)
    ap.add_argument("--cpu-limit", type=float, default=1800.0)
    ap.add_argument("--drop-row", type=int, default=None,
                    help="a mutant: remove this listed row (0-based) before expanding")
    args = ap.parse_args()
    cand = nx.read_candidate(Path(args.candidate))
    rows = list(cand["rectangles"])
    if args.drop_row is not None:
        del rows[args.drop_row]
    merged = nx.expand(rows, cand["L"])
    scale = Fraction(args.mass_scale)
    out = Path(args.outdir)
    progs = {p.name: nx.sha256_file(p) for p in sorted(Path(__file__).parent.glob("n31_*.py"))}
    progs["capture.py"] = nx.sha256_file(Path(__file__))
    for j in args.j:
        rec = run_direction(cand, merged, j, scale, args.max_nodes, args.cpu_limit)
        rec["kind"] = "review-2026-10-23-n31-capture/v1"
        rec["candidate_sha256"] = cand["sha256"]
        rec["dropped_row"] = args.drop_row
        rec["programs_sha256"] = progs
        rec["max_rss_kb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        (out / f"capture-{args.tag}-{j:04d}.json").write_text(json.dumps(rec, indent=1) + "\n")
        print(args.tag, j, rec["verdict"], "float", rec["float_nodes"], rec["float_leaves"],
              "exact", rec.get("exact_leaves"), rec.get("exact_least_bound_float"),
              "cpu", rec["cpu_total"], flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
