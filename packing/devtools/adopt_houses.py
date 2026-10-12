# ruff: noqa: RUF001 -- this module writes case prose, whose typography uses curly apostrophes.
"""Move each case record to the house `devtools.select_houses` derives from the register.

The register held confirmed, reviewed upper bounds by others below their case records'
ceilings, each *pending adoption*, while house adoption waited for jlevy/squares#403; the
owner lifted that wait on 11 October 2026. For every count whose house moves, this writes:

- **the case record's front matter**: the reported and the verified upper bound move
  together to the house's exact side, the reported lane citing the source's report and
  the verified lane its confirming replay; the earlier house becomes a priority note,
  kept as history; every confirmed certificate at the count, selected or not, joins the
  case's evidence roster, which is what lets `check_certificate_citations` drop its
  deferrals; the source joins the resources; a conjectured optimum the house beats is
  withdrawn, and one it does not beat stops the adoption for a human to decide; a blocker
  that only said the verified lane trailed the report goes;
- **the case record's body**: a dated paragraph under the title that states the move,
  and a section after the verification code that says whose certificate the house is,
  how it was confirmed here and which certificates it replaces;
- **the coverage register**: the count's selected override names the new source, the
  reports the earlier one superseded name the new one, and the earlier selected claim is
  itself recorded as superseded;
- **the deferrals**: every `certificate-citation-deferrals.yaml` entry whose evidence a
  case record now cites is removed, as that file requires;
- **the prior state**: before the first record is written, each moved record's complete
  earlier text is retained in the archive of the pass that moves it (`prior_state`), as
  the Ry-Xu and Gupta adoptions retain theirs, so the tests of a source this adoption
  displaced can still draft its case as that source held it, and the writer can be
  replayed from what each pass read. The earlier houses are not copied: each is rebuilt
  from its own retained packet.

The drawing, `witnesses/known-best/n-NNN.yaml`, is `devtools.upper_bound_houses`'s; this
refuses a count that module does not house, and the atlas is refreshed after it runs.
`adopt_case` is the generator's half: `generate_frontier_case` redrafts an adopted case
through it (`source_supersession.adopt_selected_report`), which keeps the house and takes
the ordinary lower lanes from the draft.

It is idempotent: a count already at its house is left alone, so a second run writes
nothing, and ``--check`` reports any adopted count whose record differs from its house.

Usage, from ``packing/`` with the project interpreter::

    python -m devtools.adopt_houses             # write
    python -m devtools.adopt_houses --dry-run   # list what would move
    python -m devtools.adopt_houses --check     # hold every adopted case to its house

**A later pass.** A later import adopted the same way needs:

- its register entry at `V3`/`C3` with an accepted review covering it;
- its packet in `upper_bound_houses._sources`, each count it houses in
  `upper_bound_houses.ADOPTED`, and those counts under the pass's day in
  `upper_bound_houses.LATER_PASSES`, which dates every sentence, note, review date and
  coverage reason this writes for them;
- a coverage-register entry for its source key whose scope holds each count it houses.
  Where that entry declares a `claims_record`, the record must print the in-corpus claims,
  since `_value` holds the selected value to its print: a record that holds only claims
  beyond the corpus refuses the adoption. Such a source takes a second entry for its
  in-corpus counts with no claims record, as issue 506's does (`coverage_source`); Hunt
  3's moved its `claims_record` to `claims.json` for the same reason;
- its prose in `RESULTS` and each count's credit in `CREDITS` here.

`select_houses` then names the counts and this writes them. A count an earlier pass
adopted is adopted again in place: the earlier pass's paragraph, section and verified
statements are marked as history (`historical`), its house becomes a note dated from the
day it was adopted until this one, and its selected override becomes a superseded row.
The pass retains each record it moves, as it stood before, in an archive of its own day;
the earlier pass's archive is never rewritten, so the writer can be replayed from each
count's state before its last pass (`before_last_pass`) and the history readers still
find each count as it stood before its first (`read_history`).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_output_file

from devtools import select_houses
from devtools import upper_bound_houses as houses
from sqpack.yamlio import safe_load

ROOT = select_houses.ROOT
REPO = select_houses.REPO
FRONTIER = select_houses.FRONTIER
COVERAGE = FRONTIER / "source-coverage.yaml"
BIBLIOGRAPHY = ROOT / "resources/bibliography.yaml"
DEFERRALS = ROOT / "devtools/certificate-citation-deferrals.yaml"
PRIOR_FORMAT = "house-adoption-prior-frontier-v1"
WIDTH = 96
FINAL_REVIEW = "docs/project/reviews/review-2026-10-11-final-upper-bounds.md"
FOOTER = "<!-- This document follows common-doc-guidelines.md."
PLACES = select_houses.DISPLAY_PLACES
#: Longest exact fraction the prose writes out; a longer one is given by its decimals.
FRACTION_CHARS = 72


@dataclass(frozen=True)
class Prose:
    """What a case body says of one adopted result's certificates."""

    author: str
    reported: str
    producer_route: bool
    ai: str
    #: Where the source itself ran this repository's maintained routes, what to say instead.
    routes: str = ""


