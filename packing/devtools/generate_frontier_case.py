#!/usr/bin/env python3
# ruff: noqa: RUF001 -- this module writes the register's own prose, and its typography
# is the corpus's: curly apostrophes, em dashes, ceiling and root brackets, the
# double-struck rationals, and the U+2212 minus in the display formula. A generated
# body has to match a hand-written one byte for byte.
"""Draft one `frontier/n-NNN.md` case record from the sources the register already trusts.

The first hundred cases were written by hand, one at a time, over several sessions. The
range `101..324` is 224 more of them, and the facts that vary between two neighbouring
cases are few: the catalogue's printed side, its credit line, and which of two rules the
lower bound comes from. Everything else -- the evidence ids, the resource block, the
Nagamochi note, the shape of the prose -- is the same sentence retyped, which is exactly
the kind of work that produces a transcription slip nobody finds. So it is generated,
from two inputs and a fixed set of rules, and a golden test regenerates five of the
hand-written records to show that the rules are the ones the corpus already follows.

**The two inputs.**

1. `atlas/prospective/source-availability-101-324.json`, which says for each `n` whether
   the best known packing is the trivial grid (`exact-generated-geometry`, carrying the
   grid side) or a catalogue drawing (`remote-svg-geometry`). That file's `source_key`
   names where the *geometry* would be fetched from, which is not the same question as
   where the *bound* is reported: four cases in range draw their SVG from the UnitSquare
   release, and the catalogue still prints its own side for each of them. The bound
   provenance here is always the catalogue.
2. The catalogue transcription, read through `sqpack.kingbird_catalogue.parse_catalogue`.
   That module is imported dynamically, and only when a catalogue case is generated, so
   the grid half of the range and every test in this file run without it.

**The bound rules**, from
`docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md`:

- `reported_upper_bound` is the catalogue's printed decimal, transcribed and not
  endorsed, under `E-kingbird-upper-register`; for a rule-generated grid case it is the
  integer side under `construction_method: trivial-grid`.
- `verified_upper_bound` is `ceil(sqrt(n))` under `E-basic-grid-upper`: a ceiling this
  repository can certify, never a reading of `s(n)`.
- both lower bounds are Nagamochi's closed form under `E-nagamochi-lower`, except that a
  perfect square reports the area bound under `E-basic-area-lower`, which is what the
  hand-written perfect squares do.
- `status` is `proved` only where the verified lower bound meets the reported upper
  bound exactly. In `101..324` that is the 24 cases `k^2`, `k^2 - 1` and `k^2 - 2` for
  `k = 11..18`, and nothing else.
- `rigidity` is `null`. The field means "not assessed", never "the packing can move";
  `devtools/screen_translation_escape.py` and `devtools/assess_frontier_rigidity.py`
  write it later in the promotion path.

**What this tool cannot know**, and does not guess:

- `construction_method` and `analytically_optimized` live in the catalogue's *credit
  line*, which the structured `CatalogueEntry` does not carry. They default to `unknown`
  and `null` and are set by the W2 transcription review, or passed in by a caller that
  has read the line. A generated record that still says `unknown` has not been reviewed.
- `source_reviewed` and `retrieved_date` are dates, supplied by the caller. `--check`
  reads them back out of the record being checked so that a regeneration months later
  still diffs to nothing.
- `priority_notes`, `conflicts` and any case-specific evidence are editorial and stay
  empty here.

The record it writes is a draft. It is complete and it validates, and it is not a
substitute for the review that follows it.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.generate_frontier_case \\
        --n 101
    uv run --frozen --all-extras --group dev python -m devtools.generate_frontier_case \\
        --range 101 200 --out /tmp/draft
    uv run --frozen --all-extras --group dev python -m devtools.generate_frontier_case \\
        --range 101 324 --check
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import importlib
import json
import math
import tempfile
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Context, Decimal, localcontext
from pathlib import Path
from typing import Any, Protocol

import yaml
from strif import atomic_output_file

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
AVAILABILITY = ROOT / "atlas" / "prospective" / "source-availability-101-324.json"

#: `n <= 100` is hand-authored. The generator refuses to write into the register there,
#: and the golden test is the one caller that generates those cases at all -- into a
#: temporary directory, to compare against what a person wrote.
HAND_AUTHORED_MAX = 100

#: Where the catalogue's own completeness statement stops. Past it the catalogue pictures
#: isolated cases and claims nothing about the ones it does not picture, so the grid rule
#: below has no source behind it and this tool will not apply it.
CATALOGUE_COMPLETENESS_MAX = 324

GRID_CLASSIFICATION = "exact-generated-geometry"
CATALOGUE_CLASSIFICATION = "remote-svg-geometry"

KINGBIRD_EVIDENCE = "E-kingbird-upper-register"
GRID_UPPER_EVIDENCE = "E-basic-grid-upper"
AREA_LOWER_EVIDENCE = "E-basic-area-lower"
NAGAMOCHI_EVIDENCE = "E-nagamochi-lower"

NAGAMOCHI_NOTE = (
    "General closed form: s(N) >= min(ceil(sqrt(N)), sqrt(N - 2*floor(sqrt(N)) + 1) + 1)."
)
UPPER_GAP_BLOCKER = "No formal certificate currently supports the tighter reported upper bound."

#: The three resources every generated case cites. A perfect square drops the middle one:
#: its lower bound is the area bound, and the hand-written perfect squares list only the
#: two sources they actually lean on.
KINGBIRD_RESOURCE: dict[str, Any] = {
    "key": "[Kingbird]",
    "role": "record-catalogue",
    "local": "web/kingbird-squares-in-squares",
    "url": "https://kingbird.myphotos.cc/packing/squares_in_squares.html",
    "retrieved": True,
}
NAGAMOCHI_RESOURCE: dict[str, Any] = {
    "key": "[Nagamochi 2005]",
    "role": "lower-bound-proof",
    "local": "papers/nagamochi-2005-packing-unit-squares-in-a-rectangle",
    "url": "https://www.combinatorics.org/ojs/index.php/eljc/article/view/v12i1r37",
    "retrieved": True,
}
FRIEDMAN_RESOURCE: dict[str, Any] = {
    "key": "[Friedman DS7]",
    "role": "survey",
    "local": "papers/friedman-ds7-packing-unit-squares-in-squares",
    "url": "https://erich-friedman.github.io/papers/squares/squares.html",
    "retrieved": True,
}

#: Significant figures each lower-bound lane carries. Both are the corpus's own choice,
#: re-measured against all hundred records rather than assumed: `reported_lower_bound`
#: prints 13 and `verified_lower_bound` 12, each with trailing zeros dropped, which is
#: why `n = 50` reads 7.082762530298 above and 7.0827625303 below.
REPORTED_SIGNIFICANT = 13
VERIFIED_SIGNIFICANT = 12

#: Enough digits that the square root is exact well past either lane's last place.
BOUND_PRECISION = 60

COMMON_DOC_FOOTER = (
    "<!-- This document follows common-doc-guidelines.md.\n"
    "See github.com/jlevy/practical-prose and review guidelines before editing.\n"
    "-->\n"
)

NAGAMOCHI_DISPLAY = "s(N) ≥ min{ ⌈√N⌉,  √(N − 2⌊√N⌋ + 1) + 1 }"

#: The closing sentence of "The lower bound", in the two forms the corpus uses.
#:
#: The first quotes a corpus-wide count, and `devtools/check_nagamochi_bounds.py` owns
#: that count: it re-derives "N of the M open cases" from the case records and fails if
#: any body disagrees. Writing it into 200 new records would put a figure about the first
#: hundred into files that are not part of what it counts, and would move the count on
#: the day the new cases land. So generated records past the hand-authored range say the
#: same thing without the arithmetic, and the counted form is emitted only where the
#: corpus that owns it already carries it.
NAGAMOCHI_DEFAULT_COUNTED = (
    "This is the default across almost the whole open frontier — 58 of the 65 open cases "
    "at `n ≤ 100` are governed by it, and outside this repository’s own displacements it "
    "has not been improved since 2005."
)
NAGAMOCHI_DEFAULT_UNCOUNTED = (
    "This is the default across almost the whole open frontier, and outside this "
    "repository’s own displacements it has not been improved since 2005."
)

#: `construction_method` enum value -> the phrase the corpus's prose uses for it. The
#: first four are read off the hand-written bodies; the rest follow their pattern and are
#: unused until a catalogue credit line is transcribed into one of them.
CONSTRUCTION_PHRASES = {
    "trivial-grid": "the trivial grid",
    "hand-construction": "a hand construction",
    "diagonal-strip": "a diagonal-strip construction",
    "pattern-family": "a pattern family",
    "extension": "extension of a smaller record",
    "composition": "a composition of smaller packings",
    "simulated-annealing": "simulated annealing",
    "inflation-billiard": "an inflation-billiard search",
    "unknown": "an unrecorded method",
}


class GenerationError(Exception):
    """A case cannot be drafted from the inputs given."""


# --------------------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SourceAvailability:
    """One row of the prospective source map: where this `n`'s best known packing lives."""

    n: int
    classification: str
    source_key: str
    trivial_grid_side: int | None

    @property
    def is_grid(self) -> bool:
        return self.classification == GRID_CLASSIFICATION


