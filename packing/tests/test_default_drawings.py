"""Each count's default picture follows the improvement rule, read from the data.

The owner, 13 October 2026 (policy section 12): the regularized view is the default
picture where it improves on the house drawing, and the house drawing stays "as
published". The whole record is measured again by its check in the records tier
(`default pictures improve on their house drawings`); these tests hold the decision on
real counts of each kind and the reader's refusals, so nothing here pins how many counts
the data gives.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from devtools import default_drawings as defaults
from devtools import improvement_rule as rule


@pytest.fixture(scope="module")
def entries() -> dict[int, dict]:
    return defaults.drawn_views()


def _decided(entries: dict[int, dict], n: int) -> dict:
    return defaults.decide((defaults.REPO, n, entries))


def test_the_record_decides_exactly_the_views_the_index_draws(entries: dict) -> None:
    record = json.loads(defaults.RECORD.read_text(encoding="utf-8"))
    assert [row["n"] for row in record["entries"]] == sorted(entries)
    assert record["rule"] == rule.SECTION
    totals = record["totals"]
    assert totals["views"] == len(entries) == totals["regularized"] + totals["house"]
    drawn = defaults.regularized_defaults()
    assert len(drawn) == totals["regularized"]
    for n, row in drawn.items():
        # Every regularized default is valid and an improvement, as the rule says.
        assert row["exact_routes"], n
        assert row["better"], n
        assert not row["worse"], n
        assert row["side"]["view_minus_U"] is not None, n
        assert float(row["side"]["view_minus_U"]) <= 0 or n in defaults.ABOVE_U, n


def _first(entries: dict, *, house_exact: bool, gains: bool) -> int:
    """The first count whose stored decision is of a kind, so the test follows the
    data rather than naming a count that a later layer may redraw."""
    record = json.loads(defaults.RECORD.read_text(encoding="utf-8"))
    for row in record["entries"]:
        measured = bool([goal for goal in row["better"] if goal in rule.MEASURES])
        if row["house_exact"] is house_exact and measured is gains and row["n"] in entries:
            return int(row["n"])
    pytest.skip("the data holds no such count")


def test_a_view_better_on_a_measure_is_the_default(entries: dict) -> None:
    n = _first(entries, house_exact=True, gains=True)
    decided = _decided(entries, n)
    assert decided["default"] == defaults.REGULARIZED
    assert decided["reason"].startswith("better on ")
    assert not decided["worse"]


def test_exactness_alone_makes_a_view_over_a_numerically_checked_house_the_default(
    entries: dict,
) -> None:
    n = _first(entries, house_exact=False, gains=False)
    decided = _decided(entries, n)
    assert decided["default"] == defaults.REGULARIZED
    assert decided["better"] == [rule.EXACTNESS]
    assert all(value["view"] == value["house"] for value in decided["measures"].values())


def test_a_view_that_ties_an_exact_house_keeps_the_house(entries: dict) -> None:
    record = json.loads(defaults.RECORD.read_text(encoding="utf-8"))
    tied = [
        row["n"]
        for row in record["entries"]
        if row["house_exact"] and not row["better"] and not row["worse"]
    ]
    if not tied:
        pytest.skip("the data holds no tie")
    decided = _decided(entries, tied[0])
    assert decided["default"] == defaults.HOUSE
    assert decided["reason"] == "no gain"


def test_a_view_above_the_bound_and_not_named_keeps_the_house(
    entries: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    n = next(iter(sorted(defaults.ABOVE_U)))
    monkeypatch.setattr(defaults, "ABOVE_U", {})
    assert _decided(entries, n)["reason"] == defaults.ABOVE_BOUND


def test_a_view_an_exact_route_refused_keeps_the_house(entries: dict) -> None:
    n = next(iter(sorted(entries)))
    refused = {**entries[n], "exact_verification": {"passed": False}}
    decided = defaults.decide((defaults.REPO, n, {**entries, n: refused}))
    assert decided["default"] == defaults.HOUSE
    assert decided["reason"] == defaults.ROUTE_REFUSED
    # A refused view is not exactly verified, so it gains nothing on exactness either.
    assert rule.EXACTNESS not in decided["better"]


def test_a_stale_record_is_refused_rather_than_drawn_from(tmp_path: Path) -> None:
    record = json.loads(defaults.RECORD.read_text(encoding="utf-8"))
    record["entries"] = record["entries"][1:]
    stale = tmp_path / "default-drawings.json"
    stale.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(SystemExit, match="stale"):
        defaults.regularized_defaults(stale)
    record = json.loads(defaults.RECORD.read_text(encoding="utf-8"))
    record["entries"][0]["view"] = (
        "packing/atlas/known-best/regularized/n-999-regularized.yaml.gz"
    )
    stale.write_text(json.dumps(record), encoding="utf-8")
    defaults.regularized_defaults.cache_clear()
    with pytest.raises(SystemExit, match="another view"):
        defaults.regularized_defaults(stale)


def test_the_check_refuses_a_regularized_default_the_rule_does_not_give(tmp_path: Path) -> None:
    expected = json.loads(defaults.RECORD.read_text(encoding="utf-8"))
    kept = next(row for row in expected["entries"] if row["default"] == defaults.HOUSE)
    altered = json.loads(json.dumps(expected))
    for row in altered["entries"]:
        if row["n"] == kept["n"]:
            row["default"] = defaults.REGULARIZED
    record = tmp_path / "default-drawings.json"
    record.write_text(defaults.text(altered), encoding="utf-8")
    found, listed = defaults.problems(expected, record)
    assert any(f"n={kept['n']} is drawn regularized by default" in line for line in found)
    assert f"n={kept['n']} keeps the house picture: {kept['reason']}" in listed


@pytest.mark.parametrize("n", [18, 26, 66, 85])
def test_an_irrational_bound_is_read_exactly_for_a_named_exception(
    entries: dict, n: int
) -> None:
    from devtools import regularize_axis_components as axis  # noqa: PLC0415
    from devtools import regularize_evand as drive  # noqa: PLC0415

    assert defaults.ABOVE_U is axis.ABOVE_U
    decided = _decided(entries, n)
    bound = drive.verified_bound(drive.case_facts(n))
    assert bound is not None
    assert bound.rational is None
    side, *_ = drive.view_geometry(defaults._view_witness(entries[n]))  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert bound.compare(side) == 1
    assert decided["reason"] != defaults.UNKNOWN_U
    assert decided["side"]["view_minus_U"] == f"{bound.difference(side):.3e}"
    assert 0 < defaults.drawn_above_bound()[n] < 1e-28


def test_an_unread_bound_cannot_authorize_a_regularized_default(
    entries: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    from devtools import regularize_evand as drive  # noqa: PLC0415

    n = min(entries)
    monkeypatch.setattr(
        drive, "verified_bound", lambda _facts: drive.VerifiedBound("unknown", unread="unread")
    )
    decided = _decided(entries, n)
    assert decided["default"] == defaults.HOUSE
    assert decided["reason"] == defaults.UNKNOWN_U
    assert decided["side"]["view_minus_U"] is None
    with pytest.raises(ValueError, match="U is not read exactly"):
        defaults.drawn_above_bound()
