"""Reconcile reported n17 patterns with an admitted residue; never admit certificates.

The result is a finite named-cell/D4 projection conditional on the frozen ordinary
cover and census. Contributor verifier reports do not establish the cap, angle-domain,
boundary or object-custody joins. No producer, LP, certificate replay or download runs.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from devtools import census_n17_certified as census
from devtools import select_n17_sub_patterns as selector
from sqpack import retained_json
from sqpack.yamlio import load_yaml

REPO = Path(__file__).resolve().parents[2]
SOURCE_SCHEMA = "n17-issue-pattern-source/v1"
RESULT_SCHEMA = "n17-issue-pattern-reconciliation/v1"
CAP = "1169/250"
POPULATION_LIMIT = 50000
INPUT_LIMIT = 8 << 20
OUTPUT_LIMIT = 1 << 20
MAX_SECONDS = 60
type Group = tuple[tuple[int, ...], ...]
SCOPE = {
    "metadata_projection_only": True,
    "certificate_verification_performed": False,
    "ordinary_assignment_exclusion_proved": False,
    "census_admission_proved": False,
    "global_optimality_proved": False,
}
MISSING_PREMISES = [
    "certificate cap/frame matched to ordinary 1169/250 cover",
    "complete independent closed angle-domain coverage",
    "boundary-contact convention and narrower guards discharged",
    "immutable complete certificate objects and current manifest identity",
    "complete standing FULL receipt bound to those objects and checker source",
    "reviewed ordinary admission/composition contract",
]


class RefusedError(ValueError):
    """A metadata input fails the declared join."""


def require(condition: object, message: str) -> None:
    if not condition:
        raise RefusedError(message)


def tick(deadline: float) -> None:
    require(time.monotonic() < deadline, "metadata wall ceiling exceeded; incomplete")


def read_document(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        raw = stream.read(INPUT_LIMIT + 1)
    require(len(raw) <= INPUT_LIMIT, "metadata input byte ceiling exceeded")
    document = json.loads(raw)
    require(isinstance(document, dict), "metadata input must be an object")
    return document


def parse_reports(messages: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply only explicit per-row updates; preserve unsupported aggregate claims."""
    rows: dict[int, dict[str, Any]] = {}
    discrepancies = []
    for message in messages:
        source = message["source"]
        require(isinstance(source, str) and bool(source), "missing source reference")
        seen = set()
        for line in message["table"].splitlines():
            columns = [part.strip() for part in line.strip().strip("|").split("|")]
            require(len(columns) == 4 and columns[0].isdigit(), "malformed pattern table row")
            number = int(columns[0])
            require(number > 0 and number not in seen, "duplicate row number in update")
            seen.add(number)
            cells = [name.strip() for name in columns[1].split(",")]
            require(cells and all(cells), "empty cell name")
            require(len(set(cells)) == len(cells), "repeated cell in reported pattern")
            status, verifier = columns[2:]
            require(status in {"Computed", "Certificate verified"}, "unknown reported status")
            old = rows.get(number)
            require(
                old is None or old["cells"] == cells,
                "changed cells need explicit reconciliation",
            )
            history = [] if old is None else old["history"]
            history.append({"source": source, "status": status, "verified_with": verifier})
            rows[number] = {
                "row": number,
                "cells": cells,
                "status": status,
                "verified_with": verifier,
                "source": source,
                "history": history,
            }
        for correction in message.get("verifier_corrections", []):
            number = correction["row"]
            require(
                type(number) is int and number in rows,
                "verifier correction references an unknown row",
            )
            verifier = correction["verified_with"]
            require(isinstance(verifier, str) and bool(verifier), "empty verifier correction")
            row = rows[number]
            row["verified_with"] = verifier
            row["source"] = source
            row["history"].append(
                {
                    "source": source,
                    "status": row["status"],
                    "verified_with": verifier,
                    "correction": True,
                }
            )
        aggregate = message.get("totals")
        computed = sum(row["status"] == "Computed" for row in rows.values())
        actual = {"verified": len(rows) - computed, "computed": computed}
        for discrepancy in discrepancies:
            if "resolved_by" not in discrepancy and discrepancy["claimed"] == actual:
                discrepancy["resolved_by"] = source
        if aggregate is not None and aggregate != actual:
            discrepancies.append(
                {"source": source, "claimed": aggregate, "explicit_rows": actual}
            )
    ordered = [rows[number] for number in sorted(rows)]
    computed = sum(row["status"] == "Computed" for row in ordered)
    return {
        "rows": ordered,
        "row_totals": {"verified": len(ordered) - computed, "computed": computed},
        "aggregate_discrepancies": discrepancies,
        "unresolved_aggregate_discrepancies": [
            item for item in discrepancies if "resolved_by" not in item
        ],
    }


