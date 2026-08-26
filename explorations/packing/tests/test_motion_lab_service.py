"""Loopback service, free-quench scenario, and deterministic replay contracts."""

from __future__ import annotations

import http.client
import json
import threading
from pathlib import Path
from typing import cast

import pytest

from cases.campaign_smoke.basin_events import deterministic_start as campaign_start
from devtools.serve_packing_motion_lab import (
    LOOPBACK_HOST,
    build_quench_trace,
    create_server,
    replay_trace,
    save_trace,
)
from sqpack.motion_lab.contracts import QuenchRequest, canonical_json
from sqpack.motion_lab.scenarios.free_quench import (
    deterministic_editor_start,
    free_quench_scenario,
)
from sqpack.verify import corners_from_poses, float_sign, verify_packing

TEST_TIME_BUDGET_SECONDS = 10.0
ROOT = Path(__file__).parents[1]
KNOWN_REQUEST = ROOT / "atlas/rendering/free-quench-n1-request.json"
KNOWN_TRACE = ROOT / "atlas/rendering/free-quench-n1-trace.json"


def _request() -> QuenchRequest:
    return QuenchRequest(
        side=1.6,
        x=(0.5,),
        y=(0.5,),
        theta=(0.0,),
        max_sweeps=1,
        time_budget=TEST_TIME_BUDGET_SECONDS,
    )


def test_free_quench_seed_matches_the_declared_campaign_proposer() -> None:
    state = deterministic_editor_start(n=5, seed=7, side=3.2)
    expected_x, expected_y, expected_theta = campaign_start(5, 7, 3.2)
    scenario = free_quench_scenario(n=5, seed=7, side=3.2)

    assert [square.x for square in state.squares] == expected_x
    assert [square.y for square in state.squares] == expected_y
    assert [square.theta for square in state.squares] == expected_theta
    assert scenario.scenario_id == "free-quench"
    assert scenario.initial_frame.container_side == 3.2
    capabilities = cast(list[str], scenario.to_record()["capabilities"])
    assert "run-quench" in capabilities


def test_trace_save_and_replay_are_byte_deterministic(tmp_path: Path) -> None:
    request = _request()
    first = build_quench_trace(request.to_record())
    second = build_quench_trace(request.to_record())
    output = tmp_path / "trace.json"

    save_trace(output, first)
    replayed = replay_trace(output)

    assert canonical_json(first) == canonical_json(second)
    assert output.read_text(encoding="utf-8") == canonical_json(first)
    assert replayed == first


def test_retained_trace_replays_and_its_endpoint_passes_the_independent_oracle() -> None:
    request = json.loads(KNOWN_REQUEST.read_text(encoding="utf-8"))
    trace = build_quench_trace(request)
    retained = KNOWN_TRACE.read_text(encoding="utf-8")

    assert retained == canonical_json(trace)
    assert replay_trace(KNOWN_TRACE) == trace
    assert len(trace.events) == 144
    assert trace.result.side == pytest.approx(1.138209210409642, abs=1e-15)
    assert trace.result.theta == pytest.approx((0.15000000000000052,), abs=1e-15)
    report = verify_packing(
        corners_from_poses(trace.result.x, trace.result.y, trace.result.theta),
        trace.result.side,
        float_sign(1e-9),
    )
    assert report.valid, report


def test_http_service_binds_loopback_and_returns_typed_success_and_failure() -> None:
    server = create_server(port=0)
    assert cast(tuple[str, int], server.server_address)[0] == LOOPBACK_HOST
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = cast(tuple[str, int], server.server_address)[1]
    connection = http.client.HTTPConnection(LOOPBACK_HOST, port, timeout=15)
    try:
        body = json.dumps(_request().to_record())
        connection.request(
            "POST",
            "/api/quench",
            body=body,
            headers={"Content-Type": "application/json"},
        )
        response = connection.getresponse()
        success = json.loads(response.read())
        assert response.status == 200
        assert success["contract"] == "packing.squares:QuenchTrace/v1"
        assert success["events"][0]["event_kind"] == "setup-released"

        connection.request(
            "POST",
            "/api/quench",
            body=json.dumps(_request().to_record() | {"groups": [[0]]}),
            headers={"Content-Type": "application/json"},
        )
        response = connection.getresponse()
        failure = json.loads(response.read())
        assert response.status == 400
        assert failure["contract"] == "packing.squares:MotionLabError/v1"
        assert failure["error"]["code"] == "invalid-request"
        assert "groups" in failure["error"]["message"]
    finally:
        connection.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
