# ruff: noqa: RUF001 -- the record's typography (minus signs, superscripts) is matched as written.
"""The T-007 consumer audit: its exact arithmetic, the classes it assigns, and its record."""

from __future__ import annotations

import hashlib
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_t007_consumers as audit
from devtools import check_nagamochi_bounds as nagamochi

REPO = Path(__file__).resolve().parents[2]


def rows() -> dict[int, dict[str, Any]]:
    return {row["n"]: row for row in audit.build_document()["rows"]}


def line_of(path: str, needle: str) -> int:
    """The line a needle is on, so a test survives edits elsewhere in the file."""
    lines = (REPO / path).read_text(encoding="utf-8").split("\n")
    return next(number for number, line in enumerate(lines, 1) if needle in line)


def test_the_retained_inventory_is_current() -> None:
    assert audit.OUTPUT.read_text(encoding="utf-8") == audit.render(audit.build_document())


def test_surd_arithmetic_is_exact() -> None:
    root2, root3 = audit.Surd.root(2), audit.Surd.root(3)
    assert audit.Surd.root(8) == audit.Surd.rational(2) * root2
    assert (root2 * root2).as_rational == 2
    assert audit.Surd.root(Fraction(1, 4)).as_rational == Fraction(1, 2)
    assert audit.Surd.rational(6) / root2 == audit.Surd.rational(3) * root2
    assert (root2 + audit.Surd.rational(Fraction(1, 10**50)) - root2).sign() == 1
    assert (root2 + root3 - audit.Surd.root(5)).sign() == 1
    assert (root2 + root3 - audit.Surd.root(10)).sign() == -1
    assert (root2 - root2).sign() == 0
    assert audit.Surd.root(150).floor() == 12
    assert root2.decimal() == "1.414213562373"
    assert audit.Surd.rational(Fraction(-1, 3)).decimal() == "-0.333333333334"
    with pytest.raises(ValueError, match="sum of radicals"):
        _ = audit.Surd.rational(1) / (audit.Surd.rational(1) + root2)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("2 + (1/2)sqrt(2)", "2 + (1/2)*sqrt(2)"),
        ("sqrt(150 - 2*floor(sqrt(150)) + 1) + 1", "1 + sqrt(127)"),
        ("18*sqrt(5)/101 + 2*sqrt(2) + 709/101", "709/101 + 2*sqrt(2) + (18/101)*sqrt(5)"),
        ("94*sqrt(2)/41 + 247/41", "247/41 + (94/41)*sqrt(2)"),
        ("15680/3951", "15680/3951"),
        ("5.0", "5"),
    ],
)
def test_the_parser_reads_every_shape_the_register_uses(text: str, expected: str) -> None:
    assert audit.parse_exact(text).render() == expected


@pytest.mark.parametrize(
    "text",
    [
        "x+1",
        "sin(1)",
        "__import__('os')",
        "sqrt(sqrt(2))",
        "1/(1+sqrt(2))",
        "1/0",
        "True",
        "2**3",
    ],
)
def test_the_parser_refuses_what_its_arithmetic_cannot_hold(text: str) -> None:
    with pytest.raises(ValueError, match=r"expression|radical|division"):
        audit.parse_exact(text)


def test_display_slack_refuses_to_guess_a_close_comparison() -> None:
    def display(value: str, places: int) -> audit.Quantity:
        return audit.Quantity(
            audit.Surd.rational(Fraction(value)), "display", Fraction(1, 10**places)
        )

    assert audit.compare(display("3.877", 3), display("3.900", 3)) == -1
    with pytest.raises(ValueError, match="cannot separate"):
        audit.compare(display("3.877", 3), display("3.8775", 4))
    with pytest.raises(ValueError, match="cannot separate"):
        audit.compare(display("3.877", 3), display("3.9", 1))