@dataclass(frozen=True, slots=True)
class CatalogueFacts:
    """Everything a case record takes from the record catalogue, for one `n`.

    The first nine fields come straight off `sqpack.kingbird_catalogue.CatalogueEntry`.
    The last three do not exist there: they are read from the catalogue's credit line,
    which the structured entry does not carry, so they default to the values that say
    "nobody has read the line yet" and a reviewer sets them.
    """

    n: int
    side_decimal: str
    exact_form: str | None = None
    algebraic_degree: int | None = None
    minimal_polynomial: str | None = None
    found_by: tuple[str, ...] = ()
    found_year: int | None = None
    catalogue_rigid: str = "not-stated"
    catalogue_pictured: bool = True
    construction_method: str = "unknown"
    analytically_optimized: bool | None = None
    improved_by: tuple[str, ...] = ()


class CatalogueEntryLike(Protocol):
    """The half of `sqpack.kingbird_catalogue.CatalogueEntry` this tool reads.

    Declared structurally so that this module neither imports that one at module scope
    nor duplicates its definition: the catalogue parser is a separate piece of work, and
    a case can be drafted from facts handed in directly, which is what the tests do.
    """

    @property
    def n(self) -> int: ...
    @property
    def side_decimal(self) -> str: ...
    @property
    def exact_form(self) -> str | None: ...
    @property
    def algebraic_degree(self) -> int | None: ...
    @property
    def minimal_polynomial(self) -> str | None: ...
    @property
    def found_by(self) -> Sequence[str]: ...
    @property
    def found_year(self) -> int | None: ...
    @property
    def catalogue_rigid(self) -> str: ...
    @property
    def catalogue_pictured(self) -> bool: ...


