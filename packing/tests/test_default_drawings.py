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
import re
import shutil
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


# --------------------------------------------------------------------------------------
# The regularization state (think-gvke): every count says whether its drawing is
# regularized, and the gate fails on a pending count the allowlist does not name.
# --------------------------------------------------------------------------------------


def _record() -> dict:
    return json.loads(defaults.RECORD.read_text(encoding="utf-8"))


def _write(tmp_path: Path, record: dict) -> Path:
    path = tmp_path / "default-drawings.json"
    path.write_text(defaults.text(record), encoding="utf-8")
    return path


def _first_state(record: dict, state: str) -> dict:
    row = next((row for row in record["states"] if row["state"] == state), None)
    if row is None:
        pytest.skip(f"the data holds no {state} count")
    return row


def _measured(record: dict, n: int) -> dict:
    """What `document` measured at `n`: its view's decision, or its house's measures."""
    view = next((row for row in record["entries"] if row["n"] == n), None)
    if view is not None:
        return view
    row = next(row for row in record["states"] if row["n"] == n)
    return {"n": n, "measures": row["measures"]}


def test_every_count_has_one_state_and_says_what_is_drawn() -> None:
    record = _record()
    rows = record["states"]
    assert [row["n"] for row in rows] == sorted(defaults.index_entries())
    totals = record["totals"]["states"]
    assert sum(totals.values()) == len(rows)
    assert set(totals) == set(defaults.STATES)
    views = {row["n"]: row for row in record["entries"]}
    for row in rows:
        n = row["n"]
        viewed = n in views and views[n]["default"] == defaults.REGULARIZED
        assert row["drawn"] == (defaults.VIEW if viewed else defaults.HOUSE), n
        if row["state"] == defaults.REGULARIZED_STATE:
            # Only a strong generator's drawn view makes a count regularized: at n = 176
            # the axis tool's view was held, the raw house drawn, and the index said
            # `regularized`.
            assert row["generator"] in defaults.STRONG_GENERATORS, n
        if row["state"] == defaults.PENDING:
            assert n in defaults.PENDING_ALLOWED, n
        if viewed:
            assert row["measures"] == {
                key: value[defaults.VIEW] for key, value in views[n]["measures"].items()
            }, n


def test_the_committed_record_passes_the_gate_with_its_allowlist() -> None:
    found, listed = defaults.state_problems()
    assert found == []
    pending = [row["n"] for row in _record()["states"] if row["state"] == defaults.PENDING]
    assert pending == sorted(defaults.PENDING_ALLOWED)
    # The list's size is printed, so that a change growing it shows in the log (A2).
    assert listed[-2] == f"PENDING_ALLOWED: {len(defaults.PENDING_ALLOWED)} counts"
    assert listed[-1].startswith("regularization states: 324 counts")


def test_the_gate_fails_on_a_new_pending_count(tmp_path: Path) -> None:
    record = _record()
    row = _first_state(record, defaults.REGULAR_AS_PUBLISHED)
    row["state"] = defaults.PENDING
    found, _listed = defaults.state_problems(_write(tmp_path, record))
    assert any(line.startswith(f"n={row['n']} is pending:") for line in found)
    assert any("PENDING_ALLOWED with the bead" in line for line in found)


def test_the_allowlist_equals_the_pending_set_and_each_entry_names_a_bead(
    tmp_path: Path,
) -> None:
    # Not shrink-only: a reviewed change may add a count with its bead (review A2 of
    # #636). The gate holds the list to the pending set, and `check_bead_tree` holds
    # each bead open (`test_the_record_defers_each_count_to_the_bead_that_owns_it`).
    record = _record()
    regular = [row for row in record["states"] if row["state"] == defaults.REGULAR_AS_PUBLISHED]
    if len(regular) < 2:
        pytest.skip("the data holds fewer than two counts regular as published")
    pending, joining = regular[0], regular[1]
    # The data's own list is empty since 16 October 2026 (think-3zi3), so a count is
    # allowed pending here as a deferral would allow it, with its bead. Only a corrected
    # witness's runs may wait since the house rule (`CORRECTED`, reviews A5 and B2 of
    # #660), so each count here is one, at its house's own source and side.
    corrected = {pending["n"]: _correction(pending)}
    pending["state"] = defaults.PENDING
    allowed = {**defaults.PENDING_ALLOWED, pending["n"]: "think-0000: a deferral"}
    found, _listed = defaults.state_problems(
        _write(tmp_path, record), allowed=allowed, corrected=corrected
    )
    assert found == []
    # A count allowed pending that is no longer pending fails until it comes off the list.
    pending["state"] = defaults.REGULARIZED_STATE
    found, _listed = defaults.state_problems(
        _write(tmp_path, record), allowed=allowed, corrected=corrected
    )
    assert found == [
        (
            f"n={pending['n']}: PENDING_ALLOWED names it, but it is regularized; take it "
            "off the list"
        )
    ]
    # And a count that joins it names its bead.
    pending["state"] = defaults.PENDING
    joining["state"] = defaults.PENDING
    allowed = {**allowed, joining["n"]: "later"}
    corrected = {**corrected, joining["n"]: _correction(joining)}
    found, _listed = defaults.state_problems(
        _write(tmp_path, record), allowed=allowed, corrected=corrected
    )
    assert found == [f"n={joining['n']}: PENDING_ALLOWED names no bead: 'later'"]


def _correction(row: dict) -> defaults.Correction:
    """A correction of the row's witness: the one it replaced had the row's source, path and
    exact side at an earlier revision. Checked as declared, with no base record."""
    witness = row["witness"]
    return defaults.Correction(
        witness["source"], witness.get("path"), "an-earlier-revision", witness["side"]
    )


def _replaced(witness: dict) -> defaults.Correction:
    """The correction that names `witness` as the one it replaced."""
    return defaults.Correction(
        witness["source"], witness.get("path"), witness.get("revision"), witness["side"]
    )


def _base(rows: dict, changed: frozenset[int] = frozenset()) -> defaults.Base:
    """A base record of these rows, as `base_record` reads one from a commit, with the
    counts whose witness file the change alters."""
    return defaults.Base("origin/main", rows, changed)


def test_a_row_out_of_place_fails_the_gate(tmp_path: Path) -> None:
    # The id is the count's, the same for every house (`W-known-best-nNNN`), so this holds
    # a row to its count, and no more (review A4 of #636).
    record = _record()
    row = record["states"][0]
    held = row["witness"]["id"]
    for state in record["states"]:
        assert state["witness"]["id"] == f"W-known-best-n{state['n']:03d}"
    row["witness"]["id"] = "W-elsewhere"
    found, _listed = defaults.state_problems(_write(tmp_path, record))
    stale = f"run `{defaults.GENERATOR} --update`"
    assert found == [
        (
            f"n={row['n']}: the record's row names witness 'W-elsewhere', and the index's "
            f"count names {held!r}; {stale}"
        )
    ]


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("side", "1/1"),
        ("source", "[another source]"),
        # A replacement certificate from the same source at the same side (review A4).
        ("path", "resources/web/elsewhere/n-102.cert.gz"),
        ("revision", "0" * 40),
    ],
)
def test_the_state_follows_the_witness_as_it_identifies_itself(key: str, value: str) -> None:
    # A new house, a new certificate file or an upstream fix changes what the witness
    # says of itself -- its source's key, path or revision, or its side -- and a decision
    # made on the old one no longer applies: the count reads pending again (OR-16:
    # identified by what the witness says, never by a digest of its bytes).
    n = min(n for n, held in defaults.SETTLED.items() if held.state == defaults.DECIDED)
    record = _record()
    row = next(row for row in record["states"] if row["n"] == n)
    assert row["state"] == defaults.DECIDED
    assert {key: row["witness"][key] for key in defaults.IDENTITY} == {
        key: getattr(defaults.SETTLED[n], key) for key in defaults.IDENTITY
    }
    moved = {**defaults.SETTLED, n: defaults.SETTLED[n]._replace(**{key: value})}
    found, _listed = defaults.state_problems(settled=moved)
    assert [line for line in found if line.startswith(f"n={n}: ")] == [
        (
            f"n={n}: SETTLED was decided on another witness ({key} "
            f"{value[:24]!r} to {str(row['witness'][key])[:24]!r}); run the generators on "
            'it (regularization-process.md, "When a Witness Changes"), then settle it again '
            "or take it off SETTLED"
        )
    ]

    entry = defaults.index_entries()[n]
    state = defaults.count_state(n, entry, _measured(record, n), row["witness"], settled=moved)
    assert state["state"] == defaults.PENDING
    assert state["why"].startswith("no strong generator has decided this witness")
    assert [found["run"] for found in state["decisions"]] == [None]
    # The witness the record names is the one the index holds, as it identifies itself.
    assert row["witness"] == defaults.witness_identity(defaults.REPO, entry)


