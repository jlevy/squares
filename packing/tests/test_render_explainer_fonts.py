"""The four rules that decide which faces the explainer ships, and at what cost.

`tests/test_explainer.py` renders the page and asserts that nothing in it is a
reference outside it. That is the property, and it is the wrong instrument for these
four seams: a page that inlines every face in the distribution passes it, and so does
a page that drops the half of a composite slot the other half depends on. The first
costs 40 KB a face; the second is worse than either alternative, because the reading
face's metric tables would still be installed and KaTeX would lay out digits it is not
drawing -- the exact mismatch the math text face exists to prevent.

So the four are exercised directly, on inputs small enough to read:

- `inline_font_urls` over the four `url()` shapes the distribution actually carries,
  and over the two refusals it owes a build: a face that names a file that is not
  there, and a kept face that still names a source the rewrite did not reach.
- `_font_face_reachable` over both prunes, the KaTeX one and the composite one, in the
  keeping and the dropping direction. The composite's reading-face blocks name no KaTeX
  file at all, so their reachability is their slot partner's, and `KaTeX_Math-BoldItalic`
  is the partner this page cannot reach.
- `katex_js`'s ordering guard, which is what keeps kpress's metric tables from being
  loaded before the bundle they patch.
- `_print_sans_face`, the prune that keeps kpress's static print instances out of the
  page. They are at kpress's weight tokens and this page prints at its own, so they
  would answer nothing while costing 20 KB of base64 a face in every copy served; the
  PDF pass injects this page's own set into the loaded document instead.

One test does read the real static tree, and it is the one that has to: that registering
`print-fonts.css` upstream leaves the rendered page byte for byte where it was. Nothing
else here reads a real font -- `tmp_path` holds two stand-in files of a few bytes -- and
the whole file still runs in well under a second, so it belongs in the quick lane and
carries no marker.
"""

# `_font_face_reachable` and `_print_sans_face` are the prunes, and they are private
# because nothing outside the renderer should decide what a page ships. Testing them
# directly rather than through `katex_css` is what keeps all but one test here off the
# real static tree, and every one of them off a 1.4 MB page.
# pyright: reportPrivateUsage=false
from __future__ import annotations

import base64
from pathlib import Path

import pytest
from kpress.format import assets as kpress_assets

from devtools.render_explainer import (
    _declares_nothing,
    _font_face_reachable,
    _print_sans_face,
    inline_font_urls,
    katex_js,
    kpress_css,
    kpress_static,
)
from devtools.sans_instances import SCREEN_SANS, print_family

#: kpress's generated print-face stylesheet, registered in `DEFAULT_CSS_ASSETS`.
PRINT_FONTS = "css/print-fonts.css"

#: Stand-ins for the two faces the shapes below reference. Any bytes will do: the
#: rewrite reads a file and base64s it, and nothing in this file parses a font.
PROSE_BYTES = b"pt-serif-regular-stand-in"
MATH_BYTES = b"katex-main-regular-stand-in"


def _data_uri(payload: bytes) -> str:
    return f"data:font/woff2;base64,{base64.b64encode(payload).decode()}"


PROSE_URI = _data_uri(PROSE_BYTES)
MATH_URI = _data_uri(MATH_BYTES)


@pytest.fixture
def stylesheet_dir(tmp_path: Path) -> Path:
    """kpress's static tree in miniature, and the directory a stylesheet is served from.

    `katex/` beside `fonts/`, which is the only structure the three relative shapes
    depend on: `../fonts/` climbs to the reading faces, a bare `fonts/` stays inside
    `katex/`, and the composite's `../katex/fonts/` climbs and comes back to the same
    place. Resolving from the stylesheet's own directory is what makes all three work
    without a special case, so the fixture returns that directory rather than the root.
    """
    (tmp_path / "katex" / "fonts").mkdir(parents=True)
    (tmp_path / "katex" / "fonts" / "KaTeX_Main-Regular.woff2").write_bytes(MATH_BYTES)
    (tmp_path / "fonts").mkdir()
    (tmp_path / "fonts" / "pt-serif-latin-400-normal.woff2").write_bytes(PROSE_BYTES)
    return tmp_path / "katex"


