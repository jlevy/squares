"""The stage's citation data: its rules, over recorded register entries, and its contract.

`devtools.build_bound_citations` writes one line per bound the stage shows. The rules are
tested on their own over small hand-built registers, the committed record is tested against
the composite figure it sits beside, and the source keys it cites are tested against the
archive index, which is where `think-dlof` found three of them missing and two spelled two
ways.
"""

from __future__ import annotations

import functools
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

from devtools import build_bound_citations as citations
from devtools import validate_schemas
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_INDEX = ROOT / "resources" / "README.md"
COMPOSITE = ROOT / "atlas" / "known-best" / "composite-figure.json"

#: How the archive index defines a key: in bold, at the head of a table row or a bullet.
DEFINED_KEY = re.compile(r"\*\*(\[.+?\])\*\*")
RESULT_KEY = re.compile(r"^\[(T-[0-9]{3})\]$")

#: The date every synthetic result is scored on; the year is what a project line prints.
SCORED = {"significance": {"scored": "2026-09-01"}}


@functools.cache
def _register() -> citations.Register:
    return citations.load_register()


@functools.cache
def _record() -> dict[str, Any]:
    return citations.build_record()["citations"]


@functools.cache
def _composite() -> dict[int, dict[str, Any]]:
    figure = json.loads(COMPOSITE.read_text(encoding="utf-8"))["figure"]
    return {entry["n"]: entry for entry in figure["entries"]}


@functools.cache
def _defined_keys() -> frozenset[str]:
    return frozenset(DEFINED_KEY.findall(ARCHIVE_INDEX.read_text(encoding="utf-8")))


def _papers_table() -> dict[str, dict[str, str]]:
    """The archive index's Papers table, by key: its Authors and Year cells."""
    section = ARCHIVE_INDEX.read_text(encoding="utf-8").split("\n## Papers\n", 1)[1]
    section = section.split("\n## ", 1)[0]
    rows: dict[str, dict[str, str]] = {}
    for line in section.splitlines():
        if not line.startswith("| **["):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        key = DEFINED_KEY.match(cells[0])
        assert key is not None, line
        rows[key.group(1)] = {"authors": cells[2], "year": cells[3]}
    return rows


def _entry(n: int) -> dict[str, Any]:
    entry = _record()["entries"][n - 1]
    assert entry["n"] == n
    return entry


def _line(citation: Mapping[str, Any] | None) -> tuple[str, str, str] | None:
    """A line as the stage sets it -- the reference and its note -- with where it stands."""
    if citation is None:
        return None
    return (citations.drawn(citation), citation["basis"], citation["assurance"])


# --------------------------------------------------------------------------- the rules


def test_authors_join_as_one_two_or_the_first_et_al() -> None:
    assert citations.join_authors(["Göbel"]) == "Göbel"
    assert citations.join_authors(["Kearney", "Shiu"]) == "Kearney & Shiu"
    assert citations.join_authors(["Arslanov", "Mustafin", "Shangitbayev"]) == "Arslanov et al."
    with pytest.raises(ValueError, match="at least one author"):
        citations.join_authors([])


def test_a_missing_author_or_year_is_left_out_not_filled() -> None:
    assert (
        citations.cite("Göbel", 1979, "Squares in Squares") == "Göbel 1979, Squares in Squares"
    )
    assert (
        citations.cite("Ellsworth", None, "Squares in Squares")
        == "Ellsworth, Squares in Squares"
    )
    assert citations.cite(None, None, "Squares in Squares") == "Squares in Squares"


def test_an_improved_construction_credits_its_lineage_and_leaves_the_year_out() -> None:
    """`found_year` dates the find; the side the stage prints is the improvement's."""
    names = _register().names
    found = {"found_by": ["Frits Göbel"], "found_year": 1979, "improved_by": []}
    assert citations.credit(found, names) == ("Göbel", 1979)
    improved = {
        "found_by": ["Thomas Schadt"],
        "found_year": 2025,
        "improved_by": ["David Ellsworth"],
    }
    assert citations.credit(improved, names) == ("Schadt & Ellsworth", None)
    # A finder who improved their own packing is named once, and the year still goes.
    own = {
        "found_by": ["David Ellsworth"],
        "found_year": 2024,
        "improved_by": ["David Ellsworth", "David W. Cantrell"],
    }
    assert citations.credit(own, names) == ("Ellsworth & Cantrell", None)
    assert citations.credit({"found_by": [], "found_year": None, "improved_by": []}, names) == (
        None,
        None,
    )


