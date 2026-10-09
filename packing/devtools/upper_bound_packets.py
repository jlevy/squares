#!/usr/bin/env python3
"""Acquire, certify and check the September 2026 parallel upper-bound packets.

Three public repositories report packings that beat the best known sides this project
recorded, and issue #227 asked for the first of them to be registered:

- ``franciscouzo/square-packing`` at ``f3c5a529`` (27 September 2026), 49 packings for
  ``n = 68..307``, by Francisco Couzo;
- ``JoostdeWinter/square-packing-211`` at ``702df9bb`` (16 September 2026), one packing
  of 211 squares at side below 15, by Joost de Winter;
- ``griffcass/square-packing`` at ``82661bc`` (23 September 2026, UTC-6), 39 packings
  for ``n = 103..307``, by Griffin Casson.

Couzo's next revision, ``6042c56`` (3 October 2026), lowered seven of his 49 sides; its
packet keeps those seven alone and names the first as the packet it follows
(`Source.supersedes`).

The first two publish no licence, and their packets keep only derived Witness/v2 facts
and metadata, never the upstream bytes (``raw_asset_retained: false``): the
derived-only form of the known-best retention policy in
``resources/web/known-best-packings/README.md``, which also permits retaining an
unlicensed source's factual data. Casson licenses his packings CC BY 4.0, so they are
retained raw.

The main subcommands, run from ``packing/``:

``acquire --source ID --clone PATH``
    Read a local clone at the pinned revision and write the packet's
    ``acquisition/sources.json`` and ``facts/`` (and, for Casson, the retained files).
    Needs the clone; nothing else here does.

``certify [--source ID] [--n N ...] [--workers K]``
    For each packing, promote the retained decimal facts to an exact rational
    certificate (``packing-witness promote --strategy robust-rational
    --max-side-increase 1e-9``, called in process), store it as deterministic gzip under
    ``witnesses/<dir>/n-NNN-rational.yaml.gz``, decide it again with
    ``devtools.check_rational_witness_independent``, which shares no code with the
    generator, and write ``receipts/certification.json``. Negative controls on the
    smallest certificate go to ``receipts/negative-controls.json``.

``restamp [--source ID]``
    Re-derive each receipt row's units above the printed side, verified value and exact
    form from its committed certificate, promoting nothing; for a change in how those
    fields are derived.

``check``
    Fast and offline: facts, receipts, certificates' digests and sides, and the value
    each case's verified upper lane must carry. This is what the tests run.

``check --replay [--n N ...] [--workers K]``
    The evidence replay: regenerate every certificate from the retained facts, require
    its bytes to equal the committed one, and decide the committed one again with the
    independent checker. Deterministic; about half an hour on four workers.

The value a case's verified upper lane carries (`verified_value`) is the larger of the
printed side and the certified side rounded up at the printed precision, and its
``exact_form`` is that decimal as a fraction: the certificate proves ``s(n)`` at most
its own side, which is at most that value.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
from collections.abc import Iterable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from decimal import ROUND_CEILING, Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import check_rational_witness_independent as independent
from devtools.retained_data import (
    LINE_THRESHOLD,
    compressed_path,
    read_retained_text,
    retained_exists,
)
from sqpack.witness import (
    WitnessError,
    exact_verify,
    load_witness,
    promote_rational,
    witness_document,
)

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "resources/web"
WITNESSES = ROOT / "witnesses"
WITNESS_SCHEMA = WITNESSES / "witness.schema.yaml"
#: When the first three packets were retrieved; a later packet carries its own date.
RETRIEVED = "2026-09-29"
#: The promotion the research lane ran and this tool repeats, byte for byte.
RATIONAL_DIGITS = 36
MAX_SIDE_INCREASE = "1e-9"
#: The certificate the 27 September packet's negative controls mutate, the smallest so
#: they run in seconds, and the square they move. A packet's own pair is `Source.control`.
CONTROL_N = 68
CONTROL_SHIFT_SQUARE = 31
FORMAT = "external-source-acquisition-v1"


@dataclass(frozen=True, slots=True)
class Source:
    """One retained repository and what this project does with it."""

    id: str
    #: The prefix of its witness ids, ``W-<short>-nNNN``.
    short: str
    directory: str
    key: str
    url: str
    revision: str
    author: str
    licence: str | None
    #: Whether the upstream packing files may be kept byte for byte.
    retain_raw: bool
    #: Where exact certificates go, for a source whose packings are certified here.
    witness_directory: str | None
    #: How its packing files are written: ``couzo`` (a ``# n`` and ``# s`` header and
    #: ``x y theta`` rows), ``de-winter`` (one JSON record) or ``casson``.
    layout: str
    #: The day the clone the packet was written from was taken.
    retrieved: str = RETRIEVED
    #: The certificate the exact route's negative controls mutate, and the square they
    #: move right by ``1e-6``; None where the packet keeps no exact-route controls.
    control: tuple[int, int] | None = None
    #: The id of the earlier packet of the same repository that this one follows. Such a
    #: packet retains only the counts whose printed side changed since that one's pin.
    supersedes: str | None = None

    @property
    def packet(self) -> Path:
        return WEB / self.directory

    @property
    def sources_json(self) -> Path:
        return self.packet / "acquisition/sources.json"

    @property
    def facts(self) -> Path:
        return self.packet / "facts"

    @property
    def receipts(self) -> Path:
        return self.packet / "receipts"

    @property
    def certification(self) -> Path:
        return self.receipts / "certification.json"

    @property
    def controls(self) -> Path:
        return self.receipts / "negative-controls.json"

    def fact(self, n: int) -> Path:
        return self.facts / f"n-{n:03d}.yaml"

    def certificate(self, n: int) -> Path:
        """The committed certificate, deterministic gzip of `certificate_yaml`."""
        assert self.witness_directory is not None
        return WITNESSES / self.witness_directory / f"n-{n:03d}-rational.yaml.gz"

    def certificate_yaml(self, n: int) -> Path:
        """What ``gunzip -k`` restores, and the path the certificate's replay names."""
        assert self.witness_directory is not None
        return WITNESSES / self.witness_directory / f"n-{n:03d}-rational.yaml"

    def blob_url(self, path: str) -> str:
        return f"{self.url}/blob/{self.revision}/{path}"


