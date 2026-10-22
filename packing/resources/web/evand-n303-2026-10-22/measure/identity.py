"""Measure #728's packing at 303 pose by pose against the record's, for credit.

Written for the stage 3 registration of issue 728 (think-icp1), from the stage 1
triage's measurement (c-triage-1022c). A measurement for credit; it decides nothing.
#728's packing is read from this packet's retained certificate, admitted by
`devtools.upper_bound_reports.read_facts` (custody held to the digest the packet pins);
the packings it is compared with are read from their own packets:

- T-186: Mykhailo Polkovskyi's KKT refinement (mishapolk-kkt-refinements-2026-10-14),
  the house best packing at 303;
- T-174: PingYou Ltd's PR 574 fact (pingyou-pr574-certificates-2026-10-13);
- T-162: Daniil Ostashev's #562 certificate (dostashev-compositions-2026-10-12).

The measures are those of the evand-regularized-2026-10-20 packet's measure/identity.py,
loaded from its file unchanged: the nearest centre under each of the box's eight
symmetries, kept only where one to one (`devtools.check_half_angle_area.arrangement_gap`),
and an optimal assignment (least total squared centre displacement under each symmetry,
scipy in binary64): the largest move, the squares moved beyond each bound and the largest
turn. Added here, in binary64 from the exact bases: each packing's tilt classes (a square
is tilted beyond one degree, near upright, or exactly upright where c*s = 0), and, under
the assignment against each packing, how the tilted squares pair by the sign of their
tilt and whether any tilt angle is shared within 1e-4 degrees. Exact sides and their
differences are exact.

Usage, from packing/ with the project interpreter:
    python resources/web/evand-n303-2026-10-22/measure/identity.py \
        --out resources/web/evand-n303-2026-10-22/measure/identity.json
"""

from __future__ import annotations

import argparse
import gzip
import importlib.util
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "src")]

import numpy as np  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402

from devtools import upper_bound_reports as reports  # noqa: E402
from sqpack.yamlio import load_yaml  # noqa: E402

WEB = reports.WEB
PACKET = WEB / "evand-n303-2026-10-22"
MEASURES = WEB / "evand-regularized-2026-10-20/measure/identity.py"
N = 303

type Packing = tuple[Fraction, list[tuple[Fraction, ...]]]


