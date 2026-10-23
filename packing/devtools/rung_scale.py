#!/usr/bin/env python3
"""The rung chips' colour scale as the stylesheet makes it: every fill, and the contrast
of the chip's text on it.

A rung chip's fill is one rule in `templates/site.css`,
`oklch(base + level * step, chroma-base + level * chroma-step, hue)`, from four tokens a
theme sets and a hue (and, for significance, a flat chroma) a ladder sets. This reads
those tokens from the stylesheet, the page's text and background colours from kpress's
own, and the levels of each ladder from `epistemics.md`, and reports each rung in each
theme: the fill in OkLCh and as sRGB hex, whether sRGB holds it, and the WCAG contrast
ratio of the page's text on it.

The status chips take fills from the same scale, a rule each in the stylesheet naming
a hue, a level and an optional chroma boost (`status_fills`, the owner, 2026-10-02,
`think-c19o`), and are reported the same way. So are the topic chips that Results and
News once shared. Result kinds keep those fills (`topic_fills`); News now uses one
neutral surface and colored ink (`news_topic_inks`). News inks must keep 4.5:1 contrast
against that surface in both themes. Result-topic fills retain their distinctness
contract against statuses and each other. The V and C rung
fills are not compared: a rung chip names its rung, and the upper-bound topic stands
0.020 from C1 in the dark theme, a pairing older than the topic palette.

Significance is no chip since 2026-10-03 (`think-m3m4`): its rung is drawn in an ink of
its own, `--site-significance`, on the page itself. The inks, that one and the
new-result star's, are reported against the page's background in each theme
(`inks`), each held to the contrast its use needs: text 4.5:1, and a symbol 3:1.

It needs no browser. `tests/test_rung_scale.py` holds the scale to what the design
system says of it (`templates/paper-design.md`, Color): saturation and strength rise
with the level, every fill is in gamut, and the text keeps 4.5:1 on every one. The same
test holds the table in that document to this tool's output.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.rung_scale
"""

from __future__ import annotations

import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from math import atan2, cos, degrees, hypot, radians, sin
from pathlib import Path

from devtools.overview_sections import rubric_levels
from devtools.render_n11_lower_bounds_explainer import kpress_static
from devtools.render_overview import SITE_CSS
from devtools.site_topics import NEWS_TOPICS, TOPICS
from sqpack.render.color import (
    _linear_to_srgb,  # pyright: ignore[reportPrivateUsage]
    _maximum_chroma,  # pyright: ignore[reportPrivateUsage]
    _oklch_linear_rgb,  # pyright: ignore[reportPrivateUsage]
    hex_oklch,
)

#: The ladders drawn as chips, in the order the site lists them. Significance, which the
#: site lists first, is drawn in an ink of its own (`INKS`).
LADDERS = ("V", "C")
THEMES = ("light", "dark")
#: WCAG 2 AA for body text, which a chip's label is.
MINIMUM_CONTRAST = 4.5
#: The inks the site draws with on the page itself, each with the contrast against the
#: page its use needs: significance is text, the star a symbol (WCAG 1.4.11, 3:1).
INKS = {"--site-significance": MINIMUM_CONTRAST, "--site-new-result": 3.0}

_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
_BLOCK = re.compile(r"([^{}]+)\{([^{}]*)\}")
_DECLARATION = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);")
_OKLCH = re.compile(r"oklch\(\s*([\d.]+)%\s+([\d.]+)\s+([\d.]+)\s*\)")
_VAR = re.compile(r"var\((--[\w-]+)\)")
#: A status chip's own rule: its attribute, a result's `status` or a case's
#: `case-status`, and its word.
_STATUS_RULE = re.compile(r'\.site-chip\[data-(status|case-status)="([a-z-]+)"\]')
#: Only result-kind fills; News topic ink is measured separately.
_TOPIC = re.compile(r'\[data-kind="([a-z-]+)"\]')
#: A bound topic's fill: its bound's ink mixed into the page background in OkLab.
_BOUND_MIX = re.compile(
    r"color-mix\(\s*in oklab,\s*var\((--site-bound-[a-z]+)\)\s+var\((--site-chip-tint)\),"
    r"\s*var\(--kpress-doc-bg\)\s*\)"
)
_HEX = re.compile(r"#[0-9a-fA-F]{6}")
#: The least OkLab distance between two fills that mean different things, about one
#: just noticeable difference.
DISTINCT = 0.02
#: The fills that mean one thing on two chips: the Verification topic is a result's
#: `reviewed` blue.
SHARED_FILLS = frozenset({frozenset({"verification", "reviewed"})})

