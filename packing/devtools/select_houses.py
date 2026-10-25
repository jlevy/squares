"""Derive each count's house from the register: the smallest validated exact side.

A case record's upper-bound lanes hold one certificate, its *house*. Until 11 October 2026
each import chose its houses by hand, in its own review's table, and the tables went
stale as later imports landed (`T-140`, `T-141` and the regularizations of `T-146`
changed several counts after the reviews that recommended a house were written). This
derives the house again from the record, so it cannot go stale. It applies the house
rule (packing/campaign/result-import.md, "The House Rule"): at every count the house is
the smallest packing whose certificate has passed stage 4, whoever found it, and nothing
in choosing it is a question for a person.

- **a candidate** is an upper-bound register entry at `V3` and `C3` or above whose
  `reviews` hold an `accepted` review covering it, citing a confirming evidence entry
  (`assurance: verified`, a passing replay or audit here) whose scope reaches the count,
  and whose source's exact side at the count rebuilds from its retained packet: a
  rational side through `upper_bound_reports.HOUSES`; an algebraic one where the packet's
  algebraic declaration states the count so (`algebraic_counts`, read by
  `algebraic_house_side`), or through `ALGEBRAIC_READERS` for a source that states only
  algebraic sides. One complete replay is what stage 4 asks, so a certificate decided on
  one exact route, as a number-field witness is today, is a candidate like any other;
- **the house** at a count is the candidate with the smallest exact side, where it is
  below the case record's verified ceiling. Sides and ceilings are compared exactly
  (`devtools.exact_sides`): a fraction, or a real algebraic number held as the one root of
  its minimal polynomial in a rational interval, a closed-form ceiling included. Ties go
  to the earlier finder, by the entry's `attribution.published`, and then to the earlier
  entry; the case record keeps its own house where nothing is below it. A ceiling whose
  exact form no reader here holds cannot be ordered, and `--check` fails on it as a defect
  of this code (`Selection.unordered`);
- **credit** follows the entry, except that a candidate listed in its entry's
  `regularizations` at the count leaves the packing with the finder of the result it
  names as `of`, and credits the regularizer with the regularization
  (epistemics.md, Parallel Projects and Their Credit);
- **an entry over several sources** is read at each count through the source of its
  confirming evidence there, the replay that decided the certificate at that count, which
  a reported atom under the same key must also state (`source_key_at`): T-181's replays
  decided 211 and 241 from issue 583's revision and 302 from issue 586's, though both
  reports state all three;
- **no result is held.** A house is adopted in the intake pass that validates it. Its
  adoption may follow in a later pull request of the same pass only where the count is
  staged in `PENDING_ADOPTION` with the open bead that adopts it, which `bead tree` holds
  open (`deferrals`); `--check` fails on a staged count the selection no longer moves.

**The records as written.** A record says what the selection was when its pass wrote it,
and `devtools.adopt_houses` replays each pass from the record it read. Passes before the
house rule ran under the rule of 15 October, which held PR #574's houses (T-174) for the
owner and left every algebraic certificate out for the owner's decision (RP-3 of the 14
October review of PR #574). `select(recorded=...)` gives that selection at each count
whose record a pass archived before `RULE_PASSES_FROM`, and leaves a staged count's staged
house out elsewhere, so that the records read as written until their counts are written
again. `LIFTED` keeps the lifted hold's words for those records and for nothing else.

Nothing here writes: `devtools.adopt_houses` writes the selection into the case records.

Usage, from ``packing/`` with the project interpreter::

    python -m devtools.select_houses            # the counts whose house moves
    python -m devtools.select_houses --all      # every count a candidate reaches
    python -m devtools.select_houses --json     # the same rows as JSON
    python -m devtools.select_houses --check    # fail where a case is above its house

``--check`` exits non-zero wherever a validated smaller packing is not the house: where a
case record's verified ceiling is above the derived house and the count is not staged,
which is what an unadopted, confirmed and reviewed certificate looks like. It also fails
on a staged count whose house the selection no longer names, on a ceiling it cannot order
exactly, and on an eligible entry with no exact reader that states a side below its case
(`check_standing.improvements`), which no candidate can carry. It names every eligible
entry it could not read and every staged count, with the bead that owes its adoption.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any, cast

from devtools import algebraic_witness_reports as algebraic_reports
from devtools import exact_sides
from devtools import upper_bound_reports as reports
from devtools.check_results import scope_values
from devtools.exact_sides import Side
from sqpack.assurance import confirming_execution
from sqpack.field import FieldPreconditionError
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FRONTIER = ROOT / "frontier"
RESULTS = FRONTIER / "results.yaml"
EVIDENCE = FRONTIER / "evidence.yaml"
#: The case corpus is ``n = 1..324``.
HORIZON = reports.HORIZON
CONFIRMED_RANK = 3
CONFIRMING_ORIGINS = frozenset({"replayed-here", "audited-here"})
DISPLAY_PLACES = 16
#: The owner set the house rule on 16 October 2026: "We should always be adopting the
#: smallest packing and then regularizing it." The records say it ended each wait, and
#: `default_drawings` dates it from here; a deferral of a count's runs since then is keyed
#: on the witness it defers, never on a day (`default_drawings.deferral_problems`).
RULE_SET_ON = "2026-10-16"
#: The adoption pass of 16 October (#657) ran under the rule of 15 October, and its prior
#: state is archived under that day, so the first pass that adopts under the house rule
#: is dated no earlier than this. It switches the replay of the records as written only.
RULE_PASSES_FROM = "2026-10-17"
#: The beads that own the adoptions the house rule stages here, each labelled
#: `regularization` and `validation` with stage 4's block and a row in the pass's backlog
#: (review A1 of #660): T-174's rational houses, and the algebraic ones, which wait for
#: the writer to take an algebraic side.
ADOPTION_BEAD = "think-3mry"
WRITER_BEAD = "think-ot5c"
#: Why a count's adoption waits for a later pull request, from a closed set: nothing
#: else stages one (packing/campaign/result-import.md, "The House Rule"). The pass
#: validated it in one pull request and adopts it in its next:
NEXT_PULL_REQUEST = "next pull request"
#: its regularization runs pass the item cap, and the counts they do not cover wait:
OVER_CAP = "over the item cap"
#: or the writer cannot write the house yet, the one code gap the rule names: since 23
#: October 2026 it writes an algebraic side, and the gap is one whose packet holds no derived
#: number-field fact and receipt for the count (`upper_bound_houses.FIELD_COUNTS`, `writable`).
NO_WRITER = "no writer"
STAGING_REASONS = (NEXT_PULL_REQUEST, OVER_CAP, NO_WRITER)


@dataclass(frozen=True)
class Hold:
    """A hold the house rule lifted: whose houses waited on the owner, why, from when, and
    the day the rule lifted it."""

    #: Whose houses, as prose names them: ``PR #574's``.
    whose: str
    #: Why they waited, as a clause after "since".
    why: str
    #: The day the hold was decided, ISO.
    since: str
    #: The day the house rule lifted it, ISO.
    until: str = RULE_SET_ON

    @property
    def reason(self) -> str:
        return f"{self.whose} houses were held for the owner, since {self.why}"


#: The holds the house rule lifted on 16 October 2026, kept only for the words of the
#: records written under them (`select(recorded=...)`, `adopt_houses.held_note`). On 15
#: October 2026 the coordinator of the 14 October intake held PR #574's houses (T-174) for
#: the owner, after the adoption lane measured what its 60 houses would cost: 18.5 MB more
#: of witnesses in a checkout, 5.8 MB more in every worker's snapshot, and about 440 CPU
#: seconds more in the pull request's sampled atlas rebuild. Size is met by OR-18's means,
#: never by holding a house (result-import.md, "The House Rule"). Delete an entry once no
#: record written under it remains.
LIFTED: dict[str, Hold] = {
    "T-174": Hold(
        whose="PR #574's",
        why=(
            "their witnesses would add about 18.5 MB to a checkout and their custody "
            "inputs about 5.8 MB to every worker's snapshot"
        ),
        since="2026-10-15",
    ),
}


@dataclass(frozen=True)
class Pending:
    """A count whose house moves, staged to a later pull request of the pass that adopts it."""

    #: The result the selection names as the count's house.
    house: str
    #: The open bead that owns the adoption.
    bead: str
    #: Why the adoption waits: one of `STAGING_REASONS`.
    why: str

    def __post_init__(self) -> None:
        if self.why not in STAGING_REASONS:
            raise ValueError(
                f"an adoption is staged for one of {', '.join(STAGING_REASONS)}, "
                f"not {self.why!r}"
            )


#: The counts the house rule moved when it was set, each staged to the adoption that
#: follows it: T-174's rational houses, which the lifted hold kept out, for the next pull
#: request, and its algebraic ones at 70, 153 and 207, which RP-3 kept out, for the
#: writer. There were 60 rational counts on 16 October 2026; the same day's adoption of
#: T-186 to T-190 (#657) took ten of them below T-174 (129, 146, 156, 175, 176, 204, 232,
#: 264, 271 and 303), which left 50. The adoption of 17 October 2026 (think-3mry)
#: took 37 rational counts off. Issue 639's exact algebraic sides (T-193), validated at
#: stage 4 on 16 October 2026 (#658), are smaller at twelve others: 88, 102, 123, 126,
#: 199, 258, 259, 266, 267, 292, 295 and 301. They are staged for the writer, as are its
#: four houses below T-186 at 175, 204, 232 and 302. At 236 Evan Daniel's issue 659
#: reports a side 2.02e-3 below T-174's; the adoption of 19 October 2026 took 236 to it
#: (T-218), which left T-174 no rational count staged. A pull request that validates a
#: smaller packing adopts it or stages its counts here with the bead that adopts them and
#: why (`STAGING_REASONS`); an adoption waits with its regularization runs, never apart
#: from them (`default_drawings.deferral_problems`). The pull request that adopts a count
#: takes it off, as the adoption of 19 October 2026 (think-jh4w) took 183 off once it
#: adopted Evan Daniel's original certificate there (T-220). A smaller validated packing
#: takes a staged count off too: the adoption of 20 October 2026 (think-xu4d) took 204
#: from T-193 to Francisco Couzo's issue 678 (T-223), below T-193's algebraic side there by
#: 2.04e-5, which leaves T-193 three houses below T-186, at 175, 232 and 302. The adoption
#: of 23 October 2026 (think-ot5c), once the writer wrote an algebraic side, took T-174's
#: three algebraic houses off at 70, 153 and 207, and T-193's at 102, 123, 258, 259, 295 and
#: 302, whose exact forms the packet retains and derives as number-field facts. T-193's
#: other eight wait for think-8ido to correct their regularization items
#: (`CORRECTIONS_OWED`), and 267 for its form, which the packet pins only; none of the nine
#: has a derived fact, so the writer cannot write them yet. At 267 the form, fetched from
#: the pin and equal to its digest, makes a degree-41 field witness of 4.53 MB in a checkout
#: and 1.88 MB as Git stores it, and its jobs are priced at about 2 CPU-hours each from a
#: 66-pair sample (14.6 CPU s), about 6 for the three and about 2 more at each atlas rebuild
#: of the witness: over the lanes' 2 CPU-hour limit on one run, so 267 waits, not run.
#: Evan Daniel's 268 (T-242), validated on 24 October 2026 with his 304, is smaller than
#: T-240's 268 by 4.48e-12, but the pass of 25 October that adopts his 304 also moves 268 to
#: T-240, and one day's archive holds one prior state a count: 268 moves to T-242 in the
#: pass's next pull request, dated 26 October (think-hx0e, whose H2 is think-3anz).
PENDING_ADOPTION: dict[int, Pending] = {
    **{
        n: Pending(house="T-193", bead=WRITER_BEAD, why=NO_WRITER)
        for n in (88, 126, 175, 199, 232, 266, 267, 292, 301)
    },
    268: Pending(house="T-242", bead="think-hx0e", why=NEXT_PULL_REQUEST),
}  # fmt: skip


@dataclass(frozen=True)
class Correction:
    """A regularization item the register states wrongly at a count, which the house's
    adoption waits on: the `of` the item names, the packing a stage 4 review measured the
    house to solve, and the open bead that corrects the item."""

    #: The result whose `regularizations` item is wrong at the count: the house.
    result: str
    #: The `of` the item names, which the measurement refutes.
    named: str
    #: The packing the review measured the house to solve, as its finding states it.
    measured: str
    #: The open bead that corrects the item.
    bead: str
    #: The review that measured it, repository-relative.
    measured_in: str


#: The bead that corrects T-193's regularization items, after the owner's Q2.
RE1_BEAD = "think-8ido"
#: The stage 4 review of issue 639, whose RE-1 measured T-193's forms pose by pose.
REVIEW_639 = "docs/project/reviews/review-2026-10-16-evand-exact-sides-639.md"

#: Regularization items owed a correction before their house is adopted (review B1 of
#: #658). At nine of T-193's counts the item names PingYou Ltd's (T-174) or Polkovskyi's
#: (T-186) refinement as the packing the form solves, and the 16 October review measured
#: it, centre by centre, to be the case's own house there (RE-1). The writer takes a
#: house's credit from that item (`regularized`, then `adopt_houses._regularization`), so
#: `adopt_houses.plan` refuses a house whose item still names `named`, and the adoption
#: waits on `bead`. `--check` fails once the item names anything else, so the entry goes
#: with the correction, and `deferrals` holds the bead open while it stands. Unlike
#: `PENDING_ADOPTION`, an entry here outlives the staging: the pull request that takes a
#: count off that list cannot write the uncorrected credit. An entry goes where T-193 will
#: not be the house: at 204 Francisco Couzo's issue 678 (T-223) is below it, adopted on 20
#: October 2026, so T-193's item there no longer waits on an adoption, and `--check`
#: refuses an entry whose count another result houses. The item itself, Polkovskyi's
#: T-186 named where the review measured T-162, stays think-8ido's to correct.
CORRECTIONS_OWED: dict[int, Correction] = {
    n: Correction(result="T-193", named=named, measured=measured, bead=RE1_BEAD,
                  measured_in=REVIEW_639)
    for n, named, measured in (
        (88, "T-174", "T-127"), (126, "T-174", "T-139"), (175, "T-186", "T-158"),
        (199, "T-174", "T-127"), (232, "T-186", "T-158"),
        (266, "T-174", "T-119"), (292, "T-174", "T-146"), (301, "T-174", "T-098"),
    )
}  # fmt: skip


def owed_correction(n: int, house: Candidate) -> Correction | None:
    """The correction `house`'s regularization item at `n` still waits for, if any: the
    entry in `CORRECTIONS_OWED` for its result whose wrong `of` the item still names."""
    owed = CORRECTIONS_OWED.get(n)
    if owed is None or owed.result != house.result or house.regularizes != owed.named:
        return None
    return owed


class SelectionError(ValueError):
    """The record does not support a selection: a reader or a case record is missing."""


def _rank(rung: object) -> int:
    text = str(rung or "")
    return int(text[1:]) if len(text) == 2 and text[1:].isdigit() else -1


@dataclass(frozen=True)
class Candidate:
    """One confirmed, reviewed register entry's exact side at one count."""

    result: str
    n: int
    side: Side
    source_key: str
    published: str
    report_evidence: tuple[str, ...]
    confirming_evidence: tuple[str, ...]
    regularizes: str | None

    @property
    def algebraic(self) -> bool:
        """Whether the side is irrational: the root of an irreducible polynomial."""
        return isinstance(self.side, exact_sides.Algebraic)


