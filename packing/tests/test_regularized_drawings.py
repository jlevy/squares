"""The register's record of the regularized drawings, on synthetic entries.

Which registered result holds a drawn count's packing: the one attributing the
witness's source for a view at the witness's side, the one the verified upper bound rests
on for a view at the bound or for a view at a witness's side that is exactly the bound
where no result attributes the source, and none where no result answers or several do.
The generated block reads back as the data it was written from, and the register's
checker holds each item to the register.
"""

from __future__ import annotations

from typing import Any

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
