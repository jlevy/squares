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
from datetime import date
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
        # This project's replay of the later source's own route to the same bound.
        "E-other-replay": {
            "claim": "lower-bound",
            "performed_by": "repository",
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
        # The later source's route, replayed here.
        {"id": "T-904", "scope": {"n_values": [7]}, "evidence": ["E-other-replay"], **SCORED},
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
        # The synthetic source is from 2001, so the bound is not a recent result.
        "recent": False,
        # No result behind it says it corrects a published one.
        "corrects": None,
    }


def test_a_sources_credit_is_printed_in_place_of_its_joined_authors() -> None:
    """A joint credit with the lineage is the source's own, and is printed whole.

    Three or more names would fold into "et al.", which is exactly the lineage the credit
    exists to name; `credit` keeps it, and the width check still applies.
    """
    register = _synthetic_register()
    credited = citations.Source(
        "[Paper 2001]", ("Author",), 2001, "J. Test 1", credit="Author after A, B, C"
    )
    register = citations.Register(
        evidence=register.evidence,
        results=register.results,
        sources={**register.sources, "[Paper 2001]": credited},
        names=register.names,
    )
    line = citations.lower_citation(7, _synthetic_case(["E-paper"]), register)
    assert line is not None
    assert line["text"] == "Author after A, B, C 2001, J. Test 1"
    assert citations.Source("[K]", ("A", "B", "C"), 2001, "J").credited == "A et al."


def test_a_credit_whose_line_would_not_fit_fails_before_any_case_cites_it() -> None:
    """The width is checked on the credit's own line, year and venue included."""
    fits = "K" * (citations.TEXT_LIMIT - len(" 2026, GitHub"))
    citations.check_credits([citations.Source("[K]", ("K",), 2026, "GitHub", credit=fits)])
    with pytest.raises(ValueError, match="67 characters, over 66"):
        citations.check_credits(
            [citations.Source("[K]", ("K",), 2026, "GitHub", credit=fits + "K")]
        )


def test_a_short_credit_is_the_authors_and_a_prefix_of_the_links() -> None:
    """The stage may drop links from the end of a credit, and nothing else.

    Longest first, at least one link kept, never all of them: `Tokoharu et al.` would read
    as coauthors, and a shortening that kept every link would say `et al.` of nobody.
    """
    full = "Tokoharu after Levy, wand125, Stromquist"
    assert citations.short_credits(full) == [
        "Tokoharu after Levy, wand125 et al.",
        "Tokoharu after Levy et al.",
    ]
    assert citations.short_credits("Guzhou0806, Mira after Levy, Burns") == [
        "Guzhou0806, Mira after Levy et al."
    ]
    assert citations.short_credits("Kleddamag after Levy") == []
    assert citations.short_credits("Daniel") == []


@pytest.mark.parametrize(
    ("credit", "short"),
    [
        ("Guzhou0806, Mira after Levy, Burns", "Guzhou0806 after Levy et al."),
        ("Tokoharu after Levy, wand125, Burns", "Tokoharu after wand125, Levy et al."),
        ("Tokoharu after Levy, wand125, Burns", "Tokoharu after Levy, Mira et al."),
        ("Tokoharu after Levy, wand125, Burns", "Tokoharu after Levy, wand125"),
        ("Tokoharu after Levy, wand125, Burns", "Tokoharu et al."),
        ("Tokoharu after Levy, wand125", "Tokoharu after Levy, wand125 et al."),
        ("Kleddamag after Levy", "Kleddamag after Levy et al."),
    ],
    ids=[
        "drops-an-author",
        "reorders-the-links",
        "names-a-link-the-credit-does-not",
        "shortens-without-saying-so",
        "keeps-no-link-and-reads-as-coauthors",
        "keeps-every-link-and-says-et-al-of-nobody",
        "shortens-a-one-link-credit",
    ],
)
def test_a_short_credit_that_misstates_the_credit_fails(credit: str, short: str) -> None:
    source = citations.Source("[K]", ("K",), 2026, "GitHub", credit=credit, short_credit=short)
    with pytest.raises(ValueError, match="is not the credit's authors"):
        citations.check_short_credit(source)


def test_a_short_credit_needs_a_credit_to_shorten() -> None:
    source = citations.Source("[K]", ("K",), 2026, "GitHub", short_credit="K after A et al.")
    with pytest.raises(ValueError, match="does not have"):
        citations.check_credits([source])


