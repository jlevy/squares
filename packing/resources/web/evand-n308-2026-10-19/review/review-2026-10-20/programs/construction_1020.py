"""Hold each certificate to the construction the source describes, and decide the views.

Written for the stage 4 review of 20 October 2026. The source's ``search/exact/README.md``
(read as data) says a certificate is the exact KKT configuration scaled about the origin
corner by 1 + eps with eps = 10^-20, its centres rounded to 10^-35, its rotations as
rational t = tan(theta/2), and S' = S(1 + eps) rounded up. For each certificate this
program reads the retained ``NAME.exact.txt`` (``n S*`` then ``x y theta_deg`` per
square, 70 digits) and measures:

- whether S' equals ceil(S* (1 + eps) 10^30) / 10^30 exactly;
- for every centre, the difference between the certificate's and the KKT centre scaled
  by 1 + eps, which should be at most 5 * 10^-36 (rounding to the nearest 10^-35);
- for every rotation, |t - tan(theta/2)| with tan taken at 60 decimal digits, and how
  many are exactly 0 (an upright square);
- how many rows of the KKT file are printed short (at most 17 significant digits), the
  solver's free squares being moved in binary64.

It also decides the two same-side regularized views on this review's route (imported
from ``third_route_1020.py`` beside it), without controls, and holds their sides to the
certificates'. Nothing here is a decision about the certificate's validity, which the
route decides; it says how the certificate was made and that the view is what it says.

Usage, from ``packing/``::

    python -I construction_1020.py --json OUT.json
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import third_route_1020 as route  # noqa: E402

WEB = Path("resources/web")
EPS = Fraction(1, 10**20)
CERTS = {
    "#689 n308": (WEB / "evand-n308-2026-10-19/source/search/packer/candidates", "s308_d308"),
    "#694 n154": (WEB / "evand-n154-sweep-2026-10-20/source/search/packer/candidates", "s154_sw"),
}


def ceil_at(value: Fraction, places: int) -> Fraction:
    return Fraction(-((-value.numerator * 10**places) // value.denominator), 10**places)


def tan_half_degrees(theta: Decimal, digits: int) -> Fraction:
    """tan(theta/2) for theta in degrees, by a Decimal Taylor series at `digits` digits."""
    getcontext().prec = digits + 20
    # pi by Machin's formula.
    def arctan_inv(n: int) -> Decimal:
        x = Decimal(1) / n
        x2 = x * x
        term = x
        total = x
        k = 1
        while True:
            term *= x2
            k += 2
            delta = term / k
            if delta < Decimal(10) ** (-(digits + 15)):
                break
            total += delta if (k // 2) % 2 == 0 else -delta
        return total

    pi = 16 * arctan_inv(5) - 4 * arctan_inv(239)
    half = theta * pi / 360
    # sin and cos by series.
    x2 = half * half
    s = half
    term = half
    k = 1
    while True:
        term *= -x2 / ((k + 1) * (k + 2))
        k += 2
        if abs(term) < Decimal(10) ** (-(digits + 15)):
            break
        s += term
    c = Decimal(1)
    term = Decimal(1)
    k = 0
    while True:
        term *= -x2 / ((k + 1) * (k + 2))
        k += 2
        if abs(term) < Decimal(10) ** (-(digits + 15)):
            break
        c += term
    value = s / c
    return Fraction(value.quantize(Decimal(10) ** -digits))


def measure(label: str, folder: Path, stem: str) -> dict[str, object]:
    n, side, poses = route.read_certificate((folder / f"{stem}.cert").read_text("utf-8"))
    kkt_lines = [line for line in (folder / f"{stem}.exact.txt").read_text("utf-8").splitlines() if line.strip()]
    count, s_star = kkt_lines[0].split()
    assert int(count) == n and len(kkt_lines) == n + 1
    s_star_f = Fraction(Decimal(s_star))
    expected = ceil_at(s_star_f * (1 + EPS), 30)
    centre_err: list[Fraction] = []
    tangent_err: list[Fraction] = []
    short_rows = 0
    uprights = 0
    for (x, y, t), line in zip(poses, kkt_lines[1:], strict=True):
        xs, ys, ths = line.split()
        if all(len(v.lstrip("-").replace(".", "").lstrip("0")) <= 17 for v in (xs, ys)):
            short_rows += 1
        kx, ky = Fraction(Decimal(xs)) * (1 + EPS), Fraction(Decimal(ys)) * (1 + EPS)
        centre_err.append(max(abs(x - kx), abs(y - ky)))
        if t == 0:
            uprights += 1
        tangent_err.append(abs(t - tan_half_degrees(Decimal(ths), 60)))
    return {
        "n": n,
        "side": str(side),
        "kkt_side_70_digits": s_star,
        "side_is_kkt_times_1_plus_1e-20_rounded_up_at_30": side == expected,
        "side_rounded_up_by": str(side - s_star_f * (1 + EPS)),
        "largest_centre_difference_from_scaled_kkt": f"{float(max(centre_err)):.3e}",
        "centres_within_5e-36": sum(1 for e in centre_err if e <= Fraction(5, 10**36)),
        "largest_tangent_difference_from_tan_half_theta": f"{float(max(tangent_err)):.3e}",
        "tangents_within_1e-35": sum(1 for e in tangent_err if e <= Fraction(1, 10**35)),
        "upright_squares_t_zero": uprights,
        "kkt_rows_printed_short": short_rows,
    }


def view(folder: Path, stem: str, side: Fraction) -> dict[str, object]:
    started = time.time()
    n, vside, poses = route.read_certificate((folder / f"{stem}_regularized.cert").read_text("utf-8"))
    try:
        decided = route.decide(n, vside, poses)
    except route.Refused as error:
        return {"accepted": False, "reason": str(error)}
    groups = sorted({t for _x, _y, t in poses})
    return {
        "accepted": True,
        "same_side_as_certificate": vside == side,
        "wall_clearance": decided["wall_clearance"],
        "least_distance_float": decided["least_distance_float"],
        "closest_pair": decided["closest_pair"],
        "distinct_tangents": len(groups),
        "seconds": round(time.time() - started, 1),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)
    report: dict[str, object] = {}
    bad = 0
    for label, (folder, stem) in CERTS.items():
        row = measure(label, folder, stem)
        row["view"] = view(folder, stem, Fraction(str(row["side"])))
        report[label] = row
        if not row["side_is_kkt_times_1_plus_1e-20_rounded_up_at_30"] or not row["view"]["accepted"]:  # type: ignore[index]
            bad += 1
        print(json.dumps({label: row}, indent=1), flush=True)
    args.json.write_text(json.dumps(report, indent=1) + "\n", "utf-8")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
