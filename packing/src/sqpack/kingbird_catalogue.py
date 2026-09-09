r"""Reparse the retained Kingbird catalogue into one typed record per pictured entry.

The frontier's ``reported_upper_bound.exact_form``, ``algebraic_degree`` and
``minimal_polynomial`` are hand-transcribed from this page, and until this module
existed nothing re-read them: ``devtools/check_source_coverage.py`` extracted the
printed decimal and the bare integer side, so a missed radical was invisible. That is
what hid ``n = 54``, the one entry at ``n <= 100`` the catalogue renders as a multi-line
``\begin{aligned}`` block instead of the single-line ``$s = <radical> = \Nn{<decimal>}$``
pattern the transcriber handled. The miss reached a published figure (``think-k5z2``).

Three decisions follow from that history.

**Entries are matched to ``n`` by their heading and their picture anchor, never by
position.** The catalogue's blocks move whenever a record is improved, and one block can
serve two counts -- a picture of ``n`` squares also settles ``n - 1`` by removing any
square -- so ``parse_catalogue`` keys every listed count to the same record.

**A block the parser cannot classify raises.** The failure this module exists to prevent
is a silent ``None`` standing in for a form the page prints, so an unrecognised side
line, an unconverted LaTeX fragment, or a polynomial with no degree lock and no readable
exponent all raise `CatalogueParseError` naming the line it was read from.

**Parsing needs no computer algebra.** ``parse_catalogue`` is pure text work; SymPy is
imported lazily, and only by the callers that evaluate a form (`evaluate_exact_form`)
or compare two polynomials (`normalized_polynomial`). SymPy is an optional dependency
here, and reading the catalogue must not require it.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from sqpack.project import require_project_root

#: Repository-relative location of the retained catalogue, transcription and original.
CATALOGUE_MARKDOWN = "resources/web/kingbird-squares-in-squares.md"
CATALOGUE_HTML = "resources/web/kingbird-squares-in-squares.html"

#: The glyph the catalogue prints where a root's degree is known but its form is not.
LOCK_GLYPH = "\N{LOCK}"

# The catalogue's own rigidity vocabulary. It annotates a handful of packings and is
# silent for the rest; it never asserts that a packing can move, which is why the third
# value is `not-stated` rather than `false`.
NOT_STATED = "not-stated"
RIGIDITY_STATES = ("rigid", "semi-rigid", NOT_STATED)

_HEADING = re.compile(r"^(\d+(?:\s*,\s*\d+)*)$")
# The picture filename may carry a variant suffix (`square-26b.svg`), and its number is
# not always the heading's largest, so it identifies a block but never names one.
_PICTURE = re.compile(r"^\[]\((square-[^)]+\.svg)\)$")
_MATH_SPAN = re.compile(r"\$([^$]*)\$")
_VALUE_MATH = re.compile(r"^\s*(?:\\begin\{aligned\})?\s*s\s*&?\s*=")
_RIGIDITY = re.compile(r"^\[(Rigid|Semi-rigid)\.?]\(squares_in_squares__rigid\.html\)")
_PRINTED_DECIMAL = re.compile(r"^\\Nn\{([0-9]+(?:\.[0-9]+)?)\}$")
_DEGREE_LOCK = re.compile(rf"^\{{}}\^\{{(\d+)}}{LOCK_GLYPH}$")
_PLAIN_NUMBER = re.compile(r"^[0-9]+(?:\.[0-9]+)?$")
_MARKDOWN_LINK = re.compile(r"\[([^\]]*)]\([^)]*\)")
#: The sentence openers the catalogue uses to name who found a packing, longest first so
#: that "Found and improved by" is never read as "Found by". Six, not the three this
#: module started with: reading only "Found first by", "Found by" and "Proved by" left
#: eight entries the page credits with no finder at all (``n = 123, 129, 154, 177, 206,
#: 230, 266, 301``), each opened with one of the three added here.
_CREDIT_OPENERS = (
    "Found first by",
    "Found and improved by",
    "Originally found by",
    "Found by",
    "Proved by",
    "Drafted by",
)
_CREDIT = re.compile(
    rf"(?:{'|'.join(_CREDIT_OPENERS)})\s+(?P<names>.+?)"
    r"\s+in\s+(?P<when>(?:[A-Za-z-]+\s+)*)(?P<year>\d{4})\b"
)
#: A sentence boundary inside one block's joined annotation lines. A period ends a
#: sentence only where it does not follow a single capital letter, which is what keeps
#: "David W. Cantrell" and "M.Z. Arslanov" whole. `devtools/generate_frontier_case.py`
#: carries the same three lines, for the reason its `CatalogueEntryLike` gives.
_SENTENCE_BREAK = re.compile(r"(?<![A-Z])\.\s+")
_COMPLETENESS = re.compile(
    r"For the \$n\s*(?:\u2264|<=|\\le(?:q)?\b)\s*(\d+)\$\s*not pictured", re.IGNORECASE
)
_EXPONENT_BRACES = re.compile(r"\^\{(-?\d+)}")
_SIDE_POWER = re.compile(r"s\^\{?(\d+)}?")

_FRACTION = re.compile(r"\{\s*(-?\d+)\s*\\over\s*(-?\d+)\s*}")
_SQRT_PLAIN = re.compile(r"\\sqrt\s*(\d+)")
_SQRT_BRACED = re.compile(r"\\sqrt\s*\{([^{}]*)}")
_ROW_BREAK = re.compile(r"\\{2,}")
_SIGN_SPACING = re.compile(r"\s*([+-])\s*")

#: LaTeX conversion is a fixpoint loop over nested braces; the deepest nesting the
#: catalogue prints is two (`\sqrt{1+\sqrt 2}`), so a form needing more rounds than this
#: is a shape this module has never seen and must not guess at.
_MAX_CONVERSION_ROUNDS = 8

_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_HTML_BOX = re.compile(r'<div class="box"><font size="\+3">\s*([0-9 ,]+)<br>')
_HTML_DECIMAL = re.compile(r"\\Nn\{([0-9]+(?:\.[0-9]+)?)}")
_HTML_INTEGER = re.compile(r"\$s\s*=\s*([0-9]+)\$")


class CatalogueParseError(ValueError):
    """The retained catalogue no longer has the shape this parser reads.

    Always carries the 1-based line it was raised from, because the whole point of the
    parser is that a transcription miss is loud rather than silent.
    """

    def __init__(self, message: str, *, line: int | None = None) -> None:
        super().__init__(message if line is None else f"line {line}: {message}")
        self.line: int | None = line


@dataclass(frozen=True)
class CatalogueEntry:
    """One pictured catalogue block, as the page prints it.

    Every field is what the catalogue states, never what this repository derives from it.
    `exact_form`, `algebraic_degree` and `minimal_polynomial` are `None` exactly where
    the page prints nothing, so a caller can tell "the source is silent" from "the
    transcription lost it" -- the distinction whose absence produced `think-k5z2`.
    """

    n: int
    """The count this entry primarily serves: the largest of `listed_n`."""

    listed_n: tuple[int, ...]
    """Every count the entry serves, in the order the heading lists them."""

    side_decimal: str
    """The printed decimal, verbatim digits. Truncated by the page, not rounded."""

    exact_form: str | None
    """The printed closed form in this repository's `exact_form` spelling."""

    algebraic_degree: int | None
    """The degree the page locks, or the printed polynomial's degree when it does not."""

    minimal_polynomial: str | None
    """The printed polynomial, LaTeX radicals and fractions converted, else verbatim."""

    found_by: tuple[str, ...]
    """Names from the entry's first credit sentence, in order; empty when unparseable.

    The catalogue writes six openers in the same slot -- "Found by", "Found first by",
    "Found and improved by", "Originally found by", "Drafted by" and "Proved by" -- and
    does not separate who built a packing from who proved a bound about it, so this
    field does not either. The frontier does -- `n = 6` credits Erich Friedman with the
    packing and Kearney and Shiu with the proof, where the catalogue prints only the
    latter -- which is why it is not a field the transcription check gates on.
    """

    found_year: int | None
    """The year of that credit sentence."""

    catalogue_rigid: str
    """One of `RIGIDITY_STATES`, from the entry's own annotation."""

    catalogue_pictured: bool
    """Whether the entry carries a picture. Every entry the page prints does."""

    svg_path: str | None
    """The picture the entry links, e.g. `square-71.svg`."""

    source_line: int
    """1-based line in the transcription carrying this entry's side value."""

    credit_line: str | None = None
    """The entry's annotation lines, verbatim, below its side value; `None` when it has none.

    Everything the block prints after the side value and before the next heading: the
    credit sentences, the rigidity annotation, the "Explore group" link, the family notes,
    and the page's "Not yet analytically optimized." disclaimer. The catalogue's own
    characters, with two mechanical changes and no others -- each line is right-stripped
    (the transcription's line ends carry Markdown's two-space hard break), and blank lines
    are dropped -- so the surviving lines are joined by a single newline in page order,
    Markdown link syntax included.

    The link syntax is what makes it worth keeping verbatim. `[Explore group](...)` is the
    only thing separating the Göbel strips from the Göbel squares, and its text is the same
    for both: the two families differ solely in the page it links to. `found_by` and
    `found_year` are read from the same lines with that markup unwrapped, which is why they
    are parsed separately rather than from this field.

    Added last, with a default, so that every existing construction of this record keeps
    working. It is the field a caller needs to read `construction_method` and
    `analytically_optimized`, neither of which the catalogue states anywhere else.
    """


