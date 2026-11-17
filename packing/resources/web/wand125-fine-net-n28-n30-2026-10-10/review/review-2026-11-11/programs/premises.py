"""Every exact premise of the two candidates, recomputed apart from the crate and tools.

Usage: python -I premises.py --release DIR --out FILE

DIR is the packet's release/certificates/ directory. For each certificate this checks,
in fractions: its identity (stored and decompressed SHA-256, and the source's
candidate_digest recomputed); the claim (n, L, B, the declared net, the total mass
n - 1/100000 < n); every row inside [0, L]^2 with positive extents and positive mass,
every coordinate a multiple of 1e-17; the merged D4 expansion's size, integral and
invariance under all eight symmetries; the densest row against 2^32; lemma N0's (a) to
(e), the sharp extent, the last bin; and, by direct geometry at both ends of all 2,073
bins, the containment of the core and the per-bin centre domain. It prints
PREMISES_HOLD when everything holds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fnlib as F  # noqa: E402

CLAIMS = {
    "mixed_n28_L57425": {
        "n": 28,
        "L": Fraction(2297, 400),
        "rows": 631,
        "expanded": 5036,
        "sha256": "5ef20511e18a9997dfcc4cef773b65eac83dfe59e6a56fa810f3c789076c0107",
        "candidate_digest": "a1ea15ca8c4c9751029ea5d3bf98ad23f57a69a31accf04723587717888f6dd4",
    },
    "mixed_n30_L58925": {
        "n": 30,
        "L": Fraction(2357, 400),
        "rows": 463,
        "expanded": 3672,
        "sha256": "981a17db67b24f99d64e176c892655c27fde67f8e99f2875a8f1d55ff3d0677e",
        "candidate_digest": "716bcb62b5d6ce733968985f9efd0a5456915c135cd72feca4bb4983cb11380a",
    },
}

Q = 10**17


def check(cond: bool, label: str, failures: list[str]) -> bool:
    if not cond:
        failures.append(label)
    return cond


def net_premises(B: Fraction, step: Fraction, last: int) -> dict:
    D, N = step, last + 1
    tmax = last * D
    out = {
        "a_D_positive_and_count": D > 0 and 2 <= N <= 2**16,
        "b_B_1_plus_D": F.fstr(B * (1 + D)),
        "b_holds": B * (1 + D) < 1,
        "c_reach": F.fstr(tmax * tmax + 2 * tmax - 1),
        "c_holds": tmax * tmax + 2 * tmax - 1 > 0,
        "d_tmax": F.fstr(tmax),
        "d_holds": tmax <= Fraction(1, 2),
        "e_tangent_form": F.fstr(B * (1 + D / (1 - D * D / 4))),
        "e_holds": B * (1 + D / (1 - D * D / 4)) < 1,
        "sharp_extent": F.fstr(B * (1 + D - D * D / 4) / (1 + D * D / 4)),
        "sharp_holds": B * (1 + D - D * D / 4) / (1 + D * D / 4) < 1,
    }
    lo = (last - Fraction(1, 2)) * D
    out["last_bin_lower_end"] = F.fstr(lo)
    out["last_bin_lower_end_reach"] = F.fstr(lo * lo + 2 * lo - 1)
    out["last_bin_needed"] = lo * lo + 2 * lo - 1 < 0
    return out


def net_geometry(B: Fraction, L: Fraction, step: Fraction, last: int) -> dict:
    """Containment and the centre domain at both ends of every bin, in fractions."""
    D = step
    worst_extent = Fraction(0)
    worst_at = None
    min_width = None
    min_far = None
    min_far_at = None
    fails = []
    for j in range(last + 1):
        t = j * D
        ends = [max(Fraction(0), t - D / 2), t + D / 2]
        for u in ends:
            # The relative turn of an orientation u in bin j against the node's angle.
            z = abs(u - t) / (1 + u * t)
            if z > D / 2:
                fails.append(f"z beyond D/2 at bin {j}")
            # The concentric core of side B turned by delta = 2 atan z lies in the open
            # unit square iff B (cos delta + sin delta) < 1.
            ext = B * (1 - z * z + 2 * z) / (1 + z * z)
            if ext >= 1:
                fails.append(f"core not inside at bin {j}")
            if ext > worst_extent:
                worst_extent, worst_at = ext, (j, "lower" if u == ends[0] else "upper")
        a = F.a_of(j, D)
        # r increases on [0, sqrt 2 - 1]; a_j must lie there for r(a_j) to be the least.
        if not a * a + 2 * a - 1 < 0:
            fails.append(f"a_j past tan(pi/8) at bin {j}")
        width = L - 2 * F.r_of(a)
        if min_width is None or width < min_width:
            min_width = width
        if F.upper_end(j, L, D) < L / 2:
            fails.append(f"empty quadrant at bin {j}")
        # Informational: the core at the domain's far corner still lies in [0, L]^2 when
        # B r(t_j) <= r(a_j).
        far = F.r_of(a) - B * F.r_of(t)
        if min_far is None or far < min_far:
            min_far, min_far_at = far, j
    # Bins abut: t_j + D/2 = t_{j+1} - D/2 by construction; bin 0 starts at -D/2 < 0.
    upper = (last + Fraction(1, 2)) * D
    return {
        "bins": last + 1,
        "ends_checked": 2 * (last + 1),
        "failures": fails,
        "largest_extent": F.fstr(worst_extent),
        "largest_extent_float": float(worst_extent),
        "largest_extent_at": worst_at,
        "clearance": float(1 - worst_extent),
        "last_bin_upper_end_past_tan_pi_8": upper * upper + 2 * upper - 1 > 0,
        "narrowest_domain_width": F.fstr(min_width),
        "narrowest_domain_width_float": float(min_width),
        "least_far_corner_clearance": float(min_far),
        "least_far_corner_clearance_at": min_far_at,
    }


def one(name: str, path: Path) -> dict:
    claim = CLAIMS[name]
    failures: list[str] = []
    cert = F.read_candidate(path)
    out: dict = {"certificate": name, "file": str(path.name)}
    out["stored_sha256"] = cert.stored_sha256
    out["sha256"] = cert.sha256
    check(cert.sha256 == claim["sha256"], "decompressed SHA-256 is not the pin", failures)
    # The source's candidate_digest: SHA-256 of the JSON with sorted keys, compact.
    canon = json.dumps(cert.obj, sort_keys=True, separators=(",", ":")).encode()
    out["candidate_digest"] = hashlib.sha256(canon).hexdigest()
    check(out["candidate_digest"] == claim["candidate_digest"], "candidate_digest differs", failures)
    check(cert.n == claim["n"], "n", failures)
    check(cert.L == claim["L"], "L", failures)
    check(cert.B == F.CORE, "B", failures)
    check(cert.step == F.STEP and cert.last == F.LAST, "net", failures)
    check(set(cert.obj["proof_net"]) == {"step", "last"}, "proof_net keys", failures)
    out["claim"] = {
        "n": cert.n,
        "L": F.fstr(cert.L),
        "B": F.fstr(cert.B),
        "step": F.fstr(cert.step),
        "last": cert.last,
        "total_mass": F.fstr(cert.total_mass),
    }
    check(cert.total_mass == cert.n - Fraction(1, 100000), "total_mass is not n - 1e-5", failures)
    check(cert.total_mass < cert.n, "total mass not below n", failures)
    rows = cert.rows
    check(len(rows) == claim["rows"], "row count", failures)
    L = cert.L
    bad_geom = [
        i for i, (x0, y0, x1, y1, m) in enumerate(rows) if not (0 <= x0 < x1 <= L and 0 <= y0 < y1 <= L)
    ]
    bad_mass = [i for i, r in enumerate(rows) if not r[4] > 0]
    bad_grid = [i for i, r in enumerate(rows) if any(Q % v.denominator for v in r[:4])]
    check(not bad_geom, "row outside [0, L]^2 or empty", failures)
    check(not bad_mass, "nonpositive mass", failures)
    check(not bad_grid, "coordinate off the 1e-17 grid", failures)
    msum = sum((r[4] for r in rows), Fraction(0))
    check(msum == cert.total_mass, "masses do not sum to total_mass", failures)
    dens_row = [r[4] / ((r[2] - r[0]) * (r[3] - r[1])) for r in rows]
    dmax = max(dens_row)
    imax = dens_row.index(dmax)
    check(dmax <= 2**32, "densest row above 2^32", failures)
    images = F.expand(rows, L)
    check(len(images) == claim["expanded"], "expanded count differs from the source's", failures)
    integral = sum((d * (k[2] - k[0]) * (k[3] - k[1]) for k, d in images.items()), Fraction(0))
    check(integral == cert.total_mass, "expansion does not integrate to the mass", failures)
    inv = True
    for g in F.symmetries(L):
        for k, d in images.items():
            if images.get(g(k)) != d:
                inv = False
                break
    check(inv, "expansion not D4-invariant", failures)
    heaviest = max(range(len(rows)), key=lambda i: rows[i][4])
    out["rows"] = {
        "count": len(rows),
        "all_inside_with_positive_extent": not bad_geom,
        "all_masses_positive": not bad_mass,
        "all_coordinates_multiples_of_1e-17": not bad_grid,
        "mass_sum": F.fstr(msum),
        "mass_gap_below_n": F.fstr(cert.n - msum),
        "densest_row": {"index": imax, "mass_over_area": float(dmax), "image_density": float(dmax / 8)},
        "heaviest_row": {"index": heaviest, "mass": float(rows[heaviest][4]),
                         "rectangle": [float(v) for v in rows[heaviest][:4]]},
        "least_row_mass": float(min(r[4] for r in rows)),
        # Descriptive: rows whose shorter side is below 1/500, and the mass they carry.
        "thin_strips": {
            "count": sum(1 for r in rows if min(r[2] - r[0], r[3] - r[1]) < Fraction(1, 500)),
            "mass": float(sum((r[4] for r in rows if min(r[2] - r[0], r[3] - r[1]) < Fraction(1, 500)), Fraction(0))),
        },
    }
    out["expansion"] = {
        "images": 8 * len(rows),
        "distinct_after_merge": len(images),
        "integral": F.fstr(integral),
        "d4_invariant": inv,
    }
    out["lemma_N0"] = net_premises(cert.B, cert.step, cert.last)
    for key in ("a_D_positive_and_count", "b_holds", "c_holds", "d_holds", "e_holds", "sharp_holds",
                "last_bin_needed"):
        check(out["lemma_N0"][key], f"lemma N0 {key}", failures)
    out["net_geometry"] = net_geometry(cert.B, L, cert.step, cert.last)
    check(not out["net_geometry"]["failures"], "net geometry", failures)
    check(out["net_geometry"]["last_bin_upper_end_past_tan_pi_8"], "net stops short", failures)
    out["failures"] = failures
    out["status"] = "PREMISES_HOLD" if not failures else "PREMISES_FAIL"
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    t0 = time.process_time()
    res = {}
    for name in CLAIMS:
        res[name] = one(name, Path(args.release) / name / "candidate.json.gz")
        print(name, res[name]["status"], res[name]["failures"])
    status = "PREMISES_HOLD" if all(r["status"] == "PREMISES_HOLD" for r in res.values()) else "PREMISES_FAIL"
    F.write_json(args.out, {"program": "premises.py", "status": status, "cpu_seconds": round(time.process_time() - t0, 2),
                            "certificates": res})
    print(status)
    return 0 if status == "PREMISES_HOLD" else 1


if __name__ == "__main__":
    raise SystemExit(main())
