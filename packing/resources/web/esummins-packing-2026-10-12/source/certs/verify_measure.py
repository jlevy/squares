#!/usr/bin/env python3
"""
verify_measure.py -- exact-arithmetic verifier for MEASURE certificates (lower bounds for the
square-packing problem).  Written independently of the LP code that produces the certificates
(attempt A08-measure-verify); shares no code with attempts/A07-lp-dual or certs/verify_unavoidable.py.

CLAIM CERTIFIED
    Let mu = sum_i w_i * delta_{p_i} be a finite non-negative atomic measure on [0,s]^2 with
    total mass  M = sum_i w_i  <  n  (n = 11 by default; field "n" of the certificate).
    If every CLOSED unit square Q contained in the closed square [0,s]^2 (any orientation)
    satisfies mu(Q) >= 1, then no n pairwise-disjoint closed unit squares fit in [0,s]^2, and
    therefore s(n) >= s.   (Proof: if n unit squares with disjoint interiors fit in side s' < s,
    scale by s/s' > 1 and shrink each square about its centre back to a unit square; the n
    closed unit squares are now pairwise disjoint inside [0,s]^2, so mu([0,s]^2) >= n > M,
    contradiction.  Hence s(n) >= s.)

    The verifier decides the hypothesis "mu(Q) >= 1 for every closed unit square Q in [0,s]^2"
    by exact integer/rational interval branch-and-bound; the two-line argument above and the
    symmetry remark below are the only mathematics taken on trust.

PARAMETRISATION
    Q(c, theta) = closed unit square with centre c = (cx, cy) and edge direction theta.
    Q(c, theta) = Q(c, theta + pi/2), so theta in [0, pi/2] suffices.  Put t = tan(theta/2) in
    [0, 1]:  cos theta = (1 - t^2)/(1 + t^2)  (decreasing on [0,1]),
             sin theta = 2t/(1 + t^2)         (increasing on [0,1]),
    so for a rational t-interval [t0, t1] the enclosures  C = [cos(t1), cos(t0)]  and
    S = [sin(t0), sin(t1)]  are exact rationals.  All decisions are exact (Python ints /
    fractions.Fraction); floating point (numpy) is used ONLY to shortlist atoms and to choose
    sample placements -- every accept decision is re-derived exactly.

    p is inside Q(c, theta)  <=>  |u| <= 1/2 and |v| <= 1/2   where
        u =  cos*(px-cx) + sin*(py-cy),    v = -sin*(px-cx) + cos*(py-cy).
    Q(c, theta) is inside [0,s]^2  <=>  w/2 <= cx <= s - w/2 and w/2 <= cy <= s - w/2,
        w = cos theta + sin theta  (>= 1, unimodal in t: min over an interval at an endpoint).

BRANCH AND BOUND over boxes B = [t0,t1] x [x0,x1] x [y0,y1]  (root: [0,1] x [1/2, s-1/2]^2;
    every admissible centre lies there because w >= 1).  A box is DISCHARGED if
      (a) VACUOUS: no admissible placement in B.  The centre ranges are first CLIPPED to
          [wmin/2, s - wmin/2] with wmin = min(w(t0), w(t1)) <= w(t) on [t0,t1] (rounded outward to
          the integer grid); an empty clipped box is vacuous, otherwise the clipped box (which still
          contains every admissible placement of B) is used for (b) and for splitting;
      (b) COVERED: sum{ w_i : p_i inside Q(c,theta) for EVERY (t,c) in B } >= 1 + margin,
          the inclusion being decided by exact interval arithmetic on u, v.
    Otherwise it is bisected along its widest side (t-width scaled by --tscale) and the two halves
    are examined (children inherit the atoms already certified for the parent); boxes reaching
    --depth bisections undischarged are FAIL witnesses.

    LIMITATION (inherent to boxes): a placement where an atom lies EXACTLY on the boundary of Q
    and is needed for mass >= 1 can never be certified (e.g. Goebel's point (1,1) for the corner
    square [0,1]^2).  Certificates must be robust: every placement must reach mass 1 using atoms
    at positive distance from the boundary of Q.  Such witnesses are reported as "tight".

INTEGER ARITHMETIC
    Lengths are scaled by D = den(s) * 2^(depth+2) (so all bisection points are integers), t by
    2^K with K = depth+1; for T = t*2^K:  cos = (4^K - T^2)/(4^K + T^2), sin = 2T*2^K/(4^K + T^2).
    Atoms keep their own denominator PD (px = PXn/PD, py = PYn/PD).  Every comparison is between
    integers (cross-multiplied); no gcds.  A Fraction reference implementation of the same
    predicates is kept for --selftest (random cross-checks).

USAGE
    python verify_measure.py cert.json [--depth D] [--strict-margin m] [--report [path]]
        [--jobs J] [--split k] [--max-witnesses K] [--max-witnesses-per-box k] [--tscale T]
        [--scale-weights r] [--no-float-prepass] [--witness-file path] [--n N] [--quiet]
    python verify_measure.py --selftest
    exit code 0 = PASS, 1 = FAIL, 2 = certificate malformed / total mass >= n.

CERTIFICATE FORMAT (JSON; all numbers are exact rationals written as strings, e.g. "19/5",
    "3.8", "0.4022988505747193" -- decimal strings are read EXACTLY as the rational they denote;
    JSON floats are rejected)
    {"s": "19/5",
     "n": 11,                                   optional, default 11
     "atoms":   [["x","y"], ...],
     "weights": ["w", ...],                     same length as atoms; all >= 0
     "total":   "...",                          optional; compared with sum(weights) (warning only)
     "symmetry": "D4",                          optional; if present every atom is expanded to
                                                its D4-orbit under the symmetries of [0,s]^2
                                                (distinct images only), each image getting the
                                                listed weight
     "provenance": {...}}                       ignored
    Also accepted: "atoms": [{"x":..,"y":..,"w":..}, ...] (weights inline).
"""
import sys
import os
import json
import time
import math
import argparse
from fractions import Fraction as F

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None

