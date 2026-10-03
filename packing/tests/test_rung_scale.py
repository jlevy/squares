"""The rung chips' colour scale: saturation and strength rise with the level, and the
chip's text stays readable on every fill.

The scale is four tokens a theme and a hue a ladder in `templates/site.css`;
`devtools.rung_scale` computes every fill they make and the contrast of the page's text
on it, with no browser. These tests hold that report to what the design system says of
it (`templates/paper-design.md`, Color, The Rung Scale).
"""

from __future__ import annotations

from itertools import pairwise

import pytest

from devtools import render_overview, rung_scale
from devtools.overview_sections import rubric_levels

#: The ladders that carry a hue, and so a chroma that rises.
HUED = ("V", "C")
#: The minus sign the design document writes a negative step with.
MINUS = chr(0x2212)


@pytest.fixture(scope="module")
def fills() -> list[rung_scale.Fill]:
    return rung_scale.fills()


def _ladder(fills: list[rung_scale.Fill], theme: str, scale: str) -> list[rung_scale.Fill]:
    ladder = [fill for fill in fills if fill.theme == theme and fill.scale == scale]
    assert [fill.level for fill in ladder] == sorted(fill.level for fill in ladder)
    return ladder


def _rising(values: list[float]) -> bool:
    return all(low < high for low, high in pairwise(values))


def test_every_rung_of_the_rubric_has_a_fill_in_both_themes(
    fills: list[rung_scale.Fill],
) -> None:
    levels = rubric_levels()
    expected = [
        (theme, f"{scale}{level}")
        for theme in rung_scale.THEMES
        for scale in rung_scale.LADDERS
        for level, _ in sorted(levels[scale])
    ]
    assert [(fill.theme, fill.rung) for fill in fills] == expected
    used = {level for scale in rung_scale.LADDERS for level, _ in levels[scale]}
    assert used <= rung_scale.styled_levels()


@pytest.mark.parametrize("theme", rung_scale.THEMES)
@pytest.mark.parametrize("scale", HUED)
def test_saturation_rises_with_the_level(
    theme: str, scale: str, fills: list[rung_scale.Fill]
) -> None:
    """Rung 0 is the least saturated and the top rung the most, with no step level or
    reversed, whether saturation is read as chroma or as chroma against lightness."""
    ladder = _ladder(fills, theme, scale)
    assert ladder[0].level == 0
    assert _rising([fill.chroma for fill in ladder])
    assert _rising([fill.chroma / fill.lightness for fill in ladder])
    assert ladder[-1].chroma >= 4 * ladder[0].chroma


@pytest.mark.parametrize("theme", rung_scale.THEMES)
@pytest.mark.parametrize("scale", rung_scale.LADDERS)
def test_strength_rises_with_the_level(
    theme: str, scale: str, fills: list[rung_scale.Fill]
) -> None:
    """Each level is further from the page background than the one below it, in
    lightness and in contrast against the page: darker in light mode, lighter in dark."""
    page = rung_scale.page_colours()[theme]["bg"]
    ladder = _ladder(fills, theme, scale)
    assert _rising([abs(fill.lightness - page[0]) for fill in ladder])
    against_page = [
        rung_scale.contrast(page, (fill.lightness, fill.chroma, fill.hue)) for fill in ladder
    ]
    assert _rising(against_page)
    direction = -1 if theme == "light" else 1
    assert all(direction * (fill.lightness - page[0]) > 0 for fill in ladder)


@pytest.mark.parametrize("theme", rung_scale.THEMES)
def test_rung_zero_is_closest_to_the_neutral_background(
    theme: str, fills: list[rung_scale.Fill]
) -> None:
    page = rung_scale.page_colours()[theme]["bg"]
    for scale in HUED:
        lowest = _ladder(fills, theme, scale)[0]
        assert abs(lowest.lightness - page[0]) <= 0.07, lowest
        assert lowest.chroma <= 0.02, lowest


def test_significance_is_drawn_in_its_own_teal_ink() -> None:
    """Significance is no chip (`think-m3m4`): its rung is drawn on the page in
    `--site-significance`, a teal between the confirmation green and the verification
    blue in hue, so it reads as neither, and darker than the accent in light mode, so it
    never reads as a link. It is text, held to 4.5:1 against the page in both themes, and
    inside sRGB, so no browser maps its chroma down."""
    drawn = [ink for ink in rung_scale.inks() if ink.rung == "--site-significance"]
    assert [ink.theme for ink in drawn] == list(rung_scale.THEMES)
    hues = {
        ladder: float(tokens["--rung-hue"])
        for ladder, tokens in rung_scale.ladder_tokens().items()
    }
    # The accent's light lightness, 51.09% (paper-design.md, Color).
    accent_light = 0.5109
    for ink in drawn:
        assert hues["C"] < ink.hue < hues["V"], ink
        assert ink.in_gamut, ink
        assert ink.contrast >= rung_scale.MINIMUM_CONTRAST, ink
    light = next(ink for ink in drawn if ink.theme == "light")
    assert light.lightness < accent_light - 0.05, light


