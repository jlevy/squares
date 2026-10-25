"""Couzo's 43f666c, the live records since #763's pin (think-gn29), and #763's recipes.

`devtools.couzo_43f666c_claims` re-derives the claims from the indexes the
``couzo-43f666c-2026-10-24`` packet retains: every count whose certified bound 43f666c lowers
below 964ee2b's. `devtools.beyond_horizon_replay` declares the publication as a release,
dates it by the push of 06:10:44Z, walks it in report order after #763's claims that have
no row on ``main`` and the push of 23:38:42Z read commit by commit at its counts, and
decides its recipes and #763's, held until then, by the construction checker (D2,
think-g2qy). These tests hold the claim map to a fresh derivation and its rule at its
edges, the walk to its sources and verdicts, and the recipe rows to their decisions and
dates.
"""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
from yaml import safe_load

from devtools import beyond_horizon_replay as replay
from devtools import construction_checker as checker
from devtools import couzo_43f666c_claims as claims

LABEL = "franciscouzo/square-packing@43f666c"
SOURCE = "couzo-43f666c-2026-10-24"
SOURCE_763 = "couzo-issue763-2026-10-23"
WALK = replay.ROOT / "campaign/issue-intake/upper-bounds-couzo-43f666c-20261024"
#: #763's recipes, held on its walk until the construction checker decided them.
RECIPES_763 = [365, 444, 487, 632, 733, 734, 737, 788, 789, 845, 910, 966, 970]
#: 43f666c's recipes at or below 1024 (the triage's 17).
RECIPES_43F = [
    367,
    444,
    487,
    632,
    683,
    732,
    733,
    737,
    744,
    787,
    788,
    792,
    800,
    844,
    845,
    903,
    964,
]


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _steps() -> dict[str, dict[int, dict[str, Any]]]:
    steps: dict[str, dict[int, dict[str, Any]]] = {}
    for count in _read(WALK / "ledger.json")["counts"]:
        for step in count["steps"]:
            steps.setdefault(step["report"], {})[count["n"]] = step
    return steps


def _entry(n: int, bound: Fraction, credit: str = "Francisco Couzo") -> dict[str, Any]:
    return {
        "n": n,
        "kind": "certificate",
        "certificate": f"certificates/best/n{n}.cert",
        "certificate_sha256": "0" * 64,
        "source_n": n,
        "deleted_squares": 0,
        "bound": f"{bound.numerator}/{bound.denominator}",
        "credit": credit,
    }


# --------------------------------------------------------------------------- the claim map


def test_the_claim_map_is_a_fresh_derivation_with_the_triage_s_counts() -> None:
    """The receipt is what the retained indexes give, and the derivation reproduces the
    stage 1 triage's counts (think-cncq): 957 lowered, 126 at 325 to 1024 (108
    certificates, 690 as a deletion and 17 recipes) and 831 recipes above."""
    assert claims.check() == []
    summary = _read(claims.RECEIPT)["summary"]
    assert summary["at_or_below_limit"] == 126
    assert summary["constructions"] == RECIPES_43F
    assert summary["deletions"] == [690]
    assert sum(summary["refines"].values()) == 126


def test_a_claim_is_strictly_below_964ee2b_s_bound() -> None:
    """The rule at its edge: an equal bound is no claim, one unit lower in any place is."""
    side = Fraction(19)
    previous = {"400": _entry(400, side)}
    equal = claims.claim_map({"400": _entry(400, side)}, {}, previous)
    lower = claims.claim_map({"400": _entry(400, side - Fraction(1, 10**30))}, {}, previous)
    assert equal["lowered"] == []
    assert [item["n"] for item in lower["lowered"]] == [400]


def test_a_lowered_bound_credited_to_another_author_is_refused() -> None:
    """Every lowered bound is credited to Couzo; one that is not is refused rather than
    imported under his source."""
    previous = {"400": _entry(400, Fraction(19))}
    with pytest.raises(claims.ClaimError, match="not credited to Couzo"):
        claims.claim_map({"400": _entry(400, Fraction(18), "Kirill Tymchishin")}, {}, previous)


def test_the_credits_name_the_packings_they_refine() -> None:
    """The triage's credit lines: Couzo after Lavrentev's v11 at 76 counts, Tymchishin's v3
    at 40, and six more, one his own."""
    refines = _read(claims.RECEIPT)["summary"]["refines"]
    assert refines == dict(sorted(claims.REFINES_CONTROLS.items()))
    assert claims.refines("Francisco Couzo; refines the packing of X (x); more") == "X (x)"
    assert claims.refines("Francisco Couzo") is None