def facts_from_catalogue_entry(
    entry: CatalogueEntryLike, *, n: int | None = None
) -> CatalogueFacts:
    """Adapt one parsed catalogue entry to the facts a case record needs.

    `n` overrides the entry's own, and the caller normally passes it. A catalogue row can
    cover two sizes -- "119, 120" is one drawing and one printed side -- and the parser
    keys such an entry under both while `entry.n` names only one of them.
    """
    return CatalogueFacts(
        n=entry.n if n is None else n,
        side_decimal=entry.side_decimal,
        exact_form=entry.exact_form,
        algebraic_degree=entry.algebraic_degree,
        minimal_polynomial=entry.minimal_polynomial,
        found_by=tuple(entry.found_by),
        found_year=entry.found_year,
        catalogue_rigid=entry.catalogue_rigid or "not-stated",
        catalogue_pictured=entry.catalogue_pictured,
    )


def load_availability(path: Path | None = None) -> dict[int, SourceAvailability]:
    """Read the prospective source map into one row per `n`."""
    source = path or AVAILABILITY
    document = json.loads(source.read_text(encoding="utf-8"))
    rows: dict[int, SourceAvailability] = {}
    for entry in document["availability"]["entries"]:
        n = int(entry["n"])
        rows[n] = SourceAvailability(
            n=n,
            classification=str(entry["classification"]),
            source_key=str(entry["source_key"]),
            trivial_grid_side=(
                int(entry["trivial_grid_side"])
                if entry.get("trivial_grid_side") is not None
                else None
            ),
        )
    return rows


def load_catalogue(path: Path | None = None) -> dict[int, CatalogueFacts]:
    """Parse the retained catalogue transcription into per-`n` facts.

    The import is dynamic and late on purpose. `sqpack.kingbird_catalogue` is written
    against the same plan as this module and lands beside it; nothing here needs it until
    a catalogue-sourced case is actually drafted, and no test in this file needs it at
    all, because facts can be handed in directly.
    """
    try:
        module = importlib.import_module("sqpack.kingbird_catalogue")
    except ModuleNotFoundError as error:
        raise GenerationError(
            "the catalogue parser sqpack.kingbird_catalogue is not available, so only "
            "grid cases can be drafted"
        ) from error
    parsed: Mapping[int, CatalogueEntryLike] = module.parse_catalogue(path)
    return {n: facts_from_catalogue_entry(entry, n=n) for n, entry in parsed.items()}


# --------------------------------------------------------------------------------------
# Bounds
# --------------------------------------------------------------------------------------


