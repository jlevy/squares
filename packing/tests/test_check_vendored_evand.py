"""The vendored regularizer is held to its manifest, the manifest to upstream, and every
way out of either is refused.

`devtools.check_vendored_evand` passes the real copy, then each rule is rehearsed on a
small copy built here: an unrecorded edit, a dropped file, a stray file, a link, a mode,
a module that would shadow a dependency, each kind of local change done right and done
wrong, the licence, the re-pin writer, and `--upstream` against a local upstream
repository, which refuses the edits a matching manifest edit hides from the offline check.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import time
from pathlib import Path

import pytest

from devtools import check_vendored_evand as vendored
from sqpack.yamlio import safe_load

COMMIT = "0123456789abcdef0123456789abcdef01234567"
SCRATCH_GIT = (
    "-c",
    "user.name=vendored test",
    "-c",
    "user.email=vendored-test@example.invalid",
    "-c",
    "commit.gpgsign=false",
    "-c",
    "core.hooksPath=/dev/null",
)
UPSTREAM = {
    "LICENSE": b"MIT License\n\nCopyright (c) 2026 Example Author\n",
    "CREDITS.md": b"# credits\n",
    "search/tool.py": b"import sys\nprint(sys.argv)\n",
    "search/data.json": b'{"n": 1}\n',
}
METADATA = {
    "source_url": "https://example.invalid/upstream",
    "source_commit": COMMIT,
    "git_tree": "f" * 40,
    "committed": "2026-10-11T10:34:02-06:00",
    "subject": "a subject: with a colon",
    "copyright": "Copyright (c) 2026 Example Author",
}


@pytest.fixture(autouse=True)
def _no_inherited_git(monkeypatch: pytest.MonkeyPatch) -> None:
    """An inherited `GIT_INDEX_FILE` must not aim the scratch repositories elsewhere."""
    for name in list(os.environ):
        if name.startswith("GIT_"):
            monkeypatch.delenv(name)


def _git(directory: Path, *arguments: str) -> str:
    done = subprocess.run(
        ("git", "-C", str(directory), *SCRATCH_GIT, *arguments),
        capture_output=True,
        text=True,
        check=True,
    )
    return done.stdout.strip()


def _copy(root: Path, local_changes: str = "[]") -> Path:
    """A vendored copy of `UPSTREAM` under `root`, with its manifest and provenance file."""
    directory = root / "vendor" / "upstream"
    for path, data in UPSTREAM.items():
        (directory / path).parent.mkdir(parents=True, exist_ok=True)
        (directory / path).write_bytes(data)
    files = [
        vendored.Pinned(path, len(data), hashlib.sha256(data).hexdigest())
        for path, data in sorted(UPSTREAM.items())
    ]
    text = vendored.render_manifest(metadata=METADATA, files=files, retrieved="2026-10-11")
    (directory / vendored.MANIFEST_NAME).write_text(
        text.replace("local_changes: []", f"local_changes: {local_changes}"), encoding="utf-8"
    )
    (directory / "README.md").write_text("# Vendored\n\n### Local Changes\n\nNone.\n")
    return directory


def _describe(directory: Path, entry: str) -> None:
    """The provenance file, with `entry` as its Local Changes section."""
    (directory / "README.md").write_text(f"# Vendored\n\n### Local Changes\n\n{entry}\n")


def _problems(directory: Path) -> list[str]:
    manifest = vendored.load_manifest(directory / vendored.MANIFEST_NAME)
    return vendored.check(directory, manifest, vendored.present_files(directory))


def _change(path: str, kind: str) -> str:
    return (
        f"[{{path: {path}, kind: {kind}, date: '2026-10-12', bead: think-abcd, reason: why}}]"
    )


def test_the_real_vendored_copy_matches_its_manifest(
    capsys: pytest.CaptureFixture[str],
) -> None:
    started = time.perf_counter()
    assert vendored.main([]) == 0
    assert time.perf_counter() - started < 5  # the step is priced at under a second
    output = capsys.readouterr().out
    # The count and the commit are written here, not read from the manifest, so a file
    # or a pin added to the manifest alone fails this test even where it passes the check.
    assert "vendored copy check passed: 351 files match vendored.yaml" in output
    assert "square-packing@675a5ea" in output
    assert "not compared with upstream (--upstream does that)" in output


def test_the_real_manifest_pins_the_licence_and_the_commit() -> None:
    manifest = vendored.load_manifest(vendored.VENDORED / vendored.MANIFEST_NAME)
    assert manifest.source_commit == "675a5eaa8712542daac8b4515b0f69ad7044df44"
    assert manifest.license_file == "LICENSE"
    assert "README.md" not in manifest.files  # the project's own, never an upstream file
    assert "Copyright (c) 2026 Evan Daniel" in (vendored.VENDORED / "LICENSE").read_text()
    # A re-render of the parsed manifest is the file itself, so `--write` reproduces it;
    # the recorded local changes are edited by hand, and a re-pin starts without them.
    text = (vendored.VENDORED / vendored.MANIFEST_NAME).read_text()
    record = safe_load(text)
    rendered = vendored.render_manifest(
        metadata={key: str(record[key]) for key in METADATA},
        files=list(manifest.files.values()),
        retrieved=str(record["retrieved"]),
    )
    start = text.index("local_changes:")
    recorded = text[start : text.index("\n\n", start) + 1]
    assert rendered == text.replace(recorded, "local_changes: []\n")


def test_a_pristine_copy_passes(tmp_path: Path) -> None:
    assert _problems(_copy(tmp_path)) == []


def test_an_unrecorded_edit_is_refused_whether_or_not_the_size_moved(tmp_path: Path) -> None:
    directory = _copy(tmp_path)
    (directory / "search/tool.py").write_bytes(b"import sys\nprint(sys.path)\n")
    (directory / "search/data.json").write_bytes(b'{"n": 2, "m": 3}\n')
    problems = _problems(directory)
    assert any("search/tool.py: not the pinned bytes" in line for line in problems)
    assert any("search/data.json: 17 bytes, not the pinned 9" in line for line in problems)


def test_a_dropped_file_and_a_stray_file_are_refused(tmp_path: Path) -> None:
    directory = _copy(tmp_path)
    (directory / "search/data.json").unlink()
    (directory / "runs").mkdir()
    (directory / "runs/out.json").write_text("{}")
    problems = _problems(directory)
    assert "search/data.json: pinned, but missing from the vendored copy" in problems
    assert any(line.startswith("runs/out.json: not in the manifest") for line in problems)


def test_the_walk_skips_interpreter_caches(tmp_path: Path) -> None:
    directory = _copy(tmp_path)
    (directory / "search/__pycache__").mkdir()
    (directory / "search/__pycache__/tool.cpython-314.pyc").write_bytes(b"\0")
    assert _problems(directory) == []


def test_git_answers_what_the_directory_holds(tmp_path: Path) -> None:
    _git(tmp_path, "init", "-q")
    (tmp_path / ".gitignore").write_text("*.log\n")
    directory = _copy(tmp_path)
    _git(tmp_path, "add", ".")
    (directory / "search/run.log").write_text("ignored, so never content\n")
    assert _problems(directory) == []
    (directory / "search/new.py").write_text(
        "untracked and unignored, so it would be committed\n"
    )
    assert _problems(directory) == [
        (
            "search/new.py: not in the manifest; vendored code changes only by a recorded "
            "local change, and run outputs belong in a scratch directory, not here"
        )
    ]


def test_a_recorded_modification_passes_once_it_is_marked(tmp_path: Path) -> None:
    directory = _copy(tmp_path, _change("search/tool.py", "modified"))
    assert _problems(directory) == [
        "search/tool.py: recorded as modified, but it is still the pinned bytes",
        (
            "search/tool.py: recorded as a local change, but README.md's Local Changes "
            "does not name it"
        ),
    ]
    (directory / "search/tool.py").write_bytes(b"import sys\nprint(sys.path)\n")
    (directory / "README.md").write_text(
        "### Local Changes\n\n`search/tool.py` prints sys.path.\n"
    )
    assert _problems(directory) == [
        (
            "search/tool.py: modified, but its first 20 lines carry no comment naming "
            "vendor/evand-regularize/README.md"
        )
    ]
    (directory / "search/tool.py").write_bytes(
        b"# Locally modified (think-abcd); see vendor/evand-regularize/README.md.\n"
        b"import sys\nprint(sys.path)\n"
    )
    assert _problems(directory) == []


def test_a_modified_data_file_needs_no_header_comment(tmp_path: Path) -> None:
    directory = _copy(tmp_path, _change("search/data.json", "modified"))
    (directory / "search/data.json").write_bytes(b'{"n": 2}\n')
    _describe(directory, "`search/data.json` holds 2.")
    assert _problems(directory) == []


def test_a_removal_and_an_addition_are_held_to_what_they_say(tmp_path: Path) -> None:
    changes = (
        "[{path: search/data.json, kind: removed, date: '2026-10-12', bead: think-abcd, "
        "reason: unused}, {path: search/extra.py, kind: added, date: '2026-10-12', "
        "bead: think-abcd, reason: a driver}]"
    )
    directory = _copy(tmp_path, changes)
    _describe(directory, "`search/data.json` removed; `search/extra.py` added.")
    assert _problems(directory) == [
        "search/data.json: recorded as removed, but it is still here",
        "search/extra.py: recorded as added, but it is not here",
    ]
    (directory / "search/data.json").unlink()
    (directory / "search/extra.py").write_text(
        "# Added here (think-abcd); see vendor/evand-regularize/README.md.\n"
    )
    assert _problems(directory) == []


STALL = "packing/devtools/patches/tool-path.patch"
PATCH = """A replica patch: prose before the first hunk is the patch's own account.

