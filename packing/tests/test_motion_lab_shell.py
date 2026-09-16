"""Shared Motion Lab assets and exact-scenario adapter contracts."""

from __future__ import annotations

import re

import pytest
from nodejs_wheel import node

from devtools.packing_motion_studies import build_motion_lab_manifest
from devtools.render_general_motion_lab import render_general_motion_lab
from devtools.render_packing_motion_lab import (
    CSS,
    MOTION_MODEL_JAVASCRIPT,
    MOTION_PAGE_JAVASCRIPT,
    render_motion_lab,
)
from sqpack.motion_lab.assets import asset_text, motion_lab_css
from sqpack.motion_lab.contracts import Capability, ScenarioRunner
from sqpack.motion_lab.scenarios.exact_n5 import exact_n5_scenario
from sqpack.render.style import (
    CONTACT_HIGHLIGHT_COLOR,
    PACKING_BOUNDARY_COLOR,
    SQUARE_FILL_PALETTE,
)


def test_exact_lab_uses_package_owned_shared_assets_and_visual_tokens() -> None:
    assert motion_lab_css() == CSS
    assert asset_text("exact-n5-model.js") == MOTION_MODEL_JAVASCRIPT
    assert asset_text("motion-lab.js") == MOTION_PAGE_JAVASCRIPT
    assert "--radius: 6px" in CSS
    assert "border-radius: 18px" not in CSS
    assert f"--packing-boundary: {PACKING_BOUNDARY_COLOR}" in CSS
    assert f"--contact: {CONTACT_HIGHLIGHT_COLOR}" in CSS
    for index, color in enumerate(SQUARE_FILL_PALETTE):
        assert f"--square-{index:02d}: {color}" in CSS


def test_exact_manifest_adapts_to_the_shared_scenario_contract() -> None:
    scenario = exact_n5_scenario(build_motion_lab_manifest())

    assert scenario.scenario_id == "exact-n5"
    assert scenario.runner is ScenarioRunner.ANALYTIC
    assert scenario.capabilities == (Capability.PLAYBACK, Capability.SCRUB)
    assert scenario.initial_frame.scenario_id == "exact-n5"
    assert [square.palette_index for square in scenario.initial_frame.squares] == list(range(5))

    with pytest.raises(ValueError, match="unsupported exact n=5 motion manifest"):
        exact_n5_scenario({"contract": "unversioned", "schema_version": 1})


def test_asset_loader_rejects_names_outside_the_owned_bundle() -> None:
    with pytest.raises(ValueError, match="unknown Motion Lab asset"):
        asset_text("../../pyproject.toml")


#: A `<script>` opening tag and its `type`, if it has one.
SCRIPT_TAG = re.compile(r"<script\b([^>]*)>")
SCRIPT_TYPE = re.compile(r'\btype="([^"]+)"')

#: Each rendered lab, and its scripts in the order the page must run them.
LAB_SCRIPTS = {
    "exact n=5": (render_motion_lab, ("exact-n5-model.js", "motion-lab.js")),
    "general": (
        lambda: render_general_motion_lab(n=5, seed=7, side=3.2),
        ("free-quench-model.js", "free-quench.js"),
    ),
}


@pytest.mark.parametrize(
    "asset", sorted({name for _, names in LAB_SCRIPTS.values() for name in names})
)
def test_each_browser_script_parses_as_the_module_it_ships_as(asset: str) -> None:
    """Parsed as a module, which is strict: `with`, octal literals and duplicate parameters are
    errors here exactly as they are in the page."""
    completed = node(
        ["--check", "--input-type=module", "-"],
        return_completed_process=True,
        input=asset_text(asset),
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


@pytest.mark.parametrize("lab", sorted(LAB_SCRIPTS))
def test_each_lab_runs_its_scripts_as_separate_module_scripts_in_order(lab: str) -> None:
    """The scripts carry no strict-mode directive, so a classic `<script>` would run them
    sloppy; and they share nothing by scope, so neither may be concatenated into the other."""
    render, names = LAB_SCRIPTS[lab]
    rendered = render()
    kinds = [
        found.group(1) if found else "classic"
        for found in (SCRIPT_TYPE.search(tag) for tag in SCRIPT_TAG.findall(rendered))
    ]
    assert set(kinds) <= {"application/json", "module"}, kinds
    assert kinds.count("module") == len(names)
    positions = [
        rendered.index(f'<script type="module">{asset_text(name)}</script>') for name in names
    ]
    assert positions == sorted(positions)


def test_exact_artifact_declares_the_scenario_registry_for_the_shared_shell() -> None:
    rendered = render_motion_lab()

    assert 'data-shell-contract="packing.squares:MotionLabShell/v1"' in rendered
    assert 'id="scenario-registry" type="application/json"' in rendered
    assert '"scenario_id": "exact-n5"' in rendered
    assert '"capabilities": [' in rendered
    assert '"playback"' in rendered
    assert '"scrub"' in rendered
