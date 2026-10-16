"""The controls of #639's replay: the source's checker accepts a retained exact form and
refuses it mutated.

`T-193`'s replay ran Evan Daniel's `verify_exact.py` unchanged from its retained copy on
all 23 exact forms of evand/square-packing at 7d1407a, with four mutated controls at each
count (`packing/resources/web/evand-exact-cur-2026-10-16/review/replay_verify_exact.py`,
receipt `receipts/replay-verify-exact.json`). This holds the smallest retained form, n =
51, to the same outcomes: the original is VALID with the statement the source prints, and
a square moved through the wall it touches and a duplicate square are refused.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

PACKING = Path(__file__).resolve().parents[1]
WEB = PACKING / "resources/web"
CHECKER = WEB / "evand-exact-and-local-reports-2026-10-12/source/search/exact/verify_exact.py"
DATA = WEB / "evand-exact-cur-2026-10-16/source/search/exact/cur/data"
FORM = DATA / "n-51.minpoly.json.gz"


def check(path: Path) -> tuple[int, str]:
    shown = subprocess.run(
        (sys.executable, "-I", str(CHECKER), str(path)),
        capture_output=True,
        text=True,
        check=False,
    )
    lines = shown.stdout.strip().splitlines()
    return shown.returncode, lines[-1] if lines else ""


def written(tmp_path: Path, name: str, data: dict[str, object]) -> Path:
    path = tmp_path / name
    path.write_bytes(gzip.compress(json.dumps(data).encode("utf-8"), mtime=0))
    return path


def form() -> dict[str, object]:
    return json.loads(gzip.decompress(FORM.read_bytes()).decode("utf-8"))


def test_the_checker_is_the_copy_the_replay_read() -> None:
    digest = hashlib.sha256(CHECKER.read_bytes()).hexdigest()
    assert digest == "a0f38ca87c13c7e1b1d6ca99d69adea47df6008a645e3b4dbb79e8e0af35bab4"


def test_the_retained_form_is_valid_as_the_source_prints() -> None:
    status, line = check(FORM)
    printed = (DATA / "verify.txt").read_text(encoding="utf-8").splitlines()[0]
    assert status == 0
    assert line.split(": ", 1)[1] == printed.split(": ", 1)[1]


def test_a_square_moved_through_its_wall_is_refused(tmp_path: Path) -> None:
    data = form()
    equations = data["equations"]
    squares = data["squares"]
    assert isinstance(equations, list)
    assert isinstance(squares, list)
    _, square, _, wall = next(item for item in equations if item[0] == "W")
    coordinate, sign = {"L": ("x", -1), "R": ("x", 1), "B": ("y", -1), "T": ("y", 1)}[wall]
    values = squares[square][coordinate]
    values[0] = str(Fraction(values[0]) + sign * Fraction(1, 10**6))
    status, line = check(written(tmp_path, "moved.json.gz", data))
    assert status == 1
    assert "NOT VERIFIED" in line
    assert "outside the box" in line


def test_a_duplicate_square_is_refused(tmp_path: Path) -> None:
    data = form()
    squares = data["squares"]
    assert isinstance(squares, list)
    squares[1] = json.loads(json.dumps(squares[0]))
    status, line = check(written(tmp_path, "duplicate.json.gz", data))
    assert status == 1
    assert "NOT VERIFIED" in line
    assert "no separating line" in line
