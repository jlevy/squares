"""The frontier atlas page: one row per case record, every value read from the record."""

from __future__ import annotations

import re
import shutil
from fractions import Fraction
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import pytest

from devtools import render_frontier_page as frontier
from devtools import render_overview, site_assets
from devtools import render_research_tables as tables
from devtools.render_overview import assert_fetches_only_assets
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.yamlio import safe_load
from tests import site_renders

#: Measured at 3.6 MB on 2026-09-29 (324 cases): 1.6 MB is the site shell every page
#: carries (the explainer's inlined faces and KaTeX), about 0.95 MB the 324 thumbnails
#: and the rest the cells and their record links. The ceiling leaves room for the corpus
#: to grow a little; a change that crosses it should shrink something rather than lift it.
#: Measured at 4,168,556 bytes on 2026-10-01 before the drawing took its own column and
#: the closed forms their decimals, and at 4,183,093 after: 25,748 bytes of room, then
#: 11,211. Each cell KPress writes carried `data-col` and `data-col-index`, 128,050
#: bytes of the page that nothing on the site reads; every page drops them since
#: 2026-10-02 (think-k8xp), which left the page 4,070,117 bytes with the status chips'
#: fills of the same day. Each row's own popover went on 2026-10-03, when a row came to
#: open its case's record in the one case popover (think-necq): 3,442,575 bytes, and
#: 3,498,657 with the case badges of the same day (think-7cbx). With the 265 lower
#: bounds that correct Nagamochi 2005 carrying their tag and `data-corrects` (the owner,
#: 2026-10-02), and the star's tooltip said once by its column's heading, it measured
#: 3,523,448 bytes on 2026-10-03. The shell, 1,838,406 bytes of the page by 2026-10-04,
#: became the site's shared assets that day (`site_assets`), which the page links rather
#: than carries: 1,656,135 bytes, with the ceiling, 4 MiB until then, lowered by as much
#: to keep the room it had. The merge of main into PR 305 that day, carrying both,
#: measured 1,681,361 bytes.
PAGE_CEILING_BYTES = 1_750_000

#: The columns as a reader meets them: the drawing under no heading, the case, the star,
#: and then what is known.
COLUMNS = [
    "",
    "n",
    "Recent",
    "Status",
    "Best known packing",
    "Verified upper",
    "Reported lower",
    "Verified lower",
    "Gap",
    "Records",
]
#: The value columns and the record field each one's `data-value` carries.
VALUE_COLUMNS = {
    "Best known packing": "reported_upper_bound",
    "Verified upper": "verified_upper_bound",
    "Reported lower": "reported_lower_bound",
    "Verified lower": "verified_lower_bound",
}
#: A decimal under a closed form: whether it is the whole value, and its digits.
APPROX = re.compile(r'<span class="site-approx">([=≈]) (\d+\.\d+)(…?)</span>')


def column(label: str) -> int:
    """The index of the column headed `label` in a row's cells."""
    return COLUMNS.index(label)


class Rows(HTMLParser):
    """The header cells, and each body row's attributes with its cells' attributes, in
    order. A cell also records the tags it holds and its words, under `tags` and
    `words`, which no attribute is named."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[tuple[dict[str, str | None], list[dict[str, str | None]]]] = []
        self.head: list[dict[str, str | None]] = []
        self._body = False
        self._cell: dict[str, str | None] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tbody":
            self._body = True
        elif tag == "tr" and self._body:
            self.rows.append((dict(attrs), []))
        elif tag == "td" and self._body and self.rows:
            self._cell = {**dict(attrs), "tags": "", "words": ""}
            self.rows[-1][1].append(self._cell)
        elif tag == "th" and not self._body and not self.rows:
            self._cell = {**dict(attrs), "tags": "", "words": ""}
            self.head.append(self._cell)
        elif self._cell is not None:
            self._cell["tags"] = f"{self._cell['tags']} {tag}".strip()

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell["words"] = f"{self._cell['words']}{data}"

    def handle_endtag(self, tag: str) -> None:
        if tag == "tbody":
            self._body = False
        elif tag in {"td", "th"}:
            self._cell = None


@pytest.fixture(scope="module")
def page() -> str:
    return site_renders.html("frontier.html")


@pytest.fixture(scope="module")
def served() -> str:
    """The page as a reader's browser assembles it, with every shared asset it links put
    back in it (`tests.site_renders.served`)."""
    return site_renders.served("frontier.html")


@pytest.fixture(scope="module")
def parsed(page: str) -> Rows:
    parser = Rows()
    parser.feed(page[page.index('id="frontier-table"') :])
    return parser


@pytest.fixture(scope="module")
def rows(parsed: Rows) -> list[tuple[dict[str, str | None], list[dict[str, str | None]]]]:
    return parsed.rows


@pytest.fixture(scope="module")
def cases() -> dict[int, dict[str, Any]]:
    return {case["n"]: case for case in tables.load_cases()}


def test_every_case_file_is_a_row_and_every_row_a_case_file(rows) -> None:
    files = sorted(int(path.stem.split("-")[1]) for path in tables.FRONTIER.glob("n-*.md"))
    shown = [int(attributes["data-n"] or 0) for attributes, _ in rows]
    assert shown == files
    assert len(shown) == len(set(shown))


def test_every_row_is_its_cases_anchor(rows) -> None:
    """`frontier.html#n-11` lands on the case, which the overview's case cards open."""
    for attributes, _ in rows:
        assert attributes["id"] == f"n-{attributes['data-n']}"