FRANCISCOUZO = Source(
    id="franciscouzo-square-packing",
    short="franciscouzo",
    directory="franciscouzo-square-packing-2026-09-27",
    key="[franciscouzo square-packing 2026-09-27]",
    url="https://github.com/franciscouzo/square-packing",
    revision="f3c5a529c255b546db18605702b8da298132309f",
    author="Francisco Couzo",
    licence=None,
    retain_raw=False,
    witness_directory="franciscouzo-2026",
    layout="couzo",
    control=(CONTROL_N, CONTROL_SHIFT_SQUARE),
)
#: The same repository at its next revision, ``6042c56`` of 3 October 2026, which lowered
#: seven of the 49 sides. Its controls mutate ``n = 208``, the smallest of the seven, and
#: move square 2, the first whose move right by ``1e-6`` makes an overlap (with square 51).
FRANCISCOUZO_2026_10_03 = Source(
    id="franciscouzo-square-packing-2026-10-03",
    short="franciscouzo-2026-10-03",
    directory="franciscouzo-square-packing-2026-10-03",
    key="[franciscouzo square-packing 2026-10-03]",
    url="https://github.com/franciscouzo/square-packing",
    revision="6042c56b43b64c09fe5a32c64879e698f399beaf",
    author="Francisco Couzo",
    licence=None,
    retain_raw=False,
    witness_directory="franciscouzo-2026-10-03",
    layout="couzo",
    retrieved="2026-10-05",
    control=(208, 2),
    supersedes="franciscouzo-square-packing",
)
DE_WINTER = Source(
    id="de-winter-square-packing-211",
    short="de-winter",
    directory="de-winter-square-packing-211-2026-09-16",
    key="[de Winter n211 2026-09-16]",
    url="https://github.com/JoostdeWinter/square-packing-211",
    revision="702df9bb3b1e7fe13279a61a1fa89722aa2d496a",
    author="Joost de Winter",
    licence=None,
    retain_raw=False,
    witness_directory="de-winter-2026",
    layout="de-winter",
)
CASSON = Source(
    id="casson-square-packing",
    short="casson",
    directory="casson-square-packing-2026-09-23",
    key="[griffcass square-packing 2026-09-23]",
    url="https://github.com/griffcass/square-packing",
    revision="82661bc8777beeecf458312e8aca9179a969da4f",
    author="Griffin Casson",
    licence="MIT (code); CC BY 4.0 (packings, figures and paper)",
    retain_raw=True,
    witness_directory=None,
    layout="casson",
)
SOURCES = (FRANCISCOUZO, FRANCISCOUZO_2026_10_03, DE_WINTER, CASSON)
BY_ID = {source.id: source for source in SOURCES}
CERTIFIED = tuple(source for source in SOURCES if source.witness_directory is not None)

#: Casson's retained upstream files, beside his 39 packings; the rest is pinned by digest.
CASSON_RETAINED = ("README.md", "LICENSE", "CITATION.cff", "results/summary.csv")
CASSON_TREE = "griffcass-square-packing"


# --------------------------------------------------------------------------------------
# Values
# --------------------------------------------------------------------------------------


def places(value: str) -> int:
    """Decimal places a printed side carries."""
    exponent = Decimal(value).as_tuple().exponent
    assert isinstance(exponent, int)
    return -exponent


def ceiling_at(value: Fraction, digits: int) -> Decimal:
    """``value`` rounded up to ``digits`` decimal places, exactly."""
    with localcontext() as context:
        context.prec = 200
        quotient = Decimal(value.numerator) / Decimal(value.denominator)
        result = quotient.quantize(Decimal(1).scaleb(-digits), rounding=ROUND_CEILING)
    if Fraction(result) < value:
        # The division is inexact at 200 digits only for sides far longer than any here.
        raise ValueError("ceiling underflowed its working precision")
    return result


def verified_value(printed: str, certified: Fraction) -> str:
    """The upper bound a case's verified lane carries for a certificate of this side."""
    ceiling = ceiling_at(certified, places(printed))
    chosen = max(Decimal(printed), ceiling)
    return printed if chosen == Decimal(printed) else format(chosen, "f")


def units_above(printed: str, certified: Fraction) -> int:
    """How many units of the printed last place the verified value sits above the side.

    Zero where the certificate is at or inside the printed side. The signed distance is
    the receipt's ``side_increase``; counted in units of each source's own last place it
    would not compare across sources, since de Winter prints twenty decimals and his
    ``2.1e-14`` margin would read as ``-2100010`` units.
    """
    digits = places(printed)
    difference = ceiling_at(certified, digits) - Decimal(printed)
    return max(0, int(difference.scaleb(digits)))


def exact_form(value: str) -> str:
    fraction = Fraction(value)
    return f"{fraction.numerator}/{fraction.denominator}"


def derived(printed: str, certified: Fraction) -> dict[str, Any]:
    """The receipt fields that follow from the printed side and the certificate's side."""
    value = verified_value(printed, certified)
    return {
        "units_above_printed": units_above(printed, certified),
        "verified_value": value,
        "exact_form": exact_form(value),
    }


# --------------------------------------------------------------------------------------
# Acquisition
# --------------------------------------------------------------------------------------


def _git(clone: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(clone), *arguments], check=True, capture_output=True, text=True
    ).stdout


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _utc(timestamp: str) -> str:
    """An ISO timestamp with offset, rewritten in UTC."""
    from datetime import UTC, datetime  # noqa: PLC0415

    return datetime.fromisoformat(timestamp).astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _file_record(clone: Path, path: str, *, retained: bool) -> dict[str, Any]:
    data = (clone / path).read_bytes()
    return {
        "path": path,
        "bytes": len(data),
        "sha256": _sha256(data),
        "raw_asset_retained": retained,
    }


