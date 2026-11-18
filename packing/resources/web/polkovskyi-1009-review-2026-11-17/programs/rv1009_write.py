"""Writers of the two forms, for the self-test and the controls. Decides nothing.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Clean-room.

A modified packing is written as the bytes of a form P file and of a form C file, and
read back through the readers, so that a control passes through everything a certificate
passes through.
"""

from __future__ import annotations

from fractions import Fraction

import rv1009_geom as geom


def scalar_text(value: Fraction) -> str:
    """Canonical text of a rational: ``p`` or ``p/q`` in lowest terms."""
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def cert_bytes(
    rows: list[geom.Row],
    side: Fraction,
    *,
    stated_n: int | None = None,
    side_text: str | None = None,
) -> bytes:
    """Form P: one comment line, the header, one row for each square."""
    n = len(rows) if stated_n is None else stated_n
    lines = [f"# control packing written by lane c-review-1009-1117 (n = {n})"]
    lines.append(f"{n} {scalar_text(side) if side_text is None else side_text}")
    lines.extend(f"{scalar_text(x)} {scalar_text(y)} {scalar_text(t)}" for x, y, t in rows)
    return ("\n".join(lines) + "\n").encode("ascii")


def witness_bytes(
    quads: list[object],
    side: Fraction,
    *,
    stated_n: int | None = None,
    side_text: str | None = None,
    ids: list[str] | None = None,
) -> bytes:
    """Form C: a Witness/v2 envelope with four corners for each square, laid out as the
    source's files are."""
    n = len(quads) if stated_n is None else stated_n
    side_out = scalar_text(side) if side_text is None else side_text
    lines = [
        "softschema:",
        "  contract: packing.squares:Witness/v2",
        "  schema: https://github.com/jlevy/squares/blob/main/packing/witnesses/witness.schema.yaml",
        "  envelope: witness",
        "  status: enforced",
        "witness:",
        f"  id: W-n{n}-control-c-review-1009-1117",
        f"  n: {n}",
        f"  side: '{side_out}'",
        "  square_size: '1'",
        "  representation: corners",
        "  scalar:",
        "    kind: rational",
        "  coordinates:",
        "    origin: lower-left",
        "    axes: x-right-y-up",
        "    angle_unit: not-applicable",
        "  claim:",
        "    coordinate_provenance: reported",
        "    method: exact-algebraic",
        "    limitations: A control packing of this review, not a claim.",
        "  squares:",
    ]
    for k, quad in enumerate(quads):
        ident = f"square-{k + 1}" if ids is None else ids[k]
        lines.append(f"  - id: {ident}")
        lines.append("    corners:")
        for x, y in quad:  # type: ignore[union-attr]
            lines.append(f"    - - '{scalar_text(x)}'")
            lines.append(f"      - '{scalar_text(y)}'")
    return ("\n".join(lines) + "\n").encode("ascii")


def both_forms(rows: list[geom.Row], side: Fraction) -> tuple[bytes, bytes]:
    """The two files of one packing."""
    return cert_bytes(rows, side), witness_bytes([geom.corners(r) for r in rows], side)
