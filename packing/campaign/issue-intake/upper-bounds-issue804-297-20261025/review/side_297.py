"""Issue #804's side at 297: the derived fact, its exact checks and route A's agreement.

Hyukdong Kim's comment of 2026-10-25T12:23:57Z on issue 804 (issuecomment-6397593690)
states that the stationary side of T-174's packing at 297 is the only real root of an
irreducible degree-21 integer polynomial ``P297``, prints the polynomial and the root to
100 places, and attaches ``s297-exact-configuration.zip`` under CC0 1.0, giving its SHA-256
and that of its one certificate. The attachment could not be read from the session that
imported it (the proxy refuses user-attachments URLs), so nothing of it is retained or run
here; the comment's text is retained in the packet (``acquisition/comments-804.json``).

- ``derive [--check]`` reads that comment from the packet as data and writes the packet's
  ``facts/s297-polynomial.json`` (the polynomial, highest degree first, and the printed side)
  and ``acquisition/sources.json`` (the attachment's address and the digests the comment
  states, not measured here).
- ``sides [--check]`` is offline. It decides ``P297`` primitive and irreducible over Q twice,
  by SymPy's ``factor_list`` and by ``sqpack.field`` through ``devtools.exact_sides.algebraic``;
  counts its real roots; isolates the root the print names below ``10^-130``; and writes
  ``exact-sides.json`` beside this directory: the root's cut at `PLACES` (the ledger's print)
  and `CLAIM_PLACES` (the register's), its exact order against the case record's verified
  upper bound at 297 (T-174's rational certificate) and Evan Daniel's #639 side there, and
  how far route A's refined side (the packet's ``receipts/solve.json``, from
  ``devtools.build_field_configuration``) lies from the isolated root.

Run from ``packing/``:
``python campaign/issue-intake/upper-bounds-issue804-297-20261025/review/side_297.py sides``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy
import yaml

REPO = Path(__file__).resolve().parents[5]
PACKING = REPO / "packing"
sys.path.insert(0, str(PACKING))

from devtools import exact_sides  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
PACKET = PACKING / "resources/web/hyukdongkim-s297-2026-10-25"
COMMENTS = PACKET / "acquisition/comments-804.json"
SOURCES = PACKET / "acquisition/sources.json"
FACT = PACKET / "facts/s297-polynomial.json"
SOLVE = PACKET / "receipts/solve.json"
SIDES = HERE / "exact-sides.json"
CASE = PACKING / "frontier/n-297.md"
DANIEL = PACKING / "campaign/issue-intake/upper-bounds-20261016/exact-sides.json"
TOOL = "packing/campaign/issue-intake/upper-bounds-issue804-297-20261025/review/side_297.py"

COMMENT_ID = 6397593690
ATTACHMENT = "https://github.com/user-attachments/files/33925868/s297-exact-configuration.zip"
#: The digests the comment states; the attachment was not read, so neither is measured.
ARCHIVE_SHA256 = "e08b5d0a64c5c68eed827ee7e323687929048a4cfea438bb77ef390bdd4147a7"
MEMBER = "n297.minpoly.json"
MEMBER_SHA256 = "e5c340b8af2ff75d01b9b414e32ef19d9c3d07ecce665c8fddad9c5952252826"

N = 297
PLACES = 120
CLAIM_PLACES = 100
WIDTH = Fraction(1, 10**130)
#: The print has 100 places; the root it names lies within this of it.
PRINT_RADIUS = Fraction(1, 10**95)
X = sympy.Symbol("s")


def written(path: Path, document: dict[str, Any], *, check: bool) -> int:
    text = json.dumps(document, indent=1, ensure_ascii=False) + "\n"
    if check:
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            print(f"{path.relative_to(REPO)}: differs from what this program writes")
            return 1
        return 0
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(REPO)}")
    return 0


def comment() -> dict[str, Any]:
    document = json.loads(COMMENTS.read_text(encoding="utf-8"))
    return next(item for item in document["comments"] if int(item["id"]) == COMMENT_ID)


def derive(*, check: bool) -> int:
    """The polynomial and the printed side, read from the comment's text as data."""
    item = comment()
    body = str(item["body"])
    listed = re.search(r"`(\[5132808[^`]*\])`", body)
    printed = re.search(r"S\\\* = (17\.\d+)…", body)
    if listed is None or printed is None:
        sys.exit("the comment does not state the polynomial and side in the expected form")
    coefficients = [int(token) for token in re.findall(r"-?\d+", listed.group(1))]
    if len(coefficients) != 22:
        sys.exit(f"{len(coefficients)} coefficients; the comment states degree 21")
    fact = {
        "format": "issue-804-s297-polynomial-fact-v1",
        "derived_by": TOOL,
        "source": {
            "comment": str(item["html_url"]),
            "created_at": str(item["created_at"]),
            "comments_sha256": hashlib.sha256(COMMENTS.read_bytes()).hexdigest(),
        },
        "note": (
            "The polynomial and printed side as the comment states them, read as text. "
            "The attachment holds the author's exact configuration; it was not read here."
        ),
        "n": N,
        "degree": len(coefficients) - 1,
        "polynomial_high_to_low": [str(c) for c in coefficients],
        "printed_side": printed.group(1),
    }
    sources = {
        "format": "issue-attachment-sources-v1",
        "issue": "https://github.com/jlevy/squares/issues/804",
        "comment": str(item["html_url"]),
        "attachment": {
            "url": ATTACHMENT,
            "bytes": None,
            "sha256": ARCHIVE_SHA256,
            "sha256_stated_by_comment": True,
            "sha256_measured": False,
            "raw_asset_retained": False,
            "licence": "CC0 1.0 (stated by the comment)",
            "not_read": (
                "The importing session's proxy answers user-attachments URLs with 403, so "
                "the archive was neither downloaded nor measured; under CC0 it may be kept "
                "once it is reachable."
            ),
        },
        "members": [
            {
                "path": MEMBER,
                "sha256": MEMBER_SHA256,
                "stated_by_comment": True,
                "retained": False,
            }
        ],
    }
    status = written(FACT, fact, check=check)
    return status | written(SOURCES, sources, check=check)