def test_every_value_cell_carries_the_records_value(rows, cases) -> None:
    for attributes, cells in rows:
        case = cases[int(attributes["data-n"] or 0)]
        assert cells[column("n")]["data-value"] == str(case["n"])
        assert cells[column("Status")]["data-value"] == case["status"]
        assert attributes["data-status"] == case["status"]
        assert (
            cells[column("Recent")]["data-value"]
            == {"true": "1", "false": "0"}[attributes["data-recent"] or ""]
        )
        for label, field in VALUE_COLUMNS.items():
            assert cells[column(label)]["data-value"] == str(case[field]["value"]), (
                case["n"],
                field,
            )


def test_the_columns_run_drawing_case_star_and_then_what_is_known(parsed: Rows) -> None:
    """The drawing has the first column to itself, under a header with no words that a
    screen reader is told is the packing; `n` is next and holds the number alone, the
    link to the case record; the star follows, ahead of the status and the bounds, so the
    table's left edge says which case a row is and whether its bound is new."""
    assert [heading for heading, _, _ in frontier.HEADERS] == COLUMNS
    assert [(cell["words"] or "").strip() for cell in parsed.head] == COLUMNS
    first, *others = parsed.head
    assert first["aria-label"] == frontier.THUMB_LABEL == "Packing"
    assert first["class"] == "site-thumb"
    assert first["tags"] == ""
    assert "data-sort" not in first
    assert all("aria-label" not in cell for cell in others)
    assert [cell.get("data-sort") for cell in others] == [
        "num",
        "num",
        "text",
        "num",
        "num",
        "num",
        "num",
        "num",
        None,
    ]
    assert len(parsed.rows) == 324
    for attributes, cells in parsed.rows:
        n = attributes["data-n"]
        assert len(cells) == len(COLUMNS), n
        thumb, number, star = cells[0], cells[column("n")], cells[column("Recent")]
        # A standalone SVG image reserves its size without expanding the table HTML.
        assert thumb["class"] == "site-thumb", n
        assert thumb["tags"] == "img", n
        assert thumb["words"] == "", n
        assert "data-value" not in thumb
        # The number alone, as the one link to the case record.
        assert number["class"] == "num site-col-n", n
        assert number["tags"] == "a", n
        assert number["words"] == n
        # The star, and after it the tag of a bound that corrects a published result.
        shown = "★" if attributes["data-recent"] == "true" else ""
        if "data-corrects" in attributes:
            shown += "corrects Nagamochi 2005"
        assert star["words"] == shown, n