def test_nagamochi_values_agree_with_the_gate_checker_at_every_case() -> None:
    for n in range(4, 325):
        value = audit.nagamochi_value(n)  # raises on any disagreement with theorem_two
        _, is_exact = nagamochi.theorem_two(n)
        assert (value.as_rational is not None) == is_exact
        assert audit.compare(
            audit.Quantity(value, "nagamochi"), audit.Quantity(audit.area_bound(n), "area")
        ) == (0 if math.isqrt(n) ** 2 == n else 1)


def test_karakus_bound_sits_between_area_and_nagamochi_touching_it_at_k2_minus_1() -> None:
    for n in range(1, 325):
        bound = audit.karakus_bound(n)
        if n < 8 or math.isqrt(n) ** 2 == n:
            assert bound is None
            continue
        assert bound is not None
        area = audit.Quantity(audit.area_bound(n), "area")
        karakus = audit.Quantity(bound, "karakus")
        target = audit.Quantity(audit.nagamochi_value(n), "nagamochi")
        assert audit.compare(karakus, area) == 1
        k2_minus_1 = math.isqrt(n + 1) ** 2 == n + 1
        assert audit.compare(karakus, target) == (0 if k2_minus_1 else -1)
        if k2_minus_1:
            assert bound.as_rational == math.isqrt(n + 1)


def classify(**overrides: Any) -> dict[str, Any]:
    def quantity(value: int | str) -> audit.Quantity:
        return audit.Quantity(audit.Surd.rational(Fraction(value)), "test")

    arguments: dict[str, Any] = {
        "cites_t007": True,
        "target": quantity(8),
        "area": quantity("7.8"),
        "registered": None,
        "shape": None,
        "karakus": None,
    }
    numeric = {"target", "area", "registered", "karakus"}
    arguments.update(
        {key: quantity(value) if key in numeric else value for key, value in overrides.items()}
    )
    return audit.classify(**arguments)


def test_classification_follows_its_declared_order() -> None:
    assert classify(cites_t007=False)["reason"] == "operative-bound-independent"
    assert classify(area=8)["reason"] == "area-bound"
    assert classify(registered=8)["reason"] == "registered-verified-bound-covers-it"
    assert classify(registered=8, shape=("k^2-1", 9))["class"] == audit.UNAFFECTED
    assert classify(shape=("k^2-1", 9))["class"] == audit.REPROVED
    assert classify()["class"] == audit.ONLY
    assert classify(registered="7.5")["class"] == audit.ONLY
    weakened = classify(registered="7.9")
    assert weakened["class"] == audit.WEAKENED
    assert weakened["weakened_to"]["exact"] == "79/10"
    assert classify(registered="7.9", karakus="7.95")["reason"] == "karakus-6.1"
    assert classify(registered="7.95", karakus="7.9")["reason"] == "registered-verified-bound"
    with pytest.raises(ValueError, match="Nagamochi value"):
        audit.classify(
            cites_t007=True,
            target=None,
            area=audit.Quantity(audit.Surd.rational(1), "area"),
            registered=None,
            shape=None,
            karakus=None,
        )


def test_the_register_counts_match_the_frontier_readme() -> None:
    """Since the correction of 2 October 2026 no operative verified bound cites T-007."""
    summary = audit.build_document()["summary"]
    operative = summary["operative_cites_t007"]
    # 261 open cases at the correction; 247 since the merge of 2026-10-03, whose replayed
    # covers and families proved n = 59 to 61, 77, 78 and nine k^2 - 3 cases.
    assert (operative["all"], operative["open"], summary["open_cases"]) == (0, 0, 247)
    assert operative["outside_t007_registered_scope_n"] == ""
    assert summary["classes"] == {
        audit.UNAFFECTED: 324,
        audit.REPROVED: 0,
        audit.WEAKENED: 0,
        audit.ONLY: 0,
    }
    assert summary["reported_lower_bounds_citing_t007"].startswith("23, 34, 47-48, 62-63")


