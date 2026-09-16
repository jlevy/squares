"""Controls for the video capture's pure parts and the animation SVG export.

The capture itself needs a browser and ffmpeg, so what is tested here is everything around
them that decides what the file says: how steps are priced, which instants are sampled,
what the receipt records, and what ffmpeg is asked to write and where. The export is run
end to end through its command, and its honesty statement is read back from the file it
wrote rather than from the document it was given.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections.abc import Callable
from itertools import pairwise
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import pytest

from workbench_tools import animation_render, capture_video, export_animation_svg
from workbench_tools.animation_records import ANIMATION_CONTRACT, decode_animation
from workbench_tools.animation_render import TRANSITIONS_STATEMENT

FIXTURES = Path(__file__).parent / "fixtures"
SVG = "{http://www.w3.org/2000/svg}"

Runner = Callable[..., subprocess.CompletedProcess[str]]


# ---------------------------------------------------------------- capture: pricing and schedule


def _beat(*, on: bool, first: int, last: int, duration: float) -> dict[str, Any]:
    return {
        "continuous": on,
        "range": {
            "first": first,
            "last": last,
            "steps": last - first + 1,
            "duration": duration,
        },
    }


def _steps(*indices: int) -> list[dict[str, Any]]:
    return [{"index": index, "n": index + 1, "kind": "assignment"} for index in indices]


def test_pricing_accepts_the_continuous_beat_the_page_plays() -> None:
    durations = [2.4, 1.15]
    beat = _beat(on=True, first=0, last=1, duration=3.55)
    assert capture_video.price_steps(_steps(0, 1), durations, beat) == durations


def test_pricing_refuses_the_single_step_beat() -> None:
    # The review's measurement: priced with continuous play off, a static append runs 2.4 s
    # where the page plays it in 1.15 s. The page says which beat it is on, and that is read.
    beat = _beat(on=False, first=0, last=1, duration=4.8)
    with pytest.raises(SystemExit, match="continuous"):
        capture_video.price_steps(_steps(0, 1), [2.4, 2.4], beat)


def test_pricing_refuses_durations_that_disagree_with_the_range() -> None:
    beat = _beat(on=True, first=0, last=1, duration=3.55)
    with pytest.raises(SystemExit, match="range"):
        capture_video.price_steps(_steps(0, 1), [2.4, 2.4], beat)


def test_pricing_refuses_steps_the_page_did_not_scope() -> None:
    beat = _beat(on=True, first=1, last=2, duration=3.55)
    with pytest.raises(SystemExit, match="range"):
        capture_video.price_steps(_steps(0, 1), [2.4, 1.15], beat)


def test_the_pricing_commands_turn_continuous_play_on_and_leave_it_paused() -> None:
    commands = capture_video.pricing_commands(2, 24)
    names = [command[0] for command in commands]
    assert ["setRange", 2, 24] in commands
    assert names.index("setRange") < names.index("playRange") < names.index("pause")
    assert names[-1] == "pause"


def test_the_schedule_has_duration_times_fps_frames_and_no_boundary_repeat() -> None:
    durations = [1.0, 0.5, 1.5]
    schedule = capture_video.frame_schedule(durations, 4)
    assert len(schedule) == round(sum(durations) * 4) == 12
    assert [sample.index for sample in schedule] == list(range(12))
    # Each instant is sampled once. The old capture sampled a step's end and then the next
    # step's start, which draw the same picture, so every boundary was a repeated frame.
    instants = [sum(durations[: sample.step]) + sample.at for sample in schedule]
    assert len(set(instants)) == len(instants)
    assert instants == sorted(instants)
    assert not [sample for sample in schedule if sample.at == 0.0]
    # A step owns the instants up to and including its end, so a step whose end is on the
    # frame grid ends on its settled packing, and the range always ends settled.
    ends = [(s.step, s.at) for s in schedule if s.at == durations[s.step]]
    assert ends == [(0, 1.0), (1, 0.5), (2, 1.5)]
    assert capture_video.frames_per_step(schedule, len(durations)) == [4, 2, 6]


def test_the_schedule_rounds_a_range_off_the_grid_to_the_nearest_frame() -> None:
    durations = [1.15, 2.4]
    schedule = capture_video.frame_schedule(durations, 30)
    assert len(schedule) == round(3.55 * 30)
    assert (schedule[-1].step, schedule[-1].at) == (1, 2.4)
    assert all(0.0 < sample.at <= durations[sample.step] for sample in schedule)


@pytest.mark.parametrize(("durations", "fps"), [([], 30), ([1.0], 0), ([float("nan")], 30)])
def test_the_schedule_refuses_an_empty_or_unfinite_clock(
    durations: list[float], fps: int
) -> None:
    with pytest.raises(ValueError, match=r"step|fps|finite"):
        capture_video.frame_schedule(durations, fps)


# ---------------------------------------------------------------- capture: encode and receipt


def test_ffmpeg_version_is_read_from_its_banner() -> None:
    banner = "ffmpeg version 7.1.1 Copyright (c) 2000-2025 the FFmpeg developers\nbuilt with"
    assert capture_video.ffmpeg_version(banner) == "ffmpeg version 7.1.1"


def test_the_encode_is_faststart_and_says_transitions_are_not_packings(tmp_path: Path) -> None:
    out = tmp_path / "ascent.partial.mp4"
    arguments = capture_video.encode_arguments(
        "ffmpeg", tmp_path / "frames", 30, out, page_sha256="ab" * 32, title="n = 2 to 3"
    )
    assert arguments[-1] == str(out)
    assert "-y" not in arguments
    flags = list(pairwise(arguments))
    assert ("-movflags", "+faststart") in flags
    assert ("-i", str(tmp_path / "frames" / capture_video.FRAME_PATTERN)) in flags
    comments = [v for flag, v in flags if flag == "-metadata" and v.startswith("comment=")]
    assert len(comments) == 1
    assert "illustrative-tween" in comments[0]
    assert "not packings" in comments[0]
    assert "ab" * 32 in comments[0]


def _fake_ffmpeg(out: Path, returncode: int) -> tuple[list[bool], Runner]:
    seen_final: list[bool] = []

    def run(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        target = Path(command[-1])
        assert target != out
        assert target.parent == out.parent
        seen_final.append(out.read_bytes() == b"old video")
        target.write_bytes(b"new video")
        return subprocess.CompletedProcess(command, returncode, "", "encoder broke")

    return seen_final, run


def test_the_video_is_encoded_beside_its_destination_and_renamed_into_place(
    tmp_path: Path,
) -> None:
    out = tmp_path / "ascent.mp4"
    out.write_bytes(b"old video")
    seen_old, run = _fake_ffmpeg(out, 0)
    command = capture_video.encode_into_place(
        lambda partial: ["ffmpeg", str(partial)], out, run=run
    )
    assert seen_old == [True]
    assert out.read_bytes() == b"new video"
    assert Path(command[-1]) != out
    assert sorted(path.name for path in tmp_path.iterdir()) == ["ascent.mp4"]


def test_a_failed_encode_leaves_neither_a_partial_nor_a_replaced_video(tmp_path: Path) -> None:
    out = tmp_path / "ascent.mp4"
    out.write_bytes(b"old video")
    _, run = _fake_ffmpeg(out, 1)
    with pytest.raises(SystemExit, match="ffmpeg failed"):
        capture_video.encode_into_place(lambda partial: ["ffmpeg", str(partial)], out, run=run)
    assert out.read_bytes() == b"old video"
    assert sorted(path.name for path in tmp_path.iterdir()) == ["ascent.mp4"]


def test_the_receipt_carries_the_plan_d9_statement_and_provenance() -> None:
    steps = [
        {"n": 3, "seconds": 1.0, "frames": 30, "landed_on_record": True, "ms_per_frame": 40.0},
        {"n": 4, "seconds": 0.5, "frames": 15, "landed_on_record": False, "ms_per_frame": 50.0},
    ]
    provenance = capture_video.Provenance(
        commit="0" * 40,
        dirty=True,
        playwright_version="1.62.0",
        browser_version="151.0.7922.34",
        ffmpeg_version="ffmpeg version 7.1.1",
    )
    receipt = capture_video.capture_receipt(
        page="site/workbench/index.html",
        page_sha256="a" * 64,
        video="ascent.mp4",
        video_sha256="b" * 64,
        first=2,
        last=4,
        fps=30,
        size=(1920, 1080),
        steps=steps,
        provenance=provenance,
        encoder=["ffmpeg", "-movflags", "+faststart"],
        capture_seconds=12.34,
    )
    assert receipt["transitions_are_packings"] is False
    assert "not packings" in receipt["reason"]
    assert receipt["intermediate_frames"] == "illustrative-tween"
    assert receipt["commit"] == "0" * 40
    assert receipt["dirty"] is True
    assert receipt["playwright_version"] == "1.62.0"
    assert receipt["browser_version"] == "151.0.7922.34"
    assert receipt["ffmpeg_version"] == "ffmpeg version 7.1.1"
    assert receipt["frames"] == 45
    assert receipt["seconds"] == 1.5
    assert receipt["steps_off_record"] == [4]
    assert receipt["ms_per_frame"] == {"mean": 45.0, "worst": 50.0, "worst_at_n": 4}
    assert json.loads(json.dumps(receipt)) == receipt


def test_the_receipt_is_written_atomically(tmp_path: Path) -> None:
    path = tmp_path / "ascent.receipt.json"
    capture_video.write_receipt(path, {"transitions_are_packings": False})
    assert json.loads(path.read_text(encoding="utf-8")) == {"transitions_are_packings": False}
    assert sorted(p.name for p in tmp_path.iterdir()) == ["ascent.receipt.json"]


def test_the_repository_state_names_a_commit() -> None:
    commit, dirty = capture_video.repository_state(capture_video.REPO)
    assert commit is not None
    assert len(commit) == 40
    assert isinstance(dirty, bool)


# ---------------------------------------------------------------- the SVG export


def _write_animation(tmp_path: Path, document: dict[str, Any]) -> Path:
    path = tmp_path / "animation.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    return path


def _guided_fixture() -> dict[str, Any]:
    raw = json.loads((FIXTURES / "packing-animation-v1.json").read_text(encoding="utf-8"))
    raw["palette"]["shade"] = "full-side-contact"
    return raw


def _checked_fixture() -> dict[str, Any]:
    frames = [
        {
            "t": 0.0,
            "side": 2.0,
            "squares": [[0.5, 0.5, 0.0], [1.5, 0.5, 0.0]],
            "feasible": True,
        },
        {
            "t": 1.0,
            "side": 2.0,
            "squares": [[0.5, 1.5, 0.0], [1.5, 1.5, 0.0]],
            "feasible": True,
        },
    ]
    return {"contract": ANIMATION_CONTRACT, "name": "checked", "n": 2, "frames": frames}


def _read_svg(svg_text: str) -> tuple[str, list[str]]:
    """The file's description, and every line of text it draws."""
    root = ET.fromstring(svg_text)
    desc = root.find(f"{SVG}desc")
    assert desc is not None
    assert desc.text is not None
    drawn = ["".join(node.itertext()) for node in root.iter(f"{SVG}text")]
    return desc.text, drawn


