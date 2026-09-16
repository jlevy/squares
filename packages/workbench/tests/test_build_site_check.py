"""`build_site --check` builds the page twice, at once, and publishes only one of the two.

No real build runs here. `build` is replaced by a stand-in that writes `index.html` where it
is told to and records what it was given, so these tests take milliseconds and say only what
`main` does with the two builds. Whether the real build reproduces itself is what the Pages
workflow's `--check` step decides, in about a build's wall time.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import NamedTuple

import pytest

from workbench_tools import build_site

REVISION = "0" * 40


class Call(NamedTuple):
    out: Path
    revision: str | None
    dirty: bool | None


class FakeBuild:
    """A stand-in for `build_site.build`: the published page for `--out`, the twin's elsewhere.

    Both calls meet at a barrier before either returns. A `--check` that ran its builds one
    after the other would leave the first waiting for a second that has not started, and the
    barrier's timeout would fail the test rather than let it pass on the old wall time.
    """

    def __init__(self, published_dir: Path, *, published: str, twin: str) -> None:
        self.published_dir = published_dir
        self.published = published
        self.twin = twin
        self.calls: list[Call] = []
        self.barrier = threading.Barrier(2, timeout=10)

    def __call__(
        self, out: Path, *, revision: str | None = None, dirty: bool | None = None
    ) -> str:
        self.calls.append(Call(out, revision, dirty))
        self.barrier.wait()
        page = self.published if out == self.published_dir else self.twin
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(page, encoding="utf-8")
        return page


def run_check(monkeypatch: pytest.MonkeyPatch, fake: FakeBuild) -> int:
    monkeypatch.setattr(build_site, "build", fake)
    monkeypatch.setattr(build_site, "source_dirty", lambda: False)
    argv = ["--check", "--out", str(fake.published_dir), "--revision", REVISION]
    return build_site.main(argv)


def test_check_runs_two_builds_at_once_into_distinct_directories(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out = tmp_path / "site"
    fake = FakeBuild(out, published="<html></html>", twin="<html></html>")

    assert run_check(monkeypatch, fake) == 0

    directories = [call.out for call in fake.calls]
    assert len(directories) == 2
    assert len(set(directories)) == 2
    assert out in directories
    # One identity, looked up once, so a stamp cannot be what differs between the twins.
    assert {(call.revision, call.dirty) for call in fake.calls} == {(REVISION, False)}
    assert "deterministic, self-contained" in capsys.readouterr().out


def test_check_fails_when_the_two_pages_differ(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    fake = FakeBuild(tmp_path / "site", published="<html></html>", twin="<html> </html>")

    with pytest.raises(ValueError, match="did not reproduce itself"):
        run_check(monkeypatch, fake)


def test_check_publishes_the_page_only_under_out(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    out = tmp_path / "site"
    fake = FakeBuild(out, published="<html></html>", twin="<html></html>")

    run_check(monkeypatch, fake)

    (twin,) = (call.out for call in fake.calls if call.out != out)
    assert not twin.is_relative_to(out)
    assert not twin.exists(), "the twin's directory outlived the check"
    assert sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*")) == [
        Path("site"),
        Path("site/index.html"),
    ]
    assert (out / "index.html").read_text(encoding="utf-8") == "<html></html>"
