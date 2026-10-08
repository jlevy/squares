#!/usr/bin/env python3
"""Render the frontier atlas page: one table row for every case `n = 1…324`.

Every row is read from the case's softschema record, the `packing:` envelope of
`frontier/n-NNN.md` under the enforced `packing.squares:SquarePackingCase/v2` contract,
and each file is validated against its declared schema before a cell is written, so an
invalid record fails the render rather than rendering a blank. Nothing is read from
`STATUS.md` and nothing is typed by hand: the formatting is `render_research_tables`'s
(`latex`, `compact_bound`'s exact-form rule), and "shown once" is
`bounds_agree_at_declared_precision`, the test `STATUS.md` applies.

The page is one of `render_overview.PAGES`; render it with the rest of the site:

    uv run --frozen --all-extras --group dev python -m devtools.render_overview --output DIR
"""

from __future__ import annotations

import html
import re
from collections.abc import Callable, Iterable, Mapping
from decimal import Decimal
from functools import cache
from pathlib import Path
from typing import Any, cast

from devtools import render_research_tables as tables
from devtools.build_bound_citations import RECENT_SINCE, corrects_tag
from devtools.build_bound_citations import RECORD as BOUND_CITATIONS
from devtools.render_recent_results import RecentCounts, recent_counts, recent_rows
from devtools.repo_links import repo_url
from devtools.validate_schemas import check as check_record
from sqpack.assurance import bounds_agree_at_declared_precision

PACKING = Path(__file__).resolve().parents[1]
TEMPLATES = PACKING / "devtools" / "templates"
FRONTIER_ARTICLE = TEMPLATES / "frontier-article.md"
RENDERINGS = PACKING / "atlas" / "known-best" / "rendering"
#: The regularized views' index and their drawings, by the house renderer at the house
#: settings (`devtools.render_regularized_atlas`), which the homepage's atlas offers as
#: its second layer and reduces to tiles with `packing_svg(root=)`.
REGULARIZED_INDEX = PACKING / "atlas" / "known-best" / "regularized" / "index.json"
REGULARIZED_RENDERINGS = REGULARIZED_INDEX.parent / "rendering"
TABLE_SCRIPT = PACKING / "devtools" / "overview" / "table.js"
#: The two repository documents the page's prose links: the literature archive's README
#: and the evidence inventory.
ARCHIVE_README = "packing/resources/README.md"
EVIDENCE_INVENTORY = "packing/frontier/INVENTORY.md"

#: Every file this page reads beyond the site shell's own inputs. The survey's counts
#: are `render_recent_results`', which reads the register and the bibliography beside
#: the case records.
FRONTIER_INPUTS: tuple[Path, ...] = (
    Path(__file__).resolve(),
    FRONTIER_ARTICLE,
    TABLE_SCRIPT,
    PACKING / "frontier",
    RENDERINGS,
    BOUND_CITATIONS,
    PACKING / "resources" / "bibliography.yaml",
    PACKING / "devtools" / "render_research_tables.py",
    PACKING / "devtools" / "render_recent_results.py",
    PACKING / "devtools" / "build_bound_citations.py",
    PACKING / "devtools" / "validate_schemas.py",
    PACKING / "src" / "sqpack" / "assurance.py",
)


def since_prose() -> str:
    """`RECENT_SINCE`, the first day of this project's work, as the site's prose writes a
    date: 22 August 2026. The one place the day is written out, so the Frontier page's
    star sentence and the results tables' star legend read the same date."""
    return f"{RECENT_SINCE.day} {RECENT_SINCE:%B %Y}"


def survey_counts(counts: RecentCounts) -> str:
    """The survey's four counts as one Markdown sentence, for the Frontier page's Recent
    results paragraph, which has just said what the star marks and the date it runs
    from: of the first hundred cases, how many have a recent lower bound in either lane,
    how many of those a recent verified one, which are the starred cases, and of those
    how many are this project's and how many new exact values
    (`render_recent_results.recent_counts`)."""
    return (
        f"Of the first hundred cases, {counts.cases} have a lower bound published or proved "
        f"since then, reported or verified; {counts.verified} of those have a recent "
        f"verified one, the starred cases; {counts.ours} of the {counts.verified} are this "
        f"project\u2019s, and {counts.exact} are new exact values."
    )


