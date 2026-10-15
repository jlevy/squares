"""Decide exactly the 14 October ledger's undecided comparisons that have two exact sides.

The upper-bound ledger of 14 October 2026
(``packing/campaign/issue-intake/upper-bounds-20261014/README.md``, Undecided
Comparisons) leaves 21 rows undecided, all PR #574 (PingYou Ltd) against the reported
lane of a case record or a pending register entry. Seventeen have an exact side on both
sides, and this tool decides them; at the other four (29, 55, 71, 83) the record holds
only the Kingbird print, and the receipt names the input each needs. It changes neither
the ledger nor the record.

Every side is an exact real number of one of four kinds, and no decision uses floating
point:

- **rational**: a fraction.
- **root**: the one real root of a squarefree integer polynomial in a rational interval,
  certified by Sturm's theorem (`Root`). A case record's ``minimal_polynomial`` is taken
  at its print, in the window of one unit of the print's last place either side; a
  register entry's polynomial in its retained root interval.
- **field**: ``c0 + c1 b + ...`` with ``b`` the root of a minimal polynomial in an
  isolating interval, in `sqpack.field.NumberField`: PR #574's algebraic witnesses.
- **closed form** ``k - (1/2)sqrt(2) + sqrt(1 + sqrt(2))``, the reported lane at 54, 107
  and 178, as ``k + 1/2 - a^2/2 + a`` in ``Q(a)``, ``a`` the root of ``x^4 - 2x^2 - 1``
  in ``(3/2, 8/5)``. The tool checks in the field that ``a^2 - 1`` squares to 2 and is
  positive and that ``a`` is positive with ``a^2 = 1 + (a^2 - 1)``, so ``a`` is
  ``sqrt(1 + sqrt(2))``.

A root against a rational is decided by one sign: the rational's position in the
isolating interval and the polynomial's sign there. A field element against the closed
form is equal exactly when the closed form, moved by the side's rational part, is a root
of the witness's minimal polynomial inside its isolating interval; otherwise both are
refined until their enclosures separate. Each row's margin, PR #574's side minus the
standing one, is given by rigorous bounds.

Two commands:

- ``extract`` reads PR #574's sides from files exported from the PR #574 lane's branch
  and from the pull request (`LANE_COMMIT`, `PR_COMMIT`), and from the v2 certificate
  at 17, and writes them to `SIDES` with the commit and path each file was read at; the
  downloaded certificate alone keeps its digest. That lane's packet is not on ``main``,
  so its sides are kept here.
- ``decide`` reads `SIDES` and the record's sides from the repository and writes
  `RESOLVED`; ``--check`` compares the retained receipt with a fresh decision.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.decide_undecided_comparisons \\
        extract --inputs DIR
    uv run --frozen --all-extras --group dev python -m devtools.decide_undecided_comparisons \\
        decide
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools.check_source_coverage import parse_case
from sqpack.field import FieldElement, NumberField
from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
PACKING = REPO / "packing"
FRONTIER = PACKING / "frontier"
#: The ledger's intake directory, which keeps the sides and the receipt beside the ledger.
INTAKE = PACKING / "campaign/issue-intake/upper-bounds-20261014"
SIDES = INTAKE / "undecided-sides.json"
RESOLVED = INTAKE / "undecided-resolved.json"
LEDGER = "packing/campaign/issue-intake/upper-bounds-20261014/README.md"
CATALOGUE = (
    PACKING / "resources/web/evand-exact-and-local-reports-2026-10-07/reported-catalogue.json"
)

LANE_BRANCH = "claude/wizardly-meitner-wqn4x3-intake-1014-pr574"
LANE_COMMIT = "56cf868c617975eaada5b0c10dab953cc6fa2e37"
LANE_PACKET = "packing/resources/web/pingyou-pr574-certificates-2026-10-13"
PR_COMMIT = "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde"
PR_CLAIMS = "packing/resources/web/pingyou-numerical-refinements-2026-10-13/claims.json"
V2_ARCHIVE = {
    "repository": "BuddenPing/square-packing-certificates",
    "tag": "data/pingyou-numerical-refinements-2026-10-13-v2",
    "asset": "pingyou-numerical-refinements-2026-10-13.zip",
    "sha256": "ced042973412d43217aab66b5c07fe6242e019a8280efc20bb99650c97892249",
    "member": "numerical-refinements/certificates/n017.cert.json",
}

KINGBIRD = "record [Kingbird] (reported lane)"
#: The Undecided Comparisons table, read and not edited: what each row is against.
DECIDABLE: dict[int, str] = {
    17: KINGBIRD,
    28: KINGBIRD,
    37: KINGBIRD,
    39: KINGBIRD,
    41: KINGBIRD,
    54: KINGBIRD,
    69: KINGBIRD,
    87: KINGBIRD,
    106: "register T-121, pending adoption",
    107: KINGBIRD,
    128: KINGBIRD,
    152: "register T-122, pending adoption",
    177: "register T-123, pending adoption",
    178: KINGBIRD,
    205: KINGBIRD,
    235: KINGBIRD,
    300: KINGBIRD,
}
REGISTER = {106: "T-121", 152: "T-122", 177: "T-123"}
#: The four rows whose record side has no exact form, with the input each needs.
GATED: dict[int, str] = {
    29: (
        "an exact side for the reported lane's packing: the case record holds only the "
        "Kingbird print 5.93383346267692; Evan Daniel's degree-7213 minimal polynomial "
        "(#545) is unpublished (think-6gti)"
    ),
    55: (
        "an exact side for the reported lane's packing: the case record holds only the "
        "Kingbird print 7.94577100750391 (exact_form and minimal_polynomial null)"
    ),
    71: (
        "an exact side for the reported lane's packing: the case record holds only the "
        "Kingbird print 8.94407155757031 (exact_form and minimal_polynomial null)"
    ),
    83: (
        "an exact side for the reported lane's packing: the case record holds only the "
        "Kingbird print 9.63475764863108 and algebraic_degree 672, with no minimal "
        "polynomial (exact_form and minimal_polynomial null)"
    ),
}
_CLOSED_FORM = re.compile(r"(\d+) - \(1/2\)sqrt\(2\) \+ sqrt\(1 \+ sqrt\(2\)\)")
_MONOMIAL = re.compile(r"([+-]?)(\d*)(s(?:\^\{?(\d+)\}?)?)?")

type Json = dict[str, Any]


class DecisionError(ValueError):
    """An input is not what the tool can decide exactly."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _rel(path: Path) -> str:
    return path.resolve().relative_to(REPO).as_posix()