Oklch = tuple[float, float, float]


@dataclass(frozen=True)
class Fill:
    """One rung's chip in one theme."""

    theme: str
    rung: str
    lightness: float
    chroma: float
    hue: float
    hex: str
    in_gamut: bool
    contrast: float

    @property
    def level(self) -> int:
        return int(self.rung[1:])

    @property
    def scale(self) -> str:
        return self.rung[0]

    @property
    def oklch(self) -> str:
        return f"oklch({self.lightness * 100:.1f}% {self.chroma:.3f} {self.hue:g})"


def _blocks(css: Path) -> list[tuple[str, dict[str, str]]]:
    """A stylesheet's rules as (selector, custom properties), comments dropped."""
    text = _COMMENT.sub("", css.read_text(encoding="utf-8"))
    return [
        (" ".join(selector.split()), dict(_DECLARATION.findall(body)))
        for selector, body in _BLOCK.findall(text)
    ]


def _is_dark(selector: str) -> bool:
    return 'data-kpress-resolved-theme="dark"' in selector


def _number(value: str) -> float:
    value = value.strip()
    return float(value[:-1]) / 100 if value.endswith("%") else float(value)


def theme_tokens() -> dict[str, dict[str, str]]:
    """Each theme's `--site-rung-*` tokens, from the rule that sets the scale."""
    themes: dict[str, dict[str, str]] = {}
    for selector, declared in _blocks(SITE_CSS):
        if "--site-rung-base" not in declared:
            continue
        theme = "dark" if _is_dark(selector) else "light"
        if theme in themes:
            raise SystemExit(f"site.css sets the {theme} rung scale twice")
        themes[theme] = {
            name: value for name, value in declared.items() if name.startswith("--site-rung-")
        }
    if set(themes) != set(THEMES):
        raise SystemExit(f"site.css sets the rung scale for {sorted(themes)}, not both themes")
    return themes


def ladder_tokens() -> dict[str, dict[str, str]]:
    """Each ladder's `--rung-*` properties: the rule's own, then the ladder's."""
    rules = dict(_blocks(SITE_CSS))
    shared = rules.get(".site-rung-fill")
    if not shared:
        raise SystemExit("site.css has no .site-rung-fill rule")
    return {
        scale: shared | rules.get(f'.site-rung-fill[data-rung="{scale}"]', {})
        for scale in LADDERS
    }


def styled_levels() -> set[int]:
    """The levels `site.css` gives a fill of their own: 0, and each `data-level` rule."""
    levels = {0}
    for selector, declared in _blocks(SITE_CSS):
        match = re.fullmatch(r'\.site-rung-fill\[data-level="(\d+)"\]', selector)
        if match and declared.get("--rung-level") == match.group(1):
            levels.add(int(match.group(1)))
    return levels


def page_colours() -> dict[str, dict[str, Oklch]]:
    """The page's text and background in each theme, from kpress's neutral palette."""
    found: dict[str, dict[str, Oklch]] = {}
    for selector, declared in _blocks(kpress_static() / "css" / "style-tokens.css"):
        if "--kpress-doc-text" not in declared or "data-kpress-palette" in selector:
            continue
        theme = "dark" if _is_dark(selector) else "light"
        colours: dict[str, Oklch] = {}
        for role in ("text", "bg"):
            match = _OKLCH.fullmatch(declared[f"--kpress-doc-{role}"].strip())
            if not match:
                raise SystemExit(f"kpress's {theme} {role} colour is not an oklch() value")
            lightness, chroma, hue = (float(part) for part in match.groups())
            colours[role] = (lightness / 100, chroma, hue)
        found.setdefault(theme, colours)
    if set(found) != set(THEMES):
        raise SystemExit("kpress's style tokens do not state both themes' page colours")
    return found


def luminance(colour: Oklch) -> float:
    """WCAG relative luminance of an OkLCh colour, clipped to sRGB as a browser shows it."""
    red, green, blue = (min(1.0, max(0.0, channel)) for channel in _oklch_linear_rgb(*colour))
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast(first: Oklch, second: Oklch) -> float:
    """The WCAG 2 contrast ratio of two colours."""
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def hex_colour(colour: Oklch) -> str:
    """An OkLCh colour as the sRGB hex a browser shows it as, clipped to the gamut."""
    channels = (
        round(_linear_to_srgb(min(1.0, max(0.0, channel))) * 255)
        for channel in _oklch_linear_rgb(*colour)
    )
    return "#" + "".join(f"{channel:02x}" for channel in channels)


