"""Changelog reader, publication boundaries, and merged-PR authoring behavior."""

from __future__ import annotations

import copy
import html
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote, urlsplit

import pytest
import yaml
from kpress.format.markdown import parse_markdown

from devtools import (
    import_changelog,
    render_changelog,
    render_overview,
    site_math,
)
from devtools.repo_links import repo_url


def document() -> dict:
    data = {
        "softschema": {
            "contract": "packing.squares:SiteChangelog/v1",
            "schema": "site-changelog.schema.yaml",
            "status": "enforced",
        },
        "repository": "https://github.com/jlevy/squares",
        "deliveries": [
            {
                "number": number,
                "title": f"Contribution {number}",
                "merged_at": day + "T12:00:00Z",
                "base_ref": "main",
                "merge_commit": "a" * 40,
                **({"stack_id": 498} if number != 553 else {}),
            }
            for number, day in [
                (553, "2026-10-12"),
                (497, "2026-10-12"),
                (509, "2026-10-13"),
                (549, "2026-10-14"),
            ]
        ],
        "stacks": [
            {
                "id": 498,
                "pull_requests": [497, 509, 549],
                "evidence": "https://github.com/jlevy/squares/pull/498",
            }
        ],
        "coverage": {"pull_requests": [497, 509, 549, 553], "omissions": []},
        "entries": [
            {
                "id": "admission",
                "date": "2026-10-12",
                "title": "Replayed certificates",
                "pull_requests": [553],
                "summary": "Admitted **verified** bounds for $n = 304$.",
                "references": [
                    {"label": "Evidence", "target": "packing/frontier/results.yaml"}
                ],
            },
            {
                "id": "foundations",
                "date": "2026-10-13",
                "title": "Regularization & tooling",
                "pull_requests": [497, 509],
                "stack_id": 498,
                "summary": "Retained the [policy]"
                "(docs/project/policies/regularization-policy.md).",
                "details": "- Comparison tool\n- Provenance\n  - Pinned source",
            },
            {
                "id": "later-delivery",
                "date": "2026-10-14",
                "title": "Driver",
                "pull_requests": [549],
                "stack_id": 498,
                "summary": "Added the driver.",
            },
        ],
        "frozen_entries": [
            {"id": "foundations", "date": "2026-10-13", "pull_requests": [497, 509]}
        ],
    }

    for entry in data["entries"]:
        entry["significance"] = {
            "score": 3,
            "rationale": "A focused public tooling improvement.",
        }
    return data


def test_news_title_math_uses_the_escaped_register_headline_boundary() -> None:
    data = document()
    title = "Initial Review of proofs for n = 17 <script>forbidden</script>"
    data["entries"][0]["title"] = title
    rendered = render_changelog.render_news(data)
    article = rendered.split('data-news-entry="admission">', 1)[1].split("</article>", 1)[0]
    header = article.split("<h3>", 1)[1].split("</h3>", 1)[0]
    assert [formula.source for formula in site_math.formula_sources(header)] == ["n = 17"]
    assert "<math" in header
    assert "<mi>n</mi>" in header
    assert "<mn>17</mn>" in header
    assert "&lt;script&gt;forbidden&lt;/script&gt;" in header
    assert "<script>" not in header
    assert "$" not in header


def test_authored_headline_markdown_and_math_survive_archive_and_preview() -> None:
    data = document()
    entry = render_changelog.ordered_entries(data)[0]
    entry["title"] = r"**A bound** for $n = 17$: $s(n) \ge \sqrt{n}$ and `T-154`"
    anchor = render_changelog.entry_anchor(entry["id"])
    for limit in (None, 1):
        rendered = render_changelog.render_news(data, limit=limit)
        header = rendered.split("<h3>", 1)[1].split("</h3>", 1)[0]
        assert "<strong>A bound</strong>" in header
        assert "<code>T-154</code>" in header
        assert "<msqrt>" in header
        assert "$" not in header
        assert [formula.source for formula in site_math.formula_sources(header)] == [
            "n = 17",
            r"s(n) \ge \sqrt{n}",
        ]
        if limit is not None:
            assert header.startswith(f'<a href="news.html#{anchor}">')
            assert header.count("<a ") == 1
    site = render_changelog.render_markdown(data, destination="site")
    assert f'<h4 id="{anchor}"><strong>A bound</strong>' in site
    assert "<msqrt>" in site


def test_inline_markdown_keeps_safe_links_and_escaped_literals_distinct() -> None:
    rendered = render_changelog.inline_html(
        r"*Reviewed* [policy](README.md), `T-154`, \[literal](https://example.com), "
        r"<script>forbidden</script>; $N \ne n$ and n = 17."
    )
    assert "<em>Reviewed</em>" in rendered
    assert f'<a href="{repo_url("README.md")}">policy</a>' in rendered
    assert "<code>T-154</code>" in rendered
    assert "[literal](https://example.com)" in rendered
    assert "&lt;script&gt;forbidden&lt;/script&gt;" in rendered
    assert "<script>" not in rendered
    assert rendered.count("<a ") == 1
    assert [formula.source for formula in site_math.formula_sources(rendered)] == [
        r"N \ne n",
        "n = 17",
    ]
    for payload in (
        "[bad](javascript:alert%281%29)",
        r"$\href{javascript:alert(1)}{X}$",
        '[text](https://example.com){onclick="forbidden"}',
        "![image](https://example.com/image.png)",
    ):
        with pytest.raises(ValueError, match=r"unsafe|attributes|images"):
            render_changelog.inline_html(payload)
    for linked in (
        "[source](https://example.com/proof)",
        r"$\href{https://example.com/proof}{X}$",
    ):
        with pytest.raises(ValueError, match="links are not allowed"):
            render_changelog.inline_html(linked, allow_links=False)

    names = (
        '[John Bidwell](<https://example.org/John Bidwell> "John Bidwell"); '
        r"`John Bidwell`; $\text{John Bidwell}$; John Bidwell."
    )
    rendered_names = render_changelog.inline_html(names)
    assert (
        '<a href="https://example.org/John%20Bidwell" title="John Bidwell">John Bidwell</a>'
        in rendered_names
    )
    assert "<code>John Bidwell</code>" in rendered_names
    assert [formula.source for formula in site_math.formula_sources(rendered_names)] == [
        r"\text{John Bidwell}"
    ]
    assert rendered_names.endswith("; John Bidwell.")


def test_shared_renderer_orders_links_math_and_anchors() -> None:
    data = document()
    render_changelog.validate(data)
    github = render_changelog.render_markdown(data)
    site = render_changelog.render_markdown(data, destination="site")
    for text in (github, site):
        assert text.index("2026-10-14") < text.index("2026-10-13") < text.index("2026-10-12")
        assert 'id="changelog-entry-foundations"' in text
        assert "https://github.com/jlevy/squares/pull/497" in text
    assert "$n = 304$" in github
    assert "  - Pinned source" in github
    assert "<math" in site
    assert "Pinned source" in site
    assert "[Evidence](packing/frontier/results.yaml)" in github
    assert (
        "[Evidence](https://github.com/jlevy/squares/blob/main/packing/frontier/results.yaml)"
        in site
    )
    assert (
        "https://github.com/jlevy/squares/blob/main/docs/project/policies/regularization-policy.md"
        in site
    )
    assert "Regularization &amp; tooling" in github