#: Each adopted result, as its register entry and its review describe it.
RESULTS: dict[str, Prose] = {
    "T-128": Prose(
        author="Francisco Couzo",
        reported="on [jlevy/squares#451](https://github.com/jlevy/squares/issues/451)",
        producer_route=True,
        ai="",
    ),
    "T-130": Prose(
        author="Francisco Couzo",
        reported=(
            "in a comment on "
            "[pull request #460](https://github.com/jlevy/squares/pull/460#issuecomment-6070798890)"
        ),
        producer_route=True,
        ai="",
    ),
    "T-134": Prose(
        author="Francisco Couzo",
        reported="on [jlevy/squares#476](https://github.com/jlevy/squares/issues/476)",
        producer_route=True,
        ai="The author says the search was written with Claude under his direction.",
    ),
    "T-136": Prose(
        author="Nate Chaoweeraprasit",
        reported="on [jlevy/squares#481](https://github.com/jlevy/squares/issues/481)",
        producer_route=False,
        ai=(
            "The source states that SQUISH’s solver, its verification and the issue were "
            "written with Claude Opus 5.5 under the author’s direction."
        ),
    ),
    "T-139": Prose(
        author="Evan Daniel",
        reported="in his repository’s `search/trio126` directory, on no issue",
        producer_route=False,
        ai="The source’s commit names Claude Opus 5.5 as co-author.",
    ),
    "T-140": Prose(
        author="Francisco Couzo",
        reported="on [jlevy/squares#488](https://github.com/jlevy/squares/issues/488)",
        producer_route=True,
        ai=(
            "The author says the search code and the request were written with Claude "
            "under his direction."
        ),
    ),
    "T-141": Prose(
        author="Evan Daniel",
        reported="on [jlevy/squares#489](https://github.com/jlevy/squares/issues/489)",
        producer_route=False,
        ai=(
            "The author says the search code and the request were written with Claude "
            "under his direction."
        ),
    ),
    "T-146": Prose(
        author="Evan Daniel",
        reported="in his regularized record lists, on no issue",
        producer_route=False,
        ai=(
            "The source’s credits say the repository’s work was produced by Claude "
            "(Anthropic) under human direction."
        ),
    ),
    "T-147": Prose(
        author="PingYou Ltd",
        reported="on [jlevy/squares#503](https://github.com/jlevy/squares/issues/503)",
        producer_route=False,
        ai=(
            "The source’s first commit and the issue as first posted said that verification, "
            "comparison review and package preparation were assisted by OpenAI Codex; the "
            "pinned commit removed that sentence, giving no reason."
        ),
        routes=(
            "The source ran both maintained routes itself before reporting; both predate it, "
            "and the third route is independently re-implemented."
        ),
    ),
    "T-148": Prose(
        author="PingYou Ltd",
        reported="on [jlevy/squares#504](https://github.com/jlevy/squares/issues/504)",
        producer_route=False,
        ai=(
            "The source makes no statement about AI assistance; the same author’s n207 "
            "release, eight minutes earlier, removed a disclosure of OpenAI Codex assistance "
            "at its pin."
        ),
        routes=(
            "The source ran both maintained routes itself before reporting; both predate it, "
            "and the third route is independently re-implemented."
        ),
    ),
    "T-149": Prose(
        author="Daniil Ostashev",
        reported="on [jlevy/squares#501](https://github.com/jlevy/squares/issues/501)",
        producer_route=False,
        ai="The source states nothing about AI assistance.",
    ),
    "T-150": Prose(
        author="Robert Barnett",
        reported="on [jlevy/squares#505](https://github.com/jlevy/squares/issues/505)",
        producer_route=False,
        ai=(
            "The author discloses OpenAI Codex assistance with the solver, the certificate "
            "and checker code, source review and preparation."
        ),
    ),
    "T-151": Prose(
        author="Nate Chaoweeraprasit",
        reported="on [jlevy/squares#500](https://github.com/jlevy/squares/issues/500)",
        producer_route=False,
        ai=(
            "The source states that SQUISH’s solver, its verification and the issue were "
            "written with Claude Opus 5.5, and that the Mondrian composition method was "
            "formulated by the author and implemented with Claude Opus 5.5, under his "
            "direction."
        ),
    ),
    "T-152": Prose(
        author="Francisco Couzo",
        reported="on [jlevy/squares#506](https://github.com/jlevy/squares/issues/506)",
        producer_route=True,
        ai=(
            "The author says the search code and the request were written with Claude "
            "under his direction."
        ),
    ),
}

XU = "ry-xu"
SQUISH = "Nate Chaoweeraprasit (itsnaka)"
COUZO = "Francisco Couzo"
DANIEL = "Evan Daniel"
PINGYOU = "PingYou Ltd"
OSTASHEV = "Daniil Ostashev"
BARNETT = "Robert Barnett"


@dataclass(frozen=True)
class Credit:
    """Who found the packing a count's house holds, who improved it, and how to say so."""

    found_by: tuple[str, ...]
    improved_by: tuple[str, ...]
    phrase: str


def _couzo(start: str) -> Credit:
    finder = XU if start == "Xu" else SQUISH
    whose = "Ryan Xu’s" if start == "Xu" else "Nate Chaoweeraprasit’s SQUISH"
    return Credit((finder,), (COUZO,), f"Francisco Couzo’s refinement of {whose} packing")


def _mondrian(pieces: str) -> Credit:
    """A SQUISH Mondrian composition, with the pieces as its source names them (T-151)."""
    return Credit(
        (SQUISH,), (), f"Nate Chaoweeraprasit’s SQUISH packing, composed from {pieces}"
    )


def _regularized(finder: str, whose: str, *, via: str | None = None) -> Credit:
    improved = (via, DANIEL) if via else (DANIEL,)
    refined = f", as {via} refined it," if via else ""
    return Credit(
        (finder,),
        improved,
        f"Evan Daniel’s display regularization of {whose} packing{refined}",
    )


#: The credit of each adopted count, from the register's credit lines and the adoption
#: tables of the reviews that recommended each house; a regularization leaves the packing
#: with its finder (`T-146`'s `regularizations`).
CREDITS: dict[int, Credit] = {
    70: _regularized(XU, "Ryan Xu’s"),
    84: _couzo("Xu"),
    86: _couzo("Xu"),
    102: _regularized(XU, "Ryan Xu’s"),
    103: _regularized(XU, "Ryan Xu’s", via="Mishapolk"),
    105: _couzo("Xu"),
    108: _couzo("Xu"),
    123: _regularized(XU, "Ryan Xu’s"),
    126: Credit(
        (XU,),
        (DANIEL,),
        "Evan Daniel’s reconstruction and exact certificate of Ryan Xu’s arrangement",
    ),
    127: _couzo("Xu"),
    129: _regularized(XU, "Ryan Xu’s"),
    131: Credit((SQUISH,), (), "Nate Chaoweeraprasit’s SQUISH packing"),
    132: Credit((DANIEL,), (), "Evan Daniel’s record-hunt packing"),
    146: Credit((XU,), (BARNETT,), "Robert Barnett’s refinement of Ryan Xu’s packing"),
    153: Credit(
        (PINGYOU,),
        (),
        "PingYou Ltd’s construction, after Ryan Xu’s n = 70 packing and Evan Daniel’s exact "
        "certificate of it",
    ),
    154: Credit((SQUISH,), (), "Nate Chaoweeraprasit’s SQUISH packing"),
    155: Credit((OSTASHEV,), (), "Daniil Ostashev’s packing"),
    156: Credit((OSTASHEV,), (), "Daniil Ostashev’s packing"),
    175: _couzo("Xu"),
    176: _mondrian(
        "Francisco Couzo’s n = 127 packing and the Kingbird catalogue’s n = 5 packing"
    ),
    180: Credit(
        (SQUISH,),
        ("Siddharth Gupta", COUZO),
        "Francisco Couzo’s refinement of Nate Chaoweeraprasit’s SQUISH packing, "
        "as Siddharth Gupta refined it",
    ),
    181: _mondrian("two of SQUISH’s own n = 154 packings"),
    207: Credit(
        (PINGYOU,),
        (),
        "PingYou Ltd’s assembly of two placed patches of Ryan Xu’s n = 70 packing, from "
        "Evan Daniel’s exact certificate of it",
    ),
    209: _couzo("SQUISH"),
    211: Credit((OSTASHEV,), (), "Daniil Ostashev’s packing"),
    228: Credit((COUZO,), (), "Francisco Couzo’s refinement of his own packing"),
    232: Credit((SQUISH,), (), "Nate Chaoweeraprasit’s SQUISH packing"),
    236: _regularized(SQUISH, "Nate Chaoweeraprasit’s SQUISH"),
    237: _couzo("SQUISH"),
    238: _mondrian("SQUISH’s own n = 305 and n = 154 packings"),
    239: _mondrian(
        "SQUISH’s n = 209 packing as Siddharth Gupta refined it and its own n = 240 packing"
    ),
    258: _regularized(SQUISH, "Nate Chaoweeraprasit’s SQUISH", via="Mishapolk"),
    259: Credit((SQUISH,), (), "Nate Chaoweeraprasit’s SQUISH packing"),
    261: Credit((XU,), (BARNETT,), "Robert Barnett’s refinement of Ryan Xu’s packing"),
    263: _regularized(SQUISH, "Nate Chaoweeraprasit’s SQUISH"),
    267: _couzo("Xu"),
    269: _regularized(SQUISH, "Nate Chaoweeraprasit’s SQUISH"),
    270: _mondrian(
        "SQUISH’s issue 481 n = 209 packing, whole, and the Kingbird catalogue’s former "
        "n = 19 packing"
    ),
    271: _mondrian("SQUISH’s own n = 305 and n = 240 packings"),
    272: _mondrian(
        "SQUISH’s own n = 240 packing and the Kingbird catalogue’s former n = 182 packing"
    ),
    292: _regularized(SQUISH, "Nate Chaoweeraprasit’s SQUISH"),
    295: _regularized(XU, "Ryan Xu’s"),
    302: _regularized(SQUISH, "Nate Chaoweeraprasit’s SQUISH"),
    303: _regularized(SQUISH, "Nate Chaoweeraprasit’s SQUISH"),
    304: Credit(
        (SQUISH,),
        (COUZO,),
        "Francisco Couzo’s refinement of Nate Chaoweeraprasit’s SQUISH Mondrian packing",
    ),
    305: Credit(
        (SQUISH,),
        (COUZO,),
        "Francisco Couzo’s refinement of Nate Chaoweeraprasit’s SQUISH Mondrian packing",
    ),
    306: Credit((COUZO,), (), "Francisco Couzo’s refinement of his own packing"),
    307: Credit((SQUISH,), (), "Nate Chaoweeraprasit’s SQUISH packing"),
    308: Credit(
        ("Kevin Fang",),
        (DANIEL,),
        "Evan Daniel’s move of Kevin Fang’s two-wedge construction",
    ),
}