def _commit(clone: Path, revision: str) -> dict[str, str]:
    line = _git(clone, "show", "-s", "--format=%H%x00%T%x00%an%x00%aI%x00%cI", revision)
    commit, tree, author, authored, committed = line.strip().split("\x00")
    return {
        "source_commit": commit,
        "git_tree": tree,
        "commit_author": author,
        "authored_utc": _utc(authored),
        "committed_utc": _utc(committed),
    }


_COUZO_HEADER = re.compile(r"# n = (\d+)\n# s = ([0-9.eE+-]+)\n# x y theta\(rad\)\n")


def parse_couzo(text: str) -> tuple[int, str, list[tuple[str, str, str]]]:
    """``nNNN.txt``: two header lines, a column line, then ``x y theta`` per square."""
    match = _COUZO_HEADER.match(text)
    if match is None:
        raise ValueError("not a franciscouzo packing file")
    n, side = int(match.group(1)), match.group(2)
    rows = [tuple(line.split()) for line in text[match.end() :].splitlines() if line.strip()]
    if len(rows) != n or any(len(row) != 3 for row in rows):
        raise ValueError(f"expected {n} rows of three fields")
    return n, side, [(row[0], row[1], row[2]) for row in rows]


def couzo_history(clone: Path, n: int) -> list[dict[str, str]]:
    """Every commit that changed the packing for ``n``, oldest first, across its names.

    The first eight commits name files by side (``n102_s10.607902017700.txt``), and one
    replaces ``n206_s14.860232206380.txt`` by ``n206.txt`` without a rename Git can
    follow, so the history is read tree by tree rather than with ``--follow``. Those
    eight commits were also committed again on 2026-09-24, the first at 10:33:57 UTC and
    the last before 10:35, up to 33 hours after they were authored, so both clocks are
    kept: the author's, and the committer's, which bounds when the history now public was
    pushed.
    """
    pattern = re.compile(rf"n{n}(?:_s[0-9.]+)?\.txt")
    history: list[dict[str, str]] = []
    blob = None
    for line in _git(clone, "log", "--reverse", "--format=%H %aI %cI").splitlines():
        commit, authored, committed = line.split()
        found = [
            entry.split("\t")
            for entry in _git(clone, "ls-tree", commit).splitlines()
            if pattern.fullmatch(entry.split("\t")[1])
        ]
        if len(found) > 1:
            raise ValueError(f"{commit} holds two packings for n={n}")
        if not found or found[0][0].split()[2] == blob:
            continue
        ((meta, path),) = found
        blob = meta.split()[2]
        _n, side, _rows = parse_couzo(_git(clone, "show", f"{commit}:{path}"))
        history.append(
            {
                "commit": commit,
                "path": path,
                "authored_utc": _utc(authored),
                "committed_utc": _utc(committed),
                "side": side,
            }
        )
    return history


def _witness(
    source: Source,
    *,
    n: int,
    side: str,
    rows: Iterable[tuple[str, str, str]],
    claim: dict[str, Any],
    upstream: str,
) -> dict[str, Any]:
    return {
        "id": f"W-{source.short}-n{n:03d}",
        "n": n,
        "side": side,
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "radians",
        },
        "squares": [
            {"id": index, "center": [x, y], "angle": theta}
            for index, (x, y, theta) in enumerate(rows, start=1)
        ],
        "claim": claim,
        "source": {
            "key": source.key,
            "path": source.sources_json.relative_to(ROOT).as_posix(),
            "url": source.blob_url(upstream),
            "retrieved": source.retrieved,
            "revision": source.revision,
        },
    }


def _write_fact(source: Source, n: int, witness: Mapping[str, Any]) -> None:
    path = source.fact(n)
    path.parent.mkdir(parents=True, exist_ok=True)
    schema = Path("../../../../witnesses/witness.schema.yaml").as_posix()
    with atomic_output_file(path) as temporary:
        temporary.write_text(witness_document(witness, schema=schema), encoding="utf-8")


COUZO_CLAIM = {
    "coordinate_provenance": "reported",
    "method": "numerical-f64",
    "precision": {
        "binary_bits": 53,
        "rounding": "the source prints each binary64 value as a %.17e literal",
    },
    "tolerance": "not stated by the source",
    "limitations": (
        "Author-reported decimal poses carried verbatim from the source's text file, "
        "whose bytes are not retained; the source states no feasibility tolerance or "
        "checker. No exact geometry, certificate or optimality claim."
    ),
}


def acquire_couzo(clone: Path, source: Source = FRANCISCOUZO) -> dict[str, Any]:
    """Facts and history for every ``nNNN.txt`` at the pinned revision.

    A packet that follows an earlier one of the same repository (`Source.supersedes`)
    takes facts only where the printed side differs from that packet's, and pins every
    upstream file by digest as the first did.
    """
    if _git(clone, "rev-parse", "HEAD").strip() != source.revision:
        raise ValueError(f"{clone} is not checked out at {source.revision}")
    earlier = cases(BY_ID[source.supersedes]) if source.supersedes else None
    files = sorted(
        (path.name for path in clone.iterdir() if path.is_file()),
        key=lambda name: (re.sub(r"\d+", "", name), int(re.sub(r"\D", "", name) or 0)),
    )
    cases_found = []
    for name in (name for name in files if re.fullmatch(r"n\d+\.txt", name)):
        n, side, rows = parse_couzo((clone / name).read_text(encoding="utf-8"))
        if earlier is not None and n in earlier and earlier[n]["side"] == side:
            continue
        history = couzo_history(clone, n)
        current = next(entry for entry in history if entry["side"] == side)
        cases_found.append(
            {
                "n": n,
                "side": side,
                "file": name,
                "first_authored_utc": history[0]["authored_utc"],
                "first_side": history[0]["side"],
                "current_since_authored_utc": current["authored_utc"],
                "current_since_committed_utc": current["committed_utc"],
                "current_since_commit": current["commit"],
                "history": history,
            }
        )
        _write_fact(
            source,
            n,
            _witness(source, n=n, side=side, rows=rows, claim=COUZO_CLAIM, upstream=name),
        )
    follows = (
        {
            "supersedes": {
                "packet": BY_ID[source.supersedes].directory,
                "source_commit": BY_ID[source.supersedes].revision,
                "retained_here": "the counts whose printed side changed since that pin",
            }
        }
        if source.supersedes
        else {}
    )
    return {
        "id": source.id,
        "source_url": source.url,
        **_commit(clone, source.revision),
        **follows,
        "author": source.author,
        "author_read_from": "commit metadata; the repository has no LICENSE and its README "
        "names no author",
        "licence": None,
        "retention_policy": "metadata-and-derived-numerical-facts-only",
        "raw_asset_retained": False,
        "ai_statement": {
            "text": "I found better solutions with the help of Claude for the 102 and 103 "
            "problems: https://github.com/franciscouzo/square-packing",
            "where": "https://github.com/jlevy/squares/issues/227",
            "opened_utc": "2026-09-23T02:48:35Z",
            "note": "The repository itself states no AI assistance.",
        },
        "files": [_file_record(clone, name, retained=False) for name in files],
        "cases": sorted(cases_found, key=lambda case: case["n"]),
    }