# --------------------------------------------------------------------------- the walk


def test_43f666c_is_dated_by_the_push_of_0610() -> None:
    chosen = replay.release(LABEL)
    (push,) = [
        push
        for push in replay.PUSHED_LATER["franciscouzo/square-packing"]
        if push.head == chosen.retained
    ]
    assert chosen.reported == push.pushed == "2026-10-24T06:10:44Z"
    assert (chosen.pin[:7], chosen.retained[:7], chosen.source) == (
        "43f666c",
        "1c17153",
        SOURCE,
    )


def test_the_walk_transcribes_its_sources() -> None:
    """``sources.yaml`` is what `claim_map_walk_sources` writes from starts frozen at main
    2ed0ea740: 43f666c's claims, #763's claims with no row there, the push of 23:38:42Z read
    commit by commit at its counts, and the earlier publications below the start."""
    sources = safe_load((WALK / "sources.yaml").read_text(encoding="utf-8"))
    assert sources == replay.claim_map_walk_sources(LABEL, str(sources["read_on"]))
    assert sources["read_at_main"] == replay.COUZO_43F_READ_AT_MAIN
    reports = {item["report"] for item in sources["reports"]}
    assert reports >= {
        LABEL,
        "#763",
        "franciscouzo/square-packing@efef7d1",
        "franciscouzo/square-packing@fa6237e",
        "franciscouzo/square-packing@964ee2b",
    }


def test_763_s_claims_walked_are_those_with_no_row_on_main() -> None:
    """#763's claims the walk reads are each claim beyond the corpus its filtered receipt
    does not hold: the 13 recipes, 683, and 328, 850 and 909, which restate f1ceee4."""
    _earlier, found = replay.earlier_issue_claims(replay.WALKS[replay.COUZO_43F])
    assert sorted(int(item["n"]) for item in found) == sorted(
        [*RECIPES_763, 683, 328, 850, 909]
    )
    steps = _steps()["#763"]
    assert {n for n, step in steps.items() if step["verdict"] != "recorded"} == {328, 850, 909}


def test_the_walk_records_43f666c_s_rows_and_names_each_exception() -> None:
    """122 rows: 106 certificates and 16 recipes. 797 and 847 restate #763's rows; 367 is
    above 23aff0c's deletion from Friedman's 368 and rests on that hold; 690 is recorded and
    settled with no row by the D6 answer."""
    steps = _steps()[LABEL]
    assert len(steps) == 126
    unrecorded = {
        n: step["reason"] for n, step in steps.items() if step["verdict"] != "recorded"
    }
    assert unrecorded == {367: "above", 797: "restates", 847: "restates"}
    walk = replay.WALKS[replay.COUZO_43F]
    (settled,) = walk.held[LABEL]
    assert (sorted(settled.counts), settled.answer) == ([690], replay.DELETION_ANSWER)
    rows = replay.decided_claims(replay.release(LABEL))
    assert len(rows) == 122
    assert Counter(row.recipe is not None for row in rows) == {False: 106, True: 16}
    assert {row.n for row in rows} == set(steps) - set(unrecorded) - {690}


def test_the_earlier_push_is_walked_and_records_nothing() -> None:
    """The push of 23:38:42Z, read commit by commit at the walk's counts, states sides below
    the start only at #763's counts and at 792 and 800; each is above, equal to or a
    restatement of an earlier report, so none is recorded."""
    steps = _steps()
    pushed = {
        commit: steps[f"franciscouzo/square-packing@{commit}"]
        for commit in ("efef7d1", "fa6237e", "964ee2b")
    }
    assert {commit: len(found) for commit, found in pushed.items()} == {
        "efef7d1": 8,
        "fa6237e": 12,
        "964ee2b": 14,
    }
    assert all(
        step["verdict"] == "not recorded"
        for found in pushed.values()
        for step in found.values()
    )
    receipt = _read(replay.release(LABEL).directory / replay.EARLIER_PUSH)
    assert receipt["counts"] == replay.walk_counts(replay.WALKS[replay.COUZO_43F])
    assert receipt["push"]["head"] == replay.COUZO_763_PIN