--- a/search/tool.py
+++ b/search/tool.py
@@ -1,2 +1,3 @@
+# Patched in a replica (think-abcd); see vendor/evand-regularize/README.md.
 import sys
-print(sys.argv)
+print(sys.path)
"""


def _replica(tmp_path: Path, patch: str | None = PATCH) -> Path:
    change = (
        "[{path: search/tool.py, kind: replica, patch: "
        f"{STALL}, date: '2026-10-12', bead: think-abcd, reason: why}}]"
    )
    directory = _copy(tmp_path, change)
    if patch is not None:
        (tmp_path / STALL).parent.mkdir(parents=True)
        (tmp_path / STALL).write_text(patch)
    (directory / "README.md").write_text(
        "### Local Changes\n\n`search/tool.py`, `tool-path.patch`: prints sys.path.\n"
    )
    return directory


def test_a_replica_patch_leaves_the_file_pinned_and_must_still_apply(tmp_path: Path) -> None:
    directory = _replica(tmp_path)
    assert _problems(directory) == []
    manifest = vendored.load_manifest(directory / vendored.MANIFEST_NAME)
    assert manifest.changes["search/tool.py"].patch == STALL
    # Applying it here instead of to a replica is an unrecorded edit, and the patch then
    # no longer applies to the bytes in the copy.
    (directory / "search/tool.py").write_text(
        vendored.apply_patch(UPSTREAM["search/tool.py"].decode(), PATCH)
    )
    problems = _problems(directory)
    assert any("does not apply" in line for line in problems)
    assert any("not the pinned" in line for line in problems)


def test_a_replica_patch_must_be_there_and_named_in_the_readme(tmp_path: Path) -> None:
    directory = _replica(tmp_path, patch=None)
    assert _problems(directory) == [f"search/tool.py: its replica patch {STALL} is missing"]
    (tmp_path / STALL).parent.mkdir(parents=True)
    (tmp_path / STALL).write_text(PATCH)
    (directory / "README.md").write_text("### Local Changes\n\n`search/tool.py` patched.\n")
    assert _problems(directory) == [
        (
            "search/tool.py: its replica patch tool-path.patch is not named in README.md's "
            "Local Changes"
        )
    ]


def test_a_replica_change_names_its_patch(tmp_path: Path) -> None:
    manifest = _copy(tmp_path, _change("search/tool.py", "replica")) / vendored.MANIFEST_NAME
    with pytest.raises(vendored.ManifestError, match="`patch` must be a non-empty string"):
        vendored.load_manifest(manifest)


def test_a_patch_applies_by_its_exact_context_or_not_at_all() -> None:
    original = UPSTREAM["search/tool.py"].decode()
    assert vendored.apply_patch(original, PATCH) == (
        "# Patched in a replica (think-abcd); see vendor/evand-regularize/README.md.\n"
        "import sys\nprint(sys.path)\n"
    )
    with pytest.raises(vendored.PatchError, match="is not in the text"):
        vendored.apply_patch("import os\nprint(sys.argv)\n", PATCH)
    with pytest.raises(vendored.PatchError, match="occurs 2 times"):
        vendored.apply_patch(original + original, PATCH)
    with pytest.raises(vendored.PatchError, match="no hunk"):
        vendored.apply_patch(original, "prose only\n")
    with pytest.raises(vendored.PatchError, match="ends before"):
        vendored.apply_patch(original, PATCH.rsplit("\n", 3)[0] + "\n")


def test_a_hunk_that_could_land_in_two_places_or_mid_line_is_refused() -> None:
    """Review B of #511, B9: occurrences are whole lines, and overlapping ones count."""
    hunk = "--- a/f\n+++ b/f\n@@ -1,3 +1,3 @@\n x\n-y\n+Z\n x\n"
    with pytest.raises(vendored.PatchError, match="occurs 2 times"):
        vendored.apply_patch("x\ny\nx\ny\nx\n", hunk)
    assert vendored.apply_patch("w\nx\ny\nx\n", hunk) == "w\nx\nZ\nx\n"
    tail = "--- a/f\n+++ b/f\n@@ -1,1 +1,1 @@\n-y = 1\n+y = 2\n"
    with pytest.raises(vendored.PatchError, match="is not in the text"):
        vendored.apply_patch("xy = 1\n", tail)
    assert vendored.apply_patch("x = 0\ny = 1\n", tail) == "x = 0\ny = 2\n"


