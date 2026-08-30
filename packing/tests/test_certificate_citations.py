#!/usr/bin/env python3
"""An exact certificate this repository holds must be named by the record it bears on.

`D-398`: `cases/gobel40` and `cases/gobel_family` ran in the gate for two sessions while
the three frontier records they bear on declared a `mathematics` blocker saying no formal
certificate existed. Every existing check reads a record against its own fields, so none
of them could see a certificate the record was never told about.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools.check_certificate_citations import (
    CASES,
    FRONTIER,
    Undeclared,
    cited_certificates,
    declared_sizes,
    main,
)
from sqpack.yamlio import safe_load


def evidence_by_id() -> dict[str, dict]:
    document = safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))
    return {record["id"]: record for record in document["evidence"]}


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
    with pytest.raises(Undeclared):
        declared_sizes(stub)


def test_an_out_of_range_size_does_not_crash(tmp_path: Path) -> None:
    """A size with no frontier record is a refusal; reading n-999.md would raise."""
    assert cited_certificates(999, {}) == set()


def test_a_reported_record_does_not_satisfy_the_sweep() -> None:
    """Citing a certificate is not claiming it.

    A `reported` evidence record carrying a path into a case package would satisfy the
    letter of the sweep while asserting nothing this repository checked.
    """
    real = {
        "E-fake": {
            "id": "E-fake",
            "assurance": "verified",
            "certificate": "cases/gobel40/packing.py",
        }
    }
    demoted = {"E-fake": {**real["E-fake"], "assurance": "reported"}}

    # n = 40 reaches E-fake through neither map; use the real record set instead and
    # check the filter directly on the shape the sweep consumes.
    from devtools.check_certificate_citations import cited_certificates as sweep

    evidence = evidence_by_id()
    assert any(path.startswith("cases/gobel40/") for path in sweep(40, evidence))

    downgraded = {
        k: ({**v, "assurance": "reported"} if k == "E-n040-gobel-upper" else v)
        for k, v in evidence.items()
    }
    assert not any(path.startswith("cases/gobel40/") for path in sweep(40, downgraded)), (
        "a reported record must not satisfy the sweep"
    )
