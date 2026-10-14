"""The homepage previews bound their actual content while keeping complete records linked."""

from __future__ import annotations

import inspect
import re
from collections.abc import Callable, Mapping
from copy import deepcopy
from dataclasses import replace
from datetime import timedelta
from typing import Any, cast
from unittest.mock import patch

import mpmath as mp
import pytest

from devtools import overview_data, overview_sections


@pytest.fixture(scope="module")
def atlas_markup() -> Callable[[str], str]:
    """Build each immutable surface once, inside the test call that first requests it."""
    built: dict[str, str] = {}
    drawing = overview_sections._atlas_drawing  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]

    def validated_drawing(
        n: int, *, regularized: bool, side: float, upper: Mapping[str, Any] | None = None
    ) -> str:
        # frontier_cases still validates every real case; each cell must receive that
        # metadata. Recency independently reads complete cases through the same loader.
        assert upper is not None, "an atlas cell must reuse its validated case metadata"
        return drawing(n, regularized=regularized, side=side, upper=upper)

    def surface(name: str) -> str:
        if name not in {"grid", "preview"}:
            raise ValueError(f"unknown Atlas surface: {name}")
        if name not in built:
            with patch.object(
                overview_sections, "_atlas_drawing", side_effect=validated_drawing
            ):
                built[name] = (
                    overview_sections.atlas_grid()
                    if name == "grid"
                    else overview_sections.atlas_preview()
                )
        return built[name]

    return surface


def test_results_table_omits_the_superseded_bottom_legend() -> None:
    overview = overview_data.load()
    table = overview_sections.results_table(overview)
    assert "site-rung-legend" not in table
    assert "What each rung means" not in table
    # The full Results documentation still defines every rung and remains linkable.
    ladders = overview_sections.verification_block()
    for label in overview_sections.rung_meanings():
        assert label in ladders
    assert overview_sections.LADDERS_SECTION == "verification-ladders"


def test_canonical_atlas_targets_keep_every_tile_addressable_without_scripts(
    atlas_markup: Callable[[str], str],
) -> None:
    grid = atlas_markup("grid")
    assert overview_sections.ATLAS_DEFAULT == "triangle"
    assert 'data-atlas-view="triangle" data-atlas-size="small"' in grid
    assert 'data-atlas-first="100" data-atlas-grid' in grid
    tabs = overview_sections.atlas_view_tabs()
    selected = re.findall(r'<button[^>]*aria-selected="true"[^>]*>', tabs)
    assert len(selected) == 1
    assert 'data-atlas-tab="triangle"' in selected[0]
    assert re.findall(r'id="atlas-n-(\d+)"', grid) == [str(n) for n in range(1, 325)]
    assert 'id="atlas-n-324" href="cases/324.html" data-case="324"' in grid
    fallback = grid.split("<noscript>", 1)[1].split("</noscript>", 1)[0]
    assert "[data-atlas-grid] .site-atlas-rest[hidden]{display:contents}" in fallback
    assert "[data-atlas-grid] .site-atlas-toggle-row{display:none}" in fallback
    assert 'href="atlas.html#the-frontier-survey"' in fallback
    assert 'href="atlas.html#the-frontier-survey"' in overview_sections.page_cards()
    assert 'href="frontier.html"' not in fallback


def test_recent_preview_contains_only_the_twelve_newest_eligible_rows() -> None:
    overview = overview_data.load()
    reference = overview_sections.reference_date(overview)
    cutoff = (reference - timedelta(days=180)).isoformat()
    assert (
        overview_sections.FilterDefaults(significance=4, max_age=180, hide_superseded=True)
        == overview_sections.RECENT_DEFAULTS
    )
    # The record currently has six eligible major results. Promote current S3
    # results in this fixture so the twelve-row DOM cap is exercised.
    extras = [
        result
        for result in overview.results
        if result.record["significance"]["score"] == 3
        and not overview_sections.is_superseded(result)
        and overview_sections.first_day(result.dated[1]) >= cutoff
    ][:12]
    promoted = {
        extra.id: replace(
            extra,
            record={
                **extra.record,
                "significance": {**extra.record["significance"], "score": 4},
            },
        )
        for extra in extras
    }
    overview = replace(
        overview,
        results=[promoted.get(result.id, result) for result in overview.results],
    )
    eligible = [
        result
        for result in overview_sections.recent_results(overview)
        if result.record["significance"]["score"] >= 4
        and not overview_sections.is_superseded(result)
        and overview_sections.first_day(result.dated[1]) >= cutoff
    ]
    assert len(eligible) > 12
    preview = overview_sections.recent_table(overview)
    rows = re.findall(r'<tr data-result="([^"]+)"([^>]*)>', preview)
    assert [result_id for result_id, _ in rows] == [
        result.id.lower() for result in eligible[:12]
    ]
    assert all(" hidden" not in attributes for _, attributes in rows)
    for _, attributes in rows:
        significance = re.search(r'data-s="(\d+)"', attributes)
        dated = re.search(r'data-date="([^"]+)"', attributes)
        assert significance is not None
        assert int(significance[1]) >= 4
        assert dated is not None
        assert dated[1] >= cutoff
        assert 'data-current="true"' in attributes
    assert preview.count('class="site-popover site-row-pop"') == len(rows)
    for result in eligible[:12]:
        assert f'href="result/{result.id.lower()}.html"' in preview
    assert "site-recent-scope" not in preview
    assert "Showing 12 of" not in preview
    assert "from the last 180 days" not in preview
    attributes = overview_sections.all_results_link_attributes(overview)
    assert attributes.startswith("data-all-results ")
    assert f'data-result-ids="{" ".join(r.id.lower() for r in overview.results)}"' in (
        attributes
    )
    assert "data-retired-results=" in attributes


