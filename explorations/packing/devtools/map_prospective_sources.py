#!/usr/bin/env python3
"""Build the source-availability-only map for prospective ``n = 101..324``."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

from strif import atomic_output_file

from sqpack.known_best import KINGBIRD_BASE_URL, catalogue_source_map
from sqpack.render.svg import append_metadata, append_title_desc, element, serialize_svg, sub

ROOT = Path(__file__).resolve().parent.parent
CATALOGUE = ROOT / "resources/web/kingbird-squares-in-squares.html"
UNITSQUARE_RESULTS = ROOT / "resources/web/unitsquare-release1-2026/results.json"
OUTPUT = ROOT / "atlas/prospective/source-availability-101-324.json"
COVERAGE_OUTPUT = ROOT / "atlas/prospective/source-coverage-101-324.svg"
GENERATOR = "python -m devtools.map_prospective_sources"

COVERAGE_WIDTH = 1440
COVERAGE_HEIGHT = 1030
COVERAGE_FIRST_N = 101
COVERAGE_LAST_N = 324
COVERAGE_COUNT = COVERAGE_LAST_N - COVERAGE_FIRST_N + 1
COVERAGE_COLUMNS = 16
COVERAGE_ROWS = 14
COVERAGE_GRID_LEFT = 60
COVERAGE_GRID_TOP = 250
COVERAGE_COLUMN_PITCH = 82
COVERAGE_ROW_PITCH = 49
COVERAGE_CELL_WIDTH = 76
COVERAGE_CELL_HEIGHT = 42
COVERAGE_FONT = "Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif"
COVERAGE_STYLES = {
    "exact-grid-retained": ("#cceee6", "#0f513f", "#0f8f79"),
    "licensed-svg-retained": ("#dbeafe", "#1e3a8a", "#4361c2"),
    "public-svg-license-deferred": ("#ffedd5", "#7c2d12", "#d97706"),
    "no-located-source": ("#e2e8f0", "#475569", "#94a3b8"),
}
COVERAGE_STROKES = {
    "exact-grid-retained": {"stroke-width": "1"},
    "licensed-svg-retained": {"stroke-width": "2.5"},
    "public-svg-license-deferred": {
        "stroke-width": "1.4",
        "stroke-dasharray": "5 3",
    },
    "no-located-source": {"stroke-width": "1", "stroke-dasharray": "2 3"},
}


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def availability_errors(availability: dict) -> list[str]:
    """Return cross-field errors not expressible in the JSON Schema."""
    errors: list[str] = []
    entries = availability["entries"]
    numbers = [entry["n"] for entry in entries]
    if numbers != list(range(COVERAGE_FIRST_N, COVERAGE_LAST_N + 1)):
        errors.append("entries must contain each n=101..324 exactly once and in order")

    summary = availability["summary"]
    counts = Counter(entry["source_key"] for entry in entries)
    expected_counts = {
        "catalogue-trivial-grid-rule": summary["exact_generated_grid_cases"],
        "kingbird-current-catalogue": summary["kingbird_selected_cases"],
        "unitsquare-release-1": summary["unitsquare_selected_cases"],
    }
    if counts != Counter(expected_counts):
        errors.append("entry source counts do not match summary")

    for entry in entries:
        n = entry["n"]
        has_upstream_digest = "upstream_declared_sha256" in entry
        if has_upstream_digest != (entry["source_key"] == "unitsquare-release-1"):
            errors.append(f"n={n}: upstream digest ownership is inconsistent")
        if n not in entry["listed_n"] or entry["source_n"] != max(entry["listed_n"]):
            errors.append(f"n={n}: source/listed identity is inconsistent")
        if entry["source_key"] == "catalogue-trivial-grid-rule":
            expected_side = math.isqrt(n - 1) + 1
            if entry.get("trivial_grid_side") != expected_side:
                errors.append(f"n={n}: incorrect exact-grid side")
            if any(entry[field] is not None for field in ("source_path", "source_url")):
                errors.append(f"n={n}: generated grid unexpectedly has a remote source")
        elif "trivial_grid_side" in entry:
            errors.append(f"n={n}: remote SVG unexpectedly has an exact-grid side")

    selected_unitsquare = {
        entry["n"] for entry in entries if entry["source_key"] == "unitsquare-release-1"
    }
    if selected_unitsquare != {103, 105, 110, 131}:
        errors.append("UnitSquare precedence must select exactly n=103,105,110,131")

    if any(
        source["coordinate_use"] != "prohibited"
        for source in availability["visual_only_sources"]
    ):
        errors.append("visual sources cannot supply coordinates")

    audit = availability["access_audit"]
    for key in ("kingbird", "unitsquare"):
        receipt = audit[key]
        if receipt["urls_checked"] != receipt["svg_responses"]:
            errors.append(f"{key}: URL and SVG-response counts differ")
    kingbird = audit["kingbird"]
    if (
        kingbird["adapter_passed"] + len(kingbird["adapter_gap_sources"])
        != kingbird["svg_responses"]
    ):
        errors.append("Kingbird adapter pass and gap counts do not exhaust responses")
    gap_paths = [gap["source_path"] for gap in kingbird["adapter_gap_sources"]]
    if gap_paths:
        errors.append("Kingbird adapter gaps differ from the sequential audit")
    return errors


def expected_document() -> dict:
    """Return the deterministic availability map from retained listing evidence."""
    catalogue = catalogue_source_map(
        CATALOGUE, first_n=COVERAGE_FIRST_N, last_n=COVERAGE_LAST_N
    )
    release = json.loads(UNITSQUARE_RESULTS.read_text(encoding="utf-8"))
    improvements = {
        result["n"]: result
        for result in release["results"]
        if COVERAGE_FIRST_N <= result["n"] <= COVERAGE_LAST_N
    }

    entries = []
    for n in range(COVERAGE_FIRST_N, COVERAGE_LAST_N + 1):
        if n in improvements:
            result = improvements[n]
            entries.append(
                {
                    "classification": "remote-svg-geometry",
                    "listed_n": [n],
                    "n": n,
                    "source_key": "unitsquare-release-1",
                    "source_n": n,
                    "source_path": result["svg"],
                    "source_url": f"https://www.hmbelvedere.com/{result['svg']}",
                    "upstream_declared_sha256": result["svg_sha256"],
                }
            )
        elif n in catalogue:
            filename, source_n, listed_n = catalogue[n]
            entries.append(
                {
                    "classification": "remote-svg-geometry",
                    "listed_n": list(listed_n),
                    "n": n,
                    "source_key": "kingbird-current-catalogue",
                    "source_n": source_n,
                    "source_path": filename,
                    "source_url": f"{KINGBIRD_BASE_URL}/{filename}",
                }
            )
        else:
            side = math.isqrt(n - 1) + 1
            entries.append(
                {
                    "classification": "exact-generated-geometry",
                    "listed_n": [n],
                    "n": n,
                    "source_key": "catalogue-trivial-grid-rule",
                    "source_n": n,
                    "source_path": None,
                    "source_url": None,
                    "trivial_grid_side": side,
                }
            )

    counts = Counter(entry["source_key"] for entry in entries)
    document = {
        "softschema": {
            "contract": "packing.squares:ProspectiveSourceAvailability/v1",
            "envelope": "availability",
            "schema": "prospective-source-availability.schema.yaml",
            "status": "enforced",
        },
        "availability": {
            "claim_status": "source-availability-only-no-annotations",
            "generated_by": GENERATOR,
            "range": {
                "count": COVERAGE_COUNT,
                "first_n": COVERAGE_FIRST_N,
                "last_n": COVERAGE_LAST_N,
            },
            "readiness": {
                "acquisition": "incomplete",
                "normalization": "incomplete",
                "source_selection": "provisionally-complete",
            },
            "policy": {
                "coordinate_sources": (
                    "Use full SVG geometry or exact generated grids only. Never transcribe "
                    "coordinates from raster images or video."
                ),
                "selection_order": (
                    "Select a newer UnitSquare certified construction when present; otherwise "
                    "select the current Kingbird catalogue SVG; otherwise apply the "
                    "catalogue's "
                    "stated trivial no-tilt grid rule through n=324."
                ),
                "annotation_boundary": (
                    "This map records availability and provenance only. It contains no "
                    "contact, "
                    "chunk, rigidity, or grammar annotation and supplies no hypothesis verdict."
                ),
                "rendering": (
                    "Any acquired geometry must be normalized to Witness/v2 and rendered with "
                    "the repository's deterministic house renderer."
                ),
            },
            "summary": {
                "exact_generated_grid_cases": counts["catalogue-trivial-grid-rule"],
                "kingbird_selected_cases": counts["kingbird-current-catalogue"],
                "kingbird_svg_groups_in_range": len({value[0] for value in catalogue.values()}),
                "kingbird_svg_listed_cases": len(catalogue),
                "selected_cases": len(entries),
                "unitsquare_selected_cases": counts["unitsquare-release-1"],
            },
            "sources": [
                {
                    "access": "public-http-svg",
                    "acquisition_status": "deferred-pending-license-review",
                    "evidence_path": "resources/web/kingbird-squares-in-squares.html",
                    "format": "html-listing-and-svg-geometry",
                    "key": "kingbird-current-catalogue",
                    "license_status": "not-stated-on-inspected-catalogue-page",
                    "url": "https://kingbird.myphotos.cc/packing/squares_in_squares.html",
                },
                {
                    "access": "public-http-svg",
                    "acquisition_status": "eligible-after-retention-control",
                    "evidence_path": "resources/web/unitsquare-release1-2026/results.json",
                    "format": "json-index-and-svg-geometry",
                    "key": "unitsquare-release-1",
                    "license_status": "CC-BY-4.0-in-dataset-page-metadata",
                    "url": "https://www.hmbelvedere.com/",
                },
                {
                    "access": "local-deterministic-generation",
                    "acquisition_status": "ready",
                    "evidence_path": "resources/web/kingbird-squares-in-squares.html",
                    "format": "catalogue-rule-and-exact-grid",
                    "key": "catalogue-trivial-grid-rule",
                    "license_status": "generated-locally-from-stated-mathematical-rule",
                    "url": "https://kingbird.myphotos.cc/packing/squares_in_squares.html",
                },
            ],
            "access_audit": {
                "checked_at": "2026-08-26T06:03:34-07:00",
                "kingbird": {
                    "adapter_gap_sources": [],
                    "adapter_passed": 114,
                    "svg_responses": 114,
                    "urls_checked": 114,
                },
                "method": (
                    "Fetched every distinct active Kingbird SVG concurrently, then parsed "
                    "each sequentially at its catalogue count. Duplicate IDs use DOM's first "
                    "element in tree order; one invalid bare local use is ignored only after "
                    "the remaining geometry matches the declared count. Fetched the four "
                    "selected UnitSquare SVGs, matched their declared hashes, and parsed their "
                    "complete square counts."
                ),
                "unitsquare": {
                    "adapter_passed": 4,
                    "declared_hashes_matched": 4,
                    "svg_responses": 4,
                    "urls_checked": 4,
                },
            },
            "visual_only_sources": [
                {
                    "channel": "Deckard",
                    "coordinate_use": "prohibited",
                    "title": "Packing Squares Inside The Smallest Square Possible",
                    "url": "https://www.youtube.com/watch?v=uL5wuiy34rs",
                    "use": "visual-index-and-aesthetic-cross-check-only",
                    "video_id": "uL5wuiy34rs",
                },
                {
                    "channel": "Andy Math",
                    "coordinate_use": "prohibited",
                    "title": "Square Packing",
                    "url": "https://www.youtube.com/watch?v=jToq8C89r0I",
                    "use": "visual-index-only",
                    "video_id": "jToq8C89r0I",
                },
                {
                    "channel": "OneMinuteThings",
                    "coordinate_use": "prohibited",
                    "title": "Square packing is weird.",
                    "url": "https://www.youtube.com/watch?v=81DCjd5DPMs",
                    "use": "visual-index-only",
                    "video_id": "81DCjd5DPMs",
                },
            ],
            "excluded_sources": [
                {
                    "reason": (
                        "Older records or alternative packings are not the active selection."
                    ),
                    "url": "https://kingbird.myphotos.cc/packing/squares_in_squares__compared2.html",
                },
                {
                    "reason": (
                        "Older records or alternative packings are not the active selection."
                    ),
                    "url": "https://kingbird.myphotos.cc/packing/squares_in_squares__compared3.html",
                },
                {
                    "reason": (
                        "Duplicate table presentation, useful for browsing but not a second "
                        "geometry authority."
                    ),
                    "url": "https://kingbird.myphotos.cc/packing/squares_in_squares__triangular_table.html",
                },
                {
                    "reason": (
                        "Raster and video frames are visual evidence only; coordinate "
                        "transcription is prohibited."
                    ),
                    "url": "https://www.youtube.com/",
                },
            ],
            "entries": entries,
        },
    }
    errors = availability_errors(document["availability"])
    if errors:
        raise ValueError("invalid prospective availability map: " + "; ".join(errors))
    return document


def _coverage_status(entry: dict) -> str:
    return {
        "catalogue-trivial-grid-rule": "exact-grid-retained",
        "unitsquare-release-1": "licensed-svg-retained",
        "kingbird-current-catalogue": "public-svg-license-deferred",
    }.get(entry["source_key"], "no-located-source")


def _append_coverage_stat(
    root: ET.Element,
    *,
    x: int,
    count: int,
    label: str,
    status: str,
) -> None:
    background, ink, accent = COVERAGE_STYLES[status]
    group = sub(root, "g", {"data-feature": "coverage-stat", "data-coverage": status})
    sub(
        group,
        "rect",
        {
            "x": str(x),
            "y": "127",
            "width": "310",
            "height": "82",
            "rx": "12",
            "fill": background,
        },
    )
    sub(
        group,
        "rect",
        {
            "x": str(x),
            "y": "127",
            "width": "8",
            "height": "82",
            "rx": "4",
            "fill": accent,
        },
    )
    sub(
        group,
        "text",
        {
            "x": str(x + 26),
            "y": "166",
            "font-family": COVERAGE_FONT,
            "font-size": "28",
            "font-weight": "700",
            "fill": ink,
        },
    ).text = str(count)
    sub(
        group,
        "text",
        {
            "x": str(x + 26),
            "y": "192",
            "font-family": COVERAGE_FONT,
            "font-size": "14",
            "fill": ink,
        },
    ).text = label


def render_coverage_svg(availability: dict) -> str:
    """Render the audited source status for every prospective ``n``."""
    entries = availability["entries"]
    if [entry["n"] for entry in entries] != list(range(COVERAGE_FIRST_N, COVERAGE_LAST_N + 1)):
        raise ValueError("coverage SVG requires exactly n=101..324 in order")
    status_counts = Counter(_coverage_status(entry) for entry in entries)
    root = element(
        "svg",
        {
            "width": str(COVERAGE_WIDTH),
            "height": str(COVERAGE_HEIGHT),
            "viewBox": f"0 0 {COVERAGE_WIDTH} {COVERAGE_HEIGHT}",
            "role": "img",
            "aria-labelledby": "figure-title figure-description",
        },
    )
    append_title_desc(
        root,
        "Source coverage for square packings beyond one hundred",
        (
            "An audited grid for n equals 101 through 324. Ninety-seven exact grids and "
            "four licensed SVG constructions are retained locally. Public SVG geometry "
            "was located and parsed for the other 123 cases, but retention is deferred "
            "pending license review. No case in the audited range lacks selected geometry."
        ),
    )
    append_metadata(
        root,
        {
            "audit-checked-at": availability["access_audit"]["checked_at"],
            "claim-status": availability["claim_status"],
            "columns": str(COVERAGE_COLUMNS),
            "first-n": str(COVERAGE_FIRST_N),
            "generated-by": GENERATOR,
            "last-n": str(COVERAGE_LAST_N),
            "located-source-gaps": "0",
            "rows": str(COVERAGE_ROWS),
            "selected-cases": str(COVERAGE_COUNT),
        },
        coordinates="document-grid; row-major n=101..324",
    )
    sub(
        root,
        "rect",
        {"width": str(COVERAGE_WIDTH), "height": str(COVERAGE_HEIGHT), "fill": "#ffffff"},
    )
    sub(
        root,
        "text",
        {
            "x": "60",
            "y": "58",
            "font-family": COVERAGE_FONT,
            "font-size": "36",
            "font-weight": "700",
            "fill": "#17202a",
        },
    ).text = "What is available beyond n = 100?"
    sub(
        root,
        "text",
        {
            "x": "60",
            "y": "95",
            "font-family": COVERAGE_FONT,
            "font-size": "18",
            "fill": "#5c6673",
        },
    ).text = "Audited n = 101-324  ·  all 224 cases have selected geometry"

    _append_coverage_stat(
        root,
        x=60,
        count=status_counts["exact-grid-retained"],
        label="exact grids retained",
        status="exact-grid-retained",
    )
    _append_coverage_stat(
        root,
        x=397,
        count=status_counts["licensed-svg-retained"],
        label="licensed SVGs retained",
        status="licensed-svg-retained",
    )
    _append_coverage_stat(
        root,
        x=734,
        count=status_counts["public-svg-license-deferred"],
        label="public SVGs, license deferred",
        status="public-svg-license-deferred",
    )
    _append_coverage_stat(
        root,
        x=1071,
        count=status_counts["no-located-source"],
        label="no located source",
        status="no-located-source",
    )

    for index, entry in enumerate(entries):
        row, column = divmod(index, COVERAGE_COLUMNS)
        x = COVERAGE_GRID_LEFT + column * COVERAGE_COLUMN_PITCH
        y = COVERAGE_GRID_TOP + row * COVERAGE_ROW_PITCH
        status = _coverage_status(entry)
        background, ink, accent = COVERAGE_STYLES[status]
        cell = sub(
            root,
            "g",
            {
                "data-feature": "coverage-cell",
                "data-n": str(entry["n"]),
                "data-coverage": status,
                "data-source-key": entry["source_key"],
            },
        )
        cell_attributes = {
            "x": str(x),
            "y": str(y),
            "width": str(COVERAGE_CELL_WIDTH),
            "height": str(COVERAGE_CELL_HEIGHT),
            "rx": "7",
            "fill": background,
            "stroke": accent,
            **COVERAGE_STROKES[status],
        }
        sub(
            cell,
            "rect",
            cell_attributes,
        )
        sub(
            cell,
            "text",
            {
                "x": str(x + COVERAGE_CELL_WIDTH // 2),
                "y": str(y + 27),
                "text-anchor": "middle",
                "font-family": COVERAGE_FONT,
                "font-size": "14",
                "font-weight": "600",
                "fill": ink,
            },
        ).text = str(entry["n"])

    sub(
        root,
        "text",
        {
            "x": "60",
            "y": "974",
            "font-family": COVERAGE_FONT,
            "font-size": "15",
            "fill": "#475569",
        },
    ).text = (
        "The orange cells are a local retention-policy gap, not a gap in located public "
        "geometry."
    )
    sub(
        root,
        "text",
        {
            "x": "60",
            "y": "1002",
            "font-family": COVERAGE_FONT,
            "font-size": "13",
            "fill": "#64748b",
        },
    ).text = (
        "Availability audit 2026-08-26 · Kingbird 114/114 distinct SVG groups parsed "
        "· UnitSquare 4/4 declared hashes matched"
    )
    return serialize_svg(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document = expected_document()
    rendered = _json_text(document)
    coverage = render_coverage_svg(document["availability"])
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != rendered:
            raise ValueError("prospective source-availability map is missing or stale")
        if (
            not COVERAGE_OUTPUT.is_file()
            or COVERAGE_OUTPUT.read_text(encoding="utf-8") != coverage
        ):
            raise ValueError("prospective source-coverage SVG is missing or stale")
        print("prospective source map check passed: 224 cases, availability and SVG")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(rendered, encoding="utf-8")
    with atomic_output_file(COVERAGE_OUTPUT) as temporary:
        temporary.write_text(coverage, encoding="utf-8")
    print("prospective source map updated: 224 cases, availability and SVG")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
