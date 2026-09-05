"""A case's prose must still say what its own front matter says, after the front matter moves.

`n-017.md`, `n-018.md` and `n-019.md` all once stated "The verified lower bound is `s(17)
>= 22529/5000 = 4.5058`" in prose while their own front matter's `verified_lower_bound` had
already moved to `4.59` -- the defect `check_case_prose.py` answers. These tests reconstruct
that shape (and the module's other three recognised shapes, and the historical-mention
exemption, and the repository-wide fraction-arithmetic rule it shares with
`check_rung_figures`) as synthetic fixtures written to `tmp_path`, never as edits to a real
`frontier/n-*.md` -- those files are live records other work is in flight against.
"""

from __future__ import annotations

from itertools import pairwise
from pathlib import Path

import pytest

from devtools.check_case_prose import (
    BoundClaim,
    BoundField,
    CaseFrontMatter,
    check_bound_claim,
    check_case_file,
    sentence_spans,
    split_front_matter,
)

_Bounds = dict[str, tuple[str, str | None] | None]


def _field_yaml(name: str, bound: tuple[str, str | None] | None) -> str:
    if bound is None:
        return f"  {name}: {{}}\n"
    value, exact_form = bound
    exact_line = "null" if exact_form is None else exact_form
    return f"  {name}:\n    value: '{value}'\n    exact_form: {exact_line}\n"


def make_case(tmp_path: Path, filename: str, n: int, bounds: _Bounds, body: str) -> Path:
    """Write a minimal, synthetic `n-*.md`-shaped file: just enough front matter for
    `check_case_file` to read, plus whatever prose body the test wants checked.
    """
    front_matter = (
        "---\ntitle: synthetic test case\npacking:\n"
        f"  n: {n}\n"
        + _field_yaml("verified_lower_bound", bounds.get("verified_lower_bound"))
        + _field_yaml("verified_upper_bound", bounds.get("verified_upper_bound"))
        + _field_yaml("reported_lower_bound", bounds.get("reported_lower_bound"))
        + _field_yaml("reported_upper_bound", bounds.get("reported_upper_bound"))
        + "---\n"
    )
    path = tmp_path / filename
    path.write_text(front_matter + body, encoding="utf-8")
    return path


# The front matter every "n = 17/18/19, verified_lower_bound now 4.59" fixture below shares:
# a plain rational verified lower bound, a Nagamochi reported lower bound too weak to match
# the stale figure either, and upper bounds that no test in this module exercises.
_N17_STYLE_BOUNDS: _Bounds = {
    "verified_lower_bound": ("4.59", "459/100"),
    "verified_upper_bound": ("5", "5"),
    "reported_lower_bound": ("4.16", None),
    "reported_upper_bound": ("5", "5"),
}


@pytest.mark.parametrize(
    ("n", "stale_sentence", "fixed_sentence"),
    [
        (
            17,
            (
                "The verified lower bound is `s(17) ≥ 22529/5000 = 4.5058`, adopted "
                "from a prior certificate."
            ),
            (
                "The verified lower bound is `s(17) ≥ 459/100 = 4.59`, from this "
                "repository's own certificate."
            ),
        ),
        (
            18,
            (
                "The verified lower bound is `s(18) ≥ s(17) ≥ 22529/5000 = 4.5058`, "
                "inherited by monotonicity from the n = 17 certificate."
            ),
            (
                "The verified lower bound is `s(18) ≥ 459/100 = 4.59`, from this "
                "repository's own weighted fractional unavoidable-set certificate."
            ),
        ),
        (
            19,
            (
                "The verified lower bound is `s(19) ≥ s(17) ≥ 22529/5000 = 4.5058`, "
                "and the same certificate carries `s(19) ≥ 4.5058` by monotonicity."
            ),
            (
                "The verified lower bound is `s(19) ≥ 459/100 = 4.59`, and the same "
                "certificate carries `s(19) ≥ 4.59` directly."
            ),
        ),
    ],
)
def test_the_three_historical_stale_bodies_fail_and_their_fixes_pass(
    tmp_path: Path, n: int, stale_sentence: str, fixed_sentence: str
) -> None:
    stale_body = f"# case\n\n{stale_sentence}\n"
    stale = make_case(tmp_path, f"n-{n:03d}-stale.md", n, _N17_STYLE_BOUNDS, stale_body)
    stale_findings = check_case_file(stale)
    assert any(finding.check == "bound-figure" for finding in stale_findings), stale_findings
    assert any("4.5058" in finding.detail for finding in stale_findings)

    fixed_body = f"# case\n\n{fixed_sentence}\n"
    fixed = make_case(tmp_path, f"n-{n:03d}-fixed.md", n, _N17_STYLE_BOUNDS, fixed_body)
    assert check_case_file(fixed) == []


