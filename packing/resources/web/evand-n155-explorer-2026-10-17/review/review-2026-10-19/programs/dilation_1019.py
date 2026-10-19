"""Hold #674's two s(229) certificates to the dilation their header states (19 October review).

Each certificate's first line says it is ``dilate_cert.py``'s dilation, by ``delta 1e-12``,
of a named binary64 packing that its packet retains beside it. This program reads both
files as data and re-derives the certificate from the input by the construction the
retained ``search/packer/dilate_cert.py`` documents, written again here from that
description; the source program is not run:

- the factor is ``f = 1 + delta``, with ``delta`` the binary64 number ``1e-12`` read
  exactly (``Fraction(1e-12)``), which is not ``10^-12``;
- the side is ``ceil(S f 10^30) / 10^30`` for the input's printed side ``S``, and each
  centre coordinate ``round(v f 10^30) / 10^30``, ties to even, for its printed ``v``;
- each ``t`` is the best rational approximation with denominator at most ``10^15`` to the
  binary64 ``tan(radians(theta mod 90) / 2)`` of the printed angle ``theta`` in degrees.

It then splits each least margin the maintained routes report into the input's own
margin, the dilation's share and the rounding's, as exact identities: for the square and
wall of the least clearance, ``clearance' = clearance + (f - 1) * lever + rounding``,
where the lever is the centre's distance from that wall in the input; for the pair of the
least separating-axis gap, along its separating axis ``u``, ``gap' = gap + (f - 1) * (c_j
- c_i).u + rounding``. Both margins are measured with the certificate's own rotations at
the input's centres and side, so that only the dilation and the rounding of the centres
and side change between the two. The separating-axis gap is the maintained routes'
measure (``sqpack.witness._margin_summary``), recomputed here only to compare; this
program decides nothing.

The other three certificates (#669's 155, #659's 236, #664's 271) are, by the source's
``search/exact/README.md``, its 80-digit KKT point scaled by ``1 + 1e-20`` about the
origin corner, centres rounded to ``10^-35`` and the side rounded up. Each packet retains
that point (``*.exact.txt``, printed at 70 digits), so this program also holds each side
to ``ceil(S* (1 + 10^-20) 10^30) / 10^30`` and counts the centres equal to
``round(v (1 + 10^-20) 10^35) / 10^35``; that explains their margins and decides nothing.

Usage, from ``packing/`` with the project interpreter::

    python -I dilation_1019.py --json OUT.json
"""

from __future__ import annotations

import argparse
import json
import lzma
import math
import sys
from fractions import Fraction
from pathlib import Path

WEB = Path.cwd() / "resources/web"
CASES = (
    (
        "#674 n229 opening",
        "evand-n229-dilation-2026-10-17",
        "search/packer/candidates/s229.input.txt",
        "search/packer/candidates/s229.cert",
    ),
    (
        "#674 n229 update",
        "evand-n229-dilation-update-2026-10-18",
        "search/packer/candidates/s229_v2.input.txt",
        "search/packer/candidates/s229_v2.cert",
    ),
)
DIGITS = 10**30
DELTA = Fraction(1e-12)
FACTOR = 1 + DELTA


def rows(text: str) -> list[list[str]]:
    return [line.split() for line in text.splitlines() if line.strip() and not line.startswith("#")]


def rotation(t: Fraction) -> tuple[Fraction, Fraction]:
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def half_width(c: Fraction, s: Fraction, ux: Fraction, uy: Fraction) -> Fraction:
    """Half the width of the unit square turned by (c, s) along the unit axis u."""
    return (abs(ux * c + uy * s) + abs(-ux * s + uy * c)) / 2


def sci(value: Fraction) -> str:
    return f"{float(value):.6e}"


def wall_margins(side: Fraction, centres: list[tuple[Fraction, Fraction]], turns: list[tuple[Fraction, Fraction]]):
    """Every square-to-wall clearance: (clearance, square, wall), walls 0..3 = x=0, y=0, x=S, y=S."""
    out = []
    for index, ((x, y), (c, s)) in enumerate(zip(centres, turns, strict=True)):
        h = (abs(c) + abs(s)) / 2
        out.extend(((x - h, index, 0), (y - h, index, 1), (side - x - h, index, 2), (side - y - h, index, 3)))
    return out


def pair_gap(ci, cj, ti, tj) -> tuple[Fraction, tuple[Fraction, Fraction]]:
    """The separating-axis gap of two unit squares over the four edge axes, and its axis."""
    best: tuple[Fraction, tuple[Fraction, Fraction]] | None = None
    for c, s in (ti, tj):
        for ux, uy in ((c, s), (-s, c)):
            pi = ci[0] * ux + ci[1] * uy
            pj = cj[0] * ux + cj[1] * uy
            width = half_width(*ti, ux, uy) + half_width(*tj, ux, uy)
            gap = abs(pj - pi) - width
            if best is None or gap > best[0]:
                sign = 1 if pj >= pi else -1
                best = (gap, (sign * ux, sign * uy))
    assert best is not None
    return best


