"""Load the retained n = 11 certificates and hand them to the exact verifier.

Three certificates are retained. `certificate.json` carries the bound the case
holds, s(11) >= 381/100; `certificate-19-5.json` is the rung below it, the first
value that moved this case past Stromquist; and `certificate-189-50.json` is the
calibration rung below Stromquist's bound, which proves nothing new, and that is
the point -- it is the diagnostic the project registered in advance to test the
approach honestly.

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
FIRST_RUNG_PATH = Path(__file__).with_name("certificate-189-50.json")
STROMQUIST_RUNG_PATH = Path(__file__).with_name("certificate-19-5.json")


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
