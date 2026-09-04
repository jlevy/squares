#!/usr/bin/env python3
"""Every mass, atom count, and margin a result's prose quotes must match its own certificate.

`D-439`: three durable-record statements described "the top rung" and were left behind
when the ladder advanced past them -- every figure exact and real, each simply about the
wrong file. No existing check re-derives a result's quoted figures from the artifact it
names, so nothing caught any of the three until a line-by-line read did.

These tests reconstruct D-439's two in-scope instances as in-memory perturbations of the
live `T-019` record -- never edits to `results.yaml` itself, which stays a live record
other work is in flight against. The third instance, a third-party package's byte-identity
claim checked by a printed SHA-256, is a claim about file identity rather than a quoted
mass, atom count, or margin; this module reads no file hash and has no test claiming
otherwise, which is the honest account of what it covers.
"""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

from devtools.check_rung_figures import (
    DEFECTS,
    EVIDENCE,
    RESULTS,
    CertificateFigures,
    certificate_consistency_problems,
    check_result,
    fraction_decimal_problems,
    load_certificate,
    main,
    movement_problems,
    pick_retained,
    resolve_certificates,
)
from sqpack.yamlio import safe_load


def _result(result_id: str) -> dict:
    document = safe_load(RESULTS.read_text(encoding="utf-8"))
    return next(r for r in document["results"] if r["id"] == result_id)


def test_the_check_passes_on_the_retained_tree() -> None:
    assert main() == 0


def test_the_reach_table_distinguishes_reports_from_retained_measurements() -> None:
    reach = RESULTS.parent / "CERTIFICATE-REACH.md"
    text = reach.read_text(encoding="utf-8")
    expected_rows = (
        "| 3.82 | 11.0000 | result narrative; no raw run |",
        "| 3.95 | 11.9706 | frozen 969-atom certificate; feasible mass, not a proved optimum |",
        "| 3.96 | 11.9936 | no raw run |",
        "| 4.58 | 16.9628 | no raw run; frozen candidate mass 16.965735 |",
        "| 4.59 | 16.9303 | no raw run; frozen candidate mass 16.933080 |",
        "| 4.68 | 18.0000 | three site sets reported; no raw run |",
    )
    assert all(row in text for row in expected_rows)
    assert "Only the displayed 3.95 value is recomputable from a tracked artifact" in text
    assert "the artifact proves a feasible mass rather than optimality" in text


def test_t019_case_pages_bind_the_current_direct_certificate() -> None:
    expected_evidence = {
        "E-n017-fractional-certificate",
        "E-fractional-interval-decision",
    }
    frontier = RESULTS.parent
    for n in (17, 18, 19):
        text = (frontier / f"n-{n:03d}.md").read_text(encoding="utf-8")
        _, frontmatter, body = text.split("---", 2)
        packing = safe_load(frontmatter)["packing"]
        bound = packing["verified_lower_bound"]
        assert str(bound["exact_form"]) == "459/100"
        assert set(bound["evidence"]) == expected_evidence
        assert "459/100 = 4.59" in body
        if n > 17:
            assert "direct" in body


def test_t019_control_has_no_disagreement() -> None:
    """The premise every perturbation below edits away from: today's record agrees."""
    problems, checked = check_result(_result("T-019"))
    assert problems == []
    assert checked == 3  # certificate.json (459/100) and the 229/50 and 451/100 rungs


def test_catches_d439_first_instance_the_movement_past_a_displaced_value() -> None:
    """D-439's first instance: the rationale gave the movement past Massaccesi as
    `0.0042` -- that is `451/100 - 22529/5000`, the *first* rung's own movement -- where
    the rung retained at the time (`229/50`) moved by `0.0742`. The live record now
    retains `459/100`, whose movement is `0.0842`, and states that; the reconstruction
    below perturbs whatever the record currently claims.
    """
    corrupted = copy.deepcopy(_result("T-019"))
    rationale = corrupted["significance"]["rationale"]
    assert "0.0842" in rationale, "premise: the live rationale states the retained movement"
    corrupted["significance"]["rationale"] = rationale.replace("0.0842", "0.0042")

    problems, _ = check_result(corrupted)
    assert len(problems) == 1
    assert "T-019 [significance.rationale]" in problems[0]
    assert "0.0042" in problems[0]
    assert "0.0842" in problems[0]


