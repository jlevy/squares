#!/usr/bin/env python3
"""Derive the composite figure's data record from the frontier and the catalogue.

The figure renders from this record and from nothing else. Every fact it states
lands here first, with the provenance of that fact, so the drawing and the data
cannot drift apart and the corpus can be reviewed without reading the renderer.

The provenance is the point. A bare null cannot separate "transcribed from a
source", "missed in transcription", "the source is silent" and "nobody knows",
and conflating those is what put a wrong badge on n=54. Here every fact says
where it came from, so a review can ask a precise question: which facts are
derived here, or absent, while a source could supply them?
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import sympy as sp
from strif import atomic_output_file
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
RECORD = ROOT / "atlas/known-best/composite-figure.json"
GENERATOR = "python -m devtools.build_composite_figure_data"
CONTRACT = "packing.squares:CompositeFigure/v1"
SCHEMA = "composite-figure.schema.yaml"

# Kingbird annotates exactly these four packings "Rigid.", at lines 44, 80, 163
# and 224 of resources/web/kingbird-squares-in-squares.md, each identified by the
# side value printed above it.
CATALOGUE_RIGID = {5, 11, 28, 40}

PROVENANCE_VOCABULARY = {
    "frontier": ("Read from the case's frontier record, which transcribes a retained source."),
    "catalogue": (
        "Transcribed here from the retained catalogue, not carried by the frontier record."
    ),
    "derived": "Computed by this repository from a fact it already holds.",
    "absent": (
        "No source on hand supplies it. Not a claim that the fact is unknown to mathematics."
    ),
}

_TRANSFORMS = (*standard_transformations, implicit_multiplication_application)
_SIDE = sp.Symbol("s")


def _packing(n: int) -> dict:
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return safe_load(text.split("---", 2)[1])["packing"]


def _degree_from_form(exact_form: str) -> tuple[int, str]:
    """Degree of the algebraic number this radical denotes, and its polynomial."""
    value = parse_expr(exact_form, transformations=_TRANSFORMS)
    polynomial = sp.minimal_polynomial(value, _SIDE)
    return int(sp.degree(polynomial)), str(sp.expand(polynomial)) + " = 0"


def _side_text(value: str) -> str:
    """Six significant decimals, trailing zeros and point removed."""
    number = sp.Float(value, 20)
    text = f"{float(number):.6f}".rstrip("0").rstrip(".")
    return text or "0"


def _entry(n: int) -> dict:
    packing = _packing(n)
    reported = packing.get("reported_upper_bound") or {}
    status = str(packing["status"])
    value = str(reported["value"])

    exact_form = reported.get("exact_form")
    minimal_polynomial = reported.get("minimal_polynomial")
    recorded_degree = reported.get("algebraic_degree")

    if recorded_degree:
        state = "minimal-polynomial"
        degree, degree_provenance = int(recorded_degree), "frontier"
    elif exact_form:
        # The catalogue prints either a radical or a degree, never both, so a
        # radical case carries no degree upstream even though the radical fixes
        # it completely. Computing it is the whole point of recording it here.
        degree, derived_polynomial = _degree_from_form(str(exact_form))
        minimal_polynomial = minimal_polynomial or derived_polynomial
        state, degree_provenance = "closed-form", "derived"
    elif minimal_polynomial:
        state, degree, degree_provenance = "minimal-polynomial", None, "absent"
    else:
        state, degree, degree_provenance = "numeric-only", None, "absent"

    root = math.isqrt(n)
    if root * root == n:
        rigidity = {
            "state": "established",
            "basis": "perfect-square-tiling",
            "evidence": (
                f"{n} unit squares exactly tile a {root} by {root} container, "
                "leaving no slack, so no square can move."
            ),
            "provenance": "derived",
        }
    elif n in CATALOGUE_RIGID:
        rigidity = {
            "state": "established",
            "basis": "catalogue-annotation",
            "evidence": 'Kingbird annotates this packing "Rigid."',
            "provenance": "catalogue",
        }
    else:
        # The stored rigid flag is deliberately not consulted: it is non-null
        # only where catalogue_pictured is true, so false there means "the
        # catalogue did not say" and reads as "not rigid".
        rigidity = {
            "state": "not-established",
            "basis": "none",
            "evidence": None,
            "provenance": "absent",
        }

    badges: list[dict] = []
    if status == "proved":
        badges.append({"glyph": "O", "meaning": "proved optimal", "style": "solid"})
    if state == "numeric-only":
        badges.append({"glyph": "≈", "meaning": "only known numerically", "style": "muted"})
    else:
        badges.append({"glyph": "=", "meaning": "exact value known", "style": "solid"})
    if rigidity["state"] == "established":
        badges.append({"glyph": "R", "meaning": "rigid (established)", "style": "solid"})

    relation = "equality" if status == "proved" else "upper-bound"
    return {
        "n": n,
        "side": {
            "value": value,
            "relation": relation,
            "display": (f"s({n}) {'=' if relation == 'equality' else '≤'} {_side_text(value)}"),
            "provenance": "frontier",
        },
        "optimality": {"status": status, "provenance": "frontier"},
        "exactness": {
            "state": state,
            "exact_form": str(exact_form) if exact_form else None,
            "minimal_polynomial": (str(minimal_polynomial) if minimal_polynomial else None),
            "degree": degree,
            "degree_provenance": degree_provenance,
            "degree_recorded_upstream": bool(recorded_degree),
        },
        "rigidity": rigidity,
        "badges": badges,
    }


def build_record() -> dict:
    entries = [_entry(n) for n in range(1, 101)]
    return {
        "softschema": {
            "contract": CONTRACT,
            "schema": SCHEMA,
            "envelope": "figure",
            "status": "enforced",
        },
        "figure": {
            "range": {"first_n": 1, "last_n": 100, "count": 100},
            "generated_by": GENERATOR,
            "provenance_vocabulary": PROVENANCE_VOCABULARY,
            "totals": {
                "proved_optimal": sum(
                    1 for e in entries if e["optimality"]["status"] == "proved"
                ),
                "exact_value_known": sum(
                    1 for e in entries if e["exactness"]["state"] != "numeric-only"
                ),
                "only_known_numerically": sum(
                    1 for e in entries if e["exactness"]["state"] == "numeric-only"
                ),
                "rigidity_established": sum(
                    1 for e in entries if e["rigidity"]["state"] == "established"
                ),
                "degree_known": sum(1 for e in entries if e["exactness"]["degree"] is not None),
                "degree_recorded_upstream": sum(
                    1 for e in entries if e["exactness"]["degree_recorded_upstream"]
                ),
                "degree_derived_here": sum(
                    1 for e in entries if e["exactness"]["degree_provenance"] == "derived"
                ),
            },
            "entries": entries,
        },
    }


def load_record() -> dict:
    """The figure's data, as committed."""
    return json.loads(RECORD.read_text(encoding="utf-8"))["figure"]