def _kpress_block(source: str) -> str:
    """kpress's own shape: pretty-printed, quoted, with a `format()` clause after it."""
    return (
        '@font-face {\n  font-family: "PT Serif";\n  font-style: normal;\n'
        f'  src: url("{source}") format("woff2");\n}}'
    )


def _katex_block(source: str) -> str:
    """KaTeX's, out of the minified bundle: one line, and the bare form is unquoted."""
    return (
        "@font-face{font-display:swap;font-family:KaTeX_Main;font-style:normal;"
        f"font-weight:400;src:url({source})}}"
    )


def _composite_block(source: str) -> str:
    """The composite's Greek half, which reaches sideways out of `katex/` and back in."""
    return (
        '@font-face {\n  font-family: "KPress Math Text";\n  size-adjust: 102.5%;\n'
        f'  src: url("{source}") format("woff2");\n'
        "  unicode-range: U+0391-03A9;\n}"
    )


#: The four `@font-face` shapes the distribution carries, each with what it must become.
#: kpress writes its own pretty-printed with a `format()` clause; the minified KaTeX
#: bundle writes a bare, unquoted, relative `url()`; the composite reaches sideways into
#: `../katex/fonts/`; and a stylesheet inlined once already must survive being inlined
#: again unchanged, since `kpress_css` and `katex_css` both run this over whole files.
FONT_FACE_SHAPES: list[tuple[str, str, str]] = [
    (
        "kpress-quoted-relative",
        _kpress_block("../fonts/pt-serif-latin-400-normal.woff2"),
        _kpress_block(PROSE_URI),
    ),
    (
        "katex-bare-relative",
        _katex_block("fonts/KaTeX_Main-Regular.woff2"),
        _katex_block(f'"{MATH_URI}"'),
    ),
    (
        "composite-sideways",
        _composite_block("../katex/fonts/KaTeX_Main-Regular.woff2"),
        _composite_block(MATH_URI),
    ),
    (
        "already-inlined",
        _kpress_block(PROSE_URI),
        _kpress_block(PROSE_URI),
    ),
]


@pytest.mark.parametrize(
    ("css", "expected"),
    [pytest.param(css, expected, id=name) for name, css, expected in FONT_FACE_SHAPES],
)
def test_every_font_face_shape_becomes_a_data_uri(
    css: str, expected: str, stylesheet_dir: Path
) -> None:
    """Each shape is resolved from the stylesheet's directory, and nothing else moves."""
    assert inline_font_urls(css, stylesheet_dir) == expected


def test_a_face_the_stylesheet_names_but_does_not_ship_fails_the_render(
    stylesheet_dir: Path,
) -> None:
    """An unresolved reference is a build error, not a face left to the reader's machine.

    Falling back would be silent and would look almost right: the page would draw
    mathematics in whatever the reader has, laid out from metrics for a face that never
    arrived.
    """
    css = '@font-face { font-family: "Gone"; src: url("../fonts/gone.woff2"); }'
    with pytest.raises(SystemExit, match="which is not there"):
        inline_font_urls(css, stylesheet_dir)


def test_a_kept_face_that_still_names_a_file_fails_the_render(stylesheet_dir: Path) -> None:
    """The self-containment check covers every source, not only the woff2 ones.

    The rewrite recognises `.woff2`, because that is all the pinned distribution
    carries. A `woff` or `truetype` fallback added upstream would pass straight through
    it and ship as a relative path beside a file that has no such neighbour, so a kept
    block naming any non-`data:` source stops the build instead.
    """
    css = (
        '@font-face { font-family: "PT Serif";\n'
        '  src: url("../fonts/pt-serif-latin-400-normal.woff2") format("woff2"),\n'
        '       url("../fonts/pt-serif-latin-400-normal.woff") format("woff"); }'
    )
    with pytest.raises(SystemExit, match="still fetches"):
        inline_font_urls(css, stylesheet_dir)