#: The digits a decimal cell shows before it is cut, with an ellipsis rather than rounded:
#: a rounded bound can read as a different bound.
DECIMAL_PLACES = 8
#: An exact gap longer than this, in TeX, is shown as its decimal: a difference of two
#: long closed forms is exact and unreadable.
GAP_SHOWN = 44
#: A rational gap whose numerator or denominator has more digits than this is shown as
#: its decimal too: `327174680178947/1000000000000000`, Couzo's ceiling at n = 102 less
#: the linear 257/25, is short in TeX and still too wide to read, and widened the column
#: past the table's track at 1280 pixels; n = 68's `4512425581603/15625000000000` reads
#: no better.
GAP_DIGITS = 8
#: A closed form longer than this, in TeX, is shown as its decimal. The longest structured
#: form runs to 45 characters; a 30-digit rational certificate value does not read as one.
VALUE_SHOWN = 56


def math_html(tex: str) -> str:
    """Inline math in kpress's own markup, which the page's KaTeX scripts enhance.

    kpress turns `$…$` into math only in Markdown text, and a table here is an HTML
    block, so the cell asks kpress's renderer for the same span it would have written:
    the TeX for KaTeX and server MathML as the no-script fallback.
    """
    from kpress.format.markdown import (  # noqa: PLC0415
        _render_math,  # pyright: ignore[reportPrivateUsage]
    )

    return _render_math(tex, display="inline", math="auto", env={})


def decimal_text(value: object) -> str:
    """A record's decimal, cut rather than rounded after `DECIMAL_PLACES`.

    A whole number the record writes as `3.0` prints as `3`, as the best-known side
    beside it does.
    """
    text = str(value)
    whole, _, fraction = text.partition(".")
    if fraction and not fraction.strip("0"):
        return whole
    if len(fraction) <= DECIMAL_PLACES:
        return text
    return f"{whole}.{fraction[:DECIMAL_PLACES]}…"


def is_integer(text: str) -> bool:
    return re.fullmatch(r"\d+", text) is not None


def cell_tex(tex: str) -> str:
    """A value's TeX as a table cell sets it: a lone fraction at full size.

    Inline math sets `\\frac` in text style, where `31/8` reads at a subscript's size;
    a fraction that is the whole value is the one a reader is looking for, so it gets
    `\\dfrac`. A fraction inside a sum keeps text style and the row its height.
    """
    if re.fullmatch(r"\\frac\{\d+\}\{\d+\}", tex):
        return "\\dfrac" + tex.removeprefix("\\frac")
    return tex


def exact_decimal(value: Any) -> tuple[str, bool]:
    """An exact value's decimal as a cell prints it, and whether that is the whole of it.

    The digits come from the exact value and from nothing looser. A rational is divided
    in whole numbers, so its decimal either ends within `DECIMAL_PLACES` and is printed
    in full, or is cut there. Anything else is evaluated by sympy to 30 significant
    digits and cut by `decimal_text`, the rule every decimal on the page follows. A cut
    drops digits and never rounds, so the digits dropped must not be all nines or all
    zeros as far as they are known: there the last digit kept would depend on digits
    that were never computed, and the render stops instead of printing a guess.
    """
    import sympy  # noqa: PLC0415

    if value.is_Rational:
        scaled, left = divmod(abs(int(value.p)) * 10**DECIMAL_PLACES, int(value.q))
        whole, fraction = divmod(scaled, 10**DECIMAL_PLACES)
        sign = "-" if value.p < 0 else ""
        digits = f"{fraction:0{DECIMAL_PLACES}d}"
        if left:
            return f"{sign}{whole}.{digits}…", False
        return f"{sign}{whole}.{digits}".rstrip("0").rstrip("."), True
    numeric = f"{Decimal(str(sympy.N(value, 30))):f}"
    dropped = numeric.partition(".")[2][DECIMAL_PLACES:-2]
    if not dropped.strip("9") or not dropped.strip("0"):
        raise SystemExit(f"{value} is too close to a {DECIMAL_PLACES}-place decimal to cut")
    return decimal_text(numeric), False


def approx_html(value: Any) -> str:
    """The decimal a closed form is set over, quiet, on a line of its own under it:
    `= 4.695` where the decimal is the value, `≈ 3.96861554…` where it is cut."""
    text, whole = exact_decimal(value)
    return f'<span class="site-approx">{"=" if whole else "≈"} {text}</span>'