def test_a_credit_too_wide_for_the_stage_needs_a_short_credit_that_fits() -> None:
    """The whole credit may run past the stage; the line the stage would print may not."""
    links = ", ".join(f"Link{index:02d}" for index in range(10))
    wide = f"Author after {links}"
    assert len(citations.cite(wide, 2026, "GitHub")) > citations.TEXT_LIMIT
    with pytest.raises(ValueError, match="gives no `short_credit`"):
        citations.check_credits([citations.Source("[K]", ("K",), 2026, "GitHub", credit=wide)])
    fits = "Author after Link00, Link01 et al."
    citations.check_credits(
        [citations.Source("[K]", ("K",), 2026, "GitHub", credit=wide, short_credit=fits)]
    )
    too_wide = citations.short_credits(wide)[0]
    with pytest.raises(ValueError, match="short credit line"):
        citations.check_credits(
            [
                citations.Source(
                    "[K]", ("K",), 2026, "GitHub", credit=wide, short_credit=too_wide
                )
            ]
        )


def _with_source(source: citations.Source) -> citations.Register:
    register = _synthetic_register()
    return citations.Register(
        evidence=register.evidence,
        results=register.results,
        sources={**register.sources, source.key: source},
        names=register.names,
    )


def test_the_stage_shortens_a_credit_only_where_the_whole_line_does_not_fit() -> None:
    """R068's shape: the whole credit fits alone, and the confirmation pushes it over.

    The citation names every link where there is room, and `et al.` where there is not;
    what every other renderer reads, `Source.credited`, stays whole either way.
    """
    credit = "Guzhou0806 after Kleddamag, Mira, Levy"
    source = citations.Source(
        "[Paper 2001]",
        ("Guzhou0806",),
        2001,
        "GitHub",
        credit=credit,
        short_credit="Guzhou0806 after Kleddamag et al.",
    )
    register = _with_source(source)
    plain = citations.lower_citation(7, _synthetic_case(["E-paper"]), register)
    assert plain is not None
    assert plain["text"] == f"{credit} 2001, GitHub"
    confirmed = citations.lower_citation(7, _synthetic_case(["E-paper", "E-replay"]), register)
    assert confirmed is not None
    assert len(f"{credit} 2001, GitHub (confirmed T-901)") > citations.TEXT_LIMIT
    assert (confirmed["text"], confirmed["note"]) == (
        "Guzhou0806 after Kleddamag et al. 2001, GitHub",
        "(confirmed T-901)",
    )
    assert source.credited == credit


def test_a_venue_gives_way_before_a_credit_does() -> None:
    """Who did the work outranks where it appeared: the short venue is tried first."""
    source = citations.Source(
        "[K]",
        ("Author",),
        2001,
        "V" * 30,
        short_venue="Short J.",
        credit="Author after Alpha, Beta, Gamma",
        short_credit="Author after Alpha et al.",
    )
    whole = "Author after Alpha, Beta, Gamma 2001, Short J."
    assert citations.compose(source.credit, 2001, source, len(whole), source.short_credit) == (
        whole
    )
    # One character less, and neither venue carries the whole credit: the short credit
    # is tried with the full venue, which is too wide, and then with the short one.
    assert citations.compose(
        source.credit, 2001, source, len(whole) - 1, source.short_credit
    ) == ("Author after Alpha et al. 2001, Short J.")


def test_a_stale_record_names_the_lines_that_moved() -> None:
    """The atlas is re-rendered once for many bibliography edits; the check says which."""
    line = {"text": "Author 2001, J. Test 1", "note": "(confirmed T-901)", "value": "2.25"}

    def record(lower: dict[str, str]) -> dict[str, Any]:
        return {"entries": [{"n": 7, "upper": None, "lower": lower}]}

    moved = {**line, "text": "Author after A et al. 2001, J. Test 1"}
    was = "'Author 2001, J. Test 1 (confirmed T-901)'"
    assert citations.stale_lines(record(line), record(line)) == []
    assert citations.stale_lines(record(line), record(moved)) == [
        f"n=7 lower: {was} -> 'Author after A et al. 2001, J. Test 1 (confirmed T-901)'"
    ]
    assert citations.stale_lines(record(line), record({**line, "value": "2.5"})) == [
        f"n=7 lower: {was}, fields ['value'] changed"
    ]


#: Names an AI agent goes by. The owner's rule (2026-09-27): no agent is ever a credited
#: author; a release's use of one belongs in its provenance note, not in `credit`.
AGENT_NAMES = re.compile(r"codex|openai|claude|anthropic|gpt|gemini|copilot", re.IGNORECASE)