def class_relations(mask: int, admitted: dict[int, str], group: Group) -> dict[str, list[str]]:
    """D4 equality and strict subset relations have different logical directions."""
    images = selector.orbit(mask, group)
    canonical = min(images)
    equal, contained, containing = [], [], []
    for other, name in sorted(admitted.items()):
        if other == canonical:
            equal.append(name)
        elif any((other & image) == other for image in images):
            contained.append(name)
        elif any((image & other) == image for image in images):
            containing.append(name)
    return {
        "equal_admitted": equal,
        "contained_admitted": contained,
        "containing_admitted": containing,
    }


def project(mask: int, population: dict[int, int], group: Group) -> set[int]:
    """Canonical assignment orbits that contain a D4 image of this pattern."""
    images = selector.orbit(mask, group)
    return {state for state in population if any((state & image) == image for image in images)}


def population_count(population: dict[int, int], masks: set[int]) -> dict[str, int]:
    return {"orbits": len(masks), "states": sum(population[mask] for mask in masks)}


def require_roster(actual: list[int], expected: list[int], where: str) -> None:
    require(actual == expected and len(set(actual)) == len(actual), f"{where}: roster mismatch")


def assignment_roster(
    rows: list[dict[str, Any]], cover: census.Cover, where: str
) -> dict[int, int]:
    require(0 < len(rows) <= POPULATION_LIMIT, f"{where}: population size ceiling")
    result = {}
    for row in rows:
        mask = row["mask"]
        require(type(mask) is int and mask.bit_count() == 17, f"{where}: typed17 assignment")
        require(
            census.class_mask(cover, row["cells"], where) == mask, f"{where}: cell/mask join"
        )
        size = len(selector.orbit(mask, cover.geometry.group))
        require(row["orbit_size"] == size and mask not in result, f"{where}: orbit identity")
        result[mask] = size
    return result


def populations(
    document: dict[str, Any], root: Path, deadline: float
) -> tuple[census.Cover, dict[int, str], dict[str, dict[int, int]], dict[str, Any]]:
    """Inherit admitted proof premises, reconstruct finite residue and check the roster."""
    cover = census.cover_context()
    expected = document["baseline"]
    report = read_document(root / expected["census"])
    partition = read_document(root / expected["partition"])
    tail = read_document(root / expected["tail"])
    require(report["design"] == partition["design"] == census.DESIGN, "cover identity")
    require(partition["cap"] == tail["outer_U"] == document["cap"] == CAP, "cap/frame identity")
    require(report["certified"] == partition["certified"], "census/partition baseline mismatch")
    require(report["certified"] == expected["certified"], "frozen census identity mismatch")
    admitted = {}
    for entry in report["entries"]:
        if entry["status"] == "admitted":
            mask = census.class_mask(cover, entry["cells"], "admitted census")
            require(mask not in admitted, "duplicate admitted D4 class")
            admitted[mask] = entry["name"]
    require(len(admitted) == expected["certified"]["admitted"], "admitted entry count")
    ledger = load_yaml((root / partition["ledger"]).read_text(encoding="utf-8"))
    ledger_admitted = [entry for entry in ledger["entries"] if entry["status"] == "admitted"]
    ledger_classes = {
        census.class_mask(cover, entry["cells"], "ledger"): entry["name"]
        for entry in ledger_admitted
    }
    require(
        admitted == ledger_classes and len(ledger_admitted) == len(admitted),
        "ledger/census class identities differ",
    )
    full = assignment_roster(partition["orbits"], cover, "complete residue")
    require(
        population_count(full, set(full))
        == {
            "orbits": expected["certified"]["orbits"],
            "states": expected["certified"]["surviving_states"],
        },
        "complete residue totals",
    )
    tick(deadline)
    forbidden = sorted(
        {image for mask in admitted for image in selector.orbit(mask, cover.geometry.group)}
    )
    survivors = selector.survivors(cover.states, forbidden)
    canonical = {
        int(mask)
        for mask in survivors
        if selector.canonical(int(mask), cover.geometry.group) == int(mask)
    }
    require(set(full) == canonical, "partition omits/adds an ordinary surviving orbit")
    require(int(survivors.size) == sum(full.values()), "surviving state accounting")
    tail_population = assignment_roster(tail["states"], cover, "distance-two tail")
    endpoint_images = selector.orbit(cover.endpoint_state, cover.geometry.group)
    require(
        all(
            row["distance"]
            == min((row["mask"] ^ image).bit_count() for image in endpoint_images)
            for row in partition["orbits"]
        ),
        "partition endpoint distances differ",
    )
    require(
        {tuple(permutation) for permutation in tail["d4"].values()}
        == set(cover.geometry.group),
        "tail D4 group identity",
    )
    distance_two = sorted(row["mask"] for row in partition["orbits"] if row["distance"] == 2)
    require_roster(sorted(tail_population), distance_two, "distance-two")
    require(
        population_count(tail_population, set(tail_population))
        == {"orbits": 95, "states": 744},
        "tail95 identity",
    )
    pilot = document["pilot"]
    require_roster(pilot["masks"], sorted(tail_population)[:8], "frozen first-eight")
    require(
        pilot["selection"] == "first eight increasing canonical distance-two masks",
        "pilot order",
    )
    tick(deadline)
    return (
        cover,
        admitted,
        {
            "complete_residue": full,
            "distance_two_tail": tail_population,
            "first_eight_pilot": {mask: tail_population[mask] for mask in pilot["masks"]},
        },
        {
            "design": census.DESIGN,
            "cap": CAP,
            "frame": census.KERNEL_FRAME,
            "catalogue": list(cover.geometry.names),
            "d4": [list(permutation) for permutation in cover.geometry.group],
            "census": expected["census"],
            "partition": expected["partition"],
            "ledger": partition["ledger"],
            "tail": expected["tail"],
            "certified": expected["certified"],
            "pilot": pilot,
            "proof_premises": "inherited retained census; no certificate re-verification",
        },
    )


