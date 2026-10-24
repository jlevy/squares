"""Re-derive issue #763's claims from the indexes its packet retains (think-ptkk).

Francisco Couzo's issue #763 (23 October 2026, 23:35:51Z) asks to register "the 436
improved upper bounds below: 203 at or below 1024 and 233 above 1024" from
franciscouzo/square-packing at ``964ee2bd``, but its body ends at the legend of the
``refines`` column: it carries no table. The ``couzo-issue763-2026-10-23`` packet retains
the two indexes the selection reads, ``certified_bounds.json`` (each count's finite
certificate or construction recipe, its exact bound and its credit) and
``public_bounds.json`` (the author's reviewed comparison at each count), and this module
re-derives the claims from them by the rule the source's README states for its own table:

- **a claim** is a count whose certified entry is a certificate or a construction
  credited to Couzo (the credit begins ``Francisco Couzo`` or ``franciscouzo``); the index
  also holds Kaggle notebook packings by other authors, which the issue says "are not part
  of this request";
- **the comparison** is the count's public bound, except where that is the competition's
  staff per-puzzle leaderboard, whose packings "are not public, so they are not used as
  comparisons": there the entry's ``superseded_review``, the reviewed public bound it
  replaced, is the comparison;
- **against Couzo's own comparison** the certified side, rounded up at 12 places, must be
  strictly below the comparison rounded up at 12 places ("Updates to our own packings
  have no minimum gain"); **against another author's** it must be more than ``1e-10``
  below the comparison's exact value ("The 1e-10 reporting tolerance applies only to
  claims of new improvements over another author's public bound").

Each comparison is decided exactly: a bound is a rational or ``r + s*sqrt(2)``, and every
sign is decided with integers (`sign_sqrt2`). The rule as the issue's own sentence states
it, the 12-place print alone at every comparison, selects every claim and 15 more counts
(``unrequested``): 204 in the corpus and 14 at 335 to 998, which by the runbook are an
import of their own, the publication of the index that holds them.

The receipt, ``receipts/claim-map.json`` in the packet, keeps each claim's kind
(certificate, deletion or construction recipe), its certificate path and SHA-256 as the
index states them, its exact bound and 12-place print, the recipe of a construction, its
credit and the issue's ``refines`` legend letter read from that credit, and its comparison
with the margin. The issue's own counts are this module's controls (`CONTROLS`): 436 rows,
203 at or below 1024 and 233 above, 196 certificate rows and deletions at exactly 683,
1646 and 1727. Two of the issue's counts are not reproduced and are reported, not forced:
its legend counts 345 rows that refine another author's packing, the credits give 351 (2
of them from a notebook the legend does not name), and its leaderboard column counts 180
counts, where the leaderboard's side is below 182 of the claims at n <= 1000, the counts
the competition scores.

It runs no code of the source and decides nothing about the packings: whether a claim is
recorded is the report-order walk's (``campaign/issue-intake/upper-bounds-issue763-20261024``).

From ``packing/``, with the project interpreter::

    python -m devtools.couzo_763_claims derive [--write]
    python -m devtools.couzo_763_claims check
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from collections.abc import Mapping
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, NamedTuple

from strif import atomic_output_file

from devtools import acquire_source
from devtools import evand_exact_certificates as legacy
from devtools.retained_data import read_retained_text
from sqpack.retained_json import dumps as retained_dumps

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/couzo-issue763-2026-10-23"
ARCHIVE = PACKET / "source"
RECEIPT = PACKET / "receipts/claim-map.json"
FORMAT = "couzo-763-claim-map-v1"
ISSUE = "https://github.com/jlevy/squares/issues/763"
PIN = "964ee2bdf301d0c8912d956d4010f478dcbbd5ea"
CERTIFIED = "certified_bounds.json"
PUBLIC = "public_bounds.json"
#: The case corpus is ``n <= 324``; the record decides rows to ``LIMIT`` (D1, think-llit).
HORIZON, LIMIT = 324, 1024
PLACES = 12
#: Another author's comparison must be beaten by more than this (the source README).
TOLERANCE = Fraction(1, 10**10)
#: The credits that name Couzo as the holder of a certified entry or a comparison.
OWN = ("Francisco Couzo", "franciscouzo")
#: The competition's staff per-puzzle leaderboard, whose packings are not public; the
#: index carries its sides to larger counts by L-borders, but it scores n = 1 to 1000.
LEADERBOARD = "https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard"
COMPETITION = 1000
#: The issue's legend of the ``refines`` column, as each letter's packing is credited.
LEGEND = {
    "A": 'Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11',
    "B": 'Kirill Tymchishin (kirilltym), Kaggle "CPU Alternating Reclosure" v3',
    "C": 'Kirill Tymchishin (kirilltym), Kaggle "CPU/GPU/MPS EDA+Seam LP" v4',
    "D": "Mykhailo Polkovskyi (Mishapolk)",
    "E": "Darius Muglich",
}
#: The counts the issue states, which the derivation must reproduce.
CONTROLS = {
    "rows": 436,
    "at_or_below_limit": 203,
    "above_limit": 233,
    "certificate_rows": 196,
    "deletions": [683, 1646, 1727],
}
#: The issue's counts the derivation does not reproduce: reported beside it, not forced.
STATED_ONLY = {"refines_another_author": 345, "leaderboard_smaller": 180}
_REFINES = re.compile(r"refines the packing of ([^;]+)")


class ClaimError(ValueError):
    """Refuse an index entry or a receipt that does not hold."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ClaimError(message)


