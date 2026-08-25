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
        ContactFeature,
        ContainerWall,
        EvidenceTier,
        PackingFrame,
        Point2,
        RigidPose,
        SquareGeometry,
        VerificationSummary,
        validate_frame,
    )
    from sqpack.render.numbers import scalar_from_exact, scalar_from_float

    scalar = scalar_from_float(1.0)
    corners = tuple(
        Point2(scalar_from_float(x), scalar_from_float(y))
        for x, y in ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))
    )
    square = SquareGeometry("square-0", corners, RigidPose(corners[0], scalar_from_float(0.0)))
    verified = VerificationSummary(valid=True, method="exact", detail="known-answer")
    frame = PackingFrame(scalar, (square,), EvidenceTier.VERIFIED_CONSTRUCTION, verified)
    validate_frame(frame)
    exact_zero = scalar_from_exact("0", Decimal(0))
    exact_one = scalar_from_exact("1", Decimal(1))
    exact_point = Point2(exact_zero, exact_one)
    wall_contact = ContactFeature(
        "contact-wall-square-0-left",
        exact_point,
        ("square-0",),
        wall=ContainerWall.LEFT,
    )
    contact_frame = replace(frame, features=(wall_contact,))
    validate_frame(contact_frame)
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
        "binary64_contact_rejected": _rejects(
            validate_frame,
            replace(
                frame,
                features=(
                    replace(
                        wall_contact,
                        start=Point2(scalar_from_float(0.0), scalar_from_float(1.0)),
                    ),
                ),
            ),
        ),
        "degenerate_contact_segment_rejected": _rejects(
            validate_frame,
            replace(contact_frame, features=(replace(wall_contact, end=exact_point),)),
        ),
        "bad_wall_participants_rejected": _rejects(
            validate_frame,
            replace(
                contact_frame,
                features=(replace(wall_contact, square_ids=("square-0", "square-1")),),
            ),
        ),
        "uncertified_contact_rejected": _rejects(
            validate_frame,
            replace(contact_frame, evidence=EvidenceTier.CANDIDATE, verification=None),
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


def run_contact_controls() -> dict[str, bool]:
    from sqpack.packings import trump11
    from sqpack.packings.n5_equal_side_face import build_equal_side_face
    from sqpack.render.adapters import frame_from_gobel10, frame_from_trump11
    from sqpack.render.contacts import contact_features_from_exact
    from sqpack.render.model import ContactFeature, ContainerWall
    from sqpack.render.numbers import scalar_from_exact
    from sqpack.verify import Report, exact_sign, verify_packing

    face = build_equal_side_face()
    q, root = face.field.rational, face.field.alpha

    def project(value):
        return scalar_from_exact(repr(value), Decimal(repr(float(value))))

    def contacts(squares, side):
        report = verify_packing(squares, side, sign=exact_sign)
        if not report.valid:
            raise ValueError("contact control fixture is not a valid packing")
        return contact_features_from_exact(
            squares,
            side,
            square_ids=tuple(f"square-{index:02d}" for index in range(len(squares))),
            scalar=project,
            report=report,
        )

    edge_a = ((q(0), q(0)), (q(1), q(0)), (q(1), q(1)), (q(0), q(1)))
    edge_b = ((q(1), q(0)), (q(2), q(0)), (q(2), q(1)), (q(1), q(1)))
    edge_features = contacts((edge_a, edge_b), q(2))
    edge_pairs = [feature for feature in edge_features if feature.wall is None]

    point_a = ((q(0), q(1)), (q(1), q(1)), (q(1), q(2)), (q(0), q(2)))
    point_b = (
        (q(1), q(3) / 2),
        (q(1) + root / 2, q(3) / 2 - root / 2),
        (q(1) + root, q(3) / 2),
        (q(1) + root / 2, q(3) / 2 + root / 2),
    )
    point_features = contacts((point_a, point_b), q(3))
    point_pairs = [feature for feature in point_features if feature.wall is None]

    wall_point_square = (
        (q(0), q(3) / 2),
        (root / 2, q(3) / 2 - root / 2),
        (root, q(3) / 2),
        (root / 2, q(3) / 2 + root / 2),
    )
    wall_point_features = contacts((wall_point_square,), q(3))

    strict_b = ((q(2), q(0)), (q(3), q(0)), (q(3), q(1)), (q(2), q(1)))
    strict_features = contacts((edge_a, strict_b), q(3))
    inconsistent_report = Report(
        valid=True,
        n=2,
        container_contacts=8,
        touching_pairs=1,
        pairs_tested=1,
        touching_pair_indices=[(0, 1)],
    )

    exact_squares, side, _field = trump11.build()
    trump_report = verify_packing(exact_squares, side, sign=exact_sign)
    trump = frame_from_trump11()
    trump_pairs = [
        feature
        for feature in trump.features
        if isinstance(feature, ContactFeature) and feature.wall is None
    ]
    return {
        "wall_edge_is_one_segment": sum(
            feature.wall is ContainerWall.LEFT and feature.end is not None
            for feature in edge_features
        )
        == 1,
        "square_edge_is_one_segment": len(edge_pairs) == 1 and edge_pairs[0].end is not None,
        "point_to_edge_is_one_dot": len(point_pairs) == 1 and point_pairs[0].end is None,
        "wall_point_is_one_dot": len(wall_point_features) == 1
        and wall_point_features[0].wall is ContainerWall.LEFT
        and wall_point_features[0].end is None,
        "strict_pair_has_no_contact": not any(
            feature.wall is None for feature in strict_features
        ),
        "shared_edge_endpoints_are_deduplicated": len(edge_pairs) == 1,
        "inconsistent_pair_geometry_rejected": _rejects(
            contact_features_from_exact,
            (edge_a, strict_b),
            q(3),
            square_ids=("square-00", "square-01"),
            scalar=project,
            report=inconsistent_report,
        ),
        "contact_ids_are_stable": [feature.feature_id for feature in edge_features]
        == sorted(feature.feature_id for feature in edge_features),
        "trump_pair_contacts_match_verifier": len(trump_pairs) == trump_report.touching_pairs,
        "candidate_pose_arrays_have_no_contacts": frame_from_gobel10().features == (),
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
    external_clip = element("svg")
    sub(external_clip, "rect", {"clip-path": "url(https://example.com/shape.svg#clip)"})
    return {
        "comment_round_trip": "<!--x = 1/3-->" in text,
        "invalid_comment_rejected": _rejects(append_exact_comment, root, "bad -- comment"),
        "script_rejected": _rejects(validate_safe_tree, bad),
        "duplicate_xml_ids_rejected": _rejects(validate_safe_tree, duplicate),
        "external_use_rejected": _rejects(append_local_use, root, "https://example.com/x"),
        "local_use_accepted": append_local_use(root, "#shape").attrib["href"] == "#shape",
        "foreign_namespace_rejected": _rejects(validate_safe_tree, foreign_namespace),
        "arbitrary_marked_css_rejected": _rejects(validate_safe_tree, arbitrary_css),
        "external_presentation_url_rejected": _rejects(validate_safe_tree, external_clip),
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
    from sqpack.render.model import ActiveFeature
    from sqpack.render.style import (
        CONTACT_CLIP_POLICY,
        CONTACT_HIGHLIGHT_COLOR,
        CONTACT_HIGHLIGHT_OPACITY,
        CONTACT_HIGHLIGHT_POINT_RADIUS,
        CONTACT_HIGHLIGHT_STROKE_WIDTH,
        LAYOUT,
        PACKING_BOUNDARY_COLOR,
        PACKING_BOUNDARY_WIDTH,
        PAPER_THEME,
        SQUARE_FILL_PALETTE,
        evidence_style,
    )

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
        next(
            child
            for child in panel.iter()
            if child.attrib.get("data-feature") == "container-outline"
        )
        for panel in comparison_root.iter()
        if "data-panel" in panel.attrib
    ]
    overview_root = ET.fromstring(overview)
    overview_panel = next(
        node for node in overview_root.iter() if node.attrib.get("data-panel") == "Trump n=11"
    )
    overview_layers = [
        child for child in overview_panel if child.attrib.get("data-layer") is not None
    ]
    overview_fills = next(
        child for child in overview_layers if child.attrib["data-layer"] == "fills"
    )
    overview_contacts = next(
        child for child in overview_layers if child.attrib["data-layer"] == "contacts"
    )
    overview_outlines = next(
        child for child in overview_layers if child.attrib["data-layer"] == "outlines"
    )
    overview_container = next(
        child
        for child in overview_outlines
        if child.attrib.get("data-feature") == "container-outline"
    )
    overview_squares = [
        child for child in overview_fills if child.attrib.get("data-feature") == "square-fill"
    ]
    overview_square_outlines = [
        child
        for child in overview_outlines
        if child.attrib.get("data-feature") == "square-outline"
    ]
    overview_contact_marks = [
        child
        for child in overview_contacts
        if child.attrib.get("data-feature", "").startswith("contact-")
    ]
    overview_contact_clips = {
        child.attrib["id"]: child
        for child in overview_panel.iter()
        if child.attrib.get("data-feature") == "contact-clip"
    }
    overview_contact_clip_shapes = {
        child.attrib["id"]: child
        for child in overview_panel.iter()
        if child.attrib.get("data-feature") == "contact-clip-shape"
    }
    overview_fills_by_id = {square.attrib["data-square"]: square for square in overview_squares}
    expected_palette = (
        "#378c3f",
        "#00aeee",
        "#c1a0fb",
        "#00b393",
        "#3d63be",
        "#78d7d6",
        "#877deb",
        "#9fce85",
        "#0096b1",
        "#854888",
        "#83c4ff",
        "#3bb360",
        "#008376",
        "#7acfe9",
        "#0079bf",
        "#86a2ff",
        "#865eb1",
        "#7fd6b1",
        "#00afb9",
        "#c18dd8",
    )

    def contact_clip_matches_participants(mark) -> bool:
        reference = mark.attrib.get("clip-path", "")
        if not reference.startswith("url(#") or not reference.endswith(")"):
            return False
        clip = overview_contact_clips.get(reference[5:-1])
        if clip is None or clip.attrib.get("clipPathUnits") != "userSpaceOnUse":
            return False
        participants = tuple(mark.attrib["data-squares"].split())
        uses = tuple(clip)
        return (
            clip.attrib.get("data-squares") == mark.attrib["data-squares"]
            and tuple(use.attrib.get("data-clip-square") for use in uses) == participants
            and all(
                overview_contact_clip_shapes[use.attrib["href"][1:]].attrib.get("points")
                == overview_fills_by_id[square_id].attrib["points"]
                and overview_contact_clip_shapes[use.attrib["href"][1:]].attrib.get(
                    "data-square"
                )
                == square_id
                for square_id, use in zip(participants, uses, strict=True)
            )
        )

    point = trump.squares[0].corners[0]
    featured = replace(
        trump,
        features=(
            ActiveFeature("active-feature-0", point, "active wall", "square-00"),
            *trump.features,
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
    exact_contact_text = render_packing_svg(
        trump, spec=RenderSpec(annotations=AnnotationLevel.EXACT)
    )
    hidden_exact_contact_text = render_packing_svg(
        trump,
        spec=RenderSpec(
            annotations=AnnotationLevel.EXACT,
            overlays=frozenset(),
        ),
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
        "rendered_square_fill_palette_is_selected_cool_set": expected_palette
        == SQUARE_FILL_PALETTE
        and tuple(square.attrib["fill"] for square in overview_squares)
        == tuple(
            expected_palette[index % len(expected_palette)]
            for index in range(len(overview_squares))
        ),
        "packing_outlines_are_thin_opaque_pure_black": PAPER_THEME.container
        == PACKING_BOUNDARY_COLOR
        == "#000000"
        and LAYOUT.stroke_width == PACKING_BOUNDARY_WIDTH == 1.25
        and overview_container.attrib["stroke"] == PACKING_BOUNDARY_COLOR
        and overview_container.attrib["fill"] == "none"
        and len(overview_square_outlines) == len(overview_squares)
        and all(
            square.attrib["stroke"] == PACKING_BOUNDARY_COLOR
            and square.attrib["fill"] == "none"
            and square.attrib["stroke-width"]
            == overview_container.attrib["stroke-width"]
            == str(LAYOUT.stroke_width)
            for square in overview_square_outlines
        ),
        "contact_highlight_is_reserved_tempered_yellow": PAPER_THEME.contact
        == CONTACT_HIGHLIGHT_COLOR
        == "#e3c64a"
        and PAPER_THEME.contact not in expected_palette
        and all(
            mark.attrib.get("fill") == PAPER_THEME.contact
            or mark.attrib.get("stroke") == PAPER_THEME.contact
            for mark in overview_contact_marks
        ),
        "contact_highlights_use_selected_opacity_and_size": CONTACT_HIGHLIGHT_OPACITY == 0.6
        and LAYOUT.contact_stroke_width == CONTACT_HIGHLIGHT_STROKE_WIDTH == 9
        and LAYOUT.contact_point_radius == CONTACT_HIGHLIGHT_POINT_RADIUS == 5.5
        and all(
            (
                mark.attrib.get("stroke-opacity") == str(CONTACT_HIGHLIGHT_OPACITY)
                and mark.attrib.get("stroke-width") == str(CONTACT_HIGHLIGHT_STROKE_WIDTH)
            )
            if mark.attrib["data-feature"] == "contact-segment"
            else (
                mark.attrib.get("fill-opacity") == str(CONTACT_HIGHLIGHT_OPACITY)
                and mark.attrib.get("r") == str(CONTACT_HIGHLIGHT_POINT_RADIUS)
            )
            for mark in overview_contact_marks
        ),
        "contact_highlights_are_clipped_to_participating_squares": CONTACT_CLIP_POLICY
        == "participating-square-union"
        and len(overview_contact_clips) == len(overview_contact_marks)
        and all(contact_clip_matches_participants(mark) for mark in overview_contact_marks),
        "contact_highlights_are_between_fills_and_outlines": [
            layer.attrib["data-layer"] for layer in overview_layers
        ]
        == ["fills", "contacts", "outlines"]
        and all(square.attrib["stroke"] == "none" for square in overview_squares),
        "certified_contacts_render_by_default": 'data-feature="contact-segment"' in overview
        and 'data-feature="contact-point"' in overview,
        "contact_overlay_can_be_removed": 'data-feature="contact-'
        not in render_packing_svg(trump, spec=RenderSpec(overlays=frozenset())),
        "typed_overlays_render": 'data-feature="active-feature"' in overlay
        and 'data-feature="contact-' in overlay,
        "evidence_tokens_are_distinct": len(
            {evidence_style(tier) for tier in type(start.evidence)}
        )
        == 4,
        "decimal_source_round_trips": source_x in exact_text,
        "exact_contact_comments_round_trip": "<!--contact-pair-" in exact_contact_text
        and " to (" in exact_contact_text,
        "hidden_contact_annotations_are_retained": "<!--contact-pair-"
        in hidden_exact_contact_text
        and 'data-feature="contact-' not in hidden_exact_contact_text,
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
        "final_contacts_reveal_at_trajectory_end": 'class="motion-final-overlay"' in text
        and "opacity:0" in text
        and "step-end" in text,
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
            for token in ("<!DOCTYPE", "<script", "foreignObject", "xlink:", "@import")
        ),
        "presentation_urls_are_local_fragments": all(
            re.search(r"url\((?!#[A-Za-z][A-Za-z0-9_.-]*\))", text) is None for text in texts
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
        "gallery_contact_flags_match_exact_sources": {
            example["id"]: example["contacts"] for example in examples
        }
        == {
            "n3-optimal-moduli": False,
            "n5-exact-face-trajectory": True,
            "n10-source-return-comparison": False,
            "n11-trump-overview": True,
        },
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
    controls = {**run_model_controls(), **run_number_controls(), **run_contact_controls()}
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