def acquire_de_winter(clone: Path) -> dict[str, Any]:
    source = DE_WINTER
    if _git(clone, "rev-parse", "HEAD").strip() != source.revision:
        raise ValueError(f"{clone} is not checked out at {source.revision}")
    record = json.loads((clone / "n211__record.json").read_text(encoding="utf-8"))
    n = int(record["n"])
    if record["unit_square_side"] != "1" or record["angle_unit"] != "radians":
        raise ValueError("unexpected de Winter record units")
    rows = [(square["x"], square["y"], square["theta"]) for square in record["squares"]]
    verification = record["verification"]
    claim = {
        "coordinate_provenance": "reported",
        "method": "numerical-multiprecision",
        "precision": {
            "decimal_digits": int(verification["interval_precision_decimal_digits"]),
            "rounding": "source interval arithmetic, outward; decimal export at 21 "
            "significant digits",
        },
        "tolerance": "0 (source reports strict clearances: wall at least "
        f"{verification['minimum_wall_clearance_lower_bound']}, pair gap at least "
        f"{verification['minimum_pair_separating_axis_gap_lower_bound']})",
        "limitations": (
            "Author-reported decimal poses and an author-reported interval verification "
            "summary, carried verbatim from the source's JSON record, whose bytes are not "
            "retained; no interval boxes or checker are published. No exact geometry, "
            "certificate or optimality claim."
        ),
    }
    _write_fact(
        source,
        n,
        _witness(
            source,
            n=n,
            side=str(record["s"]),
            rows=rows,
            claim=claim,
            upstream="n211__record.json",
        ),
    )
    log = _git(clone, "log", "--reverse", "--format=%H %aI %cI").splitlines()
    history = [
        {"commit": commit, "authored_utc": _utc(authored), "committed_utc": _utc(committed)}
        for commit, authored, committed in (line.split() for line in log)
    ]
    files = sorted(path.name for path in clone.iterdir() if path.is_file())
    return {
        "id": source.id,
        "source_url": source.url,
        **_commit(clone, source.revision),
        "author": source.author,
        "author_read_from": "commit metadata; the repository has no LICENSE and its README "
        "names no author",
        "licence": None,
        "retention_policy": "metadata-and-derived-numerical-facts-only",
        "raw_asset_retained": False,
        "ai_statement": None,
        "history": history,
        "files": [_file_record(clone, name, retained=False) for name in files],
        "cases": [
            {
                "n": n,
                "side": str(record["s"]),
                "file": "n211__record.json",
                "first_authored_utc": history[-1]["authored_utc"],
                "current_since_authored_utc": history[-1]["authored_utc"],
                "current_since_committed_utc": history[-1]["committed_utc"],
                "current_since_commit": history[-1]["commit"],
                "record_improvement": record.get("record_improvement"),
                "previous_verified_s": record.get("previous_verified_s"),
                "method": record.get("method"),
                "verification": verification,
            }
        ],
    }


_CASSON_SIDE = re.compile(r"s: ([0-9.]+)\n")


def acquire_casson(clone: Path) -> dict[str, Any]:
    source = CASSON
    if _git(clone, "rev-parse", "HEAD").strip() != source.revision:
        raise ValueError(f"{clone} is not checked out at {source.revision}")
    tracked = sorted(_git(clone, "ls-files").splitlines())
    packings = [path for path in tracked if re.fullmatch(r"results/packings/n\d+\.txt", path)]
    retained = set(CASSON_RETAINED) | set(packings)
    destination = source.packet / CASSON_TREE
    for path in sorted(retained):
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((clone / path).read_bytes())
    import csv  # noqa: PLC0415

    with (clone / "results/summary.csv").open(encoding="utf-8", newline="") as stream:
        summary = {int(row["n"]): row for row in csv.DictReader(stream)}
    commit = _commit(clone, source.revision)
    cases = []
    for path in packings:
        n = int(re.sub(r"\D", "", Path(path).stem))
        match = _CASSON_SIDE.match((clone / path).read_text(encoding="utf-8"))
        if match is None:
            raise ValueError(f"{path} has no side line")
        row = summary[n]
        cases.append(
            {
                "n": n,
                "side": match.group(1),
                "file": path,
                "readme_side": row["our_side"],
                "record_side_2026_09_23": row["record_side_2026_09_23"],
                "method": row["method"],
                "check_packing_16d": row["check_packing_16d"],
                "verify_mp_50d": row["verify_mp_50d"],
                "shrink_2e-11_control": row["shrink_2e-11_control"],
                "first_authored_utc": commit["authored_utc"],
                "current_since_authored_utc": commit["authored_utc"],
                "current_since_committed_utc": commit["committed_utc"],
                "current_since_commit": commit["source_commit"],
            }
        )
    return {
        "id": source.id,
        "source_url": source.url,
        **commit,
        "author": source.author,
        "author_read_from": "LICENSE (Copyright (c) 2026 Griffin Casson), CITATION.cff and "
        "the README's Credits section",
        "licence": source.licence,
        "retention_policy": "packings, summary and attribution files retained byte for byte "
        "under CC BY 4.0 and MIT; every other tracked file pinned by SHA-256",
        "raw_asset_retained": True,
        "ai_statement": {
            "text": "The work was done by Griffin Casson with the help of Claude (Anthropic).",
            "where": "README.md, section Credits",
        },
        "archived_path": (source.packet / CASSON_TREE).relative_to(ROOT.parent).as_posix(),
        "files": [_file_record(clone, path, retained=path in retained) for path in tracked],
        "cases": sorted(cases, key=lambda case: case["n"]),
    }


