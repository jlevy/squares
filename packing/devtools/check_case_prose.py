#!/usr/bin/env python3
"""A case's prose must still say what its own front matter says, after the front matter moves.

`packing/frontier/n-NNN.md` files carry YAML front matter -- the machine record, including
`packing.verified_lower_bound` and `packing.verified_upper_bound`, each a `value` and an
`exact_form` -- followed by hand-written Markdown prose that restates those bounds in
sentences. When a result moves a case's verified bound, the front matter is updated and the
prose is not: on 2026-09-04, `n-017.md`, `n-018.md` and `n-019.md` all still read "The
verified lower bound is `s(17) >= 22529/5000 = 4.5058`" in prose while their front matter
already said `4.59`, and stayed that way for six hours before a line-by-line read caught it.
This is the same defect class as `D-439` -- a durable record describing a rung after the
rung moved -- at a surface no existing checker reaches: `check_rung_figures.py` reads
`results.yaml`, `evidence.yaml` and `defects.yaml`, never a case body.

This is that detector. For every `frontier/n-*.md`, it does three things:

1. **Parses the front matter** (the YAML block between the first two `---` lines, via
   `sqpack.yamlio.safe_load`) and reads `verified_lower_bound` and `verified_upper_bound`
   (`value`/`exact_form`), plus `reported_lower_bound`/`reported_upper_bound` for the one
   purpose described next.

2. **Scans the prose body for quoted bound figures anchored to this file's own `n`**, in the
   shapes the corpus actually uses:
   - `` `s(19) >= 22529/5000 = 4.5058` ``, `` `s(19) >= 4.5058` ``, `` `s(19) <= 4.88561808` ``
     -- a direct bound on this file's own `n`, `>=`/`≥` meaning lower and `<=`/`≤` upper.
   - The same inside a chain, `` `s(19) >= s(17) >= 22529/5000 = 4.5058` `` -- inheritance
     is irrelevant; the figure is a bound on *this* `n` regardless of where it came from.
   - A bare decimal introduced by name: "the best proved lower bound is `4.741657`", or
     "Nagamochi's general `4.316625`" / "Nagamochi's general `1 + √12 ≈ 4.464102`" -- the
     other bare-decimal shape the corpus uses, whenever the reported bound is Nagamochi's.
   - The disclaimer sentence a case with an unverified tighter construction always carries:
     "`verified_upper_bound` for this case is `5`" (`n-017`, `n-028`, ... -- every case where
     `reported_upper_bound` is tighter than what this repository has itself verified says
     this, in exactly this form, and it is checked directly against `verified_upper_bound`
     with no fallback: the field is named in the sentence, so there is nothing to guess at).

   A quoted figure must equal the front matter's corresponding bound, rounded
   (`ROUND_HALF_UP`, exactly as `check_rung_figures` rounds) to the number of decimal places
   the prose itself wrote -- **or** it must equal the corresponding `reported_*_bound` at
   that same precision. The second alternative is not a loophole; it is what keeps this
   check from crying wolf at every open case: "the best known packing gives `s(29) <=
   5.93383346`" is a citation of the *reported* construction, not of this repository's own
   verified ceiling, and the two legitimately differ whenever a published packing outruns
   what has been formally verified here (`n-017`'s own body explains this at length, under
   "The verified upper bound is a ceiling"). Checking reported figures against
   `reported_*_bound` is exactly as mechanical, and exactly as load-bearing, as checking
   verified figures against `verified_*_bound` -- both are the front matter disagreeing with
   the prose, just via different fields depending on which one the sentence is about.

   A figure that matches neither is not automatically a finding: if it is *strictly weaker*
   than the current `verified_*_bound` (a smaller lower bound, a larger upper bound) and its
   sentence is explicitly marked historical -- this corpus writes that as "now weaker",
   "was", "previously", "second strongest", "until", or "superseded" -- it is a case
   describing its own history, not a stale claim, and is allowed. Every other disagreement
   is a finding.

3. **Rechecks every `a/b = d.ddd` in each case body**, repository-wide, for correct
   arithmetic -- the exact rule `check_rung_figures.py` already applies to `results.yaml`,
   `evidence.yaml` and `defects.yaml` (its `_FRACTION_EQUALS_DECIMAL` pattern and its
   `decimal_matches`/`round_to` helpers, imported rather than reimplemented, so the two
   checkers can never disagree about what "arithmetically true" means). This is unconditional
   and unrelated to which `n` a figure is about: `189/50 = 3.78` in `n-011`'s body is checked
   the same way regardless of whose bound it is illustrating.

What this does **not** cover: `n-011`'s own "`s(11)` is pinned to `[3.8, 3.877084]`" range
notation is a fourth shape this module does not recognise, so a stale figure written only
that way would not be caught -- the corpus does not use it for any other open case, and a
check that guesses at an unfamiliar shape risks the same false positive this module works to
avoid elsewhere. Nor does it check the companion figure in "which is **larger** than the
best known `X` two fields above it" (the `reported_upper_bound` restated next to the
`verified_upper_bound` disclaimer) -- that figure is already covered by the direct `s(n) <=`
citation earlier in the same body, and adding a second, unanchored pattern for the same
number was judged not worth the added surface for cross-checking a value this module already
checks once.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_case_prose
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Literal

from devtools.check_rung_figures import decimal_matches, round_to
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
# The repository root; findings are reported repository-relative, as this repository's own
# convention requires for every declared path in the record (`AGENTS.md`).
REPO = ROOT.parent
FRONTIER = ROOT / "frontier"

#: Enough significant figures for any fraction this register carries; matches
#: `check_rung_figures`'s own constant, for the same reason.
_DECIMAL_PRECISION = 60

#: Sentence boundaries within raw (line-wrapped) Markdown prose: identical to
#: `check_rung_figures`'s rule, which already handles a period that is not itself part of a
#: decimal number and a line-wrap's whitespace (including the newline) before the next
#: capitalised sentence.
_SENTENCE_BOUNDARY = re.compile(r"(?<=[a-z0-9`*_)\]])\.\s+(?=[A-Z])")

#: `a/b = d.ddd`, anywhere in a case body -- byte-for-byte `check_rung_figures`'s own
#: `_FRACTION_EQUALS_DECIMAL`, mirrored rather than imported because that name is private to
#: its module; `decimal_matches` and `round_to`, which *are* public, are imported below so
#: the two checkers still share one definition of "arithmetically true".
_FRACTION_EQUALS_DECIMAL = re.compile(r"(?<![\w.])(\d+)/(\d+)\s*=\s*(-?\d+\.\d+)(?!\d)")

#: The corpus's own markers for "this figure is deliberately historical", read case-
#: insensitively anywhere in the figure's sentence. See the module docstring, point 2.
_HISTORICAL_MARKER = re.compile(
    r"now weaker|previously|second strongest|\buntil\b|superseded|displaced|\bwas\b",
    re.IGNORECASE,
)

_OP_GE = r"(?:≥|>=)"
_OP_LE = r"(?:≤|<=)"
#: A rational, optionally followed by its decimal rendering, or a bare integer/decimal.
#: The final boundary is load-bearing: without it, an exact-only `24/5` is misread as 24.
_FIGURE = r"(?:(\d+)/(\d+)(?:\s*=\s*(-?\d+(?:\.\d+)?))?|(-?\d+(?:\.\d+)?))(?![/\d])"

#: `` `s(19) >= ... >= 22529/5000 = 4.5058` `` -- one or more `s(M) >=` hops (any `M`,
#: unchecked) ending at the figure a bound on *this file's own `n`* -- captured as group 1 --
#: is stated to be.
_BOUND_GE = re.compile(rf"s\((\d+)\)\s*{_OP_GE}\s*(?:s\(\d+\)\s*{_OP_GE}\s*)*{_FIGURE}")
_BOUND_LE = re.compile(rf"s\((\d+)\)\s*{_OP_LE}\s*(?:s\(\d+\)\s*{_OP_LE}\s*)*{_FIGURE}")

#: "the best proved lower bound is `9.544004`" -- the bare-decimal shape, always about this
#: file's own `n` since nothing else is named.
_BEST_PROVED = re.compile(r"best proved (lower|upper) bound\s+is\s+`(-?\d+(?:\.\d+)?)`")

# A generic ``s(n) >= X`` sentence may cite either the verified or reported field. Once
# the prose explicitly calls it the verified/current first-party bound, the reported
# fallback would hide exactly the stale-prose defect this checker exists to catch.
_VERIFIED_BOUND_ANCHOR = re.compile(
    r"\b(?:verified|current first-party|best proved)\s+(lower|upper)\s+bound\b",
    re.IGNORECASE,
)

# A direct inequality described as the reported/best-known bound must not silently match
# the repository's verified field when the two differ. "Best known packing" is the corpus's
# recurring upper-bound spelling; lower-bound prose names the bound itself.
_REPORTED_BOUND_ANCHOR = re.compile(
    r"\b(?:reported|best[- ]known(?: published)?)\s+(lower|upper)\s+bound\b",
    re.IGNORECASE,
)
_BEST_KNOWN_PACKING = re.compile(r"\bbest[- ]known(?: published)? packing\b", re.IGNORECASE)

#: "Nagamochi's general `4.316625`" or "Nagamochi's general `1 + √12 ≈ 4.464102`" -- this
#: corpus's other recurring bare-decimal shape, always this file's own reported (and, unless
#: displaced, verified) lower bound, so also always about this file's own `n`.
_NAGAMOCHI_GENERAL = re.compile(r"Nagamochi[\u2019']s general\s*`(?:[^`]*?≈\s*)?(-?\d+\.\d+)`")

# The one remaining unambiguous bare-field shape in the corpus: "the verified `4.59`
# bound" in a lower-bound history paragraph. It is deliberately narrow; an unqualified
# bare value still carries too little information for this checker to infer a field.
_VERIFIED_BARE_LOWER = re.compile(r"\bverified\s+`(-?\d+(?:\.\d+)?)`\s+bound\b", re.IGNORECASE)

#: "`verified_upper_bound` for this case is `5`" -- the ceiling-disclaimer's own explicit
#: claim, naming the front-matter field it is about, so it is checked against that field
#: directly with no reported-bound fallback and no historical exemption.
_VERIFIED_FIELD = re.compile(
    r"`verified_(upper|lower)_bound`\s+for this case is\s+`(-?\d+(?:\.\d+)?)`"
)


def sentence_spans(text: str) -> list[tuple[int, int]]:
    """Every sentence in `text` as a `(start, end)` character span, covering all of `text`."""
    spans: list[tuple[int, int]] = []
    start = 0
    for match in _SENTENCE_BOUNDARY.finditer(text):
        spans.append((start, match.start() + 1))  # include the sentence-ending period
        start = match.end()
    spans.append((start, len(text)))
    return spans


def _digits_of(figure: str) -> int:
    return len(figure.split(".", 1)[1]) if "." in figure else 0


def _stated_decimal(figure: str) -> tuple[Decimal, int]:
    """Return the stated value and comparison precision, preserving exact rationals."""
    if "/" in figure:
        digits = 40
        return round_to(Fraction(figure), digits), digits
    return Decimal(figure), _digits_of(figure)


@dataclass(frozen=True, slots=True)
class BoundField:
    """One front-matter bound: its printed `value` and, when present, its exact `exact_form`."""

    value: str | None
    exact_form: str | None

    def exact_fraction(self) -> Fraction | None:
        """Return the exact value when `exact_form` is a plain integer or rational."""
        candidate = self.exact_form.strip() if isinstance(self.exact_form, str) else ""
        if re.fullmatch(r"-?\d+(?:/\d+)?", candidate):
            return Fraction(candidate)
        return None

    def decimal_at(self, digits: int) -> Decimal | None:
        """This bound rounded to `digits` decimal places, the way prose rounds a number.

        Exact `Fraction` arithmetic when `exact_form` is a plain integer or rational (the
        common case -- `459/100`, `24/5`, or a bare `5`); otherwise the stored `value`
        decimal string itself, which is the only representation available for an irrational
        `exact_form` like `(7/2) + (1/2)sqrt(7)`, and carries ample precision for any digit
        count this corpus's prose writes.
        """
        if self.value is None:
            return None
        exact = self.exact_fraction()
        if exact is not None:
            return round_to(exact, digits)
        quantum = Decimal(1).scaleb(-digits)
        with localcontext() as context:
            context.prec = _DECIMAL_PRECISION
            return Decimal(str(self.value)).quantize(quantum, rounding=ROUND_HALF_UP)

    def safe_decimal_at(self, digits: int, kind: str) -> Decimal | None:
        """Render a decimal without strengthening a lower or upper bound."""
        if self.value is None:
            return None
        exact = self.exact_fraction()
        with localcontext() as context:
            context.prec = _DECIMAL_PRECISION
            candidate = (
                Decimal(exact.numerator) / Decimal(exact.denominator)
                if exact is not None
                else Decimal(self.value)
            )
            quantum = Decimal(1).scaleb(-digits)
            rounding = ROUND_FLOOR if kind == "lower" else ROUND_CEILING
            return candidate.quantize(quantum, rounding=rounding)


@dataclass(frozen=True, slots=True)
class CaseFrontMatter:
    """The four bound fields one case's front matter carries, plus its own `n`."""

    n: int
    verified_lower: BoundField
    verified_upper: BoundField
    reported_lower: BoundField
    reported_upper: BoundField


