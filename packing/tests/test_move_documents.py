"""A lifecycle move repoints every reference shape, and frozen records keep theirs."""

import subprocess
from pathlib import Path

import pytest

from devtools import move_documents
from devtools.move_documents import DEFAULT_EXCLUDES, main, parse_moves, plan, rewrite

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


def test_a_file_whose_blob_a_tool_pins_keeps_its_bytes(tree: Path) -> None:
    record = tree / "docs/project/reviews/bound.md"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text(f"The review began while `{ACTIVE}/a.md` changed.\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tree), "add", "docs/project/reviews/bound.md"], check=True)
    blob = subprocess.run(
        ["git", "-C", str(tree), "hash-object", str(record)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    tool = tree / "packing/devtools/replay.py"
    tool.parent.mkdir(parents=True, exist_ok=True)
    tool.write_text(f'SOURCE = ("docs/project/reviews/bound.md", "{blob}")\n', encoding="utf-8")
    subprocess.run(["git", "-C", str(tree), "add", "packing/devtools/replay.py"], check=True)
    result = plan({f"{ACTIVE}/a.md": f"{DONE}/a.md"}, tree, DEFAULT_EXCLUDES)
    assert result.kept == ["docs/project/reviews/bound.md"]
    assert "docs/project/reviews/bound.md" not in result.rewrites
    assert "README.md" in result.rewrites


def test_a_directory_link_keeps_its_trailing_slash() -> None:
    moves = {"docs/project/x.md": "docs/project/guides/x.md"}
    text, _ = rewrite("[tool](../../packing/tool/)\n", "docs/project/x.md", moves)
    assert text == "[tool](../../../packing/tool/)\n"


def status(tree: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(tree), "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def snapshot(tree: Path) -> dict[str, bytes]:
    return {
        path.relative_to(tree).as_posix(): path.read_bytes()
        for path in sorted(tree.rglob("*"))
        if path.is_file() and ".git" not in path.relative_to(tree).parts
    }


def test_every_tracked_text_file_is_read_and_binary_mentions_are_reported(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    review = "docs/project/reviews/review-2026-09-03-quoted.md"
    tree = repository(
        tmp_path,
        {
            review: "Quoted source.\n",
            ".flowmarkignore": f"# keep the quotations raw\n{review}\n",
            "Makefile": f"lint:\n\tflowmark {review}\n",
            "packing/tool.rs": f'const REVIEW: &str = "{review}";\n',
        },
    )
    (tree / "evidence.bin").write_bytes(b"\x00\x01" + review.encode() + b"\x00")
    subprocess.run(["git", "-C", str(tree), "add", "evidence.bin"], check=True)
    moved = "docs/project/reviews/archive/review-2026-09-03-quoted.md"
    assert main([f"{review}={moved}", "--repo", str(tree)]) == 0
    out = capsys.readouterr().out
    assert "skipped, not text: evidence.bin" in out
    result = plan({review: moved}, tree, DEFAULT_EXCLUDES)
    assert sorted(result.rewrites) == [".flowmarkignore", "Makefile", "packing/tool.rs"]
    assert result.rewrites[".flowmarkignore"].endswith(f"{moved}\n")
    assert result.skipped == ["evidence.bin"]


def test_math_markup_stays_sorted_after_a_move(tmp_path: Path) -> None:
    register = "packing/devtools/math-markup.yaml"
    tree = repository(
        tmp_path,
        {
            f"{ACTIVE}/a.md": "A plan.\n",
            f"{ACTIVE}/b.md": "B plan.\n",
            register: (
                "# header\n\nmigrated:\n"
                f"- README.md\n- {ACTIVE}/a.md\n- {ACTIVE}/b.md\n- {DONE}/c.md\n"
                f"keep:\n- path: {ACTIVE}/a.md\n  span: x\n  reason: kept\n"
                f"exempt:\n- path: {ACTIVE}/b.md\n  reason: pinned\n- path: {DONE}/c.md\n"
                "  reason: quoted\n"
            ),
        },
    )
    assert (
        main([f"{ACTIVE}/b.md=docs/project/specs/paused/b.md", "--repo", str(tree), "--apply"])
        == 0
    )
    text = (tree / register).read_text(encoding="utf-8")
    assert text.split("keep:")[0].splitlines()[3:] == [
        "- README.md",
        f"- {ACTIVE}/a.md",
        f"- {DONE}/c.md",
        "- docs/project/specs/paused/b.md",
    ]
    assert text.split("exempt:\n")[1] == (
        f"- path: {DONE}/c.md\n  reason: quoted\n- path: docs/project/specs/paused/b.md\n"
        "  reason: pinned\n"
    )


def test_fenced_code_and_code_spans_are_not_relinked() -> None:
    moves = {f"{ACTIVE}/a.md": f"{DONE}/a.md"}
    text = (
        "Run `[x](notes.md)` first.\n\n"
        "```text\nsee [x](notes.md) and docs/project/specs/active/a.md\n```\n\n"
        "  ~~~\n  [y](notes.md)\n  ~~~\n\n"
        "[z](notes.md)\n"
    )
    rewritten, count = rewrite(text, f"{ACTIVE}/a.md", moves)
    assert rewritten == text.replace("[z](notes.md)", "[z](../active/notes.md)")
    assert count == 1


def test_a_path_left_in_fenced_code_is_reported(
    tree: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tree / "docs/runbook.md").write_text(
        f"```bash\nflowmark {ACTIVE}/a.md\n```\n", encoding="utf-8"
    )
    subprocess.run(["git", "-C", str(tree), "add", "docs/runbook.md"], check=True)
    assert main([f"{ACTIVE}/a.md={DONE}/a.md", "--repo", str(tree)]) == 0
    assert "left in fenced code, decide by hand: docs/runbook.md (1)" in capsys.readouterr().out
    assert (tree / "docs/runbook.md").read_text(encoding="utf-8").count(f"{ACTIVE}/a.md") == 1


def test_footnotes_in_a_moved_file_keep_their_text() -> None:
    moves = {f"{ACTIVE}/a.md": f"{DONE}/a.md"}
    text = "Claim.[^1]\n\n[^1]: Shown in the n = 11 record.\n[ref]: b.md\n"
    rewritten, _ = rewrite(text, f"{ACTIVE}/a.md", moves)
    assert rewritten == (
        "Claim.[^1]\n\n[^1]: Shown in the n = 11 record.\n[ref]: ../active/b.md\n"
    )


def test_link_titles_in_single_quotes_or_parentheses_are_relinked() -> None:
    moves = {f"{ACTIVE}/a.md": f"{DONE}/a.md"}
    text = "[b](b.md 'Title') and [c](c.md (Title)) and [d](d.md \"Title\")\n"
    rewritten, count = rewrite(text, f"{ACTIVE}/a.md", moves)
    assert rewritten == (
        "[b](../active/b.md 'Title') and [c](../active/c.md (Title)) and "
        '[d](../active/d.md "Title")\n'
    )
    assert count == 3


def test_crlf_line_endings_survive_a_rewrite(tmp_path: Path) -> None:
    tree = repository(tmp_path, {f"{ACTIVE}/a.md": "x\n"})
    (tree / "notes.yaml").write_bytes(f"a: 1\r\nplan: {ACTIVE}/a.md\r\nb: 2\r\n".encode())
    subprocess.run(["git", "-C", str(tree), "add", "notes.yaml"], check=True)
    assert main([f"{ACTIVE}/a.md={DONE}/a.md", "--repo", str(tree), "--apply"]) == 0
    assert (
        tree / "notes.yaml"
    ).read_bytes() == f"a: 1\r\nplan: {DONE}/a.md\r\nb: 2\r\n".encode()


def test_every_reconciliation_record_is_frozen(tmp_path: Path) -> None:
    receipts = [
        "docs/project/reviews/review-2026-10-13-owner-decisions-applied.json",
        "docs/project/reviews/review-2026-10-13-owner-decisions-dup.json",
        "docs/project/reviews/review-2026-10-12-bead-reconciliation-lane-1.json",
    ]
    tree = repository(
        tmp_path,
        {f"{ACTIVE}/a.md": "x\n", **dict.fromkeys(receipts, f'["{ACTIVE}/a.md"]\n')},
    )
    assert plan({f"{ACTIVE}/a.md": f"{DONE}/a.md"}, tree, DEFAULT_EXCLUDES).rewrites == {}


def test_a_path_that_ends_a_sentence_is_rewritten() -> None:
    moves = {f"{ACTIVE}/a.md": f"{DONE}/a.md"}
    text = f"The plan is {ACTIVE}/a.md. See also `{ACTIVE}/a.md`, and {ACTIVE}/a.md.bak.\n"
    rewritten, count = rewrite(text, "notes.md", moves)
    assert rewritten == (
        f"The plan is {DONE}/a.md. See also `{DONE}/a.md`, and {ACTIVE}/a.md.bak.\n"
    )
    assert count == 2


@pytest.mark.parametrize(
    ("moves", "problem"),
    [
        ([f"{ACTIVE}/a.md={DONE}/x.md", f"{ACTIVE}/b.md={DONE}/x.md"], "two moves share"),
        ([f"{ACTIVE}/a.md={ACTIVE}/b.md", f"{ACTIVE}/b.md={DONE}/b.md"], "target is another"),
        ([f"{ACTIVE}/a.md={DONE}/d.md/a.md"], "parent is a file"),
        ([f"{ACTIVE}/a.md=../outside/a.md"], "outside the repository"),
        ([f"{ACTIVE}/a.md=/tmp/outside/a.md"], "outside the repository"),
        ([f"../{ACTIVE}/a.md={DONE}/a.md"], "outside the repository"),
    ],
)
def test_an_invalid_move_list_is_refused_with_nothing_changed(
    tree: Path, moves: list[str], problem: str, capsys: pytest.CaptureFixture[str]
) -> None:
    before, index_before = snapshot(tree), status(tree)
    assert main([*moves, "--repo", str(tree), "--apply"]) == 1
    assert problem in capsys.readouterr().err
    assert (snapshot(tree), status(tree)) == (before, index_before)
    assert not (tree.parent / "outside").exists()


def test_a_failed_move_restores_every_file(tree: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    before = snapshot(tree)
    index_before = status(tree)
    real = move_documents.git_mv
    calls: list[tuple[str, str]] = []

    def failing(repo: Path, old: str, new: str) -> None:
        calls.append((old, new))
        if len(calls) == 2:
            raise subprocess.CalledProcessError(128, ["git", "mv", old, new])
        real(repo, old, new)

    monkeypatch.setattr(move_documents, "git_mv", failing)
    with pytest.raises(subprocess.CalledProcessError):
        main(
            [
                f"{ACTIVE}/a.md={DONE}/a.md",
                f"{ACTIVE}/b.md={DONE}/b.md",
                "--repo",
                str(tree),
                "--apply",
            ]
        )
    assert snapshot(tree) == before
    assert status(tree) == index_before


def test_a_tracked_symlink_is_not_written_through(tmp_path: Path) -> None:
    outside = tmp_path / "outside.md"
    outside.write_text(f"names {ACTIVE}/a.md\n", encoding="utf-8")
    tree = tmp_path / "tree"
    repository(tree, {f"{ACTIVE}/a.md": "x\n"})
    (tree / "linked.md").symlink_to(outside)
    subprocess.run(["git", "-C", str(tree), "add", "linked.md"], check=True)
    assert main([f"{ACTIVE}/a.md={DONE}/a.md", "--repo", str(tree), "--apply"]) == 0
    assert outside.read_text(encoding="utf-8") == f"names {ACTIVE}/a.md\n"


def test_a_repeated_source_is_refused() -> None:
    with pytest.raises(ValueError, match="moved twice"):
        parse_moves([f"{ACTIVE}/a.md={DONE}/a.md", f"{ACTIVE}/a.md={DONE}/b.md"])


def test_a_link_whose_label_is_a_code_span_is_relinked() -> None:
    moves = {f"{ACTIVE}/a.md": f"{DONE}/a.md"}
    text = "See [`b.md`](b.md) and [`the plan`][plan].\n\n[plan]: ./b.md\n"
    rewritten, count = rewrite(text, f"{ACTIVE}/a.md", moves)
    assert rewritten == (
        "See [`b.md`](../active/b.md) and [`the plan`][plan].\n\n[plan]: ../active/b.md\n"
    )
    assert count == 2


def test_reports_name_a_moved_file_by_its_new_path(
    tree: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tree / ACTIVE / "a.md").write_text(
        f"[b](b.md)\n\n```bash\ntbd list --spec {ACTIVE}/a.md\n```\n", encoding="utf-8"
    )
    subprocess.run(["git", "-C", str(tree), "add", f"{ACTIVE}/a.md"], check=True)
    assert main([f"{ACTIVE}/a.md={DONE}/a.md", "--repo", str(tree)]) == 0
    out = capsys.readouterr().out
    assert f"  1 reference(s) in {ACTIVE}/a.md -> {DONE}/a.md" in out
    assert f"left in fenced code, decide by hand: {ACTIVE}/a.md -> {DONE}/a.md (1)" in out


def test_an_escaped_backtick_opens_no_code_span() -> None:
    moves = {f"{ACTIVE}/a.md": f"{DONE}/a.md"}
    text = "Type \\` to quote, then see [b](b.md) and `x`.\n"
    rewritten, count = rewrite(text, f"{ACTIVE}/a.md", moves)
    assert rewritten == "Type \\` to quote, then see [b](../active/b.md) and `x`.\n"
    assert count == 1