def _measures() -> object:
    spec = importlib.util.spec_from_file_location("evand_regularized_identity", MEASURES)
    if spec is None or spec.loader is None:
        raise SystemExit(f"{MEASURES} is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


m = _measures()
area = m.area  # type: ignore[attr-defined]


def fact(packet: Path) -> Packing:
    """A packet's admitted certificate or derived fact at 303, as the measures read it."""
    certificate = reports.read_facts(packet, {N})[N]
    return certificate.side, area.placed([(p.x, p.y, p.t) for p in certificate.poses])


def witness(path: Path) -> Packing:
    """A retained centre-basis witness, each basis held to the unit circle."""
    document = load_yaml(gzip.decompress(path.read_bytes()).decode("utf-8"))["witness"]
    squares = []
    for square in document["squares"]:
        x, y = (Fraction(str(value)) for value in square["center"])
        c, s = (Fraction(str(value)) for value in square["basis"])
        squares.append((x, y, *area.unit_basis(c, s)))
    return Fraction(str(document["side"])), squares


def sqcert(path: Path) -> Packing:
    """Daniil Ostashev's retained .sqcert, read by the import's own adapter."""
    certificate = reports.ADAPTERS["sqcert"](path.read_bytes(), N, {})
    return certificate.side, area.placed([(p.x, p.y, p.t) for p in certificate.poses])


def signed_tilt(c: Fraction, s: Fraction) -> float:
    """The square's turn in degrees, folded to (-45, 45]."""
    angle = math.degrees(math.atan2(float(s), float(c))) % 90.0
    return angle if angle <= 45.0 else angle - 90.0


def tilt_class(c: Fraction, s: Fraction) -> str:
    if c * s == 0:
        return "upright"
    return "tilted" if abs(signed_tilt(c, s)) >= 1.0 else "near-upright"


def tilts(packing: Packing) -> dict[str, object]:
    squares = packing[1]
    tilted = [signed_tilt(c, s) for _x, _y, c, s in squares if tilt_class(c, s) == "tilted"]
    near = sorted(
        signed_tilt(c, s) for _x, _y, c, s in squares if tilt_class(c, s) == "near-upright"
    )
    return {
        "exactly_turned": sum(1 for _x, _y, c, s in squares if c * s != 0),
        "tilted_beyond_1_degree": len(tilted),
        "tilted_positive": sum(1 for t in tilted if t > 0),
        "tilted_negative": sum(1 for t in tilted if t < 0),
        "tilt_range_degrees": [min(map(abs, tilted)), max(map(abs, tilted))] if tilted else [],
        "near_upright": len(near),
        "near_upright_beyond_1e-3_degrees": [t for t in near if abs(t) > 1e-3],
    }


def bands(first: Packing, second: Packing) -> dict[str, object]:
    """How the first packing's tilted squares pair, by sign, under the identity assignment."""
    a = np.array([[float(x), float(y)] for x, y, _c, _s in first[1]])
    b = np.array([[float(x), float(y)] for x, y, _c, _s in second[1]])
    cost = ((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2)
    rows, cols = linear_sum_assignment(cost)
    moves = np.sqrt(cost[rows, cols])
    same = flipped = to_other = same_within = flipped_beyond = 0
    for i, j, move in zip(rows, cols, moves, strict=True):
        c, s = first[1][i][2], first[1][i][3]
        if tilt_class(c, s) != "tilted":
            continue
        cc, ss = second[1][j][2], second[1][j][3]
        if tilt_class(cc, ss) != "tilted":
            to_other += 1
            continue
        if signed_tilt(c, s) * signed_tilt(cc, ss) > 0:
            same += 1
            same_within += int(move <= 0.1)
        else:
            flipped += 1
            flipped_beyond += int(move > 0.1)
    ours = [signed_tilt(c, s) for _x, _y, c, s in first[1] if tilt_class(c, s) == "tilted"]
    theirs = [signed_tilt(c, s) for _x, _y, c, s in second[1] if tilt_class(c, s) == "tilted"]
    shared = sum(1 for t in ours if any(abs(t - u) < 1e-4 for u in theirs))
    return {
        "assignment": "identity, least total squared centre displacement",
        "tilted_paired_same_sign": same,
        "tilted_paired_same_sign_within_1e-1": same_within,
        "tilted_paired_opposite_sign": flipped,
        "tilted_paired_opposite_sign_beyond_1e-1": flipped_beyond,
        "tilted_paired_with_untilted": to_other,
        "tilt_angles_shared_within_1e-4_degrees": shared,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    ours = fact(PACKET)
    others = {
        "T-186 (70a033f), the house": witness(
            WEB / "mishapolk-kkt-refinements-2026-10-14/facts/n-303.yaml.gz"
        ),
        "T-174 (PR 574)": witness(
            WEB / "pingyou-pr574-certificates-2026-10-13/facts/n-303.yaml.gz"
        ),
        "T-162 (#562)": sqcert(
            WEB / "dostashev-compositions-2026-10-12/source/records/n0303.sqcert"
        ),
    }
    pairs = [
        {
            "view": "#728",
            "against": label,
            **m.measure(ours, packing),  # type: ignore[attr-defined]
            "bands": bands(ours, packing),
        }
        for label, packing in others.items()
    ]
    result = {
        "format": "evand-728-identity-v1",
        "tilts": {"#728": tilts(ours)}
        | {label: tilts(packing) for label, packing in others.items()},
        "pairs": pairs,
    }
    text = json.dumps(result, indent=1, default=str) + "\n"
    args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
