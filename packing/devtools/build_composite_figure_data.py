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
from collections.abc import Sequence
from decimal import ROUND_DOWN, ROUND_UP, Decimal
from functools import cache
from pathlib import Path

import sympy as sp
from strif import atomic_output_file

from devtools.build_bound_citations import corrected_lower_bounds, recent_lower_bounds
from sqpack import retained_json
from sqpack.exact_values import CATALOGUE, DERIVED_FROM_EXACT_FORM
from sqpack.known_best import (
    KNOWN_BEST_COMPOSITES,
    KNOWN_BEST_CORPUS,
    CompositeSpec,
    CorpusRange,
)
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
EVIDENCE = FRONTIER / "evidence.yaml"
RECORD = ROOT / "atlas/known-best/composite-figure.json"
GENERATOR = "python -m devtools.build_composite_figure_data"
CONTRACT = "packing.squares:CompositeFigure/v1"
SCHEMA = "composite-figure.schema.yaml"

#: The cases this record carries, one entry each. Shared with the atlas builder rather
#: than re-spelled, so the record and the drawing cover the same corpus by construction.
CORPUS = KNOWN_BEST_CORPUS
#: The composites drawn from it. Recorded here so a reader of the record knows which
#: figures state these facts and at what grid, without opening the builder.
COMPOSITES: tuple[CompositeSpec, ...] = KNOWN_BEST_COMPOSITES

TILING_EVIDENCE = "E-perfect-square-tiling-rigid"
"""The evidence id the frontier carries on a record rigid by exact tiling.

Keyed on the id rather than on `math.isqrt(n)`. A hard-coded set of `n` is what let the
two halves of `D-354`'s split merge back together here (`D-385`), and the general form of
that mistake is deciding from `n` what the record already states.
"""

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


def _packing(n: int) -> dict:
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return safe_load(text.split("---", 2)[1])["packing"]


