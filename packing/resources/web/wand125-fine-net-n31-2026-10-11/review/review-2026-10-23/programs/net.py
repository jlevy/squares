"""The declared net of mixed_n31_L59775 covers every orientation, exactly.

Usage: python3 -I net.py CANDIDATE.json[.gz] OUTPUT.json

Re-derives the reduction from a packing to the capture condition on the net, in exact
rationals, node by node, rather than from the closed-form premise B(1 + D) < 1 alone:

1. Fold. A unit square's orientation is defined modulo a quarter turn; a reflection of
   the container maps orientation phi to -phi, so every square has an image under D4
   with phi in [0, pi/4], that is, half-angle tangent t in [0, tan(pi/8)].
2. Bins. Node j has tangent t_j = j D and bin [t_j - D/2, t_j + D/2]; consecutive bins
   abut, bin 0 starts at 0, and the last bin reaches past tan(pi/8)
   ((t_last + D/2)^2 + 2(t_last + D/2) - 1 > 0 is implied by t_last^2 + 2t_last - 1 > 0,
   checked).
3. Containment. For t in bin j, the relative turn delta between the square and the core
   at theta_j has tan(|delta|/2) = z = |t - t_j|/(1 + t t_j), which increases with
   |t - t_j| on each side of t_j; the core of side B fits strictly inside the square iff
   B (cos delta + sin|delta|) = B (1 - z^2 + 2z)/(1 + z^2) < 1, increasing in z for
   |delta| <= pi/4. So it suffices to check both ends of every bin, which this program
   does with exact z (2,073 x 2 inequalities), and it also checks the uniform bound
   B (1 + 2 z_max) <= B (1 + D) < 1.
4. Centre domain. r(t) = (1 + 2t - t^2)/(2(1 + t^2)) has derivative
   (1 - 2t - t^2)/(1 + t^2)^2, positive below tan(pi/8); so every square in bin j has
   its centre in [r(a_j), L - r(a_j)]^2 with a_j = max(0, t_j - D/2). Checked: the
   numerator's sign at every a_j that lies below tan(pi/8), and nonemptiness.
5. Quarter turn. The rotation by pi/2 about (L/2, L/2) maps a core at angle theta_j to
   a core at the same angle, and maps [r, L - r]^2 onto itself; the four images of the
   quadrant [L/2, L - r]^2 cover it. Checked on the corners exactly.

Prints a verdict and writes the least margins to OUTPUT.json.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import n31_exact as nx  # noqa: E402


def fr(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def extent(core: Fraction, z: Fraction) -> Fraction:
    return core * (1 - z * z + 2 * z) / (1 + z * z)


def main() -> int:
    start = time.process_time()
    cand = nx.read_candidate(Path(sys.argv[1]))
    out_path = Path(sys.argv[2])
    side, core, d, last = cand["L"], cand["B"], cand["step"], cand["last"]
    checks: dict[str, bool] = {}
    facts: dict[str, object] = {}

    t_last = last * d
    checks["last_tangent_past_tan_pi_8"] = t_last * t_last + 2 * t_last - 1 > 0
    reach = t_last + d / 2
    checks["last_bin_reaches_past_tan_pi_8"] = reach * reach + 2 * reach - 1 > 0
    checks["bins_abut"] = all((j * d + d / 2) == ((j + 1) * d - d / 2) for j in range(last))
    checks["bin_0_starts_at_0"] = 0 * d == 0

    worst_extent = Fraction(0)
    worst_at = None
    uniform_ok = True
    for j in range(last + 1):
        tj = j * d
        for t in (max(Fraction(0), tj - d / 2), tj + d / 2):
            z = abs(t - tj) / (1 + t * tj)
            ext = extent(core, z)
            if ext > worst_extent:
                worst_extent, worst_at = ext, (j, fr(t) if t else "0")
            if not core * (1 + 2 * z) <= core * (1 + d):
                uniform_ok = False
    checks["core_strictly_inside_at_every_bin_end"] = worst_extent < 1
    checks["uniform_bound_B_1_plus_2z_at_most_B_1_plus_D"] = uniform_ok
    facts["largest_extent"] = fr(worst_extent)
    facts["largest_extent_margin"] = fr(1 - worst_extent)
    facts["largest_extent_at"] = worst_at

    # Lemma D: r increases on [0, tan(pi/8)]; every a_j below tan(pi/8) has
    # 1 - 2a - a^2 > 0, and the per-bin domain is nonempty.
    mono_ok = True
    nonempty_ok = True
    least_width = None
    for j in range(last + 1):
        a = max(Fraction(0), j * d - d / 2)
        below = a * a + 2 * a - 1 < 0
        if not below:
            mono_ok = False  # an a_j past tan(pi/8) only enlarges the set; flagged
        w = side - 2 * nx.r_of(a)
        if w <= 0:
            nonempty_ok = False
        if least_width is None or w < least_width:
            least_width = w
    checks["every_a_j_below_tan_pi_8"] = mono_ok
    checks["per_bin_domain_nonempty"] = nonempty_ok
    facts["least_domain_width"] = fr(least_width)

    # Quarter turn about the centre: (x, y) -> (L - y, x). The quadrant's four images
    # cover the domain: check each corner of [r, L - r]^2 lies in one image.
    half = side / 2

    def rot(p):
        return (side - p[1], p[0])

    cover_all = True
    for j in range(last + 1):
        r0 = nx.r_of(max(Fraction(0), j * d - d / 2))
        quad = [(half, half), (side - r0, half), (half, side - r0), (side - r0, side - r0)]
        images = [quad]
        for _ in range(3):
            images.append([rot(p) for p in images[-1]])
        boxes = [(min(p[0] for p in im), max(p[0] for p in im), min(p[1] for p in im),
                  max(p[1] for p in im)) for im in images]
        corners = [(r0, r0), (side - r0, r0), (r0, side - r0), (side - r0, side - r0),
                   (half, r0), (r0, half), (half, half)]
        cover_ok = all(any(b[0] <= x <= b[1] and b[2] <= y <= b[3] for b in boxes)
                       for x, y in corners)
        inside = all(r0 <= b[0] and b[1] <= side - r0 and r0 <= b[2] and b[3] <= side - r0
                     for b in boxes)
        union_area = sum((b[1] - b[0]) * (b[3] - b[2]) for b in boxes)
        if not (cover_ok and inside and union_area == (side - 2 * r0) ** 2):
            cover_all = False
    checks["quarter_turn_images_tile_domain_at_every_node"] = cover_all
    status = "NET_COVERS" if all(checks.values()) else "NET_FAILS"
    out = {"kind": "review-2026-10-23-n31-net/v1", "status": status, "checks": checks,
           "facts": facts, "program_sha256": nx.sha256_file(Path(__file__)),
           "module_sha256": nx.sha256_file(Path(nx.__file__)),
           "candidate_sha256": cand["sha256"],
           "cpu_seconds": round(time.process_time() - start, 3)}
    out_path.write_text(json.dumps(out, indent=1) + "\n")
    print(status, {k: v for k, v in checks.items() if not v} or "all checks true",
          f"cpu {out['cpu_seconds']} s")
    return 0 if status == "NET_COVERS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