def test_atlas_preview_reuses_canonical_split_rows_and_keeps_every_case(
    atlas_markup: Callable[[str], str],
) -> None:
    complete = atlas_markup("grid")
    preview = atlas_markup("preview")
    tiles = re.findall(r'<a class="site-atlas-cell"[^>]*>.*?</a>', preview)
    assert len(tiles) == 324
    assert tiles == re.findall(r'<a class="site-atlas-cell"[^>]*>.*?</a>', complete)
    assert [int(n) for n in re.findall(r'data-atlas-n="(\d+)"', preview)] == list(range(1, 325))
    assert 'data-atlas-view="triangle" data-atlas-size="small"' in preview
    assert 'data-atlas-count="100"' in preview
    assert 'id="homepage-atlas-cells"' in preview
    assert 'data-atlas-first="100"' in preview
    visible, rest = preview.split('<div class="site-atlas-rest" data-atlas-rest hidden>', 1)
    assert re.findall(r'data-atlas-row="(\d+)"', visible) == list(map(str, range(1, 11)))
    assert re.findall(r'data-atlas-row="(\d+)"', rest) == list(map(str, range(11, 19)))
    assert preview.count('data-atlas-segment="non-grid"') == 18
    assert preview.count('data-atlas-segment="grid"') == 18
    for n, tile in enumerate(tiles, 1):
        assert f'id="atlas-n-{n}" href="cases/{n}.html" data-case="{n}"' in tile
        assert "<img " in tile
        assert 'loading="lazy"' in tile
        assert 'class="site-star"' not in tile
        recent = overview_sections.recent_contributions_by_case()[n].any
        assert (", new result" in tile) == recent
        assert 'class="site-atlas-n"' in tile
        assert 'class="site-atlas-n is-new-result"' not in tile
        assert "evidence-badge" not in tile
    assert preview.count('id="pop-case"') == 1
    assert preview.count('role="tab"') == complete.count('role="tab"') == 10
    assert 'data-atlas-drawing="regularized"' in preview
    drawing_tabs = overview_sections.atlas_drawing_tabs("homepage-atlas-cells")
    assert preview.count(drawing_tabs) == 1
    assert drawing_tabs.count('role="tab"') == 2
    selected = re.findall(r'<button[^>]*aria-selected="true"[^>]*>', drawing_tabs)
    assert len(selected) == 1
    assert 'data-atlas-drawing-tab="regularized"' in selected[0]
    assert "data-atlas-toggle data-homepage-atlas-toggle" in preview
    assert preview.count("data-atlas-legend") == complete.count("data-atlas-legend")
    assert 'aria-controls="atlas-cells"' not in preview
    assert preview.count('aria-controls="homepage-atlas-cells"') == 11
    assert len(preview.encode("utf-8")) < 400_000
    for absent in (
        "data-homepage-atlas-gzip",
        "data-homepage-atlas-svg",
        "<noscript>",
    ):
        assert absent not in preview


@pytest.mark.parametrize("regularized", [False, True])
def test_validated_upper_metadata_keeps_the_drawing_without_reopening_the_case(
    monkeypatch: pytest.MonkeyPatch, *, regularized: bool
) -> None:
    from devtools import build_bound_citations  # noqa: PLC0415

    n = next(iter(overview_sections.atlas_regularized()))
    upper = build_bound_citations.load_case(n)["reported_upper_bound"]
    side = overview_sections.atlas_enclosing_sides(original=not regularized)[n]
    drawing = overview_sections._atlas_drawing  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    baseline = drawing(n, regularized=regularized, side=side)

    def reopened(_n: int) -> dict:
        pytest.fail("validated atlas metadata must not reopen its frontier case")

    monkeypatch.setattr(build_bound_citations, "load_case", reopened)
    assert drawing(n, regularized=regularized, side=side, upper=upper) == baseline


