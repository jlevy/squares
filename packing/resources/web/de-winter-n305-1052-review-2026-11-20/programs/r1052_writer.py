"""Lane r1052's writer: a packing as form J or form C text, every scalar canonical.

It decides nothing. The controls write modified packings with it and read them back
through the reader, so that every whole-file control passes through the reading.
"""

from __future__ import annotations

import json
from fractions import Fraction

FORMAT_J = "lane r1052 control copy: each square [x, y, cos, sin], exact"


def text(value: Fraction) -> str:
    return str(value)


def form_j(side: Fraction, poses: list[tuple[Fraction, Fraction, Fraction, Fraction]]) -> bytes:
    obj = {
        "n": len(poses),
        "side": text(side),
        "square_size": "1",
        "format": FORMAT_J,
        "squares": [[text(v) for v in pose] for pose in poses],
    }
    return (json.dumps(obj, indent=1) + "\n").encode("ascii")


def form_c(
    side: Fraction,
    corners: list[list[tuple[Fraction, Fraction]]],
    *,
    ids: list[str] | None = None,
    origin: str = "lower-left",
) -> bytes:
    shift = side / 2 if origin == "container-center" else Fraction(0)
    lines = [
        "softschema:",
        "  contract: packing.squares:Witness/v2",
        "  envelope: witness",
        "witness:",
        "  id: W-n305-r1052-control",
        f"  n: {len(corners)}",
        f"  side: {text(side)}",
        "  square_size: '1'",
        "  representation: corners",
        "  scalar:",
        "    kind: rational",
        "  coordinates:",
        f"    origin: {origin}",
        "    axes: x-right-y-up",
        "    angle_unit: not-applicable",
        "  claim:",
        "    coordinate_provenance: derived",
        "    method: exact-algebraic",
        "    limitations: a control copy written by lane r1052",
        "  squares:",
    ]
    for k, square in enumerate(corners):
        name = ids[k] if ids is not None else f"square-{k + 1}"
        lines.append(f"  - id: {name}")
        lines.append("    corners:")
        for x, y in square:
            lines.append(f"    - - {text(x - shift)}")
            lines.append(f"      - {text(y - shift)}")
    return ("\n".join(lines) + "\n").encode("ascii")
