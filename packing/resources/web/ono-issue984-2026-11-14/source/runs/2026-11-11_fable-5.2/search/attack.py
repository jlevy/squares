#!/usr/bin/env python3
"""Phase-3 attack drivers. Every driver starts from the published record packings (loaded by
witness_io) or from seeds derived from them, optimises with opt.py, and writes any packing whose
float side is below the record to work/cand/. Nothing here decides what counts as a result:
candidates still have to pass certify.py + verify.py (make_cert.py).

Sub-commands
  delone   : for each target n, delete each single square of the (n+1)-record and re-polish
  unl      : approximate "un-L" transfer from the ((k+1)^2+j)-record to n = k^2+j
  hop      : basin hopping around a seed packing
"""
import argparse
import json
import math
import multiprocessing as mp
import os
import sys
import time
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from opt import penalty_min, polish  # noqa: E402
from sqgeom import energy_grad, max_violation, normalize  # noqa: E402

_W = None
_R = None


def W():
    global _W
    if _W is None:
        _W = json.load(open(os.path.join(RUN, "work", "witness_float.json")))
    return _W


def R():
    global _R
    if _R is None:
        _R = {r["n"]: r for r in json.load(open(os.path.join(RUN, "records.json")))["records"]}
    return _R


def rec(n):
    return float(F(R()[n]["upper"]))


def wit(n):
    w = W()[str(n)]
    return w["side"], np.array(w["x"]), np.array(w["y"]), np.array(w["th"])


def save_cand(n, S, x, y, th, tag, extra=None):
    d = os.path.join(RUN, "work", "cand")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"n{n}_S{S:.10f}_{tag}.json")
    json.dump(dict(n=n, S=S, x=list(map(float, x)), y=list(map(float, y)), th=list(map(float, th)), tag=tag, extra=extra),
              open(p, "w"))
    return p


def log_attempt(n, method, best_float_S, certified_S, wall_seconds, note):
    recd = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "n": n, "method": method,
            "best_float_S": best_float_S, "certified_S": certified_S,
            "wall_seconds": round(wall_seconds, 1), "note": note}
    with open(os.path.join(RUN, "attempts.jsonl"), "a") as f:
        f.write(json.dumps(recd) + "\n")


def descend(x, y, th, S, mus, maxiter=2500):
    for mu in mus:
        x, y, th, S, E = penalty_min(x, y, th, S, mu, maxiter=maxiter)
    return x, y, th, S


def local_opt(x, y, th, S, mus=(200.0, 2000.0, 20000.0), delta=0.03):
    """penalty continuation then exact polish; returns (x, y, th, S) strictly feasible in floats, or None."""
    if mus:
        x, y, th, S = descend(x, y, th, S, mus)
        S = S + 2e-3
    x, y, th, S, V, info = polish(x, y, th, S=S, delta=delta)
    if V > 1e-10:
        return None
    return x, y, th, S


# ------------------------------------------------------------------ delone
def _delone_task(args):
    n, i0, i1 = args
    S, x, y, th = wit(n + 1)
    out = []
    for i in range(i0, i1):
        keep = np.ones(n + 1, bool); keep[i] = False
        try:
            r = polish(x[keep], y[keep], th[keep], S=S, delta=0.03)
        except Exception as e:  # noqa: BLE001
            out.append((i, None, str(e))); continue
        if r[4] > 1e-10:
            out.append((i, None, "viol")); continue
        out.append((i, r[3], None))
        if r[3] < rec(n) - 1e-9:
            save_cand(n, r[3], r[0], r[1], r[2], f"delone_from{n+1}_sq{i}")
    return n, out


