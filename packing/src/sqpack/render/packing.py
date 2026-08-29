"""Overview, comparison, and trajectory rendering for square packings."""

from __future__ import annotations

from decimal import Decimal
from xml.etree import ElementTree as ET

from sqpack.render.color import (
    ANGLE_CLASS_CONTRACT,
    AngleHueRegistry,
    SquareColor,
    assign_square_colors,
)
from sqpack.render.model import (
    ActiveFeature,
    AnnotationLevel,
    ContactFeature,
    DetectedContactFeature,
    HueScheme,
    Overlay,
    PackingFrame,
    PackingTrajectory,
    Point2,
    RenderSpec,
    ScalarKind,
    ScalarSource,
    SquareGeometry,
    ViewLevel,
    validate_render_request,
)
from sqpack.render.motion import (
    append_final_overlay_motion,
    append_motion_styles,
    append_square_motion,
)
from sqpack.render.numbers import format_points, format_svg_number, format_visible_number
from sqpack.render.style import (
    CONTACT_CENSUS_COLOR,
    CONTACT_CENSUS_DASH,
    CONTACT_CENSUS_OPACITY,
    CONTACT_CENSUS_STROKE_WIDTH,
    CONTACT_CLIP_POLICY,
    CONTACT_HIGHLIGHT_OPACITY,
    LAYOUT,
    PAPER_THEME,
    SQUARE_FILL_OPACITY,
    evidence_style,
    presentation_attributes,
)
from sqpack.render.svg import (
    append_exact_comment,
    append_local_use,
    append_metadata,
    append_title_desc,
    element,
    serialize_svg,
    sub,
)


def _select_frames(
    final: PackingFrame,
    start: PackingFrame | None,
    trajectory: PackingTrajectory | None,
    view: ViewLevel,
) -> tuple[PackingFrame, ...]:
    if view is ViewLevel.OVERVIEW:
        return (final,)
    if view is ViewLevel.COMPARISON:
        if start is None:
            raise ValueError("comparison requires start")
        return (start, final)
    if trajectory is None:
        raise ValueError("trajectory requires frames")
    return (trajectory.frames[-1],)


def _shared_extent(frames: tuple[PackingFrame, ...]) -> Decimal:
    return max(frame.container_side.projected for frame in frames)


def _panel_layout(panel_count: int, width: int) -> tuple[int, int, int]:
    height = 680
    panel_width = (
        width - 2 * LAYOUT.margin - (panel_count - 1) * LAYOUT.panel_gap
    ) // panel_count
    return panel_width, height - LAYOUT.caption_height - 2 * LAYOUT.margin, height


def _project_point(
    point: Point2, *, side: Decimal, x: Decimal, y: Decimal, scale: Decimal
) -> Point2:
    def scalar(value: Decimal) -> ScalarSource:
        return ScalarSource(ScalarKind.DECIMAL, str(value), value, 32)

    return Point2(
        scalar(x + point.x.projected * scale), scalar(y + (side - point.y.projected) * scale)
    )


def _append_container(
    group: ET.Element, *, x: Decimal, y: Decimal, side: Decimal, scale: Decimal
) -> None:
    sub(
        group,
        "rect",
        {
            "data-feature": "container-outline",
            "x": format_svg_number(x),
            "y": format_svg_number(y),
            "width": format_svg_number(side * scale),
            "height": format_svg_number(side * scale),
            **presentation_attributes(
                fill="none",
                stroke=PAPER_THEME.container,
                width=LAYOUT.stroke_width,
            ),
        },
    )


def _append_square_id(
    group: ET.Element, square: SquareGeometry, projected: tuple[Point2, ...]
) -> None:
    cx = sum((point.x.projected for point in projected), Decimal(0)) / 4
    cy = sum((point.y.projected for point in projected), Decimal(0)) / 4
    sub(
        group,
        "text",
        {
            "x": format_svg_number(cx),
            "y": format_svg_number(cy + 5),
            "text-anchor": "middle",
            "font-size": "14",
            "fill": PAPER_THEME.ink,
        },
    ).text = square.label or square.square_id


