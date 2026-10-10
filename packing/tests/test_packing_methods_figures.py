"""Packing-method illustrations preserve their retained source identities."""

from __future__ import annotations

import gzip
import json
import math
from fractions import Fraction
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from devtools import packing_methods_figures as figures
from sqpack.render.svg import svg_tag, validate_safe_tree


def _points(node: ET.Element) -> list[tuple[float, float]]:
    return [
        (float(x), float(y))
        for x, y in (pair.split(",") for pair in node.attrib["points"].split())
    ]


def test_examples_are_passive_accessible_phone_width_drawings() -> None:
    rendered = figures.render_figures()
    expected_counts = {
        "HAND_CONSTRUCTION_SVG": 11,
        "ANNEALING_SVG": 29,
        "ANNEALING_SLP_SVG": 106,
        "SURGERY_SVG": 108,
        "ALGEBRAIC_WITNESS_SVG": 51,
    }
    assert set(rendered) == set(expected_counts)
    identifiers: list[str] = []
    for key, count in expected_counts.items():
        root = ET.fromstring(rendered[key])
        validate_safe_tree(root)
        assert root.attrib["role"] == "img"
        assert float(root.attrib["width"]) <= 390
        ground = root.find(svg_tag("rect"))
        assert ground is not None
        assert ground.attrib["fill"] == "#ffffff"
        local_ids = {node.attrib["id"] for node in root.iter() if "id" in node.attrib}
        identifiers.extend(local_ids)
        assert set(root.attrib["aria-labelledby"].split()) <= local_ids
        title, description = root.find(svg_tag("title")), root.find(svg_tag("desc"))
        assert title is not None
        assert title.text
        assert description is not None
        assert description.text
        assert "illustration" in description.text.lower()
        squares = root.findall(f'.//{svg_tag("polygon")}[@data-feature="square-fill"]')
        assert len(squares) == count
        assert all(len(_points(square)) == 4 for square in squares)
        assert len({square.attrib["data-square"] for square in squares}) == count
        assert not any(
            node.tag
            in {svg_tag(tag) for tag in ("script", "image", "foreignObject", "style", "use")}
            for node in root.iter()
        )
        assert all(
            math.isfinite(value) and 11.99 <= value <= 378.01
            for square in squares
            for point in _points(square)
            for value in point
        )
    assert len(identifiers) == len(set(identifiers))
    assert figures.render_figures() == rendered


def test_attribution_retains_historical_source_identity() -> None:
    rendered = figures.render_figures()
    assert "Walter Trump" in rendered["HAND_CONSTRUCTION_SVG"]
    assert "trump11-exact-q-u" in rendered["HAND_CONSTRUCTION_SVG"]
    assert "Thomas Schadt" in rendered["ANNEALING_SVG"]
    assert "David Ellsworth" in rendered["ANNEALING_SVG"]
    assert "Griffin Casson" in rendered["ANNEALING_SLP_SVG"]
    assert "CC BY 4.0" in rendered["ANNEALING_SLP_SVG"]
    assert "2026-09-23" in rendered["ANNEALING_SLP_SVG"]
    assert "Chaoweeraprasit" in rendered["SURGERY_SVG"]
    assert "e63e4e52b1728b6671b2f263c5e02a4aa79a39d3" in rendered["SURGERY_SVG"]
    assert "ry-xu" not in rendered["SURGERY_SVG"]
    assert "110" in rendered["SURGERY_SVG"]
    assert "ry-xu" in rendered["ALGEBRAIC_WITNESS_SVG"]


def test_dated_pose_centres_survive_projection() -> None:
    rendered = figures.render_figures()
    casson = ET.fromstring(rendered["ANNEALING_SLP_SVG"])
    square = casson.find(f'.//{svg_tag("polygon")}[@data-square="square-001"]')
    assert square is not None
    points = _points(square)
    source_lines = figures.CASSON_POSE.read_text(encoding="utf-8").splitlines()
    side = float(source_lines[0].removeprefix("s: "))
    first = source_lines[1].split(": ", 1)[1].split(", ")
    cx, cy = (float(entry.split("=", 1)[1]) for entry in first[:2])
    assert math.isclose(
        sum(x for x, _ in points) / 4, 12 + 366 * (cx / side + 0.5), abs_tol=0.001
    )
    assert math.isclose(
        sum(y for _, y in points) / 4, 12 + 366 * (0.5 - cy / side), abs_tol=0.001
    )

    surgery = ET.fromstring(rendered["SURGERY_SVG"])
    square = surgery.find(f'.//{svg_tag("polygon")}[@data-square="square-001"]')
    assert square is not None
    points = _points(square)
    record = json.loads(gzip.decompress(figures.SURGERY_FACTS.read_bytes()))
    side = float(Fraction(record["side"]))
    cx, cy = (float(Fraction(record["squares"][0][axis])) for axis in ("x", "y"))
    assert math.isclose(sum(x for x, _ in points) / 4, 12 + 366 * cx / side, abs_tol=0.001)
    assert math.isclose(
        sum(y for _, y in points) / 4, 12 + 366 * (1 - cy / side), abs_tol=0.001
    )


