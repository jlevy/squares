"""The payload counter includes automatic resources and refuses lossy projections."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest

from devtools.measure_exact_catalogue_web import (
    check_projection,
    initial_assets,
    local_path,
    working_tree_dirty,
)
from devtools.report_exact_catalogue_web import CAMPAIGN, report


def test_counts_automatic_assets_once_and_follows_css(tmp_path: Path) -> None:
    (tmp_path / "papers").mkdir()
    page = tmp_path / "papers/browser.html"
    page.write_text(
        '<style>@font-face {src:url("font.woff2")}</style>'
        '<script src="browser.js"></script><script src="browser.js"></script>'
        '<link rel="stylesheet" href="browser.css">'
        '<main data-index-url="index.json"></main>'
        '<a href="coefficients.json">deferred</a>',
        encoding="utf-8",
    )
    for name, content in (
        ("browser.js", "void 0"),
        ("browser.css", "a{background:url(icon.svg)}"),
        ("font.woff2", "font"),
        ("icon.svg", "svg"),
        ("index.json", "{}"),
        ("coefficients.json", "deferred"),
    ):
        (page.parent / name).write_text(content, encoding="utf-8")
    assets, index = initial_assets(page, tmp_path)
    assert index == page.parent / "index.json"
    assert set(assets) == {
        f"papers/{name}"
        for name in (
            "browser.html",
            "browser.js",
            "browser.css",
            "font.woff2",
            "icon.svg",
            "index.json",
        )
    }
    assert sum(assets.values()) == sum((tmp_path / name).stat().st_size for name in assets)


@pytest.mark.parametrize(
    "url", ["../../outside.json", "https://example.com/file.json", "absent.json"]
)
def test_refuses_uncounted_assets(tmp_path: Path, url: str) -> None:
    with pytest.raises(ValueError, match="asset"):
        local_path(url, base=tmp_path, site=tmp_path)


def test_projection_keeps_zero_and_large_integer_strings(tmp_path: Path) -> None:
    papers = tmp_path / "papers"
    data = papers / "data"
    data.mkdir(parents=True)
    vector = ["1", "0", "-" + "9" * 724]
    original = {
        "n": 83,
        "status": "open",
        "polynomial": {"coefficients": vector, "text": "large", "latex": "large"},
    }
    register = {"entries": [original], "historical_entries": [], "summary": {"proved": 0}}
    index = {
        "entries": [
            {"id": "current-83", "section": "current", "metadata_url": "data/metadata.json"}
        ],
        "summary": {"proved": 0},
    }
    metadata = {
        "id": "current-83",
        "section": "current",
        "record": {
            "n": 83,
            "status": "open",
            "polynomial": {"coefficients_url": "data/coefficients.json", "order": "descending"},
        },
    }
    payload: dict[str, Any] = {"order": "descending", "coefficients": list(vector)}
    for name, content in (("index", index), ("metadata", metadata), ("coefficients", payload)):
        (data / f"{name}.json").write_text(json.dumps(content), encoding="utf-8")
    assert check_projection(register, data / "index.json", tmp_path) == {
        "current": 1,
        "historical": 0,
        "coefficient_vectors": 1,
        "integer_coefficients": 3,
    }
    payload["coefficients"][1] = "1"
    (data / "coefficients.json").write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="coefficient strings"):
        check_projection(register, data / "index.json", tmp_path)


def test_recorded_report_is_current() -> None:
    assert report() == (CAMPAIGN / "report.md").read_text(encoding="utf-8")


def test_report_refuses_forged_acceptance(tmp_path: Path) -> None:
    copied = tmp_path / "record"
    shutil.copytree(CAMPAIGN, copied)
    receipt = copied / "exp-001-bytes.json"
    measured = json.loads(receipt.read_text(encoding="utf-8"))
    measured["passes_acceptance"] = False
    receipt.write_text(json.dumps(measured), encoding="utf-8")
    with pytest.raises(ValueError, match="registered threshold"):
        report(copied)


def test_provenance_includes_staged_and_untracked_inputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name in tuple(os.environ):
        if name.startswith("GIT_"):
            monkeypatch.delenv(name)

    def git(*arguments: str) -> None:
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Provenance Control",
                "-c",
                "user.email=control@example.invalid",
                "-c",
                "core.hooksPath=/dev/null",
                *arguments,
            ],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

    git("init", "-q", "-b", "main")
    git("commit", "--allow-empty", "-qm", "control")
    assert not working_tree_dirty(tmp_path)
    source = tmp_path / "source.txt"
    source.write_text("first input", encoding="utf-8")
    assert working_tree_dirty(tmp_path)
    git("add", "source.txt")
    assert working_tree_dirty(tmp_path)
    git("commit", "-qm", "retained input")
    assert not working_tree_dirty(tmp_path)
    source.write_text("edited input", encoding="utf-8")
    assert working_tree_dirty(tmp_path)
    git("add", "source.txt")
    assert working_tree_dirty(tmp_path)
