"""Run the simple mode-A producer on one n17 sub-pattern, then certify it (H-267, BC-418).

The frame is the H-266 unique-state cover at cap 1169/250 with D4 and no capture cap
(`check_hull_kernel_mask0.n17_unique_frame`). A pattern is a set of cells named by the
cover; its claim, if it closes, is that no packing at that cap has distinct squares with
centres in those closed cells, one per cell, whatever the other squares do.

`sqpack.hull_kernel.producer` proposes a seed and a node; nothing it says counts. The
certificate is `node.admit_seed` (every owned point proved, every wall row the full
legal domain) followed by `sequential.replay_sequential` on exactly the produced
objects, which derives closure itself. A certified closure excludes, by containment and
D4, every orbit representative that `Frame.states_containing` lists; a stall excludes
nothing and is reported with every owner's residual extents per round.

The selector lane's flagged arity-6 classes are `A`, `B` and `C`, in its priority order;
`W7` heads its arity-7 certification priority (corner-SW, the west wall, side-N0 and the
two west interior cells).
`endpoint6` is the positive control: six cells of the H256 endpoint's own state, which
the endpoint realises at a side below the cap, so a closure there is a soundness failure
and the run refuses.
"""

from __future__ import annotations

import argparse
import codecs
import gzip
import hashlib
import importlib
import json
import math
import sys
import time
from collections.abc import Iterator
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import check_hull_kernel_mask0 as mask0_tool
from devtools.provenance import provenance
from sqpack.hull_kernel import node, sequential
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError, require
from sqpack.hull_kernel.rational import BACKEND

PATTERNS = {
    "A": (
        "interior-SW",
        "interior-NW",
        "interior-W",
        "interior-S",
        "interior-N",
        "interior-SE",
    ),
    "B": ("side-S1", "side-W1", "interior-NW", "interior-W", "interior-S", "interior-SE"),
    "C": ("interior-NW", "interior-W", "interior-S", "interior-N", "interior-E", "interior-SE"),
    "W7": (
        "corner-SW",
        "side-N0",
        "side-W0",
        "side-W1",
        "side-W2",
        "interior-SW",
        "interior-W",
    ),
    "endpoint6": ("corner-SW", "side-S0", "side-W0", "side-W2", "corner-NW", "interior-W"),
    # Second in the arity-7 certification priority (best penetration 6.3e-5).
    "NW7": (
        "side-N0",
        "side-N1",
        "side-W2",
        "interior-SW",
        "interior-NW",
        "interior-W",
        "interior-S",
    ),
    # The endpoint's own west-wall cells (its squares 1, 2, 3, 4, 9, 10 and 11): W7's
    # falsifier, which shares five of W7's seven cells.
    "endpoint7": (
        "corner-SW",
        "side-S0",
        "side-W0",
        "side-W2",
        "side-N0",
        "corner-NW",
        "interior-W",
    ),
}
CONTROLS = frozenset({"endpoint6", "endpoint7"})
PRODUCER = "sqpack.hull_kernel.producer"
MAX_EVENTS = 200_000


def canonical_bytes(value: Any) -> bytes:
    """The bytes an object is digested and saved as: sorted keys, no spaces, UTF-8."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def _member_bytes(name: str, value: Any) -> bytes:
    return json.dumps(name).encode() + b":" + canonical_bytes(value)


class SpilledSteps:
    """A production's steps on disk, as `produce` appends them (`producer.StepLog`).

    Each step's canonical bytes are one line of a gzipped file, which canonical JSON
    allows since it escapes every newline; a step is appended as a gzip member of its own,
    so no file stays open. Iterating parses the steps back one at a time, and `pieces`
    gives their bytes unparsed to `canonical_pieces`, so a production that saves holds
    the step it is making, not the node.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self._count = 0
        path.unlink(missing_ok=True)

    def append(self, step: dict[str, Any], /) -> None:
        with gzip.open(self.path, "ab", compresslevel=1) as spill:
            _ = spill.write(canonical_bytes(step) + b"\n")
        self._count += 1

    def __len__(self) -> int:
        return self._count

    def pieces(self) -> Iterator[bytes]:
        if not self._count:
            return
        with gzip.open(self.path, "rb") as spill:
            for line in spill:
                yield line.removesuffix(b"\n")

    def __iter__(self) -> Iterator[dict[str, Any]]:
        for piece in self.pieces():
            yield json.loads(piece)


