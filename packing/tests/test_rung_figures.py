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

import pytest

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


def _evidence(evidence_id: str) -> dict:
    document = safe_load(EVIDENCE.read_text(encoding="utf-8"))
    return next(e for e in document["evidence"] if e["id"] == evidence_id)


def test_the_check_passes_on_the_retained_tree() -> None:
    assert main() == 0


def test_the_reach_table_distinguishes_reports_from_retained_measurements() -> None:
    reach = RESULTS.parent / "CERTIFICATE-REACH.md"
    text = reach.read_text(encoding="utf-8")
    expected_rows = (
        "| 3.82 | 11.0000 | result narrative; no raw run |",
        "| 3.95 | 11.9706 | frozen 969-atom certificate; feasible mass, not a proved optimum |",
        (
            "| 3.96 | 11.9936 | reported objective has no raw run; frozen 2,097-atom "
            "certificate has feasible mass 11.998960 |"
        ),
        "| 4.58 | 16.9628 | no raw run; frozen candidate mass 16.965735 |",
        "| 4.59 | 16.9303 | no raw run; frozen candidate mass 16.933080 |",
        "| 4.68 | 18.0000 | three site sets reported; no raw run |",
        (
            "| 4.80 | 18.916941 | no raw run; frozen 2,260-atom certificate has "
            "feasible mass 18.922620 |"
        ),
    )
    assert all(row in text for row in expected_rows)
    assert "The frozen artifacts at 3.95 and 4.80 recompute feasible masses" in text
    assert "frozen candidates corroborate scale with" in text


def test_t019_case_pages_bind_the_current_direct_certificate() -> None:
    expected_evidence = {
        "E-n017-fractional-certificate",
        "E-fractional-interval-decision",
    }
    frontier = RESULTS.parent
    for n in (17, 18):
        text = (frontier / f"n-{n:03d}.md").read_text(encoding="utf-8")
        _, frontmatter, body = text.split("---", 2)
        packing = safe_load(frontmatter)["packing"]
        bound = packing["verified_lower_bound"]
        assert str(bound["exact_form"]) == "459/100"
        assert set(bound["evidence"]) == expected_evidence
        assert "459/100 = 4.59" in body
        if n > 17:
            assert "direct" in body

    t020_evidence = {
        "E-n020-fractional-certificate",
        "E-fractional-interval-decision",
    }
    for n in (19, 20, 21):
        text = (frontier / f"n-{n:03d}.md").read_text(encoding="utf-8")
        _, frontmatter, body = text.split("---", 2)
        bound = safe_load(frontmatter)["packing"]["verified_lower_bound"]
        assert str(bound["exact_form"]) == "24/5"
        assert set(bound["evidence"]) == t020_evidence
        assert "24/5 = 4.8" in body


def test_t017_current_rung_is_bound_to_its_record_and_explanations() -> None:
    """D-470: advancing the pointer must advance every claim about that pointer.

    The retained n = 12 certificate moved from 79/20 to 99/25 while its result headline,
    evidence figures, case body, and replay orientation remained on older rungs. Numeric
    certificate checks cannot detect prose that truthfully describes the wrong artifact,
    so this narrow cross-record contract pins the live pointer and the surfaces that tell
    a reader what it means.
    """
    repo = RESULTS.parents[2]
    case_dir = repo / "packing/cases/n12_fractional_certificate"
    certificate = json.loads((case_dir / "certificate.json").read_text(encoding="utf-8"))
    assert certificate["claim"] == "s(12) >= 99/25"
    assert certificate["outer_side"] == "99/25"
    assert certificate["total_mass"] == "149987/12500"
    assert certificate["least_cell_mass"] == "12501/12500"
    assert len(certificate["atoms"]) == 2097

    result = _result("T-017")
    assert "s(12) >= 99/25" in result["claim"]
    assert set(result["evidence"]) == {
        "E-n012-fractional-certificate",
        "E-fractional-interval-decision",
    }
    assert "eight-rung ladder" in result["significance"]["rationale"]
    assert "149987/12500 = 11.998960" in result["next_rung"]
    assert "about 6.9 times tighter" in result["next_rung"]
    assert "about 1.77 times the 1184-atom n = 17 certificate" in result["next_rung"]

    primary = _evidence("E-n012-fractional-certificate")
    assert primary["certificate"] == "cases/n12_fractional_certificate/certificate.json"
    assert "2,097-atom" in primary["limitations"]
    assert "12501/12500" in primary["limitations"]
    historical = _evidence("E-n012-independent-verifier")
    assert historical["certificate"].endswith("certificate-77-20.json")
    assert "does not decide the current 99/25 bytes" in historical["limitations"]

    case_text = (repo / "packing/frontier/n-012.md").read_text(encoding="utf-8")
    readme = (repo / "README.md").read_text(encoding="utf-8")
    replay = (case_dir / "replay.py").read_text(encoding="utf-8")
    assert "verified lower bound is `99/25 = 3.96`" in case_text
    assert "2,097 weighted atoms" in case_text
    assert "T-017: `s(12) ≥ 99/25`" in readme
    assert "Eight rungs are retained" in replay

    agenda = (
        repo
        / "packing/campaign/agendas/agenda-019-efficiency-first-retarget-and-deep-strategy.md"
    ).read_text(encoding="utf-8")
    assert "2097 atoms took 4866 s" in agenda
    assert "raw timing transcript" in agenda
    assert "2097 atoms took about 13000 s" not in agenda