def _append_square_fill(
    group: ET.Element,
    square: SquareGeometry,
    color: SquareColor,
    *,
    projected: tuple[Point2, ...],
    motion: bool,
) -> None:
    node = sub(
        group,
        "polygon",
        {
            "data-feature": "square-fill",
            "data-square": square.square_id,
            "data-hue-index": str(color.hue_index),
            "data-shade-index": str(color.shade_index),
            "data-orientation-radians": str(color.orientation_radians),
            "points": format_points(projected),
            "fill": color.fill,
            "fill-opacity": str(SQUARE_FILL_OPACITY),
            "stroke": "none",
        },
    )
    if color.angle_class is not None:
        node.set("data-angle-class", str(color.angle_class))
    if color.angle_class_residual_radians is not None:
        node.set(
            "data-angle-class-residual-radians",
            str(color.angle_class_residual_radians),
        )
    if color.contact_sides is not None:
        node.set("data-contact-sides", str(color.contact_sides))
        node.set("data-full-side-contacts", " ".join(color.full_side_contacts))
    if color.maximum_contact_residual is not None:
        node.set("data-maximum-contact-residual", str(color.maximum_contact_residual))
    if motion:
        append_square_motion(node, square.square_id)


def _append_square_outline(
    group: ET.Element,
    square: SquareGeometry,
    *,
    projected: tuple[Point2, ...],
    motion: bool,
) -> None:
    node = sub(
        group,
        "polygon",
        {
            "data-feature": "square-outline",
            "data-square": square.square_id,
            "points": format_points(projected),
            "stroke-linejoin": "round",
            **presentation_attributes(
                fill="none",
                stroke=PAPER_THEME.container,
                width=LAYOUT.stroke_width,
            ),
        },
    )
    if motion:
        append_square_motion(node, square.square_id)


def _append_contact_overlay(
    group: ET.Element,
    frame: PackingFrame,
    *,
    side: Decimal,
    x: Decimal,
    y: Decimal,
    scale: Decimal,
    panel_index: int,
    projected_squares: dict[str, tuple[Point2, ...]],
    motion: bool,
) -> None:
    contacts = tuple(
        feature for feature in frame.features if isinstance(feature, ContactFeature)
    )
    if not contacts:
        return
    clip_ids: dict[str, str] = {}
    clip_definitions = sub(
        group,
        "defs",
        {"data-contact-clip-policy": CONTACT_CLIP_POLICY},
    )
    clip_shape_ids: dict[str, str] = {}
    for square_id in sorted(
        {square_id for feature in contacts for square_id in feature.square_ids}
    ):
        shape_id = f"panel-{panel_index}-contact-clip-shape-{square_id}"
        clip_shape_ids[square_id] = shape_id
        sub(
            clip_definitions,
            "polygon",
            {
                "id": shape_id,
                "data-feature": "contact-clip-shape",
                "data-square": square_id,
                "points": format_points(projected_squares[square_id]),
            },
        )
    for feature in contacts:
        clip_id = f"panel-{panel_index}-clip-{feature.feature_id}"
        clip_ids[feature.feature_id] = clip_id
        clip = sub(
            clip_definitions,
            "clipPath",
            {
                "id": clip_id,
                "clipPathUnits": "userSpaceOnUse",
                "data-feature": "contact-clip",
                "data-squares": " ".join(feature.square_ids),
            },
        )
        for square_id in feature.square_ids:
            append_local_use(
                clip,
                f"#{clip_shape_ids[square_id]}",
                **{"data-clip-square": square_id},
            )
    overlay = sub(
        group,
        "g",
        {
            "id": f"panel-{panel_index}-contacts",
            "data-layer": "contacts",
            "data-overlay": "contacts",
        },
    )
    if motion:
        append_final_overlay_motion(overlay)
    for feature in contacts:
        start = _project_point(feature.start, side=side, x=x, y=y, scale=scale)
        attributes = {
            "id": f"panel-{panel_index}-{feature.feature_id}",
            "data-squares": " ".join(feature.square_ids),
            "clip-path": f"url(#{clip_ids[feature.feature_id]})",
        }
        if feature.wall is not None:
            attributes["data-wall"] = feature.wall.value
        if feature.end is None:
            sub(
                overlay,
                "circle",
                {
                    **attributes,
                    "cx": format_svg_number(start.x),
                    "cy": format_svg_number(start.y),
                    "r": str(LAYOUT.contact_point_radius),
                    "fill": PAPER_THEME.contact,
                    "fill-opacity": str(CONTACT_HIGHLIGHT_OPACITY),
                    "data-feature": "contact-point",
                },
            )
            continue
        end = _project_point(feature.end, side=side, x=x, y=y, scale=scale)
        sub(
            overlay,
            "line",
            {
                **attributes,
                "x1": format_svg_number(start.x),
                "y1": format_svg_number(start.y),
                "x2": format_svg_number(end.x),
                "y2": format_svg_number(end.y),
                "stroke": PAPER_THEME.contact,
                "stroke-opacity": str(CONTACT_HIGHLIGHT_OPACITY),
                "stroke-width": str(LAYOUT.contact_stroke_width),
                "stroke-linecap": "round",
                "vector-effect": "non-scaling-stroke",
                "data-feature": "contact-segment",
            },
        )


