#!/usr/bin/env python3
"""Build the compact abstract atlas of size-five contact-scaffold orbit representatives."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from strif import atomic_output_file

from sqpack.contact_assembly import (
    Axis,
    ContactEdge,
    ContactScaffold,
    connected_topology_representatives,
    enumerate_isomorph_free_scaffolds,
)
from sqpack.render.style import PAPER_THEME, color_for_square
from sqpack.render.svg import (
    append_metadata,
    append_title_desc,
    element,
    serialize_svg,
    sub,
    write_svg_atomic,
)
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
ATLAS_ROOT = ROOT / "atlas/enumerated"
OUTPUT = ATLAS_ROOT / "contact-scaffolds-size5.json"
SCHEMA = ATLAS_ROOT / "contact-scaffold-atlas.schema.yaml"
RENDERING = ATLAS_ROOT / "rendering/contact-scaffolds-size5-overview.svg"
GENERATOR = "python -m devtools.build_contact_scaffold_atlas"
COLOR_DIGITS: dict[tuple[Axis, int], str] = {
    ("u", -1): "0",
    ("u", 1): "1",
    ("v", -1): "2",
    ("v", 1): "3",
}
DIGIT_COLORS: dict[str, tuple[Axis, int]] = {
    digit: color for color, digit in COLOR_DIGITS.items()
}
VERTEX_OFFSETS = ((0, -46), (44, -14), (27, 37), (-27, 37), (-44, -14))


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _topology(scaffold: ContactScaffold) -> tuple[tuple[int, int], ...]:
    return tuple((edge.left, edge.right) for edge in scaffold.edges)


def _coloring(scaffold: ContactScaffold) -> str:
    return "".join(COLOR_DIGITS[(edge.normal, edge.sign)] for edge in scaffold.edges)


def decode_representative(topology: dict[str, Any], representative: str) -> ContactScaffold:
    """Decode one stable atlas identity into its abstract scaffold, without geometry."""
    edges = topology["edges"]
    if len(representative) != len(edges) or any(
        digit not in DIGIT_COLORS for digit in representative
    ):
        raise ValueError("representative digits do not match the topology encoding")
    return ContactScaffold(
        ("one-angle-class",) * 5,
        tuple(
            ContactEdge(left, right, *DIGIT_COLORS[digit])
            for (left, right), digit in zip(edges, representative, strict=True)
        ),
        ((),) * 5,
    )


def _require_valid_atlas(atlas: dict[str, Any]) -> None:
    problems = schema_errors(atlas)
    if problems:
        raise ValueError("invalid contact scaffold atlas: " + "; ".join(problems))
    problems = atlas_errors(atlas)
    if problems:
        raise ValueError("invalid contact scaffold atlas: " + "; ".join(problems))


def scaffold_by_identity(atlas: dict[str, Any], identity: str) -> ContactScaffold:
    """Decode one retained stable identity, rejecting non-representative codes."""
    _require_valid_atlas(atlas)
    topology_id, separator, representative = identity.partition("/")
    if not separator or not topology_id or not representative or "/" in representative:
        raise ValueError("identity must be <topology-id>/<representative-digit-string>")
    topology = next((item for item in atlas["topologies"] if item["id"] == topology_id), None)
    if topology is None:
        raise ValueError(f"unknown contact scaffold topology: {topology_id}")
    if representative not in topology["representatives"]:
        raise ValueError(f"identity is not a retained orbit representative: {identity}")
    return decode_representative(topology, representative)


def identity_record(atlas: dict[str, Any], identity: str) -> dict[str, Any]:
    """Return a JSON-ready abstract record for one retained identity."""
    scaffold = scaffold_by_identity(atlas, identity)
    topology_id, _, representative = identity.partition("/")
    return {
        "abstract_scaffold": {
            "contact_edges": [
                {
                    "left": edge.left,
                    "normal": edge.normal,
                    "right": edge.right,
                    "sign": edge.sign,
                }
                for edge in scaffold.edges
            ],
            "vertex_count": len(scaffold.vertex_colors),
            "wall_colors": [list(walls) for walls in scaffold.wall_contacts],
        },
        "claim_status": "abstract-only-no-geometry-no-feasibility-no-packing-verdict",
        "identity": identity,
        "representative": representative,
        "semantics": (
            "signed contact-incidence colors only; no square positions or physical realization"
        ),
        "topology_id": topology_id,
    }


def iter_atlas_scaffolds(
    atlas: dict[str, Any],
) -> Iterator[tuple[str, ContactScaffold]]:
    """Yield every composite atlas identity and decoded abstract scaffold in order."""
    _require_valid_atlas(atlas)
    for topology in atlas["topologies"]:
        for representative in topology["representatives"]:
            yield (
                f"{topology['id']}/{representative}",
                decode_representative(topology, representative),
            )


def _text(
    parent: Any,
    *,
    x: int,
    y: int,
    value: str,
    size: int,
    fill: str,
    weight: str = "400",
    anchor: str = "start",
) -> None:
    sub(
        parent,
        "text",
        {
            "x": str(x),
            "y": str(y),
            "fill": fill,
            "font-size": str(size),
            "font-weight": weight,
            "text-anchor": anchor,
        },
    ).text = value


def render_overview(topologies: list[dict[str, Any]]) -> str:
    """Render only abstract graph topologies and counts, never packing coordinates."""
    root = element(
        "svg",
        {
            "viewBox": "0 0 1200 1410",
            "width": "1200",
            "height": "1410",
            "role": "img",
            "aria-labelledby": "figure-title figure-description",
            "font-family": "Inter, ui-sans-serif, system-ui, sans-serif",
        },
    )
    append_title_desc(
        root,
        "Size-five abstract contact-scaffold atlas",
        "Twenty-one connected graph topologies with exact signed-axis color-orbit counts. "
        "The diagrams are abstract incidence graphs, not realized square packings.",
    )
    append_metadata(
        root,
        {
            "artifact-kind": "abstract-contact-scaffold-topology-overview",
            "claim-status": "no-geometry-no-packing-verdict",
            "generator": GENERATOR,
            "orbit-count": "11013",
            "topology-count": "21",
        },
        coordinates="abstract-diagram-layout; svg-y-down; no-packing-coordinates",
    )
    sub(root, "rect", {"width": "1200", "height": "1410", "fill": PAPER_THEME.background})
    _text(
        root,
        x=48,
        y=52,
        value="Size-five contact scaffolds",
        size=30,
        fill=PAPER_THEME.ink,
        weight="700",
    )
    _text(
        root,
        x=48,
        y=82,
        value="11,013 signed-axis color orbits across 21 connected topologies",
        size=17,
        fill=PAPER_THEME.muted,
    )
    _text(
        root,
        x=1152,
        y=52,
        value="ABSTRACT · NO GEOMETRY",
        size=14,
        fill="#d95f02",
        weight="700",
        anchor="end",
    )

    for index, topology in enumerate(topologies):
        column, row = index % 3, index // 3
        x, y = 40 + 380 * column, 112 + 174 * row
        accent = color_for_square(index)
        card = sub(root, "g", {"id": f"card-{topology['id'].lower()}"})
        sub(
            card,
            "rect",
            {
                "x": str(x),
                "y": str(y),
                "width": "350",
                "height": "150",
                "rx": "14",
                "fill": PAPER_THEME.panel,
                "stroke": accent,
                "stroke-width": "2",
            },
        )
        center_x, center_y = x + 86, y + 78
        points = [(center_x + dx, center_y + dy) for dx, dy in VERTEX_OFFSETS]
        for left, right in topology["edges"]:
            start, end = points[left], points[right]
            sub(
                card,
                "line",
                {
                    "x1": str(start[0]),
                    "y1": str(start[1]),
                    "x2": str(end[0]),
                    "y2": str(end[1]),
                    "stroke": PAPER_THEME.muted,
                    "stroke-width": "2.5",
                    "stroke-linecap": "round",
                },
            )
        for vertex, (point_x, point_y) in enumerate(points):
            sub(
                card,
                "circle",
                {
                    "cx": str(point_x),
                    "cy": str(point_y),
                    "r": "10",
                    "fill": color_for_square(vertex),
                    "stroke": PAPER_THEME.container,
                    "stroke-width": "1.25",
                },
            )
        _text(
            card,
            x=x + 158,
            y=y + 38,
            value=topology["id"],
            size=18,
            fill=PAPER_THEME.ink,
            weight="700",
        )
        _text(
            card,
            x=x + 158,
            y=y + 70,
            value=f"{topology['orbit_count']:,} color orbits",
            size=20,
            fill=accent,
            weight="700",
        )
        _text(
            card,
            x=x + 158,
            y=y + 99,
            value=f"{topology['edge_count']} contact edges",
            size=15,
            fill=PAPER_THEME.muted,
        )
        _text(
            card,
            x=x + 158,
            y=y + 124,
            value=f"IDs: {topology['id']}/000…",
            size=13,
            fill=PAPER_THEME.muted,
        )

    _text(
        root,
        x=48,
        y=1372,
        value=(
            "Edges encode only abstract signed u/v contact relations. No square positions, "
            "container fit, non-overlap, or packing claim is shown."
        ),
        size=14,
        fill=PAPER_THEME.muted,
    )
    return serialize_svg(root)


def atlas_errors(atlas: dict[str, Any]) -> list[str]:
    """Return cross-field failures not expressible in the JSON Schema."""
    errors = []
    topologies = atlas["topologies"]
    expected_edges = connected_topology_representatives(5)
    if [tuple(map(tuple, topology["edges"])) for topology in topologies] != list(
        expected_edges
    ):
        errors.append("topology edge representatives are missing, duplicated, or reordered")
    if [topology["id"] for topology in topologies] != [
        f"T5-{index:02d}" for index in range(1, 22)
    ]:
        errors.append("topology IDs must be contiguous and ordered")
    total = 0
    for topology in topologies:
        representatives = topology["representatives"]
        if topology["edge_count"] != len(topology["edges"]):
            errors.append(f"{topology['id']}: edge count mismatch")
        if topology["orbit_count"] != len(representatives):
            errors.append(f"{topology['id']}: orbit count mismatch")
        if len(set(representatives)) != len(representatives):
            errors.append(f"{topology['id']}: duplicate representative")
        if representatives != sorted(representatives):
            errors.append(f"{topology['id']}: representatives are not ordered")
        if any(len(code) != topology["edge_count"] for code in representatives):
            errors.append(f"{topology['id']}: representative width mismatch")
        total += len(representatives)
    if total != atlas["counts"]["orbit_count"]:
        errors.append("topology orbit counts do not sum to the atlas total")
    return errors


def schema_errors(atlas: dict[str, Any]) -> list[str]:
    """Return enforced structural-schema failures for mutation controls."""
    schema = safe_load(SCHEMA.read_text(encoding="utf-8"))
    return [
        problem.message
        for problem in sorted(
            Draft202012Validator(schema).iter_errors(atlas),
            key=lambda problem: list(problem.path),
        )
    ]


def expected_outputs() -> tuple[dict[str, Any], str]:
    proposals = enumerate_isomorph_free_scaffolds(
        5,
        maximum_colorings=2_000_000,
        maximum_emitted_scaffolds=100_000,
    )
    if proposals.status != "completed":
        raise RuntimeError(f"contact scaffold atlas reached {proposals.limit_kind}")
    grouped: dict[tuple[tuple[int, int], ...], list[str]] = defaultdict(list)
    for scaffold in proposals.scaffolds:
        grouped[_topology(scaffold)].append(_coloring(scaffold))
    topologies = [
        {
            "edge_count": len(edges),
            "edges": [list(edge) for edge in edges],
            "id": f"T5-{index:02d}",
            "orbit_count": len(codes),
            "representatives": codes,
        }
        for index, (edges, codes) in enumerate(grouped.items(), start=1)
    ]
    rendering = render_overview(topologies)
    document = {
        "softschema": {
            "contract": "packing.squares:ContactScaffoldAtlas/v1",
            "envelope": "atlas",
            "schema": "contact-scaffold-atlas.schema.yaml",
            "status": "enforced",
        },
        "atlas": {
            "claim_status": "abstract-contact-scaffolds-no-geometry-no-packing-verdict",
            "counts": {
                "orbit_action_images": proposals.orbit_action_images,
                "orbit_count": len(proposals.scaffolds),
                "topology_coloring_candidates": proposals.required_colorings,
                "topology_count": proposals.topology_count,
            },
            "encoding": {
                "color_digits": {
                    "0": "u-normal-minus",
                    "1": "u-normal-plus",
                    "2": "v-normal-minus",
                    "3": "v-normal-plus",
                },
                "edge_order": "lexicographic unordered vertex pairs in each topology",
                "identity": "<topology-id>/<representative-digit-string>",
            },
            "generated_by": GENERATOR,
            "rendering": {
                "path": str(RENDERING.relative_to(ROOT)),
                "semantics": "abstract-topology-count-overview-not-packing-geometry",
            },
            "scope": (
                "connected size-five graphs, one semantic angle class, no walls; every "
                "present edge has one signed u/v normal color"
            ),
            "topologies": topologies,
        },
    }
    errors = atlas_errors(document["atlas"])
    if errors:
        raise ValueError("invalid contact scaffold atlas: " + "; ".join(errors))
    problems = schema_errors(document["atlas"])
    if problems:
        raise ValueError(f"contact scaffold atlas schema failure: {problems[0]}")
    return document, rendering


def update() -> None:
    document, rendering = expected_outputs()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(_json_text(document), encoding="utf-8")
    write_svg_atomic(RENDERING, rendering)
    print("contact scaffold atlas updated: 21 topologies, 11013 abstract orbits")


def check() -> None:
    document, rendering = expected_outputs()
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != _json_text(document):
        raise ValueError("abstract contact scaffold atlas is missing or stale")
    if not RENDERING.is_file() or RENDERING.read_text(encoding="utf-8") != rendering:
        raise ValueError("abstract contact scaffold overview is missing or stale")
    print("contact scaffold atlas check passed: 21 topologies, 11013 abstract orbits")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--show", metavar="IDENTITY")
    args = parser.parse_args()
    if args.update:
        update()
    elif args.check:
        check()
    else:
        document = json.loads(OUTPUT.read_text(encoding="utf-8"))
        print(_json_text(identity_record(document["atlas"], args.show)), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
