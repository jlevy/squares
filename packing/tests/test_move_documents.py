"""A lifecycle move repoints every reference shape, and frozen records keep theirs."""

import subprocess
from pathlib import Path

import pytest

from devtools.move_documents import DEFAULT_EXCLUDES, main, plan, rewrite

ACTIVE = "docs/project/specs/active"
DONE = "docs/project/specs/done"
BASELINE = "docs/project/reviews/review-2026-10-10-bead-reconciliation-baseline.json"


def repository(tmp_path: Path, files: dict[str, str]) -> Path:
    for path, text in files.items():
        (tmp_path / path).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / path).write_text(text, encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    return tmp_path


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    return repository(
        tmp_path,
        {
            f"{ACTIVE}/a.md": "[b](b.md), [c](./c.md), [up](../../README.md), [w](https://x.org/a.md)\n",
            f"{ACTIVE}/b.md": "See [a](a.md#scope) and [a again][ref].\n\n[ref]: ./a.md\n",
            f"{ACTIVE}/c.md": "Mentions a.md in prose, which is not a link.\n",
            f"{DONE}/d.md": "[a](../active/a.md)\n",
            "README.md": f"[a]({ACTIVE}/a.md)\n",
            "docs/project/document-map.yaml": f"- {{path: {ACTIVE}/a.md, role: plan}}\n",
            "packing/tool.py": (
                f'PLAN = "{ACTIVE}/a.md"\nOLD = "explorations/packing/{ACTIVE}/a.md"\n'
            ),
            BASELINE: f'["{ACTIVE}/a.md"]\n',
        },
    )


def test_every_reference_shape_follows_the_move(tree: Path) -> None:
    moves = {f"{ACTIVE}/a.md": f"{DONE}/a.md"}
    assert main([f"{ACTIVE}/a.md={DONE}/a.md", "--repo", str(tree), "--apply"]) == 0
    moved = (tree / DONE / "a.md").read_text(encoding="utf-8")
    assert moved.startswith("[b](../active/b.md), [c](../active/c.md), [up](../../README.md)")
    assert "https://x.org/a.md" in moved
    assert (tree / ACTIVE / "b.md").read_text(encoding="utf-8") == (
        "See [a](../done/a.md#scope) and [a again][ref].\n\n[ref]: ../done/a.md\n"
    )
    assert (tree / DONE / "d.md").read_text(encoding="utf-8") == "[a](a.md)\n"
    assert (tree / "README.md").read_text(encoding="utf-8") == f"[a]({DONE}/a.md)\n"
    assert f"{DONE}/a.md" in (tree / "docs/project/document-map.yaml").read_text(
        encoding="utf-8"
    )
    code = (tree / "packing/tool.py").read_text(encoding="utf-8")
    assert f'PLAN = "{DONE}/a.md"' in code
    assert f'OLD = "explorations/packing/{ACTIVE}/a.md"' in code
    assert (tree / BASELINE).read_text(encoding="utf-8") == f'["{ACTIVE}/a.md"]\n'
    assert (tree / ACTIVE / "c.md").read_text(encoding="utf-8").startswith("Mentions a.md")
    assert not (tree / ACTIVE / "a.md").exists()
    assert plan(moves, tree, DEFAULT_EXCLUDES).problems == [
        f"source is not a tracked file: {ACTIVE}/a.md",
        f"target already exists: {DONE}/a.md",
    ]


def test_dry_run_writes_nothing(tree: Path, capsys: pytest.CaptureFixture[str]) -> None:
    before = (tree / "README.md").read_text(encoding="utf-8")
    assert main([f"{ACTIVE}/a.md={DONE}/a.md", "--repo", str(tree)]) == 0
    assert "dry run: 1 move(s)" in capsys.readouterr().out
    assert (tree / "README.md").read_text(encoding="utf-8") == before
    assert (tree / ACTIVE / "a.md").exists()


def test_refused_move_changes_nothing(tree: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([f"{ACTIVE}/a.md={DONE}/d.md", "--repo", str(tree), "--apply"]) == 1
    assert "target already exists" in capsys.readouterr().err
    assert (tree / ACTIVE / "a.md").exists()


def test_two_moved_siblings_keep_linking_each_other() -> None:
    moves = {f"{ACTIVE}/a.md": f"{DONE}/a.md", f"{ACTIVE}/b.md": f"{DONE}/b.md"}
    text, count = rewrite("[b](b.md) and [b](./b.md)\n", f"{ACTIVE}/a.md", moves)
    assert (text, count) == ("[b](b.md) and [b](./b.md)\n", 0)