class AdoptionError(ValueError):
    """The record cannot be moved as asked: a count, a source or a reader is missing."""


# ------------------------------------------------------------------------- reading


def _split(text: str) -> tuple[str, str, str]:
    """The record's opening fence, its front matter and the rest from the closing fence."""
    if not text.startswith("---\n"):
        raise AdoptionError("case record has no front matter")
    end = text.index("\n---\n", 4)
    return "---\n", text[4 : end + 1], text[end + 1 :]


def _packing(front: str) -> dict[str, Any]:
    return dict(safe_load(front)["packing"])


def _block_span(front: str, key: str) -> tuple[int, int]:
    """Where `packing.<key>` sits in the front matter, from its line to the next key's."""
    match = re.search(rf"^  {key}:", front, re.MULTILINE)
    if match is None:
        raise AdoptionError(f"front matter has no packing.{key}")
    following = re.search(r"^(  [a-z_]+:|[a-z_]+:)", front[match.end() :], re.MULTILINE)
    return match.start(), match.end() + following.start() if following else len(front)


def _dump(key: str, value: Any) -> str:
    text = yaml.safe_dump(
        {"packing": {key: value}}, sort_keys=False, allow_unicode=True, width=WIDTH
    )
    return text.split("\n", 1)[1]


def _replace(front: str, key: str, value: Any) -> str:
    start, end = _block_span(front, key)
    return front[:start] + _dump(key, value) + front[end:]


def _append(front: str, key: str, items: Sequence[Any]) -> str:
    """Append list items to `packing.<key>`, leaving the existing items' text alone."""
    if not items:
        return front
    start, end = _block_span(front, key)
    block = front[start:end]
    if block.rstrip().endswith("[]"):
        return front[:start] + _dump(key, list(items)) + front[end:]
    added = _dump(key, list(items)).split("\n", 1)[1]
    if not block.endswith("\n"):
        raise AdoptionError(f"packing.{key} does not end a line")
    return front[:end] + added + front[end:]


@cache
def _register() -> tuple[Mapping[str, Any], ...]:
    return tuple(select_houses.load_results())


def display(side: Fraction) -> str:
    """A side as prose shows it: exact where it ends within sixteen places, else rounded up."""
    for places in range(PLACES + 1):
        if (side * 10**places).denominator == 1:
            return select_houses.ceiling(side, places) if places else str(side.numerator)
    return select_houses.ceiling(side)


def _bibliography() -> Mapping[str, Mapping[str, Any]]:
    return _keyed(BIBLIOGRAPHY.read_text(encoding="utf-8"), "key")


def _covering(key: str, n: int) -> Mapping[str, Any]:
    """`coverage_source` in the register on disk, parsed and looked up once for each text."""
    return _covered(COVERAGE.read_text(encoding="utf-8"), key, n)


@cache
def _covered(text: str, key: str, n: int) -> Mapping[str, Any]:
    return coverage_source(_listed(text), key, n)


def coverage_source(
    sources: Sequence[Mapping[str, Any]], key: str, n: int
) -> Mapping[str, Any]:
    """The coverage register's entry for the source key `key` whose scope holds `n`.

    A source key can have more than one entry. Francisco Couzo's release of 11 October
    has two: its beyond-horizon rows read a claims record that holds only the claims
    beyond the corpus, and `check_source_coverage` holds a selected override of a source
    with a claims record to that record's print, so its in-corpus counts are an entry of
    their own. A key with one entry is that entry, as the register is keyed elsewhere.
    """
    found = [source for source in sources if str(source["source_key"]) == key]
    if len(found) > 1:
        found = [
            source for source in found if n in select_houses.scope_values(dict(source["scope"]))
        ]
    if len(found) != 1:
        raise AdoptionError(f"n={n}: {len(found)} coverage entries of {key} hold this count")
    return found[0]


@cache
def _listed(text: str) -> tuple[Mapping[str, Any], ...]:
    """A register's `sources` in order, parsed once for each text the file has held."""
    return tuple(safe_load(text)["sources"])


@cache
def _keyed(text: str, key: str) -> Mapping[str, Mapping[str, Any]]:
    """A register's `sources` by `key`, parsed once for each text the file has held."""
    return {str(source[key]): source for source in _listed(text)}


# ------------------------------------------------------------------------- the move


@dataclass(frozen=True)
class Move:
    """One count's adoption: the selection, the house and the record as it stood before."""

    selection: select_houses.Selection
    house: select_houses.Candidate
    packing: Mapping[str, Any]
    #: The case record's complete text before the move, which `rewrite` rewrites.
    text: str

    @property
    def n(self) -> int:
        return self.selection.n


@cache
def _claims(path: Path) -> Mapping[int, str]:
    """A source's claims reparsed from its retained record, once a run: the records are
    retained evidence, which an adoption reads and never writes."""
    from devtools.check_source_coverage import load_claims  # noqa: PLC0415

    return load_claims(path)


def _value(candidate: select_houses.Candidate) -> str:
    """The reported value: the source's print where its coverage claims record holds one.

    `check_source_coverage` holds a selected source that declares a claims record to the
    side that record prints; every other house is reported at its exact side rounded up
    at sixteen places, as the verified lane writes it.
    """
    source = _covering(candidate.source_key, candidate.n)
    if source.get("claims_record"):
        printed = _claims(ROOT / str(source["claims_record"])).get(candidate.n)
        if printed is None or Fraction(Decimal(printed)) != candidate.side:
            raise AdoptionError(
                f"n={candidate.n}: {source['id']}'s claims record does not print the exact side"
            )
        return printed
    return select_houses.ceiling(candidate.side)


