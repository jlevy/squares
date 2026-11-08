"""Exact preflight of unnir's ``s(12) >= 9929/2500`` certificate, and its controls.

jlevy/squares#924 reports ``s(12) >= 9929/2500 = 3.9716`` from
``certificate/s12_lower_3.9716.txt`` of unnir/s12-lower-bound-3.9716 at ``064c2955``: a
plain weighted-point certificate in Evan Daniel's format, 4,996 points over the container
``15886400/4000000``, ``W = 9985226``, total ``119787760/9985226 < 12``. This command
decides in exact rational arithmetic, from the retained bytes and nothing else,
everything the claim rests on but coverage:

- the file has the SHA-256 the issue names, and its bytes are the canonical rendering of
  its integers;
- the header is ``15886400 4000000 / 4000000 / 9985226 / 4996``, so the container is
  exactly ``9929/2500``, ``1/10000`` above ``T-095``'s ``7943/2000``;
- every weight is positive, every point lies in the closed container, the points are
  distinct, the weighted multiset is invariant under the container's eight symmetries,
  and the total is ``119787760/9985226``, below ``12`` by ``34952/9985226``;
- at bin ``39531`` of the net ``N = 96000``, where both reported checkers print their
  least captured weight, a pose of the bin's test square (side ``sigma_k`` as Daniel's
  verifier rounds it, at the bin's left angle, centred where a unit square at that angle
  fits) captures exactly ``9985226/9985226 = 1``: every open cell of the centre
  arrangement in a window around the reported centre is evaluated exactly, and the least
  is the reported minimum. So the certificate has no slack there. This bounds the
  minimum from above and decides nothing about coverage;
- the source's two controls are rebuilt here as its ``verification/replay.py`` writes
  them (``W`` doubled; the last point dropped with the count kept), and two sharper ones
  are added: the orbit of one point captured at that pose lowered by ``1/W`` a point,
  the least change a weight can take, and the same integers read over ``D = 3999600``,
  the precedent's regrid of ``T-095``.

It decides nothing about coverage: whether every closed unit square in the container
captures weight at least one is the checkers' question.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.audit_s12_unnir_certificate \\
        --output OUT.json [--write-controls DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.audit_s12_rescaled_certificate import (
    PointCertificate,
    d4_invariant,
    read,
    sha256,
)
from devtools.audit_s12_v11_certificate import orbit_key, orbits, side_units
from devtools.verify_evand_angle_net_native import sigma

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
PACKET = WEB / "unnir-s12-lower-bound-2026-11-08"
SOURCE = PACKET / "s12-lower-bound-3.9716"
CERTIFICATE = SOURCE / "certificate/s12_lower_3.9716.txt"
CERTIFICATE_SHA256 = "833b76a179a420a40775cc76305ec9ffb7f6ea27472e587958c234c4c4712cbd"

N = 12
HEADER = (15886400, 4_000_000, 4_000_000, 9_985_226, 4996)
SIDE = Fraction(9929, 2500)
#: T-095, the verified bound this certificate would supersede.
T095_SIDE = Fraction(7943, 2000)
TOTAL = 119787760
MARGIN = 34952
NET = 96_000
#: The bin at which both reported checkers print their least captured weight.
TIGHT_BIN = 39531
#: Their least captured weight there, over W: exactly one.
REPORTED_MINIMUM = 9_985_226
#: ``indep_scan``'s diagnostic centre of its least cell, in container coordinates, which
#: it prints in floating point to six decimals; the window below is searched around it.
REPORTED_CENTRE = (Fraction("1.486822"), Fraction("1.219308"))
#: Half the side of the window of rotated-frame centres whose cells are enumerated.
WINDOW = Fraction(1, 1000)
REGRID = 3_999_600
SOURCE_CONTROLS = ("double-denominator", "truncated")
ADDED_CONTROLS = ("lowered-tight-orbit", "regrid-3999600")
CONTROLS = SOURCE_CONTROLS + ADDED_CONTROLS


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def frame(k: int, net: int = NET) -> tuple[int, int, int]:
    """``(cos, sin, g)`` of the net angle ``2 arctan(k/N)``, as ``cos = c/g, sin = s/g``."""
    return net * net - k * k, 2 * k * net, net * net + k * k


def rotated(cert: PointCertificate, k: int) -> list[tuple[Fraction, Fraction, int, int]]:
    """Each point in the frame of bin ``k``'s left angle: ``(u0, u1, weight, index)``."""
    c, s, g = frame(k)
    d = cert.denominator
    return [
        (Fraction(c * x + s * y, g * d), Fraction(-s * x + c * y, g * d), w, i)
        for i, (x, y, w) in enumerate(cert.points)
    ]


def unit_square_fits(cert: PointCertificate, k: int, centre: tuple[Fraction, Fraction]) -> bool:
    """Does the unit square at bin ``k``'s left angle, centred at ``centre``, fit?"""
    c, s, g = frame(k)
    half_width = Fraction(c + s, 2 * g)
    side = cert.side
    return all(half_width <= v <= side - half_width for v in centre)


