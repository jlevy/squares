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

The tool's other behaviors are checked by running them rather than by reading their
declarations: the metric patch over a synthetic KaTeX table, the stock-KaTeX baseline
the variant pages are built against, and the reconciliation that holds each route's CSS
to its own metric plan. A route measured against the wrong baseline, or drawn from a
face KaTeX is not measuring, is the failure mode the whole tool exists to prevent, and
neither shows up as an error -- only as a montage that answers a question nobody asked.

The reconciliation is tested from both sides, because a checker that has only ever
passed cannot be told from one that cannot fail: every built-in route is clean, and each
of the four routes that shipped broken is rebuilt here and reported. What no test here
can do is compare ink with metrics -- that needs a browser and the built pages, and it
is `compare_math_fonts verify`, run as a gate rather than under pytest.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from devtools.compare_math_fonts import (
    DEFAULT_FACES,
    GREEK_SCALE,
    PROSE_FONTS,
    WHOLE_FACE,
    FaceMetrics,
    Variant,
    built_in_variants,
    measure,
    metrics_table,
    page_faces,
    patch_metrics,
    reconcile,
    stock_katex_baseline,
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


def _prose(style: str, weight: str, payload: str) -> str:
    """One of kpress's own blocks, pretty-printed the way it writes them."""
    return (
        f'@font-face {{ font-family: "PT Serif"; font-style: {style}; '
        f'font-weight: {weight}; src: url("data:font/woff2;base64,{payload}"); }}'
    )


def _katex(name: str, style: str, payload: str) -> str:
    """One of KaTeX's, minified inside the bundle's stylesheet the way it ships them."""
    return (
        f"@font-face{{font-display:swap;font-family:{name};font-style:{style};"
        f'font-weight:400;src:url("data:font/woff2;base64,{payload}")}}'
    )


#: The five `@font-face` blocks a route is assembled from, in the two shapes the page
#: actually carries them in. Nothing here reads the font bytes, but the five payloads
#: differ, because a route is traced back to its file by the URL it was built from and
#: five faces sharing one URL would all look like the same face.
MINIMAL_PAGE = (
    _prose("normal", "400", "AA==")
    + _prose("italic", "400", "AQ==")
    + _prose("normal", "700", "Ag==")
    + _katex("KaTeX_Main", "normal", "Aw==")
    + _katex("KaTeX_Math", "italic", "BA==")
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


#: One face's entries in the shape KaTeX bakes them into `katex.min.js`: a code point,
#: then `[depth, height, italic correction, skew, width]`. `43` is `+`, which no route
#: moves; `48` and `49` are `0` and `1`, which every route does. Short enough to read,
#: and it exercises the same substitution the whole 900 KB table goes through.
SYNTHETIC_TABLE = (
    '"Main-Regular":{43:[.08333,.58333,0,0,.77778],48:[0,.64444,0,0,.5],49:[0,.64444,0,0,.5]}'
)

#: The one route the rewrite is checked on: digits from PT Serif Regular into the
#: Main-Regular table, which is Route B's swap and the first half of every later route's.
_DIGIT_VARIANT = Variant(
    "digits-only",
    "digits from PT Serif Regular",
    css="",
    swaps=(("Main-Regular", "pt-serif-latin-400-normal.woff2", tuple(range(0x30, 0x3A))),),
)


def test_the_metric_patch_rewrites_the_digits_and_nothing_else() -> None:
    """The rewrite moves the entries the variant swaps, to the shipped face's own bounds.

    The counted-entries test above reads the route's declaration; this one runs the
    substitution over a table and reads what came out, against the two figures the
    kpress brief spot-checks its own generator on: a PT Serif digit is 0.712 em tall
    and 0.533 em wide, against the 0.644 and 0.5 KaTeX believes it is placing. That
    0.068 em of width is why an unpatched page sets numbers in boxes too narrow for
    them, and the 0.068 em of height is what clips a numerator at 3x.
    """
    patched, rewritten = patch_metrics(SYNTHETIC_TABLE, _DIGIT_VARIANT, PROSE_FONTS)

    assert rewritten == 2
    # `0` overshoots the baseline, so its depth moves too; `1` sits on it.
    assert "48:[0.01200,0.71200,0.00000,0.0,0.53300]" in patched
    assert "49:[0.00000,0.71200,0.00000,0.0,0.53300]" in patched
    # `+` is not a glyph any route redirects, so its entry is passed through untouched.
    assert "43:[.08333,.58333,0,0,.77778]" in patched


@pytest.fixture(scope="module")
def routes() -> dict[str, Variant]:
    """The eight built-in routes, built from the synthetic page above."""
    return {variant.name: variant for variant in built_in_variants(page_faces(MINIMAL_PAGE))}


def test_every_built_in_route_draws_what_it_measures(routes: dict[str, Variant]) -> None:
    r"""Each route's CSS and its metric plan are held to each other, per code point.

    Four routes shipped whose two descriptions disagreed, and every one of them rendered
    without an error: `\sin` drawn from KaTeX and measured from PT Serif, a whole face
    scaled in CSS and only its letters in the plan, five operators moved with no entries
    for them, and scaled Greek capitals shadowed by a family claiming the whole plane.
    The check reads both descriptions rather than agreeing with either.
    """
    faces = page_faces(MINIMAL_PAGE)
    for variant in routes.values():
        assert reconcile(variant, faces) == [], variant.name


#: The four shapes the PR #114 review found, each as the smallest change to a shipped
#: route that makes it describe itself twice again. Built from the routes themselves so
#: that a future route cannot drift out from under them: two of the four are literally
#: another shipped route's plan against this one's CSS, which is what the defect was.
def _broken(routes: dict[str, Variant]) -> list[tuple[str, Variant, str]]:
    letters = tuple(range(0x41, 0x5B)) + tuple(range(0x61, 0x7B))
    return [
        (
            "a row the plan moves and the CSS leaves on KaTeX",
            replace(
                routes["digits"],
                swaps=(
                    *routes["digits"].swaps,
                    ("Main-Regular", "pt-serif-latin-400-normal.woff2", (0x2B,)),
                ),
            ),
            "U+002B",
        ),
        (
            "a row the CSS moves and the plan does not",
            replace(routes["ops"], swaps=routes["all"].swaps),
            "U+002B, U+003C-003E, U+2212",
        ),
        (
            "a scale narrower than the face the CSS adjusts",
            replace(routes["sizeadj"], scales=(("Math-Italic", letters, GREEK_SCALE),)),
            "Math-Italic",
        ),
        (
            "a scale the CSS never applies",
            replace(
                routes["all-1em"],
                swaps=routes["greek"].swaps,
                scales=routes["greek"].scales,
            ),
            "Main-Regular",
        ),
    ]


def test_a_route_that_describes_itself_twice_is_reported(routes: dict[str, Variant]) -> None:
    """The checker fails on each of the four routes that shipped disagreeing with itself.

    A checker that has only ever passed cannot be told from one that cannot fail, and
    this one passes on all eight routes above. So each defect is rebuilt and reported,
    and the reported text has to name the code points, because "something disagrees" sends
    the reader back to the same two descriptions that disagreed in the first place.
    """
    faces = page_faces(MINIMAL_PAGE)
    for shape, variant, expected in _broken(routes):
        found = reconcile(variant, faces)
        assert found, shape
        assert any(expected in line for line in found), (shape, found)


def test_a_whole_face_scale_moves_every_row_of_that_face() -> None:
    """A `size-adjust` with no `unicode-range` scales the file, so the plan scales the table.

    The route that eliminated itself scaled KaTeX_Math by 1.134 in CSS and only its Latin
    letters in the plan, which drew `\\alpha` 13.4% larger than the box KaTeX had placed
    it in. `WHOLE_FACE` is the plan that says what the CSS says: `43` is `+` and `48` is
    `0`, and both move, where a code-point list would have had to name them.
    """
    whole = Variant(
        "whole-face",
        "the adjusted face",
        css="",
        scales=(("Main-Regular", WHOLE_FACE, 1.134),),
    )
    patched, rewritten = patch_metrics(SYNTHETIC_TABLE, whole, PROSE_FONTS)

    assert rewritten == 3
    assert "43:[0.09450,0.66150,0.00000,0.00000,0.88200]" in patched
    assert "48:[0.00000,0.73079,0.00000,0.00000,0.56700]" in patched


def test_the_baseline_switches_the_pages_own_math_text_face_off() -> None:
    """A variant page opts out of kpress's feature, whatever the rendered page declared.

    Both shapes matter: the explainer renders `<html ... data-kpress-math-text="prose">`
    today, and a page rendered with the attribute left off would silently take kpress's
    default. One attribute reverts both halves of the feature -- the stylesheet's rules
    and the page's inline metric install -- so `current` is stock KaTeX either way.
    """
    rendered = '<!doctype html>\n<html lang="en"\n      data-kpress-math-text="prose">\n<head>'
    assert 'data-kpress-math-text="katex"' in stock_katex_baseline(rendered)
    assert 'data-kpress-math-text="prose"' not in stock_katex_baseline(rendered)
    assert stock_katex_baseline(rendered).count("data-kpress-math-text") == 1

    bare = '<!doctype html>\n<html lang="en">\n<head>'
    assert '<html lang="en" data-kpress-math-text="katex">' in stock_katex_baseline(bare)
