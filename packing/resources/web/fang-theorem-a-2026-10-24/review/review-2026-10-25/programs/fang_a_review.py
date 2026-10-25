#!/usr/bin/env python3
"""Kevin Fang's Theorem A (#797), its construction re-implemented from the note alone.

Stage 4 mathematical review, lane c-review-797-math, 25 October 2026. Written from note
v0.2 (theorem-a/note/main.tex, SHA-256 f6f26d7b...1152) before its author read any
program of the source (lband.py, windowed_check.py) or the maintained
cases/asymptotic/fang_theorem_a.py. Every quantity is exact: int and fractions.Fraction.

Subcommands, each writing a JSON receipt with --out:

  construction  For every k in [--kmin, --kmax] and every odd b with |b - sqrt(2k)| <= 1:
                choose a rational t = 1/b + delta, decide (a)-(d), H(t) < 4 sqrt(2k) + 2,
                S < k, k - b > h; count the packing N(t) by the note's formulas; decide
                w = k^2 - N(t) < H(t) (identity (1) with Lemmas 2 and 3) and
                w < 4 sqrt(2k) + 2; decide Lemma 2 at each end and Lemma 3 for each band;
                B(k) < 4 sqrt(2k) + 2. With --limit-kmax, also the one-sided limit count
                as t -> 1/b+ (exact power series in t - 1/b), and B(k) - w there.
  lemmas        Lemma 2 and Lemma 3, and (E2) square by square, at sampled close t across
                the whole close interval, sampled lifts y in [0, sec) (ties included) and
                sampled band lengths L > h. A sample.
  geometry      Every square of the packing at the listed k, both widths at a tie: inside
                [0, S]^2, pairwise disjoint interiors (exact separating-axis test), count
                equal to N(t); and mutated packings that must be refused.
  sharpness     The remark of Section 5 at k = (b^2 - b + 8)/2: the limit waste, the waste
                over the close interval, and 4 sqrt(2k) + 2 - 4b.
  ties          k = 2m^2 (sqrt(2k) an even integer, two odd widths) for m up to --mmax.
  squeeze       The note's Section 6 example: k = 43218 at a fixed squeeze.
  selftest      Small known answers and refusals.

Run with the project interpreter: python3 -I fang_a_review.py SUBCOMMAND --out FILE.json
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import math
import sys
import time
from dataclasses import dataclass, field
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

HALF = Q(1, 2)


def fl(x: Q | int) -> int:
    """Exact floor of a rational."""
    if isinstance(x, int):
        return x
    return x.numerator // x.denominator


def below_bound(x: Q | int, k: int) -> bool:
    """Exactly decide x < 4 sqrt(2k) + 2."""
    y = Q(x) - 2
    return y < 0 or y * y < 32 * k


def odd_widths(k: int) -> list[int]:
    """Every odd b >= 1 with |b - sqrt(2k)| <= 1, decided in integers."""
    r = math.isqrt(2 * k)
    return [b for b in range(max(1, r - 3), r + 4)
            if b % 2 == 1 and (b - 1) ** 2 <= 2 * k <= (b + 1) ** 2]


def kappa(b: int) -> Q:
    return Q(7 * b**4 + 1, b * (b * b + 1) ** 2)


def B_of(k: int, b: int) -> Q:
    D = b * b + 1
    return Q(4 * k * b, D) + 2 * b + 2 + Q(2, D) - 2 * kappa(b)


# ---------------------------------------------------------------- the band at a rational t


@dataclass(frozen=True)
class Angle:
    b: int
    t: Q
    c: Q
    s: Q
    tan: Q
    tau: Q
    sec: Q
    W: Q
    h: Q
    eta: Q


@functools.lru_cache(maxsize=8192)
def angle(b: int, t: Q) -> Angle:
    t2 = t * t
    d = 1 + t2
    c = (1 - t2) / d
    s = 2 * t / d
    tau = c / s
    return Angle(b, t, c, s, s / c, tau, 1 / c, b * c + s, b * s + c, Q(b, 2) - tau)


def close(a: Angle) -> dict[str, bool]:
    return {
        "a": fl(a.W - a.s - a.tau) == (a.b - 1) // 2,
        "b": 0 <= a.eta < HALF,
        "c": 2 * a.tau - a.b * a.c >= 0,
        "d": a.h < 3,
    }


def levels(a: Angle, y: Q) -> list[int]:
    """m_0(y), m_1(y), ... of the note's Fill, up to the first level with a_i >= W."""
    out: list[int] = []
    i = 0
    while True:
        raw = a.s + (i + 1 - y) * a.tau
        if raw >= a.W:
            return out
        ai = raw if raw > 0 else Q(0)
        out.append(max(0, fl(a.W - ai)))
        i += 1


@dataclass
class Band:
    L: Q
    R: int
    F: Q
    near: list[int]
    far: list[int]
    b: int

    @property
    def count(self) -> int:
        return self.b * self.R + sum(self.near) + sum(self.far)


def band(a: Angle, L: Q) -> Band:
    if not L > a.h:
        raise ValueError("L <= h")
    R = fl((L - a.h) * a.c) + 1  # floor((L - h)/sec) + 1
    F = L - (R - 1) * a.sec - a.h
    if not (0 <= F < a.sec):
        raise AssertionError("free length outside [0, sec)")
    return Band(L, R, F, levels(a, Q(0)), levels(a, F), a.b)


def rhs2(a: Angle, L: Q) -> Q:
    b = a.b
    return (b * L * (1 - a.c) + b * a.c * a.h - 2 * b + 2
            - 2 * (a.W - a.s - 2 * a.tau) + 2 * a.eta)


def lemma2_far_bound(a: Angle, y: Q) -> Q:
    z = a.W - a.s - 2 * a.tau + y * a.tau
    return Q(a.b - 1, 2) + 2 * z - 1 - 2 * a.eta