def test_every_recorded_credit_fits_the_stage_in_latin_letters_and_names_no_agent() -> None:
    """Every `credit` and `short_credit` in the bibliography, on the stage today or not."""
    joint = {
        (source.key, text)
        for source in _register().sources.values()
        for text in (source.credit, source.short_credit)
        if text is not None
    }
    assert joint
    citations.check_credits(_register().sources.values())
    for key, credit in joint:
        assert credit.isascii(), key
        assert credit.isprintable(), key
        assert not AGENT_NAMES.search(credit), key


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
    # Replays of two sources and no published proof leave the credit to choose, too.
    with pytest.raises(ValueError, match="names 2 sources"):
        citations.lower_citation(7, _synthetic_case(["E-replay", "E-other-replay"]), register)


def test_a_later_routes_replay_beside_the_first_proof_confirms_it() -> None:
    """The shape of n = 13 and n = 33 since 2026-10-06: Bentz's proof, and beside it the
    replays here of Daniel's later proof of the same value. The line credits the source
    whose own proof the lane cites, and the result carrying the replay confirms it
    (`first_source`)."""
    register = _synthetic_register()
    line = citations.lower_citation(7, _synthetic_case(["E-paper", "E-other-replay"]), register)
    assert line is not None
    assert (line["text"], line["note"], line["source_key"]) == (
        "Author 2001, J. Test 1",
        "(confirmed T-904)",
        "[Paper 2001]",
    )
    assert (line["results"], line["confirmed_by"], line["recent"]) == (
        ["T-902", "T-904"],
        ["T-904"],
        False,
    )