def cmd_delone(a):
    targets = []
    for n in range(a.nmin, a.nmax + 1):
        if n + 1 not in R() or R()[n]["proven_optimal"]:
            continue
        if abs(rec(n + 1) - round(rec(n + 1))) < 1e-12:      # (n+1)-record is a plain grid: nothing to gain
            continue
        if rec(n + 1) - rec(n) > a.maxstep:
            continue
        targets.append(n)
    tasks = []
    for n in targets:
        ch = max(1, (n + 1) // 8)
        for i0 in range(0, n + 1, ch):
            tasks.append((n, i0, min(n + 1, i0 + ch)))
    print(f"delone: {len(targets)} targets, {len(tasks)} tasks", flush=True)
    t0 = time.time()
    res = {}
    left = {}
    for n, i0, i1 in tasks:
        left[n] = left.get(n, 0) + 1
    outp = os.path.join(RUN, "work", "delone_results.jsonl")

    def report(n):
        vals = [s for _, s, _ in res[n] if s is not None]
        best = min(vals) if vals else None
        nfail = sum(1 for _, s, _ in res[n] if s is None)
        gain = None if best is None else rec(n) - best
        flag = "  <<< BELOW RECORD" if gain is not None and gain > 1e-9 else ""
        nmoved = sum(1 for v in vals if v < rec(n + 1) - 1e-7)
        print(f"[{time.time()-t0:6.0f}s] n={n:3d} rec={rec(n):.9f} rec(n+1)={rec(n+1):.9f} best after deleting one={best} "
              f"(needs {rec(n+1)-rec(n):.5f}, got {None if best is None else round(rec(n+1)-best,7)}; {nmoved}/{len(vals)} deletions compress at all) fails={nfail}{flag}", flush=True)
        with open(outp, "a") as f:
            f.write(json.dumps(dict(n=n, rec=rec(n), rec_next=rec(n + 1), best=best, nmoved=nmoved, tried=len(vals), fails=nfail,
                                    per_square=[(i, s) for i, s, _ in sorted(res[n])])) + "\n")
        log_attempt(n, "delone: delete each single square of the published (n+1)-record, exact SLP polish (search/attack.py delone)",
                    best, None, (time.time() - t0),
                    f"{len(vals)} deletions tried from n+1={n+1} (S={rec(n+1):.9f}); best compresses by "
                    f"{None if best is None else round(rec(n+1)-best,9)}, record needs {rec(n+1)-rec(n):.6f}; "
                    + ("BELOW RECORD, see work/cand" if flag else "no improvement"))

    with mp.Pool(a.procs) as pool:
        for n, out in pool.imap_unordered(_delone_task, tasks):
            res.setdefault(n, []).extend(out)
            left[n] -= 1
            if left[n] == 0:
                report(n)
    print("wall %.1fs" % (time.time() - t0), flush=True)


# ------------------------------------------------------------------ helpers for seeds
def overlap_energy_per_square(x, y, th, S):
    """Per-square share of the penalty energy (used to pick squares to drop)."""
    n = len(x)
    e = np.zeros(n)
    from sqgeom import pair_sep
    for i in range(n):
        for j in range(i + 1, n):
            dx = x[j] - x[i]; dy = y[j] - y[i]
            if dx * dx + dy * dy >= 2.0:
                continue
            sep, k, sg = pair_sep(x[i], y[i], th[i], x[j], y[j], th[j])
            if sep < 0:
                e[i] += sep * sep; e[j] += sep * sep
    h = 0.5 * (np.abs(np.cos(th)) + np.abs(np.sin(th)))
    for arr in (h - x, x + h - S, h - y, y + h - S):
        v = np.maximum(arr, 0.0)
        e += v * v
    return e


def largest_holes(x, y, S, rng, m=3000, top=10):
    px = rng.uniform(0.5, S - 0.5, m); py = rng.uniform(0.5, S - 0.5, m)
    d2 = ((px[:, None] - x[None, :]) ** 2 + (py[:, None] - y[None, :]) ** 2).min(axis=1)
    o = np.argsort(-d2)[:top]
    return px[o], py[o]


def fix_count(x, y, th, S, n, rng):
    """Drop the most-overlapping squares / add squares in the largest holes until exactly n."""
    x = list(x); y = list(y); th = list(th)
    while len(x) > n:
        e = overlap_energy_per_square(np.array(x), np.array(y), np.array(th), S)
        if e.max() <= 0:
            i = int(rng.integers(len(x)))
        else:
            i = int(np.argmax(e))
        del x[i], y[i], th[i]
    while len(x) < n:
        px, py = largest_holes(np.array(x), np.array(y), S, rng)
        k = int(rng.integers(min(3, len(px))))
        x.append(px[k]); y.append(py[k]); th.append(rng.choice([0.0, rng.uniform(-0.78, 0.78)]))
    return np.array(x), np.array(y), np.array(th)


# ------------------------------------------------------------------ unl : (k+1)^2+j  ->  k^2+j
def unl_seed(src, n, c, d, rng):
    S, x, y, th = wit(src)
    inv = (x >= c) & (x < c + 1.0)
    inh = (y >= d) & (y < d + 1.0)
    keep = ~(inv | inh)
    x2 = x[keep].copy(); y2 = y[keep].copy(); t2 = th[keep].copy()
    x2[x2 >= c + 1.0] -= 1.0
    y2[y2 >= d + 1.0] -= 1.0
    S2 = S - 1.0
    x2, y2, t2 = fix_count(x2, y2, t2, S2, n, rng)
    return x2, y2, t2, S2


def _unl_task(args):
    src, n, c, d, seed = args
    rng = np.random.default_rng(seed)
    t0 = time.time()
    try:
        x, y, th, S = unl_seed(src, n, c, d, rng)
        r = local_opt(x, y, th, S + 0.05)
    except Exception as e:  # noqa: BLE001
        return (src, n, c, d, None, str(e), time.time() - t0)
    if r is None:
        return (src, n, c, d, None, "polish failed", time.time() - t0)
    p = None
    if r[3] < rec(n) + 0.03:
        p = save_cand(n, r[3], r[0], r[1], r[2], f"unl_from{src}_c{c:.2f}_d{d:.2f}") if r[3] < rec(n) - 1e-9 else \
            _save_seed(n, r[3], r[0], r[1], r[2], f"unl_from{src}_c{c:.2f}_d{d:.2f}")
    return (src, n, c, d, r[3], p, time.time() - t0)


def _save_seed(n, S, x, y, th, tag):
    d = os.path.join(RUN, "work", "seeds")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"n{n}_S{S:.8f}_{tag}.json")
    json.dump(dict(n=n, S=S, x=list(map(float, x)), y=list(map(float, y)), th=list(map(float, th)), tag=tag), open(p, "w"))
    return p


