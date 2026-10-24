#!/usr/bin/env python3
"""The issue 755 packing measured pose by pose against the packings the record holds at 303.

Written for the stage 4 review of T-238 (bead think-jdz0). Decides nothing: whether two
certificates are the same packing is not decided here; how far apart they lie is measured.

For each reference, read from its retained file in the repository at REF, the eight
symmetries of the box are applied to the reference in its own box. Under each, an
assignment of this certificate's squares to the reference's is found that minimizes the
total squared centre displacement (this program's own Hungarian algorithm, held by
`--self-test` to scipy's `linear_sum_assignment` and to brute force), and the symmetry with
the least total is reported with:

- whether nearest centres pair the squares one to one;
- how many squares lie within 1e-9, 1e-6, 1e-3 and 1e-2 of their partner, and beyond 1e-2,
  0.1 and 0.5, decided exactly over the rationals;
- the largest and the RMS move, and the bottleneck (the least possible largest move over
  all assignments, this program's own threshold search with augmenting paths);
- how many squares turn by more than 1 degree modulo 90, and how many tilts beyond 1
  degree reverse their sign.

Against T-230 it also reports the assignment that minimizes the total (unsquared) move,
for the issue's figures, and compares the two contact graphs through the assignment: a
contact is a pair whose exact separating-axis gap (route Z of `review_t238_check.py`) is
below 1e-10, or a wall clearance below 1e-10; both certificates are 1e-12 dilations, so
every contact appears as a gap of about 1e-12.

Usage:
  python3 -I identity_t238.py CERT --checker review_t238_check.py --repo /home/user/squares \
      --ref REF --out OUT.json
  python3 -I identity_t238.py --self-test
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import io
import itertools
import json
import math
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np
import yaml

WEB = "packing/resources/web/"
REFERENCES = [
    ("T-230, Daniel (#728), the house", "cert", WEB + "evand-n303-2026-10-22/source/search/packer/candidates/s303_r303w0.cert"),
    ("W-known-best-n303, the house witness", "fact", "packing/witnesses/known-best/n-303.yaml"),
    ("T-186, Polkovskyi (70a033f)", "fact", WEB + "mishapolk-kkt-refinements-2026-10-14/facts/n-303.yaml.gz"),
    ("T-174, PingYou Ltd (PR #574)", "fact", WEB + "pingyou-pr574-certificates-2026-10-13/facts/n-303.yaml.gz"),
    ("#593, Polkovskyi", "fact", WEB + "mishapolk-records-2026-10-14/facts/n-303.yaml.gz"),
    ("T-162, Ostashev (#562)", "sqcert", WEB + "dostashev-compositions-2026-10-12/source/records/n0303.sqcert"),
    ("T-146, Daniel's regularized lists", "cert", WEB + "evand-regularized-2026-10-10/source/search/regularize/lists/certs/n-303.cert.gz"),
    ("T-136, SQUISH (#481)", "fact", WEB + "squish-481-third-request-2026-10-09/facts/n-303.yaml.gz"),
    ("#573, Polkovskyi", "fact", WEB + "mishapolk-exact-certificates-2026-10-12/facts/n-303.yaml.gz"),
    ("#488, Couzo", "cert", WEB + "couzo-certificates-2026-10-10/source/certificates/n303.cert"),
    ("T-134, Couzo (#476)", "cert", WEB + "couzo-exact-certificates-2026-10-09/source/certificates/n303.cert"),
    ("T-138, Polkovskyi (#470)", "fact", WEB + "mishapolk-decimal-poses-2026-10-09/facts/n-303.yaml.gz"),
    ("T-113, SQUISH (#401)", "json", WEB + "squish-401-2026-10-07/facts/n-303.json.gz"),
    ("T-098, Daniel's exact optima (#375)", "cert", WEB + "evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-303.cert"),
]
SYMMETRIES = ("identity", "rot90", "rot180", "rot270", "mirror-x", "mirror-y", "transpose", "anti-transpose")


# --- readers: poses as exact centres and an angle in degrees -----------------------------


def basis_of_t(t: Q) -> tuple[Q, Q]:
    w = 1 + t * t
    return (1 - t * t) / w, 2 * t / w


def poses_from_text(kind: str, raw: bytes) -> tuple[Q, list[tuple[Q, Q, float]]]:
    if kind == "cert":
        lines = [ln for ln in raw.decode().splitlines() if ln.strip() and not ln.startswith("#")]
        n, s = lines[0].split()
        rows = [ln.split() for ln in lines[1:]]
        out = []
        for x, y, t in rows:
            c, sn = basis_of_t(Q(t))
            out.append((Q(x), Q(y), math.degrees(math.atan2(float(sn), float(c)))))
        assert len(out) == int(n)
        return Q(s), out
    if kind == "sqcert":
        lines = [ln for ln in raw.decode().splitlines() if ln.strip() and not ln.startswith("#")]
        assert lines[0] == "n 303" and lines[1].startswith("s ")
        side = Q(lines[1][2:])
        out = []
        for ln in lines[2:]:
            x, y, t = ln.split()
            c, sn = basis_of_t(Q(t))
            out.append((Q(x), Q(y), math.degrees(math.atan2(float(sn), float(c)))))
        assert len(out) == 303
        return side, out
    if kind == "json":
        d = json.loads(raw)
        out = []
        for sq in d["squares"]:
            c, sn = basis_of_t(Q(sq["t"]))
            out.append((Q(sq["x"]), Q(sq["y"]), math.degrees(math.atan2(float(sn), float(c)))))
        return Q(d["side"]), out
    if kind == "fact":
        doc = yaml.safe_load(raw)
        w = doc["witness"]
        assert w["n"] == 303
        out = []
        for sq in w["squares"]:
            x, y = (Q(str(v)) for v in sq["center"])
            if w["representation"] == "center-basis":
                c, sn = (Q(str(v)) for v in sq["basis"])
                deg = math.degrees(math.atan2(float(sn), float(c)))
            else:
                ang = float(sq["angle"])
                deg = math.degrees(ang) if w["coordinates"]["angle_unit"] == "radians" else ang
            out.append((x, y, deg))
        return Q(str(w["side"])), out
    raise ValueError(kind)


def show(repo: str, ref: str, path: str) -> bytes:
    data = subprocess.run(["git", "-C", repo, "show", f"{ref}:{path}"], check=True, capture_output=True).stdout
    return gzip.decompress(data) if path.endswith(".gz") else data


def tilt(deg: float) -> float:
    return ((deg + 45.0) % 90.0) - 45.0


def transform(name: str, side: Q, x: Q, y: Q, deg: float) -> tuple[Q, Q, float]:
    s = side
    table = {
        "identity": (x, y, deg),
        "rot90": (s - y, x, deg + 90),
        "rot180": (s - x, s - y, deg + 180),
        "rot270": (y, s - x, deg + 270),
        "mirror-x": (s - x, y, -deg),
        "mirror-y": (x, s - y, -deg),
        "transpose": (y, x, 90 - deg),
        "anti-transpose": (s - y, s - x, -90 - deg),
    }
    return table[name]


# --- assignment ----------------------------------------------------------------------------


def hungarian(cost: np.ndarray) -> np.ndarray:
    """Rows to columns minimizing total cost; returns col index for each row (potentials method)."""
    n = cost.shape[0]
    inf = float("inf")
    u = np.zeros(n + 1)
    v = np.zeros(n + 1)
    p = np.zeros(n + 1, dtype=np.int64)
    way = np.zeros(n + 1, dtype=np.int64)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = np.full(n + 1, inf)
        used = np.zeros(n + 1, dtype=bool)
        while True:
            used[j0] = True
            i0 = p[j0]
            js = np.nonzero(~used)[0]
            cur = cost[i0 - 1, js - 1] - u[i0] - v[js]
            better = cur < minv[js]
            minv[js[better]] = cur[better]
            way[js[better]] = j0
            k = int(np.argmin(minv[js]))
            j1 = int(js[k])
            delta = minv[j1]
            idx = np.nonzero(used)[0]
            u[p[idx]] += delta
            v[idx] -= delta
            minv[js] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = int(way[j0])
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    col = np.zeros(n, dtype=np.int64)
    for j in range(1, n + 1):
        col[p[j] - 1] = j - 1
    return col


def perfect_matching_within(dist: np.ndarray, thr: float) -> bool:
    n = dist.shape[0]
    adj = [np.nonzero(dist[i] <= thr)[0].tolist() for i in range(n)]
    if any(not a for a in adj):
        return False
    match_col = [-1] * n
    sys.setrecursionlimit(10000)

    def augment(i, seen):
        for j in adj[i]:
            if not seen[j]:
                seen[j] = True
                if match_col[j] == -1 or augment(match_col[j], seen):
                    match_col[j] = i
                    return True
        return False

    for i in range(n):
        if not augment(i, [False] * n):
            return False
    return True


def bottleneck(dist: np.ndarray) -> float:
    values = np.unique(dist)
    lo, hi = 0, len(values) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if perfect_matching_within(dist, values[mid]):
            hi = mid
        else:
            lo = mid + 1
    return float(values[lo])


# --- measurement ---------------------------------------------------------------------------


def measure(mine: list, mine_side: Q, ref: list, ref_side: Q, sym: str, objective: str = "squared") -> dict:
    tr = [transform(sym, ref_side, x, y, d) for x, y, d in ref]
    a = np.array([[float(x), float(y)] for x, y, _ in mine])
    b = np.array([[float(x), float(y)] for x, y, _ in tr])
    diff = a[:, None, :] - b[None, :, :]
    d2 = (diff**2).sum(axis=2)
    dist = np.sqrt(d2)
    col = hungarian(d2 if objective == "squared" else dist)
    moves = dist[np.arange(len(mine)), col]
    nearest = np.argmin(dist, axis=1)
    one_to_one = len(set(nearest.tolist())) == len(mine)
    exact = []
    for i, j in enumerate(col.tolist()):
        dx = mine[i][0] - tr[j][0]
        dy = mine[i][1] - tr[j][1]
        exact.append(dx * dx + dy * dy)

    def within(r):
        return sum(1 for e in exact if e < Q(r) ** 2)

    def beyond(r):
        return sum(1 for e in exact if e > Q(r) ** 2)

    turned = 0
    reversed_tilts = 0
    for i, j in enumerate(col.tolist()):
        t1, t2 = tilt(mine[i][2]), tilt(tr[j][2])
        dt = abs(((t1 - t2) + 45.0) % 90.0 - 45.0)
        if dt > 1.0:
            turned += 1
        if abs(t1) > 1.0 and abs(t2) > 1.0 and (t1 > 0) != (t2 > 0):
            reversed_tilts += 1
    return {
        "symmetry": sym,
        "objective": objective,
        "total_squared": float(d2[np.arange(len(mine)), col].sum()),
        "nearest_one_to_one": one_to_one,
        "within_1e-20": within(Q(1, 10**20)),
        "within_1e-15": within(Q(1, 10**15)),
        "within_1e-12": within(Q(1, 10**12)),
        "within_1e-9": within(Q(1, 10**9)),
        "within_1e-6": within(Q(1, 10**6)),
        "within_1e-3": within(Q(1, 10**3)),
        "within_1e-2": within(Q(1, 10**2)),
        "beyond_1e-2": beyond(Q(1, 10**2)),
        "beyond_0.1": beyond(Q(1, 10)),
        "beyond_0.5": beyond(Q(1, 2)),
        "largest_move": round(float(moves.max()), 6),
        "largest_move_square": int(np.argmax(moves)),
        "rms_move": round(float(np.sqrt((moves**2).mean())), 6),
        "turned_beyond_1_deg": turned,
        "tilts_reversed": reversed_tilts,
        "assignment_is_row_identity": bool((col == np.arange(len(mine))).all()),
        "_col": col.tolist(),
        "_moves": moves.tolist(),
    }


def contacts(checker, text: bytes, threshold: Q) -> tuple[set, dict, dict]:
    cert = checker.read_certificate(text)
    buf = io.StringIO()
    checker.route_z(cert, buf)
    pairs = set()
    gaps = []
    least_by_square: dict[int, Q] = {}
    for line in buf.getvalue().splitlines():
        i, j, g, _ax = line.split("\t")
        gq = Q(g)
        gaps.append(gq)
        for k in (int(i), int(j)):
            if k not in least_by_square or gq < least_by_square[k]:
                least_by_square[k] = gq
        if gq < threshold:
            pairs.add((int(i), int(j)))
    side = Q(*cert["side"])
    walls = {}
    clear = []
    for k, ((xp, xq), (yp, yq), (tp, tq)) in enumerate(cert["rows"]):
        x, y, t = Q(xp, xq), Q(yp, yq), Q(tp, tq)
        c, s = basis_of_t(t)
        h = (abs(c) + abs(s)) / 2
        for wall, val in (("left", x - h), ("right", side - x - h), ("bottom", y - h), ("top", side - y - h)):
            clear.append(val)
            if val < least_by_square[k]:
                least_by_square[k] = val
            if val < threshold:
                walls.setdefault(k, []).append(wall)
    below = [g for g in gaps if g < threshold]
    above = [g for g in gaps if g >= threshold]
    wbelow = [c for c in clear if c < threshold]
    wabove = [c for c in clear if c >= threshold]
    stats = {
        "pair_contacts": len(pairs),
        "largest_contact_gap": f"{float(max(below)):.6e}" if below else None,
        "least_non_contact_gap": f"{float(min(above)):.6e}" if above else None,
        "wall_contacts": len(wbelow),
        "largest_wall_contact_clearance": f"{float(max(wbelow)):.6e}" if wbelow else None,
        "least_non_contact_wall_clearance": f"{float(min(wabove)):.6e}" if wabove else None,
    }
    touched = {a for p in pairs for a in p} | set(walls)
    stats["free_squares_least_clearance"] = {
        str(k): f"{float(least_by_square[k]):.6e}" for k in range(len(cert["rows"])) if k not in touched
    }
    return pairs, walls, stats


def load_checker(path: str):
    spec = importlib.util.spec_from_file_location("review_t238_check", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def self_test() -> int:
    from scipy.optimize import linear_sum_assignment  # noqa: PLC0415

    rng = np.random.default_rng(20261023)
    failures = 0
    for trial in range(300):
        n = int(rng.integers(2, 7)) if trial < 150 else int(rng.integers(10, 40))
        cost = rng.random((n, n)) * (10 if trial % 2 else 1)
        col = hungarian(cost)
        mine = cost[np.arange(n), col].sum()
        r, c = linear_sum_assignment(cost)
        theirs = cost[r, c].sum()
        if abs(mine - theirs) > 1e-9:
            failures += 1
        if n <= 6:
            best = min(sum(cost[i, p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
            bott = min(max(cost[i, p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
            if abs(mine - best) > 1e-9 or abs(bottleneck(cost) - bott) > 1e-12:
                failures += 1
    print(json.dumps({"instances": 300, "failures": failures}))
    return 0 if failures == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert", nargs="?")
    ap.add_argument("--checker")
    ap.add_argument("--repo")
    ap.add_argument("--ref")
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    data = Path(args.cert).read_bytes()
    side, mine = poses_from_text("cert", data)
    rev = subprocess.run(["git", "-C", args.repo, "rev-parse", args.ref], check=True, capture_output=True, text=True).stdout.strip()
    out: dict = {
        "program": "identity_t238.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_sha256": hashlib.sha256(data).hexdigest(),
        "ref_commit": rev,
        "tilted_beyond_0.1_deg": sum(1 for _, _, d in mine if abs(tilt(d)) > 0.1),
        "references": [],
    }
    t230_raw = None
    for label, kind, path in REFERENCES:
        raw = show(args.repo, args.ref, path)
        ref_side, ref = poses_from_text(kind, raw)
        if label.startswith("T-230"):
            t230_raw = raw
        rows = [measure(mine, side, ref, ref_side, sym) for sym in SYMMETRIES]
        best = min(rows, key=lambda r: r["total_squared"])
        ident = next(r for r in rows if r["symmetry"] == "identity")
        dist_for_bottleneck = None
        tr = [transform(best["symmetry"], ref_side, x, y, d) for x, y, d in ref]
        a = np.array([[float(x), float(y)] for x, y, _ in mine])
        b = np.array([[float(x), float(y)] for x, y, _ in tr])
        dist_for_bottleneck = np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2))
        entry = {
            "reference": label,
            "path": path,
            "reference_tilted_beyond_0.1_deg": sum(1 for _, _, d in ref if abs(tilt(d)) > 0.1),
            "best": {k: v for k, v in best.items() if not k.startswith("_")},
            "bottleneck": round(bottleneck(dist_for_bottleneck), 6),
            "totals_by_symmetry": {r["symmetry"]: round(r["total_squared"], 6) for r in rows},
            "identity": {k: v for k, v in ident.items() if not k.startswith("_")},
        }
        if label.startswith("T-230"):
            plain = measure(mine, side, ref, ref_side, best["symmetry"], objective="plain")
            entry["min_total_move"] = {k: v for k, v in plain.items() if not k.startswith("_")}
            entry["min_total_move"]["same_assignment_as_squared"] = plain["_col"] == best["_col"]
            moved = sorted(
                ((m, i, best["_col"][i]) for i, m in enumerate(best["_moves"]) if m > 0.1), reverse=True
            )
            entry["squares_beyond_0.1"] = [
                {
                    "square": i,
                    "partner": j,
                    "move": round(m, 4),
                    "tilt_here": round(tilt(mine[i][2]), 4),
                    "tilt_there": round(tilt(transform(best["symmetry"], ref_side, *ref[j])[2]), 4),
                }
                for m, i, j in moved
            ]
            col = best["_col"]
            entry["tilt_changes"] = {
                "tilted_here_aligned_there": sum(
                    1 for i, j in enumerate(col) if abs(tilt(mine[i][2])) > 0.1 and abs(tilt(ref[j][2])) <= 0.1
                ),
                "aligned_here_tilted_there": sum(
                    1 for i, j in enumerate(col) if abs(tilt(mine[i][2])) <= 0.1 and abs(tilt(ref[j][2])) > 0.1
                ),
            }
        out["references"].append(entry)
        b_ = entry["best"]
        print(
            f"{label[:42]:42} {b_['symmetry']:14} 1:1={b_['nearest_one_to_one']!s:5} "
            f"w1e-9={b_['within_1e-9']:3} w1e-6={b_['within_1e-6']:3} w1e-3={b_['within_1e-3']:3} "
            f">1e-2={b_['beyond_1e-2']:3} >0.1={b_['beyond_0.1']:3} >0.5={b_['beyond_0.5']:3} "
            f"max={b_['largest_move']:.4f} rms={b_['rms_move']:.4f} bott={entry['bottleneck']:.4f} "
            f"turned={b_['turned_beyond_1_deg']:3} rev={b_['tilts_reversed']:3}",
            flush=True,
        )
    if args.checker and t230_raw is not None:
        checker = load_checker(args.checker)
        out["contacts_against_t230"] = {}
        for label_thr, thr in (("1e-10", Q(1, 10**10)), ("1e-6", Q(1, 10**6))):
            out["contacts_against_t230"][label_thr] = compare_contacts(checker, data, t230_raw, thr, mine, side, out)
            print(label_thr, json.dumps(out["contacts_against_t230"][label_thr], indent=1))
        t230 = out["references"][0]
        col = measure(mine, side, poses_from_text("cert", t230_raw)[1], poses_from_text("cert", t230_raw)[0], "identity")["_col"]
        _s, ref230 = poses_from_text("cert", t230_raw)
        t230["tilt_changed_squares"] = [
            {"square": i, "tilt_here": round(tilt(mine[i][2]), 4), "tilt_there": round(tilt(ref230[j][2]), 4)}
            for i, j in enumerate(col)
            if abs(((tilt(mine[i][2]) - tilt(ref230[j][2])) + 45.0) % 90.0 - 45.0) > 1.0
        ]
        moves230 = measure(mine, side, ref230, _s, "identity")["_moves"]
        t230["squares_beyond_1e-2"] = sorted(i for i, m in enumerate(moves230) if m > 0.01)
        listed = set(t230["squares_beyond_1e-2"])
        for thr_label in out["contacts_against_t230"]:
            listed |= set(out["contacts_against_t230"][thr_label]["squares_whose_contacts_differ_list"])
        t230["square_table"] = [
            {
                "square": i,
                "x": round(float(mine[i][0]), 4),
                "y": round(float(mine[i][1]), 4),
                "tilt_here": round(tilt(mine[i][2]), 4),
                "tilt_there": round(tilt(ref230[col[i]][2]), 4),
                "move": float(f"{moves230[i]:.4e}"),
                "dx": float(f"{float(mine[i][0] - ref230[col[i]][0]):.4e}"),
                "dy": float(f"{float(mine[i][1] - ref230[col[i]][1]):.4e}"),
            }
            for i in sorted(listed)
        ]
        exact_moves = []
        for i in range(len(mine)):
            dx = mine[i][0] - ref230[col[i]][0]
            dy = mine[i][1] - ref230[col[i]][1]
            exact_moves.append((dx * dx + dy * dy, i))
        near = sorted(m for m in exact_moves if m[0] < Q(1, 10**18))
        t230["squares_within_1e-9"] = {
            "count": len(near),
            "largest_move": f"{math.sqrt(float(near[-1][0])):.6e}" if near else None,
            "smallest_move": f"{math.sqrt(float(near[0][0])):.6e}" if near else None,
        }
    Path(args.out).write_text(json.dumps(out, indent=2) + "\n")
    return 0


def compare_contacts(checker, data, t230_raw, thr, mine, side, out):
    """The two contact graphs at one threshold, T-230's mapped through the assignment."""
    mine_pairs, mine_walls, mine_stats = contacts(checker, data, thr)
    ref_pairs, ref_walls, ref_stats = contacts(checker, t230_raw, thr)
    t230 = out["references"][0]
    sym = t230["best"]["symmetry"]
    assert sym == "identity", "contact comparison is written for the identity symmetry"
    _side230, ref230 = poses_from_text("cert", t230_raw)
    col = measure(mine, side, ref230, _side230, sym)["_col"]
    inv = {j: i for i, j in enumerate(col)}
    mapped = {tuple(sorted((inv[a], inv[b]))) for a, b in ref_pairs}
    common = mine_pairs & mapped
    mapped_walls = {(inv[k], w) for k, ws in ref_walls.items() for w in ws}
    my_walls = {(k, w) for k, ws in mine_walls.items() for w in ws}
    degree_mine = {}
    for a, b in mine_pairs:
        degree_mine[a] = degree_mine.get(a, 0) + 1
        degree_mine[b] = degree_mine.get(b, 0) + 1
    degree_ref = {}
    for a, b in mapped:
        degree_ref[a] = degree_ref.get(a, 0) + 1
        degree_ref[b] = degree_ref.get(b, 0) + 1
    touched_mine = {k for k in range(303) if degree_mine.get(k, 0) or any(kk == k for kk, _ in my_walls)}
    touched_ref = {k for k in range(303) if degree_ref.get(k, 0) or any(kk == k for kk, _ in mapped_walls)}
    changed_squares = sorted(
        {a for p in (mine_pairs ^ mapped) for a in p} | {k for k, _ in (my_walls ^ mapped_walls)}
    )
    return {
        "threshold": str(float(thr)),
        "this_certificate": mine_stats,
        "t230": ref_stats,
        "pair_contacts_common": len(common),
        "pair_contacts_only_here": len(mine_pairs - mapped),
        "pair_contacts_only_in_t230": len(mapped - mine_pairs),
        "wall_contacts_common": len(my_walls & mapped_walls),
        "wall_contacts_only_here": len(my_walls - mapped_walls),
        "wall_contacts_only_in_t230": len(mapped_walls - my_walls),
        "squares_without_contact_here": 303 - len(touched_mine),
        "squares_without_contact_in_t230": 303 - len(touched_ref),
        "squares_whose_contacts_differ": len(changed_squares),
        "squares_whose_contacts_differ_list": changed_squares,
        "squares_without_contact_here_list": sorted(set(range(303)) - touched_mine),
        "squares_without_contact_in_t230_list": sorted(set(range(303)) - touched_ref),
        "pair_contacts_only_here_list": sorted(mine_pairs - mapped),
        "pair_contacts_only_in_t230_list": sorted(mapped - mine_pairs),
        "wall_contacts_only_here_list": sorted(my_walls - mapped_walls),
        "wall_contacts_only_in_t230_list": sorted(mapped_walls - my_walls),
    }


if __name__ == "__main__":
    sys.exit(main())