def canonical_pieces(value: dict[str, Any]) -> Iterator[bytes]:
    """`canonical_bytes(value)` in pieces whose concatenation is exactly those bytes: a
    member at a time, and a member `steps` that is a list or `SpilledSteps` a step at a
    time, so that a node is hashed or written without its bytes ever being held whole."""
    if not all(isinstance(name, str) for name in value):
        yield canonical_bytes(value)
        return
    yield b"{"
    for index, name in enumerate(sorted(value)):
        comma = b"," if index else b""
        member = value[name]
        if name == "steps" and isinstance(member, list | SpilledSteps):
            yield comma + b'"steps":['
            steps = (
                member.pieces()
                if isinstance(member, SpilledSteps)
                else map(canonical_bytes, cast("list[Any]", member))
            )
            for position, piece in enumerate(steps):
                yield (b"," if position else b"") + piece
            yield b"]"
        else:
            yield comma + _member_bytes(name, member)
    yield b"}"


def content_sha256(value: Any) -> str:
    """The SHA-256 of `canonical_bytes(value)`, hashed in `canonical_pieces` for a node."""
    if not isinstance(value, dict):
        return hashlib.sha256(canonical_bytes(value)).hexdigest()
    digest = hashlib.sha256()
    for piece in canonical_pieces(cast("dict[str, Any]", value)):
        digest.update(piece)
    return digest.hexdigest()


def save_certificate(
    directory: Path, seed: dict[str, Any], node_object: dict[str, Any]
) -> Path:
    """Write `seed-<sha256>.json.gz` and `node-<sha256>.json.gz` of the canonical bytes,
    and return the node's file.

    Each is gzipped as `gzip.compress(raw, mtime=0)` would, a piece at a time
    (`canonical_pieces`), into a dot-file that is renamed to its content id once written,
    so that a node's bytes are never held whole.
    """
    directory.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for kind, value in (("seed", seed), ("node", node_object)):
        partial = directory / f".{kind}-writing.json.gz"
        digest = hashlib.sha256()
        with (
            partial.open("wb") as raw,
            gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as packed,
        ):
            for piece in canonical_pieces(value):
                digest.update(piece)
                _ = packed.write(piece)
        written.append(partial.replace(directory / f"{kind}-{digest.hexdigest()}.json.gz"))
    return written[1]


def saved_files(directory: Path) -> tuple[Path, Path]:
    """The one saved seed and the one saved node in `directory`."""
    found: list[Path] = []
    for kind in ("seed", "node"):
        matches = sorted(directory.glob(f"{kind}-*.json.gz"))
        if len(matches) != 1:
            raise RefusalError(f"expected exactly one saved {kind} in {directory}")
        found.append(matches[0])
    return found[0], found[1]


def load_certificate(directory: Path) -> tuple[dict[str, Any], dict[str, Any], str, str]:
    """The saved seed and node, and their content ids (`content_sha256`).

    `save_certificate` names each file by its content id; the name is a name, and a file
    is read whatever it is called and however its JSON is spaced. The node names its seed
    by the seed's content id, which the replay's header admission checks. This holds the
    whole node in memory; `check_saved` reads it a step at a time with `stream_node`.
    """
    seed_file, node_file = saved_files(directory)
    seed = json.loads(gzip.decompress(seed_file.read_bytes()))
    node_object = json.loads(gzip.decompress(node_file.read_bytes()))
    return seed, node_object, content_sha256(seed), content_sha256(node_object)