def test_a_correcting_bound_keeps_its_star_and_names_what_it_corrects(
    rows, parsed: Rows
) -> None:
    """A verified lower bound that corrects a published result is still recent, so its
    row keeps the star, and the same cell says which work it corrects, in one short span
    with no link; the row names the register's record of that work in `data-corrects`
    (the owner, 2026-10-02). Which bounds those are is the citation record's to say."""
    corrected = frontier.corrected_lower_bounds()
    # 265 since n = 37 and 61 moved onto Bašić and Slivková's bound (T-087) on 2026-10-03;
    # 225 since the merge of the same day, when replayed certificates and covers recorded
    # in parallel took 40 of the corrected floors, none of them correcting anything; 220
    # since the second merge that day, when T-080's replayed certificate took n = 101 to 105;
    # 219 since the third, when T-076's replayed linear certificate took n = 82.
    assert len(corrected) == 219
    seen = 0
    for attributes, cells in rows:
        n = int(attributes["data-n"] or 0)
        star = cells[column("Recent")]
        if n not in corrected:
            assert "data-corrects" not in attributes, n
            assert (star["tags"] or "") in ("", "span"), n
            continue
        seen += 1
        assert attributes["data-corrects"] == corrected[n]["result"] == "T-007", n
        assert attributes["data-recent"] == "true", n
        assert star["data-value"] == "1", n
        assert star["tags"] == "span span", n
        assert star["words"] == f"★corrects {corrected[n]['credit']}", n
    assert seen == len(corrected)
    # n = 38 was the example until the merge of 2026-10-03 put wand125's replayed
    # certificate (T-074) above its corrected floor, and n = 82 until the third merge that
    # day put T-076's replayed linear certificate above its own; n = 106, the least open
    # case on Karakuş's floor, still stands on it.
    case = next(case for case in tables.load_cases() if case["n"] == 106)
    row = frontier.case_row(case, recent=True, corrects=corrected[106])
    assert (
        '<td data-value="1"><span class="site-star">★</span>'
        '<span class="site-corrects">corrects Nagamochi 2005</span></td>'
    ) in row
    assert ' data-recent="true" data-corrects="T-007" ' in row
    plain = frontier.case_row(case, recent=True)
    assert '<td data-value="1"><span class="site-star">★</span></td>' in plain
    assert "data-corrects" not in plain
    # The star's tooltip is said once, by its column's heading, not on every star.
    (recent,) = [cell for cell in parsed.head if (cell["words"] or "").strip() == "Recent"]
    assert recent["title"] == frontier.HEADER_TITLES["Recent"]
    assert all("title" not in cell for cell in parsed.head if cell is not recent)


def test_the_page_says_once_what_the_tag_means_and_links_the_corrected_result(
    page: str,
) -> None:
    """The rows repeat the tag without a link; the Recent results paragraph says what it
    means once, with the count from the citation record, the register's record of the
    corrected work linked to its row, and the register's words for what failed."""
    sentence = frontier.corrections_prose()
    assert sentence == (
        "Beside 219 of the stars, *corrects Nagamochi 2005* says the bound stands in for "
        "a published result found unsound, the register\u2019s "
        "[T-007](all-results.html#t-007): "
        "Lemma 1, on which Theorem 2\u2019s proof rests, is false."
    )
    prose = page[: page.index('id="frontier-table"')]
    assert (
        "Beside 219 of the stars, <em>corrects Nagamochi 2005</em> says the bound stands in"
    ) in prose
    assert '<a href="all-results.html#t-007">T-007</a>' in prose
    table = page[page.index("<tbody>") : page.index("</tbody>")]
    assert "all-results.html#t-007" not in table


#: The cases whose verified lower bound rests only on a published proof nobody here has
#: read: Göbel's s(5), Kearney and Shiu's s(6), Stromquist's s(10) and Bentz's s(22), each
#: transcribed with its theorem and pinpoints and never worked through here. Bentz's s(33)
#: was one until its lane cited T-064's replays beside the proof on 2026-10-06; n = 13's
#: proof, Bentz's of 2010, is read here, with an erratum in one lemma, and its lane cites
#: T-006's replays since the same day.
UNREAD_PROOF_CASES = (5, 6, 10, 22)
#: The cases whose reported lower bound is a value of Green's DS7 Theorem 9, whose
#: illustrated argument leaves a unit square empty (`devtools.check_green_ds7`), above
#: the verified floor.
GREEN_THEOREM_9 = frozenset(
    {
        *range(122, 126),
        *range(145, 149),
        *range(170, 174),
        *range(197, 201),
        *range(226, 230),
        *range(257, 262),
        *range(290, 295),
    }
)