def test_every_ink_keeps_the_contrast_its_use_needs() -> None:
    """Each ink the site draws with on the page, in each theme: text at 4.5:1, the
    new-result star, a symbol, at 3:1, and every one inside sRGB."""
    drawn = rung_scale.inks()
    assert {ink.rung for ink in drawn} == set(rung_scale.INKS)
    for ink in drawn:
        assert ink.in_gamut, ink
        assert ink.contrast >= rung_scale.INKS[ink.rung], ink


def test_every_fill_is_shown_as_written_and_keeps_its_text_readable(
    fills: list[rung_scale.Fill],
) -> None:
    """Inside sRGB, so no browser maps the chroma down, and the page's text on the fill
    at WCAG AA or better. One text colour serves every step of a theme."""
    for fill in fills:
        assert fill.in_gamut, fill
        assert fill.contrast >= rung_scale.MINIMUM_CONTRAST, fill


def test_the_scale_is_tokens_and_no_chip_has_a_value_of_its_own() -> None:
    """One `oklch()` in the rung rules, the rule's; a ladder sets a hue or a chroma and a
    level sets its number, never a colour."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    start = css.index(".site-rung-fill {")
    rules = css[start : css.index(".site-star {", start)]
    assert rules.count("oklch(") == 1
    assert rules.count("background:") == 1
    assert "#" not in rules
    for theme, tokens in rung_scale.theme_tokens().items():
        assert set(tokens) == {
            "--site-rung-base",
            "--site-rung-step",
            "--site-rung-chroma-base",
            "--site-rung-chroma-step",
        }, theme
    for scale, declared in rung_scale.ladder_tokens().items():
        assert set(declared) == {
            "--rung-hue",
            "--rung-chroma-base",
            "--rung-chroma-step",
            "--rung-level",
        }, scale


def test_the_design_document_carries_the_measured_scale(
    fills: list[rung_scale.Fill],
) -> None:
    """The table in `paper-design.md` is this tool's output, and the token table beside
    it states the tokens `site.css` sets."""
    design = (render_overview.TEMPLATES / "paper-design.md").read_text(encoding="utf-8")
    for line in rung_scale.markdown_table(fills).splitlines():
        assert line in design, line
    themes = rung_scale.theme_tokens()
    for token in sorted(themes["light"]):
        light, dark = (themes[theme][token].replace("-", MINUS) for theme in rung_scale.THEMES)
        dark = f"+{dark}" if token == "--site-rung-step" else dark
        row = [line for line in design.splitlines() if line.startswith(f"| `{token}`")]
        assert len(row) == 1, token
        assert row[0].endswith(f"| {light} | {dark} |"), row[0]
    lowest = {
        theme: min(fill.contrast for fill in fills if fill.theme == theme)
        for theme in rung_scale.THEMES
    }
    assert (
        f"{lowest['light']:.1f}:1 or better in light mode and "
        f"{lowest['dark']:.1f}:1 or better in dark"
    ) in " ".join(design.split())


def test_the_status_chips_take_fills_from_the_scale() -> None:
    """A status chip's fill is the rung scale's at its own hue and level (the owner,
    2026-10-02, `think-c19o`): a result's `confirmed` the green of the confirmation
    rungs at C3's strength, its `reviewed` the verification rungs' blue, a case's
    `proved` a green and its `open` a yellow. Each is in gamut with the page's text at
    WCAG AA or better on it in both themes, and the one `oklch()` that makes them is the
    status rule's, so no status has a colour of its own."""
    statuses = rung_scale.status_fills()
    assert {fill.rung for fill in statuses} == {"confirmed", "reviewed", "proved", "open"}
    assert {fill.theme for fill in statuses} == set(rung_scale.THEMES)
    for fill in statuses:
        assert fill.in_gamut, fill
        assert fill.contrast >= rung_scale.MINIMUM_CONTRAST, fill
    hues = {fill.rung: fill.hue for fill in statuses}
    ladders = rung_scale.ladder_tokens()
    assert hues["confirmed"] == float(ladders["C"]["--rung-hue"])
    assert hues["reviewed"] == float(ladders["V"]["--rung-hue"])
    assert 130 <= hues["proved"] <= 160
    assert 80 <= hues["open"] <= 110
    confirmed = {fill.theme: fill for fill in statuses if fill.rung == "confirmed"}
    for fill in rung_scale.fills():
        if fill.rung == "C3":
            assert (fill.lightness, fill.chroma) == pytest.approx(
                (confirmed[fill.theme].lightness, confirmed[fill.theme].chroma)
            )
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    start = css.index(".site-chip:is([data-case-status]")
    rules = css[start : css.index("\n/*", start)]
    assert rules.count("oklch(") == 1
    assert "#" not in rules
    assert 'data-tone="accent"' not in css


def test_the_design_document_carries_the_status_fills() -> None:
    """The status table in `paper-design.md` is this tool's output."""
    design = (render_overview.TEMPLATES / "paper-design.md").read_text(encoding="utf-8")
    for line in rung_scale.markdown_table(rung_scale.status_fills(), "Status").splitlines():
        assert line in design, line


def test_the_design_document_carries_the_inks() -> None:
    """The ink table in `paper-design.md` is this tool's output."""
    design = (render_overview.TEMPLATES / "paper-design.md").read_text(encoding="utf-8")
    for line in rung_scale.ink_table(rung_scale.inks()).splitlines():
        assert line in design, line
