#!/usr/bin/env python3
"""The case-level rigidity block is held to the contract its evidence records are held to.

`check_evidence_semantics` enforces the assurance-method pairing on `evidence.yaml`. The
case-level `rigidity` block was the one first-party claim that escaped it: the schema
requires only `[property, assurance, scope, evidence]`, leaves `method`, `certificate` and
`replay` optional and nullable, and couples none of them. `D-396` is what that allowed.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from sqpack.assurance import check_case_semantics
from sqpack.yamlio import safe_load

FRONTIER = Path(__file__).resolve().parent.parent / "frontier"


def load_evidence() -> dict[str, dict]:
    document = safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))
    return {record["id"]: record for record in document["evidence"]}


def load_case(n: int) -> dict:
    path = FRONTIER / f"n-{n:03d}.md"
    return safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]


def rigidity_errors(case: dict, evidence: dict[str, dict]) -> list[str]:
    return [error for error in check_case_semantics(case, evidence) if "rigidity:" in error]


def test_every_retained_case_satisfies_the_rigidity_contract() -> None:
    """All hundred cases pass as they stand, so the guard added no retroactive debt."""
    evidence = load_evidence()
    failures = {
        n: errors
        for n in range(1, 101)
        if (errors := check_case_semantics(load_case(n), evidence))
    }
    assert failures == {}, f"cases now failing: {failures}"


def test_a_verified_block_may_not_rest_on_numerical_evidence() -> None:
    """The flattering direction, and the one this guard exists for.

    `n = 65`'s rigidity evidence is `numerically-checked` at `tolerance: 1e-8`. Relabelling
    the block `verified` is a formal claim resting on a numerical one, and before `D-396`
    nothing refused it.
    """
    evidence = load_evidence()
    case = deepcopy(load_case(65))
    cited = evidence[case["rigidity"]["evidence"][0]]
    assert cited["assurance"] == "numerically-checked", "premise of this test changed"

    case["rigidity"].update(assurance="verified", method="exact-algebraic")
    assert any(
        "requires at least one verified evidence record" in error
        for error in rigidity_errors(case, evidence)
    )


def test_a_numerical_method_may_not_carry_verified_assurance() -> None:
    evidence = load_evidence()
    case = deepcopy(load_case(65))
    case["rigidity"].update(assurance="verified", method="numerical-multiprecision")
    assert any(
        "numerical method cannot support verified" in error
        for error in rigidity_errors(case, evidence)
    )


def test_verified_requires_a_formal_method() -> None:
    evidence = load_evidence()
    case = deepcopy(load_case(65))
    case["rigidity"].update(assurance="verified", method=None)
    assert any(
        "verified requires a formal method" in error
        for error in rigidity_errors(case, evidence)
    )


def test_a_formal_method_may_not_carry_numerical_assurance() -> None:
    evidence = load_evidence()
    case = deepcopy(load_case(65))
    case["rigidity"].update(assurance="numerically-checked", method="exact-algebraic")
    assert any(
        "formal method requires verified assurance" in error
        for error in rigidity_errors(case, evidence)
    )


def test_certificate_and_replay_may_be_delegated_to_the_cited_record() -> None:
    """The ten perfect squares rely on this, and it must keep working.

    Their blocks leave `certificate` and `replay` null and delegate to
    `E-perfect-square-tiling-rigid`, which carries both. `n = 5`, `11` and `40` name the
    artifacts on the block instead. Both conventions are legitimate.
    """
    evidence = load_evidence()
    for n in (1, 4, 9, 16, 25, 36, 49, 64, 81, 100):
        case = load_case(n)
        block = case["rigidity"]
        assert block["assurance"] == "verified"
        assert not block.get("certificate") and not block.get("replay")
        assert rigidity_errors(case, evidence) == [], f"n={n} should pass by delegation"


def test_a_machine_formal_claim_backed_nowhere_is_refused() -> None:
    """Delegation is not a loophole: the cited record must actually carry the artifacts."""
    evidence = load_evidence()
    stripped = deepcopy(evidence)
    stripped["E-perfect-square-tiling-rigid"].update(certificate=None, replay=None)

    case = load_case(9)
    assert rigidity_errors(case, evidence) == [], "n=9 passes against intact evidence"
    assert any(
        "requires certificate and replay" in error for error in rigidity_errors(case, stripped)
    ), "with the artifacts gone from both block and record, the claim must be refused"


def test_an_unsupported_pair_is_refused_rather_than_ignored() -> None:
    """The catch-all `check_evidence_semantics` has and this once did not.

    Every branch of the guard is keyed on a value the block might not have, so before the
    catch-all the least-specified claim was the least checked: `reported` with no method,
    or no assurance at all, produced no error.
    """
    evidence = load_evidence()
    for patch in (
        {"assurance": "reported", "method": None},
        {"assurance": None, "method": None},
        {"assurance": "numerically-checked", "method": None},
    ):
        case = deepcopy(load_case(65))
        case["rigidity"].update(patch)
        assert any(
            "unsupported assurance-method pair" in error
            for error in rigidity_errors(case, evidence)
        ), patch


def test_reported_rigidity_is_refused_outright() -> None:
    """The block has no `reported_method` to carry it, and the register forbids it anyway.

    What a source says about rigidity belongs in `reported_upper_bound.catalogue_rigid`
    and must not be restated in this block.
    """
    evidence = load_evidence()
    case = deepcopy(load_case(65))
    case["rigidity"].update(assurance="reported", method=None, evidence=[])
    assert rigidity_errors(case, evidence)


def test_verified_rigidity_may_not_rest_on_a_bound_record() -> None:
    """Verified backing must also be backing about rigidity.

    Requiring only `assurance == verified` let a rigidity claim rest on a record of the
    right n proving something else entirely -- an upper bound, say -- which is backing in
    name only.
    """
    evidence = load_evidence()
    borrowed = deepcopy(evidence["E-n040-gobel-upper"])
    assert borrowed["claim"] == "upper-bound", "premise of this test changed"
    borrowed["scope"] = {"n_values": [65]}
    evidence = {**evidence, "E-n040-gobel-upper": borrowed}

    case = deepcopy(load_case(65))
    case["rigidity"].update(
        assurance="verified", method="exact-algebraic", evidence=["E-n040-gobel-upper"]
    )
    assert any(
        "claiming derived-structure" in error for error in rigidity_errors(case, evidence)
    )
