"""The published URL boundary: omissions, identity changes, crawl files and aliases."""

import json
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest

from devtools import (
    check_published_site,
    overview_data,
    render_overview,
    render_research_tables,
    site_documents,
    site_urls,
)


def row(path: str) -> site_urls.SiteURL:
    return site_urls.SiteURL(
        path=path,
        canonical=path.removesuffix("index.html"),
        kind="page",
        generator="fixture:render",
        producer="overview",
        first_published="2026-09-01",
        lastmod="2026-09-01",
        identity={},
    )


def failures(checks: list[tuple[bool, str]]) -> str:
    return "\n".join(message for passed, message in checks if not passed)


def test_partial_producer_omission_fails_without_building_other_producers(
    tmp_path: Path,
) -> None:
    rows = [
        row("index.html"),
        row("frontier.html"),
        replace(row("workbench/index.html"), producer="workbench"),
    ]
    (tmp_path / "index.html").write_text("fixture", encoding="utf-8")
    failed = failures(
        site_urls.check_site(tmp_path, rows, partial=True, producers=("overview",))
    )
    assert "frontier.html" in failed
    assert "workbench/index.html" not in failed
    assert "workbench/index.html" in failures(site_urls.check_site(tmp_path, rows))
    with pytest.raises(ValueError, match="producer"):
        site_urls.check_site(tmp_path, rows, partial=True)
    empty = tmp_path / "empty"
    empty.mkdir()
    failed = failures(site_urls.check_site(empty, rows, partial=True, producers=("overview",)))
    assert "index.html" in failed
    assert "frontier.html" in failed


def test_selected_producer_requires_its_patterned_data_namespace(tmp_path: Path) -> None:
    data = replace(
        site_urls.hashed_asset_rows("2026-09-01")[0],
        path="workbench/data/corpus.{hash}.json",
        producer="workbench",
        pattern=site_urls.WORKBENCH_DATA_PATTERN,
    )
    page = replace(row("workbench/index.html"), producer="workbench")
    rows = [page, data]
    (tmp_path / "workbench").mkdir()
    (tmp_path / page.path).write_text("fixture", encoding="utf-8")
    failed = failures(
        site_urls.check_site(tmp_path, rows, partial=True, producers=("workbench",))
    )
    assert "required workbench namespace missing" in failed
    (tmp_path / "workbench/data").mkdir()
    (tmp_path / "workbench/data/corpus.0123456789abcdef.json").write_text(
        "{}", encoding="utf-8"
    )
    assert not failures(
        site_urls.check_site(tmp_path, rows, partial=True, producers=("workbench",))
    )


def test_closed_world_and_constrained_asset_names(tmp_path: Path) -> None:
    rows = [row("index.html"), *site_urls.hashed_asset_rows("2026-09-01")]
    (tmp_path / "index.html").write_text("fixture", encoding="utf-8")
    folder = tmp_path / "assets/css"
    folder.mkdir(parents=True)
    (folder / "site.0123456789abcdef.css").write_text("", encoding="utf-8")
    assert not failures(site_urls.check_site(tmp_path, rows))
    (folder / "unregistered.html").write_text("", encoding="utf-8")
    assert "unregistered.html" in failures(site_urls.check_site(tmp_path, rows))
    (tmp_path / "escape").symlink_to(tmp_path.parent)
    assert "symlink" in failures(site_urls.check_site(tmp_path, rows))


def test_history_retains_withdrawals_and_rejects_forwarder_cycles() -> None:
    old = row("cases/11.html")
    assert "removed" in failures(site_urls.check_history([], [old]))
    withdrawn = replace(
        old,
        status="withdrawn",
        tombstone="Replaced by a corrected case.",
        target="cases/12.html",
    )
    assert not failures(site_urls.check_history([withdrawn, row("cases/12.html")], [old]))
    assert "unknown" in failures(site_urls.validate_registry([withdrawn]))
    first = replace(
        row("first.html"),
        kind="forwarder",
        status="forwarded",
        target="second.html",
        canonical="second.html",
    )
    second = replace(first, path="second.html", target="first.html", canonical="first.html")
    assert "cycle" in failures(site_urls.validate_registry([first, second]))
    replacements = [
        replace(first, status="withdrawn", tombstone="Consolidated."),
        replace(second, status="withdrawn", tombstone="Consolidated."),
    ]
    assert "cycle" in failures(site_urls.validate_registry(replacements))
    unknown = replace(row("index.html"), canonical="missing.html")
    assert "canonical destination" in failures(site_urls.validate_registry([unknown]))
    backwards = replace(row("index.html"), lastmod="2026-08-31")
    assert "dates" in failures(site_urls.validate_registry([backwards]))


