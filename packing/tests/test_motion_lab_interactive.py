"""General Motion Lab editor, playback, and served-scenario contracts."""

from __future__ import annotations

import http.client
import json
import math
import random
import threading
from typing import cast

import pytest
from nodejs_wheel import node

from devtools.render_general_motion_lab import render_general_motion_lab
from devtools.serve_packing_motion_lab import LOOPBACK_HOST, create_server
from sqpack.motion_lab.assets import asset_text
from sqpack.motion_lab.contracts import MAX_INTERACTIVE_SQUARES
from sqpack.motion_lab.snap import (
    EditorSquare,
    EditorState,
    apply_best_snap,
    set_snapping,
)
from sqpack.render.style import SQUARE_FILL_PALETTE


def test_free_quench_browser_model_uses_one_reducer_for_snap_rotate_and_release() -> None:
    probe = (
        asset_text("free-quench-model.js")
        + r"""
const editor = globalThis.MotionLabEditor;
const baseline = {
  side: 3,
  squares: [
    {square_id: 0, x: 0.5, y: 1.5, theta: 0},
    {square_id: 1, x: 1.51, y: 1.5, theta: 0},
  ],
  groups: [[0], [1]],
  snapping_enabled: true,
};
const snapped = editor.applyBestSnap(baseline, 1, 0.05);
const before = Math.hypot(
  snapped.state.squares[0].x - snapped.state.squares[1].x,
  snapped.state.squares[0].y - snapped.state.squares[1].y,
);
const rotated = editor.rotateGroup(snapped.state, 1, Math.PI / 3);
const after = Math.hypot(
  rotated.squares[0].x - rotated.squares[1].x,
  rotated.squares[0].y - rotated.squares[1].y,
);
const request = editor.releaseQuenchRequest(rotated, 3, 4);
const longEvents = Array.from({length: 2651}, (_, index) => {
  let phase = index % 2 ? "fixed-angle-lp" : "angular-probe";
  if (index === 0) phase = "setup";
  if (index === 177) phase = "angle-accepted";
  if (index === 2650) phase = "stop";
  return {phase};
});
const playback = editor.selectPlaybackIndices(longEvents, 160);
const windowed = editor.timelineWindow(longEvents.length, 1300, 20);
process.stdout.write(JSON.stringify({
  snapped,
  before,
  after,
  request,
  fixed: editor.phasePresentation({phase: "fixed-angle-lp"}),
  probe: editor.phasePresentation({phase: "angular-probe", outcome: "rejected"}),
  playback,
  windowed,
}));
"""
    )
    completed = node(
        ["-e", probe],
        return_completed_process=True,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    result = cast(dict[str, object], json.loads(completed.stdout))
    snapped = cast(dict[str, object], result["snapped"])
    state = cast(dict[str, object], snapped["state"])
    assert state["groups"] == [[0, 1]]
    assert cast(dict[str, object], snapped["result"])["target_kind"] == "square"
    assert cast(float, result["before"]) == pytest.approx(cast(float, result["after"]))
    request = cast(dict[str, object], result["request"])
    assert set(request) == {
        "contract",
        "schema_version",
        "side",
        "x",
        "y",
        "theta",
        "solver",
        "max_sweeps",
        "time_budget",
    }
    assert "groups" not in request
    assert cast(dict[str, object], result["fixed"])["variant"] == "lp"
    assert cast(dict[str, object], result["probe"])["variant"] == "probe-rejected"
    playback = cast(list[int], result["playback"])
    assert len(playback) <= 160
    assert playback[0] == 0
    assert playback[-1] == 2650
    assert 177 in playback
    assert cast(dict[str, int], result["windowed"]) == {"start": 1280, "end": 1321}


def test_general_lab_is_deterministic_shared_scenario_ui() -> None:
    first = render_general_motion_lab(n=5, seed=7, side=3.2)
    second = render_general_motion_lab(n=5, seed=7, side=3.2)

    assert first == second
    assert 'data-contract="packing.squares:GeneralMotionLab/v1"' in first
    assert 'id="scenario-select"' in first
    assert '<option value="free-quench" selected>Setup + free quench</option>' in first
    assert '<option value="exact-n5">Exact n=5 paths</option>' in first
    assert 'id="snapping-toggle"' in first
    assert 'id="rotate-left-button"' in first
    assert 'id="run-button"' in first
    assert 'id="timeline-input"' in first
    assert "Setup snapping is released before every numerical run" in first
    assert "connect-src 'self'" in first
    assert "phase-fixed-angle-lp" in first
    assert "probe-square" in first
    assert "(prefers-reduced-motion: reduce)" in first
    assert "Reduced-motion mode advanced one retained event" in first
    assert '"scenario_id": "free-quench"' in first
    assert 'fetch("http' not in first
    assert '<script src="http' not in first
    assert '<link href="http' not in first


def test_general_browser_javascript_parses_as_shipped() -> None:
    javascript = asset_text("free-quench-model.js") + asset_text("free-quench.js")
    completed = node(
        ["--check", "-"],
        return_completed_process=True,
        input=javascript,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


@pytest.mark.slow
def test_service_serves_live_and_exact_profiles_with_scenario_refresh() -> None:
    server = create_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = cast(tuple[str, int], server.server_address)[1]
    connection = http.client.HTTPConnection(LOOPBACK_HOST, port, timeout=15)
    try:
        connection.request("GET", "/")
        response = connection.getresponse()
        live_html = response.read().decode()
        assert response.status == 200
        assert "GeneralMotionLab/v1" in live_html
        assert "connect-src 'self'" in response.headers["Content-Security-Policy"]

        connection.request("GET", "/exact-n5")
        response = connection.getresponse()
        exact_html = response.read().decode()
        assert response.status == 200
        assert "n=5 square-packing motion lab" in exact_html
        assert "connect-src 'none'" in response.headers["Content-Security-Policy"]

        connection.request("GET", "/api/scenario/free-quench?n=3&seed=11&side=2.75")
        response = connection.getresponse()
        scenario = json.loads(response.read())
        assert response.status == 200
        assert scenario["scenario_id"] == "free-quench"
        assert len(scenario["initial_frame"]["squares"]) == 3
        assert math.isclose(scenario["initial_frame"]["container_side"], 2.75)

        connection.request("GET", "/api/scenario/free-quench?n=3&n=4&side=2.75")
        response = connection.getresponse()
        failure = json.loads(response.read())
        assert response.status == 400
        assert failure["contract"] == "packing.squares:MotionLabError/v1"
        assert "exactly once" in failure["error"]["message"]
    finally:
        connection.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_browser_reducer_matches_its_python_reference_on_generated_states() -> None:
    """Two implementations of one reducer, and the browser runs the one users touch.

    `snap.py` is the reference the Python tests pin, but every drag in the lab is
    resolved by `free-quench-model.js`. Nothing tied the two together, so they could
    drift silently in either direction. Lattice coordinates and repeated angles are
    used deliberately: equal distances make the rank tie-break decide the answer, which
    is where a `min` and a comparator sort are most likely to disagree.
    """
    generator = random.Random(2026)
    cases: list[dict[str, object]] = []
    for _ in range(120):
        count = generator.randint(2, 6)
        squares = [
            EditorSquare(
                square_id=index,
                x=0.5 + generator.randrange(0, 9) * 0.5,
                y=0.5 + generator.randrange(0, 9) * 0.5,
                theta=generator.choice(
                    [0.0, 0.0, math.pi / 4, generator.uniform(0, math.pi / 2)]
                ),
            )
            for index in range(count)
        ]
        identifiers = list(range(count))
        generator.shuffle(identifiers)
        cut = generator.randint(1, count)
        singletons = [(value,) for value in sorted(identifiers[cut:])]
        groups = tuple(
            sorted(
                [tuple(sorted(identifiers[:cut])), *singletons],
                key=lambda group: group[0],
            )
        )
        state = EditorState(side=5.0, squares=tuple(squares), groups=groups)
        threshold = generator.choice([0.05, 0.2, 0.51])
        moving = generator.randrange(count)
        snapped, result = apply_best_snap(state, moving_square_id=moving, threshold=threshold)
        cases.append(
            {
                "state": {
                    "side": 5.0,
                    "squares": [
                        {"square_id": s.square_id, "x": s.x, "y": s.y, "theta": s.theta}
                        for s in squares
                    ],
                    "groups": [list(group) for group in groups],
                    "snapping_enabled": True,
                },
                "moving": moving,
                "threshold": threshold,
                "expected": {
                    "groups": [list(group) for group in snapped.groups],
                    "x": [s.x for s in snapped.squares],
                    "y": [s.y for s in snapped.squares],
                    "target": None
                    if result is None
                    else [result.target_kind.value, result.target_id],
                },
            }
        )

    probe = (
        asset_text("free-quench-model.js")
        + r"""
const editor = globalThis.MotionLabEditor;
process.stdout.write(JSON.stringify(JSON.parse(process.argv[1]).map((entry) => {
  const got = editor.applyBestSnap(entry.state, entry.moving, entry.threshold);
  return {
    groups: got.state.groups,
    x: got.state.squares.map((square) => square.x),
    y: got.state.squares.map((square) => square.y),
    target: got.result ? [got.result.target_kind, got.result.target_id] : null,
  };
})));
"""
    )
    completed = node(
        ["-e", probe, "--", json.dumps(cases)],
        return_completed_process=True,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    observed = cast(list[dict[str, object]], json.loads(completed.stdout))

    assert len(observed) == len(cases)
    for case, got in zip(cases, observed, strict=True):
        expected = cast(dict[str, object], case["expected"])
        assert got["target"] == expected["target"]
        assert got["groups"] == expected["groups"]
        assert cast(list[float], got["x"]) == pytest.approx(
            cast(list[float], expected["x"]), abs=1e-12
        )
        assert cast(list[float], got["y"]) == pytest.approx(
            cast(list[float], expected["y"]), abs=1e-12
        )


def test_browser_reducer_mirrors_the_python_snapping_toggle() -> None:
    probe = (
        asset_text("free-quench-model.js")
        + r"""
const editor = globalThis.MotionLabEditor;
const base = {
  side: 3,
  squares: [{square_id: 0, x: 0.5, y: 0.5, theta: 0}],
  groups: [[0]],
  snapping_enabled: true,
};
const off = editor.setSnapping(base, false);
process.stdout.write(JSON.stringify({
  off: off.snapping_enabled,
  sourceUntouched: base.snapping_enabled,
  back: editor.setSnapping(off, true).snapping_enabled,
}));
"""
    )
    completed = node(
        ["-e", probe], return_completed_process=True, capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr
    result = cast(dict[str, bool], json.loads(completed.stdout))

    reference = EditorState.with_singletons(
        side=3.0, squares=(EditorSquare(square_id=0, x=0.5, y=0.5, theta=0.0),)
    )
    assert result["off"] is set_snapping(reference, enabled=False).snapping_enabled
    assert result["back"] is True
    assert result["sourceUntouched"] is True


def test_live_profile_declares_the_palette_size_the_browser_indexes_into() -> None:
    """The browser wraps square colours modulo a count it cannot otherwise know.

    A hard-coded modulus silently produces an undefined CSS variable, and a square with
    no fill, the moment the palette or the square cap changes.
    """
    html = render_general_motion_lab(n=5, seed=7, side=3.2)

    assert f'data-palette-size="{len(SQUARE_FILL_PALETTE)}"' in html
    assert "% 20" not in asset_text("free-quench.js")
    assert len(SQUARE_FILL_PALETTE) >= MAX_INTERACTIVE_SQUARES