# --------------------------------------------------------------------------- exact numbers


def _sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def sign_sqrt2(rational: Fraction, root: Fraction) -> int:
    """The sign of ``rational + root * sqrt(2)``, decided with integers."""
    if root == 0 or rational == 0:
        return _sign(rational) or _sign(root)
    if _sign(rational) == _sign(root):
        return _sign(rational)
    # Opposite signs: the larger magnitude wins, and a*a == 2*b*b has no rational solution.
    return _sign(rational) if rational * rational > 2 * root * root else _sign(root)


class Bound(NamedTuple):
    """A side ``r + s*sqrt(2)``, as the source's ``exact_bound`` states it."""

    rational: Fraction
    root: Fraction = Fraction(0)

    def above(self, side: Fraction, by: Fraction = Fraction(0)) -> bool:
        """Whether ``side + by`` is strictly below this bound."""
        return sign_sqrt2(self.rational - side - by, self.root) > 0

    def below(self, side: Fraction) -> bool:
        """Whether this bound is strictly below ``side``."""
        return sign_sqrt2(self.rational - side, self.root) < 0

    def ceiling(self, places: int = PLACES) -> str:
        """This bound rounded up at ``places`` decimal places, decided exactly."""
        scale = 10**places
        rational, root = self.rational * scale, self.root * scale
        with localcontext() as context:
            context.prec = 80
            guess = math.ceil(
                Decimal(rational.numerator) / Decimal(rational.denominator)
                + Decimal(root.numerator) / Decimal(root.denominator) * Decimal(2).sqrt()
            )
        # ``guess`` is the ceiling when x <= guess and x > guess - 1; step until both hold.
        while sign_sqrt2(rational - guess, root) > 0:
            guess += 1
        while sign_sqrt2(rational - (guess - 1), root) <= 0:
            guess -= 1
        return legacy.ceiling_decimal(Fraction(guess, scale), places)

    def minus(self, side: Fraction) -> str:
        """This bound less ``side``, to three significant digits."""
        with localcontext() as context:
            context.prec = 60
            difference = (
                Decimal((self.rational - side).numerator)
                / Decimal((self.rational - side).denominator)
                + Decimal(self.root.numerator)
                / Decimal(self.root.denominator)
                * Decimal(2).sqrt()
            )
        return f"{difference:.2e}"

    def literal(self) -> str:
        """``r`` or ``r + s*sqrt(2)``, each a rational literal."""
        if self.root == 0:
            return legacy.literal(self.rational)
        return f"{legacy.literal(self.rational)} + {legacy.literal(self.root)}*sqrt(2)"


def bound_of(entry: Mapping[str, Any]) -> Bound:
    """A comparison's exact side: its ``exact_bound`` where it states one, else its
    ``bound``, which must then be a rational."""
    exact = entry.get("exact_bound")
    if isinstance(exact, Mapping):
        return Bound(Fraction(str(exact["rational"])), Fraction(str(exact["sqrt2"])))
    return Bound(Fraction(str(entry["bound"])))


# --------------------------------------------------------------------------- the rule


