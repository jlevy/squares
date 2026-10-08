"""The results register's rungs are earned: the derivation and its refusals.

`epistemics.md` owns the vocabulary; `devtools/check_results.py` is its
executable form. These tests pin the derivation ladder on synthetic atoms, the
live register's health, and the refusal directions a control also exercises:
a rung claimed past its atoms, and an understatement with no composition note.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from devtools import (
    backfill_result_registration,
    check_results,
    render_results,
    result_status,
)
from devtools.check_results import (
    derive_confirmation,
    derive_verification,
    repository_file_problem,
    verification_relation,
)
from devtools.result_credit import credit_line
from sqpack.yamlio import safe_load

MACHINE_ENTRY = {
    "method": "exact-algebraic",
    "certificate": "somewhere.py",
    "replay": "uv run --frozen python -m somewhere",
    "replay_status": "passed",
    "origin": "audited-here",
}


def test_the_live_register_is_healthy() -> None:
    assert check_results.main() == 0


def test_a_dated_records_own_title_is_not_held_to_the_register(tmp_path: Path) -> None:
    """A review keeps the provisional id it was written with, and the synopsis quotes it.

    T-101 was registered as the provisional T-118, and its two reviews, stored as their
    reviewers wrote them, still name T-118 in their titles, which the synopsis's document
    map quotes. Only those quoted titles leave the reader-tier mention check; the same id
    anywhere else on the page is still refused.
    """
    document_map = safe_load(check_results.DOCUMENT_MAP.read_text(encoding="utf-8"))
    links = check_results.record_links(document_map)
    review = "docs/project/reviews/review-2026-10-06-evand-exact-ceilings.md"
    (quoted,) = [link for link in links if link.endswith(f"({review})")]
    assert "T-118" in quoted
    maintained = [
        entry["path"] for entry in document_map["documents"] if entry["authority"] != "record"
    ]
    assert maintained
    assert not any(link.endswith(f"({path})") for link in links for path in maintained)
    page = tmp_path / "page.md"
    page.write_text(f"| {quoted} | review |\n\nT-118 is named here too.\n", encoding="utf-8")
    remaining = check_results.reader_tier_text(page, links)
    assert quoted not in remaining
    assert re.findall(r"\bT-\d{3}\b", remaining) == ["T-118"]


def test_the_uniqueness_reviews_title_keeps_its_provisional_id() -> None:
    """T-112 was registered as the provisional T-102 and renumbered when it merged with
    main, whose T-102 is wand125's bound at n = 18. Its adversarial review, stored as its
    reviewer wrote it, names T-102 in its title, and the synopsis quotes that title; the
    register's note on T-112 says which result the review's "T-102" is (think-d1bd)."""
    review = "docs/project/reviews/review-2026-10-06-n11-uniqueness-adversarial.md"
    title = (check_results.REPO / review).read_text(encoding="utf-8").splitlines()[0]
    assert title.endswith("(T-102)")
    record, _, _ = _live_record("T-112")
    notes = " ".join(record["notes"].split())
    assert 'its "T-102" is this entry' in notes
    assert any(item["path"] == review for item in record["reviews"])


def test_the_check2_reviews_title_keeps_the_provisional_range() -> None:
    """T-102 to T-111 were registered as the provisional T-108 to T-117, and the review of
    the ten, stored as its reviewer wrote it, names that range in its title. The synopsis
    quotes the title, and the quoted link is left out of the mention check, so the
    provisional T-113 to T-117, ids the register does not hold, are not refused there;
    T-112, which the register now holds, is the uniqueness of the eleven-square optimum
    and not the review's provisional id for T-106."""
    document_map = safe_load(check_results.DOCUMENT_MAP.read_text(encoding="utf-8"))
    links = check_results.record_links(document_map)
    review = "docs/project/reviews/review-2026-10-06-wand125-check2-ten-certificates.md"
    (quoted,) = [link for link in links if link.endswith(f"({review})")]
    assert "(T-108 to T-117)" in quoted
    synopsis = check_results.REPO / "SYNOPSIS.md"
    assert quoted in synopsis.read_text(encoding="utf-8")
    assert quoted not in check_results.reader_tier_text(synopsis, links)


def test_confirmation_ladder_on_synthetic_atoms() -> None:
    assert derive_confirmation([]) == "C0"
    read_only = {
        "external_review": {
            "state": "informally-verified",
            "date": "2026-08-31",
            "reviewed_by": "reviewer",
            "note": "Read the argument; did not rederive its case split.",
        },
        "origin": "external",
    }
    assert derive_confirmation([read_only]) == "C1"
    assert derive_confirmation([{**read_only, "origin": "independently-external"}]) == "C1"
    assert derive_confirmation([{**read_only, "origin": "replayed-here"}]) == "C0"
    assert (
        derive_confirmation(
            [{**read_only, "external_review": {"state": "informally-verified"}}]
        )
        == "C0"
    )
    replayed = {
        "origin": "replayed-here",
        "replay": "uv run replay",
        "replay_status": "passed",
        "method": "numerical-f64",
    }
    assert derive_confirmation([replayed]) == "C2"
    assert derive_confirmation([{**replayed, "replay": None}]) == "C0"
    assert derive_confirmation([dict(MACHINE_ENTRY)]) == "C3"
    # Distinct methods are an attribute, not a rung: two machine proofs of one method
    # or of two methods both derive C3 without the rung-4 review record.
    assert derive_confirmation([dict(MACHINE_ENTRY), dict(MACHINE_ENTRY)]) == "C3"
    interval = dict(MACHINE_ENTRY, method="interval-certified")
    assert derive_confirmation([dict(MACHINE_ENTRY), interval]) == "C3"
    assert check_results.distinct_methods([dict(MACHINE_ENTRY), interval]) == 2
    # A third party's own replay, retained here, confirms like ours.
    third_party = dict(MACHINE_ENTRY, origin="independently-external")
    assert derive_confirmation([third_party]) == "C3"
    assert check_results.third_party_replayed([third_party])
    # The world's machine proof raises V, never C.
    external_machine = dict(MACHINE_ENTRY, origin="external")
    assert derive_confirmation([external_machine]) == "C0"
    # A review record alone changes nothing without machine evidence.
    assert derive_confirmation([replayed], RUNG_4_REVIEWS) == "C2"


#: The review record rung 4 needs: two adversarial AI reviews by distinct reviewers, the
#: latest accepting, and a human oversight record with the three checks.
RUNG_4_REVIEWS: list[dict[str, object]] = [
    {
        "path": "a.md",
        "kind": "adversarial",
        "reviewer": "Model A at max reasoning",
        "reviewer_kind": "ai",
        "date": "2026-09-01",
        "verdict": "defects-resolved",
    },
    {
        "path": "b.md",
        "kind": "adversarial",
        "reviewer": "Model B, independent lane",
        "reviewer_kind": "ai",
        "date": "2026-09-02",
        "verdict": "accepted",
    },
    {
        "path": "c.md",
        "kind": "oversight",
        "reviewer": "A. Person",
        "reviewer_kind": "human",
        "relation": "owner",
        "date": "2026-09-03",
        "verdict": "accepted",
        "checked": ["trust-boundary", "certificate-meaning", "ai-findings"],
    },
]