def test_no_exact_value_rests_on_t007_and_each_family_names_its_new_proof() -> None:
    summary = audit.build_document()["summary"]
    assert summary["exact_value_claims_citing_t007"] == []
    assert summary["exact_value_claims_on_t007_alone"] == []
    assert summary["exact_value_claims_on_t007_alone_without_karakus"] == []
    by_n = rows()
    for k in range(3, 19):
        minus_two = by_n[k * k - 2]["operative_lower_bound"]
        assert (minus_two["evidence"], minus_two["results"]) == (
            ["E-chelokot-square-minus-two-lean"],
            ["T-086"],
        )
        minus_one = by_n[k * k - 1]["operative_lower_bound"]
        assert minus_one["evidence"] == [
            "E-karakus-strip-lower",
            "E-karakus-strip-measure-interval",
        ]
        assert "T-084" in minus_one["results"]


def test_case_rows_carry_each_kind_of_support_separately() -> None:
    by_n = rows()
    n62 = by_n[62]
    assert (n62["exposure_class"], n62["exposure_reason"]) == (
        audit.UNAFFECTED,
        "operative-bound-independent",
    )
    assert n62["reported_lower_bound"]["cites_t007"] is True
    # Since the merge of 2026-10-03 the replayed covers proving s(59) = 8 (T-066) and
    # s(60) = s(61) = 8 (T-062) are verified too, and carry to n = 62 by monotonicity.
    assert [s["results"] for s in n62["support"]["registered_verified"]["sources"]] == [
        ["T-066"],
        ["T-062"],
        ["T-086"],
    ]
    assert n62["support"]["registered_reported"]["reaches_nagamochi"] is True
    assert [s["results"] for s in n62["support"]["registered_reported"]["sources"]] == [
        ["T-066"],
        ["T-062"],
        ["T-063"],
    ]
    assert n62["support"]["karakus_explicit_bound"]["reaches_nagamochi"] is False
    assert n62["support"]["chelokot_lean"]["verified"] is True
    assert by_n[63]["support"]["karakus_k2_minus_1"]["value"] == 8
    # T-044's 861/100 until the merge of 2026-10-03; wand125's replayed n = 71 rectangle
    # certificate (T-070), carried by monotonicity, until 5 October; since, wand125's own
    # n = 73 mixed certificate (T-091), decided here by sqverify-fast.
    assert by_n[73]["operative_lower_bound"]["exact_form"] == "8813/1000"
    assert by_n[73]["operative_lower_bound"]["results"] == ["T-091"]
    # T-007 was scoped 4 to 100 until 2026-10-06, when it took the scope of its evidence,
    # E-nagamochi-lower, 4 to 324.
    assert by_n[150]["operative_lower_bound"]["t007_scope_covers_n"] is True
    assert all(
        row["operative_lower_bound"]["t007_scope_covers_n"]
        for row in by_n.values()
        if row["n"] >= 4
    )


def test_an_independent_route_through_a_nagamochi_lemma_says_so() -> None:
    sources = rows()[47]["support"]["registered_verified"]["sources"]
    assert [(source["n"], source["results"]) for source in sources] == [
        (45, ["T-053"]),
        (46, ["T-004", "T-008"]),
        (47, ["T-086"]),
    ]
    assert "shares_a_nagamochi_lemma" not in sources[0]
    caveat = sources[1]["shares_a_nagamochi_lemma"]
    for key, needle in (("cited_at", "Nagamochi [7]"), ("nagamochi_lemma_at", "Lemma 7")):
        path, line = caveat[key].rsplit(":", 1)
        assert needle in (REPO / path).read_text(encoding="utf-8").split("\n")[int(line) - 1]


def test_case_prose_proofs_and_their_defects_are_carried() -> None:
    by_n = rows()
    n7 = by_n[7]["support"]["case_prose_published_proofs"]
    assert n7["defects"] == ["D-344–D-347"]
    assert n7["proofs"][0]["label"] == "El Moumni’s Theorem 1"
    assert by_n[150]["support"]["case_prose_published_proofs"] is None