def fills() -> list[Fill]:
    """Every rung of every ladder in each theme, in the site's order, lowest level first."""
    themes = theme_tokens()
    ladders = ladder_tokens()
    pages = page_colours()
    levels = rubric_levels()
    report = []
    for theme in THEMES:
        tokens = themes[theme]

        def value(declared: str, tokens: dict[str, str] = tokens) -> float:
            reference = _VAR.fullmatch(declared.strip())
            return _number(tokens[reference.group(1)] if reference else declared)

        for scale in LADDERS:
            ladder = ladders[scale]
            hue = _number(ladder["--rung-hue"])
            for level, _meaning in sorted(levels[scale]):
                colour = (
                    value("var(--site-rung-base)") + level * value("var(--site-rung-step)"),
                    value(ladder["--rung-chroma-base"])
                    + level * value(ladder["--rung-chroma-step"]),
                    hue,
                )
                report.append(
                    Fill(
                        theme=theme,
                        rung=f"{scale}{level}",
                        lightness=colour[0],
                        chroma=colour[1],
                        hue=hue,
                        hex=hex_colour(colour),
                        in_gamut=colour[1] <= _maximum_chroma(colour[0], hue),
                        contrast=contrast(pages[theme]["text"], colour),
                    )
                )
    return report


def status_fills() -> list[Fill]:
    """Every status chip's fill in each theme, its word as the `rung`: the scale's
    lightness and chroma at the rule's `--rung-level`, its `--rung-chroma-boost` added to
    the chroma, at its `--rung-hue`."""
    themes = theme_tokens()
    pages = page_colours()
    rules = [
        (match.group(2), declared)
        for selectors, declared in _blocks(SITE_CSS)
        for selector in selectors.split(",")
        if (match := _STATUS_RULE.fullmatch(selector.strip()))
    ]
    if not rules:
        raise SystemExit("site.css has no status chip rule")
    report = []
    for theme in THEMES:
        tokens = themes[theme]
        for word, declared in rules:
            level = _number(declared["--rung-level"])
            hue = _number(declared["--rung-hue"])
            lightness = _number(tokens["--site-rung-base"])
            colour = (
                lightness + level * _number(tokens["--site-rung-step"]),
                _number(tokens["--site-rung-chroma-base"])
                + level * _number(tokens["--site-rung-chroma-step"])
                + _number(declared.get("--rung-chroma-boost", "0")),
                hue,
            )
            report.append(
                Fill(
                    theme=theme,
                    rung=word,
                    lightness=colour[0],
                    chroma=colour[1],
                    hue=hue,
                    hex=hex_colour(colour),
                    in_gamut=colour[1] <= _maximum_chroma(colour[0], hue),
                    contrast=contrast(pages[theme]["text"], colour),
                )
            )
    return report


def _theme_values(name: str) -> dict[str, str]:
    """A custom property's value in each theme: the dark theme's own, or the light one."""
    declared: dict[str, str] = {}
    for selector, tokens in _blocks(SITE_CSS):
        if name in tokens:
            declared.setdefault("dark" if _is_dark(selector) else "light", tokens[name])
    if "light" not in declared:
        raise SystemExit(f"site.css declares no {name}")
    return {theme: declared.get(theme, declared["light"]) for theme in THEMES}


def _parse_colour(value: str) -> Oklch:
    """An `oklch()` or sRGB hex value as OkLCh."""
    value = value.strip()
    if match := _OKLCH.fullmatch(value):
        lightness, chroma, hue = (float(part) for part in match.groups())
        return (lightness / 100, chroma, hue)
    if _HEX.fullmatch(value):
        return hex_oklch(value)
    raise SystemExit(f"site.css gives a colour this tool cannot read: {value}")


def _oklab(colour: Oklch) -> tuple[float, float, float]:
    lightness, chroma, hue = colour
    return (lightness, chroma * cos(radians(hue)), chroma * sin(radians(hue)))


def distance(first: Fill, second: Fill) -> float:
    """The OkLab distance of two fills, where about 0.02 is a just noticeable difference."""
    return hypot(
        *(
            a - b
            for a, b in zip(
                _oklab((first.lightness, first.chroma, first.hue)),
                _oklab((second.lightness, second.chroma, second.hue)),
                strict=True,
            )
        )
    )


