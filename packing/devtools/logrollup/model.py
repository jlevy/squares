"""The vocabulary every harness reader shares.

A rollup has two halves. This half is systematic: what a session log *is*, regardless of
which agent wrote it -- a source file, a time span, a set of turns, a set of tool calls,
and a statement of what each figure may be read as. The other half is whatever a
particular harness knows that the others do not, which each reader supplies in its own
terms through `extra`.

Everything here is a frozen dataclass rather than a dictionary, because these values are
read back out of a checked-in record months later, and a field name that is only ever a
string key is a field name nothing catches when it drifts.
"""

from __future__ import annotations

import hashlib
import statistics
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Self

SECONDS_PER_HOUR = 3600.0


def instant(value: object) -> float | None:
    """Seconds since the epoch for one ISO-8601 timestamp, or None if it is not one."""
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value).timestamp()
    except ValueError:
        return None


@dataclass(frozen=True, slots=True)
class Elapsed:
    """Count and distribution for one set of durations."""

    count: int
    total_seconds: float
    median_seconds: float | None = None
    max_seconds: float | None = None

    @classmethod
    def of(cls, seconds: Sequence[float]) -> Self:
        if not seconds:
            return cls(count=0, total_seconds=0.0)
        return cls(
            count=len(seconds),
            total_seconds=round(sum(seconds), 3),
            median_seconds=round(statistics.median(seconds), 3),
            max_seconds=round(max(seconds), 3),
        )

    def payload(self) -> dict[str, Any]:
        counted: dict[str, Any] = {"count": self.count, "total_seconds": self.total_seconds}
        if self.median_seconds is not None:
            counted["median_seconds"] = self.median_seconds
        if self.max_seconds is not None:
            counted["max_seconds"] = self.max_seconds
        return counted


@dataclass(frozen=True, slots=True)
class SourceLog:
    """The log a rollup was built from, identified well enough to outlive it.

    The log itself is not retained, so `sha256` is what lets a later reader tell whether
    two records describe the same transcript.
    """

    harness: str
    filename: str
    sha256: str
    bytes: int
    records: int
    session_id: str
    harness_versions: tuple[str, ...]

    @classmethod
    def of(cls, path: Path, *, harness: str, records: Sequence[Mapping[str, Any]]) -> Self:
        raw = path.read_bytes()
        return cls(
            harness=harness,
            filename=path.name,
            sha256=hashlib.sha256(raw).hexdigest(),
            bytes=len(raw),
            records=len(records),
            session_id=str(next((r["sessionId"] for r in records if r.get("sessionId")), "")),
            harness_versions=tuple(
                sorted({str(r["version"]) for r in records if r.get("version")})
            ),
        )

    def payload(self) -> dict[str, Any]:
        return {
            "harness": self.harness,
            "filename": self.filename,
            "sha256": self.sha256,
            "bytes": self.bytes,
            "records": self.records,
            "session_id": self.session_id,
            "harness_versions": list(self.harness_versions),
        }


@dataclass(frozen=True, slots=True)
class Span:
    """First to last timestamped record."""

    started_at: str | None
    ended_at: str | None
    wall_seconds: float

    @classmethod
    def of(cls, records: Sequence[Mapping[str, Any]]) -> Self:
        stamped = [
            (str(r["timestamp"]), moment)
            for r in records
            if (moment := instant(r.get("timestamp"))) is not None
        ]
        if not stamped:
            return cls(started_at=None, ended_at=None, wall_seconds=0.0)
        first = min(stamped, key=lambda pair: pair[1])
        last = max(stamped, key=lambda pair: pair[1])
        return cls(
            started_at=first[0],
            ended_at=last[0],
            wall_seconds=round(last[1] - first[1], 3),
        )

    @property
    def hours(self) -> float:
        return self.wall_seconds / SECONDS_PER_HOUR

    def payload(self) -> dict[str, Any]:
        return {
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "wall_seconds": self.wall_seconds,
        }


@dataclass(frozen=True, slots=True)
class ToolCall:
    """One completed tool call, reduced to identity and cost.

    `command`, `family` and `shape` are structural: none carries an argument value, a
    path beyond a script's own basename, or a literal out of the command. Nothing
    reconstructs a command line from a rollup.
    """

    tool: str
    seconds: float
    thinking_level: str
    command: str | None = None
    family: str | None = None
    shape: str | None = None


@dataclass(frozen=True, slots=True)
class Turn:
    """One model turn and what the harness reported about it."""

    model: str
    thinking_level: str
    branch: str
    sidechain: bool
    tokens: Mapping[str, int]
    latency_seconds: float | None


@dataclass(frozen=True, slots=True)
class SessionRollup:
    """One harness session, in the shared shape plus that harness's own detail.

    `semantics` is not optional and not decoration. These records outlive the logs they
    came from, so a figure whose meaning is not carried beside it gets read as whatever
    the reader assumes. A measurement a harness cannot supply is named here and omitted
    from the data rather than defaulted to zero: a zero will be summed with a harness
    that does report it, and the total will be wrong in the flattering direction.
    """

    contract: str
    schema: str
    source: SourceLog
    span: Span
    semantics: Mapping[str, str]
    extra: Mapping[str, Any] = field(default_factory=dict)
    envelope: str = "rollup"

    def payload(self) -> dict[str, Any]:
        if not self.semantics:
            raise ValueError(f"{self.contract}: a rollup must state its own semantics")
        return {
            "softschema": {
                "contract": self.contract,
                "schema": self.schema,
                "envelope": self.envelope,
                "status": "enforced",
            },
            self.envelope: {
                "source": self.source.payload(),
                "span": self.span.payload(),
                **dict(self.extra),
                "semantics": dict(self.semantics),
            },
        }
