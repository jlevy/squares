"""The PDF cap holds indexed bytes and complete revisions without reading PDF data."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from devtools import check_tracked_pdfs as guard


def _git(repo: Path, *arguments: str, data: bytes | None = None) -> bytes:
    return subprocess.run(
        ("git", "-C", str(repo), *arguments), check=True, capture_output=True, input=data
    ).stdout


def _repository(tmp_path: Path) -> Path:
    repo = tmp_path / "repository"
    repo.mkdir()
    _ = _git(repo, "init", "-q")
    return repo


def _pdf(repo: Path, name: str, size: int) -> Path:
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    _ = path.write_bytes(b"%PDF" + b"x" * (size - 4))
    return path


def test_a_staged_nested_pdf_is_refused_after_its_working_copy_shrinks(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _repository(tmp_path)
    name = "papers/deep/source with spaces.PdF"
    path = _pdf(repo, name, guard.MAX_PDF_BYTES + 1)
    _ = _git(repo, "add", "--", name)
    _ = path.write_bytes(b"%PDF small working copy")
    assert guard.main(["--repo", str(repo)]) == 1
    said = capsys.readouterr()
    assert name in said.err
    assert str(guard.MAX_PDF_BYTES + 1) in said.err


def test_the_exact_boundary_and_unusual_nested_name_pass_without_counting_scratch(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _repository(tmp_path)
    name = "papers/nested/tab\there\nand spaces.PDF"
    _ = _pdf(repo, name, guard.MAX_PDF_BYTES)
    _ = _pdf(repo, "untracked.pdf", guard.MAX_PDF_BYTES + 1)
    _ = _pdf(repo, "ignored/source.pdf", guard.MAX_PDF_BYTES + 1)
    _ = (repo / ".gitignore").write_text("ignored/\n", encoding="utf-8")
    _ = _git(repo, "add", ".gitignore", "--", name)
    # A caller below the root still gets every indexed PDF, with tabs/newlines intact.
    nested = repo / "papers" / "nested"
    assert guard.inventory(nested) == (guard.Pdf(name, guard.MAX_PDF_BYTES),)
    assert guard.main(["--repo", str(nested)]) == 0
    said = capsys.readouterr()
    assert said.err == ""
    assert "1 tracked PDFs" in said.out


def test_a_staged_removal_passes_while_the_committed_revision_still_fails(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _repository(tmp_path)
    name = "papers/nested/archived source.pdf"
    _ = _pdf(repo, name, guard.MAX_PDF_BYTES + 1)
    _ = _git(repo, "add", "--", name)
    _ = _git(
        repo,
        "-c",
        "user.name=PDF guard fixture",
        "-c",
        "user.email=pdf-guard@example.invalid",
        "-c",
        "core.hooksPath=/dev/null",
        "commit",
        "-qm",
        "fixture",
    )
    _ = _git(repo, "rm", "--cached", "--", name)
    assert (repo / name).is_file()
    assert guard.main(["--repo", str(repo)]) == 0
    _ = capsys.readouterr()
    assert guard.main(["--repo", str(repo), "--revision", "HEAD"]) == 1
    said = capsys.readouterr()
    assert name in said.err
    assert "revision HEAD: 1 tracked PDFs" in said.out
    # A caller below the root must still audit the complete committed tree.
    nested = repo / "papers" / "nested"
    assert guard.main(["--repo", str(nested), "--revision", "HEAD"]) == 1
    said = capsys.readouterr()
    assert name in said.err
    assert "revision HEAD: 1 tracked PDFs" in said.out


def test_an_unresolved_pdf_index_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _repository(tmp_path)
    object_id = _git(repo, "hash-object", "-w", "--stdin", data=b"%PDF small").decode().strip()
    rows = "".join(f"100644 {object_id} {stage}\tunresolved.PDF\n" for stage in (1, 2, 3))
    _ = _git(repo, "update-index", "--index-info", data=rows.encode())
    assert guard.main(["--repo", str(repo)]) == 1
    assert "unresolved PDF merge" in capsys.readouterr().err


def test_an_unavailable_revision_does_not_report_an_empty_pass(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _repository(tmp_path)
    assert guard.main(["--repo", str(repo), "--revision", "missing-revision"]) == 1
    said = capsys.readouterr()
    assert "cannot inspect tracked PDFs" in said.err
    assert "0 tracked PDFs" not in said.out
