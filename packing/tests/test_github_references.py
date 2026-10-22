"""Issue and PR references require exact retained URLs and explicit evidence joins."""

from __future__ import annotations

import xml.etree.ElementTree as ET

import pytest

from devtools.github_references import (
    credit_reference_urls,
    github_references,
    parse_github_reference,
    render_github_references,
)
from devtools.site_icons import github_reference_icon


def test_exact_github_thread_urls_preserve_comment_targets() -> None:
    url = "https://github.com/Octo/pack.ing/issues/23#issuecomment-99"
    reference = parse_github_reference(url)
    assert reference is not None
    assert (reference.repository, reference.kind, reference.number, reference.url) == (
        "Octo/pack.ing",
        "issue",
        23,
        url,
    )
    pull = parse_github_reference("https://github.com/owner/repo/pull/17/")
    assert pull is not None
    assert (pull.repository, pull.kind, pull.number) == ("owner/repo", "pull-request", 17)


@pytest.mark.parametrize(
    "url",
    [
        "http://github.com/owner/repo/issues/1",
        "https://github.com.evil.test/owner/repo/issues/1",
        "https://evil.test/github.com/owner/repo/issues/1",
        "https://user@github.com/owner/repo/issues/1",
        "https://github.com:443/owner/repo/issues/1",
        "//github.com/owner/repo/issues/1",
        "https://github.com/owner/repo/issues/0",
        "https://github.com/owner/repo/issues/001",
        "https://github.com/owner/repo/issues/1/extra",
        "https://github.com/owner/../issues/1",
        "https://github.com/owner/repo%2fpull%2f3/issues/1",
        "https://github.com/owner/repo/issues/1\n",
        "https://github.com/owner/repo/issues/1\\@evil.test",
        "https://[github.com/owner/repo/issues/1",
        "Issue #17",
        "https://github.com/owner/repo",
    ],
)
def test_non_thread_and_ambiguous_urls_are_not_rendered(url: str) -> None:
    assert parse_github_reference(url) is None
    assert render_github_references([url]) == ""


def test_duplicate_threads_keep_first_evidence_url_and_distinct_repositories() -> None:
    references = github_references(
        [
            "https://github.com/Owner/Repo/issues/17#issuecomment-2",
            "https://github.com/owner/repo/issues/17",
            "https://github.com/other/repo/issues/17",
            "https://github.com/owner/repo/pull/18",
        ]
    )
    assert [(ref.repository, ref.kind, ref.number) for ref in references] == [
        ("Owner/Repo", "issue", 17),
        ("other/repo", "issue", 17),
        ("owner/repo", "pull-request", 18),
    ]
    assert references[0].url.endswith("#issuecomment-2")


def test_links_use_accessible_repository_type_labels_and_escape_attributes() -> None:
    rendered = render_github_references(
        [
            'https://github.com/owner/repo/issues/17?x="quoted"&y=<tag>',
            "https://github.com/owner/repo/pull/18",
        ],
        class_name='reference" onclick="bad',
    )
    assert 'aria-label="GitHub issue owner/repo#17"' in rendered
    assert 'aria-label="GitHub pull request owner/repo#18"' in rendered
    assert "&quot;quoted&quot;&amp;y=&lt;tag&gt;" in rendered
    assert 'class="reference&quot; onclick=&quot;bad"' in rendered
    assert "</svg> #17</a>" in rendered
    assert "</svg> #18</a>" in rendered
    assert "<script" not in rendered
    assert "<use" not in rendered
    assert rendered.count('aria-hidden="true"') == 2
    ET.fromstring("<div>" + rendered.replace("&nbsp;", "&#160;") + "</div>")


def test_issue_and_pull_icons_share_canonical_lucide_geometry() -> None:
    issue = ET.fromstring(github_reference_icon("issue"))
    pull = ET.fromstring(github_reference_icon("pull-request"))
    assert issue.attrib["viewBox"] == pull.attrib["viewBox"] == "0 0 24 24"
    assert [circle.attrib for circle in issue] == [
        {"cx": "12", "cy": "12", "r": "10"},
        {"cx": "12", "cy": "12", "r": "1"},
    ]
    assert [child.tag.rsplit("}", 1)[-1] for child in pull] == [
        "circle",
        "circle",
        "path",
        "line",
    ]
    assert pull[2].attrib["d"] == "M13 6h3a2 2 0 0 1 2 2v7"
    assert issue.attrib["stroke"] == pull.attrib["stroke"] == "currentColor"
    assert issue.attrib["aria-hidden"] == pull.attrib["aria-hidden"] == "true"
    assert issue.attrib["class"] == pull.attrib["class"] == "site-account-icon"
    assert issue.attrib["focusable"] == pull.attrib["focusable"] == "false"
    with pytest.raises(ValueError, match="GitHub reference kind"):
        github_reference_icon("commit")


def test_credit_urls_follow_only_explicit_source_and_result_joins() -> None:
    coverage = {
        "sources": [
            {"source_key": "credited", "url": "https://github.com/research/packing/issues/3"},
            {"source_key": "repository-only", "url": "https://github.com/research/packing"},
            {"source_key": "unrelated", "url": "https://github.com/elsewhere/work/issues/9"},
        ]
    }
    changelog = {
        "repository": "https://github.com/jlevy/squares",
        "entries": [
            {
                "result_ids": ["T-1"],
                "pull_requests": [12],
                "references": [
                    {"target": "https://github.com/research/packing/issues/3"},
                    {"target": "https://github.com/jlevy/squares/issues/2#issuecomment-7"},
                    {"target": "packing/frontier/n-011.md"},
                ],
            },
            {"result_ids": ["T-2"], "pull_requests": [13]},
            {"pull_requests": [14], "summary": "T-1 has no explicit association here."},
        ],
    }
    found = credit_reference_urls(
        {"credited", "repository-only"}, {"T-1"}, coverage=coverage, changelog=changelog
    )
    assert found.sources == ("https://github.com/research/packing/issues/3",)
    assert found.registrations == ("https://github.com/jlevy/squares/pull/12",)
    assert found.supporting == (
        "https://github.com/research/packing/issues/3",
        "https://github.com/jlevy/squares/issues/2#issuecomment-7",
    )
    empty = credit_reference_urls(set(), set(), coverage=coverage, changelog=changelog)
    assert empty.sources == empty.registrations == empty.supporting == ()
