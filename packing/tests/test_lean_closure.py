"""`devtools.lean_closure` reads a Lean import closure from Git objects at a pinned commit."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from devtools import lean_closure
from devtools.lean_closure import Source, closure, escape_counts, header_imports
from devtools.retained_data import git_blob

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


@pytest.mark.parametrize(
    "line",
    [
        "theorem n : 2 + 2 = 4 := by decide +native\n",
        "theorem n : 2 + 2 = 4 := by decide +kernel +native\n",
        "theorem n : 2 + 2 = 4 := by decide (config := { native := true })\n",
        "def b : Bool := Lean.reduceBool true\n",
        "theorem n : True := Lean.trustCompiler.elim\n",
    ],
)
def test_escape_counts_find_native_evaluation_that_never_names_of_reduce_bool(
    line: str,
) -> None:
    # `decide +native` compiles to `Lean.ofReduceBool` through `Lean.trustCompiler`
    # without the module's text naming either, so it needs tokens of its own.
    assert sum(escape_counts(line).values()) == 1
    assert sum(escape_counts(f"-- {line}/- {line} -/\n").values()) == 0


SECRET = "ghp_" + "0123456789abcdefghij"


@pytest.mark.parametrize(
    ("url", "public"),
    [
        (
            f"https://x-access-token:{SECRET}@example.invalid/o/r.git",
            "https://example.invalid/o/r.git",
        ),
        (f"https://{SECRET}@example.invalid/o/r", "https://example.invalid/o/r"),
        (f"http://proxy:{SECRET}@127.0.0.1:8080/git/o/r", "http://127.0.0.1:8080/git/o/r"),
        ("https://example.invalid/o/r.git", "https://example.invalid/o/r.git"),
        ("git@example.invalid:o/r.git", "git@example.invalid:o/r.git"),
    ],
)
def test_public_url_drops_the_authority_s_credentials(url: str, public: str) -> None:
    assert lean_closure.public_url(url) == public


def test_the_receipt_never_carries_the_remote_s_credentials(
    repo: tuple[Path, str], tmp_path: Path
) -> None:
    checkout, commit = repo
    _git(
        checkout,
        "remote",
        "add",
        "origin",
        f"https://x-access-token:{SECRET}@example.invalid/o/r.git",
    )
    report = closure(Source(checkout, commit), "lean", ["Pkg.Spec"])
    assert report["source_url"] == "https://example.invalid/o/r.git"
    assert SECRET not in json.dumps(report)
    out = tmp_path / "named.json"
    lean_closure.main(
        [
            str(checkout),
            "--commit",
            commit,
            "--root",
            "lean",
            "--source-url",
            "https://github.com/o/public",
            "Pkg.Spec",
            "--json",
            str(out),
        ]
    )
    named = out.read_text(encoding="utf-8")
    assert json.loads(named)["source_url"] == "https://github.com/o/public"
    assert SECRET not in named


@pytest.mark.parametrize(
    ("lakefile", "text", "directory"),
    [
        (
            "lakefile.toml",
            'name = "pkg"\nsrcDir = "src"\n\n[[lean_lib]]\nname = "Pkg"\nsrcDir = "lib"\n',
            "src/lib",
        ),
        (
            "lakefile.toml",
            'name = "pkg"\nsrcDir = "src"\n\n[[lean_lib]]\nname = "Pkg"\n',
            "src",
        ),
        (
            "lakefile.lean",
            (
                'import Lake\nopen Lake DSL\n\npackage «pkg» where\n  srcDir := "src"\n\n'
                "-- a comment between blocks\n@[default_target]\nlean_lib Pkg where\n"
                '  srcDir := "lib"\n'
            ),
            "src/lib",
        ),
    ],
)
def test_modules_are_looked_up_under_the_lakefile_s_src_dir(
    tmp_path: Path, lakefile: str, text: str, directory: str
) -> None:
    checkout = tmp_path / "upstream"
    files = {
        f"lean/{lakefile}": text,
        f"lean/{directory}/Pkg/Top.lean": "import Pkg.Spec\n\ntheorem t : True := trivial\n",
        f"lean/{directory}/Pkg/Spec.lean": "import Mathlib\n\ndef spec : Nat := 1\n",
        # A module at the project root is not the library's under a source directory.
        "lean/Pkg/Spec.lean": "theorem wrong : True := by sorry\n",
    }
    for name, body in files.items():
        path = checkout / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    _git(checkout, "init", "--quiet")
    _git(checkout, "add", "-A")
    _git(checkout, "commit", "--quiet", "-m", "pin")
    report = closure(Source(checkout, _git(checkout, "rev-parse", "HEAD")), "lean", ["Pkg.Top"])
    assert report["libraries"] == ["Pkg"]
    assert report["missing"] == []
    assert [m["path"] for m in report["modules"]] == [
        f"lean/{directory}/Pkg/Spec.lean",
        f"lean/{directory}/Pkg/Top.lean",
    ]
    assert report["escapes"][r"\bsorry\b"] == 0


RECEIPTS = sorted(
    (Path(__file__).resolve().parent.parent / "resources" / "web").glob("*/receipts/*.json")
)


def test_committed_closure_receipts_agree_with_the_tool_on_the_retained_bytes() -> None:
    # Every module a committed closure receipt lists is retained somewhere under
    # resources/web, byte for byte; re-counting it with today's tokens must give the
    # receipt's counts, and zero for any token added since the receipt was written.
    retained: dict[str, bytes] = {}
    for path in RECEIPTS[0].parents[2].rglob("*.lean"):
        data = path.read_bytes()
        retained.setdefault(git_blob(data), data)
    receipts = [
        report
        for report in (json.loads(path.read_text(encoding="utf-8")) for path in RECEIPTS)
        if isinstance(report, dict) and report.get("kind") == lean_closure.KIND
    ]
    assert len(receipts) >= 6
    for report in receipts:
        for module in report["modules"]:
            counts = escape_counts(retained[module["blob"]].decode("utf-8"))
            recorded = module["escapes"]
            assert {token: counts[token] for token in recorded} == recorded, module["path"]
            assert not any(counts[token] for token in counts if token not in recorded)
