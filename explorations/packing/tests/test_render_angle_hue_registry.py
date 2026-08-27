"""Cross-panel contracts for deterministic angle-hue assignment."""

from __future__ import annotations

from decimal import Decimal
from xml.etree import ElementTree as ET

from sqpack.render.color import AngleHueRegistry, assign_square_colors
from sqpack.render.model import (
    PackingFrame,
    Point2,
    RenderSpec,
    RigidPose,
    SquareGeometry,
    ViewLevel,
)
from sqpack.render.numbers import scalar_from_decimal
from sqpack.render.packing import render_packing_svg


def _point(x: Decimal | int | str, y: Decimal | int | str) -> Point2:
    return Point2(scalar_from_decimal(x), scalar_from_decimal(y))


def _square(square_id: str, x: int, angle: str) -> SquareGeometry:
    return SquareGeometry(
        square_id,
        (
            _point(x, 1),
            _point(x + 1, 1),
            _point(x + 1, 2),
            _point(x, 2),
        ),
        RigidPose(
            _point(Decimal(x) + Decimal("0.5"), Decimal("1.5")), scalar_from_decimal(angle)
        ),
    )


def _frame(angles: tuple[str, ...], *, label: str, logical_time: int) -> PackingFrame:
    return PackingFrame(
        scalar_from_decimal(8),
        tuple(
            _square(f"square-{index:02d}", 2 * index - 1, angle)
            for index, angle in enumerate(angles, start=1)
        ),
        label=label,
        logical_time=Decimal(logical_time),
    )


def _panel_hues(svg: str) -> list[dict[str, int]]:
    root = ET.fromstring(svg)
    panels = [node for node in root.iter() if node.get("data-panel") is not None]
    return [
        {
            node.get("data-square", ""): int(node.get("data-hue-index", "-1"))
            for node in panel.iter()
            if node.get("data-feature") == "square-fill"
        }
        for panel in panels
    ]


def test_comparison_reuses_hues_for_shared_angles_across_different_class_orders() -> None:
    start = _frame(("0.1", "0.2", "0.3"), label="start", logical_time=0)
    final = _frame(("0.2", "0.4", "0.5"), label="final", logical_time=1)
    spec = RenderSpec(view=ViewLevel.COMPARISON, shades_per_hue=1, overlays=frozenset())

    start_hues, final_hues = _panel_hues(render_packing_svg(final, start=start, spec=spec))

    assert list(start_hues.values()) == [3, 0, 4]
    assert list(final_hues.values()) == [0, 1, 2]
    assert start_hues["square-02"] == final_hues["square-01"]

    standalone = assign_square_colors(final, RenderSpec(shades_per_hue=1))
    assert [color.hue_index for color in standalone.values()] == [0, 1, 2]


def test_registry_reserves_an_exact_match_before_a_near_match() -> None:
    registry = AngleHueRegistry(20, Decimal("1e-6"))

    assert registry.hues_for((Decimal("0.2"),)) == (0,)
    assert registry.hues_for((Decimal("0.1999995"), Decimal("0.2"))) == (1, 0)
