from __future__ import annotations

import copy
import json
import subprocess
from collections.abc import Callable
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest

from cases.n11_five_dot_cover.independent_union import Direction, FrozenInput
from devtools.owner_footprints import full_owner_direction_manifest, owner_branch_manifest
from devtools.wall_owner_containment import WallClass, WallInput, physical_corner_maps
from devtools.wall_owner_escape_compatibility import ClassCompatibility, evaluate_class
from devtools.wall_owner_footprints import (
    OwnerFrameFootprint,
    centre_set_dimension,
    closed_centre_set,
    retained_owner_frames,
    support_rectangle,
)
from devtools.wall_owner_parent_compatibility import (
    GLOBAL_PARENT_RULE,
    ParentClassCompatibility,
    ParentCompatibilityError,
    ResidualParentCheck,
    check_residual_parent_centre,
    evaluate_parent_class,
)
from devtools.wall_owner_parent_experiment import (
    IMPLEMENTATION_PATHS,
    ParentExperimentError,
    ParentExperimentEvaluation,
    ParentOwnerComparison,
    authority_record,
    execute_parent_experiment,
    load_parent_result,
    parent_result_record,
    replay_parent_result_record,
    retained_parent_input_pins,
    run_parent_target,
    run_parent_worker,
    settings_record,
    sources_record,
    supervise_parent_worker,
    validate_result_document,
    write_result_document,
)
from devtools.wall_owner_parent_inputs import (
    ParentAdapterInputs,
    ParentInputPins,
    ProducedReceiptPin,
    ReceiptPin,
    bind_parent_adapter_inputs,
    load_parent_adapter_inputs,
    validate_physical_corner_maps,
)
from devtools.wall_owner_selected_cover import (
    DirectionResult,
    SelectedCoverEvidence,
    SelectedEscape,
)
from devtools.wall_owner_sixth_site_screen import SixDotEscapeEvidence

CHECKOUT = "a" * 40
ENDPOINT_BLOB = "b" * 40
WALL_BLOB = "c" * 40
SELECTED_BLOB = "d" * 40
STRICT_BLOB = "e" * 40
WALL_REVISION = "1" * 40
SELECTED_REVISION = "2" * 40
STRICT_REVISION = "3" * 40
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def _pins() -> ParentInputPins:
    return ParentInputPins(
        REPOSITORY_ROOT,
        CHECKOUT,
        ReceiptPin("synthetic/endpoint.json", ENDPOINT_BLOB),
        ProducedReceiptPin("synthetic/wall.json", WALL_BLOB, WALL_REVISION),
        ProducedReceiptPin(
            "synthetic/selected.json",
            SELECTED_BLOB,
            SELECTED_REVISION,
        ),
        ProducedReceiptPin("synthetic/strict.json", STRICT_BLOB, STRICT_REVISION),
    )


def _synthetic_inputs():
    manifest = full_owner_direction_manifest()
    branch = owner_branch_manifest(manifest)
    directions = tuple(
        Direction(
            item.direction.label,
            item.direction.ux,
            item.direction.uy,
        )
        for item in manifest.orientations
    )
    polygon = (
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
    )
    source = FrozenInput(
        "synthetic/endpoint.json",
        CHECKOUT,
        ENDPOINT_BLOB,
        Fraction(96, 25),
        Fraction(9977, 10000),
        Fraction(207107, 500000),
        180,
        (polygon,) * 4,
        ((Fraction(1), Fraction(1)),) * 5,
        Fraction(1),
        Fraction(5),
        directions,
    )
    wall_classes = []
    for owner_class in branch.classes:
        frames = tuple(
            OwnerFrameFootprint(frame, (), -1, None, None, None, "empty")
            for frame in retained_owner_frames(owner_class, manifest)
        )
        wall_classes.append(
            WallClass(owner_class.class_id, polygon, "possible", polygon, frames)
        )
    wall = WallInput(
        "synthetic/wall.json",
        CHECKOUT,
        WALL_BLOB,
        WALL_REVISION,
        tuple(wall_classes),
    )
    selected_direction = DirectionResult(
        0,
        directions[0].label,
        Fraction(1),
        Fraction(0),
        Fraction(1),
        1,
    )
    selected = SelectedCoverEvidence(
        "synthetic/selected.json",
        CHECKOUT,
        SELECTED_BLOB,
        SELECTED_REVISION,
        selected_direction,
        SelectedEscape(0, directions[0].label, (Fraction(1), Fraction(1))),
        (polygon,) * 4,
    )
    strict_direction = DirectionResult(
        6,
        directions[6].label,
        Fraction(1),
        Fraction(0),
        Fraction(1),
        1,
    )
    strict = SixDotEscapeEvidence(
        "synthetic/strict.json",
        CHECKOUT,
        STRICT_BLOB,
        STRICT_REVISION,
        strict_direction,
        SelectedEscape(6, directions[6].label, (Fraction(2), Fraction(2))),
    )
    return source, wall, selected, strict, manifest


def _bind(
    *,
    pins: ParentInputPins | None = None,
    source: FrozenInput | None = None,
    wall: WallInput | None = None,
    selected: SelectedCoverEvidence | None = None,
    strict: SixDotEscapeEvidence | None = None,
    manifest=None,
    maps=None,
) -> ParentAdapterInputs:
    default_source, default_wall, default_selected, default_strict, default_manifest = (
        _synthetic_inputs()
    )
    return bind_parent_adapter_inputs(
        pins or _pins(),
        source=source or default_source,
        wall=wall or default_wall,
        selected_cover=selected or default_selected,
        strict_escape=strict or default_strict,
        owner_manifest=manifest or default_manifest,
        maps=maps or physical_corner_maps(),
    )