def _bound_field(packing: dict[str, Any], name: str) -> BoundField:
    raw = packing.get(name) or {}
    value = raw.get("value")
    exact_form = raw.get("exact_form")
    return BoundField(
        value=None if value is None else str(value),
        exact_form=None if exact_form is None else str(exact_form),
    )


def parse_front_matter(document: dict[str, Any]) -> CaseFrontMatter:
    packing = document["packing"]
    return CaseFrontMatter(
        n=int(packing["n"]),
        verified_lower=_bound_field(packing, "verified_lower_bound"),
        verified_upper=_bound_field(packing, "verified_upper_bound"),
        reported_lower=_bound_field(packing, "reported_lower_bound"),
        reported_upper=_bound_field(packing, "reported_upper_bound"),
    )


def split_front_matter(text: str) -> tuple[str, str, int]:
    """`(front_matter_yaml, body, body_start_line)` -- the block between the first two `---`
    delimiter lines, everything after the second, and that body's 1-indexed starting line
    number in `text`, for reporting findings as `file:line`.
    """
    lines = text.splitlines(keepends=True)
    delimiters = [index for index, line in enumerate(lines) if line.rstrip("\r\n") == "---"]
    if len(delimiters) < 2:
        raise ValueError("no YAML front matter delimiters ('---') found")
    first, second = delimiters[0], delimiters[1]
    front_matter = "".join(lines[first + 1 : second])
    body = "".join(lines[second + 1 :])
    body_start_line = second + 2  # 1-indexed line number of the body's first line
    return front_matter, body, body_start_line


