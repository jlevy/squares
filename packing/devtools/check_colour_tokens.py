#!/usr/bin/env python3
"""Every colour in the stylesheets the site serves is a named token.

A colour is set once, as a custom property (`--site-significance`, `--site-shadow`,
`--kpress-doc-accent`), and every rule that paints with it says `var(...)`. So a colour
can be tried and changed in one place, and a dark theme or a print sheet redefines the
token rather than every rule that uses it (the owner, 2026-10-03, `think-zhlc`).

The rule this holds, for every declaration that is not itself a custom property, once
each `var(...)` in its value is set aside:

- no hex colour, `#17202a`;
- no colour function that names a number of its own, `oklch(52% 0.19 25)` or a mix's
  `color-mix(in oklch, var(--a) 16%, var(--b))`: a function built only of tokens,
  `oklch(calc(var(--base) + var(--level) * var(--step)) ...)`, is the token's own
  arithmetic and passes, and a mix's ratio is a token too;
- no named colour, `white` or `teal`, in a property that paints, though `transparent`,
  `currentcolor` and the system colours a forced-colours sheet must use are allowed;
- and every token a property that paints names is declared, in these stylesheets or
  KPress's: a misspelt one paints nothing, and nothing else would say so.

A `var()`'s fallback is held to the same rule, since it paints wherever its token is
unset: `var(--site-ink, #000)` names a colour of its own. Every rule's own declarations
are read, those of a rule that also holds a nested rule (an `@page` beside its margin
boxes) among them. A token is counted declared if any of these stylesheets or KPress's
declares it, not only those a given page loads; that a page's own sheets declare every
token it paints with is `think-wviw`'s.

A custom property may hold any value: that is what a token is. A mix of other colours
stays in the rule that uses it, with its ratio a token, since a token resolves where it
is declared and a mix of the page's colours declared at the root would miss the dark
theme's, which are set lower down.

The workbench's stylesheet is held to a wider contract of its own
(`packages/workbench/tools/design-contract.ts`); this one is about colour and covers the
site's and the papers' stylesheets.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_colour_tokens
"""

from __future__ import annotations

import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
#: The stylesheets the site and its papers serve.
STYLESHEETS = tuple(sorted((ROOT / "devtools" / "templates").glob("*.css")))

_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
_HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
_FUNCTION = re.compile(
    r"\b(rgba?|hsla?|hwb|lab|lch|oklab|oklch|color|color-mix)\(", re.IGNORECASE
)
_DIGIT = re.compile(r"\d")
_WORD = re.compile(r"(?<![\w-])[a-zA-Z]+(?![\w-])")
#: The properties that paint, where a word may be a named colour.
_PAINTS = re.compile(
    r"^(?:color|background(?:-color|-image)?|border(?:-[a-z]+)*?(?:-color)?|"
    r"outline(?:-color)?|fill|stroke|accent-color|caret-color|text-decoration(?:-color)?|"
    r"column-rule(?:-color)?|box-shadow|text-shadow|scrollbar-color|stop-color|"
    r"flood-color|lighting-color|filter|backdrop-filter|-webkit-text-fill-color|"
    r"-webkit-text-stroke(?:-color)?|mask(?:-image)?)$"
)
_NAMED = """aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue
    blueviolet brown burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk
    crimson cyan darkblue darkcyan darkgoldenrod darkgray darkgreen darkgrey darkkhaki
    darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen
    darkslateblue darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue
    dimgray dimgrey dodgerblue firebrick floralwhite forestgreen fuchsia gainsboro
    ghostwhite gold goldenrod gray green greenyellow grey honeydew hotpink indianred indigo
    ivory khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral
    lightcyan lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon
    lightseagreen lightskyblue lightslategray lightslategrey lightsteelblue lightyellow lime
    limegreen linen magenta maroon mediumaquamarine mediumblue mediumorchid mediumpurple
    mediumseagreen mediumslateblue mediumspringgreen mediumturquoise mediumvioletred
    midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive olivedrab
    orange orangered orchid palegoldenrod palegreen paleturquoise palevioletred papayawhip
    peachpuff peru pink plum powderblue purple rebeccapurple red rosybrown royalblue
    saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue slateblue
    slategray slategrey snow springgreen steelblue tan teal thistle tomato turquoise violet
    wheat white whitesmoke yellow yellowgreen"""