def test_a_novel_first_party_bound_cites_this_project_and_its_result() -> None:
    register = _synthetic_register()
    line = citations.lower_citation(7, _synthetic_case(["E-ours", "E-paper"]), register)
    assert line is not None
    assert (line["text"], line["basis"], line["result"], line["source_key"]) == (
        "Squares Project (Levy) 2026, result T-900",
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


@pytest.mark.parametrize("verified_value", ["2.75", "2.5"])
def test_an_earlier_certificate_confirms_only_the_displayed_upper_value(
    verified_value: str,
) -> None:
    register = _synthetic_register()
    case = _synthetic_case(["E-area"], certificate=True)
    case["reported_upper_bound"]["exact_form"] = "5/2"
    case["verified_upper_bound"]["value"] = verified_value
    case["verified_upper_bound"]["exact_form"] = "5/2" if verified_value == "2.5" else "11/4"
    before = json.dumps(case, sort_keys=True)
    line = citations.upper_citation(7, case, register)
    assert line is not None
    assert line["value"] == "2.5"
    # Earlier evidence and its result link survive even when it certifies a weaker bound.
    assert line["results"] == ["T-910"]
    assert json.dumps(case, sort_keys=True) == before
    if verified_value == "2.5":
        assert line["confirmed_by"] == ["T-910"]
        assert (line["note"], line["assurance"]) == ("(confirmed T-910)", "verified")
    else:
        assert line["confirmed_by"] == []
        assert (line["note"], line["assurance"]) == ("(reported)", "reported")


@pytest.mark.parametrize("n", [123, 126, 129, 154, 155, 179, 208, 237, 238, 239, 258, 263])
def test_the_selected_squish_update_does_not_inherit_earlier_confirmation(n: int) -> None:
    case = citations.load_case(n)
    # Hold the earlier verified lane independently of whether the live update has
    # since been confirmed. These are the actual twelve pre-confirmation bounds.
    previous = json.loads(
        (ROOT / "tests/fixtures/squish-update-prior-verified.json").read_text()
    )
    case["verified_upper_bound"] = previous[str(n)]
    assert case["reported_upper_bound"]["source_key"] == "[SQUISH update 2026-10-07]"
    assert not bounds_agree_at_declared_precision(
        case["reported_upper_bound"], case["verified_upper_bound"]
    )
    upper = citations.upper_citation(n, case, _register())
    assert upper is not None
    assert upper["value"] == case["reported_upper_bound"]["value"]
    assert upper["confirmed_by"] == []
    assert (upper["note"], upper["assurance"]) == ("(reported)", "reported")


@pytest.mark.parametrize("n", [123, 126, 129, 154, 155, 179, 208, 237, 238, 239, 258, 263])
def test_the_confirmed_squish_update_cites_only_its_matching_result(n: int) -> None:
    case = citations.load_case(n)
    assert bounds_agree_at_declared_precision(
        case["reported_upper_bound"], case["verified_upper_bound"]
    )
    upper = _entry(n)["upper"]
    assert upper["value"] == case["verified_upper_bound"]["value"]
    assert upper["confirmed_by"] == ["T-115"]
    assert (upper["note"], upper["assurance"]) == ("(confirmed T-115)", "verified")


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
    long_credit = {
        **register.sources,
        "[Paper 2001]": citations.Source("[Paper 2001]", ("A" * 70,), 2001, "V" * 60),
    }
    wide = citations.Register(register.evidence, register.results, long_credit, register.names)
    with pytest.raises(ValueError, match="over 66"):
        citations.lower_citation(7, _synthetic_case(["E-paper"]), wide)


def test_a_venue_goes_before_the_line_fails() -> None:
    """Where neither venue leaves room, the credit and year stand alone; the credit is
    never cut to keep a venue."""
    register = _synthetic_register()
    long_venue = {
        **register.sources,
        "[Paper 2001]": citations.Source("[Paper 2001]", ("Author",), 2001, "V" * 60),
    }
    wide = citations.Register(register.evidence, register.results, long_venue, register.names)
    line = citations.lower_citation(7, _synthetic_case(["E-paper"]), wide)
    assert line is not None
    assert line["text"] == "Author 2001"
    source = citations.Source("[K]", ("Author",), 2001, "V" * 30, short_venue="Short J.")
    assert citations.compose("Author", 2001, source, len("Author 2001, Short J.")) == (
        "Author 2001, Short J."
    )
    assert citations.compose("Author", 2001, source, len("Author 2001, Short J.") - 1) == (
        "Author 2001"
    )


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
    # The same line with a confirmation does not fit, and there is no short venue to fall
    # to, so the venue goes and the credit and year stand alone beside the note.
    confirmed = citations.lower_citation(7, _synthetic_case(["E-paper", "E-replay"]), wide)
    assert confirmed is not None
    assert (confirmed["text"], confirmed["note"]) == ("Author 2001", "(confirmed T-901)")
    assert len(citations.drawn(confirmed)) <= citations.TEXT_LIMIT


#: A published work a synthetic bound corrects, and the register's record of it.
FLAWED = {"source_key": "[Flawed 1990]", "result": "T-899", "what": "its lemma is false"}


def _correcting_register(*correcting: tuple[str, dict[str, str]]) -> citations.Register:
    """The synthetic register with a flawed 1990 paper in its bibliography, and with each
    named result saying it corrects the given work."""
    register = _synthetic_register()
    named = dict(correcting)
    results = [
        {**result, "corrects": named[result["id"]]} if result["id"] in named else result
        for result in register.results
    ]
    sources = {
        **register.sources,
        "[Flawed 1990]": citations.Source("[Flawed 1990]", ("Flawed",), 1990, "J. X"),
    }
    return citations.Register(register.evidence, results, sources, register.names)


def test_a_bound_whose_results_correct_a_published_work_names_that_work() -> None:
    """The tag is read from the results the line lists, never from its source key: the
    replay T-901 says it corrects the flawed paper, so the line carries that work's key,
    its short citation as the bibliography prints it, and the register's record of it."""
    register = _correcting_register(("T-901", FLAWED))
    line = citations.lower_citation(7, _synthetic_case(["E-paper", "E-replay"]), register)
    assert line is not None
    assert line["corrects"] == {
        "source_key": "[Flawed 1990]",
        "credit": "Flawed 1990",
        "result": "T-899",
    }
    assert citations.corrects_tag(line["corrects"]) == "corrects Flawed 1990"
    # Set between the reference and the note, and the recency is untouched by it.
    assert citations.drawn(line) == (
        "Author 2001, J. Test 1 corrects Flawed 1990 (confirmed T-901)"
    )
    assert line["recent"] is False
    # An upper line carries neither field: both are the lower bound's alone.
    upper = citations.upper_citation(
        7, _synthetic_case(["E-paper"], certificate=True), register
    )
    assert upper is not None
    assert "corrects" not in upper
    assert "recent" not in upper


def test_a_project_bound_that_corrects_a_published_work_says_so_too() -> None:
    register = _correcting_register(("T-900", FLAWED))
    line = citations.lower_citation(7, _synthetic_case(["E-ours"]), register)
    assert line is not None
    assert line["basis"] == "project"
    assert line["recent"] is True
    assert line["corrects"] == {
        "source_key": "[Flawed 1990]",
        "credit": "Flawed 1990",
        "result": "T-899",
    }


def test_a_result_that_corrects_nothing_leaves_the_tag_off() -> None:
    """Only the results the line lists are asked: T-903 corrects the paper at n = 8, which
    is not this n, so the n = 7 line carries no tag."""
    register = _correcting_register(("T-903", FLAWED))
    line = citations.lower_citation(7, _synthetic_case(["E-paper", "E-replay"]), register)
    assert line is not None
    assert line["corrects"] is None
    assert citations.corrects_tag(None) is None


def test_two_results_naming_different_corrected_works_fail_rather_than_choosing() -> None:
    other = {"source_key": "[Other 2002]", "result": "T-898", "what": "also false"}
    register = _correcting_register(("T-901", FLAWED), ("T-902", other))
    with pytest.raises(ValueError, match="correct 2 published works"):
        citations.lower_citation(7, _synthetic_case(["E-paper", "E-replay"]), register)
    # Two results naming the same work are one tag.
    register = _correcting_register(("T-901", FLAWED), ("T-902", FLAWED))
    line = citations.lower_citation(7, _synthetic_case(["E-paper", "E-replay"]), register)
    assert line is not None
    assert line["corrects"]["result"] == "T-899"


def test_a_corrected_work_missing_from_the_bibliography_fails() -> None:
    register = _correcting_register(("T-901", {**FLAWED, "source_key": "[Nowhere 1980]"}))
    with pytest.raises(ValueError, match=r"\[Nowhere 1980\] is not in bibliography.yaml"):
        citations.lower_citation(7, _synthetic_case(["E-paper", "E-replay"]), register)


def test_the_width_a_line_is_checked_against_counts_its_correction() -> None:
    """The tag shares the stage's line with the reference and the note, so the reference
    gives way to it as it does to the note: here the venue falls to its short form."""
    register = _correcting_register(("T-901", FLAWED))
    sources = {
        **register.sources,
        "[Paper 2001]": citations.Source(
            "[Paper 2001]", ("Author",), 2001, "V" * 30, short_venue="Short"
        ),
    }
    wide = citations.Register(register.evidence, register.results, sources, register.names)
    line = citations.lower_citation(7, _synthetic_case(["E-paper", "E-replay"]), wide)
    assert line is not None
    assert line["text"] == "Author 2001, Short"
    assert len(citations.drawn(line)) <= citations.TEXT_LIMIT
    plain = citations.lower_citation(7, _synthetic_case(["E-paper"]), wide)
    assert plain is not None
    assert plain["text"] == f"Author 2001, {'V' * 30}"


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
    # chelokot's Lean theorem s(n^2 - 2) = n, replayed here (T-086), since 2026-10-02,
    # which stands in for Nagamochi's Theorem 2, so the line says it corrects that paper.
    7: (
        None,
        (
            "chelokot 2026, GitHub corrects Nagamochi 2005 (confirmed T-086)",
            "external",
            "verified",
        ),
    ),
    10: (
        ("Göbel 1979, Squares in Squares", "external", "verified"),
        ("Stromquist 2003, Electron. J. Combin. 10, #R8", "external", "verified"),
    ),
    # T-060 confirms the exact Trump lower bound; the narrow stage shortens its
    # lineage and venue, while the bibliography retains both in full.
    11: (
        ("Trump 1979, Squares in Squares (confirmed T-011)", "external", "verified"),
        (
            "Queuingtheorydotcom after Levy et al. 2026, Web (confirmed T-060)",
            "external",
            "verified",
        ),
    ),
    # Bentz's proofs, credited as the first, and since 2026-10-06 the replays of the later
    # routes beside them in the lane: Daniel's case-free cover of [0,4]^2 (T-006) and his
    # s(k^2 - 3) = k family (T-064), which confirm the bound (`first_source`).
    13: (
        None,
        (
            "Bentz 2010, Electron. J. Combin. 17, #R126 (confirmed T-006)",
            "external",
            "verified",
        ),
    ),
    22: (None, ("Bentz 2016, arXiv:1606.03746", "external", "verified")),
    33: (None, ("Bentz 2016, arXiv:1606.03746 (confirmed T-064)", "external", "verified")),
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
    # A parallel packing certified here: the finder's line, where the UnitSquare release
    # stood until then, confirmed by T-056 until 2026-10-05, when Evan Daniel's exact
    # optimum of the same packing took both lanes (T-098): the finder and the improver,
    # with no year, since the year dates the find. Below it, wand125's rectangle bound of
    # 1 October replayed as T-074, which took the case on 2026-10-02 from its 28 September
    # certificate (T-070), itself raised that day from the point bound of T-044.
    68: (
        ("Couzo & Daniel, GitHub (confirmed T-098)", "external", "verified"),
        (
            "wand125 after Tokoharu, Levy et al. 2026, GitHub (confirmed T-074)",
            "external",
            "verified",
        ),
    ),
    # The catalogue credits nobody, so the line cites the catalogue by its compilers. Since
    # 6 October 2026 Evan Daniel's exact certificate of the packing (T-101) checks a ceiling
    # one unit above its fourteenth decimal, short of the reported closed form. That earlier
    # certificate remains a result link and does not confirm the displayed value.
    # The lower line was Nagamochi's
    # until 3 October 2026, when the replayed linear certificate of 2 October was recorded
    # (T-080); on PR 305's line it was Karakuş's from 2 October (T-083) until the two lines
    # merged.
    101: (
        ("Friedman & Ellsworth, Squares in Squares (reported)", "external", "reported"),
        (
            "wand125 after Tokoharu, Levy et al. 2026, GitHub (confirmed T-080)",
            "external",
            "verified",
        ),
    ),
    # Three finders and two improvers gave "Arslanov et al." with no year here until
    # Couzo's certified packing took the case; the synthetic test above keeps that shape.
    # Since 2026-10-05 its exact optimum, Couzo's packing improved by Daniel (T-098).
    132: (
        ("Couzo & Daniel, GitHub (confirmed T-098)", "external", "verified"),
        (
            "Karakuş 2026, arXiv corrects Nagamochi 2005 (confirmed T-083)",
            "external",
            "verified",
        ),
    ),
    # A certified ceiling that trailed its report by two units of the printed place was
    # cited as reported until 2026-10-05, when the exact optimum of the same packing put
    # both lanes on one side (T-098).
    206: (
        ("Couzo & Daniel, GitHub (confirmed T-098)", "external", "verified"),
        (
            "Karakuş 2026, arXiv corrects Nagamochi 2005 (confirmed T-083)",
            "external",
            "verified",
        ),
    ),
    211: (
        ("de Winter & Daniel, GitHub (confirmed T-098)", "external", "verified"),
        (
            "Karakuş 2026, arXiv corrects Nagamochi 2005 (confirmed T-083)",
            "external",
            "verified",
        ),
    ),
}


