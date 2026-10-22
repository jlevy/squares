"""Current-record counts retain explicit uncertainty on every presentation surface."""

from devtools.profile_records import RecordFacet, RecordIndex
from devtools.record_presentation import record_tally


def test_supported_current_records_and_pending_facets_are_both_visible() -> None:
    index = RecordIndex(
        ("known",),
        {"known": (RecordFacet("bound"),)},
        {"known": ("one comparison pending",), "unknown": ("date tie",)},
    )
    rendered = record_tally(
        ("known", "unknown", "known"),
        {"known": (5, ""), "unknown": (4, "")},
        index=index,
        total_href="person.html#records",
        pending_href="person.html#records",
    )
    assert '>1 record</a> <span class="site-tally-levels">(at S5)</span>' in rendered
    assert "Review pending" in rendered
    assert "unknown: date tie" in rendered
    assert "one comparison pending" not in rendered
    assert 'href="person.html#records"' in rendered


def test_unknown_is_not_zero_and_known_zero_can_be_blank() -> None:
    uncertain = RecordIndex((), {}, {"a": ('source "date" <unknown>',)})
    rendered = record_tally(("a",), {"a": (5, "")}, index=uncertain, blank_zero=True)
    assert "Review pending" in rendered
    assert "0 record" not in rendered
    assert "&quot;date&quot; &lt;unknown&gt;" in rendered
    assert record_tally((), {}, index=RecordIndex((), {}, {}), blank_zero=True) == ""


def test_a_known_current_result_with_an_uncertain_extra_facet_has_no_pending_count() -> None:
    index = RecordIndex(("a",), {"a": (RecordFacet("bound"),)}, {"a": ("other case tied",)})
    rendered = record_tally(("a",), {"a": (4, "")}, index=index)
    assert rendered == '1 record <span class="site-tally-levels">(at S4)</span>'
    assert "Review pending" not in rendered
