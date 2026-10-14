"""The grid-slack prototype on fixtures whose best drawing is known by hand.

Four unit squares scattered in a side-11/5 box can at best form a 2 x 2 block in a
corner, and the lower-left corner is the one nearest the start in L1: the view must put
them on exact halves there, at exactly the witness's side, decided on both exact routes,
with no house or stage total falling and every square paired one to one. A square turned
by `2 arctan(1/500)` (about 0.229 degrees) beside an axis square is straightened and
slid flush. A run directory under `witnesses/` is refused before anything is written.
When both ways of closing the tight set fail, the re-solve holds the unchanged squares at
their exact centres and tries again, and a literal past Python's integer-text limit moves
on to the next way rather than refusing the count. A rational `U` below the witness's side
is tried first, and one above it only after the witness's own side; the layer's generator
block keeps the defaults whatever threshold a run used.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import census_drawing_regularity as census
from devtools import regularize_axis_components as axis
from devtools import regularize_evand as driver
from devtools import regularize_grid_slack as slack
from devtools import render_regularized_atlas as render
from devtools.regularize_evand import Decision, view_geometry
from sqpack.yamlio import load_yaml

HALF = Fraction(1, 2)


REAL_RATIONAL_BOUND = slack.rational_bound


@pytest.fixture(autouse=True)
def _no_record_bound(monkeypatch: pytest.MonkeyPatch) -> None:
    """The synthetic fixtures borrow real counts (2, 4) whose case records' bounds would
    otherwise be tried first; a test that wants a record's bound restores it."""
    monkeypatch.setattr(slack, "rational_bound", lambda _n: None)


def _basis_witness(
    rows: list[tuple[Fraction, Fraction, Fraction, Fraction]], side: str = "11/5"
) -> dict[str, Any]:
    """A rational centre-basis witness, in a side-11/5 box unless `side` says otherwise."""

    def text(value: Fraction) -> str:
        return str(value.numerator) if value.denominator == 1 else str(value)

    return {
        "id": "W-fixture",
        "n": len(rows),
        "side": side,
        "square_size": "1",
        "representation": "center-basis",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {"id": index, "center": [text(x), text(y)], "basis": [text(c), text(s)]}
            for index, (x, y, c, s) in enumerate(rows, start=1)
        ],
        "claim": {
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "limitations": "synthetic fixture",
        },
        "source": {"path": "tests/synthetic"},
    }


def scattered() -> dict[str, Any]:
    """Four axis squares, each a few hundredths to a seventh off a 2 x 2 corner block."""
    one, zero = Fraction(1), Fraction(0)
    return _basis_witness(
        [
            (HALF + Fraction(1, 20), HALF + Fraction(1, 20), one, zero),
            (Fraction(16, 10), HALF, one, zero),
            (HALF, Fraction(16, 10), one, zero),
            (Fraction(165, 100), Fraction(165, 100), one, zero),
        ]
    )


def tilted() -> dict[str, Any]:
    """An axis square on the floor and a square turned about 0.229 degrees beside it."""
    t = Fraction(1, 500)
    c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    one, zero = Fraction(1), Fraction(0)
    return _basis_witness([(HALF, HALF, one, zero), (Fraction(16, 10), Fraction(6, 10), c, s)])


def _centres(view: dict[str, Any]) -> list[tuple[Fraction, Fraction]]:
    _side, placements, _corners = view_geometry(view)
    return [(x, y) for x, y, _c, _s in placements]


def test_scattered_squares_close_into_the_nearest_corner_block() -> None:
    view, report = slack.regularize(scattered(), slack.Settings())
    assert view is not None
    assert report["relation"] == "same"
    (first,) = report["attempts"]
    assert first["placement"]["status"] == "placed"
    assert Fraction(view["side"]) == Fraction(11, 5)
    assert _centres(view) == [
        (HALF, HALF),
        (Fraction(3, 2), HALF),
        (HALF, Fraction(3, 2)),
        (Fraction(3, 2), Fraction(3, 2)),
    ]
    verdicts = first["exact"]["verdicts"]
    assert verdicts["exact_verify"]["passed"]
    assert verdicts["independent"]["passed"]
    drawn = census.regularity(view)
    assert drawn["axis_sides"] == [0, 0, 1, 2, 1]
    assert drawn["uneven_axis"] == 3
    measured = slack.measure(4, scattered(), view, [])
    assert measured["identity"]["one_to_one"] is True
    assert measured["totals_fall"] is False
    assert view["certificate"]["kind"] == "regularized-view"
    assert view["certificate"]["side_relation"] == "same"