def test_the_real_replica_patch_applies_to_the_pinned_solver() -> None:
    manifest = vendored.load_manifest(vendored.VENDORED / vendored.MANIFEST_NAME)
    change = manifest.changes["search/exact/exactsolve.py"]
    assert change.kind == "replica"
    assert change.patch is not None
    pinned = (vendored.VENDORED / change.path).read_text(encoding="utf-8")
    patched = vendored.apply_patch(
        pinned, (vendored.project_root(vendored.VENDORED) / change.patch).read_text()
    )
    added = sorted(set(patched.splitlines()) - set(pinned.splitlines()))
    assert any("nr > prev / 10" in line for line in added)
    assert len(patched.splitlines()) == len(pinned.splitlines()) + 8


#: Each kind of local change, applied correctly: the path it records and the bytes it
#: leaves there (None for a removal).
APPLIED = {
    "modified": (
        "search/tool.py",
        (
            b"# Locally modified (think-abcd); see vendor/evand-regularize/README.md.\n"
            b"import sys\nprint(sys.path)\n"
        ),
    ),
    "added": (
        "search/extra.py",
        b"# Added here (think-abcd); see vendor/evand-regularize/README.md.\n",
    ),
    "removed": ("search/data.json", None),
}


@pytest.mark.parametrize("kind", sorted(APPLIED))
def test_only_the_local_changes_section_names_a_change(tmp_path: Path, kind: str) -> None:
    """A path the role table or a later section names is not thereby a described change."""
    path, data = APPLIED[kind]
    directory = _copy(tmp_path, _change(path, kind))
    if data is None:
        (directory / path).unlink()
    else:
        (directory / path).write_bytes(data)
    pristine = "None. Every file is byte-identical to the pin."
    readme = (
        f"# Vendored\n\n## What Each File Is For\n\n| `{path}` | its role |\n\n"
        f"### Local Changes\n\n{pristine}\n\n## Re-pinning\n\nRestore `{path}` first.\n"
    )
    (directory / "README.md").write_text(readme)
    assert _problems(directory) == [
        f"{path}: recorded as a local change, but README.md's Local Changes does not name it"
    ]
    (directory / "README.md").write_text(readme.replace(pristine, f"`{path}` is {kind}."))
    assert _problems(directory) == []