def _katex_font_block(face: str) -> str:
    """A KaTeX `@font-face`, judged on the file it names."""
    return (
        f"@font-face{{font-display:swap;font-family:{face.partition('-')[0]};"
        f"font-style:normal;font-weight:400;src:url(fonts/{face}.woff2)}}"
    )


def _composite_slot_block(style: str, weight: str, source: str) -> str:
    """A composite slot's reading half, which names no KaTeX file for the prune to read."""
    return (
        f'@font-face {{\n  font-family: "KPress Math Text";\n  font-style: {style};\n'
        f"  font-weight: {weight};\n  font-display: swap;\n"
        f'  src: url("../fonts/{source}") format("woff2");\n'
        "  unicode-range: U+0041-005A, U+0061-007A;\n}"
    )


#: The two prunes, in both directions. The first two blocks name a KaTeX file and are
#: judged on it; the second two are the composite's reading-face halves, which name no
#: KaTeX file and are judged on the KaTeX face their slot replaces.
REACHABILITY_CASES: list[tuple[str, str, bool]] = [
    ("katex-face-the-page-draws", _katex_font_block("KaTeX_Main-Regular"), True),
    ("katex-face-the-page-cannot-reach", _katex_font_block("KaTeX_Fraktur-Regular"), False),
    (
        "composite-slot-with-a-reachable-partner",
        _composite_slot_block("italic", "400", "pt-serif-latin-400-italic.woff2"),
        True,
    ),
    (
        "composite-slot-whose-partner-is-dropped",
        _composite_slot_block("italic", "700", "pt-serif-latin-700-italic.woff2"),
        False,
    ),
]


@pytest.mark.parametrize(
    ("block", "reachable"),
    [pytest.param(block, reachable, id=name) for name, block, reachable in REACHABILITY_CASES],
)
def test_only_the_faces_the_page_can_draw_are_kept(block: str, *, reachable: bool) -> None:
    """Both halves of a composite slot are kept or dropped together.

    The bold-italic slot is the case that matters: the page sets nothing in bold italic,
    so `KaTeX_Math-BoldItalic` is outside `KATEX_FACES` and its PT Serif partner goes
    with it. Keeping the reading half alone would be a slot the CSS calls one contract,
    split -- 40 KB shipped for a range whose Greek is gone.
    """
    assert _font_face_reachable(block) is reachable


#: What kpress's list must not become. The tables patch the bundle's own metrics through
#: `katex.__setFontMetrics`, so a list that loads them first would install them into
#: nothing and leave the page drawing PT Serif from Computer Modern's measurements.
BAD_ASSET_LISTS: list[tuple[str, list[str], str]] = [
    (
        "tables-before-the-bundle",
        [
            "katex/katex-text-metrics.js",
            "katex/katex.min.js",
            "katex/katex-init.js",
        ],
        "which cannot be right",
    ),
    (
        "tables-gone",
        ["katex/katex.min.js", "katex/auto-render.min.js", "katex/katex-init.js"],
        "no longer lists",
    ),
]