def _refused(action: Callable[[], object], message: str) -> None:
    try:
        action()
    except ValueError:
        return
    raise AssertionError(message)


def _one_frame_parent_inputs() -> ParentAdapterInputs:
    inputs = _bind()
    owner = inputs.selected_owners[3]
    identity = owner.expected_frames[0]
    centre_set = closed_centre_set(
        owner.owner_class.mark,
        identity.ray,
        outer_side=GLOBAL_PARENT_RULE.outer_side,
        half=GLOBAL_PARENT_RULE.core_side / 2,
    )
    rectangle, support_r, support_jr = support_rectangle(
        centre_set,
        identity.ray,
        half=GLOBAL_PARENT_RULE.core_side / 2,
    )
    frame = OwnerFrameFootprint(
        identity,
        centre_set,
        centre_set_dimension(centre_set),
        support_r,
        support_jr,
        rectangle,
        "allowed",
    )
    bound_owner = replace(
        owner,
        wall_class=replace(owner.wall_class, frames=(frame,)),
        expected_frames=(identity,),
    )
    strict = replace(
        inputs.strict_escape,
        escape=replace(
            inputs.strict_escape.escape,
            centre=(Fraction(2), Fraction(2)),
        ),
    )
    return replace(
        inputs,
        selected_owners=(*inputs.selected_owners[:3], bound_owner),
        strict_escape=strict,
    )


def test_binds_complete_target_blind_authority() -> None:
    result = _bind()
    assert result.checkout_revision == CHECKOUT
    assert len(result.owner_manifest.orientations) == 361
    assert len(result.residual_manifest) == 361
    assert tuple(row.index for row in result.residual_manifest) == tuple(range(361))
    assert all(row.sources for row in result.residual_manifest)
    assert [row.corner for row in result.selected_owners] == ["BL", "BR", "TL", "TR"]
    assert [row.class_index for row in result.selected_owners] == [0, 0, 0, 7]
    assert all(len(row.expected_frames) == 181 for row in result.selected_owners)
    assert result.selected_residual.index == 6
    assert result.selected_residual.sources


def test_refuses_changed_or_omitted_git_provenance() -> None:
    source, wall, selected, strict, manifest = _synthetic_inputs()
    _refused(
        lambda: _bind(source=replace(source, git_commit="f" * 40)),
        "changed checkout revision passed",
    )
    _refused(
        lambda: _bind(strict=replace(strict, implementation_revision="")),
        "omitted strict-escape producer revision passed",
    )
    pins = replace(
        _pins(),
        selected_cover=replace(_pins().selected_cover, producer_revision="4" * 40),
    )
    _refused(
        lambda: bind_parent_adapter_inputs(
            pins,
            source=source,
            wall=wall,
            selected_cover=selected,
            strict_escape=strict,
            owner_manifest=manifest,
            maps=physical_corner_maps(),
        ),
        "changed selected-cover producer revision passed",
    )


def test_refuses_incomplete_frame_and_residual_source_manifests() -> None:
    source, wall, _, _, manifest = _synthetic_inputs()
    bad_class = replace(wall.classes[0], frames=wall.classes[0].frames[:-1])
    bad_wall = replace(wall, classes=(bad_class, *wall.classes[1:]))
    _refused(lambda: _bind(wall=bad_wall), "partial selected frame inventory passed")

    orientation = replace(manifest.orientations[6], sources=())
    bad_manifest = replace(
        manifest,
        orientations=(*manifest.orientations[:6], orientation, *manifest.orientations[7:]),
    )
    _refused(
        lambda: _bind(manifest=bad_manifest),
        "omitted residual orientation provenance passed",
    )
    bad_directions = list(source.directions)
    bad_directions[6] = replace(bad_directions[6], label="changed")
    _refused(
        lambda: _bind(source=replace(source, directions=tuple(bad_directions))),
        "changed endpoint residual orientation passed",
    )


def test_refuses_wrong_physical_map_or_local_class() -> None:
    maps = physical_corner_maps()
    wrong_map = replace(maps[1], tx=Fraction(0))
    _refused(
        lambda: validate_physical_corner_maps((maps[0], wrong_map, maps[2], maps[3])),
        "wrong physical map passed",
    )

    _, wall, _, _, _ = _synthetic_inputs()
    wrong_class = replace(wall.classes[0], class_id="bottom-left:m2:j0")
    _refused(
        lambda: _bind(wall=replace(wall, classes=(wrong_class, *wall.classes[1:]))),
        "changed selected local-class identity passed",
    )


