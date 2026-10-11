"""The orientation refresh delegates to maintained producers within its case scope."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from devtools import refresh_atlas_orientation as tool
from devtools.atlas_orientation import PARENT_FACTS, PARENT_SOURCE_KEY
from devtools.regularize_axis_components import AtlasLayout
from devtools.render_regularized_atlas import Layout


@pytest.fixture
def scoped_refresh(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[list[tuple[Any, ...]], list[Path]]:
    entries = [{"n": n, "witness": {"path": f"n-{n}.yaml"}} for n in (210, 211, 212)]
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"atlas": {"entries": entries}}))
    layout = AtlasLayout(tmp_path, tmp_path, manifest, tmp_path, tmp_path)
    monkeypatch.setattr(tool.regularizer, "ATLAS", layout)
    monkeypatch.setattr(
        tool,
        "load_witness",
        lambda *_args, **_kwargs: {
            "n": 211,
            "source": {"path": PARENT_FACTS, "key": PARENT_SOURCE_KEY},
            "certificate": {"geometry_transform": {"operation": "reflect-y-axis"}},
        },
    )
    calls = []
    monkeypatch.setattr(
        tool.regularizer,
        "update_atlas",
        lambda actual, **kwargs: calls.append(("regularize", actual, kwargs)),
    )
    monkeypatch.setattr(tool.renderer, "regularized_entries", lambda: entries)
    monkeypatch.setattr(tool.renderer, "LAYOUT", Layout(tmp_path, manifest, tmp_path))
    monkeypatch.setattr(tool.renderer, "render", lambda entry: f"<svg>n={entry['n']}</svg>")
    monkeypatch.setattr(
        tool.screen,
        "update",
        lambda workers, **kwargs: calls.append(("screen", workers, kwargs)),
    )
    frontier = [tmp_path / f"frontier-{n}.md" for n in (210, 211, 212)]
    for path in frontier:
        path.write_text("before")
    monkeypatch.setattr(
        tool.rigidity,
        "plan",
        lambda: [
            (n, path, "before", "after")
            for n, path in zip((210, 211, 212), frontier, strict=True)
        ],
    )
    return calls, frontier


def test_refresh_updates_only_the_registered_case_via_scoped_producers(
    scoped_refresh: tuple[list[tuple[Any, ...]], list[Path]],
) -> None:
    calls, frontier = scoped_refresh
    manifest_before = tool.regularizer.ATLAS.manifest.read_bytes()
    assert tool.main(["--n", "211"]) == 0
    assert calls == [
        ("regularize", tool.regularizer.ATLAS, {"only": [211], "workers": 1}),
        ("screen", 1, {"only": [211]}),
    ]
    assert [path.read_text() for path in frontier] == ["before", "after", "before"]
    assert tool.renderer.LAYOUT.rendering(211).read_text() == "<svg>n=211</svg>"
    assert not tool.renderer.LAYOUT.rendering(210).exists()
    assert not tool.renderer.LAYOUT.rendering(212).exists()
    assert tool.regularizer.ATLAS.manifest.read_bytes() == manifest_before


@pytest.mark.parametrize("numbers", [[], [210], [211, 211], [211, 212]])
def test_refresh_refuses_unregistered_or_duplicate_counts_before_writes(
    scoped_refresh: tuple[list[tuple[Any, ...]], list[Path]],
    numbers: list[int],
) -> None:
    calls, frontier = scoped_refresh
    with pytest.raises(ValueError, match="unique registered counts"):
        tool.refresh(numbers)
    assert calls == []
    assert all(path.read_text() == "before" for path in frontier)


def test_refresh_refuses_an_unreflected_selected_witness_before_writes(
    scoped_refresh: tuple[list[tuple[Any, ...]], list[Path]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls, frontier = scoped_refresh
    monkeypatch.setattr(tool, "load_witness", lambda *_args, **_kwargs: {"n": 211})
    with pytest.raises(ValueError, match="current orientation"):
        tool.refresh([211])
    assert calls == []
    assert all(path.read_text() == "before" for path in frontier)


def test_refresh_refuses_the_superseded_vertical_orientation_before_writes(
    scoped_refresh: tuple[list[tuple[Any, ...]], list[Path]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls, frontier = scoped_refresh
    monkeypatch.setattr(
        tool,
        "load_witness",
        lambda *_args, **_kwargs: {
            "n": 211,
            "source": {"path": PARENT_FACTS, "key": PARENT_SOURCE_KEY},
            "certificate": {"geometry_transform": {"operation": "reflect-x-axis"}},
        },
    )
    with pytest.raises(ValueError, match="current orientation"):
        tool.refresh([211])
    assert calls == []
    assert all(path.read_text() == "before" for path in frontier)


@pytest.mark.parametrize("changed_manifest", [False, True])
def test_selected_refresh_preserves_the_manifest_or_refuses_before_writing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    changed_manifest: bool,
) -> None:
    entry = {
        "n": 211,
        "witness": {"path": "selected.yaml"},
        "rendering": {"path": "house.svg"},
    }
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"atlas": {"entries": [entry]}}))
    layout = AtlasLayout(tmp_path, tmp_path, manifest, tmp_path, tmp_path)
    for name in ("selected.yaml", "house.svg", "unselected.yaml"):
        (tmp_path / name).write_text("before")
    calls = []

    def build(numbers: list[int], workers: int) -> list[SimpleNamespace]:
        calls.append((numbers, workers))
        return [SimpleNamespace(witness_text="selected after", rendering_text="house after")]

    monkeypatch.setattr(tool.builder, "built_cases", build)
    monkeypatch.setattr(
        tool.builder,
        "_manifest_entry",
        lambda _case: {**entry, "reported_side": "changed"} if changed_manifest else entry,
    )
    before = manifest.read_bytes()
    refresh = tool._refresh_selected  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    if changed_manifest:
        with pytest.raises(ValueError, match="would change manifest facts"):
            refresh([entry], layout)
        assert (tmp_path / "selected.yaml").read_text() == "before"
        assert (tmp_path / "house.svg").read_text() == "before"
    else:
        refresh([entry], layout)
        assert (tmp_path / "selected.yaml").read_text() == "selected after"
        assert (tmp_path / "house.svg").read_text() == "house after"
    assert calls == [([211], 1)]
    assert manifest.read_bytes() == before
    assert (tmp_path / "unselected.yaml").read_text() == "before"