def _text(record: dict) -> str:
    return json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def update() -> None:
    content = _text(build_record())
    if RECORD.is_file() and RECORD.read_text(encoding="utf-8") == content:
        print(f"composite figure record already current: {RECORD.name}")
        return
    with atomic_output_file(RECORD, make_parents=True) as temporary:
        temporary.write_text(content, encoding="utf-8")
    print(f"composite figure record updated: {RECORD.name}")


def check() -> None:
    if not RECORD.is_file():
        raise ValueError(f"missing {RECORD.relative_to(ROOT)}; run with --update")
    if RECORD.read_text(encoding="utf-8") != _text(build_record()):
        raise ValueError(f"stale {RECORD.relative_to(ROOT)}; re-run with --update")
    print("composite figure record check passed: matches the frontier and catalogue")


def review() -> None:
    """Report where the figure knows more than the records do."""
    figure = build_record()["figure"]
    entries = figure["entries"]
    derived = [e["n"] for e in entries if e["exactness"]["degree_provenance"] == "derived"]
    unknown = [e["n"] for e in entries if e["exactness"]["state"] == "numeric-only"]
    catalogue_only = [
        e["n"] for e in entries if e["rigidity"]["basis"] == "catalogue-annotation"
    ]
    tiling = [e["n"] for e in entries if e["rigidity"]["basis"] == "perfect-square-tiling"]
    for label, value in figure["totals"].items():
        print(f"  {label:26s} {value:3d}")
    print()
    print(f"  degree derived here but NOT stored upstream: {len(derived)}")
    print(f"    n = {derived}")
    print(f"  no exact value on record: {len(unknown)}")
    print(f"    n = {unknown}")
    print(f"  rigidity from catalogue annotation: n = {catalogue_only}")
    print(f"  rigidity from perfect-square tiling: n = {tiling}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action="store_true", help="write the record")
    group.add_argument("--check", action="store_true", help="fail if the record is stale")
    group.add_argument("--review", action="store_true", help="report gaps against the sources")
    arguments = parser.parse_args(argv)
    try:
        if arguments.update:
            update()
        elif arguments.check:
            check()
        else:
            review()
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
