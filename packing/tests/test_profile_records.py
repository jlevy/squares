"""Current Records retain typed contribution families without changing authored Results."""

from __future__ import annotations

import json
from fractions import Fraction
from typing import Any

import pytest

from devtools import profile_records as records
from devtools import render_recent_results as standing
from devtools.build_bound_citations import Register


def result(
    identifier: str, kind: str = "upper-bound", *, published: str = "2026-09-01", **extra: Any
) -> dict[str, Any]:
    return {
        "id": identifier,
        "kind": kind,
        "scope": {"n_values": [11, 17]},
        "attribution": {"source_keys": [identifier], "published": published},
        **extra,
    }


def facet(
    identifier: str,
    value: str,
    *,
    n: int = 11,
    direction: records.Direction = "upper",
    lane: records.Lane = "reported",
    high: str | None = None,
) -> records.BoundFacet:
    return records.BoundFacet(
        identifier, n, direction, lane, Fraction(value), Fraction(high or value)
    )


def test_non_bound_families_use_whole_or_partial_lifecycle_not_numeric_standing() -> None:
    raw = {
        "method": result("method", "method-limit"),
        "formal": result("formal", "formalization", proves_kind="optimality"),
        "simple": result("simple", "simplification", proves_kind="optimality"),
        "part": result(
            "part",
            "restricted-optimality",
            superseded_by=[{"result": "formal", "extent": "part"}],
        ),
        "whole": result(
            "whole", "audit", superseded_by=[{"result": "method", "extent": "whole"}]
        ),
    }
    index = records.classify_records(raw, [])
    assert index.current_results == ("formal", "method", "part", "simple")
    assert index.facets["formal"] == (records.RecordFacet("formalization"),)
    authored = ("formal", "whole", "part", "formal")
    assert records.current_record_ids(authored, index) == ("formal", "part")
    assert authored == ("formal", "whole", "part", "formal")


def test_strict_numeric_frontier_compares_every_pending_claim_per_case_and_lane() -> None:
    raw = {name: result(name) for name in ("old", "pending", "stronger")}
    index = records.classify_records(
        raw, [facet("old", "5"), facet("pending", "4.9"), facet("stronger", "4.8")]
    )
    assert index.current_results == ("stronger",)
    assert index.unresolved == {}
    lower = records.classify_records(
        {name: result(name, "lower-bound") for name in raw},
        [facet("old", "3", direction="lower"), facet("stronger", "4", direction="lower")],
    )
    assert lower.current_results == ("stronger",)


def test_exact_ties_require_proven_original_publication_priority() -> None:
    raw = {
        "first": result("first", published="2025"),
        "later": result("later", published="2026-01-01"),
    }
    index = records.classify_records(raw, [facet("first", "4"), facet("later", "4")])
    assert index.current_results == ("first",)
    for dates in [("2026", "2026-01-01"), ("2026-01-01", "2026-01-01"), ("", "2026")]:
        uncertain = records.classify_records(
            {name: result(name, published=day) for name, day in zip(raw, dates, strict=True)},
            [facet("first", "4"), facet("later", "4")],
        )
        assert uncertain.current_results == ()
        assert set(uncertain.unresolved) == {"first", "later"}
        assert "priority" in uncertain.unresolved["first"][0]


def test_identical_or_overlapping_rounded_intervals_do_not_prove_equal_values() -> None:
    raw = {
        "first": result("first", published="2024"),
        "later": result("later", published="2026"),
    }
    for later in [facet("later", "3.9", high="4.1"), facet("later", "3.95", high="4")]:
        index = records.classify_records(raw, [facet("first", "3.9", high="4.1"), later])
        assert index.current_results == ()
        assert set(index.unresolved) == {"first", "later"}


def test_first_certified_redirects_only_repeat_facet_and_keeps_unrelated_advance() -> None:
    raw = {
        "first": result("first", published="2026-10-05"),
        "regularized": result(
            "regularized",
            published="2026-10-12",
            regularizations=[{"n": 11, "first_certified_in": "first"}],
        ),
    }
    index = records.classify_records(
        raw,
        [
            facet("regularized", "4"),
            facet("regularized", "5", n=17),
            facet("regularized", "5", n=17),
        ],
    )
    assert index.current_results == ("first", "regularized")
    assert [f.n for f in index.facets["first"]] == [11]
    assert [f.n for f in index.facets["regularized"]] == [17]
    assert records.current_record_ids(["regularized", "regularized"], index) == ("regularized",)


def test_partial_currentness_and_independent_exact_value_proof_family() -> None:
    raw = {
        "partial": result("partial"),
        "better": result("better"),
        "proof": result("proof", "optimality"),
    }
    index = records.classify_records(
        raw,
        [
            facet("partial", "5"),
            facet("better", "4"),
            facet("partial", "6", n=17),
            facet("partial", "5", lane="verified"),
        ],
        proof_facets=[
            (
                "proof",
                records.RecordFacet(
                    "optimality", 11, lane="verified", scope="exact-value proof"
                ),
            )
        ],
    )
    assert index.current_results == ("better", "partial", "proof")
    assert {(f.n, f.lane) for f in index.facets["partial"]} == {
        (17, "reported"),
        (11, "verified"),
    }
    assert index.facets["proof"][0].family == "optimality"


