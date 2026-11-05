"""Rigorous branch and bound for one oblique direction of #910's certificate.

Written for the think-xzxd review from the mathematics alone; it reads no checker's
source. It decides, for one net index r >= 1, whether

    F(p) = sum_k rho_k |R_k n Q(p)| >= 1  for every centre p in [L/2, U_r]^2,

with Q(p) the closed core of side B, centre p and angle theta_r (exact cosine c and sine
s), R_k and rho_k the expanded rectangles and densities, and U_r the per-bin bound of
lemma D. By lemma C1 (quarter turn) that quadrant stands for the whole per-bin domain.

Method (the proofs are in the README):

1. Boxes of centres C = [x0, x1] x [y0, y1] with binary64 endpoints, starting from a
   box that contains the quadrant (L/2 rounded down, U_r rounded up).
2. Each rectangle is inside every Q(p), p in C, outside every Q(p), or boundary. The
   tests use outward-rounded rectangles and a slack of 1e-9 against the decision.
3. F(p0) at the box centre is bounded below by the inside masses plus, for each
   boundary rectangle, a trapezoid sum of its vertical sections eta(a) at 14 nodes.
   eta(a) = min(y2, p_y + F1, p_y + F2) - max(y1, p_y + G1, p_y + G2) is concave in a,
   so the trapezoid of max(0, piece) underestimates the integral for any nodes; the
   nodes include every breakpoint, so the bound is nearly exact.
4. The gradient of F is continuous and dF/dx = sum_k rho_k (sigma_k(x1) - sigma_k(x2)),
   with sigma(a) the length of the rectangle's vertical edge at a inside Q(p); dF/dy the
   same with horizontal edges. Over C each edge length is enclosed: its lower end is
   the least of its four corner values (eta is concave in p), its upper end is the
   least over the nine piece-pairs of their greatest corner value. Where the active
   pieces and the sign are the same at all four corners (with margin), the edge length
   is affine on C, so a rectangle with both edges so is summed exactly through its
   corner values; the rest are summed as intervals, cut by |sigma(x1) - sigma(x2)| <=
   min(y2 - y1, (x2 - x1)/(sc)).
5. Mean value: F(p) >= F_lo(p0) - G_x d_x - G_y d_y on C, with G the enclosure's
   magnitude and d the half-widths. A box is accepted when this, less its error budget,
   is at least 1; otherwise it is split along the coordinate with the larger term.

Every binary64 quantity carries an explicit error bound (README, "Error budget"), and a
box is accepted only when its bound exceeds 1 by more than that budget.

Usage: bnb.py CERT_GZ R OUT_JSON [--mass-factor a/b] [--max-nodes N] [--region x0,x1,y0,y1]
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
from gmpy2 import mpq

from xzcommon import direction, expand, frac_str, load_certificate

U2 = 2.0**-52  # twice the unit roundoff of binary64
TAU = 1e-9  # slack against the decision in the inside/outside tests


def f_down(x: mpq) -> float:
    f = float(x)
    if mpq(f) > x:
        f = math.nextafter(f, -math.inf)
    return f


def f_up(x: mpq) -> float:
    f = float(x)
    if mpq(f) < x:
        f = math.nextafter(f, math.inf)
    return f


class Direction:
    def __init__(self, cert_path: Path, r: int, mass_factor: mpq, region: list[float] | None) -> None:
        cert = load_certificate(cert_path)
        if r < 1 or r > cert.last:
            raise ValueError("r must be a net index >= 1")
        self.cert = cert
        self.r = r
        dr = direction(cert, r)
        self.dr = dr
        dens = expand(cert, mass_factor)
        keys = list(dens)
        self.keys = keys
        self.exact_rho = [dens[k] for k in keys]
        # Inner (area lower bound), outer (classification) and nearest (gradient) floats.
        self.X1i = np.array([f_up(k[0]) for k in keys])
        self.Y1i = np.array([f_up(k[1]) for k in keys])
        self.X2i = np.array([f_down(k[2]) for k in keys])
        self.Y2i = np.array([f_down(k[3]) for k in keys])
        self.X1o = np.array([f_down(k[0]) for k in keys])
        self.Y1o = np.array([f_down(k[1]) for k in keys])
        self.X2o = np.array([f_up(k[2]) for k in keys])
        self.Y2o = np.array([f_up(k[3]) for k in keys])
        self.X1n = np.array([float(k[0]) for k in keys])
        self.Y1n = np.array([float(k[1]) for k in keys])
        self.X2n = np.array([float(k[2]) for k in keys])
        self.Y2n = np.array([float(k[3]) for k in keys])
        self.rho = np.array([float(dens[k]) for k in keys])
        self.mass = np.array([float(dens[k] * (k[2] - k[0]) * (k[3] - k[1])) for k in keys])
        assert np.all(self.X1i < self.X2i) and np.all(self.Y1i < self.Y2i)
        self.c = float(dr.c)
        self.s = float(dr.s)
        self.h = float(cert.B / 2)
        c, s = self.c, self.s
        mcs = min(c, s)
        # Error bound of one section value eta (or tau) at a binary64 node and pose,
        # for exact y1, y2 (README, "Error budget"), doubled for safety.
        self.E_eta = (64.0 + 256.0 / mcs) * U2
        # Plus the nearest-float rectangle coordinates (|x| < 10): Lipschitz 1/(sc) in
        # the edge's abscissa and 1 in each of its ends.
        self.E_sig = self.E_eta + 16.0 * U2 * (1.0 / (s * c) + 2.0) * 2.0
        self.lip_a = 1.0 / (s * c) * (1.0 + 1e-12)
        self.lo = f_down(cert.L / 2)
        self.hi = f_up(dr.U)
        if region is not None:
            self.root = region
        else:
            self.root = [self.lo, self.hi, self.lo, self.hi]

    # -- classification ------------------------------------------------------------
    def classify(self, px, py, dx, dy, k):
        c, s, h = self.c, self.s, self.h
        mx = (self.X1o[k] + self.X2o[k]) * 0.5
        my = (self.Y1o[k] + self.Y2o[k]) * 0.5
        wx = (self.X2o[k] - self.X1o[k]) * 0.5
        wy = (self.Y2o[k] - self.Y1o[k]) * 0.5
        DX = mx - px
        DY = my - py
        du = np.abs(c * DX + s * DY)
        dv = np.abs(-s * DX + c * DY)
        eu = c * wx + s * wy
        ev = s * wx + c * wy
        bu = c * dx + s * dy
        bv = s * dx + c * dy
        inside = (du + eu + bu <= h - TAU) & (dv + ev + bv <= h - TAU)
        ext = h * (c + s)
        outside = (
            (du >= eu + h + bu + TAU)
            | (dv >= ev + h + bv + TAU)
            | (np.abs(DX) >= wx + ext + dx + TAU)
            | (np.abs(DY) >= wy + ext + dy + TAU)
        )
        return inside, outside

    # -- area lower bound at the centre --------------------------------------------
    def area_lb(self, px, py, k):
        """Lower bound on |R_k n Q(p0)| and its error budget, per pair."""
        c, s, h = self.c, self.s, self.h
        xa, xb = self.X1i[k], self.X2i[k]
        ya, yb = self.Y1i[k], self.Y2i[k]
        n = len(k)
        nodes = np.empty((n, 14))
        nodes[:, 0] = xa
        nodes[:, 1] = xb
        nodes[:, 2] = px + h * (c - s)
        nodes[:, 3] = px + h * (c + s)
        nodes[:, 4] = px - h * (c + s)
        nodes[:, 5] = px + h * (s - c)
        col = 6
        for yy in (ya, yb):
            z = yy - py
            nodes[:, col] = px + (h - s * z) / c
            nodes[:, col + 1] = px + (c * z - h) / s
            nodes[:, col + 2] = px + (-h - s * z) / c
            nodes[:, col + 3] = px + (c * z + h) / s
            col += 4
        np.clip(nodes, xa[:, None], xb[:, None], out=nodes)
        nodes.sort(axis=1)
        xi = nodes - px[:, None]
        pyc = py[:, None]
        top = np.minimum(np.minimum(pyc + (h - c * xi) / s, pyc + (h + s * xi) / c), yb[:, None])
        bot = np.maximum(np.maximum(pyc + (-h - c * xi) / s, pyc + (s * xi - h) / c), ya[:, None])
        eta = top - bot
        tr = np.diff(nodes, axis=1) * ((eta[:, 1:] + eta[:, :-1]) * 0.5)
        T = np.sum(np.maximum(tr, 0.0), axis=1)
        width = xb - xa
        err = width * (self.E_eta + 64.0 * U2 * (yb - ya + 1.0)) + 32.0 * U2 * T
        return T, err

    # -- edge-length enclosures over the box ---------------------------------------
    def edge_enclosure(self, cx, cy, a, lo_end, hi_end, vertical: bool):
        """For edges at a (per pair) spanning [lo_end, hi_end], over the 4 corners.

        Returns (sigma at corners, sigma_lo, sigma_hi, stable) for vertical edges
        (sections in y) or horizontal edges (sections in x).
        """
        c, s, h = self.c, self.s, self.h
        if vertical:
            xi = a[:, None] - cx  # (n, 4)
            base = cy
            p1 = base + (h - c * xi) / s
            p2 = base + (h + s * xi) / c
            q1 = base + (-h - c * xi) / s
            q2 = base + (s * xi - h) / c
        else:
            ze = a[:, None] - cy
            base = cx
            p1 = base + (h - s * ze) / c
            p2 = base + (c * ze + h) / s
            q1 = base + (-h - s * ze) / c
            q2 = base + (c * ze - h) / s
        n = len(a)
        tops = np.empty((n, 4, 3))
        tops[:, :, 0] = hi_end[:, None]
        tops[:, :, 1] = p1
        tops[:, :, 2] = p2
        bots = np.empty((n, 4, 3))
        bots[:, :, 0] = lo_end[:, None]
        bots[:, :, 1] = q1
        bots[:, :, 2] = q2
        tmin = tops.min(axis=2)
        bmax = bots.max(axis=2)
        eta = tmin - bmax  # (n, 4)
        E = self.E_sig
        sig_lo = np.maximum(0.0, eta.min(axis=1) - E)
        diffs = tops[:, :, :, None] - bots[:, :, None, :]  # (n, 4, 3, 3)
        sig_hi = np.maximum(0.0, diffs.max(axis=1).reshape(n, 9).min(axis=1) + E)
        sig_hi = np.minimum(sig_hi, hi_end - lo_end + E)
        # Stability: same argmin top piece and argmax bottom piece at all corners, with a
        # gap of more than 2E to the runner-up at each corner, and one strict sign.
        targ = tops.argmin(axis=2)
        barg = bots.argmax(axis=2)
        tsort = np.sort(tops, axis=2)
        bsort = np.sort(bots, axis=2)
        tgap = (tsort[:, :, 1] - tsort[:, :, 0]).min(axis=1)
        bgap = (bsort[:, :, 2] - bsort[:, :, 1]).min(axis=1)
        same = (targ == targ[:, :1]).all(axis=1) & (barg == barg[:, :1]).all(axis=1)
        pos = (eta >= E).all(axis=1)
        neg = (eta <= -E).all(axis=1)
        stable = same & (tgap > 2 * E) & (bgap > 2 * E) & (pos | neg)
        sig_c = np.maximum(eta, 0.0)
        return sig_c, sig_lo, sig_hi, stable

    def grad_parts(self, x0, x1, y0, y1, k):
        """Per pair: x- and y-derivative enclosures, split into affine (corner values)
        and interval parts, each already multiplied by rho, with error budgets."""
        cx = np.stack([x0, x0, x1, x1], axis=1)
        cy = np.stack([y0, y1, y0, y1], axis=1)
        rho = self.rho[k]
        out = {}
        for name, vertical in (("x", True), ("y", False)):
            if vertical:
                a1, a2 = self.X1n[k], self.X2n[k]
                e1, e2 = self.Y1n[k], self.Y2n[k]
                span = self.X2n[k] - self.X1n[k]
            else:
                a1, a2 = self.Y1n[k], self.Y2n[k]
                e1, e2 = self.X1n[k], self.X2n[k]
                span = self.Y2n[k] - self.Y1n[k]
            s1c, s1lo, s1hi, st1 = self.edge_enclosure(cx, cy, a1, e1, e2, vertical)
            s2c, s2lo, s2hi, st2 = self.edge_enclosure(cx, cy, a2, e1, e2, vertical)
            stable = st1 & st2
            Dc = (s1c - s2c) * rho[:, None]  # (n, 4)
            cap = np.minimum(e2 - e1, span * self.lip_a) + 2 * self.E_sig
            lo = np.maximum(s1lo - s2hi, -cap) * rho
            hi = np.minimum(s1hi - s2lo, cap) * rho
            err = 2.0 * self.E_sig * rho * (1.0 + 1e-9) + 8.0 * U2 * rho * (e2 - e1 + 1.0)
            out[name] = (stable, Dc, lo, hi, err)
        return out


def run(dirn: Direction, max_nodes: int, batch_pairs: int, log_every: float, threshold: float = 1.0) -> dict[str, object]:
    t0 = time.process_time()
    nrect = len(dirn.keys)
    x0r, x1r, y0r, y1r = dirn.root
    # A stack of batches; each batch: box bounds, inside mass, depth, CSR candidates.
    stack: list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = [
        (
            np.array([[x0r, x1r, y0r, y1r]]),
            np.zeros(1),
            np.zeros(1, dtype=np.int64),
            np.array([0, nrect], dtype=np.int64),
            np.arange(nrect, dtype=np.int64),
        )
    ]
    nodes = 0
    leaves = 0
    least_bound = math.inf
    least_box: list[float] | None = None
    lowest_est = math.inf
    lowest_est_at: tuple[float, float] | None = None
    max_depth = 0
    status = "verified"
    stop_reason = None
    sum_boundary = 0
    last_log = time.time()
    worst_err = 0.0
    while stack:
        boxes, inside, depth, off, cand = stack.pop()
        nb = len(boxes)
        nodes += nb
        x0, x1, y0, y1 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
        px = x0 + (x1 - x0) * 0.5
        py = y0 + (y1 - y0) * 0.5
        dx = np.nextafter(np.maximum(x1 - px, px - x0), np.inf)
        dy = np.nextafter(np.maximum(y1 - py, py - y0), np.inf)
        counts = np.diff(off)
        bid = np.repeat(np.arange(nb), counts)
        ins, outs = dirn.classify(px[bid], py[bid], dx[bid], dy[bid], cand)
        inside = inside + np.bincount(bid, weights=np.where(ins, dirn.mass[cand], 0.0), minlength=nb)
        keep = ~(ins | outs)
        bid = bid[keep]
        kk = cand[keep]
        sum_boundary += len(kk)
        T, Terr = dirn.area_lb(px[bid], py[bid], kk)
        rho = dirn.rho[kk]
        contrib = np.maximum(T - Terr, 0.0) * rho
        Flo = inside + np.bincount(bid, weights=contrib, minlength=nb)
        Fest = inside + np.bincount(bid, weights=T * rho, minlength=nb)
        gp = dirn.grad_parts(x0[bid], x1[bid], y0[bid], y1[bid], kk)
        G = {}
        Gerr = np.zeros(nb)
        for name in ("x", "y"):
            stable, Dc, lo, hi, err = gp[name]
            Sc = np.zeros((nb, 4))
            for j in range(4):
                Sc[:, j] = np.bincount(bid, weights=np.where(stable, Dc[:, j], 0.0), minlength=nb)
            ilo = np.bincount(bid, weights=np.where(stable, 0.0, lo), minlength=nb)
            ihi = np.bincount(bid, weights=np.where(stable, 0.0, hi), minlength=nb)
            e = np.bincount(bid, weights=err, minlength=nb)
            glo = Sc.min(axis=1) + ilo - e
            ghi = Sc.max(axis=1) + ihi + e
            G[name] = np.maximum(np.abs(glo), np.abs(ghi))
            Gerr += e
        # Error budget of the centre bound: inside sum, rho rounding, sums (README).
        npairs = np.bincount(bid, minlength=nb)
        Eb = 1e-9 + 64.0 * U2 * (Flo + 1.0) * (npairs + 10) + np.bincount(bid, weights=Terr * rho, minlength=nb) * 0.0
        loss = G["x"] * dx + G["y"] * dy
        bound = Flo - loss - Eb - 8.0 * U2 * (Flo + loss)
        worst_err = max(worst_err, float(np.max(Eb + 8.0 * U2 * (Flo + loss))))
        acc = bound >= threshold
        leaves += int(acc.sum())
        if acc.any():
            ia = np.nonzero(acc)[0]
            j = ia[np.argmin(bound[ia])]
            if bound[j] < least_bound:
                least_bound = float(bound[j])
                least_box = [float(x0[j]), float(x1[j]), float(y0[j]), float(y1[j])]
        jj = int(np.argmin(Fest))
        if Fest[jj] < lowest_est:
            lowest_est = float(Fest[jj])
            lowest_est_at = (float(px[jj]), float(py[jj]))
        max_depth = max(max_depth, int(depth.max()))
        rej = np.nonzero(~acc)[0]
        if len(rej) == 0:
            continue
        cex = rej[Fest[rej] < threshold - 1e-7]
        if len(cex):
            j = cex[np.argmin(Fest[cex])]
            status = "counterexample-candidate"
            stop_reason = {"centre": [float(px[j]), float(py[j])], "estimate": float(Fest[j])}
            break
        if nodes > max_nodes:
            status = "unresolved"
            stop_reason = {"node_limit": max_nodes}
            break
        # Split each rejected box along the coordinate with the larger loss term.
        bx = boxes[rej]
        splitx = (G["x"][rej] * dx[rej]) >= (G["y"][rej] * dy[rej])
        mx = bx[:, 0] + (bx[:, 1] - bx[:, 0]) * 0.5
        my = bx[:, 2] + (bx[:, 3] - bx[:, 2]) * 0.5
        degenerate = np.where(splitx, (mx <= bx[:, 0]) | (mx >= bx[:, 1]), (my <= bx[:, 2]) | (my >= bx[:, 3]))
        if degenerate.any():
            status = "unresolved"
            stop_reason = {"degenerate_box": bx[np.argmax(degenerate)].tolist()}
            break
        ch1 = bx.copy()
        ch2 = bx.copy()
        ch1[:, 1] = np.where(splitx, mx, bx[:, 1])
        ch2[:, 0] = np.where(splitx, mx, bx[:, 0])
        ch1[:, 3] = np.where(splitx, bx[:, 3], my)
        ch2[:, 2] = np.where(splitx, bx[:, 2], my)
        # Children's candidates: the parent's boundary rectangles.
        newcounts = np.bincount(bid, minlength=nb)
        order = np.argsort(bid, kind="stable")
        kk_sorted = kk[order]
        poff = np.concatenate([[0], np.cumsum(newcounts)])
        rc = newcounts[rej]
        # Build CSR for children interleaved: child1 of each rejected box, then child2.
        idx_lists = [kk_sorted[poff[i]:poff[i + 1]] for i in rej]
        children = np.concatenate([ch1, ch2])
        cins = np.concatenate([inside[rej], inside[rej]])
        cdep = np.concatenate([depth[rej] + 1, depth[rej] + 1])
        ccounts = np.concatenate([rc, rc])
        ccand = np.concatenate(idx_lists + idx_lists) if idx_lists else np.zeros(0, dtype=np.int64)
        coff = np.concatenate([[0], np.cumsum(ccounts)])
        # Push in chunks of at most batch_pairs candidates.
        start = 0
        nc = len(children)
        while start < nc:
            end = start + 1
            while end < nc and coff[end + 1] - coff[start] <= batch_pairs:
                end += 1
            sl = slice(start, end)
            stack.append(
                (
                    children[sl],
                    cins[sl],
                    cdep[sl],
                    coff[start:end + 1] - coff[start],
                    ccand[coff[start]:coff[end]],
                )
            )
            start = end
        if time.time() - last_log > log_every:
            last_log = time.time()
            print(
                f"  r={dirn.r} nodes {nodes} leaves {leaves} stack {len(stack)} least {least_bound:.12f} "
                f"lowest-estimate {lowest_est:.9f} cpu {time.process_time() - t0:.0f}s",
                flush=True,
            )
    rep: dict[str, object] = {
        "r": dirn.r,
        "theta_half_tangent": frac_str(dirn.dr.t),
        "U_r": frac_str(dirn.dr.U),
        "searched_box": dirn.root,
        "status": status,
        "stop": stop_reason,
        "nodes": nodes,
        "leaves": leaves,
        "max_depth": max_depth,
        "mean_boundary_rectangles": sum_boundary / max(nodes, 1),
        "threshold": threshold,
        "least_certified_bound": least_bound,
        "least_bound_box": least_box,
        "lowest_centre_estimate": lowest_est,
        "lowest_centre_estimate_at": lowest_est_at,
        "largest_error_budget": worst_err,
        "E_eta": dirn.E_eta,
        "cpu_seconds": time.process_time() - t0,
    }
    return rep


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("r", type=int)
    ap.add_argument("out")
    ap.add_argument("--mass-factor", default="1")
    ap.add_argument("--max-nodes", type=int, default=20_000_000)
    ap.add_argument("--batch-pairs", type=int, default=150_000)
    ap.add_argument("--region", default=None)
    ap.add_argument("--log-every", type=float, default=30.0)
    ap.add_argument("--threshold", default="1")
    a = ap.parse_args()
    region = [float(v) for v in a.region.split(",")] if a.region else None
    dirn = Direction(Path(a.cert), a.r, mpq(a.mass_factor), region)
    thr = mpq(a.threshold)
    if thr < 1:
        raise SystemExit('threshold below 1 proves nothing')
    thr_f = f_up(thr)
    rep = run(dirn, a.max_nodes, a.batch_pairs, a.log_every, thr_f)
    rep["threshold_exact"] = a.threshold
    rep["mass_factor"] = a.mass_factor
    for k, v in rep.items():
        print(f"{k}: {v}")
    Path(a.out).write_text(json.dumps(rep, indent=1) + "\n")
    return 0 if rep["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
