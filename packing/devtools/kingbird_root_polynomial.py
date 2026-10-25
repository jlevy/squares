#!/usr/bin/env python3
"""Measure the polynomial a Kingbird picture prints as a Mathematica `Root`, against its pin.

Usage, from `packing/`, after `uv run --frozen --all-extras --group dev`::

    python -m devtools.kingbird_root_polynomial 83               # fetch, measure, print
    python -m devtools.kingbird_root_polynomial 83 --write       # and write the receipt
    python -m devtools.kingbird_root_polynomial 83 --svg PATH    # read a copy instead

The catalogue's n = 83 is algebraic of degree 672, and its picture, `square-83.svg`,
prints the side in a comment as `s = Root[p, 27]`: `p` a polynomial in `#1` and 27 the
root's index in Mathematica's order. The Kingbird retention policy keeps no picture
(packing/resources/web/known-best-packings/README.md), so the register of exact sides
holds that polynomial by the picture's digest, which the pictures receipt of
5 October 2026 pins, and by the facts this measures from it.

**The boundary.** The picture is fetched, or read from `--svg`, into memory, and its
bytes are held to the size and SHA-256 the pictures receipt pins before anything is read
from them: bytes acquired from another party, held against the value the review pinned
(OR-16). Different bytes are refused, exit 2; the catalogue may have changed the
picture, and a new reading is a new pin.

**What it measures** (`measure`). From the `Root` object: the polynomial's degree, how
many coefficients it has and how many are nonzero, whether it is primitive, its leading
coefficient's sign and digits, its height in digits and its constant term's digits, and
the root's index. From the picture's `s` entity: the printed side and its places. It
then decides, exactly, that `p` changes sign across the printed side widened by one unit
of its last place and has exactly one root there, by Descartes' rule of signs
(`exact_side_register.root_count`); at n = 83 that takes about a minute. Neither the
picture nor its coefficients are retained, and irreducibility over Q and the count of
real roots below the side (the source's index) are not measured here: think-chsu.

`--write` writes the receipt `exact_side_register` reads,
`resources/web/known-best-packings/receipts/kingbird-nNNN-root-polynomial.json`.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import exact_side_register as register
from sqpack import retained_json

FORMAT = "kingbird-root-polynomial-v1"
GENERATOR = "python -m devtools.kingbird_root_polynomial"
#: The comment's statement of the side: `s = Root[p, k]`, `p` in `#1`, perhaps written as
#: a pure function, `p &`.
_ROOT = re.compile(
    r"\bs\s*=\s*Root\[(?P<polynomial>[^\[\]]*?)\s*&?\s*,\s*(?P<index>[0-9]+)\s*\]", re.DOTALL
)
#: One term of `p`, its whitespace removed: a signed integer, then `*#1` with an optional
#: power, or `#1` with an optional power and the coefficient one left unwritten.
_TERM = re.compile(
    r"(?P<sign>[+-]?)(?:(?P<coefficient>[0-9]+)(?P<times>\*#1(?:\^(?P<power>[0-9]+))?)?"
    r"|(?P<bare>#1(?:\^(?P<bare_power>[0-9]+))?))"
)
#: The picture's printed side, its `s` entity.
_SIDE = re.compile(r'<!ENTITY\s+s\s+"(?P<side>[0-9]+\.[0-9]+)"\s*>')


class MeasurementError(ValueError):
    """The picture is not the pinned one, or it does not state what this measures."""


@dataclass(frozen=True)
class Pin:
    """A picture as the pictures receipt pins it."""

    n: int
    url: str
    size: int
    sha256: str
    last_modified: str | None

    @classmethod
    def of(cls, n: int) -> Pin:
        reading = register.pinned_picture(n)
        return cls(
            n=n,
            url=str(reading["url"]),
            size=int(reading["bytes"]),
            sha256=str(reading["sha256"]),
            last_modified=reading.get("last_modified"),
        )


def receipt_path(n: int) -> Path:
    return register.KINGBIRD_RECEIPTS / f"kingbird-n{n:03d}-root-polynomial.json"


def held(data: bytes, pin: Pin) -> None:
    """Refuse bytes that are not the pinned picture's: the trust boundary of a download."""
    if len(data) != pin.size or hashlib.sha256(data).hexdigest() != pin.sha256:
        raise MeasurementError(
            f"n={pin.n}: the picture is not the pinned one ({pin.size} bytes, SHA-256 "
            f"{pin.sha256}); a changed picture is a new reading and a new pin"
        )


