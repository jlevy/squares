#!/usr/bin/env python3
"""Build a compact evidence profile for non-grid known-best contact assemblies."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from strif import atomic_output_file

from sqpack.render.style import PAPER_THEME, color_for_square
from sqpack.render.svg import (
    append_metadata,
    append_title_desc,
    element,
    serialize_svg,
    sub,
    write_svg_atomic,
)

ROOT = Path(__file__).resolve().parent.parent
ATLAS_ROOT = ROOT / "atlas/known-best"
MANIFEST = ATLAS_ROOT / "manifest.json"
COMPONENTS = ATLAS_ROOT / "chunk-components.json"
PARTITIONS = ATLAS_ROOT / "chunk-partitions.json"
OUTPUT = ATLAS_ROOT / "chunk-evidence-profile.json"
SCHEMA = ATLAS_ROOT / "chunk-evidence-profile.schema.yaml"
EVIDENCE_ROOT = ATLAS_ROOT / "evidence"
RENDERING = EVIDENCE_ROOT / "non-grid-chunk-evidence-profile.svg"
GENERATOR = "python -m devtools.profile_known_best_chunks"
PRIMARY_SWEEP = "registered-angle-contact"
SENSITIVITY_SWEEP = "regularized-angle-contact"
PARTITION_BAND = "exact"


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _ratio(numerator: int, denominator: int) -> str:
    value = Decimal(numerator) / Decimal(denominator)
    return f"{value:.12f}".rstrip("0").rstrip(".")


def _text(
    parent: Any,
    *,
    x: int,
    y: int,
    value: str,
    size: int,
    fill: str,
    weight: str = "400",
    anchor: str = "start",
) -> None:
    sub(
        parent,
        "text",
        {
            "x": str(x),
            "y": str(y),
            "fill": fill,
            "font-size": str(size),
            "font-weight": weight,
            "text-anchor": anchor,
        },
    ).text = value


def _partition_label(partition: dict[str, Any]) -> str:
    status = partition["status"]
    if status == "established":
        return f"fit C{partition['selected_chunk_count']}"
    if status == "outside-registered-budget":
        return f">budget C{partition['selected_chunk_count']}"
    if status == "not-established-search-limit":
        return "search cap"
    return "none"


def render_profile(profile: dict[str, Any]) -> str:
    """Render the 36-case table as a house-style descriptive evidence overview."""
    root = element(
        "svg",
        {
            "viewBox": "0 0 1500 1120",
            "width": "1500",
            "height": "1120",
            "role": "img",
            "aria-labelledby": "figure-title figure-description",
            "font-family": "Inter, ui-sans-serif, system-ui, sans-serif",
        },
    )
    append_title_desc(
        root,
        "Non-grid known-best contact-assembly evidence profile",
        "Thirty-six calibration cases from n equals 1 through 100. Bars show the share "
        "of squares in detected same-angle positive-edge contact components. This is a "
        "descriptive numerical census, not a rigidity, optimality, or hypothesis verdict.",
    )
    append_metadata(
        root,
        {
            "artifact-kind": "known-best-non-grid-contact-evidence-profile",
            "case-count": "36",
            "claim-status": "calibration-only-descriptive-no-hypothesis-verdict",
            "generator": GENERATOR,
            "primary-sweep": PRIMARY_SWEEP,
        },
        coordinates="document-table-layout; svg-y-down; no-packing-coordinates",
    )
    sub(root, "rect", {"width": "1500", "height": "1120", "fill": PAPER_THEME.background})
    _text(
        root,
        x=40,
        y=44,
        value="Non-grid contact-assembly profile · n = 1…100 calibration",
        size=27,
        fill=PAPER_THEME.ink,
        weight="700",
    )
    summary = profile["aggregate"]
    _text(
        root,
        x=40,
        y=73,
        value=(
            f"{summary['structured_square_count']:,}/{summary['square_count']:,} squares "
            f"in {summary['contact_component_count']} same-angle contact components · "
            f"{summary['within_six_components_and_three_free_cases']}/36 cases within C≤6, F≤3"
        ),
        size=16,
        fill=PAPER_THEME.muted,
    )
    _text(
        root,
        x=1460,
        y=44,
        value="DESCRIPTIVE · NO VERDICT",
        size=14,
        fill="#d95f02",
        weight="700",
        anchor="end",
    )

    thresholds = summary["coverage_threshold_cases"]
    narrow_counts = summary["narrow_partition_status_counts"]
    cards = (
        (
            40,
            "Broad contact assembly",
            (
                f"{summary['fully_structured_cases']} fully covered · "
                f"{thresholds['at_least_90_percent']} at least 90% · "
                f"{thresholds['at_least_75_percent']} at least 75% · "
                f"{thresholds['at_least_50_percent']} at least 50%"
            ),
            color_for_square(0),
        ),
        (
            760,
            "Narrow bars / Ls / rectangles",
            (
                f"{narrow_counts['established']} inside budget · "
                f"{narrow_counts['outside-registered-budget']} outside · "
                f"{narrow_counts['not-established']} absent · "
                f"{narrow_counts['not-established-search-limit']} search-capped"
            ),
            "#d95f02",
        ),
    )
    for x, title, detail, accent in cards:
        sub(
            root,
            "rect",
            {
                "x": str(x),
                "y": "92",
                "width": "700",
                "height": "66",
                "rx": "12",
                "fill": PAPER_THEME.panel,
                "stroke": accent,
                "stroke-width": "2",
            },
        )
        _text(root, x=x + 16, y=118, value=title, size=16, fill=accent, weight="700")
        _text(root, x=x + 16, y=143, value=detail, size=14, fill=PAPER_THEME.ink)

    rows = profile["cases"]
    for column in range(2):
        x = 40 + 720 * column
        _text(root, x=x + 12, y=183, value="n · src", size=11, fill=PAPER_THEME.muted)
        _text(
            root,
            x=x + 104,
            y=183,
            value="contact-covered squares",
            size=11,
            fill=PAPER_THEME.muted,
        )
        _text(root, x=x + 392, y=183, value="C", size=11, fill=PAPER_THEME.muted)
        _text(root, x=x + 438, y=183, value="F", size=11, fill=PAPER_THEME.muted)
        _text(root, x=x + 480, y=183, value="max", size=11, fill=PAPER_THEME.muted)
        _text(root, x=x + 530, y=183, value="slide", size=11, fill=PAPER_THEME.muted)
        _text(root, x=x + 582, y=183, value="narrow", size=11, fill=PAPER_THEME.muted)
        _text(root, x=x + 666, y=183, value="broad", size=11, fill=PAPER_THEME.muted)
        for local_index, row in enumerate(rows[column * 18 : (column + 1) * 18]):
            y = 193 + 46 * local_index
            primary = row["primary"]
            delta = row["sensitivity_delta"]
            changed = (
                any(
                    delta[key] != 0
                    for key in (
                        "structured_square_count",
                        "contact_component_count",
                        "free_square_count",
                    )
                )
                or delta["within_budget_changed"]
            )
            source_color = (
                color_for_square(0)
                if row["source_kind"] == "kingbird-derived-facts"
                else color_for_square(1)
            )
            sub(
                root,
                "rect",
                {
                    "x": str(x),
                    "y": str(y),
                    "width": "700",
                    "height": "40",
                    "rx": "7",
                    "fill": PAPER_THEME.panel
                    if local_index % 2 == 0
                    else PAPER_THEME.background,
                    "stroke": "#d95f02" if changed else "#e1e5ea",
                    "stroke-width": "1.5" if changed else "1",
                },
            )
            sub(
                root,
                "circle",
                {"cx": str(x + 76), "cy": str(y + 20), "r": "5", "fill": source_color},
            )
            _text(
                root,
                x=x + 12,
                y=y + 25,
                value=f"{row['n']:02d}",
                size=14,
                fill=PAPER_THEME.ink,
                weight="700",
            )
            _text(
                root,
                x=x + 84,
                y=y + 24,
                value="K" if row["source_kind"] == "kingbird-derived-facts" else "U",
                size=11,
                fill=PAPER_THEME.muted,
            )
            bar_x, bar_y, bar_width = x + 104, y + 12, 198
            sub(
                root,
                "rect",
                {
                    "x": str(bar_x),
                    "y": str(bar_y),
                    "width": str(bar_width),
                    "height": "15",
                    "rx": "7.5",
                    "fill": "#e5e9ee",
                },
            )
            covered_width = bar_width * primary["structured_square_count"] / row["square_count"]
            if covered_width:
                sub(
                    root,
                    "rect",
                    {
                        "x": str(bar_x),
                        "y": str(bar_y),
                        "width": f"{covered_width:.3f}",
                        "height": "15",
                        "rx": "7.5",
                        "fill": source_color,
                    },
                )
            _text(
                root,
                x=x + 310,
                y=y + 25,
                value=f"{primary['structured_square_count']}/{row['square_count']}",
                size=12,
                fill=PAPER_THEME.ink,
            )
            for offset, value in (
                (392, primary["contact_component_count"]),
                (438, primary["free_square_count"]),
                (480, primary["largest_component_size"]),
                (530, primary["internal_slide_dof"]),
            ):
                _text(
                    root,
                    x=x + offset,
                    y=y + 25,
                    value=str(value),
                    size=12,
                    fill=PAPER_THEME.ink,
                )
            _text(
                root,
                x=x + 582,
                y=y + 25,
                value=_partition_label(row["narrow_partition"]),
                size=11,
                fill="#d95f02"
                if row["narrow_partition"]["status"] != "established"
                else color_for_square(0),
            )
            _text(
                root,
                x=x + 666,
                y=y + 25,
                value="yes" if primary["within_six_components_and_three_free"] else "no",
                size=11,
                fill=color_for_square(0)
                if primary["within_six_components_and_three_free"]
                else "#d95f02",
                weight="700",
            )

    _text(
        root,
        x=40,
        y=1053,
        value=(
            "K = retained Kingbird-derived numerical facts · U = six-decimal "
            "UnitSquare rendering-derived normalization · C = multi-square contact "
            "components · F = free squares · orange outline = detector-sensitive row"
        ),
        size=13,
        fill=PAPER_THEME.muted,
    )
    _text(
        root,
        x=40,
        y=1082,
        value=(
            "Primary detector: same fitted angle, positive edge overlap, contact residual "
            "≤ 0.001. Connectedness is not rigidity; slide counts precede overlap intervals "
            "and wall seating."
        ),
        size=13,
        fill=PAPER_THEME.muted,
    )
    _text(
        root,
        x=40,
        y=1107,
        value=(
            "Calibration only. No claim of global optimality, complete chunk grammar, "
            "or H-044 verdict."
        ),
        size=13,
        fill="#d95f02",
        weight="700",
    )
    return serialize_svg(root)


def profile_errors(profile: dict[str, Any]) -> list[str]:
    """Return cross-field errors not conveniently expressed in JSON Schema."""
    errors: list[str] = []
    rows = profile["cases"]
    ns = [row["n"] for row in rows]
    if ns != sorted(ns) or len(ns) != 36 or len(set(ns)) != 36:
        errors.append("case n values must be 36 unique ordered non-grid counts")
    for row in rows:
        primary = row["primary"]
        if row["square_count"] != row["n"]:
            errors.append(f"n={row['n']}: square count must equal n")
        if primary["structured_square_count"] + primary["free_square_count"] != row["n"]:
            errors.append(f"n={row['n']}: structured plus free squares must equal n")
        expected_fraction = _ratio(primary["structured_square_count"], row["n"])
        if primary["structured_fraction"] != expected_fraction:
            errors.append(f"n={row['n']}: structured fraction mismatch")
        expected_budget = (
            primary["contact_component_count"] <= 6 and primary["free_square_count"] <= 3
        )
        if primary["within_six_components_and_three_free"] != expected_budget:
            errors.append(f"n={row['n']}: broad-budget flag mismatch")
        narrow = row["narrow_partition"]
        has_chunk_count = narrow["selected_chunk_count"] is not None
        has_free_count = narrow["selected_free_square_count"] is not None
        requires_counts = narrow["status"] in {
            "established",
            "outside-registered-budget",
        }
        forbids_counts = narrow["status"] == "not-established"
        minimality = narrow["selected_partition_minimality"]
        if (
            has_chunk_count != has_free_count
            or (requires_counts and not has_chunk_count)
            or (forbids_counts and has_chunk_count)
        ):
            errors.append(f"n={row['n']}: narrow-partition status/count mismatch")
        if (has_chunk_count and minimality == "not-applicable") or (
            not has_chunk_count and minimality != "not-applicable"
        ):
            errors.append(f"n={row['n']}: narrow-partition minimality/count mismatch")
        if (
            narrow["status"] == "not-established-search-limit"
            and has_chunk_count
            and minimality != "indeterminate-search-limit"
        ):
            errors.append(f"n={row['n']}: capped selected partition claims minimality")
        if narrow["status"] == "outside-registered-budget" and minimality != "complete":
            errors.append(f"n={row['n']}: conclusive outside-budget row lacks minimality")
    aggregate = profile["aggregate"]
    square_count = sum(row["square_count"] for row in rows)
    structured_square_count = sum(row["primary"]["structured_square_count"] for row in rows)
    checks = {
        "case_count": len(rows),
        "square_count": square_count,
        "structured_square_count": structured_square_count,
        "contact_component_count": sum(
            row["primary"]["contact_component_count"] for row in rows
        ),
        "internal_slide_dof": sum(row["primary"]["internal_slide_dof"] for row in rows),
        "fully_structured_cases": sum(row["primary"]["free_square_count"] == 0 for row in rows),
        "within_six_components_and_three_free_cases": sum(
            row["primary"]["within_six_components_and_three_free"] for row in rows
        ),
    }
    for key, expected in checks.items():
        if aggregate[key] != expected:
            errors.append(f"aggregate {key} mismatch")
    if aggregate["structured_fraction"] != _ratio(structured_square_count, square_count):
        errors.append("aggregate structured fraction mismatch")
    threshold_counts = {
        "at_least_50_percent": sum(
            row["primary"]["structured_square_count"] * 2 >= row["n"] for row in rows
        ),
        "at_least_75_percent": sum(
            row["primary"]["structured_square_count"] * 4 >= row["n"] * 3 for row in rows
        ),
        "at_least_90_percent": sum(
            row["primary"]["structured_square_count"] * 10 >= row["n"] * 9 for row in rows
        ),
    }
    if aggregate["coverage_threshold_cases"] != threshold_counts:
        errors.append("aggregate coverage thresholds mismatch")
    status_counts = dict(
        sorted(Counter(row["narrow_partition"]["status"] for row in rows).items())
    )
    if aggregate["narrow_partition_status_counts"] != status_counts:
        errors.append("aggregate narrow-partition statuses mismatch")
    changed_ns = [
        row["n"]
        for row in rows
        if any(
            row["sensitivity_delta"][key] != 0
            for key in (
                "structured_square_count",
                "contact_component_count",
                "free_square_count",
            )
        )
        or row["sensitivity_delta"]["within_budget_changed"]
    ]
    sensitivity = aggregate["sensitivity_comparison"]
    expected_sensitivity = {
        "changed_case_count": len(changed_ns),
        "changed_ns": changed_ns,
        "primary_structured_square_count": structured_square_count,
        "sensitivity_structured_square_count": sum(
            row["primary"]["structured_square_count"]
            + row["sensitivity_delta"]["structured_square_count"]
            for row in rows
        ),
        "within_budget_flip_ns": [
            row["n"] for row in rows if row["sensitivity_delta"]["within_budget_changed"]
        ],
    }
    if sensitivity != expected_sensitivity:
        errors.append("aggregate sensitivity comparison mismatch")
    source_strata = []
    for source_kind in ("kingbird-derived-facts", "unitsquare-rendering"):
        selected_rows = [row for row in rows if row["source_kind"] == source_kind]
        stratum_squares = sum(row["square_count"] for row in selected_rows)
        stratum_structured = sum(
            row["primary"]["structured_square_count"] for row in selected_rows
        )
        source_strata.append(
            {
                "case_count": len(selected_rows),
                "fully_structured_cases": sum(
                    row["primary"]["free_square_count"] == 0 for row in selected_rows
                ),
                "sensitivity_changed_ns": [
                    row["n"] for row in selected_rows if row["n"] in changed_ns
                ],
                "source_kind": source_kind,
                "square_count": stratum_squares,
                "structured_fraction": _ratio(stratum_structured, stratum_squares),
                "structured_square_count": stratum_structured,
                "within_six_components_and_three_free_cases": sum(
                    row["primary"]["within_six_components_and_three_free"]
                    for row in selected_rows
                ),
            }
        )
    if aggregate["source_strata"] != source_strata:
        errors.append("aggregate source strata mismatch")
    return errors


def schema_errors(profile: dict[str, Any]) -> list[str]:
    """Return structural-schema errors for mutation controls."""
    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    return [
        problem.message
        for problem in sorted(
            Draft202012Validator(schema).iter_errors(profile),
            key=lambda problem: list(problem.path),
        )
    ]


def _index(items: list[dict[str, Any]], key: str) -> dict[int, dict[str, Any]]:
    result = {item["n"]: item for item in items}
    if len(result) != len(items):
        raise ValueError(f"duplicate n in {key}")
    return result


def expected_outputs() -> tuple[dict[str, Any], str]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas"]
    components = json.loads(COMPONENTS.read_text(encoding="utf-8"))
    partitions = json.loads(PARTITIONS.read_text(encoding="utf-8"))["atlas"]
    source_entries = _index(manifest["entries"], "manifest")
    sweeps = {sweep["name"]: sweep for sweep in components["contact_sweeps"]}
    bands = {band["name"]: band for band in partitions["bands"]}
    primary = _index(sweeps[PRIMARY_SWEEP]["entries"], PRIMARY_SWEEP)
    sensitivity = _index(sweeps[SENSITIVITY_SWEEP]["entries"], SENSITIVITY_SWEEP)
    narrow = _index(bands[PARTITION_BAND]["entries"], PARTITION_BAND)
    non_grid_ns = sorted(
        n for n, entry in source_entries.items() if entry["source"]["kind"] != "exact-grid"
    )
    rows: list[dict[str, Any]] = []
    for n in non_grid_ns:
        source_kind = source_entries[n]["source"]["kind"]
        base = primary[n]
        alternate = sensitivity[n]
        partition = narrow[n]
        if partition["source_kind"] != source_kind:
            raise ValueError(f"n={n}: partition source kind does not match manifest")
        contact_components = [
            component for component in base["components"] if component["size"] >= 2
        ]
        if len(contact_components) != base["contact_chunk_count"]:
            raise ValueError(f"n={n}: contact component count mismatch")
        delta = {
            "contact_component_count": alternate["contact_chunk_count"]
            - base["contact_chunk_count"],
            "free_square_count": alternate["free_square_count"] - base["free_square_count"],
            "structured_square_count": alternate["structured_square_count"]
            - base["structured_square_count"],
            "within_budget_changed": alternate["within_six_chunks_and_three_free"]
            != base["within_six_chunks_and_three_free"],
        }
        rows.append(
            {
                "n": n,
                "narrow_partition": {
                    "selected_chunk_count": partition["selected_chunk_count"],
                    "selected_free_square_count": partition["selected_free_square_count"],
                    "selected_partition_minimality": partition["selected_partition_minimality"],
                    "status": partition["status"],
                },
                "primary": {
                    "angle_class_count": base["angle_class_count"],
                    "contact_component_count": base["contact_chunk_count"],
                    "contact_edge_count": sum(
                        len(component["edges"]) for component in contact_components
                    ),
                    "free_square_count": base["free_square_count"],
                    "internal_slide_dof": base["internal_slide_dof"],
                    "largest_component_size": max(
                        component["size"] for component in base["components"]
                    ),
                    "structured_fraction": _ratio(base["structured_square_count"], n),
                    "structured_square_count": base["structured_square_count"],
                    "wall_seated_square_count": base["wall_seated_square_count"],
                    "within_six_components_and_three_free": base[
                        "within_six_chunks_and_three_free"
                    ],
                },
                "sensitivity_delta": delta,
                "source_kind": source_kind,
                "square_count": n,
            }
        )

    status_counts = Counter(row["narrow_partition"]["status"] for row in rows)
    changed_ns = [
        row["n"]
        for row in rows
        if any(
            row["sensitivity_delta"][key] != 0
            for key in (
                "structured_square_count",
                "contact_component_count",
                "free_square_count",
            )
        )
        or row["sensitivity_delta"]["within_budget_changed"]
    ]
    source_strata = []
    for source_kind in ("kingbird-derived-facts", "unitsquare-rendering"):
        selected = [row for row in rows if row["source_kind"] == source_kind]
        square_count = sum(row["square_count"] for row in selected)
        structured = sum(row["primary"]["structured_square_count"] for row in selected)
        source_strata.append(
            {
                "case_count": len(selected),
                "fully_structured_cases": sum(
                    row["primary"]["free_square_count"] == 0 for row in selected
                ),
                "sensitivity_changed_ns": [
                    row["n"] for row in selected if row["n"] in changed_ns
                ],
                "source_kind": source_kind,
                "square_count": square_count,
                "structured_fraction": _ratio(structured, square_count),
                "structured_square_count": structured,
                "within_six_components_and_three_free_cases": sum(
                    row["primary"]["within_six_components_and_three_free"] for row in selected
                ),
            }
        )

    square_count = sum(row["square_count"] for row in rows)
    structured = sum(row["primary"]["structured_square_count"] for row in rows)
    primary_summary = sweeps[PRIMARY_SWEEP]["summary"]["non_grid"]
    sensitivity_summary = sweeps[SENSITIVITY_SWEEP]["summary"]["non_grid"]
    aggregate = {
        "case_count": len(rows),
        "contact_component_count": sum(
            row["primary"]["contact_component_count"] for row in rows
        ),
        "coverage_threshold_cases": {
            "at_least_50_percent": sum(
                row["primary"]["structured_square_count"] * 2 >= row["n"] for row in rows
            ),
            "at_least_75_percent": sum(
                row["primary"]["structured_square_count"] * 4 >= row["n"] * 3 for row in rows
            ),
            "at_least_90_percent": sum(
                row["primary"]["structured_square_count"] * 10 >= row["n"] * 9 for row in rows
            ),
        },
        "fully_structured_cases": sum(row["primary"]["free_square_count"] == 0 for row in rows),
        "internal_slide_dof": sum(row["primary"]["internal_slide_dof"] for row in rows),
        "narrow_partition_status_counts": dict(sorted(status_counts.items())),
        "sensitivity_comparison": {
            "changed_case_count": len(changed_ns),
            "changed_ns": changed_ns,
            "primary_structured_square_count": primary_summary["structured_squares"],
            "sensitivity_structured_square_count": sensitivity_summary["structured_squares"],
            "within_budget_flip_ns": [
                row["n"] for row in rows if row["sensitivity_delta"]["within_budget_changed"]
            ],
        },
        "source_strata": source_strata,
        "square_count": square_count,
        "structured_fraction": _ratio(structured, square_count),
        "structured_square_count": structured,
        "within_six_components_and_three_free_cases": sum(
            row["primary"]["within_six_components_and_three_free"] for row in rows
        ),
    }
    profile = {
        "aggregate": aggregate,
        "cases": rows,
        "claim_boundaries": [
            "The retained n=1..100 corpus is calibration-only and supplies no H-044 verdict.",
            (
                "Detected same-angle positive-edge contact establishes descriptive "
                "assembly, not rigidity."
            ),
            "Internal slide degrees are counted before overlap intervals and wall seating.",
            (
                "Narrow partition non-establishment applies only to bars, filled "
                "rectangles, and corner Ls."
            ),
            (
                "Retained constructions are feasible witnesses, not new global-optimality "
                "certificates."
            ),
        ],
        "claim_status": "calibration-only-descriptive-no-hypothesis-verdict",
        "detectors": {
            "primary_sweep": PRIMARY_SWEEP,
            "sensitivity_sweep": SENSITIVITY_SWEEP,
        },
        "generated_by": GENERATOR,
        "inputs": {
            "contact_census": "chunk-components.json",
            "corpus": "manifest.json",
            "narrow_partitions": "chunk-partitions.json",
        },
        "rendering": {
            "path": str(RENDERING.relative_to(ROOT)),
            "semantics": "descriptive-document-table-no-packing-geometry",
        },
        "scope": {
            "excluded_exact_grid_cases": 64,
            "non_grid_cases": 36,
            "range": "n=1..100",
        },
    }
    rendering = render_profile(profile)
    errors = [*schema_errors(profile), *profile_errors(profile)]
    if errors:
        raise ValueError("invalid known-best chunk evidence profile: " + "; ".join(errors))
    document = {
        "softschema": {
            "contract": "packing.squares:KnownBestChunkEvidenceProfile/v1",
            "envelope": "profile",
            "schema": "chunk-evidence-profile.schema.yaml",
            "status": "enforced",
        },
        "profile": profile,
    }
    return document, rendering


def update() -> None:
    document, rendering = expected_outputs()
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(_json_text(document), encoding="utf-8")
    write_svg_atomic(RENDERING, rendering)
    print("known-best chunk evidence profile updated: 36 non-grid calibration cases")


def check() -> None:
    document, rendering = expected_outputs()
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != _json_text(document):
        raise ValueError("known-best chunk evidence profile is missing or stale")
    if not RENDERING.is_file() or RENDERING.read_text(encoding="utf-8") != rendering:
        raise ValueError("known-best chunk evidence overview is missing or stale")
    unexpected = {path.name for path in EVIDENCE_ROOT.glob("*.svg")} - {RENDERING.name}
    if unexpected:
        raise ValueError(f"unexpected known-best evidence renderings: {sorted(unexpected)}")
    print("known-best chunk evidence profile check passed: 36 non-grid calibration cases")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    update() if args.update else check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
