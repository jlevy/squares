"""Load the retained n = 20 certificate and hand it to the exact verifier.

One certificate is retained, at container side 24/5. Its atoms carry three
registered cases rather than one: only C1 mentions n among the five conditions,
so a set of total mass 946131/50000 certifies its side for every integer above
that mass, which is 19 and upward. At n = 19 and n = 20 the side improves the
register directly; at n = 21 it improves Nagamochi's closed form as well; from
n = 22 on the register already holds 5, so the certificate is true there and
weaker.

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
            Atom(f"{index:04d}", Fraction(x), Fraction(y), Fraction(weight))
            for index, (x, y, weight) in enumerate(record["atoms"])
        ),
        half_tangents=tuple(limit * k / steps for k in range(steps + 1)),
        symmetry=record["symmetry"],
    )


def declared(path: Path = CERTIFICATE_PATH) -> dict[str, str]:
    """What the record claims, for a replay to compare against."""

    record = json.loads(path.read_text())
    return {key: str(record[key]) for key in ("claim", "total_mass", "least_cell_mass")}