@pytest.mark.parametrize("n", sorted(RECORDED))
def test_the_recorded_register_gives_these_lines(n: int) -> None:
    entry = _entry(n)
    assert (_line(entry["upper"]), _line(entry["lower"])) == RECORDED[n]


@pytest.mark.parametrize(
    ("n", "author", "venue", "entry"),
    [
        (11, "Queuingtheorydotcom after Levy et al.", "Web", "T-060"),
        (17, "Guzhou0806 after Kleddamag et al.", "GitHub", "T-093"),
        # Tokoharu's T-047 held n = 26 and 29 until 2026-10-02, when wand125's merged
        # rectangle replays raised both, n = 26 under T-045 and n = 29 under T-070, and
        # the replays of its 1 October certificates raised both again later that day
        # (T-074); its mixed certificates of 6 October on declared nets, decided by
        # sqverify-fast, raised both again (T-105, T-108).
        (26, "wand125 after Tokoharu, Levy et al.", "GitHub", "T-105"),
        (29, "wand125 after Tokoharu, Levy et al.", "GitHub", "T-108"),
    ],
)
def test_promoted_external_bounds_keep_the_sources_credit(
    n: int, author: str, venue: str, entry: str
) -> None:
    """The line credits the source; the register entry that replays it says so once.

    Since 2026-09-29 the register holds others' results (epistemics.md, Results by
    Others), so a promoted external bound has an entry of its own that carries the
    replay: the credit stays the source's, the result id stays empty because the bound
    is not this project's, and the entry is named as what confirms it. Each of these
    credits names more links than the line has room for beside its confirmation, so the
    stage prints the source's `short_credit`, and every other renderer the whole credit.
    """
    lower = _entry(n)["lower"]
    assert _line(lower) == (
        f"{author} 2026, {venue} (confirmed {entry})",
        "external",
        "verified",
    )
    assert lower["result"] is None
    assert lower["confirmed_by"] == [entry]
    source = _register().sources[lower["source_key"]]
    assert author == source.short_credit
    assert author in citations.short_credits(source.credited)