def default_catalogue_path() -> Path:
    """Return the retained Markdown transcription inside the packing checkout."""
    return require_project_root() / CATALOGUE_MARKDOWN


def default_catalogue_html_path() -> Path:
    """Return the retained original HTML beside the transcription."""
    return require_project_root() / CATALOGUE_HTML


def _convert_latex(latex: str, line: int | None) -> str:
    """Rewrite the catalogue's LaTeX into the repository's plain spelling.

    `{1\\over 2}` becomes `(1/2)` and `\\sqrt{1+\\sqrt 2}` becomes `sqrt(1 + sqrt(2))`,
    innermost first. Whitespace is left alone here: the caller decides whether the result
    is an expression to normalise or a polynomial to keep verbatim.
    """
    text = latex
    for _ in range(_MAX_CONVERSION_ROUNDS):
        replaced = _FRACTION.sub(r"(\1/\2)", text)
        replaced = _SQRT_PLAIN.sub(r"sqrt(\1)", replaced)
        replaced = _SQRT_BRACED.sub(r"sqrt(\1)", replaced)
        if replaced == text:
            break
        text = replaced
    else:
        raise CatalogueParseError(
            f"LaTeX nests deeper than this parser reads: {latex!r}", line=line
        )
    if "\\" in text:
        raise CatalogueParseError(
            f"unconverted LaTeX remains in {latex!r}; the catalogue prints a form this "
            f"parser does not read, and must not be recorded as having none",
            line=line,
        )
    return text


