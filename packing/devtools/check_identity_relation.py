#!/usr/bin/env python3
"""Score candidate endpoint-identity relations against the two exact controls.

`Atlas.add` calls two endpoints the same basin when their quantized geometric key *and*
their contact certificate agree, and `distinct_basins` is then read as a count of
connected terminal components.  `D-034` records that this splits one connected optimum
family into quantization-dependent rows.  This module asks the prior question -- which
relation *should* be counted -- and answers it the only way that is checkable: against
cases whose component count is already proved.

**The controls are the two exact moduli experiments**, and between them they isolate the
two independent reasons the current key disagrees with a component count:

- `exp-015` at `n = 4` is pure *symmetry*.  The labelled space is 24 isolated grids and
  the `D4 x S4` quotient is a single point, with no connectivity involved at all.  A
  relation that does not quotient reports 24 where the answer is 1.
- `exp-014` at `n = 3` is pure *connectivity*.  The `D4 x S3` quotient is the interval
  `[0,1/2]`, one component, carrying three orbit strata and **two** contact certificates:
  `C` has one, `G` and `M` share the other.  A relation that does not merge along the
  retained closure relation `closure(G) = [C, G, M]` reports 2 where the answer is 1.

Neither control alone is enough, and that is the point of running both.  A relation can
pass one for the wrong reason: `side` alone gets `n = 3` right because every point of
`F_3(2)` has side 2, and it is refuted only by the labelled `n = 4` count.

**This module refuses rather than scores where it cannot decide.**  A relation is
reported `undecidable` on a control when the retained artifact does not carry the
invariant it needs, which is different from being wrong, and the difference is exactly
what `BC-080` was asked to report.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESULTS = ROOT / "campaign" / "series" / "series-000-smoke-and-calibration" / "results"
UNDECIDABLE = "undecidable"


@dataclass(frozen=True)
class Control:
    """One exact case whose component count is proved, at one level of quotient."""

    name: str
    n: int
    level: str
    component_count: int
    """The proved answer. Every relation is scored against this and nothing else."""

    isolates: str
    samples: tuple[dict[str, Any], ...]
    strata_closure: dict[str, tuple[str, ...]]


def _load(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def controls() -> list[Control]:
    """The four proved answers the retained experiments carry."""
    n3 = _load(RESULTS / "exp-014-h-032-n3-optimal-moduli.json")
    n4 = _load(RESULTS / "exp-015-h-032-n4-optimal-moduli.json")
    n3_samples = tuple(n3["samples"])
    # BC-082 retained these. Before it, `exp-015` carried its proved counts and no
    # per-sample keys, so the one control that most directly tests the relation
    # `Atlas.add` implements could not score it at all.
    n4_samples = tuple(n4["samples"])
    closure_raw = n3["spaces"]["d4_s3_quotient"].get("incidence", {})
    closure = {
        key.removeprefix("closure(").removesuffix(")"): tuple(value)
        for key, value in closure_raw.items()
    }
    return [
        Control(
            name="n=3 labelled",
            n=3,
            level="labelled",
            component_count=n3["spaces"]["labelled"]["component_count"],
            isolates="connectivity, before any quotient",
            samples=n3_samples,
            strata_closure=closure,
        ),
        Control(
            name="n=3 D4xS3 quotient",
            n=3,
            level="d4_s3_quotient",
            component_count=n3["spaces"]["d4_s3_quotient"]["component_count"],
            isolates="connectivity: one interval, three strata, two contact certificates",
            samples=n3_samples,
            strata_closure=closure,
        ),
        Control(
            name="n=4 labelled",
            n=4,
            level="labelled",
            component_count=n4["spaces"]["labelled"]["component_count"],
            isolates="symmetry: 24 isolated labelled grids, no connectivity at all",
            samples=n4_samples,
            strata_closure={},
        ),
        Control(
            name="n=4 D4xS4 quotient",
            n=4,
            level="d4_s4_quotient",
            component_count=n4["spaces"]["d4_s4_quotient"]["component_count"],
            isolates="symmetry: the same 24 states as one orbit",
            samples=n4_samples,
            strata_closure={},
        ),
    ]


Relation = Callable[[Control], int | str]


def _keys(control: Control, field: str) -> int | str:
    """Distinct values of one per-sample field, or `undecidable` with no samples.

    A control with no retained samples cannot score a sample-based relation. Saying so
    is the honest answer; returning 1 for an empty set would make every such relation
    look correct on the control that most discriminates.
    """
    if not control.samples:
        return UNDECIDABLE
    return len({sample[field] for sample in control.samples})


def relation_side_alone(control: Control) -> int | str:
    """Every point of an optimal configuration space has the optimal side, by definition.

    So this returns 1 wherever it can answer at all, which is why it passes the `n = 3`
    controls for a reason that has nothing to do with being right.
    """
    return 1


def relation_geometric_and_contact(control: Control) -> int | str:
    """What `Atlas.add` counts today: both hashes must agree."""
    if not control.samples:
        return UNDECIDABLE
    return len({(s["geometric_key"], s["contact_certificate"]) for s in control.samples})


def relation_contact_alone(control: Control) -> int | str:
    return _keys(control, "contact_certificate")


def relation_contact_with_closure(control: Control) -> int | str:
    """Contact certificates, merged where one stratum lies in another's closure.

    This is the relation the `n = 3` artifact makes checkable: it retains
    `closure(G) = [C, G, M]`, so the two certificates on that interval are two strata of
    one connected set rather than two components.
    """
    certificates = _keys(control, "contact_certificate")
    if certificates == UNDECIDABLE:
        return UNDECIDABLE
    if not control.strata_closure:
        return certificates
    merged = {frozenset(members) for members in control.strata_closure.values()}
    return max(1, len(merged))


NOT_APPLICABLE = "n/a"


@dataclass(frozen=True)
class Candidate:
    """One identity relation, and the level at which it claims to be a component count.

    The level is not decoration. A contact certificate is invariant under relabelling and
    under `D4`, so it is a statement about the quotient and cannot distinguish two
    labelled components that differ only by a relabelling. Scoring it against a labelled
    control would refute it for the wrong reason.

    `any` marks a relation that claims to work at every level. That is a stronger claim,
    and it is the one `side alone` makes and fails.
    """

    relation: Relation
    level: str
    why: str


RELATIONS: dict[str, Candidate] = {
    "side alone": Candidate(
        relation_side_alone, "any", "the optimal side, shared by every point"
    ),
    # Declared `quotient`, not `labelled`, and the correction is D-375. Both inputs are
    # canonical under relabelling and under D4 by construction -- `geometric_key` sorts
    # the squares and minimises over the eight container images, and
    # `contact_certificate` does the same -- so this relation cannot distinguish two
    # labelled components differing only by a relabelling, and scoring it against a
    # labelled control refutes it for doing what it is built to do. X-005 made exactly
    # that argument for `contact alone` and `contact + closure` and did not apply it
    # here. At its true level it is still refuted, by the n = 3 quotient control, which
    # is D-034 and is the refutation that was always load-bearing.
    "geometric + contact": Candidate(
        relation_geometric_and_contact, "quotient", "what Atlas.add counts today (D-034)"
    ),
    "contact alone": Candidate(
        relation_contact_alone, "quotient", "the contact certificate, ignoring pose"
    ),
    "contact + closure": Candidate(
        relation_contact_with_closure,
        "quotient",
        "certificates merged along the retained strata closure",
    ),
}


def _applies(candidate: Candidate, control: Control) -> bool:
    if candidate.level == "any":
        return True
    if candidate.level == "quotient":
        return "quotient" in control.level
    return control.level == "labelled"


def score(candidate: Candidate) -> list[tuple[Control, int | str, str]]:
    rows = []
    for control in controls():
        if not _applies(candidate, control):
            rows.append((control, NOT_APPLICABLE, NOT_APPLICABLE))
            continue
        got = candidate.relation(control)
        if got == UNDECIDABLE:
            verdict = "undecidable"
        elif got == control.component_count:
            verdict = "agrees"
        else:
            verdict = "REFUTED"
        rows.append((control, got, verdict))
    return rows


PAIR = RESULTS / "bc-083-n5-identity-pair.json"


def prospective_pair() -> dict[str, Any] | None:
    """`D-034`'s two n = 5 endpoints, retained by `devtools.build_n5_identity_pair`.

    A *prospective* control: its two constituents are retained and its component count is
    not proved, so it is scored for what it would decide rather than for what it does.
    """
    if not PAIR.exists():
        return None
    return _load(PAIR)


def prospective_verdicts(pair: dict[str, Any]) -> dict[str, tuple[int, dict[int, str]]]:
    """What each relation reports on the pair, and what each possible answer decides.

    The pair is two endpoints, so the only answers in question are 1 (one component seen
    twice) and 2 (two components). Every relation is evaluated on the two retained
    endpoints directly; there is no closure data at n = 5, so `contact + closure` and
    `contact alone` coincide here, and that is itself part of what the control reports.
    """
    endpoints = pair["endpoints"]
    reports = {
        "side alone": 1,
        "geometric + contact": len(
            {(e["geometric_key"], e["contact_certificate"]) for e in endpoints}
        ),
        "contact alone": len({e["contact_certificate"] for e in endpoints}),
        "contact + closure": len({e["contact_certificate"] for e in endpoints}),
    }
    return {
        name: (got, {answer: ("agrees" if got == answer else "REFUTED") for answer in (1, 2)})
        for name, got in reports.items()
    }


def discriminating(results: dict[str, list[tuple[Control, int | str, str]]]) -> bool:
    """Does the control set separate the candidates, or pass more than one?

    A control set that every candidate survives has not tested anything. This is the
    check `BC-080`'s acceptance rule needed and did not have: as originally written it
    named only the two quotient controls, and `side alone` passes both.
    """
    surviving = [
        name
        for name, rows in results.items()
        if all(verdict != "REFUTED" for _control, _got, verdict in rows)
    ]
    return len(surviving) <= 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero unless the controls separate the candidate relations",
    )
    args = parser.parse_args(argv)

    results = {name: score(candidate) for name, candidate in RELATIONS.items()}

    print(f"{'control':<24}{'proved':>8}  isolates")
    for control in controls():
        print(f"  {control.name:<22}{control.component_count:>8}  {control.isolates}")
    print()

    header = f"{'relation':<22}{'level':<10}" + "".join(f"{c.name:>22}" for c in controls())
    print(header)
    for name, rows in results.items():
        cells = "".join(
            f"{(verdict if got in (NOT_APPLICABLE, UNDECIDABLE) else f'{got} {verdict}'):>22}"
            for _c, got, verdict in rows
        )
        print(f"{name:<22}{RELATIONS[name].level:<10}{cells}")
    print()

    surviving = [
        name
        for name, rows in results.items()
        if all(verdict != "REFUTED" for _c, _g, verdict in rows)
    ]
    print(f"survives every control: {surviving or 'none'}")
    separates = discriminating(results)
    print(
        "the control set separates the candidates"
        if separates
        else f"the control set does NOT separate them: {len(surviving)} survive"
    )

    quotient_only = {
        name: [row for row in rows if "quotient" in row[0].level]
        for name, rows in results.items()
    }
    passing_quotient_only = [
        name
        for name, rows in quotient_only.items()
        if all(verdict != "REFUTED" for _c, _g, verdict in rows)
    ]
    print(
        f"survives the quotient controls alone: {passing_quotient_only} "
        f"-- the labelled controls are what refute the rest"
    )

    pair = prospective_pair()
    if pair is not None:
        print()
        print("prospective control -- D-034's n=5 pair, component count NOT proved")
        measured = pair["measured"]
        print(
            f"  two endpoints at side {pair['subject']['side']}; "
            f"same contact certificate: {measured['share_contact_certificate']}; "
            f"same geometric key: {measured['share_geometric_key']}"
        )
        verdicts = prospective_verdicts(pair)
        print(f"  {'relation':<22}{'reports':>9}{'if 1':>10}{'if 2':>10}")
        for name, (got, by_answer) in verdicts.items():
            print(f"  {name:<22}{got:>9}{by_answer[1]:>10}{by_answer[2]:>10}")
        for answer in (1, 2):
            split = {
                verdict
                for _got, by_answer in verdicts.values()
                for verdict in [by_answer[answer]]
            }
            if len(split) < 2:
                print(f"  answer {answer} would decide nothing: every relation {split.pop()}")
        # The point of the table: whichever way it resolves, it separates the two
        # relations no existing control separates, and one branch refutes the standing
        # winner. That is what makes it worth the proof it is waiting on.
        print(
            f"  missing quantity: {pair['subject']['defect']} "
            "-- see why_component_count_is_null"
        )

    if args.check and not separates:
        print("controls do not separate the candidate relations", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