STREAM_CHUNK = 1 << 20
JSON_BLANK = " \t\n\r"
AFTER_VALUE = frozenset(JSON_BLANK + ",:]}")


def gzip_text(path: Path) -> Iterator[str]:
    """The UTF-8 text of a gzipped file, in pieces of `STREAM_CHUNK` bytes or so."""
    utf8 = codecs.getincrementaldecoder("utf-8")()
    with gzip.open(path, "rb") as file:
        while chunk := file.read(STREAM_CHUNK):
            yield utf8.decode(chunk)
    yield utf8.decode(b"", final=True)


class GzipJsonText:
    """The text of a gzipped UTF-8 JSON file, decompressed as it is consumed.

    Values are parsed off the front of a buffer by `json`'s own decoder. A value that runs
    past the buffer is parsed again after at least as much again has been read, so a
    value costs time linear in its length and the buffer holds about the value being read,
    never the file.
    """

    def __init__(self, path: Path) -> None:
        self._pieces = gzip_text(path)
        self._decoder = json.JSONDecoder()
        self._text = ""
        self._at = 0
        self._ended = False

    def _more(self) -> None:
        pieces = [self._text[self._at :]]
        wanted = max(STREAM_CHUNK, len(pieces[0]))
        while wanted > 0 and (piece := next(self._pieces, None)) is not None:
            pieces.append(piece)
            wanted -= len(piece)
        self._ended = wanted > 0
        self._text = "".join(pieces)
        self._at = 0

    def peek(self) -> str:
        """The next character that is not JSON whitespace, or "" at the end of the file."""
        while True:
            while self._at < len(self._text) and self._text[self._at] in JSON_BLANK:
                self._at += 1
            if self._at < len(self._text):
                return self._text[self._at]
            if self._ended:
                return ""
            self._more()

    def take(self, expected: str, message: str) -> str:
        """The next character, consumed; it must be one of `expected`."""
        found = self.peek()
        require(bool(found) and found in expected, message)
        self._at += 1
        return found

    def value(self) -> Any:
        """The next JSON value, parsed whole, as `json.loads` would parse it."""
        _ = self.peek()
        while True:
            try:
                value, end = self._decoder.raw_decode(self._text, self._at)
            except json.JSONDecodeError:
                if self._ended:
                    raise
            else:
                # A number at the buffer's end may continue in the next chunk.
                if self._ended or (end < len(self._text) and self._text[end] in AFTER_VALUE):
                    self._at = end
                    return value
            self._more()


def _member_name(text: GzipJsonText, header: dict[str, Any]) -> str:
    name = text.value()
    require(isinstance(name, str), "a node member's name is a string")
    require(name not in header, f"the saved node repeats its member {name!r}")
    _ = text.take(":", "a node member's name is followed by a colon")
    return name


class SavedSteps:
    """A saved node's `steps`, parsed one at a time as they are iterated, once.

    When the last step has been read, the members after the array are read into the
    node's header and `content_sha256` is set: the SHA-256 of the node's canonical bytes,
    hashed as they are produced, member by member and step by step, in the order
    `canonical_bytes` writes them. So a replay holds one step, and the node is never
    in memory whole.
    """

    def __init__(self, text: GzipJsonText, header: dict[str, Any]) -> None:
        self._text = text
        self._header = header
        self._digest = hashlib.sha256(b"{")
        for name in sorted(name for name in header if name < "steps"):
            self._digest.update(_member_bytes(name, header[name]) + b",")
        self._digest.update(b'"steps":[')
        self._started = False
        self._count = 0
        self.content_sha256: str | None = None

    def __bool__(self) -> bool:
        """Whether there is a step, decided without reading one."""
        return self._count > 0 if self._started else self._text.peek() != "]"

    def __iter__(self) -> Iterator[dict[str, Any]]:
        require(not self._started, "a saved node's steps are read once")
        self._started = True
        text = self._text
        separator = "," if text.peek() != "]" else text.take("]", "an empty steps array")
        while separator == ",":
            step = text.value()
            self._digest.update((b"," if self._count else b"") + canonical_bytes(step))
            self._count += 1
            yield step
            separator = text.take(",]", "a node's steps are separated by commas")
        self._digest.update(b"]")
        while text.take(",}", "a node's members are separated by commas") == ",":
            name = _member_name(text, self._header)
            require(name > "steps", f"the node member {name!r} follows the steps")
            self._header[name] = text.value()
        require(text.peek() == "", "data follows the saved node")
        for name in sorted(name for name in self._header if name > "steps"):
            self._digest.update(b"," + _member_bytes(name, self._header[name]))
        self._digest.update(b"}")
        self.content_sha256 = self._digest.hexdigest()