@pytest.mark.parametrize(
    "link",
    [
        "../resources/papers/el-moumni-1999-optimal-packings-unit-squares.pdf",
        (
            "https://github.com/jlevy/squares/releases/download/data/source-pdfs-v1/"
            "el-moumni-1999-optimal-packings-unit-squares.pdf"
        ),
    ],
)
def test_hosted_paper_citations_preserve_archived_proof_identity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, link: str
) -> None:
    root = tmp_path / "repo"
    frontier = root / "packing/frontier"
    frontier.mkdir(parents=True)
    source = "packing/resources/papers/el-moumni-1999-optimal-packings-unit-squares.pdf"
    hosted = (
        "https://github.com/jlevy/squares/releases/download/data/source-pdfs-v1/"
        "el-moumni-1999-optimal-packings-unit-squares.pdf"
    )
    monkeypatch.setattr(audit, "REPO", root)
    monkeypatch.setattr(audit, "hosted_paper_sources", lambda: {hosted: source})
    (frontier / "n-007.md").write_text(
        "## The lower bound\n"
        f"[El Moumni’s Theorem 1]({link})\n"
        "[Other paper](https://example.invalid/other.pdf)\n"
        "[D-344–D-347](../../defects.md)\n"
    )
    assert audit.prose_published_proofs(7) == {
        "status": "published-archived-unregistered",
        "proofs": [
            {
                "label": "El Moumni’s Theorem 1",
                "source": source,
                "at": "packing/frontier/n-007.md:2",
            }
        ],
        "defects": ["D-344–D-347"],
    }


def test_the_scan_sorts_lines_into_tiers() -> None:
    lines = (
        "Nagamochi proved s(k^2 - 2) = k.",
        "",
        "| T-044 | lower bound | wand125 after Stromquist, Nagamochi, Burns |",
        "| 92 | 10 | Nagamochi | 0.34 |",
        "",
        "The floor here is Nagamochi’s closed form.",
        "",
        "Karakuş showed the scoring lemma fails; s(n^2-2) = n is open.",
        "",
        "the loop stalls at the 1e-12 floor, and E-nagamochi-lower is an identifier",
        "since n^2-2n < (n-1)^2",
    )
    hits = {hit["line"]: hit for hit in audit.scan_text("\n".join(lines))}
    assert {line: hit["tier"] for line, hit in hits.items()} == {
        1: "states",
        3: "mentions",
        4: "relies",
        6: "relies",
        8: "states",
    }
    assert [line for line, hit in hits.items() if hit["qualified"]] == [8]


def test_the_inventory_finds_the_statements_the_correction_reached() -> None:
    """Each statement the correction of 2 October 2026 reached is still found, now qualified.

    T-007's own register row still states its theorem without the qualifier, as the row of
    a result whose status is `incomplete` should, so the scan must still report it.
    """
    files = {entry["path"]: entry for entry in audit.build_document()["documents"]["files"]}
    expected = (
        ("packing/frontier/RESULTS.md", "| T-007 |", False),
        ("packing/frontier/evidence.yaml", "exact values for N in {m^2, m^2-1, m^2-2}", True),
        ("packing/frontier/README.md", "have Nagamochi’s formula as their verified", True),
        ("packing/frontier/n-322.md", "that Nagamochi’s general theorem (2005) stated", True),
        (
            "docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md",
            "Nagamochi’s $s(n^2 - 1) = s(n^2 - 2) = n$",
            True,
        ),
    )
    groups = {path: group for group, path in audit.document_paths()}
    for path, needle, qualified in expected:
        stated = {
            hit["line"]: hit["qualified"]
            for hit in audit.scan_document(groups[path], path)
            if hit["tier"] == "states"
        }
        assert stated.get(line_of(path, needle)) is qualified, path
        live = [line for line, is_qualified in stated.items() if not is_qualified]
        assert files[path]["statements"]["unqualified_states"] == len(live), path


