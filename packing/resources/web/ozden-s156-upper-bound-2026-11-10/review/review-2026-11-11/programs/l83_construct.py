"""Measure what the issues' construction statements say; decides nothing (review L83).

Usage: python -I -B l83_construct.py N CERT.yaml POSE.yaml CHECK.json OUT.json

Wall clearances are exact (Fraction). The decimal pose is evaluated with mpmath at 60
digits and compared with the certificate: centres after the translation that puts the
pose's least corner coordinates at 0, angles, and every near pair's margin.
"""

from __future__ import annotations

import json
import statistics
import sys
from fractions import Fraction as F
from pathlib import Path

import mpmath

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l83_check as C  # noqa: E402
import l83_reader as R  # noqa: E402
import l83_sat as A  # noqa: E402

mpmath.mp.dps = 60
WALLS = ("left", "bottom", "right", "top")
BINS = [("contact", 0, 0), ("(0,1e-15)", 0, 1e-15), ("[1e-15,1e-13)", 1e-15, 1e-13), ("[1e-13,1e-12)", 1e-13, 1e-12), ("[1e-12,1e-9)", 1e-12, 1e-9), ("[1e-9,1e-3)", 1e-9, 1e-3)]


def mp(x: F):
    return mpmath.mpf(x.numerator) / x.denominator


def sat_mp(P, Q):
    """Pose margin (largest projection gap over the four axes) and its axis, at 60 digits."""
    best, best_axis = None, None
    for sq in (P, Q):
        for a in sq["axes"]:
            pa = [x * a[0] + y * a[1] for x, y in P["pts"]]
            qa = [x * a[0] + y * a[1] for x, y in Q["pts"]]
            g = max(min(qa) - max(pa), min(pa) - max(qa))
            if best is None or g > best:
                best, best_axis = g, a
    return best, best_axis


def pose_square(cx, cy, deg):
    t = mpmath.radians(deg)
    u = (mpmath.cos(t), mpmath.sin(t))
    v = (-u[1], u[0])
    p0 = (cx - u[0] / 2 - v[0] / 2, cy - u[1] / 2 - v[1] / 2)
    pts = [p0, (p0[0] + u[0], p0[1] + u[1]), (p0[0] + u[0] + v[0], p0[1] + u[1] + v[1]), (p0[0] + v[0], p0[1] + v[1])]
    return {"pts": pts, "axes": [u, v], "c": (cx, cy), "deg": deg}