def test_a_verified_bound_on_an_unread_published_proof_says_so(rows, cases) -> None:
    """A published proof enters the verified column whether or not anyone here has read
    it, and "✓ same" says only that the verified bound equals the reported value. So a
    verified cell whose every cited entry is a published proof nobody here has read says
    so under its bound, and no other cell does. Until 2026-10-06 those cells said "✓
    same" alone, which the page's introduction read as "verified here at the reported
    value"."""
    evidence = tables.load_evidence()
    marked = set()
    for attributes, cells in rows:
        n = int(attributes["data-n"] or 0)
        for label, field in (
            ("Verified upper", "verified_upper_bound"),
            ("Verified lower", "verified_lower_bound"),
        ):
            words = cells[column(label)]["words"] or ""
            unread = tables.rests_on_unread_proof(cases[n][field], evidence)
            assert words.endswith(frontier.UNREAD_PROOF) == unread, (n, label)
            if unread:
                marked.add((n, label))
    assert marked == {(n, "Verified lower") for n in UNREAD_PROOF_CASES}
    row = frontier.case_row(cases[5], recent=False)
    assert (
        '<span class="site-frontier-same">✓ same</span>'
        '<span class="site-frontier-note site-cell-quiet">published proof, not read here'
        "</span></td>"
    ) in row
    # A read proof is not marked, with or without a defect found by the read.
    assert frontier.UNREAD_PROOF not in frontier.case_row(cases[13], recent=False)
    assert frontier.UNREAD_PROOF not in frontier.case_row(cases[8], recent=False)


def test_a_reported_bound_on_a_proof_found_defective_says_so(rows, cases) -> None:
    """A reported bound that stands on a proof whose read here found a defect, and that
    no verified bound reaches, says "defect recorded" under its credit: Nagamochi's
    closed form wherever it is above the verified floor (T-007), and Green's DS7 Theorem
    9 values. Where the verified bound equals the reported one, as at n = 13, 23 and 46,
    the defect moves no value on the row and the cell is not marked."""
    evidence = tables.load_evidence()
    flagged: dict[int, str] = {}
    for attributes, cells in rows:
        n = int(attributes["data-n"] or 0)
        for label, reported, verified in (
            ("Best known packing", "reported_upper_bound", "verified_upper_bound"),
            ("Reported lower", "reported_lower_bound", "verified_lower_bound"),
        ):
            words = cells[column(label)]["words"] or ""
            defect = tables.reported_defect(cases[n][reported], cases[n][verified], evidence)
            assert words.endswith(frontier.DEFECT_RECORDED) == defect, (n, label)
            if defect:
                flagged[n] = label
    assert set(flagged.values()) == {"Reported lower"}
    assert set(flagged) >= GREEN_THEOREM_9
    nagamochi = set(flagged) - GREEN_THEOREM_9
    assert all(
        cases[n]["reported_lower_bound"]["evidence"] == ["E-nagamochi-lower"] for n in nagamochi
    )
    # 149 of Nagamochi's values, all at n = 106 to 319, and Green's 30, on 2026-10-06.
    assert (len(nagamochi), min(nagamochi), max(nagamochi)) == (149, 106, 319)
    assert not {13, 23, 46} & set(flagged)


def test_status_names_each_verified_lane_and_marks_a_reported_defect(cases) -> None:
    """`STATUS.md` says who verified each lane apart, and whether a published proof was
    read here; until 2026-10-06 it merged the two lanes, and n = 5 read "replayed here,
    external proof" with nothing to say which half was the unread proof."""
    evidence = tables.load_evidence()
    assert tables.verification_origins(cases[5], evidence) == (
        "upper: replayed here; lower: external proof (not read here)"
    )
    assert tables.verification_origins(cases[106], evidence) == (
        "upper: replayed here; lower: external proof (read here), audited here"
    )
    assert "reported lower: defect recorded" in tables.case_disposition(cases[106], evidence)
    assert "defect recorded" not in tables.case_disposition(cases[23], evidence)
    status = tables.STATUS.read_text(encoding="utf-8")
    assert "| upper: replayed here; lower: external proof (not read here) |" in status


