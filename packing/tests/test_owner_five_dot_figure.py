"""Keep the explanatory graphic tied to the retained full-direction result."""

from __future__ import annotations

import json
from pathlib import Path

from devtools.render_owner_five_dot_figure import ARTIFACT, REPLAY, load_data, render_figure


def test_retained_figure_matches_its_sources() -> None:
    assert ARTIFACT.read_text() == render_figure()


def test_figure_refuses_a_coverage_hole_hidden_by_the_summary(tmp_path: Path) -> None:
    replay = json.loads(REPLAY.read_text())
    replay["directions"][180]["minimum_covered_mass"] = "0"
    damaged = tmp_path / "missing-direction-coverage.json"
    damaged.write_text(json.dumps(replay))
    try:
        load_data(replay=damaged)
    except ValueError as error:
        assert "four-owner five-dot result" in str(error)
    else:
        raise AssertionError("A zero-coverage direction must prevent the proof illustration")