def grid_ceiling(n: int) -> int:
    """`ceil(sqrt(n))`, the side of the trivial no-tilt grid."""
    root = math.isqrt(n)
    return root if root * root == n else root + 1


def is_perfect_square(n: int) -> bool:
    return math.isqrt(n) ** 2 == n


def is_nagamochi_exact(n: int) -> bool:
    """Whether `n` is one of Nagamochi's exact cases `m^2`, `m^2 - 1`, `m^2 - 2`."""
    side = grid_ceiling(n)
    return side * side - n <= 2


def nagamochi_exact_form(n: int) -> str:
    """The exact identity of Nagamochi's bound for `n`, spelled as the corpus spells it."""
    if is_nagamochi_exact(n):
        return str(grid_ceiling(n))
    return f"sqrt({n} - 2*floor(sqrt({n})) + 1) + 1"


def _strip_trailing_zeros(text: str) -> str:
    if "." not in text:
        return text
    return text.rstrip("0").rstrip(".")


def nagamochi_value(n: int, significant: int) -> str:
    """Nagamochi's bound for `n`, printed to `significant` figures as the register does."""
    if is_nagamochi_exact(n):
        return str(grid_ceiling(n))
    with localcontext() as context:
        context.prec = BOUND_PRECISION
        root = math.isqrt(n)
        value = Decimal(n - 2 * root + 1).sqrt() + 1
    return _strip_trailing_zeros(format(Context(prec=significant).plus(value), "f"))


def _quantized(value: Decimal, places: int, rounding: str) -> Decimal:
    with localcontext() as context:
        context.prec = BOUND_PRECISION
        return value.quantize(Decimal(1).scaleb(-places), rounding=rounding)


def display_upper(value: str, places: int = 8) -> str:
    """An upper bound at `places`, rounded up so the inequality the prose writes stays true."""
    return _strip_trailing_zeros(format(_quantized(Decimal(value), places, ROUND_CEILING), "f"))


def display_lower(value: str, places: int = 6) -> str:
    """A lower bound at `places`, rounded down for the same reason."""
    return format(_quantized(Decimal(value), places, ROUND_FLOOR), "f")


def display_gap(upper: str, lower: str, places: int = 4) -> str:
    """The width between two bounds, to nearest, with trailing zeros dropped when safe.

    `check_case_prose` re-derives a quoted gap at whatever precision the prose wrote it
    to, so dropping a trailing zero changes which precision is checked. It is dropped
    only when the shorter form still renders the same width.
    """
    with localcontext() as context:
        context.prec = BOUND_PRECISION
        difference = Decimal(upper) - Decimal(lower)
    full = format(_quantized(difference, places, ROUND_HALF_UP), "f")
    stripped = _strip_trailing_zeros(full)
    shorter = len(stripped.partition(".")[2])
    if Decimal(stripped) == _quantized(difference, shorter, ROUND_HALF_UP):
        return stripped
    return full


def _exact_difference(larger: str, smaller: str) -> str:
    """`larger - smaller` at the register's own 28 digits.

    Pinned rather than inherited: `decimal`'s context is process-global and
    `sqpack.field` raises it while refining an enclosure, so a generator running after
    one of those would otherwise print a longer rendering of the same number than
    `tests/test_verified_upper_bound_contract.py` recomputes.
    """
    with localcontext() as context:
        context.prec = 28
        return str(Decimal(larger) - Decimal(smaller))


# --------------------------------------------------------------------------------------
# The record
# --------------------------------------------------------------------------------------


def _witness_id(n: int) -> str:
    return f"W-known-best-n{n:03d}"


def _join_names(names: Sequence[str]) -> str:
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return f"{', '.join(names[:-1])} and {names[-1]}"


