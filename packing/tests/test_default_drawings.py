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
    pending = _first_state(record, defaults.PENDING)
    regular = _first_state(record, defaults.REGULAR_AS_PUBLISHED)
    # A count allowed pending that is no longer pending fails until it comes off the list.
    pending["state"] = defaults.REGULARIZED_STATE
    found, _listed = defaults.state_problems(_write(tmp_path, record))
    assert found == [
        (
            f"n={pending['n']}: PENDING_ALLOWED names it, but it is regularized; take it "
            "off the list"
        )
    ]
    # And a count that joins it names its bead.
    pending["state"] = defaults.PENDING
    regular["state"] = defaults.PENDING
    allowed = {**defaults.PENDING_ALLOWED, regular["n"]: "later"}
    found, _listed = defaults.state_problems(_write(tmp_path, record), allowed=allowed)
    assert found == [f"n={regular['n']}: PENDING_ALLOWED names no bead: 'later'"]


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
    # The ten decided counts rest on the #518 runs' prose; each says what think-0ut1 still
    # owes, so the record shows it (review A6 of #636).
    rows = {row["n"]: row for row in _record()["states"]}
    for n, held in defaults.SETTLED.items():
        if held.state == defaults.DECIDED:
            assert held.owed is not None, n
            assert held.owed.startswith("think-0ut1: "), n
            assert rows[n]["why"].endswith(f"; still owed: {held.owed}"), n
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
    # A bead an entry names elsewhere in its text is not the one that owns it.
    assert defaults.deferrals(settled={}, allowed={1: "later, maybe think-aaaa"}) == []


def test_a_lapsed_view_reads_pending_and_names_what_lapsed() -> None:
    record = _record()
    row = _first_state(record, defaults.PENDING)
    n = row["n"]
    entry = dict(defaults.index_entries()[n])
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

    # Or until the adoption's pull request defers it with the bead that owns its runs
    # (result-import.md, "Adopt a House, Then Regularize It"; think-g3q7): then the gate
    # lists it as allowed, and an entry naming no bead fails it again.
    def about(lines: list[str]) -> list[str]:
        return [line for line in lines if re.match(rf"n={n}\b", line)]

    deferred = {**defaults.PENDING_ALLOWED, n: "think-g3q7: re-housed by an adoption"}
    found, listed = defaults.state_problems(regenerated, adopted, allowed=deferred)
    assert about(found) == []
    assert about(listed) == [f"n={n} is pending, allowed: {deferred[n]}"]
    unowned = {**defaults.PENDING_ALLOWED, n: "until the runs fit the cap"}
    found, _listed = defaults.state_problems(regenerated, adopted, allowed=unowned)
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
    witness = state["witness"]
    settled = {
        **defaults.SETTLED,
        n: defaults.Settled(
            defaults.DECIDED,
            str(witness["source"]),
            str(witness["path"]),
            witness["revision"],
            str(witness["side"]),
            (("evand-regularize", "a-run"),),
            "drew no better",
            "a test",
        ),
    }
    decided = defaults.count_state(n, axis_entry, measured, witness, settled=settled)
    assert decided["state"] == defaults.DECIDED
    record["states"] = [decided if found["n"] == n else found for found in record["states"]]
    found, _listed = defaults.state_problems(_write(tmp_path, record), adopted, settled=settled)
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
    def gate(states: dict[int, dict]) -> tuple[list[str], list[str]]:
        changed = {**record, "states": [states.get(row["n"], row) for row in record["states"]]}
        return defaults.state_problems(_write(tmp_path, changed), allowed=allowed)

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
    allowed = defaults.PENDING_ALLOWED
    n = next(n for n in sorted(allowed) if n in views and n not in defaults.SETTLED)
    witness = rows[n]["witness"]
    house = _regular_house(views[n])
    strong = {
        **every[n],
        "generator": "regularize_grid_slack/1",
        "run": {"id": "grid-slack-a-test-run"},
    }
    strong.pop(defaults.LAPSED, None)
    settled = {
        **defaults.SETTLED,
        n: defaults.Settled(
            defaults.DECIDED,
            str(witness["source"]),
            str(witness["path"]),
            witness["revision"],
            str(witness["side"]),
            (("evand-regularize", "a-test-run"),),
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
            _write(tmp_path, changed), index, settled=held, allowed=allowed
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