def context(raw: dict[str, dict[str, Any]]) -> standing.Records:
    return standing.Records(
        Register(evidence={}, results=list(raw.values()), sources={}, names={}), raw, {}, {}
    )


def test_family_scope_link_validates_source_and_exposes_unassessed_comparison() -> None:
    raw = {"family": result("family")}
    row = {
        "source_key": "family",
        "side_condition": "k >= 15",
        "record_scope": {"result": "family", "review_bead": "think-kqi1"},
    }
    ledger = {"deficiency_upper_bounds": [row]}
    family = records.family_record_facets(ledger, context(raw))
    index = records.classify_records(raw, [], family_facets=family)
    assert index.current_results == ()
    assert set(index.unresolved) == {"family"}
    assert "think-kqi1" in index.unresolved["family"][0]
    assert (
        records.family_record_facets(
            {"deficiency_upper_bounds": [{"source_key": "family"}]}, context(raw)
        )
        == ()
    )
    row["source_key"] = "other"
    with pytest.raises(ValueError, match="source does not match"):
        records.family_record_facets(ledger, context(raw))
    row["source_key"] = "family"
    with pytest.raises(ValueError, match="duplicate or unknown"):
        records.family_record_facets({"deficiency_upper_bounds": [row, row]}, context(raw))


def test_live_current_families_pending_comparison_and_known_scope_gap() -> None:
    index = records.load_record_index()
    assert {"T-003", "T-036", "T-054", "T-055", "T-060", "T-084", "T-154"} <= set(
        index.current_results
    )
    assert "T-031" not in index.current_results
    assert "T-037" not in index.current_results
    assert "T-225" in index.current_results
    assert {"T-196", "T-199", "T-223", "T-226", "T-227", "T-228"}.isdisjoint(
        index.current_results
    )
    assert "T-163" not in index.current_results
    assert "think-kqi1" in " ".join(index.unresolved["T-163"])
    assert records.current_record_ids(["T-037", "T-060", "T-163", "T-060"], index) == ("T-060",)
    # T-229 (#719) states a smaller side at 105 and 204 than T-174 and T-225, and since
    # its adoption of 23 October 2026 holds both lanes there; T-174 and T-225 hold
    # neither lane at those counts. At 204 the release's lower file (T-231), pending
    # adoption, is the stronger pending claim on the reported lane, so T-229 holds only
    # the verified lane there until T-231 is adopted.
    assert {(facet.n, facet.direction, facet.lane) for facet in index.facets["T-225"]} == {
        (n, "upper", lane) for n in (227, 229, 260) for lane in ("reported", "verified")
    }
    assert {(facet.n, facet.direction, facet.lane) for facet in index.facets["T-229"]} == {
        (105, "upper", "reported"),
        (105, "upper", "verified"),
        (204, "upper", "verified"),
    }
    assert {(facet.n, facet.direction, facet.lane) for facet in index.facets["T-231"]} == {
        (204, "upper", "reported")
    }
    assert not {facet for facet in index.facets["T-174"] if facet.n == 105}


def test_cli_keeps_unassessed_distinct_from_known_current(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    index = records.RecordIndex(
        ("current",),
        {"current": (records.RecordFacet("formalization"),)},
        {"unknown": ("Publication priority is unassessed",)},
    )
    monkeypatch.setattr(records, "load_record_index", lambda: index)
    assert records.main(["--json"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["current_result_count"] == output["unassessed_result_count"] == 1
    assert output["current_results"] == ["current"]
    assert output["unresolved"] == {"unknown": ["Publication priority is unassessed"]}
    assert output["facets"]["current"][0]["family"] == "formalization"


def test_proof_derivation_requires_own_lower_holder_and_the_correct_lane_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw = {"proof": result("proof", "optimality")}
    base = context(raw)
    case = {
        "status": "proved",
        "reported_status": "open",
        "verified_lower_bound": {"value": "4"},
        "verified_upper_bound": {"value": "4"},
        "reported_lower_bound": {"value": "4"},
        "reported_upper_bound": {"value": "4"},
    }
    loaded = standing.Records(base.register, raw, {}, {11: case})
    held: dict[tuple[str, str], set[str]] = {("upper", "verified"): {"proof"}}
    monkeypatch.setattr(
        standing,
        "lane_holders",
        lambda _n, _records, direction, lanes: set().union(
            *(held.get((direction, lane), set()) for lane in lanes)
        ),
    )
    monkeypatch.setattr(records.check_standing, "improvements", lambda _record, _records: [])
    upper_only = records.build_record_index(loaded)
    assert all(f.scope != "exact-value proof" for f in upper_only.facets.get("proof", ()))
    held.clear()
    held["lower", "reported"] = {"proof"}
    open_report = records.build_record_index(loaded)
    assert all(f.scope != "exact-value proof" for f in open_report.facets.get("proof", ()))
    case.update(status="open", reported_status="proved")
    closed_report = records.build_record_index(loaded)
    assert any(
        f.scope == "exact-value proof" and f.lane == "reported"
        for f in closed_report.facets["proof"]
    )