def test_a_credited_name_with_no_surname_on_record_fails_rather_than_being_guessed() -> None:
    with pytest.raises(ValueError, match="credited names missing"):
        citations.credit({"found_by": ["A. N. Other"], "found_year": 2000}, {})


def _synthetic_register() -> citations.Register:
    """A register small enough to read: derived, published, replayed and novel entries."""
    evidence = {
        "E-grid": {"claim": "upper-bound", "novelty": "common-knowledge"},
        "E-area": {"claim": "lower-bound", "novelty": "common-knowledge"},
        "E-paper": {
            "claim": "lower-bound",
            "performed_by": "source-author",
            "novelty": "previously-published",
            "source_key": "[Paper 2001]",
        },
        "E-replay": {
            "claim": "lower-bound",
            "performed_by": "repository",
            "novelty": "previously-published",
            "source_key": "[Paper 2001]",
        },
        "E-other": {
            "claim": "lower-bound",
            "performed_by": "source-author",
            "novelty": "previously-published",
            "source_key": "[Other 2002]",
        },
        "E-ours": {
            "claim": "lower-bound",
            "performed_by": "repository",
            "novelty": "apparently-novel",
        },
        "E-catalogue": {"claim": "upper-bound", "novelty": "previously-published"},
        # A new certificate of someone else's packing: the n = 29 shape.
        "E-certificate": {
            "claim": "upper-bound",
            "performed_by": "repository",
            "novelty": "apparently-novel",
        },
    }
    results = [
        {"id": "T-900", "scope": {"n_values": [7]}, "evidence": ["E-ours"], **SCORED},
        # Carries the replay, so it confirms the published bound.
        {"id": "T-901", "scope": {"n_values": [7]}, "evidence": ["E-replay"], **SCORED},
        # Cites the source's own proof only: relevant, and confirming nothing.
        {"id": "T-902", "scope": {"n_values": [7]}, "evidence": ["E-paper"], **SCORED},
        # The same replay at another n, which this n may not claim.
        {"id": "T-903", "scope": {"n_values": [8]}, "evidence": ["E-replay"], **SCORED},
        {"id": "T-910", "scope": {"n_values": [7]}, "evidence": ["E-certificate"], **SCORED},
    ]
    sources = {
        "[Paper 2001]": citations.Source("[Paper 2001]", ("Author",), 2001, "J. Test 1"),
        "[Other 2002]": citations.Source("[Other 2002]", ("Other",), 2002, "J. Test 2"),
        "[Catalogue]": citations.Source("[Catalogue]", ("Compiler",), None, "The Catalogue"),
    }
    return citations.Register(
        evidence=evidence, results=results, sources=sources, names={"A. Finder": "Finder"}
    )


def _synthetic_case(
    lower: list[str], *, found_by: list[str] | None = None, certificate: bool = False
) -> dict[str, Any]:
    """One case: a reported construction at 2.5 under a grid ceiling of 3.

    With `certificate`, this project has certified that construction at its own value,
    which is what makes the bound `verified` without making it this project's bound.
    """
    verified_upper = (
        {"value": "2.5", "exact_form": None, "evidence": ["E-certificate"]}
        if certificate
        else {"value": "3", "exact_form": "3", "evidence": ["E-grid"]}
    )
    return {
        "reported_upper_bound": {
            "value": "2.5",
            "exact_form": None,
            "found_by": found_by or [],
            "found_year": 1999 if found_by else None,
            "improved_by": [],
            "source_key": "[Catalogue]",
            "evidence": ["E-catalogue"],
        },
        "verified_upper_bound": verified_upper,
        "verified_lower_bound": {"value": "2.25", "exact_form": None, "evidence": lower},
    }


def test_a_bound_from_common_knowledge_alone_has_no_line() -> None:
    register = _synthetic_register()
    assert citations.lower_citation(7, _synthetic_case(["E-area"]), register) is None


def test_a_published_bound_and_its_replay_cite_the_one_source_and_name_the_replay() -> None:
    """The replay is this project's, so it confirms the source's bound rather than owning it."""
    register = _synthetic_register()
    line = citations.lower_citation(7, _synthetic_case(["E-paper", "E-replay"]), register)
    assert line == {
        "text": "Author 2001, J. Test 1",
        "note": "(confirmed T-901)",
        "basis": "external",
        "assurance": "verified",
        "source_key": "[Paper 2001]",
        "result": None,
        # T-902 cites the source's own proof: relevant to the bound, confirming nothing.
        "results": ["T-901", "T-902"],
        "confirmed_by": ["T-901"],
        "value": "2.25",
    }