def test_loader_wrapper_connects_all_receipts_and_strict_replays() -> None:
    source, wall, selected, strict, manifest = _synthetic_inputs()
    augmented = replace(source, dots=(*source.dots, selected.escape.centre))
    with (
        patch(
            "devtools.wall_owner_parent_inputs.load_frozen_input",
            return_value=source,
        ) as endpoint,
        patch(
            "devtools.wall_owner_parent_inputs.load_wall_input",
            return_value=wall,
        ) as wall_loader,
        patch(
            "devtools.wall_owner_parent_inputs.load_selected_cover_evidence",
            return_value=selected,
        ) as selected_loader,
        patch(
            "devtools.wall_owner_parent_inputs.load_six_dot_escape_evidence",
            return_value=strict,
        ) as strict_loader,
        patch(
            "devtools.wall_owner_parent_inputs.replay_selected_cover_evidence"
        ) as selected_replay,
        patch(
            "devtools.wall_owner_parent_inputs.augment_with_selected_escape",
            return_value=augmented,
        ),
        patch("devtools.wall_owner_parent_inputs.replay_six_dot_escape") as strict_replay,
        patch(
            "devtools.wall_owner_parent_inputs.full_owner_direction_manifest",
            return_value=manifest,
        ),
    ):
        result = load_parent_adapter_inputs(_pins(), replay_deadline=123.0)

    assert result.selected_residual.index == 6
    endpoint.assert_called_once_with(
        REPOSITORY_ROOT / "synthetic/endpoint.json",
        ENDPOINT_BLOB,
    )
    wall_loader.assert_called_once_with(
        REPOSITORY_ROOT / "synthetic/wall.json",
        WALL_BLOB,
        expected_source=WALL_REVISION,
    )
    selected_loader.assert_called_once_with(
        REPOSITORY_ROOT / "synthetic/selected.json",
        SELECTED_BLOB,
        expected_source=SELECTED_REVISION,
        source=source,
        wall=wall,
    )
    strict_loader.assert_called_once_with(
        REPOSITORY_ROOT / "synthetic/strict.json",
        STRICT_BLOB,
        expected_source=STRICT_REVISION,
        source=source,
        wall=wall,
        selected=selected,
    )
    selected_replay.assert_called_once_with(selected, source=source, deadline=123.0)
    strict_replay.assert_called_once_with(strict.escape, augmented, deadline=123.0)


def test_pin_paths_and_source_revisions_are_mandatory() -> None:
    pins = _pins()
    _refused(
        lambda: _bind(pins=replace(pins, endpoint=replace(pins.endpoint, path=""))),
        "omitted receipt path passed",
    )
    _refused(
        lambda: _bind(
            pins=replace(
                pins,
                wall=replace(pins.wall, producer_revision=""),
            )
        ),
        "omitted wall constructor revision passed",
    )
    try:
        _bind(pins=replace(pins, checkout_revision=""))
    except ParentCompatibilityError:
        return
    raise AssertionError("omitted checkout revision passed")


def test_explicit_repository_root_controls_resolution_from_both_working_directories(
    monkeypatch,
) -> None:
    pins = _pins()

    def inspect_first_loader(path: Path, blob: str) -> None:
        assert blob == ENDPOINT_BLOB
        assert path == REPOSITORY_ROOT / pins.endpoint.path
        raise RuntimeError("synthetic path inspected")

    for working_directory in (REPOSITORY_ROOT, REPOSITORY_ROOT / "packing"):
        monkeypatch.chdir(working_directory)
        with patch(
            "devtools.wall_owner_parent_inputs.load_frozen_input",
            side_effect=inspect_first_loader,
        ):
            try:
                load_parent_adapter_inputs(pins, replay_deadline=1.0)
            except RuntimeError as error:
                assert str(error) == "synthetic path inspected"
            else:
                raise AssertionError("synthetic path inspection did not run")


def test_result_authority_is_complete_and_independent_of_processed_rows() -> None:
    inputs = _bind()
    authority = authority_record(inputs)
    residual = cast(list[object], authority["residual_manifest"])
    owners = cast(list[dict[str, object]], authority["selected_owners"])

    assert len(residual) == 361
    assert authority["selected_residual_index"] == 6
    assert [row["corner"] for row in owners] == ["BL", "BR", "TL", "TR"]
    assert [row["class_index"] for row in owners] == [0, 0, 0, 7]
    assert all(len(cast(list[object], row["expected_frames"])) == 181 for row in owners)
    assert [cast(dict[str, object], row["physical_map"])["name"] for row in owners] == [
        "I",
        "H",
        "V",
        "R",
    ]


def test_result_sources_and_settings_retain_every_frozen_pin() -> None:
    inputs = _bind()
    sources = sources_record(inputs, implementation_revision=CHECKOUT)
    settings = settings_record()
    retained = retained_parent_input_pins(REPOSITORY_ROOT, CHECKOUT)

    assert sources["endpoint"] == {
        "path": "synthetic/endpoint.json",
        "git_commit": CHECKOUT,
        "git_blob": ENDPOINT_BLOB,
        "producer_revision": None,
    }
    assert sources["strict_escape"] == {
        "path": "synthetic/strict.json",
        "git_commit": CHECKOUT,
        "git_blob": STRICT_BLOB,
        "producer_revision": STRICT_REVISION,
    }
    assert cast(dict[str, object], sources["implementation"])["dependency_paths"] == list(
        IMPLEMENTATION_PATHS
    )
    assert {
        "packing/devtools/wall_owner_fixed_pattern.py",
        "packing/src/sqpack/fractional/generate.py",
        "packing/src/sqpack/fractional/model.py",
    }.issubset(IMPLEMENTATION_PATHS)
    assert settings["candidate"] == [0, 0, 0, 7]
    assert settings["physical_owner_order"] == ["TR", "BL", "BR", "TL"]
    assert retained.endpoint.git_blob == "cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19"
    assert retained.wall.producer_revision == "915758898a97c92793f51e62b7a6b17f846895ca"


