#!/usr/bin/env python3
"""An exact certificate this repository holds must be named by the record it bears on.

`D-398`: `cases/gobel40` and `cases/gobel_family` ran in the gate for two sessions while
the three frontier records they bear on declared a `mathematics` blocker saying no formal
certificate existed. Every existing check reads a record against its own fields, so none
of them could see a certificate the record was never told about.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest

from devtools.check_certificate_citations import (
    CASES,
    DEFERRAL_DAYS,
    FRONTIER,
    UndeclaredError,
    cited_certificates,
    declared_sizes,
    deferred,
    load_deferrals,
    main,
    method_limit_evidence,
    orphaned_evidence,
    referenced_evidence,
)
from sqpack.yamlio import safe_load


def evidence_by_id() -> dict[str, dict]:
    document = safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))
    return {record["id"]: record for record in document["evidence"]}


def last_reviewed() -> str:
    document = safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))
    return str(document["last_reviewed"])


def results() -> list[dict]:
    return safe_load((FRONTIER / "results.yaml").read_text(encoding="utf-8"))["results"]


def test_the_sweep_passes_on_the_retained_tree() -> None:
    assert main() == 0


def test_every_exact_verifier_declares_what_it_certifies() -> None:
    """An undeclared CERTIFIES is a refusal, not a skip, so a package cannot opt out."""
    modules = sorted(CASES.glob("*/verify_exact.py"))
    assert modules, "no exact verifiers found; the sweep would pass vacuously"
    for module in modules:
        sizes = declared_sizes(module)
        assert sizes, f"{module.parent.name} declares no CERTIFIES"
        assert all(1 <= n <= 100 for n in sizes), module.parent.name


def test_a_package_with_no_declaration_is_refused(tmp_path: Path) -> None:
    stub = tmp_path / "verify_exact.py"
    stub.write_text('"""A verifier that never says what it decides."""\n\nX = 1\n')
    assert declared_sizes(stub) is None


def test_it_catches_the_defect_it_was_written_for() -> None:
    """Drop D-398's evidence record and n=40 stops naming its own certificate.

    This is the state the repository was actually in: `cases/gobel40/verify_exact` decided
    780 pairs exactly, and `frontier/n-040.md` reached no evidence record pointing at it.
    """
    evidence = evidence_by_id()
    assert any(
        path.startswith("cases/gobel40/") for path in cited_certificates(40, evidence)
    ), "premise: n=40 cites its package today"

    before_promotion = {k: v for k, v in evidence.items() if k != "E-n040-gobel-upper"}
    assert not any(
        path.startswith("cases/gobel40/") for path in cited_certificates(40, before_promotion)
    ), "with the promotion's evidence removed, the sweep must find nothing citing the package"


def test_the_family_package_covers_both_of_its_sizes() -> None:
    """One replay decides two sizes, so both records must name it, not just one."""
    evidence = evidence_by_id()
    for n in (65, 89):
        assert any(
            path.startswith("cases/gobel_family/") for path in cited_certificates(n, evidence)
        ), n


def test_a_non_literal_declaration_is_refused_not_a_crash(tmp_path: Path) -> None:
    """An unreadable CERTIFIES must name its package, not abort the sweep.

    `ast.literal_eval` raises on `tuple(range(...))`, and an exception escaping `main`
    would stop every later package from being checked -- the guard failing open on the one
    input designed to confuse it.
    """
    stub = tmp_path / "verify_exact.py"
    stub.write_text("CERTIFIES = tuple(range(1, 4))\n")
    with pytest.raises(UndeclaredError):
        declared_sizes(stub)


def test_an_out_of_range_size_does_not_crash() -> None:
    """A size with no frontier record is a refusal; reading n-999.md would raise."""
    assert cited_certificates(999, {}) == set()


def test_a_reported_record_does_not_satisfy_the_sweep() -> None:
    """Citing a certificate is not claiming it.

    A `reported` evidence record carrying a path into a case package satisfies the letter
    of the sweep while asserting nothing this repository checked -- the record would name
    the certificate without claiming it. Verified is part of the question, not a separate
    one.
    """
    evidence = evidence_by_id()
    assert any(path.startswith("cases/gobel40/") for path in cited_certificates(40, evidence))

    downgraded = {
        key: ({**record, "assurance": "reported"} if key == "E-n040-gobel-upper" else record)
        for key, record in evidence.items()
    }
    assert not any(
        path.startswith("cases/gobel40/") for path in cited_certificates(40, downgraded)
    ), "a reported record must not satisfy the sweep"


def test_no_verified_evidence_is_cited_by_nothing() -> None:
    """The general form of D-398, and the half the CERTIFIES sweep cannot see.

    A case package is only one place a certificate lives. `E-n029-interval-certified-upper`
    is verified, replays, and proves a bound tighter than the one n = 29 carries -- and was
    cited by nothing while that record's blocker said no formal certificate existed. Its
    certificate is a witness file, so nothing keyed on `cases/` could have found it.

    An orphan stands only while a recorded deferral names it, and every deferral names
    one: nothing else is cited by nothing.
    """
    evidence = evidence_by_id()
    excused, problems = deferred(evidence, load_deferrals(), results(), last_reviewed())
    assert problems == []
    assert set(orphaned_evidence(evidence)) == excused


def test_the_orphan_check_bites() -> None:
    """Remove the one citation that closes it and the sweep must say so."""
    evidence = evidence_by_id()
    identifier = "E-n029-interval-certified-upper"
    assert identifier in evidence, "premise of this test changed"

    case = safe_load((FRONTIER / "n-029.md").read_text(encoding="utf-8").split("---\n")[1])
    assert identifier in referenced_evidence(case["packing"]), (
        "n = 29 must cite the interval certificate; without it the record is behind its "
        "own evidence, which is what D-398 named"
    )


def test_only_a_method_limit_result_stands_in_for_a_case_citation() -> None:
    """T-058's exact ceilings span n = 1..100 and no case block holds a method limit."""
    cited = method_limit_evidence(evidence_by_id())

    assert "E-wand125-tools-ceiling-certificates" in cited
    # A bound-bearing result's certificate must still be cited by its case.
    assert "E-n029-interval-certified-upper" not in cited


