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

from devtools.build_known_best_atlas import frame_from_witness
from sqpack.field import NumberField
from sqpack.render import RenderSpec, render_packing_svg
from sqpack.render.numbers import SVG_EMISSION_PRECISION
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
