"""The intake announcement says no more than the record holds, and credits by evidence.

`devtools.render_announcement` turns an intake pass's new results into lines the owner
can post (think-ghbx). These hold its numbers to the direction that keeps a printed bound
true, its "new best known" to the bounds on record, its handles to the evidence that
names them, and the command to the register as it stands.
"""

from __future__ import annotations

import textwrap
from collections.abc import Mapping
from dataclasses import replace
from datetime import date
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import render_announcement as ra
from devtools.check_standing import LOWER, UPPER, Stated
from devtools.render_recent_results import Records, load_records

SAMPLE = [f"T-{n}" for n in range(128, 147)]


@pytest.fixture(scope="module")
def records() -> Records:
    return load_records()


def exact(value: str | Fraction) -> ra.Span:
    number = Fraction(value)
    return ra.Span(number, number)


# --- Numbers ------------------------------------------------------------------------


def test_an_upper_bound_is_rounded_up_and_a_lower_bound_down() -> None:
    assert ra.shown(exact("13.812856253277056"), UPPER) == "13.81286"
    assert ra.shown(exact(Fraction(1340000, 199529)), LOWER) == "6.71581"
    # Where the value ends within the places, it is printed exactly, without zeros.
    assert ra.shown(exact(Fraction(291, 50)), LOWER) == "5.82"
    assert ra.shown(exact(Fraction(2297, 400)), LOWER) == "5.7425"
    for value in (Fraction(22, 7), Fraction(10**12 + 1, 10**11), Fraction(7, 3)):
        assert Fraction(ra.shown(exact(value), UPPER)) >= value
        assert Fraction(ra.shown(exact(value), LOWER)) <= value


def test_cut_decimals_are_rounded_up_from_the_top_of_what_they_stand_for() -> None:
    stated = Stated(Fraction("11.987099332245063"), Fraction(1, 10**15))
    bound = ra.Span.of_stated(stated)
    assert bound.open_high
    # 11.98710, its zero dropped.
    assert ra.shown(bound, UPPER) == "11.9871"
    assert Fraction(ra.shown(bound, UPPER)) >= bound.high


def test_a_bound_is_printed_to_as_many_places_as_keep_it_better_than_the_previous() -> None:
    new, previous = exact("10.904821012320356"), exact("10.904821012324")
    printed = Fraction(ra.shown(new, UPPER, previous))
    assert new.high <= printed < previous.low
    low, earlier = exact("6.7158157460820"), exact("6.71581574608")
    printed = Fraction(ra.shown(low, LOWER, earlier))
    assert earlier.high < printed <= low.low


def test_a_tied_or_trailing_bound_is_printed_at_the_usual_places() -> None:
    """No number of places makes such a bound better than the previous, so none are added
    in the attempt (review A, A5)."""
    tie = exact("17.5355339059327376220042218105242")
    assert ra.shown(tie, UPPER, tie) == "17.53554"
    assert ra.shown(exact("10.61"), UPPER, exact("10.5")) == "10.61"
    assert ra.shown(exact(Fraction(1340000, 199529)), LOWER, exact("7")) == "6.71581"
    cut = ra.Span.of_stated(Stated(Fraction("10.5"), Fraction(1, 10)))
    assert ra.shown(cut, UPPER, exact("10.6")) == "10.6"


def test_a_margin_is_cut_to_two_significant_figures_never_rounded_up() -> None:
    assert ra.margin_text(Fraction("0.0006598949723517562")) == "6.5e-4"
    assert ra.margin_text(Fraction("0.0102")) == "1.0e-2"
    assert ra.margin_text(Fraction("0.00999999")) == "9.9e-3"
    assert ra.margin_text(Fraction(3)) == "3.0e0"
    assert ra.margin_text(Fraction(1, 10**17) * Fraction(22, 10)) == "2.2e-17"


