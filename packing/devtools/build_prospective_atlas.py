#!/usr/bin/env python3
"""Acquire and build the annotation-free 101-case prospective atlas seed.

Usage:
    uv run --frozen python -m devtools.build_prospective_atlas --update
    uv run --frozen python -m devtools.build_prospective_atlas --check
    uv run --frozen python -m devtools.build_prospective_atlas --check --jobs 4
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import time
import urllib.error
import urllib.request
from collections.abc import Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from functools import cache
from pathlib import Path

from strif import atomic_output_file

from devtools.build_known_best_atlas import frame_from_witness
from devtools.map_prospective_sources import availability_errors
from sqpack.known_best import (
    exact_grid_witness,
    parse_unitsquare_svg,
    unitsquare_witness,
)
from sqpack.render import render_packing_svg
from sqpack.render.model import RenderSpec
from sqpack.witness import check_witness_semantics, witness_document
from sqpack.workers import worker_count

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY_ROOT = ROOT.parent
SOURCE_MAP = ROOT / "atlas/prospective/source-availability-101-324.json"
SOURCE_ROOT = ROOT / "resources/web/prospective-packings/unitsquare"
WITNESS_ROOT = ROOT / "witnesses/prospective"
ATLAS_ROOT = ROOT / "atlas/prospective"
RENDER_ROOT = ATLAS_ROOT / "rendering"
MANIFEST = ATLAS_ROOT / "manifest.json"
GENERATOR = "python -m devtools.build_prospective_atlas"
RETRIEVED = "2026-08-26"
USER_AGENT = "thinking-scratchpad-prospective-atlas/1.0"


def _relative(path: Path) -> str:
    return path.relative_to(REPOSITORY_ROOT).as_posix()


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _availability() -> dict:
    document = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))
    availability = document["availability"]
    errors = availability_errors(availability)
    if errors:
        raise ValueError("prospective source map is invalid: " + "; ".join(errors))
    return availability


def eligible_entries() -> list[dict]:
    """Return exactly the generated or CC-identified source-map entries."""
    entries = [
        entry
        for entry in _availability()["entries"]
        if entry["source_key"] in {"catalogue-trivial-grid-rule", "unitsquare-release-1"}
    ]
    if len(entries) != 101:
        raise ValueError(f"safe prospective seed must contain 101 cases, got {len(entries)}")
    return entries


def seed_errors(seed: dict) -> list[str]:
    """Return manifest cross-field errors outside the schema's reach."""
    errors: list[str] = []
    selected = eligible_entries()
    selected_by_n = {entry["n"]: entry for entry in selected}
    expected_numbers = [entry["n"] for entry in selected]
    entries = seed["entries"]
    numbers = [entry["n"] for entry in entries]
    if numbers != expected_numbers:
        errors.append("manifest entries differ from the frozen safe source selection")

    source_counts = {"exact-generated-grid": 0, "unitsquare-rendering": 0}
    for entry in entries:
        n = entry["n"]
        kind = entry["source"].get("kind")
        if kind not in source_counts:
            errors.append(f"n={n}: excluded source kind entered the seed")
        else:
            source_counts[kind] += 1
        if entry["annotation_status"] != "prohibited-uncomputed":
            errors.append(f"n={n}: annotation status is not prohibited-uncomputed")
        if entry["witness"]["id"] != f"W-prospective-source-n{n:03d}":
            errors.append(f"n={n}: witness identity is aliased or inconsistent")
        if entry["witness"]["path"] != f"witnesses/prospective/n-{n:03d}.yaml":
            errors.append(f"n={n}: witness path is inconsistent")
        if entry["rendering"]["path"] != f"atlas/prospective/rendering/n-{n:03d}.svg":
            errors.append(f"n={n}: rendering path is inconsistent")
    if source_counts != {"exact-generated-grid": 97, "unitsquare-rendering": 4}:
        errors.append("manifest source counts differ from the 97/4 selection")

    retained = seed["retained_sources"]
    if [source["n"] for source in retained] != [103, 105, 110, 131]:
        errors.append("retained UnitSquare source identities are incomplete or reordered")
    retained_by_n = {source["n"]: source for source in retained}
    for entry in entries:
        if entry["source"].get("kind") != "unitsquare-rendering":
            continue
        selection = selected_by_n.get(entry["n"])
        if selection is None or selection["source_key"] != "unitsquare-release-1":
            errors.append(f"n={entry['n']}: UnitSquare source is not in the selection")
            continue
        expected_path = _relative(_source_path(selection))
        source = retained_by_n.get(entry["n"])
        if source is None or source["path"] != expected_path:
            errors.append(f"n={entry['n']}: retained source path is missing or inconsistent")
        if entry["source"].get("path") != expected_path:
            errors.append(f"n={entry['n']}: entry source path is inconsistent")
        if entry["source"].get("url") != selection["source_url"]:
            errors.append(f"n={entry['n']}: entry source URL is inconsistent")

    if seed["source_map"] != {"path": _relative(SOURCE_MAP)}:
        errors.append("source-map path differs from the selected input")
    if seed["excluded"].get("source_key") != "kingbird-current-catalogue":
        errors.append("excluded Kingbird source class is missing")
    return errors