def build_payload(
    n: int,
    *,
    source: SourceAvailability,
    facts: CatalogueFacts | None,
    review_date: str,
    retrieved_date: str,
) -> dict[str, Any]:
    """The `packing` payload for one case, under `packing.squares:SquarePackingCase/v2`."""
    if n < 1:
        raise GenerationError(f"n must be positive, got {n}")
    side = grid_ceiling(n)
    if source.is_grid:
        if source.trivial_grid_side is not None and source.trivial_grid_side != side:
            raise GenerationError(
                f"n={n}: source map says the grid side is {source.trivial_grid_side}, "
                f"but ceil(sqrt({n})) is {side}"
            )
        reported_upper = _grid_reported_upper(n, side, retrieved_date)
    else:
        if facts is None:
            raise GenerationError(f"n={n}: a catalogue case needs catalogue facts")
        if facts.n != n:
            raise GenerationError(f"n={n}: catalogue facts are for n={facts.n}")
        reported_upper = _catalogue_reported_upper(n, facts, retrieved_date)

    verified_upper = {
        "value": str(side),
        "exact_form": str(side),
        "evidence": [GRID_UPPER_EVIDENCE],
    }
    verified_lower = {
        "value": nagamochi_value(n, VERIFIED_SIGNIFICANT),
        "exact_form": nagamochi_exact_form(n),
        "evidence": [NAGAMOCHI_EVIDENCE],
    }
    reported_lower = _reported_lower(n, side)

    reported_value = str(reported_upper["value"])
    with localcontext() as context:
        context.prec = BOUND_PRECISION
        proved = Decimal(reported_value) == Decimal(str(verified_lower["value"]))
        trails = Decimal(str(verified_upper["value"])) > Decimal(reported_value)
    status = "proved" if proved else "open"

    if proved:
        conjectured: str | None = None
    elif source.is_grid:
        # The grid case's best known side is an integer and the catalogue does not
        # picture it, so the conjecture on record is that the optimum is that integer --
        # which is what the hand-written grid cases say, in that one word.
        conjectured = "integer"
    else:
        conjectured = reported_value

    rollup = (
        [KINGBIRD_EVIDENCE, AREA_LOWER_EVIDENCE, GRID_UPPER_EVIDENCE, NAGAMOCHI_EVIDENCE]
        if reported_lower["kind"] == "perfect-square"
        else [KINGBIRD_EVIDENCE, NAGAMOCHI_EVIDENCE, GRID_UPPER_EVIDENCE]
    )
    blockers: list[dict[str, Any]] = []
    if trails:
        # The blocker's evidence is the *same list object* the reported upper bound
        # carries, which is how the hand-written records read and how they serialise
        # (one YAML anchor, one alias). `assurance.check_case_semantics` requires the
        # two to intersect; sharing the object makes that structural.
        blockers.append(
            {
                "kind": "mathematics",
                "detail": UPPER_GAP_BLOCKER,
                "evidence": reported_upper["evidence"],
            }
        )
    resources = [KINGBIRD_RESOURCE, FRIEDMAN_RESOURCE]
    if reported_lower["kind"] != "perfect-square":
        resources = [KINGBIRD_RESOURCE, NAGAMOCHI_RESOURCE, FRIEDMAN_RESOURCE]

    return {
        "n": n,
        "reported_status": status,
        "status": status,
        "source_reviewed": review_date,
        "reported_upper_bound": reported_upper,
        "verified_upper_bound": verified_upper,
        "reported_lower_bound": reported_lower,
        "verified_lower_bound": verified_lower,
        # Not assessed. The escape screen and the rigidity assessment write this field
        # later in the promotion path; `null` here says nobody has looked, and never
        # that the packing can move.
        "rigidity": None,
        "conjectured_optimum": conjectured,
        "priority_notes": [],
        "evidence": rollup,
        "conflicts": [],
        "blockers": blockers,
        "resources": [dict(resource) for resource in resources],
    }


def _grid_reported_upper(n: int, side: int, retrieved_date: str) -> dict[str, Any]:
    return {
        "value": str(float(side)),
        "exact_form": str(side),
        "algebraic_degree": None,
        "minimal_polynomial": None,
        "analytically_optimized": None,
        "catalogue_rigid": "not-stated",
        "construction_method": "trivial-grid",
        "tilt_angles_deg": [0],
        "found_by": [],
        "found_year": None,
        "improved_by": [],
        "catalogue_pictured": False,
        "source_key": "[Kingbird]",
        "source_date": None,
        "retrieved_date": retrieved_date,
        "witnesses": [_witness_id(n)],
        "evidence": [KINGBIRD_EVIDENCE],
    }


def _catalogue_reported_upper(
    n: int, facts: CatalogueFacts, retrieved_date: str
) -> dict[str, Any]:
    if facts.construction_method not in CONSTRUCTION_PHRASES:
        raise GenerationError(
            f"n={n}: {facts.construction_method!r} is not a construction_method the "
            f"schema allows"
        )
    return {
        "value": facts.side_decimal,
        "exact_form": facts.exact_form,
        "algebraic_degree": facts.algebraic_degree,
        "minimal_polynomial": facts.minimal_polynomial,
        "analytically_optimized": facts.analytically_optimized,
        "catalogue_rigid": facts.catalogue_rigid,
        "construction_method": facts.construction_method,
        "tilt_angles_deg": None,
        "found_by": list(facts.found_by),
        "found_year": facts.found_year,
        "improved_by": list(facts.improved_by),
        "catalogue_pictured": facts.catalogue_pictured,
        "source_key": "[Kingbird]",
        "source_date": None,
        "retrieved_date": retrieved_date,
        "witnesses": [_witness_id(n)],
        "evidence": [KINGBIRD_EVIDENCE],
    }