def latex_to_exact_form(latex: str, line: int | None = None) -> str:
    """Convert one printed side expression into the repository's `exact_form` spelling.

    The spelling is the frontier's own: `7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))`, with one
    space either side of a binary sign and the coefficient spacing the page itself uses
    (`(1/2)sqrt(2)` from `{1\\over 2}\\sqrt 2`, `2 sqrt(2)` from `2 \\sqrt 2`).
    """
    text = _convert_latex(latex, line)
    text = _SIGN_SPACING.sub(r" \1 ", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def _normalize_aligned(side_math: str, line: int) -> str:
    """Flatten a multi-line `\\begin{aligned}` side block into the single-line form.

    This is the shape that hid `n = 54`. The two renderings carry identical content --
    an alignment marker and a row break where the single-line form writes `=` -- so
    removing both leaves a string the ordinary path reads.
    """
    inner = side_math.strip()
    if not inner.startswith(r"\begin{aligned}"):
        return inner
    if not inner.endswith(r"\end{aligned}"):
        raise CatalogueParseError(f"unterminated aligned side block: {side_math!r}", line=line)
    inner = inner[len(r"\begin{aligned}") : -len(r"\end{aligned}")]
    return _ROW_BREAK.sub(" ", inner).replace("&", " ").strip()


def _split_equations(side_math: str) -> list[str]:
    """Split a side expression on its top-level `=`, ignoring braced subexpressions."""
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for character in side_math:
        if character == "{":
            depth += 1
        elif character == "}":
            depth = max(depth - 1, 0)
        if character == "=" and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(character)
    parts.append("".join(current))
    return [part.strip() for part in parts]


def _parse_side(side_math: str, line: int) -> tuple[str, str | None, int | None]:
    """Return the printed decimal, the exact form, and any locked degree."""
    parts = _split_equations(_normalize_aligned(side_math, line))
    if len(parts) < 2 or parts[0] != "s":
        raise CatalogueParseError(
            f"side expression is not an `s = ...` chain: {side_math!r}", line=line
        )

    decimal_text: str | None = None
    exact_form: str | None = None
    degree: int | None = None
    for part in parts[1:]:
        printed = _PRINTED_DECIMAL.match(part)
        if printed is not None:
            decimal_text = printed.group(1)
            continue
        lock = _DEGREE_LOCK.match(part)
        if lock is not None:
            degree = int(lock.group(1))
            continue
        if exact_form is not None:
            raise CatalogueParseError(
                f"side expression prints two closed forms: {side_math!r}", line=line
            )
        exact_form = latex_to_exact_form(part, line)

    if decimal_text is None:
        if exact_form is not None and _PLAIN_NUMBER.match(exact_form):
            decimal_text = exact_form
        else:
            raise CatalogueParseError(
                f"side expression prints no decimal: {side_math!r}", line=line
            )
    return decimal_text, exact_form, degree


def _printed_degree(polynomial: str, line: int) -> int:
    """Read a printed polynomial's degree from its own exponents.

    Only sound over the rationals: a polynomial whose coefficients carry a radical has a
    larger degree over Q than the exponent it prints, so this refuses rather than
    guesses. The catalogue always pairs such a polynomial with a degree lock.
    """
    if "sqrt" in polynomial:
        raise CatalogueParseError(
            f"polynomial has radical coefficients and no degree lock, so its degree over "
            f"the rationals is not the exponent it prints: {polynomial!r}",
            line=line,
        )
    exponents = [int(match) for match in _SIDE_POWER.findall(polynomial)]
    if not exponents:
        raise CatalogueParseError(f"polynomial states no degree: {polynomial!r}", line=line)
    return max(exponents)


def split_credit_sentences(text: str) -> tuple[str, ...]:
    """One block's joined annotation lines, split into the sentences the page wrote."""
    return tuple(part.strip() for part in _SENTENCE_BREAK.split(text) if part.strip())


def _parse_credit(text: str) -> tuple[tuple[str, ...], int | None]:
    """Return the names and year of the entry's first credit sentence.

    Matched one sentence at a time, because the openers now include "Originally found
    by" and the page writes it without a year: `n = 272` reads "Originally found by Lars
    Cleemann between 1991 and 1998", and a search over the whole block would run the
    names group past two sentences to reach the next four-digit year it found. A credit
    is a sentence, so it is read as one, and an opener whose own sentence names no year
    yields nothing rather than a year from somewhere else.
    """
    for sentence in split_credit_sentences(text):
        match = _CREDIT.search(sentence)
        if match is None:
            continue
        names = [
            name.strip()
            for part in match.group("names").split(" and ")
            for name in part.split(",")
            if name.strip()
        ]
        return tuple(names), int(match.group("year"))
    return (), None


def _parse_block(
    block: list[str], *, start_line: int, listed_n: tuple[int, ...], svg_path: str
) -> CatalogueEntry:
    """Read one heading-to-heading block into its record."""
    value_offset: int | None = None
    spans: list[str] = []
    for offset, line in enumerate(block):
        candidates = _MATH_SPAN.findall(line)
        if candidates and _VALUE_MATH.match(candidates[0]):
            value_offset = offset
            spans = candidates
            break
    if value_offset is None:
        raise CatalogueParseError(
            f"catalogue block for n={list(listed_n)} prints no side value", line=start_line
        )
    value_line = start_line + value_offset

    decimal_text, exact_form, degree = _parse_side(spans[0], value_line)
    polynomial: str | None = None
    if len(spans) > 1:
        polynomial = _convert_latex(spans[1], value_line).strip()
        if degree is None:
            degree = _printed_degree(polynomial, value_line)

    rigidity = NOT_STATED
    for line in block:
        annotation = _RIGIDITY.match(line.strip())
        if annotation is not None:
            rigidity = annotation.group(1).lower()
            break

    annotation_lines = [line.rstrip() for line in block[value_offset + 1 :] if line.strip()]
    credit = " ".join(_MARKDOWN_LINK.sub(r"\1", line).strip() for line in annotation_lines)
    found_by, found_year = _parse_credit(credit)

    return CatalogueEntry(
        n=max(listed_n),
        listed_n=listed_n,
        side_decimal=decimal_text,
        exact_form=exact_form,
        algebraic_degree=degree,
        minimal_polynomial=polynomial,
        found_by=found_by,
        found_year=found_year,
        catalogue_rigid=rigidity,
        catalogue_pictured=True,
        svg_path=svg_path,
        source_line=value_line,
        credit_line="\n".join(annotation_lines) or None,
    )


def parse_entries(text: str) -> tuple[CatalogueEntry, ...]:
    """Parse the retained transcription into its pictured blocks, in file order."""
    lines = text.splitlines()
    starts: list[tuple[int, tuple[int, ...], str]] = []
    for index, line in enumerate(lines):
        heading = _HEADING.match(line.strip())
        if heading is None:
            continue
        following = next((c for c in lines[index + 1 : index + 3] if c.strip()), "")
        picture = _PICTURE.match(following.strip())
        if picture is None:
            continue
        listed = tuple(int(part) for part in re.split(r"\s*,\s*", heading.group(1)))
        starts.append((index, listed, picture.group(1)))
    if not starts:
        raise CatalogueParseError(
            "no pictured catalogue blocks found; the archive format changed"
        )

    bounds = [start for start, _, _ in starts] + [len(lines)]
    return tuple(
        _parse_block(
            lines[start : bounds[position + 1]],
            start_line=start + 1,
            listed_n=listed_n,
            svg_path=svg_path,
        )
        for position, (start, listed_n, svg_path) in enumerate(starts)
    )


def index_entries(entries: tuple[CatalogueEntry, ...]) -> dict[int, CatalogueEntry]:
    """Key parsed entries by every count each one serves.

    A block labelled `7, 8` resolves under both keys and yields the same record, because
    the picture of eight squares settles seven by removing one.
    """
    by_n: dict[int, CatalogueEntry] = {}
    for entry in entries:
        for n in entry.listed_n:
            previous = by_n.setdefault(n, entry)
            if previous is not entry:
                raise CatalogueParseError(
                    f"n={n} is listed by two blocks, at lines {previous.source_line} "
                    f"and {entry.source_line}",
                    line=entry.source_line,
                )
    return by_n


def parse_catalogue(path: Path | None = None) -> dict[int, CatalogueEntry]:
    """Return the retained catalogue keyed by every count each entry serves."""
    target = default_catalogue_path() if path is None else path
    return index_entries(parse_entries(target.read_text(encoding="utf-8")))


def catalogue_completeness_bound(path: Path | None = None) -> int:
    """Return the largest n the page covers, from its own sentence about it.

    The catalogue states that for every `n` below this bound it does not picture, the
    trivial untilted packing is the best known. Parsed rather than assumed: if the page
    is re-retrieved with a larger bound, silently keeping the old one would make every
    "the catalogue is silent here" reading wrong.
    """
    target = default_catalogue_path() if path is None else path
    return completeness_bound_from_text(target.read_text(encoding="utf-8"))


def completeness_bound_from_text(text: str) -> int:
    """Read the completeness bound out of already-loaded catalogue text."""
    match = _COMPLETENESS.search(text)
    if match is None:
        raise CatalogueParseError(
            "the catalogue no longer states the bound below which an unpictured n takes "
            "the trivial packing; re-read the page before trusting any coverage claim"
        )
    return int(match.group(1))


def evaluate_exact_form(exact_form: str, digits: int = 50) -> Decimal:
    """Evaluate one `exact_form` string to `digits` significant decimal digits.

    The parse is the repository's existing recipe -- SymPy's standard transformations
    plus implicit multiplication, so `(1/2)sqrt(2)` and `2 sqrt(2)` both read -- which is
    what makes a frontier form and a catalogue form comparable as numbers rather than as
    strings.
    """
    import sympy as sp  # noqa: PLC0415 - optional dependency, imported where it is used
    from sympy.parsing.sympy_parser import (  # noqa: PLC0415
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )

    transformations = (*standard_transformations, implicit_multiplication_application)
    value = parse_expr(exact_form, transformations=transformations)
    if value.free_symbols:
        raise CatalogueParseError(f"exact form is not a number: {exact_form!r}")
    return Decimal(str(sp.N(value, digits)))


def agrees_with_printed_decimal(value: Decimal, side_decimal: str) -> bool:
    """Whether an exact value agrees with the decimal the catalogue prints for it.

    The page truncates rather than rounds -- `7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))` is
    `7.84666719284348978...` and prints as `7.84666719284348` -- so the tolerance is one
    unit in the last printed place, which admits either convention and nothing looser.
    """
    printed = Decimal(side_decimal)
    exponent = printed.as_tuple().exponent
    places = -exponent if isinstance(exponent, int) else 0
    return abs(value - printed) < Decimal(10) ** -places


def exact_form_matches_decimal(entry: CatalogueEntry) -> bool:
    """Whether one entry's printed closed form agrees with its printed decimal.

    Vacuously true where the page prints no closed form. It is false for exactly one
    entry, `n = 179`, whose block pairs a January-2025 closed form with a January-2026
    decimal it does not equal and then says "Not yet analytically optimized": the record
    was improved and the stale form was left beside it. That is a fact about the source,
    not a parse failure, so it is reported here rather than raised -- a caller reading
    `exact_form` for `n >= 101` has to be able to see it.
    """
    if entry.exact_form is None:
        return True
    return agrees_with_printed_decimal(
        evaluate_exact_form(entry.exact_form), entry.side_decimal
    )


def normalized_polynomial(polynomial: str) -> tuple[int, ...]:
    """Return one printed polynomial as primitive integer coefficients, highest first.

    Two spellings of the same polynomial normalise to the same tuple: a trailing `= 0`,
    braced exponents, and any nonzero rational scale all wash out. A polynomial whose
    coefficients live in a real quadratic field -- the catalogue prints one, at `n = 37`
    -- is replaced by its norm over the rationals, which is the polynomial the frontier
    records for the same root. Applying that to both sides keeps the comparison
    symmetric: either spelling of that entry reduces to the same tuple.
    """
    import sympy as sp  # noqa: PLC0415 - optional dependency, imported where it is used
    from sympy.parsing.sympy_parser import (  # noqa: PLC0415
        convert_xor,
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )

    body = _EXPONENT_BRACES.sub(r"^\1", polynomial.split("=", maxsplit=1)[0])
    if "{" in body or "}" in body:
        raise CatalogueParseError(f"polynomial carries unread braces: {polynomial!r}")
    transformations = (
        *standard_transformations,
        implicit_multiplication_application,
        convert_xor,
    )
    expression = sp.expand(parse_expr(body, transformations=transformations))
    side = sp.Symbol("s")
    if expression.free_symbols - {side}:
        raise CatalogueParseError(f"polynomial names more than one unknown: {polynomial!r}")

    for _ in range(_MAX_CONVERSION_ROUNDS):
        radicals = sorted(
            (
                atom
                for atom in expression.atoms(sp.Pow)
                if atom.exp == sp.Rational(1, 2) and atom.base.is_Rational
            ),
            key=sp.default_sort_key,
        )
        if not radicals:
            break
        radical = radicals[0]
        expression = sp.expand(expression * expression.subs(radical, -radical))
    else:
        raise CatalogueParseError(f"polynomial has more radicals than expected: {polynomial!r}")

    coefficients = sp.Poly(expression, side).all_coeffs()
    if not all(coefficient.is_Rational for coefficient in coefficients):
        raise CatalogueParseError(f"polynomial has irrational coefficients: {polynomial!r}")
    scale = 1
    for coefficient in coefficients:
        scale = math.lcm(scale, int(sp.denom(coefficient)))
    integers = [int(coefficient * scale) for coefficient in coefficients]
    common = math.gcd(*(abs(value) for value in integers)) if integers else 0
    if common:
        integers = [value // common for value in integers]
    if integers and integers[0] < 0:
        integers = [-value for value in integers]
    return tuple(integers)


def polynomials_agree(left: str, right: str) -> bool:
    """Whether two printed polynomials denote the same rational polynomial."""
    return normalized_polynomial(left) == normalized_polynomial(right)


def html_entry_labels(text: str) -> tuple[tuple[tuple[int, ...], str], ...]:
    """Return the live HTML boxes as (listed counts, printed side), in document order.

    The transcription is what everything else reads, so this exists to answer one
    question about it: did `html2text` drop or reorder a box? Commented-out boxes are
    superseded records the page keeps in source, and are not live entries.
    """
    stripped = _HTML_COMMENT.sub("", text)
    chunks = stripped.split('<div class="box">')
    labels: list[tuple[tuple[int, ...], str]] = []
    for chunk in chunks[1:]:
        heading = _HTML_BOX.match('<div class="box">' + chunk)
        if heading is None:
            continue
        listed = tuple(int(value) for value in re.findall(r"\d+", heading.group(1)))
        printed = _HTML_DECIMAL.search(chunk) or _HTML_INTEGER.search(chunk)
        if printed is None:
            raise CatalogueParseError(f"HTML box for n={list(listed)} prints no side value")
        labels.append((listed, printed.group(1)))
    return tuple(labels)


def cross_check_html(
    entries: tuple[CatalogueEntry, ...], html_text: str | None = None
) -> list[str]:
    """Report every place the transcription and the retained HTML disagree.

    Compared on labels and printed sides only. Those are the two facts both renderings
    carry verbatim, and they are enough to catch a lost, duplicated, or reordered box.
    """
    text = (
        html_text
        if html_text is not None
        else default_catalogue_html_path().read_text(encoding="utf-8")
    )
    html = html_entry_labels(text)
    errors: list[str] = []
    if len(html) != len(entries):
        errors.append(
            f"the transcription has {len(entries)} entries and the retained HTML has "
            f"{len(html)}; a box was lost or added in transcription"
        )
    for entry, (listed, printed) in zip(entries, html, strict=False):
        if entry.listed_n != listed:
            errors.append(
                f"line {entry.source_line}: transcription lists n={list(entry.listed_n)} "
                f"where the HTML lists n={list(listed)}"
            )
        elif entry.side_decimal != printed:
            errors.append(
                f"line {entry.source_line}: n={list(entry.listed_n)} prints "
                f"{entry.side_decimal} in the transcription and {printed} in the HTML"
            )
    return errors
