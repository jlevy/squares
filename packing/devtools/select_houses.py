"""Derive each count's house from the register: the smallest confirmed and reviewed side.

A case record's upper-bound lanes hold one certificate, its *house*. Until 11 October 2026
each import chose its houses by hand, in its own review's table, and the tables went
stale as later imports landed (`T-140`, `T-141` and the regularizations of `T-146`
changed several counts after the reviews that recommended a house were written). This
derives the house again from the record, so it cannot go stale:

- **a candidate** is an upper-bound register entry at `V3` and `C3` or above whose
  `reviews` hold an `accepted` review covering it, citing a confirming evidence entry
  (`assurance: verified`, a passing replay or audit here) whose scope reaches the count,
  and whose source's exact side at the count rebuilds from its retained packet through
  `upper_bound_reports.HOUSES`;
- **the house** at a count is the candidate with the smallest exact side, compared
  exactly, where it is below the case record's verified ceiling (a ceiling that is not
  rational is held by its display, and a candidate below that is left to a human, since
  it may lie between the two); ties go to the earlier
  finder, by the entry's `attribution.published`, and then to the earlier entry; the case
  record keeps its own house where nothing is below it;
- **credit** follows the entry, except that a candidate listed in its entry's
  `regularizations` at the count leaves the packing with the finder of the result it
  names as `of`, and credits the regularizer with the regularization
  (epistemics.md, Parallel Projects and Their Credit);
- **an entry over several sources** is read at each count through the source of its
  confirming evidence there, the replay that decided the certificate at that count, which
  a reported atom under the same key must also state (`source_key_at`): T-181's replays
  decided 211 and 241 from issue 583's revision and 302 from issue 586's, though both
  reports state all three;
- **an algebraic certificate is no candidate.** A house reader rebuilds a rational side,
  and a count at which the source's packet states only an algebraic witness
  (`algebraic_counts`) is left out of the selection and named, not read: its side cannot
  be held exactly against a rational ceiling here, and adopting it would rest a verified
  ceiling on one route, which the owner decides (RP-3 of the 14 October review of PR
  #574);
- **a held result** (`HELD`) is left out of the selection, and the house is the best of
  the rest: where a held result is below that house, or below the case where the case
  stays, the selection names it (`Selection.held`) and the count is reported as held, for
  the owner, rather than as an adoption this has missed. If the owner releases the result,
  those counts move again, to it.

Nothing here writes: `devtools.adopt_houses` writes the selection into the case records.

Usage, from ``packing/`` with the project interpreter::

    python -m devtools.select_houses            # the counts whose house moves
    python -m devtools.select_houses --all      # every count a candidate reaches
    python -m devtools.select_houses --json     # the same rows as JSON
    python -m devtools.select_houses --check    # fail where a case is above its house

``--check`` exits non-zero where a case record's verified ceiling is above the derived
house, which is what an unadopted, confirmed and reviewed certificate looks like. It also
fails where it cannot tell: a candidate below the rounded-up display of an algebraic
ceiling, which a human orders, and an eligible entry with no exact reader that states a
side below its case (`check_standing.improvements`), which no candidate can carry. It
names every eligible entry it could not read, every algebraic count it left out and every
count a held result holds.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any, cast

from devtools import algebraic_witness_reports as algebraic_reports
from devtools import upper_bound_reports as reports
from devtools.check_results import scope_values
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


@dataclass(frozen=True)
class Hold:
    """Why a result's houses wait on the owner, and since when."""

    #: Whose houses, as prose names them: ``PR #574's``.
    whose: str
    #: Why they wait, as a clause after "are held for the owner:".
    why: str
    #: The day the hold was decided, ISO.
    since: str

    @property
    def reason(self) -> str:
        return f"{self.whose} houses are held for the owner: {self.why}"


