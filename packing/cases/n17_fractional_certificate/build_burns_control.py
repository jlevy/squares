"""Rebuild Burns's published n = 17 certificate as a control in the case's own schema.

Sam Burns's August 2026 note proposes ``s(17) >= 44811/10000 = 4.4811`` on 268
rationally weighted atoms: a 29 by 29 grid of step ``(L - 1)/28`` from ``1/2``,
37 ``D4`` orbit seeds, weights in units of ``1/10000``, total mass
``169476/10000``, and least covered mass ``10003/10000``. The retained source
verifier lives under ``resources/web/n17-lower-bounds-2026/``; this module
rebuilds the same atoms from the note's constants so the certificate can be
handed to the repository's two decision procedures.

It is a control, not a claim. Its value as a control is the one number the
adopted Massaccesi control cannot supply: a least covered mass that is not
exactly ``1``. A verifier that only ever reports ``1/1`` is caught here.

Run as ``python -m cases.n17_fractional_certificate.build_burns_control`` to
print the record; ``--check PATH`` reports whether the shipped file matches.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path

L = Fraction(44811, 10000)
B = Fraction(9973, 10000)
T = Fraction(207107, 500000)
KMAX = 180
WEIGHT_SCALE = 10000
NGRID = 29
LAST = NGRID - 1
SOURCE = "https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/"
CONTROL_PATH = Path(__file__).with_name("control-burns-4-4811.json")

# (i, j, w): every distinct D4 image of grid point (i, j) receives weight w/10000.
# Transcribed from Section 3 of the retained proof note.
SEEDS: tuple[tuple[int, int, int], ...] = (
    (1, 11, 107),
    (2, 4, 137),
    (2, 9, 214),
    (2, 11, 107),
    (2, 12, 137),
    (3, 4, 3884),
    (3, 7, 214),
    (3, 8, 913),
    (3, 9, 214),
    (3, 10, 214),
    (3, 11, 1234),
    (3, 12, 2189),
    (3, 14, 384),
    (4, 4, 1961),
    (4, 7, 520),
    (4, 8, 214),
    (4, 9, 1413),
    (4, 10, 1234),
    (4, 11, 1083),
    (4, 13, 137),
    (4, 14, 292),
    (7, 11, 529),
    (7, 12, 33),
    (8, 10, 906),
    (8, 11, 384),
    (8, 12, 351),
    (9, 9, 340),
    (9, 10, 180),
    (9, 11, 204),
    (9, 12, 549),
    (10, 12, 879),
    (10, 13, 201),
    (10, 14, 378),
    (11, 11, 396),
    (11, 12, 622),
    (11, 13, 204),
    (11, 14, 204),
)


def orbit(i: int, j: int) -> set[tuple[int, int]]:
    n = LAST
    return {
        (i, j),
        (n - i, j),
        (i, n - j),
        (n - i, n - j),
        (j, i),
        (n - j, i),
        (j, n - i),
        (n - j, n - i),
    }


def build() -> dict[str, object]:
    step = (L - 1) / LAST
    coord = [Fraction(1, 2) + step * i for i in range(NGRID)]
    by_index: dict[tuple[int, int], int] = {}
    for i, j, w in SEEDS:
        for ij in orbit(i, j):
            if ij in by_index:
                raise ValueError(f"two seeds reach grid point {ij}")
            by_index[ij] = w
    atoms = [
        [str(coord[i]), str(coord[j]), str(Fraction(w, WEIGHT_SCALE))]
        for (i, j), w in sorted(by_index.items())
    ]
    total = sum((Fraction(w, WEIGHT_SCALE) for w in by_index.values()), start=Fraction(0))
    return {
        "id": "control-n17-burns-4.4811",
        "n": 17,
        "claim": f"s(17) >= {L}",
        "outer_side": str(L),
        "square_side": str(B),
        "angle_limit": str(T),
        "direction_steps": KMAX,
        "total_mass": str(total),
        "least_cell_mass": str(Fraction(10003, 10000)),
        "symmetry": "D4",
        "source": SOURCE,
        "atoms": atoms,
    }


def render(record: dict[str, object]) -> str:
    return json.dumps(record, indent=1) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and not (len(arguments) == 2 and arguments[0] == "--check"):
        print(f"unknown arguments: {' '.join(arguments)}", file=sys.stderr)
        return 2
    text = render(build())
    if len(arguments) == 2 and arguments[0] == "--check":
        shipped = Path(arguments[1]).read_text()
        if shipped == text:
            print(f"control rebuilt from the note's constants: identical to {arguments[1]}")
            return 0
        print(f"MISMATCH: {arguments[1]} differs from the rebuilt control")
        return 1
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