def test_the_gap_is_exact_where_both_bounds_are(rows, cases) -> None:
    gaps = {
        int(attributes["data-n"] or 0): cells[column("Gap")]["data-value"]
        for attributes, cells in rows
    }
    for n, case in cases.items():
        if case["status"] == "proved":
            assert gaps[n] == "0", n
    # s(12): verified upper 4, verified lower 7943/2000 since 5 October 2026 (T-095;
    # 15680000/3949423, 31360/7901 and 15680/3951 before it), so the gap is 57/2000.
    assert gaps[12] is not None
    assert abs(float(gaps[12]) - 57 / 2000) < 1e-15
    html_12, _ = frontier.gap(cases[12])
    assert r"\dfrac{57}{2000}" in html_12
    assert html_12.endswith('<span class="site-approx">= 0.0285</span>')


def _exact(form: str) -> Any:
    return frontier.exact_value(form)


def _holds(sign: str, digits: str, cut: str, value: Any) -> bool:
    """Whether a printed decimal is the exact `value`'s own: equal to it where the cell
    says `=`, and where it says `≈` the value cut, not rounded, after its last digit,
    which is to say at or under the value and less than one unit of that digit short.
    The comparison is made on the exact value, a rational as a fraction and a radical by
    the sign of an exact difference, never on a float."""
    import sympy  # noqa: PLC0415

    shown = sympy.Rational(Fraction(digits).numerator, Fraction(digits).denominator)
    if sign == "=":
        return cut == "" and sympy.simplify(value - shown) == 0
    places = len(digits.partition(".")[2])
    short = value - shown
    return (
        cut == "…"
        and places == frontier.DECIMAL_PLACES
        and bool(short > 0)
        and bool(short < sympy.Rational(1, 10**places))
    )


def test_a_closed_form_carries_its_decimal_and_the_decimal_is_the_exact_value(
    cases: dict[int, dict[str, Any]],
) -> None:
    """Every bound the table sets as a closed form that is not a whole number has its
    decimal under it, and the decimal is the closed form's value to the digits printed:
    the whole of it after `=`, cut and not rounded after `≈`. It is not the record's own
    decimal, which for a lower bound may be shorter (`15680/3951` is recorded as
    `3.968615`). A whole number and a bound already set as a decimal carry none."""
    seen = {"=": 0, "≈": 0, "": 0}
    for case in cases.values():
        for field in VALUE_COLUMNS.values():
            bound = case[field]
            shown = frontier.value_html(bound)
            under = frontier.bound_approx_html(bound)
            closed = "kpress-math" in shown
            if not closed:
                assert under == "", (case["n"], field)
                seen[""] += 1
                continue
            value = _exact(bound["exact_form"])
            if value.is_Integer:
                assert under == "", (case["n"], field)
                continue
            found = APPROX.fullmatch(under)
            assert found, (case["n"], field, under)
            sign, digits, cut = found.groups()
            assert _holds(sign, digits, cut, value), (case["n"], field, under)
            seen[sign] += 1
    assert all(seen.values()), seen
    # The owner's example, n = 12's reported lower bound 31360/7901 (T-078) as it stood
    # when it was set, and the three kinds of cell beside it.
    lower_12 = frontier.bound_approx_html({"value": "3.969117", "exact_form": "31360/7901"})
    assert lower_12 == '<span class="site-approx">≈ 3.96911783…</span>'
    assert frontier.bound_approx_html(cases[12]["reported_lower_bound"]) == (
        '<span class="site-approx">= 3.9715</span>'
    )
    assert frontier.bound_approx_html(cases[18]["reported_lower_bound"]) == (
        '<span class="site-approx">= 4.705</span>'
    )
    assert frontier.bound_approx_html(cases[5]["reported_upper_bound"]) == (
        '<span class="site-approx">≈ 2.70710678…</span>'
    )
    assert frontier.bound_approx_html(cases[12]["reported_upper_bound"]) == ""
    assert frontier.bound_approx_html(cases[11]["verified_lower_bound"]) == ""