def main(argv):
    n = int(argv[1])
    cert, pose_path, chk, out = Path(argv[2]), Path(argv[3]), json.loads(Path(argv[4]).read_text()), Path(argv[5])
    w = R.read_files(cert).witness
    S = F(*w.side)
    pts = [A.points(c) for c in w.corners]
    # walls, exact
    bins = {b[0]: {wl: 0 for wl in WALLS} for b in BINS}
    largest_below_1e12 = None
    beyond = []
    for k, p in enumerate(pts):
        cl = A.wall_clearances(p, S)
        for wl in WALLS:
            v = cl[wl]
            if v == 0:
                bins["contact"][wl] += 1
                continue
            fv = float(v)
            for name, lo, hi in BINS[1:]:
                if lo <= fv < hi:
                    bins[name][wl] += 1
            if fv < 1e-12 and (largest_below_1e12 is None or fv > largest_below_1e12[0]):
                largest_below_1e12 = (fv, w.ids[k], wl)
            if 1e-12 <= fv < 1e-3:
                beyond.append((w.ids[k], wl, fv))
    # the pose
    tree = R.compose_yaml(pose_path.read_text())
    pw = tree["witness"]
    pose = []
    for sq in pw["squares"]:
        pose.append(pose_square(mpmath.mpf(sq["center"][0]), mpmath.mpf(sq["center"][1]), mpmath.mpf(sq["angle"])))
    pside = mpmath.mpf(pw["side"])
    tx = min(min(x for x, _ in s["pts"]) for s in pose)
    ty = min(min(y for _, y in s["pts"]) for s in pose)
    ex = max(max(x for x, _ in s["pts"]) for s in pose) - tx
    ey = max(max(y for _, y in s["pts"]) for s in pose) - ty
    pose_wall = min(min(tx, ty), pside - (ex + tx), pside - (ey + ty))
    dc, da = mpmath.mpf(0), mpmath.mpf(0)
    for k, p in enumerate(pts):
        c = (mp((p[0][0] + p[2][0]) / 2), mp((p[0][1] + p[2][1]) / 2))
        q = pose[k]
        dc = max(dc, abs(c[0] - (q["c"][0] - tx)), abs(c[1] - (q["c"][1] - ty)))
        ang = mpmath.atan2(mp(p[1][1] - p[0][1]), mp(p[1][0] - p[0][0]))
        diff = ang - mpmath.radians(q["deg"])
        diff = diff - mpmath.pi / 2 * mpmath.nint(diff / (mpmath.pi / 2))
        da = max(da, abs(diff))
    # near pairs: pose margin vs exact certificate margin
    sqA = [A.Square(p) for p in pts]
    near = [(a - 1, b - 1) for a, b, m in chk["near_pairs_below_1e-9"] if m < 1e-12]
    dm = mpmath.mpf(0)
    ratios = []
    for i, j in near:
        mc = mp(A.pair_margin(sqA[i], sqA[j]))
        mpose, axis = sat_mp(pose[i], pose[j])
        dm = max(dm, abs(mc - mpose))
        sep = abs((pose[j]["c"][0] - pose[i]["c"][0]) * axis[0] + (pose[j]["c"][1] - pose[i]["c"][1]) * axis[1])
        ratios.append(float(mpose / sep))
    # tilts, exact
    on_axes = below_1e9 = upto_half = beyond_half = 0
    for s in sqA:
        ux, uy = s.axes[0]
        if ux == 0 or uy == 0:
            on_axes += 1
            continue
        t = abs(float(mpmath.atan2(mp(uy), mp(ux))))
        t = min(t % (mpmath.pi / 2), mpmath.pi / 2 - t % (mpmath.pi / 2))
        if t < 1e-9:
            below_1e9 += 1
        elif t <= float(mpmath.radians(0.5)):
            upto_half += 1
        else:
            beyond_half += 1
    # contact squares in the pose
    contact_pose = []
    for sid, wl in chk["wall_contacts"]:
        sq = pw["squares"][sid - 1]
        contact_pose.append({"id": sid, "wall": wl, "pose_center": sq["center"], "pose_angle": sq["angle"]})
    meta = chk["meta"]
    doc = {
        "n": n,
        "wall_clearance_bins": bins,
        "largest_clearance_below_1e-12": largest_below_1e12,
        "clearances_in_[1e-12,1e-3)": sorted(beyond, key=lambda x: x[2]),
        "contact_squares_in_pose": contact_pose,
        "pose_side": pw["side"],
        "pose_least_corner": [mpmath.nstr(tx, 6), mpmath.nstr(ty, 6)],
        "pose_least_wall_clearance_at_own_side": mpmath.nstr(pose_wall, 6),
        "pose_side_minus_certificate_side": mpmath.nstr(pside - mp(S), 6),
        "pose_extent_x_minus_y": mpmath.nstr(ex - ey, 6),
        "largest_centre_difference": mpmath.nstr(dc, 4),
        "largest_angle_difference_rad": mpmath.nstr(da, 4),
        "near_pairs": len(near),
        "largest_near_margin_difference": mpmath.nstr(dm, 4),
        "margin_over_axis_separation": {"min": min(ratios), "median": statistics.median(ratios), "max": max(ratios)} if ratios else None,
        "tilts": {"exactly_on_axes": on_axes, "below_1e-9_rad": below_1e9, "1e-9_rad_to_0.5deg": upto_half, "beyond_0.5deg": beyond_half},
        "certificate_meta": meta,
        "pose_id": pw["id"],
        "derived_from_is_pose_id": meta["certificate"]["derived_from"] == pw["id"],
        "source_path": meta["source"]["path"],
        "source_path_is_pose_file": meta["source"]["path"] == pose_path.name,
        "pose_softschema_schema": tree["softschema"]["schema"],
        "pose_claim": pw.get("claim"),
        "replay": meta["certificate"]["replay"],
        "replay_names_certificate_file": meta["certificate"]["replay"].endswith(" " + cert.name),
        "programs": C.program_digests(),
    }
    out.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: doc[k] for k in ("n", "wall_clearance_bins", "largest_clearance_below_1e-12", "pose_least_corner", "pose_least_wall_clearance_at_own_side", "pose_side_minus_certificate_side", "pose_extent_x_minus_y", "largest_centre_difference", "largest_angle_difference_rad", "near_pairs", "largest_near_margin_difference", "margin_over_axis_separation", "tilts", "derived_from_is_pose_id", "source_path_is_pose_file", "pose_softschema_schema", "replay_names_certificate_file")}))
    print("beyond 1e-12:", len(doc["clearances_in_[1e-12,1e-3)"]), doc["clearances_in_[1e-12,1e-3)"][:8])
    print("contacts in pose:", contact_pose)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
