"""The register's record of the regularized drawings, on synthetic entries.

Which registered result holds a drawn count's packing: the one attributing the
witness's source for a view at the witness's side, the one the verified upper bound rests
on for a view at the bound or for a view at a witness's side that is exactly the bound
where no result attributes the source, and none where no result answers or several do.
The generated block reads back as the data it was written from, and the register's
checker holds each item to the register. The last tests read the record itself: which of
T-155's registered sides Evan Daniel's certificates first stated, and which of its solves
the layer draws.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest

from devtools import register_regularized_bounds as registration
from devtools import regularized_drawings as drawings
from devtools.check_results import regularized_drawings_problems
from sqpack.yamlio import safe_load

RESULTS = [
    {"id": "T-001", "scope": {"n_values": [5, 6]}, "attribution": {"source_keys": ["[A]"]}},
    {"id": "T-002", "scope": {"n_min": 5, "n_max": 9}},
    {"id": "T-003", "scope": {"n_values": [6]}, "attribution": {"source_keys": ["[A]"]}},
]
INDEX = "packing/atlas/known-best/regularized/index.json"


def entry(n: int, relation: str | None = None) -> dict[str, Any]:
    found: dict[str, Any] = {
        "n": n,
        "status": "regularized",
        "view": {"path": f"packing/atlas/known-best/regularized/n-{n:03d}-regularized.yaml.gz"},
        "regularization": {
            "n": n,
            "of_witness": f"W-known-best-n{n:03d}",
            "provenance": {"source_key": "[A]", "found_by": ["A"], "improved_by": []},
            "by": "project",
            "method": "Evan Daniel's search/regularize, through devtools.regularize_evand",
            "side": "solved" if relation == "bound" else "same",
            "changes": {"re_angled": 2},
            "identity": {
                "basis": "measured",
                "measured_in": INDEX,
                "one_to_one": True,
                "moved": 3,
                "max_move": 0.4216289,
                "max_turn_deg": 2.35479,
            },
        },
    }
    if relation:
        found["side"] = {"relation": relation}
    return found


def test_the_packing_is_the_result_holding_it_at_the_side_drawn() -> None:
    def resolve(
        n: int, key: str | None, relation: str | None = None, holders=(), *, at_u: bool = True
    ) -> Any:
        return drawings.packing_result(
            entry(n, relation),
            RESULTS,
            source_key=key,
            bound_holders=list(holders),
            side_at_bound=at_u,
        )

    assert resolve(5, "[A]").of == "T-001"
    assert resolve(7, "[A]").of is None
    assert "no registered result" in resolve(7, "[A]").reason
    assert resolve(6, "[A]").of is None
    assert "several" in resolve(6, "[A]").reason
    assert resolve(6, "[A]", "bound", ["T-002"]).of == "T-002"
    assert resolve(6, "[A]", "bound", []).of is None
    # A later result that lowers U leaves a `bound` view at a side no result holds: it is
    # not credited to whoever holds the bound now (#548 review B1).
    moved = resolve(6, "[A]", "bound", ["T-002"], at_u=False)
    assert moved.of is None
    assert "no longer the verified upper bound" in moved.reason


def test_an_axis_view_is_at_the_side_its_regularization_states() -> None:
    axis_view = entry(5)
    assert drawings.relation(axis_view) == "same"
    solved = {**axis_view, "regularization": {**axis_view["regularization"], "side": "solved"}}
    assert drawings.relation(solved) == "solved"
    found = drawings.packing_result(solved, RESULTS, source_key="[A]", bound_holders=[])
    assert found.of is None
    assert "row 4" in found.reason


def test_an_exact_side_is_at_the_bound_only_where_the_bound_is_rational() -> None:
    drawn = {**entry(6, "bound"), "side": {"relation": "bound", "view": "1449/250"}}
    assert drawings.at_bound(drawn, {"value": "5.796", "exact_form": None})
    assert drawings.at_bound(drawn, {"value": "5.80", "exact_form": "1449/250"})
    assert not drawings.at_bound(drawn, {"value": "5.797", "exact_form": None})
    assert not drawings.at_bound(drawn, {"value": "5.79", "exact_form": "3 + 2 sqrt(2)"})


def test_a_witness_side_exactly_at_the_bound_falls_back_to_the_bound_holder() -> None:
    """T-155 certified witnesses' own sides exactly: a `same` view there that no result
    attributes is held by the result the bound rests on, and only when the side is exact."""
    found = entry(7, "same")
    found["side"]["view"] = "33/5"

    def resolve(holders: list[str], *, at: bool = True) -> Any:
        return drawings.packing_result(
            found, RESULTS, source_key="[B]", bound_holders=holders, side_at_bound=at
        )

    assert resolve(["T-002"]).of == "T-002"
    assert resolve(["T-002"], at=False).of is None
    assert resolve(["T-002", "T-003"]).of is None
    # A source some result attributes keeps that result, at the bound or not.
    attributed = drawings.packing_result(
        entry(5, "same"), RESULTS, source_key="[A]", bound_holders=["T-002"], side_at_bound=True
    )
    assert attributed.of == "T-001"
    assert drawings.at_bound(found, {"value": "6.6", "exact_form": "33/5"})
    assert drawings.at_bound(found, {"value": "6.6"})
    assert not drawings.at_bound(
        found, {"value": "6.6000001", "exact_form": "330000001/50000000"}
    )
    assert not drawings.at_bound(found, {"value": "6.6", "exact_form": "4 + sqrt(2)"})
    assert not drawings.at_bound(entry(7, "same"), {"value": "6.6"})


def test_a_bound_two_results_prove_is_held_by_the_one_that_registered_the_view() -> None:
    """At 33 counts T-155's view lies exactly at the side of Evan Daniel's earlier
    certificate (T-101), and the case cites both: the view drawn at that bound is the one
    whose result registered it, by a `regularizations` item on the drawn side; with no
    such item, or two, the count stays unregistered (PR #549, review B2)."""
    registering = [
        {"id": "T-101", "scope": {"n_values": [6, 7]}, "attribution": {"source_keys": ["[A]"]}},
        {
            "id": "T-155",
            "scope": {"n_values": [6, 7]},
            "regularizations": [{"n": 6, "side": "solved"}, {"n": 7, "side": "same"}],
        },
    ]

    def resolve(n: int, relation: str, *, at: bool = False) -> Any:
        found = entry(n, relation)
        return drawings.packing_result(
            found,
            registering,
            source_key="[B]",
            bound_holders=["T-101", "T-155"],
            side_at_bound=at,
        )

    # A `bound` view resolves only while its side is the bound (#548 review B1).
    assert resolve(6, "bound", at=True).of == "T-155"
    assert resolve(6, "bound").of is None
    assert resolve(7, "same", at=True).of == "T-155"
    # A `bound` drawing where the registering result's item is on the other side, or a
    # count no item names, keeps both holders and so no answer.
    assert resolve(7, "bound", at=True).of is None
    assert "T-101" in resolve(7, "bound", at=True).reason
    assert drawings.registering_holders(8, ["T-101", "T-155"], registering, side="solved") == [
        "T-101",
        "T-155",
    ]


def test_the_block_reads_back_as_the_items_it_was_written_from() -> None:
    item = drawings.item(entry(5), "T-001")
    assert "of_witness" not in item
    assert "provenance" not in item
    text = drawings.block_text([item], [{"n": 7, "reason": "no registered result: [B]"}])
    assert text.startswith(drawings.MARKER)
    document = safe_load(text)[drawings.KEY]
    assert document["items"] == [item]
    assert document["unregistered"] == [{"n": 7, "reason": "no registered result: [B]"}]
    head, block = drawings.split("results: []\n\n" + text)
    assert (head, block) == ("results: []\n\n", text)


def test_a_number_in_exponent_form_reads_back_as_a_number() -> None:
    # n = 84's identity measures a turn of 1e-15 degrees, which JSON prints without a
    # point and YAML 1.1 then reads as a string.
    for value in (1e-15, 2e-07, 7.516648e-20, 1.5e300, 0.0, 2.35479, 3):
        assert safe_load(f"x: {drawings.scalar(value)}\n")["x"] == value


def test_the_checker_holds_each_item_to_the_register() -> None:
    scopes = {"T-001": {5, 6}, "T-002": {5, 6, 7, 8, 9}}
    good = drawings.item(entry(5), "T-001")
    register = {"regularized_drawings": {"items": [good], "unregistered": []}}
    assert regularized_drawings_problems(register, scopes, drift=False) == []
    elsewhere = {**good, "n": 7, "of": "T-001"}
    stranger = {**good, "n": 8, "of": "T-099", "by": "[A]"}
    lost = {**good, "n": 9, "of": "T-002", "identity": {**good["identity"], "moved": 10}}
    register = {
        "regularized_drawings": {
            "items": [good, good, elsewhere, stranger, lost],
            "unregistered": [{"n": 5, "reason": "x"}],
        }
    }
    assert regularized_drawings_problems(register, scopes, drift=False) == [
        "regularized drawing at n = 5 is listed twice",
        "regularized drawing at n = 7 names T-001, whose scope does not hold n = 7",
        "regularized drawing at n = 8 names T-099, which is not registered",
        "regularized drawing at n = 8 is by [A], not `project`",
        "regularized drawing at n = 9: identity.moved, 10, is more squares than n = 9",
        "regularized drawing at n = 5 is both an item and unregistered",
    ]


def test_the_modifications_are_read_from_the_index_entry_alone() -> None:
    """Which of this project's modifications to Evan Daniel's regularizer made a view
    (the owner, 13 October 2026): the rungs its solve climbed, the patches its method
    names, the same-side re-solve; the grid-slack port names itself; the axis tool is not
    his regularizer, so it has none to name."""
    kinds = {"probe-flat-stall-stop": "replica"}
    evand = {**entry(5, "same"), "generator": drawings.EVAND_GENERATOR}
    assert drawings.project_modifications(evand, kinds) == [drawings.SAME_SIDE_RESOLVE]
    bound = {**entry(5, "bound"), "generator": drawings.EVAND_GENERATOR}
    assert drawings.project_modifications(bound, kinds) == []
    # Before the retry ladder the index kept the one retry's arguments.
    legacy = {**evand, "run": {"id": "r", "retried_with": ["--dps", "100"]}}
    assert drawings.project_modifications(legacy, kinds) == [
        "retry rung dps-100",
        drawings.SAME_SIDE_RESOLVE,
    ]
    patched = {
        **bound,
        "run": {"id": "r", "rungs": ["force-kkt", "stall-stop", "first-pass"]},
        "regularization": {
            **bound["regularization"],
            "method": "Evan Daniel's search/regularize (MIT), "
            "evand/square-packing@675a5ea+probe-flat-stall-stop, conservative, coincide",
        },
    }
    assert drawings.project_modifications(patched, kinds) == [
        "retry rung force-kkt",
        "retry rung first-pass (devtools.regularize_evand_first_pass)",
        "replica patch probe-flat-stall-stop",
    ]
    grid = {**entry(5, "same"), "generator": "regularize_grid_slack/1"}
    assert drawings.project_modifications(grid, kinds) == [
        "port of his coincidence placement (regularize_grid_slack/1) rather than his code",
        drawings.SAME_SIDE_RESOLVE,
    ]
    axis = {**entry(5), "generator": "regularize_axis_components/2"}
    assert drawings.project_modifications(axis, kinds) is None
    # The register's item carries them where his method made the view, and only there.
    assert drawings.item(evand, "T-001", [])["modifications"] == []
    assert "modifications" not in drawings.item(axis, "T-001", None)


def test_an_unknown_generator_rung_or_registering_kind_is_refused() -> None:
    """Credit and modifications fail closed: a generator the tool does not map, a rung or
    retry argument it has no words for, and a registering result that is not an upper
    bound are refused, never credited or read as unmodified by default. The stall-stop
    rung alone is silent, since its one change is the replica patch `method` names."""
    kinds: dict[str, str] = {}
    stranger = {**entry(5, "same"), "generator": "someone-elses-tool"}
    with pytest.raises(drawings.RegularizedDrawingsError, match="someone-elses-tool"):
        drawings.project_modifications(stranger, kinds)
    with pytest.raises(drawings.RegularizedDrawingsError, match="someone-elses-tool"):
        drawings.project_case_item(
            drawings.Drawn(stranger, drawings.Resolved("T-001", "x"), None), {}
        )
    evand = {**entry(5, "bound"), "generator": drawings.EVAND_GENERATOR}
    with pytest.raises(drawings.RegularizedDrawingsError, match="names no credit"):
        drawings.project_case_item(
            drawings.Drawn(evand, drawings.Resolved("T-001", "x"), []), {}
        )
    for run in (
        {"id": "r", "rungs": ["dps-200"]},
        {"id": "r", "retried_with": ["--dps", "80"]},
        {"id": "r", "retried_with": ["--relax"]},
    ):
        with pytest.raises(drawings.RegularizedDrawingsError, match="n=5"):
            drawings.project_modifications({**evand, "run": run}, kinds)
    stalled = {**evand, "run": {"id": "r", "rungs": ["stall-stop"]}}
    assert drawings.project_modifications(stalled, kinds) == []
    assert drawings.upper_bound_result({"id": "T-003", "kind": "upper-bound"}) == "T-003"
    with pytest.raises(drawings.RegularizedDrawingsError, match="T-004 registers"):
        drawings.upper_bound_result({"id": "T-004", "kind": "lower-bound"})


def test_a_case_note_credits_the_regularizer_and_is_never_a_result() -> None:
    evand = {**entry(5, "same"), "generator": drawings.EVAND_GENERATOR}
    count = drawings.Drawn(evand, drawings.Resolved("T-001", "x"), [drawings.SAME_SIDE_RESOLVE])
    generators = {drawings.EVAND_GENERATOR: {"credit": "Regularized by the Squares Project"}}
    ours = drawings.project_case_item(count, generators)
    assert ours["by"] == "project"
    assert ours["side"] == "same"
    note = drawings.case_note([ours])
    assert note == (
        "Regularized by the Squares Project, with the project's modifications: "
        f"{drawings.SAME_SIDE_RESOLVE}. A drawing of T-001's packing at the witness's own "
        "side: a pure regularization, which proves no new bound, so not a result."
    )
    plain = drawings.project_case_item(
        drawings.Drawn(evand, drawings.Resolved(None, "none"), []), generators
    )
    assert plain["of"] is None
    assert drawings.case_note([plain]).startswith(
        "Regularized by the Squares Project, unmodified."
    )
    axis = {**entry(5), "generator": "regularize_axis_components/2"}
    own = drawings.project_case_item(
        drawings.Drawn(axis, drawings.Resolved("T-001", "x"), None), {}
    )
    assert own["credit"] == drawings.AXIS_CREDIT
    assert "modifications" not in own
    source = {
        "by": "[A]",
        "credit": "A after B",
        "of": "T-002",
        "registered_in": "T-003",
        "method": "fewest",
        "side": "solved",
    }
    assert drawings.case_note([source, own]).endswith(
        "The house is itself its source's regularization of T-002's packing (A after B), "
        "registered as T-003 for the upper bound its exact side proves."
    )


def test_a_drawing_whose_exact_side_is_registered_says_so() -> None:
    """Where the drawn packing's own result registers this very regularization (a
    `by: project` item at the count, by the drawn view's method, at its side relation),
    the item names it as `registered_in` and the note says its exact side is registered
    as that result, which proves a new bound; a drawing by another method or at another
    side is a pure regularization."""
    method = "Evan Daniel's search/regularize, through devtools.regularize_evand"
    results = [
        {
            "id": "T-155",
            "kind": "upper-bound",
            "regularizations": [
                {"n": 5, "of": "T-001", "by": "project", "method": method, "side": "solved"}
            ],
        }
    ]
    bound = {**entry(5, "bound"), "generator": drawings.EVAND_GENERATOR}
    count = drawings.Drawn(bound, drawings.Resolved("T-155", "x"), [])
    assert drawings.registering_result(count, results) == "T-155"
    generators = {drawings.EVAND_GENERATOR: {"credit": "Regularized by the Squares Project"}}
    ours = drawings.project_case_item(count, generators, "T-155")
    assert ours["registered_in"] == "T-155"
    assert drawings.case_note([ours]) == (
        "Regularized by the Squares Project, unmodified. A drawing of T-155's packing at the "
        "verified upper bound. Its exact side is registered as T-155, the upper bound it "
        "proves; the drawing itself is no further result."
    )
    same = drawings.Drawn(
        {**entry(5, "same"), "generator": drawings.EVAND_GENERATOR},
        drawings.Resolved("T-155", "x"),
        [],
    )
    assert drawings.registering_result(same, results) is None
    grid = {**bound, "generator": "regularize_grid_slack/1"}
    grid["regularization"] = {**bound["regularization"], "method": "regularize_grid_slack/1"}
    assert (
        drawings.registering_result(drawings.Drawn(grid, count.resolved, []), results) is None
    )
    elsewhere = drawings.Drawn(bound, drawings.Resolved("T-001", "x"), [])
    assert drawings.registering_result(elsewhere, results) is None
    lower = [{**results[0], "kind": "lower-bound"}]
    with pytest.raises(drawings.RegularizedDrawingsError, match="not an upper-bound"):
        drawings.registering_result(count, lower)


GENERATORS = {
    drawings.EVAND_GENERATOR: {
        "method": "Evan Daniel's search/regularize (MIT), evand/square-packing@675a5ea, "
        "conservative",
        "credit": "Regularized by the Squares Project with Evan Daniel's regularizer",
    },
    "regularize_grid_slack/0": {"method": "regularize_grid_slack/0: a port", "credit": "G"},
    drawings.AXIS_GENERATOR: {"method": "regularize_axis_components/2"},
}
EVAND_METHOD = GENERATORS[drawings.EVAND_GENERATOR]["method"]
REGISTER = """results:
  - id: T-153
    kind: upper-bound
    regularizations:
      - n: 7
        of: T-001
        by: project
        method: "{method}"
        side: same
        identity:
          basis: measured
      - n: 8
        of: T-001
        by: project
        method: "{method}"
        modifications: ["stale"]
        side: solved
        identity:
          basis: measured
  - id: T-155
    kind: upper-bound
    regularizations:
      - n: 9
        of: T-001
        by: "[A]"
        method: fewest
        side: solved
        identity:
          basis: source-claim
"""


def test_a_registered_regularization_names_what_its_item_establishes() -> None:
    """A registered result's own regularization names this project's modifications as a
    drawing's are read, from its method and side, and says the retry rungs are not
    recorded, since an item records no solve; an unknown method is refused."""
    same = {"method": EVAND_METHOD, "side": "same"}
    assert drawings.registered_modifications(same, GENERATORS, {}) == (
        [drawings.SAME_SIDE_RESOLVE],
        [drawings.UNRECORDED_RUNGS],
    )
    solved = {"method": EVAND_METHOD, "side": "solved"}
    assert drawings.registered_modifications(solved, GENERATORS, {}) == (
        [],
        [drawings.UNRECORDED_RUNGS],
    )
    patched = {
        "method": EVAND_METHOD.replace("@675a5ea", "@675a5ea+probe-flat-stall-stop"),
        "side": "solved",
    }
    assert drawings.registered_modifications(
        patched, GENERATORS, {"probe-flat-stall-stop": "replica"}
    ) == (["replica patch probe-flat-stall-stop"], [drawings.UNRECORDED_RUNGS])
    grid = {"method": "regularize_grid_slack/0: a port", "side": "same"}
    assert drawings.registered_modifications(grid, GENERATORS, {}) == (
        drawings.grid_modifications("regularize_grid_slack/0", same=True),
        [],
    )
    written = {
        "method": "regularize_grid_slack/0: a port" + drawings.GRID_THROUGH,
        "side": "same",
    }
    assert drawings.registered_modifications(written, GENERATORS, {}) == (
        drawings.grid_modifications("regularize_grid_slack/0", same=True),
        [],
    )
    axis = {"method": "regularize_axis_components/2", "side": "same"}
    assert drawings.registered_modifications(axis, GENERATORS, {}) == (None, [])
    through = {"method": "regularize_axis_components/2" + drawings.GRID_THROUGH, "side": "same"}
    with pytest.raises(drawings.RegularizedDrawingsError, match="no generator"):
        drawings.registered_modifications(through, GENERATORS)
    with pytest.raises(drawings.RegularizedDrawingsError, match="no generator"):
        drawings.registered_modifications({"method": "x", "side": "same"}, GENERATORS)


def test_registered_modifications_are_written_in_place_and_held() -> None:
    """The register's `by: project` items gain their modifications after `method`, a stale
    value is replaced, a source's item is left alone, and the check names the result."""
    text = REGISTER.format(method=EVAND_METHOD)
    results = safe_load(text)["results"]
    written = drawings.with_registered_modifications(text, results, GENERATORS)
    found = safe_load(written)["results"]
    seven, eight = found[0]["regularizations"]
    assert seven["modifications"] == [drawings.SAME_SIDE_RESOLVE]
    assert seven["modifications_unrecorded"] == ["retry rungs"]
    assert eight["modifications"] == []
    assert "modifications" not in found[1]["regularizations"][0]
    assert list(seven)[:6] == [
        "n",
        "of",
        "by",
        "method",
        "modifications",
        "modifications_unrecorded",
    ]
    assert drawings.with_registered_modifications(written, found, GENERATORS) == written
    assert drawings.registered_problems(written, GENERATORS) == []
    (problem,) = drawings.registered_problems(text, GENERATORS)
    assert "['T-153']" in problem


def test_a_registered_regularization_the_layer_does_not_draw_is_credited() -> None:
    """Where a result registers this project's regularization of a count and the layer
    does not draw it, the case record still credits the Squares Project and names the
    result, in the register's terms; a drawn regularization the result registers is the
    drawn item's, and a source's regularization is not this project's."""
    results = safe_load(REGISTER.format(method=EVAND_METHOD))["results"]
    found = drawings.registered_case_items(results, GENERATORS, {("T-153", 8)})
    assert sorted(found) == [7]
    seven = found[7]
    assert seven == {
        "by": "project",
        "credit": GENERATORS[drawings.EVAND_GENERATOR]["credit"],
        "generator": drawings.EVAND_GENERATOR,
        "method": EVAND_METHOD,
        "modifications": [drawings.SAME_SIDE_RESOLVE],
        "modifications_unrecorded": ["retry rungs"],
        "side": "same",
        "of": "T-001",
        "registered_in": "T-153",
    }
    assert drawings.case_note([seven]) == (
        "Regularized by the Squares Project with Evan Daniel's regularizer, with the "
        f"project's modifications: {drawings.SAME_SIDE_RESOLVE}; whether its solve climbed "
        "a retry rung is not recorded. A regularization of T-001's packing at the "
        "witness's own side, not drawn here; its exact side is registered as T-153, the "
        "upper bound it proves."
    )
    solved = drawings.registered_case_items(results, GENERATORS)[8]
    assert drawings.case_note([solved]).startswith(
        "Regularized by the Squares Project with Evan Daniel's regularizer, with none of "
        "the project's modifications established; whether its solve climbed a retry rung "
        "is not recorded."
    )
    # Beside a drawing by another method, it follows the drawing's sentences.
    grid = {**entry(7, "same"), "generator": "regularize_grid_slack/0"}
    drawn = drawings.project_case_item(
        drawings.Drawn(grid, drawings.Resolved("T-153", "x"), []), GENERATORS
    )
    assert "Also regularized by the Squares Project" in drawings.case_note([drawn, seven])
    lower = [{**results[0], "kind": "lower-bound"}]
    with pytest.raises(drawings.RegularizedDrawingsError, match="not an upper-bound"):
        drawings.registered_case_items(lower, GENERATORS)


def test_the_case_field_is_written_in_place_and_removed_whole() -> None:
    text = "---\npacking:\n  n: 5\n  resources: []\n---\n# s(5)\n"
    field = {"note": "A drawing, not a result.", "items": [{"by": "project", "of": None}]}
    written = drawings.with_case_field(text, field)
    front = safe_load(written.split("---\n")[1])["packing"]
    assert front[drawings.CASE_FIELD] == field
    assert written.endswith("---\n# s(5)\n")
    assert drawings.with_case_field(written, field) == written
    changed = drawings.with_case_field(written, {**field, "note": "Another."})
    assert safe_load(changed.split("---\n")[1])["packing"][drawings.CASE_FIELD]["note"] == (
        "Another."
    )
    assert drawings.with_case_field(written, None) == text


def test_a_side_an_earlier_certificate_first_stated_proves_no_new_bound() -> None:
    """Where the registering result's item names the earlier result whose certificate
    first stated its exact side (`first_certified_in`), as T-155's 33 items at the side of
    Evan Daniel's certificates name T-101, the drawn and the undrawn notes credit the
    Squares Project, say the side is registered in the result and was first certified by
    that certificate, naming it, and that it proves no new bound; without the field the
    side is the upper bound it proves (PR #585, review B1)."""
    record = {
        "n": 5,
        "of": "T-101",
        "by": "project",
        "method": EVAND_METHOD,
        "side": "solved",
        "first_certified_in": "T-101",
        "identity": {"basis": "measured"},
    }
    results = [{"id": "T-155", "kind": "upper-bound", "regularizations": [record]}]
    bound = {**entry(5, "bound"), "generator": drawings.EVAND_GENERATOR}
    bound["regularization"] = {**bound["regularization"], "method": EVAND_METHOD}
    count = drawings.Drawn(bound, drawings.Resolved("T-155", "x"), [])
    registered = drawings.registered_record(count, results)
    assert registered is not None
    assert registered == ("T-155", record)
    drawn = drawings.project_case_item(count, GENERATORS, "T-155", "T-101")
    assert drawn["first_certified_in"] == "T-101"
    assert "first_certified_in" not in drawings.project_case_item(
        count, GENERATORS, None, "T-101"
    )
    certificates = {"T-101": "Evan Daniel's certificate"}
    assert drawings.case_note([drawn], certificates) == (
        "Regularized by the Squares Project with Evan Daniel's regularizer, unmodified. A "
        "drawing of T-155's packing at the verified upper bound. Its exact side is "
        "registered in T-155, and the same side was first certified by Evan Daniel's "
        "certificate (T-101), so it proves no new bound; the drawing itself is no further "
        "result."
    )
    undrawn = drawings.registered_case_items(results, GENERATORS)[5]
    assert undrawn["first_certified_in"] == "T-101"
    assert drawings.case_note([undrawn], certificates) == (
        "Regularized by the Squares Project with Evan Daniel's regularizer, with none of "
        "the project's modifications established; whether its solve climbed a retry rung "
        "is not recorded. A regularization of T-101's packing solved to its side, not drawn "
        "here; its exact side is registered in T-155, and the same side was first "
        "certified by Evan Daniel's certificate (T-101), so it proves no new bound."
    )
    new = {key: value for key, value in undrawn.items() if key != "first_certified_in"}
    assert drawings.case_note([new]).endswith(
        "its exact side is registered as T-155, the upper bound it proves."
    )
    register = cast(
        Any,
        SimpleNamespace(
            results=[
                {"id": "T-101", "attribution": {"source_keys": ["[D]"]}},
                {"id": "T-009"},
            ],
            sources={"[D]": SimpleNamespace(authors=("Daniel",))},
            names={"Evan Daniel": "Daniel"},
        ),
    )
    assert drawings.certificate_words("T-101", register) == "Evan Daniel's certificate"
    assert drawings.certificate_words("T-009", register) == "this project's certificate"
    assert drawings.certificate_words("T-999", register) == "T-999's certificate"


def test_the_earlier_certificate_is_named_exactly_where_the_case_bound_rests_on_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An item names `first_certified_in` exactly where the case's verified upper bound
    rests on an earlier registered result beside the registering one: a missing name, a
    name the bound does not rest on, and a name where the registering result alone proves
    the bound are listed; a later result proving the same bound needs none (PR #585,
    review B1). Where a later house adoption holds the count, the bound rests on the house
    alone and the item is history, its name kept."""
    holders = {
        5: ["T-101", "T-155"],
        6: ["T-101", "T-155"],
        7: ["T-155"],
        8: ["T-155"],
        9: ["T-155", "T-160"],
        10: ["T-101", "T-155"],
        11: ["T-170"],
    }
    monkeypatch.setattr(drawings, "bound_holders", lambda n, _register: holders[n])
    monkeypatch.setattr(registration, "readopted_by", lambda n, rid: (n, rid) == (11, "T-155"))

    def item(n: int, first: str | None = None) -> dict[str, Any]:
        found: dict[str, Any] = {"n": n, "of": "T-101", "by": "project", "side": "solved"}
        if first:
            found["first_certified_in"] = first
        return found

    register = cast(
        Any,
        SimpleNamespace(
            results=[
                {"id": "T-101", "attribution": {"published": "2026-10-05"}},
                {
                    "id": "T-155",
                    "established": "2026-10-12",
                    "regularizations": [
                        item(5, "T-101"),
                        item(6),
                        item(7, "T-101"),
                        item(8),
                        item(9),
                        item(10, "T-160"),
                        item(11, "T-101"),
                    ],
                },
                {"id": "T-160", "established": "2026-10-20"},
                {"id": "T-170", "established": "2026-10-21"},
            ]
        ),
    )
    assert drawings.first_certified_problems(register) == [
        (
            "T-155's regularization at n = 6: the case's verified upper bound rests on "
            "['T-101'] as well, whose certificate stated the side first; name it as "
            "first_certified_in"
        ),
        (
            "T-155's regularization at n = 7 names T-101 as first_certified_in, but the "
            "case's verified upper bound rests on ['T-155']"
        ),
        (
            "T-155's regularization at n = 10 names T-160 as first_certified_in, but the "
            "case's verified upper bound rests on ['T-101', 'T-155']"
        ),
    ]


def test_a_registered_item_reads_the_rungs_of_the_solve_the_layer_draws(
    tmp_path: Path,
) -> None:
    """Where the layer draws the very solve a result registered (the result registers the
    drawing, and its registration receipt names, at the count, a run whose receipt the
    entry's run block records, with the entry's output and exact side), the item reads
    its rungs from the drawn entry and leaves nothing unrecorded; a later run's view at
    the same side, another output or side, or no receipt says nothing of that solve
    (PR #585, review B2)."""
    record = {
        "n": 5,
        "of": "T-101",
        "by": "project",
        "method": EVAND_METHOD,
        "side": "solved",
        "identity": {"basis": "measured"},
    }
    parameters = {"variant": "conservative", "workers": 4}
    receipt = {
        "format": drawings.REGISTRATION_RECEIPT,
        "runs": [
            {
                "run": "full",
                "generator": {"name": drawings.EVAND_GENERATOR},
                "parameters": {**parameters, "timeout": 1800.0},
                "cost": {"cpu_seconds": 10.0, "wall_seconds": 5.0, "workers": 4, "counts": 1},
            }
        ],
        "rows": [{"n": 5, "run": "full", "output": "solved", "side": "33/5"}],
    }
    (tmp_path / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
    results = [
        {
            "id": "T-155",
            "kind": "upper-bound",
            "artifacts": ["receipt.json"],
            "regularizations": [record],
        }
    ]
    cost = {"cpu_seconds": 10.0, "wall_seconds": 5.0, "workers": 4}
    runs = [
        {
            "id": "refreshed-full",
            "generator": drawings.EVAND_GENERATOR,
            "parameters": parameters,
            "cost": cost,
        },
        {
            "id": "later",
            "generator": drawings.EVAND_GENERATOR,
            "parameters": parameters,
            "cost": {**cost, "cpu_seconds": 1.0},
        },
    ]

    def drawn(run: str = "refreshed-full", output: str = "solved", side: str = "33/5") -> Any:
        found = {**entry(5, "bound"), "generator": drawings.EVAND_GENERATOR}
        found["regularization"] = {**found["regularization"], "method": EVAND_METHOD}
        found["run"] = {"id": run, "output": output}
        found["side"] = {"relation": "bound", "view": side}
        return drawings.Drawn(found, drawings.Resolved("T-155", "x"), [])

    count = drawn()
    solves = drawings.recorded_solves([count], results, runs, repo=tmp_path)
    assert solves == {("T-155", 5): count.entry}
    assert drawings.registered_modifications(record, GENERATORS, {}, count.entry) == ([], [])
    assert drawings.registered_modifications(record, GENERATORS, {}) == (
        [],
        [drawings.UNRECORDED_RUNGS],
    )
    climbed = {**count.entry, "run": {**count.entry["run"], "rungs": ["force-kkt"]}}
    assert drawings.registered_modifications(record, GENERATORS, {}, climbed) == (
        ["retry rung force-kkt"],
        [],
    )
    for other in (drawn("later"), drawn(output="same"), drawn(side="34/5")):
        assert drawings.recorded_solves([other], results, runs, repo=tmp_path) == {}
    # A reclassified copy records no cost of its own (#548 review B5): its source's
    # cost is the receipt's, so the copy's views answer as that run's solves.
    copied = {
        "id": "copied",
        "generator": drawings.EVAND_GENERATOR,
        "parameters": parameters,
        "cost": {**cost, "cpu_seconds": 0.0, "wall_seconds": 0.0},
        "reclassified_from": "refreshed-full",
    }
    copy = drawn("copied")
    found = drawings.recorded_solves([copy], results, [*runs, copied], repo=tmp_path)
    assert found == {("T-155", 5): copy.entry}
    alone = drawings.recorded_solves([copy], results, [copied], repo=tmp_path)
    assert alone == {}
    bare = [{**results[0], "artifacts": []}]
    assert drawings.recorded_solves([count], bare, runs, repo=tmp_path) == {}
    text = f"""results:
  - id: T-155
    kind: upper-bound
    regularizations:
      - n: 5
        of: T-101
        by: project
        method: "{EVAND_METHOD}"
        side: solved
        identity:
          basis: measured
"""
    written = drawings.with_registered_modifications(
        text, safe_load(text)["results"], GENERATORS, solves
    )
    (five,) = safe_load(written)["results"][0]["regularizations"]
    assert five["modifications"] == []
    assert "modifications_unrecorded" not in five
    assert drawings.registered_problems(written, GENERATORS, solves) == []
    assert drawings.registered_problems(written, GENERATORS) != []


def test_t155_names_daniels_earlier_certificate_where_its_side_is_his() -> None:
    """On the record: T-155's items that name `first_certified_in` are exactly the rows of
    its registration receipt whose side is that of Evan Daniel's earlier certificate
    (`register_regularized_bounds.at_t101_side`), 33 of its 59, each naming T-101; eight
    are drawn and 25 are not. Their case notes say the side is registered in T-155 and
    was first certified by Evan Daniel's certificate (T-101), so it proves no new bound;
    the other 26 say it is the upper bound it proves. The layer draws T-155's own solve
    at fourteen counts, whose items read their rungs from the drawn entries; at 87 it
    draws a later run's view, so T-155's item there keeps the rungs unrecorded (PR #585,
    review B1, B2)."""
    register = drawings.load_register()
    (t155,) = (result for result in register.results if result["id"] == "T-155")
    items = {int(item["n"]): item for item in t155["regularizations"]}
    receipt = json.loads(registration.FIRST.selection.read_text(encoding="utf-8"))
    at_daniel = {int(row["n"]) for row in receipt["rows"] if registration.at_t101_side(row)}
    named = {n for n, item in items.items() if item.get("first_certified_in")}
    assert named == at_daniel
    assert len(named) == 33
    assert len(items) - len(named) == 26
    assert {items[n]["first_certified_in"] for n in named} == {"T-101"}
    index = drawings.index_document()
    drawn = drawings.drawn_counts(index)
    fields = drawings.case_fields(index, drawn=drawn)
    # At 264 the drawing is of the house a later adoption put there (T-158), not of
    # T-155's packing, whose item there is history (`registration.readopted`).
    drawn_named = sorted(
        n
        for n in named
        if not registration.readopted(n)
        and any("view" in found for found in fields[n]["items"] if found["by"] == "project")
    )
    assert drawn_named == [83, 87, 107, 171, 198, 230, 234, 293]
    first = (
        "registered in T-155, and the same side was first certified by Evan Daniel's "
        "certificate (T-101), so it proves no new bound"
    )
    for n in items:
        note = " ".join(fields[n]["note"].split())
        if n in named:
            assert first in note, n
            assert "the upper bound it proves" not in note, n
        else:
            assert "registered as T-155, the upper bound it proves" in note, n
            assert "first certified" not in note, n
    solves = drawings.recorded_solves(drawn, register.results, index.get("runs") or [])
    assert sorted(n for _rid, n in solves) == [
        29, 37, 41, 50, 54, 71, 83, 107, 171, 178, 198, 230, 234, 293,
    ]  # fmt: skip
    for n, item in items.items():
        assert ("modifications_unrecorded" in item) == (("T-155", n) not in solves), n


def test_a_side_a_larger_counts_ceiling_already_proved_is_no_new_bound() -> None:
    """Where a larger count's verified upper bound already proved the bound when the side
    was registered, as T-155's certificate at n = 291 proved T-156's at n = 290, the
    registering result's receipt records it (`implied_by`), and the note says the side is
    registered in the result and that the certificate registered at that count already
    proved the bound by monotonicity, so it proves no new bound, rather than calling it the
    upper bound it proves (PR #587, review C1)."""
    record = {
        "n": 5,
        "of": "T-101",
        "by": "project",
        "method": EVAND_METHOD,
        "side": "same",
        "identity": {"basis": "measured"},
    }
    results = [{"id": "T-156", "kind": "upper-bound", "regularizations": [record]}]
    undrawn = drawings.registered_case_items(results, GENERATORS)[5]
    implied = {"n": 6, "side": "3", "evidence": ["E-x"], "results": ["T-155"]}
    note = drawings.case_note([undrawn], {}, {"T-156": implied})
    assert note.endswith(
        "not drawn here; its exact side is registered in T-156, and the certificate "
        "registered at n = 6 (T-155) already proved the bound by monotonicity, so it "
        "proves no new bound."
    )
    assert "the upper bound it proves" not in note
    # Another result's ceiling says nothing of this one's.
    assert drawings.case_note([undrawn], {}, {"T-999": implied}).endswith(
        "its exact side is registered as T-156, the upper bound it proves."
    )


def test_t156s_note_says_its_bound_follows_from_t155_by_monotonicity() -> None:
    """On the record: T-156's receipt records T-155's certificate at n = 291 as the ceiling
    that already proved its bound, and it is the only registered regularization whose
    receipt records one, so n = 290's note says so and no note calls T-156's side the
    upper bound it proves (PR #587, review C1)."""
    register = drawings.load_register()
    implied = drawings.implied_bounds(register.results)
    assert set(implied) == {("T-156", 290)}
    assert implied["T-156", 290]["n"] == 291
    assert implied["T-156", 290]["results"] == ["T-155"]
    front = safe_load(
        (drawings.REPO / "packing/frontier/n-290.md")
        .read_text(encoding="utf-8")
        .split("---\n")[1]
    )
    note = " ".join(front["packing"][drawings.CASE_FIELD]["note"].split())
    assert (
        "its exact side is registered in T-156, and the certificate registered at n = 291 "
        "(T-155) already proved the bound by monotonicity, so it proves no new bound."
    ) in note
    assert "the upper bound it proves" not in note


def test_the_generated_block_check_fails_on_an_edited_block() -> None:
    """`problems` holds the committed block to what the layer's index generates, so an
    edit to it fails the records tier rather than passing until the next regeneration
    (#548 review B6)."""
    text = drawings.RESULTS.read_text(encoding="utf-8")
    index = drawings.index_document()
    assert drawings.problems(text, index) == []
    head, block = drawings.split(text)
    named = safe_load(block)[drawings.KEY]["items"]
    first, second = named[0], named[1]

    edited = block.replace(f"      of: {first['of']}\n", "      of: T-999\n", 1)
    assert edited != block
    (problem,) = drawings.problems(head + edited, index)
    assert problem.startswith(f"results.yaml's {drawings.KEY} differs")

    renumbered = block.replace(f"    - n: {second['n']}\n", "    - n: 999\n", 1)
    (problem,) = drawings.problems(head + renumbered, index)
    assert f"items for [{second['n']}] missing, [999] extra" in problem

    (problem,) = drawings.problems(head, index)
    assert "missing" in problem