def stream_node(path: Path) -> tuple[dict[str, Any], SavedSteps]:
    """A saved node whose `steps` are read as a replay reaches them (`SavedSteps`).

    The members before `steps` are parsed whole into the returned header, whose `steps`
    is the `SavedSteps`. Every member that sorts before `steps` must come before it, as in
    the canonical bytes `save_certificate` writes, so that the header is complete before
    the first step is checked; spacing is free, as for `json.loads`. A repeated member, or
    a node without `steps`, is refused.
    """
    text = GzipJsonText(path)
    _ = text.take("{", "a saved node is a JSON object")
    header: dict[str, Any] = {}
    if text.peek() != "}":
        while True:
            name = _member_name(text, header)
            if name == "steps":
                _ = text.take("[", "a node's steps are an array")
                steps = SavedSteps(text, header)
                header[name] = steps
                return header, steps
            header[name] = text.value()
            if text.take(",}", "a node's members are separated by commas") == "}":
                break
    raise RefusalError("the saved node has no steps")


def checker_modules() -> dict[str, str]:
    """SHA-256 of every `sqpack.hull_kernel` module this process has imported."""
    digests: dict[str, str] = {}
    for name, module in sorted(sys.modules.items()):
        location = getattr(module, "__file__", None)
        if name.startswith("sqpack.hull_kernel") and location:
            digests[name] = hashlib.sha256(Path(location).read_bytes()).hexdigest()
    return digests


def check_saved(
    directory: Path,
    frame: Frame | None = None,
    *,
    max_seconds: float = 3600.0,
    require_no_producer: bool = True,
    cover: str = "indexed",
) -> dict[str, Any]:
    """Certify saved objects with the checker alone: seed admission, the sequential
    replay and the transfer. The producer is never imported; with `require_no_producer`
    its absence from `sys.modules` is asserted before and after the check. `cover` names
    the row-cover sweep (`sequential.COVERS`); the indexed and reference forms prove the
    same cover and report the same events and probes. The node is read a step at a time
    (`stream_node`), so the check holds one step of it, and its content id is taken as it
    is read."""
    if require_no_producer and PRODUCER in sys.modules:
        raise RefusalError("the producer is loaded; a saved check must run without it")
    started = time.monotonic()
    seed_file, node_file = saved_files(directory)
    seed = json.loads(gzip.decompress(seed_file.read_bytes()))
    seed_sha = content_sha256(seed)
    node_object, steps = stream_node(node_file)
    frame = frame if frame is not None else mask0_tool.n17_unique_frame()
    mask = node_object["mask"]
    bins = seed["bins"]
    budget = Budget(started + max_seconds, MAX_EVENTS)
    seed_state = node.admit_seed(
        frame, seed, mask=mask, bins=bins, budget=budget, allow_empty_groups=True
    )
    trace = sequential.replay_sequential(
        frame,
        node_object,
        seed_state,
        mask=mask,
        seed_sha256=seed_sha,
        budget=budget,
        cover=cover,
    )
    if require_no_producer and PRODUCER in sys.modules:
        raise RefusalError("the producer was imported during a saved check")
    node_sha = steps.content_sha256
    require(node_sha is not None, "the replay did not read the saved node to its end")
    closed = trace.closure is not None
    result: dict[str, Any] = {
        "status": "PASS_SAVED_CLOSED" if closed else "PASS_SAVED_STALL",
        "frame": frame.name,
        "cells": [frame.cell_names[owner] for owner in mask],
        "mask": mask,
        "bins": bins,
        "cover_backend": cover,
        "rational_backend": BACKEND,
        "seed_sha256": seed_sha,
        "node_sha256": node_sha,
        "closure": trace.closure,
        "steps_checked": len(trace.steps),
        "rows_checked": sum(step["rows"] for step in trace.steps),
        "events": sum(step["events"] for step in trace.steps),
        "collision_regions": sum(step.get("collision_regions", 0) for step in trace.steps),
        "producer_imported": PRODUCER in sys.modules,
        "checker_modules_sha256": checker_modules(),
        "check_seconds": time.monotonic() - started,
    }
    excluded = frame.states_containing(mask) if closed else []
    result["excluded_orbits"] = len(excluded)
    result["excluded_states"] = sum(
        orbit_size(frame, frame.representatives[index]) for index in excluded
    )
    return result


