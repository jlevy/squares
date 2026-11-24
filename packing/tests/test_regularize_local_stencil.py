"""Controls for the exact same-side local stack recipe."""

import gzip
import hashlib
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path

import pytest

from devtools import regularize_local_stencil as local
from devtools import regularize_same_side as same


def fixture_frame() -> same.Frame:
    return same.Frame(
        kind="rational",
        side=Q(5),
        reported_side=Q(5),
        centers=[(Q(1), Q(1)), (Q(2), Q(5, 4)), (Q(2), Q(3)), (Q(4), Q(4))],
        rotations=[(Q(1), Q(0)), (Q(1), Q(0)), (Q(4, 5), Q(3, 5)), (Q(1), Q(0))],
        ids=[8, 3, 12, 2],
        derivation="test",
    )


def test_stack_closes_two_face_contacts_and_holds_other_squares() -> None:
    frame = fixture_frame()
    centers, rotations, straightened = local.stack(frame, ["8", "3", "12"])
    assert centers == [(Q(1), Q(1)), (Q(2), Q(1)), (Q(2), Q(2)), (Q(4), Q(4))]
    assert all(match.rotation == (Q(1), Q(0)) for match in rotations)
    assert straightened == [3]
    assert frame.centers[1:3] == [(Q(2), Q(5, 4)), (Q(2), Q(3))]
    assert frame.rotations[2] == (Q(4, 5), Q(3, 5))


def test_stack_refuses_repeated_ids_or_an_angled_anchor() -> None:
    frame = fixture_frame()
    with pytest.raises(ValueError, match="three distinct IDs"):
        local.stack(frame, ["8", "3", "8"])
    with pytest.raises(ValueError, match="must already be axis aligned"):
        local.stack(frame, ["12", "3", "8"])


def test_receipt_identifies_the_installed_drawing_and_both_full_checks() -> None:
    path = local.RECEIPTS / "think-1po1-2026-11-23/receipt.json"
    receipt_path = local.receipt_path(path)
    receipt = local.driver.read_json(receipt_path)
    assert receipt["comparison"]["after"]["drawing"]["path"] == local.view_path(127)
    assert receipt["comparison"]["losses"] == []
    assert receipt["comparison"]["after"]["uneven_axis"] == 0
    assert receipt["run"]["parameters"]["admission_receipt"] == path.as_posix()
    assert all(
        verdict["passed"] and verdict["pairs_tested"] == 8001
        for verdict in receipt["verdicts"].values()
    )


