#!/usr/bin/env python3
"""The issue 755 certificate against the float packing it states it was made from.

Written for the stage 4 review of T-238 (bead think-jdz0). Decides nothing: it measures
how the certificate's numbers stand to the input's, to check the issue's method statement
("the float64 packing's centres and box scaled by 1 + 10^-12, coordinates rounded to
rationals and each angle to a rational half-angle tangent"). It runs no program of the
source and reproduces no generator; it compares numbers.

For each of the certificate and the input it reads (the input as `n side` then
`x y angle_deg`, each value both as its exact decimal and as the binary64 it denotes):

- the side: the certificate's side against the input side times 1 + 1e-12;
- the centres: each certificate centre against the input centre times 1 + 1e-12, and
  against it times the ratio of the two sides;
- the tangents: each certificate tangent t against tan(theta/2) for the input angle,
  computed to 60 digits with mpmath, and against candidate float pipelines followed by
  `Fraction.limit_denominator(10**15)`; and the rotation 2 atan(t) against the input angle.

With `--reference CERT INPUT` it measures a second pair the same way (T-230's certificate
and input), for comparison.

Revised after the review's checker had decided, and after its author had read Evan
Daniel's `search/packer/dilate_cert.py` at 7982d7a (SHA-256 a07082b7...), to hold the
certificate to that program's formulas, written out here and not run: the factor
f = 1 + Fraction(1e-12) (the binary64 value of 1e-12), each centre round(x * f * 10^30)
/ 10^30 with x the input's decimal, the side ceil(S * f * 10^30) / 10^30, and each tangent
Fraction(tan(radians(deg % 90) / 2)).limit_denominator(10^15) in this platform's binary64
arithmetic. Where that tangent differs, it searches the floats within four ulps of this
platform's tan for one whose best approximation is the certificate's.

Usage:
  python3 -I method_t238.py CERT INPUT [--reference CERT2 INPUT2] --out OUT.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path

import mpmath as mp

mp.mp.dps = 60
DELTA = Q(1, 10**12)


def read_cert(path: str):
    lines = [ln for ln in Path(path).read_text().splitlines() if ln and not ln.startswith("#")]
    n, s = lines[0].split()
    rows = [tuple(Q(tok) for tok in ln.split()) for ln in lines[1:]]
    assert len(rows) == int(n)
    return int(n), Q(s), rows


def read_input(path: str):
    lines = [ln for ln in Path(path).read_text().splitlines() if ln.strip()]
    n, s = lines[0].split()
    rows = [ln.split() for ln in lines[1:]]
    assert len(rows) == int(n)
    return int(n), s, rows


def sci(x) -> str:
    x = Q(x)
    if x == 0:
        return "0"
    return mp.nstr(mp.mpf(x.numerator) / x.denominator, 7)


def pipelines(deg_text: str) -> dict[str, float]:
    a = float(deg_text)
    return {
        "tan(radians(a)/2)": math.tan(math.radians(a) / 2),
        "tan(radians(a/2))": math.tan(math.radians(a / 2)),
        "tan(a*pi/360)": math.tan(a * math.pi / 360),
    }


def measure(cert_path: str, input_path: str) -> dict:
    n, side, rows = read_cert(cert_path)
    n2, side_text, inp = read_input(input_path)
    assert n == n2
    side_dec = Q(side_text)
    side_bin = Q(float(side_text))
    out: dict = {
        "certificate_sha256": hashlib.sha256(Path(cert_path).read_bytes()).hexdigest(),
        "input_sha256": hashlib.sha256(Path(input_path).read_bytes()).hexdigest(),
        "n": n,
        "certificate_side": f"{side.numerator}/{side.denominator}",
        "input_side": side_text,
        "side_minus_input_decimal_times_dilation": sci(side - side_dec * (1 + DELTA)),
        "side_minus_input_binary64_times_dilation": sci(side - side_bin * (1 + DELTA)),
        "side_ratio_minus_one_minus_delta": sci(side / side_dec - 1 - DELTA),
    }
    ratio = side / side_dec
    res_dil = []
    res_ratio = []
    res_bin = []
    t_vs_exact = []
    rot_err = []
    pipe_match = {name: 0 for name in pipelines("0")}
    pipe_first_miss = {}
    tilted_beyond = {"1e-9 deg": 0, "1e-6 deg": 0, "1e-3 deg": 0, "0.1 deg": 0, "1 deg": 0}
    tilts = []
    for k, ((x, y, t), (xs, ys, ds)) in enumerate(zip(rows, inp)):
        xd, yd = Q(xs), Q(ys)
        res_dil.append(max(abs(x - xd * (1 + DELTA)), abs(y - yd * (1 + DELTA))))
        res_ratio.append(max(abs(x - xd * ratio), abs(y - yd * ratio)))
        res_bin.append(max(abs(x - Q(float(xs)) * (1 + DELTA)), abs(y - Q(float(ys)) * (1 + DELTA))))
        exact_half = mp.tan(mp.radians(mp.mpf(ds)) / 2)
        t_vs_exact.append(abs(mp.mpf(t.numerator) / t.denominator - exact_half))
        rot = 2 * mp.atan(mp.mpf(t.numerator) / t.denominator)
        rot_err.append(abs(mp.degrees(rot) - mp.mpf(ds)))
        for name, value in pipelines(ds).items():
            if Q(value).limit_denominator(10**15) == t:
                pipe_match[name] += 1
            elif name not in pipe_first_miss:
                pipe_first_miss[name] = k
        deg = float(mp.degrees(rot))
        tilt = ((deg + 45.0) % 90.0) - 45.0
        tilts.append(tilt)
        for label, thr in (("1e-9 deg", 1e-9), ("1e-6 deg", 1e-6), ("1e-3 deg", 1e-3), ("0.1 deg", 0.1), ("1 deg", 1.0)):
            if abs(tilt) > thr:
                tilted_beyond[label] += 1
    out["centres_minus_input_decimal_times_dilation"] = {"max": sci(max(res_dil)), "min": sci(min(res_dil))}
    out["centres_minus_input_decimal_times_side_ratio"] = {"max": sci(max(res_ratio)), "min": sci(min(res_ratio))}
    out["centres_minus_input_binary64_times_dilation"] = {"max": sci(max(res_bin)), "min": sci(min(res_bin))}
    out["tangent_minus_exact_half_angle_tangent"] = {"max": mp.nstr(max(t_vs_exact), 7)}
    out["rotation_minus_input_angle_deg"] = {"max": mp.nstr(max(rot_err), 7)}
    out["float_pipelines_then_limit_denominator_1e15"] = {
        name: {"rows_reproduced": pipe_match[name], "of": n, "first_row_not": pipe_first_miss.get(name)}
        for name in pipe_match
    }
    out["tilt_counts_mod_90"] = tilted_beyond
    big = sorted(abs(t) for t in tilts if abs(t) > 0.1)
    out["tilt_range_beyond_0p1_deg"] = [round(big[0], 4), round(big[-1], 4)] if big else None
    out["tilt_signs_beyond_0p1_deg"] = {
        "positive": sum(1 for t in tilts if t > 0.1),
        "negative": sum(1 for t in tilts if t < -0.1),
    }
    out["rows_with_t_in_0_or_pm1"] = sum(1 for _, _, t in rows if t in (0, 1, -1))
    # dilate_cert.py's formulas, written out (not run)
    f = 1 + Q(1e-12)
    big = 10**30
    side_formula = Q(-((-(side_dec * f * big).numerator) // (side_dec * f * big).denominator), big)
    centre_hits = sum(
        1
        for (x, y, _t), (xs, ys, _ds) in zip(rows, inp)
        if x == Q(round(Q(xs) * f * big), big) and y == Q(round(Q(ys) * f * big), big)
    )
    tangent_hits = 0
    ulp_offsets: dict[str, int] = {}
    misses = []
    for k, ((_x, _y, t), (_xs, _ys, ds)) in enumerate(zip(rows, inp)):
        th = math.radians(float(ds) % 90.0)
        value = math.tan(th / 2)
        if Q(value).limit_denominator(10**15) == t:
            tangent_hits += 1
            continue
        found = None
        for step in (1, -1, 2, -2, 3, -3, 4, -4):
            v = value
            for _ in range(abs(step)):
                v = math.nextafter(v, math.inf if step > 0 else -math.inf)
            if Q(v).limit_denominator(10**15) == t:
                found = step
                break
        ulp_offsets[str(found)] = ulp_offsets.get(str(found), 0) + 1
        misses.append({"row": k, "degrees": ds, "certificate_t": f"{t.numerator}/{t.denominator}", "ulps_from_this_tan": found})
    out["dilate_cert_formulas"] = {
        "factor_minus_one_minus_1e-12": sci(f - 1 - DELTA),
        "side_reproduced": side_formula == side,
        "centres_reproduced": centre_hits,
        "tangents_reproduced_on_this_platform": tangent_hits,
        "of": n,
        "other_tangents_by_ulp_offset": ulp_offsets,
        "other_tangents": misses[:60],
    }
    out["rows_with_input_angle_text_0"] = sum(1 for _, _, d in inp if float(d) == 0.0)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("input")
    ap.add_argument("--reference", nargs=2)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = {
        "program": "method_t238.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "certificate": measure(args.cert, args.input),
    }
    if args.reference:
        out["reference"] = measure(*args.reference)
    Path(args.out).write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
