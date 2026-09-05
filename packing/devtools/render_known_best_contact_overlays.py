#!/usr/bin/env python3
"""Render a deterministic descriptive-contact gallery from the known-best atlas."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Sequence
from dataclasses import replace
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from strif import atomic_output_file

from devtools.build_known_best_atlas import frame_from_witness
from sqpack.render import render_packing_svg
from sqpack.render.model import (
    ContainerWall,
    DetectedContactFeature,
    Overlay,
    PackingFrame,
    Point2,
    RenderSpec,
    ScalarSource,
    SquareGeometry,
)
from sqpack.render.numbers import scalar_from_decimal
from sqpack.witness import load_witness
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
ATLAS_ROOT = ROOT / "atlas/known-best"
CORPUS = ATLAS_ROOT / "manifest.json"
CENSUS = ATLAS_ROOT / "chunk-components.json"
OUTPUT_ROOT = ATLAS_ROOT / "contact-overlays"
OUTPUT = ATLAS_ROOT / "contact-overlays.json"
SCHEMA = ATLAS_ROOT / "contact-overlay-gallery.schema.yaml"
WITNESS_SCHEMA = ROOT / "witnesses/witness.schema.yaml"
GENERATOR = "python -m devtools.render_known_best_contact_overlays"
SWEEP_NAME = "registered-angle-contact"


def _centre(square: SquareGeometry) -> Point2:
    with localcontext() as context:
        context.prec = 100
        x = sum((point.x.projected for point in square.corners), Decimal(0)) / 4
        y = sum((point.y.projected for point in square.corners), Decimal(0)) / 4
    return Point2(scalar_from_decimal(str(x)), scalar_from_decimal(str(y)))


def _wall_endpoint(centre: Point2, side: ScalarSource, wall: ContainerWall) -> Point2:
    zero = scalar_from_decimal("0")
    if wall is ContainerWall.LEFT:
        return Point2(zero, centre.y)
    if wall is ContainerWall.RIGHT:
        return Point2(side, centre.y)
    if wall is ContainerWall.BOTTOM:
        return Point2(centre.x, zero)
    return Point2(centre.x, side)


def _square_id(source_id: str) -> str:
    return f"square-{int(source_id):03d}"


def contact_census_features(
    frame: PackingFrame, entry: dict[str, Any]
) -> tuple[DetectedContactFeature, ...]:
    """Translate census rows into explicitly numerical graph-overlay features."""
    if entry["witness_id"] != frame.source_id or entry["n"] != len(frame.squares):
        raise ValueError("contact census entry does not match the rendered witness")
    angle_tolerance = Decimal(entry["angle_tolerance_radians"])
    contact_tolerance = Decimal(entry["contact_tolerance"])
    centres = {square.square_id: _centre(square) for square in frame.squares}
    features = []
    for component in entry["components"]:
        for edge in component["edges"]:
            square_ids = tuple(sorted(_square_id(value) for value in edge["squares"]))
            features.append(
                DetectedContactFeature(
                    feature_id=f"census-pair-{square_ids[0]}-{square_ids[1]}",
                    start=centres[square_ids[0]],
                    end=centres[square_ids[1]],
                    square_ids=square_ids,
                    angle_tolerance_radians=angle_tolerance,
                    contact_tolerance=contact_tolerance,
                    residual=Decimal(edge["residual"]),
                    normal=edge["normal"],
                )
            )
        for source_id, walls in component["wall_seated_squares"].items():
            square_id = _square_id(source_id)
            for wall_name in walls:
                wall = ContainerWall(wall_name)
                features.append(
                    DetectedContactFeature(
                        feature_id=f"census-wall-{square_id}-{wall.value}",
                        start=centres[square_id],
                        end=_wall_endpoint(centres[square_id], frame.container_side, wall),
                        square_ids=(square_id,),
                        angle_tolerance_radians=angle_tolerance,
                        contact_tolerance=contact_tolerance,
                        wall=wall,
                    )
                )
    return tuple(sorted(features, key=lambda feature: feature.feature_id))


def _selected_entries(
    entries: list[dict[str, Any]], source_kinds: dict[int, str]
) -> list[tuple[dict[str, Any], str]]:
    non_grid = [entry for entry in entries if source_kinds[entry["n"]] != "exact-grid"]

    def topologies(entry: dict[str, Any]) -> set[str]:
        return {component["topology"] for component in entry["components"]}

    rules = [
        (
            min(
                [
                    entry
                    for entry in non_grid
                    if {"contact-chain", "contact-patch", "singleton"} <= topologies(entry)
                ],
                key=lambda entry: entry["n"],
            ),
            "smallest non-grid case mixing chains, patches, and singletons",
        ),
        (
            min(
                [
                    entry
                    for entry in non_grid
                    if entry["free_square_count"] == 0
                    and {"contact-chain", "contact-patch"} <= topologies(entry)
                ],
                key=lambda entry: entry["n"],
            ),
            "smallest fully structured non-grid case mixing chains and patches",
        ),
        (
            min(
                [
                    entry
                    for entry in non_grid
                    if entry["free_square_count"] == 0
                    and topologies(entry) == {"contact-patch"}
                ],
                key=lambda entry: entry["n"],
            ),
            "smallest fully structured non-grid case containing patches only",
        ),
        (
            min(
                [
                    entry
                    for entry in non_grid
                    if source_kinds[entry["n"]] == "unitsquare-rendering"
                ],
                key=lambda entry: entry["n"],
            ),
            "first retained UnitSquare rendering-derived geometry",
        ),
        (
            max(
                non_grid,
                key=lambda entry: (
                    max(component["size"] for component in entry["components"]),
                    -entry["n"],
                ),
            ),
            "non-grid case with the largest registered contact component",
        ),
    ]
    if len({entry["n"] for entry, _rule in rules}) != len(rules):
        raise ValueError("representative contact-overlay strata are not distinct")
    return sorted(rules, key=lambda item: item[0]["n"])


def expected_outputs() -> tuple[dict[str, Any], dict[Path, str]]:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))["atlas"]
    source_kinds = {entry["n"]: entry["source"]["kind"] for entry in corpus["entries"]}
    witness_paths = {entry["n"]: ROOT / entry["witness"]["path"] for entry in corpus["entries"]}
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    sweep = next(sweep for sweep in census["contact_sweeps"] if sweep["name"] == SWEEP_NAME)
    selections = _selected_entries(sweep["entries"], source_kinds)
    renderings: dict[Path, str] = {}
    records = []
    for entry, rule in selections:
        n = entry["n"]
        witness = load_witness(witness_paths[n], fallback_schema=WITNESS_SCHEMA)
        base_frame = frame_from_witness(witness)
        features = contact_census_features(base_frame, entry)
        frame = replace(base_frame, features=features, label=f"n={n} contact census")
        path = OUTPUT_ROOT / f"n-{n:03d}.svg"
        topology_counts = Counter(component["topology"] for component in entry["components"])
        description = (
            f"House rendering of known-best n={n} with dashed graph edges for contacts "
            f"detected at angle tolerance {entry['angle_tolerance_radians']} radians "
            f"and contact tolerance {entry['contact_tolerance']}. Lines join square "
            "centres or centres to walls; they are descriptive graph incidence, not "
            "exact physical contact loci or rigidity certificates."
        )
        rendered = render_packing_svg(
            frame,
            spec=RenderSpec(
                overlays=frozenset({Overlay.CONTACT_CENSUS, Overlay.SQUARE_IDS}),
                title=f"Known-best n={n}: descriptive contact census",
                description=description,
                width=1200,
            ),
        )
        renderings[path] = rendered
        records.append(
            {
                "n": n,
                "selection_rule": rule,
                "source_kind": source_kinds[n],
                "rendering": str(path.relative_to(ATLAS_ROOT)),
                "component_count": len(entry["components"]),
                "contact_edge_count": sum(
                    len(component["edges"]) for component in entry["components"]
                ),
                "wall_seating_edge_count": sum(
                    len(walls)
                    for component in entry["components"]
                    for walls in component["wall_seated_squares"].values()
                ),
                "free_square_count": entry["free_square_count"],
                "internal_slide_dof": entry["internal_slide_dof"],
                "topology_counts": dict(sorted(topology_counts.items())),
            }
        )
    document = {
        "softschema": {
            "contract": "packing.squares:ContactOverlayGallery/v1",
            "schema": "contact-overlay-gallery.schema.yaml",
            "envelope": "gallery",
            "status": "enforced",
        },
        "gallery": {
            "generated_by": GENERATOR,
            "claim_status": "calibration-no-verdict",
            "corpus": "manifest.json",
            "annotations": "chunk-components.json",
            "sweep": SWEEP_NAME,
            "angle_tolerance_radians": sweep["entries"][0]["angle_tolerance_radians"],
            "contact_tolerance": sweep["entries"][0]["contact_tolerance"],
            "visual_semantics": (
                "Dashed orange centre-to-centre and centre-to-wall lines show "
                "tolerance-qualified census graph incidence. They are not exact "
                "contact loci, rigidity certificates, or H-044 evidence."
            ),
            "selection_policy": (
                "Five deterministic, distinct calibration strata selected from the "
                "registered census; changes regenerate a new checked gallery."
            ),
            "entries": records,
        },
    }
    return document, renderings


def _validate(document: dict[str, Any]) -> None:
    schema = safe_load(SCHEMA.read_text(encoding="utf-8"))
    problems = sorted(
        Draft202012Validator(schema).iter_errors(document["gallery"]),
        key=lambda problem: list(problem.path),
    )
    if problems:
        raise ValueError(f"contact-overlay schema failure: {problems[0].message}")


def _text(document: dict[str, Any]) -> str:
    return json.dumps(document, indent=2, sort_keys=True) + "\n"


def update() -> None:
    document, renderings = expected_outputs()
    _validate(document)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    for path, rendered in renderings.items():
        with atomic_output_file(path) as temporary:
            temporary.write_text(rendered, encoding="utf-8")
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(_text(document), encoding="utf-8")
    print("known-best contact overlays updated: 5 house-rendered calibration strata")


def check() -> None:
    document, renderings = expected_outputs()
    _validate(document)
    problems = []
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != _text(document):
        problems.append("contact-overlays.json is stale")
    expected_names = {path.name for path in renderings}
    actual_names = {path.name for path in OUTPUT_ROOT.glob("*.svg")}
    if actual_names != expected_names:
        problems.append("contact-overlays directory has missing or unexpected SVGs")
    problems.extend(
        f"{path.name} is stale"
        for path, rendered in renderings.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != rendered
    )
    if problems:
        raise ValueError("known-best contact overlay drift: " + "; ".join(problems))
    print("known-best contact overlay check passed: 5 house-rendered calibration strata")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.update:
        update()
    else:
        check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
