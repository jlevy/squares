"""Programs for the stage 4 review of Khalili and Gharabaghi's s(44) = 7 mixed cover.

Written for the review from the mixed format v1 specification (certificate/FORMAT_mixed_v1.md)
and the statement; it imports nothing from the source, from Daniel's checkers or from this
repository. Every decision it prints is exact (Python integers and fractions.Fraction);
floating point only chooses where to look. It decides nothing about the claim: a sample of
poses can find a violation, and cannot show there is none.

Commands (each prints JSON):

  cover COVER
      Parse the cover with this program's own reader; exact total, slack below 44, counts,
      segment census, D4 invariance as a measure (points by position, each line's density as
      a canonical step function) under all eight symmetries, points on loaded lines, and the
      SHA-256 of the bytes.
  poses COVER [--seed S] [--random N] [--descents K]
      Exact mu(Q) of the closed unit square at sampled admissible poses of [0,7]^2: uniform
      in the D4 region; near the 7 x 7 tiling's cells (tiny tilts, small offsets); flush
      against a wall near a corner at tilts 0.01 to 3 degrees (the source's "valleys");
      near 45 degrees; then K float descents from the lowest exact poses, each end point
      re-evaluated exactly at a rational pose. Reports the least exact mu found and its pose.
  compare-s45 COVER S45
      Compares the cover with Evan Daniel's s(45) = 7 cover, which the source names as its
      warm start: segment supports, point positions, masses.
  zm-records DIR
      Reads the source's zm_mixed.py per-root records (verification/logs/zm_mixed): root
      coverage of the D4 region at the header's pitch and bins, census, uncertified boxes,
      digests in each header, and whether every root uncertified at depth 24 has a deeper
      run of the whole root with none. A read of the producer's records, not a replay.

Usage: python3 -I s44_review.py COMMAND ...
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import random
import sys
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

SIDE = 7
N = 44


# ------------------------------------------------------------------ parsing


def read_bytes(path: str) -> bytes:
    data = Path(path).read_bytes()
    return gzip.decompress(data) if path.endswith(".gz") else data


def parse(data: bytes):
    tokens = []
    for line in data.decode("ascii").splitlines():
        body = line.split("#", 1)[0].split()
        tokens.extend(body)
    it = iter(tokens)
    assert next(it) == "mixed" and next(it) == "1"
    s_num, s_den = int(next(it)), int(next(it))
    d, w = int(next(it)), int(next(it))
    npts = int(next(it))
    pts = [(int(next(it)), int(next(it)), int(next(it))) for _ in range(npts)]
    nseg = int(next(it))
    segs = [tuple(int(next(it)) for _ in range(5)) for _ in range(nseg)]
    npg = int(next(it))
    rest = list(it)
    return dict(s=F(s_num, s_den), D=d, W=w, pts=pts, segs=segs, npg=npg, trailing=len(rest))


# ------------------------------------------------------------------ the measure


class Cover:
    def __init__(self, c):
        self.D, self.W = c["D"], c["W"]
        self.S = c["s"] * self.D
        assert self.S.denominator == 1
        self.S = int(self.S)
        # points as exact Fractions in container units, with float copies for pruning
        self.pts = [(F(x, self.D), F(y, self.D), F(wt, self.W)) for x, y, wt in c["pts"]]
        self.fpts = [(float(x), float(y)) for x, y, _ in self.pts]
        # segments grouped by line: ('V', x) -> [(a, b, density)], density = mass per unit length
        self.lines = defaultdict(list)
        for x0, y0, x1, y1, wt in c["segs"]:
            if x0 == x1:
                key, a, b = ("V", F(x0, self.D)), F(min(y0, y1), self.D), F(max(y0, y1), self.D)
            else:
                assert y0 == y1
                key, a, b = ("H", F(y0, self.D)), F(min(x0, x1), self.D), F(max(x0, x1), self.D)
            self.lines[key].append((a, b, F(wt, self.W) / (b - a)))
        # buckets of 1/2 for point pruning
        self.buckets = defaultdict(list)
        for i, (x, y) in enumerate(self.fpts):
            self.buckets[(int(x * 2), int(y * 2))].append(i)

    def mu(self, cx: F, cy: F, u: F) -> F:
        """Exact mass of the closed unit square centred at (cx, cy) at angle 2 atan(u)."""
        q = 1 + u * u
        c, s = (1 - u * u) / q, 2 * u / q
        half = F(1, 2)
        total = F(0)
        fx, fy = float(cx), float(cy)
        r = 0.7072
        for bx in range(int((fx - r) * 2) - 1, int((fx + r) * 2) + 2):
            for by in range(int((fy - r) * 2) - 1, int((fy + r) * 2) + 2):
                for i in self.buckets.get((bx, by), ()):
                    px, py = self.fpts[i]
                    if (px - fx) ** 2 + (py - fy) ** 2 > 0.5001:
                        continue
                    x, y, wt = self.pts[i]
                    dx, dy = x - cx, y - cy
                    if abs(c * dx + s * dy) <= half and abs(-s * dx + c * dy) <= half:
                        total += wt
        for (kind, pos), segs in self.lines.items():
            centre_along, centre_across = (cy, cx) if kind == "V" else (cx, cy)
            if abs(float(pos - centre_across)) > 0.7072:
                continue
            # along the line, t is the coordinate; the across offset is fixed
            if kind == "V":
                dxc = pos - cx  # x fixed; constraints on dy = t - cy
                cons = [(s, c * dxc), (c, -s * dxc)]  # |k*dy + m| <= 1/2
            else:
                dyc = pos - cy  # y fixed; constraints on dx = t - cx
                cons = [(c, s * dyc), (-s, c * dyc)]
            lo, hi = None, None
            empty = False
            for k, m in cons:
                if k == 0:
                    if abs(m) > half:
                        empty = True
                    continue
                a1, b1 = (-half - m) / k, (half - m) / k
                if a1 > b1:
                    a1, b1 = b1, a1
                lo = a1 if lo is None else max(lo, a1)
                hi = b1 if hi is None else min(hi, b1)
            if empty or lo is None or lo > hi:
                continue
            tlo, thi = centre_along + lo, centre_along + hi
            for a, b, dens in segs:
                overlap = min(b, thi) - max(a, tlo)
                if overlap > 0:
                    total += dens * overlap
        return total

    def admissible(self, cx: F, cy: F, u: F) -> bool:
        q = 1 + u * u
        c, s = (1 - u * u) / q, 2 * u / q
        hw = (c + s) / 2  # half-width of the rotated square's bounding box, for theta in [0, 90)
        return hw <= cx <= SIDE - hw and hw <= cy <= SIDE - hw


def fmu(cov: Cover, x: float, y: float, u: float) -> float:
    """Float mass, for choosing where to look only."""
    q = 1 + u * u
    c, s = (1 - u * u) / q, 2 * u / q
    tot = 0.0
    for bx in range(int((x - 0.71) * 2) - 1, int((x + 0.71) * 2) + 2):
        for by in range(int((y - 0.71) * 2) - 1, int((y + 0.71) * 2) + 2):
            for i in cov.buckets.get((bx, by), ()):
                px, py = cov.fpts[i]
                dx, dy = px - x, py - y
                if abs(c * dx + s * dy) <= 0.5 and abs(-s * dx + c * dy) <= 0.5:
                    tot += float(cov.pts[i][2])
    for (kind, pos), segs in cov.lines.items():
        p = float(pos)
        along, across = (y, x) if kind == "V" else (x, y)
        if abs(p - across) > 0.71:
            continue
        d0 = p - across
        cons = [(s, c * d0), (c, -s * d0)] if kind == "V" else [(c, s * d0), (-s, c * d0)]
        lo, hi = -1e9, 1e9
        ok = True
        for k, m in cons:
            if abs(k) < 1e-15:
                if abs(m) > 0.5:
                    ok = False
                continue
            a1, b1 = (-0.5 - m) / k, (0.5 - m) / k
            if a1 > b1:
                a1, b1 = b1, a1
            lo, hi = max(lo, a1), min(hi, b1)
        if not ok or lo > hi:
            continue
        tlo, thi = along + lo, along + hi
        for a, b, dens in segs:
            ov = min(float(b), thi) - max(float(a), tlo)
            if ov > 0:
                tot += float(dens) * ov
    return tot


def rat(v: float, den: int = 10**9) -> F:
    return F(round(v * den), den)


def fhw(u: float) -> float:
    q = 1 + u * u
    return ((1 - u * u) / q + 2 * u / q) / 2


# ------------------------------------------------------------------ commands


def cmd_cover(path: str) -> dict:
    data = read_bytes(path)
    c = parse(data)
    s, D, W = c["s"], c["D"], c["W"]
    S = int(s * D)
    tp = sum(w for *_, w in c["pts"])
    ts = sum(seg[4] for seg in c["segs"])
    total = F(tp + ts, W)
    lengths = defaultdict(int)
    walls = 0
    lines = set()
    for x0, y0, x1, y1, w in c["segs"]:
        assert (x0 == x1) != (y0 == y1)
        lengths[str(F(abs(x1 - x0) + abs(y1 - y0), D))] += 1
        pos = x0 if x0 == x1 else y0
        lines.add(("V" if x0 == x1 else "H", pos))
        if pos in (0, S):
            walls += 1
    cov = Cover(c)

    def image(g, x, y):
        swap, fx, fy = g
        if fx:
            x = S - x
        if fy:
            y = S - y
        return (y, x) if swap else (x, y)

    group = [(sw, fx, fy) for sw in (0, 1) for fx in (0, 1) for fy in (0, 1)]
    pmass = defaultdict(int)
    for x, y, w in c["pts"]:
        pmass[(x, y)] += w

    def canon_lines(segs):
        # each line: sorted breakpoints with the density on each piece, zero pieces dropped
        per = defaultdict(list)
        for x0, y0, x1, y1, w in segs:
            if x0 == x1:
                per[("V", x0)].append((min(y0, y1), max(y0, y1), F(w, abs(y1 - y0))))
            else:
                per[("H", y0)].append((min(x0, x1), max(x0, x1), F(w, abs(x1 - x0))))
        out = {}
        for key, items in per.items():
            bps = sorted({p for a, b, _ in items for p in (a, b)})
            steps = []
            for lo, hi in zip(bps, bps[1:]):
                dens = sum(dd for a, b, dd in items if a <= lo and hi <= b)
                if dens:
                    if steps and steps[-1][1] == lo and steps[-1][2] == dens:
                        steps[-1] = (steps[-1][0], hi, dens)
                    else:
                        steps.append((lo, hi, dens))
            out[key] = tuple(steps)
        return out

    base_lines = canon_lines(c["segs"])
    invariant = True
    for g in group:
        img_pts = defaultdict(int)
        for (x, y), w in pmass.items():
            img_pts[image(g, x, y)] += w
        if img_pts != pmass:
            invariant = False
        segs2 = []
        for x0, y0, x1, y1, w in c["segs"]:
            a, b = image(g, x0, y0), image(g, x1, y1)
            segs2.append((a[0], a[1], b[0], b[1], w))
        if canon_lines(segs2) != base_lines:
            invariant = False
    on_lines = sum(
        1 for x, y, w in c["pts"] if ("V", x) in lines or ("H", y) in lines
    )
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "side": str(s),
        "D": D,
        "W": W,
        "points": len(c["pts"]),
        "segments": len(c["segs"]),
        "polygons": c["npg"],
        "trailing_tokens": c["trailing"],
        "total": str(total),
        "total_decimal": f"{float(total):.10f}",
        "slack_below_44": str(N - total),
        "slack_fraction": f"{float((N - total) / N):.6%}",
        "point_mass": str(F(tp, W)),
        "segment_mass": str(F(ts, W)),
        "segment_lengths": dict(lengths),
        "segment_lines": sorted(f"{k}{F(p, D)}" for k, p in lines),
        "wall_segments": walls,
        "points_on_loaded_lines": on_lines,
        "zero_or_negative_weights": sum(1 for *_, w in c["pts"] if w <= 0)
        + sum(1 for *_, w in c["segs"] if w <= 0),
        "d4_invariant_as_measure_all_eight": invariant,
        "point_positions": len(pmass),
        "lines_with_density": len(cov.lines),
    }


def sample_poses(rng: random.Random, n_random: int) -> list[tuple[str, F, F, F]]:
    out = []
    # uniform in the D4 region: centres in [0, 7/2]^2, u in [0, tan(pi/8)]
    t8 = math.tan(math.pi / 8)
    while len(out) < n_random:
        u = rng.uniform(0, t8)
        hw = fhw(u)
        x, y = rng.uniform(hw, 3.5), rng.uniform(hw, 3.5)
        out.append(("uniform", rat(x), rat(y), rat(u)))
    # near-tile: cell centres (i + 1/2, j + 1/2) of the 7 x 7 grid, tiny tilts and offsets
    for i in range(4):
        for j in range(4):
            for u in (0.0, 1e-7, 1e-5, 1e-4, 1e-3, 5e-3):
                for ox, oy in ((0, 0), (1e-4, 0), (0, 1e-4), (-1e-4, 1e-4), (3e-3, -2e-3)):
                    x, y = i + 0.5 + ox, j + 0.5 + oy
                    hw = fhw(u)
                    x, y = max(x, hw), max(y, hw)
                    out.append(("near-tile", rat(x), rat(y), rat(u)))
    # wall valleys: a square flush against the wall x = 0 (and so y by D4), near a corner,
    # nearly axis-parallel at tilts of 0.01 to 3 degrees
    for deg in (0.01, 0.03, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0):
        u = math.tan(math.radians(deg) / 2)
        hw = fhw(u)
        for y in [hw + k * 0.02 for k in range(0, 76)]:
            out.append(("wall-valley", rat(hw + 1e-12), rat(min(y, 3.5)), rat(u)))
    # near 45 degrees
    for k in range(400):
        u = math.tan(math.pi / 8) - rng.uniform(0, 0.01)
        hw = fhw(u)
        out.append(("near-45", rat(rng.uniform(hw, 3.5)), rat(rng.uniform(hw, 3.5)), rat(u)))
    return out


def descend(cov: Cover, x: float, y: float, u: float, steps: int = 60) -> tuple[float, float, float]:
    best = fmu(cov, x, y, u)
    h = [0.01, 0.01, 0.002]
    for _ in range(steps):
        improved = False
        for k in range(3):
            for sgn in (1, -1):
                v = [x, y, u]
                v[k] += sgn * h[k]
                v[2] = min(max(v[2], 0.0), math.tan(math.pi / 8))
                hw = fhw(v[2])
                v[0] = min(max(v[0], hw), 3.5)
                v[1] = min(max(v[1], hw), 3.5)
                m = fmu(cov, *v)
                if m < best:
                    best, (x, y, u), improved = m, v, True
        if not improved:
            h = [t / 2 for t in h]
            if h[0] < 1e-7:
                break
    return x, y, u


def cmd_poses(path: str, seed: int, n_random: int, descents: int) -> dict:
    cov = Cover(parse(read_bytes(path)))
    rng = random.Random(seed)
    poses = sample_poses(rng, n_random)
    by_family: dict[str, dict] = {}
    results = []
    below = 0
    for fam, x, y, u in poses:
        if not cov.admissible(x, y, u):
            continue
        m = cov.mu(x, y, u)
        results.append((m, fam, x, y, u))
        below += m < 1
        f = by_family.setdefault(fam, {"poses": 0, "least": None})
        f["poses"] += 1
        if f["least"] is None or m < F(f["least"]):
            f["least"] = str(m)
    results.sort()
    descents_out = []
    for m0, fam, x, y, u in results[:descents]:
        ex, ey, eu = descend(cov, float(x), float(y), float(u))
        X, Y, U = rat(ex), rat(ey), rat(eu)
        if not cov.admissible(X, Y, U):
            X, Y = max(X, rat(fhw(float(U)) + 1e-9)), max(Y, rat(fhw(float(U)) + 1e-9))
        m = cov.mu(X, Y, U)
        below += m < 1
        descents_out.append(
            {
                "from_family": fam,
                "start_mu": f"{float(m0):.9f}",
                "end_pose": [str(X), str(Y), str(U)],
                "end_theta_deg": f"{math.degrees(2 * math.atan(float(U))):.6f}",
                "end_mu_exact": str(m),
                "end_mu": f"{float(m):.9f}",
            }
        )
    least = min([r[0] for r in results] + [F(d["end_mu_exact"]) for d in descents_out])
    lowest = results[:10]
    return {
        "poses_evaluated": len(results),
        "descents": len(descents_out),
        "exact_mu_below_one": below,
        "least_exact_mu": str(least),
        "least_exact_mu_decimal": f"{float(least):.9f}",
        "by_family": {k: {**v, "least_decimal": f"{float(F(v['least'])):.9f}"} for k, v in by_family.items()},
        "lowest_sampled": [
            {"family": f, "pose": [str(x), str(y), str(u)], "mu": f"{float(m):.9f}"}
            for m, f, x, y, u in lowest
        ],
        "descent_ends": descents_out,
    }


def cmd_compare_s45(path: str, s45: str) -> dict:
    a, b = parse(read_bytes(path)), parse(read_bytes(s45))
    sa = {(x0, y0, x1, y1) for x0, y0, x1, y1, _ in a["segs"]}
    sb = {(x0, y0, x1, y1) for x0, y0, x1, y1, _ in b["segs"]}
    scale = F(b["D"], a["D"])
    pa = {(x, y) for x, y, _ in a["pts"]}
    pb = {(F(x, 1) / scale, F(y, 1) / scale) for x, y, _ in b["pts"]}
    pa_f = {(F(x), F(y)) for x, y in pa}
    tb = F(sum(w for *_, w in b["pts"]) + sum(s[4] for s in b["segs"]), b["W"])
    return {
        "s44": {"D": a["D"], "W": a["W"], "points": len(a["pts"]), "segments": len(a["segs"])},
        "s45": {"D": b["D"], "W": b["W"], "points": len(b["pts"]), "segments": len(b["segs"]), "total": str(tb)},
        "same_coordinate_denominator": a["D"] == b["D"],
        "segment_supports_identical": sa == sb if a["D"] == b["D"] else None,
        "point_positions_shared": len(pa_f & pb),
        "s44_point_positions": len(pa_f),
        "s45_point_positions": len(pb),
    }


def cmd_zm_records(directory: str) -> dict:
    root_dir = Path(directory)
    stats = {"files": 0, "headers": set(), "settings": set()}
    first: dict[tuple, dict] = {}
    deep: dict[tuple, dict] = {}
    for f in sorted(root_dir.rglob("*.jsonl")):
        stats["files"] += 1
        lines = f.read_text(encoding="ascii").splitlines()
        header = json.loads(lines[0])
        assert header["kind"] == "zm_mixed cert header", f
        stats["headers"].add(json.dumps(header["sha256"], sort_keys=True))
        st = dict(header["settings"])
        st.pop("region")
        depth = st["depth"]
        stats["settings"].add(json.dumps(st, sort_keys=True))
        target = first if depth == 24 else deep
        for line in lines[1:]:
            rec = json.loads(line)
            key = tuple(rec["root"])
            entry = {"uncert": rec["st"]["UNCERT"], "boxes": rec["st"]["boxes"],
                     "maxdepth": rec["st"]["maxdepth"], "cpu": rec["st"]["cpu"], "file": f.name,
                     "depth_limit": depth, "label": rec.get("label", "")}
            target.setdefault(key, []).append(entry)
    # the D4 region at the depth-24 header's pitch and bins
    st24 = [json.loads(s) for s in stats["settings"] if json.loads(s)["depth"] == 24]
    pitch = F(st24[0]["pitch"])
    ubins = st24[0]["ubins"]
    cells = int(F(SIDE, 2) / pitch)
    du = F(1, 2) / ubins
    expected = {
        (str(i * pitch), str((i + 1) * pitch), str(j * pitch), str((j + 1) * pitch),
         str(k * du), str((k + 1) * du))
        for i in range(cells) for j in range(cells) for k in range(ubins)
    }

    def norm(key):
        return tuple(str(F(v)) for v in key)

    first_n = {norm(k): v for k, v in first.items()}
    repeated = sum(1 for v in first.values() if len(v) > 1)
    uncert_roots = {k for k, v in first_n.items() if any(e["uncert"] for e in v)}
    deep_n = {}
    for k, v in deep.items():
        deep_n.setdefault(norm(k), []).extend(v)
    # a deeper run may sweep a root in sub-roots; record which deep roots lie inside each
    def inside(sub, root):
        s, r = [F(x) for x in sub], [F(x) for x in root]
        return all(r[2 * i] <= s[2 * i] and s[2 * i + 1] <= r[2 * i + 1] for i in range(3))

    closure = {}
    for root in sorted(uncert_roots):
        subs = [(k, e) for k, v in deep_n.items() if inside(k, root) for e in v]
        vol_root = math.prod(F(root[2 * i + 1]) - F(root[2 * i]) for i in range(3))
        vol = sum(math.prod(F(k[2 * i + 1]) - F(k[2 * i]) for i in range(3)) for k, _ in subs)
        closure["|".join(root)] = {
            "depth24_uncert": sum(e["uncert"] for e in first_n[root]),
            "deep_records": len(subs),
            "deep_uncert": sum(e["uncert"] for _, e in subs),
            "deep_maxdepth": max((e["maxdepth"] for _, e in subs), default=None),
            "deep_volume_equals_root": vol == vol_root,
        }
    return {
        "files": stats["files"],
        "distinct_digest_sets": [json.loads(h) for h in stats["headers"]],
        "settings_apart_from_region": [json.loads(s) for s in stats["settings"]],
        "d4_roots_expected": len(expected),
        "depth24_roots_recorded": len(first_n),
        "depth24_roots_missing": len(expected - first_n.keys()),
        "depth24_roots_outside_region": len(first_n.keys() - expected),
        "depth24_roots_recorded_more_than_once": repeated,
        "depth24_boxes": sum(e["boxes"] for v in first_n.values() for e in v),
        "depth24_uncert_boxes": sum(e["uncert"] for v in first_n.values() for e in v),
        "depth24_maxdepth": max(e["maxdepth"] for v in first_n.values() for e in v),
        "depth24_cpu_seconds": round(sum(e["cpu"] for v in first_n.values() for e in v), 1),
        "roots_uncertified_at_depth24": len(uncert_roots),
        "deep_records": sum(len(v) for v in deep_n.values()),
        "deep_cpu_seconds": round(sum(e["cpu"] for v in deep_n.values() for e in v), 1),
        "every_uncertified_root_closed_by_deeper_run": all(
            c["deep_records"] > 0 and c["deep_uncert"] == 0 and c["deep_volume_equals_root"]
            for c in closure.values()
        ),
        "closure": closure,
    }


def d4_orbit(S: int, x: int, y: int) -> set[tuple[int, int]]:
    out = set()
    for sw in (0, 1):
        for fx in (0, 1):
            for fy in (0, 1):
                a, b = (S - x if fx else x), (S - y if fy else y)
                out.add((b, a) if sw else (a, b))
    return out


def mutant_text(data: bytes, kind: str) -> tuple[bytes, str]:
    """This program's own orbit removal, rewriting the file line by line.

    point: every point at the D4 images of the position with the most point mass (ties:
    least (X, Y)); segment: every segment that is a D4 image of the heaviest one with its
    weight (ties: least endpoints). Comments and other lines are kept.
    """
    c = parse(data)
    S = int(c["s"] * c["D"])
    mass = defaultdict(int)
    for x, y, w in c["pts"]:
        mass[(x, y)] += w
    if kind == "point":
        top = min(mass, key=lambda p: (-mass[p], p))
        orbit = d4_orbit(S, *top)
        drop_pt = lambda x, y, w: (x, y) in orbit  # noqa: E731
        drop_seg = lambda *v: False  # noqa: E731
        what = f"point orbit of ({top[0]}, {top[1]})/{c['D']}, {mass[top]}/{c['W']} each"
    else:
        def key(v):
            a, b = sorted(((v[0], v[1]), (v[2], v[3])))
            return a, b, v[4]
        a0, b0, w0 = min((key(v) for v in c["segs"]), key=lambda k: (-k[2], k[0], k[1]))
        images = set()
        for sw in (0, 1):
            for fx in (0, 1):
                for fy in (0, 1):
                    def g(p):
                        x, y = (S - p[0] if fx else p[0]), (S - p[1] if fy else p[1])
                        return (y, x) if sw else (x, y)
                    images.add((*sorted((g(a0), g(b0))), w0))
        drop_pt = lambda x, y, w: False  # noqa: E731
        drop_seg = lambda *v: key(v) in images  # noqa: E731
        what = f"segment orbit of {a0}-{b0}/{c['D']}, {w0}/{c['W']} each"
    lines = data.decode("ascii").splitlines(keepends=True)
    out, state, counts = [], "head", {}
    rows = 0
    kept_pts = [p for p in c["pts"] if not drop_pt(*p)]
    kept_segs = [s for s in c["segs"] if not drop_seg(*s)]
    # walk the file: header rows (mixed 1, side, D, W), np, points, ns, segments, npg
    seen = 0
    for line in lines:
        body = line.split("#", 1)[0].split()
        if not body:
            out.append(line)
            continue
        seen += 1
        if seen <= 4:
            out.append(line)
            continue
        if seen == 5:
            out.append(line.replace(body[0], str(len(kept_pts)), 1))
            state = "pts"
            rows = 0
            continue
        if state == "pts" and rows < len(c["pts"]):
            rows += 1
            x, y, w = map(int, body)
            if not drop_pt(x, y, w):
                out.append(line)
            if rows == len(c["pts"]):
                state = "ns"
            continue
        if state == "ns":
            out.append(line.replace(body[0], str(len(kept_segs)), 1))
            state, rows = "segs", 0
            continue
        if state == "segs" and rows < len(c["segs"]):
            rows += 1
            v = tuple(map(int, body))
            if not drop_seg(*v):
                out.append(line)
            if rows == len(c["segs"]):
                state = "tail"
            continue
        out.append(line)
    counts["points_dropped"] = len(c["pts"]) - len(kept_pts)
    counts["segments_dropped"] = len(c["segs"]) - len(kept_segs)
    return "".join(out).encode("ascii"), what + f"; {counts}"


def cmd_mutants(path: str, seed: int) -> dict:
    data = read_bytes(path)
    base = Cover(parse(data))
    rng = random.Random(seed)
    out = {}
    for kind in ("point", "segment"):
        mdata, what = mutant_text(data, kind)
        mc = parse(mdata)
        mcov = Cover(mc)
        removed = F(sum(w for *_, w in parse(data)["pts"]) + sum(s[4] for s in parse(data)["segs"])
                    - sum(w for *_, w in mc["pts"]) - sum(s[4] for s in mc["segs"]), mc["W"])
        # look near the removed pieces' images inside the D4 region
        c0 = parse(data)
        S = int(c0["s"] * c0["D"])
        if kind == "point":
            gone = {(x, y) for x, y, _ in c0["pts"]} - {(x, y) for x, y, _ in mc["pts"]}
            anchors = [(x / c0["D"], y / c0["D"]) for x, y in gone]
        else:
            gone = set(c0["segs"]) - set(mc["segs"])
            anchors = [((v[0] + v[2]) / 2 / c0["D"], (v[1] + v[3]) / 2 / c0["D"]) for v in gone]
        anchors = [(x, y) for x, y in anchors if x <= 3.5 + 0.7 and y <= 3.5 + 0.7]
        cands = []
        for _ in range(4000):
            ax, ay = rng.choice(anchors)
            u = rng.uniform(0, math.tan(math.pi / 8))
            hw = fhw(u)
            x = min(max(ax + rng.uniform(-0.75, 0.75), hw), 3.5)
            y = min(max(ay + rng.uniform(-0.75, 0.75), hw), 3.5)
            cands.append((fmu(mcov, x, y, u), x, y, u))
        cands.sort()
        best = None
        for m0, x, y, u in cands[:8]:
            ex, ey, eu = descend(mcov, x, y, u, steps=80)
            X, Y, U = rat(ex), rat(ey), rat(eu)
            if not mcov.admissible(X, Y, U):
                continue
            m = mcov.mu(X, Y, U)
            if best is None or m < best[0]:
                best = (m, X, Y, U)
        m, X, Y, U = best
        out[kind] = {
            "removed": what,
            "mass_removed": str(removed),
            "mutant_sha256": hashlib.sha256(mdata).hexdigest(),
            "pose": [str(X), str(Y), str(U)],
            "theta_deg": f"{math.degrees(2 * math.atan(float(U))):.6f}",
            "zmx2_root_cell": [int(X * 10), int(Y * 10), int(U * 8)],
            "mutant_mu_exact": str(m),
            "mutant_mu": f"{float(m):.9f}",
            "mutant_below_one": m < 1,
            "published_mu_exact": str(base.mu(X, Y, U)),
            "published_mu": f"{float(base.mu(X, Y, U)):.9f}",
        }
    return out


#: The least floating-point masses the source reports, verification/logs/stress.out:
#: (label, x, y, theta in radians), as printed.
SOURCE_MINIMA = (
    ("random 300000", 4.554412827950355, 5.117327539844629, 1.2423897061974727),
    ("near-tile 300000", 4.499999502429363, 0.5000005182754007, -1.0365513385827142e-06),
    ("near-45 75000", 0.707071005337892, 3.7747439817517177, 0.7753388277318225),
    ("near-tile 2000", 0.5000008246043217, 5.499999251934642, 1.6492100032384228e-06),
    ("random 2000", 0.565505643430089, 3.541950770398206, 0.14147342512837216),
    ("near-45 500", 6.292893219689965, 3.7486020992883042, 0.7854479544968138),
)


def cmd_source_minima(path: str) -> dict:
    """Exact mu at the source's reported float minima, each pose taken to a rational one.

    A square at angle theta is the square at theta mod 90 degrees; the pose is used as
    printed, with its centre and u = tan(theta/2) rounded to 1e-12, and is reported
    inadmissible if rounding put it outside the container.
    """
    cov = Cover(parse(read_bytes(path)))
    out = []
    for label, x, y, th in SOURCE_MINIMA:
        th = th % (math.pi / 2)
        X, Y, U = rat(x, 10**12), rat(y, 10**12), rat(math.tan(th / 2), 10**12)
        ok = cov.admissible(X, Y, U)
        m = cov.mu(X, Y, U) if ok else None
        out.append({
            "source": label,
            "pose_as_printed": [x, y, th],
            "admissible": ok,
            "mu_exact": None if m is None else str(m),
            "mu": None if m is None else f"{float(m):.9f}",
            "float_mu_here": f"{fmu(cov, x, y, math.tan(th / 2)):.9f}",
        })
    return {"poses": out}


def main(argv: list[str]) -> None:
    cmd = argv[0]
    if cmd == "source-minima":
        print(json.dumps(cmd_source_minima(argv[1]), indent=1, default=str))
        return
    if cmd == "mutants":
        print(json.dumps(cmd_mutants(argv[1], 842), indent=1, default=str))
        return
    if cmd == "cover":
        out = cmd_cover(argv[1])
    elif cmd == "poses":
        args = argv[2:]
        def opt(name, default):
            return int(args[args.index(name) + 1]) if name in args else default
        out = cmd_poses(argv[1], opt("--seed", 842), opt("--random", 1500), opt("--descents", 25))
    elif cmd == "compare-s45":
        out = cmd_compare_s45(argv[1], argv[2])
    elif cmd == "zm-records":
        out = cmd_zm_records(argv[1])
    else:
        raise SystemExit(__doc__)
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main(sys.argv[1:])