def _append_feature_overlay(
    group: ET.Element,
    frame: PackingFrame,
    *,
    side: Decimal,
    x: Decimal,
    y: Decimal,
    scale: Decimal,
) -> None:
    for feature in frame.features:
        if isinstance(feature, ActiveFeature):
            point = _project_point(feature.point, side=side, x=x, y=y, scale=scale)
            sub(
                group,
                "text",
                {
                    "id": feature.feature_id,
                    "x": format_svg_number(point.x),
                    "y": format_svg_number(point.y),
                    "fill": PAPER_THEME.ink,
                    "data-feature": "active-feature",
                },
            ).text = feature.label


def _append_contact_census_overlay(
    group: ET.Element,
    frame: PackingFrame,
    *,
    side: Decimal,
    x: Decimal,
    y: Decimal,
    scale: Decimal,
    panel_index: int,
    motion: bool,
) -> None:
    features = tuple(
        feature for feature in frame.features if isinstance(feature, DetectedContactFeature)
    )
    if not features:
        return
    overlay = sub(
        group,
        "g",
        {
            "id": f"panel-{panel_index}-contact-census",
            "data-layer": "contact-census",
            "data-overlay": "contact-census",
            "data-semantics": "tolerance-qualified graph edges, not exact contact loci",
        },
    )
    if motion:
        append_final_overlay_motion(overlay)
    for feature in features:
        start = _project_point(feature.start, side=side, x=x, y=y, scale=scale)
        end = _project_point(feature.end, side=side, x=x, y=y, scale=scale)
        attributes = {
            "id": f"panel-{panel_index}-{feature.feature_id}",
            "data-feature": (
                "detected-wall-seating"
                if feature.wall is not None
                else "detected-contact-graph-edge"
            ),
            "data-squares": " ".join(feature.square_ids),
            "data-angle-tolerance-radians": str(feature.angle_tolerance_radians),
            "data-contact-tolerance": str(feature.contact_tolerance),
        }
        if feature.wall is not None:
            attributes["data-wall"] = feature.wall.value
        else:
            attributes["data-normal"] = str(feature.normal)
            attributes["data-residual"] = str(feature.residual)
        sub(
            overlay,
            "line",
            {
                **attributes,
                "x1": format_svg_number(start.x),
                "y1": format_svg_number(start.y),
                "x2": format_svg_number(end.x),
                "y2": format_svg_number(end.y),
                "stroke": CONTACT_CENSUS_COLOR,
                "stroke-opacity": str(CONTACT_CENSUS_OPACITY),
                "stroke-width": str(CONTACT_CENSUS_STROKE_WIDTH),
                "stroke-dasharray": CONTACT_CENSUS_DASH,
                "stroke-linecap": "round",
                "vector-effect": "non-scaling-stroke",
            },
        )


def _append_caption(root: ET.Element, frame: PackingFrame, *, x: int, y: int) -> None:
    label, dash, icon = evidence_style(frame.evidence)
    relation, digits = format_visible_number(frame.container_side, frame.evidence)
    sub(
        root,
        "text",
        {
            "x": str(x),
            "y": str(y),
            "font-size": "18",
            "font-family": "system-ui, sans-serif",
            "fill": PAPER_THEME.ink,
            "data-evidence": frame.evidence.value,
            "stroke-dasharray": dash,
        },
    ).text = f"{icon} {frame.label}: side {relation} {digits} ({label})"


def _append_contact_census_legend(
    root: ET.Element, frame: PackingFrame, *, x: int, y: int
) -> None:
    features = tuple(
        feature for feature in frame.features if isinstance(feature, DetectedContactFeature)
    )
    if not features:
        return
    angles = sorted({feature.angle_tolerance_radians for feature in features})
    contacts = sorted({feature.contact_tolerance for feature in features})
    detail = (
        f"θ≤{angles[0]} rad; contact≤{contacts[0]}"
        if len(angles) == len(contacts) == 1
        else "per-edge tolerances retained in SVG metadata"
    )
    sub(
        root,
        "line",
        {
            "x1": str(x),
            "y1": str(y - 4),
            "x2": str(x + 42),
            "y2": str(y - 4),
            "stroke": CONTACT_CENSUS_COLOR,
            "stroke-opacity": str(CONTACT_CENSUS_OPACITY),
            "stroke-width": str(CONTACT_CENSUS_STROKE_WIDTH),
            "stroke-dasharray": CONTACT_CENSUS_DASH,
            "data-feature": "contact-census-legend-swatch",
        },
    )
    sub(
        root,
        "text",
        {
            "x": str(x + 52),
            "y": str(y),
            "font-size": "13",
            "font-family": "system-ui, sans-serif",
            "fill": PAPER_THEME.muted,
            "data-feature": "contact-census-legend",
        },
    ).text = f"Detected graph ({detail}); not exact contact geometry"