def words(iso: str) -> str:
    """An ISO date as prose writes it: ``2026-10-12`` is ``12 October 2026``."""
    day = date.fromisoformat(iso)
    return f"{day.day} {day:%B %Y}"


def day_words(n: int) -> str:
    """The day the count's house was adopted, as prose writes it: ``12 October 2026``."""
    return words(houses.adopted_on(n))


def _sci(value: Fraction) -> str:
    return f"{float(value):.2e}"


def _join(names: Sequence[str]) -> str:
    names = list(names)
    if len(names) <= 2:
        return " and ".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def _results_holding(evidence: Sequence[str], n: int) -> list[str]:
    """The register entries whose evidence the case's bound cites, at `n`."""
    wanted = set(evidence)
    found = []
    for entry in _register():
        scope = select_houses.scope_values(dict(entry["scope"]))
        if n in scope and wanted & set(entry.get("evidence") or ()):
            found.append(str(entry["id"]))
    return found


#: Credited handles prose writes as the person's name, as the register's prose does.
PROSE_NAMES = {"ry-xu": "Ryan Xu"}


def _person(name: object) -> str:
    """A credited name as prose writes it, without the handle in parentheses."""
    text = re.sub(r"\s*\([^)]*\)$", "", str(name))
    return PROSE_NAMES.get(text, text)


def _earlier(packing: Mapping[str, Any]) -> list[str]:
    """The register entries the case's earlier verified ceiling rests on."""
    evidence = list(packing["verified_upper_bound"].get("evidence") or ())
    return _results_holding(evidence, packing["n"])


def _holder(packing: Mapping[str, Any]) -> str:
    """The earlier house, said the way the record credits it."""
    upper = packing["reported_upper_bound"]
    finders = [_person(name) for name in upper.get("found_by") or ()]
    improvers = [_person(name) for name in upper.get("improved_by") or ()]
    evidence = list(packing["verified_upper_bound"].get("evidence") or ())
    if "E-basic-grid-upper" in evidence:
        return "the trivial grid"
    text = _join(finders) + "’s packing" if finders else "the catalogue’s packing"
    if improvers:
        text += f", improved by {_join(improvers)}"
    results = _earlier(packing)
    if results:
        text += f" ({', '.join(results)})"
    return text


def plan(
    selections: Mapping[int, select_houses.Selection] | None = None,
    texts: Mapping[int, str] | None = None,
) -> list[Move]:
    """Every count whose derived house is below its case and is one this adoption houses.

    Each move carries its case record's text, read from the frontier unless `texts` holds
    the count, as a replay of the retained prior state passes it.
    """
    selections = select_houses.select() if selections is None else selections
    moves = []
    for n, selection in sorted(selections.items()):
        if selection.house is None:
            continue
        house = selection.house
        if houses.ADOPTED.get(n) != house.result:
            raise AdoptionError(
                f"n={n}: the house is {house.result}, which upper_bound_houses does not draw "
                "here; add its packet and the count to upper_bound_houses first"
            )
        if house.result not in RESULTS or n not in CREDITS:
            raise AdoptionError(f"n={n}: no prose or credit for {house.result}")
        if texts is not None and n in texts:
            text = texts[n]
        else:
            text = select_houses.case_path(n).read_text(encoding="utf-8")
        moves.append(Move(selection, house, _packing(_split(text)[1]), text))
    return moves


def _source_url(key: str, n: int) -> str:
    return str(_covering(key, n)["url"])


def reported_bound(move: Move) -> dict[str, Any]:
    house, credit = move.house, CREDITS[move.n]
    bibliography = _bibliography()[house.source_key]
    origin = houses.source_for(move.n).origin(move.n)
    return {
        "value": _value(house),
        "exact_form": houses.legacy.literal(house.side),
        "evidence": list(house.report_evidence),
        "algebraic_degree": 1,
        "minimal_polynomial": None,
        "analytically_optimized": None,
        "catalogue_rigid": "not-stated",
        "construction_method": "unknown",
        "tilt_angles_deg": None,
        "found_by": list(credit.found_by),
        "found_year": date.fromisoformat(house.published).year,
        "improved_by": list(credit.improved_by),
        "catalogue_pictured": False,
        "source_key": house.source_key,
        "source_date": str(bibliography["dated"]),
        "retrieved_date": origin.retrieved,
        "witnesses": [f"W-known-best-n{move.n:03d}"],
    }


def verified_bound(move: Move) -> dict[str, Any]:
    return {
        "value": select_houses.ceiling(move.house.side),
        "exact_form": houses.legacy.literal(move.house.side),
        "evidence": list(move.house.confirming_evidence),
    }


#: A history note this adoption wrote, and the day its house stopped being the ceiling.
HELD_UNTIL = re.compile(r"^Earlier house .*, the case’s ceiling (?:from .* )?until (.+?);")


def held_since(packing: Mapping[str, Any]) -> str | None:
    """The day the record's house became its ceiling, where an earlier note dates it.

    When an earlier pass adopted the house, its note on the house before says until when
    that one held, which is the day this one began; a house no pass of this adoption
    wrote has no such note, and its start is not stated.
    """
    days = [
        match.group(1)
        for note in packing.get("priority_notes") or ()
        if (match := HELD_UNTIL.match(" ".join(str(note.get("claim") or "").split())))
    ]
    return days[-1] if days else None


def history_note(move: Move) -> dict[str, Any]:
    upper = move.packing["reported_upper_bound"]
    claimed = [*(upper.get("found_by") or ()), *(upper.get("improved_by") or ())]
    since = held_since(move.packing)
    held = f"from {since} until" if since else "until"
    return {
        "claim": (
            f"Earlier house {upper['value']} from {upper['source_key']}, the case’s ceiling "
            f"{held} {day_words(move.n)}; its certificate and replay remain retained."
        ),
        "claimed_by": [str(name) for name in claimed],
        "published": upper.get("source_date"),
        "year": upper.get("found_year"),
    }


def _roster(move: Move) -> list[str]:
    """Every confirmed certificate's evidence at the count, selected or not."""
    wanted: list[str] = []
    for candidate in move.selection.candidates:
        wanted.extend(candidate.report_evidence)
        wanted.extend(candidate.confirming_evidence)
    return list(dict.fromkeys(wanted))


def _resource(move: Move) -> dict[str, Any]:
    return {
        "key": move.house.source_key,
        "role": "upper-bound-report",
        "local": f"web/{houses.source_for(move.n).packet.name}",
        "url": _source_url(move.house.source_key, move.n),
        "retrieved": True,
    }


