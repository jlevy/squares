"""Refusal and overlap controls for the n17 issue metadata join."""

from __future__ import annotations

import copy
import time

from devtools import reconcile_n17_issue_patterns as join

GROUP = ((0, 1, 2, 3), (3, 2, 1, 0))


def test_d4_equality_is_separate_from_containment() -> None:
    # Q=one cell, P=two cells: Q entails exclusion of P, not conversely.
    result = join.class_relations(3, {1: "small", 3: "equal", 7: "large"}, GROUP)
    assert result["equal_admitted"] == ["equal"]
    assert result["contained_admitted"] == ["small"]
    assert result["containing_admitted"] == ["large"]
    reverse = join.class_relations(1, {3: "large"}, GROUP)
    assert reverse["contained_admitted"] == []


def test_d4_union_overlap_and_fixed_margins() -> None:
    population = {3: 2, 5: 2, 7: 2}
    first = join.project(3, population, GROUP)
    image = join.project(12, population, GROUP)
    second = join.project(5, population, GROUP)
    assert first == image == {3, 7}
    assert second == {5, 7}
    assert join.population_count(population, first | second) == {"orbits": 3, "states": 6}
    assert join.population_count(population, second - first) == {"orbits": 1, "states": 2}


def test_report_history_keeps_unexplained_promotion() -> None:
    messages = [
        {"source": "body", "table": "| 1 | a, b | Computed | — |", "totals": None},
        {
            "source": "comment1",
            "table": "| 2 | c, d | Computed | — |",
            "totals": {"verified": 1, "computed": 1},
        },
    ]
    result = join.parse_reports(messages)
    assert len(result["rows"]) == 2
    assert result["row_totals"] == {"verified": 0, "computed": 2}
    assert len(result["aggregate_discrepancies"]) == 1
    corrected = copy.deepcopy(messages)
    corrected.append(
        {
            "source": "promotion",
            "table": "| 1 | a, b | Certificate verified | standing verifier (full) |",
            "totals": {"verified": 1, "computed": 1},
        }
    )
    corrected.append(
        {
            "source": "retraction",
            "table": "",
            "verifier_corrections": [
                {"row": 1, "verified_with": "parallel node checks plus fast"}
            ],
        }
    )
    updated = join.parse_reports(corrected)
    assert updated["row_totals"] == {"verified": 1, "computed": 1}
    assert updated["aggregate_discrepancies"][0]["resolved_by"] == "promotion"
    assert updated["unresolved_aggregate_discrepancies"] == []
    assert updated["rows"][0]["verified_with"] == "parallel node checks plus fast"
    assert updated["rows"][0]["history"][-2]["verified_with"] == "standing verifier (full)"
    bad_correction = copy.deepcopy(corrected)
    bad_correction[-1]["verifier_corrections"][0]["row"] = 3
    try:
        join.parse_reports(bad_correction)
    except join.RefusedError as exc:
        assert "unknown row" in str(exc)
    else:
        raise AssertionError("an unjoined verifier correction passed")
    changed = copy.deepcopy(messages)
    changed.append({"source": "comment2", "table": "| 1 | a, e | Computed | — |"})
    try:
        join.parse_reports(changed)
    except join.RefusedError as exc:
        assert "changed cells" in str(exc)
    else:
        raise AssertionError("an unexplained class replacement passed")


def test_unknown_duplicate_and_omitted_rosters_are_refused() -> None:
    bad = {"source": "body", "table": "| 1 | a, a | Computed | — |"}
    try:
        join.parse_reports([bad])
    except join.RefusedError as exc:
        assert "repeated cell" in str(exc)
    else:
        raise AssertionError("duplicate cells passed")
    try:
        join.require_roster([1, 1], [1, 2], "pilot")
    except join.RefusedError as exc:
        assert "pilot" in str(exc)
    else:
        raise AssertionError("omitted/duplicated pilot passed")
    unknown = {"source": "body", "table": "| 1 | a | Verified | fast |"}
    try:
        join.parse_reports([unknown])
    except join.RefusedError as exc:
        assert "status" in str(exc)
    else:
        raise AssertionError("unknown status passed")


def test_frozen_input_join_and_partial_proof_status() -> None:
    source = join.REPO / "packing/campaign/issue-intake/n17-20261008/github-issues.json"
    document = join.read_document(source)
    result = join.reconcile(document, deadline=time.monotonic() + 30)
    assert result["reported33_union"]["distance_two_tail"] == {"orbits": 1, "states": 8}
    assert result["reported33_union"]["first_eight_pilot"] == {"orbits": 0, "states": 0}
    assert result["standing_full_reported_rows"] == [1, 2]
    assert result["explicit_row_totals"] == {"verified": 22, "computed": 11}
    assert result["unresolved_aggregate_discrepancies"] == []
    assert result["certificate_verification_performed"] is False
    assert result["census_admission_proved"] is False
    assert all(row["premise_join"].startswith("unknown") for row in result["patterns"])
    assert not any(row["endpoint_assignment_in_projection"] for row in result["patterns"])
    for mutate, fragment in [
        (lambda d: d.update(cap="117/25"), "cap/frame"),
        (lambda d: d["pilot"]["masks"].pop(), "first-eight"),
        (
            lambda d: d["reports"][0].update(
                table=d["reports"][0]["table"].replace("side-S1", "unknown-cell", 1)
            ),
            "cell",
        ),
    ]:
        broken = copy.deepcopy(document)
        mutate(broken)
        try:
            join.reconcile(broken, deadline=time.monotonic() + 30)
        except ValueError as exc:
            assert fragment in str(exc)
        else:
            raise AssertionError("changed frame or incomplete/mismatched roster passed")
    try:
        join.reconcile(document, deadline=time.monotonic() - 1)
    except join.RefusedError as exc:
        assert "incomplete" in str(exc)
    else:
        raise AssertionError("expired metadata deadline passed")
