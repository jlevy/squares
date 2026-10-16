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
    # allowed pending here as an adoption's deferral would allow it, with its bead.
    pending["state"] = defaults.PENDING
    allowed = {**defaults.PENDING_ALLOWED, pending["n"]: "think-0000: a deferral"}
    found, _listed = defaults.state_problems(_write(tmp_path, record), allowed=allowed)
    assert found == []
    # A count allowed pending that is no longer pending fails until it comes off the list.
    pending["state"] = defaults.REGULARIZED_STATE
    found, _listed = defaults.state_problems(_write(tmp_path, record), allowed=allowed)
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
    found, _listed = defaults.state_problems(_write(tmp_path, record), allowed=allowed)
    assert found == [f"n={joining['n']}: PENDING_ALLOWED names no bead: 'later'"]


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
    n = 204
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
    assert (
        f"n={n}: SETTLED names run evand-regularize-3a-rerun-s-1016, which no record holds"
    ) in "\n".join(found)
    assert (
        f"n={n}: SETTLED names run evand-regularize-3a-1016, which only the layer's index holds"
    ) in "\n".join(found)


def test_a_settlement_keeps_its_record_when_the_index_drops_a_run(tmp_path: Path) -> None:
    # The index keeps a run's block only while an entry draws from it, so a settlement
    # resting on an index block failed as soon as later work redrew that run's views:
    # #657 redraws all five views of evand-regularize-3a-1016, and 272's settlement then
    # named a run no record held (review F1 of #644). Every run a settlement names is held
    # by the retained evidence instead, and the index's block of one that had no other is
    # copied there (`--retain-runs`).
    records = defaults.run_records()
    for n, held in defaults.SETTLED.items():
        for generator, run in held.runs:
            assert records[run].generator == generator, (n, run)
            assert records[run].retained, (n, run)
    index = json.loads(defaults.INDEX.read_text(encoding="utf-8"))
    indexed = {block["id"] for block in index["runs"]}
    dropped = {"evand-regularize-3a-1016", "grid-slack-on518"}
    index["runs"] = [block for block in index["runs"] if block["id"] not in dropped]
    without = tmp_path / "index.json"
    without.write_text(json.dumps(index), encoding="utf-8")
    found, _listed = defaults.state_problems(index=without)
    assert found == []

    # Into evidence without the copies, `retain_runs` copies the blocks again as they
    # are committed, and a second pass writes nothing.
    committed = defaults.EVIDENCE / defaults.SETTLED_RUNS
    copies = sorted(path.name for path in committed.iterdir())
    evidence = tmp_path / "evidence"
    shutil.copytree(
        defaults.EVIDENCE, evidence, ignore=shutil.ignore_patterns(defaults.SETTLED_RUNS)
    )
    found, _listed = defaults.state_problems(evidence=evidence)
    assert found
    assert all("which only the layer's index holds" in problem for problem in found)
    assert {problem.split()[4].rstrip(",") for problem in found} == set(copies)
    assert defaults.retain_runs(evidence=evidence) == (copies, [])
    for run in copies:
        copied = evidence / defaults.SETTLED_RUNS / run / "run.json"
        assert copied.read_bytes() == (committed / run / "run.json").read_bytes()
    assert defaults.retain_runs(evidence=evidence) == ([], [])
    assert defaults.state_problems(evidence=evidence)[0] == []

    # A run neither the index nor the evidence holds any longer cannot be retained. Into
    # no evidence at all, every other named run the index still holds is copied: the
    # committed copies, and on a layer whose own runs the index records beside their
    # receipts, those runs too.
    named = {run for held in defaults.SETTLED.values() for _generator, run in held.runs}
    written, missing = defaults.retain_runs(index=without, evidence=tmp_path / "none")
    assert set(written) == (named & indexed) - dropped
    assert set(copies) - dropped <= set(written)
    assert set(missing) == dropped | (named - indexed)


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
    assert records["evand-regularize-3a-1016"].counts is None
    n = 204
    held = defaults.SETTLED[n]
    named = (*held.runs, ("evand-regularize", "evand-regularize-3a-rerun-303-1016"))
    found, _listed = defaults.state_problems(
        settled={**defaults.SETTLED, n: held._replace(runs=named)}
    )
    assert found == [
        (
            f"n={n}: SETTLED names run evand-regularize-3a-rerun-303-1016, whose record "
            "shows it ran 303, not 204"
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

    # And the gate fails on the regenerated record until the generators decide it.
    record["states"] = [state if found["n"] == n else found for found in record["states"]]
    found, _listed = defaults.state_problems(_write(tmp_path, record), adopted)
    assert [line for line in found if line.startswith(f"n={n}")] == [
        (
            f"n={n} is pending: {state['why']}. Run the strong generators on its witness "
            '(regularization-process.md, "When a Witness Changes"), or allow it in '
            "PENDING_ALLOWED with the bead that owns the run"
        )
    ]


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