def test_a_decision_names_what_it_still_owes_and_the_bead_that_owns_it() -> None:
    # A decision that still owes runs or a recorded outcome says so, naming the open bead
    # that owns them, so the record shows it (review A6 of #636); one whose runs and
    # per-count outcome are recorded owes nothing (`owed` is None, as the contract allows)
    # and its state says nothing is owed rather than inventing a debt. The ten counts
    # decided on 15 October 2026 owed think-0ut1 until its runs of 16 October 2026
    # recorded each count's outcome; the three think-la7h settled that day owed nothing.
    # No committed decision owes anything now, so one that owes is made here.
    record = _record()
    rows = {row["n"]: row for row in record["states"]}
    decided = [n for n, held in defaults.SETTLED.items() if held.state == defaults.DECIDED]
    for n in decided:
        held = defaults.SETTLED[n]
        if held.owed is None:
            assert "still owed" not in rows[n]["why"], n
        else:
            assert defaults.BEAD.match(held.owed), n
            assert rows[n]["why"].endswith(f"; still owed: {held.owed}"), n
    n = min(decided)
    owing = {**defaults.SETTLED, n: defaults.SETTLED[n]._replace(owed="think-aaaa: a run")}
    entry = defaults.index_entries()[n]
    state = defaults.count_state(
        n, entry, _measured(record, n), rows[n]["witness"], settled=owing
    )
    assert state["state"] == defaults.DECIDED
    assert state["why"].endswith("; still owed: think-aaaa: a run")
    n = min(defaults.SETTLED)
    unowned = {**defaults.SETTLED, n: defaults.SETTLED[n]._replace(owed="later")}
    found, _listed = defaults.state_problems(settled=unowned)
    assert found == [f"n={n}: SETTLED's owed names no bead first: 'later'"]


#: The exact algebraic houses adopted on 23 October 2026 (think-ot5c), each drawn
#: unregularized while its regularization was owed to think-mbdw (review A4 of #756), and
#: drawn by grid-slack's version 2 in its own number field since 26 October 2026.
EXACT_HOUSES = (102, 123, 153, 207, 258, 259, 302)


def test_the_exact_algebraic_houses_are_regularized_and_nothing_is_owed() -> None:
    # In the owner's words of 23 October 2026, a drawing is regularized or it is not. The
    # seven exact houses were `regularization-owed` until grid-slack's version 2 drew each
    # in its own number field (think-mbdw): now each is regularized, drawn from that view,
    # with no `SETTLED` entry, and no count owes a regularization.
    record = _record()
    rows = {row["n"]: row for row in record["states"]}
    assert [n for n, row in rows.items() if row["state"] == defaults.OWED] == []
    for n in EXACT_HOUSES:
        assert rows[n]["state"] == defaults.REGULARIZED_STATE, n
        assert rows[n]["drawn"] == defaults.VIEW, n
        assert rows[n]["generator"] == "regularize_grid_slack/2", n
        assert n not in defaults.SETTLED, n
    totals = record["totals"]["states"]
    assert totals[defaults.OWED] == 0
    _found, listed = defaults.state_problems()
    assert "0 regularization owed" in listed[-1]
    assert "think-mbdw" not in dict(defaults.deferrals()).values()


def test_a_regularization_owed_is_its_own_state_and_names_its_bead() -> None:
    # The state stays for a capability a later count may want: an entry `OWED` must name
    # the bead that owes it, and one that names none, or a state the gate does not know,
    # fails the gate.
    n = min(n for n, held in defaults.SETTLED.items() if held.state == defaults.DECIDED)
    unowned = {**defaults.SETTLED, n: defaults.SETTLED[n]._replace(state=defaults.OWED)}
    found, _listed = defaults.state_problems(settled=unowned)
    assert f"n={n}: a regularization owed names the bead that owes it in `owed`" in found
    unknown = {**defaults.SETTLED, n: defaults.SETTLED[n]._replace(state="owed")}
    found, _listed = defaults.state_problems(settled=unknown)
    assert f"n={n}: SETTLED gives state 'owed'" in found


def test_a_settled_entry_the_layer_decides_unaided_fails_the_gate(tmp_path: Path) -> None:
    # Where the layer holds a strong generator's view of this witness and does not draw
    # it, the count is decided without SETTLED, so an entry there is redundant (review A10
    # of #636). No committed count is in that case today, so a regularized count's row is
    # read as if its strong view were held and not drawn.
    record = _record()
    every = defaults.index_entries()
    row = next(
        row
        for row in record["states"]
        if row["state"] == defaults.REGULARIZED_STATE
        and every[row["n"]].get("generator") in defaults.STRONG_GENERATORS
    )
    n = row["n"]
    row.update(state=defaults.DECIDED, drawn=defaults.HOUSE, generator=None)
    witness = row["witness"]
    redundant = {
        **defaults.SETTLED,
        n: defaults.Settled(
            defaults.DECIDED,
            str(witness["source"]),
            str(witness["path"]),
            witness["revision"],
            str(witness["side"]),
            (),
            "drew no better",
            "a test",
        ),
    }
    found, _listed = defaults.state_problems(_write(tmp_path, record), settled=redundant)
    assert found == [
        (
            f"n={n}: SETTLED names it, but the layer holds the {every[n]['generator']} view "
            "of this witness, which decides it unaided; take it off"
        )
    ]
    # Read as it stands, regularized, the entry fails as before.
    found, _listed = defaults.state_problems(settled=redundant)
    assert found == [f"n={n}: SETTLED names it, but it is regularized; take it off"]


def test_every_run_a_settlement_names_is_one_a_record_holds(tmp_path: Path) -> None:
    # A settlement rests on its runs, so each must be held by a record: a block in the
    # layer's index, or a run block or receipt in the retained evidence. Nothing held the
    # three of 16 October 2026 to one, and two of the runs they named had none (review E1
    # of #644).
    recorded = defaults.recorded_runs()
    for held in defaults.SETTLED.values():
        for generator, run in held.runs:
            assert recorded.get(run) == generator, run
    # The evidence directory's grid-slack blocks and driver receipts are read, the
    # receipts under the driver's own name for a run (`evand-regularize-<directory>`).
    assert recorded["grid-slack-3a-rerun-deg1-1016"] == "regularize_grid_slack/1"
    assert recorded["evand-regularize-3a-rerun-303-1016"] == "evand-regularize"
    assert "grid-slack-3a-deg1-1016" not in recorded
    # 272 rests on the adoption's runs of 17 October 2026 (think-3mry).
    n = 272
    held = defaults.SETTLED[n]
    named = (
        *held.runs,
        ("evand-regularize", "evand-regularize-no-such-run"),
        ("evand-regularize", "grid-slack-3a-rerun-deg05-1016"),
    )
    found, _listed = defaults.state_problems(
        settled={**defaults.SETTLED, n: held._replace(runs=named)}
    )
    assert found == [
        (
            f"n={n}: SETTLED names run evand-regularize-no-such-run, which no record holds: "
            "neither the layer's index nor a run block or receipt under "
            "packing/cases/regularized_drawings/; retain its evidence or take it off"
        ),
        (
            f"n={n}: SETTLED names run grid-slack-3a-rerun-deg05-1016 as evand-regularize's, "
            "and its record as regularize_grid_slack/1's"
        ),
    ]
    # Without the retained evidence, only the index's blocks hold a run, and that is not
    # enough (below).
    found, _listed = defaults.state_problems(evidence=tmp_path)
    # No view was drawn from the run at 1 degree, so the index keeps no block of it.
    assert (
        f"n={n}: SETTLED names run grid-slack-adopt174-deg1-1017, which no record holds"
    ) in "\n".join(found)
    # Views were drawn from the driver run (172) and the 0.5-degree run, so the index holds
    # their blocks, and that is all that holds them here.
    assert (
        f"n={n}: SETTLED names run evand-regularize-adopt174-1017, which only the layer's "
        "index holds"
    ) in "\n".join(found)
    assert (
        f"n={n}: SETTLED names run grid-slack-adopt174-deg05-1017, which only the layer's "
        "index holds"
    ) in "\n".join(found)


