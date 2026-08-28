#!/usr/bin/env python3
"""Regenerate or check the retained packing SVG gallery and discovery manifest."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import TypedDict
from xml.etree import ElementTree as ET

from strif import atomic_output_file

from cases.small_n.optimal_moduli import build_result as build_small_n_result
from devtools.packing_render_adapters import (
    frame_from_kingbird29,
    frame_from_trump11,
    frames_from_basin_event,
    trajectory_from_n5_equal_side_face,
)
from sqpack.render import (
    PackingFrame,
    PackingTrajectory,
    RenderSpec,
    ViewLevel,
    render_packing_svg,
)
from sqpack.render.svg import RENDERER_VERSION, write_svg_atomic

ROOT = Path(__file__).resolve().parents[1]

RENDERING_DIR = ROOT / "atlas/rendering"
MANIFEST_PATH = RENDERING_DIR / "manifest.json"
METRICS_PATH = RENDERING_DIR / "metrics.json"
N3_ARTIFACT = ROOT / "atlas/n-003-optimal-moduli.svg"
SOURCE_RETURN_PATH = ROOT / (
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-031-h-002-n10-source-return.jsonl"
)
SOURCE_RETURN_EVENT_ID = "1bf0f489a5f82333801d4157419d404a865350409c72563679f08dcdb297c7a9"


@dataclass(frozen=True)
class GallerySources:
    trump11: PackingFrame
    kingbird29: PackingFrame
    gobel10_start: PackingFrame
    gobel10_final: PackingFrame
    n5_trajectory: PackingTrajectory


class GalleryExample(TypedDict):
    id: str
    n: int
    title: str
    alt: str
    caption: str
    artifact: str
    frontier_case: str
    view: str
    evidence: str
    motion: bool
    contacts: bool
    generator: str


class GalleryManifest(TypedDict):
    schema_version: int
    renderer_version: str
    gallery_generator: str
    examples: list[GalleryExample]


def _load_source_return_event() -> dict[str, object]:
    for line in SOURCE_RETURN_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line, parse_float=Decimal)
        if event.get("event_id") == SOURCE_RETURN_EVENT_ID:
            return event
    raise ValueError(f"retained source-return event is missing: {SOURCE_RETURN_EVENT_ID}")


def build_gallery_sources() -> GallerySources:
    start, final = frames_from_basin_event(_load_source_return_event())
    return GallerySources(
        trump11=frame_from_trump11(),
        kingbird29=frame_from_kingbird29(),
        gobel10_start=start,
        gobel10_final=final,
        n5_trajectory=trajectory_from_n5_equal_side_face(),
    )


def render_gallery() -> dict[str, str]:
    sources = build_gallery_sources()
    trajectory = sources.n5_trajectory
    return {
        "trump11-overview.svg": render_packing_svg(sources.trump11),
        "kingbird29-overview.svg": render_packing_svg(sources.kingbird29),
        "gobel10-source-return-comparison.svg": render_packing_svg(
            sources.gobel10_final,
            start=sources.gobel10_start,
            spec=RenderSpec(view=ViewLevel.COMPARISON),
        ),
        "n5-exact-face-trajectory.svg": render_packing_svg(
            trajectory.frames[-1],
            trajectory=trajectory,
            spec=RenderSpec(view=ViewLevel.TRAJECTORY),
        ),
    }


def render_n3_moduli() -> str:
    _model, svg = build_small_n_result(3)
    if svg is None:
        raise ValueError("the n=3 known-answer renderer produced no SVG")
    return svg


def build_gallery_manifest() -> GalleryManifest:
    gallery_command = (
        "uv run --frozen --all-extras --group dev python "
        "-m devtools.render_packing_gallery --update"
    )
    return {
        "schema_version": 2,
        "renderer_version": RENDERER_VERSION,
        "gallery_generator": gallery_command,
        "examples": [
            {
                "id": "n3-optimal-moduli",
                "n": 3,
                "title": "Exact optimal configuration space for three squares",
                "alt": (
                    "Exact quotient map for the optimal configurations of three unit "
                    "squares in a square of side two."
                ),
                "caption": (
                    "Two labelled cycles reduce to one quotient interval, with "
                    "representative packings at its distinguished strata."
                ),
                "artifact": "atlas/n-003-optimal-moduli.svg",
                "frontier_case": "frontier/n-003.md",
                "view": "moduli",
                "evidence": "proved-optimum",
                "motion": False,
                "contacts": False,
                "generator": (
                    "uv run --frozen --all-extras --group dev python "
                    "-m cases.small_n.optimal_moduli --n 3 "
                    "--record campaign/series/series-000-smoke-and-calibration/results/"
                    "exp-014-h-032-n3-optimal-moduli.json "
                    "--svg atlas/n-003-optimal-moduli.svg"
                ),
            },
            {
                "id": "n5-exact-face-trajectory",
                "n": 5,
                "title": "Certified exact five-square trajectory",
                "alt": (
                    "Final packing on the certified exact feasible trajectory for five "
                    "unit squares, with certified contacts highlighted in translucent "
                    "tempered yellow."
                ),
                "caption": (
                    "The animated export follows endpoint A, the exact midpoint, and "
                    "endpoint B; translucent tempered-yellow marks show endpoint B's "
                    "certified contacts, "
                    "and reduced-motion and non-CSS viewers show that final endpoint."
                ),
                "artifact": "atlas/rendering/n5-exact-face-trajectory.svg",
                "frontier_case": "frontier/n-005.md",
                "view": "trajectory",
                "evidence": "certified-upper-bound",
                "motion": True,
                "contacts": True,
                "generator": (
                    "uv run --frozen --all-extras --group dev python "
                    "-m devtools.render_packing_svg n5-face "
                    "--view trajectory --output "
                    "atlas/rendering/n5-exact-face-trajectory.svg"
                ),
            },
            {
                "id": "n10-source-return-comparison",
                "n": 10,
                "title": "Göbel source-return comparison",
                "alt": (
                    "Side-by-side comparison of a perturbed Göbel ten-square packing "
                    "and its returned endpoint."
                ),
                "caption": (
                    "A retained numerical source perturbation and the endpoint returned "
                    "by the deterministic quench share one geometric scale."
                ),
                "artifact": "atlas/rendering/gobel10-source-return-comparison.svg",
                "frontier_case": "frontier/n-010.md",
                "view": "comparison",
                "evidence": "candidate",
                "motion": False,
                "contacts": False,
                "generator": (
                    "uv run --frozen --all-extras --group dev python "
                    "-m devtools.render_packing_svg event "
                    "campaign/series/series-000-smoke-and-calibration/results/"
                    "exp-031-h-002-n10-source-return.jsonl --event-id "
                    f"{SOURCE_RETURN_EVENT_ID} --view comparison --output "
                    "atlas/rendering/gobel10-source-return-comparison.svg"
                ),
            },
            {
                "id": "n11-trump-overview",
                "n": 11,
                "title": "Trump exact packing overview",
                "alt": (
                    "Walter Trump exact packing of eleven unit squares, with edge and "
                    "point contacts highlighted in translucent tempered yellow."
                ),
                "caption": (
                    "Six axis-aligned squares surround a five-square block tilted at an "
                    "algebraic angle near 40.18 degrees; translucent tempered-yellow "
                    "segments and dots show contacts certified in the same number "
                    "field."
                ),
                "artifact": "atlas/rendering/trump11-overview.svg",
                "frontier_case": "frontier/n-011.md",
                "view": "overview",
                "evidence": "certified-upper-bound",
                "motion": False,
                "contacts": True,
                "generator": (
                    "uv run --frozen --all-extras --group dev python "
                    "-m devtools.render_packing_svg builtin trump11 "
                    "--output atlas/rendering/trump11-overview.svg"
                ),
            },
            {
                "id": "n29-kingbird-overview",
                "n": 29,
                "title": "Kingbird high-precision packing overview",
                "alt": (
                    "High-precision reconstruction of the Kingbird packing of twenty-nine "
                    "unit squares."
                ),
                "caption": (
                    "The retained roughly 100-digit source is evaluated at 160 decimal "
                    "digits of working precision and tolerance 1e-80, and passes all "
                    "406 separating-axis pair checks; this is a numerically checked "
                    "construction, not an exact certificate."
                ),
                "artifact": "atlas/rendering/kingbird29-overview.svg",
                "frontier_case": "frontier/n-029.md",
                "view": "overview",
                "evidence": "numerically-checked",
                "motion": False,
                "contacts": False,
                "generator": (
                    "uv run --frozen --all-extras --group dev python "
                    "-m devtools.render_packing_svg builtin kingbird29 "
                    "--output atlas/rendering/kingbird29-overview.svg"
                ),
            },
        ],
    }


def build_gallery_metrics(rendered: dict[str, str], n3_svg: str) -> dict[str, object]:
    documents = {"n-003-optimal-moduli.svg": n3_svg}
    documents.update(rendered)
    records = {}
    for name, text in sorted(documents.items()):
        root = ET.fromstring(text)
        records[name] = {
            "bytes": len(text.encode()),
            "elements": sum(1 for _ in root.iter()),
            "renderer_version": RENDERER_VERSION,
            "viewBox": root.attrib["viewBox"],
        }
    return {"schema_version": 1, "fixtures": records}


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def _write_text_atomic(path: Path, text: str) -> None:
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(text, encoding="utf-8")


def write_gallery() -> None:
    rendered = render_gallery()
    n3_svg = render_n3_moduli()
    for name, text in rendered.items():
        write_svg_atomic(RENDERING_DIR / name, text)
    _write_text_atomic(N3_ARTIFACT, n3_svg)
    _write_text_atomic(METRICS_PATH, _json_text(build_gallery_metrics(rendered, n3_svg)))
    _write_text_atomic(MANIFEST_PATH, _json_text(build_gallery_manifest()))


def check_gallery() -> None:
    rendered = render_gallery()
    n3_svg = render_n3_moduli()
    for name, text in rendered.items():
        path = RENDERING_DIR / name
        if path.read_text(encoding="utf-8") != text:
            raise ValueError(f"retained SVG differs from deterministic render: {path}")
    if N3_ARTIFACT.read_text(encoding="utf-8") != n3_svg:
        raise ValueError("retained n=3 SVG differs from deterministic render")
    expected_metrics = _json_text(build_gallery_metrics(rendered, n3_svg))
    if METRICS_PATH.read_text(encoding="utf-8") != expected_metrics:
        raise ValueError("retained SVG metrics differ from deterministic render")
    expected_manifest = _json_text(build_gallery_manifest())
    if MANIFEST_PATH.read_text(encoding="utf-8") != expected_manifest:
        raise ValueError("retained SVG manifest differs from deterministic gallery")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true", help="regenerate retained files")
    mode.add_argument("--check", action="store_true", help="byte-check retained files")
    mode.add_argument("--list", action="store_true", help="list discoverable examples")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.update:
            write_gallery()
            action = "updated"
        elif args.check:
            check_gallery()
            action = "checked"
        else:
            for example in build_gallery_manifest()["examples"]:
                print(f"{example['id']}\t{example['artifact']}")
            return 0
    except (KeyError, OSError, TypeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    count = len(build_gallery_manifest()["examples"])
    print(f"SVG GALLERY {action.upper()}: {count} examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
