"""The measurements the math-text-face decision was made on, pinned to the shipped files.

`vendor/kpress/docs/math-text-face.research.md` argues from one table, and three of its
rows are the argument: PT Serif's x-height is 0.714 of its cap height against Computer
Modern's 0.647, so no single scale factor matches both; its stems are heavier, so no
scale factor matches the weight; and its operators are centred at 344 against KaTeX's
250, which is why no route moves them. A tool that reported those figures differently
would not fail -- it would quietly re-argue the decision, which is why the numbers are
here rather than only in the prose.

The two faces checked are the two the brief tabulates most closely, one from each side
of the pairing. The whole file reads two woff2 files and takes well under a second, so
it belongs in the quick lane and carries no marker.
"""

from __future__ import annotations

import pytest

from devtools.compare_math_fonts import (
    DEFAULT_FACES,
    FaceMetrics,
    built_in_variants,
    measure,
    metrics_table,
    page_faces,
)


@pytest.fixture(scope="module")
def faces() -> dict[str, FaceMetrics]:
    """Every shipped face measured once, since the rest of the file only reads them."""
    return {label: measure(label, path) for label, path in DEFAULT_FACES}


def test_pt_serif_regular_matches_the_brief(faces: dict[str, FaceMetrics]) -> None:
    face = faces["PT Serif Regular"]
    assert round(face.x_height) == 500
    assert round(face.cap_height) == 700
    assert round(face.digit_height or 0) == 712
    assert round(face.ascender or 0) == 752
    assert round(face.operator_centre or 0) == 344
    assert round(face.hairline or 0) == 53
    assert round(face.stem or 0) == 90
    assert round(face.round_stroke or 0) == 96


def test_katex_main_regular_matches_the_brief(faces: dict[str, FaceMetrics]) -> None:
    face = faces["KaTeX_Main-Regular"]
    assert round(face.x_height) == 442
    # The declared x-height and the ink of `x` disagree by 11 units in this face, and
    # KaTeX's own layout constant is the ink figure. Both are reported for that reason.
    assert round(face.x_height_ink or 0) == 431
    assert round(face.cap_height) == 683
    assert round(face.digit_height or 0) == 666
    assert round(face.ascender or 0) == 694
    assert round(face.operator_centre or 0) == 250
    assert round(face.hairline or 0) == 40
    assert round(face.stem or 0) == 81
    assert round(face.round_stroke or 0) == 98


def test_the_table_reports_both_x_heights_only_where_they_differ(
    faces: dict[str, FaceMetrics],
) -> None:
    table = metrics_table([faces["PT Serif Regular"], faces["KaTeX_Main-Regular"]])
    prose = "| PT Serif Regular | 500 | 700 | 712 | 752 | 344 | 53 | 90 | 96 |"
    math = "| KaTeX_Main-Regular | 442 (ink 431) | 683 | 666 | 694 | 250 | 40 | 81 | 98 |"
    assert prose in table
    assert math in table


#: The three `@font-face` blocks a variant is assembled from, in the two shapes the page
#: actually carries them in: kpress writes its own pretty-printed, KaTeX's arrive
#: minified inside the bundle's stylesheet. Nothing here reads the font bytes.
MINIMAL_PAGE = (
    '@font-face { font-family: "PT Serif"; font-style: normal; font-weight: 400;'
    ' src: url("data:font/woff2;base64,AA=="); }'
    "@font-face{font-display:swap;font-family:KaTeX_Main;font-style:normal;"
    'font-weight:400;src:url("data:font/woff2;base64,AA==")}'
    "@font-face{font-display:swap;font-family:KaTeX_Math;font-style:italic;"
    'font-weight:400;src:url("data:font/woff2;base64,AA==")}'
)


def test_the_all_latin_route_swaps_the_228_entries_the_brief_counts() -> None:
    """Route D's metric patch is 228 entries.

    A route that moved fewer glyphs than it claims, or more, would be a different
    experiment from the one the brief decided on, and the montages would not be
    comparable with the ones already published.
    """
    variants = {
        variant.name: variant for variant in built_in_variants(page_faces(MINIMAL_PAGE))
    }
    assert list(variants) == [
        "current",
        "digits",
        "letters",
        "all",
        "all-1em",
        "sizeadj",
        "ops",
        "greek",
    ]
    swapped = sum(len(code_points) for _, _, code_points in variants["all"].swaps)
    assert swapped == 228