def orbit_size(frame: Frame, state: tuple[int, ...]) -> int:
    return len({frame.image(action, state) for action in frame.actions})


def run(
    frame: Frame,
    cells: tuple[str, ...],
    *,
    name: str,
    bins: int,
    max_rounds: int,
    max_seconds: float,
    cover: str,
    collision: bool = True,
    hull_limit: int | None = 16,
    producer_share: float = 0.5,
    save_objects: Path | None = None,
    core: str = "envelope",
    split: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Produce, save if asked, then certify with the checker. `split` (keys `floor`,
    `max_rows`, `patience`) turns on the producer's adaptive rows; without it the rows
    stay the seed's uniform bins and nothing in the output changes. With `save_objects`
    the steps go to disk as they are made (`SpilledSteps`) and the check reads the saved
    node a step at a time, so the process never holds the node; without it the node is
    kept and checked in memory."""
    producer = importlib.import_module(PRODUCER)
    started = time.monotonic()
    mask = sorted(frame.cell_names.index(cell) for cell in cells)
    budget = Budget(started + max_seconds, MAX_EVENTS)
    spill = None
    if save_objects is not None:
        # A run that saves keeps its steps on disk until the save, never in memory.
        save_objects.mkdir(parents=True, exist_ok=True)
        spill = SpilledSteps(save_objects / ".steps-spill.json.gz")
    production = producer.produce(
        frame,
        mask,
        bins=bins,
        max_rounds=max_rounds,
        budget=budget,
        node_id=f"n17-{name}",
        collision=collision,
        hull_limit=hull_limit,
        stop_at=started + max_seconds * producer_share,
        core=core,
        split=None if split is None else producer.SplitPolicy(**split),
        step_log=spill,
        progress=lambda event: print(
            json.dumps({**event, "seconds": round(time.monotonic() - started, 1)}),
            file=sys.stderr,
            flush=True,
        ),
    )
    produced = time.monotonic()
    finest_row = (
        None
        if split is None
        else str(
            min(
                Q(row["interval"][1]) - Q(row["interval"][0])
                for step in production.node["steps"]
                for row in step["rows"]
            )
        )
    )
    source, saved_steps = production.node, None
    if save_objects is not None:
        # Saved before checking, so a check the ceiling cuts short can be finished later
        # with --check-saved; saved objects claim nothing until a check passes on them.
        # The check then reads the saved node a step at a time, as --check-saved does,
        # and the produced node is let go, so that the process does not hold it twice.
        saved = save_certificate(save_objects, production.seed, production.node)
        source, saved_steps = stream_node(saved)
        production.node = {}
        if spill is not None:
            spill.path.unlink()
    seed = node.admit_seed(
        frame, production.seed, mask=mask, bins=bins, budget=budget, allow_empty_groups=True
    )
    trace = sequential.replay_sequential(
        frame,
        source,
        seed,
        mask=mask,
        seed_sha256=content_sha256(production.seed),
        budget=budget,
        cover=cover,
    )
    node_sha = content_sha256(source) if saved_steps is None else saved_steps.content_sha256
    require(node_sha is not None, "the replay did not read the saved node to its end")
    checked = time.monotonic()
    closed = trace.closure is not None
    result: dict[str, Any] = {
        "pattern": name,
        "cells": list(cells),
        "mask": mask,
        "bins": bins,
        "max_rounds": max_rounds,
        "cover_backend": cover,
        "rational_backend": BACKEND,
        "collision_regions": collision,
        "hull_limit": hull_limit,
        "producer_share": producer_share,
        "core": core,
        "producer_outcome": production.outcome,
        "certified": "closed" if closed else "stalled",
        "closure": trace.closure,
        "seed_points": {
            frame.cell_names[owner]: len(production.seed["groups"][str(owner)])
            for owner in mask
        },
        "steps_checked": len(trace.steps),
        "rows_checked": sum(step["rows"] for step in trace.steps),
        "events": sum(step["events"] for step in trace.steps),
        "probes": sum(step["probes"] for step in trace.steps),
        "steps": trace.steps,
        "rounds": [
            {
                "round": entry["round"],
                "steps": entry["steps"],
                "live_rows": {e["cell"]: e["live_rows"] for e in entry["extents"]},
                "residual_box_extent": {
                    e["cell"]: e["residual_box_extent"] for e in entry["extents"]
                },
                "owned_hull_vertices": {
                    e["cell"]: e["owned_hull_vertices"] for e in entry["extents"]
                },
            }
            | (
                {}
                if split is None
                else {
                    "rows": {e["cell"]: e["rows"] for e in entry["extents"]},
                    "splits": entry.get("splits"),
                    "planned_rows": entry.get("planned_rows"),
                }
            )
            for entry in production.rounds
        ],
        "final_extents": trace.extents,
        "node_sha256": node_sha,
        "seed_sha256": content_sha256(production.seed),
        "producer_seconds": produced - started,
        "checker_seconds": checked - produced,
    }
    if split is not None:
        result["split"] = dict(split)
        result["finest_row"] = finest_row
    if closed:
        excluded = frame.states_containing(mask)
        result["excluded_orbits"] = len(excluded)
        result["excluded_states"] = sum(
            orbit_size(frame, frame.representatives[index]) for index in excluded
        )
    else:
        result["excluded_orbits"] = 0
        result["excluded_states"] = 0
    if name in CONTROLS:
        result["control"] = "an endpoint sub-pattern must stall"
        result["status"] = "REFUSED_CONTROL_CLOSED" if closed else "PASS_CONTROL_STALLED"
    else:
        result["status"] = "PASS_CERTIFIED_CLOSED" if closed else "PASS_CERTIFIED_STALL"
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pattern", choices=sorted(PATTERNS), default="A")
    parser.add_argument("--cells", nargs="+", help="cell names, in place of --pattern")
    parser.add_argument("--bins", type=int, default=64)
    parser.add_argument("--max-rounds", type=int, default=6)
    parser.add_argument("--cover", choices=sorted(sequential.COVERS), default="indexed")
    parser.add_argument("--max-seconds", type=float, default=1800.0)
    parser.add_argument("--no-collision", action="store_true", help="no partner collisions")
    parser.add_argument("--hull-limit", type=int, default=16, help="0 keeps every vertex")
    parser.add_argument(
        "--save-objects", type=Path, help="write the certified seed and node here, gzipped"
    )
    parser.add_argument(
        "--producer-share",
        type=float,
        default=0.5,
        help="the share of the wall ceiling after which the producer starts no new step",
    )
    parser.add_argument(
        "--core",
        choices=("envelope", "octagon"),
        default="envelope",
        help="the producer's strict core: the midpoint envelope square or the end octagon",
    )
    parser.add_argument(
        "--split-floor",
        type=int,
        default=0,
        help="adaptive rows: bisect stuck rows down to 1/N in t (0, the default, is off)",
    )
    parser.add_argument(
        "--max-rows", type=int, default=0, help="with --split-floor: rows over all owners"
    )
    parser.add_argument(
        "--split-patience",
        type=int,
        default=1,
        help="with --split-floor: rounds a row must stay unshrunk before it is split",
    )
    parser.add_argument(
        "--check-saved",
        type=Path,
        help="certify a saved seed and node with the checker alone; nothing is produced",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("the wall ceiling must be positive and finite")
    if args.bins <= 0 or args.max_rounds <= 0:
        parser.error("bins and rounds must be positive")
    if not 0 < args.producer_share < 1:
        parser.error("the producer share must lie in (0, 1)")
    if args.split_floor < 0 or (
        args.split_floor and (args.max_rows <= 0 or args.split_patience <= 0)
    ):
        parser.error("--split-floor needs a positive --max-rows and --split-patience")
    name = "custom" if args.cells else args.pattern
    cells = tuple(args.cells) if args.cells else PATTERNS[args.pattern]
    start, cpu = time.monotonic(), time.process_time()
    if args.check_saved is not None:
        try:
            result = check_saved(
                args.check_saved, max_seconds=args.max_seconds, cover=args.cover
            )
        except IncompleteError as error:
            result = {"status": "INCOMPLETE", "reason": str(error), "excluded_orbits": 0}
        except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
            result = {"status": "REFUSED", "reason": str(error), "excluded_orbits": 0}
        result.update(
            provenance=provenance(Path(__file__)),
            wall_seconds=time.monotonic() - start,
            process_cpu_seconds=time.process_time() - cpu,
        )
        encoded = json.dumps(result, indent=2, sort_keys=True, default=str) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(encoded, encoding="utf-8")
        print(encoded, end="")
        return 0 if str(result["status"]).startswith("PASS") else 2
    try:
        frame = mask0_tool.n17_unique_frame()
        result = run(
            frame,
            cells,
            name=name,
            bins=args.bins,
            max_rounds=args.max_rounds,
            max_seconds=args.max_seconds,
            cover=args.cover,
            collision=not args.no_collision,
            hull_limit=args.hull_limit or None,
            producer_share=args.producer_share,
            save_objects=args.save_objects,
            core=args.core,
            split=(
                {
                    "floor": args.split_floor,
                    "max_rows": args.max_rows,
                    "patience": args.split_patience,
                }
                if args.split_floor
                else None
            ),
        )
    except IncompleteError as error:
        result = {"status": "INCOMPLETE", "reason": str(error), "excluded_orbits": 0}
    except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
        result = {"status": "REFUSED", "reason": str(error), "excluded_orbits": 0}
    result.update(
        provenance=provenance(Path(__file__), *sorted(Path(node.__file__).parent.glob("*.py"))),
        wall_seconds=time.monotonic() - start,
        process_cpu_seconds=time.process_time() - cpu,
        wall_ceiling_seconds=args.max_seconds,
    )
    encoded = json.dumps(result, indent=2, sort_keys=True, default=str) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    summary = {
        key: result.get(key)
        for key in (
            "status",
            "pattern",
            "certified",
            "producer_outcome",
            "closure",
            "excluded_orbits",
            "excluded_states",
            "steps_checked",
            "rows_checked",
            "rounds",
            "reason",
            "wall_seconds",
        )
    }
    print(json.dumps(summary, indent=1, sort_keys=True, default=str))
    return 0 if str(result["status"]).startswith("PASS") else 2


if __name__ == "__main__":
    sys.exit(main())