def closed_form_tex(exact: str) -> str | None:
    """A closed form that fits a table cell, with one rule for both display lines."""
    if not exact or tables.ROOT_FORM.fullmatch(exact) or is_integer(exact):
        return None
    tex = tables.latex(exact)
    if len(tex) > VALUE_SHOWN:
        return None
    value = exact_value(exact)
    if value.is_Rational and any(
        len(str(abs(part))) > GAP_DIGITS for part in (value.p, value.q)
    ):
        return None
    return tex


def value_html(bound: dict[str, Any]) -> str:
    """A bound as a reader should see it: integers plain, readable closed forms as math."""
    exact = bound.get("exact_form")
    if isinstance(exact, str) and exact:
        if is_integer(exact):
            return html.escape(exact)
        if (tex := closed_form_tex(exact)) is not None:
            return math_html(cell_tex(tex))
    title = (
        f' title="{html.escape(exact)}"'
        if isinstance(exact, str) and re.fullmatch(r"-?\d+/\d+", exact)
        else ""
    )
    return (
        f'<span class="site-decimal"{title}>{html.escape(decimal_text(bound["value"]))}</span>'
    )


def bound_approx_html(bound: dict[str, Any]) -> str:
    """The decimal under a displayed closed form, read from that exact form."""
    exact = bound.get("exact_form")
    if not isinstance(exact, str) or closed_form_tex(exact) is None:
        return ""
    value = exact_value(exact)
    return "" if value.is_Integer else approx_html(value)


def credit(names: Iterable[str] | None, year: object) -> str:
    who = ", ".join(names or [])
    when = str(year) if year else ""
    return html.escape(" ".join(part for part in (who, when) if part))


@cache
def exact_value(form: str) -> Any:
    """A sympy value for an exact form, or `None` for a polynomial root."""
    import sympy  # noqa: PLC0415
    from sympy.parsing.sympy_parser import (  # noqa: PLC0415
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )

    if tables.ROOT_FORM.fullmatch(form):
        return None
    return parse_expr(
        form,
        transformations=(*standard_transformations, implicit_multiplication_application),
        local_dict={"sqrt": sympy.sqrt, "floor": sympy.floor},
    )


def gap(case: dict[str, Any]) -> tuple[str, str]:
    """Verified upper minus verified lower: `(cell HTML, decimal for sorting)`.

    Exact where both bounds are closed forms and the difference is short enough to read
    in a cell, with its decimal beneath unless it is a whole number; otherwise the
    decimal difference, cut like every other decimal here. Both bounds written as the
    same exact form -- one polynomial root, as for n = 11 since T-060 -- are one number,
    so the gap is zero without evaluating the root.
    """
    import sympy  # noqa: PLC0415

    upper, lower = case["verified_upper_bound"], case["verified_lower_bound"]
    if upper.get("exact_form") and upper["exact_form"] == lower.get("exact_form"):
        return "0", "0"
    upper_exact = exact_value(upper["exact_form"]) if upper.get("exact_form") else None
    lower_exact = exact_value(lower["exact_form"]) if lower.get("exact_form") else None
    if upper_exact is not None and lower_exact is not None:
        difference = cast("Any", sympy.radsimp(sympy.expand(upper_exact - lower_exact)))
        numeric = Decimal(str(sympy.N(difference, 30)))
        sort_value = "0" if numeric == 0 else f"{numeric:.30f}"
        tex = sympy.latex(difference, order="rev-lex")
        if difference.is_Integer:
            return html.escape(str(difference)), sort_value
        long_rational = difference.is_Rational and any(
            len(str(abs(part))) > GAP_DIGITS for part in (difference.p, difference.q)
        )
        if len(tex) <= GAP_SHOWN and not long_rational:
            return math_html(cell_tex(tex)) + approx_html(difference), sort_value
        return f'<span class="site-decimal">{decimal_text(numeric)}</span>', sort_value
    numeric = Decimal(str(upper["value"])) - Decimal(str(lower["value"]))
    return (
        f'<span class="site-decimal">{html.escape(decimal_text(numeric))}</span>',
        str(numeric),
    )