def test_posted_length_counts_a_link_as_23_and_a_relation_sign_twice() -> None:
    assert ra.posted_length("s(5) ≤ 2 https://jlevy.github.io/squares/results.html#t-001") == (
        len("s(5) ≤ 2 ") + 1 + ra.URL_LENGTH
    )
    # The en dash and the typographic apostrophe are in X's light ranges.
    light = "n = 122\u2013126 \u2019"
    assert ra.posted_length(light) == len(light)


# --- Standing at a count ------------------------------------------------------------


def test_a_better_bound_on_record_takes_new_best_known_away() -> None:
    bound = exact("10.5")
    count = ra.assess(105, UPPER, bound, [ra.Rival("T-200", exact("10.4"), earlier=False)])
    assert not count.best
    assert count.bettered_by == ("T-200",)


def test_an_equal_bound_registered_first_takes_it_away_and_a_later_one_does_not() -> None:
    bound = exact("10.5")
    assert not ra.assess(1, UPPER, bound, [ra.Rival("T-1", exact("10.5"), earlier=True)]).best
    assert ra.assess(1, UPPER, bound, [ra.Rival("T-9", exact("10.5"), earlier=False)]).best


def test_the_previous_best_is_the_best_bound_on_record_before_the_entry() -> None:
    rivals = [
        ra.Rival("the n = 7 case record", exact("10.9"), earlier=True),
        ra.Rival("T-100", exact("10.8"), earlier=True),
        ra.Rival("T-300", exact("10.6"), earlier=False),
    ]
    count = ra.assess(7, UPPER, exact("10.5"), rivals)
    assert count.best
    assert count.previous == exact("10.8")
    assert count.margin == Fraction("0.3")
    lower = ra.assess(7, LOWER, exact("6"), [ra.Rival("T-1", exact("5.9"), earlier=True)])
    assert lower.best
    assert lower.margin == Fraction("0.1")


def test_cut_decimals_better_a_bound_only_where_every_number_they_stand_for_does() -> None:
    cut = ra.Span.of_stated(Stated(Fraction("10.5"), Fraction(1, 10)))
    # `10.5…` to one place stands for [10.5, 10.6).
    assert ra.better(cut, exact("10.6"), UPPER)
    assert not ra.better(cut, exact("10.59"), UPPER)
    assert ra.better(exact("10.6"), cut, LOWER)
    assert not ra.better(exact("10.59"), cut, LOWER)
    assert not ra.better(exact("10.5"), cut, UPPER)


# --- Credit and handles -------------------------------------------------------------


def handle(name: str, at: str) -> ra.Handle:
    return ra.Handle(name, at, "test")


def test_a_credit_line_splits_into_its_finders_and_its_lineage_in_register_order() -> None:
    assert ra.credit_parts("Ahmed et al. after Levy, Daniel") == (
        ["Ahmed et al."],
        ["Levy", "Daniel"],
    )
    assert ra.credit_parts("wand125 after Tokoharu and Levy") == (
        ["wand125"],
        ["Tokoharu", "Levy"],
    )
    assert ra.credit_parts("Couzo; Daniel after Couzo, Levy") == (
        ["Couzo", "Daniel"],
        ["Couzo", "Levy"],
    )
    assert ra.primary_names("Wang, Li after Overbeck, Levy") == ["Wang", "Li"]


def test_the_owner_is_never_among_the_people_a_line_credits() -> None:
    assert ra.PROJECT_AUTHOR == "Levy"
    assert ra.people(["Couzo", "Levy", "Levy et al.", "Daniel"]) == [
        "Couzo",
        "Daniel",
    ]
    handles, _ = ra.resolve_handles(["Levy"], [], None, {"Levy": handle("Levy", "ojoshe")})
    assert handles == {}