def test_the_local_changes_section_ends_at_the_next_heading_outside_code() -> None:
    readme = (
        "## Forking\n\nName `a.py` here.\n\n### Local Changes\n\n"
        "```sh\n# a comment, not a heading\n```\n\n`b.py` is patched.\n\n"
        "#### Detail\n\n`c.py`\n\n## Re-pinning\n"
    )
    section = vendored.local_changes_text(readme)
    assert "`b.py` is patched." in section
    assert "a.py" not in section
    assert "c.py" not in section
    assert vendored.local_changes_text("`b.py` is patched.\n") == ""


def test_the_licence_is_never_a_local_change(tmp_path: Path) -> None:
    directory = _copy(tmp_path, _change("LICENSE", "modified"))
    (directory / "LICENSE").write_text("All rights reserved.\n")
    _describe(directory, "`LICENSE` replaced.")
    assert (
        "LICENSE: the licence file is never a local change; the MIT grant requires its notice "
        "with every copy"
    ) in _problems(directory)


def test_the_project_files_must_be_there(tmp_path: Path) -> None:
    directory = _copy(tmp_path)
    (directory / "README.md").unlink()
    assert _problems(directory) == [
        "README.md: this project's file is missing from the vendored directory"
    ]


@pytest.mark.parametrize(
    ("edit", "complaint"),
    [
        (("source_commit: " + COMMIT, "source_commit: 0123abc"), "full 40-digit commit id"),
        (("format: vendored-source-v1", "format: other"), "`format` must be"),
        (("retrieved: '2026-10-11'", "retrieved: yesterday"), "`retrieved` must be"),
        (("license_file: LICENSE", "license_file: COPYING"), "not among the pinned files"),
        (("local_changes: []", "local_changes: none"), "`local_changes` must be a list"),
    ],
)
def test_a_malformed_manifest_is_refused(
    tmp_path: Path, edit: tuple[str, str], complaint: str
) -> None:
    directory = _copy(tmp_path)
    manifest = directory / vendored.MANIFEST_NAME
    manifest.write_text(manifest.read_text().replace(*edit), encoding="utf-8")
    with pytest.raises(vendored.ManifestError, match=complaint):
        vendored.load_manifest(manifest)


def test_a_change_without_a_bead_or_a_known_kind_is_refused(tmp_path: Path) -> None:
    manifest = _copy(tmp_path, _change("search/tool.py", "patched")) / vendored.MANIFEST_NAME
    with pytest.raises(vendored.ManifestError, match="`kind` is one of"):
        vendored.load_manifest(manifest)
    text = manifest.read_text().replace("kind: patched", "kind: modified")
    manifest.write_text(text.replace("bead: think-abcd", "bead: soon"), encoding="utf-8")
    with pytest.raises(vendored.ManifestError, match="`bead` must name the bead"):
        vendored.load_manifest(manifest)


def test_a_path_listed_twice_or_outside_the_copy_is_refused(tmp_path: Path) -> None:
    manifest = _copy(tmp_path) / vendored.MANIFEST_NAME
    text = manifest.read_text()
    line = next(row for row in text.splitlines() if "path: LICENSE" in row)
    manifest.write_text(text + line + "\n", encoding="utf-8")
    with pytest.raises(vendored.ManifestError, match="LICENSE is listed twice"):
        vendored.load_manifest(manifest)
    manifest.write_text(
        text.replace("path: search/tool.py", "path: ../tool.py"), encoding="utf-8"
    )
    with pytest.raises(vendored.ManifestError, match="not a plain relative POSIX path"):
        vendored.load_manifest(manifest)


