"""Source arithmetic is exact; missing source proofs remain outside the verified lane."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
import sympy as sp
import yaml

from devtools import audit_ds7_lower_bounds as ds7
from sqpack.yamlio import load_yaml

REPO = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    ("k", "expected"),
    [
        (4, "(19+40sqrt(2))/17"),
        (5, "2sqrt(2)+(27+2sqrt(10))/13"),
        (6, "2sqrt(2)+(113+10sqrt(3))/37"),
        (9, "(247+94sqrt(2))/41"),
        (10, "2sqrt(2)+(709+18sqrt(5))/101"),
        (16, "(3343+574sqrt(2))/257"),
    ],
)
def test_general_theorem_matches_source_specializations(k: int, expected: str) -> None:
    assert ds7.compare(ds7.green(k), ds7.exact_parse(expected))["sign"] == 0
    lo, hi = ds7.enclosure(ds7.green(k), 24)
    assert lo < hi
    assert hi - lo < sp.Rational(1, 10**22)


@pytest.mark.parametrize(
    "expression",
    ["x+1", "sin(1)", "__import__('os')", "sqrt(x)", "sqrt(-1)", "1/0", "True"],
)
def test_parser_refuses_unsupported_or_nonreal_expressions(expression: str) -> None:
    with pytest.raises(ValueError, match="expression"):
        ds7.exact_parse(expression)


def test_comparison_uses_exact_signs_and_refuses_unsupported_radicals() -> None:
    above = ds7.exact_parse("sqrt(2)+1/10^50")
    result = ds7.compare(above, ds7.exact_parse("sqrt(2)"))
    assert result["sign"] == 1
    assert ds7.compare(-above, -ds7.exact_parse("sqrt(2)"))["sign"] == -1
    with pytest.raises(ValueError, match="unsupported exact enclosure"):
        ds7.compare(sp.real_root(2, 3), sp.Integer(1))


def test_theorem10_floor_threshold_and_unexplained_table_tension() -> None:
    seeds = {c.k: c for c in ds7.candidates() if c.theorem == 10}
    assert seeds[4].base_n == 19
    assert seeds[5].base_n == 28  # floor(5/2), not ceiling or a real-valued half.
    assert ds7.compare(seeds[4].expression, ds7.exact_parse("6sqrt(2)-4"))["sign"] == 1
    for n in (19, 20):
        chosen = ds7.best_candidate(n)
        assert chosen is not None
        assert chosen == seeds[4]
        assert "Table 2 lists the weaker" in ds7.reported_payload(chosen, n)["note"]
    chosen27 = ds7.best_candidate(27)
    assert chosen27 is not None
    assert chosen27.theorem == 9
    assert ds7.best_candidate(28) == seeds[5]
    with pytest.raises(ValueError, match="positive"):
        ds7.green_ten(0)
    with pytest.raises(ValueError, match="positive"):
        ds7.green(0)


def test_table82_contradiction_is_excluded_without_rewriting_the_theorem() -> None:
    malformed = ds7.exact_parse("2sqrt(2)+(288+12sqrt(3))/41")
    assert ds7.compare(malformed, sp.Integer(10))["sign"] == 1
    selected = ds7.best_candidate(82)
    assert selected is not None
    assert selected.theorem == 9
    assert selected.k == 9
    assert ds7.compare(selected.expression, sp.Integer(10))["sign"] == -1
    assert all(ds7.compare(c.expression, malformed)["sign"] != 0 for c in ds7.candidates())


@pytest.mark.parametrize(
    ("n", "verified_exact", "note_fragment", "verified_value"),
    [
        (17, "18641771/4000000", "s(17) > 18641771/4000000", "4.66044275"),
    ],
)
def test_indexed_external17_report_holds_the_verified_lane_at_the_selectors_fixed_point(
    n: int, verified_exact: str, note_fragment: str, verified_value: str
) -> None:
    """The strongest indexed external n17 lower-bound report, and what it may and may not move.

    It was anabologyco-maker's 9141/2000, below the verified lane at both sizes.
    Since 2026-09-20 Guzhou0806's historical R012 has supplied the n = 18 report. At
    n = 17 later strict bounds supersede R012 -- Overbeck's 461300/99853 from
    2026-09-22, Guzhou0806's R052 231001/50000 from 2026-09-25, Overbeck's v1.1.0
    232001/50000 and then Overbeck's 466001/100000 (building on this project, Mira and
    Guzhou0806), both from 2026-09-27, Guzhou0806's R068 116511/25000, continuing
    Overbeck's charge, from 2026-09-29, and then R071 18641771/4000000 on R068's charge
    unchanged (T-093), reported from 2026-10-05 above the verified lane until its paired
    replay passed here the same day, when the two fields came to hold the same value.
    The verified field keeps R071. Since 2026-10-12 the reported field holds Overbeck's
    candidate equality instead (T-153), which
    `test_n17_reported_candidate_equality_is_not_misparsed_or_ranked` covers. At n = 18
    R012 held the report below a stronger first-party rung until wand125's rectangle
    report replaced it; see the next test. Either way the audit's own selector must be
    at a fixed point: with R071 in the reported lane, as it was until T-153, no DS7
    candidate exceeds it, so the selector raises nothing.
    """
    case = ds7.read_case(REPO, None, n)
    verified = case["verified_lower_bound"]
    assert verified["value"] == verified_value
    assert verified["exact_form"] == verified_exact
    assert "E-n017-guzhou-r071-source-replay" in verified["evidence"]
    assert note_fragment in case["reported_lower_bound"]["note"]
    verified_expression, _ = ds7.field_expression(case, "verified_lower_bound")
    assert ds7.compare(verified_expression, ds7.exact_parse(verified_exact))["sign"] == 0
    as_reported = deepcopy(case)
    as_reported["reported_status"] = "open"
    as_reported["reported_lower_bound"] = deepcopy(verified)
    reported_expression, _ = ds7.field_expression(as_reported, "reported_lower_bound")
    assert ds7.compare(reported_expression, verified_expression)["sign"] == 0
    assert not ds7.report_without_parser_identity(as_reported, "reported_lower_bound")
    assert ds7.select_update(as_reported) is None
    comparison = next(row for row in ds7.audit(REPO, None, None, n)["rows"] if row["n"] == n)
    assert comparison["verified_lower_bound"]["current_exact"] == verified_exact


def test_a_stronger_non_ds7_report_at_n18_is_left_in_place() -> None:
    """wand125's check2 report on its finest declared net (T-102) outranks its certificates
    of 5 and 6 October (T-096, T-099), R012, its rectangle certificate and the DS7
    candidates at n = 18.

    The DS7 selector must neither lower nor replace the reported one.
    """
    case = ds7.read_case(REPO, None, 18)
    assert case["reported_lower_bound"]["exact_form"] == "941/200"
    assert (
        case["reported_lower_bound"]["source_key"] == "[wand125 mixed bounds check2 2026-10-06]"
    )
    assert ds7.select_update(case) is None


def test_n11_reported_algebraic_identity_is_not_misparsed_or_ranked() -> None:
    case = ds7.read_case(REPO, None, 11)
    reported = case["reported_lower_bound"]
    assert reported["exact_form"] is None
    assert "T=(6u+4)/(1+2u-u^2)" in reported["note"]
    assert ds7.report_without_parser_identity(case, "reported_lower_bound")
    assert ds7.select_update(case) is None
    comparison = next(row for row in ds7.audit(REPO, None, None, 11)["rows"] if row["n"] == 11)
    assert comparison["reported_lower_bound"]["comparison"]["sign"] is None
    assert comparison["reported_lower_bound"]["current_exact"] is None
    assert (
        comparison["verified_lower_bound"]["current_exact"]
        == case["verified_lower_bound"]["exact_form"]
    )
    assert comparison["verified_lower_bound"]["comparison"]["sign"] == -1
    assert "unique root" in comparison["verified_lower_bound"]["exact_identity_basis"]
    assert not ds7.report_without_parser_identity(case, "verified_lower_bound")
    for key, value in (
        ("value", "3.8"),
        ("source_key", "[another source]"),
        ("evidence", []),
    ):
        near_miss = deepcopy(case)
        near_miss["reported_lower_bound"][key] = value
        assert not ds7.report_without_parser_identity(near_miss, "reported_lower_bound")
        with pytest.raises(ValueError, match="lacks a usable exact identity"):
            ds7.field_expression(near_miss, "reported_lower_bound")
    unproved = deepcopy(case)
    unproved["reported_status"] = "open"
    assert not ds7.report_without_parser_identity(unproved, "reported_lower_bound")
    without_verified_identity = deepcopy(case)
    without_verified_identity["verified_lower_bound"]["exact_form"] = None
    with pytest.raises(ValueError, match="lacks a usable exact identity"):
        ds7.field_expression(without_verified_identity, "verified_lower_bound")
    malformed = deepcopy(case)
    malformed["reported_lower_bound"]["exact_form"] = "unknown"
    assert not ds7.report_without_parser_identity(malformed, "reported_lower_bound")
    with pytest.raises(ValueError, match="expression"):
        ds7.field_expression(malformed, "reported_lower_bound")


def test_n17_reported_candidate_equality_is_not_misparsed_or_ranked() -> None:
    """Overbeck's candidate equality s(17) = L (T-153) holds n = 17's reported lane.

    L is the root of the H-255 chart, outside this audit's exact grammar, so the audit
    recognises the claim only under its full pin -- displayed value, source key,
    evidence and reported status -- and then neither parses nor ranks it. The claim lies
    above the verified lane, which keeps R071 until a complete replay passes.
    """
    case = ds7.read_case(REPO, None, 17)
    reported = case["reported_lower_bound"]
    assert reported["exact_form"] is None
    assert reported["source_key"] == "[Overbeck n17 candidate 2026]"
    assert "candidate proof, not an established theorem" in reported["note"]
    assert ds7.report_without_parser_identity(case, "reported_lower_bound")
    assert not ds7.report_without_parser_identity(case, "verified_lower_bound")
    assert ds7.select_update(case) is None
    verified, _ = ds7.field_expression(case, "verified_lower_bound")
    assert ds7.compare(verified, sp.Rational(reported["value"]))["sign"] < 0
    comparison = next(row for row in ds7.audit(REPO, None, None, 17)["rows"] if row["n"] == 17)
    assert comparison["reported_lower_bound"]["comparison"]["sign"] is None
    assert comparison["reported_lower_bound"]["current_exact"] is None
    assert (
        comparison["verified_lower_bound"]["current_exact"]
        == case["verified_lower_bound"]["exact_form"]
    )
    for key, value in (
        ("value", "4.67"),
        ("source_key", "[another source]"),
        ("evidence", []),
    ):
        near_miss = deepcopy(case)
        near_miss["reported_lower_bound"][key] = value
        assert not ds7.report_without_parser_identity(near_miss, "reported_lower_bound")
        with pytest.raises(ValueError, match="lacks a usable exact identity"):
            ds7.field_expression(near_miss, "reported_lower_bound")
    unproved = deepcopy(case)
    unproved["reported_status"] = "open"
    assert not ds7.report_without_parser_identity(unproved, "reported_lower_bound")


def test_verified_n11_root_comparison_uses_the_polynomial_not_display_digits() -> None:
    case = ds7.read_case(REPO, None, 11)
    with pytest.raises(ValueError, match="unsupported exact expression"):
        ds7.exact_parse(case["verified_lower_bound"]["exact_form"])
    # These rational endpoints straddle T; changing the display must not move it.
    case["verified_lower_bound"]["value"] = "0"
    for expression, sign in (("3.87708359", -1), ("3.87708360", 1)):
        comparison = ds7.n11_verified_root_comparison(case, ds7.exact_parse(expression))
        assert comparison is not None
        assert comparison["sign"] == sign
    for key, value in (("exact_form", "root(P_unknown, 3.877)"), ("evidence", [])):
        near_miss = deepcopy(case)
        near_miss["verified_lower_bound"][key] = value
        assert ds7.n11_verified_root_comparison(near_miss, sp.Integer(3)) is None
        with pytest.raises(ValueError, match="unsupported exact expression"):
            ds7.field_expression(near_miss, "verified_lower_bound")
    case["status"] = "open"
    assert ds7.n11_verified_root_comparison(case, sp.Integer(3)) is None


def test_opaque21_stays_nonexact_and_cannot_replace_a_stronger_exact_identity() -> None:
    case = ds7.read_case(REPO, None, 21)
    # Evan Daniel's s(21) = 5 in both lanes since 2026-09-29, and his 5000/1001 from
    # 2026-09-27 before it; before that the reported lane held DS7's opaque 4.7438 and
    # the verified lane T-034's 122/25, then T-021's 97/20.
    assert case["reported_lower_bound"]["exact_form"] == "5"
    assert case["verified_lower_bound"]["value"] == "5"
    assert ds7.select_update(case) is None
    assert not ds7.opaque_needs_update(case, "4.7438")
    # The opaque decimal itself stays non-exact: restored to the lane, it is not an update
    # of itself and carries no exact identity.
    opaque = deepcopy(case)
    opaque["reported_lower_bound"].update(value="4.7438", exact_form=None)
    assert not ds7.opaque_needs_update(opaque, "4.7438")
    with pytest.raises(ValueError, match="lacks a usable exact identity"):
        ds7.field_expression(opaque, "reported_lower_bound")
    case["reported_lower_bound"].update(value="4.7", exact_form="19/4")
    before = deepcopy(case)
    assert ds7.select_update(case) is None
    assert not ds7.opaque_needs_update(case, "4.7438")
    assert ds7.field_expression(case, "reported_lower_bound")[0] == sp.Rational(19, 4)
    assert case == before


def test_stronger_exact_reports_and_proved_case_preconditions_are_preserved() -> None:
    case = ds7.read_case(REPO, None, 101)
    case["reported_lower_bound"].update(value="10.5", exact_form="21/2")
    assert ds7.select_update(case) is None
    proved = ds7.read_case(REPO, None, 5)
    assert ds7.field_expression(proved, "reported_lower_bound")[1].startswith("DS7 Table 2")
    proved["status"] = "open"
    with pytest.raises(ValueError, match="lacks a usable exact identity"):
        ds7.field_expression(proved, "reported_lower_bound")


def test_full_corpus_check_is_reachable_and_rejects_an_omitted_source(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # This ordinary pytest test runs on the PR surface; the guard is not manual-only.
    ds7.main(["--check"])
    assert '"max_n": 324' in capsys.readouterr().out
    original_read = ds7.read_case
    read_cases: set[int] = set()

    # The omitted source is n = 122's, where Green's DS7 value is the reported lower bound
    # above the verified one. It was n = 101's until 3 October 2026, when T-080's replayed
    # linear certificate made the two fields equal there, so omitting it changed nothing.
    def omit_122(repo: Path, revision: str | None, n: int) -> dict[str, Any]:
        read_cases.add(n)
        case = original_read(repo, revision, n)
        if n == 122:
            case["reported_lower_bound"] = deepcopy(case["verified_lower_bound"])
        return case

    monkeypatch.setattr(ds7, "read_case", omit_122)
    with pytest.raises(SystemExit, match=r"exact=\[122\]"):
        ds7.main(["--check"])
    assert read_cases == set(range(1, 325))


def test_owned_case_reader_refuses_duplicate_yaml_keys(tmp_path: Path) -> None:
    target = tmp_path / "packing/frontier/n-001.md"
    target.parent.mkdir(parents=True)
    target.write_text("---\npacking:\n  n: 1\n  n: 2\n---\n")
    with pytest.raises(yaml.constructor.ConstructorError, match="duplicate key"):
        ds7.read_case(tmp_path, None, 1)


def test_source_update_is_idempotent_and_preserves_all_upper_and_verified_fields(
    tmp_path: Path,
) -> None:
    original = (REPO / "packing/frontier/n-019.md").read_text()
    _, front, body = original.split("---", 2)
    document = load_yaml(front)
    case = document["packing"]
    case["reported_lower_bound"] = {
        "value": "4.485281374239",
        "exact_form": "6sqrt(2)-4",
        "evidence": ["E-friedman-ds7-table2-opaque-lower"],
    }
    protected = ("verified_lower_bound", "reported_upper_bound", "verified_upper_bound")
    before = deepcopy({key: case[key] for key in protected})
    target = tmp_path / "packing/frontier/n-019.md"
    target.parent.mkdir(parents=True)
    target.write_text("---\n" + yaml.safe_dump(document) + "---" + body)
    assert ds7.update_records(tmp_path) == [19]
    updated = ds7.read_case(tmp_path, None, 19)
    assert {key: updated[key] for key in protected} == before
    assert "Table 2 lists the weaker" in updated["reported_lower_bound"]["note"]
    first = target.read_bytes()
    assert ds7.update_records(tmp_path) == []
    assert target.read_bytes() == first