def test_a_name_shows_as_its_handle_else_its_full_name_else_as_credited() -> None:
    full = ra.full_names(
        {
            "Francisco Couzo": "Couzo",
            "Nate Chaoweeraprasit (itsnaka)": "Chaoweeraprasit",
            "Nate Chaoweeraprasit": "Chaoweeraprasit",
            "ry-xu": "ry-xu",
        }
    )
    assert full == {
        "Couzo": "Francisco Couzo",
        "Chaoweeraprasit": "Nate Chaoweeraprasit",
        "ry-xu": "ry-xu",
    }
    names = ra.Names({"Ahmed": handle("Ahmed", "ManassehA06")}, full)
    assert names.show("Couzo") == "Francisco Couzo"
    assert names.show("Ahmed et al.") == "@ManassehA06 et al."
    assert names.show("Xu") == "Xu"
    # Two full names for one credited name give neither.
    assert ra.full_names({"Ada Smith": "Smith", "Bo Smith": "Smith"}) == {}


PROFILE = """\
---
softschema:
  contract: packing.squares:Contributor/v1
  schema: contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: {id}
  display_name: '{display}'
  aliases: [{aliases}]
  links:
{links}
  sources:
    - id: primary-byline
      archive_path: LICENSE
      locator: 'test'
  provenance:
    - field: /display_name
      sources: [primary-byline]
---
"""


def write_profile(
    directory: Path, person: str, display: str, aliases: str, links: list[tuple[str, str, str]]
) -> None:
    lines = "\n".join(
        f"    - kind: {kind}\n      url: {url}\n      handle: {at}" for kind, url, at in links
    )
    directory.mkdir(exist_ok=True)
    (directory / f"{person}.md").write_text(
        PROFILE.format(id=person, display=display, aliases=aliases, links=lines),
        encoding="utf-8",
    )


def test_a_contributor_profile_gives_its_twitter_link_and_its_github_login(
    tmp_path: Path,
) -> None:
    write_profile(
        tmp_path,
        "francisco-couzo",
        "Francisco Couzo",
        "Couzo, franciscouzo",
        [
            ("github", "https://github.com/franciscouzo", "franciscouzo"),
            ("twitter", "https://x.com/fc_test", "fc_test"),
        ],
    )
    write_profile(
        tmp_path,
        "evan-daniel",
        "Evan Daniel",
        "Daniel, evand",
        [("github", "https://github.com/evand", "evand")],
    )
    profiles = ra.load_profiles(tmp_path)
    assert {p.id for p in profiles} == {"francisco-couzo", "evan-daniel"}
    assert {p.id: p.github for p in profiles}["evan-daniel"] == ("evand",)
    handles, warnings = ra.resolve_handles(["Couzo", "Daniel", "Xu"], profiles, None, {})
    assert warnings == []
    assert handles["Couzo"].handle == "fc_test"
    assert "francisco-couzo.md" in handles["Couzo"].source
    assert set(handles) == {"Couzo"}
    assert ra.load_profiles(tmp_path / "absent") == []


def fake_github(
    users: Mapping[str, Mapping[str, Any]],
    *,
    issues: list[dict[str, Any]] | None = None,
    credited: Mapping[str, str] | None = None,
    primaries: Mapping[str, list[str]] | None = None,
) -> tuple[ra.GitHub, list[str]]:
    fetched: list[str] = []

    def fetch(login: str) -> Mapping[str, Any] | None:
        fetched.append(login)
        return users.get(login)

    github = ra.GitHub(
        owner="jlevy",
        issues=issues or [],
        credited_names=credited or {},
        primaries=primaries or {},
        fetch=fetch,
    )
    return github, fetched


def issue(number: int, author: str, *ids: str) -> dict[str, Any]:
    return {"number": number, "author": author, "results": [{"register": list(ids)}]}