ACQUIRE = {
    FRANCISCOUZO.id: acquire_couzo,
    FRANCISCOUZO_2026_10_03.id: lambda clone: acquire_couzo(clone, FRANCISCOUZO_2026_10_03),
    DE_WINTER.id: acquire_de_winter,
    CASSON.id: acquire_casson,
}


def acquire(source: Source, clone: Path) -> None:
    record = {
        "format": FORMAT,
        "retrieved": source.retrieved,
        "sources": [ACQUIRE[source.id](clone)],
    }
    _write_json(source.sources_json, record)


def acquisition(source: Source) -> dict[str, Any]:
    record = json.loads(read_retained_text(source.sources_json))
    (entry,) = record["sources"]
    return entry


def cases(source: Source) -> dict[int, dict[str, Any]]:
    """The packet's per-case facts, by ``n``."""
    return {int(case["n"]): case for case in acquisition(source)["cases"]}


# --------------------------------------------------------------------------------------
# Certification
# --------------------------------------------------------------------------------------


def _gzip(data: bytes) -> bytes:
    """``gzip -9n``: no name and no timestamp, so the same input gives the same bytes."""
    return subprocess.run(["gzip", "-9n"], input=data, check=True, capture_output=True).stdout


def certificate_text(source: Source, n: int) -> tuple[str, dict[str, Any]]:
    """Promote one retained fact to its certificate text, as `certify` writes it."""
    witness = load_witness(source.fact(n), fallback_schema=WITNESS_SCHEMA)
    result, promoted = promote_rational(
        witness,
        rational_digits=RATIONAL_DIGITS,
        max_side_increase=MAX_SIDE_INCREASE,
        source_path=source.fact(n).relative_to(ROOT).as_posix(),
        replay_path=source.certificate_yaml(n).relative_to(ROOT).as_posix(),
    )
    return witness_document(promoted, schema="../witness.schema.yaml"), result


def independent_check(text: str) -> dict[str, Any]:
    """The independent checker's verdict on one certificate's text."""
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "certificate.yaml"
        path.write_text(text, encoding="utf-8")
        return independent.check(path)


def _side(text: str) -> Fraction:
    """The certificate's exact side, read from its header without parsing the rest."""
    match = re.search(r"^  side: (\S+)$", text, flags=re.MULTILINE)
    if match is None:
        raise ValueError("certificate has no side line")
    return Fraction(match.group(1).strip("'"))


def certify_one(unit: tuple[str, int]) -> dict[str, Any]:
    source_id, n = unit
    source = BY_ID[source_id]
    printed = cases(source)[n]["side"]
    started = time.monotonic()
    text, result = certificate_text(source, n)
    promote_seconds = time.monotonic() - started
    data = text.encode("utf-8")
    stored = _gzip(data)
    path = source.certificate(n)
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(stored)
    started = time.monotonic()
    verdict = independent_check(text)
    independent_seconds = time.monotonic() - started
    side = _side(text)
    return {
        "n": n,
        "printed_side": printed,
        "certificate": path.relative_to(ROOT).as_posix(),
        "certificate_sha256": _sha256(data),
        "stored_sha256": _sha256(stored),
        "certified_side": f"{side.numerator}/{side.denominator}",
        "certified_side_decimal": format(ceiling_at(side, 40), "f"),
        "side_increase": f"{float(side - Fraction(printed)):.3e}",
        "center_dilation": result["center_dilation"],
        "pairs_tested": result["pairs_tested"],
        "promotion": "certificate-produced",
        "independent": {
            "verification_passed": verdict["verification_passed"],
            "pairs_tested": verdict["pairs_tested"],
            "minimum_containment_clearance": verdict["minimum_containment_clearance"],
            "failures": verdict["failures"],
        },
        **derived(printed, side),
        "wall_seconds": {
            "promote": round(promote_seconds, 1),
            "independent": round(independent_seconds, 1),
        },
    }


def _units(sources: Sequence[Source], numbers: set[int] | None) -> list[tuple[str, int]]:
    units = [
        (source.id, n)
        for source in sources
        for n in sorted(cases(source))
        if numbers is None or n in numbers
    ]
    # Largest first, so the slowest start first and the pool drains evenly.
    return sorted(units, key=lambda unit: -unit[1])


def _map(function: Any, units: list[tuple[str, int]], workers: int) -> list[dict[str, Any]]:
    if workers <= 1:
        return [function(unit) for unit in units]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(function, units))


