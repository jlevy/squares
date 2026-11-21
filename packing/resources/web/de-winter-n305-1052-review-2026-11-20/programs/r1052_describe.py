"""Lane r1052's description of a two-form certificate. It decides nothing.

Usage: r1052_describe.py J_FILE C_FILE OUT_JSON

It reads form J through the reader and reports, from exact values where it can: the
squares' tilts (angles printed in binary64 for reading), the half-angle tangents of the
edge directions and whether they terminate, the centres' decimal places and frame, the
sizes of the denominators, the near pairs with their exact Euclidean gaps, the wall
contacts and what touches, and the squares' near-pair degrees. A filter on margins is
used here only to choose what to describe; the decision is r1052_check.py's.
"""

from __future__ import annotations

import json
import math
import sys
import time
from fractions import Fraction as F
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import r1052_check as check  # noqa: E402
import r1052_geom as geom  # noqa: E402
import r1052_poses as poses_a  # noqa: E402
import r1052_reader as reader  # noqa: E402

NEAR = F(1, 10**3)


def places(value: F) -> int | None:
    """Decimal places of a terminating decimal, or None."""
    d = value.denominator
    twos = fives = 0
    while d % 2 == 0:
        d //= 2
        twos += 1
    while d % 5 == 0:
        d //= 5
        fives += 1
    return max(twos, fives) if d == 1 else None


def root_print(value: F, digits: int = 6) -> str:
    """sqrt of a non-negative exact value, to ``digits`` figures rounded down (for reading)."""
    if value == 0:
        return "0"
    scale = 10 ** 400
    return check.sci(F(math.isqrt((value * scale * scale).__floor__()), scale), digits)


def tilt(a: F, b: F) -> float:
    """The edge direction's angle modulo 90 degrees, in [0, 90), for reading."""
    ang = math.degrees(math.atan2(float(b), float(a))) % 90.0
    return 0.0 if ang >= 90.0 else ang