def test_shared_atlas_markup_builds_lazily_and_restores_its_drawing_guard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []
    drawing = overview_sections._atlas_drawing  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]

    def grid() -> str:
        assert overview_sections._atlas_drawing is not drawing  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        calls.append("grid")
        return "immutable grid"

    def preview() -> str:
        assert overview_sections._atlas_drawing is not drawing  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        calls.append("preview")
        if calls.count("preview") == 1:
            raise RuntimeError("injected render failure")
        return "immutable preview"

    monkeypatch.setattr(overview_sections, "atlas_grid", grid)
    monkeypatch.setattr(overview_sections, "atlas_preview", preview)
    factory = cast(Callable[[], Callable[[str], str]], inspect.unwrap(atlas_markup))
    surface = factory()
    assert calls == []
    assert surface("grid") == "immutable grid"
    assert overview_sections._atlas_drawing is drawing  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert surface("grid") == "immutable grid"
    assert calls == ["grid"]
    with pytest.raises(RuntimeError, match="injected render failure"):
        surface("preview")
    assert overview_sections._atlas_drawing is drawing  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert surface("preview") == "immutable preview"
    assert surface("preview") == "immutable preview"
    assert calls == ["grid", "preview", "preview"]
    assert overview_sections._atlas_drawing is drawing  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    with pytest.raises(ValueError, match="unknown Atlas surface"):
        surface("unexpected")
    assert calls == ["grid", "preview", "preview"]


def _side_reader_witness(kind: str) -> dict[str, Any]:
    witness: dict[str, Any] = {
        "id": "W-side-reader-control",
        "n": 1,
        "side": "2",
        "representation": "center-basis",
        "scalar": {"kind": kind},
        "coordinates": {"origin": "lower-left", "angle_unit": "not-applicable"},
        "squares": [{"center": ["1/2", "1/2"], "basis": ["1", "0"]}],
        "claim": {
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "limitations": "presentation control only",
        },
    }
    if kind == "algebraic-number-field":
        witness["scalar"].update(
            minimal_polynomial=["1", "0", "-2"], isolating_interval=["1", "2"]
        )
        witness["side"] = ["16/3", "5/3"]
    elif kind == "decimal":
        witness["side"] = "2.000000000000000001"
        witness["representation"] = "center-angle"
        witness["coordinates"]["angle_unit"] = "radians"
        witness["squares"] = [{"center": ["1/2", "0.5"], "angle": "1/2"}]
        witness["claim"].update(
            coordinate_provenance="numerically-checked",
            method="numerical-multiprecision",
            precision={"decimal_digits": 80, "rounding": "nearest"},
            tolerance="1e-60",
        )
        witness["certificate"] = {"result": {"check_passed": True}}
    return witness


@pytest.mark.parametrize("kind", ["rational", "algebraic-number-field", "decimal"])
def test_side_reader_retains_the_full_frames_scalar_identity(kind: str) -> None:
    from devtools import build_known_best_atlas as builder  # noqa: PLC0415

    witness = _side_reader_witness(kind)
    with mp.workdps(11):
        side = builder.side_from_witness(witness)
        assert mp.mp.dps == 11, "a layout-side read must not change ambient precision"
    assert side == builder.frame_from_witness(witness).container_side


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("root", "isolating interval must be nonempty"),
        ("coefficients", "coefficient-string arrays"),
        ("exact-angle", "angle evaluation is unavailable"),
        ("missing-center", "center"),
        ("decimal-nonstring", "decimal literals must be strings"),
        ("decimal-nan", "finite value"),
        ("decimal-infinity", "finite value"),
        ("decimal-corner-nan", "finite value"),
        ("missing-receipt", "numerical receipt is absent or failed"),
        ("failed-receipt", "numerical receipt is absent or failed"),
        ("missing-claim-field", "limitations"),
        ("missing-id", "id"),
        ("malformed-source", "get"),
    ],
)
def test_side_reader_preserves_malformed_literal_and_receipt_refusals(
    mutation: str, message: str
) -> None:
    from devtools import build_known_best_atlas as builder  # noqa: PLC0415

    exact = mutation in {"root", "coefficients", "exact-angle", "missing-center"}
    witness = _side_reader_witness("algebraic-number-field" if exact else "decimal")
    if mutation == "root":
        witness["scalar"]["isolating_interval"] = ["1", "1"]
    elif mutation == "coefficients":
        witness["squares"][0]["center"][0] = [1, "0"]
    elif mutation == "exact-angle":
        witness["representation"] = "center-angle"
        witness["squares"][0]["angle"] = "0"
    elif mutation == "missing-center":
        del witness["squares"][0]["center"]
    elif mutation == "decimal-nonstring":
        witness["squares"][0]["center"][0] = 0.5
    elif mutation == "decimal-nan":
        witness["squares"][0]["center"][0] = "NaN"
    elif mutation == "decimal-infinity":
        witness["squares"][0]["center"][0] = "inf"
    elif mutation == "decimal-corner-nan":
        witness["representation"] = "corners"
        witness["squares"] = [{"corners": [["NaN", "0"], ["1", "0"], ["1", "1"], ["0", "1"]]}]
    elif mutation == "missing-receipt":
        del witness["certificate"]
    elif mutation == "failed-receipt":
        witness["certificate"]["result"]["check_passed"] = False
    elif mutation == "missing-claim-field":
        del witness["claim"]["limitations"]
    elif mutation == "missing-id":
        del witness["id"]
    else:
        witness["source"] = []
    before = deepcopy(witness)
    with mp.workdps(15):
        for reader in (builder.side_from_witness, builder.frame_from_witness):
            with pytest.raises((ValueError, KeyError, AttributeError), match=message):
                reader(witness)
    assert witness == before


