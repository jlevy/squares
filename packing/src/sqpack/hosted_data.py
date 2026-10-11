"""Bulk data hosted as GitHub release assets, named by a committed manifest (OR-18).

Git keeps source, records and data small enough to review. A dump or binary of more than
a few megabytes is published as an asset on a GitHub release instead, and the repository
keeps a manifest naming each object: where it lives once fetched, its asset name, its size
and its SHA-256. The manifest's contract is ``packing/hosted/hosted-data.schema.yaml``,
and every manifest lives beside it in ``packing/hosted/``.

The SHA-256 is justified under OR-16 because a download crosses a trust boundary, so
`fetch` compares every byte it receives and writes nothing that fails. Nothing here reads
a Git revision or pins a file the repository writes: an object is found by its path, and
Git is asked only whether that path is ignored.

A release's bytes never change. `publish` uploads only the assets a release lacks and
refuses an existing asset whose bytes differ; different bytes go out under the next tag
version. It never deletes or replaces an asset, because `gh release upload --clobber`
deletes the old asset before uploading, and an upload that then fails leaves nothing.

Every network call goes through a `ReleaseClient`; `GhClient` is the one that runs `gh`,
and the tests pass a fake. A tool that reads hosted data calls `require`, which returns
the local path or raises `HostedDataMissingError` naming the command that fetches it.
"""

from __future__ import annotations

import fnmatch
import hashlib
import os
import subprocess
import tempfile
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Protocol

import yaml
from jsonschema_rs import Draft202012Validator

from sqpack.project import require_project_root
from sqpack.yamlio import load_yaml, safe_load

CONTRACT = "packing.squares:HostedData/v1"
SCHEMA_NAME = "hosted-data.schema.yaml"
#: GitHub refuses a 1001st asset on one release with HTTP 422.
MAX_OBJECTS = 1000
#: An object must be smaller than this: GitHub refuses a release asset of 2 GiB or more.
MAX_OBJECT_BYTES = 2 * 1024**3
#: The host GitHub takes release asset uploads on, apart from the API host.
UPLOAD_HOST = "uploads.github.com"
_CHUNK = 1 << 20


class HostedDataError(Exception):
    """A manifest, a local object or a release disagrees with what the manifest says."""


class HostedDataMissingError(HostedDataError, FileNotFoundError):
    """A hosted object is absent from this checkout; the message names the fetch command."""


def project_root() -> Path:
    """``packing/``, where the commands run."""
    return require_project_root()


def repository_root() -> Path:
    """The repository root, which every object path is relative to."""
    return project_root().parent


def hosted_directory() -> Path:
    """``packing/hosted/``: the schema and every committed manifest."""
    return project_root() / "hosted"


def committed_manifests() -> list[Path]:
    """Every manifest in ``packing/hosted/``, in name order."""
    return sorted(
        path
        for path in hosted_directory().glob("*.yaml")
        if not path.name.endswith(".schema.yaml")
    )


@dataclass(frozen=True, slots=True)
class HostedObject:
    path: str
    asset: str
    size: int
    sha256: str
    description: str | None = None

    def record(self) -> dict[str, object]:
        fields: dict[str, object] = {
            "path": self.path,
            "asset": self.asset,
            "size": self.size,
            "sha256": self.sha256,
        }
        if self.description:
            fields["description"] = self.description
        return fields


@dataclass(frozen=True, slots=True)
class Manifest:
    repository: str
    tag: str
    objects: tuple[HostedObject, ...]
    description: str | None = None

    def find(self, path: str) -> HostedObject | None:
        return next((item for item in self.objects if item.path == path), None)

    @property
    def total_size(self) -> int:
        return sum(item.size for item in self.objects)


def _validator() -> Draft202012Validator:
    schema = hosted_directory() / SCHEMA_NAME
    return Draft202012Validator(safe_load(schema.read_text(encoding="utf-8")))