# --------------------------------------------------------------------- integer polynomials


def parse_polynomial(text: str) -> list[int]:
    """The integer coefficients, highest first, of ``4775s^{18} - 190430s^{17} + ... = 0``;
    a right-hand side other than none or ``0`` is refused."""
    written, _, right = text.partition("=")
    if right.strip() not in ("", "0"):
        raise DecisionError(f"the right-hand side is not 0: {text!r}")
    written = written.replace(" ", "")
    terms: dict[int, int] = {}
    position = 0
    while position < len(written):
        match = _MONOMIAL.match(written, position)
        if match is None or match.end() == position:
            raise DecisionError(f"not a polynomial in s: {text!r}")
        sign = -1 if match[1] == "-" else 1
        if match[3]:
            degree, coefficient = int(match[4] or 1), int(match[2] or 1)
        elif match[2]:
            degree, coefficient = 0, int(match[2])
        else:
            raise DecisionError(f"not a polynomial in s: {text!r}")
        if degree in terms:
            raise DecisionError(f"repeated term s^{degree} in {text!r}")
        terms[degree] = sign * coefficient
        position = match.end()
    if not terms:
        raise DecisionError(f"not a polynomial in s: {text!r}")
    return [terms.get(d, 0) for d in range(max(terms), -1, -1)]


def _trim(poly: Sequence[int]) -> list[int]:
    out = list(poly)
    while out and out[0] == 0:
        out.pop(0)
    return out