FORMAL_ENTRY: dict[str, object] = {
    **MACHINE_ENTRY,
    "method": "proof-assistant-checked",
    "origin": "replayed-here",
    "axioms_receipt": "axioms.log",
}


def _expert(name: str, **changes: object) -> dict[str, object]:
    return {
        "path": f"{name}.md",
        "kind": "formalization",
        "reviewer": name,
        "reviewer_kind": "human",
        "relation": "external",
        "date": "2026-09-04",
        "verdict": "accepted",
        "checked": ["statement-fidelity", "definitions", "axioms", "build"],
        "independent_of_author": True,
        **changes,
    }


def test_rung_4_needs_two_distinct_adversarial_reviews_and_human_oversight() -> None:
    machine = [dict(MACHINE_ENTRY)]
    assert derive_confirmation(machine, RUNG_4_REVIEWS) == "C4"
    assert derive_verification(machine, RUNG_4_REVIEWS) == "V4"
    # One reviewer twice is one reviewer.
    same = [dict(RUNG_4_REVIEWS[0]), dict(RUNG_4_REVIEWS[0], path="d.md"), RUNG_4_REVIEWS[2]]
    assert derive_confirmation(machine, same) == "C3"
    # No human oversight, no rung 4; an AI "oversight" record is not oversight.
    ai_only = RUNG_4_REVIEWS[:2]
    assert derive_confirmation(machine, ai_only) == "C3"
    ai_oversight = [*ai_only, dict(RUNG_4_REVIEWS[2], reviewer_kind="ai")]
    assert derive_verification(machine, ai_oversight) == "V3"
    # Oversight that did not check the AI findings is not the record.
    partial = [*ai_only, dict(RUNG_4_REVIEWS[2], checked=["trust-boundary"])]
    assert derive_confirmation(machine, partial) == "C3"
    # An open defect in the latest review holds the rung at 3.
    open_defect = [
        *RUNG_4_REVIEWS,
        dict(RUNG_4_REVIEWS[1], path="e.md", date="2026-09-09", verdict="defect-open"),
    ]
    assert derive_confirmation(machine, open_defect) == "C3"
    # The source's own reviews count toward V and not toward C.
    source_side = [dict(review, relation="source") for review in RUNG_4_REVIEWS]
    assert derive_verification(machine, source_side) == "V4"
    assert derive_confirmation(machine, source_side) == "C3"


def test_rung_5_needs_formal_evidence_experts_and_openness() -> None:
    experts = [_expert("Expert One"), _expert("Expert Two")]
    assert derive_verification([FORMAL_ENTRY], experts[:1]) == "V5"
    assert derive_confirmation([FORMAL_ENTRY], experts, open_review=True) == "C5"
    # A kernel check without its axiom receipt, or without the expert review, is rung 3.
    assert derive_verification([dict(FORMAL_ENTRY, axioms_receipt=None)], experts) == "V3"
    assert derive_verification([FORMAL_ENTRY]) == "V3"
    assert derive_verification([{"method": "proof-assistant-checked"}]) == "V0"
    # C5 needs two distinct experts, the rebuild here and the open pointer.
    assert derive_confirmation([FORMAL_ENTRY], experts[:1], open_review=True) == "C3"
    assert derive_confirmation([FORMAL_ENTRY], experts, open_review=False) == "C3"
    assert (
        derive_confirmation(
            [dict(FORMAL_ENTRY, origin="audited-here")], experts, open_review=True
        )
        == "C3"
    )
    assert (
        derive_confirmation(
            [FORMAL_ENTRY], [experts[0], _expert("Expert One", path="x.md")], open_review=True
        )
        == "C3"
    )
    # The author reading their own formalization is not a review.
    author = [_expert("Expert One"), _expert("The Author", independent_of_author=False)]
    assert derive_confirmation([FORMAL_ENTRY], author, open_review=True) == "C3"
    assert derive_verification([FORMAL_ENTRY], author[1:]) == "V3"


def test_verification_ladder_on_synthetic_atoms() -> None:
    assert derive_verification([]) == "V0"
    numeric = {"method": "numerical-f64", "precision": {"rounding": "nearest"}}
    assert derive_verification([numeric]) == "V1"
    published = {"method": "published-proof", "proof": {"theorem": "T"}}
    assert derive_verification([published]) == "V3"
    audited = {"method": "proof-audited", "proof": {"theorem": "T"}}
    assert derive_verification([audited]) == "V3"
    # A machine certificate of any origin is checkable, V3, until the review record.
    assert derive_verification([dict(MACHINE_ENTRY, origin="external")]) == "V3"
    assert derive_verification([dict(MACHINE_ENTRY, origin="external")], RUNG_4_REVIEWS) == "V4"


def test_v2_bridges_only_an_unavailable_proof() -> None:
    assert verification_relation("V2", "V0") == "supported"
    assert verification_relation("V2", "V1") == "supported"
    assert verification_relation("V2", "V3") == "understated"
    assert verification_relation("V2", "V4") == "understated"


def test_result_paths_must_name_repository_files() -> None:
    assert repository_file_problem("epistemics.md") is None
    assert repository_file_problem("packing") == "does not name a file"
    assert repository_file_problem("/etc/passwd") == (
        "must be a normalized repository-relative path"
    )
    assert repository_file_problem("../outside") == (
        "must be a normalized repository-relative path"
    )


def test_a_reversed_scope_range_is_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    poisoned = _changed_result(tmp_path, "T-007", scope={"n_min": 100, "n_max": 4})
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert "T-007: scope range is reversed: 100 > 4" in capsys.readouterr().out