def test_github_ties_a_login_to_a_credited_name_only_by_evidence() -> None:
    users = {
        "jlevy": {"name": "Joshua Levy", "twitter_username": "ojoshe"},
        "ry-xu": {"name": "Ryan Xu", "twitter_username": "small_LM"},
        "franciscouzo": {"name": "Francisco Couzo", "twitter_username": "fc_x"},
        "itsnaka": {"name": "natcha", "twitter_username": "naka_x"},
        "lollipoll": {"name": None, "twitter_username": "rehwaldt_x"},
        "evand": {"name": "Evan Daniel", "twitter_username": None},
    }
    github, _ = fake_github(
        users,
        issues=[
            issue(432, "ry-xu", "T-125"),
            issue(451, "franciscouzo", "T-128"),
            issue(481, "itsnaka", "T-136"),
            issue(425, "lollipoll", "T-117", "T-118"),
            issue(465, "evand", "T-131", "T-128"),
        ],
        credited={
            "Francisco Couzo": "Couzo",
            "Nate Chaoweeraprasit (itsnaka)": "Chaoweeraprasit",
            "Evan Daniel": "Daniel",
        },
        primaries={
            "T-125": ["ry-xu"],
            "T-128": ["Couzo"],
            "T-131": ["Daniel"],
            "T-136": ["Chaoweeraprasit"],
            "T-117": ["Rehwaldt"],
            "T-118": ["Rehwaldt"],
        },
    )
    names = ["Levy", "ry-xu", "Xu", "Couzo", "Chaoweeraprasit", "Rehwaldt", "Daniel"]
    handles, warnings = ra.resolve_handles(names, [], github, {})
    assert warnings == []
    # The owner is never tagged, whatever his account declares.
    assert {name: h.handle for name, h in handles.items()} == {
        "ry-xu": "small_LM",
        "Couzo": "fc_x",
        "Chaoweeraprasit": "naka_x",
        "Rehwaldt": "rehwaldt_x",
    }
    assert "jlevy" not in github.candidates()
    assert "credited_names" in handles["Chaoweeraprasit"].source
    assert "#425" in handles["Rehwaldt"].source
    # Xu is credited by surname and nothing in the record ties it to ry-xu's login; Daniel's
    # account declares no handle. Neither gets one.
    assert "Xu" not in handles
    assert "Daniel" not in handles


def test_an_issue_never_ties_the_owner_or_an_issue_that_credits_two_people() -> None:
    users = {"jlevy": {"twitter_username": "ojoshe"}, "evand": {"twitter_username": "ev"}}
    github, _ = fake_github(
        users,
        issues=[issue(1, "jlevy", "T-001"), issue(465, "evand", "T-131", "T-128")],
        primaries={"T-001": ["Bentz"], "T-131": ["Daniel"], "T-128": ["Couzo"]},
    )
    handles, _ = ra.resolve_handles(["Bentz", "Daniel", "Couzo"], [], github, {})
    assert handles == {}


def test_two_handles_for_one_name_give_none() -> None:
    users = {
        "alpha": {"name": "Ada Smith", "twitter_username": "one"},
        "beta": {"name": "Ada Smith", "twitter_username": "two"},
    }
    github, _ = fake_github(
        users,
        issues=[issue(1, "alpha"), issue(2, "beta")],
        credited={"Ada Smith": "Smith"},
    )
    handles, warnings = ra.resolve_handles(["Smith"], [], github, {})
    assert handles == {}
    assert len(warnings) == 1
    assert "Smith" in warnings[0]


def test_a_malformed_login_is_never_fetched() -> None:
    github, fetched = fake_github({}, issues=[issue(1, "../../orgs/x")])
    ra.resolve_handles(["Somebody"], [], github, {})
    assert "../../orgs/x" not in fetched