def test_the_exported_file_says_its_transitions_are_not_packings(tmp_path: Path) -> None:
    source = _write_animation(tmp_path, _guided_fixture())
    out = tmp_path / "out" / "animation.svg"
    assert export_animation_svg.main([str(source), "--out", str(out), "--width", "320"]) == 0
    desc, drawn = _read_svg(out.read_text(encoding="utf-8"))
    assert TRANSITIONS_STATEMENT in desc
    # No caption line: the statement is in the description, not drawn on the picture.
    assert not [line for line in drawn if "illustrative" in line or "not packings" in line]
    receipt = json.loads(out.with_suffix(".receipt.json").read_text(encoding="utf-8"))
    assert receipt["transitions_are_packings"] is False
    assert TRANSITIONS_STATEMENT in receipt["reason"]
    assert receipt["svg_sha256"] == hashlib.sha256(out.read_bytes()).hexdigest()
    assert receipt["animation_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert sorted(p.name for p in out.parent.iterdir()) == [
        "animation.receipt.json",
        "animation.svg",
    ]


def test_a_checked_unguided_export_still_says_its_tweens_are_not_packings(
    tmp_path: Path,
) -> None:
    """Every frame here is a checked packing, but the motion between them is a tween."""
    source = _write_animation(tmp_path, _checked_fixture())
    out = tmp_path / "checked.svg"
    assert export_animation_svg.main([str(source), str(out), "--width", "320"]) == 0
    desc, drawn = _read_svg(out.read_text(encoding="utf-8"))
    assert TRANSITIONS_STATEMENT in desc
    assert not [line for line in drawn if "illustrative" in line or "not packings" in line]
    receipt = json.loads(out.with_suffix(".receipt.json").read_text(encoding="utf-8"))
    # The in-between states are interpolated either way: the receipt never calls them packings.
    assert receipt["transitions_are_packings"] is False
    assert "interpolate" in receipt["reason"]


