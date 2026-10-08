"""The published URL boundary: omissions, identity changes, crawl files and aliases."""

import json
import os
import subprocess
from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path

import pytest

from devtools import (
    check_published_site,
    overview_data,
    paper_front,
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
        ("papers/n11-lower-bounds-explainer.html", 1_417_498),
        ("papers/n11-threshold-bound-review.html", 823_322),
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


@pytest.fixture(scope="module")
def t116_transition() -> tuple[site_urls.SiteURL, site_urls.SiteURL]:
    current = next(
        entry for entry in site_urls.load_registry() if entry.path == "result/t-116.html"
    )
    assert current.identity is not None
    assert current.identity["kind"] == "upper-bound"
    old = replace(
        current,
        status="withdrawn",
        target="result/t-110.html",
        tombstone="The provisional n=39 result was consolidated into T-110.",
        identity=site_urls.result_identity(
            {
                "kind": "lower-bound",
                "scope": {"n_values": [39]},
                "attribution": {
                    "source_keys": ["[wand125 mixed bounds check2 2026-10-06]"],
                    "published": "2026-10-06",
                },
                "evidence": ["E-n039-wand125-mixed-665-report"],
            }
        ),
        amendments=(),
    )
    amended = replace(
        current,
        amendments=(
            {
                "date": "2026-10-07",
                "reason": "Record the n=39 binding after main reused the provisional token.",
                "previous": old.identity,
                "historical_target": "result/t-110.html",
                "historical_title": "T-110: the former n=39 lower-bound result",
            },
        ),
    )
    return old, amended


def test_actual_t116_withdrawal_can_be_explicitly_amended(
    t116_transition: tuple[site_urls.SiteURL, site_urls.SiteURL],
) -> None:
    old, amended = t116_transition
    target = row("result/t-110.html")
    assert not failures(site_urls.check_history([amended, target], [old]))
    current_main_binding = replace(amended, amendments=())
    assert not failures(site_urls.check_history([amended, target], [current_main_binding]))
    derived = {entry.path: entry for entry in site_urls.derive_registry([amended])}
    assert derived[amended.path].amendments == amended.amendments
    assert derived[amended.path].first_published == "2026-10-06"


@pytest.mark.parametrize("amendment", ["absent", "wrong-previous"])
def test_t116_identity_change_requires_the_exact_previous_binding(
    t116_transition: tuple[site_urls.SiteURL, site_urls.SiteURL], amendment: str
) -> None:
    old, amended = t116_transition
    if amendment == "absent":
        candidate = replace(amended, amendments=())
    else:
        candidate = replace(
            amended, amendments=({**amended.amendments[0], "previous": {"wrong": True}},)
        )
    assert "identity" in failures(
        site_urls.check_history([candidate, row("result/t-110.html")], [old])
    )


@pytest.mark.parametrize("prefix", ["deleted", "rewritten"])
def test_accepted_amendment_prefix_cannot_be_removed_or_rewritten(
    t116_transition: tuple[site_urls.SiteURL, site_urls.SiteURL], prefix: str
) -> None:
    _, amended = t116_transition
    candidate = replace(
        amended,
        amendments=()
        if prefix == "deleted"
        else ({**amended.amendments[0], "reason": "Rewrite the accepted history."},),
    )
    assert "identity" in failures(
        site_urls.check_history([candidate, row("result/t-110.html")], [amended])
    )


def test_derivation_rejects_a_silent_withdrawn_to_live_identity_collision(
    t116_transition: tuple[site_urls.SiteURL, site_urls.SiteURL],
) -> None:
    old, _ = t116_transition
    with pytest.raises(ValueError, match="identity"):
        site_urls.derive_registry([old])


def test_history_seed_keeps_earliest_publication_and_latest_semantics(
    monkeypatch: pytest.MonkeyPatch,
    t116_transition: tuple[site_urls.SiteURL, site_urls.SiteURL],
) -> None:
    old, current = t116_transition
    frames = []
    for entry, registered in ((current, "2026-10-07"), (old, "2026-10-06")):
        record = {"id": "T-116", "registered": registered, **(entry.identity or {})}
        payload = json.dumps({"results": [record], "last_reviewed": registered}).encode()
        frames.append(f"record blob {len(payload)}\n".encode() + payload + b"\n")

    def run(
        args: list[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
        if args[1] == "log":
            return subprocess.CompletedProcess(args, 0, "latest\noriginal\n")
        if args[1] == "cat-file":
            if args[2] == "-e":
                return subprocess.CompletedProcess(args, 1, b"")
            return subprocess.CompletedProcess(args, 0, b"".join(frames))
        assert args[1] == "ls-tree"
        return subprocess.CompletedProcess(args, 0, "")

    declarations = (
        'PAGES = {"index.html": None}\nDOCUMENT_PAGES = ()\n'
        "MOVED_PAGES = ()\nMOVED_FILES = ()\nPAPERS = ()\n"
        'SOCIAL_CARD = "preview-card.png"\n'
    )
    monkeypatch.setattr(site_urls.subprocess, "run", run)
    monkeypatch.setattr(
        site_urls,
        "_git_read",
        lambda _ref, path: (
            "COMPOSITE_ASSETS = ()"
            if path.endswith("render_n11_lower_bounds_explainer.py")
            else declarations
        ),
    )
    seeded = {entry.path: entry for entry in site_urls.historical_registry("fixture")}
    result = seeded["result/t-116.html"]
    assert result.first_published == "2026-10-06"
    assert result.lastmod == "2026-10-07"
    assert result.identity == current.identity


def test_failed_history_write_leaves_both_generated_files_unchanged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry, document = tmp_path / "registry.yaml", tmp_path / "register.md"
    registry.write_bytes(b"accepted registry bytes\n")
    document.write_bytes(b"accepted document bytes\n")
    entries = [row("index.html")]
    monkeypatch.setattr(site_urls, "REGISTRY", registry)
    monkeypatch.setattr(site_urls, "DOCUMENT", document)
    monkeypatch.setattr(site_urls, "load_registry", lambda: entries)
    monkeypatch.setattr(site_urls, "derive_registry", lambda _previous: entries)
    monkeypatch.setattr(site_urls, "historical_registry", lambda _ref: entries)
    monkeypatch.setattr(
        site_urls, "check_history", lambda *_args: [(False, "rejected history")]
    )
    assert site_urls.main(["--write", "--history-ref", "fixture"]) == 1
    assert registry.read_bytes() == b"accepted registry bytes\n"
    assert document.read_bytes() == b"accepted document bytes\n"


def test_t116_registry_retains_the_complete_historical_source_binding() -> None:
    current = next(
        entry for entry in site_urls.load_registry() if entry.path == "result/t-116.html"
    )
    amendment = current.amendments[0]
    assert current.first_published == "2026-10-06"
    assert current.status == "live"
    assert amendment["date"] == "2026-10-07"
    assert amendment["historical_target"] == "result/t-110.html"
    previous = amendment["previous"]
    assert previous["kind"] == "lower-bound"
    assert previous["scope"] == {"n_values": [39]}
    assert previous["attribution"]["published"] == "2026-10-06"
    assert "E-n039-wand125-mixed-665-sqverify-fast-replay" in previous["evidence"]
    assert "packing/sqverify_fast/SOUNDNESS.md" in previous["artifacts"]


@pytest.mark.parametrize(
    ("published", "proof", "revised"),
    [
        ("September 5, 2026", "September 1, 2026", "October 5, 2026"),
        ("September 30, 2026", "September 29, 2026", "October 7, 2026"),
        ("October 5, 2026", "September 22, 2026", "October 5, 2026"),
        ("October 7, 2026", "September 22, 2026", "October 7, 2026"),
    ],
)
def test_paper_history_seed_uses_publication_history_not_original_proof(
    monkeypatch: pytest.MonkeyPatch, published: str, proof: str, revised: str
) -> None:
    declarations = (
        'PAGES = {"index.html": None}\nDOCUMENT_PAGES = ()\n'
        "MOVED_PAGES = ()\nMOVED_FILES = ()\n"
        'PAPERS = (PaperRecord(slug="example", module="devtools.example"),)\n'
        'SOCIAL_CARD = "preview-card.png"\n'
    )
    release = (
        "REVIEW_HISTORY = ("
        'PublicationHistoryEntry(version="v0.2.0", first_published="October 7, 2026"),'
        f'PublicationHistoryEntry(version="v0.1.0", first_published={published!r}),)\n'
        "REVIEW_VERSION = REVIEW_HISTORY[0].version\n"
        'REVIEW_EDITION = " ".join(part for part in ("Draft", REVIEW_VERSION) if part)\n'
        f"REVIEW_REVISED = {revised!r}\nPROOF_PUBLISHED = {proof!r}\n"
    )
    # Historical reviews lacked a First published front line. Their version history
    # records publication; the original proof line describes someone else's work.
    paper = (
        "FRONT = paper_front.check(paper_front.PaperFront("
        "version=REVIEW_EDITION, dates=("
        'paper_front.Dated("Original proof", PROOF_PUBLISHED),'
        "paper_front.Dated(paper_front.REVISED, REVIEW_REVISED))))"
    )
    sources = {
        "packing/devtools/render_overview.py": declarations,
        "packing/src/sqpack/release.py": release,
        "packing/devtools/example.py": paper,
        "packing/devtools/render_n11_lower_bounds_explainer.py": "COMPOSITE_ASSETS = ()",
    }
    reads: list[tuple[str, str]] = []

    def read(ref: str, path: str) -> str:
        reads.append((ref, path))
        return sources[path]

    monkeypatch.setattr(site_urls, "_git_read", read)
    monkeypatch.setattr(site_urls, "_historical_results", lambda _ref: [])
    monkeypatch.setattr(
        site_urls.subprocess,
        "run",
        lambda args, **_kwargs: subprocess.CompletedProcess(
            args, 1 if args[1] == "cat-file" else 0, ""
        ),
    )
    seeded = {entry.path: entry for entry in site_urls.historical_registry("trusted-history")}
    for extension in (".html", ".md", ".pdf"):
        paper_row = seeded[f"papers/example{extension}"]
        assert paper_row.first_published == paper_front.iso_date(published)
        assert paper_row.first_published != paper_front.iso_date(proof)
        assert paper_row.lastmod == paper_front.iso_date(revised)
    assert ("trusted-history", "packing/src/sqpack/release.py") in reads
    assert all(ref == "trusted-history" for ref, _path in reads)


@pytest.mark.parametrize(
    ("slug", "published"),
    [
        ("n11-lower-bounds-explainer", "2026-09-05"),
        ("n11-optimality-review", "2026-09-30"),
        ("n11-threshold-bound-review", "2026-10-05"),
    ],
)
def test_paper_registry_declares_first_publication_separately_from_proof(
    slug: str, published: str
) -> None:
    rows = {entry.path: entry for entry in site_urls.derive_registry()}
    for extension in (".html", ".md", ".pdf"):
        paper_row = rows[f"papers/{slug}{extension}"]
        assert paper_row.first_published == published
        assert paper_row.lastmod >= paper_row.first_published


def test_published_registry_dates_remain_authoritative_after_bootstrap_fix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    accepted = replace(
        row("papers/example.html"),
        kind="paper-file",
        first_published="2026-09-29",
        lastmod="2026-10-07",
    )
    document = site_urls.render_registry([accepted])

    def read(ref: str, path: str) -> str:
        assert ref == "published-main"
        assert path == "packing/site-urls.yaml"
        return document

    monkeypatch.setattr(site_urls, "_git_read", read)
    monkeypatch.setattr(
        site_urls.subprocess,
        "run",
        lambda args, **_kwargs: subprocess.CompletedProcess(args, 0, b""),
    )
    baseline = site_urls.historical_registry("published-main")
    assert baseline == [accepted]
    corrected = replace(accepted, first_published="2026-09-30")
    assert "first publication retained" in failures(
        site_urls.check_history([corrected], baseline)
    )


def test_overview_writer_emits_every_registered_crawl_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The real producer writes its crawler/withdrawal outputs, not only a preview."""
    monkeypatch.setattr(render_overview, "asset_files", lambda _pages: {})
    monkeypatch.setattr(render_overview, "support_files", dict)
    files, assets = site_urls.crawl_files()
    assert set(files) == {
        "404.html",
        "sitemap.xml",
        *(row.path for row in site_urls.load_registry() if row.status == "withdrawn"),
    }
    render_overview.write_site(tmp_path, ())
    assert all(
        (tmp_path / name).read_text(encoding="utf-8") == text for name, text in files.items()
    )
    assert all(
        (tmp_path / "assets" / name).read_bytes() == data for name, data in assets.items()
    )
    assert (
        sum(path.stat().st_size for path in tmp_path.rglob("*") if path.is_file()) < 10_000_000
    )


def test_every_partial_paper_or_workbench_check_stages_the_shared_card() -> None:
    from sqpack.yamlio import safe_load  # noqa: PLC0415

    workflow = safe_load((site_urls.REPO / ".github/workflows/pages.yml").read_text())
    jobs = workflow["jobs"]
    checked = []
    for name, job in jobs.items():
        for step in job.get("steps", []):
            command = step.get("run", "")
            if (
                "--partial --producer paper:" in command
                or "--partial --producer workbench" in command
            ):
                card = "python -m devtools.social_card --output-dir site"
                publication = "python -m devtools.check_published_site --local site --partial"
                assert card in command, name
                assert command.index(card) < command.index(publication), name
                checked.append(name)
    assert set(checked) == {
        "n11-optimality-review",
        "n11-threshold-bound-review",
        "square-packing-methods-survey",
        "workbench",
        "pdf",
    }


def _memory_site(monkeypatch: pytest.MonkeyPatch, files: dict[str, int]) -> Path:
    """Exercise physical ownership and byte ceilings without allocating site fixtures."""
    directory = Path("/virtual-publication")
    original_glob, original_file, original_stat = Path.rglob, Path.is_file, Path.stat

    def rglob(path: Path, pattern: str) -> Iterator[Path]:
        if path == directory:
            return iter(directory / name for name in files)
        return original_glob(path, pattern)

    def is_file(path: Path) -> bool:
        if path.is_relative_to(directory):
            return path.relative_to(directory).as_posix() in files
        return original_file(path)

    def stat(path: Path, *, follow_symlinks: bool = True) -> os.stat_result:
        if path.is_relative_to(directory):
            size = files[path.relative_to(directory).as_posix()]
            return os.stat_result((0, 0, 0, 0, 0, 0, size, 0, 0, 0))
        return original_stat(path, follow_symlinks=follow_symlinks)

    monkeypatch.setattr(Path, "rglob", rglob)
    monkeypatch.setattr(Path, "is_file", is_file)
    monkeypatch.setattr(Path, "stat", stat)
    return directory


def _catalogue_rows() -> list[site_urls.SiteURL]:
    return [
        replace(
            row(path),
            kind=kind,
            producer=site_urls.CATALOGUE_PRODUCER,
            generator=generator,
        )
        for path, (kind, generator) in site_urls.catalogue_output_contracts().items()
    ]


def test_catalogue_outputs_are_exact_and_required_for_the_selected_producer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rows = [*_catalogue_rows(), row("index.html")]
    files = {item.path: 1 for item in rows if item.producer == site_urls.CATALOGUE_PRODUCER}
    directory = _memory_site(monkeypatch, files)
    options = {"partial": True, "producers": (site_urls.CATALOGUE_PRODUCER,)}
    assert not failures(site_urls.check_site(directory, rows, **options))
    assert "required overview output missing" in failures(site_urls.check_site(directory, rows))
    for suffix in (
        "index.json",
        "metadata/current-n83.json",
        "coefficients/current-n83.json",
    ):
        name = site_urls.CATALOGUE_DATA_PREFIX + suffix
        assert name in files
        del files[name]
        failed = failures(site_urls.check_site(directory, rows, **options))
        assert f"site {name}: required {site_urls.CATALOGUE_PRODUCER} output missing" in failed
        files[name] = 1
    files["index.html"] = 1
    for name in (
        site_urls.CATALOGUE_DATA_PREFIX + "metadata/unowned.json",
        site_urls.CATALOGUE_DATA_PREFIX + "coefficients/unowned.json",
        "papers/unowned.js",
    ):
        files[name] = 1
        assert f"site {name}: unregistered file" in failures(
            site_urls.check_site(directory, rows, **options)
        )
        del files[name]
    coefficient = site_urls.CATALOGUE_DATA_PREFIX + "coefficients/current-n83.json"
    del files[coefficient]
    assert not failures(
        site_urls.check_site(directory, rows, partial=True, producers=("overview",))
    )
    assert coefficient in failures(site_urls.check_site(directory, rows))
    owned = next(item for item in rows if item.path == coefficient)
    for wrong in (
        replace(owned, producer="overview"),
        replace(owned, kind="paper-file"),
        replace(owned, generator="fixture:unowned"),
        replace(owned, path=site_urls.CATALOGUE_DATA_PREFIX + "unowned.json"),
    ):
        assert "exact renderer filename, type and owner" in failures(
            site_urls.validate_registry([wrong])
        )


def test_archive_cap_requires_the_exact_classified_path_and_owner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    archive = next(item for item in _catalogue_rows() if item.kind == "archive-file")
    files = {archive.path: 5_016_486}
    directory = _memory_site(monkeypatch, files)
    assert site_urls.HARD_HTML_LIMIT == 2_000_000
    assert site_urls.html_limit(archive) == 6_000_000
    assert not failures(site_urls.check_site(directory, [archive]))
    files[archive.path] = 6_000_001
    assert "hard limit 6000000" in failures(site_urls.check_site(directory, [archive]))
    files[archive.path] = 5_016_486
    for wrong in (
        replace(
            archive,
            path="papers/unowned-complete.html",
            canonical="papers/unowned-complete.html",
        ),
        replace(archive, producer="overview"),
        replace(archive, generator="fixture:unowned"),
        replace(archive, kind="paper-file"),
        replace(archive, canonical="papers/exact-side-values.html"),
    ):
        assert site_urls.html_limit(wrong) == site_urls.HARD_HTML_LIMIT
        assert failures(site_urls.validate_registry([wrong]))
    ordinary = replace(row("papers/unowned.html"), kind="paper-file")
    files.clear()
    files[ordinary.path] = 2_000_001
    assert "hard limit 2000000" in failures(site_urls.check_site(directory, [ordinary]))


def test_deployed_archive_uses_the_same_qualified_cap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    archive = next(item for item in _catalogue_rows() if item.kind == "archive-file")
    body = b"x" * 5_016_486
    monkeypatch.setattr(check_published_site, "head_checks", lambda *_args: [])

    def read(_url: str, *, timeout: float) -> tuple[int, bytes]:
        assert timeout == 1
        return 200, body

    assert not failures(
        check_published_site.deployed_registry_checks(
            "https://example.org/squares/", read, timeout=1, rows=[archive]
        )
    )
    body = b"x" * 6_000_001
    assert "registered HTML" in failures(
        check_published_site.deployed_registry_checks(
            "https://example.org/squares/", read, timeout=1, rows=[archive]
        )
    )