def _reported_lower(n: int, side: int) -> dict[str, Any]:
    if is_perfect_square(n):
        return {
            "value": str(float(side)),
            "exact_form": None,
            "kind": "perfect-square",
            "proved_by": [],
            "proved_year": None,
            "source_key": None,
            "note": None,
            "scope": None,
            "evidence": [AREA_LOWER_EVIDENCE],
        }
    return {
        "value": nagamochi_value(n, REPORTED_SIGNIFICANT),
        "exact_form": None,
        "kind": "nagamochi",
        "proved_by": ["Hiroshi Nagamochi"],
        "proved_year": 2005,
        "source_key": "[Nagamochi 2005]",
        "note": NAGAMOCHI_NOTE,
        "scope": None,
        "evidence": [NAGAMOCHI_EVIDENCE],
    }


# --------------------------------------------------------------------------------------
# The prose
# --------------------------------------------------------------------------------------


def _packing_section(n: int, payload: Mapping[str, Any]) -> list[str]:
    reported = payload["reported_upper_bound"]
    if not reported["catalogue_pictured"]:
        side = grid_ceiling(n)
        return [
            (
                f"The record catalogue does not picture `n = {n}`: no arrangement has "
                f"ever been found that beats the trivial `⌈√{n}⌉ = {side}` grid, so the "
                f"grid is still the best known packing."
            ),
            "That is a statement about what has been searched, not a proof.",
        ]

    method = CONSTRUCTION_PHRASES[reported["construction_method"]]
    names = _join_names(reported["found_by"])
    year = reported["found_year"]
    if not names:
        credit = f"Found by an unrecorded author, via {method}."
    elif year is None:
        credit = f"Found by {names}, via {method}."
    else:
        credit = f"Found by {names} in {year}, via {method}."
    lines = [credit]
    if reported["improved_by"]:
        lines.append(f"Later improved by {_join_names(reported['improved_by'])}.")
    if reported["algebraic_degree"] is not None:
        lines.append(
            f"Its side length is algebraic of degree **{reported['algebraic_degree']}** "
            f"over `ℚ`."
        )
    return lines


def _nagamochi_lower_section(n: int) -> list[str]:
    default = (
        NAGAMOCHI_DEFAULT_COUNTED if n <= HAND_AUTHORED_MAX else NAGAMOCHI_DEFAULT_UNCOUNTED
    )
    return [
        "Nothing specific to this `n` has ever been proved.",
        "The bound is Nagamochi’s general closed form, which applies to every `N ≥ 4`:",
        "",
        "```",
        NAGAMOCHI_DISPLAY,
        "```",
        "",
        default,
    ]


def _ceiling_section(n: int, payload: Mapping[str, Any]) -> list[str]:
    verified = str(payload["verified_upper_bound"]["value"])
    reported = str(payload["reported_upper_bound"]["value"])
    return [
        "## The verified upper bound is a ceiling",
        "",
        (
            f"`verified_upper_bound` for this case is `{verified}`, which is **larger** "
            f"than the best known `{reported}` two fields above it."
        ),
        (
            "It is not a tighter reading of the same packing and it is not the value of "
            f"`s({n})`: it is the strongest ceiling this repository can certify from its "
            f"own evidence — the trivial grid bound `⌈√{n}⌉ = {verified}` — and it trails "
            f"the reported construction by `{_exact_difference(verified, reported)}`."
        ),
        "",
        (
            f"Its `exact_form` is the exact form of that ceiling, never of `s({n})`. "
            f"`s({n})` is not known exactly; `status` stays `open`, and the `mathematics` "
            "blocker in the frontmatter names the gap. Read `reported_upper_bound` for "
            "the best known side length."
        ),
        "",
    ]