def test_a_settlement_keeps_its_record_when_the_index_drops_a_run(tmp_path: Path) -> None:
    # The index keeps a run's block only while an entry draws from it, so a settlement
    # resting on an index block failed as soon as later work redrew that run's views:
    # #657 redrew all five views of evand-regularize-3a-1016, and 272's settlement then
    # named a run no record held (review F1 of #644). Every run a settlement names is held
    # by the retained evidence instead, and the index's block of one that had no other is
    # copied there (`--retain-runs`). The settlements of 17 October 2026 rest on runs whose
    # receipts and blocks are retained beside their reports, so no copy is committed; the
    # copy is made here from evidence without the driver run's receipt.
    records = defaults.run_records()
    for n, held in defaults.SETTLED.items():
        for generator, run in held.runs:
            assert records[run].generator == generator, (n, run)
            assert records[run].retained, (n, run)
    assert not (defaults.EVIDENCE / defaults.SETTLED_RUNS).exists()
    run = "evand-regularize-adopt174-1017"
    evidence = tmp_path / "evidence"
    shutil.copytree(
        defaults.EVIDENCE,
        evidence,
        ignore=lambda directory, _names: (
            ["receipt.json"] if Path(directory).name == "adopt174-1017" else []
        ),
    )
    found, _listed = defaults.state_problems(evidence=evidence)
    assert found
    assert all(f"names run {run}, which only the layer's index holds" in p for p in found)
    # `retain_runs` copies the block the index still holds, and a second pass writes nothing.
    assert defaults.retain_runs(evidence=evidence) == ([run], [])
    copied = evidence / defaults.SETTLED_RUNS / run / "run.json"
    index = json.loads(defaults.INDEX.read_text(encoding="utf-8"))
    (block,) = [block for block in index["runs"] if block["id"] == run]
    assert json.loads(copied.read_text(encoding="utf-8")) == block
    assert defaults.retain_runs(evidence=evidence) == ([], [])
    assert defaults.state_problems(evidence=evidence)[0] == []
    # Once the index drops the block, the copy is the run's only record and holds it.
    index["runs"] = [block for block in index["runs"] if block["id"] != run]
    without = tmp_path / "index.json"
    without.write_text(json.dumps(index), encoding="utf-8")
    assert defaults.state_problems(index=without, evidence=evidence)[0] == []
    # Without the copy, nothing holds it, and `retain_runs` cannot restore it.
    shutil.rmtree(evidence / defaults.SETTLED_RUNS)
    assert defaults.retain_runs(index=without, evidence=evidence) == ([], [run])
    found, _listed = defaults.state_problems(index=without, evidence=evidence)
    assert found
    assert all(f"names run {run}, which no record holds" in p for p in found)


def test_a_copy_no_settlement_names_fails_the_gate(tmp_path: Path) -> None:
    # `SETTLED_RUNS` holds the blocks the settlements rest on, so a copy outlives the
    # last settlement that names its run only by mistake: once this layer re-recorded
    # the 15 October settlements, five of the seven copies were named by none (review G2
    # of #644). The gate names each such copy, and one whose id is not its directory's.
    assert defaults.orphaned_copies() == []
    run = "grid-slack-adopt174-deg05-1017"
    evidence = tmp_path / "evidence"
    shutil.copytree(
        defaults.EVIDENCE,
        evidence,
        ignore=lambda directory, _names: (
            ["run.json"] if Path(directory).name == "adopt174-deg05-1017" else []
        ),
    )
    assert defaults.retain_runs(evidence=evidence) == ([run], [])
    assert defaults.orphaned_copies(evidence) == []
    copies = evidence / defaults.SETTLED_RUNS
    (copies / "grid-slack-orphan").mkdir()
    (copies / "grid-slack-orphan" / "run.json").write_text(
        json.dumps({"id": "grid-slack-orphan", "generator": "regularize_grid_slack/1"}),
        encoding="utf-8",
    )
    misnamed = copies / run / "run.json"
    block = json.loads(misnamed.read_text(encoding="utf-8"))
    misnamed.write_text(json.dumps({**block, "id": "grid-slack-elsewhere"}), encoding="utf-8")
    assert defaults.orphaned_copies(evidence) == [run, "grid-slack-orphan"]
    found, _listed = defaults.state_problems(evidence=evidence)
    orphans = [problem for problem in found if "is not the copy of a run" in problem]
    assert len(orphans) == 2
    assert any("settled-runs/grid-slack-orphan/run.json" in problem for problem in orphans)


def test_a_settled_run_covered_the_count_where_its_record_says_which() -> None:
    # A receipt lists the counts its run covered, and a grid-slack block's retained
    # reports are the counts it covered; the settled count must be one of them. An index
    # block, or a copy of one, keeps only how many counts it ran (review F5 of #644).
    records = defaults.run_records()
    assert records["evand-regularize-3a-rerun-303-1016"].counts == frozenset({303})
    assert records["evand-regularize-3a-rerun-s-1016"].counts == frozenset({204, 272})
    assert records["grid-slack-3a-rerun-deg5-1016"].counts == frozenset(
        {129, 146, 156, 204, 271, 272, 303}
    )
    assert records["evand-regularize-adopt174-c-1017"].counts == frozenset({103, 261})
    assert len(records["grid-slack-adopt174-deg5-1017"].counts or ()) == 35
    n = 272
    held = defaults.SETTLED[n]
    named = (*held.runs, ("evand-regularize", "evand-regularize-adopt174-c-1017"))
    found, _listed = defaults.state_problems(
        settled={**defaults.SETTLED, n: held._replace(runs=named)}
    )
    assert found == [
        (
            f"n={n}: SETTLED names run evand-regularize-adopt174-c-1017, whose record "
            f"shows it ran 103, 261, not {n}"
        )
    ]


def test_the_record_defers_each_count_to_the_bead_that_owns_it() -> None:
    # Each bead the allowlist, an exemption or an owed decision names is a deferral
    # `check_bead_tree` holds open, as the intake records' are (review A2 of #636).
    from devtools import check_bead_tree  # noqa: PLC0415

    named = defaults.deferrals()
    assert named == check_bead_tree.regularization_deferrals()
    by_where = dict(named)
    for n, why in defaults.PENDING_ALLOWED.items():
        assert why.startswith(by_where[f"default_drawings.py PENDING_ALLOWED n={n}"]), n
    for n, held in defaults.SETTLED.items():
        if held.state == defaults.EXEMPT:
            assert by_where[f"default_drawings.py SETTLED n={n} exempt"] in held.evidence, n
        if held.owed is not None:
            assert held.owed.startswith(by_where[f"default_drawings.py SETTLED n={n} owed"]), n
    assert len(named) == len(by_where)
    assert all(alias.startswith("think-") and len(alias) == 10 for _where, alias in named)
    # The live list is empty since 16 October 2026, so one count is allowed here, as an
    # adoption's deferral would allow it, and its location is the one the gate reports
    # (review A2 of #654).
    found = defaults.deferrals(allowed={7: "think-0000: re-housed by an adoption"})
    assert ("default_drawings.py PENDING_ALLOWED n=7", "think-0000") in found
    # A bead an entry names elsewhere in its text is not the one that owns it.
    assert defaults.deferrals(settled={}, allowed={1: "later, maybe think-aaaa"}) == []


def test_a_lapsed_view_reads_pending_and_names_what_lapsed() -> None:
    record = _record()
    # No count is pending since 16 October 2026 (think-3zi3), so the lapse is laid on a
    # count the axis tool's record draws, regular as published and settled by nothing.
    entries = defaults.index_entries()
    row = next(
        (
            found
            for found in record["states"]
            if found["state"] == defaults.REGULAR_AS_PUBLISHED
            and entries[found["n"]]["generator"] == defaults.ALGORITHM
            and found["n"] not in defaults.SETTLED
        ),
        None,
    ) or _first_state(record, defaults.PENDING)
    n = row["n"]
    entry = dict(entries[n])
    lapse = {"generator": "evand-regularize", "run": "a-run", "witness_sha256": "2" * 64}
    entry[defaults.LAPSED] = lapse
    state = defaults.count_state(n, entry, _measured(record, n), row["witness"], allowed={})
    assert state["state"] == defaults.PENDING
    assert state["lapsed"] == lapse
    why = str(state["why"])
    # "An earlier witness": the lapse is the last strong view that lapsed, carried through
    # later houses, so it may be more than one back (review A8 of #636).
    assert "the evand-regularize view of an earlier witness lapsed (run a-run)" in why
    assert "allowed pending" not in why