def test_a_profile_wins_over_github_and_github_over_the_record(tmp_path: Path) -> None:
    write_profile(
        tmp_path,
        "queuingtheorydotcom",
        "Queuingtheorydotcom",
        "Ahmed, ManassehA06",
        [("twitter", "https://x.com/ManassehA06", "ManassehA06")],
    )
    stated = {"Ahmed": handle("Ahmed", "from_record"), "Fang": handle("Fang", "from_record")}
    github, _ = fake_github(
        {"TheSnakeFang": {"name": "Fang", "twitter_username": "fang_x"}},
        issues=[issue(484, "TheSnakeFang")],
    )
    handles, _ = ra.resolve_handles(
        ["Ahmed", "Fang"], ra.load_profiles(tmp_path), github, stated
    )
    assert handles["Ahmed"].handle == "ManassehA06"
    assert handles["Fang"].handle == "fang_x"
    handles, _ = ra.resolve_handles(["Fang"], [], None, stated)
    assert handles["Fang"].handle == "from_record"


def test_every_handle_the_record_states_is_still_stated_there() -> None:
    found = ra.record_handles()
    assert found["Ahmed"].handle == "ManassehA06"
    assert "packing/frontier/n-011.md" in found["Ahmed"].source


def test_a_record_handle_whose_words_are_gone_fails_loudly(tmp_path: Path) -> None:
    (tmp_path / "case.md").write_text("Ahmed wrote a proof.\n", encoding="utf-8")
    table = (
        ra.RecordHandle("Ahmed", "ManassehA06", "case.md", "posts on X as [@ManassehA06]"),
    )
    with pytest.raises(SystemExit, match="no longer says"):
        ra.record_handles(table, tmp_path)


# --- The register as it stands ------------------------------------------------------


def test_every_printed_bound_is_true_and_beats_the_previous_best_where_it_is_new(
    records: Records,
) -> None:
    """Over the whole register: a printed upper bound is at least every number the entry
    states and a printed lower bound at most; where a count is the best known, the printed
    number is still strictly better than the previous best."""
    index = ra.rival_bounds(records)
    checked = 0
    for record in records.register.results:
        if record["kind"] not in ra.BOUND_KINDS:
            continue
        for count in ra.counts(record, records, index):
            printed = Fraction(ra.shown(count.bound, count.direction, count.previous))
            if count.direction == UPPER:
                assert printed >= count.bound.high, (record["id"], count.n)
            else:
                assert printed <= count.bound.low, (record["id"], count.n)
            if count.best and count.previous is not None:
                assert ra.better(exact(printed), count.previous, count.direction)
            checked += 1
    assert checked > 100


def test_since_selects_by_the_date_the_register_received_a_result(records: Records) -> None:
    chosen, skipped = ra.select(records, since="2026-10-10", min_significance=3)
    assert chosen
    assert all(str(r["registered"]) >= "2026-10-10" for r in chosen)
    assert all(int(r["significance"]["score"]) >= 3 for r in chosen)
    assert all("significance" in line.left_out for line in skipped)
    with pytest.raises(SystemExit, match="not in the register"):
        ra.select(records, ids=["T-999"])


def run(
    capsys: pytest.CaptureFixture[str], argv: list[str], **kwargs: Any
) -> tuple[list[str], str]:
    assert ra.main(argv, **kwargs) == 0
    captured = capsys.readouterr()
    return captured.out.splitlines(), captured.err


def test_the_announcement_of_the_sample_is_brief_and_states_no_more_than_its_rungs(
    records: Records, capsys: pytest.CaptureFixture[str]
) -> None:
    lines, err = run(capsys, ["--ids", *SAMPLE, "--date", "2026-10-11"])
    head, body = lines[0], lines[1:]
    assert head == f"11 October 2026: {len(body)} new results"
    assert body
    for line in body:
        entry = line.rsplit("#", 1)[-1].upper()
        record = records.results[entry]
        assert line.endswith(ra.result_link(entry))
        text = ra.before_link(line)
        assert len(text) <= ra.BRIEF_LIMIT, line
        assert "#" not in text, "no hashtags"
        assert "Levy" not in text, "the owner is never credited"
        assert " after " not in text, "the lineage is opt-in"
        if ra.verified(record):
            assert text.count("(verified)") == 1
        else:
            assert "(reported)" in text
            assert "verified" not in text
    # Full names where the bibliography gives one.
    assert any("Francisco Couzo" in line for line in body)
    assert "warning" not in err
    # T-129 is scored 1; every result left out is said to be, with why.
    assert "left out T-129: significance 1, below 3" in err
    left = {
        line.split(":")[0].removeprefix("left out ")
        for line in err.splitlines()
        if line.startswith("left out")
    }
    printed = {line.rsplit("#", 1)[-1].upper() for line in body}
    assert left | printed == set(SAMPLE)
    assert not left & printed


