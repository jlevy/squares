"""Load the retained n = 18 certificate and hand it to the exact verifier.

One certificate is retained. ``certificate.json`` sits at container side 467/100
with total mass 8937839/500000. The atoms carry more than one registered case
each: only Condition 2 mentions n among the five conditions, so a set of total
mass M certifies its side for every integer strictly above M. This mass lies in
[17, 18), so it certifies n = 18 and says nothing about n = 17, where T-019's
459/100 certificate still holds the register. From n = 19 on the register already
holds 24/5, so the certificate is true there and weaker.

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


def _from_record(record: dict) -> Certificate:
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


def snapshot(path: Path = CERTIFICATE_PATH) -> tuple[Certificate, dict[str, str], bytes]:
    """Parse one byte snapshot into the certificate and its declarations."""

    data = path.read_bytes()
    record = json.loads(data)
    declarations = {key: str(record[key]) for key in ("claim", "total_mass", "least_cell_mass")}
    return _from_record(record), declarations, data


def load(path: Path = CERTIFICATE_PATH) -> Certificate:
    """Rebuild the retained certificate exactly as it was accepted."""

    return snapshot(path)[0]


def declared(path: Path = CERTIFICATE_PATH) -> dict[str, str]:
    """What the record claims, for a replay to compare against."""

    return snapshot(path)[1]
