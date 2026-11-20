"""Lane r1012's writer: a packing as Witness/v2 corners text, for the self-test and controls.

It writes every scalar in canonical form ('p/q', or 'p' for an integer), single
quoted, inside the softschema envelope. It decides nothing.
"""

from fractions import Fraction


def scalar_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return f"'{value.numerator}'"
    return f"'{value.numerator}/{value.denominator}'"


def id_text(sid):
    if isinstance(sid, int):
        return str(sid)
    return "'" + str(sid).replace("'", "''") + "'"


def write(n, side, ids, quads, origin="lower-left", side_text=None, representation="corners",
          kind="rational", square_size="'1'"):
    """quads: lower-left frame; with origin container-center they are shifted by -S/2."""
    shift = Fraction(side) / 2 if origin == "container-center" else Fraction(0)
    lines = [
        "softschema:",
        "  contract: packing.squares:Witness/v2",
        "  schema: ../witness.schema.yaml",
        "  envelope: witness",
        "  status: enforced",
        "witness:",
        "  id: W-r1012-control",
        f"  n: {n}",
        f"  side: {side_text if side_text is not None else scalar_text(side)}",
        f"  square_size: {square_size}",
        f"  representation: {representation}",
        "  scalar:",
        f"    kind: {kind}",
        "  coordinates:",
        f"    origin: {origin}",
        "    axes: x-right-y-up",
        "    angle_unit: not-applicable",
        "  squares:",
    ]
    for sid, quad in zip(ids, quads):
        lines.append(f"  - id: {id_text(sid)}")
        lines.append("    corners:")
        for x, y in quad:
            lines.append(f"    - [{scalar_text(x - shift)}, {scalar_text(y - shift)}]")
    lines += [
        "  claim:",
        "    coordinate_provenance: reported",
        "    method: exact-algebraic",
        "    limitations: written by lane r1012's controls; decides nothing",
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")