def root_object(svg: str) -> tuple[tuple[int, ...], int, int]:
    """The `Root` object's polynomial, highest degree first, its index and its length."""
    match = _ROOT.search(svg)
    if match is None:
        raise MeasurementError("the picture states no `s = Root[p, k]`")
    written = re.sub(r"\s+", "", match["polynomial"])
    terms: dict[int, int] = {}
    position = 0
    while position < len(written):
        term = _TERM.match(written, position)
        if term is None or term.end() == position or (position and not term["sign"]):
            raise MeasurementError(
                f"not a polynomial in #1 at {written[position : position + 40]!r}"
            )
        if term["coefficient"] is not None:
            coefficient = int(term["coefficient"])
            power = int(term["power"] or 1) if term["times"] else 0
        else:
            coefficient, power = 1, int(term["bare_power"] or 1)
        if power in terms:
            raise MeasurementError(f"#1^{power} is written twice")
        terms[power] = (-1 if term["sign"] == "-" else 1) * coefficient
        position = term.end()
    degree = max(terms)
    polynomial = tuple(terms.get(power, 0) for power in range(degree, -1, -1))
    return polynomial, int(match["index"]), len(match["polynomial"])


def printed_side(svg: str) -> str:
    match = _SIDE.search(svg)
    if match is None:
        raise MeasurementError("the picture prints no side entity `s`")
    return match["side"]


def digits(number: int) -> int:
    return len(str(abs(number)))


def measure(data: bytes, pin: Pin, *, today: str) -> dict[str, Any]:
    """The receipt of one pinned picture's `Root` polynomial, its root isolated exactly."""
    held(data, pin)
    svg = data.decode("utf-8")
    polynomial, index, characters = root_object(svg)
    printed = printed_side(svg)
    places = len(printed.split(".", 1)[1])
    unit = Fraction(1, 10**places)
    low, high = Fraction(printed) - unit, Fraction(printed) + unit
    signs = [register.sign(polynomial, low), register.sign(polynomial, high)]
    if 0 in signs or signs[0] == signs[1]:
        raise MeasurementError(f"p does not change sign across {printed} +- 1e-{places}")
    # One transform decides the usual case; `root_count` bisects only where it does not.
    changes = register.variations(polynomial, low, high)
    found = changes if changes <= 1 else register.root_count(polynomial, low, high)
    if found != 1:
        raise MeasurementError(f"p has {found} roots within 1e-{places} of {printed}, not one")
    return {
        "format": FORMAT,
        "n": pin.n,
        "measured_by": f"{GENERATOR} {pin.n} --write",
        "measured_on": today,
        "url": pin.url,
        "bytes": pin.size,
        "last_modified": pin.last_modified,
        "pinned_in": register.repository_path(register.PICTURES),
        "retained": False,
        "polynomial": {
            "variable": "#1",
            "degree": len(polynomial) - 1,
            "coefficients": len(polynomial),
            "nonzero_coefficients": sum(1 for term in polynomial if term),
            "primitive": math.gcd(*polynomial) == 1 and polynomial[0] > 0,
            "leading_sign": 1 if polynomial[0] > 0 else -1,
            "leading_digits": digits(polynomial[0]),
            "height_digits": max(digits(term) for term in polynomial),
            "constant_digits": digits(polynomial[-1]),
            "text_characters": characters,
        },
        "root": {
            "index": index,
            "printed": printed,
            "places": places,
            "low": register.cut(low, places, up=False),
            "high": register.cut(high, places, up=True),
            "endpoint_signs": signs,
            "sign_variations": changes,
            "roots": found,
            "method": (
                "Descartes' rule of signs on (1 + x)^d p((low + high x) / (1 + x)), in "
                "exact integers: one sign change, so exactly one root in (low, high)"
            ),
        },
        "not_measured": (
            "irreducibility over Q, and the count of real roots below the side that the "
            "source's Root index states (think-chsu)"
        ),
    }


def fetch(pin: Pin) -> bytes:
    """The picture, as `derive_kingbird_facts.fetch_picture` fetches catalogue SVGs."""
    from devtools.derive_kingbird_facts import fetch_picture  # noqa: PLC0415 -- network only

    return fetch_picture(pin.url)[0]


def text(receipt: Mapping[str, Any]) -> str:
    return retained_json.dumps(receipt, ensure_ascii=False) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("n", type=int, help="the count whose pinned picture to measure")
    parser.add_argument("--svg", type=Path, help="read this copy instead of fetching")
    parser.add_argument("--write", action="store_true", help="write the receipt")
    args = parser.parse_args(argv)
    try:
        pin = Pin.of(args.n)
        data = args.svg.read_bytes() if args.svg else fetch(pin)
        receipt = measure(data, pin, today=datetime.now(UTC).date().isoformat())
    except (MeasurementError, register.RegisterError) as error:
        print(f"kingbird root polynomial: {error}", file=sys.stderr)
        return 2
    content = text(receipt)
    if args.write:
        path = receipt_path(args.n)
        with atomic_output_file(path) as temporary:
            temporary.write_text(content, encoding="utf-8")
        print(f"wrote {register.repository_path(path)}")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
