"""Writers of both forms, in the layout of de Winter's files (lane r127b-1118).

Decides nothing. Used by the self-test and the controls, which write a changed packing
as bytes and read it back through the strict readers, so that every whole-file control
passes through the same reading as the certificates.
"""

from __future__ import annotations

import rb127_read as R

Q = tuple[int, int]


def scalar(v: Q) -> str:
    p, q = v
    if q < 0:
        p, q = -p, -q
    return str(p) if q == 1 else f"{p}/{q}"


def form_j(n: int, side: Q, rows: list[tuple[Q, Q, Q, Q]]) -> bytes:
    lines = ["{", f' "n": {n},', f' "side": "{scalar(side)}",', ' "square_size": "1",',
             f' "format": "{R.FORMAT_SENTENCE}",', ' "squares": [']
    for k, row in enumerate(rows):
        lines.append("  [")
        for c, v in enumerate(row):
            lines.append(f'   "{scalar(v)}"' + ("," if c < 3 else ""))
        lines.append("  ]" + ("," if k < len(rows) - 1 else ""))
    lines.append(" ]")
    lines.append("}")
    return "\n".join(lines).encode("ascii")


def _yaml_scalar(v: Q) -> str:
    s = scalar(v)
    return f"'{s}'" if "/" not in s else s


def form_c(n: int, side: Q, corners: list[tuple[tuple[Q, Q], ...]], *, id_style: str = "square-k") -> bytes:
    lines = [
        "softschema:",
        "  contract: packing.squares:Witness/v2",
        "  schema: https://github.com/jlevy/squares/blob/main/packing/witnesses/witness.schema.yaml",
        "  envelope: witness",
        "  status: enforced",
        "witness:",
        "  id: W-n127-control",
        f"  n: {n}",
        f"  side: {_yaml_scalar(side)}",
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
        "    limitations: A control written by the review's own writer.",
        "  squares:",
    ]
    for k, sq in enumerate(corners, 1):
        lines.append(f"  - id: square-{k}" if id_style == "square-k" else f"  - id: {k}")
        lines.append("    corners:")
        for x, y in sq:
            lines.append(f"    - - {_yaml_scalar(x)}")
            lines.append(f"      - {_yaml_scalar(y)}")
    return ("\n".join(lines) + "\n").encode("ascii")