def test_results_renderer_escapes_a_pipe_in_a_claim(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    register = _poisoned_register(
        tmp_path,
        "      Sixteen points make [0, 4426213/1000000]^2 unavoidable",
        "      Sixteen points | make [0, 4426213/1000000]^2 unavoidable",
    )
    monkeypatch.setattr(render_results, "RESULTS", register)
    row = next(
        line for line in render_results.render().splitlines() if line.startswith("| T-001 ")
    )
    assert r"Sixteen points \| make" in row
    # Ten cells: id, n, kind, credit, V, C, S, status, novelty, claim.
    assert len(re.findall(r"(?<!\\)\|", row)) == 11


def _poisoned_register(tmp_path: Path, old: str, new: str) -> Path:
    text = check_results.RESULTS.read_text(encoding="utf-8")
    assert text.count(old) == 1
    target = tmp_path / "results.yaml"
    target.write_text(text.replace(old, new), encoding="utf-8")
    return target


def _changed_result(tmp_path: Path, result_id: str, **changes: object) -> Path:
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    record = next(result for result in register["results"] if result["id"] == result_id)
    record.update(changes)
    target = tmp_path / "results.yaml"
    target.write_text(
        yaml.safe_dump(register, sort_keys=False, allow_unicode=True, width=96),
        encoding="utf-8",
    )
    return target


#: A mapped, non-superseded review the live document map holds.
MAPPED_REVIEW = (
    "docs/project/reviews/review-2026-08-31-overnight-run-verification-determinations.md"
)


def _live_reviews(**changes: object) -> list[dict[str, object]]:
    """Rung 4's record on paths the live document map holds, with `changes` applied to
    the oversight record."""
    reviews: list[dict[str, object]] = [
        dict(review, path=MAPPED_REVIEW) for review in RUNG_4_REVIEWS
    ]
    reviews[1]["path"] = "docs/project/reviews/review-2026-09-04-pr78-s11-adversarial.md"
    reviews[2].update(changes)
    return reviews


def test_rung_4_is_earned_by_mapped_review_records(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    promoted = _changed_result(
        tmp_path, "T-004", verification="V4", confirmation="C4", reviews=_live_reviews()
    )
    monkeypatch.setattr(check_results, "RESULTS", promoted)
    assert check_results.main() == 0


def test_a_review_that_is_not_a_mapped_review_earns_nothing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    promoted = _changed_result(
        tmp_path,
        "T-004",
        verification="V4",
        confirmation="C4",
        reviews=_live_reviews(path="epistemics.md"),
    )
    monkeypatch.setattr(check_results, "RESULTS", promoted)
    assert check_results.main() == 1
    out = capsys.readouterr().out
    assert "not a non-superseded review" in out
    assert "declares C4 but the cited atoms support only C3" in out


def test_a_human_review_without_a_relation_is_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    reviews = _live_reviews()
    del reviews[2]["relation"]
    promoted = _changed_result(tmp_path, "T-004", reviews=reviews)
    monkeypatch.setattr(check_results, "RESULTS", promoted)
    assert check_results.main() == 1
    assert "states no relation to the project" in capsys.readouterr().out


def test_a_review_covering_other_results_is_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    promoted = _changed_result(tmp_path, "T-004", reviews=_live_reviews(covers=["T-005"]))
    monkeypatch.setattr(check_results, "RESULTS", promoted)
    assert check_results.main() == 1
    assert "covers ['T-005'], not this result" in capsys.readouterr().out


def test_a_confirmation_above_the_verification_is_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    promoted = _changed_result(tmp_path, "T-046", confirmation="C2")
    monkeypatch.setattr(check_results, "RESULTS", promoted)
    assert check_results.main() == 1
    assert "confirmation C2 exceeds verification V0" in capsys.readouterr().out


def test_an_inflated_rung_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    poisoned = _poisoned_register(
        tmp_path,
        "    verification: V3\n    confirmation: C3\n    significance:\n"
        "      score: 3\n      rationale: >-\n        A published exact value",
        "    verification: V3\n    confirmation: C5\n    significance:\n"
        "      score: 3\n      rationale: >-\n        A published exact value",
    )
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert "T-006: declares C5" in capsys.readouterr().out


def test_an_unexplained_understatement_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # T-004 sits at its derived C3; dropping it to C2 with no composition note
    # must fail in the sandbagging direction.
    poisoned = _poisoned_register(
        tmp_path,
        "    verification: V3\n    confirmation: C3\n    significance:\n"
        "      score: 3\n      rationale: >-\n"
        "        As far as the archived corpus shows, the first machine verification of",
        "    verification: V3\n    confirmation: C2\n    significance:\n"
        "      score: 3\n      rationale: >-\n"
        "        As far as the archived corpus shows, the first machine verification of",
    )
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert "T-004: understates C3 as C2" in capsys.readouterr().out


def test_v0_cannot_hide_machine_verification_behind_notes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    poisoned = _changed_result(
        tmp_path,
        "T-004",
        verification="V0",
        notes="Deliberately poisoned declaration for the regression.",
    )
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert "T-004: understates V3 as V0" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("kind", "value"),
    [
        ("hypothesis", "H-999"),
        ("agenda_cell", "BC-999"),
        ("session", "session-999"),
        ("experiment", "exp-999"),
    ],
)
def test_a_dangling_produced_by_id_is_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    kind: str,
    value: str,
) -> None:
    """The join from a result back to the campaign is a reference, so it can dangle.

    Before `produced_by` existed the join ran through prose -- a `by:` line, cell ids
    in `next_rung` -- and nothing could resolve it. A field that resolves to nothing
    would be the same prose with a colon in front of it.
    """
    poisoned = _changed_result(tmp_path, "T-017", produced_by={kind: value})
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert f"T-017: produced_by.{kind} names {value}, which is not a recorded" in (
        capsys.readouterr().out
    )


def test_produced_by_resolves_every_kind_of_campaign_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    known = check_results.campaign_ids()
    assert {"H-060", "H-061"} <= known["hypothesis"]
    assert {"BC-150", "BC-152", "BC-161"} <= known["agenda_cell"]
    assert {"session-083", "session-085"} <= known["session"]
    assert {"exp-058", "exp-059"} <= known["experiment"]
    linked = _changed_result(
        tmp_path,
        "T-017",
        produced_by={
            "hypothesis": "H-061",
            "agenda_cell": "BC-161",
            "session": "session-085",
            "experiment": "exp-058",
        },
    )
    monkeypatch.setattr(check_results, "RESULTS", linked)
    assert check_results.main() == 0