def test_github_handles_reach_the_lines_and_their_sources_reach_stderr(
    capsys: pytest.CaptureFixture[str],
) -> None:
    users = {
        "jlevy": {"name": "Joshua Levy", "twitter_username": "ojoshe"},
        "franciscouzo": {"name": "Francisco Couzo", "twitter_username": "fc_test"},
    }
    lines, err = run(
        capsys,
        ["--ids", "T-128", "--date", "2026-10-11", "--github", "--lineage"],
        fetch=users.get,
    )
    assert len(lines) == 2
    assert ": @fc_test after " in lines[1]
    assert "Francisco Couzo" not in lines[1]
    assert "ojoshe" not in lines[1]
    assert "Levy" not in lines[1]
    assert "@fc_test for Couzo: GitHub profile of franciscouzo" in err


def test_margins_are_opt_in_and_say_how_far_past_the_previous_best(
    capsys: pytest.CaptureFixture[str],
) -> None:
    lines, _ = run(capsys, ["--ids", "T-157", "--date", "2026-10-12"])
    assert "previous best" not in lines[1]
    lines, _ = run(capsys, ["--ids", "T-157", "--date", "2026-10-12", "--margins"])
    assert "above the previous best)" in lines[1]


def test_all_keeps_a_bettered_result_and_says_what_betters_it(
    capsys: pytest.CaptureFixture[str], records: Records
) -> None:
    index = ra.rival_bounds(records)
    bettered = next(
        record
        for record in records.register.results
        if record["kind"] in ra.BOUND_KINDS
        and (found := ra.counts(record, records, index))
        and not any(count.best for count in found)
        and int(record["significance"]["score"]) >= ra.MIN_SIGNIFICANCE
    )
    entry = str(bettered["id"])
    lines, err = run(capsys, ["--ids", entry, "--date", "2026-10-11"])
    assert lines == ["11 October 2026: 0 new results"]
    assert f"left out {entry}: the best known at no count" in err
    lines, _ = run(capsys, ["--ids", entry, "--date", "2026-10-11", "--all"])
    assert ", since " in lines[1]
    assert "new best" not in lines[1]


