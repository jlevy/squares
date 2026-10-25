"""Tests for devtools.check_exact_side_packing on a two-square system with an exact side.

Square 0 is axis-aligned in the lower-left corner; square 1 is tilted by 2 atan(1/2) (cosine
3/5, sine 4/5, half-width h(t) = (1 - t^2 + 2t) / (2 (1 + t^2)) = 7/10 at t = 1/2), resting on
the floor and the right wall with a corner on square 0's right edge.  The consistency
polynomial is 2 t1 - 1.  The first row, y1 = 7/10, holds only at t* = 1/2: it takes the
basis place of y1 = h(t), so the floor contact of square 1 is exact only through the
elimination, which must find its residual divisible by F_1.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools.check_exact_side_packing import SystemFormatError, decide, parse_system

HALF_WIDTH = "(t1^2 - 2*t1 - 1, 2*t1^2 + 2)"


def write_system(directory: Path, overlap: str = "0") -> tuple[Path, Path]:
    contact = f"(-t1 - 1 + ({overlap})*t1^2 + ({overlap}), t1^2 + 1)"
    rows = [
        '(Dict{String,Any}("y1" => (1, 1)), (-(big(7)//10), 1)),',
        '(Dict{String,Any}("x0" => (1, 1)), (-(big(1)//2), 1)),',
        '(Dict{String,Any}("y0" => (1, 1)), (-(big(1)//2), 1)),',
        f'(Dict{{String,Any}}("y1" => (1, 1)), {HALF_WIDTH}),',
        f'(Dict{{String,Any}}("x1" => (1, 1), "x0" => (-1, 1)), {contact}),',
        f'(Dict{{String,Any}}("S" => (1, 1), "x1" => (-1, 1)), {HALF_WIDTH}),',
    ]
    text = "\n".join(
        [
            "# synthetic",
            "@var t1",
            "tvars = [t1]",
            "F = [",
            "2*t1 - 1",
            "]",
            'tstar = [big"0.5"]',
            "Sn = 2*t1 + 2",
            "Sd = t1^2 + 1",
            'zvars = ["S", "x0", "x1", "y0", "y1"]',
            "rows = [",
            *("  " + row for row in rows),
            "]",
        ]
    )
    system = directory / "system.jl"
    system.write_text(text + "\n")
    box = directory / "box.json"
    box.write_text(json.dumps({"certified": True, "radius": "1e-50", "tstar": ["0.5"]}))
    return system, box


def reference(x1: Fraction) -> list[tuple[int, Fraction, Fraction, Fraction, Fraction]]:
    return [
        (1, Fraction(1, 2), Fraction(1, 2), Fraction(1), Fraction(0)),
        (2, x1, Fraction(7, 10), Fraction(3, 5), Fraction(4, 5)),
    ]


def test_decides_the_two_square_packing_exactly(tmp_path: Path) -> None:
    system, box = write_system(tmp_path)
    receipt = decide(system, box, reference(Fraction(17, 10)), digits=60)
    assert receipt["decided"], receipt["failures"]
    assert receipt["box"]["independent_krawczyk"]["unique"]
    assert receipt["touching"]["by_exactness"] == {
        "basis": 4,
        "proportional-to-basis": 0,
        "consistency": 1,
    }
    assert receipt["touching"]["consistency"]["rows"] == {"3": "numerator divisible by F_1"}
    assert receipt["contacts_exact_without_monte_carlo"]
    low, high = (Fraction(v) for v in receipt["side_enclosure"]["from_rows"])
    assert low <= Fraction(12, 5) <= high


def test_refuses_an_overlapping_configuration(tmp_path: Path) -> None:
    system, box = write_system(tmp_path, overlap="big(1)//100")
    receipt = decide(system, box, reference(Fraction(169, 100)), digits=60)
    assert not receipt["decided"]
    assert any(failure.startswith("pair 0-1") for failure in receipt["failures"])


def test_parser_refuses_text_outside_the_grammar(tmp_path: Path) -> None:
    system, _ = write_system(tmp_path)
    system.write_text(system.read_text().replace("2*t1 - 1", "exp(t1) - 1"))
    with pytest.raises(SystemFormatError):
        parse_system(system)