def test_a_previously_published_result_names_its_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A result by others without its source would be credit restated nowhere."""
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    record = next(result for result in register["results"] if result["id"] == "T-032")
    record.pop("attribution")
    target = tmp_path / "results.yaml"
    target.write_text(yaml.safe_dump(register, sort_keys=False, allow_unicode=True))
    monkeypatch.setattr(check_results, "RESULTS", target)
    assert check_results.main() == 1
    assert "T-032: a previously-published result names its source in attribution" in (
        capsys.readouterr().out
    )


def test_a_novel_result_is_this_projects_and_names_no_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    claimed = _changed_result(
        tmp_path,
        "T-017",
        attribution={"source_keys": ["[evand square-packing 2026]"], "published": "2026-08-25"},
    )
    monkeypatch.setattr(check_results, "RESULTS", claimed)
    assert check_results.main() == 1
    assert "T-017: an apparently-novel result is this project's" in capsys.readouterr().out


def test_an_attribution_key_resolves_in_the_bibliography(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    dangling = _changed_result(
        tmp_path,
        "T-032",
        attribution={"source_keys": ["[nobody 2026]"], "published": "2026-09-20"},
    )
    monkeypatch.setattr(check_results, "RESULTS", dangling)
    assert check_results.main() == 1
    assert "T-032: attribution names [nobody 2026], which bibliography.yaml lacks" in (
        capsys.readouterr().out
    )


def test_a_recent_result_by_others_needs_its_sources_lineage() -> None:
    record = {
        "id": "T-999",
        "novelty": "previously-published",
        "attribution": {"source_keys": ["[a]", "[b]"], "published": "2026-09-01"},
    }
    sources = {"[a]": {"lineage": "independent"}, "[b]": {}}
    assert check_results.attribution_problems(record, sources) == [
        "T-999: [b] has no lineage, which a result by others published since 2026-08-22 needs"
    ]
    record["attribution"]["published"] = "2026-08-21"
    assert check_results.attribution_problems(record, sources) == []


#: The source this project's weighted certificates build on, its dash written as an
#: escape for the reason `tests/test_generated_table_typography.py` gives.
WEIGHTED = "[Burns\u2013Massaccesi n17]"
SOURCES = {
    WEIGHTED: {"authors": ["Massaccesi", "Burns"]},
    "[Stromquist 2003]": {"authors": ["Stromquist"]},
    "[K]": {"authors": ["Kleddamag"], "credit": "Kleddamag after Levy, Guzhou0806, Mira"},
}


def test_every_credit_names_people_and_this_projects_is_levy() -> None:
    """One form for every result: `X`, or `X after Y`. This project's results are Levy's
    by name, and the `after` is the entry's own `builds_on`, in the order it lists."""
    own: dict[str, object] = {"id": "T-999", "novelty": "apparently-novel"}
    assert credit_line(own, SOURCES) == "Levy"
    own["builds_on"] = {"credit": ["Burns", "Massaccesi"], "source_keys": [WEIGHTED]}
    assert credit_line(own, SOURCES) == "Levy after Burns, Massaccesi"
    theirs = {"id": "T-998", "attribution": {"source_keys": ["[K]"], "published": "2026-09-22"}}
    assert credit_line(theirs, SOURCES) == "Kleddamag after Levy, Guzhou0806, Mira"
    bare = {"id": "T-997", "attribution": {"source_keys": ["[Stromquist 2003]"]}}
    assert credit_line(bare, SOURCES) == "Stromquist"


def test_no_registered_result_is_credited_to_this_project_by_that_phrase() -> None:
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    sources = render_results.load_sources()
    lines = {record["id"]: credit_line(record, sources) for record in register["results"]}
    assert all(credit and "project" not in credit.lower() for credit in lines.values())
    ours = [record for record in register["results"] if not record.get("attribution")]
    assert ours
    assert all(lines[record["id"]].split(" after ")[0] == "Levy" for record in ours)
    # The view prints the same line in its own table's credit column.
    rendered = render_results.render()
    for record in ours:
        row = next(
            line for line in rendered.splitlines() if line.startswith(f"| {record['id']} ")
        )
        assert row.split(" | ")[3] == lines[record["id"]], record["id"]


def test_builds_on_says_only_what_the_cited_evidence_names() -> None:
    """The `after` of this project's credit comes from the record: each source is one a
    cited evidence entry names, and each credited name is one of that source's authors."""
    cited = [{"id": "E-a", "source_key": WEIGHTED}, {"id": "E-b"}]
    record = {
        "id": "T-999",
        "novelty": "apparently-novel",
        "builds_on": {
            "credit": ["Burns", "Massaccesi"],
            "source_keys": [WEIGHTED],
        },
    }
    assert check_results.builds_on_problems(record, SOURCES, cited) == []
    assert check_results.builds_on_problems({"id": "T-999"}, SOURCES, cited) == []

    record["builds_on"]["credit"] = ["Burns", "Stromquist"]
    assert check_results.builds_on_problems(record, SOURCES, cited) == [
        f"T-999: builds_on credits Stromquist, who is not an author of {WEIGHTED}"
    ]
    record["builds_on"] = {"credit": ["Stromquist"], "source_keys": ["[Stromquist 2003]"]}
    assert check_results.builds_on_problems(record, SOURCES, cited) == [
        (
            "T-999: builds_on names [Stromquist 2003], which no evidence entry the result "
            "cites carries as its source_key"
        )
    ]
    record["builds_on"] = {"credit": ["Nobody"], "source_keys": ["[nobody 2026]"]}
    assert check_results.builds_on_problems(record, SOURCES, cited) == [
        "T-999: builds_on names [nobody 2026], which bibliography.yaml lacks",
        "T-999: builds_on credits Nobody, who is not an author of [nobody 2026]",
    ]