def test_a_method_limit_result_cannot_stand_in_for_a_bound() -> None:
    """Evidence that claims a bound needs a case citation even when a method limit cites it.

    Relabel T-058's ceiling certificates as a lower bound and the exception must let go of
    them, so the orphan sweep reports them, since no case record cites them.
    """
    evidence = dict(evidence_by_id())
    identifier = "E-wand125-tools-ceiling-certificates"
    evidence[identifier] = {**evidence[identifier], "claim": "lower-bound"}

    assert identifier not in method_limit_evidence(evidence)
    assert identifier in orphaned_evidence(evidence)


def test_evidence_refs_are_found_wherever_the_schema_puts_them() -> None:
    """Bounds, rigidity, the roster, conflicts and blockers all carry evidence lists.

    Reading a subset reports a citation as missing when it is merely somewhere else, and a
    guard that cries wolf gets switched off.
    """
    found = referenced_evidence(
        {
            "verified_upper_bound": {"evidence": ["A"]},
            "rigidity": {"evidence": ["B"]},
            "evidence": ["C"],
            "conflicts": [{"evidence": ["D"]}],
            "blockers": [{"evidence": ["E"]}],
        }
    )
    assert found == {"A", "B", "C", "D", "E"}


# --------------------------------------------------------------------------- deferrals


def _orphan(evidence: dict[str, dict]) -> tuple[dict[str, dict], str]:
    """The evidence with one verified, replayed certificate that no case record cites."""
    identifier = "E-test-orphaned-certificate"
    evidence = {
        **evidence,
        identifier: {
            "id": identifier,
            "claim": "upper-bound",
            "assurance": "verified",
            "replay_status": "passed",
            "certificate": "packing/resources/web/example/certificate.cert",
        },
    }
    return evidence, identifier


def _deferral(identifier: str, **changes: object) -> dict[str, object]:
    return {
        "evidence": identifier,
        "results": ["T-001"],
        "bead": "think-abcd",
        "blocked_on": "jlevy/squares#403",
        "recorded": "2026-10-10",
        "reason": "Case adoption waits for a pull request that rewrites the case records.",
        **changes,
    }


def _citing(identifier: str) -> list[dict]:
    return [{"id": "T-001", "evidence": [identifier]}]


def test_an_undeclared_orphan_still_fails() -> None:
    evidence, identifier = _orphan(evidence_by_id())
    assert identifier in orphaned_evidence(evidence)
    excused, problems = deferred(evidence, [], _citing(identifier), "2026-10-10")
    assert identifier not in excused
    assert problems == []


def test_a_recorded_deferral_excuses_the_orphan_it_names() -> None:
    evidence, identifier = _orphan(evidence_by_id())
    excused, problems = deferred(
        evidence, [_deferral(identifier)], _citing(identifier), "2026-10-10"
    )
    assert (excused, problems) == ({identifier}, [])


def test_a_deferral_goes_stale_once_a_case_record_cites_its_evidence() -> None:
    """n = 29 cites its interval certificate, so a deferral of it excuses nothing."""
    identifier = "E-n029-interval-certified-upper"
    excused, problems = deferred(
        evidence_by_id(), [_deferral(identifier)], _citing(identifier), "2026-10-10"
    )
    assert excused == set()
    assert len(problems) == 1
    assert "stale" in problems[0]


def test_a_deferral_names_register_entries_that_cite_its_evidence() -> None:
    evidence, identifier = _orphan(evidence_by_id())
    excused, problems = deferred(
        evidence, [_deferral(identifier)], [{"id": "T-001", "evidence": []}], "2026-10-10"
    )
    assert excused == {identifier}
    assert problems == [f"deferral of {identifier}: T-001 does not cite it"]


def test_a_deferral_expires() -> None:
    evidence, identifier = _orphan(evidence_by_id())
    late = (date(2026, 10, 10) + timedelta(days=DEFERRAL_DAYS + 1)).isoformat()
    excused, problems = deferred(evidence, [_deferral(identifier)], _citing(identifier), late)
    assert excused == set()
    assert len(problems) == 1
    assert "re-date" in problems[0]


def test_a_deferral_must_say_what_it_waits_on_and_who_owns_it() -> None:
    evidence, identifier = _orphan(evidence_by_id())
    excused, problems = deferred(
        evidence,
        [_deferral(identifier, bead="", blocked_on="")],
        _citing(identifier),
        "2026-10-10",
    )
    assert excused == set()
    assert problems == [f"deferral of {identifier}: names no bead, blocked_on"]
