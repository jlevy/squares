#!/usr/bin/env python3
"""Check the retired prospective atlas seed record.

Until 2026-09-07 this module built the collection's license-safe seed: 101 normalized
`Witness/v2` records and 101 house renderings for the exact-grid and UnitSquare cases of
`n = 101..324`, indexed by `atlas/prospective/manifest.json`. The known-best atlas now
retains one construction and one house rendering for every `n` in that range under the
same retention policy, so the seed indexed nothing its successor does not carry, and two
collections drawing the same cases from the same sources is two things to keep in step
for no reader's benefit. The witnesses and renderings were removed and the manifest
replaced by a retirement record pointing at `atlas/known-best/manifest.json`.

What is left here is the check that the retirement stayed true: the record validates,
its pointer resolves, the source-availability map it names is still present, and no seed
witness or rendering has come back. `--update` refuses rather than rebuilds, because
rebuilding is what `devtools.build_known_best_atlas` does now.

The four retained UnitSquare SVGs under `resources/web/prospective-packings/unitsquare/`
are not part of the retirement. They stay where they are, and `build_known_best_atlas`
reads them there and fetches them with its own `--fetch`, which is why this tool no
longer carries one.

Usage:
    uv run --frozen python -m devtools.build_prospective_atlas --check
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from jsonschema_rs import Draft202012Validator

from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY_ROOT = ROOT.parent
SOURCE_MAP = ROOT / "atlas/prospective/source-availability-101-324.json"
WITNESS_ROOT = ROOT / "witnesses/prospective"
ATLAS_ROOT = ROOT / "atlas/prospective"
RENDER_ROOT = ATLAS_ROOT / "rendering"
MANIFEST = ATLAS_ROOT / "manifest.json"
SCHEMA = ATLAS_ROOT / "prospective-atlas-seed.schema.yaml"
GENERATOR = "python -m devtools.build_prospective_atlas"
SUCCESSOR = "devtools.build_known_best_atlas"
RETIRED_STATUS = "retired-2026-09-07"


def _relative(path: Path) -> str:
    """Repository-relative where that means anything, absolute where it does not.

    A caller that repoints a root -- the test that puts a seed file back does -- names a
    directory outside the checkout, and `relative_to` raises on one. Reporting a
    returned file by an absolute path is right there; failing to report it is not.
    """
    if path.is_relative_to(REPOSITORY_ROOT):
        return path.relative_to(REPOSITORY_ROOT).as_posix()
    return path.as_posix()


def retired_record() -> dict:
    """The `atlas_seed` envelope of the retirement record."""
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    metadata = document.get("softschema", {})
    declared = metadata.get("schema")
    if declared != SCHEMA.name:
        raise ValueError(
            f"{_relative(MANIFEST)} declares schema {declared!r}, expected {SCHEMA.name!r}"
        )
    envelope = metadata.get("envelope")
    if envelope != "atlas_seed":
        raise ValueError(
            f"{_relative(MANIFEST)} declares envelope {envelope!r}, expected 'atlas_seed'"
        )
    return document[envelope]


def retirement_errors(record: dict) -> list[str]:
    """Return what the schema cannot say about a retirement record.

    The schema pins the shape and every constant in it. What it cannot do is look
    outside the file: whether the successor it names and the source map it keeps are
    really there, and whether the removed seed has come back. Each of those is the way
    this retirement could quietly stop being true.
    """
    errors: list[str] = []
    validator = Draft202012Validator(load_yaml(SCHEMA.read_text(encoding="utf-8")))
    for failure in sorted(
        validator.iter_errors(record), key=lambda item: list(item.instance_path)
    ):
        location = "/".join(str(part) for part in failure.instance_path) or "<root>"
        errors.append(f"{location}: {failure.message}")
    if errors:
        return errors

    if record["generated_by"] != GENERATOR:
        errors.append(f"generated_by is {record['generated_by']!r}, expected {GENERATOR!r}")
    if record["status"] != RETIRED_STATUS:
        errors.append(f"status is {record['status']!r}, expected {RETIRED_STATUS!r}")
    if record["status"] != f"retired-{record['retired_on']}":
        errors.append("status and retired_on disagree about the retirement date")
    # The two roots differ because the two paths do, and both spellings are the ones
    # their own collections use: the known-best manifest indexes itself packing-relative,
    # and the seed named its source map repository-relative from the day it was written.
    # Resolving each the way its writer meant it is what keeps this a check rather than a
    # coincidence.
    successor = ROOT / record["superseded_by"]["path"]
    if not successor.is_file():
        errors.append(f"successor manifest does not exist: {record['superseded_by']['path']}")
    source_map = REPOSITORY_ROOT / record["source_map"]["path"]
    if source_map != SOURCE_MAP:
        errors.append(f"source map is not this collection's: {record['source_map']['path']}")
    elif not source_map.is_file():
        errors.append(f"source map does not exist: {record['source_map']['path']}")
    if record["entries"]:
        errors.append(
            f"a retired seed indexes nothing, and this one indexes {len(record['entries'])}"
        )
    return errors


def returned_seed_files() -> list[str]:
    """Seed witnesses or house renderings that exist again under the retired roots."""
    returned = list(WITNESS_ROOT.glob("*.yaml"))
    returned.extend(RENDER_ROOT.glob("*.svg"))
    return sorted(_relative(path) for path in returned)


def update() -> None:
    """Refuse, in the words a caller reaching for `--update` needs to read.

    `SystemExit` rather than `ValueError`: this is a refusal and not a failure, and a
    traceback over a decision reads as a crash. Drift found by `check` still raises,
    because there the stack is where the drift is.
    """
    raise SystemExit(
        "the prospective atlas seed was retired on 2026-09-07 and is not rebuilt: "
        f"{_relative(MANIFEST)} points at atlas/known-best/manifest.json, and the "
        f"witnesses and house renderings for n=101..324 are built by {SUCCESSOR} "
        "--update. Retiring the retirement, if the collection is ever wanted back, is "
        "an edit to that record and to its schema's seed shape, not a run of this tool."
    )


def check() -> None:
    record = retired_record()
    problems = retirement_errors(record)
    problems.extend(f"retired seed file is back: {name}" for name in returned_seed_files())
    if problems:
        raise ValueError("prospective atlas seed drift:\n  " + "\n  ".join(problems[:20]))
    # The counts are read from the record rather than written here, and they are zero:
    # what this collection retains is what the line reports, in the same words it used
    # when there were 101 of each. A consumer counting the seed's entries reads the
    # retirement correctly instead of failing on a missing field.
    retained = len(record["entries"])
    print(
        f"prospective atlas seed check passed: {retained} witnesses and "
        f"{retained} house renderings retained; retired {record['retired_on']}, "
        f"superseded by {record['superseded_by']['path']}"
    )


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.update:
        update()
    else:
        check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
