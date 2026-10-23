"""The stage 4 review's grade-C checker accepts retained exact forms and refuses them mutated.

The mathematical review of Evan Daniel's Theorem C
(`docs/project/reviews/review-2026-10-23-evand-grade-c-theorem-c.md`, bead think-7scz)
wrote `check_theorem_c.py` from the theorem as it re-derives it and ran it on all 233
configurations the release's grade-C archive certifies (receipts in the exact-data
packet). This holds the program to the bytes the receipts name, holds n = 10 and n = 19
to the outcomes the receipts record (n = 19 needs affine null vectors along a
six-dimensional flat family), and holds two mutated inputs to refusal: a load-bearing
square moved by 10^-30, so that a row is no longer tight, and the right-wall rows removed,
so that no strictly positive multipliers exist. It also holds the Hessian test to
refusing an indefinite matrix. Nothing here runs the source's code.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import json
import tarfile
from fractions import Fraction
from pathlib import Path

PACKING = Path(__file__).resolve().parents[1]
PACKET = PACKING / "resources/web/evand-exact-data-2026-10-12"
CHECKER = PACKET / "review/check_theorem_c.py"
DATA = PACKET / "source/search/exact/minpoly/data"
ARCHIVE = PACKET / "acquisition/release/gradec-233.tar.zst"
RECEIPTS = PACKET / "receipts/review-theorem-c-233.jsonl"


def checker() -> object:
    spec = importlib.util.spec_from_file_location("check_theorem_c", CHECKER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def form(n: int) -> dict[str, object]:
    stored = (DATA / f"n-{n}.minpoly.json.gz").read_bytes()
    data = json.loads(gzip.decompress(stored).decode("utf-8"))
    assert isinstance(data, dict)
    return data


def contacts(n: int) -> dict[str, object]:
    with tarfile.open(ARCHIVE, "r:zst") as archive:
        member = archive.extractfile(f"gradec-233/certs/n-{n}.contacts.json")
        assert member is not None
        data = json.loads(member.read())
    assert isinstance(data, dict)
    return data


def receipt(n: int) -> dict[str, object]:
    for line in RECEIPTS.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record["n"] == n:
            assert isinstance(record, dict)
            return record
    raise AssertionError(f"no receipt for n = {n}")


def verdict(n: int, data: dict[str, object], rows: dict[str, object]) -> tuple[bool, str]:
    check_count = checker().check_count  # type: ignore[attr-defined]
    try:
        result = check_count(n, data, rows, svd=False)
    except AssertionError as refusal:
        return False, str(refusal)
    return bool(result["valid"]), str(result.get("reason"))


def test_the_program_is_the_copy_the_receipts_name() -> None:
    digest = hashlib.sha256(CHECKER.read_bytes()).hexdigest()
    lines = RECEIPTS.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 233
    for line in lines:
        assert json.loads(line)["environment"]["program_sha256"] == digest


def test_n10_and_n19_are_valid_as_the_receipts_record() -> None:
    check_count = checker().check_count  # type: ignore[attr-defined]
    for n in (10, 19):
        result = check_count(n, form(n), contacts(n), svd=False)
        recorded = receipt(n)
        assert result["valid"] is True
        for key in ("rows", "side_end_rows", "rank_L0", "dim_F", "dim_W", "lifts_solved"):
            assert result[key] == recorded[key], key
        assert abs(result["lambda_min"] - recorded["lambda_min"]) < 1e-12
    assert receipt(19)["side_end_rows_slipping"] == 16


def test_a_square_moved_by_a_tiny_amount_is_refused() -> None:
    data = form(10)
    squares = data["squares"]
    assert isinstance(squares, list)
    moved = squares[8]["x"]
    moved[0] = str(Fraction(moved[0]) + Fraction(1, 10**30))
    valid, reason = verdict(10, data, contacts(10))
    assert not valid
    assert "not tight" in reason or "separated" in reason


def test_without_the_right_wall_rows_no_multipliers_are_positive() -> None:
    rows = contacts(10)
    listed = rows["load_bearing"]
    assert isinstance(listed, list)
    rows["load_bearing"] = [row for row in listed if not (row[0] == "W" and row[3] == "R")]
    valid, reason = verdict(10, form(10), rows)
    assert not valid
    assert "multiplier" in reason or "linear program" in reason


def test_the_hessian_test_refuses_an_indefinite_matrix() -> None:
    module = checker()
    field = module.RationalField(["0", "1"])  # type: ignore[attr-defined]
    ldl = module.ldl_pivots  # type: ignore[attr-defined]
    _, definite = ldl(field, [[Fraction(2), Fraction(1)], [Fraction(1), Fraction(2)]])
    _, indefinite = ldl(field, [[Fraction(1), Fraction(2)], [Fraction(2), Fraction(1)]])
    assert definite is True
    assert indefinite is False