def _source_path(entry: dict) -> Path:
    if entry["source_key"] != "unitsquare-release-1":
        raise ValueError(f"n={entry['n']}: generated grid has no retained source path")
    return SOURCE_ROOT / f"n{entry['n']:03d}.svg"


def _check_unitsquare_acquisition(entry: dict, content: bytes) -> None:
    """Check SVG bytes against the digest independently declared by UnitSquare."""
    actual_sha256 = _sha256_bytes(content)
    expected_sha256 = entry["upstream_declared_sha256"]
    if actual_sha256 != expected_sha256:
        raise ValueError(
            f"n={entry['n']}: UnitSquare SVG hash mismatch against upstream declaration"
        )


def _fetch_one(entry: dict, *, refresh: bool) -> str:
    path = _source_path(entry)
    if path.is_file() and not refresh:
        content = path.read_bytes()
        _check_unitsquare_acquisition(entry, content)
        return "retained"
    request = urllib.request.Request(entry["source_url"], headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                content = response.read()
        except (OSError, urllib.error.HTTPError, urllib.error.URLError) as error:
            last_error = error
            if attempt < 2:
                time.sleep(2**attempt)
        else:
            if b"<svg" not in content[:100_000]:
                raise ValueError(f"n={entry['n']}: upstream response is not SVG")
            _check_unitsquare_acquisition(entry, content)
            path.parent.mkdir(parents=True, exist_ok=True)
            with atomic_output_file(path) as temporary:
                temporary.write_bytes(content)
            return "fetched"
    raise RuntimeError(f"n={entry['n']}: fetch failed: {last_error}")


def fetch(*, refresh: bool) -> None:
    entries = [
        entry for entry in eligible_entries() if entry["source_key"] == "unitsquare-release-1"
    ]
    outcomes = [_fetch_one(entry, refresh=refresh) for entry in entries]
    print(
        "prospective source fetch passed: "
        f"{outcomes.count('fetched')} fetched, {outcomes.count('retained')} retained, "
        "4 declared hashes matched"
    )


def _witness(entry: dict, source_path: str | None = None) -> dict:
    """The Witness/v2 document for one case, from an already-resolved source path.

    `source_path` is where the retained UnitSquare SVG for this case lives, or `None`
    for a generated grid, which has no retained source at all. It is passed in rather
    than read from `SOURCE_ROOT` because this runs in a pool worker, and a `forkserver`
    child re-imports this module instead of inheriting it: a caller that repointed that
    root would have the parent reading one directory and the workers reading another,
    with nothing raising. Resolving in the parent puts the answer in the unit's payload,
    where it travels with the work.
    """
    n = entry["n"]
    witness_id = f"W-prospective-source-n{n:03d}"
    witness_path = f"witnesses/prospective/n-{n:03d}.yaml"
    if entry["source_key"] == "catalogue-trivial-grid-rule":
        witness = exact_grid_witness(
            n,
            entry["trivial_grid_side"],
            frontier_path="atlas/prospective/source-availability-101-324.json",
            witness_id=witness_id,
            witness_path=witness_path,
            source_key="Kingbird current-catalogue trivial-grid rule",
            limitations=(
                "Exactly verifies this canonical no-tilt construction. The source "
                "catalogue reports it as best known, but this witness does not prove "
                "global optimality, uniqueness, or the catalogue claim."
            ),
        )
    else:
        retained = Path(source_path) if source_path else _source_path(entry)
        if not retained.is_file():
            raise FileNotFoundError(f"missing retained source: {_relative(retained)}")
        content = retained.read_bytes()
        _check_unitsquare_acquisition(entry, content)
        geometry = parse_unitsquare_svg(content.decode("utf-8"), expected_n=n)
        witness = unitsquare_witness(
            n,
            geometry,
            source_path=_relative(retained),
            source_url=entry["source_url"],
            witness_id=witness_id,
            witness_path=witness_path,
            limitations=(
                "Coordinates were recovered from the public six-decimal SVG rendering, "
                "not the unavailable governed interval boxes named by its metadata. "
                "This checks the displayed construction only and does not replay the "
                "source interval claim or prove optimality."
            ),
        )
    problems = check_witness_semantics(witness)
    if problems:
        raise ValueError(f"{witness_id}: {problems[0]}")
    return witness


def _render(witness: dict) -> str:
    n = witness["n"]
    frame = replace(
        frame_from_witness(witness),
        label=f"n={n} prospective source construction",
    )
    return render_packing_svg(
        frame,
        spec=RenderSpec(
            overlays=frozenset(),
            title=f"Prospective source construction for {n} unit squares",
            description=(
                f"The source-selected n={n} construction, normalized to Witness/v2 and "
                "drawn with the repository deterministic house renderer. This is a "
                "feasible construction, not an optimality or chunk-structure claim."
            ),
        ),
    )


def _manifest_entry(entry: dict, witness: dict, source_path: str | None = None) -> dict:
    n = entry["n"]
    source_kind = (
        "exact-generated-grid"
        if entry["source_key"] == "catalogue-trivial-grid-rule"
        else "unitsquare-rendering"
    )
    source = {
        "kind": source_kind,
        "source_key": entry["source_key"],
        "derivation": (
            "canonical row-major subset of the exact catalogue-rule grid"
            if source_kind == "exact-generated-grid"
            else "complete normalization of the retained six-decimal source SVG"
        ),
    }
    if source_kind == "unitsquare-rendering":
        source.update(
            {
                "path": _relative(Path(source_path) if source_path else _source_path(entry)),
                "url": entry["source_url"],
            }
        )
    claim = witness["claim"]
    return {
        "annotation_status": "prohibited-uncomputed",
        "n": n,
        "rendering": {
            "path": f"atlas/prospective/rendering/n-{n:03d}.svg",
            "renderer": "sqpack deterministic house renderer",
        },
        "source": source,
        "witness": {
            "coordinate_provenance": claim["coordinate_provenance"],
            "id": witness["id"],
            "method": claim["method"],
            "path": f"witnesses/prospective/n-{n:03d}.yaml",
            **({"tolerance": claim["tolerance"]} if "tolerance" in claim else {}),
        },
    }


def _build_one(entry: dict, source_path: str | None) -> tuple[str, str, dict]:
    """Witness text, house rendering and manifest entry for one case.

    The whole unit of parallel work, and the process boundary is drawn here rather than
    around `_witness` on purpose. What crosses it is text in both directions: a
    source-map entry and an already-resolved retained-source path going out, and a YAML
    document, an SVG and a plain manifest dict coming back. Nothing carrying a scalar
    kind is ever pickled, so the witness is built and rendered in the same process, and
    no digit can be lost to a round trip.
    """
    try:
        witness = _witness(entry, source_path)
        return (
            witness_document(witness, schema="../witness.schema.yaml"),
            _render(witness),
            _manifest_entry(entry, witness, source_path),
        )
    except Exception as error:
        # A pool reports which call raised without saying which unit raised it, and the
        # messages here name a witness id or a path rather than the case. Naming it
        # keeps a failure attributable whichever way the seed was built.
        message = str(error)
        prefix = f"n={entry['n']}"
        blamed = message if message.startswith(prefix) else f"{prefix}: {message}"
        raise ValueError(blamed) from error


def build_cases(entries: Sequence[dict], workers: int | None) -> list[tuple[str, str, dict]]:
    """Build every case, in source-map order, across `workers` processes.

    Every case is independent of every other -- each parses or generates its own
    geometry and renders only itself -- so this is a map, and it was a serial one. It
    cost 37.03s in the `sweeps` job of run 34018763923.

    `workers` is the pool size. `None` asks `sqpack.workers.worker_count`, which reads
    the `PACK_JOBS` cap the gate exports to every step, so the count is never taken from
    the machine behind the gate's back. `1` runs in this process rather than through a
    pool, because a one-worker pool is a subprocess and a protocol for no concurrency.

    The retained source paths are resolved here, in the parent, and travel with the
    work. `_source_path` reads the module-level `SOURCE_ROOT`, and a `forkserver` worker
    re-imports this module rather than inheriting it, so a caller that repointed that
    root -- `clear_build_caches` exists for one -- would otherwise have the parent
    reading a temporary directory and the workers reading the real one, silently.

    Order is the source map's, whichever way it ran: `pool.map` yields by submission
    index rather than by completion, so `seed_errors` still sees the frozen selection in
    the frozen order and `check` can compare the manifest byte for byte.
    """
    source_paths = [
        str(_source_path(entry)) if entry["source_key"] == "unitsquare-release-1" else None
        for entry in entries
    ]
    requested = worker_count(len(entries)) if workers is None else workers
    count = max(1, min(requested, len(entries)))
    if count == 1:
        return [
            _build_one(entry, source_path)
            for entry, source_path in zip(entries, source_paths, strict=True)
        ]
    with ProcessPoolExecutor(max_workers=count) as pool:
        return list(pool.map(_build_one, entries, source_paths))


def clear_build_caches() -> None:
    """Drop the memoized seed build.

    ``_expected_outputs`` reads the module-level source roots, so a caller that
    repoints one must clear the memo on the way in and out rather than read, or
    leave behind, a build made against the other root.
    """
    _expected_outputs.cache_clear()


def expected_outputs(workers: int | None = None) -> tuple[dict[Path, str], dict]:
    """Derived seed artifacts and manifest; callers get copies of the memo."""
    outputs, manifest = _expected_outputs(workers)
    return dict(outputs), copy.deepcopy(manifest)


@cache
def _expected_outputs(workers: int | None = None) -> tuple[dict[Path, str], dict]:
    entries = eligible_entries()
    outputs: dict[Path, str] = {}
    manifest_entries = []
    for entry, (witness_text, rendering, manifest_entry) in zip(
        entries, build_cases(entries, workers), strict=True
    ):
        n = entry["n"]
        outputs[WITNESS_ROOT / f"n-{n:03d}.yaml"] = witness_text
        outputs[RENDER_ROOT / f"n-{n:03d}.svg"] = rendering
        manifest_entries.append(manifest_entry)

    retained_sources = []
    for entry in entries:
        if entry["source_key"] != "unitsquare-release-1":
            continue
        path = _source_path(entry)
        content = path.read_bytes()
        retained_sources.append(
            {
                "bytes": len(content),
                "creator": "UnitSquare Project",
                "license": "CC-BY-4.0-in-dataset-page-metadata",
                "n": entry["n"],
                "path": _relative(path),
                "retrieved": RETRIEVED,
                "url": entry["source_url"],
            }
        )
    manifest = {
        "softschema": {
            "contract": "packing.squares:ProspectiveAtlasSeed/v1",
            "envelope": "atlas_seed",
            "schema": "prospective-atlas-seed.schema.yaml",
            "status": "enforced",
        },
        "atlas_seed": {
            "annotation_policy": (
                "No contact, chunk, rigidity, or grammar annotations are computed or retained."
            ),
            "entries": manifest_entries,
            "excluded": {
                "count": 123,
                "reason": "Kingbird acquisition is deferred pending license review.",
                "source_key": "kingbird-current-catalogue",
            },
            "generated_by": GENERATOR,
            "rendering_policy": "repository deterministic house renderer",
            "retained_sources": retained_sources,
            "selection": {
                "count": 101,
                "exact_generated_grid_cases": 97,
                "unitsquare_rendering_cases": 4,
            },
            "source_map": {"path": _relative(SOURCE_MAP)},
            "status": "partial-prospective-corpus-seed-not-hypothesis-evidence",
        },
    }
    errors = seed_errors(manifest["atlas_seed"])
    if errors:
        raise ValueError("invalid prospective atlas seed: " + "; ".join(errors))
    outputs[MANIFEST] = _json_text(manifest)
    return outputs, manifest


def update(workers: int | None = None) -> None:
    outputs, _manifest = expected_outputs(workers)
    for path, content in sorted(outputs.items(), key=lambda item: item[0].as_posix()):
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_file() and path.read_text(encoding="utf-8") == content:
            continue
        with atomic_output_file(path) as temporary:
            temporary.write_text(content, encoding="utf-8")
    print("prospective atlas seed updated: 101 witnesses and 101 house renderings")


def check(workers: int | None = None) -> None:
    outputs, manifest = expected_outputs(workers)
    problems = []
    for path, expected in sorted(outputs.items(), key=lambda item: item[0].as_posix()):
        if not path.is_file():
            problems.append(f"missing {_relative(path)}")
        elif path.read_text(encoding="utf-8") != expected:
            problems.append(f"stale {_relative(path)}")
    expected_names = {f"n-{entry['n']:03d}" for entry in manifest["atlas_seed"]["entries"]}
    if WITNESS_ROOT.is_dir():
        unexpected = {path.stem for path in WITNESS_ROOT.glob("*.yaml")} - expected_names
        problems.extend(f"unexpected prospective witness {name}" for name in sorted(unexpected))
    if RENDER_ROOT.is_dir():
        unexpected = {path.stem for path in RENDER_ROOT.glob("*.svg")} - expected_names
        problems.extend(
            f"unexpected prospective rendering {name}" for name in sorted(unexpected)
        )
    if problems:
        raise ValueError("prospective atlas seed drift:\n  " + "\n  ".join(problems[:20]))
    print("prospective atlas seed check passed: 101 witnesses and 101 house renderings")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--fetch", action="store_true")
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    command.add_argument("--refresh", action="store_true")
    command.add_argument(
        "--jobs",
        type=int,
        metavar="N",
        default=None,
        help=(
            "processes to build the seed with; the default follows the PACK_JOBS cap "
            "the gate exports, and the whole machine when there is no gate"
        ),
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.refresh and not args.fetch:
        raise ValueError("--refresh is valid only with --fetch")
    workers: int | None = args.jobs
    if args.fetch:
        fetch(refresh=args.refresh)
    elif args.update:
        update(workers)
    else:
        check(workers)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