def test_a_published_bound_with_no_replay_here_carries_no_confirmation() -> None:
    register = _synthetic_register()
    line = citations.lower_citation(7, _synthetic_case(["E-paper"]), register)
    assert line is not None
    assert line["text"] == "Author 2001, J. Test 1"
    assert (line["results"], line["confirmed_by"]) == (["T-902"], [])


def test_a_result_at_another_n_is_not_this_n_s_confirmation() -> None:
    register = _synthetic_register()
    line = citations.lower_citation(8, _synthetic_case(["E-paper", "E-replay"]), register)
    assert line is not None
    # T-903 carries the same replay but is scoped to n = 8; at n = 7 it says nothing.
    assert (line["results"], line["confirmed_by"]) == (["T-903"], ["T-903"])


def test_two_published_sources_behind_one_bound_fail_rather_than_choosing() -> None:
    register = _synthetic_register()
    with pytest.raises(ValueError, match="names 2 sources"):
        citations.lower_citation(7, _synthetic_case(["E-paper", "E-other"]), register)


def test_a_novel_first_party_bound_cites_this_project_and_its_result() -> None:
    register = _synthetic_register()
    line = citations.lower_citation(7, _synthetic_case(["E-ours", "E-paper"]), register)
    assert line is not None
    assert (line["text"], line["basis"], line["result"], line["source_key"]) == (
        "This project 2026, result T-900",
        "project",
        "T-900",
        None,
    )
    # Our own bound is established, not confirmed, and the source's own result is not ours.
    assert (line["results"], line["confirmed_by"]) == (["T-900"], [])


def test_a_novel_bound_no_result_carries_for_this_n_fails() -> None:
    register = _synthetic_register()
    with pytest.raises(ValueError, match=r"carried by results \[\]"):
        citations.lower_citation(8, _synthetic_case(["E-ours"]), register)


def test_a_reported_construction_above_a_certified_grid_is_cited_as_reported() -> None:
    register = _synthetic_register()
    credited = citations.upper_citation(
        7, _synthetic_case(["E-area"], found_by=["A. Finder"]), register
    )
    assert _line(credited) == ("Finder 1999, The Catalogue (reported)", "external", "reported")
    uncredited = citations.upper_citation(7, _synthetic_case(["E-area"]), register)
    assert _line(uncredited) == ("Compiler, The Catalogue (reported)", "external", "reported")


def test_our_certificate_of_someone_else_s_packing_confirms_it_and_does_not_own_it() -> None:
    """`n = 29`'s shape: the certificate is scored new, the construction is not ours."""
    register = _synthetic_register()
    line = citations.upper_citation(
        7, _synthetic_case(["E-area"], found_by=["A. Finder"], certificate=True), register
    )
    assert line is not None
    assert (line["text"], line["note"], line["basis"], line["assurance"]) == (
        "Finder 1999, The Catalogue",
        "(confirmed T-910)",
        "external",
        "verified",
    )
    assert (line["results"], line["confirmed_by"], line["result"]) == (
        ["T-910"],
        ["T-910"],
        None,
    )


def test_a_confirmation_that_would_not_fit_falls_back_to_the_short_venue() -> None:
    register = _synthetic_register()
    sources = {
        **register.sources,
        "[Paper 2001]": citations.Source(
            "[Paper 2001]", ("Author",), 2001, "V" * 40, short_venue="Short J."
        ),
    }
    narrow = citations.Register(register.evidence, register.results, sources, register.names)
    confirmed = citations.lower_citation(7, _synthetic_case(["E-paper", "E-replay"]), narrow)
    assert confirmed is not None
    assert (confirmed["text"], confirmed["note"]) == (
        "Author 2001, Short J.",
        "(confirmed T-901)",
    )
    # Without the confirmation the full venue still fits, so it is what the line prints.
    plain = citations.lower_citation(7, _synthetic_case(["E-paper"]), narrow)
    assert plain is not None
    assert plain["text"] == "Author 2001, " + "V" * 40


