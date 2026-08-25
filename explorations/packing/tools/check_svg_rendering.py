#!/usr/bin/env python3
"""Exercise the deterministic SVG renderer and replay its retained artifacts."""

from __future__ import annotations

import argparse
import math
import os
import re
import subprocess
import sys
from dataclasses import replace
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _rejects(function, *args, **kwargs) -> bool:
    try:
        function(*args, **kwargs)
    except (TypeError, ValueError):
        return True
    return False


def run_model_controls() -> dict[str, bool]:
    from sqpack.render.model import (
        EvidenceTier,
        PackingFrame,
        Point2,
        RigidPose,
        SquareGeometry,
        VerificationSummary,
        validate_frame,
    )
    from sqpack.render.numbers import scalar_from_float

    scalar = scalar_from_float(1.0)
    corners = tuple(
        Point2(scalar_from_float(x), scalar_from_float(y))
        for x, y in ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))
    )
    square = SquareGeometry("square-0", corners, RigidPose(corners[0], scalar_from_float(0.0)))
    verified = VerificationSummary(valid=True, method="exact", detail="known-answer")
    frame = PackingFrame(scalar, (square,), EvidenceTier.VERIFIED_CONSTRUCTION, verified)
    validate_frame(frame)
    return {
        "duplicate_ids_rejected": _rejects(
            validate_frame, replace(frame, squares=(square, square))
        ),
        "unstable_order_rejected": _rejects(
            validate_frame,
            replace(frame, squares=(replace(square, square_id="square-1"), square)),
        ),
        "unverified_evidence_rejected": _rejects(
            validate_frame, replace(frame, verification=replace(verified, valid=False))
        ),
    }


def run_number_controls() -> dict[str, bool]:
    from sqpack.render.model import ScalarKind
    from sqpack.render.numbers import (
        format_svg_number,
        project_decimal,
        scalar_from_exact,
        scalar_from_float,
        scalar_from_fraction,
    )

    precise = Decimal("3.87708359002281417730789706010096")
    return {
        "negative_zero_normalized": format_svg_number(Decimal("-0")) == "0",
        "fraction_preserved": scalar_from_fraction(Fraction(1, 3)).source == "1/3",
        "binary64_identified": scalar_from_float(0.1).kind is ScalarKind.BINARY64,
        "exact_source_required": _rejects(scalar_from_exact, "", precise),
        "nonfinite_rejected": _rejects(scalar_from_float, math.inf),
        "precision_is_local": project_decimal(precise, 24)
        == Decimal("3.87708359002281417730790"),
    }


def build_fixtures():
    from render_packing_gallery import build_gallery_sources

    sources = build_gallery_sources()
    return {
        "trump11-overview.svg": sources.trump11,
        "gobel10-source-return-comparison.svg": (
            sources.gobel10_start,
            sources.gobel10_final,
        ),
        "n5-exact-face-trajectory.svg": sources.n5_trajectory,
    }


def run_xml_controls() -> dict[str, bool]:
    from xml.etree import ElementTree as ET

    from sqpack.render.svg import (
        MOTION_MARKER,
        append_exact_comment,
        append_local_use,
        element,
        serialize_svg,
        sub,
        validate_safe_tree,
    )

    root = element("svg")
    append_exact_comment(root, "x = 1/3")
    text = serialize_svg(root)
    bad = element("svg")
    ET.SubElement(bad, "script")
    duplicate = element("svg")
    ET.SubElement(duplicate, "rect", {"id": "same"})
    ET.SubElement(duplicate, "circle", {"id": "same"})
    foreign_namespace = element("svg")
    ET.SubElement(foreign_namespace, "{https://example.com/evil}rect")
    arbitrary_css = element("svg")
    sub(
        arbitrary_css,
        "style",
        {"data-sqpack-style": MOTION_MARKER},
    ).text = "@media (prefers-reduced-motion: no-preference){rect{fill:none}}"
    return {
        "comment_round_trip": "<!--x = 1/3-->" in text,
        "invalid_comment_rejected": _rejects(append_exact_comment, root, "bad -- comment"),
        "script_rejected": _rejects(validate_safe_tree, bad),
        "duplicate_xml_ids_rejected": _rejects(validate_safe_tree, duplicate),
        "external_use_rejected": _rejects(append_local_use, root, "https://example.com/x"),
        "local_use_accepted": append_local_use(root, "#shape").attrib["href"] == "#shape",
        "foreign_namespace_rejected": _rejects(validate_safe_tree, foreign_namespace),
        "arbitrary_marked_css_rejected": _rejects(validate_safe_tree, arbitrary_css),
    }