def reconcile(
    document: dict[str, Any], *, root: Path = REPO, deadline: float
) -> dict[str, Any]:
    require(document.get("schema") == SOURCE_SCHEMA, "source schema")
    reports = parse_reports(document["reports"])
    require_roster([row["row"] for row in reports["rows"]], list(range(1, 34)), "reported33")
    patterns = [
        {**row, "id": f"413-{row['row']}", "issue": 413} for row in reports["rows"]
    ] + document["companion_patterns"]
    identifiers = [pattern.get("id") for pattern in patterns]
    require(
        all(type(identity) is str and bool(identity.strip()) for identity in identifiers),
        "pattern IDs must be nonempty strings",
    )
    require(len(set(identifiers)) == len(identifiers), "duplicate pattern ID")
    cover, admitted, groups, baseline = populations(document, root, deadline)
    class_rows: dict[int, list[str]] = {}
    hit_by_id: dict[str, dict[str, set[int]]] = {}
    rows = []
    for pattern in patterns:
        tick(deadline)
        mask = census.class_mask(cover, pattern["cells"], pattern["id"])
        class_rows.setdefault(mask, []).append(pattern["id"])
        hits = {
            name: project(mask, population, cover.geometry.group)
            for name, population in groups.items()
        }
        hit_by_id[pattern["id"]] = hits
        relations = class_relations(mask, admitted, cover.geometry.group)
        rows.append(
            {
                **pattern,
                "canonical_mask": mask,
                "admitted_relations": relations,
                "projection": {
                    name: population_count(groups[name], matched)
                    for name, matched in hits.items()
                },
                "matched_distance_two_masks": sorted(hits["distance_two_tail"]),
                "matched_pilot_masks": sorted(hits["first_eight_pilot"]),
                "custody": "not_joined" if pattern["issue"] == 413 else pattern["custody"],
                "premise_join": "unknown; exact names only",
                "certificate_availability": (
                    "not generated; contributor estimate only"
                    if pattern["id"] == "413-33"
                    else "unpublished per source status; generation availability unknown"
                    if pattern["status"] == "Computed"
                    else "reported, complete custody not joined"
                ),
                "endpoint_assignment_in_projection": bool(
                    project(
                        mask,
                        {selector.canonical(cover.endpoint_state, cover.geometry.group): 1},
                        cover.geometry.group,
                    )
                ),
                **SCOPE,
            }
        )
    report_ids = [f"413-{number}" for number in range(1, 34)]
    unions = {name: set() for name in groups}
    for row in rows[:33]:
        marginal = {}
        for name, population in groups.items():
            hits = hit_by_id[row["id"]][name]
            marginal[name] = population_count(population, hits - unions[name])
            unions[name] |= hits
        row["fixed_order_marginal"] = marginal
    companions = [pattern["id"] for pattern in document["companion_patterns"]]
    companion_union = {
        name: set().union(*(hit_by_id[item][name] for item in companions)) for name in groups
    }
    require(
        population_count(groups["complete_residue"], companion_union["complete_residue"])
        == {"orbits": 21, "states": 148},
        "358 known union control",
    )
    require(not companion_union["distance_two_tail"], "358 known zero-tail control")
    companion_classes = {
        row["canonical_mask"]: row["id"] for row in rows if row["issue"] == 358
    }
    for row in rows[:33]:
        row["companion_358_relations"] = class_relations(
            row["canonical_mask"], companion_classes, cover.geometry.group
        )
    tick(deadline)
    return {
        "schema": RESULT_SCHEMA,
        "status": "complete_named_cell_projection_premise_join_partial",
        "baseline": baseline,
        "source_observed_at": document["observed_at"],
        "source_refresh_observed_at": document.get("refresh_observed_at"),
        "contributor_conditional_join": [
            note
            for note in document["additional_source_notes"]
            if note["source"].endswith("issuecomment-6064503349")
        ],
        "explicit_row_totals": reports["row_totals"],
        "aggregate_discrepancies": reports["aggregate_discrepancies"],
        "unresolved_aggregate_discrepancies": reports["unresolved_aggregate_discrepancies"],
        "standing_full_reported_rows": [
            row["row"]
            for row in rows[:33]
            if "standing verifier (full)" in row["verified_with"]
        ],
        "class_duplicates": [
            {"mask": mask, "ids": ids}
            for mask, ids in sorted(class_rows.items())
            if len(ids) > 1
        ],
        "missing_premises_for_admission": MISSING_PREMISES,
        "marginal_order": report_ids,
        "union_scope": "hypothetical containment relevance; no census subtraction",
        "population_semantics": (
            "canonical D4 orbits; states count all distinct D4 images, including the pilot"
        ),
        "population_sizes": {
            name: population_count(population, set(population))
            for name, population in groups.items()
        },
        "reported33_union": {
            name: population_count(groups[name], hits) for name, hits in unions.items()
        },
        "companion358_union": {
            name: population_count(groups[name], hits) for name, hits in companion_union.items()
        },
        "patterns": rows,
        **SCOPE,
    }