def test_retained_figure_anchor_beats_a_later_comparison_rung() -> None:
    """A historical comparison later in one sentence must not retarget the top-rung figures."""
    corrupted = copy.deepcopy(_result("T-017"))
    corrupted["next_rung"] = (
        "The retained certificate's total is 11.000000, leaving 1.000000 below twelve "
        "-- compared with margin 0.007175 at 197/50."
    )

    problems, _ = check_result(corrupted)
    assert len(problems) == 2
    assert all("certificate.json" in problem for problem in problems)
    assert all("certificate-197-50.json" not in problem for problem in problems)


def test_two_in_scope_rungs_without_an_anchor_are_left_ambiguous() -> None:
    """A figure beside two of the result's own rungs must not be guessed onto either."""
    ambiguous = copy.deepcopy(_result("T-017"))
    ambiguous["next_rung"] = "The total is 1.000000 between the 197/50 and 79/20 rungs."

    problems, _ = check_result(ambiguous)
    assert problems == []


def test_t018_literature_receipt_is_folded_into_canonical_surfaces() -> None:
    """The novelty audit must live in the source and frontier tiers, not only a review."""
    repo = RESULTS.parents[2]
    receipt = "packing/resources/web/s11-lower-bound-literature-audit-2026/README.md"
    assert (repo / receipt).is_file()
    assert receipt in _result("T-018")["artifacts"]
    assert (
        receipt.removeprefix("packing/")
        in _evidence("E-n011-fractional-certificate")["novelty_basis"]["corpus"]
    )

    case_text = (repo / "packing/frontier/n-011.md").read_text(encoding="utf-8")
    _, frontmatter, _ = case_text.split("---", 2)
    packing = safe_load(frontmatter)["packing"]
    locals_ = {resource.get("local") for resource in packing["resources"]}
    assert "web/s11-lower-bound-literature-audit-2026/README.md" in locals_
    assert str(packing["source_reviewed"]) == "2026-09-04"

    survey = (
        repo / "docs/project/research/research-2026-08-22-packing-11-unit-squares.md"
    ).read_text(encoding="utf-8")
    assert "2026-09-04: the lower bound moved to `381/100`" in survey
    assert "s11-lower-bound-literature-audit-2026" in survey

    resources = (repo / "packing/resources/README.md").read_text(encoding="utf-8")
    assert "[Göbel 1979]" in resources
    assert "gobel-1979-geometrical-packing-and-covering-problems` is **PDF-only**" in resources
    assert "Every paper is stored three ways" not in resources
    assert "first *exact algebraic* solution" not in survey
    assert "first exact algebraic solution" not in survey

    repaired = _result("T-010")["significance"]["rationale"]
    assert "Stromquist's 1984 Memo III" in repaired
    assert "lower bound was stated in 1979" not in repaired

    strategies = safe_load(
        (repo / "packing/frontier/proof-strategies.yaml").read_text(encoding="utf-8")
    )["strategies"]
    by_id = {strategy["id"]: strategy for strategy in strategies}
    assert "Göbel 1979" in by_id[2]["refs"]
    assert "Kearney\u2013Shiu 2002" in by_id[5]["refs"]
    assert "Nagamochi 2005" in by_id[8]["refs"]
    assert "T-017 through T-020" in by_id[22]["note"]
    assert "n = 11" in by_id[22]["note"]


def test_recovered_trump_note_is_not_described_as_missing() -> None:
    """D-472: recovery of a source must retire the old acquisition disclaimer."""
    repo = RESULTS.parents[2]
    assert (repo / "packing/resources/papers/trump-2023-packing-11-unit-squares.pdf").is_file()
    tutorial = (repo / "TUTORIAL.md").read_text(encoding="utf-8")
    evidence = EVIDENCE.read_text(encoding="utf-8")
    assert "His 2023 author writeup is now retained" in tutorial
    assert "2023 writeup was not retrievable" not in tutorial
    assert "Trump's personal site is not retained" not in evidence


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
    assert "margin below 17 0.406" in joined
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

    `T-017`'s own claim restates its one rung (`99/25 = 3.96`) twice, once for its own
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


