"""Göbel's construction beyond n = 324, from the maintained module, against the retained one.

`devtools.goebel_construction` builds Göbel's three families to a limit with loop bounds
derived from it, and proves each side final by the area bound: a member at count k packs k
unit squares, so its side is at least sqrt(k). The 15 October packet's retained program,
read by its path and never run from its packet directory, stays the regression oracle.
The refusals come first: the retained loops raised past their limit, and a count no build
proves (think-llit's plan, Göbel's Construction Beyond 1073).
"""

from __future__ import annotations

import importlib.util
import math
import re
from fractions import Fraction
from types import ModuleType
from typing import Any

import pytest

from devtools import goebel_construction as goebel

CATALOGUE = "resources/web/kingbird-squares-in-squares-2026-08-22.md"


def _retained() -> ModuleType:
    """The retained program, loaded from its path; nothing runs from its directory."""
    from devtools.intake_ledger import GOEBEL_PROGRAM  # noqa: PLC0415

    spec = importlib.util.spec_from_file_location("goebel_beyond_horizon", GOEBEL_PROGRAM)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _key(form: Any) -> tuple[Fraction, Fraction, str, int]:
    """A member of either program as its side, family and count."""
    return (Fraction(form.p), Fraction(form.q), str(form.family), int(form.count))


def _side(form: goebel.Form | None) -> tuple[Fraction, Fraction]:
    assert form is not None
    return (form.p, form.q)


def test_the_retained_loops_raised_to_10500_are_refused_at_1573_counts() -> None:
    """The retained loops stop at a < 40 and b < 80, so no strip is built above 1617: raised
    to 10,500 they give a side that is too large at 1,573 counts from 1682 to 6116, and none
    above 6256. A row between that side and Göbel's true one would have been recorded."""
    program = _retained()
    raised = [goebel.Form(*_key(form)) for form in program.families(10_500)]
    built = goebel.least_table(raised, 10_500)
    assert max(form.count for form in raised if form.family != goebel.SQUARE) == 1617
    wrong = [
        n
        for n in range(goebel.HORIZON + 1, 10_501)
        if built[n] is not None and _side(built[n]) != _side(goebel.side(n))
    ]
    assert len(wrong) == 1573
    assert (wrong[0], wrong[-1]) == (1682, 6116)
    assert all(_side(goebel.side(n)) != _side(built[n]) for n in wrong)
    assert all(goebel.less(goebel.side(n), form) for n in wrong if (form := built[n]))
    assert next(n for n in range(goebel.HORIZON + 1, 10_501) if built[n] is None) == 6257


def test_a_count_no_build_proves_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    """The retained program's limit of 1100 proves no side from 1039 to 1073: its reach was
    its largest member, not a proof. With every build capped there, 1074 is refused rather
    than read as Göbel's, and so is 1073; the default builds prove both."""
    assert goebel.reach(1100) == 1038
    assert not goebel.proved(1039, 1100)
    monkeypatch.setattr(goebel, "MAX_BUILD", 1100)
    for n in (1039, 1073, 1074, 10_000):
        assert not goebel.proved(n)
        with pytest.raises(goebel.GoebelError, match=rf"n = {n}: no build to 1100 proves"):
            goebel.side(n)
    assert _side(goebel.side(1038)) == _side(goebel.table(1100)[1038])
    monkeypatch.undo()
    assert goebel.proved(1073)
    assert goebel.proved(1074)


def test_a_build_holds_every_member_its_limit_admits() -> None:
    """The derived bounds miss nothing: wider loops with the families' own conditions find
    no other member at or below the limit, and the members come in the retained order."""
    for limit in (1100, 4000, 10_500):
        wide = []
        top = 2 * math.isqrt(limit) + 5
        for a in range(1, top):
            for b in range(1, top):
                n = 2 * (a + 1) * a + b * b
                if 2 * (a - 1) ** 2 < b * b < 2 * (a + 1) ** 2 and n <= limit:
                    wide.append((a + 1, Fraction(b, 2), goebel.SQUARE, n))
            b = 1 + math.isqrt(2 * (a - 1) ** 2)
            if (a + 1) * a + 2 + b <= limit:
                wide.append((a + 1, Fraction(1, 2), goebel.STRIP, (a + 1) * a + 2 + b))
            if 18 <= (a + 1) * a + 3 + b <= limit:
                wide.append((2, Fraction(b + 1, 2), goebel.CORNER, (a + 1) * a + 3 + b))
        assert [_key(form) for form in goebel.families(limit)] == [
            (Fraction(p), q, family, n) for p, q, family, n in wide
        ]


