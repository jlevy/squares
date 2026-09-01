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

from collections.abc import Sequence
from typing import Any

from devtools.build_n5_identity_pair import measurement_problem
from devtools.check_identity_relation import (
    NOT_APPLICABLE,
    RELATIONS,
    Control,
    controls,
    discriminating,
    prospective_pair,
    prospective_verdicts,
    relation_contact_alone,
    relation_contact_with_closure,
    relation_geometric_and_contact,
    relation_side_alone,
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

    This is `D-034` as a number rather than a description: the `n = 3` D4xS3 quotient is
    one component, and four retained samples of it produce four distinct keys.

    Scored at the *quotient* level, which is `D-375`. `geometric_key` is relabelling- and
    D4-invariant by construction, and exp-015's 24 labelled states are measured to collapse
    to one key and one certificate, so the relation is a quotient statement; the labelled
    controls report `n/a` for it, exactly as they do for the other two quotient relations.
    The refutation is unchanged in force and is now attributed to the control that can
    carry it. (`contact_certificate` is *not* invariant by construction -- see D-375 --
    which is why the argument runs through the measurement rather than the code.)
    """
    verdicts = _verdicts()["geometric + contact"]
    assert verdicts["n=3 D4xS3 quotient"] == "REFUTED"
    assert verdicts["n=3 labelled"] == NOT_APPLICABLE
    assert verdicts["n=4 labelled"] == NOT_APPLICABLE


def test_no_relabelling_invariant_relation_can_pass_a_labelled_control() -> None:
    """`D-375`'s second half, and the constraint it puts on `BC-083`.

    The n = 4 labelled control has 24 states that differ only by relabelling. The claim is
    that no candidate can report 24 there, so the control refutes the whole family and
    separates none of it -- the dual of `D-373`, where every answer was 1 and everything
    passed.

    The assertion is against the *retained samples*, not against the relations' return
    values. An earlier version collected the candidates the control scores, but `_applies`
    admits only `side alone` at a labelled control, and that relation returns 1
    unconditionally -- so it pinned a two-line constant and would have passed unchanged if
    every key in the campaign had stopped being relabelling invariant. What actually
    carries the claim is that exp-015's 24 states collapse to one key and one certificate.
    """
    n4 = next(c for c in controls() if c.name == "n=4 labelled")
    assert len(n4.samples) == 24
    assert n4.component_count == 24
    # The measurement the claim rests on: 24 distinct labelled states, one key each.
    assert len({s["geometric_key"] for s in n4.samples}) == 1
    assert len({s["contact_certificate"] for s in n4.samples}) == 1
    assert len({s["state"] for s in n4.samples}) == 24
    # So every key-based relation reports 1 against a proved 24, whatever its level.
    assert relation_geometric_and_contact(n4) == 1
    assert relation_contact_alone(n4) == 1
    assert relation_side_alone(n4) == 1


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

    A contact certificate is a statement about the quotient: it is minimised over the
    eight container images, and over well-separated angles it is invariant under
    relabelling in every case fuzzed. Two labelled components differing only by a
    relabelling therefore share it, and calling that a refutation would reject the right
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


def test_the_n5_pair_discriminates_whichever_way_it_resolves() -> None:
    """`BC-083`'s answer, as a computation rather than an argument.

    The two existing quotient controls both have component count 1, so a merge-everything
    relation passes them (`D-373`). The `n = 4` labelled control has count 24, which no
    relabelling-invariant relation can reach, so it refutes all of them (`D-375`). A
    discriminating control has to sit between those, and `D-034`'s `n = 5` pair does:
    neither of its two possible answers is unanimous.

    The stronger half is that answer 2 refutes `contact + closure`, the standing sole
    survivor. A control that can only confirm the current winner would not be worth the
    proof it is waiting on.
    """
    pair = prospective_pair()
    assert pair is not None, "the retained n=5 pair is missing"
    verdicts = prospective_verdicts(pair)
    for answer in (1, 2):
        outcomes = {by_answer[answer] for _got, by_answer in verdicts.values()}
        assert outcomes == {"agrees", "REFUTED"}, (
            f"answer {answer} is unanimous ({outcomes}), so the pair would decide nothing"
        )
    assert verdicts["contact + closure"][1][2] == "REFUTED"
    assert verdicts["geometric + contact"][1][1] == "REFUTED"


def test_the_n5_pair_measures_what_d034_asserted() -> None:
    """`D-034` quoted these invariants for three years of session-time without retaining them.

    The claim is that the two endpoints share a contact certificate while differing
    geometrically. Now that both endpoints are retained, that is checkable rather than
    quotable, and it is what makes the pair a control at all: if they differed in contact
    certificate too, every relation would report 2 and the pair would decide nothing.
    """
    pair = prospective_pair()
    assert pair is not None
    assert pair["measured"]["share_contact_certificate"] is True
    assert pair["measured"]["share_geometric_key"] is False
    # D-021's floor is 1e-11; a side difference below it is not a difference.
    assert pair["measured"]["side_difference"] < 1e-11
    assert pair["component_count"] is None, (
        "a proved count here would close D-034; it must not appear without one"
    )


def test_identity_pair_replay_ignores_only_subfloor_float_drift() -> None:
    retained = {
        "share_contact_certificate": True,
        "share_geometric_key": False,
        "side_difference": 8.881784197001252e-16,
    }
    rebuilt = {**retained, "side_difference": 2.6645352591003757e-15}
    assert measurement_problem(retained, rebuilt) is None
    assert "solver floor" in (
        measurement_problem(retained, {**rebuilt, "side_difference": 2e-11}) or ""
    )
    assert (
        measurement_problem(retained, {**rebuilt, "share_geometric_key": True})
        == "share_geometric_key has drifted"
    )


def test_contact_with_closure_reads_its_certificates() -> None:
    """The relation's certificate half, tested where a retained control cannot test it.

    On the `n = 3` quotient control `closure(G) = [C, G, M]` covers every stratum, so any
    faithful implementation returns 1 whatever the certificates say. That is a property of
    the control, not of the relation (`D-378`), and it means the retained set never
    exercises half the definition. A synthetic control with two *disjoint* closure classes
    does, and this is what distinguishes the relation from a merge-everything one.
    """
    sample = {"parameter": "0", "contact_certificate": "a", "geometric_key": "g"}

    def control(samples: Sequence[dict[str, Any]]) -> Control:
        return Control(
            name="synthetic",
            n=3,
            level="d4_s3_quotient",
            component_count=2,
            isolates="two disjoint closure classes",
            samples=tuple(samples),
            strata_closure={"P": ("P", "Q"), "R": ("R", "S")},
            strata={"P": "0", "Q": "1/4", "R": "1/2", "S": "3/4"},
        )

    # Four samples, one per stratum, all with distinct certificates: the two closure
    # classes merge P~Q and R~S, leaving two components.
    distinct = [
        {**sample, "parameter": p, "contact_certificate": c}
        for p, c in (("0", "a"), ("1/4", "b"), ("1/2", "c"), ("3/4", "d"))
    ]
    assert relation_contact_with_closure(control(distinct)) == 2

    # One certificate shared across the two classes merges them: the relation says two
    # endpoints agreeing on their certificate are the same component, and it must act on
    # that even when no closure connects their strata.
    shared = [
        {**sample, "parameter": p, "contact_certificate": c}
        for p, c in (("0", "a"), ("1/4", "a"), ("1/2", "a"), ("3/4", "a"))
    ]
    assert relation_contact_with_closure(control(shared)) == 1


def test_no_retained_control_separates_closure_from_merging_everything() -> None:
    """`D-378`, as an assertion rather than a remark.

    The record carries exactly one closure set and it covers every stratum of the only
    control that has any, so `contact + closure` and `side alone` cannot be told apart on
    the retained quotient controls. If a future control adds a second, disjoint closure
    class, this fails -- and that failure is the good news, because it means the relation
    has finally become testable.
    """
    with_closure = [c for c in controls() if c.strata_closure]
    assert len(with_closure) == 2, "only the two n=3 controls carry closure data"
    for control in with_closure:
        classes = {frozenset(members) for members in control.strata_closure.values()}
        assert len(classes) == 1
        covered = set().union(*classes)
        assert covered == set(control.strata), (
            "the closure no longer covers every stratum, so this control can now "
            "distinguish contact + closure from a merge-everything relation"
        )