def value_at(poly: list[int], x: Fraction) -> Fraction:
    total = Fraction(0)
    for c in poly:
        total = total * x + c
    return total


def isolate(poly: list[int], low: Fraction, high: Fraction) -> tuple[Fraction, Fraction]:
    low_positive = value_at(poly, low) > 0
    while high - low >= WIDTH:
        middle = (low + high) / 2
        if (value_at(poly, middle) > 0) == low_positive:
            low = middle
        else:
            high = middle
    return low, high


def cut(low: Fraction, high: Fraction, places: int) -> str:
    scale = 10**places
    floor_low, floor_high = math.floor(low * scale), math.floor(high * scale)
    if floor_low != floor_high:
        sys.exit("the root sits on a cut boundary; narrow it further")
    whole, fraction = divmod(floor_low, scale)
    return f"{whole}.{fraction:0{places}d}"


def magnitude(value: Fraction) -> str:
    return f"{float(value):.4g}"


def case_bound() -> Fraction:
    text = CASE.read_text(encoding="utf-8")
    front = yaml.safe_load(text.split("---", 2)[1])
    return Fraction(str(front["packing"]["verified_upper_bound"]["exact_form"]))


def daniel_side() -> tuple[exact_sides.Side, dict[str, Any]]:
    document = json.loads(DANIEL.read_text(encoding="utf-8"))
    row = next(item for item in document["rows"] if int(item["n"]) == N)
    poly = [int(value) for value in reversed(row["polynomial_low_to_high"])]
    low, high = (Fraction(str(end)) for end in row["interval"])
    return exact_sides.algebraic(poly, (low, high)), row