def test_an_adoption_that_rebuilds_only_the_axis_view_reads_pending(tmp_path: Path) -> None:
    """The n = 176 failure replayed through the real derivation (review A3 of #636): an
    adoption rebuilds only the axis tool's record of a count a strong view regularizes,
    which `--update-atlas` writes as its `reference` with the lapse of the strong view."""
    from devtools.regularize_axis_components import lapse_of  # noqa: PLC0415

    record = _record()
    document = json.loads(defaults.INDEX.read_text(encoding="utf-8"))
    every = {int(entry["n"]): entry for entry in document["entries"]}
    views = {row["n"]: row for row in record["entries"]}
    row = next(
        (
            row
            for row in record["states"]
            if row["state"] == defaults.REGULARIZED_STATE
            and every[row["n"]].get("reference")
            and (
                views[row["n"]]["measures"]["uneven_axis"][defaults.HOUSE]
                or views[row["n"]]["measures"]["near_axis"][defaults.HOUSE]
            )
        ),
        None,
    )
    if row is None:
        pytest.skip("the data holds no strong view of an irregular house")
    n = row["n"]
    entry = every[n]
    axis_entry = {**entry["reference"], defaults.LAPSED: lapse_of(entry)}
    document["entries"] = [
        axis_entry if int(found["n"]) == n else found for found in document["entries"]
    ]
    adopted = tmp_path / "index.json"
    adopted.write_text(json.dumps(document), encoding="utf-8")

    # The committed record, now stale, draws a view the index no longer holds.
    found, _listed = defaults.state_problems(index=adopted)
    stale = f"run `{defaults.GENERATOR} --update`"
    assert f"n={n}: the record draws another view than the index holds; {stale}" in found

    # Regenerated, the count reads pending whether the axis tool's view is drawn or held,
    # and names the strong view that lapsed: the state comes from the generators, not
    # from the `lapsed` block, which only explains it.
    for default in (defaults.HOUSE, defaults.REGULARIZED):
        state = defaults.count_state(
            n, axis_entry, {**views[n], "default": default}, row["witness"], allowed={}
        )
        assert state["state"] == defaults.PENDING, default
        assert state["lapsed"] == lapse_of(entry)
        lapsed = f"the {entry['generator']} view of an earlier witness lapsed"
        assert lapsed in state["why"]
        without = {key: value for key, value in axis_entry.items() if key != defaults.LAPSED}
        bare = defaults.count_state(
            n, without, {**views[n], "default": default}, row["witness"], allowed={}
        )
        assert bare["state"] == defaults.PENDING, default

    # The adoption's printout names the count among those certain to be pending, read from
    # the index before the refresh (review A11 of #641).
    from devtools import adopt_houses as adopt  # noqa: PLC0415

    owed = adopt.regularization_owed([n], day="2026-10-16")
    assert owed[1:3] == [
        "  pending until the strong generators decide the new witness:",
        f"    {n}: its {entry['generator']} view lapses",
    ]

    # And the gate fails on the regenerated record until the generators decide it.
    record["states"] = [state if found["n"] == n else found for found in record["states"]]
    regenerated = _write(tmp_path, record)
    found, _listed = defaults.state_problems(regenerated, adopted)
    assert [line for line in found if line.startswith(f"n={n}")] == [
        (
            f"n={n} is pending: {state['why']}. Run the strong generators on its witness "
            '(regularization-process.md, "When a Witness Changes"), or allow it in '
            "PENDING_ALLOWED with the bead that owns the run"
        )
    ]

    # The adoption's pull request may not defer it: its runs are owed there, whatever
    # the cap (result-import.md, "The House Rule"; reviews A5 and B1 of #660). Only a
    # witness corrected at its house's own source and side may wait, with its bead, and
    # an entry naming no bead fails it again.
    def about(lines: list[str]) -> list[str]:
        return [line for line in lines if re.match(rf"n={n}\b", line)]

    deferred = {**defaults.PENDING_ALLOWED, n: "think-g3q7: re-housed by an adoption"}
    found, listed = defaults.state_problems(regenerated, adopted, allowed=deferred)
    (refused,) = about(found)
    assert refused.startswith(
        f"n={n}: PENDING_ALLOWED defers its runs, but CORRECTED names no corrected witness"
    )
    corrected = {n: _correction(state)}
    found, listed = defaults.state_problems(
        regenerated, adopted, allowed=deferred, corrected=corrected
    )
    assert about(found) == []
    assert about(listed) == [f"n={n} is pending, allowed: {deferred[n]}"]
    unowned = {**defaults.PENDING_ALLOWED, n: "until the runs fit the cap"}
    found, _listed = defaults.state_problems(
        regenerated, adopted, allowed=unowned, corrected=corrected
    )
    assert about(found) == [f"n={n}: PENDING_ALLOWED names no bead: {unowned[n]!r}"]


def test_a_lapse_where_the_house_reads_regular_reads_pending(tmp_path: Path) -> None:
    """Review B2 of #636: where a strong view regularizes a count whose house already has
    no uneven and no near-axis square, a re-housing that lapsed the view read `regular-as-
    published`, and the drawing fell from the view's full shared sides to the house's with
    every gate green (at n = 230, from 626 to 562). Replayed through the real `document`,
    on the index `--update-atlas` writes, at the first such count whose view also gains
    shared sides (83 today): the lapse makes the count pending until the generators decide
    the new witness or `SETTLED` names it."""
    from devtools.regularize_axis_components import lapse_of  # noqa: PLC0415

    record = _record()
    document = json.loads(defaults.INDEX.read_text(encoding="utf-8"))
    every = {int(entry["n"]): entry for entry in document["entries"]}
    views = {row["n"]: row for row in record["entries"]}

    def regular_house(n: int) -> bool:
        measures = views[n]["measures"]
        return (
            not measures["uneven_axis"][defaults.HOUSE]
            and not measures["near_axis"][defaults.HOUSE]
        )

    row = next(
        (
            row
            for row in record["states"]
            if row["state"] == defaults.REGULARIZED_STATE
            and every[row["n"]].get("reference")
            and regular_house(row["n"])
            and "house_total" in views[row["n"]]["better"]
        ),
        None,
    )
    if row is None:
        pytest.skip("the data holds no strong view over a regular house that gains sides")
    n = row["n"]
    entry = every[n]
    axis_entry = {**entry["reference"], defaults.LAPSED: lapse_of(entry)}
    rehoused = [axis_entry if int(found["n"]) == n else found for found in document["entries"]]
    adopted = tmp_path / "index.json"
    adopted.write_text(json.dumps({**document, "entries": rehoused}), encoding="utf-8")
    # The real derivation, on an index of this count alone, so it measures one count.
    alone = tmp_path / "alone.json"
    alone.write_text(json.dumps({**document, "entries": [axis_entry]}), encoding="utf-8")
    regenerated = defaults.document(index=alone)
    (state,) = regenerated["states"]
    assert state["n"] == n
    assert state["state"] == defaults.PENDING
    assert state["lapsed"] == lapse_of(entry)
    assert f"the {entry['generator']} view of an earlier witness lapsed" in state["why"]
    # What the gate now catches: the drawing has fewer full shared sides than the view.
    assert state["measures"]["house_total"] < row["measures"]["house_total"]

    # The lapse is what makes it pending here: without it the house reads regular, as
    # before, so a hand merge that drops the block falls back to that, never further.
    bare = {key: value for key, value in axis_entry.items() if key != defaults.LAPSED}
    measured = _measured(regenerated, n)
    assert (
        defaults.count_state(n, bare, measured, state["witness"])["state"]
        == defaults.REGULAR_AS_PUBLISHED
    )

    # The gate fails on it until the generators decide the new witness.
    record["states"] = [state if found["n"] == n else found for found in record["states"]]
    found, _listed = defaults.state_problems(_write(tmp_path, record), adopted)
    assert [line for line in found if line.startswith(f"n={n}")] == [
        (
            f"n={n} is pending: {state['why']}. Run the strong generators on its witness "
            '(regularization-process.md, "When a Witness Changes"), or allow it in '
            "PENDING_ALLOWED with the bead that owns the run"
        )
    ]

    # A decision recorded on the new witness settles it, and the gate does not then ask
    # for the entry to be taken off as if the house's regularity had decided the count.
    # It names a run a record holds, here the lapsed view's own, whose block the index
    # keeps and `retain_runs` copies into the evidence.
    witness = state["witness"]
    settled = {
        **defaults.SETTLED,
        n: defaults.Settled(
            defaults.DECIDED,
            str(witness["source"]),
            str(witness["path"]),
            witness["revision"],
            str(witness["side"]),
            ((str(entry["generator"]), str(entry["run"]["id"])),),
            "drew no better",
            "a test",
        ),
    }
    decided = defaults.count_state(n, axis_entry, measured, witness, settled=settled)
    assert decided["state"] == defaults.DECIDED
    record["states"] = [decided if found["n"] == n else found for found in record["states"]]
    evidence = tmp_path / "evidence"
    only = {n: settled[n]}
    assert defaults.retain_runs(adopted, evidence, settled=only) == ([entry["run"]["id"]], [])
    found, _listed = defaults.state_problems(
        _write(tmp_path, record), adopted, settled=settled, evidence=evidence
    )
    assert [line for line in found if line.startswith(f"n={n}")] == []