@dataclass(frozen=True, slots=True)
class BoundClaim:
    """One quoted `>=`/`<=` (or "best proved ... is") figure, anchored to this file's `n`."""

    kind: str
    """"lower" or "upper"."""
    figure: str
    """The figure exactly as written, e.g. "4.5058" or "5"."""
    offset: int
    """Character offset within the case body, for line-number lookup."""
    sentence: str
    """The sentence the figure was found in, for the historical-mention exemption."""
    provenance: Literal["verified", "reported", "either"] = "either"
    """Which front-matter field the surrounding prose says the figure comes from."""


def _direct_claim_provenance(
    preceding_context: str, kind: str
) -> Literal["verified", "reported", "either"]:
    anchors: list[tuple[int, Literal["verified", "reported"]]] = []
    anchors.extend(
        (anchor.start(), "verified")
        for anchor in _VERIFIED_BOUND_ANCHOR.finditer(preceding_context)
        if anchor.group(1).lower() == kind
    )
    anchors.extend(
        (anchor.start(), "reported")
        for anchor in _REPORTED_BOUND_ANCHOR.finditer(preceding_context)
        if anchor.group(1).lower() == kind
    )
    if kind == "upper":
        anchors.extend(
            (anchor.start(), "reported")
            for anchor in _BEST_KNOWN_PACKING.finditer(preceding_context)
        )
    if not anchors:
        return "either"
    return max(anchors, key=lambda anchor: anchor[0])[1]