def test_every_read_is_in_declared_publication_inputs(monkeypatch: pytest.MonkeyPatch) -> None:
    actual: set[Path] = set()
    read_text, read_bytes = Path.read_text, Path.read_bytes

    def tracked_text(
        path: Path,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> str:
        actual.add(path.resolve())
        return read_text(path, encoding=encoding, errors=errors, newline=newline)

    def tracked_bytes(path: Path) -> bytes:
        actual.add(path.resolve())
        return read_bytes(path)

    monkeypatch.setattr(Path, "read_text", tracked_text)
    monkeypatch.setattr(Path, "read_bytes", tracked_bytes)
    figures.render_figures()
    declared = set(figures.FIGURE_INPUTS)
    assert actual <= declared
    assert {figures.CASSON_POSE, figures.SURGERY_FACTS, figures.SURGERY_SOURCES} <= actual
    assert all(path.is_absolute() and path.is_file() for path in declared)
    assert all(path.is_relative_to(figures.REPO) for path in declared)
    assert not any("known-best" in str(path) and "108" in path.name for path in declared)


def test_incomplete_rosters_and_mixed_historical_identity_are_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    text = figures.CASSON_POSE.read_text(encoding="utf-8")
    facts = json.loads(gzip.decompress(figures.SURGERY_FACTS.read_bytes()))
    read_text, read_bytes = Path.read_text, Path.read_bytes

    def incomplete_casson(
        path: Path,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> str:
        if path == figures.CASSON_POSE:
            return "\n".join(text.splitlines()[:-1])
        return read_text(path, encoding=encoding, errors=errors, newline=newline)

    with monkeypatch.context() as patches:
        patches.setattr(Path, "read_text", incomplete_casson)
        with pytest.raises(ValueError, match="expected 106 retained squares"):
            figures.render_figures()

    facts["side"] = "11"

    def mixed_squish(path: Path) -> bytes:
        if path == figures.SURGERY_FACTS:
            return gzip.compress(json.dumps(facts).encode())
        return read_bytes(path)

    with monkeypatch.context() as patches:
        patches.setattr(Path, "read_bytes", mixed_squish)
        with pytest.raises(ValueError, match="historical SQUISH facts differ"):
            figures.render_figures()


@pytest.mark.parametrize(
    "fill",
    [
        pytest.param(
            r"u\72l(https://example.invalid/security-fill.svg#paint)", id="escaped-url"
        ),
        pytest.param(
            r"\75\72\6c(https://example.invalid/security-fill.svg#paint)",
            id="fully-escaped-url",
        ),
        pytest.param("var(--figure-fill)", id="css-variable"),
        pytest.param("red", id="named-colour"),
        pytest.param("#abc", id="short-hex"),
        pytest.param("#4b9582\n", id="trailing-newline"),
    ],
)
def test_retained_square_fills_require_six_digit_hex_colours(
    monkeypatch: pytest.MonkeyPatch, fill: str
) -> None:
    source = ET.fromstring(figures.TRUMP_DRAWING.read_text(encoding="utf-8"))
    square = source.find(f'.//{svg_tag("polygon")}[@data-feature="square-fill"]')
    assert square is not None
    square.set("fill", fill)
    modified = ET.tostring(source, encoding="unicode")
    read_text = Path.read_text

    def untrusted_fill(
        path: Path,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> str:
        if path == figures.TRUMP_DRAWING:
            return modified
        return read_text(path, encoding=encoding, errors=errors, newline=newline)

    monkeypatch.setattr(Path, "read_text", untrusted_fill)
    with pytest.raises(ValueError, match="fill must be a six-digit hexadecimal colour"):
        figures.render_figures()


def test_retained_square_colours_are_preserved() -> None:
    rendered = figures.render_figures()
    sources = {
        "HAND_CONSTRUCTION_SVG": figures.TRUMP_DRAWING,
        "ANNEALING_SVG": figures.ANNEALING_DRAWING,
        "ALGEBRAIC_WITNESS_SVG": figures.ALGEBRAIC_DRAWING,
    }
    for key, path in sources.items():
        source = ET.fromstring(path.read_text(encoding="utf-8"))
        drawing = ET.fromstring(rendered[key])
        selector = f'.//{svg_tag("polygon")}[@data-feature="square-fill"]'
        assert [square.attrib["fill"] for square in drawing.findall(selector)] == [
            square.attrib["fill"] for square in source.findall(selector)
        ]