def test_a_held_strong_view_is_recorded_held_with_the_rules_reason() -> None:
    # Review B3 of #636, at the reviewer's count (26 today, the first a strong view
    # regularizes over an irregular house): where the layer holds a strong view the rule
    # does not draw, the run's outcome reads `held: ` and why, not `view`, so the record
    # does not say a view decided what it did not draw.
    record = _record()
    every = defaults.index_entries()
    views = {found["n"]: found for found in record["entries"]}
    row = next(
        (
            row
            for row in record["states"]
            if row["state"] == defaults.REGULARIZED_STATE
            and every[row["n"]].get("generator") in defaults.STRONG_GENERATORS
            and (
                views[row["n"]]["measures"]["uneven_axis"][defaults.HOUSE]
                or views[row["n"]]["measures"]["near_axis"][defaults.HOUSE]
            )
        ),
        None,
    )
    if row is None:
        pytest.skip("the data holds no strong view of an irregular house")
    n = row["n"]
    view = views[n]
    drawn = defaults.count_state(n, every[n], view, row["witness"])
    assert drawn["decisions"][-1]["outcome"] == "view"
    later = {**every[n], "generator": "regularize_grid_slack/1", "run": {"id": "a-later-run"}}
    held = {**view, "default": defaults.HOUSE, "reason": "worse on hues", "worse": ["hues"]}
    state = defaults.count_state(n, later, held, row["witness"])
    assert state["state"] == defaults.DECIDED
    assert state["decisions"][-1] == {
        "generator": "regularize_grid_slack/1",
        "run": "a-later-run",
        "outcome": "held: worse on hues",
    }


def test_a_held_view_is_explained_in_the_policys_words() -> None:
    # The n = 176 note read "worse on uneven_axis", the code's key (review A9 of #636).
    record = _record()
    held = defaults.held_reasons()
    for row in record["entries"]:
        if row["default"] != defaults.HOUSE:
            continue
        words = held[row["view"]]
        assert not any(goal in words for goal in rule.MEASURES), words
        if row["worse"]:
            assert words == "it draws " + ", ".join(
                defaults._worse_words(goal)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
                for goal in row["worse"]
            )
    assert defaults._worse_words("uneven_axis") == "more uneven squares"  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert (
        defaults._worse_words("house_total")  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        == "a smaller house total of full shared sides"
    )
    assert defaults._worse_words(rule.SIDE) == "a larger exact side"  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]


def test_a_held_view_does_not_lead_the_case_note() -> None:
    # Where the house is drawn although the layer holds a view, the note says so first
    # instead of opening "Regularized by" (n = 176, think-gvke).
    from devtools import regularized_drawings  # noqa: PLC0415

    held = defaults.held_reasons()
    item = {
        "by": regularized_drawings.PROJECT_REGULARIZER,
        "credit": regularized_drawings.AXIS_CREDIT,
        "generator": regularized_drawings.AXIS_GENERATOR,
        "side": "same",
        "of": "T-1",
        "view": next(iter(held)),
    }
    note = regularized_drawings.case_note([item], held=held)
    assert note.startswith(
        "Drawn as published: the layer's regularized view does not improve on the packing"
    )
    assert "The view was regularized by the Squares Project" in note
    assert regularized_drawings.case_note([item]).startswith("Regularized by")


def _regular_house(measured: dict) -> dict:
    """What was measured at a count, with its house drawing given no uneven and no
    near-axis square: a new house that reads regular."""
    measures = dict(measured["measures"])
    for key in ("uneven_axis", "near_axis"):
        value = measures[key]
        measures[key] = {**value, defaults.HOUSE: 0} if isinstance(value, dict) else 0
    return {**measured, "measures": measures}


def test_an_allowed_count_owes_its_runs_whatever_its_new_house_reads(tmp_path: Path) -> None:
    """Review B1 of #641: fourteen of the twenty counts `PENDING_ALLOWED` first named lost
    a strong view before #636 wrote the index's `lapsed` block (272's and 304's Evan
    Daniel views were never admitted to the index at all), so their axis records carry
    none. A new house
    with no uneven and no near-axis square read `regular-as-published`, the gate asked for
    the entry to come off, and the runs its bead owes were dropped. Held on every real
    entry the list names, each as the index holds it, and on a real axis record a test
    allows: on the list, a count stays pending whatever its house reads."""
    from devtools import adopt_houses as adopt  # noqa: PLC0415

    record = _record()
    rows = {row["n"]: row for row in record["states"]}
    every = defaults.index_entries()
    extra = next(
        n
        for n, entry in sorted(every.items())
        if n not in defaults.PENDING_ALLOWED
        and entry["generator"] == defaults.ALGORITHM
        and defaults.LAPSED not in entry
    )
    allowed = {
        **defaults.PENDING_ALLOWED,
        extra: "think-la7h: a test; its grid-slack view lapsed",
    }
    counts = sorted(n for n in allowed if defaults.LAPSED not in every[n])
    assert extra in counts
    regenerated = []
    for n in counts:
        measured = _regular_house(_measured(record, n))
        witness = rows[n]["witness"]
        state = defaults.count_state(n, every[n], measured, witness, allowed=allowed)
        assert state["state"] == defaults.PENDING, n
        assert f"allowed pending: {allowed[n]}" in state["why"], n
        # Off the list, the same entry and house read regular: the gap the list closes.
        bare = defaults.count_state(n, every[n], measured, witness, allowed={})
        assert bare["state"] == defaults.REGULAR_AS_PUBLISHED, n
        regenerated.append((state, bare))

    # The gate lists each as allowed and asks for none to come off; on the record the
    # earlier rule gave, it asked for every one to come off.
    corrected = {extra: _correction(rows[extra])}

    def gate(states: dict[int, dict]) -> tuple[list[str], list[str]]:
        changed = {**record, "states": [states.get(row["n"], row) for row in record["states"]]}
        return defaults.state_problems(
            _write(tmp_path, changed), allowed=allowed, corrected=corrected
        )

    found, listed = gate({state["n"]: state for state, _bare in regenerated})
    assert found == []
    assert all(f"n={n} is pending, allowed: {allowed[n]}" in listed for n in counts)
    found, _listed = gate({bare["n"]: bare for _state, bare in regenerated})
    assert found == [
        f"n={n}: PENDING_ALLOWED names it, but it is regular-as-published; take it off the list"
        for n in counts
    ]

    # The adoption's printout counts each as certain to be pending, naming its bead.
    owed = adopt.regularization_owed(counts, allowed=allowed, day="2026-10-16")
    certain = [line for line in owed if line.startswith("    ") and ": " in line[:10]]
    for n in counts:
        bead = defaults.BEAD.match(allowed[n])
        assert bead is not None, n
        assert any(
            line.startswith(f"    {n}: ")
            and f"PENDING_ALLOWED holds it for {bead[0]}'s runs" in line
            for line in certain
        ), n