@dataclass(frozen=True)
class Case:
    """What a case record holds now: its verified ceiling and the source of its house.

    `verified` is the ceiling exactly: its rational `exact_form`, its printed value where
    it has none, or its closed form held as an isolated root. Where no reader here holds
    the closed form, `unread` says why and `verified` is the print plus one unit of its
    last place, at or above the ceiling however the print was rounded: a candidate below
    that cannot be ordered against the ceiling.
    """

    n: int
    verified: Side
    reported: Fraction
    source_key: str
    evidence: tuple[str, ...]
    unread: str | None = None

    @property
    def exact(self) -> bool:
        return self.unread is None


@dataclass(frozen=True)
class Selection:
    """The house at one count: the case's own, or the candidate that replaces it."""

    n: int
    case: Case
    house: Candidate | None
    candidates: tuple[Candidate, ...]
    #: Why the best candidate could not be ordered against the case's ceiling: a ceiling
    #: no reader here holds exactly. The case stays and `--check` fails until a reader is
    #: written; it is never left to a person.
    unordered: str | None = None
    #: The records as written only (`select(recorded=...)`): the candidates of `LIFTED`
    #: results below the house, or below the case where it stays.
    held: tuple[Candidate, ...] = ()
    #: The records as written only: the results whose certificate here is algebraic, with
    #: the source each is read from, which the rule of 15 October left out (RP-3).
    algebraic: tuple[tuple[str, str], ...] = ()

    @property
    def moves(self) -> bool:
        return self.house is not None

    @property
    def margin(self) -> Fraction:
        """How far the new house is below the case's verified ceiling, zero if it stays:
        exact where both are rational, else a lower bound within 2e-60."""
        if self.house is None:
            return Fraction(0)
        return exact_sides.lower_gap(self.case.verified, self.house.side)