def test_a_line_wider_than_the_stage_fails_rather_than_being_cut() -> None:
    register = _synthetic_register()
    long_venue = {
        **register.sources,
        "[Paper 2001]": citations.Source("[Paper 2001]", ("Author",), 2001, "V" * 60),
    }
    wide = citations.Register(register.evidence, register.results, long_venue, register.names)
    with pytest.raises(ValueError, match="over 66"):
        citations.lower_citation(7, _synthetic_case(["E-paper"]), wide)


def test_several_confirmations_are_named_in_id_order() -> None:
    source = citations.Source("[K]", ("Author",), 2001, "J. Test 1")
    assert citations.compose("Author", 2001, source, citations.TEXT_LIMIT) == (
        "Author 2001, J. Test 1"
    )
    assert citations.note("verified", ["T-009", "T-011"]) == "(confirmed T-009, T-011)"
    assert citations.result_order("T-032") == 32


def test_the_one_aside_says_both_things_where_both_are_true() -> None:
    """`n = 29`'s shape again, and the reason the note exists: the register reports the bound
    and a result of ours confirms it, which used to be drawn as two marks in two styles."""
    assert citations.note("reported", []) == "(reported)"
    assert citations.note("verified", ["T-009"]) == "(confirmed T-009)"
    assert citations.note("reported", ["T-009"]) == "(reported; confirmed T-009)"
    assert citations.note("verified", []) is None


def test_the_width_a_line_is_checked_against_counts_its_note() -> None:
    """The note used to be drawn outside the count, so a line could pass and overflow."""
    register = _synthetic_register()
    sources = {
        **register.sources,
        "[Paper 2001]": citations.Source("[Paper 2001]", ("Author",), 2001, "V" * 53),
    }
    wide = citations.Register(register.evidence, register.results, sources, register.names)
    # `Author 2001, ` and 53 of venue is exactly the limit with no note.
    plain = citations.lower_citation(7, _synthetic_case(["E-paper"]), wide)
    assert plain is not None
    assert len(citations.drawn(plain)) == citations.TEXT_LIMIT
    # The same line with a confirmation does not fit, and there is no short venue to fall to.
    with pytest.raises(ValueError, match="over 66"):
        citations.lower_citation(7, _synthetic_case(["E-paper", "E-replay"]), wide)


# ------------------------------------------------------------ over the recorded register

#: Lines the recorded register gives, chosen from cases whose sources are settled. Each is
#: (upper, lower) as (text, basis, assurance), or None where the line is omitted.
RECORDED: dict[int, tuple[tuple[str, str, str] | None, tuple[str, str, str] | None]] = {
    # The area bound and a trivial tiling: nothing is owed a citation.
    1: (None, None),
    # Center counting below, the grid above.
    2: (None, None),
    5: (
        ("Göbel 1979, Squares in Squares", "external", "verified"),
        ("Göbel 1979, Math. Centre Tracts 106", "external", "verified"),
    ),
    # The grid ceiling is derived whoever the catalogue credits (think-dlof).
    6: (None, ("Kearney & Shiu 2002, Electron. J. Combin. 9, #R14", "external", "verified")),
    # What the register verified, not the earlier reported proof (the owner, 2026-09-22).
    7: (None, ("Nagamochi 2005, Electron. J. Combin. 12, #R37", "external", "verified")),
    10: (
        ("Göbel 1979, Squares in Squares", "external", "verified"),
        ("Stromquist 2003, Electron. J. Combin. 10, #R8", "external", "verified"),
    ),
    13: (None, ("Bentz 2010, Electron. J. Combin. 17, #R126", "external", "verified")),
    22: (None, ("Bentz 2016, arXiv:1606.03746", "external", "verified")),
    # A published proof and this project's audit of it are one source's bound, and the
    # audit's two results are named on the line; the article number gives way so they fit.
    46: (
        None,
        (
            "Bentz 2010, Electron. J. Combin. 17 (confirmed T-004, T-008)",
            "external",
            "verified",
        ),
    ),
    68: (
        ("UnitSquare Project 2026, Results Release 1 (reported)", "external", "reported"),
        ("wand125 2026, GitHub", "external", "verified"),
    ),
    # The catalogue credits nobody, so the line cites the catalogue by its compilers.
    101: (
        ("Friedman & Ellsworth, Squares in Squares (reported)", "external", "reported"),
        ("Nagamochi 2005, Electron. J. Combin. 12, #R37", "external", "verified"),
    ),
    # Three finders and two improvers: the first and et al., and no year.
    132: (
        ("Arslanov et al., Squares in Squares (reported)", "external", "reported"),
        ("Nagamochi 2005, Electron. J. Combin. 12, #R37", "external", "verified"),
    ),
}