def topic_fills() -> list[Fill]:
    """Every result-kind chip with its own fill in each theme, its key as the `rung`: a
    topic on the scale at its rule's `--rung-level` and `--rung-hue`, as `status_fills`
    reads a status, or a bound topic's ink mixed into the page background at the chip
    tint. A topic with no rule of its own keeps the plain chip and is not reported."""
    themes = theme_tokens()
    pages = page_colours()
    rules: dict[str, dict[str, str]] = {}
    for selectors, declared in _blocks(SITE_CSS):
        for selector in (part.strip() for part in selectors.split(",")):
            if selector.startswith(".site-chip"):
                for topic in _TOPIC.findall(selector):
                    rules.setdefault(topic, {}).update(declared)
    report = []
    for theme in THEMES:
        tokens = themes[theme]
        for topic in TOPICS:
            declared = rules.get(topic, {})
            if "--rung-level" in declared:
                level = _number(declared["--rung-level"])
                hue = _number(declared["--rung-hue"])
                colour = (
                    _number(tokens["--site-rung-base"])
                    + level * _number(tokens["--site-rung-step"]),
                    _number(tokens["--site-rung-chroma-base"])
                    + level * _number(tokens["--site-rung-chroma-step"])
                    + _number(declared.get("--rung-chroma-boost", "0")),
                    hue,
                )
            elif mix := _BOUND_MIX.fullmatch(declared.get("--site-chip-fill", "").strip()):
                ink = _oklab(_parse_colour(_theme_values(mix.group(1))[theme]))
                page = _oklab(pages[theme]["bg"])
                share = _number(_theme_values(mix.group(2))[theme])
                lightness, a, b = (
                    share * first + (1 - share) * second
                    for first, second in zip(ink, page, strict=True)
                )
                colour = (lightness, hypot(a, b), round(degrees(atan2(b, a)) % 360, 1))
            else:
                continue
            report.append(
                Fill(
                    theme=theme,
                    rung=topic,
                    lightness=colour[0],
                    chroma=colour[1],
                    hue=colour[2],
                    hex=hex_colour(colour),
                    in_gamut=colour[1] <= _maximum_chroma(colour[0], colour[2]),
                    contrast=contrast(pages[theme]["text"], colour),
                )
            )
    if not report:
        raise SystemExit("site.css gives no topic chip a fill of its own")
    return report


def news_topic_backgrounds() -> dict[str, Oklch]:
    """The shared neutral News topic surface in each theme."""
    return {
        theme: _parse_colour(value)
        for theme, value in _theme_values("--site-news-topic-bg").items()
    }


def news_topic_inks() -> list[Fill]:
    """Every News label's actual ink and contrast on its shared neutral background."""
    surfaces = news_topic_backgrounds()
    lightness = _theme_values("--site-news-topic-ink-lightness")
    chroma = _theme_values("--site-news-topic-ink-chroma")
    hues = {
        match[1]: _number(declared["--site-news-topic-hue"])
        for selector, declared in _blocks(SITE_CSS)
        if (match := re.fullmatch(r'\.site-chip\[data-news-topic="([a-z-]+)"\]', selector))
        and "--site-news-topic-hue" in declared
    }
    return [
        Fill(
            theme=theme,
            rung=topic,
            lightness=(value := _number(lightness[theme])),
            chroma=(saturation := _number(chroma[theme]) if topic in hues else 0),
            hue=(hue := hues.get(topic, 265)),
            hex=hex_colour((value, saturation, hue)),
            in_gamut=saturation <= _maximum_chroma(value, hue),
            contrast=contrast((value, saturation, hue), surfaces[theme]),
        )
        for theme in THEMES
        for topic in NEWS_TOPICS
    ]


def crowded(report: Sequence[Fill]) -> list[tuple[Fill, Fill, float]]:
    """Each topic fill closer than `DISTINCT` to another fill of `report` in its theme
    that means something else, or apart from one that shares its meaning, with their
    distance. `main` passes the statuses and the topics."""
    topics = {fill.rung for fill in report if fill.rung in TOPICS}
    found = []
    for first in report:
        if first.rung not in topics:
            continue
        for second in report:
            if second.theme != first.theme or second.rung == first.rung:
                continue
            if second.rung in topics and second.rung < first.rung:
                continue
            apart = distance(first, second)
            shared = frozenset({first.rung, second.rung}) in SHARED_FILLS
            if (apart > 1e-9) if shared else (apart < DISTINCT):
                found.append((first, second, apart))
    return found