def test_same_date_result_id_swap_requires_explicit_semantic_amendment() -> None:
    first = replace(
        row("result/t-001.html"),
        kind="result",
        identity=site_urls.result_identity(
            {"kind": "lower-bound", "scope": {"n_values": [17]}, "evidence": ["E-first"]}
        ),
    )
    second = replace(
        first,
        path="result/t-002.html",
        canonical="result/t-002.html",
        identity=site_urls.result_identity(
            {"kind": "lower-bound", "scope": {"n_values": [18]}, "evidence": ["E-second"]}
        ),
    )
    swapped = [
        replace(first, identity=second.identity),
        replace(second, identity=first.identity),
    ]
    assert "identity" in failures(site_urls.check_history(swapped, [first, second]))
    amended = replace(
        first,
        identity=second.identity,
        amendments=(
            {
                "date": "2026-09-02",
                "reason": "Correct the cited case and evidence.",
                "previous": first.identity,
            },
        ),
    )
    assert not failures(site_urls.check_history([amended, second], [first, second]))
    assert site_urls.result_identity(
        {"kind": "lower-bound", "headline": "New wording"}
    ) == site_urls.result_identity({"kind": "lower-bound", "headline": "Old wording"})


def test_sitemap_uses_canonical_paths_and_record_dates() -> None:
    rows = [
        row("index.html"),
        replace(row("result/t-001.html"), kind="result", lastmod="2026-10-02"),
        replace(
            row("moved.html"),
            kind="forwarder",
            status="forwarded",
            canonical="index.html",
            target="index.html",
        ),
        replace(row("papers/example.pdf"), kind="paper-file"),
    ]
    first = site_urls.render_sitemap(rows)
    assert first == site_urls.render_sitemap(rows)
    assert "<loc>https://jlevy.github.io/squares/</loc>" in first
    assert "2026-10-02" in first
    assert "moved.html" not in first
    assert "example.pdf" not in first


def test_crawl_writer_emits_safe_404_and_tombstones(tmp_path: Path) -> None:
    rows = [
        row("index.html"),
        replace(row("cases/11.html"), kind="record"),
        replace(row("result/t-001.html"), kind="result"),
        row("all-results.html"),
        replace(
            row("result/t-002.html"),
            kind="result",
            status="withdrawn",
            tombstone="Correction <retained>",
            target="result/t-001.html",
        ),
    ]
    site_urls.write_crawl_files(tmp_path, rows)
    text = (tmp_path / "404.html").read_text(encoding="utf-8")
    assert 'content="noindex' in text
    assert "/squares/assets/" in text
    assert 'data-site-root="/squares/"' in text
    assert "result/t-001.html" in text
    tombstone = (tmp_path / "result/t-002.html").read_text(encoding="utf-8")
    assert "Correction &lt;retained&gt;" in tombstone
    assert "result/t-001.html" in tombstone
    assert not site_urls.alias_target("cases/012.html", rows)
    assert site_urls.alias_target("cases/n-11.html", rows) == "cases/11.html"
    assert site_urls.alias_target("result/T-001.html", rows) == "result/t-001.html"
    assert not site_urls.alias_target("result/T-999.html", rows)
    assert not site_urls.alias_target("//elsewhere.example/result/T-001.html", rows)


def test_html_family_and_hard_budgets(tmp_path: Path) -> None:
    rows = [replace(row("cases/12.html"), kind="record")]
    (tmp_path / "cases").mkdir()
    (tmp_path / "cases/12.html").write_bytes(b"x" * 300_001)
    assert "300000" in failures(site_urls.check_site(tmp_path, rows))
    (tmp_path / "cases/12.html").write_bytes(b"x" * 2_000_001)
    assert "2000000" in failures(site_urls.check_site(tmp_path, rows))