@pytest.mark.parametrize("n", sorted(RECORDED))
def test_the_recorded_register_gives_these_lines(n: int) -> None:
    entry = _entry(n)
    assert (_line(entry["upper"]), _line(entry["lower"])) == RECORDED[n]


@pytest.mark.parametrize(
    ("n", "author"),
    [(11, "Kleddamag"), (17, "Guzhou0806"), (26, "Tokoharu"), (29, "Tokoharu")],
)
def test_promoted_external_bounds_keep_the_sources_credit(n: int, author: str) -> None:
    lower = _entry(n)["lower"]
    assert _line(lower) == (f"{author} 2026, GitHub", "external", "verified")
    assert lower["result"] is None
    assert lower["confirmed_by"] == []


def test_n29_credits_finder_and_optimizer_and_takes_the_registers_verdict() -> None:
    """`n = 29` is where the catalogue's truncated decimal meets T-009's certificate.

    Its assurance is whatever `bounds_agree_at_declared_precision` says, as for every other
    case; this test names it so a change of that rule is seen here, not special-cased. The
    certificate is scored new and the packing is still Schadt and Ellsworth's, so T-009
    confirms the bound and does not make it this project's.
    """
    case = citations.load_case(29)
    upper = _entry(29)["upper"]
    # The one bound that is both reported and confirmed, and so the one line that says both.
    assert upper["text"] == "Schadt & Ellsworth, Squares in Squares"
    assert upper["note"] == "(reported; confirmed T-009)"
    assert (upper["basis"], upper["confirmed_by"]) == ("external", ["T-009"])
    agrees = bounds_agree_at_declared_precision(
        case["reported_upper_bound"], case["verified_upper_bound"]
    )
    assert upper["assurance"] == ("verified" if agrees else "reported")


#: What this project has recorded about a recorded bound: (results, confirmed_by).
RECORDED_LINKS: dict[tuple[int, str], tuple[list[str], list[str]]] = {
    # Trump's packing, exactly replayed here.
    (11, "upper"): (["T-011"], ["T-011"]),
    # The audit of Bentz's Theorem 8, and the equality it settles.
    (46, "lower"): (["T-004", "T-008"], ["T-004", "T-008"]),
    # Two results cite Bentz 2010 at n = 13 -- one of them says a lemma is false as
    # printed -- and neither replays the bound, so neither confirms it.
    (13, "lower"): (["T-005", "T-006"], []),
    # The register records Nagamochi's theorem below 100 without replaying it.
    (7, "lower"): (["T-007"], []),
    (101, "lower"): ([], []),
    # This project's own bound: established, not confirmed.
    (18, "lower"): (["T-030"], []),
}


@pytest.mark.parametrize(("n", "label"), sorted(RECORDED_LINKS))
def test_the_recorded_register_links_these_results(n: int, label: str) -> None:
    line = _entry(n)[label]
    assert line is not None
    assert (line["results"], line["confirmed_by"]) == RECORDED_LINKS[(n, label)]


# ------------------------------------------------------------------------- the contract


def test_the_committed_record_is_current() -> None:
    citations.check()


def test_the_record_and_the_bibliography_validate_against_their_schemas() -> None:
    assert validate_schemas.check(citations.RECORD) == []
    assert validate_schemas.check(citations.BIBLIOGRAPHY) == []
    assert citations.RECORD in validate_schemas.corpus_paths()[1]
    assert citations.BIBLIOGRAPHY in validate_schemas.corpus_paths()[1]


def test_one_entry_per_case_in_order() -> None:
    assert [entry["n"] for entry in _record()["entries"]] == list(citations.CORPUS.numbers)
    assert _record()["generated_by"] == citations.GENERATOR


def test_every_entry_names_the_frontier_record_it_comes_from() -> None:
    """Including the cases whose two lines are both left out; the stage draws it per n."""
    for entry in _record()["entries"]:
        assert entry["record"] == f"n-{entry['n']:03d}"
        assert (citations.FRONTIER / f"{entry['record']}.md").is_file()