def test_the_tables_cells_carry_those_decimals(page: str, cases) -> None:
    """The rendered rows hold them: under each closed form in the four bound columns,
    and under a gap that is not a whole number."""
    row_12 = page[page.index('<tr id="n-12"') : page.index('<tr id="n-13"')]
    # Since 5 October 2026 the verified lower bound equals the reported one (T-095), so
    # the verified cell shows no second decimal, and the gap is the terminating 57/2000.
    assert [found.group(0) for found in APPROX.finditer(row_12)] == [
        '<span class="site-approx">= 3.9715</span>',
        '<span class="site-approx">= 0.0285</span>',
    ]
    assert "<mfrac><mrow><mn>7943</mn></mrow><mrow><mn>2000</mn></mrow></mfrac>" in row_12
    assert "<mfrac><mrow><mn>57</mn></mrow><mrow><mn>2000</mn></mrow></mfrac>" in row_12
    table = page[page.index("<tbody>") : page.index("</tbody>")]
    expected = sum(
        bool(frontier.bound_approx_html(case[field]))
        for case in cases.values()
        for field, reported in (
            ("reported_upper_bound", None),
            ("reported_lower_bound", None),
            ("verified_upper_bound", "reported_upper_bound"),
            ("verified_lower_bound", "reported_lower_bound"),
        )
        if reported is None
        or not bounds_agree_at_declared_precision(case[reported], case[field])
    ) + sum("site-approx" in frontier.gap(case)[0] for case in cases.values())
    assert len(APPROX.findall(table)) == table.count("site-approx") == expected


def test_an_exact_decimal_is_cut_from_the_exact_value_or_not_printed() -> None:
    import sympy  # noqa: PLC0415

    assert frontier.exact_decimal(sympy.Rational(939, 200)) == ("4.695", True)
    assert frontier.exact_decimal(sympy.Rational(24, 5)) == ("4.8", True)
    assert frontier.exact_decimal(sympy.Rational(15680, 3951)) == ("3.96861554…", False)
    # Cut, where rounding would print 0.66666667.
    assert frontier.exact_decimal(sympy.Rational(2, 3)) == ("0.66666666…", False)
    # Nine places: one more than the cell prints, so it is cut and says so.
    assert frontier.exact_decimal(sympy.Rational(123456789, 10**9)) == ("0.12345678…", False)
    assert frontier.exact_decimal(2 + sympy.sqrt(2) / 2) == ("2.70710678…", False)
    # A value whose digits past the cut are all zeros as far as they were computed could
    # be either side of the cut; the render stops.
    with pytest.raises(SystemExit, match="too close"):
        frontier.exact_decimal(1 + sympy.sqrt(2) / 10**40)


def test_an_invalid_record_fails_the_render(tmp_path: Path, monkeypatch) -> None:
    source = tables.FRONTIER / "n-012.md"
    shutil.copy(tables.FRONTIER / "square-packing-case.schema.yaml", tmp_path)
    text = source.read_text(encoding="utf-8")
    front = safe_load(text.split("---\n")[1])
    assert front["packing"]["status"] == "open"
    broken = text.replace("\n  status: open\n", "\n  status: unknown\n", 1)
    assert broken != text
    (tmp_path / "n-012.md").write_text(broken, encoding="utf-8")
    monkeypatch.setattr(tables, "FRONTIER", tmp_path)
    with pytest.raises(SystemExit, match=r"n-012\.md is not a valid case record"):
        frontier.frontier_cases()


def test_the_page_fetches_only_the_shared_assets_and_is_under_its_ceiling(page: str) -> None:
    assert_fetches_only_assets("frontier.html", page)
    # Each file it names is one the build writes beside it.
    assert site_assets.shared().assets.referenced([page])
    size = len(page.encode("utf-8"))
    assert size < PAGE_CEILING_BYTES, f"frontier.html is {size:,} bytes"
    # KPress's per-cell column labels, which nothing on the site reads, are dropped.
    assert "data-col=" not in page
    assert "data-col-index=" not in page


def test_the_page_carries_the_table_script_and_its_controls(page: str, served: str) -> None:
    table = site_assets.shared().assets.script_file(frontier.TABLE_SCRIPT)
    assert page.count(site_assets.script_tag(table, "frontier.html")) == 1
    assert frontier.TABLE_SCRIPT.read_text(encoding="utf-8") in served
    assert 'class="site-table-tools" data-table="frontier" hidden' in page
    assert 'aria-current="page" href="frontier.html"' in page