def test_n29_credits_finder_and_optimizer_and_takes_the_registers_verdict() -> None:
    """`n = 29` is where the catalogue's truncated decimal meets T-009's certificate.

    Its assurance is whatever `bounds_agree_at_declared_precision` says, as for every other
    case; this test names it so a change of that rule is seen here, not special-cased. The
    certificate is scored new and the packing is still Schadt and Ellsworth's. T-009
    remains linked to the case but its weaker ceiling does not confirm the displayed bound.
    """
    case = citations.load_case(29)
    upper = _entry(29)["upper"]
    assert upper["text"] == "Schadt & Ellsworth, Squares in Squares"
    assert upper["note"] == "(reported)"
    assert (upper["basis"], upper["confirmed_by"], upper["results"]) == (
        "external",
        [],
        ["T-009"],
    )
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
    # printed. Since 2026-10-06 the lane also cites T-006's replays of Daniel's case-free
    # cover, so T-006 confirms the bound and T-005, which replays nothing, does not.
    (13, "lower"): (["T-005", "T-006"], ["T-006"]),
    # Bentz's s(33) = 6, which no result registers, beside T-064's replays since then.
    (33, "lower"): (["T-064"], ["T-064"]),
    # chelokot's Lean proof, replayed here with its axiom receipt, since 2026-10-02.
    (7, "lower"): (["T-086"], ["T-086"]),
    # Karakuş's general bound since 2026-10-02, read here; its Proposition 5.1 machine-checked
    # here since 2026-10-06. n = 101 stood here until its linear certificate's replay was
    # recorded (T-080) on 3 October.
    (106, "lower"): (["T-083"], ["T-083"]),
    (101, "lower"): (["T-080"], ["T-080"]),
    # This project's own bound, established rather than confirmed, was T-030's until
    # 2026-10-02 (`test_a_novel_first_party_bound_cites_this_project_and_its_result` keeps
    # that shape); then wand125's rectangle bound, which T-045 replays, until 2026-10-05;
    # then its mixed bound on a declared net, which T-096 replays, until 2026-10-06; then
    # its bound on a finer declared net, which sqverify-fast decides (T-099), and later
    # that day its check2 bound on the finest net yet, decided the same way (T-102).
    (18, "lower"): (["T-102"], ["T-102"]),
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