HALF = F(1, 2)
ONE = F(1)
ZERO = F(0)


# ============================================================================= exact core (ints)
# This block (plus the driver's bisection rule) is what a Lean port needs.

def imul4(a0, a1, b0, b1):
    """interval product [a0,a1]*[b0,b1] for integers (or Fractions)."""
    p1 = a0 * b0
    p2 = a0 * b1
    p3 = a1 * b0
    p4 = a1 * b1
    return min(p1, p2, p3, p4), max(p1, p2, p3, p4)


def trig_int(T, K):
    """(cn, sn, dn) with cos theta = cn/dn, sin theta = sn/dn for t = T/2^K in [0,1]."""
    TT = T * T
    P = 1 << (2 * K)             # 4^K
    return P - TT, (T << (K + 1)), P + TT


def box_trig(T0, T1, K):
    """cos/sin enclosure of the t-interval [T0,T1]/2^K brought to a common denominator E:
    returns (Clo, Chi, Slo, Shi, E) with cos in [Clo,Chi]/E, sin in [Slo,Shi]/E  (all >= 0)."""
    cn0, sn0, dn0 = trig_int(T0, K)
    cn1, sn1, dn1 = trig_int(T1, K)
    E = dn0 * dn1
    return cn1 * dn0, cn0 * dn1, sn0 * dn1, sn1 * dn0, E     # cos decreasing, sin increasing in t


def atom_inside_int(PXn, PYn, PD, D, Clo, Chi, Slo, Shi, E, X0, X1, Y0, Y1):
    """True iff atom (PXn/PD, PYn/PD) lies in Q(c,theta) for EVERY cx in [X0,X1]/D, cy in [Y0,Y1]/D,
    cos in [Clo,Chi]/E, sin in [Slo,Shi]/E  (sound: interval arithmetic over-approximates u, v)."""
    dxlo = PXn * D - X1 * PD          # (px - cx) * PD * D
    dxhi = PXn * D - X0 * PD
    dylo = PYn * D - Y1 * PD
    dyhi = PYn * D - Y0 * PD
    lim = E * PD * D                  # 1/2 in these units is lim/2, i.e. compare 2*u with lim
    a0, a1 = imul4(Clo, Chi, dxlo, dxhi)
    b0, b1 = imul4(Slo, Shi, dylo, dyhi)
    if 2 * (a1 + b1) > lim or 2 * (a0 + b0) < -lim:      # u = C*dx + S*dy
        return False
    a0, a1 = imul4(-Shi, -Slo, dxlo, dxhi)
    b0, b1 = imul4(Clo, Chi, dylo, dyhi)
    if 2 * (a1 + b1) > lim or 2 * (a0 + b0) < -lim:      # v = -S*dx + C*dy
        return False
    return True


def vacuous_int(SD, D, K, T0, T1, X0, X1, Y0, Y1):
    """True iff certainly no admissible placement (Q inside [0,s]^2, s = SD/D) has (t,c) in the box.
    Uses w >= wmin = min(w(t0), w(t1)) on [t0,t1]: the box is vacuous if x1 < w/2 for BOTH endpoint
    values (then x1 < wmin/2), etc."""
    cn0, sn0, dn0 = trig_int(T0, K)
    cn1, sn1, dn1 = trig_int(T1, K)
    w0 = (cn0 + sn0) * D             # w(t0) * dn0 * D
    w1 = (cn1 + sn1) * D
    # x1 < w/2  <=>  2*X1*dn < w*D  ;  x0 > s - w/2  <=>  2*X0*dn > 2*SD*dn - w*D
    if 2 * X1 * dn0 < w0 and 2 * X1 * dn1 < w1:
        return True
    if 2 * Y1 * dn0 < w0 and 2 * Y1 * dn1 < w1:
        return True
    if 2 * X0 * dn0 > 2 * SD * dn0 - w0 and 2 * X0 * dn1 > 2 * SD * dn1 - w1:
        return True
    if 2 * Y0 * dn0 > 2 * SD * dn0 - w0 and 2 * Y0 * dn1 > 2 * SD * dn1 - w1:
        return True
    return False