def front_matter(move: Move, front: str) -> str:
    packing = move.packing
    conjecture = conjectured(packing)
    if conjecture is not None and move.house.side >= conjecture:
        raise AdoptionError(
            f"n={move.n}: the house {select_houses.ceiling(move.house.side)} does not "
            f"beat the conjectured optimum {packing['conjectured_optimum']}; whether the "
            "conjecture stands is decided by hand"
        )
    reviewed = f"  source_reviewed: '{houses.adopted_on(move.n)}'"
    front = re.sub(r"^  source_reviewed: .*$", reviewed, front, count=1, flags=re.MULTILINE)
    front = _replace(front, "reported_upper_bound", reported_bound(move))
    front = _replace(front, "verified_upper_bound", verified_bound(move))
    if conjecture is not None:
        front = re.sub(
            r"^  conjectured_optimum: .*$",
            "  conjectured_optimum: null",
            front,
            count=1,
            flags=re.MULTILINE,
        )
    front = _append(front, "priority_notes", [history_note(move)])
    present = set(packing.get("evidence") or ())
    front = _append(front, "evidence", [item for item in _roster(move) if item not in present])
    keys = {str(item["key"]) for item in packing.get("resources") or ()}
    if move.house.source_key not in keys:
        front = _append(front, "resources", [_resource(move)])
    blockers = packing.get("blockers") or []
    kept = [item for item in blockers if not _trailing_blocker(item)]
    if kept != blockers:
        front = _replace(front, "blockers", kept)
    return front


def conjectured(packing: Mapping[str, Any]) -> Fraction | None:
    """The side a record conjectures optimal, if it conjectures one.

    The generator writes `integer` for a grid case, whose conjecture is that the optimum
    is the integer side the case reports (`generate_frontier_case`).
    """
    conjecture = packing.get("conjectured_optimum")
    if conjecture is None:
        return None
    if conjecture == "integer":
        conjecture = packing["reported_upper_bound"]["value"]
    return Fraction(Decimal(str(conjecture)))


def _trailing_blocker(blocker: Mapping[str, Any]) -> bool:
    """A blocker that only said the verified lane trailed the report, which now agree."""
    detail = str(blocker.get("detail") or "")
    return blocker.get("kind") == "mathematics" and detail.startswith(
        "verified_upper_bound is "
    )


# ------------------------------------------------------------------------- the body


def _math_fraction(value: Fraction) -> str | None:
    text = houses.legacy.literal(value)
    return f"${text}$" if len(text) <= FRACTION_CHARS else None


def _review(result: str) -> tuple[str, str]:
    """The stage 4 review that recommended the result, and its date in words."""
    entry = next(e for e in _register() if e["id"] == result)
    review = next(
        r for r in entry["reviews"] if r["path"] != FINAL_REVIEW and r["verdict"] == "accepted"
    )
    return str(review["path"]), words(str(review["date"]))


def _finally_reviewed(result: str) -> bool:
    """Whether the final review of 11 October covered the result as well as its own."""
    entry = next(e for e in _register() if e["id"] == result)
    return any(r["path"] == FINAL_REVIEW for r in entry["reviews"])


def opening(move: Move) -> str:
    n, house, credit = move.n, move.house, CREDITS[move.n]
    upper = move.packing["reported_upper_bound"]
    return (
        f"**House adoption, {day_words(n)}.** {credit.phrase[0].upper()}{credit.phrase[1:]} "
        f"({house.result}) is now this case’s house: its exact certificate proves "
        f"$s({n}) \\le {select_houses.ceiling(house.side)}$, the reported and the verified "
        f"upper bound, `{_sci(move.selection.margin)}` below the ceiling the case held until "
        f"then, ${upper['value']}$ from {_holder(move.packing)}, which stays retained as "
        f"history ([the certificate](#{_anchor(move)}))."
    )


def _title(move: Move) -> str:
    return f"{RESULTS[move.house.result].author}’s certificate ({move.house.result})"


def _anchor(move: Move) -> str:
    text = _title(move).lower().replace("’", "")
    return re.sub(r"[^a-z0-9 -]", "", text).replace(" ", "-")


def section(move: Move) -> str:
    n, house, credit = move.n, move.house, CREDITS[move.n]
    prose = RESULTS[house.result]
    packet = houses.source_for(n).packet.name
    review, reviewed = _review(house.result)
    fraction = _math_fraction(house.side)
    ceiling = select_houses.ceiling(house.side)
    side = (
        f"at exact side {fraction}, displayed upward as ${ceiling}$"
        if fraction
        else f"at an exact rational side, displayed upward as ${ceiling}$"
    )
    routes = prose.routes or (
        "One maintained route is the verifier the source ran; the independent rational "
        "corner checker and the third route are independently re-implemented."
        if prose.producer_route
        else "No route here is the source’s code, so the replay is independently "
        "re-implemented."
    )
    reviews = f"[review of {reviewed}](../../{review})"
    if _finally_reviewed(house.result):
        reviews = f"{reviews} and the [final review of 11 October 2026](../../{FINAL_REVIEW})"
    paragraphs = [
        f"## {_title(move)}",
        (
            f"{credit.phrase[0].upper()}{credit.phrase[1:]}, reported {prose.reported}, "
            f"{side} ({house.result}). The certificate gives a rational side and, for each "
            f"of the {n} unit squares, a rational centre and the tangent of its half-angle; "
            f"the [retained packet](../resources/web/{packet}/README.md) holds it with the "
            "complete native jobs that decided it."
        ),
        (
            "Both maintained exact routes decided it here, `sqpack`’s exact separating-axis "
            "verifier and the independent rational corner checker, with its duplicate-square "
            "and outside-container controls, and a third exact route, half-extent containment "
            f"and exact intersection area, decided it again. {routes} The {reviews} "
            "accepted the replay for finite feasibility. "
            f"That proves $s({n}) \\le {ceiling}$, the verified upper bound: confirmed, "
            "independently re-implemented. It says nothing about "
            "optimality, rigidity or a local minimum."
        ),
    ]
    if house.regularizes:
        paragraphs.append(
            "The certificate regularizes for display the packing "
            f"{house.regularizes} records, at the side the source reports as that packing’s "
            "exact optimum, so the packing stays with its finder and Evan Daniel is "
            "credited with the regularization and the certificate. That the two are one "
            f"packing is the source’s claim, measured here and not decided ({house.result}’s "
            "regularizations)."
        )
    if prose.ai:
        paragraphs.append(prose.ai)
    earlier = set(_earlier(move.packing))
    others = [
        c for c in move.selection.candidates if c is not house and c.result not in earlier
    ]
    upper = move.packing["reported_upper_bound"]
    history = (
        f"The house it replaces, ${upper['value']}$ from {_holder(move.packing)}, stays "
        "retained with its own replay as history."
    )
    if others:
        listed = _join([f"{c.result} at ${display(c.side)}$" for c in others])
        history += (
            f" The other certificates confirmed here at this count, {listed}, stay verified "
            "and are not selected."
        )
    paragraphs.append(history)
    return "\n\n".join(paragraphs) + "\n"


#: The heading `apply_exact_ceilings` gives the section on a ceiling that trails the print.
CEILING_HEADING = "## The verified upper bound is a ceiling"
EARLIER_CEILING = "## The earlier verified ceiling"