#: Results whose houses wait on the owner, with why. A held result is left out of the
#: selection: the house at each of its counts is the best of the other candidates, and
#: the case records name the held result as smaller and waiting (`Selection.held`). On 15
#: October 2026 the coordinator of the 14 October intake held PR #574's houses (T-174) for
#: the owner, after the adoption lane measured what its 60 houses would cost: 18.5 MB more
#: of witnesses in Git (OR-18), 5.8 MB more in every worker's snapshot, and about 440 CPU
#: seconds more in the pull request's sampled atlas rebuild. The same day, after reviews A
#: and B of PR 614, the coordinator decided that a hold skips only the held entry, so the
#: next candidate takes the house where it is below the case (at 10 counts, by 1.1e-19 to
#: 1.42e-2); those counts move again, to T-174, if the owner adopts its houses.
HELD: dict[str, Hold] = {
    "T-174": Hold(
        whose="PR #574's",
        why=(
            "their witnesses would add about 18.5 MB to Git (OR-18) and their custody "
            "inputs about 5.8 MB to every worker's snapshot"
        ),
        since="2026-10-15",
    ),
}


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
    side: Fraction
    source_key: str
    published: str
    report_evidence: tuple[str, ...]
    confirming_evidence: tuple[str, ...]
    regularizes: str | None


@dataclass(frozen=True)
class Case:
    """What a case record holds now: its verified ceiling and the source of its house.

    `exact` says whether `verified` is the ceiling itself, a rational `exact_form`. An
    algebraic ceiling is held by its display, rounded up at sixteen places, and a
    candidate between the two cannot be ordered against it here.
    """

    n: int
    verified: Fraction
    reported: Fraction
    source_key: str
    evidence: tuple[str, ...]
    exact: bool = True


@dataclass(frozen=True)
class Selection:
    """The house at one count: the case's own, or the candidate that replaces it."""

    n: int
    case: Case
    house: Candidate | None
    candidates: tuple[Candidate, ...]
    #: The best candidate is below the display of a ceiling that is not rational, so
    #: whether it is below the ceiling is not decided here: the case stays, and a human
    #: decides.
    undecided: bool = False
    #: The candidates of `HELD` results below the house, or below the case where it
    #: stays: left out of the selection until the owner releases them.
    held: tuple[Candidate, ...] = ()
    #: The results whose certificate at this count is algebraic, with the source each is
    #: read from: left out of the selection, which the owner decides (RP-3).
    algebraic: tuple[tuple[str, str], ...] = ()

    @property
    def moves(self) -> bool:
        return self.house is not None

    @property
    def margin(self) -> Fraction:
        """How far the new house is below the case's verified ceiling; zero if it stays."""
        return self.case.verified - self.house.side if self.house else Fraction(0)


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