def least_pair(centres, turns) -> tuple[Fraction, int, int, tuple[Fraction, Fraction]]:
    best = None
    for i in range(len(centres)):
        for j in range(i + 1, len(centres)):
            dx, dy = centres[j][0] - centres[i][0], centres[j][1] - centres[i][1]
            if dx * dx + dy * dy >= 4:
                continue
            gap, axis = pair_gap(centres[i], centres[j], turns[i], turns[j])
            if best is None or gap < best[0]:
                best = (gap, i, j, axis)
    assert best is not None
    return best


def analyse(key: str, packet: str, input_path: str, cert_path: str) -> dict[str, object]:
    source = WEB / packet / "source"
    head_line = (source / cert_path).read_text(encoding="ascii").splitlines()[0]
    inp = rows((source / input_path).read_text(encoding="ascii"))
    cert = rows((source / cert_path).read_text(encoding="ascii"))
    n = int(inp[0][0])
    side_in = Fraction(inp[0][1])
    side_cert = Fraction(cert[0][1])
    out: dict[str, object] = {"header": head_line, "n": n, "input_side": inp[0][1], "certificate_side": str(side_cert)}
    expected_side = Fraction(math.ceil(side_in * FACTOR * DIGITS), DIGITS)
    exact_power = Fraction(math.ceil(side_in * (1 + Fraction(1, 10**12)) * DIGITS), DIGITS)
    out["side_is_ceil_S_f_at_30_places"] = expected_side == side_cert
    out["side_with_exact_10^-12_instead"] = str(exact_power)
    out["side_with_exact_10^-12_minus_certificate"] = sci(exact_power - side_cert)
    out["side_rounding_up"] = sci(side_cert - side_in * FACTOR)
    out["delta_binary64"] = str(DELTA)
    out["delta_minus_10^-12"] = sci(DELTA - Fraction(1, 10**12))
    centres_in, centres_cert, turns, mismatched_t = [], [], [], []
    centre_matches = t_matches = 0
    rounding: list[tuple[Fraction, Fraction]] = []
    for index, (row_in, row_cert) in enumerate(zip(inp[1 : n + 1], cert[1 : n + 1], strict=True)):
        x, y = Fraction(row_in[0]), Fraction(row_in[1])
        xc, yc, tc = Fraction(row_cert[0]), Fraction(row_cert[1]), Fraction(row_cert[2])
        if (xc, yc) == (Fraction(round(x * FACTOR * DIGITS), DIGITS), Fraction(round(y * FACTOR * DIGITS), DIGITS)):
            centre_matches += 1
        theta = math.radians(float(row_in[2]) % 90.0)
        t = Fraction(math.tan(theta / 2)).limit_denominator(10**15)
        if t == tc:
            t_matches += 1
        else:
            mismatched_t.append({"square": index, "recomputed": str(t), "certificate": str(tc), "difference": sci(t - tc)})
        centres_in.append((x, y))
        centres_cert.append((xc, yc))
        rounding.append((xc - x * FACTOR, yc - y * FACTOR))
        turns.append(rotation(tc))
    out["centres_equal_construction"] = f"{centre_matches} of {n}"
    out["tangents_equal_construction"] = f"{t_matches} of {n}"
    out["tangent_mismatches"] = mismatched_t
    out["largest_centre_rounding"] = sci(max(max(abs(a), abs(b)) for a, b in rounding))
    # Walls.
    walls_in = wall_margins(side_in, centres_in, turns)
    walls_cert = wall_margins(side_cert, centres_cert, turns)
    least_cert = min(walls_cert)
    clearance_cert, square, wall = least_cert
    clearance_in = next(c for c, i, w in walls_in if i == square and w == wall)
    x, y = centres_in[square]
    lever = (x, y, side_in - x, side_in - y)[wall]
    rho = rounding[square][wall % 2]
    side_round = side_cert - side_in * FACTOR
    rounding_term = rho if wall < 2 else side_round - rho
    identity = clearance_cert == clearance_in + DELTA * lever + rounding_term
    near_walls = [
        cc
        for (ci, _i, _w), (cc, _j, _v) in zip(walls_in, walls_cert, strict=True)
        if ci < Fraction(1, 10**12)
    ]
    out["walls"] = {
        "least_certificate_clearance": str(clearance_cert),
        "least_certificate_clearance_decimal": sci(clearance_cert),
        "square": square,
        "wall": ["x = 0", "y = 0", "x = S", "y = S"][wall],
        "input_clearance_there": sci(clearance_in),
        "lever": sci(lever),
        "dilation_share": sci(DELTA * lever),
        "rounding_share": sci(rounding_term),
        "identity_holds_exactly": identity,
        "least_input_clearance": sci(min(walls_in)[0]),
        "input_clearances_below_1e-12": len(near_walls),
        "certificate_clearance_over_those": [sci(min(near_walls)), sci(max(near_walls))] if near_walls else None,
    }
    # Pairs.
    gap_cert, i, j, axis = least_pair(centres_cert, turns)
    ux, uy = axis
    width = half_width(*turns[i], ux, uy) + half_width(*turns[j], ux, uy)
    along_in = (centres_in[j][0] - centres_in[i][0]) * ux + (centres_in[j][1] - centres_in[i][1]) * uy
    gap_in_axis = along_in - width
    rounding_pair = (rounding[j][0] - rounding[i][0]) * ux + (rounding[j][1] - rounding[i][1]) * uy
    dilation_pair = DELTA * along_in
    identity_pair = gap_cert == gap_in_axis + dilation_pair + rounding_pair
    gap_in_least, _a, _b, _axis = least_pair(centres_in, turns)
    out["pairs"] = {
        "least_certificate_gap": str(gap_cert),
        "least_certificate_gap_decimal": sci(gap_cert),
        "pair": [i, j],
        "input_gap_on_that_axis": sci(gap_in_axis),
        "centre_distance_on_that_axis": sci(along_in),
        "dilation_share": sci(dilation_pair),
        "rounding_share": sci(rounding_pair),
        "identity_holds_exactly": identity_pair,
        "least_input_gap": sci(gap_in_least),
    }
    # The receipt's margins, read as data.
    record = json.loads(lzma.decompress((WEB / packet / "receipts/exact-certification.json.xz").read_bytes()))
    (positive,) = [case for case in record["cases"] if case["control"] == "positive"]
    out["receipt"] = {
        route: {
            "clearance_equal": Fraction(positive[route]["minimum_containment_clearance"]) == clearance_cert,
            "gap_equal": Fraction(positive[route]["minimum_best_pair_gap"]) == gap_cert,
        }
        for route in ("exact_verify", "independent")
    }
    return out


