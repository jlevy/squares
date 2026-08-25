#!/usr/bin/env python3
"""Render an explicit packing source as deterministic, self-contained SVG."""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqpack.render import AnnotationLevel, Overlay, RenderSpec, ViewLevel, render_packing_svg
from sqpack.render.adapters import (
    frame_from_gobel10,
    frame_from_trump11,
    frames_from_basin_event,
    trajectory_from_n5_equal_side_face,
)
from sqpack.render.svg import write_svg_atomic


def _add_render_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--view", choices=[value.value for value in ViewLevel], default="overview"
    )
    parser.add_argument(
        "--annotations",
        choices=[value.value for value in AnnotationLevel],
        default="minimal",
    )
    parser.add_argument(
        "--contacts",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="show certified exact contacts when the source provides them (default: on)",
    )
    parser.add_argument("--output", type=Path, required=True)


def build_source_parser(parser: argparse.ArgumentParser) -> None:
    sources = parser.add_subparsers(dest="source", required=True)
    event = sources.add_parser("event", help="BasinEvent/v3 JSON or JSONL")
    _add_render_options(event)
    event.add_argument("path", type=Path)
    event.add_argument("--event-id")
    builtin = sources.add_parser("builtin", help="retained built-in packing")
    _add_render_options(builtin)
    builtin.add_argument("name", choices=("gobel10", "trump11"))
    n5_face = sources.add_parser("n5-face", help="certified exact n=5 trajectory")
    _add_render_options(n5_face)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    build_source_parser(parser)
    return parser.parse_args()


def load_event(path: Path, event_id: str | None = None) -> dict[str, object]:
    records = [
        json.loads(line, parse_float=Decimal)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(records) == 1 and isinstance(records[0], list):
        records = records[0]
    if event_id is not None:
        records = [record for record in records if str(record.get("event_id")) == event_id]
    if len(records) != 1 or not isinstance(records[0], dict):
        raise ValueError("event selection must resolve to exactly one BasinEvent/v3 object")
    return records[0]


def load_builtin(name: str):
    return frame_from_gobel10() if name == "gobel10" else frame_from_trump11()


def build_spec(args: argparse.Namespace) -> RenderSpec:
    overlays = frozenset({Overlay.CONTACTS}) if args.contacts else frozenset()
    return RenderSpec(
        view=ViewLevel(args.view),
        annotations=AnnotationLevel(args.annotations),
        overlays=overlays,
    )


def main() -> int:
    args = parse_args()
    try:
        spec = build_spec(args)
        start = trajectory = None
        if args.source == "event":
            start, final = frames_from_basin_event(load_event(args.path, args.event_id))
        elif args.source == "builtin":
            final = load_builtin(args.name)
            if spec.view is ViewLevel.COMPARISON:
                start = final
        else:
            trajectory = trajectory_from_n5_equal_side_face()
            final = trajectory.frames[-1]
            if spec.view is ViewLevel.COMPARISON:
                start = trajectory.frames[0]
        text = render_packing_svg(final, start=start, trajectory=trajectory, spec=spec)
        write_svg_atomic(args.output, text)
        print(f"wrote {args.output} ({len(text.encode())} bytes)")
    except (OSError, TypeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