def test_a_near_axis_square_is_straightened_and_slid_flush() -> None:
    view, report = slack.regularize(tilted(), slack.Settings())
    assert view is not None
    assert [row["square"] for row in report["straightened"]] == [2]
    assert report["straightened"][0]["degrees"] == pytest.approx(0.229183, abs=1e-6)
    assert view["squares"][1]["basis"] == ["1", "0"]
    assert _centres(view) == [(HALF, HALF), (Fraction(3, 2), HALF)]
    assert view["certificate"]["straightened"] == [2]
    drawn = census.regularity(view)
    assert drawn["near_axis"] == 0
    assert drawn["axis"] == 2
    measured = slack.measure(2, tilted(), view, [2])
    assert measured["identity"]["unnamed_turns"] == []


def test_nothing_is_straightened_past_the_threshold() -> None:
    view, report = slack.regularize(tilted(), slack.Settings(near_axis_degrees=0.1))
    assert view is not None
    assert report["straightened"] == []
    assert view["squares"][1]["basis"] != ["1", "0"]


def test_a_run_directory_in_the_record_is_refused() -> None:
    with pytest.raises(slack.GridSlackError):
        slack.run_one(1, slack.ROOT / "witnesses" / "scratch", slack.Settings())
    assert not (slack.ROOT / "witnesses" / "scratch").exists()


def test_a_run_writes_its_view_report_and_drawing(tmp_path: Path) -> None:
    report = slack.run_one(1, tmp_path, slack.Settings())
    directory = tmp_path / "n-001"
    assert (directory / "report.json").is_file()
    assert report["n"] == 1
    assert "measured" in report
    assert (directory / "view.yaml.gz").is_file()
    assert (directory / "drawing.svg").read_text(encoding="utf-8").startswith("<?xml")