#: CSS's named colours: a word that paints a colour of its own.
NAMED_COLOURS = frozenset(_NAMED.split())


#: The declarations that keep a colour of their own, each by stylesheet, selector and
#: property, with the reason. A check that finds an entry no longer needed fails, so the
#: list can only shrink.
ALLOWED: dict[tuple[str, str, str], str] = {
    ("paper-publication.css", "@bottom-left", "color"): (
        "a printed page's margin box, which stands outside the document tree, so a "
        "custom property set on the root is not relied on there: its folio's ink is "
        "written where it is drawn"
    ),
    ("paper-publication.css", "@bottom-right", "color"): (
        "a printed page's margin box, as `@bottom-left`"
    ),
}


@dataclass(frozen=True)
class Finding:
    """A declaration that paints with a colour of its own."""

    path: Path
    line: int
    selector: str
    declaration: str
    why: str

    def __str__(self) -> str:
        where = self.path.relative_to(ROOT.parent) if self.path.is_absolute() else self.path
        return f"{where}:{self.line}: {self.selector} {{ {self.declaration} }}: {self.why}"


def _blank_comments(css: str) -> str:
    """The stylesheet with each comment blanked, its newlines kept, so lines still count."""
    return _COMMENT.sub(lambda match: re.sub(r"[^\n]", " ", match.group()), css)


def _closing(text: str, opening: int) -> int:
    """The index just past the parenthesis that closes the one at `opening`."""
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == "(":
            depth += 1
        elif text[index] == ")":
            depth -= 1
            if depth == 0:
                return index + 1
    return len(text)


def _fallback(inner: str) -> str:
    """What a `var()` holds after its token: the fallback past its first top-level comma,
    or nothing."""
    depth = 0
    for index, char in enumerate(inner):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            return inner[index + 1 :]
    return ""


def without_tokens(value: str) -> str:
    """A value with every `var(...)`'s token set aside and its fallback kept, itself
    without tokens, since a fallback paints wherever its token is unset."""
    while (start := value.find("var(")) >= 0:
        end = _closing(value, start + 3)
        fallback = without_tokens(_fallback(value[start + 4 : end - 1]))
        value = f"{value[:start]} {fallback} {value[end:]}"
    return value


def colour_problems(property_name: str, value: str) -> list[str]:
    """Why a declaration paints with a colour of its own, or nothing."""
    if property_name.startswith("--"):
        return []
    rest = without_tokens(value)
    problems = [f"hex colour {found}" for found in _HEX.findall(rest)]
    for match in _FUNCTION.finditer(rest):
        call = rest[match.start() : _closing(rest, match.end() - 1)]
        if _DIGIT.search(call):
            problems.append(
                f"{match.group(1)}() names a value of its own: {' '.join(call.split())}"
            )
    if _PAINTS.match(property_name.lower()):
        problems += [
            f"named colour {word}"
            for word in _WORD.findall(rest)
            if word.lower() in NAMED_COLOURS
        ]
    return problems


def _blank(text: str, start: int, end: int) -> str:
    """`text` with `start` to `end` blanked, its newlines kept."""
    return text[:start] + re.sub(r"[^\n]", " ", text[start:end]) + text[end:]


def rule_blocks(text: str) -> list[tuple[str, int, str]]:
    """Every rule of a stylesheet, outer and nested: its selector or at-rule prelude, where
    its body starts, and the body with each rule nested in it blanked, prelude and all,
    so what is left is the rule's own declarations, at their own offsets."""
    blocks: list[tuple[str, int, str]] = []
    opened: list[tuple[str, int]] = []
    for index, char in enumerate(text):
        if char == "{":
            prelude = max(text.rfind(mark, 0, index) for mark in ";{}") + 1
            opened.append((" ".join(text[prelude:index].split()), index + 1))
        elif char == "}" and opened:
            selector, body_start = opened.pop()
            body = text[body_start:index]
            depth = 0
            nested_from = 0
            for at, inner in enumerate(body):
                if inner == "{":
                    if depth == 0:
                        nested_from = max(body.rfind(mark, 0, at) for mark in ";}") + 1
                    depth += 1
                elif inner == "}":
                    depth -= 1
                    if depth == 0:
                        body = _blank(body, nested_from, at + 1)
            blocks.append((selector or "(top level)", body_start, body))
    return blocks