@pytest.mark.parametrize(
    ("listed", "complaint"),
    [pytest.param(listed, complaint, id=name) for name, listed, complaint in BAD_ASSET_LISTS],
)
def test_the_metric_tables_must_follow_the_bundle_they_patch(
    listed: list[str], complaint: str, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Both refusals fire before a byte is read, so the static tree is not needed."""
    monkeypatch.setattr(kpress_assets, "KATEX_JS_ASSETS", listed)
    with pytest.raises(SystemExit, match=complaint):
        katex_js(tmp_path)


def _sans_face(family: str, weight: int) -> str:
    """One of kpress's generated print instances, in the shape its generator writes."""
    return (
        f'  @font-face {{\n    font-family: "{family}";\n    font-style: normal;\n'
        f"    font-display: swap;\n    font-weight: {weight};\n"
        f'    src: url("../fonts/kpress-print-sans-latin-{weight}-normal.woff2")'
        ' format("woff2");\n'
        "  }\n"
    )


#: The prune, in both directions. Only the static print family goes: it is the one this
#: page overrides, and it is asked of kpress rather than spelled here, so a rename
#: upstream moves the case with the rule. `Source Sans 3 Variable` is a different family
#: and a different string, and the page's screen face; the rest are what the document is
#: set in.
PRINT_SANS_CASES: list[tuple[str, str, bool]] = [
    ("the static print instance", _sans_face(print_family(), 550), True),
    ("the variable face the screen uses", _sans_face(SCREEN_SANS, 400), False),
    ("the reading face", _kpress_block("../fonts/pt-serif-latin-400-normal.woff2"), False),
    ("the composite", _composite_block("../katex/fonts/KaTeX_Main-Regular.woff2"), False),
    ("a KaTeX face", _katex_block("fonts/KaTeX_Main-Regular.woff2"), False),
]


@pytest.mark.parametrize(
    ("block", "dropped"),
    [pytest.param(block, dropped, id=name) for name, block, dropped in PRINT_SANS_CASES],
)
def test_only_kpress_own_print_instances_are_pruned(block: str, *, dropped: bool) -> None:
    """Judged on the family alone, so the rule survives kpress reshaping the stylesheet.

    The variable face is the case that matters: it is what the screen reads in, and
    dropping it would leave the page with no sans at all. It was also the near miss the
    whole-string comparison was written for -- while the instances were declared under
    `"Source Sans 3"`, `"Source Sans 3 Variable"` shared its first eleven characters.
    kpress's rename put the two families further apart than that; the comparison is
    still whole, because the next family it declares may not be.
    """
    assert _print_sans_face(block) is dropped


#: What a stylesheet is once its faces are gone, and what is not empty. The `@media`
#: wrapper is kpress's: the instances are declared inside one so a screen never fetches
#: them, and pruning the faces out of it leaves the wrapper behind.
EMPTINESS_CASES: list[tuple[str, str, bool]] = [
    ("a comment and an emptied media block", "/* generated */\n\n@media print {\n}\n", True),
    ("nested empty blocks", "@media print {\n  @supports (x: y) {\n  }\n}\n", True),
    ("whitespace", "\n\n  \n", True),
    ("one real rule left in the block", "@media print {\n  body { margin: 0 }\n}\n", False),
    ("a rule outside any block", "/* c */\n:root { --x: 1 }\n", False),
]


@pytest.mark.parametrize(
    ("css", "empty"),
    [pytest.param(css, empty, id=name) for name, css, empty in EMPTINESS_CASES],
)
def test_a_stylesheet_with_nothing_left_in_it_does_not_enter_the_page(
    css: str, *, empty: bool
) -> None:
    """Not even as its own comment marker, which is what keeps the page's bytes still."""
    assert _declares_nothing(css) is empty


def test_registering_the_print_faces_upstream_does_not_move_the_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """kpress's print stylesheet arrives, and the served page is byte for byte where it was.

    The one test here that reads the real static tree, because the claim is about that
    tree: twelve faces at kpress's weights, about 250 KB of base64, land in
    `DEFAULT_CSS_ASSETS` and none of it reaches a reader. The PDF pass supplies this
    page's own instances at this page's weights, to the loaded document only.
    """
    static = kpress_static()
    if not (static / PRINT_FONTS).is_file():
        pytest.skip(f"kpress ships no {PRINT_FONTS} at this gitlink")
    listed = [name for name in kpress_assets.DEFAULT_CSS_ASSETS if name != PRINT_FONTS]
    monkeypatch.setattr(kpress_assets, "DEFAULT_CSS_ASSETS", listed)
    without = kpress_css(static)
    monkeypatch.setattr(kpress_assets, "DEFAULT_CSS_ASSETS", [*listed, PRINT_FONTS])
    assert kpress_css(static) == without
    assert f'font-family: "{SCREEN_SANS}"' in without