def cmd_unl(a):
    tasks = []
    targets = [int(t) for t in a.targets.split(",")] if a.targets else None
    for n in (targets or range(a.nmin, a.nmax + 1)):
        if R()[n]["proven_optimal"]:
            continue
        k = math.floor(rec(n) + 1e-12)
        src = n + 2 * k + 1
        if src not in R() or abs(rec(src) - round(rec(src))) < 1e-12:
            continue
        if rec(src) - 1.0 >= rec(n) - 1e-9:
            continue                      # no margin: the source is just the L-extension
        Ssrc = rec(src)
        cs = np.arange(0.0, Ssrc - 0.999, a.step)
        if a.corner:      # only strips within 1.5 of either end of the side (natural for diagonal-band packings)
            cs = np.array([c for c in cs if c <= 1.5 or c >= Ssrc - 2.5])
        for c in cs:
            for d in cs:
                tasks.append((src, n, float(c), float(d), int(1000 * c + 7 * d + n)))
    rngm = np.random.default_rng(0)
    rngm.shuffle(tasks)
    print(f"unl: {len(tasks)} tasks", flush=True)
    t0 = time.time()
    best = {}
    cnt = {}
    tsum = {}
    with mp.Pool(a.procs) as pool:
        for (src, n, c, d, S, p, dt) in pool.imap_unordered(_unl_task, tasks, chunksize=2):
            cnt[n] = cnt.get(n, 0) + 1
            tsum[n] = tsum.get(n, 0.0) + dt
            if S is not None and (n not in best or S < best[n][0]):
                best[n] = (S, src, c, d)
                print(f"[{time.time()-t0:7.0f}s] n={n} from {src} c={c:.2f} d={d:.2f}: S={S:.9f}  record {rec(n):.9f}  "
                      f"(loss vs S_src-1: {S-(rec(src)-1):+.5f}, margin {rec(n)-(rec(src)-1):.5f})"
                      + ("  <<< BELOW RECORD" if S < rec(n) - 1e-9 else ""), flush=True)
    for n in sorted(cnt):
        b = best.get(n)
        log_attempt(n, "unl: approximate un-L transfer (delete a unit row+column from the published record at n+2k+1, "
                       "close up, fix the count, penalty continuation + SLP polish) (search/attack.py unl)",
                    b[0] if b else None, None, tsum[n],
                    f"{cnt[n]} (c,d) offsets from source n={n+2*math.floor(rec(n)+1e-12)+1}; best float S={b[0] if b else None} vs record {rec(n):.9f}; "
                    + ("BELOW RECORD, see work/cand" if b and b[0] < rec(n) - 1e-9 else "no improvement"))
    print("wall %.1fs" % (time.time() - t0))