KKT = (
    ("#669 n155", "evand-n155-explorer-2026-10-17", "search/packer/candidates/s155_ex2"),
    ("#659 n236", "evand-n236-2026-10-16", "search/packer/candidates/s236_bm3c"),
    ("#664 n271", "evand-n271-2026-10-17", "search/packer/candidates/s271_ex1"),
)


def kkt_dilation(packet: str, stem: str) -> dict[str, object]:
    """The side and centres of a certificate against its retained 70-digit KKT point."""
    source = WEB / packet / "source"
    point = rows((source / f"{stem}.exact.txt").read_text(encoding="ascii"))
    cert = rows((source / f"{stem}.cert").read_text(encoding="ascii"))
    eps = Fraction(1, 10**20)
    side_star, side_cert = Fraction(point[0][1]), Fraction(cert[0][1])
    equal = 0
    largest = Fraction(0)
    n = int(point[0][0])
    for a, b in zip(point[1 : n + 1], cert[1 : n + 1], strict=True):
        made = tuple(Fraction(round(Fraction(v) * (1 + eps) * 10**35), 10**35) for v in a[:2])
        kept = (Fraction(b[0]), Fraction(b[1]))
        if made == kept:
            equal += 1
        largest = max(largest, *(abs(u - v) for u, v in zip(made, kept, strict=True)))
    return {
        "kkt_side_digits": point[0][1],
        "side_is_ceil_S_star_times_1_plus_1e-20_at_30_places": Fraction(
            math.ceil(side_star * (1 + eps) * DIGITS), DIGITS
        )
        == side_cert,
        "certificate_side_minus_kkt_side": sci(side_cert - side_star),
        "centres_equal_construction": f"{equal} of {n}",
        "largest_centre_difference": sci(largest),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)
    report: dict[str, object] = {key: analyse(key, packet, i, c) for key, packet, i, c in CASES}
    kkt = {key: kkt_dilation(packet, stem) for key, packet, stem in KKT}
    args.json.write_text(json.dumps({**report, "kkt": kkt}, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({**report, "kkt": kkt}, indent=1))
    good = all(r["side_is_ceil_S_star_times_1_plus_1e-20_at_30_places"] for r in kkt.values()) and all(
        r["side_is_ceil_S_f_at_30_places"]
        and r["walls"]["identity_holds_exactly"]
        and r["pairs"]["identity_holds_exactly"]
        and all(v["clearance_equal"] and v["gap_equal"] for v in r["receipt"].values())
        for r in report.values()
    )
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