def _primitive(poly: Sequence[int]) -> list[int]:
    content = math.gcd(*poly)
    return [c // content for c in poly]


def _derivative(poly: Sequence[int]) -> list[int]:
    degree = len(poly) - 1
    return [c * (degree - i) for i, c in enumerate(poly[:-1])]


def _pseudo_remainder(a: Sequence[int], b: Sequence[int]) -> list[int]:
    """``|lc(b)|^k a mod b`` for the least k that clears denominators: a positive multiple
    of the remainder, so the signs a Sturm chain needs are kept."""
    rest, scale, sign = list(a), abs(b[0]), 1 if b[0] > 0 else -1
    while len(rest) >= len(b) and any(rest):
        lead = rest[0]
        shifted = list(b) + [0] * (len(rest) - len(b))
        rest = [scale * r - sign * lead * s for r, s in zip(rest, shifted, strict=True)][1:]
        rest = _trim(rest)
    return rest


def sturm_chain(poly: Sequence[int]) -> list[list[int]]:
    """A Sturm chain of a squarefree integer polynomial, each member scaled by a positive
    integer; refuses a polynomial with a repeated factor."""
    chain = [_primitive(_trim(poly)), _primitive(_derivative(_trim(poly)))]
    while len(chain[-1]) > 1:
        rest = _pseudo_remainder(chain[-2], chain[-1])
        if not rest:
            raise DecisionError("the polynomial is not squarefree")
        chain.append(_primitive([-c for c in rest]))
    return chain


def evaluate(poly: Sequence[int], point: Fraction) -> Fraction:
    total = Fraction(0)
    for coefficient in poly:
        total = total * point + coefficient
    return total


def _sign(value: Fraction | int) -> int:
    return (value > 0) - (value < 0)


def _variations(chain: Sequence[Sequence[int]], point: Fraction) -> int:
    signs = [s for s in (_sign(evaluate(p, point)) for p in chain) if s]
    return sum(1 for a, b in pairwise(signs) if a != b)


def root_count(poly: Sequence[int], low: Fraction, high: Fraction) -> int:
    """The distinct real roots of ``poly`` in ``(low, high)``, neither end a root."""
    if evaluate(poly, low) == 0 or evaluate(poly, high) == 0:
        raise DecisionError("an interval end is a root")
    chain = sturm_chain(poly)
    return _variations(chain, low) - _variations(chain, high)


@dataclass(frozen=True)
class Root:
    """The one root of a squarefree integer polynomial in ``(low, high)``."""

    poly: tuple[int, ...]
    low: Fraction
    high: Fraction

    @classmethod
    def isolate(cls, poly: Sequence[int], low: Fraction, high: Fraction) -> Root:
        count = root_count(poly, low, high)
        if count != 1:
            raise DecisionError(f"({low}, {high}) holds {count} roots, not one")
        return cls(tuple(poly), low, high)

    def refined(self, width: Fraction) -> Root:
        """The same root in an interval narrower than ``width``, by bisection."""
        low, high = self.low, self.high
        low_sign = _sign(evaluate(self.poly, low))
        while high - low >= width:
            middle = (low + high) / 2
            value = _sign(evaluate(self.poly, middle))
            if value == 0:
                return Root(self.poly, middle - width / 4, middle + width / 4)
            if value == low_sign:
                low = middle
            else:
                high = middle
        return Root(self.poly, low, high)

    def compare(self, value: Fraction) -> int:
        """The sign of ``value - root``, decided exactly."""
        if value <= self.low:
            return -1
        if value >= self.high:
            return 1
        at = _sign(evaluate(self.poly, value))
        if at == 0:
            return 0
        return -1 if at == _sign(evaluate(self.poly, self.low)) else 1


# ------------------------------------------------------------------------------- sides


def closed_form(text: str) -> tuple[NumberField, FieldElement]:
    """``k - (1/2)sqrt(2) + sqrt(1 + sqrt(2))`` as an element of ``Q(sqrt(1 + sqrt(2)))``."""
    match = _CLOSED_FORM.fullmatch(text.strip())
    if match is None:
        raise DecisionError(f"not the closed form this tool reads: {text!r}")
    field = NumberField([1, 0, -2, 0, -1], (Fraction(3, 2), Fraction(8, 5)))
    a = field.alpha
    root2 = a * a - 1
    if not ((root2 * root2 - 2).is_zero() and root2.sign() > 0):
        raise DecisionError("a^2 - 1 is not sqrt(2)")
    if not ((a * a - (root2 + 1)).is_zero() and a.sign() > 0):
        raise DecisionError("a is not sqrt(1 + sqrt(2))")
    return field, int(match[1]) - root2 / 2 + a


def field_side(side: Json) -> tuple[NumberField, FieldElement]:
    """PR #574's algebraic side: its coefficients in ``Q(b)``, low degree first."""
    field = NumberField(
        [Fraction(c) for c in side["minimal_polynomial"]],
        (Fraction(side["isolating_interval"][0]), Fraction(side["isolating_interval"][1])),
    )
    return field, field.element([Fraction(c) for c in side["coefficients"]])


def print_window(text: str) -> tuple[Fraction, Fraction]:
    """The print plus and minus one unit of its last place."""
    unit = Fraction(1, 10 ** len(text.partition(".")[2]))
    return Fraction(text) - unit, Fraction(text) + unit


type Exact = Root | tuple[NumberField, FieldElement]


def record_side(n: int) -> tuple[Json, Exact]:
    """The standing side the row is against, read from the repository: its description,
    and the exact number."""
    if n in REGISTER:
        catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
        claim = catalogue["new_form_claims"][str(n)]
        poly = list(reversed(claim["polynomial_ascending"]))
        low, high = (Fraction(x) for x in claim["reported_root_interval"])
        exact = Root.isolate(poly, low, high)
        return {
            "kind": "root",
            "holder": REGISTER[n],
            "degree": len(poly) - 1,
            "polynomial": [str(c) for c in poly],
            "interval": [str(low), str(high)],
            "interval_from": "the retained reported_root_interval",
            "print": claim["reported_side"],
            "read_from": f"{_rel(CATALOGUE)}, new_form_claims.{n}",
        }, exact
    lane = parse_case(FRONTIER / f"n-{n:03d}.md")["reported_upper_bound"]
    read_from = f"packing/frontier/n-{n:03d}.md, reported_upper_bound"
    if lane.get("exact_form") and _CLOSED_FORM.fullmatch(str(lane["exact_form"])):
        return {
            "kind": "closed form",
            "holder": lane["source_key"],
            "exact_form": lane["exact_form"],
            "print": lane["value"],
            "read_from": read_from,
        }, closed_form(str(lane["exact_form"]))
    if not lane.get("minimal_polynomial"):
        raise DecisionError(f"n = {n}: the reported lane has no exact side")
    poly = parse_polynomial(str(lane["minimal_polynomial"]))
    low, high = print_window(str(lane["value"]))
    exact = Root.isolate(poly, low, high)
    if lane.get("algebraic_degree") not in (None, len(poly) - 1):
        raise DecisionError(f"n = {n}: algebraic_degree is not the polynomial's degree")
    return {
        "kind": "root",
        "holder": lane["source_key"],
        "degree": len(poly) - 1,
        "polynomial": [str(c) for c in poly],
        "interval": [str(low), str(high)],
        "interval_from": "the print plus and minus one unit of its last place",
        "print": lane["value"],
        "read_from": read_from,
    }, exact


# ---------------------------------------------------------------------------- deciding


def _sci(value: Fraction, *, rounding: str, digits: int = 6) -> str:
    """``value`` in scientific notation at ``digits`` significant places, rounded ``up``,
    ``down`` or to the ``nearest``."""
    if value == 0:
        return "0"
    size = abs(value)
    exponent = len(str(size.numerator)) - len(str(size.denominator))
    while Fraction(10) ** exponent > size:
        exponent -= 1
    while Fraction(10) ** (exponent + 1) <= size:
        exponent += 1
    scaled = value * Fraction(10) ** (digits - 1 - exponent)
    rounder = {"up": math.ceil, "down": math.floor, "nearest": round}[rounding]
    mantissa = int(rounder(scaled))
    if abs(mantissa) == 10**digits:
        mantissa //= 10
        exponent += 1
    sign, text = ("-" if mantissa < 0 else ""), str(abs(mantissa))
    return f"{sign}{text[0]}.{text[1:]}e{exponent:+d}"


def _relation(sign: int) -> str:
    return {-1: "below", 0: "equal", 1: "above"}[sign]


def _margin(low: Fraction, high: Fraction) -> Json:
    return {"low": _sci(low, rounding="down"), "high": _sci(high, rounding="up")}


def decide_rational(value: Fraction, root: Root) -> Json:
    """PR #574's rational side against a root: the relation and the margin's bounds."""
    sign = root.compare(value)
    if sign == 0:
        return {
            "relation": "equal",
            "margin": "0",
            "margin_bounds": _margin(Fraction(0), Fraction(0)),
        }
    tight = root
    while True:
        tight = tight.refined((tight.high - tight.low) / 2**20)
        low, high = value - tight.high, value - tight.low
        if _sign(low) == _sign(high) == sign and abs(high - low) * 10**6 < abs(low):
            return {
                "relation": _relation(sign),
                "margin": _sci((low + high) / 2, rounding="nearest", digits=3),
                "margin_bounds": _margin(low, high),
            }


def decide_fields(
    report: tuple[NumberField, FieldElement],
    record: tuple[NumberField, FieldElement],
    side: Json,
) -> Json:
    """PR #574's field side against the closed form, both exact."""
    (report_field, report_value), (record_field, record_value) = report, record
    coefficients = [Fraction(c) for c in side["coefficients"]]
    if len(coefficients) == 2 and coefficients[1] != 0:
        moved = (record_value - coefficients[0]) / coefficients[1]
        poly = [Fraction(c) for c in side["minimal_polynomial"]]
        at = record_field.zero
        for c in poly:
            at = at * moved + c
        low, high = (Fraction(x) for x in side["isolating_interval"])
        if at.is_zero() and (moved - low).sign() > 0 and (moved - high).sign() < 0:
            return {
                "relation": "equal",
                "margin": "0",
                "margin_bounds": _margin(Fraction(0), Fraction(0)),
                "equality": (
                    "the closed form minus the side's rational part, over its coefficient, "
                    "is a root of the witness's minimal polynomial inside its isolating "
                    "interval, so it is the witness's root"
                ),
            }
    for digits in range(40, 4000, 40):
        report_field.refine_to(digits)
        record_field.refine_to(digits)
        a_low, a_high = report_field.enclose(report_value)
        b_low, b_high = record_field.enclose(record_value)
        low, high = a_low - b_high, a_high - b_low
        if _sign(low) == _sign(high) != 0 and abs(high - low) * 10**6 < abs(low):
            sign = _sign(low)
            return {
                "relation": _relation(sign),
                "margin": _sci((low + high) / 2, rounding="nearest", digits=3),
                "margin_bounds": _margin(low, high),
            }
    raise DecisionError("the two sides did not separate at 4,000 places")


def decide_row(n: int, sides: Json) -> Json:
    report = sides["sides"][str(n)]
    record, exact = record_side(n)
    row: Json = {"n": n, "report": "PR #574", "against": DECIDABLE[n]}
    if report["kind"] == "rational" and isinstance(exact, Root):
        row |= decide_rational(Fraction(report["value"]), exact)
        row["method"] = "the rational's position in the root's isolating interval, by one sign"
    elif report["kind"] == "field" and not isinstance(exact, Root):
        row |= decide_fields(field_side(report), exact, report)
        row["method"] = "exact arithmetic in the two number fields"
    else:
        raise DecisionError(f"n = {n}: no rule for {report['kind']} against {record['kind']}")
    row["pr574_side"] = {k: v for k, v in report.items() if k != "value"} | (
        {"value_digits": len(report["value"])} if "value" in report else {}
    )
    row["standing_side"] = {k: v for k, v in record.items() if k != "polynomial"}
    return row


def resolved_receipt(sides: Json) -> Json:
    rows = [decide_row(n, sides) for n in sorted(DECIDABLE)]
    counts = {
        name: sum(1 for row in rows if row["relation"] == name)
        for name in ("below", "equal", "above")
    }
    return {
        "schema": "undecided-comparisons-resolved/v1",
        "tool": "devtools.decide_undecided_comparisons decide",
        "ledger": f"{LEDGER}, Undecided Comparisons (read, not edited)",
        "relation": (
            "PR #574's side against the standing one: below means PR #574's upper bound is "
            "the smaller; margin is PR #574's side minus the standing side, with rigorous "
            "bounds rounded outward"
        ),
        "sides": _rel(SIDES),
        "counts": counts,
        "rows": rows,
        "gated": [
            {"n": n, "report": "PR #574", "against": KINGBIRD, "needs": need}
            for n, need in GATED.items()
        ],
    }


# ------------------------------------------------------------------------------ extract


def extract(inputs: Path) -> Json:
    """PR #574's sides at the 17 rows, from the exported files in ``inputs``."""
    # The files this repository's branches hold are named by commit and path; the
    # certificate, downloaded from the release archive, by the digest PR #574 names.
    files: dict[str, Json] = {
        "lane-claims.json": {
            "commit": LANE_COMMIT,
            "path": f"{LANE_PACKET}/acquisition/claims.json",
        },
        "lane-algebraic-claims.json": {
            "commit": LANE_COMMIT,
            "path": f"{LANE_PACKET}/acquisition/algebraic-claims.json",
        },
        "pr-claims.json": {"commit": PR_COMMIT, "path": PR_CLAIMS},
        "n017.cert.json": {
            "path": V2_ARCHIVE["member"],
            "sha256": sha256((inputs / "n017.cert.json").read_bytes()),
        },
    }
    for n in (54, 107, 178):
        files[f"facts/alg-n-{n:03d}.yaml.gz"] = {
            "commit": LANE_COMMIT,
            "path": f"{LANE_PACKET}/facts/alg-n-{n:03d}.yaml.gz",
        }
    lane = {
        row["n"]: row
        for row in json.loads((inputs / "lane-claims.json").read_bytes())["results"]
    }
    algebraic = {
        row["n"]: row
        for row in json.loads((inputs / "lane-algebraic-claims.json").read_bytes())["results"]
    }
    sides: dict[str, Json] = {}
    for n in sorted(DECIDABLE):
        if n == 17:
            (row,) = [
                r
                for r in json.loads((inputs / "pr-claims.json").read_bytes())["rows"]
                if r["n"] == 17
            ]
            certificate = json.loads((inputs / "n017.cert.json").read_bytes())
            if files["n017.cert.json"]["sha256"] != row["portable_certificate_sha256"]:
                raise DecisionError(
                    "n017.cert.json is not the certificate PR #574's claim names"
                )
            if certificate["s_exact"] != row["side_exact"]:
                raise DecisionError("the certificate's side is not the side PR #574 prints")
            sides["17"] = {
                "kind": "rational",
                "value": str(Fraction(row["side_exact"])),
                "print": row["safe_upper_bound_40_decimals"],
                "read_from": (
                    f"{PR_CLAIMS} at {PR_COMMIT}, rows[n = 17].side_exact, equal to s_exact of "
                    f"{V2_ARCHIVE['member']} in {V2_ARCHIVE['asset']} (SHA-256 "
                    f"{V2_ARCHIVE['sha256'][:8]}...), whose digest the row names"
                ),
            }
        elif n in algebraic:
            fact = safe_load(
                gzip.decompress((inputs / f"facts/alg-n-{n:03d}.yaml.gz").read_bytes()).decode()
            )
            witness = fact["witness"]
            scalar = witness["scalar"]
            claim = algebraic[n]
            if (
                claim["minimal_polynomial"] != scalar["minimal_polynomial"]
                or claim["side"] != witness["side"]
            ):
                raise DecisionError(f"n = {n}: the claim and the fact disagree")
            sides[str(n)] = {
                "kind": "field",
                "minimal_polynomial": [str(c) for c in scalar["minimal_polynomial"]],
                "isolating_interval": [str(c) for c in scalar["isolating_interval"]],
                "coefficients": [str(c) for c in witness["side"]],
                "print": claim["side_decimal"],
                "read_from": (
                    f"{LANE_PACKET}/facts/alg-n-{n:03d}.yaml.gz at {LANE_COMMIT}, "
                    "witness.side and scalar"
                ),
            }
        else:
            row = lane[n]
            sides[str(n)] = {
                "kind": "rational",
                "value": str(Fraction(row["exact_side"])),
                "print": row["offered_side"],
                "read_from": (
                    f"{LANE_PACKET}/acquisition/claims.json at {LANE_COMMIT}, "
                    f"results[n = {n}].exact_side"
                ),
            }
    return {
        "schema": "pr574-exact-sides/v1",
        "tool": "devtools.decide_undecided_comparisons extract",
        "note": (
            "PR #574's exact sides at the 17 decidable rows of the 14 October ledger's "
            "Undecided Comparisons. The PR #574 lane's packet is not on main, so the sides "
            "are kept here with the commit and path of each file they were read from, and "
            "the downloaded n = 17 certificate with its digest."
        ),
        "lane": {"branch": LANE_BRANCH, "commit": LANE_COMMIT},
        "pull_request": {"number": 574, "commit": PR_COMMIT},
        "v2_archive": V2_ARCHIVE,
        "files": files,
        "sides": sides,
    }


# --------------------------------------------------------------------------------- main


def _write_or_check(receipt: Json, path: Path, *, check: bool) -> int:
    text = json.dumps(receipt, indent=1, ensure_ascii=False) + "\n"
    if check:
        if not path.is_file() or path.read_text(encoding="utf-8") != text:
            print(f"{_rel(path)} is stale; rerun without --check", file=sys.stderr)
            return 1
        print(f"{_rel(path)}: current")
        return 0
    atomic_write_text(path, text)
    print(f"wrote {_rel(path)}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    extract_parser = commands.add_parser(
        "extract", help="write PR #574's sides from exported files"
    )
    extract_parser.add_argument("--inputs", type=Path, required=True)
    decide_parser = commands.add_parser("decide", help="decide the 17 rows")
    decide_parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "extract":
        return _write_or_check(extract(args.inputs), SIDES, check=False)
    receipt = resolved_receipt(json.loads(SIDES.read_text(encoding="utf-8")))
    for row in receipt["rows"]:
        print(f"n = {row['n']:3d}: {row['relation']:5s} {row['margin']}")
    return _write_or_check(receipt, RESOLVED, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