def _write_json(path: Path, value: object) -> None:
    """Write a record, as deterministic gzip where the retained-data rule asks for it.

    A packet stores a data file of more than ``LINE_THRESHOLD`` lines as ``X.gz`` (the
    archive's policy, `devtools.retained_data`), and readers take ``X`` and read either,
    so whichever form is written the other is removed.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, indent=2) + "\n"
    packed = compressed_path(path)
    target, stale = (packed, path) if text.count("\n") > LINE_THRESHOLD else (path, packed)
    data = _gzip(text.encode("utf-8")) if target is packed else text.encode("utf-8")
    with atomic_output_file(target) as temporary:
        temporary.write_bytes(data)
    stale.unlink(missing_ok=True)


def certify(sources: Sequence[Source], numbers: set[int] | None, workers: int) -> None:
    rows = _map(certify_one, _units(sources, numbers), workers)
    for source in sources:
        mine = {row["n"]: row for row in rows if row["n"] in cases(source)}
        if not mine:
            continue
        previous = (
            {
                row["n"]: row
                for row in json.loads(read_retained_text(source.certification))["cases"]
            }
            if retained_exists(source.certification)
            else {}
        )
        merged = {**previous, **mine}
        _write_json(
            source.certification,
            {
                "tool": "python -m devtools.upper_bound_packets certify",
                "promotion": {
                    "strategy": "robust-rational",
                    "rational_digits": RATIONAL_DIGITS,
                    "max_side_increase": MAX_SIDE_INCREASE,
                },
                "independent_checker": "devtools.check_rational_witness_independent",
                "cases": [merged[n] for n in sorted(merged)],
            },
        )
        print(f"{source.id}: certified {sorted(mine)}")
        if source.control is not None and source.control[0] in mine:
            _write_json(source.controls, negative_controls(source))
            print(f"{source.id}: negative controls written")


def restamp(sources: Sequence[Source]) -> None:
    """Rewrite each receipt row's `derived` fields from its committed certificate's side.

    For a change in how those fields are derived: it promotes nothing, so the
    certificates, their digests and the recorded walls stay as `certify` wrote them.
    """
    for source in sources:
        record = json.loads(read_retained_text(source.certification))
        for row in record["cases"]:
            text = gzip.decompress(source.certificate(row["n"]).read_bytes()).decode("utf-8")
            row.update(derived(cases(source)[row["n"]]["side"], _side(text)))
        _write_json(source.certification, record)
        print(f"{source.id}: restamped {len(record['cases'])} receipt rows")


def shrink_side(text: str) -> str:
    """The certificate with its side cut by ``1e-15``: containment must now fail."""
    side = _side(text)
    smaller = side - Fraction(1, 10**15)
    return re.sub(
        r"^  side: \S+$",
        f"  side: {smaller.numerator}/{smaller.denominator}",
        text,
        count=1,
        flags=re.MULTILINE,
    )


def shift_square(text: str, square: int, shift: Fraction) -> str:
    """The certificate with one square moved right by ``shift``: a pair must now overlap."""
    lines = text.splitlines(keepends=True)
    start = lines.index(f"  - id: {square}\n")
    out = lines[: start + 2]
    index = start + 2
    while index < len(lines) and lines[index].startswith("    - - "):
        x = Fraction(lines[index].removeprefix("    - - ").strip().strip("'")) + shift
        out.append(f"    - - {x.numerator}/{x.denominator}\n")
        out.append(lines[index + 1])
        index += 2
    return "".join(out + lines[index:])


def negative_controls(source: Source) -> dict[str, Any]:
    """Two mutations of the packet's control certificate, each of which must fail."""
    assert source.control is not None
    control_n, square = source.control
    text = gzip.decompress(source.certificate(control_n).read_bytes()).decode("utf-8")
    controls = {
        "side-shrunk-1e-15": shrink_side(text),
        f"square-{square}-shifted-1e-6": shift_square(text, square, Fraction(1, 10**6)),
    }
    rows = []
    for name, mutated in controls.items():
        verdict = independent_check(mutated)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control.yaml"
            path.write_text(mutated, encoding="utf-8")
            _result, report = exact_verify(load_witness(path, fallback_schema=WITNESS_SCHEMA))
        rows.append(
            {
                "control": name,
                "n": control_n,
                "independent_passed": verdict["verification_passed"],
                "independent_failures": [failure[:160] for failure in verdict["failures"]],
                "exact_verify_passed": report.valid,
            }
        )
    return {
        "tool": "python -m devtools.upper_bound_packets certify",
        "certificate": source.certificate(control_n).relative_to(ROOT).as_posix(),
        "expectation": "every control is refused by both checkers",
        "controls": rows,
    }


# --------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------


def certification(source: Source) -> dict[int, dict[str, Any]]:
    record = json.loads(read_retained_text(source.certification))
    return {int(row["n"]): row for row in record["cases"]}


def fast_problems(source: Source) -> list[str]:
    """What is wrong with a packet, from its retained files alone."""
    problems: list[str] = []
    entry = acquisition(source)
    if entry["source_commit"] != source.revision:
        problems.append(f"{source.id}: acquisition pins {entry['source_commit']}")
    for n, case in sorted(cases(source).items()):
        if source.retain_raw:
            path = source.packet / CASSON_TREE / case["file"]
            match = _CASSON_SIDE.match(path.read_text(encoding="utf-8"))
            if match is None or match.group(1) != case["side"]:
                problems.append(f"{source.id} n={n}: retained file does not print its side")
            continue
        try:
            witness = load_witness(source.fact(n), fallback_schema=WITNESS_SCHEMA)
        except WitnessError as error:
            problems.append(f"{source.id} n={n}: facts do not load: {error}")
            continue
        if witness["n"] != n or witness["side"] != case["side"]:
            problems.append(f"{source.id} n={n}: facts disagree with the acquisition record")
    # An upstream file the policy does not retain must not be in the packet under any
    # name, so every packet file is compared by digest rather than by path.
    held = {_sha256(path.read_bytes()) for path in source.packet.rglob("*") if path.is_file()}
    for record in entry["files"]:
        if record["raw_asset_retained"]:
            data = (source.packet / CASSON_TREE / record["path"]).read_bytes()
            if _sha256(data) != record["sha256"]:
                problems.append(f"{source.id}: {record['path']} differs from its pinned digest")
        elif record["sha256"] in held:
            problems.append(f"{source.id}: {record['path']} is retained against the policy")
    if source.witness_directory is None:
        return problems
    receipts = certification(source)
    if set(receipts) != set(cases(source)):
        problems.append(f"{source.id}: certification receipts do not cover every case")
    for n, row in sorted(receipts.items()):
        problems.extend(
            f"{source.id} n={n}: {problem}" for problem in _receipt_problems(source, n, row)
        )
    if live_receipt(source).is_file():
        rows = json.loads(live_receipt(source).read_text(encoding="utf-8"))["cases"]
        if {row["n"] for row in rows} != set(receipts) or not all(
            row["below_live"] and Decimal(row["printed_side"]) < Decimal(row["live_side"])
            for row in rows
        ):
            problems.append(f"{source.id}: a case is not below the live catalogue it records")
    if source.control is not None and source.control[0] in receipts:
        controls = json.loads(source.controls.read_text(encoding="utf-8"))["controls"]
        if not controls or any(
            row["independent_passed"] or row["exact_verify_passed"] for row in controls
        ):
            problems.append(f"{source.id}: a negative control was accepted")
    return problems


