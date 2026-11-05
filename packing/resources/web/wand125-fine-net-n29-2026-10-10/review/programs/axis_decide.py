"""Decide direction r = 0 of a check2 candidate over its whole per-bin domain,
with code written for review think-1lri and nothing of the crate's.  Adapted
from the n = 28 and n = 30 review's program after re-reading it; the changes are
in the README (chiefly: the certification is an exact comparison).

Claim decided: for every centre c in [rho(a_0), L - rho(a_0)]^2 = [1/2, L - 1/2]^2
the closed axis-aligned core of side B centred at c captures at least 1.

Method (re-derived from lemma A1's mathematics, not transcribed from axis.rs):

1. F(x, y) = sum_k g_k ox_k(x) oy_k(y) over the eight images of every row
   (unmerged), with ox_k(x) = |[x - h, x + h] cap [x1_k, x2_k]|, h = B/2.  Each
   ox_k is continuous and affine between consecutive points of
   {x1_k +- h, x2_k +- h}, so on every cell of E x E, E the set of those points
   inside the domain plus the domain's two ends, F is bilinear and its minimum over
   the closed cell is at a corner.  The minimum over the domain is the minimum over
   the grid's vertices.  The whole domain is covered: lemma C1 is not used.
2. Every event and edge is an integer on the grid 1/S, S the lcm of the
   denominators, so every overlap is computed exactly in int64.
3. Each vertex value is a dot product of nonnegative terms (g_k / S^2) OX_k OY_k
   in binary64: three correctly rounded inputs, one rounded product and a K-term
   dot product in any order (BLAS) give F_hat = sum_k t_k (1 + theta_k) with
   |theta_k| <= gamma = (K+4)u / (1 - (K+4)u), u = 2^-53, every t_k >= 0 and none
   subnormal, so F >= F_hat / (1 + gamma).  The grid is certified when the least
   F_hat, read exactly as a rational, is at least 1 + gamma (an exact comparison).
4. The lowest vertices, the least vertex's D4 orbit, a random sample and the
   source's reported vertex are evaluated exactly in fractions.
5. For comparison with the source's sweep, the events of the quadrant
   [L/2, L - 1/2] are counted as lemma A1 defines them.

Usage: python3 -I axis_decide.py CANDIDATE.json[.gz] [--source-run RUN.jsonl.gz]
       [--control CONTROL.jsonl.gz] [--out FILE]
Set OPENBLAS_NUM_THREADS to limit BLAS threads.
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import random
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fine_net_exact as fx  # noqa: E402

U = F(1, 2**53)


def axis_row(path):
    if path is None:
        return None
    with gzip.open(path, "rt") as fh:
        for line in fh:
            if line.startswith("{"):
                row = json.loads(line)
                if row.get("r") == 0:
                    return row
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate", type=Path)
    ap.add_argument("--source-run", type=Path)
    ap.add_argument("--control", type=Path)
    ap.add_argument("--block", type=int, default=1024)
    ap.add_argument("--lowest", type=int, default=24)
    ap.add_argument("--sample", type=int, default=40)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    t0 = time.time()
    cand = fx.load_candidate(args.candidate)
    ims = fx.images(cand)
    h = cand.h
    lo, hi = fx.per_bin_domain(cand, 0)
    S = 1
    for q in [lo, hi, h] + [v for im in ims for v in im[:4]]:
        S = math.lcm(S, q.denominator)
    if not (cand.L + 2) * S < 2**62:
        raise SystemExit("grid too fine for int64")

    def events(axis, a, b):
        ev = {a, b}
        for im in ims:
            for e in (im[axis], im[axis + 2]):
                for p in (e - h, e + h):
                    if a <= p <= b:
                        ev.add(p)
        return sorted(ev)

    xs, ys = events(0, lo, hi), events(1, lo, hi)
    quadrant_events = len(events(0, cand.L / 2, hi))
    toint = lambda q: int(q * S)  # exact: S is a common denominator  # noqa: E731
    Xe = np.array([toint(p) for p in xs], dtype=np.int64)
    Ye = np.array([toint(p) for p in ys], dtype=np.int64)
    X1 = np.array([toint(im[0]) for im in ims], dtype=np.int64)
    Y1 = np.array([toint(im[1]) for im in ims], dtype=np.int64)
    X2 = np.array([toint(im[2]) for im in ims], dtype=np.int64)
    Y2 = np.array([toint(im[3]) for im in ims], dtype=np.int64)
    H = toint(h)
    assert all(F(int(v), S) == p for v, p in zip(Xe, xs)), "event not on the grid"
    assert all(F(int(v), S) == p for v, p in zip(Ye, ys)), "event not on the grid"
    assert F(H, S) == h
    rho = np.array([float(im[4] / (S * S)) for im in ims], dtype=np.float64)
    K = len(ims)
    gamma = (K + 4) * U / (1 - (K + 4) * U)
    least_term = min(im[4] for im in ims) / (S * S)

    def overlaps(E, A1, A2):
        return np.maximum(0, np.minimum(E[:, None] + H, A2[None, :]) - np.maximum(E[:, None] - H, A1[None, :]))

    best = (math.inf, -1, -1)
    low_pool = []
    below = {1.0005: 0, 1.001: 0, 1.002: 0, 1.005: 0}
    vertices = 0
    blk = args.block
    for i0 in range(0, len(Xe), blk):
        OX = overlaps(Xe[i0:i0 + blk], X1, X2)
        actx = OX.any(axis=0)
        W = OX.astype(np.float64) * rho[None, :]
        for j0 in range(0, len(Ye), blk):
            OY = overlaps(Ye[j0:j0 + blk], Y1, Y2)
            act = actx & OY.any(axis=0)
            Fb = W[:, act] @ OY[:, act].astype(np.float64).T
            vertices += Fb.size
            if not np.isfinite(Fb).all():
                raise SystemExit("non-finite vertex value")
            k = int(np.argmin(Fb))
            bi, bj = divmod(k, Fb.shape[1])
            if Fb[bi, bj] < best[0]:
                best = (float(Fb[bi, bj]), i0 + bi, j0 + bj)
            for thr in below:
                below[thr] += int((Fb < thr).sum())
            flat = Fb.ravel()
            m = min(args.lowest, flat.size)
            idx = np.argpartition(flat, m - 1)[:m]
            for q in idx:
                bi, bj = divmod(int(q), Fb.shape[1])
                low_pool.append((float(flat[q]), i0 + bi, j0 + bj))
        print(f"  columns {i0}..{min(i0 + blk, len(Xe)) - 1} of {len(Xe)}; least so far {best[0]:.12f}", file=sys.stderr)
    low_pool.sort()
    low_pool = low_pool[: args.lowest]
    sweep_seconds = time.time() - t0
    least_hat = F(best[0])  # the binary64 value, read exactly
    decided = least_hat >= 1 + gamma
    certified_lower = least_hat / (1 + gamma)

    def exact_at(i, j):
        return fx.axis_capture(ims, xs[i], ys[j], h)

    rng = random.Random(29)
    sample = [(rng.randrange(len(xs)), rng.randrange(len(ys))) for _ in range(args.sample)]
    checks = []
    worst_rel = F(0)
    for val, i, j in low_pool:
        e = exact_at(i, j)
        rel = abs(F(val) - e) / e
        worst_rel = max(worst_rel, rel)
        checks.append({"x": str(xs[i]), "y": str(ys[j]), "binary64": val, "exact": str(e), "exact_approx": float(e)})
    for i, j in sample:
        e = exact_at(i, j)
        OXv = overlaps(Xe[i:i + 1], X1, X2).astype(np.float64)[0]
        OYv = overlaps(Ye[j:j + 1], Y1, Y2).astype(np.float64)[0]
        val = float(np.dot(OXv * rho, OYv))
        if e:
            worst_rel = max(worst_rel, abs(F(val) - e) / e)
    least_exact = min(F(c["exact"]) for c in checks)
    least_at = next(c for c in checks if F(c["exact"]) == least_exact)
    out = {
        "candidate": str(args.candidate),
        "candidate_sha256": cand.file_sha256,
        "domain": [str(lo), str(hi)],
        "grid_denominator_S": S,
        "x_events": len(xs),
        "y_events": len(ys),
        "quadrant_events_per_axis_by_lemma_A1": quadrant_events,
        "vertices": vertices,
        "images_unmerged": K,
        "gamma_K_plus_4": float(gamma),
        "least_positive_term": float(least_term),
        "no_subnormal_term": least_term > F(2) ** -1022,
        "least_binary64": best[0],
        "least_at": [str(xs[best[1]]), str(ys[best[2]])],
        "certified_least_lower_bound": float(certified_lower),
        "decided_verified": decided,
        "vertices_below": {str(k): v for k, v in below.items()},
        "lowest_exact": checks[: min(8, len(checks))],
        "least_exact": str(least_exact),
        "least_exact_approx": float(least_exact),
        "least_exact_at": [least_at["x"], least_at["y"]],
        "exact_at_least_binary64_vertex_equals_least_exact": exact_at(best[1], best[2]) == least_exact,
        "true_minimum_bracket": [float(certified_lower), float(least_exact)],
        "worst_relative_binary64_error_seen": float(worst_rel),
        "within_gamma": worst_rel <= gamma,
    }
    Lq = cand.L
    lx, ly = F(least_at["x"]), F(least_at["y"])
    orbit = {(lx, ly), (Lq - ly, lx), (Lq - lx, Lq - ly), (ly, Lq - lx), (ly, lx), (Lq - lx, ly), (lx, Lq - ly), (Lq - ly, Lq - lx)}
    out["least_vertex_orbit_size"] = len(orbit)
    out["least_vertex_orbit_values_equal"] = all(fx.axis_capture(ims, a, b, h) == least_exact for a, b in orbit)
    out["least_vertex_orbit_in_quadrant"] = sorted([str(a), str(b)] for a, b in orbit if Lq / 2 <= a <= hi and Lq / 2 <= b <= hi)

    for label, path in (("source_run", args.source_run), ("source_control", args.control)):
        row = axis_row(path)
        if row is None:
            continue
        ax, ay = (F(v) for v in row["argmin"])
        e = fx.axis_capture(ims, ax, ay, h)
        rec = {
            "argmin": row["argmin"],
            "argmin_in_quadrant": cand.L / 2 <= ax <= hi and cand.L / 2 <= ay <= hi,
            "argmin_on_domain_edge": ax == hi or ay == hi,
            "events_vertices": [row.get("x_events"), row.get("y_events"), row.get("vertices")],
            "events_equal_lemma_A1_quadrant_count": row.get("x_events") == quadrant_events and row.get("y_events") == quadrant_events,
            "certified_bound": row["min_certified_lower_bound"],
            "verdict": row["verdict"],
            "exact_original_at_argmin": str(e),
            "exact_original_approx": float(e),
            "argmin_is_in_the_least_vertex_orbit": (ax, ay) in orbit,
        }
        if label == "source_run":
            rec["gap_exact_minus_bound"] = float(e - F(row["min_certified_lower_bound"]))
            rec["bound_le_exact"] = F(row["min_certified_lower_bound"]) <= e
        else:
            em = e * F(197, 200)
            rec["exact_197_200"] = str(em)
            rec["exact_197_200_approx"] = float(em)
            rec["exact_197_200_below_1"] = em < 1
            rec["gap_exact_minus_bound"] = float(em - F(row["min_certified_lower_bound"]))
            rec["bound_le_exact"] = F(row["min_certified_lower_bound"]) <= em
        out[label] = rec
    e = least_exact
    out["mutants_at_least_vertex"] = {
        "197/200": {"exact": float(e * F(197, 200)), "below_1": e * F(197, 200) < 1},
        "99/100": {"exact": float(e * F(99, 100)), "below_1": e * F(99, 100) < 1},
        "near_threshold_factor_1_over_least": str(1 / e),
    }
    ru = resource.getrusage(resource.RUSAGE_SELF)
    out["cpu_seconds"] = ru.ru_utime + ru.ru_stime
    out["wall_seconds"] = time.time() - t0
    out["sweep_wall_seconds"] = sweep_seconds
    text = json.dumps(out, indent=1)
    if args.out:
        args.out.write_text(text + "\n")
    print(text)
    return 0 if decided and out["within_gamma"] else 1


if __name__ == "__main__":
    sys.exit(main())
