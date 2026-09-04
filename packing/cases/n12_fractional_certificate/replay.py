"""Load any retained n = 12 certificate and hand it to the exact verifier.

Eight rungs are retained. `certificate.json` carries the current bound
`s(12) >= 99/25`; `certificate-79-20.json` is its immediate predecessor; and
`certificate-19-5.json` is the first rung. The JSON carries exact rationals as strings,
so a replay reconstructs the object the generator proposed. Nothing here decides
anything: the verdict comes from `sqpack.fractional.certificate.verify`, and this module
only feeds it.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from sqpack.fractional.certificate import Certificate
from sqpack.fractional.model import Atom

CERTIFICATE_PATH = Path(__file__).with_name("certificate.json")
PREVIOUS_RUNG_PATH = Path(__file__).with_name("certificate-79-20.json")
FIRST_RUNG_PATH = Path(__file__).with_name("certificate-19-5.json")


def load(path: Path = CERTIFICATE_PATH) -> Certificate:
    """Rebuild the retained certificate exactly as it was accepted."""

    record = json.loads(path.read_text())
    limit = Fraction(record["angle_limit"])
    steps = int(record["direction_steps"])
    return Certificate(
        n=int(record["n"]),
        outer_side=Fraction(record["outer_side"]),
        square_side=Fraction(record["square_side"]),
        atoms=tuple(
            Atom(f"{index:03d}", Fraction(x), Fraction(y), Fraction(weight))
            for index, (x, y, weight) in enumerate(record["atoms"])
        ),
        half_tangents=tuple(limit * k / steps for k in range(steps + 1)),
        symmetry=record["symmetry"],
    )


def declared(path: Path = CERTIFICATE_PATH) -> dict[str, str]:
    """What the record claims, for a replay to compare against."""

    record = json.loads(path.read_text())
    return {key: str(record[key]) for key in ("claim", "total_mass", "least_cell_mass")}