def _append_packing_panel(
    root: ET.Element,
    frame: PackingFrame,
    *,
    panel_index: int,
    panel_width: int,
    panel_height: int,
    shared_side: Decimal,
    spec: RenderSpec,
    motion: bool,
    angle_hue_registry: AngleHueRegistry | None,
) -> Decimal:
    left = Decimal(LAYOUT.margin + panel_index * (panel_width + LAYOUT.panel_gap))
    top = Decimal(LAYOUT.margin)
    scale = Decimal(min(panel_width, panel_height)) / shared_side
    group = sub(root, "g", {"id": f"panel-{panel_index}", "data-panel": frame.label})
    if spec.annotations is AnnotationLevel.EXACT:
        append_exact_comment(group, f"container side: {frame.container_side.source}")
    projected_squares: list[tuple[SquareGeometry, int, tuple[Point2, ...]]] = []
    for index, square in enumerate(frame.squares):
        projected = tuple(
            _project_point(
                point,
                side=frame.container_side.projected,
                x=left,
                y=top,
                scale=scale,
            )
            for point in square.corners
        )
        projected_squares.append((square, index, projected))
        if spec.annotations is AnnotationLevel.EXACT:
            pose_text = ""
            if square.pose is not None:
                pose_text = (
                    f"; pose=({square.pose.centre.x.source}, "
                    f"{square.pose.centre.y.source}, {square.pose.angle.source})"
                )
            append_exact_comment(
                group,
                f"{square.square_id}: "
                + "; ".join(f"({point.x.source}, {point.y.source})" for point in square.corners)
                + pose_text,
            )
    if spec.annotations is AnnotationLevel.EXACT:
        for feature in frame.features:
            if not isinstance(feature, ContactFeature):
                continue
            geometry = f"({feature.start.x.source}, {feature.start.y.source})"
            if feature.end is not None:
                geometry += f" to ({feature.end.x.source}, {feature.end.y.source})"
            append_exact_comment(group, f"{feature.feature_id}: {geometry}")
    fills = sub(
        group,
        "g",
        {"id": f"panel-{panel_index}-fills", "data-layer": "fills"},
    )
    colors = assign_square_colors(frame, spec, angle_hue_registry=angle_hue_registry)
    for square, _index, projected in projected_squares:
        _append_square_fill(
            fills,
            square,
            colors[square.square_id],
            projected=projected,
            motion=motion,
        )
    if Overlay.CONTACTS in spec.overlays:
        _append_contact_overlay(
            group,
            frame,
            side=frame.container_side.projected,
            x=left,
            y=top,
            scale=scale,
            panel_index=panel_index,
            projected_squares={
                square.square_id: projected for square, _index, projected in projected_squares
            },
            motion=motion,
        )
    if Overlay.CONTACT_CENSUS in spec.overlays:
        _append_contact_census_overlay(
            group,
            frame,
            side=frame.container_side.projected,
            x=left,
            y=top,
            scale=scale,
            panel_index=panel_index,
            motion=motion,
        )
    outlines = sub(
        group,
        "g",
        {"id": f"panel-{panel_index}-outlines", "data-layer": "outlines"},
    )
    for square, _index, projected in projected_squares:
        _append_square_outline(
            outlines,
            square,
            projected=projected,
            motion=motion,
        )
    _append_container(
        outlines,
        x=left,
        y=top,
        side=frame.container_side.projected,
        scale=scale,
    )
    if Overlay.SQUARE_IDS in spec.overlays:
        labels = sub(
            group,
            "g",
            {"id": f"panel-{panel_index}-labels", "data-layer": "labels"},
        )
        for square, _index, projected in projected_squares:
            _append_square_id(labels, square, projected)
    if Overlay.ACTIVE_FEATURES in spec.overlays:
        _append_feature_overlay(
            group, frame, side=frame.container_side.projected, x=left, y=top, scale=scale
        )
    _append_caption(root, frame, x=int(left), y=panel_height + LAYOUT.margin + 30)
    if Overlay.CONTACT_CENSUS in spec.overlays:
        _append_contact_census_legend(
            root,
            frame,
            x=int(left),
            y=panel_height + LAYOUT.margin + 56,
        )
    return scale