# ------------------------------------------------------------------ lins : (k-1)^2+j-1  ->  k^2+j
def lins_seed(src, n, c, d, rng):
    """Approximate L-insertion: cut the source record at x=c and y=d, move the far parts out by 1,
    fill the cross with axis-aligned squares, then add the missing square(s) in the largest holes."""
    S, x, y, th = wit(src)
    x2 = x.copy(); y2 = y.copy(); t2 = th.copy()
    x2[x >= c] += 1.0
    y2[y >= d] += 1.0
    S2 = S + 1.0
    xs, ys = [c + 0.5], [d + 0.5]
    v = 0.5
    while v + 0.5 <= d + 1e-9:
        xs.append(c + 0.5); ys.append(v); v += 1.0
    v = d + 1.5
    while v + 0.5 <= S2 + 1e-9:
        xs.append(c + 0.5); ys.append(v); v += 1.0
    v = 0.5
    while v + 0.5 <= c + 1e-9:
        xs.append(v); ys.append(d + 0.5); v += 1.0
    v = c + 1.5
    while v + 0.5 <= S2 + 1e-9:
        xs.append(v); ys.append(d + 0.5); v += 1.0
    x2 = np.concatenate([x2, xs]); y2 = np.concatenate([y2, ys]); t2 = np.concatenate([t2, np.zeros(len(xs))])
    x2, y2, t2 = fix_count(x2, y2, t2, S2, n, rng)
    return x2, y2, t2, S2


def _transfer_task(args):
    kind, src, n, c, d, seed = args
    rng = np.random.default_rng(seed)
    t0 = time.time()
    try:
        if kind == "unl":
            x, y, th, S = unl_seed(src, n, c, d, rng)
        else:
            x, y, th, S = lins_seed(src, n, c, d, rng)
        r = local_opt(x, y, th, S + 0.05)
    except Exception as e:  # noqa: BLE001
        return (kind, src, n, c, d, None, None, time.time() - t0)
    if r is None:
        return (kind, src, n, c, d, None, None, time.time() - t0)
    return (kind, src, n, c, d, r[3], (r[0].tolist(), r[1].tolist(), r[2].tolist()), time.time() - t0)