@dataclass
class Packing:
    k: int
    b: int
    t: Q
    a: Angle
    S: Q
    right: Band
    top: Band
    N: int
    w: int
    H: Q
    checks: dict[str, bool] = field(default_factory=dict)


def evaluate(k: int, b: int, t: Q) -> Packing:
    """The packing of Section 3 at (k, b, t), with every inequality the proof uses."""
    a = angle(b, t)
    S = k - b + a.W
    chk: dict[str, bool] = {}
    cl = close(a)
    chk.update({f"close_{key}": val for key, val in cl.items()})
    chk["t_above_1/b"] = t > Q(1, b)
    chk["S_below_k"] = S < k
    chk["k-b_above_h"] = (k - b) > a.h
    right = band(a, S)
    top = band(a, Q(k - b))
    N = (k - b) ** 2 + right.count + top.count
    w = k * k - N
    H = b * (k - S) + rhs2(a, S) + rhs2(a, Q(k - b))
    # identity (1) as an equality for the count
    chk["identity_1"] = w == b * (k - S) + (b * S - right.count) + (b * (k - b) - top.count)
    for name, bd in (("right", right), ("top", top)):
        chk[f"lemma2_near_{name}"] = sum(bd.near) >= Q(b - 1, 2)
        chk[f"lemma2_far_{name}"] = sum(bd.far) > lemma2_far_bound(a, bd.F)
        chk[f"lemma3_{name}"] = b * bd.L - bd.count < rhs2(a, bd.L)
    chk["w_below_H"] = w < H
    chk["H_below_bound"] = below_bound(H, k)
    chk["w_below_bound"] = below_bound(w, k)
    return Packing(k, b, t, a, S, right, top, N, w, H, chk)


def first_delta(k_hi: int, b: int) -> Q:
    D = b * b + 1
    return Q(1, b * D * (6 * k_hi + 4 * b))


def choose(k: int, b: int, delta: Q) -> tuple[Packing, int]:
    """The first t = 1/b + delta/8^j, j >= 0, that is close with H(t) below the bound."""
    j = 0
    while True:
        t = Q(1, b) + delta / 8**j
        a = angle(b, t)
        if all(close(a).values()):
            S = k - b + a.W
            H = b * (k - S) + rhs2(a, S) + rhs2(a, Q(k - b))
            if below_bound(H, k):
                return evaluate(k, b, t), j
        j += 1
        if j > 40:
            raise RuntimeError(f"no admissible t found at k={k}, b={b}")


# ---------------------------------------------------- the one-sided limit t -> 1/b+, exact


class Undetermined(Exception):
    pass


class Ser:
    """A power series in e = t - 1/b, truncated at ORDER, with Fraction coefficients."""

    __slots__ = ("v",)
    ORDER = 3

    def __init__(self, v: list[Q]) -> None:
        self.v = v

    @staticmethod
    def const(x: Q | int) -> Ser:
        return Ser([Q(x)] + [Q(0)] * Ser.ORDER)

    @staticmethod
    def var(x0: Q) -> Ser:
        return Ser([Q(x0), Q(1)] + [Q(0)] * (Ser.ORDER - 1))

    def _c(self, o: Ser | Q | int) -> Ser:
        return o if isinstance(o, Ser) else Ser.const(o)

    def __add__(self, o: Ser | Q | int) -> Ser:
        o = self._c(o)
        return Ser([p + q for p, q in zip(self.v, o.v)])

    __radd__ = __add__

    def __neg__(self) -> Ser:
        return Ser([-p for p in self.v])

    def __sub__(self, o: Ser | Q | int) -> Ser:
        return self + (-self._c(o))

    def __rsub__(self, o: Ser | Q | int) -> Ser:
        return self._c(o) - self

    def __mul__(self, o: Ser | Q | int) -> Ser:
        if not isinstance(o, Ser):
            return Ser([p * o for p in self.v])
        n = Ser.ORDER
        r = [Q(0)] * (n + 1)
        for i_, p in enumerate(self.v):
            if p:
                for j_ in range(n + 1 - i_):
                    r[i_ + j_] += p * o.v[j_]
        return Ser(r)

    __rmul__ = __mul__

    def inv(self) -> Ser:
        a0 = self.v[0]
        if a0 == 0:
            raise ZeroDivisionError
        n = Ser.ORDER
        r = [Q(0)] * (n + 1)
        r[0] = 1 / a0
        for m in range(1, n + 1):
            acc = Q(0)
            for i_ in range(1, m + 1):
                acc += self.v[i_] * r[m - i_]
            r[m] = -acc / a0
        return Ser(r)

    def __truediv__(self, o: Ser | Q | int) -> Ser:
        if not isinstance(o, Ser):
            return Ser([p / o for p in self.v])
        return self * o.inv()

    def __rtruediv__(self, o: Ser | Q | int) -> Ser:
        return self._c(o) * self.inv()

    def sign(self) -> int | None:
        for p in self.v:
            if p:
                return 1 if p > 0 else -1
        return None


def gsign(x: Ser) -> int:
    sg = x.sign()
    if sg is None:
        raise Undetermined
    return sg


def lim_floor(g: Ser) -> int:
    v0 = g.v[0]
    n = fl(v0)
    if v0 != n:
        return n
    return n if gsign(g - n) > 0 else n - 1


@dataclass
class SerAngle:
    b: int
    c: Ser
    s: Ser
    tau: Ser
    sec: Ser
    W: Ser
    h: Ser


_SER_CACHE: dict[tuple[int, int], SerAngle] = {}


def ser_angle(b: int) -> SerAngle:
    key = (b, Ser.ORDER)
    if key not in _SER_CACHE:
        t = Ser.var(Q(1, b))
        t2 = t * t
        d = 1 + t2
        c = (1 - t2) / d
        s = (2 * t) / d
        tau = c / s
        _SER_CACHE[key] = SerAngle(b, c, s, tau, 1 / c, b * c + s, b * s + c)
    return _SER_CACHE[key]