def publish_metadata(path: Path, text: str) -> None:
    """Replace complete bytes using private staging permissions; no durability promise."""
    descriptor, name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".partial"
    )
    temporary = Path(name)
    try:
        try:
            remaining = memoryview(text.encode("utf-8"))
            while remaining:
                written = os.write(descriptor, remaining)
                if written <= 0:
                    raise OSError("metadata staging write made no progress")
                remaining = remaining[written:]
        finally:
            failure = sys.exception()
            try:
                os.close(descriptor)
            except OSError as error:
                if failure is None:
                    raise
                failure.add_note(f"metadata staging close failed: {error}")
        temporary.replace(path)
    finally:
        failure = sys.exception()
        try:
            temporary.unlink(missing_ok=True)
        except OSError as error:
            if failure is None:
                raise
            failure.add_note(f"metadata staging cleanup failed for {temporary}: {error}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args(argv)
    if (args.output is None) == (args.check is None):
        parser.error("select exactly one of --output or --check")
    try:
        document = read_document(args.source)
        result = reconcile(document, deadline=time.monotonic() + MAX_SECONDS)
        text = retained_json.dumps(result, ensure_ascii=False, allow_nan=False)
        require(len(text.encode("utf-8")) <= OUTPUT_LIMIT, "output byte ceiling")
        if args.check is not None:
            require(result == read_document(args.check), "fresh metadata result differs")
            print("PASS: complete fresh named-cell reconstruction; admission remains unproved")
        else:
            assert args.output is not None
            publish_metadata(args.output, text)
            print("WROTE: conditional metadata projection; no admission")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        for note in getattr(exc, "__notes__", []):
            print(f"  {note}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
