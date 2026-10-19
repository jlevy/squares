"""Hosted data: stage, check, fetch and publish against a fake release, with no network."""

from __future__ import annotations

import hashlib
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest

from devtools import hosted_data as cli
from sqpack import hosted_data
from sqpack.hosted_data import (
    MAX_OBJECTS,
    HostedDataError,
    HostedDataMissingError,
    HostedObject,
    Manifest,
    RemoteAsset,
    check,
    committed_manifests,
    fetch,
    load_manifest,
    publish,
    render_manifest,
    require,
    require_from_manifest,
    schema_problems,
    stage,
)
from sqpack.yamlio import load_yaml

REPOSITORY = "jlevy/squares"
TAG = "data/fixture-v1"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class FakeRelease:
    """A `ReleaseClient` holding releases in memory; ``served`` overrides what downloads see."""

    def __init__(self, *, digests: bool = True) -> None:
        self.releases: dict[str, dict[str, bytes]] = {}
        self.served: dict[str, bytes] = {}
        self.digests = digests
        self.created: list[tuple[str, str, str, str | None]] = []
        self.uploaded: list[str] = []

    def assets(self, repository: str, tag: str) -> dict[str, RemoteAsset] | None:
        assert repository == REPOSITORY
        held = self.releases.get(tag)
        if held is None:
            return None
        return {
            name: RemoteAsset(name, len(data), f"sha256:{_sha(data)}" if self.digests else None)
            for name, data in held.items()
        }

    def create(
        self, repository: str, tag: str, *, title: str, notes: str, target: str | None
    ) -> None:
        assert repository == REPOSITORY
        assert tag not in self.releases
        self.created.append((tag, title, notes, target))
        self.releases[tag] = {}

    def upload(self, repository: str, tag: str, source: Path, asset: str) -> None:
        assert repository == REPOSITORY
        assert asset not in self.releases[tag], "an existing asset must never be replaced"
        self.releases[tag][asset] = source.read_bytes()
        self.uploaded.append(asset)

    def download(self, repository: str, tag: str, asset: str, destination: Path) -> None:
        assert repository == REPOSITORY
        destination.write_bytes(self.served.get(asset, self.releases[tag][asset]))


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A Git checkout that ignores ``data/``, holding two small objects there."""
    root = tmp_path / "repo"
    (root / "data" / "nested").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    (root / ".gitignore").write_text("data/\n", encoding="utf-8")
    (root / "data" / "alpha.bin").write_bytes(b"alpha bytes")
    (root / "data" / "nested" / "beta.json.gz").write_bytes(b"beta bytes, longer")
    return root


def _staged(repo: Path) -> tuple[Path, Manifest]:
    path = repo / "manifest.yaml"
    return path, stage(path, repo / "data", repo, repository=REPOSITORY, tag=TAG)


def _published(repo: Path, manifest: Manifest) -> FakeRelease:
    release = FakeRelease()
    publish(manifest, repo, release, title=TAG, notes="fixture")
    return release


def _leftovers(directory: Path) -> list[str]:
    return sorted(path.name for path in directory.iterdir() if path.name.startswith("."))


def test_stage_writes_a_manifest_that_meets_its_contract_and_passes_check(repo: Path) -> None:
    path, manifest = _staged(repo)
    assert [item.path for item in manifest.objects] == [
        "data/alpha.bin",
        "data/nested/beta.json.gz",
    ]
    assert manifest.objects[0] == HostedObject(
        "data/alpha.bin", "alpha.bin", 11, _sha(b"alpha bytes")
    )
    assert load_manifest(path) == manifest
    assert load_yaml(path.read_text(encoding="utf-8"))["softschema"]["status"] == "enforced"
    assert check(manifest, repo) == []


def test_restaging_keeps_names_and_descriptions_and_takes_the_new_digest(repo: Path) -> None:
    path, manifest = _staged(repo)
    described = Manifest(
        manifest.repository,
        manifest.tag,
        (replace(manifest.objects[0], description="kept"), *manifest.objects[1:]),
    )
    path.write_text(render_manifest(described, path), encoding="utf-8")
    (repo / "data" / "alpha.bin").write_bytes(b"alpha, regenerated")
    restaged = stage(path, repo / "data", repo)
    assert restaged.objects[0].description == "kept"
    assert restaged.objects[0].sha256 == _sha(b"alpha, regenerated")
    assert restaged.tag == TAG


def test_stage_refuses_two_files_under_one_asset_name(repo: Path) -> None:
    (repo / "data" / "nested" / "alpha.bin").write_bytes(b"another alpha")
    with pytest.raises(HostedDataError, match="asset name collision"):
        _staged(repo)
    assert not (repo / "manifest.yaml").exists()


def test_stage_refuses_a_tag_outside_the_data_namespace(repo: Path) -> None:
    with pytest.raises(HostedDataError, match="tag"):
        stage(repo / "m.yaml", repo / "data", repo, repository=REPOSITORY, tag="v1.0.0")
    assert not (repo / "m.yaml").exists()


def test_check_refuses_a_path_that_is_not_git_ignored(repo: Path) -> None:
    (repo / "kept").mkdir()
    (repo / "kept" / "gamma.bin").write_bytes(b"gamma")
    manifest = stage(repo / "m.yaml", repo / "kept", repo, repository=REPOSITORY, tag=TAG)
    assert check(manifest, repo) == [
        "kept/gamma.bin: not git-ignored; add it to .gitignore so the bytes cannot be committed"
    ]


def test_check_refuses_a_tracked_file_even_under_an_ignore_rule(repo: Path) -> None:
    _, manifest = _staged(repo)
    subprocess.run(["git", "-C", str(repo), "add", "-f", "data/alpha.bin"], check=True)
    assert check(manifest, repo) == [
        "data/alpha.bin: not git-ignored; add it to .gitignore so the bytes cannot be committed"
    ]


def test_check_refuses_repeated_names_and_unplain_paths(repo: Path) -> None:
    item = HostedObject("data/alpha.bin", "alpha.bin", 1, "0" * 64)
    odd = HostedObject("data/../alpha.bin", "other.bin", 1, "0" * 64)
    problems = check(Manifest(REPOSITORY, TAG, (item, item, odd)), repo)
    assert "path data/alpha.bin appears more than once" in problems
    assert "asset alpha.bin appears more than once" in problems
    assert "data/../alpha.bin: not a plain repository-relative path" in problems


def test_more_than_a_thousand_objects_is_refused(repo: Path) -> None:
    objects = [
        HostedObject(f"data/{index}.bin", f"{index}.bin", 1, "0" * 64)
        for index in range(MAX_OBJECTS + 1)
    ]
    document = load_yaml(render_manifest(Manifest(REPOSITORY, TAG, tuple(objects)), repo / "m"))
    assert schema_problems(document) == [
        "1001 objects: a release holds at most 1000 assets; pack small files into a tarball"
    ]
    document["objects"] = document["objects"][:MAX_OBJECTS]
    assert schema_problems(document) == []


def test_an_object_of_two_gibibytes_is_refused() -> None:
    document = {
        "softschema": {"contract": hosted_data.CONTRACT, "schema": "s", "status": "enforced"},
        "repository": REPOSITORY,
        "tag": TAG,
        "objects": [{"path": "data/a", "asset": "a", "size": 2**31, "sha256": "0" * 64}],
    }
    assert [problem.split(":")[0] for problem in schema_problems(document)] == [
        "objects/0/size"
    ]


def test_fetch_downloads_verifies_and_then_skips_what_is_present(repo: Path) -> None:
    path, manifest = _staged(repo)
    release = _published(repo, manifest)
    for item in manifest.objects:
        (repo / item.path).unlink()
    fetched = fetch(load_manifest(path), repo, release)
    assert [outcome.action for outcome in fetched] == ["fetched", "fetched"]
    assert (repo / "data" / "nested" / "beta.json.gz").read_bytes() == b"beta bytes, longer"
    again = fetch(manifest, repo, release, only="*.gz")
    assert [(outcome.path, outcome.action) for outcome in again] == [
        ("data/nested/beta.json.gz", "present")
    ]
    assert _leftovers(repo / "data") == []


@pytest.mark.parametrize(
    ("served", "reason"),
    [(b"alpha BYTES", "sha256"), (b"alpha bytes!", "size 12, manifest says 11")],
)
def test_fetch_refuses_bytes_that_differ_and_writes_nothing(
    repo: Path, served: bytes, reason: str
) -> None:
    _, manifest = _staged(repo)
    release = _published(repo, manifest)
    (repo / "data" / "alpha.bin").unlink()
    release.served["alpha.bin"] = served
    with pytest.raises(HostedDataError, match=reason):
        fetch(manifest, repo, release, only="alpha.bin")
    assert not (repo / "data" / "alpha.bin").exists()
    assert _leftovers(repo / "data") == []


def test_fetch_will_not_overwrite_a_present_file_that_differs_unless_asked(repo: Path) -> None:
    _, manifest = _staged(repo)
    release = _published(repo, manifest)
    (repo / "data" / "alpha.bin").write_bytes(b"unstaged regeneration")
    with pytest.raises(HostedDataError, match="--replace"):
        fetch(manifest, repo, release, only="alpha.bin")
    assert (repo / "data" / "alpha.bin").read_bytes() == b"unstaged regeneration"
    fetch(manifest, repo, release, only="alpha.bin", replace_local=True)
    assert (repo / "data" / "alpha.bin").read_bytes() == b"alpha bytes"


def test_a_failed_download_leaves_no_partial_file(repo: Path) -> None:
    _, manifest = _staged(repo)
    release = _published(repo, manifest)
    (repo / "data" / "alpha.bin").unlink()

    class Interrupted(FakeRelease):
        def download(self, repository: str, tag: str, asset: str, destination: Path) -> None:
            del repository, tag, asset
            destination.write_bytes(b"alph")
            raise ConnectionResetError("connection reset mid-transfer")

    broken = Interrupted()
    broken.releases = release.releases
    with pytest.raises(ConnectionResetError):
        fetch(manifest, repo, broken, only="alpha.bin")
    assert sorted(path.name for path in (repo / "data").iterdir()) == ["nested"]


def test_publish_creates_a_release_off_latest_uploads_and_verifies_once(repo: Path) -> None:
    _, manifest = _staged(repo)
    release = FakeRelease()
    first = publish(manifest, repo, release, title="Fixture data", notes="n", target="abc123")
    assert release.created == [(TAG, "Fixture data", "n", "abc123")]
    assert first.created
    assert first.uploaded == ("alpha.bin", "beta.json.gz")
    assert first.verified == ("alpha.bin", "beta.json.gz")
    second = publish(manifest, repo, release, title="Fixture data", notes="n")
    assert not second.created
    assert second.uploaded == ()
    assert second.already_present == ("alpha.bin", "beta.json.gz")
    assert release.uploaded == ["alpha.bin", "beta.json.gz"]
    assert _leftovers(repo / "data") == []


@pytest.mark.parametrize("digests", [True, False])
def test_publish_refuses_an_existing_asset_with_different_bytes(
    repo: Path, *, digests: bool
) -> None:
    _, manifest = _staged(repo)
    release = FakeRelease(digests=digests)
    release.releases[TAG] = {"alpha.bin": b"ALPHA BYTES"}
    with pytest.raises(HostedDataError, match=r"never rewritten.*Bump the tag"):
        publish(manifest, repo, release, title=TAG, notes="n")
    assert release.uploaded == []
    assert release.releases[TAG] == {"alpha.bin": b"ALPHA BYTES"}


def test_publish_refuses_local_bytes_that_no_longer_match_the_manifest(repo: Path) -> None:
    _, manifest = _staged(repo)
    (repo / "data" / "alpha.bin").write_bytes(b"changed after staging")
    release = FakeRelease()
    with pytest.raises(HostedDataError, match="stage it again"):
        publish(manifest, repo, release, title=TAG, notes="n")
    assert release.created == []


def test_publish_refuses_to_exceed_the_asset_limit(repo: Path) -> None:
    _, manifest = _staged(repo)
    release = FakeRelease()
    release.releases[TAG] = {f"other-{index}": b"x" for index in range(MAX_OBJECTS - 1)}
    with pytest.raises(HostedDataError, match="would hold 1001 assets"):
        publish(manifest, repo, release, title=TAG, notes="n")
    assert release.uploaded == []


def test_require_names_the_fetch_command_when_an_object_is_absent(
    repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path, _ = _staged(repo)
    monkeypatch.setattr(hosted_data, "repository_root", lambda: repo)
    assert require("data/alpha.bin", path) == repo / "data" / "alpha.bin"
    (repo / "data" / "alpha.bin").unlink()
    with pytest.raises(HostedDataMissingError, match=r"devtools\.hosted_data fetch --manifest"):
        require(repo / "data" / "alpha.bin", path)
    with pytest.raises(FileNotFoundError):
        require("data/alpha.bin", path)
    (repo / "data" / "alpha.bin").write_bytes(b"stale")
    with pytest.raises(HostedDataError, match="differs from its manifest"):
        require("data/alpha.bin", path)


@pytest.mark.parametrize("changed", [b"stale", b"other bytes"])
def test_loaded_manifest_checks_each_object_and_new_readers_admit_fresh_bytes(
    repo: Path, changed: bytes
) -> None:
    path, admitted = _staged(repo)
    alpha = repo / "data/alpha.bin"
    original = alpha.read_bytes()
    assert require_from_manifest(alpha, admitted, path, repo=repo) == alpha
    alpha.write_bytes(changed)
    with pytest.raises(HostedDataError, match="differs from its manifest"):
        require_from_manifest(alpha, admitted, path, repo=repo)
    # A new invocation must read the newly admitted manifest, while the existing
    # transaction continues to enforce the bytes it admitted at its own start.
    _staged(repo)
    assert require(alpha, path, repo=repo) == alpha
    with pytest.raises(HostedDataError, match="differs from its manifest"):
        require_from_manifest(alpha, admitted, path, repo=repo)
    alpha.write_bytes(original)
    assert require_from_manifest(alpha, admitted, path, repo=repo) == alpha
    with pytest.raises(HostedDataError, match="differs from its manifest"):
        require(alpha, path, repo=repo)
    alpha.unlink()
    with pytest.raises(HostedDataMissingError, match="not in this checkout"):
        require_from_manifest(alpha, admitted, path, repo=repo)
    with pytest.raises(HostedDataError, match="is not named"):
        require_from_manifest("data/unknown.bin", admitted, path, repo=repo)


def test_an_upload_refused_by_the_upload_host_names_the_host_and_the_remedy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The first real publish met HTTP 403 from uploads.github.com, an egress refusal,
    after the release was created; the error says which host and what to do."""
    source = tmp_path / "alpha.bin"
    source.write_bytes(b"alpha bytes")
    url = "https://uploads.github.com/repos/jlevy/squares/releases/1/assets?name=alpha.bin"
    calls: list[tuple[str, ...]] = []

    def refused(
        _self: hosted_data.GhClient, *arguments: str
    ) -> subprocess.CompletedProcess[str]:
        calls.append(arguments)
        return subprocess.CompletedProcess(
            ["gh", *arguments], 1, "", f"HTTP 403: 403 Forbidden ({url})\n"
        )

    monkeypatch.setattr(hosted_data.GhClient, "_run", refused)
    client = hosted_data.GhClient()
    with pytest.raises(HostedDataError) as caught:
        client.upload(REPOSITORY, TAG, source, "alpha.bin")
    message = str(caught.value)
    assert "refused with HTTP 403 by uploads.github.com" in message
    assert "network access" in message
    assert "run publish again" in message
    assert url in message
    assert "--clobber" not in calls[0]

    def failed(
        _self: hosted_data.GhClient, *arguments: str
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(["gh", *arguments], 1, "", "HTTP 502: Bad Gateway")

    monkeypatch.setattr(hosted_data.GhClient, "_run", failed)
    with pytest.raises(
        HostedDataError, match=r"gh release upload failed for alpha\.bin: HTTP 502"
    ):
        client.upload(REPOSITORY, TAG, source, "alpha.bin")


def test_require_reads_paths_under_a_root_the_caller_passes(repo: Path) -> None:
    """A tool with its own root finds objects there, never under the repository root."""
    path, _ = _staged(repo)
    beta = repo / "data" / "nested" / "beta.json.gz"
    assert require("data/nested/beta.json.gz", path, repo=repo) == beta
    assert require(beta, path, repo=repo) == beta
    beta.unlink()
    with pytest.raises(HostedDataMissingError, match="not in this checkout"):
        require("data/nested/beta.json.gz", path, repo=repo)


def test_the_command_line_stages_and_checks(
    repo: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(cli, "repository_root", lambda: repo)
    manifest = str(repo / "m.yaml")
    arguments = ["stage", "--manifest", manifest, "--from", str(repo / "data")]
    assert cli.main([*arguments, "--repository", REPOSITORY, "--tag", TAG]) == 0
    assert "2 objects" in capsys.readouterr().out
    assert cli.main(["check", "--manifest", manifest]) == 0
    (repo / ".gitignore").write_text("", encoding="utf-8")
    assert cli.main(["check", "--manifest", manifest]) == 1
    assert "data/alpha.bin: not git-ignored" in capsys.readouterr().err


def test_every_committed_manifest_passes_check() -> None:
    repo = hosted_data.repository_root()
    problems = [
        f"{path.name}: {problem}"
        for path in committed_manifests()
        for problem in check(load_manifest(path), repo)
    ]
    assert problems == []