def cmd_sweep(a):
    """Transfer sweep over many targets: unl (from n+2k+1) and lins (from n-2k), coarse offsets."""
    tasks = []
    info = {}
    targets = [int(t) for t in a.targets.split(",")] if a.targets else range(a.nmin, a.nmax + 1)
    for n in targets:
        if R()[n]["proven_optimal"] or abs(rec(n) - round(rec(n))) < 1e-12:
            continue
        k = math.floor(rec(n) + 1e-12)
        for kind in a.kinds.split(","):
            src = n + 2 * k + 1 if kind == "unl" else n - 2 * k
            if src not in R() or src < 5 or abs(rec(src) - round(rec(src))) < 1e-12:
                continue
            base = rec(src) - 1.0 if kind == "unl" else rec(src) + 1.0
            margin = rec(n) - base
            if margin < a.minmargin:
                continue
            Ssrc = rec(src)
            hi = Ssrc - 0.999 if kind == "unl" else Ssrc + 1e-9
            cs = np.arange(0.0, hi, a.step)
            pairs = [(float(c), float(d)) for c in cs for d in cs]
            if a.maxpairs and len(pairs) > a.maxpairs:
                rr = np.random.default_rng(n)
                pairs = [pairs[i] for i in rr.choice(len(pairs), a.maxpairs, replace=False)]
            for (c, d) in pairs:
                tasks.append((kind, src, n, c, d, int(1000 * c + 7 * d + n)))
            info[(n, kind)] = (src, margin, len(pairs))
    rngm = np.random.default_rng(0)
    rngm.shuffle(tasks)
    print(f"sweep: {len(tasks)} tasks over {len(info)} (target, kind) pairs", flush=True)
    t0 = time.time()
    best = {}
    cnt = {}
    tsum = {}
    with mp.Pool(a.procs) as pool:
        for (kind, src, n, c, d, S, cfg, dt) in pool.imap_unordered(_transfer_task, tasks, chunksize=2):
            key = (n, kind)
            cnt[key] = cnt.get(key, 0) + 1
            tsum[key] = tsum.get(key, 0.0) + dt
            if S is not None and S < rec(n) + a.keep:
                _save_seed(n, S, cfg[0], cfg[1], cfg[2], f"{kind}_from{src}_c{c:.2f}_d{d:.2f}")
            if S is not None and (key not in best or S < best[key][0]):
                best[key] = (S, src, c, d)
                tag = f"{kind}_from{src}_c{c:.2f}_d{d:.2f}"
                if S < rec(n) - 1e-9:
                    save_cand(n, S, cfg[0], cfg[1], cfg[2], tag)
                print(f"[{time.time()-t0:7.0f}s] n={n} {kind} from {src} c={c:.2f} d={d:.2f}: S={S:.9f} record {rec(n):.9f} "
                      f"gap {S-rec(n):+.5f} (margin was {info[key][1]:.4f})" + ("  <<< BELOW RECORD" if S < rec(n) - 1e-9 else ""), flush=True)
            if cnt[key] == info[key][2]:
                b = best.get(key)
                log_attempt(n, f"{kind}: approximate " + ("un-L transfer (delete a unit row+column from the published record at n+2k+1, close up"
                               if kind == "unl" else "L-insertion transfer (cut the published record at n-2k, open a unit cross, fill it")
                               + ", fix the count, penalty continuation + SLP polish) (search/attack.py sweep)",
                            b[0] if b else None, None, tsum[key],
                            f"{cnt[key]} (c,d) offsets from source n={info[key][0]}; best float S={b[0] if b else None} vs record {rec(n):.9f}; "
                            + ("BELOW RECORD, see work/cand" if b and b[0] < rec(n) - 1e-9 else "no improvement"))
    print("sweep summary (gap = best S - record):", flush=True)
    for key in sorted(best, key=lambda q: best[q][0] - rec(q[0])):
        print(f"  n={key[0]} {key[1]}: gap {best[key][0]-rec(key[0]):+.5f}  S={best[key][0]:.7f} from {best[key][1]} c={best[key][2]} d={best[key][3]}", flush=True)
    print("wall %.1fs" % (time.time() - t0), flush=True)