def _receipt_problems(source: Source, n: int, row: Mapping[str, Any]) -> list[str]:
    stored = source.certificate(n).read_bytes()
    problems = []
    if _sha256(stored) != row["stored_sha256"]:
        problems.append("stored certificate differs from its receipt")
    text = gzip.decompress(stored).decode("utf-8")
    if _sha256(text.encode("utf-8")) != row["certificate_sha256"]:
        problems.append("certificate text differs from its receipt")
    side = _side(text)
    printed = cases(source)[n]["side"]
    if f"{side.numerator}/{side.denominator}" != row["certified_side"]:
        problems.append("certified side differs from its receipt")
    if side - Fraction(printed) > Fraction(MAX_SIDE_INCREASE):
        problems.append("certified side exceeds the allowed increase")
    if {key: row.get(key) for key in derived(printed, side)} != derived(printed, side):
        problems.append("receipt's verified value or units above do not follow from it")
    if not row["independent"]["verification_passed"]:
        problems.append("the independent checker refused the certificate")
    return problems


def replay_one(unit: tuple[str, int]) -> dict[str, Any]:
    """Regenerate one certificate and decide the committed one again."""
    source_id, n = unit
    source = BY_ID[source_id]
    committed = gzip.decompress(source.certificate(n).read_bytes()).decode("utf-8")
    started = time.monotonic()
    regenerated, _result = certificate_text(source, n)
    verdict = independent_check(committed)
    return {
        "source": source_id,
        "n": n,
        "regenerated_identical": regenerated == committed,
        "independent_passed": verdict["verification_passed"],
        "seconds": round(time.monotonic() - started, 1),
    }


def replay(sources: Sequence[Source], numbers: set[int] | None, workers: int) -> list[str]:
    problems = []
    for row in _map(replay_one, _units(sources, numbers), workers):
        verdict = row["regenerated_identical"] and row["independent_passed"]
        print(
            f"  {row['source']} n={row['n']}: "
            + ("VERIFIED" if verdict else "FAILED")
            + f" (regenerated identical: {row['regenerated_identical']}, independent: "
            f"{row['independent_passed']}, {row['seconds']} s)",
            flush=True,
        )
        if not verdict:
            problems.append(f"{row['source']} n={row['n']}: replay failed")
    return problems


# --------------------------------------------------------------------------------------
# The live catalogue, and the packet tables
# --------------------------------------------------------------------------------------

LIVE_URL = "https://kingbird.myphotos.cc/packing/squares_in_squares.html"


def live_receipt(source: Source) -> Path:
    return source.receipts / f"live-catalogue-{source.retrieved}.json"


def record_live(catalogue: Path) -> None:
    """Record the live catalogue's side at each certified count, from a page fetched today.

    The page itself is not retained here: refreshing the retained catalogue is a dated
    survey of its own. What is kept is the side it printed at each count these packets
    report, and the digest of the bytes read.
    """
    from devtools.check_source_coverage import parse_kingbird  # noqa: PLC0415

    live = parse_kingbird(catalogue, 1, 324)
    digest = _sha256(catalogue.read_bytes())
    for source in CERTIFIED:
        rows = [
            {
                "n": n,
                "printed_side": case["side"],
                "live_side": live[n],
                "below_live": Decimal(case["side"]) < Decimal(live[n]),
            }
            for n, case in sorted(cases(source).items())
        ]
        _write_json(
            live_receipt(source),
            {
                "tool": "python -m devtools.upper_bound_packets live",
                "url": LIVE_URL,
                "retrieved": source.retrieved,
                "page_sha256": digest,
                "page_retained": False,
                "note": "An unpictured count takes the catalogue's stated grid side.",
                "cases": rows,
            },
        )
        print(f"{source.id}: live sides recorded for {len(rows)} counts")


def _earlier_sides() -> dict[int, tuple[str, str]]:
    """The side this project recorded before the intake, and whose it was.

    Read from the catalogue capture the intake read, never the current one: a later
    capture prints later sides, and this column says what the records held on the day.
    """
    from devtools.check_source_coverage import parse_kingbird  # noqa: PLC0415
    from sqpack.kingbird_catalogue import INTAKE_CATALOGUE_HTML  # noqa: PLC0415

    kingbird = parse_kingbird(ROOT / INTAKE_CATALOGUE_HTML, 1, 324)
    release = json.loads((WEB / "unitsquare-release1-2026/results.json").read_text())
    unitsquare = {int(row["n"]): str(row["offered_side"]) for row in release["results"]}
    return {
        n: (unitsquare[n], "UnitSquare") if n in unitsquare else (kingbird[n], "Kingbird")
        for n in range(1, 325)
    }


