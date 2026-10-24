"""Current registered contributions, kept separate from unchanged authored Results.

A result is counted once if any of its facets remains current. Non-bound families use
this register's explicit lifecycle: whole supersession retires, partial supersession
keeps the remaining contribution. This says nothing about a globally strongest method.
Bounds need positive case/lane support or a stronger pending claim. Comparable candidates
compete on their stated intervals; equal later certificates add no strict numeric record.
Explicit first_certified_in attribution follows the original certificate. Publication
priority is used only where its date precision proves an earlier date, never T order,
registration time or a missing supersession field. Unordered ties remain diagnostic.

Typed record_scope references expose a finite registered projection's additional
family scope as unassessed currentness, with its review bead, until an assessment says
whether that scope is current; the gate holds every assessment to the family's
maintained comparison (`cases.asymptotic.deficiency_family`). They neither create a
result nor change authorship, scope, assurance or significance in the result register.
"""

from __future__ import annotations

import argparse
import calendar
import json
import re
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from fractions import Fraction
from pathlib import Path
from typing import Any, Literal, NamedTuple

from devtools import check_standing
from devtools import render_recent_results as standing
from devtools.check_results import BOUND_KINDS, scope_values
from sqpack.yamlio import load_yaml

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
FAMILY_LEDGER = PACKING / "frontier/asymptotic-waste-bounds.yaml"
FAMILY_SCHEMA = FAMILY_LEDGER.with_suffix(".schema.yaml")
_DATE = re.compile(r"([0-9]{4})(?:-([0-9]{2})(?:-([0-9]{2}))?)?")
Direction = Literal["lower", "upper"]
Lane = Literal["verified", "reported"]


class RecordFacet(NamedTuple):
    """Why one registered contribution remains current, without another result count."""

    family: str
    n: int | None = None
    direction: str | None = None
    lane: str | None = None
    scope: str | None = None


class RecordIndex(NamedTuple):
    """Known-current IDs and their facets; unsupported priority is not silently zero."""

    current_results: tuple[str, ...]
    facets: Mapping[str, tuple[RecordFacet, ...]]
    unresolved: Mapping[str, tuple[str, ...]]


@dataclass(frozen=True)
class BoundFacet:
    """A positive current/pending numeric candidate in one comparable case and lane."""

    result: str
    n: int
    direction: Direction
    lane: Lane
    low: Fraction
    high: Fraction

    def __post_init__(self) -> None:
        if self.low > self.high:
            raise ValueError("bound facet interval is reversed")


@dataclass(frozen=True)
class FamilyFacet:
    """An additional canonical family scope, with its current comparison if assessed."""

    result: str
    family: str
    scope: str
    review_bead: str
    #: Whether the scope is current, as a reproduced assessment says; None if unassessed.
    current: bool | None = None


def _date_interval(value: object) -> tuple[date, date] | None:
    match = _DATE.fullmatch(str(value))
    if match is None:
        return None
    year, month, day = (int(part) if part else None for part in match.groups())
    assert year is not None
    try:
        low = date(year, month or 1, day or 1)
        if month is None:
            high = date(year, 12, 31)
        elif day is None:
            high = date(year, month, calendar.monthrange(year, month)[1])
        else:
            high = low
    except ValueError:
        return None
    return low, high


def _published(record: Mapping[str, Any]) -> tuple[date, date] | None:
    # A compound source attribution's shared date cannot establish each source's priority.
    attribution = record.get("attribution")
    if attribution:
        if len(attribution["source_keys"]) != 1:
            return None
        return _date_interval(attribution.get("published"))
    return _date_interval(record.get("established"))


def _stronger(left: BoundFacet, right: BoundFacet) -> bool:
    return left.low > right.high if left.direction == "lower" else left.high < right.low


def _original(facet: BoundFacet, records: Mapping[str, Mapping[str, Any]]) -> BoundFacet:
    current = facet.result
    visited: set[str] = set()
    while facet.direction == "upper":
        if current in visited:
            raise ValueError(f"cyclic first_certified_in at {current}, n={facet.n}")
        visited.add(current)
        prior = {
            str(item["first_certified_in"])
            for item in records[current].get("regularizations", ())
            if item.get("n") == facet.n and item.get("first_certified_in")
        }
        if not prior:
            break
        if len(prior) != 1:
            raise ValueError(f"conflicting first_certified_in at {current}, n={facet.n}")
        (current,) = prior
        if current not in records or records[current].get("kind") != "upper-bound":
            raise ValueError(f"first_certified_in names no upper bound: {current}")
        if facet.n not in scope_values(dict(records[current]["scope"])):
            raise ValueError(f"first_certified_in {current} does not cover n={facet.n}")
    return BoundFacet(current, facet.n, facet.direction, facet.lane, facet.low, facet.high)