def test_side_reader_reuses_originals_without_mutating_the_comparison_cache(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from devtools import build_known_best_atlas as builder  # noqa: PLC0415
    from devtools import render_regularized_atlas as regularized  # noqa: PLC0415
    from sqpack import yamlio  # noqa: PLC0415

    original = _side_reader_witness("rational")
    selected = deepcopy(original)
    selected["side"] = "3"
    manifest = {"atlas": {"entries": [{"n": 1, "witness": {"path": "witness.yaml"}}]}}
    parsed: list[str] = []
    read_text = overview_sections.Path.read_text

    def retained_text(path: Any, *args: Any, **kwargs: Any) -> str:
        if path.name == "manifest.json":
            import json  # noqa: PLC0415

            return json.dumps(manifest)
        if path.name == "witness.yaml":
            parsed.append(path.name)
            return "retained witness"
        return read_text(path, *args, **kwargs)

    monkeypatch.setattr(overview_sections.Path, "read_text", retained_text)
    monkeypatch.setattr(yamlio, "load_yaml", lambda _text: {"witness": original})
    monkeypatch.setattr(overview_sections, "atlas_regularized", lambda: (1,))
    monkeypatch.setattr(regularized, "regularized_entries", lambda: [{"n": 1}])
    monkeypatch.setattr(regularized, "view_witness", lambda _entry: selected)
    with patch.object(builder, "side_from_witness", wraps=builder.side_from_witness) as read:
        overview_sections.atlas_enclosing_sides.cache_clear()
        try:
            assert overview_sections.atlas_enclosing_sides() == {1: 3.0}
            assert overview_sections.atlas_enclosing_sides(original=True) == {1: 2.0}
            assert parsed == ["witness.yaml"]
            assert read.call_count == 2
            overview_sections.atlas_enclosing_sides.cache_clear()
            selected["side"] = "4"
            assert overview_sections.atlas_enclosing_sides() == {1: 4.0}
            assert read.call_count == 4, "cache_clear must invalidate both side modes"
            monkeypatch.setattr(regularized, "regularized_entries", list)
            overview_sections.atlas_enclosing_sides.cache_clear()
            with pytest.raises(KeyError, match="1"):
                overview_sections.atlas_enclosing_sides()
        finally:
            overview_sections.atlas_enclosing_sides.cache_clear()


@pytest.mark.parametrize("literal", ["1/0", "not-a-number"])
def test_side_reader_reports_invalid_decimal_pose_literals_as_witness_errors(
    literal: str,
) -> None:
    from devtools import build_known_best_atlas as builder  # noqa: PLC0415
    from sqpack.witness import WitnessError  # noqa: PLC0415

    witness = _side_reader_witness("decimal")
    witness["squares"][0]["center"][0] = literal
    with pytest.raises(WitnessError, match="invalid rational literal") as error:
        builder.side_from_witness(witness)
    assert error.value.kind == "malformed-scalar"
    # mpmath accepts rational strings directly and raises ZeroDivisionError for 1/0
    # before the full reader's Fraction fallback. Its existing refusal is retained.
    with pytest.raises((WitnessError, ZeroDivisionError)):
        builder.frame_from_witness(witness)