def test_scientific_clock_starts_after_source_replay_and_checkpoints_partial(
    tmp_path: Path,
) -> None:
    bound_inputs = _bind()
    events: list[str] = []
    published: list[dict[str, object]] = []
    times = iter((10.0, 20.0, 21.0, 22.0, 25.0, 26.0))

    def clock() -> float:
        return next(times)

    def loader(pins: ParentInputPins, *, replay_deadline: float) -> ParentAdapterInputs:
        del pins
        events.append("load")
        assert replay_deadline == 130.0
        return bound_inputs

    def target(
        inputs: ParentAdapterInputs,
        *,
        deadline: float,
        clock: Callable[[], float],
        checkpoint: Callable[[ParentExperimentEvaluation], None],
    ) -> ParentExperimentEvaluation:
        del clock, checkpoint
        events.append("target")
        assert inputs is bound_inputs
        assert events == ["load", "target"]
        assert deadline == 110.0
        residual = inputs.selected_residual
        return ParentExperimentEvaluation(
            "complete",
            "residual-self-excluded",
            ResidualParentCheck(
                "outside-parent-box",
                inputs.strict_escape.escape.centre,
                residual.ray,
                residual.sources,
                Fraction(1, 2),
                (),
            ),
            (),
        )

    def publisher(_path: Path, document: dict[str, object]) -> None:
        published.append(document)

    document = execute_parent_experiment(
        _pins(),
        implementation_revision=CHECKOUT,
        output=tmp_path / "result.json",
        clock=clock,
        loader=loader,
        target=target,
        publisher=publisher,
    )

    assert [row["status"] for row in published] == ["partial", "complete"]
    assert published[0]["authority"] == authority_record(bound_inputs)
    assert document["clocks"] == {
        "source_replay_seconds": 10.0,
        "scientific_seconds": 5.0,
        "process_seconds": 15.0,
        "scientific_started": True,
    }


def test_process_bound_shortens_the_scientific_allowance_after_source_replay(
    tmp_path: Path,
) -> None:
    bound_inputs = _bind()
    deadlines: list[float] = []
    times = iter((10.0, 50.0, 51.0, 52.0, 60.0, 61.0))

    def target(
        inputs: ParentAdapterInputs,
        *,
        deadline: float,
        clock: Callable[[], float],
        checkpoint: Callable[[ParentExperimentEvaluation], None],
    ) -> ParentExperimentEvaluation:
        del clock, checkpoint
        deadlines.append(deadline)
        residual = inputs.selected_residual
        return ParentExperimentEvaluation(
            "complete",
            "residual-self-excluded",
            ResidualParentCheck(
                "outside-parent-box",
                inputs.strict_escape.escape.centre,
                residual.ray,
                residual.sources,
                Fraction(1, 2),
                (),
            ),
            (),
        )

    def loader(
        pins: ParentInputPins,
        *,
        replay_deadline: float,
    ) -> ParentAdapterInputs:
        del pins
        assert replay_deadline == 130.0
        return bound_inputs

    execute_parent_experiment(
        _pins(),
        implementation_revision=CHECKOUT,
        output=tmp_path / "result.json",
        clock=times.__next__,
        loader=loader,
        target=target,
        publisher=lambda _path, _document: None,
    )

    assert deadlines == [130.0]


def test_scientific_overrun_cannot_publish_or_validate_as_complete(
    tmp_path: Path,
) -> None:
    inputs = _bind()
    times = iter((0.0, 1.0, 2.0, 3.0, 92.0, 93.0))

    def loader(
        pins: ParentInputPins,
        *,
        replay_deadline: float,
    ) -> ParentAdapterInputs:
        del pins
        assert replay_deadline == 120.0
        return inputs

    def target(
        inputs: ParentAdapterInputs,
        *,
        deadline: float,
        clock: Callable[[], float],
        checkpoint: Callable[[ParentExperimentEvaluation], None],
    ) -> ParentExperimentEvaluation:
        del clock, checkpoint
        assert deadline == 91.0
        residual = inputs.selected_residual
        return ParentExperimentEvaluation(
            "complete",
            "residual-self-excluded",
            ResidualParentCheck(
                "outside-parent-box",
                inputs.strict_escape.escape.centre,
                residual.ray,
                residual.sources,
                Fraction(1, 2),
                (),
            ),
            (),
        )

    document = execute_parent_experiment(
        _pins(),
        implementation_revision=CHECKOUT,
        output=tmp_path / "overrun.json",
        clock=times.__next__,
        loader=loader,
        target=target,
    )

    assert document["status"] == "partial"
    assert document["error"] == "scientific deadline reached before result publication"
    changed = copy.deepcopy(document)
    changed["status"] = "complete"
    changed["outcome"] = "residual-self-excluded"
    changed["error"] = None
    clocks = cast(dict[str, object], changed["clocks"])
    clocks["scientific_seconds"] = 90.0
    clocks["process_seconds"] = 91.0
    with pytest.raises(ParentExperimentError, match="scientific allowance"):
        validate_result_document(changed)


