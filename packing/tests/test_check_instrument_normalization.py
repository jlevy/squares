"""Controls for the pre-freeze instrument-normalization check.

The positive control is the real repository, which must pass today: every Python file
bound by an immutable result is either formatter-clean or excluded from formatting. The
negative control is a synthetic tree carrying two unformatted bound files, one excluded
and one not, and only the second may be refused -- a check that refuses both would just
be a formatter, and a check that refuses neither would never have caught anything.
"""

from __future__ import annotations

import json
import pathlib
import textwrap

from devtools import check_instrument_normalization as normalization

UNFORMATTED = "def instrument(  x ):\n    return    x+1\n"

PYPROJECT = textwrap.dedent(
    """
    [tool.ruff]
    line-length = 96
    extend-exclude = ["resources"]

    [tool.ruff.format]
    exclude = ["cases/frozen/excluded_instrument.py"]
    """
).strip()


def _fixture(root: pathlib.Path, *, bound: dict[str, str]) -> None:
    (root / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")
    results = root / "campaign" / "series" / "series-000-fixture" / "results"
    results.mkdir(parents=True)
    (results / "exp-999-fixture.json").write_text(
        json.dumps({"instrument_bindings": bound}, indent=2),
        encoding="utf-8",
    )
    for relative in bound:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(UNFORMATTED, encoding="utf-8")


def test_real_repository_normalization_is_clean() -> None:
    """Positive control: every bound instrument file in this repository is safe today."""
    receipt = normalization.report(normalization.ROOT)

    assert receipt["bound_python_files"] > 0, "the check must actually be reaching bindings"
    assert receipt["violations"] == []
    assert receipt["ok"] is True
    assert normalization.main([]) == 0


def test_unformatted_and_unexcluded_binding_is_refused(tmp_path: pathlib.Path) -> None:
    """Negative control: an unformatted bound file with no exclusion must be refused."""
    digest = "a" * 64
    _fixture(
        tmp_path,
        bound={
            "cases/frozen/excluded_instrument.py": digest,
            "cases/frozen/exposed_instrument.py": digest,
        },
    )

    receipt = normalization.report(tmp_path)

    statuses = {entry["path"]: entry["status"] for entry in receipt["bindings"]}
    assert statuses["cases/frozen/excluded_instrument.py"] == "excluded"
    assert statuses["cases/frozen/exposed_instrument.py"] == "unformatted-and-not-excluded"
    assert [entry["path"] for entry in receipt["violations"]] == [
        "cases/frozen/exposed_instrument.py"
    ]
    assert receipt["ok"] is False
    assert normalization.main(["--root", str(tmp_path)]) == 1
    assert normalization.main(["--root", str(tmp_path), "--json"]) == 1


def test_missing_bound_file_is_refused(tmp_path: pathlib.Path) -> None:
    """A binding that names a path no longer in the tree cannot be checked, so it fails."""
    _fixture(tmp_path, bound={"cases/frozen/exposed_instrument.py": "b" * 64})
    (tmp_path / "cases" / "frozen" / "exposed_instrument.py").unlink()

    receipt = normalization.report(tmp_path)

    assert [entry["status"] for entry in receipt["violations"]] == ["missing"]
    assert normalization.main(["--root", str(tmp_path)]) == 1