def clip_int(SD, D, K, T0, T1, X0, X1, Y0, Y1):
    """Clip the centre ranges of the box to the admissible region wLo/2 <= c <= s - wLo/2, where
    wLo = min(w(t0), w(t1)) <= w(t) on the box (w = cos+sin is unimodal in t).  The bounds are
    rounded OUTWARD to the integer grid (floor / ceil), so the clipped box still contains every
    admissible placement of the original box.  Returns None if the box is vacuous."""
    cn0, sn0, dn0 = trig_int(T0, K)
    cn1, sn1, dn1 = trig_int(T1, K)
    wn0, wn1 = cn0 + sn0, cn1 + sn1
    if wn0 * dn1 <= wn1 * dn0:            # w(t0) <= w(t1)
        wn, wd = wn0, dn0
    else:
        wn, wd = wn1, dn1
    lo = (wn * D) // (2 * wd)                       # floor(wLo/2 * D)
    hi = -((-(2 * SD * wd - wn * D)) // (2 * wd))   # ceil((s - wLo/2) * D)
    X0c = X0 if X0 > lo else lo
    X1c = X1 if X1 < hi else hi
    Y0c = Y0 if Y0 > lo else lo
    Y1c = Y1 if Y1 < hi else hi
    if X0c > X1c or Y0c > Y1c:
        return None
    return X0c, X1c, Y0c, Y1c


# ============================================================================= reference (Fractions)
def cos_sin_t(t):
    tt = t * t
    return (1 - tt) / (1 + tt), 2 * t / (1 + tt)


def atom_inside_frac(px, py, t0, t1, x0, x1, y0, y1):
    C1, S0 = cos_sin_t(t0)
    C0, S1 = cos_sin_t(t1)
    dx0, dx1 = px - x1, px - x0
    dy0, dy1 = py - y1, py - y0
    a0, a1 = imul4(C0, C1, dx0, dx1)
    b0, b1 = imul4(S0, S1, dy0, dy1)
    if a1 + b1 > HALF or a0 + b0 < -HALF:
        return False
    a0, a1 = imul4(-S1, -S0, dx0, dx1)
    b0, b1 = imul4(C0, C1, dy0, dy1)
    if a1 + b1 > HALF or a0 + b0 < -HALF:
        return False
    return True


def vacuous_frac(s, t0, t1, x0, x1, y0, y1):
    c0, s0 = cos_sin_t(t0)
    c1, s1 = cos_sin_t(t1)
    h = min(c0 + s0, c1 + s1) / 2
    return x1 < h or x0 > s - h or y1 < h or y0 > s - h


def mass_at_frac(atoms, weights, t, cx, cy, idx=None):
    """exact mu(Q(c,theta(t))) (closed square) at a rational placement."""
    c, sn = cos_sin_t(t)
    acc = ZERO
    for i in (range(len(atoms)) if idx is None else idx):
        px, py = atoms[i]
        dx, dy = px - cx, py - cy
        u = c * dx + sn * dy
        if u > HALF or u < -HALF:
            continue
        v = -sn * dx + c * dy
        if v > HALF or v < -HALF:
            continue
        acc += weights[i]
    return acc


# ============================================================================= float helpers
def f_mass_mask(PX, PY, t, cx, cy, tol):
    c = (1 - t * t) / (1 + t * t)
    sn = 2 * t / (1 + t * t)
    dx = PX - cx
    dy = PY - cy
    u = c * dx + sn * dy
    v = -sn * dx + c * dy
    return (np.abs(u) <= 0.5 + tol) & (np.abs(v) <= 0.5 + tol)


# ============================================================================= the search
class Verifier:
    def __init__(self, s, atoms, weights, margin=ZERO, depth=48, tscale=2, use_float=True,
                 max_witnesses=200, verbose=True, progress_every=200000):
        self.s = s
        self.margin = margin
        self.need = ONE + margin
        self.depth = depth
        self.tscale = F(tscale)
        if self.tscale.denominator == 1:
            self.tscale = int(self.tscale)      # keep the split-rule comparison in pure ints
        self.max_witnesses = max_witnesses
        self.verbose = verbose
        self.progress_every = progress_every
        # heavy atoms first: early exit of the exact loop
        order = sorted(range(len(atoms)), key=lambda i: -weights[i])
        self.atoms = [atoms[i] for i in order]
        self.weights = [weights[i] for i in order]
        # ---- integer scaling
        self.K = depth + 1
        self.D = s.denominator << (depth + 2)
        self.SD = s.numerator << (depth + 2)
        self.T_ROOT = 1 << self.K
        self.PX = [];  self.PY = [];  self.PD = []
        for (px, py) in self.atoms:
            pd = px.denominator * py.denominator // math.gcd(px.denominator, py.denominator)
            self.PX.append(px.numerator * (pd // px.denominator))
            self.PY.append(py.numerator * (pd // py.denominator))
            self.PD.append(pd)
        # weights as integers over a common denominator WD
        WD = 1
        for w in self.weights:
            WD = WD * w.denominator // math.gcd(WD, w.denominator)
        self.WD = WD
        self.WI = [w.numerator * (WD // w.denominator) for w in self.weights]
        self.NEED = self.need.numerator * WD // self.need.denominator + (1 if (self.need.numerator * WD) % self.need.denominator else 0)
        # NEED = ceil(need * WD): integer mass >= NEED  <=>  mass >= need   (mass is a multiple of 1/WD)
        # ---- floats (shortlist only)
        self.use_float = use_float and np is not None and len(atoms) > 0
        if np is not None:
            self.fPX = np.array([float(p[0]) for p in self.atoms])
            self.fPY = np.array([float(p[1]) for p in self.atoms])
            self.fW = np.array([float(w) for w in self.weights])
        self.fneed = float(self.need) - 1e-9
        self.reset_stats()

    def reset_stats(self):
        self.n_boxes = 0
        self.n_vac = 0
        self.n_cov = 0
        self.n_split = 0
        self.n_exact = 0
        self.n_float_reject = 0
        self.hist_cov = {}
        self.witnesses = []
        self.max_depth_seen = 0

    # -- conversions
    def t_of(self, T):
        return F(T, self.T_ROOT)

    def x_of(self, X):
        return F(X, self.D)

    def root_boxes(self, k):
        """the root [0,1] x [1/2, s-1/2]^2 split into 4^k boxes (k bisections in cx and in cy)."""
        lo = self.D >> 1
        hi = self.SD - lo
        m = 1 << k
        step = (hi - lo) >> k
        assert step << k == hi - lo, "split too fine for the integer scale"
        out = []
        for i in range(m):
            for j in range(m):
                out.append((2 * k, 0, self.T_ROOT, lo + step * i, lo + step * (i + 1),
                            lo + step * j, lo + step * (j + 1), (), 0))
        return out

    # -- float shortlist: indices of atoms that MIGHT be inside for the whole box
    def float_candidates(self, ft0, ft1, fx0, fx1, fy0, fy1):
        eps = 1e-9
        # cos, sin >= 0 exactly on t in [0,1], so clamping the lower bounds at 0 keeps them valid
        C0 = max(0.0, (1 - ft1 * ft1) / (1 + ft1 * ft1) - eps)
        C1 = (1 - ft0 * ft0) / (1 + ft0 * ft0) + eps
        S0 = max(0.0, 2 * ft0 / (1 + ft0 * ft0) - eps)
        S1 = 2 * ft1 / (1 + ft1 * ft1) + eps
        dx0 = self.fPX - fx1
        dx1 = self.fPX - fx0
        dy0 = self.fPY - fy1
        dy1 = self.fPY - fy0
        # C, S >= 0 so the interval products are monotone in dx, dy
        a_hi = np.maximum(C0 * dx1, C1 * dx1)
        a_lo = np.minimum(C0 * dx0, C1 * dx0)
        b_hi = np.maximum(S0 * dy1, S1 * dy1)
        b_lo = np.minimum(S0 * dy0, S1 * dy0)
        ok = (a_hi + b_hi <= 0.5 + eps) & (a_lo + b_lo >= -0.5 - eps)
        # v = -S*dx + C*dy : -S in [-S1,-S0] <= 0
        a_hi = np.maximum(-S1 * dx0, -S0 * dx0)
        a_lo = np.minimum(-S1 * dx1, -S0 * dx1)
        b_hi = np.maximum(C0 * dy1, C1 * dy1)
        b_lo = np.minimum(C0 * dy0, C1 * dy0)
        ok &= (a_hi + b_hi <= 0.5 + eps) & (a_lo + b_lo >= -0.5 - eps)
        return np.nonzero(ok)[0]

    def covered(self, T0, T1, X0, X1, Y0, Y1, known, kmass):
        """Exact test: is the certified mass on the whole box >= need?
        known: tuple of atom indices already certified inside for a parent box, kmass their mass.
        Returns (True, None, None) if covered, else (False, known', kmass') with the enlarged set."""
        if self.use_float:
            r = self.T_ROOT
            D = self.D
            cand = self.float_candidates(T0 / r, T1 / r, X0 / D, X1 / D, Y0 / D, Y1 / D)
            idx = cand.tolist()
            if self.fW[cand].sum() < self.fneed:      # even the optimistic float shortlist is too light:
                self.n_float_reject += 1              # the box will be split; still certify the candidates
                if len(idx) == len(known):            # exactly so that the children inherit them
                    return False, known, kmass
        else:
            idx = range(len(self.atoms))
        Clo, Chi, Slo, Shi, E = box_trig(T0, T1, self.K)
        D = self.D
        PX, PY, PD, WI = self.PX, self.PY, self.PD, self.WI
        acc = kmass
        new = list(known)
        kset = set(known)
        NEED = self.NEED
        for i in idx:
            if i in kset:
                continue
            self.n_exact += 1
            if atom_inside_int(PX[i], PY[i], PD[i], D, Clo, Chi, Slo, Shi, E, X0, X1, Y0, Y1):
                acc += WI[i]
                new.append(i)
                if acc >= NEED:
                    return True, None, None
        return False, tuple(new), acc

    def exact_mass_at(self, t, cx, cy):
        """exact mu(Q(c,theta(t))) at a rational placement (float pre-filter with slack, exact decision)."""
        if np is not None:
            mask = f_mass_mask(self.fPX, self.fPY, float(t), float(cx), float(cy), 1e-9)
            idx = np.nonzero(mask)[0].tolist()
        else:
            idx = None
        return mass_at_frac(self.atoms, self.weights, t, cx, cy, idx)

    def make_witness(self, d, T0, T1, X0, X1, Y0, Y1):
        t0, t1 = self.t_of(T0), self.t_of(T1)
        x0, x1, y0, y1 = self.x_of(X0), self.x_of(X1), self.x_of(Y0), self.x_of(Y1)
        s = self.s
        w = {"depth": d,
             "box": {"t": [str(t0), str(t1)], "cx": [str(x0), str(x1)], "cy": [str(y0), str(y1)]}}
        cands = []
        for tt in ((t0 + t1) / 2, t0, t1):
            c, sn = cos_sin_t(tt)
            h = (c + sn) / 2
            for fx in ((x0 + x1) / 2, x0, x1):
                if fx < h or fx > s - h:
                    continue
                for fy in ((y0 + y1) / 2, y0, y1):
                    if fy < h or fy > s - h:
                        continue
                    cands.append((tt, fx, fy))
            if tt != (t0 + t1) / 2 and cands:
                break                                   # centre-t samples found; enough
        if not cands:
            tt = (t0 + t1) / 2
            c, sn = cos_sin_t(tt)
            h = (c + sn) / 2
            fx = min(max((x0 + x1) / 2, h), s - h)
            fy = min(max((y0 + y1) / 2, h), s - h)
            if h <= fx <= s - h and h <= fy <= s - h:
                cands.append((tt, fx, fy))
        if not cands:
            w["placement"] = None
            w["kind"] = "undecided"
            return w
        best = None
        min_interior = None
        for (tt, fx, fy) in cands:
            m = self.exact_mass_at(tt, fx, fy)
            if best is None or m < best[0]:
                best = (m, tt, fx, fy)
            if np is not None:
                # mass of atoms at distance > 1e-9 from the boundary of Q (float): detects tangencies
                mi = float(self.fW[f_mass_mask(self.fPX, self.fPY, float(tt), float(fx), float(fy), -1e-9)].sum())
                if min_interior is None or mi < min_interior:
                    min_interior = mi
        m, tt, fx, fy = best
        w["placement"] = {"t": str(tt), "cx": str(fx), "cy": str(fy), "t_float": float(tt),
                          "theta_deg": math.degrees(2 * math.atan(float(tt))),
                          "cx_float": float(fx), "cy_float": float(fy)}
        w["exact_mass"] = str(m)
        w["float_mass"] = float(m)
        if m < self.need:
            w["kind"] = "hole"          # rigorous: this admissible placement has mass < 1 + margin
        elif min_interior is not None:
            w["float_mass_interior_min"] = min_interior
            # tight: at some sampled placement the mass drops below need once boundary atoms are excluded
            w["kind"] = "tight" if min_interior < float(self.need) - 1e-9 else "undecided"
        else:
            w["kind"] = "undecided"
        return w

    def run(self, boxes, per_box_cap=None):
        """boxes: iterable of (depth, T0,T1,X0,X1,Y0,Y1, known, kmass).  Returns True iff no witness.
        per_box_cap: stop exploring an initial box after that many witnesses (diversity of witnesses)."""
        SD, D, K = self.SD, self.D, self.K
        tscale = self.tscale
        need_stop = False
        tstart = time.time()
        for box in boxes:
            if need_stop:
                break
            stack = [box]
            nw0 = len(self.witnesses)
            while stack:
                d, T0, T1, X0, X1, Y0, Y1, known, kmass = stack.pop()
                self.n_boxes += 1
                if d > self.max_depth_seen:
                    self.max_depth_seen = d
                clipped = clip_int(SD, D, K, T0, T1, X0, X1, Y0, Y1)
                if clipped is None:
                    self.n_vac += 1
                    continue
                X0, X1, Y0, Y1 = clipped          # sound: contains all admissible placements of the box
                ok, known, kmass = self.covered(T0, T1, X0, X1, Y0, Y1, known, kmass)
                if ok:
                    self.n_cov += 1
                    self.hist_cov[d] = self.hist_cov.get(d, 0) + 1
                    continue
                if d >= self.depth:
                    self.witnesses.append(self.make_witness(d, T0, T1, X0, X1, Y0, Y1))
                    if len(self.witnesses) >= self.max_witnesses:
                        need_stop = True
                        break
                    if per_box_cap is not None and len(self.witnesses) - nw0 >= per_box_cap:
                        break
                    continue
                self.n_split += 1
                # widths on a common scale: t-width in units of 1/2^K * (D/2^K)... compare as rationals
                # wt = (T1-T0)/2^K * tscale ; wx = (X1-X0)/D   ->  compare wt*D vs wx*2^K
                wt = (T1 - T0) * tscale * D
                wx = (X1 - X0) * self.T_ROOT
                wy = (Y1 - Y0) * self.T_ROOT
                if wx >= wy and wx >= wt:
                    m = (X0 + X1) >> 1
                    stack.append((d + 1, T0, T1, m, X1, Y0, Y1, known, kmass))
                    stack.append((d + 1, T0, T1, X0, m, Y0, Y1, known, kmass))
                elif wy >= wt:
                    m = (Y0 + Y1) >> 1
                    stack.append((d + 1, T0, T1, X0, X1, m, Y1, known, kmass))
                    stack.append((d + 1, T0, T1, X0, X1, Y0, m, known, kmass))
                else:
                    m = (T0 + T1) >> 1
                    stack.append((d + 1, m, T1, X0, X1, Y0, Y1, known, kmass))
                    stack.append((d + 1, T0, m, X0, X1, Y0, Y1, known, kmass))
                if self.verbose and self.n_boxes % self.progress_every == 0:
                    print(f"  ... {self.n_boxes} boxes ({self.n_cov} covered, {self.n_vac} vacuous, "
                          f"{len(self.witnesses)} witnesses), stack {len(stack)}, {time.time()-tstart:.0f}s",
                          flush=True)
        self.stopped_early = need_stop
        return len(self.witnesses) == 0

    def stats(self):
        return {"boxes": self.n_boxes, "covered": self.n_cov, "vacuous": self.n_vac,
                "split": self.n_split, "exact_atom_checks": self.n_exact,
                "float_rejects": self.n_float_reject, "max_depth": self.max_depth_seen,
                "depth_hist_covered": dict(sorted(self.hist_cov.items())),
                "witnesses": len(self.witnesses)}


# ============================================================================= certificate I/O
def _rat(x):
    if isinstance(x, F):
        return x
    if isinstance(x, bool):
        raise ValueError("boolean is not a number")
    if isinstance(x, int):
        return F(x)
    if isinstance(x, float):
        raise ValueError(f"float {x!r} in certificate: numbers must be exact strings or ints")
    return F(str(x).strip())


def d4_images(x, y, s):
    return [(x, y), (s - x, y), (x, s - y), (s - x, s - y),
            (y, x), (s - y, x), (y, s - x), (s - y, s - x)]


def load_certificate(path, n_override=None):
    with open(path) as fh:
        d = json.load(fh)
    s = _rat(d["s"])
    n = int(n_override if n_override is not None else d.get("n", 11))
    raw_atoms = d["atoms"]
    atoms, weights = [], []
    if raw_atoms and isinstance(raw_atoms[0], dict):
        for a in raw_atoms:
            atoms.append((_rat(a["x"]), _rat(a["y"])))
            weights.append(_rat(a["w"]))
    else:
        ws = d["weights"]
        if len(ws) != len(raw_atoms):
            raise ValueError("atoms/weights length mismatch")
        for (x, y), w in zip(raw_atoms, ws):
            atoms.append((_rat(x), _rat(y)))
            weights.append(_rat(w))
    sym = d.get("symmetry")
    if sym:
        if str(sym).upper() != "D4":
            raise ValueError(f"unknown symmetry {sym!r}")
        ex_atoms, ex_w = [], []
        for (x, y), w in zip(atoms, weights):
            seen = []
            for q in d4_images(x, y, s):
                if q not in seen:
                    seen.append(q)
            for q in seen:
                ex_atoms.append(q)
                ex_w.append(w)
        atoms, weights = ex_atoms, ex_w
    for (x, y), w in zip(atoms, weights):
        if w < 0:
            raise ValueError("negative weight")
        if not (0 <= x <= s and 0 <= y <= s):
            raise ValueError(f"atom ({x},{y}) outside [0,s]^2")
    total = sum(weights, ZERO)
    if "total" in d and _rat(d["total"]) != total:
        print(f"WARNING: declared total {d['total']} != computed total {total} "
              f"(~{float(total):.12f}); using computed", file=sys.stderr)
    return d, s, n, atoms, weights, total


# ============================================================================= self test
def selftest(n_iter=3000, seed=1):
    """random cross-check of the integer predicates against the Fraction reference implementation"""
    import random
    rng = random.Random(seed)
    depth = 12
    bad = 0
    for it in range(n_iter):
        s = F(rng.randint(15, 45), 10) + F(rng.randint(0, 99), 1000)
        px = F(rng.randint(0, 1000), 1000) * s
        py = F(rng.randint(0, 997), 997) * s
        atoms = [(px, py)]
        v = Verifier(s, atoms, [ONE], depth=depth, use_float=False, verbose=False)
        K, D = v.K, v.D
        # random dyadic box
        a = rng.randint(0, v.T_ROOT - 1); b = rng.randint(a + 1, v.T_ROOT)
        T0, T1 = a, b
        lo, hi = D >> 1, v.SD - (D >> 1)
        X0 = rng.randint(lo, hi - 1); X1 = rng.randint(X0 + 1, hi)
        Y0 = rng.randint(lo, hi - 1); Y1 = rng.randint(Y0 + 1, hi)
        if rng.random() < 0.5:   # small boxes too
            X1 = min(hi, X0 + rng.randint(1, D // 50 + 1)); Y1 = min(hi, Y0 + rng.randint(1, D // 50 + 1))
            T1 = min(v.T_ROOT, T0 + rng.randint(1, v.T_ROOT // 30 + 1))
        Clo, Chi, Slo, Shi, E = box_trig(T0, T1, K)
        r1 = atom_inside_int(v.PX[0], v.PY[0], v.PD[0], D, Clo, Chi, Slo, Shi, E, X0, X1, Y0, Y1)
        r2 = atom_inside_frac(px, py, F(T0, v.T_ROOT), F(T1, v.T_ROOT), F(X0, D), F(X1, D), F(Y0, D), F(Y1, D))
        v1 = vacuous_int(v.SD, D, K, T0, T1, X0, X1, Y0, Y1)
        v2 = vacuous_frac(s, F(T0, v.T_ROOT), F(T1, v.T_ROOT), F(X0, D), F(X1, D), F(Y0, D), F(Y1, D))
        cl = clip_int(v.SD, D, K, T0, T1, X0, X1, Y0, Y1)
        if (cl is None) != v1:
            # clip may declare vacuous slightly less often (outward rounding) but never more often
            if cl is None and not v1:
                bad += 1
                print("CLIP declares vacuous but vacuous_frac does not", (T0, T1, X0, X1, Y0, Y1))
        if cl is not None:
            # every admissible placement in the box must lie in the clipped box
            for _ in range(3):
                TT = rng.randint(T0, T1)
                cn, sn, dn = trig_int(TT, K)
                # admissible cx in [w/2, s-w/2] intersect [x0,x1]  (as Fractions)
                w = F(cn + sn, dn)
                lo_, hi_ = max(F(X0, D), w / 2), min(F(X1, D), s - w / 2)
                if lo_ <= hi_:
                    cx = lo_ + (hi_ - lo_) * F(rng.randint(0, 100), 100)
                    if not (F(cl[0], D) <= cx <= F(cl[1], D)):
                        bad += 1
                        print("CLIP lost an admissible cx", (T0, T1, X0, X1), cx, cl)
        if r1 != r2 or v1 != v2:
            bad += 1
            print("MISMATCH", s, atoms, (T0, T1, X0, X1, Y0, Y1), r1, r2, v1, v2)
        # soundness spot check: if inside for the box, then inside at random placements of the box
        if r1:
            for _ in range(3):
                tt = F(rng.randint(T0, T1), v.T_ROOT)
                cx = F(rng.randint(X0, X1), D)
                cy = F(rng.randint(Y0, Y1), D)
                if mass_at_frac(atoms, [ONE], tt, cx, cy) != 1:
                    bad += 1
                    print("UNSOUND", s, atoms, (T0, T1, X0, X1, Y0, Y1), tt, cx, cy)
    print(f"selftest: {n_iter} random boxes, {bad} problems")
    return bad == 0


# ============================================================================= parallel driver
_G = {}


def _worker_init(s, atoms, weights, margin, depth, tscale, use_float, max_w, per_box_cap):
    _G["v"] = Verifier(s, atoms, weights, margin=margin, depth=depth, tscale=tscale,
                       use_float=use_float, max_witnesses=max_w, verbose=False)
    _G["cap"] = per_box_cap


def _worker(box):
    v = _G["v"]
    v.reset_stats()
    v.run([box], per_box_cap=_G["cap"])
    return v.stats(), v.witnesses


def merge_stats(acc, st):
    for k, val in st.items():
        if isinstance(val, dict):
            dd = acc.setdefault(k, {})
            for kk, vv in val.items():
                dd[kk] = dd.get(kk, 0) + vv
        elif k == "max_depth":
            acc[k] = max(acc.get(k, 0), val)
        else:
            acc[k] = acc.get(k, 0) + val
    return acc


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cert", nargs="?")
    ap.add_argument("--depth", type=int, default=48,
                    help="max number of bisections per box (default 48 ~ width 2^-16 of the root in each dim)")
    ap.add_argument("--strict-margin", type=str, default="0",
                    help="require exact covered mass >= 1 + m on every box (rational string)")
    ap.add_argument("--report", nargs="?", const="__auto__", default=None,
                    help="write a JSON report (default path <cert>.report.json)")
    ap.add_argument("--witness-file", type=str, default=None,
                    help="where to write witnesses on FAIL (default <cert>.witnesses.json)")
    ap.add_argument("--max-witnesses", type=int, default=200, help="stop after this many witness boxes in total")
    ap.add_argument("--max-witnesses-per-box", type=int, default=8,
                    help="stop exploring one of the 4^k initial boxes after this many witnesses (diversity)")
    ap.add_argument("--jobs", type=int, default=1, help="worker processes (each takes initial boxes from the 4^k split)")
    ap.add_argument("--split", type=int, default=3, help="k: the root is first split into 4^k boxes in (cx,cy)")
    ap.add_argument("--scale-weights", type=str, default="1",
                    help="multiply every weight by this rational before verifying (e.g. 1.00000001 to absorb LP rounding)")
    ap.add_argument("--tscale", type=str, default="2", help="weight of the t-width when choosing the split axis")
    ap.add_argument("--no-float-prepass", action="store_true", help="exact checks on ALL atoms (slow; for auditing)")
    ap.add_argument("--n", type=int, default=None, help="override n (default: certificate field or 11)")
    ap.add_argument("--selftest", action="store_true", help="random cross-check int vs Fraction predicates")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return 0 if selftest() else 1
    if not a.cert:
        ap.error("certificate path required")

    t_start = time.time()
    try:
        d, s, n, atoms, weights, total = load_certificate(a.cert, a.n)
    except Exception as e:
        print(f"MALFORMED certificate: {e}")
        return 2
    margin = F(a.strict_margin)
    scale = F(a.scale_weights)
    if scale != 1:
        weights = [w * scale for w in weights]
        total = sum(weights, ZERO)
        print(f"weights scaled by {scale}")
    verbose = not a.quiet
    print(f"certificate: {a.cert}")
    print(f"s = {s} (~{float(s):.10f}), n = {n}, atoms = {len(atoms)}, "
          f"total mass = {total} (~{float(total):.10f}), margin = {margin}")
    if total >= n:
        print(f"FAIL: total mass {float(total):.6f} >= n = {n}: certificate proves nothing")
        return 2
    if s < 1:
        print("s < 1: no unit square fits; vacuous PASS")
        return 0

    use_float = not a.no_float_prepass
    v0 = Verifier(s, atoms, weights, margin=margin, depth=a.depth, tscale=F(a.tscale),
                  use_float=use_float, max_witnesses=a.max_witnesses, verbose=verbose)
    boxes = v0.root_boxes(a.split)
    stats = {}
    witnesses = []
    if a.jobs > 1:
        import multiprocessing as mp
        with mp.Pool(a.jobs, initializer=_worker_init,
                     initargs=(s, atoms, weights, margin, a.depth, F(a.tscale), use_float, a.max_witnesses,
                           a.max_witnesses_per_box)) as pool:
            done = 0
            for st, ws in pool.imap_unordered(_worker, boxes):
                merge_stats(stats, st)
                witnesses.extend(ws)
                done += 1
                if verbose and (done % max(1, len(boxes) // 16) == 0):
                    print(f"  ... {done}/{len(boxes)} top boxes, {stats['boxes']} boxes, "
                          f"{len(witnesses)} witnesses, {time.time()-t_start:.0f}s", flush=True)
                if len(witnesses) >= a.max_witnesses:
                    pool.terminate()
                    break
    else:
        v0.run(boxes, per_box_cap=a.max_witnesses_per_box)
        stats = v0.stats()
        witnesses = v0.witnesses
    stats["witnesses"] = len(witnesses)
    elapsed = time.time() - t_start
    passed = len(witnesses) == 0

    print(f"boxes = {stats['boxes']}  covered = {stats['covered']}  vacuous = {stats['vacuous']}  "
          f"split = {stats['split']}  exact atom checks = {stats['exact_atom_checks']}  "
          f"max depth = {stats['max_depth']}  time = {elapsed:.1f}s")
    if verbose:
        print("depth histogram (covered leaves):",
              " ".join(f"{k}:{v}" for k, v in sorted(stats['depth_hist_covered'].items())))
    if passed:
        print(f"PASS: every closed unit square in [0,{s}]^2 has mass >= {ONE + margin} ; total {total} < {n}"
              f"  ==>  s({n}) >= {s} (~{float(s):.10f})")
    else:
        holes = [w for w in witnesses if w.get("kind") == "hole"]
        tight = [w for w in witnesses if w.get("kind") == "tight"]
        und = [w for w in witnesses if w.get("kind") == "undecided"]
        print(f"FAIL: {len(witnesses)} witness boxes at depth {a.depth}: {len(holes)} HOLES (a placement with exact "
              f"mass < {ONE + margin}), {len(tight)} tight (mass ok at samples but an atom on the boundary of Q), "
              f"{len(und)} undecided at this depth"
              + ("  [stopped at --max-witnesses]" if len(witnesses) >= a.max_witnesses else ""))
        pick = min(witnesses, key=lambda w: w.get("float_mass", 9e9))
        if pick.get("placement"):
            p = pick["placement"]
            print(f"  worst witness: theta = {p['theta_deg']:.6f} deg, centre = ({p['cx_float']:.9f}, {p['cy_float']:.9f}), "
                  f"exact mass = {pick['exact_mass']} (~{pick['float_mass']:.12f})")
        cl = {}
        for w in witnesses:
            p = w.get("placement")
            if not p:
                continue
            key = (round(p["theta_deg"]), round(p["cx_float"] / 0.05) * 0.05, round(p["cy_float"] / 0.05) * 0.05)
            cl.setdefault(key, []).append(w["float_mass"])
        print(f"  {len(cl)} witness clusters (theta~1deg, centre~0.05):")
        for key, ms in sorted(cl.items(), key=lambda kv: min(kv[1]))[:12]:
            print(f"    theta~{key[0]:3d} deg centre~({key[1]:.2f},{key[2]:.2f})  n={len(ms):3d}  min mass {min(ms):.9f}")
        wf = a.witness_file or (os.path.splitext(a.cert)[0] + ".witnesses.json")
        with open(wf, "w") as fh:
            json.dump({"cert": a.cert, "s": str(s), "depth": a.depth, "margin": str(margin),
                       "scale_weights": str(scale), "witnesses": witnesses}, fh, indent=1)
        print(f"  witnesses written to {wf}")
    if a.report is not None:
        rp = a.report if a.report != "__auto__" else os.path.splitext(a.cert)[0] + ".report.json"
        with open(rp, "w") as fh:
            json.dump({"cert": a.cert, "s": str(s), "n": n, "atoms": len(atoms), "total": str(total),
                       "total_float": float(total), "margin": str(margin), "depth": a.depth,
                       "tscale": a.tscale, "jobs": a.jobs, "split": a.split, "float_prepass": use_float,
                       "scale_weights": str(scale),
                       "result": "PASS" if passed else "FAIL", "time_s": elapsed, "stats": stats,
                       "witnesses_preview": witnesses[:20]}, fh, indent=1)
        print(f"  report written to {rp}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