def run_geometry_controls() -> dict[str, bool]:
    from xml.etree import ElementTree as ET

    from sqpack.render import (
        AnnotationLevel,
        Overlay,
        RenderSpec,
        ViewLevel,
        render_packing_svg,
    )
    from sqpack.render.adapters import frame_from_gobel10, frame_from_trump11
    from sqpack.render.model import ActiveFeature, ContactFeature
    from sqpack.render.style import evidence_style

    overview = render_packing_svg(frame_from_trump11(), spec=RenderSpec())
    trump = frame_from_trump11()
    start = frame_from_gobel10()
    comparison = render_packing_svg(
        start,
        start=start,
        spec=RenderSpec(view=ViewLevel.COMPARISON),
    )
    comparison_root = ET.fromstring(comparison)
    _min_x, _min_y, viewport_width, viewport_height = (
        Decimal(value) for value in comparison_root.attrib["viewBox"].split()
    )
    panel_containers = [
        next(child for child in panel if child.tag.endswith("}rect"))
        for panel in comparison_root.iter()
        if "data-panel" in panel.attrib
    ]
    point = start.squares[0].corners[0]
    featured = replace(
        start,
        features=(
            ActiveFeature("feature-0", point, "active wall", "square-00"),
            ContactFeature("feature-1", point, ("square-00", "square-01")),
        ),
    )
    overlay = render_packing_svg(
        featured,
        spec=RenderSpec(overlays=frozenset({Overlay.CONTACTS, Overlay.ACTIVE_FEATURES})),
    )
    event_start, _event_final = build_fixtures()["gobel10-source-return-comparison.svg"]
    exact_text = render_packing_svg(
        event_start, spec=RenderSpec(annotations=AnnotationLevel.EXACT)
    )
    event_pose = event_start.squares[0].pose
    if event_pose is None:
        raise ValueError("BasinEvent fixture lost its pose")
    source_x = event_pose.centre.x.source
    return {
        "overview_is_svg": overview.startswith("<?xml") and "<polygon" in overview,
        "comparison_has_two_panels": comparison.count('data-panel="') == 2,
        "comparison_panels_fit_viewport": all(
            Decimal(container.attrib["x"]) >= 0
            and Decimal(container.attrib["y"]) >= 0
            and Decimal(container.attrib["x"]) + Decimal(container.attrib["width"])
            <= viewport_width
            and Decimal(container.attrib["y"]) + Decimal(container.attrib["height"])
            <= viewport_height
            for container in panel_containers
        ),
        "typed_overlays_render": overlay.count('data-feature="') == 2,
        "evidence_tokens_are_distinct": len(
            {evidence_style(tier) for tier in type(start.evidence)}
        )
        == 4,
        "decimal_source_round_trips": source_x in exact_text,
        "exact_projection_is_high_precision": str(trump.container_side.projected).startswith(
            "3.877083590022814177307897"
        ),
    }


def run_animation_controls() -> dict[str, bool]:
    from sqpack.render import RenderSpec, ViewLevel, render_packing_svg
    from sqpack.render.adapters import trajectory_from_n5_equal_side_face

    trajectory = trajectory_from_n5_equal_side_face()
    text = render_packing_svg(
        trajectory.frames[-1],
        trajectory=trajectory,
        spec=RenderSpec(view=ViewLevel.TRAJECTORY),
    )
    changed_square = replace(trajectory.frames[0].squares[0], square_id="square-X")
    mismatched = replace(
        trajectory,
        frames=(
            replace(
                trajectory.frames[0],
                squares=(changed_square, *trajectory.frames[0].squares[1:]),
            ),
            *trajectory.frames[1:],
        ),
    )
    return {
        "motion_is_reduced_motion_scoped": "prefers-reduced-motion: no-preference" in text,
        "no_smil": "<animate" not in text,
        "final_state_is_underlying": 'data-static-fallback="final"' in text,
        "mismatched_tracks_rejected": _rejects(
            render_packing_svg,
            trajectory.frames[-1],
            trajectory=mismatched,
            spec=RenderSpec(view=ViewLevel.TRAJECTORY),
        ),
        "invalid_duration_rejected": _rejects(
            render_packing_svg,
            trajectory.frames[-1],
            trajectory=trajectory,
            spec=RenderSpec(view=ViewLevel.TRAJECTORY, duration_seconds=Decimal(0)),
        ),
    }


def _rendered_fixtures() -> dict[str, str]:
    from render_packing_gallery import render_gallery

    return render_gallery()