def test_certificate_exposes_target_margin_and_explicit_reach_margin() -> None:
    """T-020 is stored at n=20 but also reaches n=19, and both margins are meaningful."""
    figures = CertificateFigures(
        path="cases/n20_fractional_certificate/certificate.json",
        n=20,
        outer_side=Fraction(24, 5),
        atom_count=2260,
        mass=Fraction(946131, 50000),
        stored_mass=Fraction(946131, 50000),
    )
    assert figures.margin == Fraction(53869, 50000)
    assert figures.margin_below(19) == Fraction(3869, 50000)


@pytest.mark.parametrize(
    ("stated", "target"),
    (("0.077380", "nineteen"), ("1.077380", "twenty"), ("0.077380", "19")),
)
def test_qualified_reach_and_target_margins_are_checked_against_the_named_integer(
    stated: str, target: str
) -> None:
    probe = copy.deepcopy(_result("T-020"))
    probe["claim"] = ""
    probe["significance"]["rationale"] = ""
    probe["composition"] = ""
    probe["next_rung"] = (
        f"The retained certificate's total is 18.922620, leaving {stated} below {target}."
    )

    problems, _ = check_result(probe)
    assert problems == []


@pytest.mark.parametrize(
    ("stated", "target"), (("0.077380", "twenty"), ("1.077380", "nineteen"))
)
def test_swapping_reach_and_target_margins_is_refused(stated: str, target: str) -> None:
    probe = copy.deepcopy(_result("T-020"))
    probe["claim"] = ""
    probe["significance"]["rationale"] = ""
    probe["composition"] = ""
    probe["next_rung"] = f"The retained certificate is leaving {stated} below {target}."

    problems, _ = check_result(probe)
    assert len(problems) == 1
    assert f"margin below {20 if target == 'twenty' else 19} {stated}" in problems[0]


@pytest.mark.parametrize(("stated", "problem_count"), (("1.077380", 0), ("0.077380", 1)))
def test_unqualified_margin_still_uses_the_certificates_recorded_target(
    stated: str, problem_count: int
) -> None:
    """A reach margin is valid only when prose names its lower integer explicitly."""
    probe = copy.deepcopy(_result("T-020"))
    probe["claim"] = ""
    probe["significance"]["rationale"] = ""
    probe["composition"] = ""
    probe["next_rung"] = f"The retained certificate's margin is {stated}."

    problems, _ = check_result(probe)
    assert len(problems) == problem_count
    if problems:
        assert f"prose says margin {stated}" in problems[0]
        assert "gives 1.077380" in problems[0]


@pytest.mark.parametrize(
    ("stated", "target", "problem_count"),
    (("0.077380", "nineteen", 0), ("0.077380", "twenty", 1)),
)
def test_named_margin_at_an_explicit_side_uses_the_named_integer(
    stated: str, target: str, problem_count: int
) -> None:
    probe = copy.deepcopy(_result("T-020"))
    probe["claim"] = ""
    probe["significance"]["rationale"] = ""
    probe["composition"] = ""
    probe["next_rung"] = f"The margin below {target} at 24/5 is already {stated}."

    problems, _ = check_result(probe)
    assert len(problems) == problem_count
    if problems:
        assert f"margin below 20 {stated}" in problems[0]


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

    # No file is literally named certificate.json: never reinterpret history as current.
    assert pick_retained([historical]) is None
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


def test_a_result_with_only_historical_rungs_is_refused() -> None:
    """Dropping the moving pointer must not retarget unqualified prose to old bytes."""
    probe = copy.deepcopy(_result("T-019"))
    probe["artifacts"] = [
        artifact
        for artifact in probe["artifacts"]
        if not artifact.endswith("/certificate.json")
    ]

    problems, checked = check_result(probe)
    assert checked == 2
    assert len(problems) == 1
    assert "only historical rungs" in problems[0]
    assert "exactly one moving certificate.json pointer is required" in problems[0]


def test_a_result_with_two_moving_pointers_is_refused() -> None:
    """A second live basename is ambiguous rather than silently winning by order."""
    probe = copy.deepcopy(_result("T-020"))
    probe["artifacts"].append("packing/cases/n17_fractional_certificate/certificate.json")

    problems, checked = check_result(probe)
    assert checked == 2
    assert len(problems) == 1
    assert "declare 2 moving certificate.json pointers" in problems[0]
    assert "exactly one is required" in problems[0]


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