def lim_levels(sa: SerAngle, y: Ser) -> list[int]:
    out: list[int] = []
    i_ = 0
    while True:
        raw = sa.s + (i_ + 1 - y) * sa.tau
        if gsign(raw - sa.W) >= 0:
            return out
        sr = raw.sign()
        ai = raw if (sr is not None and sr > 0) else Ser.const(0)
        out.append(max(0, lim_floor(sa.W - ai)))
        i_ += 1


def lim_band(sa: SerAngle, L: Ser) -> tuple[int, int, int]:
    if gsign(L - sa.h) <= 0:
        raise ValueError("L <= h in the limit")
    R = lim_floor((L - sa.h) * sa.c) + 1
    F = L - (R - 1) * sa.sec - sa.h
    if F.sign() == -1 or gsign(sa.sec - F) <= 0:
        raise AssertionError("limit free length outside [0, sec)")
    return R, sum(lim_levels(sa, Ser.const(0))), sum(lim_levels(sa, F))


def limit_waste(k: int, b: int) -> tuple[int, int]:
    """k^2 - N(t) for every t in some interval (1/b, 1/b + e'), and the series order used."""
    for order in (3, 6, 10):
        Ser.ORDER = order
        try:
            sa = ser_angle(b)
            L1 = Ser.const(k - b) + sa.W
            R1, n1, f1 = lim_band(sa, L1)
            R2, n2, f2 = lim_band(sa, Ser.const(k - b))
            N = (k - b) ** 2 + b * (R1 + R2) + n1 + f1 + n2 + f2
            return k * k - N, order
        except Undetermined:
            continue
        finally:
            Ser.ORDER = 3
    raise Undetermined(f"k={k} b={b}")


# ------------------------------------------------------------------------------ helpers


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frac(x: Q) -> str:
    return f"{x.numerator}/{x.denominator}"


def write(out: Path, receipt: dict[str, Any]) -> None:
    receipt = {
        "program": Path(__file__).name,
        "program_sha256": sha256(Path(__file__)),
        "python": sys.version.split()[0],
        **receipt,
    }
    out.write_text(json.dumps(receipt, indent=1) + "\n")


# ------------------------------------------------------------------------- construction