def load_results() -> list[Mapping[str, Any]]:
    return list(_parsed(RESULTS.read_text(encoding="utf-8"))["results"])


def load_evidence() -> dict[str, Mapping[str, Any]]:
    entries = _parsed(EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    return {str(entry["id"]): entry for entry in entries}


@cache
def _parsed(text: str) -> Mapping[str, Any]:
    """A register parsed once for each text it has held; callers read it, never write."""
    return cast("Mapping[str, Any]", safe_load(text))


def _fraction(value: object) -> Fraction | None:
    text = str(value or "").strip()
    try:
        return Fraction(text) if text else None
    except ValueError:
        return None


def case_path(n: int) -> Path:
    return FRONTIER / f"n-{n:03d}.md"


def load_case(n: int) -> Case:
    path = case_path(n)
    if not path.is_file():
        raise SelectionError(f"n={n}: no case record at {path.relative_to(REPO)}")
    return parse_case(n, path.read_text(encoding="utf-8"))


@cache
def closed_form(value: str, form: str) -> tuple[Side | None, str | None]:
    """A closed-form ceiling held exactly, as the regularized layer holds `U`, or why not."""
    from devtools import regularize_evand  # noqa: PLC0415 -- SymPy, where a form needs it

    bound = regularize_evand.verified_bound({"verified_upper_bound": value, "exact_form": form})
    if bound is None:
        return None, "the case states no verified upper bound"
    try:
        side = exact_sides.of_bound(bound)
    except exact_sides.ExactSideError as error:
        # A form whose polynomial no route here decides irreducible, as at
        # sqrt(2) + sqrt(3) + sqrt(5), is held no more exactly than an unread one, and a
        # candidate below its print is unordered (review B3 of #660).
        return None, f"the form's polynomial is not held exactly: {error}"
    return side, None if side is not None else (bound.unread or "no reader holds the form")


def _above_print(printed: str) -> Fraction:
    """A printed decimal plus one unit of its last place, which no rounding of it passes."""
    places = len(printed.strip().partition(".")[2])
    return Fraction(printed.strip()) + Fraction(1, 10**places)


def parse_case(n: int, text: str) -> Case:
    """What the case record `text` holds at `n`."""
    packing = safe_load(text.split("---", 2)[1])["packing"]
    upper = packing["verified_upper_bound"]
    reported = packing["reported_upper_bound"]
    printed = _fraction(upper["value"])
    stated = _fraction(reported.get("exact_form")) or _fraction(reported["value"])
    if printed is None or stated is None:
        raise SelectionError(f"n={n}: the case's upper bounds are not numbers")
    form = upper.get("exact_form")
    verified: Side = printed
    unread: str | None = None
    if form is not None and str(form).strip():
        rational = _fraction(form)
        if rational is not None:
            verified = rational
        else:
            side, unread = closed_form(str(upper["value"]), str(form))
            verified = side if side is not None else _above_print(str(upper["value"]))
    return Case(
        n=n,
        verified=verified,
        reported=stated,
        source_key=str(reported.get("source_key") or ""),
        evidence=tuple(str(item) for item in upper.get("evidence") or ()),
        unread=unread,
    )


def accepted_review(entry: Mapping[str, Any]) -> bool:
    """An accepted review in the entry's `reviews` covers it."""
    return any(
        review.get("verdict") == "accepted" and entry["id"] in (review.get("covers") or ())
        for review in entry.get("reviews") or ()
    )


def confirming(
    entry: Mapping[str, Any], evidence: Mapping[str, Mapping[str, Any]], n: int
) -> tuple[str, ...]:
    """The entry's evidence that confirms a finite upper bound at `n` by a passing replay."""
    found = []
    for identifier in entry.get("evidence") or ():
        item = evidence.get(str(identifier))
        if (
            item
            and item.get("claim") == "upper-bound"
            and item.get("assurance") == "verified"
            and item.get("origin") in CONFIRMING_ORIGINS
            and confirming_execution(item)
            and item.get("replay_status") == "passed"
            and ("scope" not in item or n in scope_values(dict(item["scope"])))
        ):
            found.append(str(identifier))
    return tuple(found)


def reporting(
    entry: Mapping[str, Any],
    evidence: Mapping[str, Mapping[str, Any]],
    key: str,
    n: int | None = None,
) -> tuple[str, ...]:
    """The entry's own reported evidence: the source's report, under the entry's key, and,
    given a count, whose scope reaches it (PR 574 reports its rational and its algebraic
    certificates in two atoms)."""
    return tuple(
        str(identifier)
        for identifier in entry.get("evidence") or ()
        if (item := evidence.get(str(identifier)))
        and item.get("assurance") == "reported"
        and item.get("source_key") == key
        and (n is None or "scope" not in item or n in scope_values(dict(item["scope"])))
    )


def regularized(entry: Mapping[str, Any], n: int) -> str | None:
    """The result whose packing the entry regularizes at `n`, if it lists one."""
    for item in entry.get("regularizations") or ():
        if item.get("n") == n:
            return str(item["of"])
    return None


def eligible(entry: Mapping[str, Any]) -> bool:
    return (
        entry.get("kind") == "upper-bound"
        and _rank(entry.get("verification")) >= CONFIRMED_RANK
        and _rank(entry.get("confirmation")) >= CONFIRMED_RANK
        and accepted_review(entry)
    )


@cache
def _side(key: str, n: int) -> Fraction:
    return reports.house_side(key, n)


def source_key_at(
    entry: Mapping[str, Any], evidence: Mapping[str, Mapping[str, Any]], n: int
) -> str:
    """The source the entry's side at `n` is read from; empty where none is certain.

    An entry over one source is read through it. An entry over several is read, count by
    count, through the source of its confirming evidence at `n`, the replay that decided
    the certificate there, and only where that is one of the entry's keys, the only one,
    and a reported atom of the entry under it states the count too. The order of
    `source_keys` decides nothing: two reports may both state a count that one replay
    decided from one of them, as both of T-181's state 211 and 241 (review B of PR 614).
    """
    keys = [str(key) for key in entry["attribution"]["source_keys"]]
    if len(keys) == 1:
        return keys[0]
    decided = {
        str(evidence[identifier].get("source_key"))
        for identifier in confirming(entry, evidence, n)
    }
    if len(decided) != 1:
        return ""
    (key,) = decided
    if key not in keys or not reporting(entry, evidence, key, n):
        return ""
    return key


@cache
def algebraic_counts(key: str) -> frozenset[int]:
    """The counts at which the source's packet states only an algebraic certificate.

    Read from the packet's two declarations, not from its certificates: a count its
    algebraic declaration states (`algebraic_witness_reports`) and its rational one does
    not. PR #574's packet states T-174's sides at 70, 153, 207 and 302 so, each a root of
    an integer polynomial decided on one route.
    """
    packet = reports.import_packet(key)
    if packet is None or not (packet / algebraic_reports.DECLARATION).is_file():
        return frozenset()
    rational = {row["n"] for row in reports.load_declaration(packet)["certificates"]}
    stated = {row["n"] for row in algebraic_reports.load_declaration(packet)["witnesses"]}
    return frozenset(stated - rational)


@cache
def algebraic_house_side(key: str, n: int) -> Side:
    """The exact side the source's algebraic witness states at `n`, by its minimal
    polynomial (`exact_sides.of_field_element`)."""
    value, _degree = algebraic_side(key, n)
    return exact_sides.of_field_element(value)


#: Issue 639's exact sides (T-193), as the 16 October intake tabulated them from Evan
#: Daniel's `search/exact/cur/data/n-N.minpoly.json.gz`, each file held to its digest
#: (`review/exact_sides.py`): the side's integer polynomial and an interval about its one
#: root there, inside the source's own interval. The table is complete where the packet is
#: not, since the packet pins four of its files by digest only.
EVAND_EXACT_SIDES = ROOT / "campaign/issue-intake/upper-bounds-20261016/exact-sides.json"


@cache
def _evand_exact_rows() -> dict[int, Mapping[str, Any]]:
    table = json.loads(EVAND_EXACT_SIDES.read_text(encoding="utf-8"))
    return {int(row["n"]): row for row in table["rows"]}


@cache
def evand_exact_side(n: int) -> Side:
    """The exact side issue 639 states at `n`: the one root of its polynomial in the
    tabulated interval, which must lie within the source's, held by `exact_sides.algebraic`
    to an irreducible polynomial with exactly one root there."""
    row = _evand_exact_rows().get(n)
    if row is None:
        raise exact_sides.ExactSideError(f"issue 639 states no exact side at n = {n}")
    low, high = (Fraction(str(end)) for end in row["interval"])
    source_low, source_high = (Fraction(str(end)) for end in row["source_interval"])
    if not source_low <= low < high <= source_high:
        raise exact_sides.ExactSideError(
            f"n={n}: the tabulated interval is not within the source's"
        )
    coefficients = [Fraction(str(value)) for value in reversed(row["polynomial_low_to_high"])]
    return exact_sides.algebraic(coefficients, (low, high))


#: Sources whose packets state only algebraic sides, in a form `upper_bound_reports` has
#: no reader for, each with the reader of its exact side at a count. An eligible entry
#: whose source has no reader here or there is unread, and `--check` fails where it states
#: a side below its case (`unread_pending`): the cure is a reader, never a hold.
ALGEBRAIC_READERS: dict[str, Callable[[int], Side]] = {
    "[Daniel exact current records 2026-10-16]": evand_exact_side,
}


def _readable(key: str) -> bool:
    return key in reports.HOUSES or key in ALGEBRAIC_READERS


def exact_side(key: str, n: int) -> Side:
    """The exact side the source `key` states at `n`, rational or algebraic."""
    if key in ALGEBRAIC_READERS:
        return ALGEBRAIC_READERS[key](n)
    if n in algebraic_counts(key):
        return algebraic_house_side(key, n)
    return _side(key, n)


def candidates(
    results: Sequence[Mapping[str, Any]],
    evidence: Mapping[str, Mapping[str, Any]],
    *,
    since: str | None = None,
    unread: list[str] | None = None,
    unheld: list[str] | None = None,
) -> dict[int, list[Candidate]]:
    """Every confirmed, reviewed entry's exact side at every count it covers in the corpus.

    `since` keeps entries registered on or after a date, so a second pass can read only
    the entries a later intake added. An entry whose source has no exact reader is left
    to the case records and named in `unread`: those are entries adopted before the
    readers existed, whose sides the case records hold where they are the house. A side a
    reader cannot hold exactly (`exact_sides.ExactSideError`), or one in a field
    `sqpack.field` cannot certify (`FieldPreconditionError`), is no candidate and is
    named in `unheld`, which `--check` fails on: a defect of the reader, never a traceback
    (reviews B3 and C2 of #660).
    """
    found: dict[int, list[Candidate]] = {}
    for entry in results:
        if not eligible(entry) or (since and str(entry.get("registered")) < since):
            continue
        keys = list(entry["attribution"]["source_keys"])
        if len(keys) == 1 and not _readable(str(keys[0])):
            if unread is not None:
                unread.append(str(entry["id"]))
            continue
        missed = False
        for n in sorted(scope_values(dict(entry["scope"]))):
            if n > HORIZON:
                continue
            proof = confirming(entry, evidence, n)
            if not proof:
                continue
            key = source_key_at(entry, evidence, n)
            if not _readable(key):
                missed = True
                continue
            try:
                side = exact_side(key, n)
            except (exact_sides.ExactSideError, FieldPreconditionError) as error:
                if unheld is not None:
                    unheld.append(f"{entry['id']} at n = {n}: {error}")
                continue
            found.setdefault(n, []).append(
                Candidate(
                    result=str(entry["id"]),
                    n=n,
                    side=side,
                    source_key=key,
                    published=str(entry["attribution"].get("published") or ""),
                    report_evidence=reporting(entry, evidence, key, n),
                    confirming_evidence=proof,
                    regularizes=regularized(entry, n),
                )
            )
        if missed and unread is not None:
            unread.append(str(entry["id"]))
    return found


def precedence(candidate: Candidate) -> tuple[Side, str, int]:
    return candidate.side, candidate.published, int(candidate.result.removeprefix("T-"))


def _by_rule(n: int, case: Case, ranked: tuple[Candidate, ...]) -> Selection:
    """The house rule at one count: the smallest candidate, where it is below the case."""
    best = ranked[0] if ranked else None
    if best is None or not best.side < case.verified:
        return Selection(n=n, case=case, house=None, candidates=ranked)
    if case.unread is not None:
        # Below the ceiling's print plus a unit, the candidate may lie on either side of the
        # ceiling, and no reader here holds the ceiling to decide which.
        return Selection(n=n, case=case, house=None, candidates=ranked, unordered=case.unread)
    return Selection(n=n, case=case, house=best, candidates=ranked)


def _as_recorded(n: int, case: Case, ranked: tuple[Candidate, ...], day: str) -> Selection:
    """The selection a record written on `day` was written under (`select`)."""
    if day >= RULE_PASSES_FROM:
        staged = PENDING_ADOPTION.get(n)
        kept = tuple(c for c in ranked if staged is None or c.result != staged.house)
        return _by_rule(n, case, kept)
    # The rule of 15 October: an algebraic certificate of a packet a rational reader
    # reads was left out and named, a source with no rational reader was unread, and the
    # held results were left out, the next candidate taking the house.
    rational = tuple(c for c in ranked if not c.algebraic)
    named = tuple(
        (c.result, c.source_key)
        for c in ranked
        if c.algebraic and c.source_key in reports.HOUSES
    )
    free = [c for c in rational if c.result not in LIFTED]
    best = free[0] if free else None
    house = best if best is not None and best.side < case.verified else None
    bar = house.side if house is not None else case.verified
    return Selection(
        n=n,
        case=case,
        house=house,
        candidates=rational,
        held=tuple(c for c in rational if c.result in LIFTED and c.side < bar),
        algebraic=named,
    )


def select(
    results: Sequence[Mapping[str, Any]] | None = None,
    evidence: Mapping[str, Mapping[str, Any]] | None = None,
    *,
    since: str | None = None,
    cases: Mapping[int, Case] | None = None,
    unread: list[str] | None = None,
    recorded: Mapping[int, str] | None = None,
    unheld: list[str] | None = None,
) -> dict[int, Selection]:
    """The house at every count a candidate reaches, against the case records as they are.

    By default this is the house rule. `recorded` maps counts to the day their record was
    last written, for replaying the records as written: at a count written before
    `RULE_PASSES_FROM` the selection is the rule of 15 October's, and at any other staged
    count the staged house is left out, as its record does not yet name it.
    """
    results = load_results() if results is None else results
    evidence = load_evidence() if evidence is None else evidence
    selections: dict[int, Selection] = {}
    found_at = candidates(results, evidence, since=since, unread=unread, unheld=unheld)
    for n, found in sorted(found_at.items()):
        case = cases[n] if cases is not None else load_case(n)
        ranked = tuple(sorted(found, key=precedence))
        if recorded is not None and n in recorded:
            selections[n] = _as_recorded(n, case, ranked, recorded[n])
        else:
            selections[n] = _by_rule(n, case, ranked)
    return selections


@cache
def algebraic_side(key: str, n: int) -> tuple[Any, int]:
    """The exact side the source's algebraic witness states at `n`, and its field's degree.

    A field element (`algebraic_witness_reports.side_of`); `algebraic_house_side` holds it
    as an isolated root, which is how a candidate's side is compared.
    """
    packet = reports.import_packet(key)
    if packet is None:
        raise SelectionError(f"{key}: no packet to read an algebraic side from")
    witness = algebraic_reports.read_facts(packet, {n})[n]
    rows = algebraic_reports.load_declaration(packet)["witnesses"]
    degree = next(int(row["degree"]) for row in rows if row["n"] == n)
    return algebraic_reports.side_of(witness), degree


def algebraic_below(key: str, n: int, side: Side) -> bool:
    """Whether the algebraic side at `n` is below `side`, decided exactly."""
    return exact_sides.compare(algebraic_house_side(key, n), side) < 0


def algebraic_margin(key: str, n: int, side: Side) -> Fraction:
    """How far the algebraic side at `n` is below `side`, from a tight enclosure."""
    if isinstance(side, exact_sides.Algebraic):
        return exact_sides.lower_gap(side, algebraic_house_side(key, n))
    value, _degree = algebraic_side(key, n)
    _low, high = algebraic_reports.enclosure(value, 60)
    return side - high


def unread_pending(unread: Sequence[str]) -> dict[str, list[int]]:
    """The unread entries that state a bound below their case: adoptions nothing here sees.

    An eligible entry without an exact reader is never a candidate, so a confirmed and
    reviewed side it states below a case would stay pending without this.
    """
    from devtools import check_standing  # noqa: PLC0415
    from devtools import render_recent_results as view  # noqa: PLC0415

    if not unread:
        return {}
    records = view.load_records()
    entries = {str(entry["id"]): entry for entry in records.register.results}
    pending = {}
    for identifier in unread:
        better = check_standing.improvements(entries[identifier], records)
        if better:
            pending[identifier] = sorted({finding.n for finding in better})
    return pending


def unread_unordered(unread: Sequence[str]) -> dict[str, list[int]]:
    """The unread entries whose stated upper bound meets their case's ceiling only by
    print, at each count it does.

    `check_standing.relation` reads two spans that overlap as equal, which orders nothing:
    an entry with no exact reader whose print overlaps the ceiling may be below it or not.
    The rule orders sides exactly or fails (packing/campaign/result-import.md, "The House
    Rule"), so `--check` fails on each until a reader holds the entry's side (review A10
    of #660). An exact equality, a print that is the ceiling, is a tie and passes.
    """
    from devtools import check_standing as standing  # noqa: PLC0415
    from devtools import render_recent_results as view  # noqa: PLC0415

    if not unread:
        return {}
    records = view.load_records()
    entries = {str(entry["id"]): entry for entry in records.register.results}
    found: dict[str, set[int]] = {}
    for identifier in unread:
        entry = entries[identifier]
        lanes = (
            ("reported",)
            if str(entry.get("confirmation")) in standing.UNREPLAYED
            else (
                "reported",
                "verified",
            )
        )
        findings = standing.findings(entry, records)
        claimed = standing.directions(entry, findings)
        for finding in findings:
            if finding.direction != standing.UPPER or finding.direction not in claimed:
                continue
            for lane in lanes:
                if getattr(finding, lane) != standing.EQUAL:
                    continue
                bound = records.cases[finding.n].get(f"{lane}_upper_bound")
                if not bound:
                    continue
                floor, ceiling = view.span(bound)
                stated = finding.stated
                if not (stated.slack == 0 and floor == ceiling == stated.value):
                    found.setdefault(identifier, set()).add(finding.n)
    return {identifier: sorted(counts) for identifier, counts in found.items()}


def correction_problems(selections: Mapping[int, Selection]) -> list[str]:
    """Why `CORRECTIONS_OWED` no longer matches the register: an entry whose count's house
    is another result's, or whose item no longer names the refuted `of`, which means the
    correction has landed and the entry goes. Read against the whole register's selection,
    which reaches every count a candidate does."""
    problems = []
    for n, owed in sorted(CORRECTIONS_OWED.items()):
        house = selections[n].house if n in selections else None
        if house is None or house.result != owed.result:
            problems.append(
                f"FAIL: n={n} owes {owed.result}'s regularization a correction ({owed.bead}), "
                f"but the house is {house.result if house else 'the case'}'s; take it off "
                "CORRECTIONS_OWED"
            )
        elif house.regularizes != owed.named:
            problems.append(
                f"FAIL: n={n}: {owed.result}'s regularization item names "
                f"{house.regularizes or 'no packing'}, not {owed.named}, so the correction "
                f"{owed.bead} owed has landed; take it off CORRECTIONS_OWED"
            )
    return problems


def deferrals() -> list[tuple[str, str]]:
    """Each staged adoption as (where, the bead alias), for `devtools.check_bead_tree`,
    which holds the bead open while the count is staged."""
    return [
        *(
            (f"select_houses.PENDING_ADOPTION n={n} ({pending.house})", pending.bead)
            for n, pending in sorted(PENDING_ADOPTION.items())
        ),
        *(
            (f"select_houses.CORRECTIONS_OWED n={n} ({owed.result} of {owed.named})", owed.bead)
            for n, owed in sorted(CORRECTIONS_OWED.items())
        ),
    ]


def ceiling(side: Side, places: int = DISPLAY_PLACES) -> str:
    """The side rounded up at `places` decimals, as a case record prints an exact side."""
    return exact_sides.ceiling(side, places)


def _sci(value: Fraction) -> str:
    return f"{float(value):.2e}"


def row(selection: Selection) -> dict[str, Any]:
    house = selection.house
    staged = PENDING_ADOPTION.get(selection.n)
    return {
        "n": selection.n,
        "case_source": selection.case.source_key,
        "case_side": ceiling(selection.case.verified),
        "house": house.result if house else None,
        "house_side": ceiling(house.side) if house else None,
        "house_exact": exact_sides.literal(house.side) if house else None,
        "margin": reports.legacy.literal(selection.margin) if house else None,
        "regularizes": house.regularizes if house else None,
        "staged": staged.bead if staged is not None and house is not None else None,
        "staged_why": staged.why if staged is not None and house is not None else None,
        "unordered": selection.unordered,
        "candidates": [
            {
                "result": candidate.result,
                "side": ceiling(candidate.side),
                "published": candidate.published,
            }
            for candidate in selection.candidates
        ],
    }


def table(selections: Mapping[int, Selection], *, everything: bool) -> str:
    lines = [f"{'n':>4}  {'case house':<44} {'new house':<9} {'side':<20} margin   credit"]
    for n, selection in sorted(selections.items()):
        if not (selection.moves or selection.unordered or everything):
            continue
        house = selection.house
        old = f"{selection.case.source_key} {ceiling(selection.case.verified)}"
        if selection.unordered:
            best = selection.candidates[0]
            lines.append(
                f"{n:>4}  {old:<44} {'(stays)':<9} {ceiling(best.side):<20} "
                f"unordered: {selection.unordered}"
            )
            continue
        if house is None:
            lines.append(f"{n:>4}  {old:<44} {'(stays)':<9}")
            continue
        notes = [f"packing of {house.regularizes}"] if house.regularizes else []
        if house.algebraic:
            notes.append("algebraic")
        if (staged := PENDING_ADOPTION.get(n)) is not None and staged.house == house.result:
            notes.append(f"staged ({staged.why}): {staged.bead}")
        if (owed := owed_correction(n, house)) is not None:
            notes.append(f"after {owed.bead}, which corrects the packing to {owed.measured}")
        lines.append(
            f"{n:>4}  {old:<44} {house.result:<9} {ceiling(house.side):<20} "
            f"{_sci(selection.margin):<8} {'; '.join(notes)}"
        )
    moving = sum(selection.moves for selection in selections.values())
    lines.append(f"{moving} of {len(selections)} counts move")
    return "\n".join(lines)


def writable(house: Candidate) -> bool:
    """Whether `adopt_houses` can write the house: a rational side, or an algebraic one whose
    derived number-field fact and receipt `upper_bound_houses` reads (`FIELD_COUNTS`)."""
    from devtools import upper_bound_houses as houses  # noqa: PLC0415 -- the writer's half

    found = houses.writable_source(
        house.result, house.n, house.source_key, algebraic=house.algebraic
    )
    return found is not None or not house.algebraic


def check(selections: Mapping[int, Selection]) -> list[str]:
    """Why the record breaks the house rule: one line a failure, empty where it holds."""
    moving = {n: selection for n, selection in selections.items() if selection.moves}
    unstaged = sorted(n for n in moving if n not in PENDING_ADOPTION)
    problems = []
    if unstaged:
        problems.append(
            "FAIL: a validated smaller packing is not the house, and no pull request has "
            f"staged its adoption, at n = {unstaged}"
        )
    for n, pending in sorted(PENDING_ADOPTION.items()):
        selection = moving.get(n)
        if selection is None:
            problems.append(
                f"FAIL: n={n} is staged for {pending.house}'s adoption ({pending.bead}), but "
                "the selection moves nothing there; take it off PENDING_ADOPTION"
            )
        elif selection.house is not None and selection.house.result != pending.house:
            problems.append(
                f"FAIL: n={n} is staged for {pending.house}, but the house is "
                f"{selection.house.result}; stage that, or adopt it"
            )
        elif selection.house is not None and writable(selection.house) == (
            pending.why == NO_WRITER
        ):
            # The writer's gap stages a house the writer cannot write and nothing else
            # (review A1 of #660): an algebraic side no derived number-field fact holds.
            problems.append(
                f"FAIL: n={n} is staged as {pending.why!r} under {pending.bead}, but "
                + (
                    "the writer writes it, so stage it for the next pull request"
                    if writable(selection.house)
                    else f"the writer cannot write it: stage it as {NO_WRITER!r} under the "
                    "writer's bead"
                )
            )
    unordered = sorted(n for n, selection in selections.items() if selection.unordered)
    if unordered:
        problems.append(
            "FAIL: a candidate is below the print of a ceiling no reader here holds "
            f"exactly, at n = {unordered}; write the reader (a defect, not a question)"
        )
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    parser.add_argument("--all", action="store_true", help="every count a candidate reaches")
    parser.add_argument("--json", action="store_true", help="print the rows as JSON")
    parser.add_argument("--check", action="store_true", help="fail where a house would move")
    parser.add_argument("--since", help="only entries registered on or after this date")
    arguments = parser.parse_args(argv)
    if arguments.check and arguments.since:
        # A narrowed selection leaves out the very entries a count is staged for, and would
        # advise unstaging every one of them (review A9 of #660).
        parser.error("--check judges the whole register; --since narrows a listing only")
    unread: list[str] = []
    unheld: list[str] = []
    selections = select(since=arguments.since, unread=unread, unheld=unheld)
    if arguments.json:
        rows = [row(s) for s in selections.values() if s.moves or arguments.all]
        print(json.dumps(rows, indent=2))
    else:
        print(table(selections, everything=arguments.all))
    if not arguments.check:
        return 0
    problems = [*check(selections), *correction_problems(selections)]
    for line in problems:
        print(line)
    staged: dict[str, list[int]] = {}
    for n, pending in sorted(PENDING_ADOPTION.items()):
        staged.setdefault(f"{pending.house} under {pending.bead} ({pending.why})", []).append(n)
    for owner, counts in staged.items():
        print(f"staged adoption, {owner}: n = {counts}")
    owing: dict[str, list[int]] = {}
    for n, owed in sorted(CORRECTIONS_OWED.items()):
        owing.setdefault(f"{owed.result}'s regularization items under {owed.bead}", []).append(
            n
        )
    for owner, counts in owing.items():
        print(f"adoption waits for a correction of {owner}: n = {counts}")
    print(
        f"unread, eligible but with no exact reader: {', '.join(unread) if unread else 'none'}"
    )
    pending_unread = unread_pending(unread)
    for identifier, counts in pending_unread.items():
        print(
            f"FAIL: {identifier} has no exact reader and states a side below its case "
            f"at n = {counts}, pending an adoption this cannot select"
        )
    overlapping = unread_unordered(unread)
    for identifier, counts in overlapping.items():
        print(
            f"FAIL: {identifier} has no exact reader, and its print meets its case's "
            f"ceiling only by overlap at n = {counts}: write the reader (a defect, not a "
            "question)"
        )
    for line in unheld:
        print(f"FAIL: no exact side for {line}; fix the reader (a defect, not a question)")
    return 1 if problems or pending_unread or overlapping or unheld else 0


if __name__ == "__main__":
    sys.exit(main())