def stylesheet_findings(css: str, path: Path = Path("<css>")) -> list[Finding]:
    """Every declaration in `css` that paints with a colour of its own."""
    text = _blank_comments(css)
    findings: list[Finding] = []
    for selector, body_start, body in rule_blocks(text):
        offset = 0
        for piece in body.split(";"):
            if ":" in piece:
                name, _, value = piece.partition(":")
                name = name.strip()
                if name and not name.startswith("@"):
                    at = body_start + offset + len(piece) - len(piece.lstrip())
                    line = text.count("\n", 0, at) + 1
                    findings.extend(
                        Finding(path, line, selector, f"{name}: {' '.join(value.split())}", why)
                        for why in colour_problems(name, value)
                    )
            offset += len(piece) + 1
    return findings


_VAR_NAME = re.compile(r"var\(\s*(--[\w-]+)")
_CUSTOM = re.compile(r"(--[\w-]+)\s*:")


def kpress_stylesheets() -> list[Path]:
    """KPress's own stylesheets, which declare the `--kpress-*` tokens the site paints with."""
    from devtools.render_n11_lower_bounds_explainer import kpress_static  # noqa: PLC0415

    return sorted((kpress_static() / "css").glob("*.css"))


def undeclared_paint_tokens(
    paths: Iterable[Path] = STYLESHEETS, declaring: Iterable[Path] = ()
) -> list[str]:
    """The tokens a rule paints with that no stylesheet declares, in `paths` or the
    `declaring` ones beside them (KPress's): a misspelt colour token paints nothing, with
    no error anywhere."""
    sheets = list(paths)
    every = [*sheets, *declaring]
    texts = [_blank_comments(path.read_text(encoding="utf-8")) for path in every]
    declared = {name for text in texts for name in _CUSTOM.findall(text)}
    painted: set[str] = set()
    for text in texts[: len(sheets)]:
        for _, _, body in rule_blocks(text):
            for piece in body.split(";"):
                name, _, value = piece.partition(":")
                if _PAINTS.match(name.strip().lower()):
                    painted.update(_VAR_NAME.findall(value))
    return sorted(painted - declared)


def _key(finding: Finding) -> tuple[str, str, str]:
    return (finding.path.name, finding.selector, finding.declaration.split(":", 1)[0])


def findings(
    paths: Iterable[Path] = STYLESHEETS, allowed: Mapping[tuple[str, str, str], str] = ALLOWED
) -> tuple[list[Finding], list[tuple[str, str, str]]]:
    """Every such declaration in the stylesheets the site serves that `allowed` does not
    name, and the entries of `allowed` that named nothing."""
    found = [
        finding
        for path in paths
        for finding in stylesheet_findings(path.read_text(encoding="utf-8"), path)
    ]
    used = {_key(finding) for finding in found}
    return (
        [finding for finding in found if _key(finding) not in allowed],
        [entry for entry in allowed if entry not in used],
    )


def main(argv: Sequence[str] | None = None) -> int:
    if argv:
        raise SystemExit(__doc__)
    found, stale = findings()
    undeclared = undeclared_paint_tokens(declaring=kpress_stylesheets())
    for finding in found:
        print(finding)
    for entry in stale:
        print(f"ALLOWED names {entry}, which no longer paints with a colour of its own")
    for name in undeclared:
        print(f"{name} paints, and no stylesheet declares it")
    if found or stale or undeclared:
        print(
            f"{len(found)} declarations paint with a colour that is not a token; "
            f"{len(stale)} allowed entries are stale; {len(undeclared)} tokens undeclared"
        )
        return 1
    print(
        f"{len(STYLESHEETS)} stylesheets: every colour is a named token, but for "
        f"{len(ALLOWED)} declarations allowed with a reason"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