def test_the_recent_lower_bounds_are_exactly_the_starred_cases() -> None:
    """The figure stars what the citation record calls recent, and nothing else."""
    starred = {n for n, figure in _composite().items() if figure["lower"]["recent_result"]}
    recent = {
        entry["n"]
        for entry in _record()["entries"]
        if entry["lower"] is not None and entry["lower"]["recent"]
    }
    assert recent == starred
    assert starred  # an empty set would pass vacuously


def test_the_figure_counts_exactly_the_corrections_the_lines_name() -> None:
    """The composite figure's `correction` is the citation record's `corrects`, and its
    totals count them beside the starred cases, never more of them than are starred."""
    composite = _composite()
    flagged = {n for n, figure in composite.items() if figure["lower"]["correction"]}
    tagged = {
        entry["n"]
        for entry in _record()["entries"]
        if entry["lower"] is not None and entry["lower"]["corrects"]
    }
    assert flagged == tagged
    assert flagged
    assert all(composite[n]["lower"]["recent_result"] for n in flagged)
    figure = json.loads(COMPOSITE.read_text(encoding="utf-8"))["figure"]
    assert figure["totals"]["lower_bound_correction"] == len(flagged)
    for drawn in figure["composites"]:
        first, last = drawn["range"]["first_n"], drawn["range"]["last_n"]
        totals = drawn["totals"]
        assert totals["lower_bound_correction"] == sum(first <= n <= last for n in flagged)
        assert totals["lower_bound_correction"] <= totals["lower_bound_recent_result"]


def test_the_project_lower_bounds_are_exactly_those_first_proved_here() -> None:
    proved = {n for n, figure in _composite().items() if figure["lower"]["first_proved_here"]}
    project = {
        entry["n"]
        for entry in _record()["entries"]
        if entry["lower"] is not None and entry["lower"]["basis"] == "project"
    }
    assert project == proved
    # The guard against a vacuous pass was `assert proved` until 2026-10-02, when the
    # merged rectangle replays raised n = 18, 19 and 20 above T-030, T-020 and T-021, the
    # last lower bounds first proved here. The synthetic test above holds a project line's
    # shape. A project lower bound stood again from 3 to 5 October 2026: n = 12, T-079's
    # re-weighting of Daniel's points, until squarepacker's re-weighting of them (T-095)
    # raised it. None stands now.
    assert proved == set()


def test_the_star_marks_recent_results_whoever_proved_them() -> None:
    """n = 11 is starred as Queuingtheorydotcom's, and project bounds are too.

    Kleddamag's 3.875, developed from T-026, preceded the exact T-060 proof. Credit
    is the line's business: joint work names this project after the author, other work
    names only its own lineage, and this project's sole work names the project. n = 18
    was this project's (T-030) until 2026-10-02 and is wand125's rectangle bound since,
    starred all the same.
    """
    lines = {entry["n"]: entry["lower"] for entry in _record()["entries"]}
    assert lines[11]["recent"]
    assert lines[11]["text"] == "Queuingtheorydotcom after Levy et al. 2026, Web"
    assert lines[12]["recent"]
    # squarepacker's re-weighting of Daniel's points since 5 October 2026 (T-095), after
    # this project's (T-079), which named the project; the credit names Levy for Route B.
    assert lines[12]["text"] == "squarepacker after Daniel, Levy 2026, GitHub"
    assert lines[18]["recent"]
    assert lines[18]["text"] == "wand125 after Tokoharu, Levy et al. 2026, GitHub"
    assert all(line["recent"] for line in lines.values() if line and line["basis"] == "project")
    assert not lines[6]["recent"]  # Kearney and Shiu 2002