# ------------------------------------------------------------------ hop : basin hopping
def perturb(x, y, th, S, rng, kinds=None):
    n = len(x)
    x = x.copy(); y = y.copy(); th = th.copy()
    kind = rng.choice(kinds or ["reseat", "jiggle", "cluster", "blocktilt", "straighten", "remelt"])
    if kind in ("attach", "detach", "swapcell"):
        # polyomino moves on the tilted lattice: convert a straight square into a lattice cell next to a
        # tilted square (attach), straighten a weakly attached tilted square (detach), or do both (swapcell)
        tn = (th + np.pi / 4) % (np.pi / 2) - np.pi / 4
        tilted = np.abs(tn) > 0.03
        did = False
        if tilted.any() and (~tilted).any():
            if kind in ("attach", "swapcell"):
                for _try in range(12):
                    t = int(rng.choice(np.where(tilted)[0]))
                    c, sn = math.cos(th[t]), math.sin(th[t])
                    dirs = [(c, sn), (-c, -sn), (-sn, c), (sn, -c)]
                    dx, dy = dirs[int(rng.integers(4))]
                    px, py = x[t] + dx, y[t] + dy
                    h = 0.5 * (abs(c) + abs(sn))
                    if not (h - 0.1 <= px <= S - h + 0.1 and h - 0.1 <= py <= S - h + 0.1):
                        continue
                    d2 = (x - px) ** 2 + (y - py) ** 2
                    if np.any(tilted & (d2 < 0.45)):
                        continue
                    cand = np.where(~tilted)[0]
                    j = int(cand[np.argmin(d2[cand])])
                    if d2[j] > 3.0:
                        continue
                    x[j] = px; y[j] = py; th[j] = th[t]
                    tilted[j] = True
                    did = True
                    break
            if kind in ("detach", "swapcell"):
                idx = np.where(tilted)[0]
                if len(idx) > 1:
                    nb = np.array([np.count_nonzero(tilted & ((x - x[i]) ** 2 + (y - y[i]) ** 2 < 1.3)) - 1 for i in idx])
                    weak = idx[nb <= max(1, int(nb.min()) + 1)]
                    j = int(rng.choice(weak))
                    th[j] = 0.0
                    did = True
        if not did:
            kind = "jiggle"
    if kind in ("attach", "detach", "swapcell"):
        pass
    elif kind == "reseat":
        k = int(rng.integers(1, 3))
        idx = rng.choice(n, k, replace=False)
        px, py = largest_holes(np.delete(x, idx), np.delete(y, idx), S, rng, m=1500, top=8)
        for q, i in enumerate(idx):
            j = int(rng.integers(len(px)))
            x[i] = px[j]; y[i] = py[j]; th[i] = rng.choice([0.0, np.pi / 4, rng.uniform(-0.78, 0.78)])
    elif kind == "jiggle":
        sig = rng.choice([0.01, 0.03, 0.08])
        x += rng.normal(0, sig, n); y += rng.normal(0, sig, n); th += rng.normal(0, sig, n)
    elif kind == "cluster":
        c = int(rng.integers(n))
        d2 = (x - x[c]) ** 2 + (y - y[c]) ** 2
        idx = np.argsort(d2)[: int(rng.integers(3, 10))]
        x[idx] += rng.normal(0, 0.25, len(idx)); y[idx] += rng.normal(0, 0.25, len(idx))
        th[idx] += rng.normal(0, 0.3, len(idx))
    elif kind == "blocktilt":            # rotate a rectangular block rigidly
        cx, cy = rng.uniform(1, S - 1), rng.uniform(1, S - 1)
        wx, wy = rng.uniform(1.0, 3.5), rng.uniform(1.0, 3.5)
        idx = np.where((np.abs(x - cx) < wx) & (np.abs(y - cy) < wy))[0]
        if len(idx):
            phi = rng.choice([-1, 1]) * rng.uniform(0.05, 0.6)
            c, s = math.cos(phi), math.sin(phi)
            dx, dy = x[idx] - cx, y[idx] - cy
            x[idx] = cx + c * dx - s * dy; y[idx] = cy + s * dx + c * dy; th[idx] += phi
    elif kind == "straighten":           # set a local group to a common angle (0 or the group mean)
        c = int(rng.integers(n))
        d2 = (x - x[c]) ** 2 + (y - y[c]) ** 2
        idx = np.argsort(d2)[: int(rng.integers(2, 9))]
        th[idx] = 0.0 if rng.random() < 0.6 else th[c]
    else:                                 # remelt a disc
        cx, cy = rng.uniform(0, S), rng.uniform(0, S)
        rad = rng.uniform(1.2, 3.0)
        idx = np.where((x - cx) ** 2 + (y - cy) ** 2 < rad * rad)[0]
        if len(idx):
            x[idx] += rng.normal(0, 0.35, len(idx)); y[idx] += rng.normal(0, 0.35, len(idx))
            th[idx] = rng.uniform(-np.pi / 4, np.pi / 4) + rng.normal(0, 0.1, len(idx)) if rng.random() < 0.5 \
                else rng.uniform(-np.pi / 4, np.pi / 4, len(idx))
    return x, y, th, kind