def test_final_publication_time_can_only_leave_a_partial_artifact(tmp_path: Path) -> None:
    inputs = _bind()
    state = {"now": 0.0}
    publications: list[str] = []
    output = tmp_path / "slow-final-publication.json"

    def clock() -> float:
        return state["now"]

    def loader(
        pins: ParentInputPins,
        *,
        replay_deadline: float,
    ) -> ParentAdapterInputs:
        del pins
        assert replay_deadline == 120.0
        state["now"] = 1.0
        return inputs

    def target(
        inputs: ParentAdapterInputs,
        *,
        deadline: float,
        clock: Callable[[], float],
        checkpoint: Callable[[ParentExperimentEvaluation], None],
    ) -> ParentExperimentEvaluation:
        del clock, checkpoint
        assert deadline == 91.0
        residual = inputs.selected_residual
        return ParentExperimentEvaluation(
            "complete",
            "residual-self-excluded",
            ResidualParentCheck(
                "outside-parent-box",
                inputs.strict_escape.escape.centre,
                residual.ray,
                residual.sources,
                Fraction(1, 2),
                (),
            ),
            (),
        )

    def publisher(path: Path, document: dict[str, object]) -> None:
        publications.append(cast(str, document["status"]))
        write_result_document(path, document)
        if document["status"] == "complete":
            state["now"] = 200.0

    document = execute_parent_experiment(
        _pins(),
        implementation_revision=CHECKOUT,
        output=output,
        clock=clock,
        loader=loader,
        target=target,
        publisher=publisher,
    )

    assert publications == ["partial", "complete", "partial"]
    assert document["status"] == "partial"
    assert document["clocks"] == {
        "source_replay_seconds": 1.0,
        "scientific_seconds": 199.0,
        "process_seconds": 200.0,
        "scientific_started": True,
    }
    assert json.loads(output.read_text(encoding="utf-8"))["status"] == "partial"


def test_slow_initial_publication_prevents_target_entry(tmp_path: Path) -> None:
    inputs = _bind()
    state = {"now": 0.0}
    publications: list[str] = []

    def clock() -> float:
        return state["now"]

    def loader(
        pins: ParentInputPins,
        *,
        replay_deadline: float,
    ) -> ParentAdapterInputs:
        del pins
        assert replay_deadline == 120.0
        state["now"] = 1.0
        return inputs

    def publisher(_path: Path, document: dict[str, object]) -> None:
        publications.append(cast(str, document["status"]))
        state["now"] = 200.0

    def forbidden_target(
        inputs: ParentAdapterInputs,
        *,
        deadline: float,
        clock: Callable[[], float],
        checkpoint: Callable[[ParentExperimentEvaluation], None],
    ) -> ParentExperimentEvaluation:
        del inputs, deadline, clock, checkpoint
        raise AssertionError("target entered after initial publication consumed the budget")

    document = execute_parent_experiment(
        _pins(),
        implementation_revision=CHECKOUT,
        output=tmp_path / "slow-initial-publication.json",
        clock=clock,
        loader=loader,
        target=forbidden_target,
        publisher=publisher,
    )

    assert publications == ["partial", "partial"]
    assert document["status"] == "partial"
    assert "deadline" in cast(str, document["error"])


def test_source_refusal_writes_a_schema_valid_invalid_result(tmp_path: Path) -> None:
    output = tmp_path / "result.json"
    calls: list[str] = []
    times = iter((10.0, 15.0))

    def refused_loader(
        pins: ParentInputPins,
        *,
        replay_deadline: float,
    ) -> ParentAdapterInputs:
        del pins
        assert replay_deadline == 130.0
        raise ParentCompatibilityError("synthetic source refusal")

    def forbidden_target(
        inputs: ParentAdapterInputs,
        *,
        deadline: float,
        clock: Callable[[], float],
        checkpoint: Callable[[ParentExperimentEvaluation], None],
    ) -> ParentExperimentEvaluation:
        del inputs, deadline, clock, checkpoint
        calls.append("target")
        raise AssertionError("target ran after a source refusal")

    document = execute_parent_experiment(
        _pins(),
        implementation_revision=CHECKOUT,
        output=output,
        clock=times.__next__,
        loader=refused_loader,
        target=forbidden_target,
    )

    assert not calls
    assert document["status"] == "invalid"
    assert document["clocks"] == {
        "source_replay_seconds": 5.0,
        "scientific_seconds": 0.0,
        "process_seconds": 5.0,
        "scientific_started": False,
    }
    assert json.loads(output.read_text(encoding="utf-8")) == document


def test_target_attributes_gain_only_after_a_compatible_b_only_control() -> None:
    inputs = _bind()
    checkpoints: list[ParentExperimentEvaluation] = []
    owner = inputs.selected_owners[3]
    b_only = ClassCompatibility(
        owner.corner_index,
        owner.class_index,
        owner.physical_map,
        "compatible",
        len(owner.expected_frames),
        (),
        Fraction(1, 7),
        None,
    )
    parent = ParentClassCompatibility(
        "incompatible",
        len(owner.expected_frames),
        (),
        (),
        Fraction(0),
        Fraction(0),
    )
    with (
        patch(
            "devtools.wall_owner_parent_experiment.check_residual_parent_centre",
            return_value=ResidualParentCheck(
                "inside-parent-box",
                inputs.strict_escape.escape.centre,
                inputs.selected_residual.ray,
                inputs.selected_residual.sources,
                Fraction(1, 2),
                (),
            ),
        ),
        patch(
            "devtools.wall_owner_parent_experiment.evaluate_class",
            return_value=b_only,
        ) as control,
        patch(
            "devtools.wall_owner_parent_experiment.evaluate_parent_class",
            return_value=parent,
        ) as restricted,
    ):
        result = run_parent_target(
            inputs,
            deadline=100,
            clock=lambda: 0,
            checkpoint=checkpoints.append,
        )

    assert result.status == "complete"
    assert result.outcome == "owner-domain-gain"
    assert result.comparisons[0].owner.corner == "TR"
    assert result.comparisons[0].b_only is b_only
    assert result.comparisons[0].parent_restricted is parent
    control.assert_called_once()
    restricted.assert_called_once()
    assert checkpoints[-1].comparisons[0].attribution == "owner-domain-gain"