def run_determinism_matrix() -> dict[str, bool]:
    expected = _rendered_fixtures()
    controls = {}
    environments = (
        {"PYTHONHASHSEED": "1", "TZ": "UTC", "LC_ALL": "C"},
        {"PYTHONHASHSEED": "8675309", "TZ": "America/Los_Angeles", "LC_ALL": "C"},
    )
    for name, text in expected.items():
        probes = []
        for overrides in environments:
            environment = os.environ.copy()
            environment.update(overrides)
            probes.append(
                subprocess.check_output(
                    [sys.executable, str(Path(__file__)), "--probe", name],
                    env=environment,
                    text=True,
                )
            )
        controls[name] = all(probe == text for probe in probes)
    return controls


def run_portability_controls() -> dict[str, bool]:
    texts = _rendered_fixtures().values()
    return {
        "self_contained": all(
            "http://" not in text.replace("http://www.w3.org/2000/svg", "") for text in texts
        ),
        "no_external_features": all(
            token not in text
            for text in texts
            for token in ("<!DOCTYPE", "<script", "foreignObject", "xlink:", "@import", "url(")
        ),
    }


def run_gallery_controls() -> dict[str, bool]:
    from render_packing_gallery import build_gallery_manifest

    manifest = build_gallery_manifest()
    examples = manifest["examples"]
    ids = [example["id"] for example in examples]
    cases = [ROOT / example["frontier_case"] for example in examples]
    artifacts = [ROOT / example["artifact"] for example in examples]

    def embeds(document: str, artifact: str) -> bool:
        document_path = ROOT / document
        relative = os.path.relpath(ROOT / artifact, document_path.parent)
        text = document_path.read_text(encoding="utf-8")
        pattern = rf"!\[[^\]]+\]\({re.escape(relative)}\)"
        return re.search(pattern, text) is not None

    by_id = {example["id"]: example for example in examples}
    surface_expectations = {
        "README.md": ("n10-source-return-comparison", "n11-trump-overview"),
        "TUTORIAL.md": (
            "n3-optimal-moduli",
            "n10-source-return-comparison",
            "n11-trump-overview",
        ),
        "SYNOPSIS.md": ("n5-exact-face-trajectory", "n11-trump-overview"),
        "atlas/README.md": ("n3-optimal-moduli", "n11-trump-overview"),
    }
    return {
        "gallery_has_four_known_answers": len(examples) == 4,
        "gallery_ids_are_unique": len(ids) == len(set(ids)),
        "gallery_covers_expected_n": [example["n"] for example in examples] == [3, 5, 10, 11],
        "frontier_cases_exist": all(path.is_file() for path in cases),
        "gallery_artifacts_exist": all(path.is_file() for path in artifacts),
        "gallery_alt_text_is_nonempty": all(example["alt"].strip() for example in examples),
        "gallery_commands_are_explicit": all(
            example["generator"].startswith("uv run --frozen python tools/")
            for example in examples
        ),
        "frontier_cases_embed_gallery_artifacts": all(
            embeds(example["frontier_case"], example["artifact"]) for example in examples
        ),
        "gallery_readme_embeds_every_artifact": all(
            embeds("atlas/rendering/README.md", example["artifact"]) for example in examples
        ),
        "exposition_surfaces_embed_expected_examples": all(
            embeds(document, by_id[example_id]["artifact"])
            for document, example_ids in surface_expectations.items()
            for example_id in example_ids
        ),
        "atlas_documents_manifest": "[`manifest.json`](rendering/manifest.json)"
        in (ROOT / "atlas/README.md").read_text(encoding="utf-8"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--model-numbers", action="store_true")
    parser.add_argument("--probe", choices=tuple(_rendered_fixtures()))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.probe:
        sys.stdout.write(_rendered_fixtures()[args.probe])
        return 0
    controls = {**run_model_controls(), **run_number_controls()}
    if not args.model_numbers:
        controls |= run_xml_controls()
        controls |= run_geometry_controls()
        controls |= run_animation_controls()
        controls |= run_determinism_matrix()
        controls |= run_portability_controls()
        controls |= run_gallery_controls()
        if args.update:
            from render_packing_gallery import write_gallery

            write_gallery()
        elif args.check:
            from render_packing_gallery import check_gallery

            check_gallery()
    failed = [name for name, passed in controls.items() if not passed]
    if failed:
        raise ValueError(f"SVG rendering controls failed: {failed}")
    print(f"SVG RENDERING CHECKS PASSED: {len(controls)} controls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