def render_body(n: int, payload: Mapping[str, Any]) -> str:
    """The reader-facing half of the record, wrapped the way every other document here is."""
    side = grid_ceiling(n)
    reported_value = str(payload["reported_upper_bound"]["value"])
    verified_lower_value = str(payload["verified_lower_bound"]["value"])
    lines: list[str] = []

    if payload["status"] == "proved":
        lines.append(f"# `s({n})` — solved")
        lines.append("")
        if is_perfect_square(n):
            lines.append(f"`s({n}) = {side}`. Established by triviality (a perfect square).")
        else:
            lines.append(
                f"`s({n}) = {side}`. Established by Nagamochi’s general theorem, "
                "Hiroshi Nagamochi (2005)."
            )
            lines.append(f"General closed form: {NAGAMOCHI_NOTE.split(': ', 1)[1]}")
        lines.append("")
    else:
        lines.append(f"# `s({n})` — open")
        lines.append("")
        lines.append(
            f"Open. The best known packing gives `s({n}) ≤ "
            f"{display_upper(reported_value)}`, and the best proved lower bound is "
            f"`{display_lower(verified_lower_value)}` from Nagamochi’s general theorem, "
            f"leaving a gap of `{display_gap(reported_value, verified_lower_value)}`. "
            f"General closed form: {NAGAMOCHI_NOTE.split(': ', 1)[1]}"
        )
        lines.append("")
        if payload["blockers"]:
            lines.extend(_ceiling_section(n, payload))

    lines.append("## The packing")
    lines.append("")
    lines.extend(_packing_section(n, payload))
    lines.append("")
    lines.append("## The lower bound")
    lines.append("")
    if is_perfect_square(n):
        lines.append(
            f"`{n}` is a perfect square, so the `{side}×{side}` grid is optimal and the "
            "area bound `√n` is already tight."
        )
    else:
        lines.extend(_nagamochi_lower_section(n))
    lines.append("")
    lines.append(COMMON_DOC_FOOTER)

    # Formatted in process by the Python build of the same formatter the pre-commit hook
    # runs, so a generated record arrives already wrapped the way the register is and the
    # hook has nothing to restage. `render_explainer.py` loads it the same way and for
    # the same reason: a network fetch inside a generator would make it depend on an
    # index being reachable.
    from flowmark import reformat_text  # noqa: PLC0415

    return reformat_text("\n".join(lines), semantic=True, cleanups=True)


def render_record(payload: Mapping[str, Any]) -> str:
    """One complete `n-NNN.md`: front matter, then the prose that restates it."""
    n = int(payload["n"])
    document = {
        "title": f"s({n}) — square packing case",
        "softschema": {
            "contract": "packing.squares:SquarePackingCase/v2",
            "schema": "square-packing-case.schema.yaml",
            "envelope": "packing",
            "status": "enforced",
        },
        "packing": dict(payload),
    }
    front = yaml.safe_dump(document, allow_unicode=True, sort_keys=False, width=96)
    return f"---\n{front}---\n{render_body(n, payload)}"


def generate_record(
    n: int,
    *,
    availability: Mapping[int, SourceAvailability],
    catalogue: Mapping[int, CatalogueFacts] | None,
    review_date: str,
    retrieved_date: str,
) -> str:
    """Draft the complete record text for one `n`."""
    source = availability.get(n)
    if source is None:
        raise GenerationError(
            f"n={n} has no row in the source map; the map covers "
            f"{min(availability)}..{max(availability)}"
        )
    facts: CatalogueFacts | None = None
    if not source.is_grid:
        if catalogue is None:
            raise GenerationError(f"n={n} is a catalogue case and no catalogue was supplied")
        facts = catalogue.get(n)
        if facts is None:
            raise GenerationError(f"n={n} is a catalogue case and the catalogue has no entry")
    payload = build_payload(
        n,
        source=source,
        facts=facts,
        review_date=review_date,
        retrieved_date=retrieved_date,
    )
    return render_record(payload)


# --------------------------------------------------------------------------------------
# Writing, and refusing to
# --------------------------------------------------------------------------------------


def record_path(out_dir: Path, n: int) -> Path:
    return out_dir / f"n-{n:03d}.md"


def refuse_reason(n: int, out_dir: Path, *, force: bool) -> str | None:
    """Why this `n` may not be written to `out_dir`, or `None` if it may."""
    into_register = out_dir.resolve() == FRONTIER.resolve()
    if n <= HAND_AUTHORED_MAX and into_register:
        return (
            f"n={n} is hand-authored; the generator does not write n <= "
            f"{HAND_AUTHORED_MAX} into {FRONTIER.name}/. Generate it into another "
            f"directory to compare against what a person wrote."
        )
    if n > CATALOGUE_COMPLETENESS_MAX:
        return (
            f"n={n} is past {CATALOGUE_COMPLETENESS_MAX}, where the catalogue's "
            f"completeness statement stops: no source vouches for the grid there."
        )
    target = record_path(out_dir, n)
    if target.exists() and not force:
        return f"{target} exists; pass --force to overwrite it"
    return None


