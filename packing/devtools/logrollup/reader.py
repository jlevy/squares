"""The reader interface every harness plugs into, and the registry that picks one.

Systematic across harnesses: detection, the shared record shape, and the emit path.
Customised per harness: everything a reader does between opening the file and filling in
`SessionRollup.extra`.

A reader is registered rather than imported at the call site so that adding a harness is
one module and one line, and so that no consumer has to know which harnesses exist.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

from devtools.logrollup.model import SessionRollup


@runtime_checkable
class HarnessReader(Protocol):
    """One harness's transcript reader."""

    @property
    def harness(self) -> str:
        """The harness name this reader speaks for, and its key in the registry.

        A read-only property rather than a mutable attribute so a frozen reader
        satisfies the protocol; a reader that could be renamed after registration would
        make the registry's uniqueness check meaningless.
        """
        ...

    def detects(self, path: Path) -> bool:
        """Whether this reader recognises the file as its own harness's log.

        Detection reads the file rather than trusting its name, because a transcript
        that has been copied or renamed is still that harness's transcript.
        """
        ...

    def read(self, path: Path) -> SessionRollup:
        """The rollup for one log this reader has already detected."""
        ...


@dataclass(frozen=True, slots=True)
class Registry:
    """The readers this build knows about, in detection order."""

    readers: tuple[HarnessReader, ...]

    def __iter__(self) -> Iterator[HarnessReader]:
        return iter(self.readers)

    @property
    def harnesses(self) -> tuple[str, ...]:
        return tuple(reader.harness for reader in self.readers)

    def for_path(self, path: Path) -> HarnessReader:
        """The one reader that recognises this log.

        An ambiguous log is an error rather than a first-match: two harnesses claiming
        one transcript means a detector is too loose, and silently picking one would
        produce a record attributed to the wrong agent.
        """
        matched = [reader for reader in self.readers if reader.detects(path)]
        if not matched:
            known = ", ".join(self.harnesses)
            raise LookupError(f"{path.name}: no reader recognises this log (known: {known})")
        if len(matched) > 1:
            claimed = ", ".join(reader.harness for reader in matched)
            raise LookupError(f"{path.name}: claimed by more than one reader ({claimed})")
        return matched[0]


def build_registry(readers: Sequence[HarnessReader]) -> Registry:
    """A registry with no two readers claiming the same harness name."""
    names = [reader.harness for reader in readers]
    duplicated = {name for name in names if names.count(name) > 1}
    if duplicated:
        raise ValueError(f"duplicate harness names in registry: {sorted(duplicated)}")
    return Registry(readers=tuple(readers))
