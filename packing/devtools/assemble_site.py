"""Merge built producer trees, accepting identical shared assets and refusing collisions.

Preflight examines every file before writing anything. Publication uses atomic file
replacement; symlinks and overlapping source/destination trees are refused.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from kpress.output import write_bytes_atomic


def assemble(destination: Path, sources: Sequence[Path]) -> int:
    """Copy validated producer files into a site without overwriting different bytes."""
    if destination.is_symlink():
        raise ValueError(f"publication symlink is not a real directory: {destination}")
    destination = destination.resolve()
    planned: dict[Path, Path] = {}
    if not sources:
        raise ValueError("at least one producer tree is required")
    for producer in sources:
        if producer.is_symlink() or not producer.is_dir():
            raise ValueError(f"not a producer directory: {producer}")
        source = producer.resolve()
        if source.is_relative_to(destination) or destination.is_relative_to(source):
            raise ValueError("producer and publication directories overlap")
        files = 0
        for path in sorted(source.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"producer symlink is not publishable: {path}")
            if not path.is_file():
                continue
            files += 1
            target = destination / path.relative_to(source)
            if any(
                parent.is_symlink() or (parent.exists() and not parent.is_dir())
                for parent in target.parents
                if parent.is_relative_to(destination)
            ):
                raise ValueError(f"publication path is not a real directory: {target}")
            prior = planned.get(
                target, target if target.exists() or target.is_symlink() else None
            )
            if prior is not None:
                if (
                    prior.is_symlink()
                    or not prior.is_file()
                    or prior.read_bytes() != path.read_bytes()
                ):
                    raise ValueError(
                        f"publication collision: {target.relative_to(destination)}"
                    )
            else:
                planned[target] = path
        if not files:
            raise ValueError(f"empty producer tree: {source}")
    for target in planned:
        if any(parent in planned for parent in target.parents):
            raise ValueError(
                f"publication file/directory collision: {target.relative_to(destination)}"
            )
    for target, source in sorted(planned.items()):
        target.parent.mkdir(parents=True, exist_ok=True)
        write_bytes_atomic(target, source.read_bytes())
    return len(planned)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("sources", nargs="+", type=Path)
    args = parser.parse_args(argv)
    try:
        count = assemble(args.destination, args.sources)
    except (OSError, ValueError) as error:
        print(f"site assembly failed: {error}", file=sys.stderr)
        return 1
    print(f"assembled {count} new files into {args.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
