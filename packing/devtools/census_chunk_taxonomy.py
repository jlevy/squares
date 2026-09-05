#!/usr/bin/env python3
"""A source-stratified taxonomy of what the known-best corpus is actually made of.

`BC-024` asks which chunk shapes, sizes, tilted-chunk counts and wall seatings recur
across the imported `n <= 100` corpus, and what the non-expressible residue has in common.
The broad component census already answers "what components are there"; this asks the
question the partition-instrument design needs, which is **whose geometry they came from**.

That distinction turns out to carry the finding. The corpus has three source strata and
they are not three samples of one population:

- `exact-grid` (64 records) is a row-major subset of an integer grid. Its components are
  not rectangles, and that is the point: a grid *subset* is a rectangle only when `n`
  happens to factor conveniently, so most of them are the very `other-polyomino` shape the
  grammar cannot express. The largest part of the residue is trivial geometry, not exotic.
- `kingbird-derived-facts` (34 records) is the real packings, and it is where every tilted
  component lives.
- `unitsquare-rendering` (2 records) is `n = 68` and `n = 69`, whose witness geometry the
  escape screen also excludes. Every one of their 137 squares is a singleton, and a large
  share of those singletons is tilted -- so this stratum is not "unstructured because it is
  a grid", it is unstructured because nothing in it lines up with anything else.

**No verdict is emitted and none is available.** This is descriptive: it reports what the
retained census contains, stratified, with the residue characterized. `H-044` is untouched,
the grammar cost stays unfrozen, and a component this calls unsupported is one the *current
detector* did not express, which the census's own `known_gap` says is not a refutation
until the minimal-partition solver exists.

Wall seating is the one axis not already in the census, and it is computed here from the
retained witness corners rather than inferred from lattice coordinates, which are relative
to a component and say nothing about the container.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.census_chunk_taxonomy
    uv run --frozen --all-extras --group dev python -m devtools.census_chunk_taxonomy --check
    uv run --frozen --all-extras --group dev python -m devtools.census_chunk_taxonomy --review
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import Counter
from typing import Any

from strif import atomic_output_file

from sqpack.witness import load_witness, materialize_witness

ROOT = pathlib.Path(__file__).resolve().parent.parent
ATLAS = ROOT / "atlas" / "known-best"
MANIFEST = ATLAS / "manifest.json"
CENSUS = ATLAS / "chunk-components.json"
WITNESS_SCHEMA = ROOT / "witnesses/witness.schema.yaml"
OUT = ROOT / "campaign" / "series" / "series-000-smoke-and-calibration" / "results"
RECORD = OUT / "bc-024-chunk-taxonomy.json"

BAND = "exact"
"""The exact-adjacency band. The near band differs by nine components across the corpus and
adds nothing to a taxonomy; a claim that rested on which band it read would be a claim about
the tolerance rather than about the packings."""

WALL_TOLERANCE = 1e-9
"""A corner is seated on a wall when it is this close to it.

