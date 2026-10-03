"""The branch-and-bound verifier re-proves Taylor certificates and refuses doctored ones."""

from __future__ import annotations

import gzip
import hashlib
import json
import shutil
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import pilot_n17_subpattern_bb as bb
from devtools import verify_n17_bb_certificate as verifier


def rectangle(x0: str, x1: str) -> tuple[tuple[Q, Q], ...]:
    a, b, c, d = Q(x0), Q(x1), Q("2.00"), Q("2.05")
    return ((a, c), (b, c), (b, d), (a, d))


# A crowded row in the open, and one against the west wall (wall rows referenced).
CASES = {
    "row": (rectangle("1.00", "1.05"), rectangle("1.40", "2.40"), rectangle("2.94", "2.99")),
    "wall": (rectangle("0.50", "0.60"), rectangle("0.95", "1.95"), rectangle("2.40", "2.45")),
}
NAMES = ("a", "b", "c")


def cells_of(directory: Path, case: str) -> verifier.Cells:
    path = directory / f"cells-{case}.json"
    document = {
        "U": str(bb.cover.U),
        "order": list(NAMES),
        "cells": {
            name: [[str(x), str(y)] for x, y in polygon]
            for name, polygon in zip(NAMES, CASES[case], strict=True)
        },
    }
    _ = path.write_text(json.dumps(document), encoding="utf-8")
    return verifier.file_cells(path, hashlib.sha256(path.read_bytes()).hexdigest())


@pytest.fixture(scope="module")
def taylor_certificates(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    """Taylor certificates of both cases, made once."""
    made: dict[str, Path] = {}
    for case, polygons in CASES.items():
        directory = tmp_path_factory.mktemp(f"taylor-{case}")
        pattern = bb.Pattern(NAMES, polygons, bb.cover.U)
        result = bb.search(
            pattern, bb.Settings(taylor=True, obbt_rounds=0), certificate=directory
        )
        assert result["verdict"] == "certified-infeasible"
        made[case] = directory
    return made


@pytest.mark.parametrize("case", sorted(CASES))
def test_the_verifier_passes_taylor_certificates(
    tmp_path: Path, taylor_certificates: dict[str, Path], case: str
) -> None:
    receipt = verifier.verify_certificate(taylor_certificates[case], cells_of(tmp_path, case))
    assert receipt["status"] == "PASS", receipt["failures"]
    assert receipt["checked_nodes"] == receipt["nodes"] > 1
    assert receipt["counts"]["taylor_cut_ok"] > 0
    if case == "wall":
        assert receipt["counts"]["wall_ok"] > 0


def read_named(directory: Path, name: str) -> Any:
    return json.loads(gzip.decompress((directory / f"{name}.json.gz").read_bytes()))


def write_named(directory: Path, document: Any) -> str:
    data = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    name = hashlib.sha256(data.encode()).hexdigest()
    (directory / f"{name}.json.gz").write_bytes(gzip.compress(data.encode(), mtime=0))
    return name


def rational(q: Q) -> str:
    return f"{q.numerator}/{q.denominator}"


def referenced(record: dict[str, Any], kind: str) -> list[Any] | None:
    """The first row of `kind` ("taylor" or "w") that a multiplier references, if any."""
    lists = [record.get("farkas", [])] + [b[3] for b in record.get("bounds", [])]
    for weights in lists:
        for ref, _ in weights:
            if kind == "w" and ref[0] == "w":
                return record["walls"][ref[1]]
            if kind == "taylor" and ref[0] == "u" and len(record["cuts"][ref[1]]) == 8:
                return record["cuts"][ref[1]]
    return None


def corrupt(directory: Path, kind: str) -> str | None:
    """One change to a Taylor certificate, re-hashed; the new manifest, or None."""
    manifest = read_named(directory, verifier.manifest_from_readme(directory))
    chunks = [read_named(directory, c)["nodes"] for c in manifest["chunks"]]
    nodes = [n for chunk in chunks for n in chunk]
    settings = manifest["header"]["settings"]
    found: tuple[dict[str, Any], dict[str, Any], list[Any]] | None = None
    for node in nodes:
        for record in node["rounds"]:
            row = referenced(record, "w" if kind == "wall_a" else "taylor")
            if row is not None:
                found = (node, record, row)
                break
        if found is not None:
            break
    if kind == "taylor_k":
        settings["taylor_k"] = "1/4"
    elif kind == "interval_claim":
        del settings["taylor"], settings["taylor_k"]
        manifest["schema"] = bb.CERTIFICATE_SCHEMA
    elif kind == "schema":
        manifest["schema"] = bb.CERTIFICATE_SCHEMA
    elif found is None:
        return None
    else:
        node, _, row = found
        if kind == "taylor_v":
            row[3] = rational(Q(row[3]) + Q(1, 10**6))
        elif kind == "taylor_b":
            row[7] = rational(Q(row[7]) + Q(1, 2))
        elif kind == "taylor_signs":
            row[5] = -row[5]
        elif kind == "centre":
            i, _ = manifest["header"]["pairs"][row[0]]
            centres = node["taylor"]["centres"]
            centres[i] = rational(Q(centres[i]) + Q(1, 10))
        elif kind == "no_centres":
            del node["taylor"]
        elif kind == "wall_a":
            row[6] = rational(Q(row[6]) + Q(1, 10**6))
        else:
            raise ValueError(kind)
    manifest["chunks"] = [write_named(directory, {"nodes": chunk}) for chunk in chunks]
    return write_named(directory, manifest)


KINDS = (
    "taylor_v",
    "taylor_b",
    "taylor_signs",
    "centre",
    "no_centres",
    "wall_a",
    "taylor_k",
    "interval_claim",
    "schema",
)


@pytest.mark.parametrize("kind", KINDS)
def test_the_verifier_refuses_each_doctored_taylor_kind(
    tmp_path: Path, taylor_certificates: dict[str, Path], kind: str
) -> None:
    refused = 0
    for case, certificate in taylor_certificates.items():
        directory = tmp_path / case
        _ = shutil.copytree(certificate, directory)
        manifest = corrupt(directory, kind)
        if manifest is None:
            continue
        receipt = verifier.verify_certificate(
            directory, cells_of(tmp_path, case), manifest=manifest
        )
        assert receipt["status"] == "FAIL", (kind, case)
        refused += 1
    assert refused > 0, f"no certificate carries a {kind} record"


def test_the_exact_taylor_bound_is_the_lp_value() -> None:
    """The Lagrangian candidates give the LP's value on a hand-solved instance."""
    # min x - t over x in [0, 2], y in [0, 2], t in [-1, 1], with x - t >= 1/2 (c = 1,
    # b = 1, a = 1/2, o = 0, normal (1, 0)): the value is 1/2.
    plane = (Q(1), Q(0), Q(1, 2), Q(1), Q(0))
    value = verifier.taylor_plane_min(
        (Q(1), Q(0)), Q(1), plane, (Q(1, 2), Q(1)), ((Q(0), Q(2)), (Q(0), Q(2)), (Q(-1), Q(1)))
    )
    assert value == Q(1, 2)
    # Without the constraint's help the bound is the box minimum, -1.
    loose = verifier.taylor_plane_min(
        (Q(1), Q(0)), Q(1), plane, (Q(-10), Q(1)), ((Q(0), Q(2)), (Q(0), Q(2)), (Q(-1), Q(1)))
    )
    assert loose == Q(-1)