def test_an_evidence_name_and_its_comma_are_one_box() -> None:
    """Each evidence identifier links to its entry and sits, with the comma after it, in
    one `.site-name` box, so a line breaks between names and never on a hyphen inside
    one; the text reads as it always did."""
    known = list(frontier.evidence_lines())[:3]
    links = frontier.evidence_links([*known, known[0]])
    boxes = re.findall(r'<span class="site-name">(.*?)</span>', links)
    assert [re.sub(r"<[^>]+>", "", box) for box in boxes] == [
        f"{known[0]},",
        f"{known[1]},",
        known[2],
    ]
    assert re.sub(r"<[^>]+>", "", links) == ", ".join(known)
    assert all(box.startswith('<a href="') and "<code>" in box for box in boxes)
    (one,) = re.findall(
        r'<span class="site-name">(.*?)</span>', frontier.evidence_links(known[:1])
    )
    assert one.endswith("</code></a>")


def test_a_row_opens_its_case_record(cases: dict[int, dict[str, Any]]) -> None:
    """A frontier row's cells hold no disclosure, and the row has no popover of its own:
    the whole row opens its case's record in the page's one case popover, the visual
    summary and then the record's further data, as the atlas does (think-necq). The row
    names its record file for that popover, keeps its `n` a link to the same record,
    and links the case file in the Records cell. The table carries one popover, the
    case popover, after it."""
    row = frontier.case_row(cases[11], recent=True)
    assert "<details" not in row
    assert "<dl" not in row
    assert row.startswith('<tr id="n-11" data-n="11" ')
    assert 'data-case-row="11" data-case-href="cases/11.html"' in row
    assert 'aria-label="n = 11, proved: open its case record"' in row
    assert "data-row-popover" not in row
    assert "site-row-open" not in row
    assert 'href="cases/11.html" data-case="11"' in row
    assert ">n-011.md</a>" in row
    assert '<a class="site-cell-quiet" href="cases/11.html" data-case="11">Record</a>' in row
    table = frontier.table_html([cases[11], cases[12]])
    assert table.count('<div class="site-popover') == 1
    assert table.index("</table>") < table.index('id="pop-case"')
    assert "<details" not in table


def test_no_math_is_left_as_source_text_in_the_table(page: str) -> None:
    table = page[page.index("<tbody>") : page.index("</tbody>")]
    assert "$" not in table
    assert "sqrt(" not in table
    assert 'class="katex"' in table
    assert "<math" in table
    assert r"\(\dfrac{7943}{2000}\)" not in table


def test_the_frontier_inputs_are_render_inputs() -> None:
    for path in frontier.FRONTIER_INPUTS:
        assert path in render_overview.inputs()
        assert path.exists(), path


@pytest.mark.parametrize(
    ("form", "tex"),
    [
        ("31/8", r"\frac{31}{8}"),
        ("2 + (1/2)sqrt(2)", r"2 + \frac{1}{2}\sqrt{2}"),
        ("4 + 2 sqrt(2)", r"4 + 2\sqrt{2}"),
        ("sqrt(37 - 2*floor(sqrt(37)) + 1) + 1", r"1 + \sqrt{26}"),
        ("94*sqrt(2)/41 + 247/41", r"\frac{94\sqrt{2}}{41} + \frac{247}{41}"),
        (
            "7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))",
            r"7 - \frac{1}{2}\sqrt{2} + \sqrt{1 + \sqrt{2}}",
        ),
    ],
)
def test_exact_forms_render_as_latex(form: str, tex: str) -> None:
    assert tables.latex(form) == tex


def test_a_polynomial_root_has_no_closed_form() -> None:
    with pytest.raises(ValueError, match="polynomial root"):
        tables.latex("root(P_trump11, 3.877)")
    bound = {"value": "3.87708359002281417730789706010096", "exact_form": "root(P, 3.877)"}
    assert "3.87708359…" in frontier.value_html(bound)


def test_every_thumbnail_draws_its_cases_squares() -> None:
    image = frontier.thumbnail_svg(11)
    assert 'src="atlas/house/n-11.svg" width="50" height="50"' in image
    svg = frontier.drawing_files()[frontier.drawing_path(11)].decode()
    assert svg.count("z") == 11
    assert 'xmlns="http://www.w3.org/2000/svg"' in svg
    assert "id=" not in svg


def test_a_minimal_polynomial_with_radical_coefficients_renders_as_latex() -> None:
    tex = tables.polynomial_latex("24s^4-(1400+352sqrt(2))s^3+641430=0")
    assert tex == r"24s^4-(1400+352\sqrt{2})s^3+641430=0"
    with pytest.raises(ValueError, match="no LaTeX form"):
        tables.polynomial_latex("s^2 - log(2) = 0")