def schema_problems(document: object) -> list[str]:
    """The manifest document against its contract, the object count included."""
    if not isinstance(document, dict):
        return ["the manifest is not a mapping"]
    meta = document.get("softschema")
    meta = meta if isinstance(meta, dict) else {}
    problems = [
        f"softschema.{key} missing" for key in ("contract", "schema") if key not in meta
    ]
    if meta.get("contract", CONTRACT) != CONTRACT:
        problems.append(f"softschema.contract is {meta['contract']!r}, expected {CONTRACT!r}")
    if meta.get("status") != "enforced":
        problems.append("softschema.status must be 'enforced'")
    payload = {key: value for key, value in document.items() if key != "softschema"}
    objects = payload.get("objects")
    if isinstance(objects, list) and len(objects) > MAX_OBJECTS:
        # Reported here rather than by `maxItems`, whose message would print every object.
        problems.append(
            f"{len(objects)} objects: a release holds at most {MAX_OBJECTS} assets; "
            "pack small files into a tarball"
        )
        payload["objects"] = objects[:MAX_OBJECTS]
    for error in _validator().iter_errors(payload):
        where = "/".join(str(part) for part in error.instance_path) or "<root>"
        problems.append(f"{where}: {error.message}")
    return problems


def _parse(document: dict[str, Any]) -> Manifest:
    return Manifest(
        repository=document["repository"],
        tag=document["tag"],
        description=document.get("description"),
        objects=tuple(
            HostedObject(
                path=item["path"],
                asset=item["asset"],
                size=item["size"],
                sha256=item["sha256"],
                description=item.get("description"),
            )
            for item in document["objects"]
        ),
    )


def load_manifest(path: Path) -> Manifest:
    """The manifest at ``path``, refused unless it meets its contract."""
    document = load_yaml(path.read_text(encoding="utf-8"))
    problems = schema_problems(document)
    if problems:
        raise HostedDataError(f"{path}: " + "; ".join(problems))
    return _parse(document)


def render_manifest(manifest: Manifest, location: Path) -> str:
    """The manifest's YAML, its softschema header naming the schema relative to ``location``."""
    schema = os.path.relpath(hosted_directory() / SCHEMA_NAME, location.parent)
    header = {"contract": CONTRACT, "schema": Path(schema).as_posix(), "status": "enforced"}
    body: dict[str, object] = {"repository": manifest.repository, "tag": manifest.tag}
    if manifest.description:
        body["description"] = manifest.description
    body["objects"] = [item.record() for item in manifest.objects]

    def dump(value: object) -> str:
        return yaml.safe_dump(value, sort_keys=False, width=100, allow_unicode=True)

    return dump({"softschema": header}) + "\n" + dump(body)