def test_one_delivery_can_support_distinct_articles_and_complete_audit() -> None:
    data = document()
    previous = copy.deepcopy(data)
    second = copy.deepcopy(data["entries"][0])
    second.update(id="second-admission", title="Another result", summary="A distinct result.")
    data["entries"].append(second)
    render_changelog.validate(data)
    render_changelog.validate_frozen(data, previous)

    news = render_changelog.render_news(data)
    for identifier in ("admission", "second-admission"):
        assert news.count(f'data-news-entry="{identifier}"') == 1
    audit = import_changelog.coverage_audit(data)
    assert audit.count("| [#553](") == 1
    assert "| admission, second-admission |" in audit

    delivery = data["deliveries"][0]
    row = {
        "number": delivery["number"],
        "title": delivery["title"],
        "state": "MERGED",
        "mergedAt": delivery["merged_at"],
        "baseRefName": delivery["base_ref"],
        "mergeCommit": {"oid": delivery["merge_commit"]},
    }
    candidate = import_changelog.draft([row], data)
    for field in ("entries", "deliveries", "coverage"):
        assert candidate[field] == data[field]
    remaining = copy.deepcopy(data)
    remaining["entries"].pop()
    render_changelog.validate(remaining)
    with pytest.raises(ValueError, match="frozen entry second-admission"):
        render_changelog.validate_frozen(remaining, data)


def test_shared_delivery_keeps_identity_date_stack_and_coverage_boundaries() -> None:
    mutations = [
        (
            lambda d: d["deliveries"].append(copy.deepcopy(d["deliveries"][0])),
            "duplicate retained",
        ),
        (lambda d: d["entries"][-1].update(id="admission"), "duplicate entry"),
        (lambda d: d["entries"][-1].update(pull_requests=[553, 553]), "non-unique"),
        (lambda d: d["entries"][-1].update(pull_requests=[999]), "no retained"),
        (lambda d: d["entries"][-1].update(date="2026-10-11"), "latest merge date"),
        (lambda d: d["entries"][-1].update(stack_id=498), "stack disagrees"),
        (lambda d: d["coverage"]["pull_requests"].pop(), "coverage"),
        (
            lambda d: d["coverage"]["omissions"].append(
                {"pull_request": 553, "reason": "Already announced"}
            ),
            "coverage",
        ),
    ]
    for mutate, message in mutations:
        data = document()
        second = copy.deepcopy(data["entries"][0])
        second["id"] = "second-admission"
        data["entries"].append(second)
        mutate(data)
        with pytest.raises(ValueError, match=message):
            render_changelog.validate(data)


def test_semantic_negative_boundaries() -> None:
    mutations = [
        (lambda d: d["entries"][0].update(date="2026-02-30"), "calendar date"),
        (lambda d: d["entries"][0].update(date="2026-10-11"), "latest merge date"),
        (lambda d: d["entries"][2].update(pull_requests=[553]), "PR #553"),
        (lambda d: d["entries"][0].update(id="foundations"), "duplicate entry"),
        (lambda d: d["deliveries"][0].update(base_ref="feature"), "main"),
        (lambda d: d["deliveries"][0].update(merged_at=None), "merged_at"),
        (lambda d: d["entries"][1].update(stack_id=999), "stack"),
        (
            lambda d: d["entries"][1].update(pull_requests=[509]),
            "frozen",
        ),
        (lambda d: d["entries"][0].update(summary=" "), "blank"),
        (lambda d: d.update(unknown=True), "Additional properties"),
    ]
    for mutate, message in mutations:
        data = document()
        mutate(data)
        with pytest.raises(ValueError, match=message):
            render_changelog.validate(data)
    data = document()
    data["entries"][1].pop("stack_id")
    with pytest.raises(ValueError, match="grouped PRs"):
        render_changelog.validate(data)


def test_markdown_rejects_html_and_unsafe_links_preserves_code() -> None:
    for prose in (
        "<script>forbidden</script>",
        "[bad](javascript:alert%281%29)",
        "[bad](data:text/html,hello)",
        "[bad](//evil.example/x)",
        "[bad](../../escape.md)",
        "[bad][x]\n\n[x]: javascript:alert(1)",
        '[bad](https://example.com){onclick="alert(1)"}',
        "{#unexpected}\n\nA paragraph.",
    ):
        data = document()
        data["entries"][0]["summary"] = prose
        with pytest.raises(ValueError, match=r"raw HTML|unsafe|repository-relative|attributes"):
            render_changelog.validate(data)
    data = document()
    data["entries"][0]["summary"] = "`<b>` and `[policy](README.md)` are code."
    render_changelog.validate(data)
    assert "<code>[policy](README.md)</code>" in render_changelog.render_markdown(
        data, destination="site"
    )


def test_kpress_preserves_math_and_unique_stable_ids() -> None:
    data = document()
    data["entries"][1]["title"] = "Foundations"
    site = render_changelog.render_markdown(data, destination="site")
    tree = parse_markdown(site, title="Changelog", math="auto")
    ids = re.findall(r'\bid="([^"]+)"', tree.html)
    assert len(ids) == len(set(ids))
    assert ids.count("changelog") == 1
    assert ids.count("changelog-entry-foundations") == 1
    assert "<math" in tree.html
    assert "<ul>" in tree.html
    assert '<h4 id="changelog-entry-foundations">Foundations</h4>' in tree.html