def test_restart_restores_only_interrupted_count(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(local, "REPO", tmp_path)
    view = tmp_path / local.view_path(7)
    view.parent.mkdir(parents=True)
    view.write_bytes(b"incomplete")
    marker = view.with_name("another-count.svg")
    marker.write_bytes(b"unchanged")
    receipt = local.receipt_path(local.RECEIPTS / "example/receipt.json")
    entry = {"n": 7, "generator": "old"}
    monkeypatch.setattr(local.census, "read_index", lambda _: {7: entry})
    state, backup = local.pending_paths(receipt)
    local.driver.write_json(state, {"n": 7, "entry": entry, "had_view": True})
    local.driver.write_json(receipt, {"n": 7})
    backup.write_bytes(b"previous")

    local.restore_interrupted(7, receipt)
    assert view.read_bytes() == b"previous"
    assert marker.read_bytes() == b"unchanged"
    assert not any(path.exists() for path in (state, backup, receipt))


def test_new_run_on_a_stencil_count_reaches_admission(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(local, "REPO", tmp_path)
    old = local.receipt_path(local.RECEIPTS / "old/receipt.json")
    new = local.receipt_path(local.RECEIPTS / "new/receipt.json")
    entry = {"generator": local.axis.LOCAL_STENCIL_GENERATOR, "run": {"id": local.run_id(old)}}
    monkeypatch.setattr(local.census, "read_index", lambda _: {7: entry})

    assert not local.already_installed(7, ["1", "2", "3"], new)
    with pytest.raises(ValueError, match="original admission receipt"):
        local.already_installed(7, ["1", "2", "3"], old)


def test_installer_rolls_back_an_ordinary_write_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(local, "REPO", tmp_path)
    view = tmp_path / local.view_path(7)
    view.parent.mkdir(parents=True)
    view.write_bytes(b"previous")
    entry = {"generator": "old"}
    monkeypatch.setattr(local.census, "read_index", lambda _: {7: entry})
    receipt = local.receipt_path(local.RECEIPTS / "example/receipt.json")

    def fail(*_args: object, **_kwargs: object) -> None:
        assert receipt.is_file()
        view.write_bytes(b"incomplete")
        raise OSError("injected write failure before committing the index")

    monkeypatch.setattr(local.driver, "admit_views", fail)
    admitted = local.driver.Admitted(
        n=7,
        generator=local.axis.LOCAL_STENCIL_GENERATOR,
        run={"id": local.run_id(receipt)},
        source={},
        side={},
        view={},
        provenance={},
        routes={},
        decision={},
        measured={},
        regularization={},
        house_after=[],
    )
    with pytest.raises(OSError, match="injected write failure"):
        local.install(admitted, {}, receipt, elapsed=1, cpu=1)
    assert view.read_bytes() == b"previous"
    assert not any(path.exists() for path in (*local.pending_paths(receipt), receipt))


def test_faces_close_in_native_coordinate_order_and_hold_the_exterior() -> None:
    frame = fixture_frame()
    pairs = [("3", "8"), ("2", "3")]
    centers, steps = local.aligned_faces(frame, pairs)
    assert centers == [(Q(1), Q(1)), (Q(2), Q(1)), frame.centers[2], (Q(2), Q(2))]
    assert [step["offset"] for step in steps] == [[1, 0], [0, 1]]
    assert [step["translation"] for step in steps] == [["0", "-1/4"], ["-2", "-2"]]
    assert frame.centers[1] == (Q(2), Q(5, 4))
    with pytest.raises(ValueError, match="already coincide"):
        local.aligned_faces(replace(frame, centers=centers), pairs)
    left, steps = local.aligned_faces(frame, [("8", "3")])
    assert steps[0]["offset"] == [-1, 0]
    assert left[0] == (Q(1), Q(5, 4))
    below, steps = local.aligned_faces(frame, [("3", "2")])
    assert steps[0]["offset"] == [0, -1]
    assert below[1] == (Q(4), Q(3))


def test_faces_refuse_ambiguous_tilted_and_reopened_contacts() -> None:
    frame = fixture_frame()
    for pairs, reason in (
        ([("8", "12")], "axis aligned"),
        ([("8", "2")], "dominant axis"),
        ([("3", "8"), ("3", "2")], "reopened"),
        ([("3", "3")], "distinct square IDs"),
        ([("3", "99")], "distinct square IDs"),
    ):
        with pytest.raises(ValueError, match=reason):
            local.aligned_faces(frame, pairs)


def test_face_install_replays_the_axis_recipe_and_checks_its_base(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(local, "REPO", tmp_path)
    frame = fixture_frame()
    matched = [same.Matched(r, i, 0) for i, r in enumerate(frame.rotations)]
    source = {
        "witness": "packing/witnesses/known-best/n-004.yaml",
        "id": "W-004",
        "scalar_kind": "rational",
        "sha256": "a" * 64,
    }
    view_id = "W-004-regularized"
    base = same.same_side_witness({}, frame, frame.centers, matched, view_id=view_id)
    base_text = local.witness_document(base)
    reference = {
        "n": 4,
        "status": "regularized",
        "generator": local.axis.ALGORITHM,
        "source": source,
        "exact_verification": {"passed": True},
        "view": {
            "path": local.view_path(4),
            "sha256": hashlib.sha256(base_text.encode()).hexdigest(),
        },
    }
    faces = [("3", "8")]
    monkeypatch.setattr(local.axis, "manifest_entries", lambda _layout: [{"n": 4}])
    replay_text = base_text

    def regenerate(_row, _layout, *, smallest_dilation):
        assert smallest_dilation is False
        return reference, replay_text, 0

    monkeypatch.setattr(local.axis, "atlas_record", regenerate)
    digest = reference["view"]["sha256"]
    saved_frame, base_record = local.face_base(
        4, reference, source, base, selected=True, selection_digest=digest
    )
    centers, steps = local.aligned_faces(saved_frame, faces)
    construction = {"native_frame": True, "base": base_record, "faces": steps}
    placed = same.same_side_witness({}, frame, centers, matched, view_id=view_id)
    placed["certificate"] = {"generated": construction}
    target = tmp_path / local.view_path(4)
    target.parent.mkdir(parents=True)
    target.write_bytes(gzip.compress(local.witness_document(placed).encode()))
    path = local.receipt_path(local.RECEIPTS / "test-face-alignment/receipt.json")
    run = {
        "id": local.run_id(path),
        "generator": local.axis.LOCAL_FACE_GENERATOR,
        "parameters": {
            **construction,
            "admission_receipt": path.relative_to(tmp_path).as_posix(),
        },
    }
    entry = {
        **reference,
        "generator": run["generator"],
        "run": {"id": run["id"]},
        "reference": reference,
    }
    local.driver.write_json(
        tmp_path / local.driver.LAYER_INDEX_PATH, {"entries": [entry], "runs": [run]}
    )
    local.driver.write_json(
        path,
        {
            "run": run,
            "construction": construction,
            "source": source,
            "n": 4,
            "comparison": {"after": {"drawing": {"path": local.view_path(4)}}},
            "verdicts": {
                name: {"passed": True, "pairs_tested": 6}
                for name in ("exact_verify", "independent")
            },
        },
    )
    assert local.already_installed(4, (), path, faces=faces)
    with pytest.raises(ValueError, match="different face pairs"):
        local.already_installed(4, (), path, faces=[("8", "3")])

    replay_text += "\n"
    assert local.already_installed(4, (), path, faces=faces)
    _, replay_record = local.face_base(
        4, reference, source, base, selected=True, selection_digest=digest
    )
    assert replay_record == base_record
    with pytest.raises(ValueError, match="different sources"):
        local.face_base(
            4,
            reference,
            source,
            {**base, "source": {"path": "other"}},
            selected=True,
            selection_digest=digest,
        )

    shifted = frame.centers.copy()
    shifted[2] = (Q(3), Q(3))
    turned = matched.copy()
    turned[2] = same.Matched((Q(3, 5), Q(4, 5)), 2, 0)
    for differing_base in (
        same.same_side_witness({}, frame, shifted, matched, view_id=view_id),
        same.same_side_witness({}, frame, frame.centers, turned, view_id=view_id),
    ):
        replay_text = local.witness_document(differing_base)
        with pytest.raises(ValueError, match="selected geometry differs"):
            local.face_base(4, reference, source, base, selected=True, selection_digest=digest)
        with pytest.raises(ValueError, match="installed drawing does not match"):
            local.already_installed(4, (), path, faces=faces)