def test_catches_d439_second_instance_a_superseded_rungs_total_and_margin() -> None:
    """D-439's second instance: next_rung quoted the *first* rung's (`451/100`) total and
    margin -- `16.5936` and `0.406` -- as though they belonged to the retained
    certificate. The retained certificate is now `459/100`, total
    `423327/25000 = 16.933080` with margin `0.066920`; the reconstruction plants the
    superseded rung's figures over whatever the record currently states.
    """
    corrupted = copy.deepcopy(_result("T-019"))
    next_rung = corrupted["next_rung"]
    original = (
        "the retained certificate's total is 423327/25000 = 16.933080, "
        "leaving 0.066920 below seventeen"
    )
    assert original in next_rung, "premise: the live next_rung states the retained figures"
    corrupted["next_rung"] = next_rung.replace(
        original,
        "the retained certificate's total is 16.5936, leaving 0.406 below seventeen",
    )

    problems, _ = check_result(corrupted)
    assert len(problems) == 2
    joined = " | ".join(problems)
    assert "T-019 [next_rung]" in joined
    assert "total 16.5936" in joined
    assert "16.9331" in joined
    assert "margin 0.406" in joined
    assert "0.067 (exact" in joined  # 0.066920 rounded to the three places "0.406" states


def test_catches_a_bare_possessive_mass_after_the_top_rung_moves() -> None:
    corrupted = copy.deepcopy(_result("T-019"))
    current = "this certificate's 16.933080 reaching 17, 18 and 19 directly"
    assert current in corrupted["next_rung"]
    corrupted["next_rung"] = corrupted["next_rung"].replace(
        current,
        "this certificate's 16.965735 reaching 17, 18 and 19 directly",
    )
    problems, _ = check_result(corrupted)
    assert len(problems) == 1
    assert "prose says total 16.965735" in problems[0]
    assert "gives 16.933080" in problems[0]


def test_ignores_a_cross_referenced_rung_that_is_not_this_results_own() -> None:
    """T-019's own next_rung cites n = 12's ladder (`197/50`, `79/20`) for contrast;
    neither belongs to T-019's own artifacts, and a wrong-looking figure attached to one
    of them must not be compared against T-019's certificates -- a check that cries wolf
    on a cross-reference is worse than one that says nothing.
    """
    modified = copy.deepcopy(_result("T-019"))
    modified["next_rung"] += (
        " The 197/50 rung below this one has total 99.000000 and margin 99.000000."
    )
    problems, _ = check_result(modified)
    assert problems == []


def test_resolves_an_explicitly_named_secondary_rung() -> None:
    """A figure attached to `451/100` -- one of T-019's own three artifacts, not the
    retained one -- is checked against that certificate specifically."""
    t019 = _result("T-019")
    original = "The 451/100 rung two below this one has total 16.593620 and margin 0.406380"
    assert original in t019["next_rung"]
    modified = copy.deepcopy(t019)
    modified["next_rung"] = modified["next_rung"].replace(
        original,
        "The 451/100 rung below this one has total 1.000000 and margin 1.000000",
    )
    problems, _ = check_result(modified)
    assert len(problems) == 2
    assert all("certificate-451-100.json" in problem for problem in problems)


def test_repeating_the_same_rung_twice_does_not_trip_the_movement_gate() -> None:
    """The movement gate requires two *distinct* fraction-equals-decimal figures.

    `T-017`'s own claim restates its one rung (`79/20 = 3.95`) twice, once for its own
    container side and once compared against a published packing -- the same value, not
    a displaced prior one -- and must not be read as a movement claim just because a
    `movement is` phrase sits elsewhere in the same result.
    """
    fake = {
        "id": "T-000",
        "claim": (
            "at container side 3/2 = 1.5. Separately, 3/2 = 1.5 exceeds a published value."
        ),
        "significance": {
            "rationale": "The movement is +9.000000, which nothing here supports."
        },
        "next_rung": "",
        "composition": "",
        "artifacts": [],
    }
    assert movement_problems(fake) == []


def test_movement_check_accepts_either_subtraction_order() -> None:
    """The check does not assume which of a claim's two figures is written first."""
    reversed_order = {
        "id": "T-000",
        "claim": "at container side 22529/5000 = 4.5058, displacing 229/50 = 4.58.",
        "significance": {"rationale": "The movement is -0.0742 relative to the prior value."},
        "next_rung": "",
        "composition": "",
        "artifacts": [],
    }
    assert movement_problems(reversed_order) == []


