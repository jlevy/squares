"""A certificate's padding against the house it is measured on. Decides nothing.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Written after the checker
and the controls plan were frozen, tried on a count outside the review, and run on the
review's counts only after the findings were frozen.

    python -I -B rv1009_padding.py HOUSE.yaml CERT YAML N OUT.json

A packing whose centres are all multiplied by a factor g, the squares kept unit, stays a
packing of unit squares with disjoint interiors until two of them first touch. A pair's
margin at g is ``g*max|d.w| - H`` (method A's terms), zero at ``g = H/max|d.w|``; the
greatest of these factors over all pairs, g*, is the first contact. The contracted
squares fit the box of their own extent, the larger of their width and height, so the
side the certificate gives away, its contraction margin or padding, is its side less
that extent. It counts both the slack between the squares and any slack at the walls. A
later certificate whose gain on the house is within the house's padding states no
smaller packing than the house contracted would; one whose gain is beyond it does.

Control K1 of the frozen plan contracts differently, the side with the centres and the
walls held as constraints, which is a sharp control of the checker and not this measure:
there a square near the left or bottom wall binds first.

HOUSE.yaml is a Witness/v2 file with rational scalars in the ``center-basis`` or the
``corners`` representation, read here with ``yaml.safe_load`` and checked by method A
(every square a unit pose, every clearance and every margin non-negative) before
anything is measured. CERT and YAML are the two files of the new certificate, read by
the frozen readers.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1009_axes as axes  # noqa: E402
import rv1009_forms as forms  # noqa: E402
import rv1009_reader as reader  # noqa: E402

F = Fraction
WALLS = ("left", "bottom", "right", "top")


def exact(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def sci(value: Fraction, digits: int = 12) -> str:
    return f"{float(value):.{digits - 1}e}"


def ceiling_12(value: Fraction) -> str:
    k = -((-value.numerator * 10**12) // value.denominator)
    return f"{k // 10**12}.{k % 10**12:012d}"


def scalar(text: object) -> tuple[int, int]:
    num, den, _canonical = reader.parse_scalar(text, "house scalar")
    return num, den


def lcm(a: int, b: int) -> int:
    import math

    return a * b // math.gcd(a, b)


def read_house(data: bytes) -> dict:
    """Poses and side of a rational Witness/v2 file in center-basis or corners form."""
    doc = yaml.safe_load(data.decode("ascii"))
    wit = doc["witness"]
    if wit["scalar"]["kind"] != "rational":
        msg = f"house scalars are {wit['scalar']['kind']}, not rational"
        raise ValueError(msg)
    if wit["coordinates"]["origin"] != "lower-left":
        msg = "house origin is not lower-left"
        raise ValueError(msg)
    side = scalar(str(wit["side"]))
    poses = []
    rep = wit["representation"]
    for item in wit["squares"]:
        if rep == "center-basis":
            (xn, xd), (yn, yd) = (scalar(str(v)) for v in item["center"])
            (cn, cd), (sn, sd) = (scalar(str(v)) for v in item["basis"])
            e = lcm(xd, yd)
            r = lcm(cd, sd)
            poses.append((xn * (e // xd), yn * (e // yd), e, cn * (r // cd), sn * (r // sd), r))
        elif rep == "corners":
            quad = [tuple(scalar(str(v)) for v in corner) for corner in item["corners"]]
            pose, _sense = forms.pose_from_corners(quad)
            poses.append(pose)
        else:
            msg = f"house representation {rep} is not read here"
            raise ValueError(msg)
    if len(poses) != wit["n"]:
        msg = "house count differs from its squares"
        raise ValueError(msg)
    return {
        "id": wit["id"],
        "n": wit["n"],
        "side": side,
        "representation": rep,
        "poses": poses,
        "source": wit.get("source", {}),
    }


def measure(poses: list, side: tuple[int, int]) -> dict:
    """Method A on the packing as given, and its first contact under contraction."""
    n = len(poses)
    unit = all(axes.is_unit_pose(p) for p in poses)
    sn, sd = side
    s = F(sn, sd)
    least_clear = min(min(axes.wall_clearances(p, side)) for p in poses)
    least_margin = None
    least_pair = None
    touching = 0
    overlapping = 0
    star = F(0)
    at: list = []
    for i in range(n):
        for j in range(i + 1, n):
            proj, k, den = axes.pair_numbers(poses[i], poses[j])
            top = max(proj)
            m = F(top - k, den)
            if least_margin is None or m < least_margin:
                least_margin, least_pair = m, (i + 1, j + 1)
            if m == 0:
                touching += 1
            elif m < 0:
                overlapping += 1
            g = F(k, top)
            if g > star:
                star, at = g, [(i + 1, j + 1)]
            elif g == star:
                at.append((i + 1, j + 1))
    # the extent of the contracted squares: centres times g*, half-extents unchanged
    lows_x, highs_x, lows_y, highs_y = [], [], [], []
    for x, y, e, a, b, r in poses:
        h = F(abs(a) + abs(b), 2 * r)
        cx, cy = star * F(x, e), star * F(y, e)
        lows_x.append(cx - h)
        highs_x.append(cx + h)
        lows_y.append(cy - h)
        highs_y.append(cy + h)
    width = max(highs_x) - min(lows_x)
    height = max(highs_y) - min(lows_y)
    contracted = max(width, height)
    # the extent of the squares as given
    given_w = max(F(x, e) + F(abs(a) + abs(b), 2 * r) for x, y, e, a, b, r in poses) - min(
        F(x, e) - F(abs(a) + abs(b), 2 * r) for x, y, e, a, b, r in poses
    )
    given_h = max(F(y, e) + F(abs(a) + abs(b), 2 * r) for x, y, e, a, b, r in poses) - min(
        F(y, e) - F(abs(a) + abs(b), 2 * r) for x, y, e, a, b, r in poses
    )
    assert least_margin is not None
    return {
        "squares": n,
        "all_unit_poses": unit,
        "least_clearance": least_clear,
        "least_margin": least_margin,
        "least_margin_pair": least_pair,
        "touching_pairs": touching,
        "overlapping_pairs": overlapping,
        "accepted_by_method_a": unit and least_clear >= 0 and overlapping == 0,
        "first_contact_factor": star,
        "first_contact_at": at,
        "side": s,
        "extent": max(given_w, given_h),
        "wall_slack": s - max(given_w, given_h),
        "side_margin": s - contracted,
        "contracted_side": contracted,
        "contracted_width_less_height": width - height,
    }


def as_json(facts: dict) -> dict:
    return {
        "squares": facts["squares"],
        "accepted_by_method_a": facts["accepted_by_method_a"],
        "side": exact(facts["side"]),
        "side_sci": f"{float(facts['side']):.17g}",
        "side_ceiling_12": ceiling_12(facts["side"]),
        "least_clearance": sci(facts["least_clearance"]),
        "least_margin": sci(facts["least_margin"]),
        "least_margin_pair": facts["least_margin_pair"],
        "touching_pairs": facts["touching_pairs"],
        "overlapping_pairs": facts["overlapping_pairs"],
        "one_less_first_contact_factor": exact(1 - facts["first_contact_factor"]),
        "one_less_first_contact_factor_sci": sci(1 - facts["first_contact_factor"]),
        "first_contact_at": facts["first_contact_at"][:12],
        "first_contact_count": len(facts["first_contact_at"]),
        "wall_slack": exact(facts["wall_slack"]),
        "wall_slack_sci": sci(facts["wall_slack"]),
        "side_margin": exact(facts["side_margin"]),
        "side_margin_sci": sci(facts["side_margin"]),
        "contracted_width_less_height_sci": sci(facts["contracted_width_less_height"]),
        "contracted_side_sci": f"{float(facts['contracted_side']):.17g}",
        "contracted_side_ceiling_12": ceiling_12(facts["contracted_side"]),
    }


def main(argv: list[str]) -> int:
    house_path, cert_path, yaml_path, n_text, out_path = argv[1:6]
    n = int(n_text)
    started = time.process_time()
    house_data = Path(house_path).read_bytes()
    house = read_house(house_data)
    cert = reader.read_cert(Path(cert_path).read_bytes())
    wit = reader.read_witness(Path(yaml_path).read_bytes())
    if house["n"] != n or cert["n"] != n or wit["n"] != n:
        msg = "a file is not of the count named"
        raise SystemExit(msg)
    new_poses = [axes.pose_from_xyt(*row) for row in cert["poses"]]
    hf = measure(house["poses"], house["side"])
    nf = measure(new_poses, cert["side"])
    gain = hf["side"] - nf["side"]
    margin = hf["side_margin"]
    receipt = {
        "program": "rv1009_padding.py",
        "lane": "c-review-1009-1117",
        "decides": "nothing",
        "n": n,
        "house": {
            "file": Path(house_path).name,
            "sha256": hashlib.sha256(house_data).hexdigest(),
            "id": house["id"],
            "representation": house["representation"],
            "source": house["source"],
            **as_json(hf),
        },
        "certificate": as_json(nf),
        "gain": exact(gain),
        "gain_sci": sci(gain),
        "gain_positive": gain > 0,
        "gain_over_house_padding": sci(gain / margin) if margin > 0 else None,
        "gain_within_house_padding": gain <= margin,
        "certificate_below_house_contracted": nf["side"] < hf["contracted_side"],
        "certificate_less_house_contracted_sci": sci(nf["side"] - hf["contracted_side"]),
        "print_12": {
            "house": ceiling_12(hf["side"]),
            "house_contracted": ceiling_12(hf["contracted_side"]),
            "certificate": ceiling_12(nf["side"]),
            "certificate_print_below_house_print": ceiling_12(nf["side"]) < ceiling_12(hf["side"]),
            "certificate_print_below_house_contracted_print": ceiling_12(nf["side"])
            < ceiling_12(hf["contracted_side"]),
            "units_below_house_print": int(
                (F(ceiling_12(hf["side"])) - F(ceiling_12(nf["side"]))) * 10**12
            ),
            "units_below_house_contracted_print": int(
                (F(ceiling_12(hf["contracted_side"])) - F(ceiling_12(nf["side"]))) * 10**12
            ),
        },
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    Path(out_path).write_text(json.dumps(receipt, indent=1) + "\n", encoding="ascii")
    sys.stdout.write(
        f"n={n} house {house['id']} accepted={hf['accepted_by_method_a']} padding={sci(margin, 6)} "
        f"gain={sci(gain, 6)} ratio={receipt['gain_over_house_padding']} "
        f"within={receipt['gain_within_house_padding']} cpu={receipt['cpu_seconds']}s\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