def _paragraph_around(text: str, offset: int) -> str:
    """The Markdown paragraph containing `offset`, excluding adjacent headings/sections."""
    start = text.rfind("\n\n", 0, offset)
    start = 0 if start < 0 else start + 2
    end = text.find("\n\n", offset)
    end = len(text) if end < 0 else end
    return text[start:end]


def bound_claims(body: str, n: int) -> list[BoundClaim]:
    """Every figure anchored to this file's own `n`, from any of the four bound shapes."""
    claims: list[BoundClaim] = []
    for start, end in sentence_spans(body):
        sentence = body[start:end]
        for regex, kind in ((_BOUND_GE, "lower"), (_BOUND_LE, "upper")):
            for match in regex.finditer(sentence):
                if int(match.group(1)) != n:
                    continue
                absolute_offset = start + match.start()
                paragraph = _paragraph_around(body, absolute_offset)
                paragraph_start = body.rfind("\n\n", 0, absolute_offset)
                paragraph_start = 0 if paragraph_start < 0 else paragraph_start + 2
                within_paragraph = absolute_offset - paragraph_start
                provenance = _direct_claim_provenance(
                    paragraph[: max(0, within_paragraph)], kind
                )
                numerator, denominator, rendered, bare = match.group(2, 3, 4, 5)
                if rendered is not None:
                    figure = rendered
                    figure_group = 4
                elif numerator is not None:
                    figure = f"{numerator}/{denominator}"
                    figure_group = 2
                else:
                    figure = bare
                    figure_group = 5
                assert figure is not None
                claims.append(
                    BoundClaim(
                        kind,
                        figure,
                        start + match.start(figure_group),
                        sentence,
                        provenance=provenance,
                    )
                )
        claims.extend(
            BoundClaim(
                match.group(1),
                match.group(2),
                start + match.start(2),
                sentence,
                provenance="verified",
            )
            for match in _BEST_PROVED.finditer(sentence)
        )
        claims.extend(
            BoundClaim(
                "lower",
                match.group(1),
                start + match.start(1),
                sentence,
                provenance="reported",
            )
            for match in _NAGAMOCHI_GENERAL.finditer(sentence)
        )
        claims.extend(
            BoundClaim(
                "lower",
                match.group(1),
                start + match.start(1),
                sentence,
                provenance="verified",
            )
            for match in _VERIFIED_BARE_LOWER.finditer(sentence)
        )
    return claims