def _earlier_ceiling(move: Move, text: str) -> str:
    """`T-101`'s exact-ceiling prose, in the past tense from this adoption on.

    `apply_exact_ceilings` wrote it where a certified side, rounded up at the catalogue's
    places, trailed the catalogue's print; the house replaces both lanes, so the ceiling,
    the blocker that recorded the gap and the certificate's bound are history.
    """
    n, until = move.n, day_words(move.n)
    bound = rf"\$s\({n}\)\s+\\le\s+[0-9.]+\$"
    text = re.sub(
        rf"\bit\s+proves\s+({bound}),\s+the\s+verified\s+upper\s+bound\s+\((T-\d+)\)\.",
        rf"it proved \1, the verified upper bound until {until} (\2).",
        text,
    )
    text = re.sub(
        rf"\bThat\s+proves\s+({bound}),\s+the\s+verified\s+upper\s+bound:\s+the\s+certificate’s",
        rf"That proved \1, the verified upper bound until {until}: the certificate’s",
        text,
    )
    start = text.find(f"\n{CEILING_HEADING}\n")
    if start < 0:
        return text
    end = text.find("\n## ", start + 1)
    end = len(text) if end < 0 else end
    section = text[start:end].replace(CEILING_HEADING, EARLIER_CEILING, 1)
    section = re.sub(
        r"`verified_upper_bound`\s+for\s+this\s+case\s+is\s+(\$[0-9.]+\$),",
        rf"Until {until} the verified upper bound here was \1,",
        section,
    )
    section = re.sub(
        r"It\s+is\s+\*\*larger\*\*\s+than\s+the\s+best\s+known\s+(\$[0-9.]+\$)\s+two\s+fields"
        r"\s+above\s+it,",
        r"It was **larger** than the catalogue’s printed side \1, then the best known,",
        section,
    )
    section = re.sub(
        rf"It\s+is\s+not\s+the\s+value\s+of\s+\$s\({n}\)\$",
        f"It was not the value of $s({n})$",
        section,
    )
    section = re.sub(
        r"The\s+`mathematics`\s+blocker\s+in\s+the\s+frontmatter\s+records\s+the\s+difference\."
        r"\s+Read\s+`reported_upper_bound`\s+for\s+the\s+best\s+known\s+side\s+length\.",
        f"A `mathematics` blocker in the frontmatter recorded the difference until "
        f"{_title(move)} replaced both lanes.",
        section,
    )
    return text[:start] + section + text[end:]


def historical(move: Move, text: str) -> str:
    """The body's own statements of the earlier house, marked as history.

    `check_case_prose` holds every `s(n) <= x` a body writes to the front matter unless
    its sentence says it is historical. Four kinds of prose state the earlier house, and
    each says now that it held until this adoption:

    - the opening "Open." sentence the generator writes, of the best known packing;
    - the exact-optimum sections that `T-098` wrote, in two fixed sentences;
    - the exact-ceiling prose that `T-101` wrote where a certified side rounded up trails
      the catalogue's print (`apply_exact_ceilings`): its dated paragraph, its ceiling
      section, now "The earlier verified ceiling", and its certificate section;
    - a house an earlier pass of this adoption adopted, in its dated paragraph and its
      section.

    Prose in no fixed form, which no tool here wrote, is not rewritten; `check_case_prose`
    refuses a record that still states it as the bound. The first pass marked such prose
    by hand at five counts, the SQUISH update sections at 155, 258, 263 and 302 and the
    grid prose at 308 (`test_house_adoption.HAND_MARKED`); every other word of an adopted
    body is what this writes from the record its last pass read.
    """
    n, until = move.n, day_words(move.n)
    text = re.sub(
        r"^Open\. The best known published packing,",
        "Open. Previously, the best known published packing,",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^Open\.\s+The\s+best\s+known\s+packing\s+gives\b",
        "Open. Previously, the best known packing gave",
        text,
        flags=re.MULTILINE,
    )
    text = _earlier_ceiling(move, text)
    # The records are wrapped, so a sentence may break at any space; whitespace is
    # matched as such and the reflow is the formatter's.
    text = re.sub(
        r"(\*\*House adoption, [^*]+\.\*\*(?:(?!\n\n).)*?)\bis\s+now\s+this\s+case’s\s+house:",
        rf"\1was this case’s house until {until}:",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        rf"(That\s+proves\s+\$s\({n}\)\s+\\le\s+[0-9.]+\$,\s+the\s+verified\s+upper\s+bound):"
        r"\s+confirmed,",
        rf"\1 until {until}: confirmed,",
        text,
    )
    return re.sub(
        rf"(That\s+proves\s+\$s\({n}\)\s+\\le\s+[0-9.]+\\ldots\$,\s+the\s+verified\s+upper\s+bound);"
        r"\s+it\s+says",
        rf"\1 until {until}; it says",
        text,
    )


def body(move: Move, rest: str) -> str:
    """The body with the dated paragraph under its title and the section before the footer."""
    rest = historical(move, rest)
    lines = rest.split("\n")
    title = next(i for i, line in enumerate(lines) if line.startswith("# "))
    lines[title + 1 : title + 1] = ["", opening(move)]
    text = "\n".join(lines)
    footer = text.find(FOOTER)
    insert = section(move) + "\n"
    if footer < 0:
        return text.rstrip("\n") + "\n\n" + insert
    return text[:footer] + insert + text[footer:]


def adopted(move: Move) -> bool:
    upper = move.packing["reported_upper_bound"]
    return (
        upper.get("source_key") == move.house.source_key
        and Fraction(str(move.packing["verified_upper_bound"].get("exact_form")))
        == move.house.side
    )


def rewrite(move: Move) -> str:
    """The case record at its house: `move.text` with its front matter and body moved."""
    opening_fence, front, rest = _split(move.text)
    closing, text = rest[:4], rest[4:]
    if closing != "---\n":
        raise AdoptionError(f"n={move.n}: front matter has no closing fence")
    return opening_fence + front_matter(move, front) + closing + body(move, text)


# ------------------------------------------------------------------------- coverage


def _section_span(text: str, key: str) -> tuple[int, int]:
    start = re.search(rf"^{key}:\n", text, re.MULTILINE)
    if start is None:
        raise AdoptionError(f"coverage register has no {key}")
    following = re.search(r"^[a-z_]+:", text[start.end() :], re.MULTILINE)
    return start.start(), start.end() + following.start() if following else len(text)


#: The clause of a displaced house's row that names the certificate below it.
DISPLACED_BY = re.compile(r"and T-\d+'s exact side is smaller\.$")
#: The day a selected override's reason says its house was adopted.
ADOPTED_ON_DAY = re.compile(r"\badopted on (\d{4}-\d{2}-\d{2}) \(T-\d+\)")