def test_certificate_figures_are_recomputed_from_atoms_not_trusted_from_the_file() -> None:
    """The file's own stored `total_mass` is cross-checked, never substituted for the
    atom sum -- the whole point of a checker that re-derives from the rawest ground
    truth an artifact carries."""
    figures = CertificateFigures(
        path="synthetic",
        n=5,
        outer_side=Fraction(7, 2),
        atom_count=2,
        mass=Fraction(3, 2),
        stored_mass=Fraction(999, 100),
    )
    assert certificate_consistency_problems(figures) != []

    agreeing = copy.deepcopy(figures)
    object.__setattr__(agreeing, "stored_mass", Fraction(3, 2))
    assert certificate_consistency_problems(agreeing) == []


def test_a_non_certificate_artifact_is_silently_skipped(tmp_path: Path) -> None:
    """Most of a result's artifacts are generator or verifier modules, not certificates,
    and an unrelated JSON archive (an experiment record, say) must not be mistaken for
    one just because it happens to parse."""
    module = tmp_path / "colgen.py"
    module.write_text("x = 1\n")
    assert load_certificate(module) is None

    stray = tmp_path / "experiment.json"
    stray.write_text(json.dumps({"unrelated": "schema"}))
    assert load_certificate(stray) is None

    malformed = tmp_path / "malformed.json"
    malformed.write_text("{not valid json")
    assert load_certificate(malformed) is None

    assert load_certificate(tmp_path / "missing.json") is None


def test_retained_is_the_file_literally_named_certificate_json() -> None:
    """ "Retained" follows this repository's own naming convention (D-439's fix: the
    moving top-rung pointer is always `certificate.json`; a suffixed name is an
    immutable historical rung) rather than list position, so a result listing its
    artifacts out of order still resolves the right one as primary."""
    historical = CertificateFigures(
        path="cases/x/certificate-1-2.json",
        n=3,
        outer_side=Fraction(1, 2),
        atom_count=1,
        mass=Fraction(1, 2),
        stored_mass=None,
    )
    retained_figures = CertificateFigures(
        path="cases/x/certificate.json",
        n=3,
        outer_side=Fraction(7, 2),
        atom_count=1,
        mass=Fraction(3, 2),
        stored_mass=None,
    )

    # Historical rung listed first: retained must still win on its exact basename.
    assert pick_retained([historical, retained_figures]) is retained_figures
    assert pick_retained([retained_figures, historical]) is retained_figures

    # No file is literally named certificate.json: fall back to the first resolved.
    assert pick_retained([historical]) is historical
    assert pick_retained([]) is None


def test_resolve_certificates_reads_real_repository_relative_artifacts() -> None:
    """The path-resolution half of certificate lookup, exercised against a real result:
    `resolve_certificates` reads exactly the artifacts a result names, repository-relative,
    and nothing outside the repository."""
    retained, sides, resolved = resolve_certificates(_result("T-019"))
    assert retained is not None
    assert retained.path == "packing/cases/n17_fractional_certificate/certificate.json"
    assert Fraction(451, 100) in sides
    assert len(resolved) == 3


def test_repo_wide_fraction_equals_decimal_catches_wrong_arithmetic() -> None:
    """The mechanical check is generic text scanning, not tied to results.yaml's schema:
    any `a/b = d.ddd` anywhere must be true to the precision written."""
    problems = fraction_decimal_problems("the total is 1/4 = 0.30", "synthetic")
    assert len(problems) == 1
    assert "1/4 = 0.30 is wrong" in problems[0]
    assert fraction_decimal_problems("the total is 1/4 = 0.25", "synthetic") == []


def test_the_repo_wide_scan_covers_evidence_and_defects_too() -> None:
    """This is repository-wide value, not just for results: the same pattern recurs in
    `evidence.yaml` and `defects.yaml` (D-439's own fix restates the corrected total in
    the latter), and the mechanical check applies there identically."""
    for path, label in ((EVIDENCE, "evidence.yaml"), (DEFECTS, "defects.yaml")):
        assert fraction_decimal_problems(path.read_text(encoding="utf-8"), label) == []
