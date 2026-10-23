"""`devtools.lean_closure` reads a Lean import closure from Git objects at a pinned commit."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from devtools import lean_closure
from devtools.lean_closure import Source, closure, escape_counts, header_imports

SCRATCH_GIT = (
    "-c",
    "user.name=lean closure test",
    "-c",
    "user.email=lean-closure-test@example.invalid",
    "-c",
    "commit.gpgsign=false",
    "-c",
    "core.hooksPath=/dev/null",
)

FILES: dict[str, str] = {
    "lean/lean-toolchain": "leanprover/lean4:v4.33.1\n",
    "lean/lakefile.toml": 'name = "pkg"\n\n[[lean_lib]]\nname = "Pkg"\n',
    "lean/lake-manifest.json": json.dumps(
        {"packages": [{"name": "mathlib", "rev": "0df444a3", "inputRev": "v4.33.1"}]}
    ),
    "lean/Pkg/Spec.lean": "import Mathlib\n\ndef spec : Nat := 1\n",
    "lean/Pkg/Lemma.lean": (
        "/- A header comment: import Pkg.Unused -/\n"
        "import Pkg.Spec\n"
        "import Mathlib.Data.Real.Basic  -- trailing comment\n\n"
        "theorem l : True := by sorry\n"
        "-- native_decide in a comment is not counted\n"
    ),
    "lean/Pkg/Top.lean": (
        "module\n\npublic import Pkg.Lemma\nimport all Pkg.Spec\nimport Pkg.Gen.Data\n\n"
        "theorem t : True := trivial\n"
    ),
    "lean/Pkg/Unused.lean": "theorem u : True := trivial\n",
    "lean/Other.lean": "axiom bad : False\n",
}


def _git(checkout: Path, *arguments: str) -> str:
    done = subprocess.run(
        ("git", "-C", str(checkout), *SCRATCH_GIT, *arguments),
        capture_output=True,
        text=True,
        check=True,
        env={
            "PATH": "/usr/bin:/bin",
            "GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z",
            "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z",
        },
    )
    return done.stdout.strip()


@pytest.fixture
def repo(tmp_path: Path) -> tuple[Path, str]:
    checkout = tmp_path / "upstream"
    checkout.mkdir()
    _git(checkout, "init", "--quiet")
    for name, text in FILES.items():
        path = checkout / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    _git(checkout, "add", "-A")
    _git(checkout, "commit", "--quiet", "-m", "pin")
    commit = _git(checkout, "rev-parse", "HEAD")
    # A later edit of the working tree must not change what the commit is read as.
    (checkout / "lean/Pkg/Spec.lean").write_text("import Pkg.Unused\n", encoding="utf-8")
    return checkout, commit


def test_header_imports_skip_comments_and_stop_at_the_first_command() -> None:
    text = (
        "/- import Hidden -/\nmodule\nimport A.B C\npublic meta import D\n\n"
        "def x := 1\nimport E\n"
    )
    assert header_imports(text) == ["A.B", "C", "D"]


def test_escape_counts_ignore_comments() -> None:
    counts = escape_counts("theorem t : True := by sorry -- native_decide\n/- axiom x -/\n")
    assert counts[r"\bsorry\b"] == 1
    assert counts[r"\bnative_decide\b"] == 0
    assert counts[r"^\s*axiom\b"] == 0


def test_closure_follows_project_imports_at_the_commit(repo: tuple[Path, str]) -> None:
    checkout, commit = repo
    report = closure(Source(checkout, commit), "lean", ["Pkg.Top"])
    assert report["commit"] == commit
    assert report["toolchain"] == "leanprover/lean4:v4.33.1"
    assert report["libraries"] == ["Pkg"]
    assert report["packages"] == [
        {"name": "mathlib", "rev": "0df444a3", "input_rev": "v4.33.1"}
    ]
    assert [m["module"] for m in report["modules"]] == ["Pkg.Lemma", "Pkg.Spec", "Pkg.Top"]
    assert report["missing"] == ["Pkg.Gen.Data"]
    assert report["external"] == {"Mathlib": 2}
    assert report["escapes"][r"\bsorry\b"] == 1
    assert report["escapes"][r"^\s*axiom\b"] == 0
    assert report["scope"] == [
        "lean/Pkg/Lemma.lean",
        "lean/Pkg/Spec.lean",
        "lean/Pkg/Top.lean",
        "lean/lake-manifest.json",
        "lean/lakefile.toml",
        "lean/lean-toolchain",
    ]
    spec = next(m for m in report["modules"] if m["module"] == "Pkg.Spec")
    assert spec["imports"] == ["Mathlib"]
    assert spec["blob"] == _git(checkout, "rev-parse", f"{commit}:lean/Pkg/Spec.lean")


def test_main_writes_the_report(repo: tuple[Path, str], tmp_path: Path) -> None:
    checkout, commit = repo
    out = tmp_path / "closure.json"
    code = lean_closure.main(
        [str(checkout), "--commit", commit, "--root", "lean", "Pkg.Lemma", "--json", str(out)]
    )
    assert code == 0
    report = json.loads(out.read_text(encoding="utf-8"))
    assert report["kind"] == lean_closure.KIND
    assert [m["module"] for m in report["modules"]] == ["Pkg.Lemma", "Pkg.Spec"]
