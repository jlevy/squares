#!/usr/bin/env python3
"""A rendered figure is a function of its inputs, not of the ambient decimal context.

`decimal` keeps working precision in a thread-global context, so any module that sets it
and does not put it back moves the arithmetic of every unrelated Decimal in the process.
That happened: `NumberField.decimal` widened the context permanently, the atlas renderer
computed its coordinates at whatever precision it was handed, and the composite atlas's
stored PNG receipt then matched the freshly rendered SVG only when no test had refined a
number field first (D-359).

Both halves are checked here, because either one alone restores the drift.
"""

from __future__ import annotations

import decimal
import subprocess
import sys
from pathlib import Path
from textwrap import dedent
from xml.etree import ElementTree as ET

import pytest

from devtools import atlas_print_font
from devtools.build_known_best_atlas import frame_from_witness
from sqpack.field import NumberField
from sqpack.render import RenderSpec, render_packing_svg
from sqpack.render.numbers import SVG_EMISSION_PRECISION
from sqpack.render.svg import (
    PRINT_FONT_MARKER,
    XML_DECLARATION,
    append_exact_comment,
    append_metadata,
    element,
    serialize_svg,
    sqpack_tag,
    sub,
    svg_tag,
)
from sqpack.witness import load_witness

ROOT = Path(__file__).resolve().parents[1]
# The retained n=5 packing, whose coordinates are irrational: its emitted digits move
# when the working precision does. A grid case would prove nothing here, since every
# coordinate is a small rational that prints the same string at any precision.
WITNESS = ROOT / "witnesses/known-best/n-005.yaml"
# The precision the leak actually left behind, rather than an invented one:
# `NumberField.decimal(x, 30)` set `digits + 20`.
WIDENED_PRECISION = 50


def _rendering() -> str:
    """The n=5 house rendering, produced exactly as the atlas produces it."""
    return render_packing_svg(
        frame_from_witness(load_witness(WITNESS)), spec=RenderSpec(overlays=frozenset())
    )


def test_svg_precision_checks_do_not_load_the_native_rasterizer() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import runpy, sys; sys.modules['cairosvg'] = None; "
                "print(runpy.run_path(sys.argv[1])['_rendering']())"
            ),
            str(Path(__file__).resolve()),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "<svg" in completed.stdout


def test_number_field_decimal_leaves_the_global_precision_alone() -> None:
    """Refining a field is not licence to rewiden every other Decimal in the process."""
    before = decimal.getcontext().prec
    field = NumberField((1, 0, -2), (1, 2))
    assert field.decimal(field.alpha, 30).startswith("1.41421356")
    after = decimal.getcontext().prec
    assert after == before, (
        f"NumberField.decimal left the global decimal precision at {after}, not {before}"
    )


def test_rendering_is_byte_identical_after_a_field_refinement() -> None:
    """D-359 in its own words: refining a field must not redraw an unrelated figure.

    Weaker than the two around it on purpose. Either guard alone keeps this true, so it
    is a statement of the defect rather than a separate detector of it.
    """
    baseline = _rendering()
    field = NumberField((1, 0, -2), (1, 2))
    field.decimal(field.alpha, 30)
    assert _rendering() == baseline, "a number-field refinement changed the emitted SVG bytes"


def test_rendering_ignores_a_widened_ambient_decimal_context() -> None:
    """The pin holds even against a caller who widens the context deliberately."""
    baseline = _rendering()
    with decimal.localcontext() as context:
        context.prec = WIDENED_PRECISION
        widened = _rendering()
    assert widened == baseline, (
        f"the emitted SVG followed the ambient decimal context to {WIDENED_PRECISION} "
        f"digits instead of the renderer's pinned {SVG_EMISSION_PRECISION}"
    )


def _parse_svg(text: str) -> ET.Element:
    return ET.fromstring(text, parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))


def assert_compact_svg_roundtrip(text: str, *, embedded_print_fonts: str | None = None) -> str:
    """Replay a complete pretty artifact, also usable for an external composite receipt."""
    compact = serialize_svg(
        _parse_svg(text), compact=True, embedded_print_fonts=embedded_print_fonts
    )
    assert len(compact.encode("utf-8")) < len(text.encode("utf-8"))
    assert serialize_svg(_parse_svg(compact), embedded_print_fonts=embedded_print_fonts) == text
    return compact