def walk(node: object, key: str = "") -> list[str]:
    """Every key in a JSON tree, so a test can ask what the record never carries."""
    if isinstance(node, dict):
        return [k for name, value in node.items() for k in (name, *walk(value, name))]
    if isinstance(node, list):
        return [k for value in node for k in walk(value, key)]
    return []


def test_the_retained_document_worklist_carries_no_line_numbers() -> None:
    keys = walk(audit.build_document()["documents"])
    assert not [key for key in keys if key == "line" or key.endswith("_lines")]
    retained = audit.OUTPUT.read_text(encoding="utf-8")
    assert '"line"' not in retained
    assert "_lines" not in retained


def test_a_document_entry_survives_edits_elsewhere_in_the_document() -> None:
    lines = (
        "Nagamochi proved s(k^2 - 2) = k.",
        "",
        "| 92 | 10 | Nagamochi | 0.34 |",
        "",
        "The floor here is Nagamochi’s closed form.",
    )
    text = "\n".join(lines)
    edited = "A new opening paragraph.\n\nAnother, two lines\nlong.\n\n" + text + "\n\nCoda."
    before = audit.document_entry("reader", "x.md", audit.scan_text(text))
    after = audit.document_entry("reader", "x.md", audit.scan_text(edited))
    assert before == after
    assert before["statements"]["states"] == 1
    assert before["phrases"] == {
        "beside: floor": 1,
        "k2-minus-2-identity: k^2 - 2": 1,
        "lone table cell": 1,
    }


def test_check_fails_when_the_anchored_formula_is_gone(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(audit.KARAKUS_AT, "explicit_bound_at", "a formula the archive lacks")
    audit.build_document.cache_clear()
    try:
        assert audit.main(["--check"]) == 1
    finally:
        monkeypatch.undo()
        audit.build_document.cache_clear()
    assert audit.main(["--check"]) == 0


def test_check_reports_a_stale_record(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "audit.json"
    monkeypatch.setattr(audit, "OUTPUT", target)
    assert audit.main(["--check"]) == 1
    assert audit.main(["--update"]) == 0
    assert audit.main(["--check"]) == 0
    target.write_text(target.read_text(encoding="utf-8") + " ", encoding="utf-8")
    assert audit.main(["--check"]) == 1


def test_the_archived_preprint_is_the_one_whose_statements_are_used() -> None:
    karakus = audit.build_document()["sources"]["karakus"]
    pdf = REPO / next(path for path in karakus["archived"] if path.endswith(".pdf"))
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == karakus["pdf_sha256"]
    path, line = karakus["explicit_bound_at"].rsplit(":", 1)
    printed = (REPO / path).read_text(encoding="utf-8").split("\n")[int(line) - 1]
    assert "\\tag{6.1}" in printed


def test_chelokot_is_listed_at_every_k2_minus_2_case_as_the_register_holds_it() -> None:
    by_n = rows()
    for k in range(2, 19):
        entry = by_n[k * k - 2]["support"]["chelokot_lean"]
        assert entry["kind"] == "Lean theorem, replayed here with its axiom receipt"
        assert entry["verified"] is True
        assert (entry["claims"][0]["value"], entry["claims"][0]["verified"]) == (k, True)
    individual = by_n[23]["support"]["chelokot_lean"]["claims"][1:]
    assert individual
    assert not [claim for claim in individual if claim["verified"]]


def test_chelokot_reads_as_reported_when_the_register_does_not_hold_it_verified(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    held = audit.register()
    evidence = dict(held.evidence)
    evidence[str(audit.CHELOKOT["evidence"])] = {
        **evidence[str(audit.CHELOKOT["evidence"])],
        "replay_status": "failed",
    }
    monkeypatch.setattr(
        audit, "register", lambda: audit.Register(held.cases, held.results, evidence)
    )
    entry = audit.chelokot_entry(62)
    assert entry is not None
    assert entry["verified"] is False
    assert entry["claims"][0]["verified"] is False