def inks() -> list[Fill]:
    """Every ink in each theme, its token as the `rung` and its contrast against the
    page's background: the value a theme's rule declares, or the light one where the
    dark theme declares none."""
    pages = page_colours()
    declared: dict[str, dict[str, str]] = {}
    for selector, tokens in _blocks(SITE_CSS):
        theme = "dark" if _is_dark(selector) else "light"
        for name in INKS:
            if name in tokens:
                if name in declared.setdefault(theme, {}):
                    raise SystemExit(f"site.css declares {name} twice for the {theme} theme")
                declared[theme][name] = tokens[name]
    report = []
    for theme in THEMES:
        for name in INKS:
            written = declared.get(theme, {}).get(name) or declared.get("light", {}).get(name)
            match = _OKLCH.fullmatch((written or "").strip())
            if not match:
                raise SystemExit(f"site.css gives {name} no oklch() in the {theme} theme")
            lightness, chroma, hue = (float(part) for part in match.groups())
            colour = (lightness / 100, chroma, hue)
            report.append(
                Fill(
                    theme=theme,
                    rung=name,
                    lightness=colour[0],
                    chroma=chroma,
                    hue=hue,
                    hex=hex_colour(colour),
                    in_gamut=chroma <= _maximum_chroma(colour[0], hue),
                    contrast=contrast(colour, pages[theme]["bg"]),
                )
            )
    return report


def ink_table(report: Sequence[Fill], *, surface: str = "page") -> str:
    """The inks as the design document carries them: one row a token, a theme a pair of
    columns, the ink in OkLCh with its hex and its contrast against the page."""
    by_token: dict[str, dict[str, Fill]] = {}
    for ink in report:
        by_token.setdefault(ink.rung, {})[ink.theme] = ink
    lines = [
        f"| Ink | Light | Against the {surface} | Dark | Against the {surface} |",
        "| --- | --- | --- | --- | --- |",
    ]
    for token, themed in by_token.items():
        cells = [f"`{token}`"]
        for theme in THEMES:
            ink = themed[theme]
            cells += [f"`{ink.oklch}` `{ink.hex}`", f"{ink.contrast:.1f}:1"]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def news_topic_table(report: Sequence[Fill]) -> str:
    """News ink and its measured contrast on the common neutral surface."""
    return ink_table(report, surface="neutral surface").replace("| Ink |", "| News topic |", 1)


def markdown_table(report: Sequence[Fill], head: str = "Rung") -> str:
    """The scale as the design document carries it: one row a rung, a theme a pair of
    columns, the fill in OkLCh with its hex and the text's contrast on it."""
    by_rung: dict[str, dict[str, Fill]] = {}
    for fill in report:
        by_rung.setdefault(fill.rung, {})[fill.theme] = fill
    lines = [
        f"| {head} | Light fill | Text contrast | Dark fill | Text contrast |",
        "| --- | --- | --- | --- | --- |",
    ]
    for rung, themed in by_rung.items():
        cells = [f"`{rung}`"]
        for theme in THEMES:
            fill = themed[theme]
            cells += [f"`{fill.oklch}` `{fill.hex}`", f"{fill.contrast:.1f}:1"]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    if argv:
        raise SystemExit(__doc__)
    report = fills()
    statuses = status_fills()
    topics = topic_fills()
    drawn = inks()
    news = news_topic_inks()
    print(markdown_table(report))
    print()
    print(markdown_table(statuses, "Status"))
    print()
    print(markdown_table(topics, "Topic"))
    print()
    print(ink_table(drawn))
    print()
    print(news_topic_table(news))
    report += statuses + topics + news
    pages = page_colours()
    for theme in THEMES:
        print(f"{theme}: text on the page background {contrast(*pages[theme].values()):.1f}:1")
    failed = [fill for fill in report if not fill.in_gamut or fill.contrast < MINIMUM_CONTRAST]
    failed += [ink for ink in drawn if not ink.in_gamut or ink.contrast < INKS[ink.rung]]
    for fill in failed:
        print(
            f"{fill.theme} {fill.rung}: {fill.oklch} "
            f"{'in' if fill.in_gamut else 'out of'} gamut, {fill.contrast:.2f}:1",
            file=sys.stderr,
        )
    close = crowded(statuses + topics)
    for first, second, apart in close:
        print(
            f"{first.theme} {first.rung} and {second.rung}: {apart:.3f} apart in OkLab",
            file=sys.stderr,
        )
    return 1 if failed or close else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