def classify_records(
    records: Mapping[str, Mapping[str, Any]],
    bound_facets: Iterable[BoundFacet],
    *,
    family_facets: Iterable[FamilyFacet] = (),
    proof_facets: Iterable[tuple[str, RecordFacet]] = (),
) -> RecordIndex:
    """Classify loaded positive facets; source reading and HTML belong to callers."""
    current: dict[str, set[RecordFacet]] = defaultdict(set)
    uncertain: dict[str, set[str]] = defaultdict(set)
    for identifier, record in records.items():
        if record["kind"] not in BOUND_KINDS and not standing.superseded(record, ""):
            current[identifier].add(RecordFacet(str(record["kind"])))
    groups: dict[tuple[int, str, str], set[BoundFacet]] = defaultdict(set)
    for facet in bound_facets:
        if facet.result not in records:
            raise ValueError(f"unknown result in bound facet: {facet.result}")
        if records[facet.result]["kind"] not in BOUND_KINDS:
            raise ValueError(f"non-bound result supplied as a bound facet: {facet.result}")
        original = _original(facet, records)
        groups[facet.n, facet.direction, facet.lane].add(original)
    for (n, direction, lane), candidates in sorted(groups.items()):
        frontier = [
            item
            for item in candidates
            if not any(_stronger(other, item) for other in candidates)
        ]
        # A result may supply a case citation and a more exact statement of the same bound.
        by_result: dict[str, list[BoundFacet]] = defaultdict(list)
        for item in frontier:
            by_result[item.result].append(item)
        winners: set[str] = set()
        if len(by_result) == 1:
            winners.update(by_result)
        elif (
            all(item.low == item.high for item in frontier)
            and len({item.low for item in frontier}) == 1
        ):
            dates = {identifier: _published(records[identifier]) for identifier in by_result}
            for identifier, published in dates.items():
                if published is not None and all(
                    other is not None and published[1] < other[0]
                    for peer, other in dates.items()
                    if peer != identifier
                ):
                    winners.add(identifier)
        if winners:
            for identifier in winners:
                current[identifier].add(
                    RecordFacet(str(records[identifier]["kind"]), n, direction, lane)
                )
        else:
            reason = f"Unordered {lane} {direction} bound priority at n={n}: " + ", ".join(
                sorted(by_result)
            )
            for identifier in by_result:
                uncertain[identifier].add(reason)
    for identifier, facet in proof_facets:
        if identifier not in records or records[identifier]["kind"] != "optimality":
            raise ValueError(f"proof facet names no optimality result: {identifier}")
        current[identifier].add(facet)
    for facet in family_facets:
        if facet.result not in records:
            raise ValueError(f"unknown result in family facet: {facet.result}")
        if facet.current:
            current[facet.result].add(
                RecordFacet(
                    str(records[facet.result]["kind"]), scope=f"{facet.family}: {facet.scope}"
                )
            )
        elif facet.current is None:
            uncertain[facet.result].add(
                f"The {facet.family} theorem scope survives its finite case projection; "
                f"current family comparison is unassessed ({facet.review_bead}): "
                f"{facet.scope}"
            )
    return RecordIndex(
        tuple(sorted(current)),
        {
            identifier: tuple(sorted(facets, key=repr))
            for identifier, facets in sorted(current.items())
        },
        {
            identifier: tuple(sorted(reasons))
            for identifier, reasons in sorted(uncertain.items())
        },
    )