def test_the_module_agrees_with_the_retained_program_to_1073() -> None:
    """At every count to 1073, the least member at or above it is the retained program's:
    the same side, family and count, so every frozen start and claim record reads the same
    construction from either. To 1100 the two build the same members in the same order."""
    program = _retained()
    forms = program.families(program.LIMIT)
    assert [_key(form) for form in forms] == [_key(form) for form in goebel.families(1100)]
    assert max(form.count for form in forms) == 1073
    for n in range(1, 1074):
        assert _key(program.goebel_at(n, forms)) == _key(goebel.side(n)), n


def test_every_count_to_10000_is_proved_final_by_the_area_bound() -> None:
    """The build to 10,500 holds 343 members, the largest at 10,488, and proves every count
    from 325 to 10,345 final; the first it cannot is 10,346, which the next build proves."""
    members = goebel.families(goebel.BUILD)
    assert (len(members), max(form.count for form in members)) == (343, 10_488)
    assert goebel.reach() == 10_345
    assert all(goebel.proved(n, goebel.BUILD) for n in range(goebel.HORIZON + 1, 10_001))
    assert not goebel.proved(10_346, goebel.BUILD)
    assert goebel.build_for(10_346) == 2 * goebel.BUILD
    assert goebel.side(10_000).text() == "51 + 35*sqrt(2)"
    for n in (10_000, 10_345):
        form = goebel.side(n)
        assert goebel.final(form, goebel.BUILD)
        assert float(form.p) + float(form.q) * math.sqrt(2) >= math.sqrt(n)


def test_the_catalogue_s_words_and_sides_beyond_1024() -> None:
    """The Kingbird capture of 22 August says 1765 "Beats the s(1765) Göbel square" and 2043
    "Beats the s(2043) Göbel strip"; the module picks those forms, and each of the four
    catalogue sides above 1024 is below it by the margins think-llit's plan states."""
    from devtools.intake_ledger import ROOT  # noqa: PLC0415

    text = (ROOT / CATALOGUE).read_text(encoding="utf-8")
    assert "Beats the $s(1765)$ [Göbel square]" in text
    assert "Beats the $s(2043)$ [Göbel strip]" in text
    assert (goebel.side(1765).family, goebel.side(1765).count) == (goebel.SQUARE, 1765)
    assert goebel.side(1765).text() == "22 + 29/2*sqrt(2)"
    assert (goebel.side(2043).family, goebel.side(2043).count) == (goebel.STRIP, 2043)
    assert goebel.side(2043).text() == "45 + 1/2*sqrt(2)"
    margins = {1453: "0.079", 1765: "0.018", 1850: "0.218", 2043: "0.011"}
    for n, margin in margins.items():
        block = text.split(f"\n{n}  \n", 1)[1]
        match = re.search(r"\\Nn\{([0-9.]+)\}", block)
        assert match is not None
        printed = Fraction(match[1])
        assert goebel.sign(printed, goebel.side(n)) == -1
        assert round(-goebel.side(n).margin(printed), 3) == float(margin), n


def test_daniel_s_1092_and_1228_are_above_the_construction() -> None:
    """At 1092 the side is Göbel's strip of 1102 less 10, 33 + sqrt(2)/2; at 1228 the
    square of 1237 less 9, 18 + 25 sqrt(2)/2 (think-jtlq): Daniel's prints are above both."""
    strip, square = goebel.side(1092), goebel.side(1228)
    assert (strip.text(), strip.family, strip.count) == ("33 + 1/2*sqrt(2)", goebel.STRIP, 1102)
    assert (square.text(), square.family, square.count) == (
        "18 + 25/2*sqrt(2)",
        goebel.SQUARE,
        1237,
    )
    assert goebel.sign(Fraction("33.840529687178261"), strip) == 1
    assert goebel.sign(Fraction("35.847313543154434"), square) == 1


def test_a_comparison_reads_the_sign_exactly() -> None:
    """The comparison a receipt writes: the relation by exact sign, never by the float."""
    form = goebel.side(2043)
    exact = 45 + Fraction(1, 2) * Fraction(math.isqrt(2 * 10**60), 10**30)
    result = goebel.compare("sample", [(2043, exact, "a"), (2043, Fraction(46), "b")])
    assert [item["relation"] for item in result["detail"]] == ["below", "above"]
    assert result["tally"] == {"above": 1, "equal": 0, "below": 1}
    assert result["above"] == [2043]
    assert result["detail"][0]["goebel"] == form.text()


def test_a_larger_build_picks_the_same_member_at_every_proved_count() -> None:
    """Review B, B5: a side the build to `BUILD` proves final is the one twice that build
    gives, member for member, at every count to `reach`: the same side, family and count,
    so the member a receipt names does not depend on the build that proved it."""
    first, second = goebel.table(goebel.BUILD), goebel.table(2 * goebel.BUILD)
    for n in range(goebel.HORIZON + 1, goebel.reach() + 1):
        assert first[n] == second[n], n