def test_a_decision_outranks_the_allowlist(tmp_path: Path) -> None:
    """Review C1 of #641: since B1 the list is an input to the state at one branch, so the
    promise that a count leaves the list as soon as it is decided rests on that branch's
    order. Held at a real allowlisted count, its new house read regular: a strong view
    drawn, a strong view held and a `SETTLED` decision on its witness each decide it, and
    the gate then asks for the entry to come off."""
    record = _record()
    rows = {row["n"]: row for row in record["states"]}
    views = {row["n"]: row for row in record["entries"]}
    document = json.loads(defaults.INDEX.read_text(encoding="utf-8"))
    every = {int(entry["n"]): entry for entry in document["entries"]}
    allowed = dict(defaults.PENDING_ALLOWED)
    corrected = dict(defaults.CORRECTED)
    # The decision names a run the retained evidence holds and whose record does not
    # rule the count out: a copied block that lists no counts, or a receipt that lists
    # the count, so the settlement-run rules ask nothing more of it (review F1 of #644).
    records = defaults.run_records()
    driver_runs = [
        (run, found)
        for run, found in sorted(records.items())
        if found.retained and found.generator == "evand-regularize"
    ]

    def covered(count: int) -> str | None:
        return next(
            (
                run
                for run, found in driver_runs
                if found.counts is None or count in found.counts
            ),
            None,
        )

    if not allowed:
        # The live list is empty once the stack's last allowed counts are decided, so a
        # count the layer draws is allowed here, as a corrected witness's deferral would
        # allow it: since the house rule no adoption defers (reviews A5 and B2 of #660).
        drawn = next(
            n
            for n in sorted(views)
            if n not in defaults.SETTLED
            and every[n].get("generator") == defaults.ALGORITHM
            and covered(n) is not None
        )
        allowed = {drawn: "think-0000: a corrected witness"}
        corrected = {drawn: _correction(rows[drawn])}
    n = next(n for n in sorted(allowed) if n in views and n not in defaults.SETTLED)
    witness = rows[n]["witness"]
    house = _regular_house(views[n])
    strong = {
        **every[n],
        "generator": "regularize_grid_slack/1",
        "run": {"id": "grid-slack-a-test-run"},
    }
    strong.pop(defaults.LAPSED, None)
    run = covered(n)
    assert run is not None
    settled = {
        **defaults.SETTLED,
        n: defaults.Settled(
            defaults.DECIDED,
            str(witness["source"]),
            str(witness["path"]),
            witness["revision"],
            str(witness["side"]),
            (("evand-regularize", run),),
            "drew no better",
            "a test",
        ),
    }
    cases = {
        defaults.REGULARIZED_STATE: (strong, {**house, "default": defaults.REGULARIZED}, None),
        defaults.DECIDED: (
            strong,
            {**house, "default": defaults.HOUSE, "reason": "worse on hues"},
            None,
        ),
        "settled": (every[n], house, settled),
    }
    for case, (entry, measured, held) in cases.items():
        state = defaults.count_state(n, entry, measured, witness, settled=held, allowed=allowed)
        expected = defaults.DECIDED if case == "settled" else case
        assert state["state"] == expected, case
        assert "allowed pending" not in state["why"], case

        index = tmp_path / f"index-{expected}.json"
        entries = [entry if int(found["n"]) == n else found for found in document["entries"]]
        index.write_text(json.dumps({**document, "entries": entries}), encoding="utf-8")
        changed = {
            **record,
            "states": [state if row["n"] == n else row for row in record["states"]],
        }
        found, _listed = defaults.state_problems(
            _write(tmp_path, changed), index, settled=held, allowed=allowed, corrected=corrected
        )
        assert found == [
            f"n={n}: PENDING_ALLOWED names it, but it is {expected}; take it off the list"
        ], case


