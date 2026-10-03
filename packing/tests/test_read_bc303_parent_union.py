"""Geometry and source-content controls for the BC303 parent reader; its audit replay."""

# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
import subprocess
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import audit_bc303_parent_union as audit
from devtools import read_bc303_parent_union as reader

REPO = Path(__file__).resolve().parents[2]
AGENDA_035 = REPO / (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-035"
)


def test_closed_union_counts_contact_atoms_once() -> None:
    atoms: tuple[reader.Atom, ...] = (
        ((Fraction(0), Fraction(0)), Fraction(1, 4)),
        ((Fraction(1), Fraction(1, 2)), Fraction(1, 3)),
        ((Fraction(2), Fraction(1, 2)), Fraction(1, 5)),
        ((Fraction(2) + Fraction(1, 10), Fraction(1, 2)), Fraction(1, 7)),
    )
    first = (Fraction(0), Fraction(0), Fraction(1), Fraction(1))
    second = (Fraction(1), Fraction(0), Fraction(2), Fraction(1))
    assert reader.parent_union_mass(atoms, (first,)) == Fraction(7, 12)
    assert reader.parent_union_mass(atoms, (first, second)) == Fraction(47, 60)
    assert reader.parent_union_mass(atoms, (first, first)) == Fraction(7, 12)


def test_parent_geometry_refuses_invalid_squares() -> None:
    atoms: tuple[reader.Atom, ...] = (((Fraction(0), Fraction(0)), Fraction(1)),)
    with pytest.raises(reader.ParentUnionError, match="empty"):
        reader.parent_union_mass(atoms, ())
    with pytest.raises(reader.ParentUnionError, match="unit square"):
        reader.parent_union_mass(atoms, ((Fraction(0), Fraction(0), Fraction(2), Fraction(1)),))
    with pytest.raises(reader.ParentUnionError, match="outside container"):
        reader.parent_union_mass(
            atoms, ((Fraction(-1), Fraction(0), Fraction(0), Fraction(1)),)
        )


def test_source_content_is_checked_and_its_layout_is_not() -> None:
    data = (REPO / reader.SOURCE_PATH).read_bytes()
    atoms = reader.parse_measure(data)
    assert len(atoms) == 377
    # The same measure serialized differently is the same measure (OR-16).
    assert reader.parse_measure(json.dumps(json.loads(data), indent=2).encode()) == atoms
    document = json.loads(data)
    document["total_mass"] = "1"
    with pytest.raises(reader.ParentUnionError, match="measure constants changed"):
        reader.parse_measure(json.dumps(document).encode())
    document = json.loads(data)
    document["atoms"][0][2] = "1"
    with pytest.raises(reader.ParentUnionError, match="does not equal source total"):
        reader.parse_measure(json.dumps(document).encode())
    with pytest.raises(reader.ParentUnionError, match="duplicate JSON key"):
        reader.parse_measure(b'{"atoms":[],"atoms":[]}')


def test_the_bound_measure_records_revisions_and_reports_drift_without_refusing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    head = subprocess.run(
        ("git", "-C", str(REPO), "rev-parse", "HEAD"),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    measure = reader.load_bound_measure(REPO)
    assert measure.source_revision == reader.SOURCE_REVISION
    assert measure.implementation_revision == head
    assert len(measure.atoms) == 377

    original_git = reader._git

    def edited_reader(repository: Path, *arguments: str) -> bytes:
        if arguments[0] == "status":
            return f" M {reader.READER_PATH}\n".encode()
        return original_git(repository, *arguments)

    monkeypatch.setattr(reader, "_git", edited_reader)
    drifted = reader.load_bound_measure(REPO)
    assert drifted.implementation_dirty is True
    assert drifted.atoms == measure.atoms


def test_the_independent_audit_replays_the_retained_exp159_receipt() -> None:
    """The arithmetic replay reproduces every retained audit value but the old digest."""
    retained = json.loads(
        (AGENDA_035 / "exp-159-bc303-literal-parent-union-audit.json").read_text()
    )
    result = audit.audit(REPO, AGENDA_035 / "exp-159-bc303-literal-parent-union.json")
    del retained["source_sha256"]
    assert {key: result[key] for key in retained} == retained
    assert result["source_path"] == audit.SOURCE_PATH