def coverage(moves: Sequence[Move], text: str) -> str:
    """The coverage register with each moved count's selection and supersessions."""
    data = safe_load(text)
    overrides = {int(entry["n"]): entry for entry in data["selected_overrides"]}
    superseded = list(data["superseded_reports"])
    for move in moves:
        n, house = move.n, move.house
        new = str(coverage_source(data["sources"], house.source_key, n)["id"])
        old = overrides.get(n)
        if old is not None and old["source_id"] == new:
            continue
        reason = (
            f"The smallest exact side the register holds at this count, confirmed at V3/C3 "
            f"by a replay here and an accepted review, adopted on {houses.adopted_on(n)} "
            f"({house.result})."
        )
        # Every report the earlier house beat, a catalogue baseline's included, is beaten
        # by the new one, which is smaller still. A row that an earlier adoption wrote for
        # the house it displaced names the house that is smaller; that is now this one.
        for report in superseded:
            if report["n"] == n:
                report["superseded_by"] = new
                if "reason" in report:
                    report["reason"] = DISPLACED_BY.sub(
                        f"and {house.result}'s exact side is smaller.", str(report["reason"])
                    )
        # The displaced house is recorded whether or not its source has a claims record:
        # its selected value is the source's print where it has one and the ceiling of
        # its exact side where it has none (`_value`). One an earlier pass adopted is
        # dated from that pass's day.
        if old is not None:
            since = ADOPTED_ON_DAY.search(str(old.get("reason") or ""))
            held = f"from {since.group(1)} until" if since else "until"
            superseded.append(
                {
                    "n": n,
                    "source_id": old["source_id"],
                    "value": old["value"],
                    "reason": (
                        f"The house {held} {houses.adopted_on(n)}; its certificate stays "
                        "retained and "
                        f"verified, and {house.result}'s exact side is smaller."
                    ),
                    "superseded_by": new,
                }
            )
        overrides[n] = {
            "n": n,
            "source_id": new,
            "value": _value(house),
            "evidence": house.report_evidence[0],
            "reason": reason,
        }
    superseded.extend(_unaccounted(data, overrides, superseded, moves))
    data["selected_overrides"] = [overrides[n] for n in sorted(overrides)]
    data["superseded_reports"] = superseded
    for key in ("selected_overrides", "superseded_reports"):
        start, end = _section_span(text, key)
        dumped = yaml.safe_dump(
            {key: data[key]}, sort_keys=False, allow_unicode=True, width=WIDTH
        )
        text = text[:start] + dumped + text[end:]
    return text


def _unaccounted(
    data: Mapping[str, Any],
    overrides: Mapping[int, Mapping[str, Any]],
    superseded: Sequence[Mapping[str, Any]],
    moves: Sequence[Move],
) -> list[dict[str, Any]]:
    """Each reparsed claim at a moved count that the new house holds, as superseded.

    `check_source_coverage` accounts for every claim a claims record prints, as a
    selected override, a superseded report or a beyond-horizon row. A claim at a moved
    count that was none of these, such as a certificate the issue did not name, is
    superseded by the count's new house when the house is not above it. Where the claim's
    source has an exact reader the two exact sides are compared, so a certificate equal
    to the house is said to be equal, whatever its print; otherwise the house is held to
    the print, and the row says so.
    """
    held = {move.n: move.house for move in moves}
    accounted = {(str(e["source_id"]), int(e["n"])) for e in superseded}
    accounted |= {(str(o["source_id"]), n) for n, o in overrides.items()}
    added = []
    for source in data["sources"]:
        if not source.get("claims_record"):
            continue
        for n, printed in sorted(_claims(ROOT / str(source["claims_record"])).items()):
            selected = overrides.get(n)
            if n not in held or (str(source["id"]), n) in accounted or selected is None:
                continue
            house, day = held[n], houses.adopted_on(n)
            exact = _exact_side(str(source.get("source_key") or ""), n)
            if exact is None and house.side < Fraction(Decimal(printed)):
                standing = f"the side it prints is above the house adopted here on {day}"
            elif exact is not None and house.side < exact:
                standing = (
                    f"its exact side is above the house adopted here on {day} ({house.result})"
                )
            elif exact is not None and house.side == exact:
                standing = (
                    f"its exact side equals the house adopted here on {day}, which "
                    f"{house.result}'s registered certificate holds"
                )
            else:
                continue
            added.append(
                {
                    "n": n,
                    "source_id": source["id"],
                    "value": printed,
                    "reason": (
                        "A certificate of the same release that no register entry cites; "
                        f"{standing}."
                    ),
                    "superseded_by": selected["source_id"],
                }
            )
    return added


def _exact_side(key: str, n: int) -> Fraction | None:
    """A claim's exact side where its source has a reader that rebuilds it at `n`."""
    if key not in select_houses.reports.HOUSES:
        return None
    try:
        return select_houses.reports.house_side(key, n)
    except select_houses.reports.ReportError:
        return None


# ------------------------------------------------------------------------- deferrals


def deferrals(text: str, cited: set[str]) -> str:
    """The deferral list without every entry whose evidence a case record now cites."""
    data = safe_load(text)
    kept = [entry for entry in data["deferrals"] if entry["evidence"] not in cited]
    if len(kept) == len(data["deferrals"]):
        return text
    head = text[: text.index("deferrals:")]
    if not kept:
        return head + "deferrals: []\n"
    rendered = yaml.safe_dump(
        {"deferrals": kept}, sort_keys=False, allow_unicode=True, width=WIDTH
    )
    lines = rendered.splitlines(keepends=True)
    return (
        head + lines[0] + "".join(f"  {line}" if line.strip() else line for line in lines[1:])
    )


def _cited(rewritten: Mapping[int, str] | None = None) -> set[str]:
    """The evidence every case record cites, reading `rewritten`'s texts where it has them."""
    rewritten = rewritten or {}
    found: set[str] = set()
    for path in sorted(FRONTIER.glob("n-[0-9][0-9][0-9].md")):
        n = int(path.stem.removeprefix("n-"))
        text = rewritten.get(n) or path.read_text(encoding="utf-8")
        found |= _evidence(_packing(_split(text)[1]))
    return found


def _evidence(node: object) -> set[str]:
    found: set[str] = set()
    if isinstance(node, Mapping):
        for key, value in node.items():
            if key == "evidence" and isinstance(value, list):
                found.update(str(item) for item in value)
            else:
                found |= _evidence(value)
    elif isinstance(node, list):
        for item in node:
            found |= _evidence(item)
    return found


# ------------------------------------------------------------------------- driving


# ------------------------------------------------------------------------- history


def passes() -> tuple[str, ...]:
    """The adoption's passes, earliest first: the day it began and each later pass's."""
    return (houses.ADOPTED_ON, *sorted(houses.LATER_PASSES))


def prior_state(day: str) -> Path:
    """The archive of the pass of `day`: each record it moved, as it stood before."""
    return ROOT / f"devtools/house-adoption-prior-state-{day}.json.xz"


def read_pass(day: str) -> dict[int, str]:
    """Each record the pass of `day` moved, as that pass read it before writing, by count.

    A count two passes moved is in both archives: the earlier holds the record before
    the adoption first moved it, and the later the record as the earlier pass left it.
    """
    path = prior_state(day)
    houses.reports.ensure_private(path)
    record = houses.kernel.read_xz(path)
    if (
        type(record) is not dict
        or set(record) != {"format", "adopted_on", "cases"}
        or record["format"] != PRIOR_FORMAT
        or record["adopted_on"] != day
        or type(record["cases"]) is not list
    ):
        raise AdoptionError(f"{path.name}: not the prior state of the pass of {day}")
    rows = {}
    for row in record["cases"]:
        if type(row) is not dict or set(row) != {"n", "frontier"} or row["n"] in rows:
            raise AdoptionError(f"{path.name}: malformed or repeated row")
        rows[int(row["n"])] = str(row["frontier"])
    return rows