@cache
def evidence_lines() -> dict[str, int]:
    """Each evidence id's line in `evidence.yaml`, for a link to the entry itself."""
    lines = (tables.FRONTIER / "evidence.yaml").read_text(encoding="utf-8").splitlines()
    found = {}
    for number, line in enumerate(lines, start=1):
        match = re.fullmatch(r"\s*- id: (\S+)", line)
        if match:
            found[match.group(1)] = number
    return found


def evidence_links(refs: Iterable[str]) -> str:
    """Each evidence id once, as code linking to its entry in `evidence.yaml`, with commas
    between. A name and the comma after it are one `.site-name` box, so a line breaks
    between names and never on a hyphen inside one (`site.css`, Words stay whole).

    The link is scheme-relative (`//github.com/...`): the same entry, opened in the same
    tab. The frontier page carries one of these per evidence id per row, about 1,600 in
    all, and the absolute form, which kpress decorates with `target` and `rel`, cost 47
    bytes more each; that difference is what took the page over its 4 MiB ceiling on
    2026-10-02, when Karakuş's bound joined the verified lane of 254 rows.
    """
    base = repo_url(tables.FRONTIER / "evidence.yaml").removeprefix("https:")
    lines = evidence_lines()
    links = []
    for ref in dict.fromkeys(refs):
        if ref not in lines:
            raise SystemExit(f"evidence id {ref} is not in evidence.yaml")
        links.append(f'<a href="{base}#L{lines[ref]}"><code>{html.escape(ref)}</code></a>')
    return " ".join(
        f'<span class="site-name">{link}{"," if index < len(links) else ""}</span>'
        for index, link in enumerate(links, start=1)
    )


def thumbnail_svg(n: int) -> str:
    """The case's cached 1000-unit SVG, in a reserved 50-pixel square image.

    The drawing lives at its declared atlas address and can be cached across pages.
    The table cell sizes the image without embedding another copy of its geometry.
    """

    return drawing_img(n, size=50)


def packing_svg(
    n: int,
    *,
    units: int = 100,
    ink: str = "currentColor",
    paper: str = "none",
    frame_px: int | None = None,
    root: Path = RENDERINGS,
) -> str:
    """Case `n`'s atlas drawing as a bare `<svg>`: the frame and each square's outline at
    whole units of a `units`-wide frame, drawn in `ink` on `paper`.

    The drawing is read from `root`: the house renderings, or another set the house
    renderer drew, as the regularized views are (`REGULARIZED_RENDERINGS`), so one code
    reduces both and a tile of either is the same kind of picture.

    A table cell needs 100 units; a drawing shown large needs more, or the rounding shows
    as uneven gaps. A drawing used outside the page, where `currentColor` means nothing,
    names its ink. An icon drawn `frame_px` pixels square (the site's logo and favicon)
    gets a frame exactly one of those pixels wide, its outer edge on the drawing's edge,
    so the container reads as a square at icon size and lands on the pixel grid, and
    its squares' outlines half a pixel, so each square stays distinct.
    """
    source = (root / f"n-{n:03d}.svg").read_text(encoding="utf-8")
    frame = re.search(
        r'<rect data-feature="container-outline" x="([\d.]+)" y="([\d.]+)" '
        r'width="([\d.]+)" height="([\d.]+)"',
        source,
    )
    if frame is None:
        raise SystemExit(f"n-{n:03d}.svg has no container outline")
    x0, y0, width, _ = (Decimal(part) for part in frame.groups())
    scale = Decimal(units) / width
    paths: dict[str, list[str]] = {}
    squares = re.findall(
        r'<polygon data-feature="square-fill"[^>]*? points="([^"]+)" fill="(#[0-9a-f]{6})"',
        source,
    )
    if len(squares) != n:
        raise SystemExit(f"n-{n:03d}.svg draws {len(squares)} squares, not {n}")
    for points, fill in squares:
        corners = [
            (round((Decimal(x) - x0) * scale), round((Decimal(y) - y0) * scale))
            for x, y in (pair.split(",") for pair in points.split())
        ]
        paths.setdefault(fill, []).append(_square_path(corners))
    body = "".join(
        f'<path fill="{fill}" d="{"".join(parts)}"/>' for fill, parts in sorted(paths.items())
    )
    unit = Decimal(units) / 100
    box = f"{-unit:g} {-unit:g} {units + 2 * unit:g} {units + 2 * unit:g}"
    frame_width = (Decimal("1.2") * unit).normalize()
    crisp = ""
    line_width = (Decimal("0.6") * unit).normalize()
    if frame_px is not None:
        # One pixel of a `frame_px`-pixel drawing whose box is the frame plus half its
        # stroke on each side: (units + w) / frame_px = w.
        pixel = Decimal(units) / (frame_px - 1)
        half = pixel / 2
        box = f"{-half:.4f} {-half:.4f} {units + pixel:.4f} {units + pixel:.4f}"
        frame_width = pixel.quantize(Decimal("0.0001"))
        crisp = ' shape-rendering="crispEdges"'
        # At icon size the page's hairline all but vanishes, so the squares' outlines
        # take half a pixel: one device pixel on a 2x screen, and still lighter than
        # the frame.
        line_width = (pixel / 2).quantize(Decimal("0.0001"))
    return (
        f'<svg viewBox="{box}" aria-hidden="true" focusable="false">'
        f'<rect x="0" y="0" width="{units}" height="{units}" fill="{paper}" '
        f'stroke="{ink}" stroke-width="{frame_width:f}"{crisp}/><g stroke="{ink}" '
        f'stroke-width="{line_width:f}" stroke-linejoin="round">{body}</g></svg>'
    )