def test_all_prints_a_tied_bound_at_five_places_and_says_what_supersedes_a_boundless_one(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """T-156 only equals its case record; T-125 states no bound and holds no case
    (review A, A5)."""
    lines, _ = run(
        capsys, ["--ids", "T-156", "--date", "2026-10-12", "--all", "--min-significance", "1"]
    )
    assert lines[1].startswith("s(290) ≤ 17.53554 (verified), since equalled first by ")
    lines, _ = run(capsys, ["--ids", "T-125", "--date", "2026-10-12", "--all"])
    assert "(verified), since superseded by " in lines[1]


def test_a_since_clause_names_at_most_three_and_counts_the_rest() -> None:
    assert ra.whom("bettered", ["T-146", "T-150"], 2) == "bettered by T-146 and T-150"
    cases = [f"the n = {n} case record" for n in (28, 29, 37, 39)]
    assert ra.whom("bettered", cases, 4) == "bettered at 4 counts by their case records"
    labels = ["T-128", "T-130", "T-134", "T-136, T-140", *cases]
    assert ra.whom("bettered", labels, 9) == (
        "bettered at 9 counts by 5 results and their case records"
    )
    assert ra.whom("superseded", ["T-128", "T-130", "T-134", "T-136"]) == (
        "superseded by 4 results"
    )


def test_all_keeps_a_long_since_clause_postable(capsys: pytest.CaptureFixture[str]) -> None:
    """T-155 is bettered or equalled first at 59 counts by their case records; its line
    once listed fourteen of them, 1,587 characters (review A, A5)."""
    lines, err = run(
        capsys, ["--ids", "T-155", "--date", "2026-10-12", "--all", "--min-significance", "1"]
    )
    assert "case record," not in lines[1]
    assert "on X" not in err


def test_a_line_about_a_few_counts_prints_each_bound_where_the_line_stays_brief(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """T-141's two bounds fit; T-151's five counts do not and stay elided (review A,
    A8). T-149's three were the example until the intake of 14 October left it the best
    known at 155 alone, and T-162's three until T-186 bettered it at all three on 15
    October."""
    lines, _ = run(capsys, ["--ids", "T-141", "T-151", "--date", "2026-10-14"])
    assert lines[1].startswith(
        "s(132) ≤ 11.98569, s(308) ≤ 17.99827, new best known (verified): "
    )
    assert lines[2].startswith("s(n) ≤ … at n = 181, 238, 239, 270, 272, new best known ")
    record = {"id": "T-900", "headline": "s(n) ≤ 10", "claim": ""}
    group = [ra.Count(n, UPPER, exact(f"{n}.5")) for n in (10, 11)]
    assert ra.statement(record, group) == "s(10) ≤ 10.5, s(11) ≤ 11.5"
    assert ra.statement(record, group, each=False) == "s(n) ≤ … at n = 10, 11"


def test_a_regularization_credits_the_finder_of_the_packing_it_regularizes(
    capsys: pytest.CaptureFixture[str], records: Records
) -> None:
    entry = next(
        str(record["id"])
        for record in records.register.results
        if record.get("regularizations") and record["kind"] in ra.BOUND_KINDS
    )
    lines, _ = run(
        capsys, ["--ids", entry, "--date", "2026-10-11", "--min-significance", "1", "--all"]
    )
    assert ", regularizing " in lines[1]


def test_a_case_held_by_a_regularization_of_the_entrys_own_packing_does_not_better_it(
    records: Records,
) -> None:
    """T-146 regularizes T-136's packings at 236, 263, 269, 292, 302 and 303 and holds
    those cases: neither its own bound nor the case records' count against T-136 there
    (review B, B2)."""
    index = ra.rival_bounds(records)
    found = {c.n: c for c in ra.counts(records.results["T-136"], records, index)}
    for n in (236, 263, 269, 292, 302, 303):
        assert ra.regularizes(records.results["T-146"], n, "T-136")
        assert "T-146" not in found[n].bettered_by, (n, found[n].bettered_by)
        # T-146's side is the smaller, so the line prints no number of T-136's there.
        assert found[n].regularized_by == ("T-146",)
    record = {"id": "T-900", "headline": "s(103) ≤ 10", "claim": ""}
    count = ra.Count(103, UPPER, exact("10"), regularized_by=("T-901",))
    assert ra.statement(record, [count]) == "s(103) ≤ …"


def test_a_refinement_credits_the_person_its_headline_names_singular_or_plural(
    capsys: pytest.CaptureFixture[str], records: Records
) -> None:
    """T-137 refines Ryan Xu's packing and T-150 his packings; both credit him. Since
    T-187 bettered T-150 at 146 on 15 October, and PingYou Ltd's re-solves (T-168,
    T-169) took both its counts the same day, T-150's line is kept with `--all`; over
    both its counts it says "packings"."""
    lines, _ = run(
        capsys, ["--ids", "T-137", "--date", "2026-10-11", "--all", "--min-significance", "1"]
    )
    assert ", refining Ryan Xu's packing " in lines[1]
    lines, _ = run(
        capsys, ["--ids", "T-150", "--date", "2026-10-12", "--all", "--min-significance", "1"]
    )
    assert ": Robert Barnett, refining Ryan Xu's packings " in lines[1]
    both = [ra.Count(n, UPPER, exact("13")) for n in (146, 261)]
    names = ra.Names(full={"Xu": "Ryan Xu"})
    assert ra.worked_on(records.results["T-150"], both, records, names) == (
        "refining Ryan Xu's packings"
    )
    names = ra.Names({"Xu": handle("Xu", "from_record")}, names.full)
    assert ra.worked_on(records.results["T-150"], both, records, names) == (
        "refining @from_record's packings"
    )
    written = {**records.results["T-150"], "headline": "refinements of Ryan Xu's packings"}
    assert ra.worked_on(written, both, records, ra.Names()) == ("refining Ryan Xu's packings")


def test_a_refinement_of_a_requests_packings_credits_the_entry_its_claim_names(
    capsys: pytest.CaptureFixture[str], records: Records
) -> None:
    """T-152 refines "SQUISH's Mondrian packings", which its claim names as T-151's, Nate
    Chaoweeraprasit's; the line credits him, since T-151's own line no longer names 304 or
    305 (review B, B1). Since the intake of 14 October T-152 is the best known at 305
    alone, so the packing is singular."""
    lines, err = run(capsys, ["--ids", "T-152", "--date", "2026-10-12"])
    assert ": Francisco Couzo, refining Nate Chaoweeraprasit's packing " in lines[1]
    assert "Chaoweeraprasit" in err.split("printed by name: ", 1)[1]
    refinement = ra.refined(records.results["T-152"], records)
    assert refinement is not None
    assert refinement.people == (("Chaoweeraprasit", ""),)


def test_a_refinement_resolves_through_headlines_with_either_apostrophe(
    records: Records,
) -> None:
    """`REFINED` reads a straight or a typographic apostrophe before the s, and so does
    the search for the entry a claim names (review C, C7): with every SQUISH headline
    typeset, T-152 still credits Nate Chaoweeraprasit."""
    typeset = {
        entry: {**records.results[entry], "headline": str(records.results[entry]["headline"])}
        for entry in ("T-136", "T-151", "T-152")
    }
    for record in typeset.values():
        record["headline"] = str(record["headline"]).replace("SQUISH's", "SQUISH\u2019s")
    assert all("\u2019" in str(record["headline"]) for record in typeset.values())
    swapped = replace(records, results={**records.results, **typeset})
    refinement = ra.refined(typeset["T-152"], swapped)
    assert refinement is not None
    assert refinement.people == (("Chaoweeraprasit", ""),)


def test_the_frontmatter_reader_reads_only_the_opening_block() -> None:
    text = textwrap.dedent(
        """\
        ---
        a: 1
        ---
        body
        ---
        b: 2
        """
    )
    assert ra.frontmatter(text) == "a: 1"
    assert ra.frontmatter("no front matter\n") == ""


def test_stderr_says_whether_the_announcement_fits_one_post_or_a_thread(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Review A, A9: the line limit implies one post a line, so the block is checked too."""
    _, err = run(capsys, ["--ids", "T-147", "--date", "2026-10-12"])
    assert "the announcement fits one X post" in err
    _, err = run(
        capsys, ["--ids", *[f"T-{n}" for n in range(147, 153)], "--date", "2026-10-12"]
    )
    assert "over one post's 280; as a thread of one line a post, every line fits" in err
    assert ra.block_fit(["a", "b"]) == "the announcement fits one X post: 3 of 280 characters"


def test_the_header_names_the_day_and_the_count() -> None:
    assert ra.header(date(2026, 10, 11), 1) == "11 October 2026: 1 new result"
    assert ra.header(date(2026, 1, 2), 12) == "2 January 2026: 12 new results"
