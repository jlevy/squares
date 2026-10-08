"""Capture receipts read the published corpus without changing the offline contract."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from workbench_tools import capture_video


def test_capture_reads_a_published_corpus_relative_to_the_page(tmp_path: Path) -> None:
    payload = json.dumps(
        {"version": "v0.4.1-f5e113", "citations": {"sha256": "c" * 64}}
    ).encode()
    digest = hashlib.sha256(payload).hexdigest()[:16]
    data = tmp_path / "data" / f"corpus.{digest}.json"
    data.parent.mkdir()
    data.write_bytes(payload)
    page = (
        '<script id="atlas-data" type="application/json" '
        f'data-src="data/{data.name}">null</script>'
    )
    edition = capture_video.page_edition(page, page_path=tmp_path / "index.html")
    assert edition == capture_video.PageEdition("v0.4.1-f5e113", "c" * 64)
    with pytest.raises(SystemExit, match="needs the page path"):
        capture_video.page_edition(page)
    data.write_text("{}")
    with pytest.raises(SystemExit, match="content-addressed"):
        capture_video.page_edition(page, page_path=tmp_path / "index.html")