def test_target_rechecks_deadline_after_owner_checkpoint_publication() -> None:
    inputs = _bind()
    state = {"now": 0.0}
    owner = inputs.selected_owners[3]
    b_only = ClassCompatibility(
        owner.corner_index,
        owner.class_index,
        owner.physical_map,
        "compatible",
        len(owner.expected_frames),
        (),
        Fraction(1, 7),
        None,
    )
    parent = ParentClassCompatibility(
        "incompatible",
        len(owner.expected_frames),
        (),
        (),
        Fraction(0),
        Fraction(0),
    )

    def checkpoint(evaluation: ParentExperimentEvaluation) -> None:
        if evaluation.comparisons:
            state["now"] = 2.0

    with (
        patch(
            "devtools.wall_owner_parent_experiment.check_residual_parent_centre",
            return_value=ResidualParentCheck(
                "inside-parent-box",
                inputs.strict_escape.escape.centre,
                inputs.selected_residual.ray,
                inputs.selected_residual.sources,
                Fraction(1, 2),
                (),
            ),
        ),
        patch(
            "devtools.wall_owner_parent_experiment.evaluate_class",
            return_value=b_only,
        ),
        patch(
            "devtools.wall_owner_parent_experiment.evaluate_parent_class",
            return_value=parent,
        ),
    ):
        result = run_parent_target(
            inputs,
            deadline=1.0,
            clock=lambda: state["now"],
            checkpoint=checkpoint,
        )

    assert result.status == "partial"
    assert result.outcome == "incomplete"
    assert len(result.comparisons) == 1
    assert result.comparisons[0].attribution == "owner-domain-gain"
    assert result.error == ("scientific deadline reached after owner checkpoint publication")


def test_residual_only_target_checks_deadline_before_complete_disposition() -> None:
    inputs = _bind()
    inputs = replace(
        inputs,
        strict_escape=replace(
            inputs.strict_escape,
            escape=replace(
                inputs.strict_escape.escape,
                centre=(Fraction(1, 10), Fraction(2)),
            ),
        ),
    )
    result = run_parent_target(
        inputs,
        deadline=100.0,
        clock=lambda: 100.0,
    )

    assert result.status == "partial"
    assert result.outcome == "incomplete"
    assert result.error == "scientific deadline reached before residual disposition"


def test_owner_target_rechecks_deadline_before_each_early_complete_disposition() -> None:
    inputs = _bind()
    owner = inputs.selected_owners[3]
    residual = ResidualParentCheck(
        "inside-parent-box",
        inputs.strict_escape.escape.centre,
        inputs.selected_residual.ray,
        inputs.selected_residual.sources,
        Fraction(1, 2),
        (),
    )
    compatible = ClassCompatibility(
        owner.corner_index,
        owner.class_index,
        owner.physical_map,
        "compatible",
        len(owner.expected_frames),
        (),
        Fraction(1, 7),
        None,
    )
    incompatible = replace(
        compatible,
        status="incompatible",
        observed_maximum_slack=Fraction(0),
        global_maximum_slack=Fraction(0),
    )
    parent = ParentClassCompatibility(
        "incompatible",
        len(owner.expected_frames),
        (),
        (),
        Fraction(0),
        Fraction(0),
    )
    cases = (
        (incompatible, parent, "B-only disposition"),
        (compatible, parent, "parent-restricted disposition"),
    )
    for b_only, parent_result, message in cases:
        times = iter((0.0, 100.0))
        with (
            patch(
                "devtools.wall_owner_parent_experiment.check_residual_parent_centre",
                return_value=residual,
            ),
            patch(
                "devtools.wall_owner_parent_experiment.evaluate_class",
                return_value=b_only,
            ),
            patch(
                "devtools.wall_owner_parent_experiment.evaluate_parent_class",
                return_value=parent_result,
            ),
        ):
            result = run_parent_target(
                inputs,
                deadline=100.0,
                clock=times.__next__,
            )

        assert result.status == "partial"
        assert result.comparisons == ()
        assert message in cast(str, result.error)


def test_readback_rebinds_authority_instead_of_trusting_saved_counts(
    tmp_path: Path,
) -> None:
    source, wall, selected, strict, manifest = _synthetic_inputs()
    strict = replace(
        strict,
        escape=replace(strict.escape, centre=(Fraction(1, 10), Fraction(2))),
    )
    inputs = _bind(
        source=source,
        wall=wall,
        selected=selected,
        strict=strict,
        manifest=manifest,
    )
    output = tmp_path / "result.json"
    times = iter((10.0, 20.0, 21.0, 22.0, 25.0, 25.5, 26.0, 27.0, 28.0))

    def loader(pins: ParentInputPins, *, replay_deadline: float) -> ParentAdapterInputs:
        del pins
        assert replay_deadline in (130.0, 999.0)
        return inputs

    execute_parent_experiment(
        _pins(),
        implementation_revision=CHECKOUT,
        output=output,
        clock=times.__next__,
        loader=loader,
    )
    document = load_parent_result(
        output,
        _pins(),
        replay_deadline=999.0,
        loader=loader,
        revision_validator=lambda _repository, revision: revision,
        clock=lambda: 0.0,
    )
    assert document["outcome"] == "residual-self-excluded"

    with pytest.raises(ParentExperimentError, match="readback exceeded"):
        load_parent_result(
            output,
            _pins(),
            replay_deadline=999.0,
            loader=loader,
            revision_validator=lambda _repository, revision: revision,
            clock=lambda: 999.0,
        )

    changed = cast(dict[str, object], json.loads(output.read_text()))
    authority = cast(dict[str, object], changed["authority"])
    manifest_rows = cast(list[object], authority["residual_manifest"])
    authority["residual_manifest"] = manifest_rows[:-1]
    summary = cast(dict[str, object], changed["summary"])
    summary["bound_residual_orientations"] = 360
    output.write_text(json.dumps(changed), encoding="utf-8")
    with pytest.raises(ParentExperimentError, match="authority"):
        load_parent_result(
            output,
            _pins(),
            replay_deadline=999.0,
            loader=loader,
            revision_validator=lambda _repository, revision: revision,
            clock=lambda: 0.0,
        )