def cmd_construction(args: argparse.Namespace) -> int:
    t0 = time.process_time()
    failures: list[dict[str, Any]] = []
    pairs = 0
    halvings_max = 0
    halved = 0
    min_bound_minus_w: tuple[Q, int, int] | None = None
    min_B_slack_to_bound_sq: tuple[float, int, int] | None = None
    lim = {"pairs": 0, "orders": {}, "min_B_minus_w": None, "w_lim_eq_w_t": 0,
           "w_lim_ne_w_t": [], "B_minus_wlim_nonpositive": []}
    near_loss_max: tuple[Q, int, int] | None = None
    far_loss_max: tuple[Q, int, int, str] | None = None
    far_loss_over_3_2 = 0
    delta_cache: dict[int, Q] = {}
    for k in range(args.kmin, args.kmax + 1):
        for b in odd_widths(k):
            pairs += 1
            if b not in delta_cache:
                delta_cache[b] = first_delta((b + 1) ** 2 // 2, b)
            Bk = B_of(k, b)
            if not below_bound(Bk, k):
                failures.append({"k": k, "b": b, "what": "B(k) not below the bound"})
            try:
                p, j = choose(k, b, delta_cache[b])
            except Exception as exc:  # noqa: BLE001 - recorded as a failure
                failures.append({"k": k, "b": b, "what": repr(exc)})
                continue
            if j:
                halved += 1
                halvings_max = max(halvings_max, j)
            bad = [name for name, ok in p.checks.items() if not ok]
            if bad:
                failures.append({"k": k, "b": b, "t": frac(p.t), "failed": bad})
            # margin of w below the bound, as (4 sqrt(2k) + 2 - w), exact via a float only for reporting
            gap = 4 * math.sqrt(2 * k) + 2 - p.w
            if min_bound_minus_w is None or gap < min_bound_minus_w[0]:
                min_bound_minus_w = (gap, k, b)
            bgap = 4 * math.sqrt(2 * k) + 2 - float(Bk)
            if min_B_slack_to_bound_sq is None or bgap < min_B_slack_to_bound_sq[0]:
                min_B_slack_to_bound_sq = (bgap, k, b)
            # rounding losses at the two ends of each band (continuous length minus squares)
            a = p.a
            for name, bd in (("right", p.right), ("top", p.top)):
                for which, y, got in (("near", Q(0), bd.near), ("far", bd.F, bd.far)):
                    cont = Q(0)
                    i_ = 0
                    while True:
                        raw = a.s + (i_ + 1 - y) * a.tau
                        if raw >= a.W:
                            break
                        cont += a.W - (raw if raw > 0 else 0)
                        i_ += 1
                    loss = cont - sum(got)
                    if which == "near":
                        if near_loss_max is None or loss > near_loss_max[0]:
                            near_loss_max = (loss, k, b)
                    else:
                        if loss > Q(3, 2):
                            far_loss_over_3_2 += 1
                        if far_loss_max is None or loss > far_loss_max[0]:
                            far_loss_max = (loss, k, b, name)
            if k <= args.limit_kmax:
                wl, order = limit_waste(k, b)
                lim["pairs"] += 1
                lim["orders"][order] = lim["orders"].get(order, 0) + 1
                slack = Bk - wl
                if slack <= 0:
                    lim["B_minus_wlim_nonpositive"].append({"k": k, "b": b, "w_lim": wl})
                if lim["min_B_minus_w"] is None or slack < lim["min_B_minus_w"][0]:
                    lim["min_B_minus_w"] = (slack, k, b, wl)
                if wl == p.w:
                    lim["w_lim_eq_w_t"] += 1
                else:
                    lim["w_lim_ne_w_t"].append({"k": k, "b": b, "w_lim": wl, "w_t": p.w})
    cpu = time.process_time() - t0
    assert min_bound_minus_w is not None and near_loss_max is not None and far_loss_max is not None
    lm = lim["min_B_minus_w"]
    receipt = {
        "subcommand": "construction",
        "range": [args.kmin, args.kmax],
        "pairs_k_b": pairs,
        "failures": failures,
        "all_checks_hold": not failures,
        "delta_rule": "t = 1/b + delta, delta = 1/(b(b^2+1)(6 k_hi + 4b)), k_hi = floor((b+1)^2/2), "
                      "divided by 8 until (a)-(d) and H(t) < 4 sqrt(2k) + 2 hold",
        "pairs_needing_a_smaller_delta": halved,
        "most_divisions_by_8": halvings_max,
        "least_bound_minus_w_float": {"value": min_bound_minus_w[0], "k": min_bound_minus_w[1],
                                      "b": min_bound_minus_w[2]},
        "least_bound_minus_B_float": {"value": min_B_slack_to_bound_sq[0] if min_B_slack_to_bound_sq else None,
                                      "k": min_B_slack_to_bound_sq[1] if min_B_slack_to_bound_sq else None,
                                      "b": min_B_slack_to_bound_sq[2] if min_B_slack_to_bound_sq else None},
        "near_end_rounding_loss_max": {"value": frac(near_loss_max[0]), "float": float(near_loss_max[0]),
                                       "k": near_loss_max[1], "b": near_loss_max[2]},
        "far_end_rounding_loss_max": {"value": frac(far_loss_max[0]), "float": float(far_loss_max[0]),
                                      "k": far_loss_max[1], "b": far_loss_max[2], "band": far_loss_max[3]},
        "far_end_losses_above_3/2": far_loss_over_3_2,
        "limit": {
            "kmax": args.limit_kmax,
            "pairs": lim["pairs"],
            "series_orders_used": lim["orders"],
            "least_B_minus_w_lim": None if lm is None else
            {"value": frac(lm[0]), "float": float(lm[0]), "k": lm[1], "b": lm[2], "w_lim": lm[3]},
            "B_minus_w_lim_nonpositive": lim["B_minus_wlim_nonpositive"],
            "w_lim_equals_w_at_chosen_t": lim["w_lim_eq_w_t"],
            "w_lim_differs_from_w_at_chosen_t": lim["w_lim_ne_w_t"][:50],
            "w_lim_differs_count": len(lim["w_lim_ne_w_t"]),
        },
        "cpu_seconds": round(cpu, 1),
    }
    write(args.out, receipt)
    print(json.dumps({k_: v for k_, v in receipt.items() if k_ not in ("failures",)}, indent=1)[:3000])
    print(f"failures: {len(failures)}")
    return 0 if not failures and not lim["B_minus_wlim_nonpositive"] else 1


# ------------------------------------------------------------------------------- lemmas


def close_samples(b: int, count: int) -> list[Q]:
    """Close t spread over the close set: a scan of (1/b, 1/b + 8/b^3], plus extremes."""
    t0 = Q(1, b)
    span = Q(8, b**3)
    found: list[Q] = []
    flags: list[bool] = []
    steps = 512
    for j in range(1, steps + 1):
        t = t0 + span * j / steps
        ok = all(close(angle(b, t)).values())
        flags.append(ok)
        if ok:
            found.append(t)
    # the close set should be an interval starting at 1/b: count the switches
    switches = sum(1 for p, q in zip(flags, flags[1:]) if p != q)
    if not found:
        raise RuntimeError(f"no close t found for b={b}")
    # the last close t: refine the boundary by bisection between it and the next scan point
    lo = found[-1]
    hi = lo + span / steps
    for _ in range(80):
        mid = (lo + hi) / 2
        if all(close(angle(b, mid)).values()):
            lo = mid
        else:
            hi = mid
    pick = [t0 + Q(1, 10**30), t0 + Q(1, b**6)]
    stride = max(1, len(found) // count)
    pick += found[::stride]
    pick += [lo]
    out = []
    for t in pick:
        if t > t0 and all(close(angle(b, t)).values()) and t not in out:
            out.append(t)
    return out + [Q(switches), hi - t0]  # two trailing diagnostics, popped by the caller


def lift_samples(a: Angle) -> list[Q]:
    ys: list[Q] = [Q(0), Q(1, 10**25), Q(1), a.sec - Q(1, 10**25), a.sec * Q(39, 40)]
    ys += [a.sec * j / 40 for j in range(1, 40)]
    base = a.W - a.s - 2 * a.tau  # z = base + y tau
    target_lo = base
    target_hi = base + a.sec * a.tau
    n_lo = fl(target_lo) - 1
    n_hi = fl(target_hi) + 1
    for n in range(n_lo, n_hi + 1):
        for f in (Q(0), HALF + a.eta, HALF + a.eta - Q(1, 10**25), HALF + a.eta + Q(1, 10**25),
                  1 - Q(1, 10**25), HALF - a.eta):
            zt = n + f
            y = (zt - base) / a.tau
            if 0 <= y < a.sec:
                ys.append(y)
    return ys


def length_samples(a: Angle) -> list[Q]:
    Ls: list[Q] = [a.h + Q(1, 10**20), a.h + HALF, a.h + 1]
    Ls += [Q(n) for n in range(3, 61)]
    Ls += [Q(n) for n in (97, 101, 250, 1000, 4999, 10**4, 10**5 + 7, 10**6)]
    Ls += [Q(10**4 * j + 3, 7 * j + 11) for j in range(1, 30)]
    Ls += [a.h + j * a.sec for j in range(0, 40)]                      # F = 0 exactly
    Ls += [a.h + j * a.sec + a.sec - Q(1, 10**20) for j in range(0, 40)]  # F just below sec
    return [L for L in Ls if L > a.h]


def e2_violations(a: Angle, y: Q, lev: list[int]) -> int:
    """Squares of the fill at lift y that are not under l(X) = V with vertex (s, y)."""
    bad = 0
    for i_, m in enumerate(lev):
        if m == 0:
            continue
        x0 = a.W - m
        if x0 < 0:
            bad += 1
            continue
        if x0 <= a.s:
            low = y  # the minimum of l on [x0, W] is at X = s
        else:
            low = y + (x0 - a.s) * a.tan
        if not (i_ + 1 <= low):
            bad += 1
    return bad


def cmd_lemmas(args: argparse.Namespace) -> int:
    t_start = time.process_time()
    bs = list(range(3, 100, 2)) + [101, 199, 347, 999, 2001]
    rows = []
    fail = []
    l2_min = None
    l3_min = None
    for b in bs:
        ts = close_samples(b, args.per_b)
        boundary_width = ts.pop()
        switches = ts.pop()
        n2 = n3 = 0
        for t in ts:
            a = angle(b, t)
            near = levels(a, Q(0))
            if not sum(near) >= Q(b - 1, 2):
                fail.append({"b": b, "t": frac(t), "what": "Lemma 2 near"})
            if e2_violations(a, Q(0), near):
                fail.append({"b": b, "t": frac(t), "what": "(E2) near"})
            for y in lift_samples(a):
                lev = levels(a, y)
                slack = sum(lev) - lemma2_far_bound(a, y)
                n2 += 1
                if not slack > 0:
                    fail.append({"b": b, "t": frac(t), "y": frac(y), "what": "Lemma 2 far"})
                if e2_violations(a, y, lev):
                    fail.append({"b": b, "t": frac(t), "y": frac(y), "what": "(E2) far"})
                if l2_min is None or slack < l2_min[0]:
                    l2_min = (slack, b)
            for L in length_samples(a):
                bd = band(a, L)
                slack3 = rhs2(a, L) - (b * L - bd.count)
                n3 += 1
                if not slack3 > 0:
                    fail.append({"b": b, "t": frac(t), "L": frac(L), "what": "Lemma 3"})
                if l3_min is None or slack3 < l3_min[0]:
                    l3_min = (slack3, b)
        rows.append({"b": b, "close_t_sampled": len(ts), "lemma2_cases": n2, "lemma3_cases": n3,
                     "scan_switches": int(switches), "close_set_right_end_minus_1/b_upper": float(boundary_width)})
    assert l2_min is not None and l3_min is not None
    # The whole chain at close t far from 1/b: identity (1), Lemmas 2 and 3, and w(t) < H(t),
    # at every sampled close t of the close interval (H(t) below the bound is not required).
    chain_cases = 0
    chain_bound_holds = 0
    sample_cache: dict[int, list[Q]] = {}
    for k in list(range(6, 401)) + [1000, 4999, 20000, 59344, 60000]:
        for b in odd_widths(k):
            if b not in sample_cache:
                ts = close_samples(b, args.per_b)
                ts.pop()
                ts.pop()
                sample_cache[b] = ts
            for t in sample_cache[b]:
                p = evaluate(k, b, t)
                chain_cases += 1
                bad = [n for n, ok in p.checks.items()
                       if not ok and n not in ("H_below_bound", "w_below_bound")]
                if bad:
                    fail.append({"k": k, "b": b, "t": frac(t), "what": "chain", "failed": bad})
                if p.checks["H_below_bound"]:
                    chain_bound_holds += 1
                    if not p.checks["w_below_bound"]:
                        fail.append({"k": k, "b": b, "t": frac(t), "what": "H below bound but w not"})
    receipt = {
        "subcommand": "lemmas",
        "widths": bs,
        "rows": rows,
        "chain_cases": chain_cases,
        "chain_cases_with_H_below_bound": chain_bound_holds,
        "failures": fail,
        "all_hold": not fail,
        "least_lemma2_slack": {"value": frac(l2_min[0]), "float": float(l2_min[0]), "b": l2_min[1]},
        "least_lemma3_slack": {"value": frac(l3_min[0]), "float": float(l3_min[0]), "b": l3_min[1]},
        "lemma2_cases": sum(r["lemma2_cases"] for r in rows),
        "lemma3_cases": sum(r["lemma3_cases"] for r in rows),
        "cpu_seconds": round(time.process_time() - t_start, 1),
    }
    write(args.out, receipt)
    print(json.dumps({k_: v for k_, v in receipt.items() if k_ != "rows"}, indent=1)[:2500])
    return 0 if not fail else 1


# ----------------------------------------------------------------------------- geometry

Pt = tuple[Q, Q]


def build_squares(k: int, b: int, t: Q, mutate: str | None = None) -> tuple[list[list[Pt]], Q, int]:
    a = angle(b, t)
    S = k - b + a.W
    sq: list[list[Pt]] = []

    def axis(x0: Q, y0: Q) -> list[Pt]:
        return [(x0, y0), (x0 + 1, y0), (x0 + 1, y0 + 1), (x0, y0 + 1)]

    gshift = Q(1, 10**6) if mutate == "grid_shift_right" else Q(0)
    for i_ in range(k - b):
        for j_ in range(k - b):
            sq.append(axis(Q(i_) + gshift, Q(j_)))
    count = (k - b) ** 2
    for which, L in (("right", S), ("top", Q(k - b))):
        if which == "right":
            def place(X: Q, Y: Q) -> Pt:
                return (k - b + X, Y)
        else:
            def place(X: Q, Y: Q) -> Pt:
                return (Y, k - b + X)
        bd = band(a, L)
        R = bd.R + (1 if (mutate == "extra_row" and which == "right") else 0)
        lift = -Q(1, 10**6) if (mutate == "rows_down" and which == "right") else Q(0)
        for j_ in range(R):
            for q in range(b):
                vs = []
                for (uu, vv) in ((q, 0), (q + 1, 0), (q + 1, 1), (q, 1)):
                    X = a.s + uu * a.c - vv * a.s
                    Y = lift + j_ * a.sec + uu * a.s + vv * a.c
                    vs.append(place(X, Y))
                sq.append(vs)
        count += b * bd.R
        near = list(bd.near)
        far = list(bd.far)
        if mutate == "near_plus_one" and which == "right":
            near[0] += 1
        if mutate == "far_plus_one" and which == "top":
            far[0] += 1
        if mutate == "far_level1_plus_one" and which == "right":
            if len(far) > 1:
                far[1] += 1
            else:
                far.append(1)
        for i_, m in enumerate(near):
            for q in range(m):
                x0 = a.W - m + q
                sq.append([place(X, Y) for (X, Y) in axis(x0, Q(i_))])
        for i_, m in enumerate(far):
            for q in range(m):
                x0 = a.W - m + q
                sq.append([place(a.W - X, L - Y) for (X, Y) in axis(x0, Q(i_))])
        count += sum(bd.near) + sum(bd.far)
    if mutate == "duplicate":
        sq.append(list(sq[len(sq) // 2]))
    return sq, S, count


def check_squares(sq: list[list[Pt]], S: Q) -> dict[str, Any]:
    dens = set()
    for vs in sq:
        for (px, py) in vs:
            dens.add(px.denominator)
            dens.add(py.denominator)
    lcd = 1
    for d in dens:
        lcd = lcd * d // math.gcd(lcd, d)
    iv = [[(int(px * lcd), int(py * lcd)) for (px, py) in vs] for vs in sq]
    Sint = S * lcd
    outside = 0
    for vs in iv:
        for (px, py) in vs:
            if not (0 <= px <= Sint and 0 <= py <= Sint):
                outside += 1
                break
    # unit side check: |v1 - v0|^2 = |v3 - v0|^2 = lcd^2 and perpendicular
    not_unit = 0
    for vs in iv:
        e1 = (vs[1][0] - vs[0][0], vs[1][1] - vs[0][1])
        e2 = (vs[3][0] - vs[0][0], vs[3][1] - vs[0][1])
        e3 = (vs[2][0] - vs[1][0], vs[2][1] - vs[1][1])
        if (e1[0] ** 2 + e1[1] ** 2 != lcd * lcd or e2[0] ** 2 + e2[1] ** 2 != lcd * lcd
                or e1[0] * e2[0] + e1[1] * e2[1] != 0 or e3 != e2):
            not_unit += 1
    # centre doubled: v0 + v2
    cen = [(vs[0][0] + vs[2][0], vs[0][1] + vs[2][1]) for vs in iv]
    lim = 8 * lcd * lcd  # |2c1 - 2c2|^2 >= 4 * 2 lcd^2 means centre distance >= sqrt 2
    cell = 2 * lcd * 2  # bucket side 2 (in doubled units)
    buckets: dict[tuple[int, int], list[int]] = {}
    for idx, (cx, cy) in enumerate(cen):
        buckets.setdefault((cx // cell, cy // cell), []).append(idx)
    overlaps = 0
    sat_tests = 0
    first_overlap = None
    for (bx, by), members in buckets.items():
        neigh: list[int] = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                neigh.extend(buckets.get((bx + dx, by + dy), []))
        for i_ in members:
            ci = cen[i_]
            for j_ in neigh:
                if j_ <= i_:
                    continue
                cj = cen[j_]
                if (ci[0] - cj[0]) ** 2 + (ci[1] - cj[1]) ** 2 >= lim:
                    continue
                sat_tests += 1
                if not separated(iv[i_], iv[j_]):
                    overlaps += 1
                    if first_overlap is None:
                        first_overlap = [i_, j_]
    return {"squares": len(sq), "outside": outside, "not_unit": not_unit, "overlapping_pairs": overlaps,
            "sat_tests": sat_tests, "first_overlap": first_overlap}


def separated(p: list[tuple[int, int]], q: list[tuple[int, int]]) -> bool:
    """Interiors disjoint iff some edge direction of p or q weakly separates them."""
    for poly in (p, q):
        for e in ((poly[1][0] - poly[0][0], poly[1][1] - poly[0][1]),
                  (poly[3][0] - poly[0][0], poly[3][1] - poly[0][1])):
            # the normal of one edge of a square is the direction of the other
            pp = [vx * e[0] + vy * e[1] for (vx, vy) in p]
            qq = [vx * e[0] + vy * e[1] for (vx, vy) in q]
            if max(pp) <= min(qq) or max(qq) <= min(pp):
                return True
    return False


MUTANTS = ("near_plus_one", "far_plus_one", "far_level1_plus_one", "extra_row", "rows_down",
           "grid_shift_right", "duplicate")


def cmd_geometry(args: argparse.Namespace) -> int:
    t_start = time.process_time()
    ks = parse_ks(args.k)
    rows = []
    fail = []
    ctrl = []
    for k in ks:
        for b in odd_widths(k):
            p, j = choose(k, b, first_delta((b + 1) ** 2 // 2, b))
            sq, S, count = build_squares(k, b, p.t)
            res = check_squares(sq, S)
            ok = (res["outside"] == 0 and res["not_unit"] == 0 and res["overlapping_pairs"] == 0
                  and res["squares"] == p.N == count and S < k and all(p.checks.values()))
            rows.append({"k": k, "b": b, "t": frac(p.t), "S_below_k": S < k, "N": p.N, "w": p.w,
                         "bound": 4 * math.sqrt(2 * k) + 2, **res, "valid": ok})
            if not ok:
                fail.append({"k": k, "b": b, **res})
            if k in args.controls_at:
                for mut in MUTANTS:
                    msq, mS, _ = build_squares(k, b, p.t, mutate=mut)
                    mres = check_squares(msq, mS)
                    refused = (mres["outside"] > 0 or mres["overlapping_pairs"] > 0 or mres["not_unit"] > 0)
                    ctrl.append({"k": k, "b": b, "mutant": mut, "refused": refused,
                                 "outside": mres["outside"], "overlapping_pairs": mres["overlapping_pairs"]})
    receipt = {
        "subcommand": "geometry",
        "rows": rows,
        "failures": fail,
        "controls": ctrl,
        "all_valid": not fail,
        "all_controls_refused": all(c["refused"] for c in ctrl),
        "cpu_seconds": round(time.process_time() - t_start, 1),
    }
    write(args.out, receipt)
    for r in rows:
        print(f"k={r['k']:4d} b={r['b']:3d} squares={r['squares']:6d} N={r['N']:6d} w={r['w']:3d} "
              f"sat={r['sat_tests']:6d} overlaps={r['overlapping_pairs']} outside={r['outside']} valid={r['valid']}")
    for c in ctrl:
        print(f"control k={c['k']} b={c['b']} {c['mutant']}: refused={c['refused']}")
    print(f"cpu {receipt['cpu_seconds']} s; valid={not fail}; controls refused={receipt['all_controls_refused']}")
    return 0 if (not fail and receipt["all_controls_refused"]) else 1


def parse_ks(spec: str) -> list[int]:
    out: list[int] = []
    for part in spec.split(","):
        if "-" in part:
            lo, hi = part.split("-")
            out.extend(range(int(lo), int(hi) + 1))
        else:
            out.append(int(part))
    return out


# --------------------------------------------------------------------------- sharpness


def cmd_sharpness(args: argparse.Namespace) -> int:
    t_start = time.process_time()
    rows = []
    fail = []
    for b in range(5, args.bmax + 1, 2):
        k = (b * b - b + 8) // 2
        widths = odd_widths(k)
        wl, order = limit_waste(k, b)
        gap = 4 * math.sqrt(2 * k) + 2 - 4 * b
        row: dict[str, Any] = {"b": b, "k": k, "widths": widths, "w_lim": wl, "four_b": 4 * b,
                               "bound_minus_4b": gap, "times_b": gap * b, "series_order": order}
        if b <= args.scan_bmax:
            # the waste over the whole close interval, at the sampled close t
            ts = close_samples(b, 24)
            ts.pop()
            ts.pop()
            ws = sorted({evaluate(k, b, t).w for t in ts if (k - b) > angle(b, t).h})
            row["w_over_close_t"] = ws
        rows.append(row)
        if wl != 4 * b or b not in widths:
            fail.append(row)
    receipt = {
        "subcommand": "sharpness",
        "rows": rows,
        "failures": fail,
        "w_lim_is_4b_at_every_b": not fail,
        "cpu_seconds": round(time.process_time() - t_start, 1),
    }
    write(args.out, receipt)
    for r in rows[:12] + rows[-3:]:
        print(r)
    print(f"failures {len(fail)}; cpu {receipt['cpu_seconds']}")
    return 0 if not fail else 1


# -------------------------------------------------------------------------------- ties


def cmd_ties(args: argparse.Namespace) -> int:
    t_start = time.process_time()
    rows = []
    fail = []
    for m in range(2, args.mmax + 1):
        k = 2 * m * m
        widths = odd_widths(k)
        if widths != [2 * m - 1, 2 * m + 1]:
            fail.append({"k": k, "what": f"widths {widths}"})
        for b in widths:
            p, j = choose(k, b, first_delta((b + 1) ** 2 // 2, b))
            bad = [n for n, ok in p.checks.items() if not ok]
            Bk = B_of(k, b)
            row = {"m": m, "k": k, "b": b, "w": p.w, "bound": 8 * m + 2, "B_minus_w": float(Bk - p.w),
                   "bound_minus_B": float(8 * m + 2 - Bk), "divisions": j, "failed": bad}
            if m <= args.limit_mmax:
                wl, _ = limit_waste(k, b)
                row["w_lim"] = wl
                if not wl < 8 * m + 2:
                    bad.append("w_lim not below 8m + 2")
            if bad or not below_bound(Bk, k):
                fail.append(row)
            rows.append(row)
    receipt = {
        "subcommand": "ties",
        "mmax": args.mmax,
        "pairs": len(rows),
        "failures": fail,
        "all_hold": not fail,
        "least_bound_minus_B": min(rows, key=lambda r: r["bound_minus_B"]),
        "largest_w_relative_to_bound": max(rows, key=lambda r: r["w"] - r["bound"]),
        "cpu_seconds": round(time.process_time() - t_start, 1),
        "rows_sample": rows[:20] + rows[-6:],
    }
    write(args.out, receipt)
    print(json.dumps({k_: v for k_, v in receipt.items() if k_ != "rows_sample"}, indent=1)[:2000])
    return 0 if not fail else 1


# ------------------------------------------------------------------------------ squeeze


def cmd_squeeze(args: argparse.Namespace) -> int:
    """Section 6: at k = 43218, sqrt(2k) = 294, and a squeeze k - S = b - W near 1e-7."""
    k = 43218
    out = []
    for b in odd_widths(k):
        for sq_exp in (7, 8, 9, 10, 12):
            # t with b - W(t) as close to 10^-sq_exp as a rational root approximation allows:
            # W(t) = b - e  <=>  (2b - e) t^2 - 2t - e = 0, t = (1 + sqrt(1 + e(2b - e)))/(2b - e)
            e = Q(1, 10**sq_exp)
            disc = 1 + e * (2 * b - e)
            # a rational square root of disc to 60 digits, from integers
            scale = 10**60
            r = Q(math.isqrt(int(disc * scale * scale)), scale)
            t = (1 + r) / (2 * b - e)
            a = angle(b, t)
            if not t > Q(1, b):
                continue
            p = evaluate(k, b, t)
            out.append({"b": b, "squeeze_target": f"1e-{sq_exp}", "squeeze": float(b - a.W),
                        "close": all(close(a).values()), "w": p.w, "H": float(p.H),
                        "w_below_bound": p.checks["w_below_bound"], "H_below_bound": p.checks["H_below_bound"],
                        "w_below_H": p.checks["w_below_H"]})
    # The other reading of "squeeze": t - 1/b itself.
    delta_rows = []
    for b in odd_widths(k):
        for d in (Q(1, 10**7), Q(1, 10**8)):
            t = Q(1, b) + d
            a = angle(b, t)
            p = evaluate(k, b, t)
            delta_rows.append({"b": b, "t_minus_1/b": float(d), "k_minus_S": float(k - p.S),
                               "close_fails": [n for n, ok in close(a).items() if not ok], "w": p.w,
                               "H": float(p.H), "w_below_bound": p.checks["w_below_bound"]})
    # Where the waste first reaches 1177 and 1178 as k - S grows from 1e-9 to 1e-5 (log scan).
    scan = []
    for b in odd_widths(k):
        firsts: dict[int, dict[str, Any]] = {}
        for j in range(1, 401):
            ex = -9 + 4 * j / 400
            e = Q(int(10 ** (ex + 30)), 10**30)
            disc = 1 + e * (2 * b - e)
            scale = 10**50
            t = (1 + Q(math.isqrt(int(disc * scale * scale)), scale)) / (2 * b - e)
            p = evaluate(k, b, t)
            if p.w not in firsts:
                firsts[p.w] = {"k_minus_S": float(e), "close": all(close(angle(b, t)).values()),
                               "H": float(p.H)}
        scan.append({"b": b, "first_k_minus_S_at_each_waste": firsts})
    receipt = {"subcommand": "squeeze", "k": k, "sqrt_2k": 294, "bound": 4 * 294 + 2,
               "rows_k_minus_S": out, "rows_t_minus_1/b": delta_rows, "log_scan": scan}
    write(args.out, receipt)
    for r in out + delta_rows:
        print(r)
    for r in scan:
        print(r)
    return 0


# ----------------------------------------------------------------------------- selftest


def cmd_selftest(args: argparse.Namespace) -> int:
    results: dict[str, bool] = {}
    results["odd_widths(6) == [3]"] = odd_widths(6) == [3]
    results["odd_widths(7) == [3]"] = odd_widths(7) == [3]
    results["odd_widths(8) == [3, 5]"] = odd_widths(8) == [3, 5]
    results["odd_widths(18) == [5, 7]"] = odd_widths(18) == [5, 7]
    results["odd_widths(59) == [11]"] = odd_widths(59) == [11]
    results["below_bound exact tie refused (k=43218, x=1178)"] = not below_bound(1178, 43218)
    results["below_bound 1177 at k=43218"] = below_bound(1177, 43218)
    results["below_bound negative side"] = below_bound(Q(1), 6)
    results["floor of negatives"] = fl(Q(-1, 3)) == -1 and fl(Q(-3, 1)) == -3 and fl(Q(5, 3)) == 1
    wl, _ = limit_waste(59, 11)
    results["remark's example: k=59, b=11, limit waste 44"] = wl == 44
    p, _ = choose(59, 11, first_delta(72, 11))
    results["k=59 at a chosen t: waste 44"] = p.w == 44
    # Lemma 2 fails for an even width at a suitable lift: the pairing needs odd b
    b = 10
    a = angle(b, Q(1, b) + Q(1, 10**6))
    worst = None
    for y in [a.sec * j / 400 for j in range(400)]:
        sl = sum(levels(a, y)) - (Q(b - 1, 2) + 2 * (a.W - a.s - 2 * a.tau + y * a.tau) - 1 - 2 * a.eta)
        worst = sl if worst is None or sl < worst else worst
    results["even b = 10: the odd-b Lemma 2 bound fails at some lift"] = worst is not None and worst <= 0
    # the series limit agrees with a tiny delta where no tie occurs
    k, b = 1000, 45
    wl, _ = limit_waste(k, b)
    results["limit waste equals waste at delta = 1e-40 (k=1000, b=45)"] = wl == evaluate(k, b, Q(1, b) + Q(1, 10**40)).w
    receipt = {"subcommand": "selftest", "results": results, "all_pass": all(results.values())}
    write(args.out, receipt)
    for name, ok in results.items():
        print(("ok  " if ok else "FAIL") + "  " + name)
    return 0 if all(results.values()) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("construction")
    c.add_argument("--kmin", type=int, default=6)
    c.add_argument("--kmax", type=int, default=60000)
    c.add_argument("--limit-kmax", type=int, default=20000)
    c.add_argument("--out", type=Path, required=True)
    lm = sub.add_parser("lemmas")
    lm.add_argument("--per-b", type=int, default=10)
    lm.add_argument("--out", type=Path, required=True)
    g = sub.add_parser("geometry")
    g.add_argument("--k", default="6-40,50,59,72,98,101")
    g.add_argument("--controls-at", type=lambda s: [int(v) for v in s.split(",")], default=[6, 8, 18, 40, 101])
    g.add_argument("--out", type=Path, required=True)
    sh = sub.add_parser("sharpness")
    sh.add_argument("--bmax", type=int, default=2001)
    sh.add_argument("--scan-bmax", type=int, default=61)
    sh.add_argument("--out", type=Path, required=True)
    ti = sub.add_parser("ties")
    ti.add_argument("--mmax", type=int, default=1000)
    ti.add_argument("--limit-mmax", type=int, default=1000)
    ti.add_argument("--out", type=Path, required=True)
    sq = sub.add_parser("squeeze")
    sq.add_argument("--out", type=Path, required=True)
    st = sub.add_parser("selftest")
    st.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    table: dict[str, Callable[[argparse.Namespace], int]] = {
        "construction": cmd_construction, "lemmas": cmd_lemmas, "geometry": cmd_geometry,
        "sharpness": cmd_sharpness, "ties": cmd_ties, "squeeze": cmd_squeeze, "selftest": cmd_selftest,
    }
    return table[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
