#!/usr/bin/env python3
"""Reparse retained first-party result sources and reconcile the frontier.

This check deliberately uses stable local snapshots. Refreshing a source is a dated
research action; ordinary tests must not depend on network state.
"""

from __future__ import annotations

import json
import math
import pathlib
import re
import sys
from decimal import Decimal

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
COVERAGE = FRONTIER / "source-coverage.yaml"
EVIDENCE = FRONTIER / "evidence.yaml"


def parse_case(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---\n")[1])["packing"]


def parse_kingbird(path: pathlib.Path, n_min: int, n_max: int) -> dict[int, str]:
    """Read the catalogue's visible boxes, then apply its stated grid fallback."""
    text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    blocks = re.findall(
        r'<div class="box"><font size="\+3">(.*?)</div></div>', text, flags=re.S
    )
    values: dict[int, str] = {}
    for block in blocks:
        label = re.match(r"\s*([0-9][0-9, ]*)<br>", block)
        if label is None:
            continue
        ns = [int(value) for value in re.findall(r"\d+", label.group(1))]
        approximate = re.search(r"\\Nn\{([0-9]+(?:\.[0-9]+)?)\}", block)
        integer = re.search(r"\$s\s*=\s*([0-9]+(?:\.[0-9]+)?)\$", block)
        match = approximate or integer
        if match is None:
            raise ValueError(f"could not parse Kingbird value for labels {ns}")
        value = match.group(1)
        for n in ns:
            previous = values.setdefault(n, value)
            if previous != value:
                raise ValueError(f"conflicting Kingbird values for n={n}: {previous}, {value}")
    for n in range(n_min, n_max + 1):
        values.setdefault(n, str(math.isqrt(n - 1) + 1))
    return values


def source_by_id(coverage: dict, source_id: str) -> dict:
    matches = [source for source in coverage["sources"] if source["id"] == source_id]
    if len(matches) != 1:
        raise ValueError(f"source id {source_id!r} occurs {len(matches)} times")
    return matches[0]


def scope_contains(scope: dict, n: int) -> bool:
    """Return whether a source's declared scope includes one case."""
    if "n_values" in scope:
        return n in scope["n_values"]
    return scope["n_min"] <= n <= scope["n_max"]


def main() -> int:
    coverage = yaml.safe_load(COVERAGE.read_text(encoding="utf-8"))
    n_min = coverage["case_corpus"]["n_min"]
    n_max = coverage["case_corpus"]["n_max"]
    errors: list[str] = []

    reader_view = ROOT / coverage["case_corpus"]["reader_view"]
    if not reader_view.is_file():
        errors.append(f"case reader view does not exist: {reader_view.relative_to(ROOT)}")
    if n_min > n_max:
        errors.append(f"case corpus range is reversed: {n_min}..{n_max}")

    source_ids = [source["id"] for source in coverage["sources"]]
    if len(source_ids) != len(set(source_ids)):
        errors.append("source ids are not unique")
    errors.extend(
        f"{source['id']}: local source does not exist: {source['local']}"
        for source in coverage["sources"]
        if not (ROOT / source["local"]).exists()
    )

    evidence_document = yaml.safe_load(EVIDENCE.read_text(encoding="utf-8"))
    evidence_ids = [entry["id"] for entry in evidence_document["evidence"]]
    if len(evidence_ids) != len(set(evidence_ids)):
        errors.append("frontier evidence ids are not unique")
    evidence_id_set = set(evidence_ids)
    for source in coverage["sources"]:
        errors.extend(
            f"{source['id']}: unknown evidence id {evidence_id}"
            for evidence_id in source["evidence"]
            if evidence_id not in evidence_id_set
        )

    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1

    kingbird_source = source_by_id(coverage, "kingbird-current")
    kingbird = parse_kingbird(ROOT / kingbird_source["local"], n_min, n_max)
    overrides = {entry["n"]: entry for entry in coverage["selected_overrides"]}
    if len(overrides) != len(coverage["selected_overrides"]):
        errors.append("selected override n values are not unique")
    for entry in coverage["selected_overrides"]:
        n = entry["n"]
        if not n_min <= n <= n_max:
            errors.append(f"selected override n={n} lies outside the case corpus")
        if entry["source_id"] not in source_ids:
            errors.append(f"selected override n={n} names unknown source {entry['source_id']}")
            continue
        source = source_by_id(coverage, entry["source_id"])
        if not scope_contains(source["scope"], n):
            errors.append(f"selected override n={n} is outside {source['id']}'s scope")
        if entry["evidence"] not in source["evidence"]:
            errors.append(
                f"selected override n={n} uses evidence {entry['evidence']} "
                f"not declared by {source['id']}"
            )

    cases = {
        case["n"]: case
        for case in (parse_case(path) for path in sorted(FRONTIER.glob("n-[0-9][0-9][0-9].md")))
    }
    expected_ns = set(range(n_min, n_max + 1))
    if set(cases) != expected_ns:
        errors.append(f"case corpus is not exactly n={n_min}..{n_max}")
    for n in sorted(expected_ns & set(cases)):
        case = cases[n]
        bound = case["reported_upper_bound"]
        if n in overrides:
            expected = overrides[n]
            source = source_by_id(coverage, expected["source_id"])
            expected_value = expected["value"]
            expected_key = source["source_key"]
            if expected["evidence"] not in bound["evidence"]:
                errors.append(f"n={n}: selected evidence {expected['evidence']} is absent")
        else:
            expected_value = kingbird[n]
            expected_key = kingbird_source["source_key"]
        if Decimal(bound["value"]) != Decimal(expected_value):
            errors.append(
                f"n={n}: reported upper {bound['value']} != selected source {expected_value}"
            )
        if bound["source_key"] != expected_key:
            errors.append(
                f"n={n}: source {bound['source_key']!r} != selected source {expected_key!r}"
            )

    unit_source = source_by_id(coverage, "unitsquare-release1")
    release = json.loads((ROOT / unit_source["local"]).read_text(encoding="utf-8"))
    release_values = {entry["n"]: entry["offered_side"] for entry in release["results"]}
    inventory = {entry["n"]: entry["value"] for entry in coverage["beyond_horizon_claims"]}
    if len(inventory) != len(coverage["beyond_horizon_claims"]):
        errors.append("beyond-horizon n values are not unique")
    for entry in coverage["beyond_horizon_claims"]:
        n = entry["n"]
        if n_min <= n <= n_max:
            errors.append(f"beyond-horizon claim n={n} lies inside the case corpus")
        if entry["source_id"] not in source_ids:
            errors.append(f"beyond-horizon n={n} names unknown source {entry['source_id']}")
            continue
        source = source_by_id(coverage, entry["source_id"])
        if not scope_contains(source["scope"], n):
            errors.append(f"beyond-horizon n={n} is outside {source['id']}'s scope")
    for n, expected in release_values.items():
        recorded = overrides.get(n, {}).get("value") if n <= n_max else inventory.get(n)
        if recorded != expected:
            errors.append(f"UnitSquare n={n}: source {expected} != inventory {recorded}")
    if set(release_values) != set(overrides) | set(inventory):
        errors.append("UnitSquare result set differs from in- and beyond-horizon inventory")

    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1
    print(
        f"  source coverage reconciled: {n_max - n_min + 1} cases, "
        f"{len(overrides)} newer in-horizon reports, {len(inventory)} tracked beyond horizon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
