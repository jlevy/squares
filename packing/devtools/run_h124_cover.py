"""Bound a separately declared whole-band H124 cover or an unrelated toy control.

No scientific source is constructed on import. The reader route reconstructs its
source independently; a proof for one named band is not a proof of H124. Both bands
and the reviewed analytical reduction are required. Failed covers stay unresolved.
"""

from __future__ import annotations

import argparse
import json
import signal
import subprocess
import sys
import time
from collections.abc import Sequence
from importlib import import_module
from pathlib import Path
from typing import Any

from devtools.check_closed_polygon_cover import check_packet
from devtools.check_full_size_density_support_ceiling import PACKET_BYTES, load_packet
from devtools.closed_polygon_cover import produce_cover
from sqpack.field import NumberField

KIND = "h124-closed-cover/v1"
MAX_LIMIT = 5000
MAX_SECONDS = 120


def scientific_source(
    frame: str | None, *, reader: bool, collision: bool = False
) -> tuple[NumberField, Any, Any]:
    """Load only the requested independent route, under the worker's process cap."""
    if collision:
        module = "check_h124_collision_source" if reader else "h124_collision_source"
        return import_module(f"devtools.{module}").cover_source()
    module = "check_h124_cover_source" if reader else "h124_cover_source"
    return import_module(f"devtools.{module}").cover_source(frame)


def toy_source(control: str) -> tuple[NumberField, Any, Any]:
    """Unrelated rational rectangles; no scientific constants or constructors."""
    field = NumberField((1, 0), (-1, 1))

    def point(x: int, y: int) -> list[list[str]]:
        return [[str(x)], [str(y)]]

    polygons = []
    if control == "covered":
        polygons = [
            {"id": "toy", "vertices": [point(0, 0), point(1, 0), point(1, 1), point(0, 1)]}
        ]
    elif control != "gap":
        raise ValueError("unknown unrelated toy control")
    return field, [point(0, 0), point(1, 1)], polygons


def serialize_packet(raw: Any) -> str:
    encoded = json.dumps(raw, sort_keys=True, allow_nan=False)
    if len(encoded.encode("utf-8")) + 1 > PACKET_BYTES:
        raise ValueError("serialized cover exceeds the input byte cap")
    return encoded


def worker(
    *,
    frame: str | None,
    control: str | None,
    raw: Any,
    limit: int,
    collision: bool = False,
) -> dict[str, Any]:
    """Explicit source, exact bound and complete independent replay only."""
    if type(collision) is not bool:
        raise ValueError("collision mode must be boolean")
    if (frame is not None) + (control is not None) + collision != 1:
        raise ValueError("exactly one explicit band, collision mode or toy control is required")
    if frame is not None and frame not in ("axis", "diagonal"):
        raise ValueError("unknown scientific band")
    if control is not None and control not in ("covered", "gap"):
        raise ValueError("unknown toy control")
    if type(limit) is not int or not 1 <= limit <= MAX_LIMIT:
        raise ValueError("event and slab cap outside admitted range")
    source = (
        "h124:axis-collision-v1"
        if collision
        else f"h124:{frame}"
        if frame is not None
        else f"toy:{control}"
    )
    if raw is not None and (
        type(raw) is not dict
        or set(raw) != {"kind", "source", "certificate"}
        or raw["kind"] != KIND
        or raw["source"] != source
    ):
        raise ValueError("cover envelope differs from the explicit source")
    if collision:
        field, rectangle, polygons = scientific_source(
            None, reader=raw is not None, collision=True
        )
    elif frame is not None:
        field, rectangle, polygons = scientific_source(frame, reader=raw is not None)
    else:
        field, rectangle, polygons = toy_source(control or "")
    if raw is None:
        return {
            "kind": KIND,
            "source": source,
            "certificate": produce_cover(
                field,
                rectangle,
                polygons,
                event_limit=limit,
                slab_limit=limit,
            ),
        }
    checked = check_packet(
        raw["certificate"], field=field, rectangle=rectangle, polygons=polygons
    )
    proved = checked["status"] == "verified_cover" and checked["cover_proved"] is True
    return {
        "source": source,
        "status": "verified_source_cover" if proved else "unresolved",
        "cover_proved": proved,
        "verification": checked,
        "scope": (
            "This source cover only; H124 requires both whole bands "
            "and the reviewed analytical reduction."
        ),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--frame", choices=("axis", "diagonal"))
    modes.add_argument("--toy-control", choices=("covered", "gap"))
    modes.add_argument("--axis-collision", action="store_true")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--limit", type=int, required=True)
    parser.add_argument("--timeout-seconds", type=int, required=True)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if not 1 <= args.limit <= MAX_LIMIT or not 1 <= args.timeout_seconds <= MAX_SECONDS:
        parser.error("limits require 1-5000 events/slabs and 1-120 process seconds")

    def expired(_signal: int, _frame: Any) -> None:
        raise TimeoutError("cover worker reached its fixed cap")

    try:
        if args.worker:
            start, cpu = time.monotonic(), time.process_time()
            previous = signal.signal(signal.SIGALRM, expired)
            signal.alarm(args.timeout_seconds)
            try:
                raw = load_packet(args.input) if args.input is not None else None
                if args.input is not None and type(raw) is not dict:
                    raise ValueError(
                        "input certificate must be an object, never a producer request"
                    )
                encoded = serialize_packet(
                    worker(
                        frame=args.frame,
                        control=args.toy_control,
                        collision=args.axis_collision,
                        raw=raw,
                        limit=args.limit,
                    )
                )
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, previous)
            print(encoded)
            print(
                json.dumps(
                    {
                        "wall_seconds": time.monotonic() - start,
                        "cpu_seconds": time.process_time() - cpu,
                    }
                ),
                file=sys.stderr,
            )
            return 0
        command = [
            sys.executable,
            "-m",
            "devtools.run_h124_cover",
            "--worker",
            "--limit",
            str(args.limit),
            "--timeout-seconds",
            str(args.timeout_seconds),
        ]
        if args.axis_collision:
            command.append("--axis-collision")
        else:
            command.extend(
                ["--frame", args.frame]
                if args.frame is not None
                else ["--toy-control", args.toy_control]
            )
        if args.input is not None:
            command.extend(["--input", str(args.input)])
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=args.timeout_seconds, check=False
        )
        sys.stderr.write(completed.stderr)
        if completed.returncode == 0:
            sys.stdout.write(completed.stdout)
    except subprocess.TimeoutExpired, TimeoutError:
        print("unresolved: complete subprocess exceeded its original cap", file=sys.stderr)
        return 1
    except (OSError, ArithmeticError, ValueError, RecursionError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    else:
        return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