def test_the_walk_s_holds_and_resting_verdicts_are_the_ledger_s() -> None:
    walk = replay.WALKS[replay.COUZO_43F]
    assert set(replay.resting_on_holds(walk)) == set(walk.resting)
    assert not [problem for problem in replay.resting_problems() if replay.COUZO_43F in problem]


# --------------------------------------------------------------------------- the recipes


def test_763_s_recipes_are_rows_decided_by_the_checker() -> None:
    """think-g2qy: #763's walk holds only 683 now; its 13 recipes are declared rows with
    their recipes, each decided exactly from its replayed parent with every control
    refused."""
    walk = replay.WALKS[replay.ISSUE_763]
    (deletion,) = walk.held["#763"]
    assert sorted(deletion.counts) == [683]
    chosen = replay.release(763)
    recipes = replay.recipe_claims(chosen)
    assert [row.n for row in recipes] == RECIPES_763
    receipt = _read(chosen.path(replay.RECIPES))
    assert [item["n"] for item in receipt["rows"]] == RECIPES_763
    assert all(item["verdict"] == checker.DECIDED for item in receipt["rows"])
    assert all(control["refused"] for item in receipt["rows"] for control in item["controls"])
    assert replay.recipe_problems(chosen, replay=False, workers=1) == []


def test_43f666c_s_recipes_are_decided_by_the_checker() -> None:
    chosen = replay.release(LABEL)
    receipt = _read(chosen.path(replay.RECIPES))
    assert [item["n"] for item in receipt["rows"]] == [n for n in RECIPES_43F if n != 367]
    assert all(item["verdict"] == checker.DECIDED for item in receipt["rows"])
    assert receipt["parents"] == []
    assert replay.recipe_problems(chosen, replay=False, workers=1) == []


def test_a_recipe_row_is_dated_by_the_first_index_that_states_it() -> None:
    """#793's review A, A8: #763's 365 and 970 are first stated by efef7d1's index, its
    other recipes by 964ee2b's; every one of 43f666c's by its own commit."""
    found = {
        row["n"]: row["first_commit"][:7]
        for row in _read(replay.release(763).path(replay.FIRST_COMMITS))["rows"]
        if "dated_by" in row
    }
    assert found == {n: ("efef7d1" if n in (365, 970) else "964ee2b") for n in RECIPES_763}
    assert {
        row["first_commit"][:7]
        for row in _read(replay.release(LABEL).path(replay.FIRST_COMMITS))["rows"]
    } == {"43f666c"}


def test_an_index_entry_that_changes_the_recipe_does_not_date_it() -> None:
    """`states_recipe` refuses an entry whose bound, parent digest or layers differ."""
    (row,) = [row for row in replay.recipe_claims(replay.release(763)) if row.n == 632]
    recipe = dict(row.recipe or {})
    entry = {
        "kind": "construction",
        "construction": {
            key: recipe[key]
            for key in ("kind", "source_n", "tiles_per_side", "layers", "capacity")
        },
        "certificate_sha256": recipe["sha256"],
        "bound": recipe["bound"],
        "deleted_squares": 0,
    }
    assert replay.states_recipe(entry, row)
    assert not replay.states_recipe(entry | {"bound": "1"}, row)
    assert not replay.states_recipe(entry | {"certificate_sha256": "0" * 64}, row)
    layers = {**entry["construction"], "layers": recipe["layers"] + 1}
    assert not replay.states_recipe(entry | {"construction": layers}, row)
    assert not replay.states_recipe(None, row)


# --------------------------------------------------------------------------- the register


def test_43f666c_s_rows_are_current_and_supersede_the_rows_they_beat() -> None:
    """Each of the 122 is the count's current row. The first report the walk records with a
    row beats main's start at 115 counts; at the other 7, #763's recipe row this import
    writes comes first, and the register leads from it to 43f666c's."""
    rows = [row for row in replay.planned_rows() if row["source_id"] == SOURCE]
    assert len(rows) == 122
    assert all(row["disposition"] == "tracked-outside-case-corpus" for row in rows)
    beaten = Counter(
        start for _, start, source in replay.planned_supersessions() if source == SOURCE
    )
    assert sum(beaten.values()) == 115
    assert beaten[SOURCE_763] == 65
    register = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    after = {
        row["n"]
        for row in register["beyond_horizon_claims"]
        if row["source_id"] == SOURCE_763 and row.get("superseded_by") == SOURCE
    }
    assert after >= {444, 487, 632, 733, 737, 788, 845}
    assert not [problem for problem in replay.coverage_problems(register) if SOURCE in problem]