@dataclass(frozen=True, slots=True)
class VerifiedFieldClaim:
    """The ceiling-disclaimer's own explicit claim about one verified bound field."""

    kind: str
    figure: str
    offset: int


def verified_field_claims(body: str) -> list[VerifiedFieldClaim]:
    return [
        VerifiedFieldClaim(match.group(1), match.group(2), match.start(2))
        for match in _VERIFIED_FIELD.finditer(body)
    ]


def _is_historical_mention(sentence: str) -> bool:
    return _HISTORICAL_MARKER.search(sentence) is not None


def _field_matches_claim(field: BoundField, figure: str, kind: str) -> bool:
    """Whether `figure` is an exact or directionally safe rendering of `field`.

    A lower-bound decimal may round only downward and an upper-bound decimal only upward.
    This matters at coarse precision: nearest-integer rounding must not let an exact lower
    bound of `24/5` validate the stronger false statement `s(n) >= 5`.
    """
    if field.value is None:
        return False
    exact = field.exact_fraction()
    if "/" in figure:
        stated_fraction = Fraction(figure)
        if exact is not None:
            return stated_fraction == exact
        stated_decimal = Decimal(stated_fraction.numerator) / Decimal(
            stated_fraction.denominator
        )
        return stated_decimal == Decimal(field.value)

    stated = Decimal(figure)
    digits = _digits_of(figure)
    quantum = Decimal(1).scaleb(-digits)
    with localcontext() as context:
        context.prec = _DECIMAL_PRECISION
        if exact is not None:
            candidate = Decimal(exact.numerator) / Decimal(exact.denominator)
        else:
            candidate = Decimal(field.value)
        if kind == "lower":
            return stated <= candidate < stated + quantum
        return stated - quantum < candidate <= stated


