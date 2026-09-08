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


@pytest.mark.parametrize("n", [17, 18])
def test_indexed_external17_report_is_non_strict_and_below_verified(n: int) -> None:
    case = ds7.read_case(REPO, None, n)
    assert case["reported_lower_bound"]["exact_form"] == "9141/2000"
    assert "s(17) >= 9141/2000" in case["reported_lower_bound"]["note"]
    assert case["verified_lower_bound"]["value"] == "4.59"
    assert ds7.select_update(case) is None


def test_opaque21_stays_nonexact_and_cannot_replace_a_stronger_exact_identity() -> None:
    case = ds7.read_case(REPO, None, 21)
    assert case["reported_lower_bound"]["exact_form"] is None
    assert case["reported_lower_bound"]["value"] == "4.7438"
    assert case["verified_lower_bound"]["value"] == "4.85"
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

    def omit_101(repo: Path, revision: str | None, n: int) -> dict[str, Any]:
        read_cases.add(n)
        case = original_read(repo, revision, n)
        if n == 101:
            case["reported_lower_bound"] = deepcopy(case["verified_lower_bound"])
        return case

    monkeypatch.setattr(ds7, "read_case", omit_101)
    with pytest.raises(SystemExit, match=r"exact=\[101\]"):
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