def test_default_svg_serialization_keeps_its_existing_bytes() -> None:
    root = element("svg")
    label = sub(sub(root, "g"), "text")
    sub(label, "tspan").text = "A"
    sub(label, "tspan").text = "B"
    expected = XML_DECLARATION + dedent("""\
        <svg xmlns="http://www.w3.org/2000/svg">
          <g>
            <text><tspan>A</tspan><tspan>B</tspan></text>
          </g>
        </svg>
        """)
    assert serialize_svg(root) == expected
    compact = serialize_svg(root, compact=True)
    assert compact == (
        XML_DECLARATION
        + '<svg xmlns="http://www.w3.org/2000/svg"><g><text>'
        + "<tspan>A</tspan><tspan>B</tspan></text></g></svg>\n"
    )
    assert serialize_svg(_parse_svg(compact)) == expected
    assert root.text is None
    assert label.text is None


def test_compact_svg_preserves_semantic_whitespace_and_payloads() -> None:
    root = element("svg")
    root.text = "\n  "
    group = sub(root, "g")
    group.text = "\n    "
    group.tail = "\n"
    label = sub(group, "text")
    label.text = "\n  "
    first = sub(label, "tspan")
    first.text = "first"
    first.tail = " \t "
    second = sub(label, "tspan")
    second.text = "second "
    sub(second, "tspan").text = "inner"
    second.tail = "\n  "
    label.tail = "\n  "
    title = sub(root, "title")
    title.text = "  Title\n "
    desc = sub(root, "desc")
    desc.text = "before "
    sub(desc, "tspan").text = "description"
    desc[0].tail = "\n  "
    append_exact_comment(root, " exact = 1/3 ")
    append_metadata(root, {"blank": "\n  ", "credit": " A & B\n C ", "json": '{"n":5}'})
    css = atlas_print_font.embedded_css()
    sub(root, "style", {"data-sqpack-style": PRINT_FONT_MARKER}).text = css

    compact = serialize_svg(root, compact=True, embedded_print_fonts=css)
    parsed = _parse_svg(compact)
    assert parsed.text is None
    assert parsed[0].text is None
    assert parsed[0].tail is None
    for name in ("text", "title", "desc"):
        expected = next(root.iter(svg_tag(name)))
        actual = next(parsed.iter(svg_tag(name)))
        assert list(actual.itertext()) == list(expected.itertext())
    assert [node.text for node in parsed.iter(sqpack_tag("value"))] == [
        "\n  ",
        " A & B\n C ",
        '{"n":5}',
    ]
    assert next(parsed.iter(svg_tag("style"))).text == css
    assert "<!-- exact = 1/3 -->" in compact
    assert root.text == "\n  "
    assert label.tail == "\n  "


def test_compact_svg_leaves_mixed_container_content_intact() -> None:
    root = element("svg")
    group = sub(root, "g")
    group.text = "mixed "
    sub(group, "text").text = "label"
    group[0].tail = "\n  "
    parsed = _parse_svg(serialize_svg(root, compact=True))
    assert list(parsed[0].itertext()) == ["mixed ", "label", "\n  "]


def test_compact_svg_keeps_font_opt_in_and_security_validation() -> None:
    css = atlas_print_font.embedded_css()
    root = element("svg")
    style = sub(root, "style", {"data-sqpack-style": PRINT_FONT_MARKER})
    style.text = css
    with pytest.raises(ValueError, match="arbitrary CSS"):
        serialize_svg(root, compact=True)
    with pytest.raises(ValueError, match="arbitrary CSS"):
        serialize_svg(root, compact=True, embedded_print_fonts=css + "\n")
    style.text = css + '\n@import "https://example.invalid/font.css";'
    with pytest.raises(ValueError, match="retained-face grammar"):
        serialize_svg(root, compact=True, embedded_print_fonts=style.text)
    style.text = css
    sub(root, "use", {"href": "https://example.invalid/shape.svg#shape"})
    with pytest.raises(ValueError, match="external SVG reference"):
        serialize_svg(root, compact=True, embedded_print_fonts=css)


def test_a_real_packing_roundtrips_through_compact_svg() -> None:
    assert_compact_svg_roundtrip(_rendering())