def test_registry_round_trip_keeps_root_canonical_and_semantic_identity(tmp_path: Path) -> None:
    rows = [row("index.html"), *site_urls.hashed_asset_rows("2026-09-01")]
    path = tmp_path / "site-urls.yaml"
    path.write_text(site_urls.render_registry(rows), encoding="utf-8")
    assert site_urls.load_registry(path) == rows


def test_deployed_registry_walk_does_not_sample_cases_or_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rows = [replace(row(f"cases/{n}.html"), kind="record") for n in range(1, 14)]
    rows += [replace(row(f"result/t-{n:03}.html"), kind="result") for n in range(1, 5)]
    visited: list[str] = []

    def read(url: str, *, timeout: float) -> tuple[int, bytes]:
        assert timeout == 1
        visited.append(url)
        return (404, b"") if url.endswith("cases/7.html") else (200, b"fixture")

    monkeypatch.setattr(check_published_site, "head_checks", lambda *_args: [])
    checks = check_published_site.deployed_registry_checks(
        "https://example.org/squares/", read, timeout=1, rows=rows
    )
    assert "registered cases/7.html: HTTP 404" in failures(checks)
    assert len(visited) == len(rows) + 1  # The shared preview card.
    assert any(url.endswith("result/t-004.html") for url in visited)


def test_not_found_alias_script_keeps_unknown_addresses_and_fragments() -> None:
    script = Path(__file__).parent / "node/overview_urls/not-found.test.mjs"
    result = subprocess.run(
        ["node", "--test", str(script)], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    ("path", "measured"),
    [
        ("papers/n11-lower-bounds-explainer.html", 1_417_109),
        ("papers/n11-threshold-bound-review.html", 824_137),
    ],
)
def test_measured_budget_exception_preserves_the_hard_limit(
    tmp_path: Path, path: str, measured: int
) -> None:
    paper = replace(row(path), kind="paper-file", producer="paper:" + Path(path).stem)
    (tmp_path / "papers").mkdir()
    (tmp_path / path).write_bytes(b"x" * measured)
    assert not failures(site_urls.check_site(tmp_path, [paper]))
    budget = site_urls.page_budget(paper)
    (tmp_path / path).write_bytes(b"x" * (budget + 1))
    assert str(budget) in failures(site_urls.check_site(tmp_path, [paper]))
    (tmp_path / path).write_bytes(b"x" * 2_000_001)
    assert "2000000" in failures(site_urls.check_site(tmp_path, [paper]))


@pytest.mark.parametrize(
    ("scope", "covered"),
    [({"n_values": [4, 6]}, {4, 6}), ({"n_min": 4, "n_max": 6}, {4, 5, 6})],
)
def test_case_lastmod_follows_amended_results_within_declared_scope(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    scope: dict[str, int | list[int]],
    covered: set[int],
) -> None:
    result = {
        "id": "T-007",
        "kind": "lower-bound",
        "registered": "2026-10-07",
        "scope": scope,
        "amendments": [{"date": "2026-10-08"}],
    }
    records = tmp_path / "results.yaml"
    records.write_text(json.dumps({"results": [result]}), encoding="utf-8")
    monkeypatch.setattr(overview_data, "RESULTS", records)
    monkeypatch.setattr(
        render_research_tables, "load_cases", lambda: [{"n": n} for n in range(3, 8)]
    )
    monkeypatch.setattr(render_overview, "PAGES", {"index.html": None})
    monkeypatch.setattr(render_overview, "PAPERS", ())
    monkeypatch.setattr(render_overview, "MOVED_PAGES", ())
    monkeypatch.setattr(render_overview, "MOVED_FILES", ())
    monkeypatch.setattr(render_overview, "support_file_paths", lambda: ())
    monkeypatch.setattr(site_documents, "chapter_names", lambda: ())
    rows = {row.path: row for row in site_urls.derive_registry()}
    assert rows["result/t-007.html"].lastmod == "2026-10-08"
    for n in range(3, 8):
        expected = "2026-10-08" if n in covered else "2026-10-07"
        assert rows[f"cases/{n}.html"].lastmod == expected


def test_standalone_case_figure_is_registered_from_support_declarations() -> None:
    path = "atlas/trump11-overview.svg"
    assert path in render_overview.support_file_paths()
    rows = {row.path: row for row in site_urls.derive_registry(site_urls.load_registry())}
    registered = rows[path]
    assert registered.kind == "asset-file"
    assert registered.producer == "overview"
    assert registered.canonical == path