def drawing_path(n: int, *, regularized: bool = False) -> str:
    """Stable address of a compact standalone atlas drawing."""
    return f"atlas/{'regularized' if regularized else 'house'}/n-{n}.svg"


def drawing_img(n: int, *, regularized: bool = False, size: int = 100) -> str:
    """A drawing with a reserved square box; tiles use a deliberate white canvas."""
    return (
        f'<img src="{drawing_path(n, regularized=regularized)}" width="{size}" '
        f'height="{size}" loading="lazy" decoding="async" alt="Packing of {n} unit squares">'
    )


def drawing_paths() -> tuple[str, ...]:
    """Published drawing declarations without rendering their contents."""
    return tuple(
        drawing_path(int(path.stem.split("-")[1]), regularized=regularized)
        for regularized, root in ((False, RENDERINGS), (True, REGULARIZED_RENDERINGS))
        for path in sorted(root.glob("n-*.svg"))
    )


@cache
def drawing_files() -> dict[str, bytes]:
    """Compact standalone SVG files, usable by images and directly by a browser."""
    files = {}
    for regularized, root in ((False, RENDERINGS), (True, REGULARIZED_RENDERINGS)):
        for path in sorted(root.glob("n-*.svg")):
            n = int(path.stem.split("-")[1])
            svg = packing_svg(n, units=1000, root=root, ink="#17202a", paper="#ffffff")
            svg = svg.replace(
                "<svg ",
                '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" ',
                1,
            )
            files[drawing_path(n, regularized=regularized)] = svg.encode("utf-8")
    return files


def _square_path(corners: list[tuple[int, int]]) -> str:
    """One square as a closed path in whole units, relative after its first corner."""
    (x, y), *rest = corners
    steps = [f"M{x} {y}"]
    for next_x, next_y in rest:
        dx, dy = next_x - x, next_y - y
        if dy == 0:
            steps.append(f"h{dx}")
        elif dx == 0:
            steps.append(f"v{dy}")
        else:
            steps.append(f"l{dx}{'' if dy < 0 else ' '}{dy}")
        x, y = next_x, next_y
    return "".join(steps) + "z"


def frontier_cases() -> list[dict[str, Any]]:
    """Every case, each validated against its declared contract before it is read."""
    paths = sorted(tables.FRONTIER.glob("n-*.md"))
    for path in paths:
        errors = check_record(path)
        if errors:
            raise SystemExit(f"{path.name} is not a valid case record: {'; '.join(errors[:3])}")
    cases = tables.load_cases()
    names = [f"n-{case['n']:03d}.md" for case in cases]
    if names != [path.name for path in paths]:
        raise SystemExit("frontier case numbers do not match their file names")
    return cases


def lower_citations() -> dict[int, dict[str, Any] | None]:
    """Each case's verified lower bound's citation, as the committed record states it."""
    import json  # noqa: PLC0415

    entries = json.loads(BOUND_CITATIONS.read_text(encoding="utf-8"))["citations"]["entries"]
    return {entry["n"]: entry["lower"] for entry in entries}