def main(argv: list[str]) -> int:
    j_path, c_path, out_path = argv[1:4]
    t0 = time.process_time()
    jj = reader.read_form_j(Path(j_path).read_bytes())
    cc = reader.read_form_c(Path(c_path).read_bytes())
    side: F = jj["side"]
    poses = jj["poses"]
    n = len(poses)
    facts = poses_a.run(side, poses=poses)
    m = facts["margins"]
    cl = facts["walls"]
    out: dict[str, Any] = {"program": "r1052_describe.py", "n": n, "format": jj["format"]}
    out["form_c_header"] = {
        "witness_id": cc["witness_id"],
        "envelope_keys": cc["envelope_keys"],
        "witness_keys": cc["witness_keys"],
        "claim_keys": cc["claim_keys"],
        "ids_first_last": [cc["ids"][0], cc["ids"][-1]],
        "ids_in_order": cc["ids"] == [f"square-{k + 1}" for k in range(n)],
        "ids_are_s1_to_sn_in_order": cc["ids"] == [f"s{k + 1}" for k in range(n)],
    }

    # tilts
    rows = []
    for k, (x, y, a, b) in enumerate(poses):
        exact_axis = a == 0 or b == 0
        t = tilt(a, b)
        s = min(abs(a), abs(b))  # |sin| of the turn from the nearest axis
        rows.append({"square": k + 1, "axis": exact_axis, "tilt_deg": t, "sin_from_axis": float(s)})
    axis = [r for r in rows if r["axis"]]
    turned = [r for r in rows if not r["axis"]]
    near_axis = [r for r in turned if r["sin_from_axis"] < 1e-9]
    visible = [r for r in turned if r["sin_from_axis"] >= 1e-9]
    groups: dict[str, list[int]] = {}
    for r in visible:
        key = f"{r['tilt_deg']:.3f}"
        groups.setdefault(key, []).append(r["square"])
    out["tilts"] = {
        "axis_aligned": len(axis),
        "turned": len(turned),
        "near_axis_turned": len(near_axis),
        "near_axis_sin_range": [min((r["sin_from_axis"] for r in near_axis), default=None),
                                max((r["sin_from_axis"] for r in near_axis), default=None)],
        "visibly_turned": len(visible),
        "clockwise_from_nearest_axis": sum(1 for r in visible if r["tilt_deg"] > 45),
        "counterclockwise_from_nearest_axis": sum(1 for r in visible if r["tilt_deg"] < 45),
        "tilt_range_deg": [min((r["tilt_deg"] for r in visible), default=None),
                           max((r["tilt_deg"] for r in visible), default=None)],
        "groups_at_1e-3_deg": {k: {"count": len(v), "squares": v[:40]} for k, v in
                               sorted(groups.items(), key=lambda kv: -len(kv[1]))[:30]},
        "group_count": len(groups),
    }
    out["tilt_list"] = [[r["square"], round(r["tilt_deg"], 9)] for r in rows]
    out["near_axis_squares"] = [
        {"square": r["square"], "sin_from_axis": r["sin_from_axis"],
         "sense": "clockwise" if r["tilt_deg"] > 45 else "counterclockwise"}
        for r in near_axis
    ]

    # half-angle tangents and coordinates
    half: dict[str, int] = {}
    cent: dict[str, int] = {}
    dens: list[int] = []
    for (x, y, a, b) in poses:
        if a == 0 or b == 0:
            half["axis"] = half.get("axis", 0) + 1
        else:
            tq = b / (1 + a)
            p = places(tq)
            key = "non-terminating" if p is None else str(p)
            half[key] = half.get(key, 0) + 1
        for v in (x, y):
            p = places(v)
            key = "non-terminating" if p is None else str(p)
            cent[key] = cent.get(key, 0) + 1
        ip = poses_a.integer_pose(x, y, a, b)
        dens.append(len(str(ip[4])))
    x0, y0 = poses[0][0], poses[0][1]
    rel: dict[str, int] = {}
    for (x, y, _, _) in poses:
        for v in (x - x0, y - y0):
            p = places(v)
            key = "non-terminating" if p is None else str(p)
            rel[key] = rel.get(key, 0) + 1
    out["half_angle_tangent_places"] = half
    out["centre_coordinate_places"] = cent
    out["centre_minus_square1_places"] = rel
    out["pose_denominator_digits"] = {"min": min(dens), "max": max(dens)}
    out["direction_denominator_digits"] = sorted({len(str(F(a).denominator)) for (_, _, a, _) in poses})[:20]
    out["side_places"] = places(side)

    # near pairs with exact Euclidean gaps
    near = sorted((v, k) for k, v in m.items() if v < NEAR)
    out["near_pairs_below_1e-3"] = len(near)
    bands: dict[str, int] = {}
    for v, _ in near:
        e = "zero" if v == 0 else (f"1e{math.floor(math.log10(float(v))) if v > 0 else 'neg'}")
        bands[e] = bands.get(e, 0) + 1
    out["near_pair_bands"] = bands
    corners = [geom.corners(p) for p in poses]
    listed = []
    for v, (i, j) in near[:400]:
        if v > 0:
            g2 = min(
                min(geom.seg_dist2(pt, corners[o][k], corners[o][(k + 1) % 4]) for pt in corners[s] for k in range(4))
                for s, o in ((i, j), (j, i))
            )
            ratio = math.sqrt(float(g2 / (v * v))) if v > 0 else None
        else:
            g2, ratio = F(0), None
        listed.append({
            "pair": [i + 1, j + 1],
            "margin_sci": check.sci(v),
            "gap_sci": root_print(g2),
            "gap_over_margin": ratio,
            "kinds": ["axis" if rows[i]["axis"] else ("near-axis" if rows[i]["sin_from_axis"] < 1e-9 else "turned"),
                      "axis" if rows[j]["axis"] else ("near-axis" if rows[j]["sin_from_axis"] < 1e-9 else "turned")],
        })
    out["near_pairs"] = listed
    out["pairs_between_1e-60_and_1e-20"] = [
        {"pair": [i + 1, j + 1], "margin_sci": check.sci(v)} for v, (i, j) in near if F(1, 10**60) <= v < F(1, 10**20)
    ]
    degree = [0] * n
    for _, (i, j) in near:
        degree[i] += 1
        degree[j] += 1
    hist: dict[str, int] = {}
    for d in degree:
        hist[str(d)] = hist.get(str(d), 0) + 1
    out["near_pair_degree_histogram"] = hist
    above = sorted(v for v in m.values() if v >= NEAR)
    out["least_margin_at_or_above_1e-3"] = check.sci(above[0]) if above else None
    gaps_sorted = sorted(v for v, _ in near)
    jumps = []
    for a_, b_ in zip(gaps_sorted, gaps_sorted[1:], strict=False):
        if a_ > 0 and b_ / a_ > 10**6:
            jumps.append([check.sci(a_), check.sci(b_)])
    out["near_margin_jumps_over_1e6"] = jumps[:10]

    # walls
    names = ("left", "bottom", "right", "top")
    walls: dict[str, Any] = {}
    for w, name in enumerate(names):
        touching = [k for k in range(n) if cl[k][w] == 0]
        positive = sorted((cl[k][w], k) for k in range(n) if cl[k][w] > 0)
        walls[name] = {
            "contacts": [k + 1 for k in touching],
            "contact_kinds": {"axis (an edge)": sum(1 for k in touching if rows[k]["axis"]),
                              "turned (a corner)": sum(1 for k in touching if not rows[k]["axis"])},
            "next_clearances": [[k + 1, check.sci(c)] for c, k in positive[:8]],
            "below_1e-20": sum(1 for c, _ in positive if c < F(1, 10**20)),
            "at_the_least": [k + 1 for c, k in positive if c == positive[0][0]] if positive else [],
            "below_1e-20_list": [[k + 1, check.sci(c)] for c, k in positive if c < F(1, 10**20)],
            "below_1e-9": sum(1 for c, _ in positive if c < F(1, 10**9)),
        }
    out["walls"] = walls
    out["cpu_seconds"] = round(time.process_time() - t0, 1)
    Path(out_path).write_text(json.dumps(out, indent=1) + "\n")
    print(f"described {len(near)} near pairs, {len(axis)} axis-aligned squares, {len(visible)} visibly turned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
