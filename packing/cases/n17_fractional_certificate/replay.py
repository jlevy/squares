"""Load the retained n = 17 certificates and hand them to the exact verifier.

Three certificates are retained. `certificate.json` carries the bound the case
holds; `certificate-229-50.json` and `certificate-451-100.json` are the rungs
below it, the second of them the first value that displaced Massaccesi's
published 22529/5000 = 4.5058.
All three lift n = 18 and n = 19 with them, and not by monotonicity: only C1
mentions n, so an atom set certifies its side for every integer above its own
mass, which for each of these is 17 and upward.

The JSON carries exact rationals as strings, so a replay reconstructs the same
object the generator proposed.
Nothing here decides anything: the verdict comes from
`sqpack.fractional.certificate.verify`, and this module only feeds it.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from sqpack.fractional.certificate import Certificate
from sqpack.fractional.model import Atom

CERTIFICATE_PATH = Path(__file__).with_name("certificate.json")
SECOND_RUNG_PATH = Path(__file__).with_name("certificate-229-50.json")
FIRST_RUNG_PATH = Path(__file__).with_name("certificate-451-100.json")


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