def recent_lower_bounds() -> dict[int, bool]:
    """Whether each case's verified lower bound is recent, as the atlas figure stars it."""
    return {n: bool(lower and lower["recent"]) for n, lower in lower_citations().items()}


def corrected_lower_bounds() -> dict[int, dict[str, str]]:
    """The published work each case's verified lower bound corrects, where it corrects
    one: its bibliography key, its short citation and the register's record of it."""
    return {
        n: lower["corrects"]
        for n, lower in lower_citations().items()
        if lower and lower["corrects"]
    }


def corrections_prose() -> str:
    """The sentence that says once what the tag beside a star means, linking the result it
    names, for the Recent results paragraph (`{{CORRECTIONS}}`): the rows repeat the tag
    without a link, and the page states the reason the corrected work failed once, in the
    register's own words (`corrects.what` in `frontier/results.yaml`)."""
    from collections import Counter  # noqa: PLC0415

    from devtools.overview_sections import result_url  # noqa: PLC0415
    from sqpack.yamlio import safe_load  # noqa: PLC0415

    corrected = Counter(
        (corrects["credit"], corrects["result"])
        for corrects in corrected_lower_bounds().values()
    )
    register = safe_load((PACKING / "frontier" / "results.yaml").read_text(encoding="utf-8"))
    # The register's words, set as the page's prose sets an apostrophe.
    what = {
        str(record["corrects"]["result"]): " ".join(
            str(record["corrects"]["what"]).replace("'", "\u2019").split()
        )
        for record in register["results"]
        if record.get("corrects")
    }
    return " ".join(
        f"Beside {count} of the stars, *corrects {credit}* says the bound stands in for a "
        f"published result found unsound, the register\u2019s [{result}]"
        f"({result_url(result)}): {what[result]}."
        for (credit, result), count in sorted(corrected.items())
    )


def corrects_html(corrects: Mapping[str, str]) -> str:
    """The tag a correcting lower bound carries beside its star, `corrects Nagamochi
    2005`: one short span, with no link, since the table repeats it in most of its rows
    and the page's introduction links the corrected result once."""
    return f'<span class="site-corrects">{html.escape(corrects_tag(corrects) or "")}</span>'


def _cell(content: str, *, value: str | None = None, classes: str = "") -> str:
    attributes = f' class="{classes}"' if classes else ""
    if value is not None:
        attributes += f' data-value="{html.escape(value)}"'
    return f"<td{attributes}>{content}</td>"


#: What a verified cell says under its bound where every entry the bound cites is a
#: published proof nobody here has read (`render_research_tables.rests_on_unread_proof`):
#: n = 5, 6, 10 and 22 on 2026-10-06. A published proof proves its claim whether or not
#: it was read, so the bound stays in the verified column; the note says what this
#: repository has itself examined, which "✓ same" alone did not.
UNREAD_PROOF = "published proof, not read here"
#: What a reported cell says under its credit where the bound stands on a read here that
#: found a defect and no verified bound holds its value
#: (`render_research_tables.reported_defect`): on 2026-10-06, Nagamochi's closed form
#: wherever it is above the verified floor, and the values of Green's DS7 Theorem 9.
DEFECT_RECORDED = "defect recorded"


@cache
def evidence_entries() -> dict[str, dict[str, Any]]:
    """The evidence register, read once for the whole table."""
    return tables.load_evidence()


def _note(text: str) -> str:
    return f'<span class="site-frontier-note site-cell-quiet">{text}</span>'


def _bound_cell(bound: dict[str, Any], note: str = "", *, flag: str = "") -> str:
    parts = [value_html(bound), bound_approx_html(bound)]
    parts.extend(_note(text) for text in (note, flag) if text)
    return _cell("".join(parts), value=str(bound["value"]), classes="num")


def _verified_cell(verified: dict[str, Any], reported: dict[str, Any]) -> str:
    """A verified bound, or the mark that it equals the reported one, shown once, and
    under either, where every entry it cites is a published proof nobody here has read,
    the note that says so (`UNREAD_PROOF`). The mark carries no tooltip: the page's
    introduction says what it means, and the phrase 470 times over was 20 KB of a page
    held under a byte ceiling."""
    note = (
        _note(UNREAD_PROOF)
        if tables.rests_on_unread_proof(verified, evidence_entries())
        else ""
    )
    if bounds_agree_at_declared_precision(reported, verified):
        return _cell(
            f'<span class="site-frontier-same">✓ same</span>{note}',
            value=str(verified["value"]),
            classes="num",
        )
    return _cell(
        value_html(verified) + bound_approx_html(verified) + note,
        value=str(verified["value"]),
        classes="num",
    )


