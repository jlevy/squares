"""Load any retained n = 12 certificate and hand it to the exact verifier.

Eight rungs are retained. `certificate.json` carries the bound the case holds,
s(12) >= 99/25, on 2097 atoms of total mass 149987/12500;
`certificate-79-20.json` is the rung immediately below it; and
`certificate-19-5.json` is the first rung the same instrument reached, kept
because it is a far smaller object (68 atoms against 2097) and the one the
discovery commit cites. The JSON carries exact rationals as strings, so a replay
reconstructs the same object the generator proposed. Nothing here decides
anything: the verdict comes from `sqpack.fractional.certificate.verify`, and
this module only feeds it.
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


def _from_record(record: dict) -> Certificate:
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