@pytest.fixture
def upstream(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A local upstream repository standing in for `UPSTREAM_URL`, its own `origin`.

    Its one commit is on its `main` branch, so a re-pin or `--upstream` finds the commit
    on one of upstream's branches, as it must.
    """
    checkout = tmp_path / "upstream"
    checkout.mkdir()
    _git(checkout, "init", "-q", "--initial-branch=main")
    for path, data in UPSTREAM.items():
        (checkout / path).parent.mkdir(parents=True, exist_ok=True)
        (checkout / path).write_bytes(data)
    _git(checkout, "add", ".")
    _git(checkout, "commit", "-q", "-m", "a subject: with a colon")
    _git(checkout, "remote", "add", "origin", checkout.as_uri())
    monkeypatch.setattr(vendored, "UPSTREAM_URL", checkout.as_uri())
    return checkout


def _head(checkout: Path) -> str:
    return _git(checkout, "rev-parse", "HEAD")


def test_a_repin_binds_each_file_to_the_upstream_blob(tmp_path: Path, upstream: Path) -> None:
    checkout = upstream
    directory = _copy(tmp_path / "project")
    commit = _git(checkout, "rev-parse", "HEAD")
    text = vendored.repin(directory, checkout, commit=commit, retrieved="2026-10-12")
    (directory / vendored.MANIFEST_NAME).write_text(text, encoding="utf-8")
    manifest = vendored.load_manifest(directory / vendored.MANIFEST_NAME)
    assert manifest.source_commit == commit
    assert manifest.source_url == checkout.as_uri()
    assert sorted(manifest.files) == sorted(UPSTREAM)
    assert _problems(directory) == []
    # A working-tree edit in the checkout is not the commit, and does not move the pin.
    (checkout / "search/tool.py").write_text("edited after the commit\n")
    assert vendored.repin(directory, checkout, commit=commit, retrieved="2026-10-12") == text


def test_a_repin_refuses_bytes_the_commit_does_not_hold(tmp_path: Path, upstream: Path) -> None:
    checkout = upstream
    directory = _copy(tmp_path / "project")
    (directory / "search/tool.py").write_text("not upstream's\n")
    (directory / "search/local.py").write_text("upstream never had this\n")
    with pytest.raises(vendored.ManifestError) as refusal:
        vendored.repin(directory, checkout, commit=_head(checkout), retrieved="2026-10-12")
    assert "search/tool.py: not upstream's bytes at" in str(refusal.value)
    assert "search/local.py: upstream has no such file at" in str(refusal.value)


def test_a_repin_refuses_while_local_changes_are_recorded(
    tmp_path: Path, upstream: Path
) -> None:
    checkout = upstream
    directory = _copy(tmp_path / "project", _change("search/data.json", "modified"))
    with pytest.raises(vendored.ManifestError, match="restore the pristine copy"):
        vendored.repin(directory, checkout, commit=_head(checkout), retrieved="2026-10-12")


def test_the_command_reports_and_fails_on_a_finding(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    directory = _copy(tmp_path)
    (directory / "stray.txt").write_text("x")
    assert vendored.main(["--directory", str(directory)]) == 1
    assert "stray.txt: not in the manifest" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Links, modes and shadowing modules (offline)
# ---------------------------------------------------------------------------


def _pin(directory: Path, path: str, *, executable: bool = False) -> None:
    """Declare `path`, as it now is, in the manifest's `files` (a forged manifest line)."""
    data = (directory / path).read_bytes()
    manifest = directory / vendored.MANIFEST_NAME
    text = manifest.read_text()
    files = [
        pinned
        for pinned in vendored.load_manifest(manifest).files.values()
        if pinned.path != path
    ]
    files.append(vendored.Pinned(path, len(data), hashlib.sha256(data).hexdigest(), executable))
    record = safe_load(text)
    rendered = vendored.render_manifest(
        metadata={key: str(record[key]) for key in METADATA},
        files=sorted(files, key=lambda item: item.path),
        retrieved=str(record["retrieved"]),
    )
    manifest.write_text(rendered, encoding="utf-8")


@pytest.mark.parametrize("indexed", [False, True], ids=["walked", "git"])
def test_a_symbolic_link_is_refused_even_to_identical_bytes(
    tmp_path: Path, *, indexed: bool
) -> None:
    if indexed:
        _git(tmp_path, "init", "-q")
    directory = _copy(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "data.json").write_bytes(UPSTREAM["search/data.json"])
    (directory / "search/data.json").unlink()
    (directory / "search/data.json").symlink_to(outside / "data.json")
    assert _problems(directory) == [
        "search/data.json: a symbolic link; the vendored copy holds regular files only"
    ]
    (directory / "search/data.json").unlink()
    (directory / "search/data.json").write_bytes(UPSTREAM["search/data.json"])
    (directory / "search/linked").symlink_to(outside, target_is_directory=True)
    assert _problems(directory)[0] == (
        "search/linked: a symbolic link; the vendored copy holds regular files only"
    )


def test_a_linked_directory_holding_pinned_files_is_refused(tmp_path: Path) -> None:
    directory = _copy(tmp_path)
    moved = tmp_path / "elsewhere"
    (directory / "search").rename(moved)
    (directory / "search").symlink_to(moved, target_is_directory=True)
    assert _problems(directory) == [
        "search: a symbolic link; the vendored copy holds regular files only"
    ]


def test_the_executable_bit_is_held_to_the_manifest(tmp_path: Path) -> None:
    directory = _copy(tmp_path)
    tool = directory / "search/tool.py"
    tool.chmod(tool.stat().st_mode | stat.S_IXUSR)
    assert _problems(directory) == [
        "search/tool.py: mode 100755, not the pinned 100644; the copy keeps upstream's modes"
    ]
    _pin(directory, "search/tool.py", executable=True)
    assert _problems(directory) == []
    tool.chmod(tool.stat().st_mode & ~0o111)
    assert _problems(directory) == [
        "search/tool.py: mode 100644, not the pinned 100755; the copy keeps upstream's modes"
    ]


def test_the_executable_field_is_a_boolean(tmp_path: Path) -> None:
    directory = _copy(tmp_path)
    _pin(directory, "search/tool.py", executable=True)
    manifest = directory / vendored.MANIFEST_NAME
    manifest.write_text(manifest.read_text().replace("executable: true", "executable: 1"))
    with pytest.raises(vendored.ManifestError, match="`executable` is `true` or absent"):
        vendored.load_manifest(manifest)


@pytest.mark.parametrize(
    ("path", "module"),
    [
        ("search/numpy.py", "numpy"),
        ("search/yaml/__init__.py", "yaml"),
        ("search/json.py", "json"),
        ("search/sitecustomize.py", "sitecustomize"),
        ("search/scipy.cpython-314-x86_64-linux-gnu.so", "scipy"),
        ("search/gmpy2.py", "gmpy2"),
        ("search/sage/__init__.py", "sage"),
        (
            "search/_sysconfigdata__linux_x86_64-linux-gnu.py",
            "_sysconfigdata__linux_x86_64-linux-gnu",
        ),
    ],
)
def test_a_module_that_would_shadow_an_import_is_refused_even_when_pinned(
    tmp_path: Path, path: str, module: str
) -> None:
    """R3 of Review B: a forged `files:` line cannot admit a `numpy.py` beside the code."""
    directory = _copy(tmp_path)
    (directory / path).parent.mkdir(parents=True, exist_ok=True)
    (directory / path).write_bytes(b"import os\n")
    _pin(directory, path)
    assert _problems(directory) == [
        (
            f"{path}: would be imported in place of the `{module}` module the vendored "
            "scripts or their dependencies load, since the scripts put its directory on "
            "sys.path"
        )
    ]


def test_the_declared_dependencies_are_what_the_vendored_code_imports() -> None:
    """`DEPENDENCIES` is read off the vendored code, so a re-pin that adds one fails here."""
    sources = sorted(vendored.VENDORED.rglob("*.py"))
    own = {source.stem for source in sources}
    imported: set[str] = set()
    for source in sources:
        for node in ast.walk(ast.parse(source.read_bytes(), str(source))):
            if isinstance(node, ast.Import):
                imported |= {alias.name.partition(".")[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imported.add(node.module.partition(".")[0])
    assert imported - own - set(sys.stdlib_module_names) == vendored.DEPENDENCIES
    assert not {name for name in own if name in vendored.RESERVED_MODULES}


#: Run in a fresh interpreter: import each named module with a finder first on
#: `sys.meta_path` that records every top-level lookup, found or not, and print the names
#: outside the standard library. With "hide", every such name that is not a declared
#: dependency is refused, as if not installed, so each fallback import is tried too.
#: CPython's `_sysconfigdata_*` modules are never hidden: `sysconfig` cannot load without.
_LOOKUPS = """
import importlib, json, sys
modules, dependencies, hide = json.loads(sys.argv[1]), set(json.loads(sys.argv[2])), sys.argv[3]
seen = set()

def outside(name):
    top = name.partition(".")[0]
    return top not in sys.stdlib_module_names and not top.startswith("_sysconfigdata_")

class Recorder:
    @staticmethod
    def find_spec(name, path=None, target=None):
        if path is None and outside(name):
            seen.add(name)
            if hide == "hide" and name not in dependencies:
                raise ModuleNotFoundError(f"hidden: {name}", name=name)
        return None

sys.meta_path.insert(0, Recorder)
for module in modules:
    try:
        importlib.import_module(module)
    except ImportError:
        pass
print(json.dumps(sorted(seen)))
"""


def test_the_reserved_names_hold_every_module_the_dependencies_look_up_at_load() -> None:
    """C2 of Review C: mpmath imports `gmpy2` as it loads, so a `gmpy2.py` beside
    `exactsolve.py` ran in its place. Every top-level module the dependencies look up
    while the vendored imports load is measured here, with the optional ones present and
    with them hidden, and each must be reserved."""
    imported: set[str] = set()
    for source in sorted(vendored.VENDORED.rglob("*.py")):
        for node in ast.walk(ast.parse(source.read_bytes(), str(source))):
            if isinstance(node, ast.Import):
                imported |= {alias.name for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imported.add(node.module)
    modules = sorted(
        name for name in imported if name.partition(".")[0] in vendored.DEPENDENCIES
    )
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("MPMATH_", "SYMPY_", "SAGE_"))
    }
    runs = [
        subprocess.Popen(
            (
                sys.executable,
                "-I",
                "-c",
                _LOOKUPS,
                json.dumps(modules),
                json.dumps(sorted(vendored.DEPENDENCIES)),
                hide,
            ),
            stdout=subprocess.PIPE,
            text=True,
            env=environment,
        )
        for hide in ("keep", "hide")
    ]
    seen: set[str] = set()
    for run in runs:
        output, _ = run.communicate(timeout=120)
        assert run.returncode == 0
        seen |= {name.partition(".")[0] for name in json.loads(output)}
    assert {"gmpy", "gmpy2", "mpmath", "numpy"} <= seen
    assert seen - vendored.RESERVED_MODULES == set()


def test_the_manifest_must_name_the_upstream_this_tool_fetches_from(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    directory = _copy(tmp_path)
    assert vendored.main(["--directory", str(directory)]) == 1
    assert (
        "`source_url` is https://example.invalid/upstream, not "
        "https://github.com/evand/square-packing"
    ) in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Re-pinning: the commit, the mode and links
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("commit", ["--output={target}", "HEAD", "-1", "0123abc"])
def test_a_commit_that_is_not_a_full_id_is_refused_before_git_sees_it(
    tmp_path: Path, upstream: Path, capsys: pytest.CaptureFixture[str], commit: str
) -> None:
    """B2 of Review B: `--commit=--output=PATH` once had `git log` write PATH."""
    checkout = upstream
    directory = _copy(tmp_path / "project")
    target = tmp_path / "injected.txt"
    argv = [
        "--write",
        "--directory",
        str(directory),
        "--checkout",
        str(checkout),
        f"--commit={commit.format(target=target)}",
    ]
    before = (directory / vendored.MANIFEST_NAME).read_text()
    assert vendored.main(argv) == 1
    assert "--commit must be the full 40-digit commit id" in capsys.readouterr().err
    assert not target.exists()
    assert (directory / vendored.MANIFEST_NAME).read_text() == before


def test_a_repin_refuses_a_checkout_whose_origin_is_not_upstream(
    tmp_path: Path, upstream: Path
) -> None:
    _git(upstream, "remote", "set-url", "origin", "https://example.invalid/a-fork.git")
    directory = _copy(tmp_path / "project")
    with pytest.raises(
        vendored.ManifestError,
        match=re.escape("the checkout's origin is https://example.invalid/a-fork"),
    ):
        vendored.repin(directory, upstream, commit=_head(upstream), retrieved="2026-10-12")


def test_a_full_id_the_checkout_does_not_hold_is_a_refusal_not_a_traceback(
    tmp_path: Path, upstream: Path
) -> None:
    checkout = upstream
    directory = _copy(tmp_path / "project")
    with pytest.raises(vendored.ManifestError, match="is not a commit in"):
        vendored.repin(directory, checkout, commit="f" * 40, retrieved="2026-10-12")


def test_a_repin_records_upstream_modes_and_refuses_links(
    tmp_path: Path, upstream: Path
) -> None:
    checkout = upstream
    for root in (checkout, _copy(tmp_path / "project")):
        script = root / "search/tool.py"
        script.chmod(script.stat().st_mode | stat.S_IXUSR)
    _git(checkout, "commit", "-q", "-a", "-m", "tool.py is executable")
    directory = tmp_path / "project" / "vendor" / "upstream"
    text = vendored.repin(directory, checkout, commit=_head(checkout), retrieved="2026-10-12")
    tool = UPSTREAM["search/tool.py"]
    assert (
        f"{{path: search/tool.py, bytes: {len(tool)}, "
        f"sha256: {hashlib.sha256(tool).hexdigest()}, executable: true}}"
    ) in text
    assert text.count(", executable: true}") == 1
    (directory / vendored.MANIFEST_NAME).write_text(text, encoding="utf-8")
    assert (
        vendored.load_manifest(directory / vendored.MANIFEST_NAME)
        .files["search/tool.py"]
        .executable
    )
    assert _problems(directory) == []
    script = directory / "search/tool.py"
    script.chmod(script.stat().st_mode & ~0o111)
    with pytest.raises(
        vendored.ManifestError, match=re.escape("search/tool.py: not upstream's mode")
    ):
        vendored.repin(directory, checkout, commit=_head(checkout), retrieved="2026-10-12")
    script.chmod(script.stat().st_mode | stat.S_IXUSR)
    (directory / "search/data.json").unlink()
    (directory / "search/data.json").symlink_to(checkout / "search/data.json")
    with pytest.raises(
        vendored.ManifestError, match=re.escape("search/data.json: a symbolic link")
    ):
        vendored.repin(directory, checkout, commit=_head(checkout), retrieved="2026-10-12")


# ---------------------------------------------------------------------------
# --upstream: the manifest against a local upstream repository
# ---------------------------------------------------------------------------


@pytest.fixture
def pinned_copy(tmp_path: Path, upstream: Path) -> Path:
    """A copy re-pinned from a local upstream that `--upstream` may fetch from."""
    checkout = upstream
    directory = _copy(tmp_path / "project")
    text = vendored.repin(directory, checkout, commit=_head(checkout), retrieved="2026-10-12")
    (directory / vendored.MANIFEST_NAME).write_text(text, encoding="utf-8")
    return directory


def _upstream_run(directory: Path, capsys: pytest.CaptureFixture[str]) -> tuple[int, str]:
    status = vendored.main(["--directory", str(directory), "--upstream"])
    captured = capsys.readouterr()
    return status, captured.out + captured.err


def test_upstream_mode_passes_a_faithful_copy(
    pinned_copy: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    status, output = _upstream_run(pinned_copy, capsys)
    assert status == 0, output
    assert (
        "vendored.yaml matches upstream at that commit, on upstream's branch main, "
        "by tree, Git blob ids"
    ) in output


def test_upstream_mode_refuses_an_edit_the_manifest_was_edited_to_hide(
    pinned_copy: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """R2 of Review B: the offline check passes this; only upstream can refuse it."""
    (pinned_copy / "search/tool.py").write_bytes(b"import os; os.system('id')\n")
    _pin(pinned_copy, "search/tool.py")
    assert _problems(pinned_copy) == []
    status, output = _upstream_run(pinned_copy, capsys)
    assert status == 1
    assert "search/tool.py: Git blob " in output
    assert "not upstream's" in output


def test_upstream_mode_refuses_a_file_upstream_never_had(
    pinned_copy: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (pinned_copy / "search/helper.py").write_bytes(b"x = 1\n")
    _pin(pinned_copy, "search/helper.py")
    assert _problems(pinned_copy) == []
    status, output = _upstream_run(pinned_copy, capsys)
    assert status == 1
    assert "search/helper.py: pinned, but upstream's tree at " in output


def test_upstream_mode_refuses_a_mode_upstream_does_not_have(
    pinned_copy: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    script = pinned_copy / "search/tool.py"
    script.chmod(script.stat().st_mode | stat.S_IXUSR)
    _pin(pinned_copy, "search/tool.py", executable=True)
    assert _problems(pinned_copy) == []
    status, output = _upstream_run(pinned_copy, capsys)
    assert status == 1
    assert "search/tool.py: vendored.yaml pins mode 100755, upstream's is 100644" in output


@pytest.mark.parametrize("key", ["git_tree", "committed", "subject"])
def test_upstream_mode_holds_the_recorded_commit_fields(
    pinned_copy: Path, capsys: pytest.CaptureFixture[str], key: str
) -> None:
    manifest = pinned_copy / vendored.MANIFEST_NAME
    record = safe_load(manifest.read_text())
    forged = {"git_tree": "e" * 40, "committed": "2026-01-01T00:00:00Z", "subject": "other"}
    text = manifest.read_text().replace(str(record[key]), forged[key], 1)
    manifest.write_text(text, encoding="utf-8")
    status, output = _upstream_run(pinned_copy, capsys)
    assert status == 1
    assert f"vendored.yaml: `{key}` is {forged[key]!r}, but " in output


def test_upstream_mode_holds_a_modified_files_pinned_entry_to_the_blob(
    pinned_copy: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    manifest = pinned_copy / vendored.MANIFEST_NAME
    manifest.write_text(
        manifest.read_text().replace(
            "local_changes: []", f"local_changes: {_change('search/data.json', 'modified')}"
        ),
        encoding="utf-8",
    )
    (pinned_copy / "search/data.json").write_bytes(b'{"n": 2}\n')
    _describe(pinned_copy, "`search/data.json` holds 2.")
    status, output = _upstream_run(pinned_copy, capsys)
    assert status == 0, output
    pristine = hashlib.sha256(UPSTREAM["search/data.json"]).hexdigest()
    manifest.write_text(manifest.read_text().replace(pristine, "a" * 64), encoding="utf-8")
    status, output = _upstream_run(pinned_copy, capsys)
    assert status == 1
    assert "search/data.json: the pinned size and SHA-256 are not upstream's blob" in output


def test_upstream_mode_never_fetches_from_another_source(
    pinned_copy: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(vendored, "UPSTREAM_URL", "https://example.invalid/the-real-one")

    def refuse(*_arguments: object) -> Path:
        pytest.fail("fetched from a source the tool was not written for")

    monkeypatch.setattr(vendored, "fetch_pin", refuse)
    status, output = _upstream_run(pinned_copy, capsys)
    assert status == 1
    assert "not https://example.invalid/the-real-one" in output


# ---------------------------------------------------------------------------
# --upstream and --write: the pin must be upstream's, not merely served by it
# ---------------------------------------------------------------------------


def _move_pin_off_main(upstream: Path) -> str:
    """Leave upstream's pinned commit under `refs/pull/1/head` alone, as GitHub keeps a
    pull request's head: `main` steps back to a commit of its own, and the pin is on no
    branch or tag. It changes no vendored file, so only reachability can refuse it."""
    pin = _head(upstream)
    _git(upstream, "update-ref", "refs/pull/1/head", pin)
    _git(upstream, "checkout", "-q", "--orphan", "fresh")
    _git(upstream, "commit", "-q", "-m", "main without the pull request")
    _git(upstream, "branch", "-q", "-f", "main", "fresh")
    _git(upstream, "checkout", "-q", "main")
    _git(upstream, "branch", "-q", "-D", "fresh")
    return pin


def test_upstream_mode_refuses_a_pin_held_only_by_a_pull_request(
    pinned_copy: Path,
    upstream: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """C1 of Review C: GitHub serves `refs/pull/N/head` by id through upstream's URL, so a
    third party's unmerged commit once passed `--upstream` as upstream's."""
    pin = _move_pin_off_main(upstream)
    assert _git(upstream, "for-each-ref", f"--contains={pin}", "--format=%(refname)") == (
        "refs/pull/1/head"
    )

    def refuse(*_arguments: object) -> Path:
        pytest.fail("fetched a pin no upstream branch or tag holds")

    monkeypatch.setattr(vendored, "fetch_pin", refuse)
    status, output = _upstream_run(pinned_copy, capsys)
    assert status == 1
    assert f"`source_commit` {pin[:12]} is on no branch or tag of {upstream.as_uri()}" in output


def test_a_repin_refuses_a_commit_held_only_by_a_pull_request(
    tmp_path: Path, upstream: Path
) -> None:
    pin = _move_pin_off_main(upstream)
    directory = _copy(tmp_path / "project")
    with pytest.raises(vendored.ManifestError, match="is on no branch or tag of"):
        vendored.repin(directory, upstream, commit=pin, retrieved="2026-10-13")


def test_upstream_mode_accepts_a_pin_a_tag_holds_and_names_it(
    pinned_copy: Path, upstream: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    pin = _move_pin_off_main(upstream)
    _git(upstream, "tag", "exact-data", pin)
    status, output = _upstream_run(pinned_copy, capsys)
    assert status == 0, output
    assert "on upstream's tag exact-data, by tree" in output
