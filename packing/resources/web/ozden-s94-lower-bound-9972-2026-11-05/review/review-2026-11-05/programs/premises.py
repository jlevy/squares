"""Exact premises of #910's certificate, recomputed for the think-xzxd review.

Reads the certificate (gzip and JSON text), Hosono's mixed_n94_L995 candidate and the
lab's 99/100 mutant, and decides in exact rationals (gmpy2.mpq):

- the file's format M shape, masses, containment and total;
- lemma N0 (a)-(e) of sqverify_fast/SOUNDNESS.md on the declared net, the admission
  caps, and the endpoint bin's coverage of tan(pi/8);
- the D4 expansion (distinct images, merged densities, integral = M) and that the
  expanded density is invariant under all eight symmetries of K, the quarter turn
  included (lemma C1);
- per-bin domains for every node r: U_r > L/2 and the core's own half-extent
  B rho(t_r) below the margin rho(a_r);
- the dilation: each row is lambda = 4986/4975 times Hosono's, masses equal; a
  byte-for-byte regeneration of the JSON text and of its gzip by this program's own
  rule (sorted keys, compact separators, level 9, mtime 0);
- what the dilation does not carry: the shared nodes with Hosono's net, the centre
  domain's growth there in Hosono's coordinates, Hosono's net with the dilated core,
  and the route's ceiling L0/B0;
- the mutant: every mass exactly 99/100 of the certificate's, nothing else changed but
  derived_from.

Usage: premises.py PACKET_DIR HOSONO_CANDIDATE_GZ OUT_JSON
"""

from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

from gmpy2 import mpq

from xzcommon import (
    d4_images,
    direction,
    expand,
    frac_str,
    load_certificate,
    read_bytes,
    rho_half_width,
    sha256,
    strict_json,
)