def superseding_table(source: Source) -> str:
    """A later packet's per-case table: each side beside the one it replaces.

    The live catalogue is not read here: the column beside it is the retained capture
    that the records compare with, and refreshing that is a dated survey of its own.
    """
    from devtools.check_source_coverage import parse_kingbird  # noqa: PLC0415
    from sqpack.kingbird_catalogue import CATALOGUE_HTML  # noqa: PLC0415

    assert source.supersedes is not None
    before = BY_ID[source.supersedes]
    replaced, replaced_receipts = cases(before), certification(before)
    receipts = certification(source)
    kingbird = parse_kingbird(ROOT / CATALOGUE_HTML, 1, 324)
    casson = cases(CASSON)
    header = (
        "| n | Side printed | Authored (UTC) | Certified side | Verified here | "
        "Side it replaces | Verified before | Lower by | Kingbird, 2026-09-30 | "
        "Casson, 2026-09-23 |"
    )
    lines = [header, "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for n, case in sorted(cases(source).items()):
        row = receipts[n]
        verified = row["verified_value"]
        units = int(row["units_above_printed"])
        plural = "" if units == 1 else "s"
        mark = "" if verified == case["side"] else f" (+{units} unit{plural})"
        old = replaced[n]["side"]
        lower = Decimal(old) - Decimal(case["side"])
        lines.append(
            f"| {n} | `{case['side']}` | "
            f"{case['current_since_authored_utc'][:16].replace('T', ' ')} | "
            f"`{row['certified_side_decimal'][: len(case['side']) + 5]}…` | "
            f"`{verified}`{mark} | `{old}` | `{replaced_receipts[n]['verified_value']}` | "
            f"`{lower:.3e}` | `{kingbird[n]}` | "
            + (f"`{casson[n]['side']}`" if n in casson else "—")
            + " |"
        )
    return "\n".join(lines) + "\n"


def table(source: Source) -> str:
    """The packet README's per-case table, from the retained records."""
    if source.supersedes is not None:
        return superseding_table(source)
    earlier = _earlier_sides()
    receipts = certification(source)
    live = {
        row["n"]: row["live_side"]
        for row in json.loads(live_receipt(source).read_text(encoding="utf-8"))["cases"]
    }
    casson = cases(CASSON)
    header = (
        "| n | Side printed | Current since (UTC) | First packing (authored, UTC) | "
        "Certified side | Verified here | Recorded before (source) | Live, 2026-09-29 | "
        "Casson, 2026-09-23 |"
    )
    lines = [
        header,
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for n, case in sorted(cases(source).items()):
        row = receipts[n]
        history = case.get("history") or []
        first = (
            f"`{history[0]['side']}`, {history[0]['authored_utc'][:16].replace('T', ' ')}"
            if history
            else "the same"
        )
        if history and history[0]["side"] == case["side"]:
            first = "the same"
        side, whose = earlier[n]
        verified = row["verified_value"]
        units = int(row["units_above_printed"])
        plural = "" if units == 1 else "s"
        mark = "" if verified == case["side"] else f" (+{units} unit{plural})"
        lines.append(
            f"| {n} | `{case['side']}` | "
            f"{case['current_since_authored_utc'][:16].replace('T', ' ')} | {first} | "
            f"`{row['certified_side_decimal'][: len(case['side']) + 5]}…` | "
            f"`{verified}`{mark} | `{side}` ({whose}) | `{live[n]}` | "
            + (f"`{casson[n]['side']}`" if n in casson else "—")
            + " |"
        )
    return "\n".join(lines) + "\n"


def priority_table() -> str:
    """Casson's side at each count beside Couzo's first and current, with their clocks."""
    couzo = cases(FRANCISCOUZO)
    header = (
        "| n | Casson\u2019s side (authored 2026-09-24 04:45 UTC) | Couzo\u2019s first side | "
        "Authored (UTC) | Committed (UTC) | First by the authors\u2019 clocks | "
        "Couzo\u2019s side now |"
    )
    lines = [
        header,
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for n, case in sorted(cases(CASSON).items()):
        first = couzo[n]["history"][0]
        earlier = "Couzo" if first["authored_utc"] < case["first_authored_utc"] else "Casson"
        lines.append(
            f"| {n} | `{case['side']}` | `{first['side']}` | "
            f"{first['authored_utc'][:16].replace('T', ' ')} | "
            f"{first['committed_utc'][:16].replace('T', ' ')} | {earlier} | "
            f"`{couzo[n]['side']}` |"
        )
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------


def _numbers(values: Sequence[int] | None) -> set[int] | None:
    return set(values) if values else None


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    grab = commands.add_parser("acquire", help="write a packet from a pinned local clone")
    grab.add_argument("--source", choices=tuple(BY_ID), required=True)
    grab.add_argument("--clone", type=Path, required=True)
    for name, text in (("certify", "write certificates and receipts"), ("check", "check")):
        command = commands.add_parser(name, help=text)
        command.add_argument("--source", choices=tuple(source.id for source in CERTIFIED))
        command.add_argument("--n", type=int, action="append")
        command.add_argument("--workers", type=int, default=1)
    commands.choices["check"].add_argument(
        "--replay", action="store_true", help="regenerate and re-decide every certificate"
    )
    again = commands.add_parser("restamp", help="re-derive receipts' fields, promoting nothing")
    again.add_argument("--source", choices=tuple(source.id for source in CERTIFIED))
    live = commands.add_parser("live", help="record the live catalogue's sides")
    live.add_argument("--catalogue", type=Path, required=True, help="a page fetched today")
    show = commands.add_parser("table", help="print a packet README's per-case table")
    show.add_argument("--source", choices=tuple(BY_ID), required=True)
    args = parser.parse_args(argv)
    if args.command == "acquire":
        acquire(BY_ID[args.source], args.clone)
        print(f"wrote {BY_ID[args.source].packet.relative_to(ROOT)}")
        return 0
    if args.command == "live":
        record_live(args.catalogue)
        return 0
    if args.command == "table":
        source = BY_ID[args.source]
        print(priority_table() if source is CASSON else table(source), end="")
        return 0
    chosen = [BY_ID[args.source]] if args.source else list(CERTIFIED)
    if args.command in {"certify", "restamp"}:
        if args.command == "certify":
            certify(chosen, _numbers(args.n), args.workers)
        else:
            restamp(chosen)
        return 0
    problems = [problem for source in (*chosen, CASSON) for problem in fast_problems(source)]
    if args.replay and not problems:
        problems = replay(chosen, _numbers(args.n), args.workers)
    for problem in problems:
        print(f"FAIL {problem}", file=sys.stderr)
    if problems:
        return 1
    total = sum(len(cases(source)) for source in chosen)
    what = "replayed from the retained facts" if args.replay else "checked"
    print(f"upper-bound packets: {total} certificates {what}; Casson's packet pinned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