def build_packing_document(
    final: PackingFrame,
    *,
    start: PackingFrame | None,
    trajectory: PackingTrajectory | None,
    spec: RenderSpec,
) -> ET.Element:
    frames = _select_frames(final, start, trajectory, spec.view)
    panel_count = len(frames)
    width = spec.width if panel_count == 1 else max(spec.width, 1280)
    panel_width, panel_height, height = _panel_layout(panel_count, width)
    root = element(
        "svg",
        {
            "width": str(width),
            "height": str(height),
            "viewBox": f"0 0 {width} {height}",
            "role": "img",
            "aria-labelledby": "figure-title figure-description",
            "data-static-fallback": "final",
        },
    )
    append_title_desc(root, spec.title, spec.description)
    records = {
        "annotations": spec.annotations.value,
        "color-angle-class-contract": ANGLE_CLASS_CONTRACT,
        "color-angle-tolerance-radians": str(spec.angle_tolerance_radians),
        "color-full-side-contact-tolerance": str(spec.full_side_contact_tolerance),
        "color-hue-count": str(spec.hue_count),
        "color-hue-scheme": spec.hue_scheme.value,
        "color-shade-scheme": spec.shade_scheme.value,
        "color-shade-lightness-span": str(spec.shade_lightness_span),
        "color-shades-per-hue": str(spec.shades_per_hue),
        "evidence": final.evidence.value,
        "source-id": final.source_id,
        "source-url": final.source_url,
        "view": spec.view.value,
    }
    if final.check is not None:
        records |= {
            "check-kind": final.check.kind.value,
            "check-method": final.check.method,
            "check-result": "passed" if final.check.passed else "failed",
        }
        records |= {
            f"check-{name}": value
            for name, value in (
                ("arithmetic", final.check.arithmetic),
                ("precision", final.check.precision),
                ("rounding", final.check.rounding),
                ("tolerance", final.check.tolerance),
                ("detail", final.check.detail),
            )
            if value
        }
    if trajectory is not None:
        records |= {
            "trajectory-kind": trajectory.kind.value,
            "trajectory-certificate": trajectory.certificate,
        }
    append_metadata(root, records)
    sub(
        root,
        "rect",
        {"width": str(width), "height": str(height), "fill": PAPER_THEME.background},
    )
    shared_side = _shared_extent(frames)
    angle_hue_registry = (
        AngleHueRegistry(spec.hue_count, spec.angle_tolerance_radians)
        if spec.hue_scheme is HueScheme.ANGLE and spec.view is ViewLevel.COMPARISON
        else None
    )
    if angle_hue_registry is not None:
        assign_square_colors(frames[-1], spec, angle_hue_registry=angle_hue_registry)
    scales = []
    for index, frame in enumerate(frames):
        scales.append(
            _append_packing_panel(
                root,
                frame,
                panel_index=index,
                panel_width=panel_width,
                panel_height=panel_height,
                shared_side=shared_side,
                spec=spec,
                motion=spec.view is ViewLevel.TRAJECTORY,
                angle_hue_registry=angle_hue_registry,
            )
        )
    if spec.view is ViewLevel.TRAJECTORY and trajectory is not None:
        append_motion_styles(
            root,
            trajectory,
            scale=scales[0],
            duration_seconds=spec.duration_seconds,
            reveal_final_overlay=(
                Overlay.CONTACTS in spec.overlays
                and any(
                    isinstance(feature, ContactFeature)
                    for feature in trajectory.frames[-1].features
                )
            )
            or (
                Overlay.CONTACT_CENSUS in spec.overlays
                and any(
                    isinstance(feature, DetectedContactFeature)
                    for feature in trajectory.frames[-1].features
                )
            ),
        )
    return root


def render_packing_svg(
    final: PackingFrame,
    *,
    start: PackingFrame | None = None,
    trajectory: PackingTrajectory | None = None,
    spec: RenderSpec | None = None,
) -> str:
    request = spec or RenderSpec()
    validate_render_request(final, start=start, trajectory=trajectory, spec=request)
    return serialize_svg(
        build_packing_document(final, start=start, trajectory=trajectory, spec=request)
    )