def main() -> int:
    packet = Path(sys.argv[1])
    hosono_path = Path(sys.argv[2])
    out_path = Path(sys.argv[3])
    src = packet / "source"
    gz_path = src / "certificate" / "n94-L9972.json.gz"
    txt_path = src / "certificate" / "n94-L9972.json"
    rep: dict[str, object] = {}
    checks: dict[str, bool] = {}

    gz_raw = gz_path.read_bytes()
    text = read_bytes(gz_path)
    rep["certificate_gz_sha256"] = sha256(gz_raw)
    rep["certificate_json_sha256"] = sha256(text)
    checks["json_text_is_gzip_content"] = text == txt_path.read_bytes()

    cert = load_certificate(gz_path)
    obj = cert.raw
    checks["top_level_keys"] = set(obj) == {
        "B", "L", "derived_from", "n", "points", "proof_net", "rectangles", "total_mass",
    }
    checks["points_empty"] = obj["points"] == []
    net = obj["proof_net"]
    assert isinstance(net, dict)
    checks["proof_net_keys_step_last"] = set(net) == {"step", "last"}
    checks["n_is_94"] = cert.n == 94
    L, B, D, last = cert.L, cert.B, cert.D, cert.last
    rep["L"], rep["B"], rep["D"], rep["last"] = frac_str(L), frac_str(B), frac_str(D), last
    checks["L_is_2493/250"] = L == mpq(2493, 250)
    rows = cert.rows
    rep["rows"] = len(rows)
    checks["masses_nonnegative"] = all(w >= 0 for w, _ in rows)
    checks["rectangles_nondegenerate_in_K"] = all(
        0 <= x1 < x2 <= L and 0 <= y1 < y2 <= L for _, (x1, y1, x2, y2) in rows
    )
    M = sum((w for w, _ in rows), mpq(0))
    checks["total_mass_is_sum"] = M == cert.total_mass
    rep["M"] = frac_str(M)
    checks["M_is_94_minus_1e-5"] = M == mpq(94) - mpq(1, 100000)
    checks["M_below_n"] = 0 < M < cert.n

    # Lemma N0 on the declared net, and the admission caps.
    N = last + 1
    tmax = last * D
    n0b = B * (1 + D)
    n0c = tmax * tmax + 2 * tmax - 1
    n0e = B * (1 + D / (1 - D * D / 4))
    rep["N_theta"] = N
    rep["t_max"] = frac_str(tmax)
    rep["N0b_B(1+D)"] = frac_str(n0b)
    rep["N0c_tmax^2+2tmax-1"] = frac_str(n0c)
    rep["N0e_B(1+D/(1-D^2/4))"] = frac_str(n0e)
    rep["N0b_margin_1-B(1+D)"] = frac_str(1 - n0b)
    checks["N0a"] = D > 0 and 2 <= N <= 2**16
    checks["N0b"] = n0b < 1
    checks["N0c"] = n0c > 0
    checks["N0d"] = tmax <= mpq(1, 2)
    checks["N0e"] = n0e < 1
    checks["B_in_(0,1)"] = 0 < B < 1
    checks["L^2>=2B^2"] = L * L >= 2 * B * B
    checks["caps_L<=1000_rows<=1e6"] = L <= 1000 and len(rows) <= 10**6
    # The endpoint bin: node `last` has bin [tmax - D/2, tmax + D/2]; tan(pi/8) = sqrt2 - 1
    # is the positive root of x^2 + 2x - 1, which is increasing for x > -1.
    lo_end = tmax - D / 2
    checks["tan(pi/8)_in_last_bin"] = (lo_end * lo_end + 2 * lo_end - 1 < 0) and n0c >= 0
    prev_hi = (last - 1) * D + D / 2
    checks["tan(pi/8)_beyond_bin_last-1"] = prev_hi * prev_hi + 2 * prev_hi - 1 < 0

    # D4 expansion and invariance.
    dens = expand(cert)
    rep["expanded_rectangles"] = len(dens)
    integral = sum((d * (k[2] - k[0]) * (k[3] - k[1]) for k, d in dens.items()), mpq(0))
    checks["expanded_integral_is_M"] = integral == M
    invariant = True
    for k, d in dens.items():
        for im in d4_images(L, k):
            if dens.get(im) != d:
                invariant = False
                break
        if not invariant:
            break
    checks["expanded_density_D4_invariant"] = invariant
    max_dens = max(dens.values())
    max_row_dens = max(w / ((x2 - x1) * (y2 - y1)) for w, (x1, y1, x2, y2) in rows)
    rep["max_expanded_density"] = float(max_dens)
    rep["max_row_density_w/|R|"] = float(max_row_dens)
    checks["eight_times_densest_row_density<=2^32"] = 8 * max_row_dens <= 2**32
    checks["expanded_density<=2^96"] = max_dens <= 2**96

    # Per-bin domains at every node.
    min_gap = None
    min_U = None
    max_U = None
    core_ok = True
    worst_core = None
    for r in range(N):
        dr = direction(cert, r)
        if min_U is None or dr.U < min_U:
            min_U = dr.U
        if max_U is None or dr.U > max_U:
            max_U = dr.U
        gap = dr.U - L / 2
        if min_gap is None or gap < min_gap:
            min_gap = gap
        core = B * rho_half_width(dr.t)  # B (c + s) / 2
        slack = dr.margin - core
        if slack <= 0:
            core_ok = False
        if worst_core is None or slack < worst_core[0]:
            worst_core = (slack, r)
    assert min_gap is not None and min_U is not None and max_U is not None
    assert worst_core is not None
    checks["U_r>L/2_all_r"] = min_gap > 0
    rep["U_r_range"] = [float(min_U), float(max_U)]
    rep["U_0"] = frac_str(direction(cert, 0).U)
    checks["core_half_extent_below_margin_all_r"] = core_ok
    rep["least_margin_minus_core_half_extent"] = {
        "value": float(worst_core[0]),
        "r": worst_core[1],
    }

    # The dilation against Hosono's candidate.
    hos = strict_json(read_bytes(hosono_path))
    rep["hosono_candidate_gz_sha256"] = sha256(hosono_path.read_bytes())
    rep["hosono_candidate_json_sha256"] = sha256(read_bytes(hosono_path))
    lam = mpq(4986, 4975)
    L0 = mpq(str(hos["L"]))
    B0 = mpq(str(hos["B"]))
    checks["L_is_lambda_L0"] = L == lam * L0
    checks["B_is_lambda_B0"] = B == lam * B0
    hrows = hos["rectangles"]
    assert isinstance(hrows, list)
    checks["same_row_count"] = len(hrows) == len(rows)
    rows_ok = True
    for (w, rect), hrow in zip(rows, hrows, strict=True):
        assert isinstance(hrow, dict)
        hw = mpq(str(hrow["mass"]))
        hr = hrow["rectangle"]
        assert isinstance(hr, list)
        hrect = [mpq(str(v)) for v in hr]
        if w != hw or any(a != lam * b for a, b in zip(rect, hrect, strict=True)):
            rows_ok = False
    checks["each_row_lambda_times_hosono_mass_equal"] = rows_ok
    checks["hosono_total_mass_equal"] = mpq(str(hos["total_mass"])) == M
    checks["hosono_scaling_factor_1"] = hos.get("scaling_factor") == "1"

    # Regeneration by this program's own rule.
    regen = {
        "B": frac_str(lam * B0),
        "L": frac_str(lam * L0),
        "derived_from": obj["derived_from"],
        "n": hos["n"],
        "points": [],
        "proof_net": {"last": last, "step": frac_str(D)},
        "rectangles": [
            {
                "mass": str(hrow["mass"]),  # type: ignore[index]
                "rectangle": [frac_str(lam * mpq(str(v))) for v in hrow["rectangle"]],  # type: ignore[index]
            }
            for hrow in hrows
        ],
        "total_mass": str(hos["total_mass"]),
    }
    regen_text = json.dumps(regen, sort_keys=True, separators=(",", ":")).encode()
    checks["regenerated_json_text_byte_identical"] = regen_text == text
    regen_gz = gzip.compress(regen_text, compresslevel=9, mtime=0)
    rep["regenerated_gz_os_byte"] = regen_gz[9]
    checks["regenerated_gzip_byte_identical"] = regen_gz == gz_raw

    # What the dilation does not carry.
    D0 = mpq(83, 40000)
    N0h = 201
    checks["hosono_net_with_dilated_core_fails_N0b"] = B * (1 + D0) >= 1
    rep["B(1+83/40000)"] = frac_str(B * (1 + D0))
    shared = []
    for j in range(N0h):
        t = j * D0
        r = t / D
        if r.denominator == 1 and int(r) <= last:
            m_old = rho_half_width(max(mpq(0), t - D0 / 2))
            m_new = rho_half_width(max(mpq(0), t - D / 2))
            shared.append(
                {"j": j, "r": int(r), "growth_hosono_coords": m_old - m_new / lam}
            )
    rep["shared_nodes"] = len(shared)
    rep["new_nodes"] = N - len(shared)
    rep["shared_node_r"] = [s["r"] for s in shared]
    growths = [s["growth_hosono_coords"] for s in shared]
    rep["growth_at_axis"] = frac_str(growths[0])  # type: ignore[arg-type]
    rep["growth_min_max"] = [float(min(growths)), float(max(growths))]  # type: ignore[type-var,arg-type]
    checks["growth_at_axis_is_11/9972"] = growths[0] == mpq(11, 9972)
    checks["growth_positive_at_all_shared"] = all(g > 0 for g in growths)  # type: ignore[operator]
    # Tokoharu's domain on Hosono's net, for comparison: margin B0 rho(t).
    tok = [B0 * rho_half_width(mpq(s["j"]) * D0) - rho_half_width(max(mpq(0), mpq(s["r"]) * D - D / 2)) / lam for s in shared]  # type: ignore[arg-type]
    rep["growth_vs_tokoharu_domain_min_max"] = [float(min(tok)), float(max(tok))]
    rep["route_ceiling_L0/B0"] = frac_str(L0 / B0)
    checks["L_below_ceiling"] = L < L0 / B0
    rep["ceiling_minus_L"] = float(L0 / B0 - L)

    # The mutant.
    mut_path = src / "controls" / "mass-99-100.json.gz"
    mut = strict_json(read_bytes(mut_path))
    rep["mutant_gz_sha256"] = sha256(mut_path.read_bytes())
    same = set(mut) == set(obj)
    for key in obj:
        if key in ("rectangles", "derived_from"):
            continue
        same = same and mut.get(key) == obj[key] if key != "total_mass" else same
    mrows = mut["rectangles"]
    assert isinstance(mrows, list)
    mrow_ok = len(mrows) == len(rows)
    for (w, rect), mrow in zip(rows, mrows, strict=True):
        assert isinstance(mrow, dict)
        mr = mrow["rectangle"]
        assert isinstance(mr, list)
        mrow_ok = mrow_ok and mpq(str(mrow["mass"])) == mpq(99, 100) * w
        mrow_ok = mrow_ok and [mpq(str(v)) for v in mr] == list(rect)
    checks["mutant_masses_99/100_rectangles_same"] = mrow_ok
    checks["mutant_other_fields_same"] = same and mpq(str(mut["total_mass"])) == mpq(99, 100) * M
    rep["mutant_derived_from"] = mut.get("derived_from")
    rep["mutant_differing_keys"] = sorted(
        k for k in set(mut) | set(obj) if k != "rectangles" and mut.get(k) != obj.get(k)
    )

    rep["checks"] = checks
    rep["all_checks_hold"] = all(checks.values())
    for k2, v in rep.items():
        if k2 != "checks":
            print(f"{k2}: {v}")
    for k2, v in checks.items():
        print(f"  [{'ok' if v else 'FAIL'}] {k2}")
    print("ALL_CHECKS_HOLD" if rep["all_checks_hold"] else "SOME_CHECK_FAILS")
    out_path.write_text(json.dumps(rep, indent=1, default=str) + "\n")
    return 0 if rep["all_checks_hold"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