def test_failed_readback_and_killed_worker_downgrade_unadmitted_complete_artifacts(
    tmp_path: Path,
) -> None:
    inputs = _bind()
    inputs = replace(
        inputs,
        strict_escape=replace(
            inputs.strict_escape,
            escape=replace(
                inputs.strict_escape.escape,
                centre=(Fraction(1, 10), Fraction(2)),
            ),
        ),
    )

    def loader(
        pins: ParentInputPins,
        *,
        replay_deadline: float,
    ) -> ParentAdapterInputs:
        del pins
        assert replay_deadline == 120.0
        return inputs

    output = tmp_path / "unread-complete.json"
    times = iter((0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0))
    complete = execute_parent_experiment(
        _pins(),
        implementation_revision=CHECKOUT,
        output=output,
        clock=times.__next__,
        loader=loader,
    )
    assert complete["status"] == "complete"

    readback_failure = tmp_path / "failed-readback.json"
    readback_failure.write_bytes(output.read_bytes())
    with (
        patch("devtools.wall_owner_parent_experiment.validate_parent_implementation_revision"),
        patch(
            "devtools.wall_owner_parent_experiment.retained_parent_input_pins",
            return_value=_pins(),
        ),
        patch(
            "devtools.wall_owner_parent_experiment.prepare_output_path",
            return_value=readback_failure,
        ),
        patch(
            "devtools.wall_owner_parent_experiment.execute_parent_experiment",
            return_value=complete,
        ),
        patch(
            "devtools.wall_owner_parent_experiment.load_parent_result",
            side_effect=ParentExperimentError("synthetic readback deadline"),
        ),
        patch(
            "devtools.wall_owner_parent_experiment.time.perf_counter",
            side_effect=(0.0, 10.0),
        ),
    ):
        worker_status = run_parent_worker(
            REPOSITORY_ROOT,
            CHECKOUT,
            readback_failure,
        )

    assert worker_status == 2
    downgraded = cast(
        dict[str, object],
        json.loads(readback_failure.read_text(encoding="utf-8")),
    )
    validate_result_document(downgraded)
    assert downgraded["status"] == "partial"
    assert downgraded["sources"] == complete["sources"]
    assert downgraded["residual_check"] == complete["residual_check"]
    assert downgraded["error"] == ("independent readback refused: synthetic readback deadline")

    class Process:
        def __init__(self) -> None:
            self.waits = 0

        def wait(self, timeout: float | None = None) -> int:
            self.waits += 1
            if self.waits == 1:
                raise subprocess.TimeoutExpired(
                    "synthetic worker",
                    0 if timeout is None else timeout,
                )
            return -15

        def terminate(self) -> None:
            return None

        def kill(self) -> None:
            raise AssertionError("terminated worker should exit during grace")

    with patch(
        "devtools.wall_owner_parent_experiment.subprocess.Popen",
        return_value=Process(),
    ):
        status = supervise_parent_worker(("synthetic-worker",), output)

    assert status == 1
    replaced = cast(dict[str, object], json.loads(output.read_text(encoding="utf-8")))
    validate_result_document(replaced)
    assert replaced["status"] == "partial"
    assert replaced["sources"] == complete["sources"]
    assert replaced["residual_check"] == complete["residual_check"]
    assert replaced["error"] == "worker exceeded the 120-second external bound"

    partial_output = tmp_path / "timeout-after-partial.json"
    partial = copy.deepcopy(complete)
    partial["status"] = "partial"
    partial["outcome"] = "incomplete"
    partial["error"] = "selected owner comparisons remain"
    partial_clocks = cast(dict[str, object], partial["clocks"])
    partial_clocks["scientific_seconds"] = 40.0
    partial_clocks["process_seconds"] = 41.0
    write_result_document(partial_output, partial)

    with (
        patch(
            "devtools.wall_owner_parent_experiment.subprocess.Popen",
            return_value=Process(),
        ),
        patch(
            "devtools.wall_owner_parent_experiment.time.perf_counter",
            side_effect=(0.0, 122.5),
        ),
    ):
        status = supervise_parent_worker(("synthetic-worker",), partial_output)

    assert status == 1
    timed_out_partial = cast(
        dict[str, object], json.loads(partial_output.read_text(encoding="utf-8"))
    )
    validate_result_document(timed_out_partial)
    assert timed_out_partial["status"] == "partial"
    assert timed_out_partial["sources"] == complete["sources"]
    assert timed_out_partial["residual_check"] == complete["residual_check"]
    assert timed_out_partial["error"] == "worker exceeded the 120-second external bound"
    assert cast(dict[str, object], timed_out_partial["clocks"])["process_seconds"] == 122.5