Deliberately loose relative to the exact work elsewhere. Thirty-six of the hundred records
carry numerically-checked decimal witnesses, so an exact-sign test would answer "no wall" for
every one of them and the taxonomy would describe the corpus's precision rather than its
geometry. Nothing here is a feasibility claim, so a tolerance is the honest instrument."""

DIGITS = 60


def manifest() -> dict[int, dict[str, Any]]:
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas"]["entries"]
    return {int(entry["n"]): entry for entry in entries}


def band() -> list[dict[str, Any]]:
    bands = json.loads(CENSUS.read_text(encoding="utf-8"))["bands"]
    for band in bands:
        if band["name"] == BAND:
            return list(band["entries"])
    raise ValueError(f"census has no {BAND} band")


def is_tilted(angle_degrees: str) -> bool:
    """Is this component off the container's own axes?

    Taken modulo a quarter turn, because a component rotated by ninety degrees is seated
    the same way against the walls and the census already normalizes angle classes that
    way. A component within a thousandth of a degree of axis-aligned counts as aligned:
    the retained decimals carry angles like `89.9999985012`, and calling those tilted would
    make the count a measure of transcription noise.
    """
    residual = float(angle_degrees) % 90.0
    return min(residual, 90.0 - residual) > 1e-3


def wall_seating(entry: dict[str, Any]) -> dict[str, set[str]]:
    """Which container walls each square touches, by square id.

    Computed from the witness corners. The census's `lattice_coordinates` are relative to
    the component and cannot answer this: a bar sitting in a corner and the same bar in
    the middle of the container have identical lattice coordinates.

    Returned per square and unioned per component by the caller, because a chunk's seating
    is a property of the chunk. A two-square bar along the bottom-left with one square on
    the left wall and the other on the bottom is seated in a corner, and taking the maximum
    over its squares would call that an edge.
    """
    witness = load_witness(ROOT / entry["witness"]["path"], fallback_schema=WITNESS_SCHEMA)
    squares, side = materialize_witness(witness, digits=DIGITS)
    identifiers = [str(source["id"]) for source in witness["squares"]]
    limit = float(side)
    touched: dict[str, set[str]] = {}
    for identifier, corners in zip(identifiers, squares, strict=True):
        walls: set[str] = set()
        for corner_x, corner_y in corners:
            x, y = float(corner_x), float(corner_y)
            if abs(x) <= WALL_TOLERANCE:
                walls.add("left")
            if abs(y) <= WALL_TOLERANCE:
                walls.add("bottom")
            if abs(limit - x) <= WALL_TOLERANCE:
                walls.add("right")
            if abs(limit - y) <= WALL_TOLERANCE:
                walls.add("top")
        touched[identifier] = walls
    return touched


def serialized(record: dict[str, Any]) -> str:
    """The one canonical text form, used to write and to compare.

    `--check` compares this rather than the parsed record against the built one. JSON has
    no integer keys, so a dict built with them and a dict read back from the file differ in
    memory while being the same document -- a check that fails on its own output the moment
    it is written. Comparing the text says what drift actually means here.
    """
    return json.dumps(record, indent=2, sort_keys=True) + "\n"


def _by_string(counter: Counter[int]) -> dict[str, int]:
    """Integer-keyed counts as JSON can actually carry them, sorted numerically."""
    return {str(key): counter[key] for key in sorted(counter)}


def taxonomy() -> dict[str, Any]:
    entries = manifest()
    allowed = set(json.loads(CENSUS.read_text(encoding="utf-8"))["detector"]["allowed_shapes"])

    by_source: dict[str, Counter[str]] = {}
    sizes: dict[str, Counter[int]] = {}
    seatings: dict[str, Counter[int]] = {}
    tilted_by_source: Counter[str] = Counter()
    components_by_source: Counter[str] = Counter()
    records_by_source: Counter[str] = Counter()
    residue: list[dict[str, Any]] = []
    tilted_records: list[int] = []

    for entry in band():
        n = int(entry["n"])
        source = str(entries[n]["source"]["kind"])
        records_by_source[source] += 1
        seated = wall_seating(entries[n])
        tilted_here = 0
        for component in entry["components"]:
            shape = str(component["shape"])
            by_source.setdefault(source, Counter())[shape] += 1
            sizes.setdefault(shape, Counter())[int(component["size"])] += 1
            components_by_source[source] += 1
            walls = len(set().union(*(seated.get(str(m), set()) for m in component["members"])))
            seatings.setdefault(shape, Counter())[walls] += 1
            if is_tilted(str(component["angle_degrees"])):
                tilted_by_source[source] += 1
                tilted_here += 1
            if shape not in allowed and shape != "singleton":
                residue.append(
                    {
                        "n": n,
                        "source": source,
                        "size": int(component["size"]),
                        "walls_touched": walls,
                        "tilted": is_tilted(str(component["angle_degrees"])),
                        "is_the_whole_record": int(component["size"]) == n,
                    }
                )
        if tilted_here:
            tilted_records.append(n)

    return {
        "schema_version": 1,
        "subject": {
            "commitment": "BC-024",
            "band": BAND,
            "corpus": "atlas/known-best/chunk-components.json, exact-adjacency band",
            "emits_no_verdict": (
                "descriptive only; H-044 is untouched and an unsupported component is one "
                "the current detector did not express, which the census's own known_gap "
                "says is not a refutation until the minimal-partition solver exists"
            ),
        },
        "strata": {
            source: {
                "records": records_by_source[source],
                "components": components_by_source[source],
                "shapes": dict(sorted(by_source[source].items())),
                "tilted_components": tilted_by_source[source],
            }
            for source in sorted(by_source)
        },
        "sizes_by_shape": {
            shape: _by_string(counter) for shape, counter in sorted(sizes.items())
        },
        "wall_seating_by_shape": {
            shape: _by_string(counter) for shape, counter in sorted(seatings.items())
        },
        "tilted_records": tilted_records,
        "residue": {
            "components": len(residue),
            "by_source": dict(Counter(item["source"] for item in residue)),
            "tilted": sum(1 for item in residue if item["tilted"]),
            "whole_record": sum(1 for item in residue if item["is_the_whole_record"]),
            "sizes": _by_string(Counter(item["size"] for item in residue)),
            "walls_touched": _by_string(Counter(item["walls_touched"] for item in residue)),
            "detail": residue,
        },
    }


def _review(record: dict[str, Any]) -> None:
    print("  by source stratum:")
    for source, block in record["strata"].items():
        shapes = ", ".join(f"{name} {count}" for name, count in block["shapes"].items())
        print(
            f"    {source:<24} {block['records']:>3} records, "
            f"{block['components']:>4} components, {block['tilted_components']:>3} tilted"
        )
        print(f"      {shapes}")
    residue = record["residue"]
    print(
        f"  residue: {residue['components']} components the grammar does not express, "
        f"{residue['tilted']} of them tilted, {residue['whole_record']} the whole record"
    )
    print(f"    by source: {residue['by_source']}")
    print(f"    walls touched: {residue['walls_touched']}")
    print(f"  records with a tilted component: {len(record['tilted_records'])}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="compare against the record")
    group.add_argument("--review", action="store_true", help="print the taxonomy")
    args = parser.parse_args()

    built = taxonomy()
    if args.check:
        if not RECORD.exists():
            print(f"  {RECORD.name} is missing", file=sys.stderr)
            return 1
        if RECORD.read_text(encoding="utf-8") != serialized(built):
            print(f"  {RECORD.name} has drifted from a fresh census", file=sys.stderr)
            return 1
        strata = built["strata"]
        print(
            f"  chunk taxonomy reproduces: {len(strata)} source strata, "
            f"{built['residue']['components']} components in the residue"
        )
        return 0

    if args.review:
        _review(built)
        return 0

    with atomic_output_file(RECORD) as temporary:
        temporary.write_text(serialized(built), encoding="utf-8")
    print(f"wrote {RECORD.relative_to(ROOT.parent)}")
    _review(built)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