def test_historical_mention_of_a_weaker_value_is_allowed_only_when_marked(
    tmp_path: Path,
) -> None:
    """`n-020`'s own real shape: "Nagamochi's general `1 + √12 ≈ 4.4641`" is
    strictly weaker than a `4.8` verified lower bound. Marked historical, in the same
    sentence, it is a case describing its own history and must pass; unmarked, the same
    figure is indistinguishable from a stale claim and must fail.
    """
    bounds: _Bounds = {
        "verified_lower_bound": ("4.8", "24/5"),
        "verified_upper_bound": ("5", "5"),
        "reported_lower_bound": None,
        "reported_upper_bound": ("5", "5"),
    }
    marked = make_case(
        tmp_path,
        "n-marked.md",
        20,
        bounds,
        "# case\n\nNagamochi's general `1 + √12 ≈ 4.4641`, now weaker than the "
        "retained bound.\n",
    )
    assert check_case_file(marked) == []

    unmarked = make_case(
        tmp_path,
        "n-unmarked.md",
        20,
        bounds,
        "# case\n\nNagamochi's general `1 + √12 ≈ 4.4641`, which remains a candidate figure.\n",
    )
    findings = check_case_file(unmarked)
    assert len(findings) == 1
    assert "4.4641" in findings[0].detail
    assert findings[0].check == "bound-figure"


def test_upper_bound_figure_checked_the_same_way_both_directions(tmp_path: Path) -> None:
    bounds: _Bounds = {
        "verified_lower_bound": ("4.5", "9/2"),
        "verified_upper_bound": ("5.5", "11/2"),
        "reported_lower_bound": ("4.5", "9/2"),
        "reported_upper_bound": ("5.25", None),
    }

    # Matches verified_upper_bound directly.
    matches_verified = make_case(
        tmp_path,
        "n-upper-verified.md",
        30,
        bounds,
        "# case\n\nThe best known packing gives `s(30) ≤ 5.5`.\n",
    )
    assert check_case_file(matches_verified) == []

    # Matches only reported_upper_bound -- the "found by" citation of an unverified tighter
    # construction, which must not be flagged just because it disagrees with `verified`.
    matches_reported = make_case(
        tmp_path,
        "n-upper-reported.md",
        30,
        bounds,
        "# case\n\n`s(30) ≤ 5.25`, found by a construction with no formal certificate.\n",
    )
    assert check_case_file(matches_reported) == []

    # Matches neither -- a genuinely stale or wrong figure.
    matches_neither = make_case(
        tmp_path,
        "n-upper-bad.md",
        30,
        bounds,
        "# case\n\nThe best known packing gives `s(30) ≤ 5.9`.\n",
    )
    findings = check_case_file(matches_neither)
    assert len(findings) == 1
    assert findings[0].check == "bound-figure"
    assert "5.9" in findings[0].detail


def test_verified_field_anchor_has_no_reported_fallback_or_exemption(tmp_path: Path) -> None:
    """The ceiling-disclaimer's own "`verified_upper_bound` for this case is `X`" sentence
    names the field directly, so `X` must equal `verified_upper_bound` exactly -- agreeing
    with `reported_upper_bound` instead does not save it, unlike the generic `s(n) <=` shape.
    """
    bounds: _Bounds = {
        "verified_lower_bound": ("4.5", "9/2"),
        "verified_upper_bound": ("6", "6"),
        "reported_lower_bound": None,
        "reported_upper_bound": ("5.5", None),
    }
    wrong = make_case(
        tmp_path,
        "n-anchor-wrong.md",
        40,
        bounds,
        "# case\n\n`verified_upper_bound` for this case is `5.5`, larger than reported.\n",
    )
    findings = check_case_file(wrong)
    assert len(findings) == 1
    assert findings[0].check == "verified-field"

    right = make_case(
        tmp_path,
        "n-anchor-right.md",
        40,
        bounds,
        "# case\n\n`verified_upper_bound` for this case is `6`, the trivial grid ceiling.\n",
    )
    assert check_case_file(right) == []


def test_a_false_fraction_equals_decimal_in_a_case_body_fails(tmp_path: Path) -> None:
    """`check_rung_figures`'s own rule, reused: any `a/b = d.ddd` must be arithmetically
    true, regardless of whether it names a bound on this file's own `n` at all.
    """
    bounds: _Bounds = {
        "verified_lower_bound": ("3.8", "19/5"),
        "verified_upper_bound": ("5", "5"),
        "reported_lower_bound": None,
        "reported_upper_bound": ("5", "5"),
    }
    path = make_case(
        tmp_path,
        "n-frac.md",
        11,
        bounds,
        "# case\n\nA calibration rung is retained at `189/50 = 3.79`, below the bound.\n",
    )
    findings = check_case_file(path)
    assert len(findings) == 1
    assert findings[0].check == "fraction-arithmetic"
    assert "189/50 = 3.79 is wrong" in findings[0].detail

    true_path = make_case(
        tmp_path,
        "n-frac-true.md",
        11,
        bounds,
        "# case\n\nA calibration rung is retained at `189/50 = 3.78`, below the bound.\n",
    )
    assert check_case_file(true_path) == []


