"""Controls for the exact same-side local stack recipe."""

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