def test_the_output_path_is_given_positionally_or_with_out_but_once(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = _write_animation(tmp_path, _checked_fixture())
    both = [str(source), str(tmp_path / "a.svg"), "--out", str(tmp_path / "b.svg")]
    with pytest.raises(SystemExit):
        export_animation_svg.main(both)
    assert "once" in capsys.readouterr().err
    with pytest.raises(SystemExit):
        export_animation_svg.main([str(source)])
    assert "output" in capsys.readouterr().err
    assert not list(tmp_path.glob("*.svg"))


@pytest.fixture
def scripted_renderer(monkeypatch: pytest.MonkeyPatch) -> None:
    real = animation_render.render_packing_svg

    # The injected element is a fixture file: a script body written as a Python string is
    # what the repository's no-JavaScript-in-Python rule forbids, test data included.
    injected = (FIXTURES / "svg-script-element.svg").read_text(encoding="utf-8").strip()

    def render(*args: Any, **kwargs: Any) -> str:
        return real(*args, **kwargs).replace("</svg>", f"{injected}</svg>")

    monkeypatch.setattr(animation_render, "render_packing_svg", render)


@pytest.mark.usefixtures("scripted_renderer")
def test_export_svg_refuses_a_rendering_that_carries_a_script() -> None:
    # Refused in `export_svg` itself, not only by the atomic writer's element allowlist, so a
    # caller that writes the text some other way gets the same refusal.
    document = decode_animation(_checked_fixture())
    with pytest.raises(ValueError, match="contains a script element"):
        animation_render.export_svg(document, width=320)


@pytest.mark.usefixtures("scripted_renderer")
def test_an_svg_carrying_a_script_is_refused_and_nothing_is_written(tmp_path: Path) -> None:
    source = _write_animation(tmp_path, _checked_fixture())
    with pytest.raises(ValueError, match="script"):
        export_animation_svg.main([str(source), "--out", str(tmp_path / "scripted.svg")])
    assert sorted(p.name for p in tmp_path.iterdir()) == ["animation.json"]


def test_the_export_receipt_is_written_after_the_svg(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = _write_animation(tmp_path, _checked_fixture())

    def refuse(*_: object) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(export_animation_svg, "write_svg_atomic", refuse)
    with pytest.raises(OSError, match="disk full"):
        export_animation_svg.main([str(source), str(tmp_path / "late.svg")])
    assert sorted(p.name for p in tmp_path.iterdir()) == ["animation.json"]