def read_indexes(archive: Path = ARCHIVE) -> tuple[dict[str, Any], dict[str, Any]]:
    """The certified and public indexes' entries, read from the packet's retained copies,
    which ``acquire_source --check`` binds to the pin."""
    problems = acquire_source.check(PACKET, REPO) if archive == ARCHIVE else []
    _require(not problems, "the packet's custody: " + "; ".join(problems))
    certified = json.loads(read_retained_text(archive / CERTIFIED))["entries"]
    public = json.loads(read_retained_text(archive / PUBLIC))["entries"]
    return certified, public


def is_own(credit: str) -> bool:
    """Whether a credit names Couzo as its holder."""
    return credit.startswith(OWN)


def comparison_of(public: Mapping[str, Any]) -> tuple[Mapping[str, Any], bool]:
    """A count's comparison, and whether it replaces the per-puzzle leaderboard."""
    if public.get("source") == LEADERBOARD:
        review = public.get("superseded_review")
        _require(isinstance(review, Mapping), f"{public}: a leaderboard bound with no review")
        assert isinstance(review, Mapping)
        return review, True
    return public, False


def refines(credit: str) -> str | None:
    """The issue's legend letter of the packing a credit says it refines, the packing's
    credit where the legend names none, or None for a credit that refines no other."""
    match = _REFINES.search(credit)
    if match is None:
        return None
    named = match[1].strip()
    return next(
        (letter for letter, packing in LEGEND.items() if named.startswith(packing)), named
    )


def kind_of(entry: Mapping[str, Any]) -> str:
    """``certificate``, ``deletion`` (a certificate less squares) or ``construction``."""
    if entry["kind"] == "construction":
        return "construction"
    _require(entry["kind"] == "certificate", f"{entry['n']}: an entry of kind {entry['kind']}")
    return "deletion" if int(entry["deleted_squares"]) else "certificate"


def row(n: int, entry: Mapping[str, Any], public: Mapping[str, Any]) -> dict[str, Any]:
    """One count's certified entry and its comparison, as the receipt keeps them."""
    side = Fraction(str(entry["bound"]))
    comparison, replaced = comparison_of(public)
    bound = bound_of(comparison)
    found: dict[str, Any] = {
        "n": n,
        "kind": kind_of(entry),
        "certificate": entry["certificate"],
        "certificate_sha256": entry["certificate_sha256"],
        "source_n": int(entry["source_n"]),
        "deleted_squares": int(entry["deleted_squares"]),
        "exact": legacy.literal(side),
        "ceiling_12": legacy.ceiling_decimal(side, PLACES),
        "index_print": entry.get("rounded_up", ""),
        "credit": entry["credit"],
        "refines": refines(str(entry["credit"])),
        "comparison": {
            "bound": bound.literal(),
            "ceiling_12": bound.ceiling(),
            "credit": comparison.get("credit", ""),
            "source": comparison.get("source", ""),
            "own": is_own(str(comparison.get("credit", ""))),
            "replaces_leaderboard": replaced,
        },
        "margin": bound.minus(side),
    }
    if "construction" in entry:
        recipe = entry["construction"]
        found["construction"] = {
            key: recipe[key]
            for key in ("kind", "source_n", "tiles_per_side", "layers", "capacity")
        }
    if public.get("source") == LEADERBOARD:
        found["leaderboard"] = {
            "bound": bound_of(public).literal(),
            "team": (public.get("origin") or {}).get("team", ""),
            "below_side": bound_of(public).below(side),
        }
    return found


def selected(item: Mapping[str, Any]) -> bool:
    """The README's rule: below the 12-place print of Couzo's own comparison, more than
    ``TOLERANCE`` below another author's."""
    side = Fraction(str(item["exact"]))
    comparison = item["comparison"]
    if comparison["own"]:
        return Fraction(item["ceiling_12"]) < Fraction(comparison["ceiling_12"])
    return _bound_literal(comparison["bound"]).above(side, TOLERANCE)


def stated(item: Mapping[str, Any]) -> bool:
    """The rule as the issue's sentence states it: the 12-place print alone."""
    return Fraction(item["ceiling_12"]) < Fraction(item["comparison"]["ceiling_12"])


def _bound_literal(text: str) -> Bound:
    rational, _, root = text.partition(" + ")
    return Bound(Fraction(rational), Fraction(root.removesuffix("*sqrt(2)") or "0"))