MOVESETS = {
    "poly": ["attach", "attach", "detach", "swapcell", "swapcell", "jiggle", "cluster", "straighten", "reseat", "blocktilt"],
    "polyonly": ["attach", "detach", "swapcell", "swapcell", "jiggle"],
}


def _best_elite(n, share):
    """Best saved seed for n whose file name contains `share` (chains exchange their best states through work/seeds)."""
    import glob
    import re
    best = None
    for f in glob.glob(os.path.join(RUN, "work", "seeds", f"n{n}_S*{share}*.json")):
        m = re.search(r"_S([0-9.]+)_", os.path.basename(f))
        if m and (best is None or float(m.group(1)) < best[0]):
            best = (float(m.group(1)), f)
    return best


def _hop_task(args):
    n, seedfile, seed, tlimit, temp, tag, share = args
    rng = np.random.default_rng(seed)
    if seedfile.startswith("wit:"):
        # "wit:N"  = published record of N as is;  "wit:N:del" = record of N with one random square deleted, re-polished
        parts = seedfile.split(":")
        Sw, xw, yw, tw = wit(int(parts[1]))
        if len(parts) > 2 and parts[2] == "del":
            # optional explicit candidates: "wit:N:del:i1,i2,..." (each chain picks one of them)
            cands = [int(v) for v in parts[3].split(",")] if len(parts) > 3 and parts[3] else None
            for _try in range(20):
                i = int(rng.choice(cands)) if cands else int(rng.integers(len(xw)))
                keep = np.ones(len(xw), bool); keep[i] = False
                r = polish(xw[keep], yw[keep], tw[keep], S=Sw, delta=0.03)
                if r[4] <= 1e-10:
                    cur = (r[0], r[1], r[2], r[3])
                    break
        else:
            r = polish(xw, yw, tw, S=Sw, delta=0.003)
            cur = (r[0], r[1], r[2], r[3])
    else:
        d = json.load(open(seedfile))
        cur = (np.array(d["x"]), np.array(d["y"]), np.array(d["th"]), float(d["S"]))
    assert len(cur[0]) == n, (len(cur[0]), n)
    best = cur
    t0 = time.time()
    nloc = 0
    stats = {}
    record = rec(n)
    last_report = t0
    while time.time() - t0 < tlimit:
        px, py, pt, kind = perturb(cur[0], cur[1], cur[2], cur[3], rng, kinds=MOVESETS.get(os.environ.get("SQ_MOVES", ""), None))
        try:
            cand = local_opt(px, py, pt, cur[3] + 0.02)
        except Exception:  # noqa: BLE001
            cand = None
        nloc += 1
        st = stats.setdefault(kind, [0, 0, 0])
        st[0] += 1
        if cand is None:
            continue
        dS = cand[3] - cur[3]
        if dS < -1e-9:
            st[1] += 1
        if dS < 1e-9 or rng.random() < math.exp(-dS / temp):
            cur = cand
            st[2] += 1
        if cur[3] < best[3] - 1e-9:
            best = cur
            _save_seed(n, best[3], best[0], best[1], best[2], f"hop_{tag}_s{seed}")
            if best[3] < record - 1e-9:
                save_cand(n, best[3], best[0], best[1], best[2], f"hop_{tag}_s{seed}")
        if share and nloc % 25 == 0:
            el = _best_elite(n, share)
            if el is not None and el[0] < cur[3] - 1e-6:
                try:
                    dd = json.load(open(el[1]))
                    if len(dd["x"]) == n:
                        cur = (np.array(dd["x"]), np.array(dd["y"]), np.array(dd["th"]), float(dd["S"]))
                        if cur[3] < best[3]:
                            best = cur
                        stats.setdefault("migrate", [0, 0, 0])[0] += 1
                except Exception:  # noqa: BLE001
                    pass
        if time.time() - last_report > 120:
            last_report = time.time()
            print(f"  [hop n={n} seed={seed} t={time.time()-t0:.0f}s] cur={cur[3]:.7f} best={best[3]:.7f} rec={record:.7f} nloc={nloc} {stats}", flush=True)
    return dict(n=n, seed=seed, best=best[3], nloc=nloc, stats=stats, t=time.time() - t0, seedfile=os.path.basename(seedfile))