def build_record_index(
    records: standing.Records, *, family_facets: Iterable[FamilyFacet] = ()
) -> RecordIndex:
    """Derive current numeric facets from canonical evidence, including pending claims."""
    facets = []
    proofs = []
    for n, case in sorted(records.cases.items()):
        for direction in ("lower", "upper"):
            for lane in ("verified", "reported"):
                bound = case.get(f"{lane}_{direction}_bound")
                if not bound:
                    continue
                low, high = standing.span(bound)
                for identifier in standing.lane_holders(n, records, direction, (lane,)):
                    record = records.results[identifier]
                    if record["kind"] == "optimality" or record["kind"] == f"{direction}-bound":
                        facets.append(BoundFacet(identifier, n, direction, lane, low, high))
                        status = case.get("status" if lane == "verified" else "reported_status")
                        if (
                            record["kind"] == "optimality"
                            and direction == "lower"
                            and status == "proved"
                        ):
                            proofs.append(
                                (
                                    identifier,
                                    RecordFacet(
                                        "optimality", n, lane=lane, scope="exact-value proof"
                                    ),
                                )
                            )
    # Read every improvement together; independently admitting each would count a weaker
    # pending claim even after a stronger public claim at the same case is registered.
    for identifier, record in records.results.items():
        if record["kind"] not in BOUND_KINDS:
            continue
        for finding in check_standing.improvements(record, records):
            if finding.direction not in {"lower", "upper"}:
                raise ValueError(f"unknown bound direction: {finding.direction}")
            direction: Direction = "lower" if finding.direction == "lower" else "upper"
            for lane in ("verified", "reported"):
                if lane == "verified" and str(record["confirmation"]) in standing.UNREPLAYED:
                    continue
                if getattr(finding, lane) != check_standing.EXCEEDS:
                    continue
                value = finding.stated
                facets.append(
                    BoundFacet(
                        identifier,
                        finding.n,
                        direction,
                        lane,
                        value.value,
                        value.value + value.slack,
                    )
                )
    return classify_records(
        records.results, facets, family_facets=family_facets, proof_facets=proofs
    )


def current_record_ids(authored_ids: Iterable[str], index: RecordIndex) -> tuple[str, ...]:
    """A subset of primary-authored IDs, deduplicated once per registered result."""
    return tuple(sorted(set(authored_ids) & set(index.current_results)))


def family_record_facets(
    ledger: Mapping[str, Any], records: standing.Records
) -> tuple[FamilyFacet, ...]:
    """Expose explicitly linked family scope, current only where an assessment says so.

    This reads the assessment and recomputes nothing: `tests/test_deficiency_family.py`
    holds every recorded assessment to `cases.asymptotic.deficiency_family`, which
    recomputes it from every statement of its family on each pull request, so no current
    window rests on a frozen comparison and the site's build reads no mathematics."""
    facets = []
    used: set[str] = set()
    for section, rows in ledger.items():
        if not isinstance(rows, list):
            continue
        for row in rows:
            link = row.get("record_scope")
            if link is None:
                continue
            identifier = link["result"]
            if identifier in used or identifier not in records.results:
                raise ValueError(f"duplicate or unknown record-scope result: {identifier}")
            used.add(identifier)
            keys = (records.results[identifier].get("attribution") or {}).get("source_keys", ())
            if row["source_key"] not in keys:
                raise ValueError(f"record-scope source does not match {identifier}")
            bead = link["review_bead"]
            if re.fullmatch(r"think-[a-z0-9]{4}", bead) is None:
                raise ValueError(f"record scope needs a review bead: {identifier}")
            assessment = link.get("assessment")
            current = None if assessment is None else bool(assessment["current"])
            facets.append(
                FamilyFacet(identifier, section, row["side_condition"], bead, current)
            )
    return tuple(facets)


def record_input_paths() -> tuple[Path, ...]:
    """Additional inputs beyond already-declared register, evidence and case inputs."""
    return (Path(__file__).resolve(), FAMILY_LEDGER, FAMILY_SCHEMA)


def load_record_index() -> RecordIndex:
    """Load the canonical current-record projection once for a renderer's shared context."""
    records = standing.load_records()
    ledger = load_yaml(FAMILY_LEDGER.read_text())
    family = family_record_facets(ledger, records)
    return build_record_index(records, family_facets=family)


def main(argv: Sequence[str] | None = None) -> int:
    """Report the same known-current and unassessed IDs the site consumes, read-only."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json", action="store_true", help="Include every current ID and facet."
    )
    args = parser.parse_args(argv)
    index = load_record_index()
    output: dict[str, Any] = {
        "current_result_count": len(index.current_results),
        "unassessed_result_count": len(index.unresolved),
        "unresolved": dict(index.unresolved),
    }
    if args.json:
        output["current_results"] = index.current_results
        output["facets"] = {
            identifier: [facet._asdict() for facet in facets]
            for identifier, facets in index.facets.items()
        }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
