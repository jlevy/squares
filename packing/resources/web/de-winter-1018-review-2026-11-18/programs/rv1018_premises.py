"""Exact premises of #1018's measure and of its enlargement argument.

Lane r108-1118, blind review of jlevy/squares#1018. Recomputes in exact rationals:

1. the measure: rows inside K = [0, L]^2 with positive extents and masses, the listed
   total, the merged D4 expansion, its total and its invariance under all eight symmetries;
2. the declared net's premises (a) to (e) as the issue's verifier states them, the sharp
   extent of a core, which tangents the net covers, and every per-bin quadrant;
3. the argument of `proof_n108.pdf`: u = 2 B w(D/2), h > 1/sqrt 2, the side
   S = 2h + (L - 2h)/u, that S is the claimed fraction, that it prints as claimed, the
   scaled packing's margins, and the inequality chain the proof uses;
4. informational values that decide nothing: the same enlargement at T-216's premises, and
   what T-216's own certificate would give after the rescaling.

Imports nothing from jlevy/squares or the source.

Usage: python -I rv1018_premises.py --measure M.json.gz [--base T216.json.gz] --out OUT.json
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1018_common as cm  # noqa: E402

# What proof_n108.pdf and issue #1018 state, transcribed by hand from the PDF and the issue.
STATED = {
    "L": Fraction(1063, 100),
    "B": Fraction("0.99896"),
    "D": Fraction(83, 80000),
    "last": 400,
    "u": Fraction(319998768697057, 320000086112500),
    "h": Fraction(707107, 10**6),
    "S": Fraction(1700799526134255846599, 159999384348528500000),
    "S_12_places": "10.630037940829",
    "orbits": 823,
    "total_mass": Fraction("107.99999"),
    "n": 108,
    "rescale": Fraction(1063, 1062),
}


def decimal(q: Fraction, places: int) -> str:
    """q rounded toward zero at the given number of places (q > 0)."""
    scaled = q.numerator * 10**places // q.denominator
    s = str(scaled).rjust(places + 1, "0")
    return s[:-places] + "." + s[-places:]


def check_measure(meas: dict) -> tuple[dict, list[str]]:
    fails: list[str] = []
    side, rows = meas["L"], meas["rows"]
    for i, (x0, y0, x1, y1, m) in enumerate(rows):
        if not (0 <= x0 < x1 <= side and 0 <= y0 < y1 <= side):
            fails.append(f"row {i} not a rectangle of positive area inside K")
        if not m > 0:
            fails.append(f"row {i} mass not positive")
    listed = sum((r[4] for r in rows), Fraction(0))
    if listed != meas["total_mass"]:
        fails.append("rows do not sum to total_mass")
    if not meas["total_mass"] < meas["n"]:
        fails.append("total mass not below n")
    rects = cm.expand(rows, side)
    expanded = sum((r[4] for r in rects), Fraction(0))
    if expanded != meas["total_mass"]:
        fails.append("expansion does not integrate to total_mass")
    keyed = {(a, b, c, d): g for (a, b, c, d, _m, g) in rects}
    for a, b, c, d, _m, g in rects:
        for img in cm.d4_images(a, b, c, d, side):
            if keyed.get(img) != g:
                fails.append("expansion not D4 invariant")
                break
    dens = max(r[5] for r in rects)
    thin = sum(1 for r in rows if min(r[2] - r[0], r[3] - r[1]) < Fraction(1, 500))
    out = {
        "n": meas["n"],
        "L": str(side),
        "B": str(meas["B"]),
        "proof_net": {"step": str(meas["step"]), "last": meas["last"]},
        "rows": len(rows),
        "total_mass": str(meas["total_mass"]),
        "n_minus_mass": str(meas["n"] - meas["total_mass"]),
        "expanded_images": 8 * len(rows),
        "expanded_distinct": len(rects),
        "max_density": float(dens),
        "eight_times_max_density": float(8 * dens),
        "rows_thinner_than_1_500": thin,
        "json_sha256": meas["json_sha256"],
        "stored_sha256": meas["stored_sha256"],
        "canonical_sha256": meas["canonical_sha256"],
    }
    return out, fails


def check_net(side_b: Fraction, step: Fraction, last: int, side: Fraction) -> tuple[dict, list[str]]:
    fails: list[str] = []
    tmax = last * step
    cond = {
        "a_step_positive_and_count": step > 0 and 2 <= last + 1 <= 2**16,
        "b_B_times_1_plus_D": side_b * (1 + step) < 1,
        "c_endpoint": tmax * tmax + 2 * tmax - 1 > 0,
        "d_tmax_at_most_half": tmax <= Fraction(1, 2),
        "e_tangent_form": side_b * (1 + step / (1 - step * step / 4)) < 1,
    }
    for k, ok in cond.items():
        if not ok:
            fails.append(f"net premise {k} fails")
    z0 = step / 2
    sharp = side_b * (1 + 2 * z0 - z0 * z0) / (1 + z0 * z0)
    last_low = last * step - step / 2
    second_last_high = (last - 1) * step + step / 2
    # every folded tangent t in [0, tan(pi/8)] has a node within D/2 among 0..last
    covers = (tmax + step / 2) ** 2 + 2 * (tmax + step / 2) - 1 > 0
    widths = []
    for r in range(last + 1):
        upper = cm.domain_upper(r, step, side)
        widths.append(upper - side / 2)
    if min(widths) <= 0:
        fails.append("an empty quadrant")
    # monotonicity of w on [0, tan(pi/8)]: w'(t) = (1 - 2t - t^2)/(1 + t^2)^2, positive below
    # sqrt 2 - 1; every a_r used by a folded square is below tan(pi/8)
    used = [r for r in range(last + 1) if (lambda a: a * a + 2 * a - 1 < 0)(cm.bin_low(r, step))]
    out = {
        "conditions": {k: bool(v) for k, v in cond.items()},
        "B_times_1_plus_D": str(side_b * (1 + step)),
        "tangent_form": str(side_b * (1 + step / (1 - step * step / 4))),
        "sharp_extent_2Bw(D/2)": str(sharp),
        "t_max": str(tmax),
        "t_max_poly": str(tmax * tmax + 2 * tmax - 1),
        "net_covers_tan_pi_8": bool(covers),
        "last_bin_low_end": str(last_low),
        "last_bin_low_poly": str(last_low * last_low + 2 * last_low - 1),
        "last_bin_needed": bool(last_low * last_low + 2 * last_low - 1 < 0),
        "second_last_bin_high_poly": str(
            second_last_high * second_last_high + 2 * second_last_high - 1
        ),
        "nodes_whose_bin_holds_a_folded_angle": [used[0], used[-1]] if used else None,
        "count_nodes_used": len(used),
        "least_quadrant_width": float(min(widths)),
        "least_quadrant_width_at": widths.index(min(widths)),
    }
    return out, fails


def check_enlargement(
    side: Fraction, side_b: Fraction, step: Fraction, h: Fraction, claimed: Fraction
) -> tuple[dict, list[str]]:
    fails: list[str] = []
    z0 = step / 2
    u = 2 * side_b * cm.w_half_width(z0)
    S = 2 * h + (side - 2 * h) / u
    if not 0 < u < 1:
        fails.append("u not in (0, 1)")
    if not 2 * h * h > 1:
        fails.append("h is not above 1/sqrt 2")
    if not 2 * h < side:
        fails.append("2h not below L")
    if S != claimed:
        fails.append("S differs from the claimed value")
    # the scaled packing x -> u x + h(1 - u) maps [0, S] onto [h(1-u), L - h(1-u)]
    if u * S + h * (1 - u) != side - h * (1 - u):
        fails.append("the scaled packing is not centred with equal margins")
    if not h * (1 - u) > 0:
        fails.append("no margin")
    # a centre at distance v from the walls of [0, S] lands at distance u v + h(1 - u);
    # with v <= sqrt(1/2) < h and u < 1 that is at least v: (1 - u)(h - v) >= 0.
    worst_v = Fraction(707106781186548, 10**15)  # above sqrt(1/2)? checked below
    chain_ok = (1 - u) * (h - worst_v) >= 0 and worst_v * worst_v > Fraction(1, 2)
    if not chain_ok:
        fails.append("inequality chain at v = sqrt(1/2) fails")
    # the core inside a scaled square: 2 B w(z) <= u for 0 <= z <= z0, w increasing there
    if not z0 * z0 + 2 * z0 - 1 < 0:
        fails.append("z0 not below tan(pi/8)")
    out = {
        "z0": str(z0),
        "u": str(u),
        "u_equals_stated": u == STATED["u"],
        "one_minus_u": str(1 - u),
        "h": str(h),
        "two_h_squared_minus_1": str(2 * h * h - 1),
        "S": str(S),
        "S_decimal_40": decimal(S, 40),
        "S_12_places_rounded_down": decimal(S, 12),
        "claimed": str(claimed),
        "S_equals_claimed": S == claimed,
        "S_minus_L": float(S - side),
        "margin_h_1_minus_u": float(h * (1 - u)),
        "gain_factor_1_over_u_minus_1": float(1 / u - 1),
    }
    if decimal(S, 12) != STATED["S_12_places"] and claimed == STATED["S"]:
        fails.append("S does not print as the issue's 12 places")
    return out, fails


def informational(base: dict | None, meas: dict) -> dict:
    """Decides nothing: the same enlargement at T-216's own premises, and whether T-216's
    certificate itself could carry the rescaled measure."""
    if base is None:
        return {}
    h = STATED["h"]
    zb = base["step"] / 2
    ub = 2 * base["B"] * cm.w_half_width(zb)
    sb = 2 * h + (base["L"] - 2 * h) / ub
    lam = meas["L"] / base["L"]
    scaled_core = base["B"] * lam
    return {
        "T216_L_B_D_last": [str(base["L"]), str(base["B"]), str(base["step"]), base["last"]],
        "enlargement_at_T216_premises": decimal(sb, 15),
        "rescale_factor": str(lam),
        "T216_core_scaled": str(scaled_core),
        "T216_core_scaled_times_1_plus_T216_D": str(scaled_core * (1 + base["step"])),
        "T216_certificate_transfers_to_rescaled_measure": bool(
            scaled_core * (1 + base["step"]) < 1
        ),
        "new_core_at_old_scale": str(meas["B"] / lam),
        "new_core_at_old_scale_minus_T216_B": float(meas["B"] / lam - base["B"]),
    }


def premises(meas: dict, h: Fraction, claimed: Fraction, base: dict | None) -> dict:
    m_out, m_fail = check_measure(meas)
    n_out, n_fail = check_net(meas["B"], meas["step"], meas["last"], meas["L"])
    e_out, e_fail = check_enlargement(meas["L"], meas["B"], meas["step"], h, claimed)
    stated_ok = {
        "L": meas["L"] == STATED["L"],
        "B": meas["B"] == STATED["B"],
        "D": meas["step"] == STATED["D"],
        "last": meas["last"] == STATED["last"],
        "orbits": len(meas["rows"]) == STATED["orbits"],
        "total_mass": meas["total_mass"] == STATED["total_mass"],
        "n": meas["n"] == STATED["n"],
    }
    s_fail = [f"file differs from the stated {k}" for k, ok in stated_ok.items() if not ok]
    fails = m_fail + n_fail + e_fail + s_fail
    return {
        "program": "rv1018_premises.py",
        "verdict": "PREMISES_HOLD" if not fails else "PREMISES_FAIL",
        "failures": fails,
        "measure": m_out,
        "net": n_out,
        "enlargement": e_out,
        "file_matches_statements": stated_ok,
        "informational": informational(base, meas),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", required=True)
    ap.add_argument("--base")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    meas = cm.read_measure(args.measure)
    base = cm.read_measure(args.base) if args.base else None
    res = premises(meas, STATED["h"], STATED["S"], base)
    Path(args.out).write_text(json.dumps(res, indent=1) + "\n")
    print(res["verdict"], res["failures"])
    print("S =", res["enlargement"]["S_decimal_40"])
    return 0 if res["verdict"] == "PREMISES_HOLD" else 1


if __name__ == "__main__":
    raise SystemExit(main())
