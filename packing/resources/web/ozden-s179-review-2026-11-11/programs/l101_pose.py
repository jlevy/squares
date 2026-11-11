"""Compare the certificate with the decimal pose it was promoted from. Decides nothing.

Usage: python -I -B l101_pose.py SOURCE_DIR CHECK.json OUT.json

At 60 digits (mpmath): the pose's corners, its least corner coordinates (the translation
the promotion removed), each certificate centre against the translated pose centre, each
edge direction modulo 90 degrees against the pose angle, the near pairs' margins in the
pose against the certificate's exact ones, and each near pair's margin as a share of its
centres' separation along the binding axis (what a uniform scaling by a relative epsilon
leaves). Also the tilt census of the pose.
"""

from __future__ import annotations

import json
import statistics
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.set_int_max_str_digits(0)

import mpmath  # noqa: E402
import yaml  # noqa: E402

import l101_geom as geom  # noqa: E402
import l101_reader as reader  # noqa: E402
from l101_check import sha256_file  # noqa: E402

mpmath.mp.dps = 60
mpf = mpmath.mpf


def m(x: F) -> mpmath.mpf:
    return mpf(x.numerator) / mpf(x.denominator)


def pose_corners(cx, cy, deg):
    t = mpmath.radians(deg)
    c, s = mpmath.cos(t), mpmath.sin(t)
    h = mpf(1) / 2
    local = [(-h, -h), (h, -h), (h, h), (-h, h)]
    return [(cx + c * x - s * y, cy + s * x + c * y) for x, y in local], (c, s)


def sat_margin(pa, ua, pb, ub):
    """Margin and binding axis of two squares given corners and edge directions."""
    best = None
    axes = [ua, (-ua[1], ua[0]), ub, (-ub[1], ub[0])]
    for a in axes:
        va = [x * a[0] + y * a[1] for x, y in pa]
        vb = [x * a[0] + y * a[1] for x, y in pb]
        gap = max(min(vb) - max(va), min(va) - max(vb))
        if best is None or gap > best[0]:
            best = (gap, a)
    return best


def mod90(rad):
    q = mpmath.pi / 2
    r = rad % q
    return r - q if r > q / 2 else r