def route_a(low: Fraction, high: Fraction) -> dict[str, Any] | None:
    if not SOLVE.exists():
        return None
    receipt = json.loads(SOLVE.read_text(encoding="utf-8"))
    side = Fraction(str(receipt["side_digits"]))
    distance = max(abs(side - low), abs(side - high))
    return {
        "receipt": str(SOLVE.relative_to(REPO)),
        "receipt_sha256": hashlib.sha256(SOLVE.read_bytes()).hexdigest(),
        "digits_compared": len(str(receipt["side_digits"]).split(".")[1]),
        "within": magnitude(distance),
    }


def sides(*, check: bool) -> int:
    fact = json.loads(FACT.read_text(encoding="utf-8"))
    poly = [int(c) for c in fact["polynomial_high_to_low"]]
    sympy_poly = sympy.Poly(poly, X, domain=sympy.ZZ)
    content = int(sympy_poly.content())
    _, factors = sympy_poly.factor_list()
    irreducible = (
        content == 1
        and len(factors) == 1
        and factors[0][1] == 1
        and factors[0][0].degree() == sympy_poly.degree()
    )
    printed = Fraction(str(fact["printed_side"]))
    low, high = printed - PRINT_RADIUS, printed + PRINT_RADIUS
    in_print = int(sympy_poly.count_roots(sympy.Rational(low), sympy.Rational(high)))
    if in_print != 1 or value_at(poly, low) * value_at(poly, high) >= 0:
        sys.exit(f"{in_print} roots within 1e-95 of the printed side")
    side = exact_sides.algebraic(poly, (low, high))
    low, high = isolate(poly, low, high)
    house = case_bound()
    order = exact_sides.compare(side, house)
    daniel, daniel_row = daniel_side()
    daniel_low, daniel_high = exact_sides.enclosure(daniel, WIDTH)
    daniel_order = exact_sides.compare(side, daniel)
    row: dict[str, Any] = {
        "n": N,
        "degree": len(poly) - 1,
        "polynomial_high_to_low": [str(c) for c in poly],
        "primitive": content == 1,
        "irreducible_sympy": irreducible,
        "irreducible_sqpack_field": isinstance(side, exact_sides.Algebraic),
        "real_roots": int(sympy_poly.count_roots()),
        "interval": [str(low), str(high)],
        "print": cut(low, high, PLACES),
        "rounding": "cut",
        "claim_cut": cut(low, high, CLAIM_PLACES) + "…",
        "ceiling_40": exact_sides.ceiling(side, 40),
        "form": exact_sides.form(side)
        if isinstance(side, exact_sides.Algebraic)
        else str(side),
        "against_case_verified_upper_bound": {
            "member": (
                "T-174 (E-pingyou-574-exact-feasibility), the verified upper bound at 297"
            ),
            "relation": {-1: "below", 0: "equal", 1: "above"}[order],
            "margin": f"{magnitude(house - high)} to {magnitude(house - low)}"
            if order < 0
            else None,
        },
        "against_daniel_639": {
            "degree": len(daniel_row["polynomial_low_to_high"]) - 1,
            "relation": {-1: "below", 0: "equal", 1: "above"}[daniel_order],
            "margin": f"{magnitude(daniel_low - high)} to {magnitude(daniel_high - low)}"
            if daniel_order < 0
            else None,
        },
        "route_a": route_a(low, high),
    }
    print(
        N,
        row["degree"],
        irreducible,
        row["real_roots"],
        row["against_case_verified_upper_bound"]["relation"],
        row["against_case_verified_upper_bound"]["margin"],
        row["against_daniel_639"]["relation"],
        row["route_a"] and row["route_a"]["within"],
    )
    document = {
        "format": "issue-804-exact-sides-v1",
        "tool": TOOL,
        "fact": str(FACT.relative_to(REPO)),
        "fact_sha256": hashlib.sha256(FACT.read_bytes()).hexdigest(),
        "case": str(CASE.relative_to(REPO)),
        "places": PLACES,
        "claim_places": CLAIM_PLACES,
        "rows": [row],
    }
    return written(SIDES, document, check=check)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("command", choices=("derive", "sides"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    mp.mp.dps = 50
    if args.command == "derive":
        return derive(check=args.check)
    return sides(check=args.check)


if __name__ == "__main__":
    sys.exit(main())
