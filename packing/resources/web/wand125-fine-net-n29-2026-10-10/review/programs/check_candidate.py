"""Every exact premise of the check2 candidate mixed_n29_L582, recomputed apart
from the crate, the repository's tools and the source (review think-1lri).

Reads the packet's retained release/certificates/<cert>/candidate.json.gz and
source-manifest.json (for the pinned bytes and SHA-256), and prints a JSON receipt:

- custody: the retained .gz's digest, the decompressed bytes against the pin, the
  semantic digest of REPRODUCE.md's rule;
- the file: keys, format M, points empty, proof_net exactly {step, last}, no
  net / certificate / scaling_factor key, every number in a canonical exact form
  (fine_net_exact.rational refuses any other), no duplicate key;
- the claim: n and L against the claim on the command line;
- the measure (H1): rows positive, nondegenerate and inside [0, L]^2, the exact
  mass against total_mass and n - 1/100000, the distinct D4 images (the crate
  merges coincident ones), lemma F3's caps, the coordinate grid;
- the net (H2): lemma N0 (a) to (e), the sharp N3 extent, F3's step bounds;
- the fold (H4): the last bin [2071.5 D, 2072.5 D] holds tan(pi/8);
- lemma D's per-bin domain at every node: rho increasing, the domain nonempty,
  never wider than Tokoharu's, and its least width.

Usage: python3 -I check_candidate.py PACKET CERT N L_RATIONAL [--out FILE]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import resource
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fine_net_exact as fx  # noqa: E402


def lcm_den(values):
    out = 1
    for v in values:
        out = math.lcm(out, v.denominator)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("packet", type=Path)
    ap.add_argument("cert")
    ap.add_argument("n", type=int)
    ap.add_argument("L")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    claim_L = F(args.L)
    rec: dict = {"certificate": args.cert, "claim": {"n": args.n, "L": str(claim_L)}}
    problems: list[str] = []

    def need(ok, what):
        if not ok:
            problems.append(what)
        return ok

    manifest = json.loads((args.packet / "source-manifest.json").read_text())
    pinned = next(m for m in manifest["asset_members"] if m["path"] == "candidate.json")
    gz = args.packet / "release" / "certificates" / args.cert / "candidate.json.gz"
    cand = fx.load_candidate(gz)  # refuses duplicate keys, multi-member gzip, non-canonical numbers

    rec["custody"] = {
        "retained_gz_sha256": hashlib.sha256(gz.read_bytes()).hexdigest(),
        "candidate_bytes": len(cand.raw),
        "candidate_sha256": cand.file_sha256,
        "pinned_bytes": pinned["bytes"],
        "pinned_sha256": pinned["sha256"],
        "equal_to_pin": cand.file_sha256 == pinned["sha256"] and len(cand.raw) == pinned["bytes"],
        "semantic_digest": cand.semantic_digest(),
    }
    need(rec["custody"]["equal_to_pin"], "candidate bytes differ from the pin")

    doc = cand.doc
    keys = sorted(doc)
    rec["file"] = {
        "keys": keys,
        "format_M": bool(doc["rectangles"]) and all(isinstance(r, dict) for r in doc["rectangles"]),
        "points_empty": doc.get("points") == [],
        "proof_net": doc["proof_net"],
        "proof_net_keys_exactly_step_last": sorted(doc["proof_net"]) == ["last", "step"],
        "no_net_certificate_schema_or_scaling_factor_key": not ({"net", "certificate", "scaling_factor", "schema"} & set(doc)),
        "numbers_canonical_and_no_duplicate_key": True,  # load_candidate would have raised
        "L_text": doc["L"],
        "B_text": doc["B"],
        "step_text": doc["proof_net"]["step"],
        "total_mass_text": doc["total_mass"],
        "n": doc["n"],
    }
    need(keys == sorted(["n", "L", "B", "proof_net", "total_mass", "points", "rectangles"]), "unexpected keys")
    for k in ("format_M", "points_empty", "proof_net_keys_exactly_step_last", "no_net_certificate_schema_or_scaling_factor_key"):
        need(rec["file"][k], k)

    n, L, B, D, last = cand.n, cand.L, cand.B, cand.D, cand.last
    rec["claim"]["matches_file"] = n == args.n and L == claim_L
    need(rec["claim"]["matches_file"], "n or L differ from the claim")
    rec["claim"]["above"] = {
        "T-108 581/100": str(L - F(581, 100)),
        "#446 report 1163/200": str(L - F(1163, 200)),
        "mixed_n29_L58175 2327/400": str(L - F(2327, 400)),
    }

    # The measure (H1)
    rows = cand.rows
    masses = [m for _, m in rows]
    M = sum(masses, F(0))
    inside = all(0 <= x1 < x2 <= L and 0 <= y1 < y2 <= L for (x1, y1, x2, y2), _ in rows)
    sides = [min(x2 - x1, y2 - y1) for (x1, y1, x2, y2), _ in rows]
    wall = [min(x1, y1, L - x2, L - y2) for (x1, y1, x2, y2), _ in rows]
    merged: dict = {}
    sym_rows = 0
    for (x1, y1, x2, y2), m in rows:
        dens = m / (8 * (x2 - x1) * (y2 - y1))
        ims = fx.d4_images(L, x1, y1, x2, y2)
        if len(set(ims)) < 8:
            sym_rows += 1
        for im in ims:
            merged[im] = merged.get(im, F(0)) + dens
    image_dens = [m / (8 * (x2 - x1) * (y2 - y1)) for (x1, y1, x2, y2), m in rows]
    integrated = sum((d * (k[2] - k[0]) * (k[3] - k[1]) for k, d in merged.items()), F(0))
    rect_keys = [r for r, _ in rows]
    grid = lcm_den([v for (r, _) in rows for v in r])
    rec["measure"] = {
        "rows": len(rows),
        "repeated_rectangles": len(rect_keys) - len(set(rect_keys)),
        "all_positive": all(m > 0 for m in masses),
        "all_nondegenerate_inside_K": inside,
        "mass_exact": str(M),
        "total_mass": str(cand.total_mass),
        "mass_equals_total_mass": M == cand.total_mass,
        "n_minus_mass": str(n - M),
        "mass_is_n_minus_1e-5": M == n - F(1, 100000),
        "mass_below_n": M < n,
        "distinct_images": len(merged),
        "unmerged_images": 8 * len(rows),
        "rows_with_coincident_images": sym_rows,
        "merged_images_integrate_to_mass": integrated == M,
        "least_row_side": float(min(sides)),
        "least_distance_to_a_wall": float(min(wall)),
        "rows_touching_a_wall": sum(1 for w in wall if w == 0),
        "densest_image_m_over_8A": float(max(image_dens)),
        "eight_times_densest_row_m_over_A": float(64 * max(image_dens)),
        "densest_merged_image": float(max(merged.values())),
        "least_image_density": float(min(image_dens)),
        "caps": {
            "eight_times_densest_row_le_2^32": 64 * max(image_dens) <= 2**32,
            "merged_image_density_le_2^96": max(merged.values()) <= 2**96,
            "rows_le_10^6": len(rows) <= 10**6,
            "L_le_1000": L <= 1000,
        },
        "coordinate_denominator_lcm": grid,
        "coordinate_grid_is_decimal": _only_2_and_5(grid),
        "coordinate_grid_divides_10^17": 10**17 % grid == 0,
    }
    for k in ("all_positive", "all_nondegenerate_inside_K", "mass_equals_total_mass", "mass_is_n_minus_1e-5",
              "mass_below_n", "merged_images_integrate_to_mass"):
        need(rec["measure"][k], k)
    need(all(rec["measure"]["caps"].values()), "F3 caps")

    # The net: lemma N0
    N = last + 1
    tmax = last * D
    b_val = B * (1 + D)
    c_val = tmax * tmax + 2 * tmax - 1
    e_val = B * (1 + D / (1 - D * D / 4))
    sharp = B * (1 + D - D * D / 4) / (1 + D * D / 4)
    s1 = 2 * D / (1 + D * D)
    c_last, s_last = fx.direction(D, last)
    rec["lemma_N0"] = {
        "B": str(B), "D": str(D), "N_theta": N,
        "a_D_pos_and_2_le_N_le_2^16": D > 0 and 2 <= N <= 2**16,
        "b_B_1_plus_D": str(b_val), "b_margin": str(1 - b_val), "b_holds": b_val < 1,
        "c_t_max": str(tmax), "c_value": str(c_val), "c_holds": c_val > 0,
        "spec_form_(1+t_max)^2_gt_2": (1 + tmax) ** 2 > 2,
        "d_t_max_le_half": tmax <= F(1, 2),
        "e_value": str(e_val), "e_margin": str(1 - e_val), "e_holds": e_val < 1,
        "sharp_N3_extent_at_z_D_over_2": str(sharp), "sharp_holds": sharp < 1,
        "F3_D_gt_2^-18": D > F(1, 2**18),
        "F3_s1": float(s1), "F3_s1_gt_2^-18": s1 > F(1, 2**18),
        "F3_c_at_last_node": str(c_last), "F3_c_at_last_node_ge_3/5": c_last >= F(3, 5),
        "core_0_lt_B_lt_1": 0 < B < 1,
        "L2_ge_2B2": L * L >= 2 * B * B,
        "mass_0_lt_M_lt_n": 0 < M < n,
    }
    for k in ("a_D_pos_and_2_le_N_le_2^16", "b_holds", "c_holds", "spec_form_(1+t_max)^2_gt_2", "d_t_max_le_half",
              "e_holds", "sharp_holds", "F3_D_gt_2^-18", "F3_s1_gt_2^-18", "F3_c_at_last_node_ge_3/5",
              "core_0_lt_B_lt_1", "L2_ge_2B2", "mass_0_lt_M_lt_n"):
        need(rec["lemma_N0"][k], "N0 " + k)

    # The fold (H4)
    def below_pi8(t):  # for t >= 0: t < tan(pi/8) iff t^2 + 2t - 1 < 0
        return t * t + 2 * t - 1 < 0

    lo_last = (last - F(1, 2)) * D
    hi_last = (last + F(1, 2)) * D
    rec["fold"] = {
        "last_bin": [str(lo_last), str(hi_last)],
        "last_bin_low_below_tan_pi8": below_pi8(lo_last),
        "last_bin_low_poly": str(lo_last * lo_last + 2 * lo_last - 1),
        "last_bin_high_above_tan_pi8": not below_pi8(hi_last),
        "node_2071_bin_high_below_tan_pi8": below_pi8((last - 1 + F(1, 2)) * D),
        "t_max_past_tan_pi8": not below_pi8(tmax),
        "t_max_minus_tan_pi8_approx": float(tmax) - (math.sqrt(2) - 1),
    }
    need(rec["fold"]["last_bin_low_below_tan_pi8"] and rec["fold"]["last_bin_high_above_tan_pi8"], "fold")

    # Lemma D's per-bin domain
    lows = [fx.rho(fx.bin_low(D, r)) for r in range(N)]
    every_a_below = all(below_pi8(fx.bin_low(D, r)) for r in range(N))
    increasing = all(lows[r + 1] > lows[r] for r in range(N - 1))
    widths = [L - 2 * lo for lo in lows]
    rmin = min(range(N), key=lambda r: widths[r])
    tok = [fx.tokoharu_half(cand, r) for r in range(N)]
    rec["per_bin_domain"] = {
        "every_a_r_below_tan_pi8": every_a_below,
        "rho_a_r_strictly_increasing_in_r": increasing,
        "a_0_a_1_a_last": [str(fx.bin_low(D, 0)), str(fx.bin_low(D, 1)), str(fx.bin_low(D, last))],
        "domain_at_0": [str(lows[0]), str(L - lows[0])],
        "least_width": float(widths[rmin]),
        "least_width_node": rmin,
        "nonempty_everywhere_U_r_gt_L/2": all(L - lo > L / 2 for lo in lows),
        "rho_a_last": float(lows[-1]),
        "per_bin_low_ge_tokoharu_low_at_every_node": all(lows[r] >= tok[r] for r in range(N)),
        "least_per_bin_minus_tokoharu": float(min(lows[r] - tok[r] for r in range(N))),
    }
    need(every_a_below and increasing and rec["per_bin_domain"]["nonempty_everywhere_U_r_gt_L/2"], "per-bin domain")
    need(rec["per_bin_domain"]["per_bin_low_ge_tokoharu_low_at_every_node"], "a core at the domain's corner leaves K")

    ru = resource.getrusage(resource.RUSAGE_SELF)
    rec["cpu_seconds"] = ru.ru_utime + ru.ru_stime
    rec["problems"] = problems
    rec["status"] = "ALL_PREMISES_HOLD" if not problems else "PREMISE_FAILED"
    text = json.dumps(rec, indent=1)
    if args.out:
        args.out.write_text(text + "\n")
    print(text)
    return 0 if not problems else 1


def _only_2_and_5(m: int) -> bool:
    for p in (2, 5):
        while m % p == 0:
            m //= p
    return m == 1


if __name__ == "__main__":
    sys.exit(main())