def test_a_result_by_others_carries_no_builds_on(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Its whole credit line is its source's, in the bibliography."""
    doubled = _changed_result(
        tmp_path,
        "T-032",
        builds_on={"credit": ["Burns"], "source_keys": [WEIGHTED]},
    )
    monkeypatch.setattr(check_results, "RESULTS", doubled)
    assert check_results.main() == 1
    assert "T-032: a result by others takes its credit from the bibliography" in (
        capsys.readouterr().out
    )


def test_a_recent_case_lower_bound_is_covered_for_its_own_n() -> None:
    """The entry that covers a case must cite its evidence and name its `n`.

    A monotone consequence is part of the result it follows from, so the scope carries
    it; an entry that cites the evidence at another `n` does not cover this one.
    """
    evidence = {"E-x": {"novelty": "previously-published", "source_key": "[s]"}}
    sources = {"[s]": {"dated": "2026-09-28"}}
    cases = {27: {"E-x"}, 28: {"E-x"}}
    narrow = [{"evidence": ["E-x"], "scope": {"n_values": [27]}}]
    assert check_results.coverage_problems(narrow, evidence, sources, cases) == [
        "n-028: its lower bound cites E-x, and no registered result citing it covers n = 28"
    ]
    wide = [{"evidence": ["E-x"], "scope": {"n_min": 27, "n_max": 28}}]
    assert check_results.coverage_problems(wide, evidence, sources, cases) == []
    sources["[s]"]["dated"] = "2026-08-21"
    assert check_results.coverage_problems(narrow, evidence, sources, cases) == []


def test_a_sources_credit_and_lineage_agree() -> None:
    """`lineage` is typed so no tool parses `credit`; the two must still say one thing.

    A source that builds on this project or credits it is printed "X after ..., Levy";
    an independent one never names this project. The four `n = 17` keys the W8 audit
    of 2026-09-29 found without that credit would have failed here.
    """
    bibliography = safe_load(check_results.BIBLIOGRAPHY.read_text(encoding="utf-8"))
    for source in bibliography["sources"]:
        lineage = source.get("lineage")
        if lineage is None:
            continue
        names_project = "Levy" in (source.get("credit") or "")
        assert names_project == (lineage != "independent"), source["key"]


def _dropped_field(tmp_path: Path, result_id: str, field: str) -> Path:
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    record = next(result for result in register["results"] if result["id"] == result_id)
    record.pop(field)
    target = tmp_path / "results.yaml"
    target.write_text(
        yaml.safe_dump(register, sort_keys=False, allow_unicode=True, width=96),
        encoding="utf-8",
    )
    return target


def test_a_result_without_a_headline_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A table row reads the headline, so a result with none would be a blank cell."""
    monkeypatch.setattr(check_results, "RESULTS", _dropped_field(tmp_path, "T-017", "headline"))
    assert check_results.main() == 1
    assert "T-017: states no headline" in capsys.readouterr().out


def test_a_headline_longer_than_a_table_cell_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The failure a headline invites: the claim's first sentence pasted in whole."""
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    claim = next(result for result in register["results"] if result["id"] == "T-017")["claim"]
    first_sentence = " ".join(str(claim).split()).split(". ")[0]
    assert len(first_sentence) > check_results.HEADLINE_LIMIT, "premise: the sentence is long"
    pasted = _changed_result(tmp_path, "T-017", headline=first_sentence)
    monkeypatch.setattr(check_results, "RESULTS", pasted)
    assert check_results.main() == 1
    assert f"T-017: headline is {len(first_sentence)} characters, over the 100" in (
        capsys.readouterr().out
    )


def test_a_headline_states_only_numbers_its_claim_does() -> None:
    """A headline may cut the claim's decimal short, marked, but never round or add one.

    Rounding `3.810025...` up to `3.810026` would overstate a lower bound in the one cell
    a reader sees; a truncation marked with an ellipsis stays true.
    """
    record = {
        "id": "T-999",
        "claim": "s(11) >= 38100*sqrt(8100042893309449)/899996306539 = 3.810025723614703.",
    }
    assert check_results.headline_problems({**record, "headline": "`s(11) ≥ 3.8100257…`"}) == []
    assert check_results.headline_problems({**record, "headline": "`s(11) ≥ 3.810026`"}) == [
        "T-999: headline states 3.810026, which its claim does not"
    ]
    assert check_results.headline_problems({**record, "headline": "`s(11) ≥ 3.8100257`"}) == [
        "T-999: headline states 3.8100257, which its claim does not"
    ]
    assert check_results.headline_problems({**record, "headline": "`s(12) ≥ 3.8100257…`"}) == [
        "T-999: headline states 12, which its claim does not"
    ]


def test_a_result_by_others_carries_no_established_date(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Its date is its source's, in `attribution.published`; a second would disagree."""
    dated_twice = _changed_result(tmp_path, "T-032", established="2026-09-20")
    monkeypatch.setattr(check_results, "RESULTS", dated_twice)
    assert check_results.main() == 1
    assert "T-032: a result by others is dated by attribution.published" in (
        capsys.readouterr().out
    )


def test_a_result_of_this_project_names_the_day_it_was_established(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    undated = _dropped_field(tmp_path, "T-017", "established")
    monkeypatch.setattr(check_results, "RESULTS", undated)
    assert check_results.main() == 1
    assert "T-017: a result of this project names the day it was established" in (
        capsys.readouterr().out
    )


def test_an_established_date_lies_within_the_projects_record() -> None:
    """Not before the project began, not after the register was last reviewed, and real."""
    record = {"id": "T-999", "established": "2026-08-22"}
    assert check_results.established_problems(record, "2026-09-29") == []
    assert check_results.established_problems(
        {**record, "established": "2026-08-21"}, "2026-09-29"
    ) == ["T-999: established 2026-08-21 is before 2026-08-22, when this project's work began"]
    assert check_results.established_problems(
        {**record, "established": "2026-09-30"}, "2026-09-29"
    ) == ["T-999: established 2026-09-30 is after the register's last review, 2026-09-29"]
    assert check_results.established_problems(
        {**record, "established": "2026-09-31"}, "2026-09-29"
    ) == ["T-999: established 2026-09-31 is not a date"]


def test_every_result_carries_a_registration_date(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    undated = _dropped_field(tmp_path, "T-007", "registered")
    monkeypatch.setattr(check_results, "RESULTS", undated)
    assert check_results.main() == 1
    assert "T-007: registered is required" in capsys.readouterr().out


def test_a_registration_date_is_a_date_no_later_than_the_review() -> None:
    record = {"id": "T-009", "registered": "2026-09-01"}
    assert check_results.registered_problems(record, "2026-09-29") == []
    assert check_results.registered_problems(record, "2026-09-01") == []
    assert check_results.registered_problems(
        {**record, "registered": "2026-02-30"}, "2026-09-29"
    ) == ["T-009: registered is not a calendar date: 2026-02-30"]
    assert check_results.registered_problems(
        {**record, "registered": "2026-10-01"}, "2026-09-29"
    ) == ["T-009: registered 2026-10-01 is after the register's last_reviewed 2026-09-29"]


def test_grouped_results_lists_every_result_once_in_the_rendered_order() -> None:
    """`grouped_results` is the grouping `RESULTS.md` is written from, not a copy of it.

    Every entry appears exactly once, and reading the groups in order gives the ids in
    the order the committed `RESULTS.md` tables list them, group headings included.
    """
    register = safe_load(render_results.RESULTS.read_text(encoding="utf-8"))
    groups = render_results.grouped_results(register)
    grouped = [record["id"] for _, group in groups for record in group]
    assert sorted(grouped) == sorted(record["id"] for record in register["results"])
    assert len(grouped) == len(set(grouped))

    committed = render_results.OUTPUT.read_text(encoding="utf-8")
    tables = committed.split("## Next actions")[0]
    assert grouped == re.findall(r"^\| (T-\d{3}) \|", tables, re.MULTILINE)
    headings = re.findall(r"^##+ (.+)$", tables, re.MULTILINE)
    titles = [title for title, _ in groups]
    assert titles[0] == headings[0] == render_results.OURS
    assert [h for h in headings if h in dict(render_results.OTHERS).values()] == titles[1:]


def test_the_kind_vocabulary_is_one_list_in_three_places() -> None:
    """The checker's tuple, the schema's enum and the rubric's table name the same kinds
    in the same order, so none can gain or lose one alone."""
    schema = safe_load((check_results.FRONTIER / "results.schema.yaml").read_text("utf-8"))
    result = schema["$defs"]["result"]
    assert tuple(result["properties"]["kind"]["enum"]) == check_results.KINDS
    assert "kind" in result["required"]
    rubric = (check_results.REPO / "epistemics.md").read_text(encoding="utf-8")
    section = rubric.split("## Result Kinds")[1].split("\n## ")[0]
    listed = re.findall(r"^\| ([a-z][a-z ]+) \| [A-Z]", section, re.MULTILINE)
    assert listed == [check_results.kind_label(kind) for kind in check_results.KINDS]
    assert set(check_results.KINDS) > check_results.BOUND_KINDS | check_results.STRUCTURE_KINDS


def test_every_result_declares_its_kind_right_after_its_id() -> None:
    """One kind each, on the line after `id`, where a second branch's field cannot
    collide with it; and every kind the vocabulary holds is one a result uses."""
    text = check_results.RESULTS.read_text(encoding="utf-8")
    declared = re.findall(r"^  - id: (T-\d{3})\n    kind: ([a-z-]+)\n", text, re.MULTILINE)
    register = safe_load(text)
    assert [rid for rid, _ in declared] == [record["id"] for record in register["results"]]
    assert {kind for _, kind in declared} == set(check_results.KINDS)
    assert len(re.findall(r"^    kind: ", text, re.MULTILINE)) == len(declared)


def test_a_result_without_a_kind_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(check_results, "RESULTS", _dropped_field(tmp_path, "T-017", "kind"))
    assert check_results.main() == 1
    assert "T-017: states no kind" in capsys.readouterr().out


def test_not_a_bound_is_not_a_kind(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A kind says what a result is. The retired tag said only what it was not."""
    vague = _changed_result(tmp_path, "T-014", kind="not-a-bound")
    monkeypatch.setattr(check_results, "RESULTS", vague)
    assert check_results.main() == 1
    assert "T-014: kind not-a-bound is not one of lower-bound, upper-bound" in (
        capsys.readouterr().out
    )


@pytest.mark.parametrize(
    ("result", "kind", "refusal"),
    [
        # A headline that opens with a relation on s(n) states its kind.
        ("T-001", "upper-bound", "upper bound, but its headline opens with a lower bound"),
        ("T-009", "lower-bound", "lower bound, but its headline opens with an upper bound"),
        ("T-017", "optimality", "optimality, but its headline opens with a lower bound"),
        ("T-051", "lower-bound", "lower bound, but its headline opens with an exact value"),
        (
            "T-037",
            "case-exclusion",
            "case exclusion, but its headline opens with a lower bound",
        ),
        # A headline that opens with words still states its relation, and so does a claim.
        ("T-011", "lower-bound", "kind is lower bound, but its headline states s(n) ≤"),
        ("T-044", "upper-bound", "kind is upper bound, but its claim states only s(n) >="),
        ("T-004", "rigidity", "a rigidity is no bound on s(n), but its headline states s(n) ≥"),
        # The cited evidence claims what the kind needs.
        ("T-056", "lower-bound", "and no cited evidence claims `lower-bound` or `exact-value`"),
        ("T-014", "upper-bound", "and no cited evidence claims `upper-bound` or `exact-value`"),
        ("T-036", "optimality", "an optimality result states an exact value, s(n) = v"),
        ("T-112", "optimality", "an optimality result states an exact value, s(n) = v"),
        ("T-004", "uniqueness", "a uniqueness is no bound on s(n), but its headline states"),
        ("T-003", "case-exclusion", "and no cited evidence claims `derived-structure`"),
        # A simplification names the result it proves again, on a case they share.
        ("T-001", "simplification", "a simplification's claim names the registered result"),
    ],
)
def test_a_kind_its_record_contradicts_is_refused(result: str, kind: str, refusal: str) -> None:
    """Each live result, declared as a kind it is not, is refused by its own record:
    its headline, its claim or the evidence it cites."""
    record, cited, scopes = _live_record(result)
    assert check_results.kind_problems(record, cited, scopes) == []
    problems = check_results.kind_problems({**record, "kind": kind}, cited, scopes)
    assert any(refusal in problem for problem in problems), problems
    assert all(problem.startswith(f"{result}: ") for problem in problems)


def test_a_contradicted_kind_fails_the_register_gate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        check_results, "RESULTS", _changed_result(tmp_path, "T-001", kind="upper-bound")
    )
    assert check_results.main() == 1
    assert "T-001: kind is upper bound, but its headline opens with a lower bound" in (
        capsys.readouterr().out
    )


def _live_record(result_id: str) -> tuple[dict, list[dict], dict[str, set[int]]]:
    """A live result, the evidence entries it cites and every result's cases."""
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    evidence = {
        entry["id"]: entry
        for entry in safe_load(check_results.EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    }
    scopes = {
        record["id"]: check_results.scope_values(record["scope"])
        for record in register["results"]
    }
    record = next(record for record in register["results"] if record["id"] == result_id)
    return record, [evidence[ref] for ref in record["evidence"]], scopes


def test_the_kind_a_headline_opens_with_is_derived() -> None:
    derive = check_results.headline_kind
    assert derive("`s(17) ≥ 4426213/1000000 = 4.426213`, from a set") == "lower-bound"
    assert derive("`s(11) > 31/8 = 3.875`") == "lower-bound"
    assert derive("`s(27), s(28) ≥ 28/5`, `s(31) ≥ 148/25`") == "lower-bound"
    assert derive("`s(29) ≤ 5.933833…`, by a Krawczyk interval certificate") == "upper-bound"
    assert derive("`s(13) = 4`") == "optimality"
    assert derive("Trump's 1979 packing is exactly valid, so `s(11) ≤ 3.877…`") is None
    assert derive("Goebel's `n = 5` packing is second-order rigid at fixed side") is None
    assert check_results.stated_relations("s(12) > s(11) strictly, cos(x) = 1") == {">"}
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    for record in register["results"]:
        opens = derive(record["headline"])
        assert opens in {None, record["kind"]} or record["kind"] == "simplification", record[
            "id"
        ]


def test_optimality_needs_both_halves_or_an_exact_value() -> None:
    record = {
        "id": "T-999",
        "kind": "optimality",
        "headline": "`s(9) = 3`",
        "claim": "s(9) = 3.",
    }
    scopes = {"T-999": {9}}
    lower, upper, exact = ({"claim": c} for c in ("lower-bound", "upper-bound", "exact-value"))
    assert check_results.kind_problems(record, [lower, upper], scopes) == []
    assert check_results.kind_problems(record, [exact], scopes) == []
    assert check_results.kind_problems(record, [lower], scopes) == [
        (
            "T-999: kind is optimality, and no cited evidence claims `exact-value`, or both "
            "`lower-bound` and `upper-bound`"
        )
    ]


def test_a_simplification_names_a_result_on_a_case_it_shares() -> None:
    record = {
        "id": "T-999",
        "kind": "simplification",
        "headline": "`s(45) = 7` by a shorter route",
        "claim": "s(45) = 7, proved again without segments; T-053 holds the value.",
    }
    cited = [{"claim": "lower-bound"}, {"claim": "upper-bound"}]
    unnamed = [
        (
            "T-999: a simplification's claim names the registered result it proves again, "
            "on a case they share"
        )
    ]
    assert check_results.kind_problems(record, cited, {"T-999": {45}, "T-053": {45}}) == []
    assert check_results.kind_problems(record, cited, {"T-999": {45}, "T-053": {21}}) == unnamed
    silent = {**record, "claim": "s(45) = 7, proved again."}
    assert check_results.kind_problems(silent, cited, {"T-999": {45}}) == unnamed


def _superseded_by(*later: tuple[str, str], kind: str = "case-exclusion") -> dict:
    """A result of `kind` on n = 11, established 2026-09-24, declaring `later` results."""
    return {
        "id": "T-036",
        "kind": kind,
        "established": "2026-09-24",
        "superseded_by": [
            {"result": other, "extent": extent, "what": "The bound."} for other, extent in later
        ],
    }


def test_a_declared_supersession_names_a_later_result_on_a_shared_case() -> None:
    """A result whose kind is no bound declares the later results that imply it
    (`superseded_by`); each is registered, dated no earlier, on a case it shares, and
    named once (think-nlo0). The dates are the results' own, when their sources
    published them or this project established them, not when they were registered."""
    problems = check_results.superseded_by_problems
    dated = {"T-036": "2026-09-24", "T-035": "2026-09-24", "T-060": "2026-09-29"}
    dated |= {"T-020": "2026-09-05", "T-011": "1979", "T-062": "2026"}
    scopes = {"T-036": {11}, "T-035": {11}, "T-060": {11}, "T-020": {19}, "T-011": {11}}
    scopes |= {"T-062": {11}}
    assert problems(_superseded_by(("T-062", "part")), dated, scopes) == []
    assert problems(_superseded_by(("T-011", "part")), dated, scopes) == [
        "T-036: superseded_by names T-011, dated 1979, before this result's 2026-09-24"
    ]
    assert problems({"id": "T-036", "kind": "case-exclusion"}, dated, scopes) == []
    assert problems(_superseded_by(("T-060", "part")), dated, scopes) == []
    assert problems(_superseded_by(("T-035", "whole")), dated, scopes) == []
    assert problems(_superseded_by(("T-036", "whole")), dated, scopes) == [
        "T-036: superseded_by names the result itself"
    ]
    assert problems(_superseded_by(("T-060", "part"), ("T-060", "whole")), dated, scopes) == [
        "T-036: superseded_by names T-060 twice"
    ]
    assert problems(_superseded_by(("T-099", "part")), dated, scopes) == [
        "T-036: superseded_by names T-099, which is not registered"
    ]
    assert problems(_superseded_by(("T-020", "part")), dated, scopes) == [
        "T-036: superseded_by names T-020, dated 2026-09-05, before this result's 2026-09-24",
        "T-036: superseded_by names T-020, which shares no case with it",
    ]


def test_a_result_a_case_bound_rests_on_is_never_superseded_whole() -> None:
    """A result a case bound still rests on stays in the tables, so no declaration hides
    it as superseded whole, though one may supersede it in part (`think-rf21`): T-004, an
    audit at n = 46, carried that case's lower bound when this was found."""
    dated = {"T-036": "2026-09-24", "T-060": "2026-09-29"}
    scopes = {"T-036": {11}, "T-060": {11}}
    holding = frozenset({"T-036"})
    problems = check_results.superseded_by_problems
    assert problems(_superseded_by(("T-060", "whole")), dated, scopes, holding) == [
        (
            "T-036: superseded_by names T-060 as superseding all of it, but a case bound "
            "still rests on it"
        )
    ]
    assert problems(_superseded_by(("T-060", "part")), dated, scopes, holding) == []
    assert problems(_superseded_by(("T-060", "whole")), dated, scopes) == []
    # The register's own holders: every case bound rests on a registered result, and none
    # of the results declared superseded whole is among them.
    holders = check_results.holding_results()
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))["results"]
    assert holders <= {record["id"] for record in register}
    whole = {
        record["id"]
        for record in register
        for item in record.get("superseded_by") or []
        if item["extent"] == "whole"
    }
    assert "T-031" in whole
    assert not whole & holders


def test_an_unreadable_holder_is_reported_with_every_other_problem(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A case bound no registered result carries makes the holders unreadable, which
    `check_results` reports as one problem among the rest rather than stopping with a
    traceback before any of them (`think-wizo`)."""

    def unreadable() -> frozenset[str]:
        raise ValueError("n=12: novel evidence [E-x] is carried by results []")

    monkeypatch.setattr(check_results, "holding_results", unreadable)
    assert check_results.main() == 1
    shown = capsys.readouterr().out
    assert "1 results-register problems:" in shown
    assert "which results hold a case bound could not be read: n=12: novel evidence" in shown


def test_declared_supersessions_never_lead_back() -> None:
    """Two results of one day could each declare the other supersedes them, and both rows
    would be hidden; a cycle is named once, from its first result (`think-rf21`)."""

    def declaring(rid: str, *later: str) -> dict:
        items = [{"result": other, "extent": "whole", "what": "All."} for other in later]
        return {"id": rid, "superseded_by": items}

    cycles = check_results.superseded_by_cycles
    assert cycles([declaring("T-035", "T-036"), declaring("T-036", "T-035")]) == [
        "T-035: superseded_by leads back to it, T-035 to T-036 to T-035"
    ]
    three = [
        declaring("T-001", "T-002"),
        declaring("T-002", "T-003"),
        declaring("T-003", "T-001"),
    ]
    assert cycles(three) == [
        "T-001: superseded_by leads back to it, T-001 to T-002 to T-003 to T-001"
    ]
    assert cycles([declaring("T-035", "T-036"), declaring("T-036")]) == []
    assert cycles([declaring("T-036", "T-036")]) == []
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))["results"]
    assert cycles(register) == []


def test_a_bound_never_declares_what_supersedes_it() -> None:
    """A bound's supersession is derived from the case records, so a declaration on one
    is refused: two accounts of it could disagree."""
    dated = {"T-036": "2026-09-24", "T-060": "2026-09-29"}
    scopes = {"T-036": {11}, "T-060": {11}}
    for kind in check_results.BOUND_KINDS:
        later = _superseded_by(("T-060", "whole"), kind=kind)
        assert check_results.superseded_by_problems(later, dated, scopes) == [
            (
                "T-036: declares superseded_by, but its kind is "
                f"{check_results.kind_label(kind)}, whose supersession is derived from the "
                "case records and never declared"
            )
        ], kind


def test_a_declared_supersession_on_a_bound_fails_the_register_gate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    later = [{"result": "T-060", "extent": "whole", "what": "s(11) = T."}]
    monkeypatch.setattr(
        check_results, "RESULTS", _changed_result(tmp_path, "T-037", superseded_by=later)
    )
    assert check_results.main() == 1
    assert "T-037: declares superseded_by, but its kind is lower bound, whose" in (
        capsys.readouterr().out
    )


def test_t036_is_superseded_in_part_by_t060_and_t112() -> None:
    """T-060's `s(11) = T` implies T-036's bound clause for every packing and not its
    equality clause, since T-060 makes no claim of uniqueness (think-7df0); T-112, the
    uniqueness corollary of T-060, implies the equality clause (think-d1bd)."""
    record, _, _ = _live_record("T-036")
    declared = record["superseded_by"]
    assert [(item["result"], item["extent"]) for item in declared] == [
        ("T-060", "part"),
        ("T-112", "part"),
    ]
    first = " ".join(declared[0]["what"].split())
    assert first.startswith("The first clause")
    assert "equality clause" in first
    assert "is not implied" in first
    second = " ".join(declared[1]["what"].split())
    assert second.startswith("The equality clause")


def test_the_96_25_case_exclusions_are_superseded_by_t060() -> None:
    """T-060 leaves no packing of eleven squares at side 96/25, below T. That implies the
    whole of T-031's exclusion of the octagon class, and T-023's exclusion of its
    four-owner branch but not its count that at most five further squares fit beside
    the owners, which is about ten squares (think-rl2b)."""
    expected = {"T-031": "whole", "T-023": "part"}
    for entry, extent in expected.items():
        record, _, _ = _live_record(entry)
        assert record["kind"] == "case-exclusion", entry
        assert [(item["result"], item["extent"]) for item in record["superseded_by"]] == [
            ("T-060", extent)
        ], entry
        assert "96/25" in record["claim"], entry
    record, _, _ = _live_record("T-023")
    what = " ".join(record["superseded_by"][0]["what"].split())
    assert what.startswith("The conclusion")
    assert "at most five further squares" in what
    assert "is not implied" in what


def test_results_md_labels_every_result_by_its_kind() -> None:
    register = safe_load(render_results.RESULTS.read_text(encoding="utf-8"))
    committed = render_results.OUTPUT.read_text(encoding="utf-8")
    for record in register["results"]:
        row = next(
            line for line in committed.splitlines() if line.startswith(f"| {record['id']} |")
        )
        cells = row.split(" | ")
        assert cells[2] == check_results.kind_label(record["kind"]), record["id"]
        # The status column, the cell after S in both tables: the derived status first,
        # then each mark of supersession with what supersedes it, `superseded in part`
        # only on a result whose kind is no bound, which declares it (think-nlo0).
        status = cells[8 if record.get("attribution") else 7]
        assert status.split(", ")[0] in result_status.STATUSES, record["id"]
        if "superseded in part by " in status:
            assert record["kind"] not in check_results.BOUND_KINDS, record["id"]
            assert record["superseded_by"], record["id"]
        elif "superseded by " in status and record["kind"] not in check_results.BOUND_KINDS:
            assert any(item["extent"] == "whole" for item in record["superseded_by"])
    t037 = next(line for line in committed.splitlines() if line.startswith("| T-037 |"))
    assert t037.split(" | ")[8].startswith("confirmed, ")
    assert t037.split(" | ")[8].endswith(", superseded by T-060")


def test_results_by_others_awaiting_a_replay_lead_their_group() -> None:
    register = safe_load(render_results.RESULTS.read_text(encoding="utf-8"))
    for title, group in render_results.grouped_results(register)[1:]:
        replayed = [int(record["confirmation"][1]) >= 3 for record in group]
        assert replayed == sorted(replayed), title


def test_the_registration_backfill_inserts_only_missing_dates() -> None:
    text = (
        "results:\n"
        "  - id: T-001\n"
        "    registered: '2026-08-31'\n"
        "    claim: a\n"
        "  - id: T-002\n"
        "    claim: b\n"
    )
    assert backfill_result_registration.insert_dates(text, {"T-002": "2026-09-03"}) == (
        "results:\n"
        "  - id: T-001\n"
        "    registered: '2026-08-31'\n"
        "    claim: a\n"
        "  - id: T-002\n"
        "    registered: '2026-09-03'\n"
        "    claim: b\n"
    )


def test_the_registration_backfill_dates_an_entry_after_its_kind() -> None:
    """`kind` is the line after `id`, so a date goes after both and an entry dated there
    is not dated twice."""
    text = (
        "results:\n"
        "  - id: T-001\n"
        "    kind: audit\n"
        "    registered: '2026-08-31'\n"
        "  - id: T-002\n"
        "    kind: rigidity\n"
        "    claim: b\n"
    )
    dates = {"T-001": "2026-10-01", "T-002": "2026-09-03"}
    assert backfill_result_registration.insert_dates(text, dates) == (
        "results:\n"
        "  - id: T-001\n"
        "    kind: audit\n"
        "    registered: '2026-08-31'\n"
        "  - id: T-002\n"
        "    kind: rigidity\n"
        "    registered: '2026-09-03'\n"
        "    claim: b\n"
    )
    live = check_results.RESULTS.read_text(encoding="utf-8")
    ids = re.findall(r"^  - id: (T-\d{3})$", live, re.MULTILINE)
    assert backfill_result_registration.insert_dates(live, dict.fromkeys(ids, "x")) == live


def test_corrects_names_a_published_result_that_no_longer_stands() -> None:
    sources = {"[Nagamochi 2005]": {"authors": ["Nagamochi"]}}
    corrected = {
        "id": "T-007",
        "verification": "V0",
        "attribution": {"source_keys": ["[Nagamochi 2005]"]},
    }
    record = {
        "id": "T-083",
        "corrects": {"source_key": "[Nagamochi 2005]", "result": "T-007", "what": "Lemma 1"},
    }
    assert check_results.corrects_problems(record, sources, {"T-007": corrected}) == []
    assert check_results.corrects_problems({"id": "T-001"}, sources, {}) == []

    unknown = {**record, "corrects": {**record["corrects"], "source_key": "[Nobody 2000]"}}
    assert any(
        "bibliography.yaml lacks" in problem
        for problem in check_results.corrects_problems(unknown, sources, {"T-007": corrected})
    )
    missing = {**record, "corrects": {**record["corrects"], "result": "T-999"}}
    assert any(
        "not a registered result" in problem
        for problem in check_results.corrects_problems(missing, sources, {"T-007": corrected})
    )
    standing = {**corrected, "verification": "V3"}
    assert any(
        "still stands at V3" in problem
        for problem in check_results.corrects_problems(record, sources, {"T-007": standing})
    )
    other = {**corrected, "attribution": {"source_keys": ["[Someone 1999]"]}}
    assert any(
        "credits" in problem
        for problem in check_results.corrects_problems(record, sources, {"T-007": other})
    )