def _bound_evidence(n: int, label: str) -> list[str]:
    """The evidence the bound the stage shows rests on, as the case records it."""
    case = citations.load_case(n)
    if label == "lower":
        return [str(item) for item in case["verified_lower_bound"]["evidence"]]
    return [
        str(item)
        for item in (
            *case["reported_upper_bound"]["evidence"],
            *case["verified_upper_bound"]["evidence"],
        )
    ]


def test_every_listed_result_carries_the_bounds_own_evidence_for_this_n() -> None:
    """The links are the register's, not a list: each is re-derived here from it."""
    evidence = _register().evidence
    results = {str(result["id"]): result for result in _register().results}
    seen = 0
    for entry in _record()["entries"]:
        for label in ("upper", "lower"):
            line = entry[label]
            if line is None:
                continue
            own = {
                item
                for item in _bound_evidence(entry["n"], label)
                if evidence[item].get("novelty") != "common-knowledge"
            }
            assert line["results"] == sorted(line["results"], key=citations.result_order)
            assert set(line["confirmed_by"]) <= set(line["results"])
            for identifier in line["results"]:
                result = results[identifier]
                assert citations.in_scope(result["scope"], entry["n"]), (entry["n"], identifier)
                shared = own & set(result["evidence"])
                assert shared, (entry["n"], identifier)
                seen += 1
                if identifier in line["confirmed_by"]:
                    # A confirmation is work this project did: a replay, an audit, a
                    # certificate. A result that only cites the source's proof is not one.
                    assert any(
                        evidence[item].get("performed_by") == "repository" for item in shared
                    ), (entry["n"], identifier)
    assert seen


def test_a_project_line_is_established_rather_than_confirmed() -> None:
    for entry in _record()["entries"]:
        for label in ("upper", "lower"):
            line = entry[label]
            if line is None or line["basis"] != "project":
                continue
            assert line["confirmed_by"] == []
            assert line["result"] in line["results"]


def test_the_line_names_exactly_the_results_that_confirm_it() -> None:
    for entry in _record()["entries"]:
        for label in ("upper", "lower"):
            line = entry[label]
            if line is None:
                continue
            if line["confirmed_by"]:
                named = f"confirmed {', '.join(line['confirmed_by'])}"
                assert (line["note"] or "").endswith(f"{named})"), (entry["n"], label)
            else:
                assert "confirmed" not in (line["note"] or ""), (entry["n"], label)
            # The reference says where the bound comes from and never what we did with it.
            assert "confirmed" not in line["text"], (entry["n"], label)
            assert "reported" not in line["text"], (entry["n"], label)


def test_every_value_is_the_one_the_composite_draws() -> None:
    composite = _composite()
    for entry in _record()["entries"]:
        figure = composite[entry["n"]]
        if entry["upper"] is not None:
            assert entry["upper"]["value"] == figure["side"]["value"], entry["n"]
        if entry["lower"] is not None:
            assert entry["lower"]["value"] == figure["lower"]["value"], entry["n"]


def test_the_project_lower_bounds_are_exactly_the_starred_cases() -> None:
    starred = {n for n, figure in _composite().items() if figure["lower"]["first_proved_here"]}
    project = {
        entry["n"]
        for entry in _record()["entries"]
        if entry["lower"] is not None and entry["lower"]["basis"] == "project"
    }
    assert project == starred
    assert starred  # an empty set would pass vacuously


def test_a_project_line_names_the_result_that_carries_its_evidence() -> None:
    results = {str(result["id"]): result for result in _register().results}
    for entry in _record()["entries"]:
        line = entry["lower"]
        if line is None or line["basis"] != "project":
            continue
        result = results[line["result"]]
        year = str(result["significance"]["scored"])[:4]
        assert line["text"] == f"This project {year}, result {line['result']}"
        evidence = citations.load_case(entry["n"])["verified_lower_bound"]["evidence"]
        novel = {
            item
            for item in evidence
            if citations.is_novel_first_party(_register().evidence[item], "lower-bound")
        }
        assert novel <= set(result["evidence"]), entry["n"]
        assert citations.in_scope(result["scope"], entry["n"]), entry["n"]


def test_an_upper_bound_is_verified_exactly_where_the_register_certifies_it() -> None:
    """The same function the case checks and the certified-upper tripwire use."""
    for entry in _record()["entries"]:
        if entry["upper"] is None:
            continue
        case = citations.load_case(entry["n"])
        agrees = bounds_agree_at_declared_precision(
            case["reported_upper_bound"], case["verified_upper_bound"]
        )
        assert entry["upper"]["assurance"] == ("verified" if agrees else "reported"), entry["n"]