@cache
def _first_party_lower_bounds() -> frozenset[str]:
    """Evidence ids for a lower bound this project proved and believes to be new.

    The star is a claim about provenance, so it is read from the evidence register's
    own typed fields rather than inferred from the numbers: a first-party lower bound
    whose novelty the register scores as new. Deciding it by comparing our value with
    someone else's would be D-385's mistake again, reading from arithmetic what the
    record already states.
    """
    register = safe_load(EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    return frozenset(
        str(entry["id"])
        for entry in register
        if entry.get("claim") == "lower-bound"
        and entry.get("performed_by") == "repository"
        and entry.get("novelty") in {"apparently-novel", "confirmed-novel"}
    )


@cache
def _recent_lower_bounds() -> frozenset[int]:
    """The cases whose lower bound is a recent result, which the figure stars.

    The star used to be `first_proved_here`, and so it went out at n = 11 when Kleddamag's
    3.875, developed from T-026, became the verified bound. The owner (2026-09-27) wants the
    figures to show the current state of understanding, with recent changes marked as new
    and credit given case by case on each line. `devtools.build_bound_citations` decides it
    from each source's date, and both records read that one decision.
    """
    return recent_lower_bounds()


@cache
def _corrected_lower_bounds() -> frozenset[int]:
    """The cases whose lower bound corrects a published result (the owner, 2026-10-02).

    Each is still a recent result and starred; this is the separate fact that it stands in
    for a published bound found unsound, which the citation record names on its line.
    Counted, not drawn: the figure marks a correcting bound with the same star as any
    other recent result.
    """
    return frozenset(corrected_lower_bounds())


def _six(text: str) -> str:
    """Six decimals as written, unless the value is whole.

    Stripping trailing zeros made the figure's own numbers disagree about their
    precision: on 2026-09-22 the 324 displays carried 137 bounds at six decimals, 8 at
    five and 2 at four, so `s(17) <= 4.675531` and `s(23) <= 5.43689` stood next to each
    other with no reason a reader could see. Six is what the figure prints (`think-4nxe`),
    and the record behind it keeps its full precision either way.

    A whole number has nothing to say after the point, so the grid packings stay as the
    integers they are: `s(100) = 10`, never `10.000000`.
    """
    whole, _, fraction = text.partition(".")
    return whole if set(fraction) <= {"0"} else text


def _side_text(value: str) -> str:
    """The nearest six decimals of an exactly known side."""
    number = sp.Float(value, 20)
    return _six(f"{float(number):.6f}") or "0"


def _upper_text(value: str) -> str:
    """Six decimals of an upper bound, rounded away from zero rather than to nearest.

    A displayed upper bound must stay true as written, and rounded to nearest it can print
    BELOW the bound it stands for, which claims what the record does not prove: the
    certified 5.93383346... at n = 29 printed as 5.933833, a stronger bound than anything
    on record, and 51 of the 265 open cases did the same (think-1z70, 2026-09-22).
    Rounding away from zero cannot. This is `_lower_text`'s rule in the other direction; an
    equality is neither, and keeps the nearest six decimals.
    """
    exact = Decimal(str(sp.Float(value, 30)))
    number = exact.quantize(Decimal("1.000000"), rounding=ROUND_UP)
    return _six(format(number, "f")) or "0"


def _lower_text(value: str) -> str:
    """Six decimals of a lower bound, cut off rather than rounded.

    A displayed lower bound must stay true as written, and the stored value is a
    12-digit display literal rounded to nearest, so it sits above the bound it
    stands for about half the time. Rounding again would print a number the record
    does not support: `1 + sqrt(17)` is stored as 5.12310562562 and rounds to
    5.123106, which is larger than the bound. Truncating toward zero cannot.
    """
    exact = Decimal(str(sp.Float(value, 30)))
    number = exact.quantize(Decimal("1.000000"), rounding=ROUND_DOWN)
    return _six(format(number, "f")) or "0"


def _rigidity(n: int, packing: dict) -> dict:
    """What the figure may say about rigidity here, and on whose authority.

    Read from the record. The previous version decided this from `n` alone -- a
    module-level set of the four packings the catalogue annotates "Rigid." -- and never
    opened the `rigidity` block at all, so one solid glyph covered ten packings derived
    from an exact tiling and four taken from a source's word. That is `D-385`, and it is
    `D-354`'s split failing to reach the figure lane: the whole point of separating
    `reported_upper_bound.catalogue_rigid` from the first-party `rigidity` block is that
    the two must never merge again, and in the most widely seen artifact here they had.

    So `established` now means the record's own finding is `locally-rigid` and nothing
    else does. That moves the count from 14 to 11 and, in the other direction, stops
    crediting the catalogue for `n = 11`, whose rigidity is this repository's own
    `verified` argument.

    A catalogue annotation without that finding is still shown, because the corpus holds
    the fact and dropping it would lose it -- but as an annotation, muted, and not
    counted. `n = 5` is the case that makes the distinction earn its keep: `X-007`
    establishes more about it than the catalogue ever said, and still not local rigidity.
    """
    block = packing.get("rigidity") or {}
    reported = packing.get("reported_upper_bound") or {}
    if block.get("property") == "locally-rigid":
        if TILING_EVIDENCE in (block.get("evidence") or []):
            root = math.isqrt(n)
            return {
                "state": "established",
                "basis": "perfect-square-tiling",
                "evidence": (
                    f"{n} unit squares exactly tile a {root} by {root} container, "
                    "leaving no slack, so no square can move."
                ),
                "provenance": "derived",
            }
        return {
            "state": "established",
            "basis": "first-party-argument",
            "evidence": str(block.get("scope") or "").strip() or None,
            "provenance": "frontier",
        }
    if reported.get("catalogue_rigid") == "rigid":
        return {
            "state": "not-established",
            "basis": "catalogue-annotation",
            "evidence": (
                'Kingbird annotates this packing "Rigid." This repository has not '
                "established it; see the record's own rigidity block for what it has."
            ),
            "provenance": "catalogue",
        }
    # The stored rigid flag is deliberately not consulted: it is non-null only where
    # catalogue_pictured is true, so false there means "the catalogue did not say" and
    # reads as "not rigid".
    return {
        "state": "not-established",
        "basis": "none",
        "evidence": None,
        "provenance": "absent",
    }


def _entry(n: int) -> dict:
    packing = _packing(n)
    reported = packing.get("reported_upper_bound") or {}
    status = str(packing["status"])
    value = str(reported["value"])

    exact_form = reported.get("exact_form")
    minimal_polynomial = reported.get("minimal_polynomial")
    recorded_degree = reported.get("algebraic_degree")
    source = reported.get("algebraic_source")

    # The record holds every degree and polynomial it can, and says where each came
    # from (`algebraic_source`, think-kj6n). The figure reads them rather than
    # computing its own, so it cannot know more than the record (think-26at); that the
    # derived ones still follow from the closed form is `build_exact_values`'s check.
    degree = int(recorded_degree) if recorded_degree else None
    degree_provenance = (
        "absent"
        if degree is None
        else "derived"
        if source == DERIVED_FROM_EXACT_FORM
        else "frontier"
    )
    if exact_form:
        state = "closed-form"
    elif recorded_degree or minimal_polynomial:
        state = "minimal-polynomial"
    else:
        state = "numeric-only"

    rigidity = _rigidity(n, packing)

    badges: list[dict] = []
    if status == "proved":
        badges.append({"glyph": "O", "meaning": "proved optimal", "style": "solid"})
    if state == "numeric-only":
        badges.append({"glyph": "≈", "meaning": "only known numerically", "style": "muted"})
    else:
        badges.append({"glyph": "=", "meaning": "exact value known", "style": "solid"})
    if rigidity["state"] == "established":
        badges.append({"glyph": "R", "meaning": "rigid (established here)", "style": "solid"})
    elif rigidity["basis"] == "catalogue-annotation":
        # Shown, because the corpus holds the fact and dropping it would lose it -- but
        # muted, and not counted, because a source's word is not our finding.
        badges.append(
            {"glyph": "R", "meaning": "annotated rigid by the catalogue", "style": "muted"}
        )

    relation = "equality" if status == "proved" else "upper-bound"
    verified = packing["verified_lower_bound"]
    lower_value = str(verified["value"])
    return {
        "n": n,
        "lower": {
            "value": lower_value,
            # A proved case already reads `s(n) = ...`, so a second line would say the
            # same thing twice. `status` decides it, never a comparison of the two
            # stored numbers: at n = 5 and n = 10 the lower bound is stored to more
            # digits than the upper and compares larger.
            "shown": status != "proved",
            "display": f"s({n}) \u2265 {_lower_text(lower_value)}",
            "first_proved_here": bool(set(verified["evidence"]) & _first_party_lower_bounds()),
            # The star: a recent result, whoever proved it. Read from the citation record's
            # own test, so the stage's line and the figure's star cannot disagree.
            "recent_result": n in _recent_lower_bounds(),
            # Whether it corrects a published result, read from the citation record's
            # `corrects`, which also names the work.
            "correction": n in _corrected_lower_bounds(),
            "evidence": sorted(str(item) for item in verified["evidence"]),
            "provenance": "frontier",
        },
        "side": {
            "value": value,
            "relation": relation,
            "display": (
                f"s({n}) = {_side_text(value)}"
                if relation == "equality"
                else f"s({n}) ≤ {_upper_text(value)}"
            ),
            "provenance": "frontier",
        },
        "optimality": {"status": status, "provenance": "frontier"},
        "exactness": {
            "state": state,
            "exact_form": str(exact_form) if exact_form else None,
            "minimal_polynomial": (str(minimal_polynomial) if minimal_polynomial else None),
            "degree": degree,
            "degree_provenance": degree_provenance,
            "degree_recorded_upstream": source == CATALOGUE,
        },
        "rigidity": rigidity,
        "badges": badges,
    }


def _composite_record(composite: CompositeSpec, entries: list[dict]) -> dict:
    """One composite's shape and its own legend totals, as the record states them.

    Which cases a figure draws and at what grid, and nothing about pixels: the canvas
    is the builder's, and `atlas/known-best/manifest.json` records it there. The totals
    are counted over the cases this composite draws, not over the corpus, so the
    1-100 figure's legend does not change when the register grows past it.
    """
    drawn = [e for e in entries if composite.first_n <= e["n"] <= composite.last_n]
    return {
        "stem": composite.stem,
        "range": _range_record(composite.cases),
        "columns": composite.columns,
        "rows": composite.rows,
        "layout": composite.layout,
        "square_count": composite.square_count,
        "totals": _totals(drawn),
    }


def _range_record(cases: CorpusRange) -> dict:
    return {"first_n": cases.first_n, "last_n": cases.last_n, "count": cases.count}


def _totals(entries: list[dict]) -> dict:
    """The legend counts over one set of entries."""
    return {
        "proved_optimal": sum(1 for e in entries if e["optimality"]["status"] == "proved"),
        "exact_value_known": sum(
            1 for e in entries if e["exactness"]["state"] != "numeric-only"
        ),
        "only_known_numerically": sum(
            1 for e in entries if e["exactness"]["state"] == "numeric-only"
        ),
        "rigidity_established": sum(
            1 for e in entries if e["rigidity"]["state"] == "established"
        ),
        "lower_bound_first_proved_here": sum(
            1 for e in entries if e["lower"]["first_proved_here"]
        ),
        "lower_bound_recent_result": sum(1 for e in entries if e["lower"]["recent_result"]),
        # Of those, the ones that correct a published result: a second fact about a
        # recent bound, not a second star.
        "lower_bound_correction": sum(1 for e in entries if e["lower"]["correction"]),
        # Counted separately rather than folded in, which is the whole of D-385:
        # a source's word and our own argument are two facts, not one.
        "rigidity_catalogue_annotated": sum(
            1 for e in entries if e["rigidity"]["basis"] == "catalogue-annotation"
        ),
        "degree_known": sum(1 for e in entries if e["exactness"]["degree"] is not None),
        "degree_recorded_upstream": sum(
            1 for e in entries if e["exactness"]["degree_recorded_upstream"]
        ),
        "degree_derived_here": sum(
            1 for e in entries if e["exactness"]["degree_provenance"] == "derived"
        ),
    }


def build_record() -> dict:
    entries = [_entry(n) for n in CORPUS.numbers]
    return {
        "softschema": {
            "contract": CONTRACT,
            "schema": SCHEMA,
            "envelope": "figure",
            "status": "enforced",
        },
        "figure": {
            "range": _range_record(CORPUS),
            # A list rather than a single record: a second composite over the same
            # cases is a second entry, and nothing about this shape moves when one
            # is added.
            "composites": [_composite_record(spec, entries) for spec in COMPOSITES],
            "generated_by": GENERATOR,
            "provenance_vocabulary": PROVENANCE_VOCABULARY,
            "totals": _totals(entries),
            "entries": entries,
        },
    }


def load_record() -> dict:
    """The figure's data, as committed."""
    return json.loads(RECORD.read_text(encoding="utf-8"))["figure"]


def _text(record: dict) -> str:
    return retained_json.dumps(record, sort_keys=True, ensure_ascii=False)


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
    # The figure reads every degree from the record, so a derived degree is one the
    # record stores as `derived-from-exact-form`, never one only the figure knows.
    print(f"  degree derived from a closed form, stored in the record: {len(derived)}")
    print(f"  no exact value on record: {len(unknown)}")
    print(f"    n = {unknown}")
    print(f"  rigidity from catalogue annotation: n = {catalogue_only}")
    print(f"  rigidity from perfect-square tiling: n = {tiling}")


def main(argv: Sequence[str] | None = None) -> int:
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
