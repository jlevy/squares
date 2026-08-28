"""Adapt the retained exact ``n = 5`` manifest to the shared scenario contract."""

from __future__ import annotations

from typing import cast

from sqpack.motion_lab.contracts import (
    Capability,
    Evidence,
    EvidenceStatus,
    FrameKind,
    FrameOverlay,
    OverlayKind,
    Phase,
    PoseFrame,
    ScenarioDefinition,
    ScenarioRunner,
    SquarePose,
)

EXACT_N5_SCENARIO_ID = "exact-n5"
EXACT_N5_MANIFEST_CONTRACT = "packing.squares:MotionLab/v1"
EXACT_N5_SCHEMA_VERSION = 1


def _mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise TypeError(f"{label} must be an object with string keys")
    return cast(dict[str, object], value)


def _list(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise TypeError(f"{label} must be an array")
    return cast(list[object], value)


def _decimal(value: object, label: str) -> float:
    record = _mapping(value, label)
    decimal = record.get("decimal")
    if not isinstance(decimal, str):
        raise TypeError(f"{label} decimal projection must be a string")
    return float(decimal)


def _square_pose(value: object) -> SquarePose:
    square = _mapping(value, "exact n=5 square")
    square_id = square.get("id")
    if isinstance(square_id, bool) or not isinstance(square_id, int):
        raise TypeError("exact n=5 square ID must be an integer")
    centre = _mapping(square.get("centre_start"), "exact n=5 square centre")
    orientation = _mapping(square.get("orientation"), "exact n=5 square orientation")
    radians = orientation.get("radians", "0")
    if not isinstance(radians, str):
        raise TypeError("exact n=5 fixed-angle projection must be a string")
    return SquarePose(
        square_id=square_id,
        x=_decimal(centre.get("x"), "exact n=5 square x"),
        y=_decimal(centre.get("y"), "exact n=5 square y"),
        theta=float(radians),
        palette_index=square_id,
    )


def _contact_overlays(scene: dict[str, object]) -> tuple[FrameOverlay, ...]:
    contacts = _mapping(scene.get("contacts"), "exact n=5 contacts")
    pairs = _list(contacts.get("base"), "exact n=5 base contacts")
    overlays = []
    for value in pairs:
        pair = _list(value, "exact n=5 contact pair")
        if len(pair) != 2 or any(
            isinstance(square_id, bool) or not isinstance(square_id, int) for square_id in pair
        ):
            raise TypeError("exact n=5 contact pair must contain two integer IDs")
        square_ids = tuple(sorted(cast(list[int], pair)))
        overlays.append(
            FrameOverlay(
                kind=OverlayKind.CONTACT,
                square_ids=square_ids,
                label=f"source-backed contact {square_ids[0]}-{square_ids[1]}",
            )
        )
    return tuple(overlays)


def exact_n5_scenario(manifest: object) -> ScenarioDefinition:
    """Normalize the exact manifest without importing its case-bound generators."""
    record = _mapping(manifest, "exact n=5 manifest")
    schema_version = record.get("schema_version")
    if (
        record.get("contract") != EXACT_N5_MANIFEST_CONTRACT
        or isinstance(schema_version, bool)
        or schema_version != EXACT_N5_SCHEMA_VERSION
    ):
        raise ValueError("unsupported exact n=5 motion manifest")
    default_scene = record.get("default_scene")
    if not isinstance(default_scene, str):
        raise TypeError("exact n=5 default scene must be a string")
    scenes = [
        _mapping(value, "exact n=5 scene")
        for value in _list(record.get("scenes"), "exact n=5 scenes")
    ]
    try:
        scene = next(value for value in scenes if value.get("id") == default_scene)
    except StopIteration as error:
        raise ValueError("exact n=5 default scene is missing") from error
    evidence = _mapping(scene.get("evidence"), "exact n=5 evidence")
    claim = evidence.get("claim")
    source = evidence.get("source_record")
    if not isinstance(claim, str) or not isinstance(source, str):
        raise TypeError("exact n=5 evidence claim and source must be strings")
    title = record.get("title")
    if not isinstance(title, str):
        raise TypeError("exact n=5 manifest title must be a string")
    frame = PoseFrame(
        scenario_id=EXACT_N5_SCENARIO_ID,
        frame_kind=FrameKind.EXACT_PATH,
        container_side=_decimal(scene.get("container_side"), "exact n=5 container side"),
        squares=tuple(
            _square_pose(value) for value in _list(scene.get("squares"), "exact n=5 squares")
        ),
        phase=Phase.ANALYTIC_PATH,
        evidence=Evidence(
            status=EvidenceStatus.EXACT_CERTIFIED_PATH,
            claim=claim,
            source=source,
        ),
        overlays=_contact_overlays(scene),
    )
    return ScenarioDefinition(
        scenario_id=EXACT_N5_SCENARIO_ID,
        title=title,
        runner=ScenarioRunner.ANALYTIC,
        capabilities=(Capability.PLAYBACK, Capability.SCRUB),
        initial_frame=frame,
    )