def test_split_front_matter_reports_the_bodys_real_starting_line() -> None:
    text = "---\ntitle: x\npacking:\n  n: 1\n---\nfirst body line\nsecond body line\n"
    front_matter, body, body_start_line = split_front_matter(text)
    assert "n: 1" in front_matter
    assert body == "first body line\nsecond body line\n"
    assert body_start_line == 6


def test_sentence_spans_cover_the_whole_text_and_split_on_period_capital() -> None:
    text = "First sentence. Second sentence continues\nacross a line wrap. Third."
    spans = sentence_spans(text)
    sentences = [text[start:end] for start, end in spans]
    assert sentences == [
        "First sentence.",
        "Second sentence continues\nacross a line wrap.",
        "Third.",
    ]
    # The spans run start-to-end over the whole text, in order, each strictly after the
    # last (the inter-sentence whitespace itself belongs to neither span).
    assert spans[0][0] == 0
    assert spans[-1][1] == len(text)
    assert all(a[1] <= b[0] for a, b in pairwise(spans))


def test_bound_field_decimal_at_prefers_exact_fraction_over_the_value_string() -> None:
    exact = BoundField(value="4.590000000001", exact_form="459/100")
    # The value string alone would round to 4.5900 too, but this checks the Fraction path
    # is actually taken: 459/100 is exactly 4.59, no matter what the value string says.
    assert exact.decimal_at(2) == exact.decimal_at(2)
    assert str(exact.decimal_at(4)) == "4.5900"

    irrational = BoundField(value="4.82287565553229", exact_form="(7/2) + (1/2)sqrt(7)")
    assert str(irrational.decimal_at(6)) == "4.822876"

    unset = BoundField(value=None, exact_form=None)
    assert unset.decimal_at(4) is None


def test_check_bound_claim_treats_a_none_reported_bound_as_no_fallback() -> None:
    front_matter = CaseFrontMatter(
        n=99,
        verified_lower=BoundField("4.0", "4"),
        verified_upper=BoundField("5.0", "5"),
        reported_lower=BoundField(None, None),
        reported_upper=BoundField(None, None),
    )
    claim = BoundClaim("lower", "3.9", offset=0, sentence="s(99) is at least 3.9.")
    problem = check_bound_claim(claim, front_matter)
    assert problem is not None
    assert "3.9" in problem


def test_a_pinned_interval_is_read_as_a_lower_and_an_upper_bound(tmp_path: Path) -> None:
    """D-445: the n = 11 body wrote "`s(11)` is pinned to `[3.8, 3.877084]`" and stayed on
    the 19/5 rung for eleven hours under front matter that said 381/100, because no
    pattern here read an interval. Both endpoints are bounds on the file's own n.
    """
    bounds: _Bounds = {
        "verified_lower_bound": ("3.81", "381/100"),
        "verified_upper_bound": ("3.87708433", "root of the degree-8 polynomial"),
        "reported_lower_bound": ("3.788854", None),
        "reported_upper_bound": ("3.877084", None),
    }
    stale = make_case(
        tmp_path,
        "n-011-stale.md",
        11,
        bounds,
        "# case\n\n`s(11)` is pinned to `[3.8, 3.877084]`, a gap of `0.077084`.\n",
    )
    findings = check_case_file(stale)
    # 3.8 is 3.81 written to one decimal and passes as such; the gap is what gives
    # the stale body away, exactly as it did in the record.
    assert len(findings) == 1
    assert findings[0].check == "bound-figure"
    assert "0.077084" in findings[0].detail and "0.067084" in findings[0].detail

    two_decimals = make_case(
        tmp_path,
        "n-011-two-decimals.md",
        11,
        bounds,
        "# case\n\n`s(11)` is pinned to `[3.80, 3.877084]`, a gap of `0.067084`.\n",
    )
    findings = check_case_file(two_decimals)
    assert len(findings) == 1
    assert "3.80" in findings[0].detail

    current = make_case(
        tmp_path,
        "n-011-current.md",
        11,
        bounds,
        "# case\n\n`s(11)` is pinned to `[3.81, 3.877084]`, a gap of `0.067084`.\n",
    )
    assert check_case_file(current) == []

    # An interval on another case's n is not this file's claim.
    other = make_case(
        tmp_path,
        "n-011-other.md",
        11,
        bounds,
        "# case\n\nBy contrast `s(12)` is pinned to `[3.96, 4]`.\n",
    )
    assert check_case_file(other) == []