def test_readback_replays_comparison_geometry_and_attribution(tmp_path: Path) -> None:
    inputs = _one_frame_parent_inputs()
    owner = inputs.selected_owners[3]
    residual_centre = inputs.strict_escape.escape.centre
    residual_u = inputs.selected_residual.ray
    b_only = evaluate_class(
        owner.wall_class,
        owner_mark=owner.owner_class.mark,
        corner_index=owner.corner_index,
        class_index=owner.class_index,
        transform=owner.physical_map,
        residual_centre=residual_centre,
        residual_u=residual_u,
        expected_frames=1,
        outer_side=GLOBAL_PARENT_RULE.outer_side,
        half=GLOBAL_PARENT_RULE.core_side / 2,
        deadline=10**9,
    )
    parent = evaluate_parent_class(
        owner.wall_class.frames,
        owner.expected_frames,
        owner_mark=owner.owner_class.mark,
        transform=owner.physical_map,
        residual_centre=residual_centre,
        residual_u=residual_u,
        deadline=100.0,
        clock=lambda: 0.0,
    )
    assert b_only.status == "compatible"
    assert parent.status == "compatible"
    residual = check_residual_parent_centre(
        residual_centre,
        residual_u,
        inputs.selected_residual.sources,
        inputs.residual_manifest[inputs.selected_residual.index].sources,
    )
    evaluation = ParentExperimentEvaluation(
        "partial",
        "incomplete",
        residual,
        (
            ParentOwnerComparison(
                owner,
                "complete",
                "still-compatible",
                b_only,
                parent,
            ),
        ),
        "selected owner comparisons remain",
    )

    def loader(
        pins: ParentInputPins,
        *,
        replay_deadline: float,
    ) -> ParentAdapterInputs:
        del pins
        assert replay_deadline in (120.0, 10**9)
        return inputs

    expected_inputs = inputs

    def target(
        inputs: ParentAdapterInputs,
        *,
        deadline: float,
        clock: Callable[[], float],
        checkpoint: Callable[[ParentExperimentEvaluation], None],
    ) -> ParentExperimentEvaluation:
        del deadline, clock, checkpoint
        assert inputs is expected_inputs
        return evaluation

    output = tmp_path / "comparison.json"
    times = iter((0.0, 1.0, 2.0, 3.0, 4.0, 5.0))
    execute_parent_experiment(
        _pins(),
        implementation_revision=CHECKOUT,
        output=output,
        clock=times.__next__,
        loader=loader,
        target=target,
    )
    loaded = load_parent_result(
        output,
        _pins(),
        replay_deadline=10**9,
        loader=loader,
        revision_validator=lambda _repository, revision: revision,
        clock=lambda: 0.0,
    )
    assert loaded["status"] == "partial"

    original = cast(dict[str, object], json.loads(output.read_text(encoding="utf-8")))
    changed = copy.deepcopy(original)
    comparisons = cast(list[dict[str, object]], changed["comparisons"])
    parent_record = cast(dict[str, object], comparisons[0]["parent_restricted"])
    extrema = cast(list[dict[str, object]], parent_record["frame_extrema"])
    maximum = cast(dict[str, object], extrema[0]["maximum"])
    maximum["slack"] = "0"
    output.write_text(json.dumps(changed), encoding="utf-8")
    with pytest.raises(ParentExperimentError, match="parent-restricted result"):
        load_parent_result(
            output,
            _pins(),
            replay_deadline=10**9,
            loader=loader,
            revision_validator=lambda _repository, revision: revision,
            clock=lambda: 0.0,
        )

    changed = copy.deepcopy(original)
    comparisons = cast(list[dict[str, object]], changed["comparisons"])
    comparisons[0]["attribution"] = "owner-domain-gain"
    output.write_text(json.dumps(changed), encoding="utf-8")
    with pytest.raises(ParentExperimentError, match="completion fields"):
        load_parent_result(
            output,
            _pins(),
            replay_deadline=10**9,
            loader=loader,
            revision_validator=lambda _repository, revision: revision,
            clock=lambda: 0.0,
        )


def test_readback_replays_unresolved_parent_prefixes() -> None:
    inputs = _one_frame_parent_inputs()
    owner = inputs.selected_owners[3]
    complete = evaluate_parent_class(
        owner.wall_class.frames,
        owner.expected_frames,
        owner_mark=owner.owner_class.mark,
        transform=owner.physical_map,
        residual_centre=inputs.strict_escape.escape.centre,
        residual_u=inputs.selected_residual.ray,
        deadline=100.0,
        clock=lambda: 0.0,
    )
    unresolved = replace(
        complete,
        status="unresolved",
        global_maximum_slack=None,
        error="synthetic expiry after saved prefix",
    )
    record = parent_result_record(unresolved)
    replay_parent_result_record(
        record,
        owner,
        inputs,
        deadline=100.0,
        clock=lambda: 0.0,
    )

    changed = copy.deepcopy(record)
    derived = cast(list[dict[str, object]], changed["derived_frames"])
    derived[0]["extent"] = "1/2"
    with pytest.raises(ParentExperimentError, match="derived frame"):
        replay_parent_result_record(
            changed,
            owner,
            inputs,
            deadline=100.0,
            clock=lambda: 0.0,
        )