def case_row(
    case: dict[str, Any],
    *,
    recent: bool,
    corrects: Mapping[str, str] | None = None,
) -> str:
    """One table row, every cell from the record. The whole row opens the case's record
    in the page's one case popover (`overview/case-popover.js`), which shows it as the
    case's own page does, the visual summary and then the record's further data; its
    `n` is a link to that record, which is where a reader without scripts goes. The
    minimal popover each row opened until 2026-10-03, with the construction, the lower
    bound's kind and the verification notes, went then (think-necq): the record carries
    all of it. The cells are in `HEADERS`' order: the drawing, `n`, the star, and then
    what is known.

    A verified lower bound that corrects a published result keeps its star and carries
    the tag beside it in the same cell (`corrects_html`), and the row names the corrected
    result in `data-corrects`, the register's id for it (the owner, 2026-10-02)."""
    from devtools.overview_sections import case_status_chip  # noqa: PLC0415
    from devtools.render_case_pages import case_link, case_url  # noqa: PLC0415
    from devtools.result_overview import case_badges  # noqa: PLC0415

    n = case["n"]
    case_file = repo_url(tables.FRONTIER / f"n-{n:03d}.md")
    upper, lower = case["reported_upper_bound"], case["reported_lower_bound"]
    status = case["status"]
    shown_status = case_status_chip(status)
    if case["reported_status"] != status:
        shown_status += f" (reported {html.escape(case['reported_status'])})"
    gap_html, gap_value = gap(case)
    # The star carries no tooltip of its own: its column's heading names it, once
    # (`HEADER_TITLES`), where the phrase on each of 297 stars was 8 KB of a page held
    # under a byte ceiling, the room the correction tags beside them now take.
    star = '<span class="site-star">★</span>' if recent else ""
    if corrects:
        star += corrects_html(corrects)
    cells = [
        _cell(thumbnail_svg(n), classes="site-thumb"),
        _cell(
            case_link(n, str(n), label=f"n = {n}: open its case record"),
            value=str(n),
            classes="num site-col-n",
        ),
        _cell(star, value="1" if recent else "0"),
        _cell(f"{shown_status}{case_badges(n)}", value=status),
        _bound_cell(
            upper,
            credit(upper.get("found_by"), upper.get("found_year")),
            flag=DEFECT_RECORDED
            if tables.reported_defect(upper, case["verified_upper_bound"], evidence_entries())
            else "",
        ),
        _verified_cell(case["verified_upper_bound"], upper),
        _bound_cell(
            lower,
            credit(lower.get("proved_by"), lower.get("proved_year")),
            flag=DEFECT_RECORDED
            if tables.reported_defect(lower, case["verified_lower_bound"], evidence_entries())
            else "",
        ),
        _verified_cell(case["verified_lower_bound"], lower),
        _cell(gap_html, value=gap_value, classes="num"),
        # Two lines, the case file over the record, as the drawing is two lines high.
        _cell(
            f'<a href="{case_file}">n-{n:03d}.md</a> '
            f"{case_link(n, 'Record', classes='site-cell-quiet')}",
            classes="site-records",
        ),
    ]
    flag = {True: "true", False: "false"}
    attributes = (
        f'id="n-{n}" data-n="{n}" data-status="{html.escape(status)}" '
        f'data-open="{flag[status == "open"]}" data-recent="{flag[recent]}" '
        + (f'data-corrects="{html.escape(corrects["result"])}" ' if corrects else "")
        + f'data-case-row="{n}" data-case-href="{case_url(n)}" '
        f'aria-label="n = {n}, {html.escape(status)}: open its case record"'
    )
    return f"<tr {attributes}>{''.join(cells)}</tr>"