def main() -> int:
    src, check_path, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    pose = yaml.safe_load((src / "n-179-decimal-pose.yaml").read_text(encoding="utf-8"))["witness"]
    w = reader.read_files(src / "n-179-candidate.yaml", src / "n179-witness.json", 179)
    check = json.loads(check_path.read_text(encoding="utf-8"))
    assert pose["representation"] == "center-angle" and pose["coordinates"]["angle_unit"] == "degrees"
    pc, pu = [], []
    for k, sq in enumerate(pose["squares"]):
        assert sq["id"] == k + 1
        corners, u = pose_corners(mpf(sq["center"][0]), mpf(sq["center"][1]), mpf(sq["angle"]))
        pc.append(corners)
        pu.append(u)
    minx = min(x for cs in pc for x, _ in cs)
    miny = min(y for cs in pc for _, y in cs)
    maxx = max(x for cs in pc for x, _ in cs)
    maxy = max(y for cs in pc for _, y in cs)
    pose_side = mpf(pose["side"])
    cert_side = m(F(*w.side))
    centre_diff = []
    angle_diff = []
    for k, sq in enumerate(w.squares):
        c = geom.centre(sq)
        p = geom.to_fracs(sq)
        u = (m(p[1][0] - p[0][0]), m(p[1][1] - p[0][1]))
        pcx = mpf(pose["squares"][k]["center"][0]) - minx
        pcy = mpf(pose["squares"][k]["center"][1]) - miny
        centre_diff.append(max(abs(m(c[0]) - pcx), abs(m(c[1]) - pcy)))
        a_cert = mpmath.atan2(u[1], u[0])
        a_pose = mpmath.radians(mpf(pose["squares"][k]["angle"]))
        angle_diff.append(abs(mod90(a_cert - a_pose)))
    near = []
    for entry in check["near_pairs_exact"]:
        i, j = (k - 1 for k in entry["pair"])
        num, den = (int(x) for x in entry["value"].split("/"))
        exact = mpf(num) / mpf(den)
        pm, _ = sat_margin(pc[i], pu[i], pc[j], pu[j])
        cert_pts_i = [(m(x), m(y)) for x, y in geom.to_fracs(w.squares[i])]
        cert_pts_j = [(m(x), m(y)) for x, y in geom.to_fracs(w.squares[j])]
        ui = (cert_pts_i[1][0] - cert_pts_i[0][0], cert_pts_i[1][1] - cert_pts_i[0][1])
        uj = (cert_pts_j[1][0] - cert_pts_j[0][0], cert_pts_j[1][1] - cert_pts_j[0][1])
        cm, axis = sat_margin(cert_pts_i, ui, cert_pts_j, uj)
        ci, cj = geom.centre(w.squares[i]), geom.centre(w.squares[j])
        sep = abs((m(cj[0]) - m(ci[0])) * axis[0] + (m(cj[1]) - m(ci[1])) * axis[1])
        near.append({"pair": entry["pair"], "pose_less_exact": float(pm - exact),
                     "mp_less_exact": float(cm - exact), "ratio": float(exact / sep)})
    tilts = [abs(mod90(mpmath.radians(mpf(sq["angle"])))) for sq in pose["squares"]]
    deg = [float(mpmath.degrees(mod90(mpmath.radians(mpf(sq["angle"]))))) for sq in pose["squares"]]
    ratios = [x["ratio"] for x in near]
    pose_clear = {
        "left": float(minx), "bottom": float(miny),
        "right": float(pose_side - maxx), "top": float(pose_side - maxy),
    }
    receipt = {
        "program": "l101_pose.py",
        "pose_sha256": sha256_file(src / "n-179-decimal-pose.yaml"),
        "certificate_sha256": sha256_file(src / "n-179-candidate.yaml"),
        "pose_id": pose["id"], "pose_side": pose["side"], "pose_claim": pose["claim"],
        "pose_least_corner": [float(minx), float(miny)],
        "pose_extent_x_less_y": float((maxx - minx) - (maxy - miny)),
        "pose_clearances_at_own_side": pose_clear,
        "pose_side_less_certificate_side": float(pose_side - cert_side),
        "cert_side_less_pose_extent_x": float(cert_side - (maxx - minx)),
        "cert_side_less_pose_extent_y": float(cert_side - (maxy - miny)),
        "largest_centre_difference": float(max(centre_diff)),
        "largest_angle_difference_rad": float(max(angle_diff)),
        "near_pairs": len(near),
        "largest_near_margin_difference_pose": max(abs(x["pose_less_exact"]) for x in near),
        "largest_near_margin_difference_mp_cert": max(abs(x["mp_less_exact"]) for x in near),
        "ratio_min": min(ratios), "ratio_median": statistics.median(ratios), "ratio_max": max(ratios),
        "tilts": {
            "exactly_on_axes": sum(1 for t in tilts if t == 0),
            "below_1e-9_rad": sum(1 for t in tilts if 0 < t < mpf(10) ** -9),
            "1e-9_rad_to_0.5_deg": sum(1 for t in tilts if mpf(10) ** -9 <= t <= mpmath.radians(mpf("0.5"))),
            "beyond_0.5_deg": sum(1 for t in tilts if t > mpmath.radians(mpf("0.5"))),
            "beyond_1_deg": sum(1 for t in tilts if t > mpmath.radians(1)),
        },
        "tilted_degrees_sorted": sorted(round(d, 4) for d in deg if abs(d) > 0.5),
    }
    out.write_text(json.dumps(receipt, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in receipt.items() if k not in {"pose_claim"}}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