def cmd_hop(a):
    import glob as _glob
    if a.seedfile.startswith("wit:"):
        files = [a.seedfile]
    else:
        files = []
        for part in a.seedfile.split(","):
            files.extend(sorted(_glob.glob(part)) if any(ch in part for ch in "*?[") else [part])
        files = files[: a.maxseeds] if a.maxseeds else files
    print(f"hop n={a.n}: {a.procs} chains over {len(files)} seed file(s)", flush=True)
    tasks = [(a.n, files[i % len(files)], a.seed * 100 + i, a.time, a.temp, a.tag, a.share) for i in range(a.procs)]
    t0 = time.time()
    with mp.Pool(a.procs) as pool:
        res = pool.map(_hop_task, tasks)
    best = min(r["best"] for r in res)
    for r in sorted(res, key=lambda r: r["best"]):
        print(f"seed {r['seed']}: best={r['best']:.9f} nloc={r['nloc']} from {r['seedfile']} stats={r['stats']}")
    print(f"n={a.n} best {best:.9f} record {rec(a.n):.9f} wall {time.time()-t0:.0f}s")
    log_attempt(a.n, f"hop: basin hopping (moves: reseat/jiggle/cluster/blocktilt/straighten/remelt; penalty continuation + SLP polish) "
                     f"from seed {os.path.basename(a.seedfile)} (search/attack.py hop)",
                best, None, time.time() - t0,
                f"{a.procs} chains x {a.time:.0f}s, temp={a.temp}, {sum(r['nloc'] for r in res)} local optimisations; record {rec(a.n):.9f}; "
                + ("BELOW RECORD, see work/cand" if best < rec(a.n) - 1e-9 else "no improvement"))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("delone"); p.add_argument("--nmin", type=int, default=26); p.add_argument("--nmax", type=int, default=323)
    p.add_argument("--maxstep", type=float, default=1.0); p.add_argument("--procs", type=int, default=8); p.set_defaults(f=cmd_delone)
    p = sub.add_parser("unl"); p.add_argument("--nmin", type=int, default=26); p.add_argument("--nmax", type=int, default=160)
    p.add_argument("--targets", default=""); p.add_argument("--step", type=float, default=1.0)
    p.add_argument("--corner", action="store_true")
    p.add_argument("--procs", type=int, default=8); p.set_defaults(f=cmd_unl)
    p = sub.add_parser("sweep"); p.add_argument("--nmin", type=int, default=26); p.add_argument("--nmax", type=int, default=160)
    p.add_argument("--targets", default=""); p.add_argument("--kinds", default="unl,lins"); p.add_argument("--step", type=float, default=1.0)
    p.add_argument("--minmargin", type=float, default=0.02); p.add_argument("--maxpairs", type=int, default=0)
    p.add_argument("--keep", type=float, default=0.03); p.add_argument("--procs", type=int, default=8); p.set_defaults(f=cmd_sweep)
    p = sub.add_parser("hop"); p.add_argument("n", type=int); p.add_argument("seedfile"); p.add_argument("--time", type=float, default=600)
    p.add_argument("--procs", type=int, default=8); p.add_argument("--seed", type=int, default=1); p.add_argument("--temp", type=float, default=0.003)
    p.add_argument("--maxseeds", type=int, default=0)
    p.add_argument("--tag", default="x"); p.add_argument("--share", default="", help="exchange best states among chains whose seed files contain this text")
    p.set_defaults(f=cmd_hop)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
