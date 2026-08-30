"""The identity relation the atlas should count, pinned against the exact controls.

`BC-080` asked what relation the atlas should count, given that `Atlas.add` requires a
quantized geometric key *and* a contact certificate to agree, and that `distinct_basins`
is then read as a count of connected terminal components (`D-034`).

These assertions are the answer in the only form that can be checked: verdicts against
cases whose component count is proved. If a future change to the relation, to the
controls, or to the retained experiment data moves any of them, this fails and the
argument in `X-005` has to be made again rather than assumed.
"""

from __future__ import annotations

from devtools.check_identity_relation import (
    NOT_APPLICABLE,
    RELATIONS,
    controls,
    discriminating,
    score,
)


def _verdicts() -> dict[str, dict[str, str]]:
    return {
        name: {control.name: verdict for control, _got, verdict in score(candidate)}
        for name, candidate in RELATIONS.items()
    }


def test_the_proved_component_counts_are_what_the_experiments_recorded() -> None:
    """The controls must come from the artifacts, not from this file.

    A control whose answer is typed here rather than read from `exp-014` and `exp-015`
    would let the relation be scored against a number nobody proved.
    """
    assert {c.name: c.component_count for c in controls()} == {
        "n=3 labelled": 2,
        "n=3 D4xS3 quotient": 1,
        "n=4 labelled": 24,
        "n=4 D4xS4 quotient": 1,
    }


def test_only_contact_with_closure_survives_every_control() -> None:
    """The declared relation, and the reason it is the declared one."""
    surviving = [
        name
        for name, rows in _verdicts().items()
        if all(verdict != "REFUTED" for verdict in rows.values())
    ]
    assert surviving == ["contact + closure"]


def test_the_current_atlas_relation_is_refuted_where_it_can_be_scored() -> None:
    """`geometric + contact` splits one connected component into four sampled rows.

    This is `D-034` as a number rather than a description: the `n = 3` labelled space has
    two components, and four retained samples of it produce four distinct keys.
    """
    assert _verdicts()["geometric + contact"]["n=3 labelled"] == "REFUTED"


def test_the_quotient_controls_alone_do_not_discriminate() -> None:
    """The finding that matters, and the reason this block did not simply declare a winner.

    `BC-046` wrote the acceptance rule as "a criterion that the exact `n = 3` sliding
    family and the exact `n = 4` point both satisfy" -- the two *quotient* controls. Both
    have component count 1, so a relation that merges everything passes them. `side alone`
    is exactly that relation, and it is known wrong: `D-034` records two `n = 5` rows
    sharing a side while differing geometrically.

    The labelled controls are what refute it, because their answers are 2 and 24 rather
    than 1. An acceptance rule whose every control has the same answer cannot separate a
    relation that merges correctly from one that merges indiscriminately.
    """
    quotient_only = {
        name: [
            verdict
            for control, _got, verdict in score(candidate)
            if "quotient" in control.level
        ]
        for name, candidate in RELATIONS.items()
    }
    survivors = [name for name, verdicts in quotient_only.items() if "REFUTED" not in verdicts]
    assert "side alone" in survivors, (
        "a merge-everything relation must survive the quotient controls, or this "
        "block's central finding has stopped being true"
    )
    assert len(survivors) > 1


def test_the_full_control_set_does_discriminate() -> None:
    """Adding the labelled controls is what makes the acceptance rule a test."""
    assert discriminating({name: score(c) for name, c in RELATIONS.items()})


def test_a_quotient_relation_is_not_scored_against_a_labelled_control() -> None:
    """Scoring by level, so a relation is not refuted for the wrong reason.

    A contact certificate is invariant under relabelling and under `D4`, so it is a
    statement about the quotient. Two labelled components differing only by a relabelling
    share it by construction, and calling that a refutation would reject the right
    relation for doing exactly what it is supposed to do.
    """
    rows = {control.name: got for control, got, _v in score(RELATIONS["contact + closure"])}
    assert rows["n=3 labelled"] == NOT_APPLICABLE
    assert rows["n=3 D4xS3 quotient"] == 1


def test_side_alone_is_refuted_by_both_labelled_controls() -> None:
    """It claims to work at any level, which is the claim that fails.

    Every point of an optimal configuration space has the optimal side by definition, so
    this relation returns 1 everywhere. It is right twice by coincidence and wrong twice
    for the same reason.
    """
    rows = _verdicts()["side alone"]
    assert rows["n=3 labelled"] == "REFUTED"
    assert rows["n=4 labelled"] == "REFUTED"
    assert rows["n=3 D4xS3 quotient"] == "agrees"
    assert rows["n=4 D4xS4 quotient"] == "agrees"
