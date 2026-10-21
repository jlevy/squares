"""Authored people links stay exact, local and separate from reviewed source credits."""

import re
from pathlib import Path

import pytest

from devtools import render_case_pages, render_frontier_page, render_overview, site_documents
from devtools.profile_links import audit_site, link_prose, profile_index, profile_names


def test_profile_links_preserve_text_boundaries_and_explicit_context() -> None:
    index = profile_index(
        {
            "alice": {
                "display_name": "Alice Example",
                "surname": "Example",
                "real_name": "Alice Example",
                "aliases": ["Example", "alice-old"],
                "links": [
                    {"kind": "github", "url": "https://github.com/alice", "handle": "alice"}
                ],
            },
            "bob": {"display_name": "Bob Person", "surname": "Person"},
        }
    )
    source = (
        "Alice Example\u2019s proof with Bob Person; Example and alice-old remain. "
        "Alice Exampleton and preAlice Example stay unchanged. "
        '<a href="https://github.com/alice">Alice Example</a> '
        '<a href="https://github.com/alice">source repository</a> '
        '<a href="https://example.org/paper">Bob Person</a> '
        "<code>Alice Example</code><math><mi>Bob Person</mi></math>"
        "<blockquote>Alice Example</blockquote><q>Bob Person</q>"
        "<table><tr><td>Alice Example</td></tr></table>"
    )
    rendered = link_prose(source, index=index, prefix="../")
    assert rendered.startswith(
        '<a href="../profiles/alice.html">Example</a>\u2019s proof with '
        '<a href="../profiles/bob.html">Person</a>'
    )
    assert (
        '<a href="../profiles/alice.html">Example</a> '
        '<a href="https://github.com/alice">source repository</a>' in rendered
    )
    assert source[source.index('<a href="https://example.org/paper">') :] in rendered
    assert "Example and alice-old remain" in rendered
    assert "Alice Exampleton and preAlice Example stay unchanged" in rendered
    assert link_prose(rendered, index=index, prefix="../") == rendered
    own = link_prose("Alice Example and Bob Person", index=index, current_profile="alice")
    assert own.startswith("Alice Example and <a")
    assert link_prose("Alice\nExample", index=index) == (
        '<a href="profiles/alice.html">Example</a>'
    )


def test_profile_links_reject_name_collisions() -> None:
    index = profile_index(
        {
            "one": {"display_name": "Same Name"},
            "two": {"display_name": "Same  Name"},
            "other": {"display_name": "Other Person"},
        }
    )
    assert link_prose("Same Name and Same  Name", index=index) == "Same Name and Same  Name"


def test_account_retarget_preserves_other_attributes_and_unicode_names() -> None:
    index = profile_index(
        {
            "alice": {
                "display_name": "Alice Example",
                "surname": "Example",
                "links": [
                    {"kind": "github", "url": "https://github.com/alice", "handle": "alice"}
                ],
            }
        }
    )
    source = (
        '<a data-href="keep" title="href=&quot;keep too&quot;" '
        'href="https://github.com/alice">Alice Example</a>'
    )
    assert link_prose(source, index=index) == source.replace(
        'href="https://github.com/alice"', 'href="profiles/alice.html"'
    ).replace(">Alice Example</a>", ">Example</a>")
    assert link_prose("Al\u0131ce Example and ALICE EXAMPLE", index=index) == (
        "Al\u0131ce Example and ALICE EXAMPLE"
    )


def test_converted_account_links_keep_native_same_tab_navigation() -> None:
    index = profile_index(
        {
            "alice": {
                "display_name": "Alice Example",
                "surname": "Example",
                "links": [
                    {"kind": "github", "url": "https://github.com/alice", "handle": "alice"}
                ],
            }
        }
    )
    source = (
        '<a href="https://github.com/alice" target="_blank" rel="noopener">Alice Example</a>'
    )
    converted = link_prose(source, index=index)
    assert 'href="profiles/alice.html"' in converted
    assert "target=" not in converted
    assert 'rel="noopener"' in converted


def test_authored_about_and_explanations_link_reviewed_people_directly() -> None:
    about = render_overview.about_page().html
    narrative = about.split('<h1 id="profiles"', 1)[0]
    for identifier in (
        "joshua-levy",
        "marc-leonard-overbeck",
        "manasseh-ahmed",
        "evan-daniel",
        "oscar-fitzharding",
    ):
        assert f'href="profiles/{identifier}.html"' in narrative
    assert "site-profile-prose" not in about
    papers = render_overview.papers_page().html
    assert 'href="profiles/manasseh-ahmed.html"' in papers
    assert 'href="profiles/marc-leonard-overbeck.html"' in papers
    for markup in (about, papers):
        for anchor in re.findall(r'<a\b[^>]*href="profiles/[^" ]+"[^>]*>', markup):
            assert 'target="_blank"' not in anchor


def test_case_and_reader_boundaries_preserve_nested_math_and_source_regions() -> None:
    math = '<div class="kpress-math"><div><math><mi>Evan Daniel</mi></math></div></div>'
    body = "<p>Evan\nDaniel</p>" + math + "<p>Hiroaki Hosono</p>"
    source = '<div class="site-case-data">Evan Daniel</div>'
    source += '<div class="site-case-prose"><!-- profile-prose -->' + body
    source += "<!-- /profile-prose --></div>"
    linked = render_case_pages._profile_prose(source)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert linked.startswith('<div class="site-case-data">Evan Daniel</div>')
    assert '<a href="profiles/evan-daniel.html">Daniel</a>' in linked
    assert '<a href="profiles/hiroaki-hosono.html">Hosono</a>' in linked
    assert math in linked
    assert "<!-- profile-prose -->" not in linked
    reader = "<header>Evan Daniel</header><article><p>Evan Daniel</p>"
    reader += "<table><tr><td>Hiroaki Hosono</td></tr></table></article>"
    linked_reader = site_documents._reader_profile_links(reader)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert linked_reader.startswith("<header>Evan Daniel</header>")
    assert '<a href="profiles/evan-daniel.html">Daniel</a>' in linked_reader
    assert "<td>Hiroaki Hosono</td>" in linked_reader