def git_ignored(repo: Path, paths: Sequence[str]) -> set[str]:
    """The paths Git ignores. A tracked file is never ignored, so it is never returned."""
    if not paths:
        return set()
    result = subprocess.run(
        ["git", "-C", str(repo), "check-ignore", "--stdin", "-z"],
        input="".join(f"{path}\0" for path in paths),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode not in (0, 1):
        raise HostedDataError(f"git check-ignore failed: {result.stderr.strip()}")
    return {path for path in result.stdout.split("\0") if path}


def check(manifest: Manifest, repo: Path) -> list[str]:
    """What a schema cannot state: unique names, plain relative paths, all git-ignored."""
    problems: list[str] = []
    for label, names in (
        ("path", [item.path for item in manifest.objects]),
        ("asset", [item.asset for item in manifest.objects]),
    ):
        repeated = sorted({name for name in names if names.count(name) > 1})
        problems += [f"{label} {name} appears more than once" for name in repeated]
    plain: list[str] = []
    for item in manifest.objects:
        if any(part in {"", ".", ".."} for part in item.path.split("/")):
            problems.append(f"{item.path}: not a plain repository-relative path")
        else:
            plain.append(item.path)
    hidden = git_ignored(repo, plain)
    problems += [
        f"{path}: not git-ignored; add it to .gitignore so the bytes cannot be committed"
        for path in plain
        if path not in hidden
    ]
    return problems


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(_CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def mismatch(path: Path, item: HostedObject) -> str | None:
    """Why the file at ``path`` is not ``item``'s bytes, or `None` when it is."""
    size = path.stat().st_size
    if size != item.size:
        return f"size {size}, manifest says {item.size}"
    actual = sha256_file(path)
    if actual != item.sha256:
        return f"sha256 {actual}, manifest says {item.sha256}"
    return None


@contextmanager
def atomic_destination(destination: Path) -> Iterator[Path]:
    """A temporary path beside ``destination``, moved into place only if the body succeeds.

    On any failure the temporary file is removed, so a partial download never sits at
    the destination or beside it.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".part", dir=destination.parent
    )
    os.close(handle)
    temporary = Path(name)
    try:
        yield temporary
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


@dataclass(frozen=True, slots=True)
class RemoteAsset:
    name: str
    size: int
    #: ``sha256:<hex>`` as GitHub reports it, or `None` for an asset it has not hashed.
    digest: str | None = None


class ReleaseClient(Protocol):
    def assets(self, repository: str, tag: str) -> dict[str, RemoteAsset] | None:
        """The release's assets by name, or `None` when there is no such release."""
        ...

    def create(
        self, repository: str, tag: str, *, title: str, notes: str, target: str | None
    ) -> None: ...

    def upload(self, repository: str, tag: str, source: Path, asset: str) -> None: ...

    def download(self, repository: str, tag: str, asset: str, destination: Path) -> None: ...


class GhClient:
    """`ReleaseClient` over the GitHub CLI, which brings its own authentication."""

    def _run(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["gh", *arguments], capture_output=True, text=True, check=False)

    def _require(self, *arguments: str) -> str:
        result = self._run(*arguments)
        if result.returncode:
            command = " ".join(arguments[:2] if arguments[0] == "release" else arguments[:1])
            raise HostedDataError(f"gh {command} failed: {result.stderr.strip()}")
        return result.stdout

    def assets(self, repository: str, tag: str) -> dict[str, RemoteAsset] | None:
        release = self._run("api", f"repos/{repository}/releases/tags/{tag}", "--jq", ".id")
        if release.returncode:
            if "HTTP 404" in release.stderr:
                return None
            raise HostedDataError(f"gh api failed: {release.stderr.strip()}")
        rows = self._require(
            "api",
            "--paginate",
            f"repos/{repository}/releases/{release.stdout.strip()}/assets?per_page=100",
            "--jq",
            r'.[] | "\(.name)\t\(.size)\t\(.digest // "")"',
        )
        found: dict[str, RemoteAsset] = {}
        for row in rows.splitlines():
            name, size, digest = row.split("\t")
            found[name] = RemoteAsset(name, int(size), digest or None)
        return found

    def create(
        self, repository: str, tag: str, *, title: str, notes: str, target: str | None
    ) -> None:
        extra = ["--target", target] if target else []
        self._require(
            "release",
            "create",
            tag,
            "--repo",
            repository,
            "--title",
            title,
            "--notes",
            notes,
            "--latest=false",
            *extra,
        )

    def upload(self, repository: str, tag: str, source: Path, asset: str) -> None:
        # Never `--clobber`: it deletes the existing asset before the upload starts.
        with tempfile.TemporaryDirectory() as scratch:
            named = source
            if source.name != asset:
                named = Path(scratch) / asset
                named.symlink_to(source.resolve())
            result = self._run("release", "upload", tag, str(named), "--repo", repository)
        if not result.returncode:
            return
        said = result.stderr.strip()
        if "HTTP 403" in said and UPLOAD_HOST in said:
            # A cloud environment whose egress does not allow the upload host answers
            # 403 there while the API host, and so the release's creation, works.
            raise HostedDataError(
                f"uploading {asset} to {repository}@{tag} was refused with HTTP 403 by "
                f"{UPLOAD_HOST}, the host GitHub takes release assets on. Allow "
                f"{UPLOAD_HOST} in the environment's network access, then run publish "
                "again: it uploads only the assets the release lacks, and nothing was "
                f"replaced. gh said: {said}"
            )
        raise HostedDataError(f"gh release upload failed for {asset}: {said}")

    def download(self, repository: str, tag: str, asset: str, destination: Path) -> None:
        # `--clobber` here overwrites only the caller's own temporary file.
        self._require(
            "release",
            "download",
            tag,
            "--repo",
            repository,
            "--pattern",
            asset,
            "--output",
            str(destination),
            "--clobber",
        )


def fetch_command(manifest_path: Path) -> str:
    """The command, run from ``packing/``, that fetches what ``manifest_path`` names."""
    where = os.path.relpath(manifest_path.resolve(), project_root())
    return f"python -m devtools.hosted_data fetch --manifest {Path(where).as_posix()}"


@dataclass(frozen=True, slots=True)
class Fetched:
    path: str
    #: ``present`` when the local file already matched, ``fetched`` when it was downloaded.
    action: str


def fetch(
    manifest: Manifest,
    repo: Path,
    client: ReleaseClient,
    *,
    only: str | None = None,
    replace_local: bool = False,
) -> list[Fetched]:
    """Download each selected object to its path, verified, skipping those already there.

    ``only`` is a glob matched against each path and asset name. A present file whose
    bytes differ is refused unless ``replace_local``, since it may be data not yet staged.
    """
    selected = [
        item
        for item in manifest.objects
        if only is None or fnmatch.fnmatch(item.path, only) or fnmatch.fnmatch(item.asset, only)
    ]
    if not selected:
        raise HostedDataError(f"no object matches {only!r}")
    outcomes: list[Fetched] = []
    for item in selected:
        local = repo / item.path
        if local.is_file():
            problem = mismatch(local, item)
            if problem is None:
                outcomes.append(Fetched(item.path, "present"))
                continue
            if not replace_local:
                raise HostedDataError(
                    f"{item.path} is present but differs from the manifest ({problem}); "
                    "move it aside, or pass --replace to overwrite it"
                )
        with atomic_destination(local) as temporary:
            client.download(manifest.repository, manifest.tag, item.asset, temporary)
            problem = mismatch(temporary, item)
            if problem:
                raise HostedDataError(
                    f"{item.asset} from {manifest.repository}@{manifest.tag}: {problem}; "
                    "refused, nothing written"
                )
        outcomes.append(Fetched(item.path, "fetched"))
    return outcomes


def require(
    path: str | Path, manifest_path: Path, *, verify: bool = True, repo: Path | None = None
) -> Path:
    """The local file for a hosted object, or `HostedDataMissingError` naming the fetch.

    Paths are relative to ``repo``, the repository root unless a tool that takes its own
    root, such as a census over a fixture tree, passes it.
    """
    return require_from_manifest(
        path, load_manifest(manifest_path), manifest_path, verify=verify, repo=repo
    )


def require_from_manifest(
    path: str | Path,
    manifest: Manifest,
    manifest_path: Path,
    *,
    verify: bool = True,
    repo: Path | None = None,
) -> Path:
    """Check one object against a manifest already admitted for this reader invocation.

    The caller retains a freshly loaded manifest only for its current transaction;
    object presence, size and digest are independently checked on every call.
    """
    repo = repository_root() if repo is None else repo.resolve()
    candidate = Path(path)
    relative = candidate.resolve().relative_to(repo) if candidate.is_absolute() else candidate
    item = manifest.find(relative.as_posix())
    if item is None:
        raise HostedDataError(f"{relative.as_posix()} is not named by {manifest_path}")
    local = repo / item.path
    remedy = f"run `{fetch_command(manifest_path)}` from packing/"
    if not local.is_file():
        raise HostedDataMissingError(
            f"{item.path} is hosted on {manifest.repository}@{manifest.tag}, "
            f"not in this checkout; {remedy}"
        )
    if verify and (problem := mismatch(local, item)):
        raise HostedDataError(f"{item.path} differs from its manifest ({problem}); {remedy}")
    return local


def stage(
    manifest_path: Path,
    source: Path,
    repo: Path,
    *,
    repository: str | None = None,
    tag: str | None = None,
) -> Manifest:
    """Write or update the manifest from every file under ``source``, and return it.

    An object already named keeps its asset name and description and takes the new size
    and digest. Dot-files are skipped. Two paths under one asset name are refused.
    """
    existing = load_manifest(manifest_path) if manifest_path.exists() else None
    repository = repository or (existing.repository if existing else None)
    tag = tag or (existing.tag if existing else None)
    if not repository or not tag:
        raise HostedDataError("a new manifest needs --repository and --tag")
    files = sorted(
        path
        for path in source.rglob("*")
        if path.is_file()
        and not any(part.startswith(".") for part in path.relative_to(source).parts)
    )
    if not files:
        raise HostedDataError(f"no files under {source}")
    objects = {item.path: item for item in (existing.objects if existing else ())}
    root = repo.resolve()
    for file in files:
        try:
            relative = file.resolve().relative_to(root).as_posix()
        except ValueError:
            raise HostedDataError(f"{file} is outside the repository {root}") from None
        size, digest = file.stat().st_size, sha256_file(file)
        if relative in objects:
            objects[relative] = replace(objects[relative], size=size, sha256=digest)
        else:
            objects[relative] = HostedObject(relative, file.name, size, digest)
    owners: dict[str, list[str]] = {}
    for item in objects.values():
        owners.setdefault(item.asset, []).append(item.path)
    collisions = {asset: paths for asset, paths in owners.items() if len(paths) > 1}
    if collisions:
        listed = "; ".join(
            f"{asset}: {', '.join(paths)}" for asset, paths in collisions.items()
        )
        raise HostedDataError(f"asset name collision, rename one file: {listed}")
    manifest = Manifest(
        repository=repository,
        tag=tag,
        description=existing.description if existing else None,
        objects=tuple(objects[key] for key in sorted(objects)),
    )
    text = render_manifest(manifest, manifest_path)
    problems = schema_problems(load_yaml(text))
    if problems:
        raise HostedDataError("refused, manifest not written: " + "; ".join(problems))
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(text, encoding="utf-8")
    return manifest


@dataclass(frozen=True, slots=True)
class Published:
    created: bool
    uploaded: tuple[str, ...]
    already_present: tuple[str, ...]
    #: Assets on the release that the manifest does not name; left alone.
    unnamed: tuple[str, ...]
    verified: tuple[str, ...]


def publish(
    manifest: Manifest,
    repo: Path,
    client: ReleaseClient,
    *,
    title: str,
    notes: str,
    target: str | None = None,
) -> Published:
    """Create the release if absent, upload the assets it lacks, then verify every one.

    Everything that can refuse is checked before anything is created or uploaded: the
    local bytes against the manifest, an existing asset against the manifest, and the
    asset count against GitHub's limit.
    """
    problems: list[str] = []
    for item in manifest.objects:
        local = repo / item.path
        if not local.is_file():
            problems.append(f"{item.path}: absent, nothing to upload")
        elif problem := mismatch(local, item):
            problems.append(f"{item.path}: {problem}; stage it again")
    if problems:
        raise HostedDataError("refused before publishing: " + "; ".join(problems))
    remote = client.assets(manifest.repository, manifest.tag)
    present = remote or {}
    conflicts: list[str] = []
    for item in manifest.objects:
        asset = present.get(item.asset)
        if asset is None:
            continue
        if asset.size != item.size:
            conflicts.append(
                f"{item.asset}: release has {asset.size} bytes, manifest {item.size}"
            )
        elif asset.digest is not None and asset.digest != f"sha256:{item.sha256}":
            conflicts.append(f"{item.asset}: release has {asset.digest}")
        elif asset.digest is None and (
            problem := _served_mismatch(manifest, item, client, repo)
        ):
            conflicts.append(f"{item.asset}: served bytes have {problem}")
    if conflicts:
        raise HostedDataError(
            f"{manifest.tag} already holds different bytes, and a release is never "
            f"rewritten: {'; '.join(conflicts)}. Bump the tag's -v<N> in the manifest, "
            "stage again, and publish the new tag"
        )
    missing = [item for item in manifest.objects if item.asset not in present]
    if len(present) + len(missing) > MAX_OBJECTS:
        raise HostedDataError(
            f"{manifest.tag} would hold {len(present) + len(missing)} assets; "
            f"GitHub allows {MAX_OBJECTS}"
        )
    if remote is None:
        client.create(
            manifest.repository, manifest.tag, title=title, notes=notes, target=target
        )
    for item in missing:
        client.upload(manifest.repository, manifest.tag, repo / item.path, item.asset)
    verified: list[str] = []
    for item in manifest.objects:
        if problem := _served_mismatch(manifest, item, client, repo):
            raise HostedDataError(f"{item.asset} as served by {manifest.tag}: {problem}")
        verified.append(item.asset)
    named = {item.asset for item in manifest.objects}
    return Published(
        created=remote is None,
        uploaded=tuple(item.asset for item in missing),
        already_present=tuple(item.asset for item in manifest.objects if item.asset in present),
        unnamed=tuple(sorted(set(present) - named)),
        verified=tuple(verified),
    )


def _served_mismatch(
    manifest: Manifest, item: HostedObject, client: ReleaseClient, repo: Path
) -> str | None:
    """Download one asset beside its local copy, compare it, and delete the download."""
    local = repo / item.path
    local.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix=f".{local.name}.", suffix=".check", dir=local.parent)
    os.close(handle)
    served = Path(name)
    try:
        client.download(manifest.repository, manifest.tag, item.asset, served)
        return mismatch(served, item)
    finally:
        served.unlink(missing_ok=True)
