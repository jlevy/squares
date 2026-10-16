"""The controls of #639's replay: the source's checker accepts a retained exact form and
refuses it mutated.

`T-193`'s replay ran Evan Daniel's `verify_exact.py` unchanged from its retained copy on
all 23 exact forms of evand/square-packing at 7d1407a, with four mutated controls at each
count (`packing/resources/web/evand-exact-cur-2026-10-16/review/replay_verify_exact.py`,
receipt `receipts/replay-verify-exact.json`). This holds the smallest retained form, n =
51, to the same outcomes: the original is VALID with the statement the source prints, and
a square moved through the wall it touches and a duplicate square are refused. It also
holds the replay driver's irreducibility test to refusing a perfect power, and its resume
cache to reusing only a record of the same run.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
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
DRIVER = WEB / "evand-exact-cur-2026-10-16/review/replay_verify_exact.py"


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


def driver() -> object:
    spec = importlib.util.spec_from_file_location("replay_verify_exact", DRIVER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def with_polynomial(tmp_path: Path, name: str, low_first: list[int]) -> Path:
    data = form()
    side = data["S"]
    assert isinstance(side, dict)
    side["poly"] = [str(c) for c in low_first]
    return written(tmp_path, name, data)


def test_the_irreducibility_test_refuses_a_perfect_power(tmp_path: Path) -> None:
    factored = driver().factored  # type: ignore[attr-defined]
    # x^2 - 2 is irreducible; (x^2 - 2)^2 = x^4 - 4x^2 + 4 is not, nor is it squarefree;
    # (x^2 - 2)(x^2 - 3) = x^4 - 5x^2 + 6 is squarefree and reducible.
    prime = factored(with_polynomial(tmp_path, "prime.json.gz", [-2, 0, 1]))
    square = factored(with_polynomial(tmp_path, "square.json.gz", [4, 0, -4, 0, 1]))
    product = factored(with_polynomial(tmp_path, "product.json.gz", [6, 0, -5, 0, 1]))
    assert (prime["squarefree"], prime["irreducible"]) == (True, True)
    assert (square["squarefree"], square["irreducible"]) == (False, False)
    assert square["factors"] == [[2, 2]]
    assert (product["squarefree"], product["irreducible"]) == (True, False)


def test_the_resume_cache_reuses_only_the_same_run(tmp_path: Path) -> None:
    module = driver()
    cached, run_key = module.cached, module.run_key  # type: ignore[attr-defined]
    calls: list[str] = []

    def job(label: str) -> object:
        return lambda: calls.append(label) or {"ran": label}

    first = cached(tmp_path, "n-51", run_key("a" * 64, None), job("first"))
    again = cached(tmp_path, "n-51", run_key("a" * 64, None), job("again"))
    changed = cached(tmp_path, "n-51", run_key("b" * 64, None), job("changed"))
    control = cached(tmp_path, "n-51", run_key("b" * 64, "duplicate"), job("control"))
    assert (first, again, changed, control) == (
        {"ran": "first"},
        {"ran": "first"},
        {"ran": "changed"},
        {"ran": "control"},
    )
    assert calls == ["first", "changed", "control"]