def _existing_dates(path: Path, review_date: str, retrieved_date: str) -> tuple[str, str]:
    """The review and retrieval dates a record already carries, for `--check`.

    Both are caller-supplied and neither is derivable, so regenerating with today's date
    would report every record as drifted on the day after it landed. Checking a record
    against itself means reusing the dates it declares.
    """
    document = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])
    payload = document.get("packing")
    if not isinstance(payload, Mapping):
        return review_date, retrieved_date
    reported = payload.get("reported_upper_bound")
    retrieved = (
        reported.get("retrieved_date") if isinstance(reported, Mapping) else None
    ) or retrieved_date
    return str(payload.get("source_reviewed") or review_date), str(retrieved)


def write_record(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_text(text, encoding="utf-8")


def diff_record(existing: str, generated: str, name: str) -> list[str]:
    return list(
        difflib.unified_diff(
            existing.splitlines(),
            generated.splitlines(),
            fromfile=f"{name} (committed)",
            tofile=f"{name} (generated)",
            lineterm="",
        )
    )


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--n", type=int, help="generate this single case")
    selection.add_argument(
        "--range",
        nargs=2,
        type=int,
        metavar=("FIRST", "LAST"),
        help="generate every case in this inclusive range",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=FRONTIER,
        help="directory to write into (default: the frontier register)",
    )
    parser.add_argument(
        "--force", action="store_true", help="overwrite records that already exist"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="regenerate into a temporary directory and report any drift; writes nothing",
    )
    parser.add_argument(
        "--review-date",
        default=dt.datetime.now(tz=dt.UTC).date().isoformat(),
        help="source_reviewed for generated records (default: today, UTC)",
    )
    parser.add_argument(
        "--retrieved-date",
        default=None,
        help="reported_upper_bound.retrieved_date (default: the review date)",
    )
    parser.add_argument(
        "--availability", type=Path, default=None, help="override the source map path"
    )
    parser.add_argument(
        "--catalogue", type=Path, default=None, help="override the catalogue transcription path"
    )
    return parser.parse_args(argv)


def selected(args: argparse.Namespace) -> list[int]:
    if args.n is not None:
        return [int(args.n)]
    first, last = (int(value) for value in args.range)
    if last < first:
        raise GenerationError(f"--range {first} {last} is empty")
    return list(range(first, last + 1))


def _check(
    cases: Iterable[int],
    args: argparse.Namespace,
    availability: Mapping[int, SourceAvailability],
    catalogue: Mapping[int, CatalogueFacts] | None,
) -> int:
    """Regenerate each case into a temporary directory and diff it against the register."""
    problems = 0
    checked = 0
    with tempfile.TemporaryDirectory(prefix="frontier-check-") as scratch:
        scratch_dir = Path(scratch)
        for n in cases:
            existing_path = record_path(args.out, n)
            if not existing_path.exists():
                print(f"n={n}: no record at {existing_path} to check")
                problems += 1
                continue
            existing = existing_path.read_text(encoding="utf-8")
            review, retrieved = _existing_dates(
                existing_path, args.review_date, args.retrieved_date or args.review_date
            )
            generated = generate_record(
                n,
                availability=availability,
                catalogue=catalogue,
                review_date=review,
                retrieved_date=retrieved,
            )
            write_record(generated, record_path(scratch_dir, n))
            checked += 1
            if generated != existing:
                problems += 1
                print("\n".join(diff_record(existing, generated, existing_path.name)))
    print(f"checked {checked} record(s); {problems} disagree with the generator")
    return 1 if problems else 0


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        cases = selected(args)
        availability = load_availability(args.availability)
        needs_catalogue = any(n in availability and not availability[n].is_grid for n in cases)
        catalogue = load_catalogue(args.catalogue) if needs_catalogue else None

        if args.check:
            return _check(cases, args, availability, catalogue)

        retrieved = args.retrieved_date or args.review_date
        written = 0
        for n in cases:
            reason = refuse_reason(n, args.out, force=args.force)
            if reason is not None:
                print(f"refused: {reason}")
                return 1
            text = generate_record(
                n,
                availability=availability,
                catalogue=catalogue,
                review_date=args.review_date,
                retrieved_date=retrieved,
            )
            write_record(text, record_path(args.out, n))
            written += 1
    except GenerationError as error:
        print(f"error: {error}")
        return 1
    print(f"wrote {written} record(s) to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
