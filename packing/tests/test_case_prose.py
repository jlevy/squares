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

from decimal import Decimal
from itertools import pairwise
from pathlib import Path

import pytest

from devtools.check_case_prose import (
    BoundClaim,
    BoundField,
    CaseFrontMatter,
    check_bound_claim,
    check_case_file,
    rewrite_directionally_safe_figures,
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

    marker_in_later_sentence = make_case(
        tmp_path,
        "n-later-marker.md",
        20,
        bounds,
        (
            "# case\n\nA candidate says `s(20) ≥ 4.4641`. "
            "The old method was useful.\n"
        ),
    )
    findings = check_case_file(marker_in_later_sentence)
    assert len(findings) == 1
    assert "4.4641" in findings[0].detail


def test_nearest_preceding_provenance_anchor_wins_within_one_paragraph(
    tmp_path: Path,
) -> None:
    bounds: _Bounds = {
        "verified_lower_bound": ("4.8", "24/5"),
        "verified_upper_bound": ("5", "5"),
        "reported_lower_bound": ("4.7438", None),
        "reported_upper_bound": ("5", "5"),
    }
    path = make_case(
        tmp_path,
        "n-two-provenances.md",
        21,
        bounds,
        (
            "# case\n\nThe verified lower bound is `s(21) ≥ 4.8`; the reported lower "
            "bound is `s(21) ≥ 4.7438`.\n"
        ),
    )
    assert check_case_file(path) == []


def test_upper_bound_provenance_selects_the_right_front_matter_field(tmp_path: Path) -> None:
    bounds: _Bounds = {
        "verified_lower_bound": ("4.5", "9/2"),
        "verified_upper_bound": ("5.5", "11/2"),
        "reported_lower_bound": ("4.5", "9/2"),
        "reported_upper_bound": ("5.25", None),
    }

    # Explicitly verified prose matches verified_upper_bound directly.
    matches_verified = make_case(
        tmp_path,
        "n-upper-verified.md",
        30,
        bounds,
        "# case\n\nThe verified upper bound is `s(30) ≤ 5.5`.\n",
    )
    assert check_case_file(matches_verified) == []

    # "Best known packing" means the reported field, not whichever field happens to match.
    wrongly_matches_only_verified = make_case(
        tmp_path,
        "n-upper-wrong-provenance.md",
        30,
        bounds,
        "# case\n\nThe best known packing gives `s(30) ≤ 5.5`.\n",
    )
    findings = check_case_file(wrongly_matches_only_verified)
    assert len(findings) == 1
    assert "reported field" in findings[0].detail

    # The same reported wording accepts the tighter reported construction.
    matches_reported = make_case(
        tmp_path,
        "n-upper-reported.md",
        30,
        bounds,
        "# case\n\nThe best known packing gives `s(30) ≤ 5.25`.\n",
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

    unsafe_rounded_lower = make_case(
        tmp_path,
        "n-anchor-rounded-lower.md",
        40,
        {
            **bounds,
            "verified_lower_bound": ("4.8", "24/5"),
        },
        "# case\n\n`verified_lower_bound` for this case is `5`.\n",
    )
    assert len(check_case_file(unsafe_rounded_lower)) == 1

    unsafe_rounded_upper = make_case(
        tmp_path,
        "n-anchor-rounded-upper.md",
        40,
        {
            **bounds,
            "verified_upper_bound": ("5.25", "21/4"),
        },
        "# case\n\n`verified_upper_bound` for this case is `5`.\n",
    )
    assert len(check_case_file(unsafe_rounded_upper)) == 1


def test_verified_bound_words_have_no_reported_fallback(tmp_path: Path) -> None:
    """A reported value must not rescue a sentence that explicitly calls it verified."""
    bounds: _Bounds = {
        "verified_lower_bound": ("4.8", "24/5"),
        "verified_upper_bound": ("5", "5"),
        "reported_lower_bound": ("4.605551", None),
        "reported_upper_bound": ("5", "5"),
    }
    stale = make_case(
        tmp_path,
        "n-verified-fallback.md",
        20,
        bounds,
        "# case\n\nThe verified lower bound is `s(20) ≥ 4.605551`.\n",
    )
    findings = check_case_file(stale)
    assert len(findings) == 1
    assert findings[0].check == "bound-figure"
    assert "4.605551" in findings[0].detail

    sentence_global_marker = make_case(
        tmp_path,
        "n-verified-history-bypass.md",
        20,
        bounds,
        "# case\n\nThe verified lower bound is `s(20) ≥ 4.6`, and the old method was useful.\n",
    )
    findings = check_case_file(sentence_global_marker)
    assert len(findings) == 1
    assert "verified field" in findings[0].detail


def test_best_proved_words_have_no_reported_fallback(tmp_path: Path) -> None:
    bounds: _Bounds = {
        "verified_lower_bound": ("4.8", "24/5"),
        "verified_upper_bound": ("5", "5"),
        "reported_lower_bound": ("4.7438", None),
        "reported_upper_bound": ("5", "5"),
    }
    stale = make_case(
        tmp_path,
        "n-best-proved-fallback.md",
        21,
        bounds,
        "# case\n\nThe best proved lower bound is `4.7438`.\n",
    )
    findings = check_case_file(stale)
    assert len(findings) == 1
    assert "verified field" in findings[0].detail

    direct = make_case(
        tmp_path,
        "n-best-proved-direct-fallback.md",
        21,
        bounds,
        "# case\n\nThe best proved lower bound is `s(21) ≥ 4.7438`.\n",
    )
    findings = check_case_file(direct)
    assert len(findings) == 1
    assert "verified field" in findings[0].detail


def test_bare_verified_bound_value_is_checked(tmp_path: Path) -> None:
    bounds: _Bounds = {
        "verified_lower_bound": ("4.59", "459/100"),
        "verified_upper_bound": ("5", "5"),
        "reported_lower_bound": ("4.5058", None),
        "reported_upper_bound": ("5", "5"),
    }
    stale = make_case(
        tmp_path,
        "n-bare-verified-stale.md",
        18,
        bounds,
        "# case\n\nIt is weaker here than the verified `4.5058` bound recorded above.\n",
    )
    findings = check_case_file(stale)
    assert len(findings) == 1
    assert "verified field" in findings[0].detail

    current = make_case(
        tmp_path,
        "n-bare-verified-current.md",
        18,
        bounds,
        "# case\n\nThe old value is weaker than the verified `4.59` bound recorded above.\n",
    )
    assert check_case_file(current) == []


def test_exact_only_rational_is_not_partially_parsed_as_an_integer(tmp_path: Path) -> None:
    bounds: _Bounds = {
        "verified_lower_bound": ("4.8", "24/5"),
        "verified_upper_bound": ("5", "5"),
        "reported_lower_bound": None,
        "reported_upper_bound": ("5", "5"),
    }
    exact = make_case(
        tmp_path,
        "n-exact-rational.md",
        20,
        bounds,
        "# case\n\nThe verified lower bound is `s(20) ≥ 24/5`.\n",
    )
    assert check_case_file(exact) == []


def test_decimal_bound_rendering_is_directionally_safe(tmp_path: Path) -> None:
    bounds: _Bounds = {
        "verified_lower_bound": ("4.8", "24/5"),
        "verified_upper_bound": ("4.8", "24/5"),
        "reported_lower_bound": None,
        "reported_upper_bound": None,
    }
    unsafe_lower = make_case(
        tmp_path,
        "n-unsafe-rounded-lower.md",
        20,
        bounds,
        "# case\n\nThe verified lower bound is `s(20) ≥ 5`.\n",
    )
    assert len(check_case_file(unsafe_lower)) == 1

    safe_lower = make_case(
        tmp_path,
        "n-safe-rounded-lower.md",
        20,
        bounds,
        "# case\n\nThe verified lower bound is `s(20) ≥ 4`.\n",
    )
    assert check_case_file(safe_lower) == []

    unsafe_upper = make_case(
        tmp_path,
        "n-unsafe-rounded-upper.md",
        20,
        bounds,
        "# case\n\nThe verified upper bound is `s(20) ≤ 4`.\n",
    )
    assert len(check_case_file(unsafe_upper)) == 1

    safe_upper = make_case(
        tmp_path,
        "n-safe-rounded-upper.md",
        20,
        bounds,
        "# case\n\nThe verified upper bound is `s(20) ≤ 5`.\n",
    )
    assert check_case_file(safe_upper) == []


def test_fix_rewrites_nearest_decimals_without_strengthening_bounds(tmp_path: Path) -> None:
    bounds: _Bounds = {
        "verified_lower_bound": ("4.605551775464", None),
        "verified_upper_bound": ("4.88561808316412", None),
        "reported_lower_bound": ("4.605551775464", None),
        "reported_upper_bound": ("4.88561808316412", None),
    }
    path = make_case(
        tmp_path,
        "n-directional-fix.md",
        20,
        bounds,
        (
            "# case\n\nThe best known packing gives `s(20) ≤ 4.88561808`, and the "
            "best proved lower bound is `4.605552`.\n"
        ),
    )
    assert len(check_case_file(path)) == 2
    assert rewrite_directionally_safe_figures(path) == 2
    assert check_case_file(path) == []
    text = path.read_text(encoding="utf-8")
    assert "s(20) ≤ 4.88561809" in text
    assert "best proved lower bound is `4.605551`" in text


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
    exact = BoundField(value="4.58", exact_form="459/100")
    # The deliberately disagreeing value string proves that the exact-form path is used.
    assert exact.decimal_at(2) == Decimal("4.59")
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
