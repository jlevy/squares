"""Overview, comparison, and trajectory rendering for square packings."""

from __future__ import annotations

from decimal import Decimal
from xml.etree import ElementTree as ET

from sqpack.render.model import (
    ActiveFeature,
    AnnotationLevel,
    ContactFeature,
    Overlay,
    PackingFrame,
    PackingTrajectory,
    Point2,
    RenderSpec,
    ScalarKind,
    ScalarSource,
    ViewLevel,
    validate_render_request,
)
from sqpack.render.motion import append_motion_styles, append_square_motion
from sqpack.render.numbers import format_points, format_svg_number, format_visible_number
from sqpack.render.style import (
    LAYOUT,
    PAPER_THEME,
    color_for_square,
    evidence_style,
    presentation_attributes,
)
from sqpack.render.svg import (
    append_exact_comment,
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
            "x": format_svg_number(x),
            "y": format_svg_number(y),
            "width": format_svg_number(side * scale),
            "height": format_svg_number(side * scale),
            **presentation_attributes(fill="none", stroke=PAPER_THEME.container, width=3),
        },
    )


def _append_square_id(group: ET.Element, square, projected: tuple[Point2, ...]) -> None:
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


def _append_static_square(
    group: ET.Element,
    square,
    index: int,
    *,
    side: Decimal,
    x: Decimal,
    y: Decimal,
    scale: Decimal,
    show_id: bool,
    motion: bool,
) -> None:
    projected = tuple(
        _project_point(point, side=side, x=x, y=y, scale=scale) for point in square.corners
    )
    node = sub(
        group,
        "polygon",
        {
            "points": format_points(projected),
            "fill-opacity": "0.72",
            "stroke-linejoin": "round",
            **presentation_attributes(fill=color_for_square(index), stroke="#ffffff", width=2),
        },
    )
    if motion:
        append_square_motion(node, square.square_id)
    if show_id:
        _append_square_id(group, square, projected)


def _append_contact_overlay(
    group: ET.Element,
    frame: PackingFrame,
    *,
    side: Decimal,
    x: Decimal,
    y: Decimal,
    scale: Decimal,
) -> None:
    for feature in frame.features:
        if isinstance(feature, ContactFeature):
            point = _project_point(feature.point, side=side, x=x, y=y, scale=scale)
            sub(
                group,
                "circle",
                {
                    "id": feature.feature_id,
                    "cx": format_svg_number(point.x),
                    "cy": format_svg_number(point.y),
                    "r": "5",
                    "fill": PAPER_THEME.ink,
                    "data-feature": "contact",
                    "data-squares": " ".join(feature.square_ids),
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
) -> Decimal:
    left = Decimal(LAYOUT.margin + panel_index * (panel_width + LAYOUT.panel_gap))
    top = Decimal(LAYOUT.margin)
    scale = Decimal(min(panel_width, panel_height)) / shared_side
    group = sub(root, "g", {"id": f"panel-{panel_index}", "data-panel": frame.label})
    if spec.annotations is AnnotationLevel.EXACT:
        append_exact_comment(group, f"container side: {frame.container_side.source}")
    _append_container(group, x=left, y=top, side=frame.container_side.projected, scale=scale)
    for index, square in enumerate(frame.squares):
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
        _append_static_square(
            group,
            square,
            index,
            side=frame.container_side.projected,
            x=left,
            y=top,
            scale=scale,
            show_id=Overlay.SQUARE_IDS in spec.overlays,
            motion=motion,
        )
    if Overlay.CONTACTS in spec.overlays:
        _append_contact_overlay(
            group, frame, side=frame.container_side.projected, x=left, y=top, scale=scale
        )
    if Overlay.ACTIVE_FEATURES in spec.overlays:
        _append_feature_overlay(
            group, frame, side=frame.container_side.projected, x=left, y=top, scale=scale
        )
    _append_caption(root, frame, x=int(left), y=panel_height + LAYOUT.margin + 30)
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
        "evidence": final.evidence.value,
        "source-id": final.source_id,
        "source-url": final.source_url,
        "view": spec.view.value,
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
            )
        )
    if spec.view is ViewLevel.TRAJECTORY and trajectory is not None:
        append_motion_styles(
            root, trajectory, scale=scales[0], duration_seconds=spec.duration_seconds
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