def check_bound_claim(claim: BoundClaim, front_matter: CaseFrontMatter) -> str | None:
    """`None` if `claim` agrees with the front matter (directly, via the reported bound, or
    via the historical-mention exemption); otherwise a description of the disagreement.
    """
    stated, digits = _stated_decimal(claim.figure)
    lower = claim.kind == "lower"
    verified = front_matter.verified_lower if lower else front_matter.verified_upper
    reported = front_matter.reported_lower if lower else front_matter.reported_upper
    verified_value = verified.decimal_at(digits)
    reported_value = reported.decimal_at(digits)

    allow_verified = claim.provenance in {"verified", "either"}
    allow_reported = claim.provenance in {"reported", "either"}
    if allow_verified and _field_matches_claim(verified, claim.figure, claim.kind):
        return None
    if allow_reported and _field_matches_claim(reported, claim.figure, claim.kind):
        return None
    if verified_value is not None and claim.provenance != "verified":
        weaker = stated < verified_value if claim.kind == "lower" else stated > verified_value
        if weaker and _is_historical_mention(claim.sentence):
            return None

    op = "≥" if claim.kind == "lower" else "≤"
    front = (
        f"verified_{claim.kind}_bound rounds to {verified_value}"
        if (verified_value is not None)
        else f"verified_{claim.kind}_bound is unset"
    )
    if reported_value is not None:
        front += f" (reported_{claim.kind}_bound rounds to {reported_value})"
    if claim.provenance != "either":
        front += f"; prose identifies the {claim.provenance} field"
    return f"prose says s(n) {op} {claim.figure}, but {front}"


def check_verified_field_claim(
    claim: VerifiedFieldClaim, front_matter: CaseFrontMatter
) -> str | None:
    """The ceiling-disclaimer's figure must equal `verified_{kind}_bound` exactly -- the
    sentence names the field itself, so there is no reported-bound fallback here and no
    historical exemption: this sentence is never about anything but the present value.
    """
    verified = (
        front_matter.verified_lower if claim.kind == "lower" else front_matter.verified_upper
    )
    digits = _digits_of(claim.figure)
    value = verified.decimal_at(digits)
    if _field_matches_claim(verified, claim.figure, claim.kind):
        return None
    return f"prose says verified_{claim.kind}_bound is {claim.figure}, but it rounds to {value}"


def fraction_arithmetic_problems(body: str) -> list[tuple[int, str]]:
    """Every `a/b = d.ddd` in `body`, checked by `check_rung_figures`'s own exact rule --
    imported rather than reimplemented, so the two checkers can never disagree about what
    "arithmetically true" means. Returns `(character_offset, message)` pairs.
    """
    problems: list[tuple[int, str]] = []
    for match in _FRACTION_EQUALS_DECIMAL.finditer(body):
        numerator, denominator, stated = match.groups()
        value = Fraction(int(numerator), int(denominator))
        if not decimal_matches(value, stated):
            digits = _digits_of(stated)
            message = (
                f"{numerator}/{denominator} = {stated} is wrong; "
                f"rounds to {round_to(value, digits)}"
            )
            problems.append((match.start(), message))
    return problems


@dataclass(frozen=True, slots=True)
class Finding:
    """One disagreement between a case's prose and its own front matter or arithmetic."""

    path: Path
    line: int
    check: str
    """"bound-figure", "verified-field", or "fraction-arithmetic"."""
    detail: str

    def render(self) -> str:
        try:
            location = self.path.relative_to(REPO)
        except ValueError:
            location = self.path
        return f"{location}:{self.line}: [{self.check}] {self.detail}"