def tight_pose(cert: PointCertificate, k: int = TIGHT_BIN) -> dict[str, Any]:
    """The least capture over every open cell of bin ``k``'s arrangement in the window.

    The test square has side ``sigma_k`` as Daniel's verifier rounds it, at the bin's
    left angle; a point is captured at a centre ``u`` (in the rotated frame) when both of
    its rotated coordinates lie within ``sigma_k/2`` of ``u``'s. In an open cell between
    consecutive box edges no point lies on an edge, so the capture at the cell's midpoint
    is the cell's. Only cells whose midpoint centres a unit square that fits are counted.
    """
    c, s, g = frame(k)
    half = sigma(k, NET) / 2
    points = rotated(cert, k)
    cx, cy = REPORTED_CENTRE
    centre_u0 = (c * cx + s * cy) / g
    centre_u1 = (-s * cx + c * cy) / g

    def breaks(centre: Fraction, axis: int) -> list[Fraction]:
        lo, hi = centre - WINDOW, centre + WINDOW
        edges = {lo, hi}
        for p in points:
            for e in (p[axis] - half, p[axis] + half):
                if lo < e < hi:
                    edges.add(e)
        return sorted(edges)

    xs, ys = breaks(centre_u0, 0), breaks(centre_u1, 1)
    near = [
        p
        for p in points
        if abs(p[0] - centre_u0) <= half + WINDOW and abs(p[1] - centre_u1) <= half + WINDOW
    ]
    best: tuple[int, Fraction, Fraction, list[int]] | None = None
    cells = 0
    for a, b in pairwise(xs):
        m0 = (a + b) / 2
        for e, f in pairwise(ys):
            m1 = (e + f) / 2
            centre = ((c * m0 - s * m1) / g, (s * m0 + c * m1) / g)
            if not unit_square_fits(cert, k, centre):
                continue
            cells += 1
            captured = [p for p in near if abs(p[0] - m0) < half and abs(p[1] - m1) < half]
            weight = sum(p[2] for p in captured)
            if best is None or weight < best[0]:
                best = (weight, m0, m1, sorted(p[3] for p in captured))
    _require(best is not None, "no admissible cell in the window")
    assert best is not None
    weight, m0, m1, indices = best
    centre = ((c * m0 - s * m1) / g, (s * m0 + c * m1) / g)
    units = side_units(cert)
    return {
        "bin": k,
        "net": NET,
        "sigma": str(2 * half),
        "window_half_side": str(WINDOW),
        "cells": cells,
        "least_capture": f"{weight}/{cert.weight_scale}",
        "least_capture_units": weight,
        "rotated_centre": [str(m0), str(m1)],
        "centre": [str(v) for v in centre],
        "centre_decimal": [f"{float(v):.9f}" for v in centre],
        "unit_square_fits": unit_square_fits(cert, k, centre),
        "captured": [
            {
                "index": i,
                "point": list(cert.points[i]),
                "orbit": list(orbit_key(cert.points[i][0], cert.points[i][1], units)),
            }
            for i in indices
        ],
    }


def tight_orbit(pose: dict[str, Any]) -> tuple[int, int]:
    """The orbit of the heaviest point captured at the tight pose (least index on ties).

    The heaviest, so that lowering it by ``1/W`` leaves every weight positive: the least
    weights in the file are ``1/W``.
    """
    heaviest = max(pose["captured"], key=lambda entry: (entry["point"][2], -entry["index"]))
    return (heaviest["orbit"][0], heaviest["orbit"][1])


def lowered_tight_orbit(cert: PointCertificate, pose: dict[str, Any]) -> PointCertificate:
    """The orbit of `tight_orbit` lowered by ``1/W`` a point, the least change possible."""
    key = tight_orbit(pose)
    units = side_units(cert)
    return PointCertificate(
        cert.s_num,
        cert.s_den,
        cert.denominator,
        cert.weight_scale,
        tuple((x, y, w - 1 if orbit_key(x, y, units) == key else w) for x, y, w in cert.points),
    )


def flat(values: Sequence[int]) -> bytes:
    """The rendering of `verification/replay.py`: the integers on one line."""
    return (" ".join(map(str, values)) + "\n").encode()


def control_bytes(cert: PointCertificate, pose: dict[str, Any]) -> dict[str, bytes]:
    """Every control's bytes: the source's two as its helper writes them, then ours."""
    _require(
        (cert.s_num, cert.s_den, cert.denominator, cert.weight_scale, len(cert.points))
        == HEADER,
        "the controls are defined on the reported file",
    )
    tokens = [cert.s_num, cert.s_den, cert.denominator, cert.weight_scale, len(cert.points)]
    tokens += [v for point in cert.points for v in point]
    doubled = list(tokens)
    doubled[3] *= 2
    return {
        "double-denominator": flat(doubled),
        "truncated": flat(tokens[:-3]),
        "lowered-tight-orbit": lowered_tight_orbit(cert, pose).render(),
        "regrid-3999600": PointCertificate(
            cert.s_num, REGRID, REGRID, cert.weight_scale, cert.points
        ).render(),
    }