def test_case_profile_href_compaction_preserves_anchors_and_other_attributes() -> None:
    source = (
        '<article class="site-case"><a data-href="keep" '
        'href="../profiles/evan-daniel.html" title="Profile link">Daniel</a>'
        '<math><mi class="mord">x</mi></math></article>'
    )
    compact = render_case_pages.compact_visual_math_classes(source, profile_links=True)
    assert 'href=../profiles/evan-daniel.html title="Profile link"' in compact
    assert 'data-href="keep"' in compact
    assert '<article class="site-case">' in compact
    assert '<math><mi class="mord">x</mi></math>' in compact


def test_lower_bound_scope_links_people_without_changing_reviewed_credits() -> None:
    case = next(case for case in render_frontier_page.frontier_cases() if case["n"] == 104)
    panel = render_case_pages._lower_panel(case)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert '<a href="profiles/hiroaki-hosono.html">Hosono</a>' in panel
    assert "data-person" in panel


def test_surname_labels_use_registry_wide_collisions_and_explicit_order() -> None:
    metadata = {
        "ryu": {"display_name": "Ryu Sungjoon", "surname": "Ryu"},
        "alice": {"display_name": "Alice Example", "surname": "Example"},
        "bob": {"display_name": "Bob Example", "surname": "example"},
        "mira": {"display_name": "Mira", "links": [{"kind": "github", "handle": "Mira-acc"}]},
        "unknown": {"display_name": "Single Public Handle"},
    }
    names = profile_names(metadata)
    assert names["alice"].label == "Alice Example"
    assert names["bob"].label == "Bob Example"
    assert names["ryu"].label == "Ryu"
    assert names["mira"].label == "Mira-acc"
    assert names["unknown"].label == "Single Public Handle"
    assert sorted(names, key=lambda identifier: names[identifier].sort_key) == [
        "alice",
        "bob",
        "mira",
        "ryu",
        "unknown",
    ]
    duplicate = profile_names(
        {
            "one": {
                "display_name": "Same Person",
                "surname": "Person",
                "links": [{"kind": "github", "handle": "one"}],
            },
            "two": {
                "display_name": "Same Person",
                "surname": "Person",
                "links": [{"kind": "github", "handle": "two"}],
            },
        }
    )
    assert {name.label for name in duplicate.values()} == {
        "Same Person (one)",
        "Same Person (two)",
    }
    collision = profile_names(
        {
            "person": {"display_name": "Ryan Xu", "surname": "Xu"},
            "handle": {"display_name": "Xu"},
        }
    )
    assert collision["person"].label == "Ryan Xu"
    assert collision["handle"].label == "Xu"


def test_known_profile_labels_preserve_identity_paths_possessives_and_protected_text() -> None:
    index = profile_index({"alice": {"display_name": "Alice Example", "surname": "Example"}})
    source = (
        '<p>Alice Example\u2019s, <a href="../profiles/alice.html?q=1#work">'
        "<strong>Alice Example\u2019s</strong></a> proof.</p>"
    )
    expected = (
        '<p><a href="profiles/alice.html">Example</a>\u2019s, '
        '<a href="../profiles/alice.html?q=1#work"><strong>Example</strong></a>'
        "\u2019s proof.</p>"
    )
    assert link_prose(source, index=index) == expected
    assert link_prose(expected, index=index) == expected
    assert link_prose(
        '<a href="profiles/alice.html">Alice Example&#8217;s</a>', index=index
    ) == ('<a href="profiles/alice.html">Example</a>\u2019s')
    protected = (
        "<h2>Alice Example</h2><blockquote>"
        '<a href="profiles/alice.html">Alice Example</a></blockquote>'
        '<details class="site-contributor-sources"><summary>Sources</summary>'
        "Alice Example</details>"
        '<a href="https://other.example/profiles/alice.html">Alice Example</a>'
        '<a href="profiles/alice.html">original proof</a>'
    )
    assert link_prose(protected, index=index) == protected
    assert (
        link_prose("Example and Alice Exampleton", index=index)
        == "Example and Alice Exampleton"
    )


def test_generated_profile_label_audit_keeps_protected_contexts_separate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    index = profile_index({"alice": {"display_name": "Alice Example", "surname": "Example"}})
    monkeypatch.setattr("devtools.profile_links.public_index", lambda: index)
    full = '<a href="profiles/alice.html">Alice Example</a>'
    (tmp_path / "index.html").write_text(
        full
        + '<a href="profiles/alice.html">Example</a>'
        + "<h2>"
        + full
        + "</h2>"
        + '<details class="site-contributor-sources">'
        + full
        + "</details>"
        + '<table class="site-profile-table"><tr><td>'
        + full
        + "</td></tr></table>"
        + "<blockquote>"
        + full
        + "</blockquote>"
        + '<a href="https://other.example/profiles/alice.html">Alice Example</a>'
    )
    assert audit_site(tmp_path)["profile_link_label_mismatches"] == {"index.html": {"alice": 1}}