def _line_at(body_start_line: int, body: str, offset: int) -> int:
    return body_start_line + body.count("\n", 0, offset)


def check_case_file(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    front_matter_yaml, body, body_start_line = split_front_matter(text)
    document = safe_load(front_matter_yaml)
    front_matter = parse_front_matter(document)

    findings: list[Finding] = []
    for claim in bound_claims(body, front_matter.n):
        problem = check_bound_claim(claim, front_matter)
        if problem is not None:
            line = _line_at(body_start_line, body, claim.offset)
            findings.append(Finding(path, line, "bound-figure", problem))
    for field_claim in verified_field_claims(body):
        problem = check_verified_field_claim(field_claim, front_matter)
        if problem is not None:
            line = _line_at(body_start_line, body, field_claim.offset)
            findings.append(Finding(path, line, "verified-field", problem))
    for offset, message in fraction_arithmetic_problems(body):
        line = _line_at(body_start_line, body, offset)
        findings.append(Finding(path, line, "fraction-arithmetic", message))
    return findings


def _field_for_rewrite(claim: BoundClaim, front_matter: CaseFrontMatter) -> BoundField | None:
    lower = claim.kind == "lower"
    verified = front_matter.verified_lower if lower else front_matter.verified_upper
    reported = front_matter.reported_lower if lower else front_matter.reported_upper
    if claim.provenance == "verified":
        return verified
    if claim.provenance == "reported":
        return reported
    stated, digits = _stated_decimal(claim.figure)
    if verified.decimal_at(digits) == stated:
        return verified
    if reported.decimal_at(digits) == stated:
        return reported
    return None


def rewrite_directionally_safe_figures(path: Path) -> int:
    """Rewrite nearest-rounded bound decimals so every displayed inequality stays true."""
    text = path.read_text(encoding="utf-8")
    front_matter_yaml, body, _body_start_line = split_front_matter(text)
    front_matter = parse_front_matter(safe_load(front_matter_yaml))
    replacements: dict[int, tuple[int, str]] = {}

    for claim in bound_claims(body, front_matter.n):
        if "/" in claim.figure or check_bound_claim(claim, front_matter) is None:
            continue
        field = _field_for_rewrite(claim, front_matter)
        if field is None:
            continue
        rendered = field.safe_decimal_at(_digits_of(claim.figure), claim.kind)
        if rendered is not None:
            replacements[claim.offset] = (len(claim.figure), format(rendered, "f"))

    for claim in verified_field_claims(body):
        if check_verified_field_claim(claim, front_matter) is None:
            continue
        field = (
            front_matter.verified_lower
            if claim.kind == "lower"
            else front_matter.verified_upper
        )
        rendered = field.safe_decimal_at(_digits_of(claim.figure), claim.kind)
        if rendered is not None:
            replacements[claim.offset] = (len(claim.figure), format(rendered, "f"))

    for offset, (length, rendered) in sorted(replacements.items(), reverse=True):
        body = body[:offset] + rendered + body[offset + length :]
    if replacements:
        prefix = text[: len(text) - len(split_front_matter(text)[1])]
        path.write_text(prefix + body, encoding="utf-8")
    return len(replacements)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fix",
        action="store_true",
        help="rewrite nearest-rounded inequality figures in the conservative direction",
    )
    args = parser.parse_args()
    paths = sorted(FRONTIER.glob("n-*.md"))
    if args.fix:
        rewritten = sum(rewrite_directionally_safe_figures(path) for path in paths)
        print(f"  rewrote {rewritten} bound figure(s) in the conservative direction")
    findings: list[Finding] = []
    for path in paths:
        findings.extend(check_case_file(path))

    if findings:
        print(f"{len(findings)} case-prose disagreement(s) with front matter or arithmetic:")
        for finding in findings:
            print(f"  {finding.render()}")
        return 1
    print(
        f"  {len(paths)} case files checked, every quoted bound figure and fraction-decimal "
        "claim in their prose agrees with their own front matter"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