def audit() -> dict[str, Any]:
    """Every exact check of the module docstring, as named booleans and values."""
    data, cert = read(CERTIFICATE, CERTIFICATE_SHA256)
    side = cert.side
    weights = [w for _, _, w in cert.points]
    total = sum(weights)
    in_container = all(
        Fraction(x, cert.denominator) <= side and Fraction(y, cert.denominator) <= side
        for x, y, _ in cert.points
    )
    grouped = orbits(cert)
    pose = tight_pose(cert)
    mutated = control_bytes(cert, pose)
    key = tight_orbit(pose)
    lowered_by = sum(1 for entry in pose["captured"] if tuple(entry["orbit"]) == key)
    lowered = lowered_tight_orbit(cert, pose)
    checks = {
        "certificate_digest": sha256(data) == CERTIFICATE_SHA256,
        "rendering_is_byte_exact": cert.render() == data,
        "header_is_15886400_4000000_4000000_9985226_4996": (
            cert.s_num,
            cert.s_den,
            cert.denominator,
            cert.weight_scale,
            len(cert.points),
        )
        == HEADER,
        "container_is_9929_over_2500": side == SIDE,
        "advance_over_t095_is_1_over_10000": side - T095_SIDE == Fraction(1, 10000),
        "weights_positive": min(weights) > 0,
        "points_in_container": in_container,
        "points_distinct": len({(x, y) for x, y, _ in cert.points}) == len(cert.points),
        "d4_invariant": d4_invariant(cert),
        "total_is_119787760": total == TOTAL,
        "total_below_n": total < N * cert.weight_scale,
        "margin_is_34952": N * cert.weight_scale - total == MARGIN,
        "tight_pose_captures_exactly_the_reported_minimum": pose["least_capture_units"]
        == REPORTED_MINIMUM,
        "tight_pose_centres_a_unit_square_that_fits": pose["unit_square_fits"],
        "lowered_control_drops_the_tight_pose_below_one": REPORTED_MINIMUM - lowered_by
        < cert.weight_scale
        and lowered_by > 0,
        "lowered_control_keeps_every_weight_positive": min(w for _, _, w in lowered.points) > 0,
    }
    controls: dict[str, Any] = {}
    for name, raw in mutated.items():
        entry: dict[str, Any] = {"sha256": sha256(raw), "bytes": len(raw)}
        tokens = raw.split()
        if name != "truncated":
            values = [int(t) for t in tokens]
            entry["side"] = str(Fraction(values[0], values[1]))
            entry["total_weight"] = f"{sum(values[7::3])}/{values[3]}"
        controls[name] = entry
    units = side_units(cert)
    controls["lowered-tight-orbit"].update(
        {
            "orbit": list(key),
            "orbit_points": [
                list(p) for p in cert.points if orbit_key(p[0], p[1], units) == key
            ],
            "orbit_points_captured_at_tight_pose": lowered_by,
            "tight_pose_capture": f"{REPORTED_MINIMUM - lowered_by}/{cert.weight_scale}",
        }
    )
    pose = dict(
        pose,
        captured_count=len(pose["captured"]),
        captured=[entry["index"] for entry in pose["captured"]],
    )
    return {
        "schema": "S12UnnirPreflight/v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "issue": "https://github.com/jlevy/squares/issues/924",
        "certificate": str(CERTIFICATE.relative_to(REPO)),
        "certificate_sha256": CERTIFICATE_SHA256,
        "checks": checks,
        "side": str(side),
        "side_decimal": f"{float(side):.10f}",
        "t095_side": str(T095_SIDE),
        "advance_over_t095": str(side - T095_SIDE),
        "points": len(cert.points),
        "orbits": len(grouped),
        "orbit_sizes": {
            str(size): sum(1 for members in grouped.values() if len(members) == size)
            for size in sorted({len(members) for members in grouped.values()})
        },
        "least_weight": f"{min(weights)}/{cert.weight_scale}",
        "greatest_weight": f"{max(weights)}/{cert.weight_scale}",
        "total_weight": f"{total}/{cert.weight_scale}",
        "counting_gap": str(N - Fraction(total, cert.weight_scale)),
        "tight_pose": pose,
        "controls": controls,
    }


def write_controls(directory: Path) -> dict[str, Path]:
    _, cert = read(CERTIFICATE, CERTIFICATE_SHA256)
    directory.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for name, raw in control_bytes(cert, tight_pose(cert)).items():
        path = directory / f"{name}.txt"
        path.write_bytes(raw)
        written[name] = path
    return written


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--output", type=Path, help="write the receipt here as JSON")
    parser.add_argument("--write-controls", type=Path, help="write the four controls here")
    args = parser.parse_args(argv)
    result = audit()
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with atomic_output_file(args.output) as handle:
            handle.write_text(text)
    if args.write_controls:
        for name, path in write_controls(args.write_controls).items():
            print(f"{name}: {path} sha256 {sha256(path.read_bytes())}")
    failed = [name for name, ok in result["checks"].items() if not ok]
    total = len(result["checks"])
    print(f"{result['status']}: {total - len(failed)} of {total} checks")
    for name in failed:
        print(f"  failed: {name}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