def test_math_generated_markup_and_urls_are_rejected_through_full_news(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payloads = [
        r"$\text{</mtext></math><script>forbidden</script>}$",
        r"$\href{javascript:alert(1)}{X}$",
        r"$\href{http://example.com/proof}{X}$",
        r"$\href{mailto:person@example.com}{X}$",
        r'$\text{<img src="https://example.com/a.png" onerror="forbidden">}$',
    ]
    for field in ("title", "summary", "details"):
        for payload in payloads:
            data = document()
            data["entries"][0][field] = payload
            monkeypatch.setattr(render_changelog, "load", lambda data=data: data)
            with pytest.raises(ValueError, match=r"unsafe|sanitized|raw HTML"):
                render_overview.news_page()
            with pytest.raises(ValueError, match=r"unsafe|sanitized|raw HTML"):
                render_changelog.validate(data)
            with pytest.raises(ValueError, match=r"unsafe|sanitized|raw HTML"):
                render_changelog.render_markdown(data)


def test_normal_math_and_safe_math_links_survive_full_news(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data = document()
    data["entries"][0]["summary"] = (
        r"A **bound** is $\left(\frac{x}{2}\right)^2$; "
        r"$\href{https://example.com/proof(1)}{X}$ is its reference."
    )
    data["entries"][0]["details"] = (
        "- Matrix:\n\n" + r"$$\begin{pmatrix}1&2\\3&4\end{pmatrix}$$"
    )
    monkeypatch.setattr(render_changelog, "load", lambda: data)
    news = render_overview.news_page().html
    assert "<math" in news
    assert "<mfrac>" in news
    assert "<mtable" in news
    assert "<strong>bound</strong>" in news
    assert 'href="https://example.com/proof%281%29"' in news
    assert data["entries"][0]["summary"] in render_changelog.render_markdown(data)


def test_reference_labels_are_local_to_each_summary_and_details() -> None:
    data = document()
    data["entries"][0]["summary"] = "First [source].\n\n[source]: https://example.com/first"
    data["entries"][0]["details"] = (
        "Details [source][].\n\n[source]: https://example.com/details"
    )
    data["entries"][1]["summary"] = (
        "Second [**source**][source].\n\n[source]: https://example.com/second"
    )
    data["entries"][1]["details"] = (
        r"`[source]` and $\text{[source]}$ remain code and math."
        "\n\n[source]: https://example.com/unused"
    )
    github = render_changelog.render_markdown(data)
    assert "`[source]`" in github
    assert r"$\text{[source]}$" in github
    for destination in ("github", "site"):
        tree = parse_markdown(
            render_changelog.render_markdown(data, destination=destination), title="Changelog"
        )
        links = {
            (html.unescape(href), label)
            for href, label in re.findall(
                r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', tree.html, re.DOTALL
            )
        }
        assert ("https://example.com/first", "source") in links
        assert ("https://example.com/details", "source") in links
        assert ("https://example.com/second", "<strong>source</strong>") in links


def test_contributor_links_resolve_for_each_reader_surface() -> None:
    target = "packing/contributors/people/hiroaki-hosono.md?plain=1#accounts"
    for prose in (
        f"[Hiroaki Hosono]({target})\N{RIGHT SINGLE QUOTATION MARK}s certificate was retained.",
        (
            f"[Hiroaki Hosono][person]\N{RIGHT SINGLE QUOTATION MARK}s certificate was kept."
            f"\n\n[person]: {target}"
        ),
    ):
        data = document()
        data["entries"][0]["summary"] = prose
        data["entries"][0]["details"] = (
            "The [contributor records](packing/contributors/README.md) retain the evidence."
        )
        render_changelog.validate(data)
        github = render_changelog.render_markdown(data)
        assert f"[Hiroaki Hosono]({target})\N{RIGHT SINGLE QUOTATION MARK}s" in github
        site = render_changelog.render_markdown(data, destination="site")
        assert (
            '<a href="profiles/hiroaki-hosono.html?plain=1#accounts">'
            "Hiroaki Hosono</a>\N{RIGHT SINGLE QUOTATION MARK}s"
        ) in site
        assert repo_url("packing/contributors/README.md") in site


def test_contributor_links_retain_the_repository_target_in_details() -> None:
    data = document()
    target = "packing/contributors/people/evan-daniel.md"
    data["entries"][0]["details"] = f"- Retained [Evan Daniel][].\n\n[Evan Daniel]: {target}"
    github = render_changelog.render_markdown(data)
    site = render_changelog.render_markdown(data, destination="site")
    assert f"[Evan Daniel]({target})" in github
    assert '<a href="profiles/evan-daniel.html">Evan Daniel</a>' in site


def test_contributor_links_reject_missing_and_unsafe_targets() -> None:
    for target, message in (
        ("packing/contributors/people/missing-person-not-a-profile.md", "missing repository"),
        ("packing/contributors/people/../README.md", "repository-relative"),
        ("packing/contributors/people/%252e%252e/README.md", "repository-relative"),
        ("packing/contributors/people/evan-daniel.md?x=%3Cscript%3E", "unsafe"),
    ):
        for prose in (f"[Person]({target})", f"[Person][person]\n\n[person]: {target}"):
            data = document()
            data["entries"][0]["summary"] = prose
            for destination in ("github", "site"):
                with pytest.raises(ValueError, match=message):
                    render_changelog.render_markdown(data, destination=destination)


def test_structured_links_reject_decoded_markup_and_unsafe_authorities() -> None:
    attacks = [
        "https://example.com/)<script>forbidden</script>",
        "https://example.com/%3Cscript%3Ealert%281%29%3C/script%3E",
        "https://example.com/&lt;script&gt;alert(1)&lt;/script&gt;",
        "https://example.com/%26lt%3Bscript%26gt%3B",
        "https://example.com/%253Cscript%253E",
        "https://example.com/%0A<script>forbidden</script>",
        "https://example.com\\evil/path",
        "https://user@example.com/path",
        "https://@example.com/path",
        "https://visible.example%23@actual.example/path",
        "https://visible.example%2F@actual.example/path",
        "https://example.com:invalid/path",
        "https://exam ple.com/path",
        "javascript:alert(1)",
    ]
    for attack in attacks:
        for field in ("reference", "publication", "dated_publication", "artifact"):
            data = document()
            entry = data["entries"][0]
            if field == "reference":
                entry["references"] = [{"label": "Evidence", "target": attack}]
            elif field == "artifact":
                entry["artifacts"] = [
                    {"kind": "result", "label": "Current result", "target": attack}
                ]
                entry["publication"] = {"evidence": "https://example.com/audit"}
            else:
                entry["publication"] = {"evidence": attack}
                if field == "dated_publication":
                    entry["publication"]["date"] = "2026-10-12"
            with pytest.raises(ValueError, match=r"unsafe|does not match|registered public"):
                render_changelog.render_markdown(data, destination="site")


def test_structured_link_markdown_delimiters_cannot_create_html_links() -> None:
    injection = ")[Injected](https://evil.example/x)"
    target = "https://example.com/audit" + injection
    artifact_target = "https://squaremath.org/result/t-151.html#" + injection
    for dated in (False, True):
        data = document()
        entry = data["entries"][0]
        entry["references"] = [{"label": "Evidence", "target": target}]
        entry["publication"] = {"evidence": target}
        entry["artifacts"] = [
            {"kind": "result", "label": "Current result", "target": artifact_target}
        ]
        if dated:
            entry["publication"]["date"] = "2026-10-12"
        tree = parse_markdown(
            render_changelog.render_markdown(data, destination="site"), title="Changelog"
        )
        links = re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', tree.html, re.DOTALL)
        assert not any(label == "Injected" for _href, label in links)
        assert "<script" not in tree.html
        destinations = [html.unescape(href) for href, _label in links]
        assert quote(target, safe=":/?#@!$&*+,;=%-._~") in destinations
        assert quote(artifact_target, safe=":/?#@!$&*+,;=%-._~") in destinations
        assert "https://github.com/jlevy/squares/pull/553" in destinations


def test_real_structured_links_preserve_exact_canonical_destinations() -> None:
    data = render_changelog.load()
    tree = parse_markdown(
        render_changelog.render_markdown(data, destination="site"), title="Changelog"
    )
    destinations = {
        html.unescape(href) for href in re.findall(r'<a\b[^>]*href="([^"]+)"', tree.html)
    }
    for entry in data["entries"]:
        for number in entry["pull_requests"]:
            assert f"{data['repository']}/pull/{number}" in destinations
        for artifact in entry.get("artifacts", []):
            assert artifact["target"] in destinations
        for reference in entry.get("references", []):
            parts = urlsplit(reference["target"])
            fragment = (f"?{parts.query}" if parts.query else "") + (
                f"#{parts.fragment}" if parts.fragment else ""
            )
            target = reference["target"] if parts.scheme else repo_url(parts.path, fragment)
            assert target in destinations
        if "publication" in entry:
            assert entry["publication"]["evidence"] in destinations


def test_previous_local_main_is_independent_of_editable_frozen_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    previous = document()
    current = copy.deepcopy(previous)
    current.pop("frozen_entries")
    current["entries"].pop()
    current["coverage"]["omissions"] = [{"pull_request": 549, "reason": "Administrative"}]
    render_changelog.validate(current)
    calls: list[list[str]] = []

    def git(args: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(args)
        stdout = {
            "rev-parse": "a" * 40,
            "ls-tree": "100644 blob metadata site-changelog.yaml",
            "show": (
                render_changelog.SCHEMA.read_text()
                if args[-1].endswith("site-changelog.schema.yaml")
                else yaml.safe_dump(previous, sort_keys=False)
            ),
        }[args[1]]
        return subprocess.CompletedProcess(args, 0, stdout=stdout)

    monkeypatch.setattr(render_changelog.subprocess, "run", git)
    with pytest.raises(ValueError, match="frozen entry later-delivery"):
        render_changelog.validate_previous_ref(current, "origin/main")
    assert [call[1] for call in calls] == ["rev-parse", "ls-tree", "show", "show"]


def test_candidate_main_delivery_refusal_does_not_create_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rows = [
        {
            "number": 600,
            "title": "Pending main",
            "mergedAt": "2026-10-15T00:01:00Z",
            "baseRefName": "main",
            "mergeCommit": {"oid": "b" * 40},
            "state": "MERGED",
            "significance": {
                "score": 2,
                "rationale": "Routine engineering and reliability work.",
            },
        }
    ]
    metadata = tmp_path / "metadata.json"
    metadata.write_text(json.dumps(rows), encoding="utf-8")
    monkeypatch.setattr(
        import_changelog.subprocess,
        "run",
        lambda args, **_kwargs: subprocess.CompletedProcess(args, 1, stdout="", stderr=""),
    )
    output = tmp_path / "candidate.yaml"
    assert (
        import_changelog.main(
            [
                "--metadata",
                str(metadata),
                "--baseline",
                str(tmp_path / "absent.yaml"),
                "--output",
                str(output),
            ]
        )
        == 1
    )
    assert not output.exists()


def test_coverage_omissions_and_frozen_baseline() -> None:
    data = document()
    old = copy.deepcopy(data)
    data["entries"].pop()
    with pytest.raises(ValueError, match="coverage"):
        render_changelog.validate(data)
    data["coverage"]["omissions"] = [{"pull_request": 549, "reason": "Administrative closeout"}]
    render_changelog.validate(data)
    data["entries"][1]["pull_requests"] = [509]
    with pytest.raises(ValueError, match="frozen"):
        render_changelog.validate_frozen(data, old)


def test_publication_artifacts_and_historical_releases() -> None:
    data = document()
    data["entries"][0].update(
        artifacts=[
            {
                "kind": "result",
                "label": "Current result",
                "target": "https://squaremath.org/result/t-151.html",
            }
        ],
        publication={"evidence": "https://github.com/jlevy/squares/actions/runs/123"},
        releases=[{"component": "site", "version": "v0.4.1"}],
    )
    render_changelog.validate(data)
    assert "First public" not in render_changelog.render_markdown(data)
    data["entries"][0]["releases"][0]["version"] = "v9.9.9"
    with pytest.raises(ValueError, match="retained history"):
        render_changelog.validate(data)
    data["entries"][0].pop("releases")
    data["entries"][0]["artifacts"][0]["target"] = "https://evil.example/result.html"
    with pytest.raises(ValueError, match="registered public"):
        render_changelog.validate(data)
    data["entries"][0]["artifacts"][0]["target"] = "https://squaremath.org/result/t-151.html"
    data["entries"][0].pop("publication")
    with pytest.raises(ValueError, match="publication evidence"):
        render_changelog.validate(data)


def test_freshness_check_and_soft_wrapping(tmp_path: Path) -> None:
    source, output = tmp_path / "history.yaml", tmp_path / "CHANGELOG.md"
    source.write_text(yaml.safe_dump(document(), sort_keys=False), encoding="utf-8")
    assert render_changelog.main(["--source", str(source), "--output", str(output)]) == 0
    assert (
        render_changelog.main(["--source", str(source), "--output", str(output), "--check"])
        == 0
    )
    current = output.read_text(encoding="utf-8")
    output.write_text(
        current.replace("Admitted **verified** bounds", "Admitted\n**verified** bounds"),
        encoding="utf-8",
    )
    assert (
        render_changelog.main(["--source", str(source), "--output", str(output), "--check"])
        == 0
    )
    output.write_text(current.replace("Admitted", "Claimed"), encoding="utf-8")
    assert (
        render_changelog.main(["--source", str(source), "--output", str(output), "--check"])
        == 1
    )


def test_candidate_import_requires_actual_merged_main_and_preserves_old_entries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    baseline = document()
    rows = [
        {
            "number": 600,
            "title": "New tooling",
            "body": "Needs editorial review",
            "mergedAt": "2026-10-15T00:01:00Z",
            "baseRefName": "main",
            "mergeCommit": {"oid": "b" * 40},
            "state": "MERGED",
            "significance": {
                "score": 2,
                "rationale": "Routine engineering and reliability work.",
            },
        }
    ]
    candidate = import_changelog.draft(rows, baseline)
    assert candidate["entries"][:-1] == baseline["entries"]
    assert candidate["entries"][-1]["date"] == "2026-10-15"
    assert "artifacts" not in candidate["entries"][-1]
    render_changelog.validate(candidate)
    for key, value in [("mergedAt", None), ("baseRefName", "feature"), ("state", "OPEN")]:
        bad = copy.deepcopy(rows)
        bad[0][key] = value
        with pytest.raises(ValueError, match="merged main metadata"):
            import_changelog.draft(bad, baseline)
    metadata = tmp_path / "metadata.json"
    metadata.write_text(json.dumps(rows), encoding="utf-8")
    output = tmp_path / "candidate.yaml"
    checked = []
    monkeypatch.setattr(
        import_changelog,
        "verify_main_delivery",
        lambda delivery, main_ref: checked.append((delivery["number"], main_ref)),
    )
    assert (
        import_changelog.main(
            [
                "--metadata",
                str(metadata),
                "--baseline",
                str(tmp_path / "absent.yaml"),
                "--output",
                str(output),
            ]
        )
        == 0
    )
    assert checked == [(600, "origin/main")]
    assert "editorial review" in output.read_text(encoding="utf-8").lower()


def test_entry_anchors_cannot_borrow_an_existing_about_heading(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data = document()
    data["entries"][0]["id"] = "the-squares-project"
    monkeypatch.setattr(render_changelog, "load", lambda: data)
    about = render_overview.about_page().html
    ids = re.findall(r'\bid="([^\"]+)"', about)
    assert ids.count("the-squares-project") == 1
    assert ids.count("changelog-entry-the-squares-project") == 1
    assert len(ids) == len(set(ids))
    assert 'id="changelog-entry-the-squares-project"' in render_changelog.render_markdown(data)
    with monkeypatch.context() as broken:
        broken.setattr(render_changelog, "entry_anchor", lambda identifier: identifier)
        old = render_overview.about_page().html
        assert re.findall(r'\bid="([^\"]+)"', old).count("the-squares-project") == 2


def test_related_launch_group_is_explicit_and_does_not_invent_a_stack() -> None:
    data = document()
    data["deliveries"].extend(
        {
            "number": number,
            "title": "Related contribution",
            "merged_at": day + "T12:00:00Z",
            "base_ref": "main",
            "merge_commit": "b" * 40,
        }
        for number, day in [(600, "2026-10-15"), (601, "2026-10-16")]
    )
    data["coverage"]["pull_requests"].extend([600, 601])
    entry = {
        "id": "related-launch",
        "significance": {"score": 3, "rationale": "A focused public launch."},
        "date": "2026-10-16",
        "title": "Related launch",
        "pull_requests": [600, 601],
        "grouping": "related",
        "summary": "One public contribution.",
    }
    data["entries"].append(entry)
    render_changelog.validate(data)
    entry.pop("grouping")
    with pytest.raises(ValueError, match="explicit related grouping"):
        render_changelog.validate(data)
    entry.update(grouping="related", stack_id=498)
    with pytest.raises(ValueError, match="no stack_id"):
        render_changelog.validate(data)


def test_stacked_delivery_retains_real_api_base_and_requires_matching_main_receipt() -> None:
    data = document()
    delivery = data["deliveries"][1]
    delivery["base_ref"] = "stack/predecessor"
    with pytest.raises(ValueError, match="delivery_to_main"):
        render_changelog.validate(data)
    commit = delivery["merge_commit"]
    delivery["delivery_to_main"] = {
        "commit": commit,
        "evidence": data["repository"] + "/commit/" + commit,
    }
    render_changelog.validate(data)
    delivery["delivery_to_main"]["commit"] = "b" * 40
    with pytest.raises(ValueError, match="inconsistent delivery_to_main"):
        render_changelog.validate(data)


def test_stacked_import_proves_first_parent_main_delivery_before_preserving_api_base(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    row = {
        "number": 600,
        "title": "Stack delivery",
        "state": "MERGED",
        "significance": {"score": 2, "rationale": "Routine engineering and reliability work."},
        "mergedAt": "2026-10-15T00:01:00Z",
        "baseRefName": "stack/predecessor",
        "mergeCommit": {"oid": "b" * 40},
    }
    with pytest.raises(ValueError, match="merged main metadata"):
        import_changelog.draft([row], document())
    calls = []

    def git(args, **_kwargs):
        calls.append(args)
        stdout = "b" * 40 + "\n" if args[1] == "rev-list" else ""
        return subprocess.CompletedProcess(args, 0, stdout=stdout, stderr="")

    monkeypatch.setattr(import_changelog.subprocess, "run", git)
    parsed = {
        "number": row["number"],
        "base_ref": row["baseRefName"],
        "merge_commit": row["mergeCommit"]["oid"],
    }
    row["delivery_to_main"] = import_changelog.verify_main_delivery(parsed)
    candidate = import_changelog.draft([row], document())
    assert candidate["deliveries"][-1]["base_ref"] == "stack/predecessor"
    assert candidate["deliveries"][-1]["delivery_to_main"]["commit"] == "b" * 40
    assert [call[1] for call in calls] == ["merge-base", "rev-list"]
    monkeypatch.setattr(
        import_changelog.subprocess,
        "run",
        lambda args, **_kwargs: subprocess.CompletedProcess(
            args, 0, stdout="a" * 40 + "\n", stderr=""
        ),
    )
    with pytest.raises(ValueError, match="first-parent delivery"):
        import_changelog.verify_main_delivery(parsed)


@pytest.mark.parametrize(
    "rating",
    [
        None,
        {"score": 0, "rationale": "Too low."},
        {"score": 6, "rationale": "Too high."},
        {"score": True, "rationale": "Boolean."},
        {"score": 2.5, "rationale": "Fractional."},
        {"score": 3, "rationale": " "},
        {"score": 3, "rationale": "A **formatted** judgment."},
        {"score": 3, "rationale": "<script>bad</script>"},
    ],
)
def test_news_requires_an_explicit_plain_importance_judgment(rating: dict | None) -> None:
    data = document()
    if rating is None:
        data["entries"][0].pop("significance")
    else:
        data["entries"][0]["significance"] = rating
    with pytest.raises(ValueError, match=r"significance|entries/0"):
        render_changelog.validate(data)


def test_imported_result_citations_do_not_assign_importance() -> None:
    row = {
        "number": 700,
        "title": "Policy mentioning T-060",
        "body": "See T-060.",
        "state": "MERGED",
        "mergedAt": "2026-10-15T00:01:00Z",
        "baseRefName": "main",
        "mergeCommit": {"oid": "b" * 40},
    }
    with pytest.raises(ValueError, match="editorial significance"):
        import_changelog.draft([row], document())
    row["significance"] = {"score": 2, "rationale": "A routine policy clarification."}
    candidate = import_changelog.draft([row], document())
    assert candidate["entries"][-1]["significance"] == row["significance"]


def test_pr_label_import_keeps_editorial_rationale_and_project_topic(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    row = {
        "number": 700,
        "title": "Project capability mentioning T-060",
        "body": "See T-060 for background.",
        "state": "MERGED",
        "mergedAt": "2026-10-15T00:01:00Z",
        "baseRefName": "main",
        "mergeCommit": {"oid": "b" * 40},
        "labels": [{"name": "S3"}, {"name": "project"}],
    }
    calls = []

    def github(args, **_kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, stdout=json.dumps(row))

    monkeypatch.setattr(import_changelog.subprocess, "run", github)
    monkeypatch.setattr(import_changelog, "verify_main_delivery", lambda *_args: None)
    output = tmp_path / "candidate.yaml"
    args = [
        "--pr",
        "700",
        "--baseline",
        str(tmp_path / "absent.yaml"),
        "--output",
        str(output),
    ]
    assert import_changelog.main(args) == 1
    assert not output.exists()
    rationale = "A new focused public project capability."
    assert (
        import_changelog.main(
            [*args, "--significance", "4", "--significance-rationale", rationale]
        )
        == 1
    )
    assert not output.exists()
    assert import_changelog.main([*args, "--significance-rationale", rationale]) == 0
    assert "labels" in calls[-1][-1].split(",")
    data = render_changelog.load(output)
    entry = data["entries"][-1]
    assert entry["significance"] == {"score": 3, "rationale": rationale}
    assert entry["topics"] == ["project"]
    assert 'data-news-topic="project">Project</span>' in render_changelog.render_news(data)
    row["labels"] = ["project", "S2"]
    row["significance"] = {"rationale": rationale}
    data = import_changelog.draft([row])
    assert data["entries"][0]["significance"]["score"] == 2
    assert 'id="changelog-entry-pr-700"' in render_changelog.render_markdown(data)
    assert 'data-news-entry="pr-700"' not in render_changelog.render_news(data)


def test_pr_significance_labels_reject_ambiguity_and_metadata_score_conflicts() -> None:
    row = {
        "number": 700,
        "title": "New project work",
        "state": "MERGED",
        "mergedAt": "2026-10-15T00:01:00Z",
        "baseRefName": "main",
        "mergeCommit": {"oid": "b" * 40},
        "significance": {"score": 3, "rationale": "A focused public improvement."},
    }
    for labels in (["S3", "S4"], [{"name": "S3"}, {"name": "S4"}], ["S3", "S3"]):
        with pytest.raises(ValueError, match="exactly one"):
            import_changelog.draft([{**row, "labels": labels}])
    with pytest.raises(ValueError, match="conflict"):
        import_changelog.draft([{**row, "labels": ["S4"]}])
    for score in (True, 0, 6, "3"):
        with pytest.raises(ValueError, match="score"):
            import_changelog.draft(
                [{**row, "labels": ["S3"], "significance": {"score": score}}]
            )
    retained = import_changelog.draft([row])
    assert retained["entries"][0]["significance"] == row["significance"]
    for score in range(1, 6):
        labeled = {
            **row,
            "labels": [f"S{score}"],
            "significance": {"rationale": row["significance"]["rationale"]},
        }
        entry = import_changelog.draft([labeled])["entries"][0]
        assert entry["significance"]["score"] == score


def test_retained_pr_reimport_preserves_entries_and_omissions_without_new_ratings() -> None:
    for omitted in (False, True):
        baseline = document()
        if omitted:
            baseline["entries"].pop()
            baseline["coverage"]["omissions"] = [
                {"pull_request": 549, "reason": "Administrative closeout"}
            ]
        delivery = baseline["deliveries"][-1]
        row = {
            "number": delivery["number"],
            "title": delivery["title"],
            "state": "MERGED",
            "mergedAt": delivery["merged_at"],
            "baseRefName": delivery["base_ref"],
            "mergeCommit": {"oid": delivery["merge_commit"]},
        }
        for labels in ([], ["S4", "project"]):
            candidate = import_changelog.draft([{**row, "labels": labels}], baseline)
            for field in ("entries", "deliveries", "coverage"):
                assert candidate[field] == baseline[field]
        with pytest.raises(ValueError, match="exactly one"):
            import_changelog.draft([{**row, "labels": ["S3", "S4"]}], baseline)


def test_score_like_labels_fail_for_new_and_retained_prs() -> None:
    row = {
        "number": 700,
        "title": "A focused public improvement",
        "state": "MERGED",
        "mergedAt": "2026-10-15T00:01:00Z",
        "baseRefName": "main",
        "mergeCommit": {"oid": "b" * 40},
        "significance": {"score": 3, "rationale": "A focused public improvement."},
    }
    retained = import_changelog.draft([row])
    for name in ("S0", "S6", "S10", "S03", "s3", " S3 ", "S 3", "S+3", "S-3", "S3.0"):
        for labels in (
            [name],
            ["S3", name],
            [{"name": name}],
            [{"name": "S3"}, {"name": name}],
        ):
            for baseline in (None, retained):
                with pytest.raises(ValueError, match="invalid significance label"):
                    import_changelog.draft([{**row, "labels": labels}], baseline)
    candidate = import_changelog.draft([{**row, "labels": ["security", "project"]}])
    assert candidate["entries"][0]["significance"] == row["significance"]
    assert candidate["entries"][0]["topics"] == ["project"]


def test_news_exclusion_keeps_history_and_fills_the_preview_from_eligible_entries() -> None:
    data = document()
    previous = copy.deepcopy(data)
    excluded = data["entries"][-1]
    excluded["news_exclusion"] = "Routine typography maintenance."
    excluded["categories"] = ["documentation"]
    render_changelog.validate(data)
    render_changelog.validate_frozen(data, previous)
    assert data["coverage"] == previous["coverage"]
    assert data["deliveries"] == previous["deliveries"]
    github = render_changelog.render_markdown(data)
    anchor = render_changelog.entry_anchor(excluded["id"])
    assert f'id="{anchor}"' in github
    assert f"{data['repository']}/pull/549" in github
    news = render_changelog.render_news(data)
    assert 'data-news-entry="later-delivery"' not in news
    assert 'data-news-entry="foundations"' in news
    assert 'data-news-entry="admission"' in news
    archive = f"{data['repository']}/blob/main/CHANGELOG.md#{anchor}"
    assert f'id="{anchor}" href="{archive}" data-news-target' in news
    day = "changelog-date-2026-10-14"
    assert f'id="{day}" href="{data["repository"]}/blob/main/CHANGELOG.md#{day}"' in news
    assert '<p class="site-action-row"><a class="site-action"' in news
    assert f'href="{data["repository"]}/blob/main/CHANGELOG.md"' in news
    assert 'aria-label="Full changelog on GitHub">Full changelog' in news
    assert 'data-arrow="external"' in news
    about = render_changelog.legacy_news_anchors(data)
    assert f'id="{anchor}" href="{archive}" data-news-target' in about
    preview = render_changelog.render_news(data, limit=1)
    assert re.findall(r'data-news-entry="([^"]+)"', preview) == ["foundations"]
    assert anchor not in preview


@pytest.mark.parametrize("reason", ["", " \t\n", False, {"reason": "maintenance"}])
def test_news_exclusion_requires_a_nonblank_reason(reason: object) -> None:
    data = document()
    data["entries"][0]["news_exclusion"] = reason
    with pytest.raises(ValueError, match="news_exclusion"):
        render_changelog.validate(data)


def test_documentation_is_bookkeeping_but_not_a_public_news_topic() -> None:
    data = document()
    data["entries"][0]["categories"] = ["documentation"]
    data["entries"][0]["topics"] = ["upper-bound", "verification"]
    render_changelog.validate(data)
    assert 'data-news-entry="admission"' in render_changelog.render_news(data)
    for topic in ("documentation", "correction", "audit"):
        data["entries"][0]["topics"] = [topic]
        with pytest.raises(ValueError, match="topics"):
            render_changelog.validate(data)


def test_news_levels_are_described_by_the_rubric_that_scores_news() -> None:
    """A News meter and the archive's S buttons say what a level means in the label
    rubric of `result-import.md`, its `Short` column, never in the results ladder of
    `epistemics.md`, and never with a post's own rationale (`think-yznf`)."""
    from devtools.overview_sections import rung_meanings  # noqa: PLC0415

    meanings = render_changelog.news_significance_meanings()
    assert sorted(meanings) == [1, 2, 3, 4, 5]
    rubric = render_changelog.NEWS_RUBRIC.read_text(encoding="utf-8")
    section = rubric.split(render_changelog.NEWS_RUBRIC_SECTION, 1)[1]
    assert "| Label | Delivered contribution | Short | Examples |" in section
    for level, short in meanings.items():
        row = next(line for line in section.splitlines() if line.startswith(f"| `S{level}` |"))
        assert row.split(" | ")[2] == short
        assert short != rung_meanings()[f"S{level}"]
        assert len(f"Significance S{level}: {short}.") <= 120
    filters = render_changelog.news_filters()
    for score in (3, 4, 5):
        title = html.escape(render_changelog.news_significance_tooltip(score), quote=True)
        assert f'data-news-score="{score}" title="{title}"' in filters
    rating = render_changelog.news_rating({"score": 4, "rationale": "A private reason."})
    assert html.escape(render_changelog.news_significance_tooltip(4), quote=True) in rating
    assert "A private reason." not in rating


def test_prior_domain_artifacts_remain_valid_for_retained_history() -> None:
    current = render_changelog.load()
    previous = copy.deepcopy(current)
    for entry in previous["entries"]:
        for artifact in entry.get("artifacts", []):
            artifact["target"] = artifact["target"].replace(
                "https://squaremath.org/", "https://jlevy.github.io/squares/"
            )
    render_changelog.validate(previous)
    render_changelog.validate_frozen(current, previous)
    artifact = next(
        entry["artifacts"][0] for entry in previous["entries"] if entry.get("artifacts")
    )
    artifact["target"] = "https://unrelated.example/tutorial.html"
    with pytest.raises(ValueError, match="not a registered public destination"):
        render_changelog.validate(previous)


def _result(identifier: str, score: int) -> dict:
    return {"id": identifier, "significance": {"score": score, "by": "lane-x"}}


def _news(identifier: str, score: int, *result_ids: str) -> dict:
    return {
        "id": identifier,
        "date": "2026-10-20",
        "significance": {"score": score, "rationale": "An announcement."},
        "result_ids": list(result_ids),
    }


@pytest.fixture
def no_exemptions(monkeypatch: pytest.MonkeyPatch) -> None:
    """Synthetic registers hold none of the real exempt results."""
    monkeypatch.setattr(render_changelog, "ANNOUNCEMENT_EXEMPT", {})


def _merged_at_42(identifier: str, score: int) -> render_changelog.Landing:
    del identifier, score
    return {"pull_request": 42, "commit": "b" * 40, "subject": "Merge pull request #42 from x"}


#: The fifteen S4 and S5 results that landed before the News archive (6279bd0e6, 13
#: October 2026), at the scores they are exempt at. The exemption may only shrink.
FROZEN_EXEMPTIONS = {
    "T-010": 4,
    "T-017": 4,
    "T-018": 5,
    "T-019": 4,
    "T-020": 4,
    "T-022": 5,
    "T-024": 5,
    "T-025": 5,
    "T-026": 5,
    "T-037": 5,
    "T-047": 4,
    "T-051": 4,
    "T-052": 4,
    "T-064": 4,
    "T-081": 4,
}


@pytest.mark.usefixtures("no_exemptions")
def test_an_s4_or_s5_result_on_main_without_its_news_item_fails() -> None:
    results = [_result("T-901", 5), _result("T-902", 3)]
    failures, owed, unsettled = render_changelog.check_announcements(
        {"entries": []}, results, results, locate=_merged_at_42
    )
    assert (owed, unsettled) == ([], [])
    [failure] = failures
    # The message names the result, its score, the merged PR the entry must name, the
    # command that drafts it and who scored it: everything a passing author needs.
    assert failure.startswith("T-901 (S5) is on main with no News item at S5, and this")
    assert "add the item in this PR, or land the stage 7 follow-up" in failure
    assert "naming PR #42, which registered or raised it (merge bbbbbbbbb)" in failure
    assert "devtools.import_changelog --pr 42 " in failure
    assert "Announce a Significant Result" in failure
    assert "scored by lane-x" in failure
    # Without a base, nothing is in grace.
    assert render_changelog.check_announcements({"entries": []}, results).failures == [
        failure.replace(
            "PR #42, which registered or raised it (merge bbbbbbbbb)",
            "the "
            "merged PR that registered or raised it, which this checkout's history does not "
            "reach",
        ).replace("--pr 42 ", "--pr NNN ")
    ]


@pytest.mark.usefixtures("no_exemptions")
def test_an_owed_item_fails_only_a_change_to_the_register_or_news() -> None:
    results = [_result("T-901", 5)]
    empty: dict = {"entries": []}
    # An unrelated change, on a branch or merged to main, warns and passes.
    failures, owed, [warning] = render_changelog.check_announcements(
        empty, results, results, locate=_merged_at_42, records_changed=False
    )
    assert (failures, owed) == ([], [])
    assert warning.startswith("T-901 (S5) is on main with no News item at S5. This change")
    assert "naming PR #42" in warning
    # A change to the register or the News record is the one that settles it.
    assert render_changelog.check_announcements(
        empty, results, results, locate=_merged_at_42, records_changed=True
    ).failures
    # A register change that carries the owed item passes.
    carried = {"entries": [_news("item", 5, "T-901")]}
    assert render_changelog.check_announcements(
        carried, [*results, _result("T-902", 2)], results, records_changed=True
    ) == ([], [], [])


@pytest.mark.usefixtures("no_exemptions")
def test_a_records_merge_on_main_warns_where_the_same_pr_fails() -> None:
    # A records PR that went green before an S4/S5 merge, then merged after it: its PR
    # CI enforced the rule, and main's run of the merge can no longer act on a failure.
    results = [_result("T-901", 5)]
    empty: dict = {"entries": []}
    failures, owed, [warning] = render_changelog.check_announcements(
        empty, results, results, locate=_merged_at_42, records_changed=True, on_main=True
    )
    assert (failures, owed) == ([], [])
    assert warning.startswith("T-901 (S5) is on main with no News item at S5. On main")
    assert "naming PR #42" in warning
    # The same change in pull-request mode fails.
    [failure] = render_changelog.check_announcements(
        empty, results, results, locate=_merged_at_42, records_changed=True
    ).failures
    assert "settles the debt" in failure
    # On main, a result the merge itself registered is still owed after it.
    assert render_changelog.check_announcements(
        empty, results, [], locate=_merged_at_42, on_main=True
    ).owed


@pytest.mark.usefixtures("no_exemptions")
def test_a_news_item_at_the_result_score_satisfies_the_gate() -> None:
    results = [_result("T-901", 5), _result("T-903", 4)]
    document = {"entries": [_news("both", 5, "T-901", "T-903")]}
    assert render_changelog.check_announcements(document, results, results) == ([], [], [])
    # The highest showing score counts, in whatever order the entries come.
    for order in (
        [_news("a", 5, "T-901"), _news("b", 3, "T-901")],
        [_news("b", 3, "T-901"), _news("a", 5, "T-901")],
    ):
        assert render_changelog.news_announced_scores({"entries": order}) == {"T-901": 5}
    # Only an item News shows counts, at the result's own score or above.
    low = {"entries": [_news("low", 4, "T-901", "T-903")]}
    hidden = {"entries": [{**_news("hidden", 5, "T-901", "T-903"), "news_exclusion": "x"}]}
    # An S2 entry is history News never shows, which is where T-064 and T-081 sat.
    unshown = {"entries": [_news("attribution", 2, "T-901", "T-903")]}
    assert [r["id"] for r in render_changelog.owed_announcements(low, results)] == ["T-901"]
    assert len(render_changelog.owed_announcements(hidden, results)) == 2
    assert len(render_changelog.owed_announcements(unshown, results)) == 2


@pytest.mark.usefixtures("no_exemptions")
def test_a_raise_to_s4_is_owed_after_its_merge_and_fails_once_on_main() -> None:
    before = [_result("T-904", 3)]
    raised = [_result("T-904", 4)]
    empty: dict = {"entries": []}
    assert render_changelog.check_announcements(empty, before, before) == ([], [], [])
    # The raising branch: its entry can name only merged PRs, so the item is owed.
    failures, [note], unsettled = render_changelog.check_announcements(
        empty, raised, before, locate=_merged_at_42
    )
    assert (failures, unsettled) == ([], [])
    assert note.startswith("T-904 (S4) is registered or raised on this branch")
    # The next change to the register or News, with the raise on main, fails.
    failures, owed, unsettled = render_changelog.check_announcements(
        empty, raised, raised, locate=_merged_at_42
    )
    assert (owed, unsettled) == ([], [])
    assert [f.split(" is on main")[0] for f in failures] == ["T-904 (S4)"]
    # Exactly as a new registration: owed on its own branch, failed once on main.
    assert render_changelog.check_announcements(empty, raised, [], locate=_merged_at_42) == (
        [],
        [note],
        [],
    )
    # An S4 item does not announce a later raise to S5.
    s4_item = {"entries": [_news("item", 4, "T-904")]}
    to_five = [_result("T-904", 5)]
    assert (
        render_changelog.check_announcements(s4_item, to_five, to_five, locate=_merged_at_42)
        .failures[0]
        .startswith("T-904 (S5) is on main")
    )


def test_the_exemption_is_frozen_to_results_scored_and_landed_before_the_archive() -> None:
    exempt = render_changelog.ANNOUNCEMENT_EXEMPT
    assert exempt.items() <= FROZEN_EXEMPTIONS.items()
    results = {result["id"]: result for result in render_changelog.load_results()}
    for identifier, score in exempt.items():
        result = results[identifier]
        assert result["landed"] < "2026-10-13", identifier
        assert result["significance"]["scored"] < "2026-10-13", identifier
        assert result["significance"]["score"] == score, identifier
    assert (
        render_changelog.stale_exemptions(render_changelog.load(), list(results.values())) == []
    )


def test_stale_exemptions_fail_through_the_gate(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        render_changelog,
        "ANNOUNCEMENT_EXEMPT",
        {"T-905": 4, "T-906": 4, "T-907": 5, "T-908": 4, "T-909": 4},
    )
    register = [
        _result("T-905", 3),
        _result("T-907", 4),
        _result("T-908", 5),
        _result("T-909", 4),
    ]
    failures, owed, unsettled = render_changelog.check_announcements(
        {"entries": [_news("item", 4, "T-909")]},
        register,
        register,
        locate=_merged_at_42,
        records_changed=False,
    )
    remove = ": remove it from render_changelog.ANNOUNCEMENT_EXEMPT"
    assert failures == [
        f"T-905 is S3 now, below the announcement threshold{remove}",
        f"T-906 is not in the register{remove}",
        f"T-907 is S4 now, not the S5 it is exempt at{remove}",
        f"T-908 is S5 now, not the S4 it is exempt at{remove}",
        f"T-909 now has its News item{remove}",
    ]
    # Raised above its exempt score, a result is also owed like any other.
    assert owed == []
    assert [w.split(" is on main")[0] for w in unsettled] == ["T-908 (S5)"]


@pytest.mark.usefixtures("no_exemptions")
def test_the_cli_fails_a_missing_item_and_notes_an_owed_one(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        render_changelog, "announcement_base", lambda _ref: ("b" * 40, [_result("T-901", 5)])
    )
    monkeypatch.setattr(
        render_changelog, "load_results", lambda: [_result("T-901", 5), _result("T-902", 4)]
    )
    monkeypatch.setattr(render_changelog, "landing", lambda *_: None)
    monkeypatch.setattr(render_changelog, "edits_announcement_records", lambda _base: True)
    assert render_changelog.main(["--check", "--announcement-base", "origin/main"]) == 1
    out, err = capsys.readouterr()
    assert "announcement missing: T-901 (S5)" in err
    assert "announcement owed after merge: T-902 (S4)" in out
    # The same debt in a change that edits neither record is a warning, and passes.
    monkeypatch.setattr(render_changelog, "edits_announcement_records", lambda _base: False)
    assert render_changelog.main(["--check", "--announcement-base", "origin/main"]) == 0
    out, err = capsys.readouterr()
    assert "warning: announcement owed on main: T-901 (S5)" in out
    assert "announcement missing" not in err
    assert "1 owed after this merge, 1 owed on main and reported, 0 failing" in out
    # Main's own delivery (HEAD^1) only warns, even for a records merge.
    monkeypatch.setattr(render_changelog, "edits_announcement_records", lambda _base: True)
    base = render_changelog.MAIN_DELIVERY_BASE
    assert render_changelog.main(["--check", "--announcement-base", base]) == 0
    out, err = capsys.readouterr()
    assert "warning: announcement owed on main: T-901 (S5) is on main with no News item " in out
    assert "On main the gate reports and never fails" in out
    assert "announcement missing" not in err


def test_committed_changes_to_either_record_are_seen_against_the_fork(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # #738's review A: committed, as in CI, where the working tree is clean and only a
    # diff against the base sees the change; and each record on its own.
    def git(*arguments: str) -> str:
        return subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@example.org", *arguments],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    register = tmp_path / render_changelog.RESULTS_PATH
    news = tmp_path / "packing/site-changelog.yaml"
    register.parent.mkdir(parents=True)
    register.write_text("results: []\n", encoding="utf-8")
    news.write_text("entries: []\n", encoding="utf-8")
    (tmp_path / "notes.md").write_text("a\n", encoding="utf-8")
    git("init", "-q", "-b", "main")
    git("add", "-A")
    git("commit", "-q", "--no-gpg-sign", "-m", "root")
    monkeypatch.setattr(render_changelog, "REPO", tmp_path)
    for path, expected in ((register, True), (news, True), (tmp_path / "notes.md", False)):
        git("checkout", "-q", "-B", "feature", "main")
        path.write_text(path.read_text(encoding="utf-8") + "# edited\n", encoding="utf-8")
        git("commit", "-q", "--no-gpg-sign", "-am", f"edit {path.name}")
        base, _ = render_changelog.announcement_base("main")
        assert render_changelog.edits_announcement_records(base) is expected, path.name


def test_the_base_is_the_fork_point_and_record_changes_are_seen(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def git(*arguments: str) -> str:
        return subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@example.org", *arguments],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=True,
        ).stdout

    register = tmp_path / render_changelog.RESULTS_PATH

    def commit(identifiers: list[str], message: str) -> str:
        register.write_text(
            yaml.safe_dump({"results": [_result(i, 5) for i in identifiers]}), encoding="utf-8"
        )
        git("add", "-A")
        git("commit", "-q", "--no-gpg-sign", "-m", message)
        return git("rev-parse", "HEAD").strip()

    git("init", "-q", "-b", "main")
    register.parent.mkdir(parents=True)
    fork = commit(["T-901"], "register T-901")
    git("checkout", "-q", "-b", "feature")
    (tmp_path / "notes.md").write_text("unrelated\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-q", "--no-gpg-sign", "-m", "unrelated")
    git("checkout", "-q", "main")
    commit(["T-901", "T-902"], "main moves on: T-902")
    git("checkout", "-q", "feature")
    monkeypatch.setattr(render_changelog, "REPO", tmp_path)
    # A branch is measured from where it left main, not from where main is now.
    base, results = render_changelog.announcement_base("main")
    assert (base, [r["id"] for r in results]) == (fork, ["T-901"])
    assert not render_changelog.edits_announcement_records(base)
    register.write_text(register.read_text(encoding="utf-8") + "# edited\n", encoding="utf-8")
    assert render_changelog.edits_announcement_records(base)


def test_a_score_is_read_from_its_own_block_only() -> None:
    text = (
        "results:\n  - id: T-907\n    kind: x\n  - id: T-999\n    significance:\n"
        "      score: 5\n"
    )
    assert render_changelog.register_score(text, "T-907") == 0
    assert render_changelog.register_score(text, "T-999") == 5
    assert render_changelog.register_score(text, "T-123") == 0


def test_the_landing_change_is_the_oldest_first_parent_merge_at_the_score(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def register(score: int | None) -> str:
        body = "results:\n  - id: T-001\n    significance:\n      score: 2\n"
        if score is not None:
            body += f"  - id: T-907\n    kind: x\n    significance:\n      score: {score}\n"
        return body + "  - id: T-999\n    significance:\n      score: 1\n"

    # Newest first, as `git log` lists them: S5 since #11, after a dip to S3 at #10.
    history = {"c4": 5, "c3": 5, "c2": 3, "c1": 5, "c0": None}
    subjects = {
        commit: f"Merge pull request #{8 + int(commit[1])} from x" for commit in history
    }

    def git(*arguments: str) -> str:
        if arguments[0] == "log":
            return "".join(f"{commit}\0{subjects[commit]}\n" for commit in history)
        return register(history[arguments[1].split(":")[0]])

    monkeypatch.setattr(render_changelog, "_git", git)
    assert render_changelog.landing("T-907", 5, "origin/main") == {
        "pull_request": 11,
        "commit": "c3",
        "subject": subjects["c3"],
    }
    assert render_changelog.landing("T-907", 3, "origin/main") == {
        "pull_request": 9,
        "commit": "c1",
        "subject": subjects["c1"],
    }