def claim_map(certified: Mapping[str, Any], public: Mapping[str, Any]) -> dict[str, Any]:
    """The issue's claims and the index's unrequested rows (`selected`, `stated`)."""
    claims: list[dict[str, Any]] = []
    unrequested: list[dict[str, Any]] = []
    for key in sorted(certified, key=int):
        entry = certified[key]
        if entry.get("kind") not in ("certificate", "construction"):
            continue
        if not is_own(str(entry["credit"])):
            continue
        n = int(key)
        _require(int(entry["n"]) == n, f"{key}: the entry names n={entry['n']}")
        item = row(n, entry, public[key])
        if selected(item):
            claims.append(item)
        elif stated(item):
            unrequested.append(item)
    return {
        "format": FORMAT,
        "issue": ISSUE,
        "source_commit": PIN,
        "indexes": [CERTIFIED, PUBLIC],
        "program": "packing/devtools/couzo_763_claims.py",
        "summary": summary(claims, unrequested),
        "claims": claims,
        "unrequested": unrequested,
    }


def summary(claims: list[dict[str, Any]], unrequested: list[dict[str, Any]]) -> dict[str, Any]:
    """The counts the issue states (`CONTROLS`) and the ones it states that the index does
    not give (`STATED_ONLY`), as the derivation finds them."""
    kinds = Counter(item["kind"] for item in claims)
    letters = Counter(
        item["refines"] if item["refines"] in LEGEND else "other" if item["refines"] else "own"
        for item in claims
    )
    return {
        "rows": len(claims),
        "at_or_below_limit": sum(1 for item in claims if item["n"] <= LIMIT),
        "above_limit": sum(1 for item in claims if item["n"] > LIMIT),
        "in_corpus": [item["n"] for item in claims if item["n"] <= HORIZON],
        "certificate_rows": kinds["certificate"] + kinds["deletion"],
        "kinds": dict(sorted(kinds.items())),
        "deletions": [item["n"] for item in claims if item["deleted_squares"]],
        "distinct_certificates": len(
            {item["certificate"] for item in claims if item["kind"] != "construction"}
        ),
        "refines": dict(sorted(letters.items())),
        "refines_another_author": sum(
            count for letter, count in letters.items() if letter != "own"
        ),
        "leaderboard_smaller": sum(
            1
            for item in claims
            if item["n"] <= COMPETITION and (item.get("leaderboard") or {}).get("below_side")
        ),
        "issue_states": dict(STATED_ONLY),
        "unrequested": [item["n"] for item in unrequested],
    }


def control_problems(record: Mapping[str, Any]) -> list[str]:
    """Where the derivation does not give a count the issue states (`CONTROLS`)."""
    found = record["summary"]
    return [
        f"the derivation gives {key} = {found[key]}, the issue {value}"
        for key, value in CONTROLS.items()
        if found[key] != value
    ]


def derive(archive: Path = ARCHIVE) -> dict[str, Any]:
    """The claim map from the retained indexes, refused unless it gives the issue's counts."""
    record = claim_map(*read_indexes(archive))
    problems = control_problems(record)
    _require(not problems, "; ".join(problems))
    return record


def check() -> list[str]:
    """Problems with the receipt; empty when a fresh derivation gives it exactly."""
    try:
        fresh = derive()
    except ClaimError as error:
        return [str(error)]
    if not RECEIPT.is_file():
        return [f"{RECEIPT.relative_to(REPO)}: missing"]
    kept = json.loads(RECEIPT.read_text(encoding="utf-8"))
    return [] if kept == fresh else [f"{RECEIPT.relative_to(REPO)}: differs from its rebuild"]


def write(record: Mapping[str, Any]) -> None:
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(RECEIPT) as temporary:
        Path(temporary).write_text(retained_dumps(record, sort_keys=True), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("derive")
    run.add_argument("--write", action="store_true")
    commands.add_parser("check")
    args = parser.parse_args(argv)
    if args.command == "check":
        problems = check()
        for problem in problems:
            print(problem)
        print("FAILED" if problems else "OK: the claim map is a fresh derivation")
        return 1 if problems else 0
    record = derive()
    if args.write:
        write(record)
    print(json.dumps(record["summary"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