def read_history() -> dict[int, str]:
    """Each moved record as it stood before this adoption first moved it, by count.

    What a source this adoption displaced held: the earliest pass's text of each count.
    """
    rows: dict[int, str] = {}
    for day in passes():
        if prior_state(day).exists():
            for n, text in read_pass(day).items():
                rows.setdefault(n, text)
    return rows


def before_last_pass() -> dict[int, str]:
    """Each adopted record as it stood before the pass that last moved it, by count.

    What that pass's writer read, so a replay of it from here gives the committed record:
    a count moved twice is read from the later pass's archive, as the earlier left it.
    """
    archives = {day: read_pass(day) for day in passes() if prior_state(day).exists()}
    rows = {}
    for n in houses.ADOPTED:
        day = houses.adopted_on(n)
        if n not in archives.get(day, {}):
            raise AdoptionError(f"n={n}: the pass of {day} retained no prior state of it")
        rows[n] = archives[day][n]
    return rows


def retain_history(day: str, texts: Mapping[int, str]) -> None:
    """Retain each record's earlier text in its pass's archive before the pass writes it.

    A count already in that archive keeps the text it was retained with: a pass's prior
    state is the record before that pass first moved it, never an intermediate one, and
    a later pass retains in its own archive and never rewrites an earlier one.
    """
    path = prior_state(day)
    rows = read_pass(day) if path.exists() else {}
    added = {n: text for n, text in texts.items() if n not in rows}
    if not added:
        return
    rows.update(added)
    houses.kernel.save_xz(
        path,
        {
            "format": PRIOR_FORMAT,
            "adopted_on": day,
            "cases": [{"n": n, "frontier": rows[n]} for n in sorted(rows)],
        },
    )


# ------------------------------------------------------------------------- redrafting

LOWER_LANES = ("reported_lower_bound", "verified_lower_bound", "reported_status", "status")
LOWER_SECTION = r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)"


def with_lane(text: str, key: str, value: Any) -> str:
    """The record with `packing.<key>` replaced and every other line as it was."""
    fence, front, rest = _split(text)
    return fence + _replace(front, key, value) + rest


def holds(n: int, text: str) -> bool:
    """Whether the record names this adoption's source as the house at its count."""
    if n not in houses.ADOPTED:
        return False
    upper = _packing(_split(text)[1])["reported_upper_bound"]
    return upper.get("source_key") == houses.source_for(n).key


def adopt_case(n: int, existing: str, generated: str) -> str:
    """The generator's redraft of an adopted case: the house stays, lower lanes are drafted.

    `generate_frontier_case` drafts a case from the catalogue and the sources it reads and
    hands the draft here with the record. An adopted case keeps its upper lanes, its prose
    and its history from the record, each upper lane held to the exact side its certificate
    rebuilds; the ordinary lower lanes, the status and the lower-bound section are the
    draft's. A record no longer at this adoption's source is the draft's entirely.
    """
    if not holds(n, existing):
        return generated
    opening_fence, front, rest = _split(existing)
    packing = _packing(front)
    source = houses.source_for(n)
    side = houses.side(n)
    for lane in ("reported_upper_bound", "verified_upper_bound"):
        if Fraction(str(packing[lane].get("exact_form"))) != side:
            raise AdoptionError(f"n={n}: the {lane} is not {source.result}'s exact side")
    _, draft_front, draft_rest = _split(generated)
    draft = _packing(draft_front)
    for key in LOWER_LANES:
        if key in draft and draft[key] != packing.get(key):
            front = _replace(front, key, draft[key])
    drafted = re.search(LOWER_SECTION, draft_rest, re.DOTALL)
    if drafted is not None:
        rest = re.sub(
            LOWER_SECTION, lambda _match: drafted.group(), rest, count=1, flags=re.DOTALL
        )
    return opening_fence + front + rest


def _write(path: Path, text: str) -> bool:
    if path.read_text(encoding="utf-8") == text:
        return False
    with atomic_output_file(path) as temporary:
        temporary.write_text(text, encoding="utf-8")
    return True


def write(moves: Sequence[Move]) -> list[int]:
    """Write every move, so that a run stopped part-way is finished by running it again.

    Every text is computed before any file is written, so a move the tool refuses writes
    nothing. The case records are written last, since `plan` reads them: a rerun after an
    interruption plans exactly the records not yet written, and the prior state, coverage
    register and deferrals written before them are already what that rerun computes.
    """
    pending = [move for move in moves if not adopted(move)]
    rewritten = {move.n: rewrite(move) for move in pending}
    register = COVERAGE.read_text(encoding="utf-8")
    covered = coverage(pending, register) if pending else register
    deferred = deferrals(DEFERRALS.read_text(encoding="utf-8"), _cited(rewritten))
    for day in sorted({houses.adopted_on(move.n) for move in pending}):
        retain_history(
            day, {move.n: move.text for move in pending if houses.adopted_on(move.n) == day}
        )
    _write(COVERAGE, covered)
    _write(DEFERRALS, deferred)
    for move in pending:
        _write(select_houses.case_path(move.n), rewritten[move.n])
    return [move.n for move in pending]


def check() -> list[str]:
    """Every count `upper_bound_houses` draws is at its house in the case and coverage."""
    problems = []
    coverage_data = safe_load(COVERAGE.read_text(encoding="utf-8"))
    sources = {str(s["id"]): s for s in coverage_data["sources"]}
    overrides = {int(e["n"]): e for e in coverage_data["selected_overrides"]}
    for n, result in sorted(houses.ADOPTED.items()):
        packing = _packing(_split(select_houses.case_path(n).read_text(encoding="utf-8"))[1])
        side = houses.side(n)
        source = houses.source_for(n)
        upper, verified = packing["reported_upper_bound"], packing["verified_upper_bound"]
        if upper.get("source_key") != source.key:
            problems.append(f"n={n}: reported source is not {result}'s {source.key}")
        for lane, bound in (("reported", upper), ("verified", verified)):
            if Fraction(str(bound.get("exact_form"))) != side:
                problems.append(f"n={n}: the {lane} exact form is not {result}'s exact side")
            shown = Fraction(Decimal(str(bound["value"])))
            if shown not in {side, Fraction(Decimal(select_houses.ceiling(side)))}:
                problems.append(f"n={n}: the {lane} value is not the side, exact or rounded up")
        override = overrides.get(n)
        if override is None or sources[override["source_id"]]["source_key"] != source.key:
            problems.append(f"n={n}: the coverage register does not select {source.key}")
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="list the moves, write nothing")
    mode.add_argument("--check", action="store_true", help="hold adopted cases to their houses")
    arguments = parser.parse_args(argv)
    if arguments.check:
        problems = check()
        for problem in problems:
            print(f"FAIL {problem}")
        if problems:
            return 1
        print(f"OK: {len(houses.ADOPTED)} adopted cases are at their houses")
        return 0
    moves = plan()
    if arguments.dry_run:
        for move in moves:
            print(f"n={move.n}: {move.house.result} {select_houses.ceiling(move.house.side)}")
        return 0
    written = write(moves)
    print(f"adopted {len(written)} houses: {', '.join(map(str, written)) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