def test_a_lower_bound_corrects_what_the_results_it_lists_say_they_correct() -> None:
    """Each line's `corrects` is the one work its results name in their own `corrects`,
    with the credit the bibliography prints for that work, or null where none names one."""
    register = _register()
    by_id = {str(result["id"]): result for result in register.results}
    for entry in _record()["entries"]:
        line = entry["lower"]
        if line is None:
            continue
        named = [
            by_id[rid]["corrects"] for rid in line["results"] if by_id[rid].get("corrects")
        ]
        if not named:
            assert line["corrects"] is None, entry["n"]
            continue
        keys = {(item["source_key"], item["result"]) for item in named}
        assert len(keys) == 1, entry["n"]
        ((key, result),) = keys
        source = register.sources[key]
        assert line["corrects"] == {
            "source_key": key,
            "credit": citations.short_cite(source.credited, source.year),
            "result": result,
        }, entry["n"]


def test_the_corrections_on_record_are_recent_and_name_nagamochi_2005() -> None:
    """Karakuş's floor and chelokot's s(k^2 - 2) = k stand in for Nagamochi's Theorem 2,
    whose Lemma 1 is false (the owner, 2026-10-02): every bound they carry is still a
    recent result, starred, and is tagged with the paper it corrects, which the register
    records as T-007, now V0. No other bound is tagged."""
    lines = {entry["n"]: entry["lower"] for entry in _record()["entries"] if entry["lower"]}
    corrected = {n: line for n, line in lines.items() if line["corrects"]}
    # 267 on 2026-10-02; 265 since 3 October, when n = 37 and 61 moved onto Bašić and
    # Slivková's 2018 piercing bound (T-087), which corrects nothing; 225 since the merge
    # of the same day, when replayed certificates and covers recorded in parallel
    # (T-048, T-062, T-064, T-066, T-067, T-069 to T-072, T-074 and T-075) took 40 of the
    # corrected floors, none of them correcting anything; 220 since the second merge that
    # day, when wand125's replayed linear certificate (T-080) took n = 101 to 105; 219
    # since the third, when its replayed n = 82 linear certificate (T-076) took n = 82.
    assert len(corrected) == 219
    assert 37 not in corrected
    assert 61 not in corrected
    assert all(line["recent"] for line in corrected.values())
    assert {line["source_key"] for line in corrected.values()} == {
        "[Karakuş 2026]",
        "[chelokot Nagamochi counterexample 2026]",
    }
    assert {
        (line["corrects"]["credit"], line["corrects"]["result"], line["corrects"]["source_key"])
        for line in corrected.values()
    } == {("Nagamochi 2005", "T-007", "[Nagamochi 2005]")}
    # Recent bounds that correct nothing keep the star and no tag.
    for n in (11, 12, 17, 18, 21):
        assert lines[n]["recent"], n
        assert lines[n]["corrects"] is None, n
    corrected_result = next(r for r in _register().results if r["id"] == "T-007")
    assert corrected_result["verification"] == "V0"
    assert citations.corrected_lower_bounds() == {
        n: line["corrects"] for n, line in corrected.items()
    }


def test_a_source_from_the_recent_year_must_say_its_date() -> None:
    year = citations.RECENT_SINCE.year
    undated = citations.Source(key="[X 2026]", authors=("X",), year=year, venue="GitHub")
    with pytest.raises(ValueError, match="needs `dated`"):
        citations.check_dates([undated])
    earlier = citations.Source(
        key="[Y 2026]", authors=("Y",), year=2026, venue="Web", dated=date(2026, 7, 29)
    )
    citations.check_dates([earlier])
    assert not citations.is_recent(earlier)


def test_a_project_line_names_the_result_that_carries_its_evidence() -> None:
    results = {str(result["id"]): result for result in _register().results}
    for entry in _record()["entries"]:
        line = entry["lower"]
        if line is None or line["basis"] != "project":
            continue
        result = results[line["result"]]
        year = str(result["significance"]["scored"])[:4]
        assert line["text"] == f"Squares Project (Levy) {year}, result {line['result']}"
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


def test_the_file_keeps_the_whole_spelling() -> None:
    # Review A3 on jlevy/squares#305: the stage's accent fold leaked into this file and
    # from it onto the case pages. It is the workbench loader's alone now.
    document = json.loads(citations.RECORD.read_text(encoding="utf-8"))
    texts = [
        (entry.get(bound) or {}).get("text") or ""
        for entry in document["citations"]["entries"]
        for bound in ("lower", "upper")
    ]
    assert any("Karakuş 2026" in text for text in texts)
    assert not any("Karakus 2026" in text for text in texts)