def test_a_report_names_the_witness_it_read_and_the_view_it_wrote(tmp_path: Path) -> None:
    """Review B of #530, B3: the source witness by digest and exact side, and the view's
    bytes by their Git blob id. The digest and the blob id are provenance only, checked
    here for being the right values and compared by nothing (OR-18). The admitting layer
    (#548) decides instead, holding `s_W_exact` to today's witness and measuring identity
    again."""
    import hashlib  # noqa: PLC0415

    from devtools.retained_data import git_blob  # noqa: PLC0415

    report = slack.run_one(1, tmp_path, slack.Settings())
    path = slack.KNOWN_BEST / "n-001.yaml"
    source = report["source"]
    assert source["path"] == "packing/witnesses/known-best/n-001.yaml"
    assert source["witness_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert source["id"] == slack.load_source(1)["id"]
    assert Fraction(source["s_W_exact"]) == 1
    view = tmp_path / "n-001" / report["view"]["path"]
    assert report["view"]["git_blob"] == git_blob(view.read_bytes())


def test_a_rerun_without_a_view_leaves_no_earlier_view_or_drawing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review B of #530, B4: a re-run that finds no view removes the run before's view,
    drawing and report before it writes its own."""
    slack.run_one(1, tmp_path, slack.Settings())
    directory = tmp_path / "n-001"
    assert (directory / "view.yaml.gz").is_file()

    def no_view(*_arguments: object) -> tuple[None, dict[str, Any]]:
        return None, {"attempts": [], "refusal": "no view this time", "seconds": 0}

    monkeypatch.setattr(slack, "regularize", no_view)
    report = slack.run_one(1, tmp_path, slack.Settings())
    assert "measured" not in report
    assert "view" not in report
    assert not (directory / "view.yaml.gz").exists()
    assert not (directory / "drawing.svg").exists()


def _row(coefficients: dict[int, int], rhs: Fraction, priority: tuple[int, ...]) -> Any:
    return slack.same.Row(
        "pair" if len(coefficients) > 1 else "wall",
        {column: Fraction(value) for column, value in coefficients.items()},
        rhs,
        1,
        {},
        priority,
    )


def test_only_the_witness_contacts_of_unchanged_squares_are_closed() -> None:
    frame = slack.same.exact_frame(scattered())
    # Squares 1 and 2 (columns 0 and 2) are 0.05 apart along x in the witness: a near
    # contact, not a contact. Square 2 sits on the floor (column 3): a contact.
    apart = _row({0: -1, 2: 1}, Fraction(1), (0, 0, 1))
    floor = _row({3: 1}, HALF, (1, 1, 1))
    kept, left = slack.closable([apart, floor], frame, changed=set())
    assert kept == [floor]
    assert left == [apart]
    kept, left = slack.closable([apart, floor], frame, changed={1})
    assert left == []


def test_a_left_open_row_the_solve_penetrates_is_closed_after_all() -> None:
    # x0 = 1/2 on the wall, x1 = x0 + 1 closed, x2 left open at 2.4 although x2 >= x1 + 1.
    wall = _row({0: 1}, HALF, (1, 0, 0))
    pair = _row({0: -1, 2: 1}, Fraction(1), (0, 0, 1))
    later = _row({2: -1, 4: 1}, Fraction(1), (0, 1, 2))
    generator = [(HALF, HALF), (Fraction(3, 2), HALF), (Fraction(12, 5), HALF)]
    solution, _promoted, _rounds, reopened = slack.settle_reopening(
        [pair, wall], [later], generator
    )
    assert reopened == 1
    assert solution.values[4] == Fraction(5, 2)


def test_a_witness_above_the_bound_is_solved_at_the_bound_first(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Owner, 13 October 2026: a valid view has "equal or smaller side". The fixture's
    four squares sit in a box of 11/5, above n = 4's verified upper bound 2, so the box
    of side 2 is tried first and closes them into the 2 x 2 block, at the bound."""
    monkeypatch.setattr(slack, "rational_bound", REAL_RATIONAL_BOUND)
    assert slack.rational_bound(4) == 2
    assert slack.attempts_for(scattered()) == slack.BOUND_FIRST
    frame = slack.frame_for(scattered(), "bound")
    assert frame is not None
    assert frame.side == 2
    same_frame = slack.frame_for(scattered(), "same")
    assert same_frame is not None
    assert same_frame.side == Fraction(11, 5)
    view, report = slack.regularize(scattered(), slack.Settings())
    assert view is not None
    assert report["relation"] == "bound"
    assert Fraction(view["side"]) == 2
    assert sorted(_centres(view)) == [
        (HALF, HALF),
        (HALF, Fraction(3, 2)),
        (Fraction(3, 2), HALF),
        (Fraction(3, 2), Fraction(3, 2)),
    ]


def test_a_bound_above_the_witness_is_tried_after_its_own_side(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Where `U` is above `s_W` (n = 171 and 198 in the record), a view at the witness's
    own side is already at most `U`, so the same side is tried first and the bound only
    after no view there could be found (#580 review A6)."""
    for n in (171, 198):
        witness = slack.load_source(n)
        upper = REAL_RATIONAL_BOUND(n)
        assert upper is not None
        assert upper > slack.same.exact_frame(witness).side
        monkeypatch.setattr(slack, "rational_bound", REAL_RATIONAL_BOUND)
        assert slack.attempts_for(witness) == slack.ATTEMPTS

    above = Fraction(12, 5)
    monkeypatch.setattr(slack, "rational_bound", lambda _n: above)
    assert slack.attempts_for(scattered()) == slack.ATTEMPTS
    real = slack.attempt
    tried: list[tuple[str, bool, Fraction]] = []

    def same_side_refused(
        witness: dict[str, Any],
        frame: Any,
        relation: str,
        settings: slack.Settings,
        *,
        freeze: bool,
    ) -> Any:
        tried.append((relation, freeze, frame.side))
        if relation == "same":
            refused = {"relation": relation, "frozen_tilted": freeze, "refusal": "by the test"}
            return None, refused, []
        return real(witness, frame, relation, settings, freeze=freeze)

    monkeypatch.setattr(slack, "attempt", same_side_refused)
    view, report = slack.regularize(scattered(), slack.Settings())
    assert tried == [
        ("same", False, Fraction(11, 5)),
        ("same", True, Fraction(11, 5)),
        ("bound", False, above),
    ]
    assert view is not None
    assert report["relation"] == "bound"
    assert Fraction(view["side"]) == above


def test_admitted_views_describe_the_generator_by_its_defaults(tmp_path: Path) -> None:
    """A run at 5 degrees keeps its threshold in its own parameters, and the generator
    block the layer's index shares is the defaults, so runs at 0.5, 1 and 5 degrees are
    admitted side by side (owner, 13 October 2026; #580 review A6)."""
    run = tmp_path / "grid-5"
    report = slack.run_one(1, run, slack.Settings(near_axis_degrees=5.0))
    assert report["settings"]["near_axis_degrees"] == 5.0
    views, run_block, generator = slack.admitted_views(run, [])
    assert views == []
    assert run_block["parameters"]["near_axis_degrees"] == 5.0
    assert generator["settings"] == slack.DEFAULT_SETTINGS
    assert generator["settings"]["near_axis_degrees"] == slack.NEAR_AXIS_DEGREES


def test_a_closed_form_bound_is_never_a_frame(monkeypatch: pytest.MonkeyPatch) -> None:
    """n = 5's bound is 2 + (1/2)sqrt(2): its 60-digit value is not the bound."""
    monkeypatch.setattr(slack, "rational_bound", REAL_RATIONAL_BOUND)
    assert slack.rational_bound(5) is None
    assert slack.rational_bound(301) is not None


def test_no_bound_attempt_at_a_closed_form_bound(monkeypatch: pytest.MonkeyPatch) -> None:
    """Review B of #530, B1: n = 5's bound is 2 + (1/2)sqrt(2). Its 60-digit value is
    1.3e-61 above it, and a view solved in a box of that side was exactly verified above
    `U` and labelled `bound`; a closed form is no frame, so n = 5 tries `s_W` alone. The
    case records' bounds are read here, as the generator reads them."""
    monkeypatch.setattr(slack, "rational_bound", REAL_RATIONAL_BOUND)
    witness = slack.load_source(5)
    assert slack.rational_bound(5) is None
    assert slack.frame_for(witness, "bound") is None
    view, report = slack.regularize(witness, slack.Settings())
    assert [row["relation"] for row in report["attempts"]] == ["same", "same"]
    assert view is None
    # A rational `U` above `s_W` is still a frame (n = 171's printed side truncates it).
    upper = slack.rational_bound(171)
    assert upper is not None
    bound = slack.frame_for(slack.load_source(171), "bound")
    assert bound is not None
    assert bound.side == upper


def beside_a_tilted_square() -> dict[str, Any]:
    """Two axis squares on the floor a tenth apart, and a square turned by
    `arctan(3/4)` (about 36.9 degrees) wedged into the opposite corner of a side-3 box:
    the placement slides the second axis square flush and leaves the tilted one alone."""
    one, zero = Fraction(1), Fraction(0)
    return _basis_witness(
        [
            (HALF, HALF, one, zero),
            (Fraction(16, 10), HALF, one, zero),
            (Fraction(23, 10), Fraction(23, 10), Fraction(4, 5), Fraction(3, 5)),
        ],
        side="3",
    )


def test_anchoring_substitutes_held_columns_and_keeps_every_gap() -> None:
    row = _row({0: -1, 2: 1}, Fraction(1), (0, 0, 1))
    values = {0: HALF, 2: Fraction(8, 5)}
    (held,) = slack.anchor([row], {0: HALF})
    assert held.coefficients == {2: Fraction(1)}
    assert held.gap({2: Fraction(8, 5)}) == row.gap(values) == Fraction(1, 10)
    (constant,) = slack.anchor([row], values)
    assert constant.coefficients == {}
    assert constant.gap({}) == Fraction(1, 10)
    generator = [(HALF, HALF), (Fraction(8, 5), HALF)]
    solution, _promoted, _rounds, _reopened = slack.settle_reopening(
        [row], [], generator, {0: HALF, 1: HALF}
    )
    assert solution.values[0] == HALF
    assert solution.values[2] == Fraction(3, 2)
    assert 0 not in solution.free_columns
    assert 1 not in solution.free_columns


def test_an_anchored_way_holds_the_unchanged_tilted_square_exactly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real = slack.settle_variant

    def refusing(rows: str, **kwargs: Any) -> Any:
        settled = real(rows, **kwargs)
        if rows not in slack.ANCHORED:
            settled.refusal = settled.record["refusal"] = "penetrated: forced by the test"
        return settled

    monkeypatch.setattr(slack, "settle_variant", refusing)
    witness = beside_a_tilted_square()
    view, report = slack.regularize(witness, slack.Settings())
    assert view is not None
    settled = report["attempts"][0]["exact"]["settled"]
    assert [variant["rows"] for variant in settled] == [
        "witness-contacts",
        "all-tight",
        "anchored-tilted",
    ]
    assert settled[-1]["anchored"] == 1
    assert view["certificate"]["resolve"]["rows"] == "anchored-tilted"
    assert view["certificate"]["resolve"]["anchored_squares"] == 1
    assert _centres(view) == [
        (HALF, HALF),
        (Fraction(3, 2), HALF),
        (Fraction(23, 10), Fraction(23, 10)),
    ]
    verdicts = report["attempts"][0]["exact"]["verdicts"]
    assert verdicts["exact_verify"]["passed"]
    assert verdicts["independent"]["passed"]


def test_a_literal_past_the_digit_limit_tries_the_next_way(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real = slack.same.same_side_witness
    calls: list[int] = []

    def too_long_once(*args: Any, **kwargs: Any) -> Any:
        calls.append(1)
        if len(calls) == 1:
            raise ValueError("Exceeds the limit (4300 digits) for integer string conversion")
        return real(*args, **kwargs)

    monkeypatch.setattr(slack.same, "same_side_witness", too_long_once)
    view, report = slack.regularize(scattered(), slack.Settings())
    assert view is not None
    settled = report["attempts"][0]["exact"]["settled"]
    assert settled[0]["refusal"].startswith("literal-too-long")
    assert settled[1]["refusal"] is None
    assert view["certificate"]["resolve"]["rows"] == settled[1]["rows"]


def test_the_own_pairing_names_turns_square_for_square() -> None:
    one, zero = Fraction(1), Fraction(0)
    t = Fraction(1, 500)
    c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    source = [(HALF, HALF, one, zero), (Fraction(16, 10), Fraction(6, 10), c, s)]
    view = [(HALF, HALF, one, zero), (Fraction(3, 2), HALF, one, zero)]
    paired = slack.own_pairing(view, source, [1])
    assert paired["turned"] == [1]
    assert paired["unnamed_turns"] == []
    assert float(paired["max_move"]) == pytest.approx(0.1 * 2**0.5, rel=1e-6)
    assert slack.own_pairing(view, source, [])["unnamed_turns"] == [1]
    view, _report = slack.regularize(tilted(), slack.Settings())
    assert view is not None
    measured = slack.measure(2, tilted(), view, [2])
    assert measured["identity"]["own_pairing"]["unnamed_turns"] == []


def test_the_layer_contract_names_this_version() -> None:
    """A view this version makes can enter the layer: the contract's generators, the
    index schema, the method mark the checker looks for and the drawing's sentence all
    name it, beside the version whose views the layer already draws."""
    schema = load_yaml(
        (axis.ATLAS_DIR.parent / "regularized-atlas-index.schema.yaml").read_text()
    )
    named = schema["$defs"]["generator_id"]["enum"]
    assert set(named) == set(axis.GENERATORS)
    assert {slack.GENERATOR, axis.GRID_GENERATOR} <= set(axis.GRID_GENERATORS)
    assert axis.METHOD_MARKS[slack.GENERATOR] in slack.METHOD
    assert slack.GENERATOR in render.MADE_BY
    assert slack.GENERATOR in schema["properties"]["generators"]["properties"]


def test_admission_holds_the_view_to_this_checkouts_witness(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """#548 review B4: admission holds a grid view to the witness this checkout holds, by
    the run's exact side and by measuring the view again against it; the run's witness
    digest and view blob are provenance, compared with nothing (OR-18)."""
    n = 241
    index = json.loads(axis.ATLAS.index.read_text(encoding="utf-8"))
    (entry,) = (record for record in index["entries"] if record["n"] == n)
    assert entry["generator"] in axis.GRID_GENERATORS
    directory = tmp_path / f"n-{n:03d}"
    directory.mkdir()
    stored = (axis.REPO / entry["view"]["path"]).read_bytes()
    (directory / "view.yaml.gz").write_bytes(stored)
    contacts = entry["measured"]["contacts"]
    recorded = {
        "identity": {**entry["regularization"]["identity"], "symmetry": 0},
        "shades": {
            **{rule: dict(contacts[rule]) for rule in ("house", "stage")},
            "regressions": [],
            "against_current": {"regressions": []},
        },
    }
    measured_on: list[str] = []

    def measure(_n: int, witness: Any, _view: Any, _straightened: Any) -> dict[str, Any]:
        measured_on.append(str(witness["id"]))
        return json.loads(json.dumps(recorded))

    admit = Decision(10, "admit", None, None, "every admission condition holds")
    monkeypatch.setattr(slack, "measure", measure)
    monkeypatch.setattr(slack, "decided", lambda _report, _witness, _routes: admit)

    # The view is the drawn one; deciding it on both exact routes takes about 80 s at 241,
    # and is the next test's subject, on a count that decides in well under a second.
    def view_decided(_n: int, _report: Any, path: Path, _witness: Any) -> Any:
        view = load_yaml(gzip.decompress(path.read_bytes()).decode())["witness"]
        return view, dict.fromkeys(VERDICTS, True)

    monkeypatch.setattr(slack, "view_decided", view_decided)
    witness = slack.load_source(n)
    own = slack.same.literal(slack.same.exact_frame(witness).side)
    held = hashlib.sha256((axis.REPO / entry["source"]["witness"]).read_bytes()).hexdigest()

    def admitted(source: Any, **extra: Any) -> Any:
        report = {
            "n": n,
            "generator": slack.GENERATOR,
            "source": source,
            "attempts": [
                {"exact": {"verdicts": {name: {"passed": True} for name in VERDICTS}}}
            ],
            "measured": {"identity": {"one_to_one": True}},
            **extra,
        }
        (directory / "report.json").write_text(json.dumps(report))
        return slack.admitted(directory, "grid-slack-fixture")

    # A report from before the run recorded the witness's side: measured here, and said.
    older = admitted(f"packing/witnesses/known-best/n-{n:03d}.yaml")
    assert measured_on == [witness["id"]]
    assert older.source["sha256"] == held
    assert older.measured["source_note"] == slack.UNRECORDED_SIDE
    # The run's digests are provenance: a different digest or blob decides nothing.
    source = {"witness": "x", "witness_sha256": "0" * 64, "s_W_exact": own}
    later = admitted(source, view={"path": "view.yaml.gz", "git_blob": "0" * 40})
    assert later.source["sha256"] == held
    assert "source_note" not in later.measured
    assert later.regularization["identity"]["moved"] == recorded["identity"]["moved"]
    # A run on a witness at another side is refused, and so is a view that no longer
    # pairs one to one with this checkout's witness.
    with pytest.raises(slack.GridSlackError, match="run the count again on this witness"):
        admitted({**source, "s_W_exact": "1"})
    recorded["identity"]["one_to_one"] = False
    with pytest.raises(slack.GridSlackError, match="does not pair one to one"):
        admitted(source)


VERDICTS = ("exact_verify", "independent")


def test_a_view_is_decided_against_a_closed_form_bound_exactly() -> None:
    """`regularize_evand.upper_bound` gives `U` only where it is rational, so `decided`
    holds the side to the bound the driver holds exactly: below n = 5's closed form
    2 + (1/2)sqrt(2) a view is a register candidate (row 3), above it a dilated side (row
    4), and neither is read as against an unknown `U`."""
    witness = slack.load_source(5)

    def decided(side: str) -> Decision:
        report = {
            "n": 5,
            "attempts": [
                {
                    "exact": {
                        "verdicts": {name: {"passed": True} for name in VERDICTS},
                        "side": side,
                    }
                }
            ],
            "measured": {
                "identity": {"one_to_one": True},
                "shades": {"regressions": [], "against_current": {}},
                "visible_change": True,
                "totals_fall": False,
            },
        }
        return slack.decided(report, witness)

    below, above = decided("2707/1000"), decided("2708/1000")
    assert (below.row, below.decision) == (3, "held")
    assert "below the verified upper bound" in below.reason
    assert (above.row, above.decision) == (4, "held")
    assert "above the verified upper bound" in above.reason


def test_a_grid_run_is_dated_by_its_reports_and_not_by_its_files_time(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """#548 review C, C2: Git keeps no modification times, so a copied or restored grid
    run directory would be dated the day it was copied. The run is dated by the latest
    time its reports record; a run none of whose reports records one is dated by the
    index, as the driver's undated receipts are, and refused where the index has none."""
    run_dir = tmp_path / "all"
    run_id = f"grid-slack-{run_dir.name}"
    admit = Decision(10, "admit", None, None, "every admission condition holds")
    monkeypatch.setattr(slack, "decided", lambda _report, _witness: admit)

    def report(n: int, **extra: Any) -> Path:
        directory = run_dir / f"n-{n:03d}"
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "report.json"
        body = {"n": n, "generator": slack.GENERATOR, "seconds": 1.5, "settings": {}}
        path.write_text(json.dumps({**body, **extra}))
        os.utime(path, (0, 0))
        return path

    report(4)  # from before reports recorded the time: written before the others
    report(5, finished="2026-10-13T01:00:00Z")
    report(6, finished="2026-10-12T05:00:00Z")
    block, _settings = slack.run_block(run_dir, run_id)
    assert (block["finished"], block["counts"]) == ("2026-10-13", 3)

    for n in (5, 6):
        report(n)
    block, _settings = slack.run_block(run_dir, run_id)
    assert block["finished"] is None
    held = [{"id": run_id, "finished": "2026-10-12"}]
    assert driver.dated_runs([block], held)[0]["finished"] == "2026-10-12"
    with pytest.raises(driver.EvandRunError, match="records no finish time"):
        driver.dated_runs([block], [])


def test_admission_decides_the_view_file_it_admits(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """#548 review C, C1: admission decides the view file as it is now, on both exact
    routes, with its exact side and id held to its report's, before anything is measured
    on it; the table decides on those routes and the entry records them, not the report's
    verdicts. A square moved 1e-15 into its neighbour, beside a report whose verdicts say
    both routes passed, is refused, as the reviewer's mutant at 241 is; so are another
    side, another id, routes the run recorded otherwise and a file that does not read."""
    n = 4
    witness = slack.load_source(n)
    directory = tmp_path / f"n-{n:03d}"
    directory.mkdir()
    pristine = {**json.loads(json.dumps(witness)), "id": slack.regularized_id(witness)}
    side = slack.same.literal(slack.same.exact_frame(witness).side)
    shades = {"before": [0] * n, "after": [0] * n}
    measured: list[str] = []
    routed: list[Any] = []

    def measure(_n: int, _witness: Any, view: Any, _straightened: Any) -> dict[str, Any]:
        measured.append(str(view["id"]))
        return {
            "identity": {
                "one_to_one": True,
                "moved": 0,
                "max_move": 0.0,
                "max_turn_deg": 0.0,
                "symmetry": 0,
            },
            "shades": {
                "house": dict(shades),
                "stage": dict(shades),
                "regressions": [],
                "against_current": {"regressions": []},
            },
        }

    def decided(_report: Any, _witness: Any, routes: Any) -> Decision:
        routed.append(routes)
        return Decision(10, "admit", None, None, "every admission condition holds")

    monkeypatch.setattr(slack, "measure", measure)
    monkeypatch.setattr(slack, "decided", decided)

    def admitted(view: dict[str, Any], *, said: str = side, passed: bool = True) -> Any:
        text = slack.witness_document(view)
        (directory / "view.yaml.gz").write_bytes(gzip.compress(text.encode(), mtime=0))
        verdicts = {"exact_verify": {"passed": True}, "independent": {"passed": passed}}
        report = {
            "n": n,
            "generator": slack.GENERATOR,
            "source": {"s_W_exact": side},
            "attempts": [{"exact": {"side": said, "verdicts": verdicts}}],
            "measured": {"identity": {"one_to_one": True}},
        }
        (directory / "report.json").write_text(json.dumps(report))
        return slack.admitted(directory, "grid-slack-fixture")

    entry = admitted(pristine)
    assert routed == [dict.fromkeys(VERDICTS, True)]
    assert entry.routes == {"repository_verifier": True, "independent_checker": True}
    assert measured == [pristine["id"]]
    # Square 2 moved 1e-15 left, into square 1: both routes refuse the file, whatever the
    # report says, and it is refused before anything is measured on it.
    moved = json.loads(json.dumps(pristine))
    moved["squares"][1]["corners"] = [
        [slack.same.literal(Fraction(x) - Fraction(1, 10**15)), y]
        for x, y in moved["squares"][1]["corners"]
    ]
    with pytest.raises(slack.GridSlackError, match="fails exact_verify and independent"):
        admitted(moved)
    assert measured == [pristine["id"]]
    with pytest.raises(slack.GridSlackError, match="side is 2, not the 3 its report"):
        admitted(pristine, said="3")
    edited = {**pristine, "id": "W-known-best-n004-edited"}
    with pytest.raises(slack.GridSlackError, match="id is W-known-best-n004-edited"):
        admitted(edited)
    with pytest.raises(slack.GridSlackError, match="decided otherwise by independent"):
        admitted(pristine, passed=False)
    (directory / "view.yaml.gz").write_bytes(gzip.compress(b"witness: [", mtime=0))
    with pytest.raises(slack.GridSlackError, match="does not read as a rational view"):
        slack.admitted(directory, "grid-slack-fixture")
    (directory / "view.yaml.gz").unlink()
    with pytest.raises(slack.GridSlackError, match=r"no view\.yaml\.gz beside the report"):
        slack.admitted(directory, "grid-slack-fixture")
    assert measured == [pristine["id"]]


def test_feasibility_holds_the_move_bound_and_a_zero_trust_is_refused() -> None:
    """Review B of #530, B5: `feasible` holds the rows `place` holds, the L1 move bound
    among them, so a straightening it accepts can be placed; `--trust 0` would divide the
    tie-break's weight by zero and is refused."""
    one, zero = Fraction(1), Fraction(0)
    witness = _basis_witness([(Fraction(6, 10), Fraction(6, 10), one, zero)])
    frame = slack.frame_for(witness, "same")
    assert frame is not None
    g = slack.geometry(frame, [])

    def pushed(step: float) -> slack.Rows:
        """Rows asking the square to move `step` right and `step` up: within the trust
        region per coordinate, and `2 * step` in L1."""
        rows = slack.Rows()
        rows.add({0: 1.0}, float(g.x0[0]) + step, float("inf"), "test")
        rows.add({1: 1.0}, float(g.y0[0]) + step, float("inf"), "test")
        return rows

    assert slack.feasible(g, pushed(0.2), slack.TRUST)
    assert not slack.feasible(g, pushed(0.3), slack.TRUST)
    with pytest.raises(slack.GridSlackError, match="positive"):
        slack.Settings(trust=0.0)
    with pytest.raises(SystemExit):
        slack.parser().parse_args(["--n", "5", "--run-dir", "scratch", "--trust", "0"])