def test_an_omitted_line_is_one_the_register_derives_from_common_knowledge() -> None:
    evidence = _register().evidence
    for entry in _record()["entries"]:
        case = citations.load_case(entry["n"])
        if entry["lower"] is None:
            cited = case["verified_lower_bound"]["evidence"]
            assert all(evidence[i]["novelty"] == "common-knowledge" for i in cited), entry["n"]
        if entry["upper"] is None:
            cited = case["verified_upper_bound"]["evidence"]
            assert all(evidence[i]["novelty"] == "common-knowledge" for i in cited), entry["n"]
            assert bounds_agree_at_declared_precision(
                case["reported_upper_bound"], case["verified_upper_bound"]
            ), entry["n"]


def test_every_line_fits_the_stage() -> None:
    for entry in _record()["entries"]:
        for label in ("upper", "lower"):
            line = entry[label]
            if line is not None:
                assert len(line["text"]) <= citations.TEXT_LIMIT, (entry["n"], label)


def test_every_cited_source_key_resolves_in_the_bibliography_and_the_archive_index() -> None:
    sources = _register().sources
    cited = {
        entry[label]["source_key"]
        for entry in _record()["entries"]
        for label in ("upper", "lower")
        if entry[label] is not None and entry[label]["source_key"] is not None
    }
    assert cited
    assert cited <= set(sources)
    assert cited <= _defined_keys()


def test_the_review_accounts_for_every_omission() -> None:
    cases = {n: citations.load_case(n) for n in citations.CORPUS.numbers}
    report = citations.omissions(_record()["entries"], cases)
    omitted = {entry["n"] for entry in _record()["entries"] if entry["upper"] is None}
    assert set(report["upper omitted: the certified grid"]) == omitted
    assert report["lower omitted: common-knowledge evidence alone"] == [
        entry["n"] for entry in _record()["entries"] if entry["lower"] is None
    ]


# ------------------------------------------------------------------ the bibliography


def test_every_bibliography_key_is_defined_in_the_archive_index() -> None:
    assert set(_register().sources) <= _defined_keys()


def test_a_papers_year_and_authors_agree_with_the_papers_table() -> None:
    """Two statements of one fact; the README's table is the one a reader checks."""
    papers = _papers_table()
    bibliography = safe_load(citations.BIBLIOGRAPHY.read_text(encoding="utf-8"))["sources"]
    checked = 0
    for source in bibliography:
        row = papers.get(source["key"])
        if row is None:
            # A web source's authors are in no table, so it must say where they were read.
            assert source.get("note"), source["key"]
            continue
        checked += 1
        assert row["year"] == str(source["year"]), source["key"]
        for surname in source["authors"]:
            assert surname in row["authors"], (source["key"], surname)
    assert checked


# -------------------------------------------------------- source keys across the register


def _register_source_keys() -> dict[str, set[str]]:
    """Every source key the frontier register names, with where it names it."""
    keys: dict[str, set[str]] = {}

    def note(key: object, where: str) -> None:
        if key is not None:
            keys.setdefault(str(key), set()).add(where)

    for entry in _register().evidence.values():
        note(entry.get("source_key"), str(entry["id"]))
    for n in citations.CORPUS.numbers:
        case = citations.load_case(n)
        for field in ("reported_upper_bound", "reported_lower_bound"):
            note(case[field].get("source_key"), f"n-{n:03d} {field}")
        for resource in case.get("resources") or []:
            # A resource outside the archive is one of this repository's own witnesses,
            # found by its path rather than by an entry in the archive index.
            if not str(resource.get("local") or "").startswith("../"):
                note(resource["key"], f"n-{n:03d} resources")
    return keys


def test_every_source_key_the_register_uses_is_defined_once_spelled() -> None:
    """`think-dlof`: a key the archive index does not define is a dangling citation.

    A result id written as a key, `[T-017]`, is this repository's own result and resolves
    in the results register instead.
    """
    results = {str(result["id"]) for result in _register().results}
    undefined = {}
    for key, where in _register_source_keys().items():
        own_result = RESULT_KEY.match(key)
        if own_result is not None:
            if own_result.group(1) not in results:
                undefined[key] = sorted(where)
        elif key not in _defined_keys():
            undefined[key] = sorted(where)
    assert undefined == {}