#: The drawing's column has no heading to read; this is its name for a screen reader.
THUMB_LABEL = "Packing"
#: The columns: heading, sort type (none for a column that does not sort), classes. The
#: drawing comes first, under no heading, then `n`, then the star, so the left edge of the
#: table says which case a row is and whether its bound is new; what is known follows.
HEADERS: tuple[tuple[str, str, str], ...] = (
    ("", "", "site-thumb"),
    ("n", "num", "num site-col-n"),
    ("Recent", "num", "site-col-recent"),
    ("Status", "text", ""),
    ("Best known packing", "num", "num"),
    ("Verified upper", "num", "num"),
    ("Reported lower", "num", "num"),
    ("Verified lower", "num", "num"),
    ("Gap", "num", "num"),
    ("Records", "", ""),
)


#: What a heading's tooltip says where its one word does not: the star's column, whose
#: rows carry the star and, beside it, what a correcting bound corrects.
HEADER_TITLES = {
    "Recent": "A recent lower bound, and the published result it corrects where it does",
}


def _heading(label: str, kind: str, classes: str) -> str:
    """A column's header cell. One with no words is named for a screen reader."""
    sort = f' data-sort="{kind}"' if kind else ""
    named = f' class="{classes}"' if classes else ""
    if not label:
        named += f' aria-label="{THUMB_LABEL}"'
    if label in HEADER_TITLES:
        named += f' title="{html.escape(HEADER_TITLES[label])}"'
    return f'<th scope="col"{sort}{named}>{html.escape(label)}</th>'


def _tools(count: int, last: int) -> str:
    """The filter bar, hidden until the table script wires it up."""
    number = f'type="number" data-filter="n" min="1" max="{last}" size="4"'
    return (
        '<div class="site-table-tools" data-table="frontier" hidden>'
        '<label>Status <select data-filter="status"><option value="">all</option>'
        '<option value="open">open</option><option value="proved">proved</option>'
        "</select></label>"
        '<label><input type="checkbox" data-filter="open"> open only</label>'
        '<label><input type="checkbox" data-filter="recent"> recent only</label>'
        f'<label><var>n</var> from <input {number} data-bound="min" placeholder="1"></label>'
        f'<label>to <input {number} data-bound="max" placeholder="{last}"></label>'
        f'<span class="site-count" aria-live="polite" data-noun="cases">{count} cases</span>'
        "</div>"
    )


def table_html(cases: list[dict[str, Any]]) -> str:
    """The controls, the table and the popover its rows open each case's record in, as
    one HTML block with no blank line inside it."""
    from devtools.render_case_pages import case_popover  # noqa: PLC0415

    recent = recent_lower_bounds()
    corrected = corrected_lower_bounds()
    head = "".join(_heading(*column) for column in HEADERS)
    rows = "\n".join(
        case_row(case, recent=recent.get(case["n"], False), corrects=corrected.get(case["n"]))
        for case in cases
    )
    return (
        f"{_tools(len(cases), max(case['n'] for case in cases))}\n"
        '<div class="site-table-wrap site-wide site-frontier" id="frontier-table">\n'
        '<table class="kpress-table site-table">\n'
        f"<thead><tr>{head}</tr></thead>\n<tbody>\n{rows}\n</tbody>\n</table>\n</div>\n"
        f"{case_popover()}"
    )


def frontier_markdown(fill: Callable[..., str]) -> str:
    """The article with every count and link filled from the record: the case counts
    from the case records, the survey's four counts from `render_recent_results`, and
    the two documents the prose links at their addresses on `main`. The star's own
    count over every case is not written: the prose counts the starred cases among the
    first hundred, and the bar's "recent only" counts them all."""
    cases = frontier_cases()
    values = {
        "COUNT": str(len(cases)),
        # The page carried a subtitle naming its range, `n = 1, …, 324`, set as sans
        # math (`math_html`), until 2026-10-02 (the owner, think-wz9d).
        "PROVED": str(sum(case["status"] == "proved" for case in cases)),
        "OPEN": str(sum(case["status"] == "open" for case in cases)),
        "RECENT_SINCE": since_prose(),
        "SURVEY_COUNTS": survey_counts(recent_counts(recent_rows())),
        "CORRECTIONS": corrections_prose(),
        "ARCHIVE_URL": repo_url(ARCHIVE_README),
        "INVENTORY_URL": repo_url(EVIDENCE_INVENTORY),
        "TABLE": table_html(cases),
    }
    template = FRONTIER_ARTICLE.read_text(encoding="utf-8")
    return fill(template, values, where=FRONTIER_ARTICLE.name)
