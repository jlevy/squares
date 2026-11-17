"""The certificate against its decimal pose, and how far a uniform contraction can go.

Lane L108, blind stage 4 review of jlevy/squares#959. Written after the findings were
frozen; decides nothing. 60-digit mpmath throughout.

Part 1 compares the certificate's centres and angles with the decimal pose's.
Part 2 measures, for every pair, the largest relative gap rho = max over the four edge
normals a of gap_a / |a . (c_j - c_i)|: scaling every centre by any mu >= 1 - rho keeps
the pair apart, so 1 - min(rho) is the least uniform scale that keeps every pair apart.
It then scales the centres by that mu, re-places the squares against the left and bottom
walls, and reports the side the scaled packing needs, against s(70) + 5. For the walls
it compares each near-wall clearance with delta * (e_k - e_min), the clearance a uniform
dilation by 1 + delta of a packing in which those squares touched the wall would leave
(e the half-extent along the wall's normal).

Usage: python -I -B l108_pose.py CERT.yaml POSE.yaml REPO_ROOT OUT.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import mpmath

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l108_wit as wit  # noqa: E402

mpmath.mp.dps = 60


_CS: dict[int, tuple[Any, Any]] = {}


def _cs(p: wit.Pose) -> tuple[Any, Any]:
    key = id(p)
    if key not in _CS:
        r = mpmath.radians(p.deg)
        _CS[key] = (mpmath.cos(r), mpmath.sin(r))
    return _CS[key]


def axes(p: wit.Pose) -> list[tuple[Any, Any]]:
    c, s = _cs(p)
    return [(c, s), (-s, c)]


def width(p: wit.Pose, a: tuple[Any, Any]) -> Any:
    c, s = _cs(p)
    return abs(a[0] * c + a[1] * s) + abs(-a[0] * s + a[1] * c)


def pair_rho(p: wit.Pose, q: wit.Pose) -> tuple[Any, Any, Any]:
    """(margin, binding-axis separation r_b, rho = max_a gap_a / r_a)."""
    dx, dy = q.cx - p.cx, q.cy - p.cy
    best_gap, best_r, best_rho = None, None, None
    for a in axes(p) + axes(q):
        r = abs(a[0] * dx + a[1] * dy)
        h = (width(p, a) + width(q, a)) / 2
        gap = r - h
        if best_gap is None or gap > best_gap:
            best_gap, best_r = gap, r
        if r > 0:
            rho = gap / r
            if best_rho is None or rho > best_rho:
                best_rho = rho
    return best_gap, best_r, best_rho


def extents(poses: list[wit.Pose], mu: Any) -> dict[str, Any]:
    xs_lo = min(mu * p.cx - p.ex for p in poses)
    ys_lo = min(mu * p.cy - p.ex for p in poses)
    xs_hi = max(mu * p.cx + p.ex for p in poses)
    ys_hi = max(mu * p.cy + p.ex for p in poses)
    return {"x": xs_hi - xs_lo, "y": ys_hi - ys_lo, "x_lo": xs_lo, "y_lo": ys_lo}


def q(x: Any, d: int = 6) -> str:
    return mpmath.nstr(x, d)


def main(argv: list[str]) -> int:
    cert = wit.load(Path(argv[1]), "certificate")
    pose = wit.load(Path(argv[2]), "pose")
    p70 = wit.load(Path(argv[3]) / "packing/witnesses/known-best/n-070.yaml", "n-070")
    s = cert.side
    n = cert.n
    out: dict[str, Any] = {"program": "l108_pose.py"}

    # Part 1.
    ext_pose = extents(pose.poses, 1)
    tx = [c.cx - p.cx for c, p in zip(cert.poses, pose.poses, strict=True)]
    ty = [c.cy - p.cy for c, p in zip(cert.poses, pose.poses, strict=True)]
    dang = [abs(c.deg - p.deg) for c, p in zip(cert.poses, pose.poses, strict=True)]
    out["pose"] = {
        "pose_side": q(pose.side, 20),
        "pose_least_corner": [q(ext_pose["x_lo"]), q(ext_pose["y_lo"])],
        "pose_extent_x": q(ext_pose["x"], 20),
        "pose_extent_y": q(ext_pose["y"], 20),
        "pose_side_less_certificate_side": q(pose.side - s),
        "certificate_side_less_pose_extent_x": q(s - ext_pose["x"]),
        "certificate_side_less_pose_extent_y": q(s - ext_pose["y"]),
        "translation_mean": [q(sum(tx) / n, 12), q(sum(ty) / n, 12)],
        "translation_spread": [q(max(tx) - min(tx)), q(max(ty) - min(ty))],
        "translation_plus_least_corner": [q(sum(tx) / n + ext_pose["x_lo"]), q(sum(ty) / n + ext_pose["y_lo"])],
        "largest_angle_difference_deg": q(max(dang)),
        "pose_least_wall_clearance_at_own_side": q(min(min(p.cx - p.ex, p.cy - p.ex, pose.side - p.cx - p.ex, pose.side - p.cy - p.ex) for p in pose.poses)),
        "tilts": {
            "exactly_upright_in_certificate": sum(1 for p in cert.poses if p.deg == 0),
            "below_1e-9_rad": sum(1 for p in cert.poses if abs(mpmath.radians(p.deg)) < mpmath.mpf("1e-9")),
            "beyond_0.5_deg": sum(1 for p in cert.poses if abs(p.deg) > mpmath.mpf("0.5")),
            "beyond_1_deg": sum(1 for p in cert.poses if abs(p.deg) > 1),
        },
    }

    # Part 2: rho for every pair.
    rows: list[tuple[Any, Any, Any, int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            gap, r, rho = pair_rho(cert.poses[i], cert.poses[j])
            rows.append((rho, gap, r, i + 1, j + 1))
    near = sorted((row for row in rows if row[1] < mpmath.mpf("1e-12")), key=lambda t: t[0])
    rhos = [row[0] for row in near]
    rho_all_min = min(rows, key=lambda t: t[0])
    mid = rhos[len(rhos) // 2]
    out["dilation"] = {
        "near_pairs": len(near),
        "near_margin_range": [q(min(r[1] for r in near)), q(max(r[1] for r in near))],
        "near_binding_separation_range": [q(min(r[2] for r in near)), q(max(r[2] for r in near))],
        "rho_near_min": [q(rhos[0], 10), near[0][3], near[0][4]],
        "rho_near_median": q(mid, 10),
        "rho_near_max": [q(rhos[-1], 10), near[-1][3], near[-1][4]],
        "rho_near_within_1pct_of_median": sum(1 for x in rhos if abs(x - mid) < mid / 100),
        "rho_near_within_5pct_of_median": sum(1 for x in rhos if abs(x - mid) < mid / 20),
        "rho_all_pairs_min": [q(rho_all_min[0], 10), rho_all_min[3], rho_all_min[4]],
        "rho_deciles": [q(rhos[k * (len(rhos) - 1) // 10], 6) for k in range(11)],
    }
    s70p5 = p70.side + 5
    for label, rho in (("at_min_rho", rho_all_min[0]), ("at_median_rho", mid)):
        mu = 1 - rho
        e = extents(cert.poses, mu)
        side_needed = max(e["x"], e["y"])
        out["dilation"][f"contracted_{label}"] = {
            "mu": q(mu, 20),
            "side_needed": q(side_needed, 20),
            "side_needed_less_s70_plus_5": q(side_needed - s70p5),
            "extent_x_less_s70_plus_5": q(e["x"] - s70p5),
            "extent_y_less_s70_plus_5": q(e["y"] - s70p5),
        }
    out["dilation"]["side_less_s70_plus_5"] = q(s - s70p5)
    out["dilation"]["side_less_s70_plus_5_over_side_less_1"] = q((s - s70p5) / (s - 1), 10)

    # Walls: measured clearance against delta * (e_k - e_min) among the near-wall squares.
    delta = mid
    walls: dict[str, Any] = {}
    for name in ("left", "bottom", "right", "top"):
        vals = []
        for k, p in enumerate(cert.poses, start=1):
            v = {"left": p.cx - p.ex, "bottom": p.cy - p.ex, "right": s - p.cx - p.ex, "top": s - p.cy - p.ex}[name]
            if v < mpmath.mpf("1e-12"):
                vals.append((k, v, p.ex, p.deg))
        if not vals:
            continue
        emin = min(x[2] for x in vals)
        resid = [abs(v - delta * (ex - emin)) for _k, v, ex, _d in vals]
        walls[name] = {
            "near_squares": len(vals),
            "tilted_beyond_1_deg": [[k, q(v), q(d, 6)] for k, v, _ex, d in vals if abs(d) > 1],
            "largest_clearance": q(max(x[1] for x in vals)),
            "largest_residual_vs_dilation": q(max(resid)),
        }
    out["walls_vs_dilation"] = walls
    Path(argv[4]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