def parse_case(n: int, text: str) -> Case:
    """What the case record `text` holds at `n`."""
    packing = safe_load(text.split("---", 2)[1])["packing"]
    upper = packing["verified_upper_bound"]
    reported = packing["reported_upper_bound"]
    exact = _fraction(upper.get("exact_form"))
    verified = exact if exact is not None else _fraction(upper["value"])
    stated = _fraction(reported.get("exact_form")) or _fraction(reported["value"])
    if verified is None or stated is None:
        raise SelectionError(f"n={n}: the case's upper bounds are not numbers")
    return Case(
        n=n,
        verified=verified,
        reported=stated,
        source_key=str(reported.get("source_key") or ""),
        evidence=tuple(str(item) for item in upper.get("evidence") or ()),
        exact=exact is not None,
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


def candidates(
    results: Sequence[Mapping[str, Any]],
    evidence: Mapping[str, Mapping[str, Any]],
    *,
    since: str | None = None,
    unread: list[str] | None = None,
    algebraic: list[tuple[str, int]] | None = None,
) -> dict[int, list[Candidate]]:
    """Every confirmed, reviewed entry's exact side at every count it covers in the corpus.

    `since` keeps entries registered on or after a date, so a second pass can read only
    the entries a later intake added. An entry whose source has no exact reader is left
    to the case records and named in `unread`: those are entries adopted before the
    readers existed, whose sides the case records hold where they are the house. A count
    whose certificate is algebraic is left out and named in `algebraic`, as the entry and
    the count.
    """
    found: dict[int, list[Candidate]] = {}
    for entry in results:
        if not eligible(entry) or (since and str(entry.get("registered")) < since):
            continue
        keys = list(entry["attribution"]["source_keys"])
        if len(keys) == 1 and str(keys[0]) not in reports.HOUSES:
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
            if key not in reports.HOUSES:
                missed = True
                continue
            if n in algebraic_counts(key):
                if algebraic is not None:
                    algebraic.append((str(entry["id"]), n))
                continue
            found.setdefault(n, []).append(
                Candidate(
                    result=str(entry["id"]),
                    n=n,
                    side=_side(key, n),
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


def precedence(candidate: Candidate) -> tuple[Fraction, str, int]:
    return candidate.side, candidate.published, int(candidate.result.removeprefix("T-"))


def select(
    results: Sequence[Mapping[str, Any]] | None = None,
    evidence: Mapping[str, Mapping[str, Any]] | None = None,
    *,
    since: str | None = None,
    cases: Mapping[int, Case] | None = None,
    unread: list[str] | None = None,
    algebraic: list[tuple[str, int]] | None = None,
    held: Mapping[str, Hold] | None = None,
) -> dict[int, Selection]:
    """The house at every count a candidate reaches, against the case records as they are.

    A result in `held` (by default `HELD`) is left out: the house is the best of the other
    candidates, and the held candidates below it, or below the case where it stays, are
    named in `Selection.held`. A case whose ceiling is not rational moves only where its
    best candidate is not below the ceiling's display; below it, the selection is
    `undecided` and the case stays.
    """
    results = load_results() if results is None else results
    evidence = load_evidence() if evidence is None else evidence
    holds: Mapping[str, Hold] = HELD if held is None else held
    left_out: list[tuple[str, int]] = [] if algebraic is None else algebraic
    selections: dict[int, Selection] = {}
    found_at = candidates(results, evidence, since=since, unread=unread, algebraic=left_out)
    entries = {str(entry["id"]): entry for entry in results}
    stated: dict[int, list[tuple[str, str]]] = {}
    for result, n in left_out:
        stated.setdefault(n, []).append((result, source_key_at(entries[result], evidence, n)))
    for n, found in sorted(found_at.items()):
        case = cases[n] if cases is not None else load_case(n)
        ranked = tuple(sorted(found, key=precedence))
        free = [candidate for candidate in ranked if candidate.result not in holds]
        best = free[0] if free else None
        below = best is not None and best.side < case.verified
        house = best if below and case.exact else None
        bar = house.side if house is not None else case.verified
        selections[n] = Selection(
            n=n,
            case=case,
            house=house,
            candidates=ranked,
            undecided=below and not case.exact,
            held=tuple(c for c in ranked if c.result in holds and c.side < bar),
            algebraic=tuple(stated.get(n, ())),
        )
    return selections


@cache
def algebraic_side(key: str, n: int) -> tuple[Any, int]:
    """The exact side the source's algebraic witness states at `n`, and its field's degree.

    A field element (`algebraic_witness_reports.side_of`), which `algebraic_below` orders
    against a rational side exactly; never a candidate's side.
    """
    packet = reports.import_packet(key)
    if packet is None:
        raise SelectionError(f"{key}: no packet to read an algebraic side from")
    witness = algebraic_reports.read_facts(packet, {n})[n]
    rows = algebraic_reports.load_declaration(packet)["witnesses"]
    degree = next(int(row["degree"]) for row in rows if row["n"] == n)
    return algebraic_reports.side_of(witness), degree


def algebraic_below(key: str, n: int, side: Fraction) -> bool:
    """Whether the algebraic side at `n` is below `side`, decided exactly."""
    value, _degree = algebraic_side(key, n)
    return algebraic_reports.against(value, reports.exact_span(side)) == "below"


def algebraic_margin(key: str, n: int, side: Fraction) -> Fraction:
    """How far the algebraic side at `n` is below `side`, from a tight enclosure."""
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


def ceiling(side: Fraction, places: int = DISPLAY_PLACES) -> str:
    """The side rounded up at `places` decimals, as a case record prints an exact side."""
    scaled = side * 10**places
    whole = -(-scaled.numerator // scaled.denominator)
    text = str(whole).rjust(places + 1, "0")
    return f"{text[:-places]}.{text[-places:]}"


def _sci(value: Fraction) -> str:
    return f"{float(value):.2e}"


def row(selection: Selection) -> dict[str, Any]:
    house = selection.house
    return {
        "n": selection.n,
        "case_source": selection.case.source_key,
        "case_side": ceiling(selection.case.verified),
        "house": house.result if house else None,
        "house_side": ceiling(house.side) if house else None,
        "house_exact": reports.legacy.literal(house.side) if house else None,
        "margin": reports.legacy.literal(selection.margin) if house else None,
        "regularizes": house.regularizes if house else None,
        "held": [candidate.result for candidate in selection.held],
        "undecided": selection.undecided,
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
        if not (selection.moves or selection.undecided or selection.held or everything):
            continue
        house = selection.house
        old = f"{selection.case.source_key} {ceiling(selection.case.verified)}"
        if selection.held and house is None:
            best = selection.held[0]
            lines.append(
                f"{n:>4}  {old:<44} {'(held)':<9} {ceiling(best.side):<20} "
                f"held: {best.result}'s houses wait on the owner"
            )
            continue
        if selection.undecided:
            best = selection.candidates[0]
            lines.append(
                f"{n:>4}  {old:<44} {'(stays)':<9} {ceiling(best.side):<20} "
                f"undecided: {best.result} is below the display of an algebraic ceiling"
            )
            continue
        if house is None:
            lines.append(f"{n:>4}  {old:<44} {'(stays)':<9}")
            continue
        credit = f"packing of {house.regularizes}" if house.regularizes else ""
        if selection.held:
            credit = f"{credit}; held below it: {', '.join(c.result for c in selection.held)}"
        lines.append(
            f"{n:>4}  {old:<44} {house.result:<9} {ceiling(house.side):<20} "
            f"{_sci(selection.margin):<8} {credit}"
        )
    moving = sum(selection.moves for selection in selections.values())
    lines.append(f"{moving} of {len(selections)} counts move")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    parser.add_argument("--all", action="store_true", help="every count a candidate reaches")
    parser.add_argument("--json", action="store_true", help="print the rows as JSON")
    parser.add_argument("--check", action="store_true", help="fail where a house would move")
    parser.add_argument("--since", help="only entries registered on or after this date")
    arguments = parser.parse_args(argv)
    unread: list[str] = []
    algebraic: list[tuple[str, int]] = []
    selections = select(since=arguments.since, unread=unread, algebraic=algebraic)
    if arguments.json:
        rows = [row(s) for s in selections.values() if s.moves or arguments.all]
        print(json.dumps(rows, indent=2))
    else:
        print(table(selections, everything=arguments.all))
    if arguments.check:
        failed = False
        moving = [n for n, selection in selections.items() if selection.moves]
        if moving:
            print(f"FAIL: a confirmed, reviewed side is below the case at n = {moving}")
            failed = True
        undecided = [n for n, selection in selections.items() if selection.undecided]
        if undecided:
            print(
                "FAIL: a confirmed, reviewed side is below the display of an algebraic "
                f"ceiling, undecided here, at n = {undecided}"
            )
            failed = True
        print(
            "unread, eligible but with no exact reader: "
            f"{', '.join(unread) if unread else 'none'}"
        )
        print(
            "left out, an algebraic certificate the owner decides: "
            f"{', '.join(f'{r} at {n}' for r, n in algebraic) if algebraic else 'none'}"
        )
        waiting = [n for n, selection in selections.items() if selection.held]
        if waiting:
            results = sorted({c.result for n in waiting for c in selections[n].held})
            print(f"held for the owner ({', '.join(results)}): n = {waiting}")
        for identifier, counts in unread_pending(unread).items():
            print(
                f"FAIL: {identifier} has no exact reader and states a side below its case "
                f"at n = {counts}, pending an adoption this cannot select"
            )
            failed = True
        return 1 if failed else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