def test_the_comparison_lists_what_each_changed_count_draws(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Review A1 of #641: an adoption shows its pull request what each re-housed count drew
    before and draws now, from the base branch's record. It names the goals at a count
    whose strong view gives way to a drawing worse than it on a goal of the improvement
    rule (review D1), and marks one still pending with the obligation every re-housed
    count carries, that its runs are owed in this pull request (reviews E1, E2, F1 and F2
    of #641, and the house rule)."""
    earlier = _record()
    assert defaults.drawing_changes(earlier, earlier) == []
    strong = next(
        row
        for row in earlier["states"]
        if row["state"] == defaults.REGULARIZED_STATE and row["drawn"] == defaults.VIEW
    )
    regular = _first_state(earlier, defaults.REGULAR_AS_PUBLISHED)
    later = json.loads(defaults.text(earlier))
    rows = {row["n"]: row for row in later["states"]}
    fallen = rows[strong["n"]]
    measures = strong["measures"]
    uneven, near, total = (
        measures["uneven_axis"] + 3,
        measures["near_axis"] + 1,
        measures["house_total"] - 7,
    )
    fallen.update(
        state=defaults.PENDING,
        drawn=defaults.HOUSE,
        generator=None,
        witness={**fallen["witness"], "side": "1"},
        measures={**measures, "uneven_axis": uneven, "near_axis": near, "house_total": total},
    )
    # The new house is exactly verified, so only the three measures are lost.
    for entry in later["entries"]:
        if entry["n"] == strong["n"]:
            entry["house_exact"] = True
    rows[regular["n"]]["witness"] = {**regular["witness"], "revision": "a new one"}
    before = (
        f"regularized, the {strong['generator']} view ({measures['uneven_axis']} uneven, "
        f"{measures['near_axis']} near-axis, {measures['house_total']} full shared sides)"
    )
    house = regular["measures"]
    same = (
        f"regular-as-published, the house drawing ({house['uneven_axis']} uneven, "
        f"{house['near_axis']} near-axis, {house['house_total']} full shared sides)"
    )
    expected = {
        strong["n"]: (
            f"n={strong['n']} (a new witness): {before} -> pending, the house drawing "
            f"({uneven} uneven, {near} near-axis, {total} full shared sides); the strong view "
            "gives way to a drawing worse on uneven squares, near-axis squares, house total "
            "of full shared sides: its runs are owed in this pull request"
        ),
        regular["n"]: f"n={regular['n']} (a new witness): {same} -> {same}",
    }
    assert defaults.drawing_changes(earlier, later) == [expected[n] for n in sorted(expected)]

    # From the command line, against the base branch's record kept in a file.
    base = tmp_path / "base.json"
    base.write_text(defaults.text(earlier), encoding="utf-8")
    assert defaults.parser().parse_args(["--compare", str(base)]).compare == base
    assert defaults.compare(base, record=_write(tmp_path, later)) == 0
    assert capsys.readouterr().out.splitlines() == [
        *(expected[n] for n in sorted(expected)),
        (
            "2 counts changed state, drawing or witness; where a strong view gives way to a "
            "drawing worse than it on a goal of the improvement rule, whatever drew it: 1 "
            "still pending, whose runs are owed in this pull request, and 0 in another state"
        ),
    ]


#: #657's adoption at n = 302, as its review B4 and review D1 of #641 give it: light,
#: uneven and near-axis squares, angle classes, hues, house and stage totals.
LOST_302 = (0, 0, 0, 14, 14, 978, 978)
AXIS_302 = (6, 26, 11, 40, 19, 882, 952)


def _row(
    n: int, drawn: str, generator: str | None, side: str, measures: tuple[int, ...]
) -> dict:
    """A state row as the record writes one, with what `drawing_changes` reads."""
    strong = generator in defaults.STRONG_GENERATORS
    return {
        "n": n,
        "state": defaults.REGULARIZED_STATE if strong else defaults.PENDING,
        "drawn": drawn,
        "generator": generator,
        "witness": {"id": f"W-known-best-n{n:03d}", "source": side, "side": side},
        "measures": dict(zip(rule.MEASURES, measures, strict=True)),
    }


def _losses(
    earlier: dict, later: dict, *, house_exact: bool | None = None
) -> tuple[list[str], bool]:
    """What `drawing_changes` says at one count: the goals it names a lost strong view's
    replacement worse on, and whether it marks the count's runs as owed in this pull
    request."""
    record = {"states": [later]}
    if house_exact is not None:
        record["entries"] = [{"n": later["n"], "house_exact": house_exact}]
    (line,) = defaults.drawing_changes({"states": [earlier]}, record)
    _picture, _semicolon, goals = line.partition(f"; {defaults.LOST} ")
    if not goals:
        return [], False
    owed = goals.endswith(f": {defaults.RUNS_OWED}")
    return goals.removesuffix(f": {defaults.RUNS_OWED}").split(", "), owed


EVAND, AXIS = "evand-regularize", "regularize_axis_components/2"
ALL_SEVEN = [rule.GOAL_NAMES[key] for key in rule.MEASURES]


@pytest.mark.parametrize(
    ("earlier", "later", "house_exact", "goals"),
    [
        # 302 at #657: the axis tool's view of the new witness replaces Evan Daniel's view
        # of the old one, worse on all seven measures; the predicate at 7aa4775ea marked
        # none of #657's seven such losses, since it asked for the house drawing.
        pytest.param(
            _row(302, defaults.VIEW, EVAND, "17.5", LOST_302),
            _row(302, defaults.VIEW, AXIS, "17.4", AXIS_302),
            None,
            ALL_SEVEN,
            id="302-axis-view",
        ),
        # #636's B2 at 230: a regular house, exactly verified, with fewer full shared
        # sides (626 to 562), which no uneven or near-axis square shows.
        pytest.param(
            _row(230, defaults.VIEW, EVAND, "15.9", (0, 0, 0, 5, 5, 626, 626)),
            _row(230, defaults.HOUSE, None, "15.8", (0, 0, 0, 5, 5, 562, 562)),
            True,
            [rule.GOAL_NAMES["house_total"], rule.GOAL_NAMES["stage_total"]],
            id="230-regular-house-fewer-sides",
        ),
        # A house drawing as regular as the lost view, but not shown exactly verified:
        # the view was, so exactness is lost.
        pytest.param(
            _row(230, defaults.VIEW, EVAND, "15.9", (0, 0, 0, 5, 5, 626, 626)),
            _row(230, defaults.HOUSE, None, "15.8", (0, 0, 0, 5, 5, 626, 626)),
            None,
            [rule.GOAL_NAMES[rule.EXACTNESS]],
            id="house-not-shown-exact",
        ),
        pytest.param(
            _row(230, defaults.VIEW, EVAND, "15.9", (0, 0, 0, 5, 5, 626, 626)),
            _row(230, defaults.HOUSE, None, "15.8", (0, 0, 0, 5, 5, 626, 626)),
            True,
            [],
            id="exact-house-as-good",
        ),
        # A larger side is worse on the side, whatever the measures.
        pytest.param(
            _row(302, defaults.VIEW, EVAND, "17.4", LOST_302),
            _row(302, defaults.VIEW, AXIS, "17.5", LOST_302),
            None,
            [rule.GOAL_NAMES[rule.SIDE]],
            id="larger-side",
        ),
        # An axis view better on every measure at a smaller side loses nothing.
        pytest.param(
            _row(302, defaults.VIEW, EVAND, "17.5", AXIS_302),
            _row(302, defaults.VIEW, AXIS, "17.4", LOST_302),
            None,
            [],
            id="axis-view-better",
        ),
        # A strong view worse than the one it replaces is listed too: whatever drew it.
        # Its runs have run, so it reads regularized and is not marked (review E2).
        pytest.param(
            _row(302, defaults.VIEW, EVAND, "17.5", LOST_302),
            _row(302, defaults.VIEW, "regularize_grid_slack/1", "17.4", AXIS_302),
            None,
            ALL_SEVEN,
            id="strong-view-worse",
        ),
        # No strong view was drawn, so none is lost.
        pytest.param(
            _row(302, defaults.VIEW, AXIS, "17.5", LOST_302),
            _row(302, defaults.HOUSE, None, "17.4", AXIS_302),
            None,
            [],
            id="axis-view-before",
        ),
        # n = 51's algebraic side is not compared, and nothing else is lost.
        pytest.param(
            _row(51, defaults.VIEW, EVAND, "['16/3', '5/3']", LOST_302),
            _row(51, defaults.VIEW, AXIS, "9", LOST_302),
            None,
            [],
            id="algebraic-side",
        ),
    ],
)
def test_a_lost_strong_view_is_marked_with_every_goal_its_replacement_is_worse_on(
    earlier: dict,
    later: dict,
    house_exact: bool | None,  # noqa: FBT001
    goals: list[str],
) -> None:
    """Review D1 of #641: the mark asked for an irregular house drawing, but after an
    adoption the axis tool's view usually replaces a lost strong view, since the refresh
    draws it wherever it improves on the new house. Whatever drew the replacement, the
    goals the improvement rule finds it worse than the lost view on are named, and the
    count is marked where it still reads pending (review E2)."""
    named, owed = _losses(earlier, later, house_exact=house_exact)
    assert named == goals
    assert owed == (bool(goals) and later["state"] == defaults.PENDING)


@pytest.mark.parametrize(
    ("state", "owed"),
    [
        (defaults.PENDING, True),
        (defaults.DECIDED, False),
        (defaults.REGULARIZED_STATE, False),
        (defaults.EXEMPT, False),
    ],
)
def test_only_a_count_still_pending_is_marked_with_its_runs_owed(
    state: str,
    owed: bool,  # noqa: FBT001
) -> None:
    """Review E2 of #641: at #657, 146 and 156 read `regularized` and 176 reads
    `decided-no-better`, so their runs have run, yet each line asked for the owner's word.
    The goals are named whatever the count's state now; only a count still pending is
    marked, its runs owed in this pull request."""
    later = {**_row(302, defaults.VIEW, AXIS, "17.4", AXIS_302), "state": state}
    named, marked = _losses(_row(302, defaults.VIEW, EVAND, "17.5", LOST_302), later)
    assert named == ALL_SEVEN
    assert marked is owed


def test_the_summary_counts_pending_and_settled_losses_apart(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Review E2 of #641: the summary counted every listed loss as waiting. It counts the
    counts still pending apart from those in another state: at #657, six of the nine are
    pending, and three are regularized or decided."""
    earlier = {
        "states": [_row(n, defaults.VIEW, EVAND, "17.5", LOST_302) for n in (176, 211, 302)]
    }
    later = {
        "states": [
            {**_row(176, defaults.VIEW, AXIS, "17.4", AXIS_302), "state": defaults.DECIDED},
            _row(211, defaults.VIEW, AXIS, "17.4", AXIS_302),
            _row(302, defaults.VIEW, AXIS, "17.4", AXIS_302),
        ]
    }
    paths = []
    for name, record in (("earlier", earlier), ("later", later)):
        path = tmp_path / f"{name}.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        paths.append(path)
    assert defaults.compare(paths[0], record=paths[1]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert [line.endswith(defaults.RUNS_OWED) for line in lines[:3]] == [False, True, True]
    assert lines[-1].endswith(
        f"where {defaults.STRONG_VIEW_LOST}: 2 still pending, whose runs are owed in this "
        "pull request, and 1 in another state"
    )


def test_a_deferral_is_a_correction_held_to_the_base_record() -> None:
    """Reviews A5, B1, B2 and C3 of #660. The check that a re-housed count is never deferred
    read the day a pass gave itself and covered register adoptions only (A5, B1); it then
    failed the deferral the runbook allows a corrected witness (B2), and passed a house
    move declared as one (C3). Each entry is a correction now, held to the base branch's
    record: the witness it names as replaced is the base's, and the record's keeps that
    source and exact side and is another witness only."""
    record = _record()
    rows = {row["n"]: row for row in record["states"]}
    assert defaults.deferral_problems(rows, defaults.PENDING_ALLOWED) == []
    n = 68
    before = rows[n]["witness"]
    allowed = {n: "think-aaaa: a deferral"}
    base = _base(rows)

    # B1: a deferral that names no correction fails, whatever day its pass gives.
    (problem,) = defaults.deferral_problems(rows, allowed, base=base)
    assert problem.startswith(f"n={n}: PENDING_ALLOWED defers its runs, but CORRECTED names no")

    # B2: a witness corrected at its house's source and exact side, at a new revision,
    # may wait once its entry names the witness it replaced.
    newer = {**rows, n: {**rows[n], "witness": {**before, "revision": "a-newer-revision"}}}
    fix = {n: _replaced(before)}
    assert defaults.deferral_problems(newer, allowed, corrected=fix, base=base) == []
    assert defaults.deferral_problems(rows, {}, corrected=fix) == [
        f"n={n}: CORRECTED names it, but PENDING_ALLOWED does not; take it off"
    ]

    # C3: the reviewer's three house moves, each declared as a correction, fail, whether
    # the entry names the witness the base holds or the one the change brought.
    def moved(m: int, **change: str) -> dict:
        return {**rows, m: {**rows[m], "witness": {**rows[m]["witness"], **change}}}

    kingbird = next(
        m
        for m, row in sorted(rows.items())
        if row["witness"]["source"] == "Kingbird derived numerical facts"
        and row["witness"]["revision"] is None
    )
    moves = {
        "re-housed to a smaller side from a new source": (
            n,
            moved(
                n,
                source="[PingYou PR 574 certificates 2026-10-13]",
                side="87987952372182838/10000000000000000",
                revision="4c319c2",
            ),
        ),
        "re-solved from the same source to another side": (
            n,
            moved(n, side="1/2", revision="new-revision"),
        ),
        "a Kingbird catalogue intake at a smaller side": (
            kingbird,
            moved(kingbird, side="1/3"),
        ),
    }
    for case, (m, after) in moves.items():
        changed = _base(rows, frozenset({m}))
        for declared in (_replaced(rows[m]["witness"]), _replaced(after[m]["witness"])):
            found = defaults.deferral_problems(
                after, {m: "think-aaaa: a deferral"}, corrected={m: declared}, base=changed
            )
            assert len(found) == 1, (case, declared)
            assert found[0].startswith(f"n={m}: CORRECTED says the correction replaced"), case

    # A genuine fix at a source that pins no revision, as Kingbird's catalogue: the
    # witness names itself as before, and its file changed.
    witness = rows[kingbird]["witness"]
    declared = {kingbird: _replaced(witness)}
    entry = {kingbird: "think-aaaa: the catalogue's corrected witness"}
    altered = _base(rows, frozenset({kingbird}))
    assert defaults.deferral_problems(rows, entry, corrected=declared, base=altered) == []
    (problem,) = defaults.deferral_problems(rows, entry, corrected=declared, base=base)
    assert "the record's is that witness: there is no corrected witness to defer" in problem

    # Once the correction has merged, the base itself defers the count at its witness.
    deferred_row = {
        **rows[kingbird],
        "state": defaults.PENDING,
        "why": (
            f"no strong generator has decided this witness; allowed pending: {entry[kingbird]}"
        ),
    }
    merged = _base({**rows, kingbird: deferred_row})
    pending = {**rows, kingbird: deferred_row}
    assert defaults.deferral_problems(pending, entry, corrected=declared, base=merged) == []

    # D1: a pinned correction merged at 68, its runs deferred; a later change that only
    # rewrites the corrected witness's file, or its path, leaves the entry standing, and
    # a move after it does not.
    corrected = {**before, "revision": "a-newer-revision"}
    deferred = {
        **rows[n],
        "witness": corrected,
        "state": defaults.PENDING,
        "why": f"no strong generator has decided this witness; allowed pending: {allowed[n]}",
    }
    after_fix = {**rows, n: deferred}
    standing = {n: _replaced(before)}
    for changed in (frozenset(), frozenset({n})):
        base_after = _base(after_fix, changed)
        assert (
            defaults.deferral_problems(after_fix, allowed, corrected=standing, base=base_after)
            == []
        ), changed
        repathed = {
            **after_fix,
            n: {**deferred, "witness": {**corrected, "path": "x/n-068.json"}},
        }
        assert (
            defaults.deferral_problems(repathed, allowed, corrected=standing, base=base_after)
            == []
        ), changed
    moved_since = {**after_fix, n: {**deferred, "witness": {**corrected, "side": "1/2"}}}
    (problem,) = defaults.deferral_problems(
        moved_since,
        allowed,
        corrected={n: _replaced(moved_since[n]["witness"])},
        base=_base(after_fix),
    )
    assert problem.startswith(f"n={n}: origin/main's record defers it at the witness from")
    assert "the house has moved since" in problem

    # D1: at a source that pins a revision, a changed file alone is no correction: the
    # entry names the record's own witness, as it would with no base.
    (problem,) = defaults.deferral_problems(
        rows, allowed, corrected={n: _replaced(before)}, base=_base(rows, frozenset({n}))
    )
    assert "there is no corrected witness to defer" in problem

    # With no base the entry is checked as declared: it may not name the record's own
    # witness where the source pins a revision.
    (problem,) = defaults.deferral_problems(rows, allowed, corrected=fix)
    assert "there is no corrected witness to defer" in problem


def test_the_state_gate_holds_each_correction_to_its_base(tmp_path: Path) -> None:
    """The records tier's state gate runs the base-held check (`--check-state --base-ref`),
    so a refactor that unwires it fails here, as review B7 of #660 found the bead tree's
    gate untested: a house move declared as a correction fails `--check-state`."""
    record = _record()
    rows = {row["n"]: dict(row) for row in record["states"]}
    n = 68
    before = rows[n]["witness"]
    for row in record["states"]:
        if row["n"] == n:
            row["witness"] = {**before, "source": "[new]", "side": "1/2"}
    allowed = {**defaults.PENDING_ALLOWED, n: "think-aaaa: a correction"}
    corrected = {n: _replaced(before)}
    problems, _listed = defaults.state_problems(
        _write(tmp_path, record),
        allowed=allowed,
        corrected=corrected,
        base=_base(rows, frozenset({n})),
    )
    assert any(problem.startswith(f"n={n}: CORRECTED says") for problem in problems)
    assert defaults.main(["--check-state", "--base-ref", "HEAD"]) == 0
    with pytest.raises(SystemExit):
        defaults.main(["--check", "--base-ref", "HEAD"])


def test_the_records_tier_passes_the_base_and_requires_it_held(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Review D4 of #660: without `--base-ref` the gate passes, checking each entry only as
    declared, and the step required the pass line alone, so a step that stopped passing
    the base stayed green. It passes `origin/main`, or `HEAD^1` on main itself, and
    requires the line that says the base was held to."""
    import os  # noqa: PLC0415

    from sqpack.cli import validate  # noqa: PLC0415

    observed: list[tuple[str, ...]] = []
    held = f"{defaults.HELD_TO_BASE} origin/main\nregularization state check passed: ..."

    def capture(_context: validate.Context, module: str, *given: str) -> str:
        observed.append((module, *given))
        return output

    heads = {"HEAD": "aaaa\n", "origin/main": "bbbb\n"}
    monkeypatch.setattr(validate, "_module", capture)
    monkeypatch.setattr(validate, "_git", lambda *args: heads[args[-1]])
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )
    step = validate._regularization_state  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    output = held
    assert step(context) == held
    assert observed == [
        ("devtools.default_drawings", "--check-state", "--base-ref", "origin/main")
    ]
    heads["origin/main"] = heads["HEAD"]
    step(context)
    assert observed[-1][-1] == "HEAD^1"
    output = "regularization state check passed: ...\nCORRECTED is checked as declared"
    with pytest.raises(validate.StepFailureError, match="CORRECTED is held to the record"):
        step(context)


def test_the_base_is_read_only_where_a_count_is_deferred(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Review D5 of #660: the gate read the base before anything else, so a clone without
    the merge base failed with nothing deferred. Now it reads the base only where the list
    names a count, and says so either way."""

    def unread(ref: str) -> defaults.Base:
        raise AssertionError(f"read {ref}")

    monkeypatch.setattr(defaults, "base_record", unread)
    monkeypatch.setattr(defaults, "PENDING_ALLOWED", {})
    monkeypatch.setattr(defaults, "CORRECTED", {})
    assert defaults.check_state("origin/main") == 0
    assert (
        f"{defaults.HELD_TO_BASE} origin/main; nothing is deferred" in capsys.readouterr().out
    )
    monkeypatch.setattr(defaults, "PENDING_ALLOWED", {68: "think-aaaa: a correction"})
    with pytest.raises(AssertionError, match="read origin/main"):
        defaults.check_state("origin/main")


def _repository(root: Path) -> None:
    """A repository with main, a branch off its first commit that alters one witness, and
    main's second commit, which the branch has not merged."""
    import subprocess  # noqa: PLC0415

    def git(*args: str) -> None:
        subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)

    def write(path: str, text: str) -> None:
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")

    def record(side: str) -> str:
        return json.dumps({"states": [{"n": 1, "witness": {"side": side}}, {"n": 2}]})

    git("init", "-q", "-b", "main")
    git("config", "user.email", "test@example.com")
    git("config", "user.name", "test")
    write(defaults.RECORD_PATH, record("1"))
    write(f"{defaults.WITNESSES_PATH}/n-001.yaml", "side: 1\n")
    write(f"{defaults.WITNESSES_PATH}/n-002.yaml", "side: 2\n")
    git("add", "-A")
    git("commit", "-qm", "base")
    git("checkout", "-qb", "work")
    write(f"{defaults.WITNESSES_PATH}/n-002.yaml", "side: 2\nnote: a corrected file\n")
    git("commit", "-qam", "work")
    git("checkout", "-q", "main")
    write(defaults.RECORD_PATH, record("1/2"))
    git("commit", "-qam", "main moves on")
    git("checkout", "-q", "work")


def test_the_base_record_is_read_from_the_merge_base(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review D4 of #660: `base_record`'s Git reads were untested. It reads the record at
    the merge base, not the base's tip, finds the witness file the change altered, names
    a missing ref, and tells a shallow clone how to get its merge base (D5)."""
    import subprocess  # noqa: PLC0415

    root = tmp_path / "repository"
    root.mkdir()
    _repository(root)
    monkeypatch.setattr(defaults, "REPO", root)
    base = defaults.base_record("main")
    assert base.ref == "main"
    assert base.rows[1]["witness"] == {"side": "1"}
    assert base.changed == frozenset({2})
    with pytest.raises(SystemExit, match="--base-ref no-such-ref names no commit"):
        defaults.base_record("no-such-ref")

    shallow = tmp_path / "shallow"
    subprocess.run(
        ["git", "clone", "-q", "--depth", "1", "--branch", "work", root.as_uri(), str(shallow)],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(shallow), "fetch", "-q", "--depth", "1", "origin", "main:main"],
        check=True,
        capture_output=True,
    )
    monkeypatch.setattr(defaults, "REPO", shallow)
    with pytest.raises(SystemExit, match="git fetch --unshallow"):
        defaults.base_record("main")
