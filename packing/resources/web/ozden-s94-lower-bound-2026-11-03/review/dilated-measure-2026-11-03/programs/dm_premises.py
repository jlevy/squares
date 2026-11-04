"""Every premise of the measure-capture theorem except coverage, in exact rationals.

Usage: dm_premises.py CERTIFICATE.json.gz HOSONO_CANDIDATE.json.gz OUT.json

Reads the certificate and Hosono's mixed_n94_L995 candidate with this review's own reader
(dmlib) and decides, apart from the crate and the import lane's audit tool:

- the file: format M, the keys present, the declared net, every row a nondegenerate
  rectangle inside [0, L]^2 with a nonnegative mass, the total mass and its declared value;
- the D4 expansion: distinct images, the merged densities, that it integrates back to M,
  the densest row (checklist item 1 asks 8 times its density to be at most 2^32);
- lemma N0 (a)-(e), the sharp shrink condition, L^2 >= 2 B^2, and M < n;
- the net's coverage of [0, tan(pi/8)] in half-angle tangent: every tangent has a node
  within D/2, which bin holds tan(pi/8), and that 599 is the least admissible `last`;
- the per-bin domain at every node: nonempty, and the core at the node's angle with its
  centre at the domain's end inside K (a consistency check of N3);
- the dilation: L, B and every row lambda times Hosono's, masses equal; the old net's
  shrink product; the centre domain's growth, in Hosono's coordinates, at the 200
  directions the two nets share; and the route's ceiling L0/B0.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

# Run with `python -I`, which leaves the script's directory off the path: add this
# directory, and only it, which holds nothing but this review's programs.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dmlib  # noqa: E402


def sign_vs_tan_pi8(t: Fraction) -> int:
    """The sign of t - (sqrt 2 - 1) for t >= 0, decided exactly by t^2 + 2t - 1."""
    value = t * t + 2 * t - 1
    return (value > 0) - (value < 0)


def main() -> None:
    cert_path, hosono_path, out_path = (Path(arg) for arg in sys.argv[1:4])
    started = time.process_time()
    read = dmlib.read_gzip_json(cert_path)
    base_read = dmlib.read_gzip_json(hosono_path)
    report = decide(read.data, base_read.data)
    report = {
        "program": "dm_premises.py",
        "program_sha256": dmlib.sha256_file(Path(__file__)),
        "dmlib_sha256": dmlib.sha256_file(Path(dmlib.__file__)),
        "certificate": {
            "path": cert_path.name,
            "file_sha256": read.raw_sha256,
            "json_text_sha256": read.text_sha256,
            "file_bytes": read.raw_bytes,
            "json_text_bytes": read.text_bytes,
            "keys": list(read.data),
        },
        "hosono_candidate": {
            "path": str(hosono_path.name),
            "file_sha256": base_read.raw_sha256,
            "json_text_sha256": base_read.text_sha256,
            "keys": list(base_read.data),
        },
        **report,
    }
    report["cpu_seconds"] = round(time.process_time() - started, 2)
    Path(out_path).write_text(dmlib.dumps(report, 3) + "\n")
    print(json.dumps({"status": report["status"], "problems": report["problems"]}, indent=1))


def decide(data: dict, base_data: dict) -> dict:
    """Every premise but coverage, for a certificate's parsed JSON beside Hosono's."""
    cert = dmlib.certificate(data)
    base = dmlib.certificate(base_data, require_net=False)
    report: dict = {}
    problems: list[str] = []

    # ---- the file
    n, side, core, step, last = cert.n, cert.side, cert.core, cert.step, cert.last
    unknown = sorted(set(cert.keys) - {"n", "L", "B", "total_mass", "points", "rectangles", "proof_net"})
    zero_mass = 0
    for index, (x1, y1, x2, y2, mass) in enumerate(cert.rows):
        if mass < 0:
            problems.append(f"row {index}: negative mass")
        if mass == 0:
            zero_mass += 1
        if not (0 <= x1 < x2 <= side and 0 <= y1 < y2 <= side):
            problems.append(f"row {index}: degenerate or outside [0, L]^2")
    mass = cert.mass
    if cert.total_mass_declared != mass:
        problems.append("total_mass is not the exact sum")
    # Reading the rows as [x1, x2, y1, y2] instead: how many would be degenerate?
    other_order_bad = sum(1 for x1, y1, x2, y2, _ in cert.rows if not (x1 < y1 and x2 < y2))
    report["file"] = {
        "n": n,
        "L": str(side),
        "B": str(core),
        "proof_net": {"step": str(step), "last": last, "count": cert.count},
        "rows": len(cert.rows),
        "rows_with_zero_mass": zero_mass,
        "keys_not_read_by_the_theorem": unknown,
        "has_top_level_net": "net" in cert.keys,
        "has_certificate_metadata": "certificate" in cert.keys,
        "has_scaling_factor": "scaling_factor" in cert.keys,
        "mass": str(mass),
        "mass_equals_declared_total": cert.total_mass_declared == mass,
        "n_minus_mass": str(n - mass),
        "rows_degenerate_if_read_as_x1_x2_y1_y2": other_order_bad,
    }

    # ---- the D4 expansion
    images = dmlib.expand(cert)
    integrated = sum((i.density * (i.x2 - i.x1) * (i.y2 - i.y1) for i in images), Fraction(0))
    row_density = [m / ((x2 - x1) * (y2 - y1)) for x1, y1, x2, y2, m in cert.rows if m > 0]
    densest_row = max(row_density)
    densest_image = max(i.density for i in images)
    total_density = sum((i.density for i in images), Fraction(0))
    report["expansion"] = {
        "distinct_images": len(images),
        "integrates_to_mass": integrated == mass,
        "eight_times_densest_row_density": dmlib.short(densest_row),
        "eight_times_densest_row_density_at_most_2^32": densest_row <= 2**32,
        "densest_merged_image": dmlib.short(densest_image),
        "densest_merged_image_at_most_2^96": densest_image <= 2**96,
        "sum_of_image_densities": dmlib.short(total_density),
        "images_symmetric": _symmetric(images, side),
    }
    if integrated != mass:
        problems.append("the expansion does not integrate to the mass")

    # ---- lemma N0 and the theorem's other premises
    t_max = step * last
    shrink = core * (1 + step)
    reach = t_max * t_max + 2 * t_max - 1
    tangent = core * (1 + step / (1 - step * step / 4))
    sharp = core * (1 + step - step * step / 4) / (1 + step * step / 4)
    premises = {
        "(a) D > 0 and 2 <= N <= 2^16": step > 0 and 2 <= cert.count <= 2**16,
        "(b) B(1 + D)": str(shrink),
        "(b) B(1 + D) < 1": shrink < 1,
        "(b) margin 1 - B(1 + D)": str(1 - shrink),
        "(c) t_max": str(t_max),
        "(c) t_max^2 + 2 t_max - 1": str(reach),
        "(c) holds": reach > 0,
        "(d) t_max <= 1/2": t_max <= Fraction(1, 2),
        "(e) B(1 + D/(1 - D^2/4))": str(tangent),
        "(e) holds": tangent < 1,
        "sharp N3: B(1 + D - D^2/4)/(1 + D^2/4)": str(sharp),
        "sharp N3 holds": sharp < 1,
        "0 < B < 1": 0 < core < 1,
        "L^2 >= 2 B^2": side * side >= 2 * core * core,
        "0 < M < n": 0 < mass < n,
        "largest D with B(1 + D) < 1 is below 1/B - 1": str(1 / core - 1),
    }
    for key in ("(b) B(1 + D) < 1", "(c) holds", "(d) t_max <= 1/2", "(e) holds", "0 < M < n"):
        if not premises[key]:
            problems.append(f"premise fails: {key}")
    if not premises["(a) D > 0 and 2 <= N <= 2^16"]:
        problems.append("premise (a) fails")
    report["premises"] = premises

    # ---- the net's coverage of [0, tan(pi/8)]
    holding = [
        r
        for r in range(cert.count)
        if sign_vs_tan_pi8(dmlib.bin_low(step, r)) <= 0 and sign_vs_tan_pi8(step * r + step / 2) >= 0
    ]
    least_last = next(m for m in range(1, 2**16) if sign_vs_tan_pi8(step * m) > 0)
    gaps = [r for r in range(1, cert.count) if step * r - step * (r - 1) != step]
    coverage = {
        "nodes": cert.count,
        "bins_tile_without_gap": not gaps,
        "union_of_bins": [str(-step / 2), str(t_max + step / 2)],
        "tan_pi8_lies_in_bins_of_nodes": holding,
        "t_last_minus_half_step_below_tan_pi8": sign_vs_tan_pi8(t_max - step / 2) < 0,
        "t_(last-1)_plus_half_step_below_tan_pi8": sign_vs_tan_pi8(step * (last - 1) + step / 2) < 0,
        "least_last_meeting_(c)": least_last,
        "every_node_bin_meets_[0,tan(pi/8)]": all(
            sign_vs_tan_pi8(dmlib.bin_low(step, r)) < 0 for r in range(cert.count)
        ),
    }
    if coverage["least_last_meeting_(c)"] > last or not coverage["bins_tile_without_gap"]:
        problems.append("the net does not cover [0, tan(pi/8)]")
    report["net_coverage"] = coverage

    # ---- the per-bin domain at every node
    least_room = None
    least_room_at = None
    empty = []
    uppers = {}
    for r in range(cert.count):
        low, high = dmlib.domain(cert, r)
        if high <= side / 2:
            empty.append(r)
        _, cos, sin = dmlib.node(step, r)
        room = low - core * (cos + sin) / 2
        if least_room is None or room < least_room:
            least_room, least_room_at = room, r
        if r in (0, 1, 2, 3, 144, 277, 297, 298, 299, 300, 597, 598, 599):
            uppers[r] = {"rho(a_r)": str(low), "U_r": str(high), "U_r_float": dmlib.short(high)}
    report["domain"] = {
        "empty_at": empty,
        "least_rho(a_r)_minus_core_half_extent": str(least_room),
        "least_rho(a_r)_minus_core_half_extent_float": dmlib.short(least_room),
        "at_node": least_room_at,
        "sampled": uppers,
    }
    if empty or least_room is None or least_room <= 0:
        problems.append("a per-bin domain is empty, or a core at the domain's end leaves K")

    # ---- the dilation: facts about how the candidate was made, not premises of the
    # theorem, so they are kept apart from `problems`
    lam = side / base.side
    rows_scaled = len(base.rows) == len(cert.rows) and all(
        all(a == lam * b for a, b in zip(new[:4], old[:4], strict=True)) and new[4] == old[4]
        for new, old in zip(cert.rows, base.rows, strict=True)
    )
    old_step = Fraction(83, 40000)
    old_shrink = core * (1 + old_step)
    dilation_facts: list[str] = []
    if not rows_scaled:
        dilation_facts.append("the rows are not lambda times Hosono's")
    report["dilation"] = {
        "lambda": str(lam),
        "L_is_lambda_L0": side == lam * base.side,
        "B_is_lambda_B0": core == lam * base.core,
        "B0": str(base.core),
        "L0": str(base.side),
        "every_row_lambda_times_hosono_in_order_with_equal_mass": rows_scaled,
        "hosono_mass": str(base.mass),
        "old_net_shrink_B(1 + 83/40000)": str(old_shrink),
        "old_net_admits_this_core": old_shrink < 1,
        "route_ceiling_L0_over_B0": str(base.side / base.core),
        "route_ceiling_float": dmlib.short(base.side / base.core),
        "claim_below_ceiling": side < base.side / base.core,
    }
    if 3 * step == old_step:
        growth = []
        for k in range(0, 200):
            r = 3 * k
            old_low = dmlib.rho(dmlib.bin_low(old_step, k))
            new_low_in_old = dmlib.rho(dmlib.bin_low(step, r)) / lam
            growth.append((old_low - new_low_in_old, r))
        least_growth, least_growth_at = min(growth)
        most_growth, most_growth_at = max(growth)
        shared = sum(1 for r in range(cert.count) if r % 3 == 0)
        report["dilation"].update(
            {
                "nodes_shared_with_hosono_net": shared,
                "shared_nodes_are_3k": all(step * 3 * k == old_step * k for k in range(200)),
                "new_nodes": cert.count - shared,
                "domain_growth_in_hosono_coordinates_at_r0": str(growth[0][0]),
                "domain_growth_least": [str(least_growth), dmlib.short(least_growth), least_growth_at],
                "domain_growth_most": [str(most_growth), dmlib.short(most_growth), most_growth_at],
                "domain_grows_at_every_shared_node": least_growth > 0,
            }
        )
    else:
        dilation_facts.append("the net is not a third of Hosono's step")
    report["dilation"]["facts_that_differ_from_the_source_README"] = dilation_facts

    report["problems"] = problems
    report["status"] = "PREMISES_HOLD" if not problems else "REFUSED"
    return report


def _symmetric(images: list, side: Fraction) -> bool:
    """Whether the expanded measure is invariant under the eight symmetries."""
    table = {(i.x1, i.y1, i.x2, i.y2): i.density for i in images}
    for image in images:
        for key in dmlib.d4_images(side, image.x1, image.y1, image.x2, image.y2):
            if table.get(key) != image.density:
                return False
    return True


if __name__ == "__main__":
    main()
